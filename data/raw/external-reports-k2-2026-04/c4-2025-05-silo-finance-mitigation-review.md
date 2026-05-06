Silo Finance Mitigation Review Audit | Code4rena
Skip Navigation (#skip-link) (/)
For Projects
## Ready to secure your project?
The best time to start is now.
Get started
(https://go.code4rena.com/start?source=header-nav)
Security solutions
Competitive audit
We invented the format that disrupted the web3 industry. Find out why top protocols trust C4.
(/competitive-audit)
Zenith
Zenith assembles auditors with proven track records to secure your project.
(/zenith)
Resources
Docs
(https://docs.code4rena.com)
Reports
(/reports)
For Wardens
## Find bugs. Get paid.
Put your security research skills to work.
Become a Warden
(/register/account)
Audits
Ongoing audits
(/audits#active-audits)
Upcoming audits
(/audits#upcoming-audits)
Past audits
(/audits#completed-audits)
Bounties
(/bounties)
Leaderboard
Past 90 days
(/leaderboard?timeframe=Last 90 days)
Past 365 days
(/leaderboard?timeframe=Last 365 days)
All time
(/leaderboard?timeframe=All time)
Resources
Reports
(/reports)
Help desk
(/help)
Docs
(https://docs.code4rena.com)
GitHub
(https://github.com/code-423n4/)
Support (/help)
Log in (/login)
## Login
Log in / Register (/login)
Get an audit
(https://go.code4rena.com/start?source=header-nav)
(/)
Completed
(https://twitter.com/SiloFinance)
# Silo Finance Mitigation Review
Isolated lending markets on Ethereum.
View dashboard (/audits/2025-05-silo-finance-mitigation-review/dashboard)
Start date 1 May 2025
End date 5 May 2025
Total awards $8,000 in USDC
Duration 4 days
Details
# Silo Finance Mitigation Review
Total Prize Pool: $8,000 in USDC
Warden awards: $6,800 in USDC
Judge awards: $950 in USDC
Scout awards: $250 in USDC
Warden guidelines for C4 mitigation reviews (https://code4rena.notion.site/Guidelines-for-C4-mitigation-reviews-ed10fc5cfbf640bd8dcec66f38b343c4)
Starts May 01, 2025 20:00 UTC
Ends May 05, 2025 20:00 UTC
## Important note
Each warden must submit a mitigation review for every individual item listed in the `Scope` section below. Incomplete or insufficient mitigation reviews will not be eligible for awards.
## Scope
### Branch
https://github.com/silo-finance/silo-contracts-v2 (https://github.com/silo-finance/silo-contracts-v2)
### Mitigation of High & Medium Severity Issues
Mitigations of all High and Medium issues listed here will be considered in-scope:
Fix Mitigation of Notes
PR 1162 (https://github.com/silo-finance/silo-contracts-v2/pull/1162) (solution) and PR 1173 (https://github.com/silo-finance/silo-contracts-v2/pull/1173) (optimization) F-11: Deflation attack (https://code4rena.com/audits/2025-03-silo-finance/submissions/F-11) Ensure that deposit does not generate zero shares
PR 1166 (https://github.com/silo-finance/silo-contracts-v2/pull/1166) F-17: Supply function doesn't account for market maxDeposit when providing assets to it (https://code4rena.com/audits/2025-03-silo-finance/submissions/F-17) Account for `maxDeposit` when doing deposit
PR 1168 (https://github.com/silo-finance/silo-contracts-v2/pull/1168) F-26: SiloVault will incorrectly accrue rewards during user transfer/transferFrom actions due to unsynced totalSupply() (https://code4rena.com/audits/2025-03-silo-finance/submissions/F-26) Silo-vaults: accrue on transfer
PR 1165 (https://github.com/silo-finance/silo-contracts-v2/pull/1165) F-57: SiloVault.sol :: Markets with assets that revert on zero approvals cannot be removed (https://code4rena.com/audits/2025-03-silo-finance/submissions/F-57) Reset approval to 1 wei
## Out of Scope
F-195: Lack of slippage and deadline protection in deposit(), withdraw() and redeem() (https://code4rena.com/audits/2025-03-silo-finance/submissions/F-195)
F-207: Incorrect reward distribution due to feeShares minting order (https://code4rena.com/audits/2025-03-silo-finance/submissions/F-207)
Twitter (https://twitter.com/code4rena)
Discord (https://discord.gg/code4rena)
GitHub (https://github.com/code-423n4/)
Media kit (https://github.com/code-423n4/media-kit)
Terms (https://docs.code4rena.com/legal/terms-of-service)
Privacy (https://docs.code4rena.com/legal/privacy-policy)