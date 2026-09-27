# KS-1346 part C: Spark brief + golden (the ruled residue, adminConfig.ts)

Written 05:00 AEST 2026-09-28 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and `ls-remote` were READ) and wrote nothing under `!CODING/`. Every git write verb (clone, fetch, checkout, apply, one local `core.sshCommand` config line) ran in the scratch clone `ks1346cd/base`, a `--shared` clone of sparkfeed with develop fetched into it by SSH.

- **Ruling:** Kam, live board 2026-09-27 16:32, card `secuura-ks1346-logging-thrown-objects-leaks-secrets`, option a: "Type and field names only".
- **Why this brief:** gate33 F-3 (`2026-09-28-batch1310-g33/report.md:200-204`) says #1311 + #1312 do not close KS-1346. `routes/adminConfig.ts:104` (50 call sites) and `routes/webhooks.ts:566` (7) still log `String(err)`, and Done-when 3 (the rotate-secret cell) is not delivered. This brief covers adminConfig. Part D (`../KS-1346-D-webhooks/`) covers webhooks and the rotate-secret cell.
- **Base:** develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45`, confirmed by `git ls-remote` at 04:48 and again at 05:00.
- **Edit points:** 1. All 50 call sites go through the one helper, so no split is needed.
- **Attached PRs:** #1311 and #1312 are merged; #1296 and #1297 are closed without merging. No `supersedes=` pin is needed.

## Files
- `KS-1346.md` is the brief: ONE product line (`@@ -101,6 +101,6 @@`, the same line as #1311/#1312, two-space indent) and ONE new jest file of 117 lines.
- `KS-1346.golden.diff` is the golden, sha256 `fe231dcfdfdd…`.
- **Fence rebuild:** the diff rebuilt from the brief's own `File:`/`Test file:` lines and its two fences is **IDENTICAL** to the golden (`cmp`, run twice). Comparator control: a one-token mutation (`password]` changed to `passwor]`) printed **DIFFER**.
- `+`/`-` counts (`l and l[0] in '+-'`, excluding the headers): **118 + / 1 -**.
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote. There are 0 non-ASCII lines and 0 blank context lines.

## Measured (scratch clone at `ec32c40e`, node_modules farmed by `prepare_clone.sh`, rc 0)

| step | instrument | result |
|---|---|---|
| strict apply | `patch -p1 -F0 --dry-run` / `git apply --check` | rc 0 / rc 0 |
| test file alone (RED) | `npx jest <file> --json` | **4 failed / 11 passed / 15**: exactly the four `RED KS-1346 C1` rows, by ASSERTION (received `"[object Object]"` ×4; 0 TypeError/ts errors in the log) |
| golden applied (GREEN) | same | **15 / 15** |
| tsc | `npx tsc --noEmit -p .` | rc 0 |
| tsc with tests | a temp tsconfig extending originate's with `exclude` limited to node_modules/dist | rc 0. Instrument control, run once on part D's test file with the same temp tsconfig: a planted `const x: number = 'x'` gave rc 2 (default tsconfig: rc 0, blind to tests) |
| eslint | `npx eslint src/routes/adminConfig.ts <new test>` | rc 0. Two warnings (`:2089` prefer-const, `:2129` unused `e`) are IDENTICAL at the tip. Instrument control, run on part D's test file: a planted `var` gave rc 1 |
| whole originate suite | `npx jest --json` | tip **86 suites / 1013 passed / 0 failed**; golden **87 / 1028 passed / 0 failed**. No new red; +15 = this file |

**Arms** (golden test against variant product lines; the clone was restored with `git checkout` and checked clean after each arm):

| arm | failed / total | which |
|---|---|---|
| base product (`String(err)`) | 4 / 15 | C1 ×4 only |
| `inspect(err)` tamper (`typeof err === 'string' ? err : require('util').inspect(err)`) | **8 / 15** | C1 ×4 AND the no-value control C6 ×4 (the control working) |
| golden | 0 / 15 | none |

## build_input: rc 0
The first pass without `started_ok` was REFUSED because the ticket is In Progress. With the pin:
```
NIGHT_SOURCE_CHECKOUT=<clone at ec32c40e> NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-C-adminconfig bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1346 <out>/input.json product=Blockchain/Dev/services/originate/src/routes/adminConfig.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts line=104 ctx=65536 "started_ok=Kam-ruled-2026-09-27-16:32-card-secuura-ks1346-option-a;residue-per-gate33-F-3;parts-A-B-merged-#1311-#1312"
```
The output:
- `prompt source: WEDNESDAY BRIEF …/KS-1346-C-adminconfig/KS-1346.md (12563 chars) — the ticket description is NOT the prompt`;
- red cells `['RED KS-1346 C1']`;
- 1 expected `+` line (A3c);
- `suggested_test_file` = `ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts`;
- the contract key set is OK.

**Size:**
- **Whole file:** adminConfig.ts is 100,531 B, under the 160,000 B default trigger. That gives input.json 138,035 B, about **34.5K prompt tokens**.
- **Excerpted:** with `NIGHT_EXCERPT_TRIGGER_BYTES=90000`, the file becomes 3 regions `[(1,60),(76,132),(2064,2154)]` = 10,875 B. That gives input.json 50,514 B, about **12.6K prompt tokens** (rc 0).
- **Recommendation:** use the excerpt. adminConfig has been excerpted twice before, and both rounds passed byte-identical (ladder rows 14 and 20).

## The round command (NOT run)
`round.sh` pins `SRC=sparkfeed` and `TIP=94c9c7aa`, but develop is now `ec32c40e`. The round seat must do two things first:
1. Bring sparkfeed to `ec32c40e`, per IMPROVEMENTS 2026-09-27 19:22: fetch INTO sparkfeed, check it out, and confirm it is clean.
2. Run a copy of `round.sh` with `TIP=ec32c40e2b1e2698d2e855a916f390d48dad1b45`.

The round, in the row-28 form:
```
bash <round.sh copy, TIP=ec32c40e…> KS-1346-C-adminconfig KS-1346 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-C-adminconfig 90000 product=Blockchain/Dev/services/originate/src/routes/adminConfig.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts line=104 ctx=65536 "started_ok=Kam-ruled-2026-09-27-16:32-card-secuura-ks1346-option-a;residue-per-gate33-F-3;parts-A-B-merged-#1311-#1312"
```
The scratch `input.json` files name a scratchpad `source_checkout`. Do NOT queue them.

## OPEN DOUBTS
- **No Spark round was run.** This is a brief and a golden only.
- The behavioural cells drive 4 of the 50 sites. The other 46 share the one helper line, and ks730c's source cell C3 (50 helper calls, 50 distinct contexts) still passes.
- `$queryRaw` rejecting with a plain object is synthetic. As gate33 says, nothing in originate is known to throw a non-Error today (READ).
- The ruled residue F-2 (field NAMES as data, e.g. an email-shaped key) applies here as it does to A and B. It is not hardened.
- If D merges first, or C does, nothing conflicts: the two briefs touch different files.
