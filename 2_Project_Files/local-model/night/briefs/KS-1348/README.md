# KS-1348: Spark brief (RUNG 3), originate utils/logger.ts File transports get format: combine(json())

Written 2026-09-27 02:00-02:20 AEST by a Spark brief-writer sub-agent for Wednesday. It ran no model and queued nothing. Git write verbs ran only in the scratch clone (develop 94c9c7aa). Nothing was written in any Secuura folder.

- `KS-1348.md` is the brief: 1 product hunk `@@ -42,6 +42,8 @@` + NEW jest test (92 lines) that loads the REAL logger under production via jest.isolateModules in a temp cwd, logs once, and parses both files' lines.
- Ticket claim reproduced at the tip: both files read back `["undefined"]`.
- `golden/`: `KS-1348.golden.diff` (fences byte-equal, checked by script), `logger.fixed.ts`, the new test, `ks1348_verify.sh` + `verify.out`, `ks1348_repeat.sh` + `repeat.out` (stability), `build_input.out`.

## Build (rc 0, measured 02:1x)
```
NIGHT_SOURCE_CHECKOUT=<scratch clone with develop 94c9c7aa fetched> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1348 \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1348 <run>/input.json \
  product=Blockchain/Dev/services/originate/src/utils/logger.ts \
  ref=Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts line=45
```
Input 27,184 B (~6.8K est. tokens). Then `prepare_clone.sh`, `LM_BACKEND=spark local_model_task.sh …`, `spark_checker.sh …`. Note for the checker: the new cell calls `process.chdir` (fine in jest's default child-process workers and --runInBand, both measured; it would fail under workerThreads, which originate does not set).
