This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat WIN-IPC only. It opens ONE fix round after the independent check, on the owner's word. Report under "## ADDENDUM 1 (fix round)" in your STATUS file.

# WIN-IPC — ADDENDUM 1: the fix round after the check's NO GO

## 0. Before anything
Re-read WHOLE: your brief; your STATUS file; the check's verdict `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_WIN_IPC_verdict.md` (READ-ONLY; probes in `gate_win_ipc_tests/` beside it, READ-ONLY), sections 5, 6, 9, 11 and 12 above all. The checker read Microsoft's page for every Windows call you used: its quotes and URLs may be cited in your comments.

## 1. The authority
- The check: `VERDICT: NO GO — head e5e8633c530c28ebe632c0d149dbbd2f013560ea`. One Major (M-1), four Minors (m-1 to m-4), notes. Nothing changed for the Mac; every failure path it found refuses. Your three design questions were ruled acceptable (its section 11).
- The owner (Kam), card `general-c2c-win-ipc-check-nogo-1120`, verbatim: "a — One fix round, then a short re-check". This is the one round. A second NO GO goes back to him.
- The list below is CLOSED; all of it stays inside your owned paths (`crates/coagent-ipc/**`; the hook and MCP statements are NOT touched again). Anything beside it: write it down and STOP.

## 2. What to build (Windows code is still WRITTEN AND TYPE-CHECKED, NEVER RUN; say so everywhere)
1. **M-1: bind the client's server check to the pipe object, not to a process number.** As the verdict's section 12 describes: at bind, give the pipe an explicit owner in its security descriptor (`O:<own user SID>` before the DACL, `windows.rs` around :363-365); in `connect_expecting`, after `open`, read the pipe's OWNER through the client handle with `GetSecurityInfo(handle, SE_KERNEL_OBJECT, OWNER_SECURITY_INFORMATION, &mut owner, null, null, null, &mut sd)` (vendored `Security/Authorization/mod.rs:74`, constants as the verdict names; take every signature from the vendored source), turn it into text with `ConvertSidToStringSidW`, `LocalFree` the descriptor once, and require `check_peer_sid(owner, own) == Ok`. KEEP the existing process check as well: both must pass. Every `unsafe` block gets its `// SAFETY:` line; `GetSecurityInfo` returns an error code, not a BOOL (Microsoft's page, quoted in the verdict): check it as such. A failure of any step refuses.
   - What stays UNVERIFIED and goes into the README's first-run list: that a client handle opened read-write carries READ_CONTROL; that an account cannot set another account's SID as an object's owner without a restore privilege.
   - A never-run test: the client refuses a pipe whose owner is a made-up SID (expected identity passed in, as your existing test does).
2. **m-1:** in `peer_sid_different_is_refused_without_naming_either` (or beside it), an identifier that is a strict prefix of the other, both directions, refused. Show it kills the checker's mutant Q15 (prefix match) in a scratch copy; quote the failing line.
3. **m-2:** the ignored second-account test: role `owner` asserts `rejected_count() == 0`; role `second` also opens the pipe directly with `ClientOptions::new().open(..)` (no server check) and asserts the OS error is 5 (access denied); its doc says to copy the test program whose path `cargo test -p coagent-ipc --test win_pipe --no-run` prints to a folder the second account can read.
4. **m-3:** `tokio::task::yield_now().await;` after a rejected connection is dropped in `accept`, so a refused client reconnecting at full speed cannot keep the loop from yielding.
5. **m-4 and N-1 to N-4:** the three wrong limit texts (module notes, README, BACKLOG: the logon-session DACL does NOT cover the server check against a squatter); the README sentence on the name rule, replaced by the verdict's exact text; `MAX_PIPE_NAME`'s doc cites Microsoft's page (256 characters for the whole name; ours at most 209); add the verdict's first-run items 15 to 20 to the README list, word for word; wrap the same-user Windows tests' `accept` in `tokio::time::timeout` so a check that refuses everyone makes them FAIL, not hang; `rejected += 1` becomes `saturating_add(1)`.
6. NOT in this round: N-5 (an identity bound to the connection on the listener side), N-6, N-7. Append them to `BACKLOG.md` in the file's own form.

## 3. Then
1. Merge `origin/main` INTO the branch (never rebase). Main is now `16e83fbe5592658ddcda769d7827895941eca678`. `git diff --stat 2bba2a4 16e83fb -- crates/coagent-ipc crates/coagent-hook crates/coagent-mcp Cargo.toml Cargo.lock` must be empty (check; if not, STOP). Expected conflict: `BACKLOG.md` only.
2. On the merged head: the three Windows type-checks and three lint lines of your brief (light); your crate's red-control script; then ONE `scripts/check.sh` (before it, `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` below 3; a tool failure = FULL; the relay lane goes before you today).
3. Your brief's final checks (protected hashes, `unix.rs` untouched with its control, the foreign runner's text anchors start against end, `Cargo.lock` unchanged, scope, scan with control, push, ls-remote, ancestor, re-read main).

Last line when all is done, exactly: `READY FOR QA WIN-IPC r2`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
