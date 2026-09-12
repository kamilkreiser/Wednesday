# QA GATE — TIER 1, round 1 — Datasec/NexusAI RD-150 @ bec76f6

**Head:** `rd-150-falsy-setting-s55` @ `bec76f686de5415090350117437d11d1a49acb82` (on origin). **Base:** `main` @ `cd2b54397b0e83ccbd51e5b030c2ad614eb0e811`. **Range:** `cd2b543..bec76f6`, **1 commit, 4 files:** `backend/jsonStorage.js` · `__tests__/rd150-falsy-settings-round-trip.test.js` (new) · `__tests__/cost-field-validation.test.js` (modified) · `scripts/verify-expected-counts.json`. Empty delete-set.

**Why tier 1:** it changes the read path under **94 `getSetting` call sites across nine files**, product-wide, and it switches on two operator kill switches that were silently ignored until now: `red_flag_enabled` and `aiEnabled`. **A deploy of this commit changes runtime behaviour on any deployment that stored `false` or `0`.** Round 1 of 2 under the cap.

**⚠ The branch is three merges behind `main`.** It is cut from `cd2b543`; `main` has since taken RD-293 (`ae2588b`) and RD-372 (`34e7fc4`), and a NexusAI seat is about to merge RD-342 and RD-382 on top. **Read `main` with `ls-remote` at your start, name the SHA, and predict against that.**

