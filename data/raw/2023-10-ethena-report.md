# Ethena Labs
Findings & Analysis Report

#### 2023-12-21

## Table of contents

-
Overview

- About C4

- Wardens

- Summary

- Scope

- Severity Criteria

-
Medium Risk Findings (4)

- [M-01] `FULL_RESTRICTED` Stakers can bypass restriction through approvals

- [M-02] Soft Restricted Staker Role can withdraw stUSDe for USDe

- [M-03] users still forced to follow previously set cooldownDuration even when cooldown is off (set to zero) before unstaking

- [M-04] Malicious users can front-run to cause a denial of service (DoS) for StakedUSDe due to MinShares checks

-
Low Risk and Non-Critical Issues

- 01 Use an efficient logic in setter functions

- 02 Be consistent in the code logic when emitting events in setter functions

- 03 Delta neutrality caution

- 04 Easy DoS on big players when minting and redeeming in EthenaMinting.sol

- 05 Inexpedient code lines

- 06 Emission of identical values

- 07 Typo mistakes

- 08 Functions should have fully intended logic

- 09 Unneeded function still not removed

-
Gas Optimizations

- G-01 Use constants for variables that don’t change (Save a storage SLOT: 2200 Gas)

- G-02 Unnecessary SLOADS inside the constructor (Save 2 SLOADS - 4200 Gas)

- G-03 Modifier makes it expensive since we end up reading state twice (Saves 1197 Gas on average from the tests)

- G-04 Reading Same state variable twice due to modifier usage (Save 2040 Gas on average from the tests)

- G-05 We can save an entire SLOAD (2100 Gas) by short circuiting the operations

- G-06 We can avoid making a function call here by utilizing the short circuit rules

- G-07 Cache function calls

- G-08 Unnecessary function call (Saves 369 Gas on average)

- G-09 Validate function parameters before making function calls or reading any state variables

- G-10 Emit local variables instead of state variable (Save ~100 Gas)

-
Audit Analysis

- 1. Architecture Overview

- 2. Codebase Quality Analysis

- 3. Centralization Risks

- 4. Systemic Risks

- 5. Attack Vectors Discussed During the Audit

- 6. Example Report

- Disclosures

# Overview

## About C4

Code4rena (C4) is an open organization consisting of security researchers, auditors, developers, and individuals with domain expertise in smart contracts.

A C4 audit is an event in which community participants, referred to as Wardens, review, audit, or analyze smart contract logic in exchange for a bounty provided by sponsoring projects.

During the audit outlined in this document, C4 conducted an analysis of the Ethena Labs smart contract system written in Solidity. The audit took place between October 24—October 30 2023.

## Wardens

158 Wardens contributed reports to Ethena Labs:

- peanuts

- Madalad

- adeolu

- Eeyore

- Shubham

- josephdara

- jasonxiale

- Mike_Bello90

- 0xWaitress

- d3e4

- Yanchuan

- ayden

- mert_eren

- pontifex

- twcctop

- cartlex_

- critical-or-high

- trachev

- ciphermarco

- 0xmystery

- Arz

- HChang26

- Limbooo

- RamenPeople (kimchi and wasabi)

- SovaSlava

- lsaudit

- J4X

- squeaky_cactus

- hunter_w3b

- Udsen

- Kaysoft

- deepkin

- pep7siup

- btk

- ast3ros

- 0xAlix2 (a_kalout and ali_shehab)

- dirk_y

- Oxsadeeq

- Cosine

- Krace

- 0xAadi

- castle_chain

- 0xpiken

- radev_sw

- ge6a

- Team_Rocket (AlexCzm and EllipticPoint)

- sorrynotsorry

- tnquanghuy0512

- lanrebayode77

- degensec

- KIntern_NA (duc and TrungOre)

- SpicyMeatball

- Beosin

- 0xVolcano

- oakcobalt

- pavankv

- Sathish9098

- Kral01

- Al-Qa-qa

- ZanyBonzy

- 0xSmartContract

- 0xweb3boy

- fouzantanveer

- albahaca

- catellatech

- invitedtea

- 0xAnah

- niser93

- JCK

- K42

- Bauchibred

- D_Auditor

- clara

- Bulletprime

- xiao

- jauvany

- digitizeworx

- 0x11singh99

- ThreeSigma (0x73696d616f, 0xCarolina, EduCatarino, and SolidityDev99)

- arjun16

- nuthan2x

- 0xhacksmithh

- SAQ

- tabriz

- petrichor

- shamsulhaq123

- Raihan

- 0xhex

- brakelessak

- unique

- 0xta

- thekmj

- phenom80

- aslanbek

- Rolezn

- yashgoel72

- 0xgrbr

- SM3_SS

- evmboi32

- naman1778

- ybansal2403

- 0xhunter

- qpzm

- erebus

- adam-idarrha

- Avci (0xdanial and 0xArshia)

- Breeje

- PASCAL

- rotcivegaf

- asui

- codynhat

- BeliSesir

- 0xG0P1

- Imlazy0ne

- supersizer0x

- pipidu83

- cccz

- cryptonue

- kkkmmmsk

- Rickard

- Noro

- Proxy

- ziyou-

- chainsnake

- oxchsyston

- 0xStalin

- Fitro

- rokinot

- matrix_0wl

- Walter

- young

- Zach_166

- Topmark

- almurhasan

- csanuragjain

- PENGUN

- zhaojie

- ptsanev

- marchev

- Strausses

- foxb868

- max10afternoon

- DarkTower (Gelato_ST, Maroutis, OxTenma, and 0xrex)

- rvierdiiev

- twicek

- 0x_Scar

- Bughunter101

This audit was judged by 0xDjango.

Final report assembled by liveactionllama.

# Summary

The C4 analysis yielded an aggregated total of 4 unique vulnerabilities. Of these vulnerabilities, 0 received a risk rating in the category of HIGH severity and 4 received a risk rating in the category of MEDIUM severity.

Additionally, C4 analysis included 98 reports detailing issues with a risk rating of LOW severity or non-critical. There were also 41 reports recommending gas optimizations.

All of the issues presented here are linked back to their original finding.

# Scope

The code under review can be found within the C4 Ethena Labs repository, and is composed of 6 smart contracts written in the Solidity programming language and includes 588 lines of Solidity code.

In addition to the known issues identified by the project team, a Code4rena bot race was conducted at the start of the audit. The winning bot, MrsHudson from warden slvDev, generated the Automated Findings report and all findings therein were classified as out of scope.

# Severity Criteria

C4 assesses the severity of disclosed vulnerabilities based on three primary risk categories: high, medium, and low/non-critical.

High-level considerations for vulnerabilities span the following key areas when conducting assessments:

- Malicious Input Handling

- Escalation of privileges

- Arithmetic

- Gas use

For more information regarding the severity criteria referenced throughout the submission review process, please refer to the documentation provided on the C4 website, specifically our section on Severity Categorization.

# Medium Risk Findings (4)

## [M-01] `FULL_RESTRICTED` Stakers can bypass restriction through approvals

Submitted by josephdara, also found by Arz, ge6a, KIntern_NA, Team_Rocket, mert_eren, sorrynotsorry, Eeyore (1, 2), tnquanghuy0512, Limbooo, 0xmystery, Yanchuan, RamenPeople, lanrebayode77, J4X, degensec, HChang26, 0xAadi, castle_chain, 0xpiken, SpicyMeatball, and Beosin

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDe.sol#L225-L238

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDe.sol#L245-L248

The `StakedUSDe` contract implements a method to `SOFTLY` or `FULLY` restrict user address, and either transfer to another user or burn.

However there is an underlying issue. A fully restricted address is supposed to be unable to withdraw/redeem, however this issue can be walked around via the approve mechanism.

The openzeppelin `ERC4626` contract allows approved address to withdraw and redeem on behalf of another address so far there is an approval.

` function redeem(uint256 shares, address receiver, address owner) public virtual override returns (uint256) `

Blacklisted Users can explore this loophole to redeem their funds fully. This is because in the overridden `_withdraw` function, the token owner is not checked for restriction.

` function _withdraw(address caller, address receiver, address _owner, uint256 assets, uint256 shares)
internal
override
nonReentrant
notZero(assets)
notZero(shares)
{
if (hasRole(FULL_RESTRICTED_STAKER_ROLE, caller) || hasRole(FULL_RESTRICTED_STAKER_ROLE, receiver)) {
revert OperationNotAllowed();
}`

Also in the overridden `_beforeTokenTransfer` there is a clause added to allow burning from restricted addresses:

` function _beforeTokenTransfer(address from, address to, uint256) internal virtual override {
if (hasRole(FULL_RESTRICTED_STAKER_ROLE, from) && to != address(0)) {
revert OperationNotAllowed();
}`

All these issues allows a restricted user to simply approve another address and redeem their usde.

### Proof of Concept

This is a foundry test that can be run in the `StakedUSDe.blacklist.t.sol` in the `test/foundry/staking` directory.

`// SPDX-License-Identifier: MIT
pragma solidity >=0.8;

/* solhint-disable private-vars-leading-underscore */
/* solhint-disable func-name-mixedcase */
/* solhint-disable var-name-mixedcase */

import {console} from "forge-std/console.sol";
import "forge-std/Test.sol";
import {SigUtils} from "forge-std/SigUtils.sol";

import "../../../contracts/USDe.sol";
import "../../../contracts/StakedUSDe.sol";
import "../../../contracts/interfaces/IUSDe.sol";
import "../../../contracts/interfaces/IERC20Events.sol";
import "../../../contracts/interfaces/ISingleAdminAccessControl.sol";

contract StakedUSDeBlacklistTest is Test, IERC20Events {
USDe public usdeToken;
StakedUSDe public stakedUSDe;
SigUtils public sigUtilsUSDe;
SigUtils public sigUtilsStakedUSDe;
uint256 public _amount = 100 ether;

address public owner;
address public alice;
address public bob;
address public greg;

bytes32 SOFT_RESTRICTED_STAKER_ROLE;
bytes32 FULL_RESTRICTED_STAKER_ROLE;
bytes32 DEFAULT_ADMIN_ROLE;
bytes32 BLACKLIST_MANAGER_ROLE;

event Deposit(address indexed caller, address indexed owner, uint256 assets, uint256 shares);
event Withdraw(
address indexed caller, address indexed receiver, address indexed owner, uint256 assets, uint256 shares
);
event LockedAmountRedistributed(address indexed from, address indexed to, uint256 amountToDistribute);

function setUp() public virtual {
usdeToken = new USDe(address(this));

alice = makeAddr("alice");
bob = makeAddr("bob");
greg = makeAddr("greg");
owner = makeAddr("owner");

usdeToken.setMinter(address(this));

vm.startPrank(owner);
stakedUSDe = new StakedUSDe(IUSDe(address(usdeToken)), makeAddr('rewarder'), owner);
vm.stopPrank();

FULL_RESTRICTED_STAKER_ROLE = keccak256("FULL_RESTRICTED_STAKER_ROLE");
SOFT_RESTRICTED_STAKER_ROLE = keccak256("SOFT_RESTRICTED_STAKER_ROLE");
DEFAULT_ADMIN_ROLE = 0x00;
BLACKLIST_MANAGER_ROLE = keccak256("BLACKLIST_MANAGER_ROLE");
}

function _mintApproveDeposit(address staker, uint256 amount, bool expectRevert) internal {
usdeToken.mint(staker, amount);

vm.startPrank(staker);
usdeToken.approve(address(stakedUSDe), amount);

uint256 sharesBefore = stakedUSDe.balanceOf(staker);
if (expectRevert) {
vm.expectRevert(IStakedUSDe.OperationNotAllowed.selector);
} else {
vm.expectEmit(true, true, true, false);
emit Deposit(staker, staker, amount, amount);
}
stakedUSDe.deposit(amount, staker);
uint256 sharesAfter = stakedUSDe.balanceOf(staker);
if (expectRevert) {
assertEq(sharesAfter, sharesBefore);
} else {
assertApproxEqAbs(sharesAfter - sharesBefore, amount, 1);
}
vm.stopPrank();
}

function test_fullBlacklist_withdraw_pass() public {
_mintApproveDeposit(alice, _amount, false);

vm.startPrank(owner);
stakedUSDe.grantRole(FULL_RESTRICTED_STAKER_ROLE, alice);
vm.stopPrank();
//@audit-issue assert that alice is blacklisted
bool isBlacklisted = stakedUSDe.hasRole(FULL_RESTRICTED_STAKER_ROLE, alice);
assertEq(isBlacklisted, true);
//@audit-issue The staked balance of Alice
uint256 balAliceBefore = stakedUSDe.balanceOf(alice);
//@audit-issue The usde balance of address 56
uint256 bal56Before = usdeToken.balanceOf(address(56));
vm.startPrank(alice);
stakedUSDe.approve(address(56), _amount);
vm.stopPrank();

//@audit-issue address 56 receives approval and can unstake usde for Alice after a blacklist
vm.startPrank(address(56));
stakedUSDe.redeem(_amount, address(56), alice);
vm.stopPrank();
//@audit-issue The staked balance of Alice
uint256 balAliceAfter = stakedUSDe.balanceOf(alice);
//@audit-issue The usde balance of address 56
uint256 bal56After = usdeToken.balanceOf(address(56));

assertEq(bal56Before, 0);
assertEq(balAliceAfter, 0);
console.log(balAliceBefore);
console.log(bal56Before);
console.log(balAliceAfter);
console.log(bal56After);

}
}`

