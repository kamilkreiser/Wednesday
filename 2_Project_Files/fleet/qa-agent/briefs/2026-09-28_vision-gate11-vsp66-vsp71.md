# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 11: FIVE targets on portal main `0d992e0` — VSP-66 (held-client link death, TIER 1), VSP-71 (session index cannot fail a boot, TIER 1), VSP-70 (restore throws the first error, TIER 2), VSP-68 (backup INCOMPLETE alert, TIER 2), VSP-73 (backup-db dump replays into a fresh DB, TIER 2)

**Drafted for Tuesday on 2026-09-28 at 06:13-06:4x AEST by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
**The file name says "vsp66-vsp71" because the commission fixed it before VSP-70, VSP-68 and VSP-73 were added (Tuesday, 06:16, 06:19 and
06:25). The gate has FIVE targets. Tuesday: "The READY list is now closed at five."**
The builder's five READY mails (on disk, each read whole by the drafter):
- VSP-66: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp66-READY-mail.txt` (dated 2026-09-27T20:06:33Z)
- VSP-71: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp71-READY-mail.txt` (dated 2026-09-27T20:11:54Z)
- VSP-70: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp70-READY-mail.txt` (dated 2026-09-27T20:14:18Z)
- VSP-68: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp68-READY-mail.txt` (dated 2026-09-27T20:17:10Z)
- VSP-73: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp73-READY-mail.txt` (dated 2026-09-27T20:20:26Z)
**Every builder statement below comes from those mails, the six new commit messages or the BACKLOG at each head. Each one is a CLAIM.**
**The five READYs landed within about 15 minutes of each other (20:06-20:20Z), the first about 5 minutes after the builder seat booted (Tuesday: the seat's plan mail was at 20:02Z; the drafter did not see that mail).** Each fix was built, red-proved, mutated and set-counted inside a few minutes. **Every red, every mutant and every suite set in this brief must be RE-DERIVED by the gate. None is taken from a READY.**
**The drafter read all six rows from `git ls-remote origin` at 2026-09-28 06:13:49 (main, VSP-66, VSP-71), 06:16:16 (VSP-70), 06:19:14 (VSP-68) and 06:25:30 AEST (VSP-73). `cat-file -t` = commit for every head.**
The launcher parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 06:36
Self-check note: read whole by Tuesday at stamp; the drafter's WRONG list (a)-(w) read first; rulings at stamp below; pins re-read by ls-remote at stamp.

NODE20-LEG: DOCKER-PULL-NEVER
<!-- Set by Tuesday's commission ("the NODE20-LEG line (DOCKER-PULL-NEVER)"). The launcher refuses anything but NOT-RUN | DOCKER-PULL-NEVER.
     The drafter did NOT run docker: "node:20 is present" rests on gate 10's own `docker image inspect` (report §N.7,
     `sha256:8f693eaa7e0a8e71560c9a82b55fd54c2ae920a2ba5d2cde28bac7d1c01c9ba5`, linux/arm64). Re-prove it (§N5.4). -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build any of these changes and you owe the builder nothing. **Every line below that reports what the builder says
is a CLAIM, never evidence.**

**One gate, FIVE targets, FIVE verdicts (GO / NO-GO each, at its pinned sha), plus ONE merged-tree line.**
- **VSP66** at `1976275` — **TIER 1.** It changes `server/db.js` `guard()`, which EVERY pool checkout in the live portal passes through
  (the six `pool.connect()` holders and every `pool.query()`). Both failure directions are in scope: a link death that still kills the
  process, AND a healthy checkout that now misbehaves (a stacked or leaked listener, a dead client handed out again, a log flood).
- **VSP71** at `5bdaeae` — **TIER 1.** It changes `server/schema.sql` and `server/initDb.js`, which run at EVERY boot of the live portal.
  Both failure directions are in scope: a boot that still fails on a missing index, AND a boot that now does something new on a
  healthy production-shaped database (a lock wait, a leaked `lock_timeout`, a warning that fires where nothing is wrong).
- **VSP70** at `10ba4bb` — **TIER 2 (Tuesday's ruling; the builder self-graded "Tier 3").** Why: it changes only how a restore FAILURE is
  REPORTED, not what the restore deletes; the data-destruction path is unchanged. **§N3.1 names the lines that prove "unchanged".**
- **VSP68** at `7ef698d` — **TIER 2 (Tuesday's ruling).** Why: the change is an internal alert (the nightly backup's ntfy notice and its blob
  metadata); no client-facing effect.
- **VSP73** at `6d7ea73` — **TIER 2 (Tuesday's ruling).** Why: an admin-only download (`GET /api/admin/backup-db`, `datasec_admin`). It
  changes what the dump CONTAINS (sequences, indexes, `OWNED BY`), and so what a replay of it builds.
  **The dump carries customer data from the gate's OWN seeded database only. Never read, open or keep a real dump.**
- **MERGED TREE:** all five × main, one line: which merges are clean, which conflict and where, and the suites as sets on the merged tree.

**⚠ Names, written out every time:**
- **VSP66 = Jira VSP-66 = gate 9's VSP65-O1** (Major, pre-existing): a link death while a `pool.connect()` caller holds its client raised
  `uncaughtException: Connection terminated unexpectedly` and the portal exited.
- **VSP71 = Jira VSP-71 = gate 10's VSP65-R2-O1** (Minor): with `IDX_session_expire` missing, the guarded `CREATE INDEX` failed the boot
  (a) 42501 when the boot role does not own `session`, (b) `DB_QUERY_TIMEOUT` when a write on `session` was held past the bound.
- **VSP70 = Jira VSP-70 = gate 9's §N.4(c)** (Minor, pre-existing): dbRestore's ROLLBACK error replaced the error that failed the restore.
- **VSP68 = Jira VSP-68 = gate 9's §N.4(b)** (Minor, pre-existing): a backup missing a whole table was announced "DB Backup OK".
- **VSP73 = Jira VSP-73 = gate 10's VSP65-R2-O7 / §N.3(b)** (pre-existing): the backup-db SQL dump cannot replay into a fresh database
  (`42P01` on a sequence) and carries `session` without its index (VSP-71's only reachable route).

Branches, all **one or two commits on portal main `0d992e0`**, **none on main**:
`fix/vsp-66-checkout-link-death-2026-09-28` (1), `fix/vsp-71-session-index-boot-2026-09-28` (1),
`fix/vsp-70-restore-rollback-error-2026-09-28` (2: refactor `12138cb`, then the fix `10ba4bb`), `fix/vsp-68-backup-missing-table-2026-09-28` (1),
`fix/vsp-73-backup-dump-replay-2026-09-28` (1).

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`,
  dated 2026-09-25 15:19): read it whole. **C-01..C-06. No C-entry covers VSP-66, VSP-68, VSP-70, VSP-71 or VSP-73** (drafter READ 06:17:
  zero case-insensitive matches for the five ids).
- **PRODUCTION IS LIVE for this project.** `datasec-sales-portal-rg` holds the live site `https://datasec-sales-portal.azurewebsites.net`,
  its production Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault `datasec-sales-kv`. Production runs Node 20
  (`.github/workflows/test.yml`, READ at gate 10). **VSP-66 and VSP-71 change code every production request and every production boot run.**
  **Nothing in this gate touches production** (§13, HELD).
- **Main `0d992e0` is gate 10's GO'd VSP-65 round-2 head, now main by fast-forward** (READ: `ls-remote` main = `0d992e0`; its single parent
  is `b5c3e8d`). Gate 10's GO was a statement about `0d992e0` as a branch head; this gate uses it as the BASE.
- **Tuesday's tier rulings (above) are Tuesday's, not Kam's.** No product choice in any target is Kam's ruling. Report each as the BUILDER's
  choice and say whether it needs Kam: VSP-66's log-once-per-checkout and its log text; VSP-71's `WHEN OTHERS` catch-all, the 2 s
  `lock_timeout` value, and the choice to keep the index in `schema.sql` rather than `initDb.js`; VSP-70's `release(broken)`; VSP-68's
  third alert level (priority 4, "INCOMPLETE"), its body text, and still uploading a partial backup; VSP-73's choice to emit indexes (not
  FOREIGN KEY / CHECK constraints or typmods) and to emit them AFTER each table's rows.
- **OUT OF SCOPE, RULED by Tuesday, and NOT misses (name them so you do not grade them):** the VSP-68 READY's **F-A** (the backup omits
  most PRO tables, including `quotes`) and **F-B** (a restore EMPTIES a live table whose dump failed and puts nothing back). Both are
  ruled and will be separate tickets in a later gate (the VSP-73 READY: "F-B is next, stacked on 10ba4bb, then F-A"). Both sit in VSP-68's
  BACKLOG entries at `7ef698d`. **Do not measure them. If your work touches their shape, say so in one line and move on.** Also out of
  scope: VSP-73's "NOT FIXED" list (FOREIGN KEY and CHECK constraints, column typmods, still absent from the dump). Record whether a
  replayed database differs from its source only in those, and do not grade them.
- **Deploys are HELD for Kam. Nothing merges on your word.** A merge is Tuesday's GO on a pinned head. A deploy is Kam's word.

## PRIOR ROUND
PRIOR ROUND: none of these five targets has been gated before. Each is the FIRST round of its class. Their origin findings come from gates 9 and 10.
**ITS REPORT IS ON DISK AT:** gate 10 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2`
(`report.md`, 464 lines, verdict GO at `0d992e0`) and gate 9 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge`
(`report.md`, 544 lines, verdict NO-GO at `2adfc4a`, superseded by gate 10).
**Read whole:** gate 10's VERDICT, VERBATIM OPERATOR STRINGS, §N.2 (c) and (d), §N.3 (b), §N.5, FINDINGS INDEX, THE QUEUE, NOT TESTED,
Self-findings and "Floor, instruments, databases". Gate 9's §N.3 table (S1-S8), §N.4 (b) and (c), FINDINGS INDEX (VSP65-O1 at
lines 428-434), and its self-findings.
Origin findings, each a CLAIM until you measure it:
- **VSP65-O1 → VSP-66.** Gate 9 measured it with its **S7b** arm (the link RST WHILE the generate route holds its stalled client): HEAD 2/2
  and MAIN 2/2 `uncaughtException` (`evidence/vsp/HEAD-s7b-shrunk.txt`, `MAIN-s7b-shrunk.txt`). Gate 10 re-ran **S7** (late RST after the
  discards: 0 uncaught) but not S7b. Gate 9's fix-shape: "attach an `'error'` listener for the checkout's lifetime in `BoundedPool.connect`".
  The builder chose exactly that shape.
- **VSP65-R2-O1 → VSP-71.** Gate 10 §N.2(c) cell (4) (`session` owned by another role, index missing): REJECTED 42501 at the head, RESOLVED at
  main. §N.2(d) d2 (index missing, boot owns `session`, ROW EXCLUSIVE held 45 s): REJECTED `DB_QUERY_TIMEOUT` at 30,002 ms, and **the
  abandoned boot transaction later COMMITTED the index** (VSP65-R2-O4). Gate 10's fix-shape: catch `insufficient_privilege` and
  `lock_not_available` / the timeout around the index, warn and continue. Its two regression cells: "index missing, boot role not the owner:
  resolves and warns"; "index missing, a write open for bound + 5 s: resolves".
- **§N.4(c) → VSP-70.** Gate 9 READ this path and did not run it: "The ROLLBACK after a timeout on the same stalled client times out as well,
  30 s later, and its error replaces the first. **Both errors are `DB_QUERY_TIMEOUT`, so only the failing statement's identity is lost.**"
- **§N.4(b) → VSP-68.** Gate 9 MEASURED it: with `SELECT * FROM leads` black-holed, `runBackup()` returned in 1.6 s with `leads: {rowCount: 0,
  error: "DB_QUERY_TIMEOUT: …"}`, the recorder received an upload of "11 rows", **and the notifier received title "DB Backup OK"** (gate 9
  report line 187).
