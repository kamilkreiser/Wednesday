This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat SCANNER-NOTES only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in your STATUS file; last line when done exactly `MERGED SCANNER-NOTES`.

If your context was compacted while you waited: re-read your brief, addenda 1 and 2 and your STATUS file WHOLE before doing anything.

# SCANNER-NOTES ADDENDUM 2: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES` at `430dde30be41e026b909e271f698f8013325e892` (no Blocker, no Major; one Minor, three Notes): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_SCANNER_NOTES_verdict.md`, read whole by Friday.
- Your merge of main (addendum 1): head `1b1ac447041ea3df56384cd4547561ec076a3130`. Friday's proof in her own clone: its parents are exactly `430dde3…` and `9145840…`; the checked sha to the merged head changes exactly main's 11 files; main to the merged head exactly your 11 paths; your 10 paths other than `BACKLOG.md` are blob-equal to the checked sha and main's 10 blob-equal to main; in `BACKLOG.md` your lines over main are 5 added, 0 removed, identical to your lines at the checked sha.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `1b1ac44`: `scripts/check.sh` exit 0 (fmt, clippy, test, deny); by program over its log: 222 result lines, all ok, 1,548 passed, 0 failed, 21 ignored = main's 1,545 plus exactly 3, each named (`r1_cr_runs`, `r2_three_views`, `r5_flag_forms`), none gone; `scripts/red-controls-scanner.sh` exit 0: `names: 21 red controls`, `rows: 21 cfg rows`, `GREEN: 28 tests ok`, `RED CONTROLS OK`. Last line `MERGE CHECK OK scanner-notes 1b1ac447041ea3df56384cd4547561ec076a3130`.
- Friday's own `git ls-remote` just before this was written: main `9145840f24f23aff5b589044ce8aa8776283bdac`, scanner-notes `1b1ac447041ea3df56384cd4547561ec076a3130`.
- **The check's Minor and Notes are NOT a further round on this branch.** They go to a later scanner lane. Do NOT edit anything for them: the SHA that merges is the SHA that was checked.

## 2. The GO
Merge GO for `1b1ac447041ea3df56384cd4547561ec076a3130`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `9145840f24f23aff5b589044ce8aa8776283bdac`, `git ls-remote origin scanner-notes` is still `1b1ac447041ea3df56384cd4547561ec076a3130`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin 1b1ac447041ea3df56384cd4547561ec076a3130:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED SCANNER-NOTES` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
