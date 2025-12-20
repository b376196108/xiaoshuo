from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [
    "inputs",
    "canon",
    "outline",
    "state",
    "recap",
    "prompts",
    "pipelines",
    "runs",
    "scripts",
    "tools",
]
EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".py"}
ENCODINGS = ["utf-8", "utf-8-sig", "gbk", "utf-16", "utf-16le", "utf-16be"]


def _iter_files(root: Path) -> Iterable[Path]:
    for rel in SCAN_DIRS:
        base = root / rel
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in EXTENSIONS:
                yield path


def _decode_bytes(data: bytes) -> tuple[str, str | None, bool]:
    if data.startswith(b"\xef\xbb\xbf"):
        try:
            return data.decode("utf-8-sig"), "utf-8-sig", True
        except UnicodeDecodeError:
            pass
    for enc in ENCODINGS:
        try:
            return data.decode(enc), enc, True
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace"), None, False


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _is_suspected_garbled(text: str) -> bool:
    if "?" * 3 in text:
        return True
    if "\ufffd" in text:
        return True
    non_ws = [c for c in text if not c.isspace()]
    if not non_ws:
        return False
    qmarks = sum(1 for c in non_ws if c == "?")
    han = sum(1 for c in non_ws if "\u4e00" <= c <= "\u9fff")
    latin1 = sum(1 for c in non_ws if 0x00A0 <= ord(c) <= 0x00FF)
    q_ratio = qmarks / len(non_ws)
    han_ratio = han / len(non_ws)
    latin1_ratio = latin1 / len(non_ws)
    if len(non_ws) > 120 and q_ratio > 0.08 and han_ratio < 0.05:
        return True
    if len(non_ws) > 120 and latin1_ratio > 0.15 and han_ratio < 0.05:
        return True
    return False


def _ensure_backup(path: Path) -> None:
    if not path.exists():
        return
    backup = path.with_name(path.name + ".bak")
    if backup.exists():
        backup = path.with_name(path.name + ".bak2")
        if backup.exists():
            return
    backup.write_bytes(path.read_bytes())


def _write_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main() -> int:
    results: list[dict[str, str]] = []
    converted: list[str] = []
    suspected: list[str] = []
    failed: list[str] = []
    skipped: list[str] = []

    for path in _iter_files(ROOT):
        data = path.read_bytes()
        text, encoding, decode_ok = _decode_bytes(data)
        garbled = _is_suspected_garbled(text)
        rel = path.relative_to(ROOT).as_posix()

        action = "ok"
        reason = ""

        if not decode_ok:
            action = "fail"
            reason = "decode_failed"
            failed.append(f"{rel} ({reason})")
        elif garbled:
            action = "suspected_garbled"
            suspected.append(rel)
        else:
            if path.suffix.lower() == ".json":
                try:
                    json.loads(text)
                except Exception as e:  # noqa: BLE001
                    action = "fail"
                    reason = f"json_parse_failed: {e}"
                    failed.append(f"{rel} ({reason})")

            if action == "ok":
                normalized = _normalize_newlines(text)
                has_bom = data.startswith(b"\xef\xbb\xbf")
                needs_write = (encoding != "utf-8") or has_bom or (normalized != text)
                if needs_write:
                    _ensure_backup(path)
                    _write_utf8(path, normalized)
                    action = "converted"
                    converted.append(f"{rel} (from {encoding or 'unknown'})")
                else:
                    skipped.append(rel)

        results.append(
            {
                "path": rel,
                "encoding": encoding or "unknown",
                "decode_ok": "yes" if decode_ok else "no",
                "garbled": "yes" if garbled else "no",
                "action": action,
                "reason": reason,
            }
        )

    report_lines: list[str] = []
    report_lines.append("# ENCODING_AUDIT")
    report_lines.append("")
    report_lines.append("## Summary")
    report_lines.append(f"- scanned: {len(results)}")
    report_lines.append(f"- converted: {len(converted)}")
    report_lines.append(f"- suspected_garbled: {len(suspected)}")
    report_lines.append(f"- failed: {len(failed)}")
    report_lines.append(f"- already_utf8: {len(skipped)}")
    report_lines.append("")

    report_lines.append("## Converted To UTF-8")
    if converted:
        report_lines.extend(f"- {item}" for item in converted)
    else:
        report_lines.append("- (none)")
    report_lines.append("")

    report_lines.append("## Suspected Garbled / Content Lost")
    if suspected:
        report_lines.extend(f"- {item}" for item in suspected)
    else:
        report_lines.append("- (none)")
    report_lines.append("")

    report_lines.append("## Failures")
    if failed:
        report_lines.extend(f"- {item}" for item in failed)
    else:
        report_lines.append("- (none)")
    report_lines.append("")

    report_lines.append("## Per-File Results")
    for item in results:
        report_lines.append(
            f"- {item['path']} | encoding={item['encoding']} | decode_ok={item['decode_ok']} "
            f"| garbled={item['garbled']} | action={item['action']}"
            + (f" | reason={item['reason']}" if item["reason"] else "")
        )

    report_path = ROOT / "runs" / "ENCODING_AUDIT.md"
    _ensure_backup(report_path)
    _write_utf8(report_path, "\n".join(report_lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
