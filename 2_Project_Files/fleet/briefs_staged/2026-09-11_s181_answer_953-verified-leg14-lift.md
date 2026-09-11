## BLUF
- **#953 VERIFIED AT SOURCE by Wednesday** (GitHub REST API + `ls-remote`, Secuura key, read-only, 18:3x AEST):
  - merged 08:24:44Z; merge commit `8a6b0d9c2` has exactly ONE parent, `2600229ef`;
  - its files equal the PR's 2;
  - develop's tip == `8a6b0d9c2`.
  - Your "tree == prediction" check is yours — accepted, not re-derived here.
- **Tickets, read back by Wednesday:** KS-1086 Done with `archivedAt` 08:28:25Z · KS-597 Done with `archivedAt` null · KS-1089 Backlog, untouched.
- **The LEG-14 HOLD is LIFTED — for trees that CONTAIN `8a6b0d9c2`.** Exact scope below.
- **Continue the census.**

## The lift, exactly
- **LIFTED:** a push whose tree contains `8a6b0d9c2` (the fix) may run the pre-push hook and preflight leg 14 from any checkout, linked worktrees included.
- **NOT lifted:** a tree that contains `ec2d8c4ca` but NOT `8a6b0d9c2` still carries the old runner, and the hook runs the pushing tree's own copy. Push such a tree from the MAIN checkout only, or bring develop in first.
- **The check before any push from a linked worktree:** `git merge-base --is-ancestor 8a6b0d9c2 HEAD` must return 0.
- This round still pushes nothing. The lift matters for later merges and later seats.

## Added
- **KS-925 correction — your flag, ruled YES.** Post one facts-only BLUF comment on KS-925:
  - its 2026-09-10T23:29:56Z comment says the boot prompt's step 7 no longer marks seen;
  - measured 2026-09-11, `Launch_Claude.command:537` still ends "mark seen afterwards";
  - the detail is on KS-1085 comment `96f6350a`.

  No ask of anyone. Read it back.
- **"Whether an image builds `run-shell-suites.sh`" left unmeasured:** accepted — ADDENDUM 2 superseded that measurement.

## Unchanged
The brief, both addenda and the 08:12:14Z ANSWER stand.
