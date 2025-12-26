import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import requests
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError


class ExitCodes:
    SUCCESS = 0
    ENV_MISSING = 10
    VAR_MISSING = 11
    VAR_PLACEHOLDER = 12
    NEO4J_FAIL = 21
    CHROMA_FAIL = 22


REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
DEFAULT_TIMEOUT = 5.0
HEARTBEAT_KEYS = ("heartbeat", "nanosecond heartbeat", "nanosecond_heartbeat")


def load_environment() -> bool:
    if not ENV_PATH.exists():
        print(f"[ENV] FAIL: .env 文件缺失，请参考 .env.example 并创建 (UTF-8 无 BOM)。")
        return False
    load_dotenv(ENV_PATH, override=True, encoding="utf-8")
    print("[ENV] OK: 已加载 .env")
    return True


def require_env(name: str) -> Optional[str]:
    candidates = (name, f"\ufeff{name}")
    value = None
    for key in candidates:
        value = os.getenv(key)
        if value:
            if key != name:
                print("[ENV] WARN: 你的 .env 可能包含 BOM，请使用 UTF-8 无 BOM 格式保存。")
            break
    if value:
        return value.strip()
    print(f"[ENV] FAIL: 缺少环境变量 {name}")
    return None


def validate_required_vars() -> tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], float]:
    neo4j_uri = require_env("NEO4J_URI")
    neo4j_user = require_env("NEO4J_USER")
    neo4j_password = require_env("NEO4J_PASSWORD")
    chroma_host = require_env("CHROMA_HOST")
    chroma_port = require_env("CHROMA_PORT")
    timeout_str = os.getenv("HEALTHCHECK_TIMEOUT", str(DEFAULT_TIMEOUT))
    try:
        timeout = float(timeout_str)
    except ValueError:
        timeout = DEFAULT_TIMEOUT
    return neo4j_uri, neo4j_user, neo4j_password, chroma_host, chroma_port, timeout


def check_placeholder(value: Optional[str], name: str) -> bool:
    if not value:
        return False
    if name == "NEO4J_PASSWORD" and value.strip().upper() == "CHANGE_ME":
        print("[ENV] FAIL: NEO4J_PASSWORD 仍为 CHANGE_ME，请替换为真实密码。")
        sys.exit(ExitCodes.VAR_PLACEHOLDER)
    return True


def check_neo4j(uri: str, user: str, password: str, timeout: float) -> bool:
    try:
        driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            connection_timeout=timeout,
        )
        driver.verify_connectivity()
        with driver.session() as session:
            record = session.run("RETURN 1 AS ok", timeout=timeout).single()
        driver.close()
        if record and record.get("ok") == 1:
            print("[Neo4j] OK: connectivity + RETURN 1")
            return True
        print("[Neo4j] FAIL: 返回结果异常，期望 ok=1")
        return False
    except Neo4jError as exc:
        print(f"[Neo4j] FAIL: {type(exc).__name__}: {exc}")
        print("hint: 检查 URI、账号、密码、bolt 端口或防火墙设置。")
        return False
    except Exception as exc:
        print(f"[Neo4j] FAIL: {type(exc).__name__}: {exc}")
        print("hint: 验证网络是否可达，或调高 HEALTHCHECK_TIMEOUT。")
        return False


def check_chroma(host: str, port: str, timeout: float) -> bool:
    url = f"http://{host}:{port}/api/v2/heartbeat"
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code != 200:
            print(f"[Chroma] FAIL: HTTP {response.status_code}")
            return False
        payload = response.json()
        heartbeat = None
        for key in HEARTBEAT_KEYS:
            if key in payload:
                heartbeat = payload[key]
                break
        if heartbeat is not None:
            print(f"[Chroma] OK: heartbeat={heartbeat}")
            return True
        print(f"[Chroma] FAIL: heartbeat 字段缺失 (payload={payload})")
        return False
    except requests.RequestException as exc:
        print(f"[Chroma] FAIL: {type(exc).__name__}: {exc}")
        return False
    except ValueError as exc:
        print(f"[Chroma] FAIL: JSON 解析失败: {exc}")
        return False


def main() -> int:
    if not load_environment():
        return ExitCodes.ENV_MISSING

    (
        neo4j_uri,
        neo4j_user,
        neo4j_password,
        chroma_host,
        chroma_port,
        timeout,
    ) = validate_required_vars()

    if not all((neo4j_uri, neo4j_user, neo4j_password, chroma_host, chroma_port)):
        return ExitCodes.VAR_MISSING

    if not check_placeholder(neo4j_password, "NEO4J_PASSWORD"):
        return ExitCodes.VAR_PLACEHOLDER

    neo4j_ok = check_neo4j(neo4j_uri, neo4j_user, neo4j_password, timeout)
    if not neo4j_ok:
        print("[EXIT] code=21")
        return ExitCodes.NEO4J_FAIL

    chroma_ok = check_chroma(chroma_host, chroma_port, timeout)
    if not chroma_ok:
        print("[EXIT] code=22")
        return ExitCodes.CHROMA_FAIL

    print("[PASS] memory healthcheck")
    return ExitCodes.SUCCESS


if __name__ == "__main__":
    sys.exit(main())
