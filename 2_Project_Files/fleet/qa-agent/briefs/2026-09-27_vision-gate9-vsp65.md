# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 9 (portal only), ONE TARGET: VSP65 = the Postgres pool query/connect timeout (`server/db.js`), TIER 1

**Drafted for Tuesday on 2026-09-27 at 09:0x AEST by a read-only drafting agent. Tuesday reviews, decides the NODE20-LEG line, stamps and launches it.**
It was commissioned on the Vision seat's READY mail of 2026-09-27 (on disk, read whole by the drafter:
`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_vision-vsp65-READY-mail.txt`).
**Every builder statement below comes from that mail, the three commit messages or the BACKLOG. Each one is a CLAIM.**
**The drafter read both rows from `git ls-remote origin` on 2026-09-27 at 08:58:13 AEST (`cat-file -t` = commit).** The launcher parses
§PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any mismatch. The verified
table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

NODE20-LEG: TUESDAY-DECIDES
<!-- Tuesday replaces TUESDAY-DECIDES with exactly one of: NOT-RUN | DOCKER-PULL-NEVER. The launcher refuses until it reads one of them.
     NOT-RUN: no Node 20 exists on this box (drafter READ 09:0x: /opt/homebrew/bin/node is v26.8.1 only; no node@20 in Homebrew, nvm,
     volta or fnm; the Homebrew cache holds node 26.8.1 only), so the Node 20 leg is NOT RUN and reported as such.
     DOCKER-PULL-NEVER: ONE narrow docker exception for this leg only (see §N.7). The builder ran its Node 20 leg in a node:20 container. -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build this change and you owe the builder nothing. **Every line below that reports what a builder says is a
CLAIM, never evidence.**

**One gate, one target, one repo (the SALES PORTAL, not QuickQuote), one verdict: GO / NO-GO for VSP65 at its pinned sha.**
QuickQuote is NOT in this gate. Do not open or build it.

**TIER: VSP65 (the pool query/connect timeout) is TIER 1.** It changes `server/db.js`, which every database call in the live portal goes
through, including the session store on every signed-in request. A bound set too tight turns a slow but healthy database into 500s for
real users. A bound that does not fire leaves the hang it was meant to fix. **Both failure directions are in scope.**

**⚠ Names, written out every time:** **VSP65 = Jira VSP-65 = gate 7's "arm (e), unfaulted half" = the BACKLOG residual "The Postgres
pool has no query or connection timeout…"**. All four mean the branch `fix/vsp-65-pool-query-timeout-2026-09-27` at `2adfc4a`,
three commits (`67365ec` fix, `7195df7` test, `2adfc4a` test + BACKLOG) on portal main `eaf024a`. **It is NOT on main.**
This is **ROUND 1 of the VSP-65 class.** There is no round cap question here.

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`,
  dated 2026-09-25 15:19): read it whole. **C-01..C-06. No C-entry covers VSP-65** (C-06 is QuickQuote's BC round 4; it is not this gate's).
- **Kam's condition from gate 7 (arm (e)): "bound it or record it as a NAMED residual with the measurement."** Gate 7 discharged it
  by NAMING the residual. **VSP-65 is the attempt to BOUND it.** Say whether it does.
- **PRODUCTION IS LIVE for this project.** `datasec-sales-portal-rg` holds the live site `https://datasec-sales-portal.azurewebsites.net`,
  its production Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault `datasec-sales-kv`. Production runs Node 20
  (`.github/workflows/test.yml` comment: "20 = prod (App Service NODE|20-lts)", READ). **Nothing in this gate touches it** (§13, HELD).
- **No product choice here is Kam's ruling.** Report each of these as the BUILDER's choice and say whether it needs Kam: the **30,000 ms**
  query bound; the **15,000 ms** connect bound, which also caps the wait for a free client; **max 10** unchanged; **no `statement_timeout`**;
  the env overrides `DB_QUERY_TIMEOUT_MS` / `DB_CONNECT_TIMEOUT_MS`; and **a bad override value refusing the boot**.
- **Deploys are HELD for Kam. Nothing merges on your word.** Merge is Tuesday's GO on the pinned head; deploy is Kam's word.

