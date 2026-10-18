# Gate brief: GATE N1 = DELTA gate for #1589 (KS-1628 PR 2 of 2, retire the public POST /api/documents/:id/verify), TIER 1, ROUND 2 of 2

Commissioned by the Wednesday seat, 2026-10-19 ~09:2x AEDT. Model routing v1.0 row G1 (tier 1: a public verify route removed, on a surface with a live honest-labelling defect, KS-1634). **Round 2 of 2 under the two-NO-GO cap:** if this is NO GO, the closed instances ship and the residue is ticketed; there is no third round without Kam.
Kam ruled card `secuura-ks1628-retire-deprecated-verify-route-1019` = c "Retire it now". Seat R 50th built the fix round.
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

| what | value (Wednesday `git ls-remote` ~09:2x; re-read it yourself) |
|---|---|
| #1589 head now | ae9dd501b6971a5eb6e0db6bafce0560b2d7d8df |
| #1589 head gated in round 1 (gate M1) | 53cb4ec76ea7b5716089af5c4a9c5f6166a55de2 |
| develop | f95ad12fe5c22f8d037e7139d052363422463c79 (#1588 + #1587 merged on M1's GO) |
| round-1 verdict | 0_Brain/reference/2026-10-19_gate-M1-pr1588-1587-1589/verdict.md (#1589 = GO WITH NOTE as a fix round: Major 1, no gateway removal pin; Major 2, the quarantine README omits ks1057's anchor_failed heal and ks1069's KS-1129 O1 block; minors on three stale doc tables, the /api index text and the dead meetsVerificationLevel dep) |

**Author's claims (NOT evidence), from R 50th's READY at 22:13Z:**
- The delta is 5 files, +214/-5: a NEW suite `services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` (6 cells: G1 router stack, G2 who answered, G3 the published /api index; controls G-C1..G-C3); a doc comment in gateway `routes/verification.ts`; SERVICES.md, docs/QUICK-REFERENCE.md and deployment/azure/RUNBOOK.md.
- The quarantine README (NOT tracked in the repo) is `5_Project_History/quarantine/2026-10-19-seatR49-ks1628-pr2/README.md`, now 69 lines: ks1057 ENDED by design (originate verification.ts:427, :436-437, a code reading), and ks1069's O1 block with L1/L6 LOST -> KS-1634.
- api-gateway 1106/1106 and originate 1442/1442 on a predicted landing tree 1ca89b2b5b72; red-first G1-G3 red on develop's pre-removal files; leg 16 rc 0; ESLint 0 with a positive control.

## Gate
1. **The delta only, plus anything it reaches.** Diff ae9dd501b697 against 53cb4ec76ea7 by hunk; nothing outside the 5 named files. Confirm the product change is a doc comment only.
2. **Major 1 closed?** Run the new suite yourself, red-first: against develop's pre-removal gateway `verification.ts` + `index.ts`, G1/G2/G3 must red for the RIGHT reason (an assertion, not an import error); the controls must stay green in both arms. Then **plant the regression M1 named**: re-add a stub of the removed `POST /api/documents/:id/verify` handler at the PR head and confirm a cell reds. Also try a stub that answers 404 itself, to test G2's discriminator (R names G2's content-type rule as the weakest link: judge it).
3. **Major 2 closed?** Read the README (outside the repo, path above) against M1's finding: every property of ks1057 and ks1069 has a row saying RE-HOMED (file:line of the cell), ENDED (with the reason) or LOST (with a ticket). Check the citations at develop: :427, :436-437 for ENDED; for LOST, the L1/L6 sites (:712, :1191).
4. **THE NAMED QUESTION, Wednesday's, and the one that decides the ruling:** does retiring the gateway route move ANY caller from the gateway's stricter handler onto originate's chain-first fallback (the `rows.length === 0` branch at verification.ts ~:704 and its /verify twin ~:1185), the path where KS-1634's live defect sits? R's reason for proceeding is that "the removed handler was never on that code path". **Wednesday has NOT ratified that and neither should you: measure it.** Enumerate who called the old route and what they would call instead (connectors, sdk, frontends, packages, scripts, systemTest, docs; M1 found no code caller, so say whether that still holds at ae9dd501b697), and whether any successor route they would now reach uses the chain-first fallback. Answer in one sentence at the top of FOUND: "moves callers onto the chain-first path: YES / NO / UNMEASURED because <x>".
5. **R's three judgement calls:** RUNBOOK.md:263 repointed rather than deleted (is the symptom still real on the successor?); `meetsVerificationLevel` kept with KS-1635 named (confirm `enforcement.ts:54` is called at `:153`); G2's discriminator (item 2).
6. Suites: api-gateway and originate on YOUR predicted landing tree with `packages/shared` rebuilt in your clone; compare with R's 1106 / 1442. Merge prediction of ae9dd501b697 onto develop f95ad12fe5c2 (tree id), and against #1568 (J, head 09588895db75, held) in both orders.

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/n1/. Create it and use nothing else in that scratchpad: spark_l1l6/ and wcl_test/ belong to other work.** Clone there with `git clone --shared` from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git in YOUR clone, fetch with that checkout's `core.sshCommand` (read it with `git config --get`; add `-o ServerAliveInterval=30` for long fetches). Build `packages/shared` before any suite.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker, no access to the kintsugi or demo servers.
- Never cd. Delete nothing outside n1/. Run every loop from a script FILE with `/bin/bash`. An EXIT trap that restores a file uses an ABSOLUTE path. Never send stderr to /dev/null. Every zero needs a control that fired.

## Output
- Write 0_Brain/reference/2026-10-19_gate-N1-pr1589-r2/verdict.md.
- Line 1: `VERDICT: GO / GO WITH NOTE / NO GO at head <full sha> (round 2 of 2)`.
- Line 2: the item-4 sentence.
- Line 3: `sha256/16: <16 hex>` of the report with line 3 deleted.
- Then FOUND / TESTED / HOW, the README property table (property, old cell, status, new home or reason or ticket, checked how), NOT tested, and severities with file:line. Final lines: `MODEL: <your model id>` and `WALL-CLOCK: <minutes>`.
