# 手动 Codex 指令 - 2025-12-22 - ch003

> 提示：未检测到 `codex` CLI，本次无法自动生成产物。
> 请使用 VSCode Codex 扩展并按顺序执行以下步骤。
> 输出路径必须完全一致（不要改名或移动）。
> 编码强提醒：所有新建/覆盖的 .md/.json 文件必须保存为 UTF-8；若出现大量问号（????），说明编码错误或占位符，必须重做。
> 硬规则：正文（不含标题与空白）必须 >=3000 字符（建议 3200+）；不足返工；禁止灌水凑字。
> 只允许写入指定文件，禁止修改其他任何文件；如需修改其他文件必须先停止并说明原因。
> 遇到缺失文件或读取失败，请先停止并报告，不要擅自补写或猜测。
> 禁止占位符：不得出现 "???" / "TBD" / "待补全" / "TODO"。

## 运行目标

- chapter_id: `ch003`
- target_words: `3200`
- total_chapters: 80

## 需要产出（路径）
- `runs/2025-12-22/chapter_plan.md`
- `manuscript/ch003.md`
- `recap/chapter_summaries/ch003.md`
- `recap/rolling_recap.md`
- `state/state_patch.json`（JSON 对象，仅 delta；必须包含 `meta.current_chapter: "ch003"`）
- `runs/2025-12-22/changelog.md`
- `runs/2025-12-22/qa_report.md`（由 Step 4 生成）

## 操作总则（必须遵守）

- 全中文输出；严格遵守 `canon/style/style_guide.md`。
- 仅写入指定文件；禁止改动其他文件、路径与文件名。
- 不得生成任何额外正文样稿或新文件；如需修改其他文件请先停止说明原因。
- 不得出现 AI/系统/提示词痕迹；不得使用 "???" / "TBD" / "待补全" / "TODO" 作为占位。

## 步骤 1 - 章纲

提供以下文件作为上下文：
- `AGENTS.md`
- `runs/2025-12-22/brief.md`
- `runs/2025-12-22/context_pack.md`
- `prompts/roles/plot_architect.md`
- `prompts/roles/chapter_planner.md`

写入：
- `runs/2025-12-22/chapter_plan.md`

要求：
- chapter_plan.md 必须包含字段：chapter_title: 《……》（最终标题，禁止占位符）。
- 可选字段：alt_titles: [《…》,《…》]（2-3个候选）。

## 步骤 2 - 正文 + 行文润色

提供以下文件作为上下文：
- `runs/2025-12-22/chapter_plan.md`
- `runs/2025-12-22/context_pack.md`
- `canon/style/style_guide.md`
- `prompts/roles/drafter.md`
- `prompts/roles/line_editor.md`

写入：
- `manuscript/ch003.md`（第一行必须是 `# ch003`；第二行必须是 `## 《标题》`；标题必须与 chapter_plan.md 的 chapter_title 完全一致）

## 步骤 3 - 摘要 + 滚动摘要 + 状态补丁（Archivist）

提供以下文件作为上下文：
- `manuscript/ch003.md`
- `runs/2025-12-22/chapter_plan.md`
- `state/current_state.json`
- `prompts/roles/archivist.md`

写入：
- `recap/chapter_summaries/ch003.md`
- `recap/rolling_recap.md`
- `state/state_patch.json`（JSON 对象，仅 delta；`meta.current_chapter` 必须是字符串 "ch003"）
- `runs/2025-12-22/changelog.md`

要求：
- recap/chapter_summaries/ch003.md 第一行必须是 "# ch003｜《本章标题》"，标题必须与 chapter_plan.md 的 chapter_title 完全一致。

