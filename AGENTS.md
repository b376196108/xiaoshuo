# Novel Studio — 团队章程（AGENTS）

## 工作范围（强制）
- 只允许在本仓库根目录 `xiaoshuo/` 内读写文件；严禁越界写入其它路径（包括同级目录的其它仓库）。
- 任何需要改写既有文件的操作：必须先在同目录生成 `*.bak` 备份，再进行合并/追加；不得静默覆盖。
- 全部文本文件统一 UTF-8 编码。

## 真相源与读档优先级（必须按序读取）
1) `canon/`：设定真相源。默认只允许“追加”，不允许改写既有设定；若必须改写，必须在当日 `runs/YYYY-MM-DD/qa_report.md` 中记录原因与影响面。
2) `state/`：剧情状态真相源。严禁直接修改 `state/current_state.json`；只能写 `state/state_patch.json`，并在 QA PASS 后由 `tools/merge_state_patch.py` 合并更新。
3) `recap/`：滚动摘要与章节摘要。必须控制长度与信息密度，用于跨日连续性。
4) `outline/`：全书结构、节拍与里程碑；用于约束章节规划，但不得与 `state/` 冲突。

## 角色与职责（输入/输出绑定）
> 所有角色产出必须落到指定路径；不得临时改名/改目录。

### WorldBuilder（世界构建）
- 必读输入：`inputs/project_brief.json`，`canon/premise.md`，`canon/rules/world_rules.md`，`canon/locations/locations.yaml`，`canon/factions/factions.yaml`
- 允许输出（追加为主）：`canon/rules/world_rules.md`，`canon/locations/locations.yaml`，`canon/factions/factions.yaml`，并在 `runs/YYYY-MM-DD/changelog.md` 记录变更摘要

### CharacterDesigner（角色设计）
- 必读输入：`inputs/project_brief.json`，`canon/characters/characters.yaml`，`state/current_state.json`
- 允许输出（追加为主）：`canon/characters/characters.yaml`，并在 `runs/YYYY-MM-DD/changelog.md` 记录变更摘要

### PlotArchitect（剧情架构）
- 必读输入：`outline/master_outline.md`，`recap/rolling_recap.md`，`state/current_state.json`（重点：`open_loops`）
- 输出：为当日章节提供结构约束与回收窗口建议，写入 `runs/YYYY-MM-DD/chapter_plan.md`

### ChapterPlanner（章节规划）
- 必读输入：`runs/YYYY-MM-DD/brief.md`，`runs/YYYY-MM-DD/context_pack.md`，`state/current_state.json`
- 输出：`runs/YYYY-MM-DD/chapter_plan.md`（必须显式标注推进哪些 `open_loops`）

### Drafter（写作）
- 必读输入：`runs/YYYY-MM-DD/chapter_plan.md`，`runs/YYYY-MM-DD/context_pack.md`，`canon/style/style_guide.md`
- 输出：`manuscript/chNNN.md`（正文只写小说内容；不得出现任何“系统提示/AI/模型/作者自述”等痕迹）

### LineEditor（行文编辑）
- 必读输入：`manuscript/chNNN.md`，`canon/style/style_guide.md`
- 输出：覆盖更新 `manuscript/chNNN.md`（编辑后的正文），并在 `runs/YYYY-MM-DD/changelog.md` 记录编辑要点

### ContinuityQA（连续性与规则 QA）
- 必读输入：`manuscript/chNNN.md`，`recap/chapter_summaries/chNNN.md`，`state/current_state.json`，`state/state_patch.json`，`canon/**`
- 输出：`runs/YYYY-MM-DD/qa_report.md`（第一行必须是 `QA_RESULT: PASS` 或 `QA_RESULT: FAIL`）

### Archivist（归档与状态补丁）
- 必读输入：`manuscript/chNNN.md`，`runs/YYYY-MM-DD/chapter_plan.md`
- 输出：
  - `recap/chapter_summaries/chNNN.md`
  - `recap/rolling_recap.md`
  - `state/state_patch.json`（只写变更字段；不得直接改 `state/current_state.json`）
  - `runs/YYYY-MM-DD/changelog.md`

## 强制流水线顺序（不得跳过）
`CreateRun -> BuildContext -> World/Character -> Outline/Plan -> Draft -> Edit -> QA -> Archive -> Patch -> Merge(仅PASS)`

## 禁止规则（硬约束）
- 正文与摘要中不得出现“系统提示/AI/模型/作者自述/提示词/工具链”等痕迹。
- 不得随意改人称/视角/时态；若必须调整（例如项目设定变更），必须先更新 `canon/style/style_guide.md` 并在 QA 报告中记录。
- 不得绕开 `state/state_patch.json` 直接编辑 `state/current_state.json`。
- 不得引入与 `canon/` 相冲突的新设定；如需要新增设定，默认只能追加，并在 `runs/YYYY-MM-DD/changelog.md` 记录。

## 每章硬性要求
- 承上启下：至少推进 2 个 `open_loops`；最多新增 1 个 `open_loop`（新增必须在 `state/state_patch.json` 与摘要中体现）。
- 结尾必须留钩子：`新信息/误判/危机升级/目标转向` 四选一，且要与 `open_loops` 或主线冲突相连。

## 每次运行必产物清单（路径严格一致）
- `runs/YYYY-MM-DD/brief.md`
- `runs/YYYY-MM-DD/context_pack.md`
- `runs/YYYY-MM-DD/chapter_plan.md`
- `manuscript/chNNN.md`
- `recap/chapter_summaries/chNNN.md`
- `recap/rolling_recap.md`
- `state/state_patch.json`
- `runs/YYYY-MM-DD/qa_report.md`（第一行必须：`QA_RESULT: PASS` 或 `QA_RESULT: FAIL`）
- `runs/YYYY-MM-DD/changelog.md`

