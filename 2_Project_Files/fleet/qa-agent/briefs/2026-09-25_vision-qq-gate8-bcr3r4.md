# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 8 (QuickQuote only), ONE TARGET, NARROW: BCR3R4 = bounded browser.close() ROUND 4 of the BC class (the close bound 30,000 → 90,000 ms), TIER 2 with TIER-1 rigour on `lib/pdf.js`

**Drafted for Tuesday on 2026-09-25 at 13:1x AEST by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
It was commissioned on Tuesday's ruling of 2026-09-23 09:45 AEST (`0_Brain/daily_tuesday/2026-09-23.md`, the GATE 7 VERDICT line:
*"BCR3 round 4 is ONE NUMBER … gated NARROWLY … rather than a full round, because this gate already proved the 90 s arm at the same
load"*) and on the OWED line in `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:58`. **The drafter did NOT read any builder mail.** Every builder
claim below comes from the commit message of `703d304`, the BACKLOG, Tuesday's notes or gate 7's report, and every one of them is a **CLAIM**.
**The drafter read both rows from `git ls-remote origin` on 2026-09-25 at 13:09 AEST (`cat-file -t` = commit). The launcher reads them
again.** It parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build this change and you owe the builder nothing. **Every line below that reports what a builder says is a
CLAIM, never evidence.**

**One gate, one target, one repo (QuickQuote), one verdict: GO / NO-GO for BCR3R4 at its pinned sha.** The portal is NOT in this gate.

**⚠ Names, written out every time:** **BCR3R4 = ROUND 4 of the BC class** (gate 4 N-C1 → gate 5 target BC → gate 6 target BCR2 →
gate 7 target BCR3 → **this**). Tuesday's notes call it "BCR3 round 4"; the builder's commit calls it "BC round 4"; all three names mean
the one commit `703d304` on `fix/qq-bounded-browser-close-2026-09-23`. **It is NOT on QuickQuote main.** Its reason for existing is
gate 7's **BCR3-F1 (Major)**: under 8 CPU-bound workers on this 8-core box, the 30,000 ms bound killed a HEALTHY Chrome 3 of 3
(30,613 / 30,652 / 30,846 ms).

**TIER:** **BCR3R4 (bounded browser.close() round 4) is TIER 2, through-code, WITH ONE DECLARED TIER-1 TOUCH** — the shipped
`stage3/lib/pdf.js` `closeBrowser()` default moves 30,000 → 90,000 ms. Every clause that proves production is untouched is **TIER 1 in
rigour**, and you re-establish it at this sha rather than carrying it forward from gate 7.

## THIS IS A NARROW GATE — what that means, and where the pattern comes from
**The pattern is a NARROW re-gate:** re-measure ONLY what the round changed and the cells that decide the finding it answers, plus the
full suites at the new sha. **Do NOT re-run a full round.** The narrow-gate model is **gate 5 §B**, and the commission located it
wrongly. It is **NOT** in the Vision gate-5 report, whose targets were A9, CF5R2, IO1 and BC and which has no §B. It is in the
**NexusAI** gate-5 report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/report.md`,
target B, line 49: *"A narrow re-gate suffices: that ordered pair, the rd616 file, and a full verify."* That line lives in the same
client's own QA tree (Datasec), so you may read it. Read it for its SHAPE only. Its facts belong to NexusAI and are not facts about Vision.

**IN SCOPE, and nothing else (the commission's four items, with the two additions the record forces):**
1. **BC-F2 under load**: the cell that failed in gate 7, run under the same load gate 7 used, **N ≥ 3**, at 90,000 ms. See §N.3.
2. **The nine forced-hang files still exit**: the bound still fires on a close that genuinely hangs. See §N.4.
3. **`test:print` completes and exits with all EIGHT files / 143 cells.** See §N.2.
4. **The `lib/pdf.js` tier-1 clauses, re-established**: the renderer is byte-unchanged, production makes 0 calls to `closeBrowser`, and
   the emailed PDF shows 0 differing pixels against main. See §N.5.
5. **The BCR2-O1 retraction, confirmed ONCE at 90,000 ms**: the logged close time tracks the bound. See §N.6.
6. **Added by the drafter from gate 7's own evidence: every kill at 90,000 ms is DISCRIMINATED** as a hang or a slow healthy close.
   See §N.3(c). Without this, a green BC-F2 does not answer BCR3-F1's class.

**NOT IN SCOPE (do not re-open, do not re-measure beyond what the list above needs):** the stdio-release fix (BC-F1, gated at gate 6);
the NaN coercion (BC-F2's original gate-5 defect); `logo-inset`'s `closeBounded` (gated at gate 7); the `QA_CLOSE_MS` fallback (gated
at gate 7); the phone-layout contradiction, **except** the single 90 s tracking confirmation in item 5; **BCR2-F1** (Minor, ticketed,
carried: the stdio-destroy loop has no reddening cell. Report it as unchanged if you touch it, and do not fail on it); BCR3-P1/P2/P3
(Polish from gate 7: say whether round 4 fixed each one, READ ONLY, and do not fail on them); every IO1F1 / portal item. **The BC round cap
is not re-opened** (see THE CAP).

## THE CAP — C-62, and the question the drafter could not close
Kam's cap rule, recorded verbatim as **C-62** in the NexusAI clarifications
(`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:573`):
*"A Major at round 2 of 2 is ticketed, not sent to Kam. Only a third round on the same class needs his word."*
- **Tuesday's ruling (2026-09-23 06:34 AEST, at gate 7): THE CAP IS NOT SPENT by round 3.** Its reason: BCR2 was GO at its pinned sha,
  so round 3 was a pre-merge improvement and not a remediation forced by a NO-GO.
- **Tuesday's ruling for THIS round (2026-09-23 09:45 AEST):** gate round 4 NARROWLY. The pickup adds *"It does NOT reopen the BC
  cap."*
- **Gate 7 said the opposite, in writing** (`…/2026-09-23-vision-qq-gate7/report.md:123`): *"A further round on the BC class would be a
  FOURTH round, and under C-62 that needs Kam's word."* **Round 4 IS a remediation forced by a NO-GO** (gate 7's BCR3-F1, Major).
  **The drafter found no record of Kam's word on round 4** in Tuesday's daily notes for 09-23, 09-24 and 09-25, or in the pickup.
- **So: THE CAP IS NOT SPENT is TUESDAY'S ruling, not Kam's.** Say that in your report, quote gate 7's line beside it, and do **not**
  rule on it yourself: the priority call belongs to the humans. **If you grade NO-GO**, say plainly, part by part, what CLOSED and would
  ship and what is TICKETED, and say that **a third round on that class** (counted however Tuesday counts it) needs Kam's word under C-62.
  **Do not recommend a round 5.**

## RULED BY KAM, AND SETTLED (Vision `1_Project_Definition/CLARIFICATIONS.md`)
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` — read it whole. **C-01..C-05,
unchanged since gate 4 (file dated 2026-09-22 18:26). No C-entry covers this target.** Its authority is gate 7's finding and Tuesday's
rulings.
- **TUESDAY'S STANDING RULINGS THAT ARE GATE CLAUSES HERE (carried from gate 7; marked text verbatim):**
  1. **The bound is a HANG GUARD, not a latency assertion. A false kill is worse than a slow test.**
  2. **Production never calls `closeBrowser`: re-establish it, do not re-assert it.** Gate 7's firing-spy result at `58c9094` was
     `{"closeBrowser":0,"cdpClose":0,"disconnect":0,"childKill":0}`, with two real PDFs emailed and the spy proven able to fire in the
     same run. **Reproduce that at THIS sha.**
  3. **The round is ONE NUMBER** (30,000 → 90,000 ms in all FOUR occurrences), gated narrowly (09-23 09:45).
