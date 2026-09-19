# READY — KS-1258-N77-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1258-ornith35b-night4/out.md.checker/patch.diff`** (from `ls`, 20:12).

**Held 20:12 2026-09-19 by the 18:0x Wednesday seat after a source read** (woken on the verdict by the background waiter). Tip `ba1210afc`. Exact-array advice cell at :576; all six start shapes red it (N77-1; the old deny-list cell is kept). Test-only: one file under `__tests__/`; every `+`/`-` line = the brief; crossed control (the other round-15 briefs) mostly absent. Source: the #1077-#1083 gate's NOT-PINNED rows. Raise: Refs KS-1258, never Closes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[C576_TSXWATCH] every control green under the tamper
T6 summary: 6/6 tamper(s) red exactly their declared set
T7 summary: controls green under all 6 tamper(s)
T8 summary: all 6 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1248-n-1-system-status-troubleshooting-marks.test.ts mode=modify runner=vitest cells=5 tampers=6 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1248-n-1-system-status-troubleshooting-marks.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1248-n-1-system-status-troubleshooting-marks.test.ts
@@ -84,1 +84,6 @@
+  it('RED KS-1258 N77-1: the degraded required advice is exactly the read-first comment and one curl', async () => {
+    Object.assign(answers, { 'anchoring.ks1248': 'degraded', 'originate.ks1248': 'up' });
+    const advice = await adviceFor('anchoring');
+    expect([advice.length, advice[0]?.commands]).toEqual([1, ['# Read what the service reports as degraded', 'curl -s http://anchoring.ks1248:1/health']]);
+  });
   it('RED KS-1258 N68-1: the degraded required advice carries no start command in ANY common shape', async () => {
```
