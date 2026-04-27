# 数据沉淀质量门槛

这份文档约束 `data/normalized/` 里的审计案例如何进入 RAG。目标不是把公开报告机械切碎，而是沉淀可跨协议检索的漏洞模式、反例和验证线索。

## 1. High / Medium case 的必填语义质量

`data/normalized/case_reports/*.json` 只用于主召回流，优先服务竞赛审计里的 Medium / High 发现。

### root_cause

必须是一句可跨协议复用的抽象根因，不要复制 summary。

好的写法：

- `auth-bypass via missing owner check in ERC4626 _withdraw, allowing approval-based withdrawal to bypass FULL_RESTRICTED enforcement`
- `buffer accounting desync on cancelWithdrawal: hypeBuffer is deducted when queueing a withdrawal but not restored or bridged correctly when the withdrawal is cancelled`
- `withdrawal confirmation uses a queued snapshot hypeAmount instead of recalculating claim value with the current exchange rate after slashing`

坏的写法：

- `Report-described logic/accounting flaw: ...`
- 直接复制 finding description 第一段
- 只写 `missing validation` 但不说明缺的是哪个状态转换 / 角色 / 资产域

### broken_invariants

必须写具体协议场景下被破坏的约束。不要写模板句。

好的写法：

- `a FULL_RESTRICTED staker must not be able to move value out through either direct calls or allowance-mediated ERC4626 withdraw/redeem paths`
- `HYPE removed from hypeBuffer to satisfy a queued withdrawal must remain usable for withdrawal liquidity or be restored on cancellation`
- `queued withdrawals must share post-queue slashing losses consistently with remaining and later-withdrawing holders`

坏的写法：

- `The staking flow should preserve protocol accounting, authorization, and user fund invariants.`
- `The token flow should be safe.`

### tags

tags 用于跨协议语义过滤，不放协议名和严重性。

不要放：

- `ethena`
- `kinetiq`
- `nudgexyz`
- `high`
- `medium`
- `low`

这些已有独立字段：

- `protocol_name`
- `severity`
- `classification`

应该放：

- 根因：`access-control-bypass`, `accounting-desync`, `snapshot-staleness`
- 组件：`erc4626`, `oracle`, `withdrawal`, `l1-operations`
- 影响/模式：`denial-of-service`, `fund-lock`, `share-accounting`, `gas-dos`

## 2. Low / QA 的定位

Low / Non-critical / QA 不进入主 case_reports。

它们只有在能回答下面问题时才保留：

> 为什么这个看起来像 Medium / High 的问题，实际上只是 Low / QA / false positive？

保留位置：

`data/normalized/false_positive_cases/`

推荐字段重点：

- `issue_claim`: 表面上看起来的问题
- `why_it_looked_bad`: 为什么容易被误报成 HM
- `why_not_valid`: 为什么最终只能作为 Low / QA / downgrade reference
- `when_it_could_be_real`: 在什么额外条件下才可能升级
- `tags`: 仍然只放跨协议语义标签

纯代码质量项默认不入库，例如：

- typo
- event 参数类型不一致但无安全影响
- setter 逻辑可优化
- 无直接审计决策价值的 gas micro-optimization

## 3. provisional：活跃审计中的临时知识

活跃审计过程中发现的候选案例、pattern、false-positive 判断和 validation recipe，在最终结果确认前不要进入正式 RAG。

原因：这些内容还可能被后续 PoC、独立 review、sponsor/judge 反馈或最终报告推翻。如果提前进入 `data/normalized/` 或正式 eval，会把未确认假设固化成检索事实，污染后续审计判断。

默认存放位置：

```text
data/provisional/contests/<contest-slug>/
  candidate_patterns/
  candidate_cases/
  false_positive_candidates/
  validation_recipes/
  eval_candidates/
  notes/
```

归档到 `data/normalized/` 的前置条件：

1. 审计已经结束，或该 finding 已形成最终提交/最终报告/明确确认结果；
2. 重新检查 root cause、broken invariant、impact 和 downgrade 条件；
3. 抽掉当前 contest 的偶然细节，只保留可跨协议复用的知识；
4. 再补正式 eval 查询；
5. 跑完整验证门槛。

## 4. 入库后验证

每次批量沉淀后至少检查：

```bash
source .venv/bin/activate
python -m audit_rag.cli.main validate-data
python -m audit_rag.cli.main --help
pytest -q
```

`validate-data` 会同时跑 JSON Schema 和项目自定义质量门槛：

- `root_cause` 不以 `Report-described`、`protocol invariant violation in` 或 `state/accounting validation gap in` 这类自动生成前缀开头
- `broken_invariants` 不含模板句
- `tags` 不含协议名和 severity
- Low/QA 不污染主 High/Medium 检索流
