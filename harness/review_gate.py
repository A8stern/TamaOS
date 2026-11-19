#!/usr/bin/env python3
"""Validate local three-lane review evidence for the current commit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


LANES = ("correctness", "architecture", "verification-risk")


def current_commit(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def load_profiles(root: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    path = root / "harness" / "review-profiles.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {}, [f"invalid review profile registry: {error}"]

    if document.get("schema") != 1 or not isinstance(document.get("languages"), dict):
        return {}, ["review profile registry must use schema 1 and contain languages"]

    profiles: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    for language, profile in document["languages"].items():
        if not isinstance(language, str) or not language.strip():
            errors.append("review profile language IDs must be non-empty strings")
            continue
        if not isinstance(profile, dict):
            errors.append(f"review profile {language!r} must be an object")
            continue
        if set(profile) != set(LANES):
            errors.append(f"review profile {language!r} must define exactly {LANES}")
            continue
        skills = tuple(profile[lane] for lane in LANES)
        if any(not isinstance(skill, str) or not skill.strip() for skill in skills):
            errors.append(f"review profile {language!r} skill IDs must be non-empty strings")
            continue
        normalized = tuple(skill.strip() for skill in skills)
        if len(set(normalized)) != len(LANES):
            errors.append(f"review profile {language!r} skill IDs must be distinct")
            continue
        profiles[language.strip()] = dict(zip(LANES, normalized))
    return profiles, errors


def validate_reviews(root: Path, commit: str) -> list[str]:
    review_dir = root / ".harness-state" / "reviews" / commit
    profiles, errors = load_profiles(root)
    reviewers: set[str] = set()
    skills: set[str] = set()
    language: str | None = None

    for lane in LANES:
        path = review_dir / f"{lane}.json"
        if not path.is_file():
            errors.append(f"missing review: {path.relative_to(root)}")
            continue
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"invalid review {path.relative_to(root)}: {error}")
            continue

        if report.get("schema") != 3:
            errors.append(f"{lane}: schema must be 3")
        if report.get("commit") != commit:
            errors.append(f"{lane}: review is not for current commit {commit}")
        if report.get("lane") != lane:
            errors.append(f"{lane}: lane field does not match filename")

        expected_skill: str | None = None
        report_language = report.get("language")
        if not isinstance(report_language, str) or not report_language.strip():
            errors.append(f"{lane}: language must be a non-empty ID")
        else:
            report_language = report_language.strip()
            expected_skill = profiles.get(report_language, {}).get(lane)
            if language is None:
                language = report_language
                if report_language not in profiles:
                    errors.append(
                        f"{lane}: language {report_language!r} has no registered review profile"
                    )
            elif report_language != language:
                errors.append(f"{lane}: language profile does not match {language!r}")

        skill = report.get("skill")
        if not isinstance(skill, str) or not skill.strip():
            errors.append(f"{lane}: skill must be a non-empty ID")
        else:
            skill = skill.strip()
            if skill in skills:
                errors.append(f"{lane}: skill {skill!r} is not distinct")
            else:
                skills.add(skill)
            if expected_skill is not None and skill != expected_skill:
                errors.append(
                    f"{lane}: registered skill is {expected_skill!r}, got {skill!r}"
                )

        reviewer = report.get("reviewer")
        if not isinstance(reviewer, str) or not reviewer.strip():
            errors.append(f"{lane}: reviewer must be a non-empty agent ID")
        else:
            reviewer = reviewer.strip()
            if reviewer in reviewers:
                errors.append(f"{lane}: reviewer {reviewer!r} is not independent")
            else:
                reviewers.add(reviewer)

        if report.get("verdict") != "pass":
            errors.append(f"{lane}: verdict must be pass")
        findings = report.get("blocking_findings")
        if not isinstance(findings, list):
            errors.append(f"{lane}: blocking_findings must be a list")
        elif findings:
            errors.append(f"{lane}: unresolved blocking findings")
        if not isinstance(report.get("notes"), list):
            errors.append(f"{lane}: notes must be a list")
        if lane == "architecture":
            architect_skill = report.get("architect_skill")
            if not isinstance(architect_skill, str) or not architect_skill.strip():
                errors.append(
                    "architecture: architect_skill must name the consulted architect"
                )
            basis = report.get("architecture_basis")
            if (
                not isinstance(basis, list)
                or not basis
                or any(not isinstance(item, str) or not item.strip() for item in basis)
            ):
                errors.append(
                    "architecture: architecture_basis must contain accepted sources"
                )

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    commit = current_commit(root)
    errors = validate_reviews(root, commit)
    if errors:
        print(f"Local review gate failed for {commit}:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Local review gate passed for {commit}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
