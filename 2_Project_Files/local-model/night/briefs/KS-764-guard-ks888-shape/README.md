# KS-764 guard, KS-888 shape: Spark brief + golden (TEST-ONLY: the product is Kam-ruled and correct; the guard's pattern is stale)

Written 00:39 AEST 2026-09-29 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and the state of PRs #799, #1322 and #1327 were only READ, by `build_input.sh` and one read-only GraphQL query for KS-764), mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran under `scratchpad/bw764/`, a `cp -a` copy of `bw0929/base`. The original was not written.

## The finding, plainly
**develop is red in `packages/shared`: 1 failed / 945** (measured, `db8d85dcd` and `3d706c21f`). The failing cell is `CALL_SITES matches every revoke surface written in the TWO KNOWN IDIOMS` in `ks764-key-revoke-call-site-guard.test.ts`. It fails at its per-site loop (`:290`-`:293`), by assertion: `services/security/src/index.ts` no longer matches `/isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(/`.
- #1327 (KS-888 revoke) put five `//` comment lines and `try {` between `:1286` `apiKey.isActive = false;` and `:1293` `await dbSaveApiKey(apiKey, { rethrow: true });`. That is about 600 characters, and the window allows 80.
- The sweep equality in the same cell still passed at the tip. It finds `security/index.ts` through the OTHER pattern: the rotate's `UPDATE svc_api_keys SET is_active = false` at `:273`. So the route's own pattern is only checked by the per-site loop. That is pre-existing (see doubt 4).

## The fix (test-only, 2 edit points, one file)
Both copies of the pattern (`:77` and `:97`) become:
```
/isActive[^!-~]*=[^!-~]*false;(?:[^!-~]*^[ ]*[/][/].*)*[^!-~]*^[ ]*(?:try[^!-~]*[{][^!-~]*^[ ]*)?await[ ]+dbSaveApiKey[(]/m
```
Seven comment lines go above `:77` to explain it.
- **What it allows:** between the flip and the save, ONLY whitespace, whole `//` comment lines and one optional `try {`. The save must start its own line (`^` with the `m` flag).
- **Why no backslashes:** the pattern uses character classes (`[^!-~]` means whitespace here; `[/]`, `[{]` and `[(]` are those literal characters). On 2026-09-16 the KS-887 model doubled a backslash in a `+` regex line and lost a round. Every brief since keeps `+` lines backslash-free.
- **Why not a wider window:** `[\s\S]{0,2000}` goes GREEN with the save deleted. It then spans from the rotate loop's `k.isActive = false;` (`:258`) to `async function dbSaveApiKey(` (`:292`). Measured, below.

## Files
- `KS-888.md` is the brief (13,784 chars). It is named for **KS-888, not KS-764** (see "Ticket id").
- `KS-888.golden.diff` is the golden, sha256 `34f81565ed60…`: 1 file, 2 hunks (`@@ -76,3 +76,10 @@`, `@@ -96,3 +103,3 @@`), 9 `+` lines and 2 `-` lines.
- **Fence rebuild:** IDENTICAL to the golden (`cmp`). Mutated control (the final `/m,` changed to `/,`): DIFFER.
- **Char lint of `+` lines:** 0 contain a backslash, a backtick or a double quote (control: a planted backslash line counted 1). 0 non-ASCII lines. 0 blank context lines.
- **The `-` lines (2) and one context line DO carry backslashes.** They are the tip's text, so this cannot be avoided. The brief says to copy each backslash once. See doubt 1.

