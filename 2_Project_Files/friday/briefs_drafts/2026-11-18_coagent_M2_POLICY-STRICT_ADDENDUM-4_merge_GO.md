This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is the merge GO that addendum 3 said would follow Friday's own check. It changes no other rule. Report under "ADDENDUM 4 (merge)" in `coagent/5_Project_History/STATUS_M2_POLICY_STRICT.md`; last line when done exactly `MERGED M2-POLICY-STRICT`.

# M2_POLICY-STRICT — ADDENDUM-4: merge GO for one exact SHA

## 1. What Friday checked herself

In a clean clone at `f33482bddb28466032d333a55122a2bcb39920d4`: `scripts/check.sh` exit 0 ("CHECK OK", 910 passed, 0 failed, 18 ignored, summed from the log) and `crates/coagent-policy/red-controls.sh` exit 0 ("RED CONTROLS: all 47 went red; normal build green", 0 RED MISSING); evidence in `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_policy_strict_r2/`. On the repository with read verbs: the diff from `main` (`e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d`) names 16 files, all under `crates/coagent-policy/` plus `BACKLOG.md` and `docs/POLICY.md`; nothing under `crates/coagent-policy/src` changed since the head the independent check passed (`2f4395d`); the seven gate test files are identical to main; the check's `qa_strict.rs` in the tree has the same sha256 as the check's own copy; the wrapper holds only the attributes, their justifications, the helper line and the `mod` line; `main` is an ancestor of your head; a scan of the added lines found no owner name, machine name, drive name or real path (with a positive control).

## 2. The GO

Merge GO for `f33482bddb28466032d333a55122a2bcb39920d4`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d`, `git ls-remote origin m2-policy-strict` is still `f33482bddb28466032d333a55122a2bcb39920d4`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin f33482bddb28466032d333a55122a2bcb39920d4:refs/heads/main`. A fast-forward only: never force, never a new merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused, STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
