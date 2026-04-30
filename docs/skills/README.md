# Skill 文档镜像

这里保存与 audit-rag 工作流直接相关的 Hermes skill Markdown 镜像，目的是让 audit-rag 仓库本身记录：

- 合约审计流程规则由哪个 skill 定义
- audit-rag 如何作为该 skill 的状态化后端
- 后续 skill 经验更新需要同步进仓库，便于版本化和回溯

## 当前同步范围

- `c4-contest-auditor/SKILL.md`：Code4rena 合约审计主流程、scope、suppression、PoC、submission 规则。
- `c4-contest-auditor/references/c4-intake-notes.md`：C4 intake 参考说明。
- `audit-rag-workbench-maintainer/SKILL.md`：audit-rag workbench 项目本身的维护约定、数据治理规则和同步规则。

## 边界

- skill 是流程和质量门槛。
- audit-rag 是线索台账、降级判断、PoC recipe、provisional 知识和正式 normalized/eval 数据的状态化后端。
- 后续 active audit 默认使用 `add-lead` / `triage-lead` / `suppress-check` / `update-lead` / `export-contest-summary`；最终确认后先 dry-run `promote-provisional`，再人工确认 `--confirmed`。
- 这里不要手工改镜像文件；应先改本机 Hermes skill，再运行同步脚本。

## 同步命令

```bash
cd /Users/qwe/Audit/audit-rag
python3.11 scripts/sync_skill_docs.py
```

同步后运行：

```bash
source .venv/bin/activate
python -m audit_rag.cli.main --help
python -m audit_rag.cli.main validate-data
pytest -q
```
