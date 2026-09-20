# KS-1198 SKMETA-1 PIN THAT AN sk_ KEY VALIDATED ON THE API-KEY PATH ATTACHES THE VALIDATED KEY'S METADATA AS req.connectorMeta, SCOPES INTACT — the ONE source of the connector gates' input (the half of KS-1198 that is RIGHT today) — the gateway's own authenticateToken, driven in process — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 01:xx on 2026-09-21, widened sweep round 22 next-best 2)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`
Tip: `778e6cfe2b6061d60ffcf3a57a951c84dc152b67`
Runner: `vitest`

Written from develop `778e6cfe2b6061d60ffcf3a57a951c84dc152b67` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 01:xx on 2026-09-21, read verbs only; the #1104 merge, unchanged since the round-22 search and since the KS-1244 brief). The test file at that tip is **285 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (**432 lines**, read whole): `ConnectorMeta` at `:57-65`, `apiKeyCache` at `:168` (exported, `:14` of the test file imports it), `getConnectorBearer` at `:188-212`, `validateApiKey` at `:218-252` (a cache hit returns the cached `result` object itself, `:220`), `authenticateToken` at `:273-432` (exported, `:12` of the test file imports it), the `x-api-key` read at `:276`, the connector branch at `:290-343`, the principal at `:300-321`, **`(req as any).connectorMeta = meta;` at `:322`** (the ONE place in the gateway that sets `connectorMeta`), the exchange at `:327`, the limiter hand-off at `:341`. The readers of `connectorMeta` are `routes/verification.ts:1201-1239` (scope check `canCreate` at `:1207`, `allowedDocumentTypes` at `:1225-1238`), `:1257-1267` (workflow bypass) and `services/health.ts:39-43` (`/api/connector/info`) — every one of them is skipped when `connectorMeta` is absent. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `middleware/auth.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1198 reports that a **connector JWT** (the short-lived `type: 'connector'` RS256 token auth mints from a validated `sk_` key) presented directly as `Authorization: Bearer` skips the gateway's connector gates, because the RS256 path sets no `connectorMeta` — "connectorMeta is set only on the sk_ path (`middleware/auth.ts:292`)" at the ticket's base `eb1051fd3`, which is `:322` at this tip, re-read byte for byte. The ticket offers two fix shapes ("refuse it at the gateway, or attach `connectorMeta` so the same gates run") and a pin of TODAY's Bearer-path behaviour would decide between them (a pin of acceptance reds under "refuse"; a pin of no-meta reds under "attach"), so the Bearer path is NOT pinned here. The half that is RIGHT today, that BOTH fix shapes keep, and that the "attach" shape must replicate, is the sk_ path: at the tip a validated key's `ConnectorMeta` is attached to the request as `req.connectorMeta` (`:322`) — the ONLY input the scope check, the document-type allow-list, the workflow bypass and `/api/connector/info` read — and nothing in the api-gateway suite asserts it (`git grep -i -E "expect.*connectorMeta"` over `src/__tests__` at the tip: 0 lines; the two files that mention `connectorMeta` SET it inside their own fake middleware; positive control `expect.*user.role`: 4 lines; Seat B's `ks480-connector-auth.test.ts:84-87` pins `role`, `scopes`, `tenantId` and the exchanged Bearer on the principal, never `connectorMeta`). So the two ways this could silently loosen are unpinned: the meta being dropped (every connector gate then skips for sk_ callers — the very hole KS-1198 describes, opened for the API-key path too), or the meta attached with the key's grants replaced (a wildcard `'*'` passes `canCreate` at `verification.ts:1207`). This change adds ONE cell to the `describe('authenticateToken', ...)` block that seeds `apiKeyCache` with one VALID key (`sk_meta`) whose meta carries `scopes: ['documents:write']`, points the file's own `fetchMock` at an exchange answer with no token, calls the REAL `authenticateToken(true)` with the file's own `makeReq` / `makeRes` / `vi.fn()`, and asserts `[next-calls, status, req.user.role, req.connectorMeta]` equals `[1, 0, 'connector', meta]` (deep equality — the attached meta is the validated key's meta, field for field, scopes included). Every existing cell is unchanged. **It pins TODAY's sk_-path attachment and decides nothing about KS-1198's fix** — the Bearer path with a connector JWT (the defect) is deliberately NOT driven.

