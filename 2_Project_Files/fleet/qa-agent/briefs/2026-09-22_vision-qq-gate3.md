# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, BATCHED GATE 3 (portal + QuickQuote): C = A-1 ROUND 2 sign-in-code budgets (TIER 1, narrow), B = S-2 ROUND 2 reminder push redaction (TIER 1, narrow), K = item-1 follow-ups A1-F1 + A1-F2 (TIER 2), L = small sweep A-7 + A-8 + A-10 (TIER 2), M = SLOT for D-F1 (TIER 2), N = SLOT for A-6 phone layout (TIER 2, CUSTOMER-VISIBLE)

**Drafted for Tuesday 2026-09-22 21:13-21:45 AEST by a read-only drafting agent; Tuesday reviews, re-checks the pre-filled PIN table, stamps and launches.**
Commissioned on the Vision_Sales_Portal agent's READY mails as Tuesday's daily note records them (B-F1 on S-2 10:43Z; A-7/A-8/A-10
09:59Z; C round 2 11:12Z; the item-1 follow-ups named at 19:59; M and N named by Tuesday at ~21:15). **The drafter did NOT read the
mail bodies** (no AgentMail call in a read-only commission): every builder claim below comes from commit messages, code comments,
Tuesday's daily note, the builder's scratchpad files or gate 2's report, and is a CLAIM.
**EVERY HEAD WAS PRE-FILLED BY THE DRAFTER FROM `git ls-remote origin` (portal and QuickQuote 21:13:48, M and N re-read 21:15:39
AEST; each `cat-file -t` = commit); THE LAUNCHER RE-READS THEM ALL.** If any head moves before launch, Tuesday edits its row; the
launcher parses §PIN, refuses any placeholder, and re-reads EVERY head by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | @SELFCHECK_TS@
Self-check note: @SELFCHECK_NOTE@

SLOT-M: IN
SLOT-N: IN
*(Both filled `IN` by the drafter on Tuesday's instruction of ~21:15 ("Fill BOTH slots IN"). If Tuesday flips one to `OUT`: set
that PIN row's status to `OUT` with `-` in head/base/commits, DELETE its `<!-- SLOT-X:BEGIN -->..<!-- SLOT-X:END -->` section from
this brief AND its `[SLOT-X BEGIN]..[SLOT-X END]` block from the prompt. The launcher refuses the placeholder and any inconsistency
between the SLOT line, the row and the two blocks.)*

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build any of these changes and you owe no builder anything. **Every line below that reports
what a builder says is a CLAIM, never evidence.**

**ONE batched gate, FOUR targets + TWO slots, TWO repos, ONE session** (Kam's standing rule of 2026-09-18: batch gates, never
pay for the same setup twice). **Give a SEPARATE verdict for each: C, B, K, L (and M, N if IN) — each GO / NO-GO, each naming
its pinned sha.**
**⚠ Letter collision:** this gate's TARGET letters are NOT the builder's item names. C = the builder's A-1 (round 2); B = S-2
(round 2); K = gate 1's A1-F1 + A1-F2 on QuickQuote item 1; L = the builder's A-7 + A-8 + A-10; M = gate 2's D-F1; N = the
builder's A-6. Always write both (e.g. "C (A-1)", "N (A-6)").
Tiers:
- **C (A-1 round 2, sign-in-code budgets) is TIER 1, NARROW**: the auth mail surface; round 2 adds a clock change, customer-visible
  refusal text, boot validation and a refund path.
- **B (S-2 round 2, reminder push redaction) is TIER 1, NARROW** (privacy): round 2 is ONE test-only commit on the gated `fb23f64`.
- **K (item-1 follow-ups, A1-F1 + A1-F2) is TIER 2**, through-code.
- **L (small sweep, A-7 + A-8 + A-10) is TIER 2**, through-code (A-10 changes what the hosted page POSTs with every quote email).
- **M (D-F1, header-order cell) is TIER 2**: test only.
- **N (A-6, phone layout) is TIER 2, CUSTOMER-VISIBLE** (the offline file AND the hosted page; toolVersion 2.31 → 2.32).

**NOT IN THIS GATE — portal S-1** (`fix/feedback-report-auth-2026-09-22` @ `89af8ba`) was **GO at gate 2** and waits on Kam's card
(partner visibility, A-F3, and the Feedback_System poller header). Do not gate it; do not re-open it. Where §12 names it, it is
context only.

## RULED BY KAM, AND SETTLED (Vision `1_Project_Definition/CLARIFICATIONS.md`)
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` — read it whole.
- **C-01..C-05** govern item 1 (C-01, feedback CC → Tuesday: K's surface) and item 3 (C-05: H, now on main, which C must not break).
- **No C-entry covers C's numbers, B's push text, K's precedence, L, M or N.** Their authority is the Vision agent's own
  security/backlog sweep, commissioned by Tuesday. **No product choice in them is Kam's ruling** (C: 6/h and 20/h — gate 2 said
  "needs Kam: yes"; C's new refusal wording; B: the push text; K: which variable wins when both are set; N: the phone layout
  itself): report each as the BUILDER's choice and say whether it needs Kam.
- The QuickQuote repo's own rules: `Quoting Tool/hpas-quoting-tool/CLAUDE.md` (single offline HTML file; **version discipline**
  §"Version discipline"; **always verify print as a real PDF**; nothing in the sub-project goes near Azure). Read it.
- Deploys are HELD for Kam. Nothing here merges on your word. **Tuesday's ruling on C (20:55, daily note):** "fix in C (all OTP
  windows read the app clock + an advance-clock cell), fold C-F1/F2/F3 onto C's branch, gate 3 (narrow tier 1)".

## PRIOR ROUND
- **Gate 2's report is ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate2/`
  (`report.md` + `sections/` + `evidence/`). Read its VERDICTS, FINDINGS INDEX, NOT TESTED, the C, B, D and H sections.
- **C is ROUND 2.** Round 1 gated `3c8d3a4`: **GO** with C-F1..C-F4 (Minor/Minor/Minor/Polish). The GO was about `3c8d3a4` only;
  the builder's forward merge onto H-merged main then went RED on a named re-run (the H harness limiter leg: C's budgets read
  `Date.now()`, H injects `clock()`), so C was NOT merged. Round 2 = `3c8d3a4` + forward merge `4b946d0` + four commits (§1).
- **B is ROUND 2.** Round 1 gated `fb23f64`: **NO-GO** on **B-F1 (Major)** — the digest control cell fails on every FRESH test
  database (`relation "feedback" does not exist`); the redaction itself was MEASURED correct (31/31). Round 2 = `fb23f64` + ONE
  test-only commit `479c3a2`.
- **K answers gate 1's A1-F1 and A1-F2** (and AX-F1 on the QuickQuote side). Gate 1's report:
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate1/report.md`.
- **M answers gate 2's D-F1** (the MUT-afterjson mutant stripped every header from 400/413 while the suite stayed 60/60).
- **L and N are ROUND 1.** L's A-10 is gate 2's reproduced "QUOTE MISMATCH — toggleAdvanced" (D §Q5).
- **Gate 2's harnesses are REUSABLE BY COPY** (`…/2026-09-22-vision-qq-gate2/evidence/`): `qa-harness-c-budget.mjs`,
  `qa-harness-c-login.mjs`, `qa-lib-c-stage3.cjs`, `qa-harness-h.mjs`, `qa-harness-h-a1.mjs`, `qa-harness-h-e2e.mjs`,
  `qa-lib-h.cjs`, `H-advanced-ids.json`, `qa-harness-b-push.cjs`, `qa-harness-b-parse.cjs`, `qa-mkdb-suffix.cjs` /
  `qa-harness-g-mkdb-suffix.cjs`, `qa-harness-d-http.cjs`, `qa-harness-d-browser.cjs`, `qa-lib-stage3-de.cjs`,
  `qa-harness-e-browser.cjs`, `qa-harness-e-http.cjs`, `qa-harness-fj-e2e.cjs`, `qa-harness-fj-render.cjs`, `qa-lib-fj-stage3.cjs`,
  `qa-run.py` (the env -i runner, WITH its mid-gate fixes: `npm_config_update_notifier=false`, `npm_config_offline=true`, the
  second-killpg fix), `qa-chrome-egressblock.sh`, `qa-egress-monitor.py`, `qa-netlog-scan.py`, `qa-floorcount.py`, `lockcmp.py`,
  `lockwalk.py`, `mktree-qq.sh`, `mktree-portal.sh`. COPY what you use into this gate's own evidence folder, read it before
  trusting it, and never edit gate 2's (or gate 1's) copies. **Gate 2's self-findings bind you:** (1) quote every path (the project
  path has a space); (2) **zsh does not word-split `set -- $p`** — gate 2's first merge-tree batch was VOID for it (the drafter hit
  the same trap drafting this brief): run such loops under `bash`; (3) never detach a control server (`( … &)` reparents it to
  launchd and it counts FOREIGN); (4) the test-DB name MUST end in `_test` (the portal's own guard `test/db/harness.test.js:11`,
  `/_test$/` — gate 2's G-F1); (5) npm's update-notifier egresses from a fresh HOME unless disabled; (6) `file://` pages share
  localStorage — isolate a browser context per case; puppeteer's default PDF is Letter — pass `format: "A4"`; (7) the real
  server-side renderer calls public FX APIs whenever currency ≠ USD (gate 1 O-4) — see §13.3, BLOCK and RECORD them.

