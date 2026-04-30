---
name: c4-contest-auditor
description: Audit Code4rena contest repositories from a C4 audit URL, including Solidity and Rust/Soroban targets. Extract intake data, lock in in-scope files, suppress known findings and out-of-scope issues, bootstrap a local audit workspace, and package only novel in-scope findings.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, smart-contracts, code4rena, audit, solidity]
    related_skills: [github-repo-management]
---

# C4 Contest Auditor

Use this skill when auditing a Code4rena contest from its C4 audit URL or from a manually copied contest page snapshot.

## Goal

Turn a C4 contest page into a scope-locked local audit workspace, then audit only the in-scope files while suppressing known findings, prior-review artifacts, and out-of-scope issues.

## When to use

- The user gives a `code4rena.com/audits/...` URL
- The user wants to bootstrap a local smart-contract audit workspace
- The user wants help filtering known findings and keeping only novel issues
- The target is a Solidity/Vyper/Yul or Rust/Soroban contest repository

## Core rules

1. Scope first, findings second.
2. Never report issues outside `in_scope_files`.
3. Suppress duplicates to `known_findings` and `known-finding-signatures.txt`.
4. Treat `V12 findings` and `Publicly known issues` as not eligible for new submissions.
5. Treat repository artifacts tagged `MERGED`, `OOS`, `REVIEWED-INVALID`, `REVIEWED-NV`, `REVIEWED-DG`, or `REVIEWED-RISK` as review history, not active findings.
6. Do not promote issues to High/Medium when the exploit depends only on privileged misconfiguration, governance sequencing, centralization risk, trusted-role abuse, or unsupported-token behavior.
7. If `requires_join=true` or no trustworthy in-scope file list is available, stop and ask for manual scope confirmation before treating findings as submission-ready.

## Workflow

Before scoring findings, identify the contest language/runtime from the repo and README. This skill supports Solidity/Vyper/Yul and Rust/Soroban C4 repos.

### 1. Intake extraction

Preferred path:

```bash
python3 ~/.hermes/skills/software-development/c4-contest-auditor/scripts/c4_intake.py "https://code4rena.com/audits/<slug>" --output ./intake.json
```

Fallback for access-restricted contests:

```bash
python3 ~/.hermes/skills/software-development/c4-contest-auditor/scripts/parse_c4_snapshot.py ./c4_snapshot.md --audit-url "https://code4rena.com/audits/<slug>" --repo-url "https://github.com/<owner>/<repo>" --output ./intake.json
```

Read from `intake.json` before auditing:
- `repo_url`
- `in_scope_files`
- `known_findings`
- `out_of_scope_paths`
- `intake_notes`
- `requires_join`

If the C4 page is join-gated or the extracted scope is obviously partial, do not stop at the empty page or trust the partial `intake.json`. Probe the contest repository README and any linked `scope.txt` / `out_of_scope.txt` artifacts to recover machine-readable scope. When a local repo already contains `scope.txt` / `out_of_scope.txt`, prefer generating a corrected local intake (for example `intake.local.json`) from those files before running `start_audit.py`, and include public-known issues / V12 runs as known findings. For Rust/Soroban contests, extract `.rs` in-scope paths the same way Solidity contests extract `.sol` paths.

### 2. Audit bootstrap

If cloning from the intake metadata:

```bash
python3 ~/.hermes/skills/software-development/c4-contest-auditor/scripts/start_audit.py --intake-json ./intake.json --workspace ./workbench --output ./audit-context
```

If the repository already exists locally:

```bash
python3 ~/.hermes/skills/software-development/c4-contest-auditor/scripts/start_audit.py --intake-json ./intake.json --repo-path /abs/path/to/local/repo --output ./audit-context
```

Expected outputs:
- `audit-context/<slug>/audit-context.json`
- `audit-context/<slug>/in-scope-files.txt`
- `audit-context/<slug>/known-finding-signatures.txt`
- `audit-context/<slug>/heuristic-hits.json`
- `audit-context/<slug>/audit-notes.md`

### 3. Audit-RAG assisted lead ledger / triage

