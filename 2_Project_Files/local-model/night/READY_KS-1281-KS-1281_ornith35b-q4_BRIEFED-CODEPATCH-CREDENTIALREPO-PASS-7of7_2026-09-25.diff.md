# READY — KS-1281-KS-1281 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1281-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 10:30 2026-09-25; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1281-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1281-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts): `error: corrupt patch at line 19` (apply with the options recorded in section_<k>.opts; the raise seat states which); golden not located — no identity claim is made.

**Held 10:30 2026-09-25 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1281-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts , Blockchain/Dev/services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (product) and `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	7	Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
46	0	Blockchain/Dev/services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 7.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts byte-exact incl. leading whitespace (apply mode lenient): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts: hunk 1 (@@ -28,13 +28,9 @@ async function ensureTable(): Promise<void> {) declared old=13 new=9 but actual old=12 new=8`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (hunks=1, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: corrupt patch at line 19`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts fails at the untouched tip (1 failed / 2 run; controls green; assertion reds)` [red_first.json: failed=1 of total=2; red cell(s): ['KS-1281: the VC store issues no DDL at runtime RED KS-1281 - storing a credential sends no CREATE TABLE statement to the database']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts passes with the product hunk (2 passed / 2 run)` [green_after.json: failed=0 of total=2, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=127 failed=0 | after: total=129 failed=0` · `NEW reds: []` [baseline_suite.json total=127 failed=0; after_suite.json total=129 failed=0]
- A6 [verbatim]: `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +49/-7 test=src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (+3/-7 per numstat.out) and the test file `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts` (+46/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1281-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1281-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts
@@ -28,13 +28,9 @@ async function ensureTable(): Promise<void> {
   if (tableEnsured) return;
   try {
-    await query(`
-      CREATE TABLE IF NOT EXISTS vc_credentials_store (
-        id    TEXT PRIMARY KEY,
-        credential JSONB NOT NULL,
-        created_at TIMESTAMPTZ DEFAULT NOW()
-      )
-    `);
+    // KS-1281: migration 001 owns vc_credentials_store and the runtime role has no CREATE on schema public,
+    // so this is an existence check only - no DDL at runtime.
+    await query('SELECT 1 FROM vc_credentials_store LIMIT 0');
     tableEnsured = true;
   } catch (err: any) {
     logger.warn('Could not ensure vc_credentials_store table', { error: err?.message });
--- /dev/null
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts
@@ -0,0 +1,46 @@
+/**
+ * KS-1281: credentialRepo.ensureTable() ran CREATE TABLE IF NOT EXISTS vc_credentials_store at runtime. The
+ * runtime role has no CREATE on schema public (least privilege), so every vc-issuer boot logged a WARN, and
+ * migration 001 already owns the table. The db module is mocked in the credentialRepo.test.ts shape, with the
+ * database reported AVAILABLE, and every statement the repository sends is read back from the query mock.
+ */
+import { describe, it, expect, vi } from 'vitest';
+
+vi.mock('../db', () => ({
+  isDbAvailable: vi.fn(() => true),
+  query: vi.fn(async () => ({ rows: [], rowCount: 0 })),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+import * as db from '../db';
+import * as repo from '../repositories/credentialRepo';
+
+const sentSql = (): string[] => (db.query as any).mock.calls.map((c: unknown[]) => String(c[0]));
+
+function credential(id: string) {
+  return {
+    '@context': ['https://www.w3.org/2018/credentials/v1'],
+    id,
+    type: ['VerifiableCredential', 'SecuuraCredential'],
+    issuer: { id: 'did:secuura:issuer-1281', name: 'Issuer' },
+    issuanceDate: '2026-09-25T00:00:00.000Z',
+    credentialSubject: { id: 'did:secuura:holder-1281', documentHash: 'sha256:ks1281' },
+    credentialStatus: { id: 'urn:status:1281', type: 'StatusList2021', revoked: false },
+    proof: { type: 'Ed25519Signature2020', created: '2026-09-25', verificationMethod: 'did:secuura:issuer-1281#k', proofPurpose: 'assertionMethod', proofValue: 'z1281' },
+  } as any;
+}
+
+describe('KS-1281: the VC store issues no DDL at runtime', () => {
+  it('RED KS-1281 - storing a credential sends no CREATE TABLE statement to the database', async () => {
+    await repo.store(credential('urn:vc:ks1281-a'));
+    expect(sentSql().filter((s) => s.toUpperCase().includes('CREATE TABLE'))).toEqual([]);
+  });
+
+  it('CONTROL - the credential row itself still reaches vc_credentials_store', async () => {
+    await repo.store(credential('urn:vc:ks1281-b'));
+    expect(sentSql().some((s) => s.includes('INSERT INTO vc_credentials_store'))).toBe(true);
+  });
+});
```
