# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 12: THREE targets on portal main `609e967` (gate 11's five merged) — VSP-74 @ `a1794ad` (restore refuses an incomplete backup, TIER 1), VSP-75 @ `41c4a66` (the backup carries all 20 tables, TIER 1), VSP-69 @ `e79682a` (one transaction per reminder, TIER 1)

**First drafted for Tuesday on 2026-09-28 at 06:42-06:5x AEST; REFRESHED at 08:38-08:5x AEST by a read-only drafting agent after gate 11's
merges and the builder's round-2 READYs; RE-PINNED at 09:1x-09:2x AEST (third pass) to the pre-gate-12 FIX 1 / FIX 2 heads (r3 READYs).
Tuesday reviews, stamps and launches it.** Earlier versions are kept beside this file as `….md.pre-0928-refresh` (first draft) and
`….md.pre-0928-r3` (second pass, pinned `f62917f` / `69157de`); both are PROVENANCE only. 

**⚠ SEQUENCING — DONE, NOT OWED.** Gate 11 went **GO on all five** (QA/Vision-gate11, 07:54 AEST, report path in §PRIOR ROUND). The Vision seat
merged VSP-66, VSP-71, VSP-70, VSP-68 and VSP-73 to portal main in that order (main `0d992e0` → **`609e967`**; `1976275` fast-forwarded, then four
merge commits `dad64d2`, `8efb159`, `8720b34`, `609e967`). It then executed Tuesday's PHASE 2 rulings
(`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-28_vision_gate11_merge_and_gate12_prep.md`, read whole by the
drafter): **forward-merged `609e967` into VSP-74 (`987178c`), then VSP-74 into VSP-75 (`e34add4`, then three more merges of VSP-74's later
commits), and main into VSP-69 (`e79682a`)** — merges, never a rebase — and built round 2 on VSP-74 (holes (a) and (b)) and VSP-75 (the
injector, VSP68-G11-F1, the lazy tables). **All three branches are 0 behind main `609e967`.** No forward merge is owed. The heads below are
the ones the builder's r3 READYs name (VSP-74, VSP-75) and the r2 READY names (VSP-69, unchanged); the drafter re-read every one by
`ls-remote` (09:17:49 AEST). **Third pass:** the second-pass drafter's WRONG AT SOURCE items went to a Vision fix seat: **FIX 1** (VSP-74
`a1794ad`: a lacking table whose live copy is empty or missing is no longer kept) and **FIX 2** (VSP-75 `41c4a66`: `backup-lazy-absent.test.js`
derives its database from `TEST_DATABASE_URL` + `_lazy`). VSP-75 merged `a1794ad` forward (`2ed83fe`) and added FIX 1's cells (i)/(ii)
(`0d1376c`, new `test/db/restore-old-backup.test.js`). Tuesday RULED the second pass's item 4 (a clean dump of an empty database says OK:
correct as OK; a wrong database is out of scope; recorded on VSP-75, Jira comment 38536). The coupling question stays the gate's.

