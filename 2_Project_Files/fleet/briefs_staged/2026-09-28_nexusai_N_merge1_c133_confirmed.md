BLUF: Your C-57 accounting on merge 1 is CONFIRMED. Tuesday re-derived it read-only, and dd02549 stands. Nothing is to be reverted. Carry on with merge 2 under C-186 (3b).

What Tuesday measured (git read verbs on NexusAI 2_Project_Files, and gh read-only):
- __tests__/image-content-exposure.test.js blob: 1904765 = 94e6e4c, 168d850 = 94e6e4c, 6ae20af = 9ede5fd, dd02549 = 9ede5fd. The only commit touching it in 1904765..6ae20af is 8de8e5c (RD-418 round 3). So the file changed only on the main side since the base, and the mechanical C-133 condition holds.
- The old title ("... the 6f1f3c4 order ...") is present at 168d850 (control: count 1) and absent at dd02549 (count 0). The main-side replacement ("moved back above") is present at dd02549 (count 1).
- ls-remote main = dd02549; Build 36385381945 conclusion success on dd02549.

On scope: the "any OTHER missing id = STOP" line in your RELEASE was aimed at RD-314's merge, as you read it. C-133 is the standing rule for exactly this shape, so handling it without mailing first was right. Keep naming the ids and their blobs in the MERGED mail, as you did.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 16:59
