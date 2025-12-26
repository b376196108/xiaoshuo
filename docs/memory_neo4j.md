# Neo4j 硬记忆最小闭环

## 当前落地范围
- 节点：`Character`、`Location`
- 关系：`KNOWS`、`ALLY`、`ENEMY`、`LOCATED_IN`
- 保留规划：`Item`、`Event`、`OWNS`、`CAUSES`（本阶段未实现）

## Schema 初始化
运行：
```bash
python scripts/bootstrap_neo4j_schema.py
```
预期结果：
- 创建 `Character.name` 与 `Location.name` 的唯一约束
- 输出 `[OK] 已完成 Neo4j 约束初始化`

## 幂等写入验证
运行：
```bash
python scripts/test_neo4j_idempotent.py
```
预期结果：
- 连续写入同名角色 10 次，图中只保留 1 个节点
- 属性应被最后一次写入覆盖
- 输出 `[PASS] 幂等写入验证通过`

## 关系类型说明
- `KNOWS`：认识/熟人
- `ALLY`：盟友
- `ENEMY`：对立
- `LOCATED_IN`：角色当前所在地点

## 常见排查
- 连接失败：检查 `NEO4J_URI` 的 bolt 地址、端口、账号密码与防火墙
- 约束未生效：确认数据库可写且当前用户有权限创建约束
- 关系写入异常：关系类型仅允许 `KNOWS/ALLY/ENEMY`，禁止拼接用户输入

