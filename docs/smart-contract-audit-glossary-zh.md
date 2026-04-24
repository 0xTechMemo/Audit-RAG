# 智能合约审计专用术语表（smart-contract-audit-glossary-zh）

这份文档专门解释智能合约审计里最常见、最容易“看懂字面但没真正理解”的术语。

目标不是做学术定义，而是帮你在做比赛审计、读报告、写 finding、看评审意见时，快速抓住这些词在实战里的含义。

说明：
- 每个词我都会尽量按“审计语境”解释。
- 有些词在不同协议里细节不同，但核心判断框架基本一致。
- 如果一个词常常影响 severity，我会顺手标出来。

## 1. invariant

中文：不变量 / 必须始终成立的关键性质

实战理解：
审计里说 invariant，不是指代码里写了个 `assert`，而是指“这个系统正常运行时，不管谁怎么调用、按什么顺序调用，都不应该被打破的核心约束”。

常见例子：
- 用户拿到的份额不能长期大于其应得份额
- 协议总资产和总负债的关系不能失真
- 同一笔消息/签名/nonce 不能被重复消费
- 清算不能让坏账凭空转移给其他用户

为什么重要：
很多高质量 finding，本质上都可以被表述成：
“攻击者通过某种路径打破了某个本该始终成立的不变量。”

你以后看到一个 candidate，如果说不清：
- 被打破的 invariant 是什么
- 打破后造成什么后果
那这个 candidate 往往还不够成熟。

## 2. accounting

中文：会计 / 账务逻辑 / 资产负债与份额结算逻辑

实战理解：
accounting 不是单指“记账”，而是协议内部所有“谁该得多少、系统总共该有多少、某个动作后状态该怎么同步”的逻辑总称。

常见场景：
- vault 的 shares 和 assets 换算
- reward distribution 的累计奖励结算
- lending 的 debt / collateral / interest 计算
- bridge / messaging 的 fee 结算

为什么是高危区：
很多中高危问题并不是权限绕过，而是账务不同步、精度处理错误、状态更新顺序错误。

简单判断法：
只要你看到下面这些词，通常都该想到 accounting：
- totalAssets
- totalSupply
- share
- debt
- rewardDebt
- cumulativeIndex
- fee balance
- accrued

## 3. desync / state desynchronization

中文：状态不同步 / 状态失同步

实战理解：
desync 指两个本该同步的状态，在某次调用、某个边界条件、某种调用顺序下变得不一致。

常见表现：
- 用户余额更新了，但奖励基线没更新
- share 变了，但 totalAssets 的依赖值没同步
- 本地状态更新了，但全局状态没更新
- 消息标记已处理，但实际交付状态没完成

为什么重要：
很多协议不是“一步算完”，而是依赖多个变量协同表达真实状态。只要同步顺序错了，就容易出现：
- 重复领取
- 少扣 / 多发
- 错误赎回
- 状态回滚不完整

判断时常问自己：
- 哪两个状态本来应该一起变化？
- 有没有一个先变，另一个后补？
- 如果中间插入攻击者动作，会不会出问题？

## 4. stale oracle / stale price

中文：过期预言机 / 过期价格

实战理解：
协议使用的价格数据已经旧了，但系统仍然把它当作“当前可信价格”来执行借贷、清算、铸造、赎回等操作。

常见风险：
- 借得过多
- 该清算时没清算
- 不该清算时被清算
- 错误定价导致资产换算失真

为什么危险：
价格类协议极度依赖“时间上足够新”的数据。只要 stale check 不严，或者 heartbeat / timestamp / round 校验缺失，就会引发严重影响。

但也要注意：
不是所有“价格可能旧”都能算有效 finding。要看：
- 协议是否本来就接受一定延迟
- 是否还有其他保护
- 攻击者能否实际利用
- 是否真的会引发可量化影响

## 5. replay

中文：重放 / 重放攻击

实战理解：
某个本来只能被消费一次的授权、消息、签名、操作，攻击者通过缺少 nonce、domain separation、状态标记或时效检查等方式，把它再次利用。

常见场景：
- signature-based 授权
- permit
- cross-chain message
- withdrawal proof
- claim / mint authorization

常见根因：
- nonce 不唯一或未消费
- 消息 ID 不唯一
- domain separation 缺失
- 过期时间不严格
- 已处理状态未正确记录

为什么常见：
因为很多人只验证“这个签名对不对”，但没验证“它是不是只能用一次、只能在这里用、只能在这个链/合约/上下文里用”。

