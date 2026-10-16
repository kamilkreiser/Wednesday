# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 21: ONE TIER-1 QuickQuote gate — PR #10 ROUND 2 (email matches print + the custom-price bound, ratio 10; v2.38) @ `3a3399e` on QuickQuote main `437ab4b` — one verdict, one report

**TIER 1 (quote output to customers: the PDF and workbook a rep emails, which a customer receives).** **ROUND 2 OF 2 of PR #10, under the
two-NO-GO cap. A NO GO here does NOT open round 3: it ships the closed instances and tickets the rest; there is no round 3 without Kam.**
(Round 1 = gate 20, NO GO at `7b952f6` on G20-F1.) So your verdict must say, instance by instance, CLOSED / OPEN / NEW with evidence — that
table (§N10) is what Tuesday ships from and tickets from. "Ships" for QuickQuote still means Kam's own word to publish (C-20); nothing ships on
your verdict.

**Drafted for Tuesday on 2026-10-17 between 07:39 and ~08:2x AEDT by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Model: gate 20's kit (`2026-10-17_vision-gate20-qq-pr10-email-matches-print.md`, its DRAFTER-REPORT, `launch_qa_vision_qq_gate20.sh`) and gate 20's
REPORT (`/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate20-qq-pr10-email-matches-print/report.md`,
NO GO on `7b952f6`; G20-F1..F8, O1-O4, S1-S5). Section shape, identity rules (GET-only `gh` shim), the report-path convention, the verdict token,
THE MODEL RULE, the floor and HELD rules are gate 20's. **Gate 20's whole email-equals-print matrix (§N3-§N5) is KEPT — it found real defects.
This brief governs where they differ, and ADDS §N10 (every round-1 finding re-tested, each able to fail) and §N11 (the bound at its edges).**

**NO DOCKER, as gate 20 — with one changed premise.** The round-2 delta (READ, §Charter) touches the hosted server module (+9 lines: the 422
refusal branch) as well as `index.html`, `stage3/lib/pdf.js`, `stage3/strip.js`, `stage3/package.json` (one script line) and two test files.
`stage3/Dockerfile`, `stage3/package-lock.json`, `.dockerignore`, `lib/xlsx.js`, `lib/mail.js` and `lib/store.js` still carry the SAME blob at base,
round 1 and head. The image would run the same `node strip.js` and the same server module this gate runs in-process (its `createApp()` export),
with the same lockfile. **So no image is built or run, and no `docker` command of any kind is issued** (not even a read). What the published image
does is a publish-time check (§NOT TESTED).

The builder's round-2 mail under test (Tuesday saved it; read it WHOLE; sha256 `303d929851b9c775cb31a1c26d2c7aa4ffa62b61ee7b71c899df10854ab022b8`,
5,416 B, read by the drafter 07:4x):
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-qq-pr10-r2-READY-mail.txt` (READY FOR QA round 2, 20:32:15Z
  2026-10-16 UTC = 07:32 AEDT 2026-10-17, per Tuesday's 10-17 note 07:33)
**Every builder statement below comes from that mail, the commit messages or the code at each sha. Each one is a CLAIM. Every red, every mutant,
every suite set, every browser result and every comparison is RE-DERIVED by the gate. None is taken from the READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads both rows (and `refs/pull/10/head`) by `git ls-remote` immediately before launch,
refusing on any mismatch, **including any move of QuickQuote main** (this gate pins main exactly). The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

GH-API-LEG: READ-ONLY-VISION-TOKEN
<!-- As gate 20 (gate 17's D1). The launcher exports GH_CONFIG_DIR = Vision's .gh-config behind a GET-only `gh` shim first on PATH. Change it to
     NOT-RUN only if Tuesday withdraws the token; then every GitHub read is NOT RUN and the drafter's readings stay READ-BY-DRAFTER. -->

AZ-READ-LEG: TUESDAY-READS
<!-- As gate 20. The gate runs NO az. Tuesday reads the live webapp's linuxFxVersion BEFORE launch, writes it on the line below, and reads it again
     at verdict. The gate RELAYS. -->
AZ-PRE-READ: @STAMP@
<!-- One line, e.g. `linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:<tag> ; read <YYYY-MM-DD HH:MM:SS AEDT> by Tuesday (az, Vision's own
     AZURE_CONFIG_DIR, tenant d500ebad / sub 0c57ab37)`. The launcher refuses until it names linuxFxVersion. Drafter's expectation (NOT a reading):
     v0.6.4-tool2.36-437ab4b (Tuesday's 10-17 note 07:17: post-read 07:16:24 = v0.6.4-tool2.36-437ab4b, unchanged). -->

N4-METHOD: TUESDAY-DECIDES
<!-- Decision D5 (§N4). Exactly one of:
       FULL-TEXT  (gate 20's ruling, the drafter's reading again) the emailed PDF's text (pdftotext -layout) must EQUAL the printed PDF's text (the
                  page's own Generate, print media, A4, same state) after normalising ONLY the quote-number token; any other differing line is a FAIL.
                  The money multiset, page count, fonts and a pixel diff are reported beside it.
       FIGURES    money figures equal, in order; other text differences are REPORTED, not FAILs. The FULL-TEXT rows still run and are reported.
     The launcher refuses while it reads TUESDAY-DECIDES. -->

ROUTING-LINE: @STAMP@
<!-- Tuesday adds `QA/Vision-gate21|tuesday-agent@agentmail.to|no` to /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf (pattern:
     the QA/Vision-gate20 line) and stamps this line, e.g. `QA/Vision-gate21 added to inbox_routing.conf <HH:MM> by Tuesday (.pre-1017-gate21 backup)`.
     The launcher refuses while either the conf line is absent (guard 41) or this line carries the placeholder (guard 32). The drafter did NOT edit
     the conf (at drafting it ends at QA/Vision-gate20). -->

## Charter
Read `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this change and you owe the builder nothing. **Every line below that reports what the builder says is a CLAIM, never evidence.**

**One gate, ONE target, ONE verdict: GO / GO WITH FINDINGS / NO GO, at its pinned sha.**
- **QQEP** at `3a3399e` — **TIER 1 (quote output to customers).** ROUND 2 of 2 of PR #10 (round 1 = gate 20, NO GO at `7b952f6`).
  QuickQuote PR #10, branch `fix/qq-email-matches-print-2026-10-16`. SIX commits over main `437ab4b`, a straight line; round 2 added three on top
  of round 1's head with no force-push (READ: `7b952f6` is an ancestor of `3a3399e`):

| # | commit | parent | what it is |
|---|---|---|---|
| 1 | `0fc280b` (author 2026-10-16 14:13:19 +1100; committer 2026-10-17 05:32:41 — rebased) | `437ab4b` | round 1: the emailed PDF and workbook follow the rep's print mode and custom price (C-20 fix 2) |
| 2 | `a8d769b` (05:32:41) | `0fc280b` | round 1: remove the v2.36 email guard |
| 3 | `7b952f6` (05:43:02) | `a8d769b` | round 1: test wording. **ROUND 1'S HEAD — gate 20's NO GO** |
| 4 | `a7e1835` (07:24:58) | `7b952f6` | "fix 2 round 2: bound the custom price, keep key-by-key entry, clear it on reopen (gate 20; v2.38)" — `index.html` +60/−13, `lib/pdf.js` +20/−5, `package.json` +1/−1, the hosted server module +9, `strip.js` +14, new `test/custom-price-bounds.mjs` +268 |
| 5 | `1f7db41` (07:24:58) | `a7e1835` | "test: email-matches-print sees a rounded custom price (G20-F7)" — `test/email-matches-print.mjs` +28/−12 |
| 6 | `3a3399e` (07:28:12) | `1f7db41` | "fix 2 round 2: inset the custom-price refusal like the margin line" — `index.html` +2 (CSS: `#cpRefused { margin: 0 1.1rem .55rem; }`). THE HEAD |

**THE DELTA THAT SHIPS is `git diff 437ab4b 3a3399e` (8 files, +657/−119)** — the same eight files and counts as the PR files API (READ-BY-DRAFTER,
`gh api …/pulls/10/files`, 07:42:14 AEDT): `index.html` +115/−30 blob `cf71c84`; `stage3/lib/pdf.js` +51/−13 `257bbfa`; `stage3/package.json` +1/−1
`cd9118a`; the hosted server module +9/−0 `e40c20e`; `stage3/strip.js` +25/−26 `9cddb70`; `stage3/test/custom-price-bounds.mjs` added +268 `76368d2`;
`stage3/test/email-matches-print.mjs` added +165 `bdb602b`; `stage3/test/email-print-mode.mjs` +23/−49 `9dd5311`. PR `changed_files` 8, additions 657,
deletions 119, state open, merged false, draft false, mergeable_state clean, updated 2026-10-16T20:31:49Z.

**THE ROUND-2 DELTA is `git diff 7b952f6 3a3399e` (7 files)** — what round 2 changed on top of what gate 20 measured:

| file | +/− (7b952f6→3a3399e) | r1 → head blob | what (READ at the pinned shas) |
|---|---|---|---|
| `index.html` | +62 / −13 | `51c6eb9` → `cf71c84` | toolVersion `"2.37"` → `"2.38"`; `CONFIG.customPriceMaxRatio: 10`; new `cpCheck(usd)` (null when `typeof usd === "number" && Number.isFinite(usd) && usd > 0 && usd <= (c.stdPerDevMonth / c.fxRate) * CONFIG.customPriceMaxRatio`, else the sentence) and `cpRefuse(msg)` writing `#cpRefused`; `cpSyncFrom` refuses through `cpCheck` before setting `cpState` (a NaN/empty entry clears with NO message); `renderCustom(skipId)` skips the field being typed and a `change` listener tidies it; `btnApplyPct` refuses through `cpCheck`; `btnResetCustom`/`cpClear` clear the refusal; `window.cpRestore` returns `cpCheck`'s sentence (restoring nothing) or null; new `<div class="svc-warn" id="cpRefused" role="alert">` under `#ctMargin`; CSS inset for it |
| `stage3/lib/pdf.js` | +20 / −5 | `2e692d3` → `257bbfa` | on an advanced render: a non-null/defined `pdmUSD` goes through `cpRestore`; a sentence → `return { refused: why + " The quote was not sent." }`; a null/absent price with `pmCustom`/`pmBoth` posted → `refused` ("This quote asks for custom pricing but carries no custom price, so it was not sent. Reload the page and press Email again."); after the evaluate, `report.refused` → `{ pdf: null, xlsx: null, report }` (the page closes in the existing `finally`) |
| the hosted server module | +9 / −0 | `a854ba2` → `e40c20e` | in `/api/quote/email`, after `renderQuotePdf`: `report.refused` → `store.updateQuote(qnum, { status: "refused" })` (errors logged, not thrown) and `res.status(422).json({ error: String(report.refused) })`. The C-05 reservation (`status: "pending"`) happens BEFORE the render, so a refusal consumes a number |
| `stage3/strip.js` | +14 / −0 | `7c37287` → `9cddb70` | in `HOSTED_EXTRAS`' reopen handler: `clearCustom()` (returns whether `cpExport()` was non-null, calls `window.cpClear()`, empties `cpPct`) runs after a successful fetch and BEFORE `apply(j.state)`; when it cleared one the note adds "Custom pricing is not saved with a quote, so it is off; enter it again if this quote needs it." |
| `stage3/package.json` | +1 / −1 | `725a5e2` → `cd9118a` | `test/custom-price-bounds.mjs` inserted into `test:print` after `test/email-matches-print.mjs`. No dependency line changes |
| `stage3/test/custom-price-bounds.mjs` | +268 | — → `76368d2` | new, 15 cells, through `createApp()` with the real `renderQuotePdf`, its OWN `memStore()` (written in the file, not lifted from `server.test.mjs`), a capturing mail stub, a real Chrome signed in by OTP and unlocked by the word through the UI, FX lookups aborted: F1 page paste 1e308; F1 Apply −100 %; F1 crafted pdmUSD × {1e308 custom, 1e308 both, 0, −1, "27.9", {}} (6); F1 custom mode with NO price; a sane control; F2 key-by-key × {cpMonth 27.37, cpDay 0.9137, cpYear 333.33, cpTerm 999.99} (4); F6 reopen |
| `stage3/test/email-matches-print.mjs` | +28 / −12 | `3ac0e3c` → `bdb602b` | the 9 cells kept (same names); 3 new fleet-scale cells (2,500 devices, 5 yr, −7.77 %: custom AUD, custom CAD, both AUD); the workbook loop now advances `at` (order enforced). STILL hands the recorded body directly to `renderQuotePdf(state, {advanced: true})` — never through the route |

