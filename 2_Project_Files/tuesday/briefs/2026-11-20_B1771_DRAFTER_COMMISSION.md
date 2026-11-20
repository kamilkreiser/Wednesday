# B1771 drafter commission — NexusAI lane N-M: RD-1008 (SEAT-N161)
Commissioned by Tuesday (s297), 2026-11-20. Drafter model: Sonnet (routing row C8). You DRAFT a kit; you build nothing.

Draft ONE builder kit `2_Project_Files/tuesday/briefs/2026-11-20_B1771_SEAT-N161_nexusai-lane-nm-chat-error-text.md`
(+ `.measured` sidecar; ALSO save your drafter report as `2026-11-20_B1771_DRAFTER-REPORT.md` beside it, and return its
head as TEXT in your reply) in the FORM of the newest NexusAI builder kit,
`2026-11-20_B1762_SEAT-N160_nexusai-lane-nk-datasource-role-checks.md` (read it whole; its `.pre-stamp` copy shows the
unstamped form), following `2_Project_Files/tuesday/DRAFTER_RULES.md` whole (it names /Volumes/Laptop-DEV in places: the
volume is /Volumes/Datasec_DEV) and **every rule of the commission that produced that kit,
`2026-11-20_B1762_DRAFTER_COMMISSION.md`: read it whole; its sections REQUIRED CONTENT (the code-scanning rule, the
old-answer census by program, how existing tests reach the code, selectors in JS-regex syntax checked against test names,
totals recomputed, prose counts recounted, test-cell counts both ways, stamp values never repeating their label, no text
saying the product owner decided anything) and HOW apply to you unchanged, with the lane facts below in place of its
own.** Fold in by name the lessons of the builder STATUS of that lane if it has ended when you read it
(`!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-20_B1762_STATUS.md`: Corrections and Deviations first; at
13:21 today its last line read WORKING, the chain holding the jest lock) and of the two before it
(`.../2026-11-19_B1739_STATUS.md`, `.../2026-11-19_B1737_STATUS.md`) and the reviews
`2_Project_Files/tuesday/briefs/2026-11-19_B1756_verify/VERDICT.md` and `2026-11-19_B1745_verify/VERDICT.md`. All paths
are under /Volumes/Datasec_DEV/TUESDAY or /Volumes/Datasec_DEV/!CODING/Datasec.

SOURCE OF THE LANE (measured on 2026-11-19 at an OLDER main: RE-MEASURE every file, line, blob and count at the current
main): `2026-11-19_SWEEP-1630_datasec-backlog-unblock.md` lines 66 and 80 (and the cells that follow line 80), and
`2026-11-19_SWEEP-1630_TUESDAY-ANSWERS.md` lines 11 and 29 (the lane order N-K, then N-M). Read RD-1008 WHOLE by Jira GET
(description and every comment) and quote its scope and acceptance sentences; a comment or status change since
2026-11-19 is new: report it first. The ticket was filed by a records pass from the independent review of pull request
229: read that review's finding too (the verify folder of that gate under `2_Project_Files/tuesday/briefs/`; find it by
searching the briefs folder for RD-1008, with a positive control) so the kit rests on the finding and not on the
ticket's summary of it.

SCOPE (each choice is Tuesday's decision as coordinator, a default under the standing backlog grant, NOT the product
owner's; the kit, the commit text and the PR text must write it that way):
- RD-1008, both halves, as the ticket states the fix: (1) the server decides to keep an AI endpoint's own error words by
  the error's CLASS (or the adapter's own constant), never by a `code` string an endpoint can supply, at every place that
  makes that comparison (the sweep read three in `backend/server.js`: `chatErrorText` and two code-string tests; find
  them ALL by search, with a control: a fourth would be in scope, a comparison of another constant is not); (2) the
  browser writes a stream error event's message into the chat bubble as TEXT, never as markup (`static/js/index.js`,
  the line the sweep printed).