- **No product choice here is Kam's ruling.** Report each one as the BUILDER's choice and say whether it needs Kam: the **90,000 ms**
  default in a **shipped** module (claimed headroom *"1.4× the slowest healthy close gate 7 measured"*); keeping the bound as elapsed time
  instead of gate 7's fix-shape (i) "no progress", (ii) load-aware or (iii) "let the cell decide"; and leaving `toolVersion` at 2.33.
- **Kam's pending decisions that bound this gate** (`Vision_Sales_Portal/5_Project_History/2026-09-22_kam-decisions-and-publish-pack.md`,
  READ ONLY): decision 14 (P5B) still holds. Decision 18 (QuickQuote's production logs): **never query any production log.**
- The QuickQuote repo's own rules: `Quoting Tool/hpas-quoting-tool/CLAUDE.md`. Read it (it covers version discipline and says to
  **always verify print as a real PDF**). **`toolVersion` is `2.33` at BOTH main `d4426f8` and `703d304`, and `index.html` is the SAME
  BLOB (`e90250f`)**, READ-verified by the drafter. Say whether that is within the rule. Gate 7 ruled it within the rule for round 3 by
  the same reasoning.
- **Live QuickQuote is v2.33 (main `d4426f8`), published on 2026-09-23 on Kam's delegated GO.** The source is READ from Tuesday's daily
  note 2026-09-23 (the 12:19 entry and the WENT WELL line). The drafter did NOT verify the live site (that needs `az`, and production is
  never touched). **The gate-7 brief's "live QuickQuote is v2.30" is STALE.** This round does not go on main until this gate passes.
  **Deploys are HELD for Kam. Nothing merges on your word.**

