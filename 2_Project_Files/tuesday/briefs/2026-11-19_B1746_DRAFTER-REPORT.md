STARTABLE: YES - kit complete, stamp_check exits 0 (drafter's run); it needs Stamp S8 filled with a node 24 folder (the project has no drive-local node; the machine default is v26).

# B1746 drafter report (SEAT-M164, MPS v13 lane 1: MPSCALC-267 projection table)
Saved by Tuesday (s293) from the drafter's in-session reply. Condensed by Tuesday; the kit is the authority. Figures are the
DRAFTER's, not Tuesday's.

## Files
Kit `2026-11-19_B1746_SEAT-M164_mps-v13-lane1-projection-table.md` (158 lines, 60508 bytes, ASCII, 11 unfilled Stamp lines
S0 to S9 and the last line); sidecar `.measured` 103 lines. Scratch `fleet/state/s293/d1746/`.

## Recommended slots
Base MPS main 317bbb14c7258023b1d2855a9bcce1b9b07b93f6 (0 open PRs at 17:45); port block 9980-9989 (listener 9981); lane 2
should take 9970-9979; builder Sonnet row C2; gate G1 Opus with the CodeQL step (the local tool is UNMEASURED on this repo:
hosted CodeQL is the authority); branch `b1746/mps-v13-lane1-projection-table-267`; pane `Datasec/MPS-M164`; READY = Step 0
plus 120 minutes; S8 = a node 24 folder (Tuesday's own tree holds `2_Project_Files/tools/node-v24.22.2-darwin-arm64`:
verify it at the stamp).

## Frozen strings (10; the builder writes none of its own)
W1 the caption `Projection` (ticket summary, gap row V-55 at GAP_ANALYSIS.md:178, member Projection at Dtos.cs:932);
W2 `Monthly`, W3 `Annual`, W4 `Contract` (column heads); W5 `Pages`; W6 `Click cost`; W7 `Managed service cost`;
W8 `Click revenue`; W9 `Service revenue`; W10 `Recurring GP` (row labels; the gap row's lower-case words and the Api
members). The only change from the gap row is the capital first letter. The top-left cell is empty.

## Corrections to the commission and to B1744
1. 10 strings, not 9 (the caption). 2. The gap row names 10 rows; the Api sends 6 measures; NOT built and listed for the
word pack: pages mono and colour as two rows, total recurring cost and revenue (the totals would be browser arithmetic).
3. "(x12)" and "(xterm)" are DROPPED: schema.ts:1859 and ENGINE.md:166 say the contract figure is not monthly times term.
4. Purchase only: a rental quote shows no table (no Api member; MPSCALC-368 "Not in this ticket"). 5. Main has
`web/src/test/noBrowserPricing.test.ts`: a named heavy check, with a mutant that plants arithmetic. 6. CI has a new
`npm audit --omit=dev --audit-level=high` step: baselined. 7. C-110 (CLARIFICATIONS.md:2725): the member name
`projection` still awaits approval; a rename before landing is a STOP. 8. The e2e rows append to
`itemised-summaries.spec.ts`, which also holds S11 (lane 2 territory): B1747 must not edit it, or the lanes are ordered.

## D / Q (Q1 to Q14 in the kit; all Tuesday's defaults when stamped)
Rule reading as commissioned; caption included; parentheses dropped; six rows; first capital only; formatCount for Pages,
formatMoney for the rest; the stub gets a zero projection for internal personas only; four e2e rows; the internal labels
list stays at 23; the table mounts between the deal usage table and the issues list; node 24 in S8; G1 Opus; the seat
measures test counts; no rental table. The fixture deliberately breaks annual = monthly x 12 so a browser that computes
the figure fails.

## UNMEASURED
Baseline vitest and e2e counts and wall-clocks (no build or test run); the node 24 folder; pr_codeql_check.sh on this repo;
whether lane 2 touches itemised-summaries.spec.ts; the 18 shown figure texts and the red/green pattern of the nine rows and
five mutants (derived or predicted); the product owner's marks on any word.
