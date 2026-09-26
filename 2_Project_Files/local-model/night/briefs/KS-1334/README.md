# KS-1334: Spark brief A (RUNG 3), adminConfig.ts refresh-tenants + backfill-certification-metadata

Written 2026-09-26 21:15-21:22 AEST by a Spark brief-writer sub-agent for Wednesday. It ran no model and queued nothing. Git write verbs ran only in the scratch clone. Nothing was written in any Secuura folder.

- `KS-1334.md` is brief A. `brief-A.md` is a byte copy of it.
- **The ticket is split A → B.** A converts `:113` and `:1859`. B converts `:2031` and `:2158`, empties C4's KNOWN list and sets C3 to 50. Both briefs edit the same two pins in `ks730c`, so B is written only after A merges.
- **Modify-in-place.** `test_file=` points at `ks730c`, the existing KS-730 test. There is no new test file, because the checker's A3 allows only one test file and fixing any site reds C3 and C4 by design.
- `golden/`: `KS-1334-A.golden.diff` is byte-equal to the brief's three fences. `adminConfig.A.ts` and `ks730c.A.ts` are the resulting files. `verify.out` and `lint_suite.out` hold the executed results.

## Build (rc 0, measured 21:21)
```
NIGHT_EXCERPT_TRIGGER_BYTES=90000 \
NIGHT_SOURCE_CHECKOUT=<scratch clone with develop 3f70224a fetched> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1334 \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1334 <run>/input.json \
  product=Blockchain/Dev/services/originate/src/routes/adminConfig.ts \
  ref=Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts \
  test_file=Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts line=113
```
**Why `NIGHT_EXCERPT_TRIGGER_BYTES=90000`:** `adminConfig.ts` is 100,592 B. Carried whole, the builder REFUSED rc 2 (~37,815 estimated tokens against the default ctx 32768). Excerpted, it goes as 3 regions (1-229, 1810-1887, 1990-2161; 23,854 B), which gives an input of 66,639 B and ~16.6K estimated tokens. KS-1341 B's estimate ran about 38% under its actual count, so expect roughly 23K actual. The alternative is `ctx=65536` with the whole file. **The Spark has not been measured on an excerpted input.**

Then: `prepare_clone.sh`, then `LM_BACKEND=spark local_model_task.sh tasks/code_patch/task.md <run>/input.json <run>/out.md`, then `spark_checker.sh <run>/input.json <run>/out.md <run clone>`.
