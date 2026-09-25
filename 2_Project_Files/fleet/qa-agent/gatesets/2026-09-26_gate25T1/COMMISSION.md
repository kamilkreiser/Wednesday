# COMMISSION — DRAFT the round-25 TIER-1 batch gate kit "gate25T1" over FOUR PRs (Seat L8, wrapped). Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~06:2x AEST) as EIGHT READY PRs (#1267-#1274), cap 8 per kit, "decide each PR's tier from its
DIFF … if the eight split into tiers that need different gate weight, produce TWO kits". The drafter split them: this kit is the four TIER-1 PRs;
the sibling kit `gate25T2` carries #1268, #1270, #1271, #1273. Recorded here as the gate's commission; the QA agent reads it. Shape copied from
`gatesets/2026-09-26_gate24T2d/`: JSON pins, routing-file override, controls both ways with `--invert`; re-keyed to FOUR rows, no DB, no port.

## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)
| PR | ticket | head | files | tier — why, from the DIFF |
|---|---|---|---|---|
| #1267 | KS-1295 | `71f6f4d73cbde5b32f1564c9171eb1b705f77880` | credentialRepo.ts +13/-1, new ks1295 test +120 | **T1**: runtime change in the vc-issuer credential store's DB-unavailable path (a WARN naming a credential id — logs are a security surface). Lightest of the four; Wednesday may re-tier it to T2 (§ decisions in README). |
| #1269 | KS-1182 | `df21c6fd159f2a707d698e418946911f019ca9a0` | errorHandler.ts +59/-6, new ks1182 test +171 | **T1**: the service's terminal error middleware — status bound, headers, message echo (information exposure; H5 is a DoS shape). |
| #1272 | KS-849 | `34980b8e9ee22a36c658a03d9d763c48caeb9064` | kyc/src/index.ts +61/-33, new ks849 test +274 | **T1**: KYC verification writes (status, liveness, reviewer). Known limit ticketed as KS-1327 (status/currentLevel still overwritten at the 3 s timer; cell S3 pins it) — NOT a defect of #1272. |
| #1274 | KS-934 | `1a37bde12d55563f77e192519ca7db62461dbf6f` | m365 index.ts +74/-5, new ks934 test +203 | **T1**: outbound loop on the SSRF guard (row bound, wall clock, per-call deadline) and the published 200 body gains two fields. |

Each is ONE commit on develop `4db87c3e4b98`. Linear: all four link `contributes` (none closes). Titles with ` (#NNNN)`: 72 / 87 / 78 / 83 chars (≤ 92).

## Develop was MOVING during the draft
Seat M1 squashed #1262-#1266 onto `d7cdecf1` while the kit was drafted (merged 20:32:12Z-~20:34Z). The kit is pinned over the develop read at the pin,
**`df5e9f5da6d23411e7b38a79a58aa20c04b6afe2`** (#1266's squash), whose tree **equals M1's expected END tree `6942101caa7be149c1fc4a254eefc75af3607b86`**.
The launch action's step 3b re-pins on any further move.

## THE ONE OVERLAP WITH M1 — DECLARED
#1267 ∩ #1264 = `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (different hunks; #1264 is comment-only and merged). Over the pinned
develop #1267's merged blob `c93152727c39…` ≠ its head blob `94fae2659a6c…`; the equality target is the clean 3-way `git merge-file` (develop, parent,
head), measured equal. predict_gate25.py accepts it ONLY while develop's blob is the parent's or #1264's head blob; any other move REFUSES (control RE).
No other PR of either kit overlaps M1's five, each other, or the sibling kit (measured).

## The gate MUST
1. Base-invariant + PAIRWISE per PR over the launch develop; the declared-overlap target for #1267's credentialRepo.ts; #1264's comment preserved.
2. Every PR's red proof re-run (W1/W3; H-rows 11 of 14; S1/S3; N1-N3), restored by bytes.
3. Tier-1 runtime probes through the real module on 127.0.0.1 (port 0), stubs named: HDR-THROW / HDR-ON-500 (#1269), ENV-NAN / ENV-ZERO (#1274), MOCK-UPSERT-COLUMNS / SWALLOWED-SAVE-ERROR (#1272), LOG-CONTENT (#1267).
4. KS-849's limit graded as disclosed scope (KS-1327), never as a #1272 defect.
5. Fleet STOP by READ (28/0 · 6/0 · 49/0 · 60 of 60 on each push and on develop d7cdecf1); unchanged after the merge. Legs 3/4/8 NOT run.
6. GO string `GO: merge #1267, #1269, #1272, #1274 batch` (or the subset); merge SEAT (L8 wrapped). Routing `QA/Secuura-batch1267`.

## LEGITIMATE SHAPES — the drafter's predictions (the gate MEASURES every row)
Not a checker kit (all four are product changes); the table covers the runtime shapes each change will see.

| PR | shape | expected | predicted-by |
|---|---|---|---|
| #1269 | err.status 404 (http-errors) | 404, message echoed (expose true) | drafter READ |
| #1269 | err.status NaN | 500, process alive | drafter READ |
| #1269 | err.headers {"Bad Name": "x"} | setHeader THROWS ERR_INVALID_HTTP_TOKEN inside the handler — what the client gets is UNMEASURED | drafter LIVE (nodeprobe_1.out) |
| #1269 | err.headers {"X-Ok": "a\r\nInjected: 1"} | setHeader THROWS ERR_INVALID_CHAR (no header injection) | drafter LIVE |
| #1269 | status 200 + statusCode 404 | 500 (`??` picks 200) | drafter READ |
| #1274 | env unset | 50 / 10 000 / 2 000 | drafter READ |
| #1274 | env "abc" | NaN: deadline never trips; timeoutMs NaN -> setTimeout 1 ms (every row fails); LIMIT NaN to Postgres | drafter LIVE (arithmetic only) |
| #1274 | env "0" | DEADLINE 0 skips every row; MAX_ROWS 0 -> LIMIT 0 | drafter LIVE (arithmetic only) |
| #1272 | selfie inside 1500 ms | liveness kept | seat (S1) |
| #1272 | admin reject inside 3000 ms | still 'approved' — KS-1327, declared | seat (S3) |
| #1272 | dbSaveVerification rejects in the timer | silent (`.catch(() => {})`), 'approved' log NOT emitted | drafter READ |
| #1267 | DB unavailable | one WARN {credentialId, reason} | seat (W1) |
