This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-HOST-FIX only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in your STATUS file; last line when done exactly `MERGED AUDIT-HOST-FIX`.

If your context was compacted while you waited: re-read your brief, addenda 1 and 2 and your STATUS file WHOLE before doing anything.

# AUDIT-HOST-FIX ADDENDUM 2: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES` at `5b3a3959ef95c1240554d5aba38f62051a0b56ad` (no Blocker, no Major; one Minor, five Notes; 8,901 fault schedules, 0 problems): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_AUDIT_HOST_FIX_verdict.md`, read whole by Friday.
- Your merge of the scanner's head (addendum 1): head `9145840f24f23aff5b589044ce8aa8776283bdac`. Friday's proof in her own clone: its parents are exactly `5b3a395…` and `f193620…`; the checked sha to the merged head changes exactly the other side's 47 files; the scanner head to the merged head exactly your 11 paths; your 10 paths other than `BACKLOG.md` are blob-equal to the checked sha and the other side's 46 blob-equal to the scanner head; in `BACKLOG.md` your lines are 6 added, 0 removed, identical line for line to your lines at the checked sha.
- **The scanner has landed:** `origin/main` is now `f193620c14082df985cff3bb1b96d02575218811`, the second parent of your merged head. So your head already contains main and lands by fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `9145840`: `scripts/check.sh` exit 0 (fmt, clippy, test, deny); by program over its log: 221 result lines, all ok, 1,545 passed, 0 failed, 21 ignored = main's 1,537 plus exactly 8, each named (five `tests::fix2::` tests, `n4_an_unreadable_anchor_refuses_the_open`, the two `n2_` lock tests), none gone; `scripts/red-controls-audit-host.sh` exit 0: `names: 20 red controls`, `rows: 23 cfg rows`, `GREEN: 66 tests ok`, `RED CONTROLS OK`. Last line `MERGE CHECK OK audit-host-fix 9145840f24f23aff5b589044ce8aa8776283bdac`.
- Friday's own `git ls-remote` just before this was written: main `f193620c14082df985cff3bb1b96d02575218811`, audit-host-fix `9145840f24f23aff5b589044ce8aa8776283bdac`.
- **The check's Minor and Notes are NOT a further round on this branch.** They go to the lane AUDIT-HOST-NOTES (another seat, starting once you have landed). Do NOT edit anything for them: the SHA that merges is the SHA that was checked.

## 2. The GO
Merge GO for `9145840f24f23aff5b589044ce8aa8776283bdac`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `f193620c14082df985cff3bb1b96d02575218811`, `git ls-remote origin audit-host-fix` is still `9145840f24f23aff5b589044ce8aa8776283bdac`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>` and Friday sends the next steps).
2. `git push origin 9145840f24f23aff5b589044ce8aa8776283bdac:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED AUDIT-HOST-FIX` and stop. Nothing else.

Thank you: the three callers found where the plan named one, your own rule slip said plainly, and four interpretations put up to be judged instead of buried: the check agreed with all four.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
