# READY — KS-758-UNRESOLVEDERASURELOG-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_758_p1/out.md.checker/patch.diff`** (from `ls` at 10:23 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_758_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_758_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_758_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in gdprService.ts (run 11 vs golden 14 body lines — context, since the change lines are equal) (identical in ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 10:23 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_758_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cd63883c62a9bb0e66969df8cd3f02db2b9b2217`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/services/gdprService.ts , Blockchain/Dev/services/originate/src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/gdprService.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	0	Blockchain/Dev/services/originate/src/services/gdprService.ts
181	0	Blockchain/Dev/services/originate/src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (9 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 9 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/services/gdprService.ts byte-exact incl. leading whitespace (apply mode strict): OK 9 line(s) byte-exact incl. leading whitespace (of 9; 9 line(s) added by the apply)` [a3i_indent.out: `OK 9 line(s) byte-exact incl. leading whitespace (of 9; 9 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/gdprService.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts fails at the untouched tip (5 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=5 of total=9; red cell(s): ['KS-758 F9: an unresolvable connector erasure leaves an audit row RED KS-758 R1: blanking provenance for an unresolved ref writes one data_deletion_log row of the five-column shape', 'KS-758 F9: an unresolvable connector erasure leaves an audit row RED KS-758 R2: records_affected is what the blank reported, not the count read before it', 'KS-758 F9: an unresolvable connector erasure leaves an audit row RED KS-758 R3: the reason names the external ref, the tenant and that no users row resolved', 'KS-758 F9: an unresolvable connector erasure leaves an audit row RED KS-758 R4: the audit row is written after the blank it describes', 'KS-758 F9: an unresolvable connector erasure leaves an audit row RED KS-758 R5: a failing audit write fails the request instead of being swallowed']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts passes with the product hunk (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1568 failed=0 | after: total=1577 failed=0` · `NEW reds: []` [baseline_suite.json total=1568 failed=0; after_suite.json total=1577 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +190/-0 test=src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/gdprService.ts` (+9/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts` (+181/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cd63883c62a9bb0e66969df8cd3f02db2b9b2217` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_758_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_758_p1/KS-758.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_758_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/services/gdprService.ts
+++ b/Blockchain/Dev/services/originate/src/services/gdprService.ts
@@ -1488,2 +1488,11 @@
     });
+    // KS-758 F9. This branch erases identity from rows no users row owns, and it was the one place a connector erasure left no
+    // data_deletion_log entry, so nothing recorded that K erased anything for a subject it holds no user for. user_id and dsr_id
+    // stay NULL (both columns are nullable): there is neither a users row nor a DSR here. Written after the blank, with its count.
+    await prisma.$executeRaw`
+      INSERT INTO data_deletion_log (data_type, records_affected, deletion_method, reason, performed_by)
+      VALUES (${'action_provenance'}, ${blanked}, ${'anonymize'},
+        ${`KS-758: connector erasure blanked provenance identity for external_ref ${externalRef} in tenant ${tenantId}; no users row resolved`},
+        ${`connector:${connectorId}`})
+    `;
     return { status: 'completed' as const, alreadyErased: false };
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts
@@ -0,0 +1,181 @@
+/**
+ * KS-758 F9 - a connector erasure of an UNRESOLVABLE external_ref must leave an audit row.
+ *
+ * executeErasureByExternalRef has a branch for a ref that resolves to no users row: it blanks the identity columns of the
+ * action_provenance rows that carry the ref and answers `completed`. That was the one branch that wrote nothing to
+ * data_deletion_log, so nothing recorded that K erased anything for a subject it holds no user for. The resolvable branch
+ * records its steps through executeErasureImpl; this branch now records one row of its own (user_id and dsr_id stay NULL: there is
+ * neither a users row nor a DSR here).
+ *
+ * The cells read the statements the service hands to the mocked database, the way ks695-erasure-by-external-ref.test.ts does.
+ */
+
+const mockQueryRaw = jest.fn();
+const mockExecuteRaw = jest.fn();
+
+jest.mock('../db', () => ({ prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw } }));
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    publishEvent: jest.fn().mockResolvedValue(undefined),
+    EventTypes: { USER_ERASED: 'user.erased' },
+    encryptField: jest.fn((v: string) => v),
+    decryptField: jest.fn((v: string) => v),
+    encryptFieldWithDek: jest.fn((v: string) => v),
+    decryptFieldWithDek: jest.fn((v: string) => v),
+    isSubjectDekCiphertext: jest.fn(() => false),
+    isEncryptedPii: jest.fn(() => false),
+    runWithPlatformScope: jest.fn(<T,>(fn: () => T): T => fn()),
+    normaliseOrgId: jest.requireActual('@secuura/shared').normaliseOrgId,
+    SubjectDekProvider: class {
+      getOrCreateDek = async () => Buffer.alloc(32);
+      getDek = async () => null;
+      destroyDek = async () => 'destroyed' as const;
+      evict = () => undefined;
+    },
+  }),
+);
+jest.mock('../services/subjectDeks', () => ({
+  subjectDeks: {
+    getOrCreateDek: jest.fn(async () => Buffer.alloc(32)),
+    getDek: jest.fn(async () => null),
+    destroyDek: jest.fn().mockResolvedValue('destroyed'),
+    evict: jest.fn(),
+  },
+}));
+jest.mock('../events', () => ({
+  publishEvent: jest.fn().mockResolvedValue(undefined),
+  EventTypes: { USER_ERASED: 'user.erased' },
+}));
+
+import { executeErasureByExternalRef } from '../services/gdprService';
+
+function sqlOf(call: unknown[]): string {
+  return (call[0] as readonly string[]).join(' ? ').replace(/\s+/g, ' ').trim();
+}
+function valuesOf(call: unknown[]): unknown[] {
+  return call.slice(1);
+}
+
+const EXTERNAL_REF = 'person-guid-ks758';
+const TENANT = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
+const USER = '11111111-1111-1111-1111-111111111111';
+const CONNECTOR = 'platform-s:org-guid';
+
+/** Wire the reads by the SQL they carry; the executeRaw mock answers the blank with `blankReturns` rows. */
+function wire(opts: { resolved?: string | null; provenanceRows?: number; unerased?: number; blankReturns?: number; failLog?: boolean }) {
+  const { resolved = null, provenanceRows = 3, unerased = 3, blankReturns = 3, failLog = false } = opts;
+  mockQueryRaw.mockImplementation((...call: unknown[]) => {
+    const sql = sqlOf(call);
+    if (/SELECT resolved_user_id, email_hash FROM action_provenance/i.test(sql)) {
+      return Promise.resolve(Array.from({ length: provenanceRows }, (_, i) => ({
+        resolved_user_id: i === 0 ? resolved : null,
+        email_hash: null,
+      })));
+    }
+    if (/COUNT\(\*\)::bigint AS n FROM action_provenance/i.test(sql)) return Promise.resolve([{ n: BigInt(unerased) }]);
+    if (/FROM data_subject_requests .*status NOT IN \('completed', 'denied'\)/i.test(sql)) return Promise.resolve([]);
+    if (/FROM data_subject_requests .*status IN \('completed', 'denied'\)/i.test(sql)) return Promise.resolve([]);
+    if (/SELECT email FROM users/i.test(sql)) return Promise.resolve([{ email: 'subject@example.com' }]);
+    return Promise.resolve([{ id: 'dsr-new', type: 'erasure', user_id: USER, records_affected: 1 }]);
+  });
+  mockExecuteRaw.mockImplementation((...call: unknown[]) => {
+    const sql = sqlOf(call);
+    if (/INSERT INTO data_deletion_log/i.test(sql)) {
+      return failLog ? Promise.reject(new Error('simulated audit write failure')) : Promise.resolve(1);
+    }
+    if (/UPDATE action_provenance SET/i.test(sql)) return Promise.resolve(blankReturns);
+    return Promise.resolve(1);
+  });
+}
+
+function logWrites() {
+  return mockExecuteRaw.mock.calls.filter((c) => /INSERT INTO data_deletion_log/i.test(sqlOf(c)));
+}
+function blankWrites() {
+  return mockExecuteRaw.mock.calls.filter((c) => /UPDATE action_provenance SET/i.test(sqlOf(c)));
+}
+
+describe('KS-758 F9: an unresolvable connector erasure leaves an audit row', () => {
+  beforeEach(() => jest.clearAllMocks());
+
+  it('RED KS-758 R1: blanking provenance for an unresolved ref writes one data_deletion_log row of the five-column shape', async () => {
+    wire({ resolved: null, provenanceRows: 3, unerased: 3, blankReturns: 3 });
+    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    expect(r).toEqual({ status: 'completed', alreadyErased: false });
+    const rows = logWrites();
+    expect(rows).toHaveLength(1);
+    expect(sqlOf(rows[0])).toMatch(/INSERT INTO data_deletion_log \(data_type, records_affected, deletion_method, reason, performed_by\) VALUES/i);
+    const v = valuesOf(rows[0]);
+    expect(v[0]).toBe('action_provenance');
+    expect(v[1]).toBe(3);
+    expect(v[2]).toBe('anonymize');
+    expect(v[4]).toBe(`connector:${CONNECTOR}`);
+  });
+
+  it('RED KS-758 R2: records_affected is what the blank reported, not the count read before it', async () => {
+    wire({ resolved: null, provenanceRows: 3, unerased: 3, blankReturns: 2 });
+    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    const rows = logWrites();
+    expect(rows).toHaveLength(1);
+    expect(valuesOf(rows[0])[1]).toBe(2);
+  });
+
+  it('RED KS-758 R3: the reason names the external ref, the tenant and that no users row resolved', async () => {
+    wire({ resolved: null });
+    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    const rows = logWrites();
+    expect(rows).toHaveLength(1);
+    const reason = String(valuesOf(rows[0])[3]);
+    expect(reason).toContain(EXTERNAL_REF);
+    expect(reason).toContain(TENANT);
+    expect(reason).toContain('no users row resolved');
+  });
+
+  it('RED KS-758 R4: the audit row is written after the blank it describes', async () => {
+    wire({ resolved: null });
+    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    const order = mockExecuteRaw.mock.calls.map((c) => sqlOf(c));
+    const blankAt = order.findIndex((s) => /UPDATE action_provenance SET/i.test(s));
+    const logAt = order.findIndex((s) => /INSERT INTO data_deletion_log/i.test(s));
+    expect(blankAt).toBeGreaterThanOrEqual(0);
+    expect(logAt).toBeGreaterThan(blankAt);
+  });
+
+  it('RED KS-758 R5: a failing audit write fails the request instead of being swallowed', async () => {
+    wire({ resolved: null, failLog: true });
+    await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT)).rejects.toThrow(/simulated audit write failure/);
+  });
+
+  it('CONTROL KS-758 C1: the identity blank itself is unchanged - same columns, scoped to the ref and the tenant', async () => {
+    wire({ resolved: null });
+    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    const blank = blankWrites();
+    expect(blank).toHaveLength(1);
+    expect(sqlOf(blank[0])).toMatch(/email_enc = NULL, display_name_enc = NULL, email_hash = NULL/i);
+    expect(valuesOf(blank[0])).toEqual([EXTERNAL_REF, TENANT]);
+  });
+
+  it('CONTROL KS-758 C2: a ref already blanked writes nothing at all, so no audit row either', async () => {
+    wire({ resolved: null, provenanceRows: 3, unerased: 0 });
+    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    expect(r).toEqual({ status: 'completed', alreadyErased: true });
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+  });
+
+  it('CONTROL KS-758 C3: a ref K has never seen writes nothing at all, so no audit row either', async () => {
+    wire({ resolved: null, provenanceRows: 0, unerased: 0 });
+    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    expect(r).toEqual({ status: 'completed', alreadyErased: true });
+    expect(mockExecuteRaw).not.toHaveBeenCalled();
+  });
+
+  it('CONTROL KS-758 C4: a resolvable subject takes the other branch and writes no row of this shape', async () => {
+    wire({ resolved: USER, provenanceRows: 1 });
+    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
+    expect(r).toEqual({ status: 'completed', alreadyErased: false });
+    expect(logWrites()).toHaveLength(0);
+  });
+});
```