- **VSP65-R2-O7 / §N.3(b) → VSP-73.** Gate 10 MEASURED it through the real route (a 200 zip of 8,259 B from its own DB): (i-A) replayed as ONE
  query into a fresh DB it fails at once, `42P01 relation "collateral_items_id_seq" does not exist`; (i-B) statement by statement, 7 of 115
  statements succeed, and `session` is created WITHOUT its index and without the `(6)` typmod. The dump contained no `CREATE INDEX` at all.
  Gate 10's evidence: `evidence/census/n3-run.txt`; its instrument `qa-g10-n3.cjs`. VSP-71's READY argues from this route (§N2.5).
- **Self-findings from gates 2-10 bind you:** quote every path (the project path has a space and a `!`); run every loop and every
  `git show <sha>:<path>` under **bash, not zsh** (the drafter hit TWO zsh traps in this draft: an unquoted list not word-split, and
  `$A:s…` read as a zsh history modifier, which silently printed the wrong object); never detach a control server; **the portal test-DB name
  MUST end in `_test`**; npm's update-notifier egresses unless you disable it; record the load average beside every timing number (**a
  latency result with no load figure is not a measurement**); never count "reused / not reused" by bytes (use backend pid + pool counters,
  gate 9 self-finding); a spawnSync launcher blinds your own observers (gate 10 self-finding 3); backend pids by `client_port` come back
  null through Docker's NAT (use `client.processID` + `pg_stat_activity`, gate 10 self-finding 4); a harness that counts rows in a table that
  may not exist must tolerate its absence (gate 10 self-finding 1).
- **PRIOR WORK: verify every claim against git history and gates 9/10's evidence, never against this brief.**
- **Instruments are REUSED BY COPY from gate 10's `evidence/tools/`** (the newest copies; they already carry gate 9's arms):
  `qa-g10-stallproxy.cjs` (the `allowHalfOpen: true` hold / blackhole / oneway / cut / drip / tellpg proxy, a separate child process; rules
  support `once` and `armNext`; its only kill verb is `{cmd:'rst'}` = `resetAndDestroy` on the app-facing socket),
  `qa-harness-g10-vsp.cjs` (arms S1 … S8, **S7 at `:118-125`, S7b at `:129-145`**, burst, bootddl, discard, ctl, …), `qa-g10-lib.cjs`,
  `qa-harness-g10-schema.cjs`, `qa-g10-sql.cjs`, `qa-g10-sqlcheck.cjs`, `qa-g10-n2c.cjs`, `qa-g10-n2d2.cjs`, `qa-g10-n3.cjs`, `run-arm.sh`,
  `run-node20-g10.sh`, `run-suite.sh`, `mktree-portal.sh`, `mutate-vsp.py`, `mutate-r2.py`, `qa-mkdb.cjs`, `qa-dbcheck.cjs`,
  `qa-floorcount.py`, `qa-harness-floorctl.mjs`, `qa-io1-preload-fetchguard.cjs`, `qa-io1-preload-hidelayer.cjs`, `qa-run.py`,
  `lockcmp.py`, `lockwalk.py`, `specsets.py`, `tapsets.py`. **COPY what you use into this gate's own `evidence/tools/`, read it before you
  trust it, and RE-POINT every hard-coded gate-10 path** (drafter READ: `qa-harness-g10-vsp.cjs:15` and `qa-mkdb.cjs:24-25` ENFORCE the
  `vsp_qa_g10_` prefix; `qa-mkdb.cjs:7` and `mktree-portal.sh:6` hard-code `work-g10`; `run-arm.sh` names gate 10's paths). **Never edit,
  run from, or write into gate 1-10's copies, evidence, trees or databases.** Record the sha1 of each copy before and after your edits.
  **Gate 10's roles `vsp_qa_g10_boot` / `vsp_qa_g10_other` are still in the cluster (left in place by gate 10): never use, alter or drop them.**

## PIN — HEADS (PRE-FILLED BY THE DRAFTER; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head; every target row has a 40-hex base, a commit count and no `@`; the
head is a commit in the repo; the base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git
ls-remote origin refs/heads/<branch>` equals the head NOW; no target is on main. **Every target is off main and none is stale:**
`merge-base(<head>, 0d992e0) = 0d992e0` for all five; `rev-list --left-right --count 0d992e0...10ba4bb` = `0 2` (READ 06:16).
**Gated anchors (the launcher checks them):** main `0d992e0` has exactly one parent `b5c3e8d` (gate 10's GO'd head, fast-forwarded);
VSP70's `head~1` is exactly the refactor `12138cb`, whose parent is `0d992e0`.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | - | - | IN |
| VSP66 | portal | fix/vsp-66-checkout-link-death-2026-09-28 | 1976275635185db4551d5e3b015a66971f4563a5 | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | 1 | IN |
| VSP71 | portal | fix/vsp-71-session-index-boot-2026-09-28 | 5bdaeae6e28e280be380042a3dc8a56dbada0293 | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | 1 | IN |
| VSP70 | portal | fix/vsp-70-restore-rollback-error-2026-09-28 | 10ba4bbd29e34bf601426b68328f63725e228a86 | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | 2 | IN |
| VSP68 | portal | fix/vsp-68-backup-missing-table-2026-09-28 | 7ef698d7e8c00c4c8e87060bec9f5284dfe8082a | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | 1 | IN |
| VSP73 | portal | fix/vsp-73-backup-dump-replay-2026-09-28 | 6d7ea736b4f718cddd2e152f1ee0234d42d97bfe | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | 1 | IN |
<!-- PIN-HEADS:END -->

Repo: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`). **The portal has no CLAUDE.md of its own inside the repo;** its rules are
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (read it; its deploy commands are NOT for you).

**The shape at drafting (READ 06:13-06:2x):**
- **VSP66 (`0d992e0..1976275`), 4 files:** `BACKLOG.md` (+6), `server/db.js` (+20/-1: `0d402a0` → `5d42db6`; `guard()` gains
  `onHeldError` at `:106-112` and a release that removes it at `:114-117`), `test/db/checkout-link-death.test.js` (new, 6 `test(`),
  `test/db/checkout-link-death.child.js` (new, not `*.test.js`). Tree `5d4f6ef6…`.
- **VSP71 (`0d992e0..5bdaeae`), 5 files:** `BACKLOG.md` (+7), `server/schema.sql` (+16/-2: `c076d90` → `74f6e9c`; the session DO block at
  `:287-299`, **the last statement of a 299-line file**), `server/initDb.js` (+7: `e1ccf0f` → `68fc8cc`; the missing-index check at
  `:9-15`), `test/db/session-index-boot.test.js` (new, 5 `test(`), `test/db/session-index-boot.child.js` (new). Tree `f5bbfe62…`.
- **VSP70 (`0d992e0..10ba4bb`), 3 files:** `BACKLOG.md` (+6), `server/dbRestore.js` (`9878f3d` → `6f9152a` at `12138cb` → `5f4b71d` at
  `10ba4bb`), `server/dbRestore.test.js` (new, UNIT suite, 4 `test(`, a scripted fake client). `12138cb` changes `server/dbRestore.js`
  only. Tree `397947fd…`.
- **VSP68 (`0d992e0..7ef698d`), 3 files:** `BACKLOG.md` (+18: VSP-68's entry AND the F-A / F-B entries), `server/dbBackup.js`
  (`5e0cfbe` → `5e31eb4`), `server/dbBackup.test.js` (new, UNIT suite, 5 `test(`, `db`, blob SDK and `fetch` stubbed). Tree `f726694d…`.
- **VSP73 (`0d992e0..6d7ea73`), 3 files:** `BACKLOG.md` (+7), `server/routes/admin.js` (+30, additions only: `e1abcde` → `7b00469`; sequences
  at `:115-128`, per-table indexes at `:154-165`, `OWNED BY` at `:186-187`; `getTableDDL()` `:39-74` unchanged), `test/db/backup-dump-replay.test.js`
  (new, 4 `test(`; it creates and drops database `vsp73_<pid>`). Tree `788cbdc8…`.
- **Same blob at main and ALL FIVE heads:** `package.json` (`d3b76fb`), `package-lock.json` (`9d426df`), `.github/workflows/test.yml`
  (`0cb2d05`), `server/errors.js` (`c0c4b0e`), `server/index.js` (`cdc5911`), `test/db/helpers.js` (`1d90638`), `scripts/run-db-tests.js`
  (`c48966c`), `scripts/ensure-test-db.js` (`9f8bf0b`), `test/db/pool-timeout.test.js` (`f0a4b00`), `server/reminders/dispatcher.js`
  (`283be27`), `server/routes/quotes.js` (`7b95ab6`). `server/routes/admin.js` is `e1abcde` at main and every head except VSP73.
  **No target touches a file another target touches, except `BACKLOG.md`.**
**A GO is a statement about the pinned SHA only.** If a head moves, that target's verdict expires.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READYs — found by the drafter (verify each; all are claims)
- **(a) VSP-66: "It logs one line per death" is not what the code guarantees (READ; measure it).** The `told` flag is per CHECKOUT (a closure
  in `guard()`, `server/db.js:106-112` at `1976275`), and the listener is removed at release (`:115`). pg-pool's `_release` re-attaches
  its OWN idle listener before it discards a dead client (`node_modules/pg-pool/index.js:349`, 3.11.0), and that listener emits on the
  POOL, which `pool.on('error')` logs as `[db] idle client error (the pool will replace it)` (`db.js:151-153`). So if pg's second emit
  lands AFTER the holder has released, the death produces one `held` line AND one `idle client error` line. **The builder's assertion
  counts only `/\[db\] .*held/` lines** (`checkout-link-death.test.js:50`) and is blind to the second kind. Count EVERY `[db]` line per
  death, per shape.
- **(b) VSP-66: "The dead client is not reused: pg sets `_queryable=false`" has a window on the IN-FLIGHT shape (READ; measure it).** When the
  backend is terminated while a query is active, pg hands the FATAL to that query (`_handleErrorMessage`, `pg/lib/client.js:393-405`, pg
  8.18.0) WITHOUT setting `_queryable = false`. It becomes false only when the socket's `end` arrives (`client.js:176-195` → `_handleErrorEvent`
  `:384-390`). A holder that releases straight after its query rejects, with no further query, can release a dead but still-"queryable"
  client with no error. pg-pool's discard test (`pg-pool/index.js:356`) then fails, and the client goes back IDLE. The builder's child
  waits 500 ms before the next step (`checkout-link-death.child.js:156`), so it cannot see the window. **Whether the window is reachable
  from a real caller is the question "does the dead client ever get reused?" — §N1.2.**
- **(c) VSP-66: the commission's "gate 9/10's own S7/S7b instruments" — S7 and S7b are gate 9's arms, carried into gate 10's copy
  (`qa-harness-g10-vsp.cjs:118-145`). Neither has a TERMINATE or a FIN shape.** The proxy's only kill verb is `rst` (`qa-g10-stallproxy.cjs`
  IPC, `resetAndDestroy`). You must ADD `pg_terminate_backend` (over a separate direct connection) and FIN (`end()` on the app-facing socket)
  shapes. **Also: S7b IS a real-caller cell** (the generate route, `server/routes/quotes.js:262`, holding its client in a `FOR UPDATE`
  transaction), so the READY's first NOT TESTED line ("an end-to-end route cell with a real caller holding the client") is partly covered by
  re-running S7b at the head.
