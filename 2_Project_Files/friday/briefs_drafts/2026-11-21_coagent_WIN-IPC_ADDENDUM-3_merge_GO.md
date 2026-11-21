This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat WIN-IPC only. It is the merge GO after the short re-check, the owner's PC runs and Friday's own check. It changes no other rule. Report under "## ADDENDUM 3 (merge)" in `coagent/5_Project_History/STATUS_WIN_IPC.md`; last line when done exactly `MERGED WIN-IPC`.

If your context was compacted while you waited: re-read your brief, addenda 1-3 and your STATUS file WHOLE before doing anything.

# WIN-IPC — ADDENDUM 3: merge GO for one exact SHA

## 1. What stands behind it
- The short re-check: `VERDICT: GO WITH NOTES — head 329fb5f…`; your notes round (ADDENDUM-2) done at `b8aa8b7`.
- **Your Windows code RAN on the owner's PC** (2026-11-21, Friday's work order WO-1, at `b8aa8b7`): `cargo test -p coagent-ipc` 26 passed / 0 failed / 1 ignored (the second-account test); 1,000 round trips, median 241 µs; README first-run items 3, 4, 7, 8, 10, 13, 14, 21 PASS; item 16 CONFIRMS the first check's M-1 on real Windows (the pid calls report the dead creator), and item 22's one-account stand-in refused every foreign owner SID (os error 1307). Two notes for the next lane, not for you: a same-user process can create a further pipe instance (item 3), and `accept` can hand over an already-closed connection first (item 18). Results: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/2026-11-21_WO-1_results.md`.
- Friday's clean clone at `26a44851df7cbbb785cae35ea9bdbc668005e894`: `scripts/check.sh` exit 0, 1,382 / 0 / 21 over 186 result lines; `crates/coagent-ipc/red-controls.sh` exit 0; scope against main `1f58dce` by SHA: 13 files, +1,673 −90; main an ancestor; `Cargo.lock` unchanged; `unix.rs` unchanged. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_win_ipc_r3/`.

## 2. The GO
Merge GO for `26a44851df7cbbb785cae35ea9bdbc668005e894`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `1f58dce5da8e7d189e699ba70eff4b8a18ec46e9`, `git ls-remote origin win-ipc` is `26a44851df7cbbb785cae35ea9bdbc668005e894` (push it first if your own runs are done and green; if your head differs from that SHA in any way, STOP and say so: this GO does not cover it), and your worktree is clean.
2. Fast-forward `main` to exactly that SHA and push: `git push origin 26a44851df7cbbb785cae35ea9bdbc668005e894:refs/heads/main`. A fast-forward only: never force, never another merge commit, never a rebase. Do not rely on the project folder's local `main` branch. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
