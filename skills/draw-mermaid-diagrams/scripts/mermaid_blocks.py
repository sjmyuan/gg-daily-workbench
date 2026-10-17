#!/usr/bin/env python3
"""Inventory, extract, and replace fenced mermaid blocks in Markdown.

Usage:
    python3 mermaid_blocks.py list <file-or-dir> [--json]
    python3 mermaid_blocks.py extract <file> (--index N | --line N | --title T) [--out <file>]
    python3 mermaid_blocks.py replace <file> (--index N | --line N | --title T) --from <file> [--check]
    python3 mermaid_blocks.py insert <file> (--after-index N | --after-line N | --after-title T) (--from <file> | --text "<block>")

Indexes are 1-based per file and match `list` output. Prefer --title or --hash:
indexes drift when a block is inserted or removed. `list` prints each block's short
content hash, which stays valid until that block changes. `replace` prints the resolved
block and accepts --expect-title to fail loudly on drift. `insert` with
--after-index 0 inserts before the first block.

Exit: 0 = ok, 1 = validation/usage failure, 2 = bad arguments.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
import re


def split_fences(md: str) -> list[dict]:
    """Return every ```mermaid block with its fence span and content."""
    lines = md.splitlines()
    out: list[dict] = []
    open_at = None
    start = 0
    buf: list[str] = []
    for i, line in enumerate(lines):
        if open_at is None and line.strip() == "```mermaid":
            open_at, start, buf = i, i + 2, []
            continue
        if open_at is not None and line.strip() == "```":
            out.append({"fence_start": open_at + 1, "fence_end": i + 1,
                        "text_start": start, "text": "\n".join(buf)})
            open_at = None
            continue
        if open_at is not None:
            buf.append(line)
    if open_at is not None:
        out.append({"fence_start": open_at + 1, "fence_end": None,
                    "text_start": start, "text": "\n".join(buf)})
    return out


def strip_fence(text: str) -> str:
    """Return the body of a pasted ```mermaid block, or the text unchanged."""
    lines = text.splitlines()
    if len(lines) >= 2 and re.match(r"^\s*(?:```|~~~)\s*mermaid\s*$", lines[0]):
        body = lines[1:]
        if body and re.match(r"^\s*(?:```|~~~)\s*$", body[-1]):
            body = body[:-1]
        return "\n".join(body)
    return text