## PRIOR ROUND
PRIOR ROUND: round 3 (gate 7) gated `58c9094834ec98bb66c2a28a24f482000bb216ba`, verdict **NO-GO** on one stated FAIL condition,
**BCR3-F1 (Major)**, with everything else CLOSED.
**ITS REPORT IS ON DISK AT:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-23-vision-qq-gate7`
(`report.md`, `sections/BCR3.md`, `sections/CONVENTIONS.md`, `evidence/`). **Read its VERDICTS, its FINDINGS INDEX, its NOT TESTED,
all of `sections/BCR3.md` and `sections/CONVENTIONS.md`.** Gate 6 (`…/2026-09-23-vision-qq-gate6/`) and gate 5
(`…/2026-09-23-vision-qq-gate5/`, the source for BC-F1's socket-peer root cause) sit one and two levels back.
Findings carried forward and their disposition:
- **BCR3-F1 (Major):** what round 4 claims to answer. **That claim is what this gate decides.**
- **BCR2-O1 (gate 6 observation):** RETRACTED. The logged close time **tracks the bound**. At gate 7, the same instrument on the same
  file logged **5,018 ms at a 5,000 ms bound, 30,017 at 30,000 and 90,024 at 90,000**, and the SIGKILL line came **16 ms BEFORE** the
  "returned" line. Gate 6 was logging its own SIGKILL as "the close returned". **Gate 7 said it "should be retracted"; Tuesday recorded
  it RETRACTED (daily note 09-23 09:45); the builder recorded it RETRACTED in `BACKLOG.md` at `703d304`.** Gate 6's own report is
  unamended, which is correct: it is not the builder's to edit. **Do not re-derive the "thin margin" story.** Confirm the tracking
  ONCE at 90,000 ms (§N.6).
- **BCR2-F1 (Minor), carried, unchanged:** ticketed. **Do not fail on it.**
- **BCR3-P1 / P2 / P3 (Polish):** P1 (a shipped comment of "≤ 1.7 s") is claimed fixed by the new comment. P2 (the "one number" cell is a
  regex) is unchanged by design. P3 (the BACKLOG not saying "inside `test:print`") is claimed addressed by the new BACKLOG line. **Check
  each one (READ ONLY) and do not fail on any of them.**
- **PRIOR WORK: verify every claim above against history and gate 7's evidence, never against this brief:** use `git log` / `git show`
  for `58c9094` and `703d304`; gate 7's `evidence/bc/disc-b.txt` and `disc-b.qalog` (the 90 s arm); `evidence/bc/loaded.txt` and
  `loaded-boundary.txt` (the red arms); and `sections/BCR3.md` §2, §3 and §4. **Where this brief's account of prior work disagrees
  with the record, the record wins. Report the disagreement as a brief correction.**
- **Gate 7's harnesses can be REUSED BY COPY.** From `…/2026-09-23-vision-qq-gate7/evidence/`: `qa-run.py`, `qa-chrome-egressblock.sh`,
  `qa-chrome-lock.py` (the gate's OWN fcntl Chrome lock), `qa-egress-monitor.py`, `qa-egress-posctl.mjs`, `qa-netlog-scan.py`,
  `qa-floorcount.py`, `qa-harness-floorctl.mjs`, `lockcmp.py`, `lockwalk.py`, `mktree-qq.sh`, `qa-cpuload.mjs` (the 8-worker load),
  `bc-loadedrun.sh`, `bc-loadedN.sh`, `bc-printrun.sh`, `bc-hangrun.sh`, `bc-observe.sh`, `qa-bc-preload.mjs` (the close/kill logger),
  `qa-bcf2-discriminate.mjs`, `qa-harness-bc-emailed.cjs`, `qa-lib-bc-stage3.cjs`, `qa-lib-bc-png.cjs`, `BC-pdfcompare.sh`,
  `qa-bc-identity-g7.py`, `BC-diag2.sh`. **COPY what you use into this gate's own evidence folder, read it before you trust it, and never
  edit gate 1-7's copies.** Known defects in those copies that you MUST fix in YOUR copy (each with an asserting edit):
  (i) `bc-loadedrun.sh` gives the load **170 s** and the run a **150 s** deadline. At a 90 s bound the loaded run takes longer than that
  (gate 7's 90 s arm ran **188.2 s**), so the load would stop mid-run and the deadline would abort a healthy run. The load must outlast
  your deadline. (ii) `bc-loadedrun.sh` reaps with **`pkill -f qa-cpuload.mjs`**, which kills ANY process whose argv mentions that
  name, including another gate's loader. **Reap by the pid you started, never by pattern.** (iii) Every `150` deadline in the copied
  runners is wrong for this round (§13.5).
- **Self-findings from gates 2-7 bind you:** (1) quote every path, because the project path has a space; (2) **zsh does not word-split
  `set -- $p`, and it reads `$s:stage3/…` as a history modifier. Run every such loop, and every `git show <sha>:<path>`, under `bash`**;
  (3) never detach a control server; (4) npm's update-notifier egresses unless you disable it; (5) isolate a browser context per case,
  and remember puppeteer's default PDF is Letter, so pass `format: "A4"`; (6) the real renderer calls public FX APIs whenever
  currency ≠ USD, so BLOCK and RECORD them (§13.3); (7) **run `node strip.js` before any lone browser file**, which is gate 7's
  self-finding 3 (a phone-layout batch without it was VOID); (8) **the floor is SHARED, and Spotlight indexing your own fresh
  `node_modules` holds the 1-minute load at 12-29.** Record the load average beside every timing number. **A latency result with no
  load figure is not a measurement**; (9) a red arm on a file that ALREADY hangs cannot discriminate.

## PIN — HEADS (PRE-FILLED BY THE DRAFTER; RE-CHECKED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head; the target row has a 40-hex base, a commit count and no `@`; the head is a
commit in the repo; the base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals the head NOW. The base is the MAIN row's head; if it is a stale base instead, the launcher prints a NOTE.
**The target is NOT on main and is NOT stale:** `merge-base(703d304, d4426f8) = d4426f8`, and it is **6 ahead / 0 behind** main
(`git rev-list --left-right --count d4426f8...703d304` = `0 6`, READ at 13:09 AEST). **Gated anchors (the launcher checks them):**
`703d304`'s ONLY parent is gate 7's gated head `58c9094`; it contains gate 6's gated head `f8dec9c` and the forward merge `983f916`,
whose parents are exactly `f8dec9c` + `d4426f8`.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-Q | quickquote | main | d4426f899620419819ae755ff0ddba4f2a9843b7 | - | - | IN |
| BCR3R4 | quickquote | fix/qq-bounded-browser-close-2026-09-23 | 703d304d859c9138f15fa58d866a5d29e504b864 | d4426f899620419819ae755ff0ddba4f2a9843b7 | 6 | IN |
<!-- PIN-HEADS:END -->

Repo: QuickQuote = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool`
(remote `datasecau/vision_hpas-quickquote`).

