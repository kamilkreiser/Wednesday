This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat WIN-IPC only. Report under "## ADDENDUM 2 (notes, then merge main)" in your STATUS file.

# WIN-IPC — ADDENDUM 2: the re-check's notes, then hold for the relay lane's merge

## 0. The authority
The short re-check: `VERDICT: GO WITH NOTES — head 329fb5f6324051a0d4a86d2c54884c3dfcddf508` (`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_WIN_IPC_r2_verdict.md`, READ-ONLY; read sections 9 and 10 WHOLE). M-1 is closed on paper; no Blocker or Major. The items below are the coordinator's rulings on its notes; the list is CLOSED and stays inside `crates/coagent-ipc/**` plus `BACKLOG.md`. Comments and docs only: NO code line changes.

## 1. What to do now
1. **r2-N1 (your DQ1 sentence): KEEP a sentence, corrected.** In the README server-check bullet replace "A real server of another account will usually show as OS error 5, not `PeerSidRejected`." with exactly: "A real server of another account will usually be refused by the owner check (`PeerSidRejected`); OS error 5 means the owner or the server's token could not be read." Leave first-run item 15 word for word (it only asks to record which refusal happens).
2. **r2-N2:** the `Drop` SAFETY line: say what is true (built only from a successful call; `LocalFree` of a null pointer does nothing), not "non-null".
3. **r2-N3:** a one-line comment at the null-descriptor guard (`windows.rs` ~:437): it is the refusal when `GetSecurityInfo` fails and leaves `sd` null; it is not redundant.
4. **r2-N4:** a one-line comment at `windows.rs` ~:649: the owner decision must go through `check_peer_sid` (the one tested comparison); never an inline compare.
5. **r2-m1:** BACKLOG entry in the file's own form: no test catches removal of the `yield_now` after a rejection; the verdict's suggested Windows test (current-thread runtime, a separate OS thread re-opening in a tight loop with a made-up expected identity, a 10 ms timer that must fire within 500 ms); first-run item 17 covers it by hand meanwhile.
6. Light checks only: the three Windows type-checks, the three clippy lines, `cargo fmt --check`, Windows rustdoc with `--document-private-items` and `-D warnings`. Commit, push. Do NOT run `check.sh` yet.

## 2. Then HOLD for the relay lane
Last line while holding, exactly: `IN PROGRESS: notes done at <sha>; holding for MERGED RELAY-RECONNECT`. Watch `git ls-remote origin main` every 5 minutes (or Friday's pointer to an ADDENDUM-3). The relay lane merges first because the owner is waiting on it and its final runs take about four hours; your merge-in is the cheap one.
When `main` has moved off `16e83fbe5592658ddcda769d7827895941eca678`:
1. Merge `origin/main` INTO the branch (never rebase). Expected conflict: `BACKLOG.md` only, both sides kept. `git diff --stat 16e83fb origin/main -- crates/coagent-ipc crates/coagent-hook crates/coagent-mcp Cargo.toml Cargo.lock` must be empty; if not, STOP.
2. On the merged head: the light checks of item 1.6, your crate's red-control script, then ONE `scripts/check.sh` (before it `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` below 3; a tool failure = FULL).
3. Your brief's final checks (protected hashes, `unix.rs` untouched with its control, `Cargo.lock` unchanged, scope, names scan with control, push, ls-remote, ancestor, re-read main).

Last line when all is done, exactly: `READY FOR MERGE CHECK WIN-IPC r3`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