**Same blob at base, round 1 and head (READ, `rev-parse <sha>:<path>`, 07:4x):** `stage3/package-lock.json` `01c5e5e`, `stage3/Dockerfile` `8311ebe`,
`.dockerignore` `acf7db8`, `stage3/lib/xlsx.js` `10bf4d7`, `stage3/lib/mail.js` `3aa8922`, `stage3/lib/store.js` `0609594`, `stage3/login.html` `f362b45`,
`.github/workflows/tests.yml` `ec450f5`, `quote-engine.test.mjs` `2d193b6`, `stage3/test/server.test.mjs` `b35a2eb`, `CLAUDE.md` `af402a7`.
`stage3/test/email-print-mode.mjs` is `9dd5311` at round 1 and head. Head tree `ec15fb2`; round-1 tree `25ddfb8`; main tree `c71780c`.

**Names, written out every time:**
- **QQEP** = branch `fix/qq-email-matches-print-2026-10-16` = PR #10 = "fix (2)" = the delta above. **R1** = round 1's head `7b952f6` (gate 20).
  **MAIN-Q** = QuickQuote main `437ab4b` = **what is LIVE** (v0.6.4-tool2.36-437ab4b, AZ-PRE-READ confirms). **C-20** = Kam's ruling, card
  `quickquote-email-sends-standard-not-custom-1016` = (a).
- **THE BOUND** = `cpCheck`: a custom price (USD per device per month) is accepted only if it is a finite number, **more than zero**, and **at most
  `CONFIG.customPriceMaxRatio` (10) × the standard per-device price** of the CURRENT form state (apps/bundle; currency-invariant in USD). With the
  seeded rates and the full bundle (USD 20.00 standard): max **US$200.00 / A$310.00 / CA$284.00** per device per month; Manager only (USD 5.00): max
  US$50.00 / A$77.50 / CA$71.00 (drafter arithmetic from CONFIG, NOT a measurement). **The ratio 10 is the builder's choice** ("sits in CONFIG for Kam
  to change"), a fact for Kam's publish card.
- **THE REFUSAL SENTENCE** = "A custom price must be more than zero and no more than 10 times the standard price of <std>/device/month." + "Custom
  pricing is off until you change it." (fields) / "The percentage was not applied." (Apply %) / "The quote was not sent." (email, HTTP 422).
  **THE NO-PRICE SENTENCE** = "This quote asks for custom pricing but carries no custom price, so it was not sent. Reload the page and press Email
  again." **THE REOPEN SENTENCE** = "Custom pricing is not saved with a quote, so it is off; enter it again if this quote needs it."
- **W1 / W2 (RETIRED)** = Kam's two guard sentences (card `quickquote-guard-words-1016`); retired by PR #10. sha256 (absence checks only):
  W1 `0d5beedb47709eed6c7c6eec5d8ced3e73c58069ea09f49f4495cde1abeb25b9`, W2 `4c73c1593e64f73dc84d24c48a69896307108d387b70a9318b0d7f7dd3ec797d`.
  W1 begins `This email sends standard pricing only.`; W2 is `Send standard pricing anyway`.
- **THE NOTE** = the "Custom pricing note" (`.q-savings`); **THE VALUE NOTE** = the standard `.q-savings` "Value note"; **PRINT CSS** =
  `#quoteDoc .q-savings { display: none !important; }` inside `@media print` (`5ef2a60`, v1.88; the builder's backlog `cdcd490`).
- **`svc-warn`** is now ALSO the class of the new `#cpRefused` box (legitimately, when a price is refused). The W1-era rule "never `svc-warn`" applies
  to `#emailPdfNote` only.

Branch status: **NOT on main. PR #10 is open, not merged, not draft** (READ-BY-DRAFTER 07:42:14 above). `refs/pull/10/merge` =
`1345ea5ec9817a6c290f9682f288c2b1bc5e94c8` (GitHub's test merge, NOTE only). PR #8 (`4d6ed6e`) still open.

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole (C-01..C-20 at drafting; the last is C-20). **Cite only what you open.** The entries this gate turns on:
  - **C-20 (Kam, live board 2026-10-16 13:25:51 AEDT, card `quickquote-email-sends-standard-not-custom-1016` = (a)):** "Publish the guard as soon as
    it passes the gate, full fix after". **"Kam's grant covers the GUARD only. Fix (2) and PR #8 (C-19) each need Kam's own word before any publish."**
    "Do not contact anyone who received an emailed quote."
  - **C-05** (reopen a quote by its number): background for §N3 P6 and §N10 G20-F6.
- **Tuesday's rulings already made — the gate checks them AS BUILT and does not re-open them:**
  - **The note** (Tuesday 2026-10-16 ~14:02): OFF the email, ON the print; reversible by Kam on the publish card. (Gate 20 measured it is on screen
    only, and only in "Standard + custom": G20-F5. Unchanged by round 2; re-measured in §N4.4.)
  - **The guard's removal** (Tuesday 2026-10-17 05:4x): W1/W2 RETIRED; their absence is checked, their wording is not graded.
  - **G20-F1 is a FAIL** (Tuesday's ANSWER to gate 20, 2026-10-17 06:58:14 AEDT, quoted in gate 20's report): *"RULED: yes. The §N3 FAIL clause APPLIES
    to the pasted 1e308 custom price that emails "A$∞"."* Its fix-shape: *"bound the custom price both where it is set and where it is rendered. A
    finite upper bound (or a sanity ratio to the standard price) applies on the page field and in lib/pdf.js before cpRestore. A non-finite or
    out-of-bound pdmUSD is refused with a message, never rendered."* Its regression cell: *"your P8p paste case"*. **You grade round 2 against that
    fix-shape, clause by clause (§N10).**
  - **Round 2 rulings (Tuesday's 10-17 note 07:17 and 07:33):** round 2 to the builder for G20-F1, F2, F7; F8 ticket allowed unless the fix was
    trivial (the builder ticketed it: backlog `815aae7`); **the ratio-10 bound is the builder's choice and a fact for Kam's publish card**.
  - **The access word (Tuesday's 10-17 note 07:40):** the builder's S5 answer cites Kam's 2026-08-11 ruling recorded in the server module's comments
    (the word is a workflow gate, not a security control). NOT this gate's subject. **You never read, print, grep for, type or reproduce the access
    word or the offline page's constant** (gate 20 self-finding S5: a grep printed the offline constant — do not repeat it; never grep the ADVANCED
    SEAM region of `index.html` with output to your terminal or report).
- **PRODUCTION IS LIVE for this project.** Live QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, its registry `hpasqqacr`, its Table Storage and
  its log workspace) and the live portal (`datasec-sales-portal.azurewebsites.net`, `datasec-sales-portal-rg`) are PRODUCTION. **Nothing in this gate
  touches either** (§13, HELD). The gate makes no Azure contact at all (AZ-READ-LEG = TUESDAY-READS).
- **THE LIVE CHECK IS KAM'S, NOT YOURS.** (Tuesday 2026-10-16 15:07: "do NOT read HPAM_WORD; live check 2b moves to Kam.") **You never press anything
  on the live site, never request any URL of it, and never read, ask for or type the HPAM access word.** The unlock word in your harness is a fresh
  random string you generate.
- **Merging and publishing are HELD. Nothing merges or publishes on your word.**
- **The BUILDER's round-2 choices, each judged by the gate (say whether each needs Kam):** (1) the bound is a RATIO (10) to the standard price of the
  CURRENT form state, not a fixed figure; (2) the lower bound is "more than zero", so any positive price, however small, is accepted (WRONG (e));
  (3) a non-numeric or empty entry clears custom pricing SILENTLY (no sentence) (WRONG (f)); (4) the renderer refuses ANY non-null `pdmUSD` that fails
  the bound, in ANY print mode, including "Standard pricing only" (WRONG (b)); (5) a custom print mode with no price is refused (422) rather than
  emailed standard — which changes what a v2.36 tab gets after a v2.38 publish (WRONG (h)); (6) a refusal consumes a quote number and stores the row
  as "refused" (retained until normal retention; not reopenable); (7) reopen clears the custom price and print mode, so reopening A in the SAME page
  now comes back standard (the builder's "behaviour note"); (8) F8 ticketed, not fixed; (9) the new test file has its OWN `memStore()`, and
  `email-matches-print.mjs` still bypasses the route (WRONG (i)).

## PRIOR ROUND
PRIOR ROUND: round 1 gated `7b952f6edbcc3b271e4a650685f47b87760ed8f0` (gate 20), verdict NO GO (round 1 of 2, not PROVISIONAL), 2026-10-17 07:15:31 AEDT.
ITS REPORT IS ON DISK AT: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate20-qq-pr10-email-matches-print`
(`report.md`, sha256 `ab77c0063de867d8df2f0a9d9dd5436038f0774d6e47c3e0757e770615011bcb` at drafting; `evidence/`, `evidence/tools/`,
`evidence/mail/verdict-body.txt` sha256 `f16c98fb91d62101d1ace37303bacbcddce6a92af0b8319a067156a4e56b84d9`). **Read `report.md` whole, and the verdict
body.** (The coordinator's mail batch file `/private/tmp/wed_newmail/batch_20261016T203647Z.txt` carries the verdict ROW, subject
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 20: QQEP @ 7b952f6 NO GO`, 20:15Z, but its body field reads `None`; the body you read is
the gate's own saved copy.)
Findings carried forward and their disposition (each a CLAIM until §N10 measures it):

| round-1 finding | severity (gate 20) | builder's disposition (READY / commits) | §N10 check |
|---|---|---|---|
| **G20-F1** pasted 1e308 → "A$∞" printed AND emailed; same class `pdmUSD: 0` → A$0.00 "Custom Quote" | **Major — the FAIL (NO GO)** | FIXED `a7e1835` (cpCheck, ratio 10; page, renderer, route 422) | R1-F1 + §N11 |
| **G20-F2** key-by-key entry clobbered (27.37→2.02, 0.9137→0.0002, 333.33→3.00, 999.99→9.04), now emailed | Major, pre-existing | FIXED `a7e1835` (`renderCustom(skipId)`, tidy on `change`) | R1-F2 |
| G20-F3 a v2.37 tab across a rollback to v2.36 emails standard silently | Minor, publish card | untouched; "a v2.37+ tab after a rollback to v2.36 still emails standard silently" | R1-F3 (re-measure P11b with v2.38) |
| G20-F4 the lone revert of `a8d769b` makes W1 false | Minor, publish card | untouched | R1-F4 (re-measure P12) |
| G20-F5 `emailCopy` invisible to the customer | Minor, publish card | untouched | R1-F5 (re-measure M4) |
| G20-F6 reopen B while A's custom price is live re-issues B at A's price | Minor | FIXED `a7e1835` (`clearCustom` on reopen) | R1-F6 |
| G20-F7 no cell sees G20-M2; workbook `at` never advanced; both tests stub the route | Minor, test strength | FIXED `1f7db41` (3 fleet cells; `at` advanced); the new bounds file goes through `createApp()` | R1-F7 |
| G20-F8 print before the live FX rate lands, then Email: paper at seed, email at live | Minor, pre-existing class | TICKET `815aae7` (backlog) | R1-F8 (ticket verified; race re-measured, not graded) |
| O1-O4 (no `aria-live` on `#emailPdfNote`; drawer −19.2 px at 320 px; 4 unprinted workbook cells; stale `pdmUSD` after Advanced off) | pre-existing | untouched | re-observe; O4 now matters (WRONG (b)) |

**Instruments are REUSED BY COPY from gate 20's `evidence/tools/`** (it holds gate 19's copies as well): `qa-run.py`, `mktree-qq.sh`, `lockcmp.py`,
`lockwalk.py`, `tapsets.py`, `g17-dupnames.py`, `g20-run-suites.sh`, `g20-mutate.py`, `g20-mutant-arm.sh`, `g20-compare.py`, `g20-n4-run.py`,
`g20-n4-multi.py`, `g20-n5.py`, `g20-gh.sh`, `g20-cell.sh`, `g20-arm.sh`, `g20-repoint.py`, `qa-harness-g20-drive.cjs`, `qa-harness-g20-offline.cjs`,
`qa-harness-g16-shots.mjs`, `qa-chrome-egressblock.sh`, `qa-chrome-census.py`, `qa-egress-posctl.mjs`, `qa-floorcount.py`, `qa-harness-floorctl.mjs`,
`qa-netlog-scan.py`. **COPY what you use into THIS gate's own `evidence/tools/`, read it before you trust it, and RE-POINT every hard-coded path**
(gate 20's copies hard-code `work-g20`, the gate-20 report folder, `@qa-g20.invalid` and `v2.37`). **Never edit, run from, or write into gate
1-20's copies, evidence or trees** (`work-g20/` included). Record the sha1 of each copy before and after your edits. Set `qa-run.py`'s deadline
ceiling to §13.6's in YOUR copy only, and say so. **The drive harness must learn the 422 path:** a refused send returns no PDF and no mail — record
the status, the body, the note text and the store row; never treat "no PDF" as a harness error.

**Self-findings from earlier gates bind you:** quote every path (space and `!`; the repo sits under `Quoting Tool/`); run every loop and every
`git show <sha>:<path>` under **bash, not zsh**; run `node strip.js` before any lone browser file; assert every tamper landed before reading its
result; npm's update-notifier egresses unless disabled; record the load beside every timing; `git branch` and `git for-each-ref` are NOT read verbs
here; puppeteer-core's `click({clickCount: 2})` is ONE press — two real clicks N ms apart are a double-press; the Settings drawer is 340 px wide;
**take the floor count at START as well as at END** (gate 20 took END only — its own stated omission); **one tab, foreground, for every reopen**
(gate 20 S3: a background-tab click VOIDed P6 twice); **sign-in addresses lower-case** (gate 20 S4); **never print the access word or the offline
constant** (S5).

**PRIOR WORK: verify every claim against git history and the Actions API (GH-API-LEG), never against this brief.** The READY's claims (RED 14/15 on
`7b952f6`, GREEN 15/15; M2 fails 3/3 fleet cells; 69/132/200/6; "all 9 real PDFs text-identical to round 1 apart from the version"; refusal
screenshots without overflow; backlog `815aae7`; CI green incl. CodeQL and store-azurite; 0 open code-scanning) are re-derived or marked UNVERIFIED.

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head and no `@`; the head is a commit; for QQEP the base is an ancestor AND the merge-base
with MAIN; `git rev-list --count base..head` equals `commits`; the chain is exactly `437ab4b` ← `0fc280b` ← `a8d769b` ← `7b952f6` ← `a7e1835` ←
`1f7db41` ← `3a3399e` (single parents); R1 `7b952f6` is an ancestor of the head; `git ls-remote origin refs/heads/<branch>` equals the head NOW **for
BOTH rows — a moved main REFUSES (re-pin and re-brief)**; `refs/pull/10/head` equals the QQEP head NOW; QQEP is not on main and is 0 behind it.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-Q | quickquote | main | 437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6 | - | - | IN |
| QQEP | quickquote | fix/qq-email-matches-print-2026-10-16 | 3a3399e947bf5faf8a8e0c0d3e11956c6590db98 | 437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6 | 6 | IN |
<!-- PIN-HEADS:END -->

Both rows: `git -C <quickquote> ls-remote origin` read by the drafter at **2026-10-17 07:39:16 AEDT**: `HEAD` = `refs/heads/main` = `437ab4b…`,
`refs/heads/fix/qq-email-matches-print-2026-10-16` = `3a3399e…` = `refs/pull/10/head`, `refs/pull/10/merge` = `1345ea5…` (NOTE only),
`refs/pull/8/head` = `4d6ed6e…` (open), `refs/heads/backlog/qq-extract-zip-2026-10-16` = `815aae7…` (the builder's backlog branch: F8's ticket).
`rev-list --count 437ab4b..3a3399e` = 6; `3a3399e..437ab4b` = 0; merge-base `437ab4b`; `7b952f6` is an ancestor of `3a3399e`. **The head did not move
from the READY's `3a3399e`.**

Repo: quickquote = `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool` (remote `datasecau/vision_hpas-quickquote`).
**The T9 copy of this repo is STALE. Never read it.** Its rules: the repo's own `CLAUDE.md` (read at the head with `git show`; its deploy and publish
lines are NOT for you) and `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (its QuickQuote section). **The builder's checkout is
LIVE: never use the name `main` in the repo, always the pinned 40-hex sha; never read any working tree as evidence; build every tree from the object
store.** **If PR #8 merges while you run, main moves:** your pins stay valid (they are shas), say so in the three readings and do NOT re-base anything —
the verdict is on `3a3399e` over `437ab4b`.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; all are claims)
**These are the TRAPS: places where round 2's fix could pass the builder's cells, or gate 20's matrix, without fixing the defect, or fix it and
break something else.**
- **(a) The round-2 READY carries no NOT TESTED block either.** Case-insensitive count of "not tested" 0, "not run" 0 (READ). You build the NOT TESTED
  list yourself (§14) and say that the READY had none.
- **(b) The bound is checked when a price is ENTERED, against the standard price AT THAT MOMENT — not re-checked when the form changes, while the
  renderer re-checks against the POSTED state.** The ratio's denominator is `stdPerDevMonth`, which depends on the APP SELECTION (bundle USD 20.00 vs
  Manager-only USD 5.00 + 3.50/app). Set A$300.00 (9.68×) on the full bundle, then untick apps down to Manager only (now ~38.7×): `cpState` stays
  A$300.00, the page keeps pricing and PRINTING it, and the renderer REFUSES it (422) — **and it refuses in ANY print mode, because `pdf.js` calls
  `cpRestore` for every non-null `pdmUSD`, so a rep on "Standard pricing only" with a stale custom price behind it gets "A custom price must be…
  The quote was not sent." for a STANDARD quote.** The same reaches the stale `pdmUSD` posted after Settings → Advanced off (gate 20's O4: the post
  still carries it). READ-ONLY-INFERRED. **§N11 B-STATE and P3' measure it.** A refused STANDARD email for a state a rep reaches through the page's own
  controls is a FAIL (§N3's clause). A custom state the page prints but the email refuses is a finding (the customer never gets a wrong document,
  but the rep cannot send what they printed); severity yours.
- **(c) A red at `7b952f6` can be for the wrong reason.** On `7b952f6` the `#cpRefused` element does not exist, so a bounds cell that FIRST reads the
  refusal text fails on "no element" — the absence of new UI, not proof that its ∞/A$0.00/422 assertions can fail. The crafted-post cells fail on
  `200 !== 422` (a contract change, the right reason only if "nothing mailed" is ALSO shown false at R1). **§N2 quotes every red cell's first failing
  assertion, classifies it DEFECT-REASON or NEW-SURFACE-ABSENT, and uses mutants at the head (§N2.3) to show each defect assertion can fail.**
- **(d) The builder's bound cells test only ABSURD values.** 1e308, 0, −1, "27.9", {}, −100 %. No cell probes the edge (10× ± a cent). A ratio of
  1000, or 1e300, would pass every one of them (1e308 still exceeds 1e300 × 20). **Mutant G21-M4 (ratio 10 → 1000) is expected to be seen by NO
  committed cell** — a test-strength finding, not a FAIL; §N11 measures the edge directly.
- **(e) "More than zero" leaves the "A$0.00 Custom Quote" class open.** `cpCheck` accepts any positive number: a pasted `0.001` /month, a `cpDay` of
  `0.0001`, or Apply % `−99.99` gives a price that the ticket and the paper print as **A$0.00/device/month** (display `toFixed(2)`), a "Custom Quote"
  the email then carries. Gate 20 put `pdmUSD: 0` → A$0.00 in G20-F1's SAME CLASS. READ-ONLY-INFERRED (`cpCheck`: `usd > 0`). **§N11 L-EDGE
  measures it; report whether a document reading A$0.00/device/month is still reachable, and say F1's same class is OPEN if so** (severity yours;
  the §N3 FAIL clause names NaN/undefined/Infinity, not A$0.00 — Tuesday rules if you need a ruling; ask, and proceed on "finding, not FAIL").
