# 架构概览

xiaoshuo AI 栈在 A 机写作台与 B 机记忆服务器之间划分明确职责。A 机托管 CLI、编排器、Agents 与领域逻辑，B 机则在 Neo4j 中保存图记忆并用 Chroma 存储嵌入向量。通过配置变量与 Agent 管道协调章节规划、写作、复核与记忆提取的数据流。

后续版本应补充 `src/xiaoshuo_ai/core` 中的数据流路线、各 Agent 责任，以及 `prompts/` 目录下的提示模版如何被引用。