## 6. slippage

中文：滑点

实战理解：
交易执行结果与预期结果之间允许的偏差范围，尤其常见于 swap、router、vault 转换、桥接兑换路径中。

审计里的关键点：
- 是否有 minOut / minAmount 检查
- 谁来负责设置 slippage 参数
- 协议是否替用户承担价格保护责任

为什么经常被误判：
很多候选问题会说：
“如果滑点设置得很差，用户会亏钱。”

但这不一定是有效漏洞。你必须先问：
- 这个滑点是不是由用户自己传入？
- 协议是否已经明确把价格保护交给 caller？
- 这是不是 trusted role 的配置责任？

也就是说：
slippage 问题很常见，但不是都能上 M/H。

## 7. share inflation / donation inflation

中文：份额膨胀 / 捐赠导致的份额通胀操纵

实战理解：
常见于 vault/erc4626 场景。攻击者通过直接捐赠资产、操纵初始份额定价、利用空池/小池边界，让后续存入者以不公平价格获得或失去份额。

典型直觉：
系统把“池子里资产变多”当成“所有资产都应该体现在 share price 里”，但这些资产未必来自正常存款路径。

为什么常见：
- 空池首存边界很脆弱
- totalAssets / totalSupply 语义不严
- direct donation 的影响没被隔离
- preview 和 execute 路径不一致

判断要点：
- first depositor 是否可操纵
- donation 是否会污染 share price
- previewDeposit / deposit 是否一致
- 后续用户是否会被稀释或被不公平定价

## 8. fee-on-transfer token

中文：转账扣税代币 / 到账少于转出金额的代币

实战理解：
这种代币在 transfer / transferFrom 时，接收方实际收到的数量小于参数里写的数量。

为什么审计里危险：
很多协议默认认为：
“我 transferFrom 了 100，合约就一定收到 100。”

但对 fee-on-transfer token，这不成立。

可能后果：
- shares 铸造过多
- accounting 失真
- 抵押品数量被高估
- 赎回或奖励逻辑被污染

注意：
不是所有协议都必须支持这种 token。
如果协议明确不支持，且前提写得清楚，那它不一定是漏洞。
所以这类问题很容易跟“unsupported by design”纠缠在一起。

## 9. rebasing token

中文：弹性供应代币 / 会自动变化余额的代币

实战理解：
用户钱包里的 token 数量会因为协议机制自动变化，而不是只有转账才变化。

为什么审计里麻烦：
如果协议假设余额变化只来自显式转账，那么 rebasing token 会让内部 accounting 被动失真。

常见影响：
- share price 错乱
- collateral valuation 错乱
- 用户可领取金额异常
- 系统内部缓存余额与真实余额脱节

和 fee-on-transfer 的区别：
- fee-on-transfer：转账时到账量偏少
- rebasing：余额会随时间或机制主动变化

## 10. privileged misconfiguration

中文：特权角色错误配置

实战理解：
问题成立的前提主要是 owner/admin/keeper/operator 等受信任角色把参数、地址、权限、路由配置错了。

为什么经常降级：
在比赛审计里，很多这类问题不会被认定为 HM/M，因为它依赖：
- trusted role 犯错
- 治理操作错误
- 本应由管理员安全维护的参数被配坏

典型例子：
- owner 把 oracle 地址配错
- admin 把 slippage 配得过大
- governor 配置了恶意 adapter

为什么还是值得记录：
它可能是 QA、操作风险、文档风险，甚至在极端情况下能和别的问题拼接出更强 exploit path。

但默认不要高估它。

## 11. duplicate risk

中文：重复风险 / 与别人撞洞的风险

实战理解：
你发现的问题并不是“你能不能论证”，而是“有没有很多人也很容易想到并提交”。

为什么重要：
比赛里，你不是在写论文，而是在争取奖金。
同样的正确问题，如果撞车严重，实际收益就会下降。

高 duplicate risk 的常见特征：
- 经典模式，表面很明显
- 合约名和函数名已经把风险写脸上了
- 很多人第一轮 checklist 就会扫到
- 不需要深入理解系统交互就能想到

低 duplicate risk 的常见特征：
- 需要跨模块拼接
- 需要理解系统特有 invariant
- 需要时序、角色、状态机一起成立
- 单看某个函数并不明显

这不是技术真假问题，而是比赛策略问题。

## 12. denial of service / DoS

