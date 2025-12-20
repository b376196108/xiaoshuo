from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

REPO_BASENAME = "xiaoshuo"
REPO_MARKER = ".xiaoshuo_repo_root"
REPO_MARKER_CONTENT = "This repo is the production root for Novel Studio."


def get_repo_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    marker = root / REPO_MARKER
    if root.name != REPO_BASENAME and not marker.exists():
        raise RuntimeError(
            f"Safety check failed: expected repo root basename '{REPO_BASENAME}' "
            f"or marker '{REPO_MARKER}', got '{root}'."
        )
    if root.name == REPO_BASENAME and marker.exists():
        try:
            content = marker.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            content = ""
        if content and content != REPO_MARKER_CONTENT:
            raise RuntimeError(
                f"Safety check failed: marker content mismatch in '{marker}'."
            )
    return root


def iso_today() -> str:
    return date.today().isoformat()


def now_utc_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def safe_write_text(path: Path, text: str, *, backup: bool = True) -> None:
    ensure_dir(path.parent)
    if backup and path.exists():
        backup_path = path.with_name(path.name + ".bak")
        backup_path.write_text(read_text(path), encoding="utf-8")
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: Any, *, backup: bool = True) -> None:
    text = json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    safe_write_text(path, text, backup=backup)


def parse_chapter_num_from_id(chapter_id: str) -> int | None:
    match = re.fullmatch(r"ch(\\d{3})", chapter_id.strip())
    if not match:
        return None
    return int(match.group(1))


def parse_chapter_num_from_filename(filename: str) -> int | None:
    match = re.fullmatch(r"ch(\\d+)\\.md", filename)
    if not match:
        return None
    return int(match.group(1))


def chapter_id(n: int) -> str:
    return f"ch{n:03d}"


def infer_next_chapter_num(manuscript_dir: Path) -> int:
    max_seen = 0
    if not manuscript_dir.exists():
        return 1
    for path in manuscript_dir.glob("ch*.md"):
        n = parse_chapter_num_from_filename(path.name)
        if n is not None:
            max_seen = max(max_seen, n)
    return max_seen + 1 if max_seen > 0 else 1


def setup_logger(
    name: str, *, log_file: Path | None = None, verbose: bool = False
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.propagate = False

    stream = logging.StreamHandler(stream=sys.stderr)
    stream.setLevel(logging.DEBUG if verbose else logging.INFO)
    stream.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(stream)

    if log_file is not None:
        ensure_dir(log_file.parent)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)sZ [%(levelname)s] %(message)s")
        )
        logger.addHandler(file_handler)

    return logger


def is_codex_available() -> bool:
    return shutil.which("codex") is not None


def sha256_hex_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class FileHash:
    path: str
    size: int
    sha256: str
    head_bytes: int
    head_sha256: str


def hash_file(path: Path, *, head_bytes: int = 32768) -> FileHash:
    total = 0
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            h.update(chunk)

    with path.open("rb") as f:
        head = f.read(head_bytes)

    return FileHash(
        path=path.as_posix(),
        size=total,
        sha256=h.hexdigest(),
        head_bytes=min(head_bytes, total),
        head_sha256=sha256_hex_bytes(head),
    )


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file():
            yield path

