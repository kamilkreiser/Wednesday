# QA Agent Invocation Brief — Datasec/NexusAI, BATCHED GATE: RD-516 fix round (RD-585 + RD-541) and RD-604 — TIER 1 (RD-541) / THROUGH-CODE (RD-585, RD-604)

**Written by Tuesday 2026-09-21.** Commissioned on S76D's READY FOR QA for RD-585/RD-541 (`b966634`) and RD-604.

SELF-CHECK: read whole by Tuesday at 2026-09-21 18:54 AEST — the RD-604 provenance line was stale (said not at origin) and is corrected; no other contradiction found between BLUF, targets, sequence and provenance; Kam rulings C-126/C-127 delivered

## Charter
Read `fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not build this and you
owe it nothing. **Everything below that reports what the builder says is a CLAIM.**

**ONE batched gate, TWO disjoint targets, ONE session** — Kam's standing rule of 2026-09-18: batch gates, never pay for
the same floor twice. The targets share no file. **Give a SEPARATE verdict for each: A GO / NO-GO, B GO / NO-GO.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
none — C-126 and C-127 delivered.

## PRIOR ROUND
PRIOR ROUND: round 2 gated `aaffbb9`, verdict GO (through-code), with R7 and R8 left red on purpose — R7 for RD-585, R8 for RD-541.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd516-aaffbb9-round2/`
Findings carried forward and their disposition: R7 (RD-585) — the cell is re-aimed on `ae98c74` · R8 (RD-541) — one limiter on `b966634`.
**Do not re-drive what round 1 (`…/2026-09-21-rd516-f4264e5-tier1/`) and round 2 proved:** the 26 refusal classes, the absence clause, the F-2 table.

## 1. Targets — verified at commission from the object store
### TARGET A — RD-516 fix round
- **Branch `rd-516-ai-test-ssrf-s73` @ `b9666342f50646fbe44aefcdeeaa732dea10dccb`** (short `b966634`), at origin.
- **Range under test: `059f0a8..b966634`, exactly TWO commits, exactly TWO files:**
  - `ae98c74` = **RD-585**, touching only `__tests__/rd516-ai-test-ssrf.test.js`;
  - `b966634` = **RD-541**, touching only `backend/server.js`.
- `059f0a8` is a **forward merge of main `aae041a` into the branch**, with parents `aaffbb9` + `aae041a`, and the builder
  claims zero conflicts. **Measured at commission, per file, as blob ids across merge-base `60c76d7` / `aaffbb9` / `aae041a` / `059f0a8`:**
  - every file except one takes exactly one side's blob;
  - `__tests__/helpers/rd516-net-harness-preload.js` is identical on both sides;
  - **`backend/server.js` is the ONLY true content merge** (`617722c` + `a5cf76b` → `a072398`).
  **Confirm that content merge carried both sides' hunks and nothing else** — above all, that main's RD-518 server
  changes and the branch's RD-516 server changes are both present and neither was edited in the merge.
- **`backend/services/authEnforcement.js` is byte-unchanged** (blob `ca764a4`, identical at `aae041a`, `059f0a8` and
  `b966634`). RD-594 (`adminGateRefuses`, which lives there at `:634`) stays excluded, as in the earlier gates.
- **NOT on main. Nothing merges on your word or the builder's.**

### TARGET B — RD-604
- **Branch `rd-604-rd423-timer-s76d` @ `172abc8308eeb71d3ffa1a1626ef069559876b98`**, one commit off main `aae041a`, TEST-ONLY, exactly ONE file:
  `__tests__/rd423-test-ai-does-not-crash-server.test.js`.
- The launcher refuses until Tuesday pins this SHA from origin. The delta shape is enforced at launch; the content is yours to judge.

### Both targets
- **No worktree is pinned. Build your own INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store at each
  sha:** `git -C <repo> archive <sha> | tar -x -C <a fresh mktemp -d under your project>`. Archive is read-only on the
  repo. **Never run `git worktree add`, `checkout`, `fetch`, `stash`, `clean` or a commit against the NexusAI repo.**
  Its working checkout is elsewhere and dirty: pin to the sha, never `HEAD`.
- The repo is `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`.

## 2. Why this tier, and who is waiting
- **TIER 1 for RD-541.** It changes the product rate limit on `POST /api/setup/ai-test`, a security route that
  anonymous callers can reach during the open first-run window (C-42).
- **THROUGH-CODE for RD-585 and RD-604.** Both are test-only follow-ups.
- 🔴 **RD-516's merge is waiting on this gate.** C-126 fixes the sequence:
  1. this batched gate;
  2. **RD-604 merges first**;
  3. main is forward-merged into RD-516 and verified **GREEN**;
  4. RD-516's merge is Tuesday's GO under C-127.

  **So a GO on A does NOT by itself clear RD-516's merge. Say what your two verdicts mean for that merge, in those terms.**

