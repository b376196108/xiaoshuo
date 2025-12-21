# 章纲 - ch006

chapter_id: ch006
target_words: 3200
chapter_title: 《当众拆谣压名册》
alt_titles: [《谣口当场被封住》, 《里正加压我反咬》]
chapter_goals:
- 承接上章黑沫疑云，顶住公开刁难，稳住名册与口粮的基本盘
- 推进 loop_food_shortage：明确短期取水与口粮的可执行路径，并拿到当天可落袋的小资源
- 推进 loop_toxic_neighbor：当众拆谣、锁定口径与人证，削弱许文淑的压迫
- 种田爽点落地：用可落地的净水与取水流程立住口碑，当天见效但代价上升
- 结尾留钩子：名册被里正加压，目标转向寻找更硬的证据与证人

pov_lock: 第三人称限知（state.meta.pov 未设置，沿用风格指南）
timeline_anchor: 1100-03-15（与 state.meta.in_story_date 一致）
hook_scene_no: 1
push_scene_nos: [2, 3, 4]
escalation_scene_no: 5
ending_hook_scene_no: 6

must_include_lines:
- 落袋证据句：林岑以查清黑沫源头作口径，换得一小把糙米与一张临时取水木牌，当场入袋。
- 代价句：代价是三日清沟役期，并背下全村目光。
- 旁观者反应句：围观村民先哄笑，听到里正点头后，笑声像被人掐断，集体噎住，眼神立刻变了——从看戏，变成敬畏。
- 下一步指向句：他决定天一亮就去桥头卡找差役线索，名册与水源都得有个说法。

## 章纲爽点对齐字段
- 本章爽点类型：A 技术落地 + B 打脸交锋 + C 资源落袋
- 落袋证据句计划：林岑以查清黑沫源头作口径，换得一小把糙米与一张临时取水木牌，当场入袋。
- 旁观者反应计划：围观村民先哄笑，听到里正点头后，笑声像被人掐断，集体噎住，眼神立刻变了——从看戏，变成敬畏。
- 开场方式：冲突开场（巷口当众拆谣+名册质疑），禁止从冷/风/灰/薄被意象起笔。
- 结尾钩子类型：目标转向（被迫转向去桥头卡找证人线索）。

## Plot Spine
- premise_of_chapter: 主角当众拆谣、以可落地的净水流程稳住口碑，换到短期资源，却因里正加压而被迫转向寻找更硬证据。

## Open Loops
- advance:
  - {id: loop_food_shortage, starting_state: progressed, action: 追查黑沫源头并公开口径，换取临时取水木牌与小把糙米以稳住当日口粮, new_information: 水源风险触发新的管控与劳役，短期资源必须用证据与劳力换取, resulting_state: progressed, summary_evidence: "loop_food_shortage：林岑以查清黑沫源头作口径，换得一小把糙米与一张临时取水木牌，当场入袋并背上三日清沟役期"}
  - {id: loop_toxic_neighbor, starting_state: progressed, action: 许文淑当众再挑衅，林岑用人证与实情回击并当场封住其口径, new_information: 流言已与名册压力绑定，里正借机加压, resulting_state: progressed, summary_evidence: "loop_toxic_neighbor：许文淑公开挑衅并扩散口径，林岑当众拆谣并锁定证人，冲突进一步公开化"}
- new_optional: null

## Scene List
- scenes:
  - {no: 1, setting: 许家门口巷道(loc_xu_home), cast: 林岑、许文淑、围观村民, objective: 当众制止“占名额”流言, conflict: 许文淑借黑沫挑唆全村围堵, cost: 名声与名册资格被推到风口, reveal: 流言已指向名册清退, escalation: 村民要求去村委当面说清, anchor_phrase: 污水锅盖先扣谁头, advances_loops: [loop_toxic_neighbor], exit_hook: 林岑被迫去村委对质}
  - {no: 2, setting: 村委/里正办公处(loc_village_committee), cast: 林岑、里正、差役, objective: 争取澄清口径与取水安排, conflict: 里正只认回执与人证，口径随人变, cost: 需承诺额外劳役换取说法机会, reveal: 里正将名册提前复核, escalation: 名册压力被借机加码, anchor_phrase: 口径三变，只认证人, advances_loops: [loop_toxic_neighbor], exit_hook: 要求林岑拿出黑沫源头口径}
  - {no: 3, setting: 排水沟上游(loc_river_canal), cast: 林岑、王老拐, objective: 查清黑沫来源并取证, conflict: 上游泥水混杂且人多阻拦, cost: 体力消耗与错过排号风险, reveal: 黑沫来自上游烂草堆与死物堆积, escalation: 若不处理将被全村指为“散毒源”, anchor_phrase: 只能用速度换机会, advances_loops: [loop_food_shortage], exit_hook: 林岑带着口径回村}
  - {no: 4, setting: 取水点/井口(loc_river_canal), cast: 林岑、许文淑、围观村民, objective: 当众拆谣并稳住取水名额, conflict: 许文淑继续煽动，村民质疑林岑, cost: 公开对质导致后续被盯上, reveal: 林岑展示口径与人证，里正同意临时取水木牌, escalation: 许文淑当场被封口但怨气更深, anchor_phrase: 当众拆谣，干脆利落, advances_loops: [loop_food_shortage, loop_toxic_neighbor], exit_hook: 临时木牌到手但劳役条件加重}
  - {no: 5, setting: 村委/里正办公处(loc_village_committee), cast: 林岑、里正、差役, objective: 把口径落成书面与工役安排, conflict: 里正借机要求三日清沟并提前复核名册, cost: 时间与劳力被锁死，回执线索更难追, reveal: 名册压限期与工役绑定, escalation: 若不按期完成将失名册资格, anchor_phrase: 名册再压三日限期, advances_loops: [loop_toxic_neighbor], exit_hook: 目标被迫转向找证人线索}
  - {no: 6, setting: 林家租屋(loc_lin_home), cast: 林岑、陈凤英、林国柱, objective: 定下下一步行动, conflict: 家人担心劳役与名册双压, cost: 放弃部分取水时间去找证人, reveal: 只能去桥头卡寻差役线索, escalation: 明早必须出门抢先一步, anchor_phrase: 先去桥头把口再找证人, advances_loops: [], exit_hook: 林岑决定天一亮去桥头}

## Ending Hook
- type: goal_shift
- payload: 名册被里正加压并限期清沟，林岑被迫转向桥头卡寻找差役与回执线索，否则取水与名册双失。
