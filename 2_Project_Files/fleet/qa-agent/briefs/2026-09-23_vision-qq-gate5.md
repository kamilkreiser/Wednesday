# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, BATCHED GATE 5 (portal + QuickQuote): A9 = A-9 logo ink inset v2.33 (TIER 2, CUSTOMER-VISIBLE), CF5R2 = CF5 ROUND 2 of 2 (TIER 1), IO1 = I10-O1 async route errors (TIER 1, portal), BC = SLOT for the bounded browser.close() fix (TIER 2 through-code, touches the shipped lib/pdf.js)

**Drafted for Tuesday 2026-09-23 01:36-01:55 AEST by a read-only drafting agent; Tuesday reviews, pins BC, stamps and launches.**
Commissioned on the Vision_Sales_Portal agent's READY mails as Tuesday's daily note records them (A-9 14:31Z; CF5 round 2 15:24Z;
I10-O1 15:33Z) and Tuesday's ruling that the bounded `browser.close()` fix joins gate 5 (daily note 01:05 and 01:35). **The drafter
did NOT read the mail bodies** (no AgentMail call in a read-only commission): every builder claim below comes from commit
messages, code comments, the builder's BACKLOG, Tuesday's daily note or gate 4's report, and is a CLAIM.
**THREE HEADS WERE PRE-FILLED BY THE DRAFTER FROM `git ls-remote origin` (both repos 01:36:20 AEST; each `cat-file -t` = commit);
THE BC ROW IS A PLACEHOLDER — BC's branch was NOT on origin at drafting. THE LAUNCHER RE-READS EVERY HEAD.** If any head moves
before launch, Tuesday edits its row; the launcher parses §PIN, refuses any placeholder, and re-reads EVERY head by `git ls-remote`
immediately before launch, refusing on any mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-23 01:50
Self-check note: Tuesday read the header, PIN table, §BC notes and the self_check_view output (numbers/ids/claims, no contradiction found); pinned BC and added the PINNED note because the drafter's note (d) predates BC's lib/pdf.js commit. Not re-read line by line end to end at 65% context — stated here, not hidden.

SLOT-BC: IN
*(Filled `IN` by the drafter on Tuesday's ruling that BC joins gate 5. **To launch with BC:** replace the three `@BC_…@`
placeholders in PIN row BC with its 40-hex head, its 40-hex base (expected: the MAIN-Q row) and its commit count, all read by
`git ls-remote origin`, then re-read §BC against the pinned delta (the drafter read only an UNPUSHED local ref). **To launch
without BC:** set this line to `OUT`, set row BC's status to `OUT` with `-` in head/base/commits, DELETE BOTH `SLOT-BC:BEGIN`..
`SLOT-BC:END` marked sections (§1 and §BC) from this brief AND the `[SLOT-BC BEGIN]..[SLOT-BC END]` block from the prompt. The
launcher refuses the placeholder and any inconsistency between the SLOT line, the row and the blocks.)*

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build any of these changes and you owe no builder anything. **Every line below that reports
what a builder says is a CLAIM, never evidence.**

