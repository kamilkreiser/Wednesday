# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 10: VSP-65 ROUND 2 (the VSP65-F1 fix), portal `server/index.js` + `server/schema.sql`, TIER 1

**Drafted for Tuesday on 2026-09-27 at 10:5x-11:1x AEST by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
The builder's READY mail (on disk, read whole by the drafter):
`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-vsp65-f1-r2-READY-mail.txt`
(sent 2026-09-27T00:50:54Z = 10:50:54 AEST by `datasec-vision@agentmail.to`).
**Every builder statement below comes from that mail, the two new commit messages or the BACKLOG at the head. Each one is a CLAIM.**
**The drafter read both rows from `git ls-remote origin` at 2026-09-27 10:54:20 AEST (`cat-file -t` = commit for both and for `2adfc4a`).**
The launcher parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt. **This is a new SHA: gate 9's NO-GO was a statement about `2adfc4a` only and
expired with it; this gate's verdict is a statement about `0d992e0` only.**

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

NODE20-LEG: DOCKER-PULL-NEVER
<!-- Set by Tuesday's commission ("Node 20 via an image already present (DOCKER-PULL-NEVER)"). The launcher refuses anything but
     NOT-RUN | DOCKER-PULL-NEVER. The drafter did NOT run docker: "node:20 is present" rests on gate 9's own `docker image inspect`
     (report §N.7, `sha256:8f693eaa7e0a…`, linux/arm64, 2026-09-27 10:0x) and the builder's READY (same digest prefix). Re-prove it (§N.7). -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build this change and you owe the builder nothing. **Every line below that reports what the builder says is a
CLAIM, never evidence.**

**One gate, ONE target, ONE verdict: GO / NO-GO for VSP65 at its pinned sha `0d992e0`.**

**TIER: VSP65 round 2 is TIER 1.** It still changes `server/db.js` (every database call in the live portal goes through it; that file
is the SAME BLOB as at round 1) and now ALSO changes how the live portal gets its session table: the session store no longer creates
it (`createTableIfMissing: false`), and `server/schema.sql` creates it at every boot. **Both failure directions are in scope**: a stall
that still poisons an instance or hangs a request, AND a healthy production-shaped database on which the new boot DDL now fails, blocks,
or changes the live session table.

**⚠ Names, written out every time:** **VSP65 = Jira VSP-65 = gate 7's "arm (e), unfaulted half" = the BACKLOG residual "The Postgres
pool has no query or connection timeout…"**; **VSP65-F1 = gate 9's Major (a transient stall on a restarted instance's first
session-store query leaves that instance 500ing every signed-in request until restart)**. The branch is
`fix/vsp-65-pool-query-timeout-2026-09-27` at `0d992e0`, **five commits on portal main `eaf024a`**: round 1's `67365ec` (fix),
`7195df7` (test), `2adfc4a` (test + BACKLOG), then round 2's `b5c3e8d` (the F1 fix) and `0d992e0` (the session-index guard).
**It is NOT on main.**

**ROUND 2 OF 2 — THE CLASS CAP.** Round 1 (gate 9, `2adfc4a`) was **NO-GO** on VSP65-F1. This is the second and last round the
fleet's two-round cap allows without Kam. **Say in the verdict, in words, that if this round is NO-GO the VSP-65 class goes to Kam; no
round 3 happens on Tuesday's word.** (The commission and the READY both word this as "a third NO-GO goes to Kam". Under the two-round
cap a NO-GO here is the class's SECOND, and it is the one that escalates. Write what you rule; do not resolve the wording for Tuesday.)

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`,
  dated 2026-09-25 15:19): read it whole. **C-01..C-06. No C-entry covers VSP-65** (drafter READ 10:56: zero matches for `VSP-65`).
- **Kam's condition from gate 7 (arm (e)): "bound it or record it as a NAMED residual with the measurement."** VSP-65 is the attempt to
  BOUND it; gate 9 measured that the bound holds on a true black hole. **Say whether it still does at `0d992e0`.**
- **PRODUCTION IS LIVE for this project.** `datasec-sales-portal-rg` holds the live site `https://datasec-sales-portal.azurewebsites.net`,
  its production Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault `datasec-sales-kv`. Production runs Node 20
  (`.github/workflows/test.yml`: "20 = prod (App Service NODE|20-lts)", READ). **Production's session table exists and was made by
  the store** (builder's claim; READ below: `563b338`, 2026-07-02, is the only commit that introduced `createTableIfMissing`, with
  connect-pg-simple 10.0.0 in its lockfile). **This round's schema.sql change WILL RUN against that table on the first boot after a
  deploy.** That is why §N.2 exists. **Nothing in this gate touches production** (§13, HELD).
- **No product choice here is Kam's ruling.** Report each of these as the BUILDER's choice and say whether it needs Kam:
  `createTableIfMissing: false` with the table in schema.sql (gate 9 offered it as one of two fix-shapes; the builder chose it over a
  retry wrapper, citing library internals); the `to_regclass` guard on the index; and everything carried from round 1 (30,000 ms query
  bound, 15,000 ms connect/wait bound, `max 10`, no `statement_timeout`, env overrides, a bad override refusing the boot).
- **Deploys are HELD for Kam. Nothing merges on your word.** Merge is Tuesday's GO on the pinned head; deploy is Kam's word.

