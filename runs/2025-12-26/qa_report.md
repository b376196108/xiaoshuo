QA_RESULT: PASS

# QA 报告 — 2025-12-26 — ch007

## 硬失败
- （无）

## 警告
- （无）

## 章节号一致性
- 目标章节：ch007
- state_patch.meta.current_chapter：ch007
- state.current_state.meta.current_chapter：ch006（允许落后，属正常）

## 正文字数
- 正文字符数: 3073
- 最低要求: 3000

## open_loops 校验
- 章纲标注推进: ['loop_food_shortage', 'loop_toxic_neighbor']
- 章纲路径: E:/Lianghuagit/xiaoshuo/runs/2025-12-26/chapter_plan.md
- 摘要路径: E:/Lianghuagit/xiaoshuo/recap/chapter_summaries/ch007.md
- state_patch 路径: E:/Lianghuagit/xiaoshuo/state/state_patch.json

## 爽文卡口检查
- 规则标签命中: PASS（未发现落袋/代价/旁观/下一步标签前缀）
- must_include_lines: FOUND（解析到 4/4 句）
- 四句落地: PASS（正文逐字命中）
- verdict_line: PASS（里正一拍桌子：“三日清沟不到位，名册就照旧扣。”）
- crowd_beats: PASS（3 条逐字命中；顺序=OK）

## 占位符/问号串检测
- chapter_plan: PASS
- changelog: PASS

## 归档同步
- 正文: E:/Lianghuagit/xiaoshuo/manuscript/ch007.md | 时间：2025-12-21 20:18:25
- 章节摘要: E:/Lianghuagit/xiaoshuo/recap/chapter_summaries/ch007.md | 时间：2025-12-21 20:37:21
- 状态补丁: E:/Lianghuagit/xiaoshuo/state/state_patch.json | 时间：2025-12-21 20:37:21
- 变更日志: E:/Lianghuagit/xiaoshuo/runs/2025-12-26/changelog.md | 时间：2025-12-21 20:37:21

## 推荐返工步骤（仅 FAIL 时）
1) 补齐缺失产物（chapter_plan / manuscript / summary / patch）。
2) 确保章纲推进 >=2 条 open_loops，并明确写出 id。
3) 更新 summary + state_patch，让每条计划 loop 的 id 明确出现。
4) 重跑：`python tools/continuity_checks.py --date 2025-12-26 --chapter ch007`
