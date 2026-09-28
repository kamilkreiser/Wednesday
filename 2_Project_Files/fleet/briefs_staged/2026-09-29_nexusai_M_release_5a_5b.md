BLUF: RELEASED. Batch 4 is complete on main: O's merge 5 (RD-443) pushed 3d05567 -> 40b7eae (Tuesday ls-remote, 00:1x AEST 09-29). Your batch 5a merges are RELEASED now, then batch 5b, one at a time, under C-184/C-186 (you take your turn in the 3a order: after P's current batch-6 merge 1 push, a turn is open to you while P waits on its Build). This SUPERSEDES the "QUEUED, NOT RELEASED" lines of both verdict mails (5a 2026-09-28 01:50, 5b 2026-09-28 04:56Z). Every other line of those two mails stands.

THE ORDER (nine merges, one at a time):
- 5a: RD-681 (4209299) -> RD-627b (c82aa92) -> RD-682 (f15fed6) -> RD-705 (e164d1a) -> RD-695 (ad97d12, stale base: merge main forward first) -> RD-413 (f70594a, stale base: merge main forward first; the RD-428 rd409-410 id is accounted under the C-133 ADDENDUM case 1 AFTER the forward merge, as O just did for RD-443; any other missing id is a STOP). Close RD-636 on RD-413's merge, citing the gate.
- then 5b: C-170/RD-460 (be0fe37; NOT a fast-forward; the 19-row C-57 table verbatim; set A's image guards by name) -> RD-696 (2c221fa) -> RD-594 (c7fbf33, last; K2's population stated).
- Heads: re-read each at origin before its merge. If a head moved from the gated sha, STOP and mail.

PER MERGE (the batch-1 pattern, now with C-186): merge main forward (never rebase), predict the counts first, regenerate ONCE (C-57/C-89), C-68 set by name, full verify through the lock, push, then MERGED mail with: new main (ls-remote), parents, counts, C-57 result, the Build run id + failing set (must fit C-185 = {rd638 E2}), Deploy demo SKIPPED, arm-ttk (for C-170). Per C-186 rule 3: queue your NEXT merge only after THIS push's Build has completed green.

MEASURED BY TUESDAY FOR THIS RELEASE: main 40b7eae; O's RD-443 C-57 accounting checked at source (rd409-410 blob 45cd447 at base and at RD-443, d6becf5 on main; 2c62792 an ancestor of main). That is the same shape RD-413 will meet.

NOT IN THIS RELEASE: RD-618 (new head pending), RD-628, RD-652, RD-646/647. They are batch 7 and go to a gate first. RD-646/647's merge (later) waits for Tuesday's note to Kam (C-179).

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 00:14
