# QA Gate 120 verdict: Secuura/Distributed_Secuura PR 1938 (Refs KS-1725: zod 4 prep on zod 3, ZodError .errors -> .issues, z.record key schema), TIER 2 proposed

## BLUF
**GO WITH NOTES, TIER 2 HOLDS. Nothing has to be fixed before merge.**
- **`.issues` is the same array as `.errors` on zod 3.** zod 3.25.76 `v3/ZodError.js:25-27`: `get errors() { return this.issues; }`. I measured identity (`r.error.errors === r.error.issues` is true, also after `addIssue`). Every one of the 26 standalone locks plus the root lock resolves exactly 3.25.76 (logs/zod_lock_versions.log), one copy in the root tree.
- **No response body changes.** I ran the REAL auth, referral and shared `errorHandler` functions on ordinary ZodErrors, base vs head: 45 rows, **byte-identical**. No response key is renamed anywhere (every `+` line keeps the key `details`; zero `issues:` keys added).
- **No accepted/rejected set changes.** 38 input cells x 2 value schemas for `z.record(V)` vs `z.record(z.string(), V)`: 0 diffs; the key schema object is the same `ZodString` in both.
- **Auth path: the response is identical, so Tier 2 holds** (reasoned below, measured by the driver).
- **Re-measure:** tsc equal base vs head (0 at every unit; auth 42 = 42, identical set); suites equal except load flakes; merge-tree clean; docs-fragments OK with a red planted control.
- Two things the author should word differently (G120-F1, F2): the survivors in the unit suites, and four `z.record(z.unknown())` one-arg sites in security that the PR leaves and does not name.

## Heads
- START (logs/head_start.log, 09:41:05Z): PR head `6b5960b6bb0e4705b650a0a993926e3fa1ce0911` (matches), develop `777643aa6e1a29ebe121e4809fb3b16eedf5e552` (matches).
- END (logs/head_end.log, 10:16:37Z): PR head **unchanged**. Develop moved to `0e3a9b65` (one commit, "Refs KS-1081: env.example ..."), not the PR. Merge-tree re-run on both (Q6).
- Merge-base `8f313815f415` (matches). One commit. Diffstat (logs/diffstat.log): **34 files, +121/-103**, as claimed. 32 product/test .ts files + 2 docs fragments (Projects Documents/fragments/{cheat,flow}). Nothing outside the declared paths.
- PR body not read (no PAT in this session); I used the author's READY mail (evidence/s13_ready_pr1938.txt).
- Node v26.8.1, npm 11.19.0, vitest 4.1.12. **Nothing was measured on Node 24.**

## FINDINGS
- **G120-F1 (INFO / recommended for the PR body; measured)** Suite pins. Product-only mutants at head (tests untouched, sha256 restore asserted each time; scripts/mutants.sh, mutants_full.sh):
  - Pinned: the KS-1410 C3 cell (source-text count of `details: err.issues`) goes red when ONE tenant-provisioning site is reverted (M1: 1 failed / 5 passed) and when all three are (M2). A `.issuez` typo in auth's errorHandler turns 17 auth cells red (F5). A typo in security `requestRefusal.ts` turns 9 of 10 red (M7).
  - **Survivors (no test goes red):** (a) a typo in `packages/shared/src/errors/index.ts` (`err.issuez`): whole shared suite shows only the same 3 unrelated reds (threadToken timeout, wallet-signature KS-1727, ks879 load); the shared errorHandler ZodError branch has no test in its own package. (b) Reverting any rename to `.errors` (M4, M6, M8) survives: expected, they are equivalent on zod 3, so only the zod 4 bump can pin them. (c) `z.record` key narrowed to `z.number()` in analytics filters, or to a literal in nft customMetadata: whole analytics (108/108) and nft-certificate (162/162) suites stay green. No test sends a record value with string keys through those schemas. My input table (Q2) is what pins "no change", not the repo.
  - Class: not blocking, because on zod 3 the change is a no-op by construction; the survivors mean a LATER wrong edit to these lines would not be caught.
