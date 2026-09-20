# READY — KS-753-VERIFIEDPERSISTED-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks753-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 04:44 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks753-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck/VERIFIEDPERSISTED/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 04:44 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks753-ornith35b-night2/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts` (modify). `+` lines 32 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 9/9 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `VERIFIEDATDROPPED` → red exactly ['RED KS-753: with the db available, POST /api/timestamps and ']
- `VERIFIEDFALSE` → red exactly ['RED KS-753: with the db available, POST /api/timestamps and ']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks753-ornith35b-night2/input.json`. Brief: `night/briefs/KS-753-VERIFIEDPERSISTED-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks753-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts
@@ -122,1 +122,33 @@
+  it('RED KS-753: with the db available, POST /api/timestamps and /api/timestamps/batch INSERT the mock fallback into ts_timestamps with verified true and a verified_at date - the persisted half of the verified claim', async () => {
+    vi.stubGlobal('fetch', async () => ({ ok: false, status: 503, statusText: 'unavailable' } as Response));
+    const nodeCrypto = await import('crypto');
+    const { privateKey, publicKey } = nodeCrypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+    const b64url = (s: string | Buffer) => Buffer.from(s).toString('base64url');
+    const signingInput = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) + '.' + b64url(JSON.stringify({ userId: 'u-ks753', email: 'ks753@secuura.io', role: 'user', verificationLevel: 'email', exp: Math.floor(Date.now() / 1000) + 300 }));
+    const bearer = 'Bearer ' + signingInput + '.' + b64url(nodeCrypto.sign('sha256', Buffer.from(signingInput), privateKey));
+    const savedEnv = { JWT_PUBLIC_KEY: process.env.JWT_PUBLIC_KEY, PORT: process.env.PORT };
+    process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
+    process.env.PORT = '0';
+    const queries: Array<[string, unknown[]]> = [];
+    vi.doMock('../db', () => ({ initDb: async () => true, isDbAvailable: () => true, query: async (sql: string, params?: unknown[]) => { queries.push([sql, params || []]); return { rows: [], rowCount: 0 }; }, closeDb: async () => undefined }));
+    vi.resetModules();
+    const { default: app } = await import('../index');
+    const drive = (url: string, body: unknown) => new Promise<any>((resolve) => {
+      const headers: Record<string, unknown> = {};
+      const req: any = { method: 'POST', url, headers: { authorization: bearer }, body };
+      const res: any = { statusCode: 200, locals: {}, on: () => res, status: (c: number) => { res.statusCode = c; return res; }, json: (b: unknown) => { resolve({ status: res.statusCode, body: b }); return res; } };
+      res.send = res.json;
+      res.end = () => res.json(null);
+      res.setHeader = (k: string, v: unknown) => { headers[k.toLowerCase()] = v; return res; };
+      res.getHeader = (k: string) => headers[k.toLowerCase()];
+      res.removeHeader = (k: string) => { delete headers[k.toLowerCase()]; };
+      app(req, res, () => resolve({ status: -1, body: null }));
+    });
+    const single = await drive('/api/timestamps', { hash: 'a'.repeat(64), timestampType: 'rfc3161' });
+    const batch = await drive('/api/timestamps/batch', { hashes: [{ hash: 'b'.repeat(64) }, { hash: 'c'.repeat(64) }], timestampType: 'rfc3161' });
+    for (const k of ['JWT_PUBLIC_KEY', 'PORT'] as const) { if (savedEnv[k] === undefined) delete process.env[k]; else process.env[k] = savedEnv[k]; }
+    const inserts = queries.filter(([sql]) => sql.trimStart().startsWith('INSERT INTO ts_timestamps'));
+    const persisted = Object.fromEntries(inserts.map(([, p]) => [String(p[2]), [p[9], p[10] instanceof Date]]));
+    expect([single.status, single.body.data.verified, batch.status, inserts.length, persisted]).toEqual([201, true, 201, 3, { ['a'.repeat(64)]: [true, true], ['b'.repeat(64)]: [true, true], ['c'.repeat(64)]: [true, true] }]);
+  });
   it('RED KS-753: POST /api/timestamps and /api/timestamps/batch answer 201 with verified true for the mock TSA fallback when no TSA is reachable - the mock is reported as verified today', async () => {
```