Use the local audit-rag workbench as a thin state backend for active C4 leads. The detailed implementation and maintenance rules live in the separate `audit-rag-workbench-maintainer` skill; keep this C4 skill focused on when to call it during an audit.

Local defaults:
- audit-rag repo: `/Users/qwe/Audit/audit-rag`
- CLI: `cd /Users/qwe/Audit/audit-rag && source .venv/bin/activate && python -m audit_rag.cli.main ...`

Active-audit calling contract:
```bash
python -m audit_rag.cli.main add-lead <contest-slug> "<short lead title>" --component "<component-family>" --text "<candidate issue statement>"
python -m audit_rag.cli.main triage-lead <contest-slug> <lead-id>
python -m audit_rag.cli.main suppress-check <contest-slug> <lead-id>
python -m audit_rag.cli.main update-lead <contest-slug> <lead-id> [--status ...] [--current-blocker ...]
python -m audit_rag.cli.main export-contest-summary <contest-slug>
```

Rules while auditing:
- Record every non-trivial lead with `add-lead` before deep work.
- Use `triage-lead` for strong/suspicious leads and `suppress-check` for weak, duplicate-looking, QA/Low-looking, or false-positive-prone leads.
- Treat audit-rag output as navigation/evidence only, never as proof or a report citation. Current contest scope, reachability, impact, duplicate review, and runnable PoC remain mandatory.
- Keep active audit knowledge under `/Users/qwe/Audit/audit-rag/data/provisional/contests/<contest-slug>/`; do not write active-audit discoveries directly into normalized/eval data.
- Update lead status after PoC, duplicate review, or final decision with `update-lead`; export a summary when handing off or resuming.

### 4. Manual audit

Use `heuristic-hits.json` and audit-rag triage output only as navigation aids.

Prioritize:
- accounting invariants and token decimals
- authorization boundaries on admin/executor roles
- slippage and min-out checks around swaps/bridges
- stale or manipulated oracle usage
- reentrancy around external calls
- upgradeability, initialization, and storage collisions
- for Rust/Soroban: TTL expiry behavior, storage defaults after expiry, bytes32/address conversion, custom-account auth (`__check_auth`), and pull-mode delivery/compose semantics

If the repo is Rust-based and `cargo` is available, run the project's documented test command locally before finalizing claims. Use tests to distinguish intended behavior from exploitable behavior, and add temporary local tests only for validation — remove them after confirming the behavior.

### 5. Output policy

Always create in the target repository:
- `<repo>/findings/`
- `<repo>/finds/QA-report.md`

Policy:
- Active High/Medium findings: one markdown file per issue under `<repo>/findings/`
- QA/Low/governance/centralization-risk items: append to `<repo>/finds/QA-report.md`; for C4 submission packaging, consolidate all Low/QA items into a single `<repo>/submissions/QA-report.md` because C4 expects low-risk/non-critical findings to be submitted once as one combined report.
- Review history, invalid, duplicate, merged, downgraded, or out-of-scope items: keep out of final active outputs

Final submission packaging under `<repo>/submissions/`:
- prepare English submission markdowns for active HM findings and one consolidated QA/Low report at `<repo>/submissions/QA-report.md` when low-risk/non-critical items exist
- for every newly confirmed HM finding, also create a review prompt markdown under `<repo>/submissions/review-prompts/` so the user can hand it to another AI for independent validation
- for every final English HM submission, also create a Chinese translation under `<repo>/submissions/zh/` for the user's final confirmation; keep code, commands, revert strings, file paths, and URLs unchanged
- inline PoC source in fenced blocks using the appropriate language such as `solidity` or `rust` when a submission depends on runnable PoC code
- attachment copies can still live under `<repo>/submissions/poc/`

## Required sections for each final finding

Default to C4-style English writeups for submission files.

For High/Medium findings, match the tone and structure commonly seen in rewarded C4 reports:
1. Markdown title in the form `[M-01] ...` or `[H-01] ...`
2. `## Finding description and impact`
3. concise exploit narrative grounded in exact code paths
4. short quoted code snippets only where they materially clarify the bug
5. `## Proof of Concept`
6. `## Recommended mitigation steps`