Here we use `address(56)` as the second address, and we see that the user can withdraw their `100000000000000000000` tokens that was restricted.

This is my test result showing the balances.

`[PASS] test_fullBlacklist_withdraw_pass() (gas: 239624)
Logs:
100000000000000000000 // Alice staked balance before
0 // address(56) USDe balance before
0 // Alice staked balance after
100000000000000000000 // address(56) USDe balance after

Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 8.68ms`

### Tools Used

Foundry, Manual review

### Recommended Mitigation Steps

Check the token owner as well in the `_withdraw` function:

` if (hasRole(FULL_RESTRICTED_STAKER_ROLE, caller) || hasRole(FULL_RESTRICTED_STAKER_ROLE, receiver) || hasRole(FULL_RESTRICTED_STAKER_ROLE, _owner) ) {
revert OperationNotAllowed();
}`

FJ-Riveros (Ethena) confirmed via duplicate issue #666

0xDjango (judge) decreased severity to Medium

josephdara (warden) commented:

Hi @0xDjango, I do believe this is a high severity bug. It does break a major protocol functionality, compromising assets directly.
According to the severity categorization:

3 — High: Assets can be stolen/lost/compromised directly

Thanks!

0xDjango (judge) commented:

@josephdara - I have conversed with the project team, and we have agreed that breaking rules due to legal compliance is medium severity as no funds are at risk.

## [M-02] Soft Restricted Staker Role can withdraw stUSDe for USDe

Submitted by squeaky_cactus, also found by Arz, Kaysoft, Udsen, deepkin, SovaSlava, Oxsadeeq, pep7siup, Shubham, peanuts, Limbooo, Yanchuan, btk, RamenPeople, Cosine, ast3ros, HChang26, 0xAlix2, dirk_y, and Krace

A requirement is stated that a user with the `SOFT_RESTRICTED_STAKER_ROLE` is not allowed to withdraw `USDe` for `stUSDe`.

The code does not satisfy that condition, when a holder has the `SOFT_RESTRICTED_STAKER_ROLE`, they can exchange their `stUSDe` for `USDe` using `StakedUSDeV2`.

### Description

The Ethena readme has the following decription of legal requirements for the Soft Restricted Staker Role:
https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/README.md?plain=1#L98

`Due to legal requirements, there's a `SOFT_RESTRICTED_STAKER_ROLE` and `FULL_RESTRICTED_STAKER_ROLE`.
The former is for addresses based in countries we are not allowed to provide yield to, for example USA.
Addresses under this category will be soft restricted. They cannot deposit USDe to get stUSDe or withdraw stUSDe for USDe.
However they can participate in earning yield by buying and selling stUSDe on the open market.`

In summary, legal requires are that a `SOFT_RESTRICTED_STAKER_ROLE`:

- MUST NOT deposit USDe to get stUSDe

- MUST NOT withdraw USDe for USDe

- MAY earn yield by trading stUSDe on the open market

As `StakedUSDeV2` is a `ERC4626`, the `stUSDe` is a share on the underlying `USDe` asset. There are two distinct entrypoints for a user to exchange their share for their claim on the underlying the asset, `withdraw` and `redeem`. Each cater for a different input (`withdraw` being by asset, `redeem` being by share), however both invoked the same internal `_withdraw` function, hence both entrypoints are affected.

There are two cases where a user with `SOFT_RESTRICTED_STAKER_ROLE` may have acquired `stUSDe`:

- Brought `stUSDe` on the open market

- Deposited `USDe` in `StakedUSDeV2` before being granted the `SOFT_RESTRICTED_STAKER_ROLE`

In both cases the user can call either withdraw their holding by calling `withdraw` or `redeem` (when cooldown is off), or `unstake` (if cooldown is on) and successfully exchange their `stUSDe` for `USDe`.

### Proof of Concept

The following two tests demonstrate the use case of a user staking, then being granted the `SOFT_RESTRICTED_STAKER_ROLE`, then exchanging their `stUSDe` for `USDe` (first using `redeem` function, the second using `withdrawm`).

The use case for acquiring on the open market, only requiring a different setup, however the exchange behaviour is identical and the cooldown enabled `cooldownAssets` and `cooldownShares` function still use the same `_withdraw` as `redeem` and `withdraw`, which leads to the same outcome.

(Place code into `StakedUSDe.t.sol` and run with `forge test`)

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/test/foundry/staking/StakedUSDe.t.sol

` bytes32 public constant SOFT_RESTRICTED_STAKER_ROLE = keccak256("SOFT_RESTRICTED_STAKER_ROLE");
bytes32 private constant BLACKLIST_MANAGER_ROLE = keccak256("BLACKLIST_MANAGER_ROLE");

function test_redeem_while_soft_restricted() public {
// Set up Bob with 100 stUSDe
uint256 initialAmount = 100 ether;
_mintApproveDeposit(bob, initialAmount);
uint256 stakeOfBob = stakedUSDe.balanceOf(bob);

// Alice becomes a blacklist manager
vm.prank(owner);
stakedUSDe.grantRole(BLACKLIST_MANAGER_ROLE, alice);

// Blacklist Bob with the SOFT_RESTRICTED_STAKER_ROLE
vm.prank(alice);
stakedUSDe.addToBlacklist(bob, false);

// Assert that Bob has staked and is now has the soft restricted role
assertEq(usdeToken.balanceOf(bob), 0);
assertEq(stakedUSDe.totalSupply(), stakeOfBob);
assertEq(stakedUSDe.totalAssets(), initialAmount);
assertTrue(stakedUSDe.hasRole(SOFT_RESTRICTED_STAKER_ROLE, bob));

// Rewards to StakeUSDe and vest
uint256 rewardAmount = 50 ether;
_transferRewards(rewardAmount, rewardAmount);
vm.warp(block.timestamp + 8 hours);

// Assert that only the total assets have increased after vesting
assertEq(usdeToken.balanceOf(bob), 0);
assertEq(stakedUSDe.totalSupply(), stakeOfBob);
assertEq(stakedUSDe.totalAssets(), initialAmount + rewardAmount);
assertTrue(stakedUSDe.hasRole(SOFT_RESTRICTED_STAKER_ROLE, bob));

// Bob withdraws his stUSDe for USDe
vm.prank(bob);
stakedUSDe.redeem(stakeOfBob, bob, bob);

// End state being while being soft restricted Bob redeemed USDe with rewards
assertApproxEqAbs(usdeToken.balanceOf(bob), initialAmount + rewardAmount, 2);
assertApproxEqAbs(stakedUSDe.totalAssets(), 0, 2);
assertTrue(stakedUSDe.hasRole(SOFT_RESTRICTED_STAKER_ROLE, bob));
}

function test_withdraw_while_soft_restricted() public {
// Set up Bob with 100 stUSDe
uint256 initialAmount = 100 ether;
_mintApproveDeposit(bob, initialAmount);
uint256 stakeOfBob = stakedUSDe.balanceOf(bob);

// Alice becomes a blacklist manager
vm.prank(owner);
stakedUSDe.grantRole(BLACKLIST_MANAGER_ROLE, alice);

// Blacklist Bob with the SOFT_RESTRICTED_STAKER_ROLE
vm.prank(alice);
stakedUSDe.addToBlacklist(bob, false);

// Assert that Bob has staked and is now has the soft restricted role
assertEq(usdeToken.balanceOf(bob), 0);
assertEq(stakedUSDe.totalSupply(), stakeOfBob);
assertEq(stakedUSDe.totalAssets(), initialAmount);
assertTrue(stakedUSDe.hasRole(SOFT_RESTRICTED_STAKER_ROLE, bob));

// Rewards to StakeUSDe and vest
uint256 rewardAmount = 50 ether;
_transferRewards(rewardAmount, rewardAmount);
vm.warp(block.timestamp + 8 hours);

// Assert that only the total assets have increased after vesting
assertEq(usdeToken.balanceOf(bob), 0);
assertEq(stakedUSDe.totalSupply(), stakeOfBob);
assertEq(stakedUSDe.totalAssets(), initialAmount + rewardAmount);
assertTrue(stakedUSDe.hasRole(SOFT_RESTRICTED_STAKER_ROLE, bob));

// Bob withdraws his stUSDe for USDe (-1 as dust is lost in asset to share rounding in ERC4626)
vm.prank(bob);
stakedUSDe.withdraw(initialAmount + rewardAmount - 1, bob, bob);

// End state being while being soft restricted Bob redeemed USDe with rewards
assertApproxEqAbs(usdeToken.balanceOf(bob), initialAmount + rewardAmount, 2);
assertApproxEqAbs(stakedUSDe.totalAssets(), 0, 2);
assertTrue(stakedUSDe.hasRole(SOFT_RESTRICTED_STAKER_ROLE, bob));
}`

### Tools Used

Manual review, Foundry test

### Recommended Mitigation Steps

With the function overriding present, to prevent the `SOFT_RESTRICTED_STAKER_ROLE` from being able to exchange their `stUSDs` for `USDe`, make the following change in `StakedUSDe`

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDe.sol#L232

`- if (hasRole(FULL_RESTRICTED_STAKER_ROLE, caller) || hasRole(FULL_RESTRICTED_STAKER_ROLE, receiver)) {
+ if (hasRole(FULL_RESTRICTED_STAKER_ROLE, caller) || hasRole(FULL_RESTRICTED_STAKER_ROLE, receiver) || hasRole(SOFT_RESTRICTED_STAKER_ROLE, caller)) {
revert OperationNotAllowed();
}`

