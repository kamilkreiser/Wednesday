This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat RELAY-RECONNECT only. It is the merge GO after the short re-check and Friday's own check. It changes no other rule. Report under "## ADDENDUM 6 (merge)" in `coagent/5_Project_History/STATUS_RELAY_RECONNECT.md`; last line when done exactly `MERGED RELAY-RECONNECT`.

If your context was compacted while you waited: re-read your brief, addenda 1-6 and your STATUS file WHOLE before doing anything.

# RELAY-RECONNECT — ADDENDUM 6: merge GO for one exact SHA

## 1. The short re-check
`VERDICT: GO WITH NOTES — head 104dd394c390b614410cdba76ac45eeffa6bb220` (`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_RELAY_RECONNECT_r2_verdict.md`). No Blocker, Major or Minor. Its notes are NOT for this round: R2-1 (no builder test for the `cmd_join` window; the checker's probe `qrr2_d` covers it) and R2-2 (property race reach) go to BACKLOG through the next lane that owns the daemon's tests.

## 2. What Friday checked herself (2026-11-21)
- Clean clone at `104dd39` (`friday/coagent_merge_check.sh`): `scripts/check.sh` exit 0, 1,335 passed / 0 failed / 21 ignored over 179 result lines (summed by program): your figure.
- `scripts/red-controls-daemon.sh`: every row RED as required, RR-A5 included. Its final clean pass failed ONE test, `model_relay_state_delivers_what_a_real_relay_process_delivers` (U-D4 differential, slot 1: model 41 items, real relay 40), under machine load. That test file is unchanged by your branch, your branch does not touch the relay crate or `recovery.rs`, it passed in the same check's `check.sh`, and it passed 5 of 5 run alone. Ruled: an existing timing-sensitive test on main, not your fault. Friday records it for BACKLOG; you do nothing about it.
- Scope against the remote's main `16e83fb`: 21 files, +5,328 −65; main is an ancestor; root `Cargo.toml`/`Cargo.lock` unchanged. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_relay_reconnect_r2/`.

## 3. The GO
Merge GO for `104dd394c390b614410cdba76ac45eeffa6bb220`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `16e83fbe5592658ddcda769d7827895941eca678`, `git ls-remote origin relay-reconnect` is still `104dd394c390b614410cdba76ac45eeffa6bb220`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin 104dd394c390b614410cdba76ac45eeffa6bb220:refs/heads/main`. A fast-forward only: never force, never another merge commit, never a rebase. Do not rely on the project folder's local `main` branch: push the SHA to the remote ref as written. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