Important style rules:
- Prefer concise, judge-friendly English over bilingual output in submission files
- Lead with the broken invariant / security property, not with background explanation
- Explain why the bug matters before proposing fixes
- Use exact file paths and function names
- For C4 final submission markdowns, use the contest repository's default branch form for `Links to root cause`, normally `https://github.com/<owner>/<repo>/blob/main/<path>#Lx-Ly`, unless the user explicitly asks for pinned commit links.
- Keep `Links to root cause` narrow: include only the code lines that directly cause the vulnerability, not every supporting, downstream-impact, PoC, or library reference.
- C4's submission form labels this required field as `Links to root cause`; prefer that exact heading over `Code references` in final submission markdowns.
- Avoid speculative wording like "may be vulnerable" when you have validation; be direct
- Avoid inflated severity language; let the exploit path speak for itself
- For QA notes kept outside HM submissions, a looser format is acceptable

## Linked files

- `references/c4-intake-notes.md`
- `scripts/c4_intake.py`
- `scripts/parse_c4_snapshot.py`
- `scripts/start_audit.py`

## Severity calibration notes

Use Code4rena severity rules conservatively:
- High: direct non-privileged asset compromise with a concrete attack path
- Medium: protocol function/availability impact or value leakage with a credible, stated attack path
- QA/Low: user-mistake-dependent issues, trusted-role/configuration mistakes, governance/centralization risks, event-only issues, and low-signal spec mismatches

Do not over-rate findings that depend on:
- stray balances from mistaken transfers
- misconfigured trusted roles or owner-only configuration mistakes
- purely event/logging side effects without broader protocol impact

## Rust / Soroban contests

This skill also supports Rust/Soroban Code4rena contests.

Recommended local validation flow:
- inspect the contest README for prerequisites and test commands
- install Rust with `rustup` if missing
- ensure the required target is installed if the repo specifies one, e.g. `wasm32v1-none`
- run `cargo test` from the repo's Rust workspace before making stronger exploit claims
- if the environment lacks `stellar` CLI, continue with cargo-based validation first and treat WASM build validation as optional follow-up
- when `stellar` CLI is required and Homebrew search/install is slow or unavailable, `cargo install --locked stellar-cli --version <version>` is a viable fallback; set generous cargo network timeouts/retries for large dependency builds
- for Stellar CLI v25-style builds, `stellar contract build --optimize --locked --out-dir target/stellar` may write optimized `.wasm` files to the out-dir without the `.optimized.wasm` suffix; if a contest C4 harness imports `target/wasm32v1-none/release/*.optimized.wasm`, copy or alias the optimized outputs back to the harness-expected paths before running `cargo test --package <c4-package>`
- check `contractimport!` paths relative to the source file, not just the repository root; a `tests/c4/src/lib.rs` import such as `../../target/...` resolves under `tests/target/...`, so the harness may need WASM aliases in both root `target/...` and `tests/target/...`

For Stellar/Soroban repos specifically, pay extra attention to:
- TTL-based storage expiry and whether expired persistent state silently falls back to defaults
- custom account auth paths such as `__check_auth`
- message verification threshold logic
- fee prefunding/accounting paths that use global contract balances

## C4 severity guardrails

Before labeling a finding High/Medium, cross-check against C4 severity rules:
- direct theft/compromise with a concrete attack path may qualify for High
- protocol function or availability impact may qualify for Medium
- findings that depend mainly on user mistake, admin/config mistakes, governance trust assumptions, or other centralization conditions are usually QA/Low instead

When in doubt:
- keep config-only and trusted-role misuse issues in QA
- prefer evidence from local tests or a minimal reproducible scenario over purely static speculation

## Notes for Hermes use

- Prefer this skill over ad-hoc contest parsing because it preserves scope discipline.
- If the user only wants exploratory review, you can still use the intake and bootstrap stages without producing submission-ready findings.
- Keep the Hermes version thin; the scripts and reference note are the operational source of truth.
- The bundled Hermes version has been adapted to support Rust/Soroban contests in addition to Solidity/Vyper/Yul by extracting `.rs` scope entries and falling back to Rust source discovery when needed.

