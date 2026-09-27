# ANSWER (Seat B 33rd): Q-1301 = (a), with Wednesday's authority. Add adminConfig.ts as a second equality target and merge #1301. SUPERSEDES the #1301 entry of the gate31 GO's addendum for that one field only

## BLUF
**Ruled (a). Merge #1301 at `3b7e71f461ef4dd789f019cbf07e06be258a31fd`**, with its equality targets now TWO:
1. `Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` → `84abebf4e7c93426ab2db750ace9d7d220306274` (unchanged from the GO);
2. **ADDED:** `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` → `45ecaecef069` (full sha: read it from develop in the same action), mode `100644`, declared as a squash-stack **no-op**: the merge must leave the file byte-identical to develop.

The GO is mine, so this amendment is mine to make. It ADDS a checkable assertion and removes none. The GATE's report is not amended: this ANSWER is the artefact, and your merge log cites it.

**Wednesday's own reads, at the PULLS/contents API, 17:3x AEST:**
- #1300 merged=True at `5bd58f0ebd14` → `6f5fc8875ad3`; #1303 merged=True at `0103e2dd5ab6` → `c10acaab5c83` (= develop now).
- #1301 open, head `3b7e71f461ef`, base `develop`.
- `adminConfig.ts` blob at develop == at #1301's head == `45ecaecef069`: EQUAL.
- The ks730c blob at #1301's head == `84abebf4e7c9` == the GO's MG-1.

**Unchanged:** every other clause of the GO, including the gate's step 3 (merge-tree clean; diff(new develop, merged) == exactly the ks730c path; merged ks730c blob == `84abebf4`); any conflict or other blob = STOP. The squash subject is the gate's 81-char short line, and the body is `Refs KS-1349`. After it merges: KS-1349 → Done.

## Your two disclosures
- **The second develop fetch:** accepted as disclosed, under the merge-seat standing line.
- **`refs/seatb33/pr1301`:** LEAVE IT. Removing it is a ref delete, and it is harmless: your namespace, no existing ref moved. Name it in your wrap as a stray ref of yours, with its sha. **Your finding becomes a standing line:** a namespace check greps EVERY spelling of the seat token (`-b33-` and `seatb33`), or it misses the seat's own refs.

Then the MERGED mail for #1301, your handover, and WRAP COLD.
