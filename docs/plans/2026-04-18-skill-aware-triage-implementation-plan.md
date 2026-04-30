# Skill-Aware Triage 实现计划（历史记录）

> 这份计划已经完成其早期目标，并被当前 audit workbench 方向替代。保留它是为了说明项目演进，不再作为当前执行计划。

## 原计划目标

早期目标是在 audit-rag 中引入 skill-aware triage：检索不再只接收裸字符串，而是接收 skill/stage/component 语义的 query context，并输出固定 schema。

这些能力现在已经沉淀到：
- `src/audit_rag/retrieval/query_context.py`
- `src/audit_rag/retrieval/issue_triage.py`
- `src/audit_rag/indexing/hybrid_search.py`
- `src/audit_rag/contracts/triage.py`

## 当前替代方向

当前主线不是继续扩 `triage-issue`，而是把 audit-rag 做成合约审计 skill 的状态化后端：
- `src/audit_rag/contest/lead_ledger.py`
- `src/audit_rag/contest/scorecard.py`
- `data/provisional/contests/<contest-slug>/lead-ledger.jsonl`
- `data/provisional/contests/<contest-slug>/rag-triage/<lead-id>.json`
- `data/provisional/contests/<contest-slug>/contest-summary.md`
- `data/provisional/contests/<contest-slug>/promotion-manifest.json`

## 当前执行入口

```bash
python -m audit_rag.cli.main add-lead <contest-slug> <title> [--text ...]
python -m audit_rag.cli.main list-leads <contest-slug>
python -m audit_rag.cli.main triage-lead <contest-slug> <lead-id>
python -m audit_rag.cli.main suppress-check <contest-slug> <lead-id>
python -m audit_rag.cli.main update-lead <contest-slug> <lead-id> [--status ...]
python -m audit_rag.cli.main export-contest-summary <contest-slug>
python -m audit_rag.cli.main promote-provisional <contest-slug> [--confirmed]
```

## 当前质量门槛

- active lead 必须先进 ledger，不要只留在聊天上下文。
- RAG scorecard 只是 evidence，不是 finding 证明。
- 未确认 active audit 知识不能进入 `data/normalized/`。
- `promote-provisional` 默认 dry-run，只有最终结果确认和人工整理后才可 `--confirmed`。
- 修改本机 Hermes skill 后，运行 `python3.11 scripts/sync_skill_docs.py` 同步到 `docs/skills/`。