## Validation discipline learned from live use

When evaluating a candidate finding for Code4rena submission:

1. Separate issues into three buckets:
   - submission-ready HM candidates
   - QA/Low issues
   - research leads not ready for submission
2. Do not submit a High/Medium candidate if local validation fails or if the exploit path remains only theoretical.
3. For Rust/Soroban contests, prefer `cargo test`-backed validation when possible.
4. If a claim looks strong in code review but cannot be reproduced locally, downgrade it to a research note instead of forcing it into a submission.
5. If an issue depends mainly on user mistake, stray balances, or privileged misconfiguration, compare it against C4 severity guidance before classifying it as HM.
6. Before final submission, convert winning candidates into a dedicated `submissions/` package and rewrite them in concise C4 report style rather than verbose audit-template style.
7. If a candidate finding is currently supported only by composing two or more prerequisite behaviors (for example: grace-period validity + same-nonce overwrite), prefer adding a focused end-to-end local test that reproduces the full attacker path in one place.
8. For endpoint/message-flow issues, the strongest PoC is usually an attack-path test that shows the honest flow first succeeds, then an attacker-controlled or stale component mutates state, and finally the honest delivery/clear step fails with the exact contract error.
9. After such a focused test passes, rewrite the submission `## Proof of Concept` section to center the direct reproduction test first, and mention the underlying prerequisite tests only as supporting evidence.
10. If a locally passing PoC proves a bug but a V12/public-known item explicitly covers the same root cause and affected function, treat it as a suppressed duplicate even if the local reproduction is stronger or narrower. Do not leave it in active `findings/` or package it under `submissions/`; instead mark the scratch writeup/status as `SUPPRESSED-DUPLICATE` (or move it to internal notes), record the exact known title/function overlap in `audit-context/<slug>/...`, and continue searching for materially different root causes.
11. When a new-direction sweep produces mostly duplicate/weak leads, write a short triage summary under `audit-context/<slug>/` that lists: validated-but-duplicate PoCs, V12/known suppression titles, weak leads with overlap reasons, audit-rag output pointers, and the current local validation command/result. This prevents later sessions from re-promoting the same reproduced but ineligible candidate.
12. If local review dries up, run an external-reference sweep instead of only rereading the same code: search audit-rag and public reports for adjacent protocols/runtimes, extract reusable invariants, then map them back to exact local entrypoints. For Rust/Soroban lending contests, especially compare alternate value-moving entrypoints against normal operation guards: pool/reserve status (`paused`, `frozen`, `active`), whitelist/blacklist checks, interest/reward index updates, and settlement verification. A strong external analogy is only a lead; require a local PoC and a narrow duplicate check against V12/known. If the root cause is adjacent but not identical to a known item (for example global pause missing in flash loans versus reserve-local frozen status missing in flash loans), keep it as `ACTIVE-CANDIDATE` with an explicit adversarial duplicate-review note rather than immediately suppressing or submitting.
13. For split-phase flows such as `prepare`/`execute`, `commit`/`settle`, or `authorize`/`consume`, audit every state assumption captured at phase 1 against current state at phase 2. If phase 1 checks lifecycle/emergency controls (`paused`, `frozen`, `active`, whitelist/blacklist, price tolerance, health factor), verify which controls phase 2 revalidates after refetching state. A strong candidate can exist when phase 2 correctly rechecks one dimension (for example health factor or global pause) but misses a different reserve-local lifecycle flag. When reporting, frame only the dimension proven by PoC: if the test proves collateral-reserve pause after authorization, do not claim debt-reserve pause, inactive-state bypass, or healthy-account liquidation unless separate tests prove them.
14. For swap/slippage findings involving protocol fees, distinguish gross DEX output from net amount credited to the user. If `min_amount_out` is checked before deducting a bounded protocol fee and final solvency/health checks still run, default to QA/Low unless the PoC proves attacker-capturable value, direct protocol loss, or a downstream invariant break. Keep the validated PoC and rationale in `finds/QA-report.md` rather than forcing it into an HM submission.

## Submission style learned from rewarded C4 reports

