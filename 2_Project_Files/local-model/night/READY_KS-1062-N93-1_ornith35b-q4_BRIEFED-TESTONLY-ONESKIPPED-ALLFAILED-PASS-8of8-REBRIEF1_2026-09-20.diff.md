# READY — KS-1062-N93-1 (Ornith, briefed, test_only) — PASS 8/8 on its ONE rebrief — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1062-ornith35b-night2/out.md.checker/patch.diff`** (from `ls`, 03:29).

**Held 03:29 2026-09-20 by the 18:0x Wednesday seat after a source read.** Tip `c87458bdd`. Pins one tenant skipped (total 1) and every tenant FAILED (N93-1). r1 failed T4 (the model doubled a regex's backslashes; a brief defect); r2 uses startsWith/includes with no backslash. Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief. **KS-1062 is ARCHIVED: NO Refs, no KS key in branch/title/commit.** Source: the #1092-#1096 gate's NOT-PINNED rows.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[ALLFAILED] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts mode=modify runner=vitest cells=9 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts
@@ -103,1 +103,9 @@
+  it('RED KS-1062 N93-1: a single tenant, skipped, is counted as skipped', async () => {
+    await boot([tenant('qa-skip-solo', 'qa_skip')]);
+    expect(metaOf(summary())).toEqual({ migrated: 0, failed: 0, skipped: 1, total: 1 });
+  });
+  it('RED KS-1062 N93-1: when every tenant FAILS, the summary is an INCOMPLETE WARN counting all of them failed', async () => {
+    await boot([tenant('qa-ghost-a', 'qa_ghost'), tenant('qa-ghost-b', 'qa_ghost')]);
+    expect([summary().startsWith('[WARN] [startup-migrations] Tenant DB migrations INCOMPLETE '), summary().includes(' 2 tenant(s) FAILED {'), metaOf(summary())]).toEqual([true, true, { migrated: 0, failed: 2, skipped: 0, total: 2 }]);
+  });
 });
```
