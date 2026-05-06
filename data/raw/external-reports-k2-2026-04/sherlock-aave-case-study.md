Sherlock — Securing Aave V4: A New Architecture Demands a New Security Standard
(/)
(/)
Solutions
Sherlock AI
AI-powered smart contract analysis
(/solutions/ai)
Collaborative Audits
Multi-auditor review, led by a senior judge
(/solutions/collaborative-audits)
Audit Contests
Large-scale adversarial review before launch
(/solutions/audit-contests)
Bug Bounties
Ongoing vulnerability discovery post-launch
(/solutions/bug-bounties)
Sherlock Shield
Exploit coverage for live protocols
(/solutions/sherlock-shield)
Learn
Blog
News, updates, and insights on Web3 security
(/blog)
Podcast
Conversations with leaders shaping Web3 security
(/podcast)
Company
About
Why Sherlock exists and how we operate
(/about)
Docs
Technical documentation for builders and researchers
(https://docs.sherlock.xyz/)
Case Studies
How teams secured major releases with Sherlock
(/case-studies)
Brand Kit
Official Sherlock assets and brand guidelines
(/brand-kit)
Active Contests & Bounties
Leaderboards
Researcher rankings across audits and contests
(https://audits.sherlock.xyz/leaderboards)
Active Audit Contests
Open contests currently accepting submissions
(https://audits.sherlock.xyz/contests)
Active Bug Bounties
Live bounty programs for deployed protocols
(https://audits.sherlock.xyz/bug-bounties)
Contact
(/contact)
Contact Our Team
(/contact)
Case Study
# Securing Aave V4: A New Architecture Demands a New Security Standard
11
Collaborative Audit Findings
930+
Audit Contest Participants
Case Study
# Securing Aave V4: A New Architecture Demands a New Security Standard
11
Collaborative Audit Findings
930+
Audit Contest Participants
Table of Content
Text Link (#)
Aave partnered with Sherlock across the security lifecycle, from deep pre-launch review to live post-launch protection.
About Aave
Aave (https://aave.com/) is one of the foundational protocols in decentralized finance. First introduced in 2017 as EthLend, it grew from an early peer-to-peer lending concept into the category-defining lending and borrowing infrastructure now used across Ethereum and more than a dozen other chains. Users can supply assets to earn yield, borrow against collateral, and access flash loans, while governance remains in the hands of AAVE token holders. At any given time, the protocol is responsible for tens of billions of dollars in active TVL.
As one of the most forked, most studied, and most battle-tested protocols in DeFi, Aave sets a standard. That standard raises the bar for how any new version must be reviewed.
"Aave has always implemented industry-leading security standards. V4 is designed to bring trillions of dollars and millions of users onchain, so continuing to meet those standards was not negotiable. Sherlock's collaborative audit provided a deep review from a specialized team, and the public contest that followed confirmed their work was effective."
Stani Kulechov
Founder and CEO of Aave Labs
## V4: A Different Kind of Upgrade
The V4 upgrade (https://aave.com/blog/understanding-aave-v4s-architecture) fundamentally reorganizes how Aave manages liquidity, risk, and protocol governance.
### Hub and Spoke Architecture
The core change replaces V3's market-per-pool design with a unified Liquidity Hub. Where V3 fragmented liquidity across isolated pools on the same chain, V4 routes all liquidity through a central Hub. Spokes connect to the Hub as modular borrowing environments, each with its own risk configuration, oracle setup, and emergency controls, but drawing from and supplying to a shared liquidity source. New Spokes can be added or upgraded without migrating liquidity or disrupting existing markets.
### Risk Premiums
V4 introduces per-user borrowing surcharges tied to collateral quality. Users with safer collateral pay less. This creates a more efficient market where borrow rates reflect actual risk rather than treating all collateral as equivalent, and introduces a new category of security surface with no prior precedent in Aave's codebase.
### Redesigned Liquidations
The liquidation engine now operates around a Target Health Factor model: liquidators repay only enough debt to restore a position to a target health level, preventing over-liquidation. A Variable Liquidation Bonus scales with position health, creating an incentive structure that prioritizes the riskiest positions first.
These changes make V4 a significantly more complex system than its predecessor. The Hub sits at the center of protocol-wide accounting, meaning its internal invariants carry more weight than any equivalent component in V3. Any issue in Hub logic, around interest accrual, share pricing, or the credit and debit mechanics between Hub and Spokes, has broad surface area.
## Where the Risk Actually Lives
Aave Labs treated V4's security as a layered problem from the start. Following an initial audit with Trail of Bits, they brought Sherlock in to go deeper on the parts of V4 that were genuinely novel: the failure modes specific to the Hub and Spoke model, and a risk premium system that had no precedent anywhere in the codebase.
The highest-risk areas were the ones unique to V4's design. The Hub sits at the center of protocol-wide accounting, meaning failures here affect all depositors simultaneously rather than being contained to a single market. The risk premium system was entirely new to Aave, with no battle-tested precedent to draw from. And the Hub-Spoke relationship introduced a new class of isolation questions that didn't exist in V3's architecture.
Hub accounting invariants. Any violation of share pricing invariants, for example the exchange rate decreasing when it should only stay constant or increase, could affect all depositors at once.
Risk premium mechanics. Any manipulation of premium accrual, through rounding, repeated state updates, or interaction with low-decimal assets, could be exploited to inflate collateral value or shift losses onto other depositors.
Hub-Spoke isolation. The question was whether cap and allowance controls held under adversarial composition, specifically whether a malicious Spoke could extract funds from users who had granted allowance to the Hub by cycling through the add and remove mechanism.
## Built for This Kind of Problem
V4's architecture required auditors who could reason about the system as a whole rather than check contracts in isolation. The Hub and Spoke design means that safe-looking behavior in a single component can produce dangerous outcomes when composed with others.
Sherlock's collaborative audit model is built for exactly this. Rather than fixed rosters, each engagement is staffed from an elite researcher network whose members have demonstrated performance across live audits, contests, and bug bounties. That track record allows Sherlock to match researchers to the specific architecture being reviewed, so the team reflects the system itself rather than availability.
For Aave V4, Sherlock assembled five researchers from Blackthorn, its most senior audit tier, chosen for their depth on complex financial systems: lending protocols, vault accounting, and multi-component DeFi infrastructure.
## The Collaborative Audit
The engagement ran from October 6 to October 20, 2025. The team used a system-first approach: understand how the protocol is supposed to behave, then find where it bends. Scope covered Hub logic, Spoke architecture, oracle integration, liquidation paths, position management, and the full risk premium pipeline.
## The Researchers
0x52 -- Ranked #1 on Sherlock's contest leaderboard with over $1.36M earned from public audits. Led the review and multiple prior Sherlock engagements. A founding Blackthorn member.
Deadrosesxyz -- One of the most experienced researchers working on DeFi accounting manipulation. Focused on the risk premium system and Hub accounting edge cases. A founding Blackthorn member.
mstpr-brainbot -- Fundamentally adversarial in his approach to financial protocol design. On this engagement that meant stress-testing liquidation paths and capital flow between Hub and Spokes. A founding Blackthorn member.
pkqs90 -- Focused on configuration controls, cap enforcement, and Spoke isolation. Known for finding permission and access control issues that other reviewers miss. A founding Blackthorn member.
xiaoming90 -- Focused on withdrawal and redemption paths and edge cases affecting user exits. Over $1M earned from public audits. A founding Blackthorn member.
## What the Audit Found
All 11 findings were either fixed or formally acknowledged by the Aave Labs team before the public contest began.
## A Closer Look at the Findings
The audit surfaced 11 findings across the codebase. None were critical, none were high. The most instructive was a Medium — a rounding exploit that illustrated exactly why V4's novel mechanics required this level of scrutiny.
The vulnerability lived in the updateUserRiskPremium() function, callable by anyone at roughly 63,000 gas per execution. Each call inflated the premium debt of the Hub asset, the Spoke reserve, and the user position by up to 2 wei due to the internal rounding direction of premium calculations. Against a high-value, low-decimal asset — a 5-decimal BTC derivative worth $100,000 per unit where 1 wei equals $1 — the economics become exploitable. A malicious actor holding 5% of total supply shares could call the function 100,000 times for roughly $55 in gas fees and extract approximately $5,000 in value from other depositors, collapsing their own health factor to 0.13 and leaving bad debt for the umbrella Spoke to absorb.
That finding emerged directly from V4's new risk premium system - code that had never existed in production before. It's exactly the kind of issue that only surfaces when the right researchers are specifically looking for it. Aave Labs resolved it by storing premium with full ray precision, eliminating the rounding delta entirely.
## The Audit Contest: 936 Researchers, 1 Goal
With all actionable findings addressed, the codebase moved into a public contest - the most intensive adversarial check V4 would face before launch. Nearly a thousand independent researchers competed for real stakes against a system that had already been through Trail of Bits and Sherlock's most senior team.
The contest ran from December 1, 2025 through January 12, 2026, extended two weeks from its original close date to maximize coverage of a system with novel architecture and no direct precedent in production DeFi. The prize pool was $365,000 USDC.
Lead Senior Watson: 0xSimao -- Ranked top 3 on Sherlock's contest leaderboard and Sherlock's 2025 Watson of the Year.
Lead Judge: 0x52 -- The same researcher who led the collaborative audit, bringing direct continuity from the private phase into public contest judging.
The purpose of running a public contest after a rigorous private audit is not to find what the elite team missed. It is to confirm they didn't miss anything. 936 researchers put V4 under a microscope for six weeks, and after full judging of every submission, no valid findings emerged.
For a protocol of Aave's scale, that is exactly the point.
## Ongoing Security: $500k Bug Bounty Protection After Launch
With V4 now live, Aave’s work with Sherlock continues through a live bug bounty program offering up to $500K for valid findings. This extends the engagement into the post-launch phase, where real usage, new integrations, and live market conditions can surface issues that are hard to catch earlier.
That matters for V4 because Aave introduced a new architectural foundation that now has to perform under production conditions. The bug bounty keeps experienced researchers focused on the live system and gives Aave a clear path for responsible disclosure if new issues are found after launch. Security review now continues alongside the protocol itself as V4 operates in the wild.
The Aave V4 bug bounty can be accessed here. (https://audits.sherlock.xyz/bug-bounties/300)
## What This Engagement Represents
Aave V4 is a generational change to how the protocol handles liquidity and risk. Its new architecture creates a more efficient and more composable system, but also raises the security bar. For an upgrade of this significance, Aave Labs needed a security process that could match the complexity of the system from pre-launch review through live deployment.
That is what this engagement represents: not a one-time audit, but a layered security effort that carried from deep specialist review, to broad adversarial validation, to ongoing live protection. For a protocol of Aave’s scale, that is the standard.
(/case-studies/aave)
(/case-studies/centrifuge)
(/case-studies/morpho)
(/case-studies/ethereumfoundation)
(/case-studies/perennial)
(/case-studies/autofinance)
Aave is a decentralised, non-custodial liquidity protocol where users can supply assets to earn interest and borrow against collateral. The protocol also supports advanced functionality like flash loans and is deployed across multiple blockchain networks.
Categories
• DeFi Lending
• Multi-Chain Protocol
• Smart Contract Security
Services & Solutions
• Earn on Deposits
• Borrow Against Collateral
• Access flash loans
• Mint GHO stablecoin
Learn More
(https://aave.com/)
## Secure Your Protocol with sherlock
Sherlock delivers complete lifecycle security, from early development to protection on live code. Tell us what stage you’re in and we’ll help you from there.
Contact Our Team
(/contact)
Products
Collaborative Audits
(/solutions/collaborative-audits)
Audit Contests
(/solutions/audit-contests)
Bug Bounties
(/solutions/bug-bounties)
Sherlock AI
(/solutions/ai)
Sherlock Shield
(/solutions/sherlock-shield)
Live Security
Leaderboards
(https://audits.sherlock.xyz/leaderboards)
App
(https://app.sherlock.xyz/overview)
Live Audits
(https://audits.sherlock.xyz/contests)
Live Bug Bounties
(https://audits.sherlock.xyz/bug-bounties)
Resources
Blog
(/blog)
Docs
(https://docs.sherlock.xyz/)
Brand Kit
(/brand-kit)
Lifecycle eBook
(/lifecycle-ebook)
Referral Program
(/referral-program)
Sherlock secures Web3 protocols across development, launch, and live operation through a unified lifecycle security model.
Sherlock’s services do not constitute a guarantee against all security incidents or losses. Responsibility for protocol operation and risk management remains with the protocol team.
Follow Us On
(https://twitter.com/sherlockdefi)
(https://www.linkedin.com/company/sherlock-protocol/)
(https://discord.com/invite/MABEWyASkp)
(https://github.com/sherlock-protocol/)
Copyright © Sherlock Protocol 2026. All Rights Reserved.