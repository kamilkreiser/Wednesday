# BLUF — SUCCESSOR SEAT Datasec/NexusAI-H takes LANE A from S77F (NexusAI-F, wrapped 2026-09-22 06:43 AEST, wrap mail 20:43Z, pane %34 CLOSED). **No merge is authorised in this brief.** Three branches sit at READY and are NOT merged: RD-575 @ `6a32426` and RD-524 round 2 @ `dc8635c` (both in QA gate 4, running now) and RD-615 @ `b7fc78f` (gate 5, batched with your RD-616). You merge nothing without a SEPARATE Tuesday GO mail that names the branch AND its head sha. Your work is lane A's build queue, starting at RD-616 (+RD-617). Every build ends at READY FOR QA to Tuesday.

**This brief is addressed to the cockpit seat `Datasec/NexusAI-H` only.** It is not addressed to `Datasec/NexusAI`, `-D`, `-E`, `-F`, `-G` or any other suffix. The inbox `datasec-nexusai@agentmail.to` is SHARED with NexusAI-G (lane C, live). A mail addressed to `Datasec/NexusAI-F` or `-G` is not yours, however familiar its conversation looks. F's open conversations are closed with F; anything still owed to lane A reaches you as a new mail addressed to `-H`.

**Authority:**
- Kam, 2026-09-21 18:18:12 AEST, live board, verbatim (C-127): *"Until we have a stable version, feel free to redeploy, merge, or do anything else to get us to a point where everything is fully ready."* Tuesday's reading, recorded in C-127: merges to main are **Tuesday's GO on a QA-gated head**. It does NOT cover production, Partner Center or Marketplace upload, money, or external comms.
- Kam to Tuesday, 2026-09-21 ~15:2x AEST, typed: **"keep working through it and email me the zip when it's ready to upload and resubmit."** This is the resubmission push; lane A's queue feeds it.
- C-32: Tuesday authorises commissioning and sequencing. The GO for the plan AS BRIEFED is given now (see PLAN CONFIRMATION). **No merge GO is given in this brief.**

**Read first:** `HANDOVER-S77F.md` (whole; 44 lines; §1 is where you start, §2 is the lessons). F's wrap mail body `session-tools/s77f/mail-20-wrap.txt`. `HANDOVER-S76D.md` §6 (lane A's items and their starting measurements). CLARIFICATIONS: C-28, C-32, C-49, C-50, C-54 (and its additions), C-57 (and its amendments), C-65, C-67, C-68 (and its amendment), C-89, C-91, C-98, C-105, C-110, C-111, C-112, C-125, C-127, C-128 (and its S77F addendum), C-129, C-130 (and both addenda), C-131, C-132, C-133. The lane partition: `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md`.

## 0 — ESTABLISH YOUR SEAT FROM THE PROCESS TABLE FIRST (C-111)
Walk your own shell's parent chain to the `zsh -c` launcher process. Its command line ends `[cockpit] Datasec/NexusAI-H exited — pane stays for inspection`. Record that pid, your own `claude` pid and your tmux pane id, and put all three in the plan confirmation. **If the walk ends at any other label, that is the finding: do nothing else, and mail Tuesday.** Never decide which seat you are from `4_Credentials/.launch_preflight_last.txt` (per-project, last-writer-wins, RD-587) or from which inbox conversation looks like yours. Use session tag **S79H** in branch names, worktree names, files and mails.

