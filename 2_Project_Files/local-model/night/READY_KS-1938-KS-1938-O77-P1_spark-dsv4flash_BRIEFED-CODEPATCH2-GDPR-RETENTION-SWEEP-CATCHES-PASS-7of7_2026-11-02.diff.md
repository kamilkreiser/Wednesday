# READY — KS-1938-KS-1938-O77-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 15:08 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 15:08 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `968f17070208efc1e888308bdea49de5112a42e8`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/gdprService.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/gdprService.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/originate/src/services/gdprService.ts
136	0	Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: gdprService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/gdprService.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/gdprService.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts 136 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/gdprService.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1938 the retention sweep reads a thrown value safely and keeps going RED ks1938 R1 policy DELETE: a revoked Proxy rejection is logged as a constant reason and the second policy is still enforced', 'KS-1938 the retention sweep reads a thrown value safely and keeps going RED ks1938 R2 policy DELETE: an Error whose message getter throws is logged as a constant reason and the second policy is still enforced', 'KS-1938 the retention sweep reads a thrown value safely and keeps going RED ks1938 R3 policy SELECT: a revoked Proxy rejection is logged as a constant reason and the sweep returns nothing', 'KS-1938 the retention sweep reads a thrown value safely and keeps going RED ks1938 R4 policy SELECT: an Error whose message getter throws is logged as a constant reason and the sweep returns nothing']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2084 failed=0 | after: total=2090 failed=0` · `NEW reds: []` [baseline_suite.json total=2084 failed=0; after_suite.json total=2090 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/gdprService.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts` (+136/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/gdprService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `968f17070208efc1e888308bdea49de5112a42e8` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1938): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/KS-1938.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1938_o77_p1_originate_gdpr_retention_sweep_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/gdprService.ts b/Blockchain/Dev/services/originate/src/services/gdprService.ts
--- a/Blockchain/Dev/services/originate/src/services/gdprService.ts
+++ b/Blockchain/Dev/services/originate/src/services/gdprService.ts
@@ -496,9 +496,21 @@
           WHERE id = ${policy.id}::uuid
         `;
       } catch (err: any) {
-        logger.error('Retention enforcement failed', { dataType: policy.data_type, error: err instanceof Error ? err.message : String(err) });
+        let reason: string;
+        try {
+          reason = err instanceof Error ? err.message : String(err);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
+        logger.error('Retention enforcement failed', { dataType: policy.data_type, error: reason });
       }
     }
   } catch (err: any) {
-    logger.error('Retention enforcement error', { error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Retention enforcement error', { error: reason });
   }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts
@@ -0,0 +1,136 @@
+// KS-1938 (originate services/gdprService.ts, enforceRetentionImpl): the retention sweep logged a failed policy in a per-policy catch and an outer catch, and read the thrown value
+// there as `err instanceof Error ? err.message : String(err)`. When the value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws
+// on `.message`) the read threw INSIDE the per-policy catch, left the loop, and the outer catch then logged a different error: every LATER policy was skipped for that run (no DELETE,
+// no deletion-log row, no last_enforcement_at stamp), where an ordinary Error lets the sweep continue. Each catch now reads the value inside its own try and logs the constant reason
+// `unreadable thrown value`. The database stand-in classifies each tagged-template statement and rejects the one the cell names with the thrown value (a plain function, not jest.fn():
+// a spy inspects what it rejects with and could itself fail on a revoked Proxy before the code under test saw it). Nothing is written to a real database.
+const mockState: { failOn: string | null; thrown: unknown; stmts: string[]; errored: unknown[][] } = {
+  failOn: null,
+  thrown: undefined,
+  stmts: [],
+  errored: [],
+};
+
+const MOCK_POLICIES = [
+  { id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1', data_type: 'user_sessions', retention_period_days: 30, deletion_method: 'delete', auto_delete: true },
+  { id: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa2', data_type: 'verification_requests', retention_period_days: 30, deletion_method: 'delete', auto_delete: true },
+];
+
+function mockOpOf(strings: TemplateStringsArray): string {
+  const sql = strings.join('?').replace(/\s+/g, ' ').trim();
+  if (/FROM data_retention_policies/.test(sql)) return 'SELECT policies';
+  const del = /DELETE FROM (\w+)/.exec(sql);
+  if (del) return 'DELETE ' + del[1];
+  if (/INSERT INTO data_deletion_log/.test(sql)) return 'INSERT deletion_log';
+  if (/UPDATE data_retention_policies/.test(sql)) return 'UPDATE policy stamp';
+  return 'other';
+}
+
+async function mockStatement(strings: TemplateStringsArray): Promise<unknown> {
+  const op = mockOpOf(strings);
+  mockState.stmts.push(op);
+  if (mockState.failOn !== null && op === mockState.failOn) {
+    throw mockState.thrown;
+  }
+  if (op === 'SELECT policies') return MOCK_POLICIES;
+  if (op.startsWith('DELETE')) return 2;
+  if (op === 'INSERT deletion_log') {
+    return [{ id: 'x', data_type: 'd', records_affected: 2, deletion_method: 'delete', reason: 'r', performed_by: 'system', performed_at: new Date() }];
+  }
+  return 1;
+}
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: (strings: TemplateStringsArray) => mockStatement(strings),
+    $executeRaw: (strings: TemplateStringsArray) => mockStatement(strings),
+  },
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    warn: () => undefined,
+    debug: () => undefined,
+    error: (...args: unknown[]) => {
+      mockState.errored.push(args);
+    },
+  },
+}));
+
+import { enforceRetention } from '../services/gdprService';
+
+const UNREADABLE = 'unreadable thrown value';
+// What an ordinary Error gets when the FIRST policy's DELETE rejects: the failure is logged and the sweep goes on to the second policy.
+const SWEEP_CONTINUES = ['SELECT policies', 'DELETE user_sessions', 'DELETE verification_requests', 'INSERT deletion_log', 'UPDATE policy stamp'];
+
+beforeEach(() => {
+  mockState.failOn = null;
+  mockState.thrown = undefined;
+  mockState.stmts.length = 0;
+  mockState.errored.length = 0;
+});
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+async function sweep(failOn: string, thrown: unknown): Promise<{ settled: 'resolved' | 'rejected'; count: number }> {
+  mockState.failOn = failOn;
+  mockState.thrown = thrown;
+  try {
+    const logs = await enforceRetention();
+    return { settled: 'resolved', count: logs.length };
+  } catch {
+    return { settled: 'rejected', count: -1 };
+  }
+}
+
+describe('KS-1938 the retention sweep reads a thrown value safely and keeps going', () => {
+  it('control ks1938 C1 policy DELETE: an ordinary Error is logged with its own message and the second policy is still enforced', async () => {
+    expect(await sweep('DELETE user_sessions', new Error('db down'))).toEqual({ settled: 'resolved', count: 1 });
+    expect(mockState.stmts).toEqual(SWEEP_CONTINUES);
+    expect(mockState.errored).toEqual([['Retention enforcement failed', { dataType: 'user_sessions', error: 'db down' }]]);
+  });
+
+  it('control ks1938 C2 policy SELECT: an ordinary Error is logged with its own message and the sweep returns nothing', async () => {
+    expect(await sweep('SELECT policies', new Error('db down'))).toEqual({ settled: 'resolved', count: 0 });
+    expect(mockState.stmts).toEqual(['SELECT policies']);
+    expect(mockState.errored).toEqual([['Retention enforcement error', { error: 'db down' }]]);
+  });
+
+  it('RED ks1938 R1 policy DELETE: a revoked Proxy rejection is logged as a constant reason and the second policy is still enforced', async () => {
+    expect(await sweep('DELETE user_sessions', revokedProxy())).toEqual({ settled: 'resolved', count: 1 });
+    expect(mockState.stmts).toEqual(SWEEP_CONTINUES);
+    expect(mockState.errored).toEqual([['Retention enforcement failed', { dataType: 'user_sessions', error: UNREADABLE }]]);
+  });
+
+  it('RED ks1938 R2 policy DELETE: an Error whose message getter throws is logged as a constant reason and the second policy is still enforced', async () => {
+    expect(await sweep('DELETE user_sessions', getterThrows())).toEqual({ settled: 'resolved', count: 1 });
+    expect(mockState.stmts).toEqual(SWEEP_CONTINUES);
+    expect(mockState.errored).toEqual([['Retention enforcement failed', { dataType: 'user_sessions', error: UNREADABLE }]]);
+  });
+
+  it('RED ks1938 R3 policy SELECT: a revoked Proxy rejection is logged as a constant reason and the sweep returns nothing', async () => {
+    expect(await sweep('SELECT policies', revokedProxy())).toEqual({ settled: 'resolved', count: 0 });
+    expect(mockState.stmts).toEqual(['SELECT policies']);
+    expect(mockState.errored).toEqual([['Retention enforcement error', { error: UNREADABLE }]]);
+  });
+
+  it('RED ks1938 R4 policy SELECT: an Error whose message getter throws is logged as a constant reason and the sweep returns nothing', async () => {
+    expect(await sweep('SELECT policies', getterThrows())).toEqual({ settled: 'resolved', count: 0 });
+    expect(mockState.stmts).toEqual(['SELECT policies']);
+    expect(mockState.errored).toEqual([['Retention enforcement error', { error: UNREADABLE }]]);
+  });
+});
```
