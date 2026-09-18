# READY — KS-1258 N44-1 (Ornith, briefed, TEST_ONLY) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = the fenced diff in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1258-ornith35b-night2/out.md` (one test file; STRICT apply).**

**Held 2026-09-18 17:45 by the 14:4x Wednesday seat after a source read.** Tip `52df64f84`. Closes the #1042-#1045 batch gate's finding N44-1 (a follow-up to merged #1044).

## Source read
- one cell: a DEGRADED optional service's advice matches NO common start pattern (npm start / docker compose up / systemctl start / pm2 start); tampers NPMSTART + COMPOSE at system-status.ts:592 each red exactly the new cell.
- The 7 '+' lines are IDENTICAL to the brief (0 missing, 0 extra, 0 '-'). T1-T8 PASS incl. T3 strict, T5 green at tip, T6 exact red sets (assertions), T7 controls, T8 restore by sha256.
- **No product change.** Refs KS-1258 (the ticket stays In Progress per §5f). Test-only, tier 2.
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1258-degraded-optional-service-advice.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1258-degraded-optional-service-advice.test.ts
@@ -82,3 +82,10 @@
     expect([b.length, b[0]?.severity, startsOrRestarts(b[0])]).toEqual([1, 'warning', false]);
   });
+  it('KS-1258 N44-1: the degraded optional advice carries no start command in ANY common shape', async () => {
+    answers['billing.ks1258'] = 'degraded';
+    answers['staking.ks1258'] = 'up';
+    const b = await adviceFor('billing');
+    const starts = (b[0]?.commands ?? []).filter((c: string) => /npm start|npm --prefix|npm run|docker compose up|docker-compose up|systemctl start|pm2 start|restart/i.test(c));
+    expect([b.length, starts]).toEqual([1, []]);
+  });
 });
```
