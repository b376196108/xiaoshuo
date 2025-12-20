from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "tools" / "prepare_next_run.py",
        root / "scripts" / "prepare_next.bat",
        root / "state" / "current_state.json",
        root / "inputs" / "project_brief.json",
    ]
    missing = [p for p in required if not p.exists()]
    if missing:
        for p in missing:
            print(f"缺失关键文件：{p.as_posix()}")
        return 1
    print("OK: doctor pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())