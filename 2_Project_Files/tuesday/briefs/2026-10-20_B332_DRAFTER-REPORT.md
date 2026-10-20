# B332 DRAFTER REPORT · SEAT-G21 · MPS PR #86 gate round 2 of 2, tier 2 · 2026-10-20 ~14:29 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B332_SEAT-G21_mps-gate-pr86-round2-tier2.md` (91 lines; ends `READ-WHOLE-BY-TUESDAY: PENDING`). Port block **7540-7549**. Pane `Datasec/MPS-G21`, Sonnet (G2), launch line with `WED_USAGE_STOP=100` before `cockpit.sh` and `BRIEF_SEAT_LEVEL=sonnet`.

## Measured facts (2026-10-20 14:24:40-14:29:21 AEDT, read verbs only)
- `ls-remote`: branch = `refs/pull/86/head` = `2d18b6773bee26970ba97cbb13f4dedc5d21b47e`; main `1b32bbe6b3f21d019dd5dba7818d1b5032d2599f`; #85 `b451239b6fde…`; #88 `85fcfe06fd0a…`; `b332*` 0 (control `b313*` 1). All five objects present locally.
- `925caf8..2d18b67`: 3 linear commits (`89d17e0`, `710afc0`, `2d18b67`), 6 files under `web/src/screens/bom/`, +172/-3. The non-test change is one condition (`r.code === info.code &&`, `consolidatedBomModel.ts:39`) plus comments, and one CSS rule (`bom-v5.css:15-19`). PR total 20 files, +1766/-32.
- PRs by GET 14:25: #86 open, 7 commits, clean; #85 open clean (28 files); #88 open clean (19 files); #87 closed merged. Open: #88, #86, #85.
- Overlap of #86's 20 paths with main's move (`acfcf5d..1b32bbe`, 20 paths) = 0, with #85 = 0, with #88 = 0 (control: #86 against itself 20).
- Check-runs at `2d18b67`: 9 completed / 9 success. CodeQL: 4 analyses at `2d18b677`, results 0 each; open alerts on the PR ref 0.
- Ports: `lsof -iTCP:7540-7549 -sTCP:LISTEN` rc 1 (control: unfiltered 11 lines). Today's briefs name 7400-7539 and 7620-7629. 7540-7549 appears only as the end of B331's measured range, never as an assignment.
- Load: 14:24 `14.17 9.59 9.56`, 14:25 `9.05 8.94 9.32`. No heavy-slot dir existed at 14:25.
- Server code source: `PurchaseCalculator.cs:428` `Code = item?.Sku`; manual `Sku = m.Code` (`:416`). Client: inventory `row.sku` or manual `item.code` (`lineInfo.ts:20-22`).
- **Correction to my own fence:** for the merge prediction I ran `git merge-tree --write-tree` (rc 0 against main, #85 and #88). That form writes unreferenced tree objects into `2_Project_Files`'s object store (no ref, no working-tree change). That is not a pure read verb. The legacy stdout form would have written nothing. Disclosed here. Nothing else was written outside the two brief files.

## Corrections to the commission text
- "B326 … explains the 5-string difference": the gap 43 -> 47 is **4**. Five boundary strings span 43 -> 48 (`B326_STATUS.md:74-81`). The brief states it that way (T-e).
- B319's words scope was "4 touched component sources" (`B319_STATUS.md:148`). B326's was 11 non-test sources with more string kinds. That is a named rule difference, and the brief makes the gate judge on it.

## Open questions (each with a recommended answer)
1. **Path B render (dotnet + synthetic store) at load ~9-14?** It is heavy, but it is the only instrument for the over-blank risk on real server codes (T-a) and for B319-2's computed outline. **Recommend: YES, keep Path B**, gated at load1 < 8 with a slot. If it cannot be built, NOT RENDERED and B319-2 is judged on the rule.
2. **Mouse-click "Edit section" shows no `:focus-visible` ring: reopen B319-2?** **Recommend: NO, a Note**, if the keyboard path shows the ring. The round-1 FAIL was the keyboard user, and the rule is the project's own convention.
3. **B319-4 judgement rule.** **Recommend: FIXED** if the gate's own program reproduces 43 under B326's stated rule (or names each difference) and no strict string is missing from the builder's 81. The 47 vs 43 gap alone is not a finding when the rule difference is nameable.
4. **-262's best token while B319-3 is CARRIED?** **Recommend: GO WITH FINDINGS at most.** The Minor stands unfixed by ruling; it is not re-argued.
5. **Copying B319's quarantined probe and store-writer files into the gate's clone?** **Recommend: YES, copy only, never run in place, never `ctl-canary.txt`.** These are the round-1 instrument; B326 had the same exception.
6. **Semantic merge runs:** **Recommend:** a full typecheck/lint/test on #86 merged onto new main, plus a typecheck on #86 merged with #88 (which rewrites `QuoteScreen.tsx`). For #85, textual only (B319 ran its semantic merge green; the delta touches no `api/`). Also answer T-f by reading #88: can a closed `SectionFold` hide the focused section? That is a landing Note, not a #86 defect.
7. **Mutant sample:** **Recommend: m-b1, m-b2, and from the builder's set e1, e2, m6** (next to the fix, the focus the ring decorates, the leak guard), with m9 as the substitute.

READ-WHOLE-BY-TUESDAY: PENDING