- **G120-F2 (INFO / recommended; measured by type-check on zod 4.6.7)** Completeness. The 17 held `.errors` sites are exactly: anchoring `src/index.ts` 602, 900, 935, 1349 (4); auth `src/routes/oauth.ts` 1217, 1325 (2); governance `src/routes/governance.ts` 52, 133, 326, 407 (4); security `src/index.ts` 836, 969, 1454, 1639, 1840, 2067, 2086 (7). `git grep` for `.errors` at head (positive control: 166 hits at base, 84 at head) finds no other `.errors` on a ZodError in product code; the rest are unrelated (`result.errors` of verifiers, `findings.errors` in Playwright specs, `api.errors` counters).
  - On zod 4 (zod mapped to a scratch 4.6.7, each unit's own tsconfig): the anchoring (4), auth (2) and security (7) sites fail with TS2339. **Governance's 4 sites do NOT fail to compile** (`catch (error: any)`), so they are runtime-only breaks on zod 4 (`error.errors` is undefined); the author's "compile errors" metric would not show them.
  - **Four sites the PR neither converts nor lists:** `services/security/src/index.ts:651, 652, 653, 664` are still one-argument `z.record(z.unknown())` and fail on zod 4 with TS2554 (Expected 2-3 arguments). Probably held for the in-flight security KS-1868 PRs, same as the 7 `.errors` there; name them. Other zod 4 errors in my mapping (analytics.openapi x3, billing stripe.config x1 TS2769, shared validation.ts:187 TS2769) are zod 4 API changes outside this PR's scope (my total 22 vs the author's 19 differs by my mapping method and the 4 TS2554, so I do not confirm "19" exactly).
  - Four existing test files still read `zerr.errors` on a ZodError they build (analytics ks1868 p1-p3, tenant-provisioning ks1868 precheck) and ks976a reads `err.error.errors[0]` (a response-body field; check). They come from other KS-1868 PRs; they will fail at the bump.
- **G120-F3 (INFO, measured)** Auth is an identity surface, but the diff there is only `err.errors` -> `err.issues` in two places in `services/auth/src/middleware/errorHandler.ts` (the first-issue message and `details`). The driver ran the real auth handler on 6 ordinary ZodErrors: status 400, `{success:false,error:{code:'VALIDATION_ERROR',message:'email: Required',details:[...]}}`, **byte-identical base vs head**, and a plain Error stays 500/INTERNAL_ERROR. See Q3.
- **G120-F4 (INFO, measured)** Suite flakes, not effects of the PR: head showed `threadToken` (52 s timeout) and two `ks949-platform-admin-seed-identity` cells (5.0 s timeout) red in the full run. Re-run alone at head: ks949 31/31, threadToken pass. At base ks949 times out alone (rc 1, 5004/5002 ms). Same KS-1155 load class the author names.
- **G120-F5 (INFO)** `validateInput` in services/shared returns a result field also called `errors: z.ZodError` (validation.ts:398). It is a result key, not a ZodError property, so correctly untouched.
- **G120-F6 (INFO)** `validateBody/Query/Params` were run in the driver, but my mock chain produced no `next(err)` (status 0 / null rows are equal base vs head and therefore carry no evidence). Their three renames are covered only by the type/identity argument and by the shared suite (1151-1152/1153 at both ends).

## Q1. `.issues` vs `.errors` on zod 3; response bodies
- Source: node_modules/zod/v3/ZodError.js line 25-27 (above). `scripts/zodtable.cjs`, logs/zodtable.log: same array, JSON equal, equal after `addIssue`, multi-issue nested object equal (3 issues).
- Only `zod` 3.25.76 exists in the root tree; 26 standalone locks all 3.25.76 (logs/zod_lock_versions.log). Package.json ranges are ^3.22+, where `.issues` also exists.
- Receiver check (scripts/guards.py, logs/guards.log): 81 renamed product reads; the only two without a guard on the preceding lines are m365-integration `index.ts:1301, :1653`, and both are `if (error instanceof z.ZodError)` on the line above (read). Every other site is `instanceof ZodError`, `.safeParse` failure or a `error.name === 'ZodError'` check.
- Run, not read: scripts/driver.sh + repo/Blockchain/Dev/_g120_driver.ts, real `errorHandler` of auth, referral and packages/shared, plus `bodyRefusalMessage`, on 6 invalid inputs: logs/driver_base.json vs driver_head.json, 45 rows, equal (logs/driver_cmp.txt). Response body shape, ordering of issues and the `details` key are unchanged. The two files differ only in log timestamps in stdout.
- Response key names: zero. All 71 removed `details: x.errors` lines come back as `details: x.issues`; the JSON key is `details` throughout. **No consumer-visible API change.**
- Not run (read only): the ~60 inline `res.status(400).json({... details: error.issues})` sites in route files. They are the same expression on the same getter.

## Q2. `z.record` key schema (scripts/zodtable.cjs; logs/zodtable.log)
| value schema | inputs | cells | diffs |
|---|---|---|---|
| z.string() | {}, {a:'x'}, {a:1}, {'1':'x'}, {'':'x'}, "__proto__" key, inherited key, [], ['x'], null, 's', 42, undefined, Map, null-prototype object, {a:undefined}, symbol key, Date | 19 | 0 |
| z.unknown() | same | 19 | 0 |
- Both parse and error payloads compared (success flag, data, issues). The key schema is `z.string()` in both: `z.record(V)` in zod 3 builds `ZodRecord` with a `ZodString` key type (printed: ZodString both). 22 `z.record` conversions (one-argument -> `(z.string(), V)`), every one with `z.string()` as key, none stricter, none numeric.
- Note for zod 4 (not this PR): `z.record(z.string(), V)` is accepted in 4; only the later bump changes record semantics.

