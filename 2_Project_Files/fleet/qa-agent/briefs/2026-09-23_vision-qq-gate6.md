# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, BATCHED GATE 6 (portal + QuickQuote), BOTH TARGETS ROUND 2 of 2: IO1R2 = I10-O1 async route errors round 2 (TIER 1, portal), BCR2 = bounded browser.close() round 2 (TIER 2 through-code; the shipped `lib/pdf.js` clauses TIER 1 in rigour, QuickQuote)

**Drafted for Tuesday 2026-09-23 04:38-05:1x AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on Tuesday's gate-5 rulings (daily note 04:02 and 04:37): IO1 goes to ROUND 2 rather than merge-with-ticket, carrying the
IO1-F1 fix **plus the two pre-existing MAJORs gate 5 surfaced (IO1-O2, IO1-O3)**; BC goes to ROUND 2 with gate 5's two probed fix-shapes
plus a child-process exit cell. **The drafter did NOT read the builder's mail bodies** (no AgentMail call in a read-only commission):
every builder claim below comes from commit messages, code comments, the BACKLOG, Tuesday's daily note or gate 5's report, and is a CLAIM.
**BOTH HEADS AND BOTH MAINS WERE READ BY THE DRAFTER FROM `git ls-remote origin` (both repos 2026-09-23 04:37:58 AEST; each `cat-file -t`
= commit). THE LAUNCHER RE-READS EVERY HEAD.** If a head moves before launch, Tuesday edits its row; the launcher parses §PIN, refuses any
placeholder, and re-reads EVERY head by `git ls-remote` immediately before launch, refusing on any mismatch. The verified table is appended
to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-23 04:56
Self-check note: Tuesday read the header, the PIN table, both target sections and the self_check_view output; the drafter's two source corrections are accepted as written (the emailed-PDF identity clause is set against BCR2's base 3bfbfa2 with vs-main d4426f8 as a control that must show exactly A9's delta; gate 5's 'IO1 x S-1 = BACKLOG only' is stale — S-1 89af8ba sits on the pre-I10 base and deletes lastResortHandler, overlapping IO1R2 in four files, which is now a merge-order fact for Kam's S-1 card). Not re-read line by line end to end at ~75% ctx — stated.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build any of these changes and you owe no builder anything. **Every line below that reports what a builder says is a
CLAIM, never evidence.**

**ONE batched gate, TWO targets, TWO repos, ONE session** (Kam's standing rule of 2026-09-18: batch gates, never pay for the same setup
twice). **Give a SEPARATE verdict for each: IO1R2 and BCR2 — each GO / NO-GO, each naming its pinned sha.**

**⚠ Letter collision:** this gate's TARGET letters are NOT the builder's item names. **IO1R2 = round 2 of gate 5's target IO1, which is
gate 4's finding I10-O1** (NOT gate 4's target I10, which is GO and on portal main). **BCR2 = round 2 of gate 5's target BC**, the bounded
`browser.close()` change. Always write both (e.g. "IO1R2 (I10-O1 round 2)", "BCR2 (bounded close round 2)").

