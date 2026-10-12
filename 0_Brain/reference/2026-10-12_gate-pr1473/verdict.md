# Gate verdict: PR #1473 (KS-1018 item 3, option A)

**Head:** `2026b2e6d0c8b6b1ca33ba685a1c90077063220a` | **Verdict: GO WITH NOTE** | Opus QA gate, 2026-10-12, read-only

## Provenance
- I made my own clone (`--no-hardlinks`) in the scratchpad (`g1473/repo`) and fetched `develop` plus `refs/pull/1473/head`, read-only. Push URL set to `NO_PUSH`. I wrote no refs in the shared repo.
- `ls-remote` shows develop is **still `f9c7880f9`**. The brief said develop had moved; it has not. The PR's merge-base is `2d151b08e`, and develop is 5 commits ahead of it in auth (`auth.openapi.ts`, two test files, none of them overlapping).
- **Predicted merged tree: `e23a2959ea8d2caf8885b6484e981d6af39c7dd4`.** This matches the seat's prediction.
- node_modules were APFS-cloned from gate g1471. Both lockfiles are byte-identical: root `de0e55125fde`, auth `4058e18b8ca2`.

## (1) Diff: as described
`users.ts` is +14/-2: 3× `throw err;` plus comments. The three test files are exactly the listed ones: the rename `ks1193-f3-…` → `ks1018-item3-…` (+49/-33), `ks1018-security-…` (+19/-11) and `ks1194-a-failed…` (+10/-5). Nothing else changed.

## (2) Cells (my runs, `logs/mut_summary.txt`, 10 verification files / 142 tests)
| Mutation of head users.ts | Red |
|---|---|
| none (head) | 0 |
| develop users.ts / all 3 rethrows removed | 6: the 4 renamed-file cells and the 2 ks1018 controls |
| `get` rethrow removed | REVIEW + CONTROL |
| `pending` rethrow removed | PENDING + CONTROL + ks1018 POST control |
| `list` rethrow removed | LIST + CONTROL + ks1018 list control |
| rethrow → 503 | 8: the 6 above plus 2 KS-1193 F2 cells |
| rethrow → `return null/[]` (the D-CTL-NOMEM analogue) | 6 |
| memory planted in the failed-INSERT branch | **exactly 1**: the rewritten ks1194 cell. Also confirmed on the full suite: 1 of 898 |
| OLD test files against head users.ts | **exactly 7**: the 4 old F3 cells, the 2 old ks1018 controls and the old ks1194 cell |

Each old expectation is red on head, and each new one is red under its own product-line revert. The rewritten ks1194 cell stays green on develop's users.ts, which is correct: it re-observes an invariant and does not encode a behaviour change. The plant is what bites it.

## (3) Suites
- **Full auth suite:** head 85 files / 898 passed ×2; merged 86 / 908 ×2; develop 86 / 908. Develop's first run had 1 red: the ks949 5000 ms timeout under load 22. It was green on rerun, so it is a flake and not caused by the PR.
- **tsc (src):** rc 0 on all trees.
- **tsc with tests included:** 88 errors on every tree. The only change is the rename carrying the same pre-existing `keepAliveTimeoutBuffer` @types/node clash, and the PR adds no new error.
- **eslint:** 0 errors / 15 warnings, identical on all trees.

## (4) Semantics (probe `logs/gateprobe1473.test.ts`; output in `logs/probe_head.txt` and `logs/probe_base.txt`)
- **500** (generic `INTERNAL_ERROR`; 0 INSERTs; level not raised; no message, code or table name leaked): 42P01, 42501, 42703, 40001, 40P01, 22021, 25P02, and a codeless TypeError.
- **503**: 57014, 57P01, 53300, 08006, 08P01, ECONNRESET, ETIMEDOUT, the codeless pool timeout and "Connection terminated".
- On develop, every non-infrastructure class answered list 200 / POST 400 / review 200 with the level RAISED. That is the hazard this PR closes.
- The brief's phrase "503 for infrastructure errors (42P01/42501/40001/40P01 class)" is wrong. Those codes are NON-infrastructure and now answer 500; the code comment has it right.
- **Missing table:** the table is created in `001_initial-schema.sql`. On develop, POST already answered 500 at the INSERT (KS-1194) while GET answered a false empty 200. A consistent, logged 500 is the better behaviour.
- **Writes:** `saveVerificationRequest` already rethrows, so reads and writes now fail closed consistently.
- **Callers:** no frontend, mobile or SDK code calls these endpoints. I searched the whole repo; as a positive control, `users/me` is found in the frontends.
- **Memory-only mode is intact:** 200, duplicate POST 400, approve 200, re-review 400, 0 DB calls.

## Defects
1. **Minor: the justification at `users.ts:1229` is false.** It says a read that succeeds with no row "still consults the map (KS-467 depends on that)", and the header of `ks1018-item3-…test.ts:17` repeats it. ks467 mocks `isDbAvailable: () => false`. Making a success-empty read return null reds **0 of 898 (twice)**, so nothing pins this behaviour or depends on it.
2. **Minor (residual, inside the ruling's carve-out):** the success-empty consult at `users.ts:1233` still answers from memory **with a database configured**. A request filed while `isDbAvailable()` is false is still visible after the database recovers. In code, that flag is false both with no `DATABASE_URL` and during the KS-377 boot window of a configured database, so "no-database mode" in the comments is broader than the name says. My probe on head shows the effect: list 200 without the request; a second POST 200, so there are now two PENDING requests (one in memory, one in the DB); review approve 200, level raised. That is the duplicate-PENDING and memory-approval hazard class, though it is only reachable through a degraded-boot request. I recommend a follow-up ticket; it does not block this PR, because the brief's ruling scoped it out.
3. **Nit:** `pendingReadFails` in `ks1194-a-failed…test.ts:27/44/153` is now dead state.

**Observation:** 40001 and 40P01 are retryable but answer 500, not 503. That comes from the KS-253 classifier, predates this PR and is pinned by KS-1193 F2.

**Not checked:** GitHub CI status, and real-Postgres behaviour. All runs were mocked; I connected to no database.
