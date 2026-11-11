# READY — KS-1868-KS-1868-O138-P4 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 16:05 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 16:05 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/tokenisation/src/index.ts } + { Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tokenisation/src/index.ts` (product) and `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
18	3	Blockchain/Dev/services/tokenisation/src/index.ts
170	0	Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (18 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/tokenisation/src/index.ts`; test(s): `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/tokenisation/src/index.ts 18 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts 170 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tokenisation/src/index.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 tokenisation route catches read the thrown value safely RED ks1868 R1 tokenise: a revoked Proxy thrown value answers 400 with the constant reason', 'KS-1868 tokenisation route catches read the thrown value safely RED ks1868 R2 tokenise: an Error whose message getter throws answers 400 with the constant reason', 'KS-1868 tokenisation route catches read the thrown value safely RED ks1868 R3 detokenise: a revoked Proxy thrown value answers 400 with the constant reason', 'KS-1868 tokenisation route catches read the thrown value safely RED ks1868 R4 detokenise: an Error whose message getter throws answers 400 with the constant reason', 'KS-1868 tokenisation route catches read the thrown value safely RED ks1868 R5 hash-key: a revoked Proxy thrown value answers 400 with the constant reason', 'KS-1868 tokenisation route catches read the thrown value safely RED ks1868 R6 hash-key: an Error whose message getter throws answers 400 with the constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=8 failed=0 | after: total=17 failed=0` · `NEW reds: []` [baseline_suite.json total=8 failed=0; after_suite.json total=17 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tokenisation suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tokenisation: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tokenisation/src/index.ts` (+18/-3 per numstat.out) and the test file `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts` (+170/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/tokenisation/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p4_tokenisation_index_tokenise_detokenise_and_hash_key_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/tokenisation/src/index.ts b/Blockchain/Dev/services/tokenisation/src/index.ts
--- a/Blockchain/Dev/services/tokenisation/src/index.ts
+++ b/Blockchain/Dev/services/tokenisation/src/index.ts
@@ -79,5 +79,10 @@
     res.json({ success: true, fields: results });
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : String(err);
+    } catch {
+      message = 'unreadable thrown value';
+    }
     res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: message } });
   }
@@ -111,5 +116,10 @@
     res.json({ success: true, values: results });
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : String(err);
+    } catch {
+      message = 'unreadable thrown value';
+    }
     res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: message } });
   }
@@ -399,5 +409,10 @@
     res.json({ success: true, keyHash: hashKey(key) });
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
+    let message: string;
+    try {
+      message = err instanceof Error ? err.message : String(err);
+    } catch {
+      message = 'unreadable thrown value';
+    }
     res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: message } });
   }
