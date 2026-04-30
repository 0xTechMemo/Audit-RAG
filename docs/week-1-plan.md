# 第一周开发计划（历史记录，已被当前方向替代）

这份文档保留为项目早期开发记录。旧目标是让 `triage-issue` 先跑通最小 skill-aware RAG；这个阶段已经完成并被当前产品方向替代。

当前主线见：
- `docs/audit-workbench-direction.md`
- `docs/prd.md`
- `docs/triage-interface.md`

## 当前方向

audit-rag 不再以“更多历史案例 + 一次性 query”为主线，而是作为合约审计 skill 的状态化后端：
- lead ledger
- triage scorecard
- duplicate / false-positive / QA downgrade suppression
- PoC recipe
- provisional→normalized 知识沉淀

## 当前 active audit 流程

```bash
python -m audit_rag.cli.main add-lead <contest-slug> <title> [--text ...]
python -m audit_rag.cli.main triage-lead <contest-slug> <lead-id>
python -m audit_rag.cli.main suppress-check <contest-slug> <lead-id>
python -m audit_rag.cli.main update-lead <contest-slug> <lead-id> [--status ...]
python -m audit_rag.cli.main export-contest-summary <contest-slug>
```

## 仍然有效的早期原则

- Python-first
- CLI-first
- normalized JSON 是正式事实源
- active audit 未确认知识先进 provisional
- false-positive / downgrade 通道必须保留
- 测试和 eval 回归不能丢
