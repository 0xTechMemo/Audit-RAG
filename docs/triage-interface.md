# lead-triage 接口定义

## 1. 目标

定义 audit-rag 作为审计状态化后端时的 lead triage 输入输出契约，避免把 triage 做成自由散文输出。

`triage-issue` 仍保留为不落盘的自由文本查询；active audit 默认使用 `add-lead` + `triage-lead` + `update-lead`。

## 2. 输入对象

### LeadRecord

来源：`data/provisional/contests/<contest-slug>/lead-ledger.jsonl`

关键字段：
- `id`
- `contest_slug`
- `title`
- `text`
- `status`
- `component`
- `files`
- `functions`
- `severity_guess`
- `current_blocker`
- `duplicate_check`
- `false_positive_risk`
- `validation_command`
- `poc_path`
- `final_decision`

### QueryContext

`triage-lead` / `suppress-check` 会构造检索上下文：
- `skill_name`
- `stage_name`
- `component_type`
- `ecosystem`
- `language`
- `runtime`
- `strict_runtime`
- `audit_goal`
- `desired_output_schema`
- `require_false_positive_check`

## 3. CLI 契约

```bash
python -m audit_rag.cli.main add-lead <contest-slug> <title> [--text ...] [--component ...]
python -m audit_rag.cli.main triage-lead <contest-slug> <lead-id>
python -m audit_rag.cli.main suppress-check <contest-slug> <lead-id>
python -m audit_rag.cli.main update-lead <contest-slug> <lead-id> [--status ...]
python -m audit_rag.cli.main export-contest-summary <contest-slug>
```

## 4. triage-lead 输出对象：lead-triage-scorecard-v1

保存位置：`data/provisional/contests/<contest-slug>/rag-triage/<lead-id>.json`

建议字段：
- `lead_id`
- `contest_slug`
- `root_cause_similarity`
- `pattern_similarity`
- `impact_shape`
- `probable_severity_range`
- `matching_cases`
- `matching_patterns`
- `false_positive_risks`
- `suppression_signals`
- `submission_blockers`
- `validation_recipe`
- `report_framing`
- `raw_triage`

## 5. suppress-check 输出对象：suppression-check-v1

用于判断是否应继续投入 PoC，或是否应降级/压制：
- duplicate / known finding overlap
- false-positive risk
- QA / Low downgrade signal
- missing reachability
- missing impact
- privileged-only dependency
- user-mistake-only dependency

## 6. 固定质量门槛

如果输出缺少以下任一项，视为 triage 不完整：
- 相似 case/pattern 或明确说明无强匹配
- false-positive / downgrade 风险
- submission blocker
- 下一步最小验证动作
- source trace

## 7. 边界

- RAG 相似案例不是当前项目漏洞证明。
- audit-rag 不决定最终 severity；它只提供证据和阻塞项。
- 未确认 active audit 知识不能直接进入 `data/normalized/`。
