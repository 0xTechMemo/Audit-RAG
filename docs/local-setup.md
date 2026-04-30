# 本地启动说明（local-setup）

## 目的

这份文档是 audit-rag 的本地启动清单。
当前项目定位：合约审计 skill 的状态化后端，核心是 lead ledger、triage scorecard、suppression check、PoC recipe 和 provisional→normalized 知识沉淀。

## 当前状态

已完成：
- Python 项目骨架
- normalized 数据校验
- lexical-first hybrid retrieval
- free-form `triage-issue`
- active audit `add-lead` / `list-leads` / `triage-lead` / `suppress-check`
- `update-lead`
- `export-contest-summary`
- `promote-provisional` dry-run 安全门
- skill Markdown mirror 到 `docs/skills/`
- pytest / ruff 验证

## Python 说明

本机上 `python3` 可能解析到 3.9.x；项目要求 Python >= 3.11。
后续创建环境时显式使用 `python3.11`。

## 推荐启动命令

```bash
cd /Users/qwe/Audit/audit-rag
source .venv/bin/activate
python -m audit_rag.cli.main --help
python -m audit_rag.cli.main validate-data
pytest -q
ruff check .
```

如果需要从头重建环境：

```bash
cd /Users/qwe/Audit/audit-rag
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
python -m audit_rag.cli.main --help
pytest -q
```

## active audit 最小流程

```bash
python -m audit_rag.cli.main add-lead <contest-slug> "<lead title>" --text "<candidate issue>"
python -m audit_rag.cli.main triage-lead <contest-slug> <lead-id>
python -m audit_rag.cli.main suppress-check <contest-slug> <lead-id>
python -m audit_rag.cli.main update-lead <contest-slug> <lead-id> --status needs-poc --current-blocker "missing runnable PoC"
python -m audit_rag.cli.main export-contest-summary <contest-slug>
```

## 建议阅读顺序

1. `README.md`
2. `docs/audit-workbench-direction.md`
3. `docs/prd.md`
4. `docs/triage-interface.md`
5. `docs/skill-aware-architecture.md`
6. `docs/data-schema.md`
7. `docs/retrieval-design.md`

## 如果启动失败，优先检查

1. 是否在项目根目录执行命令
2. 是否激活了 `.venv`
3. 是否用了 `python3.11` 创建环境
4. 是否已经执行过 `pip install -e .[dev]`
