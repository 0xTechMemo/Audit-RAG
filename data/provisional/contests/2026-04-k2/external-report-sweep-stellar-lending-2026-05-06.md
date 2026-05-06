# K2 external report sweep — Stellar/Soroban + lending analogies (2026-05-06)

Sources saved under `data/raw/external-reports-k2-2026-04/`:
- Code4rena Reflector V3 final report: `c4-2025-10-reflector-v3-report.md`
- Code4rena Silo/Wise/Frax/Venus pages: `c4-*.md`
- Sherlock Aave case study: `sherlock-aave-case-study.md`
- Silo v3 public audit PDFs extracted under `silo-contracts-v3-audits/*.txt`

## K2-priority leads to map back to code

1. require_auth matrix for every public entrypoint
   - Reflector H-01 shows a config mutation entrypoint missing admin authorization.
   - K2 action: enumerate `pub fn` and classify as value-moving/config-mutating/view. For each state mutation, bind `Address.require_auth` to the exact account/admin whose state is consumed.

2. Oracle latest/partial-update semantics
   - Reflector M-05: latest cross-price used a global timestamp, not pair-complete timestamp.
   - K2 action: if K2 consumes Stellar oracle data, test complete pair at t1 + partial update at t2; borrow/liquidation must not consume None/stale/incomplete prices.

3. TTL / vector length / panic DoS
   - Reflector M-02: asset list and expiration vector diverged, `extend_ttl()` panicked.
   - K2 action: inspect all Vec/Map parallel arrays and storage TTL extension code. Zero/default values and added reserves must not cause panic or state expiry.

4. Stale solvency config after transfer/repay
   - Silo v3 continuous audit Medium: stale `borrowerCollateralSilo` after repay + debt transfer corrupted solvency config.
   - K2 action: re-open the existing aToken/debt-token transfer lead. Distinguish authoritative position enumeration from helper/cache inputs. If transfer is allowed, test repay -> transfer-in -> borrow/withdraw/liquidation.

5. Hook/callback transitional state
   - Silo Certora H-01: hook location after checks but before final state allowed reentrant drain with legitimate hooks.
   - K2 action: audit flash-loan callbacks, token hooks, custom account auth, compose/delivery callbacks, and any external invocation between check and final transfer. Revalidate after callback.

6. Alternate liquidation/defaulting path parity
   - Silo/Frax/Venus/Wise reports repeatedly surface liquidation path divergence, stale interest/price, dust repay DoS, bad-debt accounting, and unprofitable liquidator edge cases.
   - K2 action: compare normal borrow/withdraw/liquidate vs flash-loan/default/alternate repay/transfer paths for pool status, interest accrual, price freshness, reward update, close-factor and rounding.

## Retrieval records added

Case reports:
- `c4-2025-10-reflector-v3-h-01`
- `c4-2025-10-reflector-v3-m-02`
- `c4-2025-10-reflector-v3-m-05`
- `public-silo-v3-certora-h-01-hook-location-reentrancy`
- `public-silo-v3-continuous-m-01-stale-collateral-silo`
- `public-silo-v3-continuous-m-02-dynamic-oracle-calldata`

Patterns / checklist / recipe:
- `hook-callback-transitional-state-reentrancy-pattern`
- `lending-stale-solvency-config-transfer-pattern`
- `oracle-partial-update-latest-price-pattern`
- `k2-soroban-lending-external-report-checklist`
- `soroban-lending-transfer-solvency-cache-recipe`
- `liquidation-rounding-minimal-collateral-low-fp-01`

Use these as navigation only. A K2 submission still needs in-scope code link, local PoC, duplicate/V12 suppression check, and severity calibration.
