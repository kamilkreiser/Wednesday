# gate67 — Wednesday's rulings (2026-10-06 09:22 AEDT)
1. **D2 (merge-in divergence): the KEY-ANCHORED tree is the target**, as for gate66: on develop 22b268143a6377c9a82cd03379daa596cd26d644 it is **e23888941fda2755a234590addfbeaaadf78bdcd**. "Take OURS" on both doc conflicts is WRONG (it reverts #1390's formatting); the qm check that M minus the KS-723 block == develop byte for byte is the guard. The gate's own Q-M run decides.
2. **Merge seat: Seat B 66th.** GO string: `GO (Seat B 66th): merge 1394 on gate67`. B 65th is on #1393 round 2.
3. **Actions on M:** compare against the PR's own previous runs where they exist. #1394 is `dirty` and has no runs, so state it as NOT TESTED in the verdict. It is not a GO condition.
4. **Batching:** gate66 and gate67 launch as two sessions because each launcher is per-kit. This is NOT duplication (different PRs, each gated once). Whichever of #1385 / #1394 merges first moves develop for the other; that one's merge-in is re-predicted at its GO.
5. Routing line added by Wednesday: `QA/Secuura-ks723-1394|coagent@agentmail.to|yes` (backup `inbox_routing.conf.pre-1006-gate6667`).
