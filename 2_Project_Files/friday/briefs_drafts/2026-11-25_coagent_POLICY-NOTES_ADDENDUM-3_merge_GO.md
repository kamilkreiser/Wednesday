This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-NOTES only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 3 (merge)" in your STATUS file; last line when done exactly `MERGED POLICY-NOTES`.

If your context was compacted while you waited: re-read your brief, addenda 1 to 3 and your STATUS file WHOLE before doing anything.

# POLICY-NOTES ADDENDUM 3: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES` at `b6af26c592ab2be1a5809e57bd602ad709c8ea11` (no Blocker, no Major; one Minor m-1, seven Notes): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_POLICY_NOTES_verdict.md`, read whole by Friday.
- Your merge of the audit head (addendum 2): head `7fc61882b6eed3245428d0e120714bd3b06e0c18`. Friday's proof with read verbs in the project repository: its parents are exactly `b6af26c…` and `debbb44…`; the checked sha to the merged head changes exactly the other side's 47 files; the audit head to the merged head exactly your 12 paths; your 10 non-document paths are blob-equal to the checked sha and the other side's 45 blob-equal to the audit head; both shared documents are the audit head's text plus your 30 and 12 lines in their order, 0 removed, none missing.
- **The audit follow-up has landed: main is `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`**, the second parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `7fc6188`: `scripts/check.sh` exit 0; by program over its log: 232 result lines, all ok, 1,574 passed, 0 failed, 21 ignored = main's 1,570 plus exactly 4, each named (`fixture_facts_are_the_hooks_facts`, `missed_agent_spellings_are_refused`, `odd_shell_inputs_are_not_owner_allowed`, `relative_cwd_is_refused_in_allow`), none gone; `crates/coagent-policy/red-controls.sh` exit 0: 74 rows `RED OK`, 0 `RED MISSING`, `RED CONTROLS: all 74 went red; normal build green`. Last line `MERGE CHECK OK policy-notes 7fc61882b6eed3245428d0e120714bd3b06e0c18`.
- Friday's own `git ls-remote` just before this was written: main `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`, policy-notes `7fc61882b6eed3245428d0e120714bd3b06e0c18`.
- **The check's Minor m-1 and its Notes are NOT a further round on this branch.** m-1's wording waits for the owner's answer to a card and is the first item of the next policy lane, with n-1 to n-4. Do NOT edit anything for them: the SHA that merges is the SHA that was checked.

## 2. The GO
Merge GO for `7fc61882b6eed3245428d0e120714bd3b06e0c18`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `debbb4442fc90b1d5c1f04f123a665dcd8cf381f`, `git ls-remote origin policy-notes` is still `7fc61882b6eed3245428d0e120714bd3b06e0c18`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin 7fc61882b6eed3245428d0e120714bd3b06e0c18:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED POLICY-NOTES` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
