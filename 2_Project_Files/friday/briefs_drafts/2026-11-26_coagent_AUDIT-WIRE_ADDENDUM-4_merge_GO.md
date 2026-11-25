This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-WIRE only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 4 (merge)" in your STATUS file; last line when done exactly `MERGED AUDIT-WIRE`.

If your context was compacted while you waited: re-read your brief, its addenda and your STATUS file WHOLE before doing anything.

# AUDIT-WIRE ADDENDUM 4: merge GO for one exact SHA

## 1. What stands behind it
- The second independent check: `VERDICT: GO WITH NOTES — head e049cec8f69d9e2cda4f0f4fcdb63ebd64068785` (read whole by Friday today): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_AUDIT_WIRE_r2_verdict.md`.
- Your merge of main (addendum 3): head `5e11609cee1cb483bd006547e9092d49522691cc`. Friday's proof by program with read verbs in the project repository: its parents are exactly `e049cec…` and `184b35e…`; the checked sha to the merged head changes exactly the other side's 7 files; `184b35e` to the merged head exactly your 20 paths; 0 bytes of difference from the checked sha under the daemon crate, the daemon red script and `Cargo.lock`; the two shared documents are `184b35e`'s text plus your lane's added lines, 0 removed (66 and 23 added).
- **Main is `184b35ef17cf9865c4f9b20c721f9647233f8b98`** by Friday's own `git ls-remote` in this action: the second parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `5e11609`: `scripts/check.sh` exit 0; by program over its log: 243 result lines, 1,594 passed, 0 failed, 21 ignored; against main's last check (1,580 passed, 1,600 test names) exactly 14 new test names and 0 gone; `scripts/red-controls-daemon.sh` exit 0: 199 rows `RED (as required)`, 0 `STILL GREEN`, then `final clean run: green (77 test binaries; ignored under rulings: 2)`. Last line `MERGE CHECK OK audit-wire 5e11609cee1cb483bd006547e9092d49522691cc`.
- By Friday's own reads at `5e11609`: the 13 protected and 3 kept test files' sha256 equal the second check's values (16 of 16); the 20 paths all lie in the lane's territory; a names scan of the 3,598 added lines and the commit messages found 0 hits, with a planted line and the old lines of `BACKLOG.md` as its controls.
- **The check's Notes are NOT a further round on this branch.** Do NOT edit anything for them: the SHA that merges is the SHA that was checked plus your one merge commit.

## 2. The GO
Merge GO for `5e11609cee1cb483bd006547e9092d49522691cc`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is `184b35ef17cf9865c4f9b20c721f9647233f8b98`, `git ls-remote origin audit-wire` is still `5e11609cee1cb483bd006547e9092d49522691cc`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin 5e11609cee1cb483bd006547e9092d49522691cc:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED AUDIT-WIRE` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
