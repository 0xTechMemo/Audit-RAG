# 检索设计说明（retrieval-design）

## 目标

把关键词召回、语义召回、元数据过滤组合起来，形成一个对审计工作真正有用、且可追溯的检索流程。

当前版本补充目标：
- 让检索层知道自己当前服务于哪个 skill / stage
- 让 `candidate-triage` 和 `module-review` 使用不同的检索偏好

## 查询类型

系统第一版重点支持 4 类查询：

1. 组件查询
2. 代码 / 片段查询
3. 候选问题 triage 查询
4. 仓库热点查询

同时，查询对象不再只是裸字符串，而应逐步升级为：
- `QueryContext`
- `query payload`

## 检索阶段

### 阶段 1：查询归一化

先从输入里抽出：
- 可能的组件类型
- 可能的根因提示
- 可能的影响类型
- severity 相关上下文
- skill / stage 上下文

### 阶段 2：关键词检索

利用明确术语、函数名、协议术语做高精度召回。

适合命中的内容包括：
- specific function names
- rewardDebt / totalAssets / delegatecall 这类硬关键词
- 组件术语
- 常见漏洞模式名

### 阶段 3：语义检索

补充语义相似的 pattern 和 case 记录。

### 阶段 4：元数据过滤

按以下维度过滤和约束：
- 语言
- 组件
- 严重性相关上下文
- 验证状态
- 数据来源
- skill / stage 运行时上下文

### 阶段 5：重排（rerank）

综合以下因素打分：
- semantic similarity
- lexical match
- component match
- root-cause match
- severity relevance
- validation weight

对于 `candidate-triage` 阶段，默认额外提高：
- false positive 提示优先级
- severity calibration 相关记录权重
- submission blocker 相关记录权重

### 阶段 6：结构化组装

返回时不要只是堆 chunk，而要按结构输出：
- top patterns
- related cases
- false-positive warnings
- next validation ideas
- source traces

## 核心规则

false-positive 记录不能和正向案例混在同一个主排序流里。它们应该作为单独的警示通道输出。

RAG 的职责是辅助审计者更快找到类似漏洞、相邻模式、验证 recipe 和降级风险；它不能替代当前仓库代码阅读、可达性分析、影响证明或 PoC。

审计过程中发现但还没最终确认的案例、pattern、recipe 或 false-positive 判断，不得直接写入 `data/normalized/` 或正式 `data/eval/retrieval_queries.jsonl`。这些线索先存放在 `data/provisional/contests/<contest-slug>/`，作为当前审计的研究素材。只有在最终报告、最终提交结果、judge/sponsor 反馈或用户明确确认之后，才重新审校、抽象并归档到正式 RAG。

## skill-aware 检索约定

第一版推荐做法：
- orchestration 层传入 `skill_name`、`stage_name`、`component_type`
- retrieval 层根据上下文切换策略
- output 层返回固定 schema，而不是自由散文

## 第一版默认策略

- 先做 lexical-first 的原型
- 先把结构和工作流打通
- 向量检索可以延后
- 重排先用规则打分，不急着上复杂模型
- 先把 `candidate-triage` 的 skill-aware 骨架做透
