# KS-976 R16B-SCOPE403 - Wednesday's task for Ornith, PART B of the KS-976 pair (security `index.ts`, the two rate-limit 403s): a caller whose scope claims are PRESENT BUT UNUSABLE is told so, and only a caller with NO scope claim hears `Caller has no tenant` - two one-line message edits plus a NEW vitest suite (code_patch, vitest; re-brief of the STALE READY_KS-976-B at develop 8c2f7b3fd, written 12:49:32 AEST on 2026-09-22 by Wednesday's feed11 drafter from the file at the tip - `index.ts` :28-:36, :1366-:1385, :1478-:1494 read; 1598 lines; `rateLimitScope.ts` :112-:126 and :222-:236 read; the reference test `ks952-rate-limit-scope-route.test.ts` (boots `../index` through the SECURITY_DISABLE_BOOT seam) present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `vitest`

## Premises (measured by the feed11 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-976-B_ornith35b-q4_PASS-7of7-r2_2026-09-15.diff.md` (Ornith PASS 7/7 r2 at develop 48e65c435; paths lacked the `Blockchain/Dev/` prefix; its /check hunk carried an em-dash comment `+` line). Part A (the /reset 400 field name) is NOT briefable this feed - its site moved (FEED 10 §1). Ship B alone with `Refs KS-976 (part B)`.
- The product at the tip is UNCHANGED since the old READY at both sites (offset 0): `:1372` `    const scope = principalScope((req as any).user);`, `:1373` `    if (scope === null) {`, `:1377` `      return res.status(403).json({`, `:1378` `        success: false,`, `:1379` the /check 403 line, `:1380` `      });`, `:1381` `    }`; `:1485` `  const scope = explicitScope(parsedBody.data, (req as any).user);`, `:1486` `  if (scope === null) {`, `:1487` `    return res.status(403).json({`, `:1488` `      success: false,`, `:1489` the /reset 403 line, `:1490` `    });`, `:1491` `  }` - all byte-exact at 8c2f7b3fd.
- `'Caller has no tenant'` occurs on FOUR lines of the file (`:752`, `:803`, `:1379`, `:1489` - measured; `:1379` and `:1489` differ from each other only by indentation). ONLY `:1379` (/check) and `:1489` (/reset) are this task; `:752` / `:803` are other routes and must NOT change. The `## Where` below is LINE-KEYED so the checker grades the two `-` lines by their line NUMBERS.
- `principalScope` (`rateLimitScope.ts:112`) returns null when a claim is MALFORMED (blank string, non-string - KS-970 item 2) AND when no usable claim exists at all; `explicitScope` (`:222`) returns null for a malformed body target and otherwise delegates to `principalScope(caller)`. So the 403 is reached for three different reasons and today names one.
- The old READY's test file is ABSENT at the tip (no `ks976*` under `services/security/src/__tests__/`). `security/src/index.ts` is in NEITHER live lane (Seat B = originate/anchoring/auth/shared; Seat C = api-gateway); the held READYs that touch `security/src/index.ts` (`READY_KS-1206`, `READY_KS-888`, `READY_KS-908`, FEED 10 `held_pool.log` line 120) edit OTHER sites (api-key mint, dbSaveApiKey) - none touches `:1377`-`:1381` or `:1487`-`:1491`; the FEED 10 KS-974-A brief (queued this morning) edits `:600` of the same file - a different hunk, no overlap. Ticket KS-976: Backlog, not archived, no PR attached (board read at drafting time).
- The test is REWRITTEN so every `+` line is ASCII, backslash-free, double-quote-free and `$`-free: the JWT is assembled with `+` concatenation (no template literal), `base64url` is Buffer's own encoding (no regex), the red glyph / `\u{1F534}` titles are ASCII `RED KS-976 B1/B2` titles declared under `## Red cells`, the control title has no double quotes. Same three cells, same meaning as the old READY. The product `+` comment line is ASCII (a hyphen where the old READY had an em-dash).