## PIN — HEADS (PRE-FILLED BY THE DRAFTER; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
Rules the launcher enforces: every `IN` row has a 40-hex head and base, a commit count, no `@`; head is a commit in its repo;
base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals head NOW; **base is either the same repo's MAIN row head, or another IN row's head in the same repo
(a named stack), or — a STALE BASE — an ancestor of the repo's MAIN row that equals `merge-base(head, MAIN)`** (the row then
needs a forward merge at merge time; the launcher prints a NOTE naming it, and §12 measures it). MAIN rows are re-read by
`ls-remote` too. An `OUT` row carries `-` in head/base/commits. **Gated anchors (launcher-checked):** B's head contains the gated
`fb23f64`; C's head contains the gated `3c8d3a4`, and `4b946d0`'s parents are exactly `3c8d3a4` + `49d7027`.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | f065675c3a0d9f601a6e2a3041a2cb59d2e11cca | - | - | IN |
| MAIN-Q | quickquote | main | 51e92867930efd4c98b28dc5d95baf82219b3edb | - | - | IN |
| B | portal | fix/reminder-push-redaction-2026-09-22 | 479c3a20291e55c07901c0a506c3e8a54a0f1685 | 289e2d9545ae08fdcb8fdff47ba0115574e90f3e | 2 | IN |
| C | quickquote | feat/qq-otp-send-budget-2026-09-22 | bcef8f7dbc83da8f04d29600b882ff46d74d7b80 | 49d7027bcb627b001ed3de4c2cb560c234375261 | 6 | IN |
| K | quickquote | fix/qq-feedback-followups-2026-09-22 | a33f87ea1e3e4a6e11363b487cc5d68d6a14b52c | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 1 | IN |
| L | quickquote | fix/qq-small-sweep-2026-09-22 | 82710998d307234c843ed5f6f74a687a371cfbe4 | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 3 | IN |
| M | quickquote | fix/qq-d-f1-header-order-2026-09-22 | 0ab83e1ec52dcaec041c0491e972ce635d9ba987 | 51e92867930efd4c98b28dc5d95baf82219b3edb | 1 | IN |
| N | quickquote | fix/qq-phone-overflow-2026-09-22 | ac0a8d2536a8b991c51546e7f482df10ce0a5eb1 | 51e92867930efd4c98b28dc5d95baf82219b3edb | 1 | IN |
<!-- PIN-HEADS:END -->

Repos: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`); QuickQuote = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool`
(remote `datasecau/vision_hpas-quickquote`).
**Shape at drafting (READ, 21:13-21:30):** THREE different bases in QuickQuote, not one. **C sits on `49d7027`** (main after H and
J only; its forward merge `4b946d0`); **K and L sit on `1f3df8d`** (main BEFORE H, J, D, E, F, I — NOT on `51e9286`; Tuesday's
21:15 note that "every QuickQuote gate-3 target except C sits on 51e9286" is wrong for K and L); **M and N sit on `51e9286`**
(current main). **B sits on `289e2d9`**, which is IN portal main `f065675` (G merged) but B does not contain main. So B, C, K and L
are STALE-BASE rows and each needs a forward merge at merge time (§12). **A GO is a statement about the pinned SHA only.** If a head
moves, its verdict expires.

## 1. Targets — READ from the object store at drafting (21:13-21:45 AEST)
Drafting shas = the PIN table (read by `ls-remote` 21:13:48 / 21:15:39, each `cat-file -t` = commit). **No target changes a
lockfile** (portal `package-lock.json` blob `9d426df` at `f065675`, `479c3a2`; stage3 `package-lock.json` blob `64e49cb` at
`51e9286`, `bcef8f7`, `a33f87e`, `8271099`, `0ab83e1`, `ac0a8d2`); the launcher re-checks this at the pinned heads.
**Every file:line below is at the pinned sha; re-locate by content if anything moved.**

### TARGET C — A-1 ROUND 2: sign-in-code budgets, on one clock, validated, refunding (TIER 1, NARROW), QuickQuote
- **Chain over its base `49d7027` (6 commits):** `3c8d3a4` (the GATED round-1 head, on `1f3df8d`) → `4b946d0` = merge of main
  `49d7027` into C ("Merge main (H, J) forward into C (A-1)") → `8cbb39b` CLOCK → `792c5d5` C-F2 → `e7a43a4` C-F1 → `bcef8f7` C-F3.
  Files over `49d7027`: `BACKLOG.md`, `stage3/server.js`, `stage3/test/server.test.mjs` (the launcher refuses any other).
- **The forward merge `4b946d0` (READ + scratch merge-tree, drafter):** the auto-merge of `3c8d3a4` × `49d7027` CONFLICTS in BOTH
  `stage3/server.js` AND `stage3/test/server.test.mjs` (not the test file alone, as the READY mail was relayed) — so the builder
  hand-resolved BOTH. The auto-merge tree (`76a7b06…`) differs from `4b946d0`'s tree (`d6c4b8f…`) in exactly those two files
  (server.js 15 lines, server.test.mjs 274 lines). Cell counts (`grep -c '^test('`, server.test.mjs): `1f3df8d` 42, `3c8d3a4` 52,
  `49d7027` 64, `4b946d0` **74 = 64 + 10** (no cell lost by count), `8cbb39b` 76, `792c5d5` 77, `e7a43a4` 78, `bcef8f7` 80.
- **`8cbb39b` CLOCK (READ):** `/auth/request` `const now = clock().getTime();` feeds the per-address window, the resend cooldown
  and both budgets; `/auth/verify` reads `clock().getTime() > Number(rec.expiresAt)`. **Deliberately left on `Date.now()`:**
  session `createdAt`/`expiresAt` (`lib/store.js` checks session expiry against real time) and the feedback row key. +2 cells.
- **`792c5d5` C-F2 — CUSTOMER-VISIBLE TEXT (READ, VERBATIM):** the two budget refusals are now exactly
  `too many sign-in codes requested from your network` and `sign-in is busy right now` (no duration). The login page appends
  `. Try again in <N seconds|minutes>.` from `retryAfterSeconds` — the builder's claimed rendered lines:
  *"too many sign-in codes requested from your network. Try again in 60 minutes."* and *"sign-in is busy right now. Try again in
  60 minutes."* **You quote them from the page, not from this brief.** +1 cell.