## PRIOR ROUND
PRIOR ROUND: there is no earlier round of VSP-65. The measurement it answers is **gate 7's IO1F1 arm (e)**, which gated `15cd733` (now
merged: portal main `eaf024a` = merge of `f95f625` + `15cd733`), verdict **GO for IO1F1**, with the unfaulted half recorded as a NAMED
residual.
**ITS REPORT IS ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate7`
(`report.md`, `sections/IO1F1.md`, `sections/CONVENTIONS.md`, `evidence/io1/`). **Read its IO1F1 verdict, `sections/IO1F1.md` §5 (arm (e)),
its NOT TESTED, and `evidence/io1/armE-shipped*.txt` and `armE0-deadread.txt`.**
Findings carried forward and their disposition:
- **Arm (e) unfaulted half:** `ARM-E UNFAULTED : 200 219B STILL-OPEN-45000ms after 45001 ms` (report.md), "unbounded". **This is what
  VSP-65 claims to close.** Gate 7 measured it with an **in-process store stub**, not a real connection.
- **IO1F1-O2 (observation):** if the session store's **READ** never returns, every cookie-bearing request hangs before it reaches any
  route (`STILL-OPEN at 45,003 ms`). **VSP-65 claims to bound this too** (the READY's "read cell"). Measure it.
- **IO1F1's 30 s grace (`server/errors.js` `settings.appEndGraceMs = 30000`):** covers the FAULTED half. It is unchanged by VSP-65.
  **Its 30,000 ms and VSP-65's 30,000 ms query bound are now EQUAL.** See §N.4(i).
- **IO1F1-P1 (Polish, `appEndGraceMs` has no finite guard):** not in scope. Do not fail on it.
- **PRIOR WORK: verify every claim against git history and gate 7's evidence, never against this brief.** The READY's PRIOR WORK paragraph
  says `git log -S` on `query_timeout` / `statement_timeout` / `connectionTimeoutMillis` over all refs finds only the BACKLOG text in
  `15cd733` and `scripts/create-azure-user.js`. The drafter re-ran it (READ): `query_timeout` → `2adfc4a`, `67365ec`, `15cd733`;
  `statement_timeout` → `67365ec`, `15cd733`; `connectionTimeoutMillis` → `2adfc4a`, `67365ec`, `15cd733`, `96a5ff3` (2026-04-18, where
  `create-azure-user.js` entered). Consistent with the claim. **Re-run it yourself.**
- **Gate 7's portal harnesses can be REUSED BY COPY** from `…/2026-09-23-vision-qq-gate7/evidence/`: `mktree-portal.sh`, `qa-mkdb.cjs`,
  `qa-dbcheck.cjs`, `qa-harness-io1-edges.cjs` (the real `createApp()` on real Postgres), `qa-harness-io1-boot.cjs`,
  `qa-harness-lead-io1-hang.cjs`, `qa-io1-preload-fetchguard.cjs`, `qa-io1-preload-hidelayer.cjs`, `IO1-count-async.py`, `qa-run.py`,
  `qa-floorcount.py`, `lockcmp.py`, `lockwalk.py`. **COPY what you use into this gate's own evidence folder, read it before you trust it,
  and never edit gate 1-8's copies.** **The builder's proxy (`test/db/pool-timeout.test.js`) is NOT a harness you may reuse blindly** (§N.3).
- **Self-findings from gates 2-8 bind you:** quote every path (the project path has a space and a `!`); run every loop and every
  `git show <sha>:<path>` under `bash`, not zsh; never detach a control server; **the portal test-DB name MUST end in `_test`**; npm's
  update-notifier egresses unless you disable it; record the load average beside every timing number (**a latency result with no load
  figure is not a measurement**); the floor is SHARED — other QA gates and NexusAI seats are live on this box (§13.4).

## PIN — HEADS (PRE-FILLED BY THE DRAFTER; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head; the target row has a 40-hex base, a commit count and no `@`; the head is a
commit in the repo; the base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals the head NOW. **The target is NOT on main and is NOT stale:** `merge-base(2adfc4a, eaf024a) = eaf024a`,
`git rev-list --left-right --count eaf024a...2adfc4a` = `0 3` (READ 08:58). **Gated anchors (the launcher checks them):** main `eaf024a`
has parents exactly `f95f625` + `15cd733` (gate 7's gated IO1F1 head).

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | eaf024a3edb78cd126f7398997c99172e3e87f2f | - | - | IN |
| VSP65 | portal | fix/vsp-65-pool-query-timeout-2026-09-27 | 2adfc4aabee231dbd3ce6ac3239de174f4dfccd6 | eaf024a3edb78cd126f7398997c99172e3e87f2f | 3 | IN |
<!-- PIN-HEADS:END -->

Repo: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`). **The portal has no CLAUDE.md of its own inside the repo;** its rules are
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (read it; its deploy commands are NOT for you).

