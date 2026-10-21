# B443 drafter report (read-only; two files written)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B443_SEAT-D26_hpsmpoc-uat-redeploy-header-md.md`. Slots: `@STAMP@` x4 (stamp time, launch authority, hard stop, final READ-WHOLE line). Fill all four before launch (the seat refuses at slot count > 0). Cloned from B437's stamped brief with the sha, checks and rollback re-pinned.

## Read whole
B437 brief (stamped), B437 DRAFTER-REPORT, B437 STATUS (290 lines, DEPLOYED 09:13), and the B441 gate STATUS up to Check 6 (verdict line, residual table, pins). Grepped B438 STATUS for N1 and the file list.

## MEASURED by me (read-only)
- `git ls-remote origin refs/heads/main` = `a93b926ac8534bd0c9ae67fe63229ede46c39fd4`, 10:50 AEDT.
- `a93b926a` is NOT in the local checkout (`cat-file -t` fails; `01dd9e4b` is). So its parent and the 2-file diff are UNMEASURED; the brief makes the seat verify both and STOP on any other path.
- The two rollback packages of `01dd9e4b` exist at `.tools/wt-b437/out/deploy-packages/01dd9e4b.../{web/web.zip,api/api.zip}` and their shasum equals B437's recorded values (web `47e1d0c1...`, api `07ced683...`). `.tools/b437/rollback/` holds only the `ae7a2c86` set and the live wwwroot downloads, so the primary rollback is the copy from the B437 worktree.
- load1 3.43 at 10:50.

## Judgement calls to check
1. **Rollback source.** The `01dd9e4b` packages live inside another seat's worktree (`wt-b437`). I allowed one read-only copy by name, plus an independent `fetch 01dd9e4b` (green run, artifacts expire 2026-10-28); STOP if both fail. Remove the copy permission if you prefer fetch only.
2. **CI wait bound** set to 30 minutes from first read, never past the point a deploy could not start before the hard stop (your 12:30). Squash-merged 10:37; the CI push run's state is UNMEASURED by me (no HTTP).
3. **Failure severity.** A new two-row at 672-767/390/1280/1440 or any overflow = STOP, no automatic rollback (UI regression on a review copy, Tuesday decides); rollback only for unhealthy sites. Residual B438-N1 rows (640-664, <=375) are recorded against B441's 17-row table, new ones flagged.
4. **Widths.** I added 700, 767, 768, 1440 to the asserted set and put 640/664/672/375/360/340/320 as recorded-only. Your request said 1280/1440 and 672-767; I asserted 767 and 700 and recorded 672.
5. **Instrument control** added: a known two-row cell (Consultant 664 or 375) must read two-row, else the one-row reads are not trusted.
6. **B437 gaps fixed:** infra README "After a deploy" now must be read whole (B437 skipped it); zsh `PIPESTATUS` slip noted; the stale web `LastError` (still carried) is stated, with no restart without an addendum.
7. **Ports** 8120-8129 named; B440 8100-8109 and `.tools/b440` fenced; load rule < 7 with B440 priority.
8. The brief's `Corrections` sections and model line follow B437. The squash tree vs gated head tree comparison is informational only.

## Not done / fenced
No `az`, no HTTP, no fetch/worktree, no decision queue, no fleet stores, no Artifact/Docs/mail/chat tools. Only the two files above were written.
