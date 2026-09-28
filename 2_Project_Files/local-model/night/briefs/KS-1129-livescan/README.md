# KS-1129 LIVESCAN: Spark carve brief + golden (the gateway's live chain-scan read gets the persisted read's three shape guards)

Written 16:08 AEST 2026-09-28 (shell `date`) by a carve drafter for Wednesday. It ran no model, raised no PR, and changed no GitHub or Linear state (Linear, `ls-remote` and the builder's PR-state read were READ). It wrote nothing under `!CODING/`. Every git write verb ran in its own clones in the session scratchpad.

- **Base:** develop `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`, read by `ls-remote` at 15:53 AEST. The source clone `carve_base` (a copy of `ks1346cd/base`, fetched to `d9ce1403` from `verify_clone`) read HEAD == `d9ce1403` and porcelain 0 before and after every step.
- **What was carved:** KS-1129 is a 5-item ticket that went cloud (sites 1 and 2 merged as #1220 and #1280). Item 4, the api-gateway live chain-scan shape rule ("O1"), is ONE product file with its fix shape spelled in the ticket's RULED checklist. This brief is that item only.
- **Edit points:** 2 change regions in ONE hunk (`:606-:607` and `:609`, with `:608` as context between them): 5 `+` / 3 `-`.
- **Round counter:** 0 (`night/done.md` has no KS-1129 row; no `READY_*KS-1129*`).

## Files
- `KS-1129.md` is the brief: one product hunk and one INSERTION into the existing `ks1069-persisted-anchored-input-shape.test.ts` (reuses its stubbed-anchoring harness; 49 `+` lines, 8 cells).
- `KS-1129.golden.diff`, sha256 `e651a9001e6e…`, 4,462 B: 2 files, **54 + / 3 -**.
- **Fence rebuild:** the diff rebuilt from the brief's `File:` / `Test file:` lines and its two fences is **IDENTICAL** to the golden. Comparator control: a one-token mutation (`4242` -> `4243` in `LIVE_REAL`) read **DIFFER**.
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote; 0 non-ASCII lines in the golden; 0 blank context lines.

## Measured (scratch clone `carve/c1129` at `d9ce1403`, node_modules farmed by `prepare_clone.sh`, shared built in the clone)

| step | instrument | result |
|---|---|---|
| strict apply | `git apply --check` / `patch -p1 -F0 --dry-run` | rc 0 / rc 0 |
| test hunk alone (RED) | `vitest run <file> --reporter=json` | **6 failed / 14 passed / 20**: exactly L1-L6, each by ASSERTION (`expected { verified: true, ... } to deeply equal { verified: false, ... }`) |
| golden applied (GREEN) | same | **20 / 20** |
| whole api-gateway suite | `vitest run --reporter=json` | tip **86 files / 773 passed / 0 failed**; golden **86 / 781 / 0** (+8 = the new cells; same file count, the test file is modified in place) |
| tsc | `tsc --noEmit -p services/api-gateway` | rc 0 at the tip and with the golden |
| tsc with tests | temp config extending the package tsconfig, `include src/**/*.ts`, `exclude []`, `types: [node]` (vitest is imported); both changed files proven IN the program (`--listFilesOnly`) | rc 2 at both, **31 errors at both, the SAME set** (positions stripped), **0 naming either changed file**. Positive control: a planted `const x: number = 'not-a-number'` in the ks1069 file surfaces exactly one TS2322 naming it. (A first config without explicit `types` read 54 at both, same set; its one hit in a touched file was `ks1069…test.ts(148,3) TS2741`, pre-existing, on a line this brief does not touch.) |
| eslint | both changed files | rc 0 at both; 5 warnings at both, the same set. Control: a planted `debugger` + `var` gave rc 1, 2 errors |

**Arms** (the golden applied, one product line put back at a time; the clone reset after each):

| arm | line changed back | failed / total | which |
|---|---|---|---|
| verified | `if (j.verified === true && !j.simulated) {` -> `if (j.verified) {` | 2 / 20 | L1, L6 |
| hash | the placeholder rule -> `liveTxHash = liveHash;` | 1 / 20 | L2 |
| height | the strict height rule -> `blockNum != null ? Number(blockNum) : null` | 3 / 20 | L3, L4, L5 |
| golden | none | 0 / 20 | none |

Each guard is separately load-bearing, and the controls (C1, C2) and the 12 KS-1069 cells stay green in every arm.

## build_input: rc 0 (both forms)
```
NIGHT_SOURCE_CHECKOUT=<scratchpad>/carve_base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1129-livescan bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1129 <out>/input.json product=Blockchain/Dev/services/api-gateway/src/routes/verification.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1071-verify-confidence-one-mapping.test.ts test_file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts line=606 ctx=65536 "started_ok=carve of checklist item 4 (gateway live chain-scan read); #1220 #1280 #999 merged; no seat on api-gateway verification.ts"
```
- `prompt source: WEDNESDAY BRIEF … (15891 chars)`; the 3 attached PRs read **merged** (#1280, #1220, #999); the In Progress state admitted by `started_ok` (printed WARN).
- red cells `RED KS-1129 L1` … `L6`; 5 expected `+` lines (A3c); `test_file` pinned (modify in place) and `suggested_test_file` == the brief's File: line; contract key set OK.
- **Whole file:** input.json 122,666 B, about **30.7K prompt tokens** (the builder's own estimate; the 09-27 notes say it runs 35-73% low).
- **Excerpted (`NIGHT_EXCERPT_TRIGGER_BYTES=60000`), RECOMMENDED:** 72,040 B -> 24,022 B in 3 regions `(1-197), (213-284), (567-815)`, input.json 78,045 B, about **19.5K prompt tokens**. The edit region `:603-:612` is inside `(567-815)`.
- `carve_base` porcelain 0 before and after.

## The round command (NOT run)
Use the copy of round.sh pinned to this tip: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve/round_d9ce1403.sh`. It differs from the 09-27 `sparkrun/round.sh` in three lines only (`SP`, `SRC` = `carve_base`, `TIP` = `d9ce1403…`), and it refuses if the source is not clean at the tip.
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/carve/round_d9ce1403.sh KS-1129-LIVESCAN-R1 KS-1129 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1129-livescan 60000 product=Blockchain/Dev/services/api-gateway/src/routes/verification.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1071-verify-confidence-one-mapping.test.ts test_file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1069-persisted-anchored-input-shape.test.ts line=606 ctx=65536 "started_ok=carve of checklist item 4 (gateway live chain-scan read); #1220 #1280 #999 merged; no seat on api-gateway verification.ts"
```
⚠ `carve_base`'s `node_modules` entries are symlinks into another session's scratchpad (`d0b2ec3e…/scratchpad/sparkfeed/…`), inherited from `ks1346cd/base`. If that directory is cleaned, `prepare_clone.sh` will farm dead links.

## For the raise (after a PASS)
- Two files, no generated companion: `verification.ts` is not an OpenAPI registration, so `check:openapi` is not affected (not run).
- **It is a RUNTIME change on the verify route** (the demo's on-chain badge reads it). §5f: a live sweep is owed before Done.
- PR body: `Refs KS-1129` (item 4 only), no closing keyword.

## OPEN DOUBTS (for Wednesday)
- **"A held surface."** The 09-25 #1280 comment on KS-1129 calls the gateway chain-scan readers "a held surface" and gives no reason. The phrase "held surface" occurs nowhere in `WEDNESDAY/0_Brain` (recursive grep, 0 hits), no open PR touches the file, and api-gateway changes merged on 09-27 (#1305, #1306). **Confirm the hold has lapsed before queuing.**
- **L5 (strict height) is a behaviour choice carried from the E7 ruling** ("the same three guards PR #969 gave the persisted read"). If a live responder ever sends a numeric-string height, the route will now say off-chain-only where it said on-chain. Anchoring's own reply emits a number since #1220 (`anchorReadback.ts:134`, `toBlockNumber`). If Wednesday prefers coercion for the live read, drop L5 and change the `+` height line before the round.
- No Spark round, no `spark_checker.sh`, no live stack.
