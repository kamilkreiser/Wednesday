# READY — KS-1659-HOLDERFOLD-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1/out.md.checker/patch.diff`** (from `ls` at 09:52 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:52 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `89956fe92956a810f6821fdee09915f087feea7b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts , Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
117	0	Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts fails at the untouched tip (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-1659 the certification write folds the HOLDER principal as it folds the issuer RED KS-1659 R1: saveCertification resolves for a connector caller who named no holder (issuer and holder are the same connector principal)', 'KS-1659 the certification write folds the HOLDER principal as it folds the issuer RED KS-1659 R2: the connector holder is bound to owner_user_id as NULL, not as the principal string', 'KS-1659 the certification write folds the HOLDER principal as it folds the issuer RED KS-1659 R3: reserveCertificationRow, which shares the INSERT, resolves for a connector holder as well']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1568 failed=0 | after: total=1575 failed=0` · `NEW reds: []` [baseline_suite.json total=1568 failed=0; after_suite.json total=1575 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +118/-1 test=src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts` (+117/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `89956fe92956a810f6821fdee09915f087feea7b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1659_p1/KS-1659.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1659_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts b/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
index e216d8717..919de2f78 100644
--- a/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
+++ b/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
@@ -248,7 +248,7 @@
       ${'SHA-256'},
       ${toDbStatus(cert.status)},
       ${issuerUserId}::uuid,
-      ${cert.holder.id}::uuid,
+      ${toActorUuid(cert.holder.id)}::uuid,
       ${cert.holder.did || null},
       ${JSON.stringify({})}::jsonb,
       ${certMeta}::jsonb,
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts
new file mode 100644
index 000000000..ac0ce942e
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1659-a-connector-certifying-with-no-holder.test.ts
@@ -0,0 +1,117 @@
+/**
+ * KS-1659 - a connector certifying with no holderId must not throw 22P02 at the holder's `::uuid` cast.
+ *
+ * KS-564 folded the ISSUER principal (`connector:platform-s:<ref>`, not a UUID) with toActorUuid before binding it to a `::uuid`
+ * column, and left the HOLDER raw in the same INSERT. A certification with no holderId defaults the holder to the caller's own
+ * principal, so a connector caller bound the principal string to documents.owner_user_id and Postgres refused it (22P02), which the route
+ * reports as the client's unstorable payload. After this change the holder is folded the same way: NULL in the UUID column, while the raw
+ * principal stays in certification_metadata.holderId, exactly as the issuer's does.
+ *
+ * The database stand-in is FAITHFUL on the one property that matters: it refuses a non-UUID value bound to a `::uuid` placeholder with
+ * Postgres's own message, and it records every binding before it refuses.
+ */
+
+const mockExecuteRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: jest.fn(),
+    $executeRaw: mockExecuteRaw,
+  },
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import { saveCertification, reserveCertificationRow, Certification } from '../repositories/certificationRepo';
+
+const TENANT = 'a0000000-0000-4000-8000-000000000001';
+const CERT_ID = 'c0000000-0000-4000-8000-0000000000c1';
+const HUMAN_ISSUER = 'a0000000-0000-4000-8000-000000000010';
+const HUMAN_HOLDER = 'b0000000-0000-4000-8000-000000000020';
+const CONNECTOR = 'connector:platform-s:38d85754-17ee-4c28-8ca7-467a58f98cc3';
+const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
+
+// The documents INSERT binds (id, tenant, title, type, hash, algorithm, status, ISSUER, HOLDER, did, '{}', certMeta, ...).
+const ISSUER_AT = 7;
+const HOLDER_AT = 8;
+const CERT_META_AT = 11;
+
+type Bound = { sql: string; values: unknown[] };
+let calls: Bound[] = [];
+
+beforeEach(() => {
+  calls = [];
+  mockExecuteRaw.mockReset();
+  mockExecuteRaw.mockImplementation(async (strings: TemplateStringsArray, ...values: unknown[]) => {
+    calls.push({ sql: strings.join('?'), values });
+    values.forEach((v, i) => {
+      if (strings[i + 1].startsWith('::uuid') && v !== null && !UUID_RE.test(String(v))) {
+        throw new Error(`Raw query failed. Code: 22P02. Message: invalid input syntax for type uuid: "${String(v)}"`);
+      }
+    });
+    return 1;
+  });
+});
+
+function cert(issuerId: string, holderId: string): Certification {
+  return {
+    id: CERT_ID,
+    type: 'verification_certificate',
+    status: 'issued',
+    issuer: { id: issuerId, name: 'Issuer' },
+    holder: { id: holderId, name: 'Holder' },
+    data: { title: 'A certificate' },
+    issuedAt: '2026-10-20T00:00:00.000Z',
+    contentHash: 'a'.repeat(64),
+  } as unknown as Certification;
+}
+
+const documentsInsert = (): Bound => calls.find((c) => c.sql.includes('INSERT INTO documents')) as Bound;
+
+describe('KS-1659 the certification write folds the HOLDER principal as it folds the issuer', () => {
+  it('RED KS-1659 R1: saveCertification resolves for a connector caller who named no holder (issuer and holder are the same connector principal)', async () => {
+    const c = cert(CONNECTOR, CONNECTOR);
+    await expect(saveCertification(c, TENANT)).resolves.toBe(c);
+  });
+
+  it('RED KS-1659 R2: the connector holder is bound to owner_user_id as NULL, not as the principal string', async () => {
+    await saveCertification(cert(CONNECTOR, CONNECTOR), TENANT).catch(() => undefined);
+    expect(documentsInsert().values[HOLDER_AT]).toBeNull();
+  });
+
+  it('RED KS-1659 R3: reserveCertificationRow, which shares the INSERT, resolves for a connector holder as well', async () => {
+    await expect(reserveCertificationRow(cert(CONNECTOR, CONNECTOR), TENANT)).resolves.toBeUndefined();
+  });
+
+  it('CONTROL KS-1659 C1: a human holder UUID is still bound unchanged and the write resolves', async () => {
+    const c = cert(HUMAN_ISSUER, HUMAN_HOLDER);
+    await expect(saveCertification(c, TENANT)).resolves.toBe(c);
+    expect(documentsInsert().values[HOLDER_AT]).toBe(HUMAN_HOLDER);
+    expect(documentsInsert().values[ISSUER_AT]).toBe(HUMAN_ISSUER);
+  });
+
+  it('CONTROL KS-1659 C2: the connector ISSUER is still folded to NULL (KS-564) and a human holder beside it is untouched', async () => {
+    const c = cert(CONNECTOR, HUMAN_HOLDER);
+    await expect(saveCertification(c, TENANT)).resolves.toBe(c);
+    expect(documentsInsert().values[ISSUER_AT]).toBeNull();
+    expect(documentsInsert().values[HOLDER_AT]).toBe(HUMAN_HOLDER);
+  });
+
+  it('CONTROL KS-1659 C3: the raw connector principal still reaches certification_metadata as issuerId and holderId, so attribution survives the fold', async () => {
+    await saveCertification(cert(CONNECTOR, CONNECTOR), TENANT).catch(() => undefined);
+    const meta = JSON.parse(String(documentsInsert().values[CERT_META_AT]));
+    expect(meta.issuerId).toBe(CONNECTOR);
+    expect(meta.holderId).toBe(CONNECTOR);
+  });
+
+  it('CONTROL KS-1659 C4: the stand-in refuses a non-UUID bound to a uuid cast, so the cells above can fail for the real reason', async () => {
+    await expect(
+      (mockExecuteRaw as unknown as (s: TemplateStringsArray, ...v: unknown[]) => Promise<number>)(
+        Object.assign(['SELECT ', '::uuid'], { raw: ['SELECT ', '::uuid'] }) as unknown as TemplateStringsArray,
+        'not-a-uuid',
+      ),
+    ).rejects.toThrow(/22P02/);
+  });
+});
```
