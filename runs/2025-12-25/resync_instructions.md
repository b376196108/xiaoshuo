# 归档同步指引 — 2025-12-25 — ch006

## 失败原因
- 不同步：正文版本更新晚于 E:/Lianghuagit/xiaoshuo/runs/2025-12-25/changelog.md (2025-12-21 18:36:16), E:/Lianghuagit/xiaoshuo/recap/chapter_summaries/ch006.md (2025-12-21 18:33:56), E:/Lianghuagit/xiaoshuo/state/state_patch.json (2025-12-21 18:35:49)（正文更新时间：2025-12-21 18:55:19）

## VSCode Codex 指令（可复制粘贴）
```
你是 Archivist。请严格按仓库规范工作，只写指定文件，路径必须完全一致，不要改名，不要输出到别处。

必须先阅读这些文件作为上下文：
- manuscript/ch006.md（以此为最新事实来源）
- runs/2025-12-25/chapter_plan.md
- state/current_state.json
- recap/rolling_recap.md
- prompts/roles/archivist.md
- canon/style/style_guide.md

任务：重新生成并写入以下文件（全部必须写入/覆盖旧内容）：
1) recap/chapter_summaries/ch006.md
2) recap/rolling_recap.md
3) state/state_patch.json（JSON 对象，仅 delta；必须包含 meta.current_chapter）
4) runs/2025-12-25/changelog.md（追加 synced_at 时间戳）

硬性要求：
- 只允许写入上述四个路径，不得修改其他文件
- state/state_patch.json 必须是严格 JSON 对象，仅 delta
- meta.current_chapter 必须为 "ch006"（字符串）
- 不生成任何小说正文

同步完成后请运行：
python tools/continuity_checks.py --date 2025-12-25 --chapter ch006
```

