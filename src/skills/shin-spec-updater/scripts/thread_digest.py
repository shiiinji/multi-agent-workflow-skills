#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


AUTO_TURNS_BEGIN = "<!-- BEGIN AUTO TURNS -->"
AUTO_TURNS_END = "<!-- END AUTO TURNS -->"

TURN_HEADER_RE = re.compile(
    r"^### (?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4}) (?P<role>User|Assistant)\s*$"
)

PATH_RE = re.compile(
    r"""
    (?:
        # absolute paths
        /[^\s`]+?\.(?:md|tsx?|jsx?|js|json|ya?ml|py|sh|css|scss|go|rs|java|kt|swift|rb)(?::\d+)?
        |
        # relative-ish paths
        (?:\.\.?/)?[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+\.(?:md|tsx?|jsx?|js|json|ya?ml|py|sh|css|scss|go|rs|java|kt|swift|rb)(?::\d+)?
    )
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Turn:
    ts: str
    role: str
    body: str


def _split_frontmatter(lines: list[str]) -> tuple[str | None, list[str]]:
    if not lines:
        return None, lines
    if lines[0].strip() != "---":
        return None, lines

    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter = "\n".join(lines[1:i]).rstrip() + "\n"
            rest = lines[i + 1 :]
            return frontmatter, rest
    return None, lines


def _extract_auto_turns(text: str) -> str:
    begin = text.find(AUTO_TURNS_BEGIN)
    end = text.find(AUTO_TURNS_END)
    if begin != -1 and end != -1 and begin < end:
        return text[begin:end]
    return text


def _parse_turns(lines: Iterable[str]) -> list[Turn]:
    turns: list[Turn] = []
    current_ts: str | None = None
    current_role: str | None = None
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_ts, current_role, current_body
        if current_ts is None or current_role is None:
            return
        body = "\n".join(current_body).strip("\n")
        turns.append(Turn(ts=current_ts, role=current_role, body=body))
        current_ts = None
        current_role = None
        current_body = []

    for line in lines:
        match = TURN_HEADER_RE.match(line)
        if match:
            flush()
            current_ts = match.group("ts")
            current_role = match.group("role")
            current_body = []
            continue
        if current_ts is not None:
            current_body.append(line.rstrip("\n"))

    flush()
    return turns


def _bullet_lines(text: str) -> list[str]:
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].rstrip())
        elif stripped.startswith("* "):
            bullets.append(stripped[2:].rstrip())
    return bullets


def _find_paths(turns: Iterable[Turn]) -> list[str]:
    found: set[str] = set()
    for turn in turns:
        for match in PATH_RE.finditer(turn.body):
            path = match.group(0).rstrip(").,;")
            found.add(path)
    return sorted(found)


def _to_json(frontmatter: str | None, turns: list[Turn]) -> dict:
    latest_user = next((t for t in reversed(turns) if t.role == "User"), None)
    latest_assistant = next((t for t in reversed(turns) if t.role == "Assistant"), None)

    def turn_or_none(turn: Turn | None) -> dict | None:
        if turn is None:
            return None
        return {
            "ts": turn.ts,
            "role": turn.role,
            "body": turn.body,
            "bullets": _bullet_lines(turn.body),
        }

    return {
        "frontmatter": frontmatter,
        "turns": [
            {
                "ts": t.ts,
                "role": t.role,
                "body": t.body,
                "bullets": _bullet_lines(t.body),
            }
            for t in turns
        ],
        "paths": _find_paths(turns),
        "latest": {
            "user": turn_or_none(latest_user),
            "assistant": turn_or_none(latest_assistant),
        },
    }


def _to_markdown(frontmatter: str | None, turns: list[Turn]) -> str:
    latest_assistant = next((t for t in reversed(turns) if t.role == "Assistant"), None)
    latest_user = next((t for t in reversed(turns) if t.role == "User"), None)

    out: list[str] = []
    out.append("# Thread digest")
    out.append("")

    if frontmatter:
        out.append("## Frontmatter")
        out.append("```yaml")
        out.append(frontmatter.rstrip("\n"))
        out.append("```")
        out.append("")

    if latest_assistant:
        out.append("## Latest assistant summary")
        out.append(f"- timestamp: {latest_assistant.ts}")
        bullets = _bullet_lines(latest_assistant.body)
        if bullets:
            for b in bullets:
                out.append(f"- {b}")
        else:
            snippet = latest_assistant.body.strip().splitlines()[:20]
            out.append("```")
            out.extend(snippet)
            out.append("```")
        out.append("")

    if latest_user:
        out.append("## Latest user request")
        out.append(f"- timestamp: {latest_user.ts}")
        bullets = _bullet_lines(latest_user.body)
        if bullets:
            for b in bullets:
                out.append(f"- {b}")
        else:
            snippet = latest_user.body.strip().splitlines()[:20]
            out.append("```")
            out.extend(snippet)
            out.append("```")
        out.append("")

    out.append("## Referenced paths")
    paths = _find_paths(turns)
    if paths:
        for p in paths:
            out.append(f"- {p}")
    else:
        out.append("- (none)")
    out.append("")

    return "\n".join(out)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Extract a digest from llm-threads markdown logs.")
    parser.add_argument("thread", type=Path, help="Path to a thread markdown file")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    args = parser.parse_args(argv)

    text = args.thread.read_text(encoding="utf-8")
    lines = text.splitlines()
    frontmatter, rest = _split_frontmatter(lines)

    auto_turns_text = _extract_auto_turns("\n".join(rest))
    turns = _parse_turns(auto_turns_text.splitlines())

    if args.json:
        payload = _to_json(frontmatter, turns)
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    sys.stdout.write(_to_markdown(frontmatter, turns))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