The builder's READY mails under test (on disk, each read whole by the drafter; **these REPLACE the earlier READYs as the claims under test**):
- VSP-74 (r3): `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp74-r3-READY-mail.txt` (dated 2026-09-27T23:16:48Z)
- VSP-75 (r3): `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp75-r3-READY-mail.txt` (dated 2026-09-27T23:16:49Z)
- VSP-69 (r2, no newer READY; head unchanged): `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp69-r2-READY-mail.txt` (dated 2026-09-27T22:37:06Z)
The VSP-74 and VSP-75 r2 READYs (`…-vsp74-r2-READY-mail.txt`, `…-vsp75-r2-READY-mail.txt`, heads `f62917f` / `69157de`) are PRIOR WORK: the
r3 READYs say "everything in 69157de's READY is kept" and "all of f62917f's cells pass" — both CLAIMS the gate re-derives.
The round-1 READYs (`…-vsp74-READY-mail.txt`, `…-vsp75-READY-mail.txt`, `…-vsp69-READY-mail.txt`, dated 20:23-20:37Z) are PRIOR WORK: their
cells are still on the branches and still claims, but the heads they name (`bf5bdc0`, `0d7a2fb`, `3ede8ed`) are now ancestors, not targets.
**Every builder statement below comes from those mails, the commit messages or the BACKLOG at each head. Each one is a CLAIM.** The three
r3 READYs landed one second apart (the r2s 26 seconds apart). Every red, every mutant and every suite set in this brief must be **RE-DERIVED by the
gate. None is taken from a READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch (main may have moved only to a descendant of `609e967` that touches none of the three targets' files: a NOTE, see §PIN). The
verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 09:26
Re-read by Tuesday's drafting subagent on commission; Tuesday reviews the WRONG list before launch.
Self-check note: tier 1 x3; round 1 per class; 74+75 merge back to back or not at all (the gate says whether that holds); the deploy-time old-backup list is the builder's inference and the gate MEASURES it; CI UNMEASURED; production untouched.

NODE20-LEG: DOCKER-PULL-NEVER
<!-- STAMPED by Tuesday's ruling (2026-09-28, stamp): as gate 11 — `docker image inspect node:20` then `docker run --rm --pull=never` of
     the image ALREADY present; nothing is ever pulled; if the image is absent the leg is NOT RUN and the report says so. (Was: Tuesday sets NOT-RUN or DOCKER-PULL-NEVER at stamp (gate 11 ran DOCKER-PULL-NEVER and proved node:20 present, sha256:8f693eaa…,
     linux/arm64, v20.20.2). The launcher refuses anything else (exit 45). The drafter did NOT run docker; re-prove the image (§N5.5). -->

GATE11-MERGED: 1976275635185db4551d5e3b015a66971f4563a5 5bdaeae6e28e280be380042a3dc8a56dbada0293 10ba4bbd29e34bf601426b68328f63725e228a86 7ef698d7e8c00c4c8e87060bec9f5284dfe8082a 6d7ea736b4f718cddd2e152f1ee0234d42d97bfe
<!-- The five gate-11 GO heads (VSP66, VSP71, VSP70, VSP68, VSP73), all ancestors of main 609e967 (READ 08:4x: merge parents of dad64d2,
     8efb159, 8720b34, 609e967 and 1976275 fast-forwarded). The launcher requires each to be an ancestor of MAIN-P (exit 9). -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build any of these changes and you owe the builder nothing. **Every line below that reports what the builder says
is a CLAIM, never evidence.**

**One gate, THREE targets, THREE verdicts (GO / NO-GO each, at its pinned sha), plus ONE merged-tree line.**
- **VSP74** at `a1794ad` — **TIER 1 (Tuesday's ruling; the builder self-graded "Tier 3" in round 1, "tier 1" in round 2).** Why: it is the
  DESTRUCTIVE restore path. Its job is to decide which live tables a restore empties or changes. A wrong answer is deleted production data.
  Both failure directions are in scope: a restore that still empties or changes a table it cannot put back (directly, by CASCADE, by SET NULL),
  AND a legitimate restore that is now refused or restores less than it should.
- **VSP75** at `41c4a66` — **TIER 1 (Tuesday's ruling).** Why: the data-loss path. The live nightly backup has never contained `quotes` or any
  other PRO table (READ at first draft: the 10-table list at `0d992e0` was unchanged since `96a5ff3`, 2026-04-18). It changes how EVERY table
  is read (`row_to_json`, PK order) and written back (JSON columns as text), and now also what the nightly alert says (empty-message errors,
  all-failed = FAILED with no upload, lazy tables absent). Both directions: a table still missing or not restored identically, or a failure
  announced OK; AND a table that used to back up and restore and now does not, or a healthy backup announced INCOMPLETE/FAILED.
- **VSP69** at `e79682a` — **TIER 1 (the builder and Tuesday agree).** Why: the client email path. It rewrites `dispatchDue()`, which sends
  reminder email to CUSTOMERS. Both directions: a reminder sent twice (the ticket), AND a reminder now never sent, sent late, out of order, or
  sent while another instance also sends it.
- **MERGED TREE:** main `609e967` + VSP75 (which CONTAINS VSP74) + VSP69, one line: which merges are clean, which conflict and where, the suites as
  sets on the merged tree, **the merged tree's local coverage (§COVERAGE RISK)**, and whether **MERGE COUPLING** holds (§MERGE COUPLING).

**⚠ Names, written out every time:**
- **VSP74 = Jira VSP-74 = "F-B"** (found by the builder while building VSP-68): a restore EMPTIED a live table whose dump had failed and put
  nothing back. Round 2 adds the drafter's holes (a) cascade and (b) lacking tables, both MEASURED REAL by the builder (READY) and closed by
  `restorePlan()`. **FIX 1 (r3):** a lacking table counts only when it EXISTS here AND HAS ROWS.
- **VSP75 = Jira VSP-75 = "F-A"**: the nightly backup named 10 tables; `quotes`, `quote_approvals`, `quote_sequences`, `pricing_config`,
  `tco_scenarios`, `reminders`, `notification_log`, `integration_settings`, `monday_sync` and `feedback_coordinator_state` were never in it.
  Round 2 also carries gate 11's **VSP68-G11-F1** (Major: an empty-message dump error announced OK) and **VSP68-G11-O1** (the `feedback` noise,
  ruled noise at gate 11's WRONG (n)). **r3:** VSP-74's FIX 1 merged forward, FIX 1's cells (i)/(ii) on the 20-table list, and **FIX 2** (the
  lazy suite's database follows `TEST_DATABASE_URL`).
- **VSP69 = Jira VSP-69 = gate 9's §N.4(h)** (Minor, pre-existing): the dispatcher sent a batch of up to 50 inside ONE transaction, so a failure
  after the first send rolled every sent reminder back to `pending` and the next tick sent them all again.

Branches: `fix/vsp-74-restore-refuses-incomplete-2026-09-28`, `fix/vsp-75-backup-all-tables-2026-09-28` (stacked on VSP-74: it contains
`a1794ad` through merge `2ed83fe`), `fix/vsp-69-dispatch-per-reminder-2026-09-28`. **None is on main.**

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole. **C-01..C-06. No C-entry covers VSP-69, VSP-74 or VSP-75** (first-draft READ 06:47; the launcher re-checks for a C-07 and
  for any mention of the three ids and prints a NOTE if either appears).
- **Kam's F-B ruling "(3) both"** (carried by Tuesday's PHASE 2, ruling 5): the restore refuses an incomplete backup AND never empties a table it
  cannot restore. Holes (a) and (b) are inside that ruling. **That is the one product ruling that is Kam's.**
- **PRODUCTION IS LIVE for this project.** `datasec-sales-portal-rg` holds the live site `https://datasec-sales-portal.azurewebsites.net`,
  its production Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault `datasec-sales-kv`. Production runs Node 20
  (`.github/workflows/test.yml`, blob `0cb2d05`, unchanged at every head). **The nightly backup (VSP-75) and the reminder dispatcher (VSP-69) run
  in production on a schedule; the restore CLI (VSP-74) is run against production by an operator.** **Nothing in this gate touches production**
  (§13, HELD). Kam's VSP-65 production deploy and VSP-67's `idle_in_transaction_session_timeout` wait for his typed word and his gh login: not
  this gate's business.
- **Tuesday's rulings are Tuesday's, not Kam's:** the three tiers; VSP-69 = option A (one transaction per reminder); PHASE 2 rulings 1-6 (forward
  merges; the injector must REALLY reach the dump, proven by a mutant; F1's fix shape "message || code || name || 'unknown error'", presence
  not truthiness, "a 0-row backup of a source that has rows is INCOMPLETE or FAILED"; lazy tables absent, any other missing table INCOMPLETE;
  measure-then-close holes (a)/(b); VSP-69 re-run after the forward merge).
- **The BUILDER's choices, each judged by the gate (say whether each needs Kam):** FIX 1's rule that "lacking", like "outside", counts only live tables that
  exist and HAVE rows (the fix of the second pass's WRONG (c); a builder's implementation of a drafter's finding, not a Kam ruling); the closure keeps parents on ANY foreign key including NO ACTION;
  VSP-75's all-failed = **FAILED with no upload** (the builder's pick inside Tuesday's "INCOMPLETE or FAILED"); the LAZY_TABLES list; the
  refusal text and flag name; the inclusion of `feedback_coordinator_state` and `integration_settings`; the exclusion of `session`; VSP-69's
  at-least-once design, its per-tick cap of 50, and ending the tick on the first failure.
- **Tuesday's ruling on the second pass's item 4 (Jira VSP-75 comment 38536):** every table dumping cleanly with 0 rows (an empty database) is
  correctly "DB Backup OK"; backing up the WRONG database is OUT OF SCOPE of VSP-75. The gate does not re-open it; it may note a measurement.
- **Deploys are HELD for Kam. Nothing merges on your word.** A merge is Tuesday's GO on a pinned head. A deploy is Kam's word.

## PRIOR ROUND
PRIOR ROUND: none of these three targets has been GATED before. Each is ROUND 1 of its class. The fleet's two-NO-GO cap applies PER CLASS:
a NO-GO here is the class's FIRST; a round 2 may follow on Tuesday's word; a NO-GO in round 2 sends that class to Kam. **The builder's "r2"
label is a BUILD round, not a gate round:** round 1 of the build was never gated (gate 12 was held behind gate 11), so no NO-GO has been
spent on any of the three classes.
**How the drafter established "round 1" (READ):** at first draft (06:44-06:46), zero matches for `VSP-?(69|74|75)` in the gate 9 briefs, the
gate 10 brief, and the gate 9 and gate 10 reports; the gate 11 brief named F-A / F-B only as OUT OF SCOPE. **Refresh (08:4x):** gate 11's
report carries **0** matches for `VSP-?(69|74|75)` and rules F-A and F-B "OUT OF SCOPE (ruled), not measured" (§N4); the Vision reports folder
holds no gate-12 report (gates 9, 10, 11 and QQ gates 1-8 only).
**ITS REPORT IS ON DISK AT:** gate 11 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets`
(`report.md`, read whole by the drafter at refresh: **read its VERDICTS, its §N3 (VSP-70, under VSP-74), its §N4 (VSP-68: the empty-message
finding VSP68-G11-F1 and its whole-database-unreachable cell, the WRONG (n) noise ruling), its N1.3 `dispatchDue()` real-caller cell (VSP-69's
neighbour), its N5.2 coverage table (merged 80.79%), its NOT TESTED, its self-findings, and its `evidence/tools/`**). The origin findings live in
gate 9 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge`
(`report.md`: §N.4(h), the dispatcher re-send) and gate 10 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2`
(`report.md`, `evidence/tools/`).
Origin findings, each a CLAIM until you measure it:
- **§N.4(h) → VSP-69.** Gate 9 MEASURED with recorders only: tick 1 sends, the UPDATE times out and rolls back, tick 2 re-sends; under a true
  black hole both MAIN and HEAD send twice once the zombie backend dies. Ruling: pre-existing at-least-once; Minor; ticketed.
- **F-B → VSP-74 and F-A → VSP-75:** found by the builder, not by a gate; gate 11 was told not to measure them. **Holes (a) and (b):** found by
  this brief's first draft reading the code, MEASURED by the builder on its own database (READY), never by a gate.
- **VSP68-G11-F1 and VSP68-G11-O1 → VSP-75:** MEASURED by gate 11 on real Postgres (§N4.2, §N4.3). Re-use gate 11's cells as the positive control.
- **Self-findings from gates 2-11 bind you:** quote every path (the project path has a space and a `!`); run every loop and every
  `git show <sha>:<path>` under **bash, not zsh** (zsh reads `$S:path` as a history modifier: the refresh drafter hit it AGAIN at 08:4x); never
  detach a control server; **the portal test-DB name MUST end in `_test`**; npm's update-notifier egresses unless you disable it; record the load
  average beside every timing number (**a latency result with no load figure is not a measurement**); count reuse by backend pid + pool
  counters, never bytes; a spawnSync launcher blinds your own observers; backend pids by `client_port` are null through Docker's NAT (use
  `client.processID` + `pg_stat_activity`); a harness that counts rows in a table that may not exist must tolerate its absence; **gate 11's:
  `NODE_OPTIONS` splits on the space in a preload path (URL-encode `--import`); a connect-watcher needs a positive control (gate 11's first was
  blind); a shell helper must not shadow a system binary (`tr`); an unquoted path variable silently builds no tree.**
- **PRIOR WORK: verify every claim against git history and gates 9-11's evidence, never against this brief.**
- **Instruments are REUSED BY COPY.** Prefer gate 11's `evidence/tools/` (newest: gate 10's arms plus `qa-g11-stallproxy.cjs` with FIN,
  `qa-g11-arms.cjs` (restore, backup68 arms), `qa-g11-v68-down.cjs` (the whole-DB-unreachable cell), `qa-g11-preload-netwatch.cjs`,
  `qa-g11-clusterlist.cjs`, `mutate-g11.py`, `run-node20-g11.sh`). If gate 11's tools are absent, copy gate 10's: `qa-g10-stallproxy.cjs`,
  `qa-harness-g10-vsp.cjs`, `qa-g10-lib.cjs`, `qa-mkdb.cjs`, `qa-dbcheck.cjs`, `qa-floorcount.py`, `qa-io1-preload-fetchguard.cjs`,
  `qa-run.py`, `run-suite.sh`, `mktree-portal.sh`, `lockcmp.py`, `lockwalk.py`, `specsets.py`, `tapsets.py`. **COPY what you use into this
  gate's own `evidence/tools/`, read it before you trust it, and RE-POINT every hard-coded path and prefix** (gate 11's copies ENFORCE
  `vsp_qa_g11_` and hard-code `work-g11`). **Never edit, run from, or write into gate 1-11's copies, evidence, trees or databases.** Record the
  sha1 of each copy before and after your edits. **Roles left by earlier gates (`vsp_qa_g10_*`, `vsp_qa_g11_boot`, `vsp_qa_g11_other`) are not
  yours: never use, alter or drop them.**

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head, base and a commit count, and no `@`; the head is a commit; the base is
an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin refs/heads/<branch>` equals the head
NOW; no target is on main. **All three targets must be FULLY forward-merged: base = `609e967`, 0 commits behind it.** **Their NON-merge commits
over `609e967` must be exactly the chains below** and every merge commit has exactly two parents, its second parent on main (or, for VSP75, on
VSP74). **Never rebased:** the round-1 READY heads (`bf5bdc0` in VSP74 and VSP75, `0d7a2fb` in VSP75, `3ede8ed` in VSP69) are ancestors of the
pinned heads, and VSP74's pinned head `a1794ad` is an ancestor of VSP75's. **Main:** origin main must be `609e967` or a DESCENDANT of it whose
diff from `609e967` touches none of the targets' files (NOTE, then the targets are stale-based and the gate re-derives the merge); anything
else refuses. **Gated anchors (the launcher checks them):** the five `GATE11-MERGED` shas and `12138cb` (VSP-70's refactor) are ancestors of main;
`0d992e0`'s single parent is `b5c3e8d`; main's `server/reminders/dispatcher.js` is still blob `283be27`.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | 609e967d6b03ff77dcbd692ee6e4434a5027e70b | - | - | IN |
| VSP74 | portal | fix/vsp-74-restore-refuses-incomplete-2026-09-28 | a1794ad5111b640fd3041e4f46154c577f559baf | 609e967d6b03ff77dcbd692ee6e4434a5027e70b | 8 | IN |
| VSP75 | portal | fix/vsp-75-backup-all-tables-2026-09-28 | 41c4a664a9d1698150424337ccc9d946d221f12b | 609e967d6b03ff77dcbd692ee6e4434a5027e70b | 20 | IN |
| VSP69 | portal | fix/vsp-69-dispatch-per-reminder-2026-09-28 | e79682a3ee9ada9602a08c59a2d4d3e132b9b638 | 609e967d6b03ff77dcbd692ee6e4434a5027e70b | 2 | IN |
<!-- PIN-HEADS:END -->

Every row above: `git -C <portal> ls-remote origin` read by the drafter at **2026-09-28 09:17:49 AEST**, equal to each READY's "New head
(ls-remote)"; main and VSP69 unchanged since 08:38:45; `cat-file -t` = commit for all four. Counts by `rev-list --count 609e967..<head>` (09:1x).

**The chains over `609e967` (READ 08:4x, `rev-list`, `log --format='%h %p %s'`):**
- **VSP74 (8 commits):** non-merge `d2531ea` (refactor) → `bf5bdc0` (round-1 fix) ; merge `987178c` (parents `bf5bdc0` + main `609e967`) ;
  `b7bc78b` (fix: `restorePlan`, `server/dbRestore.js` + `test/db/restore-incomplete.test.js`) → `011becb` (BACKLOG) → `57ecad6` (unit cells,
  `server/dbRestore.plan.test.js`) → `f62917f` (the outside-table cell uses a made-up table) → **`a1794ad` (FIX 1: fix + cells + BACKLOG, one
  commit; `BACKLOG.md`, `server/dbRestore.js`, `server/dbRestore.plan.test.js`, `test/db/restore-incomplete.test.js`)**.
- **VSP75 (20 commits):** VSP74's eight, plus non-merge `cad19ab` (refactor) → `0d7a2fb` (round-1 fix) ; merge `e34add4` (parents `0d7a2fb` +
  `987178c`) ; `e64d54e` (fix: injector, F1, lazy tables; 6 files) → `f392582` (BACKLOG) ; merges `d7a5e77` (+ `011becb`), `987afab` (+ `57ecad6`),
  `949b72e` (+ `f62917f`) ; `69157de` (absent plan cells, `server/dbRestore.plan.test.js` only) ; **merge `2ed83fe` (parents `69157de` +
  `a1794ad`; the READY: only the `restorePlan()` comment conflicted) ; `0d1376c` (FIX 1 cells, new `test/db/restore-old-backup.test.js` only) ;
  `41c4a66` (FIX 2: `test/db/backup-lazy-absent.test.js` + `BACKLOG.md`)**.
- **VSP69 (2 commits):** non-merge `3ede8ed` (the round-1 fix, parent `0d992e0`) ; merge `e79682a` (parents `3ede8ed` + main `609e967`).

Repo: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`). **The portal has no CLAUDE.md inside the repo;** its rules are
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (read it; its deploy commands are NOT for you).

**The shape at the third pass (READ 09:1x at the pinned heads; re-derive it):**
- **VSP74 over `609e967`, 4 files:** `BACKLOG.md`, `server/dbRestore.js` (`5f4b71d` → `236f8ce`, 289 lines), `server/dbRestore.plan.test.js`
  (new, `24a4dd3`, **7** `test(`), `test/db/restore-incomplete.test.js` (new, `da1d223`, **12** `test(`). At `a1794ad`: `failedTables()` `:112`
  (presence test), `NOT_RESTORED = ['session']` `:120`, **`restorePlan()` `:133-160`** (`hasRows` `:137`; **lacking `:138-141` = RESTORE_ORDER
  tables the backup has no entry for that EXIST here (`live.includes(t)`) AND HAVE ROWS (FIX 1)**; outside `:142-145`; closure; return `:160`),
  `clearTables(data, db, keep)` `:164` (the `!failed.has(t)` skip `:175`), `parseArgs()` `:194`, `restoreData()` `:248` (refusal `:258`, the
  `--allow-incomplete` warning `:261`, the insert loop's keep-skip `:267`). `RESTORE_ORDER` is still the OLD 10-table list (`:25`).
- **VSP75 over `609e967`, 10 files:** `BACKLOG.md`, `server/backupTables.js` (new, `ad03428`: 20 tables, `BACKUP_EXCLUDED = {session}`,
  `LAZY_TABLES = {feedback, feedback_coordinator_state}`), `server/dbBackup.js` (`5e31eb4` → `0b38895`, UNCHANGED since `69157de`; `dumpTable()`
  `:36-60` with the lazy branch `:49-52` and F1's `const error = err.message || err.code || err.name || 'unknown error';` `:56`; presence `:69`,
  `:81`; `absent_tables` `:83`; all-failed → throw `:160-163`), `server/dbBackup.test.js` (`4fb902e` → `12a6e24`, **5 → 10 `test(`**, unchanged
  since `69157de`), `server/dbRestore.js` (→ `2ee8090`, 299 lines: `RESTORE_ORDER` from the shared list, `NOT_RESTORED` from `BACKUP_EXCLUDED`
  `:114`, `restorePlan()` `:136-169` with FIX 1's lacking `:141-144` and `absentWithRows` on the shared `hasRows` `:140`, absent kept after the
  closure), `server/dbRestore.plan.test.js` (`9b8a2e3`, **9** `test(`), `test/db/backup-coverage.test.js` (`5ffb1fe`, 6 `test(`),
  `test/db/backup-lazy-absent.test.js` (**`5f507e6`**, 3 `test(`; FIX 2 `:18-23`, `:35-36`), `test/db/restore-incomplete.test.js` (`da1d223`, SAME
  blob as VSP74), **`test/db/restore-old-backup.test.js` (new, `586d558`, 2 `test(`: FIX 1 (i) `:53`, (ii) `:69`)**.
- **VSP69 over `609e967`, 3 files:** `BACKLOG.md`, `server/reminders/dispatcher.js` (`283be27` → `7a67be9`, the SAME blob as at `3ede8ed`),
  `test/db/dispatch-once.test.js` (`c3b0d92`, 5 `test(`, same as `3ede8ed`). What changed under it: `server/db.js` (`0d402a0` → `5d42db6`,
  VSP-66's `guard()`), `server/schema.sql`, `server/initDb.js`.
- **Same blob at `609e967` and ALL THREE heads:** `package.json` (`d3b76fb`), `package-lock.json` (`9d426df`), `.github/workflows/test.yml`
  (`0cb2d05`), `test/db/helpers.js` (`1d90638`), `scripts/run-db-tests.js` (`c48966c`), `server/initDb.js` (`68fc8cc`), `server/schema.sql`
  (`74f6e9c`), `server/db.js` (`5d42db6`), `test/db/concurrency.test.js` (`0d2fc8d`), `server/dbRestore.test.js` (VSP-70's, `8315d41`),
  `server/routes/feedback.js` (`eac73d0`), `server/feedbackDigest.js` (`1d21a1b`). **VSP-69 and VSP-74/75 share no file but `BACKLOG.md`.**
**A GO is a statement about the pinned SHA only.** If a head moves, that target's verdict expires.

## MERGE COUPLING — VSP-74 and VSP-75 merge back to back, or not at all (the builder's claim; the gate says whether it holds)
**The claim (VSP-74 READY):** "Consequence on this branch ALONE: any database with quote rows makes every restore INCOMPLETE, because the
10-table list cannot bring quotes back … If gate 12 merges 74 without 75, the restore needs --allow-incomplete until 75 lands."
**The drafter's READ at `f62917f`, re-checked at `a1794ad` (stronger than the READY; FIX 1 does not change it — FIX 1 narrows "lacking", and
on VSP74 alone the PRO tables are "outside", not "lacking"):** `RESTORE_ORDER` at VSP74 is the old 10 tables, and `restorePlan()` marks
**"outside" = every live public table except `session` that is not in `RESTORE_ORDER` and HAS ROWS** (`:142-145` at `a1794ad`). Main's `schema.sql` creates
all the PRO tables at boot. So on VSP74 alone, a row in ANY of `quotes`, `quote_approvals`, `quote_sequences`, `pricing_config`,
`tco_scenarios`, `reminders`, `notification_log`, `integration_settings`, `monday_sync` or `feedback_coordinator_state` makes every restore
INCOMPLETE — not only quote rows. And every backup main's VSP-68 code writes on a database without `feedback` carries a failed `feedback`
entry, which VSP74 alone also refuses (VSP-75's lazy rule is what closes that). Production has quotes (PRO has been live since 2026-07-02), so
on VSP74 alone **every production restore is refused by default** and with `--allow-incomplete` the closure keeps `users`, `leads` and
`partner_orgs` (every PRO table points at one of them). **Tuesday keeps this as the gate's question (second pass's item 2).**
**What the gate decides, MEASURED:** on a VSP74-only tree, a production-shaped DB (quotes present) + a backup built by main's `buildBackup()`:
refused? with the flag, which tables are kept and what is restored? Then the same on the VSP75 tree with VSP75's backup. **Say in the merged-tree
line whether "74 and 75 merge back to back or not at all" holds**, and note the mechanics: VSP75 CONTAINS VSP74 (`a1794ad` via `2ed83fe`), so
merging VSP75's head brings VSP74 with it; the only unsafe order is VSP74 ALONE on main.

## COVERAGE RISK — the 80% CI line gate, thin margin on every head (the builder's numbers; the gate measures the MERGED three-way tree)
The READYs' local figures (CI's coverage command, local Node 26.8.1): **VSP74 lines 80.40%** (r3; r2 said 80.36%, 79.47% before its unit
cells), **VSP75 80.72%** (r3; r2 said 80.68%), **VSP69 80.59%** (r2). Gate 11 measured main's future merged tree at **80.79%** (its N5.2). The three branches add code to
`server/dbRestore.js`, `server/dbBackup.js` and `server/reminders/dispatcher.js`; `dbRestore.js` enters the unit denominator at ~36% (gate 11:
"its CLI body is not unit-covered"). **The gate MEASURES the coverage of the merged three-way tree (main + VSP75 + VSP69) locally**, plus each
head and main, same machine, same session; report lines AND branches (branches gate 70%). **CI is UNMEASURED (no gh login): the local figure
stands in for CI's Node 22 gate and is NOT CI.** A merged figure under 80.00% is a blocking finding for the merge queue (not a NO-GO of any one
target on its own), stated with the per-file lines that moved.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READYs — found by the drafters (verify each; all are claims)
- **(a) VSP-74's `restorePlan()` reads the plan OUTSIDE the clear transaction (READ; rule it).** `restorePlan()` queries through the pool
  (`db = { query }`, `:133` at `a1794ad`), then `clearTables()` opens its own client and `BEGIN` (`:164` ff.). The r3 VSP-74 READY now lists this window under NOT TESTED. A row written between the two (VSP-69's
  dispatcher inserting `notification_log`, a user creating feedback, a lazy table being created) is not in the plan. On the VSP75 tree every
  such table is in `RESTORE_ORDER`, so the window matters most for "absent + empty" lazy tables and for VSP74 alone. Measure once (a writer
  between plan and clear), or rule it unreachable for an operator-run CLI, and say which.
- **(b) VSP-74 READY: "Chain: … f62917f cell made branch-independent" vs its own "Unit: dbRestore.plan.test.js 5 cells" — consistent (READ).**
  But the VSP-75 READY's chain line "987afab / 949b72e merge VSP-74's unit cells" is loose: `987afab` merges `57ecad6` (the unit cells) and
  `949b72e` merges `f62917f` (the outside-table cell). Harmless wording; the chain is as §PIN says.
- **(c) RESOLVED BY FIX 1 (was: "lacking" ignored the live table's rows).** VSP-74 `a1794ad` counts a lacking table only when it exists here
  and has rows; VSP-75 `41c4a66` carries it (merge `2ed83fe`) and adds `test/db/restore-old-backup.test.js` cells (i)/(ii). The builder's own
  measurement at `69157de` confirmed the second pass's reading (lacking = all 10, keep = those + leads, users, partner_orgs, refused). **Now
  under test as FIX 1's FAIL conditions (§N1, §N2.9), including the READY's deploy-time list (§N2.9), which is an INFERENCE from the test DB's
  FK catalog, not a measurement on production data.** Residual (READ): once quotes-linked tables have rows — which production almost
  certainly has — an old backup still restores without `users`, `leads` and `partner_orgs`: that is Kam's F-B "(3) both" working as ruled,
  but it IS the disaster-recovery window after deploy; the gate measures it and says whether it needs Kam's eyes.
- **(d) The closure goes child → parent only, on `conrelid <> confrelid` (READ; measure).** Self-FKs (`quotes.revised_from_id`) are skipped,
  correctly for keeping. A kept PARENT whose CHILD is restored: the child's rows that point at parent rows the live table lacks fail `23503`
  one by one, swallowed, CLI "Restore complete." rc 0 (first draft's §2a row, still open). Count the silently lost rows per candidate.
- **(e) VSP-75's drift cell still has blind spots (READ at `69157de`; measure with mutants).** `tablesInCode()` (`backup-coverage.test.js:28-40`)
  walks `server/` only and matches only `/CREATE TABLE IF NOT EXISTS\s+"?(\w+)"?\s*\(/`. A plain `CREATE TABLE x (`, a schema-qualified
  `public.x`, a `CREATE TABLE … AS`, or code under `scripts/` is invisible. The new LAZY_TABLES pin cell (`:77`) uses the same census.
- **(f) RULED BY TUESDAY (Jira VSP-75 comment 38536):** every table dumping cleanly with 0 rows (an empty database) is correctly "DB Backup OK";
  a WRONG database is out of scope. The builder's all-failed = FAILED rule (`dbBackup.js:161`) stands as the builder's choice; the gate still
  measures 19 failed + 1 empty (INCOMPLETE upload) and says what it saw, without re-opening the empty-database ruling.
- **(g) VSP-75's M3b "truthiness back" SURVIVES and is called equivalent (READ: plausibly true; decide it).** With `error = message || code ||
  name || 'unknown error'`, `error` can be empty only if `'unknown error'` were empty, so `if (dump.error)` and `'error' in dump` agree for every
  error `dumpTable()` produces. **But** the restore side's presence test (`failedTables()`, `:112` ff. at `a1794ad`) is load-bearing for OLD backups written by
  main's code with `error: ""` — the VSP-74 cell for that exists (`restore-incomplete.test.js`, the "error: \"\"" cell; line numbers moved at `a1794ad`). Confirm M3b is equivalent on the backup side
  only, and that the restore-side truthiness mutant (VSP-74's "truthiness back") reddens.
- **(h) VSP-75's lazy rule keys on `err.code === '42P01'` (READ).** The code 42P01 comes from the PK lookup's `$1::regclass`. A lazy table in a
  different schema on `search_path`, or a permission error (42501) on an existing lazy table, is NOT absent (correct: INCOMPLETE). Measure the
  42501 shape once.
- **(i) VSP-74 hole (b) "on this branch alone it then failed on an unrelated NO ACTION key (quotes -> users)" (READY; measure at `987178c`).**
- **(j) VSP-69: the builder's out-of-scope note** — "the dispatcher's catch does ROLLBACK then release() with no error. After a FAILED rollback the
  client goes back to the pool: the VSP-76 / VSP-70 class." **Recorded as OUT OF SCOPE for VSP-69 unless the gate measures a live consequence**
  (a dead or poisoned client handed to the next caller after a failed ROLLBACK in `dispatchDue()`, e.g. a black-holed ROLLBACK at the shrunk
  bound on the merged tree). If measured, it is a finding against the READY's scope, graded like gate 11's VSP66-G11-F1 (a finding, not a
  NO-GO of VSP-69), unless it re-sends a committed reminder (then §N3's FAIL condition governs).
- **(k) VSP-69's M2 argument (carried from first draft; the gate decides M2 itself).** The READY: M2 (`FOR UPDATE` without `SKIP LOCKED`) survives
  "as the READY argued". A second instance WAITING on the row lock is a query under `DB_QUERY_TIMEOUT_MS` (30 s shipped) that holds a pool slot
  for the whole of the first instance's send; if the send outlasts the bound, the waiter times out and ends its tick. No builder cell measures it
  (sends slowed 30 ms).
- **(l) VSP-69 poison reminder, cutoff precision, VSP-66 interaction (carried; measure):** a send that THROWS blocks every later-due reminder every
  tick (predicted pre-existing); `cutoff` is a JS Date (ms) against `TIMESTAMPTZ` (µs); gate 11's `dispatchDue()` kill cell ran the OLD
  dispatcher, VSP-69 makes up to 50 checkouts per tick through VSP-66's `guard()` (now under it at `e79682a`).
- **(m) The VSP-69 test sets a dummy ACS connection string itself** (`dispatch-once.test.js`, `endpoint=https://vsp69.invalid/`) and replaces
  `@azure/communication-email` through `require.cache`. Prove the stub was in place (no DNS or socket for `vsp69.invalid`).
- **(n) VSP-75's `integration_settings` "no secrets live here: see settingsStore.js" — UNVERIFIED by both drafters.** READ `server/settingsStore.js`
  and MEASURE (§N2.6). **(p) of the first draft (the VSP-75 STATUS mail):** still not on disk; `backupTables.js` now carries a one-line reason for
  `feedback_coordinator_state` ("empty would re-send everything"); `integration_settings` has only the comment above. Treat other reasons as unstated.
- **(o) The session exclusion and restored user ids (carried; measure once at `609e967` and VSP75):** a stale session of a user created after the
  backup may authenticate as the NEXT user created after a restore resets `users_id_seq`.
- **(p) The READY red-proofs ran on the builder's `salesportal_test`,** the builder's own database, which the Vision seat (pid `38185`, pane
  `%37`, EXITED by the stamp at 09:25) used. Never use it (§13.2).
- **(q) Merge prediction: UNMEASURED by the drafter** (it may not run `merge-tree --write-tree` outside its own objdir, and did not). READ only:
  VSP75 and VSP69 both touch `BACKLOG.md`; no code file is shared. Predicted: VSP75 × main and VSP69 × main fast-forward (0 behind);
  **VSP75 × VSP69 CONFLICT in `BACKLOG.md` only.** The gate derives every merge in its own object dir.
- **(r) Round-1 READY cells are still claims:** VSP-74's original 5 cells now use a completed fixture (`complete()`, "what each cell asserts is
  unchanged" — READY); VSP-68's 5 dbBackup cells now fail `quotes` with a real 42P01 instead of `feedback` (READY). Diff each and rule "unchanged".
- **(s) UNVERIFIABLE by design, and you must not try:** production's catalog and FK actions, production's lazy tables, whether production's DB host
  resolves to two addresses, the size of a full production backup, real Azure Blob Storage, real ACS, real ntfy, a real App Service restart or a
  second real instance. **Carry each as NOT TESTED.**
- **(t) RESOLVED BY FIX 2 (was: `backup-lazy-absent.test.js` always used `salesportal_test_lazy`).** At `41c4a66` (`:18-23`) the database is
  `TEST_DATABASE_URL`'s name + `_lazy` (default `salesportal_test_lazy` only when `TEST_DATABASE_URL` is unset), the name checked
  `^[a-z0-9_]+$`, created if missing (`:35-36`), never dropped. **The gate runs the lazy suite against ITS OWN database through
  `TEST_DATABASE_URL`: with `vsp_qa_g12_<epoch>_test` the file uses `vsp_qa_g12_<epoch>_test_lazy` (ends `_lazy`, not `_test`: it is the file's
  own scratch DB, never TRUNCATEd by the runner; list it and leave it).** The checked-edit fallback of the second pass is NO LONGER NEEDED —
  unless the gate's own measurement (§N2.10) shows the file still reaching `salesportal_test_lazy`, in which case STOP running it, apply the
  fallback (one asserted edit to a `vsp_qa_g12_*` name) and report FIX 2 as a FAIL of VSP75.
- **Verified TRUE at source (READ 08:38-08:5x):** all four heads by `ls-remote` (08:38:45) = the READYs' heads = Tuesday's reading; the chains
  and merge parents in §PIN; the file sets and blobs above; `test(` counts 10/5 (VSP74), 10/7/6/3/10 (VSP75), 5 (VSP69); (third pass) `test(` counts 12/7 (VSP74 `a1794ad`), 12/9/6/3/10/2 (VSP75 `41c4a66`); the dbBackup cells' five
  VSP-68 names kept verbatim at `69157de` and `41c4a66` (`:80`, `:89`, `:97`, `:109`, `:120`) plus five new; the LAZY_TABLES line cites
  (`routes/feedback.js:25` and `:331`, `feedbackDigest.js:30`) are the `CREATE TABLE IF NOT EXISTS` lines inside `ensureTable()` (`:20`),
  `ensureStateTable()` (`:330`) and `ensureFeedbackTable()`; no boot-time `INSERT` into any PRO table in `server/` (git grep, 0 hits); `:5433`
  is listening (Docker); gate 11's `evidence/tools/` is on disk.

## THE READYs — their FIX, CELLS, RED-PROOFS, PRIOR WORK and NOT TESTED (the gate rules on every claim)
The READYs under test are on disk (paths at the top: VSP-74 r3, VSP-75 r3, VSP-69 r2); read each whole. Their NOT TESTED lines are carried VERBATIM here (the launcher checks it):

VSP-74 NOT TESTED
NOT TESTED: real Azure blob download (restoreData driven directly); the CLI end to end; production's catalog (FK edges read from the initDb test DB); a table gaining rows between restorePlan and clearTables (plan is read outside the clear's transaction, same as the outside group already was); Node 20; e2e:pro; CI UNMEASURED (Kam's gh login).

VSP-75 NOT TESTED
NOT TESTED: real Azure blob download/upload; the CLI end to end; production's catalog and row counts (the deploy-time list above is from the test DB's FK edges); a real pre-VSP-75 backup blob (cells build the old format from the live DB); CI's Postgres user needing CREATEDB for <name>_lazy (it needed it for salesportal_test_lazy already); Node 20; e2e:pro; CI UNMEASURED (Kam's gh login).
(VSP-75's r2 NOT TESTED, still carried as a claim of work not done: a real dual-address refusal (the AggregateError is constructed, shaped as Node's); the nightly cron in a running server.)

VSP-69 NOT TESTED
NOT TESTED: a real ACS send; a real process death mid-tick; connection churn under load; Node 20; CI UNMEASURED.

**The READYs' claims, in one line each (each a CLAIM, re-derived in §N):**
- **VSP-74 @ `a1794ad` (r3, FIX 1):** MEASURED first on the builder's own DB `vsp_m_fix1_0915` at `69157de`: an old 10-table backup into a DB
  whose 10 new tables were empty → lacking = all 10, keep = those + leads, users, partner_orgs, refused. Fix: a lacking table counts only when it
  exists here AND has rows (the same `hasRows` as outside); empty or missing → neither refused nor kept; with rows → refused, flag keeps it +
  its FK parents (unchanged). **Cells (red at `f62917f`, green at `a1794ad`):** plan — lacking `email_log` WITH rows is incomplete and keeps
  email_log, leads, email_templates, users, partner_orgs; lacking `email_log` EMPTY is not incomplete; lacking `feedback` that does not exist
  here is not incomplete; restore-incomplete — lacking `meetings` with live meetings EMPTY restores the rest with no flag; lacking `meetings`
  with rows is refused ("not in the backup: meetings") and the flag keeps meetings and leads exactly (already green: pins the right half).
  **Assertion CHANGED (the READY says so):** the old plan cell "a table of the restore list that the backup lacks is incomplete" used an empty
  catalog; it now seeds `email_log` rows and asserts the closure. **Mutants (2, both red):** M1 lacking ignores rows (2 cells red); M2 lacking
  ignores whether the table exists here (11 red: a query on a missing table throws). **Also changed:** `complete()` in
  `restore-incomplete.test.js` skipped a lazy table that does not exist (the file failed ALONE on a fresh DB, 5 of 12 red); "every db file now
  passes run alone on a fresh DB". Suites vs `609e967` (each file alone, fresh DB): unit 121 (+7), db 105 (+12), 0 lost; runner 105/105.
  Coverage lines 80.40%. PRIOR WORK: failed dumps refused/kept whatever their live rows; outside, closure, clearTables/VSP-70 unchanged.
- **VSP-75 @ `41c4a66` (r3, FIX 1 merged forward + FIX 2):** merge `2ed83fe` (only the `restorePlan()` comment conflicted; the absent loop
  now uses the shared `hasRows()`). **FIX 1 cells, `test/db/restore-old-backup.test.js` (red on `69157de`: INCOMPLETE naming all 10 new tables +
  feedback on a fresh DB):** (i) an old 10-table backup into a DB whose other 10 tables are empty, then the live DB changed (lead renamed, lead
  added, partner org renamed, collateral added): restore with no flag, every one of the backup's tables equals the backup's rows exactly; (ii) the
  same once `quotes` has a row: refused, naming quotes and NOT the empty lacking tables; with the flag it keeps EXACTLY quotes, leads,
  partner_orgs, users (read from the restore's own warnings), all four byte-equal, the other tables restored (meetings, emptied live, comes
  back). **Deploy-time list (the READY's, "from the FK catalog (initDb test DB)"; the gate MEASURES it, §N2.9):** which of an OLD backup's 10
  tables it cannot restore — once any of `quotes`, `quote_approvals`, `reminders`, `tco_scenarios`, `monday_sync` has rows: `partner_orgs`,
  `users`, `leads`; once only `pricing_config`, `notification_log` or `integration_settings` has rows: `partner_orgs`, `users`; `quote_sequences`
  alone: none; every other old table (meetings, collateral_items, lead_collateral_provided, email_templates, email_log, feedback,
  partner_org_requests) restored. "Inference, not measured: production almost certainly has quote rows." **FIX 2:** lazy-suite DB =
  `TEST_DATABASE_URL`'s name + `_lazy`; proof on local PG 16.15 by `pg_stat_database`: the OLD file with `TEST_DATABASE_URL=…/vsp_fix2_proof_test`
  wrote `salesportal_test_lazy` (xact_commit 2650 → 2912); the NEW file left it unchanged and used `vsp_fix2_proof_test_lazy`; a whole `test:db`
  on `…/vsp_fix12_75full_test`: `salesportal_test_lazy` sessions 76 → 76, xact_commit +2 "background (autovacuum)" (an idle control DB drifted
  the same); no env: 76 → 83. Suites vs `609e967` (each file alone, fresh DB): unit 128 (+14), db 116 (+23), 0 lost; 0 lost vs `a1794ad`; runner
  116/116 twice. Coverage lines 80.72%. PRIOR WORK: "everything in 69157de's READY is kept … all its cells pass".
- **VSP-74 @ `f62917f` (r2, PRIOR WORK — its cells must still pass at `a1794ad`):** ruling 1 forward merge `987178c`, BACKLOG-only conflict, own cells 5/5 after. Ruling 5 MEASURED at `987178c` before any
  fix: (a) REAL — `--allow-incomplete` with `meetings` failed, clearing `leads` emptied meetings 1 → 0; catalog: leads CASCADEs into `email_log`,
  `lead_collateral_provided`, `meetings`, `monday_sync`, `reminders`, SET NULL on `quotes`, `tco_scenarios`; quotes CASCADEs into
  `quote_approvals`, `reminders`. (b) REAL — a backup lacking a table the DB has was NOT refused. Fix: `restorePlan()` (failed / lacking /
  outside-with-rows), refused by default naming each group; with the flag kept plus every FK parent to a fixed point; the insert loop skips
  kept tables; `error: ""` refused. Red cells: hole (a); hole (b) ×3; `error: ""`. Unit: 5 plan cells on a scripted catalog. **Mutants (7, all
  red):** no closure; clearTables ignores keep; no lacking; no outside; no refusal; truthiness back; insert loop ignores keep. Suites vs
  `609e967`: unit 119 (+5), db 103 (+10), 0 lost, 0 dupes. Coverage lines 80.36%.
- **VSP-75 @ `69157de` (r2, PRIOR WORK — its cells must still pass at `41c4a66`):** ruling 1 `e34add4` clean, own cells then dbBackup {1,3,4} RED (cell 1: 40 !== 20). Ruling 2: the stub names the table
  as `dumpTable()` does, returns realistic rows, counts every thrown fault, every fault cell asserts `reached(<table>)`; **M1 (the old unquoted
  matcher) reddens all 7 fault cells; product mutant M2 (the catch drops `error`) reddens 6.** Ruling 3 (F1): `new Error('')` on leads →
  INCOMPLETE naming "leads (Error)"; `AggregateError('')` code ECONNREFUSED on every table → FAILED, 0 uploads, body carries ECONNREFUSED.
  Ruling 4: lazy `feedback` and `feedback_coordinator_state` 42P01 → absent (alert OK); `monday_sync` missing → INCOMPLETE; `feedback` timeout
  → INCOMPLETE; `backup-lazy-absent.test.js` on real Postgres in its own DB `salesportal_test_lazy` (created if missing, reused, nothing dropped).
  Restore side: absent + empty/missing in target = left alone; absent + rows = incomplete. **Mutants: backup side 9, 8 red, M3b survives
  (equivalent); restore side 4, all red.** Suites vs `609e967`: unit 126 (+12), db 112 (+19), 0 lost. Coverage lines 80.68%.
- **VSP-69 @ `e79682a`:** merge only (BACKLOG conflict), no code change; dispatch-once 5/5 ×3; **M1 → {2}; M3 → {4}; M4 → {1,2,3}; M5 → {3}; M2
  survives** — "identical to 3ede8ed". Suites: unit 114, db 98 (+5), 0 lost. Coverage lines 80.59%.
- **Round-1 claims still on the branches (PRIOR WORK, first draft §THE READYs):** VSP-74 at `d2531ea` failing {2,3,4,5}; VSP-75 at `cad19ab`
  failing {1,5}, M1-M5; VSP-69 at `0d992e0` failing {2} (R1:2, R2:2), M1/M3/M4/M5 red, M2 survives.
- **`salesportal_test_lazy` — RESOLVED BY FIX 2 (WRONG (t)).** At `41c4a66` the lazy suite's database follows `TEST_DATABASE_URL`; the gate's
  `vsp_qa_g12_<epoch>_test` gives `vsp_qa_g12_<epoch>_test_lazy`. The gate PROVES it did not touch the builder's `salesportal_test_lazy` (§N2.10).

**How you treat these:** every NOT TESTED line you CAN test locally, you test: the CLI's refusal path end to end with a recorder in place of
Azure (never `AZURE_BACKUP_CONN_STR`); a restore under load and a link death mid-restore (gate 11's arms); a real dual-address refusal
(`localhost` → `::1` + `127.0.0.1`, gate 11 §N4.3's probe) against the VSP75 tree; the nightly cron's `runBackup()` path through recorders;
VSP-69's process death and churn; Node 20 for all three. Azure, ACS, ntfy and production's catalog you carry into your own NOT TESTED.

## 2a. LEGITIMATE SHAPES — two targets are DESTRUCTIVE-path or client-send checkers, so a false refusal or a false send is damage (template §2a)
Measure every row. **A row whose expected verdict and clause disagree is a finding against this brief. Say so.**
**The destructive path's standing rule (template §2a): until the rows below are measured, the instruction on ANY unexpected result in a
restore cell is STOP and record it, never a remedy.** Every restore in this gate runs against a database YOU created and seeded.

| shape — its ordinary form, as the portal really produces it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| VSP75 tree: restore a COMPLETE 20-table backup (VSP75's `buildBackup()`) onto a populated production-shaped DB | not refused; every table replaced; row sets identical | `incomplete` empty | builder control cells — **measure** |
| VSP75 tree: the same, both lazy tables absent in the backup AND absent/empty in the target | not refused; lazy tables left alone, not created | absent + empty = left alone | builder (lazy-absent cell 2) — **measure** |
| VSP75 tree: absent in the backup, target `feedback` HAS rows | refused by default naming it; with the flag its rows and its FK parents (`users`) kept | `absentWithRows` + closure | builder — **measure; count what is kept** |
| any tree: one FAILED table, no flag | refused before any change; message names it and `--allow-incomplete`; every table's rows, xmins and sequences unchanged | `restoreData()` refusal | builder — **measure** |
| VSP75 tree, `--allow-incomplete`, failed table is a CASCADE CHILD (`meetings`, `email_log`, `reminders`, `monday_sync`, `lead_collateral_provided`, `quote_approvals`) | its rows kept; its parents kept by the closure | closure to a fixed point | builder (hole (a) cell: meetings) — **measure EVERY one; a lost row is a FAIL** |
| VSP75 tree, flag, failed `quotes` / `tco_scenarios` (SET NULL from leads) | rows and `lead_id` unchanged; `leads`, `users` kept | closure | builder — **measure** |
| VSP75 tree, flag, failed PARENT (`leads`) | leads kept; children restored; child rows pointing at leads the live table lacks | predicted `23503` per row, swallowed, rc 0 | WRONG (d) — **count the lost rows** |
| VSP75 tree: today's real backup SHAPE (10 tables, built by `609e967`'s `buildBackup()` on YOUR DB), the 10 new tables EMPTY | **not refused, no flag; every one of the backup's 10 tables equals the backup's rows** | FIX 1: lacking counts only tables that exist here with rows | FIX 1 (i) — **measure; a refusal or a mismatch is a FAIL** |
| the same, once `quotes` has a row | refused, naming quotes and NOT the empty lacking tables; flag keeps EXACTLY quotes, leads, partner_orgs, users, byte-equal; the other 7 restored | FIX 1 + closure | FIX 1 (ii) — **measure** |
| the same, once ONLY `pricing_config` (or `notification_log`, `integration_settings`) has rows / ONLY `quote_sequences` | kept: partner_orgs + users / none of the 10 | closure over the FK catalog | the READY's deploy-time list (INFERENCE) — **measure every trigger table, §N2.9** |
| VSP74 ALONE: a backup from main's code on a DB with ANY PRO row | refused ("outside"); with the flag PRO tables + parents kept | outside-with-rows | MERGE COUPLING — **measure** |
| VSP75: the nightly backup of an ordinary production-shaped DB (every route used once, both lazy tables created) | 20 tables, `failed_tables: []`, `absent_tables: []`, "DB Backup OK" | shared list | builder — **real `runBackup()` + recorders** |
| VSP75: a fresh DB, neither lazy table created | `absent_tables` both, `failed_tables: []`, "DB Backup OK" (gate 11's noise GONE) | lazy 42P01 | builder — **measure; gate 11 shape A is the positive control at `609e967` (INCOMPLETE)** |
| VSP75: any OTHER table missing (drop `monday_sync` in YOUR DB) | INCOMPLETE naming it | non-lazy 42P01 | builder — **measure** |
| VSP75: whole DB unreachable through a dual-address host | "DB Backup FAILED", nothing uploaded, body names `ECONNREFUSED` | all failed → throw | builder — **measure with gate 11's real probe, not a constructed AggregateError** |
| VSP75: one table's dump rejects `new Error('')` | INCOMPLETE naming `<t> (Error)` | F1 fallback chain | builder — **measure on real pg (gate 11's wrapper)** |
| VSP75: round trip over a POPULATED DB vs a TRUNCATEd one | row_to_json sets identical in both | clear then insert | **measure both** |
| VSP69: an ordinary tick, 5 due client reminders, one instance | 5 sends in due order, each once, each marked sent | per-reminder transaction | builder cell 1 |
| VSP69: two instances tick at once, realistic send latency | each reminder sent once; neither waits on the other | SKIP LOCKED | builder cell 4 at 30 ms — **measure at 30 ms and past the shrunk bound** |
| VSP69: a reminder whose send THROWS | predicted: every later-due reminder blocked every tick (pre-existing) | stop on failure + due order | WRONG (l) — **measure at `609e967` and `e79682a`** |
| VSP69: 55 due reminders | 50 in tick 1 (most overdue first), 5 in tick 2 | cap 50 | builder cell 3 |

## N1. TARGET VSP74 — the restore refuses an incomplete backup and never empties or changes a table it cannot put back (TIER 1)
**FAIL condition, stated BEFORE the runs:** any restore cell in which a table the plan must keep (failed, lacking, outside-with-rows, or
absent-with-rows) loses or changes a row — by a direct DELETE, a CASCADE, a SET NULL, or the insert loop — whether or not the flag is set; a
REFUSED restore that changed anything (row sets, xmins, sequence values, `n_tup_del`); `restorePlan()` failing to name a table that is
failed, lacking, or outside-with-rows; the closure failing to keep a parent whose clearing would CASCADE into, SET NULL, or NO-ACTION-block a
kept table; an old backup whose failed entry carries `error: ""` NOT refused; a COMPLETE backup refused, or restoring fewer rows than at
`609e967`; **FIX 1: a lacking table whose live copy is EMPTY or MISSING being refused, kept, or causing any parent to be kept (a restore that
should run clean with no flag is refused or restores less); a lacking table WITH rows NOT refused, or with the flag not kept together with its
FK parents; a failed-dump table no longer refused/kept because its live copy is empty (FIX 1 must touch only the lacking group);** VSP-70's first-error behaviour or `release(broken)` changed (`server/dbRestore.test.js` 4/4); the CLI's usage, `AZURE_BACKUP_CONN_STR
not set.` line or exit codes changed; a NAME lost vs `609e967`. **Any of the seven READY mutants that stays green is a FAIL of the cell set,
not a note. The same holds for FIX 1's two mutants (M1 lacking ignores rows; M2 lacking ignores whether the table exists here).**
1. **The builder's cells, RED re-derived at `987178c`** (the forward-merged pre-fix commit; copy `test/db/restore-incomplete.test.js` `da1d223`
   and `server/dbRestore.plan.test.js` `24a4dd3` hash-verified; the r2 blobs `cf2f35f` / `8a305d8` for the r2 claims). Predicted: the five round-2 restore cells red (hole (a), hole (b) ×3, `error: ""`);
   the plan unit file fails to LOAD (no `restorePlan` export) — **a load failure is a trivial red: say so, and prove each plan cell reddens on a
   mutant instead**. The five round-1 cells: at `987178c` 5/5 (they were green at `bf5bdc0`). At `609e967` + the test files: round-1 cells
   {2,3,4,5} red (first draft's prediction at `d2531ea`, re-derived on the new main). **FIX 1's cells red at `f62917f`** (plan: the three lacking cells;
   restore-incomplete: the empty-meetings cell red, the meetings-with-rows cell GREEN there as the READY says — prove both). **The CHANGED
   assertion:** diff the old plan cell "a table of the restore list that the backup lacks is incomplete" (`8a305d8` → `24a4dd3`) and rule it a
   correct re-statement under FIX 1, not a weakening. **`complete()`'s change:** run `restore-incomplete.test.js` ALONE on a fresh DB with the OLD
   `complete()` (the READY reports 5 of 12 red, "relation feedback does not exist", for its pre-fix copy; the r2 file `cf2f35f` has 10 cells — say
   which file you ran and what you saw) and at `a1794ad` (12/12). At `a1794ad`: 12/12 and 7/7, N ≥ 3.
2. **The nine mutants, re-derived** (fresh tree per arm, asserted edits, `node --check` rc quoted; **a red from a mutant that does not parse is
   VOID**): FIX 1's M1 (lacking ignores rows: predicted 2 red) and M2 (lacking ignores existence: predicted 11 red, "a query on a missing
   table throws" — say whether that red is a product red or a crash-red); then the r2 seven: no closure; `clearTables` ignores keep; no lacking; no outside; no refusal; truthiness back (`failedTables()`); insert loop ignores
   keep. Quote which cell reddens each and why. **Plus M8 (yours):** closure on CASCADE/SET NULL only (NO ACTION parents dropped) — predicted:
   the clear fails `23503` and rolls back (safe) rather than losing rows; say which cell sees it, or none.
3. **THE CASCADE MATRIX (MEASURED; the headline of hole (a)).** On YOUR seeded production-shaped database (all 20 tables with rows, FK links
   populated), build the backup JSON with the REAL `buildBackup()` of the VSP75 tree, mark ONE table failed (`metadata.failed_tables` + its
   entry's `error`, VSP-68's shape), run `restoreData(data, {allowIncomplete: true})` under `env -i`. **One row per candidate failed table:**
   `meetings`, `email_log`, `reminders`, `monday_sync`, `lead_collateral_provided`, `quote_approvals`, `quotes`, `tco_scenarios`, `leads`, `users`,
   `collateral_items`, `email_templates`. Per row: the kept set the plan printed, and every table's row count + row checksum before and after.
   **A single lost or changed row in any KEPT table is the FAIL. Quote it.** Also the same at `987178c` (positive control: the cascade loses
   rows) — **the matrix must come out DIFFERENTLY at `987178c` and `a1794ad`, or it is not measuring.**
4. **Holes (b), lacking and outside (MEASURED).** (i) A backup lacking `reminders` on a DB that has reminders: refused; with the flag reminders
   untouched and still pointing where they did. (ii) Lacking `meetings` (IN the list): refused, meetings survive. (iii) Today's 10-table shape
   on the VSP75 tree, PRO tables empty and populated (FIX 1; full matrix in §N2.9). (iv) An outside table with 0 rows vs 1 row (a `qa_outside_g12` table you create
   in YOUR DB). (v) At `987178c`, the READY's "on this branch alone it then failed on an unrelated NO ACTION key (quotes -> users)". Quote the
   refusal text for each.
5. **A backup PRODUCED by the real code (MEASURED; the first draft's (n)).** On the VSP75 tree: the real `runBackup()` with `@azure/storage-blob`
   replaced by YOUR recorder through `require.cache` and ntfy to YOUR loopback recorder (gate 11 §N4.2's method), one table made to fail for
   real (dropped in YOUR database, or gate 9's black hole on its dump query), then the RECORDED blob gunzipped and passed to `restoreData()`.
   Expected: refused naming the table; with the flag that table and its parents untouched.
6. **The refusal changes nothing (MEASURED):** `xmin` and row md5 of every table, `last_value` of every sequence, `pg_stat_user_tables.n_tup_del`
   deltas on YOUR DB, before and after each refused call.
7. **`parseArgs` and the CLI (MEASURED):** `[latest]`, `[latest, --allow-incomplete]`, `[--allow-incomplete, x]`, `[]`, `[--allow-incomplete]`
   alone (predicted: the listing path, stops at `AZURE_BACKUP_CONN_STR not set.` rc 1), and the typo `--allow-incomplet`.
8. **VSP-70 intact (MEASURED):** gate 11's VSP-70 real-Postgres masking cell (copied) passes unchanged on `a1794ad` and the merged tree.
9. **WRONG (a) and (d):** the plan/clear window, once; the silently lost child rows under a kept parent, counted.

## N2. TARGET VSP75 — the backup carries all 20 tables except session, in FK order; failures are never announced OK (TIER 1)
**FAIL condition, stated BEFORE the runs:** any table the code creates (by YOUR census, not the builder's regex) missing from the backup and not
in `BACKUP_EXCLUDED`; any FK whose parent comes after its child in `RESTORE_ORDER`; a round trip (TRUNCATEd OR populated target) whose
`row_to_json` set differs from the source on any table, or whose next id is not max + 1 on any serial table with rows; **the fault injector NOT
reaching the dump in any fault cell of `server/dbBackup.test.js`** (M1 must redden all 7 fault cells; if any fault cell stays green on M1, the
cell is papered over: FAIL); **VSP68-G11-F1 not closed:** an empty-message dump error recorded as a dumped table or announced OK, or a whole
database unreachable announced anything but FAILED; **a lazy table's absence announced INCOMPLETE** (gate 11's noise back), or **any NON-lazy
missing table announced OK/absent**, or a lazy table that EXISTS but fails announced OK/absent; the restore side creating or emptying an absent
lazy table, or clearing one that HAS rows without the flag; a secret in the backup; a NAME lost vs `609e967`; **FIX 1 on the 20-table list:
cell (i) or (ii) of `test/db/restore-old-backup.test.js` not reproduced on YOUR instrument, or the READY's deploy-time list contradicted by
YOUR measurement (§N2.9) without the READY's list being corrected in your report (a contradicted list is a FAIL: it is the text Kam will read
at deploy); FIX 2: ANY connection or transaction by the gate's runs in `salesportal_test_lazy` (by `pg_stat_database` / `pg_stat_activity`,
§N2.10), or ANY write to any builder database, or the lazy suite using any database other than `<your TEST_DATABASE_URL name>_lazy` — per
Tuesday's stamp ruling a measured write to `salesportal_test_lazy` or a builder database is a FAIL of VSP-75 and the gate STOPS that arm.**
1. **Red re-derived at `e34add4`** (the merge before the round-2 fix): VSP-68's dbBackup cells {1,3,4} red (the READY's "40 !== 20" and the
   silent injector). Then copy the round-2 `dbBackup.test.js` (`12a6e24`) onto `e34add4`: the five new cells red for the product reasons (F1,
   lazy), not load errors. **FIX 1 cells (i)/(ii) red at `69157de`** (READY: INCOMPLETE naming all 10 new tables + feedback). At `41c4a66`: dbBackup
   10, `backup-coverage` 6, `backup-lazy-absent` 3, `dbRestore.plan` 9, `restore-incomplete` 12, `restore-old-backup` 2, N ≥ 3.
2. **The injector really reaches the dump (MEASURED; Tuesday's ruling 2).** Re-derive the builder's **M1** (the old unquoted matcher in the stub:
   all 7 fault cells red) and product **M2** (the catch drops `error`: 6 red — name the one that stays green and why). **Independently of the
   builder's `hits` counter:** in YOUR copy of the test, log the SQL text of every query the stub throws on, and show each thrown fault is on
   the query that reads the table's rows or its PK lookup (never on some other query that happens to name the table). Positive control: the
   pre-fix stub (`4fb902e`) on `41c4a66` reddens {1,3,4}.
3. **F1 closed (MEASURED on real Postgres, not only the stub).** (i) gate 11's `new Error('')` wrapper on `meetings`: INCOMPLETE, the reason never
   blank (quote it). (ii) gate 11's whole-database-unreachable cell (`qa-g11-v68-down.cjs`: `localhost` resolving to `::1` + `127.0.0.1`, a
   refused port): "DB Backup FAILED", 0 uploads, body carries `ECONNREFUSED` — at `609e967` the same cell must say "DB Backup OK" (positive
   control). (iii) 19 failed + 1 empty (INCOMPLETE upload expected). The empty-database-says-OK case is RULED by Tuesday (WRONG (f)): do not
   re-open it. **Judge FAILED + no upload** (the builder's choice) against INCOMPLETE + upload: which serves an operator after a real outage,
   and does it need Kam?
4. **Lazy tables (MEASURED).** READ the code lines (`server/routes/feedback.js:20-25` `ensureTable()`, `:330-331` `ensureStateTable()`,
   `server/feedbackDigest.js` `ensureFeedbackTable()` `:30`) and grep YOUR census for any OTHER lazily created table (a third one missed by
   `LAZY_TABLES` is a FAIL). Cells: fresh DB (both absent: OK, `absent_tables` both); `monday_sync` dropped (INCOMPLETE); `feedback` existing but its
   dump black-holed (INCOMPLETE); `feedback` existing but its PK lookup 42501 (WRONG (h): INCOMPLETE). **The restore side of absent:** a backup with
   both absent restored into (i) a DB without them (not created, not refused), (ii) a DB where `feedback` HAS rows (refused by default; with the flag
   kept and `users` kept), (iii) where it exists EMPTY (left alone, not refused). Also `backup-lazy-absent.test.js`'s DB name (§THE READYs).
5. **YOUR OWN table census and FK check (MEASURED).** Boot the VSP75 tree's `initDb()` on a fresh `vsp_qa_g12_*` DB, drive every lazy route, read
   `pg_class` (relkind `r`, schema `public`) and every FK from `pg_constraint` (self included) against `RESTORE_ORDER`. Drift mutants M6
   (`CREATE TABLE qa_drift_g12 (id int)` in a server file) and M7 (`CREATE TABLE IF NOT EXISTS public.qa_drift_g12 (`): predicted SURVIVE
   (WRONG (e)).
6. **The round trip, twice (MEASURED).** Seed every table (a quote revision chain, JSONB objects, a top-level JSON array in
   `tco_scenarios.results`, a JSON column holding a bare string, NULL JSON, microsecond timestamps, unicode, a very long text). (i) TRUNCATEd target;
   (ii) POPULATED target (rows added, deleted, ids beyond the backup's). Compare per-table `row_to_json` sets and checksums; `nextval` = max + 1.
7. **Secrets (READ + MEASURED; WRONG (n)).** READ `server/settingsStore.js` and every writer of `integration_settings`, `pricing_config`,
   `notification_log`, `feedback_coordinator_state`; exercise each settings write route with dummy values; dump each table's `row_to_json`; list
   every key. **Any token, key, password or connection string is a FAIL** (quote the key NAME only).
8. **Size and time (MEASURED):** a scaled DB (say the numbers), `buildBackup()` elapsed, peak RSS, JSON and gzip bytes, at `609e967` and VSP75, load
   quoted. **Carry production's real size as NOT TESTED.**
9. **Old backups and FIX 1's deploy-time list (MEASURED).** A backup built by `609e967`'s `buildBackup()` (10 tables, VSP-68's `failed_tables`)
   of YOUR seeded DB, restored on the `41c4a66` tree into a DB whose 10 new tables are (a) all EMPTY: no flag, not refused, all 10 tables equal the
   backup (FIX 1 (i), including a live DB changed after the backup); then **one arm per trigger table**, each starting from (a) with rows put in
   exactly ONE of `quotes`, `quote_approvals`, `reminders`, `tco_scenarios`, `monday_sync`, `pricing_config`, `notification_log`,
   `integration_settings`, `quote_sequences`, `feedback_coordinator_state` (plus the rows its FKs need — say which you added, since an FK parent
   row can itself be the trigger): record the refusal text, then the flagged run's kept set (from the restore's own warning lines AND from
   row checksums before/after) and the restored set. **Compare with the READY's list line by line:** quotes/quote_approvals/reminders/
   tco_scenarios/monday_sync → partner_orgs, users, leads; pricing_config/notification_log/integration_settings → partner_orgs, users;
   quote_sequences → none. `feedback_coordinator_state` is not in the READY's list: measure what it keeps. Then count, in the flagged runs, the
   restored child rows lost to `23503` because they point at a lead or user the live DB lacks (the READY's "inference, not measured"). **This
   table is what Kam reads at deploy: every line MEASURED, or NOT RUN with the reason.**
10. **FIX 2 — the lazy suite stays on YOUR database (MEASURED).** Before and after each `test:db` run and each run of
   `backup-lazy-absent.test.js` alone at `41c4a66`, read `pg_stat_database` (`xact_commit`, `numbackends`) for `salesportal_test_lazy`, for YOUR
   `<name>_test_lazy`, and for one idle control DB of yours; and poll `pg_stat_activity` for any backend on `salesportal_test_lazy` during the run.
   **Pass:** 0 backends on `salesportal_test_lazy` at every poll, its `xact_commit` drift no larger than the idle control's; YOUR `_lazy` DB
   created and used. **Positive control:** the SAME instrument, with the r2 file (`1640754`, from `69157de`) copied into a tree of yours and
   pointed at a THROWAWAY copy — **never run the r2 file against the cluster as-is** (it would write `salesportal_test_lazy`); instead apply one
   asserted edit replacing its literal `salesportal_test_lazy` with `vsp_qa_g12_<epoch>_ctl_lazy`, and show your instrument SEES that database
   written (backends > 0, xact_commit rises). If the instrument cannot see the control, the FIX 2 measurement is VOID. Also READ the default:
   with `TEST_DATABASE_URL` unset the file falls back to `salesportal_test` → `salesportal_test_lazy` — never run it unset.
11. **The session exclusion (WRONG (o)), once** at `609e967` and VSP75.

## N3. TARGET VSP69 — one transaction per reminder, on the forward-merged head (TIER 1)
**FAIL condition, stated BEFORE the runs:** any reminder already sent and COMMITTED being sent again after a failure; any due reminder never
sent where `609e967` sent it (a silent miss); two instances sending one reminder; a tick that does not take the 50 most overdue; due order
changed; notification_log rows disagreeing with the sends; a send to a real provider; any of the builder's M1, M3, M4, M5 staying green on
`e79682a`; a NAME lost vs `609e967`. **One re-send of the reminder IN FLIGHT at the failure is the design (at-least-once), not a FAIL; name it.**
**Real sends are OFF.** `@azure/communication-email` is replaced by YOUR recorder (through `require.cache`, before any portal module loads);
ntfy goes to YOUR loopback recorder; fetch is stubbed to throw on any other URL.
1. **The five cells, RED re-derived at `609e967`** (the new main + `dispatch-once.test.js` `c3b0d92`, hash-verified): predicted failing {2}
   (R1:2, R2:2). At `e79682a`: 5/5, N ≥ 3. **The builder's mutants M1, M3, M4, M5 on the FORWARD-MERGED head** (not on `3ede8ed`): predicted
   {2}, {4}, {1,2,3}, {3}. Fresh tree per arm, asserted edits, `node --check` rc quoted.
2. **M2 — DECIDE it yourself (MEASURED; WRONG (k)).** Build M2 (`FOR UPDATE` without `SKIP LOCKED`) on `e79682a`. Two instances over 10 due
   reminders, recorder slowed to (i) 30 ms, (ii) HALF the shrunk bound, (iii) LONGER than the shrunk bound (`DB_QUERY_TIMEOUT_MS=1500`, send
   2,500 ms). Per arm, at `e79682a` and M2: sends per reminder, each instance's tick outcome, `[reminders] dispatch failed:` lines, pool counters,
   time spent waiting (async `pg_locks` observer every 250 ms), and whether the waiter took the NEXT row or none after the holder committed.
   **RULE:** is `SKIP LOCKED` load-bearing for correctness under the query bound, or only for throughput? If any arm reddens M2, the builder's
   "survives, as argued" is wrong: name the cell the product test should add.
3. **Gate 9's §N.4(h) arms, re-run (MEASURED):** the builder's model (UPDATE rejected) and a TRUE black hole on the UPDATE of reminder 3 of 5.
   **Count sends per reminder per tick; exactly one re-send (R3) is the design.**
4. **A real process death mid-tick (MEASURED; the READY's NOT TESTED):** a CHILD running `dispatchDue()` on 10 due reminders, recorder slowed,
   `SIGKILL` after send K; a fresh child ticks. Expected: 1..K-1 never again; K at most once more; the rest once. N ≥ 5 at `e79682a`, once at
   `609e967` (positive control: the batch re-sent).
5. **VSP-69 × VSP-66 on the forward-merged head (MEASURED):** a `pg_terminate_backend` during send K (gate 11 N1.3's real-caller method); the
   dead client never handed out again; listener count on the idle client after 1,000 ticks' checkouts; connection churn under load (50 due per
   tick with signed-in traffic in the same process; checkouts, pool peaks, pool-wait, request p50/p99, load quoted) at `609e967` and `e79682a`.
6. **The builder's out-of-scope note (WRONG (j)) — measure once:** a black-holed ROLLBACK in the dispatcher's catch at the shrunk bound on
   `e79682a`: is the client released with no error and handed to the next caller, and does that caller fail? **Out of scope for VSP-69 unless a
   live consequence is measured**; if one is, report it as a finding (the VSP-70/VSP-76 class) with the cell, not as a NO-GO of VSP-69, unless a
   committed reminder is re-sent.
7. **The poison reminder, order and cutoff (WRONG (l)):** at `609e967` and `e79682a`; READ `server/email/index.js` `sendEmail()` for inputs that
   throw.
8. **The existing dispatch cells:** `concurrency.test.js`'s dispatch cell and `reminder-push.test.js` at `e79682a` and on the merged tree, N ≥ 3,
   through `scripts/run-db-tests.js` (serialised).

## N4. THE SEMANTIC CONFLICT, CLOSED NOT PAPERED OVER — REQUIRED CELL (Tuesday's requirement, now testable on the pinned head)
The VSP-68 × VSP-75 conflict (VSP-68's stub matched ` <table> ` unquoted; VSP-75 quotes the name, so the injected failure never fired and cells
1, 3, 4 went red on the merged tree) was fixed ON THE VSP-75 BRANCH in `e64d54e`. **On `41c4a66` (which IS main + VSP74 + VSP75), ALL of these
must pass, and each must be shown able to fail:**
1. **All ten `server/dbBackup.test.js` cells pass (N ≥ 3) AND every injected failure LANDS ON THE DUMP QUERY** — §N2.2's independent SQL log.
   **Positive control:** VSP-68's pre-fix stub (`4fb902e`) on `41c4a66` reddens {1,3,4}. **Mutants:** the builder's M1 (7 fault cells red) and
   M2 (6 red), re-derived; if either count differs, quote the difference.
2. **Diff the stub fix** (`4fb902e` → `12a6e24`) and quote it. Is any assertion weakened? The READY says VSP-68's cell 1 now asserts
   `TABLES_TO_BACKUP.length * 2` plus "no fault injected", and cell 4 fails `quotes` instead of `feedback` "assertions unchanged". **A weakened
   assertion (a cell deleted, a `total_rows` loosened to "> 0", a `notEqual` removed, a fault cell that no longer asserts the alert text) is a FAIL
   of VSP75.** The five VSP-68 cell names must be present verbatim (READ: they are, `:80-126`).
3. **VSP-75's round-trip and FK-order cells pass** (`backup-coverage.test.js`, N ≥ 3) with VSP-68's `failed_tables` AND VSP-75's `absent_tables` in
   the metadata (quote both from cell 5's backup).

## N5. SHARED — held results, suites, coverage, Node 20, CI
1. **Gate 11's HELD results on the merged tree, briefly** (one run each vs gate 11's report): VSP-70's real masking cell; VSP-68's real INCOMPLETE
   cell shape B (black-holed `leads`; shape A is now the lazy-absent OK by ruling — say so); VSP-66's terminate cell under a held client; gate
   10's S1 ticket cell at the shrunk bound. "Same" or quote the difference, with load.
2. **SUITES AS SETS, NOT COUNTS, same machine, same session (MEASURED).** In fresh archived trees of `609e967`, each of the three heads,
   `987178c`, `e34add4`, and the merged three-way tree: `npm test` and `npm run test:db` (each `test:db` on a FRESHLY CREATED
   `vsp_qa_g12_<epoch>_test`, proven fresh: zero user tables). Extract every NAME with its outcome (`specsets.py` / `tapsets.py`) and report vs
   `609e967`: names passing at main that do not pass at the head (**must be empty**); names added (READY predictions: VSP74 unit +7, db +12; VSP75
   unit +14, db +23; VSP69 db +5; merged unit +14, db +28); names removed (expect 0); duplicates. Each new test file N ≥ 3 at its head, load quoted.
3. **Coverage (§COVERAGE RISK):** CI's coverage command locally (`node --test --experimental-test-coverage --test-coverage-lines=80
   --test-coverage-branches=70 $(find server -name '*.test.js')`) at `609e967`, each head and the merged tree; lines and branches; the per-file
   lines for `dbRestore.js`, `dbBackup.js`, `backupTables.js`, `reminders/dispatcher.js`. **Label it: local Node standing in for CI's Node 22; not CI.**
4. **Product-test hygiene:** after each `test:db` run, list every `vsp71_%` role, every `vsp71_%` / `vsp73_%` database, `salesportal_test_lazy` (the builder's:
   must show no activity from you, §N2.10) and YOUR `*_test_lazy` databases in the cluster. Tuesday's gate-11 ruling carries over (§TUESDAY'S RULINGS).
5. **NODE 20 LEG (production's major) — per the NODE20-LEG line at the top.** If DOCKER-PULL-NEVER: exactly ONE docker verb family is sanctioned,
   for this leg only: `docker image inspect node:20` (prove the image is ALREADY present, quote its digest; if absent, the leg is NOT RUN —
   **never pull**) and `docker run --rm --pull=never` of that image, with YOUR archived tree mounted **WRITABLE**, an explicit `-e` allowlist
   (§13.3; never `--env-file`), `NODE_ENV=test`, and the database URL pointing at YOUR `_test` database via `host.docker.internal:5433`. Name every
   container `qa-g12-node20-<epoch>`. **Never `docker start/stop/exec/rm/compose` on any container, never `vsp-dev-db`, never `--network host`.**
   Run in it: `node --version` (quote), `npm test` and `test:db` on the MERGED tree, §N1.3's cascade matrix (one CASCADE child, one SET-NULL),
   §N2.3 (ii) the dual-address cell, §N2.6 (ii), §N3.2 (iii). Reap each container in a `finally`. If NOT-RUN: say so and carry Node 20 as NOT TESTED.
6. **CI IS UNMEASURED.** This project's `gh` is not authenticated, and **you must not use `gh` at all**. CI on all three branches is
   **UNMEASURED**, including its **Node 22 coverage gate** and its **`e2e:pro` step against a server booted by the portal's entry point**. Never
   claim CI. Name them as the first things to read at merge.

## 12. The merge and the queue
**The drafter did NOT run `merge-tree`**: every merge result below is **UNMEASURED — the gate derives it in its own copy.** READ-only
predictions: VSP74 × `609e967`, VSP75 × `609e967`, VSP69 × `609e967` are fast-forwards (0 behind; the launcher enforces it); VSP75 × VSP74 is a
fast-forward (VSP75 contains VSP74); **VSP75 × VSP69: CONFLICT in `BACKLOG.md` only** (no shared code file).
**Measure it yourself:** from YOUR own object dir (`GIT_OBJECT_DIRECTORY=<your own mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects
git -C <repo> merge-tree --write-tree --name-only <a> <b>`, or SKIP it and say so): VSP74 × main, VSP75 × main, VSP69 × main, VSP75 × VSP69.
Then build the MERGED TREE in YOUR own tree only (VSP75's tree + VSP-69's code delta; BACKLOG resolved by keeping both blocks): **prove its
code files equal "`609e967` + each target's own blobs"** (`dispatcher.js` = `7a67be9`; `dbRestore.js` `2ee8090`, `dbBackup.js` `0b38895`,
`backupTables.js` `ad03428`, `dbBackup.test.js` `12a6e24` = VSP75's). That tree is **the merged tree** for §N4, §N5 and the merged-tree line.
**MERGE COUPLING (§MERGE COUPLING):** state whether "VSP-74 and VSP-75 merge back to back or not at all" holds, from YOUR VSP74-alone
measurement, and the merge ORDER you recommend (VSP75's head carries VSP74; VSP69 independent).
**Semantic interactions on the merged tree (MEASURED where marked):** VSP74 × VSP68 (a real produced backup, §N1.5); VSP75 × VSP68 (§N4);
VSP75 × VSP74 (the cascade matrix on a 20-table backup, §N1.3; absent × plan, §N2.4); VSP69 × VSP66 (§N3.5); VSP69 × VSP75 (a restore while a tick
runs: what the dispatcher does when `reminders` is cleared under it; and the plan/clear window of WRONG (a) with the dispatcher writing
`notification_log`).
**Cells to re-run on the merged head at merge** (name at least these): `npm test` + `test:db` as sets; each new test file N ≥ 3; §N4's required
cell; the cascade matrix; §N2.3 (ii); §N3.2 and §N3.4; the merged coverage figure; CI's Node 20 and Node 22 legs including the coverage gate and
`e2e:pro`. **After Kam's deploy (not yours to read):** the first nightly backup's alert (OK with `absent_tables`, or INCOMPLETE) and its table
count (20); the first reminder tick's `notification_log`; and **that no restore is attempted from a pre-deploy 10-table backup without reading
§N2.9's deploy-time table first.**

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)**, or any port another seat
   holds. **Never `127.0.0.1:49162`, `:49164` or `:49166`** (a local Logitech plugin answers 501 there). Take every port from the kernel and
   bind `127.0.0.1` wherever YOUR harness, proxy or recorder listens. **Never start the portal's own entry point** (it binds `0.0.0.0` in
   `main()`); use the real `createApp()` and `initDb()` inside your harness only.
2. **Postgres = the local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all** (the one exception is
   §N5.5, under its NODE20-LEG line). Create `vsp_qa_g12_<epoch>` for app runs and `vsp_qa_g12_<epoch>_test` as `TEST_DATABASE_URL` for
   `test:db` (it TRUNCATEs; the name MUST end in `_test`). **Never** `salesportal`, `salesportal_test` (the builder's; the Vision seat `38185` had
   exited at stamp, but a Vision seat may be relaunched at any time), `salesportal_test_lazy` (the builder's; at `41c4a66` the lazy suite derives `<your test db>_lazy` from `TEST_DATABASE_URL` —
   FIX 2 — so ALWAYS set `TEST_DATABASE_URL` and prove it per §N2.10), any `vsp_qa_g1_*` … `vsp_qa_g11_*` database, the builder's
   `vsp_bf1_*`, or any `vsp71_*` / `vsp73_*` database you did not cause. `server/db.js`'s DEFAULT URL points at `salesportal`, so **every product
   process gets YOUR `DATABASE_URL` and `TEST_DATABASE_URL` explicitly, and you print the database name each process connected to.** Local
   defaults for credentials only; never anything from `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the runtime legs are
   **NOT RUN, blocker named**. Leave your databases in place and list their names (no DROP). **Serialise or salt creation.** **ROLES ARE
   CLUSTER-GLOBAL:** create a role only inside a transaction you roll back, or name it `vsp_qa_g12_*`, list it, and never grant it anything
   outside your own databases. **Every restore in this gate runs only against a `vsp_qa_g12_*` database you created; `restoreData()`,
   `restorePlan()` and `clearTables()` read and DELETE, so print the connected database name BEFORE each call and abort if it is not yours.**
   Never `ALTER SYSTEM`, never `ALTER DATABASE` on a database you did not create, never change server settings. Session-level `SET` only on your
   own connections. Release every lock and direct session in a `finally` and prove `pg_locks` is clean for your databases at the end.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test` or
   `development`, never `production`; PORT; a fresh random SESSION_SECRET / `COORDINATOR_SECRET` you generate; DATABASE_URL / TEST_DATABASE_URL =
   yours; DB_QUERY_TIMEOUT_MS / DB_CONNECT_TIMEOUT_MS only where an arm sets them, and say so; `NTFY_SERVER=http://ntfy.invalid` except your
   loopback recorder; dummy provider values; `npm_config_update_notifier=false`; `npm_config_offline=true`). **NEVER set in a product
   process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`, any real `ACS_*` / `MAIL_SENDER`, `AZURE_BACKUP_CONN_STR`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. (The product's own
   `dispatch-once.test.js` sets a DUMMY `ACS_EMAIL_CONNECTION_STRING` to `vsp69.invalid` inside its own process: WRONG (m).) Print each product
   process's env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh**: set `NTFY_SERVER` before any portal module is
   required and stub `fetch` to throw on any other URL (gate 10's `qa-io1-preload-fetchguard.cjs`, amended to allow ONLY your own loopback
   recorder). The reminder dispatcher, the email sender and the backup notifier run ONLY against recorders you wrote.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): `basename(argv[0]) == node` AND an
   app entry point ANYWHERE in the remaining argv, from the kernel; **"ours" = the ancestor chain CONTAINS your claude pid.** **Negative
   controls, same run, must classify FOREIGN:** at refresh (08:40 AEST) the live claudes were Tuesday `59108` (pane `%0`), **the Vision builder
   `38185` (pane `%37`, LIVE on the same Postgres)**, NexusAI `20317` (`%22`), `9959` (`%21`), `62649` (`%19`), the NexusAI batch-5b QA gate `91381`
   (`%36`), QA gates `36118` (`%23`) and `38362` (`%29`), and `84139` (not in tmux). **Gate 11's seat `40404` and `18655` had exited.** **RE-READ AT STAMP (09:25:31 AEST, `ps -axo` + `tmux list-panes -a`; load 19.56 / 17.45 /
   16.93): live claudes Tuesday `59108` (`%0`), NexusAI P `20317` (`%22`), NexusAI O `38362` (`%29`), NexusAI M `62649` (`%19`), NexusAI N `9959`
   (`%21`), QA/NexusAI-batch5b `91381` (`%36`), and `84139` (not in tmux). EXITED since the refresh: the Vision builder `38185` (`%37`) and the QA
   gate `36118` (`%23`). No Vision seat is live.** The launcher's negative controls: `59108`, `20317`, `91381`. **Re-read the
   seat list at start**; say which have exited. Never count by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. **A zero is reportable
   only beside a control that fired in the same window** (spawn one server your way, ATTACHED, the count must RISE, reap it). **Record the
   1-minute load beside every timing number** (it was 18.05 at 08:40 with `hw.ncpu` 8).
5. **THE DEADLINE RULE:** every step has a written DEADLINE and a client timeout on every request (no `timeout` binary here — build deadlines
   into your runner); a step past its deadline is ABORTED and reported (a hung product request IS a finding). Deadlines: boot 60 s; `initDb()`
   alone 60 s; DB connect 15 s; any request at the SHRUNK bound 20 s; **any request at the SHIPPED bounds 120 s**; a child-process fault cell
   30 s; one restore cell 120 s; the scaled backup 300 s; the M2 arms 180 s each; one `test:db` file 180 s; a whole `test:db` run
   420 s. **Nothing above 420 s.** State each shipped-bound exception where you use it. **Every server, proxy, recorder, direct session, lock,
   child and container you start is released in a `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every
   2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**

**Reap everything you start.** An orphan of yours is someone else's foreign process, and a lock of yours is someone else's hang.

### Drivable surface — LOCAL ONLY. **NEVER the live portal.**
- **NEVER the live** portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the live
  site, its Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault). **No request, no DB connection, not even a GET or a
  health probe. No `az` of any kind — no reads, no writes, no app-setting change, no deploy.** **Never ntfy.sh**, never Azure Blob Storage (the
  backup and restore cells use recorders), never ACS, never `api.agentmail.to` from a product process, never the Feedback_System coordinator,
  never the npm registry (`npm audit` included). **Never open a real backup, a production dump or any file under
  `Vision_Sales_Portal/4_Credentials/`.** Every backup JSON in this gate is built by the product's own code from YOUR seeded database.

### HELD
- No merge, no deploy, no registry, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker` (except §N5.5, only under its NODE20-LEG line), no `npm install`, no `npm ci` without
  `--offline --ignore-scripts`, no `npm audit`, and no `npx` of anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR`
  and `GH_CONFIG_DIR` at EMPTY directories.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g12/>`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never touch `work/` or `work-g2/` … `work-g11/`.**
  Dependencies: **`npm ci --offline --ignore-scripts`** at the tree root and nothing else; a cache miss FAILS rather than fetches (then NOT RUN,
  missing tarballs named). Prove `node_modules/.package-lock.json` against `git show <sha>:package-lock.json` **entry by entry**, with
  `lockcmp.py` AND `lockwalk.py`. **Never npm audit.** In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree,
  cat-file, grep, merge-base, archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc.**
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own.
  A control derived from the run it validates is not a control. **For this gate that means: every instrument reddens its pre-fix sha
  (`987178c` and `609e967` for VSP-74, `e34add4` and `609e967` for VSP-75, `609e967` for VSP-69; the round-1 anchors `d2531ea`, `cad19ab`,
  `0d992e0` only where a round-1 claim is re-derived) before its green at the head means anything; the cascade matrix differs between `987178c`
  and `a1794ad`; FIX 1's cells red at `f62917f` / `69157de`; FIX 2's control DB seen written by the §N2.10 instrument; §N4's pre-fix stub reddens {1,3,4}; the whole-DB-unreachable cell says OK at `609e967`; §N3.4's `609e967` run re-sends the batch.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the portal repo**, none inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), inside the builder's scratchpad, or inside gate 1-11's report folders or trees. The
  gate fixes nothing; describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead. Every proxy, preload, stub, recorder, harness and fixture lives under YOUR project.

## TUESDAY'S RULINGS AT STAMP (2026-09-28)
- **Sequencing: DONE (recorded by the refresh, READ 08:4x):** gate 11 GO ×5 (07:54); merged to main in order VSP-66 (`1976275`, fast-forward),
  VSP-71 (`dad64d2`), VSP-70 (`8efb159`), VSP-68 (`8720b34`), VSP-73 (`609e967`); forward merges VSP74 `987178c`, VSP75 `e34add4` (+ `d7a5e77`,
  `987afab`, `949b72e`), VSP69 `e79682a`; the stub fix in `e64d54e` on the VSP-75 branch. **STAMPED — Tuesday's merge-record
  confirmation: gate 11's five GO heads are on portal main `609e967` in the order VSP-66 (fast-forward `1976275`), VSP-71 `dad64d2`, VSP-70
  `8efb159`, VSP-68 `8720b34`, VSP-73 `609e967`; Tuesday verified main at each step by `ls-remote` (08:02-08:11 AEST).** The drafter's
  `log --format='%h %p %s' 0d992e0..609e967` (08:4x) agrees on order and parents. The MERGED mails' suite sets were NOT supplied at stamp:
  the gate measures main `609e967`'s sets itself (§N5.2) and compares with gate 11's merged prediction (unit 114, db 93).
- **WRONG (h) of gate 11 (product `vsp71_*` roles/databases and `vsp73_*` databases created by `test:db`) — carried over and EXTENDED to
  YOUR OWN `vsp_qa_g12_*_test_lazy` (never the builder's `salesportal_test_lazy`): permitted ONLY inside a `test:db` run; list every such name before and after; a leftover LOGIN role of YOURS (its
  `<pid>` one of your own test processes, proved from your run log) is dropped at once with its databases, and each drop named in the report; a
  leftover whose pid is NOT yours, and `salesportal_test_lazy` (the builder's), is reported, never touched.** **STAMPED — Tuesday's
  product-test database ruling:** every `test:db` run uses the gate's OWN databases via `TEST_DATABASE_URL` (`vsp_qa_g12_*_test`), and the
  lazy suite therefore uses `<that>_lazy`; **never run it with `TEST_DATABASE_URL` unset; if the gate measures ANY write to
  `salesportal_test_lazy` or to any builder database, that is a FAIL of VSP-75 and the gate STOPS that arm.** **WRONG (t) is RESOLVED by FIX 2 (`41c4a66`): the gate runs the lazy suite against its own
  database via `TEST_DATABASE_URL` (`vsp_qa_g12_<epoch>_test_lazy`, listed, left in place); the checked-edit fallback applies ONLY if §N2.10
  measures the file reaching `salesportal_test_lazy`, and then FIX 2 is a FAIL of VSP75.**
- **Second pass's item 4 RULED (Tuesday, Jira VSP-75 comment 38536):** an empty database's clean dump says OK — correct; a wrong database —
  out of scope. **Item 2 (coupling understated)** stays the gate's question (§MERGE COUPLING).
- **ANSWER-subject quirk:** an ANSWER to you arrives from `tuesday-agent@agentmail.to`; treat that inbox's mail signed "-- Tuesday" as Tuesday's,
  whatever the bracketed prefix (gate 11's answer arrived as `[Wednesday -> QA/Vision-gate11] ANSWER`); anything from any other inbox is not.
- **Holes (a) and (b) are the HEADLINE risk of VSP-74:** if any cell loses or changes a row of a table the plan must keep, that is a FAIL of
  VSP-74 (Tier 1), not an observation.
- **MERGE COUPLING:** if the gate GOes VSP74 and NO-GOes VSP75, Tuesday does NOT merge VSP74 alone (§MERGE COUPLING); say in the verdict what
  the gate measured on VSP74 alone.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets/report.md`
(sections and `evidence/` beside it).

**QUESTIONS:** your routing name is **`QA/Vision-gate12`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate12] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 12` and then
`: VSP74 @ <sha7> <GO | NO-GO> · VSP75 @ <sha7> <GO | NO-GO> · VSP69 @ <sha7> <GO | NO-GO> · merged <CLEAN | BACKLOG-ONLY | CONFLICT>`
(each `<sha7>` the pinned head from the launcher's table).
Lead the body with three sentences, one per target: (1) VSP74 — is an incomplete backup (failed, lacking, outside-with-rows, absent-with-rows)
refused with nothing changed, and with `--allow-incomplete` is EVERY kept table left exactly as it was, including CASCADE and SET-NULL children
via the closure, with `987178c` reddening on the same instrument? (2) VSP75 — does the backup carry every table the code creates (by YOUR
census) in FK order, does a round trip over a TRUNCATEd AND a populated database give back identical rows, is there no secret in it, does the
injected failure really reach the dump query, is VSP68-G11-F1 closed (empty message INCOMPLETE; whole DB unreachable FAILED), and are the lazy
tables absent while every other missing table is INCOMPLETE? Does an old 10-table backup restore as FIX 1 claims, does YOUR measured deploy-time
table match the READY's, and did the lazy suite stay off `salesportal_test_lazy` (FIX 2)? (3) VSP69 — on the forward-merged head, after a failure, a black hole, and a real
process death, is every committed send never repeated and every due reminder sent, with two instances never double-sending, and is M2 correct
or not under the query bound? Then one line on the merged tree **with its local coverage figure and whether MERGE COUPLING holds**, **and one
line on the class cap: this is ROUND 1 for all three classes; a NO-GO here is that class's first; a NO-GO in its round 2 goes to Kam.** You
have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **Three verdicts, each GO / NO-GO**, naming the pinned sha and the branch. For each: the red at the pre-fix sha on YOUR instrument, the
  green at the head, the builder's cells and mutants re-derived, Node 20 (or NOT RUN), and the suites as sets vs `609e967`.
- **The merged-tree line:** the merge results, the BACKLOG resolution, the merged suites as sets, the merged coverage (lines and branches, local,
  not CI), §N4's required cell, MERGE COUPLING, and the semantic interactions of §12.
- The verbatim strings an operator needs: VSP-74's refusal message for each group (failed / lacking / outside / absent-with-rows) and the
  `--allow-incomplete` warning lines; the `Restore failed:` line and rc; the measured deploy-time table for a pre-deploy 10-table backup (§N2.9, one line per trigger table); VSP-75's
  backup `metadata.tables`, `failed_tables` and `absent_tables`, the alert on a fresh DB, on an empty-message failure, and on a whole-DB outage;
  VSP-69's `[reminders] dispatch failed:` line in each fault shape; `SELECT version()`.
- **Rule 2: what you did NOT test is first-class output.** Write a NOT TESTED section that covers at least **CI (UNMEASURED: gh not authed)**,
  **the restore CLI end to end against Azure Blob Storage**, **real Azure Blob Storage, real ACS and real ntfy**, **production's catalog and its
  two lazy feedback tables**, **the size of a full production backup**, **a real App Service restart and multiple real instances**, **a real
  stalled Azure Postgres / TLS / failover**, **Node 22**, **the container image** the App Service runs, and **`e2e:pro` / `e2e:api` /
  `e2e:feedback`**. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.**
- Report every pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads (third pass): main `609e967d6b03…`, `fix/vsp-74-restore-refuses-incomplete-2026-09-28` `a1794ad5111b…`,
  `fix/vsp-75-backup-all-tables-2026-09-28` `41c4a664a9d1…`, `fix/vsp-69-dispatch-per-reminder-2026-09-28` `e79682a3ee9a…` | `git -C <portal>
  ls-remote origin` + `cat-file -t` (commit ×4) | read 2026-09-28 09:17:49 AEST
- third pass: chains 8 / 20 / 2 and merge parents (`2ed83fe` = `69157de` + `a1794ad`), per-commit file lists (`a1794ad`, `2ed83fe`, `0d1376c`,
  `41c4a66`), blob matrix and `test(` counts at `a1794ad` / `41c4a66`, `restorePlan()` lacking loop (`41c4a66:136-148`), FIX 2 lines
  (`backup-lazy-absent.test.js:1-40`), `restore-old-backup.test.js` cell names | `rev-list`, `log`, `diff --name-only`, `rev-parse`, `show | grep`
  under bash | read 09:1x; the VSP-74 and VSP-75 r3 READYs read whole 09:1x
- second pass heads: `f62917f60518…`, `69157de61521…` (+ main, VSP69 as above) | `ls-remote` | read 08:38:45 AEST
  | read 2026-09-28 08:38:45 AEST (refresh drafter); Tuesday's own reading 08:3x per the commission
- chains, merge parents, counts 7 / 16 / 2, 0 behind | `log --format='%h %p %s'`, `rev-list --no-merges` / `--merges` / `--count` | read 08:4x
- main `0d992e0..609e967` (five gate-11 heads, four merge commits) | `log --format='%h %p %s'` | read 08:4x
- file sets, blob matrix (17 files × 6 shas), `test(` counts | `diff --name-only`, `rev-parse <sha>:<path>` under bash | read 08:4x
- `dbRestore.js` whole at `f62917f` (283 lines); `f62917f..69157de` diff of `dbRestore.js`; `dbBackup.js:1-200` at `69157de`; `backupTables.js` whole
  at `69157de`; dbBackup.test.js cell names at `609e967` and `69157de` and the assertion diff; `backup-coverage.test.js:1-56` | `git show`, `git diff` | read 08:4x
- lazy-table lines (`routes/feedback.js:20-25`, `:325-336`; `feedbackDigest.js:26-34`) | `git show | sed -n`, `git grep -n 'CREATE TABLE'` | read 08:4x
- no boot-time INSERT into a PRO table in `server/` | `git grep -n -E` at `609e967` (0 hits) | read 08:4x
- gate 11 verdicts, findings, coverage, NOT TESTED, self-findings, tools | gate 11 `report.md` (650 lines, read whole) + `ls evidence/tools` | read 08:3x-08:4x
- Tuesday's PHASE 2 rulings | `fleet/briefs_staged/2026-09-28_vision_gate11_merge_and_gate12_prep.md` (read whole) | read 08:3x
- round-2 claims | the three r2 READY mails (read whole) | read 08:3x
- round count | `grep -c -E 'VSP-?(69|74|75)'` on gate 11's report (0); `ls` of the Vision reports folder | read 08:40
- seats and panes; load 18.05 / 16.67 / 17.43; `:5433` LISTEN (Docker); routing lines up to `QA/Vision-gate11` (no gate 12 yet) |
  `ps -axo`, `tmux list-panes -a`, `uptime`, `lsof`, `grep` of `fleet/inbox_routing.conf` | read 08:40
- first-draft provenance (round-1 READYs, `0d992e0`-era reads, schema FK lines at `0d7a2fb`) | `…vsp69.md.pre-0928-refresh` | read 06:42-06:5x
- STAMP (Tuesday's rulings 1-7, relayed to the drafting subagent): NODE20-LEG, the merge-record confirmation, the product-test database
  ruling, the Self-check note; seats re-read by `ps -axo` + `tmux list-panes -a` at 09:25:31 AEST; routing line `QA/Vision-gate12` added to
  `fleet/inbox_routing.conf` (backup `.pre-0928-gate12`); whole brief re-read for contradictions, 8 fixed (stale line refs at `f62917f`, §N5.4→§N5.5,
  the exited Vision seat, the nine-mutant count, the `complete()` file, the lazy-DB extension of gate 11's WRONG (h), the builder-DB write rule) | read 2026-09-28 09:26
- no docker, no merge-tree, no fetch was run by either drafter
