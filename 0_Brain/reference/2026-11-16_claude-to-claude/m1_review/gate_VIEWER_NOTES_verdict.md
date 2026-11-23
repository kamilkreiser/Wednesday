IN PROGRESS

# QA-VIEWER-NOTES — verdict (the follow-up lane `viewer-notes` of the local activity viewer)

Branch `viewer-notes`, head `b898a7c349a9f4094da56b5c0e3bf2a3a55c5440`, base main `039b9875b69918c2a83e95d84f7f8169358b59d5`. Independent check, 2026-11-23 from about 23:00, in my own clone under `/private/tmp/claude-501/qvn` (worktrees `h` = head, `m` = main; own target dirs and cargo home, toolchain LINKED as Friday's `coagent_merge_check.sh` does; `cargo fetch --locked` only). No model run, no Claude Code session; nothing pushed, merged or edited in the project; the only project file I write is my STATUS. Scripts and outputs: `m1_review/gate_viewer_notes_tests/`.

(BLUF is written last, above this line's section when done.)

## Head and base proofs (TESTED)
- `git ls-remote gh viewer-notes main` (GitHub remote, deploy key, from my clone): `039b9875b69918c2a83e95d84f7f8169358b59d5 refs/heads/main`, `b898a7c349a9f4094da56b5c0e3bf2a3a55c5440 refs/heads/viewer-notes`. Both fetched; `rev-parse gh/viewer-notes gh/main` = the same two SHAs; `git merge-base --is-ancestor 039b987 b898a7c` → exit 0 (true).
- Commits on the lane: `c1e0256` (the lane), `b898a7c` (la_fields_narrow reporting + a spaceless look-alike case). The project repo's LOCAL `main` is `18005d6`, an older commit (not an ancestor of 039b987: exit 1); not used.
- Builder's STATUS `STATUS_VIEWER_NOTES.md`: 172 lines, ends `head b898a7c…` / `READY FOR QA VIEWER-NOTES`. As the brief says.

## 1. Scope (TESTED)
- `git diff --name-status 039b987 b898a7c`: 9 paths, all M: `BACKLOG.md`, `crates/coagent-daemon/build.rs`, `src/watch.rs`, `tests/la_support/mod.rs`, `tests/la_viewer.rs`, `tests/la_wrap.rs`, `docs/DAEMON.md`, `docs/M0-OUTCOMES.md`, `scripts/red-controls-daemon.sh` (+1130/−47). Every one is on the brief's §6 owned list; a filter of the name list against the owned set leaves nothing. `activity.rs` not touched.
- Forbidden paths (policy, hook, MCP, CLI crates, `gate.rs`, `engine.rs`, `ipc.rs`, `main.rs`, `lib.rs`, `activity.rs`, `preview`, `spikes`, root `Cargo.toml`, `Cargo.lock`, `docs/POLICY.md`, `.gitattributes`, `tests/common`, `tests/p1p_support`): **0 bytes** two-dot and three-dot (run in bash, words split). Control: the same command on `docs/DAEMON.md` → 10,609 bytes.
- No Cargo file in the diff → no new dependency. `unsafe` in added lines: 0.
- Existing test files outside `tests/la_*`: `ls-tree -r` of every `*/tests/*` path, 237 entries at base and at head, **identical blob for blob** (control: `la_viewer.rs` blob `6a3b541` → `37d40ef`).
- No test function removed or renamed: the `fn <name>` set of every `la_*` file and of `watch.rs` at base is contained in the head's (0 missing; control: the reverse lists the new `la_restart_flapping`, `la_unreadable_answer`).
- `build.rs`, `red-controls-daemon.sh`, `BACKLOG.md`, `docs/M0-OUTCOMES.md`: 0 removed lines (append only); `build.rs` +3 names and a comment in `LA_RED`; red script +4 rows and a comment after the LA rows.
- **Removed lines of every `la_*` file and of `watch.rs`'s test module** (`git diff -U0`, every `-` line listed and judged): `la_support/mod.rs` 0; `la_viewer.rs` 3 (`:90` `e[0].contains(&format!("tool {EVIL_SHOWN}"))`, `:92` `e[1].contains(&format!("Claude Code mode: {EVIL_SHOWN}"))`, `:140` `e[0].contains("tool B\\u{1b}[2Jash\\u{d}\\u{a}#9 forged")`); `la_wrap.rs` 2 (`:220` `assert_eq!(f0[2], "tool Bash \\u{7c} Claude Code mode: plan", …)`, `:224` `f1[3], "Claude Code mode: auto \\u{7c} Claude Code mode: plan",`); `watch.rs` tests 1 (`:393` `"Bash \\u{7c} Claude Code mode: plan"`). Exactly the six of FR-B1, no seventh. Each is replaced by the same kind of assertion (`contains` stays `contains`, `assert_eq!` stays `assert_eq!`) on the same input; whether each new string is the EXACT new rendering is tested in item 3 below. The other removed lines of `watch.rs` are doc comments, the four changed constants, `field`'s body, the wrap loop and the `NoDaemon | Closed` arm (item 5).
