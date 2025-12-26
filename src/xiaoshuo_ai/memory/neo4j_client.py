"""Neo4j 硬记忆客户端。"""

from __future__ import annotations

from typing import Dict, List, Optional

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from xiaoshuo_ai.config import Settings


class Neo4jMemoryClient:
    """Neo4j 最小闭环客户端，提供幂等写入与查询。"""

    _RELATION_MAP = {
        "KNOWS": "KNOWS",
        "ALLY": "ALLY",
        "ENEMY": "ENEMY",
    }

    def __init__(self, settings: Settings):
        self._settings = settings
        self._driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
            connection_timeout=settings.healthcheck_timeout,
        )

    def close(self) -> None:
        self._driver.close()

    def healthcheck(self) -> None:
        self._driver.verify_connectivity()
        with self._driver.session() as session:
            record = session.run("RETURN 1 AS ok").single()
        if not record or record.get("ok") != 1:
            raise RuntimeError("Neo4j 返回结果异常，期望 ok=1")

    def upsert_character(self, name: str, props: Dict) -> None:
        cypher = "MERGE (c:Character {name:$name}) SET c += $props"
        with self._driver.session() as session:
            session.run(cypher, name=name, props=props or {})

    def upsert_location(self, name: str, props: Dict) -> None:
        cypher = "MERGE (l:Location {name:$name}) SET l += $props"
        with self._driver.session() as session:
            session.run(cypher, name=name, props=props or {})

    def relate_character(self, a: str, rel: str, b: str, props: Optional[Dict] = None) -> None:
        rel_type = self._RELATION_MAP.get(rel)
        if not rel_type:
            raise ValueError("关系类型不被允许，仅支持 KNOWS/ALLY/ENEMY")
        cypher = (
            "MERGE (a:Character {name:$a}) "
            "MERGE (b:Character {name:$b}) "
            f"MERGE (a)-[r:{rel_type}]->(b) "
            "SET r += $props"
        )
        with self._driver.session() as session:
            session.run(cypher, a=a, b=b, props=props or {})

    def set_character_location(
        self, character: str, location: str, props: Optional[Dict] = None
    ) -> None:
        cypher = (
            "MERGE (c:Character {name:$character}) "
            "MERGE (l:Location {name:$location}) "
            "MERGE (c)-[r:LOCATED_IN]->(l) "
            "SET r += $props"
        )
        with self._driver.session() as session:
            session.run(
                cypher,
                character=character,
                location=location,
                props=props or {},
            )

    def get_character_bundle(self, name: str, limit: int = 20) -> Dict:
        with self._driver.session() as session:
            record = session.run(
                "MATCH (c:Character {name:$name}) RETURN c",
                name=name,
            ).single()
            if not record:
                return {}
            character = dict(record["c"])

            loc_record = session.run(
                "MATCH (c:Character {name:$name}) "
                "OPTIONAL MATCH (c)-[:LOCATED_IN]->(l:Location) "
                "RETURN l LIMIT 1",
                name=name,
            ).single()
            location = dict(loc_record["l"]) if loc_record and loc_record["l"] else None

            rel_records = session.run(
                "MATCH (c:Character {name:$name})-" 
                "[r:KNOWS|ALLY|ENEMY]-" 
                "(o:Character) "
                "RETURN type(r) AS rel, o.name AS name "
                "LIMIT $limit",
                name=name,
                limit=limit,
            )
            relations = [{"type": row["rel"], "name": row["name"]} for row in rel_records]

        return {
            "character": character,
            "location": location,
            "relations": relations,
        }

