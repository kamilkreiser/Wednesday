# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 12: THREE targets on portal main `@STAMP@` (after gate 11's merges) — VSP-74 (restore refuses an incomplete backup, TIER 1), VSP-75 (the backup carries all 20 tables, TIER 1), VSP-69 (one transaction per reminder, TIER 1)

**Drafted for Tuesday on 2026-09-28 at 06:42-06:5x AEST by a read-only drafting agent. Tuesday reviews, stamps and launches it.**

**⚠ SEQUENCING — TUESDAY'S RULING, READ BEFORE ANYTHING ELSE.** Gate 12 runs **AFTER gate 11's verdict** and **after VSP-66, VSP-71, VSP-70,
VSP-68 and VSP-73 are merged to portal main.** Then the Vision seat **forward-merges main into VSP-74, then into VSP-75 (a merge, NEVER a
rebase)**, and fixes, **ON THE VSP-75 BRANCH**, the semantic conflict between VSP-68 and VSP-75: VSP-68's `server/dbBackup.test.js` stub was
written for the one-query 10-table dump and does not survive VSP-75's two-query 20-table dump (§N4 says what the source actually shows). **So
the VSP-74 and VSP-75 heads the READYs name WILL CHANGE, and so will main.** Every one of those heads, and main, is an `@STAMP@` placeholder
below. The READY heads are recorded as **pre-forward-merge READY heads, superseded at stamp**: VSP-74 `bf5bdc0`, VSP-75 `0d7a2fb`. The
launcher proves each of them is an ANCESTOR of its stamped head (no rebase) and refuses any row still carrying `@`.
**VSP-69 may keep `3ede8ed`** (one commit on the OLD main `0d992e0`) **unless main has moved in `server/reminders/dispatcher.js`.** At drafting
none of the five gate-11 heads touches that file (blob `283be27` at `0d992e0` and at all five). The launcher re-derives it at stamp: if main's
`dispatcher.js` is not `283be27`, it refuses, and VSP-69 must be forward-merged and re-pinned.

The builder's three READY mails (on disk, each read whole by the drafter):
- VSP-74: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp74-READY-mail.txt` (dated 2026-09-27T20:23:47Z)
- VSP-75: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp75-READY-mail.txt` (dated 2026-09-27T20:29:53Z)
- VSP-69: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp69-READY-mail.txt` (dated 2026-09-27T20:37:31Z)
**Every builder statement below comes from those mails, the five commit messages or the BACKLOG at each head. Each one is a CLAIM.**
**The three READYs landed within 14 minutes of each other (20:23-20:37Z), 3 to 17 minutes after gate 11's five.** Every red, every mutant and
every suite set in this brief must be **RE-DERIVED by the gate. None is taken from a READY.**
**The drafter read every row from `git ls-remote origin` at 2026-09-28 06:42:16 AEST; `cat-file -t` = commit for all three READY heads.** Those
readings are PROVENANCE for the READY heads only; the stamped heads are read by Tuesday at stamp and by the launcher at launch.
The launcher parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

NODE20-LEG: TUESDAY-DECIDES
<!-- Tuesday sets NOT-RUN or DOCKER-PULL-NEVER at stamp (gate 11 ran DOCKER-PULL-NEVER). The launcher refuses anything else (exit 45).
     The drafter did NOT run docker. "node:20 is present" rests on gate 10 §N.7 (sha256:8f693eaa…, linux/arm64); re-prove it (§N5.4). -->

GATE11-MERGED: 1976275635185db4551d5e3b015a66971f4563a5 5bdaeae6e28e280be380042a3dc8a56dbada0293 10ba4bbd29e34bf601426b68328f63725e228a86 7ef698d7e8c00c4c8e87060bec9f5284dfe8082a 6d7ea736b4f718cddd2e152f1ee0234d42d97bfe
<!-- The five gate-11 heads as pinned by gate 11 (VSP66, VSP71, VSP70, VSP68, VSP73). The launcher requires each to be an ancestor of the
     stamped main (exit 9). If gate 11 NO-GO'd a target and a round-2 head was merged instead, Tuesday replaces that sha here at stamp and
     says so in the Self-check note. -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build any of these changes and you owe the builder nothing. **Every line below that reports what the builder says
is a CLAIM, never evidence.**

**One gate, THREE targets, THREE verdicts (GO / NO-GO each, at its pinned sha), plus ONE merged-tree line.**
- **VSP74** at `@STAMP@` — **TIER 1 (Tuesday's ruling; the builder self-graded "Tier 3: the restore CLI, run by an operator").** Why: it is the
  DESTRUCTIVE restore path. Its job is to decide which live tables a restore empties. A wrong answer is deleted production data. Both
  failure directions are in scope: a restore that still empties a table it should leave alone, AND a legitimate restore that is now refused
  or restores less than it did.
- **VSP75** at `@STAMP@` — **TIER 1 (Tuesday's ruling; the builder self-graded "Tier 2").** Why: the data-loss path. The live nightly backup
  has never contained `quotes` or any other PRO table (READ: the 10-table list at `0d992e0` is unchanged since `96a5ff3`, 2026-04-18; the PRO
  tables arrived 2026-07-02 in `8fd81c1`/`563b338`). It also changes how EVERY table is read (`row_to_json`, PK order) and how EVERY row is
  written back (JSON columns as text). Both directions: a table still missing or not restored identically, AND a table that used to back up
  and restore and now does not.
- **VSP69** at `3ede8ed` — **TIER 1 (the builder and Tuesday agree; the head stands unless re-pinned at stamp).** Why: the client email path. It rewrites
  `dispatchDue()`, which sends reminder email to CUSTOMERS. Both directions: a reminder sent twice (the ticket), AND a reminder that is now
  never sent, sent late, sent out of order, or sent while another instance also sends it.
- **MERGED TREE:** all three × the stamped main, one line: which merges are clean, which conflict and where, and the suites as sets on the
  merged tree.

**⚠ Names, written out every time:**
- **VSP74 = Jira VSP-74 = "F-B"** (found by the builder while building VSP-68; gate 11 ruled it OUT OF SCOPE there): a restore EMPTIED a live
  table whose dump had failed and put nothing back.
- **VSP75 = Jira VSP-75 = "F-A"** (same origin): the nightly backup named 10 tables; `quotes`, `quote_approvals`, `quote_sequences`,
  `pricing_config`, `tco_scenarios`, `reminders`, `notification_log`, `integration_settings`, `monday_sync` and `feedback_coordinator_state`
  were never in it.
- **VSP69 = Jira VSP-69 = gate 9's §N.4(h)** (Minor, pre-existing): the dispatcher sent a batch of up to 50 inside ONE transaction, so a failure
  after the first send rolled every sent reminder back to `pending` and the next tick sent them all again.

Branches: `fix/vsp-74-restore-refuses-incomplete-2026-09-28`, `fix/vsp-75-backup-all-tables-2026-09-28` (stacked on VSP-74),
`fix/vsp-69-dispatch-per-reminder-2026-09-28`. **None is on main.**

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`,
  dated 2026-09-25 15:19): read it whole. **C-01..C-06. No C-entry covers VSP-69, VSP-74 or VSP-75** (drafter READ 06:47: zero matches for the
  three ids, and none for "backup", "restore" or "reminder").
- **PRODUCTION IS LIVE for this project.** `datasec-sales-portal-rg` holds the live site `https://datasec-sales-portal.azurewebsites.net`,
  its production Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault `datasec-sales-kv`. Production runs Node 20
  (`.github/workflows/test.yml`, READ at gate 10). **The nightly backup (VSP-75) and the reminder dispatcher (VSP-69) run in production on a
  schedule; the restore CLI (VSP-74) is run against production by an operator.** **Nothing in this gate touches production** (§13, HELD).
- **Tuesday's rulings are Tuesday's, not Kam's:** the three tiers; F-B = option (3) "both" (refuse by default, `--allow-incomplete` to
  proceed, AND `clearTables()` never empties a failed table); VSP-69 = option A (one transaction per reminder); "measure first, then build"
  for F-A; the sequencing above. **No product choice in any target is Kam's ruling.** Report each of these as the BUILDER's choice and say
  whether it needs Kam: VSP-74's refusal text and flag name; VSP-75's inclusion of `feedback_coordinator_state` and `integration_settings`
  (the READY: "CHOICES FOR YOU TO OVERRULE"; their reasons are in a STATUS mail the drafter did NOT see, WRONG (p)); the exclusion of
  `session`; VSP-69's at-least-once design (option B, claim-first, "Kam's call if ever wanted"), its per-tick cap of 50, and ending the tick on
  the first failure.
- **Deploys are HELD for Kam. Nothing merges on your word.** A merge is Tuesday's GO on a pinned head. A deploy is Kam's word.

