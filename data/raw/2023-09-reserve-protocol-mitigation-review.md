- - - - Reserve Protocol - Mitigation Review Audit | Code4rena- - - Skip Navigation- For Projects
## Ready to secure your project?
The best time to start is now.
Get startedSecurity solutions- Competitive auditWe invented the format that disrupted the web3 industry. Find out why top protocols trust C4.

- ZenithZenith assembles auditors with proven track records to secure your project.

Resources- Docs
- Reports

- For Wardens
## Find bugs. Get paid.
Put your security research skills to work.
Become a WardenAudits- Ongoing audits
- Upcoming audits
- Past audits
- Bounties

Leaderboard- Past 90 days
- Past 365 days
- All time

Resources- Reports
- Help desk
- Docs
- GitHub

- Support
- Log in

## Login
Log in / RegisterGet an audit

# Reserve Protocol - Mitigation Review
A permissionless platform to launch and govern asset-backed stable currencies.
- Start date25 Sep 2023
- End date29 Sep 2023
- Total awards$17,600 USDC
- Duration4 days

- Details

# Reserve - Mitigation Review details

- Total Prize Pool: $17,600 USDC

- Warden guidelines for C4 mitigation reviews

- Submit findings using the C4 form

- Starts September 25, 2023 20:00 UTC

- Ends September 29, 2023 20:00 UTC

## Important note

Each warden must submit a mitigation review for every High and Medium finding from the parent audit that is listed as in-scope for the mitigation review. Incomplete mitigation reviews will not be eligible for awards.

## Findings being mitigated

Mitigations of all High and Medium issues will be considered in-scope, with the following exceptions: M-07, M-10, M-11, M-12, M-13, M-14, and M-15. Please refer to the "Out of scope" section below for details and context on the four acknowledged / out of scope findings.

- H-01: CBEthCollateral and AnkrStakedEthCollateral _underlyingRefPerTok is incorrect

- H-02: CurveVolatileCollateral Collateral status can be manipulated by flashloan attack

- H-03: ConvexStakingWrapper.sol after shutdown，rewards can be steal

- M-01: Upgraded Q -> 2 from #26 [1693915911684]

- M-02: CTokenV3Collateral._underlyingRefPerTok should use the decimals from underlying Comet.

- M-03: RTokenAsset price estimation accounts for margin of error twice

- M-04: Possible rounding during the reward calculation

- M-05: Permanent funds lock in StargateRewardableWrapper

- M-06: CurveStableMetapoolCollateral.tryPrice returns a huge but valid high price when the price oracle of pairedToken is timeout

- M-08: User can't redeem from RToken based on CurveStableRTokenMetapoolCollateral when any underlying collateral of paired RToken's price oracle is offline(timeout)

- M-09: RTokenAsset price oracle can return a huge but valid high price when any underlying collateral's price oracle timeout

### Findings acknowledged and NOT mitigated:

- M-07: The Asset.lotPrice doubles the oracle timeout in the worst case

- M-10: Asset.lotPrice only uses oracleTimeout to determine if the price is stale.

- M-11: StaticATokenLM transfer missing _updateRewards

- M-12: _claimRewardsOnBehalf() User's rewards may be lost

- M-13: Lack of protection when caling CusdcV3Wrapper._withdraw

- M-14: Lack of protection when withdrawing Static Atoken

- M-15: Potential Loss of Rewards During Token Transfers in StaticATokenLM.sol

## Overview of changes

Units and price calculations in LSD collateral types were fixed.

CurveVolatileCollateral was removed entirely.

Decimals fixed in wrapped cUSDCv3.

RToken Asset pricing issues fixed, (0, FIX_MAX) enforced as "unpriced".

Reward remainder held until next claim instead of lost.

## Mitigations to be reviewed

### Branch

https://github.com/reserve-protocol/protocol/tree/master

### Individual PRs

Wherever possible, mitigations should be provided in separate pull requests, one per issue. If that is not possible (e.g. because several audit findings stem from the same core problem), then please link the PR to all relevant issues in your findings repo.

URLMitigation ofPurpose
https://github.com/reserve-protocol/protocol/pull/899H-01Fixes units and price calculations in cbETH, rETH, ankrETH collateral plugins.
https://github.com/reserve-protocol/protocol/pull/896H-02Removes CurveVolatileCollateral.
https://github.com/reserve-protocol/protocol/pull/930H-03Skip reward claim in _checkpoint if shutdown.
https://github.com/reserve-protocol/protocol/pull/896M-01Removes CurveVolatileCollateral.
https://github.com/reserve-protocol/protocol/pull/889M-02Use decimals from underlying Comet.
https://github.com/reserve-protocol/protocol/pull/916M-03Acknowledged and documented.
https://github.com/reserve-protocol/protocol/pull/896M-04Roll over remainder to next call.
https://github.com/reserve-protocol/protocol/pull/896M-05Add call to emergencyWithdraw.
https://github.com/reserve-protocol/protocol/pull/917M-06Enforce (0, FIX_MAX) as "unpriced" during oracle timeout.
https://github.com/reserve-protocol/protocol/pull/917M-08Unpriced on oracle timeout.
https://github.com/reserve-protocol/protocol/pull/917M-09Enforce (0, FIX_MAX) as "unpriced" during oracle timeout.

## Out of Scope

URLMitigation ofPurpose
M-07Acknowledged. See details in comment https://github.com/code-423n4/2023-07-reserve-findings/issues/24#issuecomment-1670250237
https://github.com/reserve-protocol/protocol/pull/896M-10Acknowledged, documented.
https://github.com/reserve-protocol/protocol/pull/920M-11Acknowledged. Details in comment https://github.com/code-423n4/2023-07-reserve-findings/issues/12#issuecomment-1695841823
https://github.com/reserve-protocol/protocol/pull/920M-12Acknowledged. Details in comment https://github.com/code-423n4/2023-07-reserve-findings/issues/10#issuecomment-1701397555
M-13Acknowledged. Details in comment https://github.com/code-423n4/2023-07-reserve-findings/issues/8#issuecomment-1688439465
M-14Acknowledged. Details in comment https://github.com/code-423n4/2023-07-reserve-findings/issues/7#issuecomment-1695796001
M-15Acknowledged. Details in comment https://github.com/code-423n4/2023-07-reserve-findings/issues/4#issuecomment-1695841054

- Twitter
- Discord
- GitHub
- Media kit
- Terms
- Privacy