**The other seats on the floor, as Tuesday measured them (06:45 AEST 2026-09-22):**
- **Lane C = `Datasec/NexusAI-G`, session S78G, tmux pane `%36`, launcher pid `57417`, claude pid `57419`, started 03:44:19 AEST.** It is on RD-526 (worktree `worktrees/rd-526-s78g`) and at 06:45 it was QUEUED for the jest lock (ticket pid `89703`, tag `s78g-rd526`). Its branch `mkt-release-gate-s78g` is at `5b6a24f`. **G owns** `azure-marketplace/**`, `bicep/**`, `DEPLOYMENT_GUIDE.md`, the packaging scripts (`scripts/marketplace-package-build.sh`, `scripts/validate-marketplace-template.sh`, `scripts/deploy-dev.sh`, `scripts/provision-customer.sh`), the package tests (`__tests__/marketplace-*.test.js`, `__tests__/rd461-self-contained-and-template-toolkit.test.js`), the docs RD-526 names (`docs/MARKETPLACE_TEST_PROCEDURE.md`, `docs/REFERENCE_ARCHITECTURE.md`, `docs/runbooks/**`), and `docs/HOSTING_AND_COST_ANALYSIS.md` lines 16, 31 and 172 (Tuesday's ruling (A) of 06:22 AEST: G annotates them inline for RD-526's docs guard). **None of those is yours.** Never touch G's branches.
- **QA gate 4, tmux pane `%37`, launcher pid `95252`, started 05:46:57 AEST** (`B_HEAD=dc8635c…`). At 06:45 it HELD the jest lock (tag `qa-gate4-hold2`, pid `89297`, since 20:40:18Z). It gates A = RD-575 @ `6a32426` (tier 1, round 1) and B = RD-524 round 2 @ `dc8635c` (narrow re-gate, round 2 of 2 under C-62's cap).
- `%0` = tuesday (launcher `33220`), `%3` = fleet-monitor (`54400`), `%8` = an idle respawned shell (`69949`). NexusAI-F (S77F) is gone: pane `%34` was closed by Tuesday at 06:44, and nothing of S77F's is running. NexusAI-D and -E wrapped earlier.

## YOUR FILES (lane A)
The partition's lane-A row at `710e875` (measured at `aae041a`), plus C-132:
- `backend/server.js`, `backend/jsonStorage.js`, `backend/bootPreflight.js`, `static/**`, `Dockerfile`, `.dockerignore`;
- **`backend/customerDataFiles.js`, `backend/dataErasure.js`, `backend/dataExport.js`** (C-132: lane B's three files became lane A's on 2026-09-22; each edit must serve a ticket in your queue, be named under "What changed", and carry PRIOR WORK);
- the `__tests__` files for all of the above, and new test files and `__tests__/helpers/` files your items add;
- `scripts/verify-expected-counts.json`: every lane, never hand-edited, regenerated on the tree (C-57, C-68, C-89);
- `HISTORY.md`: your own history branch only (`s79h-history-docs`, C-91).

**Not yours:** everything in G's list above. **`README.md` is ask-first**: mail Tuesday before editing it. `DEPLOYMENT_GUIDE.md` is lane C's; if a lane-A item needs it (RD-524's recovery text is there), mail Tuesday and Tuesday routes it to G. `PRIVACY.md` and `TERMS_OF_SERVICE.md` are edited by nobody (C-65, C-105).

✅ **`backend/services/emailService.js` IS GRANTED to lane A for RD-616 / RD-617 only** (Tuesday's ruling in this brief, C-32; record it as a C-number). The fix site is `_maybeEncrypt`, `emailService.js:167-172` at `982a84f`, where the `encryptValue(plain)` call with no deps is at `:170`. No live seat owns the file (it is not in G's list). The grant covers the edits RD-616/RD-617 need, named under "What changed" with PRIOR WORK. It is not a standing claim on `backend/services/`. RD-413's option B (below) binds the fix.

## STATE AT DRAFTING — re-read every sha yourself before acting
| ref | sha (origin, 06:44:34 AEST) | what it is |
|---|---|---|
| main | `982a84f` | RD-604 (`bdca588`), RD-516 (`47be2b0`), RD-495+RD-498 (`f1319ac`), RD-525 (`982a84f`) all landed; counts **3860 / 219** |
| rd-575-purge-reaches-attachments-s76e | `6a32426` | READY, merge-only; main is its ancestor (0 behind / 5 ahead); counts 3868/220; **in gate 4** |
| rd-524-404-441-s77f | `dc8635c` | READY, round 2 of 2; main is its ancestor (0/5); counts 3902/221; **in gate 4** |
| rd-615-audit-flush-epoch-s77f | `b7fc78f` | READY; main is its ancestor (0/4); counts 3864/220; **gate 5, batched with RD-616** |
| s77f-history-docs | `44eb58a` | F's HISTORY entry (C-91 union later). Not yours to merge. |
| mkt-release-gate-s78g | `5b6a24f` | lane C's. Not yours. |

- **Demo** runs `aae041a` (revision `nexusaidev-app--0000099`; relayed from HANDOVER-S76D §0 and Tuesday's DELTA 56, not re-measured for this brief). **CI deploy from main is OFF:** `.github/workflows/deploy-demo.yml` gates its jobs on `vars.CI_DEPLOY_ENABLED == 'true'` (lines 53 and 91 at `982a84f`). The demo is not yours in any direction.
- **Never touch the `2_Project_Files` working checkout** (C-28: never write, pull, restore, reset, check out or stash it; C-67: never read it for product truth either). **Work in fresh worktrees at ABSOLUTE paths outside the clone**, cut from `origin/<ref>`, under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/` with an `-s79h` suffix (e.g. `.../worktrees/rd-616-s79h`). Do not reuse F's `-s77f` worktrees (11 of them; leave them). **Do not prune `worktrees/mkt-rc-selfcontained-s62/node_modules`** (other worktrees' node_modules chain to it; C-54 03:30Z).
- Every file:line you quote names its head, e.g. "server.js:1139 at 982a84f" (C-67).

## 1 — THE MERGE QUEUE: WHAT HAPPENS WHEN GATE 4 LANDS (no GO in this brief)
**You do not merge anything on this brief.** When gate 4's verdict reaches Tuesday, Tuesday mails you the merge GOs, each naming the branch and head. Expect them in this order:
1. **RD-575 first** (on gate-4 A GO). Main is its ancestor, so the merged tree must equal `6a32426`'s tree (Tuesday's scratch `merge-tree` of `982a84f` × `6a32426`: rc 0, clean). The GO mail will carry its conditions (ls-remote readings, C-89 pair, full verify through the lock, deploy job SKIPPED).
2. **RD-524 second, and NOT straight away** (on gate-4 B GO). RD-524's forward merge is onto `982a84f`, which does NOT contain RD-575. So after RD-575 lands, RD-524 needs **ANOTHER forward merge, onto main-with-RD-575**, and before it merges, a re-run on that merged tree of **gate 3's §6.4 cells plus A3/A3b leaker-first**, each arm proven to have executed (see LESSONS). Tuesday's scratch `merge-tree` of `6a32426` × `dc8635c`: rc 1, **CONFLICT in `scripts/verify-expected-counts.json` only** (resolved by regeneration, C-57); `server.js` and `jsonStorage.js` auto-merge. RD-575 changes `CUSTOMER_DATA_FILES`, which RD-524's evidence rule spreads (gate 3 §3.6), so a green merge-tree is not evidence the cells agree (C-68).
3. **RD-615 waits for gate 5** (batched with your RD-616). It will need a forward merge onto whatever main is by then. Tuesday's scratch `merge-tree` of `6a32426` × `b7fc78f`: rc 1, counts only, **`backend/dataErasure.js` auto-merges** (both touch it); `dc8635c` × `b7fc78f`: rc 1, counts only, `server.js` auto-merges. Both overlaps put RD-615's and RD-575's erasure cells in the C-68 re-run list.
- For every forward merge: this is a **short-lived branch**, so plain **C-57 (id-superset control) with C-112** applies. **C-133's base-aware accounting is for long-lived branches** (it was ruled for lane C's release-gate merge); do not reach for it here. A C-57 STOP stays a STOP.
- A gate NO-GO on B of the same class as F-A0 (test isolation) ships nothing new (C-62); Tuesday tickets the residue. You do not start a third round on it without Tuesday.

## 2 — YOUR BUILD QUEUE, IN ORDER (HANDOVER-S77F §1; board states read by Tuesday at 06:4x AEST, REST, read-only)
One branch per item off the CURRENT main, `-s79h` suffix. Each item: PRIOR WORK (C-49) → cells that assert the property after the fix (C-98) → red-proof → full verify → **READY FOR QA**. After each READY, go straight on to the next item; do not wait for its gate. If main moves under a branch before READY, forward-merge it (never rebase).
1. **RD-616** (To Do / High, labels `operations, s77f, security`) — gate-2 F-B2, MAJOR, pre-existing: mail secrets saved via `POST /api/setup/mail-config` are stored PLAINTEXT at rest in machine-id key mode, because `emailService._maybeEncrypt` calls `encryptValue(plain)` with no deps (`emailService.js:170` at `982a84f`), and `includeSecrets` export hands them out. **Fold in RD-617** (To Do / Medium): an export redactor given an unexpected store shape passes it through unchanged while the manifest says `redacted:true` (`dataExport.js`, lane A's under C-132). Fix shape and cells: RD-616's ticket and the gate-2 report §4.7 and §4.2 (`Testing Agent MAIN/projects/nexusai/reports/2026-09-21-gate2-rd495-rd525-rd575/report.md`).
   - **PRIOR WORK that binds this item: RD-413, Kam's decision of 2026-09-14 (comment 37521), option B:** *"no, the client gets to choose even if they overlook a component. Use option B."* When NO key source exists, the product keeps saving and tells the truth (no "Stored encrypted at rest" claim, a visible warning). RD-616 is the machine-id case, where a key source DOES exist and is simply not passed. **Do not turn RD-616 into a refusal to save.** The `_maybeEncrypt` comment at `:164-166` records RD-413 as deliberate; keep it true. If the fix would change the no-key-source behaviour, STOP and mail Tuesday: that is Kam's ruling, not ours.
   - File scope: `emailService.js` is granted above for this item.
   - **Its READY triggers gate 5** (RD-615 + RD-616, both tier 1).
2. **RD-607** (To Do / High) — gate-1 F-1: in Redis mode every limiter shares ONE `RedisStore` and one key per address. A change is STAGED at `session-tools/s77f/rd607-staged/` (`backend/server.js`, the cells `__tests__/rd607-redis-limiters-keep-their-own-counts.test.js`, the fake `__tests__/helpers/rd607-fake-redis.js`). **The staged `server.js` is a whole file made on `b966634`'s blob. Do NOT copy it over main; re-apply the change by hand on current main.**
   - ⚠ **Main now has SEVEN `_rlOpts(` call sites, not the six the handover and the staged file know.** RD-495/RD-498 (`d0d252c`) added `_cspReportLimiter` at `server.js:831` at `982a84f`, built lazily on first request because `_rlOpts` is declared further down. It needs a name too. Because it is built on first use, a duplicate-name check fires at the first `/csp-report` request, not at boot: say which you chose and why, and cover it with a cell.
   - **PRIOR WORK (read, don't re-derive):** PT-022 (`3f0783e`, 2026-04-26) routed every limiter through a single `_rlOpts()` helper and one Redis client *"so the store stays consistent"*, and added `rateLimitStore: 'redis'|'memory'` to `/api/admin/health`. That consistency was deliberate. **Keep ONE Redis client and the one helper; give each limiter its own store with its own prefix** (the library's remedy; the staged factory `_rateLimitRedisStoreFor(name)` does this under the `nexusai:rl:<name>:` root). Keep the health field.
   - Fold gate-1 F-2 (the "route's ONLY limiter" comment reword; the staged file has it). The faithfulness check against a real `redis:7.4-alpine` needs the **docker** lock as well as the jest lock.
3. **RD-583** (To Do / Medium) — re-arm the parked R10(i) scheme/port half from `__tests__/helpers/rd583-parked-NOT-RUN/rd516-r10i-scheme-port.test.js` (present at `982a84f`), through `checkEndpointName` (the name layer), not the async, DNS-resolving `assertAllowedAiEndpoint` (C-130 addendum). **Fix the parked header's wording per C-130 ADDENDUM 2** in the same change: 4 of the 9 names are refused BEFORE DNS at layers 0 and 1, and the header's "the assertions need no change" / "re-arm through checkEndpointName" contradiction goes. Also owed from C-128's addendum: the `ae98c74`-era R7 comment in `__tests__/rd516-ai-test-ssrf.test.js` — fix it in the next lane-A change that touches that file.
4. **RD-510** (To Do / High) — listen before the boot AI warm-up. F MEASURED it at `bdca588` (GOOD 1.1 s / STALL no listen by 420 s / THROTTLED10 17.1 s; RD-510 comment 37948; `session-tools/s77f/rd510-measure.json`). **That measurement leaked a never-listening server and held the jest lock ~57 minutes: RD-619** (To Do / Medium, the rd395 harness `bootServer` throws without killing the child). Your measurement and cells must spawn directly and **kill the child by a deadline in a `finally`**. Decide whether RD-619 rides with RD-510 (same harness) and say so in the READY.
5. **RD-531 + RD-497** (both To Do; RD-531 High `blocker`, RD-497 Medium). RD-531: `jsonStorage.appendErasureRequest` still does not exist at `982a84f` (`server.js:1964` guards on `typeof … === 'function'`, and `jsonStorage.js` has no such function). RD-497: C-129 moved ONE route (`GET /api/admin/csp-violations`), and it is on main now (via RD-495, `f1319ac`). **The other 15 routes are per-route decisions, each "from its prior work".** Put a census note on RD-497 (F's handover asks for it).
6. Then **RD-438 → RD-487 → RD-457 → RD-492 → RD-519 → RD-475 → RD-520** (all To Do / Medium; RD-520 "measure first"). Starting measurements are in `session-tools/s76d/lane-RD-*.txt` (S76D's board dump, 2026-09-21 19:26) and HANDOVER-S76D §6.
- **Read-only board check at drafting: none of the queue's tickets is stale.** All of RD-616, 617, 607, 583, 510, 619, 531, 497, 438, 487, 457, 492, 519, 475, 520 read **To Do**. RD-575, RD-524, RD-404, RD-441 and RD-615 read **Testing** (at QA). RD-627 (the second-SIGTERM `.tmp`) reads To Do / Low. Re-read each before you start it.

## LESSONS FROM S77F — STANDING LINES, not history (HANDOVER-S77F §2 and its wrap)
- **Every ordered or sequenced jest run must PROVE it executed** before its exit code means anything: quote the suite count and the order line it printed. F's RD-524 leaker-first arms printed `exit 1` from `Cannot find module '@jest/test-sequencer'` and were first reported as results. A harness file outside the repo cannot `require` repo packages by name; resolve from jest's cwd (`createRequire(<wt>/package.json)`).
- **A harness that spawns a server must kill it on a deadline, in a `finally`.** RD-619 is the leak; it held the shared lock ~57 minutes.
- **A proof run killed by the harness is VOID, and is reported as VOID** (F's first RD-615 hold, killed by a second SIGTERM: `rd615-proof-hold-run1-VOID-double-sigterm.log`). Never count it, never quietly re-run over it. The SIGTERM flush is `process.once`: tests that trigger it wait for the process to exit on its own (RD-627).
- A carried "would pass today" claim is not a measurement (C-130 addendum). Every red-proof hold needs a CLEAN arm beside the mutants.
- `verify-suite` fails any skip (`passed != total`). Park unbuilt cells under `__tests__/helpers/<x>-NOT-RUN/` (C-130); never `test.skip`.
- Never detach a hold with `&`; run holds attached (`run_in_background`). A detached hold reparents to launchd and the counter aborts with "no claude ancestor".
- Old fixtures seeding `authEnforced` without Entra IDs read as "setup open": seed the all-zero GUIDs.
- Cite the right entry. F's `71f2949` message cites "C-131" for what is C-132; it is recorded in C-132 and not rewritten. Check the number against CLARIFICATIONS before you type it.
- Jira: Testing = transition **"In Review"**; Release Ready = **"Tested - Release Ready"**. Write your own `session-tools/s79h/jwrite.py` from F's (`session-tools/s77f/jwrite.py`); read with `session-tools/s76d/jread.py`.

## PRIOR-WORK CHECK (C-49) — before building each item
`git log --all -S` on the symbols you change; `git log --all --grep` for the ticket id; the branch list; `session-tools/s76d/lane-RD-*.txt`; HANDOVER-S59, S65, S70, S76D, S77F; the tickets' comments; `5_Project_History/`. Write down what existed, when, which round introduced it and why, or "no source found". Keep what works (C-50). RD-413 (for RD-616) and PT-022 (for RD-607) above are the kind of thing this check exists to catch.

## FLOOR — C-110's four clauses, with C-125's counter as corrected by RD-606
1. **Every** jest invocation goes through `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh jest <tag> …` with `--maxWorkers=2`, including probes and single suites. Docker (a real Redis for RD-607) also takes `nexusai-lock.sh docker`. **The jest lock is shared with NexusAI-G and the QA gate(s). It is a FIFO queue: take a ticket and wait. Never break, take over or jump it.** At 06:45 the order was gate 4 (holding) → G (queued).
2. **Hold the lock ONCE across a multi-run measurement** (a red-proof set, the regenerate-then-verify pair). Never per run.
3. **Record the foreign-server count beside every result** with `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76e/floorcheck.py` (basename of argv[0] is `node` AND an argument ending `backend/server.js` ANYWHERE in argv). **RD-606: "ours" means the server's ancestor chain contains YOUR OWN claude pid** (the script finds the nearest `claude` ancestor of itself; it prints `anchor=claude:<pid>`). **Check that the printed anchor is YOUR claude pid from §0** and quote it. Shared ancestors (tmux, launchd) prove nothing. Run `--selftest`, and use `--expect-foreign <pid>` as the negative control (G's claude `57419` or a gate server is a real foreign pid). `session-tools/s77f/floorcheck.py` is byte-identical to the s76e copy; either works. Do NOT use `session-tools/s76d/floorcheck.py` (its ancestry was wrong).
4. **A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED IN THE SAME WINDOW.** Spawn a control the harness's way, require the count to RISE, reap it.

Reap everything you start. Before each red-proof, write down which cells you expect to redden and how many (F's `expect-*.txt` files are the template). Templates for holds: `session-tools/s77f/fwd-merge-hold.sh`, `rd524-r2b-hold.sh`, `rd615-proof-hold.sh`.

## HELD — decisions this seat is NOT making
- **No merge to main, and no push to any branch you did not create, without a Tuesday GO mail naming the branch AND its head sha.** That includes RD-575, RD-524 and RD-615, whose branches are F's and are gated as they stand. If a GO asks you to forward-merge one of them, it will say so and name the head.
- **Kam's, and untouched:** the 2.2.0 image build and push to `nexusaireleaseacr`; Partner Center; any upload or submission; RD-594's scope; RD-362's rotation; the C-124 Key Vault success-path proof; production, money, external comms. needs-decision and not yours to decide: RD-610, RD-612, RD-622.
- **Not this seat's:** a demo redeploy (it needs a separate Tuesday GO under C-127); any `az` write, registry change or Container App revision.
- No force push. No `--no-verify`. Never rebase a pushed branch (a rebased branch gets a new name).
- Never touch the stale `2_Project_Files` working checkout (C-28, C-67).
- No edit in lane C's files (§0) or on G's branches. `README.md` ask-first. No edit to `PRIVACY.md` or `TERMS_OF_SERVICE.md` (C-65, C-105). No hand edit to `scripts/verify-expected-counts.json` (C-57).
- **Vault:** stage Datasec paths one by one, never `git add -A`. The vault is **7 ahead / 527 behind** its upstream (measured 06:4x); `daily/2026-09-21.md` is modified and `daily/2026-09-22.md` is untracked, both carrying earlier seats' uncommitted appends (S76D, S76E, S77F). **Do NOT commit or touch those appends; leave them.**

RULED BY KAM, NOT YET IN AN ARTEFACT
- None. `decision_queue.sh list ruled --undelivered nexusai-` returns **0** (control: 67 lines naming `nexusai-` in the unfiltered ruled list). C-126 and C-127 are in CLARIFICATIONS. RD-413's option B (above) is recorded on the ticket, comment 37521.

RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- **C-132** (Tuesday, ANSWER 2026-09-21T19:39:40Z): lane B's three files are lane A's, for new work tied to a ticket in your queue; RD-575's branch stays merge-only.
- **C-133** (Tuesday, ANSWER 2026-09-21T19:46:03Z, RD-626): base-aware C-57 accounting, **for long-lived branches only**. For your short-lived forward merges plain C-57 with C-112 applies unchanged (C-133's own "Not covered" line).
- **C-131** (Tuesday, ANSWER 2026-09-21T18:10:32Z, RD-625): when a merge brings together a check that pins a feature and a branch that REMOVED it, the removal wins and the check is re-anchored in the merge commit. It was ruled for lane C and widens nothing for you; it is here so you recognise the shape if a forward merge of yours reddens a precondition.
- **C-130** (+ both addenda): park, never skip; R10(i) split; RD-583 re-arms the parked half through the name layer.
- **C-129:** one route moved; the other 15 RD-497 routes are per-route decisions in lane A's RD-497 work.
- **The lane partition** (`710e875`, measured at `aae041a`) as amended by C-132, with `DEPLOYMENT_GUIDE.md` lane C's since RD-516 landed (`47be2b0`).
- **The merge queue:** RD-575 → RD-524 (re-forward-merged onto main-with-RD-575, §6.4 cells + A3/A3b leaker-first re-run) → RD-615 after gate 5. Each on its own GO.
- **A tree-equal main merge needs no second verify** (Tuesday 2026-09-21T17:31:44Z, relayed in HANDOVER-S77F §2).
- C-98, C-110 + C-125 (+ RD-606), C-67, C-49, C-57/C-68/C-89 as above. **C-91:** your HISTORY entry goes on `s79h-history-docs`, never to main directly.

## READY FOR QA — one per item, to `tuesday-agent@agentmail.to`
Subject: `[Datasec/NexusAI-H -> Tuesday] READY FOR QA: <ticket> <one line>`. Body sections, in order:
1. **Branch and head sha**, pushed and read back with `git ls-remote origin`, and the main sha it is cut from.
2. **PRIOR WORK** (C-49), or "nothing replaced".
3. **What changed**: the files, each inside lane A (list any file outside it, and the Tuesday answer that allowed it).
4. **RED-PROOF**: the cells you expected to redden, written down first. Fix reverted → those cells red (quoted). Fix restored → green. One lock hold, with a CLEAN arm, **each arm's proof of execution quoted** (suite count, order line where order matters).
5. **Full verify** through the lock, the four floor clauses evidenced (anchor pid quoted). Honest N/M, read not inferred. Counts regenerated and COMMITTED if they changed (C-89 pair quoted). Any VOID run named as VOID.
6. **Verdict line**, and **what you did NOT test**.

## PLAN CONFIRMATION, then START
Send first: `[Datasec/NexusAI-H -> Tuesday] QUESTION: plan confirmation`. It must carry:
- your process-table reading (launcher pid, claude pid, pane, label);
- any launcher preflight warnings, VERBATIM;
- main, `rd-575-purge-reaches-attachments-s76e`, `rd-524-404-441-s77f` and `rd-615-audit-flush-epoch-s77f` as you read them by `ls-remote`;
- your worktree paths;
- the jest lock's owner and queue at that moment (`session-tools/locks/`);

**Then start straight away, without waiting,** on RD-616. What waits for an answer: a merge (always a separate GO), a moved head you depend on, new scope, a file outside lane A, or anything in HELD.

## WRAP
Rotate yourself at 80-90% context. Write `HANDOVER-S79H.md` in the NexusAI project root (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/`), naming each item, branch, head and next step. Push a wip snapshot of each build branch before every lock wait. At wrap:
- mail `tuesday-agent@agentmail.to`, subject `[Datasec/NexusAI-H -> Tuesday] Session wrap 2026-09-22` (or the date you wrap);
- a HISTORY entry on `s79h-history-docs` (C-91);
- confirm `.env` is not staged;
- in the vault, stage Datasec paths only, one by one, and leave the earlier seats' uncommitted daily-note appends alone.

PROVENANCE:
- main = 982a84f2d0c72596a2d389897439e1d8d3425068; rd-575 = 6a32426a7aa7b847cd2ec0ab89f0ec3bdc2fe71e; rd-524 = dc8635c50b7fd607f8845f39729f4f2ad5614bcb; rd-615 = b7fc78f2cb4e3650f4e045596688beed924aeaaa; s77f-history-docs = 44eb58acdf59654272374b8fb285ca4ed7eb3a2a; mkt-release-gate-s78g = 5b6a24fb3ce704f8cbae0b8dbb4dec3cbc05836f | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin` at 06:44:34 AEST | read 2026-09-22
- bdca588, 47be2b0, f1319ac ancestors of 982a84f; 982a84f's log (RD-525 merge of 845af47) | `git merge-base --is-ancestor`, `git log --oneline -8 982a84f` | read 2026-09-22
- main ancestor of 6a32426 / dc8635c / b7fc78f; left/right 0/5, 0/5, 0/4; each branch's files vs main; each branch's commits | `git merge-base --is-ancestor`, `git rev-list --left-right --count`, `git diff --name-only 982a84f <sha>`, `git log --oneline 982a84f..<sha>` | read 2026-09-22
- counts 3860/219 (982a84f), 3868/220 (6a32426), 3902/221 (dc8635c), 3864/220 (b7fc78f), 3797/216 (aae041a) | `git show <sha>:scripts/verify-expected-counts.json` | read 2026-09-22
- merge-trees: 982a84f×6a32426 rc 0; 6a32426×dc8635c rc 1 counts only; 6a32426×b7fc78f rc 1 counts only, dataErasure.js auto-merged; dc8635c×b7fc78f rc 1 counts only, server.js auto-merged | `GIT_OBJECT_DIRECTORY=<Tuesday's scratchpad>/objs GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git merge-tree --write-tree --name-only` (nothing written to the repo) | read 2026-09-22
- CI_DEPLOY_ENABLED at deploy-demo.yml:53 and :91 | `git grep -n CI_DEPLOY_ENABLED 982a84f -- .github` | read 2026-09-22
- demo aae041a rev 0000099 | HANDOVER-S76D §0 and NEXT-PICKUP-TUESDAY.md DELTA 56 (relayed, not re-measured) | read 2026-09-22
- seven `rateLimit(_rlOpts(` sites at 982a84f (:831 _cspReportLimiter lazy, :1139, :1152, :1186, :1202, :1237, :16593); _cspReportLimiter added by d0d252c | `git grep -n "rateLimit(_rlOpts(" 982a84f -- backend/server.js`; `git show 982a84f:backend/server.js` lines 815-845, 1098-1140; `git log -S_cspReportLimiter 47be2b0..982a84f` | read 2026-09-22
- staged RD-607 = whole server.js on b966634's blob, six named sites, `_rateLimitRedisStoreFor(name)`, prefix `nexusai:rl:${name}:` | `diff <(git show b966634:backend/server.js) session-tools/s77f/rd607-staged/backend/server.js`; `find session-tools/s77f/rd607-staged` | read 2026-09-22
- PT-022 "so the store stays consistent", rateLimitStore health field | `git show 3f0783e` (message and server.js hunk); `git log --all -S_rlOpts -- backend/server.js` | read 2026-09-22
- _maybeEncrypt at emailService.js:167-172, encryptValue at :170, RD-413 comment at :164-166 | `git show 982a84f:backend/services/emailService.js` lines 160-176 | read 2026-09-22
- emailService.js not in lane A (partition row) nor lane C (G brief "YOUR FILES"); RD-516's services files precedent | `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md` line 29; `fleet/briefs_staged/2026-09-22_nexusai_G_laneC_brief.md` | read 2026-09-22
- RD-413 Kam option B (comment 37521); RD-616 text and fix shape | `session-tools/s76d/jread.py RD-413`, `jread.py RD-616` (REST GET, read-only) with the project's Jira env | read 2026-09-22 06:4x AEST
- ticket states: RD-616 To Do/High; RD-617 To Do/Medium; RD-607 To Do/High; RD-583 To Do/Medium; RD-510 To Do/High; RD-619 To Do/Medium; RD-531 To Do/High [blocker]; RD-497 To Do/Medium; RD-438, RD-487, RD-457, RD-492, RD-519, RD-475, RD-520 To Do/Medium; RD-615 Testing/High; RD-575 Testing/Medium; RD-524 Testing/High; RD-404 Testing/Medium; RD-441 Testing/High; RD-627 To Do/Low | `session-tools/s76d/jread.py <KEY> 0 0` | read 2026-09-22 06:4x AEST
- appendErasureRequest: guarded call at server.js:1964-1965, absent from backend/jsonStorage.js at 982a84f | `git grep -n appendErasureRequest 982a84f -- backend` | read 2026-09-22
- parked RD-583 file present at 982a84f | `git ls-tree -r --name-only 982a84f -- __tests__/helpers/rd583-parked-NOT-RUN/` | read 2026-09-22
- C-128 addendum, C-129, C-130 + addenda 1 and 2, C-131 (lane C, 18:10:32Z), C-132 (19:39:40Z; 71f2949's "C-131" miscitation), C-133 (19:46:03Z, long-lived only; "short-lived branches (plain C-57 applies unchanged)") | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md lines 1366-1431 (1431 lines) | read 2026-09-22
- F's state table, NEXT order, lessons, floor templates, tickets filed, Kam-only list | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S77F.md (mtime 06:42 AEST) and session-tools/s77f/mail-20-wrap.txt | read 2026-09-22
- gate 4 targets, merge queue RD-575 → RD-524, "ANOTHER forward merge … gate 3 §6.4's list, plus A3/A3b leaker-first" | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate4-rd575-rd524r2.md §2, §6 - my project, not yours | read 2026-09-22
- RD-615 to be batched as gate 5 with RD-616 | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/daily_tuesday/2026-09-22.md, 06:41 line | read 2026-09-22
- floor: G pane %36 launcher 57417 claude 57419 (03:44:19); gate 4 pane %37 launcher 95252 (05:46:57); lock owner qa-gate4-hold2 pid 89297 since 20:40:18Z; queue ticket s78g-rd526 pid 89703; %0 33220, %3 54400, %8 69949; no %34 | `tmux list-panes -a`, `ps -axo pid,ppid,lstart,command` filtered on `[cockpit]`/`nexusai-lock`, `session-tools/locks/nexusai-jest.lock/owner`, `session-tools/locks/queue-jest/*` at 06:45 AEST | read 2026-09-22
- F pane %34 closed at 06:44 | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/daily_tuesday/2026-09-22.md, 06:44 line; absent from `tmux list-panes -a` | read 2026-09-22
- s76e/floorcheck.py == s77f/floorcheck.py (byte-identical); nearest-claude-ancestor anchor | `diff`; header and `my_anchor()` | read 2026-09-22
- lock is FIFO, owner file, queue tickets | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh header | read 2026-09-22
- zero undelivered `nexusai-` rulings (control 67 lines) | `bash /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered nexusai-` and the unfiltered `list ruled` | read 2026-09-22
- vault 527 behind / 7 ahead; daily/2026-09-21.md modified, daily/2026-09-22.md untracked | `git -C "/Volumes/KK_T9_External_HDD/Notes (MASTER)" status --short -- daily/…`, `rev-list --left-right --count @{u}...HEAD` | read 2026-09-22
- HOSTING_AND_COST_ANALYSIS.md :16/:31/:172 ruled (A) to G | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/daily_tuesday/2026-09-22.md, 06:22 line | read 2026-09-22
- no `Datasec/NexusAI-H` routing line yet (G's is line 63) | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/inbox_routing.conf | read 2026-09-22
Self-check note: re-read whole by Tuesday; the emailService.js question was replaced by a grant at every mention (§YOUR FILES, RD-616 file scope, PLAN CONFIRMATION); no other contradiction found.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-22 06:50
