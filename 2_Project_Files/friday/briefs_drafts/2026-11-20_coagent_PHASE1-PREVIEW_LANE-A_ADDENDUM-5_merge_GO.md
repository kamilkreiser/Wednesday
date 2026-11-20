This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Lane A (P1P-GATE) only. It is the merge GO that addendum 4 said would follow Friday's own check. It changes no other rule. Report under "## ADDENDUM 5 (merge)" in `coagent/5_Project_History/STATUS_P1P_GATE.md`; last line when done exactly `MERGED P1P-GATE`.

If your context was compacted while you waited: re-read your brief, addenda 1-5 and your STATUS file WHOLE before doing anything.

# PHASE 1 PREVIEW, LANE A — ADDENDUM 5: merge GO for one exact SHA

## 1. What Friday checked herself (2026-11-20)
- In a clean clone at `b7e8da4a58daf37817936f947fa655c712ac19d1` (`friday/coagent_merge_check.sh`, short work dir, head.txt `head=want`): `scripts/check.sh` exit 0 ("CHECK OK"), 1,206 passed, 0 failed, 20 ignored (summed from the log by a program, 163 result lines); `scripts/red-controls-daemon.sh` exit 0: 129 rows "RED (as required)", final clean run green (36 test binaries; ignored under rulings: 2). Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_p1p_gate_r3/`.
- With read verbs in that clone: 30 paths changed against `main` (`32beb563837341560b908d9ba5b0a60de240d860`): 20 in `crates/coagent-daemon`, 4 in `crates/coagent-hook`, `docs/DAEMON.md`, `scripts/red-controls-daemon.sh`, `scripts/test-p1p.sh`, `BACKLOG.md`, root `Cargo.toml` (one member line, `crates/coagent-hook`) and `Cargo.lock` (the `coagent-hook` package and one `coagent-policy` dependency line; no new registry source). Nothing under the policy, roster, audit, relay, crypto or proto crates. The nine gate paths (`tests/gate`, `gate_r2.rs` to `gate_r6_model_wrapper.rs`, `gate_return.rs`, `tests/common`) have the same object ids as on `main`. `main` is an ancestor of your head. A scan of the 2,878 added lines for home or volume paths, the owner's names and both client names: 0 hits (planted control: 1).
- The independent check (GO WITH NOTES, `p1p_review/gate_P1P_verdict.md`) and its notes: P1-1, P1-2, P1-4, P1-5, P1-6, P1-8 in the tree (your addendum 1); P1-7, P1-9 in `BACKLOG.md`. Your `test-p1p.sh` and `test-daemon.sh` figures at this head are your own (not re-run by Friday).

## 2. The GO
Merge GO for `b7e8da4a58daf37817936f947fa655c712ac19d1`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `32beb563837341560b908d9ba5b0a60de240d860`, `git ls-remote origin p1p-gate` is still `b7e8da4a58daf37817936f947fa655c712ac19d1`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin b7e8da4a58daf37817936f947fa655c712ac19d1:refs/heads/main`. A fast-forward only: never force, never a new merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
