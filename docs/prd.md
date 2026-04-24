# audit-rag 产品说明（PRD）

## 1. 产品定义

audit-rag 是一个面向竞赛型智能合约审计的本地 RAG 工作台。

它的目标不是替代人工审计，而是提升人工审计中的：
- 模式召回速度
- 热点定位速度
- 候选问题分诊效率
- 误报抑制能力
- 验证规划能力

## 2. 核心目标

提升“有效审计时间占比”。

更具体地说，系统应该帮助你：
- 更快进入一个新的 contest repo
- 更快识别高风险模块
- 更快判断某个候选问题是否值得继续追
- 更快补齐验证和提交前证据
- 更少花时间在弱问题和错误方向上

## 3. 目标用户

当前版本的核心用户只有一类：
- 单人或小规模的智能合约审计者
- 主要参与 Code4rena / Sherlock 这类比赛型审计
- 更关心 Medium / High 级别候选，而不是泛泛记录所有小问题

## 4. 非目标（v0 不做）

第一版明确不做：
- 全自动发现 submission-ready 漏洞
- 自动生成完整审计报告
- 替代人工 severity 判断
- 做成多人在线协作平台
- 替代 Slither、Aderyn、Foundry 等专业工具
- 做成泛化的 AI 聊天产品

## 5. MVP 功能范围

第一版实现策略补充：
- 不做“通用自由聊天式 RAG”
- 默认围绕 `contest-audit` 工作流设计
- 第一优先阶段是 `candidate-triage`
- triage 输出必须感知 skill / stage context

### F1. 模式召回（Pattern Recall）
输入一个模块、函数摘要或代码片段，返回相关漏洞模式和相似历史案例。

### F2. 组件审计清单（Component Checklist Recall）
输入组件类型，返回该组件常见 invariant、边界、风险点和测试思路。

### F3. 候选问题分诊（Candidate Issue Triage）
输入一个怀疑点，返回：
- 可能根因
- 相似案例
- 可能严重性范围
- 还缺什么证据
- 常见误判风险

### F4. 误报/降级提醒（False Positive Warning）
对容易被误判成 HM/M 的方向，主动给出降级原因和风险提示。

### F5. 验证方案建议（Validation Recipe Suggestion）
给出该类问题适合如何验证，包括：
- 测试思路
- 最小状态准备
- 断言建议
- 常见失败点

### F6. 仓库热点总结（Repo Hotspot Summary）
对 contest repo 做初步热点排序，指导优先审计顺序。

## 5.1 Skill + RAG + AI 分工

第一版明确采用三层分工：

- skill：定义审计阶段、默认查询、质量门槛、输出契约
- RAG：提供 case / pattern / false positive / validation recipe
- AI：结合当前 issue 和检索证据输出结构化判断

固定原则：
- skill 不硬编码大量判例知识
- RAG 不直接拍板“漏洞已经成立”
- AI 不脱离 skill 和 source trace 自由发挥

## 6. 输入

系统支持的主要输入：
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
- 模式召回结果
- 候选问题分诊结果
- 组件审计包
- 仓库热点结果
- 验证支持结果

其中第一版最关键的输出契约是：
- `candidate-triage-v1`

## 8. 质量规则

1. 绝不把“模式相似”表述成“漏洞已成立”。
2. 必须区分 permissionless 可利用问题和 privileged misconfiguration。
3. 所有关键结论都要带 source trace。
4. 默认补充 false-positive / downgrade 风险。
5. 没有强证据时，严重性保持保守。
6. triage 默认必须走 false-positive 通道，不能只看正向相似案例。
7. 输出必须知道自己当前服务于哪个 skill 和哪个阶段。

## 9. 成功标准

一个可用的第一版，至少应满足：
- 对已知案例查询时，Top-5 内能出现有用相似结果
- triage 输出在回放测试中经常能帮助继续追或及时止损
- 能压掉一部分弱问题 / QA-only 路径
- 在真实 repo intake 时，你愿意打开它辅助工作
- 第一版 skill-aware triage 能稳定返回固定 schema

## 10. 失败条件

如果出现以下情况，说明产品方向有问题：
- 输出像空泛安全术语堆砌
- 检索结果噪音太大
- 结果不可追溯
- false-positive 提醒太弱
- 无法帮助你判断“继续追还是放弃”
- triage 输出脱离当前阶段，像泛化聊天回答
