# KS-1244 JOINEDKEY-1 PIN THAT A REPEATED x-api-key (two individually VALID keys, joined by Node into one string) ON A REQUIRED MOUNT IS REFUSED 401 WITH NO PRINCIPAL AND NO BEARER FALL-THROUGH, IN EITHER ORDER — the gateway's own authenticateToken, driven in process — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 01:xx on 2026-09-21, widened sweep round 22 next-best 1)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`
Tip: `778e6cfe2b6061d60ffcf3a57a951c84dc152b67`
Runner: `vitest`

Written from develop `778e6cfe2b6061d60ffcf3a57a951c84dc152b67` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 01:xx on 2026-09-21, read verbs only; the #1104 merge, unchanged since the round-22 search). The test file at that tip is **285 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (**432 lines**, read whole): `apiKeyCache` at `:168` (exported, `:14` of the test file imports it), `validateApiKey` at `:218-252`, `authenticateToken` at `:273-432` (exported, `:12` of the test file imports it), the `x-api-key` read at `:276`, the `sk_` test at `:277`, the validation at `:278`, the REQUIRED-mount refusal at `:279-282`, the KS-1207 comment at `:283-289`, the connector branch at `:290-343`, the Bearer path from `:345`. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `middleware/auth.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1244 reports that a request carrying TWO `x-api-key` headers reaches `authenticateToken` as ONE joined string (Node joins a repeated header's values with `, `), that the joined string fails key validation, and that on an OPTIONAL mount the request then falls through to the anonymous / JWT principal and answers 200. The half that is RIGHT today, and that the ticket's own fix ("reject a repeated key outright ... a refusal rather than a fall-through") keeps, is the REQUIRED mount: at the tip `:276` reads the joined string, `:277` sees it start with `sk_`, `:278` asks the Security Service (which cannot know a joined string), and `:279-282` answers **401** and returns — `next` is never called, `req.user` is never set, and a Bearer sent beside the joined key is never consulted. Nothing in the api-gateway suite drives `authenticateToken` with a joined `x-api-key` today (`git grep -i -E "sk_[a-z0-9_]+, *sk_"` and `git grep -i KS-1244` over `src/__tests__` at the tip: 0 files and 0 files), so the two ways this could silently loosen are unpinned: a future reader that SPLITS the joined value and authenticates its first key (a connector principal from an ambiguous header), or a future guard that lets a joined key skip the refusal and drop to the Bearer path (the KS-1207 shape re-opened). This change adds ONE cell to the `describe('authenticateToken', ...)` block that seeds `apiKeyCache` with two individually VALID keys (`sk_first`, `sk_second`), points the file's own `fetchMock` at a `valid: false` answer for anything else, and for BOTH orders of the joined header (`'sk_first, sk_second'` and `'sk_second, sk_first'`), each beside a valid Bearer test token, calls the REAL `authenticateToken(true)` with the file's own `makeReq` / `makeRes` / `vi.fn()` and asserts, per order, `[joined, next-calls, status, body.success, body.error.code, req.user?.role]` equals `[joined, 0, 401, false, 'UNAUTHORIZED', undefined]`. Every existing cell is unchanged. **It pins TODAY's required-mount refusal and decides nothing about KS-1244's fix** — the refusal MESSAGE (`Invalid API key` today) is deliberately NOT asserted, so a fix that refuses the repeated header earlier with its own message stays green; the OPTIONAL-mount fall-through (the defect itself) is NOT pinned, because pinning it would pin the bug.

## The exact change — ONE hunk in the test file

The new cell goes at the end of the `describe('authenticateToken', ...)` block opened at `:135`, directly above that block's closing line `  });` (`:211`, the ONE trailing context line). There is NO leading context: the line above (`:210`, `    });`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`.**

