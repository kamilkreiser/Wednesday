# READY (hand-written note: hold_ready.py REFUSES a loose code_patch2 PASS, A3x unmeasured=2) - O28-P1 (KS-1544 class, originate)

Spark operator 28, 2026-10-30. Rung 5 LOOSE (TWO products, two ORDER BY shapes; product lines written by the model, hunk headers dictated, per-hunk skeleton). **A PASS is a candidate, never a merge.** The nine sites are NOT named in KS-1544 (it names tenant-provisioning); they are the same class (paged ORDER BY with no unique last key), found by operator 28's census. Wednesday decides: raise as `Refs KS-1544` or file a new ticket first.

- What: originate errorTrackingService.ts getRecentErrors (5 system_errors reads, `, id DESC`) and routes/adminConfig.ts (2 audit_logs reads `, id DESC`; 2 rights_holders reads `display_name ASC, last_name ASC, id ASC`). Six product hunks + 1 new jest source-text file (6 cells, 3 red).
- Tip: 85cd24d81cb97e30e08fdc054d1ba4b65ea8b558 (ls-remote 2026-10-30 14:5x).
- Result: PASS 7/7 on the REBRIEF (original FAILED A2a: new-file header form; see report); 216 s round, model 87.8 s, 53220+2324 tokens; A4 3 red of 6 (3 control green); A5 6/6; originate suite no new red; tsc rc 0; strict apply; A2a 6/6.
- Golden: patch.diff BYTE-IDENTICAL to the golden (the golden product lines were not shown to the model); control PASS. I read the nine +/- pairs: each only inserts the tie-break column; all three tables have id UUID PRIMARY KEY.
- Why no hold_ready READY: loose code_patch2 excluded (A3x unmeasured=2).
- Brief: night/briefs/ks_1544c_originate_paged_lists_total_order_rebrief/KS-1544.md  Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1544c_originate_paged_lists_total_order_rebrief
- Raise-seat notes: query plan on (created_at DESC)-only indexes unmeasured; the defect is reasoned from SQL, not seen in data; open PRs on adminConfig.ts not enumerated. Disjoint from READY KS-1780 p1 (systemErrors.ts) and KS-1544 p1 (tenant-provisioning).

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/errorTrackingService.ts b/Blockchain/Dev/services/originate/src/services/errorTrackingService.ts
--- a/Blockchain/Dev/services/originate/src/services/errorTrackingService.ts
+++ b/Blockchain/Dev/services/originate/src/services/errorTrackingService.ts
@@ -88,7 +88,7 @@
       errors = await prisma.$queryRaw`
         SELECT * FROM system_errors
         WHERE service = ${opts.service} AND severity = ${opts.severity}
-        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
+        ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}
       `;
       countResult = await prisma.$queryRaw`
         SELECT COUNT(*)::int as total FROM system_errors
@@ -97,7 +97,7 @@
     } else if (opts?.service) {
       errors = await prisma.$queryRaw`
         SELECT * FROM system_errors WHERE service = ${opts.service}
-        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
+        ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}
       `;
       countResult = await prisma.$queryRaw`
         SELECT COUNT(*)::int as total FROM system_errors WHERE service = ${opts.service}
@@ -105,7 +105,7 @@
     } else if (opts?.severity) {
       errors = await prisma.$queryRaw`
         SELECT * FROM system_errors WHERE severity = ${opts.severity}
-        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
+        ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}
       `;
       countResult = await prisma.$queryRaw`
         SELECT COUNT(*)::int as total FROM system_errors WHERE severity = ${opts.severity}
@@ -113,14 +113,14 @@
     } else if (opts?.resolved !== undefined) {
       errors = await prisma.$queryRaw`
         SELECT * FROM system_errors WHERE resolved = ${opts.resolved}
-        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
+        ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}
       `;
       countResult = await prisma.$queryRaw`
         SELECT COUNT(*)::int as total FROM system_errors WHERE resolved = ${opts.resolved}
       `;
     } else {
       errors = await prisma.$queryRaw`
-        SELECT * FROM system_errors ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
+        SELECT * FROM system_errors ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}
       `;
       countResult = await prisma.$queryRaw`
         SELECT COUNT(*)::int as total FROM system_errors
diff --git a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
--- a/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
+++ b/Blockchain/Dev/services/originate/src/routes/adminConfig.ts
@@ -1232,12 +1232,12 @@
       rows = await ((req as any).db || prisma).$queryRaw`
         SELECT * FROM audit_logs
          WHERE tenant_id = ${tenantId}::uuid AND action = ${action}
-        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
+        ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}
       `;
     } else {
       rows = await ((req as any).db || prisma).$queryRaw`
         SELECT * FROM audit_logs
          WHERE tenant_id = ${tenantId}::uuid
-        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
+        ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}
       `;
     }
