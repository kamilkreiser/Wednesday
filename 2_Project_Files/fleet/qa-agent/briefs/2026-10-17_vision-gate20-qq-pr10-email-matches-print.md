# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 20: ONE TIER-1 QuickQuote gate — PR #10 (email matches print, C-20 fix 2; guard removed; v2.37) @ `7b952f6` on QuickQuote main `437ab4b` — one verdict, one report

**TIER 1 (quote output to customers: the PDF and workbook a rep emails, which a customer receives).** ROUND 1 of 2 of PR #10 (the branch was opened
2026-10-16 03:13Z but has had no gate). A NO GO sends it back for round 2; it does not go to Kam.

**Drafted for Tuesday on 2026-10-17 between 05:47 and ~06:3x AEDT by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Model: gate 19's kit (`2026-10-16_vision-gate19-qq-pr9-email-guard.md`, its DRAFTER-REPORT, `launch_qa_vision_qq_gate19.sh`) and gate 19's REPORT
(`/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-16-vision-gate19-qq-pr9-email-guard/report.md`, GO WITH FINDINGS on
`5f08fe0`; G19-F1..F4, G19-P1/P2, G19-C1), written one day earlier on the same page and the same Email button. Section shape, identity rules
(GET-only `gh` shim), the report-path convention, the verdict token, THE MODEL RULE, the floor and HELD rules are gate 19's. **This brief governs
where they differ.**

**NO DOCKER, as gate 19.** The delta (READ, and the PR files API — §Charter) is `index.html`, `stage3/lib/pdf.js`, `stage3/strip.js`,
`stage3/package.json` (one script line) and two test files. `stage3/Dockerfile`, `stage3/package-lock.json`, `.dockerignore`, the hosted server module,
`lib/xlsx.js`, `lib/mail.js` and `lib/store.js` carry the SAME blob at base and head. The image would run the same `node strip.js` over the same
`index.html` and the same server module this gate runs on the host, with the same lockfile. **So no image is built or run, and no `docker` command of
any kind is issued** (not even a read). What the published image does is a publish-time check (§NOT TESTED).

The builder's two mails under test (Tuesday saved them; the drafter copied them byte for byte, sha256 `ac43ba5ddda1c49a4607207a7e34478bed400460b0ddd8c02a1aa6f38d7dba70`):
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-qq-pr10-READY-mails.txt` (the STATUS of 18:44Z and the READY of
  18:46Z, 2026-10-16 UTC = 05:44 / 05:46 AEDT 2026-10-17, per Tuesday's 10-17 note 05:47)
**Every builder statement below comes from those mails, the commit messages or the code at each sha. Each one is a CLAIM. Every red, every mutant,
every suite set, every browser result and every comparison is RE-DERIVED by the gate. None is taken from the READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads both rows (and `refs/pull/10/head`) by `git ls-remote` immediately before launch,
refusing on any mismatch, **including any move of QuickQuote main** (this gate pins main exactly). The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-17 06:09 AEDT, Tuesday (read whole, lines 1-659)
Self-check note: no contradiction found. D4 and D5 ruled as below; AZ-PRE-READ taken by Tuesday under Vision's own AZURE_CONFIG_DIR; routing line QA/Vision-gate20 added; PR #8 is not merged (main still pinned 437ab4b).

GH-API-LEG: READ-ONLY-VISION-TOKEN
<!-- As gate 19 (gate 17's D1, ruled 2026-10-13 10:39; the commission: "copy gate 19's"). The launcher exports GH_CONFIG_DIR = Vision's .gh-config
     behind a GET-only `gh` shim first on PATH. Change it to NOT-RUN only if Tuesday withdraws the token; then every GitHub read is NOT RUN and the
     drafter's readings stay READ-BY-DRAFTER. -->

AZ-READ-LEG: TUESDAY-READS
<!-- As gate 19. The gate runs NO az. Tuesday reads the live webapp's linuxFxVersion BEFORE launch, writes it on the line below, and reads it again
     at verdict. The gate RELAYS. -->
AZ-PRE-READ: linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:v0.6.4-tool2.36-437ab4b ; read 2026-10-17 06:09:20 AEDT by Tuesday (az, Vision's own AZURE_CONFIG_DIR, tenant d500ebad / sub 0c57ab37)
<!-- One line, e.g. `linuxFxVersion DOCKER|hpasqqacr.azurecr.io/hpas-quickquote:<tag> ; read <YYYY-MM-DD HH:MM:SS AEDT> by Tuesday (az, Vision's own
     AZURE_CONFIG_DIR, tenant d500ebad / sub 0c57ab37)`. The launcher refuses until it names linuxFxVersion. Drafter's expectation (NOT a reading):
     v0.6.4-tool2.36-437ab4b, published 2026-10-16 ~15:25 AEDT (Tuesday's 10-16 note 15:25: "Tuesday re-read linuxFxVersion 15:24:56 =
     …:v0.6.4-tool2.36-437ab4b"). -->

N4-METHOD: FULL-TEXT
<!-- Decision D5 (§N4). Exactly one of:
       FULL-TEXT  the drafter's reading. The emailed PDF's text (pdftotext -layout) must EQUAL the printed PDF's text (the page's own Generate, print
                  media, A4, same state) after normalising ONLY the quote-number token; any other differing line is a FAIL. The money multiset, page
                  count, fonts and a pixel diff are reported beside it. (The drafter's pdftotext of the builder's own PDFs, 06:0x: 4, 6 and 4 differing
                  lines for custom / both / default, every one a quote number.)
       FIGURES    the builder's oracle: money figures equal, in order (minus the notes); other text differences are REPORTED, not FAILs. The
                  FULL-TEXT rows still run and are reported.
     The launcher refuses while it reads TUESDAY-DECIDES. -->

## Charter
Read `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this change and you owe the builder nothing. **Every line below that reports what the builder says is a CLAIM, never evidence.**

**One gate, ONE target, ONE verdict: GO / GO WITH FINDINGS / NO GO, at its pinned sha.**
- **QQEP** at `7b952f6` — **TIER 1 (quote output to customers).** ROUND 1 of PR #10.
  QuickQuote PR #10, branch `fix/qq-email-matches-print-2026-10-16`, "email matches print: emailed PDF + workbook follow the print mode and custom
  price; guard removed (C-20 fix 2, v2.37)". THREE commits over main `437ab4b`, a straight line:

| # | commit | parent | what it is |
|---|---|---|---|
| 1 | `0fc280b` (author date 2026-10-16 14:13:19 +1100; REBASED onto `437ab4b`, which is 15:07 — the author date predates its parent) | `437ab4b` | "email matches print: the emailed PDF and workbook follow the rep's print mode and custom price (C-20 fix 2)" — `index.html` (+55/−19: `buildPrintDoc`, `buildPrintRows`, `buildQuoteRows({customPDM})`, `window.cpExport` / `window.cpRestore`, toolVersion 2.37), `lib/pdf.js` (+36/−13), `strip.js` (+6/−1: the collector posts `custom: {pdmUSD}`), `package.json` (+1/−1), the new `test/email-matches-print.mjs` (+148) |
| 2 | `a8d769b` (2026-10-17 05:32:41 +1100) | `0fc280b` | "stage3: remove the v2.36 email guard; email now follows the print mode (C-20)" — `strip.js` (+5/−25), `test/email-matches-print.mjs` (+4/−6), `test/email-print-mode.mjs` rewritten (+23/−49) |
| 3 | `7b952f6` (2026-10-17 05:43:02 +1100) | `a8d769b` | "test: the Custom pricing note half is the on-screen preview; on paper .q-savings is hidden since v1.88" — `test/email-matches-print.mjs` (+4/−1). THE HEAD |

**THE DELTA THAT SHIPS is `git diff 437ab4b 7b952f6` (6 files, +275/−108)** — the same six files and counts as the PR files API (READ-BY-DRAFTER,
`gh api …/pulls/10/files`, 05:5x: `index.html` +55/−19 blob `51c6eb9`; `stage3/lib/pdf.js` +36/−13 `2e692d3`; `stage3/package.json` +1/−1 `725a5e2`;
`stage3/strip.js` +11/−26 `7c37287`; `stage3/test/email-matches-print.mjs` added +149 `3ac0e3c`; `stage3/test/email-print-mode.mjs` +23/−49 `9dd5311`;
PR `changed_files` 6, additions 275, deletions 108):

| file | +/− | base → head blob | what (READ at the pinned shas) |
|---|---|---|---|
| `index.html` | +55 / −19 | `dde1392` → `51c6eb9` | toolVersion `"2.36"` → `"2.37"`; `buildQuoteRows(opts)` takes `opts.customPDM` and prices it with `calc(customPDM)`, title "Custom Quote" when custom; the Generate button's section assembly lifted into `buildPrintDoc(mode, qnum, opts)` (with `opts.emailCopy` forcing `hideCustomNote`), `buildPrintRows(mode, qnum)` (one row block per printed section joined by a `blank` row); inside the ADVANCED JS region `window.cpExport = () => cpState` and `window.cpRestore = v => { cpState = v; renderCustom(); }` |
| `stage3/lib/pdf.js` | +36 / −13 | `783ebea` → `2e692d3` | an advanced render now evaluates `private/advanced.js` (was `private/svc.js`); after the field passes, if `window.cpRestore` exists and `state.custom.pdmUSD` is a finite number ≥ 0, restores it and re-checks the posted `pmCustom`/`pmBoth` with `fire()`; the document is `buildPrintDoc(printMode, qnum, { emailCopy: true })` and the workbook rows `buildPrintRows(printMode, qnum)`; the report carries `printMode` |
| `stage3/strip.js` | +11 / −26 | `0730e10` → `7c37287` | in `HOSTED_EXTRAS`: the whole v2.36 guard (W1, W2, `armedFor`, `printMode()`, `disarm()`, the `change` listener, the arming block) removed; a comment in its place; the collector's body gains `custom: typeof window.cpExport === "function" ? { pdmUSD: window.cpExport() } : null` |
| `stage3/package.json` | +1 / −1 | `1606aa3` → `725a5e2` | `test/email-matches-print.mjs` inserted into `test:print` after `test/email-print-mode.mjs`. No dependency line changes |
| `stage3/test/email-matches-print.mjs` | +149 | — → `3ac0e3c` | new: 9 cells (`default`/`custom`/`both` × AUD/USD/CAD); Chrome via the tree's puppeteer-core, every request intercepted at `http://qq.test` (unlock and module stubbed, `/api/quote/email` stubbed and recorded); the recorded body handed DIRECTLY to `renderQuotePdf(state, {advanced: true})` — **never through the server route** |
| `stage3/test/email-print-mode.mjs` | +23 / −49 | `b1d4443` → `9dd5311` | rewritten: 3 cells (custom, both: ONE press sends, no W1/W2 on the page, the post carries the mode and `custom.pdmUSD > 0`; control: standard sends on one press) |

