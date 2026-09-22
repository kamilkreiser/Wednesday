# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, BATCHED GATE 4 (portal + QuickQuote): N = A-6 ROUND 2 of 2 phone layout (TIER 2, CUSTOMER-VISIBLE), CF5 = C-F5 + C2-F2 provider-only refund (TIER 1), I9 = item 9 QuickQuote error log carries no body (TIER 1), I10 = item 10 portal 413 pass-through (TIER 2), Q5 = item 5 qs advisory (TIER 2, dependency), P5B = item 5b puppeteer 25 + node 22 (TIER 2, PRODUCTION RUNTIME), FU = SLOT for the gate-3 follow-ups K-F1 / L-F1 / M-N2 (+ K-O1) (TIER 2, tests only)

**Drafted for Tuesday 2026-09-22 22:50-23:20 AEST by a read-only drafting agent; Tuesday reviews, re-checks the pre-filled PIN table, stamps and launches.**
Commissioned on the Vision_Sales_Portal agent's READY mails as Tuesday's daily note records them (item 9 11:41Z; item 10 11:46Z;
item 11 = items 5 and 5b 11:58Z; C-F5 12:35Z; N round 2 12:48Z; the gate-3 follow-ups 12:52Z) and Tuesday's commission of ~22:50
plus the ~22:53 message that filled slot FU. **The drafter did NOT read the mail bodies** (no AgentMail call in a read-only
commission): every builder claim below comes from commit messages, code comments, the builder's BACKLOG, the builder's screenshot
README, Tuesday's daily note or gate 3's report, and is a CLAIM.
**EVERY HEAD WAS PRE-FILLED BY THE DRAFTER FROM `git ls-remote origin` (both repos 22:50:41 AEST; FU 22:53:21 AEST; each
`cat-file -t` = commit); THE LAUNCHER RE-READS THEM ALL.** If any head moves before launch, Tuesday edits its row; the launcher
parses §PIN, refuses any placeholder, and re-reads EVERY head by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-22 23:06
Self-check note: Tuesday read the drafter report whole (10 wrong-at-source items accepted: the P5B branch name; FU is 2 commits incl. K-O1 and one package.json line; the M-N2 split mutant; the N commit self-contradiction, settled by a single-line revert; npm audit replaced by a read-only substitute; the CF5 refund cap also limits the putOtp-throw refund and a long outage, to be graded; decision 14 still open; Node 20 not tested; Q5 and P5B lockfile consistency; the slot-marker bug fixed). Target sections were read by headline; Tuesday wrote the commission.

SLOT-FU: IN
*(Filled `IN` by the drafter on Tuesday's ~22:53 message ("Fill slot FU IN … @ 78aa156"). If Tuesday flips it to `OUT`: set the
PIN row FU's status to `OUT` with `-` in head/base/commits, DELETE BOTH `SLOT-FU:BEGIN`..`SLOT-FU:END` marked sections (§1 and §FU) from
this brief AND the `[SLOT-FU BEGIN]..[SLOT-FU END]` block from the prompt. The launcher refuses the placeholder and any
inconsistency between the SLOT line, the row and the two blocks.)*

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build any of these changes and you owe no builder anything. **Every line below that reports
what a builder says is a CLAIM, never evidence.**

**ONE batched gate, SIX targets + ONE slot, TWO repos, ONE session** (Kam's standing rule of 2026-09-18: batch gates, never
pay for the same setup twice). **Give a SEPARATE verdict for each: N, CF5, I9, I10, Q5, P5B (and FU if IN) — each GO / NO-GO,
each naming its pinned sha.**
**⚠ Letter collision:** this gate's TARGET letters are NOT the builder's item names. N = the builder's A-6 (round 2); CF5 = gate 3's
C-F5 (= C1-F1 = C2-F1) + C2-F2; I9 = the builder's "item 9" (QuickQuote); I10 = the builder's "item 10" (portal); Q5 = "item 5"
(QuickQuote qs); P5B = "item 5b" (puppeteer 25 + node 22); FU = gate 3's K-F1 + L-F1 + M-N2 (+ K-O1). Always write both (e.g.
"CF5 (C-F5)", "N (A-6 r2)"). **Also:** the builder's decisions pack calls C-F5 "tightening item 9" (its publish list numbers the
sign-in limits 9) — that is NOT this gate's I9. Say which you mean every time.
Tiers:
- **N (A-6 round 2, phone layout) is TIER 2, CUSTOMER-VISIBLE**, and **ROUND 2 of 2: the cap — a second NO-GO ships nothing**
  (the phone layout leaves the publish entirely; say so plainly if you grade NO-GO).
- **CF5 (C-F5 + C2-F2, provider-only refund) is TIER 1**: the sign-in mail budget, the refund rule, a new per-source cap, and the
  mail module's error shapes.
- **I9 (item 9, QuickQuote error log) is TIER 1** (privacy: the HPAM word, OTP codes and customer names in the container log).
- **I10 (item 10, portal 413 pass-through) is TIER 2**, through-code.
- **Q5 (item 5, qs advisory) is TIER 2**: dependency, lockfile only.
- **P5B (item 5b, puppeteer 25 + node 22) is TIER 2**: a PRODUCTION RUNTIME CHANGE (base image and PDF engine). Kam's decision 14
  holds it: a GO here only means it is TESTED for when he decides; it ships nothing.
- **FU (gate-3 follow-ups, tests only) is TIER 2**, through-code — present only if SLOT-FU is IN.

**NOT IN THIS GATE — portal S-1** (`fix/feedback-report-auth-2026-09-22` @ `89af8ba`) was **GO at gate 2** and still waits on Kam's
card. Do not gate it; do not re-open it. §12 names it as context only. **Also not in this gate:** C, B, K, L, M (GO at gate 3 and now
ON main — portal `aeadcc1` = B merged; QuickQuote `763269d` = M, C, K, L merged, in that order).

## RULED BY KAM, AND SETTLED (Vision `1_Project_Definition/CLARIFICATIONS.md`)
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` — read it whole
(C-01..C-05 at drafting; no new entry since gate 3).
- **No C-entry covers any target here.** Their authority is the Vision agent's own security/backlog sweep, commissioned by Tuesday,
  and **Tuesday's ruling on C-F5** (daily note 22:37 and the Vision READY 12:35Z: "refund only provider-wide failures, never a
  per-recipient rejection; a per-source refund cap (6/h); a cell failing if only the global refund is dropped"). **No product choice
  in them is Kam's ruling** (CF5: the 6/h refund cap, and that the cap ALSO covers a throwing `putOtp`; the unchanged 502 text for a
  rejected address; N: the phone layout itself and the 600 / 359 px breakpoints; I9 / I10: the log wording): report each as the
  BUILDER's choice (or Tuesday's, for the C-F5 rule) and say whether it needs Kam.
- **Kam's pending decisions that bound this gate** (`Vision_Sales_Portal/5_Project_History/2026-09-22_kam-decisions-and-publish-pack.md`,
  READ ONLY): **decision 14** (the newer runtime, P5B) is a QUESTION to Kam — "If silent: it waits"; **decision 18** (QuickQuote's
  production logs may hold raw malformed bodies until I9 ships; Kam: let them expire) — never query any production log. The pack
  lists N, CF5, P5B, Q5 and I9 as "NOT in this publish".
- The QuickQuote repo's own rules: `Quoting Tool/hpas-quoting-tool/CLAUDE.md` (single offline HTML file; **version discipline**
  §"Version discipline"; **always verify print as a real PDF**; nothing in the sub-project goes near Azure). Read it.
- Deploys are HELD for Kam. Nothing here merges on your word.

## PRIOR ROUND
- **Gate 3's report is ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate3/`
  (`report.md` + `sections/` + `evidence/`). Read its VERDICTS, FINDINGS INDEX, NOT TESTED, and the C2, K, L, M and N sections.
- **N is ROUND 2 of 2.** Round 1 gated `ac0a8d2`: **NO-GO** on **N-F1 (Major)** — in advanced mode the custom-hours hourly-rate box
  `#price-custom` shrank to 18 / 23 / 38 px at 320 / 375 / 390 (overlapping `#qty-custom` by 5.2 px at ≤ 350; the 390 crop showed
  only `4` of `434`), both builds; **N-F2 (Minor)** — from 481 to 543 px a big quote's services total was cut at the panel edge and
  could no longer be scrolled to; **N-F3 (Minor)** — the gate file did not pin `minmax(0, 1fr)`; **N-F4 (Polish)** — the builder's
  AFTER screenshots were not rendered from the pinned v2.32 file (`V2.31` footer, 1.4010 prices). Round 2 = `ac0a8d2` + a forward
  merge of main `763269d` (`c1abc05`) + ONE commit `54a7202` (§1).
- **CF5 answers gate 3's C-F5** (Minor, needs Kam: a caller-chosen address the provider rejects made failed attempts from one source
  unbounded — 100 × 502 from one source, never 429) **and C2-F2** (Minor: no cell pinned the GLOBAL half of the refund).
