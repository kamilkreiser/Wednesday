# READY — KS-1868-KS-1868-O86-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 00:42 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 00:42 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `14fd8e54aefae355ec5e4bf57e4c6f3f1a710883`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts } + { Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts` (product) and `Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
156	0	Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (24 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: approvalWorkflowService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts`; test(s): `Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts 24 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts 156 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=6 of total=10; red cell(s): ['KS-1868 the approval workflow catches answer as for an ordinary Error and log text for a hostile thrown value RED ks1868 R1: a boot probe failure that is a revoked Proxy resolves and is logged as text, as for an ordinary Error', 'KS-1868 the approval workflow catches answer as for an ordinary Error and log text for a hostile thrown value RED ks1868 R2: a boot probe failure that is an Error whose message is a Symbol resolves and is logged as text, as for an ordinary Error', 'KS-1868 the approval workflow catches answer as for an ordinary Error and log text for a hostile thrown value RED ks1868 R3: a seed upsert failure that is a revoked Proxy resolves and is logged as text for every workflow, as for an ordinary Error', 'KS-1868 the approval workflow catches answer as for an ordinary Error and log text for a hostile thrown value RED ks1868 R4: a seed upsert failure that is an Error whose message is a Symbol resolves and is logged as text for every workflow, as for an ordinary Error', 'KS-1868 the approval workflow catches answer as for an ordinary Error and log text for a hostile thrown value RED ks1868 R5: an escalation failure that is a revoked Proxy returns the zero counts and is logged as text, as for an ordinary Error', 'KS-1868 the approval workflow catches answer as for an ordinary Error and log text for a hostile thrown value RED ks1868 R6: an escalation failure that is an Error whose message is a Symbol returns the zero counts and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=120 failed=0 | after: total=130 failed=0` · `NEW reds: []` [baseline_suite.json total=120 failed=0; after_suite.json total=130 failed=0]
- A6 [verbatim]: `PASS A6 whole services/transfer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/transfer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts` (+156/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `14fd8e54aefae355ec5e4bf57e4c6f3f1a710883` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts b/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
--- a/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
+++ b/Blockchain/Dev/services/transfer/src/services/approvalWorkflowService.ts
@@ -342,7 +342,14 @@
     try {
       await dbUpsertWorkflow(workflow);
     } catch (err: any) {
-      console.error(`[approvalWorkflowService] Failed to seed workflow ${wf.id}:`, err?.message);
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      console.error(`[approvalWorkflowService] Failed to seed workflow ${wf.id}:`, reason);
     }
   }
 }
@@ -353,6 +360,13 @@
     await query('SELECT 1 FROM svc_approval_workflows LIMIT 1');
     await seedDefaultWorkflows();
   } catch (err: any) {
-    console.warn('[approvalWorkflowService] DB tables not ready:', err?.message);
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    console.warn('[approvalWorkflowService] DB tables not ready:', reason);
   }
 }
@@ -626,5 +640,12 @@
         }
       }
     } catch (err: any) {
-      console.error('[approvalWorkflowService] processEscalations error:', err?.message);
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      console.error('[approvalWorkflowService] processEscalations error:', reason);
     }