- **(f) "The four fields and Apply % refuse anything else with a message" — not for a non-numeric entry.** In `cpSyncFrom`, `isNaN(raw) || value.trim()
  === ""` → `cpRefuse("")`, `cpState = null`: custom pricing is turned off with NO sentence, and `renderCustom` puts the print mode back to "Standard
  pricing only" (READ, index.html ~3478-3486). The fields are `type="number"`, so a pasted `abc`, `1,234.50`, `27,90`, `A$27.90` or `1e309` likely
  reads back as `""` (Chrome's number sanitisation; UNVERIFIED). **§N11 measures each paste: the field's value read back, `cpState`, the sentence (or
  silence), the mode, the print and the email.** A silent switch to standard is NOT an email≠print FAIL (both are standard) — a finding against the
  READY's claim; severity yours.
- **(g) Typing still passes THROUGH refusals, and a refusal drops the print mode.** Each keystroke runs `cpSyncFrom`; any intermediate value outside
  the bound (a leading `0`, a cleared field during backspace, `1e` mid-typing) sets `cpState = null`, which switches "Custom pricing only" back to
  "Standard pricing only"; a later valid keystroke restores the PRICE but not the MODE. And `#cpRefused` (`role=alert`) flashes the refusal on the way.
  READ-ONLY-INFERRED. **§N10 R1-F2' types over an existing price key by key while in custom mode** (backspace ×N then digits; and "0.5"): report the
  mode at the end, what printed, what was emailed, and the alert's transient text. Not a FAIL if email = print; a finding.
- **(h) Mixed versions change shape (G20-F3 and P11a).** The v2.38 renderer REFUSES a custom print mode with no price. A v2.36 tab open across a v2.38
  publish shows W1 ("…press the button again to send standard pricing anyway"), and its second press posts `pmCustom: true` with no `custom` key →
  now **422 THE NO-PRICE SENTENCE** instead of the standard email W1 promised (READ-ONLY-INFERRED). The reverse (a v2.38 tab across a rollback to
  v2.36) is G20-F3 unchanged: the builder says so. **P11 measures both with the v2.38 head.** Findings for the publish card, never a FAIL of the head.
- **(i) The route is still bypassed by the 12 email-matches-print cells**, and the 15 bounds cells use the test file's OWN `memStore()` (not the repo's
  `lib/store.js`, not lifted from `server.test.mjs`): its `updateQuote` is a plain merge. **`status: "refused"` has never met Azure Table Storage**
  (store-azurite is an unchanged blob and does not exercise it) — NOT TESTED beyond READ: `lib/store.js` `updateQuote` is `updateEntity(…, "Merge")`;
  the retention purge deletes non-pending rows only at full retention, so a refused row (with its stored customer state) lives as long as a sent one.
- **(j) The server-module change voids gate 20's "unchanged server module" premise.** Gate 20 READ the route as an unchanged blob; at the head it is
  `e40c20e` (+9). **§N1.4 re-reads the route whole; §N8.3 lists it in what a publish ships.** The 422 sits BEFORE the `report.qnum !== qnum` check and
  AFTER the reservation, so a refusal consumes a number (`DSQ-…-H0n` advances) — report it.
- **(k) CodeQL on PR refs is a blind instrument** (gate 17 WRONG (a); gates 19-20 N9.2). On `3a3399e` (READ-BY-DRAFTER 07:42:14): `CodeQL` success "No
  new alerts in code changed by this pull request", `Analyze (javascript-typescript)` and `Analyze (actions)` success; code-scanning open alerts:
  main 0, `refs/pull/10/head` 0. Say only what they can show.
- **(l) "Version is now 2.38, because gate 20 tested a build labelled 2.37."** TRUE at source (`a7e1835`, `toolVersion: "2.38"`; READ). `stage3/package.json`
  `version` stays `0.3.2` (READ). §N5 counts `v2.36`→`v2.38` against main and `v2.37`→`v2.38` against R1.
- **(m) "Real PDFs … all 9 are text-identical to round 1 apart from the version"** (READY) — a claim about the builder's own state; **§N5.4 measures
  it in yours** (head vs R1, same inputs, frozen clocks).
- **(n) `clearCustom` relies on `window.cpClear`.** In the hosted simple page that is the strip's no-op stub; in an advanced page the module rebinds it
  to the real one (`strip.js` module wrapper: `window.cpClear = cpClear`; READ). `had` is read from `cpExport()` BEFORE the clear. If the module were
  not loaded the note would claim "it is off" without clearing anything; **§N10 R1-F6 asserts the price IS cleared (`cpExport() === null`, mode
  default, the fields empty) and not only that the sentence appears.**
