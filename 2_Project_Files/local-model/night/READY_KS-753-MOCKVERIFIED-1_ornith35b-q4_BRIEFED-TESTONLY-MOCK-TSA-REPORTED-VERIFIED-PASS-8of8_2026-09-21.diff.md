# READY — KS-753-MOCKVERIFIED-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks753-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 00:20 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS.

**Held 00:20 2026-09-21 by the 23:4x Wednesday seat after a source read.** Tip `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`. Adds ONE cell to `services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts` pinning TODAY's behaviour: POST /api/timestamps and /api/timestamps/batch answer 201 with `verified: true` for the mock-TSA fallback when no TSA is reachable (`index.ts:516`, unconditional). **This pins the defect KS-753 describes; it decides NOTHING about the ticket's open design question (503 vs `verified:false`)** — the brief says so in its first paragraph, and the raise seat's PR body must say the same.

**Source read (Wednesday, same action):** 31 `+` lines, all 31 byte-present in `night/briefs/KS-753-MOCKVERIFIED-1.md`; 0 `-`; one test file (T2); sibling KS-1232 control 1/31. Model wall 21 s, first sample, round 1.

**Mocking shape (drafter's, reused from the same file):** `vi.stubGlobal('fetch', → 503)` so the REAL qualified-tsa takes its REAL mock fallback; `vi.resetModules()` + `await import`; a four-function `vi.doMock('../db')` stand-in (createTimestamp INSERTs unconditionally); the REAL `@secuura/shared` `authenticate()` satisfied by an in-process RS256 keypair; `PORT=0` for the fresh import; routes driven in-process as `app(req,res,next)` — no HTTP client, no DB, no port. ⚠ Pre-existing property, not introduced: the file's top-level `../index` import binds :4006 at the tip; a live timestamping container on 4006 breaks the FILE before the cell (`lsof` shows none here — the raise seat re-checks).

**Tampers (T6 each reds exactly the cell; T8 restored by bytes):** VERIFIEDEQEIDAS and VERIFIEDNOTMOCK, both on `index.ts:516` (`    verified: true, // Mock timestamps are pre-verified` — byte-checked by Wednesday at the tip, count 1; positive control: `verified: true` on 4 lines 516/573/603/612). Controls (full titles) at :19 and :106 green under both.

**Checker (00:19):** `RESULT: PASS (8/8)`; whole timestamping suite with the cell 43/43 (drafter's precheck, bare tip 42/42; `runs/2026-09-21_ks753-drafter-precheck/`). Drafter's unmeasured, carried: persisted `ts_timestamps.verified` (db is a stand-in), GET read-back, the `requireEidas:true` 503 control, `opentimestamps`/`blockchain` types; `tsc` not run (tests excluded from tsconfig).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); timestamping vitest 43 expected; `Refs KS-753`; PR body carries the "pins today's behaviour, decides nothing" sentence. Partition: the ks740 test file is disjoint from every live seat's files. **Banked: SIX for the next raise seat — KS-1234, KS-1279, KS-1223, KS-880, KS-1232, KS-753.**

---
--- a/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts
@@ -122,1 +122,32 @@
+  it('RED KS-753: POST /api/timestamps and /api/timestamps/batch answer 201 with verified true for the mock TSA fallback when no TSA is reachable - the mock is reported as verified today', async () => {
+    vi.stubGlobal('fetch', async () => ({ ok: false, status: 503, statusText: 'unavailable' } as Response));
+    const nodeCrypto = await import('crypto');
+    const { privateKey, publicKey } = nodeCrypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+    const b64url = (s: string | Buffer) => Buffer.from(s).toString('base64url');
+    const signingInput = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) + '.' + b64url(JSON.stringify({ userId: 'u-ks753', email: 'ks753@secuura.io', role: 'user', verificationLevel: 'email', exp: Math.floor(Date.now() / 1000) + 300 }));
+    const bearer = 'Bearer ' + signingInput + '.' + b64url(nodeCrypto.sign('sha256', Buffer.from(signingInput), privateKey));
+    const savedEnv = { JWT_PUBLIC_KEY: process.env.JWT_PUBLIC_KEY, PORT: process.env.PORT };
+    process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
+    process.env.PORT = '0';
+    vi.doMock('../db', () => ({ initDb: async () => false, isDbAvailable: () => false, query: async () => ({ rows: [], rowCount: 0 }), closeDb: async () => undefined }));
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
+    const shape = (t: any) => [t.eidasQualified, JSON.parse(Buffer.from(t.proof, 'base64').toString()).mock, t.verified];
+    expect([single.status, single.body.error, batch.status, batch.body.error]).toEqual([201, undefined, 201, undefined]);
+    expect([shape(single.body.data), batch.body.data.timestamps.map(shape)]).toEqual([[false, true, true], [[false, true, true], [false, true, true]]]);
+  });
 });
