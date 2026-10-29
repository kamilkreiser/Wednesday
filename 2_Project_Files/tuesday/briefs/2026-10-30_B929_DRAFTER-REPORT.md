STARTABLE: YES (after your stamp; two existing test rows must change for the fix to exist at all, see Q-1)

# B929 drafter report (2026-10-30 about 10:20 to 10:50 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B929_SEAT-H60_hpsmpoc-357-401-primitives-overflow.md` (139 lines; 9 four-underscore lines = 8 slots + the last line, by `grep -c -E '_''_''_''_'`, control scratch file 1; at-sign slot pattern 0; non-ASCII lines 0 by `LC_ALL=C grep -c '[^ -~]'`). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, Jira GET through the 10:15 sweep's reader, no `cd`, no ref written, no message. Nothing written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H60` (Sonnet, row C2 line 92; gate G2 line 109) branches `b929/hpsmpoc-357-401-primitives-overflow` off main `e21d8044` and edits only `customer/parts.tsx`, `ui/Table.tsx`, `partner/parts.tsx` and their three tests: let `StagePill` wrap (-357, B908-7) and narrow the shared table look below `md` (-401), every export and signature unchanged. It measures with copies of the gates' own probes (B760 at 360, B908 at 390 with 1 px letter spacing, B913's 360-cell crawl) against TWO references: `e21d8044` and `9659148c` (the "main" of -401).

## Facts re-measured (instrument; control)
- main `e21d8044`, parent `94274a75` (#241), whose parent is `9659148c` (#240): `commits/<sha>` GETs. Open PRs 0. `matching-refs/heads/b929` 0 (control `heads/b9` 9 refs). Panes `%0 tuesday`, `%1 fleet-monitor`. Load1 1.71 at 10:26. Ports 9610-9619: `lsof` 0; kit word scan `961[0-9]` 0 files (control `979[0-9]` 1); `HPSM-POC-H60` 0 (control H53 17).
- Lines at `e21d8044` (tarball): `StagePill` 65, nowrap span 67 (nowrap count 2 incl. `RelationshipPill` 73); `thClass` 6, `tdClass` 7, `trClass` 8, `rowHeadClass` 10; the `BarChart` table 135-152. Importers of `ui/Table`: `partner/parts.tsx`, `DesignSystemScreen.tsx`, its test. `StagePill` users: CustomerManagement, EngagementsList, EngagementOverview (3), FirmwareTask, DesignSystemScreen.
- Diff `9659148c` vs `e21d8044`: `StatusPill` (frozen `ui/Tag.tsx`) went `font-semibold` -> `font-bold`, `py-0.5` -> `py-1`; the `BarChart` table moved to `px-3` + uppercase `tracking-wider` heads. Hence the likely split: register/engagements cells = bolder pill in a nowrap wrapper; Revenue +93.4 and design-system +3.5 = the table constants (UNMEASURED per column).
- Pinning rows: `customer/parts.restyle.test.tsx:19` "still never wraps its label" expects `whitespace-nowrap`; `ui/Table.test.tsx:14` expects `px-3` and `tracking-wider` tokens in `thClass`; `ui/restyle.contrast.test.ts:99` parses `thClass` as a double-quoted literal (not in the lane: it must stay green unchanged).
- Gates' instruments read and hashed: `.tools/b913/probe5.cjs` + `lib.cjs` (port assert 9920-9929, require from `wt-b913-merge`), `.tools/b908/scratch/crawl.mjs` lines 64-86, `.tools/b760/scratch/probe.cjs` lines 19-26.

## D-decisions (in the kit)
- D-1: two references: `e21d8044` for -357/B908-7, `9659148c` for -401; the probe must reproduce B913's 20 values first (control).
- D-2: FIX branch only; any cell not movable inside the three files (e.g. needs `Tag.tsx` or a page) is named as residue for your "recorded as accepted" call.
- D-3: exactly two existing test rows change (above); everything else byte-equal.
- D-4: no new Playwright spec; browser proof is the seat's uncommitted probe.
- D-5: READY 180 min, hard stop 300.

## Q-questions for Tuesday (each with a default)
- Q-1: May the seat change the two pinning rows (`parts.restyle.test.tsx:19-22`, `Table.test.tsx:14`)? Default **YES**: both files are in the sweep's YOURS, and -357 cannot be met while a row pins `whitespace-nowrap`.
- Q-2: No committed browser row for 360 / 390-ls1 / the 20 cells? Default **YES, none** (the every-lane rule); the gate re-measures.
- Q-3: If the 1024 register cells (+4.5 px) are not recovered by the `StagePill` change because the cause is `StatusPill` bold in frozen `Tag.tsx`: residue to you, not a `Tag.tsx` edit? Default **YES, residue**.
- Q-4: Gate round: NO GO 0 of 2 on class "a shared primitive that widens content" (B913-1's class)? Default **YES**.

## Sweep pointers found WRONG or incomplete
- -401's "main" is `9659148c`, not today's main (which already contains #241). The sweep's seed says "no further right than main" without naming the tree.
- -357's Done-when includes the UAT site: unreachable in a no-deploy lane; the kit makes it NOT TESTED.
- The /design-system cell's table lives in `DesignSystemScreen.tsx` (not in H3's YOURS); only class changes in `Table.tsx` can move it.
- Line anchors in the sweep (65, 67, 6-8) are correct.

## UNMEASURED
Whether -357 and B908-7 still reproduce at `e21d8044` (B913 did not measure 360 or letter spacing); per-column attribution; whether the fixes reach every cell; unit and e2e counts.

## Outside-the-fences disclosure
None breached. Scratch only under `scratchpad/drafters/b929/` (two web tarballs extracted, the Jira read, one control file). Read but did not modify the gates' `.tools/b913`, `b908`, `b760` probe files (the kit names them as copy sources).
