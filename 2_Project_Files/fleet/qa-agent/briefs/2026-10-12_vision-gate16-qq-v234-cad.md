# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 16: ONE TIER-1 QuickQuote gate — QuickQuote v2.34 (CAD currency) @ `9bd21c0` on QuickQuote main `e408904` — one verdict, one report

**TIER 1 (Kam's ruling C-14, as Tuesday's plan-confirmation carries it: customer-shown pricing), FULL WEIGHT: through the code AND a real
browser.** ROUND 1 of this ticket. No NO GO has been spent on the CAD change. A NO GO sends it to its round 2; it does not go to Kam.

**Drafted for Tuesday on 2026-10-12 at 14:5x-15:2x AEDT by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Template: gate 15's brief `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_vision-gate15-tier1-vsp83-vsp86.md`
(method, standing rules and section shape) and, for the QuickQuote repo and its browser instrument, gate 8's brief and launcher
(`launch_qa_vision_qq_gate8.sh`) and gate 9's §Q. **This brief governs where they differ.**

**WHY ONE TARGET, AND WHY THE BROWSER.** The change is four lines of `index.html` (two `<option>`s, one seed, the version) plus tests and
docs. The engine already priced any ISO currency, so most of the risk is NOT in the arithmetic: it is in the wiring a select change touches
(the FX lookup, the seed fallback, the Settings drawer, a reopened quote, `Intl` formatting on screen, in print and in the workbook) and in
the seven currencies that already ship. Only a real page can see that. **§N1 re-runs the builder's suite and red-proofs; §N2 is the
independent browser leg; §N3 is the no-regression leg on the other seven currencies; §N4 is brand/style; §N5 is the builder's own finding;
§N6 is deploy-on-merge (READ ONLY).**

The builder's READY mail under test (on disk, read whole by the drafter, INCLUDING the correction mail appended at its end):
- `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-12_vision-qq-v234-cad-READY-mail.txt`
**Every builder statement below comes from that mail, the commit messages or the code at each sha. Each one is a CLAIM. Every red, every
mutant and every suite set must be RE-DERIVED by the gate. None is taken from the READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch — **including any move of QuickQuote main** (this gate pins main exactly; it does not allow a descendant). The verified table is
appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-12 15:04
Self-check note: Tuesday read the rulings section, the pins (branch 9bd21c0, base e408904, both by ls-remote 14:5x) and the NODE20 setting before stamping. Node 20 stays NOT-RUN and is carried as NOT TESTED.

NODE20-LEG: NOT-RUN
<!-- Drafter's setting, for Tuesday to confirm at stamp. Docker was DOWN at drafting (`docker info`: "Cannot connect to the Docker daemon",
     14:55 AEDT), so `node:20` could not even be inspected. Production's container is `node:20-bookworm-slim` with Debian `chromium`
     (stage3/Dockerfile, same blob at base and head): a DIFFERENT browser from the Mac's Google Chrome. The offline tool runs in the account
     manager's own browser, and the hosted build's PDF/xlsx render in that container. Both are carried as NOT TESTED (§14). -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build this change and you owe the builder nothing. **Every line below that reports what the builder says is a CLAIM,
never evidence.**

**One gate, ONE target, ONE verdict: GO / GO WITH FINDINGS / NO GO, at its pinned sha.**
- **QQCAD** at `9bd21c0` — **TIER 1 (C-14, Tuesday's plan-confirmation ANSWER 2026-10-12T03:41:14Z: "tier 1"; customer-shown pricing).**
  ROUND 1. QuickQuote v2.34 offers CAD in both currency selects (`#currency` on the quote, `#psvCurrency` in the Settings drawer), adds the
  offline seed `CAD: 1.4200`, and bumps `toolVersion` to `2.34`. Professional services = the USD rate card × FX (no CAD rate card).

**Names, written out every time:**
- **QQCAD** = branch `feat/qq-cad-currency-2026-10-12` = QuickQuote **v2.34** = the commits `aef649a` (the change) + `9bd21c0` (a BACKLOG
  ticket only). **C-14** = Kam's ruling, card `quickquote-cad-currency-1012` = (a). **C-13** = Kam's "look at the QuickQuote feedback and
  action it" (the pause lift this work sits under). John Spears = the requester (NEVER contacted by anyone in this gate).
- **"cells 1-5"** = the builder's five cells as its READY numbers them; **"M1-M6"** = the builder's mutants; **G-M1 ..** = yours.

Branch: `feat/qq-cad-currency-2026-10-12`. **It is NOT on main.**

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole. It carries C-01..C-14 (read 14:5x). **Cite only what you open.** The entry this gate turns on:
  - **C-14 (Kam, live board 2026-10-12 14:31:35 AEST, card `quickquote-cad-currency-1012`):** "Decision quickquote-cad-currency-1012: a — Add
    CAD, priced like the other non-regional currencies". The option text the clarification carries: "Live FX as now. Offline fallback seed 1.42
    CAD per USD (ECB 9 Oct). Professional services = USD rate card × live FX. Built as v2.34 with red-first cells, through the QA gate.
    Publishing comes back to you." Shape (Tuesday's ANSWER 03:41:14Z): **tier 1; the CAD pricing cell is a guard, not red-first**; the "CA$"
    prefix that `Intl` `en-US` prints is **named to Kam before publish**. **Not covered:** publishing or deploying v2.34 (Kam's separate
    decision, screenshots first); merging before Tuesday's GO; ANY other seed rate, including the stale AUD seed (ticket only, branch
    `backlog/qq-aud-seed-2026-10-12`); any reply to John Spears.
- **PRODUCTION IS LIVE for this project.** Live QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, its registry `hpasqqacr`, its Table
  Storage and its log workspace) and the live portal (`datasec-sales-portal.azurewebsites.net`, `datasec-sales-portal-rg`) are PRODUCTION.
  **Nothing in this gate touches either** (§13, HELD). Live QuickQuote is v2.33 (`e408904`'s `toolVersion`; deployed per BACKLOG at
  `e408904`: "retention purge deployed (v0.6.1-tool2.33-986f7b8)").