For submission-ready High/Medium findings:
- Use English-only by default unless the user explicitly wants bilingual copies.
- Format the title as `[M-01] ...` or `[H-01] ...`.
- Use exactly these main sections:
  - `## Finding description and impact`
  - `## Proof of Concept`
  - `## Recommended mitigation steps`
- Lead with the broken invariant and exploit path, not with long background context.
- Keep code excerpts short and only include the lines that materially prove the bug.
- Prefer the phrasing style common in rewarded C4 reports:
  - direct statement of the bug
  - concrete attacker path
  - concrete consequence
  - short remediation
- Avoid mixing QA/Low template language into HM submissions.
- Maintain a separate status note for strong but unproven ideas; do not force them into submission-ready files.

For each confirmed High/Medium finding, produce two user-review artifacts in addition to the English submission:
1. `<repo>/submissions/review-prompts/<finding-id>-review-prompt.md`
   - Purpose: a self-contained prompt that the user can paste into another AI for independent review.
   - Include contest name/URL, repository GitHub URL, uploaded submission markdown filename, uploaded PoC markdown filename, finding title, core claim, narrow `Links to root cause` URLs, external docs assumptions, PoC steps, latest validation commands/results, severity rationale, and explicit questions such as: root cause accuracy, PoC validity, Medium suitability, OOS/duplicate/QA risks, missing references, and exact blockers if it should not be submitted. For C4 final/review artifacts, prefer the default branch URL form such as `blob/main` unless the user asks for pinned commit links. For webpage AI review, write the runnable PoC source into a separate markdown file under `<repo>/submissions/poc/` and phrase the prompt as if the submission and PoC markdowns have been uploaded, not as local filesystem paths. Keep V12/public-known duplicate checks as internal audit memory/notes; do not add that section to the review prompt or final report unless the user explicitly asks.
   - The prompt should ask the reviewer to be adversarial and to focus on whether the issue is submission-ready, not to do a broad new audit.
2. `<repo>/submissions/zh/<finding-id>.zh.md`
   - Purpose: a Chinese translation of the final English submission for the user's final confirmation.
   - Keep all code blocks, commands, revert strings, file paths, constants, function names, and URLs exactly unchanged.
   - Translate explanatory prose into clear Chinese, preserving the C4 sections and severity rationale.
   - Do not submit the Chinese version to C4 unless the user explicitly asks; the canonical C4 submission remains the English markdown under `<repo>/submissions/`.

## Practical lessons from the LayerZero Stellar contest

- A stronger version of a fee-accounting issue may exist even when a weaker "stray balance refund" variant is only QA/Low; check whether the same root cause can steal funds from the protocol's intended prefund flow.
- TTL-based replay or expiry theories in Soroban should not be treated as submission-ready until the expiry behavior is reproduced or otherwise nailed down with much stronger evidence.


## Rust/Soroban contest notes

This skill was updated after use on the live Code4rena contest `2026-04-layerzero-stellar-endpoint`.

What changed:
- Intake parsing now recognizes Rust `.rs` in-scope and out-of-scope paths, not just Solidity/Vyper/Yul.
- Bootstrap fallback discovery now supports Rust/Soroban repositories in addition to Solidity repos.
- The skill is suitable for Soroban/Rust contests where C4 scope is published in README tables or `scope.txt`.