0xDjango (judge) decreased severity to Medium

kayinnnn (Ethena) disputed and commented:

For this issue, the docs were incorrect to say withdrawal by soft restricted role is not allowed. Only depositing is not allowed.

## [M-03] users still forced to follow previously set cooldownDuration even when cooldown is off (set to zero) before unstaking

Submitted by adeolu, also found by jasonxiale, Madalad, Mike_Bello90, peanuts, josephdara, Eeyore, and Shubham

The `StakedUSDeV2` contract can enforces coolDown periods for users before they are able to unstake/ take out their funds from the silo contract if coolDown is on. Based on the presence of the modifiers `ensureCooldownOff` and `ensureCooldownOn`, it is known that the coolDown state of the `StakedUSDeV2` contract can be toggled on or off.
In a scenario where coolDown is on (always turned on by default) and Alice and Bob deposits, two days after Alice wants to withdraw/redeem. Alice is forced to wait for 90 days before completing withdrawal/getting her tokens from the silo contract because Alice must call coolDownAsset()/coolDownShares() fcns respectively. Bob decides to wait an extra day.

On the third day, Bob decides to withdraw/redeem. Contract admin also toggles the coolDown off (sets cooldownDuration to 0), meaning there is no longer a coolDown period and all withdrawals should be sent to the users immediately. Bob now calls calls the redeem()/withdraw() fcn to withdraw instantly to his address instead of the silo address since there is no coolDown.

Alice sees Bob has gotten his tokens but Alice cant use the redeem()/withdraw() because her `StakedUSDeV2` were already burned and her underlying assets were sent to the silo contract for storage. Alice cannot sucessfully call `unstake()` because her `userCooldown.cooldownEnd` value set to ~ 90 days. Now Alice has to unfairly wait out the 90 days even though coolDowns have been turned off and everyone else has unrestricted access to their assets. Alice only crime is trying to withdraw earlier than Bob. This is a loss to Alice as Alice has no StakedUSDE or the underlying asset for the no longer necessary 90 days as if the assset is volatile, it may lose some fiat value during the unfair and no longer necessary wait period.

If cooldown is turned off, it should affect all contract processes and as such, withdrawals should become immediate to users. Tokens previously stored in the USDeSilo contract should become accessible to users when the cooldown state is off. Previous withdrawal requests that had a cooldown should no longer be restricted by a coolDown period since coolDown now off and the coolDownDuration of the contract is now 0.

### Proof of Concept

- Since StakedUSDeV2 is ERC4626, user calls deposit() to deposit the underlying token asset and get minted shares that signify the user’s position size in the vault.

- The coolDown duration is set to 90 days on deployment of the `StakedUSDeV2` contract, meaning coolDown is toggled on by default.

- User cannot redeem/withdraw his funds via withdraw() and redeem() because coolDown is on. Both functions have the ensureCooldownOff modifier which reverts if the coolDownDuration value is not 0.

-
User tried to exit position, to withdraw when coolDown is on, user must call coolDownAsset()/coolDownShares(). This will cause :

- For the user’s underlyingAmount and cooldownEnd timestamp values to be set in the mapping `cooldowns`. cooldownEnd timestamp values is set to 90 days from the present.

- For the user’s `StakedUSDeV2` ERC4626 position shares to be burnt and the positon underlying asset value to be sent to the USDeSilo contract.

` /// @notice redeem assets and starts a cooldown to claim the converted underlying asset
/// @param assets assets to redeem
/// @param owner address to redeem and start cooldown, owner must allowed caller to perform this action
function cooldownAssets(uint256 assets, address owner) external ensureCooldownOn returns (uint256) {
if (assets > maxWithdraw(owner)) revert ExcessiveWithdrawAmount();

uint256 shares = previewWithdraw(assets);

cooldowns[owner].cooldownEnd = uint104(block.timestamp) + cooldownDuration;
cooldowns[owner].underlyingAmount += assets;

_withdraw(_msgSender(), address(silo), owner, assets, shares);

return shares;
}

/// @notice redeem shares into assets and starts a cooldown to claim the converted underlying asset
/// @param shares shares to redeem
/// @param owner address to redeem and start cooldown, owner must allowed caller to perform this action
function cooldownShares(uint256 shares, address owner) external ensureCooldownOn returns (uint256) {
if (shares > maxRedeem(owner)) revert ExcessiveRedeemAmount();

uint256 assets = previewRedeem(shares);

cooldowns[owner].cooldownEnd = uint104(block.timestamp) + cooldownDuration;
cooldowns[owner].underlyingAmount += assets;

_withdraw(_msgSender(), address(silo), owner, assets, shares);

return assets;
}`

- User can only use unstake() to get the assets from the silo contract. unstake enforces that the block.timestamp (present time) is more than the 90 days cooldown period set during the execution of `cooldownAssets()` and `cooldownShares()` and reverts if 90 days time has not been reached yet.

` function unstake(address receiver) external {
UserCooldown storage userCooldown = cooldowns[msg.sender];
uint256 assets = userCooldown.underlyingAmount;

if (block.timestamp >= userCooldown.cooldownEnd) {
userCooldown.cooldownEnd = 0;
userCooldown.underlyingAmount = 0;

silo.withdraw(receiver, assets);
} else {
revert InvalidCooldown();
}
}`

- If contract admin decides to turn the coolDown period off, by setting the cooldownDuration to 0 via setCooldownDuration(), user who has his assets under the coolDown in the silo still wont be able to withdraw via unstake() because the logic in `unstake()` doesnt allow for the user’s coolDownEnd value which was set under the previous coolDown duration state to be bypassed as coolDowns are now turned off and the StakedUSDeV2 behavior is supposed to be changed to follow ERC4626 standard and allow for the user assets to get to them immediately with no coolDown period still enforced on withdrawals as seen in the comment here.

- User who initiated withdrawal when the coolDown was toggled on will still continue to be restricted from his tokens/funds even after coolDown is toggled off. This should not be because restrictions are removed, all previous pending withdrawals should be allowed to be completed without wait for 90 days since the coolDownDuration of the contract is now 0.

### Coded Proof of Concept

Run with `forge test --mt test_UnstakeUnallowedAfterCooldownIsTurnedOff`.

` // SPDX-License-Identifier: MIT
pragma solidity >=0.8;

/* solhint-disable private-vars-leading-underscore */
/* solhint-disable var-name-mixedcase */
/* solhint-disable func-name-mixedcase */

import "forge-std/console.sol";
import "forge-std/Test.sol";
import {SigUtils} from "forge-std/SigUtils.sol";

import "../../../contracts/USDe.sol";
import "../../../contracts/StakedUSDeV2.sol";
import "../../../contracts/interfaces/IUSDe.sol";
import "../../../contracts/interfaces/IERC20Events.sol";

contract StakedUSDeV2CooldownTest is Test, IERC20Events {
USDe public usdeToken;
StakedUSDeV2 public stakedUSDeV2;
SigUtils public sigUtilsUSDe;
SigUtils public sigUtilsStakedUSDe;
uint256 public _amount = 100 ether;

address public owner;
address public alice;
address public bob;
address public greg;

bytes32 SOFT_RESTRICTED_STAKER_ROLE;
bytes32 FULL_RESTRICTED_STAKER_ROLE;
bytes32 DEFAULT_ADMIN_ROLE;
bytes32 BLACKLIST_MANAGER_ROLE;
bytes32 REWARDER_ROLE;

event Deposit(address indexed caller, address indexed owner, uint256 assets, uint256 shares);
event Withdraw(
address indexed caller, address indexed receiver, address indexed owner, uint256 assets, uint256 shares
);
event LockedAmountRedistributed(address indexed from, address indexed to, uint256 amountToDistribute);

function setUp() public virtual {
usdeToken = new USDe(address(this));

alice = makeAddr("alice");
bob = makeAddr("bob");
greg = makeAddr("greg");
owner = makeAddr("owner");

usdeToken.setMinter(address(this));

vm.startPrank(owner);
stakedUSDeV2 = new StakedUSDeV2(IUSDe(address(usdeToken)), makeAddr('rewarder'), owner);
vm.stopPrank();

FULL_RESTRICTED_STAKER_ROLE = keccak256("FULL_RESTRICTED_STAKER_ROLE");
SOFT_RESTRICTED_STAKER_ROLE = keccak256("SOFT_RESTRICTED_STAKER_ROLE");
DEFAULT_ADMIN_ROLE = 0x00;
BLACKLIST_MANAGER_ROLE = keccak256("BLACKLIST_MANAGER_ROLE");
REWARDER_ROLE = keccak256("REWARDER_ROLE");
}

function test_UnstakeUnallowedAfterCooldownIsTurnedOff () public {
address staker = address(20);
uint usdeTokenAmountToMint = 10000*1e18;

usdeToken.mint(staker, usdeTokenAmountToMint);

//at the deposit coolDownDuration is set to 90 days
assert(stakedUSDeV2.cooldownDuration() == 90 days);

vm.startPrank(staker);
usdeToken.approve(address(stakedUSDeV2), usdeTokenAmountToMint);

stakedUSDeV2.deposit(usdeTokenAmountToMint / 2, staker);

vm.roll(block.number + 1);
uint assets = stakedUSDeV2.maxWithdraw(staker);
stakedUSDeV2.cooldownAssets(assets , staker);

vm.stopPrank();

//assert that cooldown for the staker is now set to 90 days from now
( uint104 cooldownEnd, ) = stakedUSDeV2.cooldowns(staker);
assert(cooldownEnd == uint104( block.timestamp + 90 days));

vm.prank(owner);
//toggle coolDown off in the contract
stakedUSDeV2.setCooldownDuration(0);

//now try to unstake,
/** since cooldown duration is now 0 and contract is cooldown state is turned off.
it should allow unstake immediately but instead it will revert **/
vm.expectRevert(IStakedUSDeCooldown.InvalidCooldown.selector);
vm.prank(staker);
stakedUSDeV2.unstake(staker);
}
}`

### Tools Used

Manual review, Foundry

### Recommended Mitigation Steps

Modify the code in unstake() fcn to allow for withdrawals from the silo contract when the contract’s coolDownDuration has become 0.

### Assessed type

Error

kayinnnn (Ethena) confirmed and commented:

Acknowledge the issue, but revise to low severity finding as it causes minor inconvenience in the rare time we change cooldown period. However, it is still fixed - existing per user cooldown is ignored if the global cooldown is `0`.

## [M-04] Malicious users can front-run to cause a denial of service (DoS) for StakedUSDe due to MinShares checks

Submitted by ayden, also found by d3e4 (1, 2), pontifex, trachev, ciphermarco, Madalad, Yanchuan, peanuts, twcctop, cartlex_, mert_eren, 0xWaitress (1, 2), and critical-or-high

Malicious users can transfer `USDe` token to `StakedUSDe` protocol directly lead to a denial of service (DoS) for StakedUSDe due to the limit shares check.

### Proof of Concept

User deposit `USDe` token to `StakedUSDe` protocol to get share via invoke external `deposit` function. Let’s see how share is calculate:

` function _convertToShares(uint256 assets, Math.Rounding rounding) internal view virtual returns (uint256) {
return assets.mulDiv(totalSupply() + 10 ** _decimalsOffset(), totalAssets() + 1, rounding);
}`