```
@@ -211,1 +211,16 @@
+    it('RED KS-1244: a repeated x-api-key (two individually valid keys joined by Node) on a required mount is refused 401 with no principal and no Bearer fall-through, in either order', async () => {
+      const meta = { connectorId: 'c-joined', scopes: ['read'], organizationId: 'org1', tenantId: 't1', tenantSlug: 'one', rateLimit: 100, rateLimitWindow: 60 };
+      apiKeyCache.set('sk_first', { result: meta, expiresAt: Date.now() + 60000 });
+      apiKeyCache.set('sk_second', { result: meta, expiresAt: Date.now() + 60000 });
+      fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { valid: false } }) });
+      const outcomes: unknown[] = [];
+      for (const joined of ['sk_first, sk_second', 'sk_second, sk_first']) {
+        const req = makeReq({ headers: { 'x-api-key': joined, authorization: 'Bearer ' + buildTestToken({ sub: 'u-beside', role: 'user' }) } });
+        const res = makeRes();
+        const next = vi.fn();
+        await authenticateToken(true)(req, res as any, next);
+        outcomes.push([joined, next.mock.calls.length, res._status, res._json?.success, res._json?.error?.code, (req as any).user?.role]);
+      }
+      expect(outcomes).toEqual([['sk_first, sk_second', 0, 401, false, 'UNAUTHORIZED', undefined], ['sk_second, sk_first', 0, 401, false, 'UNAUTHORIZED', undefined]]);
+    });
   });
```