@@ -1402,11 +1402,11 @@
           WHERE organization_id = ${tenantId}::uuid
             AND (first_name ILIKE ${q} OR last_name ILIKE ${q} OR email ILIKE ${q} OR display_name ILIKE ${q} OR external_id ILIKE ${q})
             AND status = 'active'
-          ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}
+          ORDER BY display_name ASC, last_name ASC, id ASC LIMIT ${limit} OFFSET ${offset}
         `;
       }
       return tx.$queryRaw`
         SELECT * FROM rights_holders WHERE organization_id = ${tenantId}::uuid AND status = 'active'
-        ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}
+        ORDER BY display_name ASC, last_name ASC, id ASC LIMIT ${limit} OFFSET ${offset}
       `;
     });
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1544-class-originate-paged-lists-order-in-a-total-order.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1544-class-originate-paged-lists-order-in-a-total-order.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1544-class-originate-paged-lists-order-in-a-total-order.test.ts
@@ -0,0 +1,61 @@
+/**
+ * KS-1544 class (originate): five paged reads in services/errorTrackingService.ts and four in routes/adminConfig.ts end their
+ * ORDER BY in a column that is not unique, then page with `LIMIT ${limit} OFFSET ${offset}`. Rows that tie on the sort key have no defined
+ * order between two queries, so a page walk can repeat or skip them (KS-1544 measured the same defect on platform_audit_log; KS-1731 on
+ * vc-issuer). The ORDER BY of each paged read now ends in the primary key: `, id DESC` after `created_at DESC`, and `, id ASC` after
+ * `display_name ASC, last_name ASC` (rights holders). Source-text guard: the two modules need a database and a full app to import.
+ */
+import { readFileSync } from 'node:fs';
+import { resolve } from 'node:path';
+
+const TRACK = readFileSync(resolve(__dirname, '..', 'services', 'errorTrackingService.ts'), 'utf8');
+const ADMIN = readFileSync(resolve(__dirname, '..', 'routes', 'adminConfig.ts'), 'utf8');
+
+/** Every paged ORDER BY clause (the text from ORDER BY through the OFFSET placeholder), whitespace collapsed. */
+function pagedOrders(src: string): string[] {
+  const found = src.match(/ORDER BY [^`;]*?LIMIT \$\{limit\} OFFSET \$\{offset\}/g) ?? [];
+  return found.map((s) => s.replace(/\s+/g, ' '));
+}
+
+/** True when the clause ends its sort list in the primary key before LIMIT. */
+function tied(clause: string): boolean {
+  return !/, id (ASC|DESC) LIMIT/.test(clause);
+}
+
+describe('originate paged lists order in a total order (KS-1544 class)', () => {
+  it('RED ks1544c T1 every paged read in errorTrackingService.ts ends its ORDER BY in id', () => {
+    const clauses = pagedOrders(TRACK);
+    expect(clauses).toHaveLength(5);
+    expect(clauses.filter(tied)).toEqual([]);
+  });
+
+  it('RED ks1544c A1 the two paged audit_logs reads in adminConfig.ts end their ORDER BY in id DESC', () => {
+    const clauses = pagedOrders(ADMIN).filter((c) => c.includes('created_at DESC'));
+    expect(clauses).toHaveLength(2);
+    expect(clauses.filter((c) => !c.includes('ORDER BY created_at DESC, id DESC LIMIT'))).toEqual([]);
+  });
+
+  it('RED ks1544c A2 the two paged rights_holders reads in adminConfig.ts end their ORDER BY in id ASC', () => {
+    const clauses = pagedOrders(ADMIN).filter((c) => c.includes('display_name'));
+    expect(clauses).toHaveLength(2);
+    expect(clauses.filter((c) => !c.includes('ORDER BY display_name ASC, last_name ASC, id ASC LIMIT'))).toEqual([]);
+  });
+
+  it('control ks1544c C1 the scanner flags a tied clause and passes a total one', () => {
+    expect(tied('ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}')).toBe(true);
+    expect(tied('ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}')).toBe(false);
+    expect(tied('ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}')).toBe(true);
+    expect(tied('ORDER BY display_name ASC, last_name ASC, id ASC LIMIT ${limit} OFFSET ${offset}')).toBe(false);
+  });
+
+  it('control ks1544c C2 adminConfig.ts has exactly four paged reads, and the unpaged reads keep their ORDER BY', () => {
+    expect(pagedOrders(ADMIN)).toHaveLength(4);
+    expect(ADMIN).toContain('SELECT * FROM policy_audit_log ORDER BY created_at DESC LIMIT 100');
+    expect(ADMIN).toContain('FROM users ORDER BY created_at DESC LIMIT 200');
+  });
+
+  it('control ks1544c C3 the count queries of errorTrackingService.ts are not touched', () => {
+    expect(TRACK).toContain('SELECT COUNT(*)::int as total FROM system_errors');
+    expect(TRACK).toContain('WHERE service = ${opts.service} AND severity = ${opts.severity}');
+  });
+});
```