diff --git a/Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-route-catches-unreadable-throw.test.ts
@@ -0,0 +1,170 @@
+import { describe, it, expect, vi, beforeAll, beforeEach } from 'vitest';
+
+// KS-1868: three route catches of the tokenisation service (POST /api/tokenise, POST /api/detokenise and POST /api/hash-key) read the caught value with
+// `err instanceof Error ? err.message : String(err)` into `message` before answering 400. That read can itself throw (a revoked Proxy throws on
+// `instanceof`; an Error whose `message` getter throws, throws on `.message`), and inside an async Express 4 handler the rejection is not caught: the
+// request gets no answer and Node sees an unhandled rejection. Each catch now reads the value inside its own try and uses the constant
+// `unreadable thrown value` when it cannot be read; an ordinary Error and a thrown string answer exactly as before.
+// `express`, `helmet`, `@secuura/shared`, the vault, the crypto helpers, the db and the tenant scope are replaced and the route handlers are captured and
+// called directly with a fake request and response: no port is bound, no database is touched. The stand-ins that reject or throw with the value are
+// plain functions, not vi.fn(): a spy inspects what it receives and could itself fail on a revoked Proxy before the code under test saw it.
+const ks = vi.hoisted(() => ({
+  routes: {} as Record<string, (req: unknown, res: unknown) => Promise<void>>,
+  toThrow: undefined as unknown,
+}));
+
+vi.mock('express', () => {
+  const app = {
+    use: () => app,
+    get: () => app,
+    post: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['POST ' + p] = f;
+      return app;
+    },
+    listen: () => ({}),
+  };
+  return { default: () => app };
+});
+vi.mock('helmet', () => ({ default: () => (_req: unknown, _res: unknown, next: () => void) => next() }));
+vi.mock('@secuura/shared/zod3-compat', () => ({}));
+vi.mock('@secuura/shared', () => {
+  const passThrough = () => (_req: unknown, _res: unknown, next: () => void) => next();
+  return {
+    boundedJson: passThrough,
+    authenticate: passThrough,
+    requirePlatformRole: passThrough,
+    enforceProductionConfig: () => undefined,
+    errorHandler: () => undefined,
+    tenantGucContext: passThrough,
+    rejectNulBytes: passThrough,
+    runWithTenantId: (_tenantId: string, fn: () => unknown) => fn(),
+  };
+});
+vi.mock('../db', () => ({ initDb: () => Promise.resolve(), query: () => Promise.resolve({ rows: [] }) }));
+vi.mock('../vault', () => ({
+  tokenise: () => Promise.reject(ks.toThrow),
+  detokenise: () => Promise.reject(ks.toThrow),
+  rotateKey: () => Promise.resolve(),
+}));
+vi.mock('../crypto', () => ({
+  generateKey: () => 'k',
+  hashKey: () => {
+    throw ks.toThrow;
+  },
+  encrypt: () => 'e',
+  decrypt: () => 'd',
+}));
+vi.mock('../tenant-scope', () => ({
+  resolveTenantScope: () => ({ ok: true, tenantId: 'ten-1868' }),
+}));
+
+type Res = { statusCode: number; body: unknown; status(c: number): Res; json(b: unknown): Res };
+
+function mkRes(): Res {
+  const r: Res = {
+    statusCode: 200,
+    body: undefined,
+    status(c) {
+      r.statusCode = c;
+      return r;
+    },
+    json(b) {
+      r.body = b;
+      return r;
+    },
+  };
+  return r;
+}
+
+const CASES = [
+  { route: 'POST /api/tokenise', req: { body: { key: 'k', fields: [{ name: 'n', value: 'v' }] }, user: { tenantId: 'ten-1868' } } },
+  { route: 'POST /api/detokenise', req: { body: { key: 'k', tokens: ['t1'] }, user: { tenantId: 'ten-1868' } } },
+  { route: 'POST /api/hash-key', req: { body: { key: 'k' }, user: { tenantId: 'ten-1868' } } },
+];
+
+/** Run one route handler with the stand-in failing with `value`. A handler that rejects (the defect) leaves the response untouched at 200. */
+async function invoke(i: number, value: unknown): Promise<Res> {
+  ks.toThrow = value;
+  const res = mkRes();
+  await ks.routes[CASES[i].route](CASES[i].req, res).catch(() => undefined);
+  return res;
+}
+
+const answer = (message: string) => ({ success: false, error: { code: 'BAD_REQUEST', message } });
+const revoked = () => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const getterThrows = () =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+beforeAll(async () => {
+  await import('../index.js');
+});
+
+beforeEach(() => {
+  ks.toThrow = undefined;
+});
+
+describe('KS-1868 tokenisation route catches read the thrown value safely', () => {
+  it('RED ks1868 R1 tokenise: a revoked Proxy thrown value answers 400 with the constant reason', async () => {
+    const res = await invoke(0, revoked());
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R2 tokenise: an Error whose message getter throws answers 400 with the constant reason', async () => {
+    const res = await invoke(0, getterThrows());
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R3 detokenise: a revoked Proxy thrown value answers 400 with the constant reason', async () => {
+    const res = await invoke(1, revoked());
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R4 detokenise: an Error whose message getter throws answers 400 with the constant reason', async () => {
+    const res = await invoke(1, getterThrows());
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R5 hash-key: a revoked Proxy thrown value answers 400 with the constant reason', async () => {
+    const res = await invoke(2, revoked());
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R6 hash-key: an Error whose message getter throws answers 400 with the constant reason', async () => {
+    const res = await invoke(2, getterThrows());
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('unreadable thrown value'));
+  });
+
+  it('control ks1868 C1 tokenise: an ordinary Error answers 400 with its own message', async () => {
+    const res = await invoke(0, new Error('vault boom'));
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('vault boom'));
+  });
+
+  it('control ks1868 C2 detokenise: a thrown plain string answers 400 with its own text', async () => {
+    const res = await invoke(1, 'plain text failure');
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('plain text failure'));
+  });
+
+  it('control ks1868 C3 hash-key: an ordinary Error answers 400 with its own message', async () => {
+    const res = await invoke(2, new Error('hash boom'));
+    expect(res.statusCode).toBe(400);
+    expect(res.body).toEqual(answer('hash boom'));
+  });
+});
```