**The shape at drafting (READ 08:58-09:0x):** 4 files over main — `BACKLOG.md`, `server/db.js` (+114/-4), `server/db.test.js` (new, 5
`test(` calls = 10 cells, one inside a 6-value loop), `test/db/pool-timeout.test.js` (new, 6 `test(` calls). **`package.json`
(`d3b76fb`), `package-lock.json` (`9d426df`, 248 entries), `.github/workflows/test.yml` (`0cb2d05`), `server/index.js` (`711dce0`)
and `server/errors.js` (`c0c4b0e`) are the SAME BLOB at main and head.** Lockfile versions: pg 8.18.0, pg-pool 3.11.0, pg-protocol 1.11.0,
connect-pg-simple 10.0.0, express-session 1.19.0, express 4.22.2. **A GO is a statement about the pinned SHA only.** If the head moves,
the verdict expires.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; both are claims)
- **(a) The READY's recovery claim may be an artefact of the builder's proxy (READ ONLY, drafter's hypothesis — MEASURE it).** The proxy
  is `net.createServer(...)` with the default `allowHalfOpen: false`. When the app discards a stalled client, pg sends Terminate and
  half-closes (FIN). A Node server socket with `allowHalfOpen: false` **answers a FIN with its own FIN automatically**, so the app's
  socket closes cleanly. A genuinely half-open peer (a dead host, a black-holed failover) sends nothing back. The proxy's own
  `app.on('close', () => db.destroy())` then **tells Postgres the connection is gone**, which a real half-open link never does. So the
  READY's "every stalled socket was closed by the app" and the recovery cell's `appClosed` flag (set on `'end'`, i.e. on a FIN, not on the
  fd being released) may not hold on a real half-open connection. **Your own proxy must be able to hold both sides open with no FIN back
  (§N.3, S1).**
- **(b) "Node 20 leg" (commission) has no runnable environment under this gate's floor as drafted.** No Node 20 binary exists on the box
  (READ above), and the builder's Node 20 leg ran in a `node:20` docker container. **Tuesday decides the NODE20-LEG line before launch.**
- **(c) Local Postgres was NOT listening at drafting.** `lsof -nP -iTCP:5433` returned nothing at 09:01 AEST, with Docker Desktop running
  (READ). The launcher refuses unless something LISTENs on `:5433`. **The gate never starts, stops or execs a container**; if Postgres is
  down, Tuesday asks the Vision seat to start its `vsp-dev-db`.
- **(d) The READY's CI description is incomplete, not wrong.** `.github/workflows/test.yml` at `2adfc4a` also runs (i) a **coverage gate
  on Node 22 only**, `node --test --experimental-test-coverage --test-coverage-lines=80 --test-coverage-branches=70 $(find server -name
  '*.test.js')`, and (ii) **`npm run e2e:pro` against a booted server** on both legs. VSP-65 adds ~110 lines to `server/db.js` whose
  `guard()` / `BoundedPool` paths only `test/db/` exercises. **Whether the coverage gate still passes is unmeasured by the builder** (§N.6).
- **(e) "the slowest real query is the backup's per-table SELECT *" covers ONE of the two backup paths.** `server/dbBackup.js` (nightly,
  `query()`) dumps a fixed list of TEN tables — that is the READY's "ten dump queries". **`GET /api/admin/backup-db`
  (`server/routes/admin.js:92`) dumps EVERY public table** (schema.sql creates 18) on ONE checked-out client, including `session`,
  `quotes` and the log tables. The READY does not say it measured that route. **Measure its per-query times too** (§N.4(e)).
- **(f) UNVERIFIABLE by design, and you must not try:** "Neither setting exists in production" (needs `az`); the production dump size
  "`production-full-20260226` is 96,690 bytes" (the READY names no path, and the file is production data). **Report both as READ from the
  builder only.** Do not open any production dump or anything under `Vision_Sales_Portal/4_Credentials/`.
- **(g) Behaviour changes the READY does NOT list (READ ONLY, drafter — rule on each after measuring, §N.4(f)-(j)):** boot-time DDL
  (`initDb`) is now bounded at 30 s per statement; a timed-out transaction's `ROLLBACK` runs on the same stalled client and waits a
  second full bound (generate: ~60 s, not 30 s — the READY names this only for `dbRestore`); the reminders dispatcher sends email/ntfy
  INSIDE its transaction, so a timeout after a send can roll the row back to `pending` and re-send next tick; the IO1F1 grace and the query
  bound are both 30,000 ms; a discarded client's socket can die later, after its pool has let it go.
- **Verified TRUE at source (READ):** the head and main by `ls-remote` (above); 3 commits, 0 behind; the six `pool.connect()` callers are
  exactly `server/routes/quotes.js:262` (generate), `server/routes/admin.js:93` (backup-db), `server/reminders/dispatcher.js:121`,
  `server/seed.js:18`, `server/seedCollateral.js:13` and `server/dbRestore.js:149`, and **all six call `client.release()` with no
  argument** (quotes :332, admin :182, dispatcher :159, seed :46, seedCollateral :27, dbRestore :166); the session store is
  `new PgSession({ pool, createTableIfMissing: true })` on the shared pool (`server/index.js:79`); the new cells are 10 unit + 6 db, matching
  the READY's 95→105 and 66→72 arithmetic (30+3+5+4+6+18 = 66); `pg` / `pg-pool` versions match the comment in `db.js`.

## THE READY — its NOT TESTED and BEHAVIOUR CHANGES lists, VERBATIM (the gate rules on every behaviour change)
BEHAVIOUR CHANGES FOR THE GATE TO WEIGH
- connectionTimeoutMillis also caps WAITING for a free client when all 10 are busy. Before, a request waited forever; now it gets a DB_CONNECT_TIMEOUT 500 after 15 s.
- dbBackup.dumpTable() catches per-table errors, so a timed-out table is written into the backup as an error entry, not a failed backup. Pre-existing semantics, now reachable. Not changed.
- dbRestore (CLI) runs under the same 30 s bound per statement. Its catch does ROLLBACK on the same client, which on a stalled connection times out too and masks the first error. Pre-existing pattern, bounded now. Not changed.
- statement_timeout (server-side) NOT added. It can't see a half-open connection (the server never gets the query), which is the ticket's case. It would add server-side cancellation to every statement, a separate decision.

NOT TESTED
- A real stalled Azure Postgres, TLS, or a real failover: production only, so not run. The proxy is plain TCP locally.
- CI on the pushed branch: this project's gh is not logged in (same gap as item 3). CI (.github/workflows/test.yml) runs npm test and test:db on Postgres 16 at localhost:5433, the same shape as local.
- Node 22 (the CI matrix's other leg).
- On Node 20: concurrency, harness and reminder-push weren't run (they passed on Node 26).
- e2e:api / e2e:feedback / e2e:pro (need a running server).
- The shipped 30 s / 15 s values in a live stall (the proof ran the shrunk 1.5 s bounds through the same code; the defaults are pinned by unit cells).

**How you treat these:** every NOT TESTED line that you CAN test locally (the shipped 30 s / 15 s values in a live stall; the Node 20
files the builder skipped, if the NODE20-LEG allows it) you test. The rest you carry into your own NOT TESTED, reworded as your own.

## 2a. LEGITIMATE SHAPES — the bound is a GUARD whose failure path is a 500 to a real user, so a false alarm is damage (template §2a)
Measure every row. **A row whose expected verdict and clause disagree is a finding against this brief. Say so.**

| shape — its ordinary form, as the portal really produces it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| A signed-in rep's ordinary request on a healthy local Postgres | 200, unchanged body, **no added latency vs main** (quote N and p50/p95 vs `eaf024a`) | the guard wraps `client.query` and `release` only | builder (control cell, 4 ms) — **measure against main** |
| A slow but healthy query below the bound (`pg_sleep`, and the backup-db route on a large synthetic dataset) | completes; never cut | `query_timeout` 30,000 ms | builder (507 ms at a 1,500 ms bound) — **measure at the SHIPPED bound too** |
| A legitimate burst: all 10 clients busy on healthy work for longer than 15 s, an 11th request arrives | **Before: waited and succeeded. Now: 500 `DB_CONNECT_TIMEOUT` at 15 s.** Whether that is acceptable is the gate's ruling (§N.4(a)) | `connectionTimeoutMillis` 15,000 ms | READY (named) — **measure both sides; say how plausible 10 × >15 s is from the six holders' code** |
| The session store's write never answers on an unfaulted signed-in request (the ticket) | 200 with the full body, ended at ~the bound, `DbTimeoutError DB_QUERY_TIMEOUT` logged | the bound + express-session ending on a touch error | builder (1,557 ms at 1,500) — **reproduce on YOUR proxy, and once at 30,000 ms** |
| The session store's read never answers | 500 at ~the bound, named error logged, portal keeps serving | the bound | builder (1,509 ms) — **reproduce** |
| A `pool.connect()` caller whose query stalls, releasing with no error | the client is DISCARDED, never handed out again | the `release` override | builder (M1 reddened it) — **check all SIX callers by reading, measure at least generate and backup-db** |
| A discarded client whose far end never answers the FIN | its socket and fd are released within a stated time, and a later socket error does not crash the process | pg-pool `_remove` + `pool.on('error')` | **nobody measured it** — drafter (a) |
| A bad override (`0`, `abc`, `30s`, …) at boot | the process refuses to start, with the named message | `positiveMs` throws at `require('./db')` | builder (unit cells) — **boot it for real once, `env -i`** |

## N. TARGET VSP65 — the measurements (FAIL conditions stated before the runs, per Rule 1)
**FAIL condition, stated BEFORE the runs:** any signed-in or anonymous request that still hangs past (bound + margin) on a stalled
connection; a healthy query or ordinary request cut or slowed measurably vs main; a timed-out client handed out again; a process crash
(`uncaughtException` / unhandled `'error'`) on any stall shape; a timeout that surfaces un-named where the READY claims it is named; an
unfaulted non-DB request's body, status or latency changed; `npm test` or `test:db` losing any NAME that passes at `eaf024a`; any
`server/db.js` change outside what §N.1 lists. **A behaviour change is not by itself a FAIL**: you rule on each one in §N.4, and a Major
there (a legitimate production shape that now 500s, or a new crash) is a FAIL.

1. **Scope (READ).** `git diff --stat eaf024a 2adfc4a` (4 files). Quote the whole `server/db.js` diff. Prove the files the READY says
   are untouched are the same blob (`package.json`, lockfile, `test.yml`, `server/index.js`, `server/errors.js`). Read `db.js` at the head
   end to end and state every path a query or a checkout can take: promise and callback `client.query`, submittables (cursors, streams —
   "still bounded, not renamed": is ANY submittable used in the product?), promise and callback `pool.connect`, and `pool.query`.
   **In YOUR OWN archived tree's `node_modules`, read pg-pool 3.11.0's `query()` and prove it calls `this.connect(...)`** (the READY's "pg-pool's
   own query() goes through connect(), so connect-pg-simple's pool.query path is covered too"), and read connect-pg-simple 10.0.0 to
   prove its `get` / `set` / `touch` go through `pool.query`. Read pg 8.18.0 and quote the exact strings `Query read timeout`,
   `timeout exceeded when trying to connect` and `Connection terminated due to connection timeout`, with file and line.
2. **DISCARD-ON-RELEASE, ALL SIX CALLERS (READ each, MEASURE at least two).** For each of `server/routes/quotes.js:262`,
   `server/routes/admin.js:93`, `server/reminders/dispatcher.js:121`, `server/seed.js:18`, `server/seedCollateral.js:13`,
   `server/dbRestore.js:149`, write one row: how it releases (the drafter READ `client.release()` with no argument in all six); what its
   catch does on the SAME client after a timeout (quotes and dispatcher: `ROLLBACK … .catch(() => {})`; seed and dbRestore: `ROLLBACK`
   with no catch, which REPLACES the original error; seedCollateral and admin: no ROLLBACK); how long the caller is held in total under a
   stall at the SHIPPED bounds (a queued `ROLLBACK` on a stalled client carries its own 30 s bound); and whether the discard happens.
   **Measure at least `POST /api/quotes/:id/generate` and `GET /api/admin/backup-db`** through the real `createApp()`: after a stall, the
   pool's `totalCount` / `idleCount` / `waitingCount` and the proxy's connection table must show the stalled client never reused. Also
   read and state whether any caller passes the checked-out client to code that could hold it past `release()`.
3. **AN INDEPENDENT REPRODUCTION OF THE HALF-OPEN STALL — the headline (MEASURED).** Read the builder's proxy first and write down what it
   does and does not model (correction (a)). **Then build YOUR OWN stall proxy** (in your project, `127.0.0.1`, kernel port, one per arm) in
   front of YOUR OWN database, and run the real `createApp()` through it under `env -i`. Required shapes, each at the shrunk bound
   (1,500 ms, as the builder did) AND the shipped-default rows marked ★ once at 30,000 / 15,000 ms:
   - **S1 BLACK HOLE (★).** `allowHalfOpen: true` on both sockets, ignore `'end'` and `'close'` from the app, never FIN, never RST, never
     tell Postgres. Run the ticket cell (touch never answers), the read cell, and generate. Then measure what the builder's cell could
     not: **after each discard, is the app's socket CLOSED, half-closed or still open, and does the process's fd count return to baseline**
     (`lsof -p <app pid>` before, during, and 60 s after; name the TCP state). N ≥ 3 stalls in a row; say whether sockets accumulate.
   - **S2 ONE-WAY (★ on generate).** Forward app→Postgres, drop Postgres→app, from a chosen message on. So the server EXECUTES what the client
     believes timed out. Stall generate on its `COMMIT` reply: record what the rep is told (status, elapsed) AND the row's final state read
     over a SEPARATE direct connection (`status`, `quote_number`). Then the retry: what does a second generate return? Also stall it
     mid-transaction (after `SELECT … FOR UPDATE`) and read `pg_stat_activity` / `pg_locks` over the direct connection: **is a backend left
     `idle in transaction` holding the quote row and the `quote_sequences` row after the client is discarded, and do later generates
     block on it until THEIR bound?** State how long the server keeps that backend (it never learns the client left). That is the shape a
     client-side bound cannot clean up; say whether `idle_in_transaction_session_timeout` (server-side, not added) is the missing half.
   - **S3 SERVER-SIDE WAIT (no proxy).** Hold `LOCK TABLE session IN ACCESS EXCLUSIVE MODE` in a separate direct session for 2× the bound,
     then send signed-in requests. The client bound fires; **count the server backends still waiting in `pg_stat_activity` while the lock
     is held, and say whether each abandoned backend later EXECUTES its write once the lock is released.** This is the shape a
     `statement_timeout` / `lock_timeout` WOULD bound, so it is the evidence for or against the READY's fourth behaviour change.
   - **S4 STALL MID-RESPONSE.** Forward part of a multi-row result (cut inside a `DataRow`), then silence. The error must still be the named
     `DB_QUERY_TIMEOUT`; the client must still be discarded.
   - **S5 SLOW DRIP.** Forward every byte but at a fixed low rate so a large `SELECT *` takes longer than the bound while never going
     silent. Record that `query_timeout` is a TOTAL bound, not an idle one: a slow-but-alive transfer is cut. Say what that means for the
     backup-db route on a large database.
   - **S6 HANDSHAKE STALL (★ once at 15,000 ms).** Silence from the first byte: `DB_CONNECT_TIMEOUT`.
   - **S7 LATE DEATH.** After a discard in S1, make the proxy RST the stalled socket (or end it) 5 s later: count `uncaughtException`,
     unhandled `'error'` events and `[db] idle client error` lines. **A crash here is a Major** (it is gate 5's IO1-O3 class, which
     `pool.on('error')` was added to stop).
   - **S8 TRANSIENT STALL.** A stall that LIFTS at bound + 2 s, on a client whose caller then issues `ROLLBACK`. Record what the late bytes
     do to the queued `ROLLBACK`, and prove no response is ever attributed to the wrong query on a client that is later reused.
   For every shape quote: request status and body bytes, elapsed ms, the log line verbatim (`DbTimeoutError`, `code`, `ref`), the pool
   counters after, the load average. **Positive control in the same run: the SAME shape against the `eaf024a` tree must HANG past your
   request deadline** (that is main's defect; if main does not hang, your proxy is not producing the stall). **Negative control:** the
   proxy in pass-through mode must add < 5 ms per request.
4. **THE BEHAVIOUR CHANGES — RULE ON EACH (MEASURED where possible, READ where not; label each).**
   (a) **The 15 s pool-wait cap — could a legitimate burst now 500 where it used to wait?** Measure: hold all 10 clients on healthy
   `pg_sleep` work longer than 15 s, send an 11th signed-in request, at `eaf024a` (must wait and succeed) and at `2adfc4a` (500
   `DB_CONNECT_TIMEOUT` at ~15,000 ms). Then answer from the code, READ ONLY, how many clients the six holders plus the per-request session
   store can hold at once and for how long in real traffic: backup-db holds one client for the whole dump; the dispatcher holds one while it
   makes up to 50 external sends inside a transaction; generate holds one across pricing. **Also the realistic slow-database case:** make
   every query slow (e.g. S5 at a moderate rate, or a server under load) so that 10+ concurrent signed-in requests queue — at what arrival
   rate does a healthy-but-slow database start returning 500s at 2adfc4a that main would have served? Rule: acceptable, needs a bigger
   `max` or a longer wait, or needs Kam.
   (b) **dbBackup per-table catch:** trigger a timeout on one table of `buildBackup()` (upload stubbed, never Azure) and show the backup
   object's `error` entry. Say whether a backup with an error entry is reported as a SUCCESS to its notifier (`sendNotification`, stubbed —
   never ntfy.sh).
   (c) **dbRestore ROLLBACK masking:** READ; if you run it, run it only against your own `_test` database with a stubbed download.
   (d) **No `statement_timeout`:** rule using S3's evidence, not the READY's reasoning.
   (e) **The backup-db route's headroom:** build a synthetic dataset in your own DB (state its size; scale it to at least 100× the
   READY's 96,690-byte figure, which you may NOT verify) and time every `client.query` the route makes, at the shipped bound. State the
   ratio of 30,000 ms to the slowest.
   (f) **Boot-time DDL:** `initDb()` runs `schema.sql` and `ALTER TABLE` statements at boot, now each bounded at 30 s. Hold a conflicting
   lock on one altered table longer than the bound and boot `createApp`'s caller path (`initDb` alone is enough): does the boot now FAIL
   where it waited before? Say what that means for an App Service restart while another instance holds a long transaction (READ ONLY).
   (g) **Double bound on ROLLBACK:** measure generate's total elapsed under S1 at the SHIPPED bounds (predicted ~60 s: 30 s query +
   30 s queued ROLLBACK). Say whether the rep-facing time is acceptable and whether it is below the App Service front end's request limit
   (READ ONLY; do not look it up live).
   (h) **Dispatcher re-send:** with recorder providers only (never a real send), stall `dispatchDue()`'s `UPDATE reminders` after the first
   send, let it time out, run a second tick: **is the same reminder sent twice?** At `eaf024a` the same stall hangs the tick forever (and
   cron starts a new one every 5 minutes). Say which is worse and whether this is a VSP-65 finding or a pre-existing one newly reachable.
   (i) **IO1F1 grace vs query bound, both 30,000 ms:** a signed-in request that FAULTS after its answer while the store's write stalls:
   which timer wins, is the outcome deterministic across N ≥ 5 runs, and does the client ever see a truncated body where it saw a whole
   one before? Measure at the shipped values.
   (j) **A bad override refuses the boot:** boot once under `env -i` with `DB_QUERY_TIMEOUT_MS=abc`; quote the message and the exit code.
   Say whether `server/db.test.js`, which requires `./db` at load, turns a bad value in CI's environment into a whole-suite failure.
5. **RED-PROOFS (parse-checked, fresh tree per arm, `node --check` rc quoted; a red from a mutant that does not parse is VOID).** Reproduce
   the builder's two and add your own: M1 `release` does not pass `client[TIMED_OUT]` (READY: exactly 1 red, the pool.connect() cell, at
   ~3,004 ms); M2 errors not renamed (READY: 4 red); **M3** a plain `pg.Pool` with the same options (no `BoundedPool`) — which cells redden,
   and does ANY behavioural cell catch the poisoned-client return?; **M4** `query_timeout` removed (connect bound kept) — the ticket cell
   must redden as TIMED OUT, not as a wrong status; **M5** `GUARDED` check removed so `guard()` wraps `query` on every checkout — does
   anything notice the double wrap? **Assert every tamper landed** (grep the literal) before reading its result. **A behaviour with no
   reddening cell is a finding.**
6. **SUITES AS SETS, NOT COUNTS, against base `eaf024a`, same machine, same session (MEASURED).** In fresh archived trees of BOTH shas:
   `npm test` and `npm run test:db` (the latter on a FRESHLY CREATED `vsp_qa_g9_<epoch>_test`, proven fresh: zero user tables). Extract
   every test NAME with its outcome (use a machine-readable reporter, e.g. `--test-reporter=tap` via `node --test`, or parse `spec`), and
   report: names passing at base that do not pass at head (**must be empty**); names added at head (READY: 10 unit, all `VSP-65: …`, and 6 in
   `pool-timeout.test.js`); names removed. Quote both totals beside the sets. `test:db` runs `test/db/*.test.js` one file at a time via
   `scripts/run-db-tests.js`: confirm `pool-timeout.test.js` actually ran and name its six cells. Run `pool-timeout.test.js` **N ≥ 5** at the
   head (timing cells are load-sensitive: quote the load each time), and ONCE at base with the head's file copied in (the READY's base
   red: 1 pass / 5 fail — reproduce it; the handshake cell is an import failure, not a behavioural red, say so).
   **Also CI's coverage step, locally:** run the exact command from `test.yml` (`node --test --experimental-test-coverage
   --test-coverage-lines=80 --test-coverage-branches=70 $(find server -name '*.test.js')`) at base and head on this box's Node, and quote
   the totals and `server/db.js`'s own line/branch figures. **Label it: local Node 26.8.1 standing in for CI's Node 22; not CI.**
7. **NODE 20 LEG (production's major) — per the NODE20-LEG line at the top of this brief.**
   - **NOT-RUN:** report the leg as NOT RUN, blocker "no Node 20 on this box; docker not sanctioned", and carry the READY's Node 20
     claims (unit 105/105, pool-timeout 6/6, completed-response 3/3, async-faults 30/30, routes 18/18) as the BUILDER's, unverified.
   - **DOCKER-PULL-NEVER:** exactly ONE docker verb family is sanctioned, for this leg only: `docker image inspect node:20` (prove the
     image is ALREADY present; if absent, the leg is NOT RUN — never pull) and `docker run --rm --pull=never` of that image, with YOUR
     archived tree mounted, an explicit `-e` allowlist (the same allowlist as §13.3; never `--env-file`), `NODE_ENV=test`, and the
     database URL pointing at YOUR `_test` database via `host.docker.internal:5433`. **Never `docker start/stop/exec/rm/compose` on any
     container, never `vsp-dev-db`, never `--network host`.** Run in it: `node --version` (quote), `npm test`, and every `test/db/*.test.js`
     file INCLUDING the three the builder skipped on Node 20 (concurrency, harness, reminder-push), plus your S1 and S6 shapes. Reap the
     container in a `finally` (it is `--rm`; confirm it is gone).
8. **CI IS UNMEASURED.** This project's `gh` is not authenticated (the Vision seat's status mail of 2026-09-27, item 3), and **you must not
   use `gh` at all**. Say plainly: CI on `fix/vsp-65-pool-query-timeout-2026-09-27` is **UNMEASURED**, including its Node 22 coverage gate
   and its `e2e:pro` step, and name them as the first things to read at merge.

## 12. The merge and the queue
**The drafter ran NO `merge-tree`.** READ expectation: **`2adfc4a` × main `eaf024a` is CLEAN, and the result tree equals `2adfc4a`'s own
tree**, because main is its merge-base. Quote `git merge-tree --write-tree --name-only` from YOUR OWN object dir, or say you skipped it.
**Cells to re-run on the merged head** (name at least these): `npm test` + `test:db` as sets; `pool-timeout.test.js` N ≥ 3; your S1
black-hole shape at the shipped default; the 15 s pool-wait arm; CI's Node 20 and Node 22 legs including the coverage gate and `e2e:pro`.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (stage3's dev port) or `47787` (Tuesday's dashboard)**, or any port another seat holds. Take every
   port from the kernel and bind `127.0.0.1` wherever YOUR harness or proxy listens. **Never start the portal's own entry point** (it binds
   `0.0.0.0` in `main()`); use the real `createApp()` inside your harness only.
2. **Postgres = the local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all** (the single
   exception is §N.7 if, and only if, the NODE20-LEG line reads DOCKER-PULL-NEVER). Create `vsp_qa_g9_<epoch>` for app runs and
   `vsp_qa_g9_<epoch>_test` as `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs; the name MUST end in `_test`). **Never** `salesportal`,
   `salesportal_test` (the builder's), any `vsp_qa_g1_*` … `vsp_qa_g8_*`, or the builder's `vsp_bf1_*`. `server/db.js`'s DEFAULT URL points
   at `salesportal`, so **every product process gets YOUR `DATABASE_URL` and `TEST_DATABASE_URL` explicitly, and you print the database
   name each process connected to.** Local defaults from `server/db.js` / `scripts/ensure-test-db.js` for credentials only; never anything
   from `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the runtime legs are **NOT RUN, blocker named**. Leave your
   databases in place and list their names (no DROP). **Serialise or salt creation.** Your S2/S3 direct sessions and locks touch ONLY your
   own databases; release every lock in a `finally` and prove `pg_locks` is clean for your databases at the end.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test` or
   `development`, never `production`; PORT; a fresh random SESSION_SECRET / unlock word / `COORDINATOR_SECRET` you generate; DATABASE_URL /
   TEST_DATABASE_URL = yours; DB_QUERY_TIMEOUT_MS / DB_CONNECT_TIMEOUT_MS only where an arm sets them, and say so; `NTFY_SERVER=http://ntfy.invalid`;
   dummy provider values; `npm_config_update_notifier=false`; `npm_config_offline=true`). **NEVER set in a product process:**
   `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`, any real `ACS_*` / `MAIL_SENDER`, `AZURE_BACKUP_CONN_STR`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product process's
   env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh**: set `NTFY_SERVER` before any portal module is
   required and stub `fetch` to throw on any other URL (gate 7's `qa-io1-preload-fetchguard.cjs`). The reminder dispatcher and the backup
   notifier run ONLY against recorders you wrote.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied from gate 7's evidence):
   `basename(argv[0]) == node` AND an app entry point ANYWHERE in the remaining argv, from the kernel; **"ours" = the ancestor chain CONTAINS
   your claude pid.** **Negative controls, same run, must classify FOREIGN:** at drafting (09:01 AEST) the live claudes were Tuesday
   `47349` (pane `%0`), the Vision builder `67576` (pane `%20`, cwd `Vision_Sales_Portal`), NexusAI `20317` (`%22`), `62649` (`%19`) and
   `9959` (`%21`), two other QA gates `36118` (`%23`) and `40285` (`%24`), and `84139` (not in tmux, cwd `/Users/kamil`). **Re-read the seat
   list at start**; say which have exited. Never count by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. **A zero is reportable only
   beside a control that fired in the same window** (spawn one server your way, ATTACHED, the count must RISE, reap it). **Other gates are
   live on this box: record the 1-minute load beside every timing number** (it was 9.18 at 09:01 with `hw.ncpu` 8).
5. **THE DEADLINE RULE:** every step has a written DEADLINE and a client timeout on every request (no `timeout` binary here — build
   deadlines into your runner); a step past its deadline is ABORTED and reported (a hung product request IS a finding, and at `eaf024a` it
   is the expected positive control). Deadlines: boot 60 s; DB connect 15 s; any request at the SHRUNK bound 20 s; **any request at the
   SHIPPED bounds 120 s** (worst predicted path: 15 s wait + 30 s query + 30 s queued ROLLBACK); the pool-wait burst arm 180 s; the S3 lock
   arm 180 s; one `test:db` file 180 s; a whole `test:db` run 420 s. **Nothing above 420 s.** State each shipped-bound exception in the
   report wherever you use it. **Every server, proxy, direct session, lock, child and container you start is released in a `finally`.**
   **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and
   reported.**

**Reap everything you start.** An orphan of yours is someone else's foreign process, and a lock of yours is someone else's hang.

### Drivable surface — LOCAL ONLY. **NEVER the live portal.**
- **NEVER the live** portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the
  live site, its Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault). **No request, no DB connection, not even a GET
  or a health probe. No `az` of any kind — no reads, no writes, no app-setting change, no deploy.** Never QuickQuote's live resources
  (`hpas-quickquote`, `hpas-quickquote-rg`). **Never ntfy.sh**, never Azure Blob Storage, never `api.agentmail.to` from a product process,
  never the Feedback_System coordinator, never the npm registry (`npm audit` included). **Never open a production dump or any file under
  `Vision_Sales_Portal/4_Credentials/`.**

### HELD
- No merge, no deploy, no registry, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker` (except §N.7 under DOCKER-PULL-NEVER), no `npm install`, no `npm ci` without `--offline --ignore-scripts`,
  no `npm audit`, and no `npx` of anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY
  directories.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g9/>`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never touch `work/` or `work-g2/` … `work-g8/`.**
  Dependencies: **`npm ci --offline --ignore-scripts`** at the tree root and nothing else; a cache miss FAILS rather than fetches (then NOT
  RUN, missing tarballs named). Prove `node_modules/.package-lock.json` against `git show <sha>:package-lock.json` **entry by entry**, with
  `lockcmp.py` AND `lockwalk.py` (gate 7: portal 247/247 at the old lockfile; this lockfile has 248 `packages` entries including the root).
  **Never npm audit.** In the portal repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base,
  archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc.** `git merge-tree --write-tree` only as
  `GIT_OBJECT_DIRECTORY=<your own mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree
  --name-only <a> <b>`, from the gate's OWN object dir, or SKIP it and say so.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its
  own. A control derived from the run it validates is not a control.
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the portal repo**, none inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), inside the builder's scratchpad, or inside gate 1-8's report folders or trees.
  The gate fixes nothing; describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead. Every proxy, preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65/report.md`
(sections and `evidence/` beside it).

**QUESTIONS:** your routing name is **`QA/Vision-gate9`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate9] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — VSP-65` and then ` @ 2adfc4a: GO` or ` @ 2adfc4a: NO-GO`.
Lead the body with one sentence: does a half-open Postgres connection now end every signed-in request within the bound, on YOUR proxy
as well as the builder's, and does any legitimate shape now 500 where main served it?
You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **VSP65 (pool query/connect timeout): GO / NO-GO**, naming the pinned sha `2adfc4a` and the branch
  `fix/vsp-65-pool-query-timeout-2026-09-27`. Report on each of: the ticket cell and the read cell on YOUR proxy (S1) and at the shipped
  bound; main hanging in the same shapes (positive control); discard-on-release for all six callers (table); every S-shape; every
  behaviour change ruled (the READY's four plus §N.4(e)-(j)); the red-proofs; the suites as sets vs `eaf024a`; the coverage step; the
  Node 20 leg per the NODE20-LEG line.
- The verbatim strings an operator needs: the `DbTimeoutError` log line for `DB_QUERY_TIMEOUT` and for `DB_CONNECT_TIMEOUT` at the
  shipped values, the boot refusal message for a bad override, and pg's three source strings with file:line.
- One paragraph on the queue quoting §12's merge-tree result, or saying you skipped it.
- **Rule 2: what you did NOT test is first-class output.** Write a NOT TESTED section that covers at least **CI (UNMEASURED: gh not
  authed)**, **a real stalled Azure Postgres / TLS / a real failover**, **Node 22**, **Node 20** if NOT-RUN, **the container image** the App
  Service runs, **`e2e:pro` / `e2e:api` / `e2e:feedback`**, and **production-scale data** for the headroom figure. **Every action
  recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.** Each of §N items 1-8 carries one.
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: portal main `eaf024a3edb7…`, `fix/vsp-65-pool-query-timeout-2026-09-27` `2adfc4aabee2…` | `git -C <portal> ls-remote origin` +
  `cat-file -t` (commit) | read 2026-09-27 08:58:13 AEST
- chain: `2adfc4a` ← `7195df7` ← `67365ec` ← main `eaf024a` (merge, parents `f95f625` + `15cd733`); 3 ahead, 0 behind; merge-base `eaf024a` |
  `git log --format='%H %P'`, `rev-list --left-right --count`, `merge-base` | read 08:58
- file set (4), `db.js` diff, the unchanged blobs (`package.json` d3b76fb, lockfile 9d426df, `test.yml` 0cb2d05, `index.js` 711dce0,
  `errors.js` c0c4b0e), lockfile versions, cell counts | `git diff`, `git rev-parse`, `git show`, python over `git show` output, under `bash` |
  read 08:58-09:0x
- the six `pool.connect()` callers and their release/catch lines; the session store wiring; `initDb` at boot; `dbBackup.js` TABLES_TO_BACKUP
  (10) vs schema.sql (18 `CREATE TABLE`); the admin backup-db route | `git grep` over the named server/ and scripts/ files at `2adfc4a`,
  `git show` | read 09:0x
- the builder's proxy (`net.createServer`, default `allowHalfOpen`, `app.on('close', () => db.destroy())`) | `git show 2adfc4a:test/db/pool-timeout.test.js` | read 09:0x
- CI shape (Node 20/22 matrix, coverage gate on 22, `e2e:pro`, Postgres 16 on 5433) | `git show 2adfc4a:.github/workflows/test.yml` | read 09:0x
- `git log --all -S` for the three option names | portal repo | read 09:0x
- gate 7's arm (e) figures (`STILL-OPEN-45000ms after 45001 ms`; read path 45,003 ms) and its NOT TESTED | `…/gate7/report.md:30-40,168-178,222-230,296-304`, `evidence/io1/armE-*.txt` | read 09:0x
- C-01..C-06, none on VSP-65 | Vision CLARIFICATIONS.md (2026-09-25 15:19) | read 09:0x
- VSP-65 history (filed 2026-09-23 as arm (e)'s unfaulted half; READY 2026-09-27) | `Vision_Sales_Portal/5_Project_History/history.md:1722,1832` | read 09:0x
- CI unreadable (project gh not authed) | `briefs/2026-09-27_vision-status-bcr3p2-ci-purge-mail.txt` item 3 | read 09:0x
- no Node 20 on the box | `which -a node` (v26.8.1), Homebrew Cellar/cache, nvm/volta/fnm dirs | read 09:0x
- `:5433` not listening; Docker Desktop running | `lsof -nP -iTCP:5433`, `lsof -iTCP -sTCP:LISTEN`, `pgrep` | read 09:01
- seats: `tmux list-panes -a`, `ps`, `lsof -d cwd` for each claude; load 9.18; `hw.ncpu` 8 | read 09:01
- builder claims | the READY mail (whole) and the three commit messages; BACKLOG at `2adfc4a`
