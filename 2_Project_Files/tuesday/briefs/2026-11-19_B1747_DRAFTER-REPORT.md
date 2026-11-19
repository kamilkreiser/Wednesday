STARTABLE: YES - kit built, stamp_check exits 0 (131 of 131, drafter's run); main 317bbb14 at 17:48:46. NOT READ BY TUESDAY, NOT STAMPED.

# B1747 drafter report (SEAT-M165, MPS v13 lane 2: MPSCALC-278 priced or unpriced proposal)
Saved by Tuesday (s293) from the drafter's in-session reply. Condensed by Tuesday; the kit is the authority. Figures are the
DRAFTER's, not Tuesday's.

## Files
Kit `2026-11-19_B1747_SEAT-M165_mps-v13-lane2-priced-unpriced.md` (163 lines, 66156 bytes, ASCII); sidecar `.measured` 131
lines (77 measured literals, 54 INSTRUCTION). Scratch `fleet/state/s293/d1747/`.

## TO FIX OR DECIDE AT THE STAMP (Tuesday's list, written by s293 from the report)
1. **PORT BLOCK CONFLICT.** The kit takes 9980-9989 (listener 9981). Lane 1 (B1746, M164, LIVE) was stamped with that
   block and its S7 slot promises lane 2 gets 9970-9979 (listener 9971). Change the kit to 9970-9979 by an atomic
   replace before the stamp (every literal: grep `998` and `9981`), then re-run stamp_check.
2. **NODE.** The kit uses the machine node v26.13.0; CI pins node 24 and lane 1 uses Tuesday's
   `2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin`. Decide one: recommended the node 24 folder (a green on 26 is
   not CI's green); the kit says it follows a newer convention (B1707): read that line before changing it.
3. **D3, an honest gap in the words.** W3 reads "Show SKUs and quantities only" but the unpriced documents show
   quantities and NO SKU column (adding one needs a words decision). The lane would ship a seller-facing label that
   promises more than the document shows. Options: build as frozen and flag it first in the word pack (the drafter's
   default); or hold the lane until the product owner picks the label or the column. Tuesday (s293) leans to build and
   flag, because nothing ships before the pack is ruled; the stamping seat decides and writes it as its own.
4. **D4.** "The choice is recorded" is built as page state plus a data attribute; a durable record needs a contract
   member and is OUT: MPSCALC-278 stays open on that clause (say so in the PR text and the records).
5. Lane 1 owns `web/e2e/itemised-summaries.spec.ts`: the report's four paths do not include it (verify in the kit).
6. Two MPS lanes at once: lane 1 is live; heavy slots are shared (two machine-wide).

## What the kit builds (drafter)
Four paths: `web/src/screens/ProposalPage.tsx`, `web/src/proposal/ProposalDocument.tsx`, `web/src/proposal/OnePager.tsx`,
new `web/src/proposal/unpriced.test.tsx`. The option applies to the two PURCHASE documents (full and short form); the
control is hidden on rental quotes; the rental book and rental short form stay priced (a rental option is a separate
lane). 23 price sites listed with an OMIT or COLUMN disposition and no replacement text. Oracle: a vitest over the printed
text (no dollar sign, no fixture decimal in any display form), with a planted control; a base capture of 8 priced renders
proves the priced output is byte-identical after the edit.

## Frozen strings (3, all from gap row V-63, GAP_ANALYSIS.md:196)
W1 `Customer PDF option` (legend of the option group); W2 `Show customer unit and extended prices` (first radio, default);
W3 `Show SKUs and quantities only` (second radio). No other word; `Price on request` is not used. A cell proves every leaf
text of the unpriced document already exists in the priced render.

## Recommended slots (drafter)
Base 317bbb14c7258023b1d2855a9bcce1b9b07b93f6; builder Sonnet row C2; gate G1 Opus (hosted CodeQL is the authority);
READY = Step 0 plus 150 minutes; word pack file `1_Project_Definition/Briefs/2026-11-19_B1747_WORD-PACK.md`.

## Corrections to the commission and to B1744
3 strings, not 2; four renderers on the page, not three; the real edit set is four paths, not `proposal/**`; the ticket
says both "depends on D-09, D-14" and "Depends on: nothing" (neither D row gates it; both quoted); the gap row's last cell
names a person and is omitted from the kit.

## UNMEASURED
New test-cell counts; e2e counts; whether the prototype shows W1 as a visible heading; live panes; the local CodeQL tool
on this repo; wall-clocks. No build or test was run.
