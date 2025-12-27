# 外部模型接入与手动续写方案可执行性评估

## 目的
依据仓库现有源码与文档，对《AI小说写作系统：外部模型接入与结构化数据集成方案.docx》和《AI小说写作手动续写方案.docx》提出的流程进行落地性判断，并给出可执行的实现路径。

## 现状评估
- **代码骨架不足**：`src/xiaoshuo_ai/cli.py` 仍是占位，缺少任何编排、监听或数据库交互逻辑；`src/xiaoshuo_ai/config.py` 仅提供环境变量加载功能，尚未暴露 Neo4j/Chroma 客户端。仓库内不存在脚本目录中所需的 `context_packer.py`、`file_watcher.py`、`clipboard_monitor.py` 等文件。【F:src/xiaoshuo_ai/cli.py†L1-L7】【F:src/xiaoshuo_ai/config.py†L1-L88】
- **运行期目录为空**：`runtime/` 下仅有 `.gitkeep`，没有章节文件或监听入口，无法直接触发文档所述的“保存即同步”链路。
- **文档与模板未绑定代码**：`docs/`、`prompts/` 描述了架构和提示语，但缺少将 CPACK 模板、隐写 JSON 及冲突检测逻辑接入的实现。当前缺失 Neo4j/Chroma 连接封装、实体/关系模式定义及更新流程。

## 文档方案可执行性判断
文档提出的关键能力（剪贴板导出 CPACK、手动粘贴外部模型、文件监听回填并写入 Neo4j/Chroma、冲突检测提示）在当前代码中均无对应实现。现有仓库仅能读取配置，尚无法直接运行文档级别的流程，需补齐一系列模块后方可执行。

## 可执行落地方案
以下步骤按模块拆解，可在当前目录结构内实现文档要求：

1. **基础配置与依赖**
   - 在 `requirements.txt` 增补 `neo4j`, `chromadb`, `watchdog`, `pyperclip`, `pydantic` 等依赖，并在 `README.md` 写明 A/B 机安装命令与 `.env` 配置示例。
   - 在 `configs/` 新增 `memory.yaml`（含 Neo4j/Chroma 端点、重试/超时设置）与 `prompt_templates.yaml`（存放 CPACK 模板、隐写 JSON 字段定义）。

2. **记忆服务客户端封装**
   - 新建 `src/xiaoshuo_ai/memory/graph/client.py`：基于 `neo4j` 驱动，提供 `get_driver(settings)`、`upsert_entities`、`upsert_relationships`、`write_chapter_summary` 等方法，内部处理会话、幂等性和冲突检测（如状态差异时返回冲突详情）。
   - 新建 `src/xiaoshuo_ai/memory/vector/client.py`：封装 `chromadb.HttpClient`，暴露 `ensure_collection(book_id)`、`add_embeddings(chapter_id, texts, metadatas)`、`query` 等接口。
   - 为两类客户端增加健康检查函数，供后续 CLI/服务启动前验证连接。

3. **CPACK 构建与剪贴板导出**
   - 在 `src/xiaoshuo_ai/bridge/context_packer.py` 实现 `build_cpack(chapter_path, intent, settings)`：
     - 读取 `runtime/chapters/*.md` 的正文与元数据标记。
     - 查询 Neo4j（当前活跃角色、地点、状态）和 Chroma（Top-k 相关片段），按模板填充 CPACK，附带隐写指令要求外部模型输出 `{summary, new_entities, relationship_updates}` JSON。
   - 在 `src/xiaoshuo_ai/bridge/clipboard.py` 提供 `copy_cpack_to_clipboard(cpack_text)`，并加入终端提示，便于用户在额度耗尽时手动触发。
   - 将上述能力挂到 `cli.py` 的子命令 `export-cpack`，接受章节文件路径与续写意图参数。

4. **文件监听与回填处理**
   - 新建 `src/xiaoshuo_ai/bridge/file_watcher.py`：使用 `watchdog` 监听 `runtime/chapters/`。当检测到保存事件，解析文件末尾的 JSON 区块：
     - 通过 `pydantic` 模型验证 `{summary, new_entities, relationship_updates}` 格式。
     - 调用 Neo4j 客户端写入/更新实体与关系；若检测到冲突（例如同名实体状态不同），记录日志并提示用户选择覆盖或跳过。
     - 调用 Chroma 客户端写入正文向量，并关联章节 ID、角色列表等元数据。
   - 监听器提供守护线程启动函数，供 CLI 子命令 `sync-loop` 启动，或在 VS Code 任务中持续运行。

5. **手动续写人机回路**
   - 在 `docs/usage.md` 中新增“API 限额 fallback”章节，描述：
     1) 运行 `xiaoshuo export-cpack --chapter runtime/chapters/ch1.md --intent "..."`。
     2) 将 CPACK 粘贴至外部模型（ChatGPT/Gemini）并获得续写。
     3) 将生成内容含隐写 JSON 粘贴回原 Markdown 并保存。
     4) 后台 `sync-loop` 自动解析并同步 Neo4j/Chroma；如出现冲突，用户按终端提示决策覆盖。

6. **测试与验证**
   - 在 `tests/` 添加最小集成测试：
     - 使用临时 Neo4j/Chroma 模拟服务或 test double，验证 `build_cpack` 能填充模板并包含隐写指令。
     - 验证文件监听对有效/无效 JSON 的处理（成功写入 vs. 校验失败）。
   - 提供 `scripts/healthcheck_memory.py`，调用客户端健康检查确保 B 机可用。

完成以上步骤后，即可覆盖文档要求的核心链路：手动导出 CPACK、外部模型续写、监听文件回填并同步结构化数据，同时具备冲突处理与双机配置支撑。