- **(d) VSP-66 READY: "Gate 10's S7b harness and stall proxy were read, not copied" — nominally right** (the S7b arm is in gate 10's copy), but
  the builder's in-child proxy (`checkout-link-death.child.js:107-118`) is a plain `net.createServer` pipe that destroys the Postgres side
  when the app side closes, so on its RST and FIN cells **Postgres is told**. That is not gate 9's "never tell Postgres" shape.
- **(e) VSP-71 READY NOT TESTED: "Restoring the lock_timeout after the block: no cell can see it, because the block is the last statement"
  — half right (READ; measure it).** It IS the last statement (`schema.sql` has 299 lines; `END $$;` is `:299` at `5bdaeae`). But
  `set_config('lock_timeout', …, true)` is TRANSACTION-local, and `initDb()` runs the whole file as ONE implicit transaction (gate 10 §N.2(d)
  d4 measured the whole-file rollback). So the restore line at `:297` may not be load-bearing at all, and a cell CAN see a leak: read `SHOW
  lock_timeout` on the SAME backend after `initDb()` (a pool of `max 1`). **The commission is right that a leaked `lock_timeout` would change
  every later statement in the boot.** Prove the probe can see a leak with a mutant (`is_local` = `false`), then measure the head (§N2.3).
- **(f) VSP-71: the gates' usual SHRUNK bound (`DB_QUERY_TIMEOUT_MS=1500`) is UNDER the new 2 s `lock_timeout`.** At 1,500 ms the held-write
  cell is PREDICTED TO FAIL THE BOOT (the READY's own first NOT TESTED line). **Do not run (b) at 1,500 and expect a green.** Run (b) at the
  builder's 6,000, at the SHIPPED 30,000, and at 1,500 as the named residual (quote it). Also at exactly 2,000.
- **(g) VSP-71: `WHEN OTHERS` does not catch everything (READ).** In PL/pgSQL, `WHEN OTHERS` does not trap `query_canceled` (57014) or
  `assert_failure`. A `statement_timeout` or `pg_cancel_backend` during the `CREATE INDEX` still fails the boot. The portal sets no
  `statement_timeout` (gate 9), so locally this needs a deliberate cancel. Measure one, and say whether production could produce one
  (READ ONLY: an Azure server-level `statement_timeout` is unknown).
- **(h) VSP-71: its test:db cells create CLUSTER-GLOBAL LOGIN roles and databases outside the gate's naming (READ; a floor question for
  Tuesday at stamp).** `test/db/session-index-boot.test.js:26-50` creates roles `vsp71_<pid>_owner` (NOLOGIN) and `vsp71_<pid>_boot` (LOGIN,
  **fixed password `'vsp71'`**), and `:57-59` creates databases `vsp71_<pid>_<cell>` as the superuser. Its `after()` drops them (`:97-107`).
  A run killed before `after()` leaves a LOGIN role with a known password on the shared cluster. **Every `test:db` of a tree that contains
  VSP-71 does this** (the VSP71 tree and the merged tree). **VSP-73's new test does the same with one DATABASE, `vsp73_<pid>`**
  (`test/db/backup-dump-replay.test.js:23,81,89`; no role). See §13.2 for the default the drafter wrote and TUESDAY'S RULINGS for the ruling.
- **(i) VSP-70 READY: "12138cb refactor, no behaviour change" — one behaviour changed (READ; harmless, still name it).** At `0d992e0`
  `server/dbRestore.js:185-188` called `main()` on REQUIRE, and `main()` exits 1 without `AZURE_BACKUP_CONN_STR`. At `12138cb` the call is
  guarded by `require.main === module`, and the file exports `clearTables` and `RESTORE_ORDER`. That is what lets the unit suite load it.
  The comment "Disable FK checks by deferring constraints" was also removed. **This is also why the red must be re-derived at `12138cb`,
  not `0d992e0`: at `0d992e0` there is no `clearTables` to call.**
- **(j) VSP-70: the `pool.connect()` census changes shape.** At `10ba4bb` the restore's checkout is `db.connect()` inside `clearTables(data,
  db = pool)` (`dbRestore.js:110`). A literal `pool.connect()` grep at `10ba4bb` finds FIVE holders, not six. VSP-66's BACKLOG and cells
  name six. On the merged tree the sixth holder is `clearTables` (§12).
- **(k) VSP-70: `release(broken)` may change nothing on a real link (READ; measure it).** On a DEAD link the ROLLBACK rejects with `_queryable`
  already false, so pg-pool discards the client anyway (`pg-pool/index.js:356`). On a TIMED-OUT link `guard()` passes `client[TIMED_OUT]`, so
  it is discarded anyway. The only shape where `release(broken)` changes the outcome is a ROLLBACK that fails while the connection stays
  queryable, and the READY names no real shape for it. **The builder's M1 red exists on the fake client only.** Say whether any real shape
  reddens M1.
- **(l) VSP-70 / gate 9: on the natural stalled-link shape both errors are `DB_QUERY_TIMEOUT` with IDENTICAL text** (gate 9 §N.4(c)). A
  real-Postgres cell that black-holes the DELETE cannot tell by message which error was thrown. **§N3.3 prescribes a shape that can.**
- **(m) VSP-68: a table-dump failure whose `err.message` is EMPTY is still announced OK (READ; measure it).** `failed_tables` is
  `Object.keys(tables).filter(t => tables[t].error)` (`dbBackup.js:71`), and `tables[t].error` is set only `if (dump.error)` (`:60`), from
  `err.message` (`:49`). An error with `message === ''` (Node's `AggregateError` for a refused multi-address connect is one known source)
  is falsy at both points, so that table is listed as dumped with 0 rows and the alert says OK. Measure it.
- **(n) VSP-68: a FRESH database produces "INCOMPLETE" on its first backup (READ; a legitimate-shape question).** VSP-68's own BACKLOG says
  "On a fresh database the boot-time backup always misses `feedback`, which the feedback routes create lazily" (`routes/feedback.js:19-58`,
  `CREATE TABLE IF NOT EXISTS feedback` at `:25`; `schema.sql` does not create it). So the first backup after a fresh deploy, or on any
  database where nobody has submitted feedback, now raises a priority-4 alert naming `feedback (relation "feedback" does not exist)`. Rule
  whether that is a true alarm or noise (§2a). Production's `feedback` table: NOT TESTED.
- **(o) VSP-68 test sets `AZURE_BACKUP_CONN_STR` itself** (`server/dbBackup.test.js:17`, `'UseDevelopmentStorage=true'`), with the blob SDK
  stubbed through `require.cache` (`:34-48`). That is the product's unit test, not your process env. It is dummy and loopback. Say so, and
  prove the stub was in place (no socket to `127.0.0.1:10000`).
- **(p) Merge: the commission said "both touch BACKLOG.md". With five targets, ALL FIVE insert at the SAME anchor** (`@@ -31,0 +32` in every
  `git diff -U0 0d992e0 <head> -- BACKLOG.md`). **The drafter RAN `merge-tree` in its own object dir:** each head × main is CLEAN, and ALL TEN
  pairs CONFLICT in `BACKLOG.md` only (§12). **No code file is touched by two targets.**
- **(t) VSP-73: "IF NOT EXISTS makes a replay over an existing schema a no-op" (`admin.js:156-157` comment) is not true for every replaying
  role (READ; measure it).** Gate 10 MEASURED on this server (PostgreSQL 16.15) that `CREATE INDEX IF NOT EXISTS` checks table OWNERSHIP
  BEFORE existence: a non-owner gets `42501 must be owner of table …` even when the index exists (gate 10 VERBATIM STRINGS, §N.2(c)). So a
  replay over an existing schema by a role that does not own the tables now fails on the FIRST emitted index (as one query, the whole replay
  rolls back), where before VSP-73 it reached the INSERTs (and collided 23505, the READY's NOT TESTED). Measure it, and rule its reach.
- **(u) VSP-73: the emitted index DDL is `pg_indexes.indexdef` rewritten by one regex** (`admin.js:163`,
  `/^CREATE (UNIQUE )?INDEX /` → `CREATE $1INDEX IF NOT EXISTS `). `indexdef` is schema-qualified (`ON public.<table> USING btree …`). The
  primary-key index is emitted too (predicted a no-op, because `getTableDDL()` names no constraint and Postgres's default `<table>_pkey` then
  matches). Partial indexes keep their `WHERE` (e.g. `uq_quotes_poc_credit_once`, `initDb.js:94-97`). **Measure: the index set of a replayed
  DB equals the source's by `pg_get_indexdef`, and any index whose name does NOT match (a PK constraint with a non-default name) becomes a
  SECOND, duplicate unique index.**
- **(v) VSP-71's READY calls VSP-73 "next-but-two in the queue"; it is now a target of this same gate**, and VSP-73's READY states the
  interaction ("VSP-71 stops a session-without-index from failing the boot. VSP-73 stops the dump from producing that shape"). Tuesday's
  requirement: measure on the MERGED tree that a replayed dump + a boot gives the index and no warning (§N6.4).
- **(w) VSP-73 changes `server/routes/admin.js`, the route VSP-66's end-to-end backup-db cell (§N1.3) drives.** At `1976275` the route is
  `e1abcde` (the old dump). On the merged tree it is VSP-73's `7b00469`, which runs more queries while holding the client. Run §N1.3's
  backup-db cell on the merged tree as well.
- **(q) VSP-66 READY "No earlier branch or commit touched the held-client listener (git log --all)":** the local `git log --all -S onHeldError`
  lists only `1976275`. That is consistent, but it covers local refs only, and the drafter did not fetch.
- **(r) VSP-71 READY "Postgres's WARNING never reaches the app log" — consistent at source (READ):** pg emits `notice` (`client.js:504`), and
  nothing in `server/db.js` listens for it. Measure it.
- **(s) UNVERIFIABLE by design, and you must not try:** production's `session` owner and index, its Postgres version and `search_path`,
  its `feedback` table, an Azure server-level `statement_timeout` / `lock_timeout`, a real Azure failover, real Blob Storage, and real ntfy.
  **Carry each as NOT TESTED.**
- **Verified TRUE at source (READ):** all six heads by `ls-remote`; the file sets above; the six holders at `0d992e0`
  (`server/routes/quotes.js:262`, `server/routes/admin.js:93`, `server/reminders/dispatcher.js:121`, `server/seed.js:18`,
  `server/seedCollateral.js:13`, `server/dbRestore.js:149`) and unchanged at VSP66, VSP71, VSP68 and VSP73; `test(` counts VSP66 6, VSP71 5,
  VSP70 4, VSP68 5, VSP73 4 (matching "105 + 4", "105 + 5" and the db tallies); `dbBackup.js` and `dbRestore.js` each have one prior commit
  (`96a5ff3`); `dbBackup` is required only by `server/index.js:23` and its own test; `sendNotification` is not exported; `admin.js`'s last
  change before VSP-73 is `992da21` (IO1 round 2), and VSP-73's diff to it is additions only (`getTableDDL()` untouched).

## THE READYs — their FIX, CELLS, RED-PROOFS, PRIOR WORK and NOT TESTED (the gate rules on every claim)
The five READYs are on disk (paths at the top); read each whole. Their NOT TESTED lines are carried VERBATIM here (the launcher checks it):

VSP-66 NOT TESTED
- An end-to-end route cell with a real caller holding the client (e.g. dispatchDue awaiting sendEmail inside its transaction, or backup-db streaming). The cells drive the checkout that all six callers use, not the callers themselves.
- A half-open link with no FIN or RST: VSP-65's query bound covers that, and it is not re-measured here.
- Node 20 (CI's runtime): CI is UNMEASURED per vision-gh-login-for-ci. Local run was Node 26.8.1 only.
- Production/Azure Postgres: not touched.

VSP-71 NOT TESTED
- A DB_QUERY_TIMEOUT_MS at or under 2000 ms: the query bound would beat the 2 s lock_timeout and (b) would fail the boot again. The shipped default is 30,000.
- An index build that itself takes longer than the bound on a very large session table (gate 10 flagged the SHARE lock during the build). Not measured.
- Restoring the lock_timeout after the block: no cell can see it, because the block is the last statement in the file, so nothing runs after it in that transaction.
- Node 20 / CI (UNMEASURED), production and Azure (not touched).
- A real App Service restart.

VSP-70 NOT TESTED
- A real stalled or dead Postgres under clearTables. The cells use a fake client. A real-link cell on this branch would also hit VSP-66's crash, since a held client whose backend dies throws uncaught until VSP-66 merges.
- The restore CLI end to end (it needs Azure blob storage; not touched).

VSP-68 NOT TESTED
- Real Azure Blob Storage and a real ntfy server (both recorded). Azure accepts the blob metadata key failedTables in the SDK's shape, but it was not uploaded for real.
- Real Postgres under the backup (the query is stubbed); gate 9 measured the real black-hole path.
- Node 20 / CI: UNMEASURED.

VSP-73 NOT TESTED
- Replaying over an EXISTING populated database (INSERTs collide with 23505, as before).
- Production-size dumps, Node 20 / CI (UNMEASURED), production (not touched).

**The READYs' red-proof claims, in one line each (each a CLAIM, re-derived in §N):**
- VSP-66: at `0d992e0` failing {2,3,4,5,6}, passing {1}; at `1976275` 6/6 ×3; M1 (no removeListener) failing {1,3,4,5,6}; M2 (no log-once)
  failing {3,5}; M3 (no listener) failing {2,3,4,5,6}.
- VSP-71: at `0d992e0` failing {3,4,5} (cell 3: 42501 at 96 ms; cells 4-5: `DB_QUERY_TIMEOUT` at 6,019 ms), passing {1,2}; at `5bdaeae` 5/5 ×2;
  M1 (no lock_timeout) failing {4,5}; M2 (no exception block) failing {3,4,5}; M3 (no initDb warning) failing {3,4}.
- VSP-70: at `12138cb` failing {3,4}, passing {1,2}; at `10ba4bb` 4/4; M1 (release() with no error) failing {4}; M2 (no ROLLBACK log line) failing {3}.
- VSP-68: at `0d992e0` failing {3,4,5}, passing {1,2}; at `7ef698d` 5/5 ×2; M1 (alert always ok) failing {3}; M2 (no blob marker) failing {4};
  M3 (failed list forced empty) failing {3,4}.
- VSP-73: at `0d992e0` failing {2,3,4} (cell 2: `42P01 relation "collateral_items_id_seq" does not exist`, "matching gate 10 (i-A)"),
  passing {1}; at `6d7ea73` 4/4; M1 (no sequences) failing {2,3,4}; M2 (no indexes) failing {2}; M3 (no `OWNED BY`) failing {3}.
- Sets: VSP66 npm test 105/105, test:db 84 (async-faults 30, checkout-link-death 6, completed-response 3, concurrency 5, harness 4,
  pool-timeout 12, reminder-push 6, routes 18); VSP71 105/105, test:db 83 (… session-index-boot 5); VSP70 109/109, test:db 78; VSP68 110/110,
  test:db 78; VSP73 105/105, test:db 82 (… backup-dump-replay 4). **Derived by the drafter (a prediction, not a READY claim): merged tree
  npm test 114, test:db 93.**

**How you treat these:** every NOT TESTED line you CAN test locally, you test: VSP-66's end-to-end real-caller cells and a half-open link;
VSP-71's bound ≤ 2,000 ms and the `lock_timeout` restore; VSP-70's real stalled/dead Postgres; VSP-68's real Postgres under the backup;
VSP-73's replay over an existing database (by an owner and by a non-owner, WRONG (t)); and Node 20 for all five. The rest you carry into
your own NOT TESTED, reworded as your own.

## 2a. LEGITIMATE SHAPES — each fix changes a path whose failure is a crash, a failed boot or a false alarm, so a false alarm is damage (template §2a)
Measure every row. **A row whose expected verdict and clause disagree is a finding against this brief. Say so.**

| shape — its ordinary form, as the portal really produces it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| VSP66: an ordinary signed-in session of traffic (logins, `/me`, quotes, generate, backup-db) with NO link fault | 0 `[db]` lines; every client reused (same backend pids); `listenerCount('error')` on every idle client back to 1; no MaxListeners warning after ≥ 1,000 checkouts of one client | the listener is added per checkout and removed per release | builder (control cell) — **measure at scale, `max 1`** |
| VSP66: the generate route holds its client; the link RSTs mid-transaction (gate 9 S7b) | process alive; generate 500; one death logged; next request 200 on a fresh backend | the held listener + pg-pool discard | gate 9 fix-shape — **measure; MAIN must crash** |
| VSP71: a boot on a PRODUCTION-SHAPED database (store-made `session` WITH its index, boot role owns it, live rows) | no DDL on `session`, no lock wait, **no VSP-71 warning**, `lock_timeout` unchanged afterwards | the outer `to_regclass` IF skips the block | gate 10 §N.2(b) — **re-measure at `5bdaeae`** |
| VSP71: a boot on a FRESH database | index created, no warning, catalog-identical to `table.sql` | the block's success path | builder — **re-measure** |
| VSP71: index missing, boot role owns `session`, nothing in the way | index created, no warning | success path | builder control 1 |
| VSP71: a boot while ANOTHER instance's signed-in writes run (index missing) | the boot waits ≤ ~2 s; **other writers queue behind the boot's SHARE request for up to 2 s** | the lock queue | **nobody measured it** — drafter; measure the other writers' latency |
| VSP70: a restore whose clear step succeeds | BEGIN, DELETEs in reverse order, COMMIT, `release(undefined)`; client reused | unchanged path | builder control — **on real Postgres** |
| VSP68: every table dumps | one upload; "DB Backup OK", priority 3; no `failedTables` blob key; `failed_tables: []` | unchanged path | builder control — **on real Postgres** |
| VSP68: a FRESH database, `feedback` never created (WRONG (n)) | ??? — the alert says "INCOMPLETE … feedback (relation "feedback" does not exist)" | `failed_tables` from `tables[t].error` | **nobody ruled it** — measure, then RULE true alarm vs noise, and say whether it needs Kam |
| VSP73: an admin downloads a dump of an ordinary production-shaped DB (your own seeded one) | 200 zip; replays as ONE query into a fresh DB; same tables, rows, index set; `nextval` = max + 1 | sequences first, indexes after rows, `OWNED BY` | builder cells 2-3 — **re-measure through the REAL route** |
| VSP73: the same dump replayed over the SAME (existing, populated) database by its OWNER | the DDL and index lines no-op; the INSERTs collide 23505 (the READY: "as before") | `IF NOT EXISTS` | READY NOT TESTED — **measure; say whether "as before" holds** |
| VSP73: the same, replayed by a role that does NOT own the tables | **predicted: fails 42501 on the first index line** (WRONG (t)) | PG16's ownership-before-existence check | drafter — **measure** |
| VSP73 × VSP71 (merged tree): replay into a fresh DB, then boot | index present, **no VSP-71 warning**, the portal serves | VSP-73 emits the index; VSP-71's guard skips | VSP-73 READY — **measure (§N6.4)** |

## N1. TARGET VSP66 — the held-client link death (TIER 1) — the measurements (FAIL conditions stated before the runs, per Rule 1)
**FAIL condition, stated BEFORE the runs:** any `uncaughtException` / unhandled `error` in a product process from a link death under a held
client, on any shape in §N1.1-N1.3, on Node 26 or Node 20; a dead client handed to a later caller (its backend pid seen again, or a later
caller's query failing with `not queryable` / `Connection terminated`); a listener stacked or leaked on any client (`listenerCount('error')`
> 1 on an idle client, or a MaxListeners warning); the holder's next query hanging instead of rejecting; a regression of any gate-9/10 HELD
result (§N5.1); `npm test` or `test:db` losing any NAME that passes at `0d992e0`; a red that is not behavioural. **A double log line is an
observation, not a FAIL, unless it floods** (rule it).
1. **The builder's six cells, RE-DERIVED on your instrument (MEASURED).** Copy `qa-g10-stallproxy.cjs`. ADD two shapes it lacks (WRONG (c)):
   **TERMINATE** (`pg_terminate_backend(<pid>)` over a SEPARATE direct connection to YOUR database) and **FIN** (`end()` on the app-facing
   socket, Postgres NOT told). Keep **RST** (`rst`). For each of {terminate-idle-held, terminate-in-flight, RST-idle-held, RST-in-flight,
   FIN-idle-held, FIN-in-flight} run a CHILD process that loads the tree's real `server/db.js` with NO handler of its own (the builder's
   reasoning is right: a listener in your process would be the fix), checks out a client, applies the fault, then: the holder's next query
   (reject or hang, 5 s cap), `release()`, `listenerCount('error')` after release, and a fresh `pool.query` backend pid. **Count every
   `[db]` line by kind (`held` and `idle client error`) and every emit** (WRONG (a)). Record the child's exit code and stderr. **At `0d992e0`
   (RED expected) and `1976275` (GREEN expected), N ≥ 3 each**, shrunk bound where a bound matters.
2. **"Does the dead client ever get reused?" — the in-flight release window (WRONG (b), MEASURED).** In-flight terminate, and in-flight
   RST: the holder calls `release()` IMMEDIATELY on its query's rejection (no ROLLBACK, no further query, same tick), then `pool.query` at
   once, with `max 1` so the pool has one client. Record `client._queryable` at release (read it in your own harness process, never in
   product code), the pool's `totalCount` / `idleCount` / `waitingCount`, and the backend pid of the next query. N ≥ 20 per shape, because it
   is a race. Then the same with a real caller's shape: `await client.query('ROLLBACK').catch(() => {})` before `release()` (the generate
   route and the dispatcher do that). **If ANY run hands the dead client out again, quote the run.** At `0d992e0` the process dies first, so
   this is a head-only arm. Say so.
3. **End-to-end cells with a REAL caller holding the client (MEASURED; the READY's first NOT TESTED line).** Each on the real `createApp()` /
   real module under `env -i`, at `0d992e0` (the process must crash: the positive control) and at `1976275` (it must survive):
   - **S7b re-run** (gate 9's arm, copied): generate holding its `FOR UPDATE` client, RST (a) during the stalled first query and (b) during
     the queued ROLLBACK. Gate 9: HEAD 2/2 and MAIN 2/2 uncaught. Expected at `1976275`: 0 uncaught, generate 500, follow-up `/me` 200.
   - **Terminate and FIN under generate**, same arm, one run each.
   - **`dispatchDue()`** (`server/reminders/dispatcher.js:120-162`) with `sendEmail` replaced by YOUR recorder that BLOCKS until you release
     it (the dispatcher awaits it INSIDE its transaction, `:137`): terminate the held backend while it blocks. Expected: process alive,
     `[reminders] dispatch failed:` logged, the reminder row still `pending` (rolled back), the client discarded (pid never seen again). Note
     gate 9's pre-existing at-least-once re-send (§N.4(h)) if the recorder already "sent". Do not grade it.
   - **`GET /api/admin/backup-db`** (`server/routes/admin.js:92-184`) signed in as admin: kill the backend WHILE the route holds its client.
     Either hold a dump `SELECT` with the proxy, or pause the reader during the archive stream. **Prove the kill landed while the client was
     held** (the `held` log line, `pg_stat_activity`) before reading the result. Expected: process alive, the route answers (500 or a
     truncated zip: quote which), the next request 200.
   **A cell whose fault did not land while the client was held is VOID, not green.**
4. **Log-once, per shape (MEASURED, from §N1.1-N1.3):** a table of shape × {emits by pg, `held` lines, `idle client error` lines}. Rule whether
   "logged once per death" holds on every shape, and whether any shape logs nothing at all (a SILENT death is worse than a double line).
5. **Listener hygiene at scale (MEASURED):** one client (`max 1`), 20,000 checkout/release cycles with a query each (the P1 shape), at the head:
   `listenerCount('error')` idle = 1 throughout, no `MaxListenersExceededWarning`, same backend pid, elapsed quoted. **Also the callback form
   of `pool.connect(cb)`** (`db.js:126-131`, `cb(undefined, client, client.release)`): the release it hands out must be the wrapped one.
6. **Red-proofs, re-derived** (fresh tree per arm, asserted edits, `node --check` rc quoted, a red from a mutant that does not parse is VOID):
   the builder's cells at `0d992e0` (copy the two new test files in, hash-verified): predicted failing {2,3,4,5,6}; M1 (no `removeListener`),
   M2 (no `told` flag), M3 (no `client.on('error', …)`). Quote which cells redden, and why. **Also run YOUR §N1.1 on M1 and M3**, which must
   redden. **M4 (yours): move `removeListener` AFTER `release.call`** (predicted: a no-op on the discard path, and one more listener on a
   reused client. Measure it).
7. **VSP-65's machinery is untouched (READ + MEASURED):** `GUARDED`, `TIMED_OUT` and the release passing `client[TIMED_OUT]` are unchanged
   in the `1976275` diff (READ: only `:97-117` are added or changed). Re-run gate 10's `pool-timeout.test.js` N ≥ 3 at the head, and gate 10's
   S1 ticket cell once at the shrunk bound. Same figures within load noise, or a finding.

## N2. TARGET VSP71 — the session index cannot fail a boot (TIER 1) — the measurements
**FAIL condition, stated BEFORE the runs:** a boot that fails, or waits longer than ~2 s plus noise on `session`, in either of gate 10's
(a)/(b) shapes at the shipped bound or at the builder's 6,000; any change on a production-shaped database whose index exists (DDL, lock
wait, a VSP-71 warning line); `lock_timeout` different after `initDb()` from before it, on the same backend; the rest of `schema.sql` not
committed when the index block fails; a VSP-71 warning on a healthy boot (a false alarm); a regression of gate 10's §N.2 results; a NAME
lost vs `0d992e0`. **Failures at a bound ≤ 2,000 ms are the READY's named residual, not a FAIL, if you quote them** (WRONG (f)).
All roles NON-superuser, named `vsp_qa_g11_*` and listed, or created inside a transaction you roll back. The compose user `salesportal` is a
SUPERUSER and bypasses ownership: **any owner cell run as it proves nothing.**
1. **Gate 10's (a) and (b), RE-MEASURED with gate 10's own instruments** (`qa-g10-n2c.cjs`, `qa-g10-n2d2.cjs`, copied and re-pointed), at
   `0d992e0` (RED expected: (a) 42501, (b) `DB_QUERY_TIMEOUT` at the bound) and at `5bdaeae` (GREEN expected):
   - **(a) non-owner, index missing:** the boot resolves; exactly one VSP-71 warning line in the app log; the index still missing; **every other
     table, index and `initDb.js` migration present** (the file committed). Prove it with a marker index dropped beforehand that the boot must
     recreate (gate 10's d4 used `idx_email_log_lead`).
   - **(b) held write, index missing, boot owns `session`:** ROW EXCLUSIVE held 45 s. Bounds: **30,000 (shipped), 6,000, 2,000 and 1,500**
     (WRONG (f)). Per bound: boot elapsed, the SQLSTATE in the Postgres WARNING (expected 55P03), the app warning line, and whether the index
     appears LATER (gate 10's d2 abandoned-transaction commit, VSP65-R2-O4: at `5bdaeae` nothing should be left queued). Observe `pg_locks`
     / `pg_stat_activity` every 1 s from an ASYNC observer (gate 10 self-finding 3).
2. **The rest of `schema.sql` commits (MEASURED):** in (a) and (b), a catalog snapshot of every table and index the file creates, before vs
   after, plus the rows `initDb.js` seeds. Anything missing is a FAIL.
3. **`lock_timeout` is RESTORED, and cannot leak (MEASURED; WRONG (e)).** A pool of `max 1` so the boot and your probe share ONE backend.
   Before the boot: `SET lock_timeout = '7s'` at SESSION level on that backend (a sentinel no default produces). Then `initDb()`, then
   `SHOW lock_timeout` on the same backend (verify the pid). Paths: index present (the block is skipped), index created, (a) failed (42501),
   (b) failed (55P03). Expected `7s` on every path. **Positive control (a mutant that must redden the probe): `set_config('lock_timeout', '2s',
   false)`** (session-level): the probe must read `2s` afterwards. **M-norestore (yours):** delete `:297` (the restore). Predicted: NO leak,
   because `is_local` = true ends at the file's transaction. If so, say plainly that the restore line is belt and braces. Also READ whether any
   caller runs `initDb()` inside an explicit transaction (`test/db/helpers.js`, `server/index.js` `main()`), where a transaction-local setting
   WOULD outlive the file.
4. **The production-shaped no-op boot of gate 10 §N.2(b), re-run at `5bdaeae` (MEASURED).** Store-made `session` at `0d992e0`, WITH its index,
   live rows, a kept cookie. Then `5bdaeae`'s `initDb()`, superuser-owned AND owned by a non-superuser boot role: relfilenode, `pg_class` /
   `pg_index` / `pg_constraint` xmins, owner, rows and row md5 unchanged; a DB-local `ddl_command_end` witness silent on `session`; **0
   VSP-71 warning lines**; the kept cookie 200. Gate 10's figures: RESOLVED 48 ms, diff NONE.
5. **Interaction with VSP-73 (the backup-db dump restore route) (MEASURED; READ where labelled).** Re-use gate 10 §N.3(b)'s method: a real
   `GET /api/admin/backup-db` dump of YOUR production-shaped DB, replayed STATEMENT BY STATEMENT into a fresh DB (it cannot replay whole: 42P01,
   pre-existing R2-O7). `session` arrives WITHOUT its index. Then boot `5bdaeae`: (i) as a boot role that OWNS `session` → index repaired, no
   warning; (ii) as a role that does NOT own it (the dump replayed by another role) → resolves, one warning, index missing; (iii) the other
   order (boot, then dump). At `0d992e0` (ii) is gate 10's R2-O1 42501 crash-loop. **Rule the READY's claim "a restore done as any role can no
   longer crash-loop the next boot".** This arm uses the dump as `5bdaeae` produces it (the OLD route, `admin.js` `e1abcde`: no index). The
   same question with VSP-73's dump (which now CARRIES the index) is §N6.4, on the merged tree. READ ONLY: whether any route other than a
   manual `DROP INDEX` can still produce "table present, index missing" once both are merged.
6. **The 2 s lock-queue effect on OTHER instances (MEASURED; §2a).** Index missing, boot owns `session`, one writer holding ROW EXCLUSIVE, AND
   a second instance's signed-in requests running during the boot: those requests' latency while the boot's SHARE request waits (they queue
   behind it). Quote the worst.
7. **A cancel during the build (MEASURED; WRONG (g)):** `pg_cancel_backend` on the boot backend while the `CREATE INDEX` waits. Does the boot
   fail (57014 is not caught by `WHEN OTHERS`)? Quote it, and rule whether production can produce it (READ ONLY).
8. **Two concurrent boots, index missing (MEASURED, N ≥ 10 pairs):** at `5bdaeae` vs `0d992e0`. Count outcomes by SQLSTATE. Gate 10's R2-O5
   (23505 on the first tables of a FRESH database, identical at main) is pre-existing; this arm is on an EXISTING database with the index missing.
9. **Red-proofs, re-derived:** the builder's 5 cells at `0d992e0` (predicted failing {3,4,5}); M1 (no `lock_timeout`), M2 (no exception block),
   M3 (no `initDb` warning). **Also: M5 (yours) `WHEN insufficient_privilege OR lock_not_available` in place of `WHEN OTHERS`** (does any cell
   notice the narrower catch?), and gate 10's M7 on the head (plain `CREATE INDEX IF NOT EXISTS`: the pool-timeout owner cell must still redden).
   Each mutated `schema.sql` must also EXECUTE inside BEGIN … ROLLBACK on your DB (`node --check` cannot parse SQL; gate 10's method).
10. **The builder's test hygiene (MEASURED, under TUESDAY'S RULING on WRONG (h)):** after each `test:db` run of a VSP-71 tree, list every
   `vsp71_%` role and database left in the cluster (read-only catalog query). A leftover is a finding. **Never drop it yourself.**

## N3. TARGET VSP70 — the restore throws the first error (TIER 2) — the measurements
**FAIL condition, stated BEFORE the runs:** any change to WHAT the restore deletes or inserts (tables, order, statements, transaction
boundary); on the masking shape, a thrown error that is not the FIRST (failing) statement's; a client in an unknown transaction state
handed to a later caller; the CLI's usage or exit codes changed; a NAME lost vs `0d992e0`.
1. **"Unchanged" — the lines that prove it (READ; re-derive them yourself with `diff`/`cmp` of the ranges, and quote the result).** The drafter
   READ, byte-compared with `cmp` over `git show <sha>:server/dbRestore.js | sed -n`:
   - `0d992e0:1-106` == `10ba4bb:1-106` byte-identical: `RESTORE_ORDER` (`:24-35`, 10 tables), `restoreTable()` (`:71-91`, the per-table
     `DELETE FROM` + per-row INSERT), `resetSequence()` (`:93-106`).
   - The clear transaction's BODY: `0d992e0:150-161` (`BEGIN` … reverse-order `DELETE FROM "${t}"` … `COMMIT`) == `10ba4bb:112-123`.
   - The INSERT loop and the end of `main()`: `0d992e0:169-183` == `10ba4bb:179-193`. `main()`'s prologue: `0d992e0:107-146` == `10ba4bb:136-175`.
   - What DID change: `0d992e0:148-149,162-167,185-188` → `10ba4bb:108-111,124-135,177,195-202` (the function wrapper, the ROLLBACK
     `.catch`, `release(broken)`, the `require.main` guard, the export). Diff hunks: `@@ -105,6 +105,29`, `@@ -145,26 +168,7`, `@@ -182,7 +186,11`
     (`12138cb`) and `@@ -108,6 +108,7`, `@@ -121,10 +122,15` (`10ba4bb`).
2. **The builder's 4 cells, RED re-derived at `12138cb` (not `0d992e0`: the refactor is the fix's base; WRONG (i)).** Copy
   `server/dbRestore.test.js` (hash-verified) into a `12138cb` tree: predicted failing {3,4}, passing {1,2}. Cell 3 must fail with the masking
   ("Client has encountered a connection error and is not queryable" thrown). At `10ba4bb`: 4/4, N ≥ 3. **M1** (`release()` with no error) →
   predicted failing {4}; **M2** (no ROLLBACK warn line) → predicted failing {3}. Quote why each is red.
3. **ONE real-Postgres cell of the masking shape (MEASURED; Tuesday's requirement: a DELETE that fails, then a ROLLBACK on a dead link).** The
   builder's cells use a scripted fake client only. Because both errors are `DB_QUERY_TIMEOUT` on a plain black hole (WRONG (l)), make the
   first error DISTINCT:
   - In YOUR database (a booted `0d992e0` schema), **drop `partner_org_requests`** (the LAST name in `RESTORE_ORDER`, so the FIRST `DELETE` in
     reverse order), so its `DELETE` fails with a real `42P01`. Run the tree's real `clearTables(data, pool)` from a harness under `env -i`,
     with `data.tables` naming every restore table, the pool pointed at YOUR proxy, and **`armNext` on `DELETE FROM "partner_org_requests"`
     with action `blackhole`**: the NEXT app→pg chunk (the ROLLBACK) is black-holed. The ROLLBACK then times out at the shrunk bound.
   - **At `12138cb` (RED expected):** the thrown error is the ROLLBACK's `DB_QUERY_TIMEOUT`, and the `42P01` is lost. **At `10ba4bb` (GREEN
     expected):** the thrown error is the `42P01`, one `[!] ROLLBACK failed as well: DB_QUERY_TIMEOUT …` line, and the client discarded
     (backend pid never handed out again; pool counters).
   - **The dead-link variant (RST before the ROLLBACK) ONLY on the merged VSP-66 × VSP-70 tree** (the VSP-70 READY is right: on VSP-70 alone a
     held client whose link dies throws uncaught). Run it once there, and once on `10ba4bb` alone to show the crash (the positive control).
   - **Run the real cell under M1 too** (WRONG (k)): does any real shape redden M1? If not, say that `release(broken)` is belt and braces on
     real pg.
   - No rows are deleted for real: the `42P01` aborts the transaction before any `DELETE` succeeds. Prove it with row counts of the other nine
     tables before and after.
4. **The CLI surface is unchanged (MEASURED):** `node <tree>/server/dbRestore.js` under `env -i` with NO `AZURE_BACKUP_CONN_STR`: rc 1 and
   `Error: AZURE_BACKUP_CONN_STR not set.` at both `0d992e0` and `10ba4bb`. **Never set that variable** (§13.3). `require()` of the module at
   `10ba4bb` has no side effects (no exit, no connection: count backends before and after).
5. **The builder's observation (restoreTable re-DELETEs outside the transaction; a partial restore ends "Restore complete." exit 0) is F-B's
   neighbour:** READ, one line, not graded here.

## N4. TARGET VSP68 — the backup INCOMPLETE alert (TIER 2) — the measurements
**FAIL condition, stated BEFORE the runs:** a backup missing a whole table announced as OK; the partial backup NOT uploaded; the blob
metadata shape different from the READY's (`totalRows`, `createdAt`, and `failedTables` only when non-empty); the FAILED path changed; any
egress to a real ntfy server or real Blob Storage; a NAME lost vs `0d992e0`.
1. **The builder's 5 cells, RED re-derived at `0d992e0`** (copy `server/dbBackup.test.js`, hash-verified, into a `0d992e0` tree): predicted failing
   {3,4,5}, cell 3 with "DB Backup OK". At `7ef698d`: 5/5, N ≥ 3. M1 (alert always ok) → {3}; M2 (no blob marker) → {4}; M3 (failed list forced
   empty) → {3,4}. Quote why each is red. Confirm the stub was in place (WRONG (o)).
2. **ONE cell with a REAL Postgres table-dump failure (MEASURED; Tuesday's requirement).** The tree's real `server/db.js` against YOUR database,
   with `@azure/storage-blob` replaced by YOUR recorder through `require.cache` (never the real SDK, and **never set `AZURE_BACKUP_CONN_STR`**;
   the module's constant is then `''`, which only your stub receives). ntfy goes to YOUR recorder: `NTFY_SERVER=http://127.0.0.1:<kernel
   port>` served by your harness, `NTFY_TOPIC=qa-g11-dummy` (never a real topic, never ntfy.sh; the fetch guard allows ONLY your recorder).
   Call `runBackup()` directly, never `startBackupScheduler()`.
   - **Shape A, natural:** a freshly `initDb()`'d database, where `feedback` does not exist (WRONG (n)) → `42P01` on `feedback`.
   - **Shape B, gate 9's:** `SELECT * FROM leads` black-holed by your proxy at the shrunk bound → `DB_QUERY_TIMEOUT`.
   - **At `0d992e0` (RED expected):** title "DB Backup OK". **At `7ef698d` (GREEN expected):** exactly one alert, title "DB Backup INCOMPLETE",
     `Priority: 4`, `Tags: warning,floppy_disk`, a body naming the table and its error; the log line `[db-backup] INCOMPLETE in …: not backed up: …`.
   - **The partial backup still uploads:** your blob recorder received ONE upload. Unzip it: `metadata.failed_tables` names the table, the
     other tables carry their real rows (count them against YOUR database), and `tables[<failed>].error` carries the reason. Quote the upload's
     `metadata` object (**expected keys exactly `totalRows`, `createdAt`, `failedTables`**, all strings) and `blobHTTPHeaders`.
   - **A complete backup** (create `feedback` first, nothing black-holed): "DB Backup OK", priority 3, NO `failedTables` key.
3. **The empty-message error (MEASURED; WRONG (m)):** make one table's dump reject with an `Error` whose `message` is `''` (a harness-side
   wrapper around the tree's `query` is acceptable for this ONE cell; say so). Predicted at `7ef698d`: "DB Backup OK" with that table at
   `rowCount: 0`. If so, it is a finding against the fix (the same class as the ticket), with a fix-shape in prose.
4. **FAILED path unchanged:** the blob recorder's `upload` throws → "DB Backup FAILED", priority 5, body `Backup failed: <msg>`, at both shas.
5. **F-A and F-B are OUT OF SCOPE** (RULED BY KAM, AND SETTLED, above). Do not measure them.

## N5. SHARED — held results, suites, Node 20, CI
1. **Gate 9/10 HELD results, re-run briefly on the MERGED tree (§12) AND at `1976275`** (one run each; compare to gate 10's §N.5 and say "same"
   or quote the difference, with load): S1 black hole (the ticket cell ×3 shrunk, once at the SHIPPED bound), S6 handshake at the shipped bound,
   **S7 late RST** (gate 10: 0 uncaught), S8 transient generate, discard-on-release by backend pid, the 15 s pool-wait cap at the shipped
   bound, the boot refusal (`DB_QUERY_TIMEOUT_MS=abc`, rc 1). **Positive control in the same session:** main `0d992e0` no longer hangs in S1
   (it is bounded since VSP-65), so the control that must fire is **`0d992e0` CRASHING in S7b** (the old VSP65-O1, gate 9: 2/2). If it does not
   crash, your RST is not landing on a held client. **Negative control:** pass-through adds < 5 ms per request.
2. **SUITES AS SETS, NOT COUNTS, same machine, same session (MEASURED).** In fresh archived trees of `0d992e0`, each of the five heads and the
   merged tree: `npm test` and `npm run test:db` (each `test:db` on a FRESHLY CREATED `vsp_qa_g11_<epoch>_test`, proven fresh: zero user
   tables). Extract every NAME with its outcome (`specsets.py` / `tapsets.py`), and report vs `0d992e0`: names passing at main that do not pass
   at the head (**must be empty**); names added (READ predictions: VSP66 +6 db; VSP71 +5 db; VSP70 +4 unit; VSP68 +5 unit; VSP73 +4 db; merged
   +15 db, +9 unit); names removed (expect 0); duplicates. Totals beside the sets (main: unit 105, db 78, gate 10). Each new test file N ≥ 3 at its head,
   load quoted. **CI's coverage command locally** (`node --test --experimental-test-coverage --test-coverage-lines=80
   --test-coverage-branches=70 $(find server -name '*.test.js')`) at each head and the merged tree. Gate 10: 84.94% / 73.37% at `0d992e0`.
   **Label it: local Node 26.8.1 standing in for CI's Node 22; not CI.**
3. **The product-test hygiene line** (§N2.10) after every VSP-71- or VSP-73-bearing `test:db` run: every `vsp71_%` role and every `vsp71_%` /
   `vsp73_%` database in the cluster, before and after.
4. **NODE 20 LEG (production's major) — per the NODE20-LEG line at the top (DOCKER-PULL-NEVER).** Exactly ONE docker verb family is
   sanctioned, for this leg only: `docker image inspect node:20` (prove the image is ALREADY present, quote its digest; if absent, the leg is NOT
   RUN — **never pull**) and `docker run --rm --pull=never` of that image, with YOUR archived tree mounted **WRITABLE** (a read-only mount went
   VOID with `EROFS` in the VSP-65 builder's run), an explicit `-e` allowlist (§13.3; never `--env-file`), `NODE_ENV=test`, and the database
   URL pointing at YOUR `_test` database via `host.docker.internal:5433`. Name every container `qa-g11-node20-<epoch>`. **Never
   `docker start/stop/exec/rm/compose` on any container, never `vsp-dev-db`, never `--network host`.** Run in it: `node --version` (quote),
   `npm test` and `test:db` on the MERGED tree, and at their heads: VSP-66's §N1.1 terminate/RST/FIN cells, VSP-71's (a) and (b) at 6,000,
   VSP-70's real masking cell, VSP-68's real cell (shape A), VSP-73's one-query replay and the merged-tree replay + boot (§N6.4). Reap each
   container in a `finally` (it is `--rm`; confirm it is gone the way gate 10 did).
5. **CI IS UNMEASURED.** This project's `gh` is not authenticated, and **you must not use `gh` at all**. Say plainly: CI on all five branches is
   **UNMEASURED**, including its **Node 22 coverage gate** (`test.yml` `:47-51`, "Unit + snapshot tests with coverage gate (Node 22 only)") and
   its **`e2e:pro` step against a server booted by the portal's entry point** (`test.yml` `:56-68`). For VSP-71 that step is the first CI boot of
   the new `schema.sql` block. Name them as the first things to read at merge.

## N6. TARGET VSP73 — the backup-db dump replays into a fresh database (TIER 2) — the measurements
**FAIL condition, stated BEFORE the runs:** a dump from the REAL route that does not replay as ONE query into a fresh database; a replayed
database whose tables, per-table row counts, or index set (by `pg_get_indexdef`) differ from the source's in anything but VSP-73's "NOT FIXED"
list (FK / CHECK constraints, typmods); `nextval(pg_get_serial_sequence(t, 'id'))` ≠ max(id) + 1 on any serial table; the portal not booting
on the replayed database; the route failing (non-200, a truncated zip, a crash) on a database where it served at `0d992e0`; the IO1-round-2
mid-stream fault cells regressing (`async-faults.test.js`); a NAME lost vs `0d992e0`.
**Data rule:** every dump in this gate is taken through the real route from a database YOU created and seeded (`initDb()` + seed + your own
signed-in activity). **Never read, open, copy or keep a real or production dump.** Keep the dumps you take under `work-g11/dumps/` (they hold
only your fixture data; still redact session ids in anything you quote, gate 10's practice).
1. **The red at `0d992e0`, re-derived through the REAL route (MEASURED).** Copy `test/db/backup-dump-replay.test.js` (hash-verified) into a
   `0d992e0` tree: predicted failing {2,3,4}, cell 2 with `42P01 relation "collateral_items_id_seq" does not exist`. At `6d7ea73`: 4/4, N ≥ 3.
   **Independently of the builder's cell** (its zip reader is its own code), take a dump with YOUR harness (gate 10's `qa-g10-n3.cjs` method:
   admin signed in, the real `createApp()`, the zip written raw and unzipped by a tool you trust), and replay it as ONE query into a fresh
   `vsp_qa_g11_*` database: at `0d992e0` the `42P01`, at `6d7ea73` success.
2. **The three mutants (MEASURED):** M1 (no sequences) → predicted failing {2,3,4}; M2 (no indexes) → {2}; M3 (no `OWNED BY`) → {3}. Asserted
   edits, fresh tree per arm, `node --check` rc quoted, marker grep-proved per tree. Quote why each is red.
3. **Source vs replay, compared from the catalogs (MEASURED):** tables; row counts per table AND a per-table row checksum; the index set by
   `pg_get_indexdef` (names AND definitions, partial `WHERE` clauses kept, UNIQUE kept); sequences (`last_value`, `pg_get_serial_sequence`,
   `OWNED BY` via `pg_depend` `deptype = 'a'`); a new row's id on every serial table. **List every difference**, and classify each as VSP-73's
   NOT FIXED list (FK, CHECK, typmod) or a finding. Count PK/unique indexes per table on the replay: a duplicate is a finding (WRONG (u)).
4. **VSP-73 × VSP-71 ON THE MERGED TREE (MEASURED; Tuesday's requirement, WRONG (v)).** Dump a production-shaped DB (store-made `session` WITH
   its index, live rows) through the merged tree's route, replay it into a fresh DB, then boot the merged tree's `initDb()`: **`IDX_session_expire`
   present, 0 VSP-71 warning lines, a kept cookie served 200.** Do it twice: as a boot role that owns the replayed tables, and as one that does
   not (the replay done by another role). Then the control: the same with the index dropped on the replay (the manual `DROP INDEX` route), which
   VSP-71 must survive (resolves, one warning, or a repair if the boot role owns `session`). **Also at `6d7ea73` ALONE:** replay + boot of
   `6d7ea73` (which has `0d992e0`'s `schema.sql`): the index arrives from the dump, so the boot needs no index DDL.
5. **Replay over an EXISTING database (MEASURED; the READY's first NOT TESTED line; WRONG (t)):** the dump replayed as one query over the
   source database itself, (a) as the tables' OWNER: predicted 23505 on the first INSERT (the whole replay rolls back); (b) as a NON-owner
   `vsp_qa_g11_*` role with SELECT/INSERT grants: predicted 42501 on the first index line. At `0d992e0` and `6d7ea73`, both. Rule whether VSP-73
   changes the outcome of any replay a Datasec operator would plausibly run, and say it plainly if (b) is a new failure mode.
6. **The route itself (MEASURED):** status, bytes, elapsed and load for the real route at `0d992e0` and `6d7ea73` on the same seeded DB; the
   route's query count while it holds its client (from `pg_stat_statements` if present in YOUR DB, else a count from a proxy log); gate 10's
   async-faults backup-db cells N ≥ 3 at the head. **A mixed-case table and sequence name** in your own DB (the portal has one already:
   `"session"` is lower-case, but `"IDX_session_expire"` is mixed-case): does the dump still replay? READ: `quoteIdent` quotes the new
   sequence lines (`:125`, `:187`); `${table_name}` at `:187-188` is `regclass` text, which Postgres quotes itself; the pre-existing
   `setval('${seq.sequence_name}', …)` at `:188` puts an UNQUOTED name inside a literal (pre-existing, not VSP-73's). Measure one.
7. **The dump carries no secret the old one did not (READ + MEASURED):** diff the SET of statement kinds between the `0d992e0` and `6d7ea73`
   dumps of the same DB. Only `CREATE SEQUENCE`, `CREATE [UNIQUE] INDEX IF NOT EXISTS` and `ALTER SEQUENCE … OWNED BY` may be new.

## 12. The merge and the queue
**The drafter RAN `merge-tree` from its own object dir** (`GIT_OBJECT_DIRECTORY` = a fresh `mktemp -d` in its scratchpad, alternates = the
repo's objects; 36 objects written there, none in the repo; 06:16-06:26 AEST):
| merge | result | tree |
|---|---|---|
| `0d992e0` × `1976275` (VSP66) | CLEAN | `5d4f6ef6…` = the head's own tree |
| `0d992e0` × `5bdaeae` (VSP71) | CLEAN | `f5bbfe62…` = the head's own tree |
| `0d992e0` × `10ba4bb` (VSP70) | CLEAN | `397947fd…` = the head's own tree |
| `0d992e0` × `7ef698d` (VSP68) | CLEAN | `f726694d…` = the head's own tree |
| `0d992e0` × `6d7ea73` (VSP73) | CLEAN | `788cbdc8…` = the head's own tree |
| every PAIR of the five (10 pairs) | **CONFLICT (content) in `BACKLOG.md` ONLY**, rc 1 | — |
**Prediction for the five-way merge:** a textual conflict in `BACKLOG.md` at the SAME anchor (after `BACKLOG.md:31` at `0d992e0`, the blank
line before "- [x] **A dropped IDLE pooled Postgres connection…"). Each target inserts one block there (VSP66 +6, VSP71 +7, VSP70 +6, VSP68 +18
including the F-A and F-B entries, VSP73 +7). The resolution is "keep all five blocks", and it touches no code. **Measure it yourself:** from
YOUR own object dir, the pairwise results above, and then a sequential merge, main + VSP66 → + VSP71 → + VSP70 → + VSP68 → + VSP73. Resolve
`BACKLOG.md` by keeping all blocks in that order, IN YOUR OWN TREE ONLY (an archived tree plus the five code deltas applied, never a repo
checkout). **Prove the merged tree's code files equal "main + each target's own blobs"**: `db.js` = `5d42db6`, `schema.sql` = `74f6e9c`,
`initDb.js` = `68fc8cc`, `dbRestore.js` = `5f4b71d`, `dbBackup.js` = `5e31eb4`, `routes/admin.js` = `7b00469`, and the new test files. That
tree is **the merged tree** for §N5, §N6.4 and the merged-tree line. `git merge-tree --write-tree` only as `GIT_OBJECT_DIRECTORY=<your own mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git
-C <repo> merge-tree --write-tree --name-only <a> <b>`, or SKIP it and say so.
**Semantic interactions on the merged tree (not visible to merge-tree; MEASURED where marked):** VSP66 × VSP70 (a link death under
`clearTables`' held client: §N3.3's RST variant); VSP66 × VSP71 (the boot's `pool.query(schema)` passes through `guard()`: a boot under a link
death, one run); **VSP71 × VSP73 (§N6.4, Tuesday's requirement)**; VSP66 × VSP73 (the backup-db kill cell of §N1.3 on VSP-73's route, WRONG (w));
VSP70 × VSP68 (F-B's shape, OUT OF SCOPE: one line only); the six-holder census on the merged tree (WRONG (j)).
**Cells to re-run on the merged head at merge** (name at least these): `npm test` + `test:db` as sets; each new test file N ≥ 3; S7b; §N1.2's
release window; VSP-71's (a)/(b) at the shipped bound; the production-shaped no-op boot; VSP-70's real masking cell; VSP-68's real cell;
VSP-73's replay + boot; CI's Node 20 and Node 22 legs including the coverage gate and `e2e:pro`. **After Kam's deploy (not yours to read):** the first production
boot's log (any `[db] IDX_session_expire is missing (VSP-71)` line), and the first nightly backup alert (OK or INCOMPLETE, WRONG (n)).

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)**, or any port another seat
   holds. **Never `127.0.0.1:49162`, `:49164` or `:49166`** (a local Logitech plugin answers 501 there). Take every port from the kernel and
   bind `127.0.0.1` wherever YOUR harness, proxy or recorder listens. **Never start the portal's own entry point** (it binds `0.0.0.0` in
   `main()`); use the real `createApp()` and `initDb()` inside your harness only.
2. **Postgres = the local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all** (the one exception is
   §N5.4, under its DOCKER-PULL-NEVER line). Create `vsp_qa_g11_<epoch>` for app runs and `vsp_qa_g11_<epoch>_test` as `TEST_DATABASE_URL` for
   `test:db` (it TRUNCATEs; the name MUST end in `_test`). **Never** `salesportal`, `salesportal_test` (the builder's; **the Vision builder seat
   is LIVE at drafting and uses it**), any `vsp_qa_g1_*` … `vsp_qa_g10_*` database, the builder's `vsp_bf1_*`, or any `vsp71_*` / `vsp73_*`
   database you did not cause. `server/db.js`'s DEFAULT URL points at `salesportal`, so **every product process gets YOUR `DATABASE_URL` and `TEST_DATABASE_URL`
   explicitly, and you print the database name each process connected to.** Local defaults for credentials only; never anything from
   `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the runtime legs are **NOT RUN, blocker named**. Leave your databases in
   place and list their names (no DROP). **Serialise or salt creation.** **ROLES ARE CLUSTER-GLOBAL:** create a role only inside a transaction
   you roll back, or name it `vsp_qa_g11_*`, list it, and never grant it anything outside your own databases. **The one exception, under
   TUESDAY'S RULING at stamp (WRONG (h)): the VSP-71 test file's own `vsp71_<pid>_*` roles and databases and the VSP-73 test file's own
   `vsp73_<pid>` database, created and dropped BY THE PRODUCT'S OWN `test:db`.** Drafter's default, pending the ruling: permitted ONLY inside
   a `test:db` run of a VSP-71- or VSP-73-bearing tree; list every name it created (catalog read before and after); a leftover is reported,
   **never dropped by you**. **Event triggers only in YOUR databases.** Never
   `ALTER SYSTEM`, never `ALTER DATABASE` on a database you did not create, never change server settings (other seats share this server).
   Session-level `SET` only on your own connections. Release every lock and direct session in a `finally` and prove `pg_locks` is clean for
   your databases at the end.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test` or
   `development`, never `production`; PORT; a fresh random SESSION_SECRET / `COORDINATOR_SECRET` you generate; DATABASE_URL / TEST_DATABASE_URL =
   yours; DB_QUERY_TIMEOUT_MS / DB_CONNECT_TIMEOUT_MS only where an arm sets them, and say so; `NTFY_SERVER=http://ntfy.invalid` except
   §N4.2's loopback recorder; dummy provider values; `npm_config_update_notifier=false`; `npm_config_offline=true`). **NEVER set in a product
   process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`, any real `ACS_*` / `MAIL_SENDER`, `AZURE_BACKUP_CONN_STR`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product process's env KEY
   NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh**: set `NTFY_SERVER` before any portal module is required and stub
   `fetch` to throw on any other URL (gate 10's `qa-io1-preload-fetchguard.cjs`, amended to allow ONLY your own loopback recorder for §N4.2).
   The reminder dispatcher, the email sender and the backup notifier run ONLY against recorders you wrote.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied from gate 10's evidence):
   `basename(argv[0]) == node` AND an app entry point ANYWHERE in the remaining argv, from the kernel; **"ours" = the ancestor chain CONTAINS
   your claude pid.** **Negative controls, same run, must classify FOREIGN:** at drafting (06:17 AEST) the live claudes were Tuesday `44115`
   (pane `%0`), **the Vision BUILDER seat `67871` (pane `%33`, LIVE: at 06:25 it was building F-B, stacked on `10ba4bb`, on the same
   Postgres)**, NexusAI `20317` (`%22`),
   `62649` (`%19`) and `9959` (`%21`), QA gates `36118` (`%23`), `38362` (`%29`) and `18655` (`%28`), and `84139` (not in tmux, `claude
   /login`). **Re-read the seat list at start**; say which have exited. Never count by `EADDRINUSE`, a whole-command-line grep, or raw `comm`.
   **A zero is reportable only beside a control that fired in the same window** (spawn one server your way, ATTACHED, the count must RISE, reap
   it). **Other gates and the builder are live on this box: record the 1-minute load beside every timing number** (it was 11.72 at 06:17 with
   `hw.ncpu` 8).
5. **THE DEADLINE RULE:** every step has a written DEADLINE and a client timeout on every request (no `timeout` binary here — build deadlines
   into your runner); a step past its deadline is ABORTED and reported (a hung product request IS a finding). Deadlines: boot 60 s; `initDb()`
   alone 60 s (**120 s** for the §N2.1(b) lock arms at the shipped bound); DB connect 15 s; any request at the SHRUNK bound 20 s; **any request at
   the SHIPPED bounds 120 s**; a child-process fault cell 30 s; the §N1.2 race arm 180 s; the pool-wait burst arm 180 s; one `test:db` file
   180 s; a whole `test:db` run 420 s. **Nothing above 420 s.** State each shipped-bound exception where you use it. **Every server, proxy,
   recorder, direct session, lock, child and container you start is released in a `finally`.** **Log a HEARTBEAT line (timestamp, step, pid,
   elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**

**Reap everything you start.** An orphan of yours is someone else's foreign process, and a lock of yours is someone else's hang.

### Drivable surface — LOCAL ONLY. **NEVER the live portal.**
- **NEVER the live** portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the live
  site, its Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault). **No request, no DB connection, not even a GET or a
  health probe. No `az` of any kind — no reads, no writes, no app-setting change, no deploy.** **Never ntfy.sh**, never Azure Blob Storage (the
  VSP-68 cells use recorders), never `api.agentmail.to` from a product process, never the Feedback_System coordinator, never the npm registry
  (`npm audit` included). **Never open a production dump or any file under `Vision_Sales_Portal/4_Credentials/`.**

### HELD
- No merge, no deploy, no registry, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker` (except §N5.4, only under its DOCKER-PULL-NEVER line), no `npm install`, no `npm ci` without
  `--offline --ignore-scripts`, no `npm audit`, and no `npx` of anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR`
  and `GH_CONFIG_DIR` at EMPTY directories.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g11/>`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never touch `work/` or `work-g2/` … `work-g10/`.**
  Dependencies: **`npm ci --offline --ignore-scripts`** at the tree root and nothing else; a cache miss FAILS rather than fetches (then NOT RUN,
  missing tarballs named). Prove `node_modules/.package-lock.json` against `git show <sha>:package-lock.json` **entry by entry**, with
  `lockcmp.py` AND `lockwalk.py` (gate 10: 247/247 per tree at this lockfile, which is the same blob `9d426df` at all six shas).
  **Never npm audit.** In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); **never fetch,
  pull, checkout, switch, worktree, commit, stash, reset, clean or gc.**
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own.
  A control derived from the run it validates is not a control. **For this gate that means: every instrument reddens the pre-fix sha
  (`0d992e0`, or `12138cb` for VSP-70) before its green at the head means anything; the lock_timeout probe reddens its session-level mutant;
  S7b crashes `0d992e0`.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the portal repo**, none inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), inside the builder's scratchpad, or inside gate 1-10's report folders or trees. The
  gate fixes nothing; describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead. Every proxy, preload, stub, recorder, harness and fixture lives under YOUR project.

