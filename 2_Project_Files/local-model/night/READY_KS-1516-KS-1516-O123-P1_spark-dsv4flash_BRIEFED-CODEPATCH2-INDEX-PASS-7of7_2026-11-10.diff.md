# READY — KS-1516-KS-1516-O123-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/out.md.checker/patch.diff`** (from `ls` at 00:37 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false-control/out.md.checker/patch.diff` rc 0, Wednesday spark operator o123).

**Held 00:37 2026-11-10 by Wednesday spark operator o123 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/timestamping/src/index.ts } + { Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/timestamping/src/index.ts` (product) and `Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	2	Blockchain/Dev/services/timestamping/src/index.ts
124	0	Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (9 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/timestamping/src/index.ts`; test(s): `Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/timestamping/src/index.ts 9 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts 124 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/timestamping/src/index.ts` (hunks=4, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=6 of total=10; red cell(s): ['KS-1516 creation reports verified:false for the two placeholder types RED ks1516 R1 opentimestamps: creation answers 201 verified:false and INSERTs verified false with no verified_at', 'KS-1516 creation reports verified:false for the two placeholder types RED ks1516 R2 blockchain: creation answers 201 verified:false and INSERTs verified false with no verified_at', 'KS-1516 /api/timestamps/verify answers verified:false for the two placeholder types, with or without a stored row RED ks1516 R3 opentimestamps: a forged proof (right hash plus one attestation) with no stored row is not verified', 'KS-1516 /api/timestamps/verify answers verified:false for the two placeholder types, with or without a stored row RED ks1516 R4 blockchain: a forged proof (right hash plus chain and slot) with no stored row is not verified', 'KS-1516 /api/timestamps/verify answers verified:false for the two placeholder types, with or without a stored row RED ks1516 R5 opentimestamps: even a stored row whose verified column is true does not verify', 'KS-1516 /api/timestamps/verify answers verified:false for the two placeholder types, with or without a stored row RED ks1516 R6 blockchain: even a stored row whose verified column is true does not verify']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=105 failed=0 | after: total=115 failed=0` · `NEW reds: []` [baseline_suite.json total=105 failed=0; after_suite.json total=115 failed=0]
- A6 [verbatim]: `PASS A6 whole services/timestamping suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/timestamping: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/timestamping/src/index.ts` (+9/-2 per numstat.out) and the test file `Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts` (+124/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/timestamping/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/timestamping/src/index.ts b/Blockchain/Dev/services/timestamping/src/index.ts
--- a/Blockchain/Dev/services/timestamping/src/index.ts
+++ b/Blockchain/Dev/services/timestamping/src/index.ts
@@ -461,4 +461,5 @@
   let tsaName: string | undefined;
-  // KS-753: `verified` means a TSA actually signed this token. The mock-only types below are placeholders by design
-  // and keep `true`; an rfc3161 request that fell back to the locally generated token must NOT claim it.
+  // KS-753: `verified` means a TSA actually signed this token; an rfc3161 request that fell back to the locally
+  // generated token must NOT claim it. KS-1516: the opentimestamps and blockchain proofs are generated locally and
+  // nothing checks them, so those two types set it back to false below.
   let verified = true;
@@ -492,2 +493,3 @@
       proof = generateMockOTSProof(data.hash, now);
+      verified = false; // KS-1516: no attestation check exists
       break;
@@ -499,2 +501,3 @@
       transactionHash = `mock_tx_${crypto.randomBytes(32).toString('hex')}`;
+      verified = false; // KS-1516: no chain check exists
       break;
@@ -572,2 +575,6 @@
 }> {
+  // KS-1516: nothing checks an opentimestamps or blockchain proof against anything, with or without a stored row.
+  if (data.timestampType === 'opentimestamps' || data.timestampType === 'blockchain') {
+    return { verified: false, reason: 'No check exists for this timestamp type: the proof is generated by this service and is not verified' };
+  }
   // Check DB for matching hash + proof
diff --git a/Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts b/Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts
@@ -0,0 +1,124 @@
+import { describe, expect, it, vi, afterEach } from 'vitest';
+
+// KS-1516 (Kam's ruling a, 2026-11-02): the opentimestamps and blockchain proofs are generated locally in index.ts and nothing
+// ever checks them, yet creation answered verified:true and stored verified = true, and POST /api/timestamps/verify answered
+// verified:true for a forged proof (the right hash plus one attestation, or a chain and slot) with no stored row. Until a real check
+// exists, both types must report verified:false on creation (response and INSERT) and on verify (with or without a stored row).
+// rfc3161 is unchanged (KS-753 and KS-1404 own it): the controls pin a real token and a stored verified row.
+// Harness: the real express app, the database replaced by a stand-in that records INSERTs and answers the (hash, proof) lookup.
+
+afterEach(() => {
+  vi.unstubAllGlobals();
+  vi.doUnmock('../tsa/qualified-tsa');
+  vi.doUnmock('../db');
+  vi.resetModules();
+});
+
+const HASH = 'e'.repeat(64);
+const NOW = new Date().toISOString();
+const b64 = (o: unknown) => Buffer.from(JSON.stringify(o)).toString('base64');
+const FORGED_OTS = b64({ version: 1, hash: HASH, type: 'opentimestamps', timestamp: NOW, attestations: [{ type: 'bitcoin', height: 1, merkleRoot: '00' }] });
+const FORGED_CHAIN = b64({ hash: HASH, type: 'blockchain', chain: 'cardano', slot: 1, timestamp: NOW });
+const OTS_NO_ATTESTATION = b64({ version: 1, hash: HASH, type: 'opentimestamps', timestamp: NOW, attestations: [] });
+const REAL_TOKEN = 'cmVhbC10b2tlbg==';
+
+/** One POST through the real app. `row` is what the (hash, proof) lookup answers (or nothing). Returns the response and the INSERT params. */
+async function drive(url: string, body: unknown, row: Record<string, unknown> | null = null, tsaReply: Record<string, unknown> | null = null) {
+  const nodeCrypto = await import('crypto');
+  const { privateKey, publicKey } = nodeCrypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+  const b64url = (s: string | Buffer) => Buffer.from(s).toString('base64url');
+  const signingInput = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) + '.' + b64url(JSON.stringify({ userId: 'u-ks1516', email: 'ks1516@secuura.io', role: 'user', verificationLevel: 'email', exp: Math.floor(Date.now() / 1000) + 300 }));
+  const bearer = 'Bearer ' + signingInput + '.' + b64url(nodeCrypto.sign('sha256', Buffer.from(signingInput), privateKey));
+  const saved = { JWT_PUBLIC_KEY: process.env.JWT_PUBLIC_KEY, PORT: process.env.PORT };
+  process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
+  process.env.PORT = '0';
+  const queries: Array<[string, unknown[]]> = [];
+  vi.doMock('../db', () => ({
+    initDb: async () => true, isDbAvailable: () => true, closeDb: async () => undefined,
+    query: async (sql: string, params?: unknown[]) => {
+      queries.push([sql, params || []]);
+      return /FROM ts_timestamps WHERE hash = \$1 AND proof = \$2/.test(sql) && row ? { rows: [row], rowCount: 1 } : { rows: [], rowCount: 0 };
+    },
+  }));
+  if (tsaReply) {
+    vi.doMock('../tsa/qualified-tsa', async (importOriginal) => {
+      const actual = await importOriginal<Record<string, unknown>>();
+      return { ...actual, createTimestamp: async () => ({ success: true, timestamp: new Date().toISOString(), serialNumber: 'ab', provider: 'P', ...tsaReply }) };
+    });
+  }
+  vi.resetModules();
+  const { default: app } = await import('../index');
+  const out = await new Promise<any>((resolve) => {
+    const headers: Record<string, unknown> = {};
+    const req: any = { method: 'POST', url, headers: { authorization: bearer }, body };
+    const res: any = { statusCode: 200, locals: {}, on: () => res, status: (c: number) => { res.statusCode = c; return res; }, json: (b: unknown) => { resolve({ status: res.statusCode, body: b }); return res; } };
+    res.send = res.json; res.end = () => res.json(null);
+    res.setHeader = (k: string, v: unknown) => { headers[k.toLowerCase()] = v; return res; };
+    res.getHeader = (k: string) => headers[k.toLowerCase()]; res.removeHeader = (k: string) => { delete headers[k.toLowerCase()]; };
+    app(req, res, () => resolve({ status: -1, body: null }));
+  });
+  for (const k of ['JWT_PUBLIC_KEY', 'PORT'] as const) { if (saved[k] === undefined) delete process.env[k]; else process.env[k] = saved[k]; }
+  const inserts = queries.filter(([sql]) => sql.trimStart().startsWith('INSERT INTO ts_timestamps')).map(([, p]) => ({ type: p[4], verified: p[9], verifiedAtIsDate: p[10] instanceof Date }));
+  return { ...out, inserts };
+}
+
+const storedRow = (type: string, proof: string, over: Record<string, unknown> = {}) => ({
+  id: 'ts_1516', document_id: null, hash: HASH, hash_algorithm: 'sha256', timestamp_type: type, proof,
+  tsa_url: null, created_at: NOW, verified: true, verified_at: NOW, eidas_qualified: false, tsa_name: null, ...over,
+});
+const create = (timestampType: string) => ({ hash: HASH, timestampType });
+const verify = (timestampType: string, proof: string) => ({ hash: HASH, proof, timestampType });
+
+describe('KS-1516 creation reports verified:false for the two placeholder types', () => {
+  it('RED ks1516 R1 opentimestamps: creation answers 201 verified:false and INSERTs verified false with no verified_at', async () => {
+    const r = await drive('/api/timestamps', create('opentimestamps'));
+    expect([r.status, r.body.data.verified, r.inserts]).toEqual([201, false, [{ type: 'opentimestamps', verified: false, verifiedAtIsDate: false }]]);
+  });
+
+  it('RED ks1516 R2 blockchain: creation answers 201 verified:false and INSERTs verified false with no verified_at', async () => {
+    const r = await drive('/api/timestamps', create('blockchain'));
+    expect([r.status, r.body.data.verified, r.inserts]).toEqual([201, false, [{ type: 'blockchain', verified: false, verifiedAtIsDate: false }]]);
+  });
+
+  it('control ks1516 C1 rfc3161 with a real token is unchanged: verified:true with a verified_at date', async () => {
+    const r = await drive('/api/timestamps', create('rfc3161'), null, { token: REAL_TOKEN, tsaName: 'Real TSA', eidasQualified: true });
+    expect([r.status, r.body.data.verified, r.inserts]).toEqual([201, true, [{ type: 'rfc3161', verified: true, verifiedAtIsDate: true }]]);
+  });
+});
+
+describe('KS-1516 /api/timestamps/verify answers verified:false for the two placeholder types, with or without a stored row', () => {
+  it('RED ks1516 R3 opentimestamps: a forged proof (right hash plus one attestation) with no stored row is not verified', async () => {
+    const r = await drive('/api/timestamps/verify', verify('opentimestamps', FORGED_OTS));
+    expect([r.status, r.body.data.verified]).toEqual([200, false]);
+  });
+
+  it('RED ks1516 R4 blockchain: a forged proof (right hash plus chain and slot) with no stored row is not verified', async () => {
+    const r = await drive('/api/timestamps/verify', verify('blockchain', FORGED_CHAIN));
+    expect([r.status, r.body.data.verified]).toEqual([200, false]);
+  });
+
+  it('RED ks1516 R5 opentimestamps: even a stored row whose verified column is true does not verify', async () => {
+    const r = await drive('/api/timestamps/verify', verify('opentimestamps', FORGED_OTS), storedRow('opentimestamps', FORGED_OTS));
+    expect([r.status, r.body.data.verified]).toEqual([200, false]);
+  });
+
+  it('RED ks1516 R6 blockchain: even a stored row whose verified column is true does not verify', async () => {
+    const r = await drive('/api/timestamps/verify', verify('blockchain', FORGED_CHAIN), storedRow('blockchain', FORGED_CHAIN));
+    expect([r.status, r.body.data.verified]).toEqual([200, false]);
+  });
+
+  it('control ks1516 C2 opentimestamps: a proof with no attestations is not verified (already so at the tip)', async () => {
+    const r = await drive('/api/timestamps/verify', verify('opentimestamps', OTS_NO_ATTESTATION));
+    expect([r.status, r.body.data.verified]).toEqual([200, false]);
+  });
+
+  it('control ks1516 C3 rfc3161: a stored row marked verified still verifies (unchanged)', async () => {
+    const r = await drive('/api/timestamps/verify', verify('rfc3161', REAL_TOKEN), storedRow('rfc3161', REAL_TOKEN, { tsa_name: 'Real TSA', eidas_qualified: true }));
+    expect([r.status, r.body.data.verified]).toEqual([200, true]);
+  });
+
+  it('control ks1516 C4 rfc3161: a forged token with no stored row is still not verified (KS-1404, unchanged)', async () => {
+    const r = await drive('/api/timestamps/verify', verify('rfc3161', FORGED_OTS));
+    expect([r.status, r.body.data.verified]).toEqual([200, false]);
+  });
+});
```