## PRIOR ROUND
PRIOR ROUND: none of these three targets has been gated before. Each is ROUND 1 of its class. The fleet's two-NO-GO cap applies PER CLASS:
a NO-GO here is the class's FIRST; a round 2 may follow on Tuesday's word; a NO-GO in round 2 sends that class to Kam.
**How the drafter established "round 1" (READ 06:44-06:46):** zero matches for `VSP-?(69|74|75)` in the gate 9 briefs
(`2026-09-27_vision-gate9-vsp65.md`, `…-gate9-vsp65-qqpurge.md`), the gate 10 brief, and the gate 9 and gate 10 reports; the gate 11 brief
names VSP-69 once, only in its seat list ("building VSP-69"), and names F-A / F-B only as OUT OF SCOPE. QQ gates 1-3 drove `dispatchDue()`
for HTML escaping (a different class). Gate 11's report did not exist yet (its folder held only `evidence/`).
**ITS REPORT IS ON DISK AT:** the origin findings live in gate 9 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge`
(`report.md`: §N.4(h), lines 204-207, the dispatcher re-send; FINDINGS INDEX line 436) and gate 11 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets`
(`report.md`, written after this draft: **read its VERDICT, everything on VSP-70 and VSP-68 (VSP-74 and VSP-75 sit on top of both), its WRONG (n)
ruling on the fresh-database `feedback` INCOMPLETE alert, its VSP-66 `dispatchDue()` real-caller cell, its NOT TESTED, its self-findings,
and its `evidence/tools/`**). Gate 10 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2`
(`report.md`, `evidence/tools/`) holds the instruments gate 11 copied.
Origin findings, each a CLAIM until you measure it:
- **§N.4(h) → VSP-69.** Gate 9 MEASURED with recorders only: in the builder's model (Postgres told) the HEAD sent one client reminder TWICE
  (tick 1 sends, the UPDATE times out and rolls back, tick 2 re-sends); **"Under a true black hole, both MAIN and HEAD send it twice once the
  zombie backend dies (tick 3; `vsp/*dispatch-blackhole*`)."** Ruling: pre-existing at-least-once; Minor; ticket it.
- **F-B → VSP-74 and F-A → VSP-75:** found by the builder, not by a gate. Their only measurements are the builder's (on the builder's own
  `salesportal_test`). Gate 11 was told not to measure them.
- **Self-findings from gates 2-11 bind you:** quote every path (the project path has a space and a `!`); run every loop and every
  `git show <sha>:<path>` under **bash, not zsh** (zsh reads `$S:path` as a history modifier: the drafter hit it again in this draft); never
  detach a control server; **the portal test-DB name MUST end in `_test`**; npm's update-notifier egresses unless you disable it; record the load
  average beside every timing number (**a latency result with no load figure is not a measurement**); count reuse by backend pid + pool
  counters, never bytes; a spawnSync launcher blinds your own observers; backend pids by `client_port` are null through Docker's NAT (use
  `client.processID` + `pg_stat_activity`); a harness that counts rows in a table that may not exist must tolerate its absence.
- **PRIOR WORK: verify every claim against git history and gates 9-11's evidence, never against this brief.**
- **Instruments are REUSED BY COPY.** Prefer gate 11's `evidence/tools/` (newest; it carries gate 10's arms plus the TERMINATE/FIN shapes, the
  real-Postgres VSP-68 recorder cell and the VSP-70 masking cell). If gate 11's tools are absent, copy gate 10's: `qa-g10-stallproxy.cjs`,
  `qa-harness-g10-vsp.cjs`, `qa-g10-lib.cjs`, `qa-mkdb.cjs`, `qa-dbcheck.cjs`, `qa-floorcount.py`, `qa-io1-preload-fetchguard.cjs`,
  `qa-run.py`, `run-suite.sh`, `mktree-portal.sh`, `lockcmp.py`, `lockwalk.py`, `specsets.py`, `tapsets.py`. **COPY what you use into this
  gate's own `evidence/tools/`, read it before you trust it, and RE-POINT every hard-coded path and prefix** (gate 10's copies ENFORCE
  `vsp_qa_g10_` and hard-code `work-g10`; gate 11's will enforce `vsp_qa_g11_` / `work-g11`). **Never edit, run from, or write into gate 1-11's
  copies, evidence, trees or databases.** Record the sha1 of each copy before and after your edits. **Roles left by earlier gates
  (`vsp_qa_g10_*`, `vsp_qa_g11_*`) are not yours: never use, alter or drop them.**

## PIN — HEADS (VSP74, VSP75 and MAIN-P STAMPED BY TUESDAY AFTER THE FORWARD MERGES; parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head, base and a commit count, and no `@`; the head is a commit; the base is
an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin refs/heads/<branch>` equals the head
NOW; no target is on main. **VSP74 and VSP75 must be FULLY forward-merged: base = MAIN-P's head, 0 commits behind main.** **Their
NON-merge commits over main must be exactly the READY chains** (VSP74: `d2531ea`, `bf5bdc0`; VSP75: those two plus `cad19ab`, `0d7a2fb`,
plus AT MOST ONE stub-fix commit that touches only `server/dbBackup.test.js` and `BACKLOG.md`). Every merge commit has exactly two parents
and its second parent is on main (or, for VSP75, on VSP74). **The pre-forward-merge READY heads must be ancestors of the stamped heads**
(`bf5bdc0` of VSP74 and VSP75; `0d7a2fb` of VSP75): that is what "never rebase" means. **VSP69** keeps base `0d992e0` and 1 commit; its
base may be STALE against the new main (a NOTE, not a refusal), but main's `server/reminders/dispatcher.js` MUST still be blob `283be27`.
**Gated anchors (the launcher checks them):** the five `GATE11-MERGED` shas are ancestors of MAIN-P; `0d992e0`'s single parent is `b5c3e8d`;
`12138cb` (VSP-70's refactor) is on main.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | @STAMP@ | - | - | IN |
| VSP74 | portal | fix/vsp-74-restore-refuses-incomplete-2026-09-28 | @STAMP@ | @STAMP@ | @STAMP@ | IN |
| VSP75 | portal | fix/vsp-75-backup-all-tables-2026-09-28 | @STAMP@ | @STAMP@ | @STAMP@ | IN |
| VSP69 | portal | fix/vsp-69-dispatch-per-reminder-2026-09-28 | 3ede8ed7e67e686261a260e914bb84600de84a12 | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | 1 | IN |
<!-- PIN-HEADS:END -->

**Pre-forward-merge READY heads, superseded at stamp (PROVENANCE only; never gate these):** VSP74 `bf5bdc06c07b59bf956ae7d40e436582ff1fe24d`
(`10ba4bb` → `d2531ea` refactor → `bf5bdc0` fix); VSP75 `0d7a2fb4514a682c0cb3a69593faf9ff3238a93b` (`bf5bdc0` → `cad19ab` refactor → `0d7a2fb`
fix); main `0d992e09ebe0830dbe414aa73ca9a17a1be6c480`. All three READ at `ls-remote` 06:42:16.

Repo: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`). **The portal has no CLAUDE.md inside the repo;** its rules are
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (read it; its deploy commands are NOT for you).

**The shape at drafting (READ 06:42-06:48, at the READY heads; re-derive it at the stamped heads):**
- **VSP74 (`10ba4bb..bf5bdc0`), 3 files:** `BACKLOG.md` (+6), `server/dbRestore.js` (`5f4b71d` at `10ba4bb` → `a8ebbc4`), `test/db/restore-incomplete.test.js`
  (new, blob `df9d5b7`, 5 `test(`). `d2531ea` touches `server/dbRestore.js` only. At `bf5bdc0`: `failedTables(data)` (`:106-110` at `0d7a2fb`),
  the `!failed.has(t)` skip in `clearTables()` (`:124`), `parseArgs()` (`:143-148`), `restoreData()` with the refusal (`:197-224`).
  **Over the stamped main (VSP-70 merged), the file set is predicted to be the same 3 files.**
- **VSP75 (`bf5bdc0..0d7a2fb`), 5 files:** `BACKLOG.md` (+7), `server/backupTables.js` (new, 20 tables + `BACKUP_EXCLUDED = {session}`),
  `server/dbBackup.js` (`5e0cfbe` → `5530445`: the shared list, `dumpTable()` reads the PK from `pg_index` and `SELECT row_to_json(t) AS r …
  ORDER BY <pk>`, exports `buildBackup` and `TABLES_TO_BACKUP`), `server/dbRestore.js` (`a8ebbc4` → `a41e166`: `RESTORE_ORDER` from the shared list;
  `restoreTable()` sends `json`/`jsonb` columns as `JSON.stringify` text), `test/db/backup-coverage.test.js` (new, blob `44a8dc7`, 5 `test(`).
  `cad19ab` touches `server/dbBackup.js` only. **Over the stamped main the predicted set is 7 files:** those 5, VSP-74's
  `test/db/restore-incomplete.test.js`, and `server/dbBackup.test.js` (VSP-68's file, changed by the stub fix). `server/dbBackup.js` at the
  stamped VSP75 must carry BOTH VSP-68's lines (`failed_tables`, the INCOMPLETE alert) and VSP-75's (`row_to_json`, `backupTables`).
- **VSP69 (`0d992e0..3ede8ed`), 3 files:** `BACKLOG.md` (+7), `server/reminders/dispatcher.js` (`283be27` → `7a67be9`; `sendReminder()` `:132-145`,
  `dispatchDue()` `:147-184`, `DISPATCH_PER_TICK = 50` `:130`), `test/db/dispatch-once.test.js` (new, blob `c3b0d92`, 5 `test(`).
- **Same blob at `0d992e0` and ALL THREE READY heads:** `package.json` (`d3b76fb`), `package-lock.json` (`9d426df`), `.github/workflows/test.yml`
  (`0cb2d05`), `test/db/helpers.js` (`1d90638`), `scripts/run-db-tests.js` (`c48966c`), `server/initDb.js` (`e1ccf0f`), `server/schema.sql`
  (`c076d90`), `test/db/concurrency.test.js` (`0d2fc8d`), `server/db.js` (`0d402a0`). **VSP-69's files are touched by no gate-11 target and by
  neither VSP-74 nor VSP-75; VSP-74/75's are touched by no gate-11 target except `server/dbRestore.js` (VSP-70, their base) and
  `server/dbBackup.js` + `server/dbBackup.test.js` (VSP-68).**
**A GO is a statement about the pinned SHA only.** If a head moves, that target's verdict expires.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READYs — found by the drafter (verify each; all are claims)
- **(a) VSP-74's guarantee has a CASCADE hole (READ; the HEADLINE risk of VSP-74; measure it).** `clearTables()` never issues `DELETE` on a
  failed table (`dbRestore.js:124` at `0d7a2fb`), but the schema deletes FOR it. `server/schema.sql` at `0d7a2fb` declares `ON DELETE CASCADE`
  from `leads` into `meetings` (`:43`), `lead_collateral_provided` (`:91`), `reminders` (`:219`), `monday_sync` (`:241`) and `email_log`
  (`:251`); from `quotes` into `quote_approvals` (`:190`) and `reminders` (`:220`); and `ON DELETE SET NULL` into `quotes.lead_id` (`:158`),
  `tco_scenarios.lead_id` (`:205`), `lead_collateral_provided.collateral_item_id` (`:92`) and `email_log.template_id` (`:252`). So with
  `--allow-incomplete`, if `meetings` (say) FAILED and `leads` did not, the `DELETE FROM "leads"` inside the clear transaction CASCADES and
  empties every lead-linked `meetings` row: **the failed table is emptied, not "left exactly as it is"**, and `restoreTable('leads')`
  (`:72`) deletes again outside the transaction. **The builder's cell 4 cannot see this:** its failed table is `collateral_items`, a
  PARENT whose only child link is SET NULL, and its other table is `email_templates`. Predicted: a failed CASCADE-child loses its rows; a
  failed SET-NULL child (`quotes`) keeps its rows with `lead_id` nulled. **If measured, it is a FAIL of VSP-74 (Tier 1).**
- **(b) Tables ABSENT from a backup are neither refused nor protected (READ; measure).** `failedTables()` counts only `metadata.failed_tables`
  and entries with `error`. A table in `RESTORE_ORDER` with NO entry at all is skipped by the clear (`data.tables[t] &&`) and by the insert
  loop ("(empty, skipped)"), but nothing stops a cascade into it. **Every backup in production today is a 10-table backup** (VSP-75 is not
  deployed), so on a VSP-75 tree restoring the latest real backup is this shape: `reminders`, `monday_sync`, `quote_approvals` are not in it,
  and `DELETE FROM "leads"` cascades into them. `DELETE FROM "users"` then meets `quotes.created_by_user_id` (NO ACTION, `:170`) and should
  fail `23503`, rolling the whole clear back. **Predicted: the old-backup restore FAILS with 23503 on any database with a quote (nothing
  changed), and on a database whose quotes have no creator it SUCCEEDS and silently empties the cascade children.** Measure both at
  `0d992e0` (pre-existing?), at VSP74 and at VSP75, and rule whether an absent table should count as "does not contain".
- **(c) The semantic conflict is real, but not for the reason the VSP-75 READY and the commission give (READ; measure it; §N4).** VSP-68's stub
  (`server/dbBackup.test.js:26-31` at `7ef698d`) answers EVERY query with `{rows: [{id: 1}, {id: 2}]}`, so it does answer both of VSP-75's
  queries (the PK lookup gets two rows with `attname` undefined; the row query's `r => r.r` maps to `[undefined, undefined]`, rowCount 2). What
  breaks: **(i)** cell 1 asserts `total_rows` 20 ("ten tables, two rows each"); with 20 tables it is 40. **(ii)** The failure injector matches
  `sql.includes(\` ${t} \`)`; VSP-75's SQL names the table as `"${tableName}" t` (quoted, and the PK query passes it as a parameter), so **the
  injected failure never fires**: cells 3 and 4 (the INCOMPLETE alert and the partial-backup marker) go red because the backup is announced
  OK. Predicted on an un-fixed merged tree: dbBackup.test.js failing {1,3,4}, passing {2,5}. **The danger is a "fix" that makes the cells green
  without the injected failure landing on the dump query.** The required cell (§N4) is written against that.
- **(d) VSP-75 × VSP-68 × gate 11's WRONG (n) (READ; measure).** VSP-75 adds `feedback_coordinator_state`, which, like `feedback`, is created
  lazily by its route. On a database where neither route has run (a fresh deploy, or production if nobody used the coordinator), the pk lookup
  (`$1::regclass`) throws `42P01` for BOTH, so every nightly backup is INCOMPLETE naming two tables, **and VSP-74 then refuses to restore that
  backup without `--allow-incomplete`.** Rule the chain: true alarm, noise, or a restore made unusable by default. Production's two lazy
  tables: NOT TESTED (READ ONLY forbidden too).
- **(e) VSP-75's drift cell has blind spots (READ; measure with mutants).** `tablesInCode()` (`backup-coverage.test.js`) walks `server/` only,
  skips `*.test.js`, and matches only `/CREATE TABLE IF NOT EXISTS\s+"?(\w+)"?\s*\(/`. A table created by a plain `CREATE TABLE x (`, a
  schema-qualified `public.x`, a `CREATE TABLE … AS`, or code under `scripts/` is invisible. Predicted: a mutant adding `CREATE TABLE
  qa_drift (id int)` to server code SURVIVES cell 1 (cell 4, from the live catalog, would see it only if it had an FK).
- **(f) VSP-69's M2 argument omits the query bound (READ; decide it; §N3.4).** The READY: M2 (`FOR UPDATE` without `SKIP LOCKED`) survives
  "and that is correct … Exactly-once holds either way; SKIP LOCKED is kept for throughput". But a second instance WAITING on the row lock is a
  query under `DB_QUERY_TIMEOUT_MS` (30 s shipped) that holds a pool slot for the whole of the first instance's send. If the send outlasts the
  bound, the waiter's `SELECT … FOR UPDATE` times out and ends that instance's tick (and discards its client). No cell measures that
  because the builder's cell 4 slows sends by 30 ms. Also READ: with `ORDER BY … LIMIT 1 FOR UPDATE`, after the holder commits PG re-checks
  the row, and whether the waiter then takes the NEXT row or returns none is the planner's `LockRows`/`Limit` order. Measure, do not assume.
- **(g) VSP-69: a reminder whose send THROWS blocks every later reminder, every tick (READ; measure at both shas).** The loop orders by
  `due_at, id` and a throw ends the tick (`:174-177`) with the row rolled back to `pending`. A deterministic throw on reminder K means every
  tick picks K first, throws, and stops: every reminder due after K waits forever. The same was true of the batch at `0d992e0`. **Predicted
  pre-existing; measure it, and say whether `sendEmail()` can throw (vs return `{ok:false}`) for any input a user can create.**
- **(h) VSP-69: `cutoff` is a JS Date (READ).** `SELECT NOW()` comes back as a Date with MILLISECOND precision; `due_at` is `TIMESTAMPTZ`
  (microseconds). A reminder inserted by `generateRuleReminders()` in the same tick with `due_at = NOW()` in the same millisecond as the
  cutoff is skipped until the next tick. Minor; measure once or rule it unreachable.
- **(i) VSP-69 × VSP-66 on the merged tree.** Gate 11's end-to-end `dispatchDue()` kill cell ran the OLD dispatcher (one checkout per tick).
  VSP-69 makes up to 50 checkouts per tick through VSP-66's `guard()`. Re-run a terminate-during-send cell on the merged tree (§N3.5).
- **(j) The VSP-69 test sets a dummy ACS connection string itself** (`dispatch-once.test.js:22-23`, `endpoint=https://vsp69.invalid/`,
  `reminders@vsp69.invalid`) and replaces `@azure/communication-email` through `require.cache` (`:27-37`). That is the product's test, not your
  process env. Prove the stub was in place (no DNS or socket for `vsp69.invalid`).
- **(k) VSP-75's `integration_settings` "no secrets live here: see settingsStore.js" (`backupTables.js` comment) — UNVERIFIED by the drafter.**
  A backup is uploaded to blob storage and downloadable by an operator; a secret in it would be a new exposure. READ `server/settingsStore.js`
  and MEASURE with every settings route exercised on YOUR database: dump the table's row_to_json and list every key.
- **(l) The `session` exclusion and restored user ids (READ; a pre-existing shape the exclusion makes explicit; measure once).** A restore puts
  back the backup's `users` and resets `users_id_seq` to max(id) (`resetSequence`). Live sessions (not restored, by design) of a user created
  AFTER the backup now point at a user id that no longer exists; **the next user created gets that id, and the stale session may then
  authenticate as the NEW user.** Measure at `0d992e0` and VSP75: create user X after a backup, sign X in, restore, create user Y, replay X's
  cookie on `/api/auth/me` (or the equivalent route). If the cookie is Y, it is a finding (pre-existing; say so).
- **(m) The READY red-proofs ran on the builder's `salesportal_test`,** the builder's own database. Never use it (§13.2).
- **(n) VSP-74's READY: "A backup file actually produced by VSP-68's code" is NOT TESTED** (the branches were not merged). On the merged tree
  it is testable end to end: a real `runBackup()` with a real failed table → the real blob JSON → `restoreData()`. §N1.4.
- **(o) VSP-75's round-trip cell restores into a TRUNCATEd database.** A real restore runs over a POPULATED one (clear, then insert). §N2.3 runs
  both.
- **(p) UNVERIFIABLE by the drafter: the VSP-75 STATUS mail** ("The measurement went to you in the STATUS mail and is on the ticket"; the reasons
  for including `feedback_coordinator_state` and `integration_settings`). It is not among the briefs on disk. Tuesday: attach it or name its
  path at stamp; otherwise the gate treats those reasons as unstated.
- **(q) Merge prediction: UNMEASURED by the drafter** (it may not run `merge-tree --write-tree`). READ only: VSP-69 and all five gate-11 heads
  insert their BACKLOG block at the same anchor (`@@ -31,0 +32`), so VSP-69 × main is predicted to CONFLICT in `BACKLOG.md` only. VSP-74 and
  VSP-75 will already contain main after the forward merge, so VSP74 × main and VSP75 × main are predicted CLEAN (fast-forwardable). **The
  gate derives every merge in its own object dir.**
- **(r) Tiers: the builder graded VSP-74 "Tier 3" and VSP-75 "Tier 2"; Tuesday's commission rules both TIER 1.** Recorded above as Tuesday's
  ruling. Grade them at Tier 1.
- **(s) UNVERIFIABLE by design, and you must not try:** production's catalog (any table the code does not create), production's two lazy
  feedback tables, the size of a full production backup, real Azure Blob Storage, real ACS, real ntfy, a real App Service restart or a
  second real instance. **Carry each as NOT TESTED.**
- **Verified TRUE at source (READ):** all three READY heads and main by `ls-remote` (06:42:16); VSP-74 = `10ba4bb` → `d2531ea` → `bf5bdc0`,
  VSP-75 = `bf5bdc0` → `cad19ab` → `0d7a2fb`, VSP-69 = `0d992e0` → `3ede8ed` (one commit), all linear, parents read by `git log --format='%H %P'`;
  the file sets above; `backupTables.js` lists exactly 20 tables and excludes only `session`; `test(` counts 5 / 5 / 5; `dbRestore.test.js`
  (VSP-70's, 4 `test(`) is the same blob `8315d41` at `10ba4bb` and `0d7a2fb`; `dispatcher.js` is `283be27` at `0d992e0` and at all five gate-11
  heads; the old backup list has had no edit since `96a5ff3`.

## THE READYs — their FIX, CELLS, RED-PROOFS, PRIOR WORK and NOT TESTED (the gate rules on every claim)
The three READYs are on disk (paths at the top); read each whole. Their NOT TESTED lines are carried VERBATIM here (the launcher checks it):

VSP-74 NOT TESTED
- The CLI end to end against Azure blob storage (not touched).
- A backup file actually produced by VSP-68's code. The cells build the JSON in the shape dbBackup writes; the two branches are not merged together.
- Node 20 / CI: UNMEASURED.

VSP-75 NOT TESTED
- Azure blob upload/download (untouched).
- Production's catalog: unread. A production table the code does not create would still be missed; cell 1 only guards the code.
- JSON size of a full production backup with quotes: not measured.
- Node 20 / CI: UNMEASURED.

VSP-69 NOT TESTED
- A real ACS send (SDK recorded) and a real process death mid-tick (the fault is an injected UPDATE rejection; VSP-66's cells cover link death generally).
- Connection churn: one checkout per reminder, up to 50 per tick. Not measured under load. Each is a single short transaction.
- Node 20 / CI: UNMEASURED.

**The READYs' red-proof claims, in one line each (each a CLAIM, re-derived in §N):**
- VSP-74: at `d2531ea` failing {2,3,4,5}, passing {1} (cell 4: `collateral_items` went from ['live one','live two'] to []); at `bf5bdc0` 5/5 ×2;
  M1 (no refusal) failing {2,3}; M2 (clearTables empties failed tables) failing {4}; M3 (failed set from metadata only) failing {3}.
- VSP-75: at `cad19ab` failing {1,5}, passing {2,3,4} (cell 1 lists 10 missing tables; cell 5: 19 tables not identical); at `0d7a2fb` 5/5 ×2;
  M1 (quotes dropped) failing {1,4,5}; M2 (ORDER BY id) failing {5} (`column "id" does not exist` ×4); M3 (no JSON serialise) failing {5}
  (tco_scenarios); M4 (leads after quotes) failing {4,5}; M5 (`SELECT *` with PK order) failing {5}.
- VSP-69: at `0d992e0` failing {2}, passing {1,3,4,5} (cell 2: R1:2, R2:2); at `3ede8ed` 5/5 ×2; M1 (keep going after a failure) failing {2};
  M3 (no row lock) failing {4}; M4 (`due_at DESC`) failing {1,2,3}; M5 (cap 60) failing {3}; **M2 (FOR UPDATE without SKIP LOCKED) SURVIVES,
  "and that is correct"** (WRONG (f): the gate decides).
- Sets: VSP-74 `npm test` 109/109, `test:db` 8 files (… restore-incomplete 5); VSP-75 109/109, 9 files (… backup-coverage 5); VSP-69 105/105,
  8 files (… dispatch-once 5). VSP-69 READY note: running `concurrency` + `reminder-push` in ONE parallel `node --test` fails 6 cells "identically
  at main (checked by stashing)", the known shared-DB artefact `scripts/run-db-tests.js` serialises against. **Do not repeat the builder's
  stash; measure it in your own trees.**

**How you treat these:** every NOT TESTED line you CAN test locally, you test: VSP-74 with a backup produced by the real (merged) `runBackup()`;
VSP-75's backup size on a scaled seeded database; VSP-69's connection churn under load and a real process death mid-tick; Node 20 for all
three. The CLI against Azure, a real ACS send, and production's catalog you carry into your own NOT TESTED, reworded as your own.

## 2a. LEGITIMATE SHAPES — two targets are DESTRUCTIVE-path or client-send checkers, so a false refusal or a false send is damage (template §2a)
Measure every row. **A row whose expected verdict and clause disagree is a finding against this brief. Say so.**
**The destructive path's standing rule (template §2a): until the rows below are measured, the instruction on ANY unexpected result in a
restore cell is STOP and record it, never a remedy.** Every restore in this gate runs against a database YOU created and seeded.

| shape — its ordinary form, as the portal really produces it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| VSP74: restore a COMPLETE backup (every table dumped) onto a populated production-shaped DB | not refused; every table replaced; row sets identical to the backup's | `failed` empty | builder cell 1 — **measure on a VSP-75 20-table backup** |
| VSP74: a backup with one failed table, no flag | refused before any change; message names the table and `--allow-incomplete`; CLI rc 1; every table's rows and xmins unchanged | the refusal at `restoreData()` | builder cells 2-3 — **measure** |
| VSP74: `--allow-incomplete`, failed table is a PARENT with SET-NULL children (`collateral_items`) | its rows kept; the rest restored | `!failed.has(t)` | builder cell 4 |
| VSP74: `--allow-incomplete`, failed table is a CASCADE CHILD of a non-failed parent (`meetings`, `email_log`, `reminders`, `monday_sync`, `lead_collateral_provided`, `quote_approvals`) | **the READY's promise: its rows kept. Predicted: EMPTIED by the parent's cascade** (WRONG (a)) | ON DELETE CASCADE | drafter — **measure every one; a loss is a FAIL** |
| VSP74: `--allow-incomplete`, failed table is `quotes` (SET NULL from leads, CASCADE to approvals/reminders) | predicted: rows kept, `lead_id` NULLed; its children cleared and restored | ON DELETE SET NULL | drafter — **measure; rule whether "left as it is" holds** |
| VSP74: `--allow-incomplete`, failed table is a PARENT (`leads`) whose children restore rows that point at leads the live table lacks | predicted: those child inserts fail `23503`, each swallowed as "[!] Row insert failed", CLI "Restore complete." rc 0 | per-row catch in `restoreTable()` | drafter — **measure; count the silently lost rows** |
| VSP74/75: restore today's real backup SHAPE (10 tables, no `failed_tables`, pre-VSP-68) onto a DB with quotes | predicted: `23503` on `DELETE FROM "users"`, whole clear rolled back, nothing changed (WRONG (b)) | NO ACTION FK `quotes.created_by_user_id` | drafter — **measure at `0d992e0`, VSP74, VSP75** |
| VSP74/75: the same 10-table backup onto a DB whose quotes have no creator | predicted: SUCCEEDS; `reminders`/`monday_sync`/`quote_approvals` emptied by cascade, no warning | absent ≠ failed | drafter — **measure; a silent loss is a finding** |
| VSP75: the nightly backup of an ordinary production-shaped DB (every route used once, both lazy feedback tables created) | 20 tables, `failed_tables: []`, "DB Backup OK" | the shared list | builder cell 5 — **measure through real `runBackup()` + recorders** |
| VSP75: the same on a DB where the two lazy feedback tables were never created | predicted: INCOMPLETE naming `feedback` AND `feedback_coordinator_state`; and VSP-74 refuses that backup by default | `$1::regclass` 42P01 | drafter (WRONG (d)) — **measure; RULE true alarm vs noise** |
| VSP75: round trip over a POPULATED DB (a real restore) vs a TRUNCATEd one (the builder's) | row_to_json sets identical in both | clear then insert | drafter (WRONG (o)) — **measure both** |
| VSP75: restore a pre-VSP-75 (SELECT *) backup on a VSP-75 tree | restores as before (timestamps at ms, as before); JSON columns accepted | rows are plain objects either way | builder claim — **measure** |
| VSP69: an ordinary tick, 5 due client reminders, one instance | 5 sends in due order, each once, each marked sent | per-reminder transaction | builder cell 1 |
| VSP69: two instances tick at once (App Service scale-out), sends of realistic latency | each reminder sent once; neither instance waits on the other | SKIP LOCKED | builder cell 4 at 30 ms — **measure at 30 ms and at > the shrunk bound** |
| VSP69: a user-typed reminder whose send THROWS | predicted: every later-due reminder blocked every tick (pre-existing) | stop on failure + due order | drafter (WRONG (g)) — **measure at both shas** |
| VSP69: 55 due reminders | 50 in tick 1 (most overdue first), 5 in tick 2 | cap 50 | builder cell 3 |

## N1. TARGET VSP74 — the restore refuses an incomplete backup, never empties a failed table (TIER 1) — the measurements
**FAIL condition, stated BEFORE the runs:** any restore cell in which a table the backup did not contain (failed, or, if you rule so, absent)
loses or changes a row, whether by a direct DELETE, a CASCADE or a SET NULL, without the operator being told before it happens; a refused
restore that changed anything (row sets, xmins of the live rows, sequence values); a COMPLETE backup that is now refused or restores less than
at the stamped main; VSP-70's first-error behaviour or `release(broken)` changed; the CLI's usage, `AZURE_BACKUP_CONN_STR not set.` line or
exit codes changed; a NAME lost vs the stamped main. **WRONG (a) measured as predicted is a FAIL of VSP-74.**
1. **The builder's 5 cells, RED re-derived at `d2531ea`** (a tree of the refactor; copy `test/db/restore-incomplete.test.js`, hash-verified):
   predicted failing {2,3,4,5}, passing {1}. At the stamped VSP74: 5/5, N ≥ 3. Mutants M1, M2, M3 as the READY words them, plus **M4 (yours):
   delete the `!failed.has(t)` guard but keep the refusal** (predicted: only cell 4 reddens, so the defence in depth has one cell). Fresh
   tree per arm, asserted edits, `node --check` rc quoted; **a red from a mutant that does not parse is VOID.** Quote why each is red.
2. **`d2531ea` is behaviour-preserving (READ + MEASURED):** diff `10ba4bb..d2531ea`; VSP-70's 4 unit cells pass at `d2531ea`; the CLI still
   exits 1 with `Error: AZURE_BACKUP_CONN_STR not set.` under `env -i`. **Never set that variable** (§13.3).
3. **THE CASCADE MATRIX (MEASURED; WRONG (a); the headline).** On YOUR seeded production-shaped database (every one of the 20 tables with rows,
   FK links populated: meetings, email_log, reminders, monday_sync, lead_collateral_provided on leads; quote_approvals and reminders on quotes),
   build a backup JSON with the REAL `buildBackup()` of the merged tree, then mark ONE table failed (`metadata.failed_tables` + its entry's
   `error`, the shape VSP-68 writes). Run `restoreData(data, {allowIncomplete: true})` under `env -i`. **One row per candidate failed table:**
   each CASCADE child listed in WRONG (a), `quotes`, `tco_scenarios`, `leads`, `users`, `collateral_items`, `email_templates`. Per row: the
   failed table's row count and a row checksum before and after, and every other table's. Also the same at the stamped main with the flag
   absent (the refusal must fire first) and on VSP74 alone. **A single lost or changed row in the failed table is the FAIL. Quote it.**
4. **A backup PRODUCED by VSP-68's code (MEASURED; WRONG (n); the READY's second NOT TESTED line).** On the merged tree: the real `runBackup()`
   with `@azure/storage-blob` replaced by YOUR recorder through `require.cache` and ntfy to YOUR loopback recorder (gate 11 §N4.2's method),
   one table made to fail for real (a table dropped in YOUR database, or gate 9's black hole on its dump query), then the RECORDED blob
   gunzipped and passed to `restoreData()`. Expected: refused, naming the table; with the flag, that table untouched.
5. **Absent tables (MEASURED; WRONG (b)).** A 10-table backup JSON in today's production shape (build it with `0d992e0`'s `buildBackup()` on YOUR
   DB, never a real backup) restored at `0d992e0`, VSP74 and VSP75: (i) on a DB where quotes have a creator, (ii) where they do not. Quote the
   error or the losses. **Rule whether "absent" must be refused like "failed", and say whether that needs Kam.**
6. **The refusal changes nothing (MEASURED):** for the refused path, capture `xmin` and row md5 of every table and `last_value` of every
   sequence before and after; prove no connection issued a DELETE (`pg_stat_user_tables.n_tup_del` deltas on YOUR DB).
7. **`parseArgs` and the CLI (MEASURED):** `[latest]`, `[latest, --allow-incomplete]`, `[--allow-incomplete, x]`, `[]`, **and `[--allow-incomplete]`
   alone** (predicted: `name` undefined → the listing path, which needs Azure: it must stop at `AZURE_BACKUP_CONN_STR not set.` rc 1 without
   `--allow-incomplete` being read as a blob name). Also a typo `--allow-incomplet` (predicted: read as the blob NAME if first, else ignored).
8. **VSP-70's behaviour is intact on the stamped VSP74 (MEASURED):** gate 11's VSP-70 real-Postgres masking cell (copied) passes unchanged:
   the first error thrown, the `[!] ROLLBACK failed as well:` line, the client discarded.

## N2. TARGET VSP75 — the backup carries all 20 tables except session, in FK order (TIER 1) — the measurements
**FAIL condition, stated BEFORE the runs:** any table the code creates (by your own census, not the builder's regex) missing from the backup
and not in `BACKUP_EXCLUDED`; any FK in the catalog whose parent comes after its child in `RESTORE_ORDER`; a round trip (TRUNCATEd OR
populated target) whose `row_to_json` set differs from the source for any table, or whose next id is not max + 1 on any serial table; a
backup of a database that backed up at the stamped main now failing, or a pre-VSP-75 backup that restored at the stamped main now failing;
VSP-68's INCOMPLETE alert or blob marker broken on the merged tree (§N4); a secret in the backup; a NAME lost vs the stamped main.
1. **The builder's 5 cells, RED re-derived at `cad19ab`** (copy `test/db/backup-coverage.test.js`, hash-verified): predicted failing {1,5},
   passing {2,3,4}. At the stamped VSP75: 5/5, N ≥ 3. M1-M5 as the READY words them. **Plus M6 (yours, WRONG (e)):** add a plain
   `CREATE TABLE qa_drift_g12 (id int)` to a server file (predicted: cell 1 SURVIVES). **Plus M7:** `CREATE TABLE IF NOT EXISTS public.qa_drift_g12 (`
   (predicted: survives). Quote why each is red or not.
2. **YOUR OWN table census (MEASURED; independent of the builder's regex).** Boot the stamped VSP75 tree's `initDb()` on a fresh
   `vsp_qa_g12_*` DB, drive every route that creates a table lazily (grep the tree for `CREATE TABLE` in ANY form, READ, and list them),
   then read `pg_class` (relkind `r`, schema `public`). Every table must be in `BACKUP_TABLES` or `BACKUP_EXCLUDED`. Also every FK from
   `pg_constraint` (child → parent, including self) against `RESTORE_ORDER`.
3. **The round trip, twice (MEASURED; WRONG (o)).** Seed every table (including a quote revision chain, JSONB objects, a top-level JSON array in
   `tco_scenarios.results`, a JSON column holding a bare string, NULL JSON, timestamps with microseconds, unicode, a very long text). (i) TRUNCATE
   target (the builder's); (ii) POPULATED target: the same DB after further changes (rows added, rows deleted, ids beyond the backup's). Then
   `restoreData()`. Compare per table `row_to_json` sets and per-table checksums; `nextval` = max + 1 on every serial table. Say which tables
   carry no `id` and what `resetSequence()` does for them.
4. **Real `runBackup()` on the merged tree, through recorders (MEASURED):** the blob recorder's upload gunzipped; 20 tables; `metadata` keys
   exactly `totalRows`, `createdAt` (+ `failedTables` only when non-empty); "DB Backup OK" priority 3 on a complete DB. Then the WRONG (d)
   database (no lazy feedback tables): quote the alert, and then what `restoreData()` does with that backup.
5. **Old backups still restore (MEASURED):** a backup JSON built by `0d992e0`'s `buildBackup()` (SELECT *) of YOUR DB, restored at VSP75 onto a
   DB that holds only the 10 old tables' data: row counts and values per table (timestamps at ms precision, as before).
6. **Secrets (READ + MEASURED; WRONG (k)).** READ `server/settingsStore.js` and every writer of `integration_settings`, `pricing_config`,
   `notification_log`, `feedback_coordinator_state`. Exercise each settings write route with dummy values; dump each new table's
   `row_to_json`; list every key. **Any token, key, password or connection string is a FAIL** (quote the key NAME only, never a value).
7. **Size and time (MEASURED; the READY's third NOT TESTED line):** seed a scaled DB (e.g. 20,000 quotes with realistic `computed` JSONB, 50,000
   notification_log rows; say the numbers) and measure `buildBackup()` elapsed, peak RSS, JSON and gzip bytes, at the stamped main and VSP75,
   load quoted. **Carry production's real size as NOT TESTED.**
8. **The exclusion's consequence (MEASURED once; WRONG (l)).** The stale-session-to-new-user shape at `0d992e0` and VSP75. Pre-existing if
   identical; a Major finding either way if a cookie authenticates as a different user.

## N3. TARGET VSP69 — one transaction per reminder (TIER 1) — the measurements
**FAIL condition, stated BEFORE the runs:** any reminder already sent and COMMITTED being sent again after a failure; any due reminder never
sent where the stamped main sent it (a silent miss); two instances sending one reminder; a tick that does not take the 50 most overdue;
due order changed; notification_log rows disagreeing with the sends; a send to a real provider; a NAME lost vs the stamped main. **One
re-send of the reminder IN FLIGHT at the failure is the design (at-least-once), not a FAIL; name it.**
**Real sends are OFF.** `@azure/communication-email` is replaced by YOUR recorder (through `require.cache`, before any portal module loads);
ntfy goes to YOUR loopback recorder; fetch is stubbed to throw on any other URL. Never `vsp69.invalid` resolution attempts outside the
builder's own test (count DNS lookups if you can).
1. **The builder's 5 cells, RED re-derived at `0d992e0`** (copy `test/db/dispatch-once.test.js`, hash-verified): predicted failing {2} with R1:2,
   R2:2. At `3ede8ed`: 5/5, N ≥ 3. M1, M3, M4, M5 as the READY words them. Fresh tree per arm, asserted edits, `node --check` rc quoted.
2. **Gate 9's §N.4(h) arms, re-run (MEASURED).** Copy gate 9's `dispatch-blackhole` arm (`evidence/vsp/*dispatch-blackhole*`, via gate 10/11's
   copies): (i) the builder's model (UPDATE rejected, Postgres told); (ii) a TRUE black hole on the UPDATE of reminder 3 of 5 (the zombie backend
   holds the row lock). At `0d992e0`: gate 9 saw the batch re-sent. At `3ede8ed` predicted: tick 1 sends R1-R3, tick 2 skips R3 while the zombie
   holds it and sends R4-R5, and R3 goes out AGAIN only after the zombie dies. **Count sends per reminder per tick; exactly one re-send (R3) is the
   design.** Quote the zombie's lifetime and what ended it.
3. **A real process death mid-tick (MEASURED; the READY's first NOT TESTED line).** A CHILD process running `dispatchDue()` on 10 due reminders
   with the recorder slowed; `SIGKILL` it after the recorder has seen send K. Then a fresh child ticks. Expected: sends 1..K-1 never again; send
   K at most once more; the rest once. N ≥ 5 at `3ede8ed`, and once at `0d992e0` (the positive control: the batch re-sent).
4. **M2 — decide it, do not accept it (MEASURED; WRONG (f)).** Build M2 (`FOR UPDATE` without `SKIP LOCKED`). Two instances over 10 due
   reminders with the recorder slowed to (i) 30 ms (the builder's), (ii) HALF the shrunk bound, (iii) LONGER than the shrunk bound
   (`DB_QUERY_TIMEOUT_MS=1500`, send 2,500 ms). Per arm, at `3ede8ed` and M2: sends per reminder, each instance's tick outcome, `[reminders]
   dispatch failed:` lines, pool counters, time each instance spent waiting (`pg_locks` observer, async, every 250 ms), and whether the waiter
   took the NEXT row or returned none after the holder committed. **Then RULE:** is `SKIP LOCKED` load-bearing for correctness under the query
   bound, or only for throughput? If any arm reddens M2, say that the builder's "survives, and that is correct" is wrong and name the cell the
   product test should add.
5. **Connection churn under load (MEASURED; the READY's second NOT TESTED line).** 50 due reminders per tick with signed-in route traffic in
   the same process (a request loop hitting `/me` and a quotes list): per tick, checkouts, `totalCount`/`idleCount`/`waitingCount` peaks, pool-wait
   time, request p50/p99, elapsed, load quoted; at `0d992e0` and `3ede8ed`. **Also on the merged tree with VSP-66's `guard()`:** listener count
   on the idle client after 1,000 ticks' worth of checkouts, and a `pg_terminate_backend` during send K (gate 11's real-caller method): process
   alive, R-K pending then sent once, the dead client never handed out again (WRONG (i)).
6. **The poison reminder (MEASURED; WRONG (g)).** Make one due reminder's send THROW (a recorder that throws for its id). Three ticks at
   `0d992e0` and `3ede8ed`: which reminders ever go out. Predicted: none after the poison one, at both. Then READ `server/email/index.js`
   `sendEmail()`: which inputs throw vs return `{ok:false}`; can a user create one?
7. **Order and cutoff (MEASURED; WRONG (h)).** Equal `due_at` ties go by id (the new tiebreak); a reminder inserted with `due_at = NOW()` by
   `generateRuleReminders()` in the same tick is sent in that tick (N ≥ 20; count any skipped by the millisecond cutoff).
8. **The existing dispatch cells:** `concurrency.test.js`'s "two concurrent ticks process a reminder once" and `reminder-push.test.js` pass at
   `3ede8ed` and on the merged tree, N ≥ 3 each, through `scripts/run-db-tests.js` (serialised). **The READY's parallel-invocation artefact:**
   measure it yourself in your own trees at `0d992e0` and `3ede8ed` (never by stashing in anyone's checkout).

## N4. THE SEMANTIC CONFLICT, CLOSED NOT PAPERED OVER — REQUIRED CELL (Tuesday's requirement)
**On the MERGED tree (the stamped main + VSP74 + VSP75, which after the forward merges IS the stamped VSP75 tree), BOTH of these must pass,
and each must be shown able to fail:**
1. **VSP-68's `server/dbBackup.test.js` INCOMPLETE-alert control passes** (all 5 cells, N ≥ 3), **AND the injected failure LANDS ON THE DUMP
   QUERY.** Prove it: instrument (in YOUR copy of the test, never the product's) a counter on the stub's failure path, and show it fires once
   per failing-table cell, on the query that reads the table's rows. **Positive control:** YOUR copy of the pre-fix stub (VSP-68's `7ef698d`
   blob `4fb902e`) on the merged tree must redden cells {1,3,4} (WRONG (c)'s prediction) — if it does not, your merged tree is not the one
   the conflict lives in. **Mutant:** on the merged tree, make `dumpTable()` swallow the error (`error` unset): cells 3 and 4 MUST redden. If
   they stay green, the stub fix papered over the alert.
2. **VSP-75's round-trip and FK-order cells pass** (`backup-coverage.test.js` cells 4 and 5, N ≥ 3) on the same tree, with VSP-68's
   `failed_tables` present in the backup's metadata (read it in cell 5's backup: `failed_tables: []`).
3. **Diff the stub fix** (the stamped VSP75 vs `7ef698d`, `server/dbBackup.test.js` only) and quote it: what did the Vision seat change? Is
   any assertion weakened (`total_rows` loosened to "> 0", a cell deleted, `notEqual` removed)? **A weakened assertion is a FAIL of VSP75.**
   Is the fix where Tuesday ruled it (on the VSP-75 branch, a commit or the merge commit; say which)?

## N5. SHARED — held results, suites, Node 20, CI
1. **Gate 11's HELD results on the merged tree, briefly** (one run each; compare to gate 11's report): VSP-70's real masking cell; VSP-68's real
   INCOMPLETE cell (shape A); VSP-66's terminate cell under a held client; gate 10's S1 ticket cell at the shrunk bound. "Same" or quote the
   difference, with load.
2. **SUITES AS SETS, NOT COUNTS, same machine, same session (MEASURED).** In fresh archived trees of the stamped main, each of the three heads,
   `d2531ea`, `cad19ab`, and the merged tree: `npm test` and `npm run test:db` (each `test:db` on a FRESHLY CREATED `vsp_qa_g12_<epoch>_test`,
   proven fresh: zero user tables). Extract every NAME with its outcome (`specsets.py` / `tapsets.py`), and report vs the stamped main: names
   passing at main that do not pass at the head (**must be empty**); names added (predictions: VSP74 +5 db; VSP75 +10 db over main (its own 5 +
   VSP-74's 5); VSP69 +5 db; merged +15 db, +0 unit, and `dbBackup.test.js` still 5 names); names removed (expect 0); duplicates. Each new test file N ≥ 3 at its head,
   load quoted. **CI's coverage command locally** (`node --test --experimental-test-coverage --test-coverage-lines=80
   --test-coverage-branches=70 $(find server -name '*.test.js')`) at each head and the merged tree. **Label it: local Node standing in for
   CI's Node 22; not CI.**
3. **Product-test hygiene:** after each `test:db` run, list every `vsp71_%` role and every `vsp71_%` / `vsp73_%` database in the cluster (VSP-71
   and VSP-73 are on main now, so every `test:db` of this gate creates them). Tuesday's gate-11 ruling carries over (§TUESDAY'S RULINGS).
4. **NODE 20 LEG (production's major) — per the NODE20-LEG line at the top.** If DOCKER-PULL-NEVER: exactly ONE docker verb family is
   sanctioned, for this leg only: `docker image inspect node:20` (prove the image is ALREADY present, quote its digest; if absent, the leg is NOT
   RUN — **never pull**) and `docker run --rm --pull=never` of that image, with YOUR archived tree mounted **WRITABLE**, an explicit `-e`
   allowlist (§13.3; never `--env-file`), `NODE_ENV=test`, and the database URL pointing at YOUR `_test` database via
   `host.docker.internal:5433`. Name every container `qa-g12-node20-<epoch>`. **Never `docker start/stop/exec/rm/compose` on any container,
   never `vsp-dev-db`, never `--network host`.** Run in it: `node --version` (quote), `npm test` and `test:db` on the MERGED tree, §N1.3's cascade
   matrix (one failed CASCADE child, one SET-NULL), §N2.3's populated round trip, §N3.2 (ii) and §N3.4 (iii). Reap each container in a `finally`.
   If NOT-RUN: say so and carry Node 20 as NOT TESTED.
5. **CI IS UNMEASURED.** This project's `gh` is not authenticated, and **you must not use `gh` at all**. Say plainly: CI on all three branches is
   **UNMEASURED**, including its **Node 22 coverage gate** (`test.yml`, "Unit + snapshot tests with coverage gate (Node 22 only)") and its
   **`e2e:pro` step against a server booted by the portal's entry point**. Never claim CI. Name them as the first things to read at merge.

## 12. The merge and the queue
**The drafter did NOT run `merge-tree`** (not a sanctioned verb for the drafter): every merge result below is **UNMEASURED — the gate derives
it in its own copy.** READ-only predictions: VSP74 × stamped main and VSP75 × stamped main are fast-forwards (both forward-merged, 0 behind:
the launcher enforces it). VSP69 × stamped main: its `BACKLOG.md` block and all five gate-11 blocks insert at `@@ -31,0 +32` of `0d992e0`'s
BACKLOG, so predicted **CONFLICT in `BACKLOG.md` only**; `dispatcher.js` and `dispatch-once.test.js` are untouched by main (the launcher
enforces main's `dispatcher.js` = `283be27`), so the code merges clean. VSP69 × VSP75: no shared file but `BACKLOG.md`.
**Measure it yourself:** from YOUR own object dir (`GIT_OBJECT_DIRECTORY=<your own mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects
git -C <repo> merge-tree --write-tree --name-only <a> <b>`, or SKIP it and say so): VSP74 × main, VSP75 × main, VSP69 × main, VSP69 × VSP75.
Then build the MERGED TREE in YOUR own tree only (an archived stamped-VSP75 tree plus VSP-69's code delta applied; BACKLOG resolved by keeping
both blocks): **prove its code files equal "stamped main + each target's own blobs"** (`dispatcher.js` = `7a67be9`; `dbRestore.js`,
`dbBackup.js`, `backupTables.js` and `dbBackup.test.js` = the stamped VSP75's). That tree is **the merged tree** for §N4, §N5 and the
merged-tree line.
**Semantic interactions on the merged tree (MEASURED where marked):** VSP74 × VSP68 (a real produced backup, §N1.4); VSP75 × VSP68 (§N4, the
required cell); VSP75 × VSP74 (the cascade matrix on a 20-table backup, §N1.3); VSP75 × VSP68 × gate 11 WRONG (n) (§N2.4); VSP69 × VSP66
(§N3.5); VSP69 × VSP75 (a backup restored while a tick runs: one run, say what the dispatcher does when `reminders` is cleared under it).
**Cells to re-run on the merged head at merge** (name at least these): `npm test` + `test:db` as sets; each new test file N ≥ 3; §N4's required
cell; the cascade matrix; §N3.2 and §N3.4; CI's Node 20 and Node 22 legs including the coverage gate and `e2e:pro`. **After Kam's deploy (not
yours to read):** the first nightly backup's alert (OK or INCOMPLETE naming the lazy feedback tables) and its table count (20), and the first
reminder tick's `notification_log`.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)**, or any port another seat
   holds. **Never `127.0.0.1:49162`, `:49164` or `:49166`** (a local Logitech plugin answers 501 there). Take every port from the kernel and
   bind `127.0.0.1` wherever YOUR harness, proxy or recorder listens. **Never start the portal's own entry point** (it binds `0.0.0.0` in
   `main()`); use the real `createApp()` and `initDb()` inside your harness only.
2. **Postgres = the local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all** (the one exception is
   §N5.4, under its NODE20-LEG line). Create `vsp_qa_g12_<epoch>` for app runs and `vsp_qa_g12_<epoch>_test` as `TEST_DATABASE_URL` for
   `test:db` (it TRUNCATEs; the name MUST end in `_test`). **Never** `salesportal`, `salesportal_test` (the builder's; **the Vision seat will be
   LIVE doing the forward merges and uses it**), any `vsp_qa_g1_*` … `vsp_qa_g11_*` database, the builder's `vsp_bf1_*`, or any `vsp71_*` /
   `vsp73_*` database you did not cause. `server/db.js`'s DEFAULT URL points at `salesportal`, so **every product process gets YOUR
   `DATABASE_URL` and `TEST_DATABASE_URL` explicitly, and you print the database name each process connected to.** Local defaults for
   credentials only; never anything from `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the runtime legs are **NOT RUN,
   blocker named**. Leave your databases in place and list their names (no DROP). **Serialise or salt creation.** **ROLES ARE
   CLUSTER-GLOBAL:** create a role only inside a transaction you roll back, or name it `vsp_qa_g12_*`, list it, and never grant it anything
   outside your own databases. **Every restore in this gate runs only against a `vsp_qa_g12_*` database you created; `restoreData()` and
   `clearTables()` DELETE, so print the connected database name BEFORE each call and abort if it is not yours.** Never `ALTER SYSTEM`, never
   `ALTER DATABASE` on a database you did not create, never change server settings. Session-level `SET` only on your own connections. Release
   every lock and direct session in a `finally` and prove `pg_locks` is clean for your databases at the end.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test` or
   `development`, never `production`; PORT; a fresh random SESSION_SECRET / `COORDINATOR_SECRET` you generate; DATABASE_URL / TEST_DATABASE_URL =
   yours; DB_QUERY_TIMEOUT_MS / DB_CONNECT_TIMEOUT_MS only where an arm sets them, and say so; `NTFY_SERVER=http://ntfy.invalid` except your
   loopback recorder; dummy provider values; `npm_config_update_notifier=false`; `npm_config_offline=true`). **NEVER set in a product
   process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`, any real `ACS_*` / `MAIL_SENDER`, `AZURE_BACKUP_CONN_STR`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. (The product's own
   `dispatch-once.test.js` sets a DUMMY `ACS_EMAIL_CONNECTION_STRING` to `vsp69.invalid` inside its own process: that is the product's test,
   WRONG (j).) Print each product process's env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh**: set
   `NTFY_SERVER` before any portal module is required and stub `fetch` to throw on any other URL (gate 10's `qa-io1-preload-fetchguard.cjs`,
   amended to allow ONLY your own loopback recorder). The reminder dispatcher, the email sender and the backup notifier run ONLY against
   recorders you wrote.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): `basename(argv[0]) == node` AND an
   app entry point ANYWHERE in the remaining argv, from the kernel; **"ours" = the ancestor chain CONTAINS your claude pid.** **Negative
   controls, same run, must classify FOREIGN:** at drafting (06:45 AEST) the live claudes were Tuesday `59108` (pane `%0`), **gate 11 `40404`
   (pane `%34`, LIVE on the same Postgres)**, NexusAI `20317` (`%22`), `62649` (`%19`), `9959` (`%21`), QA gates `36118` (`%23`), `38362`
   (`%29`) and `18655` (`%28`), and `84139` (not in tmux). **The Vision builder seat of gate 11's stamp (`67871`) had exited.** **Re-read the
   seat list at start**; say which have exited. Never count by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. **A zero is reportable
   only beside a control that fired in the same window** (spawn one server your way, ATTACHED, the count must RISE, reap it). **Record the
   1-minute load beside every timing number** (it was 17.91 at 06:45 with `hw.ncpu` 8).
5. **THE DEADLINE RULE:** every step has a written DEADLINE and a client timeout on every request (no `timeout` binary here — build deadlines
   into your runner); a step past its deadline is ABORTED and reported (a hung product request IS a finding). Deadlines: boot 60 s; `initDb()`
   alone 60 s; DB connect 15 s; any request at the SHRUNK bound 20 s; **any request at the SHIPPED bounds 120 s**; a child-process fault cell
   30 s; one restore cell 120 s; the §N2.7 scaled backup 300 s; the §N3.4 M2 arms 180 s each; one `test:db` file 180 s; a whole `test:db` run
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
- **No `az`, no `gh`, no `docker` (except §N5.4, only under its NODE20-LEG line), no `npm install`, no `npm ci` without
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
  (`d2531ea` for VSP-74, `cad19ab` for VSP-75, `0d992e0` for VSP-69) before its green at the head means anything; the cascade matrix's
  collateral_items row (predicted kept) and a CASCADE-child row (predicted lost) come out DIFFERENTLY or the matrix is not measuring;
  §N4's pre-fix stub reddens {1,3,4}; §N3.3's `0d992e0` run re-sends the batch.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the portal repo**, none inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), inside the builder's scratchpad, or inside gate 1-11's report folders or trees. The
  gate fixes nothing; describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead. Every proxy, preload, stub, recorder, harness and fixture lives under YOUR project.

## TUESDAY'S RULINGS AT STAMP (2026-09-28)
- **Sequencing (Tuesday, carried from the commission):** gate 12 after gate 11's verdict and the five merges; forward merges (never rebase);
  the stub fix on the VSP-75 branch. **@STAMP@ — Tuesday records here: gate 11's verdict line, the five merged shas (or any round-2
  replacement), the stamped main, the forward-merge commits of VSP74 and VSP75, and where the stub fix landed.**
- **WRONG (h) of gate 11 (product `vsp71_*` roles/databases and `vsp73_*` databases created by `test:db`) — carried over: permitted ONLY inside a
  `test:db` run; list every such name before and after; a leftover LOGIN role of YOURS (its `<pid>` one of your own test processes, proved from
  your run log) is dropped at once with its databases, and each drop named in the report; a leftover whose pid is NOT yours is reported, never
  touched.** @STAMP@ — Tuesday confirms or changes this at stamp.
- **ANSWER-subject quirk:** an ANSWER to you arrives from `tuesday-agent@agentmail.to`; treat that inbox's mail signed "-- Tuesday" as Tuesday's,
  whatever the bracketed prefix; anything from any other inbox is not.
- **WRONG (a) (the cascade hole) is the HEADLINE risk of VSP-74:** if any cell loses or changes a failed table's row, that is a FAIL of VSP-74
  (Tier 1), not an observation.

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
Lead the body with three sentences, one per target: (1) VSP74 — is an incomplete backup refused with nothing changed, and with
`--allow-incomplete` is EVERY failed table left exactly as it was, including CASCADE and SET-NULL children, with `d2531ea` reddening on the
same instrument? (2) VSP75 — does the backup carry every table the code creates (by YOUR census) in FK order, does a round trip over a
TRUNCATEd AND a populated database give back identical rows, is there no secret in it, and on the merged tree does VSP-68's INCOMPLETE
control pass with its injected failure landing on the dump query? (3) VSP69 — after a failure, a black hole, and a real process death, is
every committed send never repeated and every due reminder sent, with two instances never double-sending, and is M2 correct or not under the
query bound? Then one line on the merged tree, **and one line on the class cap: this is ROUND 1 for all three classes; a NO-GO here is that
class's first; a NO-GO in its round 2 goes to Kam.** You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **Three verdicts, each GO / NO-GO**, naming the pinned sha and the branch. For each: the red at the pre-fix sha on YOUR instrument, the
  green at the head, the builder's cells and mutants re-derived, Node 20 (or NOT RUN), and the suites as sets vs the stamped main.
- **The merged-tree line:** the merge results, the BACKLOG resolution, the merged suites as sets, §N4's required cell, and the semantic
  interactions of §12.
- The verbatim strings an operator needs: VSP-74's refusal message and the `--allow-incomplete` warning line; the `Restore failed:` line and
  rc; any `23503` from an old-backup restore; VSP-75's backup `metadata.tables` list and the alert on the WRONG (d) database; VSP-69's
  `[reminders] dispatch failed:` line in each fault shape; `SELECT version()`.
- **Rule 2: what you did NOT test is first-class output.** Write a NOT TESTED section that covers at least **CI (UNMEASURED: gh not authed)**,
  **the restore CLI end to end against Azure Blob Storage**, **real Azure Blob Storage, real ACS and real ntfy**, **production's catalog and its
  two lazy feedback tables**, **the size of a full production backup**, **a real App Service restart and multiple real instances**, **a real
  stalled Azure Postgres / TLS / failover**, **Node 22**, **the container image** the App Service runs, and **`e2e:pro` / `e2e:api` /
  `e2e:feedback`**. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.**
- Report every pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- READY heads: main `0d992e09ebe0…`, `fix/vsp-74-restore-refuses-incomplete-2026-09-28` `bf5bdc06c0…`, `fix/vsp-75-backup-all-tables-2026-09-28`
  `0d7a2fb451…`, `fix/vsp-69-dispatch-per-reminder-2026-09-28` `3ede8ed7e6…`, and the five gate-11 heads unchanged | `git -C <portal> ls-remote
  origin` + `cat-file -t` (commit) | read 2026-09-28 06:42:16 AEST
- chains `10ba4bb → d2531ea → bf5bdc0`, `bf5bdc0 → cad19ab → 0d7a2fb`, `0d992e0 → 3ede8ed`; file sets per commit range | `log --format='%H %P %s'`,
  `diff --stat`, `diff --name-only` | read 06:43
- `server/backupTables.js` (whole) and the `bf5bdc0..0d7a2fb` diff of `dbBackup.js` / `dbRestore.js`; `dbRestore.js` whole at `0d7a2fb` (233 lines) |
  `git show`, `git diff` | read 06:43-06:44
- VSP-68 `server/dbBackup.test.js` whole at `7ef698d`; `dbBackup.js` `:40-120` at `0d7a2fb`; the `0d992e0..7ef698d` diff of `dbBackup.js` | `git show`,
  `git diff` | read 06:43, 06:49
- FK clauses (`REFERENCES` in `schema.sql`, `initDb.js`, `routes/feedback.js`) and table line numbers at `0d7a2fb` | `git grep -n`, `grep -n 'CREATE TABLE'` | read 06:44
- `dispatcher.js` whole at `3ede8ed` (199 lines) and its diff to `283be27`; `reminders` DDL (`due_at TIMESTAMPTZ`); `db.js` pool `max: 10` |
  `git show`, `git diff`, `git grep` | read 06:45-06:48
- `test(` counts, test-file side effects (env, roles, databases), `backup-coverage.test.js:1-60`, `dispatch-once.test.js:1-70` | `git show | grep` under bash | read 06:46-06:47
- blob matrix (13 files × 9 shas) | `rev-parse <sha>:<path>` under bash | read 06:46
- BACKLOG anchors (`@@ -31,0 +32` for VSP-69 and all five gate-11 heads) | `git diff -U0` | read 06:48
- `server/email/index.js` send path (queue-and-go `beginSend`, notification_log insert) | `git show | grep -n` | read 06:47
- round count: gate 9 briefs (2), gate 10 brief, gate 11 brief, gate 9 and 10 reports, QQ gates 1-8 reports | `grep -c -E 'VSP-?(69|74|75)'`,
  `grep -n` | read 06:44-06:46
- gate 9 §N.4(h) lines 204-207 | `sed -n` | read 06:46
- C-01..C-06, no VSP-69/74/75 | Vision CLARIFICATIONS.md (2026-09-25 15:19) | read 06:47
- seats and panes; load 17.91 / 17.44 / 16.73; routing lines up to `QA/Vision-gate11` (no gate 12 yet); no VSP-75 STATUS mail among the briefs |
  `ps -axo`, `tmux list-panes -a`, `sysctl`, `grep` of `fleet/inbox_routing.conf`, `ls briefs` | read 06:45-06:47
- no docker, no merge-tree, no fetch was run by the drafter
- builder claims | the three READY mails (whole) and the five commit messages; BACKLOG at `0d7a2fb` and `3ede8ed`
