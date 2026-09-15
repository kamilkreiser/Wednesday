# READY — KS-887 (Wednesday's own KS-869 test defect, found by the KS-869 tier-1 gate: the WRITE-half column-list pin was satisfied by the COALESCE clause; the X2 shape ran six cells green) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r2 (r1 refused twice by a HARNESS gap — A2b read a modify-in-place hunk as a stub — then, under the fixed checker, at A3c on one model-dialect line: a doubled backslash before $ in a regex literal; the brief's placeholder pin became a plain toContain), TEST-ONLY MODIFY-IN-PLACE (the first of that shape), tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f — 0 files under Blockchain/ moved), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks887-ornith35b-night2
# Source read by me (Wednesday): the ONE hunk is the brief's byte-for-byte — line 87's loose regex replaced by a capture of the column list itself (INSERT INTO svc_api_keys \(([^)]*)\)) + toContain('connector_id') on the capture, plus the placeholder pin toContain(',$14,$15)'); lines 86/88/89 untouched. A4 under the tamper (index.ts:313 connector_id dropped from the column list): the WRITE-half cell RED BY ASSERTION on 'connector_id must be in the INSERT column list itself' (1 failed / 6 run, every other cell green); A5 at the tip 6/6; A6 no new red across services/security; A7 tsc 0. The ticket's acceptance met: the X2 tamper reds, the current fix passes — predicted (measured on the tip/tamper text before queuing) then measured by the run. A2 needed --recount (the model's hunk header miscounted by one) — re-derive the header when applying.
# PR NOTES for the Sunday raising seat: (1) TEST-ONLY — no product change; one file, one hunk at test.ts:84-91. (2) The placeholder pin ',$14,$15)' matches TWICE in index.ts (a second 15-parameter INSERT exists) — it pins that a fifteenth placeholder exists, not that svc_api_keys' VALUES list has one; tighten to a regex anchored on svc_api_keys if you want the second half of the ticket's fix-shape (the model doubles \$ in regex literals, so that edit is the Claude seat's, not Ornith's). (3) The ticket's X2 shape also drops $15 → $14; this tamper drops only the column (a one-line tamper) — the column-list capture is the load-bearing red either way. (4) Ticket is on Kam's board account (kamil.kreiser@secuura.ai), P3 Backlog, updated 2026-09-06 — cite the gate's X2 measurement in the PR body; the ticket's own Acceptance section is the test's contract.

```diff
--- a/services/security/src/__tests__/ks869-connector-id-persisted.test.ts
+++ b/services/security/src/__tests__/ks869-connector-id-persisted.test.ts
@@ -84,7 +84,11 @@ describe('KS-869 — connector_id is persisted and read back', () => {
     // The mapper cannot see the INSERT, and the INSERT is what actually makes
     // the value durable. Asserted on the STATEMENT, with the comments stripped.
     const code = codeOf(INDEX);
-    expect(code, 'connector_id must be in the INSERT column list').toMatch(/INSERT INTO svc_api_keys[\s\S]{0,400}?connector_id/);
+    // KS-887: pin the COLUMN LIST itself. The old 400-character window reached past the column list into the
+    // ON CONFLICT COALESCE clause, so a statement that never named connector_id in its columns still passed.
+    const columnList = /INSERT INTO svc_api_keys \(([^)]*)\)/.exec(code)?.[1] ?? '';
+    expect(columnList, 'connector_id must be in the INSERT column list itself').toContain('connector_id');
+    expect(code, 'the VALUES list carries fifteen placeholders, the fifteenth for connector_id').toContain(',$14,$15)');
     expect(code, 'the value must actually be passed').toContain('k.connectorId ?? null');
     // CONTROL — the pin is on real SQL, not on a comment that mentions it.
     expect(code).toContain('INSERT INTO svc_api_keys');
   });
```
