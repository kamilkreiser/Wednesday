This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat W-KIT only. It is the merge GO after the independent check and Friday's own check. It changes no other rule. Report under "## ADDENDUM 5 (merge)" in `coagent/5_Project_History/STATUS_W_KIT.md`; last line when done exactly `MERGED W-KIT`.

If your context was compacted while you waited: re-read your brief, addenda 1-5 and your STATUS file WHOLE before doing anything.

# W-KIT — ADDENDUM 5: merge GO for one exact SHA

## 1. What Friday checked herself (2026-11-21)
- Against the remote's main `104dd394c390b614410cdba76ac45eeffa6bb220`, by SHA: 5 files, +527 −0, all in `scripts/windows/**`, `preview/demo/windows.md`, `BACKLOG.md`; the filtered proof over crates, Cargo files, the toolchain file, `deny.toml`, `scripts/check.sh` and `env.sh` is empty; main is an ancestor; `Cargo.lock` unchanged; names scan of the added lines: exactly the one ruled constant.
- A clean clone at `a034263` with Friday's own tools root: `build.sh` exit 0 (70 s); `coagent` 2,841,600, `coagent-hook` 580,096, `coagent-mcp` 845,824 bytes (your sizes); `coagentd` NOT BUILT as expected; `file` says PE32+ x86-64 for MS Windows for all three; `shasum -c` OK; a byte search (ASCII and UTF-16) of the three files for this machine's folder and drive names: 0 hits. Evidence: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_w_kit_r2/`.
- The check's notes 2, 3 and 4 are applied as ruled. Thank you for the measured reason the wrapper was needed (cargo splits RUSTFLAGS at the folder name's spaces).

## 2. The GO
Merge GO for `a034263b474d775d0e965e6234d7a446efc45425`, and for no other SHA.

1. Confirm first: `git ls-remote origin main` is still `104dd394c390b614410cdba76ac45eeffa6bb220`, `git ls-remote origin w-kit` is still `a034263b474d775d0e965e6234d7a446efc45425`, and your worktree is clean at that head. If either differs, or you have made any commit since, STOP and say so: this GO does not cover it.
2. Fast-forward `main` to exactly that SHA and push: `git push origin a034263b474d775d0e965e6234d7a446efc45425:refs/heads/main`. A fast-forward only: never force, never another merge commit, never a rebase. Do not rely on the project folder's local `main` branch. If the push is refused (main moved), STOP and quote the refusal.
3. Record in STATUS the output of `git ls-remote origin main` after the push, then write the last line and stop. Nothing else: no further commit, no tag, no branch deletion, no deploy, no publish. The duplicate cache in `$COAGENT_TOOLS/xwin-cache` stays where it is: Friday handles it.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
