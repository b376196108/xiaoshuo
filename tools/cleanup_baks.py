#!/usr/bin/env python3
"""
清理 .bak 备份文件：每组仅保留最新 N 份。
仅使用标准库。
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


DEFAULT_EXCLUDES = {".git", "__pycache__", ".venv", "venv", "node_modules", "dist"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="清理 .bak 备份文件（默认仅预览）。")
    parser.add_argument("--apply", action="store_true", help="执行删除（默认仅预览）。")
    parser.add_argument(
        "--keep-latest",
        type=int,
        default=2,
        help="每组保留最新份数（默认 2）。",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="排除目录名（可重复传入）。",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="指定仓库根目录（默认自动探测）。",
    )
    parser.add_argument("--verbose", action="store_true", help="输出每组保留与删除明细。")
    return parser.parse_args()


def _try_get_repo_root() -> Optional[Path]:
    try:
        tools_dir = Path(__file__).resolve().parent
        sys.path.insert(0, str(tools_dir))
        from _common import get_repo_root  # type: ignore

        root = get_repo_root()
        return Path(root)
    except Exception:
        return None


def _find_repo_root(start: Path) -> Optional[Path]:
    cur = start.resolve()
    for parent in [cur] + list(cur.parents):
        if (parent / "tools").is_dir():
            return parent
    return None


def _resolve_root(root_arg: Optional[str]) -> Optional[Path]:
    if root_arg:
        path = Path(root_arg).expanduser().resolve()
        if path.exists():
            return path
        return None

    root = _try_get_repo_root()
    if root:
        return root
    return _find_repo_root(Path.cwd())


def _is_backup_name(name: str) -> Optional[str]:
    if not name.endswith(".bak") and ".bak" not in name:
        return None
    if name.endswith(".bak"):
        base = name[: -len(".bak")]
        return base if base else None
    if ".bak" in name:
        parts = name.rsplit(".bak", 1)
        if len(parts) != 2:
            return None
        base, tail = parts
        if not base:
            return None
        if tail.isdigit():
            return base
    return None


def _iter_files(root: Path, exclude_dirs: Set[str]) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for name in filenames:
            yield Path(dirpath) / name


def _group_backups(
    root: Path, exclude_dirs: Set[str]
) -> Tuple[Dict[Path, List[Path]], int, int, int]:
    groups: Dict[Path, List[Path]] = {}
    scanned = 0
    hits = 0
    errors = 0
    for path in _iter_files(root, exclude_dirs):
        scanned += 1
        base = _is_backup_name(path.name)
        if base is None:
            continue
        hits += 1
        key = (path.parent / base).resolve()
        groups.setdefault(key, []).append(path)
    return groups, scanned, hits, errors


def _sort_backups(paths: List[Path]) -> Tuple[List[Path], int]:
    errors = 0
    entries: List[Tuple[Path, float]] = []
    for path in paths:
        try:
            mtime = path.stat().st_mtime
        except Exception:
            errors += 1
            continue
        entries.append((path, mtime))
    entries.sort(key=lambda item: (-item[1], item[0].as_posix()))
    return [p for p, _ in entries], errors


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def main() -> int:
    args = parse_args()
    if args.keep_latest < 1:
        print("错误：--keep-latest 必须为正整数。")
        return 1

    root = _resolve_root(args.root)
    if root is None or not root.exists():
        print("错误：无法定位仓库根目录。")
        return 1

    exclude_dirs = set(DEFAULT_EXCLUDES)
    exclude_dirs.update([d for d in args.exclude_dir if d])

    groups, scanned, hits, group_errors = _group_backups(root, exclude_dirs)
    error_count = group_errors

    keep_latest = args.keep_latest
    planned_delete: List[Path] = []
    keep_map: Dict[Path, List[Path]] = {}
    delete_map: Dict[Path, List[Path]] = {}

    for key, backups in groups.items():
        sorted_backups, sort_errors = _sort_backups(backups)
        if sort_errors:
            error_count += sort_errors
        keep_list = sorted_backups[:keep_latest]
        delete_list = sorted_backups[keep_latest:]
        keep_map[key] = keep_list
        delete_map[key] = delete_list
        planned_delete.extend(delete_list)

    group_count = len(groups)
    planned_delete_count = len(planned_delete)
    deleted_count = 0
    skipped_count = 0

    if args.verbose:
        for key in sorted(keep_map.keys(), key=lambda p: p.as_posix()):
            print(f"[分组] {key.as_posix()}")
            print("保留：")
            if keep_map[key]:
                for path in keep_map[key]:
                    print(f"- {_relative(root, path)}")
            else:
                print("- 无")
            print("删除：")
            if delete_map[key]:
                for path in delete_map[key]:
                    print(f"- {_relative(root, path)}")
            else:
                print("- 无")
            print("")

    if planned_delete_count == 0:
        print("没有需要删除的备份文件。")
    else:
        print("将要删除的备份文件：")
        for path in planned_delete:
            print(f"- {_relative(root, path)}")

    if args.apply:
        for path in planned_delete:
            try:
                path.unlink()
                deleted_count += 1
            except FileNotFoundError:
                skipped_count += 1
            except Exception as exc:
                error_count += 1
                print(f"删除失败：{_relative(root, path)}；原因：{exc}")
    else:
        skipped_count = planned_delete_count
        print("当前为预览模式，未执行删除。")

    print("")
    print(f"扫描文件数：{scanned}")
    print(f"命中备份数：{hits}")
    print(f"分组数：{group_count}")
    print(f"每组保留数：{keep_latest}")
    print(f"计划删除数：{planned_delete_count}")
    print(f"实际删除数：{deleted_count}")
    print(f"跳过数：{skipped_count}")
    print(f"错误数：{error_count}")

    return 2 if error_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