- **FU answers gate 3's K-F1** (Minor: a dropped `.catch` on the feedback send stayed green while a rejecting send crashed the
  server), **L-F1** (Polish: A-10's only cell was a source regex), **M-N2** (Polish: HSTS and Referrer-Policy unpinned on the
  parser's 400/413 — a split-middleware mutant stayed 89/89 green), and, in a second commit, **K-O1** (a flaky 40 ms cooldown cell).
- **I9 was found by the builder during gate 3** (brief gate-3 §PIN note: "body-parser SyntaxError bodies logged raw by the generic
  error handler (main 51e9286)"). **I10, Q5, P5B are ROUND 1.**
- **Gate 3's harnesses are REUSABLE BY COPY** (`…/2026-09-22-vision-qq-gate3/evidence/`): `qa-run.py` (the env -i runner WITH gate
  2's fixes: `npm_config_update_notifier=false`, `npm_config_offline=true`, the second-killpg fix), `qa-chrome-egressblock.sh`,
  `qa-egress-monitor.py`, `qa-egress-posctl.mjs`, `qa-netlog-scan.py`, `qa-floorcount.py`, `lockcmp.py`, `lockwalk.py`,
  `mktree-qq.sh`, `mktree-portal.sh`, `qa-mkdb.cjs`, `qa-dbcheck.cjs`; **C:** `qa-harness-c2-budget.mjs` + `qa-lib-c2-stage3.cjs`
  (the contract copy with `ctl.mailMode` / `rejectIf` / `breakPutOtp`, and the `abuse` and `realmail` legs), `qa-harness-c2-d-http.cjs`,
  `qa-harness-c2-login.mjs`, `qa-preload-c2-entry.cjs`, `qa-harness-c2h.mjs` / `qa-harness-c2h-a1.mjs` / `qa-lib-c2h.cjs`;
  **N:** `qa-harness-n-render.cjs`, `qa-harness-n-server.cjs`, `qa-lib-n-stage3.cjs`, `qa-lib-n-png.cjs`,
  `qa-harness-n-probe-{inputs,svcrow,hostedadv,band,stats,shot481}.cjs`, `N-pdfcompare.sh`, `N-redarms.sh`, `N-mktrees.sh`;
  **K:** `qa-harness-k.mjs`, `qa-lib-k.cjs`, `qa-harness-k-portal.cjs`, `K-matrix.sh`; **L:** `qa-harness-l-a10.cjs`,
  `qa-lib-l-server.cjs`, `qa-lib-l-stage3.cjs`, `qa-harness-l-xlsxrows.cjs`; **M:** `qa-harness-m-d-http.cjs`,
  `qa-harness-m-de-server.cjs`, `qa-lib-m-stage3-de.cjs`. COPY what you use into this gate's own evidence folder, read it before
  trusting it, and never edit gate 1's, gate 2's or gate 3's copies. **Self-findings from gates 2 and 3 bind you:** (1) quote every
  path (the project path has a space); (2) **zsh does not word-split `set -- $p`, and zsh reads `$s:stage3/…` as a history
  modifier** — gate 3's forks L and N each voided a tree batch to the first, and this brief's drafter hit the second: run every such
  loop under `bash`; (3) never detach a control server (`( … &)` reparents it to launchd and it counts FOREIGN); (4) the portal
  test-DB name MUST end in `_test` (`test/db/harness.test.js`, `/_test$/`); (5) npm's update-notifier egresses from a fresh HOME
  unless disabled; (6) `file://` pages share localStorage — isolate a browser context per case; puppeteer's default PDF is Letter —
  pass `format: "A4"`; (7) the real renderer calls public FX APIs whenever currency ≠ USD — BLOCK and RECORD them (§13.3);
  (8) gate 3 C2: run `strip.js` in an archived tree BEFORE any real-renderer leg; use the production 4000 ms grace with the real
  `lib/mail.js` (its one in-process retry takes 0.5–1.5 s); (9) gate 3 N: skip sr-only / ≤ 1 px boxes in clip scans, and never
  `scrollIntoView` before a clip screenshot.

## PIN — HEADS (PRE-FILLED BY THE DRAFTER; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
Rules the launcher enforces: every `IN` row has a 40-hex head and base, a commit count, no `@`; head is a commit in its repo;
base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals head NOW; **base is either the same repo's MAIN row head, or another IN row's head in the same repo
(a named stack), or — a STALE BASE — an ancestor of the repo's MAIN row that equals `merge-base(head, MAIN)`** (the row then needs
a forward merge at merge time; the launcher prints a NOTE naming it, and §12 measures it). MAIN rows are re-read by `ls-remote` too.
An `OUT` row carries `-` in head/base/commits; **only FU may be OUT.** **Gated anchors (launcher-checked):** N contains the gated
round-1 head `ac0a8d2` and `c1abc05`'s parents are exactly `ac0a8d2` + `763269d`; CF5's base carries gate 3's gated C-F3 refund
line; Q5 contains `320a169` and `103340c`'s parents are exactly `320a169` + `51e9286`; P5B contains `3d0167e` and `0d45100`'s
parents are exactly `3d0167e` + `51e9286`; FU's `stage3/package.json` delta is exactly the one `test:print` line.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | aeadcc1c5ec0be48790c42e63d9cdd21ee9b223d | - | - | IN |
| MAIN-Q | quickquote | main | 763269d8e910e2dae9a418429d408405e37f164f | - | - | IN |
| N | quickquote | fix/qq-phone-overflow-2026-09-22 | 54a72023c04c676939c8ed219ee96020b9ce2b29 | 763269d8e910e2dae9a418429d408405e37f164f | 3 | IN |
| CF5 | quickquote | fix/qq-otp-refund-provider-only-2026-09-22 | bfb82100aa42772d5c5225811e8ff98f6a31279f | 763269d8e910e2dae9a418429d408405e37f164f | 1 | IN |
| I9 | quickquote | fix/qq-error-log-no-body-2026-09-22 | f2f5f4841ef1241b0e5ae0a443c39f76ae5fc64e | 51e92867930efd4c98b28dc5d95baf82219b3edb | 1 | IN |
| I10 | portal | fix/portal-413-passthrough-2026-09-22 | 515c9f878862fed09b3482edfb074104155308aa | f065675c3a0d9f601a6e2a3041a2cb59d2e11cca | 1 | IN |
| Q5 | quickquote | fix/qq-qs-advisory-2026-09-22 | 103340c6994ba8f1855892eddba46293d61a31da | 51e92867930efd4c98b28dc5d95baf82219b3edb | 2 | IN |
| P5B | quickquote | fix/qq-puppeteer-25-2026-09-22 | 0d451004c746608922ddf874b48ce0f19048bf20 | 51e92867930efd4c98b28dc5d95baf82219b3edb | 2 | IN |
| FU | quickquote | fix/qq-gate3-followups-2026-09-22 | 78aa1567c323f783ff6f2619a135daa1ee1a9947 | 763269d8e910e2dae9a418429d408405e37f164f | 2 | IN |
<!-- PIN-HEADS:END -->

Repos: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`); QuickQuote = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool`
(remote `datasecau/vision_hpas-quickquote`).
**Shape at drafting (READ, 22:50-23:10):** THREE targets sit on current main and FOUR on stale bases. **N, CF5 and FU sit on
QuickQuote main `763269d`** (N via its forward merge `c1abc05`). **I9, Q5 and P5B sit on `51e9286`** (QuickQuote main BEFORE M, C, K
and L merged — Q5 and P5B are `--no-ff` merges of THAT main, not of today's). **I10 sits on portal `f065675`** (main before B's merge
`aeadcc1`). So I9, I10, Q5 and P5B are STALE-BASE rows and each needs a forward merge at merge time (§12). **A GO is a statement
about the pinned SHA only.** If a head moves, its verdict expires.
**Commission corrections the drafter made at source (verify):** P5B's branch is `fix/qq-puppeteer-25-2026-09-22` (NOT
`fix/qq-puppeteer-25`); CF5's full head is `bfb82100aa42…` and I10's `515c9f878862…`; FU is TWO commits of which the second is
K-O1 (the cooldown cells), not an "M pins" commit, and FU also touches `stage3/package.json` (one script line), so it is not "test
files only" in the strict sense (§FU).

## 1. Targets — READ from the object store at drafting (22:50-23:15 AEST)
Drafting shas = the PIN table. **Only Q5 and P5B change a lockfile** (stage3 `package-lock.json` blob `64e49cb` at `763269d`,
`51e9286`, `54a7202`, `bfb8210`, `f2f5f48`, `78aa156`; `70ebda7` at Q5; `cdd7699` at P5B; portal `9d426df` at `f065675`,
`aeadcc1`, `515c9f8`); the launcher re-checks this at the pinned heads. **Every file:line below is at the pinned sha; re-locate by
content if anything moved.** Cell counts (`grep -c '^test('` in `stage3/test/server.test.mjs`): `763269d` 90, `54a7202` 90,
`bfb8210` 95, `78aa156` 91, `f2f5f48` 71 (on `51e9286`), Q5 / P5B 69.

### TARGET N — A-6 ROUND 2 of 2: the tool fits a phone (TIER 2, CUSTOMER-VISIBLE), QuickQuote
- **Chain over its base `763269d` (3 commits):** `ac0a8d2` (the GATED round-1 head, on `51e9286`) → `c1abc05` = merge of main
  `763269d` into N → `54a7202` "v2.32: A-6 round 2 — the advanced rate box stays readable on a phone; big services totals no
  longer clip at 481-566 px". Files over `763269d`: `BACKLOG.md`, `index.html`, `stage3/package.json` (`test:print` adds
  `test/phone-layout.mjs`), `stage3/test/phone-layout.mjs` (A).