Since `decimalsOffset() == 0` and totalAssets equal the balance of `USDe` in this protocol

` function totalAssets() public view virtual override returns (uint256) {
return _asset.balanceOf(address(this));
}`

$$
f(share) = (USDeAmount \ast totalSupply) / (totalUSDeAssets() + 1)
$$
The minimum share is set to 1 ether.

` uint256 private constant MIN_SHARES = 1 ether;`

Assuming malicious users transfer 1 ether of `USDe` into the protocol and receive ZERO shares, how much tokens does the next user need to pay if they want to exceed the minimum share limit of 1 ether? That would be 1 ether times 1 ether, which is a substantial amount.

I add a test case in `StakedUSDe.t.sol`:

` function testMinSharesViolation() public {
address malicious = vm.addr(100);

usdeToken.mint(malicious, 1 ether);
usdeToken.mint(alice, 1000 ether);

//assume malicious user deposit 1 ether into protocol.
vm.startPrank(malicious);
usdeToken.transfer(address(stakedUSDe), 1 ether);

vm.stopPrank();
vm.startPrank(alice);
usdeToken.approve(address(stakedUSDe), type(uint256).max);

//1000 ether can't exceed the minimum share limit of 1 ether
vm.expectRevert(IStakedUSDe.MinSharesViolation.selector);
stakedUSDe.deposit(1000 ether, alice);
}`

We can see even Alice deposit a substantial number of tokens but still cannot surpass the 1 ether share limit which will lead to a denial of service (DoS) for StakedUSDe due to MinShares checks.

### Tools Used

vscode

### Recommended Mitigation Steps

We can solve this issue by setting a minimum deposit amount.

### Assessed type

DoS

FJ-Riveros (Ethena) acknowledged, but disagreed with severity and commented via duplicate issue #32:

We acknowledge the potential exploitability of this issue, but we propose marking it as `Medium` severity. Our rationale is based on the fact that this exploit can only occur during deployment. To mitigate this risk, we plan to fund the smart contract in the next block, ensuring that nobody has access to the ABI or contract source code. We could even use flashbots for this purpose.

0xDjango (judge) commented via duplicate issue #32:

Agree with medium. Several of the duplicate reports vary in their final impacts but mostly consist of:

- Small donation leading to bricked contract

- Large donation can eventually lead to blocked withdrawals

The small donation impact simply requires a redeploy, though the impact is a valid medium. The large donation has major implications for stakers, but the large amount of capital required downgrades it to medium as well. I will be reviewing each duplicate on a case-by-case basis to ensure that all impacts due to the same bug class fit within medium.

0xDjango (judge) decreased severity to Medium

# Low Risk and Non-Critical Issues

For this audit, 98 reports were submitted by wardens detailing low risk and non-critical issues. The report highlighted below by 0xmystery received the top score from the judge.

The following wardens also submitted reports: lsaudit, 0xhunter, Team_Rocket, qpzm, erebus, ge6a, hunter_w3b, adam-idarrha, pontifex, SovaSlava, Avci, Arz, Breeje, PASCAL, Udsen, rotcivegaf, 0x11singh99, asui, codynhat, radev_sw, Kaysoft, BeliSesir, deepkin, JCK, ThreeSigma, Madalad, 0xG0P1, Imlazy0ne, Mike_Bello90, tnquanghuy0512, peanuts, supersizer0x, Shubham, 0xAadi, pep7siup, pipidu83, adeolu, Kral01, jasonxiale, cccz, oakcobalt, cryptonue, twcctop, pavankv, Eeyore, cartlex_, kkkmmmsk, arjun16, squeaky_cactus, Rickard, Noro, Proxy, J4X, Al-Qa-qa, ziyou-, chainsnake, HChang26, oxchsyston, Yanchuan, btk, 0xStalin, Bauchibred, Fitro, rokinot, matrix_0wl, Walter, ZanyBonzy, young, Zach_166, Topmark, ast3ros, degensec, almurhasan, nuthan2x, csanuragjain, PENGUN, 0xpiken, zhaojie, ptsanev, marchev, castle_chain, sorrynotsorry, ayden, 0xAlix2, Strausses, foxb868, dirk_y, max10afternoon, DarkTower, rvierdiiev, 0xWaitress, twicek, lanrebayode77, 0x_Scar, Bughunter101, 0xhacksmithh, and critical-or-high.

## [01] Use an efficient logic in setter functions

When intending to emit both the old and new values, there isn’t a need to cache the old value that will only be used once. Simply emit both values before assigning a new value to the state variable. For example, the following setter function may be refactored as follows:

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L436-L440

` function _setMaxMintPerBlock(uint256 _maxMintPerBlock) internal {
+ emit MaxMintPerBlockChanged(maxMintPerBlock, _maxMintPerBlock);
- uint256 oldMaxMintPerBlock = maxMintPerBlock;
maxMintPerBlock = _maxMintPerBlock;
- emit MaxMintPerBlockChanged(oldMaxMintPerBlock, maxMintPerBlock);
}`

All other instances entailed:

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L442-L447

` /// @notice Sets the max redeemPerBlock limit
function _setMaxRedeemPerBlock(uint256 _maxRedeemPerBlock) internal {
uint256 oldMaxRedeemPerBlock = maxRedeemPerBlock;
maxRedeemPerBlock = _maxRedeemPerBlock;
emit MaxRedeemPerBlockChanged(oldMaxRedeemPerBlock, maxRedeemPerBlock);
}`

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/StakedUSDeV2.sol#L126-L134

` function setCooldownDuration(uint24 duration) external onlyRole(DEFAULT_ADMIN_ROLE) {
if (duration > MAX_COOLDOWN_DURATION) {
revert InvalidCooldown();
}

uint24 previousDuration = cooldownDuration;
cooldownDuration = duration;
emit CooldownDurationUpdated(previousDuration, cooldownDuration);
}`

## [02] Be consistent in the code logic when emitting events in setter functions

By convention, it’s recommended emitting the old value followed by the new one in the same event instead of the other way round.

Here’s one instance found:

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/USDe.sol#L23-L26

` function setMinter(address newMinter) external onlyOwner {
- emit MinterUpdated(newMinter, minter);
+ emit MinterUpdated(minter, newMinter);
minter = newMinter;
}`

## [03] Delta neutrality caution

Users should be cautioned about the impermanent losses entailed arising from the delta-neutral stability strategy adopted by the protocol, specifically if the short positions were to encounter hefty losses. Apparently, the users could have held on to their collateral, e.g. `stETH or WETH`, and ended up a lot richer with the equivalent amount of `USDe`. I suggest all minting entries to begin with stable coins like `USDC, DAI etc` that could be converted to `stETH` to generate yield if need be instead of having users depositing `stETH` from their wallet reserves. Psychologically, this will make the users feel better as the mentality has been fostered more on preserving the 1:1 peg of `USDe` at all times.

## [04] Easy DoS on big players when minting and redeeming in EthenaMinting.sol

As indicated on the audit description, users intending to mint/redeem a large amount will need to mint/redeem over several blocks due to `maxMintPerBlock` or `maxRedeemPerBlock`. However, these RFQ’s are prone to DoS because `mintedPerBlock[block.number] + mintAmount > maxMintPerBlock` or `redeemedPerBlock[block.number] + redeemAmount > maxRedeemPerBlock` could revert by only 1 wei in excess.

While these issues could be sorted by the backend to make a full use of `maxMintPerBlock` or `maxRedeemPerBlock` per block, it will make the intended logic a lot more efficient by auto reducing the RFQ amount to perfectly fill up the remaining quota for the current block. Better yet, set up a queue system where request amount running in hundreds of thousands or millions may be auto split up with multiple orders via only one signature for batching.

## [05] Inexpedient code lines

In the function below, the if block already dictates that `getUnvestedAmount() == 0` manages to avoid a revert. Hence, consider refactoring the following code lines as it makes no sense adding 0 value `getUnvestedAmount()` of to the addend, `amount`:

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/StakedUSDe.sol#L89-L99

` function transferInRewards(uint256 amount) external nonReentrant onlyRole(REWARDER_ROLE) notZero(amount) {
if (getUnvestedAmount() > 0) revert StillVesting();
- uint256 newVestingAmount = amount + getUnvestedAmount();

- vestingAmount = newVestingAmount;
+ vestingAmount = amount;

// The rest of the codes
}`

## [06] Emission of identical values

Under the context of the above/preceding recommendation, `transferInRewards()` should also have its `emit` refactored below. Otherwise, you are practically emitting two identical values that defeat the purpose of contrasting the old and the values.

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/StakedUSDe.sol#L89-L99

` function transferInRewards(uint256 amount) external nonReentrant onlyRole(REWARDER_ROLE) notZero(amount) {
if (getUnvestedAmount() > 0) revert StillVesting();
- uint256 newVestingAmount = amount + getUnvestedAmount();

- vestingAmount = newVestingAmount;
+ emit RewardsReceived(vestingAmount, amount);
+ vestingAmount = amount;
lastDistributionTimestamp = block.timestamp;
// transfer assets from rewarder to this contract
IERC20(asset()).safeTransferFrom(msg.sender, address(this), amount);

- emit RewardsReceived(amount, newVestingAmount);
}`

## [07] Typo mistakes

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/StakedUSDeV2.sol#L94

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/StakedUSDeV2.sol#L110

`- /// @param owner address to redeem and start cooldown, owner must allowed caller to perform this action
+ /// @param owner address to redeem and start cooldown, owner must allow caller to perform this action`

## [08] Functions should have fully intended logic

The function below is meant to be used only for minting. Hence, redeeming has got nothing to do with this view function. Consider refactoring the first if block so `mint()` could revert earlier if need be:

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L351-L374

` function verifyRoute(Route calldata route, OrderType orderType) public view override returns (bool) {
// routes only used to mint
- if (orderType == OrderType.REDEEM) {
- return true;
- }
+ if (orderType =! OrderType.MINT) {
+ return false;
+ }
uint256 totalRatio = 0;
if (route.addresses.length != route.ratios.length) {
return false;
}
if (route.addresses.length == 0) {
return false;
}
for (uint256 i = 0; i < route.addresses.length; ++i) {
if (!_custodianAddresses.contains(route.addresses[i]) || route.addresses[i] == address(0) || route.ratios[i] == 0)
{
return false;
}
totalRatio += route.ratios[i];
}
if (totalRatio != 10_000) {
return false;
}
return true;
}`

## [09] Unneeded function still not removed

Per Pashov’s audit report, L-04 mentioned that the unused `EthenaMinting::encodeRoute` has been removed by Ethena. However, this erroneous function still exists in EthenaMinting.sol.

https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L334-L336

`- function encodeRoute(Route calldata route) public pure returns (bytes memory) {
- return abi.encode(ROUTE_TYPE, route.addresses, route.ratios);
- }`

Consider removing this controversial function where possible.

FJ-Riveros (Ethena) acknowledged

Note: the following submissions from the same warden were downgraded from Medium to Low/Non-critical and were also considered by the judge in scoring:

- [10] Inconsistent Role-Based Checks in `redistributeLockedAmount` and `_beforeTokenTransfer functions`

- [11] Denial-of-Service Vulnerability via Minimum Shares Restriction

- [12] Inflexible Withdrawal Management in StakedUSDeV2 Contract

# Gas Optimizations