- **Verified TRUE at source (READ 07:39-08:1x):** both heads + `refs/pull/10/head` by `ls-remote`; the 6-commit chain and single parents; 6 ahead / 0
  behind; 8 files whole, 7 in round 2, numstat = the PR files API; the unchanged-blob list above; the `test:print` line (two files inserted after
  `test/email-print-mode.mjs`); `cpCheck`/`cpRefuse`/`customPriceMaxRatio: 10`/`renderCustom(skipId)`/`#cpRefused role="alert"`/toolVersion `"2.38"` at
  the head; `pdf.js`'s two refusals; the route's 422 and `status: "refused"`; `clearCustom` in `HOSTED_EXTRAS`; W1/W2 absent from the head's
  `strip.js`; CI runs 38962577169 (push) and 38962582879 (pull_request) on `3a3399e`, `completed success`, and the check runs on `3a3399e` (13, all
  success); PR #10 open, not draft, mergeable_state clean; backlog `815aae7` (2026-10-17 07:25:21, BACKLOG.md +8: the G20-F8 entry, and the G19
  entry noted as lapsing with PR #10) — tip of `backlog/qq-extract-zip-2026-10-16`, not an ancestor of the head; Vision's gh-config mtimes unchanged by
  the drafter's GETs (12 Oct 18:09:30).

## THE READY — its claims and NOT TESTED (the gate rules on every claim)
Read the mail whole. **The round-2 READY carries no NOT TESTED block (WRONG (a)).** Its claims, one line each (each a CLAIM, re-derived in §N):
round 2 of 2, head `3a3399e`, new commits on `7b952f6`, no force-push, v2.38; G20-F1 by `cpCheck` (a number, more than zero, at most
`CONFIG.customPriceMaxRatio` (10) × standard) on the four fields and Apply % (`#cpRefused`, `role=alert`; custom pricing stays off; "nothing says ∞"),
in the renderer before anything is drawn (and a custom mode with no price), and on the route (422, nothing mailed, row "refused"); regression cells
through the REAL server path (paste 1e308, −100 %, crafted 1e308 custom/both, 0, −1, "27.9", {}, `pmBoth` + null; a sane control); G20-F2 by
`renderCustom(skipId)` (27.37 / 0.9137 / 333.33 / 999.99 key by key; `cpExport` = typed/rate to 1e-9); G20-F7 (3 fleet cells; M2 fails 3/3; the 9
still pass; `at` advanced); "custom-price-bounds.mjs: RED 14/15 on 7b952f6 (only the sane control passes), GREEN 15/15 at head"; G20-F6 FIXED
(reopen clears price + mode; same-page reopen now standard); G20-F8 TICKET (`815aae7`); local 69/69, 132/132, test:print 200/200 (182 + 15 + 3),
6/6; CI on `3a3399e` all green incl. CodeQL, store-azurite and test:print running both new files; 0 open code-scanning; 9 real PDFs text-identical to
round 1 but for the version, pages 2/2/3 A4; refusal screenshots light/dark 1280/375 without overflow; the S5 answer (NOT this gate's subject; never
re-derive it — WRONG list and RULED); the FOR KAM sentences; "The ratio 10 is my choice and sits in CONFIG for Kam to change."; F3 still silent after
a rollback.

**How you treat these:** every claim you CAN test, you test. **test:azurite** stays NOT RUN here (no docker; `lib/store.js` is an unchanged blob) —
relay CI's `store-azurite` as READ ONLY, and say it does not exercise `status: "refused"` (WRONG (i)). **A real ACS send** stays NOT TESTED (no real
mail, ever); its nearest substitute is §N3/§N4: the real server path with a capturing stub mail. **The live site** stays NOT TESTED (Kam's check).

## 2a. LEGITIMATE SHAPES — what an ordinary rep produces, and what the email must then be
**Fix (2) is not a checker, but round 2 ADDS one: THE BOUND refuses prices. A false refusal of an ordinary quote is damage in its own right (a rep
who cannot email a legitimate quote). So every ordinary shape below is MEASURED in §N3/§N11; until it is, the instruction on any unexpected refusal is
STOP and record it, never a remedy.**

| shape — its ordinary form, as a rep really produces it | expected email (PDF + workbook) | the code clause that yields it | predicted-by |
|---|---|---|---|
| simple (never-unlocked) session, any currency | = main's simple email except `v2.36`→`v2.38`; posts `custom: null`; never refused | stripped page: no `cpExport`; render not advanced → no `cpRestore` | drafter |
| advanced, "Standard pricing only", no custom price ever set | = main's except the version; posts `custom: {pdmUSD: null}`; never refused | `cu === null` and no custom mode wanted | drafter |
| advanced, a custom price set (in bound), mode left on "Standard pricing only" | standard; = the print; NOT refused | `cpRestore(cu)` passes; mode default | drafter |
| advanced, "Custom pricing only", −10 % (gate 20's state) | custom section, A$27.90 / A$45,167 (AUD), = the print, = round 1 but for the version | `cpRestore` passes; `buildPrintDoc("custom")` | builder (READY) + gate 20 |
| advanced, "Standard + custom pricing", −10 % | standard then custom, 3 pages; = the print | the same, "both" | builder + gate 20 |
| a legitimate DEEP discount (−50 %, −90 %) or a legitimate MARK-UP (+50 %, +200 %, +899 %) | accepted; = the print | inside (0, 10×] | drafter |
| a price EXACTLY at the stated maximum (A$310.00 on the full bundle, AUD; US$200.00; CA$284.00; or Apply +900 %) | ACCEPTED (the sentence says "no more than 10 times"); = the print | `usd <= max` — float-exact? (drafter arithmetic: `cpMonth` and +900 % land exactly; the displayed 4-dp `cpDay` figure for A$310.00 is just ABOVE max) | drafter |
| a custom price set, then the app selection REDUCED (bundle → Manager only), mode "Standard pricing only" | standard; = the print; **NOT refused** | the renderer re-checks a stale price in every mode → **predicted REFUSED (WRONG (b))** | drafter |
| custom price set → Reset form | standard; = the print | `cpClear` | drafter |
| custom price set → Advanced off | standard; = the print; stale `pdmUSD` posted (O4); NOT refused unless (b) applies | `applyAdvanced(false)`; `cpExport` survives | gate 20 |
| reopen a previous quote (C-05), same page or fresh | standard (price and mode cleared, THE REOPEN SENTENCE when one was cleared); = the print | `clearCustom()` before `apply(j.state)` | builder (READY) |

## N1. THE DIFF, REVIEWED AGAINST THE READY'S CLAIMS (READ ONLY)
**FAIL condition, stated BEFORE the read:** any line of the round-2 delta not explained by the READY or the commit messages; any change in `strip.js`
outside `HOSTED_EXTRAS`; any change to the collector's field set, field names, `NOT_QUOTE` set or request other than round 1's `custom` key; the
round-1 hunks (`7b952f6` vs `437ab4b`) changed by round 2 other than the lines round 2 names; a server-module change other than the 422 branch; a
dependency line in `package.json`.
1. `git diff 437ab4b 3a3399e` whole; `git diff 7b952f6 3a3399e`; and per round-2 commit (`a7e1835^..a7e1835`, `1f7db41^..1f7db41`, `3a3399e^..3a3399e`),
   quoted into `evidence/`; every round-2 hunk mapped to a claim (table: hunk, claim, holds yes/no, how). Confirm `1f7db41` touches only
   `test/email-matches-print.mjs` and `3a3399e` only `index.html` (+2, CSS).
2. **One rule, three places:** show `cpCheck` is the ONLY bound in the page (the fields, Apply %, `cpRestore`); show `pdf.js` reaches it only through
   `window.cpRestore`; show the route trusts `report.refused` and nothing else. Quote each call site.
3. **What the bound is checked against:** quote `cpCheck`'s denominator and show (READ) which inputs move `stdPerDevMonth` (apps/bundle; not devices,
   term or currency in USD terms). This is WRONG (b)'s premise — the gate MEASURES it in §N11.
4. **The route (now changed, `e40c20e`; WRONG (j)):** quote `/api/quote/email` whole: the reservation, `renderQuotePdf(state, { advanced:
   !!req.session.advanced, qnum })`, the 422 branch, the `report.qnum` check, the send; `storableQuoteState` and its "Deliberately NOT stored" comment;
   `GET /api/quote/:qnum`'s `status !== "sent"` → not found; the retention purge's cutoffs (`lib/store.js` `purgeQuotes`).
5. Read the PR files API (`gh api repos/datasecau/vision_hpas-quickquote/pulls/10/files`) and show it equals `git diff --numstat 437ab4b 3a3399e` (8 rows,
   blobs).
6. The `package.json` change: `git diff -U0 437ab4b 3a3399e` and `7b952f6 3a3399e` show ONLY the `test:print` line; dependency maps (`dependencies`,
   `devDependencies`, `overrides`, `engines`), `name` and `version` identical by JSON parse at all three shas.
7. **What strip.js generates:** fresh base, R1 and head trees, `node strip.js`; sha256 + bytes of `public/index.html`, `private/advanced.js`,
   `private/svc.js`; `diff` head vs R1 and map every differing line to a round-2 hunk (expected: `cpCheck`/`cpRefuse`/`renderCustom(skipId)`/the
   `change` listener/`cpRestore` and the `#cpRefused` markup in `advanced.js` only; `clearCustom` and the reopen sentence in `public/index.html`'s
   `HOSTED_EXTRAS`; `"2.38"` and `customPriceMaxRatio` in both outputs where CONFIG lands). Confirm `cpCheck`, `cpRefuse`, `cpRestore` and
   `id="cpRefused"` are NOT in the stripped `public/index.html`, and `strip.js`'s leak list still passes (rc 0).

## N2. THE RED-PROOFS AND THE MUTANTS (MEASURED; never trust the mail; WRONG (c))
**FAIL condition:** a new test cell passing on R1 code where the READY says it is red (other than the control); an R1 failure for a reason that is not
the absence of the round-2 fix (setup error, drawer timeout, sign-in, Chrome launch) reported as the red; the control failing on R1; any cell failing at
the head on a clean tree.
1. **R1 and base trees (each fresh, `git archive`, `npm ci --offline --ignore-scripts`, the lockfile proven entry by entry by `lockcmp.py` AND
   `lockwalk.py`):**
   - **R-D: `7b952f6` + the head's `test/custom-price-bounds.mjs`** (blob `76368d2`, landed by `git hash-object`; `node --check` rc 0 — a test that does
     not parse is VOID). `node strip.js && node --test test/custom-price-bounds.mjs` from `stage3/` under `qa-run.py` with `PUPPETEER_EXECUTABLE_PATH`
     = YOUR egress wrapper. Quote every `not ok` with its FIRST failing assertion, and classify each: **DEFECT-REASON** (∞ shown / 200 where 422 /
     a mail captured / 27.37→2.02 / B issued custom) or **NEW-SURFACE-ABSENT** (`#cpRefused` not found, the refusal regex unmatched because no
     sentence exists). READY: 14/15 red, the control passes.
   - **R-E: `437ab4b` + the same file** (the live code): the F2 cells must fail on the clobber (pre-existing), the F1 page cell on whatever base does
     (the guard / ∞ on paper); quote and classify.
   - **R-F: `7b952f6` + the head's `test/email-matches-print.mjs`** (blob `bdb602b`): **predicted 12/12 PASS** (round 1 already priced from the exact
     number; F7 is test strength). The red for F7 is G21-M2 below, not R-F. A fleet cell FAILING at R1 is a finding about round 1 — report it.
2. **Head tree:** a fresh `git archive 3a3399e`, same install and proof; `custom-price-bounds.mjs`, `email-matches-print.mjs` and
   `email-print-mode.mjs` alone, 3 runs each; each run's wall time with the load.
