"""Neo4j 最小约束初始化。"""

from neo4j import Driver


def ensure_constraints(driver: Driver) -> None:
    constraints = [
        "CREATE CONSTRAINT character_name_unique IF NOT EXISTS FOR (c:Character) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT location_name_unique IF NOT EXISTS FOR (l:Location) REQUIRE l.name IS UNIQUE",
    ]
    with driver.session() as session:
        for statement in constraints:
            session.run(statement)

