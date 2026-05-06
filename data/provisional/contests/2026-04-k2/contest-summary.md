# Contest Summary: 2026-04-k2

Generated: 2026-05-05T15:08:52+00:00

## Status counts

- `duplicate`: 6
- `false-positive`: 1

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

## Files

- ledger: `/Users/qwe/Audit/audit-rag/data/provisional/contests/2026-04-k2/lead-ledger.jsonl`
- rag triage dir: `/Users/qwe/Audit/audit-rag/data/provisional/contests/2026-04-k2/rag-triage`