- **Deploys and publishing are HELD for Kam. Nothing merges on your word.** A merge is Tuesday's GO on a pinned head. A publish is Kam's word.
- **The BUILDER's choices, each judged by the gate (say whether each needs Kam):** (1) CAD is placed after AUD in both selects (not
  alphabetical among the rest); (2) the seed is 1.4200 (Kam's 1.42); (3) the money format stays `Intl` `en-US`, so CAD prints `CA$` (C-14
  says this is named to Kam: the gate MEASURES every place it appears and every place it does not); (4) cell 2 is a GUARD, green at base by
  construction (Tuesday's ruling); (5) print-fit and xlsx-parity gained a "the currency actually took" assertion (a strengthening of two
  existing suites: confirm it is not a weakening); (6) the three static USD labels are TICKETED, not fixed (§N5).

## PRIOR ROUND
PRIOR ROUND: none on this ticket — **ROUND 1** of QQCAD. The last QuickQuote gate was gate 9 (QA/Vision-gate9, 2026-09-27): **QQPURGE GO at
`ac74111`** (merged; deployed as v0.6.1-tool2.33). The QuickQuote browser instrument (Chrome egress block, census, floor count) was last
built and used by gate 8 (QA/Vision-gate8, 2026-09-25).
ITS REPORT IS ON DISK AT: gate 9 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-27-vision-gate9-vsp65-qqpurge`
(`report.md`; §Q, FINDINGS INDEX, NOT TESTED, `evidence/tools/`) and gate 8 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-25-vision-qq-gate8`
(`report.md`, `sections/`, `evidence/`). Findings carried forward: none on CAD (it did not exist). Gate 8's BCR2-F1 (the lib-close
child-process cell cannot go red) is ticketed in BACKLOG "## Open" and is NOT re-graded here.
- **Instruments are REUSED BY COPY:** from gate 8's `evidence/`: `qa-chrome-egressblock.sh`, `qa-egress-monitor.py`, `qa-egress-posctl.mjs`,
  `qa-chrome-census.py`, `qa-floorcount.py`, `qa-harness-floorctl.mjs`, `mktree-qq.sh`, `lockcmp.py`, `lockwalk.py`; from gate 9's
  `evidence/tools/`: `mutate-qq.py`, `run-suite.sh`, `tapsets.py`. **COPY what you use into THIS gate's own `evidence/tools/`, read it before you
  trust it, and RE-POINT every hard-coded path** (they hard-code `work-g8` / `work-g9`). **Never edit, run from, or write into gate 1-15's
  copies, evidence or trees.** Record the sha1 of each copy before and after your edits.
- **Self-findings from earlier gates bind you:** quote every path (the project path has a space and a `!`, and the QuickQuote repo sits under
  `Quoting Tool/`); run every loop and every `git show <sha>:<path>` under **bash, not zsh** (zsh reads `$s:stage3` as a history modifier); run
  `node strip.js` before any lone browser file; assert every tamper landed before reading its result; npm's update-notifier egresses unless you
  disable it; record the load average beside every timing number.