## PRIOR ROUND
PRIOR ROUND: round 1 (gate 9) gated `2adfc4aabee231dbd3ce6ac3239de174f4dfccd6`, verdict **NO-GO** (VSP65-F1, Major).
**ITS REPORT IS ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge`
(`report.md`, 544 lines; `evidence/vsp/`, `evidence/suites/`, `evidence/redproofs/`, `evidence/node20/`, `evidence/tools/`, `evidence/mergetree.txt`).
**Read its VERDICTS, §N.1-§N.8, FINDINGS INDEX, THE QUEUE, NOT TESTED and "Self-findings" whole.** (Its QQPURGE half is not this gate's.)
Findings carried forward and their disposition (each a CLAIM until you measure it):
- **VSP65-F1 (Major)** → claimed fixed on `b5c3e8d` (+ the index guard `0d992e0`). **The headline of this gate: re-measure it with
  gate 9's OWN S8d instrument, corrected as §N.1 requires.** Gate 9's evidence: `evidence/vsp/HEAD-s8d-shrunk.txt`,
  `HEAD-s8d-shipped.txt`, `HEAD-s8boot-shrunk.txt`, `node20/node20-s8d.txt`; MAIN counterparts `evidence/vsp/MAIN-s8*.txt`.
- **VSP65-P1 (Minor, test gap: no cell pins the GUARDED check; M5 → `RangeError` after ~5,000-10,000 reuses)** → claimed closed by a new
  cell (20,000 checkouts, `max 1`). Re-derive its red (§N.4).
- **VSP65-P2 (Minor, test gap: under M3 every red was a NAME assertion)** → claimed closed by a new behavioural cell. Re-derive its red.
- **VSP65-O1 (Major, PRE-EXISTING, identical at MAIN: a link death while a `pool.connect()` caller holds its client raises
  `uncaughtException`)** → unchanged by this round (`server/db.js` is the same blob; drafter READ). **Not graded.** Say whether
  anything in round 2 touches it (the drafter READ: nothing does).
- **VSP65-O2 / O3 / O4 / O5 and the pre-existing Minors** (backup "OK" with a missing table, dispatcher at-least-once, dbRestore
  ROLLBACK masking) → unchanged; carry them by reference. **O4 (boot-time DDL fails at 30 s under a conflicting write transaction) is
  RE-OPENED in scope here**, because schema.sql now carries DDL against the busiest table in the database (§N.2(d)).
- **Gate 9's merge-tree:** `2adfc4a` × `eaf024a` CLEAN, result tree `c7aa746f…` = `2adfc4a`'s own tree (`evidence/mergetree.txt`).
- **Gate 9's self-findings bind you** (report lines 450-458): its dropped-bytes reuse check was BLIND to a queued query (use timing +
  pool counters + backend pid, never byte counts, for "never reused"); bash 3.2 has no `declare -A` (one tree per mutant, markers
  grep-proved per tree before any result is read); `netstat` shows no inet sockets on this macOS (use `lsof`); a harness that truncates
  bodies must never parse the truncated copy.
- **PRIOR WORK: verify every claim against git history and gate 9's evidence, never against this brief.**
- **Gate 9's instruments are REUSED BY COPY** from `…/2026-09-27-vision-gate9-vsp65-qqpurge/evidence/tools/`:
  `qa-g9-stallproxy.cjs` (the true black-hole / hold / oneway / cut / drip proxy, `allowHalfOpen: true`, a separate child process),
  `qa-harness-g9-vsp.cjs` (the arms S1-S8, S8boot, S8d, burst, bootddl, discard, ctl, …), `qa-g9-lib.cjs`, `run-arm.sh`,
  `run-node20.sh`, `run-suite.sh`, `mktree-portal.sh`, `mutate-vsp.py`, `qa-harness-g9-m5probe.cjs`, `qa-mkdb.cjs`, `qa-dbcheck.cjs`,
  `qa-floorcount.py`, `qa-harness-floorctl.mjs`, `qa-io1-preload-fetchguard.cjs`, `qa-io1-preload-hidelayer.cjs`, `qa-run.py`,
  `lockcmp.py`, `lockwalk.py`, `tapsets.py`. **COPY what you use into this gate's own `evidence/tools/`, read it before you trust it,
  and RE-POINT every hard-coded gate-9 path** (drafter READ: `run-arm.sh`, `run-node20.sh` and `mktree-portal.sh` hard-code gate 9's
  `EV`/`WK` paths; `qa-mkdb.cjs:24-25` and `qa-harness-g9-vsp.cjs:15` hard-code and ENFORCE the `vsp_qa_g9_` prefix). **Never edit,
  run from, or write into gate 1-9's copies, evidence, trees or databases.** Record the sha1 of each copy before and after your edits.
- **Self-findings from gates 2-9 bind you:** quote every path (the project path has a space and a `!`); run every loop and every
  `git show <sha>:<path>` under `bash`, not zsh (the drafter hit zsh's no-word-split on an unquoted file list at 11:0x and got a false
  zero — the reason this rule exists); never detach a control server; **the portal test-DB name MUST end in `_test`**; npm's
  update-notifier egresses unless you disable it; record the load average beside every timing number (**a latency result with no load
  figure is not a measurement**); the floor is SHARED — other QA gates and NexusAI seats are live on this box (§13.4).

## PIN — HEADS (PRE-FILLED BY THE DRAFTER; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head; the target row has a 40-hex base, a commit count and no `@`; the head is a
commit in the repo; the base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals the head NOW. **The target is NOT on main and is NOT stale:** `merge-base(0d992e0, eaf024a) = eaf024a`,
`git rev-list --left-right --count eaf024a...0d992e0` = `0 5` (READ 10:54). **Gated anchors (the launcher checks them):** main `eaf024a`
has parents exactly `f95f625` + `15cd733` (gate 7's gated IO1F1 head); round 1's gated head `2adfc4a` is an ancestor of the head, and
the head's first-parent chain is exactly `0d992e0` ← `b5c3e8d` ← `2adfc4a`.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | eaf024a3edb78cd126f7398997c99172e3e87f2f | - | - | IN |
| VSP65 | portal | fix/vsp-65-pool-query-timeout-2026-09-27 | 0d992e09ebe0830dbe414aa73ca9a17a1be6c480 | eaf024a3edb78cd126f7398997c99172e3e87f2f | 5 | IN |
<!-- PIN-HEADS:END -->

Repo: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`). **The portal has no CLAUDE.md of its own inside the repo;** its rules are
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (read it; its deploy commands are NOT for you).

**The shape at drafting (READ 10:54-11:0x):**
- **Round 2 alone (`2adfc4a..0d992e0`), 4 files:** `BACKLOG.md` (+6/-1), `server/index.js` (+4/-2: `createTableIfMissing: true` →
  `false` and a comment), `server/schema.sql` (+22: `CREATE TABLE IF NOT EXISTS "session"` and a `DO $$ … to_regclass('"IDX_session_expire"')
  IS NULL … CREATE INDEX` block, appended at the end of the file), `test/db/pool-timeout.test.js` (+174/-8: 6 → 12 `test(` calls).
- **Whole branch over main (`eaf024a..0d992e0`), 6 files:** the above plus round 1's `server/db.js` (+114/-4) and `server/db.test.js` (new).
- **Same blob at `2adfc4a` and `0d992e0`:** `server/db.js` (`0d402a0`) and `server/db.test.js` (`1f59ff2`). **Round 1's pool code is
  untouched in round 2.**
- **Same blob at main, `2adfc4a` and `0d992e0`:** `package.json` (`d3b76fb`), `package-lock.json` (`9d426df`, 248 `packages` entries
  including the root), `.github/workflows/test.yml` (`0cb2d05`), `server/errors.js` (`c0c4b0e`), `server/initDb.js` (`e1ccf0f`),
  `test/db/helpers.js` (`1d90638`), `scripts/run-db-tests.js` (`c48966c`). Lockfile versions: connect-pg-simple 10.0.0, pg 8.18.0,
  pg-pool 3.11.0, express-session 1.19.0.
- **`0d992e0`'s tree is `30798eef35ac3ee903490b3a909bd9081e17d99d`** (`rev-parse 0d992e0^{tree}`). The READY's merge-tree result equals it.
**A GO is a statement about the pinned SHA only.** If the head moves, the verdict expires.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; both are claims)
- **(a) GATE 9's S8d INSTRUMENT CANNOT FIRE AT THIS HEAD AS WRITTEN — a vacuous green is the default outcome (READ, drafter; the
  headline instrument correction).** Gate 9's S8d (and S8boot) arm triggers its one-shot hold with
  `ctx.proxy.rule({ kind: 'match', match: 'to_regclass', action: 'hold', liftMs: lift, once: true })`
  (`evidence/tools/qa-harness-g9-vsp.cjs:399`, and `:362` for S8boot). `to_regclass` is the text of connect-pg-simple's ENSURE query
  (`node_modules/connect-pg-simple/index.js:177`, `'SELECT to_regclass($1::text)'`). **At `0d992e0` that query is never sent**:
  `_ensureSessionStoreTable` returns at once when `createTableIfMissing === false` (`index.js:198`). So gate 9's arm, copied unchanged,
  holds NOTHING at the head, B's first `/me` answers 200 at once, and the arm reads as "F1 fixed" without having produced a stall.
  **Required (§N.1):** re-target the hold to "B's FIRST session-store query, whatever its text" (at `2adfc4a` that is the `to_regclass`
  ensure; at `0d992e0` it is the store's `get`, `'SELECT sess FROM ' + quotedTable + ' WHERE sid = $1 AND expire >= to_timestamp($2)'`,
  `index.js:364`), **and make the arm REFUSE to report unless the proxy logged exactly one `stalled` event for that request and the
  request's elapsed time is ≥ the bound.** A run where the hold never fired is **VOID**, not green.
- **(b) The builder's F1 cell is NOT the gate's S8d shape, by the READY's own account.** The READY's NOT TESTED says so: its proxy's
  one-shot stall "drops the connection rather than holding and releasing bytes". READ at `0d992e0` (`test/db/pool-timeout.test.js:29-61`):
  `stallOnce = Buffer.from('session')` marks the connection `stalled` for good (its comment: "A connection that has dropped a single byte
  is out of step for good"); nothing is ever released. Gate 9's S8d HOLDS both directions and releases every buffered byte in order at
  `bound + 2 s` (`qa-g9-stallproxy.cjs:99-104`), so the late answer lands on a client the pool has already discarded. **Only your
  instrument measures that shape.** Also, the builder's proxy is still `net.createServer` with the default `allowHalfOpen: false` and
  still tells Postgres when the app closes (`:60`) — gate 9's correction (a) stands for every cell that uses it.
- **(c) The builder's OWNER cell tests a SLICE of schema.sql, not the boot.** READ (`pool-timeout.test.js:330-356`): it runs
  `schemaSql.slice(schemaSql.indexOf('CREATE TABLE IF NOT EXISTS "session"'))` as the non-owner role, with the comment "A boot role that
  owns the rest but not this table". `initDb()` runs the WHOLE file as ONE multi-statement `pool.query(sql)` (`server/initDb.js:6-8`,
  READ). So the cell proves the new block tolerates a non-owner; it does not prove a boot does. Whether "owns the rest but not session"
  is a real production shape at all is unverifiable (production); the READY itself calls production's owner "very likely the boot role".
  **Measure the whole-file boot in the owner configurations of §N.2(c), and say which ones the guard actually changes.**