For this audit, 41 reports were submitted by wardens detailing gas optimizations. The report highlighted below by 0xVolcano received the top score from the judge.

The following wardens also submitted reports: 0xAnah, hunter_w3b, SovaSlava, niser93, lsaudit, SAQ, tabriz, J4X, petrichor, Udsen, shamsulhaq123, radev_sw, Raihan, 0x11singh99, JCK, 0xAadi, ThreeSigma, 0xhex, brakelessak, unique, oakcobalt, 0xta, 0xpiken, arjun16, thekmj, phenom80, aslanbek, Rolezn, yashgoel72, 0xgrbr, pavankv, Sathish9098, SM3_SS, nuthan2x, K42, castle_chain, evmboi32, naman1778, ybansal2403, and 0xhacksmithh.

## [G-01] Use constants for variables that don’t change (Save a storage SLOT: 2200 Gas)

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDeV2.sol#L22

`File: /contracts/StakedUSDeV2.sol
22: uint24 public MAX_COOLDOWN_DURATION = 90 days;`

The variable `MAX_COOLDOWN_DURATION` should be declared as a constant variable since it does not change, from the naming, it would seem the intention was to actually make it a constant.

`diff --git a/contracts/StakedUSDeV2.sol b/contracts/StakedUSDeV2.sol
index df2bb48..f8fa980 100644
--- a/contracts/StakedUSDeV2.sol
+++ b/contracts/StakedUSDeV2.sol
@@ -19,7 +19,7 @@ contract StakedUSDeV2 is IStakedUSDeCooldown, StakedUSDe {

USDeSilo public silo;

- uint24 public MAX_COOLDOWN_DURATION = 90 days;
+ uint24 public constant MAX_COOLDOWN_DURATION = 90 days;`

## [G-02] Unnecessary SLOADS inside the constructor (Save 2 SLOADS - 4200 Gas)

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L111-L136

`File: /contracts/EthenaMinting.sol
111: constructor(
112: IUSDe _usde,
113: address[] memory _assets,
114: address[] memory _custodians,
115: address _admin,
116: uint256 _maxMintPerBlock,
117: uint256 _maxRedeemPerBlock
118: ) {

134: // Set the max mint/redeem limits per block
135: _setMaxMintPerBlock(_maxMintPerBlock);
136: _setMaxRedeemPerBlock(_maxRedeemPerBlock);`

In the constructor, we call `_setMaxMintPerBlock()` and `_setMaxRedeemPerBlock()` functions to set `maxMintPerBlock` and `maxRedeemPerBlock` respectively.
The functions are defined as follows (we only focus on `_setMaxMintPerBlock()` as they are essentially the same).

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L436-L440

`436: function _setMaxMintPerBlock(uint256 _maxMintPerBlock) internal {
437: uint256 oldMaxMintPerBlock = maxMintPerBlock;
438: maxMintPerBlock = _maxMintPerBlock;
439: emit MaxMintPerBlockChanged(oldMaxMintPerBlock, maxMintPerBlock);
440: }`

This function will first read the current value of `maxMintPerBlock` and store in a local variable,however when called inside the constructor, we know the value of `maxMintPerBlock` is `0` so we don’t necessarily need to cache it inside the constructor, we just need to set it.

Caching inside the constructor would just mean we are using an SLOAD(2100 gas) to cache value `0`.

I suggest we refactor the constructor as follows which would save us 2 cold SLOADS:

` // Set the max mint/redeem limits per block
- _setMaxMintPerBlock(_maxMintPerBlock);
- _setMaxRedeemPerBlock(_maxRedeemPerBlock);
+ maxMintPerBlock = _maxMintPerBlock;
+ maxRedeemPerBlock = _maxRedeemPerBlock;`

If we really need to emit events inside the constructor, we can define a new event that would emit the current set value, i.e. `_maxMintPerBlock` and `_maxRedeemPerBlock`.

## [G-03] Modifier makes it expensive since we end up reading state twice (Saves 1197 Gas on average from the tests)

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L162-L174

Min
Average
Median
Max

Before
4657
81745
123779
195520

After
4645
80548
123639
195380

`File: /contracts/EthenaMinting.sol
162: function mint(Order calldata order, Route calldata route, Signature calldata signature)
163: external
164: override
165: nonReentrant
166: onlyRole(MINTER_ROLE)
167: belowMaxMintPerBlock(order.usde_amount)
168: {
169: if (order.order_type != OrderType.MINT) revert InvalidOrder();
170: verifyOrder(order, signature);
171: if (!verifyRoute(route, order.order_type)) revert InvalidRoute();
172: if (!_deduplicateOrder(order.benefactor, order.nonce)) revert Duplicate();
173: // Add to the minted amount in this block
174: mintedPerBlock[block.number] += order.usde_amount;`

The function `mint()` makes use of the modifier `belowMaxMintPerBlock()` which has the following implementation:

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L97-L100

`97: modifier belowMaxMintPerBlock(uint256 mintAmount) {
98: if (mintedPerBlock[block.number] + mintAmount > maxMintPerBlock) revert MaxMintPerBlockExceeded();
99: _;
100: }`

Note, the modifier reads `mintedPerBlock[block.number]` which is a state varible.

Our `mint()` function also does the same SLOAD when adding to the minted amount.

We can avoid making this two SLOADS by simply in lining this modifier and caching the result of `mintedPerBlock[block.number]` as shown below:

`@@ -164,14 +164,15 @@ contract EthenaMinting is IEthenaMinting, SingleAdminAccessControl, ReentrancyGu
override
nonReentrant
onlyRole(MINTER_ROLE)
- belowMaxMintPerBlock(order.usde_amount)
{
+ uint256 _mintedPerBlock = mintedPerBlock[block.number];
+ if (_mintedPerBlock + order.usde_amount > maxMintPerBlock) revert MaxMintPerBlockExceeded();
if (order.order_type != OrderType.MINT) revert InvalidOrder();
verifyOrder(order, signature);
if (!verifyRoute(route, order.order_type)) revert InvalidRoute();
if (!_deduplicateOrder(order.benefactor, order.nonce)) revert Duplicate();
// Add to the minted amount in this block
- mintedPerBlock[block.number] += order.usde_amount;
+ mintedPerBlock[block.number] = _mintedPerBlock + order.usde_amount;
_transferCollateral(
order.collateral_amount, order.collateral_asset, order.benefactor, route.addresses, route.ratios
);`

Since the modifier was only being used for the function `mint()`, we can go ahead and delete it.

## [G-04] Reading Same state variable twice due to modifier usage (Save 2040 Gas on average from the tests)

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L194-L205
| | Min | Average | Median | Max |
| ------ | --- | ------- | ----- | ----- |
| Before | 6349 | 40053 | 27127 | 81127 |
| After | 6337 | 38013 | 20962 | 81017 |

`File: /contracts/EthenaMinting.sol
194: function redeem(Order calldata order, Signature calldata signature)
195: external
196: override
197: nonReentrant
198: onlyRole(REDEEMER_ROLE)
199: belowMaxRedeemPerBlock(order.usde_amount)
200: {
201: if (order.order_type != OrderType.REDEEM) revert InvalidOrder();
202: verifyOrder(order, signature);
203: if (!_deduplicateOrder(order.benefactor, order.nonce)) revert Duplicate();
204: // Add to the redeemed amount in this block
205: redeemedPerBlock[block.number] += order.usde_amount;`

Similar to our previous finding, the function `redeem()` uses the modifier `belowMaxRedeemPerBlock()` which is implemented as below:

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L104-L107

`104: modifier belowMaxRedeemPerBlock(uint256 redeemAmount) {
105: if (redeemedPerBlock[block.number] + redeemAmount > maxRedeemPerBlock) revert MaxRedeemPerBlockExceeded();
106: _;
107: }`

We read the state variable `redeemedPerBlock[block.number]` which is also read inside the `redeem()` function. We can inline the modifier which would allow us to cache the call which helps avoid making extra sloads.

Refactor the code as shown below.

`@@ -196,13 +191,14 @@ contract EthenaMinting is IEthenaMinting, SingleAdminAccessControl, ReentrancyGu
override
nonReentrant
onlyRole(REDEEMER_ROLE)
- belowMaxRedeemPerBlock(order.usde_amount)
{
+ uint256 _redeemedPerBlock = redeemedPerBlock[block.number];
+ if (_redeemedPerBlock + order.usde_amount > maxRedeemPerBlock) revert MaxRedeemPerBlockExceeded();
if (order.order_type != OrderType.REDEEM) revert InvalidOrder();
verifyOrder(order, signature);
if (!_deduplicateOrder(order.benefactor, order.nonce)) revert Duplicate();
// Add to the redeemed amount in this block
- redeemedPerBlock[block.number] += order.usde_amount;
+ redeemedPerBlock[block.number] = _redeemedPerBlock + order.usde_amount;
usde.burnFrom(order.benefactor, order.usde_amount);`

Since the modifier was only being used for the function `redeem()`, we can go ahead and delete it.

## [G-05] We can save an entire SLOAD (2100 Gas) by short circuiting the operations

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L413-L433

`File: /contracts/EthenaMinting.sol
413: function _transferCollateral(

419: ) internal {
420: // cannot mint using unsupported asset or native ETH even if it is supported for redemptions
421: if (!_supportedAssets.contains(asset) || asset == NATIVE_TOKEN) revert UnsupportedAsset();`

The if statement has two checks `!_supportedAssets.contains(asset)` and `asset == NATIVE_TOKEN` where the first check involves making a state read while the second check only compares a constant variable to a function parameter.

According to the rules of short circuit, if the first check is true, we do not have to do the second check thus in this case, we should make sure the first check is the cheapest to do.

By reordering as shown below, we can avoid making the state read if `asset == NATIVE_TOKEN` which would save us ~2100 Gas.

`diff --git a/contracts/EthenaMinting.sol b/contracts/EthenaMinting.sol
index 32da3a5..35f4613 100644
--- a/contracts/EthenaMinting.sol
+++ b/contracts/EthenaMinting.sol
@@ -418,7 +418,7 @@ contract EthenaMinting is IEthenaMinting, SingleAdminAccessControl, ReentrancyGu
uint256[] calldata ratios
) internal {
// cannot mint using unsupported asset or native ETH even if it is supported for redemptions
- if (!_supportedAssets.contains(asset) || asset == NATIVE_TOKEN) revert UnsupportedAsset();
+ if (asset == NATIVE_TOKEN || !_supportedAssets.contains(asset) ) revert UnsupportedAsset();
IERC20 token = IERC20(asset);
uint256 totalTransferred = 0;
for (uint256 i = 0; i < addresses.length; ++i) {`

## [G-06] We can avoid making a function call here by utilizing the short circuit rules

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDe.sol#L245-L252

`File: /contracts/StakedUSDe.sol
245: function _beforeTokenTransfer(address from, address to, uint256) internal virtual override {
246: if (hasRole(FULL_RESTRICTED_STAKER_ROLE, from) && to != address(0)) {
247: revert OperationNotAllowed();
248: }
249: if (hasRole(FULL_RESTRICTED_STAKER_ROLE, to)) {
250: revert OperationNotAllowed();
251: }
252: }`

