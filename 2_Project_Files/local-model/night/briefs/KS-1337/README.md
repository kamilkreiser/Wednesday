# KS-1337 akto site: Spark brief (RUNG 4, the ladder experiment)

Written 2026-09-26 21:14-21:22 AEST by a Spark brief-writer sub-agent for Wednesday. It ran no model and queued nothing. Git write verbs ran only in the scratch clone `scratchpad/sparkfeed` (a `--no-local` clone of the Blockchain checkout with develop `3f70224a` fetched into it via the checkout's deploy key). Nothing was written in any Secuura folder.

- `KS-1337.md` is the brief. The builder reads `<ticket>.md`. `brief-akto.md` is a byte copy of it.
- **Rung 4.** The product fix is written in prose with #1291's merged line as the pattern. The `-` line and every context line are quoted byte-exact, but the model gets no product `+` line and no header. The test file is spelled out in full, so the round measures only the product hunk. This is the simplest open site in the class.
- `golden/`: `KS-1337-akto.golden.diff` is one valid answer, and `verify.out` holds the executed red, green, tamper, arm and lint results. The two scripts can re-run them against a scratch clone.
- The top-level `night/briefs/KS-1337.md` belongs to the merged #1291 cli.ts brief. It was NOT touched.

## Build (rc 0, measured 21:14)
```
NIGHT_SOURCE_CHECKOUT=<scratch clone with develop 3f70224a fetched + systemTest/akto/node_modules farmed> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1337 \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1337 <run>/input.json \
  tool=systemTest/akto product=systemTest/akto/tests/preSuiteSetup.ts \
  ref=systemTest/akto/tests/unit/bin/loadTemplatesGuard.test.ts line=36 vitest_config=vitest.unit.config.ts \
  "started_ok=site-1-merged-#1291;akto-site-is-a-separate-split-brief"
```
Then: `prepare_clone.sh <run>/input.json <run clone>`, followed by `LM_BACKEND=spark local_model_task.sh tasks/code_patch/task.md <run>/input.json <run>/out.md`, then `tasks/code_patch/spark_checker.sh <run>/input.json <run>/out.md <run clone>`.

**Scoring note:** A3c has 0 expected `+` lines on purpose, because this is rung 4. The checker cannot tell `fileURLToPath` from `decodeURIComponent(...pathname)`, since both turn the cell green (measured). A PASS still needs Wednesday's source read of `:37`. macOS `patch -F0` refuses a trailing-only-context insertion, while `git apply` strict accepts it. Do not score that refusal against the model.
