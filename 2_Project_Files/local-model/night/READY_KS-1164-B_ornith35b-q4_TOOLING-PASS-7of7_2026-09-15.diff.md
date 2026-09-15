# READY — KS-1164 PART B (systemTest/performance `runner/k6_docker.ts:241`: the k6 log mount falls back to `<name>-k6.log` when the summary name does not end in -summary.json — the second site the ticket's DoD names; Part A = gate/report.ts, held separately) — Ornith ornith:35b (Q4_K_M) PASS 7/7 (run night6 20:15; A2 --recount on the test section only)
# Source read by me (Wednesday): E1 exactly as briefed (a ternary keeping the existing derivation for conforming names, else `${summaryMount.replace(/\.json$/, '')}-k6.log`); the test copies k6Docker.test.ts's mocked-spawnSync driver; 🔴 cell (summary.json → summary-k6.log) red at the tip, green after; control (conforming name → <name>-k6.log, k6Docker.test.ts:151's fact) green both trees; whole performance suite green; tsc green. **Bundle A+B into ONE KS-1164 PR; the ticket's `toLocaleString()` follow-up stays open.**

```diff
--- a/systemTest/performance/runner/k6_docker.ts
+++ b/systemTest/performance/runner/k6_docker.ts
@@ -238,7 +238,9 @@ export function runK6(opts: RunOptions, envFlags: string[], obsCfg: Observability
     // terminal and nowhere else, so a concurrent four-slot run left no per-slot record of what k6
     // actually said. Derived from the summary path rather than rebuilt from the label parts, so the
     // log and the summary can never disagree about which run they belong to.
-    const k6LogMount = summaryMount.replace(/-summary\.json$/, '-k6.log');
+    // KS-1164: a summary name that does not end in `-summary.json` left this a no-op and pointed k6's log at the
+    // summary itself; fall back to `<name>-k6.log` beside it (conforming names keep their existing derivation).
+    const k6LogMount = summaryMount.endsWith('-summary.json') ? summaryMount.replace(/-summary\.json$/, '-k6.log') : `${summaryMount.replace(/\.json$/, '')}-k6.log`;
     // Resolved once: every slot-derived value in this command must describe the SAME slot.
     const slot = resolveSlot();
 
--- /dev/null
+++ b/systemTest/performance/tests/unit/runner/ks1164-k6-log-mount-never-collides-with-the-summary.test.ts
@@ -0,0 +1,73 @@
+/**
+ * Pins `runner/k6_docker.ts` line 241 — when `--summary` is named without the `-summary.json` suffix,
+ * k6's own log mount must still land beside the summary, never AT the summary.
+ *
+ * @module tests/unit/runner/ks1164-k6-log-mount-never-collides-with-the-summary
+ */
+
+import { vi } from 'vitest';
+
+const spawnSync = vi.fn(() => ({ status: 0 }));
+const existsSync = vi.fn(() => true);
+
+vi.mock('node:child_process', () => ({ spawnSync, execFileSync: vi.fn(() => '') }));
+vi.mock('node:fs', () => ({
+    existsSync,
+    mkdirSync: vi.fn(),
+    default: { existsSync, mkdirSync: vi.fn() },
+}));
+
+const { runK6 } = await import('../../../../runner/k6_docker.ts');
+const { ROOT_DIR } = await import('../../../../runner/paths.ts');
+
+const ENV = ['SECUURA_STACK_SLOT', 'SECUURA_ARTIFACT_SUFFIX', 'SECUURA_RUN_LABEL', 'STACK_SLOT'] as const;
+
+function clearEnv(): void {
+    for (const key of ENV) {
+        Reflect.deleteProperty(process.env, key);
+    }
+}
+
+const OBS_CFG = {
+    webDashboard: { period: '5s', port: 5665 },
+    docker: { k6Image: 'grafana/k6:2.1.0', scriptsMount: '/scripts' },
+} as never;
+
+function argsFor(summaryExportPath: string): string[] {
+    spawnSync.mockClear();
+    runK6(
+        {
+            scenario: 'smoke',
+            environment: 'local',
+            observabilityEnabled: true,
+            runDir: `${ROOT_DIR}/reports/performance-reports/smoke-slot1`,
+            summaryExportPath,
+            extraFlags: [],
+            quiet: false,
+        } as never,
+        [],
+        OBS_CFG,
+        false,
+    );
+    const call = spawnSync.mock.calls[0] as unknown as [string, string[]];
+    return call[1];
+}
+
+beforeEach(clearEnv);
+afterEach(() => {
+    clearEnv();
+    vi.clearAllMocks();
+});
+
+describe('k6 log mount never collides with the summary path (KS-1164)', () => {
+    it('🔴 KS-1164 — a summary named summary.json gets a k6 log beside it, never the summary path itself', () => {
+        const args = argsFor(`${ROOT_DIR}/reports/performance-reports/smoke-slot1/summary.json`);
+        const log = args.find((a) => a.startsWith('--log-output=file=')) ?? '';
+        expect(log).toBe('--log-output=file=/scripts/reports/performance-reports/smoke-slot1/summary-k6.log');
+    });
+
+    it('KS-1164 control — the conforming name still derives <name>-k6.log', () => {
+        const args = argsFor(`${ROOT_DIR}/reports/performance-reports/smoke-slot1/smoke-slot1-summary.json`);
+        const log = args.find((a) => a.startsWith('--log-output=file=')) ?? '';
+        expect(log).toBe('--log-output=file=/scripts/reports/performance-reports/smoke-slot1/smoke-slot1-k6.log');
+    });
+});
```