**Worktree under test:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/rd-150-s55`. **Clone it with `git clone --no-hardlinks` into your own `mktemp -d` and work only there;** install dependencies in your clone. Never write the worktree, its `.git`, the shared `NexusAI/2_Project_Files/.git/config`, `NexusAI/2_Project_Files` (a stale snapshot under Kam's `investigate` hold), `NexusAI/Launch_Claude.command`, or any `.env`. **Red control:** `cd2b543`.

**Ticket scope, RD-150's title quoted:** *"jsonStorage.getSetting returns `value || null`, so a stored 0 or false is indistinguishable from unset — product-wide"*. **Read the ticket's comment 37340 BEFORE its description:** the description's cited consequence (`kpis.js`, the "set to something unusable" branch) is **withdrawn**, because that branch is fed by `getAllSettings()`, not `getSetting`.

## The builder's claims (NexusAI S55, READY FOR QA 2026-09-11T22:33:24Z) — claims, not evidence
1. `getSetting` no longer flattens falsy values: a stored `0`, `false` and `''` read back as themselves; an ABSENT key still reads `null`; truthy values are unaffected.
2. **Consequence 1, driven by a test:** `red_flag_enabled` stored as boolean `false` now stops the risk-alert pass (`backend/services/riskAlertScheduler.js:81`, guard `e === false || e === 'false'`). At `cd2b543` the pass ran on after the operator disabled it, and its log printed `(unset)`. The test sets a LIVE `red_flag_email_frequency`, and a control proves the pass would genuinely have run without the switch. S55 disclosed that its first draft passed for the wrong reason (frequency `'never'`).
3. **Consequence 2, READ FROM SOURCE ONLY, not driven:** `aiEnabled` (`backend/server.js:15649`): `getSetting('aiEnabled') !== false` was true for `null`, so `GET /api/setup/ai-model` reported AI **enabled** where an admin had turned it off.
4. `__tests__/cost-field-validation.test.js`'s pinned "KNOWN GAP (RD-150)" block was converted to assert the corrected round-trip, not deleted; its repetition of the wrong `kpis.js` claim was corrected in place.
5. RED at `cd2b543`: `0`, `false` and `''` came back `null`, and the disabled risk-alert pass returned `skipped=undefined`. Controls pass at base: absent → `null`; truthy unaffected.
6. **Suite:** `VERDICT: PASS — 2285/2285 tests across 118 suites (jest exit 0)`, +7 tests / +1 suite.
7. No migration: the stored bytes are unchanged; only the read changes.
8. **NOT TESTED, by its own account:** consequence 2 through the real route; a real browser; a deployed environment.

## 🔴 WHAT TO ATTACK FIRST
1. **The 94 call sites, enumerated by you at `bec76f6`.** For every `getSetting` caller, classify how it treats a value that used to arrive as `null` and now arrives as `0`, `false` or `''`: **unchanged** · **fixed** (a switch that now works) · **NEWLY WRONG** (a caller that relied on `null` for falsy — `=== null`, `?? default`, `== null`, `if (v === null) useDefault`, arithmetic on `''`, a `.length` on a number). **A caller whose behaviour turns worse is a Major at any likelihood.** A frame is load-bearing: include every file, `static/`, scripts and tests, and name the grep you used plus a planted control that proves it finds a call site.
2. **`''` specifically.** An empty string that used to read `null` now reads `''`. Find every setting a form can save as `''` and every caller that then uses it (a URL, a number, an email address, a cron expression, a model name). Drive the worst two against a real local boot.
3. **Consequence 2, through the real route:** on a local open-mode boot of THIS commit with `aiEnabled` stored as boolean `false`, `GET /api/setup/ai-model` must report AI disabled; red control at `cd2b543`. Then check every OTHER reader of `aiEnabled` (the AI endpoints themselves, not only the setup route): does "disabled" now actually refuse AI work, or does only the setup page change? State the evidence class.
4. **Consequence 1, re-derived:** re-run the builder's scheduler case at head and base, and read WHY its control is green, not only that it is. Also the STRING `'false'` path and an unset switch.
5. **The behaviour change on deploy.** A deployment that has `false` or `0` stored today will behave differently after this merge. Read what the demo and dev data stores could plausibly hold (READ ONLY; no deployed environment is touched) and list the settings whose stored falsy value will start taking effect. **This is the list a deploy decision needs; say plainly if it cannot be established from the repository.**
6. **Merge prediction, in your own clone only:** merge the `main` you read at start into the branch. Resolve ONLY `scripts/verify-expected-counts.json`, by putting it in a parseable state and running `npm run verify -- --update-counts`. Any other conflict: STOP and report it. Report the measured numbers and the full suite result on the merged tree. Nothing is pushed.
7. **Suite at head, IN THE FOREGROUND:** 2285/118, with the counts change matching the added tests exactly.

## KNOWN — do NOT report as new
The `kpis.js` example in RD-150's description is withdrawn (comment 37340; `server.js:2042`'s comment already says `getAllSettings` is a separate path) · every branch writes its own figure into `scripts/verify-expected-counts.json`, so merges conflict there · RD-342 and RD-382 passed their gates and are being merged by a NexusAI seat · RD-327 (`/api/health` build digest) is in progress on another branch · RD-388, RD-389, RD-390 · `gitleaks` is absent on this machine · `NexusAI/2_Project_Files` is a stale snapshot under Kam's hold · the Marketplace package · four Dependabot alerts on the default branch.

## Output
Findings-only: never fix, commit, push or file tickets. No `az`, no `gh`, no deployed environment. FOUND / TESTED / HOW with an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY). A control for every zero; never `rm`; head readings at start, mid and end. Remove only processes, containers and temp directories YOU create, and keep them in your own scratchpad. **Run long commands in the FOREGROUND; never end a turn waiting on a background notice.**

**Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd150-bec76f6-tier1/report.md`
**MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-150 @ bec76f6 (tier 1)`, leading with GO, GO WITH FINDINGS or NO GO. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- main 34e7fc4 · rd-150-falsy-setting-s55 bec76f6 | git ls-remote origin from NexusAI's checkout, run by Tuesday s10 | read 2026-09-12
- range cd2b543..bec76f6: an ancestor, 1 commit, 4 files, empty delete-set, worktree clean | git merge-base / rev-list / diff --stat --summary / diff --diff-filter=D / status on worktrees/rd-150-s55, run by Tuesday s10 | read 2026-09-12
- RD-150 Testing / Medium, its title as scope; comment 37340 withdraws the kpis.js example | Jira REST reads with NexusAI's creds under the read-only grant, run by Tuesday s10 | read 2026-09-12
- claims 1–8, the 94 call sites, both consequences and their line numbers | datasec-nexusai READY FOR QA 2026-09-11T22:33:24Z, read by Tuesday s10 | read 2026-09-12
- RD-293 at ae2588b, RD-372 at 34e7fc4 | HANDOVER-S57 §0 + Tuesday s10's ls-remote | read 2026-09-12
- RD-342 and RD-382 GO WITH FINDINGS, merge instructed | QA verdict mails 02:28:12Z and 02:51:51Z + Tuesday's ANSWER 02:55:26Z | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 12:57
