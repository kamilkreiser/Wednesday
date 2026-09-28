# KS-1369: Spark brief + golden (the gateway proxy hook returns early once the outgoing headers are sent)

**RULED (a) by Kam 2026-09-29 09:05 (card KS-1369).** It is no longer held pending the 18:00 default.

Written 09:25 AEST 2026-09-29 (shell `date`) by a Spark brief-writer for Wednesday. Secuura/Blockchain only. The writer ran no model, raised no PR, and changed no GitHub or Linear state: Linear was only READ, by `build_input.sh`. It mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran in its own `--shared` clone `scratchpad/bw0929b/src`, whose origin is GitHub. The Blockchain checkout was only read, and its tracked-modified count was 0 after every farm.

- **Base:** develop `0de108577e6199de3c9402c0643a2944d86aee97`, read by `git ls-remote` at 09:06 and again at 09:08 AEST (unchanged from the commission). `215cc687..0de10857` changes no `package.json` or lockfile.
- **Shape:** `proxy.ts` gets 2 lines inserted between `:242` and `:243`. They are a KS-1369 comment and `if (proxyReq.headersSent) return;`, and they become the first statement of `onProxyReq`. No other product line changes.
- **Harness:** The new 63-line test mocks `http-proxy-middleware`'s `createProxyMiddleware` with `vi.mock`, so the REAL `createProxyRoutes` hands over the REAL options that `createServiceProxy` builds. The test then calls `onProxyReq` directly with a fake `proxyReq`: `headersSent` true and `setHeader` throwing (H1), `headersSent` true with calls recorded (H2), and `headersSent` false (the control, which expects 5 writes in order). The screen said no test reaches `onProxyReq`. More precisely, `ks1041-vouch-mint-scope` does reach it, but only through real HTTP, where `headersSent` is always false. Nothing reached the already-sent case.

## Files
- `KS-1369.md` is the brief: 14,142 chars, sha256 `91b57674488b95ba…`.
- `KS-1369.golden.diff` is the golden: sha256 `22ef5b312a2f3cb0…`. It touches 2 files: the product hunk plus the NEW test file.
- **Fence check:** the brief's ```diff fence is byte-identical to the golden's product hunk, and its plain test fence is byte-identical to the golden's new-file body (`fence2.py`). Control: one mutated token in a copy of the brief printed DIFFER.
- **Char lint:** 0 `+` lines contain a backslash, backtick, double quote or non-ASCII character. There are 0 blank context lines. The A3d pre-check found 0 test `+` lines equal to a product-tip line.

## Measured (scratch clone at 0de10857; vitest from the farmed tree)

| step | result |
|---|---|
| `git apply --check` at the tip | rc 0 |
| test file ALONE at the tip (RED) | **2 failed / 1 passed / 3 (H1 and H2, by assertion)** |
| golden applied (GREEN) | **3 / 3** |
| api-gateway suite | tip **88 files / 795 / 0**; golden **89 files / 798 / 0** (0 new reds) |
| `tsc --noEmit -p services/api-gateway` | rc 0 with the golden (rc 0 at the tip too; the config excludes tests) |
| eslint on both files with the golden | rc 0, 0 errors (4 pre-existing warnings in proxy.ts, none on an inserted line) |
| **real checker** (`tasks/code_patch/checker.sh`, golden as model output, fresh clone + `prepare_clone.sh`) | **RESULT: PASS (7/7)** |
| **real Spark checker** (`spark_checker.sh`, the same way) | **SPARK RESULT: PASS** (7/7 + A2a anchor 1/1 hunk ok, new file skipped) |

**Arms** (the golden test against a variant product file; the product was restored and porcelain was 0 after each):

| arm | result |
|---|---|
| guard line deleted | 2 failed / 3: H1, H2 |
| guard inverted (`!proxyReq.headersSent`) | 3 failed / 3: H1, H2 and the control |

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/407373b1-2c8c-4c6e-b92a-14f32c2c8007/scratchpad/bw0929b/src NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1369 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1369 <out>/input.json product=Blockchain/Dev/services/api-gateway/src/routes/proxy.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-mint-scope.test.ts line=242 ctx=65536
```
`prompt source: WEDNESDAY BRIEF … KS-1369.md` · `suggested_test_file` = the brief's `## The test` File: line · `contract: key set == KS-871 input` · input.json 85,142 B, about 21.3K prompt tokens. The source clone's origin is `git@github.com:Secuura/Distributed_Secuura.git`, checked with `git remote get-url origin`.

## The round command (NOT run)
Use the round.sh copy pinned to this tip: `scratchpad/bw0929b/round_0de10857.sh` in session `407373b1…`. It is `screen0929/round_215cc687.sh` with ONLY `SP`, `SRC` (= `bw0929b/src`) and `TIP` (= `0de10857…`) changed (`diff` read). It refuses if the source is not clean at the tip.
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/407373b1-2c8c-4c6e-b92a-14f32c2c8007/scratchpad/bw0929b/round_0de10857.sh KS-1369-R1 KS-1369 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1369 - product=Blockchain/Dev/services/api-gateway/src/routes/proxy.ts ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-mint-scope.test.ts line=242 ctx=65536
```
⚠ `bw0929b/src`'s `node_modules` entries are symlinks into the Blockchain checkout's installed `node_modules` (read-only). If develop moves, re-pin `TIP` and re-check out the clone. If the session scratchpad is cleaned, the source is gone.

**Round counter:** 0 rows in `night/done.md`, no `READY_KS-1369*`, no earlier brief (control: KS-908 shows 3 rows and 2 READY files). This is round 1, with one rebrief allowed; after that it goes to the cloud.

**Collision:** 21 live PR merge refs at 09:08 AEST. Those heads plus every head #1320-#1338 (39 in all) were fetched and diffed against their merge-base. None touches this product file or a same-name test. The only wallet-connector hit is #649, on `package.json`.

**Scope:** Refs KS-1369 (ruled option (a)). A load re-run is owed before Done.

## UNMEASURED / doubts for Wednesday
1. **No Spark model round** was run. Both checkers were run on the golden only.
2. **No live stack.** It is a runtime change, and a §5f sweep is owed after merge.
3. No load run: the KS-1354 k6 `auth-spike` crash (13 restarts) was not reproduced, and a throw from elsewhere in the proxy chain under load is not excluded.
4. The client-visible result of an early return (headers already sent, no error answer added) was not measured. The ruled option (a) adds no 502 path.
5. `proxyReq.destroyed` is not checked. The ruling names `headersSent` only.
6. **Open PRs come from `ls-remote`** plus fetched heads, not the GitHub files API. A PR opened after 09:08 would be missed.
