# Gate brief: GATE AT1 = tier-1 BATCH of three Spark-pass PRs: #1630 (KS-1653), #1631 (KS-1639), #1632 (KS-1661). Opus, round 1 of 2

Commissioned by Wednesday after Seat C 27th's READY FOR GATE (14:54Z). The author's CLAIM is beside this brief: `C27_READY_1454Z.txt` (read it WHOLE). Each PR's commit 1 is a Spark (local model) pass that Wednesday read at source and held: the READY files are in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/` (`READY_KS-1653-STUBTRANSFERSCOPE-1_*`, `READY_KS-1639-TEXTFALSEINACTIVE-1_*`, `READY_KS-1661-SIMULATEDHEAL-1_*`), and the Spark screen report is `0_Brain/reference/2026-10-18_spark-screen/SCREEN_15.md`. **#1631's commit 2 (cell F4) is the SEAT's own**, not the Spark's. Secuura only. #1634 (KS-1658) is NOT in this batch.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Make your clone INSIDE THIS SESSION'S SCRATCHPAD: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a3368218-953e-40df-ac8f-2e5abee5552f/scratchpad/gate_at1/`. Use `git clone --shared` from Wednesday's cache clone `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src`, then fetch `refs/pull/1630/head`, `refs/pull/1631/head` and `refs/pull/1632/head` with that clone's core.sshCommand. **EVERY npm / npx / vitest / jest / tsc command runs INTO your clone (`--prefix`, `--root`, or `node <clone>/node_modules/.bin/<tool>` with absolute paths). NEVER `npm exec` from your cwd: your cwd is Wednesday's tree, and a GO on your verdict is REFUSED by a tool if a stray appears there.** Build `packages/shared` first. Ports: 55490-55499.

**Heads (Wednesday's ls-remote via the cache clone, 01:5x AEDT 2026-10-20):** #1630 `19bb05069f03c8b6e9c35a2e0960cb3030dcf289` · #1631 `40ab71dd0fec5543722fedae2c5b5c5cd3d85ac1` · #1632 `77e5c5472534b6e4c817890640c4a0f6da291705` · develop `88b8ceb9f3041672d9575b40c09869d45ab1c111`. Re-read all four at start and before the verdict. The author's trees (each alone on live develop): #1630 `8de20974a299`, #1631 `0653cef42825`, #1632 `fc1cd1546a96`; stacked in merge order 1630, 1631, 1632: `198e44b77a54` (the author's figures).

## Questions, per PR (each with its instrument; name what you did NOT run)
1. **#1630 KS-1653** (auth `routes/users.ts` `hasUsersStubScope` also admits `documents:transfer-custody`). This WIDENS a security gate by one scope.
   - Enumerate every caller and every connector type that can hold `documents:transfer-custody` today (api-gateway `platform.ts` S_CONNECTOR_SCOPES and any other mint).
   - Say whether any holder of that scope who could NOT reach `POST /api/users/stub` before can reach it now.
   - The ticket's Recommendation chose exactly this change: confirm the diff does nothing more.
   - The author says C1 is the admission-half red that gate AJ1 N3 found missing: confirm C1 reds when `certifications:write` admission is removed.
2. **#1631 KS-1639** (security `converters.ts` `rowToApiKey` reads a text `is_active` as active only for `t` or `true`, trimmed, any case).
   - Does any REAL path feed a string `is_active` (a `::text` cast, `row_to_json`, a raw query, a cache layer, a fixture loader)? Name them or measure that there are none.
   - The Spark cells plus the seat's F4 (anchors): run F4's two anchor-drop mutants yourself.
   - Confirm `''`, unknown strings, `null` and an absent column all read INACTIVE (fail closed), and real booleans are unchanged.
3. **#1632 KS-1661** (originate v1 `verification.ts` and v2 `verificationV2.ts` heal paths refuse a truthy INCOMING `chain.simulated`).
   - It is the Spark's first two-product-file pass. Confirm both hunks, and that the guard is TRUTHY, not `=== true`.
   - The author reports SEVEN neighbouring guards in these two functions pinned by no test. Confirm the count with your own mutants, and list them as a note (not a blocker for this PR).
   - #1632's diff has no `index` lines: verify the applied result equals the tip's tree yourself.
4. **Batch:**
   - The three are file-disjoint: confirm from the three-dot diffs.
   - Merge-tree each on LIVE develop, and the stack in order 1630, 1631, 1632.
   - Run the auth, security and originate full suites on the stacked tree, and compare by cell NAME against develop, not by totals.
   - Type-check the new test files.
   - Note the author's load-average timeouts (ks578, ks949) and re-run any file that times out alone before calling it a red.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO|MIXED> (tier 1 batch, round 1 of 2; develop <sha>; #1630 <GO|...>, #1631 <...>, #1632 <...>; N blockers, M notes)`. Then a per-PR verdict line each with its head and its landing tree on live develop; BLUF; findings numbered B1.. and N1.. naming the PR; what was tested and HOW (commands, controls); NOT RUN. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`, no push, nothing on any server. No `cd`, no `rm`, no stderr to /dev/null, no Docker. Every zero gets a positive control. Before you finish run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/ (there must be none).
