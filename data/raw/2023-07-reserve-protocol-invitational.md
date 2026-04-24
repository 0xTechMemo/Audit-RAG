- - - - Reserve Protocol - Invitational Audit | Code4rena- - - Skip Navigation- For Projects
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

# Reserve Protocol - Invitational
A permissionless platform to launch and govern asset-backed stable currencies.
View report- Start date25 Jul 2023
- End date4 Aug 2023
- Total awards$80,100 USDC
- Duration10 days

- Details

# Reserve Invitational audit details

- Total Prize Pool: $80,100 USDC

- HM awards: $45,000 USDC

- Analysis awards: $2,500 USDC

- QA awards: $1,250 USDC

- Gas awards: $1,250 USDC

- Judge awards: $12,000 USDC

- Scout awards: $500 USDC

- Mitigation Review: $17,600 USDC (Opportunity goes to top 3 certified wardens based on placement in this audit.)

- Join C4 Discord to register

- Submit findings using the C4 form

- Read our guidelines for more details

- Starts July 25, 2023 20:00 UTC

- Ends August 4, 2023 20:00 UTC

## Automated Findings / Publicly Known Issues

Automated findings output for the audit can be found here within 24 hours of audit opening.

Note for C4 wardens: Anything included in the automated findings output is considered a publicly known issue and is ineligible for awards.

Anything mentioned in the previous audits is considered known issues:

- Trail of Bits - August 11th, 2022

- Ackee - October 7th, 2022

- Solidified - October 16th, 2022

- Halborn Security - November 15th, 2022

- Code4rena Competition January, 2023

- Code4rena Competition January, 2023 - Mitigation

# Overview

The Reserve Protocol allows anyone to create stablecoins backed by baskets of ERC20 tokens on Ethereum. Stable asset backed currencies launched on the Reserve protocol are called “RTokens”.

Once an RToken configuration has been deployed, RTokens can be minted by depositing the entire basket of collateral backing tokens, and redeemed for the entire basket as well. Thus, an RToken will tend to trade at the market value of the entire basket that backs it, as any lower or higher price could be arbitraged.

RTokens can be overcollateralized, which means that if any of their collateral tokens default, there's a pool of value available to make up for the loss. RToken overcollateralization is provided by Reserve Rights (RSR) holders, who may choose to stake their RSR on any RToken. Staked RSR can be seized in the case of a collateral default, in a process that is entirely mechanistic based on on-chain price-feeds, and does not depend on any governance votes or human choices.

RTokens can generate revenue, and this revenue is the incentive for RSR holders to stake. Revenue can come from yield from lending collateral tokens on-chain or revenue shares with collateral token issuers. Governance can direct any portion of revenue to RSR stakers, to incentivize RSR holders to stake and provide overcollateralization. If an RToken generates no revenue, or if none of it is directed to RSR stakers, it probably won't have any RSR staked on it, and thus won't be protected by overcollateralization.

Introduction Video

The protocol folder in this repo is linked to the primary Reserve Protocol public repo on branch 3.0.0 at commit hash 9ee60f142f9f5c1fe8bc50eef915cf33124a534f: https://github.com/reserve-protocol/protocol/tree/3.0.0

# Scope

See scope.txt

The base directory is assumed to be protocol relative to the root of this repo.

The following directories and implementations are considered in-scope for this audit.

ContractPurpose
contracts/plugins/assets/**These are the collateral plugins for the protocol

Details on collateral plugins can be found here.

## Out of scope

Any `/test`, `/mock`, `/mocks`, `/vendor` folders (including those found under `contracts/plugins/assets/**`).

Everything Else

# Additional Context

Here's a video walkthrough of the code which provides additional context around specific files, structure and logic.

We recommend going through the following documents in order to understand the protocol better.

- docs/system-design.md

- docs/collateral.md

- docs/Token Flow.png

- docs/solidity-style.md

- Especially the section on Fixed.sol which describes our uint192 based fixed-point decimal value.

Some areas of focus for this competition:

- Can the price or status of any plugins be manipulated or exploited?

- Can any token wrappers (CTokenWrapper, CusdcV3Wrapper, PoolTokens, CurveGaugeWrapper, RewardableERC20*, RewardableERC4626Vault) be manipulated or exploited?

# Initialing the Repo

Clone the repo with the following command:

`git clone --recurse-submodules https://github.com/code-423n4/2023-07-reserve.git
`

If you've already cloned the repo but without the --recurse-submodules, you can run the following in the repo's directory:

`git submodule update --init
`

## Tests

Detailed steps to run tests against the protocol are available here in the docs/dev-env.md document:

- Compile: `yarn compile`

- There are many available test sets. A few of the most useful are:

- Run collateral plugin tests: `yarn test:plugins:integration`

## Scoping Details

`- If you have a public code repo, please share it here: https://github.com/reserve-protocol/protocol/tree/3.0.0
- How many contracts are in scope?: 40
- Total SLoC for these contracts?: 3170
- How many external imports are there?: 40
- How many separate interfaces and struct definitions are there for the contracts within scope?: 12
- Does most of your code generally use composition or inheritance?: Inheritance
- How many external calls?: 30
- What is the overall line coverage percentage provided by your tests?: 98%
- Is this an upgrade of an existing system?: Yes, new collateral plugins
- Check all that apply (e.g. timelock, NFT, AMM, ERC20, rollups, etc.): ERC-20 Token
- Is there a need to understand a separate part of the codebase / get context in order to audit this part of the protocol?: Yes
- Please describe required context: It is helpful to understand the rest of the core protocol and how it interacts with the asset/collateral plugins, especially the asset registry, the backing manager, and the basket handler.
- Does it use an oracle?: Chainlink
- Describe any novel or unique curve logic or mathematical models your code uses: Details on our collateral unit abstract model can be found here https://github.com/reserve-protocol/protocol/blob/3.0.0/docs/collateral.md
- Is this either a fork of or an alternate implementation of another project?: No
- Does it use a side-chain?: No
- Describe any specific areas you would like addressed: convex wrapper and plugins. compound v3 wrapper and plugin. frax-eth plugin. lido plugin. rocket-eth plugin. ankr plugin. RewardableERC20Wrapper & CTokenWrapper. sDAI plugin. cbETH plugin. morpho plugin. crv plugins. stargate plugin.
`
- Twitter
- Discord
- GitHub
- Media kit
- Terms
- Privacy
