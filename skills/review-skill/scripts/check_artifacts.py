#!/usr/bin/env python3
"""Check skill artifact consistency: links, fences, step fields, zone order.

Usage:
    check_artifacts.py [options] PATH [PATH ...]

PATH may be a markdown file or a directory (scanned recursively for *.md).

Options:
    --step-fields A,B,C     Required labels, in order, for every `### Step` block.
    --zones A,B,C           Required labels, in order, for every `## Scope Boundary` block.
    --optional-zones A,B    Zones that may be omitted but must keep their relative order.
    -h, --help              Show this help.

Output: one finding per line, `path:line: CODE message`, sorted by path then line.
Exit codes: 0 clean, 1 findings, 2 usage error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK = re.compile(r"\]\(([^)\s]+\.md)(?:#[^)]*)?\)")
STEP = re.compile(r"^### Step (\d+[a-z]?):\s*(.*)$")
ZONE = re.compile(r"^\*\*([^*]+)\*\*:")
FIELD = re.compile(r"^\*\*([^*]+)\*\*:")


def scan(path: Path, step_fields: list[str], zones: list[str], optional: set[str]) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    fenced, balanced = _fence_map(lines)
    if not balanced:
        findings.append((1, "FENCE", "unbalanced code fences"))

    for i, (line, inside) in enumerate(zip(lines, fenced), 1):
        if inside:
            continue
        for target in LINK.findall(line):
            if target.startswith(("http://", "https://", "mailto:")) or target == "SKILL.md":
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                findings.append((i, "LINK", f"missing relative target {target}"))

    prose = _without_fences(lines, fenced)

    if step_fields:
        findings.extend(_check_steps(prose, step_fields))
    findings.extend(_check_duplicate_steps(prose))
    if zones:
        findings.extend(_check_zones(prose, zones, optional))
    return findings


def _fence_map(lines: list[str]) -> tuple[list[bool], bool]:
    fenced: list[bool] = []
    marker = None  # type: ignore[var-annotated]
    for line in lines:
        match = re.match(r"`{3,}", line.lstrip())
        if match:
            run = match.group(0)
            if marker is None:
                marker = run
            elif len(run) >= len(marker) and run.startswith(marker):
                marker = None
            fenced.append(True)
            continue
        fenced.append(marker is not None)
    return fenced, marker is None


def _without_fences(lines: list[str], fenced: list[bool]) -> list[str]:
    return ["" if inside else line for line, inside in zip(lines, fenced)]


def _block(lines: list[str], start: int, heading: str) -> list[str]:
    block: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## ") or line.startswith("### "):
            break
        if line.strip():
            block.append(line)
    return block


def _check_steps(lines: list[str], required: list[str]) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines):
        match = STEP.match(line)
        if not match:
            continue
        title = match.group(2)
        if "⏭" in title or "🚫" in title:
            continue
        labels = [FIELD.match(item).group(1).strip() for item in _block(lines, i, line) if FIELD.match(item)]
        labels = labels[: len(required)]
        if labels != required:
            findings.append((i + 1, "STEP", f"fields {labels} != {required}"))
    return findings


def _check_duplicate_steps(lines: list[str]) -> list[tuple[int, str, str]]:
    seen: dict[str, int] = {}
    findings: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        match = STEP.match(line)
        if not match:
            continue
        number = match.group(1)
        if number in seen:
            findings.append((i, "DUPSTEP", f"Step {number} already defined at line {seen[number]}"))
        else:
            seen[number] = i
    return findings


def _check_zones(lines: list[str], required: list[str], optional: set[str]) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    index = next((i for i, line in enumerate(lines) if line.strip() == "## Scope Boundary"), None)
    if index is None:
        return findings
    labels = [ZONE.match(line).group(1).strip() for line in _block(lines, index, "## Scope Boundary") if ZONE.match(line)]
    if not labels:
        return findings
    present = [label for label in labels if label in required]
    expected = [label for label in required if label not in optional or label in present]
    if present != expected:
        findings.append((index + 1, "ZONE", f"zones {present} != {expected}"))
    return findings


def _expand(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(raw)
    return files


def main(argv: list[str]) -> int:
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0 if argv else 2

    step_fields: list[str] = []
    zones: list[str] = []
    optional: set[str] = set()
    paths: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in {"--step-fields", "--zones", "--optional-zones"}:
            if i + 1 >= len(argv):
                print(f"error: {arg} needs a value", file=sys.stderr)
                return 2
            value = [item.strip() for item in argv[i + 1].split(",") if item.strip()]
            if arg == "--step-fields":
                step_fields = value
            elif arg == "--zones":
                zones = value
            else:
                optional = set(value)
            i += 2
            continue
        if arg.startswith("-"):
            print(f"error: unknown option {arg}", file=sys.stderr)
            return 2
        paths.append(arg)
        i += 1

    if not paths:
        print("error: no path given", file=sys.stderr)
        return 2

    try:
        files = _expand(paths)
    except FileNotFoundError as exc:
        print(f"error: no such path {exc}", file=sys.stderr)
        return 2

    results: list[tuple[str, int, str, str]] = []
    for path in files:
        for line, code, message in scan(path, step_fields, zones, optional):
            results.append((str(path), line, code, message))

    for path, line, code, message in sorted(results):
        print(f"{path}:{line}: {code} {message}")
    return 1 if results else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
