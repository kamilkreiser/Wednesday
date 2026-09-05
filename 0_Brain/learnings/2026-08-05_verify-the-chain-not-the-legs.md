---
date: 2026-08-05
type: lesson
source: "Self-caught during WED-56/57 drive syncs: KK_DEV_Local pass returned rc=0 'complete' while today's daily note was still absent from it"
status: live
tier: M
---

# Multi-hop sync: verify content at the destination, not exit codes per leg

**The catch:** the DevMASTER↔KK_DEV_Local pass finished rc=0, 0 failed — and
the drive still lacked that morning's brain-writes. The sync was honest: it
synced its two roots perfectly. The gap was UPSTREAM — the T9→DevMASTER leg
hadn't run since the previous night, so DevMASTER itself was stale for the
WEDNESDAY subtree. A chain of green legs proved nothing about the chain.

**The rule:**
1. For any multi-hop copy/sync (A→B→C), the verification target is the
   ARTIFACT AT THE FINAL DESTINATION — pick a file you know changed at the
   origin TODAY and confirm its content arrived at the end of the chain.
   (`ls` isn't enough; grep for today's content — the file may exist stale.)
2. Leg exit codes only certify leg-local consistency. rc=0 means "these two
   roots now match", never "the data you care about is here".
3. Before promising freshness to Kam ("all the code is there"), run the
   content check first — this is [[2026-08-03_mental-model-not-source-of-truth]]
   applied to data plumbing.

**Related:** [[2026-08-03_mental-model-not-source-of-truth]], WED-56/57
receipts (the two-pass churn pattern lives there too: bulk pass while agents
work, cleanup pass after their receipts).
