# ANSWER (Seat B 48th): KAM RULED (c): accept GHSA-r53p PERMANENTLY, "and fix now". Amend #1354 to permanent (ROUTE A), push; gate48b now covers #1354 then #1355. ctx:56% at 2026-09-30 11:05

## BLUF
**Your ctx: ctx:56%** (Wednesday read of pane %79, 2026-09-30 11:05 AEST). **Kam ruled on the live board at 11:03:17 AEST, verbatim:** *"Decision secuura-undici-ghsa-r53p-exception-1354: c — Accept permanently, like the twelve siblings | note: And fix now"* (card `secuura-undici-ghsa-r53p-exception-1354`, recorded as ruled c). **This SUPERSEDES your brief's NO-RULING queue.** Do both halves: make #1354 PERMANENT, and #1355 continues as the fix. **One gate, gate48b, covers both, merge order #1354 → #1355, GO string `GO (Seat B 48th): merge 1354 1355 on gate48b`.**

## DO NOW, on #1354 (adopted `-b47-3` ref, B 47th's branch)
1. In a `--detach` worktree at #1354's head `4370be410bbf`, change exactly two things.
   - **`audit-baseline.json`, the GHSA-r53p row:** REMOVE `expires`. Set `reason` to gate48a's AMENDED reason text (report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-30-batch1354-g48a/report.md`, the "AMENDED row reason" block) edited for PERMANENCE:
     - replace its final "TEMPORARY, expires 2026-10-09 … refuse again." sentences with ONE sentence citing the ruling: "Accepted permanently on Kam Kreiser's ruling (card secuura-undici-ghsa-r53p-exception-1354, 2026-09-30); the vulnerable version is removed by the undici override fix, PR #1355 (KS 1378), after which this row is no longer reported."
     - keep every measured sentence as the gate amended it; add nothing unmeasured.
   - **`scripts/audit/baseline-contract.mjs`:** +1 line adding `'GHSA-r53p-7pc4-xj5r', // undici        KS-470` to GRANDFATHERED_NO_EXPIRY at its alphabetical position. This is B 47th's measured ROUTE A.
2. Run contract / leg 6 / leg 7 at the new head (rc on its own line; expect 0/0/0). Push under `.push-lock-44`: legs 6/7 must pass in the hook.
3. **Mail ONE READY ADDENDUM** naming #1354's new head, the diff vs `4370be410bbf` (+/- per file), the three rc's, and the hook's legs. The gate48b drafter pins it from origin.
4. **#1355: unchanged.** Merge order #1354 → #1355. #1355's js-yaml hunk becomes a no-op over #1354's squash (identical blob), and the gate proves it clean.

## AFTER BOTH MERGE (for your handover if ctx runs short)
- The permanent r53p row becomes one of 13 undici rows leg 6 lists as no longer reported. **The cleanup of those rows (and the 2 ip-address rows) is a separate change, for Wednesday to commission, not yours this round.**
- The override ticket is moot: #1355 is the fix. Do not file it.
- ITEM 1a rebases after both merges.

**Hard line 75%.** No baseline edit beyond the two named lines; no `--no-verify`.

PROVENANCE:
- Kam's ruling | kam_msgs.sh 1 (live board, view=wednesday) 2026-09-30T11:03:17+10:00, verbatim above; card ruled c via reconcile_rulings.py --apply (HTTP 200) | read 2026-09-30 11:05
- your ctx | tmux capture-pane statusline ctx:56% | read 2026-09-30 11:05
- ROUTE A = 0/0/0 | B 47th's STATUS 21:38Z (routeA green) | read 2026-09-30 07:39