**Same blob at base and head (READ, `rev-parse <sha>:<path>`, 05:5x):** `stage3/package-lock.json` `01c5e5e`, `stage3/Dockerfile` `8311ebe`, the hosted
server module (`stage3/` entry module) `a854ba2`, `stage3/lib/xlsx.js` `10bf4d7`, `stage3/lib/mail.js` `3aa8922`, `stage3/lib/store.js` `0609594`,
`stage3/login.html` `f362b45`, `.dockerignore` `acf7db8`, `.github/workflows/tests.yml` `ec450f5`, `quote-engine.test.mjs` `2d193b6`,
`stage3/test/print-fit.mjs` `543f4c1`, `stage3/test/email-collector.mjs` `85a27c5`, `stage3/test/server.test.mjs` `b35a2eb`, `stage3/test/lib-close.mjs`
`826b5f7`, `stage3/test/xlsx-parity.mjs` `f81a82c`, `stage3/test/strip.test.mjs` `20248d6`, `CLAUDE.md` `af402a7`. Head tree `25ddfb8`.
**Main `437ab4b`'s tree is `c71780c`, the same tree as `818a019`** (the builder's "main" evidence folder is named `main-818a019`; READ, same tree).

**Names, written out every time:**
- **QQEP** = branch `fix/qq-email-matches-print-2026-10-16` = PR #10 = "fix (2)" = "email matches print" = the delta above. **MAIN-Q** = QuickQuote
  main `437ab4b` = merge of PR #11 (`818a019`, the v2.36 version line) over `9d1c5ab` (merge of PR #9, the guard) = **what is LIVE** (v0.6.4-tool2.36-437ab4b,
  AZ-PRE-READ confirms). **C-20** = Kam's ruling, card `quickquote-email-sends-standard-not-custom-1016` = (a) "Publish the guard as soon as it passes the
  gate, full fix after".
- **W1 / W2 (RETIRED)** = the two sentences Kam approved for the guard (card `quickquote-guard-words-1016` = a; gate 19 measured them byte-equal on
  `5f08fe0`; Tuesday's 10-16 note 15:25: live page "W1/W2 byte-equal"). This PR REMOVES them. Their sha256 (for the absence checks only):
  W1 `0d5beedb47709eed6c7c6eec5d8ced3e73c58069ea09f49f4495cde1abeb25b9`, W2 `4c73c1593e64f73dc84d24c48a69896307108d387b70a9318b0d7f7dd3ec797d`.
  W1 begins `This email sends standard pricing only.`; W2 is `Send standard pricing anyway`.
- **THE NOTE** = the "Custom pricing note" (`.q-savings` box: "this quote uses account-manager pricing of … — N% below the standard rate of …").
  **THE VALUE NOTE** = the standard `.q-savings` "Value note". **PRINT CSS** = `#quoteDoc .q-savings { display: none !important; }` inside `@media print`
  (index.html ~701 at the head, from `5ef2a60`, v1.88, 2026-06-24).

Branch status: **NOT on main. PR #10 is open, not merged, not draft** (`gh api …/pulls/10`: state open, merged false, draft false, mergeable_state clean,
head `7b952f6…`, base `437ab4b…` ref main, created 2026-10-16T03:13:36Z, updated 18:45:49Z — READ-BY-DRAFTER 05:5x).

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole (C-01..C-20 at drafting). **Cite only what you open.** The entries this gate turns on:
  - **C-20 (Kam, live board 2026-10-16 13:25:51 AEDT, card `quickquote-email-sends-standard-not-custom-1016` = (a)):** "Publish the guard as soon as
    it passes the gate, full fix after". The defect: in an advanced session the emailed quote was always "Standard pricing only". Fix (2), email matches
    print, "is its own tier-1 round". **"Kam's grant covers the GUARD only. Fix (2) and PR #8 (C-19) each need Kam's own word before any publish."**
    "Do not contact anyone who received an emailed quote."
  - **C-05** (reopen a quote by its number): background for probe P6.
- **Tuesday's rulings already made — the gate checks them AS BUILT and does not re-open them:**
  - **The note (Tuesday, 2026-10-16 ~14:02 AEDT, on the builder's 03:01Z QUESTION; Tuesday's 10-16 note 14:02):** "leave it OUT of the email
    (forwardable copy; workbook rule 'as the customer receives it'), keep on print; test asserts absence in email + presence on print. To Kam on fix (2)'s
    publish card, reversible there."
  - **The guard's removal (Tuesday, 2026-10-17 05:4x, on the builder's 05:30 QUESTION; Tuesday's 10-17 note):** "RULED remove the v2.36 email guard in
    fix 2 (Kam 13:25 'guard ... full fix after'); W1/W2 retirement goes on fix 2's publish card beside the custom-note line." W1/W2 are RETIRED; their
    absence is checked, their wording is not graded.
  - **Kam's original ruling** C-20 (a) above. The publish of fix (2) needs **Kam's own word** (C-20) — not this gate's, not Tuesday's alone.
- **NEW PRE-EXISTING FACT the builder found (STATUS mail; backlog `cdcd490`, READ: "backlog: the Custom pricing note is hidden on paper since v1.88"):**
  PRINT CSS has hidden THE NOTE and THE VALUE NOTE on paper since v1.88 (`5ef2a60`). **The gate REPORTS what is on paper, on screen, in the emailed PDF
  and in the emailed workbook, in each mode (§N4.4). It does NOT grade the product choice** (whether the note belongs on paper is Kam's).
- **PRODUCTION IS LIVE for this project.** Live QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, its registry `hpasqqacr`, its Table Storage and
  its log workspace) and the live portal (`datasec-sales-portal.azurewebsites.net`, `datasec-sales-portal-rg`) are PRODUCTION. **Nothing in this gate
  touches either** (§13, HELD). The gate makes no Azure contact at all (AZ-READ-LEG = TUESDAY-READS).
- **THE LIVE CHECK IS KAM'S, NOT YOURS.** Tuesday's ANSWER to the builder's 04:04Z QUESTION (Tuesday's 10-16 note 15:07): "do NOT read HPAM_WORD; live
  check 2b moves to Kam." **You never press anything on the live site, never request any URL of it, and never read, ask for or type the HPAM access
  word.** The unlock word in your harness is a fresh random string you generate.
- **Merging and publishing are HELD. Nothing merges or publishes on your word.**
- **The BUILDER's choices, each judged by the gate (say whether each needs Kam):** (1) the custom price travels as ONE full-precision USD number
  (`custom.pdmUSD`) rather than the rounded `cp*` fields; (2) the renderer trusts any finite non-negative `pdmUSD` from an advanced session (no upper
  bound); (3) print mode and the custom price are NOT stored for C-05 reopen (the server module's own comment: "Deliberately NOT stored: … print mode";
  unchanged blob), so a reopened custom quote comes back in standard; (4) the guard's removal is a separate commit "so it reverts on its own" (WRONG (f));
  (5) THE NOTE is excluded from the emailed copy by `emailCopy`, while PRINT CSS hides it from every PDF anyway (WRONG (g)); (6) both tests stub the
  server, and `email-matches-print.mjs` calls `renderQuotePdf` directly, so the route between them is untested by the builder (WRONG (c)).

