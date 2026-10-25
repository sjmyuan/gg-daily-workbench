#!/usr/bin/env python3
"""Check that every markdown link in a skill stays inside its own skill folder.

Usage:
    python3 check_skill_links.py [options] PATH [PATH ...]

PATH is a skill directory (holds SKILL.md), a skills root whose subdirectories
are skills, or a .md file (its nearest SKILL.md ancestor is the skill). Every
*.md under a skill is scanned. Link parsing skips fenced blocks and inline code;
the CROSSPATH scan reads every line, including commands inside fences.

Options:
    --list          Print each offending link as `path:line: -> target [CODE]`.
    --duplicates    Report basenames appearing in more than one skill, marking
                    copies that differ. Informational: exits 0.
    -h, --help      Show this help.

Default output: one finding per line, `path:line: CODE message`, sorted, with the
path relative to the skill's parent folder (e.g. `conduct-spike/SKILL.md:109`).
    ESCAPE   link target resolves outside the skill folder (any `../` escape)
    ABS      link target is absolute or a file:// URL — not portable
    CROSSPATH  a path or command points into a sibling skill's folder; name the
               skill instead so this one still works when installed alone

Codes are stable field names. Missing relative targets are not reported here —
check_artifacts.py owns that. Exit codes: 0 clean, 1 findings, 2 usage error.
Pure standard library; read-only; no timestamps or author-machine paths.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

LINK = re.compile(r"\]\(([^)\s]+)\)")
CODE_SPAN = re.compile(r"`[^`]*`")
SKIP = ("http://", "https://", "mailto:", "#")
ABS = re.compile(r"^(?:/|file:|[A-Za-z]:[\\/])")


def skill_roots(paths: list[Path]) -> list[Path]:
    """Skill root for each path: itself, its skill children, or its nearest ancestor."""
    roots: list[Path] = []
    for path in paths:
        if (path / "SKILL.md").is_file():
            roots.append(path)
        elif path.is_dir():
            roots.extend(sorted(d for d in path.iterdir() if (d / "SKILL.md").is_file()))
        else:
            root = next((p for p in path.parents if (p / "SKILL.md").is_file()), None)
            if root is None:
                raise FileNotFoundError(f"{path} is not inside a skill")
            roots.append(root)
    return roots


def links(text: str) -> list[tuple[int, str]]:
    """(line number, target) per markdown link outside fences and code spans."""
    found: list[tuple[int, str]] = []
    marker = None
    for number, line in enumerate(text.splitlines(), 1):
        fence = re.match(r"`{3,}", line.lstrip())
        if fence:
            run = fence.group(0)
            marker = run if marker is None else (None if run.startswith(marker) else marker)
            continue
        if marker is None:
            targets = LINK.findall(CODE_SPAN.sub("", line))
            found.extend((number, t) for t in targets if not t.startswith(SKIP))
    return found


def escaping(path: Path, root: Path) -> list[tuple[int, str, str]]:
    """(line, code, target) for links that leave the skill folder or are absolute."""
    findings: list[tuple[int, str, str]] = []
    for number, target in links(path.read_text(encoding="utf-8", errors="replace")):
        if ABS.match(target):
            findings.append((number, "ABS", target))
            continue
        try:
            (path.parent / target.split("#")[0]).resolve().relative_to(root.resolve())
        except ValueError:
            findings.append((number, "ESCAPE", target))
    return findings


def sibling_names(root: Path) -> set[str]:
    """Skill names installed beside this skill; empty when it stands alone."""
    parent = root.parent
    if not parent.is_dir():
        return set()
    return {d.name for d in parent.iterdir()
            if d.is_dir() and d != root and (d / "SKILL.md").is_file()}


def cross_paths(path: Path, names: set[str]) -> list[tuple[int, str]]:
    """(line, skill name) for a reference into a sibling skill's folder."""
    if not names:
        return []
    pattern = re.compile(
        r"(?:\.\./)?(" + "|".join(sorted(map(re.escape, names)))
        + r")/(?:reference|examples|scripts)/")
    found: list[tuple[int, str]] = []
    for number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        match = pattern.search(line)
        if match and f"]({match.group(0)}" not in line:
            found.append((number, match.group(1)))
    return found


def duplicates(roots: list[Path]) -> list[tuple[Path, str, str]]:
    """(origin, basename, detail) for basenames appearing under more than one skill."""
    seen: dict[str, list[tuple[Path, Path]]] = {}
    for root in roots:
        for md in sorted(root.rglob("*.md")):
            seen.setdefault(md.name, []).append((root, md))
    rows: list[tuple[Path, str, str]] = []
    for name, entries in sorted(seen.items()):
        if len({root for root, _ in entries}) < 2:
            continue
        same = len({hashlib.sha256(md.read_bytes()).hexdigest() for _, md in entries}) == 1
        skills = ",".join(sorted(root.name for root, _ in entries))
        rows.append((entries[0][1], name, f"skills={skills} status={'same' if same else 'differ'}"))
    return rows


def main(argv: list[str]) -> int:
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0 if argv else 2
    mode, paths = "check", []
    for arg in argv:
        if arg in {"--list", "--duplicates"}:
            mode = arg[2:]
        elif arg.startswith("-"):
            print(f"error: unknown option {arg}", file=sys.stderr)
            return 2
        else:
            paths.append(arg)
    if not paths:
        print("error: no path given", file=sys.stderr)
        return 2
    try:
        roots = skill_roots([Path(p) for p in paths])
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if mode == "duplicates":
        for origin, name, detail in duplicates(roots):
            print(f"{origin}: DUP {name} {detail}")
        return 0

    rows = [(str(md.relative_to(root.parent)), n, code, target)
            for root in roots for md in sorted(root.rglob("*.md"))
            for n, code, target in escaping(md, root)]
    rows += [(str(md.relative_to(root.parent)), n, "CROSSPATH", name)
             for root in roots for md in sorted(root.rglob("*.md"))
             for n, name in cross_paths(md, sibling_names(root))]
    for path, number, code, target in sorted(rows):
        if mode == "list":
            print(f"{path}:{number}: -> {target} [{code}]")
        elif code == "ABS":
            print(f"{path}:{number}: ABS absolute link target {target}")
        elif code == "CROSSPATH":
            print(f"{path}:{number}: CROSSPATH points into sibling skill '{target}'")
        else:
            print(f"{path}:{number}: ESCAPE link escapes skill folder: {target}")
    return 0 if mode == "list" or not rows else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