**The shape at drafting (READ, 13:09-13:2x AEST):** six commits over main: `907f686` → `aa89010` (gate 5's round 1) → `f8dec9c`
(gate 6's round 2, GO) → `983f916` (the forward merge of main `d4426f8`) → `58c9094` (gate 7's round 3, NO-GO) → **`703d304` (round 4,
authored 2026-09-23 09:52:40 +1000)**. **Round 4's own commit touches exactly four files:** `BACKLOG.md`, `stage3/lib/pdf.js`,
`stage3/test/lib-close.mjs` and `stage3/test/lib-close.test.mjs`. **Over main, the branch still touches the same 15 files gate 7
pinned.** **A GO is a statement about the pinned SHA only.** If the head moves, the verdict expires.

## WRONG OR UNVERIFIABLE IN THE COMMISSION — corrected AT SOURCE by the drafter (verify each; the commission is a claim like any other)
- **(a) "expecting 0 browser kills at the 90,000 bound" is WRONG as written, and gate 7's own evidence refutes it.** In gate 7's
  90 s arm (`evidence/bc/disc-b.qalog`, 8 CPU-bound workers, N = 1), **FIVE Chromes were SIGKILLed AT the 90 s bound**: `fx-provenance`
  90,038 ms, `print-fit` 90,026, `logo-inset` 90,022, `typed-rates` 90,037 and `phone-layout` 90,024. The builder's own idle claim
  says *"phone-layout pays the 90 s bound once"* per `test:print`. **The correct expectation is: 0 kills of a HEALTHY Chrome.** BC-F2
  must be green, and every kill that does happen must be attributed to a close that is PROVEN not to return. Gate 7 described those
  five as "the files that genuinely hang" **but never measured that claim**. No arm lifted the bound above 90 s for them, so a slow
  healthy close at, say, 100 s would look identical. **That is §N.3(c), and it is this gate's sharpest question.**
- **(b) "8 CPU-bound concurrent PRINT workers" misdescribes the shape.** Gate 7's loaded arm ran **8 CPU-bound worker THREADS**
  (`qa-cpuload.mjs 8 <secs>`, a pure `Math.sqrt` spin) **beside ONE `npm run test:print`**, not 8 concurrent print runs. Reproduce
  gate 7's shape. If you ALSO run concurrent print runs, label that a separate arm.
- **(c) "90 s passed that arm AT THE SAME LOAD" (the builder's commit, relayed) is not quite what the record shows.** It had the same
  WORKER COUNT, but not the same load average. The 30 s reds ran at a 1-minute load of **24.88→96.53, 96.59→120.65 and 119.29→141.45**.
  The 90 s arm (`disc-b.txt`) ran at **36.89→60.17**, and it ran **once**. Its slowest healthy close was **62,260 ms at load ≈ 60**.
  At load 96-141 the same close may pass 90 s. **Reproduce the RED BAND's load, not just the worker count** (§N.3).
- **(d) "RETRACTS gate 6's BCR2-O1":** gate 7 *recommended* the retraction (*"should be retracted"*). **The retraction was made by
  Tuesday** (09-23 09:45) and recorded by the builder in `BACKLOG.md` at `703d304`. The substance is right; this brief states who retracted.
- **(e) "PDF output byte-identical vs main" is too strong, and no gate has ever measured it.** Gate 5, 6 and 7's clause was: pages
  equal, `pdftotext` equal, **0 differing pixels**, and differing bytes **only inside `/CreationDate` and `/ModDate`** (4 bytes).
  The byte-identity clause belongs to the **renderer SOURCE** (`renderQuotePdf`, `browser()`, the launch, `svcInject()`,
  `module.exports`, and the whole file minus `closeBrowser`), not to the PDF.
- **(f) "It does NOT reopen the BC CONCURRENCY cap":** no "concurrency cap" exists at source (grep of gate 7's brief and report, the
  pickup, today's note, and `stage3/package.json` / `stage3/test` / `BACKLOG.md` at `703d304`: 0 hits). The pickup's words are *"It
  does NOT reopen the BC cap"*, meaning **C-62's round cap**, and that point is contested (THE CAP, above).
- **(g) "root 353" (relayed from the Vision seat) is UNVERIFIABLE at source and disagrees with gate 7.** No `package.json` exists at the
  repo root. CI runs **`node --test quote-engine.test.mjs`** (`.github/workflows/tests.yml`), and gate 7 counted that at **67/67**
  (`quote-engine.test.mjs` has 67 `test(` calls at `703d304`, unchanged vs main). 353 is most likely a **bare `node --test`** at the root,
  which recurses into `stage3/test/**`. CI's own comment says it does not use that form. It double-counts the unit and print files and
  runs every Chrome file at once. **Name the exact command beside every count you report.** Print 143, unit 124 and xlsx 5 match
  gate 7's counts at `58c9094` (round 4 adds no cell).
- **(h) "gate-5 §B pattern ... under Vision reports/": wrong location.** It is in the NexusAI gate-5 report (see the NARROW GATE section).
- **(i) "QQ main = d4426f8 (LIVE v2.33)":** the main half is VERIFIED (`ls-remote` 13:09). The LIVE half is READ from Tuesday's daily
  note only. Nothing in this gate may verify it (no `az`, no production).
- **Verified TRUE at source (READ):** the only product change is `stage3/lib/pdf.js` `closeBrowser`'s bound. **The bound appears in
  exactly four code places:** `stage3/lib/pdf.js:208` (`closeBrowser(ms = 90000)`) and `:212` (the NaN fallback), and
  `stage3/test/lib-close.mjs:21` and `:26`. `stage3/test/lib-close.test.mjs:132` asserts `[90000, 90000, 90000, 90000]`. Replacing
  `90000` with `30000` in the head's three files reproduces `58c9094`'s code exactly (comment lines aside). `page.goto`'s `30000` at
  `lib/pdf.js:60` is unrelated and unchanged. The branch is 6 ahead / 0 behind main. The stage3 lockfile blob `70ebda7` is equal at
  main and head. `closeBrowser` is referenced only by `lib/pdf.js` and five test files. The only production importer is
  `stage3/server.js:890`, `const { renderQuotePdf } = require("./lib/pdf");`.
- **Gate 7's report contradicts itself on one point (for you to settle, not to relay):** its §4 observe run says gate 6's
  phone-layout SIGKILL is **ABSENT** at BCR3, while its §3 table shows a BCR3 phone-layout SIGKILL at **30,017 ms**. Both can be true
  in different runs if the in-`test:print` hang is INTERMITTENT (main hung 2 of 3 and exited 1 of 3). **Count phone-layout's kills per
  run across your N runs and report the rate.** Do not report "it hangs" or "it does not hang".

## 1. Target — READ from the object store at drafting
**The round-4 delta over `58c9094`**, all of which the launcher proves:
- **`stage3/lib/pdf.js`**: `closeBrowser(ms = 30000)` becomes `closeBrowser(ms = 90000)`, and the fallback `: 30000` becomes `: 90000`.
  The comment above `closeBrowser` now reads *"gate 7 measured healthy closes of 58-62 s with 8 CPU-bound workers on 8 cores … (BC round
  4)"*. **Nothing outside that comment and the function changes** (the launcher hashes the file with the block removed at main, `58c9094`
  and `703d304`).
- **`stage3/test/lib-close.mjs`**: `closeBounded(browser, ms = 30000)` becomes `90000`, the fallback moves with it, and the measurement
  comment is rewritten (BCR3-P1).
- **`stage3/test/lib-close.test.mjs`**: the "one number" cell expects `[90000 ×4]`. **No new cell.** The 6 s healthy-close cell is
  unchanged: it now tests a 6 s stub against a 90 s default.
- **`BACKLOG.md`**: a Round 4 line, the BCR2-O1 RETRACTED line, and *"Load is an uncontrolled variable for every Chrome-timing cell
  (Vision has no jest lock) … Fleet-level fix owned by Tuesday."* That last item is Tuesday's fleet work, not this gate's.
- **Builder's self-check (CLAIM, from the commit message, load average 2.5-3.9):** the one-number cell 1/1; `test:print` 143/143, all 8
  files, **exiting on its own in 113 s (phone-layout pays the 90 s bound once)**; BC-F2 1/1 under 8 busy workers with no kill, *"a 5 s
  run, load only reached 10: not the gate's contention"*. **By the builder's own admission its loaded check did not reproduce gate 7's
  contention.**

**No worktree is pinned. Build your own trees INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store:**
`git -C <repo> archive <pinned sha> | tar -x -C <a fresh mktemp -d under your project>`. **Never run `git worktree add`, `checkout`,
`switch`, `fetch`, `pull`, `stash`, `reset`, `restore`, `clean`, `gc` or `tag` against the repo, never commit to it, and never work
inside its checkout.** In the repo, use only the read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base,
archive). **Dependencies, without the network:** in YOUR archived `stage3/`, run **`npm ci --offline --ignore-scripts`** and nothing
else. A cache miss FAILS rather than fetches; the suite is then **NOT RUN, with the blocker named** (name the missing tarballs). Never
`npm install`, never `npx` a package that is not already in the tree, and never npm audit (it is a registry call). Then prove
`node_modules/.package-lock.json` matches `git show <sha>:stage3/package-lock.json` **entry by entry**, with `lockcmp.py` AND
`lockwalk.py`, and quote the count (gate 7: 282/282). **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** Use a fresh
`mktemp -d` per arm under **`work-g8/`**, never reuse a mutant tree for a clean arm, and never touch `work/` or `work-g2/` … `work-g7/`.
**A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES:** run `node --check` on every mutated `.js`/`.mjs`, and quote the exit code. A red
from a mutant that does not parse or load is a VOID arm, never a red. **Assert every tamper landed** (grep the literal count) before you
read any result. **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the
other way on its own. **`git merge-tree --write-tree` writes objects.** Run it only as
`GIT_OBJECT_DIRECTORY=<your own mktemp -d> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree
--name-only <a> <b>`, **from the gate's OWN object dirs**, or SKIP it and say so.

