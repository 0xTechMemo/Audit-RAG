# 本地启动说明（local-setup）

## 目的

这份文档是仓库的本地启动清单，帮助你在当前机器上把项目跑起来。

## 当前状态

以下内容已经完成：
- 仓库目录骨架已创建
- 初始配置文件已创建
- 详细文档已创建
- Python 虚拟环境已创建
- 依赖已安装
- CLI 已验证可运行
- pytest 已验证通过

## 当前机器的 Python 说明

本机上：
- `python3` 当前解析到 3.9.6
- `python3.11` 可用，版本为 3.11.15

由于 `pyproject.toml` 要求 `>=3.11`，所以后续创建环境时请显式使用 `python3.11`。

## 推荐启动命令

```bash
cd /Users/qwe/Audit/audit-rag
source .venv/bin/activate
python -m audit_rag.cli.main --help
pytest -q
```

如果你需要从头重新创建环境：

```bash
cd /Users/qwe/Audit/audit-rag
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
python -m audit_rag.cli.main --help
pytest -q
```

## 预期结果

- `python -m audit_rag.cli.main --help` 能正常显示 CLI 帮助
- `pytest -q` 至少能跑通当前 starter test

## 如果启动失败，优先检查

1. 是否在项目根目录执行命令
2. 是否激活了 `.venv`
3. 是否用了 `python3.11` 创建环境
4. 是否已经执行过 `pip install -e .[dev]`

## 建议的第一轮阅读顺序

1. `docs/prd.md`
2. `docs/data-schema.md`
3. `docs/tag-taxonomy.md`
4. `docs/retrieval-design.md`
5. `docs/week-1-plan.md`

## 建议的第一轮开发动作

1. 先在 `data/normalized/` 下手工写几条样本记录
2. 再实现 `validate-data` 命令
3. 然后把 `triage-issue` 从 todo 占位改成真实样本检索
