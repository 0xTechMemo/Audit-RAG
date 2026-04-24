# 标签体系说明（tag-taxonomy）

## 目的

标签是检索、过滤、重排、误报抑制的控制面。

标签体系要满足：
- 稳定
- 简洁
- 可解释
- 便于长期维护

不要把标签做成随手起名的临时备注。

## 1. 根因标签（root-cause tags）

- `auth-bypass`
- `state-desync`
- `rounding`
- `stale-data`
- `replay`
- `missing-validation`
- `unsafe-external-call`
- `token-assumption-mismatch`
- `init-bug`
- `storage-collision`

规则：
根因标签描述的是“为什么会出问题”，而不是“最后造成了什么结果”。

## 2. 组件标签（component tags）

- `vault`
- `erc4626-vault`
- `staking`
- `reward-distribution`
- `lending`
- `router`
- `oracle`
- `bridge`
- `messaging`
- `governance`
- `auction`
- `upgradeability`

规则：
尽量用最具体且合理的组件标签，不要同时打一堆模糊同义词。

## 3. 影响标签（impact tags）

- `direct-theft`
- `value-leakage`
- `unfair-allocation`
- `accounting-corruption`
- `insolvency`
- `dos`
- `stuck-funds`

规则：
影响标签描述协议层后果，不只是代码层 smell。

## 4. 严重性上下文标签（severity-context tags）

- `permissionless`
- `privileged-only`
- `misconfiguration-only`
- `user-mistake-dependent`
- `repeatable`
- `integration-only`
- `requires-special-token`

规则：
这些标签不是 severity 本身，而是影响 severity 判断的重要上下文。

## 5. 验证状态标签（validation-status tags）

- `public-validated`
- `locally-validated`
- `theory-only`
- `disputed`

规则：
这组标签影响“可信度权重”，不直接替代 exploitability 判断。

## 命名规则

1. 使用小写 kebab-case。
2. 标签只放稳定概念，不放长句子。
3. 优先复用已有标签，不轻易创造新变体。
4. 如果两个标签含义重叠，优先保留更接近根因的那个。
5. 比赛专属或协议专属内容，尽量放进 `contest_note`，不要污染全局标签。
