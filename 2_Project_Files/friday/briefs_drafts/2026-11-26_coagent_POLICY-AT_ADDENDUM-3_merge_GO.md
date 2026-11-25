This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-AT only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 3 (merge)" in your STATUS file; last line when done exactly `MERGED POLICY-AT`.

If your context was compacted while you waited: re-read your brief, its addenda and your STATUS file WHOLE before doing anything.

# POLICY-AT ADDENDUM 3: merge GO for one exact SHA

## 1. What stands behind it
- The second independent check: `VERDICT: GO WITH NOTES — head 85565bd7283f94345c71f95c65a85d981b8f3726`: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_POLICY_AT_r2_verdict.md` (Friday read its lines 1 to 22 and 176 to 241).
- Your merge of the audit wiring head (addendum 2): head `2004a04ebba7e1d031dfa341da26f76693345aff`. Friday's proof by program with read verbs in the project repository: its parents are exactly `85565bd…` and `5e11609…`; the checked sha to the merged head changes exactly the other side's 20 files; `5e11609` to the merged head exactly your 10 paths; 0 bytes of difference from the checked sha under the policy crate and `docs/POLICY.md`; the two shared documents are `5e11609`'s text plus your lane's added lines, 0 removed (26 and 20 added).
- **The audit wiring lane has landed: main is `5e11609cee1cb483bd006547e9092d49522691cc`** by Friday's own `git ls-remote` in this action: the second parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home; the fixture variable unset, the clone under `/private/tmp`) on `2004a04`: `scripts/check.sh` exit 0; by program over its log: 244 result lines, 1,604 passed, 0 failed, 21 ignored; against main's last check (1,594 passed, 1,614 test names) exactly 10 new test names and 0 gone; `crates/coagent-policy/red-controls.sh` exit 0: 76 lines `RED OK`, then the normal build green. Last line `MERGE CHECK OK policy-at 2004a04ebba7e1d031dfa341da26f76693345aff`.
- By Friday's own reads at `2004a04`: the 15 protected test files' sha256 equal the table's values (15 of 15); the 10 paths are your lane's; a names scan of the 1,013 added lines and the commit messages found 0 hits, with a planted line as its control.
- **The check's two wording points and its Notes are NOT a further round on this branch.** Do NOT edit anything for them: the next policy lane takes them.

## 2. The GO
Merge GO for `2004a04ebba7e1d031dfa341da26f76693345aff`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is `5e11609cee1cb483bd006547e9092d49522691cc`, `git ls-remote origin policy-at` is still `2004a04ebba7e1d031dfa341da26f76693345aff`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin 2004a04ebba7e1d031dfa341da26f76693345aff:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED POLICY-AT` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