- **The forward merge `c1abc05` (drafter's scratch merge-tree, bash):** `ac0a8d2` × `763269d` merges CLEAN, and its auto-merge tree
  `b49d1bc0e07a…` is EQUAL to `c1abc05^{tree}` — i.e. the forward merge is the unmodified auto-merge. Re-measure from YOUR object dir.
- **`54a7202`'s CSS (READ):** the services-result wrap moves from the 480 px block to a NEW `@media screen and (max-width: 600px)`
  block (`.svc-result { flex-wrap: wrap; }` and `#svcSimple .svc-result .amt { white-space: normal; word-break: keep-all; … }`);
  in the 480 px block `.svc-row, .svc-head { grid-template-columns: 1.1rem minmax(4.5rem, 1fr) minmax(4.5rem, 1fr); … }` (was
  `1.1rem minmax(0, 1fr) auto`) plus `.svc-row input[type="number"] { min-width: 0; }`; a NEW `@media screen and (max-width: 359px)`
  block stacks each service-row control on its own line. `main { grid-template-columns: minmax(0, 1fr); }` (round 1) stays. **No
  `@media print` line is added or removed over main** (launcher-checked). `CONFIG.toolVersion` stays `"2.32"` (main is `"2.31"`).
- **The gate file (READ):** `phone-layout.mjs` now runs offline × {default, heavy, heavy-advanced} + public × {default, heavy} ×
  widths `[320, 350, 360, 375, 390, 481, 520, 543]` × {light, dark} = **80 cells**; it clears localStorage per page, sets the theme
  by clicking `#toggleDarkMode` and asserts it applied, adds a number-input fit check (canvas-measured text vs content box), a
  pairwise control-overlap check (`> 1 px²`), and for advanced cases `r.rateBox >= 60`.
- **An internal contradiction to MEASURE (drafter, READ):** the commit message says *"The minmax(0, 1fr) line itself is NOT pinnable
  any more … a sweep of every width 320-920 in three states is clean with it and without it"*, while the test file's own header says
  widths 481/520/543 *"also pin the minmax(0, 1fr) line (with a bare 1fr the page scrolls sideways again in that band, N-F3)"*. Only
  one can be true: revert only that line and run the 80 cells.
- **Builder's claims:** gate file 80/80; red on round 1's CSS in exactly the N-F1 and N-F2 shapes (28 cells); mutants "no 359 block →
  320 heavy-advanced red", "auto tracks → 360-390 heavy-advanced red"; desktop 768/921/1280 × light/dark × default/heavy only the
  52 px version digit differs from main; print 2 pages each, text differs only in the version footers. N-F2's band was "481-566 by a
  1 px sweep (the gate measured to 543)"; the wrap now applies to 600 ("a 920 range changed the 768 px page").
- **Version:** round 2 changes behaviour and keeps `2.32` ("v2.32 never shipped"). READ QuickQuote `CLAUDE.md` §Version discipline
  and say whether that is within the rule.
- **Screenshots for Kam (N-F4), READ ONLY — never write there:**
  `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/5_Project_History/a6-phone-layout-2026-09-22-r2-2246/`
  (68 PNG + `README.md` + `shots.json`; BEFORE = main `763269d` v2.31, AFTER = `54a7202` v2.32; states default / heavy /
  heavy-advanced × widths 320 / 375 / 390 / 481 / 520 × light / dark, plus 2× crops `crop-rate-row-{320,390}-*` and
  `crop-services-total-{481,520}-*`). README claims: every AFTER footer v2.32, fx 1.4832 in every heavy shot, no AFTER page scrolls
  sideways; `shots.json` records the rate box as `434 in 163px` at 320, `103px` at 375, `110px` at 390. **The set has no 512 or 543
  shot** — render those yourself. The two older folders (`a6-phone-layout-2026-09-22/`, `…-2053/`) are superseded.

### TARGET CF5 — C-F5 + C2-F2: only a provider-wide failure refunds, capped per source (TIER 1), QuickQuote
- **One commit `bfb8210` on `763269d`.** Files: `BACKLOG.md`, `stage3/lib/mail.js`, `stage3/lib/sendFailure.js` (A),
  `stage3/server.js`, `stage3/test/mail.test.mjs`, `stage3/test/server.test.mjs`.
- **`lib/sendFailure.js` (READ):** `isProviderWide(e)`: `e.code === "MAIL_NO_PROVIDER"` → provider; `statusOf(e)` =
  `Number(e.statusCode ?? e.status)` — 429 or 500–599 → provider, **any other integer status → recipient**; else a `NETWORK_CODES`
  code on `e` or `e.cause` (ECONNREFUSED, ECONNRESET, ENOTFOUND, ETIMEDOUT, EAI_AGAIN, EPIPE, EHOSTUNREACH, ENETUNREACH,
  UND_ERR_CONNECT_TIMEOUT, UND_ERR_SOCKET, UND_ERR_HEADERS_TIMEOUT, UND_ERR_BODY_TIMEOUT, REQUEST_SEND_ERROR) → provider; else
  `e.name === "TypeError" && e.message === "fetch failed"` → provider; **everything else → recipient (spends)**. Structured fields
  only, never message text.
- **`lib/mail.js` (READ):** the Agent Mail path's non-OK error now carries `{ status: r.status }`; the no-provider error carries
  `{ code: NO_PROVIDER }`. **Unchanged:** the ACS path throws a PLAIN `Error("ACS send failed: <status> …")` when `pollUntilDone`
  ends in any non-`Succeeded` status — no statusCode → **recipient → spends**, whatever the reason ACS failed the message; a
  `RestError` from `beginSend` carries `statusCode` (the SDK's). `send()` still retries once in-process (the thrown error is the
  SECOND attempt's), so a rejected address still costs TWO provider calls.
- **`server.js` (READ):** `const OTP_REFUND_CAP_PER_HOUR = 6;` and a new `createApp` option `otpRefundCapPerHour` (validated by the
  same `budgetSetting`, named `"otpRefundCapPerHour"`; NOT an env variable). `refundHits()` now reads `const at = clock().getTime();`,
  and if `refundCap.waitMs(src, at) > 0` logs `[stage3] OTP refund cap reached for one source — this failure spends its budget hit`
  and returns WITHOUT refunding; else it records a cap hit and refunds both budgets at the ORIGINAL `now`. **The cap applies to
  BOTH refund paths** — a provider-wide send failure AND a throwing `putOtp` (the `catch (e) { refundHits(); throw e; }` is
  unchanged). The send outcome is now `"sent"` / `"failed"` (provider) / `"rejected"` (recipient); only `"failed"` refunds; an early
  `"failed"` OR `"rejected"` answers the SAME 502 `could not send the code — mail delivery is failing right now; try again in a few
  minutes` (text unchanged; a clearer wording for `rejected` is PROPOSED in BACKLOG, "Kam's call", not shipped).
- **Cells (READ, 8 new):** in `server.test.mjs` — 100 junk-address attempts from one source → exactly 6 × 502 then 429; a status-422
  rejection whose TEXT says "429 quota too many ECONNREFUSED fetch failed" still spends; 503 / network (`TypeError("fetch failed")`
  with `cause.code ECONNREFUSED`) / no-provider still refund and a success spends; refunds capped — the 7th provider failure spends
  (one cap line); **C2-F2**: a provider failure refunds the GLOBAL hit too (per-source 100, global 3, two XFF sources); in
  `mail.test.mjs` — three classification cells over the real module's error shapes (Agent Mail 400 vs 503; no provider; ACS
  statusCode and a message the service marks Failed). **The pre-existing C-F3 cell was EDITED** so its fake throws with
  `statusCode: 429` (previously a plain Error) — verify that edit is exactly the error shape and nothing else.
- **Also in BACKLOG (READ):** the K-O1 cooldown entry "moved here … queued for the gate-4 follow-ups branch" (FU's second commit
  closes it) — a cross-branch BACKLOG dependency.
- **Stated residual (unchanged from gate 3):** real App Service `X-Forwarded-For` NOT TESTED; which recipient shapes real ACS rejects
  synchronously, and whether rejected calls count against its quota, NOT TESTED (production).

### TARGET I9 — item 9: the QuickQuote error log never carries a request body (TIER 1), QuickQuote
- **One commit `f2f5f48` on `51e9286` (STALE: main is `763269d`).** Files: `stage3/server.js` (+16/−2), `stage3/test/server.test.mjs`
  (+52). **Main `763269d` still logs `console.error("[stage3]", err);`** (the leak) — the leak is live on main and in the pending
  publish (decision 18 accepts that).
- **The handler (READ):** `const status = Number(err.status || err.statusCode);` then, for `err.expose === true && 400 ≤ status < 500`,
  `console.error("[stage3] client error", status, err.type || "(untyped)");`, else `console.error("[stage3]", (err && err.stack) ||
  String(err));`. The response is unchanged (4xx passes `err.message` back to the CLIENT — its own input; 5xx flat
  `{"error":"internal error"}`). **Why `err.message` is dropped (builder):** body-parser's SyntaxError carries the raw body on
  `err.body`, and V8's JSON.parse message quotes the input (`Unexpected token S, ..."advWord":SECRET-PRO"... is not valid JSON`;
  a short body is quoted whole).
- **Cells (READ, 2):** three malformed shapes (truncated, bad token, short) planted with `SECRET-HPAM-PLANT` and
  `ACME-CUSTOMER-PLANT`, each POSTed to `/api/quote/email`, `/auth/request` and `/auth/verify` → 400 each, and every captured line
  matches `^\[stage3\] client error 400 entity\.parse\.failed$`; control: a throwing `putFeedback` → flat 500 and a logged stack
  with no body. Builder: "Red with main's handler: the first cell fails; the control passes on both. stage3 90/90" (on `51e9286`).
- **The stack path (drafter, READ — measure):** a 5xx logs `err.stack`, which INCLUDES `err.message`. Any non-exposed error whose
  message carries request data would still reach the log. READ every `throw` / rejection a route can raise with caller text in its
  message (the drafter found `JSON.parse(row.stateJson)` wrapped in a `try` → `notFound()`, i.e. safe) and every OTHER log site that
  prints an error object: `[stage3] otp send failed:` + `e` (an Agent Mail error's message carries up to 300 chars of the provider's
  response detail, which can echo the recipient ADDRESS — a customer email), `feedback notify failed:` + `e`, `quote sent but not
  stored for reopening:` + `e`. These are outside I9's claim ("the error handler"); report them as READ observations with a severity.

### TARGET I10 — item 10: the portal answers an oversized body 413, not 500; client errors log no body (TIER 2), portal
- **One commit `515c9f8` on `f065675` (STALE: main is `aeadcc1` = B merged).** Files: `server/errors.js`, `server/errors.test.js` (A),
  the portal's app module (`server/index.js`: the inline 4-arg handler replaced by `app.use(lastResortHandler);`),
  `test/db/routes.test.js` (+1 DB cell).
- **`lastResortHandler` (READ):** for `err.expose === true && 400 ≤ status < 500`: `console.warn(\`[client error ${status}] ${where}:
  ${err.type || '(untyped)'}\`)` where `where` = `${req.method} ${req.originalUrl}`; if headers are not sent, answers
  `CLIENT_ERROR_TEXT[status] || 'Bad request'` (400 `Invalid JSON body`, 413 `Request body too large`, 415 `Unsupported content
  type`). Everything else → `serverError` (logs `[err <ref>] <method> <originalUrl>:` + the error OBJECT whole; answers 500
  `{ error: 'Internal error', ref }`). The portal's parser is `app.use(express.json())` (default 100 kb) plus per-route
  `express.json()` in `routes/auth.js` (/login, /me/prefs), `routes/feedback.js` (3 routes), `routes/admin.js`, and
  `/api/bot/leads`.
- **What the pass-through widens (drafter, READ — measure):** ANY middleware that raises an `expose: true` 4xx now keeps its status
  and gets a fixed message, where before only `entity.parse.failed` did and everything else was a 500 with a ref (e.g. serve-static /
  `send` errors on odd paths or ranges, express-session, helmet). Enumerate what can raise one in this app and measure two.
- **Tuesday's note (21:42):** "the portal was measured as not having the leak" — main's handler logged NOTHING for a parse failure,
  and a 413 went to `serverError`, which logs the error object (a `PayloadTooLargeError` carries `expected`/`length`/`limit`, not the
  body). Measure main's 413 log for a planted marker (expected: absent) so the "no body" claim has a base.