## 2. Why this is narrow, and who is waiting
- Gate 7 already measured everything round 4 does not touch. Round 4 changes four literals and two comments. **A full round would spend
  a session re-proving gate 7's CLOSED list.** What gate 7 did NOT settle is whether **90 s** stops the false kill at the load that
  produced it. It measured one run, at a lower load than the reds.
- 🔴 **Queue:** QuickQuote main `d4426f8` (**live v2.33**) still carries gate 4's N-C1 intermittent `test:print` hang (main hung 2 of 3 at
  gate 7). BCR3R4 is what removes it. **It goes on main only on a GO here and Tuesday's merge.**
- **The cost this round adds, which you must measure and state:** at 90 s, every hung close costs **90 s per file instead of 30**. With nine
  files, a fully hanging CI run could take up to **13.5 minutes** longer. **Every ordinary `test:print` in which phone-layout's close
  hangs now takes ~90 s longer** (the builder's 113 s run). That is a developer-visible slowdown on the green path, not only on a
  failure path.

## 2a. LEGITIMATE SHAPES — the bound is a GUARD whose failure path is DESTRUCTIVE (a SIGKILL), so a false alarm is damage (template §2a)
Measure every row. **A row whose expected verdict and clause disagree is a finding against this brief. Say so.**

| shape — its ordinary form, as a developer or CI really produces it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| A developer runs `npm run test:print` on an idle Mac with the installed Chrome | completes and **exits on its own**, 143/143, eight files; **phone-layout's close MAY be killed at 90 s (intermittent)**; no other kill outside the lib-close cells' deliberate stubs | the bound + the stdio release | builder (113 s) — **measure N ≥ 3, and count and attribute every kill** |
| A `test:print` run beside 8 CPU-bound workers at the **red band's load** (1-min ≥ ~96) | **BC-F2 green: 0 kills of a HEALTHY Chrome**, N ≥ 3 | 30,000 → 90,000 ms | gate 7 (N = 1, at load ≈ 60) — **the shape round 4 exists for; reproduce the LOAD** |
| The same loaded run, where OTHER files' closes are killed at 90 s | each such kill is a close that **would never have returned** | the hang guard | gate 7 asserted it, **never measured it** — **discriminate (§N.3(c)); a kill of a close that WOULD have returned is BCR3-F1 recurring** |
| A real Chrome whose `close()` genuinely hangs (stubbed, or SIGSTOP on your own browser) | each of the **nine** files exits within 90 s + margin, killing only its own browser | the hang guard | gate 7 (9/9 at 30 s) — **re-measure at 90 s** |
| Production renders and emails a quote PDF | `closeBrowser` is **never called**; the PDF shows 0 differing pixels vs main | production imports `renderQuotePdf` only | gate 7 — **RE-ESTABLISH at this sha with a spy proven able to fire** |
| CI (ubuntu, `/usr/bin/google-chrome`, node 22) runs `test:print` | NOT RUN here | — | **NOT TESTED; name it** |

## N. TARGET BCR3R4 — the narrow measurements (FAIL conditions stated before the runs, per Rule 1)
**FAIL condition, stated BEFORE the runs:** **a healthy Chrome killed at the red band's load** (BC-F2 red, or ANY kill at 90 s of a
close proven to return on its own when the bound is lifted); `test:print` failing to complete and exit on its own, or completing with fewer
than **143 cells / eight files**; a forced-hang file that does not exit; any byte of `lib/pdf.js` outside `closeBrowser` + its comment
changed; any production path reaching `closeBrowser`; the emailed PDF differing from main's in text or by one pixel (timestamp bytes
excepted); a kill that reaches a process the test did not start.

1. **Scope (READ).** `git diff --stat 58c9094 703d304` (**4 files**) and `git diff --stat d4426f8 703d304` (**15 files**). **Quote the
   whole `closeBrowser` diff over MAIN.** Prove the four literals, and prove no fifth default exists: `git grep` at the ref for
   `90000` / `30000` under `stage3` (not `node_modules`), and classify every hit. Gate 7's BCR3-P2 caller
   `test/lib-close-shared.test.mjs:33` `closeBrowser(1000)` still passes an explicit bound. Say so.
