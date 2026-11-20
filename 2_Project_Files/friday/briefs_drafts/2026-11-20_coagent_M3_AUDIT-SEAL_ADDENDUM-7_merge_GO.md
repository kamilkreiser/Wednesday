This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-SEAL only. It is the merge GO that addendum 4 said would follow Friday's own check. It changes no other rule. Report under "## ADDENDUM 7 (merge)" in `coagent/5_Project_History/STATUS_M3_AUDIT_SEAL.md`; last line when done exactly `MERGED M3-AUDIT-SEAL`.

If your context was compacted while you waited: re-read your brief, addenda 1-7 and your STATUS file WHOLE before doing anything.

# M3 AUDIT-SEAL — ADDENDUM 7: merge GO for one exact SHA

## 1. What Friday checked herself (2026-11-20)
- In a clean clone at `2bba2a468a5cce04f5d7189bdf76cbbecfbfab14` (`friday/coagent_merge_check.sh`, head.txt `head=want`, the runner on fresh target and log directories): `scripts/check.sh` exit 0 ("CHECK OK"), 1,253 passed, 0 failed, 21 ignored (summed from the log by a program, 167 result lines); `scripts/red-controls-audit.sh` exit 0: `rows: 173 cfg rows + 2 source-mutant rows`, 175 RED, 0 not red, `GREEN: 312 tests ok`, "RED CONTROLS OK". Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_audit_seal_r2/`.
- With read verbs in that clone: 22 paths changed against `main` (`d57f3a2ab6714acac3bb1bae7fbd58496adfbb20`), all in `crates/coagent-audit/`, `docs/AUDIT.md`, `BACKLOG.md`, `scripts/red-controls-audit.sh`; no change to root `Cargo.toml` or `Cargo.lock`; `main` is an ancestor of your head; `tests/qa_seal.rs` sha256 `dbfc1e200929bc17a7745db5e9d308b4479b28fc483ec6677d703c66550f0804` (the check's own); since the head the independent check passed (`841c445`) the only change under `src/` and `build.rs` is the red-control branch `seal_keeps_head_at_start` in `src/segment.rs` (the normal path keeps `h.author_seq > *n`) and its name in the list; `tests/seal_common/mod.rs` changed one line (`crate::common` to `super::common`) so the check's file compiles unedited; a scan of the 5,814 added lines for home or volume paths, the owner's names and both client names: 0 hits (planted control: 1).
- The independent check (GO WITH NOTES at `841c445`, `m1_review/gate_M3_AUDIT_SEAL_verdict.md`) and its notes: QS-1, QS-3, QS-5 and the probe file in the tree; the rest in `BACKLOG.md`. Your five release seeds are your own figures (not re-run by Friday).

## 2. The GO
Merge GO for `2bba2a468a5cce04f5d7189bdf76cbbecfbfab14`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `d57f3a2ab6714acac3bb1bae7fbd58496adfbb20`, `git ls-remote origin m3-audit-seal` is still `2bba2a468a5cce04f5d7189bdf76cbbecfbfab14`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin 2bba2a468a5cce04f5d7189bdf76cbbecfbfab14:refs/heads/main`. A fast-forward only (your head already contains `main`): never force, never another merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
