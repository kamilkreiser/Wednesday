# COMMISSION — DRAFT the round-26 TIER-1 batch gate kit "gate26T1" over 6 PRs. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~09:3x AEST) as TEN READY PRs (#1245, #1275-#1283; cap 8 per kit; "decide each PR's TIER from its DIFF"),
plus #1284 (KS-730 PR 3 of 3) at 09:5x, #1274 (KS-934 round 2 of 2) at 10:2x and #1268 (KS-1318/1142/1316 round 2 of 2) at 10:3x, #1261 (KS-1293 round 2 of 2) at 10:5x. The split: gate26T1 = #1274, #1280-#1284 (tier 1), gate26T2 = #1245, #1261, #1268, #1275-#1279 (tier 2; 8 = the cap)
(tier 2). This kit is gate26T1; its sibling is gate26T2 (#1245, #1261, #1268, #1275, #1276, #1277, #1278, #1279). Shape copied from `gatesets/2026-09-26_gate25T1/` and `…_gate25T2/`: JSON pins, routing-file
override, controls both ways with `--invert`; re-keyed to N rows, per-PR merge-bases, a declared commit count, a NOT-STACKED check and the key scan.

## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)
| PR | ticket | head | commits on merge-base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |
|---|---|---|---|---|---|---|
| #1274 | KS-934 | `8e94f5fb3e6d8ef21ba2007fde92d3ea0b5c942d` | 2 on `4db87c3e4b98` | index.ts +107/-6, ks934-teams-notify-request-path-bound.test.ts +346/-0 | 83 | **T1**: an outbound loop on the SSRF guard (row set, wall clock, per-call deadline, and now WHICH rows a call reaches) + the 200 body. ROUND 2 OF 2 — at the cap (gate25T1 NO GO on F-1274-1 LIMIT-TRUNC). |
| #1280 | KS-1129 | `12c197a9215e3156d48cf47fbcec09292619cb68` | 1 on `d7cdecf1d2ee` | ks1129-heal-persists-a-number.test.ts +228/-0, verification.ts +31/-1, verificationV2.ts +6/-1 | 71 | **T1**: what the verify path PERSISTS into the document blob (a string height makes the gateway answer off-chain); TWO heal sites (verification.ts + verificationV2.ts). |
| #1281 | KS-1074 | `c3374e3129ccaca29a9beeafe2d0098ffc86796d` | 1 on `d7cdecf1d2ee` | ks1074-every-rebuild-writer-carries-threadtoken.test.ts +180/-0, anchorStateSync.ts +37/-1 | 78 | **T1**: five writers that REPLACE the blockchain column wholesale — data destruction of threadToken on the success path. |
| #1282 | KS-730 | `34a67a9e48057a0d4939527a4b721a7a5605e4ab` | 1 on `d7cdecf1d2ee` | systemErrors.ts +28/-4, ks730a-ingest-500-never-answers-err-message.test.ts +85/-5 | 72 | **T1**: information exposure — admin 500s returned err.message off-production; now logged instead (1 of 3). |
| #1283 | KS-730 | `f92b7c19e98d888b39674eb0b39461ed214a37d3` | 1 on `d7cdecf1d2ee` | ks730b-gdpr-500-never-answers-err-message.test.ts +152/-0, gdpr.ts +44/-15 | 64 | **T1**: the same class on fifteen GDPR routes, plus a new logger import in a file that said it must not have one (2 of 3). |
| #1284 | KS-730 | `dfc2468a547f0bb3d4995404942736312384539b` | 1 on `d7cdecf1d2ee` | ks730c-adminconfig-500-never-answers-err-message.test.ts +204/-0, adminConfig.ts +69/-46 | 71 | **T1**: the same class on forty-six admin-configuration routes (3 of 3; Seat B 30th; added by Wednesday 09:5x). Four unconditional leaks remain = KS-1334. |

Linear: every PR links its ticket as `contributes`; none `closes` (linear_reads_1.out). No PR is stacked on another (measured: no head is another's ancestor; every
pair's merge-base is on develop).

## Develop at the pin
Pinned over develop **`00de57baeb405d0081fe8b6f192bd40d35acef61`** (tree `fb4d9f1691451db2cdfab3cae22db2fd675f0f80`), READ by ls-remote and fetched. END_TREE **`76e2be58f4e0ffe46ba10246c467421780ba64fc`** (13 files changed, 1517 insertions(+), 79 deletions(-)), identical in all 720 orders. END_TREE_WITH_SIBLING
**`5807048824a8e15dce62d8a7a6b0d62e2160a4c1`** (develop + both kits, either kit first). The launch action's step 3b re-pins on any move (Seat M1 merges on GOs).

## Overlaps — NONE declared, NONE found
No kit PR's paths meet another kit PR's, the sibling kit's, the develop move since its merge-base, or Seat B 30th's in-flight PRs as read at the pin ().
KS-730 PR3's worktree (s-b29-ks730c: adminConfig.ts + the ks730c test) was censused disjoint at the first pin, then became #1284 in gate26T1; #1274, #1268 and #1261 were in flight at the first pin and joined at their round 2 (T1 / T2 / T2).
Nothing of Seat B 30th is in flight at the final pin; predict_gate26.py re-censuses at every re-pin.

## Fleet STOP (READ, bounded region, NOT-FOUND control)
- #1274 `s-b30-ks934-ff-8e94f5fb3e6d-push.out` (1296 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1280 `s-b29-ks1129-12c197a9215e-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1281 `s-b29-ks1074-c3374e3129cc-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1282 `s-b29-ks730a-34a67a9e4805-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1283 `s-b29-ks730b-f92b7c19e98d-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1284 `s-b29-ks730c-dfc2468a547f-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- On develop (Seat L8, d7cdecf1; carried by the gate25 reports): 28/0 · 6/0 · 49/0 · 60 of 60. No path in either kit is a shell suite: unchanged after the merge.

## LEGITIMATE SHAPES — the drafter's predictions (the gate MEASURES every row)
| PR | shape | expected / predicted | predicted-by |
|---|---|---|---|
| #1280 | toBlockHeight(null) | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight(undefined) | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('4242') | 4242 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight(' 42 ') | 42 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('') | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('abc') | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight(0) | 0 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('0') | 0 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('0x10') | 16 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('1e3') | 1000 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('-1') | -1 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('4242.5') | 4242.5 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight('9007199254740993' (MAX_SAFE+2)) | 9007199254740992 | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight(9007199254740993n (BigInt)) | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight(Infinity) | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight(NaN) | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight(true) | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | toBlockHeight({}) | null | drafter LIVE (nodeprobe_1.out: the function extracted from the head blob; the heal paths NOT run) |
| #1280 | heal with blockNumber '4242' / '' / 'abc' / 0 | persisted 4242 / stored height / stored height / 0 | seat (cells) |
| #1281 | prior threadToken 'tt' / '' / 0 | carried by all five writers (`!= null`) | seat (cells) + drafter READ |
| #1281 | prior blob with no threadToken | NO threadToken key written | seat (cell) |
| #1281 | token minted between the per-write getDocument and updateDocument | ERASED (a residual race) | drafter READ |
| #1282-#1284 | NODE_ENV unset / development / demo / test, service throws LEAK | parent: LEAK in the 500 body; head: constant body, LEAK in logger.error | seat (cells) + drafter READ |
| #1282-#1284 | NODE_ENV production, service throws LEAK | parent and head: constant body | drafter READ |
| #1284 | LEAK message containing 'does not exist' | 200 from the benign branch; fail500 never runs (the FIXTURE TRAP; C1 must red) | seat + Wednesday |
| #1284 | the four KS-1334 sites (lines 1859, 2031, 2152, 2158 at head) | err.message in the response in EVERY environment | seat (C4) + drafter READ |
| #1283 | line 532 of gdpr.ts at head | still "Deliberately no logger import in this file" (STALE-COMMENT-532) | drafter READ |
| #1274 | 60 healthy rows, defaults, repeated calls | call 1: 50 attempted, truncated true; call 2: the 10 never-notified rows first (NULLS FIRST) | seat + drafter READ |
| #1274 | 50 always-failing rows + 10 healthy | the 10 are NEVER reached (R3 pins it; KS-1335) | seat + drafter READ |
| #1274 | MAX_ROWS="abc" | LIMIT NaN; truncated can never be true | drafter READ (arithmetic) |
| #1274 | MAX_ROWS="0" | LIMIT 1; truncated TRUE, nothing notified, total 0 | drafter READ (arithmetic) |
