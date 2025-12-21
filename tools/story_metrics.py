#!/usr/bin/env python3
"""
Generate metrics report for manuscript chapters.
Standard library only.
"""

from __future__ import annotations

import argparse
import difflib
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


WARNING_WORDS = ["冷", "风", "灰", "薄被", "饥", "饿"]
OPENING_SIMILARITY_WARNING = 0.65
DIALOGUE_RATIO_MIN = 0.20
DIALOGUE_RATIO_MAX = 0.55
DEFAULT_WINDOW = 5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="扫描 manuscript 章节并生成 metrics_report.md（标准库）。"
    )
    parser.add_argument(
        "--chapter",
        help="只分析单章（例如 ch004）。",
        default=None,
    )
    parser.add_argument(
        "--date",
        help="报告写入 runs/YYYY-MM-DD/metrics_report.md（例如 2025-12-23）。",
        default=None,
    )
    parser.add_argument(
        "--window",
        type=int,
        default=DEFAULT_WINDOW,
        help="比较开头相似度时向前查看的章节窗口（默认 5）。",
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


def remove_whitespace(text: str) -> str:
    return re.sub(r"\s+", "", text)


def extract_body_text(text: str) -> str:
    lines = text.splitlines()
    body_lines = [ln for ln in lines if not ln.lstrip().startswith("#")]
    return "\n".join(body_lines)


def compute_dialogue_ratio(body_text: str) -> Tuple[float, int, int]:
    in_dialogue = False
    dialogue_chars = 0
    total_chars = 0
    for ch in body_text:
        if ch == "“":
            in_dialogue = True
            continue
        if ch == "”":
            in_dialogue = False
            continue
        if ch.isspace():
            continue
        total_chars += 1
        if in_dialogue:
            dialogue_chars += 1
    ratio = (dialogue_chars / total_chars) if total_chars else 0.0
    return ratio, dialogue_chars, total_chars


def compute_repeated_words(opening_text: str) -> Tuple[int, Dict[str, int]]:
    counts: Dict[str, int] = {}
    for word in WARNING_WORDS:
        counts[word] = opening_text.count(word)
    total = sum(counts.values())
    return total, counts


def similarity_ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def choose_previous(
    current_num: int,
    openings: Dict[int, str],
    window: int,
) -> Optional[Tuple[int, float]]:
    best_num: Optional[int] = None
    best_ratio = 0.0
    for i in range(1, window + 1):
        prev_num = current_num - i
        if prev_num not in openings:
            continue
        ratio = similarity_ratio(openings[current_num], openings[prev_num])
        if ratio > best_ratio or best_num is None:
            best_ratio = ratio
            best_num = prev_num
    if best_num is None:
        return None
    return best_num, best_ratio


def main() -> int:
    args = parse_args()
    root = Path(".")
    manuscript_dir = root / "manuscript"
    if not manuscript_dir.exists():
        print("ERROR: manuscript/ 不存在。")
        return 1

    entries = list_chapters(manuscript_dir)
    if not entries:
        print("ERROR: manuscript/ 下未找到章节文件。")
        return 1

    entry_by_id = {chapter_id: (num, chapter_id, path) for num, chapter_id, path in entries}

    chapter_filter = None
    if args.chapter:
        chapter_filter = args.chapter.strip()
        if chapter_filter not in entry_by_id:
            print(f"ERROR: 未找到章节 {chapter_filter}。")
            return 1

    openings: Dict[int, str] = {}
    body_cache: Dict[int, Dict[str, str]] = {}
    for num, chapter_id, path in entries:
        text = path.read_text(encoding="utf-8")
        body_text = extract_body_text(text)
        body_no_ws = remove_whitespace(body_text)
        openings[num] = body_no_ws[:200]
        body_cache[num] = {
            "body_text": body_text,
            "body_no_ws": body_no_ws,
            "chapter_id": chapter_id,
        }

    report_entries = entries
    if chapter_filter:
        report_entries = [entry_by_id[chapter_filter]]

    lines: List[str] = []
    lines.append("# Metrics Report")
    lines.append("")
    lines.append(f"- generated_at: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}")
    lines.append(f"- window: {args.window}")
    if chapter_filter:
        lines.append(f"- chapter_filter: {chapter_filter}")
    lines.append("")

    for num, chapter_id, path in report_entries:
        body_text = body_cache[num]["body_text"]
        body_no_ws = body_cache[num]["body_no_ws"]
        body_chars = len(body_no_ws)
        opening_200 = openings[num]

        dialogue_ratio, dialogue_chars, total_chars = compute_dialogue_ratio(body_text)
        repeated_total, repeated_counts = compute_repeated_words(opening_200)

        prev_info = choose_previous(num, openings, args.window)
        if prev_info is None:
            similarity_text = "n/a"
            similarity_value = 0.0
            similarity_ref = "n/a"
        else:
            prev_num, similarity_value = prev_info
            similarity_ref = f"ch{prev_num:03d}"
            similarity_text = f\"{similarity_value:.3f} (vs {similarity_ref})\"

        repeated_opening_warning = (
            "WARNING" if similarity_value >= OPENING_SIMILARITY_WARNING else "OK"
        )
        dialogue_ratio_warning = (
            "WARNING"
            if dialogue_ratio < DIALOGUE_RATIO_MIN or dialogue_ratio > DIALOGUE_RATIO_MAX
            else "OK"
        )
        repeated_words_warning = "WARNING" if repeated_total >= 6 else "OK"

        lines.append(f"## {chapter_id}")
        lines.append(f"- file: {path.as_posix()}")
        lines.append(f"- body_chars: {body_chars}")
        lines.append(f"- dialogue_char_ratio: {dialogue_ratio:.3f}")
        lines.append(f"- dialogue_chars: {dialogue_chars}")
        lines.append(f"- opening_200: {opening_200}")
        lines.append(f"- opening_similarity_to_prev: {similarity_text}")
        lines.append(f"- repeated_opening_warning: {repeated_opening_warning}")
        lines.append(f"- dialogue_ratio_warning: {dialogue_ratio_warning}")
        lines.append(f"- repeated_words_total: {repeated_total}")
        lines.append(f"- repeated_words_detail: {repeated_counts}")
        lines.append(f"- repeated_words_warning: {repeated_words_warning}")
        lines.append("")

    if args.date:
        out_path = root / "runs" / args.date / "metrics_report.md"
    else:
        out_path = root / "runs" / "_metrics" / "metrics_report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")

    print(f"OK: wrote {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
