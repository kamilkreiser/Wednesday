This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat WIN-FOLLOWUP only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 6 (merge)" in your STATUS file; last line when done exactly `MERGED WIN-FOLLOWUP`.

If your context was compacted while you waited: re-read your brief, addenda 1-6 and your STATUS file WHOLE before doing anything.

# WIN-FOLLOWUP — ADDENDUM 6: merge GO for one exact SHA

## 1. What stands behind it
- Independent check: `VERDICT: GO WITH NOTES — head cf41a77…` (no Blocker or Major). Its Minor M-1 and Notes N-1, N-2, N-4 were fixed in your notes round (ADDENDUM 4); N-3 is in BACKLOG.
- Three PC runs, all passed: WO-8 at `97ccf0d`, WO-9 at `cf41a77`, WO-10 at `a074aca` (the candidate test ok on Windows with its 5 s budget; relay 125 passed and 5 ignored, summed from the result lines).
- Friday's clean clone at `a074aca0b544ff6fa7dbaf186c6436f7010d207b`: `scripts/check.sh` exit 0, 1,461 passed / 0 failed / 21 ignored over 197 result lines (main `3337192`: 1,453 / 0 / 21 over 196; +3 `win_rules`, +5 `win_guards`, +1 line); `scripts/red-controls-daemon.sh` exit 0, 154 rows red as required, final clean run green.
- Your head `3164374a8a20d73296558997438b97a41a7837ad` is `a074aca` plus one commit of four `.md` files (+44 −13; 0 other paths). Friday's own grep at that head found no code, script or build file that reads any of the four. So the clean-clone check stands for it.
- Scope against main `3337192` by SHA: 15 files, +1,499 −112; Cargo files unchanged (0 bytes); main an ancestor. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_win_followup/`.

## 2. The GO
Merge GO for `3164374a8a20d73296558997438b97a41a7837ad`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `33371921670acfcb6fc7634d0c4eacafa9800a8d`, `git ls-remote origin win-followup` is still `3164374a8a20d73296558997438b97a41a7837ad`, your worktree clean. If either differs, or you made any commit since, STOP and say so.
2. `git push origin 3164374a8a20d73296558997438b97a41a7837ad:refs/heads/main` (fast-forward only; never force, never a merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS, write the last line, stop. Nothing else.

Thank you: fast, exact and honest work, and the stops you did not need were the right ones to be ready for.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
