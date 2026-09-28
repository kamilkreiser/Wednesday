# KS-1359: Spark brief + golden (GET /api/platform/audit-log refuses a wrong-type or below-minimum limit/offset with 400 (the KS-5 clamp unchanged))

**RULED (a) by Kam 2026-09-29 09:05 (card KS-1359).** It is no longer held pending the 18:00 default.

Written 09:25 AEST 2026-09-29 (shell `date`) by a Spark brief-writer for Wednesday. Secuura/Blockchain only. The writer ran no model, raised no PR, and changed no GitHub or Linear state: Linear was only READ, by `build_input.sh`. It mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran in its own `--shared` clone `scratchpad/bw0929b/src`, whose origin is GitHub. The Blockchain checkout was only read, and its tracked-modified count was 0 after every farm.

- **Base:** develop `0de108577e6199de3c9402c0643a2944d86aee97`, read by `git ls-remote` at 09:06 and again at 09:08 AEST (unchanged from the commission). `215cc687..0de10857` changes no `package.json` or lockfile.
- **Shape:** `platform.ts` gets 6 lines inserted between `:363` and `:364`, at the top of the handler. A PRESENT `limit` that is not `/^[0-9]+$/` with value >= 1, or a PRESENT `offset` that is not `/^[0-9]+$/` with value >= 0 (arrays and empty strings included), answers 400 before any upstream call or query. **400 body, from the file's own validation style (`:503`, `:541`):** `{ success: false, error: { code: 'VALIDATION_ERROR', message: 'limit must be an integer from 1 and offset an integer from 0' } }`. The clamp lines `:370`/`:376`/`:377` are byte-identical.
- **Harness:** The new 83-line test mounts the REAL `createPlatformRoutes` on `127.0.0.1:0` with injected deps: a `super_admin` stand-in for `authenticateToken`, `tenantProvisioningUrl` set to a closed port (that leg fails fast and degrades as in production), and a fake `query` that records the overfetch (`limit + offset`). `PLATFORM_AUDIT_MAX_OFFSET` is stubbed to 5000. It needs no `vi.mock`.

## Files
- `KS-1359.md` is the brief: 17,953 chars, sha256 `5693c8b9d28c68d9…`.
- `KS-1359.golden.diff` is the golden: sha256 `3097c617c545d8c5…`. It touches 2 files: the product hunk plus the NEW test file.
- **Fence check:** the brief's ```diff fence is byte-identical to the golden's product hunk, and its plain test fence is byte-identical to the golden's new-file body (`fence2.py`). Control: one mutated token in a copy of the brief printed DIFFER.
- **Char lint:** 0 `+` lines contain a backslash, backtick, double quote or non-ASCII character. There are 0 blank context lines. The A3d pre-check found 0 test `+` lines equal to a product-tip line.

## Measured (scratch clone at 0de10857; vitest from the farmed tree)

| step | result |
|---|---|
| `git apply --check` at the tip | rc 0 |
| test file ALONE at the tip (RED) | **4 failed / 3 passed / 7 (B1 offset -1, B2 limit abc, B3 limit 0, B4 offset 1.5; by assertion)** |
| golden applied (GREEN) | **7 / 7** |
| api-gateway suite | tip **88 files / 795 / 0**; golden **89 files / 802 / 0** (0 new reds) |
| `tsc --noEmit -p services/api-gateway` | rc 0 with the golden (rc 0 at the tip too; the config excludes tests) |
| eslint on both files with the golden | rc 0, 0 errors (1 pre-existing warning at platform.ts:989) |
| **real checker** (`tasks/code_patch/checker.sh`, golden as model output, fresh clone + `prepare_clone.sh`) | **RESULT: PASS (7/7)** |
| **real Spark checker** (`spark_checker.sh`, the same way) | **SPARK RESULT: PASS** (7/7 + A2a anchor 1/1 hunk ok, new file skipped) |

**Arms** (the golden test against a variant product file; the product was restored and porcelain was 0 after each):

| arm | result |
|---|---|
| the insertion absent (the tip) | 4 failed / 7: B1-B4 |
| limit minimum 1 changed to 0 | 1 failed / 7: B3 |
| the regex admits `.` | 1 failed / 7: B4 |
| also refuses above 500 (undoes KS-5) | 1 failed / 7: the clamp control |
| offset minimum 0 changed to 1 | 1 failed / 7: the `limit 10 offset 0` control |

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/407373b1-2c8c-4c6e-b92a-14f32c2c8007/scratchpad/bw0929b/src NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1359 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1359 <out>/input.json product=Blockchain/Dev/services/api-gateway/src/routes/platform.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-mint-scope.test.ts line=370 ctx=65536
```
`prompt source: WEDNESDAY BRIEF … KS-1359.md` · `suggested_test_file` = the brief's `## The test` File: line · `contract: key set == KS-871 input` · input.json 76,815 B, about 19.2K prompt tokens. The source clone's origin is `git@github.com:Secuura/Distributed_Secuura.git`, checked with `git remote get-url origin`.

## The round command (NOT run)
Use the round.sh copy pinned to this tip: `scratchpad/bw0929b/round_0de10857.sh` in session `407373b1…`. It is `screen0929/round_215cc687.sh` with ONLY `SP`, `SRC` (= `bw0929b/src`) and `TIP` (= `0de10857…`) changed (`diff` read). It refuses if the source is not clean at the tip.
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/407373b1-2c8c-4c6e-b92a-14f32c2c8007/scratchpad/bw0929b/round_0de10857.sh KS-1359-R1 KS-1359 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1359 - product=Blockchain/Dev/services/api-gateway/src/routes/platform.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-mint-scope.test.ts line=370 ctx=65536
```
⚠ `bw0929b/src`'s `node_modules` entries are symlinks into the Blockchain checkout's installed `node_modules` (read-only). If develop moves, re-pin `TIP` and re-check out the clone. If the session scratchpad is cleaned, the source is gone.

**Round counter:** 0 rows in `night/done.md`, no `READY_KS-1359*`, no earlier brief (control: KS-908 shows 3 rows and 2 READY files). This is round 1, with one rebrief allowed; after that it goes to the cloud.

**Collision:** 21 live PR merge refs at 09:08 AEST. Those heads plus every head #1320-#1338 (39 in all) were fetched and diffed against their merge-base. None touches this product file or a same-name test. The only wallet-connector hit is #649, on `package.json`.

**Scope:** Refs KS-1359 (ruled option (a)). A re-sweep and the KS-1361 baseline are outside this diff.

## UNMEASURED / doubts for Wednesday
1. **No Spark model round** was run. Both checkers were run on the golden only.
2. **No live stack.** It is a runtime change, and a §5f sweep is owed after merge.
3. No Schemathesis re-sweep. By the ruling, the 6 above-maximum coverage cases stay 200 (the clamp). The spec's `limit maximum: 200` against the code's 500 clamp is untouched.
4. `?limit=` (empty) is now 400. Whether any client sends it was not measured. The only UI caller (`PlatformAuditLog.tsx:29`) sends integers.
5. `VALIDATION_ERROR` (not `BAD_REQUEST`) was chosen because the file uses it for a present value of the wrong shape. `BAD_REQUEST` is used for missing values. If a reviewer prefers `BAD_REQUEST`, both the golden and the brief change in one token each.
6. **Open PRs come from `ls-remote`** plus fetched heads, not the GitHub files API. A PR opened after 09:08 would be missed.