diff --git a/Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts
@@ -0,0 +1,156 @@
+import { describe, it, expect, beforeAll, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 86 screen, transfer approval workflow service): the seed catch (line 345), the DB-not-ready catch (line 356)
+// and the processEscalations catch (line 629) of services/transfer/src/services/approvalWorkflowService.ts pass
+// `err?.message` straight into console.error / console.warn, unguarded. A thrown value whose read throws (a revoked Proxy, an
+// Error whose message getter throws) makes the catch itself throw, so verifyDbReady and processEscalations REJECT instead of
+// answering (the boot probe resolves; processEscalations returns its zero counts); a Symbol message is handed to the console
+// uncoerced. The cells make the database stand-in reject with such a value and assert the answer and the logged text (the
+// constant when the value cannot be turned into text). Harness: the real module with ../db and ./delegationService replaced by
+// plain stand-ins and console.error / console.warn replaced by plain recording functions (no database).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  mode: 'probe' as 'probe' | 'seed' | 'escalate',
+  upserts: 0,
+  logged: [] as unknown[][],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (sql: string) => {
+    const text = String(sql);
+    if (h.mode === 'probe') return Promise.reject(h.toThrow);
+    if (h.mode === 'seed') {
+      if (/SELECT 1 FROM svc_approval_workflows/.test(text)) return Promise.resolve({ rows: [], rowCount: 0 });
+      h.upserts += 1;
+      return Promise.reject(h.toThrow);
+    }
+    return Promise.reject(h.toThrow);
+  },
+}));
+vi.mock('../services/delegationService', () => ({ delegationService: {} }));
+
+type Mod = typeof import('../services/approvalWorkflowService');
+let mod: Mod;
+const realError = console.error;
+const realWarn = console.warn;
+beforeAll(async () => {
+  mod = await import('../services/approvalWorkflowService');
+});
+afterAll(() => {
+  console.error = realError;
+  console.warn = realWarn;
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.mode = 'probe';
+  h.upserts = 0;
+  h.logged.length = 0;
+  console.error = (...args: unknown[]) => {
+    h.logged.push(args);
+  };
+  console.warn = (...args: unknown[]) => {
+    h.logged.push(args);
+  };
+});
+
+async function settle<T>(p: () => Promise<T>): Promise<{ ok: boolean; value: T | undefined }> {
+  try {
+    return { ok: true, value: await p() };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const probe = () => {
+  h.mode = 'probe';
+  return settle(() => mod.verifyDbReady());
+};
+const seed = () => {
+  h.mode = 'seed';
+  return settle(() => mod.verifyDbReady());
+};
+const escalate = () => {
+  h.mode = 'escalate';
+  return settle(() => mod.approvalWorkflowService.processEscalations());
+};
+const LINES = (prefix: string) => h.logged.filter((c) => typeof c[0] === 'string' && (c[0] as string).startsWith(prefix));
+const PROBE = '[approvalWorkflowService] DB tables not ready:';
+const SEED = '[approvalWorkflowService] Failed to seed workflow';
+const ESC = '[approvalWorkflowService] processEscalations error:';
+/** The logged message argument as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (c: unknown[] | undefined): string => (typeof c?.[1] === 'string' ? (c[1] as string) : '<' + typeof c?.[1] + '>');
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const ZERO = { escalatedCount: 0, timedOutCount: 0 };
+
+describe('KS-1868 the approval workflow catches answer as for an ordinary Error and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error in the boot probe resolves and is logged with its message', async () => {
+    h.toThrow = new Error('no table');
+    expect(await probe()).toEqual({ ok: true, value: undefined });
+    expect(LINES(PROBE)).toHaveLength(1);
+    expect(reasonOf(LINES(PROBE)[0])).toBe('no table');
+  });
+  it('control ks1868 C2: an ordinary Error in every seed upsert resolves and is logged once per workflow with its message', async () => {
+    h.toThrow = new Error('upsert failed');
+    expect(await seed()).toEqual({ ok: true, value: undefined });
+    expect(h.upserts).toBeGreaterThan(0);
+    expect(LINES(SEED)).toHaveLength(h.upserts);
+    expect(reasonOf(LINES(SEED)[0])).toBe('upsert failed');
+  });
+  it('control ks1868 C3: an ordinary Error in processEscalations returns the zero counts and is logged with its message', async () => {
+    h.toThrow = new Error('select failed');
+    expect(await escalate()).toEqual({ ok: true, value: ZERO });
+    expect(LINES(ESC)).toHaveLength(1);
+    expect(reasonOf(LINES(ESC)[0])).toBe('select failed');
+  });
+  it('control ks1868 C4: a thrown plain string in processEscalations returns the zero counts and is logged without a message', async () => {
+    h.toThrow = 'plain boom';
+    expect(await escalate()).toEqual({ ok: true, value: ZERO });
+    expect(LINES(ESC)).toHaveLength(1);
+    expect(reasonOf(LINES(ESC)[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a boot probe failure that is a revoked Proxy resolves and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = revokedProxy();
+    expect(await probe()).toEqual({ ok: true, value: undefined });
+    expect(LINES(PROBE)).toHaveLength(1);
+    expect(reasonOf(LINES(PROBE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a boot probe failure that is an Error whose message is a Symbol resolves and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = withMessage(Symbol('ks1868'));
+    expect(await probe()).toEqual({ ok: true, value: undefined });
+    expect(LINES(PROBE)).toHaveLength(1);
+    expect(reasonOf(LINES(PROBE)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: a seed upsert failure that is a revoked Proxy resolves and is logged as text for every workflow, as for an ordinary Error', async () => {
+    h.toThrow = revokedProxy();
+    expect(await seed()).toEqual({ ok: true, value: undefined });
+    expect(h.upserts).toBeGreaterThan(0);
+    expect(LINES(SEED)).toHaveLength(h.upserts);
+    expect(reasonOf(LINES(SEED)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: a seed upsert failure that is an Error whose message is a Symbol resolves and is logged as text for every workflow, as for an ordinary Error', async () => {
+    h.toThrow = withMessage(Symbol('ks1868'));
+    expect(await seed()).toEqual({ ok: true, value: undefined });
+    expect(h.upserts).toBeGreaterThan(0);
+    expect(LINES(SEED)).toHaveLength(h.upserts);
+    expect(reasonOf(LINES(SEED)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R5: an escalation failure that is a revoked Proxy returns the zero counts and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = revokedProxy();
+    expect(await escalate()).toEqual({ ok: true, value: ZERO });
+    expect(LINES(ESC)).toHaveLength(1);
+    expect(reasonOf(LINES(ESC)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R6: an escalation failure that is an Error whose message is a Symbol returns the zero counts and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = withMessage(Symbol('ks1868'));
+    expect(await escalate()).toEqual({ ok: true, value: ZERO });
+    expect(LINES(ESC)).toHaveLength(1);
+    expect(reasonOf(LINES(ESC)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
