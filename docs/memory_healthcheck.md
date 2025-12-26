# 内存健康检查指南

## 准备
1. 复制 `.env.example` 为 `.env`：
   ```powershell
   copy .env.example .env
   ```
2. 请务必以 **UTF-8（无 BOM）** 格式保存 `.env`，以免配置名前加上隐藏的 `\ufeff`。

## 安装依赖
```bash
pip install -r requirements.txt
```

## 运行方式
- 直接运行 Python 脚本：
  ```bash
  python scripts/healthcheck_memory.py
  ```
- 或通过 PowerShell 一键入口：
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/healthcheck_memory.ps1
  ```
两种方式都输出 Neo4j 与 Chroma 的健康结果，退出码 0 表示全部通过。

## 常见排查
| 场景 | 建议 |
| --- | --- |
| Neo4j 无法连接 | 检查 `NEO4J_URI` 的 bolt 协议、端口、用户名密码是否正确，防火墙/网络是否允许访问；超时可通过 `HEALTHCHECK_TIMEOUT` 调整。 |
| Neo4j 返回 `ok` 不是 1 | 确保 Neo4j 服务正常，不要在事务中返回多个记录；建议用 `neo4j` 工具或 Browser 验证查询。 |
| Chroma heartbeat 返回 404/500 | 确认 `CHROMA_HOST` 与 `CHROMA_PORT` 以及 `/api/v2/heartbeat` 路径是否可达，是否为 v2 接口。 |
| Chroma JSON 结构变化 | 脚本会尝试 `heartbeat`、`nanosecond heartbeat`、`nanosecond_heartbeat` 字段，若仍无，请检查服务版本并打印完整 payload 以补充适配。 |
| 环境变量解析失败 | 如果日志提示 `\ufeffNEO4J_URI`，说明 `.env` 被带了 BOM，重新用 UTF-8（无 BOM）保存即可。 |
