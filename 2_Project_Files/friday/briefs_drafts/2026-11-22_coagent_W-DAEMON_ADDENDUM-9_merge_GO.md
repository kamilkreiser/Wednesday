This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat W-DAEMON only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 9 (merge)" in your STATUS file; last line when done exactly `MERGED W-DAEMON`.

If your context was compacted while you waited: re-read your brief, addenda 1-9 and your STATUS file WHOLE before doing anything.

# W-DAEMON — ADDENDUM 9: merge GO for one exact SHA

## 1. What stands behind it
- Independent check: `VERDICT: GO WITH NOTES — head 5b008c8…` (no Blocker or Major). PC run 3 (WO-6) all green at `5b008c8`, including Ctrl-C twice. Your notes round `5b008c8..3337192`: Friday verified it changes no Rust code beyond the usage string, plus the kit's `EXPECTED` move (your run: `BUILT coagentd`).
- Friday's clean clone at `33371921670acfcb6fc7634d0c4eacafa9800a8d`: `scripts/check.sh` exit 0, 1,453 / 0 / 21 over 196 result lines; `scripts/red-controls-daemon.sh` exit 0, every row red as required, final clean run green. Scope against main `1aa4629` by SHA: 13 files, +2,643 −29; main an ancestor; Cargo files unchanged. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_w_daemon/`.

## 2. The GO
Merge GO for `33371921670acfcb6fc7634d0c4eacafa9800a8d`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `1aa4629b15881096b4a122da20bcbcb24bcf76a7`, `git ls-remote origin w-daemon` is still `33371921670acfcb6fc7634d0c4eacafa9800a8d`, your worktree clean. If either differs, or you made any commit since, STOP and say so.
2. `git push origin 33371921670acfcb6fc7634d0c4eacafa9800a8d:refs/heads/main` (fast-forward only; never force, never a merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS, write the last line, stop. Then move your tools root into the project's quarantine as your brief says, and report it. Nothing else.

Thank you: careful, honest work all the way through, especially the Ctrl-C diagnosis.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
