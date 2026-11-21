This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-HOST only. It is the merge GO after the short re-check and Friday's own check. It changes no other rule. Report under "## ADDENDUM 3 (merge)" in `coagent/5_Project_History/STATUS_AUDIT_HOST.md`; last line when done exactly `MERGED AUDIT-HOST`.

If your context was compacted while you waited: re-read your brief, addenda 1-3 and your STATUS file WHOLE before doing anything.

# AUDIT-HOST — ADDENDUM 3: merge GO for one exact SHA

## 1. What stands behind it
- The short re-check: `VERDICT: GO WITH NOTES — head 680d333…` (M-1, M-2, M-3 closed by test); your notes round (ADDENDUM-2) at `1bf4f4e`, then main `26a4485` merged in at `1aa4629`.
- Friday's clean clone at `1aa4629b15881096b4a122da20bcbcb24bcf76a7`: `scripts/check.sh` exit 0, 1,440 / 0 / 21 over 193 result lines (your figure); `scripts/red-controls-audit-host.sh` exit 0, 14 rows red, green 58. Scope against the remote's main `26a4485` by SHA: 25 files, +7,421 −2; main is an ancestor; root `Cargo.toml` = one member line; `Cargo.lock` = one package block (14 lines added, 0 removed). Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_audit_host_r3/`.
- P-r2-1 is in BACKLOG, to be fixed before the daemon is wired (L8).

## 2. The GO
Merge GO for `1aa4629b15881096b4a122da20bcbcb24bcf76a7`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `26a44851df7cbbb785cae35ea9bdbc668005e894`, `git ls-remote origin audit-host` is still `1aa4629b15881096b4a122da20bcbcb24bcf76a7`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so.
2. Fast-forward `main` to exactly that SHA and push: `git push origin 1aa4629b15881096b4a122da20bcbcb24bcf76a7:refs/heads/main`. A fast-forward only: never force, never another merge commit, never a rebase. Do not rely on the project folder's local `main` branch. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
