# NEXT SEARCH 2026-09-17 (03:04–03:20 AEST): the next Ornith ticket

**BLUF: KS-1180 FITS as a PARTIAL (P-1005-1, P-1005-2, P-1005-4).** It is test-only, modifies the ks1073 test in place (188 lines, 7 hunks, +28/-4) and leaves product code untouched. It is graded by the #1005 gate's own GL tamper, byte-for-byte. The golden passed the real checker: **RESULT: PASS (7/7)**. P-1005-3 and R-1005-2 are product edits and are left out, so the PR says "Refs KS-1180 (P-1005-1, P-1005-2, P-1005-4)". KS-1181 was not briefed, because the search stopped at the first fit.
- Brief: `night/briefs/KS-1180.md` (new; no brief for this ticket existed). Input: `night/inputs/code_1180.json`. `build_input.sh` rc 0 at 03:20:04, tip `f7c2f4acb`, ~28.7K tokens, ctx 65536. Pins (all required): `product=Blockchain/Dev/services/api-gateway/src/routes/verification.ts ref=services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts test_file=services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts line=703 ctx=65536`.
- Not queued, not run. `queue.md`, `done.md`, checkers and other briefs were not touched. The Secuura porcelain read 0 at every reading. No gate clone or gatesets dir was entered.

## Pre-measure (sandbox-exec, off-host outbound denied; `scratchpad/next1180/premeasure.sh`, `premeasure.r3.out`)
**Origin moved mid-search:** `73d3fcb90` → `f7c2f4acb` (#1008, 03:17). #1008 touched `verification.ts` only at old `:994-1008`; the test blob `26f521ebd` did not change. Rounds 1–2 ran at `73d3fcb90`. **Round 3 re-ran everything at `f7c2f4acb`**, and the numbers below are round 3's.
- OLD file: tip 3/3. Under GL: 3/3 green, and the whole api-gateway suite 394/394 green, so P-1005-2 still holds. Under the gate's GT2: the guard stayed green, the 2 🔴 cells were red on the verdict and the control passed, so P-1005-1 still holds.
- Golden: tip 5/5 twice. **Under GL: 2 failed / 5 run, both 🔴 KS-1180 cells red by assertion** (`expected 'off-chain-only' to be 'on-chain'`), with the 3 KS-1073 cells green. Under GT2: 3 red on `tier 2 must be the tier that answered: expected +0 to be 1`, so the counter witnesses the tier. Under S1: only the 2 🔴 KS-1073 cells red. Each restore was by checkout or re-copy, with the sha matching.
- Whole suite: 394 → 396, no new red. Including tsc: OLD rc 2, 1× TS18046 at (157,10). Golden rc 0 with 0 errors.
- Checker on the brief's own fences: strict apply rc 0, applied == golden. PASS A1–A7. A3c 26 lines. A4 2/5 with assertion reds and controls green. A6 394→396 with NEW `[]`. A7 rc 0. No DECL-SPLICE.
- The premises in the brief (P1–P14) each name their instrument and time.

## Rejection table
| ticket | verdict | measured reason |
|---|---|---|
| KS-1180 P-1005-3 | REFUSED (in the partial) | Rewording the `verification.ts:353` comment is a product-file edit, and test-only A3 refuses a product hunk. |
| KS-1180 R-1005-2 | REFUSED (in the partial) | Moving the conjunct to `lookupSource` is a product change, and the ticket only says "consider". |
| KS-1181 | NOT BRIEFED (stopped at first fit) | Read-only facts: Backlog, 0 attachments, 0 comments. The target guard is **946 lines** at `f7c2f4acb`, so modifying it in place is the "very large existing file" refusal class. A new-file pin would have to rebuild `driveThroughRoute`. The #1006 report was not read. |

## Wrong in the tickets, gate report or harness (for Wednesday to file; IMPROVEMENTS.md not edited)
1. **Harness, new trap class:** `decl_splice.py` matches identifiers inside STRING literals. The `+` line `{ _source: 'originate' }` "used" `originate`. With the builder's DEFAULT ref (`ks1130-tier2-e1-twin`), the splice added `REAL_TX` + `originate` and the file failed to LOAD. All nine ks10xx/ks11xx verification refs splice at least one name. Only ks466, ks815 and notifications print `spliced 0`. This is broader than the 00:42 destructuring row.
2. **Harness:** the checker's standalone tsc on the test file is blind to TS18046: rc 0 on the OLD file, while an including program gives rc 2. P-1005-4's class cannot be seen by the checker.
3. **Harness:** `build_input.sh` refused KS-1180 because the `ks1073-…test.ts` ellipsis makes its basename scan see `test.ts` as a second site. `product=` works around it.
4. **Ticket:** "invisible to all 385 cells" was true at #1005's head. It is 394 at this tip, and still invisible. The ticket's Recommendation calls a product comment edit a "test pass".
5. **Brief caveat:** the checker grades only P-1005-2. P-1005-1's witness is test-side, and only the pre-measure's GT2 grades it.
