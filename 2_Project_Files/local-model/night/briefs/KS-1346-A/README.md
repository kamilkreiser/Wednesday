# KS-1346 part A: Spark brief (RUNG 3), routes/systemErrors.ts fail500 logs a non-Error throw with its content

Written 2026-09-26 21:45-21:55 AEST by a Spark brief-writer sub-agent for Wednesday (feed3). It ran no model and queued nothing. Git write verbs ran only in the scratch clone. Nothing was written in any Secuura folder.

- `KS-1346.md` is the brief; `brief-A.md` is a byte copy. **A and B touch different files and are independent** (A = routes/systemErrors.ts, B = routes/gdpr.ts); webhooks.ts / adminConfig.ts (the ticket's other two helper files) are in flight tonight and are left out.
- Every product and test line is spelled out; the brief's diff fences and test fence are byte-equal to `golden/KS-1346-A.golden.diff` (checked by script).
- `golden/`: the golden diff, the new test, `ks1346a_verify.sh` + `verify_A.out` (red, green, suite, lint, tamper, arm), `build_input.out`.

## Build (rc 0, measured 21:5x)
```
NIGHT_SOURCE_CHECKOUT=<scratch clone at develop 3f70224a, node_modules farmed> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-A \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1346 <run>/input.json \
  product=Blockchain/Dev/services/originate/src/routes/systemErrors.ts \
  ref=Blockchain/Dev/services/originate/src/__tests__/ks730a-ingest-500-never-answers-err-message.test.ts line=94
```
Then `prepare_clone.sh`, `LM_BACKEND=spark local_model_task.sh tasks/code_patch/task.md <run>/input.json <run>/out.md`, `spark_checker.sh <run>/input.json <run>/out.md <run clone>`.

**Tamper note:** reverting the helper line to `String(err)` leaves the `inspect` import unused and ts-jest fails the SUITE to compile (0 tests, not an assertion red) — measured; the brief's tamper is `inspect(err)` → `inspect(String(err))` instead.
