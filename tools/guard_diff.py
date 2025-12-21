#!/usr/bin/env python3
"""
Guard git diff for manual Codex steps.
Standard library only.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Set, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="限制手动步骤允许变更的文件白名单（标准库）。"
    )
    parser.add_argument("--step", type=int, required=True, help="步骤编号（1/2/3）。")
    parser.add_argument("--date", required=True, help="运行日期 YYYY-MM-DD。")
    parser.add_argument("--chapter", required=True, help="章节号，例如 ch004。")
    return parser.parse_args()


def _allowed_paths(step: int, date: str, chapter: str) -> Set[str]:
    if step == 1:
        return {f"runs/{date}/chapter_plan.md"}
    if step == 2:
        return {f"manuscript/{chapter}.md"}
    if step == 3:
        return {
            f"recap/chapter_summaries/{chapter}.md",
            "recap/rolling_recap.md",
            "state/state_patch.json",
            f"runs/{date}/changelog.md",
        }
    raise ValueError("step must be 1, 2, or 3")


def _parse_git_status(output: str) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    for raw in output.splitlines():
        if not raw:
            continue
        status = raw[:2]
        path_part = raw[3:].strip() if len(raw) > 3 else ""
        if "->" in path_part:
            path_part = path_part.split("->", 1)[1].strip()
        path_part = path_part.strip('"')
        results.append((status, Path(path_part).as_posix()))
    return results


def _collect_violations(
    changes: Iterable[Tuple[str, str]], allowed: Set[str]
) -> Tuple[List[str], bool]:
    violations: List[str] = []
    has_untracked = False
    for status, path in changes:
        if path not in allowed:
            violations.append(path)
            if status == "??":
                has_untracked = True
    return sorted(set(violations)), has_untracked


def main() -> int:
    args = parse_args()
    root = Path(".")
    allowed = _allowed_paths(args.step, args.date, args.chapter)

    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("ERROR: 无法读取 git 状态。")
        if proc.stderr:
            print(proc.stderr.strip())
        return 1

    changes = _parse_git_status(proc.stdout)
    violations, has_untracked = _collect_violations(changes, allowed)

    if not violations:
        print("OK: 变更文件均在允许范围内。")
        return 0

    print("发现越权文件：")
    for path in violations:
        print(f"- {path}")
    restore_cmd = "git restore --staged --worktree " + " ".join(violations)
    print("建议恢复命令：")
    print(restore_cmd)
    if has_untracked:
        print("提示：未跟踪文件请手动删除。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