- **Cells (READ):** `errors.test.js` (in `npm test`, no DB): oversized → 413 + fixed text + log line, marker absent; malformed → 400,
  marker absent and no `Unexpected|Unterminated|JSON at position`; control 5xx → 500 + 8-hex ref + full detail under that ref;
  control: a 5xx that claims expose is NOT passed through. `routes.test.js` (in `test:db`): an oversized `POST /api/quotes` → 413.
- `req.originalUrl` (with its query string) is logged on both paths — pre-existing in `serverError`; READ which routes take query
  parameters (the drafter found only filters: stage, category, status, lead_id, quote_id, view, scenario) and say whether anything
  sensitive can ride there.

### TARGET Q5 — item 5: qs 6.16.0 via express 4.22.3 / body-parser 1.20.8 (TIER 2, dependency), QuickQuote
- **Two commits over `51e9286`:** `320a169` (on `47eb533`, an ancestor of `51e9286`) "stage3: qs 6.16.0 (via express 4.22.3 /
  body-parser 1.20.8) for two qs advisories" → `103340c` = `--no-ff` merge of `51e9286`. **Delta over `51e9286`: ONE file,
  `stage3/package-lock.json`, and exactly THREE package versions change** (drafter's python over both lockfiles: `body-parser`
  1.20.6 → 1.20.8, `express` 4.22.2 → 4.22.3, `qs` 6.15.3 → 6.16.0; 282 entries before and after; `stage3/package.json` unchanged).
- **Builder's claims:** GHSA-x5fp-wj9c-mxmx (array-limit bypass) and GHSA-4mjr-xmp4-gh2g (DoS via isBuffer), moderate; "Moderates
  3 → 0. The 3 highs (extract-zip via puppeteer-core) remain" (P5B clears those); gates 52/52, 18/18, 5/5, 66/66 (at `320a169`, OLD).
- **`npm audit` is a REGISTRY call** (the bulk advisory endpoint); with `npm_config_offline=true` and this gate's egress rule it
  cannot run. **The builder's audit numbers are therefore UNVERIFIABLE here — say so.** The READ substitute: the lockfile diff is
  exactly the three bumps; each resolved version sits inside its parent's declared range; `resolved` URLs are registry.npmjs.org
  tarballs; `integrity` present for each.
- **Behaviour (READ + MEASURED):** body-parser 1.20.8's error `type` strings (`entity.parse.failed`, `entity.too.large`) are what I9's
  log line and M's D-F1 cell depend on — measure them unchanged; qs 6.16's array-limit change: READ whether any QuickQuote route reads
  `req.query` arrays.

### TARGET P5B — item 5b: puppeteer-core 25.0.2 and a node:22 image (TIER 2, PRODUCTION RUNTIME CHANGE), QuickQuote
- **Two commits over `51e9286`:** `3d0167e` (on `47eb533`) → `0d45100` = `--no-ff` merge of `51e9286`. **Delta over `51e9286`:**
  `stage3/Dockerfile` (`FROM node:20-bookworm-slim` → `FROM node:22-bookworm-slim` + a 3-line comment; the rest — apt chromium +
  fonts, `ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium`, `RUN npm ci --omit=dev`, `USER node` — unchanged), `stage3/package.json`
  (`"puppeteer-core": "^23.5.0"` → `"^25.0.2"`), `stage3/package-lock.json` (282 → 242 entries, 55 version changes;
  `puppeteer-core` 25.0.2 with `engines.node >=22.12.0`; `@puppeteer/browsers` 2.6.1 → 3.0.2; `extract-zip` GONE).
- **Kam's decision 14** (pack): "a tested update moves to Node 22 and a newer PDF engine … When should it ship? … If silent: it waits."
  A GO is "tested, ready when he decides"; it ships nothing.
- **Builder's claims (at `3d0167e`, OLD base):** 52/52, 18/18, 5/5, 66/66; the fixture quote rendered before/after on the Mac (Chrome
  153.0.8010.48) and inside locally built images (bookworm Chromium 153.0.8010.52) — 2 pages, text byte-identical, themes
  pixel-identical. **The docker image claim is the builder's; this gate runs NO docker: the image build is NOT RUN — say so.**
- **What you CAN do (READ + MEASURED):** read the Dockerfile diff whole; `npm ci --offline --ignore-scripts` against P5B's lockfile
  (242 entries, lockcmp + lockwalk); every print gate on the new puppeteer (`test:print` — print-fit, typed-rates, fx-provenance —
  and `test:xlsx`); the real `lib/pdf.js` emailed PDF base vs P5B (text + raster, heavy AUD with the renderer egress-blocked);
  READ `lib/pdf.js` and every puppeteer call site in stage3 for APIs removed or changed between 23 and 25 (headless mode, `page.pdf`
  options, `waitForTimeout`, launch args). **Node 22 itself is NOT TESTED** (this machine runs node v26; say which version you ran).

<!-- SLOT-FU:BEGIN -->
### TARGET FU — the gate-3 follow-ups K-F1, L-F1, M-N2, and K-O1 (TIER 2, tests only), QuickQuote — present because SLOT-FU: IN
- **Two commits on `763269d`:** `9ccca8a` "stage3 tests: gate 3 follow-ups K-F1, L-F1, M-N2 (cells only, no product change)" →
  `78aa156` "stage3 tests: the two cooldown cells run on the injected app clock, not real sleeps (gate 3 K-O1)". Files over
  `763269d`: `stage3/package.json` (ONE line: `test:print` gains `test/email-collector.mjs`), `stage3/test/email-collector.mjs` (A,
  90 lines), `stage3/test/server.test.mjs` (+46/−4). **No product file** (launcher-checked: the file set, and the package.json delta
  is exactly that one script line). Tuesday's message says "the diff must touch test files only" — `package.json` is not a test file;
  prove its delta is the script line and nothing else.
- **K-F1 (READ):** a new cell — a feedback mail that REJECTS: the POST answers 201, `process.on("unhandledRejection")` records
  nothing within 50 ms, `/healthz` answers 200. Builder: "Red with the .catch dropped."
- **L-F1 (READ):** `email-collector.mjs` (in `test:print`) loads the real `strip.js` output from memory behind request interception
  (origin `http://qq.test`; `/api/quote/email` stubbed; everything else refused), ticks `toggleDarkMode`, types into `advWord` and
  `fbMsg` (**`fbMsg` only `if (fb)` — it lives in `strip.js`'s hosted extras; confirm it exists in the page or the draft assertion is
  vacuous**), sets devices / term / custName / registerDeal, clicks `#btnEmailPdf`, and asserts none of `CHROME_IDS` in
  `state.fields`/`state.checks`, neither typed string anywhere in the body, and the quote fields present. **`toggleAdvanced` is never
  ticked** (no advanced unlock) — measure whether an unticked checkbox was posted at the pre-A-10 collector, i.e. whether the mutant
  "collector posts the four keys again" reddens on ALL FOUR or only on the three the test fills.
- **M-N2 (READ):** the D-F1 cell now also asserts `strict-transport-security` = `max-age=31536000` and `referrer-policy` =
  `no-referrer` on the 400 and 413. Builder: "Red under the gate's split-middleware mutant (those two headers set after
  express.json)". **Tuesday's message names the mutant as "a body parser mounted before the headers" — that is gate 2's
  MUT-afterjson, which D-F1 ALREADY caught at gate 3; the M-N2-specific mutant is gate 3's SPLIT-middleware one (HSTS +
  Referrer-Policy set after `express.json`). Run BOTH.**
- **K-O1 (`78aa156`, READ) — NOT named in Tuesday's message:** the two cooldown cells now drive `createApp({ clock })` with the
  production 60 s cooldown (and check the 59 s edge) instead of 40–60 ms real sleeps. Builder: "10 runs of both cells under 8 busy
  CPU processes: 0 failures." Its BACKLOG entry lives on the CF5 branch.
- **Merge shape (drafter, scratch):** FU × N **CONFLICTS in `stage3/package.json`** (both append to `test:print`); FU × I9 conflicts
  in `server.test.mjs`; FU × CF5, × Q5, × P5B clean.
<!-- SLOT-FU:END -->

### All targets
- **No worktree is pinned. Build your own trees INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store:**
  `git -C <repo> archive <pinned sha> | tar -x -C <a fresh mktemp -d under your project>`. **Never `git worktree add`,
  `checkout`, `switch`, `fetch`, `pull`, `stash`, `reset`, `restore`, `clean`, `gc`, `tag` or commit against either repo, and
  never work inside either checkout.** Both checkouts are the LIVE builder's working trees (at drafting: QuickQuote on
  `fix/qq-gate3-followups-2026-09-22` with an uncommitted `server.test.mjs` edit; portal on `main`): pin by sha, read origin by
  `ls-remote`.
