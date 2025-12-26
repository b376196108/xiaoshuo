import sys
from pathlib import Path

from neo4j import GraphDatabase

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from xiaoshuo_ai.config import load_settings
from xiaoshuo_ai.memory.neo4j_schema import ensure_constraints


def main() -> int:
    try:
        settings = load_settings()
        driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
            connection_timeout=settings.healthcheck_timeout,
        )
        ensure_constraints(driver)
        driver.close()
        print("[OK] 已完成 Neo4j 约束初始化")
        return 0
    except Exception as exc:
        print(f"[FAIL] 约束初始化失败: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

