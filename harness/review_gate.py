#!/usr/bin/env python3
"""Validate local three-lane review evidence for the current commit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REVIEW_SKILLS = {
    "correctness": "tamaos-review-correctness",
    "architecture": "tamaos-review-architecture",
    "verification-risk": "tamaos-review-verification",
}
LANES = tuple(REVIEW_SKILLS)


def current_commit(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def validate_reviews(root: Path, commit: str) -> list[str]:
    review_dir = root / ".harness-state" / "reviews" / commit
    errors: list[str] = []
    reviewers: set[str] = set()

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

        if report.get("schema") != 2:
            errors.append(f"{lane}: schema must be 2")
        if report.get("commit") != commit:
            errors.append(f"{lane}: review is not for current commit {commit}")
        if report.get("lane") != lane:
            errors.append(f"{lane}: lane field does not match filename")
        if report.get("skill") != REVIEW_SKILLS[lane]:
            errors.append(f"{lane}: required skill is {REVIEW_SKILLS[lane]}")

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
