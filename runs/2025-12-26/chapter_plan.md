## 章纲 - ch007

chapter_id: ch007
target_words: 3200
chapter_title: 《桥头卡口抢口径》
alt_titles: [《口信压住许文淑》, 《清沟限期逼到桥头》]

chapter_goals:
- 承接上章钩子：去桥头卡找差役线索，拿到可落地的口信或证人。
- 推进 loop_food_shortage：明确短期口粮与取水路径，形成可执行的清沟与过滤流程。
- 推进 loop_toxic_neighbor：用卡口口信与证人当众压住许文淑口径。
- 技术落地：安排简易竹筛过滤与分时取水流程，当天见效但付出时间与劳力代价。
- 家内分工：建立清沟、取水、找证人的分工与奖惩，避免内耗。
- 结尾抛出新限期风险，驱动下一章。

pov_lock: 第三人称限知（沿用风格指南）
timeline_anchor: 1100-03-15（与 state.meta.in_story_date 一致）

## Chapter Skeleton（四段骨架映射）
hook_scene_no: 1
push_scene_nos: [2, 3, 4]
escalation_scene_no: 5
ending_hook_scene_no: 6

## must_include_lines（四句必须逐字进正文，禁止标签化）
must_include_lines:
- loot_sentence: "林岑用半天搬沙清沟换到一张桥头卡口的口信条和一小把杂粮，当场塞进袖口。"
- cost_sentence: "代价是他错过井口排号的半日时段，还欠下卡口差役一个人情。"
- crowd_sentence: "围观的村民原先起哄，见差役落笔盖了手印，笑声顿住，眼神立刻变了。"
- next_step_sentence: "他决定当晚先立家中分工，明早带着口信去村委压住名册口径。"

loot_in_scene_no: 2
cost_in_scene_no: 3
crowd_in_scene_no: 5
next_step_in_scene_no: 6

## verdict_line（裁决式封口句，必须逐字进正文）
verdict_line: "里正一拍桌子：“三日清沟不到位，名册就照旧扣。”"
verdict_in_scene_no: 3

## crowd_beats（三连变脸，必须逐字进正文）
crowd_beats:
- "有人先笑他白跑一趟。"
- "差役一落笔，笑声噎住。"
- "几张脸转向许文淑压话头。"
crowd_beats_in_scene_no: 5

## 章纲爽点对齐字段
- 本章爽点类型：A 技术落地 + B 打脸交锋 + C 资源落袋
- 落袋证据句计划：林岑用半天搬沙清沟换到卡口口信条与一小把杂粮，当场入袋。
- 旁观者反应计划：围观村民先嗤笑，见差役落笔后集体噎住，眼神立刻变了。
- 开场方式：冲突开场（桥头卡口被拦+口信争执），禁止从冷/风/灰/薄被意象起笔。
- 结尾钩子类型：危机升级（口信只保到明晚，清沟验收提前）。

## Plot Spine
- premise_of_chapter: 林岑赶到桥头卡口抢口信，用劳役换到临时口径与口粮，再在村委与许文淑的围堵中稳住名册，却被更短的限期逼到下一步。

### Open Loops
- advance:
  - {id: loop_food_shortage, starting_state: progressed, action: 以搬沙清沟劳役换取卡口口信条与小把杂粮，并落实分时取水与过滤流程, new_information: 口信只能短暂稳住名册，清沟验收成为硬门槛, resulting_state: progressed, summary_evidence: "loop_food_shortage：林岑用半天搬沙换到卡口口信条和一小把杂粮，短期口粮落袋但清沟期限被压死"}
  - {id: loop_toxic_neighbor, starting_state: progressed, action: 当众用口信与证人压住许文淑口径，迫使其收声, new_information: 流言暂时被压回，但对方将借“口信时效”再翻案, resulting_state: progressed, summary_evidence: "loop_toxic_neighbor：林岑亮出口信和证人当众拆谣，围观转向压住许文淑口风"}
- new_optional: null

### Scene List
- scenes:
  - {no: 1, setting: 桥头卡口外雨棚(loc_bridge), cast: 林岑(lin_cen)、卡口差役(checkpoint_guard)、排队村民(crowd), objective: 争取进卡口说清黑沫口径, conflict: 无回执被拦且人群受流言影响不愿作证, cost: 被拖延耽误清沟与取水时辰, reveal: 卡口只认口信条或回执, escalation: 差役警告再闹就记名, anchor_phrase: 口信不到名册不稳, advances_loops: [], exit_hook: 差役丢出条件先帮卡口搬沙清沟}
  - {no: 2, setting: 卡口临检棚(loc_bridge), cast: 林岑(lin_cen)、卡口差役(checkpoint_guard)、货车脚夫(porters), objective: 以劳役换到口信条与补给, conflict: 差役不信他且要求立刻搬沙袋, cost: 体力透支并压缩回村时间, reveal: 卡口已掌握黑沫上游堵塞信息, escalation: 若不当日带回口信就作废, anchor_phrase: 卡口搬沙换一纸条, advances_loops: [loop_food_shortage], exit_hook: 拿到口信条与杂粮赶回村委}
  - {no: 3, setting: 村委/里正办公处(loc_village_committee), cast: 林岑(lin_cen)、里正(village_head)、差役(baoyi), objective: 用口信压口径稳住名册, conflict: 里正要求清沟验收与签名回执, cost: 三日清沟劳役与名册再压三日限期, reveal: 清沟验收将与名册资格绑定, escalation: 裁决落地当场成规矩, anchor_phrase: 三日清沟写在纸上, advances_loops: [loop_food_shortage], exit_hook: 林岑被迫回家立分工再去压口风}
  - {no: 4, setting: 林家租屋(loc_lin_home), cast: 林岑(lin_cen)、陈凤英(chen_fengying)、林国栋(lin_guodong), objective: 建立清沟与取水的家内分工, conflict: 家人担心劳役拖垮体力与口粮, cost: 需要放弃部分取水时段, reveal: 竹筛过滤与分时取水流程可当天见效, escalation: 分工若失败名册与口粮双崩, anchor_phrase: 家里分工先救眼前, advances_loops: [loop_food_shortage], exit_hook: 他带着口信去巷口压住流言}
  - {no: 5, setting: 许家门口巷道(loc_xu_home), cast: 林岑(lin_cen)、许文淑(xu_wenshu)、围观村民(crowd), objective: 当众用口信与证人压住许文淑口径, conflict: 许文淑质疑口信真伪并煽动围观, cost: 公开亮出口信让自己暴露在更大视线下, reveal: 差役笔迹与手印让口径转向, escalation: 许文淑被压住却记恨更深, anchor_phrase: 口信压过闲话风口, advances_loops: [loop_toxic_neighbor], exit_hook: 有人传出“口信只保到明晚”的说法}
  - {no: 6, setting: 林家租屋门口(loc_lin_home), cast: 林岑(lin_cen)、陈凤英(chen_fengying)、传话差役(messenger), objective: 接收新的时限与下一步, conflict: 口信时效缩短与清沟验收逼近, cost: 明日必须舍弃部分取水去桥头, reveal: 口信只保到明晚且验收提前, escalation: 若赶不上就失名册资格, anchor_phrase: 限期提前命在一线, advances_loops: [], exit_hook: 林岑决定明早再去桥头卡找更硬证人}

### Ending Hook
- type: crisis_escalation
- payload: 口信只保到明晚且清沟验收提前，林岑若拿不到更硬证人，名册与取水资格将一并失守。
