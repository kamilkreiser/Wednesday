# KS-1339: Spark brief (RUNG 4 strict), ks1293 CONFIGPINNED asserts the offender list before the count floor

Written 2026-09-26 22:1x AEST by a Spark brief-writer sub-agent for Wednesday (feed4). It ran no model and queued nothing. No git write verb ran anywhere; the scratch clone `scratchpad/sparkfeed` (develop `3f70224a`) was edited in its working tree for the proofs and restored (`git status --porcelain` = 0 lines). Nothing was written in any Secuura folder.

- `KS-1339.md` is the brief (the builder reads `<ticket>.md`); `brief-ks1293.md` is a byte copy.
- **Rung 4 (strict):** NO product `+` line and NO product hunk header in the brief; the fix is given in prose (move `:164` above `:162`), the merged precedent is named by path+line (`:178`, `:221` in the same file — no merged offenders-before-floor cell exists anywhere in the repo, searched). Carries the "count each hunk's lines exactly" sentence. Caveat stated in the brief: for a MOVE the `+` text equals the quoted `-` text, so this measures hunk composition + header arithmetic for a move-inside-one-hunk, not expression derivation.
- Product is a SUITE file (originate jest); the test is a separate NEW file (normal mode, not self-testing).
- `golden/`: `KS-1339.golden.diff` (one valid answer, `@@ -161,5 +161,5 @@` + the 64-line test), the new test, `verify.out`, `build_input.out`.

## Build (rc 0, measured 22:2x)
```
NIGHT_SOURCE_CHECKOUT=<scratch clone at develop 3f70224a; originate node_modules farmed> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1339 \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1339 <run>/input.json \
  product=Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts \
  ref=Blockchain/Dev/services/originate/src/__tests__/ks780-org-id-is-the-shared-implementation.test.ts line=164
```
~10.5K estimated prompt tokens (41,872 B). Then `prepare_clone.sh`, `LM_BACKEND=spark local_model_task.sh tasks/code_patch/task.md <run>/input.json <run>/out.md`, `spark_checker.sh <run>/input.json <run>/out.md <run clone>`.

**Scoring note:** A3c has 0 expected `+` lines (rung 4) — hold_ready needs the by-hand hold with the golden byte compare (IMPROVEMENTS 21:31). A3b grades `:164` as a `-` line; a diff that expresses the move the other way round (moving `:162`-`:163` below) is refused by A3b even though it is textually equivalent — the brief forbids that form explicitly.
