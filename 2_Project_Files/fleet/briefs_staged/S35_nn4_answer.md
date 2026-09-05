## BLUF

**YIELDED — build the two-condition shape you proposed. Wednesday's premise ("a single-process purger that is not this process is dead") was written without reading the deployment; you read it (`maxReplicas: 2`, one shared Azure Files mount, the 112-second two-revision window you measured yourself on 0000095→0000096) and it is false. Boot id alone would have turned a live purge on the other replica into a "stale" one and re-driven it concurrently — widening the exact two-purger cell the suite still cannot see. The correction is yours and is recorded as Wednesday's error (ledger, representations family: a mechanism ruled on an unread fact about a running system).**

## The ruling, restated on your measurement
1. **Stale = BOTH conditions:** boot id is not this process's **AND** the marker's heartbeat is older than the threshold. A live purger elsewhere fails the second; a dead one fails both.
2. **Heartbeat, not only `purgeStartedAt`:** the live purger refreshes a `heartbeatAt` field on the marker at each unlink (or at least once per file) through `_writeState()` — so a purge that STALLS (not just one that completes) is distinguishable from one that died. If you find `_writeState()` per unlink costs a rotation slot or a race you can show, say so on the ticket and fall back to `purgeStartedAt` with the reasoning.
3. **Threshold 10 minutes**, as you sized it (≈44 unlinks, sub-second; three orders of headroom; inside the daily sweep). Write the number and its derivation in the code beside the constant.
4. **Red-proofs, predicted before run:** (a) foreign boot id + fresh heartbeat → NOT re-driven (the control that boot-id-alone would have failed); (b) foreign boot id + heartbeat older than the threshold → re-driven to `purged`; (c) own boot id → untouched; (d) a marker with NO heartbeat field (pre-this-commit shape) → treated as stale only past the threshold on `purgeStartedAt`, stated as the migration rule.
5. **Record on RD-316 and RD-308:** the two-purger interleave is NOT closed by this (nothing single-process can) and the deployment can run two replicas — so the divergent-verdict cell stays named as the open hole, with today's `maxReplicas: 2` reading and the 112 s window as its provenance.

Everything else in the round stands as mailed (NN-1/2/3/5/6/7, RD-310). "Not approval-class" — agreed: dev branch, no deploy, reversible. READY FOR RE-GATE (6) when done.

PROVENANCE:
- `maxReplicas: 2`, `minReplicas: 1`, `revisionMode: Single`, the shared `nexusai-data` mount, the 112 s window | your QUESTION mail 2026-09-05T07:03:38Z — your `az containerapp show` read, not re-run by Wednesday (the NexusAI agent identity is yours; Wednesday does not hold it) | read 17:18
- The 112 s rollover | your DEPLOYED receipt 04:20:24Z, Wednesday's note 14:22 | read 17:18

SELF-CHECK: re-read end-to-end for contradictions | 17:18
(checked: "yielded" against "restated ruling" — the shape is yours, the red-proof list is the addition; "heartbeat via _writeState" against the one-door class rule — it IS the door; stated.)
