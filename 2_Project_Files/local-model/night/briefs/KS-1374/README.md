# KS-1374: Spark brief + golden (TEST-ONLY: pin the global rate limiter at the demo figure, 2000 per 60 s)

Written 16:31 AEST 2026-09-29 (shell `date`) by a Spark brief-writer for Wednesday (session 35f90900). Secuura/Blockchain only. Linear was only READ (the ticket, and `build_input.sh`). Nothing was pushed, raised, commented or mailed. Nothing was written under `!CODING/`. Every git write verb ran in the writer's own `--shared` clone `scratchpad/ks1374/repo` (origin GitHub).

**Ruling (Kam, KS-1374 comment 2026-09-29 01:42Z):** option 2 plus one guard. Raise `RATE_LIMIT_MAX_REQUESTS` on LOCAL stacks only, leave demo and production as deployed, and add ONE limiter test at the demo's limit.

## Routing: split
- **A, this brief (SPARK, TEST-ONLY):** a new `api-gateway` test file. No product line changes. The checker plants a tamper at `index.ts:474`.
- **B, the config raise (NOT Spark):** `Blockchain/Dev/env.example:189-192` (the canonical template) and `.env.example:204-205` (legacy) go from `2000` to `10000`. The `:191` comment ("demo stays at its 100/min default") is stale. Each operator's and slot's gitignored `.env` needs the same edit by hand, because templates only reach NEW `.env` files (`scripts/bootstrap-env.sh` leaves an existing `.env` untouched). **Do NOT change `docker-compose.yml:497`'s `:-2000` fallback.** The demo VM runs this same compose file with its own `.env`, so that fallback is what the demo inherits. Cell D1 pins it. Why not Spark: the builder only accepts a product under `services/*` or `packages/shared`, a template value cannot go RED-first, and the change is two files.
- **C, the harness (needs a decision):** `systemTest/akto/src/setup/aktoRateLimit.ts:60` hard-codes `PLATFORM_REQUESTS_PER_MINUTE = 2000`. `tierPacing.ts:51-52` paces pre-merge and security at `derivedRateLimit()` = 1500. So **B alone does not speed the Akto scans up**, even though the ticket and our comment both say it would. Pacing at 7,500 against a stack whose `.env` still says 2000 would bring the 429s back. Schemathesis does read the env (`runner/config.py:234`).

## Files
- `KS-1374.md` is the brief (17,826 chars, sha256 `cd57714538c240c2…`).
- `KS-1374.golden.diff` is the golden (sha256 `165c0ab871bd90b4…`). It creates one NEW file, 116 lines.
- The brief's test fence is byte-identical to the golden body. Control: a copy with one token changed compares DIFFER.
- Char lint on the golden body: 0 non-ASCII characters, 0 backslashes, 0 backticks, 0 double quotes.

## Measured (scratch clone at `2cb85833`; node_modules farmed read-only from the Blockchain checkout)
| step | result |
|---|---|
| `git apply --check` at the tip | rc 0 |
| new file at the untouched tip | 7 / 7 green |
| under the tamper (`:474` reads `GLOBAL_RATE_LIMIT_MAX`) | 1 failed / 7 (W1 only) |
| arms: `max: 10000` / 15-min window / compose `:-10000` / `/health` not skipped / `demo` test-token bypass | W1 / W2 / D1 / B3 / B4 each red alone |
| api-gateway suite | tip 88 files, 795 passed, 0 failed; with the file 89 files, 802 passed, 0 failed |
| tsc (`-p services/api-gateway`) and eslint | rc 0, rc 0 |
| real `checker.sh`, golden as model output | **RESULT: PASS (7/7)**, mode test_only |
| real `spark_checker.sh` | **SPARK RESULT: PASS** |

## build_input: rc 0
`prompt source: WEDNESDAY BRIEF`. The builder reports 1 red cell declared, the tamper accepted with `statement_ok`, `suggested_test_file` = the brief's File: line, and an input of 98,712 B (about 24.7K prompt tokens).
```
NIGHT_SOURCE_CHECKOUT=<scratch>/ks1374/repo NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1374 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1374 <out>/input.json product=Blockchain/Dev/services/api-gateway/src/index.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts line=474 ctx=65536
```

## The round command
The script is a copy of `screen0929/round_215cc687.sh` with ONLY `SP`, `SRC` (the writer's clone `ks1374/repo`) and `TIP` (`2cb85833…`) changed (checked with `diff`).
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/35f90900-da39-4310-a097-bf496fc89a5b/scratchpad/ks1374/round_2cb85833.sh KS-1374-R1 KS-1374 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1374 - product=Blockchain/Dev/services/api-gateway/src/index.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts line=474 ctx=65536
```
Round counter: 0 rows in `night/done.md` (control: KS-908 has 3) and no `READY_KS-1374*`. The round allows the original brief plus ONE rebrief.

## UNMEASURED
1. The demo's real `RATE_LIMIT_MAX_REQUESTS` was not read. The VM `.env` is off-repo. 2000 comes from Kam's comment and the local templates.
2. The behaviour cells drive express-rate-limit with the same options, not `index.ts`'s own instance, which is inline and never imported. Driving the real instance would need a limiter CODE change (Claude seat).
3. The Node version in CI is unchecked. The farmed node_modules come from an older install, and #1339 moved morgan and lockfiles, not express, express-rate-limit or vitest.
4. Open PRs were checked from `ls-remote` plus fetched heads (20, none colliding). A PR opened after 16:2x would be missed.