- **(d) The builder's SHAPE cell compares less than it claims.** READ (`:299-328`): it compares `information_schema.columns`
  (name, data_type, is_nullable, datetime_precision, collation_name) and `pg_indexes` (name + def). It does NOT compare constraint
  deferrability (table.sql declares the PK `NOT DEFERRABLE INITIALLY IMMEDIATE`; schema.sql declares it inline with defaults), the
  relation's `reloptions` (table.sql says `WITH (OIDS=FALSE)`), ownership, or the CHAR/varchar typmod. The drafter expects these to
  match (they are defaults), **but the cell does not prove it: compare catalogs yourself (§N.2(a)).**
- **(e) Line numbers in the READY are round-1 line numbers.** "main() (server/index.js:173 before createApp at :177)": at `2adfc4a`
  `initDb()` is at `:173` and `createApp()` at `:177`; **at `0d992e0` they are `:175` and `:179`** (the comment added two lines). The
  claim holds; the citation is stale. Quote the head's lines.
- **(f) "Every path that builds the app against a database runs initDb first" — the drafter's census AGREES for the paths that call
  `createApp()`, but the READY's census does not cover paths that build or REBUILD the DATABASE without `initDb()` (READ; re-derive in
  §N.3).** `createApp()` callers at `0d992e0` (`git grep -n createApp`): `server/index.js:179` (`main()`, after `initDb()` at `:175`),
  and five `test/db` files — `async-faults.test.js:31`, `completed-response.test.js:56`, `concurrency.test.js:24`, `routes.test.js:36`,
  `pool-timeout.test.js:79` and `:211` — each after `resetDb()` → `initTestDb()` → `initDb()` (`test/db/helpers.js:23-27,48-52`). CI's
  e2e step boots `node server/index.js` (`test.yml`), i.e. `main()`; the `Dockerfile` CMD is `npm start` = `node server/index.js`.
  **Not covered by the READY:** the admin `GET /api/admin/backup-db` SQL dump, which dumps EVERY public table INCLUDING `session`
  (`routes/admin.js:95-100`, `pg_tables`), with a `CREATE TABLE IF NOT EXISTS` built from `information_schema` (columns + PRIMARY KEY
  only — no `IDX_session_expire`, no collation clause); `server/dbRestore.js` (a CLI: requires `./db` but never `initDb`; `DELETE FROM`
  then INSERT over a fixed `RESTORE_ORDER` that has no `session`); `scripts/ensure-test-db.js`. **What changed is the fallback: at main
  and `2adfc4a` a database with no session table got one from the store on first use; at `0d992e0` nothing creates it except
  `initDb()`.** Measure what an app does on a database whose session table is missing (§N.3).
- **(g) "The session table is not in schema.sql at eaf024a/2adfc4a" — TRUE (READ):** `schema.sql` is the same blob `0924671` at both,
  with 18 `CREATE TABLE` and zero case-insensitive `session` matches; at `0d992e0` it has 19. **"It exists only because the store made
  it (563b338, 2026-07-02, VSP-49)" — consistent (READ):** `git log -S createTableIfMissing -- server/index.js` lists only `563b338`
  ("fix(security): VSP-42..50/52 — … sessions …"), whose diff adds `store: new PgSession({ pool, createTableIfMissing: true })`, and
  whose lockfile pins connect-pg-simple 10.0.0 (so production's table came from 10.0.0's `table.sql`, if nobody made it by hand —
  unverifiable).
- **(h) "connect-pg-simple 10.0.0 index.js:198-204 caches #tableCreationPromise and never clears it" — TRUE at source (READ, the
  portal checkout's `node_modules/connect-pg-simple`, `package.json` 10.0.0 = the lockfile's):** `:197-204`. "With that option …
  returns before it touches #tableCreationPromise (index.js:198)" — TRUE. "The store's prune runs only on a 15-min timer after first use
  (index.js:225-236)" — CONSISTENT: `DEFAULT_PRUNE_INTERVAL_IN_SECONDS = 60 * 15` (`:6`), `#initPruneTimer` is called from `get` /
  `set` / `destroy` / `touch` (`:362, :386, :406, :424`) and at `:264`. **Re-read all of it in YOUR tree's `node_modules`.**
- **(i) The 42501 claim is the builder's MEASUREMENT on the local server, and says nothing about production's Postgres major.** "On
  Postgres 16, CREATE INDEX IF NOT EXISTS checks table OWNERSHIP before existence." The local compose db is `postgres:16-alpine`
  (`docker-compose.yml`, READ); production's major is unknown (READY NOT TESTED). **Reproduce it locally, quote `SELECT version()`, and
  say the production version is NOT TESTED.** Note: the compose `POSTGRES_USER` is `salesportal`, which is therefore a SUPERUSER on that
  server, and **a superuser bypasses the ownership check** — any owner cell run as `salesportal` proves nothing; every owner cell must
  `SET ROLE` to NON-superuser roles (the builder's does).
- **(j) The commission's "Vision's compose db on 127.0.0.1:5433" — it listens on ALL interfaces.** `lsof -nP -iTCP:5433 -sTCP:LISTEN`
  at 10:56 shows `com.docker.backend` on `TCP *:5433 (LISTEN)` (IPv6 wildcard). You still connect to `127.0.0.1:5433` only.
- **(k) UNVERIFIABLE by design, and you must not try:** production's session-table owner, its Postgres version, its search_path, whether
  its `IDX_session_expire` exists, and a real App Service restart or multi-instance boot. **Carry each as NOT TESTED.**
- **Verified TRUE at source (READ):** both heads by `ls-remote` (above); 5 commits, 0 behind; the round-2 diff is exactly as the READY's
  THE FIX section describes; the six `pool.connect()` callers are unchanged from round 1 (`server/routes/quotes.js:262`,
  `server/routes/admin.js:93`, `server/reminders/dispatcher.js:121`, `server/seed.js:18`, `server/seedCollateral.js:13`,
  `server/dbRestore.js:149`); 12 `test(` calls in `pool-timeout.test.js` at the head (6 at `2adfc4a`), matching "db 72 -> 78"; no module in
  the 49 non-test `server/`+`scripts/` `.js` files memoises a query promise the way connect-pg-simple does (drafter `git grep -i -e cache
  -e promise` under bash: only JSDoc, `Promise.all`, `new Promise` in `quotes/pdf.js`, and the new comment in `index.js:80` — re-derive it,
  §N.3(e)).

## THE READY — its FIX, PRIOR WORK, CELLS, RED-PROOFS and NOT TESTED, VERBATIM (the gate rules on every claim)
THE FIX
- server/index.js: new PgSession({ pool, createTableIfMissing: false }). With that option, connect-pg-simple 10.0.0's _ensureSessionStoreTable returns before it touches #tableCreationPromise (index.js:198), so nothing is cached. A stalled store query now fails only its own request.
- server/schema.sql: "session" created at boot in the exact shape of node_modules/connect-pg-simple/table.sql (same columns, collation, session_pkey, IDX_session_expire). CREATE TABLE IF NOT EXISTS, and the index only when to_regclass('"IDX_session_expire"') IS NULL.
- Why the guard on the index (found this round, MEASURED): on Postgres 16, CREATE INDEX IF NOT EXISTS checks table OWNERSHIP before existence. As a boot role that doesn't own "session" it fails: 42501 "must be owner of table session", which would stop the boot. Production's table was made by the store through the app's own pool, so the owner is very likely the boot role, but I can't read production to confirm, so the code no longer depends on it.

PRIOR WORK CHECK (why this shape and not "retry the ensure")
- Verified the gate's reading: connect-pg-simple 10.0.0 index.js:198-204 caches #tableCreationPromise and never clears it. It's a private field, so a retry wrapper would have to override the underscore method _ensureSessionStoreTable, which ties us to library internals. createTableIfMissing is a documented option.
- The session table is not in schema.sql at eaf024a/2adfc4a. It exists only because the store made it (563b338, 2026-07-02, VSP-49).
- Every path that builds the app against a database runs initDb first: main() (server/index.js:173 before createApp at :177), and every test/db suite via helpers.resetDb(). backup-db lists pg_tables dynamically; dbBackup has a fixed list without session; test/db/helpers truncateAll already skips session. So none of those change.
- The store's prune runs only on a 15-min timer after first use (index.js:225-236), so a fresh store's first query is the request's own.

CELLS (test/db/pool-timeout.test.js; the proxy gains a one-shot stall that then lifts, and a one-shot delay)
- "VSP65-F1: a fresh instance whose FIRST session-store query stalls past the bound serves every signed-in request again once the stall lifts": a second createApp() on the same pool = a restarted instance. First /me = 500 at the bound; then 3x /me on the same rep = 200; a fresh login stores a row (count +1) and its cookie gets 200 on that instance; instance A serves throughout. At 2adfc4a: "request 1 after the stall lifted is served, not a replayed failure: {"status":500,...,"ms":1}" (the gate's replay, 1 ms).
- "VSP65-F1 control (main's behaviour kept): ... SLOW but inside the bound waits and serves 200": first store query delayed 750 ms (bound 1,500), 200 after waiting, and the instance serves on.
- "VSP65-F1: schema.sql creates the session table the store expects, and is a no-op where the store already made it (production)": in a rolled-back transaction, schema.sql in a fresh schema vs table.sql in another. Columns, types, nullability, collation and index defs are deepEqual, and running schema.sql over the store-made table leaves it identical.
- "VSP65-F1: schema.sql boots even where the session table belongs to ANOTHER role ...": owner role creates it via table.sql; a different boot role runs schema.sql's session part. Rolled back, 0 test roles left.
- VSP65-P2 "(behaviour, not names): after a checked-out client times out and is released with no error, the next pool query gets a FRESH connection and answers at once": module pool, different backend pid, under BOUND/2. No name assertion at all.
- VSP65-P1 "one client checked out and released 20,000 times still answers a query (the wrapper goes on once, never stacks)": BoundedPool max 1, same backend pid throughout.

RED-PROOFS (fresh scratch tree per arm, asserted edits, markers grep-counted, node --check rc 0; final files)
- 2adfc4a code + new cells: 3 red, exactly the three F1 cells (the stall cell with the 1 ms replayed 500; the shape cell with "three columns: []"; the owner cell with "schema.sql creates the session table"). The control, P1 and P2 pass there.
- Gate's M3 (plain pg.Pool): P2 red for a BEHAVIOURAL reason: "the next query is answered, not queued behind the stalled one (1502 ms): Error: Query read timeout". Four other cells are red too (the three old name cells and F1).
- Gate's M5 (GUARDED removed): P1 red: "RangeError: Maximum call stack size exceeded". Nothing else is red.
- createTableIfMissing back to true: only the F1 stall cell is red (the replayed 500, 1 ms).
- Index back to plain CREATE INDEX IF NOT EXISTS: only the owner cell is red (42501).

NOT TESTED
- CI (gh still not logged in here), including the Node 22 coverage gate and e2e:pro on both legs.
- e2e:pro / e2e:api / e2e:feedback: they need main() booted with schedulers and outbound notifications; I didn't start one.
- Production: the owner of prod's "session" table, prod's Postgres version, a real Azure stall/failover/TLS. The index guard is there so the owner question doesn't matter; it is still unread.
- A real App Service restart; multiple instances; Node 22.
- The gate's own S1 black-hole proxy and S8d instrument on this head (mine is the builder's-proxy equivalent, with a one-shot stall that drops the connection rather than holding and releasing bytes; the pool discards it either way).

**How you treat these:** every NOT TESTED line you CAN test locally — **the gate's own S1 and S8d on this head (that is §N.1 and
§N.5)**, multiple instances on one database (two `createApp()` instances, and two concurrent `initDb()` boots, §N.2(e)), and the owner
question in every local configuration (§N.2(c)) — you test. The rest you carry into your own NOT TESTED, reworded as your own. The
READY's SUITES, Node 20, instrument-notes (the EROFS VOID run; the Logitech 501 on `127.0.0.1:49162/49164/49166`) and merge-tree
claims are in the mail on disk; re-derive each one you rely on.

