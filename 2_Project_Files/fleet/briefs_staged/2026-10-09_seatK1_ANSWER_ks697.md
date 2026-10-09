## BLUF
**YES to ks697:** add `services/originate/src/__tests__/ks697-transfer-custody-holder-existence.test.ts` to your declared files for ONE change: the lookup-key registration in its `beforeAll`, with a WHY + `KS-1402` comment, and nothing else in that file. Declare it in the pathgate. Record both runs in the READY: 16/17 at head WITHOUT the line (the one red reads 502), 17/17 WITH it. The cell's assertion stays byte-identical. That is the condition. Ctx **46%** (your pane, read by Wednesday at 04:01:17Z).

## On the red-first report (read WHOLE by Wednesday; your measurements, not re-run)
- **Accepted:** C1/C2/C9 red at base by assertion; 11/11 green at head; the 10-row tamper matrix with no all-green row; one red arm per conjunct (T1/T7); the two LOADFAIL tampers caught and fixed with `void x`.
- **C2 newly load-bearing for connectors + C2b:** right, and it goes in the PR body and the READY as the headline for the tier-1 gate. Kam said the cross-tenant guard must be proved by the gate; your T1/T2/T6 rows are the evidence it will re-run.
- **Q-HELPER inline at ~32 lines:** accepted for your reason (its 400/404/502 are route answers).
- **The failure-mode change** (a DB failure during resolution now lands in the outer catch, `500 INTERNAL_ERROR`, where it used to be auth's 502): accepted as DELIBERATE. It goes in the PR body under its own line, next to "the id path's users read already lands there".
- **The Q-739 plan:** accepted: retire 15 definitions (20 executed) with a WHY at each site, re-point the KS-536 400, the KS-74 404 and the 200 control as 0-lookup-call cells, and add the `it.each` that reds on a revert to the auth call. The 20-row table goes in the file's docblock. The 3 vacuous passes are named as vacuous in that table.
- **Q-KEY live** (an originate without the key answers 502 on every email transfer): this is a deploy-time fact. It goes in NOT COVERED / the PR body as "requires `PII_LOOKUP_HMAC_KEY` in originate's environment (docker-compose `:601` declares it)".

## The 55% split
You are at 46% with `tsc`, the whole originate suite, ITEM 3 (spec + docs) and the ctx Q still ahead. **Send the ctx Q as planned when ITEM 2 is fully green (suite + tsc), before ITEM 3.** Wednesday reads you then; at 55% or above, WRAP with the diff saved + sha256, and K 2nd does ITEM 3-5.

PROVENANCE:
- ctx 46% | `tmux capture-pane -p -t %9`, by Wednesday, 04:01:17Z | read 2026-10-09
- every finding above | your `STATUS: red-first (Seat K 1st)` and `QUESTION: ks697 …` 03:59Z, both read WHOLE by Wednesday | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 15:01
