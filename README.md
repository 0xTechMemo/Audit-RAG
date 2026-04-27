# audit-rag

一个面向竞赛型智能合约审计的本地 RAG 工作台。

## 项目定位

这个项目不是通用聊天机器人，也不是自动报洞器。

它的目标是服务 Code4rena、Sherlock 这类比赛型审计流程。它不是替你证明漏洞，而是在审计辅助中帮助你更快找到类似漏洞、相邻模式、验证路径和降级风险，并在每次真实审计后继续沉淀为更通用的审计 RAG。

它具体帮助你：
- 更快召回相关漏洞模式
- 更快拿到组件级审计 checklist
- 更快判断候选问题值不值得继续追
- 更少浪费时间在误报、弱问题、QA-only 方向上
- 更快形成验证思路与证据补强路径
- 把审计结束后已经确认的新模式、false-positive 和 recipe 反哺回本地知识库

活跃审计中的未确认线索不直接进入正式 RAG。它们先放在 `data/provisional/contests/<contest-slug>/`，等最终报告或提交结果确认后，再经过归档审校写入 `data/normalized/` 和正式 eval。

## 首版范围

当前版本采用：
- Python-first
- local-first
- CLI-first
- 结构化知识库优先

首版重点：
- 本地结构化数据
- lexical-first 检索 + 元数据/阶段上下文轻量加权
- 候选问题 triage
- false positive 抑制
- skill-aware triage 骨架

当前状态：
- `case_reports`: 97 条，主召回流只放 Medium/High 和少量手写高质量样本
- `false_positive_cases`: 21 条，用于降级、误报和 QA-like caution 通道
- `vulnerability_patterns`: 17 条，已从现有 C4 样本提炼出 oracle、connector、liquidation、access control、withdrawal、reward、cross-domain queue 等核心模式
- `component_checklists`: 8 条，用于组件级 intake / 模块审计辅助
- `validation_recipes`: 11 条，用于把候选问题转成 PoC / 单测 / 状态机验证路线
- `contest_notes`: 3 条，用于保存 audit page / mitigation review 上下文
- `hybrid_search.py`: 已有 lexical-first 实现；同时召回 case / pattern / validation recipe，并保持 false-positive caution 通道独立
- `data/eval/retrieval_queries.jsonl`: 26 条手工 recall 查询样本，已覆盖 case / false-positive / pattern / checklist，并纳入 `pytest` 回归测试
- `data/provisional/`: 活跃审计中的候选知识暂存区，不参与正式 RAG 检索；最终确认后再归档

当前架构默认采用：
- skill 定义阶段、质量门槛、默认输入输出契约
- RAG 提供 pattern / case / false-positive / validation 证据
- AI 在阶段上下文和检索证据约束下组织结论

一句话：
skill 管流程，RAG 管知识，AI 管推理。

## 目录说明

- `configs/`：项目配置
- `data/`：原始数据、正式结构化数据、provisional 候选知识、chunk、索引、评测集
- `docs/`：PRD、schema、标签体系、检索设计、阶段架构、术语表、周计划
- `src/audit_rag/orchestration/`：skill-aware 工作流运行时与阶段配置
- `src/audit_rag/contracts/`：阶段输入输出契约模型
- `schemas/`：核心知识对象的 JSON Schema
- `src/audit_rag/`：Python 源码
- `tests/`：测试目录

## 快速开始

```bash
cd /Users/qwe/Audit/audit-rag
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
python -m audit_rag.cli.main --help
python -m audit_rag.cli.main validate-data
pytest -q
```

## 建议先读的文档

1. `docs/prd.md`
2. `docs/data-schema.md`
3. `docs/tag-taxonomy.md`
4. `docs/retrieval-design.md`
5. `docs/skill-aware-architecture.md`
6. `docs/triage-interface.md`
7. `docs/glossary-zh.md`
8. `docs/smart-contract-audit-glossary-zh.md`
9. `docs/week-1-plan.md`
10. `docs/local-setup.md`

## 设计原则

1. 所有输出都要可追溯到来源。
2. 相似模式不等于漏洞已成立。
3. 严重性判断默认保守。
4. false-positive 抑制是核心能力，不是附属功能。
5. 优先优化真实审计流程里的可用性，而不是做演示型功能。
6. skill 管流程，RAG 管知识，AI 管推理。
