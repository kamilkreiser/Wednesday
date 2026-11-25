This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat DAEMON-NOTES only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 4 (merge)" in your STATUS file; last line when done exactly `MERGED DAEMON-NOTES`.

If your context was compacted while you waited: re-read your brief, addenda 1 to 4 and your STATUS file WHOLE before doing anything.

# DAEMON-NOTES ADDENDUM 4: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES` at `35b69bbae1ec50992e3121c1c6fa4b682b494620` (no Blocker, no Major; one Minor F1, six Notes): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_DAEMON_NOTES_verdict.md`, read whole by Friday's seat this morning.
- Your merges (addenda 2 and 3): head `a82b519ee7b7a942b6e40ce8d801dc760455384d`, parents `379daffd598f3a5ffc4945d51b76b351f9d483c5` and `1b1ac447041ea3df56384cd4547561ec076a3130` (read again by Friday now, with main `1b1ac44` an ancestor of it). The proof made in Friday's own clone at 10:17 today: the scanner-notes head to your merged head changes exactly your lane's 17 paths; your 15 non-document paths are blob-equal to the checked sha `35b69bb`; no path outside the 17 differs from the scanner-notes head; the outcomes document of the other side is a byte prefix of yours; in `BACKLOG.md` the 8 boxes your lane ticked are the only lines of the other side missing, and no line of yours is lost.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `a82b519`: `scripts/check.sh` exit 0; by program over its log: 230 result lines, all ok, 1,561 passed, 0 failed, 21 ignored = main's 1,548 plus exactly 13, each named (`a_changed_relay_certificate_is_named_in_status`, `a_dead_relay_fails_the_waiting_invitation_truthfully`, `a_forward_ack_clears_row_54s_clock`, `dn_mcp_wrong_argument_types_are_tool_errors_with_fixed_texts`, `empty_relay_url_or_pin_is_refused_at_start`, `g28_finding_a_joiner_open_before_the_create_gives_one_not_found_and_one_reconnect`, `hostile_peer_messages_and_key_exchanges_never_leave_a_wait_without_a_clock`, `link::tests::connect_with_no_candidate_names_why`, `run_and_main_both_call_the_gate_rule`, `stale_sentences_are_gone`, `tests::dn_wrong_argument_types_are_refused_with_fixed_texts`, `the_windows_gate_rule_refuses_only_on_windows`, `usage_shows_the_command_prompt_form`), none gone; `scripts/red-controls-daemon.sh` exit 0: 173 rows `RED (as required)`, 0 otherwise, `final clean run: green (66 test binaries; ignored under rulings: 2)`. Last line `MERGE CHECK OK daemon-notes a82b519ee7b7a942b6e40ce8d801dc760455384d`.
- Friday's own `git ls-remote` just before this was written: main `1b1ac447041ea3df56384cd4547561ec076a3130`, daemon-notes `a82b519ee7b7a942b6e40ce8d801dc760455384d`.
- **The check's Minor F1, its Notes and Open items and the permanent red rows are NOT a further round on this branch.** They are the next daemon lane, whose brief is written. Do NOT edit anything for them: the SHA that merges is the SHA that was checked.

## 2. The GO
Merge GO for `a82b519ee7b7a942b6e40ce8d801dc760455384d`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `1b1ac447041ea3df56384cd4547561ec076a3130`, `git ls-remote origin daemon-notes` is still `a82b519ee7b7a942b6e40ce8d801dc760455384d`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin a82b519ee7b7a942b6e40ce8d801dc760455384d:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED DAEMON-NOTES` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