## Q3. TIER
- **TIER 2 holds.** The auth change is one getter spelling in `services/auth/src/middleware/errorHandler.ts` (two reads: `firstError` and `details`). On zod 3 the getter returns the same array, and I ran the real handler: HTTP status, `code`, `message` and `details` are byte-identical for ZodErrors, and a plain Error still gets 500 INTERNAL_ERROR. No auth response shape changes, no auth control flow changes, no new log line. The auth suite 1469-1471 at head vs 1470/1471 at base differs only by the two ks949 timeouts that pass alone (F4).
- It would be TIER 1 if any response field name changed on an auth path, or if the bump had moved with it. Neither is true here.

## Q4. Completeness: see G120-F2. Positive control: `git grep -e '\.errors[^A-Za-z0-9_]'` gives 166 at base and 84 at head (the 82-hit drop is the PR's `.errors` reads plus nothing else; remaining 84 are the 17 held, tests, and unrelated names). Note: `-E '\b'` returns 0 on this host's git; I used the bracket form after the first run returned a false zero at BOTH refs.

## Q5. Re-measure (scripts/measure.sh, rerun.sh; logs/head, logs/base)
| | base 8f313815 | head 6b5960b6 |
|---|---|---|
| tsc per touched unit (18 units; test config where one exists) | 0 each; auth 42 | 0 each; auth 42 (sorted error sets identical, test-config pre-existing) |
| vitest, 15 vitest units | 5208/5209 (KS-1727 red) | 5205/5209: KS-1727 + 3 load timeouts (threadToken, ks949 x2), which pass alone at head (F4) |
| jest governance / originate | 194/194, 2163/2163 | 194/194, 2163/2163 |
- Different unit set from the author's 7571/7577 -> 7576/7577 (I did not run the 3 units without a vitest config under vitest; I ran governance/originate under jest); same direction: head is not worse than base.
- Mutants: see G120-F1 (M1, M2, M7, F5 red; M3/F3, M4, M6, M8, M9/F9, M10/F10 survive, all `RESTORE_OK`).
- Docs fragments (scripts/docs.sh): `docs-fragments check` OK at head (rc 0); with an unbalanced `<table>` planted in the new cheat fragment: rc 1, "tags are not balanced"; restored by git checkout, rc 0.

## Q6. merge-tree (scripts/mergetree.sh, mt2.sh; logs/merge_tree*.log)
- onto 777643aa: clean (rc 0), resulting tree changes exactly the PR's 34 paths; 0 of the 34 changed on develop since the base.
- onto 0e3a9b65 (develop at END): clean, same 34 paths, 0 overlap.

## Q7. ks1346 logging rule: no log line added or changed. The PR touches no logger call. (auth handler logs `err.message`/stack before the branch; unchanged.)

## Notes for the PR body
1. G120-F2: name the four `z.record(z.unknown())` sites left in `services/security/src/index.ts` (651, 652, 653, 664) with the 17 held `.errors` sites; say governance's 4 held sites are `error: any` and will not show as compile errors. Recommended.
2. G120-F1: say that no test pins the record-key conversion (analytics, nft-certificate suites stay green if the key schema is narrowed) and that the shared errorHandler ZodError branch has no test in packages/shared; the evidence for "no change" is the zod 3 getter plus the input table. Recommended.
3. G120-F4: ks949 / threadToken timeouts are load, not effects. Info.
No FIX-BEFORE-MERGE item.

## NOT TESTED
- Node 24 (host is v26.8.1). zod 4 suites (zod does not move); I only type-checked against a scratch 4.6.7 via path mapping (my method differs from the author's scratch tree).
- A real service boot or HTTP request; the gateway hop; the ~60 inline route sites were not each run (same getter).
- The `validate*` middlewares through the driver (F6).
- vitest of the 3 units without a vitest config (services/shared has 2 test files); frontends; api-gateway; the four platform suites; pre-push hook legs; PR body.
- The 5 non-touched zod units tsc (the author's "26 units") beyond the 18 touched ones.

Artefacts: scripts/, logs/, evidence/, zod4/ (scratch zod 4.6.7). Clone repo/ left at head 6b5960b6 with one untracked scratch file (_g120_driver.ts), push URL disabled. No background process of mine is running (all runs were foreground or have exited; I checked `ps`). Every test runner was anchored with --root / --rootDir to my own clone; nothing was written to Wednesday's tree beyond this workdir.
