This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-HOST-NOTES only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 4 (merge)" in your STATUS file; last line when done exactly `MERGED AUDIT-HOST-NOTES`.

If your context was compacted while you waited: re-read your brief, addenda 1 to 4 and your STATUS file WHOLE before doing anything.

# AUDIT-HOST-NOTES ADDENDUM 4: merge GO for one exact SHA

## 1. What stands behind it
- The second independent check: `VERDICT: GO WITH NOTES` at `dbc9c0a9fad3b03fff3d723bf2e66eb376ac1913` (no Blocker, no Major, no Minor; seven Notes): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_AUDIT_HOST_NOTES_r2_verdict.md`, read whole by Friday.
- Your merge of the viewer head (addendum 3): head `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`. Friday's proof with read verbs in the project repository: its parents are exactly `dbc9c0a…` and `7a04ff0…`; the checked sha to the merged head changes exactly the other side's 34 files; the viewer head to the merged head exactly your 11 paths and no path outside them; your 10 paths other than `BACKLOG.md` are blob-equal to the checked sha and the other side's 33 blob-equal to the viewer head; `BACKLOG.md` is the viewer head's text plus your 24 lines in their order, 0 removed, none missing.
- **The viewer follow-up has landed: main is `7a04ff0166689d7937e5d1fc9e0028169ada7dd9`**, the second parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `debbb44`: `scripts/check.sh` exit 0; by program over its log: 232 result lines, all ok, 1,570 passed, 0 failed, 21 ignored = main's 1,564 plus exactly 6, each named (`m1_nb_each_property_is_red_on_a_mutated_copy`, `m1_nb_the_answer_table_names_every_answer`, `na_a_second_link_on_lock_or_anchor_refuses_the_open`, `na_an_archive_bundle_with_two_links_still_opens`, `tests::notes::nc_a_seal_reports_limits_changed_by_its_reopen`, `tests::notes::nd_a_seal_does_not_plan_while_dirty`), none gone; `scripts/red-controls-audit-host.sh` exit 0: `names: 23 red controls`, `rows: 26 cfg rows`, `GREEN: 72 tests ok`, `RED CONTROLS OK`. Last line `MERGE CHECK OK audit-host-notes debbb4442fc90b1d5c1f04f123a665dcd8cf381f`.
- Friday's own `git ls-remote` just before this was written: main `7a04ff0166689d7937e5d1fc9e0028169ada7dd9`, audit-host-notes `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`.
- **The second check's Notes are NOT a further round on this branch.** They go to the brief of the lane that wires the daemon by your table. Do NOT edit anything for them: the SHA that merges is the SHA that was checked.

## 2. The GO
Merge GO for `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `7a04ff0166689d7937e5d1fc9e0028169ada7dd9`, `git ls-remote origin audit-host-notes` is still `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin debbb4442fc90b1d5c1f04f123a665dcd8cf381f:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED AUDIT-HOST-NOTES` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
