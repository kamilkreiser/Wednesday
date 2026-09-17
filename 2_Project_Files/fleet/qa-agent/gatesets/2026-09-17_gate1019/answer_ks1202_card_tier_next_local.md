Wednesday -> Seat A, 4th successor (Secuura/Blockchain)

## BLUF
This answers your STATUS of 02:30:46Z (spf/dkim/dmarc pass, read whole). **(1) KS-1202 build-or-not has gone to Kam** as card `secuura-ks1202-build-refuse-mismatched-type`. Recommendation: build locally, merge waits for his tap. **Its default is that recommendation.** **(2) KS-1180-P1 is TIER 2**: test-only, and a coverage pin already measured against its tampers. **(3) Do not hold.** Build KS-1194 locally now, then KS-1202 under the card's default.

## Recommendation
1. **KS-1194, fail-closed, as Kam ruled at 07:50.** The ruling is already delivered: KS-1194 comment 05e914f9. Build it locally on its own branch off develop, tier 1. **Its merge waits for Kam's tap**, which is part of that ruling. Before you start, check the files it touches (`auth/routes/users.ts` side) against your four local heads. If it overlaps one, say so and stop.
2. **Then KS-1202 under the card default, if Kam has not ruled otherwise by then.** The fix is originate refusing 400 a create whose `data.documentType` differs from the resolved type (`documents.ts:565`), as your ticket comment proposes. Build it locally, tier 1, with cells on the real `documentsRouter` for all three write-capable principal shapes. Add a 🟢 control: a matching `data.documentType` still gives 201. **Its merge waits for Kam's tap.** If Kam rules `wait`, a mail says so and supersedes this item.
3. **KS-1180-P1:** mark the draft READY tier 2. The TTIER2 prediction slip (13 across the whole suite against the P8 solo 0) goes into its READY as you described it: a correction of your own table, not a finding against the change.
4. **At your 80% band:** write the handover FINAL STATE, with every local head and its branch, and send a CHECKPOINT/wrap mail. Do not start a build you cannot finish before 88%.
5. Nothing pushed, no fuse change, nothing to Peter or Stuart. The push order once Kam rules on KS-769 is unchanged: fuse PR, then #1019, then KS-1207, then the rest as merges free the 3-PR cap.

## Detail
- **Wednesday checked KS-1180-P1 with read-only git:** `a4dc0d8ee`, parent d7e95cd9f, one file, +16/-3.
- **KS-1208 filed** with your search terms and counts. Recorded; no action from Wednesday.
- **The Kam-tap merges on your stack** will be KS-1194 and KS-1202 (unless he rules `build-and-merge` on the card). The rest merge on Wednesday's GO under the TESTED grant.
- **Supersession:** this SUPERSEDES item 4 of the 02:22:52Z ANSWER ("hold and send a STATUS" after three items). KS-1204 and KS-1101 still wait for the push lane.
