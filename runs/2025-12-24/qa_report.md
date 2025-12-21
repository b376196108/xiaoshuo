QA_RESULT: PASS

# QA 报告 — 2025-12-24 — ch005

## 硬失败
- （无）

## 警告
- （无）

## 章节号一致性
- 目标章节：ch005
- state_patch.meta.current_chapter：ch005
- state.current_state.meta.current_chapter：ch004（允许落后，属正常）

## 正文字数
- 正文字符数: 3088
- 最低要求: 3000

## open_loops 校验
- 章纲标注推进: ['loop_food_shortage', 'loop_toxic_neighbor']
- 章纲路径: E:/Lianghuagit/xiaoshuo/runs/2025-12-24/chapter_plan.md
- 摘要路径: E:/Lianghuagit/xiaoshuo/recap/chapter_summaries/ch005.md
- state_patch 路径: E:/Lianghuagit/xiaoshuo/state/state_patch.json

## 占位符/问号串检测
- chapter_plan: PASS
- changelog: PASS

## 归档同步
- 正文: E:/Lianghuagit/xiaoshuo/manuscript/ch005.md | 时间：2025-12-21 13:47:47
- 章节摘要: E:/Lianghuagit/xiaoshuo/recap/chapter_summaries/ch005.md | 时间：2025-12-21 14:02:23
- 状态补丁: E:/Lianghuagit/xiaoshuo/state/state_patch.json | 时间：2025-12-21 14:04:08
- 变更日志: E:/Lianghuagit/xiaoshuo/runs/2025-12-24/changelog.md | 时间：2025-12-21 14:04:46

## 推荐返工步骤（仅 FAIL 时）
1) 补齐缺失产物（chapter_plan / manuscript / summary / patch）。
2) 确保章纲推进 >=2 条 open_loops，并明确写出 id。
3) 更新 summary + state_patch，让每条计划 loop 的 id 明确出现。
4) 重跑：`python tools/continuity_checks.py --date 2025-12-24 --chapter ch005`