`diff --git a/contracts/StakedUSDe.sol b/contracts/StakedUSDe.sol
index 0a56a7d..8551478 100644
--- a/contracts/StakedUSDe.sol
+++ b/contracts/StakedUSDe.sol
@@ -243,7 +243,7 @@ contract StakedUSDe is SingleAdminAccessControl, ReentrancyGuard, ERC20Permit, E
*/

function _beforeTokenTransfer(address from, address to, uint256) internal virtual override {
- if (hasRole(FULL_RESTRICTED_STAKER_ROLE, from) && to != address(0)) {
+ if (to != address(0) && hasRole(FULL_RESTRICTED_STAKER_ROLE, from)) {
revert OperationNotAllowed();
}
if (hasRole(FULL_RESTRICTED_STAKER_ROLE, to)) {`

## [G-07] Cache function calls

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDe.sol#L89-L99

`File: /contracts/StakedUSDe.sol
89: function transferInRewards(uint256 amount) external nonReentrant onlyRole(REWARDER_ROLE) notZero(amount) {
90: if (getUnvestedAmount() > 0) revert StillVesting();
91: uint256 newVestingAmount = amount + getUnvestedAmount();`

Note, we are calling `getUnvestedAmount()` function two times. If we look at the implementation of that function here, we have the following:

`173: function getUnvestedAmount() public view returns (uint256) {
174: uint256 timeSinceLastDistribution = block.timestamp - lastDistributionTimestamp;

176: if (timeSinceLastDistribution >= VESTING_PERIOD) {
177: return 0;
178: }

180: return ((VESTING_PERIOD - timeSinceLastDistribution) * vestingAmount) / VESTING_PERIOD;
181: }`

Note, in this function, we make two state reads(SLOADS) for `lastDistributionTimestamp` and `vestingAmount`. As this is the first SLOAD in this transaction, this means the variables are COLD thus we use 2100 Gas per variable. Ie 4200 Gas for the two variables read.

Calling this function twice would incur a lot of cost (gas). We should cache the results if this call and save them in a local variable as shown below:

`diff --git a/contracts/StakedUSDe.sol b/contracts/StakedUSDe.sol
index 0a56a7d..0953b2f 100644
--- a/contracts/StakedUSDe.sol
+++ b/contracts/StakedUSDe.sol
@@ -87,8 +87,9 @@ contract StakedUSDe is SingleAdminAccessControl, ReentrancyGuard, ERC20Permit, E
* @param amount The amount of rewards to transfer.
*/
function transferInRewards(uint256 amount) external nonReentrant onlyRole(REWARDER_ROLE) notZero(amount) {
- if (getUnvestedAmount() > 0) revert StillVesting();
- uint256 newVestingAmount = amount + getUnvestedAmount();
+ uint256 _unvestedAmount = getUnvestedAmount();
+ if (_unvestedAmount > 0) revert StillVesting();
+ uint256 newVestingAmount = amount + _unvestedAmount;

vestingAmount = newVestingAmount;
lastDistributionTimestamp = block.timestamp;`

Note: The following finding is somehow related to this one, some confusion on why the devs choose to do the calls. The next finding will show an alternate optimization.

## [G-08] Unnecessary function call (Saves 369 Gas on average)

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDe.sol#L89-L99
| | Min | Average | Median | Max |
| ------ | --- | ------- | ----- | ----- |
| Before | 4359 | 42190 | 44596 | 66916 |
| After | 4359 | 41821 | 44065 | 66385 |

`File: /contracts/StakedUSDe.sol
89: function transferInRewards(uint256 amount) external nonReentrant onlyRole(REWARDER_ROLE) notZero(amount) {
90: if (getUnvestedAmount() > 0) revert StillVesting();
91: uint256 newVestingAmount = amount + getUnvestedAmount();

93: vestingAmount = newVestingAmount;
94: lastDistributionTimestamp = block.timestamp;
95: // transfer assets from rewarder to this contract
96: IERC20(asset()).safeTransferFrom(msg.sender, address(this), amount);

98: emit RewardsReceived(amount, newVestingAmount);
99: }`

The function `getUnvestedAmount()` returns `uint256` which means anything greater than or equal to `0`.

We revert if the return is greater than 0, which means the only way we get to execute the function `transferInRewards()` is when `getUnvestedAmount()` returns `0`. This begs the question, why do we call the function on the second line if we can only get there when `getUnvestedAmount() == 0`?

`diff --git a/contracts/StakedUSDe.sol b/contracts/StakedUSDe.sol
index 0a56a7d..a378300 100644
--- a/contracts/StakedUSDe.sol
+++ b/contracts/StakedUSDe.sol
@@ -88,7 +88,7 @@ contract StakedUSDe is SingleAdminAccessControl, ReentrancyGuard, ERC20Permit, E
*/
function transferInRewards(uint256 amount) external nonReentrant onlyRole(REWARDER_ROLE) notZero(amount) {
if (getUnvestedAmount() > 0) revert StillVesting();
- uint256 newVestingAmount = amount + getUnvestedAmount();
+ uint256 newVestingAmount = amount;

vestingAmount = newVestingAmount;
lastDistributionTimestamp = block.timestamp;`

## [G-09] Validate function parameters before making function calls or reading any state variables

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L339-L348

`File: /contracts/EthenaMinting.sol
339: function verifyOrder(Order calldata order, Signature calldata signature) public view override returns (bool, bytes32) {
340: bytes32 taker_order_hash = hashOrder(order);
341: address signer = ECDSA.recover(taker_order_hash, signature.signature_bytes);
342: if (!(signer == order.benefactor || delegatedSigner[signer][order.benefactor])) revert InvalidSignature();
343: if (order.beneficiary == address(0)) revert InvalidAmount();
344: if (order.collateral_amount == 0) revert InvalidAmount();
345: if (order.usde_amount == 0) revert InvalidAmount();
346: if (block.timestamp > order.expiry) revert SignatureExpired();
347: return (true, taker_order_hash);
348: }`

`diff --git a/contracts/EthenaMinting.sol b/contracts/EthenaMinting.sol
index 32da3a5..cf642d5 100644
--- a/contracts/EthenaMinting.sol
+++ b/contracts/EthenaMinting.sol
@@ -337,13 +337,13 @@ contract EthenaMinting is IEthenaMinting, SingleAdminAccessControl, ReentrancyGu

/// @notice assert validity of signed order
function verifyOrder(Order calldata order, Signature calldata signature) public view override returns (bool, bytes32) {
- bytes32 taker_order_hash = hashOrder(order);
- address signer = ECDSA.recover(taker_order_hash, signature.signature_bytes);
- if (!(signer == order.benefactor || delegatedSigner[signer][order.benefactor])) revert InvalidSignature();
if (order.beneficiary == address(0)) revert InvalidAmount();
if (order.collateral_amount == 0) revert InvalidAmount();
if (order.usde_amount == 0) revert InvalidAmount();
if (block.timestamp > order.expiry) revert SignatureExpired();
+ bytes32 taker_order_hash = hashOrder(order);
+ address signer = ECDSA.recover(taker_order_hash, signature.signature_bytes);
+ if (!(signer == order.benefactor || delegatedSigner[signer][order.benefactor])) revert InvalidSignature();
return (true, taker_order_hash);
}`

## [G-10] Emit local variables instead of state variable (Save ~100 Gas)

### Emit `_maxMintPerBlock` instead of `maxMintPerBlock`

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L436-L440

`File: /contracts/EthenaMinting.sol
436: function _setMaxMintPerBlock(uint256 _maxMintPerBlock) internal {
437: uint256 oldMaxMintPerBlock = maxMintPerBlock;
438: maxMintPerBlock = _maxMintPerBlock;
439: emit MaxMintPerBlockChanged(oldMaxMintPerBlock, maxMintPerBlock);
440: }`

Since we are setting our state variable `maxRedeemPerBlock` to the function parameter `_maxRedeemPerBlock`, we should emit the function parameter as it is cheaper to read compared to the state variable:

`diff --git a/contracts/EthenaMinting.sol b/contracts/EthenaMinting.sol
index 32da3a5..f569e40 100644
--- a/contracts/EthenaMinting.sol
+++ b/contracts/EthenaMinting.sol
@@ -436,7 +436,7 @@ contract EthenaMinting is IEthenaMinting, SingleAdminAccessControl, ReentrancyGu
function _setMaxMintPerBlock(uint256 _maxMintPerBlock) internal {
uint256 oldMaxMintPerBlock = maxMintPerBlock;
maxMintPerBlock = _maxMintPerBlock;
- emit MaxMintPerBlockChanged(oldMaxMintPerBlock, maxMintPerBlock);
+ emit MaxMintPerBlockChanged(oldMaxMintPerBlock, _maxMintPerBlock);
}`

### Emit `_maxMintPerBlock` instead of `maxMintPerBlock`

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/EthenaMinting.sol#L443-L447

`File: /contracts/EthenaMinting.sol
443: function _setMaxRedeemPerBlock(uint256 _maxRedeemPerBlock) internal {
444: uint256 oldMaxRedeemPerBlock = maxRedeemPerBlock;
445: maxRedeemPerBlock = _maxRedeemPerBlock;
446: emit MaxRedeemPerBlockChanged(oldMaxRedeemPerBlock, maxRedeemPerBlock);
447: }`

Since we are setting our state variable `maxRedeemPerBlock` to the function parameter `_maxRedeemPerBlock`, we should emit the function parameter as it is cheaper to read compared to the state variable.

`diff --git a/contracts/EthenaMinting.sol b/contracts/EthenaMinting.sol
index 32da3a5..8198a3e 100644
--- a/contracts/EthenaMinting.sol
+++ b/contracts/EthenaMinting.sol
@@ -443,7 +443,7 @@ contract EthenaMinting is IEthenaMinting, SingleAdminAccessControl, ReentrancyGu
function _setMaxRedeemPerBlock(uint256 _maxRedeemPerBlock) internal {
uint256 oldMaxRedeemPerBlock = maxRedeemPerBlock;
maxRedeemPerBlock = _maxRedeemPerBlock;
- emit MaxRedeemPerBlockChanged(oldMaxRedeemPerBlock, maxRedeemPerBlock);
+ emit MaxRedeemPerBlockChanged(oldMaxRedeemPerBlock, _maxRedeemPerBlock);
}`

### Emit `duration` instead of `cooldownDuration` (Save 1 SLOAD)

https://github.com/code-423n4/2023-10-ethena/blob/ee67d9b542642c9757a6b826c82d0cae60256509/contracts/StakedUSDeV2.sol#L126-L134
| | Min | Average | Median | Max |
| ------ | --- | ------- | ----- | ----- |
| Before | 2439 | 3110 | 2439 | 9239 |
| After | 2425 | 3097 | 2425 | 9225 |

`File: /contracts/StakedUSDeV2.sol
126: function setCooldownDuration(uint24 duration) external onlyRole(DEFAULT_ADMIN_ROLE) {
127: if (duration > MAX_COOLDOWN_DURATION) {
128: revert InvalidCooldown();
129: }

131: uint24 previousDuration = cooldownDuration;
132: cooldownDuration = duration;
133: emit CooldownDurationUpdated(previousDuration, cooldownDuration);
134: }`

`diff --git a/contracts/StakedUSDeV2.sol b/contracts/StakedUSDeV2.sol
index df2bb48..d3f1b29 100644
--- a/contracts/StakedUSDeV2.sol
+++ b/contracts/StakedUSDeV2.sol
@@ -130,6 +130,6 @@ contract StakedUSDeV2 is IStakedUSDeCooldown, StakedUSDe {

uint24 previousDuration = cooldownDuration;
cooldownDuration = duration;
- emit CooldownDurationUpdated(previousDuration, cooldownDuration);
+ emit CooldownDurationUpdated(previousDuration, duration);
}`

