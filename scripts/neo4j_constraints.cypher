// 自动生成：scripts/generate_neo4j_constraints.py
// 用途：在 Neo4j Browser 或 cypher-shell 中执行。可重复执行（IF NOT EXISTS）。
// 当前模式：开启项目隔离（组合唯一/组合索引），隔离字段：project_id
// 重要：若旧库存在“全局唯一约束”（例如 _key 唯一），需要先 DROP 再应用本文件。
// 建议：先为历史数据补齐 project_id（例如 legacy_default），再做约束迁移。

CREATE CONSTRAINT Character_id_unique IF NOT EXISTS FOR (n:Character) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Character_key_unique IF NOT EXISTS FOR (n:Character) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Character_ukeys_name_unique IF NOT EXISTS FOR (n:Character) REQUIRE (n.project_id, n.name) IS UNIQUE;
CREATE INDEX Character_project_idx IF NOT EXISTS FOR (n:Character) ON (n.project_id);
CREATE INDEX Character_name_idx IF NOT EXISTS FOR (n:Character) ON (n.project_id, n.name);

CREATE CONSTRAINT Location_id_unique IF NOT EXISTS FOR (n:Location) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Location_key_unique IF NOT EXISTS FOR (n:Location) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Location_ukeys_name_unique IF NOT EXISTS FOR (n:Location) REQUIRE (n.project_id, n.name) IS UNIQUE;
CREATE INDEX Location_project_idx IF NOT EXISTS FOR (n:Location) ON (n.project_id);
CREATE INDEX Location_name_idx IF NOT EXISTS FOR (n:Location) ON (n.project_id, n.name);

CREATE CONSTRAINT Item_id_unique IF NOT EXISTS FOR (n:Item) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Item_key_unique IF NOT EXISTS FOR (n:Item) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Item_ukeys_name_type_unique IF NOT EXISTS FOR (n:Item) REQUIRE (n.project_id, n.name, n.type) IS UNIQUE;
CREATE INDEX Item_project_idx IF NOT EXISTS FOR (n:Item) ON (n.project_id);
CREATE INDEX Item_name_idx IF NOT EXISTS FOR (n:Item) ON (n.project_id, n.name);

CREATE CONSTRAINT Event_id_unique IF NOT EXISTS FOR (n:Event) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Event_key_unique IF NOT EXISTS FOR (n:Event) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Event_ukeys_key_unique IF NOT EXISTS FOR (n:Event) REQUIRE (n.project_id, n.key) IS UNIQUE;
CREATE INDEX Event_project_idx IF NOT EXISTS FOR (n:Event) ON (n.project_id);
CREATE INDEX Event_key_idx IF NOT EXISTS FOR (n:Event) ON (n.project_id, n.key);
CREATE INDEX Event_chapter_no_idx IF NOT EXISTS FOR (n:Event) ON (n.project_id, n.chapter_no);

CREATE CONSTRAINT Faction_id_unique IF NOT EXISTS FOR (n:Faction) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Faction_key_unique IF NOT EXISTS FOR (n:Faction) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Faction_ukeys_name_unique IF NOT EXISTS FOR (n:Faction) REQUIRE (n.project_id, n.name) IS UNIQUE;
CREATE INDEX Faction_project_idx IF NOT EXISTS FOR (n:Faction) ON (n.project_id);
CREATE INDEX Faction_name_idx IF NOT EXISTS FOR (n:Faction) ON (n.project_id, n.name);

CREATE CONSTRAINT Skill_id_unique IF NOT EXISTS FOR (n:Skill) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Skill_key_unique IF NOT EXISTS FOR (n:Skill) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Skill_ukeys_name_unique IF NOT EXISTS FOR (n:Skill) REQUIRE (n.project_id, n.name) IS UNIQUE;
CREATE INDEX Skill_project_idx IF NOT EXISTS FOR (n:Skill) ON (n.project_id);
CREATE INDEX Skill_name_idx IF NOT EXISTS FOR (n:Skill) ON (n.project_id, n.name);

CREATE CONSTRAINT Scene_id_unique IF NOT EXISTS FOR (n:Scene) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Scene_key_unique IF NOT EXISTS FOR (n:Scene) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Scene_ukeys_key_unique IF NOT EXISTS FOR (n:Scene) REQUIRE (n.project_id, n.key) IS UNIQUE;
CREATE INDEX Scene_project_idx IF NOT EXISTS FOR (n:Scene) ON (n.project_id);
CREATE INDEX Scene_key_idx IF NOT EXISTS FOR (n:Scene) ON (n.project_id, n.key);
CREATE INDEX Scene_chapter_no_idx IF NOT EXISTS FOR (n:Scene) ON (n.project_id, n.chapter_no);
CREATE INDEX Scene_location_name_idx IF NOT EXISTS FOR (n:Scene) ON (n.project_id, n.location_name);

CREATE CONSTRAINT PlotThread_id_unique IF NOT EXISTS FOR (n:PlotThread) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT PlotThread_key_unique IF NOT EXISTS FOR (n:PlotThread) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT PlotThread_ukeys_key_unique IF NOT EXISTS FOR (n:PlotThread) REQUIRE (n.project_id, n.key) IS UNIQUE;
CREATE INDEX PlotThread_project_idx IF NOT EXISTS FOR (n:PlotThread) ON (n.project_id);
CREATE INDEX PlotThread_name_idx IF NOT EXISTS FOR (n:PlotThread) ON (n.project_id, n.name);
CREATE INDEX PlotThread_key_idx IF NOT EXISTS FOR (n:PlotThread) ON (n.project_id, n.key);

CREATE CONSTRAINT Chapter_id_unique IF NOT EXISTS FOR (n:Chapter) REQUIRE (n.project_id, n._id) IS UNIQUE;
CREATE CONSTRAINT Chapter_key_unique IF NOT EXISTS FOR (n:Chapter) REQUIRE (n.project_id, n._key) IS UNIQUE;
CREATE CONSTRAINT Chapter_ukeys_chapter_no_unique IF NOT EXISTS FOR (n:Chapter) REQUIRE (n.project_id, n.chapter_no) IS UNIQUE;
CREATE INDEX Chapter_project_idx IF NOT EXISTS FOR (n:Chapter) ON (n.project_id);
CREATE INDEX Chapter_chapter_no_idx IF NOT EXISTS FOR (n:Chapter) ON (n.project_id, n.chapter_no);