## 3. TARGET A / RD-541 — ONE limiter, and it must be the one that never skips (TIER 1)
Claimed:
- `aiDeploymentTestLimiter` (RD-464 r2, `8237526`, inline on the route, `skip` while AI is off) is removed: its const and its mount.
- `aiTestLimiter` (`app.use`, no skip) survives, and now reads `AI_DEPLOYMENT_TEST_LIMIT` (`backend/services/aiReadiness.js:49`, `{ windowMs: 600000, max: 5 }`).
- C-106 / C-74 / RD-545: a limiter that skips must never be the only one.

**Answer each of these with a measurement:**
1. **Does anonymous traffic with AI OFF now count against the limit?** It must. Drive it on a local run: anonymous, AI
   off, six tests from one address. The 6th must be **429**, and zero outbound connections may reach the stand-in.
   Then do the same with AI on, and across an off → on → off toggle inside one window.
2. **Is there exactly ONE limiter on the route?** Measure it three ways, not only through R8:
   - the source;
   - the **runtime middleware stack** of the booted app, if reachable;
   - the behaviour.

   🔴 **R8 is a source regex.** It counts `app.use('/api/setup/ai-test'…)` plus `app.post('/api/setup/ai-test', <word ending "limiter">`.
   **Say what it would MISS:**
   - a limiter under another name;
   - a limiter in an array;
   - one mounted via a router or a prefix path (for example `app.use('/api/setup', …)`);
   - one applied globally with a path check.

   Say also what it would **over-count**: a non-limiter `app.use` on that path.
3. **Does any existing cell now pass for a WEAKER reason?** Early-return discipline: *an early return disarms tests
   outside the diff.* Removing a middleware changes every caller's path.
   - Enumerate every NEGATIVE-asserting cell whose route runs through the changed code — `rd464*` (T4/T5; `rd464-ai-readiness-service` pins `AI_DEPLOYMENT_TEST_LIMIT`), `rd545*` (A1–A4), `rd395*`, and `rd486` (e).
   - For each one, show it still fails for the RIGHT reason under the matching mutation, not merely that it is green.
   - **Watch in particular for a 429 that now arrives from a different limiter or message** (for example `generalLimiter`), which would keep a cell green while the property moved.
4. **The removed limiter's PURPOSE** was a cap on billed one-token probes per click, AI on. Confirm the survivor caps
   the same route at the same numbers, with the same message and headers, and that a status read still answers 200 after the cap (rd486 T5).
5. **`_rlOpts` shared store.** Both limiters used `_rlOpts`, which injects `_rateLimitStore` when one is configured. Check
   the surviving limiter's key does not collide with another limiter on the same store.
   **READ ONLY is acceptable here — label it.**