FJ-Riveros (Ethena) acknowledged

# Audit Analysis

For this audit, 25 analysis reports were submitted by wardens. An analysis report examines the codebase as a whole, providing observations and advice on such topics as architecture, mechanism, or approach. The report highlighted below by radev_sw received the top score from the judge.

The following wardens also submitted reports: oakcobalt, 0xSmartContract, hunter_w3b, Sathish9098, Al-Qa-qa, J4X, Kral01, 0xweb3boy, fouzantanveer, albahaca, pavankv, catellatech, invitedtea, ZanyBonzy, D_Auditor, clara, Bulletprime, xiao, jauvany, JCK, peanuts, K42, Bauchibred, and digitizeworx.

## 1. Architecture Overview

### 1.1. Protocol Explanation

- Overview:

Ethena is developing a DeFi ecosystem with a primary goal of offering a permissionless stablecoin, USDe, that allows users to earn yield within the system. This process is a contrast to traditional stablecoins like USDC, where the central authority (e.g., Circle) benefits from the yield. In Ethena’s ecosystem, users can stake their USDe to earn stUSDe, which appreciates over time as the protocol generates yield.

-
Smart Contract Infrastructure:

- `USDe.sol`: The contract for the USDe stablecoin, limited in functionality with controls for minting privileges.

- `EthenaMinting.sol`: This contract mints and redeems USDe in a single, atomic, trustless transaction. Central to user interactions, handling minting and redemption of USDe. It employs EIP712 signatures for transactions, routing collateral through predefined safe channels, and includes security measures against potential compromises by limiting minting and providing emergency roles (GATEKEEPERS) to intervene in suspicious activities.

- `StakedUSDeV2.sol`: Allows USDe holders to stake their tokens for stUSDe, earning yield from the protocol’s profits. It incorporates mechanisms to prevent exploitation of yield payouts and has a cooldown period for unstaking. For legal compliance, it can restrict certain users (based on jurisdiction or law enforcement directives) from staking or freeze their assets, with the provision of fund recovery in extreme cases.

-
Roles in Ethena Ecosystem:

- `USDe` minter - can mint any amount of USDe tokens to any address. Expected to be the EthenaMinting contract.

- `USDe` owner - can set token minter and transfer ownership to another address

- `USDe` token holder - can not just transfer tokens but burn them and sign permits for others to spend their balance

- `StakedUSDe` admin - can rescue tokens from the contract and also to redistribute a fully restricted staker’s stUSDe balance, as well as give roles to other addresses (for example the FULLRESTRICTEDSTAKER_ROLE role)

- `StakedUSDeV2` admin - has all power of “StakedUSDe admin” and can also call the setCooldownDuration method

- `REWARDER_ROLE` - can transfer rewards into the StakedUSDe contract that will be vested over the next 8 hours

- `BLACKLIST_MANAGER_ROLE` - can do/undo full or soft restriction on a holder of stUSDe

- `SOFT_RESTRICTED_STAKER_ROLE` - address with this role can’t stake his USDe tokens or get stUSDe tokens minted to him

- `FULL_RESTRICTED_STAKER_ROLE` - address with this role can’t burn his stUSDe tokens to unstake his USDe tokens, neither to transfer stUSDe tokens. His balance can be manipulated by the admin of StakedUSDe

- `MINTER_ROLE` - can actually mint USDe tokens and also transfer EthenaMinting’s token or ETH balance to a custodian address

- `REDEEMER_ROLE` - can redeem collateral assets for burning USDe

- `EthenaMinting admin` - can set the maxMint/maxRedeem amounts per block and add or remove supported collateral assets and custodian addresses, grant/revoke roles

- `GATEKEEPER_ROLE` - can disable minting/redeeming of USDe and remove MINTERROLE and REDEEMERROLE roles from authorized accounts

-
What custodian is? (Chat GPT says)

- In the realm of cryptocurrencies and blockchain technology, a “custodian” refers to an entity (company or smart contract) that holds and safeguards an individual’s or institution’s digital assets. The role of a custodian is critical in scenarios where security and proper asset management are paramount. This concept isn’t exclusive to digital assets; traditional financial institutions have custodians as well.

- Within a blockchain environment, an address usually refers to a specific destination where cryptocurrencies are sent. Think of it like an account number in the traditional banking sense.
In the context of smart contracts or decentralized applications, `custodianAddresses` likely refer to the collection of blockchain addresses that are authorized to hold assets on behalf of others.
These addresses are controlled by the custodian, which could be a smart contract or a third-party service that maintains the security of the private keys associated with these addresses.

### 1.2. Codebase Explanation & Examples Scenarios of Intended Protocol Flow

All possible Actions and Flows in Ethena Protocol:

1. Minting USDe:

Users provide stETH as collateral to mint USDe. The system gives an RFQ (Request for Quote) detailing how much USDe they can create. Upon agreement, the user signs a transaction, and Ethena mints USDe against the stETH, which is then employed in various yield-generating activities, primarily shorting ETH perpetual futures to maintain a delta-neutral position.

Additional Explanations Related to the `Minting`:

- So, `USDe` will be equivalent to using DAI, USDC, USDT (`USDe` contract is just the ERC20 token for the stablecoin and this token will be the token used in `StakedUSDeV2.sol` staking contract) where it `doesn't have any yield` and `only the holders of stUSDe` will earn the generated yield.

- The `EthenaMinting.sol` contract is the place where `minting` is done.

2. Yield Generating:

Ethena generates yield by taking advantage of the differences in staking returns (3-4% for stETH) and shorting ETH perpetuals (6-8%). Profits are funneled into an insurance fund and later distributed to stakers, enhancing the value of stUSDe relative to USDe.

3. Maintaining Delta Neutrality:

Ethena employs a strategy involving stETH and short positions in ETH perpetuals, ensuring the value stability of users’ holdings against market volatility.

Example 1:

-
Initial Setup:

- The user initiates the process by sending 10 stETH to Ethena. The stETH is a token representing staked Ethereum in the Ethereum 2.0 network, allowing holders to earn rewards while keeping liquidity. At the time of the transaction, Ethereum’s price is $2,000; thus, 10 stETH equals $20,000.

- Ethena uses these 10 stETH to mint 20,000 USDe stablecoins for the user, reflecting the stETH’s dollar value.

- Simultaneously, Ethena opens a short position on Ethereum perpetual futures (ETH perps) equivalent to 10 ETH. Given the current Ethereum price of $2,000, this also represents a $20,000 position. This short position means that Ethena is betting on the Ethereum price going down.

-
Market Movement and Its Impact:

- Now, the market faces significant volatility, and the price of Ethereum drops by 90%. As a result, the value of the user’s 10 stETH decreases to $2,000 (reflecting the 90% drop from the original $20,000 value).

- However, because Ethena shorted 10 ETH worth of perps, the decrease in Ethereum’s price is advantageous for this position. The short ETH perps position now has an unrealized profit of $18,000. This profit occurs because Ethena ‘borrowed’ the ETH at a higher price to open the position and can now ‘buy’ it back at a much lower price, pocketing the difference.

-
Redemption Process:

- The user decides to redeem their 20,000 USDe. For Ethena to honor this request, they need to provide the user with the equivalent value in stETH that the USDe represents.

- Ethena closes the short position on the ETH perps, which means they ‘buy’ back the ETH at the current market price, realizing the $18,000 profit due to the price difference from when they opened the short position.

- With the $18,000, Ethena purchases 90 stETH at the current market price ($200 per stETH, as the price has dropped by 90%).

- Ethena then returns the original 10 stETH along with the 90 stETH purchased from the profits of the short position. So, the user receives 100 stETH, which, at the current market price, is worth $20,000.

Example 2:

-
Initial Condition:

- The price of ETH is $2,000.

- The user sends in 10 stETH (equivalent to 10 ETH) to Ethena to mint 20,000 USDe (since 10 ETH at $2,000 per ETH is worth $20,000).

- Ethena takes these 10 stETH and opens a short position on 10 ETH’s worth of perpetual futures (perps) to hedge against the price movement of ETH.

-
Market Movement:

- The market goes up by 50%. Therefore, the price of ETH (and stETH, as it’s pegged to the ETH value) increases to $3,000.

-
Position Analysis:

- The user’s 10 stETH is now worth $30,000 due to the market increase.

- However, Ethena’s short position is now at a notional loss because it was betting on the price of ETH going down, not up. The loss on the short position is $10,000 (the increase in value per ETH is $1,000, and Ethena shorted 10 ETH).

-
Redemption Process:

- If the user decides to redeem their USDe, they will present their 20,000 USDe.

- Considering the market movement, the short position’s loss needs to be covered. Ethena has to close the short position and realize the loss of $10,000.

- After covering the $10,000 loss, there’s $20,000 worth of stETH left (approximately 6.67 stETH at the new rate of $3,000 per stETH) to return to the user.

-
End Result:

- The user initially had assets worth $20,000 (10 stETH). If they hadn’t engaged with Ethena and simply held onto their 10 stETH, their assets would now be worth $30,000 due to the positive market movement.

- By choosing to use Ethena’s hedging mechanism, they’ve forfeited potential gains to safeguard against potential losses. They receive approximately 6.67 stETH (worth $20,000) back after the redemption process, missing out on the additional $10,000 value increase.

- Essentially, the user’s assets remained stable in USDe value, but they did not benefit from ETH’s bullish market. Their asset value didn’t decrease, but they also lost potential profit

## 2. Codebase Quality Analysis

-
`USDe.sol`:

- Code Organization:

- The contract is well-organized and follows the best practices for code layout and structure.

- It uses OpenZeppelin contracts, which are widely recognized and audited.

- The constructor initializes the contract and sets the owner/admin.

- It provides functions to set the minter and mint USDe tokens.

- Modifiers:

- The contract uses the `Ownable2Step` modifier, which enforces two-step ownership transfer.

- The `onlyRole` modifier is used to restrict certain functions to specific roles, enhancing security.

- Minting:

- The contract allows only the minter to mint new tokens, which is a good security measure.

- It checks if the provided minter is valid.

- Gas Efficiency:

- The contract uses the SafeERC20 library for safe token transfers, ensuring protection against reentrancy attacks.

- Gas-efficient practices are followed throughout the contract.

- Overall, `USDe.sol` appears to be well-structured and follows best practices for security and code organization.

-
`EthenaMinting.sol`:

- Code Organization:

- It imports external libraries and contracts, including OpenZeppelin contracts.

- The constructor initializes contract parameters and roles.

- It contains functions for minting and redeeming USDe tokens.

- Security Measures:

- The contract enforces access control using role-based access control (RBAC) with different roles for minters, redeemers, and gatekeepers.

- Gas limits for minting and redeeming are enforced to prevent abuse.

- Signature Verification:

- It verifies the signature of orders, ensuring that the orders are signed by authorized parties.

- It uses EIP-712 for signature verification.

- Gas Efficiency:

- Gas-efficient practices are followed, and SafeERC20 is used for token transfers.

- Domain Separator:

- The contract computes the domain separator for EIP-712, enhancing security.

- Deduplication:

- The contract implements deduplication of taker orders to prevent replay attacks.

- Supported Assets:

- The contract maintains a list of supported assets.

- Custodian Addresses:

- It keeps track of custodian addresses and allows transfers to custodian wallets.

