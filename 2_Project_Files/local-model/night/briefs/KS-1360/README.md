# KS-1360: Spark brief + golden (DELETE /api/wallets/session/:sessionId answers 200 `{ success: true, message: 'Session disconnected' }`)

**RULED (a) by Kam 2026-09-29 09:05 (card KS-1360).** It is no longer held pending the 18:00 default.

Written 09:25 AEST 2026-09-29 (shell `date`) by a Spark brief-writer for Wednesday. Secuura/Blockchain only. The writer ran no model, raised no PR, and changed no GitHub or Linear state: Linear was only READ, by `build_input.sh`. It mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran in its own `--shared` clone `scratchpad/bw0929b/src`, whose origin is GitHub. The Blockchain checkout was only read, and its tracked-modified count was 0 after every farm.

- **Base:** develop `0de108577e6199de3c9402c0643a2944d86aee97`, read by `git ls-remote` at 09:06 and again at 09:08 AEST (unchanged from the commission). `215cc687..0de10857` changes no `package.json` or lockfile.
- **Shape:** `server.ts:219` `res.json({ message: 'Session disconnected' });` becomes `res.json({ success: true, message: 'Session disconnected' });`. It is one line, additive. The hunk has NO leading context, because `:218` is whitespace-only and the builder refuses a blank context line. Its trailing context is `:220` `});`.
- **Harness:** **How the boot-at-import was avoided, with no second product edit:** no existing wallet-connector test drives `server.ts`. Each of them tests an extracted helper, mirrors the composition in its own app, or is the placeholder. The new 75-line test uses three hoisted `vi.mock`s. `../db` gets an `initDb` whose promise never settles, so `app.listen` at `:327`/`:339` never runs, and `isDbAvailable` returns false (the in-memory path). `../userErasedSubscriber` becomes a no-op. `@secuura/shared` is the real module with only `authenticate` replaced by a pass-through. The test then serves the REAL exported `app` (`:351`) on `127.0.0.1:0`, creates a session with the real POST, and deletes it.

## Files
- `KS-1360.md` is the brief: 14,405 chars, sha256 `3fffb742b1f7660d…`.
- `KS-1360.golden.diff` is the golden: sha256 `d86e2d393305b2f0…`. It touches 2 files: the product hunk plus the NEW test file.
- **Fence check:** the brief's ```diff fence is byte-identical to the golden's product hunk, and its plain test fence is byte-identical to the golden's new-file body (`fence2.py`). Control: one mutated token in a copy of the brief printed DIFFER.
- **Char lint:** 0 `+` lines contain a backslash, backtick, double quote or non-ASCII character. There are 0 blank context lines. The A3d pre-check found 0 test `+` lines equal to a product-tip line.

## Measured (scratch clone at 0de10857; vitest from the farmed tree)

| step | result |
|---|---|
| `git apply --check` at the tip | rc 0 |
| test file ALONE at the tip (RED) | **1 failed / 2 passed / 3 (D1, by assertion)** |
| golden applied (GREEN) | **3 / 3** |
| wallet-connector suite | tip **7 files / 45 / 0**; golden **8 files / 48 / 0** (0 new reds) |
| `tsc --noEmit -p services/wallet-connector` | rc 0 with the golden (rc 0 at the tip too; the config excludes tests) |
| eslint on both files with the golden | rc 0, no findings |
| **real checker** (`tasks/code_patch/checker.sh`, golden as model output, fresh clone + `prepare_clone.sh`) | **RESULT: PASS (7/7)** |
| **real Spark checker** (`spark_checker.sh`, the same way) | **SPARK RESULT: PASS** (7/7 + A2a anchor 1/1 hunk ok, new file skipped) |

**Arms** (the golden test against a variant product file; the product was restored and porcelain was 0 after each):

| arm | result |
|---|---|
| `:219` back to the tip text | 1 failed / 3: D1 |
| `success: false` at `:219` | 1 failed / 3: D1 |
| `success: true` pasted into the 404 body at `:216` | 1 failed / 3: the 404 control |

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/407373b1-2c8c-4c6e-b92a-14f32c2c8007/scratchpad/bw0929b/src NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1360 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1360 <out>/input.json product=Blockchain/Dev/services/wallet-connector/src/server.ts ref=Blockchain/Dev/services/wallet-connector/src/__tests__/ks452-malformed-body-json.test.ts line=219 ctx=65536
```
`prompt source: WEDNESDAY BRIEF … KS-1360.md` · `suggested_test_file` = the brief's `## The test` File: line · `contract: key set == KS-871 input` · input.json 35,119 B, about 8.8K prompt tokens. The source clone's origin is `git@github.com:Secuura/Distributed_Secuura.git`, checked with `git remote get-url origin`.

## The round command (NOT run)
Use the round.sh copy pinned to this tip: `scratchpad/bw0929b/round_0de10857.sh` in session `407373b1…`. It is `screen0929/round_215cc687.sh` with ONLY `SP`, `SRC` (= `bw0929b/src`) and `TIP` (= `0de10857…`) changed (`diff` read). It refuses if the source is not clean at the tip.
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/407373b1-2c8c-4c6e-b92a-14f32c2c8007/scratchpad/bw0929b/round_0de10857.sh KS-1360-R1 KS-1360 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1360 - product=Blockchain/Dev/services/wallet-connector/src/server.ts ref=Blockchain/Dev/services/wallet-connector/src/__tests__/ks452-malformed-body-json.test.ts line=219 ctx=65536
```
⚠ `bw0929b/src`'s `node_modules` entries are symlinks into the Blockchain checkout's installed `node_modules` (read-only). If develop moves, re-pin `TIP` and re-check out the clone. If the session scratchpad is cleaned, the source is gone.

**Round counter:** 0 rows in `night/done.md`, no `READY_KS-1360*`, no earlier brief (control: KS-908 shows 3 rows and 2 READY files). This is round 1, with one rebrief allowed; after that it goes to the cloud.

**Collision:** 21 live PR merge refs at 09:08 AEST. Those heads plus every head #1320-#1338 (39 in all) were fetched and diffed against their merge-base. None touches this product file or a same-name test. The only wallet-connector hit is #649, on `package.json`.

**Scope:** Refs KS-1360 (ruled option (a)). A re-sweep and the KS-1361 baseline are outside this diff.

## UNMEASURED / doubts for Wednesday
1. **No Spark model round** was run. Both checkers were run on the golden only.
2. **No live stack.** It is a runtime change, and a §5f sweep is owed after merge.
3. The JWT check is replaced in the test (auth is not under test). In production it is real and unchanged.
4. No re-sweep. `WalletSuccessSchema` (`openapi.ts:296`-`:302`, `success: boolean`, `message` optional, passthrough) matches the new body when read. The generated spec was not regenerated.
5. Whether the never-settling `initDb` promise slows worker teardown was not measured beyond the suite finishing at rc 0.
6. **Open PRs come from `ls-remote`** plus fetched heads, not the GitHub files API. A PR opened after 09:08 would be missed.