中文：拒绝服务 / 功能不可用

实战理解：
攻击者不一定偷钱，但能让关键路径无法继续执行，导致用户、keeper、清算者或协议本身无法完成重要动作。

常见形式：
- 某个用户状态卡死
- 某个队列永远处理不下去
- 清算、结算、提现、消息投递被永久阻塞
- 单个恶意输入让整个流程 revert

为什么在审计里可能是 Medium：
如果 DoS 打的是协议核心功能，而不是边缘小功能，且能稳定触发、影响面明确，往往具备中危潜力。

## 13. stuck funds

中文：资金卡死 / 资金无法取回

实战理解：
资产没有被偷，但用户或协议无法按预期取出、赎回、转移或结算。

常见场景：
- 提现路径永久失败
- 某种边界状态下资产无法赎回
- 消息桥接后资产无法最终领取
- 资金被送入没有回收路径的地址/状态

严重性判断看什么：
- 是个别用户还是全局
- 是暂时卡住还是永久卡住
- 是否有 admin 救援路径
- 数量和影响范围是否明确

## 14. insolvency

中文：资不抵债 / 系统账面负债大于可覆盖资产

实战理解：
协议欠用户的总价值已经超过它真正能拿出来覆盖的资产。

常见来源：
- 坏账累积
- 错误利率或奖励计算
- 清算失败
- share/accounting 错误长期累积
- 资产估值过高

为什么这是大词：
它往往不是一个“局部 bug”，而是一个系统级后果。
如果一个问题最终导致 insolvency，严重性通常会更敏感。

## 15. access control

中文：访问控制 / 权限控制

实战理解：
系统如何限制“谁能调用什么操作”。

常见审计点：
- onlyOwner / role modifier 是否正确
- 初始化后权限是否正确转移
- 升级权限是否受保护
- 某些敏感函数是否遗漏权限限制

为什么不能只看 modifier：
很多 access control 问题不是“完全没权限控制”，而是：
- 某个间接路径绕过去了
- 角色边界不清
- 一个看似低权限角色实际可影响高价值结果

## 16. authorization vs authentication

中文：
- authentication：身份验证，确认“你是谁”
- authorization：授权控制，确认“你能做什么”

实战理解：
在合约里，大家更常谈 authorization，因为链上身份通常由 msg.sender / signature 等已经给出，真正关键是：
“这个实体有没有被允许执行这件事？”

## 17. domain separation

中文：域隔离 / 作用域隔离

实战理解：
一个签名、消息、授权，必须被限定在某个明确上下文里，例如：
- 某条链
- 某个合约
- 某个版本
- 某个用途

如果缺少 domain separation，就容易 replay：
- 在别的链复用
- 在别的合约复用
- 在别的功能里复用

## 18. nonce

中文：一次性序号 / 防重放计数器

实战理解：
nonce 的本质目的是确保某个授权或动作只能按预期使用一次或按顺序使用。

常见错误：
- nonce 未消费
- nonce 可重复覆盖
- 不同对象共享错误 nonce 空间
- nonce 只检查存在，不检查唯一性

## 19. edge case

中文：边界情况

实战理解：
不是“冷门情况”那么简单，而是“平时大多数流程没问题，但在某个特殊输入、状态、顺序、初始值、极端规模下会出问题”。

审计里常见边界：
- 空池
- 首次存款
- 最后一位用户退出
- 小数精度极小或极大
- 零值 / 一次性极大值
- 过期状态
- 部分完成状态

很多奖励 finding 恰恰就藏在 edge case 里。

## 20. happy path

中文：正常路径 / 理想路径

实战理解：
开发者通常优先测试“用户按预期使用时会不会工作”，这就是 happy path。

而审计真正要看的，是：
- unhappy path
- adversarial path
- edge case path
- cross-function path

也就是说：
代码在 happy path 上表现正常，并不说明它安全。

## 21. griefing

中文：骚扰式攻击 / 让别人难受但不一定直接赚钱

实战理解：
攻击者自己不一定直接获利，但能让别人付出成本、操作失败、资金效率变差、系统流程变卡。

比如：
- 故意制造让某人提现失败的条件
- 让 keeper 多次白跑
- 让消息处理反复 revert

griefing 有时是 QA，有时能上 Medium，取决于影响范围和协议依赖程度。

## 22. atomicity

中文：原子性

实战理解：
一组操作要么全部完成，要么全部不生效。