- Overall, `EthenaMinting.sol` is well-structured, secure, and follows best practices for code organization and security.

- `StakedUSDe.sol:`

The contract inherits Implementation of the ERC4626 “Tokenized Vault Standard” from OZ

-
Code Organization:

- It imports external libraries and contracts, including OpenZeppelin contracts.

- The constructor initializes contract parameters and roles.

- It contains functions for transferring rewards, managing the blacklist, rescuing tokens, and redistributing locked amounts.

- Public functions are provided to query the total assets and unvested amounts.

- The `decimals` function is overridden to return the number of decimal places.

- Custom modifiers ensure input validation and role-based access control.

- Hooks and functions are in place to enforce restrictions on specific roles and token transfers.

- `StakedUSDeV2.sol:`

-
Code Organization:

- The contract extends `StakedUSDe` and inherits its code organization structure.

- It introduces additional state variables, including `cooldowns`, `silo`, `MAX_COOLDOWN_DURATION`, and `cooldownDuration`.

- Custom modifiers, `ensureCooldownOff` and `ensureCooldownOn`, are defined to control the execution of functions based on cooldown status.

- The constructor initializes the contract and sets the cooldown duration.

- External functions are provided for withdrawing, redeeming, and performing cooldown actions for assets and shares.

- The contract enforces different behavior based on the cooldown duration, adhering to or breaking the ERC4626 standard.

- The `setCooldownDuration` function allows the admin to update the cooldown duration.

- `USDeSilo.sol:`

- The contract is primary goal of `USDeSilo.sol` is to to `hold the funds` for the `cooldown period` whn user initiate `unstaking`.

General Observations:

- Role-based access control is implemented for various functions, enhancing security.

- Gas-efficient practices, such as using SafeERC20, are followed throughout the code.

- The codebase of protocol includes comprehensive comments and region divisions for clarity.

- Note that, The use of EIP-712 for signature verification adds an extra layer of security.

- `SingleAdminAccessControl.sol:`

- EthenaMinting uses SingleAdminAccessControl rather than the standard AccessControl.

In summary, the Ethena Protocol’s codebase appears to be of high quality, with a strong focus on security and code organization.

## 3. Centralization Risks

Actually, the `Ethena` Protocol contains many roles, each with quite a few abilities. This is necessary for the Protocol’s logic and purpose.

The protocol assigns important roles like “MINTER,” “REWARDER,” and “ADMIN” to specific entities, potentially exposing the system to undue influence or risks if these roles are compromised.

So, these roles introduce several centralization risks. The most significant one is the scenario in which the `MINTER` role becomes compromised. An attacker/minter could then `mint a billion USDe` without collateral and dump them into pools, causing a black swan event that our insurance fund cannot cover.

However, `Ethena` addresses this problem by enforcing on-chain mint and redeem limitations of 100k USDe per block.”

From the documentation:

Our solution is to enforce an on chain mint and redeem limitation of 100k USDe per block. In addition, we have `GATEKEEPER` roles with the ability to disable mint/redeems and remove `MINTERS`,`REDEEMERS`. `GATEKEEPERS` acts as a safety layer in case of compromised `MINTER`/`REDEEMER`. They will be run in seperate AWS accounts not tied to our organisation, constantly checking each transaction on chain and disable mint/redeems on detecting transactions at prices not in line with the market. In case compromised `MINTERS` or `REDEEMERS` after this security implementation, a hacker can at most mint 100k USDe for no collateral, and redeem all the collateral within the contract (we will hold ~$200k max), for a max loss of $300k in a single block, before `GATEKEEPER` disable mint and redeem. The $300k loss will not materialy affect our operations.

In summary, `Ethena` actually introduces several centralization risks due to the presence of many different roles in the Protocol. However, at the same time, the team has done its best to enforce measures that reduce the largest potential attack scenario to a maximum loss of $300k, which will not materially affect the `Ethena` operations/ecosystem.

## 4. Systemic Risks

Here’s an analysis of potential systemic

- Smart Contract Vulnerability Risk:
Smart contracts can contain `vulnerabilities` that can be exploited by attackers. If a smart contract has `critical security flaws`, such as logic problems, this could lead to asset loss or `system manipulation`. I strongly recommend that, once the protocol is audited, necessary actions be taken to `mitigate any issues` identified by `C4 Wardens`

- Third-Party Dependency Risk:
Contracts rely on external data sources, such as `@openzeppelin/contracts-upgradeable`, and there is a risk that if any `issues` are found with these `dependencies` in your contracts, the `Ethena` protocol could also be affected.

I observed that `old versions` of `OpenZeppelin` are used in the project, and these should be updated to the latest version:

` "name": "@openzeppelin/contracts-upgradeable",
"description": "Secure Smart Contract library for Solidity",
"version": "4.9.2",`

The latest version is `4.9.3` (as of July 28, 2023), while the project uses version `4.9.2`.

## 5. Attack Vectors Discussed During the Audit

- Issues related to Roles (Centralization Risks). Problems with roles changing.

-
Breaking of Main Protocol Invariants

- EthenaMinting.sol - User’s signed EIP712 order, if executed, must always execute as signed. ie for mint orders, USDe is minted to user and collateral asset is removed from user based on the signed values.

- Max mint per block should never be exceeded.

- USDe.sol - Only the defined minter address can have the ability to mint USDe.

- DoS for important protocol functions/flows such as `EtehnaMinting.sol#mint()` (Minting Flow), `EtehnaMinting.sol#redeem()` (Redemption Flow), `StakedUSDe#deposit()/StakedUSDe#_deposit()` (Depositing Flow), `StakedUSDeV2#unstake()` (Unstaking Flow).

- Token transfer fails.

- Minting more than 100k USDe per block.

- Users cannot unstake/withdraw/redeem.

- Can users withdraw more than they actually are supposed to?

- Minting without providing collateral amount?

## 6. Example Report

Example of report that turned out to be invalid after I wrote a `really good Explanation and PoC`. The report explain the `unstaking` really well, so you can learn for it.

### Title: Users will not be able to `withdraw/redeem` their assets/shares from `StackedUSDeV2` contract. (Inefficient logic)

### Explanation

`StakedUSDeV2.sol` is where holders of `USDe` stablecoin can stake their stablecoin, get `stUSDe` in return and `earn yield`. The Etehna Protocol yield is paid out by having a `REWARDER` role of the staking contract send yield in `USDe`, increasing the `stUSDe` value with respect to `USDe`. This contract is a modification of the `ERC4626 standard`, with a change to vest in rewards linearly over 8 hours

When the `unstake` process is initiated, from the user’s perspective, `stUSDe` is burnt immediately, and they will be able to invoke the `withdraw()` function after `cooldown` is up to get their `USDe` in return. Behind the scenes, on `burning of stUSDe`, `USDe` is sent to a seperate USDeSilo contract to hold the funds for the `cooldown period`. And on `withdrawal`, the staking contract moves user funds from `USDeSilo` contract out to the `user's address`.

- Functions respond for `redemption`, `starting of cooldown` and `transferring of converted underlying asset to USSDeSilo contract` are cooldownAssets() and cooldownShares()

` function cooldownAssets(uint256 assets, address owner) external ensureCooldownOn returns (uint256) {
if (assets > maxWithdraw(owner)) revert ExcessiveWithdrawAmount();

uint256 shares = previewWithdraw(assets);

cooldowns[owner].cooldownEnd = uint104(block.timestamp) + cooldownDuration;
cooldowns[owner].underlyingAmount += assets;

_withdraw(_msgSender(), address(silo), owner, assets, shares);

return shares;
}

/// @notice redeem shares into assets and starts a cooldown to claim the converted underlying asset
/// @param shares shares to redeem
/// @param owner address to redeem and start cooldown, owner must allowed caller to perform this action
function cooldownShares(uint256 shares, address owner) external ensureCooldownOn returns (uint256) {
if (shares > maxRedeem(owner)) revert ExcessiveRedeemAmount();

uint256 assets = previewRedeem(shares);

cooldowns[owner].cooldownEnd = uint104(block.timestamp) + cooldownDuration;
cooldowns[owner].underlyingAmount += assets;

_withdraw(_msgSender(), address(silo), owner, assets, shares);

return assets;
}`

- After `cooldown` is finished, user can call `unstake()` to `claim the staking amount after`.

` function unstake(address receiver) external {
UserCooldown storage userCooldown = cooldowns[msg.sender];
uint256 assets = userCooldown.underlyingAmount;

if (block.timestamp >= userCooldown.cooldownEnd) {
userCooldown.cooldownEnd = 0;
userCooldown.underlyingAmount = 0;

silo.withdraw(receiver, assets);
} else {
revert InvalidCooldown();
}
}`

The function check if the cooldown is finished by `block.timestamp >= userCooldown.cooldownEnd` check.

REMEMBER: The assets are transferred from `USDeSilo` contract -> https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/USDeSilo.sol#L28-L30

Described logic above works only if the cooldown is set to number greater than zero. (aka the cooldown is active)

The `Ethena` can decide to `disable the cooldown period`, so the users to be able `unstake without cooldown period`. If this is done, the user will be able to call directly `withdraw()/redeem()` to unstake:

` function withdraw(uint256 assets, address receiver, address owner)
public
virtual
override
ensureCooldownOff
returns (uint256)
{
return super.withdraw(assets, receiver, owner);
}

/**
* @dev See {IERC4626-redeem}.
*/
function redeem(uint256 shares, address receiver, address owner)
public
virtual
override
ensureCooldownOff
returns (uint256)
{
return super.redeem(shares, receiver, owner);
}`

REMEMBER: The assets are transferred from `StakedUSDeV2` contract -> https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/USDeSilo.sol#L28-L30

### Proof of Concept

So, the problem in Ethena protocol logic aries exactly when `Ethena` decide to `disable the cooldown period`.

Let’s illustrate the following example:

Scenario

- Cooldown Period: 50 days

- Alice deposit her 10000 `USDe` tokens in `StakedUSDeV2` contract.

- Bob also deposit his 20000 `USDe` tokens in `StakedUSDeV2` contract.

- After some time Bob decide to unstake and call `cooldownAssets()` to start of cooldown period and converted underlying asset are transferred to `USSDeSilo` contract and he redeem his 20000 `USDe` tokens.

- After 30 days `Ethena` disable cooldown period.

- Now users are supposed to unstake directly from `withdraw()/redeem()`.

- But when the Bob tries to call `withdraw()/redeem()` he will not be able to get his converted underlying asset, because they are in `USDeSilo` contract.

- Alice call `withdraw()/redeem()` and get his converted underlying asset.

After all, I observed that users who have already called `cooldownAssets()/cooldownShares()` can call the `unstake()` function again to retrieve their converted underlying asset.

FJ-Riveros (Ethena) acknowledged

# Disclosures

C4 is an open organization governed by participants in the community.

C4 Audits incentivize the discovery of exploits, vulnerabilities, and bugs in smart contracts. Security researchers are rewarded at an increasing rate for finding higher-risk issues. Audit submissions are judged by a knowledgeable security researcher and solidity developer and disclosed to sponsoring developers. C4 does not conduct formal verification regarding the provided code but instead provides final verification.

C4 does not provide any guarantee or warranty regarding the security of this project. All smart contract software should be used at the sole risk and responsibility of users.

Top- Twitter
- Discord
- GitHub
- Media kit
- Terms
- Privacy
