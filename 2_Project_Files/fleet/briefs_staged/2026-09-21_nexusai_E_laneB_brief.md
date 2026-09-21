# BLUF — FRESH SEAT Datasec/NexusAI-E: LANE B OF THE STAGE-2 PARTITION. RD-525, then RD-575, in that order. One branch each off main `aae041a`. Each ends at READY FOR QA to Tuesday. NO MERGES.

**This brief is addressed to the cockpit seat `Datasec/NexusAI-E` only.** It is not addressed to `Datasec/NexusAI`, `Datasec/NexusAI-D` or any other suffix. The inbox `datasec-nexusai@agentmail.to` is SHARED by NexusAI-D and NexusAI-E, so a mail addressed to another seat is not yours, however familiar its conversation looks.

**Authority:**
- Kam to the Tuesday seat, 2026-09-21 ~15:2x AEST, typed, verbatim: **"keep working through it and email me the zip when it's ready to upload and resubmit."** This is the Marketplace RESUBMISSION push, the remediation of RD-549. RD-525 is on the C-54 resubmission checklist, and RD-575 carries the board's `blocker` label.
- The partition is Kam's standing rule as applied by S76D: *"as many agents as the code allows, never two on the same file."*
- C-32: Tuesday authorises commissioning and sequencing. The GO for the plan AS BRIEFED is given now (see PLAN CONFIRMATION).

**Read first:** CLARIFICATIONS C-28, C-49, C-54 (with its 2026-09-17 13:04:44Z addition), C-57, C-65, C-67, C-68, C-89, C-91, C-98, C-110, C-125, C-126, C-127. Then the partition and the path map on branch `s76d-path-map` @ `710e875`. Read them with `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md` and `git show 710e875:docs/resubmission/2026-09-21_path-to-resubmission-zip.md`. Also read HANDOVER-S70.md (the cells), the two tickets, and the S70 census.

## 0 — ESTABLISH YOUR SEAT FROM THE PROCESS TABLE FIRST
Walk your own shell's parent chain to the `zsh -c` launcher process. Its command line ends `[cockpit] Datasec/NexusAI-E exited — pane stays for inspection`. Record that pid and your tmux pane id, and put both in the plan confirmation. **If the walk ends at any other label, that is the finding: do nothing else, and mail Tuesday.** Never decide which seat you are from which conversation in the inbox looks like yours. Use session tag **S76E** in branch names, files and mails.

**The other seats, by what each can measure about itself:**
- **Lane A = `Datasec/NexusAI-D`, session S76D, tmux pane `%30`, launcher pid `13411`, started 2026-09-21 17:39:50 AEST.** It owns `backend/server.js`, `backend/jsonStorage.js`, `backend/bootPreflight.js`, `static/**` (the `static/js/*.js` files and `static/*.html`), `.dockerignore` and `Dockerfile`. Its order: RD-516 → RD-495 → RD-524/404/441 → RD-531 + RD-497 → RD-510 → the rest.
- **Lane C = not started; no seat exists for it at the time of writing.** When it starts, it owns `azure-marketplace/**`, the packaging scripts (`scripts/marketplace-package-build.sh`, `scripts/validate-marketplace-template.sh`, `scripts/build-plan-packages.sh`), `bicep/` and `DEPLOYMENT_GUIDE.md`.
- **If RD-525 or RD-575 needs ANY change in `backend/jsonStorage.js` or `backend/server.js`** (for example a session-cache flush), lane B MAILS Tuesday the request with the exact diff and the cell that needs it. **Lane B never edits those files.** Keep building what you can. If the missing change blocks the ticket, say so and move on to the next.

