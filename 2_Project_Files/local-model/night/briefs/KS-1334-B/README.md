# KS-1334 part B: Spark brief (RUNG 3), adminConfig.ts seed-demo-users + migrate-tenant-data -> fail500

Written 2026-09-27 01:55-02:20 AEST by a Spark brief-writer sub-agent for Wednesday. It ran no model and queued nothing. Git write verbs ran only in the scratch clone (develop 94c9c7aa, part A merged as #1294). Nothing was written in any Secuura folder.

- `KS-1334.md` is brief B (the builder reads `<TICKET>.md`); `brief-B.md` is a byte copy. Part A is `../KS-1334/`.
- Re-anchored on part A's merged ks730c: C3 48 -> 50 (`:142`), KNOWN `:171-:173` -> `const KNOWN: string[] = [];`, new part B block inserted between `:255` and `:256`. Product `:2031`, `:2158` with unique leading context (`:2028`, `:2156`).
- Routes driven to their outer catch without a new jest.mock: seed-demo-users via its gate-refusal `logger.warn` throwing; migrate-tenant-data via `getPlatformPool()` throwing on a tenant manager installed on the mocked `../db`.
- **Does NOT close KS-1334**: the ticket also owns a fifth site `:2152` (per-tenant err.message in a 200 body; no fix shape ruled) and a live sweep.
- KS-1334 is In Progress by design, so the build needs `started_ok=`.
- `golden/`: `KS-1334-B.golden.diff` (fences byte-equal, checked by script), `adminConfig.B.ts`, `ks730c.B.ts`, `mkfixed.py`, `insert_block.txt`, `ks1334b_verify.sh` + `verify.out`, `build_input.out`.

## Build (rc 0, measured 02:1x)
```
NIGHT_EXCERPT_TRIGGER_BYTES=90000 \
NIGHT_SOURCE_CHECKOUT=<scratch clone with develop 94c9c7aa fetched> \
NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1334-B \
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1334 <run>/input.json \
  product=Blockchain/Dev/services/originate/src/routes/adminConfig.ts \
  ref=Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts \
  test_file=Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts line=2031 \
  "started_ok=part A merged #1294; ticket held In Progress by design for part B (Linear comment 2026-09-26T15:31Z); no open PR touches adminConfig.ts"
```
Excerpted: 2 regions (1-281, 1834-2161), 32,120 B; input 78,632 B (~19.6K est. tokens against ctx 32768; KS-1341 B's estimate ran ~38% under actual, so expect ~27K — tight; `ctx=65536` is the fallback). Then `prepare_clone.sh`, `LM_BACKEND=spark local_model_task.sh …`, `spark_checker.sh …`.
