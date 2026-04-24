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
- Start date15 Aug 2023
- End date22 Aug 2023
- Total awards$17,600 USDC
- Duration7 days

- Details

# Reserve - Mitigation Review details

- Total Prize Pool: $17,600 USDC

- Warden guidelines for C4 mitigation reviews

- Submit findings using the C4 form

- Starts August 15, 2023 20:00 UTC

- Ends August 22, 2023 20:00 UTC

## Important note

Each warden must submit a mitigation review for every High and Medium finding from the parent audit that is listed as in-scope for the mitigation review.

Incomplete mitigation reviews will not be eligible for awards.

## Findings being mitigated

Mitigations of all High and Medium issues will be considered in-scope and listed here.

- H-01: Custom redemption might revert if old assets were unregistered

- H-02: A new era might be triggered despite a significant value being held in the previous era

- M-01: A Dutch trade could end up with an unintended lower closing price #48

- M-02: The broker should not be fully disabled by GnosisTrade.reportViolation

- M-03: In case Distributor.setDistribution use, revenue from rToken RevenueTrader and rsr token RevenueTrader should be distributed

- M-04: FurnaceP1.setRatio will work incorrect after call when frozen

- M-06: Oracle timeout at rebalance will result in a sell-off of all RSRs at 0 price

- M-07: sell reward rTokens at low price because of skiping furnace.melt

- M-08: stake before unfreeze can take away most of rsr rewards in the freeze period

- M-09: cancelUnstake lack payoutRewards before mint shares

- M-10: An oracle deprecation might lead the protocol to sell assets for a low price

- M-11: Attacker can disable basket during un-registration, which can cause an unnecessary trade in some cases

## Mitigations to be reviewed

### Branch

https://github.com/reserve-protocol/protocol/pull/882 (commit hash 99d9db72e04db29f8e80e50a78b16a0b475d79f3)

### Individual PRs

Wherever possible, mitigations should be provided in separate pull requests, one per issue. If that is not possible (e.g. because several audit findings stem from the same core problem), then please link the PR to all relevant issues in your findings repo.

URLMitigation ofPurpose
https://github.com/reserve-protocol/protocol/pull/857H-01Fix redeemCustom
https://github.com/reserve-protocol/protocol/pull/888H-02Adds governance function to manually push the era forward
https://github.com/reserve-protocol/protocol/pull/876M-01Allow settle trade when paused or frozen
https://github.com/reserve-protocol/protocol/pull/873 https://github.com/reserve-protocol/protocol/pull/869M-02Disable dutch auctions on a per-collateral basis, use 4-step dutch trade curve
https://github.com/reserve-protocol/protocol/pull/878M-03Distribute revenue in setDistribution
https://github.com/reserve-protocol/protocol/pull/885M-04Update payout variables if melt fails during setRatio
https://github.com/reserve-protocol/protocol-private/pull/15M-06Use lotPrice()
https://github.com/reserve-protocol/protocol-private/pull/7M-07Refresh before selling rewards, refactor revenue & distro
https://github.com/reserve-protocol/protocol/pull/857M-08payoutRewards before freeze and update payoutLastPaid before unfreeze
https://github.com/reserve-protocol/protocol-private/pull/3M-09Payout rewards during cancelUnstake
https://github.com/reserve-protocol/protocol/pull/886M-10Add oracle deprecation check
https://github.com/reserve-protocol/protocol/pull/857M-11Change gas reservation policy in AssetRegistry

## Out of Scope

- M-05: Lack of claimRewards when manageToken in RevenueTrader

- M-12: Custom redemption can be used to get more than RToken value, when an upwards depeg occurs

- Twitter
- Discord
- GitHub
- Media kit
- Terms
- Privacy