## STATE OF MAIN — do not change it
- `main` = **`aae041a`** (RD-518 landed, 3797/3797 per the path map). Re-read it with `git ls-remote origin refs/heads/main` before cutting each branch, and quote the sha.
- Pending branches that are NOT yours and do NOT touch your three files: `rd-516-ai-test-ssrf-s73` @ `b966634`, `rd-604-rd423-timer-s76d` @ `172abc8`, `rd-495-csp-violations-hard-gate-s71` @ `5ce2b62`, and the package branch `mkt-selfcontained-pkg-s64` @ `a643fe1`. Measured with `git diff --name-only`. Never touch them.
- **Never touch the `2_Project_Files` working checkout** (C-28, C-67). It is stale by design. Don't write, pull, check out, reset, stash or even read it for product truth. **Work in worktrees at ABSOLUTE paths outside the clone**, cut from `origin/main`: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/rd-525-s76e` and `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/rd-575-s76e`. Never use a relative path (C-67). Do not prune `worktrees/mkt-rc-selfcontained-s62/node_modules`, because other worktrees chain to it (C-54).
- Every file:line you quote names its head, for example "dataErasure.js:691 at aae041a".

## 1 — RD-525: export and erasure must cover every store holding personal data
Branch `rd-525-export-erasure-coverage-s76e` off `aae041a`.
- **The defect, measured by S65 and censused by S70.** Four stores holding personal data are in neither list in `backend/customerDataFiles.js`: `authorized_users.json`, `sessions.json`, `user_assignments.json` and `quick_questions.json`. The ticket's own line also names the audit buffer (IP addresses) and feedback attachments. **Feedback attachments are RD-575's. Do not solve them here.**
- **Prior cells exist and have NEVER RUN:** `session-tools/s70/rd525-cells/rd525-export-and-erasure-cover-every-store.test.js`, with cells E1-E4, N1, E2b and E3. They derive scope FROM `customerDataFiles.js` and never hard-code it. Keep that. **N1 is the red cell of the file.** **E1's `exportEntryNames()` throws by design** ("deliberately unimplemented"). HANDOVER-S70: **"RD-525 must not merge until E1 is wired."** Wire it to `POST /api/admin/export`. Never skip it and never stub it green.
- 🔴 **C-54's gate requirement, which the S70 cells do NOT yet carry:** *"a pre-erasure session no longer signs in after erasure, with and without a restart."* Add that as its own pair of cells: one without a restart, one across a restart. Each needs a findability control first: the session DOES sign in before the erasure, read by the same path the assertion uses (C-98). Sessions also live in `jsonStorage`'s memory. **If making the no-restart cell green needs a `jsonStorage.js` or `server.js` change, that change is lane A's: mail the exact diff to Tuesday (see section 0).**
- **Two things are Kam's, so leave them to him:**
  - `printer_logs.db` is an open decision on RD-536 row 10. If he says nothing, it stays out of scope. Deriving scope from the product keeps the cells right under either ruling.
  - `PRIVACY.md` is NOT edited (C-65). S70 measured E3 **red in both directions** against the policy text. That drift goes to Kam on RD-536 and is not fixed in the file.
- **If a cell can go green only by editing PRIVACY.md, or only by weakening the cell, do neither.** Report it in the READY for Tuesday's ruling.
- At `aae041a` the only consumers of `customerDataFiles.js` are `backend/dataErasure.js`, `backend/dataExport.js` and `__tests__/customer-data-lists-agree.test.js`. Re-measure them on your head, and list them in the READY.
- S59's RD-404/441 WIP (`b587646`) spreads `CUSTOMER_DATA_FILES` into `jsonStorage.js`. If lane A keeps that piece in RD-524, your list change reaches lane A's sentinel. **Say so in the READY; do not act on it.**

## 2 — RD-575: the erasure purge loop is file-only, so `feedback-attachments/` can never be purged
Branch `rd-575-purge-reaches-attachments-s76e` off `aae041a`. Start it after RD-525's READY is sent, without waiting for RD-525's gate.
- **The defect, read at aae041a:** `for (const fname of PURGE_FILES)` at `backend/dataErasure.js:691`. `PURGE_FILES` is `CUSTOMER_DATA_FILES` (`:48`), and nothing in the loop traverses a directory. The attachments are a tree at `<DATA_DIR>/feedback-attachments/<feedbackId>/<hex>`.
- **The fix has the right SHAPE:** a recursive removal plus its recovery copies. **Adding `'feedback-attachments'` to `CUSTOMER_DATA_FILES` is NOT the fix.** It makes the list claim coverage while `fs.unlink` fails on a directory and the failure is swallowed.
- **Prior cells exist and have NEVER RUN:** `session-tools/s70/rd575-cells/rd575-purge-reaches-attachments.test.js`, with CTRL-1, CTRL-2, C1, C1b and C2, plus the `purgeThrew` term.
- **THE TRAP-CELL RULE, C-98:** a cell asserts the PROPERTY THAT MUST HOLD AFTER THE FIX and never pins the defect. So:
  - **every name in `CUSTOMER_DATA_FILES` is actually removed by a purge**, including a directory-shaped one;
  - **the `feedback-attachments/` directory itself is purged**.
  - Check that S70's C2 is written in that form before you adopt it. A cell that would go RED once the ticket closes is a bug-pin; rewrite it.
  - A red that arrives **with** `purgeThrew: true` means the diagnosis is wrong. In that case the ticket is re-measured and not fixed: stop, and mail Tuesday.
