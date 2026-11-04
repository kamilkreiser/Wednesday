From Tuesday (the product owner's Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B1290 / SEAT-D52 (the UAT deploy of the visual round). Written by Tuesday s245 BEFORE the kit was stamped; the stamp (slot S1) names this file and its sha256. Read it whole before Step 0's REFUSE checks, before the first `az` call and again before DEPLOY START (kit item 5). Where this addendum and the kit disagree, THIS ADDENDUM governs; everything it does not name stands as written.

# ADDENDUM-1: the branch head is W4 `fb84db8d`, not `a7b82c27`; the gate of record is the cap ruling, not a B1289 GO; the 06:15 / 06:45 clocks are VOID

## A1. THE BRANCH HEAD (supersedes every use of `a7b82c27b751524f813cceb9758a3d784b7903a9` as the visual-round branch head, the PR head or the tree-equality reference)
The visual-round branch `b1272/hpsmpoc-visual-round-2` now stands at **`fb84db8da91b21bd3db23317182f457e7d6b7c0f`** (W4): ONE commit on `a7b82c27` whose only change restores `web/e2e/mock-rows.spec.ts` to its `9061c291` blob. MEASURED by Tuesday (`gh api -X GET`, project `GH_CONFIG_DIR`, in the command whose `date` printed 07:32:20 AEDT 2026-11-05):
- `commits/fb84db8d...`: tree `01523852facbc17d9072d225835cb2d690cc198c`, ONE parent `a7b82c27`.
- `contents/web/e2e/mock-rows.spec.ts` blob: at `fb84db8d` `b355b1da237f446276b0b40a65f21d030f0e1243`; at `9061c291` the SAME `b355b1da...`; at `a7b82c27` `4b38025e5722f4bdce005bdd0814941457ac341e`; at `fc2bc2fc` absent (404: the file is new in the range).
- `compare fc2bc2fc...fb84db8d`: status ahead, ahead 11, behind 0, **118 files**; the path list is the SAME 118 paths as `compare fc2bc2fc...a7b82c27` (a `diff` of the two `filename status +a -d` lists differs on ONE line only: `web/e2e/mock-rows.spec.ts added` +224 at `a7b82c27`, +206 at `fb84db8d`); the only path outside `web/` is `api/src/HpsmPoc.Modules.Reporting/Pdf/BrandTokens.cs` modified +11 -11.
**So, in the kit:** (i) the closed-list proof's path `diff` is against `compare PREV...fb84db8da91b21bd3db23317182f457e7d6b7c0f` (118 paths, EQUAL, or STOP); (ii) **D-1's tree check: `TARGET`'s tree must equal `01523852facbc17d9072d225835cb2d690cc198c`** (the head-pinned squash of `fb84db8d` on an unmoved main `fc2bc2fc`); (iii) REFUSE "The target": the PR's `head.sha` = `fb84db8da91b21bd3db23317182f457e7d6b7c0f`; (iv) the "ahead 10, 10 commits" of item 1 reads ahead 11 for the branch; the squash `TARGET` is still ONE commit with ONE parent `PREV`. The product (non-test) files of the range are UNCHANGED by W4, so the 80 product paths, the BrandTokens 11 strings, D-8's census frame and the gate's product figures all stand.

## A2. THE GATE OF RECORD (supersedes REFUSE "The target"'s requirement that the B1289 first line read GO or GO WITH FINDINGS, and slot S6's "B1289 verdict line ... head-pinned squash at head a7b82c27")
- B1289 (G343) is **NO GO, round 2 of 2 (THE CAP)** at `a7b82c27` (its first line, printed by `head` by Tuesday just before this addendum was written: `GATE VERDICT B1289: branch b1272/hpsmpoc-visual-round-2 NO GO @ a7b82c2 on main fc2bc2f (round 2 of 2, THE CAP, ...`). Its first line records every property closed (brand tokens 25 of 25, API 3933/0/22, names lost 0, header 72 24 of 24, page-end max 48 over 64 0 of 72, 116 of 117 carried paths equal) EXCEPT that W3's edit of `mock-rows.spec.ts` made `journey-and-prototype` red (2) and the data-delay instrument 9 of 9 red.
- **The product owner ruled the cap card at 07:06:42 AEDT 2026-11-05 (live board), option a: "Land it without the test change"** (restore `mock-rows.spec.ts` to its `9061c291` blob, keep BrandTokens, land, UAT, then the demo). W4 is exactly that restore (A1). This ruling, with W4 verified at source, is the gate authority for `TARGET`; slot S6 quotes it.
- **The seat therefore:** prints B1289's first line (expected: NO GO round 2 of 2) and B1280's first line (NO GO round 1 of 2); proves A1's blob and tree facts itself; and STOPs on any B1289 Major OTHER than the `mock-rows.spec.ts` condition-wait finding that slot S6 does not carry by name. `Briefs/2026-11-05_B1291_STATUS.md` (the W4 builder, H122) joins STANDING LINE 1's PRIOR WORK list, read as CLAIMS; B1288's spec claims are superseded by it.
- "Where B1289 restates a figure, B1289's governs" (kit item 4) stands: those figures were measured at `a7b82c27`, whose product files equal `fb84db8d`'s.

## A3. RULING 6, THE PRINTED REPORT (answers the drafter's Q-2)
The product owner ruled card "the printed report follows the new palette" at 07:06:33 AEDT 2026-11-05 (live board), option a "Keep it". Slot S13 therefore reads `PRINTED REPORT FOLLOWS THE NEW PALETTE: ACCEPTED`. D-15 stands (no live PDF on UAT).

## A4. AUTHORITY, ADDED (kit item 5 and slot S2)
Besides the three 2026-11-04 rulings the kit quotes, the product owner wrote at 07:07:20 AEDT 2026-11-05 (live board): "please go ahead and make all the layout changes as per the HTML and let me know when its deployed on all systems". **For THIS kit that means: deploy `TARGET` to UAT now; the demo follows in its own kit after this STATUS ends** (slot S8 stays `UAT ONLY; DEMO HELD`: held for this kit only). A SECOND layout round (more HTML rows) is a later build and is NOT in `TARGET`; nothing of it is deployed here.

## A5. CLOCKS (supersedes the 06:15 cut-off and the 06:45 DONE everywhere: kit item 5, CLOCK, HOLDS, slot S3, REFUSE "Clock")
The 06:15 and 06:45 AEDT times are VOID (the review moment they served has passed; the product owner has asked to be told when it is live). **Hard stop = Step 0 + 120 minutes, written by you as an absolute AEDT clock at Step 0; no write START after it; DONE no later than Step 0 + 150 minutes; Step 0 within 45 minutes of slot S1.** The CI wait keeps its rule: at most 45 minutes AND never past the hard stop minus 40 minutes. The BEFORE-walk cut-down rule in CLOCK stands, measured against this hard stop.

## A6. THE PULL REQUEST
The visual-round PR is **#286** (`datasecau/HPSM-POC`, head `fb84db8d`, base `fc2bc2fc`, opened by Tuesday s244). Tuesday lands it as a head-pinned SQUASH (`--match-head-commit fb84db8da91b21bd3db23317182f457e7d6b7c0f`) after CodeQL and both SQL Server shards are green; slots S4, S5, S12 are filled after that landing, from reads at source.

## A7. PANES (kit REFUSE "Panes" stands; for your listing)
At the writing of this addendum the live panes were `%0 tuesday`, `%236 Datasec/NexusAI-G344` (a gate of ANOTHER project and repository; not an HPSM-POC pane) and `%1 fleet-monitor`. No `Datasec/HPSM-POC-*` pane was live. Re-list at Step 0 and before DEPLOY START.

## A8. ADDENDUM GUARD
`partA1290.sh`'s addendum guard (kit BUILD 6) counts exactly ONE file `B1290_ADDENDUM-*` in `tuesday/briefs/`: this one, whose sha256 slot S1 names. A second addendum, or this file with a different sha256: STOP.

End of ADDENDUM-1.
