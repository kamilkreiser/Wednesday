This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-EMAIL only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in your STATUS file; last line when done exactly `MERGED AUDIT-EMAIL`.

If your context was compacted while you waited: re-read your brief, its addenda and your STATUS file WHOLE before doing anything.

# AUDIT-EMAIL ADDENDUM 2: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES` at head `e31b29ac78fc19c6fc3c8fb206d44e2e91d7877c`: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_AUDIT_EMAIL_verdict.md` (Friday read its lines 1 to 43, 107 to 138 and 344 to 417; its other property sections were not read by Friday).
- Your merge of main (addendum 1): head `d4979dfe554c26019ed23139852813f95d5a4b25`. Friday's proof by read verbs in the project repository, made at your READY FOR MERGE CHECK line: its parents are `e31b29a` and `22242bb`; 0 bytes of difference between the checked head and the merged head under the audit library, its red script and `docs/AUDIT.md` (control: 40,555 over your lane's own range); `22242bb` an ancestor; in both shared documents each side's lines in order, 0 conflict-marker lines.
- **Main is still `22242bba3d93f9042019c0674e5c700d0651a120`** by Friday's own `git ls-remote` in the action that wrote this file: the second parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `d4979dfe554c26019ed23139852813f95d5a4b25`: `scripts/check.sh` exit 0; by program over its log: 249 result lines, every one `ok`, 1,614 passed, 0 failed, 22 ignored; against the last landing's check log (248 lines, 1,610 passed, 1,628 distinct test names) 5 new test names and 0 gone (the five `ae_` tests of your lane); `scripts/red-controls-audit.sh` exit 0: 180 row lines (178 cfg rows and 2 source-mutant rows by the log's own count line), each with the result `RED`, 0 lines holding a not-red or still-green word, the green run `GREEN: 316 tests ok`, last line `RED CONTROLS OK`. The check's last line: `MERGE CHECK OK audit-email d4979dfe554c26019ed23139852813f95d5a4b25`.
- **The check's findings against the coordinator's rule (RF-1 to RF-3), its Minors L-1 to L-4 and its Notes are NOT a further round on this branch.** Do NOT edit anything for them: the next audit-library lane takes them.

## 2. The GO
Merge GO for `d4979dfe554c26019ed23139852813f95d5a4b25`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is `22242bba3d93f9042019c0674e5c700d0651a120`, `git ls-remote origin audit-email` is still `d4979dfe554c26019ed23139852813f95d5a4b25`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin d4979dfe554c26019ed23139852813f95d5a4b25:refs/heads/main` (fast-forward only: main is a parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED AUDIT-EMAIL` and stop. Nothing else.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
