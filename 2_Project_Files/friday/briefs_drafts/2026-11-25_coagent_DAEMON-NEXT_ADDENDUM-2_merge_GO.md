This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat DAEMON-NEXT only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in your STATUS file; last line when done exactly `MERGED DAEMON-NEXT`.

If your context was compacted while you waited: re-read your brief, addenda 1 and 2 and your STATUS file WHOLE before doing anything.

# DAEMON-NEXT ADDENDUM 2: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES — head 3d87ecbcfb7bbae9c58ddb794e518fe1836c614d` (the verdict file's first line, read by Friday in this action; the file was read whole by Friday's earlier seat today): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_DAEMON_NEXT_verdict.md`.
- Your merge of main (addendum 1): head `bcaf1194ea268508cf92f135a60fe18076824a0f`. Friday's proof by program with read verbs in the project repository: its parents are exactly `3d87ecb…` and `0123cfc…`; the checked sha to the merged head changes exactly the other side's 33 files; `0123cfc` to the merged head exactly your 16 paths; your 12 paths other than the four shared files are blob-equal to the checked sha and the other side's 29 blob-equal to `0123cfc`; each of the four shared files is the `0123cfc` text plus exactly your lane's added lines in order, 0 removed (1563 + 44 = 1607, 307 + 45 = 352, 206 + 13 = 219, 295 + 15 = 310 lines).
- **Main is `0123cfc262419802bd4f122a2646fd7bcbb86b0a`** by Friday's own `git ls-remote` in this action: the second parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `bcaf119`: `scripts/check.sh` exit 0; by program over its log: 234 result lines, 1,577 passed, 0 failed, 21 ignored; against main's last check (1,574 passed, 1,592 test names) exactly 3 new test names and 0 gone: `the_guard_ends_as_before_when_its_reader_is_gone`, `a_relay_url_with_surrounding_blanks_is_used_trimmed`, `a_pin_that_is_not_a_fingerprint_names_no_usable_candidate`; `scripts/red-controls-daemon.sh` exit 0: 187 rows `RED (as required)`, 0 result lines otherwise, then `final clean run: green (68 test binaries; ignored under rulings: 2)`. Last line `MERGE CHECK OK daemon-next bcaf1194ea268508cf92f135a60fe18076824a0f`.
- **The check's Notes are NOT a further round on this branch.** Do NOT edit anything for them: the SHA that merges is the SHA that was checked.
- One thing for next time, no action now: in addendum 1 you made the merge commit with `core.hooksPath` pointed at `/dev/null`. You said so and that no hook exists, which is why it stands. Do not change a hook setting for a commit again without a `STOP Q<n>` first: an unasked change to how a commit is made is a question, even when it is harmless.

## 2. The GO
Merge GO for `bcaf1194ea268508cf92f135a60fe18076824a0f`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is `0123cfc262419802bd4f122a2646fd7bcbb86b0a`, `git ls-remote origin daemon-next` is still `bcaf1194ea268508cf92f135a60fe18076824a0f`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin bcaf1194ea268508cf92f135a60fe18076824a0f:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED DAEMON-NEXT` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