2. **`test:print` COMPLETES AND EXITS (MEASURED), eight files / 143 cells.** Plain `npm run test:print`, no preload, each run ALONE
   under your own exclusive Chrome lock, timed, **N ≥ 3 at `703d304`**, with a written deadline (§13.5). Quote the elapsed time, the
   **load average before → after**, the cell count and the rc for every run. **Count and attribute every kill** (use `qa-bc-preload.mjs`
   observe mode in a SEPARATE run, so the plain runs stay plain), and report **phone-layout's kill rate** over your runs. Control, same
   session: **main `d4426f8`**, N ≥ 3. It is expected to hang in some runs (gate 7: 2 of 3), and it can come out the other way, which is
   why it is a control.
3. **BC-F2 UNDER THE RED BAND'S LOAD — THE HEADLINE (MEASURED).**
   (a) **At `703d304`, `test:print` beside 8 CPU-bound workers (`qa-cpuload.mjs 8 <secs ≥ your deadline>`), N ≥ 3.** Record the 1-minute
   load at start, at BC-F2's close and at the end. **Reach the red band (1-min ≥ ~96, as gate 7's reds did) on at least two of the three
   runs.** If this box cannot reach it with 8 workers, say so, give the load you reached, and add workers until you can, labelling the
   worker count. **Do not report a green below the red band as an answer to BCR3-F1.**
   (b) **The positive control that CAN redden, in the SAME window:** the **`58c9094` tree unmodified** (its 30 s bound is the gated round
   3), run the same way. It is expected to redden BC-F2 as gate 7 measured (30,6xx ms). **If `58c9094` does NOT redden at your load, your
   load is not the red band, and (a)'s green proves nothing.** Say so.
   (c) **THE DISCRIMINATOR (drafter's addition, from correction (a)).** For **every** Chrome killed at 90 s in (a), establish whether its
   close would have returned. In a fresh mutant tree off `703d304`, lift the bound to **240,000 ms in all four places** (`node --check`
   both modules; grep-prove the tamper; expect the "one number" cell red and nothing else from the tamper). Run it under the same load
   with the close logger, and record each file's real close time. **A close that returns between 90 s and 240 s is a healthy close that
   90 s would have killed: BCR3-F1 recurring. Name the file, its time and the load.** A close still pending at 240 s is a hang. Also run
   `BC-diag2.sh` (gate 5's socket-peer attribution) on one killed file to name WHAT holds it: the stdio pipe peered with
   `chrome_crashpad_handler` (BC-F1's mechanism), or something else.
   (d) **Headroom, stated as numbers:** the slowest healthy close you measured, the load it was measured at, and the ratio of 90,000 to
   it. The builder claims 1.4× (62.3 s). **Say whether a bound sized from one load is a hang guard at a higher one.** Gate 7's own
   sentence was *"A bound sized as a multiple of a lightly-loaded measurement cannot be a hang guard on a heavily-loaded one."*
   Whether 90 s has only moved the threshold is for you to answer, not to assume.
4. **FORCED HANG — THE NINE FILES STILL EXIT (MEASURED).** `QA_BC_MODE=hang` (a `close()` that never resolves), each file ALONE, at
   `703d304`: `print-fit`, `typed-rates`, `fx-provenance`, `phone-layout`, `email-collector`, `logo-inset`, `lib-close.test.mjs`,
   `lib-close-shared.test.mjs` and `xlsx-parity`. **Each must exit on its own within 90 s + margin**, and log
   `[test] browser.close() did not return within 90000 ms; killed the test's own Chrome (pid …)` where a log line is by design. Kill
   attribution: every kill must target this gate's own Chrome wrapper, with **0 `GoogleUpdater`, 0 `chrome_crashpad_handler` and 0
   foreign Chrome**, proven by pid ancestry anchored on YOUR claude pid. **Predict `lib-close.test.mjs` before you run it:** at 30 s it
   exited at 103.8 s because a global close-stub meets ~three cells that use the default bound. At 90 s, expect roughly three times
   that. Set its deadline accordingly (§13.5), and report the result as an exit, not as a deadline abort. **A real stalled Chrome**
   (`SIGSTOP` on the browser process you started) on ONE file is enough for this narrow gate. Say which file.
5. **TIER-1 CLAUSES ON `lib/pdf.js`, RE-ESTABLISHED AT `703d304` (MEASURED + READ). Do not carry them forward.**
   (1) **Byte-unchanged renderer, extracted over MAIN** (anchor on the body brace and print every block's size; gate 5's self-finding
   was a 46-byte "identical" block): `renderQuotePdf`, `browser()` including the launch, the `puppeteer.launch` options, `svcInject()`,
   `module.exports`, and **the whole file MINUS the `closeBrowser` comment + function**. Gate 7 measured **11,258 B /
   `617a79f87ac5d27c`** on both main and `58c9094` with its own extractor (`qa-bc-identity-g7.py`). With the same extractor, round 4
   should reproduce the same number, because it changes only inside the removed region. **Quote your hashes on both sides.**
   (2) **Production never calls `closeBrowser`: re-establish it, do not re-assert it.** Read every `lib/pdf` import in stage3 outside
   `test/`. Then your harness server signs in through the real OTP flow and emails two PDFs, with spies on the export,
   `CdpBrowser.prototype.close`, `disconnect` and `ChildProcess.prototype.kill`. Expect `{"closeBrowser":0,"cdpClose":0,"disconnect":0,"childKill":0}`.
   Then call the spied export yourself **in the same run**, so the spy is proven able to fire. **Say what a non-zero would mean:** the
   shipped default is now **18×** the original 5 s (and 3× round 3's 30 s). A production caller would wait up to 90 s on a Chrome that
   will not close before an emailed-quote request completed or failed.
   (3) **The emailed PDF against MAIN `d4426f8`:** pages equal, `pdftotext` equal, **0 differing pixels**, and differing bytes **only inside
   `/CreationDate` and `/ModDate`**, for default USD and heavy AUD, with a fixed quote number and egress blocked. The comparator's
   positive control (a planted difference) must fire in the same run. Quote the footer line and version from a real PDF at both (**both
   should read v2.33**).
6. **BCR2-O1's RETRACTION, CONFIRMED ONCE AT 90,000 ms (MEASURED).** One observe run at `703d304` with `qa-bc-preload.mjs`. Quote, in the
   order the instrument wrote them, a `ChildProcess.kill(SIGKILL)` line and the `real close() returned after N ms` line for the SAME
   `browserPid`, with **N ≈ 90,0xx and the kill line FIRST**. That is the tracking gate 7 measured at 5,000 / 30,000 / 90,000 (5,018 /
   30,017 / 90,024). **If a close "returns" at 90,0xx ms with NO preceding kill, the retraction's mechanism is wrong. That is a finding
   against gate 7 and this brief.**
7. **Red-proofs (parse-checked, one fresh tree per arm, never on a file that already hangs at the pinned head).** (a) Revert `lib/pdf.js`
   ONLY to 30000: the "one number" cell reddens, and **say that no behavioural cell sees `lib/pdf.js`'s default** (gate 7 found the
   same). (b) Revert `test/lib-close.mjs` ONLY to 30000: the "one number" cell reddens; **under load, does BC-F2 redden? (It should,
   because BC-F2 uses `closeBounded`.)** The unmodified `58c9094` tree in §N.3(b) is the both-modules arm. **A fix with no reddening
   behavioural cell is a finding.** Say whether round 4 added one; it added none. The regex is the only cell tied to the value (BCR3-P2).
8. **Suites at `703d304`, each with its EXACT command:** stage3 `npm test` (claimed **124**), `npm run test:print` (§N.2, **143**),
   `npm run test:xlsx` (**5**), and the root pricing pack `node --test quote-engine.test.mjs` (gate 7: **67**). **Report the relayed
   "root 353" against these commands** (correction (g)). **Count every suite. Do not read a smaller green as the same green.**
9. **CI / Linux Chromium is the carried gap, and round 4 widens it again.** `gh` is NOT authenticated for `datasecau`, and **you must not
   use `gh`**. State plainly that CI's `print-fit` job (`npm run test:print` on ubuntu with `/usr/bin/google-chrome`, node 22) is the first
   thing to measure at merge. State that a 90 s bound adds up to **13.5 minutes** to a fully hanging CI run. State that CI runners are
   routinely oversubscribed, which is exactly BCR3-F1's condition.

## 12. The merge and the queue
**The drafter ran NO `merge-tree`.** READ expectation: **`703d304` × main `d4426f8` is CLEAN, and the result tree equals `703d304`'s own
tree**, because main is its merge-base. Quote `git merge-tree --write-tree --name-only` from YOUR OWN object dir, or say you skipped it.
**Cells to re-run on the merged head** (name at least these): `test:print` end to end, timed, N ≥ 3, **asserting the process exits, at 143
cells, including at least one run at the red band's load with BC-F2 green**; the nine forced-hang arms; the emailed-PDF compare; the
`closeBrowser` spy; and CI's `print-fit` job.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (stage3's dev port) or `47787` (Tuesday's dashboard)**, or any port another seat holds. Take every
   port from the kernel, and bind `127.0.0.1` wherever YOUR harness listens. Never start QuickQuote's own entry point on its own. Use the
   real `createApp` inside your harness only.
2. **No database is needed** (the portal is not in this gate). **No docker command at all.** Nothing from `Vision_Sales_Portal/4_Credentials/`.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test`,
   never `production`; PORT; PUPPETEER_EXECUTABLE_PATH = YOUR copy of the egress-block wrapper; `NTFY_SERVER=http://ntfy.invalid`;
   dummy provider values; `npm_config_update_notifier=false`; `npm_config_offline=true`). **NEVER set in a product process:**
   `AGENTMAIL_API_KEY` and `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real `ACS_*` / `MAIL_SENDER`,
   `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, `HPAM_WORD`, `ADVANCED_UNLOCK_SECRET`, `WEBSITE_SITE_NAME`. Print each product process's
   env KEY NAMES (never values) and assert none is forbidden. **Never contact ntfy.sh.**
   **EGRESS, INCLUDING CHROME CHILDREN:** the real renderer's page calls three public **FX** APIs whenever currency ≠ USD. **Block them**
   with YOUR copy of `qa-chrome-egressblock.sh`, **prove the block with a positive control**, and run the net-log scan at the end.
   `GoogleUpdater` / `chrome_crashpad_handler` reparent to launchd, so record them at start and at end (pid, ppid, start time) and say
   which appeared during the gate.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied from gate 7's evidence):
   `basename(argv[0]) == node`, with an app entry point ANYWHERE in the remaining argv, read from the kernel. **"Ours" = the ancestor
   chain CONTAINS your claude pid.** **The negative controls must classify FOREIGN in the same run:** Tuesday's claude `2679` (pane
   `%0`, the only other claude on this box at drafting, 13:1x AEST). **Re-read the seat list at start.** Name every other claude that
   is running, and say if `2679` has exited. Never count by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. **A zero is
   reportable only beside a control that fired in the same window**: spawn one server your way, ATTACHED, confirm the count rises, then
   reap it.
5. **THE DEADLINE RULE, with this round's DELIBERATE EXCEPTIONS (the drafter proposes them; Tuesday confirms them by stamping):** every
   browser step has a written DEADLINE and a client timeout. **This machine has no `timeout` binary, so build the deadline into your
   runner.** A step past its deadline is ABORTED and reported. **Every server, browser, loader and child you start is killed in a
   `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes. A step with no heartbeat for 5 minutes
   is aborted and reported.** **Gate 7's "never above 150 s" CANNOT hold at a 90 s bound** (its own 90 s arm ran 188.2 s). The
   deadlines for this gate: **idle `test:print` 240 s; loaded `test:print` 300 s** (the load must outlast it); **forced-hang per file 180 s,
   except `lib-close.test.mjs` 360 s; the 240 s discriminator arm 420 s. Nothing above 420 s.** State each exception in the report
   wherever you use it.

**Reap every server, every Chrome and every loader you start.** An orphan of yours becomes someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (App Service `hpas-quickquote`, resource group `hpas-quickquote-rg`, its ACR `hpasqqacr`, its Table Storage,
  and its log workspace `hpas-quickquote-logs`, which decision 18 says never to query) **or the live portal**
  (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg`: PRODUCTION). No request, not even a GET
  or a health probe. **Never ntfy.sh. Never the three FX hosts. Never the npm registry. Never `api.agentmail.to` from a product
  process.**

