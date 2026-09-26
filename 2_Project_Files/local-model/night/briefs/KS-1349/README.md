# KS-1349: Spark brief (RUNG 3), ks730c C1 per-environment mockClear + whole call list (TEST-ONLY, modify in place)

Written 2026-09-27 01:50-02:20 AEST by a Spark brief-writer sub-agent for Wednesday. It ran no model and queued nothing. Git write verbs ran only in the scratch clone (`scratchpad/sparkfeed`, develop 94c9c7aa). Nothing was written in any Secuura folder.

- `KS-1349.md` is the brief: the KS-1344 shape (#1293) on ks730c `:112-:120`, one hunk `@@ -112,9 +112,11 @@`, plus a `## Tamper` on adminConfig.ts `:104`.
- **Tamper is DEVELOPMENT-only, not the ticket's production-only** — measured: C1 has no production row, so the production-only tamper reds C1 at the UNFIXED test too (not discriminating). Dev-only: C1 green at head (blind), red at the fix.
- Declared reds: `RED KS-730 C1` (x4) and `RED KS-1334 A1` (x2; part A's rows are already per-environment and red under any env-dropping tamper).
- `golden/`: `KS-1349.golden.diff` (byte-equal to the brief's fence), `ks730c.1349.ts`, `mkgolden.sh`, `ks1349_verify.sh` + `verify.out` (2x2, ticket-tamper arm, test-inclusive tsc with positive control, lint, suite), `tsc_incl.sh`, `build_input.out`.
- **Collision with KS-1334-B:** both goldens apply on 94c9c7aa in either order (23/23 green). Recommend B first; then this brief needs no re-anchor.

## Build (rc 0, measured 02:0x)
```
NIGHT_EXCERPT_TRIGGER_BYTES=90000 \
NIGHT_SOURCE_CHECKOUT=<scratch clone with develop 94c9c7aa fetched> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1349 \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1349 <run>/input.json \
  product=Blockchain/Dev/services/originate/src/routes/adminConfig.ts \
  ref=Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts \
  test_file=Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts line=104
```
Excerpted: adminConfig.ts -> 1 region (1-281), input 52,945 B (~13.2K est. tokens). Then `prepare_clone.sh`, `LM_BACKEND=spark local_model_task.sh tasks/code_patch/task.md <run>/input.json <run>/out.md`, `spark_checker.sh <run>/input.json <run>/out.md <run clone>`. Holding note (IMPROVEMENTS 19:53): hold_ready routes this input shape as code_patch while the checker runs test_only — KS-1344 was held by hand.