## The exact change — ONE hunk in the test file

The new cell goes at the START of the `describe('authenticateToken', ...)` block opened at `:135`, directly above that block's first cell (`:136`, `    it('skips auth when required=false and no token is present', async () => {`, the ONE trailing context line — it occurs exactly once in the file). There is NO leading context: the line above (`:135`, `  describe('authenticateToken', () => {`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`.**

```
@@ -136,1 +136,10 @@
+    it('RED KS-1198: an sk_ key validated on the API-key path attaches the validated key metadata as req.connectorMeta, scopes intact, for the connector gates to read', async () => {
+      const meta = { connectorId: 'c-meta', scopes: ['documents:write'], organizationId: 'org1', tenantId: 't1', tenantSlug: 'one', rateLimit: 100, rateLimitWindow: 60 };
+      apiKeyCache.set('sk_meta', { result: meta, expiresAt: Date.now() + 60000 });
+      fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: {} }) });
+      const req = makeReq({ headers: { 'x-api-key': 'sk_meta' } });
+      const res = makeRes(), next = vi.fn();
+      await authenticateToken(true)(req, res as any, next);
+      expect([next.mock.calls.length, res._status, (req as any).user?.role, (req as any).connectorMeta]).toEqual([1, 0, 'connector', meta]);
+    });
     it('skips auth when required=false and no token is present', async () => {
```

