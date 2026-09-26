# KS-1346 part B: Spark brief (RUNG 3), routes/gdpr.ts fail500 logs a non-Error throw with its content

Written 2026-09-26 21:45-21:55 AEST by a Spark brief-writer sub-agent for Wednesday (feed3). It ran no model and queued nothing. Git write verbs ran only in the scratch clone. Nothing was written in any Secuura folder.

- `KS-1346.md` is the brief; `brief-B.md` is a byte copy. **A and B touch different files and are independent** (A = routes/systemErrors.ts, B = routes/gdpr.ts); webhooks.ts / adminConfig.ts (the ticket's other two helper files) are in flight tonight and are left out.
- Every product and test line is spelled out; the brief's diff fences and test fence are byte-equal to `golden/KS-1346-B.golden.diff` (checked by script).
- `golden/`: the golden diff, the new test, `ks1346b_verify.sh` + `verify_B.out` (red, green, suite, lint, tamper, arm), `build_input.out`.

## Build (rc 0, measured 21:5x)
```
NIGHT_SOURCE_CHECKOUT=<scratch clone at develop 3f70224a, node_modules farmed> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-B \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1346 <run>/input.json \
  product=Blockchain/Dev/services/originate/src/routes/gdpr.ts \
  ref=Blockchain/Dev/services/originate/src/__tests__/ks730b-gdpr-500-never-answers-err-message.test.ts line=211
```
Then `prepare_clone.sh`, `LM_BACKEND=spark local_model_task.sh tasks/code_patch/task.md <run>/input.json <run>/out.md`, `spark_checker.sh <run>/input.json <run>/out.md <run clone>`.

**Tamper note:** reverting the helper line to `String(err)` leaves the `inspect` import unused and ts-jest fails the SUITE to compile (0 tests, not an assertion red) — measured; the brief's tamper is `inspect(err)` → `inspect(String(err))` instead.
