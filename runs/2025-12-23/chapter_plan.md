# 章纲 - ch004

- chapter_id: ch004
- target_words: 3200
- chapter_title: 《回执失手抢种子》
- alt_titles: [《鸡鸣前求口簿》,《换种路被截》]
- chapter_goals:
  - 承接上章钩子：回执失落后争取鸡鸣前的临时口簿/证人认可，保住点卯资格
  - 推进 loop_food_shortage：为春播与长期口粮寻找种子与农具的可行路径（劳力/修补换种）
  - 推进 loop_toxic_neighbor：与许文淑正面对峙并留下拖延/截胡证据
  - 种田爽点落地：用筛选/漂洗/风选等低成本方法当天分出一把可播种子
  - 磨难/反转升级：强势户与邻居联手卡口，名册口径再收紧
- pov_lock: 第三人称限知（主角：林岑）
- timeline_anchor: 1100-03-15 鸡鸣前至午后（回执失落当日）

## Open Loops
- advance:
  - id: loop_food_shortage
    starting_state: 短期口粮靠回执与劳力债换得少量粗粮，长期来源不明
    action: 鸡鸣前拿到临时口簿并去粮铺/集市以修补与劳力换取少量种子或工具借用
    new_information: 种子与农具被强势户优先拿走，弱户只能以劳力换取零散份额
    resulting_state: progressed
    summary_evidence: 拿到可播种子的一小包与明确的换种条件
  - id: loop_toxic_neighbor
    starting_state: 许文淑以流言拖延并放大迟到风险
    action: 当众追问回执去向并要求邻里作证，揭穿她的拖延与截胡意图
    new_information: 她借强势户口风施压，试图把名额与种子一起卡住
    resulting_state: active
    summary_evidence: 巷口对峙与证人记录她的阻拦与放话
- new_optional: null

## Scene List
- scenes:
  - {no: 1, setting: "林家屋内(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、林国柱(lin_guozhu)、杜桂兰(du_guilan)", objective: "鸡鸣前确认回执去向并决定先保点卯", conflict: "回执失落与时间极短", reveal: "回执可能掉在巷口或被人捡走", escalation: "必须先去村委争口簿", exit_hook: "林岑带着证人线索冲向村委"}
  - {no: 2, setting: "村委/里正办公室(loc_village_committee)", cast: "林岑(lin_cen)、叶守正(ye_shouzheng)、差役(he_kaijun)、排队村民", objective: "无回执争取临时口簿", conflict: "规则死、强势户先占位", reveal: "临时口簿需证人+指印，且限时", escalation: "追加劳力/柴火作为代价", exit_hook: "拿到限时口头认可，仍需回执补证"}
  - {no: 3, setting: "巷道口/许家门口(loc_xu_home)", cast: "林岑(lin_cen)、许文淑(xu_wenshu)、邻里", objective: "追问回执线索并留证", conflict: "许文淑抵赖并拖延", reveal: "有人见她捡起纸片或与强势户低语", escalation: "对峙升级、她放话要卡名额", exit_hook: "林岑记下证人名单"}
  - {no: 4, setting: "集市/粮铺(loc_market)", cast: "林岑(lin_cen)、周启明(zhou_qiming)、伙计", objective: "换取种子与工具", conflict: "粮铺抬价、赊账被拒", reveal: "可用修补/劳力换少量种子", escalation: "只能先干活换一小包", exit_hook: "林岑提出当天筛选旧种换折价"}
  - {no: 5, setting: "林家灶间/院角(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、林小棠(lin_xiaotang)", objective: "当天筛出可播种子并安排劳力", conflict: "水少盐少、烟火易暴露", reveal: "用清水漂选与风选可分出饱满籽", escalation: "灶烟引来邻里侧目", exit_hook: "门外传来名册口风变动的消息"}
  - {no: 6, setting: "村口公告处(loc_village_lane)", cast: "林岑(lin_cen)、差役(he_kaijun)、围观村人", objective: "确认名册与点卯口径", conflict: "名单贴出“补证”红印", reveal: "回执是唯一补证凭据", escalation: "鸡鸣前不补证将被除名", exit_hook: "名额危机升级"}

## Ending Hook
- type: crisis_escalation
- payload: 名册贴出“补证”红印，鸡鸣前必须交回执，否则直接除名。