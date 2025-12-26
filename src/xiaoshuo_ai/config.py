from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"

DEFAULT_TIMEOUT = 5.0
DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"

# 只提示一次，避免刷屏
_BOM_WARNED = False


@dataclass(frozen=True)
class Settings:
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    chroma_host: str
    chroma_port: int
    embed_model: str
    healthcheck_timeout: float = DEFAULT_TIMEOUT


def _get_env(name: str) -> Optional[str]:
    """
    兼容 .env 带 UTF-8 BOM 的情况：环境变量名可能变成 \ufeffNEO4J_URI。
    """
    global _BOM_WARNED

    candidates = (name, f"\ufeff{name}")
    for key in candidates:
        value = os.getenv(key)
        if value:
            if key != name and not _BOM_WARNED:
                print("[ENV] WARN: 检测到 .env 可能带 BOM，请用 UTF-8 无 BOM 保存（避免变量名异常）。")
                _BOM_WARNED = True
            return value.strip()
    return None


def load_settings() -> Settings:
    """
    从 repo 根目录 .env 加载配置，并返回 Settings。
    - 依赖 python-dotenv
    - override=True：避免终端残留变量影响排错
    """
    if not ENV_PATH.exists():
        raise FileNotFoundError("未找到 .env，请复制 .env.example 为 .env 并填写配置。")

    load_dotenv(ENV_PATH, override=True, encoding="utf-8")

    values: Dict[str, Optional[str]] = {
        "NEO4J_URI": _get_env("NEO4J_URI"),
        "NEO4J_USER": _get_env("NEO4J_USER"),
        "NEO4J_PASSWORD": _get_env("NEO4J_PASSWORD"),
        "CHROMA_HOST": _get_env("CHROMA_HOST"),
        "CHROMA_PORT": _get_env("CHROMA_PORT"),
    }

    missing = [k for k, v in values.items() if not v]
    if missing:
        raise RuntimeError(f"缺少环境变量：{', '.join(missing)}")

    # 明显未配置的密码占位符，直接拦截，避免后续脚本“连不上但不好定位”
    if values["NEO4J_PASSWORD"] == "CHANGE_ME":
        raise RuntimeError("NEO4J_PASSWORD 仍为 CHANGE_ME，请在 .env 中填写真实密码。")

    # timeout
    timeout_raw = _get_env("HEALTHCHECK_TIMEOUT")
    timeout = DEFAULT_TIMEOUT
    if timeout_raw:
        try:
            timeout = float(timeout_raw)
        except ValueError:
            print("[ENV] WARN: HEALTHCHECK_TIMEOUT 非数字，使用默认值 5 秒。")

    # chroma_port
    try:
        chroma_port = int(values["CHROMA_PORT"])
    except ValueError as exc:
        raise RuntimeError(f"CHROMA_PORT 非整数：{values['CHROMA_PORT']}") from exc

    embed_model = _get_env("EMBED_MODEL") or DEFAULT_EMBED_MODEL

    return Settings(
        neo4j_uri=values["NEO4J_URI"],         # type: ignore[arg-type]
        neo4j_user=values["NEO4J_USER"],       # type: ignore[arg-type]
        neo4j_password=values["NEO4J_PASSWORD"],  # type: ignore[arg-type]
        chroma_host=values["CHROMA_HOST"],     # type: ignore[arg-type]
        chroma_port=chroma_port,
        embed_model=embed_model,
        healthcheck_timeout=timeout,
    )


# 兼容更通用的命名（后续脚本建议用 get_settings）
def get_settings() -> Settings:
    return load_settings()
