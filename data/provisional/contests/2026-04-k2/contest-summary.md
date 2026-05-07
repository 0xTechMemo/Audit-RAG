# Contest Summary: 2026-04-k2

Generated: 2026-05-07T03:48:03+00:00

## Status counts

- `duplicate`: 7
- `false-positive`: 3
- `investigating`: 3

## Leads

| id | status | severity | component | title | blocker / note |
|---|---:|---:|---|---|---|
| `atoken-transfers-bypass-pool-reserve-pause-and-inactive-state` | duplicate | medium | a-token-transfer-emergency-state | aToken transfers bypass pool/reserve pause and inactive state | Suppressed as validated duplicate of V12 High 'Collateral can be enabled despite pause/freeze or invalid pricing'. Local |
| `flash-liquidation-callback-transfers-debt-asset-without-self-authorization` | duplicate | unclear | flash-liquidation-auth | flash liquidation callback transfers debt asset without self authorization | Suppressed by known signature 'missing self authorization breaks cross contract protocol flows' plus adjacent flash liqu |
| `token-allowance-storage-ttl-shorter-than-expiration-ledger` | duplicate | unclear | token-ttl-allowance | token allowance storage ttl shorter than expiration ledger | Cold TTL lead is real as a storage/expiration mismatch pattern across Token/AToken allowance keys, but K2 known signatur |
| `public-refresh-prices-can-evict-oracle-cache-before-reverting` | false-positive | unclear | oracle-cache-ttl | public refresh_prices can evict oracle cache before reverting | refresh_prices is public and clears LastPriceData before refetch, but failed Soroban invocations roll back storage write |
| `public-update-reserve-state-can-choose-reserve-compounding-cadence` | duplicate | unclear | router-public-mutator-interest-accounting | public update_reserve_state can choose reserve compounding cadence | V12 Med/Low line ~45018 explicitly covers public update_reserve_state path-dependent compounding cadence; not novel. |
| `get-protocol-reserves-reverts-when-total-debt-exceeds-total-supply` | duplicate | unclear | reserve-deficit-treasury-accounting | get_protocol_reserves reverts when total debt exceeds total supply | V12 Med/Low line ~12070/~13547 explicitly covers false total_borrow <= total_supply invariant in get_protocol_reserves/c |
| `account-data-skips-active-config-positions-when-reserve-id-lookup-is-missing` | duplicate | unclear | account-data-user-config-ttl | account data skips active config positions when reserve id lookup is missing | V12 Critical covers calculate_user_account_data_unified trusting TTL-managed user_config/reserve counter/default-zero st |
| `external-report-sweep-smoke-stale-solvency-transfer` | investigating | medium | stellar-soroban-lending-protocol | external report sweep smoke: stale solvency transfer | 需要用当前目标仓库代码验证 reachability、权限边界和资产影响，不能只依赖历史相似案例; 需要排除 caution/false-positive 通道召回的降级条件 |
| `liquidation-engine-ignores-receive-a-token-and-has-helper-parity-drift` | duplicate | unclear | liquidation-engine-parity | liquidation engine ignores receive_a_token and has helper parity drift | Static review found real-looking parity drift, but no fresh HM path yet: LiquidationEngineContract::execute_liquidation  |
| `swap-collateral-can-add-a-destination-collateral-bit-without-max-user-reserves-c` | investigating | unclear | swap-collateral-user-config | swap_collateral can add a destination collateral bit without MAX_USER_RESERVES check | Confirmed after re-triage/suppress-check: static MAX_USER_RESERVES guard gap is real, but suppress-check still recommend |
| `hook-callback-transitional-state-in-flash-loan-paths-appears-covered-by-router-l` | false-positive | none | flash-loan-callback-ordering | Hook/callback transitional state in flash loan paths appears covered by router lock |  |
| `prepared-liquidations-can-execute-against-a-collateral-reserve-paused-after-auth` | investigating | medium | flash-liquidation-reserve-lifecycle | Prepared liquidations can execute against a collateral reserve paused after authorization | PoC validated. Main remaining risk is duplicate framing: closest known signatures are 'liquidation flow bypasses reserve |
| `fake-configured-incentives-asset-can-mint-and-drain-funded-rewards` | false-positive | medium | incentives-reward-accounting | Fake configured incentives asset can mint and drain funded rewards | Local fake-asset PoC demonstrates reward drain only after emission_manager configures attacker-controlled asset, or afte |

## Files

- ledger: `/Users/qwe/Audit/audit-rag/data/provisional/contests/2026-04-k2/lead-ledger.jsonl`
- rag triage dir: `/Users/qwe/Audit/audit-rag/data/provisional/contests/2026-04-k2/rag-triage`