`describe`, `it`, `expect` and `vi` are already imported by the file at `:6`, `authenticateToken` and `apiKeyCache` at `:12` and `:14`, and `makeReq` (`:24-32`), `makeRes` (`:34-48`) and `fetchMock` (`:67-68`, the file's global `fetch` stub) are the file's own helpers — you add NO import and NO helper. The `beforeEach` at `:75-84` already sets `NODE_ENV=test`, clears `apiKeyCache`, resets `fetchMock` and enables test tokens before every cell, so the cell's seeding is local to it. The cell needs no app boot, no port, no real fetch and no database: the middleware is called as a function with the file's fake req/res, exactly as `:136-210` already call it.

## Cells

- `skmeta` = `RED KS-1198: an sk_ key validated on the API-key path attaches the validated key metadata as req.connectorMeta, scopes intact, for the connector gates to read`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1198: an sk_ key validated on the API-key path attaches the validated key metadata as req.connectorMeta, scopes intact, for the connector gates to read

## Tampers

Two single-line tampers on the SAME line of `middleware/auth.ts` (`:322`, the only line in the gateway that sets `connectorMeta`; it occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1; positive control `grep -c -i connectormeta` over the same file is 5: `:57`, `:168`, `:218`, `:238` name the `ConnectorMeta` TYPE and `:322` is the only line that writes the `connectorMeta` PROPERTY). They are the two shapes a loosening can take: the meta DROPPED (the request carries no `connectorMeta`, so every connector gate skips for an sk_ caller — the KS-1198 hole opened on the API-key path), or the meta attached with the key's grants WIDENED to a wildcard (`canCreate` at `verification.ts:1207` accepts `'*'`, so a scope-less key would create documents). Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (`meta` is a non-null `ConnectorMeta` inside `if (apiKey && meta)`; `(req as any)` takes anything), so nothing fails to load and no cell reds for the wrong reason. The checker plants them ONE AT A TIME and restores the file by bytes between them.

### METADROPPED — the validated meta is never attached to the request
File: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts`
Line: 322
From:
```
      (req as any).connectorMeta = meta;
```
To:
```
      (req as any).connectorMeta = undefined;
```
Reds: `skmeta`

### METAWIDENED — the meta is attached with the key's grants replaced by a wildcard
File: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts`
Line: 322
From:
```
      (req as any).connectorMeta = meta;
```
To:
```
      (req as any).connectorMeta = { ...meta, scopes: ['*'] };
```
Reds: `skmeta`

## Controls

- `rejects with 401 when required=true and no token is present`
- `accepts a valid JWT and populates req.user`
- `validates sk_ prefixed keys via Security Service`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:147`, `:159` and `:218` before this hunk, `:156`, `:168` and `:227` after it — each occurs exactly once in the file and none is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; the prefix rule in `build_test_only_input.sh`'s header is for BASH suites only. The other 12 existing cells (`parseTestToken` x6, `skips auth when required=false ...`, `rejects an expired JWT ...`, `assigns defaultTenantId ...`, and the remaining three `validateApiKey` cells) are also green under both tampers but are left undeclared. The `:147` control is the liveness proof for the fake res (same `res._status` / `res._json` slots); the `:159` control proves the RS256 Bearer path — the path the ticket's defect lives on, which this cell never drives — still works beside the new cell; the `:218` control proves `fetchMock` still feeds `validateApiKey` after this cell's `mockResolvedValue` (the `beforeEach` `mockReset` at `:78` clears it).)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `:276` reads `'sk_meta'`, `:277` finds it starts with `sk_` (`presentedKey` true), `:278` calls `validateApiKey('sk_meta')` — a cache HIT (`:219-220`, the seeded entry, 60 s from now) — which returns the seeded `meta` object itself, so `:279` is false (meta is set), `:290` is true, `:299` deletes an `authorization` header that was never sent, `:300-320` build the connector principal (`role: 'connector'`, `authMethod: 'api_key'`), `:321` sets `req.user`, **`:322` sets `req.connectorMeta` to that same `meta` object**, `:327` asks `getConnectorBearer('sk_meta')` (a `connectorBearerCache` miss; `fetchMock` answers `ok: true` with no `data.token`, so `:204` returns null silently — no real fetch, no cache write, no error log), `:328` is false, `:331-337` write the forwarded headers, and `:341` runs the per-key limiter, which counts in memory (no Redis client in a unit run), finds the file's fake res has no `setHeader`, and reaches its own fallback `next()` (`rateLimitEnforce.ts:244-256`) — synchronously, before the middleware returns (measured by the KS-1244 brief's SPLITFIRST run on the same branch: `next` count 1). The asserted array is `[1, 0, 'connector', <the seeded meta>]`, and `toEqual` against `[1, 0, 'connector', meta]` holds field for field.

Under **METADROPPED** `:322` sets `req.connectorMeta` to `undefined` and everything else is identical: the array reads `[1, 0, 'connector', undefined]` — assertion red (fourth slot `undefined` vs the meta object). Under **METAWIDENED** `:322` attaches a copy of the meta whose `scopes` is `['*']`: the array reads `[1, 0, 'connector', { ...meta, scopes: ['*'] }]` — assertion red (`scopes` `['*']` vs `['documents:write']`). Under BOTH, every existing cell stays green: the no-header cells never present a key (`:277` false, `:290` false — `:322` is never reached), the JWT cells carry no `x-api-key`, and the `validateApiKey` cells call the function directly, which does not contain `:322`.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `middleware/auth.ts` at `778e6cfe2`, line 322 is `      (req as any).connectorMeta = meta;` (6-space indent), byte for byte; it occurs **exactly once** in the file (`grep -c -F -x`, 1); case-sensitive `connectorMeta` matches only this line, and the case-insensitive positive control matches 5 (the four others are the `ConnectorMeta` type at `:57`, `:168`, `:218`, `:238`) — this is the ONLY line in the gateway's middleware that writes `connectorMeta`. The checker plants and restores it one tamper at a time (T8 by sha256 after each; tip blob sha256 `9abef1c21164...`).
- **Premise: the ticket's claim, re-derived.** The ticket's `auth.ts:292` at its base `eb1051fd39fe3edab4e0b1d1967515b758d4ba3f` is `      (req as any).connectorMeta = meta;` (read with `git show`), the same line as `:322` at this tip (moved by KS-1207's +4 and KS-1215's comment block). `connectorMeta` is set nowhere else in `api-gateway/src` outside tests (`git grep connectorMeta`: `auth.ts:322` the setter; `verification.ts:59/63/1201/1202/1207/1217/1257/1263` and `health.ts:39` readers). The RS256 path `:375-423` never writes it — the ticket's defect, NOT pinned here. `KS-1198` occurs **0** times in `src/__tests__`.
- **Premise: the anchor.** The test file is **285** lines; `:136` is `    it('skips auth when required=false and no token is present', async () => {` (4-space indent, occurs exactly once in the file) and `:135` is `  describe('authenticateToken', () => {`. The trailing context line is non-blank and unique, and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: the in-process middleware call.** `makeReq` (`:24-32`) builds `{ headers, get }` from its overrides; `makeRes` (`:34-48`) records `_status` and `_json` and returns itself from `status()`; the middleware reads only `req.headers`, writes `req.user`, `req.connectorMeta` and forwarded `req.headers[...]`, and calls `next()`; `res.setHeader`, absent on the fake res, is what the limiter's own fallback catch absorbs. `(req as any).user?.role` and `(req as any).connectorMeta` read what the middleware set.
- **Premise: the seeded cache.** `apiKeyCache` is `Map<string, { result: ConnectorMeta | null; expiresAt: number }>` (`:168`); the `meta` literal carries all seven `ConnectorMeta` fields (`:57-65`), `scopes: ['documents:write']` (the canonical KS-71 create scope, `verification.ts:1203-1207`). `validateApiKey` on a hit returns `cached.result` by reference (`:220`), so the object the cell holds is the object `:322` attaches. `beforeEach` (`:77`) clears the cache before every cell; `fetchMock.mockReset()` (`:78`) clears the `mockResolvedValue`.
- **Premise: `+` lines that also occur at the tip.** Two, both added by this brief (so T4 accepts them): `    });` (`:145` and others — unavoidable for a new cell) and `      await authenticateToken(true)(req, res as any, next);` (`:152`, `:188` — the file's own call idiom, reused verbatim). `      const res = makeRes(), next = vi.fn();` is one line and does NOT occur at the tip (the existing cells declare them on two lines). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The title uses `-`, `,` and `_`, no em dash.
- **Premise: the runner.** `api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: no live-lane collision.** `middleware/auth.ts` is not `index.ts`, `preflight.sh`, `enforcement.ts` or under `services/anchoring/**`; the test file is not `ks480-connector-auth`, `ks740-bounded-fanout`, `row-converters`, `ks1041-vouch-header-strip`, `ks501-enforcement-non-string-doctype` or `ks480-org-provisioner-gate`. The ONE held `READY_*` and the ONE brief in `night/briefs/` that name `__tests__/auth.test.ts` are KS-1244's (`grep -il`, 1 and 1) — see Collision. `git log` on the test file at the tip: last change `34a5462f1` (#293, KS-302 JWT_SECRET removal); on `middleware/auth.ts`: `a105cd32b` (#1034, KS-1215); `git blame` at the tip: `:322` last touched by `29033ce47` (2026-03-22).
- **Premise: the surface.** The cell seeds an in-memory cache and drives one exported middleware function once with a fake req/res. No user store, no session, no MFA state, no JWT at all (the connector-JWT mint and the RS256 verify are never reached), no product bytes. AUTH surface, test-only pin (allowed).

## Collision

**Same test file as the held `READY_KS-1244-JOINEDKEY-1` — DISJOINT hunks, same product file, DIFFERENT tamper lines.** KS-1244's hunk is `@@ -211,1 +211,16 @@` (appends at the END of the `authenticateToken` block, trailing context `:211` `  });`); this hunk is `@@ -136,1 +136,10 @@` (inserts at the START of the same block, trailing context `:136`). Both orders apply with `git apply` — measured below: **KS-1244 first, then this** applies both at their stated lines (this hunk's `:136` is above KS-1244's insertion, so it never shifts); **this first, then KS-1244** applies this at `:136` and KS-1244's at `:220` (offset +9 — `git apply` locates the `  });` context nine lines down; the two nearer `  });` lines at `:129` and `:88` are farther from the stated line than `:220` is, so git picks `:220`). The resulting file is byte-identical in both orders (sha256 compared), and the file with BOTH cells runs 18/18 green at the tip. **Order for the raise: either; if raised in one PR, put KS-1244's hunk first in the diff (higher line numbers later is the convention) or re-derive this hunk's header as `@@ -136,1 +136,10 @@` unchanged and KS-1244's as `@@ -220,1 +220,16 @@` after this one merges.** Tamper lines: KS-1244 plants `:276` / `:279`, this plants `:322` — no shared line; each is planted-and-restored, none moves the other. The held `READY_KS-1238-F1i` (`:299`) and `READY_KS-1205-F3` (`:300` at its tip; new test files of their own) share the product file, not a line and not this test file. Seat B 11th's files (`index.ts`, `preflight.sh`, `ks480-connector-auth.test.ts`, `ks1041-vouch-header-strip.test.ts`, ...) include neither this test file nor this product file. Neither tamper of this brief reds KS-1244's cell (its `meta` is null, `:322` unreached) and neither of KS-1244's reds this cell (`'sk_meta'` has no comma: SPLITFIRST's `split(',')[0]` returns it unchanged, FALLTHROUGH's `!includes(',')` is true). Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 01:xx, `--shared` scratch clone at `778e6cfe2`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after)

(filled in below after the checker run — see the end of this section)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts`, then the hunk above exactly as shown (`@@ -136,1 +136,10 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (auth surface, test-only pin — allowed). Refs KS-1198** (and KS-480, whose connector principal this cell pins the meta half of; KS-1176/KS-1204 for the gates that read it). **NEVER Closes** — KS-1198 asks for a PRODUCT decision on the Bearer path (refuse a `type: 'connector'` JWT at the gateway, or attach `connectorMeta` for it); this brief pins the sk_-path attachment that the "attach" shape must replicate and the "refuse" shape leaves untouched, and leaves the Bearer-path defect as the open defect it is.
- **Not from a gate cell.** Found by the 2026-09-21 widened test-only sweep (round 22, next-best 2 after KS-1283 and KS-1244); the round-22 note's premise ("a minted `type: 'connector'` RS256 JWT fixture" on the Bearer path) was re-derived and REJECTED: any pin of today's Bearer-path outcome for a connector JWT decides between the ticket's two fix shapes (acceptance reds under "refuse", no-meta reds under "attach"), so it would pin the bug or the fix, never today's right behaviour. The sk_-path setter the ticket itself cites (`:292` at its base, `:322` here) is the half that is right, unpinned, and kept by both shapes.
- **Not pinned here, said plainly:** the Bearer path with a connector JWT (the defect — a cell asserting it would pin the bug); the Bearer path with a HUMAN RS256 JWT carrying no `connectorMeta` (right today and kept by both shapes, but no one-line loosening on the RS256 path makes it a graded red, and driving RS256 in this cell would route the JWKS fetch through the same `fetchMock` this cell points at the exchange); the gates themselves (`verification.ts:1201-1239`, `health.ts:39` — route code, no in-process driver in this file).
- **Collision: same test file as the held KS-1244 READY, disjoint hunks (start vs end of the same `describe`), both orders measured, same product file with three held READYs (`:276/:279`, `:299`, `:300`) and no shared line** (measured above and in the MEASURED section).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1198 night/inputs/test_only_1198SKMETA-1.json night/briefs/KS-1198-SKMETA-1.md ctx=65536
```