Practical validation workflow for Rust contests:
1. Run intake and bootstrap first, even if the audit page is join-gated or the C4 page fetch times out.
2. Read the repository README for scope, prerequisites, and build/test commands.
3. If `cargo` is missing, install Rust via `rustup` and ensure the repo's pinned toolchain can be resolved.
4. If a repository `rust-toolchain.toml` points at `stable` and rustup auto-update fails with a component conflict such as `failed to install component: 'rust-src'`, list installed toolchains and try a known installed toolchain for discovery/compile checks, e.g. `RUSTUP_TOOLCHAIN=<installed-toolchain> cargo ...`. Record the workaround in `audit-context/<slug>/first-pass-notes.md`; do not silently assume the default toolchain is usable.
5. For this class of project, run `cargo test` from the workspace root that contains the Rust crates, but if the shipped broad unit-test baseline is broken by test harness/generated-binding errors, record the failing baseline and use the contest-provided C4 PoC harness or a narrower package-specific command as the validation gate for candidate findings.
6. `stellar contract build` may still require Stellar CLI separately; do not block static review or cargo-only validation on missing Stellar CLI, but mark WASM/C4 harness validation as blocked until `stellar` is installed and optimized WASMs can be generated.
7. For behavior validation, it is acceptable to add a temporary focused test locally, run it, and then revert the test addition after confirming the behavior.
- For Rust/Soroban Code4rena contests, the contest page may be join-gated while the repository README still exposes the full in-scope file list; use the repo README as a fallback source of truth for scope extraction.
- The bundled scripts support `.rs` in-scope extraction and Rust source fallback discovery, so this skill now works for Soroban-style contests in addition to Solidity/Vyper/Yul.
- If the environment lacks `cargo`, you can still complete intake, scope locking, hotspot discovery, and static review; just label dynamic validation as blocked by missing Rust toolchain.

## Practical lessons from the Monetrix contest

This skill was updated after use on the live Code4rena contest `2026-04-monetrix`.

Scope and bootstrap lessons:
- The audit page/intake extractor can return a partial scope even when the local repository has the complete `scope.txt`. If the extracted in-scope file count is suspiciously small, compare it against local `scope.txt` / README before auditing.
- For existing local repos, it is useful to write a corrected `intake.local.json` from `scope.txt`, `out_of_scope.txt`, README public-known issues, and V12 links, then run `start_audit.py --intake-json ./intake.local.json --repo-path <repo> --output ./audit-context`.
- If a shell command with a destructive prefix such as `rm -rf` is blocked/denied, do not retry that exact command. Continue with non-destructive generation or narrower operations.

Audit-RAG lessons:
- audit-rag is the stateful backend for active audit leads, but this C4 skill should only keep the thin calling contract. Full repo/CLI/schema maintenance belongs to `audit-rag-workbench-maintainer`.
- Use `add-lead`, `triage-lead`, `suppress-check`, `update-lead`, and `export-contest-summary` during live audits instead of relying on one-off `triage-issue` calls.
- Keep active-audit discoveries provisional until final outcome and manual curation; do not write them directly to normalized/eval data.

Foundry validation lessons:
- `forge test` may update `foundry.lock` and install submodules/dependencies; note this in final status instead of assuming a clean git tree.
- Fork tests can fail for environment/RPC reasons while unit/invariant suites pass. Record the specific failing suite rather than treating the entire baseline as broken.

Monetrix-specific candidate triage patterns:
- HyperCore bridge / CoreWriter `sendAsset` flows need extra scrutiny for asynchronous or silently dropped L1 actions. Watch for EVM-side accounting updates before the L1 effect can be confirmed.
- For bridge-to-EVM of non-HYPE tokens, check whether core-side HYPE gas is required and whether the protocol preconditions enforce it.
- When `spotBalance` exposes `total` and `hold`, verify whether bridge/send actions can spend held balance. A guard that checks only `total` may not actually prevent a silent drop.
- Treat Operator inaction, bad Operator parameters, UPGRADER replacement, mutable config, and V12-listed issues as suppression risks first; frame candidates around contract-side invariant failure only when normal operator actions plus incomplete preconditions can cause user-visible impact.

Monetrix PoC/report packaging lessons:
- Keep artifact boundaries strict:
  - `audit-context/`: internal process evidence, including V12/public-known checks, raw RAG outputs, local paths, docs caches, and scratch notes.
  - `findings/`: internal candidate writeups may preserve process notes while the issue is still being shaped.
  - `submissions/`: judge-facing canonical English/Chinese submissions; no local machine paths, no audit-rag notes, and no V12/public-known diligence section unless explicitly requested.
  - `submissions/review-prompts/`: independent reviewer prompts; phrase inputs as uploaded markdown files for webpage AI review and avoid local repo paths.
  - `submissions/poc/`: upload-friendly PoC markdown files containing run command, scenario summary, and full runnable source in a fenced code block. Do not include `Latest local result` in final-facing PoC/report artifacts unless the user explicitly asks for it.
