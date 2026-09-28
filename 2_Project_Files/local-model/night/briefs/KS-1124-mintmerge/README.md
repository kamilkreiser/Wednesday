# KS-1124 MINTMERGE: Spark carve brief + golden (the thread-token cache write merges into the persisted blob instead of replacing it)

Written 16:19 AEST 2026-09-28 (shell `date`) by a carve drafter for Wednesday. It ran no model, raised no PR, and changed no GitHub or Linear state (Linear and `ls-remote` were READ; the builder made no GitHub call because KS-1124 has no attached PR). It wrote nothing under `!CODING/`. Every git write verb ran in its own clones in the session scratchpad.

- **Base:** develop `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`, read by `ls-remote` at 15:53 AEST. The source clone `carve_base` read HEAD == `d9ce1403` and porcelain 0 before and after every step.
- **What was carved:** KS-1124 carries two findings. **O1** (originate's thread-token mint callback REPLACES the document's blockchain blob with the create-time local) has its fix shape spelled in the ticket ("spread the CURRENT persisted blob, not the create-time local") and reaffirmed in the 09-26 comment. It is ONE product file. **F4** (the certification failed leg) offers three alternative fixes, so it is a card for Kam and is NOT here.
- **Edit points:** 3 (`:788` one-line replacement; a 3-line insertion after `:796`; `:799` one-line replacement), in 2 hunks.
- **Round counter:** 0 (`night/done.md` has no KS-1124 row; no `READY_*KS-1124*`).

## Files
- `KS-1124.md` is the brief: two product hunks and one INSERTION into the existing `ks520-anchor-fail-closed.test.ts` (63 `+` lines, 3 cells).
- `KS-1124.golden.diff`, sha256 `54fb96afa36b…`, 4,923 B: 2 files, **68 + / 2 -**.
- **Fence rebuild:** the diff rebuilt from the brief's `File:` / `Test file:` lines and its two fences is **IDENTICAL** to the golden. Comparator control: a one-token mutation (`anchor-ks1124` -> `anchor-ks1125`) read **DIFFER**.
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote; 0 non-ASCII lines in the golden; 0 blank context lines.

## Why the test is IN ks520, not a new file (measured)
The first golden put the cells in a NEW file. Its cells went red then green correctly, but the whole originate suite then went **1 failed**: `ks1293-originate-suite-is-hermetic.test.ts` MANIFEST-DRIFT (`missing: ['ks1124-…test.ts']`). Any file that sets `ANCHORING_SERVICE_URL` must be named in ks1293's `SUBJECTS` list (`:57`-`:67`), and a create-route cell has to set it to stay off the network. Adding the new file to that list would make it three files. `ks520` is already a subject (`:65`) and already drives the create route with the same mocks, so the cells went into it. The new-file version is kept in the scratchpad only (`carve/out1124/`), not here.

## Measured (scratch clone `carve/c1124` at `d9ce1403`, node_modules farmed by `prepare_clone.sh`, shared built in the clone)

| step | instrument | result |
|---|---|---|
| strict apply | `git apply --check` / `patch -p1 -F0 --dry-run` | rc 0 / rc 0 |
| test hunk alone (RED) | `npx jest <file> --runInBand --json` | **1 failed / 5 passed / 6**: exactly M1, by ASSERTION (`anchorId`, `status`, `txHash` received `undefined`) |
| golden applied (GREEN) | same | **6 / 6** |
| whole originate suite | `npx jest --runInBand --json` | tip **89 suites / 1052 passed / 0 failed**; golden **89 / 1055 / 0** (+3 = the new cells; ks1293 green) |
| tsc | `tsc --noEmit -p services/originate` | rc 0 at the tip and with the golden |
| tsc with tests | temp config extending the package tsconfig (`strict`, `noUnusedLocals`, `noUnusedParameters`), `include src/**/*.ts`, `types: [jest, node]`; both changed files proven IN the program (`--listFilesOnly`) | **rc 0, 0 errors at both**. Positive control: a planted `const x: number = 'not-a-number'` in ks520 surfaces exactly one TS2322 naming it |
| eslint | both changed files | rc 0, 0 problems at both. Control: a planted `debugger` + `var` gave rc 1, 2 errors |