- **Dependencies, without the network:** an archived tree has no `node_modules`. The builder's installed `node_modules` is NOT the
  gated set; do not copy it. The sanctioned route: in YOUR archived tree, **`npm ci --offline --ignore-scripts`** (in `stage3/` for
  QuickQuote, at the root for the portal). `--offline` forbids the network by construction: a cache miss FAILS rather than fetches —
  that suite is then **NOT RUN, blocker named** (name the missing tarballs). Never `npm install`, never `npm ci` without
  `--offline`, never `npx` a package that is not already in the tree, **never `npm audit`** (a registry call). After it, prove
  `node_modules/.package-lock.json` matches `git show <sha>:<lockfile>` entry by entry and quote the count (gate 3: portal 247/247,
  stage3 282/282; **P5B's lockfile is 242 entries**, Q5's 282), by `lockcmp.py` AND the on-disk `lockwalk.py`. (Drafter's READ: the
  local npm cache index holds `qs-6.16.0`, `express-4.22.3`, `body-parser-1.20.8` and `puppeteer-core-25.0.2` tarball entries; the
  rest of P5B's set is unchecked.) Chrome: `PUPPETEER_EXECUTABLE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`,
  launched through YOUR copy of the egress-block wrapper (§13.3).
- **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree for a
  clean arm; never touch gate 1's, gate 2's or gate 3's trees (`work/`, `work-g2/`, `work-g3/`). Use `work-g4/`.
- **`git merge-tree --write-tree` writes objects** — only ever as `GIT_OBJECT_DIRECTORY=<your own mktemp -d>
  GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree --name-only <a> <b>`. The same two
  variables let you `git archive <tree-id>` a merge RESULT. If you cannot do it that way, SKIP it and say so.
- **A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES:** `node --check` on every mutated `.js`/`.mjs`/`.cjs` before its arm, exit code
  quoted. A red from a mutant that does not parse or load is a VOID arm, never a red. (CSS mutants: `node --check` does not apply —
  prove the edit landed by a `diff` in the evidence.)
- **NOT on main. Nothing merges on your word or a builder's.** Merges are Tuesday's GO on a pinned head.

## 2. Why these tiers, and who is waiting
- **CF5** bounds what one network can make `/auth/request` do to ACS and Table Storage; it re-shapes C-F3's refund, adds a cap that
  now also limits the throwing-`putOtp` refund gate 3 closed, and changes what a mistyped address costs. The live tool has no budget
  at all yet (C is on main, not published).
- **I9** closes a live privacy leak (malformed request bodies — OTP codes, the HPAM word, customer names — into the container log and
  Log Analytics). **I10** is the portal's twin, mostly a status-code fix (the portal did not log bodies).
- **N** changes what every phone user sees, in both builds; round 2 of 2.
- **Q5 / P5B** clear advisories; P5B moves the production runtime (Kam's decision 14).
- **FU** pins three properties gate 3 proved unpinned, and de-flakes two cells.
- 🔴 **Queue:** deploys HELD for Kam (the live tool is v2.30; the publish card is amended to QuickQuote `763269d`; the portal's live
  site is production). Portal: I10 (forward merge onto `aeadcc1`). QuickQuote: N, CF5, FU on main (merge order sets the test-tail
  conflicts); I9, Q5, P5B need forward merges onto `763269d` (§12).

## 2a. LEGITIMATE SHAPES — CHECKERS in this gate (template §2a)
CF5 refuses (a budget, now a refund cap), I9 and I10 redact. Measure every row.

| shape — its ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| CF5: ACS throttles (429) for 10 min; an office retries 7 times; ACS recovers | 7 × 502; after recovery the office has 5 codes (6 refunded, the 7th spent), then 429 | provider-wide refund, cap 6/h | builder (cell) — **measure** |
| CF5: ACS down (5xx) for 30 min; an office retries 13 times | 13 × 502; 6 refunded, 7 spent → **the source is at 7 hits ≥ its budget of 6: locked out for up to an hour after the outage** | the cap | drafter (READ) — **measure and grade: the cap trades an outage lockout for the abuse bound** |
| CF5: Table Storage (`putOtp`) throws for 10 min; an office retries 8 times | 8 × 500; 6 refunded, 2 spent → 4 codes left | the cap ALSO covers `putOtp` | drafter (READ) — **measure; gate 3 closed C-F3's putOtp half as "budget intact"; say whether the cap re-opens it partly, and whose choice that is** |
| CF5: a user mistypes their address into one ACS rejects (4xx), 3 times | 3 × 502 "mail delivery is failing right now; try again in a few minutes"; 3 hits SPENT | `rejected` spends | builder — **quote the text; grade the misleading wording (BACKLOG's proposal is Kam's)** |
| CF5: ACS accepts the message, then the poll ends `Failed` (e.g. a transient ACS-side failure) | 502 or late; **spends** (plain Error, no status) | recipient by default | drafter (READ) — measure through the real `lib/mail.js` with an ACS recorder |
| CF5: 6 people behind one NAT, one sign-in each; a 7th | unchanged from gate 3: 6 × 200, 7th per-source 429 | 6/h per key | gate 3 (needs Kam, unchanged) |
| I9: a rep's browser posts a truncated body (network cut) to `/api/quote/email` | 400 to the client; log line `[stage3] client error 400 entity.parse.failed`, nothing else | the handler | builder — measure |
| I9: a 300 KiB quote email body | 413 to the client; log `client error 413 entity.too.large` | the handler | drafter — measure |
| I10: a 200 KiB `POST /api/quotes` from a signed-in admin | 413 `Request body too large`; log names status + type only | `lastResortHandler` | builder — measure |
| I10: a real DB fault in a route | 500 `{ error: 'Internal error', ref }`; the log under that ref has the detail | `serverError` | builder — measure |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.** A legitimate shape refused is a
**Major**.

## 3. TARGET N — A-6 ROUND 2 of 2 (TIER 2, CUSTOMER-VISIBLE)
**Screenshots from YOUR OWN renders, never the builder's.** Chrome through YOUR egress-block wrapper; a fresh browser context per
case; the theme set by clicking the real `#toggleDarkMode` control (through the cog, as gate 3 did) and a settle wait ≥ 600 ms, the
applied theme VERIFIED from `html[data-theme]` before measuring. Re-use gate 3's `qa-harness-n-render.cjs` / probes by COPY.
**FAIL condition (state it before the run):** any money figure, app price or input value hidden, clipped, overlapped or off-screen
at a supported width (320 and up), any page sideways scroll at ≤ 920, any desktop pixel changed outside the version digit, any
print/emailed PDF change outside the version line.
1. **The forward merge `c1abc05` (READ ONLY):** re-run `merge-tree` `ac0a8d2` × `763269d` from YOUR object dir; its tree must equal
   `c1abc05^{tree}` (drafter: `b49d1bc…`, equal). Then `git diff ac0a8d2 c1abc05` = main's `51e9286..763269d` delta, and
   `git diff 763269d c1abc05` = round 1's patch.
2. **Re-render yourself at 320 / 375 / 390 / 481 / 512 / 543 px, light AND dark (MEASURED):** both builds — offline `index.html`
   from `file://` and the hosted page (strip.js output behind YOUR harness, signed in, so the masthead carries Sign out and the cog) —
   at the BASE `763269d` and at N, states default, heavy and **heavy-advanced (BOTH builds: the hosted one unlocked through the real
   UI and server with a word you generate)**. For each: `scrollWidth` vs `clientWidth`; every money figure / ticket value / app price
   inside the viewport AND its panel (Range-measured text); **every visible input's value fits its content box** (gate 3's
   `N-probe-inputs` method), `#price-custom` width quoted per width; no two controls overlap; the masthead intact at 320; no
   `text-overflow` truncation. Save full-page PNGs into YOUR evidence folder. **N-F1 closed** = `#price-custom` shows `434` whole at
   every width in both builds, with no overlap; **N-F2 closed** = the services total whole at 481 / 512 / 543.
3. **The band and the new breakpoints (MEASURED, adversarial):** a 1 px sweep 470–620 in heavy (both builds, light) — N-F2's band
   was 481–566 by the builder's sweep, the new wrap stops at 600: probe 544–600 and **600 / 601** (the edge of the new block), and
   **359 / 360** (the stacking edge), plus 321, 330, 414, 430, 480, 920 / 921; zoom 200 % at 390 (record only: below 320); DKK 950
   devices 5 years; a 60-character unbroken customer name; POA tails. Widths below 320 are the builder's stated NOT TESTED — record,
   do not grade.
4. **Desktop identity (MEASURED):** 768, 921 and 1280, light and dark, default and heavy, both builds: base `763269d` vs N →
   differing pixels only in the footer version digit (gate 3: exactly 52 px in a 7×10 box). Name any other difference. 768 sits inside
   the 920 breakpoint but above the new 600 one.
5. **Print unchanged apart from the version (MEASURED):** the printed quote as a real A4 PDF (`format: "A4"`, print media) base vs N,
   default and heavy, light and dark page theme: page count; `pdftotext` differs only in the version lines; a rasterised compare with
   differences only in the footer band. The EMAILED PDF from the real `lib/pdf.js` (renderer egress blocked; a fixed qnum) base vs N:
   text and pages identical apart from the version. Confirm the 600 and 359 px blocks are `screen`-scoped (`matchMedia` in print media
   at a 400 px viewport). Quote the 2.32 footer line from a real PDF.
6. **The gate file (MEASURED):** `node --test stage3/test/phone-layout.mjs` alone at N → 80/80, exits on its own (time it); at the
   base `763269d` with N's file copied in → which cells fail (builder: every narrow case); **on round 1's CSS** (`ac0a8d2`'s
   `index.html` with N's test file) → the builder's "28, exactly the N-F1 and N-F2 shapes"; red arms (CSS, diff-proved): revert
   ONLY `minmax(0, 1fr)` → **settle the commit-vs-comment contradiction in §1** (N-F3 closed or still open); restore the `auto`
   input tracks → which cells redden; delete the 359 block → which; shrink the 600 block back to 480 → which (does 520/543 catch it?).
7. **N-F4 — Kam's screenshot set (READ ONLY, then MEASURED comparison):** list the new folder; check README claims against
   `shots.json` and against the PNGs (footer version in every AFTER = v2.32, fx 1.4832 in every heavy, sideways scroll 0 in every
   AFTER); pixel-diff comparable pairs against YOUR renders at the same width/state/theme (same layout or not, and where they
   differ). Say whether this folder can go to Kam as it is. Note its missing 512/543.
8. **Suites at N:** `stage3/` `npm test` (90 cells in server.test at N), `npm run test:print` (includes the 80-cell phone file),
   `npm run test:xlsx`, root pricing `node --test quote-engine.test.mjs`.
9. **Version (READ):** round 2 keeps 2.32 — within QuickQuote's rule? Nothing else in the queue claims 2.32 (READ each target's
   `toolVersion`).

## 4. TARGET CF5 — C-F5 + C2-F2 (TIER 1)
**The drivable surface is `createApp(...)` in YOUR OWN harness** (the stage3 entry point cannot boot without Table Storage). Inject
gate 3's in-memory store (`qa-lib-c2-stage3.cjs`, COPIED after reading), a fake mail that records and can fail per address and per
error SHAPE, and for XFF legs `trustForwardedFor: true` explicitly (never `WEBSITE_SITE_NAME` in a product process). 127.0.0.1,
kernel port.
1. **Positive control on MAIN `763269d` first (MEASURED):** reproduce gate 3's C-F5 — 100 `POST /auth/request` from ONE source to
   100 distinct junk addresses (e.g. `junk<i>@@x.example`, which pass `/^\S+@\S+\.\S+$/`) with a fake that REJECTS them → **100 × 502,
   never a 429** (gate 3: C1 30 × 502, C2 100 × 502). Quote. **Then at CF5:** the same 100 → exactly 6 × 502 then 94 × 429; the same
   with an ACS-shaped `RestError` `statusCode: 400`, an Agent Mail-shaped `{ status: 400 }`, a status-less plain Error, and a
   `status: 422` whose text reads like a throttle — each spends. A control that fired in the same run is required for the "capped" result.
2. **Provider-wide failures still refund (MEASURED):** 429, 500, 503 (as `statusCode` AND as `status`), each NETWORK_CODES code on
   `e` and on `e.cause`, `TypeError("fetch failed")`, `code: "MAIL_NO_PROVIDER"` → 502 and refunded (3 failures then a working
   mailbox → the full budget). **Boundaries:** status 499, 600, `"503"` as a string, `NaN`, `statusCode: 0`; a `fetch failed` whose
   `name` is not `TypeError`; an error that is not an object (`throw "x"`); `null`. Table what each classifies as and grade anything
   surprising.
3. **The cap (MEASURED):** 7 provider failures → 6 refunded, the 7th spent, exactly one cap line; the cap window slides on the APP
   clock (advance 61 min → 6 more refunds); the cap is per SOURCE (another source still refunds); **the throwing-`putOtp` refund is
   capped too** (8 throws → 6 refunded, 2 spent — the §2a row; say whether that partly re-opens gate 3's closed C-F3 putOtp half and
   whether it needs Kam); a refund still restores at the ORIGINAL `now` while the cap records `at = clock()` read at refund time (a
   late failure after the grace window: refunded, cap recorded at the late time). `otpRefundCapPerHour` option: `0`, `-1`, `"abc"`
   → `createApp` throws naming `otpRefundCapPerHour`; absent → 6.
4. **Through the REAL `lib/mail.js` (MEASURED; never a network):** evaluate the tree's real module with an ACS recorder standing in
   for `EmailClient` (gate 3's `realmail` leg method) and a fetch that refuses every host: (a) `beginSend` rejecting with the SDK's
   `RestError` at 400 → `rejected`, TWO `beginSend` calls (the retry), spends; at 429/503 → refunded; (b) the poll ending
   `status: "Failed"` → `rejected`, spends (the §2a row); (c) the Agent Mail path with `AGENTMAIL_*` UNSET → `MAIL_NO_PROVIDER` →
   refunded — and **never set real AGENTMAIL values in a product process** (with both set, QuickQuote SENDS FOR REAL); for the Agent
   Mail `status` path use a fetch stub that answers 400 / 503 to a fake host, never `api.agentmail.to`. READ `@azure/communication-email`
   / `@azure/core-rest-pipeline` in YOUR `node_modules` for the error shapes `beginSend` and `pollUntilDone` really throw
   (`RestError.statusCode`, `code` = `REQUEST_SEND_ERROR` / `PARSE_ERROR`), and say which ones the classifier gets right.
5. **Gate 3's C harness, re-run at CF5 (MEASURED):** COPY `qa-harness-c2-budget.mjs` + `qa-lib-c2-stage3.cjs`. **Predict before
   running:** its `abuse` leg now FAILS by design (it asserts the refund of a rejected address), and its q3 converse A may fail
   because its fake's failed send is a status-less Error (now `rejected`, i.e. spent). Derive YOUR contract copy (provider-shaped
   failures for the converses; `abuse` inverted to "capped at 6") and **quote your diff against gate 3's file**. Every other leg (q1
   q2 q3 q4 q5keys q5e2e exhaust conc shapes2 clock nat16 refund realmail hf3) must match gate 3's results.
