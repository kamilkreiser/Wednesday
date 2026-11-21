This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-MODE only. It is the merge GO after Friday's own checks. It changes no other rule. Report under "## ADDENDUM 7 (merge)" in `coagent/5_Project_History/STATUS_POLICY_MODE.md`; last line when done exactly `MERGED POLICY-MODE`.

If your context was compacted while you waited: re-read your brief, addenda 1-7 and your STATUS file WHOLE before doing anything.

# POLICY-MODE — ADDENDUM 7: merge GO for one exact SHA

## 1. What Friday checked herself (2026-11-21)
- r3 (16:09): clean clone at `4b3c627`: check.sh 1,322 / 0 / 21 over 174; the 60-row policy runner all red, normal build green.
- r4 (18:54-20:03): clean clone at `1f58dce`: `scripts/check.sh` exit 0, 1,370 passed / 0 failed / 21 ignored over 184 result lines (summed by program) = your figure. Scope against the remote's main `a034263` by SHA: the same 14 owned paths, +2,335 −6; main is an ancestor; `Cargo.lock` unchanged. The policy crate is unchanged since the r3 runner check. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_policy_mode_r4/` (and `…_r3/`).
- The owner's ruling b on the second check's NO GO (M-1b written down as a known limit, pinned by a test, the fix carried to the switch-on lane) is what this merge carries. The mode stays dark: nothing a person can switch on.

## 2. The GO
Merge GO for `1f58dce5da8e7d189e699ba70eff4b8a18ec46e9`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `a034263b474d775d0e965e6234d7a446efc45425`, `git ls-remote origin policy-mode` is still `1f58dce5da8e7d189e699ba70eff4b8a18ec46e9`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin 1f58dce5da8e7d189e699ba70eff4b8a18ec46e9:refs/heads/main`. A fast-forward only: never force, never another merge commit, never a rebase. Do not rely on the project folder's local `main` branch. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