**Arm** (the golden applied, one product line changed back; the clone reset after):

| arm | line | failed / total | which |
|---|---|---|---|
| spread | `...(current?.blockchain \|\| document.blockchain \|\| {}),` -> `...((current?.blockchain && document.blockchain) \|\| {}),` | 1 / 6 | M1 |
| golden | none | 0 / 6 | none |

The arm keeps `current` referenced, so `noUnusedLocals` cannot turn it into a compile failure (a whole-file load failure would read as "every cell red" and prove nothing).

## build_input: rc 0
```
NIGHT_EXCERPT_TRIGGER_BYTES=60000 NIGHT_SOURCE_CHECKOUT=<scratchpad>/carve_base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1124-mintmerge bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1124 <out>/input.json product=Blockchain/Dev/services/originate/src/routes/documents.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks444-documents-create-title-guard.test.ts test_file=Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts line=788 ctx=65536
```
- `prompt source: WEDNESDAY BRIEF … (16469 chars)`; Backlog, no attached PR; red cells `['RED KS-1124 M1']`; 5 expected `+` lines (A3c); `test_file` pinned (modify in place), `suggested_test_file` == the brief's File: line; contract key set OK.
- **Excerpt is REQUIRED in practice:** `documents.ts` is 150,637 characters, under the builder's default 160,000 trigger, so without `NIGHT_EXCERPT_TRIGGER_BYTES` it would be carried whole (about 40K tokens). With the trigger at 60000: 5 regions `(1-217), (492-567), (658-718), (736-842), (1326-1397)`, 28,074 B; input.json 70,388 B, about **17.5K prompt tokens** (the builder's estimate). The edit region `:785-:802` is inside `(736-842)`.
- `carve_base` porcelain 0 before and after.

## The round command (NOT run)
Use the copy of round.sh pinned to this tip: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve/round_d9ce1403.sh` (three lines differ from the 09-27 `sparkrun/round.sh`: `SP`, `SRC` = `carve_base`, `TIP` = `d9ce1403…`; it refuses unless the source is clean at the tip).
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve/round_d9ce1403.sh KS-1124-MINTMERGE-R1 KS-1124 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1124-mintmerge 60000 product=Blockchain/Dev/services/originate/src/routes/documents.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks444-documents-create-title-guard.test.ts test_file=Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts line=788 ctx=65536
```
⚠ `carve_base`'s `node_modules` entries are symlinks into another session's scratchpad (`d0b2ec3e…/scratchpad/sparkfeed/…`), and jest itself resolved from the real Secuura checkout's `node_modules` (read-only use; seen in the stack traces). If the sparkfeed directory is cleaned, `prepare_clone.sh` will farm dead links.

## For the raise (after a PASS)
- Two files; no generated companion (not an OpenAPI registration).
- **It is a RUNTIME change** on the create route's thread-token path, which runs only with `STATE_THREAD_NFT_ENABLED=true`. §5f live sweep owed.
- PR body: `Refs KS-1124` (O1 only), no closing keyword. Name the residual: this is read-then-write, so a write landing between the new read and the cache write can still be lost (the class KS-1074's merge comment records).

## OPEN DOUBTS (for Wednesday)
- **"Token" in the exclusion list.** This is the Cardano thread-token NFT cache on a document blob, not an auth token or credential. I read the commission's "auth/MFA/OAuth/token/credential" as auth tokens; if Wednesday reads it wider, this brief is out.
- The fix is the ticket's own shape and it narrows, not closes, the race: an atomic JSONB merge in `documentRepo` would close it and is a design choice nobody has ruled.
- No Spark round, no `spark_checker.sh`, no live stack.
