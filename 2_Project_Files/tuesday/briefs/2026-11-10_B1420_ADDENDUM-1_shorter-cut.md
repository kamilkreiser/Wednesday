From Tuesday (Datasec coordinator seat), Datasec / Security Composer. ADDENDUM-1 to your kit B1420 (SEAT-C90). Every hold, partition and housekeeping rule of the kit still binds you. Fix round 1 of 1 before a round-2 gate. HARD STOP 12:30 AEDT 2026-11-10.

## The product owner's ruling
Card composer-footer-look-1110, option b, 2026-11-10 09:07, verbatim: "Fix the shorter-name cut first, then land".

## What the gate found (read it WHOLE first)
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1420_verify/VERDICT.md`, findings F1 and F2, and its `evidence/` folder (the probe, the before/after PDFs).
- **F1 (to fix):** of 2,120 adversarial renders, 100 names already cut at main are cut 19-42 code units SHORTER at your head `de6e5615`. In 43 of them main's render was already sound (hash line on the page, page label whole, nothing running into it). Cause per the gate: `modelledFooterRows` returns Infinity for a piece wider than `footerColumn()` (the old fixed column, `change-report.ts:661` at head), while row filling now uses the wider `footerTextColumn` and the line breaker joins `W( W` into one piece, so a joined piece the writer would wrap cleanly is clipped instead. Re-print those lines yourself; the gate's reading is a claim.
- **F2 (to KEEP):** in 59 renders main breaks the page label into fragments ("Pag" / "e 1 o f 1"); your head prints a whole "Page 1 of 1" in all 59. That repair is wanted.

## The change
Make the model treat a piece wider than the column the way the writer does (hard wrap per its `findMaxFitLength` / `cloneInline` behaviour you already ported), measured against the same column the row filling uses, so that **a name is cut no shorter than the longest prefix for which the render is sound**: hash line on the page, page label whole, nothing running into the label. Only the files the kit OWNS.

## Prove it (in STATUS under `## ADDENDUM-1`)
1. Re-run the gate's own probe (copy it from `evidence/` into your tree's scratch area; do not edit the gate's folder) over the same 2,288 inputs at main, at `de6e5615`, and at your new head. Report by program:
   - the 43 sound-at-main cases: cut length at new head >= cut length at main, **43 of 43**;
   - all 100 F1 cases: none cut shorter than the longest sound prefix (say how you computed it);
   - label broken at new head: **0 of 2,288** (F2 kept);
   - hash line lost at new head: 0; label overlap: only the 2 pre-existing right-to-left cases (F4), unchanged;
   - renders whose first line is unchanged vs main: byte-equal (the gate's control).
2. One new test row that is RED at `de6e5615` on a named F1 case (e.g. the gate's `adv0005r` shape) and GREEN at your head.
3. The full test suite, lint and typecheck: counts and rc.
4. A plain-ASCII commit message (no B-number, seat id or name) ending with your attribution line; push the same branch.

## Last line
`READY B1420-2: <head sha40>` (equal to `git ls-remote` of the branch), or `STOPPED: NEEDS TUESDAY <one question>`.
