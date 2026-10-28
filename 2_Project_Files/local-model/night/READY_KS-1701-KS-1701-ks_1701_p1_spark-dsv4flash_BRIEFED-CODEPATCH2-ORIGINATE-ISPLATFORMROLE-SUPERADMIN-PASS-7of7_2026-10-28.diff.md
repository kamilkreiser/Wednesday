# READY — KS-1701-KS-1701-ks_1701_p1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker/patch.diff`** (from `ls` at 16:10 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker/section_3.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker/section_4.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/routes/documents.ts b/Blockchain/Dev/services/originate/src/routes/documents.ts' vs '+++ --- a/Blockchain/Dev/services/originate/src/routes/documents.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/originate/src/routes/documents.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts' vs '+++ --- a/Blockchain/Dev/services/originate/src/routes/certifications.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/originate/src/routes/certifications.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 3: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)] [section 4: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts b/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts' vs '+++ --- a/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/originate/src/routes/documents.ts): `error: patch failed: Blockchain/Dev/services/originate/src/routes/documents.ts:297`; section 2 (Blockchain/Dev/services/originate/src/routes/certifications.ts): `error: patch failed: Blockchain/Dev/services/originate/src/routes/certifications.ts:961` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:10 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/documents.ts , Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts , Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/documents.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts` (test) — equal to numstat.out's set (4 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/originate/src/routes/documents.ts
2	2	Blockchain/Dev/services/originate/src/routes/certifications.ts
54	0	Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts
3	1	Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (5 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: documents.ts certifications.ts`
- CODE_PATCH2 (rung 3, 2 product files + 2 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/documents.ts`, `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/documents.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/routes/certifications.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts 54 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts 3 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=4 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/documents.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/originate/src/routes/documents.ts:297`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_2.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/originate/src/routes/certifications.ts:961`)
- section 3 `section_3.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- section 4 `section_4.diff` → `Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts` (hunks=1, miscount=0; applied file per `section_4.opts`: `section_4.diff`, git-apply options: `(none — strict)`; `apply_check_strict_4.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=5 of total=9; red cell(s): ['KS-1701: platform-admin checks in originate use isPlatformRole RED KS-1701 R1 documents.ts keeps no hand-written system_admin comparison', 'KS-1701: platform-admin checks in originate use isPlatformRole RED KS-1701 R2 certifications.ts keeps no hand-written system_admin comparison', 'KS-1701: platform-admin checks in originate use isPlatformRole RED KS-1701 R3 documents.ts imports isPlatformRole from the shared package', 'KS-1701: platform-admin checks in originate use isPlatformRole RED KS-1701 R4 documents.ts calls isPlatformRole at the list scoping and at the by-id read', 'KS-1701: platform-admin checks in originate use isPlatformRole RED KS-1701 R5 certifications.ts calls isPlatformRole at the list scoping and at callerMayCertifyDocument']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1698 failed=0 | after: total=1707 failed=0` · `NEW reds: []` [baseline_suite.json total=1698 failed=0; after_suite.json total=1707 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=4 products=2 tests=2 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/documents.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts` (+54/-0); 4 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/documents.ts, Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 3 `section_3.diff`: `git apply -p1` (strict); section 4 `section_4.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1701): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1701_p1/KS-1701.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/documents.ts b/Blockchain/Dev/services/originate/src/routes/documents.ts
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -45,7 +45,7 @@
 import { DEFAULT_DOCUMENT_TYPE } from '@secuura/shared/documents/default-type';
 // KS-1402: + lookupHash. transfer-custody hashes a holder email itself now; before KS-1402 it
 // forwarded the caller's credential to auth's /api/users/lookup, which did the hashing.
-import { verifyMessageSignature, hasNulByte, runWithTenantId, lookupHash, signEmitterHop } from '@secuura/shared';
+import { verifyMessageSignature, hasNulByte, runWithTenantId, lookupHash, signEmitterHop, isPlatformRole } from '@secuura/shared';
 import { mintAndRegisterThreadToken } from '../services/threadTokenClient';
 import { pollAnchorUntilConfirmed, reconcileDocumentAnchorState } from '../services/anchorStateSync';
 import { simulatedFieldsFromAnchor, composeHonestBlockchainBlob } from '../services/anchorHonesty';
@@ -297,4 +297,4 @@
       const user = (req as any).user;
       const userId = user?.userId as string | undefined;
       const userRole = user?.role as string | undefined;
-      const isAdmin = userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin';
+      const isAdmin = isPlatformRole(userRole);
@@ -1098,7 +1098,7 @@
       // Cross-tenant fallback: only for admins — search the platform_document_registry
       // Pen-test F-04: read role from authenticated req.user, NOT raw headers.
       const userRole = (req as any).user?.role as string | undefined;
-      const isAdmin = userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin';
+      const isAdmin = isPlatformRole(userRole);
       // BUG-ISOLATION-001 fix (2026-05-02): if the admin explicitly set
       // X-Tenant-Override (i.e., effective tenant ≠ JWT tenant), they
       // are scoped to that override and the cross-tenant fallback MUST
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -120,7 +120,7 @@
 async function callerMayCertifyDocument(req: Request, userId: string, document: DocumentRecord): Promise<boolean> {
   const authUser = (req as any).user;
   const role = authUser?.role as string | undefined;
-  if (role === 'system_admin' || role === 'SYSTEM_ADMIN' || role === 'super_admin') return true;
+  if (isPlatformRole(role)) return true;
   if (document.owner?.id && document.owner.id === userId) return true;
   const email = authUser?.email;
   const recipientEmail = (document.data as Record<string, unknown> | undefined)?.recipientEmail;
@@ -961,4 +961,4 @@
       const user = (req as any).user;
       const userId = user?.userId as string | undefined;
       const userRole = user?.role as string | undefined;
-      const isAdmin = userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin';
+      const isAdmin = isPlatformRole(userRole);
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts
@@ -0,0 +1,54 @@
+// KS-1701 (originate routes/documents.ts and routes/certifications.ts): four places answered "is this caller a platform administrator?" with a hand-written literal that names
+// system_admin, SYSTEM_ADMIN and super_admin and omits SUPER_ADMIN, so a platform administrator whose token carries that casing was treated as an ordinary user. The repo's own predicate
+// isPlatformRole (packages/shared) upper-cases the claim and covers every spelling; the certification by-id read already uses it. These cells read the two route files as text (no app
+// boot, no database) and pin that no hand-written role literal is left in either file, that documents.ts imports the predicate, and the number of call sites in each file.
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const DOCUMENTS = readFileSync(join(__dirname, '..', 'routes', 'documents.ts'), 'utf8');
+const CERTIFICATIONS = readFileSync(join(__dirname, '..', 'routes', 'certifications.ts'), 'utf8');
+
+/** The number of non-overlapping occurrences of `needle` in `text`. */
+function count(text: string, needle: string): number {
+  return text.split(needle).length - 1;
+}
+
+describe('KS-1701: platform-admin checks in originate use isPlatformRole', () => {
+  it('RED KS-1701 R1 documents.ts keeps no hand-written system_admin comparison', () => {
+    expect(count(DOCUMENTS, "=== 'system_admin'")).toBe(0);
+  });
+
+  it('RED KS-1701 R2 certifications.ts keeps no hand-written system_admin comparison', () => {
+    expect(count(CERTIFICATIONS, "=== 'system_admin'")).toBe(0);
+  });
+
+  it('RED KS-1701 R3 documents.ts imports isPlatformRole from the shared package', () => {
+    expect(DOCUMENTS).toMatch(/import \{[^}]*\bisPlatformRole\b[^}]*\} from '@secuura\/shared';/);
+  });
+
+  it('RED KS-1701 R4 documents.ts calls isPlatformRole at the list scoping and at the by-id read', () => {
+    expect(count(DOCUMENTS, 'isAdmin = isPlatformRole(userRole);')).toBe(2);
+  });
+
+  it('RED KS-1701 R5 certifications.ts calls isPlatformRole at the list scoping and at callerMayCertifyDocument', () => {
+    expect(count(CERTIFICATIONS, 'isAdmin = isPlatformRole(userRole);')).toBe(1);
+    expect(count(CERTIFICATIONS, 'if (isPlatformRole(role)) return true;')).toBe(1);
+  });
+
+  it('control KS-1701 C1 certifications.ts still imports isPlatformRole exactly once', () => {
+    expect(count(CERTIFICATIONS, "import { isPlatformRole } from '@secuura/shared';")).toBe(1);
+  });
+
+  it('control KS-1701 C2 the certification by-id read helper still calls isPlatformRole on the authenticated role', () => {
+    expect(CERTIFICATIONS).toContain('if (isPlatformRole(authUser?.role as string | undefined)) return true;');
+  });
+
+  it('control KS-1701 C3 callerMayCertifyDocument still checks the owner', () => {
+    expect(CERTIFICATIONS).toContain('  if (document.owner?.id && document.owner.id === userId) return true;');
+  });
+
+  it('control KS-1701 C4 documents.ts still imports sanitizeString and the other shared names it had', () => {
+    expect(DOCUMENTS).toContain("import { sanitizeString } from '@secuura/shared/security';");
+    expect(DOCUMENTS).toContain('verifyMessageSignature, hasNulByte, runWithTenantId, lookupHash, signEmitterHop');
+  });
+});
diff --git a/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts b/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts
--- a/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts
@@ -28,5 +28,7 @@
   const base: Record<string, unknown> = {};
   for (const key of Object.keys(actual)) {
     const value = actual[key];
-    base[key] = typeof value === 'function' ? jest.fn() : value;
+    // KS-1701: isPlatformRole is a pure predicate over a role string. An inert jest.fn() answers undefined for every caller, which would turn every platform admin into an ordinary user in a suite
+    // that exercises an admin path through this mock, so it stays the real function (the only function export kept real).
+    base[key] = typeof value === 'function' && key !== 'isPlatformRole' ? jest.fn() : value;
   }
```


## DECISION NOTE (source-read, Spark operator 3 for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: golden.diff vs brief line by line, and vs originate `routes/documents.ts` (:48 import, :300, :1101), `routes/certifications.ts` (:123, :964) and `__tests__/helpers/sharedModuleMock.ts` at base. Each hand-written `role === 'system_admin' || 'SYSTEM_ADMIN' || 'super_admin'` becomes `isPlatformRole(<same variable>)`; `isPlatformRole` (shared keyRevokePolicy.ts:140) is `PLATFORM_ROLES.has(String(role || '').toUpperCase())`, so every spelling the literal accepted is still accepted. The shared test helper keeps `isPlatformRole` real (without it the mock turns it into an inert jest.fn and 52 existing tests go red: that is why the helper is a fourth file).
- DECISION for Wednesday (access WIDENS): the ticket is facts-only ('no remedy proposed'); calling `isPlatformRole` is the drafter's fix shape. After this PR a caller whose token role is `SUPER_ADMIN`, or any mixed-case spelling of system_admin/super_admin, is a platform administrator at four originate sites (documents LIST scoping, GET /api/documents/:id cross-tenant fallback, certifications LIST scoping, callerMayCertifyDocument). Nothing is narrowed. Wednesday/owner must rule that widening is wanted before the PR opens (KS-1695 shows the same omission was a measured regression, but that is evidence for the direction, not a ruling).
- Apply mode: NOT STRICT. Sections 1 and 2 (documents.ts, certifications.ts) were applied with `--recount --ignore-whitespace -C1` (strict `git apply --check` fails on the short-context hunks, e.g. `patch failed: ...documents.ts:297`); sections 3 and 4 (the new test, the helper) strict. Whole-patch lenient `git apply --check --recount --ignore-whitespace -C1` passes at develop bd6697e0. STRICT APPLY NOT CLAIMED.
- Interplay: ks_1591_p1 (packages/shared isPlatformRole ASCII fold) changes the predicate this PR calls; the files are disjoint, either order, but the raise seat must say so in both PR bodies.
- SEQUENCE: no shared file with any other held pass; 0 overlaps with the 14 open PRs.
- Verdict: HOLD-WITH-DECISION.
