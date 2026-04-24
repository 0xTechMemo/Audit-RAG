# 下次从这里继续（continue-here）

这份文档用于帮助你在关闭窗口、隔天继续、或者换一个新会话时，快速把 audit-rag 项目续上。

## 项目固定信息

- 项目名：audit-rag
- 项目路径：`/Users/qwe/Audit/audit-rag`
- 默认交流语言：中文
- 当前方向：面向竞赛型智能合约审计的 skill-aware RAG
- 第一优先工作流：`candidate-triage`

## 下次最推荐的开场方式

你下次直接复制下面任意一种发给我即可。

### 模板 1：最短续接版

```text
继续 audit-rag，项目路径是 /Users/qwe/Audit/audit-rag
```

### 模板 2：标准续接版

```text
继续 audit-rag 项目：
- repo: /Users/qwe/Audit/audit-rag
- 中文交流
- 先检查当前状态
- 先读 docs/prd.md、docs/skill-aware-architecture.md、docs/triage-interface.md
- 然后继续往下做
```

### 模板 3：带任务续接版

```text
继续 audit-rag 项目：
- repo: /Users/qwe/Audit/audit-rag
- 中文交流
- 先检查当前状态
- 先读 docs/skill-aware-architecture.md 和 docs/triage-interface.md
- 然后继续做第二批样本和 validate-data
```

## 我下次进入项目后应该先做什么

如果你没有特别指定，我默认应先做以下步骤：

1. 检查项目目录：`/Users/qwe/Audit/audit-rag`
2. 阅读关键文档：
   - `docs/prd.md`
   - `docs/skill-aware-architecture.md`
   - `docs/triage-interface.md`
   - `docs/week-1-plan.md`
3. 检查当前代码骨架和样本数据
4. 继续当前阶段最自然的下一步

## 当前建议优先级

如果你下次没说具体做什么，建议默认按下面顺序推进：

1. 扩充第二批样本数据
2. 实现 `validate-data` 命令
3. 把 `triage-issue` 接到本地样本检索
4. 做最小 lexical retrieval
5. 再考虑 richer retrieval 和向量检索

## 当前仓库里最重要的文档

### 总设计
- `docs/prd.md`
- `docs/retrieval-design.md`
- `docs/skill-aware-architecture.md`
- `docs/triage-interface.md`

### 学习辅助
- `docs/glossary-zh.md`
- `docs/smart-contract-audit-glossary-zh.md`

### 计划与执行
- `docs/week-1-plan.md`
- `docs/plans/2026-04-18-skill-aware-triage-implementation-plan.md`

## 当前仓库里最值得优先看的样本

### 原始机器可读版
- `data/normalized/case_reports/reward-debt-desync-case-01.json`
- `data/normalized/vulnerability_patterns/reward-debt-desync-pattern.json`
- `data/normalized/false_positive_cases/admin-bad-slippage-fp-01.json`
- `data/normalized/component_checklists/reward-distribution-checklist.json`
- `data/normalized/validation_recipes/reward-debt-desync-validation-recipe-01.json`

### 带中文注释版
- `data/normalized/case_reports/reward-debt-desync-case-01.annotated.jsonc`
- `data/normalized/vulnerability_patterns/reward-debt-desync-pattern.annotated.jsonc`
- `data/normalized/false_positive_cases/admin-bad-slippage-fp-01.annotated.jsonc`
- `data/normalized/component_checklists/reward-distribution-checklist.annotated.jsonc`
- `data/normalized/validation_recipes/reward-debt-desync-validation-recipe-01.annotated.jsonc`

## 当前代码里最关键的位置

- CLI 入口：`src/audit_rag/cli/main.py`
- triage 逻辑：`src/audit_rag/retrieval/issue_triage.py`
- lexical-first 检索：`src/audit_rag/indexing/hybrid_search.py`
- skill runtime：`src/audit_rag/orchestration/skill_runtime.py`
- triage 契约：`src/audit_rag/contracts/triage.py`
- 基础模型：`src/audit_rag/domain/models.py`

## 如果你想让我直接继续最合理的下一步

你可以直接发：

```text
继续 audit-rag，去 /Users/qwe/Audit/audit-rag
先检查当前状态，再直接做最合理的下一步
```

我默认会理解为：
- 先看文档
- 再看样本和代码状态
- 然后优先补样本 / validate-data / triage 检索

## 一句话版本

如果你只想记一句话，就记这个：

```text
继续 audit-rag，路径 /Users/qwe/Audit/audit-rag，先检查状态再往下做
```
