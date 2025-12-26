from __future__ import annotations

"""
Neo4j Store（工程核心）
目的：提供“幂等写入”能力，让记忆库长期稳定：
- upsert_node：按 (project_id, _key) MERGE 节点
- upsert_relation：按同一 project_id 下的两端节点 MERGE 关系

注意：
1) 你的 Neo4j 是远端（192.168.1.195），程序连接必须走 bolt 端口 7687
2) 连接信息统一从环境变量读取，便于部署与切换环境
3) 为了支持“多本书/多项目”，所有写入都必须携带 project_id

环境变量（建议）：
- NEO4J_URI      例如：bolt://192.168.1.195:7687
- NEO4J_USER     例如：neo4j
- NEO4J_PASSWORD 你的密码
- NEO4J_DATABASE 可选（Neo4j Community 通常不用）

项目隔离环境变量（建议）：
- XIAOSHUO_PROJECT_ID   例如：book_demo_001
- XIAOSHUO_MODE         dev / prod（默认 dev）
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from neo4j import GraphDatabase


@dataclass
class Neo4jConfig:
    """Neo4j 连接配置"""
    uri: str
    user: str
    password: str
    database: Optional[str] = None


def load_neo4j_config_from_env() -> Neo4jConfig:
    """
    从环境变量读取 Neo4j 连接信息
    说明：默认值为本地，实际部署请在运行脚本前设置环境变量
    """
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "neo4j")
    database = os.getenv("NEO4J_DATABASE")  # 可选
    return Neo4jConfig(uri=uri, user=user, password=password, database=database)


class Neo4jStore:
    """Neo4j 数据写入封装（幂等）"""

    def __init__(self, cfg: Neo4jConfig):
        self.cfg = cfg
        self.driver = GraphDatabase.driver(cfg.uri, auth=(cfg.user, cfg.password))

    def close(self) -> None:
        """关闭连接"""
        self.driver.close()

    def upsert_node(self, label: str, project_id: str, key: str, props: Dict[str, Any]) -> None:
        """
        幂等写入节点：
        - 使用 (project_id, _key) 作为 MERGE 条件（生产建议对该组合建立唯一约束）
        - ON CREATE：写 created_at（只写一次）
        - SET：合并 props（包含 updated_at 等）

        约定：
        - props 内应包含 project_id/_key/_id/_hash 等字段（由 key_builder.augment_node_props 生成）
        """
        if not project_id:
            raise ValueError("project_id 不能为空（用于项目隔离）")

        # 防呆：避免外部传错 project_id 与 props 内不一致
        if "project_id" in props and str(props["project_id"]) != str(project_id):
            raise ValueError("upsert_node: 传入的 project_id 与 props['project_id'] 不一致")

        cypher = f"""
        MERGE (n:{label} {{project_id: $project_id, _key: $key}})
        ON CREATE SET
          n.created_at = coalesce(n.created_at, $created_at)
        SET
          n += $props
        """

        created_at = props.get("created_at") or props.get("updated_at")

        with self.driver.session(database=self.cfg.database) as session:
            session.run(cypher, project_id=project_id, key=key, props=props, created_at=created_at)

    def upsert_relation(
        self,
        rel_type: str,
        project_id: str,
        from_label: str,
        from_key: str,
        to_label: str,
        to_key: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        幂等写入关系：
        - 先 MATCH 两端节点（同一 project_id 下，按 _key）
        - 再 MERGE 关系（重复写入不产生多条边）
        - 关系上也写 project_id，便于统计与隔离
        """
        if not project_id:
            raise ValueError("project_id 不能为空（用于项目隔离）")

        props = props or {}
        rel_props = dict(props)
        rel_props["project_id"] = project_id

        cypher = f"""
        MATCH (a:{from_label} {{project_id: $project_id, _key: $from_key}})
        MATCH (b:{to_label}   {{project_id: $project_id, _key: $to_key}})
        MERGE (a)-[r:{rel_type} {{project_id: $project_id}}]->(b)
        SET r += $props
        """

        with self.driver.session(database=self.cfg.database) as session:
            session.run(
                cypher,
                project_id=project_id,
                from_key=from_key,
                to_key=to_key,
                props=rel_props,
            )

    def count_nodes(self, label: str, project_id: Optional[str] = None) -> int:
        """统计某类节点数量（验收用）。传 project_id 则只统计该项目。"""
        if project_id:
            cypher = f"MATCH (n:{label} {{project_id: $pid}}) RETURN count(n) AS c"
            params = {"pid": project_id}
        else:
            cypher = f"MATCH (n:{label}) RETURN count(n) AS c"
            params = {}

        with self.driver.session(database=self.cfg.database) as session:
            rec = session.run(cypher, **params).single()
            return int(rec["c"]) if rec else 0

    def count_rels(self, rel_type: str, project_id: Optional[str] = None) -> int:
        """统计某类关系数量（验收用）。传 project_id 则只统计该项目。"""
        if project_id:
            cypher = f"MATCH ()-[r:{rel_type} {{project_id: $pid}}]->() RETURN count(r) AS c"
            params = {"pid": project_id}
        else:
            cypher = f"MATCH ()-[r:{rel_type}]->() RETURN count(r) AS c"
            params = {}

        with self.driver.session(database=self.cfg.database) as session:
            rec = session.run(cypher, **params).single()
            return int(rec["c"]) if rec else 0