- **Both of your branches edit `customerDataFiles.js` and `dataErasure.js`.** In RD-575's READY, quote `git merge-tree --write-tree origin/main <rd-575 head>` and the same against RD-525's head. After RD-525 merges, RD-575 takes a forward merge of main. **Never rebase.** Then it re-runs the named affected cells on the new head (C-68).

## PRIOR-WORK CHECK (C-49) — before building each ticket
Look first:
- `git log --all -S` on the symbols you will change;
- `git log --all --grep` for the ticket id;
- the branch list;
- `session-tools/s70/`, `session-tools/s76d/lane-RD-525.txt` and `lane-RD-575.txt`;
- HANDOVER-S65, S70 and S76D;
- the tickets' comments (RD-525 c.37866, RD-575 c.37861);
- the S65 measurements and the S70 census in `5_Project_History/`.

Write down what existed, when, which round introduced it and why, or write "no source found". The existing RD-321 erasure machinery (the partial-purge record and the backups reach) and the eight `__tests__/erasure-*.test.js` files are prior work. **Extend them; do not replace them.** Keep what works (C-50). Measured at drafting: there is no RD-525 or RD-575 branch, and no commit for either except a HISTORY docs mention.

## FLOOR — C-110's four clauses, with C-125's counter
1. **Every** jest invocation goes through `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh jest <tag> …` with `--maxWorkers=2`. That includes probes, single suites and scratchpad scripts.
2. **Hold the lock ONCE across a multi-run measurement**, for example a red-proof pair. Never take it per run.
3. **Record the foreign-server count beside every result.** Match processes where the **BASENAME of argv[0]** is `node` **AND the entry point appears ANYWHERE in the remaining argv**. Never use raw `comm`, which is blind on macOS. Never rely on the first argument, which misses `node -r <preload> … server.js`. Separate your processes from foreign ones by **ancestry**.
4. **A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED IN THE SAME WINDOW.** Spawn a control the harness's way, require the count to RISE, then reap it.

Reap everything you start. **Before each red-proof, write down which cells you expect to redden and how many.** A red you did not aim at is a finding.

## HELD — decisions this seat is NOT making
- No merge, and no push to `main`.
- No deploy, and no demo redeploy.
- No real Azure, credential, vault, tenant, key or registry.
- No Partner Center, no production, no money, no external comms.
- No force push, and no `--no-verify`.
- No edits outside `backend/customerDataFiles.js`, `backend/dataErasure.js`, `backend/dataExport.js` and NEW test files. **If an existing test file must change, name it in the plan confirmation and wait for Tuesday.**
- No edit to `PRIVACY.md` or `TERMS_OF_SERVICE.md` (C-65). No hand edit to `scripts/verify-expected-counts.json` (C-57); regenerate it on your own branch only.
- Never touch the `2_Project_Files` working checkout.
- **This seat is not merging either branch, not deciding `printer_logs.db`, and not deciding any PRIVACY.md wording.**

RULED BY KAM, NOT YET IN AN ARTEFACT
- None. `decision_queue.sh list ruled --undelivered nexusai-` returns 0. C-126 and C-127 are both recorded in CLARIFICATIONS.
- Context only: C-127, Kam 2026-09-21 18:18:12 AEST, verbatim: *"Until we have a stable version, feel free to redeploy, merge, or do anything else to get us to a point where everything is fully ready."* Tuesday's reading is that merges and demo redeploys are **Tuesday's GO on a QA-gated head**. **It gives this seat no merge rights.**

RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- The lane partition as measured at `aae041a`. Lane B owns the three files above; `jsonStorage.js` is lane A's, and lane B asks rather than edits.
- C-98 (cells assert the property, never the defect), C-110 + C-125 (the floor), C-67 (absolute worktree paths, named heads), and C-49 (PRIOR WORK in every READY).
- C-57, C-68 and C-89 (counts regenerated on the tree that exists, re-staged, and quoted before any push). C-91: your HISTORY entry goes on your own history branch and is resolved as a union later. Never commit it to main.

## READY FOR QA — one per ticket, to `tuesday-agent@agentmail.to`
Subject: `[Datasec/NexusAI-E -> Tuesday] READY FOR QA: RD-525 <one line>` (and later RD-575). Body sections, in order:
1. **Branch and head sha**, pushed and read back with `git ls-remote origin`.
2. **PRIOR WORK**, as described above, or "nothing replaced".
3. **What changed**: the files, each inside lane B, plus any `jsonStorage.js`/`server.js` request, with its exact diff.
4. **RED-PROOF**: the cells you expected to redden, written down first. Then: fix reverted → those cells red (quoted). Fix restored → green. Both under one lock hold.
5. **Full verify**: run through `nexusai-lock.sh`, with the four floor clauses evidenced (lock tag, foreign count by the C-125 form, the control rose, everything reaped). Give the honest N/M, read and not inferred.
6. **Verdict line**, and **what you did NOT test**.
7. **For Kam, via RD-536**: any PRIVACY.md contradiction you measured.

**Nothing merges without Tuesday's GO.** Keep going to the next ticket after each READY; do not wait for its gate.

## PLAN CONFIRMATION, then START
Send the plan confirmation first: `[Datasec/NexusAI-E -> Tuesday] QUESTION: plan confirmation`. It must carry:
- your process-table reading (launcher pid, pane, label);
- any launcher preflight warnings, VERBATIM;
- `main` as you read it;
- your two worktree paths.

**Then start straight away, without waiting.** The GO for the plan as briefed is given. Only a deviation waits for an answer: new scope, a file outside lane B, an existing test edit, or anything in HELD.

## WRAP
Rotate yourself at 80-90% context. Write `HANDOVER-S76E.md` in the NexusAI project root, naming the ticket, branch, head and next step. Push a wip snapshot of each branch before every lock wait. At wrap:
- send a mail to `tuesday-agent@agentmail.to` with subject `[Datasec/NexusAI-E -> Tuesday] Session wrap 2026-09-21`;
- add a HISTORY entry on your own history branch (C-91);
- confirm `.env` is not staged;
- in the vault, stage Datasec paths only, one by one. Never use `git add -A` there.