3. **Mutants — each on a FRESH head tree, tamper asserted landed, `node --check` rc 0 on the changed file, `node strip.js` rc 0, and the mutated text
   shown present in the generated file it reaches (`public/index.html`, `private/advanced.js`, the tree's `lib/pdf.js` or its server module).** Run ALL
   THREE new/changed test files on each; say which cells see it, or NONE (a mutant no cell sees is a FINDING against the tests' strength, not a FAIL):
   - **Round 1's mutants, re-run at the head (renamed G21-R1..R8 = G20-M1..M8):** collector posts `custom: null`; restore ROUNDED as `cpMonth` carries
     it (**G21-R2 = G20-M2: the READY claims the 3 fleet cells now fail; gate 20 measured NONE**); `printMode` forced `"default"`; `emailCopy: false`
     (also through the real server path: emailed "both" PDF with/without — G20-F5); renderer reads `svc.js`; `buildPrintRows` drops the custom block;
     the re-check after `cpRestore` removed; the v2.36 guard re-inserted.
   - **G21-M1 page-only bound off:** in `index.html` `cpSyncFrom`, skip `cpCheck` (fields accept anything; renderer unchanged). Expected: the page
     paste cell sees it.
   - **G21-M2 renderer-only bound off:** in the GENERATED `private/advanced.js` only (after `node strip.js`; the page's `index.html` and therefore
     the fields keep the bound), make `window.cpRestore` skip its `cpCheck` call, and run `node --test` WITHOUT re-running `node strip.js` (it
     would regenerate the file; assert the mutation is still present after the run). Expected: the crafted-post cells see it; the page cells do not.
     (Also try the `lib/pdf.js`-side form — drop `if (why) return { refused: … }` — and say whether the result differs.)
   - **G21-M3 route-only:** the server module's `report.refused` branch removed. Say what then happens (`pdf: null` reaches `mail.send`? a 500?) and
     which cells see it.
   - **G21-M4 the ratio loosened:** `customPriceMaxRatio: 10` → `1000`. **Predicted: NO committed cell sees it (WRONG (d)).**
   - **G21-M5 zero allowed:** `usd > 0` → `usd >= 0`. Expected: the `0` crafted cell and −100 % cell see it.
   - **G21-M6 type coercion:** `typeof usd === "number" &&` removed. Say whether `"27.9"` is then accepted and which cell sees it.
   - **G21-M7 F2 reverted:** `renderCustom(skipId)` → `renderCustom()` in `cpSyncFrom`. Expected: the 4 key-by-key cells.
   - **G21-M8 F6 reverted:** `clearCustom()` call removed from the reopen handler. Expected: the reopen cell.
   - **G21-M9 the no-price refusal removed** (`else if (wantsCustom) …`). Expected: the "custom print mode with NO price" cell.
   - **G21-M10 the workbook order (G20-F7's `at` fix):** a PRODUCT mutant — in "Standard + custom", make `buildPrintRows` emit the custom block
     BEFORE the standard block (the printed order stays standard → custom). Run the head's `email-matches-print.mjs` (advancing `at`) AND, in a copy,
     the R1 oracle (non-advancing `at`, blob `3ac0e3c`'s loop) on that tree: the head's both-mode cells should fail, the R1 oracle should not. Say
     what each did.

## N3. THE REAL-BROWSER DRIVE THROUGH THE REAL SERVER PATH (TIER 1; MEASURED; ONE browser at a time)
**FAIL condition:** at the head, in ANY advanced cell, the emailed PDF or workbook disagreeing with the print of the same state (per D5, §N4); a press
that does not send exactly once where a send is expected (one POST, one captured mail, both attachments); a mail captured, or a PDF rendered, for a
refused price; W1 or W2, or `svc-warn` on `#emailPdfNote`, anywhere on the page at the head; a simple session or an advanced standard email differing
from base's beyond the version tokens (§N5); **a refusal (422) of an email in "Standard pricing only", or of any in-bound custom price, for a state a rep
reaches through the page's own controls (WRONG (b), §2a)**; a render that throws, 500s or prints `NaN`/`undefined`/`Infinity`/`∞` for a shape a rep can
produce through the page's own controls (Tuesday's G20-F1 ruling: a PASTE is the page's own control); a page or console error at the head that base
does not also produce for the same steps.
1. **Instrument (PRIMARY — the real server path):** YOUR harness `require`s the tree's own hosted server module's `createApp()` export (NEVER its
   entry point, NEVER with a real secret): the repo's in-memory store pattern (lift `memStore()` from the tree's own `server.test.mjs`, and SAY whether
   its `updateQuote` matches the bounds test's), a CAPTURING stub mail (gate 20's `qa-harness-g20-drive.cjs`; copy and re-point it; teach it the 422
   path), a throwaway `sessionSecret` of 48 random chars and a throwaway `unlockSecret` (fresh random; never the HPAM word), `salesCopy` =
   `sales-copy@qa.invalid` (an option, never an env var), the tree's OWN `renderQuotePdf` from `lib/pdf.js` with `PUPPETEER_EXECUTABLE_PATH` = your
   egress wrapper, `clock` FROZEN (prove it froze), `trustForwardedFor: false`, on 127.0.0.1 and a kernel-chosen port, under `qa-run.py` (`env -i`
   allowlist). ONE Google Chrome (your egress wrapper) driven by the tree's puppeteer-core: `/login`, the OTP the stub captured (the `Secure`
   cookie: gate 20 measured Chromium kept it on `http://127.0.0.1`; re-measure), Settings → Advanced → the throwaway word → Unlock (the page's own
   controls), close the drawer, fill as a rep (40 devices, 3 years, the full bundle, customer `Parity & <Probe> "QA" 'g21'`), the currency, a custom
   price the rep's way ("% from standard" `-10`, Apply), the print mode by its LABEL; then **(i) the page's own Generate/Print control** with
   `window.print` neutralised and the page captured as a PDF in PRINT media, A4, and **(ii) the page's own Email button, pressed ONCE**. Per cell
   record: the POSTed body (verbatim, incl. `custom`), POSTs seen by the server, the HTTP status, mails captured (count, to, bcc, subject, attachment
   names and sizes), the server's JSON answer (qnum, `unknownFields`, `clearedChecks`, or `error`), the store row's `status`, `#emailPdfNote` text and
   classes, `#btnEmailPdf` text and `disabled`, `#cpRefused` text and `active`, the load.
   **SECONDARY (say which rows used it):** the builder's interception method ("stubbed server") — allowed only for phone widths if the primary is too
   slow; never for the required grid, never for a refusal row.
2. **THE REQUIRED GRID (head AND base, as gate 20):** advanced × {"Standard pricing only", "Custom pricing only", "Standard + custom pricing"} × {AUD,
   USD, CAD} = 9 cells per side, plus simple × {AUD, USD, CAD} = 3 per side, plus advanced "Standard pricing only" with no price ever set × 3. **At base
   (`437ab4b`, live v2.36) custom/both are the guard: press 1 shows W1 and sends nothing; press 2 sends STANDARD** — the base column must again show
   the emailed figure ≠ the printed custom figure before "head email = print" is credited to fix (2). **Plus the R1 column (`7b952f6`) for the same 15
   cells** — it feeds §N5.4.
3. **Probes (head; MEASURED; findings unless they hit the FAIL condition above) — gate 20's P1-P14, re-run, plus P3' and P15:**
   - **P1** double-press: two real clicks 100 ms and 300 ms apart in "Custom pricing only": POSTs, mails, the note; a press after "Sent"; Enter on the
     focused button. **And the same two clicks 100 ms apart on a REFUSED state** (§N11 B-STATE): POSTs, 422s, numbers consumed, the note.
   - **P2** custom price set, custom mode → Reset form → Generate → Email.
   - **P3** custom price set, custom mode → Settings → Advanced off → Generate → Email: record the posted (stale) `pdmUSD` and the render's `printMode`.
   - **P3' (NEW, WRONG (b)):** P3, then untick apps down to Manager only (so the stale price exceeds 10× the new standard) → Generate → Email. Expected
     by §2a: standard, = the print, NOT refused. **A 422 here is a FAIL.**
   - **P4** custom mode → clear the custom /month figure → Generate → Email.
   - **P5** custom mode → the custom ticket's "Reset to default" → Generate → Email (heading, figures; `#cpRefused` cleared?).
   - **P6 C-05 reopen (round 2 changed it):** (a) email a custom quote A; reopen A in the SAME page: price and mode CLEARED, THE REOPEN SENTENCE shown,
     Generate, Email: standard, email = print, new number; (b) reopen A in a FRESH advanced session: standard, NO reopen sentence (nothing to clear);
     (c) with A's custom price live, reopen B (other device count): B standard, NOT at A's price (G20-F6); (d) reopen a REFUSED number (from §N11):
     expect not found — quote the answer.
   - **P7** custom price set in AUD → CAD → USD → Generate → Email (the bound is currency-invariant in USD: say whether any currency change alone
     ever triggers a refusal).
   - **P8 rounding and entry routes:** each field (`cpDay`, `cpMonth`, `cpYear`, `cpTerm`, `cpPct`) **typed key by key AND pasted** (gate 20 could only
     paste: F2), awkward values (4-dp per-day, a term total ending .99), and the STRESS state (2,500 devices, 5 yr, −7.77 %, AUD and CAD): every figure
     email vs print to the cent; the stress totals beside gate 20's (A$4,397,195 / CA$4,028,498) — same expected. **P8p:** paste `1e308` into
     /device/month (Tuesday's named regression cell): refused, the sentence, custom off, nothing says ∞ anywhere (screen, print, email, workbook), the
     email is the printed STANDARD quote.
   - **P9** a canned "live" FX rate answered inside the drive Chrome: email vs print; then the race (G20-F8, ticketed): re-measure and REPORT only.
     **Plus:** a price set at exactly 10× at the SEED rate, then the live rate lands — is it still accepted on screen and in the email?
   - **P10 crafted bodies** (a `fetch` from the signed-in page to YOUR loopback server only): a simple session posting `custom: {pdmUSD: 1}` +
     `pmCustom: true`; an advanced session posting `pdmUSD` = −1, `"27.9"`, `0`, `1e308`, `{}`, `Infinity` as JSON is impossible (say so), `1e-9`,
     `200` (= 10× USD bundle), `200.01`, `null` with `pmBoth`, and a valid price with `pmDefault` only. Per body: status, error text, mails, store row,
     `unknownFields`, renderer page errors, renderer pages left open (count before/after).
   - **P11 mixed versions (WRONG (h)):** (a) the BASE page and base module served to the drive Chrome by interception, posting to the HEAD server:
     W1, press 2 → **predicted 422 THE NO-PRICE SENTENCE** (was standard at R1); (b) the HEAD page and module posting to the BASE server: one press, no
     warning, what is emailed vs printed (G20-F3); (c) the R1 page posting to the HEAD server (a v2.37 tab, if v2.37 had ever shipped — it did not;
     NOTE only).
   - **P12 the lone revert (G20-F4):** in YOUR fresh head tree only, reverse `a8d769b`'s `stage3/strip.js` hunk (`git show a8d769b -- stage3/strip.js`
     piped to `patch -R` in YOUR tree; assert landed — round 2 also edited `strip.js`; if the reverse patch no longer applies cleanly, say so and
     record the reject); custom mode: press 1 (W1?), press 2: what is emailed.
   - **P13 no stale words:** W1/W2 absent from the head's generated files and the live DOM after every cell and probe; `#emailPdfNote` never carries
     `svc-warn`; `#cpRefused` carries `svc-warn active` ONLY while a refusal is shown; the button always reads `Email me this quote (PDF & XLS)`.
     Control that can fail: the base page after a custom press 1 must FIND W1.
   - **P14 themes and widths:** print light vs dark; 1280 / 375 / 320 px, light and dark, after a custom "Sent" AND with a refusal showing (the
     READY's screenshots claim): `scrollWidth <= innerWidth`, the refusal sentence wraps inside the ticket, the button label fits, no W1.
   - **P15 (NEW) the refused send, end to end:** from a state the page refuses at send time (§N11 B-STATE, custom mode): one press → the HTTP status,
     the response body, `#emailPdfNote` (expected "Send failed: A custom price must…The quote was not sent."), the button re-enabled, 0 mails, the
     store row `refused`, the quote number consumed; a second press → a second number consumed (count them); the renderer's page closed.

## N4. WHAT THE RECIPIENT GETS vs WHAT THE REP PRINTED (TIER 1; MEASURED; method per N4-METHOD, D5)
**FAIL condition (FULL-TEXT):** for any head advanced cell or probe state a rep can reach through the page's own controls that SENDS, the emailed PDF's
`pdftotext -layout` text differing from the printed PDF's after normalising ONLY the quote-number token (state the regex, count the substitutions); the
money multiset differing; the page count differing; any workbook money figure absent from the printed quote or any printed section missing its block;
THE NOTE's text, a margin or a "% below/above the standard rate" figure in the emailed PDF or the workbook; `∞`, `Infinity`, `NaN` or `undefined` in
any emailed PDF or workbook. **(FIGURES):** the money multiset in order differing; other text differences are reported. Either way, every row reports
text, money, pages, fonts and pixels. **A refused send has no emailed PDF: its row reports "REFUSED" with the 422 body, and the printed PDF of that
state is still captured and scanned for ∞/NaN.**
1. **Method:** as gate 20 (`g20-compare.py`, copied): `pdftotext -layout` full-text diff; the MONEY-FIGURE MULTISET (state the regex); `pdftoppm -r 100`
   pixel diff per page in plain python on PPM (no ImageMagick, PIL or numpy) with the bbox of every differing region; `pdfinfo` pages + A4; `pdffonts`
   set (subset tag stripped). Workbook: unzip; every sheet part; every money cell and its number format; the title row(s); the qnum; a scan for
   `1e+308`, blank totals, `NaN`.
2. **The pairs:** every §N3.2 head cell; every §N3.3 probe state that sends; every §N11 accepted edge; base custom/both press-2 email vs base custom print
   (the defect, reproduced: must differ).
3. **Controls that can fail, BEFORE any zero is believed:** a planted one-word, one-digit and one-pixel change each reported; the base defect pair
   reports a difference; head AUD vs head CAD differ; **a planted `A$∞` token in a copy of a clean PDF's text is found by your ∞ scan.**
4. **THE NOTE and THE VALUE NOTE, per mode (REPORT only; not graded):** rows = default / custom / both, columns = on screen / printed PDF / emailed PDF /
   emailed workbook: present or absent, each, with the evidence (gate 20's table, re-measured).
5. **What the recipient sees beyond the attachments:** the captured mail's `to`, `bcc`, `subject` and `text` (no price; say so), ONE send carries both
   attachments to both recipients; **a refused send reaches nobody** (0 captured, no bcc).

## N5. SIMPLE SESSIONS AND STANDARD EMAILS UNCHANGED vs MAIN — AND THE GRID UNCHANGED vs ROUND 1 (TIER 1; MEASURED; WRONG (l), (m))
**FAIL condition:** a simple-session email (AUD/USD/CAD) or an advanced "Standard pricing only" email at the head differing from base's for the same
inputs in anything other than the version tokens `v2.36`→`v2.38` and (if not frozen) the quote number; workbook parts differing other than
`docProps/core.xml` and the parts that carry the version (name each); the POSTed body differing other than round 1's `custom` key; **any §N3.2 head
cell's emailed PDF differing from the R1 cell's (same inputs) other than `v2.37`→`v2.38`**.
1. Base vs head, same inputs, frozen clocks: text diff after normalising exactly the version tokens (count them: expected 2 per PDF) — 0; money
   multiset equal; pixels only inside the version-string line boxes (bbox); pages, fonts equal. (Gate 20's disclosed reading — the one re-flowed
   `Issued …` line — re-measure and say whether it still holds with `v2.38`.)
2. The posted body, head vs base: identical but for `custom: null` (simple) or `custom: {pdmUSD: null}` (advanced, no price).
3. The OFFLINE tool (`index.html` opened as a FILE, fresh base and head; advanced via the page's own stored setting as gate 20 did — never the
   word): Generate in each mode × AUD/USD/CAD: printed text base vs head after version and qnum normalisation: 0 differences expected for in-bound
   prices. **And offline P8p:** paste `1e308` offline: refused (round 2 fixes the pre-existing ∞ on the offline paper too): report.
4. **Head vs R1 (`7b952f6`), the 15 §N3.2 cells:** emailed PDF and workbook text after normalising `v2.37`→`v2.38` (and qnum): 0 lines expected
   (the READY's claim; WRONG (m)).

## N6. THE REPO'S CI SUITES, AS CI RUNS THEM, AT `3a3399e` (and `437ab4b`, and `7b952f6`) — as SETS, NOT COUNTS (TIER 1)
**FAIL condition:** any suite red at `3a3399e` on a clean tree; a test NAME passing at `7b952f6` that does not pass at the head; `test:print`'s names
added at the head over R1 other than exactly the 15 of `custom-price-bounds.mjs` and the 3 fleet cells; a name passing at `437ab4b` that does not pass
at the head other than gate 20's 4 lost guard names; `npm ls --all` rc ≠ 0 at the head; any installed package not byte-equal to the lockfile's integrity.
1. **Trees:** fresh `git archive` extractions of `437ab4b`, `7b952f6` and `3a3399e` under `projects/vision/work-g21/` (separate from §N2's); `npm ci
   --offline --ignore-scripts` (a cache miss FAILS, then NOT RUN with the tarball named); lockfile proven entry by entry (`lockcmp.py` AND
   `lockwalk.py`); `npm ls --all` rc and stderr.
2. **The suites by PATH and command (tests.yml at the head, READ):** root `node --test quote-engine.test.mjs` (READY 69); in `stage3/`: `npm test`
   (132), `npm run test:print` (200 head / 182 R1 / 175 base expected), `npm run test:xlsx` (6). Each ×1 at base and R1 and ×2 at the head, same
   session, as SETS by test NAME (`tapsets.py`, `g17-dupnames.py`): lost, added, removed, duplicates, head vs R1 AND head vs base. **Host Node is
   v26.8.1, not CI's 22: say so on every row.** Every Chrome under YOUR egress wrapper. `npm run test:azurite` is NOT RUN (no docker) — relay CI's
   `store-azurite` on `3a3399e` as READ ONLY.
3. Never `npm install`, never `npm audit fix`. The lockfile is an unchanged blob: no `npm audit` is required (say so).

## N7. THE OFFLINE `index.html` AND THE GENERATED FILES (TIER 1 by the customer's printed quote; READ + MEASURED)
**FAIL condition:** a change in the generated `public/index.html`, `private/advanced.js` or `private/svc.js` not explained by §N1's hunks; `cpExport`,
`cpRestore`, `cpCheck` or `id="cpRefused"` reachable in the stripped (simple) page; the guard's text in any generated file.
1. §N1.7's diffs, each line mapped.
2. The OFFLINE advanced page: `window.cpRestore(1e308)` returns the sentence and changes nothing; `cpRestore(25)` restores (gate 20 measured 27.90 →
   38.75 at R1); nothing can be posted offline (say so).
3. §N5.3's offline print comparison is the measurement.

## N8. NOTHING PUSHED, MERGED OR PUBLISHED; LIVE SITE UNCHANGED (commission; READ ONLY)
**FAIL condition:** any `git push`, merge, PR comment/review/label/approval, workflow re-run, alert dismissal, `docker` command of ANY kind, `az`
command, or deploy in your command log; any write in the QuickQuote repo or in `Vision_Sales_Portal/`; any HTTP request to the live QuickQuote or the
live portal; the live webapp's `linuxFxVersion` at verdict (Tuesday's re-read) differing from AZ-PRE-READ without an explanation that is not you.
1. **Your own discipline, MEASURED:** your shell history grepped for `push`, `merge`, `docker`, `az `, `gh pr`, `-X`, `azurewebsites.net`,
   `hpas-quickquote` as a URL host (quote the zeros beside a positive control — the same grep over a scratch file that contains each reads 1); `stat`
   the repo's `.git/index` mtime at start and end and say only whether YOU could have touched it.
2. **The Azure side (AZ-READ-LEG = TUESDAY-READS):** RELAY the `AZ-PRE-READ` line appended to your prompt; say the post-read is Tuesday's at verdict.
3. **What a publish of `3a3399e` would ship (READ ONLY):** from the AZ-PRE-READ tag's trailing sha (expected `…-437ab4b`), `git log --oneline
   --first-parent <live>..3a3399e` and `git diff --stat <live> 3a3399e`; name every file (expected exactly the 8 of the delta, **the server module
   included** (WRONG (j)); no lockfile or Dockerfile change).
4. **Rollback (READ ONLY, for the publish card):** the rollback tag (v0.6.4-tool2.36-437ab4b); what P11(b) measured (G20-F3); what P11(a) measured
   about v2.36 tabs after a v2.38 publish (WRONG (h)); what P12 measured (G20-F4).
5. **Deploy-on-merge (READ ONLY):** `.github` at the head holds only `tests.yml`; if GH-API-LEG allows: repo hooks, environments, deployments.

## N9. CI AND CODEQL ON PR #10 (READ ONLY; never caused)
**FAIL condition:** a tests.yml run on `3a3399e` not `success` on all five jobs; a CodeQL check run on `3a3399e` failing; any alert dismissed.
1. GH-API-LEG = READ-ONLY-VISION-TOKEN: `actions/runs/38962577169` (push) and `/38962582879` (pull_request) — READ-BY-DRAFTER `completed success`:
   head_sha, conclusion, and their `/jobs` (five names, each `success`); the print-fit job LOGS via `gh api …/actions/jobs/<id>/logs` (a GET; the
   print-fit check-run ids on `3a3399e` at drafting were 117181082961 and 117181060865): the `custom-price-bounds` and fleet-scale lines and
   `# tests 200`; if the shim or GitHub refuses, NOT RUN; `commits/3a3399e…/check-runs` (13 at drafting, all success); `code-scanning/alerts?state=open`
   count on main and on `refs/pull/10/head` (0 / 0 at drafting); the dynamic CodeQL run 38962578337. Otherwise NOT RUN.
2. **What CodeQL can say (WRONG (k)):** the PR-side zeros are blind. Name the post-merge reads: main's code-scanning still 0 open, tests.yml green on
   the merge commit. **Never dismiss an alert.**

## N10. ROUND-1 FINDINGS, RE-TESTED — EACH A CHECK THAT CAN FAIL (TIER 1; MEASURED)
**For each, state the FAIL condition before running it; show it RED at R1 `7b952f6` (or at base `437ab4b` where named) in YOUR harness, then GREEN at
`3a3399e`. A check that is green on both sides proves nothing: it is VOID for closure. Close a finding only on a red→green pair from YOUR runs, not on
the builder's cells (those are §N2's). Output a closure table: finding, instance, R1 result (with the figure), head result, CLOSED / OPEN / NEW.**
- **R1-F1 (G20-F1, the NO GO):** FAIL if, at the head, any rep-reachable state prints or emails `∞`/`Infinity`/`NaN`, or the route emails a document
  for a `pdmUSD` outside (0, 10×]. Instances: (i) P8p paste `1e308` /device/month → R1: "A$∞" printed and emailed (gate 20 measured); head: refused,
  custom off, the emailed doc is the printed STANDARD quote; (ii) crafted `1e308` custom and both → R1 ∞, head 422 + 0 mails + row `refused`;
  (iii) crafted `0` and Apply −100 % → R1 A$0.00 "Custom Quote", head refused; (iv) `1e304`-class absurd FINITE (gate 20: "1e304 → absurd finite";
  crafted `1e6` → A$1,550,000.00/device) → head refused; (v) **the same class at the edge: §N11 L-EDGE (A$0.00 displayed) — CLOSED only if no
  document reading A$0.00/device/month is reachable; otherwise report OPEN with the instance** (WRONG (e)); (vi) the bound in the email path when the
  form changed after entry: §N11 B-STATE (WRONG (b)).
  Tuesday's fix-shape, clause by clause, each YES/NO with evidence: "applies on the page field" · "and in lib/pdf.js before cpRestore" · "a non-finite
  or out-of-bound pdmUSD is refused with a message" · "never rendered".
- **R1-F2 (G20-F2, key-by-key):** FAIL if at the head typing `27.37` (cpMonth), `0.9137` (cpDay), `333.33` (cpYear), `999.99` (cpTerm) key by key leaves
  any field other than what was typed, or `cpExport()` ≠ typed/rate (to 1e-9), or the email ≠ the print. Red at R1 AND at base (gate 20: 2.02 /
  0.0002 / 3.00 / 9.04). **R1-F2' (WRONG (g)):** in "Custom pricing only" with A$27.90 set, edit it key by key to `25.5` via backspace ×5 then digits,
  and via typing `0.5` → report the final mode, price, print, email, and every transient `#cpRefused` text (sample after each key). Not a FAIL if email
  = print; a finding if the mode silently fell back to standard.
- **R1-F3 (G20-F3):** P11(b) at v2.38 → expected unchanged (standard emailed silently): CONFIRM for the card; a finding, not a FAIL.
- **R1-F4 (G20-F4):** P12 at v2.38 → report.
- **R1-F5 (G20-F5):** G21-R4 (= G20-M4) through the real server path → report whether the emailed "both" PDF is still pixel-identical.
- **R1-F6 (G20-F6):** FAIL if at the head reopening B with A's custom price live issues B at A's price, or leaves `cpExport() !== null`, or leaves a
  custom mode checked, or shows the reopen sentence without having cleared (WRONG (n)). Red at R1 (gate 20: B 100 devices → A$104,780). Also the same-page
  reopen of A (P6a): report it now comes back standard (the builder's behaviour note; a product change for Kam's card).
- **R1-F7 (G20-F7):** G21-R2 (= G20-M2) on the head's `email-matches-print.mjs`: the 3 fleet cells must FAIL on it (red) and pass on the clean head
  (green); quote the failing figures beside gate 20's −A$195 / −CA$498 / −A$256. G21-M10 shows the order assertion can fail. The route bypass in
  `email-matches-print.mjs` remains (WRONG (i)): say so.
- **R1-F8 (G20-F8):** verify the backlog entry at `815aae7` (READ: `git show 815aae7 -- BACKLOG.md`); re-measure the P9 race at the head and report it
  unchanged or changed. Ticketed by Tuesday's allowance: NOT graded as a FAIL here.
- **O1-O4:** re-observe each (O4 feeds P3').

## N11. THE BOUND AT ITS EDGES (TIER 1; MEASURED; THE ratio-10 number Kam will see)
**FAIL condition:** a price INSIDE (0, 10×] refused on any surface (except the documented 4-dp `cpDay` rounding — report it); a price OUTSIDE it
accepted on any surface (page, print, email, workbook); a surface that refuses where another accepts for the SAME state (screen accepts and prints, the
email refuses — a finding unless it is a STANDARD email, which FAILs per §N3); `∞`/`NaN`/`undefined` anywhere; a refused price leaving custom pricing
ON or a custom print mode checked.
**The matrix: rows = the values; columns = SCREEN (the ticket's fields after entry, `cpState` via `cpExport()`, `#cpRefused` text, the print-mode
radios), PRINT (the page's own Generate → PDF in print media), EMAIL (one press: status, mails, the emailed PDF), WORKBOOK (the emailed xlsx), and
OFFLINE (the file:// page's ticket + print, for the page-side rows). Drive in AUD (seed 1.55) on the full bundle, 40 devices, 3 yr, "Custom pricing
only", unless the row says otherwise; repeat the four boundary rows in USD and CAD.**

| row | value and route | expected (drafter, from CONFIG; MEASURE it) |
|---|---|---|
| U-UNDER | `cpMonth` A$309.99 (USD 199.99...) | accepted; = the print; email = print |
| U-AT | `cpMonth` A$310.00; Apply `+900`; `cpYear` A$3,720.00; `cpTerm` A$11,160.00 (3 yr) | ACCEPTED (the sentence says "no more than"); report any route where float arithmetic refuses it |
| U-AT-DAY | `cpDay` 10.1918 (the ticket's own 4-dp display of A$310.00) | drafter arithmetic: just ABOVE max → REFUSED; report (a rep copying the shown figure is refused) |
| U-OVER | `cpMonth` A$310.01; Apply `+900.01`; `+1000` | refused, THE REFUSAL SENTENCE, custom off, mode standard |
| U-ABSURD | paste `1e308` (P8p), `1e304`, `999999999` | refused; nothing says ∞ |
| L-ZERO | `cpMonth` `0`; Apply `-100` | refused |
| L-EDGE | `cpMonth` `0.01`, `0.004`, `0.001`; `cpDay` `0.0001`; Apply `-99.99`, `-99.9` | ACCEPTED by `cpCheck` (> 0) — REPORT what the ticket, print, email and workbook show per device and in total (A$0.00/device/month?) — WRONG (e) |
| NEG | paste `-1`, `-0`, `-0.01`; Apply `-150` | refused, with the sentence |
| NONNUM | paste `abc`, `A$27.90`, `27.9abc`, `1e309`, `` (empty) | report the field's value read back, sentence or SILENCE, `cpState`, the mode (WRONG (f)) |
| LOCALE | paste `1,234.50`, `27,90`, `1 234,50`, `27.90 ` (trailing space); and, if your wrapper can start Chrome with `--lang=de-DE` (say so), type `27,90` there | report the value read back and what was taken; a locale comma silently becoming another price (e.g. 27,90 → 2790 or 27) is a finding |
| B-STATE | A$300.00 on the full bundle (accepted, 9.68×); then untick apps to Manager only (standard A$7.75 → 38.7×); Generate; Email — in "Custom pricing only" AND in "Standard pricing only" | WRONG (b): screen keeps A$300.00; print prints it (custom) / standard; **email predicted 422 in BOTH modes** — the Standard row is a FAIL if refused |
| CUR | A$310.00 accepted, then switch to CAD and USD | still accepted (USD-invariant); report |
| FX-LIVE | at the canned live rate (P9), the U-AT and U-OVER rows | the bound in USD holds; report the sentence's quoted standard figure |
| CRAFTED | §N3 P10's bodies at `200`, `200.01`, `1e-9` USD | 200 → sent; 200.01 → 422; 1e-9 → sent (what does it print?) |

Record for each accepted row the email = print comparison (§N4) and for each refused row the 422 body, 0 mails, store row `refused`, the number
consumed. **Report THE NUMBER for Kam in one line:** "max custom price = 10 × standard = <A$/US$/CA$ per device per month on the full bundle and on
Manager only>, min = anything above zero (<what the smallest accepted price prints as>)".

## 12. The merge and the queue
QQEP is 6 ahead and 0 behind `437ab4b`, so a GitHub merge commit's tree equals `3a3399e`'s (`ec15fb2`) while main stays at `437ab4b` — prove 0 behind
with `rev-list --count`; run `git merge-tree --write-tree` only from YOUR OWN object dir, or skip it and say so. **If PR #8 (C-19) merges first, PR #10
must be re-merged over a moved main: name the cells to re-run then** (at least: §N6's four suites, §N2.2's head runs, §N3.2's head grid with §N4,
§N11's U-AT/U-OVER/B-STATE rows on the merged tree). **Cells to re-run at merge:** tests.yml's five jobs on the merge commit. **At publish (Kam's word
under C-20; not this gate):** the built image's generated files equal to this gate's head tree's (name the sha256s); Kam's live check (an advanced
custom quote emailed to his own inbox, compared with its print; and a refused price, to see the sentence); the rollback tag kept.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)** on the host. Host product processes take
   ports from the kernel and bind `127.0.0.1`. **Never start the hosted server module's own entry point; use its `createApp()` export.**
2. **Every host product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; NODE_ENV = `test`, never
   `production`; `PUPPETEER_EXECUTABLE_PATH` = YOUR egress-block wrapper; `npm_config_update_notifier=false`; `npm_config_offline=true`;
   `npm_config_cache` = the user cache, read for `npm ci --offline` only). **NEVER set in a product process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`
   (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, `HPAM_WORD`,
   `ADVANCED_UNLOCK_SECRET`, `SESSION_SECRET`, `WEBSITE_SITE_NAME`, `GH_TOKEN`, `GITHUB_TOKEN`. Print each product process's env KEY NAMES (never values)
   and assert none is forbidden. `NTFY_SERVER=http://ntfy.invalid`; never contact ntfy.sh.
3. **EGRESS INCLUDING CHROME CHILDREN:** the page calls public FX APIs whenever the currency is not USD. Every Chrome runs under YOUR copy of the
   egress-block wrapper; P9's canned rate is served by request interception INSIDE the drive Chrome; prove the block with its positive control
   (`qa-egress-posctl.mjs`) and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at start and end
   (`qa-chrome-census.py`).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): "ours" = the ancestor chain CONTAINS your
   claude pid. **Negative controls, same run, must classify FOREIGN.** The launcher DERIVES the negative-control seats live from the cockpit panes
   (the `tuesday` pane, the `Datasec/Vision_Sales_Portal` builder pane, and any live `QA/*` / `fleet-monitor` pane) and appends them to your prompt.
   **A zero is reportable only beside a control that fired in the same window. Take it at START and at END.** **Record the 1-minute load beside
   every timing.**
5. **ONE BROWSER AT A TIME.** Never two drive Chromes of yours alive at once (the suites' own Chromes count as yours); never run a suite and a §N3
   drive concurrently. Inside a §N3 send the renderer's own headless Chrome runs while the drive Chrome is open: that pairing is mandated; release
   both in each cell's `finally`. Never `docker` anything.
6. **THE DEADLINE RULE:** every step has a written DEADLINE built into your runner (no `timeout` binary here) and a client timeout on every request;
   a step past its deadline is ABORTED and reported. Deadlines: one browser cell 120 s (§N3, §N4, §N5, §N11 each render); one §N2 arm 420 s; root
   pack 120 s; a whole `npm test` 300 s; a whole `test:xlsx` 300 s; a whole `test:print` 900 s; nothing above 900 s. One retry per cell at most,
   then NOT RUN with the load. **Every Chrome, page, child, app server and temp profile you start is released in a `finally`.** **Log a HEARTBEAT
   line (timestamp, step, pid, elapsed, load) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**

**Reap everything you start.** An orphan Chrome or listener of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, `hpasqqacr`, its Table Storage, its log workspace) and **NEVER the live**
  portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION). **No HTTP request to either, not
  even a GET. Press nothing there. No az at all — no writes, no app-setting change, no deploy, no publish, no ACR build, no ACR push.** Never the FX
  hosts (blocked by your wrapper; P9 answers them inside Chrome), never ntfy.sh. **Never Claude in Chrome** (Kam's real Chrome with his sign-ins).
  Never open anything under `Vision_Sales_Portal/4_Credentials/` (the launcher wires the gh config itself), **never read, ask for or type the HPAM
  word** (the live check is Kam's), and never read the builder's `fix2-email-matches-print-2026-10-17-evidence/` (incl. `round2-3a3399e/`) as evidence
  (you may LOOK at its PDFs and screenshots to compare with yours; say so).
- **No email to any human address.** Every send in this gate goes to the capturing stub mail; recipients are your sign-in address on a `.invalid`
  domain (`@qa-g21.invalid`, lower-case) and `sales-copy@qa.invalid`. Your own AgentMail calls go only to `tuesday-agent@agentmail.to`.
- **Network, and ONLY this:** `git ls-remote origin` (head readings); `gh api` GETs (GH-API-LEG); your AgentMail calls. Nothing else reaches the
  internet: no npm registry (`npm ci --offline`), no `npm audit`, no image pulls.

### HELD
- No merge, no deploy, **no publish**, **no registry push**, **no production**, no money, **no mail to any human**, no external comms. **No comment,
  review, label, approval or status on PR #10, PR #8 or any GitHub object; no re-run of any workflow; no alert dismissal of any kind.**
- **No `docker` at all, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npm audit fix`, no `npx` of anything not already in your
  tree. `gh` only as GH-API-LEG allows; no `az`.** The launcher points `AZURE_CONFIG_DIR` at an EMPTY directory.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g21/>`, in `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never
  touch any other `work*` directory** (`work-g20/`, `work-g19/` and `work-g18/` included). In the repo use ONLY read verbs (show, log, diff, ls-remote,
  rev-parse, ls-tree, cat-file, grep, merge-base, archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch,
  revert or for-each-ref.** P12's reverse patch is applied to YOUR extracted tree by `patch`, never by git in the repo. `merge-tree --write-tree` only
  from your OWN object dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own. **For this
  gate: every §N10 closure needs its R1 (or base) red from YOUR run; the base column must show the emailed custom figure ≠ the printed custom figure;
  the PDF comparator must report non-zero on a planted one-word, one-digit and one-pixel change, and the ∞ scan must find a planted `A$∞`; the
  stale-words scan must FIND W1 on the base page; each mutant must be shown to have LANDED before its result is read; the egress block's positive
  control fires; the floor count rises on its attached control.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the QuickQuote repo** (its working tree is the
  builder's, live) **and none inside `Vision_Sales_Portal/`**, none in gate 1-20's report folders or trees. Describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead.

## THE MODEL RULE
(Kam, live board 2026-09-30 09:07, card `nexusai-gate11-opus55-safeguard-model-switch`, option (b) — QA gates may switch to Opus 4.8 when flagged,
PER SESSION.) You start on Opus 5.5 (the launcher reads the model id from Tuesday's `0_Brain/dashboard/data/models_latest.json`, `claude-opus-5-5` at
drafting). You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE
line to `evidence/classifier-stops.txt`; reap any Chrome and app server you started; mail `tuesday-agent@agentmail.to` with the subject exactly
`[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch`;
then end your turn with the line `PARKED: flagged — awaiting the Opus 4.8 switch` and wait. Tuesday switches THIS pane's model and taps you by mail. You
never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states
which rows ran on which model, with the switch time, and quotes `classifier-stops.txt` whole.

## TUESDAY'S RULINGS AT STAMP (2026-10-17)
**R1-R8 are the commission's requirements as Tuesday wrote them to the drafter (2026-10-17 ~07:39), carried as ruling lines. Apply them; do not
re-rule them.**
- R1: ONE gate, TIER 1 (customer document: the email must equal the print) on QuickQuote PR #10 ROUND 2 @ 3a3399e over main 437ab4b; round 2 of 2 under the two-NO-GO cap: the next NO GO ships the closed instances and tickets the rest.
- R2: Keep gate 20's whole email-equals-print matrix (it found real defects): the advanced grid per print mode x AUD/USD/CAD, simple sessions, the probes, the recipient-vs-print comparison, the note table.
- R3: Re-test every G20 finding the builder claims fixed (F1 the NO GO, F2, F6, F7), each as a check that CAN FAIL, red at 7b952f6 (or base) and green at 3a3399e; carry F3-F5 and F8 (ticket 815aae7) as publish-card / ticket facts, re-measured.
- R4: Probe the bound (ratio 10 in CONFIG, the builder's choice) at its edges: just under, at, just over, a pasted 1e308, a negative, a non-numeric paste, a locale-formatted number — on screen, print/PDF, workbook and the emailed PDF.
- R5: A regression of everything gate 20 passed; the CI suites as SETS at head vs base; the CodeQL read for the head (never dismiss an alert); a PRIOR WORK check; a NOT TESTED section.
- R6: Model the gate on gate 20's kit and report (G20-F1..F8, O1-O4, S1-S5 are the reference).
- R7: HARD LIMITS as gate 20: no production access (the live QuickQuote is production, hpas-quickquote / datasec-sales-portal-rg); no HTTP to the live site; press nothing there and never read the HPAM access word (the live check is Kam's); local/emulated only; no email to any real human address; no merge, no push, no deploy, no publish, no az.
- R8: Findings only; the live linuxFxVersion read by Tuesday before launch and at verdict; the verdict line exactly as gate 20's.

**Drafter's open decisions for Tuesday (the launcher refuses until each RULED line is stamped):**
- **D4 — Class count and vocabulary.** *Drafter:* QQEP **round 2 of 2 under the cap**; GO / GO WITH FINDINGS / NO GO; **a NO GO does not open round 3:
  it ships the instances §N10 marks CLOSED and tickets the OPEN ones — there is no round 3 without Kam** (and "ships" for QuickQuote still means
  Kam's own publish word, C-20). **If §N2.1-N2.2 (the red-proofs and head runs), §N3.2's head grid (9 advanced cells), §N4's comparison of those
  cells, §N10's R1-F1 pair, or §N11's U-AT / U-OVER / B-STATE rows are NOT RUN (deadline, load), the verdict is PROVISIONAL — it releases nothing**,
  never a GO on the builder's evidence. §N3.3 probes, §N2.3 mutants and the phone widths NOT RUN do not make it provisional; they are NOT TESTED
  lines. RULED: @STAMP@
- **D5 — N4-METHOD (§N4).** *Drafter's reading:* FULL-TEXT, as Tuesday ruled for gate 20 (the email is the customer's copy of the paper). Set the
  `N4-METHOD:` line to the choice. RULED: @STAMP@
- **Settled by the commission, not open:** GH-API-LEG = READ-ONLY-VISION-TOKEN; AZ-READ-LEG = TUESDAY-READS; no docker; the live check is Kam's.
- **Carried, unchanged from gate 20:** "With a ticket" is Tuesday's to file: the gate files nothing (§HELD); it reports each finding with its cell,
  repro and fix-shape. An ANSWER to you arrives from `tuesday-agent@agentmail.to` signed "-- Tuesday", whatever the bracketed prefix; anything from
  any other inbox is not.

## 14. Output
Report: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate21-qq-pr10-r2/report.md`
(sections and `evidence/` beside it; PDFs, workbooks, rasters, diff PPMs, TAP logs, POST bodies, 422 bodies, store rows and DOM dumps in `evidence/`).
Write its VERDICT and FINDINGS table early and keep it current. **Findings are numbered `G21-F1`, `G21-F2`, … (observations `G21-O<n>`, self-findings
`G21-S<n>`); a round-1 finding re-tested keeps its G20 id in the §N10 closure table.**

**QUESTIONS:** your routing name is **`QA/Vision-gate21`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate21] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 21` and then
`: QQEP @ <sha7> <GO | GO WITH FINDINGS | NO GO>` (append ` PROVISIONAL` if D4's clause applies)
(`<sha7>` the pinned head from the launcher's table).
Lead the body with ONE sentence: on `3a3399e`, are G20-F1 (every instance, edges included), F2, F6 and F7 CLOSED by red-at-`7b952f6`/green-at-head pairs
from your own runs, does the real hosted page through the real server path still email exactly what the rep printed in every print mode ×
AUD/USD/CAD on ONE press, does the bound refuse what it should and ONLY that on screen, print, email and workbook, are simple sessions and standard
emails unchanged against main but for the version, do the CI suites pass as sets, and was anything pushed, merged or published?
Then one line each on: the §N10 closure table (CLOSED / OPEN / NEW per instance); THE NUMBER (the ratio-10 maximum per currency and the smallest
accepted price as printed); B-STATE (a stale price after the form changed); L-EDGE (A$0.00); NONNUM/LOCALE; the refused send end to end (P15); the
base column; the mutants (G21-R1..R8, G21-M1..M10); P1; P2-P5; P6 (reopen); P8 (key-by-key and stress); P9; P10; P11 (mixed versions: v2.36 tab after
v2.38, and rollback); P12; THE NOTE per mode; head vs R1 (§N5.4); the live site read (RELAYED from AZ-PRE-READ); what a publish would ship (§N8.3,
server module included); the class count (round 2 of 2: a NO GO ships the closed instances and tickets the rest). You have no inbox that wakes you, so
a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env`. The path is absolute because the QA project has no
credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout (`-m 30`). It must never enter
a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format (as gate 20's):
- **One verdict, GO / GO WITH FINDINGS / NO GO (PROVISIONAL per D4)**, naming the pinned sha and the branch; and in the mail body, its own line:
  `VERDICT: <GO | GO WITH FINDINGS | NO GO>, round 2 of 2 (<PROVISIONAL or not, and why>). <what happens next under the cap>`.
  Then §N1's hunk table, §N2's red/green table with the quoted failure messages and their DEFECT-REASON / NEW-SURFACE-ABSENT class, the mutant
  table, §N3's grid (cell × base/R1/head × POSTs/mails/status/qnum/unknown/printMode/load), §N4's comparison table and the note table, §N5, §N6 as
  sets, §N7, §N8, §N9, §N10's closure table, §N11's matrix, row by row.
- The verbatim strings: the R1 red messages, each mutant's failing cells, the P1 POST counts, the emailed and printed figures per head cell (and the
  base defect pair), the stress-state totals with and without G21-R2, every refusal sentence as the page and the route returned it, THE NUMBER, the AZ
  reading "RELAYED from AZ-PRE-READ".
- **A table with one row per §N item: MEASURED / NOT TESTED / NOT RUN / VOID, and HOW (command, tree, browser, port, load).** No row without a HOW.
- **Rule 2: what you did NOT test is first-class output.** Say the READY carried no NOT TESTED block (WRONG (a)). A NOT TESTED section covering at least
  **the published image (no docker by design)**, **a real ACS send (stub mail only)**, **the live site (Kam's check)**, **CodeQL's verdict (blind
  pre-merge, WRONG (k))**, **CI's Node 22 (host is Node 26.8.1; CI read only)**, **store-azurite (READ from CI; it does not exercise `status:
  "refused"`)**, **a real live FX provider (P9 is a canned answer)**, **currencies other than AUD/USD/CAD** unless you drove them, **Chrome locales
  other than the ones you ran**, **Windows / Safari / the account managers' real browsers and real phones and real printers**, **what a customer's mail
  client does with the attachments**, **screen readers (the `role=alert` refusal is a DOM read)**, **Claude in Chrome (not used)**, **PR #8 (not this
  gate)**, and every §N row you did not run, with the reason. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED /
  READ ONLY.**
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name, plus `refs/pull/10/head`.

PROVENANCE:
- heads: main `437ab4bc412b…` (= HEAD), `fix/qq-email-matches-print-2026-10-16` `3a3399e947bf…` = `refs/pull/10/head`, `refs/pull/10/merge` `1345ea5e…`,
  `refs/pull/8/head` `4d6ed6ef…`, `backlog/qq-extract-zip-2026-10-16` `815aae76…` | `git -C <quickquote on Laptop-DEV> ls-remote origin` | read 2026-10-17 07:39:16 AEDT
- the chain (six single parents), author/committer dates, counts 6 / 0 behind, merge-base, `7b952f6` ancestor of `3a3399e`, numstat whole / round 2 / per
  commit, blobs at base / R1 / head for the 8 changed files and the 11 unchanged ones, head tree `ec15fb2`, `a7e1835` tree `7f0ee8c`, `1f7db41` tree
  `beac1df`, commit messages whole | `log`, `rev-list --count`, `merge-base`, `diff --numstat`, `rev-parse <sha>:<path>` | read 07:39-07:4x
- the code at `3a3399e` vs `7b952f6` (the whole round-2 diff of `index.html`, `lib/pdf.js`, `package.json`, the server module, `strip.js`; `cpCheck`,
  `cpSyncFrom`, `renderCustom` incl. its `cpState === null` mode reset ~3478-3486, the global input listener and `CP_FIELDS` ~3193-3210, `priceQuote`'s
  `stdPerDevMonth` ~1971, the field types ~1630-1687; `pdf.js` `renderQuotePdf` whole; the route's reservation/422/send, `GET /api/quote/:qnum`, the
  purge cutoffs; `lib/store.js` `updateQuote`/`purgeQuotes`; strip.js STUBS, `ensureAdvancedModule`, the module wrapper's `window.cpClear = cpClear`;
  `custom-price-bounds.mjs` header, names and `memStore`; the `email-matches-print.mjs` diff) | `git show` under bash | read 07:4x-07:5x
- drafter arithmetic for the bound's edges (seed AUD 1.55, CAD 1.42; bundle USD 20; Manager USD 5) | `node -e` over the CONFIG values, NOT the page | 07:4x
- GitHub (READ-BY-DRAFTER, `gh api` GET with Vision's gh-config; its two files' mtimes unchanged, 12 Oct 18:09:30): PR #10 (open, not draft, clean, 8
  files, +657/−119, updated 20:31:49Z); PR #10 files (8 rows, blobs); check-runs on `3a3399e` (13, all completed success, CodeQL "No new alerts in code
  changed by this pull request"); runs for head_sha `3a3399e` (38962582879 tests pull_request, 38962578337 "PR #10" dynamic, 38962577169 tests push —
  all completed success); code-scanning open main 0, `refs/pull/10/head` 0 | read 2026-10-17 07:42:14 AEDT
- the round-2 READY mail (read whole; sha256 `303d9298…`, 5,416 B; "not tested" 0, "not run" 0); CLARIFICATIONS (last entry C-20); Tuesday's
  `0_Brain/daily_tuesday/2026-10-17.md` entries 06:11, 06:58, 07:17, 07:33, 07:40 | read 07:4x
- gate 20's brief, DRAFTER-REPORT and launcher (whole); gate 20's report (whole, sha256 `ab77c006…`), its `evidence/mail/verdict-body.txt` (whole),
  its `evidence/tools/` listing; the mail batch `/private/tmp/wed_newmail/batch_20261016T203647Z.txt` (the gate-20 verdict row; body `None`) | read 07:3x-07:4x
- load 7.48 7.38 13.04 (07:44); tmux panes `tuesday`, `Datasec/HPSM-POC-G2`, `Datasec/NexusAI-O`, `Datasec/MPS-V`, `Datasec/MPS-LE`, `Datasec/MPS-LD`,
  `Datasec/Vision_Sales_Portal`, `fleet-monitor`; host node v26.8.1; pdftotext/pdftoppm/pdfinfo/pdffonts/patch on PATH; `inbox_routing.conf` ends at
  `QA/Vision-gate20`; no gate-21 report folder | `uptime`, `tmux list-panes -a`, `node -v`, `command -v`, `grep`, `ls` | read 07:44
- no merge-tree, no fetch, no docker, no product process, no browser, no `az`, no npm, no mail was made by the drafter; `gh` was used for GET reads only
