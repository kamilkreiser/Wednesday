# KS-1347 ks732 site: Spark brief (RUNG 4 strict)

Written 2026-09-26 21:40-21:55 AEST by a Spark brief-writer sub-agent for Wednesday (feed3). It ran no model and queued nothing. Git write verbs ran only in the scratch clone `scratchpad/sparkfeed` (develop `3f70224a`). Nothing was written in any Secuura folder.

- `KS-1347.md` is the brief (the builder reads `<ticket>.md`); `brief-ks732.md` is a byte copy.
- **Rung 4 (strict), per Kam's 21:03 ruling and the IMPROVEMENTS 21:31 lesson:** the brief text has NO product `+` line, NO product hunk header, and NO written-out fixed expression (counted: `fileURLToPath(new` 0 times; the alternative-fix arm is also kept OUT of the brief so it cannot prime). The merged example is named BY PATH only and is IN the input: `ref=` is `ks847-no-raw-control-bytes.test.ts`, whose `:41`/`:60` carry the idiom and `:44-:59` the why. The `-` lines are quoted only in the line-keyed `## Where` (the file's current text, needed for A3b). The test file is spelled out in full (its own `@@ -0,0 +1,84 @@` is the only header in the brief).
- Product is a SUITE file (`services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts`); the test is a separate NEW file, so the checker runs NORMAL mode (A3 = {product, one new test under test_dir}), not self-testing (no hunk-ordinal dependency on how the model splits its hunks).
- `golden/`: `KS-1347-ks732.golden.diff` (one valid answer), the test file, `ks1347_verify.sh` + `verify.out` (red, green, suite, lint, tamper, arm), `build_input.out`.

## Build (rc 0, measured 21:5x)
```
NIGHT_SOURCE_CHECKOUT=<scratch clone at develop 3f70224a; root + services/auth node_modules farmed> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1347 \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1347 <run>/input.json \
  product=Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts \
  ref=Blockchain/Dev/services/auth/src/__tests__/ks847-no-raw-control-bytes.test.ts line=293
```
~12.1K estimated prompt tokens (48,301 B). Then `prepare_clone.sh`, `LM_BACKEND=spark local_model_task.sh tasks/code_patch/task.md <run>/input.json <run>/out.md`, `spark_checker.sh <run>/input.json <run>/out.md <run clone>`.

**Clone note:** `prepare_clone.sh` farms `services/auth/node_modules` from `source_checkout`; with the scratch clone as the source it has none, so it was farmed BY HAND from the real checkout (same symlink method). A fresh run clone needs the same.

**Scoring note:** A3c has 0 expected `+` lines (rung 4). The checker cannot tell the node:url decoder from a string percent-decode of `.pathname` (arm measured GREEN); a PASS needs Wednesday's source read of `:294`, `:297`, `:317` and the import line. The existing ks732 lint warning (`disableBlock` unused, tip `:318`) is pre-existing, not the model's.