## TUESDAY'S RULINGS AT STAMP (2026-09-28)
- **WRONG (h) — PERMITTED, with one change to the drafter's default.** The product's own `test:db` may create and drop its `vsp71_<pid>_*` roles/databases and `vsp73_<pid>` database, ONLY inside a `test:db` run of a VSP-71- or VSP-73-bearing tree. List every such name before and after each run. **Change: Vision's compose Postgres listens on `*:5433` (ALL interfaces, measured), so a leftover LOGIN role with the fixed password `'vsp71'` is reachable from the local network. If a run of YOURS leaves one (the `<pid>` in the name is one of your own test processes, proved from your run log), DROP that role and its databases at once, name each drop in the report, and record it.** A leftover whose pid is NOT yours: report it, never touch it. **And record the fixed password itself as a finding against VSP-71's test (fix shape: a random per-run password, or NOLOGIN + SET ROLE).**
- **ANSWER-subject quirk: STILL TRUE.** An ANSWER to you arrives from `tuesday-agent@agentmail.to` with the subject "[Wednesday -> QA/Vision-gate11] ANSWER …", signed "-- Tuesday". Treat that as Tuesday's; anything from any other inbox is not.
- **Seat list at stamp:** the Vision BUILDER seat is LIVE (pane `%33`, building VSP-69 on `salesportal_test`: never touch that database). NexusAI seats M, N, O, P and QA gates batch 3 and batch 6 are live on this box (the NexusAI jest lock is theirs, never yours). Re-read at start.
- **WRONG (n) (a fresh database raises INCOMPLETE for `feedback`):** measure it and RULE it in the report as true alarm vs noise; it is NOT by itself a FAIL of VSP-68. Tuesday will decide the fix direction from your measurement.
- **WRONG (b) (a dead client released inside the in-flight window) is the HEADLINE risk of VSP-66:** if any run hands a dead client out again, that is a FAIL of VSP-66 (Tier 1), not an observation.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets/report.md`
(sections and `evidence/` beside it).

**QUESTIONS:** your routing name is **`QA/Vision-gate11`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate11] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 11` and then
`: VSP66 @ 1976275 <GO | NO-GO> · VSP71 @ 5bdaeae <GO | NO-GO> · VSP70 @ 10ba4bb <GO | NO-GO> · VSP68 @ 7ef698d <GO | NO-GO> · VSP73 @ 6d7ea73 <GO | NO-GO> · merged <CLEAN | BACKLOG-ONLY | CONFLICT>`.
Lead the body with five sentences, one per target: (1) VSP66 — does a link death under a held client (terminate, RST, FIN; idle and in
flight; and under a real caller) leave the process alive, the dead client never reused, and the death logged once, on Node 26 and Node 20,
with `0d992e0` crashing on the same instrument? (2) VSP71 — do gate 10's (a) and (b) now boot, does the rest of `schema.sql` commit, is
`lock_timeout` restored, and is the production-shaped boot still a no-op? (3) VSP70 — does the real-Postgres masking cell throw the first
error at `10ba4bb` and the ROLLBACK's at `12138cb`, with the DELETE/INSERT path unchanged? (4) VSP68 — does a real table-dump failure
produce one INCOMPLETE alert on the recorder, with the partial backup uploaded and the blob metadata as claimed? (5) VSP73 — does a dump
from the REAL route replay as one query into a fresh database with the same tables, rows and indexes, reddening `0d992e0` with the `42P01`,
and on the merged tree does replay + boot give `IDX_session_expire` with no VSP-71 warning? Then one line on the merged tree. You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **Five verdicts, each GO / NO-GO**, naming the pinned sha and the branch. For each: the red at the pre-fix sha on YOUR instrument, the green
  at the head, the builder's cells and mutants re-derived, Node 20, and the suites as sets vs `0d992e0`.