**Builder's red-proofs — RE-RUN THEM YOURSELF.** A kill you did not reproduce is the builder's.
- **M1** — a second limiter mounted → R8 red.
- **M2** — the only limiter removed → R8 red, plus rd545 A1–A4 red.
- **M3** — `fetchOptions` removed from the adapter → R7 and R7b red.
- Evidence: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76d/rd585-rd541-PROOFS.txt` and
  `rd585-rd541-proofs.sh`. **Also add a mutant of your own:** restore `skip: async () => !(await aiGate.isEnabled())` on
  the SURVIVOR. rd545 must go red, and say whether R8 does. If R8 stays green, that is expected, because R8 counts mounts
  and not skips. Name the cell that DOES carry the no-skip property.

## 4. TARGET A / RD-585 — the R7 cell must check MORE than before (through-code)
Claimed:
- ai-test never sends a top-level `code`. The adapter's healthcheck puts it in `details`, and the route passes `details` through.
- R7 now asserts `details.code == AI_ENDPOINT_REDIRECT_REFUSED` **AND** that `details.error` starts with *"The AI endpoint redirected; redirects are refused"*.
- Every containment term is kept: sink 0 connections / 0 requests, redirector reached.
- Evidence: `session-tools/s76d/rd585-r7-response.json`.

**Confirm:**
- **Strictly more is asserted.** Compare the old and new `toEqual` field by field: no term was removed or loosened.
- **The top-level `code` was really never present on any ai-test path.** If some path does emit it, the old assertion was right for that path.
- **The cell fails for the right reason under M-R7-a and M-R7-b.**
- **C-128 records this.**

## 5. TARGET A — counts and the full verify
- Builder's full verify at `b966634`: **3826 pass / 1 fail / 1 skip of 3828, 217 suites.**
  - The 1 fail is rd423 R1, the timer defect RD-604. Verified at commission: the rd423 file is **byte-identical** at `aae041a` and `b966634` (blob `dddff11`).
  - The skip is R10i, RD-583 by ruling.
- **Reproduce it:** `npm run verify -- --maxWorkers=2` (RD-561), through the lock. Account for every failure. **A second failure, or a different one, is a finding.**
- 🔴 **Measured at commission, not claimed by anyone:** `scripts/verify-expected-counts.json` at `b966634` says
  **tests 3797 / suites 216**, while the run above counted **3828 / 217** (+31 tests, +1 suite: the rd516 suite).
  - The builder's log shows `--update-counts` ran in its worktree, but the range touches only the two files, so **the update was never committed.**
  - `verify-suite`'s own `_why` says an uncommitted count protects nobody.
  - **Report whether this blocks the RD-516 merge or belongs in the post-forward-merge GREEN verify of C-126 step 3.**

## 6. TARGET B / RD-604 — a timer fix that must not weaken rd423 (through-code)
Claimed:
- `beforeAll`'s single `sleep(max(0, WAIT_PAST_MS − elapsed))` becomes a LOOP until `Date.now() − t0 >= WAIT_PAST_MS`.
- This fixes a 1 ms Node timer shortfall (*Expected >= 38000, Received 37999*). Measured: `setTimeout(13)` returned at 12 ms in 2 of 400 runs, `session-tools/s76d/timer-early-probe.js`.
- **Builder red-proof:** with every sleep shortened by 50 ms, the original fails R1 (37952 < 38000) and the fixed version passes 3/3. Unshimmed, it passes 3/3.
- Evidence: `session-tools/s76d/rd604-PROOFS.txt`, `rd604-proofs.sh`, `rd604-shim-copies/`.

**Confirm:**
1. **The real property is still asserted, unweakened.**
   - The process is alive: `exitCode` null and `signal` null.
   - `/api/health` answers **200** AFTER the window.
   - R1's precondition `waitedMs >= WAIT_PAST_MS` is kept as the guard.
   - C1 and R2 are unchanged.
2. **The loop cannot spin forever and has a bound.**
   - There is no explicit iteration cap.
   - Each pass sleeps at least 1 ms.
   - It ends on the wall clock, and the outer bound is `jest.setTimeout(180000 + WAIT_PAST_MS + 60000)`.

   Judge two things:
   - Is the jest timeout an honest bound?
   - Does a `Date.now()` step BACKWARDS (a clock adjustment) turn this into a long stall that reports as a timeout rather than a red?
3. **The shim is a fair model of the defect.** Re-run the red-proof yourself.
4. The branch touches exactly the one file, and `backend/services/authEnforcement.js` is untouched. **Both are enforced at launch.**

## 7. Floor discipline — THE FOUR CLAUSES (current wording; supersedes the RD-574 round-2 brief's §8)
1. **Every jest run goes through `session-tools/nexusai-lock.sh`.**
2. **Hold the lock ONCE per multi-run measurement.**
3. **Record the foreign `backend/server.js` count beside every result.** Count it this way:
   - **`basename(argv[0]) == node` AND `backend/server.js` appears ANYWHERE in the remaining argv** — not only as the first argument, because the preload form is `node -r <helper> …`;
   - tell yours from foreign by **ANCESTRY** (the ppid chain to your own jest or lock holder);
   - **NEVER** by `EADDRINUSE`, **never** by a grep of whole command lines (that over-reports, RD-591 c.37901), and **never** by raw `comm` (blind on macOS, RD-574 r2 R2-1).
4. **A zero is reportable only beside a control that fired in the same window.** Spawn one server the way the harness
   does, require the count to RISE, then reap it.

**Reap every server you start.** An orphan of yours is the next run's foreign seat.

## 8. Drivable surface — LOCAL RUN, **NOT THE DEMO** (RD-76). No demo pass happened for either target, and none must be recorded.

## 9. HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, no external comms.
- No real Azure, credential, vault, tenant or key.
- **Findings-only: do not commit, do not move any branch, do not write inside the NexusAI project.**

## 10. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd516-fixround-rd604-batch/report.md`

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-516 fix round @ b966634 + RD-604 (batched, tier 1/2)`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the QA project has none.

Verdict format:
- **A: GO / NO-GO**, and **B: GO / NO-GO**, stated separately.
- Then one paragraph on what the pair means for RD-516's merge, against C-126's four steps.
- **Rule 2: what you did NOT test is first-class output.** Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.
- Report the head of each target as three timestamped readings (start / mid / end), each with its branch name.

PROVENANCE:
- A head b9666342f50646fbe44aefcdeeaa732dea10dccb at refs/heads/rd-516-ai-test-ssrf-s73 | `git ls-remote origin rd-516-ai-test-ssrf-s73` | read 2026-09-21
- main is aae041a0d01113144cadadba3a44f19025b08d85 | `git ls-remote origin main` | read 2026-09-21
- 059f0a8..b966634 is 2 commits: ae98c74 (RD-585), b966634 (RD-541) | `git rev-list --count 059f0a8..b966634` → 2; `git log --format='%H %P | %s'` | read 2026-09-21
- range touches exactly __tests__/rd516-ai-test-ssrf.test.js + backend/server.js; ae98c74 = test file only, b966634 = server.js only | `git diff --name-only 059f0a8 b966634` (and per commit) | read 2026-09-21
- 059f0a8 parents aaffbb91a993… + aae041a0d011… | `git log -1 --format='%H %P' 059f0a8` | read 2026-09-21
- forward merge: only backend/server.js is a true content merge (617722c + a5cf76b → a072398); every other file takes one side's blob; the preload helper is identical on both | `git rev-parse <c>:<f>` for c in 60c76d7 aaffbb9 aae041a 059f0a8, over the union of both sides' changed files | read 2026-09-21
- RD-541: aiDeploymentTestLimiter const + inline mount removed; aiTestLimiter (no skip) now reads AI_DEPLOYMENT_TEST_LIMIT; only a comment names the removed limiter | `git show b966634 -- backend/server.js`; `git grep -n -i aiDeploymentTestLimiter b966634 -- __tests__ backend` → 1 hit (comment, server.js:1249) | read 2026-09-21
- AI_DEPLOYMENT_TEST_LIMIT = { windowMs: 600000, max: 5 } | `git show b966634:backend/services/aiReadiness.js` :49 | read 2026-09-21
- _rlOpts injects _rateLimitStore when set and adds no skip | `git show b966634:backend/server.js` :1135-1138 | read 2026-09-21
- RD-585: R7 now asserts details.code + details.error prefix, and keeps sink/redirector terms | `git show ae98c74` | read 2026-09-21
- R8 is a source regex (app.use path + app.post `\w*[Ll]imiter`) | `git show b966634:__tests__/rd516-ai-test-ssrf.test.js` :1096-1125 | read 2026-09-21
- R10i is test.skip (RD-583) | same file :1164 | read 2026-09-21
- authEnforcement.js blob ca764a4 at aae041a, b966634 and the RD-604 candidate; 0 diff lines 059f0a8..b966634; adminGateRefuses defined there :634 | `git ls-tree`, `git diff … | wc -l`, `git grep -n adminGateRefuses b966634 -- backend` | read 2026-09-21
- rd423 file byte-identical aae041a vs b966634 (dddff11) | `git rev-parse <c>:__tests__/rd423-test-ai-does-not-crash-server.test.js` | read 2026-09-21
- builder full verify on b966634: Tests 1 failed, 1 skipped, 3826 passed, 3828 total; Suites 1 failed, 216 passed, 217 total; fail = rd423 | session-tools/s76d/rd516-full-verify-raw.log + rd585-rd541-PROOFS.txt | read 2026-09-21
- builder M1 → R8 red; M2 → R8 red and rd545 A1-A4 red; M3 → R7 + R7b red | session-tools/s76d/rd585-rd541-PROOFS.txt | read 2026-09-21
- counts file at b966634 = tests 3797 / suites 216 (not updated to 3828/217) | `git show b966634:scripts/verify-expected-counts.json` | read 2026-09-21
- RD-604 head 172abc8308eeb71d3ffa1a1626ef069559876b98 at refs/heads/rd-604-rd423-timer-s76d (parent aae041a, 1 file, loop until elapsed >= WAIT_PAST_MS) | `git ls-remote origin rd-604-rd423-timer-s76d` by Tuesday at pin time; `git diff aae041a 172abc8` | read 2026-09-21
- rd423 keeps R1 precondition `waitedMs >= WAIT_PAST_MS` and asserts exitCode/signal null + healthAfter 200; jest.setTimeout(180000 + WAIT_PAST_MS + 60000) | `git show aae041a:__tests__/rd423-…` :28-29, :75-81 | read 2026-09-21
- builder RD-604 red-proof: shimmed original R1 fails 37952 < 38000; shimmed fixed 3/3; unshimmed 3/3 | session-tools/s76d/rd604-PROOFS.txt | read 2026-09-21
- C-126 (hold; sequence gate → RD-604 first → forward-merge GREEN → GO) and C-127 recorded; C-106, C-74, C-62, C-128 exist | 1_Project_Definition/CLARIFICATIONS.md :1340, :1347, :1001, :709, :573, :1355 | read 2026-09-21
- batch-gates standing rule | TUESDAY/0_Brain/learnings/2026-09-18_minimise-gate-duplication-batch-them.md | read 2026-09-21
- prior round-2 report on disk | Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd516-aaffbb9-round2/report.md | read 2026-09-21
