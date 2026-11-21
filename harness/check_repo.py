#!/usr/bin/env python3
"""Dependency-free repository checks shared by local development and CI."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


TEXT_SUFFIXES = {".md", ".py", ".rs", ".sh", ".toml", ".yml", ".yaml", ".json"}
IGNORED_DIRS = {".git", ".harness-state", "node_modules", "target", ".venv", "venv"}
MARKDOWN_LINK = re.compile(r"!?\[[^]]*]\(([^)]+)\)")


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _files(root: Path):
    for directory, dirs, names in os.walk(root):
        dirs[:] = [name for name in dirs if name not in IGNORED_DIRS]
        base = Path(directory)
        for name in names:
            path = base / name
            if path.suffix in TEXT_SUFFIXES or name in {"Makefile", ".harness"}:
                yield path


def _check_registry(root: Path, errors: list[str]) -> None:
    registry = root / "harness" / "projects"
    if not registry.is_file():
        errors.append("harness/projects: missing project registry")
        return

    names: set[str] = set()
    for number, raw in enumerate(registry.read_text(encoding="utf-8").splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue
        fields = raw.split("\t")
        if len(fields) != 2 or not all(fields):
            errors.append(f"harness/projects:{number}: expected name<TAB>path")
            continue
        name, relative = fields
        if name in names:
            errors.append(f"harness/projects:{number}: duplicate project {name!r}")
        names.add(name)

        project = (root / relative).resolve()
        if not _inside(project, root.resolve()) or not project.is_dir():
            errors.append(f"harness/projects:{number}: invalid project path {relative!r}")
            continue
        adapter = project / ".harness"
        if not adapter.is_file() or not os.access(adapter, os.X_OK):
            errors.append(f"{relative}/.harness: missing or not executable")


def _check_markdown(path: Path, root: Path, text: str, errors: list[str]) -> None:
    for match in MARKDOWN_LINK.finditer(text):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        target = raw.split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "/")):
            continue
        target = unquote(target).split(" ", 1)[0]
        resolved = (path.parent / target).resolve()
        if not _inside(resolved, root.resolve()) or not resolved.exists():
            relative = path.relative_to(root)
            errors.append(f"{relative}: broken relative link {target!r}")


def check_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    _check_registry(root, errors)

    for path in _files(root):
        relative = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{relative}: expected UTF-8 text")
            continue

        if text and not text.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f"{relative}:{number}: trailing whitespace")

        if path.suffix == ".md":
            _check_markdown(path, root, text, errors)
        elif path.suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as error:
                errors.append(f"{relative}:{error.lineno}: invalid JSON: {error.msg}")

    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = check_repository(root)
    if errors:
        print("Repository checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
