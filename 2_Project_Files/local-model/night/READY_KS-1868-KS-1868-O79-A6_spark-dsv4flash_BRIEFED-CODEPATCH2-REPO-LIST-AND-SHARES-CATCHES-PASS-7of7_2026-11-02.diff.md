# READY — KS-1868-KS-1868-O79-A6 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 17:30 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:30 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `829233f1a388b943a9fd59c40e42332c27d9066b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
92	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certificationRepo.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts 92 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=6 of total=10; red cell(s): ['KS-1868 certificationRepo listCertifications reads the thrown value safely RED ks1868 R1 listCertifications: a revoked Proxy is logged as a constant reason and re-thrown unchanged', 'KS-1868 certificationRepo listCertifications reads the thrown value safely RED ks1868 R2 listCertifications: an Error whose message getter throws is logged as a constant reason and re-thrown unchanged', 'KS-1868 certificationRepo listCertifications reads the thrown value safely RED ks1868 R3 listCertifications: an Error whose message getter returns a revoked Proxy is logged as a constant reason through the real logger and re-thrown unchanged', 'KS-1868 certificationRepo getSharesByCertification reads the thrown value safely RED ks1868 R1 getSharesByCertification: a revoked Proxy is logged as a constant reason and re-thrown unchanged', 'KS-1868 certificationRepo getSharesByCertification reads the thrown value safely RED ks1868 R2 getSharesByCertification: an Error whose message getter throws is logged as a constant reason and re-thrown unchanged', 'KS-1868 certificationRepo getSharesByCertification reads the thrown value safely RED ks1868 R3 getSharesByCertification: an Error whose message getter returns a revoked Proxy is logged as a constant reason through the real logger and re-thrown unchanged']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2163 failed=0 | after: total=2173 failed=0` · `NEW reds: []` [baseline_suite.json total=2163 failed=0; after_suite.json total=2173 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts` (+92/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `829233f1a388b943a9fd59c40e42332c27d9066b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts b/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
--- a/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
+++ b/Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
@@ -203,7 +203,13 @@
     const all = rows.map(fromDbRow);
     return { items: all, total: all.length };
   } catch (err: any) {
-    logger.warn('DB list failed', { error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = String(err instanceof Error ? err.message : err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB list failed', { error: reason });
     throw err;
   }
 }
@@ -381,7 +387,13 @@
       status: r.status,
     }));
   } catch (err: any) {
-    logger.warn('Failed to fetch shares from DB', { error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = String(err instanceof Error ? err.message : err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Failed to fetch shares from DB', { error: reason });
     throw err;
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts
@@ -0,0 +1,92 @@
+// KS-1868 (originate repositories/certificationRepo.ts, listCertifications and getSharesByCertification, gate 105 G105-F3/F5): when the query fails, each catch logs the failure as
+// `err instanceof Error ? err.message : String(err)` and then RE-THROWS the value it caught. An ordinary failure is logged once and the same Error reaches the caller. When the thrown value
+// cannot be read (a revoked Proxy makes `instanceof` throw; an Error whose `message` getter throws; one whose getter returns a hostile non-string, which the real logger cannot print) that read
+// threw INSIDE the catch, so the caller saw a TypeError in place of the value, nothing was logged, and the caller's own guard logged the TypeError text. Each catch now reads the value inside its
+// own try and logs the constant reason `unreadable thrown value`, then re-throws the same value an ordinary failure already gets. The database stand-in is passed as the `db` argument, so no
+// module-level prisma is touched, and is a plain function (a spy would inspect what it rejects with).
+const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };
+
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: jest.fn() },
+  withTenant: jest.fn(),
+}));
+
+jest.mock('../utils/logger', () => ({ logger: mockLog }));
+
+import { listCertifications, getSharesByCertification } from '../repositories/certificationRepo';
+
+const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
+const CERT_ID = 'aaaaaaaa-1111-4111-8111-111111111111';
+const UNREADABLE = 'unreadable thrown value';
+
+const CASES = [
+  { fn: 'listCertifications', context: 'DB list failed', call: (db: unknown) => listCertifications(TENANT, undefined, db as any) },
+  { fn: 'getSharesByCertification', context: 'Failed to fetch shares from DB', call: (db: unknown) => getSharesByCertification(CERT_ID, db as any) },
+];
+
+// Resolves with the value the function rejected with (compared by identity, never printed), or the marker RESOLVED.
+async function rejectedWith(c: (typeof CASES)[number], thrown: unknown): Promise<{ same: boolean; resolved: boolean }> {
+  const db = { $queryRaw: async () => { throw thrown; } };
+  try {
+    await c.call(db);
+    return { same: false, resolved: true };
+  } catch (e) {
+    return { same: e === thrown, resolved: false };
+  }
+}
+
+const revokedProxy = (): object => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const throwingMessageError = (): Error =>
+  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
+    get(): string {
+      throw new Error('ks1868 message getter threw');
+    },
+  });
+const messageGetterReturningRevokedProxy = (): Error =>
+  Object.defineProperty(new Error('ks1868 hidden'), 'message', {
+    get(): unknown {
+      return revokedProxy();
+    },
+  });
+function useRealLogger(): void {
+  const real = jest.requireActual('../utils/logger').logger;
+  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
+    t.log = (_info: unknown, next: () => void) => next();
+  });
+  mockLog.warn.mockImplementation((...a: unknown[]) => (real.warn as (...x: unknown[]) => unknown)(...a));
+}
+
+beforeEach(() => jest.clearAllMocks());
+afterEach(() => mockLog.warn.mockReset());
+
+describe.each(CASES)('KS-1868 certificationRepo $fn reads the thrown value safely', (c) => {
+  it(`control ks1868 C1 ${c.fn}: an ordinary Error is logged with its own message and re-thrown unchanged`, async () => {
+    expect(await rejectedWith(c, new Error('ks1868 ordinary'))).toEqual({ same: true, resolved: false });
+    expect(mockLog.warn.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
+  });
+
+  it(`control ks1868 C2 ${c.fn}: a thrown string is logged as itself and re-thrown unchanged, as before`, async () => {
+    expect(await rejectedWith(c, 'ks1868 plain string')).toEqual({ same: true, resolved: false });
+    expect(mockLog.warn.mock.calls).toEqual([[c.context, { error: 'ks1868 plain string' }]]);
+  });
+
+  it(`RED ks1868 R1 ${c.fn}: a revoked Proxy is logged as a constant reason and re-thrown unchanged`, async () => {
+    expect(await rejectedWith(c, revokedProxy())).toEqual({ same: true, resolved: false });
+    expect(mockLog.warn.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+
+  it(`RED ks1868 R2 ${c.fn}: an Error whose message getter throws is logged as a constant reason and re-thrown unchanged`, async () => {
+    expect(await rejectedWith(c, throwingMessageError())).toEqual({ same: true, resolved: false });
+    expect(mockLog.warn.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+
+  it(`RED ks1868 R3 ${c.fn}: an Error whose message getter returns a revoked Proxy is logged as a constant reason through the real logger and re-thrown unchanged`, async () => {
+    useRealLogger();
+    expect(await rejectedWith(c, messageGetterReturningRevokedProxy())).toEqual({ same: true, resolved: false });
+    expect(mockLog.warn.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
+  });
+});
```