- For C4 repos that ship `test/c4/C4Submission.t.sol`, put the HM proof inside the required `test_submissionValidity()` function and run `forge test --match-path "test/c4/C4Submission.t.sol" -vvv` as the primary verification gate.
- In final C4 reports, do not include a `Latest local result` block inside the `## Proof of Concept` section. Keep the run command and PoC steps/source; store validation output in internal notes, review prompts, or separate PoC artifacts only when useful.
- To model HyperCore asynchronous failures in Foundry, a no-op `CORE_WRITER` mock is acceptable when the issue is specifically that the EVM transaction/log can succeed while the L1 action has no confirmed effect. Pair this with explicit assertions that the expected EVM-side token balance did not arrive.
- For bridge accounting bugs, the strongest PoC shape is: normal deposit/bridge out succeeds, user redemption creates a shortfall, L1 read precompile is mocked to satisfy the flawed guard, bridge-from-L1 mutates accounting, no EVM funds arrive, retry reverts because accounting was cleared, and the user claim remains blocked after cooldown.
- When relying on `SpotBalance.total` vs `hold`, mock both fields in the PoC response and explain why `total == hold` represents non-spendable/held balance passing a flawed total-only guard.
- Before finalizing a bridge/CoreWriter finding, fetch and locally save the V12 public run HTML, extract listed finding IDs/titles, and internally confirm no matching bridge-principal / `sendAsset` / accounting-before-confirmation issue appears. Keep this as audit diligence only; do not include a V12/public-known check section in final reports or review prompts unless the user explicitly asks for it.
- In the final writeup, keep `Links to root cause` focused on the actual bug sites. For Monetrix bridge/CoreWriter findings, this usually means the premature state mutation and the flawed L1 availability guard; supporting docs, action encoding, and downstream payout failures can stay in the narrative without being listed as root-cause links.
- For Hyperliquid documentation, prefer fetching GitBook pages with the `.md` suffix or `?format=markdown` and save them under `audit-context/<slug>/`. Use the page's `?ask=<question>` helper only for targeted clarification, and cite the canonical docs URL in the submission rather than the local cache.
- For CoreWriter/asynchronous-action findings, support the claim with both official docs and local code: docs should establish that CoreWriter emits a log processed later by HyperCore and that CoreWriter actions are processed after the EVM block; local code should establish the exact action encoding and the protocol's premature state mutation.
- Before finalizing a submission markdown, run a quick QA pass that checks: required C4 sections exist, `Links to root cause` uses only direct root-cause GitHub line links on the default branch unless the user requests pinned links, no speculative wording such as `may/might/could/possibly/probably/likely` remains in validated claims, and the `## Proof of Concept` section has no `Latest local result` block unless explicitly requested.
- Before handing artifacts to the user or a webpage AI reviewer, run a source-hygiene pass:
  - final `submissions/` HM reports contain no `/Users/qwe` local paths
  - final `submissions/` HM reports contain no `V12/public-known check` section
  - final `submissions/` HM reports contain no `Audit-RAG triage note`
  - review prompts contain the public GitHub repository URL, not a local repo path
  - review prompts refer to uploaded submission/PoC markdown filenames, not local filesystem paths
  - PoC markdown exists under `submissions/poc/` and its fenced code block is closed
  - inline PoC snippets copied from line-numbered `read_file` output have been cleaned so they do not contain leading `12|` / `   13|` artifacts; search final artifacts with a pattern like `^[[:space:]]*[0-9]+\\|` when in doubt
  - root-cause GitHub links use `blob/main` unless the user explicitly asks for pinned commit permalinks
- For Monetrix/Foundry validation, use `forge test --match-path "test/c4/C4Submission.t.sol" -vvv` as the submission gate and `forge test --no-match-path "test/MonetrixFork.t.sol"` as the non-fork baseline. If full `forge test` only fails in `test/MonetrixFork.t.sol` setup, record it as an environment/fork failure instead of blocking the Medium submission.
- If `forge test` changes `foundry.lock`, mention it in the final status instead of assuming the git tree remained clean.
