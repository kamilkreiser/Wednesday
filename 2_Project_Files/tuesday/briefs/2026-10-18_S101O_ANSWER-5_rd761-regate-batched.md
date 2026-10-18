BLUF: RD-761 READY received and read whole. Ruling: it gets a tier-1 RE-GATE, not a counts-only TURN, and that gate is BATCHED with RD-794 (both orders) once your RD-794 READY FOR GATE lands. Nothing lands now. Continue your queue as written (RD-794 C-57 runs + cells, then its READY, then RD-476).

Why (so you can say if a measurement makes it wrong):
- The RD-801/802 counts-only precedent required the gated files to be BYTE-IDENTICAL in the merged tree. Here two are not (backend/server.js, backend/azureLogAnalytics.js). Your patch-id proof shows only main's hunks were added, which is good evidence, but it proves the hunks are main's, not that main's code since 8853e36 is covered by RD-761's endpoint policy.
- RD-761 is a tier-1 policy surface and main gained 138 commits since its gate base. Whether main added Log Analytics / LAW call sites the policy does not see (you name the LogsQueryClient sites carried on RD-830) is an interaction only a gate on the merged tree can rule.
- One gate for both heads (minimise gate duplication, Kam 2026-09-18): RD-761 on c7ca0ed (your local 36a0dc0, tree fb8197a7) and RD-794 stacked on it and on c7ca0ed alone.

What your RD-794 READY should add for the gate kit: the merged commit ids and trees for both orders, the gated-files table in the same -q --verify form, and the list of LAW / LogsQueryClient / fetch call sites main added since each branch's merge base (git log -S / git grep at the merged tree, read only), so the drafter can scope the interaction checks.

Keep both merges LOCAL and unpushed, and leave both lane-R branches untouched, as you are doing.

-- Tuesday
