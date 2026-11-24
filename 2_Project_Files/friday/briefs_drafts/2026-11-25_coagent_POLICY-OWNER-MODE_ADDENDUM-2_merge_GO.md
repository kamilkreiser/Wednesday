This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-OWNER-MODE only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in your STATUS file; last line when done exactly `MERGED POLICY-OWNER-MODE`.

If your context was compacted while you waited: re-read your brief, addenda 1 and 2 and your STATUS file WHOLE before doing anything.

# POLICY-OWNER-MODE ADDENDUM 2: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES` at `59de2d3f42d0b13a1d98b184a9ba3e7a9860a7dd` (no Blocker, no Major; two Minors, seven Notes): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_POLICY_OWNER_MODE_verdict.md`, read whole by Friday.
- Your merge of main (addendum 1): head `80ad11550971a075ca64a742fa1783589f71f673`. Friday's proof in her own clone: its parents are exactly `59de2d3…` and `734cf6e…`; the checked sha to the merged head changes exactly main's 19 files; main to the merged head exactly your 12 paths; your 10 non-document paths are blob-equal to the checked sha and main's 17 non-document files blob-equal to main; in `BACKLOG.md` and `docs/M0-OUTCOMES.md` your lines over main are 25 and 12 added, 0 removed, identical line for line to your lines at the checked sha.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `80ad115`: `scripts/check.sh` exit 0 (fmt, clippy, test, deny); by program over its log: 208 result lines, all ok, 1,512 passed, 0 failed, 21 ignored = main's 1,499 plus 13, in three new test binaries, 12 new test names, none gone; `crates/coagent-policy/red-controls.sh` exit 0, 71 rows `RED OK`, the normal build green. Last line `MERGE CHECK OK policy-owner-mode 80ad11550971a075ca64a742fa1783589f71f673`.
- Friday's own `git ls-remote` just before this was written: main `734cf6e9ad117ec1c51dd1f89c413856e308c664`, policy-owner-mode `80ad11550971a075ca64a742fa1783589f71f673`.
- **The check's Minors and Notes are NOT a further round on this branch.** They go to one policy hardening lane (another seat) before the switch lane. Do NOT edit anything for them: the SHA that merges is the SHA that was checked.

## 2. The GO
Merge GO for `80ad11550971a075ca64a742fa1783589f71f673`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is still `734cf6e9ad117ec1c51dd1f89c413856e308c664`, `git ls-remote origin policy-owner-mode` is still `80ad11550971a075ca64a742fa1783589f71f673`, your worktree clean. If either differs, or you made any commit since, STOP and say so (another lane may have merged a minute before you: then do NOT push; write `STOP Q1` and Friday sends the next steps).
2. `git push origin 80ad11550971a075ca64a742fa1783589f71f673:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED POLICY-OWNER-MODE` and stop. Nothing else.

Thank you: the measurement of what the terminal setting reaches, said plainly with its two gaps, is what lets the owner decide the switch with open eyes.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
