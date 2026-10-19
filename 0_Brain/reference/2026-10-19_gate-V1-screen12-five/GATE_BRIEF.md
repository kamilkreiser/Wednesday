# Gate brief: GATE V1 = the SCREEN_12 five, batched, Opus, round 1 of 2

Commissioned by the Wednesday seat after R 52nd's READY of 05:03Z (copied beside this brief: R52_READY_0503Z.txt; it is the author's CLAIM; its §4-§5 are about #1597, NOT in this gate, ignore them). Routing v1.0 row G1: three tier-1 PRs (an admin route's auth mount, a health route's error log, the auth service's test-token gate) plus two tier-2 test-only PRs in one session. Secuura only.
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project path: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files (READ ONLY: ls-remote, show, diff, cat-file; `git clone --shared` into YOUR scratch and work there).

**METHOD:** gate Q1's method and format: `0_Brain/reference/2026-10-19_gate-Q1-screen11-four/GATE_BRIEF.md` and its verdict.md.

develop = 7e2f8157cec243a6255aab2c4fc8678063da317b (moved since R raised: #1607, 4 anchoring files). Re-read it.

| PR | ticket | head (Wednesday ls-remote, equal to R's) | tier |
|---|---|---|---|
| #1608 | KS-1506 steps 1-2 | ce638c916fc7d550479ceb4e6f612998a1c14774 | 1 |
| #1609 | KS-1539 info-reader half | 8e68a262437a60bc4f44f770d530d3115881dde3 | 1 |
| #1610 | KS-623 | 940b84a9838d9c08a760d06278d214b0b904cfad | 1 |
| #1611 | KS-1637 Minor 1 (test only) | 70bea5c98f0aa995744a9b1a8e0594f2b0d22952 | 2 |
| #1612 | KS-1503 Minor 1 (test only) | f0b8fbbe663fd0d3e77d60e55167e799f4f2ea2e | 2 |

## Named questions (each with its instrument, or "unmeasured")
1. **#1608:** `/api/admin/audit` now sits behind `authenticateToken(true)` (api-gateway `src/index.ts`). Does any legitimate caller lose access (who calls this mount: other services, the admin UI, scripts, tests)? Does the 401 vs 403 behaviour match the router's own checks? R's reading of `middleware/audit.ts:85` (EXCLUDED_PREFIXES = audit-row writes, not auth): confirm.
2. **#1609:** can the logged `errorClass` ever carry the stored allow-list bytes? R's honest boundary: a thrown value whose CLASS NAME came from data would. Is any such throw reachable on that path?
3. **#1610 (KS-623):** test tokens accepted only when NODE_ENV is development or test. R measured both boxes read-only: NODE_ENV=development, ENABLE_TEST_TOKENS=false (not re-measured by Wednesday; do not re-measure the boxes, it is not needed for the code question). Questions: does any OTHER service or harness rely on test tokens with NODE_ENV unset or e.g. 'staging' (CI, e2e, scripts, docker-compose files, systemTest)? Does the gateway's own parseTestToken match, as the comment claims?
4. **#1611, #1612 (test only):** confirm R's mutant evidence (each new cell kills a mutant that SURVIVES develop's existing cells) by re-running at least one mutant per PR yourself.
5. Each PR: red-first reproduced, suite count at the landing parent (api-gateway and auth: vitest; R's baselines in its mail), `git apply --check` on live develop, the chained landing tree of all five (no collisions), overlap with open #1597.
6. **Every touched service's suites: RUN or named NOT tested** (api-gateway, auth: unit and integration).

Verdict file: verdict.md in this folder; first line `VERDICT:` per PR; last line the sha256 of the file with its first and last lines removed. Scratch: your own v1/ under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c4419525-d2e2-49d0-8b3f-577263d823bb/scratchpad/. Findings only: no fixes, no GitHub or Linear writes, nothing under !CODING, no `cd`, no `rm`, no stderr to /dev/null, no Docker, no SSH to any box.
