# Chroma 软记忆最小闭环

## 三个集合与用途
- `chapter_summaries`：章节摘要，存章节提要与主要人物/地点元数据
- `style_snippets`：风格片段，存语气、口癖、句式等风格样本
- `scene_memory`：场景片段，存氛围描写与时空信息

### 元数据建议
- chapter_summaries：`type`, `chapter`, `char`, `loc`, `test`
- style_snippets：`type`, `tag`, `test`
- scene_memory：`type`, `loc`, `weather`, `test`

## 为什么 A 机计算向量
A 机负责嵌入计算，B 机仅负责存储与检索，这样可以：
- 控制模型版本与升级节奏
- 保持向量一致性与可迁移
- 减少 B 机的算力依赖

## 依赖安装
```bash
pip install -r requirements.txt
```

## 验收命令
```bash
python scripts/test_chroma_semantic.py
```
可选重置测试集合：
```bash
python scripts/test_chroma_semantic.py --reset
```

## 常见问题
- 端口不通/防火墙：确认 `CHROMA_HOST`、`CHROMA_PORT` 可访问
- API 路径：默认使用 `/api/v2/heartbeat`
- 模型下载失败：提前下载模型或配置镜像源，再执行脚本
- Top1 未命中：可尝试调整 `n_results`、使用更区分的测试文本或更换空间度量参数

