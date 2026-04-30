# audit-rag 产品说明（PRD）

## 1. 产品定义

audit-rag 是一个面向竞赛型智能合约审计的本地线索台账、降级判断和 PoC recipe 工作台。RAG 是知识召回层，不是项目本体。

它的目标不是替代人工审计，也不是做通用聊天式 RAG，而是作为合约审计 skill 的状态化后端，提升人工审计中的：
- lead 生命周期管理
- 模式召回速度
- 候选问题分诊效率
- duplicate / false-positive / QA downgrade 抑制能力
- PoC 验证规划能力
- 审计结束后的 provisional→normalized 知识沉淀

## 2. 核心目标

提升“有效审计时间占比”。

更具体地说，系统应该帮助你：
- 新 lead 不丢、不重复追
- 更快进入一个新的 contest repo
- 更快识别高风险模块和强候选方向
- 更快判断某个候选问题是否值得继续追
- 更快补齐验证和提交前证据
- 更少花时间在弱问题、重复问题和错误方向上

## 3. 目标用户

当前版本的核心用户只有一类：
- 单人或小规模的智能合约审计者
- 主要参与 Code4rena / Sherlock 这类比赛型审计
- 更关心 Medium / High 级别候选，而不是泛泛记录所有小问题
- 希望保留审计过程中的降级、duplicate、PoC 验证和最终决策轨迹

## 4. 非目标（v0 不做）

第一版明确不做：
- 全自动发现 submission-ready 漏洞
- 自动生成完整审计报告
- 替代人工 severity 判断
- 替代 C4 审计 skill 的流程规则和提交格式规则
- 做成多人在线协作平台
- 替代 Slither、Aderyn、Foundry、cargo test 等专业工具
- 做成泛化的 AI 聊天产品

## 5. MVP 功能范围

第一版实现策略：
- 不做“通用自由聊天式 RAG”
- 默认围绕 `contest-audit` 工作流设计
- 第一优先工作流是 `lead-ledger` + `candidate-triage` + `suppression-check`
- 输出必须感知 skill / stage context，但流程规则仍由 skill 定义

### F1. Lead Ledger

输入一个候选线索，写入 `data/provisional/contests/<contest-slug>/lead-ledger.jsonl`。

每条 lead 至少追踪：
- status
- component / files / functions
- severity_guess
- duplicate_check
- false_positive_risk
- current_blocker
- validation_command
- poc_path
- related RAG evidence
- final_decision

### F2. Triage Scorecard

对 ledger 中的 lead 运行 `triage-lead`，返回：
- root cause similarity
- pattern similarity
- impact shape
- matching cases / patterns
- false-positive risks
- suppression signals
- validation recipe
- report framing

### F3. Suppression Check

对弱问题、疑似重复、疑似 QA/Low、疑似 false-positive 的 lead 运行 `suppress-check`，优先回答：
- 是否更像 duplicate
- 是否只是 trusted-role / config / user mistake / unsupported-token
- 是否缺少当前代码 reachability 或资产影响
- 什么证据可以 revive 这个 lead

### F4. Validation Recipe Suggestion

结合历史 case / pattern / recipe，为 lead 输出验证路线，包括：
- 测试目标
- 最小状态准备
- attacker / user action
- 必要断言
- 常见失败点

### F5. Contest Summary Export

导出当前 contest 的 lead 状态总结：

```text
data/provisional/contests/<contest-slug>/contest-summary.md
```

### F6. Provisional Promotion

审计结束后，把最终确认且经过人工审校的 provisional candidate 归档到 `data/normalized/`。
默认必须 dry-run；只有显式 `--confirmed` 才能写正式 normalized。

## 5.1 Skill + audit-rag + AI 分工

固定三层分工：

- skill：定义审计阶段、质量门槛、C4 输出格式、何时调用 audit-rag
- audit-rag：记录 active lead 状态、检索 evidence、保存 scorecard、管理 provisional/normalized 数据
- AI：结合当前代码证据、skill 规则和 audit-rag evidence 输出结构化判断

固定原则：
- skill 不硬编码大量判例知识
- audit-rag 不直接拍板“漏洞已经成立”
- AI 不脱离 skill、source trace 和当前代码证据自由发挥
- active audit 未确认知识不得直接进入 normalized/eval

## 6. 输入

系统支持的主要输入：
- contest slug
- lead title / issue text
- component / files / functions
- contest 文档 / README / scope 文件
- 代码片段 / 文件路径 / 模块摘要
- 历史审计报告结构化数据
- 漏洞模式结构化数据
- false positive 结构化数据
- 组件 checklist 数据
- 个人 contest 笔记
- skill / stage context

## 7. 输出

系统输出必须满足两个要求：
1. 尽量结构化
2. 必须可追溯

主要输出类型：
- lead-ledger JSONL
- lead triage scorecard
- suppression check
- contest summary markdown
- provisional promotion manifest
- pattern / case / false-positive / recipe 检索结果

其中第一版最关键的输出契约是：
- `lead-triage-scorecard-v1`
- `suppression-check-v1`

## 8. 质量规则

1. 绝不把“模式相似”表述成“漏洞已成立”。
2. 必须区分 permissionless 可利用问题和 privileged misconfiguration。
3. 所有关键结论都要带 source trace 或当前 lead 状态记录。
4. 默认补充 false-positive / downgrade 风险。
5. 没有强证据时，严重性保持保守。
6. triage 默认必须走 false-positive 通道，不能只看正向相似案例。
7. 输出必须知道自己当前服务于哪个 skill 和哪个阶段。
8. active audit 数据先进入 provisional；最终确认后才能 promote。
9. promote-provisional 默认 dry-run，必须人工审校后再 `--confirmed`。

## 9. 成功标准

一个可用的第一版，至少应满足：
- 每个非 trivial lead 都能被记录、更新、导出总结
- 对已知案例查询时，Top-5 内能出现有用相似结果
- triage scorecard 在回放测试中经常能帮助继续追或及时止损
- 能压掉一部分弱问题 / QA-only / duplicate 路径
- 在真实 repo intake 时，你愿意打开它辅助工作
- lead ledger、triage output、summary、promotion manifest 都能稳定生成

## 10. 失败条件

如果出现以下情况，说明产品方向有问题：
- 输出像空泛安全术语堆砌
- lead 状态仍然散落在聊天和 scratch note 里
- 检索结果噪音太大
- 结果不可追溯
- false-positive / duplicate 提醒太弱
- 无法帮助你判断“继续追还是放弃”
- triage 输出脱离当前阶段，像泛化聊天回答
