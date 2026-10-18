# Spark screen, part 6 (2026-10-19 ~04:5x-05:05 AEDT): KS-1627, one test_only brief, one round, PASS

By a Spark brief-writing sub-agent for Wednesday. Secuura only. Brief pinned to develop `5d1be7b06279950e3bfe176c237e5d640eb04581` (the cache's own fetch ran first; `ls-remote` agreed at the start, at the dry-run, and again after the round: develop did not move). Nothing held, raised, pushed, merged, committed or deleted. The ticket text of KS-1627 was NOT read (no Linear reader); the brief rests on the commission text and the gate H1 evidence (`0_Brain/reference/2026-10-19_gate-H1-pr1582-pr1584/verdict.md`, its scratch suites `h1gate-ks1540-real-redis-never-init.test.ts` and `...dead-port.test.ts`, read only).

## Result

| item | value |
|---|---|
| brief dir | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1627_p1/` (`KS-1627.md`, `golden.diff`, `spark.pins`) |
| tip | `5d1be7b06279950e3bfe176c237e5d640eb04581` |
| mode / rung | `test_only`, rung 1: ONE NEW test file, every line given (`--- /dev/null`); the product (`services/health.ts`) is the tamper target only |
| new test file | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts` (68 lines, ASCII) |
| tamper | `health.ts:53` `if (redisService.isRedisAvailable?.() === false) {` to `if ((redisService as any).isRedisAvailableRenamed?.() === false) {` (the call renamed to a name the real module does not export; `as any` so it compiles) |
| pins | `tier=test_only`, `ref=` the ks1540 test (differs from the new file), `line=53`, `ctx=131072`. No `test_file=` pin: the builder refuses a `test_file=` that is not at the tip (a NEW file); the dry-run REFUSED on it first, then on the diff sitting under `## The exact change` (a pure-insertion block with leading context only), so the new-file diff lives under `## The test` and `## The exact change` says NONE |
| brief_lint | rc 0 |
| dry-run | rc 0 (`DRY-RUN OK`, input 37649 B, about 9389 prompt tokens). Two earlier dry-runs REFUSED for the two brief defects above, both fixed before any control |
| CONTROL | `CONTROL-PASS`, checker 7/7, A2a OK, golden BYTE-IDENTICAL, run dir `local-model/runs/spark_secuura_2026-10-19_ks_1627_p1-control` (A4 2 failed / 4 run under the tamper, controls green, assertion reds; A5 4 passed / 4; A6 no new red; A7 tsc rc 0) |
| round (original, counter 1 of 1; no rebrief) | `SPARK ROUND ks_1627_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 5d1be7b06279 · 93s round, 33.623s model, 13999+1255 tok` |
| run dir | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1627_p1` |
| FAIL class | none |

Checker lines of the round: A1 one fenced diff; A2 applies strict; A3 (test-only) touched set == the one new test, product untouched; A4 RED-FIRST "fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)" (the checker's wording says "untouched tip" but in test_only mode the tamper is planted for that run, shown on the `A4 (test-only): tampered ...health.ts:53` line and reverted after); A5 GREEN-AFTER "4 passed / 4 run"; A6 whole api-gateway suite no new red; A7 tsc rc 0; `RESULT: PASS (7/7)`; `PASS A2a ANCHOR ... skipped_newfile=1`; `SPARK RESULT: PASS`.

## Red cells and controls (exact titles)

Test titles are prefixed `KS-1627 - the real redis module in its fallback state makes GET /api/connector/info refuse ` (the describe). In the brief's `## Red cells`:

- `RED KS-1627 R1: an empty fallback store answers 503 SERVICE_UNAVAILABLE with the create path text, never 200 and never []`
- `RED KS-1627 R2: a restrictive list written into the fallback memory store is still refused with 503, not echoed with 200`

Controls (green on both trees, they do not touch health.ts):

- `CONTROL KS-1627 C1: the real module exports isRedisAvailable as a function and reports false here (never initialised)`
- `CONTROL KS-1627 C2: in this state the real settings read RESOLVES to null instead of throwing (the shape that used to answer 200 [])`

Shape (copied from gate H1's never-initialised suite): the REAL `../services/redis` namespace (no double) passed to `createHealthRoutes({}, realRedis)` on an express app, listened on an ephemeral port, real `fetch` with `x-api-key`, `apiKeyCache` and `connectorBearerCache` seeded as the ks1540 suite does. R1 expects `[503, 'SERVICE_UNAVAILABLE', <create path text>, undefined]` on an empty store; R2 first writes a restrictive list through the real `setNotificationSettings` (memory store in fallback) and expects the same 503. The patch the model produced is byte-identical to the golden, so no read of a differing patch is owed.

## Things Wednesday should read before holding

- RED proof is the checker's A4: both red cells fail by assertion when the tamper is planted, and all four pass at the tip. This is the commissioned tamper; it is the rename as seen from health.ts. The OTHER half of the rename (the real module's export renamed while health.ts is untouched) is not planted by the checker; under it C1 would fail (`typeof realRedis.isRedisAvailable`) and so would tsc via `routes/verification.ts:1276`, but that was not run here.
- The state driven is the never-initialised module (`redisClient` null). The dead-port `initRedis()` state (gate H1 ran it) is not in the file.
- The cell imports the real redis module statically in a file of the whole api-gateway suite; A6 (whole suite, no new red) passed in the control and the round.
- `R2` mutates the real module's in-memory settings store for the rest of that file only (vitest isolates files).

## NOT tested / unmeasured

- The ticket text itself (KS-1627) was not read; vitest/tsc were run only by the checker, never by hand.
- A connected (live) Redis, the dead-port `initRedis()` state, a runtime Redis up-then-down transition, and the full gateway app (`index.ts`) are unmeasured.
- The real-module-export rename half of the tamper (see above): unmeasured.
- Open-PR overlap on `health.ts` or the new file name: not checked. Live seats' unpushed work: not checked.
- ESLint on the new file: not run.

## Files written

Brief dir `local-model/night/briefs/ks_1627_p1/`; one provenance comment line in `local-model/spark/queue.md`; run dirs `runs/spark_secuura_2026-10-19_ks_1627_p1` and `..._ks_1627_p1-control` and `spark/state/dry/ks_1627_p1_*` are round.sh's own; `spark/cache/work/` gained 2 clones (about 335 MB each, not pruned). Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/spark_1627/` (`test_body.ts`, `gen.py`, `brief_tpl.md`, `mk.sh`, `ctl.sh`, `round1.sh`, logs).
