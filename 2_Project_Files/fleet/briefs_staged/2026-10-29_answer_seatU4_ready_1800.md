## BLUF
Seat U 4th: READY on #1800 (KS-1494 items 1 and 4, head fb3579b0a4b4) is RECEIVED. Wednesday has not read the code, so it goes to the gate. Both of your open readings are RULED YES (below). The gate is TIER 1 (Opus), because this guard is what stops a test suite from writing to a real database. It is BATCHED with Seat Y's KS-1240 b PR, the next tier-1 PR in the chain (slot 99), so that one gate session covers both. Your merge slot stays 108. That is many merges away, so **WRAP NOW**: your HANDOVER already carries the prep recipe. A successor U seat runs the prep, or the fix round if the gate finds one.

## Your two readings, ruled
1. **`?port=` naming a free loopback port is ACCEPTED and judged on that port**, as PR 1790 decides. This SUPERSEDES the brief's red-first line "?port=56488 refused" by name. The cell that asserts the judged port is the right cell.
2. **The database name is read from the pg client, decoded.** Judging what the client will actually connect to is the point of the change, so `/%6bs_x` read as `ks_x` is correct. No new cell is added now: the gate is asked to decide whether this case needs a pinning cell, and if it does, it goes into the fix round with the gate's other findings. One push, not two.

## Filing list (Wednesday's; nothing for you to do)
- integration/README.md line 12 is now incomplete (shared-stack ports, hostaddr, unparseable DSN), and "Expect 49 applied" should read 56.
- tsconfig.test.json does not include integration/. This is a decision item.
- The KS-1795 gaps are still in the ks597 file (#1790), and the KS-1793 hole is still in the ks1263 guard. There are now three copies of this logic.
- Slot ports (KS-390) are missing from the shared-stack list.
- Your brief correction is noted: tsc comes from the Dev root, not from services/auth.

## Wrap
History entry, HANDOVER final (it should name #1800, head fb3579b0a4b4, slot 108, the PROVISIONAL section 91 to renumber at prep, and these two rulings), vault commit, wrap mail. Keep worktree s-u-ks1494 for the prep seat.

## Provenance
- Your READY mail, 16:04Z (read whole): PR 1800, head fb3579b0a4b4d3b7c1dd2b2f63ee029c4ce5c5ec, base 802eb2b8ecaf, hook 13/16 legs (3 skipped, not a pass), docs CONFLICTING on the two docs only.
- Tier 1 and slot 108 come from Wednesday's NEXT-PICKUP 02:3x block ("its READY -> a tier-1 gate (Opus; the auth-adjacent DB guard) -> its slot after #1799 (108)"). The batch is Kam's 2026-09-18 standing rule (minimise gate duplication: batch gates). Weekly usage gauge 88% (usage_gate.sh --check, 03:04).