## 2a. LEGITIMATE SHAPES — the fix changes a BOOT path and a GUARD whose failure path is a 500 or a failed boot, so a false alarm is damage (template §2a)
Measure every row. **A row whose expected verdict and clause disagree is a finding against this brief. Say so.**

| shape — its ordinary form, as the portal really produces it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| A boot (`initDb()` then `createApp()`) on a PRODUCTION-SHAPED database: session table made by the store at main/`2adfc4a` through the real `createApp()`, owned by the boot role, with live session rows | boot succeeds; **no DDL executes on `session`** (no new relfilenode, no catalog row change, no lock wait); every existing cookie still answers 200 on a head instance | `CREATE TABLE IF NOT EXISTS` no-op + the `to_regclass` guard skips the index | READY ("a no-op where the store already made it") — **measure it (§N.2(b))** |
| The same boot while signed-in traffic writes `session` (an open transaction holding ROW EXCLUSIVE on it, as a touch/set in flight) | boot completes without waiting on `session` | no statement in the new block needs a lock that conflicts with ROW EXCLUSIVE when the table and index already exist | drafter — **measure the elapsed; if it waits, that is O4's class on the busiest table** |
| A boot on a FRESH database (first deploy, CI, a new test DB) | table + PK + `IDX_session_expire` created, catalog-identical to `table.sql` | the new block's create path | builder (shape cell) — **re-derive with a full catalog comparison** |
| A restarted instance whose FIRST session-store query stalls past the bound and then lifts (gate 9's S8d) | that one request 500s at ~the bound (named `DB_QUERY_TIMEOUT`); every later request on that instance 200; a fresh login stores a row; `/api/health` 200 | nothing cached (`createTableIfMissing: false`) + discard-on-release | builder (its drop-shaped cell) — **measure on YOUR instrument, re-targeted (§N.1), shrunk AND shipped** |
| The same instance whose first store query is SLOW but inside the bound | 200 after the wait; serves on; nothing logged | the bound | builder (750 ms at 1,500) — **once at the shipped bound too (e.g. 20 s delay under 30 s)** |
| Two instances booting at once on a fresh database | both boot | the new block's create path under concurrency | **nobody measured it** — drafter |
| An app built on a database that has NO session table (a path that skipped `initDb()`) | **at main: the store creates the table on first use; at the head: the named failure you measure** | `createTableIfMissing: false` | **nobody measured it** — drafter (f) |
| Everything gate 9 measured as HELD (S1-S8, discard-on-release, the 15 s pool wait, the boot refusal) | unchanged from gate 9's HEAD figures, within load noise | `server/db.js` is the same blob | drafter — **re-run briefly (§N.5)** |

## N. TARGET VSP65 round 2 — the measurements (FAIL conditions stated before the runs, per Rule 1)
**FAIL condition, stated BEFORE the runs:** any request on a restarted instance that still returns a replayed failure after a transient
stall on its first session-store query has lifted (F1 not fixed), on YOUR instrument at the shrunk OR shipped bound OR on Node 20; a
boot of the head on a production-shaped database that fails, waits on the live session table, or changes that table (DDL, owner, shape,
rows) where the store already made it; a session table created by schema.sql that differs from `table.sql`'s in any catalog property
the store or Postgres relies on; any legitimate path in §N.3 that now leaves the app without a session table where main had one,
unless you rule it unreachable and say why; any regression of a gate-9 HELD result (§N.5); `npm test` or `test:db` losing any NAME
that passes at `2adfc4a` or at `eaf024a`; a P1/P2 red that is not behavioural or not reproducible; any change outside the files §PIN
lists. **An observation is not by itself a FAIL**: you rule on each one, and a Major (a legitimate production shape that now fails, or a
new crash) is a FAIL.

1. **VSP65-F1 RE-MEASURED WITH THE GATE'S OWN S8d INSTRUMENT — the headline (MEASURED).** Copy gate 9's `qa-g9-stallproxy.cjs` and
   `qa-harness-g9-vsp.cjs`; read both. **Correct the trigger (WRONG (a)):** B's FIRST session-store query, whatever its text. Suggested
   (your choice, justified in the report): arm the hold only after instance B is listening and before B's first request, match on the
   store's table name as it reaches the wire (both the ensure's bind parameter `"session"` at `2adfc4a` and the `get`'s query text at the
   head carry it — **verify that on the wire, per sha, and quote the matched chunk's first bytes**), `once: true`, with no other traffic on
   the pool during the arm. **Instrument assertions, both runs, or the run is VOID:** exactly ONE `stalled` event for B's first request;
   its trigger text logged; the first request's elapsed ≥ the bound; the `lifted` event logged at `bound + 2 s`.
   **Runs (each a fresh `_test` database, one tree per sha, the real `createApp()` under `env -i`):**
   - **`2adfc4a` (RED, the instrument's positive control):** must reproduce F1 with the RE-TARGETED trigger (replayed 500s in ms after the
     lift; fresh login stores nothing; `/api/health` 200). **Also once with gate 9's original `to_regclass` trigger at `2adfc4a`** (it must
     still redden) **and once at `0d992e0`** (it must log ZERO `stalled` events — that is WRONG (a), proven, and that run is VOID by design).
     **If the re-targeted trigger does not redden `2adfc4a`, your instrument cannot see F1: stop, say so, and do not report a green.**
   - **`0d992e0` (GREEN expected):** the first `/me` → 500 at ~the bound, named `DB_QUERY_TIMEOUT`, logged; then ≥ 3 `/me` for the same rep
     → 200 with the whole body; a fresh login → 200, a session row stored (count +1, read over a SEPARATE direct connection); its cookie →
     200 on B; `GET /api/quotes` with it → 200; `/api/health` 200; `/me` again at `2 × bound + 5 s` → 200; the control on instance A → 200
     throughout; `[err]` lines after the lift = 0. Report the pool counters and the discarded client's backend pid vs the next one's.
   - **`eaf024a` (main, the history oracle):** the same shape must WAIT and serve (gate 9: 200 at 32,028 ms at the shipped bound).
   - **Bounds:** the shrunk bound (`DB_QUERY_TIMEOUT_MS=1500`, `DB_CONNECT_TIMEOUT_MS=1500`, lift at 3,500 ms) N ≥ 3 at each of `2adfc4a`
     and `0d992e0`, and **the SHIPPED bound (30,000 / 15,000, lift at 32,000 ms) once at each of `2adfc4a`, `0d992e0` and `eaf024a`**.
   - **S8boot at `0d992e0`** (gate 9's §S8c: the FIRST session query after boot is a LOGIN; held and lifted), re-targeted the same way,
     shrunk, N ≥ 1: later logins store rows and answer 200.
   - **The slow-inside-the-bound control at the shipped bound, once at `0d992e0`**: first store query delayed 20,000 ms (bound 30,000) →
     200 after ~20 s, serves on, nothing logged. (The builder measured 750 ms at 1,500 only.)
   - **The builder's own F1 cell, understood:** state in one paragraph how its drop-shaped stall differs from your hold-and-lift, and
     whether it could have caught F1 with a HOLD (i.e. whether the replay in round 1 depended on the bytes coming back). Measure it if
     cheap: your hold-and-lift at `2adfc4a` vs a drop at `2adfc4a`.
   - **Node 20** (§N.7): the re-targeted S8d once at `2adfc4a` (red) and once at `0d992e0` (green), shrunk.
   Quote for every run: statuses and elapsed ms per request, body bytes, the `DbTimeoutError` line verbatim, session-row counts, the
   proxy's link table, the load average.
2. **THE SESSION TABLE IN schema.sql — shape, the production no-op, the owner guard (MEASURED; READ where labelled).**
   (a) **Catalog identity.** In your own databases build the table three ways: (i) `initDb()` at `0d992e0` on a fresh DB; (ii) the STORE
   at `eaf024a` (`createTableIfMissing: true`, the real `createApp()`, one signed-in request — this is how production's table was made);
   (iii) `table.sql` run directly. Compare, from `pg_catalog` not `information_schema`: every attribute (`attname`, `format_type(atttypid,
   atttypmod)`, `attnotnull`, `attcollation`, `attidentity`, defaults), `relkind`, `reloptions`, `relpersistence`, the owner, every
   constraint (`contype`, `conname`, `condeferrable`, `condeferred`, `pg_get_constraintdef`), every index (`pg_get_indexdef`, `indisunique`,
   `indisprimary`), and triggers. **Any difference is a finding; say whether the store or Postgres depends on it** (the store's
   `INSERT … ON CONFLICT (sid)` needs the unique PK; its prune `DELETE … WHERE expire < …` uses the index).
   (b) **The PRODUCTION-SHAPED no-op.** Make a database the way production's was: boot `eaf024a` (or `2adfc4a`), let the STORE create
   `session`, sign in several reps (rows present), keep one cookie. Then run `0d992e0`'s `initDb()` against it and prove NOTHING changed on
   `session`: `pg_class.relfilenode`, `xmin` of its `pg_class` / `pg_index` / `pg_constraint` rows, owner, row count and contents before and
   after (a DB-local `ddl_command_end` event trigger in YOUR database is a good independent witness if your role may create one; if it may
   not, say so). Then serve that kept cookie on a `0d992e0` instance: 200. **Repeat with the table owned by a non-superuser role that is
   also the boot role** (production's likely shape). **Record `SELECT version()`.**
   (c) **The owner / 42501 guard — the WHOLE boot, not a slice (WRONG (c)).** All in your own database, all roles NON-superuser, every role
   created inside a transaction you roll back OR named `vsp_qa_g10_*` and listed in the report (roles are CLUSTER-GLOBAL on a shared
   server; say which you did). Measure `initDb()`'s `schema.sql` (the whole file) as the boot role in these configurations, each at
   `eaf024a` and at `0d992e0`: (1) boot role owns everything (production's likely shape): both pass; (2) boot role owns everything EXCEPT
   `session` (the builder's premise): the head passes; show that plain `CREATE INDEX IF NOT EXISTS` fails there with 42501 (quote it) —
   the builder's claim; (3) boot role owns NOTHING (the tables exist, made by another role): does main's schema.sql already fail (its own
   18 `CREATE INDEX IF NOT EXISTS`)? If so, the guard changes nothing in that configuration — say so; (4) `session` exists but its INDEX
   is missing and the boot role does not own `session`: the guard's `CREATE INDEX` still runs and must fail 42501 — the residual, quoted;
   (5) boot role without `CREATE` on schema `public`, tables already present: does the new `CREATE TABLE IF NOT EXISTS "session"` need a
   privilege the existing 18 do not? **Rule: in which configurations does round 2 change the outcome vs main, and is any of them a
   regression.** The drafter predicts (1)/(2) pass at the head and (3)/(5) behave as main; measure, do not trust the prediction.
   (d) **Locks on the live table during boot (re-opens VSP65-O4).** On the production-shaped DB of (b): hold a ROW EXCLUSIVE transaction on
   `session` (an `UPDATE session … ` in an open transaction, as a store `touch` in flight) for 45 s, and boot `0d992e0`'s `initDb()`:
   **elapsed, and whether it waited** (read `pg_locks` / `pg_stat_activity` over a direct connection while it runs). Then the same with
   the index MISSING (the guard's `CREATE INDEX` path takes SHARE on `session`, which conflicts with ROW EXCLUSIVE): predicted to wait
   and then fail at 30,000 ms, failing the boot — measure, and say how reachable "table present, index missing" is from production (READ
   ONLY). Also: the whole schema.sql is ONE implicit transaction; if the session block fails, show that the WHOLE file rolls back and the
   boot exits (quote `main()`'s exit path at the head).
   (e) **Two concurrent boots on a fresh database (N ≥ 10 pairs):** two processes run `0d992e0`'s `initDb()` at the same instant on a fresh
   `_test` DB. Count failures by SQLSTATE (`42P07` "relation already exists" from the guard's check-then-create window; `23505` on
   `pg_type_typname_nsp_index` from concurrent `CREATE TABLE IF NOT EXISTS`). **Control: the same at `eaf024a`** (its 18 tables race too).
   Rule whether round 2 adds a race main did not have, and how reachable it is (first deploy with 2+ instances; CI's single process).
   (f) **search_path (READ ONLY):** `to_regclass('"IDX_session_expire"')`, `CREATE TABLE IF NOT EXISTS "session"` and the store's
   `quotedTable()` all resolve unqualified names through `search_path`. State whether any of them can resolve to a different schema than
   the others (e.g. a `"$user"` schema), and whether production's search_path is known (it is not: NOT TESTED).
3. **EVERY PATH THAT BUILDS THE APP OR THE DATABASE — the builder's census, RE-DERIVED (READ, then MEASURED where marked).**
   (a) `git grep -n createApp` and `git grep -n initDb` at `0d992e0` over the whole tracked tree (the repo tracks no `node_modules`;
   drafter READ: `git ls-tree -r` lists zero `node_modules` paths). Table every `createApp()` caller and whether `initDb()` runs before it
   in the same process (drafter's census is WRONG (f); yours is the one that counts).
   (b) Every path that CREATES or REBUILDS the schema without `initDb()`: `server/dbRestore.js`, the backup-db SQL dump
   (`routes/admin.js`), `scripts/ensure-test-db.js`, `docker-compose.yml`'s db service, the `Dockerfile`, CI. For each: can it leave a
   database with app tables but NO session table, or a session table WITHOUT its PK or index? **MEASURED:** take a backup-db dump of your
   own production-shaped DB through the real route (admin signed in, archiver output unzipped under your project), replay its SQL into a
   FRESH database (with the `pg` client in your tree; never `psql` against anything but your own DB), then (i) run `0d992e0`'s `initDb()`
   and compare the session catalog with §N.2(a)'s reference; (ii) run it in the other order (initDb, then the dump). Rule each outcome.
   (c) **MEASURED: an app on a database with NO session table** (app tables present; `session` absent), at `eaf024a` and at `0d992e0`:
   login, `/me`, `/api/health`. Main: the store creates the table on first use. Head: quote the status, the log line (`42P01`?), and
   whether `/api/health` stays 200 while every signed-in request fails (the same "healthy-looking but useless" shape F1 had). **Rule its
   reachability** from the paths in (a)/(b). If the only way to reach it is a path that never boots the product, say so.
   (d) `truncateAll` skipping `session` (`test/db/helpers.js`) and `dbBackup.js`'s fixed `TABLES_TO_BACKUP` (10 tables, no `session`):
   READ, confirm unchanged and irrelevant, one line each.
   (e) **Is F1's class present anywhere else?** VSP-65 made every query rejectable at 30 s. Census (READ, under bash, over the 49 non-test
   `server/` + `scripts/` `.js` files at the head, AND the request-path libraries in YOUR tree: express-session 1.19.0, connect-pg-simple
   10.0.0, pg-pool 3.11.0) every place a promise or result of a DATABASE call is cached for the life of the process. A cached rejection
   anywhere is F1 again. **Include a positive control for your grep** (a file you know contains the token must match).
4. **RED-PROOFS, RE-DERIVED (parse-checked, fresh tree per arm, `node --check` rc quoted; a red from a mutant that does not parse is VOID).**
   **Assert every tamper landed** (grep the literal, per tree) before reading its result. Run the head's `test/db/pool-timeout.test.js`
   (12 cells) plus `npm test` in each arm.
   - **R0: `2adfc4a`'s code with the head's `pool-timeout.test.js` copied in** (hash-verified): the READY says exactly 3 red — the F1 stall
     cell (replayed 500 in ~1 ms), the shape cell ("three columns: []") and the owner cell ("schema.sql creates the session table"). **Say
     which of the three reds are BEHAVIOURAL and which are "the feature is absent"** (the drafter READ: the shape and owner reds at
     `2adfc4a` come from schema.sql having no session block at all).
   - **M3 (gate 9's: plain `pg.Pool`, no `BoundedPool`) → VSP65-P2 must redden for a BEHAVIOURAL reason** (READY: "the next query is
     answered, not queued behind the stalled one (1502 ms): Error: Query read timeout"). Quote the assertion that fired. Also run P2 N ≥ 5
     at the HEAD (its `ms < BOUND_MS / 2` threshold is load-sensitive: quote the load each time; a flake at head is a finding).
   - **M5 (gate 9's: `GUARDED` check removed) → VSP65-P1 must redden with `RangeError: Maximum call stack size exceeded`.** Gate 9's probe
     found the RangeError "before 10,000" checkouts; P1 does 20,000. Quote P1's elapsed time at head and under M5 (it runs inside
     `test:db`'s 180 s file deadline), and the depth at which M5 throws on this box's Node 26 AND Node 20 (stack depth differs by version:
     if Node 20 survives 20,000 under M5, P1 is not a red there — say so).
   - **M6: `createTableIfMissing` back to `true`** → READY: only the F1 stall cell red. **Also run YOUR re-targeted S8d on M6** — it must
     redden (this is your instrument's second positive control, on the head's own code).
   - **M7: the index back to plain `CREATE INDEX IF NOT EXISTS "IDX_session_expire" ON "session" ("expire")`** → READY: only the owner cell
     red (42501). Reproduce.
   - **M8 (yours): the session block removed from schema.sql, `createTableIfMissing: false` kept** — which cells redden, and does the unit
     suite notice at all? (Predicted: every signed-in `test:db` cell; `npm test` does not load `server/index.js`, so it stays green. Measure.)
   - **M9 (yours): `CREATE TABLE IF NOT EXISTS "session"` without `CONSTRAINT "session_pkey" …`** — does any cell other than the shape
     cell redden? (The store's `ON CONFLICT (sid)` needs a unique index; predicted: every login fails. Measure.)
   **A behaviour with no reddening cell is a finding.**
5. **ROUND 1's HELD RESULTS, RE-RUN BRIEFLY AT `0d992e0` (MEASURED; one run each unless marked; compare to gate 9's HEAD figures and
   say "same" or quote the difference).** `server/db.js` is the same blob, so any difference is either round 2 or load: quote load.
   - **S1 black hole** (your proxy, no FIN back, Postgres never told): the ticket cell ×3, the read cell, generate — shrunk; **and the
     ticket cell once at the SHIPPED bound** (gate 9: 200 at 30,004 ms; read 500 at 30,011; generate 500 at 60,054). App sockets and fds
     back to baseline (`lsof -p`), as gate 9 measured.
   - **S6 handshake** at the shipped bound (gate 9: `DB_CONNECT_TIMEOUT` at 15,004 ms). **S7 late death**: 0 `uncaughtException`.
     **S8 transient generate** (bound 5,000, lift 7,000): 500 at ~7 s, three follow-ups each get their own answer.
   - **Discard-on-release**: generate and backup-db at the shrunk bound; pool counters and backend pids (never byte counts — gate 9
     self-finding 4).
   - **The 15 s pool-wait cap** at the shipped bound: 10 × `pg_sleep(20)` + an 11th signed-in request → 500 `DB_CONNECT_TIMEOUT` at
     ~15,004 ms (gate 9). Note: at the head the 11th request's first store query is `SELECT sess …` (no ensure); say whether that changes
     anything.
   - **Boot refusal** (`DB_QUERY_TIMEOUT_MS=abc`, real require under `env -i`): rc 1 and the named message.
   - **Positive control in the same session: `eaf024a` must hang in S1** (one shape is enough) — if main does not hang, your proxy is not
     producing the stall. **Negative control:** pass-through adds < 5 ms per request.
   - Gate 9's §N.4(i) (IO1F1 grace vs the query bound, both 30,000 ms): the head removes the ensure query from each instance's first
     request; **one run at the shipped values** — does the grace timer still win deterministically? (Gate 9: 5 of 5.)
6. **SUITES AS SETS, NOT COUNTS, against `2adfc4a` AND `eaf024a`, same machine, same session (MEASURED).** In fresh archived trees of all
   three shas: `npm test` and `npm run test:db` (each `test:db` on a FRESHLY CREATED `vsp_qa_g10_<epoch>_test`, proven fresh: zero user
   tables). Extract every test NAME with its outcome (a machine-readable reporter, or parse `spec`; gate 9's `tapsets.py`), and report vs
   EACH base: names passing at the base that do not pass at the head (**must be empty**); names added (READY: 0 unit vs `2adfc4a`; 6 db
   vs `2adfc4a`, exactly the six cells named in THE READY's CELLS list; 10 unit + 12 db vs `eaf024a`); names removed (expect 0); duplicates.
   Quote totals beside the sets (READY: unit 105/105 at both; db 72 → 78). Confirm `pool-timeout.test.js` ran inside `test:db` and name its
   twelve cells. `pool-timeout.test.js` alone **N ≥ 5** at the head, load quoted each time (READY: N=3, 12/12). **Also CI's coverage command
   locally** (`node --test --experimental-test-coverage --test-coverage-lines=80 --test-coverage-branches=70 $(find server -name
   '*.test.js')`) at the head: gate 9 measured 84.94% / 73.37% at `2adfc4a` (the READY now says 84.94% / 73.80%): quote yours and
   `server/db.js`'s own figures. **Label it: local Node 26.8.1 standing in for CI's Node 22; not CI.**
7. **NODE 20 LEG (production's major) — per the NODE20-LEG line at the top of this brief (DOCKER-PULL-NEVER).** Exactly ONE docker
   verb family is sanctioned, for this leg only: `docker image inspect node:20` (prove the image is ALREADY present, quote its digest;
   if absent, the leg is NOT RUN — **never pull**) and `docker run --rm --pull=never` of that image, with YOUR archived tree mounted
   **WRITABLE** (the READY's first Node 20 run was VOID on a read-only mount: `EROFS` inside `runDigest`), an explicit `-e` allowlist (the
   same allowlist as §13.3; never `--env-file`), `NODE_ENV=test`, and the database URL pointing at YOUR `_test` database via
   `host.docker.internal:5433`. Name every container `qa-g10-node20-<epoch>`. **Never `docker start/stop/exec/rm/compose` on any
   container, never `vsp-dev-db`, never `--network host`.** Run in it: `node --version` (quote), `npm test`, every `test/db/*.test.js`
   file (all seven), the re-targeted S8d at `2adfc4a` and `0d992e0` (§N.1), S1 and S6 (shrunk), and P1 under M5 if §N.4 needs it. Reap
   each container in a `finally` (it is `--rm`; confirm it is gone).
8. **CI IS UNMEASURED.** This project's `gh` is not authenticated (READY NOT TESTED; gate 9 §N.8), and **you must not use `gh` at all**.
   Say plainly: CI on `fix/vsp-65-pool-query-timeout-2026-09-27` at `0d992e0` is **UNMEASURED**, including its **Node 22 coverage gate**
   (`test.yml`, "Unit + snapshot tests with coverage gate (Node 22 only)") and its **`e2e:pro` step against a server booted by `node
   server/index.js`** on both legs — that step is the first CI run of the NEW boot path (schema.sql creating `session` on CI's fresh
   `salesportal` database). Name them as the first things to read at merge.

## 12. The merge and the queue
**The drafter ran NO `merge-tree`.** READ expectation: **`0d992e0` × main `eaf024a` is CLEAN, and the result tree equals `0d992e0`'s own
tree `30798eef…`**, because main is its merge-base (the READY reports exactly that). Quote `git merge-tree --write-tree --name-only` from
YOUR OWN object dir, or say you skipped it.
**Cells to re-run on the merged head** (name at least these): `npm test` + `test:db` as sets; `pool-timeout.test.js` N ≥ 3; your
re-targeted S8d at the shipped bound; your S1 black hole at the shipped bound; the production-shaped no-op boot (§N.2(b)); the 15 s
pool-wait arm; CI's Node 20 and Node 22 legs including the coverage gate and `e2e:pro`. **After Kam's deploy (not yours to read): the
first production boot's log** (schema.sql against production's store-made `session`).

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)**, or any port another seat
   holds. **Never `127.0.0.1:49162`, `:49164` or `:49166`** (the READY: a local Logitech plugin answers 501 there). Take every port from
   the kernel and bind `127.0.0.1` wherever YOUR harness or proxy listens. **Never start the portal's own entry point** (it binds
   `0.0.0.0` in `main()`); use the real `createApp()` and `initDb()` inside your harness only.
2. **Postgres = the local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all** (the one exception
   is §N.7, under its DOCKER-PULL-NEVER line). Create `vsp_qa_g10_<epoch>` for app runs and `vsp_qa_g10_<epoch>_test` as
   `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs; the name MUST end in `_test`). **Never** `salesportal`, `salesportal_test` (the
   builder's), any `vsp_qa_g1_*` … `vsp_qa_g9_*` database, or the builder's `vsp_bf1_*`. `server/db.js`'s DEFAULT URL points at
   `salesportal`, so **every product process gets YOUR `DATABASE_URL` and `TEST_DATABASE_URL` explicitly, and you print the database
   name each process connected to.** Local defaults from `server/db.js` / `scripts/ensure-test-db.js` for credentials only; never
   anything from `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the runtime legs are **NOT RUN, blocker named**. Leave
   your databases in place and list their names (no DROP). **Serialise or salt creation.** **ROLES ARE CLUSTER-GLOBAL:** create a role
   only inside a transaction you roll back, or name it `vsp_qa_g10_*`, list it, and never grant it anything outside your own databases.
   **Event triggers only in YOUR databases.** Never `ALTER SYSTEM`, never `ALTER DATABASE` on a database you did not create, never change
   server settings (other seats share this server). Your direct sessions and locks touch ONLY your own databases; release every lock in a
   `finally` and prove `pg_locks` is clean for your databases at the end.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test` or
   `development`, never `production`; PORT; a fresh random SESSION_SECRET / `COORDINATOR_SECRET` you generate; DATABASE_URL /
   TEST_DATABASE_URL = yours; DB_QUERY_TIMEOUT_MS / DB_CONNECT_TIMEOUT_MS only where an arm sets them, and say so; `NTFY_SERVER=http://ntfy.invalid`;
   dummy provider values; `npm_config_update_notifier=false`; `npm_config_offline=true`). **NEVER set in a product process:**
   `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`, any real `ACS_*` / `MAIL_SENDER`, `AZURE_BACKUP_CONN_STR`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product process's
   env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh**: set `NTFY_SERVER` before any portal module is
   required and stub `fetch` to throw on any other URL (gate 7's / gate 9's `qa-io1-preload-fetchguard.cjs`). The reminder dispatcher
   and the backup notifier run ONLY against recorders you wrote.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied from gate 9's evidence):
   `basename(argv[0]) == node` AND an app entry point ANYWHERE in the remaining argv, from the kernel; **"ours" = the ancestor chain CONTAINS
   your claude pid.** **Negative controls, same run, must classify FOREIGN:** at drafting (10:56 AEST) the live claudes were Tuesday
   `23230` (pane `%0`), NexusAI `20317` (`%22`), `62649` (`%19`) and `9959` (`%21`), three other QA gates `36118` (`%23`), `40285` (`%24`)
   and `35362` (`%26`), and `84139` (not in tmux, `claude /login`). **No Vision builder claude was running at 10:56.** **Re-read the seat
   list at start**; say which have exited. Never count by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. **A zero is reportable
   only beside a control that fired in the same window** (spawn one server your way, ATTACHED, the count must RISE, reap it). **Other
   gates are live on this box: record the 1-minute load beside every timing number** (it was 24.13 at 10:56 with `hw.ncpu` 8 — timing
   cells will be noisy; say so where it matters).
5. **THE DEADLINE RULE:** every step has a written DEADLINE and a client timeout on every request (no `timeout` binary here — build
   deadlines into your runner); a step past its deadline is ABORTED and reported (a hung product request IS a finding, and at `eaf024a` it
   is the expected positive control). Deadlines: boot 60 s; `initDb()` alone 60 s (**120 s** for the §N.2(d) lock arms); DB connect 15 s;
   any request at the SHRUNK bound 20 s; **any request at the SHIPPED bounds 120 s**; the S8d arm at the shipped bound 300 s; the pool-wait
   burst arm 180 s; one `test:db` file 180 s; a whole `test:db` run 420 s. **Nothing above 420 s.** State each shipped-bound exception in the
   report wherever you use it. **Every server, proxy, direct session, lock, child and container you start is released in a `finally`.**
   **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and
   reported.**

**Reap everything you start.** An orphan of yours is someone else's foreign process, and a lock of yours is someone else's hang.

### Drivable surface — LOCAL ONLY. **NEVER the live portal.**
- **NEVER the live** portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the
  live site, its Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault). **No request, no DB connection, not even a GET
  or a health probe. No `az` of any kind — no reads, no writes, no app-setting change, no deploy.** **Never ntfy.sh**, never Azure Blob
  Storage, never `api.agentmail.to` from a product process, never the Feedback_System coordinator, never the npm registry (`npm audit`
  included). **Never open a production dump or any file under `Vision_Sales_Portal/4_Credentials/`.**

### HELD
- No merge, no deploy, no registry, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker` (except §N.7, only under its DOCKER-PULL-NEVER line), no `npm install`, no `npm ci` without
  `--offline --ignore-scripts`, no `npm audit`, and no `npx` of anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR`
  and `GH_CONFIG_DIR` at EMPTY directories.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g10/>`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never touch `work/` or `work-g2/` … `work-g9/`.**
  Dependencies: **`npm ci --offline --ignore-scripts`** at the tree root and nothing else; a cache miss FAILS rather than fetches (then NOT
  RUN, missing tarballs named). Prove `node_modules/.package-lock.json` against `git show <sha>:package-lock.json` **entry by entry**, with
  `lockcmp.py` AND `lockwalk.py` (gate 9: 247/247 per tree at this lockfile, 248 `packages` entries including the root). **Never npm audit.**
  In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); **never fetch,
  pull, checkout, switch, worktree, commit, stash, reset, clean or gc.** `git merge-tree --write-tree` only as
  `GIT_OBJECT_DIRECTORY=<your own mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree
  --name-only <a> <b>`, from the gate's OWN object dir, or SKIP it and say so.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its
  own. A control derived from the run it validates is not a control. **For this gate that means: the S8d instrument must redden
  `2adfc4a` AND M6 before its green at `0d992e0` means anything.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the portal repo**, none inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), inside the builder's scratchpad, or inside gate 1-9's report folders or trees.
  The gate fixes nothing; describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead. Every proxy, preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate10-vsp65-r2/report.md`
(sections and `evidence/` beside it).

**QUESTIONS:** your routing name is **`QA/Vision-gate10`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate10] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — VSP-65 round 2` and then `: VSP65 @ 0d992e0 <GO | NO-GO>`.
Lead the body with two sentences: (1) does a restarted instance whose first session-store query stalls past the bound serve every later
signed-in request once the stall lifts, on YOUR re-targeted S8d instrument, at the shrunk and the shipped bound and on Node 20, with the
same instrument reddening `2adfc4a`? (2) is the new boot DDL a no-op on a production-shaped database (store-made table, live rows, a write
in flight), and does any legitimate path now leave the app without a working session table? Then one line: **round 2 of 2 — if NO-GO, the
VSP-65 class goes to Kam.** You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **VSP65 round 2 (the F1 fix): GO / NO-GO**, naming the pinned sha `0d992e0` and the branch `fix/vsp-65-pool-query-timeout-2026-09-27`.
  Report on each of: F1 on your re-targeted S8d (the instrument's reds at `2adfc4a` and M6, the zero-stall VOID run with the old trigger at
  the head, the greens at the head shrunk / shipped / Node 20, main's wait); the session table (catalog identity, the production-shaped
  no-op, the owner configurations, locks during boot, concurrent boots); the census of every path that builds the app or the database;
  the red-proofs R0, M3, M5-M9; round 1's HELD results re-run; the suites as sets vs `2adfc4a` and `eaf024a`; the coverage step; the
  Node 20 leg.
- The verbatim strings an operator needs: the `DbTimeoutError` line for the F1 request at the shipped bound; the 42501 message for plain
  `CREATE INDEX IF NOT EXISTS` as a non-owner (with `SELECT version()`); the error an app gives with no session table (§N.3(c)).
- One paragraph on the queue quoting §12's merge-tree result, or saying you skipped it.
- **Rule 2: what you did NOT test is first-class output.** Write a NOT TESTED section that covers at least **CI (UNMEASURED: gh not
  authed)**, **production's session-table owner, Postgres version, search_path and index**, **a real App Service restart and multiple
  real instances**, **a real stalled Azure Postgres / TLS / a real failover**, **Node 22**, **the container image** the App Service runs,
  **`e2e:pro` / `e2e:api` / `e2e:feedback`**, and **production-scale session tables** for the boot-lock arms. **Every action
  recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.** Each of §N items 1-8 carries one.
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: portal main `eaf024a3edb7…`, `fix/vsp-65-pool-query-timeout-2026-09-27` `0d992e09ebe0…` | `git -C <portal> ls-remote origin` +
  `cat-file -t` (commit; also `2adfc4a`) | read 2026-09-27 10:54:20 AEST
- chain: `0d992e0` ← `b5c3e8d` ← `2adfc4a` ← `7195df7` ← `67365ec` ← main `eaf024a` (merge, parents `f95f625` + `15cd733`); 5 ahead, 0
  behind; merge-base `eaf024a`; commit times 08:50-10:50 +1000 | `git log --format='%H %P %ad %s' eaf024a..0d992e0`, `rev-list
  --left-right --count`, `merge-base` | read 10:54
- round-2 diff (4 files) and whole-branch file set (6); the unchanged blobs (`db.js` 0d402a0, `db.test.js` 1f59ff2 at r1 = head;
  `package.json` d3b76fb, lockfile 9d426df, `test.yml` 0cb2d05, `errors.js` c0c4b0e, `initDb.js` e1ccf0f, `helpers.js` 1d90638,
  `run-db-tests.js` c48966c at all three); `index.js` 711dce0 → cdc5911; `schema.sql` 0924671 → c076d90; head tree 30798eef | `git diff
  --stat`, `git diff 2adfc4a 0d992e0 -- server/index.js server/schema.sql BACKLOG.md`, `git rev-parse <sha>:<path>` | read 10:54-10:58
- lockfile versions (connect-pg-simple 10.0.0, pg 8.18.0, pg-pool 3.11.0, express-session 1.19.0; 248 entries) | python over `git show
  0d992e0:package-lock.json` | read 10:58
- `table.sql` text; connect-pg-simple `index.js:6,117,177,197-204,225-236,264,315,322,362-440` | the portal checkout's
  `node_modules/connect-pg-simple` (package.json 10.0.0 = lockfile) — the gate re-reads it in ITS tree | read 10:58-11:0x
- the builder's proxy, the F1 / control / P1 / P2 / shape / owner cells (`test/db/pool-timeout.test.js:20-61,196-356`), 12 `test(` calls
  at head, 6 at `2adfc4a` | `git show 0d992e0:test/db/pool-timeout.test.js`, `grep -c '^test('` | read 11:0x
- `createApp` / `initDb` callers; `helpers.js`; `main()` lines (175/179 at head, 173/177 at `2adfc4a`); `require.main === module` at
  `:192`; `Dockerfile` (FROM node:20-alpine, CMD npm start); `test.yml` (e2e boots `node server/index.js`); `docker-compose.yml` db
  `postgres:16-alpine`; `routes/admin.js:1-20,55-110`; `dbBackup.js:30-41`; `dbRestore.js:1-30,120-175`; `package.json` scripts |
  `git grep -n`, `git show` | read 11:0x
- schema.sql at main/`2adfc4a`: 18 `CREATE TABLE`, no `session`; at head 19 | `git show … | grep -c -i` | read 11:0x
- `563b338` (2026-07-02) is the only commit adding `createTableIfMissing` to `server/index.js`; its lockfile's connect-pg-simple 10.0.0 |
  `git log -S createTableIfMissing -- server/index.js`, `git show 563b338 -- server/index.js`, python over `git show 563b338:package-lock.json` | read 11:0x
- the cache/promise census over 49 non-test `server/`+`scripts/` files (positive control: `server/db.js` matched) | `git grep -n -i -e cache
  -e promise 0d992e0 -- <files>` under bash | read 11:0x
- gate 9: verdicts, §N.1-§N.8, FINDINGS INDEX, QUEUE, NOT TESTED, self-findings | `…/2026-09-27-vision-gate9-vsp65-qqpurge/report.md` (whole,
  544 lines) | read 10:3x-10:5x
- gate 9's S8d trigger `match: 'to_regclass'` (`qa-harness-g9-vsp.cjs:362,399`), the hold/lift mechanics (`qa-g9-stallproxy.cjs:12-20,94-108`),
  the hard-coded g9 paths and `vsp_qa_g9_` prefix (`qa-mkdb.cjs:24-25`, `qa-harness-g9-vsp.cjs:15`, `run-arm.sh`, `run-node20.sh`,
  `mktree-portal.sh`), `evidence/vsp/HEAD-s8d-shipped.txt` head lines (trigger `to_regclass`, `DbTimeoutError` via `_rawEnsureSessionStoreTable`),
  `evidence/mergetree.txt` | `sed -n`, `grep -n -i`, `head -c` | read 10:4x-11:0x
- C-01..C-06, no `VSP-65` | Vision CLARIFICATIONS.md (2026-09-25 15:19) | read 10:56
- the two-round cap | `TUESDAY/0_Brain/learnings/_ledger_laptop_datasec_archive.md` (2026-09-07/08 rows) | read 11:0x
- `:5433` LISTEN on `*:5433` (com.docker.backend); load 24.13 / 27.84 / 24.72, `hw.ncpu` 8; seats and panes | `lsof -nP -iTCP:5433
  -sTCP:LISTEN`, `sysctl`, `ps -axo`, `tmux list-panes -a` | read 10:56
- no docker command was run by the drafter; `node:20` presence rests on gate 9 §N.7 and the READY | — | —
- builder claims | the READY mail (whole) and the `b5c3e8d` / `0d992e0` commit messages; BACKLOG at `0d992e0`
