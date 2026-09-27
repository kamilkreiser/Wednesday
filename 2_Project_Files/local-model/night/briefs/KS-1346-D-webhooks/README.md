# KS-1346 part D: Spark brief + golden (the ruled residue, webhooks.ts, plus the rotate-secret cell)

Written 05:00 AEST 2026-09-28 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and `ls-remote` were READ) and wrote nothing under `!CODING/`. Every git write verb ran in the scratch clone `ks1346cd/base` (a `--shared` clone of sparkfeed, develop fetched into it by SSH).

- **Ruling:** Kam, live board 2026-09-27 16:32, card `secuura-ks1346-logging-thrown-objects-leaks-secrets`, option a: "Type and field names only".
- **Why this brief:** gate33 F-3 (`2026-09-28-batch1310-g33/report.md:200-204`) names two gaps. `routes/webhooks.ts:566` (7 call sites) still logs `String(err)`, and "DoD item 3 (the rotate-secret cell) is not delivered".
- **What the rotate-secret cell is.** Read from Linear KS-1346, Done-when 3: "a cell pins rotate-secret throwing after `newSecret` exists, asserting the secret is absent from the body and from every logger call".
  - It is a TEST-ONLY pin. Gate29 measured today's behaviour as safe.
  - It lives on `POST /:id/rotate-secret` in webhooks.ts, so it belongs in **D** and in neither A, B nor C. It is delivered here as cell `control KS-1346 D7`.
- **Base:** develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45`, by `git ls-remote` at 04:48 and 05:00.
- **Edit points:** 1 product line. All 7 call sites go through the one helper.
- **Supersedes:** no pin is needed. #1311 and #1312 are merged, and #1296 and #1297 are closed.

## Files
- `KS-1346.md` is the brief: ONE product line (`@@ -563,6 +563,6 @@`) and ONE new jest file of 134 lines.
- `KS-1346.golden.diff` is the golden, sha256 `2ed8cf347c79…`.
- **Fence rebuild:** the diff rebuilt from the brief's fences is **IDENTICAL** to the golden (`cmp`, run twice). Comparator control: a one-token mutation (`password]` changed to `passwor]`) printed **DIFFER**.
- `+`/`-` counts (`l and l[0] in '+-'`, excluding the headers): **135 + / 1 -**.
- **Char lint:** 0 `+` lines with a backslash, backtick or double quote. 0 non-ASCII lines. 0 blank context lines.

## The test's harness
The harness is ks1341b's, with two changes:
- `encryptField` wraps the REAL `@secuura/shared` `encryptField`, and `beforeAll` registers key v1 and activates it. Gate29's S1 probe used the real `encryptField` with a key loaded, and D7 asserts the ciphertext really starts with `v1:`.
- All four logger levels are named mocks.

The routes are PATCH, DELETE and rotate-secret. The remaining sites are not driven:
- GET / and GET /:id/deliveries swallow their query errors with `.catch`, so they never reach fail500 from a DB throw;
- POST / and POST /:id/test need more setup.

## Measured (scratch clone at `ec32c40e`, node_modules farmed by `prepare_clone.sh`, rc 0)

| step | instrument | result |
|---|---|---|
| strict apply | `patch -p1 -F0 --dry-run` / `git apply --check` | rc 0 / rc 0 |
| test file alone (RED) | `npx jest <file> --json` | **3 failed / 10 passed / 13**: exactly the three `RED KS-1346 D1` rows, by ASSERTION (received `"[object Object]"` ×3; 0 TypeError/ts errors). D7 is green at the tip, as the ticket expects |
| golden applied (GREEN) | same | **13 / 13** |
| tsc | `npx tsc --noEmit -p .` | rc 0 |
| tsc with tests | a temp tsconfig extending originate's, tests included | rc 0. Control: a planted type error gave rc 2 |
| eslint | `npx eslint src/routes/webhooks.ts <new test>` | rc 0, no output. Control: a planted `var` gave rc 1 |
| whole originate suite | `npx jest --json` | tip **86 suites / 1013 passed / 0 failed**; golden **87 / 1026 passed / 0 failed**. No new red; +13 = this file |

**Arms** (the clone was restored and checked clean after each):

| arm | failed / total | which |
|---|---|---|
| base product (`String(err)`) | 3 / 13 | D1 ×3 only |
| `inspect(err)` tamper | **6 / 13** | D1 ×3 AND the no-value control D6 ×3 (the control working) |
| rotate-secret with a planted `logger.debug('…', { newSecret })` | 1 / 13 | D7 only (D7 can fail) |
| golden | 0 / 13 | none |

## build_input: rc 0
The first pass without `started_ok` was REFUSED (the ticket is In Progress). With the pin:
```
NIGHT_SOURCE_CHECKOUT=<clone at ec32c40e> NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-D-webhooks bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1346 <out>/input.json product=Blockchain/Dev/services/originate/src/routes/webhooks.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts line=566 ctx=65536 "started_ok=Kam-ruled-2026-09-27-16:32-card-secuura-ks1346-option-a;residue-per-gate33-F-3;parts-A-B-merged-#1311-#1312"
```
The output:
- `prompt source: WEDNESDAY BRIEF …/KS-1346-D-webhooks/KS-1346.md (14067 chars) — the ticket description is NOT the prompt`;
- red cells `['RED KS-1346 D1']`;
- 1 expected `+` line (A3c);
- `suggested_test_file` = `ks1346d-webhooks-fail500-logs-type-and-field-names.test.ts`;
- the contract key set is OK;
- input.json 55,167 B, about **13.8K prompt tokens** (whole file, no excerpt).

## The round command (NOT run)
As for part C:
1. Sparkfeed must first be brought to `ec32c40e`, fetched INTO it and clean.
2. Then run a `round.sh` copy with `TIP=ec32c40e2b1e2698d2e855a916f390d48dad1b45`:
```
bash <round.sh copy, TIP=ec32c40e…> KS-1346-D-webhooks KS-1346 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1346-D-webhooks - product=Blockchain/Dev/services/originate/src/routes/webhooks.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts line=566 ctx=65536 "started_ok=Kam-ruled-2026-09-27-16:32-card-secuura-ks1346-option-a;residue-per-gate33-F-3;parts-A-B-merged-#1311-#1312"
```
Do NOT queue the scratch `input.json`: it names a scratchpad `source_checkout`.

## OPEN DOUBTS
- **No Spark round was run.**
- **D7 is a pin, not a red.** It is green at the tip and after, because the behaviour is already safe (gate29 S1). Its fail-ability is shown only by the planted-log arm.
- **D7 does not cover everything the probe did.** Its UPDATE rejects with an `Error`, so it proves the secret is kept out of the log. It does not cover a Prisma error object whose own fields might carry the bound ciphertext. Under the ruling, such an object would log only field NAMES.
- **The real key sits in the process keyring for this file's lifetime.** It is not reset in `afterAll`. jest isolates module registries per file, so no other suite was affected: the whole suite stayed green.
- The behavioural cells drive 3 of the 7 sites. The other 4 share the one helper line.
- **F-2 is not hardened.** The ruled residue (field NAMES as data) applies here as it does to A and B.