审计里为什么重要：
如果协议逻辑默认“这些步骤会一起成功”，但现实中中间可能失败、中断或被插入外部调用，就会出现：
- 部分状态已更新
- 另一部分没更新
- 从而引发 desync 或可利用窗口

## 23. external call ordering

中文：外部调用顺序

实战理解：
调用外部合约是高风险动作，因为你把控制权短暂交出去了。

如果在外部调用前后，内部状态更新顺序不当，就可能导致：
- reentrancy
- accounting 不一致
- 回调利用
- 失败后状态残缺

一个常见审计直觉是：
“外部调用发生时，系统是不是已经把自己该更新的状态更新好了？”

## 24. reentrancy

中文：重入

实战理解：
在一次执行尚未完成时，外部合约通过回调等方式重新进入原协议逻辑，利用尚未稳定的中间状态。

常见后果：
- 重复提取
- 重复领取
- 绕过某些一次性假设
- 在 accounting 尚未同步时插入动作

不要把重入只理解成“ETH transfer 回调老问题”，现代协议里它常以更隐蔽的形式出现：
- token hooks
- adapter callback
- cross-contract compose

## 25. settlement

中文：结算

实战理解：
协议把某个临时状态、应付结果、挂起操作，最终落实成实际余额、资产转移、债务变化或消息落地的过程。

结算类问题常见于：
- reward claim
- bridge message delivery
- fee payment
- trade outcome finalization
- liquidation result application

判断重点：
- 结算前后状态是否一致
- 是否存在中途失败但部分完成
- 是否可能被重复结算或永远不结算

## 26. compose / composed flow

中文：组合流程 / 拼接流程

实战理解：
一个问题不是由单个函数直接造成，而是需要两个或多个步骤、模块、状态前后拼起来才成立。

为什么重要：
高质量比赛 finding 往往不是“某一行明显写错”，而是：
- A 函数制造前提
- B 模块放大影响
- C 结算路径最终兑现结果

这类问题通常 duplicate risk 更低，但验证难度更高。

## 27. duplicate vs same root cause

中文：
- duplicate：重复问题
- same root cause：相同根因

实战理解：
不是所有“根因差不多”的点都能算不同 finding。

如果两个问题：
- 依赖同一根因
- 影响高度重合
- 修复方式基本相同
那比赛里常常会被合并或判重复。

所以你在写 finding 前要问：
“这到底是一个新 exploit path，还是同一根因的另一个表象？”

## 28. proof of concept / PoC

中文：概念验证 / 复现验证

实战理解：
PoC 不只是“能跑的代码”，而是“足以说服 judge 这个问题真的能按你说的方式发生”的证据形式。

好的 PoC 通常能证明：
- 前置条件可构造
- 攻击动作可执行
- 结果确实发生
- 影响能被观测到

在很多比赛里，强 PoC 比漂亮措辞更重要。

## 29. validation gap

中文：验证缺口 / 证据缺口

实战理解：
你可能已经有个不错的静态分析直觉，但还没证明最关键的一段。

典型缺口包括：
- 没证明攻击者真能到达那个状态
- 没证明影响真能兑现
- 没排除补偿逻辑
- 没证明不是 trusted-role-only

很多 candidate 不是“完全错”，而是卡在 validation gap 上。

## 30. severity calibration

中文：严重性校准

实战理解：
不是看到“会损失钱”就说 High，也不是看到“只是配置问题”就一律 QA。
而是结合比赛规则和 exploit path，把问题放到合适层级。

你在校准 severity 时，至少要问：
- 攻击者是否 permissionless？
- 影响是直接资金损失，还是功能受阻，还是仅配置风险？
- 能否重复利用？
- 影响范围是个别用户还是系统性？
- 需要多少不现实前提？

## 最后：实战里怎么用这份术语表

你看到一个 candidate 时，可以用下面这套最小问题模板去自检：

1. 这里可能打破了什么 invariant？
2. 根因更像是 accounting、desync、replay，还是 access control？
3. 这是 happy path 外的 edge case，还是核心流程都受影响？
4. 需要 permissionless 攻击者，还是 privileged misconfiguration？
5. 有没有明显 false positive 风险？
6. 缺的到底是思路，还是 validation gap？
7. 这个点 duplicate risk 高不高？

如果你后面愿意，我还可以继续给你补两份很实用的文档：
1. 《Code4rena / Sherlock 严重性判断中文速查表》
2. 《智能合约审计中最常见的 false positive 中文案例集》
