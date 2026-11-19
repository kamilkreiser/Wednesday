# B1746 and B1747 drafter commissions — MPS v13.4.1 first wave: lane 1 (MPSCALC-267) and lane 2 (MPSCALC-278)
Commissioned by Tuesday (s293), 2026-11-19. Drafter model: Sonnet (routing row C8). Each drafter DRAFTS one kit; builds nothing.
Two drafters, one kit each; do only the kit named in your prompt.

- **B1746, SEAT-M164, lane 1: MPSCALC-267** (V5-7 projection table) -> kit
  `2_Project_Files/tuesday/briefs/2026-11-19_B1746_SEAT-M164_mps-v13-lane1-projection-table.md`, scratch `fleet/state/s293/d1746/`.
- **B1747, SEAT-M165, lane 2: MPSCALC-278** (V8-2 priced or unpriced proposal) -> kit
  `2_Project_Files/tuesday/briefs/2026-11-19_B1747_SEAT-M165_mps-v13-lane2-priced-unpriced.md`, scratch `fleet/state/s293/d1747/`.
Each kit has its `.measured` sidecar; the drafter report comes back as TEXT in the reply (Tuesday saves it).

SOURCE: `2026-11-19_B1744_mps-v13-buildable-lanes.md` (same folder): read sections 2 (the rule), 5 (your lane) and 6
(two lanes at once) whole; it was measured this afternoon at MPS main 317bbb14: RE-MEASURE every file, line and count at
the current main and print the sha. FORM: a recent MPS WEB builder kit of similar size, found with ls in the briefs folder
(lanes of 2026-11-11 to 11-16 that changed `web/src/**`; read it whole with its builder STATUS Corrections) plus the
structure of `2026-11-19_B1741_SEAT-M163_mps-lane-mg-accepted-wording.md`. Follow `2_Project_Files/tuesday/DRAFTER_RULES.md`
whole (the volume is /Volumes/Datasec_DEV). Project: '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial
Calculator' (its local code checkout is stale; read code at origin main by `gh api -X GET`).

THE RULE THE KIT QUOTES (read it at source and quote with line numbers): CLARIFICATIONS.md C-45 option a detail (line 660
at B1744's read): "Lanes start in waves as soon as you tap. Every new customer-facing word still comes to you as a word
pack before it ships, and nothing is deployed without your card." Tuesday's reading (a default under the standing backlog
grant, written as Tuesday's, never as the product owner's): the lane is BUILT and may be MERGED to main after its gate;
its new words go to the product owner as a WORD PACK before any hosted deploy; nothing is deployed. Earlier lanes did
the same (PRs #85 to #91, pack ruled in C-48).

WORDS (the centre of these kits):
- The builder writes NO word of its own. Every customer-visible string the lane introduces is FROZEN in the kit, each
  with its source quoted (the gap analysis row, the ticket, an already approved string, the Api member name). B1744
  counts 9 strings for lane 1 (gap row V-55, `GAP_ANALYSIS.md:178`) and 2 for lane 2 (gap row V-63, `:196`, and the
  already approved 'Price on request'): verify each at source, quote the row, and count them yourself by program.
- If the lane cannot be built without a string that has no source, the kit names that string as a STOP question; you do
  not draft it.
- The kit REQUIRES the seat to write `WORD-PACK.md` into its Briefs folder as part of READY: every new string, where it
  shows (screen, document, condition), its source, and a screenshot or printed-text excerpt reference if the lane's own
  tests render it. A READY without it is returned.
- Lane 2 only: the acceptance is "no price appears anywhere" in the unpriced document, tested over the PRINTED TEXT:
  the kit carries cells for every document the option applies to, and you must settle from the ticket and the gap row
  WHICH documents take the option (Standard, short form, rental book). If the ticket does not say, that is a question
  with a default for Tuesday (default: the narrowest set the ticket names). If recording the choice needs a new contract
  member, that part is OUT of the lane (a STOP), and the kit builds only what needs none.
- Lane 1 only: the table shows figures the Api sends; NO arithmetic in the browser; the Api nulls `Projection` for a
  caller without the internal-metrics permission: the kit carries a leak cell (a caller without it sees no table and no
  figure in the DOM or the stub's payload), and says what a rental quote shows.

REQUIRED CONTENT (both): PRIOR-WORK CHECK (what main already holds; the ticket whole with every comment; any PR naming
the key); the lane property (paths owned, stated from both sides; the other lane's paths and kit B1741's
`QuoteEndpoints.cs` are NOT yours); an old-answer census BY PROGRAM of tests and snapshots that pin the current output of
the files edited; predicted figures MEASURED on a scratch copy or marked UNMEASURED; the toolchain and the exact test
commands quoted from the form kit's real run (vitest `-t` is a JS regex); the port block and heavy-check slot rule of the
form kit (two MPS lanes run at once: give lane 1 and lane 2 DIFFERENT port blocks and say how each seat tells its
processes from the other's); the project's landing rule quoted (branch push only; Tuesday opens the PR; head-pinned
squash; hosted CI and CodeQL, 9 checks on #217); gate recommendation G1 OPUS for both (lane 1: internal money figures
and a leak surface; lane 2: a customer document that must hide prices) with the CodeQL step
(`2_Project_Files/tuesday/tools/codeql/GATE_STEP.md`: say whether the tool is proven for this repo's languages; if not,
say the hosted check is the authority); no ruling is cited beyond C-45 and the D-rows the ticket itself names (quote
them); every other choice is Tuesday's default; test-cell counts by the indented pattern with the column-1 count beside.

HOW: read-only everywhere except your kit, sidecar and scratch. gh `-X GET` under the project's own GH_CONFIG_DIR; git
read verbs only; Jira GET only (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN by name in-process, never printed). NEVER read
`.local/`, `Source_Documents/**`, a price book or real price store. Nothing of HPSM-POC or any other project. NO build,
NO test run, NO server (a build seat is running in this repo's project now and a gate holds another project's lock: you
measure by reading). No az, no request to any app host. No `cd`; no unquoted word starting with `=`; zsh; absolute
paths; never delete; clocks from `date`. `stamp_check.py <kit>` must exit 0; leave every Stamp slot unfilled; ASCII;
built whole, temp file, os.replace.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, recommended slots (base sha, port block, model row,
gate), the frozen strings with their sources, corrections to this commission and to B1744, D/Q defaults, UNMEASURED.