- **PRIOR WORK: verify every claim against git history and gates 8-9's evidence, never against this brief.** The READY's PRIOR WORK claim ("no
  CAD on any local or remote branch (git grep across refs); no CAD commit before aef649a (git log --all)") is re-derived with read verbs only.

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head and no `@`; the head is a commit; for QQCAD the base is an ancestor AND the
merge-base with MAIN; `git rev-list --count base..head` equals `commits`; `git ls-remote origin refs/heads/<branch>` equals the head NOW **for
BOTH rows — main included; a moved main REFUSES (re-pin and re-brief)**; QQCAD is not on main and is 0 behind it. Non-merge commits over the base
must be exactly `aef649a` + `9bd21c0`, with NO merges. **Never rebased:** `aef649a`'s single parent is `e408904`; `9bd21c0`'s single parent is
`aef649a`; `e408904`'s single parent is `986f7b8`.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-Q | quickquote | main | e4089041d6213d460e74992ddf775a909ffe03eb | - | - | IN |
| QQCAD | quickquote | feat/qq-cad-currency-2026-10-12 | 9bd21c0ef142cecc0dc06c6eabd0df1b2aeba63e | e4089041d6213d460e74992ddf775a909ffe03eb | 2 | IN |
<!-- PIN-HEADS:END -->

Both rows: `git -C <quickquote> ls-remote origin` read by the drafter at **2026-10-12 14:54:13 AEDT**, equal to the READY's heads
(`9bd21c0ef142cecc0dc06c6eabd0df1b2aeba63e`, main `e4089041d6213d460e74992ddf775a909ffe03eb`); `cat-file -t` = commit for both; count by
`rev-list --count` = 2.

**The chain (READ, `log --format='%H %P %s'`):** `aef649a` (parent `e408904`; "v2.34: CAD in both currency selects, with a 1.42 offline seed")
→ `9bd21c0` (parent `aef649a`; "backlog: three static USD labels stay on screen in a non-USD currency"; `BACKLOG.md` +7 only). Main's head
`e408904` (parent `986f7b8`; "backlog: retention purge deployed (v0.6.1-tool2.33-986f7b8); ticket the silent zero-row purge").

Repo: quickquote = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool` (remote
`datasecau/vision_hpas-quickquote`). Its rules: the repo's own `CLAUDE.md` (read it at the head with `git show`; its deploy and publish lines are
NOT for you) and `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md`. **⚠ The builder's checkout is ON the feature
branch and its working tree was modified at 14:4x-14:5x AEDT (a Vision seat, pane `%7`, is live): never read the working tree as evidence; build
every tree from the object store.**

**The shape (READ at the pinned shas; re-derive it):**
| file | base `e408904` | head `9bd21c0` | delta |
|---|---|---|---|
| `index.html` | `e90250f` | `afb56d6` (= `aef649a`'s) | +4 / −2: two `<option value="CAD">CAD — Canadian Dollar</option>`, `toolVersion "2.33"→"2.34"`, `fxSeeds` gains `CAD: 1.4200` |
| `quote-engine.test.mjs` (`test(`) | `9cfed94` (67) | `2d193b6` (69) | +64 |
| `stage3/test/fx-seed-fallback.mjs` (`test(`) | — | `64735f6` (3 literal; 4 cells: one loop × 2 builds) | +140 |
| `stage3/test/print-fit.mjs` | `135b380` | `b1bddb5` | +21 / −5 (a CAD fit case; the "currency took" assertion; `CASES[3]`→`CASES[4]` reindex) |
| `stage3/test/xlsx-parity.mjs` | `e167176` | `f81a82c` | +10 / −1 (a CAD case; the "currency took" assertion) |
| `stage3/package.json` | | | `test:print` gains `test/fx-seed-fallback.mjs` |
| `CLAUDE.md`, `HANDOVER/02-business-rules.md`, `BACKLOG.md` | | | docs only |
**Same blob at base and head (READ):** `stage3/lib/xlsx.js` `10bf4d7`, `stage3/lib/pdf.js` `783ebea`, `stage3/lib/store.js` `0609594`,
`stage3/lib/mail.js` `3aa8922`, `stage3/strip.js` `5a39ec5`, the hosted server module `41015ad`, `stage3/package-lock.json` `70ebda7`,
`stage3/Dockerfile` `8311ebe`, `.github/workflows/tests.yml` `cfba939`, `.dockerignore` `acf7db8`. The launcher re-proves every one.

**The code (READ at `9bd21c0`; re-derive line numbers):** `fmt()` `:2159` and `fmt0()` `:2172` are `Intl.NumberFormat("en-US", { style: "currency",
currency: $("currency").value })` — so every on-screen and printed money string follows the select. `psRatesFor()` `:1923`: non-USD → USD card ×
`fxRate`, a saved regional rate passes through untouched. `applyPsvRates()` `:3495-3512`: the main form's three PS price fields are set to
**`Math.round(USD default × rate)`** (whole units) unless a custom rate is saved for that currency. The Settings drawer `:1255-1275` (`#psvCurrency`)
and its handlers `:3573-3625`: Save writes `localStorage["hpasQuoteTool_settings"].proSvsRates[<cur>]`, then `applyPsvRates`, `render()`,
`syncCurrencyFromPsv()` (which switches the main currency to the drawer's). FX: `CONFIG.fxProviders` `:1812-1815` (Frankfurter `.dev`, Frankfurter
`.app`, Open ER-API), then the seed; a manual rate is never overwritten by a background fetch. The workbook (`stage3/lib/xlsx.js`, unchanged):
`NUMFMT = { amount: "#,##0", rate: "#,##0.00", count: "#,##0" }` `:27` and a footer `… amounts in ${report.currency}.` `:169`.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READY — found by the drafter (verify each; all are claims)
- **(a) The three static USD labels' line numbers are the HEAD's, not the base's.** READY + BACKLOG: "`index.html:1392` … `:1398` … `:1460` …
  present at e408904". READ: at `e408904` the same literals sit at **`:1391`, `:1397`, `:1459`**; at `aef649a`/`9bd21c0` at `:1392`, `:1398`,
  `:1460` (shifted by the `#psvCurrency` CAD option at `:1263`). The CLAIM "pre-existing" is TRUE at source (READ); the line numbers are the
  head's. Confirm both (§N5).
- **(b) "every CAD figure = USD × rate" holds for the ENGINE, not for what the screen and print show for professional services.** READ:
  `applyPsvRates()` rounds each PS rate to a WHOLE unit before the engine prices it (the READY itself: "Advanced CA$2,987 and Workpath 4h CA$1,592
  = the whole-unit rounded rates (2987, 398)"). Cell 2 calls `priceQuote()` directly with no PS fields set, so it never sees that rounding. **Your
  hand-worked quote (§N2.1) must compute PS as `round(USD rate × FX) × hours` on the page and say so; compare the same rule for AUD at base.**
  Pre-existing for every non-USD currency: an observation unless CAD differs from AUD (§TUESDAY'S RULINGS item 3).
- **(c) Cell 4's stored quote is hand-built, not saved.** READ: `fx-seed-fallback.mjs` answers `/api/quote/<qnum>` with a JSON object the test
  wrote (`state.fields.currency: "CAD"`), and the store needs `TABLES_CONNECTION_STRING` (no in-memory fallback). So no cell proves that a quote
  the product SAVES in CAD reopens in CAD. **Also READ:** the stored `fields` carry no `fxRate`, and the reopened quote waits for the live rate
  (`1.4226`): a reopened quote is re-priced at today's rate. Pre-existing for every currency (measure AUD at base the same way); state it.
- **(d) "CA$ … in the workbook total" was withdrawn by the builder's own correction.** The correction: "The workbook's amount cells are numbers
  with format #,##0, and I didn't read how the workbook labels the currency." READ: `xlsx.js` writes NO currency symbol in any number format; the
  only currency label is the footer text "amounts in CAD". **Measure what a CAD workbook carries (§N2.6).**
- **(e) "Settings drawer: CAD in #psvCurrency is asserted in markup (cell 1, M2) but not driven"** (READY NOT TESTED). Drive it (§N2.4).
- **(f) "Engine logic untouched" — TRUE at source (READ):** the only `index.html` lines changed are the four above; no CSS, no script logic.
  The launcher proves the exact delta.
- **(g) Counts (READ, re-derive):** `quote-engine.test.mjs` `test(` 67 → 69 (READY: "69/69"); stage3 `npm test` READY 127/127 (unchanged files:
  base must also be 127 — re-derive); `test:print` READY 150/150; `test:xlsx` READY 6/6 (base: one CAD case fewer → 5). The READY's base reds:
  print-fit 18/21 and xlsx 5/6 ("RED 'RangeError: Invalid currency code'").
- **(h) The builder's base finding:** "at e408904, a CAD value in the select doesn't just fall back. The next render throws, so a stored CAD
  quote would have broken the page." Re-derive at base with your own driver (the exact throw text, and what the page shows after).
- **(i) Deploy-on-merge (READY): "az acr task list -r hpasqqacr … []"; "The only workflow is .github/workflows/tests.yml, five test jobs, no deploy
  step"; "GitHub webhooks: UNMEASURED".** The `az` read is the builder's, authorised to IT only; **you never repeat it** (§N6). The workflow claim
  is READ ONLY from `git show 9bd21c0:.github/` (the drafter READ: one file `tests.yml`, jobs `pricing-pack`, `stage3-server`, `store-azurite`,
  `print-fit`, `xlsx-parity`, all `node-version: 22`, no deploy step — re-read it).
- **(j) `tests.yml`'s header comment still says "The 45-test pricing pack"** (READ; the pack has 67/69). Stale comment, pre-existing, Polish at
  most.
- **(k) UNVERIFIABLE by design, and you must not try:** whether the live site gets v2.34 on merge (registry / webhooks / Kam's publish path),
  CI on the branch (no `gh`), the production container's Chromium, John Spears' own browser and locale, the live FX providers' answers on any
  day, Azure Table Storage. **Carry each as NOT TESTED.**
- **Verified TRUE at source (READ 14:5x-15:1x):** both heads by `ls-remote` = the READY's; parents above; the file set (9 files); `9bd21c0` =
  `BACKLOG.md` only over `aef649a`; `index.html` same blob at `aef649a` and `9bd21c0`; the unchanged-blob list above; the base carries no CAD
  string except inside a base64 logo (`:1158`); C-14 present; the builder's six artefacts exist in the Vision project root (NOT opened by the
  drafter; they are the builder's claims, not evidence).

## THE READY — its claims and NOT TESTED (the gate rules on every claim)
Read the READY whole, **correction included**. Its NOT TESTED lines are carried VERBATIM here (the launcher checks it):

QQCAD NOT TESTED
```
NOT TESTED
- test:azurite and CI on the branch (above).
- The stage3 container itself (no image built, by design). Hosted behaviour was tested on the stripped page in headless Chrome.
- Settings drawer: CAD in #psvCurrency is asserted in markup (cell 1, M2) but not driven to Save a CAD regional rate.
- Dark-mode screenshots were checked by eye only. No contrast measurement; I used QuickQuote's own controls and no new styles.
```

**The claims, in one line each (each a CLAIM, re-derived in §N):** cell 1 (CAD in both selects + 1.42 seed + every offered currency has a seed;
red at base "#currency must offer CAD"); cell 2 (GUARD: every CAD figure = USD × 1.4226 by hand, licence 2176.578, Basic 1991.64, hourly 398.328,
services 3983.28, grand 6159.858; green at base by construction; proven by M4-M6); cell 3 (every provider aborted → 1.4200 and "stored indicative
rate table", offline AND hosted builds; control 1.4226 → 1.4226 with the ECB note; red at base); cell 4 (a stored CAD quote reopens in CAD through
"Open a previous quote"; red at base); cell 5 (print-fit CAD fit on both builds + CAD equations; xlsx-parity CAD case; red at base "RangeError:
Invalid currency code", print-fit 18/21, xlsx 5/6). Mutants: M1 CAD removed from `#currency` only → 9 failures; M2 from `#psvCurrency` only →
cell 1; M3 seed 1.24 → cell 1 + both cell-3 builds; M4 PS rate applied twice for non-USD → cell 2 + 6 existing; M5 a currency allowlist without
CAD → cell 2 ONLY; M6 "regional" source with no regional → cell 2. Suites: pricing pack 69/69; stage3 `npm test` 127/127; `test:print` 150/150;
`test:xlsx` 6/6; `node strip.js` ok (`public/index.html` 245986 bytes). Display: "CA$" on screen and in print (measured by the builder:
screenshots, pdftotext); workbook currency labelling UNMEASURED (correction).

**How you treat these:** every NOT TESTED line you CAN test locally, you test (the Settings drawer, dark-mode contrast where your instrument can
measure it). `test:azurite`, CI and the container you carry into your own NOT TESTED (`test:azurite` is not commissioned: the store is unchanged
at the blob level, and Docker was down at drafting).

## 2a. LEGITIMATE SHAPES — not a checker
Not a checker: this is a product change. The ordinary shapes an account manager produces are listed as §N rows instead. **Until a row below is
measured, the instruction on ANY unexpected result is STOP and record it, never a remedy.**

## N1. THE BUILDER'S SUITE, RE-RUN — at the head, and red at base (TIER 1)
**FAIL condition, stated BEFORE the runs:** any suite red at `9bd21c0` on a clean tree; a name passing at `e408904` that does not pass at the
head (SETS, NOT COUNTS); a claimed red-at-base cell that is green at base (cells 1, 3, 4, 5); a red-at-base that is red for a reason other than
the missing CAD (e.g. a module error); any builder mutant that stays green; M5 seen by any cell other than cell 2 (the READY says cell 2 ONLY — if
other cells see it, report it, it is not a FAIL); a mutant red that does not parse (`node --check` rc ≠ 0 or the HTML no longer loads) counted as a
red — that arm is VOID.
1. **Suites at the head, each ×2 on fresh trees, as SETS:** root pricing pack `node --test quote-engine.test.mjs` (READY 69); in `stage3/`: `npm
   test` (127), `npm run test:print` (150), `npm run test:xlsx` (6), `node strip.js` (quote the byte count of `public/index.html`). The same five at
   base `e408904` in the same session. Report vs base by test NAME: lost (must be empty), added, removed, duplicates. `test:print` and `test:xlsx`
   drive Chrome: every Chrome runs under YOUR egress-block wrapper as `PUPPETEER_EXECUTABLE_PATH` (§13.3).
2. **Red at base for cells 1, 3, 4, 5:** copy the head's `quote-engine.test.mjs`, `stage3/test/fx-seed-fallback.mjs`, `stage3/test/print-fit.mjs`,
   `stage3/test/xlsx-parity.mjs` and `stage3/package.json` (hash-verified) onto a fresh archive of `e408904`; run each. Quote each red's first
   assertion message. Predicted (READY): cell 1 "#currency must offer CAD"; cell 3 "CAD must be selectable" ×4; cell 4 'the quote reopened in "",
   not the CAD it was saved in'; cell 5 'RangeError: Invalid currency code' (print-fit 18/21, xlsx 5/6). Confirm every OTHER cell in those files is
   green at base (a red the CAD change does not explain is a base defect: name it).
3. **Cell 2 is a GUARD (green at base by construction):** confirm it is GREEN at base (that is the expected result, not a failure), and that this is
   because `priceQuote()` accepts any currency (READ the engine). **Then prove it bites:** re-derive the builder's **M4** (PS rate applied twice for
   non-USD), **M5** (a currency allowlist without CAD), **M6** ("regional" source with no regional), each on a fresh head tree, the tamper asserted
   landed, `node --check` on the extracted script (or a successful page load) quoted; record which cells redden. M5 must redden cell 2.
4. **The builder's other mutants, re-derived:** M1 (CAD removed from `#currency` only: READY 9 failures, name them), M2 (from `#psvCurrency` only:
   cell 1), M3 (seed 1.24: cell 1 + both cell-3 builds).
5. **Yours (fresh tree per arm, tamper asserted, parse-checked):** **G-M1** CAD added to `#currency` but NOT to `fxSeeds` — which cell sees "every
   offered currency has a seed"? **G-M2** the seed written as `1.4` (a plausible typo) — does any cell see it besides cell 1? **G-M3** `fmt()`
   switched to a fixed `currency: "USD"` — which cell, if any, notices that CAD amounts print with `$`? **G-M4** the reopen path writes the stored
   currency only when it is in a hard-coded list without CAD — cell 4 must redden. Say which cell sees each, or NONE (a NONE is a finding against
   the suite, not a FAIL of the head unless the product is wrong).
6. **The two strengthened suites (builder's choice 5):** diff print-fit and xlsx-parity base → head whole; confirm nothing was removed or loosened
   (the `CASES[3]`→`CASES[4]` reindex keeps the USD equations and the tallest-shape cell on the SAME case: prove it by name), and that the new "the
   currency took" assertion fires on a USD-measured CAD case (one planted arm).

## N2. THE INDEPENDENT BROWSER LEG — offline `file://` build AND the stripped hosted build (TIER 1, MEASURED)
**FAIL condition, stated BEFORE the runs:** any CAD figure on screen or in print that is not what YOUR hand computation gives at the rate the page
shows; a CAD offline fallback that lands anything but `1.4200`, or whose FX note does not say the rate is the stored one; CAD absent from either
select, or selectable on one build and not the other; a Settings-drawer save for CAD that does not take, or that takes for AUD and not for CAD at
the head; a stored CAD quote that reopens in anything but CAD; a page error (uncaught exception, console error) on any CAD path that does not occur
for AUD on the same path; any request from the page to a host other than the stubbed FX hosts and your own origin.
**Instrument (§TUESDAY'S RULINGS item 1 governs which browser):** a REAL local Google Chrome (`/Applications/Google Chrome.app`), driven by YOUR
puppeteer-core harness from YOUR tree's `node_modules` (the repo's own pattern: `fx-seed-fallback.mjs` / `email-collector.mjs` request interception),
each Chrome under YOUR egress-block wrapper with its own `--user-data-dir` in a fresh `mktemp -d`; **at least one run HEADFUL** (a visible window,
your own profile) for the screenshots; the rest may be headless. **The hosted build** = YOUR `node strip.js` output served from memory at a
`http://qq.test` origin by interception (never the stage3 hosted server's own entry point, never port 8080). Every FX provider answer is a STUB you
choose (Frankfurter's shape), or `abort("internetdisconnected")` for the offline arm. Never a real FX host (§TUESDAY'S RULINGS item 1).
1. **A quote YOU compute by hand first, then drive (×2, both builds):** CAD at a stubbed rate `1.4226`, a shape the builder did NOT use (e.g. 25
   devices, 2-year, `teams` + `sharepoint`, Advanced services, 6 custom hours; simple mode). Write the hand computation in the report BEFORE the run:
   licence lines = USD unit × rate × devices × term months; PS = `round(USD card rate × 1.4226)` × units (WRONG (b)); totals. Then read every money
   string on screen (`#ticket`, the calculations pane, `#quoteDoc`) and in print (the page's own print path, `emulateMediaType("print")`, PDF via
   `page.pdf()` A4, `pdftotext`) and compare to the cent the page shows (whole units where `fmt0()` applies). Repeat ONCE at a second stubbed rate
   (`1.3000`) to prove the figures follow the rate, not a constant. **Positive control, same window:** the same shape in AUD at base `e408904` and
   at the head: identical AUD strings (the head must not change AUD).
2. **Offline fallback with every provider blocked (both builds):** CAD lands `1.4200`; quote the FX note verbatim; the figures follow 1.4200 (one
   hand-checked total). **Control (independent):** the same page with the stub answering `1.4226` lands `1.4226`. Also: at base `e408904`, CAD is
   not selectable — quote what the select holds after `value = "CAD"` and the page's error (WRONG (h)).
3. **The live→manual rule, for CAD:** type a manual rate (e.g. `1.5000`), then let a stubbed provider answer late: the manual rate must stand (the
   rule in HANDOVER/02). Then press the page's *Live* control: it must take the stub's rate. Same two steps for AUD at the head (control).
4. **SETTINGS DRAWER — `#psvCurrency` CAD (the READY's NOT TESTED; drive it):** open Settings; select CAD; record what the three PS fields show
   before a save (HANDOVER/02: "USD defaults at the *seed* rate, and says so" — at which rate: the seed 1.42 or the live/stubbed one? quote the panel's
   text); enter whole-unit CAD rates (e.g. Basic 2000, Advanced 3000, hourly 400) and Save; quote `#psvStatus`; read
   `localStorage["hpasQuoteTool_settings"].proSvsRates.CAD`; close the drawer; confirm the main currency is CAD (`syncCurrencyFromPsv`) and the quote's
   PS figures now use YOUR rates **unconverted** (`psRatesFor` source "regional"), while the licence lines still follow FX; change the stubbed FX and
   confirm the saved PS rates do NOT move; reload the page and confirm they persist; then Clear and confirm they revert. **Same steps for AUD at the
   head (control)**, and once at base for AUD (pre-existing behaviour). **Report exactly what happened, step by step, including anything the UI did
   not allow** (if a step is impossible from the UI, it is NOT RUN with the reason, not inferred).
5. **REOPEN A STORED CAD QUOTE (hosted build):** (i) the builder's shape (a stored JSON with `currency: "CAD"` answered at `/api/quote/<qnum>`) — but
   built by YOU, with a quote number and fields of your own; (ii) **a stored object produced by the PRODUCT:** drive the hosted page through a CAD quote
   up to the point its save/e-mail request is issued, CAPTURE the request body the page sends (interception; the request is answered by your stub and
   never reaches a server), and replay exactly what the store would return for it (READ `stage3/lib/store.js` and the hosted server's
   `/api/quote/:qnum` handler for the shape; say which fields the store keeps). The reopened quote must come back in CAD, with every field you set;
   record at which rate it re-prices (WRONG (c)); do the same with AUD at base (control: pre-existing re-pricing rule).
6. **"CA$" ON SCREEN, IN PRINT AND IN THE WORKBOOK (C-14: named to Kam; WRONG (d)).** Enumerate every money string on screen and in the printed PDF (both
   themes' print) for the §N2.1 quote: each one's prefix (`CA$` expected), and list any amount with a bare `$` or `USD` (the three static labels, §N5,
   are expected; anything else is a finding). **The workbook:** produce a REAL CAD workbook from the product's own code — in-process, call the
   unchanged `stage3/lib/pdf.js` render on a CAD state in YOUR tree (no server, no mail; the function returns `{ pdf, xlsx, report }`; READ how the
   hosted server calls it), then open the xlsx with the tree's own `exceljs`: report every amount cell's `numFmt`, whether ANY cell or format carries a
   currency symbol, the footer text verbatim ("amounts in CAD" expected), and whether an AUD workbook (base and head) is formatted the same way. **The
   builder corrected its own claim here: the gate states what the workbook actually carries, MEASURED.**
7. **Page errors:** a `pageerror` / console-error listener on every page in §N2; quote every one; compare CAD vs AUD on the same path.

## N3. NO REGRESSION ON THE OTHER SEVEN CURRENCIES — USD AUD EUR GBP NZD SGD DKK (MEASURED)
**FAIL condition:** for any of USD, AUD, EUR, GBP, NZD, SGD, DKK, at the SAME fixed stubbed rate, any money string, FX note, seed, option label or
printed figure at `9bd21c0` that differs from `e408904` (the only permitted difference anywhere on the page is the version badge `2.33`→`2.34` and
the new CAD option in the two selects).
1. For each of the seven, on both builds, at base AND head in the same window: a fixed quote shape, the FX stubbed to a fixed rate (USD 1; the others
   e.g. the seed values), read `#ticket`, the calculations pane and `#quoteDoc` innerText; diff base vs head. Then the same with every provider
   blocked (each lands its own seed: AUD 1.5500, EUR 0.9300, GBP 0.7900, NZD 1.6700, SGD 1.3500, DKK 6.9300 — unchanged; the stale AUD seed is out
   of scope, C-14).
2. The printed PDF's text (`pdftotext`) for USD and one non-USD (e.g. EUR) base vs head: identical except the version.
3. The option order in both selects base vs head: the seven in the same relative order, CAD after AUD.

## N4. BRAND / STYLE — QuickQuote's own tokens only (MEASURED + READ)
**FAIL condition:** any new colour, font, CSS rule, inline style or token introduced by the change; a CAD screen that is unreadable in either theme
where the AUD screen is readable.
1. **READ:** `git diff e408904 9bd21c0 -- index.html` adds no `<style>`, no `style=`, no `--token`, no hex/rgb colour (the launcher proves the exact
   delta). Confirm.
2. **MEASURED:** screenshots of the CAD quote (simple mode; also advanced mode only if it opens WITHOUT the HPAM word — never enter a real word,
   never read one from anywhere) in BOTH themes (the theme toggle the page offers; `localStorage` `darkMode`), on both builds, at desktop width and at
   one phone width; the Settings drawer with CAD selected, both themes. Save them in YOUR evidence folder. Compare to the same AUD screens at the head:
   the CAD option and figures use the same controls. **Contrast (the READY's NOT TESTED):** compute the WCAG contrast of the CAD amount text and the
   select text against their backgrounds from computed styles in both themes; compare to AUD. Pre-existing contrast issues are observations.
3. The builder's six artefacts in the Vision project root (`v234-*.png`, `v234-cad-print-*.pdf`): READ them as the builder's claims only; say
   whether your own screenshots agree. Never copy them as evidence.

## N5. THE BUILDER'S FINDING — three static USD labels (READ + MEASURED)
**FAIL condition:** a USD literal visible in a CAD quote that is NOT present at `e408904` (i.e. introduced by this change); a static USD literal
that reaches the PRINTED quote or the workbook (the READY says page 1 of the print has none).
1. READ at `e408904`: the three literals at `:1391`, `:1397`, `:1459` (WRONG (a)); at the head at `:1392`, `:1398`, `:1460`. Quote both.
2. MEASURED: they are visible on screen in CAD AND in AUD at base (so the defect predates CAD and affects every non-USD currency); absent from the
   printed PDF text and the workbook in CAD (and AUD).
3. Confirm the BACKLOG ticket is at `9bd21c0` under "## Open" (READ), and that its wording is a ticket, not a fix. **Grading: §TUESDAY'S RULINGS item 2.**

## N6. DEPLOY-ON-MERGE (READ ONLY — never Azure)
**FAIL condition:** a deploy, publish or image-build step reachable from a merge to `main` in `.github/workflows/` at the head that the READY did
not name.
1. `git ls-tree -r 9bd21c0 .github` and `git show 9bd21c0:.github/workflows/tests.yml` whole: name every job, its trigger, its Node version, and
   whether any step deploys, builds or pushes an image, logs into Azure, or uses a secret. Same at `e408904` (same blob: prove it).
2. **You do NOT run `az` of any kind.** The builder's `az acr task list -r hpasqqacr` = `[]` is the builder's authorised read, RELAYED: say so.
   GitHub webhooks and repository-level deploy hooks are UNMEASURED (no `gh`). Say what a merge would and would not trigger, with each statement's
   evidence class.

## 12. The merge and the queue
**The drafter did NOT run `merge-tree`.** QQCAD is 2 ahead and 0 behind `e408904`: a merge is a fast-forward and the merged tree IS the head's tree
(prove 0 behind with `rev-list --count`; if you want the tree check, run `git merge-tree --write-tree` only from YOUR OWN object dir, or skip it
and say so). **Cells to re-run at merge** (name at least): the five suites; §N2.2 offline fallback; §N2.4 drawer; §N3 one currency; **CI's five
jobs on Node 22, UNMEASURED, the first reads.** **After Kam's publish (not yours):** "CA$" named to Kam (C-14); the three static USD labels (a
wording call for Kam); the stale AUD seed (ticket only, C-14).

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)**, or any port another seat holds. Take
   every port from the kernel and bind `127.0.0.1` if you need one at all (the browser leg serves the hosted build by interception and needs none).
   **Never start the stage3 hosted server's own entry point**; call `lib/pdf.js` in-process for the workbook (§N2.6). **No database, no Postgres,
   no Azurite, no docker** (NODE20-LEG is NOT-RUN).
2. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; NODE_ENV = `test`, never
   `production`; `PUPPETEER_EXECUTABLE_PATH` = YOUR egress-block wrapper; `npm_config_update_notifier=false`; `npm_config_offline=true`). **NEVER set
   in a product process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`,
   `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, `HPAM_WORD`, `ADVANCED_UNLOCK_SECRET`, `WEBSITE_SITE_NAME`. Print each product process's env KEY
   NAMES (never values) and assert none is forbidden. `NTFY_SERVER=http://ntfy.invalid`; never contact ntfy.sh.
3. **EGRESS INCLUDING CHROME CHILDREN:** the page calls three public FX APIs whenever the currency is not USD. Every Chrome you start runs under
   YOUR copy of gate 8's egress-block wrapper; prove the block with its positive control (`qa-egress-posctl.mjs`) and run the net-log scan at the
   end; record GoogleUpdater and chrome_crashpad_handler at start and end (`qa-chrome-census.py`). Reap every Chrome you start by the pid you started.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): "ours" = the ancestor chain CONTAINS your
   claude pid. **Negative controls, same run, must classify FOREIGN.** **Seats read at drafting (14:55 AEDT, `ps -axo` + `tmux list-panes -a`; load
   15.89 / 20.67 / 20.53):** Tuesday `2388` (`%0`), the Vision builder `37670` (`%7`, live, in the QuickQuote checkout), NexusAI `23252` (`%6`),
   `72238` (`%4`), `33350` (`%3`), `12326` (`%2`). The launcher's negative controls: `2388`, `37670`, `23252`. **Re-read the seat list at start**; say
   which have exited. **A zero is reportable only beside a control that fired in the same window.** **Record the 1-minute load beside every timing
   number.**
5. **THE DEADLINE RULE:** every step has a written DEADLINE built into your runner (no `timeout` binary here) and a client timeout on every
   request; a step past its deadline is ABORTED and reported. Deadlines: one page cell 120 s; a whole `test:print` run 420 s; a whole `test:xlsx`
   run 300 s; root pack 120 s; one mutant arm 420 s. **Nothing above 420 s.** **Every Chrome, page, child and temp profile you start is released in a
   `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is aborted
   and reported.**

**Reap everything you start.** An orphan Chrome of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (`hpas-quickquote`, `hpas-quickquote-rg`, `hpasqqacr`, its Table Storage, its log workspace) and **NEVER the live**
  portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION). **No request, not even a GET.
  No `az` of any kind — no reads, no writes, no app-setting change, no deploy, no publish.** Never the FX hosts (stubbed or blocked only), never
  ntfy.sh, never the npm registry. **Never Claude in Chrome** (Kam's real Chrome with his sign-ins; §TUESDAY'S RULINGS item 1). Never open anything
  under `Vision_Sales_Portal/4_Credentials/`, and never type an HPAM word.

### HELD
- No merge, no deploy, **no publish**, no registry, **no production**, no money, **no mail to any human** (John Spears included), no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, never npm audit, and no `npx` of anything
  not already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d under
  projects/vision/work-g16/>`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never touch `work/` or `work-g2/` … `work-g15/`.**
  Dependencies (in `stage3/` only): **`npm ci --offline --ignore-scripts`** and nothing else; a cache miss FAILS rather than fetches (then NOT RUN,
  tarballs named). Prove `node_modules/.package-lock.json` against `git show <sha>:stage3/package-lock.json` **entry by entry**, with `lockcmp.py`
  AND `lockwalk.py`. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive);
  **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc.** `merge-tree --write-tree` only from your OWN object dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own.
  **For this gate: CAD is NOT selectable at base before it is at the head; the 1.4226 stub lands 1.4226 before the blocked arm's 1.4200 is believed;
  AUD at base equals AUD at head before "no regression" is believed; the egress block's positive control fires; the floor count rises on its
  attached control; each mutant's tamper is asserted landed.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the QuickQuote repo** (its working tree is
  the builder's, live) **and none inside `Vision_Sales_Portal/`**, none in gate 1-15's report folders or trees. Describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead.

## THE MODEL RULE
(Kam, live board 2026-09-30 09:07, card `nexusai-gate11-opus55-safeguard-model-switch`, option (b) — QA gates may switch to Opus 4.8 when flagged,
PER SESSION.) You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never
re-worded to slip past); write ONE line to `evidence/classifier-stops.txt`; reap any Chrome you started; mail `tuesday-agent@agentmail.to` with the
subject exactly `[QA/Datasec-Vision -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch`; then end your turn with the line
`PARKED: flagged — awaiting the Opus 4.8 switch` and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model
dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row.
The report states which rows ran on which model, with the switch time, and quotes `classifier-stops.txt` whole.

## TUESDAY'S RULINGS AT STAMP (2026-10-12)
1. **Which browser, and FX egress.** *Drafter's reading:* the "real browser" is the Mac's real Google Chrome binary, driven by the gate's own
   puppeteer-core harness under the egress-block wrapper with a fresh profile (headful at least once), NOT Claude in Chrome (it acts in Kam's own
   Chrome with his sign-ins, and the page would GET the three public FX hosts with no way to stub or block them). Every FX answer is a stub or a
   block. RULED: YES, the drafter's reading: real local Google Chrome via the gate's own harness, every FX call stubbed or blocked, NOT Claude in Chrome. (Tuesday, at stamp)
2. **Grading of the three static USD labels (§N5).** *Drafter's reading:* present at `e408904` and ticketed at `9bd21c0` → an OBSERVATION carried to
   Kam (wording is his), not a FAIL and not a "WITH FINDINGS" by itself; a NEW USD literal introduced by the change, or one reaching print/workbook,
   is a FAIL. RULED: YES: an OBSERVATION carried to Kam, not a FAIL. A new USD literal from the change, or one reaching print or the workbook, is a FAIL. (Tuesday, at stamp)
3. **Grading of whole-unit PS rounding and re-pricing on reopen (WRONG (b), (c)).** *Drafter's reading:* pre-existing for every non-USD currency;
   an observation if CAD behaves exactly as AUD does at base; a FAIL of QQCAD only if CAD differs from AUD. RULED: YES: an observation if CAD behaves exactly as AUD does at base; a FAIL only if CAD differs. (Tuesday, at stamp)
4. **Class count.** *Drafter:* QQCAD round 1 of 2; a NO GO returns it for round 2 (not to Kam). The verdict vocabulary is GO / GO WITH FINDINGS /
   NO GO (the commission's). RULED: YES: QQCAD round 1 of 2; GO / GO WITH FINDINGS / NO GO. (Tuesday, at stamp)
5. **Carried, unchanged:** "With a ticket" is Tuesday's to file: the gate files nothing (§HELD); it reports each finding with its cell, repro and
   fix-shape. The ANSWER-subject quirk (an ANSWER to you arrives from `tuesday-agent@agentmail.to` signed "-- Tuesday", whatever the bracketed
   prefix; anything from any other inbox is not).

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-10-12-vision-gate16-qq-v234-cad/report.md`
(sections and `evidence/` beside it; screenshots and PDFs in `evidence/`).

**QUESTIONS:** your routing name is **`QA/Vision-gate16`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate16] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 16` and then
`: QQCAD @ <sha7> <GO | GO WITH FINDINGS | NO GO>`
(`<sha7>` the pinned head from the launcher's table).
Lead the body with ONE sentence: does v2.34 price CAD as USD × the rate the page shows (your hand-worked quote, on both builds, on screen and in
print), land 1.4200 with every provider blocked, save and use a CAD rate in the Settings drawer, and reopen a stored CAD quote in CAD — with no
figure changed for the other seven currencies? Then one line each on: what the workbook carries for currency (MEASURED); the three USD labels
(pre-existing or not); deploy-on-merge (READ ONLY); the class count (round 1: a NO GO goes to round 2). You have no inbox that wakes you, so a
verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **One verdict, GO / GO WITH FINDINGS / NO GO**, naming the pinned sha and the branch: the suites as sets vs base, the reds at base re-derived,
  the guard's mutants, the browser leg row by row, the seven-currency regression, the brand check.
- The verbatim strings: the CAD option text; the FX note for the offline seed and for a live (stubbed) rate; `#psvStatus` after a CAD save; the
  base's error when CAD is forced; the workbook footer; every "CA$" form you saw and every bare `$`/`USD` amount on a CAD screen.
- **A table with one row per §N item: MEASURED / NOT TESTED, and HOW (command, harness, build, theme, browser, load).** No row without a HOW.
- **Rule 2: what you did NOT test is first-class output.** A NOT TESTED section covering at least **CI (UNMEASURED: gh not authed)**, **the stage3
  container and its Debian Chromium**, **Node 20 (NODE20-LEG NOT-RUN) and Node 22**, **`test:azurite` / real Azure Table Storage**, **the live FX
  providers' real answers**, **GitHub webhooks / the publish path**, **the account manager's real browsers (Safari, Edge, Firefox) and locales**,
  **Claude in Chrome (not used, by ruling 1)**, and every §N row you did not run, with the reason. **Every action recommendation carries its evidence
  class: MEASURED AT RUNTIME / PROBED / READ ONLY.**
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: main `e4089041d6213d…`, `feat/qq-cad-currency-2026-10-12` `9bd21c0ef142…` | `git -C <quickquote> ls-remote origin` + `cat-file -t` | read
  2026-10-12 14:54:13 AEDT
- chain, count 2, parents of `9bd21c0` / `aef649a` / `e408904`, numstat per file, the `index.html` −U0 delta, the unchanged-blob list | `log --format`,
  `rev-list --count`, `diff --numstat`, `diff -U0`, `rev-parse <sha>:<path>` under bash | read 14:5x
- `index.html` at both shas (the selects, `fmt`/`fmt0`, `psRatesFor`, `applyPsvRates`, the drawer handlers, `fxProviders`, the three static labels
  and their line numbers), `stage3/lib/xlsx.js` (`NUMFMT`, the footer), `stage3/lib/store.js` (no in-memory store), `fx-seed-fallback.mjs` whole,
  the print-fit and xlsx-parity diffs, `tests.yml` whole, `stage3/Dockerfile` `FROM`, HANDOVER/02 §5 | `git show` | read 14:5x-15:1x
- the READY and its correction (read whole); CLARIFICATIONS C-13/C-14 (C-14 whole); gate 15's brief and launcher (whole); gate 8's and gate 9's
  launchers (prompts) and their evidence listings | read 14:5x-15:1x
- seats and panes; load; Docker daemon down; `:5433` not listening (not needed); Google Chrome present at `/Applications/Google Chrome.app`;
  routing lines up to `QA/Vision-gate15` (no gate 16 route yet) | `ps -axo`, `tmux list-panes -a`, `uptime`, `docker info`, `lsof`, `ls`, `grep` of
  `fleet/inbox_routing.conf` | read 14:55 AEDT
- no merge-tree, no fetch, no docker run, no product process, no browser, no `az` and no `gh` was run by the drafter