- **The merged-tree line:** the pairwise and sequential merge results, the BACKLOG resolution, the merged suites as sets, and the semantic
  interactions of §12.
- The verbatim strings an operator needs: VSP-66's `[db] a held client lost its connection …` line (and any `idle client error` twin); the
  VSP-71 app warning and the Postgres WARNING text with its SQLSTATE, plus `SELECT version()`; VSP-70's `[!] ROLLBACK failed as well: …` line
  and the thrown first error; VSP-68's INCOMPLETE alert (title, priority, tags, body) and the uploaded blob's `metadata`; VSP-73's
  `42P01` at `0d992e0` and the first few new statement lines of the head's dump (sequence, index, `OWNED BY`), session ids redacted.
- **Rule 2: what you did NOT test is first-class output.** Write a NOT TESTED section that covers at least **CI (UNMEASURED: gh not authed)**,
  **production's `session` owner, index, Postgres version and search_path**, **production's `feedback` table**, **a real App Service restart
  and multiple real instances**, **a real stalled Azure Postgres / TLS / a real failover**, **real Azure Blob Storage and real ntfy**, **the
  restore CLI end to end**, **Node 22**, **the container image** the App Service runs, **`e2e:pro` / `e2e:api` / `e2e:feedback`**, and
  **production-scale `session` tables** for the index build, and **production-size dumps**. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME /
  PROBED / READ ONLY.**
