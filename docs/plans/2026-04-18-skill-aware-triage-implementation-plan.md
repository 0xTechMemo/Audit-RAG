# Skill-Aware Triage 实现计划

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 在 audit-rag 中引入第一版 skill-aware triage 架构，让 triage 查询知道自己服务于哪个工作流阶段，并输出固定 schema。

**Architecture:** 在现有候选问题 triage 原型之上，新增 orchestration 层与 triage 契约层。retrieval 不再只接收裸字符串，而是接受带有 skill/stage/component 语义的 query context。第一版先把 candidate-triage 节点做透，不急着铺开其他阶段。

**Tech Stack:** Python 3.11, Pydantic, Typer, pytest

---

### Task 1: 创建 orchestration 骨架

**Objective:** 增加 skill-aware runtime 的基础目录与占位模块。

**Files:**
- Create: `src/audit_rag/orchestration/__init__.py`
- Create: `src/audit_rag/orchestration/skill_runtime.py`
- Create: `src/audit_rag/orchestration/stage_registry.py`
- Test: `tests/retrieval/test_issue_triage.py`

**Step 1: Write failing test**

在 `tests/retrieval/test_issue_triage.py` 中新增一个测试，断言 triage 结果里能看到 `stage_name` 和 `skill_name`。

**Step 2: Run test to verify failure**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: FAIL — 缺少相关字段

**Step 3: Write minimal implementation**

在 orchestration 层创建最小运行时上下文对象，先保证字段存在。

**Step 4: Run test to verify pass**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add src/audit_rag/orchestration tests/retrieval/test_issue_triage.py
git commit -m "feat: add skill-aware orchestration skeleton"
```

### Task 2: 定义 triage 输入输出契约

**Objective:** 用明确模型锁定 candidate-triage-v1 的输入输出结构。

**Files:**
- Modify: `src/audit_rag/domain/models.py`
- Create: `src/audit_rag/contracts/__init__.py`
- Create: `src/audit_rag/contracts/triage.py`
- Test: `tests/retrieval/test_issue_triage.py`

**Step 1: Write failing test**

添加测试，要求 triage 结果至少包含：
- `query_type`
- `skill_name`
- `stage_name`
- `false_positive_risks`
- `submission_blockers`
- `sources`

**Step 2: Run test to verify failure**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: FAIL

**Step 3: Write minimal implementation**

新增 Pydantic 模型或 Typed Dict，先把结构锁定。

**Step 4: Run test to verify pass**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add src/audit_rag/domain/models.py src/audit_rag/contracts tests/retrieval/test_issue_triage.py
git commit -m "feat: define skill-aware triage contracts"
```

### Task 3: 为检索引入 query context

**Objective:** 让检索层知道当前阶段和组件，而不是只拿 issue text。

**Files:**
- Create: `src/audit_rag/retrieval/query_context.py`
- Modify: `src/audit_rag/indexing/hybrid_search.py`
- Modify: `src/audit_rag/retrieval/issue_triage.py`
- Test: `tests/retrieval/test_issue_triage.py`

**Step 1: Write failing test**

新增测试：传入 `component_type="reward-distribution"` 时，返回结果中保留该上下文。

**Step 2: Run test to verify failure**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: FAIL

**Step 3: Write minimal implementation**

新增 `QueryContext`，并将其贯穿到 triage 调用链中。

**Step 4: Run test to verify pass**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add src/audit_rag/retrieval/query_context.py src/audit_rag/indexing/hybrid_search.py src/audit_rag/retrieval/issue_triage.py tests/retrieval/test_issue_triage.py
git commit -m "feat: pass query context through triage retrieval"
```

### Task 4: 分离正向匹配和 caution 通道

**Objective:** triage 输出中显式分开 positive matches 和 false-positive / downgrade 通道。

**Files:**
- Modify: `src/audit_rag/retrieval/issue_triage.py`
- Modify: `src/audit_rag/services/output_formatter.py`
- Test: `tests/retrieval/test_issue_triage.py`

**Step 1: Write failing test**

断言输出中存在：
- `matching_cases`
- `matching_patterns`
- `false_positive_risks`

**Step 2: Run test to verify failure**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: FAIL

**Step 3: Write minimal implementation**

在 triage 聚合逻辑里区分两类通道，哪怕当前还是样本占位。

**Step 4: Run test to verify pass**

Run: `pytest tests/retrieval/test_issue_triage.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add src/audit_rag/retrieval/issue_triage.py src/audit_rag/services/output_formatter.py tests/retrieval/test_issue_triage.py
git commit -m "feat: separate caution channel in triage outputs"
```

### Task 5: 文档与命令对齐

**Objective:** 保证 README、架构文档、接口文档和 CLI 行为一致。

**Files:**
- Modify: `README.md`
- Modify: `docs/prd.md`
- Modify: `docs/retrieval-design.md`
- Modify: `docs/week-1-plan.md`
- Create: `docs/skill-aware-architecture.md`
- Create: `docs/triage-interface.md`

**Step 1: Review docs for mismatch**

逐项检查文档中是否还把 triage 描述为无阶段上下文的纯文本检索。

**Step 2: Update docs**

把 skill-aware triage 作为 v0.1 的推荐架构写入文档。

**Step 3: Verify commands**

Run: `python -m audit_rag.cli.main --help`
Expected: CLI 正常输出

**Step 4: Run tests**

Run: `pytest -q`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md docs src tests
git commit -m "docs: align repo docs with skill-aware triage design"
```
