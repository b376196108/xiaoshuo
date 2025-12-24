import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from neo4j import GraphDatabase, Neo4jError


def load_environment(repo_root: Path) -> bool:
    env_path = repo_root / ".env"
    if not env_path.exists():
        print(
            f"环境文件未找到：{env_path}. 请复制 `.env.example` 并填入 Neo4j/Chroma 连接信息。"
        )
        return False

    load_dotenv(env_path)
    return True


def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        print(f"环境变量 `{var_name}` 未配置，请在 `.env` 中提供。")
    return value or ""


def check_neo4j(uri: str, user: str, password: str, timeout: float = 5.0) -> bool:
    try:
        with GraphDatabase.driver(
            uri,
            auth=(user, password),
            connection_timeout=timeout,
            max_connection_lifetime=30,
        ) as driver:
            with driver.session() as session:
                record = session.run("RETURN 1 AS ok", timeout=timeout).single()

        if record and record.get("ok") == 1:
            print("Neo4j: OK (ok=1)")
            return True

        print("Neo4j: FAIL (unexpected response)")
        return False
    except Neo4jError as exc:
        print(f"Neo4j: FAIL ({type(exc).__name__}: {exc})")
        return False
    except Exception as exc:  # pragma: no cover - integrations only
        print(f"Neo4j: FAIL ({type(exc).__name__}: {exc})")
        return False


def check_chroma(host: str, port: str, timeout: float = 5.0) -> bool:
    url = f"http://{host}:{port}/api/v2/heartbeat"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        payload = response.json()

        heartbeat = payload.get("heartbeat")
        if heartbeat:
            print(f"Chroma: OK (heartbeat={heartbeat})")
            return True

        print("Chroma: FAIL (heartbeat 字段缺失)")
        return False
    except requests.RequestException as exc:
        print(f"Chroma: FAIL ({type(exc).__name__}: {exc})")
        return False
    except ValueError as exc:
        print(f"Chroma: FAIL (JSON 解析失败: {exc})")
        return False


def main() -> int:
    script_root = Path(__file__).resolve().parent
    repo_root = script_root.parent

    if not load_environment(repo_root):
        return 1

    neo4j_uri = require_env("NEO4J_URI")
    neo4j_user = require_env("NEO4J_USER")
    neo4j_password = require_env("NEO4J_PASSWORD")
    chroma_host = require_env("CHROMA_HOST")
    chroma_port = require_env("CHROMA_PORT")

    if not all([neo4j_uri, neo4j_user, neo4j_password, chroma_host, chroma_port]):
        return 1

    neo4j_ok = check_neo4j(neo4j_uri, neo4j_user, neo4j_password)
    chroma_ok = check_chroma(chroma_host, chroma_port)

    if neo4j_ok and chroma_ok:
        print("Memory healthcheck: OK")
        return 0

    print("Memory healthcheck: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
