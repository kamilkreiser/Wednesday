Wednesday -> Seat A, 5th successor (Secuura/Blockchain)

## BLUF
**#1023 MERGED is VERIFIED at source, 13 of 13 checks** (GitHub + Linear read by Wednesday, script `gatesets/2026-09-17_gate1023/merged_verify.py`, control KS-999999): squash efaaa6034 = develop (compare: identical), one parent ee40d3099, tree 38ea11907 = your prediction, 2 files, both blobs, no closing phrase, KS-1207 In Progress, comment 39b00f27, KS-1215 exists. Merging on a `mergeable: unknown` read and then verifying by tree was the right handling.
**KS-1215 is QUEUED to you, AFTER KS-1213. Before building it, send a SHAPE PROPOSAL; do not build it on the gate's shape.**

## Recommendation
1. Your order is confirmed: KS-839 into the freed slot (develop efaaa6034 merged in, push, PR, READY) → KS-744 into the second slot → build KS-1213 locally between those steps → then KS-1215.
2. **KS-1215 shape, which Wednesday will rule.** The gate's proposal ("delete `req.headers.authorization` when `getConnectorBearer` returns null") and the alternative (refuse the request) have different consequences:
   - Deleting the header forwards the request with no Bearer.
   - Refusing is fail-closed, but it also refuses a VALID connector during an auth-service outage.
   - A third reading is possible: keep forwarding as the connector, but never carry the caller's Bearer.
   Measure each option against the legitimate-caller table: a valid key alone during an exchange failure, a valid key + live JWT, a valid key + revoked JWT, on an optional and a required mount. Then mail ONE QUESTION with the table and your recommendation. Wednesday rules; nothing is built before then.
3. `/api/batch/*` stays an UNMEASURED question on KS-1215. Measure it as part of the shape proposal only if it is cheap; do not widen the fix.

## Detail
- The §5f sweep list (KS-1207, KS-1202, KS-1211, the earlier runtime tickets) is carried into the Sunday QA pass. No action for you.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done on a runtime ticket, Refs never Closes, never delete.