### HELD
- No merge, no deploy, no registry, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npm audit`, and no `npx` of
  anything not already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Real sends are OFF.** Every provider is a recorder you wrote.
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in either repo**, and none inside
  `Vision_Sales_Portal/`, inside the builder's scratchpad, or inside gate 1-7's report folders or trees. The gate fixes nothing.
- **NEVER `rm`.** Quarantine instead. Every preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-25-vision-qq-gate8/report.md`
(sections and `evidence/` beside it).

**QUESTIONS:** your routing name is **`QA/Vision-gate8`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate8] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 8: BCR3 round 4 @ 703d304: ` and then `GO` or `NO-GO`.
Lead the body with one sentence: does 90 s stop the false kill at the red band's load, and was every kill at 90 s a genuine hang?
You have no inbox that wakes you, so a verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **BCR3R4 (bounded close, round 4): GO / NO-GO**, naming the pinned sha `703d304` and the branch
  `fix/qq-bounded-browser-close-2026-09-23`. Report on each of these: BC-F2 at the red band's load (N ≥ 3, load quoted) **against the
  `58c9094` control that reddened in the same window**; **every kill at 90 s discriminated** (hang or slow-healthy, with the 240 s arm);
  the headroom stated as numbers; `test:print` completing and exiting (N ≥ 3, 143 cells, the elapsed time and load for each run,
  phone-layout's kill rate); the nine forced-hang files exiting; the tier-1 clauses (renderer byte-unchanged, 0 production calls with a
  firing spy, 0 differing pixels vs main); BCR2-O1's tracking confirmed at 90,000 ms.
- **THE CAP:** state that THE CAP IS NOT SPENT is Tuesday's ruling, not Kam's, and quote gate 7's line that a fourth round needs Kam. If
  NO-GO, list what CLOSED and would ship and what is TICKETED, and say that **a third round on that class** needs Kam under C-62.
  Recommend no further round.
- The verbatim strings an operator needs: the bounded-close log line at 90,000 ms, any `TimeoutNaNWarning` (expected: none), BC-F2's
  line under load, and the footer line and version from a real PDF at `703d304` and at main.
- One paragraph on the queue quoting §12's merge-tree result, or saying you skipped it.
- **Rule 2: what you did NOT test is first-class output.** Write a NOT TESTED section that covers at least **CI / Linux Chromium**, still
  the biggest gap; **Node 20 and Node 22** (CI runs node 22); **the container image**; and **real-world CI load**. **Every action
  recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.** Each of §N Q1-Q9 carries one.
- Report the pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: QQ main `d4426f899620…`, `fix/qq-bounded-browser-close-2026-09-23` `703d304d859c…` | `git -C <repo> ls-remote origin` +
  `cat-file -t` (commit) | read 2026-09-25 13:09 AEST
- chain: `703d304` (parent `58c9094`) → `983f916` (merge, parents `f8dec9c` + `d4426f8`) → `f8dec9c` → `aa89010` → `907f686` →
  `3bfbfa2`; 6 over main, 0 behind; merge-base = `d4426f8` | `git log --format='%H %P %s'`, `rev-list --left-right --count`,
  `merge-base` | read 13:09-13:1x
- round-4 delta (4 files) and branch delta (15 files); the four literals at `lib/pdf.js:208,212` and `lib-close.mjs:21,26`; the cell
  at `lib-close.test.mjs:132`; swap-equivalence of the three files to `58c9094`; `lib/pdf.js` minus the closeBrowser block equal at main,
  `58c9094` and `703d304`; lockfile `70ebda7` and `index.html` `e90250f` (toolVersion 2.33) equal at main and head; the `closeBrowser`
  referencers; the production importer `stage3/server.js:890` | `git diff`, `git grep`, `git show`, `git rev-parse`, python over
  `git show` output, all under `bash` | read 13:1x-13:2x
- root pricing pack = `node --test quote-engine.test.mjs`, 67 `test(` calls | `.github/workflows/tests.yml`, `git show` | read 13:2x
- gate 7's 90 s arm: N = 1, 188.2 s, load 36.89→60.17, five kills at 90,0xx ms, healthy closes 62,260 / 58,240 / 42,766 ms |
  `…/gate7/evidence/bc/disc-b.txt`, `disc-b.qalog` | read 13:2x
- gate 7's verdict, BCR3-F1, the tracking figures, "A further round … would be a FOURTH round … needs Kam's word" |
  `…/gate7/report.md:57-123`, `sections/BCR3.md` §2-§5 | read 13:1x
- the narrow-gate pattern | NexusAI `…/2026-09-22-gate5-rd615-rd616/report.md:49` (the Vision gate-5 report has no §B) | read 13:2x
- Tuesday's rulings (round 4 = one number, narrow; BCR2-O1 retracted; live v2.33) and the absence of any Kam word on round 4 |
  `0_Brain/daily_tuesday/2026-09-23.md` 09:45 / 12:19 / WENT WELL, `2026-09-24.md`, `2026-09-25.md` 09:42-09:43,
  `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md:14,36,58` | read 13:1x
- C-62 verbatim | `…/NexusAI/1_Project_Definition/CLARIFICATIONS.md:573` | read 13:1x
- seats: `%0` → claude `2679` (Tuesday, started 09:25), the only other claude; `hw.ncpu` = 8; load 2.12 at 13:12 | `tmux list-panes -a`,
  `ps`, `sysctl`, `uptime` | read 13:12
- builder claims | commit message of `703d304`; `BACKLOG.md` at `703d304` (mail bodies NOT read)