- **`e7a43a4` C-F1 (READ):** `budgetSetting(name, value, fallback)`: `undefined`/`null`/`""` → default; else `String(value).trim()`
  must match `/^[0-9]+$/`, be `>= 1` and `Number.isSafeInteger` — or `createApp` THROWS naming the variable (the server refuses to
  start). `createApp` options now default to the RAW env strings (`otpIpBudgetPerHour = process.env.OTP_IP_BUDGET_PER_HOUR`). Note:
  a NUMBER passed as an option goes through `String()` — `1e9` as a number becomes `"1000000000"` and is ACCEPTED, while the env
  string `"1e9"` is refused (gate 2's exhaust leg passes `otpGlobalBudgetPerHour: 1e9` as a number) — measure, grade. `" 6 "` and
  `"06"` → 6 (READ). +1 cell.
- **`bcef8f7` C-F3 (READ):** `windowBudget` gains `refund(key, at)` (removes ONE hit with timestamp `at`); after the send,
  `outcome.then(r => { if (r === "failed") { ipBudget.refund(src, now); globalBudget.refund("*", now); } })` — inside the grace
  window (502) or after it. **NOT refunded: a THROWING `putOtp`** (the record still runs before `putOtp`; gate 2's C-F3 named BOTH
  the failed send and the throwing `putOtp`). The builder's own derived harness run (below) shows the throwing-`putOtp` converse
  still `[500,500,500,500,500,500,429]`, i.e. budget SPENT. +2 cells (one pins "a budget-refused request writes NO OTP" + source
  order of the budget checks before `putOtp` — gate 2's C-F3b).
- **The builder's DERIVED C-budget harness (READ by the drafter, a CLAIM to re-verify):** the builder's scratchpad (outside both
  repos, ephemeral) holds
  `/private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-Vision-Sales-Portal/bf3ee14c-882a-4385-a410-199b58d9800a/scratchpad/gate2-c/qa-harness-c-budget.C-F2F3-contract.mjs`
  (sha1 `edc0eeff…`), and an unmodified copy `qa-harness-c-budget.mjs` there is byte-identical to gate 2's (sha1 `bd40b388…`). The
  drafter's `diff` of gate 2's original vs the derived copy: **2 ADDED comment lines at the top + exactly 3 CHANGED lines** —
  `MSG_SRC` and `MSG_GLOBAL` (the C-F2 text) and ONE `q3` check: *"converse: failing send -> 502 each, and each attempt SPENDS budget
  (7th is the per-source 429)"* → *"C-F3 contract: failing send -> 502 each and SPENDS NO budget (all 7 are 502, none 429)"*.
  **The new q3 check is WEAKER than the contract:** it asserts only 7 × 502; it never shows the budget intact afterwards (a working
  mailbox then getting 6 × 200). The throwing-`putOtp` converse line was NOT changed and PASSED in the builder's run (budget spent).
  The `shapes` leg records `BOOT_ERROR` rather than asserting, so it needed no change. Builder's run logs in the same folder:
  `C-budget-contract.log` (SUMMARY checks=43 fails=0), `H-fix.log`.
- **Stated residual (unchanged):** real App Service `X-Forwarded-For` is NOT TESTED; a distributed sender can still exhaust the
  global 20/h.
- **C does NOT contain D, E, F or I** (they merged to main after `49d7027`): at `bcef8f7` there are NO security headers
  (`"Content-Security-Policy": CSP` absent — READ). Those arrive with C's SECOND forward merge (§12).

### TARGET B — S-2 ROUND 2: the fresh-DB fixture (TIER 1, NARROW), portal
- **Chain over its base `289e2d9` (2 commits):** `fb23f64` (the GATED round-1 head) → `479c3a2` "test(S-2): the digest control
  creates the feedback table first (gate 2 B-F1)". **`479c3a2`'s delta over `fb23f64` is ONE file, `test/db/reminder-push.test.js`
  (+5/−1)**: `require` gains `buildDigest`; `before()` calls `await buildDigest();` after `resetDb()` ("runs the app's own
  ensureFeedbackTable, so no DDL is copied").
- **`server/reminders/dispatcher.js` is byte-identical between `fb23f64` and `479c3a2`** (blob `283be27`, READ by `rev-parse`);
  portal main `f065675` = `289e2d9` carries blob `8831242` (without B). Files over `289e2d9`: `DEV-SESSION-SUMMARY.md`,
  `docker-compose.yml`, `server/reminders/dispatcher.js`, `test/db/reminder-push.test.js`.
- **Builder's claim:** proved on freshly created DBs `vsp_bf1_red_test` (before: 5/6, that error) and `vsp_bf1_green_test` (after:
  6/6); reused DB, full runner 5/4/6/17; `npm test` 77/77. **Those are the builder's databases — never touch them.**
- **CI (READ, gate 2):** `.github/workflows/test.yml` runs `npm run test:db` on a fresh `postgres:16` service — the reason B-F1 was
  Major.

### TARGET K — item-1 follow-ups: A1-F1 (a not-awaited cell) + A1-F2 (both variable names) (TIER 2), QuickQuote
- **One commit `a33f87e` on `1f3df8d`.** Files: `stage3/server.js` (+3/−1), `stage3/test/server.test.mjs` (+59).
- **A1-F2 (READ):** `feedbackNotify = process.env.FEEDBACK_NOTIFY_EMAIL || process.env.FEEDBACK_NOTIFY_EMAILS || DEFAULT_FEEDBACK_NOTIFY`
  — the SINGULAR wins when both are set. **The portal (main `f065675`, `server/feedbackNotify.js:34`) is the OPPOSITE:
  `env.FEEDBACK_NOTIFY_EMAILS || env.FEEDBACK_NOTIFY_EMAIL`** (plural wins). Same two variable names, opposite precedence across the
  two apps — measure both, and grade (a builder choice; say whether it needs Kam or just a one-line alignment).
  `parseRecipients` splits on `,`, trims, drops empties; `createApp` throws `feedbackNotify needs at least one address` if the list
  parses empty. **Predict and measure:** `_EMAIL=""` → falls through to `_EMAILS` (`||`); `_EMAIL=" , "` or `" "` → THROWS at
  `createApp` (the singular is truthy, so a valid plural is never consulted — compare the portal's G-F2 shape).
- **A1-F1 (READ):** a new cell: the feedback mail's `send` never resolves, the POST must answer 201 within 2 s (AbortController;
  `srv.closeAllConnections()`). The builder claims red-proofs: awaiting the send → "TIMED OUT (the POST waited for the mail)" ~3 s;
  dropping the plural name fails A1-F2. stage3 59/59, pricing 67/67 (at `a33f87e`, on `1f3df8d`).
- **Stale base:** K predates H, J, D, E, F, I on main; `createApp`'s signature on main now carries H's options (`51e9286`
  `server.js:144`). The drafter's scratch merge-tree K × `51e9286`: `server.js` auto-merges, **CONFLICT in
  `stage3/test/server.test.mjs`** (the tail).

### TARGET L — small sweep: A-7 + A-8 + A-10 (TIER 2), QuickQuote
- **Three commits on `1f3df8d`:** `b95cdf6` (A-7) → `6091305` (A-8) → `8271099` (A-10). Files: `BACKLOG.md`, `stage3/server.js`,
  `stage3/strip.js`, `stage3/test/server.test.mjs`, `stage3/test/strip.test.mjs`.
- **A-7 (READ) — the commission's wording was backwards:** strip.js's success line used to print `String.length` (UTF-16 code
  units, i.e. roughly CHARACTERS) and call it "bytes"; it now prints REAL BYTES (`Buffer.byteLength`) for `public/index.html`,
  `private/advanced.js`, `private/svc.js`. The label still says "bytes" and is now true. Cell: runs `strip.js` and compares the
  three numbers with `statSync().size`.
- **A-8 (READ):** `app.get("/favicon.ico", (req, res) => res.status(204).end());` placed after `/login`, before the OTP routes,
  no session needed. Cell: 204, empty body. (On main, D's header middleware precedes routes: after the forward merge the 204 should
  carry all six headers — measure on the merge result, §12.)
- **A-10 (READ) — CUSTOMER-FACING DATA FLOW:** the hosted email collector (`strip.js` `HOSTED_EXTRAS`, runs in the rep's browser)
  used to POST every `input/select/textarea` with an id. It now skips `const NOT_QUOTE = new Set(["toggleAdvanced",
  "toggleDarkMode", "advWord", "fbMsg"]);`. **The builder's commit message says the collector ALSO SENT THE TYPED HPAM WORD
  (`advWord`) and any half-written feedback (`fbMsg`) with every quote email** — a pre-existing leak of the advanced unlock word to
  the server with each quote, closed by L. READ-check where posted fields go (logged? stored by H's reopen allowlist? rendered?) on
  main and on L. `toggleAllowOptOut` is still posted (it can change which service options apply). **The only cell is a source regex**
  (`strip.test.mjs`: the Set literal and the skip line) — nothing drives the collector.
- **No version bump in K or L** (toolVersion stays `2.31` on `1f3df8d`); QuickQuote `CLAUDE.md` §Version discipline: "Changing
  behaviour without bumping the version is a bug". READ whether a stage3-only change (L's collector, A-8, K) is inside that rule;
  report it (gate 1's C-F11 was the same question and is carried "unchanged").

<!-- SLOT-M:BEGIN -->
### TARGET M — D-F1: pin the header middleware ahead of the body parser (TIER 2, test only), QuickQuote — present because SLOT-M: IN
- **One commit `0ab83e1` on `51e9286` (current main).** File: `stage3/test/server.test.mjs` (+21) only.
- **The cell (READ):** a malformed-JSON body (`'{"email":'`) → 400 and a 300 KiB JSON body → 413 (main's parser limit is
  `express.json({ limit: "256kb" })`, `51e9286` `server.js:232`), each must carry CSP containing `frame-ancestors 'none'`,
  `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Cache-Control: no-store`; plus a SOURCE-ORDER check:
  `src.indexOf('"Content-Security-Policy": CSP') < src.indexOf("app.use(express.json(")`.
- **Weakness to measure (drafter, READ):** the source-order check is VACUOUS if the first string is renamed (indexOf −1 is less
  than anything). The runtime half is what counts. It does NOT check `Strict-Transport-Security` or `Referrer-Policy` (2 of the 6).
- Builder claims: red with `express.json` moved above the headers (gate 2's MUT-afterjson); stage3 89/89 on `51e9286`.
<!-- SLOT-M:END -->

<!-- SLOT-N:BEGIN -->
### TARGET N — A-6: the tool fits a phone (TIER 2, CUSTOMER-VISIBLE), QuickQuote — present because SLOT-N: IN
- **One commit `ac0a8d2` on `51e9286` (current main), "v2.32".** Files: `BACKLOG.md`, `index.html` (+37/−2), `stage3/package.json`
  (`test:print` adds `test/phone-layout.mjs`), `stage3/test/phone-layout.mjs` (A, 77 lines). `CONFIG.toolVersion` `"2.31"` →
  `"2.32"` (on main `51e9286` `index.html:1655` it is `2.31`). **`index.html` is the OFFLINE tool AND the hosted page's source**
  (strip.js derives `stage3/public/index.html` from it): both builds change.
- **The CSS (READ):** `@media (max-width: 920px)` `main { grid-template-columns: 1fr }` → `minmax(0, 1fr)`; a NEW
  `@media screen and (max-width: 480px)` block: `.app-row` wraps (name `flex: 1 1 60%`, `.price` `margin-left: auto`); `.currency-tile`
  wraps; `.svc-result` wraps; `#svcSimple .svc-result .amt { white-space: normal; word-break: keep-all; … }`; `.svc-row`/`.svc-head`
  re-gridded `1.1rem minmax(0,1fr) auto` with children 2-4 re-placed; `.svc-wp-num` side padding 0. **No `@media print` line is added
  or removed** (READ; the launcher checks it). "Screen only."
- **The gate `stage3/test/phone-layout.mjs` (READ): 15 cells** = offline × {default, heavy, heavy-advanced} × {320, 375, 390} (9) +
  public × {default, heavy} × {320, 375, 390} (6). Each asserts `scrollWidth == clientWidth`, no element under `main` whose
  `scrollWidth > clientWidth + 1` (excluding `display: none|inline` and SELECT/TEXTAREA/INPUT), every `.ticket table.lines
  td:last-child` inside its tile and the viewport, every `.app-row .price` inside its `.panel`. **What it does NOT cover (READ):**
  anything outside `main` (the masthead — where the hosted build puts E's `Sign out` button and the settings cog); the DARK theme
  (it never ticks `toggleDarkMode`); `display: inline` elements; heights/overlap (a wrapped row overlapping the next); text
  truncated by `text-overflow`. It unlocks the offline advanced mode by typing the offline word into `advWord` (test fixture; say
  nothing more about that value in the report).
- **Builder's claims:** RED on v2.31 15/15; desktop 768/921/1280 light/dark default/heavy "byte-identical" PNGs to v2.31; the
  printed quote PDF "0 pixels differ on both pages; text identical"; stage3 88/88, test:print 44/44, xlsx-parity 5/5, pricing
  67/67. **Screenshots for Kam** (24 PNGs + README, READ ONLY — never write there):
  `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/5_Project_History/a6-phone-layout-2026-09-22-2053/`
  (`{default,heavy}-{320,375,390}-{light,dark}-{BEFORE,AFTER}.png`; README says BEFORE = main v2.31, whose `index.html` is identical
  to `1f3df8d`'s — the drafter confirmed `git diff 1f3df8d 51e9286 -- index.html` is EMPTY). An older folder
  `a6-phone-layout-2026-09-22/` (150 ms theme wait, "some dark shots may be mid-transition") is superseded — do not use it.
- **Builder's own NOT TESTED:** real phones, Safari/Firefox, widths below 320.
- **Dark theme mechanism (READ):** a checkbox `#toggleDarkMode` (`index.html:1141`, handler `:3450`), NOT `prefers-color-scheme` —
  drive the toggle; `login.html` has no dark theme at all (gate 2).
<!-- SLOT-N:END -->

### All targets
- **No worktree is pinned. Build your own trees INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store:**
  `git -C <repo> archive <pinned sha> | tar -x -C <a fresh mktemp -d under your project>`. **Never `git worktree add`,
  `checkout`, `switch`, `fetch`, `pull`, `stash`, `reset`, `restore`, `clean`, `gc`, `tag` or commit against either repo, and
  never work inside either checkout.** Both checkouts are the LIVE builder's working trees (at drafting: QuickQuote on
  `fix/qq-phone-overflow-2026-09-22`, portal on `fix/reminder-push-redaction-2026-09-22`): pin by sha, read origin by `ls-remote`.
- **Dependencies, without the network:** an archived tree has no `node_modules`. The builder's installed `node_modules` is NOT
  the gated set; do not copy it unless you prove, at copy time, that it matches entry by entry. The sanctioned route: in YOUR
  archived tree, **`npm ci --offline --ignore-scripts`** (in `stage3/` for QuickQuote, at the root for the portal). `--offline`
  forbids the network by construction: a cache miss FAILS rather than fetches — that suite is then **NOT RUN, blocker named**
  (name the missing tarballs). Never `npm install`, never `npm ci` without `--offline`, never `npx` a package that is not already
  in the tree. After it, prove `node_modules/.package-lock.json` matches `git show <sha>:<lockfile>` entry by entry and quote the
  count (gate 2: portal 247/247, stage3 282/282, by `lockcmp.py` AND the on-disk `lockwalk.py`). Chrome:
  `PUPPETEER_EXECUTABLE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, launched through YOUR copy of the
  egress-block wrapper (§13.3).
- **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree
  for a clean arm; never touch gate 1's or gate 2's trees (`work/`, `work-g2/`). Use `work-g3/`.
- **`git merge-tree --write-tree` writes objects** — only ever as `GIT_OBJECT_DIRECTORY=<your own mktemp -d>
  GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree --name-only <a> <b>`. The same two
  variables let you `git archive <tree-id>` a merge RESULT. If you cannot do it that way, SKIP it and say so.
- **A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES:** `node --check` on every mutated `.js`/`.mjs` before its arm, exit code
  quoted. A red from a mutant that does not parse or load is a VOID arm, never a red.
- **NOT on main. Nothing merges on your word or a builder's.** Merges are Tuesday's GO on a pinned head.

## 2. Why these tiers, and who is waiting
- **C** guards sign-in mail: a false refusal locks people out, a bypass sprays strangers and exhausts ACS (exhausted live
  2026-08-26, per BACKLOG). Round 2 touches every OTP time check (clock), adds a boot refusal (a mis-set variable now stops the
  server — an outage class of its own), a refund path, and customer-visible text. **C is the only gate-2 QuickQuote target not on
  main**; it blocks nothing else but its own publish.
- **B** closes a live disclosure of customer names and quote numbers on a public ntfy topic (whether the live topic is the
  documented value is UNMEASURED — production; do not try to find out). Round 2 is test-only; the question is only "is CI green
  on a fresh DB, and did nothing else change".
- **K** aligns item 1's variable names with the portal and pins "a hung mailbox never hangs a submission".
- **L**: A-10 stops a false alarm that trains people to ignore the one log line that catches a REALLY dropped PoC, and stops the
  HPAM word and feedback drafts riding along with every quote; A-7/A-8 are diagnostics hygiene.
- **M** pins a property gate 2 proved unpinned. **N** changes what every phone user sees, in both builds, and bumps the version.
- 🔴 **Queue:** deploys HELD for Kam (the live tool is still v2.30; the portal live site is production). Portal: B after its fix
  (on main `f065675` via a forward merge); S-1 held for Kam's card. QuickQuote: C (second forward merge onto `51e9286`), K, L, M,
  N — each merged forward by the builder in an order Tuesday sets (§12).

## 2a. LEGITIMATE SHAPES — CHECKERS in this gate (template §2a)
C (a mail budget, now with a boot refusal), K (a recipient list that refuses at boot when empty) each refuse something. Measure every row.

| shape — its ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| C: 6 people behind one NAT, one sign-in each in an hour; a 7th | 6 × 200; the 7th → per-source 429 | 6/h per key | builder — **grade the 7th (gate 2: needs Kam)** |
| C: a user signs in, the test/app clock advances 16 min, signs in again (H's harness shape) | 200 both times; nothing refused | `now = clock().getTime()` everywhere in `/auth/request` | builder (the CLOCK fix) — **measure** |
| C: `OTP_IP_BUDGET_PER_HOUR` / `OTP_GLOBAL_BUDGET_PER_HOUR` unset / `""` / `"6"` / `" 6 "` / `"06"` / `"10"` | 6 (20) / 6 (20) / 6 / 6 / 6 / 10 — server STARTS | `budgetSetting` | builder — measure |
| C: `"0"`, `"-1"`, `"0.5"`, `"Infinity"`, `"1e9"`, `"0x10"`, `"abc"`, `"1,000"`, `"+6"`, a 20-digit number | the server REFUSES TO START, naming the variable | `budgetSetting` throws | builder — **measure through the real entry-point code path as far as it can go without Table Storage (the throw is in `createApp`)** |
| C: the ACS mailbox is down for 10 minutes; an office retries 7 times, then ACS recovers | 7 × 502, then the office CAN sign in (budget intact) | `refund` on `"failed"` | builder (C-F3) — **measure the "after" half the derived harness dropped** |
| C: Table Storage write (`putOtp`) throws for 10 minutes; an office retries 7 times | **READ prediction: 6 × 500 then 429 — the budget is SPENT and the office is locked out for up to an hour after the outage** | no refund on the `putOtp` path | drafter — **measure; C-F3 named this half too** |
| C: the page shows a budget refusal | one sentence, then `. Try again in 60 minutes.` — no contradiction | C-F2 | builder — quote the page |
| K: neither variable set | default `kreiser.org@me.com,tuesday-agent@agentmail.to` (To Kam, CC Tuesday, C-01) | default | builder |
| K: only `FEEDBACK_NOTIFY_EMAILS` set (the portal's spelling) | honoured | `_EMAIL \|\| _EMAILS` | builder |
| K: both set to different lists | QuickQuote: `_EMAIL` wins; portal: `_EMAILS` wins | opposite `\|\|` orders | drafter — **measure both apps; grade the inconsistency** |
| K: `_EMAIL=""` and a valid `_EMAILS` | `_EMAILS` honoured, server starts | `""` is falsy | drafter — measure |
| B: a fresh test database, first run | `test:db` all green | `before()` → `buildDigest()` → `ensureFeedbackTable` | builder — **measure on a DB you prove fresh** |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.** A legitimate shape refused is
a **Major**.

## 3. TARGET C — A-1 ROUND 2 (TIER 1, NARROW)
**The drivable surface is `createApp(...)` in YOUR OWN harness** (the stage3 entry point cannot boot: `lib/store.js` throws without
`TABLES_CONNECTION_STRING`; no Azurite/Azure). Inject an in-memory store written to `lib/store.js`'s contract (gate 2's
`qa-lib-c-stage3.cjs` / `qa-lib-h.cjs`, COPIED after reading), a fake mail that records every send, and for the XFF legs pass
`trustForwardedFor: true` explicitly (never set `WEBSITE_SITE_NAME` in a product process). 127.0.0.1, kernel port.
1. **The forward merge `4b946d0`, proved (READ ONLY):** the auto-merge of `3c8d3a4` × `49d7027` conflicts in `stage3/server.js`
   and `stage3/test/server.test.mjs` (the drafter's scratch measurement; re-measure from YOUR object dir). Show that the builder's
   resolution is a UNION and nothing else: (a) `git diff 49d7027 4b946d0` must equal C's round-1 patch (`git diff 1f3df8d 3c8d3a4`)
   modulo context — compare them at `-U0` with hunk headers normalised (gate 2's `H-patch-vs-patch.txt` method); (b) `git diff
   3c8d3a4 4b946d0` must equal main's `1f3df8d..49d7027` delta modulo context; (c) every hunk where the auto-merge tree and
   `4b946d0` differ is named, read, and shown to be the conflict resolution (both sides' `createApp` options kept; H's and J's cells
   and C's 10 cells all present — 74 = 64 + 10 by count; prove by NAME that no H/J cell or C cell was dropped or altered).
2. **Each of the four round-2 commits, verified as its own claim, with ITS OWN red-proof** (a parse-checked mutant that undoes that
   one commit's product change alone, and the cell — builder's or yours — that reddens; a fix with no reddening cell is a finding):
   - **CLOCK (`8cbb39b`):** with an injected clock, advance 61 min → the same source gets a fresh budget (control: same instant →
     429); the resend cooldown and the per-address window end on the app clock; the OTP expiry is judged on the app clock (a code
     issued at T is refused at T + 10 min + 1 s by the app clock while the wall clock has not moved, and accepted at T + 9 min).
     **What stays on `Date.now()`** (session expiry): with the app clock advanced 8 days, is a session still valid (wall clock) —
     say whether that split can bite anything in production (it cannot if `clock()` is the real time: READ the entry point's
     `createApp` call and confirm no clock is injected there).
   - **C-F2 (`792c5d5`):** both 429 bodies verbatim; `Retry-After` == `retryAfterSeconds`; no duration word in either `error`.
   - **C-F1 (`e7a43a4`):** the §2a rows, every value for BOTH variables, through the env var as `createApp` reads it (gate 2's
     `shapes` leg) AND as a createApp option (number and string forms — `1e9` as a number is accepted: grade); the error message
     names the variable and quotes the value (does it echo anything a log should not carry? it echoes only the operator's own env
     value — say so). Confirm the throw happens at boot, not at first request.
   - **C-F3 (`bcef8f7`):** (i) 3 failed sends (502) then a working mailbox → the full budget is still there (6 × 200 then 429 —
     the half the derived harness dropped); (ii) a failure that lands AFTER the grace window (the 200 went out as "pending", the send
     then rejects) → refunded; (iii) **a throwing `putOtp` → budget spent (READ prediction) — measure and grade against gate 2's
     C-F3, which named it**; (iv) the refund removes exactly ONE hit: two requests from one source in the same millisecond, one fails
     → one hit remains; (v) the refund cannot over-refund: a refund after the hit already aged out of the window, and a refund for a
     key the sweep deleted → no negative count, no throw; (vi) a hostile pattern — a caller who can make sends FAIL at will (e.g. an
     address whose mail bounces synchronously in the provider) gets unlimited attempts? READ what makes `mail.send` reject for a
     given address in the real provider (`lib/mail.js`), measure with the fake, grade.
3. **Gate 2's C harness legs, re-run on C's pinned head (MEASURED):** COPY gate 2's `qa-harness-c-budget.mjs` and
   `qa-harness-c-login.mjs`; derive YOUR OWN contract copy for the round-2 text and refund, and **quote YOUR diff against gate 2's
   original**. Then **verify the builder's DERIVED copy claim:** COPY the builder's file (path in §1; it is ephemeral — if it is gone,
   say so and the claim stays UNVERIFIED) into your evidence, `diff` it against gate 2's original, and state whether the change is
   EXACTLY the contract change (the two message constants and the failed-send converse) and nothing else — and whether its new q3
   check is weaker than the contract (it asserts 7 × 502 only; drafter READ). Legs: q1 per source, q2 global, q3 refusals spend
   nothing + BOTH converses, q4 window slides, q5keys + q5e2e (XFF forgery, header shapes, IPv6 /64, hex-mapped bucket), exhaust
   (20,000 keys), conc (50 concurrent → exactly 6), shapes.
4. **The FULL H harness on C's pinned head (MEASURED):** C's tree contains H (main `49d7027` ⊃ `c8fb771`). COPY gate 2's
   `qa-harness-h.mjs` + `qa-lib-h.cjs` + `H-advanced-ids.json` (+ `qa-harness-h-a1.mjs`) and run ALL legs — access (creator 200,
   stranger 404 byte-identical to not-found/malformed/expired/pending, 401s with 0 store reads), the reopen limiter (30 per session
   per 10 min, 429 + `Retry-After`, decided before the lookup), the enum/number legs, the purge, the four C-minors, and the A1 leg.
   The builder claims "the FULL H harness passes (was 1 FAIL)" — the 1 FAIL was the limiter leg at `4b946d0` (the clock split).
   Quote your pass counts beside gate 2's H counts. **H-F3 on C's head:** a new sign-in now costs an OTP under C's budgets — measure
   what a limiter reset costs (sessions per source per hour).
5. **ADVERSARIAL PASS (C) — state the FAIL condition before each.** FAIL = more than 6 codes an hour reach the mail recorder for
   what is really one source, a legitimate distinct source refused, a budget that can be reset or refunded by the caller, or a
   server that boots with an invalid budget.
   - Everything gate 2's q5 ran (XFF forgery with rotating LEFT entries → one key; trust off → socket; header shapes that mint keys →
     the global 20/h still holds; IPv6 inside one /64; hex-mapped `::ffff:0102:0304` bucket; key-map exhaustion) — re-run, compare.
   - **Refund abuse:** can any request shape produce `"failed"` without spending the provider (a malformed address that passes the
     route's regex but the provider rejects instantly)? If so, it is a free retry loop — measure against the fake and READ the real
     provider; grade.
   - **Clock:** a request whose handling spans a clock step (inject a clock that moves between calls) — the refund uses the SAME
     `now` the record used (READ: yes); confirm.
6. **Login-page strings (MEASURED):** in a real browser (egress-blocked wrapper) against your harness, trigger each 429 and capture
   the page's message VERBATIM (screenshot + `textContent`), 1280 and 375 px. `login.html` has no dark theme — say so again. Quote
   both lines exactly as rendered.
7. **Suites, in YOUR tree at C's head:** `stage3/` `npm test` (builder: 97/97), `npm run test:print`, `npm run test:xlsx`, root
   `node --test` (pricing). **Red-proofs:** per item 2 above, plus gate 2's (`parts[0]` for the rightmost; budget checks after
   `putOtp` — does the new C-F3b cell redden now? gate 2: 67/67 GREEN; the `/64` truncation removed).
8. **C × main `51e9286` (PROBED):** C needs a SECOND forward merge. `merge-tree` `bcef8f7` × `51e9286` from YOUR object dir
   (drafter: **CONFLICT in `stage3/test/server.test.mjs` only; `stage3/server.js` AUTO-MERGES**). Archive the merge RESULT tree,
   and on it (never hand-resolve the test file — do NOT run `npm test` there) run YOUR harnesses against the auto-merged server file:
   the C budget legs, the H harness, D's header matrix (`qa-harness-d-http.cjs`: all six headers on every response class,
   including C's 429s and the new boot path), and E's logout cells. Say whether the auto-merged server file is semantically sound
   (C's options beside H/J/D/E/F/I's; one `clock`). This is PROBED evidence about the tree the builder will produce, not a GO on it.

## 4. TARGET B — S-2 ROUND 2 (TIER 1, NARROW)
**NEVER contact ntfy.sh — or any ntfy host.** Every push is captured by a `fetch` stub installed BEFORE the dispatcher module is
required, with `NTFY_SERVER=http://ntfy.invalid` set before the require (read at require time); the stub THROWS on any URL that
is not `http://ntfy.invalid/…`. Record every process's outbound connections (§13.3).
1. **Scope, mechanically (READ):** `git diff --stat fb23f64 479c3a2` = `test/db/reminder-push.test.js` only; **byte compare of
   `server/reminders/dispatcher.js`**: `git rev-parse fb23f64:server/reminders/dispatcher.js 479c3a2:server/reminders/dispatcher.js`
   equal (drafter: both `283be27…`) AND `cmp` of the two files from your archived trees; the same for `docker-compose.yml` and
   `DEV-SESSION-SUMMARY.md`. Quote. `buildDigest` (READ `server/feedbackDigest.js` at `479c3a2`): confirm it calls the app's own
   `ensureFeedbackTable` and has no side effect a test cares about (does it SEND anything? it must not publish a push inside
   `before()`— check your stub's capture count before the first cell).
2. **`test:db` on a FRESHLY CREATED database — and PROVE it is fresh:** create `vsp_qa_g3_<epoch>_test` (the name MUST end in
   `_test`), and BEFORE the run query `information_schema.tables` (or `to_regclass('public.feedback')`) and quote that `feedback` does
   NOT exist and the DB has zero user tables; run `npm run test:db` → all files green (builder: 5/4/6/17); quote per-file counts.
   Then a SECOND fresh DB, same result (gate 2 reproduced B-F1 3/3 on 2 fresh DBs — reproduce the fix the same way). **Red-proof:**
   in a parse-checked copy with the one added `await buildDigest();` line removed → on a fresh DB the digest cell fails with
   `relation "feedback" does not exist` (gate 2's exact failure). A reused DB (run twice on the same DB) stays green.
3. **The push harness with the topic SET and UNSET (MEASURED):** COPY gate 2's `qa-harness-b-push.cjs` (+ `qa-harness-b-parse.cjs`)
   and run it at `479c3a2` on YOUR fresh app DB `vsp_qa_g3_<epoch>`: topic set to a FAKE value inside your harness process → every
   push (three rules, a manual reminder via the real `POST /api/reminders`, a `user` + `channel:'email'` row with no
   `recipient_email`, huge id, 10 KB title) carries only `Reminder #<id> due` / `Open the Vision Sales Portal (PRO dashboard →
   Reminders) to read it.`; no probe value in any URL/header/body; topic unset → no request at all. Quote the counts beside gate 2's
   31/31. The HTML parse of the client-reminder mail (item 4's escaping) unchanged.
4. **File order (READ + PROBED):** gate 2 warned that once S-1 (A) is on main, `feedback-auth.test.js` creates the feedback table
   first and would MASK B-F1. Run B's `reminder-push.test.js` ALONE (`node --test test/db/reminder-push.test.js` with the repo's
   test-db env) on a fresh DB → green by itself.
5. **B × main `f065675` (PROBED):** `merge-tree` `479c3a2` × `f065675` (drafter: CLEAN, rc 0). Archive the result, `npm ci --offline
   --ignore-scripts`, `npm test` and `test:db` on a fresh `_test` DB, and the push harness on it. This is the tree B's forward merge
   produces (it should be identical in content to the builder's merge — say what the builder must re-run).

## 5. TARGET K — item-1 follow-ups (TIER 2, through-code)
**Drive `createApp` in YOUR harness (gate 2's `qa-harness-h-a1.mjs` / gate 1's A1 harness method, COPIED), fake mail that records,
real `/auth` routes to sign in.**
1. **A1-F2 matrix (MEASURED), QuickQuote at `a33f87e`:** each env shape in a FRESH child process whose env you build (`env -i`
   allowlist + only the variable under test): neither → the default (To `kreiser.org@me.com`, CC `tuesday-agent@agentmail.to`);
   `_EMAILS` only; `_EMAIL` only; both (different lists) → which wins; `_EMAIL=""` + valid `_EMAILS`; `_EMAIL=" , "` / `" "` + valid
   `_EMAILS` → boot throws?; `_EMAILS=" , "` alone → throws?. Quote To/CC per case and every boot error verbatim.
   **The same matrix on the PORTAL at main `f065675`** (`server/feedbackNotify.js` `notifyRecipients` / `assertNotifyConfig`, called
   in YOUR harness, never the entry point) — table the two apps side by side and grade the opposite precedence.
2. **A1-F1 (MEASURED):** the builder's cell passes; your own: a `send` that never resolves → the POST returns 201 within its
   deadline, the item is stored, the process keeps serving; a `send` that rejects; a `send` that throws synchronously. **Red-proof:**
   a parse-checked copy where the route `await`s the feedback send → the builder's cell FAILS in ~2 s (not a hang: time it, deadline
   it) and exits non-zero; the test FILE still exits on its own.
3. **Suites at `a33f87e`:** `stage3/` `npm test` (builder 59/59), root pricing (67/67). Red-proof for A1-F2: the plural dropped.
4. **K × main `51e9286` (PROBED):** `merge-tree` (drafter: `server.js` auto-merges, CONFLICT `stage3/test/server.test.mjs`). On the
   merge RESULT's auto-merged server file, run YOUR K matrix and gate 2's H A1 leg (the `createApp` signature both touch). Do not run
   `npm test` there.

## 6. TARGET L — small sweep (TIER 2, through-code)
1. **A-7 (MEASURED):** in YOUR tree at `8271099`, `node strip.js` → the three numbers equal `wc -c` of the three files; at the base
   `1f3df8d` they do not (quote both). The cell's red-proof: `Buffer.byteLength` → `.length` in a parse-checked copy → the cell
   reddens. Note: the cell RUNS `strip.js` (it writes `stage3/public` and `stage3/private` inside the tree) — fine in your tree.
2. **A-8 (MEASURED):** `GET /favicon.ico` → 204, empty body, no session; `HEAD /favicon.ico`; `/favicon.ico?x=1`; `/FAVICON.ICO`;
   a signed-in request; and on the §12 merge result (which carries D's headers) → all six security headers present on the 204.
3. **A-10 (MEASURED, a REAL browser):** drive the hosted page (strip.js output of YOUR tree) against YOUR harness, advanced session
   unlocked (unlock word you generate), a PoC quote, the quote emailed through the real collector: capture the POSTed JSON body.
   At the base `1f3df8d`: `toggleAdvanced`, `toggleDarkMode`, `advWord` (with the unlock word typed in it), `fbMsg` (with a draft
   typed) are posted, and the server logs `QUOTE MISMATCH — ticked but not rendered: … toggleAdvanced` (gate 2 reproduced this).
   At L: none of the four is posted, no QUOTE MISMATCH line, and **everything else the collector posted at the base is still posted**
   (diff the two bodies key by key; `toggleAllowOptOut` present). The quote itself (PDF text via `pdftotext`, xlsx rows) identical
   between base and L for the same inputs. **Where did `advWord` go at the base (READ + MEASURED):** logged? stored in H's reopen
   state (H's allowlist — READ `stateJson` building on main)? rendered? The HPAM word riding with every quote is a finding against
   MAIN (pre-existing); say what L closes. **Also the POSITIVE case:** a REALLY dropped PoC still logs `QUOTE MISMATCH` at L (the
   `cleared` guard is untouched — prove it fires with a crafted state).
   The only builder cell for A-10 is a source regex — say plainly that no cell drives the collector, and whether one should.
4. **Suites at `8271099`:** `stage3/` `npm test` (builder 60/60), `test:print` (18/18), `test:xlsx` (5/5), root pricing (67/67).
   Red-proofs: each of A-7, A-8, A-10 reverted alone in a parse-checked copy → its cell reddens.
5. **L × main `51e9286` (PROBED):** `merge-tree` (drafter: CONFLICT `stage3/test/server.test.mjs` AND `stage3/test/strip.test.mjs`;
   `server.js`, `strip.js` auto-merge). On the merge result's auto-merged product files, run the A-8 and A-10 legs (the collector
   now sits beside E's Sign out and H's stored:false note in `HOSTED_EXTRAS`). Do not run `npm test` there.
6. **Version (READ):** say whether K or L needs a `toolVersion` bump under QuickQuote's `CLAUDE.md`, and how that interacts with N's
   2.32.

<!-- SLOT-M:BEGIN -->
## M. TARGET M — D-F1 header-order cell (TIER 2, test only) — present because SLOT-M: IN
1. **Scope:** `git diff --stat 51e9286 0ab83e1` = `stage3/test/server.test.mjs` only (+21). No product file changes.
2. **The cell is GREEN on the clean tree and RED when the middleware order is swapped (MEASURED):** in YOUR tree at `0ab83e1`,
   `stage3/` `npm test` (builder 89/89). Mutant (parse-checked): move `app.use(express.json({ limit: "256kb" }))` ABOVE the header
   middleware (gate 2's MUT-afterjson) → the D-F1 cell FAILS on the RUNTIME assertions (quote which assertion fires first), not only
   the source-order one. Second mutant: keep the order but rename the CSP key string in the source so the source-order check's first
   `indexOf` returns −1 → is the source-order half still meaningful (drafter READ: vacuous)? Third: a mutant that drops only
   `Strict-Transport-Security` from the middleware → does any cell redden (the D-F1 cell checks 4 of 6 headers)? Grade.
3. **Byte-exact headers on the 400 and 413** from YOUR harness (gate 2's `qa-harness-d-http.cjs`) at `0ab83e1` — the six headers
   match every other response class.
<!-- SLOT-M:END -->

<!-- SLOT-N:BEGIN -->
## N. TARGET N — A-6 phone layout (TIER 2, CUSTOMER-VISIBLE) — present because SLOT-N: IN
**Screenshots from YOUR OWN renders, never the builder's.** Chrome through YOUR egress-block wrapper; a fresh browser context per case;
the theme set by clicking `#toggleDarkMode` and a settle wait of ≥ 600 ms (the builder's first set was voided by a 150 ms wait).
1. **Before/after at 320, 375, 390 px, light AND dark (MEASURED):** both builds — the offline `index.html` from `file://` and the
   hosted page (strip.js output served by YOUR harness, signed in, so the masthead carries E's Sign out) — at the BASE `51e9286` and at
   N, states default and heavy (the builder's heavy recipe in `phone-layout.mjs`) and heavy-advanced (offline). For each: page
   `scrollWidth` vs `clientWidth`; **no clipped app price, no off-screen or clipped ticket value** (every `.ticket table.lines
   td:last-child` and every `.app-row .price` fully inside the viewport AND its panel); **the masthead** (outside `main` — the cell
   does not look there): the logo, settings cog and Sign out not clipped/overlapping at 320; no text truncated by `text-overflow`;
   no wrapped row overlapping the next (bounding boxes). Save full-page PNGs into YOUR evidence; name any element that fails.
   **Compare your AFTER set with the builder's 12 AFTER PNGs** (visually, and pixel-diff where the renders are comparable) — same
   layout or not.
2. **Desktop identity (MEASURED):** 1280 px (and 768, 921), light and dark, default and heavy, both builds: YOUR base render vs YOUR
   N render → **pixel-identical** (quote the differing-pixel count; 0 expected). Note 921 is just above the 920 breakpoint and 768 is
   inside it (the `minmax(0,1fr)` change applies at 768 — "identical" there is a claim to measure, not assume).
3. **Print unchanged (MEASURED):** the printed quote as a real A4 PDF (`format: "A4"`, the print media path the tool uses) at the base
   and at N, default and heavy, light and dark page theme: `pdftotext` text identical and a rasterised pixel compare of every page
   (0 differing pixels expected); and the EMAILED PDF from the server renderer (stage3 `lib/pdf.js`, renderer egress blocked) at base
   vs N → text identical, page count identical. N adds no `@media print` rule — confirm the new 480 px block is `screen`-scoped so a
   narrow print viewport cannot trigger it.
4. **The version (READ + MEASURED):** `toolVersion` 2.32 reaches the on-screen badge and every generated document footer (PDF and
   xlsx) — quote the footer line from a real PDF; the BACKLOG entry closed. Say whether 2.32 collides with anything else queued (K/L
   carry no bump; C carries none).
5. **The gate file (MEASURED):** `node --test stage3/test/phone-layout.mjs` alone at N → 15/15, and the process exits on its own
   (time it); at the base with N's test file copied in → 15/15 FAIL (the builder's claim). Red-proof: revert only the `minmax(0, 1fr)`
   line (parse-safe: CSS, no `node --check` applies — say so) → which cells redden; revert only the 480 px block → which cells redden
   (does the cell catch a CLIP, or only the page overflow?).
6. **Suites at N:** `stage3/` `npm test` (builder 88/88), `test:print` (44/44), `test:xlsx` (5/5), root pricing (67/67).
7. **Adversarial (state the FAIL condition first):** FAIL = any money figure or app price hidden, clipped or off-screen at a
   supported phone width, or any desktop/print pixel changed. Widths 321, 360, 414, 430, 480, 481, 540 and 920/921; zoom 200 % at
   390; a 60-character unbroken customer name; the largest currency amounts (DKK, 950 devices, 5 years); POA tails in the services
   result. Widths below 320 are the builder's stated NOT TESTED — record, do not grade.
<!-- SLOT-N:END -->

## 12. Across targets — merges and the queue
**Every prediction below is the drafter's own scratch `merge-tree` (own object dirs under the drafter's scratchpad, 21:2x AEST,
run under bash). Quote `git merge-tree --write-tree --name-only` from YOUR OWN object directory for each pair, or say you skipped it.**
The builder merges each forward at merge time; your job is to say which pairs conflict and which cells must be re-run on each
merged head — never to resolve a conflict.

| pair | drafter's scratch result |
|---|---|
| C `bcef8f7` × main `51e9286` | **CONFLICT `stage3/test/server.test.mjs`**; `server.js` auto-merged (result tree `ec7d5a9…`) |
| K `a33f87e` × main `51e9286` | **CONFLICT `stage3/test/server.test.mjs`**; `server.js` auto-merged |
| L `8271099` × main `51e9286` | **CONFLICT `server.test.mjs` + `strip.test.mjs`**; `server.js`, `strip.js` auto-merged |
| M `0ab83e1` × N `ac0a8d2` | clean (rc 0) |
| M × C, K × C, L × C, K × L, N × C, N × L, M × K, M × L, N × K | **CONFLICT `server.test.mjs`** each (N × L and M × L also `strip.test.mjs`) — every QuickQuote target appends to the same test tails |
| B `479c3a2` × portal main `f065675` | **clean (rc 0)** |
| B × S-1 `89af8ba` (context only) | CONFLICT `BACKLOG.md` only |
| S-1 `89af8ba` × `f065675` (context only) | CONFLICT `BACKLOG.md` only |

- **Do NOT hand-resolve any conflict.** For each CLEAN pair (B × main, M × N), archive the merge RESULT into your project and run that
  repo's `npm test` on it (PROBED). For the conflicted-in-tests-only pairs with a target (C, K, L × main), run YOUR harnesses on the
  auto-merged product files as §3.8 / §5.4 / §6.5 say — never `npm test` on a tree with conflict markers.
- **A GO is a GO at the pinned sha only.** Name, for each target, the cells to re-run on its merged head (at least: C — the whole C
  harness, the full H harness, D's header matrix, E's logout cells and M's D-F1 cell on the forward-merged tree; K — the K matrix +
  H's A1 leg; L — A-8 headers + the A-10 collector leg beside E and H in `HOSTED_EXTRAS`; M, N — whichever merges second re-runs the
  other's cells; B — `test:db` on a fresh DB + the push harness on the merged tree). **CI:** `gh` is not authenticated for
  `datasecau`; every target's CI half is **NOT RUN**, measured at merge.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (`session-tools/nexusai-lock.sh`).
1. **The Vision builder seat is LIVE** (claude `1613`, pane `%41`) and owns portal `:4848` and stage3 `:8080`. **Never use 4848 or
   8080**, nor `47787` (Tuesday's dashboard), nor any port another seat holds. Take every port from the kernel (listen on 0) and bind
   `127.0.0.1` wherever YOUR harness listens. Never start the portal's entry point (it binds `0.0.0.0` in `main()`).
2. **Postgres = the running local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all.**
   Create `vsp_qa_g3_<epoch>` for app runs and `vsp_qa_g3_<epoch>_test` as `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs; the name
   MUST end in `_test` — the portal's guard; never point it at `salesportal`, `salesportal_test`, any `vsp_qa_g1_*` or `vsp_qa_g2_*`
   database, or the builder's `vsp_bf1_*`). The connection uses the repo's LOCAL defaults in `server/db.js` /
   `scripts/ensure-test-db.js`; never anything from `Vision_Sales_Portal/4_Credentials/`. Use the `pg` client from YOUR
   `node_modules` (no `psql` here). If `:5433` does not answer, the portal runtime legs are **NOT RUN, blocker named** — do not start
   a container. Leave your databases in place and list their names (no DROP).
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH, HOME = a fresh mktemp dir, TZ, NODE_ENV = `test`
   or `development` — never `production` — PORT, a fresh random SESSION_SECRET / unlock word / `COORDINATOR_SECRET` you generate,
   DATABASE_URL / TEST_DATABASE_URL = yours, PUPPETEER_EXECUTABLE_PATH, `NTFY_SERVER=http://ntfy.invalid`, dummy provider values,
   `npm_config_update_notifier=false`, `npm_config_offline=true`). **NEVER set in a product process:** `AGENTMAIL_API_KEY`,
   `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product
   process's env KEY NAMES (never values) and assert none is forbidden.
   **Egress — including Chrome children:** the real QuickQuote renderer's page calls three public FX APIs whenever currency ≠ USD
   (gate 1 O-4). **Block it** — gate 2's `qa-chrome-egressblock.sh` (COPY it) as `PUPPETEER_EXECUTABLE_PATH`, i.e.
   `--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1 , EXCLUDE localhost` plus `--log-net-log` per launch (or request
   interception on every page the renderer opens) — and **prove the block with a positive control** (one renderer page's FX fetch is
   attempted and fails, recorded). Record outbound connections of EVERY process you start, Chrome children included (`lsof -nP
   -iTCP` over the whole process tree, not just node, plus the net-log scan). Anything but `127.0.0.1` is a finding against your
   harness or the product (your own `git ls-remote` head readings and your verdict mail are the only expected external calls — say so).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND an entry point of
   either app (the portal's server entry file, the stage3 server file, or your own harness file) ANYWHERE in the remaining argv,
   from the kernel; **"ours" = the ancestor chain CONTAINS your claude pid**. Chrome children of your renderer count as yours and
   must be reaped. **Negative controls, same run, must classify FOREIGN:** the Vision builder's claude `1613` (pane `%41`), Tuesday's
   claude `45678` (pane `%0`), and the NexusAI seat's claude `8360` (pane `%44`). Re-read them at start; if one has exited, say so and
   use the others (gate 2's QA seat `86858` has exited). Never by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. Method:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorcount.py`
   (with `qa-floorlib.sh`), or gate 2's Vision copy (`…/2026-09-22-vision-qq-gate2/evidence/qa-floorcount.py`) — COPY either into
   your own evidence folder; edit neither original. **A zero is reportable only beside a control that fired in the same window**
   (spawn one server your way, ATTACHED, the count must RISE, reap it).
5. **THE DEADLINE RULE:** every real-server, browser and database step has a written DEADLINE (boot 60 s, request 30 s, render 60 s,
   DB connect 15 s, exit 20 s) and a client timeout on every request (this machine has no `timeout` binary — build deadlines into your
   own runner); a step past its deadline is ABORTED and reported (a hung product request IS a finding). **Every server, browser and
   child you start is killed in a `finally`** (SIGTERM, then SIGKILL after a grace), confirmed by your counter. **Log a HEARTBEAT
   line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**
   C's key-exhaustion leg, K's hung-mail leg, N's browser matrix and the print compares are the shapes that hang.

**Reap every server and every Chrome you start.** An orphan of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (App Service `hpas-quickquote`, resource group `hpas-quickquote-rg`, its ACR `hpasqqacr`, its Table
  Storage) **or the live portal** (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` —
  PRODUCTION: the live site, its Postgres `datasec-sales-db.postgres.database.azure.com` and key vault). No request to either host,
  no DB connection to either, not even a GET or a health probe. **Never ntfy.sh** or any ntfy host (stub the fetch). **Never the
  three FX hosts** (intercept in your browser; block in the renderer). Never run the portal `.cursor` rule's curl lines. Never the
  Feedback_System coordinator.
- The portal: `createApp()` / module functions in YOUR harness, on LOCAL Postgres, `env -i`. QuickQuote: `createApp` in YOUR harness,
  and the offline `index.html` from `file://`.

### HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npx` of anything not
  already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Real sends are OFF.** Every provider is a recorder you wrote; nothing reaches ACS, Agent Mail, ntfy or an FX host from a product
  process, a renderer or a browser you drive.
- **Findings-only:** do not commit, do not move any branch, do not file a ticket, do not write inside either repo, inside
  `Vision_Sales_Portal/` (including its `5_Project_History/` screenshot folder), inside `Feedback_System/`, inside the builder's
  scratchpad (`/private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-Vision-Sales-Portal/…` — READ and COPY only), or
  inside gate 1's or gate 2's report folders. The gate fixes nothing.
- **NEVER `rm`** — quarantine, per the template §5; every preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate3/report.md`

**Questions:** your sender `QA/Datasec-Vision` has NO inbox routing line in the fleet — you cannot receive an answer reliably. If
you must ask, mail `tuesday-agent@agentmail.to`, subject `[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one
Question / Meanwhile / Needed-by), **and proceed on the safest reading without waiting**; record the question and the reading you
took in the report.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 3: A-1 round 2 + S-2 round 2 (tier 1) + item-1 follow-ups + A-7/A-8/A-10 + D-F1 + A-6 (tier 2), heads as pinned at launch`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the QA
project has none. Use it ONLY in your own verdict/question `curl` (with a client timeout, e.g. `-m 30`); it must never enter a
product process's environment (§13.3). Never put the key, or any secret, in a mail or the report.

Verdict format:
- **C (A-1 round 2), B (S-2 round 2), K (item-1 follow-ups), L (A-7/A-8/A-10)** — and **M (D-F1)**, **N (A-6)** if IN — each
  **GO / NO-GO**, stated SEPARATELY PER TARGET, each naming its pinned sha and branch. For C, state separately: the forward merge
  `4b946d0` proved union-only or not; each of C-F1/C-F2/C-F3 closed or not (C-F3 in BOTH halves: failed send, throwing `putOtp`); the
  builder's derived-harness diff exactly the contract change or not. For B, state whether B-F1 is closed on a DB you proved fresh.
- The verbatim strings Kam's publish ask needs: C's two refusal lines **as the login page renders them**; B's push title and body;
  N's before/after description for the screenshots (what a phone user sees differently) and the 2.32 footer line; L's A-10 change in
  one sentence a non-engineer can read (what the page no longer sends).
- Then one paragraph on the queue quoting §12's merge-tree results (or that you skipped them): which GO survives which merge order,
  which cells must be re-run on each forward-merged head, and that every target's CI half is NOT RUN (gh unauthenticated).
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section — at least: real App Service `X-Forwarded-For`
  (C's defence rests on it), C's boot refusal inside the real entry point with real Table Storage, real ACS/Agent Mail/ntfy delivery,
  the live ntfy topic's value (B), CI (B's fresh-DB CI run above all), real phones / Safari / Firefox / widths below 320 (N), the
  real Docker image, Node 20 (this machine runs node v26; both apps ship on Node 20/22), multiple replicas (C's budgets and H's
  limiter are per container), every target's forward-merged head (only PROBED on auto-merged product files)). Every action
  recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY. §3 Q1-Q5, §3 Q8, §4 Q2-Q3, §4 Q5, §5 Q1-Q2,
  §6 Q3 and (if IN) §M Q2, §N Q1-Q3 must each carry one.
- Report each pinned head, and both mains, as three timestamped readings (start / mid / end), each with its branch name.

PROVENANCE:
- heads: portal main f065675c3a0d…, fix/reminder-push-redaction-2026-09-22 479c3a20291e…, integration/portal-gate2-2026-09-22 289e2d9545ae…, fix/feedback-report-auth-2026-09-22 89af8ba7817f… (NOT a target); QQ main 51e92867930e…, feat/qq-otp-send-budget-2026-09-22 bcef8f7dbc83…, fix/qq-feedback-followups-2026-09-22 a33f87ea1e3e…, fix/qq-small-sweep-2026-09-22 82710998d307…, fix/qq-d-f1-header-order-2026-09-22 0ab83e1ec52d…, fix/qq-phone-overflow-2026-09-22 ac0a8d2536a8… | `git -C <repo> ls-remote origin` + `cat-file -t` (all = commit) | read 2026-09-22 21:13:48 and 21:15:39 AEST
- chains: 479c3a2 → fb23f64 → 289e2d9 (in main f065675 = merge(ef5a9c0, 289e2d9)); bcef8f7 → e7a43a4 → 792c5d5 → 8cbb39b → 4b946d0 = merge(3c8d3a4, 49d7027); 49d7027 = merge(72fe46d, d2071c9) (J); 72fe46d = merge(1f3df8d, c8fb771) (H); 51e9286 = … merges of D 7626f6a, E d1524d3, F 17390aa, I a2fa00d; a33f87e and 8271099 (b95cdf6 → 6091305 → 8271099) on 1f3df8d; 0ab83e1 and ac0a8d2 on 51e9286 | `git log --format='%h %p %s'`, `merge-base`, `rev-list --count` | read 21:14-21:20
- file sets / numstat; lockfile blobs 9d426df (portal) and 64e49cb (stage3) unchanged at every target; dispatcher.js blob 283be27 at fb23f64 == 479c3a2 | `git diff --stat`, `git rev-parse <sha>:<path>` | read 21:14-21:25
- mechanisms, strings, line numbers; portal feedbackNotify.js:34 precedence; QQ server.js createApp signatures; express.json limit; toolVersion 2.31 at 51e9286:index.html:1655; test counts per commit | `git show <sha>:<file>`, `grep -c '^test('` | read 21:15-21:35
- merge-tree table §12 and the 4b946d0 auto-merge comparison (tree 76a7b06 vs d6c4b8f) | scratch `GIT_OBJECT_DIRECTORY` under the drafter's own scratchpad + alternates, run under bash (the drafter's first batch under zsh was VOID — the gate-2 S-2 trap) | read 21:2x
- builder's derived C harness: diff vs gate 2's `qa-harness-c-budget.mjs` (2 comment lines added, 3 lines changed), its run log `C-budget-contract.log` (43 checks, 0 fails; putOtp converse [500×6, 429]) | `diff`, `shasum`, `grep` on the builder's scratchpad (READ only) | read 21:17-21:22
- N: phone-layout.mjs read whole (15 cells = 9 + 6); the screenshot folder listed (24 PNG + README); `git diff 1f3df8d 51e9286 -- index.html` empty | `git show`, `ls`, `sed` | read 21:25
- seats: %41 → claude 1613 (Vision), %0 → claude 45678 (Tuesday), %44 → claude 8360 (NexusAI), %36 → 57419; gate 2's QA 86858 exited; :5433 listening (docker) | `tmux list-panes -a`, `ps -axo pid,ppid,comm`, `lsof` | read 21:26
- builder claims / READY times / Tuesday's rulings | Tuesday daily note `0_Brain/daily_tuesday/2026-09-22.md` 19:59-21:13 lines; Tuesday's 21:15 slot instruction (mail bodies NOT read)
