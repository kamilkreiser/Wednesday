# B326 DRAFTER REPORT · MPS PR #86 fix round 2 of 2 · 2026-10-20 (clock 13:36:08 to 13:38:21 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B326_SEAT-V5R_mps-pr86-fix-round2.md` (zero stamp slots; ends `READ-WHOLE-BY-TUESDAY: PENDING`). Pane `Datasec/MPS-V5R`, Sonnet via `BRIEF_SEAT_LEVEL=sonnet`.

## Read whole
`B319_STATUS.md` (213 lines) plus a listing of its evidence folder (12 PNGs), the B313 builder brief, `B313_STATUS.md`, the B296 template, B318 lines 1-20, and B324 (its port block is 7470-7479).

## Measured (read verbs only)
- PR #86 head = `925caf8be234675d4193f293e3a528c82aeecb07`, **unmoved**, by `gh api` and by `ls-remote` (branch and `refs/pull/86/head`). It is open, not a draft, 18 files, mergeable_state clean, and 9 of 9 check-runs succeeded.
- main = `acfcf5dec5d40257c1b917ef750256b6f76d0e2e`, which is still #86's base.
- Open PRs: #85 `b451239` (28 files), #87 `61d81f4` (20), #88 `85fcfe06` (19). Each shares **0** paths with #86 (control: #86 against itself = 18). #88 changes `styles.css` and `QuoteScreen.tsx`, so the focus rule goes in `bom-v5.css`. #85 changes `api/types.ts` and `schema.ts`, but `PurchaseLineResult.code` is identical at both heads, so the B319-1 fix needs no contract change.
- Ports: all of 7440-7519 had 0 listeners (unfiltered control: 12). **Proposed block 7500-7509.** No brief mentions 75xx.
- Load at 13:38 was 8.67. There were no heavy slots and no B326 files.
- The gate's STATUS agrees with DELTA 294 on all four findings.

## Open questions (each with a recommendation)
1. **Jira.** B313 allowed comments, so the brief allows one comment each on -263 and -151 only. Recommendation: keep it that way.
2. **B319-4 has no RED test.** The gate said "none needed", so the brief uses a counting program with a control instead. Recommendation: accept.
3. **Pairing key.** The brief uses code plus section plus quantity. Recommendation: do not add a description match.
4. **Probe files.** The seat may copy B319's quarantined probe files. Recommendation: allow it, since B319 has finished.
5. **Browser check for the focus ring.** The brief makes it best-effort and leaves the real check to the round-2 gate. Recommendation: accept.