## PRIOR ROUND
PRIOR ROUND: none for PR #10 — this is its round 1. There is no round-N−1 report of PR #10 to carry.
The last QuickQuote gate WITH A REPORT is **gate 19** (QQGD, PR #9, the guard: GO WITH FINDINGS at `5f08fe0`; Tuesday's 10-16 note 15:03, "Scored 0.97").
ITS REPORT IS ON DISK AT: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-16-vision-gate19-qq-pr9-email-guard`
(`report.md`, `evidence/`, `evidence/tools/`). **Read `report.md` whole.** It is your reference for what a careful gate on this page looks like.
Its findings and what becomes of each here (each a reading for you to MEASURE, not a conclusion):
- **G19-F1 (Major, double-press 100 ms sent standard pricing after W1 had been up ~100 ms):** the guard is gone; re-measure the same two clicks 100 ms
  apart (probe P1): expected exactly ONE POST (the button is `disabled` from the first click until the send settles; READ) and the email = the print.
- **G19-F2 (stale W1/W2 after programmatic resets: Advanced off, Reset form, clearing the custom figure):** W1/W2 must now appear NOWHERE (P13); the
  same three resets are probes P2-P4, where the question becomes "does the email equal the print in that state".
- **G19-F3 (no `aria-live` on `#emailPdfNote`):** lapses for W1; the note still carries "Sent — quote …" / "Send failed: …" — record the DOM fact again
  (pre-existing, not PR #10's).
- **G19-F4 (test strength):** the new tests are graded by §N2's mutants.
- **G19-P1 (version not bumped):** fixed by PR #11 (2.36) and here (2.37) — verify on the PDF footer, the workbook and the page badge.
- **G19-P2 (placement):** lapses with W1.
- **G19-C1 (the 340 px drawer opens at −19.2 px at 320 px):** `email-print-mode.mjs` at the head STILL waits for `r.left >= 0` (READ); harmless at its
  1280 px viewport; note it if you drive 320 px.
- **The figures gate 19 measured** (AUD, 40 devices, 3 yr, full bundle, −10 % custom, seed 1.55): standard total **A$49,631** (A$31.00/device/month);
  printed "Custom pricing only" total **A$45,167** (A$27.90). The builder's READY now claims the custom email carries A$27.90 and A$45,167 — the same
  state. Reproduce it in YOUR state and quote YOUR figures.
- **Gate 18 (PR #8, @`4d6ed6e`) was drafted 2026-10-16 but has no report and no pane at drafting** (READ: no gate-18 report folder; `tmux list-panes -a`
  05:5x shows `tuesday`, `Datasec/MPS-LE`, `Datasec/MPS-LD`, `Datasec/Vision_Sales_Portal`, `fleet-monitor`). If it runs beside you, touch none of its
  `qa-g18-*` objects or `work-g18/`. **If PR #8 merges before launch, main moves and the launcher refuses (re-pin, re-brief).**
- **Instruments are REUSED BY COPY from gate 19's `evidence/tools/` (on /Volumes/Laptop-DEV — no T9 needed):** `qa-run.py`, `mktree-qq.sh`, `lockcmp.py`,
  `lockwalk.py`, `tapsets.py`, `g17-dupnames.py`, `g19-run-suites.sh`, `g19-mutate.py`, `g19-n7-compare.py`, `g19-gh.sh`, `qa-harness-g19-drive.cjs` (the
  REAL server path: the tree's `createApp()` in-process, `memStore()` lifted from the tree's own `server.test.mjs`, a capturing stub mail, the tree's
  own `renderQuotePdf`, a frozen clock), `qa-harness-g16-shots.mjs`, `qa-chrome-egressblock.sh`, `qa-chrome-census.py`, `qa-egress-posctl.mjs`,
  `qa-floorcount.py`, `qa-harness-floorctl.mjs`, `qa-netlog-scan.py`. **COPY what you use into THIS gate's own `evidence/tools/`, read it before you trust
  it, and RE-POINT every hard-coded path** (gate 19's copies hard-code `work-g19` and the gate-19 report folder; `qa-harness-g19-drive.cjs` asserts W1/W2
  as the EXPECTED warning — that logic is now inverted: W1/W2 must be ABSENT). **Never edit, run from, or write into gate 1-19's copies, evidence or
  trees** (`work-g19/` included). Record the sha1 of each copy before and after your edits. `qa-run.py`'s copy asserts a deadline ceiling: set it to this
  brief's §13.6 ceiling in YOUR copy only, and say so.
- **Self-findings from earlier gates bind you:** quote every path (the project path has a space and a `!`; the repo sits under `Quoting Tool/`); run
  every loop and every `git show <sha>:<path>` under **bash, not zsh** (zsh reads `$H:s…` as a modifier); run `node strip.js` before any lone browser
  file; assert every tamper landed before reading its result; npm's update-notifier egresses unless you disable it; record the load average beside
  every timing number; `git branch` and `git for-each-ref` are NOT read verbs here; puppeteer-core 23.11.1's `click({clickCount: 2})` is ONE press with
  `detail=2`, NOT a double-click (gate 19 E1a) — two real clicks N ms apart are what a double-press is; the Settings drawer is 340 px wide.
- **PRIOR WORK: verify every claim against git history and the Actions API (GH-API-LEG), never against this brief.** The STATUS/READY claims (red 9/9
  on main's code; red 2/3 at v2.36 strip.js; 182/182; "print text identical to main's in all 6 mode/theme cases"; "8/8, 8/8, 16/16"; backlog `cdcd490`)
  are re-derived or marked UNVERIFIED.

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head and no `@`; the head is a commit; for QQEP the base is an ancestor AND the merge-base
with MAIN; `git rev-list --count base..head` equals `commits`; the chain is exactly `437ab4b` ← `0fc280b` ← `a8d769b` ← `7b952f6` (single parents);
`git ls-remote origin refs/heads/<branch>` equals the head NOW **for BOTH rows — a moved main REFUSES (re-pin and re-brief)**; `refs/pull/10/head` equals
the QQEP head NOW; QQEP is not on main and is 0 behind it.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-Q | quickquote | main | 437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6 | - | - | IN |
| QQEP | quickquote | fix/qq-email-matches-print-2026-10-16 | 7b952f6edbcc3b271e4a650685f47b87760ed8f0 | 437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6 | 3 | IN |
<!-- PIN-HEADS:END -->

Both rows: `git -C <quickquote> ls-remote origin` read by the drafter at **2026-10-17 05:47:35 AEDT**: `refs/heads/main` = `437ab4b…` (= `HEAD`),
`refs/heads/fix/qq-email-matches-print-2026-10-16` = `7b952f6…`, `refs/pull/10/head` = `7b952f6…`, `refs/pull/10/merge` =
`d46f5f5d51d35fee4a9afee80290c3923738a79a` (GitHub's test merge, NOTE only), `refs/pull/8/head` = `4d6ed6e…` (open, gate 18's target),
`refs/heads/release/qq-v2.36-email-guard-2026-10-16` = `refs/pull/11/head` = `818a019…`. `rev-list --count 437ab4b..7b952f6` = 3; `7b952f6..437ab4b` = 0;
merge-base `437ab4b`.

Repo: quickquote = `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool` (remote `datasecau/vision_hpas-quickquote`).
**The T9 copy of this repo is STALE. Never read it.** Its rules: the repo's own `CLAUDE.md` (read it at the head with `git show`; its deploy and
publish lines are NOT for you) and `/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (its QuickQuote section). **The builder's
checkout is LIVE: never use the name `main` in the repo, always the pinned 40-hex sha; never read any working tree as evidence; build every tree from
the object store.** **If PR #8 merges while you run, main moves:** your pins stay valid (they are shas), say so in the three readings and do NOT re-base
anything — the verdict is on `7b952f6` over `437ab4b`.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; all are claims)
- **(a) The READY carries no NOT TESTED block.** Neither mail has a "NOT TESTED" line (case-insensitive count 0, READ). The only untested item either
  mail names is the STATUS line `- test:azurite was not run locally (it needs an emulator, and the code it covers is untouched). CI's store-azurite job covers it.`
  (carried verbatim here). **You build the NOT TESTED list yourself (§14), and say that the READY had none.**
- **(b) "Red on main's code: 9/9 fail (7 unknown fields)" was measured before the rebase, on a different main.** `0fc280b`'s author date
  (2026-10-16 14:13) predates its parent `437ab4b` (15:07): it was written over `e4ce536` (no guard) and rebased. On `437ab4b` the v2.36 GUARD is in the
  page: a custom/both first press only warns and posts nothing, so `email-matches-print.mjs`'s custom and both cells are expected to fail on
  `one press of the Email button posted once` (or the 10 s note wait), NOT on the unknown-fields or figures assertion; only the 3 default cells can fail
  on `unknown`. READ-ONLY-INFERRED. **§N2 runs it on `437ab4b` AND on a pre-guard tree, and quotes every cell's failing assertion.** A red that never
  reaches the figures assertion proves nothing about the figures: §N2's mutants G20-M2/M3/M7 are what show the figures assertion can fail.
- **(c) Neither builder test exercises the server route.** Both intercept `/api/quote/email` and answer a canned qnum; `email-matches-print.mjs` hands
  the recorded body straight to `renderQuotePdf(state, {advanced: true})` with `advanced` hard-coded. The route (`requireAuth`, the C-05 reservation,
  `advanced: !!req.session.advanced` from the SESSION, the real stub-mail send with BOTH attachments) is decided by the unchanged server module.
  **§N3 runs the hosted server module's own `createApp()` and reads the PDF and workbook the capturing stub mail received.**
- **(d) "Print text is identical to main's in all 6 mode/theme cases" holds only after normalisation.** The builder's README says
  "whitespace-normalised". The drafter's `pdftotext -layout` diff of the builder's own `main-818a019/default-print-light.pdf` vs
  `fix-7b952f6/default-print-light.pdf` (06:0x): the quote number (twice), `v2.36` → `v2.37` (twice: the page-1 footer and page 2), and one line's
  leading spaces. **Expected, and NOT a FAIL: exactly the quote-number tokens and the `v2.36`/`v2.37` version tokens; §N5 normalises exactly those,
  counts each, and FAILs any other difference.** A frozen page clock (or the same issued number) removes the qnum term; say which you used.
- **(e) The figures oracle in `email-matches-print.mjs` is weaker than "the email equals the print".** It compares money tokens only
  (`/(?:[A-Z]{1,2})?\$[0-9][0-9,]*(?:\.[0-9]+)?/g`, `.00` stripped), on `#quoteDoc.innerText` in SCREEN media (where THE NOTE and THE VALUE NOTE are
  visible), not on the PDF a customer opens. Wording, device counts, term, headings ("Custom Quote"), discount lines and page structure are not compared.
  §N4 compares the two PDFs themselves.
- **(f) "Kept as a separate commit so it reverts on its own" — a lone revert of `a8d769b` would put a FALSE sentence on screen.** Reverting `a8d769b`
  alone restores W1 ("This email sends standard pricing only. Your custom pricing is on the printable quote, but it will not be in the email.") while
  `0fc280b` stays, and `0fc280b` makes the email CARRY the custom price. READ-ONLY-INFERRED. **Probe P12 builds that tree in YOUR work dir (never in the
  repo) and measures what the email carries after W1's second press.** A finding for the publish card (the safe rollback is the image, not this revert);
  not a FAIL of the head.
- **(g) The note's exclusion from the email is invisible in the emailed PDF.** PRINT CSS hides every `.q-savings` box in print media, and `page.pdf()`
  renders print media, so THE NOTE is absent from every PDF — printed or emailed — whatever `emailCopy` says (READ; the builder's README agrees: "No
  'Custom pricing note' on any PDF"). `emailCopy` changes only the render page's screen-media DOM (`docText`, which the test reads). **Mutant G20-M4 shows
  it: flip `emailCopy` off and say whether the emailed PDF bytes/text change at all.** This matters for the publish card: "Kam can reverse it" would,
  as built, change nothing a customer sees unless PRINT CSS also changes.
- **(h) Rollback and mixed versions.** The READY: "Rollback for a v2.37 publish would be v0.6.4-tool2.36-437ab4b." A v2.37 page already open in a rep's
  tab during a rollback posts `custom` and no guard stands in front of it; the v2.36 renderer ignores `custom`, does not know the 7 print-mode fields
  and emails STANDARD — the C-20 defect, back, for every open tab, silently (READ-ONLY-INFERRED). The reverse (a v2.36 tab open across the v2.37
  publish) shows W1, and its second press posts no `custom` (READ). **Probe P11 measures both** (pages from one tree, server from the other). Findings for
  the publish card, never a FAIL of the head.
- **(i) `pdmUSD` has no upper bound.** The renderer accepts any finite number ≥ 0 from an advanced session (`Number.isFinite(cu) && cu >= 0`, READ);
  `1e308` passes. A rep cannot type it, but the route accepts any body. **Probe P10 measures what is rendered and emailed** (an "Infinity", "NaN", a 500 or
  a page error is a finding; severity yours).
- **(j) The session cookie is `Secure`** (gate 19 measured: Chromium kept it on `http://127.0.0.1`; no CDP fallback was needed). Re-measure; if it is
  not kept, sign in by fetch and set it by CDP, and SAY so.
- **(k) CodeQL on PR refs is a blind instrument** (gate 17 WRONG (a); gate 19 N9.2). The check runs on `7b952f6` read `CodeQL success "No new alerts in
  code changed by this pull request"`, `Analyze (javascript-typescript)` and `Analyze (actions)` success (READ-BY-DRAFTER). Say only what they can show.
- **(l) "toolVersion 2.37 is in the same commit"** (READY) — TRUE at source (`0fc280b`, index.html ~1732; READ). `stage3/package.json` `version` stays
  `0.3.2` at base and head (READ); the image tag `v0.6.4-…` is not that field. Name what the PDF footer, the workbook and the page badge print (§N5 counts the version tokens; WRONG (l)).
- **Verified TRUE at source (READ 05:47-06:2x):** both heads + `refs/pull/10/head` by `ls-remote`; the chain and single parents; 3 ahead / 0 behind;
  6 files, numstat = the PR files API; the unchanged-blob list; the `test:print` line diff (only `test/email-matches-print.mjs` inserted); W1/W2 absent
  from `strip.js` at the head and present at base; `buildPrintDoc` / `buildPrintRows` / `cpExport` / `cpRestore` / toolVersion `"2.37"` at the head;
  `lib/pdf.js` loads `private/advanced.js` and calls `buildPrintDoc(printMode, qnum, { emailCopy: true })`; the server module passes the WHOLE posted
  `state` (with `custom`) to `renderQuotePdf` and stores only its allowlist (no `custom`, no `pm*`, no `cp*`); `.q-savings { display: none !important; }`
  under `@media print`; backlog `cdcd490` exists; CI runs 38949473743 (push) and 38949480136 (pull_request) on `7b952f6`: success, 5/5 jobs each
  (stage3-server, pricing-pack, print-fit, xlsx-parity, store-azurite); check-runs on `7b952f6`: CodeQL, Analyze ×2 and 10 test jobs all success;
  main open code-scanning 0; Dependabot open #1 #4 (extract-zip, high — PR #8's business); Vision's gh-config mtimes unchanged by the drafter's GETs
  (12 Oct 18:09:30).

## THE READY — its claims and NOT TESTED (the gate rules on every claim)
Read both mails whole. **The READY carries no NOT TESTED block (WRONG (a)).** The STATUS mail's only untested line, VERBATIM (the launcher checks it):

QQEP NOT TESTED
```
- test:azurite was not run locally (it needs an emulator, and the code it covers is untouched). CI's store-azurite job covers it.
```

**The claims, in one line each (each a CLAIM, re-derived in §N):** 3 commits; the emailed PDF and workbook follow the print mode and the exact custom
price; one shared builder `buildPrintDoc`/`buildPrintRows`; the collector posts `custom.pdmUSD`; an advanced render loads `advanced.js`, restores the
price and re-applies the mode; toolVersion 2.37 in the same commit; `a8d769b` removes the guard, separately, so it "reverts on its own"; "G19-F1..F3 lapse
with it"; `7b952f6` is test wording only; email-matches-print 3 modes × AUD/USD/CAD with the real Generate and Email buttons (ONE press) and the real
`renderQuotePdf`, "Red 9/9 on main's code, green 9/9"; email-print-mode pins one press, no warning, mode + custom price in the post, "RED 2/3" at v2.36
`strip.js`, "GREEN 3/3" at `a8d769b`; local pricing 69/69, npm test 132/132, test:print 182/182, test:xlsx 6/6; CI on `7b952f6` all green incl.
store-azurite and CodeQL, 0 open code-scanning; pages default 2, custom 2, both 3, each one A4; "Print text is identical to main's in all 6 mode/theme
cases"; "Emailed figures equal printed figures, in order: 8/8, 8/8, 16/16"; custom emails A$27.90 and A$45,167 (main: A$31.00 and A$49,631); the note is
OFF the email and ON the print, on screen only, hidden on paper since v1.88; "Rollback for a v2.37 publish would be v0.6.4-tool2.36-437ab4b."

**How you treat these:** every claim you CAN test, you test. **test:azurite** stays NOT RUN here (no docker; `lib/store.js` and its test are unchanged
blobs) — relay CI's `store-azurite` as READ ONLY. **A real ACS send** stays NOT TESTED (no real mail, ever); its nearest substitute is §N3/§N4: the real
server path with a capturing stub mail. **The live site** stays NOT TESTED (Kam's check after a publish).

## 2a. LEGITIMATE SHAPES — what an ordinary rep produces, and what the email must then be
**Fix (2) is not a checker, but it changes what EVERY advanced email carries, and a regression on the ordinary shapes (a simple session; an advanced
session in "Standard pricing only") would misprice the commonest quote. Every row below is MEASURED in §N3; until it is, the instruction on any
unexpected result is STOP and record it, never a remedy.**

| shape — its ordinary form, as a rep really produces it | expected email (PDF + workbook) | the code clause that yields it | predicted-by |
|---|---|---|---|
| simple (never-unlocked) session, any currency | = main's simple email except the version tokens (2.36 → 2.37); posts `custom: null` | the stripped page has no `cpExport`; render not advanced → no `cpRestore` | drafter |
| advanced, "Standard pricing only", no custom price ever set | = main's advanced standard email except the version tokens; posts `custom: {pdmUSD: null}` | `cpExport()` returns `cpState` = null → no restore | drafter |
| advanced, a custom price set, mode left on "Standard pricing only" | standard only; = the print | `pmCustom`/`pmBoth` posted false → no re-check; `buildPrintDoc("default")` | drafter |
| advanced, "Custom pricing only" | custom section only (heading "Custom Quote"), the exact printed figures, no note; workbook one custom block | `cpRestore(pdmUSD)`, `pmCustom` re-checked, `buildPrintDoc("custom")` | builder (READY) |
| advanced, "Standard + custom pricing" | standard section, then custom section, one qnum, 3 pages; workbook two blocks | the same, `buildPrintDoc("both")` / `buildPrintRows("both")` | builder (READY) |
| custom price set → Reset form | standard; = the print in that state | `btnReset` → `cpClear()` → `cpState` null → `renderCustom` puts the mode back to default | drafter |
| custom price set → Advanced off (Settings) | standard; = the print; but the post still carries the STALE `pdmUSD` (the module stays loaded) | `applyAdvanced(false)` sets `pmDefault` without an event; `cpExport` survives | drafter |
| custom mode → the page's "Reset to default" for the custom ticket | mode stays custom; the custom section at the standard figure, headed "Custom Quote"; = the print | `btnResetCustom` sets `cpState` = standard (gate 19 E2 measured the mode stays custom) | gate 19 |
| reopen a previous custom quote (C-05) into a fresh page | standard (print mode and custom price are not stored); = the print | storable allowlist; unchanged blob | drafter |

## N1. THE DIFF, REVIEWED AGAINST THE READY'S CLAIMS (READ ONLY)
**FAIL condition, stated BEFORE the read:** any line of the delta not explained by the READY or the commit messages; any change in `strip.js` outside
`HOSTED_EXTRAS`; any change to the collector's field set, field names, `NOT_QUOTE` set or request other than the added `custom` key; the click handler
after the guard's removal not equal to `e4ce536`'s (pre-guard) handler except the `custom` line and the `LABEL` constant; `buildPrintDoc` assembling the
Generate button's document differently from base's `btnPrint` handler (other than the `emailCopy` clause and variable names); a dependency line in
`package.json`.
1. `git diff 437ab4b 7b952f6` whole, and per commit (`0fc280b^..0fc280b`, `a8d769b^..a8d769b`, `7b952f6^..7b952f6`), quoted into `evidence/`; every
   hunk mapped to a claim (table: hunk, claim, holds yes/no, how). Confirm `7b952f6` touches only `test/email-matches-print.mjs` (+4/−1).
2. **The guard is gone and nothing else of the handler moved:** extract `HOSTED_EXTRAS`' Email IIFE at `e4ce536` (pre-guard), `437ab4b` (guard) and
   `7b952f6`; show head vs `e4ce536` differs only by `const LABEL` / `btn.textContent = LABEL`, the comment block and the `custom:` body key (bash +
   python over `git show <sha>:stage3/strip.js`; say how you delimited it).
3. **`buildPrintDoc` is the old Generate assembly:** extract base's `btnPrint` listener body and head's `buildPrintDoc`; normalise only `finalHTML`→`html`
   and `docQnum`→`qnum`; show the remaining difference is exactly `|| !!opts.emailCopy`. And show `btnPrint` at the head calls `buildPrintDoc(mode,
   docQnum)` with NO opts (so the print never takes `emailCopy`).
4. **The route (unchanged blob, READ):** quote the server module's `/api/quote/email` lines that pass `state` to `renderQuotePdf` (whole, `custom`
   included) and `advanced: !!req.session.advanced`; quote `storableQuoteState` and its "Deliberately NOT stored" comment (no `custom`, `pm*`, `cp*`).
5. Read the PR files API (`gh api repos/datasecau/vision_hpas-quickquote/pulls/10/files`) and show it equals `git diff --numstat` (6 rows, blobs).
6. The `package.json` change: `git diff -U0` shows ONLY the `test:print` line; prove the dependency maps (`dependencies`, `devDependencies`,
   `overrides`, `engines`) and `version` identical by JSON parse at both shas.
7. **What strip.js generates:** in a fresh base and head tree, `node strip.js`; sha256 + bytes of `public/index.html`, `private/advanced.js`,
   `private/svc.js`; `diff` each pair and map every differing line to a hunk of item 1 (expected: the `index.html` changes in both outputs where the
   region lands, `cpExport`/`cpRestore` only in `advanced.js`, the guard's removal and the `custom` key only in `public/index.html`'s `HOSTED_EXTRAS`).
   Confirm `cpExport` / `cpRestore` are NOT in the stripped `public/index.html`.

## N2. THE RED-PROOFS AND THE MUTANTS (MEASURED; never trust the mail; WRONG (b))
**FAIL condition:** a new or rewritten test passing on base code; a base failure for a reason that is not the absence of fix (2) (setup error, drawer
timeout, "the custom ticket never took the -10% price", Chrome launch) reported as the red; the control cell failing on base; any cell failing at the head
on a clean tree.
1. **Base-code trees (each fresh, `git archive`, `npm ci --offline --ignore-scripts`, the lockfile proven entry by entry by `lockcmp.py` AND
   `lockwalk.py`):**
   - **R-A: `437ab4b` + the head's `test/email-matches-print.mjs`** (blob `3ac0e3c`, sha1 asserted after the copy; `node --check` rc 0 — a test that does
     not parse is VOID). Run `node strip.js && node --test test/email-matches-print.mjs` from `stage3/` under `qa-run.py` with
     `PUPPETEER_EXECUTABLE_PATH` = YOUR egress wrapper. Quote every `not ok` with its assertion message. Predicted (WRONG (b)): default cells fail on
     `unknown`; custom/both fail before any figure is compared, on the guard.
   - **R-B: `e4ce536` (pre-guard main) + the same file**: predicted 9/9 on `unknown` (the builder's original red). Quote it.
   - **R-C: `437ab4b` + the head's `test/email-print-mode.mjs`** (blob `9dd5311`): READY claims custom and both fail, the control passes. Quote it.
2. **Head tree:** a fresh `git archive 7b952f6`, same install and proof; both files alone, 3 runs each; each run's wall time with the load.
3. **Mutants — each on a FRESH head tree, tamper asserted landed, `node --check` rc 0 on the changed file, `node strip.js` rc 0, and the mutated text
   shown present in the generated file it reaches (`public/index.html`, `private/advanced.js` or the tree's `lib/pdf.js`).** Run BOTH new test files on
   each; say which cells see it, or NONE (a mutant no cell sees is a FINDING against the tests' strength, not a FAIL of the head):
   - **G20-M1** the collector posts `custom: null` always (strip.js).
   - **G20-M2** the renderer restores the price ROUNDED as `cpMonth` carries it (2 dp in the display currency) instead of `pdmUSD` exactly — the drift the
     commit message says costs "dollars across a fleet". Say whether any cell sees it at 40 devices; §N3 P8 measures it at a large fleet.
   - **G20-M3** the renderer ignores the print mode (`printMode` forced to `"default"` in `lib/pdf.js`).
   - **G20-M4** `emailCopy: true` → `false` in `lib/pdf.js`. Also render ONE "both" email with and without M4 through the real server path and diff the
     two emailed PDFs (text and pixels) — WRONG (g).
   - **G20-M5** `advancedModule()` reads `private/svc.js` again (the v2.36 injector).
   - **G20-M6** `buildPrintRows` drops the custom block (workbook only).
   - **G20-M7** the `pmCustom`/`pmBoth` re-check after `cpRestore` removed.
   - **G20-M8** the v2.36 guard re-inserted (`strip.js` at `437ab4b`'s `HOSTED_EXTRAS` Email IIFE, with the head's `custom` key kept).

## N3. THE REAL-BROWSER DRIVE THROUGH THE REAL SERVER PATH (TIER 1; MEASURED; ONE browser at a time)
**FAIL condition:** at the head, in ANY advanced cell, the emailed PDF or workbook disagreeing with the print of the same state (per D5, §N4); a press
that does not send exactly once (one POST, one captured mail, both attachments); W1 or W2, or `svc-warn` on `#emailPdfNote`, anywhere on the page at
the head; a simple session or an advanced standard email differing from base's beyond the version tokens (§N5); a render that throws, 500s or prints
`NaN`/`undefined`/`Infinity` for a shape a rep can produce through the page's own controls; a page or console error at the head that base does not also
produce for the same steps.
1. **Instrument (PRIMARY — the real server path):** YOUR harness `require`s the tree's own hosted server module's `createApp()` export (NEVER its
   entry point, NEVER with a real secret): the repo's in-memory store and a CAPTURING stub mail (gate 19's `qa-harness-g19-drive.cjs` builds exactly
   this; copy and re-point it, and INVERT its W1/W2 expectations), a throwaway `sessionSecret` of 48 random chars and a throwaway `unlockSecret` (fresh
   random; never the HPAM word), `salesCopy` = `sales-copy@qa.invalid` (an option, never an env var; it lands only in the stub's `bcc`), the tree's OWN
   `renderQuotePdf` from `lib/pdf.js` with `PUPPETEER_EXECUTABLE_PATH` = your egress wrapper, `clock` FROZEN (prove it froze), `trustForwardedFor:
   false`, on 127.0.0.1 and a kernel-chosen port, under `qa-run.py` (`env -i` allowlist). ONE Google Chrome (your egress wrapper) driven by the tree's
   puppeteer-core: `/login`, the OTP the stub captured (the `Secure` cookie: WRONG (j)), Settings → Advanced → the throwaway word → Unlock (the page's own controls), close the drawer, fill
   as a rep (40 devices, 3 years, the full bundle, customer `Parity & <Probe> "QA" 'g20'`), the currency, a custom price the rep's way ("% from standard"
   `-10`, Apply), the print mode by its LABEL; then **(i) the page's own Generate/Print control** with `window.print` neutralised and the page captured as
   a PDF in PRINT media, A4 (the rep's paper), and **(ii) the page's own Email button, pressed ONCE**. Per cell record: the POSTed body (verbatim, incl.
   `custom`), POSTs seen by the server, mails captured (count, to, bcc, subject, attachment names and sizes), the server's JSON answer (qnum,
   `unknownFields`, `clearedChecks`), `#emailPdfNote` text and classes, `#btnEmailPdf` text and `disabled`, the load.
   **SECONDARY (say which rows used it):** the builder's interception method ("stubbed server") — allowed only for phone widths and P10's crafted bodies
   if the primary is too slow; never for the required grid.
2. **THE REQUIRED GRID (head AND base):** advanced × {"Standard pricing only", "Custom pricing only", "Standard + custom pricing"} × {AUD, USD, CAD} =
   9 cells per side, plus simple (never-unlocked) × {AUD, USD, CAD} = 3 per side. **At base (`437ab4b`, the live v2.36) custom/both are the guard: press 1
   shows W1 and sends nothing; press 2 sends STANDARD** — that is the base column (the defect behind the guard), and it must show the emailed figure ≠ the
   printed custom figure before "head email = print" is credited to fix (2) rather than to an instrument that cannot see custom pricing.
3. **Probes (head; MEASURED; findings unless they hit the FAIL condition above):**
   - **P1** double-press: two real clicks 100 ms apart, and 300 ms apart, in "Custom pricing only" (G19-F1's case): POSTs, mails, the note. Then a press
     after "Sent": a second send with a new number (by design; say so). Enter on the focused button: same.
   - **P2** custom price set, custom mode → Reset form (confirm accepted) → Generate → Email: mode, posted `custom`, email vs print.
   - **P3** custom price set, custom mode → Settings → Advanced off → Generate → Email: the same reads; record the posted `pdmUSD` (expected STALE,
     non-null) and the render's reported `printMode`.
   - **P4** custom mode → clear the custom /month figure → Generate → Email.
   - **P5** custom mode → the custom ticket's "Reset to default" → Generate → Email (heading, figures).
   - **P6 C-05 reopen:** (a) email a custom quote A; reopen A by its number in the SAME page; Generate; Email: the new number, email vs print; (b) reopen A
     in a FRESH advanced session (no custom price): mode, figures, email vs print — and say plainly that a reopened custom quote comes back standard
     (READ: not stored by design); (c) with A's custom price still on the page, reopen a different quote B (other device count): does A's per-device
     custom price carry into B? email vs print.
   - **P7** custom price set in AUD → change currency to CAD (and USD) → Generate → Email.
   - **P8 rounding and entry routes:** the custom price typed in each field the rep has (`cpDay`, `cpMonth`, `cpYear`, `cpTerm`, `cpPct`) with awkward
     values (e.g. a 4-dp per-day figure, a term total ending in .99), and a STRESS state: 2,500 devices, a 5-year term, AUD and CAD; every figure email vs
     print to the cent. Run G20-M2's tree on the stress state too and say whether the rounded restore would have moved the printed total.
   - **P9 a "live" FX rate:** the DRIVE Chrome answers the page's FX provider URLs by request interception with a canned rate different from the seed
     (no network: the request never leaves Chrome; the renderer's Chrome stays egress-blocked): email vs print, and the rate/provenance line on each.
     Then the race: Generate while the canned answer is held back, release it, then Email — report what the paper and the email each say.
   - **P10 crafted bodies (WRONG (i))** (a `fetch` from the signed-in page to YOUR loopback server, never anywhere else): a simple session posting
     `custom: {pdmUSD: 1}` with `pmCustom: true`; an advanced session posting `pdmUSD` = −1, `"27.9"` (string), `0`, `1e308`, `{}`, and `pmBoth` with a
     null price: per body, the HTTP status, what was emailed, `unknownFields`, any page error in the renderer.
   - **P11 mixed versions (WRONG (h)):** (a) the BASE page and base advanced module served to the drive Chrome by interception, posting to the HEAD
     server (a v2.36 tab open across the v2.37 publish): W1, press 2, what is emailed; (b) the HEAD page and head module posting to the BASE server (a
     v2.37 tab open across a rollback to v0.6.4): one press, no warning, what is emailed vs what that page printed.
   - **P12 the lone revert (WRONG (f)):** in YOUR fresh head tree only, reverse `a8d769b`'s `stage3/strip.js` hunk (`git show a8d769b -- stage3/strip.js`
     piped to `patch -R` in YOUR tree; assert landed); custom mode: press 1 (W1?), press 2: does the email carry the custom price W1 says it will not?
   - **P13 no stale words:** W1 and W2 (by the retired sha256s and by their opening words) absent from the head's generated `public/index.html`,
     `private/advanced.js`, `private/svc.js`, and from the live DOM (`document.body.innerText` and `#emailPdfNote` / `#btnEmailPdf` raw `textContent`)
     after every cell and probe; `#emailPdfNote` never carries `svc-warn`; the button always reads `Email me this quote (PDF & XLS)`. Control that can
     fail: the same scan over the BASE page after a custom press 1 must FIND W1.
   - **P14 themes and widths:** the print PDF in light and dark (the page's own toggle) — identical on paper or not? say which; 1280 px and 375 px and
     320 px, light and dark, after a custom "Sent": page `scrollWidth <= innerWidth`, the button label fits, no W1. Sequential; NOT RUN with the load if a
     cell and its one retry overrun.

## N4. WHAT THE RECIPIENT GETS vs WHAT THE REP PRINTED (TIER 1; MEASURED; method per N4-METHOD, D5; WRONG (e))
**FAIL condition (FULL-TEXT):** for any head advanced cell or probe state a rep can reach through the page's own controls, the emailed PDF's
`pdftotext -layout` text differing from the printed PDF's after normalising ONLY the quote-number token (state the regex, count the substitutions); the
money multiset differing; the page count differing; any workbook money figure absent from the printed quote or any printed section missing its block;
THE NOTE's text, a margin or a "% below/above the standard rate" figure in the emailed PDF or the workbook. **(FIGURES):** the money multiset in order
differing; other text differences are reported. Either way, every row reports text, money, pages, fonts and pixels.
1. **Method:** `pdftotext -layout` full-text diff; the MONEY-FIGURE MULTISET (every currency amount token: `A$`, `US$`, `CA$`, `$` and the tool's other
   prefixes followed by digits, by a regex you state); `pdftoppm -r 100` pixel diff per page in plain python on PPM (no ImageMagick, PIL or numpy) with
   the bounding box of every differing region (expected: only the quote-number boxes); `pdfinfo` pages + A4; `pdffonts` set (subset tag stripped).
   Workbook: unzip; every sheet part; list each money cell and its number format; the title row(s) ("Quote Estimate" / "Custom Quote"); the qnum.
2. **The pairs:** every §N3.2 head cell (email vs ITS print); every §N3.3 probe state; base custom/both press-2 email vs base custom print (the defect,
   reproduced: must differ).
3. **Controls that can fail, BEFORE any zero is believed:** a planted one-word and one-digit change and a one-pixel change must each be reported; the
   base defect pair must report a difference; head AUD vs head CAD must report a difference.
4. **THE NOTE and THE VALUE NOTE, per mode (REPORT only; not graded — RULED BY KAM, AND SETTLED):** a table, rows = default / custom / both, columns =
   on screen (`#quoteDoc` in screen media) / the printed PDF / the emailed PDF / the emailed workbook: present or absent, each, with the evidence.
5. **What the recipient sees beyond the attachments:** the captured mail's `to`, `bcc`, `subject` and `text` (they carry no price; say so) and that ONE
   send carries both attachments to both recipients.

## N5. SIMPLE SESSIONS AND STANDARD EMAILS UNCHANGED vs MAIN (TIER 1; MEASURED; WRONG (d))
**FAIL condition:** a simple-session email (AUD/USD/CAD) or an advanced "Standard pricing only" email at the head differing from base's for the same
inputs in anything other than the version tokens `v2.36`→`v2.37` and (if not frozen) the quote number; workbook parts differing other than
`docProps/core.xml` and the parts that carry the version (name each); the POSTed body differing other than the added `custom` key.
1. Base vs head, same inputs, frozen clocks: text diff after normalising exactly the version tokens (count them: expected 2 per PDF, the page-1 footer
   and page 2) — 0; money multiset equal; pixels: differing regions only inside the version-string line boxes (bbox); pages, fonts equal.
2. The posted body, head vs base: identical but for `custom: null` (simple) or `custom: {pdmUSD: null}` (advanced, no price). Quote both.
3. The OFFLINE tool (`index.html` opened as a FILE, no server, the tree's own root `index.html`, fresh base and head): Generate in each mode ×
   AUD/USD/CAD (advanced mode needs no server offline — say how you unlocked it, READ the page) — printed PDF text base vs head after the version and
   qnum normalisation: 0 differences expected; any other is a FAIL (the offline tool's printed quote is a customer document too).

## N6. THE REPO'S CI SUITES, AS CI RUNS THEM, AT `7b952f6` (and base) — as SETS, NOT COUNTS (TIER 1)
**FAIL condition:** any suite red at `7b952f6` on a clean tree; a test NAME passing at `437ab4b` that does not pass at the head, other than exactly the
5 cells of `email-print-mode.mjs` blob `b1d4443` (the guard's, removed by design); `test:print`'s added names other than exactly the 3 cells of
`9dd5311` and the 9 of `3ac0e3c`; `npm ls --all` rc ≠ 0 at the head; any installed package not byte-equal to the lockfile's integrity.
1. **Trees:** fresh `git archive` extractions of `437ab4b` and `7b952f6` under `projects/vision/work-g20/` (separate from §N2's); `npm ci --offline
   --ignore-scripts` (a cache miss FAILS, then NOT RUN with the tarball named); lockfile proven entry by entry (`lockcmp.py` AND `lockwalk.py`); `npm ls
   --all` rc and stderr.
2. **The suites by PATH and command (tests.yml at the head, READ):** root `node --test quote-engine.test.mjs` (READY 69); in `stage3/`: `npm test`
   (132), `npm run test:print` (182 head / 175 base expected: 175 − 5 + 12), `npm run test:xlsx` (6). Each ×1 at base and ×2 at the head, same session,
   as SETS by test NAME (`tapsets.py`, `g17-dupnames.py`): lost (must be exactly the 5 guard names), added (exactly the 12), removed, duplicates. **Host
   Node is v26.8.1, not CI's 22: say so on every row.** Every Chrome under YOUR egress wrapper. `npm run test:azurite` is NOT RUN (no docker) — relay
   CI's `store-azurite` success on `7b952f6` as READ ONLY.
3. Never `npm install`, never `npm audit fix`. The lockfile is an unchanged blob: no `npm audit` is required (say so).

## N7. THE OFFLINE `index.html` AND THE GENERATED FILES (TIER 1 by the customer's printed quote; READ + MEASURED)
**This differs from gate 19: `index.html` CHANGES here.** **FAIL condition:** a change in the generated `public/index.html`, `private/advanced.js` or
`private/svc.js` not explained by §N1's hunks; `cpExport`/`cpRestore` reachable in the stripped (simple) page; the guard's text in any generated file.
1. §N1.7's three diffs, each line mapped.
2. Whether `window.cpExport`/`window.cpRestore` exist in the OFFLINE advanced page (READ: they sit in the ADVANCED JS region, which the offline file
   carries) and what calling them can change there (nothing is posted offline — say so).
3. §N5.3's offline print comparison is the measurement.

## N8. NOTHING PUSHED, MERGED OR PUBLISHED; LIVE SITE UNCHANGED (commission; READ ONLY)
**FAIL condition:** any `git push`, merge, PR comment/review/label/approval, workflow re-run, alert dismissal, `docker` command of ANY kind, `az`
command, or deploy in your command log; any write in the QuickQuote repo or in `Vision_Sales_Portal/`; any HTTP request to the live QuickQuote or the
live portal; the live webapp's `linuxFxVersion` at verdict (Tuesday's re-read) differing from AZ-PRE-READ without an explanation that is not you.
1. **Your own discipline, MEASURED:** your shell history for this session grepped for `push`, `merge`, `docker`, `az `, `gh pr`, `-X`,
   `azurewebsites.net`, `hpas-quickquote` as a URL host (quote the zeros beside a positive control — the same grep over a scratch file that contains
   each reads 1); `stat` the repo's `.git/index` mtime at start and end and say only whether YOU could have touched it.
2. **The Azure side (AZ-READ-LEG = TUESDAY-READS):** RELAY the `AZ-PRE-READ` line appended to your prompt; say the post-read is Tuesday's at verdict.
3. **What a publish of `7b952f6` would ship (READ ONLY):** from the AZ-PRE-READ tag's trailing sha (expected `…-437ab4b`), `git log --oneline
   --first-parent <live>..7b952f6` and `git diff --stat <live> 7b952f6`; name every file (expected exactly the 6 of the delta; no lockfile, Dockerfile or
   server-module change). If the tag carries no sha or a different one, say so and list the delta from it.
4. **Rollback (READ ONLY, for the publish card):** the READY's rollback tag; what P11(b) measured about tabs open across a rollback; what P12 measured
   about reverting `a8d769b` alone.
5. **Deploy-on-merge (READ ONLY):** `.github` at the head holds only `tests.yml` (no deploy, no image build, no registry login); if GH-API-LEG allows:
   repo hooks, environments, deployments. State whether a merge deploys anything, with each statement's evidence class.

## N9. CI AND CODEQL ON PR #10 (READ ONLY; never caused)
**FAIL condition:** a tests.yml run on `7b952f6` not `success` on all five jobs; a CodeQL check run on `7b952f6` failing; any alert dismissed.
1. GH-API-LEG = READ-ONLY-VISION-TOKEN: `actions/runs/38949473743` (push) and `/38949480136` (pull_request): head_sha, conclusion, and their `/jobs`
   (five names, each `success`); the print-fit job LOGS via `gh api …/actions/jobs/<id>/logs` (a GET; print-fit job ids 117136924895 and 117136945803
   at drafting): the `email matches print — <mode> · <cur>` lines and `# tests 182`; if the shim or GitHub refuses, NOT RUN; `commits/7b952f6…/check-runs`;
   `code-scanning/alerts?state=open` count on main. Otherwise NOT RUN.
2. **What CodeQL can say (WRONG (k)):** the PR-side zeros are blind. Name the post-merge reads: main's code-scanning still 0 open, tests.yml green on
   the merge commit.

## 12. The merge and the queue
QQEP is 3 ahead and 0 behind `437ab4b`, so a GitHub merge commit's tree equals `7b952f6`'s (`25ddfb8`) while main stays at `437ab4b` — prove 0 behind
with `rev-list --count`; run `git merge-tree --write-tree` only from YOUR OWN object dir, or skip it and say so. **If PR #8 (C-19) merges first, PR #10
must be re-merged over a moved main: name the cells to re-run then** (at least: §N6's four suites, §N2's head runs, §N3.2's head grid on the merged
tree). **Cells to re-run at merge:** tests.yml's five jobs on the merge commit. **At publish (Kam's word under C-20; not this gate):** the built image's
generated files equal to this gate's head tree's; Kam's live check (an advanced custom quote emailed to his own inbox, compared with its print); the
rollback tag kept.

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
   egress-block wrapper; P9's canned rate is served by request interception INSIDE the drive Chrome (the request is answered before it leaves); prove
   the block with its positive control (`qa-egress-posctl.mjs`) and run the net-log scan at the end; record GoogleUpdater and chrome_crashpad_handler at
   start and end (`qa-chrome-census.py`).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): "ours" = the ancestor chain CONTAINS your
   claude pid. **Negative controls, same run, must classify FOREIGN.** The launcher DERIVES the negative-control seats live from the cockpit panes
   (the `tuesday` pane, the `Datasec/Vision_Sales_Portal` builder pane, and any live `QA/*` / `fleet-monitor` pane) and appends them to your prompt.
   **A zero is reportable only beside a control that fired in the same window.** **Record the 1-minute load beside every timing.**
5. **ONE BROWSER AT A TIME.** Never two drive Chromes of yours alive at once (the suites' own Chromes count as yours); never run a suite and a §N3 drive
   concurrently. Inside a §N3 send the renderer's own headless Chrome runs while the drive Chrome is open: that pairing is mandated (gate 19 reading 1);
   release both in each cell's `finally`. Never `docker` anything.
6. **THE DEADLINE RULE:** every step has a written DEADLINE built into your runner (no `timeout` binary here) and a client timeout on every request;
   a step past its deadline is ABORTED and reported. Deadlines: one browser cell 120 s (§N3, §N4, §N5 each render); one §N2 arm 420 s; root pack
   120 s; a whole `npm test` 300 s; a whole `test:xlsx` 300 s; a whole `test:print` 900 s; nothing above 900 s. One retry per cell at most, then NOT
   RUN with the load. **Every Chrome, page, child, app server and temp profile you start is released in a `finally`.** **Log a HEARTBEAT line
   (timestamp, step, pid, elapsed, load) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.**

**Reap everything you start.** An orphan Chrome or listener of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, `hpasqqacr`, its Table Storage, its log workspace) and **NEVER the live**
  portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION). **No HTTP request to either, not
  even a GET. Press nothing there. No az at all — no writes, no app-setting change, no deploy, no publish, no ACR build, no ACR push.** Never the FX hosts
  (blocked by your wrapper; P9 answers them inside Chrome), never ntfy.sh. **Never Claude in Chrome** (Kam's real Chrome with his sign-ins). Never open
  anything under `Vision_Sales_Portal/4_Credentials/` (the launcher wires the gh config itself; you never read its files), **never read, ask for or type
  the HPAM word** (the live check is Kam's), and never read the builder's `fix2-email-matches-print-2026-10-17-evidence/` as evidence (you may LOOK at
  its PDFs to compare with yours; say so).
- **No email to any human address.** Every send in this gate goes to the capturing stub mail; recipients are your sign-in address on a `.invalid`
  domain and `sales-copy@qa.invalid`. Your own AgentMail calls go only to `tuesday-agent@agentmail.to` (verdict / question).
- **Network, and ONLY this:** `git ls-remote origin` (head readings); `gh api` GETs (GH-API-LEG); your AgentMail calls. Nothing else reaches the
  internet: no npm registry (`npm ci --offline`), no `npm audit`, no image pulls.

### HELD
- No merge, no deploy, **no publish**, **no registry push**, **no production**, no money, **no mail to any human**, no external comms. **No comment,
  review, label, approval or status on PR #10, PR #8 or any GitHub object; no re-run of any workflow; no alert dismissal of any kind.**
- **No `docker` at all, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npm audit fix`, no `npx` of anything not already in your
  tree. `gh` only as GH-API-LEG allows; no `az`.** The launcher points `AZURE_CONFIG_DIR` at an EMPTY directory.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g20/>`, in `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never
  touch any other `work*` directory** (`work-g19/` and `work-g18/` included). In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse,
  ls-tree, cat-file, grep, merge-base, archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean, gc, branch, revert or
  for-each-ref.** P12's reverse patch is applied to YOUR extracted tree by `patch`, never by git in the repo. `merge-tree --write-tree` only from your
  OWN object dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own. **For this
  gate: the base column must show the emailed custom figure ≠ the printed custom figure before the head's "email = print" is credited to fix (2); the
  PDF comparator must report non-zero on a planted one-word, one-digit and one-pixel change; the stale-words scan must FIND W1 on the base page; each
  mutant must be shown to have LANDED before its result is read; the egress block's positive control fires; the floor count rises on its attached
  control.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the QuickQuote repo** (its working tree is the
  builder's, live) **and none inside `Vision_Sales_Portal/`**, none in gate 1-19's report folders or trees. Describe fix-shapes in prose.
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
**R1-R8 are the commission's requirements as Tuesday wrote them to the drafter (2026-10-17 ~05:47), carried as ruling lines. Apply them; do not
re-rule them.**
- R1: ONE gate, TIER 1 (quote output) on QuickQuote PR #10 @ 7b952f6 over main 437ab4b: the emailed PDF and workbook follow the rep's print mode and exact custom price (shared builder buildPrintDoc/buildPrintRows; collector posts custom.pdmUSD; advanced render loads advanced.js); the v2.36 email guard removed in a8d769b (separate commit); toolVersion 2.37.
- R2: Rulings checked as built, not re-opened: the Custom pricing note stays OFF the emailed PDF and ON the print (Tuesday 2026-10-16 ~14:02, reversible by Kam on the publish card); the guard's removal approved (Tuesday 2026-10-17 05:4x), W1/W2 retired; Kam's original ruling C-20 (a) "Publish the guard as soon as it passes the gate, full fix after".
- R3: The print CSS `.q-savings { display:none }` (5ef2a60, since v1.88) hides the custom note and the standard Value note on paper: the gate REPORTS what is on paper in each mode and does not grade the product choice.
- R4: The builder's QA focus, included: an advanced session in each print mode x AUD/USD/CAD, the emailed PDF and workbook against the printed quote figure by figure; simple sessions unchanged against main; one press sends with no stale warning or label anywhere; Reset form / Advanced off after a custom price then email -> standard; reopen a previous quote (C-05) and email again.
- R5: Adversarial cases added: the double-press timing (gate 19's G19-F1 case); currency rounding; what the email RECIPIENT sees against what the rep printed.
- R6: Model the gate on gate 19's kit and report (G19-F1..F4, P1, P2 are the reference for a careful gate on this UI).
- R7: HARD LIMITS as gate 19: no production access (the live QuickQuote is production, datasec-sales-portal-rg / the hpasqq app); press nothing on the live site and never read the HPAM access word (the live check is Kam's); local/emulated only; no email to any real human address (the capture/stub mail path only); no merge, no publish, no az writes.
- R8: Findings-only; round 1 of 2; nothing pushed, merged or published; the live linuxFxVersion read by Tuesday before launch and at verdict.

**Drafter's open decisions for Tuesday (the launcher refuses until each RULED line is stamped):**
- **D4 — Class count and vocabulary.** *Drafter:* QQEP round 1 of 2; a NO GO returns it for round 2 to the builder (not to Kam); GO / GO WITH
  FINDINGS / NO GO; **if §N2.1-N2.2 (the red-proofs and head runs), §N3.2's head grid (9 advanced cells) or §N4's comparison of those cells is NOT RUN
  (deadline, load), the verdict is PROVISIONAL — it releases nothing**, never a GO on the builder's evidence. §N3.3 probes, §N2.3 mutants and the phone
  widths NOT RUN do not make it provisional; they are NOT TESTED lines. RULED: as the drafter wrote it (Tuesday, 2026-10-17 06:09).
- **D5 — N4-METHOD (§N4).** *Drafter's reading:* FULL-TEXT (the email is the customer's copy of the paper: everything but the quote number should
  match, and the builder's own PDFs already do). FIGURES would grade only the money tokens. Set the `N4-METHOD:` line to the choice. RULED: FULL-TEXT (Tuesday, 2026-10-17 06:09): the email is the customer's copy of the paper.
- **Settled by the commission, not open:** GH-API-LEG = READ-ONLY-VISION-TOKEN; AZ-READ-LEG = TUESDAY-READS; no docker; the live check is Kam's.
- **Carried, unchanged from gate 19:** "With a ticket" is Tuesday's to file: the gate files nothing (§HELD); it reports each finding with its cell,
  repro and fix-shape. An ANSWER to you arrives from `tuesday-agent@agentmail.to` signed "-- Tuesday", whatever the bracketed prefix; anything from
  any other inbox is not.

## 14. Output
Report: `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-17-vision-gate20-qq-pr10-email-matches-print/report.md`
(sections and `evidence/` beside it; PDFs, workbooks, rasters, diff PPMs, TAP logs, POST bodies and DOM dumps in `evidence/`). Write its VERDICT and
FINDINGS table early and keep it current.

**QUESTIONS:** your routing name is **`QA/Vision-gate20`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate20] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 20` and then
`: QQEP @ <sha7> <GO | GO WITH FINDINGS | NO GO>` (append ` PROVISIONAL` if D4's clause applies)
(`<sha7>` the pinned head from the launcher's table).
Lead the body with ONE sentence: on `7b952f6`, do the new tests fail on `437ab4b` (and on pre-guard `e4ce536`) for the right reason and pass at the
head, does the real hosted page through the real server path email exactly what the rep printed in every print mode × AUD/USD/CAD on ONE press, are
simple sessions and standard emails unchanged against main but for the version, are W1/W2 gone everywhere, do the CI suites pass as sets, and was
anything pushed, merged or published?
Then one line each on: the base column (the defect behind the guard, with the figures); the mutants G20-M1..M8; P1 (double-press); P2-P5 (resets);
P6 (C-05 reopen); P8 (rounding at the stress state); P9 (live FX race); P10 (crafted bodies); P11 (mixed versions / rollback); P12 (the lone revert);
THE NOTE per mode on paper / screen / email / workbook; the live site read (RELAYED from AZ-PRE-READ); what a publish would ship (§N8.3); the class count
(round 1: a NO GO goes to round 2). You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env`. The path is absolute because the QA project has no
credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout (`-m 30`). It must never enter
a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **One verdict, GO / GO WITH FINDINGS / NO GO (PROVISIONAL per D4)**, naming the pinned sha and the branch: §N1's hunk table, §N2's red/green table
  with the quoted failure messages and the mutant table, §N3's grid (cell × base/head × POSTs/mails/qnum/unknown/printMode/load), §N4's comparison table
  and the note table, §N5, §N6 as sets, §N7, §N8, §N9, row by row.
- The verbatim strings: the base red messages, each mutant's failing cells, the P1 POST counts, the emailed and printed figures per head cell (and the
  base defect pair), the stress-state totals with and without G20-M2, the AZ reading "RELAYED from AZ-PRE-READ".
- **A table with one row per §N item: MEASURED / NOT TESTED / NOT RUN / VOID, and HOW (command, tree, browser, port, load).** No row without a HOW.
- **Rule 2: what you did NOT test is first-class output.** Say the READY carried no NOT TESTED block (WRONG (a)). A NOT TESTED section covering at least
  **the published image (no docker by design)**, **a real ACS send (stub mail only)**, **the live site (Kam's check)**, **CodeQL's verdict (blind
  pre-merge, WRONG (k))**, **CI's Node 22 (host is Node 26.8.1; CI read only)**, **store-azurite (READ from CI)**, **a real live FX provider (P9 is a
  canned answer)**, **currencies other than AUD/USD/CAD** unless you drove them, **Windows / Safari / the account managers' real browsers and real phones
  and real printers**, **what a customer's mail client does with the attachments**, **screen readers**, **Claude in Chrome (not used)**, **PR #8 (not
  this gate)**, and every §N row you did not run, with the reason. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME /
  PROBED / READ ONLY.**
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name, plus `refs/pull/10/head`.

PROVENANCE:
- heads: main `437ab4bc412b…` (= HEAD), `fix/qq-email-matches-print-2026-10-16` `7b952f6edbcc…`, `refs/pull/10/head` `7b952f6…`, `refs/pull/10/merge`
  `d46f5f5d…`, `refs/pull/8/head` `4d6ed6ef…`, `refs/pull/11/head` `818a019e…` | `git -C <quickquote on Laptop-DEV> ls-remote origin` | read 2026-10-17 05:47:35 AEDT
- the chain (`0fc280b` ← `437ab4b`, `a8d769b` ← `0fc280b`, `7b952f6` ← `a8d769b`), author dates, counts 3 / 0 behind, merge-base, numstat whole and per
  commit, the unchanged-blob list, head tree `25ddfb8`, `437ab4b`/`818a019` tree `c71780c`, `9d1c5ab`/`5f08fe0` tree `dc6aef6`, commit messages | `log`,
  `rev-list --count`, `merge-base`, `diff --numstat`, `rev-parse <sha>:<path>`, `rev-parse <sha>^{tree}` | read 05:47-05:5x
- the code at `7b952f6` and `437ab4b` (`strip.js` HOSTED_EXTRAS; `lib/pdf.js` renderQuotePdf whole; `index.html` buildPrintDoc/buildPrintRows/
  buildQuoteRows, the ADVANCED JS region cpState/cpLocal/cpSyncFrom/cpClear/renderCustom/btnResetCustom/btnApplyPct/cpExport/cpRestore, btnReset,
  applyAdvanced, PRINT CSS ~701, toolVersion ~1732, footers ~2763/~2983; the server module's /api/quote/email, storableQuoteState, GET /api/quote/:qnum;
  both test files whole; package.json versions) | `git show` under bash | read 05:5x-06:1x
- the builder's evidence README and `pdftotext -layout` of its `main-818a019/default-print-light.pdf` vs `fix-7b952f6/default-print-light.pdf`, and of
  `fix-7b952f6/<mode>-email.pdf` vs `<mode>-print-light.pdf` (4 / 6 / 4 differing lines, all quote numbers; both-email 3 pages A4) | `pdftotext`,
  `pdfinfo`, `diff` | read 06:0x (LOOKED AT, not evidence)
- GitHub (READ-BY-DRAFTER, `gh api` GET with Vision's gh-config; its two files' mtimes unchanged, 12 Oct 18:09:30): PR #10; PR #10 files; runs
  38949473743 / 38949480136 + jobs; check-runs on `7b952f6`; code-scanning open 0 on main; Dependabot open #1 #4 | read 05:5x
- the two mails (read whole, copied verbatim, sha256 `ac43ba5d…`); CLARIFICATIONS C-20 whole; Tuesday's `0_Brain/daily_tuesday/2026-10-16.md` entries
  13:52, 14:02, 15:03, 15:07, 15:25 and `2026-10-17.md` entries 05:30-ish and 05:47 | read 05:5x
- gate 19's brief, DRAFTER-REPORT, launcher and report (whole), and its `evidence/tools/` listing and the drive harness's header | read 05:47-06:0x
- load 5.70/5.27/4.45 (05:51); tmux panes `tuesday`, `Datasec/MPS-LE`, `Datasec/MPS-LD`, `Datasec/Vision_Sales_Portal`, `fleet-monitor`; host node
  v26.8.1; `inbox_routing.conf` has no `QA/Vision-gate20` line; no gate-20 report folder | `uptime`, `tmux list-panes -a`, `node -v`, `grep`, `ls` | read 05:51
- no merge-tree, no fetch, no docker, no product process, no browser, no `az`, no npm, no mail was made by the drafter; `gh` was used for GET reads only