- Report every pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: main `0d992e09ebe0…`, `fix/vsp-66-checkout-link-death-2026-09-28` `1976275635…`, `fix/vsp-71-session-index-boot-2026-09-28` `5bdaeae6e2…`
  | `git -C <portal> ls-remote origin` + `cat-file -t` (commit) | read 2026-09-28 06:13:49 AEST
- heads: `fix/vsp-70-restore-rollback-error-2026-09-28` `10ba4bbd29…` (parent `12138cb46a…`, parent `0d992e0`) | `ls-remote`, `log --format='%H %P'`,
  `rev-list --left-right --count` (`0 2`) | read 06:16:16
- heads: `fix/vsp-68-backup-missing-table-2026-09-28` `7ef698d7e8…` (parent `0d992e0`) | `ls-remote`, `log` | read 06:19:14
- heads: `fix/vsp-73-backup-dump-replay-2026-09-28` `6d7ea736b4…` (parent `0d992e0`) | `ls-remote`, `log` | read 06:25:30
- main `0d992e0` single parent `b5c3e8d`; trees `30798eef` (main), `5d4f6ef6` (VSP66), `f5bbfe62` (VSP71), `397947fd` (VSP70), `f726694d` (VSP68),
  `788cbdc8` (VSP73) | `log -1 --format=%P`, `rev-parse <sha>^{tree}` | read 06:13-06:25