- **Sibling sinks: list, do not fix.** Search `static/js/**` for every other place a server-supplied or
  endpoint-supplied string is written with `innerHTML` (or `insertAdjacentHTML`, `outerHTML`, `document.write`) and
  print the list with its count; anything beyond the one line of RD-1008 is OUT of this lane and goes in the report as a
  candidate ticket (search the board for each first, by symbol and file, and say what you found). The kit tells the
  builder the same: a sibling is listed and STOPs, never fixed quietly.
- No customer-visible word is added or changed: PROVE it by printing every error text a user can see through these
  paths before the change and what each reads after; if a text a user sees would change (other than a hostile
  endpoint's own words no longer being shown), state exactly which and make it a question with a default in the report.

BASE AND THE LANE BEFORE YOU: NexusAI main is b169b8a0eee8eaac594e98918c2ccaff91164dcf (read by Tuesday 2026-11-20 at
13:17:46 with the GitHub API; re-read it and say so). **Lane N-K (kit B1762) is building NOW and is not landed: it adds a
first statement to four handlers in `backend/server.js` and changes `backend/services/capabilities.js`, the generated
role inventory, `backend/services/accessAudit.js`, `backend/routes/entraProvisioning.js` and
`scripts/verify-expected-counts.json`. Your lane starts only after it has landed, so main will have moved.** Therefore:
give every pointer in `backend/server.js` as a content anchor (the exact line text, counted once by program) with the
line number at b169b8a0 beside it as a dated reading; say which of your owned files N-K also touches (the expected-counts
file at least) and how the kit re-derives its figures at Step 0 from the main it finds; leave the BASE slot for
Tuesday's stamp; the kit carries the re-measure rule (an owned path whose anchor no longer reads once at Step 0 is a
STOP).

PARTITION: owned = `backend/server.js` (ONLY the lines of the comparisons; every other line byte-identical; the file is
about 19,000 lines and holds open code-scanning alerts), `static/js/index.js` (ONLY the one write), the file that
defines the redirect-refusal error class ONLY if the fix needs an export from it (read it; say whether it does), new
`__tests__/rd1008-*` files, the expected-counts file (regenerated by the project's own command), and any existing test
that pins an OLD answer. NOT owned: everything else; workflows, compose, templates and every other `static/**` file are
read-only.

ALSO REQUIRED for this lane:
- **The code-scanning rule is sharper here:** this lane edits lines near open alerts and removes an XSS sink. Print the
  open alerts in `backend/server.js` and `static/js/index.js` at the current main (number, rule, severity, line), say
  for each whether its data-flow path can touch a line this lane ADDS, and whether the change is expected to CLOSE an
  alert (name it; "expected" is UNMEASURED until the kit's CQ runs say so). The kit runs
  `2_Project_Files/tuesday/tools/codeql/pr_codeql_check.sh` twice (before the lock and before the push; see
  `tools/codeql/GATE_STEP.md`); rc 1 is a STOP, never a dismissal.
- Cells (the ticket's, at least): a hostile endpoint whose error body carries the refusal constant in `code` no longer
  gets its words into the stream event; the real redirect refusal still reads as it does today; markup in an event
  message renders as text in the bubble (say how the browser half is tested in this repo: which existing harness reads
  `static/js/index.js`, with its name and one test name; if none can, say so and propose the smallest honest check);
  plants with predicted red cells, each dry-run by you on a scratch copy or marked UNMEASURED.
- Gate recommendation: Tuesday's answers file says G2 plus the CodeQL check; say whether you agree after reading the
  code, and why (an XSS sink and server error text: argue G1 if you see cause).
- Builder model recommendation with the routing row (`2_Project_Files/fleet/specs/model-routing.md`), since the change
  is security-relevant.

HOW: as B1762's commission, section HOW, word for word, with scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s297/d1771/` and the jest worktree slot chosen by scanning the
briefs of 18 to 20 November for slots already named (N-K's kit names one: not that one). Read-only everywhere; the
NexusAI jest lock is HELD by the running lane: run no jest, no build and no install in the project's trees; a dry run of
a plant happens only in your own scratch copy and only if it needs no lock and no heavy job (otherwise UNMEASURED).
First line of your reply: `STARTABLE: YES|NO - why`. Then the report: files, recommended slots, corrections to this
commission, D/Q defaults, UNMEASURED list.