## What is wrong (one paragraph)
`POST /api/rate-limit/check` (`Blockchain/Dev/services/security/src/index.ts:1372`-`:1381`) and `POST /api/rate-limit/reset` (`:1485`-`:1491`) refuse with `403 { code: 'FORBIDDEN', message: 'Caller has no tenant' }` whenever the scope helper returns null - but `principalScope` / `explicitScope` return null for a claim that is PRESENT and unusable (a blank `tenantId`, a numeric `userId`) as well as for a caller with no scope claim at all. An operator whose token carries `tenantId: '   '` is told they have no tenant; a caller with `userId: 123` likewise. The message names the wrong condition and sends the fix in the wrong direction. Fix (KS-976 item 2): at both sites, if any of `user.tenantId`, `user.userId`, `user.sub` is present (not undefined, not null) answer `'Caller scope claims are present but unusable (tenant, user or sub)'`, else keep `'Caller has no tenant'`. The predicate is written INLINE at each site (the old r1's helper function was mis-placed by a re-anchor; the PR seat may hoist it later). NOT in this task: `rateLimitScope.ts`, the other two `'Caller has no tenant'` sites (`:752`, `:803`), the 400 validation answers, Part A.

## The exact change - TWO edits in `Blockchain/Dev/services/security/src/index.ts`, each its own hunk (headers `@@ -1377,5 +1377,6 @@` and `@@ -1487,5 +1487,5 @@`); no blank context line anywhere
E1 - line 1379 (the /check 403) replaced by a KS-976 comment line + the conditional message (1 `-`, 2 `+`; leading context `:1377`-`:1378`, trailing `:1380`-`:1381`):
```
@@ -1377,5 +1377,6 @@
       return res.status(403).json({
         success: false,
-        error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
+        // KS-976 item 2: scope is null for three reasons - say whether a claim was present but unusable, or absent.
+        error: { code: 'FORBIDDEN', message: [(req as any).user?.tenantId, (req as any).user?.userId, (req as any).user?.sub].some((v) => v !== undefined && v !== null) ? 'Caller scope claims are present but unusable (tenant, user or sub)' : 'Caller has no tenant' },
       });
     }
```
E2 - line 1489 (the /reset 403) replaced by the same conditional message at its own indentation (1 `-`, 1 `+`; leading context `:1487`-`:1488`, trailing `:1490`-`:1491`):
```
@@ -1487,5 +1487,5 @@
     return res.status(403).json({
       success: false,
-      error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },
+      error: { code: 'FORBIDDEN', message: [(req as any).user?.tenantId, (req as any).user?.userId, (req as any).user?.sub].some((v) => v !== undefined && v !== null) ? 'Caller scope claims are present but unusable (tenant, user or sub)' : 'Caller has no tenant' },
     });
   }
```
Do not touch any other line: `:752` and `:803` carry the same message text and stay exactly as they are. `:1482` carries an em-dash and is not a context line of either hunk. Old sides 5 / 5 lines; new sides 6 / 5. Indentation: E1's lines start with 8 spaces, E2's with 6 - copy from the fences.

## THIS IS VITEST, NOT JEST
`repo.test_runner` begins with `vitest`: `describe/it/expect/beforeAll/afterAll` imported from `'vitest'`. No `jest.*`. `noUnusedLocals` is on: import ONLY what the cells use (every import below is used). The suite boots the real app through `await import('../index')` with `SECURITY_DISABLE_BOOT=1` and a locally-minted RS256 key in `JWT_PUBLIC_KEY` - the ks952 / ks698r1 harness, copied.

## The test - one NEW vitest file, the ks952 route driver
File: `Blockchain/Dev/services/security/src/__tests__/ks976b-rate-limit-403-says-which-scope-claim-failed.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/security/src/__tests__/ks976b-rate-limit-403-says-which-scope-claim-failed.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 77), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, no `$`, ASCII only.
```
+// KS-976 part B: the rate-limit 403 names the wrong condition. `principalScope` / `explicitScope`
+// return null for THREE reasons (no scope claim at all; a claim present but unusable - blank,
+// non-string; a malformed body target), and both /check (index.ts:1379) and /reset (:1489)
+// answer 'Caller has no tenant' for all of them. After the fix a caller whose claims are present
+// but unusable is told so. Harness: the ks952 route driver - a locally-minted RS256 token and a
+// real listener on 127.0.0.1 through the SECURITY_DISABLE_BOOT seam.
+
+import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import crypto from 'node:crypto';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+
+const b64url = (b: Buffer): string => b.toString('base64url');
+
+function token(claims: Record<string, unknown>): string {
+  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
+  const now = Math.floor(Date.now() / 1000);
+  const payload = b64url(Buffer.from(JSON.stringify({
+    sub: 'ks976', iat: now, exp: now + 300, role: 'ISSUER_ADMIN', ...claims,
+  })));
+  const sig = b64url(crypto.sign('RSA-SHA256', Buffer.from(header + '.' + payload), PRIVATE_PEM));
+  return header + '.' + payload + '.' + sig;
+}
+
+const TENANT_A = 'a0000000-0000-4000-8000-00000000000a';
+let server: Server;
+let base: string;
+
+afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));
+
+async function post(path: string, claims: Record<string, unknown>, body: Record<string, unknown>) {
+  const res = await fetch(base + path, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token(claims) },
+    body: JSON.stringify(body),
+  });
+  const json: any = await res.json();
+  return { status: res.status, json };
+}
+
+beforeAll(async () => {
+  process.env.SECURITY_DISABLE_BOOT = '1';
+  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
+  delete process.env.JWT_JWKS_URL;
+  delete process.env.AUTH_SERVICE_URL;
+  const mod = await import('../index');
+  const app = mod.default;
+  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', resolve); });
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+
+describe('KS-976 part B: rate-limit refusals name the condition that failed', () => {
+  it('RED KS-976 B1: /check with a good tenant and a non-string userId is refused as UNUSABLE, not no-tenant', async () => {
+    const r = await post('/api/rate-limit/check', { tenantId: TENANT_A, userId: 123 }, { key: 'login' });
+    expect(r.status).toBe(403);
+    expect(r.json.error.message).toContain('unusable');
+  });
+
+  it('RED KS-976 B2: /reset by a platform operator whose tenant claim is blank is refused as UNUSABLE', async () => {
+    const r = await post('/api/rate-limit/reset', { role: 'SYSTEM_ADMIN', tenantId: '   ', userId: 'operator-1' }, { key: 'login' });
+    expect(r.status).toBe(403);
+    expect(r.json.error.message).toContain('unusable');
+  });
+
+  it('control: a token with no scope claim at all still says Caller has no tenant; a good principal still passes', async () => {
+    const none = await post('/api/rate-limit/check', { sub: undefined }, { key: 'login' });
+    expect(none.status).toBe(403);
+    expect(none.json.error.message).toBe('Caller has no tenant');
+
+    const ok = await post('/api/rate-limit/check', { tenantId: TENANT_A, userId: 'u-1' }, { key: 'login' });
+    expect(ok.status).toBe(200);
+  });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-976 B1: /check with a good tenant and a non-string userId is refused as UNUSABLE, not no-tenant')` - `userId: 123` is MALFORMED so `principalScope` returns null; at the tip the 403 says `Caller has no tenant` and `toContain('unusable')` fails by assertion; after E1 it says the claims are present but unusable.
- RED `it('RED KS-976 B2: /reset by a platform operator whose tenant claim is blank is refused as UNUSABLE')` - the body names no target, so `explicitScope` delegates to `principalScope(caller)` whose blank `tenantId` is MALFORMED; the same red/green at `:1489` / E2.
- CONTROL `it('control: a token with no scope claim at all still says Caller has no tenant; a good principal still passes')` - no `tenantId`, `userId` or `sub` in the token: the predicate is false on both trees and the message stays `Caller has no tenant`; a good principal is 200 on both trees (proves the harness reaches the route).

## Red cells
- RED KS-976 B1: /check with a good tenant and a non-string userId is refused as UNUSABLE, not no-tenant
- RED KS-976 B2: /reset by a platform operator whose tenant claim is blank is refused as UNUSABLE

## Where (line-keyed - every **must change** line must appear as a `-` line AT ITS NUMBER in your diff; the two `-` lines differ only by indentation, so the checker grades them by line number)
* `:1379` - **must change**: `        error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },` - the /check 403 (E1)
* `:1489` - **must change**: `      error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },` - the /reset 403 (E2)
* `:1372` - (correct) `    const scope = principalScope((req as any).user);` - stays (the /check scope call)
* `:1378` - (correct) `        success: false,` - stays (E1's leading context)
* `:1485` - (correct) `  const scope = explicitScope(parsedBody.data, (req as any).user);` - stays (the /reset scope call)
* `:1488` - (correct) `      success: false,` - stays (E2's leading context)
* `:752` - (correct) `      error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },` - stays (another route - NOT this task)
* `:803` - (correct) `      error: { code: 'FORBIDDEN', message: 'Caller has no tenant' },` - stays (another route - NOT this task)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/security/src/index.ts` / `+++ b/Blockchain/Dev/services/security/src/index.ts` (TWO hunks, headers `@@ -1377,5 +1377,6 @@` and `@@ -1487,5 +1487,5 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/security/src/__tests__/ks976b-rate-limit-403-says-which-scope-claim-failed.test.ts` (one `@@ -0,0 +1,77 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `$`, `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