6. **Red-proofs (parse-checked mutants, `node --check` rc quoted):** (a) `isProviderWide` → always `true` → the 100-junk cell reddens;
   (b) drop the cap check → the cap cell reddens; (c) **drop only `globalBudget.refund("*", now)` from `refundHits` → the C2-F2 cell
   reddens** (gate 3: builder suite 98/98 GREEN on this mutant); (d) classify on message text (e.g. `/429/.test(e.message)`) → the
   text-echo cell reddens; (e) revert `lib/mail.js`'s `{ status: r.status }` → the mail.test Agent Mail cell reddens. A fix with no
   reddening cell is a finding.
7. **The edited C-F3 cell (READ):** `git diff 763269d bfb8210 -- stage3/test/server.test.mjs` for the pre-existing C-F3 cell: the
   only change is the fake's error gaining `statusCode: 429`. Quote it.
8. **Adversarial (state the FAIL condition first):** FAIL = more than 6 provider calls' worth of attempts per hour from one real
   source for caller-chosen addresses; a provider outage that refunds without bound; a classification driven by caller text; a
   legitimate source refused that gate 3 admitted. Re-run gate 3's q5 set (XFF rotation, key-minting header shapes, IPv6 /64, the
   hex v4-mapped bucket) — unchanged expected. **Can a caller manufacture a provider-shaped failure?** (e.g. an address that makes
   the provider answer 5xx or time out) — READ `lib/mail.js` and the ACS path; if yes, each costs at most 6 refunds per hour (the cap):
   measure that bound.
9. **Suites at CF5:** `stage3/` `npm test` (95 cells in server.test + mail/strip/store), `test:print`, `test:xlsx`, pricing.
10. **Login page (MEASURED, one case):** the 502 text for a rejected address as the page renders it (real Chrome, 375 and 1280) —
    quote it; it is customer-visible and unchanged.

## 5. TARGET I9 — item 9 (TIER 1)
1. **Plant and capture (MEASURED):** in YOUR harness at `f2f5f48`, capture EVERY console stream of the product process (stdout AND
   stderr, `console.error/warn/log/info`, rendered with `util.inspect` as a real container log would). POST malformed bodies planted
   with markers — an `advWord` value you generate and a customer name (`custName`) — to `/api/quote/email`, `/auth/request` and
   `/auth/verify`, shapes: truncated, bad token, short/whole-quoted, a body whose FIRST bad token is the marker, a 300 KiB body (413),
   an unsupported charset (`application/json; charset=utf-7` → 415), `Content-Type: application/json` with a gzip `Content-Encoding`
   you do not send (400/415), an empty body. **Captured logs contain neither marker, in any shape**; each client error logs exactly
   `[stage3] client error <status> <type>`. **Positive control on the base `51e9286` (and on main `763269d`):** the same bodies →
   the markers ARE in the log (quote one line, redacted to the marker) — without it, a clean log proves nothing.
2. **A 5xx still logs a stack (MEASURED):** a throwing store method (and a throwing `renderQuotePdf`) → flat 500
   `{"error":"internal error"}` and a log line with the stack; the stack carries no request body. **Then the stack-path probe (§1):**
   can any route produce a non-exposed error whose MESSAGE carries caller text? READ every route; measure any you find.
