# READY (hand-written note: hold_ready.py REFUSES a loose code_patch2 PASS, A3x unmeasured=1) - O31-P1 (KS-1544 class, auth issuerCertRepo.ts)

Spark operator 31, 2026-10-30 16:2x AEDT. Rung 4-5 LOOSE (one product, 1 hunk, product line written by the model, hunk header + per-hunk skeleton + new-file header skeleton dictated). **A PASS is a candidate, never a merge.** The site is NOT named in KS-1544 (it names tenant-provisioning); same class (paged ORDER BY with no unique last key), listed by op 29's census, read by op 31 at the tip.

- What: auth src/repositories/issuerCertRepo.ts :293 (listIssuerCerts, behind routes/issuerCerts.ts:357) `ORDER BY uploaded_at DESC` -> `ORDER BY uploaded_at DESC, id DESC`. Tie-break from the table's actual key: `issuer_certs.id UUID PRIMARY KEY` (migrations/024_issuer_certs.sql:45). Direction kept DESC. Plus 1 new vitest source-text file (6 cells, 2 red, 4 control).
- NOT touched: the other `ORDER BY uploaded_at DESC` at :246 (single-row active-cert read, ends LIMIT 1, not paged); userRepo.ts:1044 (Seat F 18th); staking stake.ts:458 (Seat E 22nd).
- Tip: a8c554659cb34c4406d0274daa5fed4aafec35ec (ls-remote 2026-10-30 16:19 and again at round time).
- Overlap: no OPEN PR (25 PRs, 130 file rows via GitHub API) touches issuerCertRepo.ts or routes/issuerCerts.ts; planted control providers/social/github.ts -> #1830 hit.
- Result: PASS 7/7 on the ORIGINAL brief, round 2 = a HARNESS RE-RUN of the same brief (NOT a rebrief). Round 1 had the identical model output (patch BYTE-IDENTICAL to the golden, cmp) and FAILED only A6: ks949-platform-admin-seed-identity.test.ts "the enumeration actually finds seed sites" hit vitest's 5000 ms default (duration 5004 ms; it takes 4000 ms at baseline under this load, a whole-tree walk), machine load ~12-15. Re-run: A4 2 red of 6, A5 6/6, whole auth suite 1332/1332, tsc rc 0, strict apply, A2a ok; model 21.1 s, 18602+1055 tokens, round 154 s. Control PASS (golden byte-identical) beforehand.
- Raise-seat notes: query plans unmeasured; ties in practice unmeasured (a bulk upload in one transaction would tie on NOW()); non-PR branches of live seats not enumerated; whether seat U 7th's KS-1844 'certifications' is this table is unknown. The ks949 seed-site cell (and, in the r2 baseline, a second ks949 cell) is load-flaky in the auth suite.
- Brief: night/briefs/ks_1544a_auth_issuer_certs_paged_list_total_order/KS-1544.md  Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1544a_auth_issuer_certs_paged_list_total_order-r2 (round 1: same name without -r2)

```diff
diff --git a/Blockchain/Dev/services/auth/src/repositories/issuerCertRepo.ts b/Blockchain/Dev/services/auth/src/repositories/issuerCertRepo.ts
--- a/Blockchain/Dev/services/auth/src/repositories/issuerCertRepo.ts
+++ b/Blockchain/Dev/services/auth/src/repositories/issuerCertRepo.ts
@@ -290,7 +290,7 @@
     query<IssuerCertRow>(
       `SELECT * FROM issuer_certs
        WHERE ${whereClause}
-       ORDER BY uploaded_at DESC
+       ORDER BY uploaded_at DESC, id DESC
        LIMIT $${params.length + 1} OFFSET $${params.length + 2}`,
       [...params, limit, offset],
       opts.tenantId,
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1544-class-auth-issuer-certs-list-orders-in-a-total-order.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1544-class-auth-issuer-certs-list-orders-in-a-total-order.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1544-class-auth-issuer-certs-list-orders-in-a-total-order.test.ts
@@ -0,0 +1,50 @@
+/**
+ * KS-1544 class (auth): the paged read in repositories/issuerCertRepo.ts (listIssuerCerts, behind GET /issuer-certs) sorts on
+ * `uploaded_at`, which is not unique, then pages with `LIMIT ... OFFSET ...`. Rows that tie on the sort key have no defined order
+ * between two queries, so a page walk can repeat or skip them (KS-1544 measured the same defect on platform_audit_log).
+ * issuer_certs has `id UUID PRIMARY KEY` (migrations/024_issuer_certs.sql), so the ORDER BY now ends in `, id DESC`.
+ * Source-text guard: the module needs a database to import.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { resolve } from 'node:path';
+
+const SRC = readFileSync(resolve(__dirname, '..', 'repositories', 'issuerCertRepo.ts'), 'utf8');
+
+/** Every paged ORDER BY clause (the text from ORDER BY through the OFFSET placeholder), whitespace collapsed. */
+function pagedOrders(src: string): string[] {
+  const found = src.match(/ORDER BY [^`;]*?OFFSET \$\$\{[^}]*\}/g) ?? [];
+  return found.map((s) => s.replace(/\s+/g, ' '));
+}
+
+/** True when the clause does not end its sort list in the primary key before LIMIT. */
+function tied(clause: string): boolean {
+  return !/, id DESC LIMIT/.test(clause);
+}
+
+describe('issuer certs paged list orders in a total order (KS-1544 class)', () => {
+  it('RED ks1544a T1 the paged list read orders by uploaded_at DESC, id DESC', () => {
+    expect(pagedOrders(SRC)).toEqual(['ORDER BY uploaded_at DESC, id DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}']);
+  });
+
+  it('RED ks1544a T2 no paged read in issuerCertRepo.ts is left tied', () => {
+    expect(pagedOrders(SRC).filter(tied)).toEqual([]);
+  });
+
+  it('control ks1544a C1 the scanner flags a tied clause and passes a total one', () => {
+    expect(tied('ORDER BY uploaded_at DESC LIMIT $1 OFFSET $2')).toBe(true);
+    expect(tied('ORDER BY uploaded_at DESC, id DESC LIMIT $1 OFFSET $2')).toBe(false);
+  });
+
+  it('control ks1544a C2 issuerCertRepo.ts has exactly one paged read', () => {
+    expect(pagedOrders(SRC)).toHaveLength(1);
+  });
+
+  it('control ks1544a C3 the single-row active-cert read keeps its own order', () => {
+    expect(SRC).toMatch(/ORDER BY uploaded_at DESC\s+LIMIT 1`/);
+  });
+
+  it('control ks1544a C4 the count query is not touched', () => {
+    expect(SRC).toContain('SELECT COUNT(*)::text AS count FROM issuer_certs WHERE ${whereClause}');
+  });
+});
```
