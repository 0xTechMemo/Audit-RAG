# Skill + Audit-RAG + AI 架构设计

## 1. 当前设计目标

audit-rag 的当前定位不是“更聪明的聊天式 RAG”，也不是另一个审计 skill。
它是合约审计 skill 的状态化后端：记录 active audit lead、保存 triage 证据、给出降级/duplicate/false-positive 信号，并沉淀 PoC recipe 与 provisional knowledge。

一句话：

skill 管流程和质量门槛，audit-rag 管状态和证据，RAG 管召回，AI 管推理和报告组织。

## 2. 为什么不继续做单纯 skill-aware RAG

早期 `skill-aware RAG` 的核心是让检索知道当前 skill/stage/component。这个方向仍然保留在底层 `QueryContext` 中，但它不再是产品主线。

真实审计里更缺的是：
- 哪些 lead 还没验证
- 哪些 lead 被 duplicate / known finding / QA 降级风险挡住
- 哪些 lead 有 PoC，哪些只有直觉
- 哪些 provisional 知识审计结束后能沉淀到 normalized/eval
- 跨会话继续时，如何恢复当前审计状态

所以当前架构把 `lead-ledger` 作为 active audit 的 canonical state，把 RAG 检索降为支撑层。

## 3. 三层分工

### Skill 层

负责：
- contest intake、scope、known finding、V12/public-known 检查规则
- severity guardrails
- 提交格式和报告质量门槛
- 什么时候调用 audit-rag 的 CLI

不负责：长期存 active lead 状态、大量案例知识、每个 lead 的 PoC 进度。

### Audit-RAG 状态层

负责：
- `lead-ledger.jsonl`
- `rag-triage/<lead-id>.json`
- `contest-summary.md`
- `promotion-manifest.json`
- provisional contest knowledge
- normalized/eval 正式知识库

这是 active audit 的状态化后端。

### AI 推理层

负责：
- 阅读当前代码
- 综合 skill 规则、audit-rag evidence、PoC 结果
- 组织审计报告
- 判断哪些内容仍缺证据

AI 不能把 RAG 相似案例当作当前项目漏洞证明。

## 4. 当前默认工作流

```bash
python -m audit_rag.cli.main add-lead <contest-slug> <title> [--text ...] [--component ...]
python -m audit_rag.cli.main list-leads <contest-slug>
python -m audit_rag.cli.main triage-lead <contest-slug> <lead-id>
python -m audit_rag.cli.main suppress-check <contest-slug> <lead-id>
python -m audit_rag.cli.main update-lead <contest-slug> <lead-id> [--status ...] [--current-blocker ...]
python -m audit_rag.cli.main export-contest-summary <contest-slug>
python -m audit_rag.cli.main promote-provisional <contest-slug> [--confirmed]
```

## 5. 固定数据路径

- active lead ledger: `data/provisional/contests/<contest-slug>/lead-ledger.jsonl`
- RAG scorecard: `data/provisional/contests/<contest-slug>/rag-triage/<lead-id>.json`
- contest summary: `data/provisional/contests/<contest-slug>/contest-summary.md`
- promotion manifest: `data/provisional/contests/<contest-slug>/promotion-manifest.json`
- formal knowledge: `data/normalized/`
- retrieval eval: `data/eval/retrieval_queries.jsonl`

## 6. 质量门槛

1. active audit 中的未确认知识只进 `data/provisional/contests/<slug>/`。
2. `promote-provisional` 默认 dry-run；只有最终结果确认、人工整理后才允许 `--confirmed`。
3. triage 输出只能作为 evidence，不是 finding 证明。
4. PoC、reachability、impact 必须回到当前代码验证。
5. skill Markdown 镜像只从本机 Hermes skill 同步，不手工改 `docs/skills/*/SKILL.md`。
