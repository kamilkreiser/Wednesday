# READY — KS-811-F7SETPIN-R16 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks811-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 06:16 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks811-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed5-drafter-precheck/811F7SETPIN-R16/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 06:16 2026-09-22 by Wednesday after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks811-ornith35b-night/out.md.checker`, not typed).** Tip `64ab105132eada0621622acf4d6053bc59926780`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks811-social-callback-403-code-set-agrees.test.ts` (new). `+` lines 111 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 6/6 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `ROUTECOLLAPSE` → red exactly ['RED KS-811 - the callback route can throw exactly four 403 c', 'RED KS-811 - the published 403 set and the thrown 403 set ag']
- `SPECRENAME` → red exactly ['RED KS-811 - the operation 403 block in auth.openapi.ts name', 'RED KS-811 - the published 403 set and the thrown 403 set ag']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks811-ornith35b-night/input.json`. Brief: `night/briefs/KS-811-F7SETPIN-R16.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks811-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks811-social-callback-403-code-set-agrees.test.ts
@@ -0,0 +1,111 @@
+// KS-811 - nothing in the repo asserted the #815 published 403 code SET for the social callback against the set the
+// route can actually throw; the only comparison ever made was the QA re-gate evidence/f7-setcompare.mjs, outside
+// this repo. check:openapi cannot cover it: it proves the committed yaml matches the generator, not that the generator
+// prose is true. These cells derive BOTH sets from source text at run time - the classes thrown inside the callback
+// handler body, resolved to (status, code) through errorHandler.ts, against the codes the operation 403 block names in
+// auth.openapi.ts - and pin them to each other and to the four codes the contract calls distinct by design. The sets
+// agree at the tip; this is about the day one of them moves.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { join } from 'path';
+
+const NL = String.fromCharCode(10);
+const ROUTES = readFileSync(join(__dirname, '../routes/auth.ts'), 'utf8');
+const ERRORS = readFileSync(join(__dirname, '../middleware/errorHandler.ts'), 'utf8');
+const OPENAPI = readFileSync(join(__dirname, '../auth.openapi.ts'), 'utf8');
+
+/** The four 403 codes the operation description calls distinct by design (KS-722, KS-795 F-4, KS-795 F-6). */
+const PUBLISHED_403 = ['MFA_REQUIRED', 'OAUTH_STATE_INVALID', 'SOCIAL_EMAIL_UNAVAILABLE', 'SOCIAL_SIGN_IN_REFUSED'];
+
+/** The callback handler body: from its registration to the next authRoutes registration. */
+function callbackBody(): string {
+  const start = ROUTES.indexOf('authRoutes.get(' + String.fromCharCode(39) + '/social/:provider/callback');
+  if (start < 0) throw new Error('KS-811 anchor missing: the social callback registration');
+  const rest = ROUTES.slice(start + 10);
+  const end = rest.search(/authRoutes[.](get|post|put|patch|delete)[(]/);
+  if (end < 0) throw new Error('KS-811 anchor missing: the registration after the callback');
+  return ROUTES.slice(start, start + 10 + end);
+}
+
+/** Every error class the body throws, each name once, sorted. */
+function thrownClasses(body: string): string[] {
+  const names = [...body.matchAll(/throw new ([A-Za-z0-9_]+)[(]/g)].map((m) => m[1]);
+  return [...new Set(names)].sort();
+}
+
+type Resolved = { cls: string; status: number | null; code: string | null };
+
+/** Resolve a class to the (status, code) its super() call carries, walking one parent per hop while a hop is silent. */
+function resolveClass(cls: string, depth = 0): Resolved {
+  if (depth > 5) return { cls, status: null, code: null };
+  const head = 'export class ' + cls + ' extends ';
+  const at = ERRORS.indexOf(head);
+  if (at < 0) return { cls, status: null, code: null };
+  const close = ERRORS.indexOf(NL + '}', at);
+  const block = ERRORS.slice(at, close < 0 ? ERRORS.length : close).split(NL).join(' ');
+  const parent = block.slice(head.length).split(' ')[0];
+  const sup = block.match(/super[(](.*)[)];/);
+  const args = sup ? sup[1] : '';
+  const status = args.match(/([0-9]{3}),/);
+  const code = args.match(/'([A-Z][A-Z0-9_]+)'/);
+  if (status && code) return { cls, status: Number(status[1]), code: code[1] };
+  const up = resolveClass(parent, depth + 1);
+  return { cls, status: status ? Number(status[1]) : up.status, code: code ? code[1] : up.code };
+}
+
+/** The 403 response block of the callback operation in auth.openapi.ts, from `403: {` to the `404:` entry. */
+function operationBlock403(): string {
+  const opStart = OPENAPI.indexOf('summary: ' + String.fromCharCode(39) + 'Social OAuth callback');
+  if (opStart < 0) throw new Error('KS-811 anchor missing: the callback operation in auth.openapi.ts');
+  const opEnd = OPENAPI.indexOf('registerPath({', opStart);
+  const op = OPENAPI.slice(opStart, opEnd < 0 ? OPENAPI.length : opEnd);
+  const b403 = op.indexOf('403: {');
+  const b404 = op.indexOf('404:', b403);
+  if (b403 < 0 || b404 < 0) throw new Error('KS-811 anchor missing: the 403 / 404 entries of the callback operation');
+  return op.slice(b403, b404);
+}
+
+/** Every UPPER_SNAKE token in a block, each once, sorted - the codes a response description names. */
+function namedCodes(block: string): string[] {
+  return [...new Set([...block.matchAll(/[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+/g)].map((m) => m[0]))].sort();
+}
+
+describe('KS-811 - the social callback 403 code SET: published in auth.openapi.ts, thrown by routes/auth.ts', () => {
+  const body = callbackBody();
+  const resolved = thrownClasses(body).map((cls) => resolveClass(cls));
+  const thrown403 = [...new Set(resolved.filter((r) => r.status === 403).map((r) => r.code as string))].sort();
+  const named403 = namedCodes(operationBlock403());
+
+  it('RED KS-811 - the callback route can throw exactly four 403 codes: MFA_REQUIRED, OAUTH_STATE_INVALID, SOCIAL_EMAIL_UNAVAILABLE, SOCIAL_SIGN_IN_REFUSED', () => {
+    expect(thrown403).toEqual(PUBLISHED_403);
+  });
+
+  it('RED KS-811 - the operation 403 block in auth.openapi.ts names exactly those four codes', () => {
+    expect(named403).toEqual(PUBLISHED_403);
+  });
+
+  it('RED KS-811 - the published 403 set and the thrown 403 set agree (the F-7 comparison, now in the repo)', () => {
+    expect({ thrownButNotNamed: thrown403.filter((c) => !named403.includes(c)), namedButNotThrown: named403.filter((c) => !thrown403.includes(c)) })
+      .toEqual({ thrownButNotNamed: [], namedButNotThrown: [] });
+  });
+
+  it('CONTROL KS-811 - the callback body is isolated: one registration, holding the account gate', () => {
+    expect((body.match(/authRoutes[.](get|post|put|patch|delete)[(]/g) ?? []).length).toBe(1);
+    expect(body.includes('assertAccountMayReceiveCredential')).toBe(true);
+  });
+
+  it('CONTROL KS-811 - every thrown class resolves in errorHandler.ts, and the 400 classes stay out of the 403 set', () => {
+    expect(resolved.filter((r) => r.status === null || r.code === null)).toEqual([]);
+    const codes400 = resolved.filter((r) => r.status === 400).map((r) => r.code as string).sort();
+    expect(codes400).toEqual(['BAD_REQUEST', 'OAUTH_PROVIDER_ERROR']);
+    expect(thrown403.filter((c) => codes400.includes(c))).toEqual([]);
+  });
+
+  it('CONTROL KS-811 - the 403 block is isolated: the 400 block names OAUTH_PROVIDER_ERROR and the 403 block does not', () => {
+    const opStart = OPENAPI.indexOf('summary: ' + String.fromCharCode(39) + 'Social OAuth callback');
+    const op = OPENAPI.slice(opStart, OPENAPI.indexOf('registerPath({', opStart));
+    const block400 = op.slice(op.indexOf('400: {'), op.indexOf('401:'));
+    expect(namedCodes(block400).includes('OAUTH_PROVIDER_ERROR')).toBe(true);
+    expect(named403.includes('OAUTH_PROVIDER_ERROR')).toBe(false);
+  });
+});
```
