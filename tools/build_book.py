#!/usr/bin/env python3
"""
Build a plain text book from manuscript chapters.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="拼接 manuscript 章节，输出 dist/book.txt（标准库）。"
    )
    return parser.parse_args()


def list_chapters(manuscript_dir: Path) -> List[Tuple[int, str, Path]]:
    entries: List[Tuple[int, str, Path]] = []
    pattern = re.compile(r"^ch(\d+)\.md$")
    for path in manuscript_dir.iterdir():
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if not match:
            continue
        num = int(match.group(1))
        chapter_id = f"ch{num:03d}"
        entries.append((num, chapter_id, path))
    return sorted(entries, key=lambda x: x[0])


def extract_title(lines: List[str]) -> str:
    if len(lines) >= 2:
        match = re.match(r"^##\s*《(.+?)》\s*$", lines[1].strip())
        if match:
            return match.group(1)
    return "未命名"


def strip_markdown_headings(lines: List[str]) -> List[str]:
    result = list(lines)
    if result and re.match(r"^#\s*ch\d+\s*$", result[0].strip()):
        result = result[1:]
    if result and re.match(r"^##\s*《.+?》\s*$", result[0].strip()):
        result = result[1:]
    return result


def build_book_text(entries: List[Tuple[int, str, Path]]) -> str:
    sections: List[str] = []
    for num, chapter_id, path in entries:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = extract_title(lines)
        body_lines = strip_markdown_headings(lines)
        body = "\n".join(body_lines).strip("\n")
        heading = f"第{num:03d}章 《{title}》"
        if body:
            sections.append(heading + "\n" + body)
        else:
            sections.append(heading)
    return "\n\n".join(sections) + "\n"


def main() -> int:
    _ = parse_args()
    root = Path(".")
    manuscript_dir = root / "manuscript"
    if not manuscript_dir.exists():
        print("ERROR: manuscript/ 不存在。")
        return 1

    entries = list_chapters(manuscript_dir)
    if not entries:
        print("ERROR: manuscript/ 下未找到章节文件。")
        return 1

    book_text = build_book_text(entries)
    out_dir = root / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "book.txt"
    out_path.write_text(book_text, encoding="utf-8", newline="\n")
    print(f"OK: wrote {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
