# 章纲 - ch003

- chapter_id: ch003
- target_words: 3200
- chapter_title: 《鸡鸣前回执不见》
- alt_titles: [《鸡鸣前抢名额》,《回执在手也难保》]
- chapter_goals:
  - 承接上章钩子：点卯提前到鸡鸣前，明确当日点卯流程与名册口径
  - 推进 loop_food_shortage：以回执与劳役安排争取短期缓冲或换粮路径，明确地点与代价
  - 推进 loop_toxic_neighbor：当众对质并争取里正表态，留下流言扩散证据
  - 种田爽点落地：先汤后粮+分段闷煮省柴省粮，当天见效让晚饭更顶饱
  - 磨难/反转升级：里正偏袒强户与邻居拖延叠加，关键证据被人拿走
- pov_lock: 第三人称限知（主角：林岑）
- timeline_anchor: 1100-03-15 鸡鸣前至清晨（点卯提前当日）

## 本章要点
- 冲突：点卯提前与里正偏袒叠加，名册资格随时被卡
- 爽点：用可落地的省柴省粮流程让当晚更顶饱，但付出时间与暴露代价
- 反转：以为回执稳了名额，关键证据却被人拿走
- 结尾钩子：误判导致名额风险陡增，必须立刻补救

## Open Loops 推进
- loop_food_shortage：争取点卯缓冲并问清后续换粮时段/条件，短期口粮路径更具体但代价加重。
- loop_toxic_neighbor：当众对质并争取里正表态，留下她拖延与散布流言的证据，矛盾升级未解。

## Open Loops
- advance:
  - id: loop_food_shortage
    starting_state: 短期口粮靠回执与劳力债换得少量粗粮，仍无稳定来源
    action: 点卯前带回执去村委/里正处争取缓冲与下一次换粮时段，必要时加码劳力或柴火
    new_information: 点卯名单鸡鸣前锁死，缓冲只认可回执与里正口头认定
    resulting_state: progressed
    summary_evidence: 里正明确换粮与点卯口径及代价，短期路径可执行但成本上升
  - id: loop_toxic_neighbor
    starting_state: 许文淑盯点卯迟到，以流言威胁名额
    action: 当众对质并要求里正在场表态，留下围观证人与口风
    new_information: 她借强势户与流言拖延对手，试图制造迟到失格
    resulting_state: active
    summary_evidence: 巷道或村委对峙并留下证人或里正口头表态
- new_optional: null

## Scene List
- scenes:
  - {no: 1, setting: "林家屋内(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、林国柱(lin_guozhu)、杜桂兰(du_guilan)", objective: "在鸡鸣前决定点卯人选并整理回执", conflict: "父亲坚持出面但体力不稳，时间极短", reveal: "点卯提前到鸡鸣前且只认回执口径", escalation: "若迟到全家失去赈粮资格", exit_hook: "林岑带回执急赴村委"}
  - {no: 2, setting: "巷道口/许家门口(loc_xu_home)", cast: "林岑(lin_cen)、许文淑(xu_wenshu)、围观村人", objective: "不被拖延地赶往点卯处", conflict: "许文淑当众挖苦并借流言阻拦", reveal: "强势户已打过招呼，名册口风可能变化", escalation: "她要求查看回执并拖住脚步", exit_hook: "林岑决定去村委争里正表态"}
  - {no: 3, setting: "村委/里正办公室(loc_village_committee)", cast: "林岑(lin_cen)、叶守正(ye_shouzheng)、差役(he_kaijun)、排队村民", objective: "争取点卯缓冲与劳力保留", conflict: "里正偏袒强户，排队与口径挤压", reveal: "点卯名单鸡鸣前锁死，缓冲只认回执与里正口头认定", escalation: "林岑加码劳力/柴火换取一次缓冲或明确时段", exit_hook: "他以为回执在手能保名额"}
  - {no: 4, setting: "林家灶间(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)、林小棠(lin_xiaotang)", objective: "用更省柴的做法让当晚更顶饱", conflict: "粗粮难煮、柴火更紧", reveal: "先汤后粮+分段闷煮能更稠更省柴", escalation: "耗时加倍、灶烟外泄暴露风险", exit_hook: "门外脚步与目光靠近"}
  - {no: 5, setting: "村口巷道(loc_village_lane)", cast: "林岑(lin_cen)、许文淑(xu_wenshu)", objective: "护住回执并压住流言", conflict: "许文淑逼他当众亮回执并拖延", reveal: "她盯准“迟到就失格”的口风", escalation: "争执中回执滑落或被人顺走", exit_hook: "林岑未立刻察觉"}
  - {no: 6, setting: "林家门口(loc_lin_home)", cast: "林岑(lin_cen)、陈淑英(chen_shuying)", objective: "确认回执与点卯准备", conflict: "回执不见，点卯迫在鸡鸣前", reveal: "没有回执就可能被名册划掉", escalation: "必须立刻找回或补证", exit_hook: "关键证据失手，名额岌岌可危"}

## Ending Hook
- type: misjudgment
- payload: 林岑以为回执在手就能保住名额，回家才发现回执不见，鸡鸣前点卯迫在眉睫。