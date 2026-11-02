# QA Gate 135 verdict: Secuura/Distributed_Secuura PR 1953 (Refs KS-1725: zod 3 -> zod 4.6.7 behind a zod 3 issue layer; GHSA-mrhx-c7xc-m3w5 row removed), TIER 1

## BLUF
**NO GO, one small fix round. Four classes of 400 body still differ from develop for the same invalid input, and none of them is an accepted tightening.** Three are fixed in `packages/shared/src/validation/zod3-compat.ts`; the fourth needs a helper at 9 `z.nativeEnum` request sites. I applied the three compat fixes in-process (the repo was not edited), and the product residual over the whole corpus then drops to the accepted classes plus one class that comes from the advisory fix itself (F5).
- **Acceptance is held.** No INVALID input is now accepted (0 REJ->ACC cells in product code). The only VALID inputs now refused are the two listed tightenings: safe-int (22 cells) and coerce Infinity (9 cells). `.guid()` and `zod3Datetime` keep zod 3's acceptance on every product cell. Status codes are unchanged except on those two tightenings.
- **Body differences that are not accepted** (measured on base vs head, real schemas, real serializer; also run through the real shared `validateBody` -> `errorHandler`):
  - F1: `zod3Datetime({message})` puts its message on the TYPE issue. `received` is dropped, and a missing, null or number date reads "Invalid RFC 3339 date-time" where it read "Required" / "Expected string, received null".
  - F2: zod 4 still runs `.min/.max/.length` after a type failure, so the body carries an EXTRA issue (an array into a string with a length check, or a string into an array with one).
  - F3: when an array breaks `.min` and also has bad elements, the array's own issue now comes after its elements' issues.
  - F4: `z.nativeEnum` given a number now answers `invalid_type` where it answered `invalid_enum_value`.
- **Everything else holds.** the author's compat cells (golden set included) re-run green, 217/217, governance 6/6, 270/270 governance suite, 18 units' tsc 0 errors, every other suite as the author reports. Audit: the head passes, and base's zod 3 locks FAIL against head's baseline (control). 46/46 tracked lockfiles hold 31 zod entries, all 4.6.7. The only other packages that moved are zod-to-openapi, openapi3-ts and yaml, all three declared. merge-tree is clean.
- **Fuse:** merging this PR makes the 2026-11-09 zod fuse moot. The row is gone, and no lock resolves zod below 4.6.6. Without the merge, develop's `audit:gate` goes red on 2026-11-09 00:00Z. The fix round is about a day of work, so it fits.

## Heads
- START (logs/head_start.log, 2026-11-02T15:26:02Z): PR head `ea6d924eb5de309482cbb586d97285fc4851fbdb` (matches), develop `8150eeb3802bd9cfe5242ffbc49278c1a3739a84` (matches).
- END (logs/head_end.log, 15:48:41Z): both **unchanged**.
- Merge-base = develop (`8150eeb3802b`); develop is already merged into the branch. The PR body was read from the author's drafted file (evidence/pr3_body_author_copy.md, the author says it is byte-equal to the live body; I did not read the live body: no PAT).
- Node v26.8.1, npm 11.19.0. **Nothing was measured on Node 24.**

## FINDINGS
- **G135-F1 (FIX-BEFORE-MERGE; measured)** `zod3Datetime(options)` passes `{ error: options.message }` to `z.stringFormat`. On zod 4 a schema-level error applies to the invalid_type issue too, and it skips the global map, so `received` is never set. zod 3's `.datetime({message})` put the message on the format issue only.
  - Evidence: logs/f1_datetime_message.log, 6 of 11 inputs differ: missing, null, 5, true, [], {}. For example, null: zod 3 `{"code":"invalid_type","expected":"string","received":"null",...,"message":"Expected string, received null"}`, head `{"code":"invalid_type","expected":"string",...,"message":"Invalid RFC 3339 date-time"}`.
  - Run through the real shared `validateBody` + `errorHandler` (logs/driver_cmp.txt): 422 and 400 bodies differ.
  - Corpus: 870 product cells.
  - Live sites:
    - `isoDateTimeSchema`: analytics `types/analytics.types.ts:429,430,467,468,487,488`, prism `index.ts:350`, security `index.ts:714`, transfer `index.ts:380`, `routes/delegations.ts:37,38`, and shared `validation/index.ts:165,166`;
    - `ISODateSchema` / `FutureDateSchema` in services/shared, which no service imports.
  - **Exact fix:** in `zod3-compat.ts:332`, replace `{ error: options.message }` with `{ error: (iss) => (iss.code === 'invalid_format' ? options.message : undefined) }`. A function that returns undefined falls through to the global map.
    - Verified: 6 differences become 0 (probe3), and the whole corpus F1 class becomes 0.
    - Add golden cases (missing / null / number into a datetime that carries a message).
