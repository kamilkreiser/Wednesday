This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-HOST only. Report under "## ADDENDUM 2 (notes, then merge main)" in your STATUS file.

# AUDIT-HOST — ADDENDUM 2: the re-check's notes, then hold for WIN-IPC's merge

## 0. The authority
The short re-check: `VERDICT: GO WITH NOTES — head 680d3333c8713fc12f140068b2a3a985d96c4681` (`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_AUDIT_HOST_r2_verdict.md`, READ-ONLY; read sections 4, 7 and 12 WHOLE). M-1, M-2 and M-3 are closed by test, and nothing else changed. The list below is the coordinator's ruling on its notes: CLOSED, docs and BACKLOG only, NO code line changes, inside your owned paths.

## 1. What to do now
1. **P-r2-1 (pre-existing Minor, identical at 35f7e89):** a BACKLOG entry in the file's form. Where: `mutate` → `reopen` (`host.rs:1120`, `:910`, `:919`). Symptom: after a P-4 re-open whose own second write fails, a record that LANDED is answered with an Err, and a caller that retries records it twice (two failures in one call, for example a full disk). Fix sketch: compute `landed` even when the re-open's later steps fail, and test it. Why deferred: pre-existing; to fix BEFORE the daemon is wired (L8). Discovered: QA-AUDIT-HOST-R2, probe `qa2_p4_then_a_second_write_fails_in_the_reopen`.
2. **N-r2-1 (docs):** in `docs/AUDIT-HOST.md` §3's P-4 bullet (around `:55-59`) and in `apply`'s doc comment, one sentence each: an `Err(LimitsChanged { .. })` may carry a successful answer, so unwrap `answer` and never retry on it blind. Qualify the "never records it twice" promise with a pointer to the P-r2-1 entry until that is fixed. (A doc comment is the one non-docs file touch allowed: comment lines only.)
3. **N-r2-2:** a BACKLOG entry: `release`'s Ok branch returns early through `?` (`host.rs:1188-1189`) without clearing `pending_held` or saving current; unreachable unless the dry and real release bundles differ.
4. Light checks only: `cargo fmt --check`, `cargo clippy -p coagent-audit-host --all-targets -- -D warnings`, the crate's tests without the two long ones. Commit, push.

## 2. Then HOLD for WIN-IPC
Last line while holding, exactly: `IN PROGRESS: notes done at <sha>; holding for MERGED WIN-IPC`. You merge AFTER WIN-IPC because WIN-IPC's check requires `Cargo.lock` byte-identical to its start, and you are the one lane that changes it. Main is now `a034263b474d775d0e965e6234d7a446efc45425` (relay-reconnect + W-KIT); POLICY-MODE and WIN-IPC merge next. Watch `git ls-remote origin main` every 5 minutes, or wait for Friday's pointer.
When main contains WIN-IPC (Friday will say, or `git log origin/main` shows the win-ipc head):
1. Merge `origin/main` INTO the branch (never rebase). Expected conflicts: `BACKLOG.md` (keep both sides) and possibly root `Cargo.toml` / `Cargo.lock`. If `Cargo.lock` conflicts, regenerate it with `cargo generate-lockfile --offline` only if it adds back your one package and changes nothing else (show `git diff origin/main -- Cargo.lock` = your one `[[package]]` block); otherwise STOP.
2. On the merged head, once each: `scripts/check.sh`; `scripts/red-controls-audit-host.sh`. Before each, `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` must print below 3.
3. Your brief's final checks (protected hashes, the 4 tree hashes, root Cargo diffs against main = your one member line and one package, no crate depends on yours, `seal_record` absent with control, scope, names scan with control, push, ls-remote, ancestor, re-read main).

Last line when all is done, exactly: `READY FOR MERGE CHECK AUDIT-HOST r3`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
