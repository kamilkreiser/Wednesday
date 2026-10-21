# B441 drafter report (read-only drafter, 2026-10-22 ~09:40 AEDT)

**Kit:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B441_SEAT-G34_hpsmpoc-b438-header-gate-tier2.md` (cloned from the B435 gate: sections, standing lines, REFUSE, STATUS protocol, launch line).

## Measured by the drafter (read verbs only)
- `ls-remote origin`: main `01dd9e4b4d9225999a2830343b1d4bf9f29966ac`; `refs/heads/b438/uat-header-compact-to-md` `c1a245f894edefc616f722449e4b963abb36c26b` (= the builder's READY sha); `b429/telemetry-224` (B440) `39d4d1a25294bf5059cf7a088ac3e7ca5fd8efcf`; no `b441*`.
- `rev-list --count main..head` = 1; `diff --stat main...head` = `AppShell.tsx` (+6/-5) and new `AppShell.compact.test.tsx` (+103); only UAT arms and one JSX comment changed (diff read). Load1 1.90 at 09:38.
- `.tools/` has `b198 b435 b438 b440 wt-b435-* wt-b440-*`, no `*b441*`.
- Model row: tier-2 gate row is **G2** (`model-routing.md:109`; G1 at :108 is tier 1/Opus). Kit line: `model claude-sonnet-5-5 -- G2`.

## Design choices
- Sweep widths: the brief's sample (320, 360, 390, 640, 664, 672, 700, 767, 768, 1280) is a floor; I added the builder's 33-width grid so the 17/132, 47/132, 4/132 counts and the B438-N1 list are reproduced row by row. Ref `35b2b73` and main `01dd9e4` are both built as references.
- Own mutant: gate chooses one of four (brand-group gap, nowrap removed, text-sm base, md to lg); nowrap-only survivor is classed as real-browser-only, not a defect.
- Ports 8110-8114 used; 8090-8099 must be free (STOP if B438's seat still listens); 8100-8109 named as B440's. Partition spelled from both sides; B440 priority on load.
- Severity: B438-N1 rows are Notes per ADDENDUM-1; an undisclosed extra residual row is Minor, a regression vs `01dd9e4` is Blocker.

## Open items for Tuesday
1. Stamp slots left `____`: stamp time, heads, hard stop (proposed 12:30, target 11:30), rulings, launch authority.
2. B438's commit message still says "PARTIAL, STOPPED"; kit makes it a Minor/Note only. Say if you want it ignored.
3. B438 is not yet confirmed idle (ports 8090-8099 / `.tools/b438`): the kit STOPs if a listener is there. Not checked by the drafter (no lsof run).
4. No PR existed per B438 STATUS; the kit re-reads it at start (`gh` GET), not measured by the drafter.
