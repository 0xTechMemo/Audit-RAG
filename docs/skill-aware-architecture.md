# Skill + RAG + AI 架构设计（skill-aware architecture）

## 1. 设计目标

本项目不把 RAG、skill、AI 当成三套彼此竞争的系统，而是明确分工：

- skill：定义工作流、阶段、质量门槛、默认输入输出契约
- RAG：提供结构化知识、相似案例、误报样本、验证模板
- AI：基于当前代码上下文和检索证据做推理、取舍、组织输出

一句话：
skill 管流程，RAG 管知识，AI 管推理。

## 2. 为什么要做 skill-aware RAG

普通 RAG 的问题是：
- 不知道当前任务处于哪一个审计阶段
- 不知道应该优先召回 pattern 还是 false positive
- 不知道输出应该满足什么 schema
- 容易给出泛泛而谈但工作流价值不高的回答

skill-aware RAG 的核心思想是：
检索和输出都要知道“自己当前正在服务哪个 skill、哪个阶段、哪个目标”。

## 3. 第一版聚焦的 skill

第一版只聚焦一个主工作流：
- 竞赛型智能合约审计 triage 工作流

对应阶段：
1. intake
2. hotspoting
3. module-review
4. candidate-triage
5. validation
6. submission-packaging

当前 v0 最先做透的阶段：
- candidate-triage

## 4. 三层架构

### 第一层：Workflow / Skill 层

作用：
- 告诉系统当前阶段是什么
- 规定当前阶段必须回答哪些问题
- 定义质量门槛与失败条件

这一层不存放大量案例知识。
它更像运行时策略层。

### 第二层：Knowledge / RAG 层

作用：
- 返回匹配的 case_report
- 返回相关 vulnerability_pattern
- 返回 false_positive_case
- 返回 validation_recipe

这一层只负责供料，不直接拍板“这个问题已经成立”。

### 第三层：Reasoning / AI 层

作用：
- 读取当前代码上下文
- 综合 skill 约束与 RAG 返回证据
- 输出结构化 triage 结果

这一层的职责不是“自由发挥”，而是在证据和流程约束中做判断。

## 5. 第一版 candidate-triage 节点设计

### 输入

- issue_text：当前怀疑点描述
- code_context：可选，来自函数摘要、代码片段、文件路径说明
- stage_context：说明当前 skill、阶段、组件、目标

### stage_context 建议字段

- skill_name
- stage_name
- component_type
- audit_goal
- require_false_positive_check
- desired_output_schema

### 检索策略

candidate-triage 阶段默认优先检索：
1. 相似 case_report
2. 相关 vulnerability_pattern
3. false_positive_case
4. validation_recipe

和 module-review 不同的是：
candidate-triage 阶段要额外提高：
- false positive 权重
- severity calibration 相关案例权重
- submission blocker 提示权重

## 6. candidate-triage 固定输出问题

第一版默认所有 triage 输出都要回答：
1. 可能根因是什么
2. 可能打破了什么 invariant
3. 谁能利用：permissionless 还是 privileged-only
4. 影响大致是什么
5. 为什么可能不成立
6. 还缺什么验证证据
7. 下一步最小验证动作是什么

## 7. 推荐目录结构调整

在现有仓库上新增以下逻辑层：

- `src/audit_rag/orchestration/`
  - 保存 skill-aware 运行时上下文、阶段配置和调度逻辑
- `src/audit_rag/contracts/`
  - 保存输入输出契约模型，尤其是 triage 阶段的 schema
- `src/audit_rag/retrieval/query_context.py`
  - 保存 query context 定义，而不是只传裸字符串
- `docs/plans/`
  - 保存实现计划

## 8. 第一版运行流

1. skill runtime 接收当前阶段信息
2. 组装 query context
3. 检索层根据 context 决定召回和重排偏好
4. AI 聚合层读取：
   - 当前 issue_text
   - stage_context
   - RAG 结果
5. 输出固定 triage schema

## 9. 第一版不做的事

- 让 AI 直接跳过 skill 和 query context 自由检索
- 把大量判例直接写死进 skill 文本
- 一上来支持所有阶段自动化
- 在没有 source trace 的情况下输出强结论

## 10. 设计默认值

- 默认只做 candidate-triage 的 skill-aware 集成
- 默认所有 triage 都查 false-positive 通道
- 默认 severity 取保守区间
- 默认返回结构化 JSON 优先
- 默认区分“模式相似证据”和“项目内成立证据”
