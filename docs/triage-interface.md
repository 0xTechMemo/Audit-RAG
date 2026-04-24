# candidate-triage 接口定义

## 1. 目标

定义第一版 skill-aware triage 的输入输出契约，避免后续把 triage 做成自由散文输出。

## 2. 输入对象

### issue_text

类型：字符串

含义：
当前审计者对某个怀疑点的一句话或几句话描述。

例子：
- `withdraw updates reward debt after transfer, which may allow excess reward claims`
- `oracle timestamp is checked but heartbeat freshness is not enforced`

### code_context

类型：可选对象

建议字段：
- `repo_path`
- `file_path`
- `function_name`
- `code_snippet`
- `module_summary`

第一版可空。

### stage_context

类型：对象

建议字段：
- `skill_name`: 当前工作流名，例如 `contest-audit`
- `stage_name`: 当前阶段，第一版固定为 `candidate-triage`
- `component_type`: 例如 `reward-distribution`、`erc4626-vault`
- `audit_goal`: 例如 `judge whether this lead is submission-worthy`
- `require_false_positive_check`: 默认 `true`
- `desired_output_schema`: 默认 `candidate-triage-v1`

## 3. 检索输出对象

### positive_matches

含义：
正向相似案例与模式。

建议字段：
- `case_reports`
- `patterns`

### caution_matches

含义：
误报、降级、弱问题提示。

建议字段：
- `false_positive_cases`

### validation_support

含义：
验证建议素材。

建议字段：
- `validation_recipes`

## 4. 最终输出对象：candidate-triage-v1

建议字段：
- `query_type`
- `skill_name`
- `stage_name`
- `issue_text`
- `likely_root_cause`
- `broken_invariant`
- `attacker_profile`
- `matching_cases`
- `matching_patterns`
- `false_positive_risks`
- `probable_severity_range`
- `submission_blockers`
- `validation_gap`
- `next_validation_steps`
- `sources`
- `notes`

## 5. 字段解释

### likely_root_cause

这里写根因，不写影响。

错例：
- `attacker steals rewards`

对例：
- `reward accounting state desynchronization after balance mutation`

### broken_invariant

这里写被破坏的系统约束。

例子：
- `reward baseline must remain aligned with effective stake checkpoints`

### attacker_profile

建议值：
- `permissionless`
- `privileged-only`
- `user-mistake-dependent`
- `unclear`

### probable_severity_range

第一版建议写区间，不强行写单点。

例子：
- `medium`
- `qa-to-medium`
- `low-confidence-medium`

### submission_blockers

描述离 submission-ready 还缺什么。

例子：
- 没证明攻击者能稳定兑现影响
- 没排除补偿逻辑
- 没证明不是 privileged-only

### validation_gap

一句话描述当前最关键的证据缺口。

### sources

必须带来源对象列表，至少能追踪到 case / pattern / fp / recipe 的 ID。

## 6. 固定质量门槛

如果输出里没有下面任一项，就视为 triage 不完整：
- 根因
- false-positive 风险
- validation gap
- source trace

## 7. 第一版默认策略

- 优先输出结构化 JSON
- 正向匹配和 caution 通道分开
- 没有强证据时，不直接写 HM
- 不把 similarity 说成 exploit proof