## Ticket id
**KS-764 is Done and ARCHIVED** (2026-09-14, PR #799 merged). `build_input.sh KS-764` refused it, verbatim: `build_input: REFUSED KS-764 — archived at 2026-09-14T02:01:53.326Z`.

No other ticket names the guard. A Linear search for `ks764-key-revoke-call-site-guard` found only KS-1155, which is about timing.

So I named the brief for **KS-888**:
- It is the ticket whose ruled change (#1327) caused the red.
- It is In Progress, and #1322 and #1327 are both merged.
- The build therefore carries `started_ok=`.

The folder keeps the requested name `KS-764-guard-ks888-shape/`. If you would rather file a new ticket, rename `KS-888.md` and `KS-888.golden.diff` to it and drop `started_ok=`.

## The tamper, and why it is not on the revoke
The builder admits a `test_file=` only under the PRODUCT's own package (`build_input.sh:408`). The checker plants a tamper as a ONE-line replacement in the product file. So a guard in `packages/shared` cannot have its tamper in `services/security/src/index.ts`. Also, the new pattern needs the save on its own line, and no single-line tamper can express that.

The builder tamper is therefore `packages/shared/src/security/keyRevokePolicy.ts:17`:
- It is a doc-comment line, byte-unique (`grep -c -F -x` = 1).
- The tamper makes it contain `UPDATE svc_api_keys SET is_active = false`, which puts a revoke write in the allowlisted policy module.
- Result: 2 failed / 15, both by assertion. The red cells are `CALL_SITES matches every revoke surface` (found 3 vs 2) and `every allowlisted non-revoke really is present`.

The grip on the REAL revoke was proved by the arms below. It was not proved by the checker.

## Measured (scratch copy at `db8d85dcd`, tree `6840bc5026da`; re-measured at `3d706c21f`, tree `49211e66ba23`; `Blockchain/Dev` subtree `31f29a587038` is IDENTICAL at both; vitest 4.1.10, node 24.7.0; `packages/shared` rebuilt, porcelain 0)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0; applied result `cmp`-identical to the measured file |
| the guard file at the untouched tip (RED) | **1 failed / 15**, the CALL_SITES cell, by ASSERTION (`toMatch`), 0 Unhandled |
| with the golden (GREEN) | **15 / 15**, 0 Unhandled |
| `packages/shared` suite | tip **48 files, 1 failed / 945**; golden **48 files, 945 / 945** (at both tips) |
| sweep with the new pattern (470 non-test files) | finds `services/security/src/index.ts` only; the UPDATE pattern finds originate `adminConfig.ts` + security. **Nothing new.** The other `isActive = false;` files (auth `session.ts`, m365 `index.ts`, referral `referralService.ts`) do not match. The probe and drift cells stay green. |
| new pattern over `index.ts` at 4 commits | `63db8a383` (pre-#1327) MATCH; `ea816de19`, `0d156d12c`, `db8d85dcd` MATCH at `:1286`. The old pattern matches only at `63db8a383`, which confirms Wednesday's finding. |
| tsc (temp tsconfig including the test file) | rc 0 at the tip and with the fix. Control: planted `const bw764plant: number = 'x'` gave rc 2 (TS2322). `tsc -p packages/shared --noEmit` rc 0. |
| eslint (from `Blockchain/Dev`) on the test file | rc 0 at the tip and with the fix. Control: planted `var` + `debugger` gave rc 1 (no-var, no-debugger). |
| **the real Spark checker on the golden as model output** (`prepare_clone.sh` then `spark_checker.sh`, clone at `3d706c21f`) | **SPARK RESULT: PASS**, A1-A7 PASS in test-only mode. A4: under the tamper, 2 failed / 15 by assertion, controls green. A5: 15 / 15. A6: suite 945 with 1 failed before and 0 failed after. A7: tsc rc 0. A2a: anchors 2/2. This ran on the 13,570-char build of the brief. The final brief differs only by one added "re-measured" premise line, and it was rebuilt rc 0. |

**Arms.** Each arm changed one thing in `services/security/src/index.ts` in the scratch copy and ran the FIXED guard file. The tip was restored and `cmp`-checked after.

| arm | new pattern | loose `[\s\S]{0,2000}` in both places |
|---|---|---|
| untouched tip | 15 / 15 green | 15 / 15 green |
| flip moved after the save | **1 failed / 15** (CALL_SITES, assertion) | **15 / 15 GREEN** |
| save deleted | **1 failed / 15** | **15 / 15 GREEN** |
| save replaced by `memApiKeys.set(apiKey.id, apiKey);` (never stored) | **1 failed / 15** | not run |
| save commented out (`// await dbSaveApiKey(...)`) | **1 failed / 15** | not run |
| unrelated statement between (`apiKey.isActive = !decision.allow;`) | **1 failed / 15** | **15 / 15 GREEN** |
| early `return` between the flip and the save | **1 failed / 15** | not run |
| builder tamper (`keyRevokePolicy.ts:17`) | 2 failed / 15 (both declared cells) | not run |

0 Unhandled in every arm. With the old pattern at the tip, the builder tamper also gives 2 failed / 15.

## build_input: rc 0
```
NIGHT_EXCERPT_TRIGGER_BYTES=60000 NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw764/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-888 <out>/input.json product=Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts ref=Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts test_file=Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts line=17 ctx=65536 started_ok=revoke-1327-merged_ks764-guard-test-only-carved-2026-09-29
```
Output, verbatim:
```
ticket KS-888 · In Progress (started) · Medium · assignee=kamil.kreiser@secuura.ai · updated 2026-09-28T12:37:49.971Z
attached PR #1327 (Secuura/Distributed_Secuura): merged
attached PR #1322 (Secuura/Distributed_Secuura): merged
WARN state is In Progress (started) — ADMITTED by started_ok: revoke-1327-merged_ks764-guard-test-only-carved-2026-09-29
product file PINNED: packages/shared/src/security/keyRevokePolicy.ts (ticket names 1: ['services/security/src/index.ts'])
fix shape: WEDNESDAY BRIEF (KS-888.md) — the ticket's fix-shape/decision gates are bypassed; the brief states the change and any decision → 'The exact change'
product packages/shared/src/security/keyRevokePolicy.ts (12157 B, 247 lines) defect line 17 [pinned (line=)]: '* PURE BY CONSTRUCTION: no database, no request, no clock, no environment. The'
reference test PINNED: Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts
test_file PINNED (modify in place): Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts (21258 B) — suggested_test_file = it
  named sites: no '## Where' section — checklist empty (A3b passes vacuously)
  expected '+' lines from the brief's edit blocks: 9 (A3c)
  red cells declared by the brief: 2 ['CALL_SITES matches every revoke surface', 'every allowlisted non-revoke really is present']
  TEST-ONLY tamper from the brief: packages/shared/src/security/keyRevokePolicy.ts:17 '* PURE BY CONSTRUCTION: no database, no request, no clock, n' -> '* PURE BY CONSTRUCTION: UPDATE svc_api_keys SET is_active = '
  prompt source: WEDNESDAY BRIEF /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape/KS-888.md (13784 chars) — the ticket description is NOT the prompt
  suggested_test_file = the brief's `## The test` File: line Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts (== the title slug)
contract: key set == KS-871 input (top-level, ticket, repo)
wrote /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw764/bi_888/input.json (58160 B; ~14560 prompt tokens at 4 B/token — num_ctx 65536 leaves ~50976 for the answer)
```

The builder was refused twice before this rc 0:
1. **G6 tip.** develop had moved to `3d706c21f` (#1331, KS-1365, docs only: 4 files, none under `Blockchain/Dev`), and that commit was not in the object store. I fetched `origin develop` into the SCRATCH copy only. The `Blockchain/Dev` subtree hash is the same at both commits (`31f29a587038`), so I moved the scratch base to `3d706c21f`, rebuilt `packages/shared` and re-measured.
2. **KS-764 archived** (above).

## The round command (NOT run)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw764/round_db8d85dc.sh KS-764-GUARD-KS888-SHAPE KS-888 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-764-guard-ks888-shape 60000 product=Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts ref=Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts test_file=Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts line=17 ctx=65536 started_ok=revoke-1327-merged_ks764-guard-test-only-carved-2026-09-29
```
- `round_db8d85dc.sh` is a copy of `bw0929/round_0d156d12.sh` with ONLY SP, SRC and TIP changed; `diff` shows 4 lines per side, the header note included.
- **TIP is `3d706c21f…`, not `db8d85dcd`.** `prepare_clone.sh` refuses when the clone HEAD differs from the input's tip, and the input's tip is origin develop. The file keeps the `db8d85dc` name, and its header says why.
- If develop moves again before the round, both the base and TIP need moving. The script stops on a HEAD mismatch.
- The run folder name in the script still carries the date `2026-09-28` (unchanged, as instructed).

**Round counter:** this is the first brief for this red. One rebrief is allowed, then it goes to the cloud.

## UNMEASURED / doubts for Wednesday
1. **Backslashes the model must COPY.** There are 2 `-` lines and 1 context line (Edit 2's `:96`), each with 4-6 backslashes. The KS-887 failure was a doubled backslash in a `+` line. A doubled one in a `-` line fails A2 strict and lenient apply, and `reanchor.py` keys on `-` lines. This cannot be avoided: those are the lines being replaced. The brief says to copy each backslash once. If it fails this way, the cheapest fallback is a Claude seat. This is not measured on Spark.
2. **The checker's tamper does not exercise the new pattern.** It is proved only by my arms. A3c (9 byte-exact `+` lines) is what stops the model shipping a looser pattern.
3. **`started_ok=` is my assertion.** I could not see the lanes. KS-888 validate has its own brief (`KS-888-validate-logonly`) on a different file (the security `ks888` test), so the two are file-disjoint. Confirm nobody else holds KS-888.
4. **Pre-existing and not fixed:** the sweep equality finds `security/index.ts` through the rotate UPDATE (`:273`), not through the revoke pattern. `REVOKE_WRITES[1]` can therefore stop matching without the equality noticing. Only the per-site loop catches it, and that is exactly what happened here. Worth a card; outside 3 edit points.
5. The pattern is strict by design. A trailing comment on the flip line (`apiKey.isActive = false; // x`) turns it red: measured with node, no match. In the other direction, `[^!-~]` counts any non-ASCII character in the gap as whitespace: reasoned, not tested.
6. Timing: KS-1155 records these tree-walking guards exceeding vitest's 5 s default under fleet load. Here the file ran in under 1 s, unloaded.
7. **File ownership:** Seat B 40th is in `vc-issuer`, `packages/shared/src/vc/verifier.ts` and `api-gateway` `startup-migrations.ts` / `health.ts` / `index.ts`. This brief edits `packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts` and tampers `keyRevokePolicy.ts` in a clone only. The two are disjoint. Note that `startup-migrations.ts` is in this guard's `NON_REVOKE_MENTIONS` allowlist: if Seat B's migration change stops mentioning `svc_api_keys` + `is_active`, the drift cell goes red. That was not measured against Seat B's branch.