## 可复制粘贴提示词块（用于 VSCode Codex）
【复制粘贴块 1：第1步 章纲提示词】
```
请只执行【第1步：章纲】。

必须先阅读这些文件作为上下文：
- AGENTS.md
- runs/2025-12-22/brief.md
- runs/2025-12-22/context_pack.md
- prompts/roles/plot_architect.md
- prompts/roles/chapter_planner.md

然后写出并仅写入：
- runs/2025-12-22/chapter_plan.md

要求：
- 全中文输出
- 只写指定文件，禁止修改其他任何文件
- chapter_plan.md 必须包含字段：chapter_title: 《……》（最终标题，禁止占位符）
- 可选字段：alt_titles: [《…》,《…》]（2-3个候选）
- 禁止使用 "???" / "TBD" / "待补全" / "TODO" 占位符
- 若缺失上下文文件，先停止并报告缺失
```

【复制粘贴块 2：第2步 正文+润色提示词】
```
请只执行【第2步：正文+润色】。

必须先阅读这些文件作为上下文：
- runs/2025-12-22/chapter_plan.md
- runs/2025-12-22/context_pack.md
- canon/style/style_guide.md
- prompts/roles/drafter.md
- prompts/roles/line_editor.md

然后写出并仅写入：
- manuscript/ch003.md

硬规则：
- 第一行必须是：# ch003
- 第二行必须是：## 《标题》（标题来自 chapter_plan.md 的 chapter_title）
- 标题必须与 chapter_plan.md 的 chapter_title 完全一致
- 正文（不含标题与空白）>=3000 字符，建议 3200–3800
- 禁止灌水凑字：重复句、流水账旁白、无意义心理独白、长篇科普说明书
- 必须包含：行动推进 + 对话交锋 + 场景细节 + 阻碍升级 + 小爽点落地 + 结尾钩子
- 语言必须中文，严格遵守 canon/style/style_guide.md
- 禁止使用 "???" / "TBD" / "待补全" / "TODO" 占位符
- 只写指定文件，禁止修改其他任何文件；若缺失文件先停止并报告
```

【复制粘贴块 3：第3步 归档同步提示词】
```
请只执行【第3步：归档同步】（不要改正文）。

必须先阅读这些文件作为上下文：
- manuscript/ch003.md
- runs/2025-12-22/chapter_plan.md
- state/current_state.json
- prompts/roles/archivist.md

然后写出/更新并仅写入：
- recap/chapter_summaries/ch003.md
- recap/rolling_recap.md
- state/state_patch.json
- runs/2025-12-22/changelog.md

硬规则：
- 全中文输出；只写指定文件，禁止修改其他任何文件
- recap/chapter_summaries/ch003.md 第一行必须是 # ch003｜《本章标题》，标题必须与 chapter_plan.md 的 chapter_title 完全一致
- state/state_patch.json 必须是 JSON 对象、delta only，不得复制整份 current_state
- 必须包含 meta.current_chapter: "ch003"
- 只能更新本章确实变化的人物状态/资源/地点/关系/knowledge_flags
- open_loops 至少推进 2 条（若无法推进，必须说明原因）
- 归档内容不得引入 manuscript/ch003.md 未发生的新事实
- changelog 必须追加 synced_at 时间戳
- 禁止使用 "???" / "TBD" / "待补全" / "TODO" 占位符
- 若缺失文件或读取失败，先停止并报告
```

## 步骤 4 - QA + 合并（仅 PASS）
在仓库根目录执行：
```bash
python tools/continuity_checks.py --date 2025-12-22 --chapter ch003
```

该命令会生成/更新 `runs/2025-12-22/qa_report.md`（首行 `QA_RESULT: PASS/FAIL`）。
若 `QA_RESULT: PASS`，再执行：
```bash
python tools/merge_state_patch.py --date 2025-12-22
```

## 常见失败与处理
- BodyTooShort：只扩写 `manuscript/ch003.md` 正文（不改其他文件）→重跑 Step3 →再跑 QA。
- OutOfSync：查看 `runs/2025-12-22/resync_instructions.md` 并按其指引执行，然后重跑 QA。
- TitleMissingOrInvalid：修正正文标题为 `# ch003` + `## 《标题》`，标题来自 chapter_plan.md 的 chapter_title →重跑 Step3 →再跑 QA。

