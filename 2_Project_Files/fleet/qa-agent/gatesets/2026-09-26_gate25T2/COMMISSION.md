# COMMISSION — DRAFT the round-25 TIER-2 batch gate kit "gate25T2" over FOUR PRs (Seats L7 wrapped, B 29th). Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~06:2x AEST) as EIGHT READY PRs (#1267-#1274), cap 8 per kit, tiered from the DIFF. The drafter
split them: this kit is the three TIER-2 PRs and the one TIER-3 PR; the sibling kit `gate25T1` carries #1267, #1269, #1272, #1274 (tier 1). Shape
copied from `gatesets/2026-09-26_gate24T2d/`: JSON pins, routing-file override, controls both ways with `--invert`; FOUR rows, no DB, no port.

## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)
| PR | ticket | head | files | tier — why, from the DIFF |
|---|---|---|---|---|
| #1268 | KS-1318 + KS-1142 + KS-1316 | `a8e0fca70ed41ef061cc99a325b610d27f08c7fb` | 2 files under packages/shared/src/__tests__ (+175/-33) | **T2** test-only; changes a CHECKER (the ks781 walk) -> THE READER RULE |
| #1270 | KS-1275 | `448b8b7fdd87a145acc895c4138811f34aa53c59` | lifecycleEventRepo.ts +7/-3, documents.ts +6/-4 | **T3** comment-only (20 changed lines, 0 non-comment by the drafter's line port); an already-gated follow-up of #1252 |
| #1271 | KS-1164 | `c9ea1dc1705f10f4b40ccc786604da6768a2c2fb` | systemTest/performance: gate/report.ts, runner/k6_docker.ts, 2 new tests | **T2** tooling (no product, no deploy surface) |
| #1273 | KS-1321 | `b800791a3295f048b40f920435b080a270c65106` | one originate test file (+72/-1) | **T2** test-only; changes a CHECKER (the description verb matcher) -> THE READER RULE |

Each is ONE commit on develop `4db87c3e4b98`. Pinned over develop `df5e9f5da6d23411e7b38a79a58aa20c04b6afe2` (tree == M1's expected END tree
`6942101caa7b…`). Path-disjoint from each other, from gate25T1 and from M1's five (measured; no declared overlap).

## Findings the drafter READ (the gate rules them)
- **MAGIC-WORD-CLOSES (#1271):** the body's "`#1200` closed KS-1164's original class" made Linear link KS-1164 as **`closes`** (every other PR in both kits: `contributes`). A squash with that body closes KS-1164.
- **TITLE-OVER-92 (#1271):** title 93 chars; squash subject 101 > MG-11's 92.
- **NO-REFS-LINE (#1268):** no `Refs` line; the body names foreign KS-1143.
- **KS1329-TSC (#1268):** L7 filed KS-1329 — three ks781 TS errors "after #1268 merges", in files no CI leg type-checks.
- **BACKTICK-SPAN (#1273):** the drafter's live probe of the extracted function flags `` `subversion` ``, `` `a new version` `` and a closing/opening back-quote pairing — over-reports on unnamed shapes; graded by reach.

## LEGITIMATE SHAPES (BRIEF_TEMPLATE §2a) — the two CHECKERS
### #1268 ks781 walk (KS-1316) — the gate measures each through the REAL walk
| shape | expected `guarded` | clause | predicted-by |
|---|---|---|---|
| guard in an uninvoked nested arrow (W9) | false | "no longer descends into an uninvoked nested function expression" | seat |
| arrow invoked by name (W10) / IIFE (W11) / handed to a call (W12) | true | invoked | seat |
| guard in a never-run branch (W13) | true, NOT DECIDED (declared) | general reachability is out of scope | seat |
| arrow assigned to a const, called later in the continuation | true | invoked by name | drafter READ |
| nested function DECLARATION, called | true? (a declaration is not an expression — which branch?) | UNMEASURED | drafter |
| `.call` / `.apply` / `.bind(...)()` / `fn?.()` / `await (async () => g())()` | true? | "invoked" — which syntactic forms count | drafter |
### #1273 namesVerbAsRouteToken (drafter's LIVE probe of the extracted function, nodeprobe_1.out)
| shape | read | named? | reading |
|---|---|---|---|
| back-quoted `version` / `/version` | ["version"] | cells | correct |
| "a new version" prose | [] | cell | correct |
| `share/transfer-custody/revoke` | [revoke, share, transfer-custody] | cell | correct (cell asserts it) |
| bare `share must use its own route` | [] | DECLARED not caught | declared scope |
| `` `subversion` `` / `` `a new version` `` / "`enum` … version` list`" | ["version"] | not named | over-report, by reach |
| `/revoke/confirm` | ["revoke"] | not named | route token — plausible |

## The gate MUST
1. Base-invariant + PAIRWISE per PR over the launch develop.
2. Red proofs re-run (#1268 ARM A/B, K1b arms, W9-only under develop's walk; #1271 S1/S2 + L1/L3; #1273 the three arms); restored by bytes.
3. THE READER RULE for #1268 and #1273; #1270's TIER-3 PROOF (emit with removeComments + a same-size DIFFERENT control).
4. Rule MAGIC-WORD-CLOSES and TITLE-OVER-92 with the squash body and subject the merger must use.
5. Fleet STOP by READ: 28/0 · 6/0 · 49/0 · 60 of 60 for #1268, #1270, #1273; #1271 NOT APPLICABLE (systemTest/, 11-line push log). Unchanged after merge. Legs 3/4/8 NOT run.
6. GO string `GO: merge #1268, #1270, #1271, #1273 batch` (or the subset). #1268/#1271: merge SEAT (L7 wrapped); #1270/#1273: B 29th if LIVE, else the merge seat. Routing `QA/Secuura-batch1268`.
