# BLUF — SUCCESSOR SEAT Datasec/NexusAI-F takes LANE A from S76D (NexusAI-D, wrapped 2026-09-21 21:26 AEST). Three merges are PRE-AUTHORISED IN THIS BRIEF, in order and under conditions: (1) RD-604 to main NOW; (2) forward-merge the new main into RD-516 with counts regenerated AND committed; (3) RD-516 to main only if (2) is GREEN. Then the gate-1 findings (F-1 fix, F-2, F-5 correction, F-3/F-7 tickets), then lane A's queue from RD-524. Every build ends at READY FOR QA to Tuesday.

**This brief is addressed to the cockpit seat `Datasec/NexusAI-F` only.** It is not addressed to `Datasec/NexusAI`, `-D`, `-E` or any other suffix. The inbox `datasec-nexusai@agentmail.to` is SHARED with NexusAI-E, so a mail addressed to another seat is not yours, however familiar its conversation looks.

**Authority:**
- Kam, 2026-09-21 18:18:12 AEST, live board, verbatim (C-127): *"Until we have a stable version, feel free to redeploy, merge, or do anything else to get us to a point where everything is fully ready."* Tuesday's reading, recorded in C-127: merges to main are **Tuesday's GO on a QA-gated head**.
- **Tuesday gives that GO here, for RD-604 and (conditionally) RD-516 only**, on the gate-1 verdict: `[QA] A — RD-516 fix round @ b966634: GO` and `B — RD-604 @ 172abc8: GO` (report path in PROVENANCE).
- Kam, card `nexusai-rd516-merge-two-known-reds`, option (a) (C-126): *"Keep holding; fix the two small tickets first"*. Both are fixed, gated and GO. C-126's step order still binds and is the order below.
- C-32: Tuesday authorises commissioning and sequencing. The GO for the plan AS BRIEFED is given now (see PLAN CONFIRMATION).
- Kam to Tuesday, 2026-09-21 ~15:2x AEST, typed: **"keep working through it and email me the zip when it's ready to upload and resubmit."** This is the resubmission push (remediation of RD-549).

**Read first:** `HANDOVER-S76D.md` (whole; §6 is where you start). The gate-1 report (whole). CLARIFICATIONS C-28, C-32, C-49, C-54 (with its 2026-09-17 13:04:44Z addition), C-57 (and its 03:43:09Z amendment), C-67, C-68 (and its amendment), C-89, C-91, C-98, C-110, C-125, C-126, C-127, C-128, C-129. The lane partition: `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md`.

## 0 — ESTABLISH YOUR SEAT FROM THE PROCESS TABLE FIRST
Walk your own shell's parent chain to the `zsh -c` launcher process. Its command line ends `[cockpit] Datasec/NexusAI-F exited — pane stays for inspection`. Record that pid, your own `claude` pid and your tmux pane id, and put all three in the plan confirmation. **If the walk ends at any other label, that is the finding: do nothing else, and mail Tuesday.** Never decide which seat you are from which conversation in the inbox looks like yours. Use session tag **S77F** in branch names, files and mails.

