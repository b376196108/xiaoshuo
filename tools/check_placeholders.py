#!/usr/bin/env python3
"""
Check placeholder tokens in key files.
Standard library only.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="检查占位内容与编码问题（标准库）。"
    )
    parser.add_argument("--date", required=True, help="运行日期 YYYY-MM-DD。")
    parser.add_argument("--chapter", required=True, help="章节号，例如 ch004。")
    return parser.parse_args()


def _build_targets(date: str, chapter: str) -> List[str]:
    return [
        f"runs/{date}/chapter_plan.md",
        f"manuscript/{chapter}.md",
        f"recap/chapter_summaries/{chapter}.md",
        "recap/rolling_recap.md",
        "state/state_patch.json",
        f"runs/{date}/changelog.md",
    ]


def _patterns() -> List[Tuple[str, str]]:
    return [
        ("three_question_marks", "?" * 3),
        ("four_question_marks", "?" * 4),
        ("t_b_d", "T" + "BD"),
        ("t_o_d_o", "TO" + "DO"),
        ("pending_complete", "\u5f85\u8865\u5168"),
        ("replacement_char", "\ufffd"),
    ]


def main() -> int:
    args = parse_args()
    root = Path(".")
    targets = _build_targets(args.date, args.chapter)
    patterns = _patterns()

    hits: Dict[str, List[str]] = {}
    for rel in targets:
        path = root / rel
        if not path.exists():
            print(f"[MISSING] {rel}")
            continue
        try:
            data = path.read_bytes()
            text = data.decode("utf-8")
        except Exception:
            print(f"FAIL: 疑似编码错误：{rel}")
            return 1
        for label, token in patterns:
            if token and token in text:
                hits.setdefault(rel, []).append(label)

    if hits:
        print("FAIL: 发现占位内容或替换字符。")
        for rel, labels in hits.items():
            print(f"- {rel}: {', '.join(sorted(set(labels)))}")
        return 1

    print("OK: 未发现占位内容或替换字符。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