PROVENANCE:
- main = aae041a0d01113144cadadba3a44f19025b08d85 | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin refs/heads/main` (run twice, the second at 19:36 AEST) | read 2026-09-21
- the three lanes, lane B = RD-525 then RD-575, its three files, lane A and lane C file sets, the jsonStorage ask-not-edit rule, the C-54 session risk | `git show 710e875:docs/resubmission/2026-09-21_stage2-lane-partition.md` (s76d-path-map = 710e875 by `git ls-remote origin`) | read 2026-09-21
- the resubmission stages, RD-525 and RD-575 rows (not built), main green 3797/3797 at aae041a | `git show 710e875:docs/resubmission/2026-09-21_path-to-resubmission-zip.md` | read 2026-09-21
- the three lane B files exist at aae041a (blobs f16dfe2, 06f630c, 396b2cf) | `git ls-tree aae041a backend/customerDataFiles.js backend/dataErasure.js backend/dataExport.js` | read 2026-09-21
- no pending branch touches the three files: rd-516 b966634, rd-604 172abc8, rd-495 5ce2b62, pkg a643fe1, zero lines each; control: server.js IS listed on rd-516 (1 line) | `git diff --name-only aae041a...origin/<branch>` filtered on the three names | read 2026-09-21
- NexusAI-D = launcher pid 13411, pane %30, label Datasec/NexusAI-D, started 17:39:50 AEST | `ps -o pid,ppid,lstart,command -p 13411` and `tmux list-panes -a` | read 2026-09-21
- only one NexusAI cockpit seat running at drafting (D); no E, no lane C | `ps -axo pid,lstart,command` filtered on the cockpit label | read 2026-09-21
- RD-525 To Do / High, blocker label, S70 comment 37866 (cells written, NOT RUN, E3 red both ways) | board dump written by S76D at 19:26 AEST, /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76d/lane-RD-525.txt (not re-read from Jira by Tuesday) | read 2026-09-21
- RD-575 To Do / Medium, blocker label, cell shape ruled in comment 37861 | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76d/lane-RD-575.txt (same S76D dump) | read 2026-09-21
- C-54 RD-525 gate sentence "a pre-erasure session no longer signs in after erasure, with and without a restart" | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-54 ADDED 2026-09-17 13:04:44Z | read 2026-09-21
- C-98 cell asserts the property after the fix, RD-575 C2 invariant, purgeThrew | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-98 | read 2026-09-21
- floor four clauses and the counter form | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-110 and C-125 | read 2026-09-21
- stale checkout never touched or read, absolute worktree paths | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-28 and C-67 | read 2026-09-21
- counts regeneration, head-bound verdicts, pre-push check, HISTORY union; rebased branches get a new name and are never force-pushed | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-57 (and its 04:01:23Z widening), C-68, C-89, C-91 | read 2026-09-21
- PRIVACY.md not edited; contradictions go to RD-536 | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-65 | read 2026-09-21
- prior-work check and PRIOR WORK section | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md, C-49 and C-50 | read 2026-09-21
- Kam's C-127 words and C-126 recorded; zero undelivered NexusAI rulings | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md C-126, C-127; `bash /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered nexusai-` = 0 | read 2026-09-21
- S70 RD-525 cells NOT RUN, E1 throws by design, no sign-in or restart cell (0 hits; control: "sign" 2 hits in the same file) | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s70/rd525-cells/rd525-export-and-erasure-cover-every-store.test.js | read 2026-09-21
- S70 RD-575 cells NOT RUN, C2 titled as the every-name invariant | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s70/rd575-cells/rd575-purge-reaches-attachments.test.js | read 2026-09-21
- "RD-525 must not merge until E1 is wired" | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S70.md | read 2026-09-21
- the four census stores and the S65 measurement | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/5_Project_History/2026-09-20_S70_rd525-personal-data-census.md and 2026-09-17_S65_rd524-rd525-measurements.md in the same folder | read 2026-09-21
- purge loop at dataErasure.js:691 and PURGE_FILES = CUSTOMER_DATA_FILES at :48, at aae041a | `git grep -n PURGE_FILES aae041a -- backend/dataErasure.js` | read 2026-09-21
- consumers of customerDataFiles at aae041a: dataErasure.js, dataExport.js, customer-data-lists-agree.test.js | `git grep -n "require(.*customerDataFiles" aae041a` | read 2026-09-21
- S59 WIP b587646 spreads CUSTOMER_DATA_FILES into jsonStorage.js | `git show b587646` (branch rd-404-441-sentinel-banner-s59) | read 2026-09-21
- no RD-525 or RD-575 branch; no commit for either except HISTORY docs fb2f64d; control: --grep RD-321 finds fbf3791 | `git branch -a --list` and `git log --all -i --grep` | read 2026-09-21
- lock usage and --maxWorkers=2 | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh header | read 2026-09-21
- Kam's resubmission quote | the NexusAI-D fresh seat brief, Tuesday mail of 2026-09-21T07:39:07Z, and the path map header | read 2026-09-21
Self-check note: read whole by Tuesday at 2026-09-21 19:38 AEST against Kam's rulings (C-126/C-127 delivered, none open for NexusAI), against itself (lane files, branch names, sequence, C-numbers consistent), and against the previous mails to this inbox (NexusAI-D keeps lane A; jsonStorage stays D's — matches the 09:3xZ answer to D)
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 19:38
