# COMMISSION — DRAFT the round-26 TIER-2 batch gate kit "gate26T2" over 8 PRs. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~09:3x AEST) as TEN READY PRs (#1245, #1275-#1283; cap 8 per kit; "decide each PR's TIER from its DIFF"),
plus #1284 (KS-730 PR 3 of 3) at 09:5x, #1274 (KS-934 round 2 of 2) at 10:2x and #1268 (KS-1318/1142/1316 round 2 of 2) at 10:3x, #1261 (KS-1293 round 2 of 2) at 10:5x. The split: gate26T1 = #1274, #1280-#1284 (tier 1), gate26T2 = #1245, #1261, #1268, #1275-#1279 (tier 2; 8 = the cap)
(tier 2). This kit is gate26T2; its sibling is gate26T1 (#1274, #1280, #1281, #1282, #1283, #1284). Shape copied from `gatesets/2026-09-26_gate25T1/` and `…_gate25T2/`: JSON pins, routing-file
override, controls both ways with `--invert`; re-keyed to N rows, per-PR merge-bases, a declared commit count, a NOT-STACKED check and the key scan.

## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)
| PR | ticket | head | commits on merge-base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |
|---|---|---|---|---|---|---|
| #1245 | KS-1313 | `cb31a58c190f86aad49b402c1c001429c037ed24` | 3 on `6e2a00bfed57` | unitSuiteSlotIndependence.test.ts +452/-6, capturedChildOutput.ts +64/-0 | 98 | **T2**: test tooling only (the child-vitest summary reader). A CHECKER: THE READER RULE. ROUND 3 OF 3 — at the cap. |
| #1261 | KS-1293 | `0b2fdbb1b8195d4f73467508f8eb6a4c3781b81a` | 2 on `fa25c9b10fb4` | ks1293-originate-suite-is-hermetic.test.ts +303/-0 | 80 | **T2**: one originate test file (the suite pins its own hermeticity); a CHECKER: THE READER RULE. ROUND 2 OF 2 — at the cap (gate24T2c NO GO B-1261-1 REVERT-SKIPS). PR body NOT refreshed for round 2. |
| #1268 | KS-1318 + KS-1142 + KS-1316 | `5ac42fafeee11dec596e7e7d833ac82b8b478790` | 2 on `4db87c3e4b98` | ks781-p3-3-body-parser-order.test.ts +197/-4, entrypoint-corpus.test.ts +73/-29 | 90 | **T2**: two packages/shared test files; a CHECKER (the ks781 walk): THE READER RULE. ROUND 2 OF 2 — at the cap (gate25T2 NO GO on the alias shape). Round 2 adds a THIRD rule (returned escape) accepted as a SHAPE. |
| #1275 | KS-1179 | `d852e56b912f8a14b8f2cf01639dc37f9c9ff6a2` | 1 on `4db87c3e4b98` | ssrf-guard.ts +17/-9, ks1179-dns-timer-cleared.test.ts +57/-3 | 102 | **T2 on condition**: ssrf-guard.ts is a T1 surface, but the diff is comments + ONE parameter annotation (2 non-comment lines, READ). EMIT PROOF owed; a different emit = NO GO here. |
| #1276 | KS-794 | `737a4069c6316b10a89fa9c499fac6c2cb20f619` | 1 on `d7cdecf1d2ee` | ks794-verify-file-fields-are-published.test.ts +101/-0, secuura-api.yaml +25/-7, originate.openapi.ts +44/-6 | 67 | **T2**: published contract (registry + committed yaml); the schemas are registered for the spec only, not validated at runtime (READ). |
| #1277 | KS-1319 | `702171eaadbeb0a9d830237ec6fd86219311477c` | 1 on `4db87c3e4b98` | walkTimeouts.test.ts +109/-22 | 104 | **T2**: one test file. A CHECKER (the walker derivation + the wiring check): THE READER RULE. |
| #1278 | KS-1314 | `c321bcce2a9ae7e2c3d5da65f3c1d64fc3295de9` | 1 on `4db87c3e4b98` | sheddingCeiling.test.ts +66/-3, readYamlRouting.ts +69/-2 | 116 | **T2**: test support + a test file, systemTest/. A CHECKER (parserImportSites): THE READER RULE. |
| #1279 | KS-1306 | `dabde931df5e02e45272b70f2fe75fb3dab6ed38` | 1 on `d7cdecf1d2ee` | ks597-issuer-organization-id.integration.test.ts +69/-5 | 68 | **T2**: one integration test file (INSERTs into Postgres). Its DB leg is NOT RUN in this gate (no Docker); the no-DB guard is measurable. |

Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out). No PR is stacked on another (measured: no head is another's ancestor; every
pair's merge-base is on develop).

## Develop at the pin
Pinned over develop **`00de57baeb405d0081fe8b6f192bd40d35acef61`** (tree `fb4d9f1691451db2cdfab3cae22db2fd675f0f80`), READ by ls-remote and fetched. END_TREE **`d400f96a955ebdfb427fbde2951cd95fc9af13d3`** (14 files changed, 1646 insertions(+), 96 deletions(-)), identical in all 40320 orders. END_TREE_WITH_SIBLING
**`5807048824a8e15dce62d8a7a6b0d62e2160a4c1`** (develop + both kits, either kit first). The launch action's step 3b re-pins on any move (Seat M1 merges on GOs).

## Overlaps — NONE declared, NONE found
No kit PR's paths meet another kit PR's, the sibling kit's, the develop move since its merge-base, or Seat B 30th's in-flight PRs as read at the pin ().
KS-730 PR3's worktree (s-b29-ks730c: adminConfig.ts + the ks730c test) was censused disjoint at the first pin, then became #1284 in gate26T1; #1274, #1268 and #1261 were in flight at the first pin and joined at their round 2 (T1 / T2 / T2).
Nothing of Seat B 30th is in flight at the final pin; predict_gate26.py re-censuses at every re-pin.

## Fleet STOP (READ, bounded region, NOT-FOUND control)
- #1245 `s-b29-pr1245-ff-cb31a58c190f-push.out` (7 lines, rc 0): a systemTest/ push, no preflight — NOT APPLICABLE
- #1261 `s-b30-ks1293-ff-0b2fdbb1b819-push.out` (1296 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1268 `s-b30-ks1318-ff-5ac42fafeee1-push.out` (1296 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1275 `s-l7-ks1179-d852e56b912f-push.out` (1300 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1276 `s-b29-ks794-737a4069c631-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1277 `s-l7-ks1319-702171eaadbe-push.out` (1300 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1278 `s-l7-ks1314-c321bcce2a9a-push.out` (11 lines, rc 0): a systemTest/ push, no preflight — NOT APPLICABLE
- #1279 `s-b29-ks1306-dabde931df5e-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- On develop (Seat L8, d7cdecf1; carried by the gate25 reports): 28/0 · 6/0 · 49/0 · 60 of 60. No path in either kit is a shell suite: unchanged after the merge.

## LEGITIMATE SHAPES — the drafter's predictions (the gate MEASURES every row)
| PR | shape | expected / predicted | predicted-by |
|---|---|---|---|
| #1245 | LIVE U1 (status 1 signal null error null; gap ["     Errors  1 error"]) | oracle {2,0}; round 3 NULL | drafter LIVE (liveshape_live_1.out) |
| #1245 | LIVE U2 (status 1 signal null error null; gap ["     Errors  1 error"]) | oracle {2,0}; round 3 NULL | drafter LIVE (liveshape_live_1.out) |
| #1245 | LIVE U3 (status 1 signal null error null; gap ["     Errors  1 error"]) | oracle {2,1}; round 3 NULL | drafter LIVE (liveshape_live_1.out) |
| #1245 | LIVE X1 (status 1 signal null error null; gap []) | oracle {1,1}; round 3 {1,1} | drafter LIVE (liveshape_live_1.out) |
| #1245 | LIVE X2 (status 1 signal null error null; gap []) | oracle {1,1}; round 3 {1,1} | drafter LIVE (liveshape_live_1.out) |
| #1245 | LIVE X3 (status 1 signal null error null; gap []) | oracle {1,1}; round 3 {1,1} | drafter LIVE (liveshape_live_1.out) |
| #1245 | round 2 vs round 3 on U1 | oracle {2,0} / round2 {2,0} / round3 NULL | drafter LIVE (liveshape_r2cmp_1.out) |
| #1245 | round 2 vs round 3 on U2 | oracle {2,0} / round2 {2,0} / round3 NULL | drafter LIVE (liveshape_r2cmp_1.out) |
| #1245 | round 2 vs round 3 on U3 | oracle {2,1} / round2 {2,1} / round3 NULL | drafter LIVE (liveshape_r2cmp_1.out) |
| #1245 | REAL CAPTURES: 42 read, 0 WRONG | | drafter (liveshape_1.out; gate24T2c captures, or SYN = composed, NOT real) |
| #1245 | {7,0}  SYN-H1s killed after a lookalike INCLUDING Start at (stdout only; childSuiteCounts refuses on status 143) | | drafter (liveshape_1.out; gate24T2c captures, or SYN = composed, NOT real) |
| #1245 | {7,0}  SYN-H4s process.on(exit) writes a COMPLETE lookalike AFTER vitest's real block (status 1, NOT refused) | | drafter (liveshape_1.out; gate24T2c captures, or SYN = composed, NOT real) |
| #1245 | NULL   SYN-H4t exit-hook writes only `   Start at  hh:mm:ss` after the real block | | drafter (liveshape_1.out; gate24T2c captures, or SYN = composed, NOT real) |
| #1245 | NULL   SYN-ERRLINE an `Errors  1 error` line between Tests and Start at | | drafter (liveshape_1.out; gate24T2c captures, or SYN = composed, NOT real) |
| #1245 | NULL   SYN-TYPEERR a `Type Errors  1 error` line between Tests and Start at | | drafter (liveshape_1.out; gate24T2c captures, or SYN = composed, NOT real) |
| #1245 | {1,1}  SYN-CRLF the real S14 block with CRLF line ends | | drafter (liveshape_1.out; gate24T2c captures, or SYN = composed, NOT real) |
| #1261 | the env line of ks1228 / ks1264 / ks1213 deleted in the REAL files | CONFIGPINNED reds naming the file (round 1: stayed green) | seat (RS1/RS2/RS3a on copies) + Wednesday ruling |
| #1261 | a new anchoring-touching file absent from the manifest | MANIFEST-DRIFT reds naming it | seat |
| #1261 | the key assigned only inside a finally block (ks1213) | not an import-scope base -> offender (RS3a) | seat |
| #1268 | W14-W18 (alias, .call/.apply, .bind()(), new Promise(cb), mk()()) | guarded:true | seat (cells) + Wednesday ruling |
| #1268 | W9 / W19 (stored in an object, never called) | guarded:false (the overwide arm reds exactly these two) | seat |
| #1268 | `const mk = () => () => guard(); mk();` (returned, NEVER called) | UNKNOWN — the third rule may read it true (an over-report): the gate measures | drafter READ (a question, not a prediction) |
| #1268 | entrypoint-corpus.test.ts round 1 vs round 2 | the same blob 8a4ce36a3a96 | drafter READ (predict_1.out) |
| #1275 | transpile(merge-base) vs transpile(head), removeComments | byte-equal (seat: 12,137 vs 12,137) | seat |
| #1277 | setupFiles commented out, OLD check / NEW check | 7/7 green / the wiring cell reds | seat |
| #1278 | a 136-char import through the package prettier | 12 lines; parserImportSites finds it (it returned [] before) | seat |
| #1279 | DSN host 203.0.113.7 / compose port on 127.0.0.1 | refused before connecting | seat + drafter READ |
