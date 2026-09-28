# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 14: ONE batched TIER 2 gate on portal main `6dbffdf`, SEVEN targets — VSP-76 @ `f593e38` (dead client handed out), VSP-77 @ `da62873` (session-index test hygiene), VSP-78 @ `1de6d92` (another role's replay no longer crash-loops the boot), VSP-79 @ `241b8bb` (backup-db and a mixed-case sequence), VSP-80 @ `28adf36` (supertest on 127.0.0.1), VSP-82 @ `ccfc7ef` (the dispatch cutoff), VSP-85 @ `b78d2e3` (backup test gaps) — seven verdicts, one merged line, one report

**All seven are TIER 2 (through-code) and ROUND 1 of their own tickets.** No NO-GO has been spent on any of them. Each was filed from an
earlier gate's finding (gate 11: VSP66-G11-F1, VSP71-G11-P1/P2, G11-M1, G11-O3; gate 12: VSP69-G12-F1, VSP75-G12-O3/O4) or, for VSP-80, from a
harness incident the builder traced (BACKLOG, 2026-09-27). A NO-GO sends that ticket to its round 2; it does not go to Kam. Tuesday confirms
the class counts at stamp (§TUESDAY'S RULINGS item 4).

**Drafted for Tuesday on 2026-09-29 between 06:4x and 07:2x AEST by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Template: gate 13's brief `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-gate13-vsp74r2-vsp75.md`
(read it as PRIOR WORK for method, §13 and instruments; **this brief governs where they differ**). The commission named three targets (VSP-76,
VSP-78, VSP-82); Tuesday's three ADDENDA added VSP-85, then VSP-80, then VSP-77 and VSP-79 ("the last addendum"). The file names were settled
at seven: this brief `2026-09-29_vision-gate14-seven-targets.md`, the report folder `2026-09-29-vision-gate14-seven-targets`, and the per-gate
launcher `launch_qa_vision_gate14.sh` (as every earlier Vision gate launcher is named).

**WHY ONE BATCHED GATE, AND WHY THE MERGED TREE IS THE KEY MEASUREMENT (read this before planning).** All seven sit linearly on main `6dbffdf`
(no merges, 0 behind). Together they change **23 files**, none of them `BACKLOG.md`. **Two files are shared:** `server/routes/admin.js` (VSP-78's
one dump-header line; VSP-79's sequence loop, ~70 lines away) and `test/db/backup-coverage.test.js` (VSP-80's `require` and `serve` lines 20/47;
VSP-85's census rewrite). Every other pair is path-disjoint. **What git cannot see:** VSP-80 changes `test/db/helpers.js`, which every DB test
file loads, and claims "0 bare call sites" — but VSP-79's NEW test file (built off `6dbffdf`, before VSP-80 existed) hands supertest a bare
app (§WRONG (t)); VSP-76 changes the client every query goes through (the dispatcher's held client included: VSP-82); VSP-78 changes the index
VSP-82's rules depend on and the dump VSP-79 fixes; VSP-77 pins a concurrent-boot race on the `schema.sql` VSP-78 rewrites. **So §N8 (all seven
on main: sets by name, 0 lost; the two overlaps; the forced-hazard sweep that proves supertest now binds 127.0.0.1) is the measurement the merge
rests on.** Weight per target: cells, mutants, controls, verifies; the four product changes (VSP-76, 78, 79, 82) carry red-first cells on main;
the three test-only changes (VSP-77, 80, 85) carry mutant re-derivation and a not-weakened check.

The builder's READY mails under test (on disk beside this brief, each read whole by the drafter):
`2026-09-29_vision-vsp76-READY-mail.txt` (with its evidence-line correction), `2026-09-29_vision-vsp77-READY-mail.txt`,
`2026-09-29_vision-vsp78-READY-mail.txt` (the `c74d7fd` READY; its content stands) with `2026-09-29_vision-vsp78-newhead-READY-mail.txt` (new head
`1de6d92`: teardown only), `2026-09-29_vision-vsp79-READY-mail.txt`, `2026-09-29_vision-vsp80-READY-mail.txt`, `2026-09-29_vision-vsp82-READY-mail.txt`,
`2026-09-29_vision-vsp85-READY-mail.txt` (its Dependabot note is OUT OF SCOPE: do not act on it).
**Every builder statement below comes from those mails, the commit messages or the code at each head. Each one is a CLAIM. Every red, every
mutant and every suite set must be RE-DERIVED by the gate. None is taken from a READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 07:19
Self-check note: read whole by Tuesday (s92) before stamping; the drafter's WRONG list (a)-(x) accepted as written; rulings 2-5 adopted as the drafter proposed; NODE20-LEG kept DOCKER-PULL-NEVER as gates 11-13; the negative-control seats are re-read by the gate at start (the Vision seat %44 was closed by Tuesday at 07:08).

NODE20-LEG: DOCKER-PULL-NEVER
<!-- Carried from gates 11-13 (each ran DOCKER-PULL-NEVER: `docker image inspect node:20` then `docker run --rm --pull=never` of the image
     ALREADY present; nothing is ever pulled; if the image is absent the leg is NOT RUN and the report says so). Tuesday may set NOT-RUN at
     stamp for a tier-2 batch. The drafter read `docker image inspect node:20` = sha256:8f693eaa…, arm64 (same digest as gates 12-13). -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build any of these changes and you owe the builder nothing. **Every line below that reports what the builder says
is a CLAIM, never evidence.**

**One gate, SEVEN targets, SEVEN verdicts (GO / NO-GO each, at its pinned sha), plus ONE merged-tree line.**
- **VSP76** at `f593e38` — **TIER 2 (through-code).** Jira VSP-76 (High) = gate 11's **VSP66-G11-F1** + Jira comment 38535 (the dispatcher's
  failed-ROLLBACK catch). `server/db.js` `guard()`: a query that rejects with severity FATAL, SQLSTATE class 57P or 08, or on a client pg already
  reads as unqueryable, marks the client BROKEN; `release()` passes `err || TIMED_OUT || BROKEN`, so pg-pool discards it.
- **VSP77** at `da62873` — **TIER 2 (through-code), TEST FILE ONLY.** Jira VSP-77 (Low) = gate 11's **VSP71-G11-P1 + P2**
  (`test/db/session-index-boot.test.js`): the boot-test role's password is random per run (was the fixed `'vsp71'`), and a new cell pins
  `WHEN OTHERS` with 5 pairs of concurrent boots (gate 11's mutant M5 must fail it).
- **VSP78** at `1de6d92` — **TIER 2 (through-code).** Jira VSP-78 (Medium) = gate 11's **G11-M1**. `server/schema.sql`: each of 16 indexes is made
  only when `to_regclass()` finds it missing; 15 fail soft (`EXCEPTION WHEN OTHERS … RAISE WARNING`); **`idx_reminders_rule_key` (UNIQUE) does not:
  missing and unmakeable still fails the boot.** `server/initDb.js`: ONE WARN line naming every public table the portal's role cannot
  SELECT/INSERT/UPDATE/DELETE and every sequence it cannot USAGE (**C-10 ruling 1: the WARN shape is ACCEPTED; whether it fires correctly is this
  gate's question**), and ONE line naming any guarded index still missing. `server/routes/admin.js`: one dump-header comment line. The new head
  changes ONLY the test file (teardown, C-10 ruling 2).
- **VSP79** at `241b8bb` — **TIER 2 (through-code); a production-reachable route fix.** Jira VSP-79 (Low) = gate 11's **G11-O3**
  (`GET /api/admin/backup-db` answered 500 on a mixed-case sequence). `server/routes/admin.js`: the catalog lookup's `$1::regclass` gets
  `quoteIdent(sequence_name)`, and the dump's `setval` gets `sqlLiteral(quoteIdent(name))`. New `test/db/backup-db-sequence-names.test.js`.
- **VSP80** at `28adf36` — **TIER 2 (through-code), TEST HARNESS ONLY.** Jira VSP-80 (Low). New `test/loopback.js` `serve(app)` =
  `http.createServer(app).listen(0, '127.0.0.1')`, awaited; every supertest call site in its tree takes a served server; `helpers.closeDb()` closes
  the servers first. The hazard: supertest's own `app.listen(0)` binds `[::]`, then requests `127.0.0.1`, where another process (a LogiPlugin
  listener on this Mac) can hold the port.
- **VSP82** at `ccfc7ef` — **TIER 2 (through-code).** Jira VSP-82 (Medium) = gate 12's **VSP69-G12-F1**. `dispatchDue()` reads `SELECT NOW()::text`
  and compares `due_at <= $1::timestamptz`. **Its "CLIENT REACH: NONE" is a CLAIM this gate verifies: client reminders on the millisecond grid are
  decided identically to main, and nothing is ever sent before it is due.**
- **VSP85** at `b78d2e3` — **TIER 2 (through-code), TEST FILES ONLY.** Jira VSP-85 (Medium) = gate 12's **VSP75-G12-O3/O4**
  (`test/db/backup-coverage.test.js`, `server/dbBackup.test.js`). Re-derive its four mutants (M6-M9) independently, confirm no cell removed or
  weakened, sets 0 lost.
- **MERGED LINE:** all seven on main `6dbffdf`, from YOUR OWN object dir (§N8): conflict-free or not; the two overlaps; the merged tree equals
  main + the heads' blobs (+ the two merged files); sets as names vs main (0 lost); the forced-hazard sweep; the merged coverage against CI's 80%
  line gate; the cross-target cells.

**⚠ Names, written out every time:**
- **VSP76 = gate 11's VSP66-G11-F1**: after an in-flight `pg_terminate_backend`, a holder that releases in the same tick hands the DEAD client to
  the next caller (20/20 at gate 11, silent at main; a real caller: `GET /api/admin/backup-db` terminated in flight, and an innocent queued
  `/api/auth/me` answered 500).
- **VSP77 = VSP71-G11-P1** (a LOGIN role with the fixed password `'vsp71'` on a Postgres listening on every interface) **+ P2** (no cell pinned
  `WHEN OTHERS`: gate 11's M5, the narrow catch, passed all five cells and failed its concurrent-boot pairs arm 6/6 with `23505`).
- **VSP78 = G11-M1**: a whole-dump replay by another role makes that role own every table; the next boot failed `42501 must be owner of table
  leads` on `schema.sql`'s `CREATE INDEX IF NOT EXISTS`: a crash-loop.
- **VSP79 = G11-O3**: with a table `"QA_Mixed_Case"` (serial) the route answered 500 at every sha (`relation "qa_mixed_case_id_seq" does not
  exist`): the unquoted `$1::regclass` folded the name.
- **VSP80**: a random 501 or "socket hang up" in DB cells (five occurrences 2026-09-23 to 2026-09-29, the last in VSP-86's first full run).
- **VSP82 = VSP69-G12-F1**: the tick's cutoff was a JS `Date` (millisecond floor); a reminder with `due_at = NOW()` waited one tick (gate 12:
  125/300 and 106/300 at `e79682a`, 72/300 merged, 0/300 at `609e967`).
- **VSP85 = VSP75-G12-O3 + O4**: the drift census missed a plain `CREATE TABLE`, a schema-qualified name and `scripts/`; every stub fault landed on
  the PK lookup, none on the row SELECT.

Branches: `vsp-76-dead-client-handoff`, `vsp-77-session-index-test-hygiene`, `vsp-78-restore-role-boot`, `vsp-79-mixed-case-sequence`,
`vsp-80-supertest-loopback`, `vsp-82-dispatch-cutoff`, `vsp-85-backup-test-gaps`. **None is on main.** (`vsp-83-old-backup-dates` and
`vsp-86-restore-clears-sessions` also exist on origin: NOT in this gate.)

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole. The drafter read C-01..C-12 (header, QuickQuote list, and the Portal section whole; C-12 appeared while drafting). **The ones that bear on this gate:**
  - **C-10 (new 2026-09-29, Tuesday's rulings, recorded by the Vision agent; not Kam's):** "VSP-78: when the portal's role lacks table or sequence
    privileges, the boot WARNS, it does not fail; tests tear down their own fixtures." Ruling 1: the WARN design "ratifies the SHAPE of the choice
    only; whether the warning fires correctly is the gate's question. Tuesday reports it to Kam as a boot-behaviour change with the one-line revert
    you named; his word overrides." Ruling 2: "a committed test drops the databases and roles IT created, in its own after()" and "Leftovers from
    earlier runs stay in place for Kam." (VSP-79's test also cites it for its table + sequence.) Ruling 3: `feedbackDigest.js`'s unguarded
    `CREATE INDEX` on `feedback` is **VSP-88** (out of scope). "Built at `1de6d92`."
  - **C-08 (Kam, 2026-09-28):** main fast-forwarded `e59232e` → `110bb03` (gate 13's VSP-75 GO head, VSP-74 round 2 inside it) and then the
    BACKLOG follow-up `6dbffdf`. **That is why main is `6dbffdf`; VSP-74's class is NOT under test here.**
  - **C-09 (Kam, signed, 2026-09-28):** production `idle_in_transaction_session_timeout` = 600000 ms. **For VSP-76 this makes a backend FATAL
    `25P03` a production-real death shape** (a client held idle in a transaction for 10 minutes); §N1.3 includes it.
  - C-11 (VSP-83, old-backup DATEs) is **not in this gate** (Tuesday ruled VSP-83 TIER 1, gated separately).
  - **C-12 (appeared at 07:1x, during drafting; Tuesday's rulings of 2026-09-28T20:47-20:52Z):** VSP-86 (the restore clears `session`) is TIER 1,
    gated with VSP-83 — **not in this gate**; the Lows' build order was "VSP-80, VSP-77, VSP-79"; **VSP-72 is PARKED: "pre-existing, needs two first
    boots on an empty database at once"** — so the race of two FIRST boots on an EMPTY database is not graded here; §N2.4's pairs arm runs on an
    EXISTING database with indexes dropped (a different shape), and if it meets the VSP-72 shape, it is recorded as VSP-72's, not graded. VSP-84
    parked (production size).
  The launcher checks C-08..C-12 are present and C-10 names `1de6d92`, and prints a NOTE on any C-13.
- **PRODUCTION IS LIVE for this project.** `datasec-sales-portal-rg` holds the live site `https://datasec-sales-portal.azurewebsites.net`,
  its production Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault `datasec-sales-kv`. Production runs Node 20
  (`.github/workflows/test.yml`, blob `0cb2d05`, unchanged at every head). **On merge, VSP-76 runs on every held client, VSP-78 on every boot,
  VSP-79 on every backup-db request, VSP-82 on every tick. Nothing in this gate touches production** (§13, HELD).
- **Tuesday's rulings on VSP-78 (from the commission, not Kam's):** (1) WARN, not fail the boot, on missing privileges is ACCEPTED AS A SHAPE —
  whether it fires correctly is the gate's; (2) the test drops its own fixtures; (3) the `feedbackDigest` index is VSP-88 (out of scope). **The
  unique-index exception (`idx_reminders_rule_key`) must still fail the boot: §N2.2 is the REQUIRED CELL for it.**
- **Tuesday's commission on VSP-79:** a production-reachable route fix (backup-db 500 → 200): **a REAL-ROUTE cell with a mixed-case sequence, red
  on main** (§N3.1).
- **Deploys are HELD for Kam. Nothing merges on your word.** A merge is Tuesday's GO on a pinned head. A deploy is Kam's word.

## PRIOR ROUND
PRIOR ROUND: gates 11, 12 and 13 (QA/Vision-gate11, -gate12, -gate13; 2026-09-28). No earlier round exists for any of the seven tickets.
ITS REPORT IS ON DISK AT: gate 11 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets`
(`report.md`, 655 lines). **Read at least: N1.2 (the release window, 20/20 at both shas, and "Why"), N1.3 (real callers), N1.5 (listener
hygiene), N2.5, N2.8 (concurrent boots), N2.9 (M5 → G11-P2), N2.10, N6.4 (cells (i)-(vi); (ii)/(iii) are G11-M1), N6.5, N6.6 (the mixed-case
`"QA_Mixed_Case"` route 500: G11-O3), FINDINGS INDEX (VSP66-G11-F1 with its regression cell `window:terminate:immediate:product` / `…:max1`;
G11-M1; VSP71-G11-P1/P2; G11-O3), THE QUEUE, NOT TESTED.**
ITS REPORT IS ON DISK AT: gate 12 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets`
(`report.md`, 700 lines). **Read at least: the VSP69 verdict, N3 (N3.1-N3.8: the dispatch instrument, M2, black hole, SIGKILL, churn, N3.7's
cutoff arm), N2.2 (27/27 stub faults on the PK lookup; O4), N2.5 (census M6/M7 survive; O3), FINDINGS INDEX (VSP69-G12-F1 with its regression
cell "100/100"; VSP75-G12-O3/O4), N5.2-N5.6.**
ITS REPORT IS ON DISK AT: gate 13 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate13-vsp74r2-vsp75`
(`report.md`, 546 lines): the most recent Vision gate and the source of the generic instruments. **Read: N2.5-N2.8 (suites, coverage 80.80 /
76.18 at `110bb03`, hygiene, Node 20), self-findings 1-7, Floor.**
- **Instruments are REUSED BY COPY. Never edit, run from, or write into gate 1-13's copies, evidence, trees or databases.** COPY what you use into
  THIS gate's own `evidence/tools/`, read it before you trust it, record its sha1 before and after your edits, and RE-POINT every hard-coded
  path and prefix (they ENFORCE `vsp_qa_g11_` / `vsp_qa_g12_` / `vsp_qa_g13_` and hard-code `work-g11` / `work-g12` / `work-g13`).
  - **From gate 11's `evidence/tools/`, for VSP-76, VSP-77, VSP-78 and VSP-79:** `qa-g11-n1-child.cjs` (**sha1
    `39044865e0f4aff2f08d242dcbd30c1b71530b9e`, the same bytes in gate 12's folder; the launcher checks it**), `qa-g11-stallproxy.cjs` (sha1
    `61681e54…`), `qa-g11-n1.cjs`, `qa-g11-arms.cjs`, `qa-harness-g11-vsp.cjs`, `qa-harness-g11-schema.cjs`, `qa-g11-n2.cjs`, `qa-g11-n6.cjs`,
    `qa-g11-lib.cjs`, `qa-g11-sql.cjs`.
    **THE VSP-76 RED CELL IS GATE 11'S OWN TOOL, `qa-g11-n1-child.cjs`, by path, read-only** — and it cannot be run unmodified by you: it refuses
    any database not matching `^vsp_qa_g11_\d+(_test)?$` (line 26) and loads its pg client from `work-g11/ptree-TOOLS-pgclient.*` (lines 21-23).
    So: COPY it and `qa-g11-stallproxy.cjs` (hash-verified against the sha1s above), change **exactly two things** — the `WK` path (to your own
    `work-g14` pg-client tree) and the DB regex (to `^vsp_qa_g14_\d+(_test)?$`) — and prove by `diff` against the pinned original that nothing else
    changed. **Never create a `vsp_qa_g11_*` database** (the builder did: §WRONG (a)).
  - **From gate 12's `evidence/tools/`, for VSP-82:** `qa-harness-g12-disp.cjs`, `qa-g12-disp.cjs` (SDK replaced through `require.cache`, a
    synchronous send log, black hole, SIGKILL, the 300-run cutoff arm), `qa-g12-cellrun.py`.
  - **From gate 13's `evidence/tools/`, generic:** `qa-run.py`, `mktree-portal.sh`, `qa-mkdb.cjs`, `run-suite.sh`, `lockcmp.py`, `lockwalk.py`,
    `specsets.py`, `tapsets.py`, `dupcount-g13.py`, `qa-floorcount.py`, `floor-g13.sh`, `qa-harness-floorctl.mjs`,
    `qa-io1-preload-fetchguard.cjs`, `qa-g13-lazywatch.cjs`, `qa-g13-clusterlist.cjs`, `run-node20-g13.sh`, `qa-g13-node20.cjs`.
  Earlier gates' roles (`vsp_qa_g10_*` … `vsp_qa_g13_*`) are not yours: never use, alter or drop them.
- **Self-findings from gates 2-13 bind you:** quote every path (the project path has a space and a `!`); run every loop and every
  `git show <sha>:<path>` under **bash, not zsh** (gate 12 and gate 13 self-finding 1: a zsh loop did not word-split; zsh also reads `$H:t…` as a
  modifier — write `"${H}:path"`); pass SQL to a wrapper as base64, never through a whitespace-split env var; absolute recorder paths; **the
  portal test-DB name MUST end in `_test`**; an asserted edit must be checked for its SEMANTICS, not just its anchor (gate 13 self-finding 2);
  scratch files go in YOUR project folder, never `/tmp` (gate 13 self-finding 5); npm's update-notifier egresses unless you disable it; record
  the load average beside every timing number.
- **PRIOR WORK: verify every claim against git history and the earlier gates' evidence, never against this brief.**

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head, base and commit count, and no `@`; the head is a commit; the base is
main `6dbffdf`, an ancestor AND the merge-base with MAIN; `git rev-list --count base..head` equals `commits`; the non-merge commits over the base
are exactly the chains below and there are NO merges; `git ls-remote origin refs/heads/<branch>` equals the head NOW; no target is on main; each
target's file set is exactly as listed; **the pairwise overlaps are exactly the two named (admin.js: VSP78 × VSP79; backup-coverage.test.js:
VSP80 × VSP85) and nothing else, and no target touches `BACKLOG.md`** (exit 80). **Main:** origin main must be `6dbffdf` or a DESCENDANT of it
whose diff from `6dbffdf` touches none of the targets' files (NOTE); anything else refuses. `6dbffdf`'s single parent is `110bb03` and
`110bb03..6dbffdf` touches `BACKLOG.md` only.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | 6dbffdf36c98aac74d32eaae16e4563966cef42c | - | - | IN |
| VSP76 | portal | vsp-76-dead-client-handoff | f593e38198e6110c6013d24644611b341cc8754e | 6dbffdf36c98aac74d32eaae16e4563966cef42c | 2 | IN |
| VSP77 | portal | vsp-77-session-index-test-hygiene | da6287321b3c0ce6561e4601d70661469081d73c | 6dbffdf36c98aac74d32eaae16e4563966cef42c | 1 | IN |
| VSP78 | portal | vsp-78-restore-role-boot | 1de6d92f67cd4db5b568fcb6de0b60127c408b99 | 6dbffdf36c98aac74d32eaae16e4563966cef42c | 3 | IN |
| VSP79 | portal | vsp-79-mixed-case-sequence | 241b8bb646a401f04eeab2d8be87f0ca18f72885 | 6dbffdf36c98aac74d32eaae16e4563966cef42c | 1 | IN |
| VSP80 | portal | vsp-80-supertest-loopback | 28adf36579ed0136df38c2e1bbe132caf44823fb | 6dbffdf36c98aac74d32eaae16e4563966cef42c | 1 | IN |
| VSP82 | portal | vsp-82-dispatch-cutoff | ccfc7ef60c4421847755a3ce7f5afc866b60263b | 6dbffdf36c98aac74d32eaae16e4563966cef42c | 1 | IN |
| VSP85 | portal | vsp-85-backup-test-gaps | b78d2e314b6a930d897ed4b5986431d4139962f3 | 6dbffdf36c98aac74d32eaae16e4563966cef42c | 1 | IN |
<!-- PIN-HEADS:END -->

Every row above: `git -C <portal> ls-remote origin` read by the drafter at **2026-09-29 06:46:47 AEST** (main, VSP76, VSP78, VSP82), **06:50:40**
(+ VSP85), **07:05:30** (+ VSP80) and **07:05:58 AEST** (all eight rows, the last read), each equal to its READY's head (the READYs give 12 hex, or
7 for VSP-79; full values from ls-remote); `cat-file -t` = commit for all eight. Counts by `rev-list --count` (06:47-07:06).

**The chains (READ, `rev-list --no-merges`, `log --format='%h %p %ad %s'`; no merges in any; every parent chain starts at `6dbffdf`):**
- **VSP76 (2):** `79ec3cd` (06:12:13 +1000, "discard a client whose query died on a connection-class error") → `f593e38` (06:21:50, "unit cells for
  the connection-error classes; fix a race in the keep-cancel child").
- **VSP77 (1):** `da62873` (06:52:26, "random password for the boot-test role; pin WHEN OTHERS with a concurrent-boot cell").
- **VSP78 (3):** `788477f` (06:30:36, the boot-FAILING access check) → `c74d7fd` (06:33:28, "report unusable tables at boot instead of failing
  it") → `1de6d92` (06:38:48, "the restore-role test drops the databases and roles it made"; **the test file only**).
- **VSP79 (1):** `241b8bb` (07:00:44, "quote sequence names in backup-db, in the catalog lookup and the dump").
- **VSP80 (1):** `28adf36` (06:58:47, "serve every supertest app on 127.0.0.1 before supertest sees it").
- **VSP82 (1):** `ccfc7ef` (06:38:08, "keep the dispatch cutoff in Postgres's precision").
- **VSP85 (1):** `b78d2e3` (06:46:50, "close the backup tests' census and row-SELECT gaps").

Repo: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`). **The portal has no CLAUDE.md inside the repo;** its rules are
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (read it; its deploy commands are NOT for you).

**The shape (READ at the pinned heads; re-derive it). 23 files; the only shared files are marked ⚑:**
| target | file | main `6dbffdf` | head | numstat | `test(` main → head |
|---|---|---|---|---|---|
| VSP76 | `server/db.js` | `5d42db6` | **`cd12c78`** 186 l | +33/−8 | — |
| VSP76 | `server/db.test.js` | `1f59ff2` | **`8e10e3a`** | +57/−1 (the `require`) | 4 → 7 top-level (+2 in a `for (form …)` loop = +5 names) |
| VSP76 | `test/db/checkout-link-death.child.js` | `f694fdd` | **`f79a272`** | +107/−1 (the `require`) | — |
| VSP76 | `test/db/checkout-link-death.test.js` | `bcc950f` | **`0b5d793`** | +57/−0 | 6 → 13 |
| VSP77 | `test/db/session-index-boot.test.js` | `79de198` | **`ebc17ed`** | +23/−1 (the password) | 5 → 6 |
| VSP78 | `server/schema.sql` | `74f6e9c` | **`2193f21`** 311 l | +28/−16 | — |
| VSP78 | `server/initDb.js` | `68fc8cc` | **`66e55e4`** | +40/−0 | — |
| VSP78 ⚑ | `server/routes/admin.js` | `7b00469` | **`681c874`** | +1/−0 (line 113) | — |
| VSP78 | `test/db/restore-role-boot.test.js` | — | **`877a8e5`** 169 l | new | 5 |
| VSP79 ⚑ | `server/routes/admin.js` | `7b00469` | **`10489b2`** | +3/−2 (lines 183-190) | — |
| VSP79 | `test/db/backup-db-sequence-names.test.js` | — | **`5bf8e24`** 68 l | new | 2 |
| VSP80 | `test/loopback.js` | — | **`44da81a`** | new | — |
| VSP80 | `test/db/loopback.test.js` | — | **`2791bf4`** | new | 2 |
| VSP80 | `test/db/helpers.js` | `1d90638` | **`dde7058`** | +3/−1 | — |
| VSP80 | `server/errors.test.js`, `test/db/{async-faults,backup-dump-replay,completed-response,concurrency,routes}.test.js` | … | … | +2..+8 / −1..−5 each | unchanged (9, 5, 4, 3, 5, 18) |
| VSP80 ⚑ | `test/db/backup-coverage.test.js` | `5ffb1fe` | **`76f7c3d`** | +2/−2 (lines 20, 47) | 6 → 6 |
| VSP82 | `server/reminders/dispatcher.js` | `7a67be9` | **`d9f733d`** | +7/−2 | — |
| VSP82 | `test/db/dispatch-cutoff.test.js` | — | **`7d508ea`** 78 l | new | 3 |
| VSP85 | `server/dbBackup.test.js` | `12a6e24` | **`5864161`** | +22/−2 | 10 → 11 |
| VSP85 ⚑ | `test/db/backup-coverage.test.js` | `5ffb1fe` | **`e9064be`** | +46/−18 | 6 → 9 |
**Same blob at every head and main:** `package.json` `d3b76fb`, `package-lock.json` `9d426df`, `.github/workflows/test.yml` `0cb2d05`,
`test/db/dispatch-once.test.js` `c3b0d92`, `test/db/session-index-boot.child.js` `7ead7a3`.
**The two overlaps, PROBED by the drafter** (`git merge-file -p` on scratch copies of the three blobs each, in the drafter's scratchpad; nothing
written to any repo): `admin.js` (base `7b00469`, VSP78 `681c874`, VSP79 `10489b2`) → **clean**, merged content hashes to `b967b9d`;
`backup-coverage.test.js` (base `5ffb1fe`, VSP85 `e9064be`, VSP80 `76f7c3d`) → **clean**, `b26d38e`, carrying both VSP-80's `serve` lines (20, 87)
and VSP-85's census. **Re-derive both from YOUR OWN object dir; the drafter's hashes are a prediction.**

**The code (READ; re-derive):**
- **VSP76 `server/db.js`:** `isConnectionError(err, client)` = `client._queryable === false` OR `err.severity === 'FATAL'` OR `err.code` starting
  `57P` or `08`. In `guard()`'s `name(err)`: the DB_QUERY_TIMEOUT path unchanged; else `if (!client[BROKEN] && isConnectionError(err, client))
  client[BROKEN] = err`. `release()` → `release.call(this, err || client[TIMED_OUT] || client[BROKEN])`. Submittables still bypass the wrapper.
- **VSP77:** `PASSWORD = require('crypto').randomBytes(16).toString('hex')`; the new cell: 5 pairs, each on a fresh DB after one full boot,
  `DROP INDEX "IDX_session_expire"`, two `initDb()` children at once, both must resolve and the index must exist. The file's `after()` drops
  `vsp71_<pid>_boot` / `_owner` unconditionally (pre-existing); roles are created only when absent (line 51).
- **VSP78 `server/schema.sql`:** 16 index statements rewritten as `DO $$ BEGIN IF to_regclass('<name>') IS NULL THEN CREATE [UNIQUE] INDEX …
  END IF; … END $$;`. The drafter checked all 16: the `to_regclass` literal, the `CREATE INDEX` name and the `RAISE WARNING` name agree in every
  block, and **the 16 index definitions are byte-identical to main's** (normalised extraction, 0 diff). 15 carry `EXCEPTION WHEN OTHERS THEN RAISE
  WARNING '<name> not created (% %) (VSP-78)'`; `idx_reminders_rule_key` carries none. No lock_timeout on the 15. No `CREATE … INDEX IF NOT
  EXISTS` statement remains (two comment lines mention it).
- **VSP78 `server/initDb.js`:** `reportAccess()` runs right after `schema.sql`, **not wrapped in a try/catch**: one `pg_class` query over `public`
  `relkind IN ('r','p','S')` with a `CASE` (sequences: `NOT has_sequence_privilege(oid,'USAGE')`; tables: NOT all four of
  `has_table_privilege(oid,'SELECT'|'INSERT'|'UPDATE'|'DELETE')`, each asked separately); on any row, ONE `console.warn` line `[db] the portal's
  database role (<current_user>) cannot use N object(s): <kind name, …>. …(VSP-78)`. After VSP-71's check, the names parsed from `schema.sql` by
  `/to_regclass\('(\w+)'\) IS NULL THEN CREATE INDEX/g` (**15: the UNIQUE block does not match**) that `to_regclass()` cannot find are named in ONE
  line. `initDb.js:135`'s `CREATE UNIQUE INDEX IF NOT EXISTS uq_quotes_poc_credit_once` is pre-existing and fail-soft (READY; re-derive).
- **VSP78 test:** 5 cells, each on its own `vsp78_<pid>_<name>` DB made `OWNER vsp78_<pid>_boot`; `vsp78_<pid>_other` (NOLOGIN) replays
  `schema.sql` as ONE query under `SET ROLE`; the boot runs VSP-71's `session-index-boot.child.js` (exit 3 = rejected). `after()` terminates and
  drops each DB in `made[]`, then each role in `rolesCreated[]` (a pre-existing role is reused and neither recorded nor dropped).
- **VSP79 `server/routes/admin.js:176-191`:** for each `information_schema.sequences` row in `public`: `… WHERE d.objid = $1::regclass …` now bound
  to `quoteIdent(seq.sequence_name)`; `ALTER SEQUENCE ${quoteIdent(name)} OWNED BY ${table_name}.${quoteIdent(column)}` (unchanged; `table_name` is
  `d.refobjid::regclass` text); `SELECT setval(${sqlLiteral(quoteIdent(name))}, COALESCE((SELECT MAX(…) FROM ${table_name}), 1));`. Its test makes
  `"Vsp79Seq"` + `vsp79_t` in the test DB, calls the REAL route through supertest, reads the zip, and drops both in `after()`. **It hands supertest a
  bare app: `admin = request.agent(createApp())` (line 43).**
- **VSP80:** `serve(app)` pushes each server; `closeServers()` `closeAllConnections()` + `close()`; `helpers.closeDb()` awaits `closeServers()`
  before `pool.end()` and exports `serve`; every other change swaps what a file hands supertest (19 deleted lines, **none an `assert`**, READ).
  `loopback.test.js` cell 1: `serve()` binds `127.0.0.1`; cell 2: a decoy on `127.0.0.1:P` answering 501, the app bound on `[::]:P`, a request to
  `127.0.0.1:P` gets the decoy (or `EADDRINUSE` on an OS that refuses), then `serve()` gets the app's 200. `server/errors.test.js` (a UNIT file)
  now requires `../test/loopback`.
- **VSP82 `dispatchDue()`:** `const cutoff = (await query('SELECT NOW()::text AS now')).rows[0].now;` then per reminder `… WHERE status =
  'pending' AND due_at <= $1::timestamptz ORDER BY due_at, id LIMIT 1 FOR UPDATE SKIP LOCKED`. **The only client path (READ):** `POST
  /api/reminders` (`server/routes/reminders.js:32-62`) inserts `b.due_at` AS SENT; the PRO dashboard sends `new Date($('remDue').value).toISOString()`
  (`public/pro/js/pro-dashboard.js:278`). The rules' `INSERT … ON CONFLICT (rule_key) WHERE rule_key IS NOT NULL DO NOTHING` are
  `dispatcher.js:83/99/114`.
- **VSP85:** one regex `CREATE_TABLE = /\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:"?\w+"?\s*\.\s*)?"?(\w+)"?\s*\(/gi` and one walker
  `census(dirs, {exts, skip})` (skips `*.test.js` and `node_modules`); `tablesInCode = census(['server','scripts'])`; the lazy census stays
  `server/` minus `initDb.js`. `dbBackup.test.js`: `failingSelect` fires on `/FROM "(\w+)" t\b/` only (`dumpTable()`'s row SELECT is `SELECT
  row_to_json(t) AS r FROM "${tableName}" t ORDER BY …`, `dbBackup.js:44` at main); `pkAnswered` records the PK lookup. **Every main `test(` line
  and every main `assert` line is still present at the head (READ).**

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READYs — found by the drafter (verify each; all are claims)
- **(a) VSP-76 READY: "RED FIRST (gate 11 tool qa-g11-n1-child.cjs, read-only, run unmodified from its evidence path, N=20, my own DB
  vsp_qa_g11_7609291_test)".** READ: the tool refuses any DB not named `vsp_qa_g11_*` and loads pg from gate 11's `work-g11/ptree-TOOLS-pgclient.*`;
  so running it unmodified meant the BUILDER created a database **in the QA gate-11 namespace** and executed code out of gate 11's evidence and
  work folders. `vsp_qa_g11_7609291_test` is the builder's: never use, list as yours, alter or drop it. **For this gate the commission's "by path,
  read-only" is met by COPY + a two-line re-point proven by diff (§PRIOR ROUND), never by running from gate 11's folder.** (Hygiene note for
  Tuesday: a builder DB named like a QA gate's.)
- **(b) VSP-76 READY: "comment 38535's dispatcher catch is covered by construction" and "the guard covers it [backup-db] by construction".**
  Construction is a claim: §N1.2 runs gate 11's real-caller cells and §N8.1 a dispatcher send under a terminate.
- **(c) VSP-76's classifier boundaries.** It marks any error on a client with `_queryable === false`, any FATAL, any `57P*` / `08*`. The READY
  names 22012, 23505 and 57014 as NOT marking. Unnamed and worth one cell each (§N1.3): `55P03`, `40P01`, `57014` from a server
  `statement_timeout`, `25P03` (C-09's production idle-in-transaction FATAL), `57P05`. Over-marking costs a reconnect; under-marking is the bug.
- **(d) VSP-78 READY: "for 15 of the 16 indexes".** TRUE at source (READ). The mechanism ("CREATE INDEX IF NOT EXISTS checks table OWNERSHIP
  before existence") is re-derived by §N2.1's red, not assumed.
- **(e) VSP-78: `to_regclass('<name>')` resolves through the search_path.** A relation with an index's name in a schema EARLIER on the search_path
  makes the check skip creating `public`'s index and initDb's missing-index line stays silent; main's `CREATE INDEX IF NOT EXISTS <name> ON <table>`
  checks the TABLE's schema. Gate 13's class. **MEASURE once at the head and at main** (§N2.6); production's search_path NOT TESTED.
- **(f) VSP-78: `reportAccess()` and the missing-index query are NOT wrapped** (READ). Any error they raise fails the boot (the builder's first
  draft raised `42809`). Hunt for a real catalog shape that makes either throw (§N2.3 (l)).
- **(g) VSP-78 and VSP-77 tests, pid collision (READ, not measured):** each reuses a pre-existing role of its own name pattern
  (`vsp78_<pid>_boot`; `vsp71_<pid>_boot`) — with a random password per run the login then FAILS (under VSP-77 this is new: the fixed `'vsp71'` used
  to match). The builder left 26 `vsp78_*` roles. VSP-77's `after()` drops `vsp71_<pid>_*` roles unconditionally (pre-existing). Flaky, not
  destructive to anything outside those patterns. Say whether it is worth a Polish finding.
- **(h) VSP-78 new-head READY: product files byte-identical to `c74d7fd`.** TRUE at source (READ). `c74d7fd`'s red-first and mutants "stand": they
  are claims about a different test file; **re-derive them on `1de6d92`.**
- **(i) VSP-78 leftovers (58/24 → 63/26).** Not yours. List `vsp78_*` and `vsp71_*` DB and role NAMES before and after every `test:db` (§N8.5).
- **(j) VSP-82 READY "CLIENT REACH: NONE".** Two reads the READY does not close: (1) `POST /api/reminders` stores `b.due_at` as sent, so the
  millisecond grid is the UI's property, not the API's (the READY says so: "never before due" — measure it); (2) **the `::text` round trip depends
  on the session's DateStyle and TimeZone** (READ): `ISO` output carries a numeric offset, but the `Postgres`, `SQL` and `German` styles print a
  zone ABBREVIATION, read back through `timezone_abbreviations`. **The drafter PREDICTS, unmeasured,** that an abbreviation the reading side maps to
  a different offset (candidate: TimeZone `Asia/Kolkata` prints `IST`) moves the cutoff by hours and could select reminders — client ones included
  — BEFORE they are due. The portal sets neither (READ: `server/db.js` passes no `options`); production's settings are NOT TESTED. **MEASURE
  (§N4.4); grading is §TUESDAY'S RULINGS item 2 (STAMP).**
- **(k) VSP-82's "nothing goes out early" control uses due = clock + 2 s** (READ): it cannot see a sub-ms or 1 ms early selection. Your mutant
  M-ceil (§N4.5) decides whether that is a test gap.
- **(l) Coverage claims:** main 80.78 lines (every READY); VSP-82 alone **80.65** ("the only new lines are the comment"), VSP-76 **82.09** (+1.31);
  the rest "unchanged". **VSP-82 alone is the thinnest margin (0.65 points, local, NOT CI).** VSP-80's `server/errors.test.js` now loads
  `test/loopback.js` in the UNIT coverage run (a non-test file outside `server/`): say whether the denominator changed.
- **(m) VSP-85 cell "the census reads scripts/ as well as server/" is VACUOUS on today's tree** (READ: `git grep -i` for
  `create [temp|unlogged] table` over `scripts/` at `6dbffdf` finds nothing, rc 1): its loop runs over zero names; only M8 proves the walk.
- **(n) VSP-85's regex misses** `CREATE UNLOGGED TABLE`, `CREATE TEMP TABLE`, `CREATE TABLE … AS SELECT`, `… PARTITION OF` and quoted names with
  non-word characters (READ). Observations unless the tree has one (you census `server/`).
- **(o) Branch-coverage figures disagree for the same code:** VSP-75 READY 76.68 at `110bb03`, gate 13 measured 76.18, VSP-76 READY 76.31 at
  `6dbffdf` (= `110bb03` + BACKLOG). Run coverage N=2 per tree.
- **(p) None of the seven touches `BACKLOG.md`** (READ). Say whether the BACKLOG should carry these rounds.
- **(q) TIER 2 as commissioned; the drafter notes (not a change):** VSP-78's `schema.sql` runs on EVERY production boot and its access line is a
  boot-behaviour change Tuesday takes to Kam (C-10); VSP-78's and VSP-77's test teardowns run `pg_terminate_backend` / `DROP DATABASE` / `DROP
  ROLE` on the shared local cluster (names pinned to their own run: §N8.5 proves it); VSP-76 changes the client every production query goes
  through; VSP-79 changes the production backup-db route.
- **(r) Short shas in the commission and READYs:** VSP-82 `ccfc7ef60c44`, VSP-85 `b78d2e314b6a`, VSP-80 `28adf36579ed`, VSP-77 `da6287321b3c`, VSP-79
  `241b8bb` — full values in §PIN (ls-remote 07:05:58).
- **(s) UNVERIFIABLE by design, and you must not try:** production's roles and table owners, its search_path, DateStyle and TimeZone, its
  timeouts in effect (C-09 says 600000; not yours to read), its catalog, indexes and sequences; real Azure Blob Storage, ACS, ntfy; CI. **Carry
  each as NOT TESTED.**
- **(t) VSP-80 × VSP-79 — THE MERGED TREE REOPENS VSP-80's HAZARD IN ONE FILE (READ, predicted).** VSP-80 claims "Every `request(app)` /
  `request.agent(app)` in test/ and server/ now takes a served server (grep: 0 bare call sites left)" — true on VSP-80's own tree. VSP-79's new
  `test/db/backup-db-sequence-names.test.js:43` has `admin = request.agent(createApp())`: a BARE app. Neither builder could see the other (both off
  `6dbffdf`). On the merged tree that file is exposed to the hazard VSP-80 removes. **§N8.3's forced-hazard sweep measures it; grading is
  §TUESDAY'S RULINGS item 5 (STAMP).**
- **(u) VSP-80 READY: "The random failure itself can't be forced (supertest picks the ephemeral port)".** It can be forced in YOUR harness: a
  preload that rewrites a wildcard `listen(0)` onto the port of a decoy already listening on `127.0.0.1` (§N5.2, §N8.3). That is the positive
  control Tuesday asked for.
- **(v) VSP-80 × every DB file:** `helpers.closeDb()` now closes servers before `pool.end()`; every DB test file's `after(closeDb)` goes through
  it, including VSP-79's, VSP-82's and VSP-85's. A hang would show as a suite past its deadline.
- **(w) VSP-79 READY NOT TESTED: a replay of a dump with a mixed-case sequence, and a sequence name with a single quote.** Both testable locally
  (§N3.2, §N3.3). Also READ: only `public` sequences are dumped (`information_schema.sequences WHERE sequence_schema = 'public'`), pre-existing.
- **(x) VSP-77 × VSP-78:** VSP-77 pins `WHEN OTHERS` for `IDX_session_expire` only; VSP-78's 15 new `WHEN OTHERS` blocks have no pairs cell of
  their own (the VSP-78 READY's NOT TESTED). §N2.4's all-indexes-missing pairs arm covers them on the merged tree.
- **Verified TRUE at source (READ 06:46-07:1x):** all eight heads by `ls-remote` = the READYs' heads; parents and chains above; no merges;
  counts 2/1/3/1/1/1/1; every file set; the pairwise overlap matrix (21 pairs: exactly the two named overlaps); `test(` counts; the 16 index
  names and definitions; the 15 regex names; `c74d7fd` = `1de6d92` on product files; VSP-85 keeps every old cell and assert line; VSP-80 deletes no
  assert line; the READYs' evidence folders `5_Project_History/evidence/2026-09-29-vsp{76,77,78,79,80,82,85}` exist per the READYs (`ls` of four;
  not opened as evidence); C-10 present; `:5433` LISTEN (Docker); `node:20` present locally (`docker image inspect` only, `sha256:8f693eaa…`).

## THE READYs — their claims and NOT TESTED (the gate rules on every claim)
Read each READY whole. Their NOT TESTED lines are carried VERBATIM here (the launcher checks it). VSP-78's new-head READY has no NOT TESTED of its
own ("Everything else in the c74d7fd READY stands").

VSP-76 NOT TESTED
```
NOT TESTED
- CI (gh not logged in). Node 22/20 not run locally; only Node 26.8.1.
- A ROLLBACK that is itself the FIRST connection-class failure on a link pg still reads as queryable: not reached on a real link. In the real shape the preceding query's FATAL marks the client first. Covered only by the fake-client unit cell, which goes through the same wrapper path.
- RST/FIN during an in-flight query with a same-tick release (the gate measured those 0/20 before the fix; not re-run).
- Submittables (cursors/streams) bypass the wrapper as before; the repo has none (grep).
- No route-level cell for GET /api/admin/backup-db under an in-flight terminate; the guard covers it by construction.
- e2e:pro not run.
```

VSP-77 NOT TESTED
```
NOT TESTED: CI; Node 20/22. More than 5 pairs (the gate's arm was 6/6 red under M5; this cell went red on pair 1).
```

VSP-78 NOT TESTED (the c74d7fd READY)
```
NOT TESTED
- CI; Node 20/22.
- Production's roles: whether the app's role owns the tables, and whether a restore would run as it. That decides whether the access line would ever fire there. Reading them is a production read, so it's not mine.
- The real backup-db dump as the replay source: the cells replay schema.sql by another role (the same ownership effect and the same CREATE INDEX shapes). The gate's own replay of the route's dump was not re-run.
- Concurrent boots racing a guarded index: WHEN OTHERS absorbs the 23505 as in VSP-71, but I didn't re-run the gate's pairs arm.
- feedbackDigest.js's own CREATE INDEX IF NOT EXISTS on `feedback` (idx_feedback_status/clarity): not part of the boot path I changed, not guarded. If feedback is replayed by another role, the digest's index statement could fail at its run. Left as is. Tell me if you want it on this branch or ticketed.
- e2e:pro.
```

VSP-79 NOT TESTED
```
NOT TESTED: CI; Node 20/22. A replay of a dump carrying a mixed-case sequence (the cell checks the dump text, not a replay). A sequence name containing a single quote (sqlLiteral doubles it; not exercised). No such sequence exists in the app's schema today.
```

VSP-80 NOT TESTED
```
NOT TESTED: CI (Linux: the hazard cell's EADDRINUSE branch is expected there, not seen here). Node 20/22. Frequency: before the fix it was about 1 in 6 full runs, so "no occurrence since" needs more runs than one session.
```

VSP-82 NOT TESTED
```
NOT TESTED: CI; Node 20/22; e2e:pro. A second portal instance ticking at the same time (SKIP LOCKED unchanged). A session TimeZone other than the local default for the ::text round trip (the text carries its offset, and ::timestamptz reads it back; not varied).
```

VSP-85 NOT TESTED
```
NOT TESTED: CI; Node 20/22. The census still only reads .sql/.js, so a table made from a .sh or a migration file in another language would not be seen; none exist today.
```

**The claims, in one line each (each a CLAIM, re-derived in §N):**
- **VSP-76 @ `f593e38`:** gate 11's `window:terminate:immediate:product` / `…:max1` reused 20/20 + next failed 20/20 at main → 0/20 + 0/20 at
  `79ec3cd` and `f593e38`, window hit 20/20; control `rollback:product` 0/20. Builder cells: window-promise, window-callback, window-max1 RED on the
  unfixed `db.js`, green on the fix; controls green on both. Mutants A (classifier always true → 2 keep controls fail), B (release drops BROKEN →
  3 window + 2 unit cells fail). Sets: unit 131 → 136, db 126 → 133, 0 lost. Coverage 80.78 → 82.09 lines, 76.31 → 76.50 branches.
- **VSP-77 @ `da62873`:** M5 (catch narrowed to `insufficient_privilege OR lock_not_available`) → the new cell fails on pair 1 (`23505
  pg_class_relname_nsp_index`), the 5 VSP-71 cells pass; the new file on main's product 6/6; on `da62873` 6/6. Sets: db 126 → 127, 0 lost.
- **VSP-78 @ `1de6d92` (product = `c74d7fd`):** main REJECTED `42501 must be owner of table leads` after another role replays. New cells red on main
  5/5 (3 "must be owner of table leads"), green 5/5. Controls: the unique-index cell (→ 42501 on reminders); the partial-grant cell (exactly "1
  object(s): table meetings"). Mutants: no access report → 2 fail; excusing `idx_reminders_rule_key` → the unique control fails. Sets: db 126 → 131.
  Teardown: `c74d7fd`'s file +5 DBs / +2 roles, `1de6d92`'s +0 / +0.
- **VSP-79 @ `241b8bb`:** control (lower-case sequences only) 200 on main and branch; a mixed-case sequence: main 500, branch 200, and the dump
  carries `ALTER SEQUENCE "Vsp79Seq" OWNED BY` and `SELECT setval('"Vsp79Seq"', `. Sets: db 126 → 128, 0 lost.
- **VSP-80 @ `28adf36`:** `loopback.test.js` cell 2 reproduces the hazard on this Mac (decoy 501 through a `[::]` bind) and `serve()` gets 200;
  cell 1 `serve()` binds 127.0.0.1 (mutant "serve binds the wildcard" fails it). "0 bare call sites left". Sets: db 126 → 128, 0 lost.
- **VSP-82 @ `ccfc7ef`:** cell 1 red on main 3/3 runs (28, 45, 26 of 100 deferred), green 3/3. Controls: 100 client reminders due
  `date_trunc('milliseconds', NOW())` all sent in their tick; 20 due 2 s ahead never sent; mutant `NOW()+5 s` fails that control. Sets: db 126 → 129.
- **VSP-85 @ `b78d2e3`:** M6 0 → 3 fail (census, LAZY_TABLES, round trip); M7 0 → 3; M8 0 → 2; M9 unit 10/10 → 1 fail (the O4 cell). Sets: unit
  131 → 132, db 126 → 129, 0 lost.

**How you treat these:** every NOT TESTED line you CAN test locally, you test. CI, Azure, ACS, ntfy and production go into your own NOT TESTED.

## 2a. LEGITIMATE SHAPES — what must still work
**Until the rows below are measured, the instruction on ANY unexpected result is STOP and record it, never a remedy.** Every cell runs against a
database YOU created. **A row whose expected verdict and clause disagree is a finding against this brief. Say so.**

| shape | expected at the head / merged | predicted-by |
|---|---|---|
| a held client whose query fails 22012 / 23505 / 57014 (cancel), released | the SAME backend is handed out next | VSP-76 READY — **measure** |
| a clean checkout/query/release, 20,000 cycles | 1 backend, idle `error` listener count 1 | gate 11 N1.5 — **measure** |
| production-shaped DB (boot role owns everything, all indexes present), boot | RESOLVED, **0** VSP-78 lines, 0 VSP-71 lines | gate 11 N2.4 — **measure** |
| another role replays, boot role granted ALL | RESOLVED, 0 VSP-78 lines, serves | VSP-78 READY — **measure** |
| another role replays, NO grants | RESOLVED, exactly ONE access line naming every public table + sequence; data requests 500 (C-10 shape) | C-10 — **measure** |
| another role replays, `idx_reminders_rule_key` dropped | **REJECTED 42501 `must be owner of table reminders`** | Tuesday's ruling — **the REQUIRED CELL** |
| backup-db on the app's own (lower-case) schema | 200, the dump replays whole (VSP-73) | gate 11 N6.1 — **measure** |
| backup-db with a mixed-case serial table | 200 at the head; its dump replays and `nextval` = max+1 | VSP-79 — **measure** |
| internal reminder `due_at = NOW()`, dispatched at once | handled in that tick, 100/100 | VSP69-G12-F1 regression cell — **measure** |
| client reminder `due_at` on the ms grid ≤ the tick's `NOW()` | sent in that tick, as at main | VSP-82 READY — **measure** |
| any reminder with `due_at` > the tick's `NOW()` (by 1 µs, 1 ms, 2 s) | **never selected** | VSP-82 READY — **measure** |
| every supertest call site in the merged `test/` and `server/` | reaches only its own app, even with a decoy on the port | VSP-80 — **measure (§N8.3)** |
| the backup census on today's tree | the same set as main's census for `server/`; `scripts/` adds nothing | VSP-85 READY — **measure** |

## N1. VSP-76 — the dead client is discarded (TIER 2)
**FAIL condition, stated BEFORE the runs:** at `f593e38`, in any run of gate 11's window cells (terminate × same-tick release × product pool or
max-1 pool with a queued waiter), the dead backend is handed to the next caller or the next caller fails; a real caller (§N1.2) answers an innocent
request 500 with `Connection terminated unexpectedly`; a client whose query failed with a class the READY names as non-marking (22012, 23505, 57014
cancel) is discarded; any VSP-65/VSP-66 regression (an uncaught link death, a listener count ≠ 1 after release, `pool-timeout.test.js` not 12/12,
a TIMED_OUT client not discarded); a builder mutant that stays green; a name lost (§N8.4). A non-named class marked or kept against §N1.3's
prediction is a FINDING with its code, not a FAIL.
1. **The red cell, on gate 11's own tool (copied + two-line re-point, §PRIOR ROUND), N=20 per mode:** `window:terminate:immediate:product`,
   `window:terminate:immediate:max1`, and the controls `window:terminate:rollback:product` and `window:rst:immediate:product`, at **main `6dbffdf`
   (POSITIVE CONTROL: predicted reused 20/20, next failed 20/20)** and at `f593e38`. Quote each `summary` (`reused`, `nextFailed`,
   `queryableTrueAtRelease`). **At the head `queryableTrueAtRelease` must be ~20/20 or the window was not hit and the cell is VOID.** FIN is not a
   mode of the tool; READ gate 11 N1.2's reason RST/FIN never open the window and say whether FIN needs a cell.
2. **Real callers (gate 11 N1.2/N1.3 arms, `qa-g11-arms.cjs` + `qa-harness-g11-vsp.cjs`, copied):** `GET /api/admin/backup-db` whose dump waits on
   YOUR `ACCESS EXCLUSIVE` lock is terminated in flight, (i) alone, (ii) with the pool full (9 × `pg_sleep(5)`) and a queued signed-in
   `/api/auth/me`. Main: the dead client reused (gate 11: the innocent `/me` 500). Head: `/me` 200 on a DIFFERENT backend, the dead pid acquired 0×,
   one `[db] a held client lost its connection` line. N ≥ 3 per arm.
3. **The classifier's boundaries (MEASURED on real Postgres; a held client, the failing query, release, the next checkout's backend pid):** 22012,
   23505, 42P01, 57014 by `pg_cancel_backend`, 57014 by `SET statement_timeout`, 55P03 by `SET lock_timeout` against YOUR lock, 40P01 by a deadlock you
   make, `25P03` by `SET idle_in_transaction_session_timeout = '1s'` in YOUR session (C-09's shape: the death arrives while the client is IDLE in a
   transaction), `57P05` by `idle_session_timeout` if cheap. Table: code, severity, marked?, same backend next?, prediction (FATAL / 57P / 08 /
   unqueryable → discarded; the rest kept).
4. **The READY's NOT TESTED "A ROLLBACK that is itself the FIRST connection-class failure …":** attempt only if cheap on a real link; otherwise carry
   it NOT TESTED with the reason.
5. **VSP-65 / VSP-66 untouched:** `pool-timeout.test.js` 12/12 ×3; gate 11's `hygiene` mode (20,000 promise + 1,000 callback cycles: 1 pid, idle
   listener count 1, 0 `MaxListenersExceededWarning`); one TIMED_OUT cell (a query past a shrunk bound) still discarded.
6. **Red-proofs (fresh tree per arm, asserted edits, `node --check` rc quoted; a red from a mutant that does not parse is VOID):** the head's
   `db.test.js` + link-death pair (blobs `8e10e3a`, `0b5d793`, `f79a272`, hash-verified) on main's `db.js` → predicted {window-promise,
   window-callback, window-max1} red, controls green, and say which of the 5 unit names redden; the head ×3. The READY's mutants A and B with counts.
   **Yours:** (C) the classifier without the `_queryable` term; (D) without `08`; (E) FATAL only; (F) the mark read from `_queryable` in `release()`
   only (no wrapper). Say which cell sees each, or that it is equivalent and why.

## N2. VSP-78 — a replay by another role does not crash-loop the boot (TIER 2)
**FAIL condition, stated BEFORE the runs:** at `1de6d92`, a boot after another role replays (`schema.sql` as one query, AND the REAL backup-db
route's dump as one query) with the boot role granted access is not RESOLVED or does not serve; **`idx_reminders_rule_key` missing and unmakeable
does NOT fail the boot (§N2.2, the REQUIRED CELL)**; the access line is absent when a privilege is missing, present on a production-shaped or fully
granted DB, printed more than once, or names an object it can use / omits one it cannot (C-10: correctness is the gate's); any VSP-71 cell regressing;
a production-shaped boot printing any VSP-78 line; the test's teardown dropping, terminating or altering ANY database or role it did not create in
that run; a builder mutant that stays green; a name lost.
1. **Red first on YOUR instrument (gate 11's N6.4 harness, copied):** a production-shaped source DB (store-made `session` WITH index, rows, a kept
   cookie); dump it through the REAL `GET /api/admin/backup-db` at each tree; another role (`vsp_qa_g14_other`, NOLOGIN, inside your DB only)
   replays the WHOLE dump as ONE query; boot as `vsp_qa_g14_boot`. **Main `6dbffdf`: REJECTED `42501 must be owner of table leads` (POSITIVE CONTROL,
   gate 11 G11-M1).** Head: (i) + GRANT ALL → RESOLVED, 0 VSP-78 lines, the kept cookie `/me` 200; (ii) no grants → RESOLVED, ONE access line, a
   data request 500 (the accepted shape); (iii) the dump carries the new header comment verbatim. Then the same with `schema.sql` replayed (the
   builder's shape). N ≥ 2.
2. **THE REQUIRED CELL — the unique-index exception still fails the boot.** Another role replays and then drops `idx_reminders_rule_key`; boot as
   the boot role: **REJECTED `42501 must be owner of table reminders`**, rc and message quoted, N ≥ 3, on `schema.sql` AND on the route dump.
   Independent controls: (a) the same with `idx_leads_stage` dropped instead → RESOLVED with ONE missing-index line naming it; (b) the boot role owns
   `reminders`, the index missing → CREATED, RESOLVED. **Why it is load-bearing, measured once:** on a scratch copy of the head with the unique block
   given `EXCEPTION WHEN OTHERS` (mutant M-u), the boot resolves and the rules' `INSERT … ON CONFLICT (rule_key) WHERE rule_key IS NOT NULL` then
   fails — quote its SQLSTATE (predicted `42P10`). The builder's unique cell must redden under M-u.
3. **Does the access line fire correctly? (C-10 ruling 1's question; one boot per row, exact line quoted):** (a) production-shaped → 0 lines;
   (b) other-role replay + GRANT ALL → 0; (c) no grants → one line, the object count equal to YOUR `pg_class` count of public `r`/`p` tables + `S`
   sequences, every name present; (d) REVOKE each of SELECT, INSERT, UPDATE, DELETE on one table, one at a time → exactly that table; (e) REVOKE
   USAGE on one sequence only → exactly that sequence; (f) privileges held only through a group role the boot role INHERITS → 0 lines; NOINHERIT →
   say what it prints and whether that is right; (g) column-level grants only on one table → say; (h) a superuser boot → 0; (i) a public VIEW and a
   partitioned table owned by another role → the view not named, the partitioned table named; (j) a mixed-case public table `"QA_Mixed"` → quote
   how it is printed; (k) the line appears once per boot; (l) **THE THROW HUNT:** any catalog shape in your DB under which `reportAccess()` or the
   missing-index query raises (a boot that fails there is a FAIL). Mutants: (M-a) the comma-list `has_table_privilege(oid,
   'SELECT,INSERT,UPDATE,DELETE')` → the partial-grant cells must redden; (M-b) `AND` in place of `CASE` → does `42809` appear on a real catalog
   (N=10); the READY's "no access report" → 2 builder cells fail.
4. **VSP-71 not regressed (gate 11's N2 cells, copied):** (a) non-owner of `session` → RESOLVED with one VSP-71 line; (b) a held write on `session`
   at the shipped 30,000 bound → RESOLVED ~2 s; the `lock_timeout` sentinel reads back on the same backend; the production-shaped no-op boot 0
   warnings; the pairs arm with `IDX_session_expire` missing is VSP-77's cell now (§N6); **the pairs arm with ALL 16 indexes missing on an EXISTING database (the VSP-78
   READY's NOT TESTED; WRONG (x); not VSP-72's parked empty-database shape, C-12), 10 pairs:** the 15 guarded blocks must absorb the loser's 23505; the unguarded `idx_reminders_rule_key` may still
   lose one boot — **run the same at main**: identical = pre-existing FINDING, worse at the head = FAIL.
5. **The held-write cell:** another instance holds an open ROW EXCLUSIVE transaction on `leads` while the portal boots. Indexes present: at main
   (each plain `CREATE INDEX IF NOT EXISTS` takes a SHARE lock first) quote how long the boot waits and whether it fails at the bound; at the head
   (`to_regclass` first, no lock) predicted no wait. Index missing + held write: at the head the boot waits (no lock_timeout on the 15) — quote the
   time and outcome at a shrunk bound, beside VSP71-G11-O2. Load beside every number.
6. **search_path shadowing (WRONG (e)), once each at the head and at main:** in YOUR DB, a schema earlier on the search_path (`ALTER DATABASE <your
   db> SET search_path`, or a schema named after the boot role) holding a relation named `idx_leads_stage`; `public`'s `idx_leads_stage` dropped;
   boot. Is `public`'s index created? Does any line name it missing? Graded by §TUESDAY'S RULINGS item 3.
7. **Red-proofs:** the head's test file (blob `877a8e5`) on main → predicted 5/5 red (3 "must be owner of table leads"); the head ×3; the READY's two
   mutants with counts; M-u, M-a, M-b above; **yours:** (M-c) drop `to_regclass` and wrap `CREATE INDEX IF NOT EXISTS` in `WHEN OTHERS` (VSP-71's
   exact pattern) — which cell sees it (predicted: only §N2.5's held-write cell); (M-d) the initDb regex matching `CREATE (UNIQUE )?INDEX` → which cell.

## N3. VSP-79 — backup-db answers 200 with a mixed-case sequence (TIER 2; a production-reachable route fix)
**FAIL condition, stated BEFORE the runs:** at `241b8bb`, the REAL route answers anything but 200 for a DB carrying a mixed-case sequence owned by a
table column; its dump does not replay whole as ONE query into a fresh DB, or the replayed sequence's `nextval` ≠ max+1; any change to the dump of
an all-lower-case DB other than the quoting of names that need it (diff the statement lists); a builder cell not red at main / green at the head;
a name lost.
1. **THE REAL-ROUTE CELL, red on main (Tuesday's commission):** YOUR harness (gate 11's N6 route harness, copied: `createApp()` + a signed-in admin
   agent **served on 127.0.0.1**), YOUR seeded DB plus (i) gate 11's `"QA_Mixed_Case"` (serial, rows) and (ii) a table whose `DEFAULT
   nextval('"Vsp79Seq"')` sequence is `OWNED BY` it (the builder's shape). `GET /api/admin/backup-db`: **main `6dbffdf` → 500 (quote the `[admin]
   Backup error:` line; gate 11: `relation "qa_mixed_case_id_seq" does not exist`)**; head → 200, bytes and elapsed with load. N ≥ 3. Control: the
   all-lower-case DB → 200 at both.
2. **The dump replays (the READY's NOT TESTED):** the head's dump into a fresh DB of yours as ONE query: success; the table set, row counts and
   index set equal the source (gate 11 N6.3's comparison, copied); for each sequence, `nextval` = max+1 and `pg_get_serial_sequence` resolves; the
   mixed-case ones by name, quoted. Main's dump for the same DB cannot be taken (500): say so.
3. **Names that stress the quoting:** a sequence named with a single quote (`"qa'seq"`), a double quote (`"qa""seq"`), a space, and a dot, each
   owned by a column: route status, the dump's `ALTER SEQUENCE` / `setval` lines quoted verbatim, and the replay. A sequence NOT owned by any column
   (no `pg_depend` 'a' row): skipped as at main. A mixed-case TABLE with a lower-case sequence: the `OWNED BY ${table_name}` and `FROM
   ${table_name}` text (regclass output) replays.
4. **VSP-79 × VSP-78 on the same file:** on the merged tree the dump carries VSP-78's header line AND VSP-79's quoting; §N2.1's other-role replay of
   that dump with the mixed-case fixture present.
5. **Red-proofs:** the head's test (blob `5bf8e24`) on main → {cell 2} red, control green; the head ×3; **your mutants:** (M-q1) quote only the
   lookup (the dump's `setval` unquoted) → which cell sees it (the builder's text assertion; your replay cell); (M-q2) quote only the `setval` → the
   500 returns. `node --check` rc for each.

## N4. VSP-82 — the cutoff keeps Postgres's precision; clients unchanged (TIER 2)
**FAIL condition, stated BEFORE the runs:** at `ccfc7ef`, any internal reminder with `due_at = NOW()` deferred a tick (builder's cell ×3 AND gate 12's
300-run arm); **under the default DateStyle (`ISO, MDY`) and any TimeZone you test, any reminder selected by a tick whose `NOW()` precedes its
`due_at`**, or any client reminder on the millisecond grid decided differently from main; a regression of dispatch-once, reminder-push or
concurrency, or of gate 12's no-double-send arms; a builder mutant that stays green; a name lost. Early selection under a NON-default DateStyle is
graded by §TUESDAY'S RULINGS item 2.
1. **Red first, two instruments:** the builder's cell 1 (×3 each) at main `6dbffdf` (predicted 20-50 of 100 deferred) and at the head (0); **gate
   12's own cutoff arm (`qa-g12-disp.cjs`, copied; 300 runs) at main (gate 12: 72-125/300), the head (0/300), and `609e967` (the pre-VSP-69 control,
   gate 12: 0/300).** Every deferred one must be picked up by the next tick (quote).
2. **CLIENT REACH, decision equivalence through the REAL code path:** N ≥ 10,000 cutoffs sampled from the database's own clock; for each, `due_at`
   on the ms grid at `floor_ms(t) − 1 ms`, `floor_ms(t)`, `floor_ms(t) + 1 ms`, and off-grid at `t − 1 µs`, `t`, `t + 1 µs`. Decide each with MAIN's
   predicate (the cutoff through the tree's own `pg` as a `Date`, bound back, `due_at <= $1`) and the HEAD's (`NOW()::text`, `due_at <= $1::timestamptz`),
   both run by Postgres with the dispatcher's own WHERE text. Report: ms-grid disagreements (**claim: 0**); off-grid disagreements (predicted only for
   due in (`floor_ms(t)`, `t`]); **any `due > t` selected by the head (claim: 0).**
3. **Nothing early, through `dispatchDue()` itself** (gate 12's harness; SDK recorder, ntfy to YOUR loopback): client reminders due at the DB clock
   + 1 µs, + 500 µs, + 1 ms, + 2 s, inserted immediately before a tick, ×100 each: 0 sent before due, at main and at the head.
4. **Session settings (WRONG (j)(2)), on YOUR database only (`ALTER DATABASE <your db> SET …`):** TimeZone ∈ {UTC, Australia/Sydney, Asia/Kolkata,
   America/St_Johns} × DateStyle ∈ {`ISO, MDY` (default), `SQL, DMY`, `Postgres, MDY`, `German`}. For each pair: `NOW()::text` quoted,
   `NOW()::text::timestamptz = NOW()` true/false, the offset of any mismatch, and §N4.2's counts; then ONE real `dispatchDue()` with a client reminder
   due at `NOW() + 1 hour` for each pair where the round trip moves the cutoff forward. Main's `Date` path under the same settings, for comparison.
5. **Mutants (fresh tree per arm, `node --check` rc quoted):** revert to the `Date` cutoff → cell 1 red (the READY); the READY's `NOW() + 5 s` → the
   2 s control fails; **yours:** (M-ceil) `date_trunc('milliseconds', NOW()) + interval '1 millisecond'` as the cutoff text → does ANY builder cell
   fail? (predicted: none — a test gap if so); your §N4.3 cell must catch it; (M-cast) `$1` without `::timestamptz` → equivalent or not, and why.
6. **The dispatcher's other properties, short list:** `dispatch-once` 5/5, `reminder-push` 6/6, `concurrency` 5/5, `dispatch-cutoff` 3/3, each ×3 alone
   on a fresh DB; gate 12 N3.2 arm (i) (two processes, no double send; the READY's "second instance" NOT TESTED) and N3.4 once (SIGKILL mid-tick).

## N5. VSP-80 — every supertest app is served on 127.0.0.1 (TIER 2, TEST HARNESS ONLY)
**FAIL condition, stated BEFORE the runs:** at `28adf36`, a `serve()`d server not bound to `127.0.0.1`; any bare supertest call site left in VSP-80's
own `test/` and `server/`; under §N5.2's forced hazard any file at the head reaching the decoy; any deleted or changed `assert` line, or any cell
renamed/removed in the eight files it edits; a suite that no longer exits (closeDb past its deadline); a builder mutant that stays green; a name lost.
1. **The builder's cells:** `loopback.test.js` 2/2 ×3 (quote which branch cell 2 took on this Mac: decoy 501 or `EADDRINUSE`); its mutant (serve
   binds the wildcard) → cell 1 red; **yours:** (M-80a) `closeDb()` without `closeServers()` → does any suite hang (deadline) or leak a listener
   (count listeners of your test process at exit)?; (M-80b) revert ONE call site (e.g. `async-faults`) to a bare app → only §N5.2 sees it (predicted).
2. **THE POSITIVE CONTROL (WRONG (u); Tuesday's addendum): force the hazard.** A preload (yours, loaded with `--require` into the test process
   only) starts a decoy HTTP server on `127.0.0.1:<kernel port P>` answering 501 with a marker, and rewrites any `listen(0)` whose host is absent
   or a wildcard (what supertest's `app.listen(0)` does) to `listen(P, '::')`. Record every `listen` call (host, port, caller file). Run the whole
   `npm run test:db` (and `server/errors.test.js`) under it, **at main `6dbffdf` (POSITIVE CONTROL: predicted, every supertest file reaches the decoy
   — quote which fail and the decoy's hit count) and at `28adf36` (predicted: 0 decoy hits; every app `listen` is `127.0.0.1`)**. If this OS refuses the
   overlapping bind, say so: the positive control is then NOT RUN here and the record of bind hosts is the evidence.
3. **Not weakened (READ + MEASURED):** every main `test(` name present in each of the 8 edited files; 0 deleted `assert` lines (the drafter READ 19
   deleted lines, none an assert); `errors.test.js` 9/9 ×3 (its `captureLogs` awaits `fn()`, READ).

## N6. VSP-77 — the session-index test pins WHEN OTHERS; no fixed password (TIER 2, TEST FILE ONLY)
**FAIL condition, stated BEFORE the runs:** M5 does not fail the new cell on the head's file; the new cell fails on main's product (it must pass
there: WHEN OTHERS is present); any of the 5 VSP-71 cells changed or removed; a fixed or guessable password remains; the file's teardown touching a
database or role it did not create; a name lost.
1. **M5 re-derived independently** (fresh tree; `schema.sql`'s `WHEN OTHERS` narrowed to `insufficient_privilege OR lock_not_available` by YOUR
   asserted edit, `node --check` not applicable: run the SQL mutant inside `BEGIN … ROLLBACK` first, as gate 11 did): OLD file (main's `79de198`) →
   5/5 pass (M5 survives, gate 11's finding); NEW file (`ebc17ed`) → the new cell fails (quote the pair and `23505`); **on the merged tree too**
   (`schema.sql` is VSP-78's there: the mutant narrows the `IDX_session_expire` block only).
2. The new file on main's product 6/6 ×3; on the head ×3; the pair loop's timing and load (5 pairs × 3 boots).
3. **P1:** READ the password line; list `vsp71_*` roles before and after (0 left after a clean run); WRONG (g)'s pid-collision reading.

## N7. VSP-85 — the backup test gaps close (TIER 2, TEST FILES ONLY)
**FAIL condition, stated BEFORE the runs:** any of M6-M9 that the NEW files do not kill, or that the OLD files (main's `12a6e24`, `5ffb1fe`) ALSO
kill; an old cell removed or renamed, or an old assertion weakened or removed; the new files not green ×3 at the head; a product file changed; a name
lost.
1. **M6-M9 re-derived independently** (fresh tree per arm from `6dbffdf`, your own edit script with asserted anchor counts, `node --check` rc quoted;
   OLD test files vs NEW, hash-verified): M6 a plain `CREATE TABLE <yours> (` in a `server/` source file; M7 `CREATE TABLE IF NOT EXISTS
   public.<yours> (`; M8 a `CREATE TABLE` in a `scripts/` file; M9 `dumpTable()` swallowing the row-SELECT error. Quote the failing cell NAMES per
   arm vs the READY (3 / 3 / 2 / 1). **Plus yours:** (M10) the row-SELECT fault rethrown as a different error class; (M11) a quoted, schema-qualified,
   multi-line form in `server/`; (M12) `CREATE UNLOGGED TABLE` in `server/` (WRONG (n): predicted to survive — an observation).
2. **No cell removed or weakened:** every main `test(` name present; every main `assert` line present; the old census functions' SETS on today's tree
   equal the new walker's for `server/` (print both); `census(['scripts'])` on today's tree (WRONG (m): predicted empty).
3. **The O4 cell lands where it says:** your copy of `dbBackup.test.js` logs every thrown fault's SQL (asserted edit): the new cell's fault is on
   `SELECT row_to_json(t) AS r FROM "quotes" t …`, AFTER that table's PK lookup was answered.
The VSP-85 READY's Dependabot note (18 vulnerabilities on the default branch) is **OUT OF SCOPE**: do not read, query or act on it.

## N8. MERGED TREE — all seven on main (THE KEY MEASUREMENT)
1. **Cross-target cells (the overlaps git cannot see), on the merged tree:** (i) VSP-76 × VSP-82: a dispatch tick whose held client is terminated
   during a send (gate 12 N3.5): the dead pid re-acquired 0×, the reminder handled as at gate 12, no innocent caller 500; (ii) VSP-78 × VSP-82: boot,
   then one rules pass: the `ON CONFLICT (rule_key)` inserts succeed and a second pass inserts nothing; (iii) VSP-78 × VSP-79: §N3.4; (iv) VSP-85 ×
   VSP-78 × VSP-80: the census and `backup-coverage` 9/9 on the merged file (both sides' lines present); (v) VSP-77 × VSP-78: §N6.1 on the merged
   tree; (vi) VSP-76 × VSP-78: a boot whose connection is terminated mid-`schema.sql` rejects cleanly and the next boot RESOLVES.
2. **The merge, from YOUR OWN object dir** (`GIT_OBJECT_DIRECTORY=<your own mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C
   <repo> merge-tree --write-tree --name-only …`, sequential main + VSP76 → 77 → 78 → 79 → 80 → 82 → 85, synthetic commits in your objdir only; or
   SKIP it and say so): predicted conflict-free (§PIN: the drafter's `merge-file` on the two shared files was clean). **Prove the result tree equals
   "main `6dbffdf` + each head's blobs for its unshared files + the merged `admin.js` and `backup-coverage.test.js`"**, file by file; quote the two
   merged blobs (the drafter predicts `b967b9d`, `b26d38e`) and show both sides' lines in each. Try one other merge order (e.g. VSP-85 before VSP-80,
   VSP-79 before VSP-78): same tree or not.
3. **THE FORCED-HAZARD SWEEP ON THE MERGED TREE (Tuesday's positive control):** §N5.2's preload over the merged tree's whole `test:db` and
   `server/errors.test.js`. Predicted (WRONG (t)): every file served on `127.0.0.1` except **`test/db/backup-db-sequence-names.test.js`** (VSP-79's
   bare `request.agent(createApp())`), which reaches the decoy. Quote every file's bind hosts and decoy hits. Also a static count of bare call sites
   (every `request(`/`request.agent(` whose argument is not a served server) on the merged tree. Graded by §TUESDAY'S RULINGS item 5.
4. **SUITES AS SETS, NOT COUNTS** (same machine, same session): `npm test` and `npm run test:db` (each `test:db` on a FRESHLY CREATED
   `vsp_qa_g14_<epoch>_test`, zero user tables proven) at main `6dbffdf`, each of the seven heads, and the merged tree. Report vs main: names passing
   at main not passing at the tree (**must be empty everywhere**); added (READYs: unit +5 (76), +1 (85), others 0; db +7 (76), +1 (77), +5 (78),
   +2 (79), +2 (80), +3 (82), +3 (85); **merged predicted unit 137, db 149 — arithmetic, not a measurement**); removed; duplicates. The FIX 2 watcher
   (`qa-g13-lazywatch.cjs`, copied) beside every `test:db`, with its positive control once: **a write to `salesportal_test_lazy` or any builder
   database is a FAIL of the target whose tree ran and STOPS that arm.**
5. **Product-test hygiene:** `vsp71_*`, `vsp73_*`, `vsp78_*` DBs and roles, `salesportal_test_lazy` (no activity from you), YOUR `*_test_lazy` DBs,
   listed by NAME before and after each `test:db`; VSP-79's `vsp79_t` / `"Vsp79Seq"` exist only in YOUR test DBs and are gone after its file. The
   product's teardowns (VSP-77's, VSP-78's, VSP-79's) drop only what their own run made: the set present before is present after.
6. **Coverage, CI's command run locally** (`node --test --experimental-test-coverage --test-coverage-lines=80 --test-coverage-branches=70
   $(find server -name '*.test.js')`), **N=2 per tree** (WRONG (o)), at main, each head that changes a counted file (VSP-76, VSP-80, VSP-82, VSP-85)
   and the merged tree: lines and branches, per-file `db.js`, `reminders/dispatcher.js`, `dbBackup.js`, and whether `test/loopback.js` is counted.
   **Label it: local Node standing in for CI's Node 22; NOT CI.** The CI line gate is **80%**: VSP-82 alone is claimed at **80.65** (margin 0.65),
   VSP-76 claims **+1.31**. **Under 80.00% at any tree that could merge alone is a blocking finding for that merge order** (not by itself a NO-GO of
   the target); name the safe order.
7. **NODE 20 LEG (DOCKER-PULL-NEVER), per the NODE20-LEG line at the top.** Exactly ONE docker verb family is sanctioned, for this leg only:
   `docker image inspect node:20` (prove the image is ALREADY present, quote its digest; if absent, NOT RUN — **never pull**) and `docker run
   --rm --pull=never` of that image, YOUR archived tree mounted WRITABLE, an explicit `-e` allowlist (never `--env-file`), `NODE_ENV=test`,
   the DB URL pointing at YOUR database via `host.docker.internal:5433`, containers named `qa-g14-node20-<epoch>`. **Never `docker
   start/stop/exec/rm/compose`, never `vsp-dev-db`, never `--network host`.** Run in it on the MERGED tree: `node --version` (quote), `npm test`
   and `test:db` as sets, §N1.1's `window:terminate:immediate:product` N=20, §N4.1's cell 1 ×1, §N2.2's required cell ×1, §N3.1's route cell ×1.
   Reap each container in a `finally` and prove it gone. If NOT-RUN: say so and carry Node 20 as NOT TESTED.
8. **CI IS UNMEASURED.** This project's `gh` is not authenticated, and **you must not use `gh` at all**. Name CI's Node 20 / Node 22 legs, its
   coverage gate (local margin above) and its `e2e:pro` step as the first reads at merge. Never claim CI. (VSP-80's hazard cell takes its
   `EADDRINUSE` branch on a Linux runner, per its READY: say what that means for CI.)

## 12. The merge and the queue
**The drafter did NOT run `merge-tree`** (it writes objects into the repo's `.git`, which the drafter and the launcher may not do). The launcher's
guard is the OVERLAP MATRIX (exit 80): exactly the two named shared files, nothing else, no `BACKLOG.md`. The drafter PROBED the two shared files
with `git merge-file` on scratch copies (clean). **Measure the merge yourself** (§N8.2). **Merge order:** recommend one from your coverage numbers
and §N8.3 (VSP-82 alone is the thinnest; VSP-80 before or after VSP-79 decides whether the bare site lands under VSP-80's rule). **Cells to re-run on
the merged head at merge** (name at least): `npm test` + `test:db` as sets; §N1.1's window cells; §N2.2's required cell; §N3.1's route cell;
§N4.1's cell 1; §N8.3's sweep; the merged coverage; **CI's Node 20 and Node 22 legs including the coverage gate and `e2e:pro`: UNMEASURED, the
first reads.** **After Kam's deploy (not yours to read):** the first production boot's log (any `[db] the portal's database role … cannot use`
line, any `index(es) missing … (VSP-78)` line, any `[db] a held client lost its connection` line) and the first admin backup-db download.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)**, or any port another seat holds. **Never
   `127.0.0.1:49162`, `:49164` or `:49166`** (a LogiPlugin process listens there: the VSP-80 cause). Take every port from the kernel and bind
   `127.0.0.1` — **§N5.2's decoy is yours, on a kernel port; never the LogiPlugin's.** **Never start the portal's own entry point** (it binds
   `0.0.0.0` in `main()`); use the real `createApp()` and `initDb()` inside your harness only.
2. **Postgres = the local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all** (the one exception is
   §N8.7, under its NODE20-LEG line). Create `vsp_qa_g14_<epoch>` for app runs and `vsp_qa_g14_<epoch>_test` as `TEST_DATABASE_URL` for `test:db` (it
   TRUNCATEs; the name MUST end in `_test`). **Never** `salesportal`, `salesportal_test`, `salesportal_test_lazy` (the builder's; **the Vision seat,
   claude `93533` / pane `%44`, was LIVE at 06:49:33 building VSP-83 on the same Postgres and had exited by 07:08:09 — a Vision seat may be
   relaunched at any time**), any `vsp_qa_g1_*` … `vsp_qa_g13_*` database, **`vsp_qa_g11_7609291_test` (the builder's, in gate 11's namespace: WRONG
   (a))**, the builder's `vsp_s0929_*`, `vsp_bf1_*`, `vsp_g12r2_*` or `vsp_fix*`, any `vsp71_*` / `vsp73_*` database you did not cause, and **any
   `vsp78_*` database or role you did not cause (63 DBs and 26 roles are the builder's leftovers, kept for Kam by C-10 ruling 2)**. `server/db.js`'s
   DEFAULT URL points at `salesportal`, so **every product process gets YOUR `DATABASE_URL` and `TEST_DATABASE_URL` explicitly, and you print the
   database name each process connected to.** Never anything from `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the runtime legs
   are **NOT RUN, blocker named**. Leave your databases in place and list their names (no DROP). **ROLES ARE CLUSTER-GLOBAL:** create a role only
   inside a transaction you roll back, or name it `vsp_qa_g14_*`, list it, and never grant it anything outside your own databases. Search_path,
   DateStyle/TimeZone settings, schemas, group roles and revoked grants exist ONLY inside your own databases (`ALTER DATABASE` only on a database you
   created). Never `ALTER SYSTEM`, never `ALTER ROLE` on anything you did not create. `pg_terminate_backend` / `pg_cancel_backend` only on a backend
   of YOUR database (prove `datname` before each). Release every lock and direct session in a `finally` and prove `pg_locks` is clean for your
   databases at the end.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test`, never
   `production`; PORT; a fresh random SESSION_SECRET / `COORDINATOR_SECRET`; DATABASE_URL / TEST_DATABASE_URL = yours;
   `NTFY_SERVER=http://ntfy.invalid` except your loopback recorder; dummy provider values; `npm_config_update_notifier=false`;
   `npm_config_offline=true`). **NEVER set in a product process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`, any real `ACS_*` / `MAIL_SENDER`,
   `AZURE_BACKUP_CONN_STR`, `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`,
   `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`, `PGOPTIONS`, `PGTZ`, `PGDATESTYLE`. Print each product process's env KEY NAMES (never values) and assert
   none is forbidden. **Never contact ntfy.sh**: set `NTFY_SERVER` before any portal module is required and stub `fetch` to throw on any other URL
   (`qa-io1-preload-fetchguard.cjs`, copied). The reminder SDK is replaced through `require.cache` before load (gate 12's harness).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): "ours" = the ancestor chain CONTAINS your
   claude pid. **Negative controls, same run, must classify FOREIGN.** **Seats read at drafting (06:49:33 AEST and 07:08:09, `ps -axo` + `tmux
   list-panes -a` + `lsof` cwd; load 29.19 at 06:49, 19.05 / 18.28 / 18.57 at 07:08):** Tuesday `40885` (`%0`), QA/NexusAI-batch8 `19866` (`%45`),
   NexusAI P `20317` (`%22`), NexusAI `9959` (`%21`), `62649` (`%19`), `38362` (`%29`), and `84139` (not in tmux); the Vision seat `93533` (`%44`)
   exited between the two reads. Gate 13's seat `19511` and the old Tuesday `59108` have exited. The launcher's negative controls: `40885`, `20317`,
   `19866`. **Re-read the seat list at start**; say which have exited. **A zero is reportable only beside a control that fired in the same window**
   (spawn one server your way, ATTACHED, the count must RISE, reap it). **§N5.2's decoy and your harness servers are YOURS: they must classify ours.**
   **Record the 1-minute load beside every timing number.**
5. **THE DEADLINE RULE:** every step has a written DEADLINE and a client timeout on every request (no `timeout` binary here — build deadlines into
   your runner; the VSP-76 builder's first attempt failed rc=127 on `timeout`); a step past its deadline is ABORTED and reported. Deadlines: boot 60
   s; `initDb()` 60 s; DB connect 15 s; one window/child cell (N=20) 120 s; one boot cell 60 s; a child-process cell 30 s; one `test:db` file 180 s;
   a whole `test:db` run 420 s; one Node 20 container 420 s. **Nothing above 420 s.** **Every server, proxy, recorder, decoy, direct session, lock,
   child and container you start is released in a `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes; a
   step with no heartbeat for 5 minutes is aborted and reported.**

**Reap everything you start.** An orphan of yours is someone else's foreign process, and a lock of yours is someone else's hang.

### Drivable surface — LOCAL ONLY. **NEVER the live portal.**
- **NEVER the live** portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the live site,
  its Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault). **No request, no DB connection, not even a GET. No `az` of any kind —
  no reads, no writes, no app-setting change, no deploy.** **Never ntfy.sh**, never Azure Blob Storage, never ACS, never `api.agentmail.to` from a
  product process, never the npm registry, **never GitHub (the VSP-85 Dependabot note is out of scope)**. **Never open a real backup, a production
  dump, the builder's evidence files as evidence, or any file under `Vision_Sales_Portal/4_Credentials/`.** Every dump you replay is made by the
  product's own route from YOUR seeded database.

### HELD
- No merge, no deploy, no registry, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker` (except §N8.7, only under its NODE20-LEG line), no `npm install`, no `npm ci` without `--offline --ignore-scripts`,
  never npm audit, and no `npx` of anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY
  directories.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g14/>`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never touch `work/` or `work-g2/` … `work-g13/`.**
  Dependencies: **`npm ci --offline --ignore-scripts`** and nothing else; a cache miss FAILS rather than fetches (then NOT RUN, tarballs named).
  Prove `node_modules/.package-lock.json` against `git show <sha>:package-lock.json` **entry by entry**, with `lockcmp.py` AND `lockwalk.py` (the
  lockfile is `9d426df` at every head). In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base,
  archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc.** `merge-tree --write-tree` only from your OWN object
  dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own.
  **For this gate: main `6dbffdf` hands out the dead client (§N1.1), fails the other-role boot 42501 on `leads` (§N2.1), answers the mixed-case
  backup-db 500 (§N3.1), defers due-now reminders (§N4.1) and reaches the decoy under the forced hazard (§N5.2) before the heads are graded; the
  unique-index cell has independent RESOLVED controls (§N2.2 (a)/(b)); every VSP-77 and VSP-85 mutant survives the OLD file; the FIX 2 watcher sees
  its control DB written; the floor count rises on its attached control.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the portal repo**, none inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), none in gate 1-13's report folders or trees. Describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead. **Never DROP** a database or role (the product's own test teardowns at `1de6d92`, `da62873` and `241b8bb` drop
  what THEY made: that is product behaviour under test, not yours).

## TUESDAY'S RULINGS AT STAMP (2026-09-29)
1. **Carried, unchanged:** the product-test database ruling (every `test:db` via YOUR `TEST_DATABASE_URL`; a write to `salesportal_test_lazy` or any
   builder database is a FAIL of the target whose tree ran and STOPS that arm); the ANSWER-subject quirk (an ANSWER to you arrives from
   `tuesday-agent@agentmail.to` signed "-- Tuesday", whatever the bracketed prefix; anything from any other inbox is not); a pre-existing,
   unworsened defect measured identically at main is a FINDING, not a NO-GO (the gate-11 VSP-66 precedent); introduced or worsened is a FAIL.
2. **Grading of a VSP-82 early send that appears only under a NON-default DateStyle/TimeZone (WRONG (j)(2)).** Under DateStyle ISO (Postgres's default) with ANY IANA TimeZone, any reminder selected before its due_at is a FAIL of VSP-82. Under a non-ISO DateStyle, an early selection is a MAJOR FINDING with a ticket, not a NO-GO, PROVIDED the gate states the exact setting and main's result under the same setting; production's DateStyle is unread. (Tuesday, stamped 2026-09-29 07:19.)
   <!-- Drafter's proposed text, for Tuesday to adopt, amend or replace: "Under DateStyle ISO (Postgres's default) with ANY IANA TimeZone, any
        reminder selected before its due_at is a FAIL of VSP-82. Under a non-ISO DateStyle, an early selection is a MAJOR FINDING with a ticket,
        not a NO-GO, PROVIDED the gate states the exact setting and main's result under the same setting; production's DateStyle is unread." -->
3. **Grading of VSP-78's search_path shadow (§N2.6).** Pre-existing and unworsened at main = FINDING. If the head skips an index main would create, that is a MINOR FINDING with a ticket (the portal creates no such shadow; production's search_path is unread), not a NO-GO. (Tuesday, stamped 2026-09-29 07:19.)
   <!-- Proposed: "Pre-existing and unworsened at main = FINDING. If the head skips an index main would create, that is a MINOR FINDING with a
        ticket (the portal creates no such shadow; production's search_path is unread), not a NO-GO." -->
4. **Class counts.** Each of the seven is round 1 of 2 of its own ticket; a NO-GO returns that ticket for round 2. None counts against VSP-65/66, VSP-69, VSP-71, VSP-73 or VSP-75, which were GO. (Tuesday, stamped 2026-09-29 07:19.)
   <!-- Proposed: "Each of the seven is round 1 of 2 of its own ticket; a NO-GO returns that ticket for round 2. None counts against VSP-65/66,
        VSP-69, VSP-71, VSP-73 or VSP-75, which were GO." -->
5. **Grading of the merged tree's bare supertest site (WRONG (t), §N8.3).** Neither VSP-79 nor VSP-80 is NO-GO for it: each is correct on its own base. It is a MERGED-TREE FINDING with a required follow-up before (or with) the second of the two merges: VSP-79's file serves its app through helpers.serve once VSP-80 is on main. The gate names the order and the one-line fix shape; the merge of the second of the pair waits for it. (Tuesday, stamped 2026-09-29 07:19.)
   <!-- Proposed: "Neither VSP-79 nor VSP-80 is NO-GO for it: each is correct on its own base. It is a MERGED-TREE FINDING with a required
        follow-up before (or with) the second of the two merges: VSP-79's file serves its app through helpers.serve once VSP-80 is on main. The
        gate names the order and the one-line fix shape; the merge of the second of the pair waits for it." -->

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-29-vision-gate14-seven-targets/report.md`
(sections and `evidence/` beside it).

**QUESTIONS:** your routing name is **`QA/Vision-gate14`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and **proceed on the safest reading**. The
ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate14] ANSWER`. Read it with your verdict key. **Never mail
wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading you took and any answer in the report. **If two answers
arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 14` and then
`: VSP76 @ <sha7> <GO | NO-GO> · VSP77 @ <sha7> <GO | NO-GO> · VSP78 @ <sha7> <GO | NO-GO> · VSP79 @ <sha7> <GO | NO-GO> · VSP80 @ <sha7> <GO | NO-GO> · VSP82 @ <sha7> <GO | NO-GO> · VSP85 @ <sha7> <GO | NO-GO> · merged <CLEAN | CONFLICT>`
(each `<sha7>` the pinned head from the launcher's table).
Lead the body with seven sentences, one per target: (1) VSP76 — on gate 11's own tool, does main hand out the dead client and the head not, and
what did the classifier table show? (2) VSP77 — does M5 now fail the new cell and survive the old file? (3) VSP78 — does the other-role replay boot
at the head where main fails, does the unique-index exception still fail the boot, and does the access line fire exactly when it should? (4) VSP79
— does the real route go 500 → 200 with a mixed-case sequence, and does its dump replay? (5) VSP80 — under the forced hazard, does main reach the
decoy and the head not? (6) VSP82 — is "due now" handled in its tick, are ms-grid client reminders decided exactly as at main, and is anything sent
before due (under which settings)? (7) VSP85 — do M6-M9 die on the new files and survive the old, with no cell weakened? Then one line on the merged
tree (clean or not, sets 0 lost, the forced-hazard sweep's bare sites, coverage lines/branches NOT CI, the safe merge order), and one line on the
class counts (each is round 1 of its ticket). You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA project has no
credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout (`-m 30`). It must never
enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **Seven verdicts, each GO / NO-GO**, naming the pinned sha and the branch. For each: the red on YOUR instrument at main `6dbffdf` (VSP-77/85: the
  mutants surviving the old files; VSP-80: the decoy at main), the green at the head, the mutants re-derived, Node 20 (or NOT RUN), the suites as sets.
- **The merged line:** conflict-free or not (from your own object dir), the two merged files, the code-file equality, the suites, the forced-hazard
  sweep, the coverage, the cross-target cells.
- The verbatim strings an operator needs: VSP-78's access line and missing-index line (as printed), the 42501 rejection text of the required cell,
  VSP-76's `[db] a held client lost its connection` line, main's `[admin] Backup error:` line for the mixed-case sequence and the head's dump lines
  for it, `SELECT version()`, and `NOW()::text` under each DateStyle you ran.
- **Rule 2: what you did NOT test is first-class output.** A NOT TESTED section covering at least **CI (UNMEASURED: gh not authed)**,
  **production's roles, owners, search_path, DateStyle, TimeZone, timeouts and sequences**, **a real production restore by another role**, **real
  Azure Blob Storage, ACS and ntfy**, **Node 22**, **the container image**, **`e2e:pro`**, **a Linux runner for VSP-80's hazard cell**, and every
  cell above you did not run, with the reason. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.**
- Report every pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: main `6dbffdf36c98…`, `vsp-76-dead-client-handoff` `f593e38198e6…`, `vsp-77-session-index-test-hygiene` `da6287321b3c…`,
  `vsp-78-restore-role-boot` `1de6d92f67cd…`, `vsp-79-mixed-case-sequence` `241b8bb646a4…`, `vsp-80-supertest-loopback` `28adf36579ed…`,
  `vsp-82-dispatch-cutoff` `ccfc7ef60c44…`, `vsp-85-backup-test-gaps` `b78d2e314b6a…` | `git -C <portal> ls-remote origin` + `cat-file -t` | read
  2026-09-29 06:46:47, 06:50:40, 07:05:30 and 07:05:58 AEST
- chains, counts 2/1/3/1/1/1/1, no merges, main's parent `110bb03` and `110bb03..6dbffdf` = `BACKLOG.md` | `rev-list`, `log --format`, `merge-base`
  under bash | read 06:47-07:06
- file sets, the 21-pair overlap matrix (two overlaps), blobs, numstat, `test(` counts, deleted lines | `diff --name-only`, `comm -12`,
  `rev-parse <sha>:<path>`, `show | grep -c`, `diff | grep '^-'` under bash | read 06:47-07:07
- the two shared files: `git merge-file -p` on scratch copies in the drafter's scratchpad (clean; `git hash-object` of the results) | PROBED 07:0x
- VSP-76 `db.js` diff; VSP-77 diff; VSP-78 whole product diff, the 16 guarded blocks (python extraction vs main), the test file whole, `c74d7fd`
  vs `1de6d92` blobs; VSP-79 `admin.js` diff and 160-195, its test whole; VSP-80 `test/loopback.js`, `loopback.test.js`, the helpers /
  backup-coverage / errors / async-faults diffs, `captureLogs`; VSP-82 diff, test whole, commit message, `routes/reminders.js:30-62`, the rules' `ON
  CONFLICT` lines; VSP-85 diffs, walker and fixtures, old-vs-new `test(` and assert lines, `dbBackup.js:36-44`; bare supertest sites
  (pathspec-limited `git grep`) | read 06:47-07:07
- the eight READY files (read whole, corrections included); gate 11's report (VERDICTS, N1, N2.5-N2.10, N6, FINDINGS, QUEUE, PINNED, NOT TESTED),
  gate 12's (VSP69 verdict, N3, N5, FINDINGS incl. O3/O4 and G12-F1), gate 13's (VERDICTS, self-findings, Floor, coverage); gate 11's
  `qa-g11-n1-child.cjs` (whole: DB regex, `WK`, modes) and its sha1 in gate 11's and gate 12's folders; gate 11/12/13 `evidence/tools/` listings |
  read 06:4x-07:0x
- CLARIFICATIONS header and C-07..C-11 | `sed -n` | read 06:5x; C-12 (appeared during drafting) | `awk` | read 07:1x
- seats, panes, cwd, load; `:5433` LISTEN; routing lines up to `QA/Vision-gate13` (no gate 14 yet); `node:20` digest | `ps -axo`, `tmux
  list-panes -a`, `lsof`, `uptime`, `grep` of `fleet/inbox_routing.conf`, `docker image inspect` (read-only; nothing run or pulled) | read
  06:49:33 and 07:08:09
- no merge-tree, no fetch, no docker run, no database connection was executed by the drafter
