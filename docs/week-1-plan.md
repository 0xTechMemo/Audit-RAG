# 第一周开发计划

> 目标：完成一个干净的 Python-first 项目骨架，锁定核心数据结构，并让最小版 `triage-issue` 能基于手工样本数据跑通端到端流程。

补充说明：
- 第一周结束时，`triage-issue` 最好已经具备最小 skill-aware 形态
- 即便检索能力还很朴素，也要先把 `skill_name` / `stage_name` / `false-positive 通道` 这些骨架打进去

## Day 1：环境和仓库基线

目标：
- 建立本地 Python 环境
- 完成 editable install
- 确认 CLI 入口能正常运行

任务：
1. `cd /Users/qwe/Audit/audit-rag`
2. `python3.11 -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install -U pip`
5. `pip install -e .[dev]`
6. `python -m audit_rag.cli.main --help`
7. `pytest -q`

完成标准：
- editable install 成功
- CLI help 正常打印
- pytest 通过

## Day 2：锁定 schema，并起草样本对象

目标：
- 确认前四类核心 schema 足够用
- 手工写出第一批样本数据

任务：
1. 阅读 `docs/data-schema.md`
2. 阅读 `docs/tag-taxonomy.md`
3. 在 `data/normalized/` 下创建样本 JSON：
   - `case_reports`
   - `vulnerability_patterns`
   - `false_positive_cases`
   - `component_checklists`
4. 手工检查标签是否统一、字段是否清晰

完成标准：
- 四类对象各至少 2 条样本
- 标签不混乱、不临时发挥

## Day 3：实现 schema 校验工具

目标：
- 支持本地 JSON Schema 校验
- 尽早拦截脏数据和坏记录

任务：
1. 创建 `src/audit_rag/storage/json_store.py`
2. 创建 `src/audit_rag/utils/files.py`
3. 增加 CLI 命令，例如 `validate-data`
4. 对 `data/normalized/` 下所有 JSON 做校验
5. 增加一个 valid / invalid 的测试用例

完成标准：
- 一条命令就能看到校验成功/失败结果

## Day 4：做最小本地检索

目标：
- 读取样本数据
- 实现最简单的 lexical matcher

任务：
1. 实现 record loader
2. 在 `src/audit_rag/indexing/hybrid_search.py` 里写最朴素的 scoring
3. 让 `triage_issue()` 调用这个检索逻辑
4. 正向匹配和 false-positive warning 分开返回
5. 为 triage 增加最小 `stage_context`
6. 增加 deterministic 测试

完成标准：
- `triage-issue` 返回真实样本匹配，而不是 todo 占位
- 返回里能看到最小 skill-aware 上下文字段

## Day 5：固定输出结构

目标：
- 停止返回临时 dict 结构
- 锁定 candidate issue 输出格式

任务：
1. 在 `domain/models.py` 或 `contracts/` 里定义 triage result model
2. 更新 formatter
3. 输出中固定包含：
   - `sources`
   - `submission_blockers`
   - `false_positive_risks`
   - `skill_name`
   - `stage_name`
4. 增加回归测试

完成标准：
- 输出结构稳定且面向 source trace

## Day 6：准备微型评测集

目标：
- 准备第一批 benchmark 数据

任务：
1. 创建 `data/eval/retrieval_queries.jsonl`
2. 创建 `data/eval/triage_cases.jsonl`
3. 包含 5 个强案例和 5 个弱/QA-like 案例
4. 为每条查询记录预期匹配 ID

完成标准：
- 可以手工判断检索方向是否在变好

## Day 7：复盘和收口

目标：
- 把这周当成产品复盘，而不只是代码堆积

任务：
1. 跑测试
2. 检查输出噪音
3. 删除无用或重复标签
4. 写 `docs/week-1-retro.md`
5. 决定第二周优先做 ingestion 还是 richer retrieval

完成标准：
- 已有工作骨架、样本数据、可运行 triage、清晰的 week-2 方向

## 第一周固定默认值

- 语言：只用 Python
- 接口：只做 CLI
- 数据源：只用本地手工样本
- 检索：先 lexical-first，不先接向量库
- 成功标准：先证明工作流有价值，而不是模型高级

## 第一周质量门槛

进入第二周前，至少要满足：
1. `pip install -e .[dev]` 可稳定运行
2. CLI 无 import 错误
3. schema 足够支撑 8~10 条样本记录
4. `triage-issue` 能分开输出正向匹配和 false-positive 提醒
5. `triage-issue` 已具备最小 skill-aware 字段
6. 至少有一组测试存在并通过
