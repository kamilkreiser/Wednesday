This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat VIEWER-NEXT-2 only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in your STATUS file; last line when done exactly `MERGED VIEWER-NEXT-2`.

If your context was compacted while you waited: re-read your brief, addenda 1 and 2 and your STATUS file WHOLE before doing anything.

# VIEWER-NEXT-2 ADDENDUM 2: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO — head bc771535cff36b74cfbf0d187fa6c06a257e21e9` (the verdict file's first line, read by Friday in this action; the file was read whole by Friday's earlier seat today): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_VIEWER_NEXT_2_verdict.md`.
- Your merge of the policy head (addendum 1): head `36109f98123f9f15884d47447eb1851f62c01ff4`. Friday's proof with read verbs in the project repository, run again by this seat: its parents are exactly `bc77153…` and `7fc6188…`; the checked sha to the merged head changes exactly the other side's 12 files (the same list as their merge base `debbb44` to main); main to the merged head exactly your 3 paths (`BACKLOG.md`, `crates/coagent-daemon/tests/la_wrap.rs`, `docs/M0-OUTCOMES.md`); `la_wrap.rs` is blob-equal to the checked sha and the other side's 10 files other than the two documents are blob-equal to main; each of the two documents is main's text with your lane's added lines (6 and 3) in order, 0 removed (by program: 1551 + 6 = 1557 lines and 203 + 3 = 206 lines).
- **Main is `7fc61882b6eed3245428d0e120714bd3b06e0c18`** by Friday's own `git ls-remote` in this action: the second parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `36109f9`: `scripts/check.sh` exit 0; by program over its log: 232 result lines, 1,574 passed, 0 failed, 21 ignored, the same totals and the same 1,592 test names as main at `7fc6188` (0 new, 0 gone: your lane changes one assertion inside an existing test); `scripts/red-controls-daemon.sh` exit 0: 174 rows `RED (as required)`, then `final clean run: green (66 test binaries; ignored under rulings: 2)`. Last line `MERGE CHECK OK viewer-next-2 36109f98123f9f15884d47447eb1851f62c01ff4`.

## 2. The GO
Merge GO for `36109f98123f9f15884d47447eb1851f62c01ff4`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is `7fc61882b6eed3245428d0e120714bd3b06e0c18`, `git ls-remote origin viewer-next-2` is still `36109f98123f9f15884d47447eb1851f62c01ff4`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin 36109f98123f9f15884d47447eb1851f62c01ff4:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED VIEWER-NEXT-2` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
