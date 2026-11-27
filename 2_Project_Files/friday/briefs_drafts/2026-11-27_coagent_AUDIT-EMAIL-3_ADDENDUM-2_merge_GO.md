This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-EMAIL-3 only. It is the merge GO. It changes no other rule. Report under "## ADDENDUM 2 (merge)" in your STATUS file; last line when done exactly `MERGED AUDIT-EMAIL-3`.

If your context was compacted while you waited: re-read your brief, its addenda and your STATUS file WHOLE before doing anything.

# AUDIT-EMAIL-3 ADDENDUM 2: merge GO for one exact SHA

## 1. What stands behind it
- The independent check: `VERDICT: GO WITH NOTES` at head `627431877d5fa3b86f91ec23d0dc2879c800eb33`: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_AUDIT_EMAIL_3_verdict.md` (415 lines; Friday read its lines 9 to 16, 318 to 329 and 367 to 395: the BLUF, the findings against the coordinator's rulings, the owner section and the findings; its property sections were not read by Friday).
- No merge of main was needed: by Friday's read verbs your head is ONE commit whose only parent is `5aa56e1217947471bbb358c6a5a5214f31ee65a8`.
- **Main is still `5aa56e1217947471bbb358c6a5a5214f31ee65a8`** by Friday's own `git ls-remote` (the output this file was built from): the parent of your head, so your push is a fast-forward.
- Friday's clean-clone merge check (her own clone, target and cargo home) on `627431877d5fa3b86f91ec23d0dc2879c800eb33`: `scripts/check.sh` exit 0; by program over its log: 251 result lines, every one `ok`, 1,630 passed, 0 failed, 24 ignored; against the last landing's check log (250 lines, 1,621 passed, 1,641 distinct test names) 10 new test names, all `ae3_`, and 0 gone; `scripts/red-controls-audit.sh` exit 0: 191 row lines each with a `RED` result (189 cfg rows and 2 source-mutant rows by the log's own count line), 0 lines holding a not-red or still-green word, `GREEN: 332 tests ok`, last line `RED CONTROLS OK`. The check's last line: `MERGE CHECK OK audit-email-3 627431877d5fa3b86f91ec23d0dc2879c800eb33`.
- **The check's Minor L3-1 (five unguarded branches), its Notes L3-2 to L3-10, and its findings against the coordinator's rulings (RM3-1, RM3-2 and the Notes beside them) are NOT a further round on this branch.** Do NOT edit anything for them: the next audit-library lane takes them.

## 2. The GO
Merge GO for `627431877d5fa3b86f91ec23d0dc2879c800eb33`, and for no other SHA.
1. Confirm: `git ls-remote origin main` is `5aa56e1217947471bbb358c6a5a5214f31ee65a8`, `git ls-remote origin audit-email-3` is still `627431877d5fa3b86f91ec23d0dc2879c800eb33`, your worktree clean. If either differs, or you made any commit since, STOP and say so (then do NOT push; write `STOP Q<n>`).
2. `git push origin 627431877d5fa3b86f91ec23d0dc2879c800eb33:refs/heads/main` (fast-forward only: main is the parent of that commit; never force, never a new merge commit, never a rebase; not via the local `main`). If refused, STOP and quote it.
3. Record `git ls-remote origin main` after the push in STATUS. Then write the last line `MERGED AUDIT-EMAIL-3` and stop. Nothing else.

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
