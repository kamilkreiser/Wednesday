SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1029 KS-1180 part 1 @cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc (TIER 2, test-only)
TS: 2026-09-17T11:00:44.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
READY FOR QA: #1029 KS-1180 part 1 at `cd3580e1f7c6d00ac2ff05d2f3703460feaf34cc` (TIER 2, test-only, as ruled 02:34:03Z). The ks1072 verify cells now witness tier 2 by the stub anchor store's requests (exactly one read of this document) instead of `blockchain.source`, which reads `persisted` on both tiers. A new control proves the listener sees a miss. Develop `20ab16f9a` is merged in (tree = prediction). **Tamper re-run at the merged head: 5 / 5 as predicted** on api-gateway 56 files / 551 tests. api-gateway 551 / 551, tsc rc 0. Push PROTOCOL-DIFF ruled benign by you (10:57:09Z). linkKinds: KS-1180 `contributes` only; KS-1073 not linked.

## Recommendation
1. **Gate the head `cd3580e1f`** (tier 2). `Refs KS-1180 (P-1016-1, P-1016-2)`, never Closes: the tier-1 half and the P-1005 items stay open on KS-1180.
2. **KS-1180 walked Backlog → In Progress at 11:00:14Z** with no actor (the GitHub branch automation on PR creation). Expected; left as is.
3. **No KS-1180 comment names #1029.** Its one comment predates the PR. Default, as for KS-1050 / KS-839 / KS-744: one BLUF facts comment after the verdict.
4. **Next:** open PRs are #1028 and #1029, so one slot is free. **KS-1213 goes in** (develop `75ad0e55c` merged in first, originate re-run, push, READY tier 1).

## Detail
- **Head and push:** branch `feature/ks-1180-ks1073-verify-cells-the-tier-guard-is-not-a-tier-witness-the`. Commits over develop:
  - `a4dc0d8ee` (the fix, 1 file +16 −3);
  - `7553821fc` (develop `81ee4b729` merged in, earlier seat);
  - `cd3580e1f` (develop `20ab16f9a` merged in, parents `7553821fc` + `20ab16f9a`, tree `5138ce742` = my read-only prediction).

  First push 10:48:54Z → 10:54:47Z, rc 0. Preflight `12/15 legs ran, 3 SKIPPED. Nothing failed.`: legs 3 / 4 / 8 skipped (no stack), not a pass of those. Leg 1 `spec is in sync`, leg 5 59 / 59, shell suites 35 / 35. Verify PROTOCOL-DIFF, ruled benign 10:57:09Z (Seat B's merge-in on `feature/ks-1211-bump-vitest`).
- **PR:** REST 201, #1029, base develop at creation `75ad0e55c`; title `KS-1180 part 1: the ks1072 verify cells witness tier 2 by anchor-store reads, not by blockchain.source`; body read back byte-equal, `Linear:` URL, `Refs KS-1180`, closing phrases 0, at-signs 0, footer. Origin: `refs/heads/<branch>` = `cd3580e1f` (ls-remote before creation).
- **Tamper re-run** (`5_Project_History/2026-09-17_seatA-6th/ks1180p1/tamper/tamper.json`, 20:47:44 → 20:48:33 AEST). The rows are the 4th successor's, with its measured results as predictions. Each row: anchor 1, tsc rc 0, the whole api-gateway suite 56 / 551, pending 0; restored by blob sha plus `git diff --quiet HEAD`; every red an `AssertionError`.
  - T0: 0.
  - GREREAD: 5 in the ks1072 file (the three 🔴 KS-1072 cells + two controls); the KS-1180 control green.
  - GT2 (tier 1 answers): the same 5.
  - TTIER2: 0 in-file, plus exactly the 13 other-file tier-1 cells: ks1057 ×4, ks1069 ×2, ks1071 ×3, ks1073 ×1, ks1123 ×2, ks1176 ×1.
  - TI: 0.
- **Stubs:** 4 ended by verified pid (69295 / 69405 / 69493 / 69625, started 20:51:52-54 AEST, cwd this worktree, ppid 1). 0 of mine remain.
- **NOT done / NOT covered:**
  - P-1016-2's with-tests tsc reading was not re-measured at `cd3580e1f` (the building seat measured the ks1072 line present at develop and absent at its pre-merge head). No count is quoted (#1018 F-2 lesson).
  - a real anchoring service or originate;
  - Schemathesis / Akto / Playwright / k6 (no stack).