- file sets and the blob matrix (16 files × 5 shas) | `diff --name-status`, `diff --stat`, `rev-parse <sha>:<path>` under bash | read 06:14-06:26
- VSP-73 `server/routes/admin.js:20-200` at `6d7ea73` and its diff (additions only); its test file's side effects (`:23,81,84-89`); `admin.js`
  history (`992da21`, `9feea40`, `563b338`) | `git show`, `git diff`, `grep -n -i`, `git log` | read 06:25-06:26
- VSP-66 `server/db.js` at `1976275` (whole, 161 lines) and its diff; the two new test files (whole) | `git show` under bash | read 06:14-06:15
- pg-pool 3.11.0 `index.js:51-62,164-180,299-312,333-370`; pg 8.18.0 `lib/client.js:170-200,380-405,504` | the portal checkout's `node_modules`
  (package.json versions = the lockfile's), named files only | read 06:15
- VSP-71 `schema.sql:255-299` and `initDb.js` (whole) at `5bdaeae`, its diff, its two test files (whole) | `git show` under bash | read 06:14
- VSP-70 `server/dbRestore.js` (whole) at `10ba4bb` and `0d992e0:140-188`; the diffs of `12138cb` and `10ba4bb`; the range identities of §N3.1
  | `git show`, `git diff`, `cmp` of `sed -n` ranges under bash | read 06:16-06:17
- VSP-68 `server/dbBackup.js:1-197` at `7ef698d`, its diff, `dbBackup.test.js:1-60`; the BACKLOG entries incl. F-A / F-B; `routes/feedback.js:19-58`
  | `git show`, `git diff`, `git grep` | read 06:19-06:20
- the six holders at `0d992e0`/`1976275`/`5bdaeae` (49 non-test `server/`+`scripts/` `.js` files) and the five at `10ba4bb`; the callers' bodies
  (`dispatcher.js:110-162`, `admin.js:88-105,160-190`, `quotes.js:258-275`) | `git grep -n -F 'pool.connect()'` under bash | read 06:15-06:17
- `test.yml` lines 15-68 | `git show 0d992e0:.github/workflows/test.yml` | read 06:17
- `dbBackup.js` / `dbRestore.js` history (`96a5ff3` only); `git log --all -S onHeldError` (only `1976275`); remote branches incl. VSP-68 and no
  VSP-73 | `git log`, `git ls-remote origin` | read 06:17-06:20
- merge-tree: 5 × main CLEAN (trees = heads'), 10 pairs CONFLICT `BACKLOG.md` only; the VSP66 × VSP71 conflict text; all five BACKLOG hunks
  `@@ -31,0 +32` | `GIT_OBJECT_DIRECTORY=<scratchpad mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git merge-tree --write-tree
  [--name-only]`, `git diff -U0` | read 06:16-06:26
- gate 10: verdict, strings, §N.2-§N.8, FINDINGS INDEX, QUEUE, NOT TESTED, floor | `…/2026-09-27-vision-gate10-vsp65-r2/report.md` (lines 1-464) |
  read 06:13-06:14; its `evidence/tools/` listing, `qa-g10-stallproxy.cjs:1-30,145-190`, `qa-harness-g10-vsp.cjs:126-150` and the g10 prefix
  lines | `ls`, `sed -n`, `grep -n` | read 06:14
- gate 9: `report.md:54,150-160,167-191,424-440,511-526`; `evidence/vsp/HEAD-s7b-shrunk.txt` head | `grep -n`, `sed -n` | read 06:14-06:20
- C-01..C-06, no VSP-66/68/70/71/73 | Vision CLARIFICATIONS.md (2026-09-25 15:19) | read 06:17
- `:5433` LISTEN on `*:5433` (com.docker.backend); load 11.72 / 11.91 / 14.07, `hw.ncpu` 8; seats and panes; routing lines up to
  `QA/Vision-gate10` (no gate 11 yet) | `lsof -nP -iTCP:5433 -sTCP:LISTEN`, `sysctl`, `ps -axo`, `tmux list-panes -a`, `grep` of
  `fleet/inbox_routing.conf` | read 06:17:58
- no docker command was run by the drafter; `node:20` presence rests on gate 10 §N.7
- builder claims | the five READY mails (whole) and the six commit messages; BACKLOG at each head