- **G135-F2 (FIX-BEFORE-MERGE; measured)** zod 4.6.7's length checks carry a default `when: _whenHasLength` (zod `v4/core/checks.js:16`, `schemas.js:40-45`). So they run after an aborted invalid_type whenever the input has a `.length`.
  - The result is an EXTRA issue, for example `z.string().min(8)` given `[]`: zod 3 sends one invalid_type; head sends invalid_type + `{"code":"too_small","minimum":8,"type":"array",...}`. An array schema with `.min` given a string adds a `type:"string"` too_small.
  - 526 product cells. Examples: packages/shared `passwordSchema`, anchoring `index.ts`, auth `routes/mfa.ts`, `routes/users.ts`, referral `routes/referrals.ts`, tokenisation `index.ts`, governance `types/governance.types.ts`, services/shared.
  - Real-handler run: logs/driver_cmp.txt `F2_string_into_min_array`. A `.trim()` chain happens to be immune (`F2_array_into_min_string` EQUAL).
  - **Exact fix:** in `zod3Issues`, after mapping, drop every `too_small`/`too_big` whose `path` equals the path of an `invalid_type` issue in the same list whose `expected !== 'integer'` (zod 3 never ran a check after a type failure). Do it inside the recursion so union branches get it too.
  - Verified in-process: F2 class becomes 0 over the corpus (logs/categories_product_fix.log).
- **G135-F3 (FIX-BEFORE-MERGE; measured)** zod 3 reported an array's own `.min`/`.max` issue BEFORE its elements' issues; zod 4 reports it after them.
  - Example: `z.array(z.string().min(3)).min(2)` given `['a']`: zod 3 `[array too_small, ids.0 too_small]`, head reversed (driver_cmp.txt `F3a`, both envelopes).
  - **Exact fix:** in the same `zod3Issues` post-pass, move a `too_small`/`too_big` with `type:"array"` at path P in front of the first issue whose path extends P. Verified in-process.
- **G135-F4 (FIX-BEFORE-MERGE; measured)** zod 3 `z.nativeEnum` accepted a NUMBER into its enum check and answered `invalid_enum_value` (`received: 1`, "Invalid enum value. Expected 'hot' | 'cold', received '1'"). The compat map applies z.enum's rule, which treats a non-string as invalid_type, so head answers `{"expected":"'hot' | 'cold'","received":"number","code":"invalid_type",...}`.
  - Evidence: logs/probe4_unevaluated_constructs.log, and driver_cmp.txt `F4` on both envelopes.
  - Live sites: nft-certificate `routes/nft.routes.ts:34,35,41,55,56,658,659`, vc-issuer `routes/credentials.ts:37,96`.
  - My corpus could not evaluate these from source (an imported enum), which is why the probe was needed.
  - **Exact fix:** zod 4 cannot tell nativeEnum from enum at the issue.
    - Add `zod3NativeEnum(E)` to the compat module: `z.nativeEnum(E, { error: (iss) => { iss.zod3NativeEnum = true; return zod3Annotate(iss); } })`.
    - In `zod3Annotate`'s enum branch, treat a `number` input as `invalid_enum_value` when that flag is set.
    - Use the helper at the 9 sites, and add one golden case per input type.
