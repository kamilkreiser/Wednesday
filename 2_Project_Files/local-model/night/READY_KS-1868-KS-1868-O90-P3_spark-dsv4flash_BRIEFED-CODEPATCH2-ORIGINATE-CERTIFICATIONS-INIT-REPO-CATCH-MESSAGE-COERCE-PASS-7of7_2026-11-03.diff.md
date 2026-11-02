# READY — KS-1868-KS-1868-O90-P3 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 05:18 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts' vs '+++ --- a/Blockchain/Dev/services/originate/src/routes/certifications.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/originate/src/routes/certifications.ts: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location (hunk 1: reanchored at 70 (1 '-' / 9 '+' lines; model header -69,2 +69,10);reanchored 1/1 hunk(s);); strict rc=1 lenient rc=1 fuzzy rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/originate/src/routes/certifications.ts): `error: patch failed: Blockchain/Dev/services/originate/src/routes/certifications.ts:69` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 05:18 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/certifications.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	1	Blockchain/Dev/services/originate/src/routes/certifications.ts
121	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (9 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: certifications.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/certifications.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/certifications.ts 9 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts 121 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/certifications.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.reanchored.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/originate/src/routes/certifications.ts:69`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 certifications router: the module-load initRepo failure is logged as text for a hostile rejection value RED ks1868 R1: a revoked Proxy rejection is logged as text, as for an ordinary Error', 'KS-1868 certifications router: the module-load initRepo failure is logged as text for a hostile rejection value RED ks1868 R2: an Error whose message getter throws is logged as text, as for an ordinary Error', 'KS-1868 certifications router: the module-load initRepo failure is logged as text for a hostile rejection value RED ks1868 R3: an object with no prototype (String() throws) is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2334 failed=0 | after: total=2339 failed=0` · `NEW reds: []` [baseline_suite.json total=2334 failed=0; after_suite.json total=2339 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/certifications.ts` (+9/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts` (+121/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/certifications.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.reanchored.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/certifications.ts b/Blockchain/Dev/services/originate/src/routes/certifications.ts
--- a/Blockchain/Dev/services/originate/src/routes/certifications.ts
+++ b/Blockchain/Dev/services/originate/src/routes/certifications.ts
@@ -69,2 +69,10 @@
 // Initialize repository on module load
-initRepo().catch((err) => logger.error('Failed to init repo', { error: err instanceof Error ? err.message : String(err) }));
+initRepo().catch((err) => {
+  let reason: string;
+  try {
+    reason = err instanceof Error ? err.message : String(err);
+  } catch {
+    reason = 'unreadable thrown value';
+  }
+  logger.error('Failed to init repo', { error: reason });
+});
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts
@@ -0,0 +1,121 @@
+// KS-1868 (operator 90 screen, originate certifications router): services/originate/src/routes/certifications.ts starts the
+// repository at module load with `initRepo().catch((err) => logger.error('Failed to init repo', { error: err instanceof Error ?
+// err.message : String(err) }))` (line 70). When the rejection value cannot be read (a revoked Proxy throws on `instanceof`;
+// an Error whose message getter throws, throws on `.message`; an object with a null prototype throws in `String(...)`) the
+// arrow throws before it logs: the rejection of the `.catch` chain is unhandled (the service's unhandledRejection handler
+// then runs its shutdown path). Cells: load the real router with the repository stand-in rejecting with the value; assert the
+// failure is logged as text and nothing is left unhandled (jest fails the running test on an unhandled rejection). The
+// stand-in rejects with a plain function, not jest.fn(): a spy could inspect a revoked Proxy and fail before the code under
+// test saw it. Mocks follow ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts. No database, no network.
+const mockState: { toThrow: unknown; errored: unknown[][] } = { toThrow: undefined, errored: [] };
+
+jest.mock('../repositories/certificationRepo', () => ({
+  initRepo: (..._args: unknown[]) => Promise.reject(mockState.toThrow),
+  getCertification: jest.fn(),
+  saveCertification: jest.fn(),
+  listCertifications: jest.fn(),
+  saveShare: jest.fn(),
+  getSharesByCertification: jest.fn(),
+  getLineageEvents: jest.fn(),
+  deleteCertification: jest.fn(),
+  reserveCertificationRow: jest.fn(),
+}));
+jest.mock('../db', () => ({
+  prisma: { $queryRaw: jest.fn(async () => []), $executeRaw: jest.fn(async () => 1), $executeRawUnsafe: jest.fn() },
+}));
+jest.mock('../services/chargeEvents', () => ({
+  createChargeEvent: jest.fn(),
+  getChargeEventsByCertification: jest.fn(),
+}));
+jest.mock('../utils/notificationClient', () => ({
+  notifyDocumentCertified: jest.fn(async () => undefined),
+  notifyDocumentRevoked: jest.fn(async () => undefined),
+  notifyDocumentShared: jest.fn(async () => undefined),
+}));
+jest.mock('../events', () => ({
+  publishEvent: jest.fn(async () => undefined),
+  EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' },
+}));
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: jest.fn(),
+  saveDocument: jest.fn(async () => undefined),
+  assertNoCycle: jest.fn(async () => undefined),
+  generateContentHash: jest.fn(() => 'hash'),
+}));
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    warn: () => undefined,
+    error: (...args: unknown[]) => {
+      mockState.errored.push(args);
+    },
+  },
+}));
+
+const INIT = 'Failed to init repo';
+
+beforeEach(() => {
+  mockState.toThrow = undefined;
+  mockState.errored.length = 0;
+  jest.resetModules();
+});
+
+/** Load the real router (its module-load initRepo() rejects with the value) and let the rejection settle. */
+async function loadWith(value: unknown): Promise<unknown[][]> {
+  mockState.toThrow = value;
+  require('../routes/certifications');
+  await new Promise<void>((resolve) => setImmediate(resolve));
+  await new Promise<void>((resolve) => setImmediate(resolve));
+  return mockState.errored.filter((a) => a[0] === INIT);
+}
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (a: unknown[] | undefined): string => {
+  const e = (a?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof e === 'string' ? e : '<' + typeof e + '>';
+};
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 certifications router: the module-load initRepo failure is logged as text for a hostile rejection value', () => {
+  it('control ks1868 C1: an ordinary Error rejection is logged with its message', async () => {
+    const logs = await loadWith(new Error('init boom'));
+    expect(logs).toHaveLength(1);
+    expect(reasonOf(logs[0])).toBe('init boom');
+  });
+  it('control ks1868 C2: a plain string rejection is logged as that string', async () => {
+    const logs = await loadWith('init string');
+    expect(logs).toHaveLength(1);
+    expect(reasonOf(logs[0])).toBe('init string');
+  });
+  it('RED ks1868 R1: a revoked Proxy rejection is logged as text, as for an ordinary Error', async () => {
+    const logs = await loadWith(revokedProxy());
+    expect(logs).toHaveLength(1);
+    expect(reasonOf(logs[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws is logged as text, as for an ordinary Error', async () => {
+    const logs = await loadWith(getterThrows());
+    expect(logs).toHaveLength(1);
+    expect(reasonOf(logs[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an object with no prototype (String() throws) is logged as text, as for an ordinary Error', async () => {
+    const logs = await loadWith(Object.create(null));
+    expect(logs).toHaveLength(1);
+    expect(reasonOf(logs[0])).toBe('unreadable thrown value');
+  });
+});
```
