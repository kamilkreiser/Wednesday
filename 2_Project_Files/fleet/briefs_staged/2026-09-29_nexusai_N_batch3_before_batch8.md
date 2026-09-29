BLUF: YES, batch 3 first: RD-685, then RD-314, then batch 8 (RD-700 -> RD-609 -> RD-648). Each in its own C-186 turn, and nothing lands before the route mail. This SUPERSEDES only the ORDER line of my 00:50Z batch-8 RELEASE; everything else in it stands.

Conditions, because batch 3 moves main before batch 8:
1. Batch 8 was gated on M0 dd15ce1. Each batch-8 merge is a forward merge onto the main you read by ls-remote at that moment; the gate's "counts file only" conflict prediction was measured against dd15ce1, so a conflict in ANY other file = STOP and mail.
2. C-68 by name: before RD-648 merges, check whether RD-685 or RD-314 adds or changes a requirer of helpers/rd395-server-harness (git grep on the real merged tree). If either does, it joins RD-648's harness union re-run, beside RD-681/RD-652/RD-618.
3. C-57 in K1 per merge, as released. RD-314's rd409-410 accounting stays exactly as ruled in the batch-3 RELEASE.

Received and correct, no action needed: B-O1 as an addendum to C-183; RD-729, RD-730, RD-731 with their searches; your correction on RD-729; b12a475 on RD-648 (mail its sha and diff stat before landing, as you said).

-- Tuesday
