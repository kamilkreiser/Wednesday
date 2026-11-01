# Spark operator 43, 2026-11-01 (Secuura only)
Written by Wednesday from the operator's final message (its Write call was refused by the harness, and it correctly did not go around that). Every figure below is the operator's, citing the output files in this folder. Wednesday did not re-derive them.

## BLUF
Two KS-1868 sites PASS 7/7 and are HELD, both byte-identical to their goldens. Nothing was raised, pushed or merged; the only write verb was `git fetch` in the cache clone. Tip: develop 85c56a3d1eb92c8399dcfd3d6ee2a717cf356428 (fetch.out rc 0). Partition: prscan.out "19 PRs 108 files", control services/auth 7. No open PR touches demo-service or governance src (partition.out).

## Sites
- **O43-P1** `services/demo-service/src/routes/persona.ts:77`, the `POST /persona/switch` catch.
  - round_p1.out: `PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · 96s round, 32.267s model, 10700+1395 tok`, 7/7.
  - Dry-run rc 0; control PASS first time (83 s).
  - It logs, then answers a fixed generic 500. Product +6/-1; red 2/3, green 3/3; suite 91 -> 94.
  - **Wednesday's tier ruling: TIER 1.** The route is the demo persona-login path (calls `authenticatePersona`, proxies the refresh-token cookie), which is identity territory. Wednesday's own commission named this candidate without checking that, and the exclusion list should have caught it.
- **O43-P2** `services/governance/src/services/governanceService.ts:219`, the `dbGetProposal` catch (the operator's choice). It logs and returns undefined. The test is jest.
  - round_p2.out (second real round): `PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · 92s round, 23.339s model, 19729+1065 tok`, 7/7.
  - The first real round FAILED A7 only: `tsc --noEmit for services/governance: rc=134 after the patch (baseline rc=0) ... Abort trap: 6` (round_p2_try1.out, checker_p2_try1.out). That patch was also byte-identical to the golden. The same brief re-run passed; the cause is not diagnosed.
  - Product +7/-1; red 2/3, green 3/3; suite 179 -> 182.
  - **Wednesday's tier ruling: TIER 2** (DAO voting, not payments or auth by path; the gate has the final word). The A7 abort is recorded as an UNDIAGNOSED harness abort, not a pass. The raise seat runs tsc itself.

## Held
- night/READY_KS-1868-O43-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-DEMO-PERSONA-SWITCH-PASS-7of7_2026-11-01.diff.md
- night/READY_KS-1868-O43-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-GOVERNANCE-DBGETPROPOSAL-PASS-7of7_2026-11-01.diff.md
- The first hold_ready runs used the wrong golden argument. Those files were renamed `*.superseded-golden-not-compared` in night/; nothing was deleted.

## Left
- Governance reads at :255, :265, :275, :313, :342 and :448.
- demo-service reset.ts:64 and resetService.ts:71/:112 (whether the message reaches the response is unchecked).
- nft-certificate minting.service.ts and blockchain-verifier.service.ts.
- Governance dbSave* at :167/:187/:205 are excluded: they rethrow.
- Screens: screen_all 322 lines, screen_cand 107.

## UNMEASURED
eslint on the new files; a real service boot; why tsc aborted; the other ~300 sites; the S9 brief; whether such a value ever occurs.