- **G135-F5 (recommended: list in the PR body for Wednesday's ruling; measured)** An array over its `.max` no longer reports its elements' issues; zod 3 reported the length issue and then every element.
  - Example: 3 bad elements with `.max(2)` gives zod 3 4 issues, head 1.
  - Live: referral `routes/rewards.ts:18` (`rewardIds ... .max(50)`); also mcp-server tools `register.ts:77`, `verify.ts:100` and services/shared; 6 corpus cells.
  - This is the advisory's own fix: its title is "Zod can exhaust memory while validating oversized constrained collections" (logs/audit_gate_base_ctrl.log). It cannot and should not be restored. It is not among the five listed changes, so name it as a sixth.
- **G135-F6 (recommended; measured) Survivor.** No acceptance test pins `.guid()`.
  - M3b: `users.ts:778` reverted to `.uuid()`. The whole auth suite stays green (1536/1536), and so do the 217 compat cells.
  - M3a: all 39 product `.guid(` reverted to `.uuid(`. Compat 217/217 green. The only red is kyc ks629's SOURCE-TEXT control. auth's 1 red was a ks949 5 s timeout, not a kill.
  - The 20-input uuid evidence lives in the author's tools/, not the repo. Add a cell that runs real request schemas (at least `users.ts` PATCH id and one `UUIDSchema`) on the 9 ids zod 3 accepts and zod 4 `.uuid()` refuses.
- **G135-F7 (info / recommended wording)** Inside the listed tightenings, the PR body should also say:
  - (a) safe-int also has a LOWER bound: -2^53 renders `too_small` `minimum: -9007199254740991` (51 product cells).
  - (b) `z.coerce.number().int()` given "Infinity" was already refused. It now answers `not_finite` instead of zod 3's `invalid_type` "Expected integer, received float", and a trailing min/max issue goes away with it (about 39 cells).
- **G135-F8 (info)** Scope. Outside the six declared categories (manifests/locks, issue layer, call sites, tests, regenerated spec, baseline), the PR also changes:
  - `docs/openapi/KS-1725-SPEC-STRUCTURAL-DIFF.md` (+407; a doc beside the bind-mounted spec);
  - the two `Projects Documents/fragments/*/KS-1725-*.html`;
  - `scripts/typecheck-tests/baseline-api-gateway.txt` (the test-type ratchet, 27 -> 25 errors).
  - All are declared in the PR body. Every other product `-`/`+` line is a zod 3 -> 4 rewrite (logs/unexplained_lines.txt: 38 lines, each explained).
- **G135-F9 (info)** Frontends have no layer, by design. Issuer `validateFileUpload`'s enum with its own message now renders `invalid_value`, and the issuer datetime schemas refuse seconds-less input. Both are front-end only, not 400 bodies; the author says the second has no caller.

## Q1. Heads + diffstat (logs/diffstat.log, paths.txt)
146 files, +4062/-515, three-dot vs develop, as claimed. See F8 for the files outside the declared categories. No log line is added anywhere (Q7).

## Q2. The hunks (logs/product_hunks.diff)
- 113 serialiser sites go `x.issues` / `x.errors` -> `zod3Issues(x.issues)` inside unchanged envelopes. The JSON keys, status codes, `code` strings and messages built from `.message` / `.path` are untouched, so a body differs only where `zod3Issues(zod 4)` differs from zod 3 `.issues`.
- 39 product `.uuid(` -> `.guid(`, plus 1 in the frontend.
- 4 datetime sites -> `zod3Datetime`.
- 4 `z.record` two-argument rewrites.
- `acceptTerms` -> `zod3Error`.
- stripe `.default` -> `.prefault`.
- 7 spec-source `pattern` overrides.
- 27 entry imports.

## Q3. Behaviour (REPLACEMENT): 400 bodies, base vs head
**Method (run, not read):**
- `scripts/corpus_side.cjs` parses every product `.ts` file of EACH tree with the TypeScript AST, takes every maximal `z.`-rooted expression, and evaluates it in that tree's own module scope (top-level consts and enums, `@secuura/shared` exports, zod-to-openapi extension) with that tree's zod.
  - Base: zod 3.25.76, raw `.issues`.
  - Head: zod 4.6.7 with the real compat module imported first, then the real `zod3Issues`.
- That gives 953 expressions; 829 were evaluated at both ends and paired by normalised source (`scripts/corpus_cmp.py`, 951 pairs). 122 could not be evaluated: 75 are not schemas (z.ZodError, types); the rest depend on handler-local values.
- The constructs those 122 hide were probed separately (scripts/probe4.cjs: nativeEnum, the MFA union, literal unions, url-or-empty unions, record, strict nesting).
- The inputs are generated from base's schema shape (scripts/corpus_side.cjs `genInputs`): a per-field-valid object, then every field swept over an 82-value palette (types, empties, long strings, email/url/uuid/datetime edge cases, safe-int and Infinity, arrays incl. 60 items, objects), plus all-fields-same and nested objects. That is **294,503 cells**.
- Then the real `packages/shared` middleware `validateBody` -> `errorHandler` (422) and `validation.validateBody` (400) were run base vs head on the finding cases (scripts/driver.cjs, logs/driver_cmp.txt): control EQUAL, F1-F4 DIFF, T1 422 vs passed.
- **No service route was booted.** The envelopes at the 113 sites are unchanged text, so the body equals the envelope plus `details`.

**Results, product code** (logs/categories_product.log; spec-only `*.openapi.ts` and frontend counted separately):

| class | product cells | status |
|---|---|---|
| REJ->ACC (invalid now accepted) | **0** | - |
| ACC->REJ safe-int (tightening 1) | 22 | accepted |
| ACC->REJ coerce Infinity (tightening 2) | 9 | accepted |
| body: int stops the chain (residual 3) | 54 | accepted, pinned |
| body: safe-int bound incl. lower bound | 132 | accepted (F7a wording) |
| body: not_finite on already-refused Infinity | 39 | F7b |
| body: datetime message on type issue | 870 | **F1** |
| body: extra length issue after invalid_type | 526 | **F2** |
| body: array length issue order | probe + driver | **F3** |
| body: nativeEnum number | probe + driver | **F4** |
| body: over-max array drops element issues | 6 | **F5** (the advisory fix) |

- With F1+F2+F3 applied in-process (`G135_FIX=1`), the residual in product code is ONLY tightenings 1-3 plus F5 (logs/f3_overmax_sites.log: "other residual rows 0").
- uuid / datetime acceptance in product code: 0 differences (`.guid` = zod 3 `.uuid`; `zod3Datetime` = zod 3 `.datetime`).
- Spec-only `*.openapi.ts` schemas keep `.uuid()` / `.datetime()` and differ as designed: they are not runtime (only originate imports a constant from one). Unions, refine/superRefine, strict and record keys: identical (probe2/probe4).

## Q4. Re-measure
- New cells green at head:
  - packages/shared ks1725-zod3-compat 217/217;
  - governance ks1725 6/6;
  - billing 3/3;
  - services/shared 2/2;
  - timestamping 3/3.
- Red-first by assertion:
  - M1 (map not installed): 117/217 red, governance 4/6 red;
  - M5 (governance vote catch back to `error.errors`): governance red.
- tsc `--noEmit` at head: 0 errors in all 18 units run (logs/suites_head/).
- Whole suites at head (logs/suites_head/summary.txt):

| unit | passed / total | note |
|---|---|---|
| packages/shared | 1395/1396 | wallet-signature KS-1727, red at base too (logs/base_wallet_sig.log) |
| governance | 270/270 | |
| anchoring | 759/760 | threadTokenMint, red at base too |
| security | 465/465 | |
| analytics | 108/108 | |
| transfer | 120/120 | |
| referral | 36/36 | |
| nft-certificate | 178/178 | |
| staking | 84/84 | |
| kyc | 79/79 | |
| tenant-provisioning | 117/117 | |
| billing | 368/368 | |
| timestamping | 100/100 | |
| vc-issuer | 714/714 | |
| m365 | 280/280 | |
| prism | 30/30 | |
| demo-service | 97/97 | |
| originate | 2322/2322 | |
| auth | 1536/1536 | under mutant M3b only, see NOT TESTED |

- Docs fragments: `check` rc 0 OK. A planted unbalanced `<table>` in the KS-1725 cheat fragment gives rc 1 naming it; restored sha256-equal, rc 0.

## Q5. Mutants (REPLACEMENT) (scripts/mutants.py; logs/mutants*.json)
Product only, tests untouched. Each mutant is an exact replacement; packages/shared is rebuilt for compat mutants; every file is restored by checkout, sha256 is asserted equal, and git status is clean after each. All 12 runs `RESTORE_OK`.

| mutant | result |
|---|---|
| M1 global map dropped (no install call) | KILLED: compat 117 red, gov 4 red |
| M1b map installed but returns undefined | KILLED: 122 red, gov 4 red |
| M2 datetime helper dropped (zod 4 native `.datetime`) | KILLED: 2 red |
| M3b `users.ts:778` `.guid` -> `.uuid` | **SURVIVED** (compat 217 green, auth 1536/1536) -> F6 |
| M3a all 39 product `.guid` -> `.uuid` | killed only by kyc ks629's source-TEXT control -> F6 |
| M4a serializer too_small key order | KILLED: 25 red, gov 2 |
| M4b invalid_format keeps zod 4 code | KILLED: 22 red, gov 1 |
| M4c union branch paths not prefixed | KILLED: 3 red |
| M4d enum drops `received` | KILLED: 8 red, gov 2 |
| M4e guid validation name leaks | KILLED: 3 red |
| M4f datetime key order | KILLED: 4 red |
| M5 governance catch back to `error.errors` | KILLED: gov 1 red |

The F1-F4 shapes have no cell, by construction: they are the findings.

## Q6. merge-tree (logs/merge_tree.log)
Onto develop `8150eeb3802b`: clean (rc 0). The resulting tree EQUALS the PR head tree and changes exactly the PR's 146 paths. Develop did not move during the gate.

## Q7. AUDIT + LOCKFILES (REPLACEMENT) (scripts/locks.py; logs/locks.log, audit_*.log)
- **Every lockfile, enumerated with `git ls-tree -r`:** 46 at base and head (all `package-lock.json`; no yarn/pnpm/shrinkwrap; none added or removed).
  - Across all 46: **31 `node_modules/zod` entries, every one 4.6.7**, 0 below the fixed 4.6.6.
  - 26 locks changed. 26 manifests declare `zod: ^4.6.7`, and none declares ^3.
- **Resolved-tree diff of every changed lock** (by package path), the only version moves:
  - zod 3.25.76 -> 4.6.7 (26 entries);
  - @asteasolutions/zod-to-openapi 7.3.4 -> 9.1.0 (2);
  - openapi3-ts 4.5.0 -> 4.6.2 (1, root lock);
  - yaml 2.9.0 -> 2.9.1 (1, root lock).
  - 0 entries added, 0 removed. All four are named in the PR body. **No unrelated dependency moved.**
- **Audit gate** (`scripts/audit/audit-gate.mjs`, header read: exit 0 clean, 1 new/lapsed, 2 could not run, 3 malformed baseline):
  - head: rc 0, "8 distinct advisories reported, 8 baselined";
  - **control:** base's zod 3 tree with head's 8-row baseline via `AUDIT_BASELINE_PATH`: **rc 1**, "9 reported, 8 baselined", naming GHSA-mrhx-c7xc-m3w5 "Zod can exhaust memory while validating oversized constrained collections";
  - base with its own baseline: rc 0 (9/9).
- `audit-locks.mjs`: head rc 0 (44 locks, 6 match / 6 baselined); control base locks + head baseline **rc 1** (7 match, GHSA-mrhx named).
- **Fuse:** the zod row (`expires 2026-11-09`, lapses 00:00Z that day) is deleted, not re-dated, so merging makes that fuse moot. Without the merge, develop's `audit:gate` and `audit:locks` turn red on 2026-11-09.
  - The baseline is keyed by advisory id only, so after the merge any future zod 4 < 4.6.6 in any lock would fail loudly: no residual suppression.
  - The other 8 rows are untouched (diff: -7 lines, one object).

## Q8. Logging (ks1346)
No log line is added or changed in product code (grep of added lines for logger/console: 0). The compat map drops `input` from every issue (the author's sentinel cell; not re-measured beyond the 217 green).

## Notes for the PR body
1. **G135-F1, FIX-BEFORE-MERGE:** `zod3Datetime` error function only on `invalid_format` (exact code above), plus golden cases.
2. **G135-F2, FIX-BEFORE-MERGE:** `zod3Issues` drops a length issue at the same path as a non-integer invalid_type, plus cells for a string-with-min given `[]` and an array-with-min given a string.
3. **G135-F3, FIX-BEFORE-MERGE:** `zod3Issues` puts an array's length issue before its elements' issues, plus a cell.
4. **G135-F4, FIX-BEFORE-MERGE:** a `zod3NativeEnum` helper at the 9 `z.nativeEnum` request sites, plus a cell with a number input.
5. **G135-F5, recommended:** list "an array over its `.max` no longer lists its elements' issues (the advisory's fix)" as a sixth change, for Wednesday's ruling.
6. **G135-F6, recommended:** an acceptance cell for `.guid` on the 9 zod-3-only ids through real request schemas.
7. **G135-F7, recommended wording:** the lower safe-int bound; Infinity into `.int()` now `not_finite`.
8. G135-F8, F9: info.

## NOT TESTED
- Node 24 (the host has v26.8.1 only).
- A booted service, a real HTTP route through express/nginx/gateway. Bodies were measured from real schemas + the real serializer, plus the real shared middleware/errorHandler.
- 122 expressions not evaluable from source; their constructs were probed by hand (probe4), not the exact schemas.
- auth's whole suite at clean head; it ran only under mutants M3b (1536/1536) and M3a.
- Whole suites at base, other than the two red-at-both cells. The author's per-test base comparison was not re-run.
- The units not listed in Q4: api-gateway, guardian, queue, tokenisation, wallet-connector, mcp-server, services/shared whole, frontend/issuer.
- Image builds, the four platform suites, the pre-push hook, `generate-openapi --check` (not re-run), the PR body as live on GitHub.
- The F2/F3 fixes were verified only as an in-process patch over the corpus; F4's fix is specified, not run.

Artefacts:
- scripts/, logs/, evidence/ (READY mail, author body copy, head baseline copy).
- Clone repo/ at head `ea6d924e`, clean, push URL disabled; worktree repo_base/ at develop `8150eeb3`, clean.
- No background process of mine is running: the install runs and the suites run exited, and I checked `ps`.
- Every test runner was anchored with `npm --prefix` / `--root` to my clone. Nothing was written outside this workdir.
