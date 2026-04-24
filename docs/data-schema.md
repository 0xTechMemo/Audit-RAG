# 数据结构说明（data-schema）

本文档定义 audit-rag 的第一版结构化知识对象。

## 设计原则

1. 以 finding 为粒度，而不是以整篇报告为粒度。
2. 把“抽象模式”和“具体案例”分开存储。
3. 把 false positive / 降级知识当成一等公民。
4. 数据结构要足够支撑检索、过滤、重排和评测。

## 1. case_report

表示一条具体历史问题，来源可以是：
- C4 报告
- Sherlock 报告
- 公开审计报告
- exploit/postmortem

核心必填字段：
- `id`
- `source_type`
- `protocol_name`
- `finding_title`
- `summary`
- `root_cause`
- `severity`
- `tags`

重要可选字段：
- `component_types`
- `broken_invariants`
- `attack_preconditions`
- `attacker_capability`
- `impact`
- `why_not_higher`
- `why_not_lower`
- `validation_status`
- `common_false_positive_angles`

作用：
- 相似案例召回
- 严重性校准
- exploit path 对照
- source-backed 输出拼装

## 2. vulnerability_pattern

表示一个抽象漏洞模式，不依赖具体协议。

核心必填字段：
- `id`
- `name`
- `category`
- `description`
- `severity_baseline`
- `tags`

重要可选字段：
- `component_types`
- `broken_invariants`
- `common_triggers`
- `preconditions`
- `typical_impact`
- `common_false_positives`
- `validation_methods`
- `related_case_ids`

作用：
- 漏洞模式召回
- checklist 扩展
- 验证建议生成

## 3. false_positive_case

表示一种常见误判、弱问题或典型降级案例。

核心必填字段：
- `id`
- `issue_claim`
- `why_not_valid`
- `classification`
- `tags`

重要可选字段：
- `why_it_looked_bad`
- `downgrade_reason`
- `trust_assumption`
- `when_it_could_be_real`
- `source_url`

作用：
- triage 降噪
- QA/Low 校准
- submission 前风险提醒

## 4. low_non_critical_case

表示公开报告里的 Low / Non-critical / QA 问题。

这些记录必须和 Medium/High 的 `case_report` 分开存储，默认放在：
- `data/normalized/low_non_critical_cases/`

核心必填字段：
- `id`
- `source_type`
- `protocol_name`
- `issue_title`
- `classification`
- `summary`
- `why_not_medium_or_high`
- `tags`

重要可选字段：
- `component_types`
- `root_cause`
- `operational_risk`
- `affected_functions`
- `recommended_mitigation`
- `when_it_could_escalate`
- `retrieval_channel`

作用：
- QA/Low 知识沉淀
- 严重性降级校准
- 配置、可用性、运维风险检索
- 避免把弱问题混入 HM 候选样本池

质量要求：
- `classification` 使用 `low`、`non-critical` 或 `qa`
- 默认 `retrieval_channel` 使用 `low_non_critical_caution`
- 不要和 `case_reports/` 下的 Medium/High 样本混排

## 5. component_checklist

表示某一类协议组件的审计清单。

核心必填字段：
- `id`
- `component_type`
- `core_invariants`
- `check_items`
- `tags`

重要可选字段：
- `trust_boundaries`
- `common_bug_classes`
- `test_ideas`
- `related_pattern_ids`

作用：
- 仓库 intake
- 模块审计辅助
- 审计计划组织

## 6. validation_recipe

表示某类问题常见的验证方式。

建议字段：
- `id`
- `pattern_id`
- `test_style`
- `goal`
- `setup_requirements`
- `minimal_state`
- `attacker_actions`
- `assertions`
- `common_failures`
- `notes`

作用：
- 验证路线设计
- 单测 / PoC 思路草拟

## 7. contest_note

表示单场比赛的本地研究记录，不应混入全局模式库。

建议字段：
- `id`
- `contest_name`
- `repo_url`
- `commit`
- `scope_files`
- `trusted_roles`
- `known_issues`
- `architecture_summary`
- `hotspot_modules`
- `candidate_leads`
- `dead_ends`

作用：
- 单场比赛连续性记录
- 热点排序辅助
- 本地研究可追溯

## 最低标签要求

每条较强的 case record 至少应包含：
- 1 个根因标签
- 1 个组件标签
- 1 个影响标签

## 验证纪律

如果来源本身没有支撑 permissionless exploit path，或者没有具体影响证据，就不要把这条记录当作强 HM 指导样本。