`describe`, `it`, `expect` and `vi` are already imported by the file at `:6`, `authenticateToken` and `apiKeyCache` at `:12` and `:14`, and `makeReq` (`:24-32`), `makeRes` (`:34-48`), `buildTestToken` (`:50-53`) and `fetchMock` (`:67-68`, the file's global `fetch` stub) are the file's own helpers — you add NO import and NO helper. The `beforeEach` at `:75-84` already sets `NODE_ENV=test`, clears `apiKeyCache`, resets `fetchMock` and enables test tokens before every cell, so the cell's seeding is local to it. The cell needs no app boot, no port, no real fetch and no database: the middleware is called as a function with the file's fake req/res, exactly as `:136-210` already call it.

## Cells

- `joined` = `RED KS-1244: a repeated x-api-key (two individually valid keys joined by Node) on a required mount is refused 401 with no principal and no Bearer fall-through, in either order`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1244: a repeated x-api-key (two individually valid keys joined by Node) on a required mount is refused 401 with no principal and no Bearer fall-through, in either order

## Tampers

Two single-line tampers on two DIFFERENT lines of `middleware/auth.ts` (`:276` and `:279`; each occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1 each; positive control `x-api-key` matches 3 lines, `:267`, `:276`, `:287`). They are the two shapes a loosening can take: the header read resolving a joined value to its FIRST key (an ambiguous header authenticates a connector), or the required-mount refusal stepping aside for a joined value so the request drops to the Bearer path (the KS-1207 fall-through re-opened for this header). Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (`req.headers['x-api-key']` is `string | string[] | undefined` and `apiKey` is `string | undefined`), so nothing fails to load and no cell reds for the wrong reason.

### SPLITFIRST — the header read takes the first key of a joined value
File: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts`
Line: 276
From:
```
    const apiKey = req.headers['x-api-key'] as string | undefined;
```
To:
```
    const apiKey = (req.headers['x-api-key'] as string | undefined)?.split(',')[0]?.trim();
```
Reds: `joined`

### FALLTHROUGH — the required-mount refusal steps aside for a joined value
File: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts`
Line: 279
From:
```
    if (presentedKey && !meta && required) {
```
To:
```
    if (presentedKey && !meta && required && !String(apiKey).includes(',')) {
```
Reds: `joined`

## Controls

- `rejects with 401 when required=true and no token is present`
- `accepts a valid JWT and populates req.user`
- `validates sk_ prefixed keys via Security Service`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:147`, `:159` and `:218` — each occurs exactly once in the file and none is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; the prefix rule in `build_test_only_input.sh`'s header is for BASH suites only. The other 12 existing cells (`parseTestToken` x6, `skips auth when required=false ...`, `rejects an expired JWT ...`, `assigns defaultTenantId ...`, and the remaining three `validateApiKey` cells) are also green under both tampers but are left undeclared. The `:147` control is the liveness proof for the 401 shape (same `res._status` / `res._json` slots, same `UNAUTHORIZED` code, read through the same fake res); the `:159` control proves the Bearer path — the path FALLTHROUGH would drop into — still works; the `:218` control proves `fetchMock` still feeds `validateApiKey`.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: for `'sk_first, sk_second'`, `:276` reads the whole joined string, `:277` finds it starts with `sk_` (`presentedKey` true), `:278` calls `validateApiKey('sk_first, sk_second')` — a cache MISS (only the two single keys were seeded) — which asks `fetchMock` and is told `valid: false` (`:234-236`, cached null for 30 s), so `meta` is null; `:279` is `presentedKey && !meta && required` = true, `:280` answers `401` with `{ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } }` and `:281` returns. `next` was never called, `req.user` was never set (so `user?.role` is undefined), and the Bearer test token beside the key was never read. The same for `'sk_second, sk_first'`. `outcomes` is `[['sk_first, sk_second', 0, 401, false, 'UNAUTHORIZED', undefined], ['sk_second, sk_first', 0, 401, false, 'UNAUTHORIZED', undefined]]`, exactly what the cell asserts.

Under **SPLITFIRST** `:276` yields `'sk_first'` (then `'sk_second'` for the other order): `validateApiKey` hits the seeded cache and returns `meta`, `:290` is true, `:299` drops the Bearer, `:300-321` build the connector principal (`role: 'connector'`), `:327` asks `getConnectorBearer` (a `connectorBearerCache` miss; `fetchMock` answers with no `data.token`, so null — no real fetch), and `:341` runs the per-key limiter, which counts in memory (no Redis client in a unit run), finds the file's fake res has no `setHeader`, and reaches its own fallback `next()` (`rateLimitEnforce.ts:244-256`) — synchronously, before the middleware returns. Each entry reads `[joined, 1, 0, undefined, undefined, 'connector']` — assertion red. Under **FALLTHROUGH** `:279` is false for a value containing `,`, `:290` is false (no meta), the Bearer path at `:346-357` finds `Bearer test_token_...`, `parseTestToken` (`:118-160`, test tokens enabled, `NODE_ENV=test`) returns the `u-beside` / `user` payload, `:362` sets `req.user`, and `:371` runs the limiter, which passes a non-machine caller straight to `next()` (`rateLimitEnforce.ts:89-91`). Each entry reads `[joined, 1, 0, undefined, undefined, 'user']` — assertion red. Under BOTH, every existing cell stays green: the no-header cells never present a key (`:277` false under both; SPLITFIRST's `undefined?.split` short-circuits to undefined), the JWT cells carry no `x-api-key`, and the `validateApiKey` cells call the function directly, below both tamper lines.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` lines.** `middleware/auth.ts` at `778e6cfe2`, line 276 is `    const apiKey = req.headers['x-api-key'] as string | undefined;` and line 279 is `    if (presentedKey && !meta && required) {`, byte for byte; each occurs **exactly once** in the file (`grep -c -F -x`, 1 and 1). The checker plants and restores them one at a time (T8 by sha256 after each).
- **Premise: the ticket's claim, re-derived.** Node's `http` joins a repeated `x-api-key` into one `, `-separated string (it is not a set-cookie and not one of the discard-duplicate headers), so `:276` sees `'sk_a, sk_b'`. At the tip that string goes to `validateApiKey` whole (`:278`), which the Security Service cannot validate, so `meta` is null; on a REQUIRED mount `:279-282` refuses 401; on an OPTIONAL mount `:279` is false and the request falls to the Bearer path (the ticket's defect — NOT pinned here). `KS-1244` occurs **0** times in `src/__tests__`; no cell in `src/__tests__` sends a joined `sk_` value (`git grep -i -E "sk_[a-z0-9_]+, *sk_"` over `src/__tests__` at the tip: 0 files; positive control: `x-api-key` occurs in 7 test files).
- **Premise: the anchor.** The test file is **285** lines; `:211` is `  });` (two-space indent, one of exactly FIVE such lines — `:84`, `:88`, `:129`, `:211`, `:284` — so the hunk header's line number, not the bytes alone, places the insertion) and `:210` is `    });`. The trailing context line is non-blank and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: the in-process middleware call.** `makeReq` (`:24-32`) builds `{ headers, get }` from its overrides; `makeRes` (`:34-48`) records `_status` and `_json` and returns itself from `status()`; the middleware reads only `req.headers`, `res.status(...).json(...)`, `next()` and (under a tamper) `res.setHeader`, whose absence the limiter's own fallback catch absorbs. `res._json` is typed `any` (`:34`), so `res._json?.success` type-checks; `(req as any).user?.role` reads the principal the middleware may set.
- **Premise: the seeded cache.** `apiKeyCache` is `Map<string, { result: ConnectorMeta | null; expiresAt: number }>` (`:168`); the `meta` literal carries all seven `ConnectorMeta` fields (`:57-75`). `beforeEach` (`:77`) clears the cache before every cell, so the seeding cannot leak into another cell; `fetchMock.mockReset()` (`:78`) likewise resets the `mockResolvedValue`.
- **Premise: no `+` line re-adds a tip line.** The only `+` line that also occurs at the tip is `    });` (`:210` and others — unavoidable for a new cell); `        const res = makeRes();` and `        const next = vi.fn();` are 8-space indented and do NOT occur at the tip (the existing cells use 6 spaces).
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (the Bearer is built with `'Bearer ' + ...`). The title uses `-` and `,`, no em dash.
- **Premise: the runner.** `api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: no live-lane collision.** `middleware/auth.ts` is not `index.ts`, `preflight.sh`, `enforcement.ts` or under `services/anchoring/**`; the test file is not `ks480-connector-auth`, `ks740-bounded-fanout`, `row-converters`, `ks1041-vouch-header-strip`, `ks501-enforcement-non-string-doctype` or `ks480-org-provisioner-gate`. **No held `READY_*` and no brief in `night/briefs/` names `__tests__/auth.test.ts`** (0 by `grep -il`; positive control: the same grep for `ks480-org-provisioner-gate` finds `KS-1283-PROVADMIN-1.md`). `git log` on the test file at the tip: last change `34a5462f1` (#293, KS-302 JWT_SECRET removal); on `middleware/auth.ts`: `a105cd32b` (#1034, KS-1215); `git blame` at the tip: `:276` last touched by `29033ce47` (2026-03-22), `:279` by `efaaa6034` (2026-09-17, KS-1207).
- **Premise: the surface.** The cell seeds an in-memory cache and drives one exported middleware function twice with a fake req/res. No user store, no session, no MFA state, no real JWT verification (the beside-Bearer is a test token that the tip never reaches), no product bytes. AUTH surface, test-only pin (allowed).

## Collision

**Shared product file, different lines, different test files.** The held `READY_KS-1238-F1i` tampers `middleware/auth.ts:299` and the held `READY_KS-1205-F3` tampers `:300` — both test-only, both in NEW test files of their own, both planted-and-restored, so neither moves `:276` / `:279` and neither touches `auth.test.ts`. Seat B 11th's files (`index.ts`, `preflight.sh`, `ks480-connector-auth.test.ts`, `ks1041-vouch-header-strip.test.ts`, ...) include neither this test file nor this product file. KS-1198 (round-22 next-best 2) pins the RS256 branch of the same file from `:375` down — a later brief, no overlap with these two lines. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 01:xx, `--shared` scratch clone at `778e6cfe2`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after)

- REAL `tasks/test_only/checker.sh` on this brief's own diff: **RESULT: PASS (8/8), TWICE on two fresh `--shared` clones** (`checker.log`, `checker_final.log`), `apply=strict` (header counts right: 15 `+` and 1 context = 16). T5 green at the tip 17/17 cells in the file (16 at the bare tip: 6 `parseTestToken` + 5 `authenticateToken` + 5 `validateApiKey`, plus the new one); T6 SPLITFIRST reds exactly `joined`, T6 FALLTHROUGH reds exactly `joined`, every red an assertion failure — the direct runs with the default reporter (`direct_splitfirst.out`, `direct_fallthrough.out`) show the received arrays as `['sk_first, sk_second', 1, 0, undefined, undefined, 'connector']` / `['sk_second, sk_first', 1, 0, undefined, undefined, 'connector']` under SPLITFIRST and the same with `'user'` under FALLTHROUGH, against the expected `[..., 0, 401, false, 'UNAUTHORIZED', undefined]` (`direct_tip.out`: 17 passed); T7 all three controls green under both; T8 `middleware/auth.ts` restored by bytes (sha256 9abef1c21164 == tip blob) after each. No `Unhandled` error in any run output (0 by grep across `out.md.checker/*.out`).
- Two WRONG variants refused at the named gates: a control declared as the PREFIX `rejects with 401 when required=true` -> **FAIL T5** `DECLARED CELL NOT IN THE RUN` (`var1/`, its own fresh clone); the SPLITFIRST tamper at `Line: 275` (off by one) -> **builder REFUSED rc 2** naming the tip's `:275` (`    // --- API key path ---`) against the brief's From (`var2/`). Each checker variant ran in its own fresh `--shared` clone (the checker resets its clone at START, not END).
- Whole api-gateway vitest suite with the cell applied: **69 files, 679/679 green** (`full_suite.out`); the bare tip **69 files, 678/678** (`full_suite_tip.out`; +1 = this cell). `tsc` not run: `tsconfig.json` excludes `src/__tests__`.
- Input key set identical to `night/inputs/test_only_1283PROVADMIN-1.json` (both directions empty, `keydiff.log`); 15 `+` lines, 0 non-ASCII, 0 backslash, 0 blank. Source checkout tracked-modified count 0 before the clone, after prepare, after every checker run; `ls-remote` develop = `778e6cfe2` at start and at close. No port touched (the middleware's fetches all land on the file's `fetchMock`; no Redis client exists in the run).
- Artefacts: `local-model/runs/2026-09-21_ks1244-drafter-precheck/` (linear_ks1244.json, build.log, keydiff.log, prepare.log, prepare_final.log, checker.log, checker_final.log, out.md, out_final.md, golden.patch.md, out.md.checker/, out_final.md.checker/, direct_tip.out, direct_splitfirst.out, direct_fallthrough.out, full_suite.out, full_suite_tip.out, var1/, var2/, input_prechecked.json).
- NOT measured: a real HTTP request with two `x-api-key` header lines through Express (the join is Node's documented behaviour; the cell hands the middleware the joined string Node would produce, and no server was booted); the OPTIONAL-mount fall-through (deliberately unpinned — it is the defect); the connector-token exchange under SPLITFIRST beyond `fetchMock` answering no token.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`, then the hunk above exactly as shown (`@@ -211,1 +211,16 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2. Refs KS-1244** (and KS-1207, whose required-mount refusal this cell pins for the joined-header case; KS-736 for the fall-through family). **NEVER Closes** — KS-1244 asks for a PRODUCT change (refuse a repeated `x-api-key` outright, on optional mounts too); this brief pins the half that is already right and leaves the optional-mount fall-through as the open defect it is.
- **Not from a gate cell.** Found by the 2026-09-21 widened test-only sweep (round 22, next-best 1 after KS-1283); the round-22 note's "no one-line tamper" verdict was re-derived: the FIX has no one-line shape (an inserted refusal), but the PIN of today's required-mount refusal has two (`:276` split-first, `:279` comma-exempt), which is what a test-only brief needs.
- **Not pinned here, said plainly:** the OPTIONAL-mount fall-through to anonymous (`authenticateToken(false)` with a joined key calls `next()` with no user today — the defect; a cell asserting it would pin the bug); the refusal message; a repeated header arriving as an ARRAY (Node never hands `x-api-key` as an array, so `:276`'s `as string` cast is the shape that runs).
- **Collision: shared product file with two held test-only READYs (`:299`, `:300`), no shared line, no shared test file** (measured above).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1244 night/inputs/test_only_1244JOINEDKEY-1.json night/briefs/KS-1244-JOINEDKEY-1.md ctx=65536
```