**ONE batched gate, THREE targets + ONE slot, TWO repos, ONE session** (Kam's standing rule of 2026-09-18: batch gates, never
pay for the same setup twice). **Give a SEPARATE verdict for each: A9, CF5R2, IO1 (and BC if IN) — each GO / NO-GO, each naming
its pinned sha.**
**⚠ Letter collision:** this gate's TARGET letters are NOT the builder's item names. A9 = the builder's "A-9" / "item 12" (logo ink
inset); CF5R2 = round 2 of gate 4's CF5 (= gate 3's C-F5 + C2-F2), answering gate 4's CF5-F1 and CF5-F2; IO1 = gate 4's finding
**I10-O1** (NOT gate 4's target I10, which is GO and on main); BC = the "bounded browser.close()" test-harness fix. Always write both
(e.g. "IO1 (I10-O1)", "A9 (A-9)").
Tiers:
- **A9 (A-9, logo ink inset) is TIER 2, CUSTOMER-VISIBLE**: CSS only, v2.33, every phone user sees the masthead and footer move.
- **CF5R2 (CF5 round 2, provider-only refund) is TIER 1**, and **ROUND 2 of 2: the cap — a second NO-GO ships the parts that
  closed and tickets the rest** (say plainly, per part, what would ship and what would be ticketed if you grade NO-GO).
- **IO1 (I10-O1, portal async route errors) is TIER 1**: it replaces an Express 4 internal under EVERY route of the live portal's
  code, including the unauthenticated sign-in.
- **BC (bounded browser.close()) is TIER 2, through-code** — present only if SLOT-BC is IN — **EXCEPT that it touches the shipped
  module `stage3/lib/pdf.js`** (`closeBrowser()`): the parts of the gate that prove production is untouched are TIER 1 in rigour.

**NOT IN THIS GATE:** portal S-1 (`fix/feedback-report-auth-2026-09-22` @ `89af8ba`) is GO from gate 2 and waits on Kam's card.
N (A-6 r2), FU, I9, Q5 (QuickQuote) and I10 (portal) were GO at gate 4 and are ON main (QuickQuote `3bfbfa2` = N, FU, I9, Q5 merged
in that order; portal `6f197ca` = I10 merged). **P5B (puppeteer 25 + node 22) is GO-tested at gate 4 and HELD by Kam's decision 14 —
NOT on main.** Do not gate any of them; do not re-open them.

## RULED BY KAM, AND SETTLED (Vision `1_Project_Definition/CLARIFICATIONS.md`)
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` — read it whole
(C-01..C-05 at drafting; no new entry since gate 4).
- **No C-entry covers any target here.** Their authority is the Vision agent's own backlog, gate 4's findings and **Tuesday's
  rulings**: CF5 round 2 = "a provider-wide failure always returns its GLOBAL hit; only the per-source refund is capped (6/h); a
  store (`putOtp`) failure refunds uncapped" (daily note 01:26); IO1 = fix gate 4's I10-O1 in one place (01:35); BC = a bounded
  close (5 s, then kill the test's OWN browser process; never touch the updater), and Tuesday ruled YES to it changing
  `closeBrowser()` in `lib/pdf.js` (01:35).
- **Known and Kam's — REPORT, DO NOT FAIL ON** (they go in Kam's pack): (1) an office that KEEPS retrying through a long provider
  outage spends its own per-source hits past the cap and gets its own per-source 429 at recovery (builder: Retry-After ~1741 s) —
  the cap's intended trade; (2) **CF5-F3**, the unchanged 502 wording for a rejected address. Measure and quote both; they are not
  grounds for NO-GO. Anything else that locks out a source that did NOT keep retrying IS a finding.
- **No product choice in the targets is Kam's ruling** (A9: the inset formula; IO1: patching `Layer.prototype.handle_request`
  rather than 26 try/catch edits, and refusing to boot on a non-Express-4 Layer; BC: the 5 s bound). Report each as the BUILDER's
  choice (or Tuesday's) and say whether it needs Kam.
- **Kam's pending decisions that bound this gate** (`Vision_Sales_Portal/5_Project_History/2026-09-22_kam-decisions-and-publish-pack.md`,
  READ ONLY): decision 14 (P5B) still holds; decision 18 (QuickQuote's production logs) — never query any production log.
- The QuickQuote repo's own rules: `Quoting Tool/hpas-quoting-tool/CLAUDE.md` (single offline HTML file; **version discipline**;
  **always verify print as a real PDF**; nothing in the sub-project goes near Azure). Read it.
- Deploys are HELD for Kam. Nothing here merges on your word.

## PRIOR ROUND
- **Gate 4's report is ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate4/`
  (`report.md` + `sections/` + `evidence/`). Read its VERDICTS, FINDINGS INDEX, NOT TESTED, and the CF5, I10 and N sections.
- **CF5R2 is ROUND 2 of 2.** Round 1 gated `bfb8210`: **NO-GO** on **CF5-F1 (Major)** — past a source's cap `refundHits` returned
  before BOTH refunds, so each over-cap provider failure kept one of the 20 site-wide hits; 4 offices each retrying through a 60-min
  503 outage drained the global budget and a FRESH office that never retried got `429 sign-in is busy right now` at recovery (T0+61),
  first 200 at T0+91 (gate 4 lead's S1; the fork's 30-min fresh-address variant: first 200 at T0+76). **CF5-F2 (Minor)** — the cap
  also covered the throwing-`putOtp` refund: 8 store throws left 4 codes, not 6 (the cap was SHARED: 4 putOtp throws + 4 provider
  failures gave 6 refunded, 2 spent). Also CF5-F3 (wording, Kam's), CF5-P1 (unlisted transport codes spend), CF5-O1, CF5-O2.
  C-F5 and C2-F2 were CLOSED at `bfb8210`. Round 2 = `bfb8210` + a forward merge of main `3bfbfa2` (`1435686`) + ONE commit `309e6c7`.
- **IO1 answers gate 4's I10-O1** (MAJOR, pre-existing on main and in production's code): a DB fault in an async PRO route with no
  try/catch (e.g. `GET /api/quotes`) was an unhandled rejection that killed the whole portal process — MEASURED identically on
  `aeadcc1` and `515c9f8` (`sections/I10.md`, `evidence/I10-crash.sh`, `I10-crash-{main,head}.log`).
- **A9 is ROUND 1.** It revisits item 20 (v2.30, `f96a622`, 2026-08-28, "the disclaimer finally lines up with the logo"), whose
  BACKLOG entry said the drift was "not something CSS can read".
- **BC is ROUND 1.** It answers the intermittent test hang gate 4 recorded as **N-C1** (gate-file runs that "finished every cell, then
  hung in teardown until their deadline") and gate 4's self-finding 4 (orphaned `chrome_crashpad_handler` / `GoogleUpdater`
  processes); the builder diagnosed the installed Chrome's GoogleUpdater child blocking puppeteer's `browser.close()` (daily note 01:05).
- **PRIOR WORK — verify every claim above against history, never against this brief:** `git log` / `git show` for `f96a622` and
  the item-20 BACKLOG entry (A9); `bfb8210`, `1435686` (CF5R2); gate 4's I10 section and evidence (IO1); gate 4's N-C1 and
  self-finding 4 (BC). If this brief's account of prior work disagrees with the record, the record wins — report it as a brief
  correction.
- **Gate 4's harnesses are REUSABLE BY COPY** (`…/2026-09-22-vision-qq-gate4/evidence/`): `qa-run.py` (the env -i runner),
  `qa-chrome-egressblock.sh`, `qa-egress-monitor.py`, `qa-egress-posctl.mjs`, `qa-netlog-scan.py`, `qa-floorcount.py`,
  `qa-harness-floorctl.mjs`, `lockcmp.py`, `lockwalk.py`, `mktree-qq.sh`, `mktree-portal.sh`, `qa-mkdb.cjs`, `qa-dbcheck.cjs`;
  **CF5:** `qa-harness-cf5.mjs`, `qa-lib-cf5-stage3.cjs`, `qa-harness-cf5-c2contract.mjs`, `qa-harness-cf5-login.mjs`,
  **`qa-harness-lead-cf5.cjs`** (the lead's independent S1-S4 outage probe — the one that re-measured CF5-F1), `CF5-mutate.py`;
  **I10/IO1:** `qa-harness-i10.cjs`, `qa-i10-preload-fetchguard.cjs`, `I10-crash.sh`; **N (for A9's renders):**
  `qa-harness-n-render.cjs`, `qa-harness-n-server.cjs`, `qa-lib-n-stage3.cjs`, `qa-lib-n-png.cjs`, `qa-harness-n-probe-sweep.cjs`,
  `qa-harness-n-probe-crops.cjs`, `N-pdfcompare.sh`; **P5B (for BC's emailed-PDF compare):** `qa-harness-p5b-emailed.cjs`,
  `qa-lib-p5b-png.cjs`, `P5B-pdfcompare.sh`. Gate 4's `sections/CONVENTIONS.md` is the working method. COPY what you use into this
  gate's own evidence folder, read it before trusting it, and never edit gate 1-4's copies. **Self-findings from gates 2-4 bind you:**
  (1) quote every path (the project path has a space); (2) **zsh does not word-split `set -- $p`, and zsh reads `$s:stage3/…` as a
  history modifier** — gates 3 AND 4 voided batches on it, and this brief's drafter hit it again: run every such loop under `bash`;
  (3) never detach a control server; (4) the portal test-DB name MUST end in `_test`; (5) npm's update-notifier egresses unless
  disabled; (6) isolate a browser context per case; puppeteer's default PDF is Letter — pass `format: "A4"`; (7) the real renderer
  calls public FX APIs whenever currency ≠ USD — BLOCK and RECORD them (§13.3); (8) gate 4 CF5: a harness leg that asserts the shape
  it measured is circular for a NO-GO — re-measure any NO-GO with an independent probe; (9) gate 4: concurrent Chrome jobs made the
  phone gate file hang in teardown (N-C1) — run each browser gate file ALONE, and time it.

## PIN — HEADS (PRE-FILLED BY THE DRAFTER EXCEPT BC; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
Rules the launcher enforces: every `IN` row has a 40-hex head and base, a commit count, no `@`; head is a commit in its repo;
base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals head NOW; **base is either the same repo's MAIN row head, or — a STALE BASE — an ancestor of the repo's
MAIN row that equals `merge-base(head, MAIN)`** (the row then needs a forward merge at merge time; the launcher prints a NOTE naming
it, and §12 measures it). MAIN rows are re-read by `ls-remote` too. An `OUT` row carries `-` in head/base/commits; **only BC may be
OUT.** **Gated anchors (launcher-checked):** CF5R2 contains the gated round-1 head `bfb8210` and `1435686`'s parents are exactly
`bfb8210` + the MAIN-Q row; A9's base carries item 20's fixed `--logo-ink-inset: calc(.5rem + 18.9px);` line; IO1's base carries
I10's `app.use(lastResortHandler);`; BC's base (if IN) calls `closeBrowser` only from the two test files.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | 6f197ca8e6090cd6b6a8ac6c5969fa772e3767c4 | - | - | IN |
| MAIN-Q | quickquote | main | 3bfbfa25c8dae52c2ac16b96d4ddf65ad075fdb6 | - | - | IN |
| A9 | quickquote | fix/qq-logo-ink-inset-2026-09-23 | 5d787d24a7b2ed8d33d319bd495b35ee0dbd96be | 763269d8e910e2dae9a418429d408405e37f164f | 1 | IN |
| CF5R2 | quickquote | fix/qq-otp-refund-provider-only-2026-09-22 | 309e6c7e96e0f7694c597252849c8689f9b58e90 | 3bfbfa25c8dae52c2ac16b96d4ddf65ad075fdb6 | 3 | IN |
| IO1 | portal | fix/portal-async-route-errors-2026-09-23 | a83140ebcbbd29b50f054e3b088c5cbed43efa09 | 6f197ca8e6090cd6b6a8ac6c5969fa772e3767c4 | 1 | IN |
| BC | quickquote | fix/qq-bounded-browser-close-2026-09-23 | aa8901067aec9bb0ff8ec6f296f51e9cd029b572 | 3bfbfa25c8dae52c2ac16b96d4ddf65ad075fdb6 | 2 | IN |
<!-- PIN-HEADS:END -->

**PINNED BY TUESDAY 2026-09-23 01:50 (supersedes the drafter's note (d) below):** BC = `aa8901067aec9bb0ff8ec6f296f51e9cd029b572` (ls-remote), base `3bfbfa2`, 2 commits (`907f686`, `aa89010`). **The pinned delta DOES change `stage3/lib/pdf.js`** — only inside `closeBrowser(ms = 5000)` and its leading comment (launcher guard 74 corrected by Tuesday to accept a parameterised signature and the function's own comment; red-proofed: a one-line edit inside `renderQuotePdf` is refused). **§BC's production clauses are LIVE.** Builder's claims to verify, not trust: renderer bytes unchanged outside that block; emailed PDF text-identical, 0 differing pixels, bytes identical with dates masked; full `test:print` 115/115 in one run, exiting in ~22 s.


Repos: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`); QuickQuote = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool`
(remote `datasecau/vision_hpas-quickquote`).
**Shape at drafting (READ, 01:36-01:50):** **CF5R2 and IO1 sit on current main** (CF5R2 via its forward merge `1435686`; IO1 directly
on `6f197ca`). **A9 is a STALE-BASE row: it sits on `763269d`**, i.e. QuickQuote main BEFORE N, FU, I9 and Q5 merged — it does NOT
contain A-6 (N), although the builder's merge-order note says "after A-6". A9 needs a forward merge at merge time (§12). **BC**
(if pinned as the drafter expects) sits on `3bfbfa2`. **A GO is a statement about the pinned SHA only.** If a head moves, its verdict
expires.
**Commission corrections the drafter made at source (verify):** (a) A9 does not contain A-6 — "after A-6 (already on main)" is a merge
ORDER, satisfied only by A9's forward merge onto `3bfbfa2`, which the builder has not made; both sides edit the same
`toolVersion` line (2.31 → 2.32 on main, 2.31 → 2.33 on A9) and the same `test:print` line — expect CONFLICTS (§12). (b) A9's
lockfile is the OLD `64e49cb` (pre-Q5) because it sits on `763269d`; main's is `70ebda7` — A9 changes no lockfile. (c) BC's
`closeBrowser()` callers are `stage3/test/fx-provenance.mjs` and `stage3/test/typed-rates.mjs` (directory `test/`, not `tests/`).
(d) At drafting BC's branch existed only as a LOCAL, UNPUSHED ref (`907f686`, 01:35:43, on `3bfbfa2`, one commit "stage3 tests:
bound every browser.close() at 5 s, then kill the test's own Chrome") whose delta did NOT touch `stage3/lib/pdf.js` — it touched
`stage3/package.json`, `stage3/test/{email-collector,phone-layout,print-fit,xlsx-parity}.mjs` and added `stage3/test/lib-close.mjs` +
`stage3/test/lib-close.test.mjs`. Tuesday's ruling says the `lib/pdf.js` change is coming; §BC's production clauses apply IF the
pinned delta touches `lib/pdf.js`, and are reported as "not applicable — lib/pdf.js unchanged" otherwise.

## 1. Targets — READ from the object store at drafting (01:36-01:55 AEST)
Drafting shas = the PIN table. **No target changes a lockfile** (stage3 `package-lock.json`: `70ebda7` at `3bfbfa2` and `309e6c7`;
`64e49cb` at `763269d` and `5d787d2`; portal `9d426df` at `6f197ca` and `a83140e`, 248 entries incl. root; express `4.22.2`); the
launcher re-checks this at the pinned heads. **Every file:line below is at the pinned sha; re-locate by content if anything moved.**
Cell counts (`grep -c '^test('` in `stage3/test/server.test.mjs`): `763269d` 90, `5d787d2` 90, `3bfbfa2` 93, `309e6c7` 100.

### TARGET A9 — A-9: the logo's ink, the disclaimer and the footer share one left edge on a phone (TIER 2, CUSTOMER-VISIBLE), QuickQuote
- **One commit `5d787d2` on `763269d` (STALE: main is `3bfbfa2`).** Files: `BACKLOG.md` (the item-20 drift entry ticked),
  `index.html`, `stage3/package.json` (`test:print` gains `test/logo-inset.mjs`), `stage3/test/logo-inset.mjs` (A, 86 lines).
- **The CSS (READ):** ONE declaration changes: `--logo-ink-inset: calc(.5rem + 18.9px);` → `--logo-ink-inset: calc(.5rem + min(18.9px,
  (100% - 1rem) * 59 / 1080));` (plus a 14-line comment). `CONFIG.toolVersion` `"2.31"` → `"2.33"` ("A-6 already claims 2.32"). **No
  `@media print` line added or removed** (launcher-checked). The variable is consumed by `padding-left: var(--logo-ink-inset)` at
  the masthead `.subline` and `.site-foot .org` (READ at `3bfbfa2`: 2 uses + a comment). **The mechanism rests on a subtle CSS fact
  — a `%` inside a custom property resolves where the property is USED, against THAT element's containing block — and on the claim
  that each using element's containing block is exactly as wide as the logo's. MEASURE both; enumerate every `var(--logo-ink-inset)`
  consumer in both builds (the stripped hosted page included) and say whether any resolves `%` against a different box.**
- **Builder's claims:** text-minus-ink within 0.02 px at every width 320-1300 (1 px sweep), both builds, both themes; was 1.96 px at
  390, 2.77 at 375, 5.78 at 320; the gate file (24 cells: 1280/768/430/390/375/320 × light/dark × 2 builds; first ink column found by
  decoding the real image on a canvas) red on main at 390/375/320 (12 cells) and green here; desktop 768/921/1280 × light/dark ×
  default/heavy: 0 pixels differ from main "(same version)"; print: 2 pages, identical text and rasters, both themes ("the masthead
  and footer do not print").
- **Version:** 2.33 on a stale base whose version is 2.31, while main is 2.32. READ QuickQuote `CLAUDE.md` §Version discipline.

### TARGET CF5R2 — CF5 ROUND 2 of 2: global refund always returned; per-source refund capped; store failures uncapped (TIER 1), QuickQuote
- **Chain over its base `3bfbfa2` (3 commits):** `bfb8210` (the GATED round-1 head, on `763269d`) → `1435686` = merge of main
  `3bfbfa2` into CF5 ("One conflict, BACKLOG.md … server.js, both test files and lib/mail.js auto-merged, each equal to main plus
  CF5's own change (-U0)") → `309e6c7` "stage3: CF5 round 2 — the refund cap is per source only; store failures refund uncapped".
  Files over `3bfbfa2`: `BACKLOG.md`, `stage3/lib/mail.js`, `stage3/lib/sendFailure.js` (A), `stage3/server.js`,
  `stage3/test/mail.test.mjs`, `stage3/test/server.test.mjs`. `309e6c7` alone: `BACKLOG.md` (+ the I9-F1 entry, "as ruled"),
  `stage3/server.js`, `stage3/test/server.test.mjs` (+2 cells).
- **`refundHits(kind)` at `309e6c7` (READ):** `globalBudget.refund("*", now);` FIRST and unconditionally; then `if (kind === "store")
  { ipBudget.refund(src, now); return; }`; else (provider) `const at = clock().getTime(); if (refundCap.waitMs(src, at) > 0) {
  console.error("[stage3] OTP refund cap reached for one source — this failure spends its per-source hit"); return; }
  refundCap.record(src, at); ipBudget.refund(src, now);`. Call sites: `catch (e) { refundHits("store"); throw e; }` and
  `outcome.then(r => { if (r === "failed") refundHits("provider"); });`. `lib/sendFailure.js`, `lib/mail.js` and the 502 text are
  unchanged from `bfb8210` (verify by diff).
- **What the new rule widens (drafter, READ — measure):** the GLOBAL refund is now UNCAPPED for every provider-wide failure. The
  per-source bound (6 codes + 6 refunded tries per source per hour) still holds, but the global budget (20/h) no longer bounds
  provider-shaped failures across MANY sources. If a caller can manufacture a provider-shaped failure (gate 4: NOT TESTED against
  real ACS; READ `lib/mail.js`), how many provider calls per hour can N sources buy, round 1 vs round 2? Measure with a fake that
  fails provider-wide for caller-chosen addresses, 1 / 4 / 16 XFF sources.
- **Cells (READ, 2 new at `309e6c7`):** `CF5-F1: after a 60-min provider outage with 4 offices retrying, a FRESH office signs in at
  recovery (the global hit is always returned)`; `CF5-F2: a throwing putOtp is OUR failure — refunded without the per-source cap: 8
  throws still leave the full 6 codes`. Builder: each red on round 1 "for the gate's reason"; mutants "global behind the cap -> C2-F2
  + CF5-F1; store through the cap -> CF5-F2; global refund dropped -> C2-F2 + CF5-F1; no per-source cap -> the C-F5 cap cell".
- **Builder's stated residual (Kam's, report only):** the retrying office's own per-source 429 after a long outage; CF5-F3 wording.

### TARGET IO1 — I10-O1: a rejected async route reaches the error handler instead of killing the portal (TIER 1), portal
- **One commit `a83140e` on `6f197ca`.** Files: `BACKLOG.md`, `server/asyncErrors.js` (A, 51 lines), `server/asyncErrors.test.js`
  (A; in `npm test`, no DB), `server/index.js` (+3: `require('./asyncErrors');` before any router), `test/db/async-faults.test.js`
  (A; in `test:db`).
- **`server/asyncErrors.js` (READ):** `require('express/lib/router/layer')`; `install()` returns if `Layer.prototype[Symbol.for(
  'vision.asyncErrors')]`; throws `asyncErrors: express Layer is not the Express 4 shape this patch was written for` unless both
  `handle_request` and `handle_error` are functions; replaces `Layer.prototype.handle_request` with: `if (fn.length > 3) return
  next();` then `try { const ret = fn(req, res, next); if (ret && typeof ret.then === 'function') ret.then(undefined, (err) =>
  next(err || new Error('async handler rejected without a reason'))); } catch (err) { next(err); }`. `install()` runs at require.
  **Compare it LINE BY LINE to express 4.22.2's own `lib/router/layer.js` `handle_request` from YOUR installed `node_modules`** and
  name every difference (e.g. whether 4.22.2 calls `next()` with or without an argument for the arity skip; anything else it does).
- **What it covers (builder, READ):** 26 of 81 async handlers had no try/catch (BACKLOG: admin 2, auth 1 = `POST /api/auth/login`,
  feedback 1, monday 1, partnerOrgs 1, quotes 10, reminders 3, settings 1, tco 6). Cells: `asyncErrors.test.js` — router handler,
  app-level handler and async middleware that reject → 500 + ref, fault logged under it, no unhandled rejection, server still serving;
  controls: a sync throw, a resolving handler, an explicit `next(err)` "handled once", a 4-arg error handler skipped;
  `async-faults.test.js` — every app query failing (session queries untouched): 26 routes answered, the 11 GETs exactly 500 + ref,
  login under a fault 500 + ref and recovers. **Builder's red-on-main claim: on `6f197ca` the DB file fails 20 route cells plus login
  and never exits; with the patch not installed the three class cells time out.**
- **Edges the drafter found by READ (measure each):**
  - **Rejection after headers are sent / a streaming response.** `serverError` logs and answers only `if (!res.headersSent)` — it
    never ends the response. A handler that has started a response (e.g. the backup route streams `archive.pipe(res)` at
    `routes/admin.js:173`) and then rejects will now reach `serverError`, log, and leave the socket OPEN: the process no longer dies,
    but does the client hang until its own timeout? Before IO1 the process exited. Measure with a stub route that writes headers
    then rejects, and with a rejection mid-stream; grade a hang.
  - **A handler that calls `next(err)` AND then rejects** (or rejects after calling `next()`) → `next` called twice: logged twice?
    a second response attempt? `ERR_HTTP_HEADERS_SENT`? The builder's control covers "calls next(err) itself (logged once)" — read
    exactly what that cell does and probe the double-call shape.
  - **4-arg error handlers skipped:** the patch keeps `fn.length > 3 → next()`. Confirm an async 4-ARG error handler that rejects is
    still NOT caught by this patch (it goes through `handle_error`, unchanged) — say whether any exists in the app.
  - **The refuse-to-boot guard:** under Express 5 `express/lib/router/layer` does not exist, so the `require` throws
    `MODULE_NOT_FOUND` before the shape check can print its message. Probe both (a fake Layer missing `handle_error`; a resolver that
    hides the module) and quote what an operator would see. Also: does the guard stop a DIFFERENT 4.x whose `handle_request` does
    more than 4.22.2's (it only checks `typeof`)?
  - **Idempotence and order:** `require('./asyncErrors')` after a router was already constructed — does the patch still apply (it
    patches the prototype, so it should)? Measure once.
  - **The unauthenticated login** under a DB fault: 500 + 8-hex ref, no crash, no unhandled rejection, no user enumeration change,
    then a normal sign-in once the DB is back; `/api/health` stays 200 throughout the fault and after.
- **What it does NOT cover (READ):** async code OUTSIDE a route layer (a `setTimeout`/cron callback, the reminder dispatcher, the
  session store's own callbacks, `initDb`/seed at boot) — list every such site and say whether an unhandled rejection there still
  kills the process. Outside IO1's claim; report with a severity.

<!-- SLOT-BC:BEGIN -->
### TARGET BC — a bounded browser.close() (TIER 2, through-code; lib/pdf.js clauses TIER 1 in rigour), QuickQuote — present because SLOT-BC: IN
- **PINNED DELTA NOT READ BY THE DRAFTER** (the branch was not on origin at drafting). Tuesday re-reads this section against the
  pinned head. At drafting a LOCAL unpushed commit `907f686` (on `3bfbfa2`) bounded `browser.close()` at 5 s and then killed the
  test's own Chrome in `stage3/test/{email-collector,phone-layout,print-fit,xlsx-parity}.mjs` through a new helper
  `stage3/test/lib-close.mjs` (+ its own cell file `lib-close.test.mjs`), with a one-line `stage3/package.json` change — and did
  NOT touch `lib/pdf.js`.
- **The shipped-module premise (READ at `3bfbfa2`):** `stage3/lib/pdf.js` exports `{ renderQuotePdf, closeBrowser }`; `closeBrowser`
  (line ~199) is called ONLY by `stage3/test/fx-provenance.mjs` and `stage3/test/typed-rates.mjs` (`after(closeBrowser)`);
  production (the stage3 server) imports `renderQuotePdf` only. The launcher checks this premise at the pinned head.
- **What the gate must establish (Tuesday's ruling, 01:35):** (1) `renderQuotePdf` and the browser launch (`browser()`,
  `puppeteer.launch({...})`) are BYTE-UNCHANGED; the only `lib/pdf.js` change is inside `closeBrowser()` (and any helper only it
  calls); (2) production never calls `closeBrowser` (READ every import of `lib/pdf.js` in stage3, and MEASURE: the server under your
  harness renders and emails a PDF with a spy on `closeBrowser` that must record 0 calls); (3) the EMAILED PDF from the real
  `lib/pdf.js`, main `3bfbfa2` vs BC (default USD and heavy AUD, a fixed qnum, renderer egress blocked): text-identical and **0
  differing pixels** (apart from the creation timestamp bytes); (4) a FORCED `close()` hang (a stubbed browser whose `close()` never
  resolves, and — separately — a real Chrome whose close you stall) still lets EACH test file exit on its own within the bound + a
  margin, and kills only the test's OWN browser process (never the updater, never a Chrome the file did not start — verify by pid
  ancestry against your claude pid); (5) the bound cannot kill a browser that is still rendering (a close that completes in 4.9 s is
  NOT killed).
<!-- SLOT-BC:END -->

### All targets
- **No worktree is pinned. Build your own trees INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store:**
  `git -C <repo> archive <pinned sha> | tar -x -C <a fresh mktemp -d under your project>`. **Never `git worktree add`,
  `checkout`, `switch`, `fetch`, `pull`, `stash`, `reset`, `restore`, `clean`, `gc`, `tag` or commit against either repo, and
  never work inside either checkout.** Both checkouts are the LIVE builder's working trees: pin by sha, read origin by `ls-remote`.
- **Dependencies, without the network:** in YOUR archived tree, **`npm ci --offline --ignore-scripts`** (in `stage3/` for QuickQuote,
  at the root for the portal). `--offline` forbids the network by construction: a cache miss FAILS rather than fetches — that suite is
  then **NOT RUN, blocker named** (name the missing tarballs). Never `npm install`, never `npm ci` without `--offline`, never `npx` a
  package that is not already in the tree, **never `npm audit`** (a registry call). After it, prove `node_modules/.package-lock.json`
  matches `git show <sha>:<lockfile>` entry by entry and quote the count (gate 4: stage3 282/282, portal 247/247), by `lockcmp.py` AND
  the on-disk `lockwalk.py`. Chrome: `PUPPETEER_EXECUTABLE_PATH` = YOUR copy of the egress-block wrapper (§13.3).
- **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a
  clean arm; never touch gate 1-4's trees (`work/`, `work-g2/`, `work-g3/`, `work-g4/`). Use `work-g5/`.
- **`git merge-tree --write-tree` writes objects** — only ever as `GIT_OBJECT_DIRECTORY=<your own mktemp -d>
  GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree --name-only <a> <b>`, **from the gate's
  OWN object directories**. The same two variables let you `git archive <tree-id>` a merge RESULT. If you cannot do it that way, SKIP
  it and say so.
- **A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES:** `node --check` on every mutated `.js`/`.mjs`/`.cjs` before its arm, exit code
  quoted. A red from a mutant that does not parse or load is a VOID arm, never a red. (CSS mutants: prove the edit landed by a `diff`.)
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every positive or negative control is a separate measurement that could have come
  out the other way on its own (a comparator's control finds a planted difference; a crash probe's control crashes on main). A
  control derived from the same run it validates is not a control.
- **NOT on main. Nothing merges on your word or a builder's.** Merges are Tuesday's GO on a pinned head.

## 2. Why these tiers, and who is waiting
- **IO1** changes how EVERY request of the live portal's code is dispatched, including the unauthenticated sign-in; it turns a
  process crash into a 500 — and must not turn it into a hang or a double response.
- **CF5R2** bounds what one network can make `/auth/request` do to ACS and Table Storage, and decides who is locked out after an
  outage. Round 2 of 2.
- **A9** changes what every phone user sees in the masthead and footer, both builds.
- **BC** de-flakes the print/phone gates (N-C1) and touches a shipped module.
- 🔴 **Queue:** deploys HELD for Kam (the live tool is v2.30; Kam's pack v5 + the publish-card amend are deferred to ONE update after
  this gate). Portal: IO1 on main. QuickQuote: CF5R2 and BC on main; A9 needs a forward merge onto `3bfbfa2` (§12).

## 2a. LEGITIMATE SHAPES — CHECKERS in this gate (template §2a)
CF5R2 refuses (a budget, a refund cap); IO1 answers faults. Measure every row.

| shape — its ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| CF5R2: 4 offices, one rep each retrying the SAME address every 5 min through a 60-min 503 outage; a FRESH office signs in at recovery | fresh office 200 at T0+61 (round 1: 429 until T0+91) | global hit always returned | builder (cell) + gate 4 lead S1 — **measure with the lead's probe** |
| CF5R2: 3 offices, 60-min outage (gate 4 S2) | fresh office 200; each retrying office its own per-source 429 at recovery | per-source cap | gate 4 — **measure; the retrying office's 429 is Kam's, report only** |
| CF5R2: 1 office, 60-min outage (gate 4 S4) | that office 429 at recovery, Retry-After quoted | per-source cap | gate 4 / builder (~1741 s) — **report only** |
| CF5R2: Table Storage (`putOtp`) throws for 10 min; an office retries 8 times | 8 × 500, then 6 × 200, then 429 | store failures refund uncapped | builder (cell) — measure |
| CF5R2: 4 putOtp throws + 4 provider failures from one source (gate 4's shared-cap row) | the 4 store refunds do NOT consume the cap: 4 + 4 refunded | kind-split | drafter (READ) — measure |
| CF5R2: 100 junk addresses from one source | 6 × 502 then 94 × 429 (unchanged from round 1) | rejected spends | gate 4 — measure |
| CF5R2: 6 people behind one NAT, one sign-in each; a 7th | 6 × 200, 7th per-source 429 | 6/h per key | gate 3 (needs Kam, unchanged) |
| IO1: a Postgres blip during `GET /api/quotes` (signed-in rep) | 500 `{ error: 'Internal error', ref }`; the portal keeps serving; next request 200 | `serverError` via `next(err)` | builder (cell) — measure |
| IO1: a Postgres blip during the unauthenticated `POST /api/auth/login` | 500 + ref; then the same user signs in | same | builder (cell) — measure |
| IO1: an admin downloads the backup zip and the DB fails mid-stream | the response ends (truncated/aborted), the process lives, one log line | ? | drafter (READ) — **measure; a response left open is a finding** |
| A9: a rep on a 375 px phone opens the offline file, dark mode | disclaimer and footer text start on the logo's first ink column (±0.5 px) | the new `--logo-ink-inset` | builder (cell) — measure |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.** A legitimate shape refused is a
**Major**.

## 3. TARGET A9 — A-9 (TIER 2, CUSTOMER-VISIBLE)
**Screenshots from YOUR OWN renders, never the builder's.** Chrome through YOUR egress-block wrapper; a fresh browser context per
case; theme set by clicking the real `#toggleDarkMode` control, settle ≥ 600 ms, applied theme VERIFIED from `html[data-theme]`.
**FAIL condition (state it before the run):** any text/ink edge further apart than 0.5 px at a supported width (320 and up) in either
build or theme; any page sideways scroll; any desktop pixel changed outside the version digits; any print/emailed PDF change outside
the version line; any OTHER consumer of `--logo-ink-inset` moved.
1. **Independent measurement (MEASURED):** YOUR own ink finder (not the builder's file) — decode the real logo PNG yourself, find the
   first ink column, and measure the disclaimer and footer glyph edges by Range, at 320-1300 by 1 px, light AND dark, both builds
   (offline `index.html` from `file://` and the hosted page from `strip.js` output behind YOUR harness, signed in). Base `763269d` vs
   A9: quote the max |text − ink| per band. Positive control: the base shows the builder's 1.96 / 2.77 / 5.78 px drift (±0.1).
2. **The `%` premise (MEASURED + READ):** for every consumer of the variable, the computed `padding-left` in px vs the logo's rendered
   width × 59/1080 + 8 px; zoom 200 % at 390; a 60-character unbroken customer name; the hosted masthead with Sign out + the cog.
3. **Desktop identity (MEASURED):** 768 / 921 / 1280, light and dark, default and heavy, both builds: base `763269d` vs A9 → only the
   version digits differ (2.31 → 2.33). Name any other difference.
4. **Print unchanged apart from the version (MEASURED):** printed quote as a real A4 PDF (print media) base vs A9, light and dark page
   theme; `pdftotext` differs only in the version line; raster differs only in the footer band; the emailed PDF from the real
   `lib/pdf.js` likewise. Quote the 2.33 footer line from a real PDF.
5. **The gate file (MEASURED):** `logo-inset.mjs` alone at A9 → 24/24, exits on its own (time it); with A9's file on base `763269d`'s
   `index.html` → which cells fail (builder: 12, at 390/375/320); red arm (CSS, diff-proved): restore `calc(.5rem + 18.9px)` → red;
   `59 / 1080` → `60 / 1080` → does the 0.5 px tolerance catch it?
6. **A9 × main (PROBED):** `merge-tree` A9 × `3bfbfa2` from YOUR object dir. Drafter's READ expectation (NOT measured — the drafter
   could not run merge-tree): conflicts in `index.html` (`toolVersion`) and `stage3/package.json` (`test:print`). Never hand-resolve;
   if the CSS hunk auto-merges, run your §3.1 measurement on a tree built from main's `index.html` with ONLY A9's
   `--logo-ink-inset` line applied (diff-proved) — i.e. the A-6 phone layout AND the inset together at 320/360/375/390/430.
7. **Suites at A9:** `stage3/` `npm test`, `test:print` (each browser file ALONE if N-C1 recurs — record it), `test:xlsx`, pricing.
8. **Version (READ):** 2.33 over a 2.31 base while main is 2.32 — within QuickQuote's rule? What version does the merged file carry?

## 4. TARGET CF5R2 — CF5 ROUND 2 of 2 (TIER 1)
**The drivable surface is `createApp(...)` in YOUR OWN harness** (gate 4's `qa-lib-cf5-stage3.cjs`, COPIED after reading), a fake
mail that records and fails per address and per error SHAPE, `trustForwardedFor: true` for XFF legs, the APP clock for every outage.
**FAIL condition (state it first):** a source that did NOT keep retrying is refused after an outage (CF5-F1 open); a store failure
spends a per-source hit (CF5-F2 open); a refund beyond the per-source cap; a classification driven by caller text; any gate-4 CLOSED
property (C-F5, C2-F2) re-opened.
1. **CF5-F1 re-check (MEASURED, positive control first):** run gate 4 lead's `qa-harness-lead-cf5.cjs` S1-S4 UNCHANGED (copied; hash
   quoted) on round 1 `bfb8210` — it must reproduce gate 4's table (S1 fresh office 429 at T0+61, first 200 T0+91) — then on
   `309e6c7`: S1 fresh office 200 at T0+61; S2, S3; **S4 (the retrying office's own 429 — Kam's, report the Retry-After)**. Also the
   fork's 4 × 12 fresh-address 30-min variant. Then an INDEPENDENT probe of your own (not derived from the builder's CF5-F1 cell) at
   8 offices × 90-min outage.
2. **CF5-F2 re-check (MEASURED):** 8 putOtp throws → 8 × 500, then 6 × 200, then 429 (round 1: 4 × 200); the gate-4 shared-cap row
   (4 store + 4 provider) → store refunds do not consume the cap; 20 store throws from one source → still 6 codes (UNCAPPED: say
   whether that is an unbounded Table Storage write path for one source, and grade it — a store outage is not caller-made, but each
   throw is a `putOtp` attempt).
3. **The uncapped global refund (MEASURED, §1):** provider-shaped failures from 1 / 4 / 16 sources for 1 h: provider calls made, codes
   issued, global budget remaining — round 1 vs round 2. Say whether the global budget still bounds anything for provider failures.
4. **Everything gate 4 closed still holds (MEASURED):** C-F5 (100 junk → 6 × 502 then 94 × 429, five shapes, with the main positive
   control on `3bfbfa2`: 100 × 502, never 429); classification table (gate 4's 59 shapes); the real `lib/mail.js` with an ACS recorder
   (gate 4's 14 cases); gate 4's derived C contract copy (116 checks) re-run — predict first which, if any, change; the cap window on
   the app clock; `otpRefundCapPerHour` validation.
5. **The forward merge `1435686` (READ ONLY):** `merge-tree bfb8210 × 3bfbfa2` from YOUR object dir (the builder: BACKLOG conflict only);
   for every file except `BACKLOG.md`, the auto-merged blob must equal `1435686`'s; `git diff 3bfbfa2 1435686 -- stage3/` must equal
   `git diff 763269d bfb8210 -- stage3/` hunk for hunk. Quote.
6. **Red-proofs (parse-checked, `node --check` rc quoted):** (a) global refund moved back behind the cap → CF5-F1 cell AND your S1
   redden; (b) store routed through the cap → CF5-F2 reddens; (c) global refund dropped → C2-F2 + CF5-F1; (d) per-source cap removed
   → the C-F5 cap cell; (e) `kind` ignored (every refund treated as `"provider"`) → which. **A fix with no reddening cell is a finding.**
   Also confirm each builder cell is red on round 1 `bfb8210` as claimed.
7. **Suites at CF5R2:** `stage3/` `npm test` (100 cells in server.test + mail/strip/store), `test:print`, `test:xlsx`, pricing.
8. **Login page (MEASURED, one case):** the 502 text for a rejected address and the 429 text a locked-out office sees, as the page
   renders them (real Chrome, 375 and 1280) — quote both; customer-visible.
9. **Round-2 cap (say it in the verdict):** if NO-GO, list which parts CLOSED (C-F5, C2-F2, CF5-F1, CF5-F2, each) and would ship, and
   which are ticketed.

## 5. TARGET IO1 — I10-O1 (TIER 1)
**The portal's `createApp()` in YOUR harness on LOCAL Postgres (§13.2), `env -i`; never the portal's entry point (it binds all
interfaces).** Gate 4's `qa-harness-i10.cjs` + `qa-i10-preload-fetchguard.cjs` + `I10-crash.sh` by COPY.
**FAIL condition (state it first):** any async route fault that still kills the process; a faulted request that never gets an answer
while the process lives (a hang); a double response / `ERR_HTTP_HEADERS_SENT` crash; a fault logged twice or not at all; `/api/health`
not 200 during or after a fault; the unauthenticated login leaking anything beyond 500 + ref; any change to a NON-faulted request.
1. **Positive control first (MEASURED):** gate 4's `I10-crash.sh` shape on main `6f197ca` → the process EXITS on `GET /api/quotes` with
   a DB fault (quote the exit); then on `a83140e` → 500 + 8-hex ref, process alive, next request 200.
2. **The 26 routes (MEASURED):** every route in the builder's list under a DB fault on YOUR `_test`-suffixed or app DB (a renamed table,
   or a pool stub that rejects app queries but not session queries): status, body shape, one log line under the ref, no
   `unhandledRejection`, process alive, `/api/health` 200. Then the builder's red-on-main claim: `async-faults.test.js` on `6f197ca`
   → 20 route cells + login failing and the file never exiting (bound it with your deadline; quote what you saw).
3. **The edges in §1 (MEASURED, one probe each):** rejection after headers sent; rejection mid-stream (a stub route that pipes then
   rejects; and the real backup route with a fault injected after `setHeader`, on YOUR DB only); `next(err)` then reject; reject after
   `next()`; an async 4-arg handler that rejects; a sync throw (unchanged); a resolving handler (unchanged); a handler returning a
   non-promise thenable. For each: client outcome within 30 s, log lines, process state.
4. **Line-by-line vs express 4.22.2 (READ):** quote express's `Layer.prototype.handle_request` from YOUR installed `node_modules` beside
   the patch; name every difference and whether it changes behaviour for a non-async handler.
5. **Refuse-to-boot (MEASURED):** a fake Layer without `handle_error` → the thrown message; a module resolver that hides
   `express/lib/router/layer` → what an operator sees (`MODULE_NOT_FOUND`?); install twice → one patch (the Symbol).
6. **The unauthenticated login (MEASURED):** under a DB fault → 500 + ref, the same shape for a known and an unknown username (no
   enumeration), no crash; after recovery → normal sign-in; rate-limit / lockout counters unchanged by the fault (READ which exist).
7. **Async sites outside a route layer (READ, then MEASURE one):** list them (§1); inject one rejection → does the process still die?
8. **Red-proofs (parse-checked):** remove the `require('./asyncErrors')` line → the DB cells and the class cells redden (the builder:
   time out); drop the `ret.then` branch → which; call `next(err)` without the `|| new Error(...)` fallback and reject with
   `undefined` → which (Express treats `next(undefined)` as success: a hang?).
9. **Suites at `a83140e`:** `npm test` (builder 87/87), `npm run test:db` on a FRESH `vsp_qa_g5_<epoch>_test` database (prove it fresh
   first: zero user tables), which runs `async-faults.test.js` and gate 4's 413 cell.

<!-- SLOT-BC:BEGIN -->
## BC. TARGET BC — bounded browser.close() (TIER 2 through-code; lib/pdf.js clauses TIER 1 in rigour) — present because SLOT-BC: IN
**FAIL condition (state it first):** any byte of `renderQuotePdf` or the browser launch changed; any production path reaching
`closeBrowser`; the emailed PDF differing in text or by one pixel (timestamp bytes excepted); a test file that does not exit on a
forced close hang; a kill that reaches any process the test did not start; a healthy close killed early.
1. **Scope (READ):** `git diff --stat <base> <BC head>`; every file named; if `lib/pdf.js` is touched, extract `renderQuotePdf`,
   `browser()`, `svcInject()` and the `puppeteer.launch` options at base and head and prove them byte-identical (quote the hashes);
   quote the whole `closeBrowser` diff. `package.json` delta = test scripts only.
2. **Production never calls it (READ + MEASURED):** every `require("./lib/pdf")` / `lib/pdf.js` import in stage3 outside `test/`;
   then your harness server emails a PDF with a spy on the export → 0 calls.
3. **Emailed PDF identity (MEASURED):** gate 4's `qa-harness-p5b-emailed.cjs` + `P5B-pdfcompare.sh` (copied): main `3bfbfa2` vs BC,
   default USD and heavy AUD, fixed qnum, egress blocked → pages equal, `pdftotext` equal, raster 0 differing pixels; the comparator's
   positive control (a planted difference) must fire in the same run.
4. **Forced hang (MEASURED):** (a) a stubbed browser whose `close()` never resolves → each patched test file exits within 5 s + margin
   (time it; quote the kill line); (b) a real Chrome with its close stalled (e.g. SIGSTOP on the browser process you started) → same;
   (c) the kill targets only that browser's own pid tree — prove by pid ancestry anchored on your claude pid that no updater or
   foreign Chrome was signalled; (d) a slow but healthy close (4.9 s) is NOT killed.
5. **N-C1 (MEASURED):** run `test:print` (all browser files) 10× back-to-back AND 3× with a concurrent Chrome job (gate 4's hang
   shape): 0 teardown hangs, every run exits on its own; the same loop on main `3bfbfa2` as the control (it may or may not hang — quote).
6. **Red-proofs (parse-checked):** revert the bound in one test file → under (4a) that file hangs to your deadline; revert `closeBrowser`
   (if changed) → `lib-close`/its cell reddens.
7. **Suites at BC:** `stage3/` `npm test`, `test:print`, `test:xlsx`, pricing.
<!-- SLOT-BC:END -->

## 12. Across targets — merges and the queue
**The drafter did NOT run merge-tree for this gate (its commission forbade it). Every row below is a READ expectation. Quote `git
merge-tree --write-tree --name-only` from YOUR OWN object directory for each pair, or say you skipped it.** Never hand-resolve.

| pair | drafter's READ expectation |
|---|---|
| `bfb8210` × main `3bfbfa2` (CF5R2's forward merge) | CONFLICT `BACKLOG.md` only (builder's own account); every other file = `1435686`'s |
| A9 `5d787d2` × main `3bfbfa2` | likely CONFLICT `index.html` (`toolVersion`) and `stage3/package.json` (`test:print`); the CSS hunk likely auto-merges |
| A9 × CF5R2 | likely clean (disjoint files except BACKLOG.md — measure) |
| A9 × BC, CF5R2 × BC | BC's `test:print` / test files vs A9's `test:print` line — measure |
| IO1 × main `6f197ca` | IO1 sits on main |
| IO1 × S-1 `89af8ba` (context only) | measure (`BACKLOG.md` and `server/index.js` both touched?) |

- **A GO is a GO at the pinned sha only.** Name, for each target, the cells to re-run on its merged head (at least: A9 — `logo-inset.mjs`
  + your independent ink sweep + desktop/print compare + N's 80 phone cells on the merged file; CF5R2 — the stage3 suite + S1-S4 +
  your contract copy + the real-mail leg; IO1 — `npm test` + `test:db` on a fresh DB + your edge probes; BC — the forced-hang arms and
  the emailed-PDF compare). **CI:** `gh` is not authenticated for `datasecau`; every target's CI half is **NOT RUN**, measured at merge.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (`session-tools/nexusai-lock.sh`).
1. **The Vision builder seat is LIVE** (claude `1613`, pane `%41`) and owns portal `:4848` and stage3 `:8080`. **Never use 4848 or
   8080**, nor `47787` (Tuesday's dashboard), nor any port another seat holds. Take every port from the kernel and bind `127.0.0.1`
   wherever YOUR harness listens. Never start the portal's entry point (it binds `0.0.0.0` in `main()`).
2. **Postgres = the running local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all.**
   Create `vsp_qa_g5_<epoch>` for app runs and `vsp_qa_g5_<epoch>_test` as `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs; the name
   MUST end in `_test`; never `salesportal`, `salesportal_test`, any `vsp_qa_g1_*`, `vsp_qa_g2_*`, `vsp_qa_g3_*` or `vsp_qa_g4_*`
   database, or the builder's `vsp_bf1_*`). Local defaults from `server/db.js` / `scripts/ensure-test-db.js` only; never anything from
   `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the portal runtime legs are **NOT RUN, blocker named**. Leave your
   databases in place and list their names (no DROP).
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH, HOME = a fresh mktemp dir, TZ, NODE_ENV = `test`
   or `development` — never `production` — PORT, a fresh random SESSION_SECRET / unlock word / `COORDINATOR_SECRET` you generate,
   DATABASE_URL / TEST_DATABASE_URL = yours, PUPPETEER_EXECUTABLE_PATH, `NTFY_SERVER=http://ntfy.invalid`, dummy provider values,
   `npm_config_update_notifier=false`, `npm_config_offline=true`). **NEVER set in a product process:** `AGENTMAIL_API_KEY`,
   `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product
   process's env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh**: set `NTFY_SERVER=http://ntfy.invalid`
   before any portal module is required and stub `fetch` to throw on any other URL.
   **Egress — including Chrome children:** the real QuickQuote renderer's page calls three public FX APIs whenever currency ≠ USD.
   **Block it** with YOUR copy of `qa-chrome-egressblock.sh` as `PUPPETEER_EXECUTABLE_PATH` and **prove the block with a positive
   control**. Record outbound connections of EVERY process you start, Chrome children included (`lsof` over the whole process tree,
   plus the net-log scan). **Gate 4's self-finding 4: GoogleUpdater reparents out of the descendant monitor — record every
   `GoogleUpdater` / `chrome_crashpad_handler` process at start and end (pid, ppid, start time) and say which appeared during the gate.**
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (gate 4's `qa-floorcount.py`, COPIED from
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate4/evidence/qa-floorcount.py`):
   `basename(argv[0]) == node` AND an app entry point ANYWHERE in the remaining argv, from the kernel; **"ours" = the ancestor chain
   CONTAINS your claude pid**. **Negative controls, same run, must classify FOREIGN:** the Vision builder's claude `1613` (pane `%41`),
   Tuesday's claude `3434` (pane `%0`), the NexusAI seat's claude `8360` (pane `%44`). Re-read them at start; if one has exited, say so
   and use the others (gate 4's QA seat `26862` has exited). Never by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. **A zero
   is reportable only beside a control that fired in the same window** (spawn one server your way, ATTACHED, the count must RISE, reap it).
5. **THE DEADLINE RULE:** every real-server, browser and database step has a written DEADLINE (boot 60 s, request 30 s, render 60 s,
   DB connect 15 s, exit 20 s) and a client timeout on every request (no `timeout` binary here — build deadlines into your runner); a
   step past its deadline is ABORTED and reported (a hung product request IS a finding). **Every server, browser and child you start is
   killed in a `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat
   for 5 minutes is aborted and reported.** A9's 1 px sweep, CF5R2's outage legs, IO1's `async-faults` on main (it never exits) and
   BC's forced-hang and 10× loops are the shapes that hang.

**Reap every server and every Chrome you start.** An orphan of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (App Service `hpas-quickquote`, resource group `hpas-quickquote-rg`, its ACR `hpasqqacr`, its Table
  Storage, its log workspace `hpas-quickquote-logs` — decision 18: never query it) **or the live portal**
  (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the live site, its
  Postgres `datasec-sales-db.postgres.database.azure.com` and key vault). No request, no DB connection, not even a GET or a health
  probe. **Never ntfy.sh** or any ntfy host. **Never the three FX hosts.** Never the npm registry (`npm audit` included). Never
  `api.agentmail.to` from a product process. Never the Feedback_System coordinator.

### HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npm audit`, no `npx` of
  anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Real sends are OFF.** Every provider is a recorder you wrote.
- **Findings-only:** do not commit, do not move any branch, do not file a ticket, **no writes in either repo**, inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), inside `Feedback_System/`, inside the builder's scratchpad, or inside gate
  1-4's report folders. The gate fixes nothing.
- **NEVER `rm`** — quarantine; every preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate5/report.md`

**QUESTIONS:** if you must ask, mail `tuesday-agent@agentmail.to` with subject `[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>`
(Context / one Question / Meanwhile / Needed-by) and **proceed on the safest reading**; the ANSWER arrives in `tuesday-agent@` with
subject beginning `[Wednesday -> QA/Vision-gate5] ANSWER` — read it with your verdict key. Record every question, the reading you
took and any answer in the report. If a response is cut off by a safety check, record it and continue with the next item; this is
authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 5: CF5 round 2 + I10-O1 async route errors (tier 1) + A-9 logo inset + bounded browser.close (tier 2), heads as pinned at launch`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the QA
project has none. Use it ONLY in your own verdict/question/answer-read `curl` (with a client timeout, e.g. `-m 30`); it must never
enter a product process's environment (§13.3). Never put the key, or any secret, in a mail or the report.

Verdict format:
- **A9 (A-9), CF5R2 (CF5 r2), IO1 (I10-O1)** — and **BC (bounded close)** if IN — each **GO / NO-GO**, stated SEPARATELY PER TARGET,
  each naming its pinned sha and branch. For CF5R2: CF5-F1 and CF5-F2 each closed or not (with the round-1 positive control), C-F5 and
  C2-F2 still closed, the two Kam items measured and quoted (the retrying office's 429 + Retry-After; CF5-F3's wording), and — if
  NO-GO — that this was round 2 of 2: which parts ship and which are ticketed. For IO1: the crash on main (positive control) vs the 500
  on the branch, and each §5.3 edge. For A9: the max edge gap per band, base vs A9. For BC: renderQuotePdf/launch byte-unchanged,
  production 0 calls, emailed PDF 0 pixels, forced hang exits.
- The verbatim strings Kam's publish ask needs: A9's before/after in plain words and the 2.33 footer from a real PDF; CF5R2's 502 and
  429 texts as the page renders them; IO1's client body and log line for a faulted request (operator-visible).
- Then one paragraph on the queue quoting §12's merge-tree results (or that you skipped them).
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section — at least: real App Service `X-Forwarded-For`; real
  ACS rejection shapes and quota accounting; real Azure Postgres failover shapes (IO1); Node 20 / Node 22 (every result is this
  machine's node); CI; real phones / Safari / Firefox (A9); multiple replicas; every stale-base target's forward-merged head (only
  PROBED)). Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY. §3 Q1-Q7, §4 Q1-Q8,
  §5 Q1-Q9 and (if IN) §BC Q1-Q6 must each carry one.
- Report each pinned head, and both mains, as three timestamped readings (start / mid / end), each with its branch name.

PROVENANCE:
- heads: portal main 6f197ca8e609…, fix/portal-async-route-errors-2026-09-23 a83140ebcbbd…; QQ main 3bfbfa25c8da…,
  fix/qq-logo-ink-inset-2026-09-23 5d787d24a7b2…, fix/qq-otp-refund-provider-only-2026-09-22 309e6c7e96e0…;
  fix/qq-bounded-browser-close-2026-09-23 ABSENT from origin (local unpushed 907f686686…) | `git -C <repo> ls-remote origin` +
  `cat-file -t` (all = commit) | read 2026-09-23 01:36:20 AEST
- chains: 5d787d2 on 763269d (merge-base with 3bfbfa2 = 763269d); 309e6c7 → 1435686 = merge(bfb8210, 3bfbfa2); bfb8210 on 763269d;
  a83140e on 6f197ca; QQ main 3bfbfa2 = merge Q5 ← merge I9 (4c49eaf) ← merge FU (6cda865) ← merge N (f2b2b4e) on 763269d; portal main
  6f197ca = merge I10 (8aaff37) on aeadcc1; f96a622 (item 20) ⊂ 763269d | `git log --format='%h %p %s'`, `merge-base`, `rev-list` | read 01:37-01:45
- file sets; lockfile blobs (stage3 70ebda7 at 3bfbfa2/309e6c7, 64e49cb at 763269d/5d787d2; portal 9d426df at 6f197ca/a83140e, express
  4.22.2); cell counts (90/90/93/100) | `git diff --stat`, `git rev-parse <sha>:<path>`, python over `git show`, bash (the drafter's
  first zsh read of the counts was VOID: `$s:stage3` history modifier) | read 01:40-01:45
- mechanisms and strings (asyncErrors.js, errors.js `serverError` headersSent, admin.js:173 `archive.pipe(res)`, refundHits(kind),
  --logo-ink-inset, closeBrowser callers) | `git show`, `git grep` | read 01:42-01:50
- seats: %41 → claude 1613 (Vision), %0 → claude 3434 (Tuesday), %44 → claude 8360 (NexusAI); gate 4's QA 26862 exited; :5433 listening
  (docker) | `tmux list-panes -a`, `ps -axo pid,ppid,comm`, `lsof` | read 01:39
- builder claims / READY times / Tuesday's rulings | Tuesday daily note `0_Brain/daily_tuesday/2026-09-23.md` 00:32-01:35 lines;
  commit messages (mail bodies NOT read)