3. **Red-proof:** revert only the handler to `console.error("[stage3]", err);` (parse-checked) → the builder's first cell FAILS and
   YOUR capture finds the markers; the control cell passes on both (builder's claim).
4. **Other log sites (READ, severity each):** `otp send failed: e`, `feedback notify failed: e`, `quote sent but not stored for
   reopening: … e` — what can each carry (a customer email address in an Agent Mail / ACS error message)? Outside I9's claim; report.
5. **Suites at `f2f5f48`:** `stage3/` `npm test` (builder 90/90), `test:print`, `test:xlsx`, pricing.
6. **I9 × main `763269d` (PROBED):** `merge-tree` (drafter: **CONFLICT `stage3/test/server.test.mjs` only; `server.js`
   auto-merges**). On the merge result's auto-merged server file (0 conflict markers, `node --check`), run YOUR I9 capture legs plus
   the C budget refusals (their 429s go through routes, not the handler — confirm no change) and M's D-F1 malformed/oversized shapes
   (the log line those produce). Never `npm test` on a tree with conflict markers. **I9 × Q5 (clean, drafter):** archive the merge
   result and run the I9 capture on it — body-parser 1.20.8 must still set `type` = `entity.parse.failed` / `entity.too.large`.

## 6. TARGET I10 — item 10 (TIER 2, through-code)
**The portal's `createApp()` in YOUR harness on LOCAL Postgres (§13.2), `env -i`; never the portal's entry point (it binds all
interfaces).**
1. **Oversized → 413, malformed → 400, unsupported charset → 415, a real 5xx still 500 with a ref (MEASURED):** through the global
   parser AND at least two per-route parsers (`/api/auth/login`, a feedback route) and `/api/bot/leads`; quote status + body for each;
   helmet's headers present on each 4xx.
2. **No body logged (MEASURED):** capture every console stream; planted markers in each malformed / oversized body → absent from every
   log line; the client-error line is exactly `[client error <status>] <METHOD> <originalUrl>: <type>`. **Base control:** main
   `aeadcc1` (and `f065675`) — does the marker appear in main's 413 log (via `serverError` logging the error object)? Quote either way;
   Tuesday's note says the portal did not have the leak.
3. **The 5xx path:** a route that throws (a DB fault you induce on YOUR database, e.g. a dropped table in YOUR `_test` DB, or a stub)
   → 500 + 8-hex ref, the log line under that ref carries the detail; a 5xx error with `expose: true` is not passed through.
4. **The widened pass-through (READ + MEASURED):** list the middlewares that can raise an `expose: true` 4xx (express.static/`send`,
   express-session, helmet, the CSRF backstop) and measure two (e.g. a static path with an encoded traversal, a bad Range) — status
   and body at main vs I10. Grade any 500 → 4xx change you did not expect.
5. **Suites at `515c9f8`:** `npm test` (includes `server/errors.test.js`), `npm run test:db` on a FRESH `vsp_qa_g4_<epoch>_test`
   database (prove it fresh first: zero user tables), which runs the new `routes.test.js` 413 cell. **Red-proof:** restore the old
   inline handler in a parse-checked copy → the 413 cells redden.
6. **I10 × main `aeadcc1` (PROBED):** `merge-tree` (drafter: **clean**, tree `53a2838…`). Archive the result, `npm ci --offline
   --ignore-scripts`, `npm test` and `test:db` on a fresh `_test` DB (B's `reminder-push.test.js` included — say its count).

## 7. TARGET Q5 — item 5 (TIER 2, dependency)
1. **Scope (READ):** `git diff --name-only 51e9286 103340c` = `stage3/package-lock.json`; entry-by-entry version diff of the two
   lockfiles = exactly body-parser, express, qs (drafter); `package.json` blob unchanged; `103340c`'s parents = `320a169` + `51e9286`.
2. **`npm audit` before/after: NOT RUN** (registry call; say so, and that the builder's "moderates 3 → 0" is UNVERIFIED). The READ
   substitute per §1.
3. **Install (MEASURED):** `npm ci --offline --ignore-scripts` in YOUR tree at `103340c` → 282/282 by lockcmp AND lockwalk; the three
   new versions on disk (`node_modules/<pkg>/package.json` versions quoted).
4. **Suites at `103340c` (MEASURED):** `stage3/` `npm test`, `test:print`, `test:xlsx`, pricing — all green; the body-parser error
   `type` strings unchanged (one malformed and one oversized request in YOUR harness, `err.type` quoted).
5. **Q5 × main `763269d` (PROBED; drafter: clean, tree `fa07fad…`):** archive, install offline, `npm test` there (it carries C, K, L,
   M's cells with the new express/body-parser). **Q5 × P5B (drafter: CLEAN, tree `ea71815…`, although BOTH edit the lockfile):**
   archive the auto-merged lockfile and prove it is a valid lock for the merged `package.json` — `npm ci --offline --ignore-scripts`
   succeeds and lockcmp/lockwalk agree; name any entry that is in neither parent. A textually clean lockfile merge is not proof of a
   consistent tree.

## 8. TARGET P5B — item 5b (TIER 2, PRODUCTION RUNTIME CHANGE)
1. **The Dockerfile diff read whole (READ):** quote it; only the base image line and its comment change over `51e9286`; `npm ci
   --omit=dev`, the apt chromium/fonts line, `PUPPETEER_EXECUTABLE_PATH`, `USER node` unchanged. **The image build is NOT RUN (no
   docker for the gate) — say so in the verdict line.** Node 22 in the image is NOT TESTED (this machine: node v26 — quote
   `node --version`). CI's workflow already pins node 22 (`.github/workflows/tests.yml`, READ) — CI itself NOT RUN.
2. **Install (MEASURED):** `npm ci --offline --ignore-scripts` against P5B's lockfile → 242/242 by lockcmp AND lockwalk; a cache miss
   is NOT RUN with the missing tarballs named. `puppeteer-core` 25.0.2 and `@puppeteer/browsers` 3.0.2 on disk; `extract-zip` absent.
3. **Print gates on the new puppeteer (MEASURED):** `test:print`, `test:xlsx`, `npm test`, pricing at `0d45100`; the emailed PDF from
   the real `lib/pdf.js` (default USD and heavy AUD, a fixed qnum, renderer egress blocked) base `51e9286` vs P5B → pages identical,
   `pdftotext` identical, raster identical (or name the differing band); the offline printed quote is not puppeteer's — say so.
4. **API drift (READ):** every `puppeteer.launch` / `page.pdf` / `waitFor*` / `headless` call in stage3 (lib and tests) against
   puppeteer 25's API; name anything removed or re-defaulted.
5. **P5B × main `763269d` (PROBED; drafter: clean, tree `a82a4c0…`):** archive, install offline, run `test:print` there (N's
   phone file is not on main yet; C, K, L, M's are).

<!-- SLOT-FU:BEGIN -->
## FU. TARGET FU — gate-3 follow-ups (TIER 2, tests only) — present because SLOT-FU: IN
1. **Scope (READ):** `git diff --stat 763269d 78aa156` = `stage3/package.json`, `stage3/test/email-collector.mjs`,
   `stage3/test/server.test.mjs`; the `package.json` delta is EXACTLY the one `test:print` line (quote it); no product file. Prove it.
2. **Each new cell GREEN on the clean tree and RED on a mutant that reintroduces its defect (MEASURED, parse-checked):**
   - **K-F1:** drop the `.catch(e => console.error("[stage3] feedback notify failed:", e))` from the feedback route → the K-F1 cell
     FAILS (on the `unhandledRejection` assertion — quote which fires), and the test FILE still exits on its own (time it).
   - **L-F1:** remove the `NOT_QUOTE` skip in `strip.js`'s collector → `email-collector.mjs` FAILS; a second mutant that posts only
     `advWord` under a different key (e.g. `aw`) → still caught (the whole-body string assertion)? a third that posts
     `toggleAdvanced` only → caught? (it is never ticked in the cell — measure whether it is posted unticked). Confirm `fbMsg` exists
     in the stripped page.
   - **M-N2:** gate 3's SPLIT-middleware mutant (HSTS + Referrer-Policy set in a second middleware AFTER `express.json`) → the D-F1
     cell now FAILS (gate 3: 89/89 green); gate 2's MUT-afterjson (the whole header middleware after the parser) → still FAILS.
   - **K-O1 (`78aa156`):** a mutant that stops the cooldown (e.g. `otpResendCooldownMs` ignored) → both cooldown cells FAIL; a mutant
     where a refused resend DOES burn a window slot → "does not burn a slot" FAILS. **Determinism:** run the two cells 20× under load
     (the machine's own) → 0 failures; quote the loop.
3. **Suites at `78aa156`:** `stage3/` `npm test` (91 cells in server.test), `test:print` (includes `email-collector.mjs`), `test:xlsx`,
   pricing. `email-collector.mjs` runs under YOUR egress-block wrapper too; it refuses the FX hosts itself — quote its `refused` list.
<!-- SLOT-FU:END -->

## 12. Across targets — merges and the queue
**Every prediction below is the drafter's own scratch `merge-tree` (own object dirs under the drafter's scratchpad, 22:5x AEST,
run under bash). Quote `git merge-tree --write-tree --name-only` from YOUR OWN object directory for each pair, or say you skipped it.**
The builder merges each forward at merge time; your job is to say which pairs conflict and which cells must be re-run on each
merged head — never to resolve a conflict.

| pair | drafter's scratch result |
|---|---|
| `ac0a8d2` × main `763269d` (N's forward merge) | clean; tree `b49d1bc…` **= `c1abc05^{tree}`** |
| I9 `f2f5f48` × main `763269d` | **CONFLICT `stage3/test/server.test.mjs`**; `server.js` auto-merged |
| Q5 `103340c` × main `763269d` | clean (`fa07fad…`) |
| P5B `0d45100` × main `763269d` | clean (`a82a4c0…`) |
| Q5 × P5B | **clean** (`ea71815…`) although both edit `stage3/package-lock.json` — validate it (§7.5) |
| N × CF5, N × Q5, N × P5B, CF5 × Q5, CF5 × P5B, I9 × Q5, I9 × P5B | clean each |
| N × I9, CF5 × I9 | **CONFLICT `stage3/test/server.test.mjs`** |
| FU × N | **CONFLICT `stage3/package.json`** (both extend `test:print`) |
| FU × I9 | **CONFLICT `stage3/test/server.test.mjs`** |
| FU × CF5, FU × Q5, FU × P5B | clean |
| I10 `515c9f8` × portal main `aeadcc1` | **clean** (`53a2838…`) |
| I10 × S-1 `89af8ba` (context only) | CONFLICT `BACKLOG.md` only |
| S-1 × `aeadcc1` (context only) | CONFLICT `BACKLOG.md` only |

- **Do NOT hand-resolve any conflict.** For each CLEAN pair with a target on a stale base (I10 × main, Q5 × main, P5B × main,
  Q5 × P5B), archive the merge RESULT into your project and run the suites §6.6 / §7.5 / §8.5 name (PROBED). For I9 × main
  (conflicted in the test file only), run YOUR harnesses on the auto-merged server file (§5.6) — never `npm test` on a tree with
  conflict markers.
- **A GO is a GO at the pinned sha only.** Name, for each target, the cells to re-run on its merged head (at least: N — the 80-cell
  phone file + your render/probe matrix + the print compare, after whichever of FU/N merges second resolves `test:print`; CF5 — the
  stage3 suite + your C contract harness + the real-mail leg; I9 — your capture legs + the builder's two cells after the test-tail
  resolution; I10 — `npm test` + `test:db` on a fresh DB; Q5/P5B — install offline + every suite + (P5B) the emailed-PDF compare, and
  whichever lands second re-validates the lockfile; FU — every FU mutant arm). **CI:** `gh` is not authenticated for `datasecau`;
  every target's CI half is **NOT RUN**, measured at merge.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (`session-tools/nexusai-lock.sh`).
1. **The Vision builder seat is LIVE** (claude `1613`, pane `%41`) and owns portal `:4848` and stage3 `:8080`. **Never use 4848 or
   8080**, nor `47787` (Tuesday's dashboard), nor any port another seat holds. Take every port from the kernel (listen on 0) and bind
   `127.0.0.1` wherever YOUR harness listens. Never start the portal's entry point (it binds `0.0.0.0` in `main()`).
2. **Postgres = the running local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all.**
   Create `vsp_qa_g4_<epoch>` for app runs and `vsp_qa_g4_<epoch>_test` as `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs; the name
   MUST end in `_test` — the portal's guard; never point it at `salesportal`, `salesportal_test`, any `vsp_qa_g1_*`, `vsp_qa_g2_*` or
   `vsp_qa_g3_*` database, or the builder's `vsp_bf1_*`). The connection uses the repo's LOCAL defaults in `server/db.js` /
   `scripts/ensure-test-db.js`; never anything from `Vision_Sales_Portal/4_Credentials/`. Use the `pg` client from YOUR `node_modules`
   (no `psql` here). If `:5433` does not answer, the portal runtime legs are **NOT RUN, blocker named** — do not start a container.
   Leave your databases in place and list their names (no DROP).
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH, HOME = a fresh mktemp dir, TZ, NODE_ENV = `test`
   or `development` — never `production` — PORT, a fresh random SESSION_SECRET / unlock word / `COORDINATOR_SECRET` you generate,
   DATABASE_URL / TEST_DATABASE_URL = yours, PUPPETEER_EXECUTABLE_PATH, `NTFY_SERVER=http://ntfy.invalid`, dummy provider values,
   `npm_config_update_notifier=false`, `npm_config_offline=true`). **NEVER set in a product process:** `AGENTMAIL_API_KEY`,
   `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`,
   `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product
   process's env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh** or any ntfy host: the portal's
   reminder dispatcher (on main since B) reads `NTFY_SERVER` at require time — set `NTFY_SERVER=http://ntfy.invalid` before any
   portal module is required and stub `fetch` to throw on any other URL.
   **Egress — including Chrome children:** the real QuickQuote renderer's page calls three public FX APIs whenever currency ≠ USD.
   **Block it** — gate 3's `qa-chrome-egressblock.sh` (COPY it) as `PUPPETEER_EXECUTABLE_PATH`, i.e. `--host-resolver-rules=MAP * ~NOTFOUND ,
   EXCLUDE 127.0.0.1 , EXCLUDE localhost` plus `--log-net-log` per launch — and **prove the block with a positive control** (one
   renderer page's FX fetch is attempted and fails, recorded). Record outbound connections of EVERY process you start, Chrome
   children included (`lsof -nP -iTCP` over the whole process tree, plus the net-log scan). Anything but `127.0.0.1` is a finding
   against your harness or the product (your own `git ls-remote` head readings and your QUESTION/verdict mails are the only expected
   external calls — say so). **P5B's puppeteer 25 must not fetch a browser** (puppeteer-core never does; `--ignore-scripts` too) —
   confirm in the monitor.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND an entry point of
   either app (the portal's server entry file, the stage3 server file, or your own harness file) ANYWHERE in the remaining argv, from
   the kernel; **"ours" = the ancestor chain CONTAINS your claude pid**. Chrome children of your renderer count as yours and must be
   reaped. **Negative controls, same run, must classify FOREIGN:** the Vision builder's claude `1613` (pane `%41`), Tuesday's claude
   `45678` (pane `%0`), and the NexusAI seat's claude `8360` (pane `%44`) (also live at drafting: `2360` in pane `%47`, the NexusAI
   QA gate 7 seat). Re-read them at start; if one has exited, say so and use the others (gate 3's QA seat `16568` has exited).
   Never by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. Method: gate 3's Vision copy
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate3/evidence/qa-floorcount.py`
   — COPY it into your own evidence folder; edit no original. **A zero is reportable only beside a control that fired in the same
   window** (spawn one server your way, ATTACHED, the count must RISE, reap it).
5. **THE DEADLINE RULE:** every real-server, browser and database step has a written DEADLINE (boot 60 s, request 30 s, render 60 s,
   DB connect 15 s, exit 20 s) and a client timeout on every request (this machine has no `timeout` binary — build deadlines into your
   own runner); a step past its deadline is ABORTED and reported (a hung product request IS a finding). **Every server, browser and
   child you start is killed in a `finally`** (SIGTERM, then SIGKILL after a grace), confirmed by your counter. **Log a HEARTBEAT
   line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**
   N's render matrix and 1 px sweep, CF5's 100-attempt and real-mail legs, FU's 20× loop and every print compare are the shapes that
   hang.

**Reap every server and every Chrome you start.** An orphan of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (App Service `hpas-quickquote`, resource group `hpas-quickquote-rg`, its ACR `hpasqqacr`, its Table
  Storage, its log workspace `hpas-quickquote-logs` — decision 18: never query it) **or the live portal**
  (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the live site, its
  Postgres `datasec-sales-db.postgres.database.azure.com` and key vault). No request to either host, no DB connection to either, not
  even a GET or a health probe. **Never ntfy.sh** or any ntfy host (stub the fetch; `ntfy.invalid`). **Never the three FX hosts**
  (intercept in your browser; block in the renderer). Never the npm registry (`npm audit` included). Never `api.agentmail.to` from a
  product process. Never run the portal `.cursor` rule's curl lines. Never the Feedback_System coordinator.
- The portal: `createApp()` / module functions in YOUR harness, on LOCAL Postgres, `env -i`. QuickQuote: `createApp` in YOUR harness,
  and the offline `index.html` from `file://`.

### HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npm audit`, no `npx` of
  anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Real sends are OFF.** Every provider is a recorder you wrote; nothing reaches ACS, Agent Mail, ntfy or an FX host from a product
  process, a renderer or a browser you drive.
- **Findings-only:** do not commit, do not move any branch, do not file a ticket, do not write inside either repo, inside
  `Vision_Sales_Portal/` (including its `5_Project_History/` screenshot folders), inside `Feedback_System/`, inside the builder's
  scratchpad (READ and COPY only), or inside gate 1's, gate 2's or gate 3's report folders. The gate fixes nothing.
- **NEVER `rm`** — quarantine, per the template §5; every preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate4/report.md`

**QUESTIONS:** if you must ask, mail `tuesday-agent@agentmail.to` with subject `[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>`
(Context / one Question / Meanwhile / Needed-by) and **proceed on the safest reading**; the ANSWER arrives in `tuesday-agent@` with
subject beginning `[Wednesday -> QA/Vision-gate4] ANSWER` — read it with your verdict key. Record every question, the reading you
took and any answer in the report. If a response is cut off by a safety check, record it and continue with the next item; this is
authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 4: C-F5 + item 9 (tier 1) + A-6 round 2 + item 10 + qs advisory + puppeteer 25 + gate-3 follow-ups (tier 2), heads as pinned at launch`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the QA
project has none. Use it ONLY in your own verdict/question/answer-read `curl` (with a client timeout, e.g. `-m 30`); it must never
enter a product process's environment (§13.3). Never put the key, or any secret, in a mail or the report.

Verdict format:
- **N (A-6 r2), CF5 (C-F5 + C2-F2), I9 (item 9), I10 (item 10), Q5 (item 5), P5B (item 5b)** — and **FU (K-F1/L-F1/M-N2/K-O1)** if IN
  — each **GO / NO-GO**, stated SEPARATELY PER TARGET, each naming its pinned sha and branch. For N: N-F1, N-F2, N-F3, N-F4 each
  closed or not, and — if NO-GO — that this was round 2 of 2 and the phone layout ships nothing. For CF5: C-F5 closed (main
  positive control vs branch), C2-F2 closed (its mutant red), and the cap's effect on an outage and on the putOtp half. For I9 / I10:
  markers absent with a positive control that found them on the base. For P5B: "image build NOT RUN; Node 22 NOT TESTED".
- The verbatim strings Kam's publish ask needs: N's before/after in plain words and the 2.32 footer from a real PDF; CF5's 502 text
  for a rejected address as the page renders it; I9's and I10's log lines (operator-visible, not customer-visible).
- Then one paragraph on the queue quoting §12's merge-tree results (or that you skipped them): which GO survives which merge order,
  which cells must be re-run on each forward-merged head, and that every target's CI half is NOT RUN (gh unauthenticated).
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section — at least: real App Service `X-Forwarded-For`; real
  ACS rejection shapes and quota accounting (CF5's real cost); real ACS / Agent Mail / ntfy delivery; `npm audit` (Q5, P5B); the
  Docker image build and Node 22 (P5B) and Node 20 (the current production runtime, for I9's message quoting); CI; real phones /
  Safari / Firefox / widths below 320 (N); multiple replicas (CF5's budgets and cap are per container); every stale-base target's
  forward-merged head (only PROBED)). Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ
  ONLY. §3 Q2-Q7, §4 Q1-Q6, §5 Q1-Q3, §5 Q6, §6 Q1-Q6, §7 Q3-Q5, §8 Q2-Q5 and (if IN) §FU Q2 must each carry one.
- Report each pinned head, and both mains, as three timestamped readings (start / mid / end), each with its branch name.

PROVENANCE:
- heads: portal main aeadcc1c5ec0…, fix/portal-413-passthrough-2026-09-22 515c9f878862…, fix/feedback-report-auth-2026-09-22 89af8ba7817f… (NOT a target); QQ main 763269d8e910…, fix/qq-phone-overflow-2026-09-22 54a72023c04c…, fix/qq-otp-refund-provider-only-2026-09-22 bfb82100aa42…, fix/qq-error-log-no-body-2026-09-22 f2f5f4841ef1…, fix/qq-qs-advisory-2026-09-22 103340c6994b…, fix/qq-puppeteer-25-2026-09-22 0d451004c746…, fix/qq-gate3-followups-2026-09-22 78aa1567c323… | `git -C <repo> ls-remote origin` + `cat-file -t` (all = commit) | read 2026-09-22 22:50:41 AEST (FU 22:53:21)
- chains: 54a7202 → c1abc05 = merge(ac0a8d2, 763269d); ac0a8d2 on 51e9286; bfb8210 on 763269d; f2f5f48 on 51e9286; 103340c = merge(320a169, 51e9286), 320a169 on 47eb533 (⊂ 51e9286); 0d45100 = merge(3d0167e, 51e9286), 3d0167e on 47eb533; 78aa156 → 9ccca8a on 763269d; 515c9f8 on f065675; QQ main 763269d = merge L (f4f7f2b) ← merge K (c1880cb) ← merge C (92581f2) ← merge M (0ab83e1) on 51e9286; portal main aeadcc1 = merge B (97e232d) on f065675 | `git log --format='%h %p %s'`, `merge-base`, `rev-list --count` | read 22:51-22:55
- file sets; lockfile blobs (stage3 64e49cb / Q5 70ebda7 / P5B cdd7699; portal 9d426df); lockfile entry diffs (Q5: 3 versions; P5B: 282 → 242, 55 changes, extract-zip gone, puppeteer-core 25.0.2 engines node >=22.12.0) | `git diff --stat`, `git rev-parse <sha>:<path>`, python over `git show` | read 22:55-23:00
- mechanisms, strings, test names and counts (N 80 cells; CF5 8 new cells; I9 2; I10 5; FU 2 + 2 edited), the minmax commit-vs-comment contradiction, N's screenshot folder (68 PNG + README + shots.json) | `git show`, `grep -c '^test('`, `ls`, `cat` | read 22:52-23:10
- merge-tree table §12 and `b49d1bc` = `c1abc05^{tree}` | scratch `GIT_OBJECT_DIRECTORY` under the drafter's own scratchpad + alternates, run under bash 3.2 | read 22:5x
- seats: %41 → claude 1613 (Vision), %0 → claude 45678 (Tuesday), %44 → claude 8360 (NexusAI), %47 → claude 2360 (NexusAI QA gate 7), %36 → 57419; gate 3's QA 16568 exited; :5433 listening (docker) | `tmux list-panes -a`, `ps -axo pid,ppid,comm`, `lsof` | read 22:58
- builder claims / READY times / Tuesday's rulings | Tuesday daily note `0_Brain/daily_tuesday/2026-09-22.md` 21:42-22:53 lines; Vision `5_Project_History/2026-09-22_kam-decisions-and-publish-pack.md` (decisions 14, 18; "NOT in this publish"); Tuesday's ~22:50 commission and ~22:53 FU message (mail bodies NOT read)
