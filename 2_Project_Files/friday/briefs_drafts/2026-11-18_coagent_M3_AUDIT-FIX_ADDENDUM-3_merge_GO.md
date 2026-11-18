This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is the merge GO that addendum 1 said would follow Friday's own check. It changes no other rule. Report under "ADDENDUM 3 (merge)" in `coagent/5_Project_History/STATUS_M3_AUDIT_FIX.md`; last line when done exactly `MERGED M3-AUDIT-FIX`.

# M3_AUDIT-FIX — ADDENDUM-3: merge GO for one exact SHA

## 1. What Friday checked herself

In a clean clone at `e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d`: `scripts/check.sh` exit 0 ("CHECK OK", 886 passed, 0 failed, 18 ignored, summed from the log); `scripts/red-controls-audit.sh` exit 0 ("RED CONTROLS OK", green run 245 tests, no row not red). On the repository with read verbs: the diff from `393e7e45794b54793c08fa3c8eaf55b10abb2da7` (the head the independent check passed) names six files and nothing under `crates/coagent-audit/src`, no `build.rs`, no `Cargo.lock`, no gate file; `tests/qa_fix.rs` has the same sha256 as the check's own copy; the wrapper holds only the attributes, their justifications and the `mod` line; `main` (`c9a66534600e47fdd4a8da913df79d220086340b`) is an ancestor of your head; a scan of the added lines found no owner name, machine name, drive name or real path (with a positive control).

## 2. The GO

Merge GO for `e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `c9a66534600e47fdd4a8da913df79d220086340b`, `git ls-remote origin m3-audit-fix` is still `e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d:refs/heads/main`. A fast-forward only: never force, never a new merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused, STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