Tiers:
- **IO1R2 (I10-O1 round 2, portal async route errors) is TIER 1**: it changes how EVERY request of the live portal's code is dispatched
  (round 1's `Layer.prototype.handle_request` patch is carried unchanged), AND it now edits `server/errors.js`, the module every route's
  error path runs through, `server/db.js`, and two live route files.
- **BCR2 (bounded browser.close() round 2) is TIER 2, through-code — EXCEPT that it touches the shipped module `stage3/lib/pdf.js`**
  (`closeBrowser()`): the parts of the gate that prove production is untouched are **TIER 1 in rigour**.

**BOTH TARGETS ARE ROUND 2 of 2. THE CAP APPLIES TO EACH SEPARATELY.** Kam's cap rule, recorded verbatim as **C-62** in the NexusAI
clarifications (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:573`), verbatim:
*"A Major at round 2 of 2 is ticketed, not sent to Kam. Only a third round on the same class needs his word."*
So **if you grade either target NO-GO, say plainly,
part by part, what CLOSED and would ship and what is TICKETED** — and say that a third round on that class would need Kam.

**NOT IN THIS GATE:** portal **S-1** (`fix/feedback-report-auth-2026-09-22` @ `89af8ba`) is GO from gate 2 and waits on Kam's card —
**but read §12: at IO1R2 it now overlaps three files and is on a pre-I10 base, so its merge order matters.** N (A-6), FU, I9, Q5, **A9** and
**CF5R2** are GO and on QuickQuote main `d4426f8`; **I10** is GO and on portal main `6f197ca`. **P5B (puppeteer 25 + node 22) is GO-tested at
gate 4 and HELD by Kam's decision 14 — NOT on main.** Do not gate any of them; do not re-open them.

## RULED BY KAM, AND SETTLED (Vision `1_Project_Definition/CLARIFICATIONS.md`)
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` — read it whole
(C-01..C-05 at drafting; no new entry since gate 4).
- **No Vision C-entry covers either target here.** Their authority is gate 5's findings and **Tuesday's rulings of 2026-09-23 04:02**:
  (a) IO1 returns for a one-line round 2 — end the response when `headersSent` — **and carries IO1-O2 and IO1-O3, the two pre-existing
  MAJORs gate 5 surfaced, in the same round**; (b) **IO1-F2, IO1-F3 and IO1-P1 are TICKETED, not in scope** — do not fail IO1R2 on any of
  them, but say whether each ticket's BACKLOG entry is accurate; (c) BC returns with gate 5's two probed fix-shapes (destroy the child's
  stdio after the kill; `after(() => closeBrowser())`) **plus a child-process exit cell**.
- **Known and REPORT-ONLY — do not fail on them** (they go in Kam's pack, not in a verdict): **IO1-F2** (a DB fault during sign-in spends
  the login limiter, so 10 faulted tries lock a rep out for 15 minutes after recovery) — **measure it again and quote it, but it is ticketed,
  not a finding against IO1R2 unless round 2 made it WORSE**; **IO1-F3** and **IO1-P1** likewise. **CF5R2-O1** (the site-wide budget no longer
  bounds provider-shaped failures) is already in Kam's pack and is not this gate's business.
- **No product choice in either target is Kam's ruling.** Report each as the BUILDER's choice (or Tuesday's) and say whether it needs Kam:
  IO1R2's `res.destroy(e)` (rather than `res.end()` or `req.socket.destroy()`) for a faulted stream; its `pool.on('error')` that logs and
  carries on; BCR2's `Number.isFinite` coercion of `ms` and the stdio-destroy loop.
- **Kam's pending decisions that bound this gate** (`Vision_Sales_Portal/5_Project_History/2026-09-22_kam-decisions-and-publish-pack.md`,
  READ ONLY): decision 14 (P5B) still holds; decision 18 (QuickQuote's production logs) — **never query any production log**.
- The QuickQuote repo's own rules: `Quoting Tool/hpas-quoting-tool/CLAUDE.md` (single offline HTML file; **version discipline**; **always
  verify print as a real PDF**; nothing in the sub-project goes near Azure). Read it. **BCR2 changes no version** (it is `2.32` on its stale
  base while main is now `2.33`) — say whether that is within the rule at merge time.
- Deploys are HELD for Kam. Nothing here merges on your word.

## PRIOR ROUND
- **Gate 5's report is ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate5/`
  (`report.md` + `sections/` + `evidence/`, 398 evidence files). **Read its VERDICTS, FINDINGS INDEX, NOT TESTED, `sections/IO1.md`,
  `sections/BC.md` and `sections/CONVENTIONS.md`.** Gate 4's report is one level back
  (`…/2026-09-22-vision-qq-gate4/`) and is still the source for I10-O1's original measurement and for N-C1.
- **IO1R2 is ROUND 2 of 2.** Round 1 gated `a83140e`: **NO-GO on IO1-F1 (Minor severity, but it met the brief's stated FAIL clause "a
  faulted request that never gets an answer while the process lives")** — `serverError` logged the fault but answered only
  `if (!res.headersSent)` and never ended or destroyed the response, so a rejection AFTER the response had started left the socket OPEN.
  Measured by gate 5's fork on the **real backup route** (`GET /api/admin/backup-db`, `archive.pipe(res)`): 200 + 8,183 zip bytes, then
  never ends; and re-measured independently by the gate 5 lead (`LEAD-io1-hang.log`): `/headers-then-reject` **STILL-OPEN at 12,000 ms,
  twice**, while controls that could have failed behaved (`/ok` ended in 6 ms, `/destroyed` reset in 1 ms, a pre-headers rejection answered
  500 in 2 ms). **Everything else at round 1 PASSED and is re-checked here, not assumed** (see §5.1).
  Round 2 = `a83140e` + ONE commit `992da21` ("fix(IO1 round 2): end a response that faults after it started; import serverError; handle
  idle pool errors").
- **BCR2 is ROUND 2 of 2.** Round 1 gated `aa89010`: **NO-GO on BC-F1 (Major)** — `npm run test:print` still hung to its deadline **8 runs
  of 8** at BC, the same 8/8 as main, because the SIGKILL killed Chrome but never released Chrome's **stdio pipes**: the
  `chrome_crashpad_handler` Chrome spawned (reparented to launchd) held the far end, and the hung process's fd 16 was peered with that
  handler's fd 2; killing that handler made the test exit 2 s later. **And BC-F2 (Minor)** — `after(closeBrowser)` in `test/typed-rates.mjs`
  and `test/fx-provenance.mjs` handed node:test's `TestContext` in as `ms`, so `setTimeout` coerced `NaN` → **1 ms** and **a HEALTHY Chrome
  was SIGKILLed on every ordinary run** (killed at +1 ms; the real close would have returned at 24 / 21 ms), with two `TimeoutNaNWarning`
  lines per `test:print` run. **Every TIER-1 clause about the shipped module PASSED at round 1** (renderer byte-unchanged, 0 production
  calls with a spy that fired, 0 differing pixels, 27/27 kills attributed) — **re-establish them here at the new sha, do not carry them over.**
  Round 2 = `aa89010` + ONE commit `f8dec9c` ("stage3 tests (BC round 2): release Chrome's stdio after the kill; the bound is never NaN").
- **PRIOR WORK — verify every claim above against history and gate 5's evidence, never against this brief:** `git log` / `git show` for
  `a83140e` and `aa89010`; gate 5's `sections/IO1.md` (IO1-F1, IO1-O2, IO1-O3, IO1-F2/F3/P1) and `sections/BC.md` (BC-F1's socket-peer
  root cause, BC-F2's `TestContext` measurement, the fix-shape probe numbers). **If this brief's account of prior work disagrees with the
  record, the record wins — report it as a brief correction.**
- **Gate 5's and gate 4's harnesses are REUSABLE BY COPY.** From `…/2026-09-23-vision-qq-gate5/evidence/`: `qa-run.py` (the `env -i`
  runner), `qa-chrome-egressblock.sh`, `qa-chrome-lock.py` (the gate's OWN fcntl Chrome lock — **never NexusAI's**), `qa-egress-monitor.py`,
  `qa-egress-posctl.mjs`, `qa-netlog-scan.py`, `qa-floorcount.py`, `lockcmp.py`, `lockwalk.py`, `mktree-qq.sh`, `mktree-portal.sh`,
  `qa-mkdb.cjs`, `qa-dbcheck.cjs`, `qa-harness-floorctl.mjs`; **IO1R2:** `qa-harness-io1-edges.cjs` (the real `createApp()` on real Postgres,
  faults by renaming tables), `qa-harness-io1-boot.cjs`, `qa-harness-lead-io1-hang.cjs` (the lead's independent post-headers probe — the one
  that re-measured IO1-F1), `qa-io1-preload-fetchguard.cjs`, `qa-io1-preload-hidelayer.cjs`, `IO1-count-async.py`; **BCR2:**
  `qa-bc-preload.mjs` (the close/kill/NaN-delay logger), `qa-harness-bc-emailed.cjs` (the server route + spies), `qa-harness-bc-concurrent.mjs`,
  `qa-lib-bc-stage3.cjs`, `qa-lib-bc-png.cjs`, `BC-pdfcompare.sh`, `BC-diag2.sh` (the socket-peer attribution that found BC-F1's root cause).
  Gate 5's `sections/CONVENTIONS.md` is the working method. **COPY what you use into this gate's own evidence folder, read it before
  trusting it, and never edit gate 1-5's copies.**
- **Self-findings from gates 2-5 bind you:** (1) quote every path (the project path has a space); (2) **zsh does not word-split
  `set -- $p`, and zsh reads `$s:stage3/…` as a history modifier** — gates 3, 4 and 5 AND both drafters hit it; **run every such loop under
  `bash`**; (3) never detach a control server; (4) the portal test-DB name MUST end in `_test`; (5) npm's update-notifier egresses unless
  disabled; (6) isolate a browser context per case; puppeteer's default PDF is Letter — pass `format: "A4"`; (7) the real renderer calls
  public FX APIs whenever currency ≠ USD — BLOCK and RECORD them (§13.3); (8) a harness leg that asserts the shape it measured is circular
  for a NO-GO — re-measure any NO-GO with an independent probe; (9) **run each browser gate file ALONE and time it** (N-C1); (10) **gate 5:
  parallel `qa-mkdb.cjs` calls collided on the same millisecond name and voided an arm — serialise DB creation or add entropy**; (11)
  **gate 5: a red arm on a file that ALREADY hangs cannot discriminate** — pick a red arm on a file that passes at the pinned head.

## PIN — HEADS (PRE-FILLED BY THE DRAFTER; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
Rules the launcher enforces: every row has a 40-hex head; every target row has a 40-hex base and a commit count and no `@`; head is a
commit in its repo; base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals head NOW; **base is either the same repo's MAIN row head, or — a STALE BASE — an ancestor of the repo's MAIN
row that equals `merge-base(head, MAIN)`** (the row then needs a forward merge at merge time; the launcher prints a NOTE naming it, and
§12 measures it). MAIN rows are re-read by `ls-remote` too. **No row may be OUT in this gate.** **Gated anchors (launcher-checked):**
IO1R2 contains the gated round-1 head `a83140e`; **IO1R2's `server/asyncErrors.js` blob is IDENTICAL to `a83140e`'s** (round 2 does not
touch the patch itself); BCR2 contains the gated round-1 head `aa89010`; IO1R2's base wires I10's `app.use(lastResortHandler);`; BCR2's
base calls `closeBrowser` only from the two test files.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | 6f197ca8e6090cd6b6a8ac6c5969fa772e3767c4 | - | - | IN |
| MAIN-Q | quickquote | main | d4426f899620419819ae755ff0ddba4f2a9843b7 | - | - | IN |
| IO1R2 | portal | fix/portal-async-route-errors-2026-09-23 | 992da21aae9d08596cbd877fa3e95c7e636804d6 | 6f197ca8e6090cd6b6a8ac6c5969fa772e3767c4 | 2 | IN |
| BCR2 | quickquote | fix/qq-bounded-browser-close-2026-09-23 | f8dec9c6b9898e05182a15ee1a0babd591a442c4 | 3bfbfa25c8dae52c2ac16b96d4ddf65ad075fdb6 | 3 | IN |
<!-- PIN-HEADS:END -->

Repos: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`); QuickQuote = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool`
(remote `datasecau/vision_hpas-quickquote`).

**Shape at drafting (READ, 04:38-05:0x AEST):**
- **IO1R2 sits on current portal main.** Portal main has NOT moved since gate 5 (`6f197ca`); the row's two commits are `a83140e` (gate 5's
  gated round-1 head) then `992da21` (round 2). **No forward merge is owed.**
- **BCR2 is a STALE-BASE row.** Its chain is `907f686` → `aa89010` (gate 5's gated round-1 head) → `f8dec9c`, all on QuickQuote `3bfbfa2`,
  **which is no longer main**: main is now `d4426f8` because **CF5R2 (`309e6c7`) and A9 (`5d787d2`) merged after gate 5** (`cfe85d3` =
  merge CF5R2; `562ab94` = A9's forward merge; `d4426f8` = merge A9). `merge-base(f8dec9c, d4426f8) = 3bfbfa2`, so **a forward merge is
  owed at merge time, which you measure with `merge-tree` and PROBE, never resolve** (§12).
- **A GO is a statement about the pinned SHA only.** If a head moves, its verdict expires.

**Commission corrections the drafter made at source (verify each):**
- **(a) THE BIG ONE — BCR2's emailed-PDF identity clause must be measured against its BASE `3bfbfa2`, NOT against main `d4426f8`.** The
  commission this brief was drafted from said "emailed PDF text-identical and 0 differing pixels vs main". **That is wrong at source now
  that A9 is on main.** A9 changed `index.html` (`--logo-ink-inset` + `toolVersion` 2.32 → 2.33), and gate 5 MEASURED that the printed and
  emailed PDFs at A9 differ from `3bfbfa2` in the version line (`pdftotext`) and in one ~10 px footer raster band per page. So
  **BCR2 vs main `d4426f8` would legitimately differ, for A9's reasons, not BC's.** Do it this way: **(i) the identity clause is BCR2
  `f8dec9c` vs its base `3bfbfa2` — text-identical, 0 differing pixels, bytes identical apart from `/CreationDate` and `/ModDate`;
  (ii) then, as an extra control that can fail on its own, BCR2 vs main `d4426f8` must differ in EXACTLY A9's delta (the version line and
  that one footer band) and in nothing else.** Quote both. READ-verified by the drafter: `stage3/lib/pdf.js` is the SAME blob
  (`9be413c8…`) at `3bfbfa2` and at `d4426f8`, so the renderer itself did not move between them.
- **(b) BCR2's `stage3/package.json` `test:print` line and main's now DIVERGE, and they are the ONLY file both sides touched.** Main
  `d4426f8` lists `… phone-layout.mjs email-collector.mjs test/logo-inset.mjs` (A9's gate file); BCR2 lists `… phone-layout.mjs
  email-collector.mjs test/lib-close.test.mjs test/lib-close-shared.test.mjs`. **Expect a CONFLICT on exactly that line and on nothing else**
  (`comm -12` of the two deltas over `3bfbfa2` = `stage3/package.json` alone). The merged line must carry **all seven** files; count the
  cells on the merged head, never trust a green (gate 5's §BC said the same).
- **(c) BCR2 gains TWO new fixture files** under `stage3/test/fixtures/` (`browser-file.mjs`, `hang-close.cjs`) — a real 12-cell browser
  file and a preload that makes `close()` hang. They are the child-process cell's subject. Gate 5's §BC premise "`closeBrowser` is called
  ONLY by `fx-provenance` and `typed-rates`" is **already superseded**: at `f8dec9c` the callers are `lib/pdf.js` itself,
  `test/fx-provenance.mjs`, `test/typed-rates.mjs` and `test/lib-close-shared.test.mjs` — all tests. **Production is still not a caller —
  MEASURE it, do not assume it.**
- **(d) IO1R2 does NOT change `server/asyncErrors.js`** (blob identical to `a83140e`'s), so round 1's `Layer.prototype.handle_request`
  patch is carried verbatim — **but you still re-run its evidence at the NEW sha** (§5.1). It DOES change `server/errors.js`, which is on
  the error path of every route in the app, including S-1's territory.
- **(e) S-1 (`89af8ba`) is on a PRE-I10 base** (`merge-base(89af8ba, 6f197ca) = ef5a9c0`, 3 commits) and its `server/errors.js` **deletes
  `lastResortHandler` and the client-error wording table**, which main HAS. It also edits `server/routes/feedback.js`. So **IO1R2 × S-1 now
  overlaps `BACKLOG.md`, `server/errors.js`, `server/routes/feedback.js` and `server/index.js`** — not "BACKLOG.md only" as gate 5's table
  said for round 1. Measure it in §12 as context; it is Tuesday's merge-order problem, not a finding against IO1R2.

## 1. Targets — READ from the object store at drafting (04:38-05:0x AEST)
Drafting shas = the PIN table. **Neither target changes a lockfile** (portal `package-lock.json` blob `9d426df` at `6f197ca` and
`992da21`, **express 4.22.2**; stage3 `package-lock.json` blob `70ebda7` at `3bfbfa2`, `f8dec9c` AND `d4426f8`); the launcher re-checks
this at the pinned heads. **Every file:line below is at the pinned sha; re-locate by content if anything moved.**
Cell counts READ by the drafter under `bash` (`grep -c '^test('`): portal `server/asyncErrors.test.js` **3 → 4**, `test/db/async-faults.test.js`
**2 → 5** (`a83140e` → `992da21`); QuickQuote `stage3/test/server.test.mjs` 93 at `3bfbfa2`/`aa89010`/`f8dec9c`, 100 at main `d4426f8`
(CF5R2's two new cells plus A9's — CF5R2 and A9 are on main, not in BCR2's tree). **Count them yourself; that grep only sees column-0 `test(`.**

### TARGET IO1R2 — I10-O1 ROUND 2 of 2: a faulted response that has already started is ENDED, the missing `serverError` import is added, and an idle pool error no longer kills the portal (TIER 1), portal
- **Chain over its base `6f197ca` (2 commits):** `a83140e` (gate 5's GATED round-1 head) → `992da21`.
  Files over `6f197ca` (**exactly 9**): `BACKLOG.md`, `server/asyncErrors.js`, `server/asyncErrors.test.js`, `server/db.js`,
  `server/errors.js`, `server/index.js`, `server/routes/admin.js`, `server/routes/feedback.js`, `test/db/async-faults.test.js`.
  **`992da21` alone (7 files, +161/−1):** `BACKLOG.md` (+23), `server/asyncErrors.test.js` (+36), `server/db.js` (+11),
  `server/errors.js` (+9/−1), `server/routes/admin.js` (+1), `server/routes/feedback.js` (+1), `test/db/async-faults.test.js` (+81).
- **The IO1-F1 fix, `server/errors.js` (READ, verbatim):** the old
  `if (!res.headersSent) res.status(500).json({ error: 'Internal error', ref });` becomes
  `if (!res.headersSent) return void res.status(500).json({ error: 'Internal error', ref });`
  followed by a comment and
  **`if (!res.writableEnded) res.destroy(e instanceof Error ? e : new Error(String(e)));`**.
  **This is the whole product change for IO1-F1.** Gate 5's recommended shape was `res.destroy(err)` — the builder took it, and added the
  `!res.writableEnded` guard so a COMPLETED response is not destroyed. **MEASURE both halves.**
- **The IO1-O2 fix (READ):** one line each — `const { serverError } = require('../errors');` — added to `server/routes/feedback.js` (9
  catch sites used it) and `server/routes/admin.js` (`/backup-db`). Round 1 answered 500 + ref there but the line under the ref read
  `ReferenceError: serverError is not defined` instead of the real fault; on main the same path **kills the portal**, including through the
  **UNAUTHENTICATED `GET /api/feedback/summary`**.
- **The IO1-O3 fix, `server/db.js` (READ):** a `pool.on('error', (err) => { console.error('[db] idle client error (the pool will replace
  it):', (err && err.stack) || err); });` with a 7-line comment. Round 1 and main alike **exited** when an idle pooled connection was
  dropped (gate 5 measured it with `pg_terminate_backend`).
- **Cells added at `992da21` (READ, 4 new):**
  `server/asyncErrors.test.js` — `test('IO1-F1: a rejection AFTER the response started closes the connection instead of hanging the client', …)`;
  `test/db/async-faults.test.js` — `test('IO1-O2: a fault in the UNAUTHENTICATED GET /api/feedback/summary logs the real fault, not "serverError is not defined"', …)`,
  `test('IO1-O2 + IO1-F1: the streaming backup route faulted MID-STREAM breaks the connection and logs the real fault', …)`,
  `test('IO1-O3: a dropped IDLE pooled connection does not kill the process', …)`. Two of them assert
  `!/serverError is not defined/.test(logged)`.
- **BACKLOG (READ):** IO1-O2 and IO1-O3 are ticked `[x] FIXED 2026-09-23`; **IO1-F2, IO1-F3 and IO1-P1 are added as OPEN tickets** with
  their fix shapes, "ticketed by Tuesday, not fixed in round 2". **Check each entry against what gate 5 actually measured.**
- **Edges the drafter found by READ (MEASURE each — these are round 2's new risk surface):**
  - **`res.destroy(err)` on a ServerResponse destroys the SOCKET with an error.** Does that emit an `'error'` on the response, the socket
    or the server (`clientError`)? Does it become a NEW unhandled rejection or an uncaught exception — i.e. **did round 2 trade a hang for
    a crash?** Probe with the stub route and with the REAL backup route; watch for `ECONNRESET`, `ERR_STREAM_DESTROYED`, `EPIPE`.
  - **The writer keeps writing.** `archive.pipe(res)` is a live stream: after `res.destroy()`, does `archiver` (or any piped source) throw
    `write after destroy` / `ERR_STREAM_DESTROYED` asynchronously, outside a route layer, where `asyncErrors` cannot help? Grade a crash.
  - **What the CLIENT sees.** Not just "the connection closes": is the partial body a truncated ZIP, and does the browser present it as a
    failed or as a completed download? Quote the exact client-side outcome (curl's exit code / message) — this is operator-visible.
  - **A response that ALREADY ENDED, then a late rejection.** `!res.writableEnded` should skip the destroy. Confirm, and confirm no double
    log, no second response.
  - **Keep-alive.** Every gate-5 request used `Connection: close`. With a keep-alive agent, does destroying the socket for ONE faulted
    request kill an unrelated in-flight request on the same connection? Measure at least once.
  - **`pool.on('error')` and the in-flight query.** When an idle client is terminated, the handler logs — but what happens to a query that
    was ISSUED on a client that dies mid-flight? Does it reject into its route (500 + ref) or vanish? And does the session store
    (`connect-pg-simple`, which the portal hands its OWN pool) still work after a terminate, or does the next sign-in fail?
  - **Does `pool.on('error')` mask a real outage?** With Postgres stopped entirely, does the portal now log forever instead of failing
    loudly? Compare boot-time behaviour on main and at IO1R2.
  - **Double `next(err)`, 4-arg error handlers, a rejection mid-stream** — re-probe all of gate 5's §Q3 edge table at the new sha, because
    `serverError` changed underneath every one of them.
- **What it still does NOT cover (READ, re-state with severities):** async code OUTSIDE a route layer (`setTimeout`/cron callbacks, the
  reminder dispatcher, `initDb`/seed at boot) and an async 4-ARG error handler (`handle_error` is unpatched; gate 5 found none exists).
  **IO1-O3 removes one of those sites; list what remains.**

### TARGET BCR2 — bounded browser.close() ROUND 2 of 2: the kill now releases Chrome's stdio, and the bound can never be NaN (TIER 2 through-code; the `lib/pdf.js` clauses TIER 1 in rigour), QuickQuote
- **Chain over its base `3bfbfa2` (3 commits):** `907f686` → `aa89010` (gate 5's GATED round-1 head) → `f8dec9c`.
  Files over `3bfbfa2` (**exactly 13**): `stage3/lib/pdf.js`, `stage3/package.json`, `stage3/test/email-collector.mjs`,
  `stage3/test/fixtures/browser-file.mjs` (A), `stage3/test/fixtures/hang-close.cjs` (A), `stage3/test/fx-provenance.mjs`,
  `stage3/test/lib-close-shared.test.mjs` (A), `stage3/test/lib-close.mjs` (A), `stage3/test/lib-close.test.mjs` (A),
  `stage3/test/phone-layout.mjs`, `stage3/test/print-fit.mjs`, `stage3/test/typed-rates.mjs`, `stage3/test/xlsx-parity.mjs`.
  **`f8dec9c` alone (7 files, +99/−5):** `stage3/lib/pdf.js` (+9/−1), the two new fixtures, `stage3/test/fx-provenance.mjs` (1 line),
  `stage3/test/lib-close.mjs` (+14/−2), `stage3/test/lib-close.test.mjs` (+42), `stage3/test/typed-rates.mjs` (1 line).
  **No `BACKLOG.md` entry in BCR2's delta at all — say whether that is a gap** (IO1R2 carries one; QuickQuote's BACKLOG lives at the repo root).
- **The BC-F1 fix (READ, in BOTH `stage3/lib/pdf.js` `closeBrowser` and `stage3/test/lib-close.mjs` `closeBounded`), verbatim:**
  `if (child) for (const s of child.stdio || []) { try { s && s.destroy && s.destroy(); } catch { /* already gone */ } }`
  placed **after** the SIGKILL and **before** the bounded `disconnect()`. This is exactly gate 5's probed fix-shape.
- **The BC-F2 fix (READ):** in both modules,
  `const limit = Number.isFinite(Number(ms)) && Number(ms) > 0 ? Number(ms) : 5000;` and every use of `ms` in the race and in the log line
  becomes `limit`; **and** the two call sites become `after(() => closeBrowser());` (was `after(closeBrowser);`) in
  `stage3/test/typed-rates.mjs` and `stage3/test/fx-provenance.mjs`. **Belt AND braces — measure BOTH independently:** the call-site fix
  alone, and the coercion alone (mutate one, keep the other).
  **Note the asymmetry to check:** `Number.isFinite(Number(ms)) && Number(ms) > 0` also silently rewrites a deliberate `0` or a negative
  bound to 5000. Is any caller relying on a small bound? (`test/fixtures/browser-file.mjs` passes `QA_CLOSE_MS`, default 5000.)
- **The BC-F1 regression cell (READ), exactly what gate 5 asked for:** `test/lib-close.test.mjs` gains
  `test("BC-F1 (child process): a whole test FILE whose close() never returns still exits on its own", …)` — it `spawn`s
  `node --test test/fixtures/browser-file.mjs` with `NODE_OPTIONS=--require …/test/fixtures/hang-close.cjs` and `QA_CLOSE_MS=1000`, strips
  `NODE_TEST*` from the child env, and asserts exit code 0, `/pass 12/`, `/killed the test's own Chrome/` and `took < 45000`, with a 60 s
  SIGKILL escape. **Plus** `test("BC-F2: a bound that is not a number (node:test hands after() its TestContext) does not kill a healthy
  Chrome", …)` which calls `closeBounded(b, {})` and asserts `closed === "cleanly"`. **Both cells are the gate's business: prove each one
  is RED at round 1 `aa89010` and on the base, and that neither can pass for the wrong reason** (e.g. the child exiting because Chrome
  never launched; the `pass 12` assertion is the guard — check it holds).
- **The shipped-module premise (READ at `f8dec9c`):** `stage3/lib/pdf.js` exports `{ renderQuotePdf, closeBrowser }`; the only production
  importer is the stage3 server's entry block (`renderQuotePdf` only). `closeBrowser` is referenced by `lib/pdf.js` itself and by
  `test/fx-provenance.mjs`, `test/typed-rates.mjs`, `test/lib-close-shared.test.mjs` — all tests. The launcher checks this at the pinned head.
- **What the gate must establish (TIER 1 rigour, Tuesday's ruling carried from gate 5):** (1) `renderQuotePdf`, `browser()`, the
  `puppeteer.launch` options, `svcInject()` and `module.exports` are **BYTE-UNCHANGED** from the base, and **the whole file minus the
  `closeBrowser` comment+function hashes identically** (gate 5's strong row — reproduce it at `f8dec9c`); (2) **production never calls
  `closeBrowser`** (READ every import of `lib/pdf.js` in stage3, and MEASURE: the server under your harness renders and emails a PDF with a
  spy on the export that must record **0 calls**, with the spy proven able to fire in the same run); (3) the **EMAILED PDF** identity —
  **vs the BASE `3bfbfa2`** (see correction (a)), default USD and heavy AUD, a fixed qnum, renderer egress blocked: text-identical and
  **0 differing pixels** apart from the creation-timestamp bytes, with the comparator's planted-difference control firing in the same run;
  then vs main `d4426f8` expecting exactly A9's delta and nothing more; (4) the forced-hang arms still exit and kill only the test's OWN
  browser process (pid ancestry anchored on your claude pid); (5) **a healthy close is NOT killed** — the clause BC-F2 broke.

### All targets
- **No worktree is pinned. Build your own trees INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store:**
  `git -C <repo> archive <pinned sha> | tar -x -C <a fresh mktemp -d under your project>`. **Never `git worktree add`, `checkout`,
  `switch`, `fetch`, `pull`, `stash`, `reset`, `restore`, `clean`, `gc`, `tag` or commit against either repo, and never work inside either
  checkout.** Both checkouts are the LIVE builder's working trees: pin by sha, read origin by `ls-remote`.
- **Dependencies, without the network:** in YOUR archived tree, **`npm ci --offline --ignore-scripts`** (in `stage3/` for QuickQuote, at
  the root for the portal). `--offline` forbids the network by construction: a cache miss FAILS rather than fetches — that suite is then
  **NOT RUN, blocker named** (name the missing tarballs). Never `npm install`, never `npm ci` without `--offline`, never `npx` a package
  that is not already in the tree, **never `npm audit`** (a registry call). After it, prove `node_modules/.package-lock.json` matches
  `git show <sha>:<lockfile>` **entry by entry** and quote the count (gate 5: stage3 282/282, portal 247/247), by `lockcmp.py` AND the
  on-disk `lockwalk.py`. Chrome: `PUPPETEER_EXECUTABLE_PATH` = YOUR copy of the egress-block wrapper (§13.3).
- **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a clean
  arm; never touch gate 1-5's trees (`work/`, `work-g2/` … `work-g5/`). **Use `work-g6/`.**
- **`git merge-tree --write-tree` writes objects** — only ever as `GIT_OBJECT_DIRECTORY=<your own mktemp -d>
  GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree --name-only <a> <b>`, **from the gate's OWN
  object directories**. The same two variables let you `git archive` a merge RESULT. If you cannot do it that way, SKIP it and say so.
- **A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES:** `node --check` on every mutated `.js`/`.mjs`/`.cjs` before its arm, exit code
  quoted. A red from a mutant that does not parse or load is a VOID arm, never a red.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every positive or negative control is a separate measurement that could have come out
  the other way on its own (a crash probe's control crashes on main; a comparator's control finds a planted difference). A control derived
  from the same run it validates is not a control.
- **NOT on main. Nothing merges on your word or a builder's.** Merges are Tuesday's GO on a pinned head.

## 2. Why these tiers, and who is waiting
- **IO1R2** decides whether the portal's crash-to-500 change can ship at all. Round 1 turned a process crash into a 500 everywhere except
  a response that had already started, where it became a hang; round 2 turns that into a broken connection — **and must not turn it into a
  new crash.** It also closes two pre-existing MAJORs that are live in production's code today, one of them reachable **unauthenticated**.
- **BCR2** de-flakes `test:print` (N-C1, a live defect on main measured 8/8 at gate 5) and touches a shipped module.
- 🔴 **Queue:** deploys HELD for Kam. Portal main still carries I10-O1's crash (IO1 did not merge at gate 5) and both pre-existing MAJORs.
  QuickQuote main `d4426f8` carries A9 + CF5R2 and still hangs `test:print`. **A second NO-GO on either target ships what closed and
  tickets the rest (C-62); a third round on that class needs Kam.**

## 2a. LEGITIMATE SHAPES — CHECKERS in this gate (template §2a)
Measure every row. **A row whose expected verdict and clause disagree is a finding against this brief — say so.** A legitimate shape
refused is a **Major**.

| shape — its ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| IO1R2: an admin downloads the backup zip and the DB fails **mid-stream** | the download ENDS (truncated/aborted) within a second or two; the process lives; the log line names the REAL fault, not a `ReferenceError` | `serverError`'s `res.destroy` + the new `serverError` import | builder (2 cells) — **measure; a response left open, OR a new crash, is a finding** |
| IO1R2: a Postgres blip during `GET /api/quotes` (signed-in rep) | 500 `{ error: 'Internal error', ref }`; the portal keeps serving; next request 200 | `serverError` via `next(err)`, pre-headers branch unchanged | gate 5 (GO) — **re-measure at the new sha** |
| IO1R2: a Postgres blip during the unauthenticated `POST /api/auth/login` | 500 + ref, no enumeration, then the same user signs in | same | gate 5 — re-measure |
| IO1R2: **anyone on the internet** hits `GET /api/feedback/summary` while the DB is faulted | 500 + ref; the portal LIVES; the ref line names the real fault | the IO1-O2 import | builder (cell) — **measure, and measure it red on main (it crashes there)** |
| IO1R2: Postgres restarts / an admin terminates an idle backend while the portal is idle | one `[db] idle client error` line; the portal lives; the next query gets a fresh connection; the next sign-in still works | `pool.on('error')` | builder (cell) — **measure, red on main and at round 1** |
| IO1R2: a rep retries the right password 10× during a DB outage | 10 × 500, then after recovery **429 for 15 min** | the login limiters counting a 5xx | gate 5 IO1-F2 — **TICKETED: report and quote, do NOT fail on it** |
| BCR2: a developer runs `npm run test:print` on a machine with the installed Google Chrome | the run completes and **exits on its own**, every cell green | the stdio destroy after the kill | builder — **measure N≥3 at BCR2, with main `d4426f8` as the control (it should still hang)** |
| BCR2: an ordinary `test:print` run, nothing hanging | **0 kills of a healthy Chrome, 0 `TimeoutNaNWarning` lines** | `after(() => closeBrowser())` + the `limit` coercion | builder — measure; round 1 killed a healthy Chrome twice per run |
| BCR2: a real Chrome whose `close()` genuinely hangs | each test file exits within the bound + margin, killing only its own browser | the 5 s bound | gate 5 (7/8 passed; `phone-layout` did not) — **measure all 8 files** |
| BCR2: production renders and emails a quote PDF | `closeBrowser` is never called; the PDF is byte-identical to the base's | production imports `renderQuotePdf` only | gate 5 — re-measure at the new sha |

## 5. TARGET IO1R2 — I10-O1 ROUND 2 of 2 (TIER 1)
**The portal's `createApp()` in YOUR harness on LOCAL Postgres (§13.2), `env -i`; never the portal's own entry point (it binds all
interfaces).** Gate 5's `qa-harness-io1-edges.cjs`, `qa-harness-io1-boot.cjs`, `qa-harness-lead-io1-hang.cjs` and
`qa-io1-preload-fetchguard.cjs` by COPY, read before trusted.
**FAIL condition (state it before the runs):** IO1-F1 still open (a faulted request that never gets an answer while the process lives);
**a NEW way to kill the process that round 1 did not have** (including anything thrown by the destroy itself or by a writer writing into a
destroyed response); any async route fault that still kills the process; a double response / `ERR_HTTP_HEADERS_SENT` crash; a fault logged
twice or not at all; a ref line that still says `serverError is not defined`; an idle-connection drop that still exits; `/api/health` not
200 during or after a fault; the unauthenticated login leaking anything beyond 500 + ref; any change to a NON-faulted request.
1. **Re-establish round 1's closed parts at the NEW sha (MEASURED, positive control first) — do NOT carry them over.**
   (a) Gate 5's crash probe on main `6f197ca` → the process EXITS on `GET /api/quotes` under a DB fault (quote the exit); on `992da21` →
   500 + 8-hex ref, process alive, `/api/health` 200, next request 200 after restore.
   (b) **The 26 listed handlers** under a DB fault: status, body shape, exactly one log line under the ref, no `unhandledRejection`,
   process alive, health 200. (c) **The builder's red-on-main claim** for `async-faults.test.js` on `6f197ca` (gate 5: 20 route cells +
   login fail and the file never exits — bound it with your deadline). (d) **Line by line vs express 4.22.2's own
   `Layer.prototype.handle_request`** from YOUR installed `node_modules`, naming every difference (gate 5 found: keeps the return value,
   adds the `.then` branch, `const` vs `var`; identical arity rule and sync try/catch). (e) **Refuse-to-boot** on a non-Express-4 Layer and
   on a hidden module; install twice → one patch. (f) **No login enumeration**: known user / unknown user / wrong password all the same
   500 + ref shape under a fault. (g) **Non-faulted requests unchanged** vs main (gate 5: 18/18).
2. **IO1-F1 closed (MEASURED, with an INDEPENDENT probe, not the builder's cell).** Copy `qa-harness-lead-io1-hang.cjs` — the probe that
   measured STILL-OPEN at 12,000 ms at round 1 — and run it **on `a83140e` first as the positive control** (it must reproduce the hang)
   and then on `992da21`. Report, for each: time to connection close, what the client received, the exit shape (`curl` rc / Node's error
   code), the log lines, and the process state afterwards. **Then the REAL streaming backup route** (`GET /api/admin/backup-db`,
   `archive.pipe(res)`) with a fault injected after `setHeader`, **on YOUR DB only**: the download must end, and you must say **whether the
   partial ZIP is recognisable as truncated**. Keep gate 5's controls that can fail on their own: `/ok` completes, `/destroyed` resets, a
   pre-headers rejection answers 500.
3. **Did round 2 trade the hang for a crash? (MEASURED — this is the new risk.)** For each of: the destroy on a socket that a stream is
   still writing into; a response that already ENDED then rejects; a keep-alive connection carrying a second in-flight request; a
   `next(err)` followed by a rejection; a rejection after `next()`; an async 4-arg error handler that rejects; a sync throw; a resolving
   handler; a non-promise thenable — record client outcome within 30 s, every log line (including anything Express's finalhandler prints
   bare), `unhandledRejection` / `uncaughtException` counts, and process state. **Any new uncaught exception or unhandled rejection
   introduced by `res.destroy` is a Major.**
4. **IO1-O2 closed (MEASURED, red on main in the same session).** A DB fault on the **UNAUTHENTICATED** `GET /api/feedback/summary` and on
   `/api/feedback/report`: on main `6f197ca` → the process exits; at round 1 `a83140e` → 500 + ref whose line says `ReferenceError:
   serverError is not defined`; at `992da21` → 500 + ref whose line names the REAL fault. Quote all three. Then all 9 feedback catch sites
   plus the admin backup route. **Confirm the two new cells are RED at `a83140e` for the gate's reason** (the assertion that fails is the
   `!/serverError is not defined/` one) — a fix with no reddening cell is a finding.
5. **IO1-O3 closed (MEASURED, red on main AND at round 1).** `pg_terminate_backend` on YOUR database's idle backends: main and `a83140e`
   exit (gate 5 measured `throw er; // Unhandled 'error' event`); `992da21` logs `[db] idle client error (the pool will replace it):` and
   lives, and the next query reconnects. Then the harder shapes: a client that dies **mid-query**; the session store after a terminate
   (does sign-in still work?); Postgres stopped entirely (does the handler now hide a real outage, and what does boot do?).
6. **The ticketed items — REPORT, DO NOT FAIL ON (MEASURED where cheap).** IO1-F2: reproduce the 10-faulted-sign-ins lockout and quote the
   429 body; say whether round 2 changed it at all. IO1-F3: does the `|| new Error('async handler rejected without a reason')` fallback
   still have no reddening cell? IO1-P1: what does an operator see when the layer module is absent? **For each, check the BACKLOG entry
   `992da21` added against what you measure, and report any inaccuracy as a brief/BACKLOG correction.**
7. **Async sites outside a route layer (READ, then MEASURE one):** re-list them now that `pool.on('error')` exists; inject one rejection →
   does the process still die?
8. **Red-proofs (parse-checked, `node --check` rc quoted; fresh tree per arm):** (a) remove the `res.destroy` line → IO1-F1's cell and the
   mid-stream backup cell redden; (b) remove the `!res.writableEnded` guard → what breaks (a completed response destroyed)? (c) remove the
   `serverError` import from `feedback.js` → the IO1-O2 cell reddens; from `admin.js` → the backup cell reddens; (d) remove
   `pool.on('error')` → the IO1-O3 cell reddens; (e) remove the `require('./asyncErrors')` wiring → gate 5 found `npm test` stays green and
   only `test:db` reddens — confirm that still holds and say what it means for CI. **A fix with no reddening cell is a finding.**
9. **Suites at `992da21`:** `npm test` (gate 5 baseline 87/87 at round 1 — expect more now), `npm run test:db` on a **FRESHLY CREATED**
   `vsp_qa_g6_<epoch>_test` database (prove it fresh first: zero user tables), which runs `async-faults.test.js` and gate 4's 413 cell.
   **Serialise or salt your database creation** (gate 5 void: four parallel `qa-mkdb.cjs` calls collided on the same millisecond name).

## BC. TARGET BCR2 — bounded browser.close() ROUND 2 of 2 (TIER 2 through-code; the `lib/pdf.js` clauses TIER 1 in rigour)
**FAIL condition (state it before the runs):** `test:print` still not completing and exiting on its own; a healthy close killed early; a
test file that does not exit on a forced close hang; any byte of `renderQuotePdf` or the browser launch changed; any production path
reaching `closeBrowser`; the emailed PDF differing from its BASE in text or by one pixel (timestamp bytes excepted); a kill that reaches
any process the test did not start.
1. **Scope (READ):** `git diff --stat <base> <BCR2 head>` and `<round-1 head> <BCR2 head>`; every file named. **Extract `renderQuotePdf`,
   `browser()`, `svcInject()`, the `puppeteer.launch` options and `module.exports` at the base and at `f8dec9c` and prove them
   byte-identical (quote the hashes), and hash the WHOLE FILE MINUS the `closeBrowser` comment+function on both sides** — that is the
   strong row. Quote the whole `closeBrowser` diff. `package.json` delta = the `test:print` line only. **Gate 5's own self-finding: its
   first extraction anchored on the signature and stopped inside an `opts = {}` default, "proving" a 46-byte block identical — anchor on
   the body brace and sanity-check the size.**
2. **Production never calls it (READ + MEASURED):** every `require("./lib/pdf")` / `lib/pdf.js` import in stage3 outside `test/`; then your
   harness server signs in through the real OTP flow and emails a PDF with spies on the export, on `CdpBrowser.prototype.close`, on
   `disconnect` and on `ChildProcess.prototype.kill` → **0 calls**, repeated; then call the spied export yourself so the spy is proven able
   to fire in the same run.
3. **Emailed PDF identity (MEASURED) — against the BASE `3bfbfa2`, see correction (a).** Gate 5's `qa-harness-bc-emailed.cjs` +
   `BC-pdfcompare.sh` (copied): base `3bfbfa2` vs BCR2 `f8dec9c`, default USD and heavy AUD, fixed qnum, egress blocked → pages equal,
   `pdftotext` equal, raster **0 differing pixels**, differing bytes only inside `/CreationDate` and `/ModDate`; the comparator's positive
   control (a planted difference) must fire in the same run. **Then the extra control: BCR2 vs main `d4426f8` must differ in EXACTLY A9's
   delta** (the version line in `pdftotext`, one ~10 px footer raster band per page) **and nothing else** — quote the v2.32 and v2.33
   footer lines from real PDFs.
4. **N-C1 — the reason this change exists (MEASURED; the headline result).** Plain `npm run test:print`, no preload, each run ALONE under
   your own exclusive Chrome lock, timed, with a written deadline: **at `f8dec9c`, N ≥ 3 back-to-back runs must COMPLETE and EXIT on their
   own**, every cell green, and you must quote the elapsed time (the builder's probed number at gate 5 was 24-26 s). **Controls that can
   fail independently, in the same session: main `d4426f8` (gate 5 measured 8/8 hangs on `3bfbfa2`; main has moved, so re-measure) and
   round 1 `aa89010`.** Then ≥ 2 runs beside a concurrent Chrome job of yours. **Count the cells on each run and say how many** — A9's
   `logo-inset.mjs` is on main and NOT in BCR2's `test:print` line, so the run sizes differ between trees; do not read a smaller green as
   the same green.
5. **Forced hang (MEASURED), all 8 files.** (a) a stubbed browser whose `close()` never resolves → **each** patched test file exits within
   the bound + margin (round 1: 7 of 8; **`phone-layout.mjs` did not** — that is the file to watch), with main as the control (round 1:
   0 of 6 exited); (b) a real Chrome with its close stalled (`SIGSTOP` on the browser process you started) → same; (c) the kill targets
   only that browser's own pid tree — prove by pid ancestry anchored on YOUR claude pid that no updater or foreign Chrome was signalled,
   and reconcile every kill against the `browserPid` the same process's own `close()` reported (round 1: 27/27 attributed); (d) **a slow
   but healthy close (4.9 s) is NOT killed**; (e) **an ordinary run in OBSERVE mode (no stubbing at all): 0 kills and 0
   `TimeoutNaNWarning` lines** — that is BC-F2 closed, and round 1 failed it.
6. **The child-process cell is the one that could not exist before (MEASURED).** Run `test/lib-close.test.mjs` alone at `f8dec9c`; then
   prove the child-process cell RED at round 1 `aa89010` (copy the cell + fixtures into a round-1 tree — a mutant that must parse,
   `node --check` rc quoted) and say what it asserts that no in-process cell can. Probe it for a false green: make the fixture's Chrome fail
   to launch and confirm the cell fails rather than passing on a fast exit.
7. **Red-proofs (parse-checked, fresh tree per arm):** (a) remove the stdio-destroy loop from `test/lib-close.mjs` → the child-process cell
   and the hang arm redden; (b) remove it from `lib/pdf.js` `closeBrowser` → `lib-close-shared.test.mjs` reddens; (c) revert
   `after(() => closeBrowser())` to `after(closeBrowser)` in ONE file → the BC-F2 cell reddens and the kill returns at +1 ms; (d) remove the
   `limit` coercion but KEEP the call-site fix → what, if anything, reddens (this is the belt-and-braces question); (e) revert the bound in
   one test file → under (5a) that file hangs to your deadline. **Do NOT pick a red arm on a file that already hangs at the pinned head**
   (gate 5's VOID arm). **A fix with no reddening cell is a finding.**
8. **Suites at `f8dec9c`:** stage3 `npm test`, `test:print` (§4), `test:xlsx`, root pricing.
9. **CI / Linux Chromium is the carried gap.** `gh` is NOT authenticated for `datasecau` and **you must not use `gh`**. State plainly in
   your verdict that **BC-F1's root cause (Chrome's crash handler holding the stdio) may be macOS-with-installed-Chrome only**, that
   nothing here measures the container's Chromium, and that CI is the first thing to measure at merge. Say what a Linux run would have to
   show to make the fix unnecessary — and whether the fix could HURT there.

## 12. Across targets — merges and the queue
**The drafter did NOT run `merge-tree` for this gate (its commission forbade it). Every row below is a READ expectation, derived from file
sets and blob identities. Quote `git merge-tree --write-tree --name-only` from YOUR OWN object directory for each pair, or say you skipped
it.** Never hand-resolve.

| pair | drafter's READ expectation |
|---|---|
| IO1R2 `992da21` × portal main `6f197ca` | **CLEAN — IO1R2 sits on main**; the result tree should equal IO1R2's own tree |
| BCR2 `f8dec9c` × QuickQuote main `d4426f8` | **CONFLICT in `stage3/package.json` ONLY** (the `test:print` line: main has A9's `test/logo-inset.mjs`, BCR2 has the two `lib-close` files). `comm -12` of the two deltas over `3bfbfa2` is that one file. Every other BCR2 file should auto-merge |
| IO1R2 × S-1 `89af8ba` (context only, NOT gated) | **CONFLICT in more than `BACKLOG.md`** — gate 5 predicted BACKLOG-only for round 1, and that is now stale. S-1 is on the pre-I10 base `ef5a9c0` (3 commits) and its `server/errors.js` **deletes `lastResortHandler` and the client-error wording table that main has**, while IO1R2 rewrites the adjacent `serverError` lines. Both also touch `server/routes/feedback.js` and `server/index.js`. **Measure it and tell Tuesday plainly: S-1 needs its own forward merge before it can go anywhere near IO1R2.** |
| BCR2 × A9 `5d787d2` / CF5R2 `309e6c7` (context) | both are already IN main `d4426f8`; the row above covers them |

- **A GO is a GO at the pinned sha only.** Name, for each target, the cells to re-run on its merged head — at least: **IO1R2** — `npm test`
  + `test:db` on a fresh `_test` DB + your independent post-headers probe + the IO1-O2 unauthenticated-summary leg + the IO1-O3 terminate
  leg; **BCR2** — `test:print` end to end, timed, N ≥ 3, **asserting the process exits**, on a tree whose `test:print` line carries **all
  seven** files (print-fit, typed-rates, fx-provenance, phone-layout, email-collector, **logo-inset**, and both `lib-close` files), plus the
  forced-hang arms, the child-process cell, the emailed-PDF compare and the `closeBrowser` spy.
- **CI:** `gh` is not authenticated for `datasecau`; every target's CI half is **NOT RUN**, measured at merge. For IO1R2, CI's `test:db` is
  what pins the `asyncErrors` wiring — `npm test` alone stays green with the require removed (gate 5).

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (`session-tools/nexusai-lock.sh`).
1. **The Vision builder seat is LIVE** (claude `1613`, pane `%41`) and owns portal `:4848` and stage3 `:8080`. **Never use 4848 or 8080**,
   nor `47787` (Tuesday's dashboard), nor any port another seat holds. Take every port from the kernel and bind `127.0.0.1` wherever YOUR
   harness listens. Never start the portal's own entry point (it binds `0.0.0.0` in `main()`).
2. **Postgres = the running local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all.** Create
   `vsp_qa_g6_<epoch>` for app runs and `vsp_qa_g6_<epoch>_test` as `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs; the name MUST end in
   `_test`; never `salesportal`, `salesportal_test`, any `vsp_qa_g1_*`, `vsp_qa_g2_*`, `vsp_qa_g3_*`, `vsp_qa_g4_*` or `vsp_qa_g5_*`
   database, or the builder's `vsp_bf1_*`). Local defaults from `server/db.js` / `scripts/ensure-test-db.js` only; never anything from
   `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the portal runtime legs are **NOT RUN, blocker named**. Leave your
   databases in place and list their names (no DROP). **Serialise or salt creation** (gate 5's millisecond-collision void).
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH, HOME = a fresh mktemp dir, TZ, NODE_ENV = `test` or
   `development` — never `production` — PORT, a fresh random SESSION_SECRET / unlock word / `COORDINATOR_SECRET` you generate,
   DATABASE_URL / TEST_DATABASE_URL = yours, PUPPETEER_EXECUTABLE_PATH, `NTFY_SERVER=http://ntfy.invalid`, dummy provider values,
   `npm_config_update_notifier=false`, `npm_config_offline=true`). **NEVER set in a product process:** `AGENTMAIL_API_KEY`,
   `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product process's
   env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh**: set `NTFY_SERVER=http://ntfy.invalid` before any
   portal module is required and stub `fetch` to throw on any other URL.
   **Egress — including Chrome children:** the real QuickQuote renderer's page calls three public **FX** APIs whenever currency ≠ USD.
   **Block it** with YOUR copy of `qa-chrome-egressblock.sh` as `PUPPETEER_EXECUTABLE_PATH` and **prove the block with a positive control**.
   Record outbound connections of EVERY process you start, Chrome children included (`lsof` over the whole process tree, plus the net-log
   scan). **Gate 4's self-finding 4, worse at gate 5 (15 → 67 helpers): GoogleUpdater reparents out of the descendant monitor — record every
   `GoogleUpdater` / `chrome_crashpad_handler` process at start and end (pid, ppid, start time) and say which appeared during the gate.**
   **Gate 5's socket-peer method (`BC-diag2.sh`) is what attributes them — reuse it; it is also BC-F1's own root-cause instrument.**
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (gate 5's `qa-floorcount.py`, COPIED from
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate5/evidence/qa-floorcount.py`):
   `basename(argv[0]) == node` AND an app entry point ANYWHERE in the remaining argv, from the kernel; **"ours" = the ancestor chain
   CONTAINS your claude pid**. **Negative controls, same run, must classify FOREIGN:** the Vision builder's claude `1613` (pane `%41`),
   Tuesday's claude `3434` (pane `%0`), the NexusAI seat's claude `8360` (pane `%44`) and the NexusAI gate-7-r2 QA seat's claude `40615`
   (pane `%50`). Re-read them at start; if one has exited, say so and use the others (gate 5's QA seat `25545` has exited). Never by
   `EADDRINUSE`, a whole-command-line grep, or raw `comm`. **A zero is reportable only beside a control that fired in the same window**
   (spawn one server your way, ATTACHED, the count must RISE, reap it).
5. **THE DEADLINE RULE:** every real-server, browser and database step has a written DEADLINE (boot 60 s, request 30 s, render 60 s, DB
   connect 15 s, exit 20 s) and a client timeout on every request (no `timeout` binary here — build deadlines into your runner); a step past
   its deadline is ABORTED and reported (a hung product request IS a finding). **Every server, browser and child you start is killed in a
   `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is
   aborted and reported.** The shapes that hang here: IO1R2's post-headers probe and `async-faults` on main (it never exits), and every
   BCR2 `test:print` and forced-hang arm.

**Reap every server and every Chrome you start.** An orphan of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (App Service `hpas-quickquote`, resource group `hpas-quickquote-rg`, its ACR `hpasqqacr`, its Table Storage,
  its log workspace `hpas-quickquote-logs` — decision 18: never query it) **or the live portal**
  (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the live site, its Postgres
  `datasec-sales-db.postgres.database.azure.com` and key vault). No request, no DB connection, not even a GET or a health probe. **Never
  ntfy.sh** or any ntfy host. **Never the three FX hosts.** Never the npm registry (`npm audit` included). Never `api.agentmail.to` from a
  product process. Never the Feedback_System coordinator.

### HELD
- No merge, no deploy, no registry, no Partner Center, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npm audit`, no `npx` of anything
  not already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Real sends are OFF.** Every provider is a recorder you wrote.
- **Findings-only:** do not commit, do not move any branch, do not file a ticket, **no writes in either repo**, inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), inside `Feedback_System/`, inside the builder's scratchpad, or inside gate 1-5's
  report folders. The gate fixes nothing.
- **NEVER `rm`** — quarantine; every preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate6/report.md`

**QUESTIONS:** if you must ask, mail `tuesday-agent@agentmail.to` with subject `[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>`
(Context / one Question / Meanwhile / Needed-by) and **proceed on the safest reading**; the ANSWER arrives in `tuesday-agent@` with subject
beginning `[Wednesday -> QA/Vision-gate6] ANSWER` — read it with your verdict key. Record every question, the reading you took and any
answer in the report.
If a response is cut off by a safety check, record it and continue with the next item; this is
authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 6: I10-O1 async route errors round 2 of 2 (tier 1, portal) + bounded browser.close round 2 of 2 (tier 2, QuickQuote), heads as pinned at launch`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the QA project
has none. Use it ONLY in your own verdict/question/answer-read `curl` (with a client timeout, e.g. `-m 30`); it must never enter a product
process's environment (§13.3). Never put the key, or any secret, in a mail or the report.

Verdict format:
- **IO1R2 (I10-O1 round 2)** and **BCR2 (bounded close round 2)** — each **GO / NO-GO**, stated SEPARATELY PER TARGET, each naming its
  pinned sha and branch.
  **For IO1R2:** IO1-F1 closed or not, with the round-1 positive control and your INDEPENDENT probe; IO1-O2 and IO1-O3 each closed or not,
  each red on main; whether round 2 introduced any new way to kill the process; round 1's closed parts each re-confirmed at the new sha;
  and IO1-F2 / IO1-F3 / IO1-P1 measured and quoted as TICKETED, not graded.
  **For BCR2:** `test:print` completing and exiting, N ≥ 3, timed, with main and round 1 as controls; 0 kills of a healthy Chrome and 0
  `TimeoutNaNWarning` lines in observe mode; all 8 forced-hang arms; the child-process cell proven red at round 1; `renderQuotePdf` and the
  launch byte-unchanged; production 0 calls with a firing spy; the emailed PDF 0 differing pixels **vs its base**, plus the vs-main control
  showing exactly A9's delta.
- **ROUND 2 of 2, for each target separately: if NO-GO, list which parts CLOSED and would ship and which are TICKETED**, and say that a
  third round on that class needs Kam (C-62).
- The verbatim strings an operator or Kam's pack needs: IO1R2's client body and log line for a faulted request, the ref line on the
  unauthenticated feedback route, the `[db] idle client error` line, and what a client sees when a faulted download is cut; BCR2's bounded-
  close log line, whether any `TimeoutNaNWarning` remains, and the footer line from a real PDF at BCR2 and at main.
- Then one paragraph on the queue quoting §12's merge-tree results (or that you skipped them), **including the S-1 warning**.
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section — at least: **CI / Linux Chromium**, which is BCR2's
  biggest gap; Node 20 (production's runtime) and Node 22 — every result is this machine's node; real Azure Postgres failover shapes; the
  App Service front end's own idle timeout; real App Service `X-Forwarded-For`; multiple replicas; the container image; every stale-base
  target's forward-merged head (only PROBED)). Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED /
  READ ONLY**. §5 Q1-Q9 and §BC Q1-Q9 must each carry one.
- Report each pinned head, and both mains, as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: portal main `6f197ca8e609…`, `fix/portal-async-route-errors-2026-09-23` `992da21aae9d…`; QQ main `d4426f899620…`,
  `fix/qq-bounded-browser-close-2026-09-23` `f8dec9c6b989…` | `git -C <repo> ls-remote origin` + `cat-file -t` (all = commit) |
  read 2026-09-23 04:37:58 AEST
- chains: `992da21` → `a83140e` → portal main `6f197ca` (2 commits; merge-base with main = `6f197ca`); `f8dec9c` → `aa89010` → `907f686` →
  `3bfbfa2` (3 commits; merge-base with QQ main `d4426f8` = `3bfbfa2` — STALE BASE); QQ main `d4426f8` = merge A9 ← `562ab94` (A9's forward
  merge) ← `cfe85d3` = merge CF5R2 on `3bfbfa2`; S-1 `89af8ba` on `ef5a9c0` (3 commits), merge-base with portal main = `ef5a9c0` |
  `git log --format='%h %p %s'`, `merge-base`, `rev-list` | read 04:38-04:45
- file sets (IO1R2 9 files over main, `992da21` alone 7; BCR2 13 over `3bfbfa2`, `f8dec9c` alone 7); lockfile blobs (portal `9d426df` at
  `6f197ca`/`992da21`, express 4.22.2; stage3 `70ebda7` at `3bfbfa2`/`f8dec9c`/`d4426f8`); `lib/pdf.js` blob `9be413c8…` at BOTH `3bfbfa2`
  and `d4426f8`; `server/asyncErrors.js` blob `9e770e9f…` at BOTH `a83140e` and `992da21`; the `test:print` lines at `d4426f8` and
  `f8dec9c`; `comm -12` of the two deltas over `3bfbfa2` = `stage3/package.json` | `git diff --name-only/--stat`, `git rev-parse <sha>:<path>`,
  `git show`, all under `bash` | read 04:39-04:50
- mechanisms and strings (`errors.js` `res.destroy` + `writableEnded`, `db.js` `pool.on('error')`, the two `serverError` imports, the 4 new
  portal cells, `lib/pdf.js` `limit` + the stdio loop, `after(() => closeBrowser())`, the child-process cell and its two fixtures,
  `closeBrowser` callers at `f8dec9c`) | `git show`, `git diff`, `git grep` | read 04:42-04:55
- the outside-`closeBrowser` identity of `lib/pdf.js` between `3bfbfa2` and `f8dec9c` | gate 5's guard-74 strip function, re-run by the
  drafter on both blobs (result: IDENTICAL) | 04:52
- seats: `%41` → claude `1613` (Vision builder), `%0` → claude `3434` (Tuesday), `%44` → claude `8360` (NexusAI), `%50` → claude `40615`
  (NexusAI gate 7 r2 QA); gate 5's QA `25545` has exited; `:5433` LISTENING | `tmux list-panes -a`, `ps -axo pid,ppid,comm`, `lsof` | read 04:53
- C-62's verbatim text | `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:573` | read 04:56
- builder claims / Tuesday's rulings | Tuesday daily note `0_Brain/daily_tuesday/2026-09-23.md` 04:02 and 04:37 lines; gate 5's
  `report.md`, `sections/IO1.md` and `sections/BC.md`; commit messages (mail bodies NOT read)
