# 英中文术语对照表（glossary-zh）

这份文档用于辅助阅读本项目中的英文术语、配置名和常见 RAG / 审计概念。

说明：
- 我保留英文原词，因为后续你实际写代码、查资料、看开源库时，还是会频繁遇到这些词。
- 中文释义尽量按“这个项目语境下怎么理解”来写，不追求教科书式翻译。

## 一、项目与产品层术语

- audit-rag：审计 RAG 项目 / 审计检索增强生成系统
- local-first：本地优先
- Python-first：以 Python 为主
- CLI-first：命令行优先
- workbench：工作台
- product：产品
- project scope：项目范围
- PRD (Product Requirements Document)：产品需求文档
- MVP (Minimum Viable Product)：最小可用产品
- non-goals：非目标 / 当前版本明确不做的事
- success metrics：成功指标
- failure conditions：失败条件
- quality gate：质量门槛
- baseline：基线 / 初始可运行状态
- skeleton：骨架 / 最小项目框架
- bootstrap：启动搭建 / 初始化

## 二、RAG 与检索层术语

- RAG (Retrieval-Augmented Generation)：检索增强生成
- retrieval：检索
- retrieval design：检索设计
- query：查询
- query type：查询类型
- lexical retrieval：关键词检索 / 词面检索
- semantic retrieval：语义检索
- hybrid retrieval：混合检索
- metadata filter：元数据过滤
- rerank / reranking：重排 / 二次排序
- scoring：打分
- source-backed：有来源支撑的
- source trace：来源追踪 / 来源可追溯信息
- top-k：取前 k 个结果
- chunk：文本切块 / 检索块
- chunking：切块
- index：索引
- vector index：向量索引
- BM25：一种常用关键词检索算法
- recall：召回
- precision：精度 / 准确率
- recall result：召回结果
- retrieval pipeline：检索流水线 / 检索流程

## 三、数据与结构化层术语

- schema：数据结构定义 / 模式
- JSON Schema：JSON 结构校验规范
- structured data：结构化数据
- normalized data：归一化后的数据
- raw data：原始数据
- record：记录
- object：对象
- field：字段
- required fields：必填字段
- optional fields：可选字段
- validation：校验
- validation utility：校验工具
- validation status：验证状态
- storage：存储层
- loader：加载器
- parser：解析器
- extractor：提取器
- normalizer：归一化器
- formatter：格式化器
- config：配置
- taxonomy：分类体系 / 标签体系
- tag：标签
- tag taxonomy：标签体系

## 四、审计工作流术语

- contest：比赛 / 审计竞赛
- contest repo：比赛代码仓库
- intake：项目 intake / 初始摄入与理解阶段
- hotspot：热点 / 高风险区域
- hotspot summary：热点总结
- hotspot ranking：热点排序
- component：组件
- component type：组件类型
- checklist：检查清单
- component checklist：组件级审计清单
- pattern：模式
- vulnerability pattern：漏洞模式
- pattern recall：模式召回
- candidate issue：候选问题 / 怀疑点
- triage：分诊 / 初筛判断
- candidate issue triage：候选问题分诊
- false positive：误报 / 看起来像问题但实际上不成立或不够强
- false positive warning：误报提醒
- downgrade：降级
- validation recipe：验证方案模板 / 验证配方
- repo hotspot scan：仓库热点扫描
- submission：提交
- submission-ready：达到可提交程度
- submission blocker：阻碍提交的缺口 / 证据缺口
- replay test：回放测试
- audit workflow：审计工作流

## 五、漏洞分析相关术语

- finding：发现的问题 / 漏洞条目
- finding title：问题标题
- summary：摘要
- root cause：根因
- broken invariant：被破坏的不变量 / 关键约束
- invariant：不变量 / 系统应该始终成立的性质
- attack preconditions：攻击前置条件
- attacker capability：攻击者能力假设
- trigger action：触发动作
- exploit path：利用路径
- impact：影响
- severity：严重性
- severity baseline：基础严重性判断
- severity calibration：严重性校准
- why_not_higher：为什么不该定得更高
- why_not_lower：为什么不该定得更低
- mitigations：缓解建议 / 修复建议
- validation methods：验证方法
- common false positives：常见误判点
- trust boundary：信任边界
- trusted role：受信任角色
- privileged-only：仅特权角色才能触发
- permissionless：无权限用户也能触发
- misconfiguration-only：仅错误配置才会发生
- user-mistake-dependent：依赖用户误操作
- repeatable：可重复利用
- theory-only：仅理论成立，未验证
- publicly validated：已被公开验证
- locally validated：已在本地验证
- disputed：存在争议

## 六、代码与工程开发术语

- package：包
- editable install：可编辑安装
- virtual environment / venv：虚拟环境
- dependency：依赖
- test：测试
- regression test：回归测试
- deterministic：确定性的 / 可稳定复现的
- import error：导入错误
- entrypoint：入口
- command：命令
- script：脚本
- module：模块
- utils：工具函数
- domain models：领域模型
- service：服务层
- implementation：实现
- prototype：原型
- hardening：加固 / 稳定化
- refactor：重构
- retro / retrospective：复盘

## 七、当前文档里最关键的一批词，建议你优先记住

第一组：产品与范围
- MVP：最小可用产品
- PRD：产品需求文档
- non-goals：当前不做什么
- quality gate：质量门槛

第二组：检索系统
- retrieval：检索
- hybrid retrieval：混合检索
- rerank：重排
- source trace：来源追踪
- chunk：切块
- metadata filter：元数据过滤

第三组：审计工作流
- intake：项目初始理解阶段
- hotspot：高风险热点
- checklist：检查清单
- triage：分诊
- false positive：误报
- validation recipe：验证方案
- submission-ready：达到可提交程度

第四组：漏洞判断
- root cause：根因
- invariant：不变量
- impact：影响
- severity：严重性
- permissionless：无权限即可利用
- privileged-only：只有特权角色才能触发

## 八、在这个项目里，几个最容易混淆的词

1. pattern vs case_report
- pattern：抽象漏洞模式
- case_report：具体历史案例

2. recall vs triage
- recall：把相关知识召回出来
- triage：对你眼前这个怀疑点做强弱判断

3. validation vs retrieval
- retrieval：把相关资料找出来
- validation：真正验证这个问题在目标项目里是否成立

4. false positive vs low severity
- false positive：问题本身不成立，或关键前提不成立
- low severity / QA：问题可能成立，但不足以算 HM/M

5. source-backed vs generated answer
- source-backed：结论能指回具体来源
- generated answer：模型生成了一段话，但未必有证据支撑

## 九、你之后看文档时可以这样理解

如果你看到：
- pattern recall：理解成“给我这个模块常见会出什么问题”
- candidate triage：理解成“我怀疑这里有洞，帮我判断值不值得继续追”
- false positive warning：理解成“这个方向为什么可能是浪费时间”
- validation recipe：理解成“如果我要证明/证伪它，该怎么测”
- hotspot summary：理解成“我进 repo 以后先看哪里最划算”

## 十、建议

如果后面你还觉得哪些词看着别扭，可以继续把词丢给我。我可以继续把这份文档扩成：
- 审计专用术语表
- RAG/向量检索专用术语表
- Python 工程专用术语表
- Code4rena 常见 judge 语境术语表