def fingerprint(text: str) -> str:
    """Stable short id for a block's current content."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def classify(text: str) -> tuple[str, str]:
    kind, title = "unknown", ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%%"):
            continue
        if not kind or kind == "unknown":
            kind = stripped.split()[0].rstrip(":")
        if stripped.lower().startswith("title ") and not title:
            title = stripped[6:].strip()
        if kind != "unknown" and title:
            break
    if not title:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("%%"):
                note = stripped.lstrip("%").strip()
                if note and not note.lower().startswith("level"):
                    title = note
                    break
    return kind, title


FLOW_KEYWORDS = {
    "flowchart", "graph", "td", "tb", "bt", "lr", "rl", "subgraph", "end",
    "style", "classdef", "class", "click", "linkstyle", "direction",
    "acctitle", "accdescr",
}


def flow_nodes(lines: list[str]) -> set[str]:
    """Node ids from shapes and bare edges, ignoring labels and directives."""
    nodes: set[str] = set()
    for line in lines:
        if re.match(r"^\s*(subgraph|style|classDef|class|click|linkStyle|direction|accTitle|accDescr)\b", line):
            continue
        text = re.sub(r"\|[^|]*\|", " ", line)
        text = re.sub(r"\[[^\]]*\]|\{[^}]*\}|\([^)]*\)|<[^>]*>", " ", text)
        for token in re.split(r"[\s;]+", text):
            match = re.match(r"([A-Za-z_][\w-]*)", token.strip())
            if match and match.group(1).lower() not in FLOW_KEYWORDS:
                nodes.add(match.group(1))
    return nodes


def count_units(kind: str, text: str) -> int:
    """Count the reader-facing elements: lifelines, C4 elements, nodes, states."""
    lines = text.splitlines()
    if kind == "sequenceDiagram":
        return sum(1 for ln in lines if ln.strip().startswith(("actor ", "participant ")))
    if kind.startswith("C4"):
        return sum(1 for ln in lines
                   if re.match(r"^\s*(Person|System|Container|Component)\w*\s*\(", ln))
    if kind in {"flowchart", "graph"}:
        return len(flow_nodes(lines))
    if kind == "classDiagram":
        return sum(1 for ln in lines if re.match(r"^\s*class\s+[A-Za-z_]\w*", ln))
    if kind == "erDiagram":
        return sum(1 for ln in lines if re.match(r"^\s*[A-Za-z_]\w*\s*\{\s*$", ln))
    if kind == "stateDiagram-v2":
        states = set()
        for ln in lines:
            match = re.match(r"^\s*(\[\*\]|\w+)\s*-->\s*(\[\*\]|\w+)", ln)
            if match:
                states.update(match.groups())
        return len(states)
    return 0


def collect(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(p for p in target.rglob("*.md") if p.is_file())
    return [target]


def summarize(path: Path) -> list[dict]:
    md = path.read_text(encoding="utf-8")
    rows = []
    for i, block in enumerate(split_fences(md), start=1):
        kind, title = classify(block["text"])
        rows.append({
            "index": i,
            "file": str(path),
            "line": block["fence_start"],
            "type": kind,
            "title": title,
            "units": count_units(kind, block["text"]),
            "hash": fingerprint(block["text"]),
            "closed": block["fence_end"] is not None,
        })
    return rows


def read_source(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    blocks = split_fences(text)
    if len(blocks) == 1 and text.strip().startswith("```mermaid"):
        return blocks[0]["text"]
    if text.strip().startswith("```"):
        lines = text.splitlines()
        return "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    return text.rstrip("\n")


def normalize(text: str) -> str:
    return " ".join(text.split()).casefold()


def resolve(blocks: list[dict], index=None, line=None, title=None, digest=None) -> tuple[int, dict]:
    """Resolve exactly one selector to a (1-based index, block) pair."""
    chosen = [n for n, v in (("--index", index), ("--line", line),
                             ("--title", title), ("--hash", digest)) if v is not None]
    if len(chosen) != 1:
        raise ValueError("choose exactly one selector: --index, --line, --title, or --hash")
    if digest is not None:
        hits = [i for i, b in enumerate(blocks, 1)
                if fingerprint(b["text"]).startswith(digest.lower())]
        if not hits:
            raise ValueError(f"no block matches --hash {digest} — run `list` to see fingerprints")
        if len(hits) > 1:
            raise ValueError(f"--hash {digest} matches {len(hits)} blocks — use more characters")
        return hits[0], blocks[hits[0] - 1]
    if index is not None:
        if not 1 <= index <= len(blocks):
            raise ValueError(f"index {index} out of range 1..{len(blocks)}")
        return index, blocks[index - 1]
    if line is not None:
        hits = [i for i, b in enumerate(blocks, 1) if b["fence_start"] == line]
    else:
        exact = [i for i, b in enumerate(blocks, 1)
                 if normalize(classify(b["text"])[1]) == normalize(title)]
        hits = exact or [i for i, b in enumerate(blocks, 1)
                         if normalize(title) in normalize(classify(b["text"])[1])]
    if not hits:
        wanted = f"{chosen[0]} {title!r}" if title is not None else f"{chosen[0]} {line if line is not None else ''}".strip()
        raise ValueError(f"no block matches {wanted} — run `list` to see available blocks")
    if len(hits) > 1:
        listing = ", ".join(f"{i} ({classify(blocks[i - 1]['text'])[1] or 'untitled'})" for i in hits)
        raise ValueError(f"{chosen[0]} matches {len(hits)} blocks: {listing}")
    return hits[0], blocks[hits[0] - 1]


def identity(index: int, block: dict) -> str:
    kind, title = classify(block["text"])
    return f"block {index} ({kind}, {title or 'untitled'}) at line {block['fence_start']}"


def write_replace(path: Path, block: dict, new_text: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    payload = [ln + "\n" for ln in new_text.rstrip("\n").splitlines()]
    lines[block["text_start"] - 1:block["fence_end"] - 1] = payload
    path.write_text("".join(lines), encoding="utf-8")


def write_insert(path: Path, position: int, new_text: str) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    payload = ["```mermaid\n", new_text.rstrip("\n") + "\n", "```\n"]
    lines[position:position] = payload
    path.write_text("".join(lines), encoding="utf-8")
    return position + 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Inspect and edit mermaid blocks.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="list blocks with index, line, type, title")
    p_list.add_argument("paths", nargs="+")
    p_list.add_argument("--json", action="store_true")

    p_extract = sub.add_parser("extract", help="write one block to stdout or a file")
    p_extract.add_argument("path")
    p_extract.add_argument("--index", type=int)
    p_extract.add_argument("--line", type=int)
    p_extract.add_argument("--title")
    p_extract.add_argument("--hash")
    p_extract.add_argument("--out")

    p_replace = sub.add_parser("replace", help="replace one block in place")
    p_replace.add_argument("path")
    p_replace.add_argument("--index", type=int)
    p_replace.add_argument("--line", type=int)
    p_replace.add_argument("--title")
    p_replace.add_argument("--hash")
    p_replace.add_argument("--expect-title", help="fail when the resolved block title differs")
    p_replace.add_argument("--from", dest="source", required=True)
    p_replace.add_argument("--check", action="store_true", help="preview only")

    p_insert = sub.add_parser("insert", help="insert a block after a selector (index 0 = first)")
    p_insert.add_argument("path")
    p_insert.add_argument("--after-index", type=int)
    p_insert.add_argument("--after-line", type=int)
    p_insert.add_argument("--after-title")
    p_insert.add_argument("--from", dest="source")
    p_insert.add_argument("--text", help="inline block instead of --from")

    args = parser.parse_args(argv)

    if args.cmd == "list":
        rows = [row for target in args.paths for path in collect(Path(target)) for row in summarize(path)]
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            for row in rows:
                flag = "" if row["closed"] else "  [unterminated]"
                title = row["title"] or "-"
                print(f"{row['index']:>2}  {row['file']}:{row['line']}  "
                      f"{row['type']}  ({row['units']} unit(s))  {title}  #{row['hash']}{flag}")
        return 0

    path = Path(args.path)
    blocks = split_fences(path.read_text(encoding="utf-8"))

    if args.cmd == "extract":
        try:
            _, block = resolve(blocks, args.index, args.line, args.title, args.hash)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        text = block["text"] + "\n"
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
        return 0

    if args.cmd == "insert" and args.text is not None:
        if args.source:
            print("choose --from or --text, not both", file=sys.stderr)
            return 2
        source = strip_fence(args.text)
    elif args.cmd == "insert" and args.source == "-":
        source = strip_fence(sys.stdin.read())
    elif args.source:
        source = read_source(Path(args.source))
    else:
        print("insert needs --from <file> or --text \"<block>\"", file=sys.stderr)
        return 2

    if args.cmd == "replace":
        try:
            index, block = resolve(blocks, args.index, args.line, args.title, args.hash)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        if args.expect_title:
            actual = classify(block["text"])[1]
            if normalize(actual) != normalize(args.expect_title):
                print(f"refusing: {identity(index, block)} does not match "
                      f"--expect-title {args.expect_title!r} — run `list` first", file=sys.stderr)
                return 1
        if block["fence_end"] is None:
            print("cannot replace an unterminated block", file=sys.stderr)
            return 1
        print(f"{path}: {identity(index, block)}")
        if args.check:
            old = block["text"].splitlines()
            new = source.rstrip("\n").splitlines()
            diff = [f"- {ln}" for ln in old if ln not in new]
            diff += [f"+ {ln}" for ln in new if ln not in old]
            print("\n".join(diff[:60]) or "identical")
            return 0
        write_replace(path, block, source)
        print(f"replaced {identity(index, block)}")
        return 0

    try:
        if args.after_index is not None:
            if args.after_index == 0:
                position = blocks[0]["fence_start"] - 1 if blocks else 0
            else:
                _, anchor = resolve(blocks, index=args.after_index)
                position = anchor["fence_end"]
        else:
            _, anchor = resolve(blocks, None, args.after_line, args.after_title)
            position = anchor["fence_end"]
        if position is None:
            raise ValueError("cannot insert after an unterminated block")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    line = write_insert(path, position, source)
    print(f"inserted block at {path}:{line}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
