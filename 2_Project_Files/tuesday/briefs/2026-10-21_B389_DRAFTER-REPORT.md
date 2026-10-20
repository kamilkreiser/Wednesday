# B389 drafter report (2026-10-21 ~09:15 AEDT)

Brief: `2026-10-21_B389_SEAT-G18_hpsmpoc-pr169-gate-tier1.md` (tier 1, Opus, G1, round 1 of 2, pane Datasec/HPSM-POC-G18, ports 7480-7489). Shape: B387 (read whole) raised to tier 1, severity floor and sweep style from B376 (read whole). Builder STATUS B381 (147 lines) and builder brief (113 lines) read whole. No dotnet/npm/vitest/Jira run.

## Stamp slots
Two: `@STAMP_TIME@` and `@LAUNCH_AUTH@`, both at the end of the Stamp paragraph. `grep -o -E '@[A-Z_]+@' | wc -l` = 2 (the SELF-CHECK mention removed). Last line `READ-WHOLE-BY-TUESDAY: PENDING`.

## Measured by me (09:06 AEDT, read verbs only)
- main `54fbceac`; branch and `refs/pull/169/head` = `bcff3e46`; PR #169 open, not draft, 3 commits, 5 files, +159/-3 (file stats match your numbers). Open PRs #168, #169.
- `.tools/b38*`: b380-b383, b386, b387 trees exist; no b389.
- Reader line at base: `FeedbackFiles.cs:338` `HeadersCountLimit = 16, HeadersLengthLimit = 16 * 1024`.
- formGate.ts patch read (headerName, Set, `names.size > 16`, one `""` literal).
- Load 10.09 / 10.83 / 11.43.

## IMPORTANT finding for you before launch
CI at the head: `web build (audit, lint, typecheck, build, deploy package)` is already **failure** (job 118913548600, run 39505585248). Failing step 6 = `npm audit, all dependencies`: `FAIL GHSA-587h-7wmj-h5pm (high) vite >=8.3.0 <=8.3.2` (log). Lint, typecheck, build, deploy package and e2e were SKIPPED. Same check was success at main 54fbcea and at #168's head (21:15Z, 50 min earlier). Looks like a new advisory, not this PR (no lockfile in diff), but that is a hypothesis; the brief tells the gate to establish it and to say CI never ran lint/typecheck/build at this head. This will block a landing (and #168's, and any PR) until the advisory is dealt with: your call, outside the gate.

## Deliberate additions beyond B387
Never-tighter invariant (A=read AND C=0 = Blocker) with a differential table, 20k-block seeded sweep, planted tighter/wrong-oracle controls; extra shapes (tab, control bytes, obs-fold, bare CR/LF, Kelvin/dotless-i/long-s folds, two-part forms); `headerName` timed itself (the 285 tests spy on indexOf and do not see it); M2 control (16 names + 20 MiB+1 must still be 413); own -288 mutants; export extraction by program; the `""` literal as a Note; B380/bff.ts interplay in the merge prediction.

## Not verified (UNMEASURED)
Test file contents, `ClientFollowUpEndpoints.cs`, the 21 MiB cap line, B380's branch contents, Jira state, the ticket Done-when text (RELAYED), whether the hosted API is on 10.0.12.

## Questions (each with a recommended answer)
1. Launch with CI pending/red and the conditional suffix? Yes.
2. The red web build blocks landing: have a seat/ruling for the vite advisory in parallel? Your call; recommend yes, separate card, not the gate.
3. Stamp authority: Kam's 2026-10-16 merge-once-tested grant + terminal words ~07:2x + the three-hop QA rule (as B387)? Yes.
4. Launch at load ~10 with four seats live? Yes behind the HOLD (the gate waits per LOAD).