**The other seats on the floor, by what each can measure about itself (read at 21:32-21:33 AEST):**
- **Lane B = `Datasec/NexusAI-E`, session S76E, tmux pane `%32`, pane shell pid `73275`, claude pid `73277`, started 19:38:41 AEST.** It owns `backend/customerDataFiles.js`, `backend/dataErasure.js`, `backend/dataExport.js` and its new test files. RD-525 is done (READY, in gate 2). RD-575 is E's: at 21:32 origin had `rd-575-purge-reaches-attachments-s76e` @ `4c0fe45`, still off `aae041a` and NOT yet on RD-525's head; E is re-stacking it. **Never touch either lane-B branch.**
- **`QA/NexusAI-gate2`, tmux pane `%33`, launcher pid `65689`, started 21:27:02 AEST,** launched `--without-rd575`: it gates RD-495 @ `179bf60` and RD-525 @ `792fda0`. It uses the same lock as you.
- **NexusAI-D (S76D) is gone.** Its launcher `13411` and claude `13413` are no longer in the process table. Nothing of S76D's is running.
- **Lane C = not started; no seat exists.** It will own `azure-marketplace/**`, the packaging scripts, `bicep/` and `DEPLOYMENT_GUIDE.md` once RD-516 has landed.
- **Lane B asks, it does not edit, `backend/server.js` and `backend/jsonStorage.js`.** Tuesday routes such requests to you as lane-A work. The RD-525 lane-A registration is already done by S76D at `fef773b` (on RD-525's branch).

## STATE AT DRAFTING — re-read every sha yourself before acting
| ref | sha (origin, 21:32 AEST) | what it is |
|---|---|---|
| main | `aae041a` | RD-518 on it; demo runs it (rev `nexusaidev-app--0000099`); counts 3797/216 |
| rd-604-rd423-timer-s76d | `172abc8` | ONE commit off main; one file (`__tests__/rd423-test-ai-does-not-crash-server.test.js`); gate-1 B: GO |
| rd-516-ai-test-ssrf-s73 | `b966634` | main is its ancestor; seven files vs main; counts still 3797/216 (F-6); gate-1 A: GO |
| rd-495-csp-violations-hard-gate-s71 | `179bf60` | READY; in gate 2; counts 3809/217 |
| rd-525-export-erasure-coverage-s76e | `792fda0` | READY (E) + lane-A commit `fef773b` (S76D); in gate 2; counts 3817/217 |
| s76d-path-map | `710e875` | docs only; do NOT merge until the release gate |
| s76d-history-docs | `04b529d` | S76D's HISTORY entry (C-91 union later) |
| rd-404-441-sentinel-banner-s59 | `feac318` | S59's WIP for RD-404/441; conflicts with main (C-54 13:04Z) |

- **Never touch the `2_Project_Files` working checkout** (C-28, C-67). It is stale by design. Don't write, pull, check out, reset, stash or read it for product truth. **Work in fresh worktrees at ABSOLUTE paths outside the clone**, cut from `origin/<ref>`, under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/` with an `-s77f` suffix (e.g. `.../worktrees/merge-rd604-s77f`, `.../worktrees/rd-516-fwd-s77f`, `.../worktrees/merge-rd516-s77f`). Do not reuse S76D's worktrees. Do not prune `worktrees/mkt-rc-selfcontained-s62/node_modules` (other worktrees chain to it).
- **`d0b9cde` in `worktrees/s74-merge-main` is superseded. DO NOT DELETE it, do not push it, do not build on it.**
- Every file:line you quote names its head, e.g. "server.js:16539 at b966634".

## 1 — MERGE RD-604 TO MAIN, NOW (GO GIVEN IN THIS BRIEF)
**Basis:** gate-1 verdict **B — RD-604 @ `172abc8308eeb71d3ffa1a1626ef069559876b98`: GO** (one-file, test-only; red-proofed by QA; 3 separate unshimmed runs 3/3).
**Conditions, all of them, or STOP and mail Tuesday:**
1. Immediately before merging: `git ls-remote origin refs/heads/main refs/heads/rd-604-rd423-timer-s76d` reads **main = `aae041a0d01113144cadadba3a44f19025b08d85`** and **rd-604 = `172abc8308eeb71d3ffa1a1626ef069559876b98`**. Either moved: STOP, mail.
2. In a fresh worktree off `origin/main`: `git merge --no-ff origin/rd-604-rd423-timer-s76d`. Forward merge, never rebase, never squash. `git diff --name-only aae041a HEAD` must list only the rd423 test file (plus the counts file if regeneration changes it). Anything else: STOP, mail.
3. **Counts (C-57, C-68 amendment, C-89):** regenerate on the merged tree with `npm run verify -- --maxWorkers=2 --update-counts` through the lock. RD-604 adds no test, so expect **3797 tests / 216 suites unchanged**. Say what you MEASURED. If the numbers changed, re-stage the file and commit it into the merge; if only the `_updated` stamp changed, do not commit a stamp-only rewrite, and say so. Run the C-57 id-superset control ("merged N ⊇ A M ∪ B K; missing 0").
4. **Full verify GREEN through the lock**, the four floor clauses evidenced. Name rd423 C1/R1/R2 individually in the result (C-68).
5. **C-89 before pushing:** `git diff --quiet HEAD` holds, and `git show HEAD:scripts/verify-expected-counts.json` equals the measured numbers. Quote both.
6. Re-read main by `ls-remote` once more; still `aae041a` → `git push origin HEAD:main`. No force, no `--no-verify`. Then `ls-remote` and quote the new main sha.
7. **Deploy check.** Demo auto-deploy is OFF: `.github/workflows/deploy-demo.yml` gates its jobs on `vars.CI_DEPLOY_ENABLED == 'true'` (lines 53 and 91 at `aae041a`), and C-126 records that every push to main skipped the deploy. Read the Actions run for your merge commit and **quote the deploy job as skipped**. If a deploy job RAN, that is a demo deploy without a GO: mail Tuesday at once.
8. Mail `[Datasec/NexusAI-F -> Tuesday] MERGED: RD-604 to main @ <sha>`, with conditions 1-7 quoted.

## 2 — C-126 STEP 3: FORWARD-MERGE THE NEW MAIN INTO RD-516
Branch `rd-516-ai-test-ssrf-s73` @ `b9666342f50646fbe44aefcdeeaa732dea10dccb`.
1. `ls-remote`: rd-516 still `b966634`, main = the sha you pushed in step 1. Either differs: STOP, mail.
2. Fresh worktree off `origin/rd-516-ai-test-ssrf-s73`. `git merge --no-ff --no-commit origin/main`.
3. **Measured prediction (gate-1 §9 and read at drafting):** the only incoming file is `__tests__/rd423-test-ai-does-not-crash-server.test.js` (blob `dddff11` on RD-516 and at `aae041a`; `de12f88` at `172abc8`). **If the merge brings ANY other file, or any conflict, STOP and mail Tuesday. Do not go on to step 3.**
4. **Gate finding F-6, quoted:** *"`scripts/verify-expected-counts.json` at `b966634` is blob `eb071ad` = main's (`tests 3797, suites 216`) … Both my run 2 and the builder's measured **3828 / 217**"*, and *"The forward-merge commit of step 3 is where the file must be regenerated **and committed**."* So: run `--update-counts` on the merged tree, **`git add` the counts file again after it is rewritten** (the C-89 failure was exactly a rewrite that was never re-staged), then commit the merge. Expect **3828 / 217**. C-57 id-superset control against both parents. Commit message: "counts file regenerated on the merged tree; id superset control: missing 0".
5. **Full verify GREEN** on the committed merge, through the lock. A GREEN without the committed counts is impossible by construction; if you see one, the counts were bypassed (`MIN_TESTS` / `MIN_SUITES`), and that is a finding. Name rd423 C1/R1/R2 and the rd516 suite (expect 30 passed / 1 pending) individually (C-68).
6. C-89 checks quoted. Push to `origin rd-516-ai-test-ssrf-s73` (a fast-forward of the branch; no force). `ls-remote` and quote.
7. Mail `[Datasec/NexusAI-F -> Tuesday] STEP 3 DONE: RD-516 forward-merged @ <sha>, verify <N/M>, counts <t/s>`.

## 3 — MERGE RD-516 TO MAIN (GO GIVEN IN THIS BRIEF, CONDITIONAL)
**Basis:** gate-1 verdict **A — RD-516 fix round @ `b966634`: GO**. The step-2 merge changes no code RD-516's cells read: rd423 is the only incoming file.
**Only if ALL hold, otherwise STOP and mail:** step 2 GREEN; the committed counts equal the run; `ls-remote` shows main = your step-1 sha and rd-516 = your step-2 sha.
1. Fresh worktree off `origin/main`. `git merge --no-ff origin/rd-516-ai-test-ssrf-s73`.
2. Because main is an ancestor of your step-2 head, the merged tree must equal it: quote `git rev-parse HEAD^{tree}` and `<step-2 sha>^{tree}`; they must match. If not, STOP.
3. Full verify GREEN through the lock (expect 3828/217); C-89 checks; re-read main; `git push origin HEAD:main`; `ls-remote`; deploy job skipped (as step 1.7).
4. Mail `[Datasec/NexusAI-F -> Tuesday] MERGED: RD-516 to main @ <sha>`, naming the files RD-516 brought (DEPLOYMENT_GUIDE.md, HISTORY.md, the rd516 test, server.js, aiEndpointPolicy.js, aiTestCredentials.js, docs/rd516/RD-516-gate-brief.md, plus the counts file).
5. **From this point lane A no longer owns `DEPLOYMENT_GUIDE.md`** (partition: lane A until RD-516 lands, then lane C). With no lane-C seat, any later need to edit it goes to Tuesday first.

## 4 — RD-495 AND RD-525: NOT YOURS TO MERGE YET
Both are in **QA gate 2** (pane `%33`, running). **Their merges wait for Tuesday's separate GO mail naming each. That GO is NOT given in this brief.** When it comes, expect it to require a forward merge of the then-current main and named affected-cell re-runs (C-68): after steps 1-3, main will carry RD-516's `server.js`, and RD-495 (`d0d252c`) and RD-525's lane-A commit (`fef773b`) also touch `server.js`, so a gate-2 GO holds at the gated sha only. RD-575 is E's and is not in gate 2.

## 5 — GATE-1 FINDINGS LANE A OWNS (server.js is yours)
Quoted from the report; line numbers are at `b966634`.
- **F-1 · Major · pre-existing:** *"In Redis mode (`docker-compose.yml` sets `REDIS_HOST`), every limiter shares ONE RedisStore and ONE key per address. The ai-test cap is **1 per 10 min, not 5**, and any `/api` traffic from the address counts against it."* Mechanism: *"`_rlOpts` (`server.js:1135-1138`) injects the one `_rateLimitStore` into every limiter"*; `ERR_ERL_STORE_REUSE` is logged at boot.
  - **FILE A TICKET.** First search the board by the symbols `_rlOpts`, `RedisStore` and `ERR_ERL_STORE_REUSE` (text search), and say in the mail exactly what you searched and what came back. Then `git log --all -S _rlOpts` for prior work (the report attributes `_rlOpts` to PT-022).
  - **Fix shape (the report's):** *"one `RedisStore` per limiter, each with a unique `prefix` (the library's own remedy)."* Regression cell (the report's): *"in Redis mode (a real Redis or a faithful fake), 5 ai-tests from one address pass and the 6th is 429; and boot output carries no `ERR_ERL_STORE_REUSE`."* A real Redis needs the **docker** lock as well.
  - **Build it as a lane-A item after the merges** (branch off the main that step 3 produced, `rd-<ticket>-redis-store-s77f`), red-proof, full verify, **READY FOR QA** with PRIOR WORK.
- **F-2 · Minor:** *"'the route's ONLY limiter' (`server.js:16539`) is false at runtime. POST `/api/setup/ai-test` runs **three** rate limiters."* Reword to "the route's only **ai-test-specific** limiter". **Fold it into the F-1 change.**
- **F-5 · Minor, doc/ruling:** C-128's claim *"No path of ai-test has ever set a top-level `code`"* is FALSE: *"`server.js:16589` `res.status(400).json({ success:false, ...target.refused })` sends `code: AI_TEST_KEY_REQUIRED`; `:16628` sends `code: AI_ENDPOINT_NOT_ALLOWED`."*
  - **Correct C-128 by ADDENDUM** in CLARIFICATIONS (supersede, never delete; the file's own rule), using the report's wording: *"the redirect refusal (and any healthcheck outcome) is named in `details`; the 400 refusal paths (AI_TEST_KEY_REQUIRED, AI_ENDPOINT_NOT_ALLOWED) name it at the top level."* Its "Rule for later cells" line is superseded with it.
  - Fix the `ae98c74`-era R7 comment in `__tests__/rd516-ai-test-ssrf.test.js` in **the next lane-A change that touches that test file**. Not a separate branch.
- **F-3 · Minor** (*"R8 misses four shapes of a second limiter … and false-reds on two shapes that still have one limiter"*) and **F-7 · Minor · pre-existing** (*"`handover-gate-table`'s SHA cell PASSES outside a git checkout while checking nothing"*): **TICKET each**, board searched first (say what you searched). Do not build them now.
- F-4 (a proof artefact) and B-O1 (optional hardening) need no action. F-6 is step 2.

## 6 — THEN LANE A CONTINUES (HANDOVER-S76D §6 and the partition)
Order: **RD-524 + RD-404 + RD-441** → **RD-531 + RD-497** → RD-510 → RD-438 → RD-487 → RD-457 → RD-492 → RD-519 → RD-475 → RD-520 (measure first). One branch per item off the current main, `-s77f` suffix.
- **RD-524 + RD-404 + RD-441 close together (C-54 13:04Z).** HANDOVER-S76D §6: *"Starting measurement is on RD-524 comment 37932: merge-tree main vs `feac318` conflicts in server.js and BACKLOG.md, so RE-IMPLEMENT on main (C-54 13:04Z), keeping S59's pieces that still apply. Read S59's six WIP commits (`git log ca8d364..feac318`) before writing anything."* PRIOR WORK lists what was kept, improved and dropped. S59's `b587646` spreads `CUSTOMER_DATA_FILES` into `jsonStorage.js`; RD-525 added stores to that list, so if you keep that piece, measure what the sentinel now covers. RD-524's recovery text sits in `DEPLOYMENT_GUIDE.md`: ask Tuesday before editing it (section 3.5).
- **RD-531 + RD-497 ride together (C-54).** C-129 already moved ONE route (`GET /api/admin/csp-violations`), and that move lives on RD-495's branch, not on main. Do not redo it. **The other 15 RD-497 routes are per-route decisions, each "from its prior work".** Start after RD-495 lands, or expect a forward merge.
- **Every item:** the PRIOR-WORK check (C-49) → cells asserting the property after the fix (C-98) → red-proof → full verify → **READY FOR QA**. Keep going to the next item after each READY; do not wait for its gate.

## PRIOR-WORK CHECK (C-49) — before building each item
`git log --all -S` on the symbols you change; `git log --all --grep` for the ticket id; the branch list; `session-tools/s76d/lane-RD-*.txt` (S76D's board dump, 19:26 AEST); HANDOVER-S59, S65, S70, S76D; the tickets' comments; `5_Project_History/`. Write down what existed, when, which round introduced it and why, or "no source found". Keep what works (C-50).

## FLOOR — C-110's four clauses, with C-125's counter as corrected by RD-606
1. **Every** jest invocation goes through `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh jest <tag> …` with `--maxWorkers=2`, including probes and single suites. Docker (a real Redis for F-1) also takes `nexusai-lock.sh docker`.
2. **Hold the lock ONCE across a multi-run measurement** (a red-proof pair, the regenerate-then-verify pair). Never per run.
3. **Record the foreign-server count beside every result** with `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76e/floorcheck.py` (basename of argv[0] is `node` AND the entry point ANYWHERE in argv). **RD-606: "ours" means the server's ancestor chain contains YOUR OWN claude pid.** Shared ancestors (tmux, launchd) prove nothing. Run `--selftest`, and use `--expect-foreign <pid>` as the negative control. Do NOT use `session-tools/s76d/floorcheck.py`; S76D's own handover says its ancestry was wrong.
4. **A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED IN THE SAME WINDOW.** Spawn a control the harness's way, require the count to RISE, reap it.

The lock is shared with NexusAI-E and the gate-2 QA seat. Reap everything you start. Before each red-proof, write down which cells you expect to redden and how many.

## HELD — decisions this seat is NOT making
- **No merge other than steps 1-3 above.** RD-495, RD-525 and every later item wait for a Tuesday GO naming them.
- No production. No Partner Center. **No push to `nexusaireleaseacr`** (Kam's). No demo redeploy (needs a separate Tuesday GO). No real Azure writes, credentials, tenants, keys or registries. No money, no external comms.
- No force push. No `--no-verify`. Never rebase a pushed branch (a rebased branch gets a new name).
- Never touch the stale `2_Project_Files` working checkout (C-28, C-67).
- No edit in lane B's three files or on lane B's branches. No edit to `PRIVACY.md` or `TERMS_OF_SERVICE.md` (C-65). No hand edit to `scripts/verify-expected-counts.json` (C-57).
- **Vault:** stage Datasec paths one by one, never `git add -A`. S76D appended to `daily/2026-09-21.md` and did NOT commit it (the vault is 7 ahead / 527 behind). It needs a supervised reconcile: **do NOT commit it; leave it.**
- Kam-only and untouched: the 2.2.0 image push, Partner Center, RD-594 scope, RD-362 rotation, the C-124 Key Vault success-path proof.

RULED BY KAM, NOT YET IN AN ARTEFACT
- None. `decision_queue.sh list ruled --undelivered nexusai-` returns 0 (control: 66 ruled `nexusai-` cards listed). C-126 and C-127 are both recorded in CLARIFICATIONS.

RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- **C-129:** one route moved (`GET /api/admin/csp-violations` below `requireAuth`); the other 15 RD-497 routes are per-route decisions in lane A's RD-497 work.
- **The lane partition** as measured at `aae041a` (lane A = `server.js`, `jsonStorage.js`, `bootPreflight.js`, `static/**`, `.dockerignore`, `Dockerfile`; `DEPLOYMENT_GUIDE.md` until RD-516 lands).
- **Lane B asks, it does not edit, `server.js` and `jsonStorage.js`;** Tuesday routes those requests to lane A.
- **The RD-525 lane-A registration is done** at `fef773b` (an erasure also drops the in-memory audit buffer). Nothing more is owed on it unless Tuesday routes a new ask.
- C-98, C-110 + C-125 (+ RD-606), C-67, C-49, C-57/C-68/C-89 as above. C-91: your HISTORY entry goes on your own history branch (`s77f-history-docs`), never to main directly.

## READY FOR QA — one per item, to `tuesday-agent@agentmail.to`
Subject: `[Datasec/NexusAI-F -> Tuesday] READY FOR QA: <ticket> <one line>`. Body sections, in order:
1. **Branch and head sha**, pushed and read back with `git ls-remote origin`.
2. **PRIOR WORK** (C-49), or "nothing replaced".
3. **What changed**: the files, each inside lane A.
4. **RED-PROOF**: the cells you expected to redden, written down first. Fix reverted → those cells red (quoted). Fix restored → green. One lock hold.
5. **Full verify** through the lock, the four floor clauses evidenced. Honest N/M, read not inferred. Counts regenerated on your branch if they changed.
6. **Verdict line**, and **what you did NOT test**.

MERGED mails (steps 1 and 3) carry: both `ls-remote` readings, the merge sha, the C-57 control line, the C-89 pair, the full-verify N/M with the named cells, and the deploy-job-skipped reading.

## PLAN CONFIRMATION, then START
Send first: `[Datasec/NexusAI-F -> Tuesday] QUESTION: plan confirmation`. It must carry:
- your process-table reading (launcher pid, claude pid, pane, label);
- any launcher preflight warnings, VERBATIM;
- main, rd-604 and rd-516 as you read them by `ls-remote`;
- your worktree paths.

**Then start straight away, without waiting.** Merges 1-3 are pre-authorised under their conditions. Only a deviation waits for an answer: a moved head, an unexpected file or conflict, new scope, a file outside lane A, or anything in HELD.

## WRAP
Rotate yourself at 80-90% context. Write `HANDOVER-S77F.md` in the NexusAI project root (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/`), naming each item, branch, head and next step. Push a wip snapshot of each build branch before every lock wait. At wrap:
- mail `tuesday-agent@agentmail.to`, subject `[Datasec/NexusAI-F -> Tuesday] Session wrap 2026-09-21` (or the date you wrap);
- a HISTORY entry on `s77f-history-docs` (C-91);
- confirm `.env` is not staged;
- in the vault, stage Datasec paths only, one by one, and leave S76D's uncommitted daily-note append alone.

PROVENANCE:
- main = aae041a0d01113144cadadba3a44f19025b08d85; rd-604 = 172abc8308eeb71d3ffa1a1626ef069559876b98; rd-516 = b9666342f50646fbe44aefcdeeaa732dea10dccb; rd-495 = 179bf603cf563013ac9f89dbc7b1e216e8a9d385; rd-525 = 792fda0b3dc1884b32f3e04877f18959fbaaae77; rd-575 = 4c0fe458342add5110800753b427aee4074da465; s76d-path-map = 710e875; s76d-history-docs = 04b529d; rd-404-441-sentinel-banner-s59 = feac318 | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin <each ref>` at 21:32:04 AEST | read 2026-09-21
- gate-1 verdicts A GO at b966634 and B GO at 172abc8; F-1 to F-7 and B-O1 texts; F-6 prediction 3828/217; step-3 prediction (rd423 the only incoming file) | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd516-fixround-rd604-batch/report.md (§0, §8, §9) | read 2026-09-21
- rd-604 is one commit, one file off main; main is ancestor of rd-604 and of rd-516; merge-base(rd-516, rd-604) = aae041a; the only file rd-604 brings = the rd423 test | `git log --oneline aae041a..172abc8`, `git diff --name-only aae041a 172abc8`, `git merge-base --is-ancestor`, `git merge-base b966634 172abc8` | read 2026-09-21
- rd423 blob dddff11 at b966634 and aae041a, de12f88 at 172abc8 | `git rev-parse <sha>:__tests__/rd423-test-ai-does-not-crash-server.test.js` | read 2026-09-21
- rd-516's seven files vs main | `git diff --name-only aae041a b966634` | read 2026-09-21
- counts 3797/216 at aae041a, b966634, 172abc8; 3817/217 at 792fda0; 3809/217 at 179bf60 | `git show <sha>:scripts/verify-expected-counts.json` | read 2026-09-21
- rd-575 4c0fe45 is off aae041a, not on 792fda0 | `git merge-base --is-ancestor 792fda0 4c0fe45` rc 1; `git merge-base 4c0fe45 792fda0` = aae041a | read 2026-09-21
- server.js:1135 `_rlOpts`, :16539 "the route's ONLY limiter", :16589 `...target.refused`, :16628 `...callerBody`, all at b966634 | `git show b966634:backend/server.js` lines 1133-1139, 16537-16541, 16587-16590, 16626-16629; `git grep -n _rlOpts b966634 -- backend/server.js` | read 2026-09-21
- deploy jobs gated on vars.CI_DEPLOY_ENABLED == 'true' (lines 53, 91) | `git grep -n CI_DEPLOY_ENABLED aae041a -- .github` | read 2026-09-21
- every push to main skipped the deploy; C-126 sequence; the "[[C-128]]" citation correction | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-126 | read 2026-09-21
- Kam's C-127 words and Tuesday's reading (merges are Tuesday's GO on a QA-gated head) | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-127 | read 2026-09-21
- C-128 text "No path of ai-test has ever set a top-level `code`" and its rule for later cells | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-128 | read 2026-09-21
- C-129 one route, the other 15 untouched until RD-497 decides each | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-129 | read 2026-09-21
- supersede-never-delete rule for entries | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, header "Rules for entries" | read 2026-09-21
- counts regeneration + id-superset control; regenerate regardless of conflict; C-89 re-stage lesson | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-57 (+03:43:09Z), C-68 (+amendment), C-89 | read 2026-09-21
- stale checkout never touched or read; absolute worktree paths; heads named | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-28 and C-67 | read 2026-09-21
- RD-524/404/441 close together; feac318 merge-tree conflicts in server.js and BACKLOG.md; re-implement on main | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-54 ADDED 2026-09-17 13:04:44Z | read 2026-09-21
- PRIOR WORK, keep what works, cells assert the property, floor four clauses, counter form, Tuesday as coordinator, HISTORY union | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-49, C-50, C-98, C-110, C-125, C-32, C-91 | read 2026-09-21
- S76D state table, merge order, d0b9cde superseded, RD-524 comment 37932 starting measurement, lane-A order, RD-606 floorcheck switch, uncommitted vault append, Kam-only list | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S76D.md §0, §4, §6 (file mtime 21:26:51 AEST) | read 2026-09-21
- lane files, lane-A order RD-495 → … → RD-520, DEPLOYMENT_GUIDE ownership passes to lane C after RD-516, lane B asks-not-edits jsonStorage.js | `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md` | read 2026-09-21
- ticket states: RD-524 To Do/High, RD-404 In Progress/Medium, RD-441 In Progress/High, RD-531 To Do/High, RD-497 To Do/Medium (16 routes), RD-510 To Do/High, RD-438, RD-487, RD-457, RD-492, RD-519, RD-475, RD-520 To Do/Medium | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76d/lane-RD-*.txt (S76D board dump 19:26 AEST, not re-read from Jira by Tuesday) | read 2026-09-21
- NexusAI-E = pane %32, shell 73275, claude 73277, started 19:38:41; gate-2 QA = pane %33, launcher 65689, 21:27:02, `--without-rd575`; D's 13411/13413 absent | `ps -axo pid,ppid,lstart,command` filtered on the cockpit labels, `ps -p 13411,13413`, `tmux list-panes -a` at 21:32-21:33 AEST | read 2026-09-21
- gate 2 covers RD-495 179bf60 and RD-525 792fda0; "a GO here is a GO at the gated SHA only (C-68)" | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-gate2-rd495-rd525-rd575.md - my project, not yours | read 2026-09-21
- s76e floorcheck: "ours" = chain contains THIS seat's claude; --selftest; --expect-foreign PID | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76e/floorcheck.py header lines 6-14 | read 2026-09-21
- lock usage, jest and docker kinds, --maxWorkers=2 | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh header | read 2026-09-21
- `--update-counts` flag and MIN_TESTS/MIN_SUITES bypass | `git grep -n update-counts aae041a -- scripts/verify-suite.sh` | read 2026-09-21
- vault daily/2026-09-21.md modified, uncommitted; 7 ahead / 527 behind | `git -C "/Volumes/KK_T9_External_HDD/Notes (MASTER)" status --short -- daily/2026-09-21.md` and `rev-list --left-right --count @{u}...HEAD` | read 2026-09-21
- zero undelivered NexusAI rulings (control: 66 ruled nexusai- cards) | `bash /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered nexusai-` | read 2026-09-21
Self-check note: read whole by Tuesday at 2026-09-21 21:37; merges 1-3 carry stop conditions on moved heads, extra files or conflicts; RD-495/RD-525 merges explicitly NOT given; lane boundaries match the E brief and the 09:3xZ partition answer; C-126/C-127 delivered, no Kam ruling open.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 21:37
