# READY — KS-1912-KS-1912-O137-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/out.md.checker/patch.diff`** (from `ls` at 15:24 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 15:24 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx , Blockchain/Dev/frontend/admin/src/services/api.ts } + { Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx` (product) and `Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
11	2	Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx
5	4	Blockchain/Dev/frontend/admin/src/services/api.ts
79	0	Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: ClientList.tsx api.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx`, `Blockchain/Dev/frontend/admin/src/services/api.ts`; test(s): `Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx 11 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/frontend/admin/src/services/api.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx 79 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx` (hunks=4, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/frontend/admin/src/services/api.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1912 client list shows a refused status move or delete RED ks1912 R1 a refused status move shows the server message on the page', 'KS-1912 client list shows a refused status move or delete RED ks1912 R2 a refused Delete shows the server message on the page']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=0 failed=0 | after: total=4 failed=0` · `NEW reds: []` [baseline_suite.json total=0 failed=0; after_suite.json total=4 failed=0]
- A6 [verbatim]: `PASS A6 whole frontend/admin suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for frontend/admin: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx` (+11/-2 per numstat.out) and the test file `Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx` (+79/-0); 3 files in all (code_patch2: products Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx, Blockchain/Dev/frontend/admin/src/services/api.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/input.json`. Brief (given by --brief; its `# ` heading names KS-1912): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/KS-1912.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1912_o137_p1_admin_client_list_shows_the_servers_refusal_of_a_status_move_or_delete/checker.out`.

```diff
diff --git a/Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx b/Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx
--- a/Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx
+++ b/Blockchain/Dev/frontend/admin/src/pages/platform/ClientList.tsx
@@ -41,4 +41,6 @@
   const [keyError, setKeyError] = useState('');
   const [success, setSuccess] = useState('');
+  // KS-1912: the server's refusal of a status move or a Delete (the create dialog keeps its own `error`).
+  const [actionError, setActionError] = useState('');
   const [keyFileJson, setKeyFileJson] = useState<string | null>(null);
   const fileInputRef = useRef<HTMLInputElement>(null);
@@ -80,4 +82,5 @@
   const handleStatusChange = async (tenant: Tenant, status: string) => {
-    await updateTenantStatus(tenant.id, status);
+    const result = await updateTenantStatus(tenant.id, status);
+    setActionError(result.ok ? '' : result.error || 'Failed to change the client status');
     load();
   };
@@ -85,5 +88,6 @@
   const handleDelete = async (tenant: Tenant) => {
     if (!confirm(`Delete client "${tenant.name}"? This cannot be undone.`)) return;
-    await deleteTenant(tenant.id);
+    const result = await deleteTenant(tenant.id);
+    setActionError(result.ok ? '' : result.error || 'Failed to delete the client');
     load();
   };
@@ -158,3 +162,8 @@
+      {actionError && (
+        <Alert variant="destructive" className="mb-4">
+          <AlertDescription>{actionError}</AlertDescription>
+        </Alert>
+      )}
       {success && (
         <Alert className="mb-4 border-green-500/30 bg-green-500/10">
           <AlertDescription className="text-green-400">{success}</AlertDescription>
diff --git a/Blockchain/Dev/frontend/admin/src/services/api.ts b/Blockchain/Dev/frontend/admin/src/services/api.ts
--- a/Blockchain/Dev/frontend/admin/src/services/api.ts
+++ b/Blockchain/Dev/frontend/admin/src/services/api.ts
@@ -1074,7 +1074,8 @@
-export async function updateTenantStatus(id: string, status: string): Promise<boolean> {
+export async function updateTenantStatus(id: string, status: string): Promise<{ ok: boolean; error?: string }> {
   const res = await request(`/api/platform/tenants/${id}/status`, {
     method: 'PATCH',
     body: JSON.stringify({ status }),
   });
-  return res.ok;
+  // KS-1912: the server's refusal text (a 409 on a move it does not allow) reaches the page instead of a bare false.
+  return res.ok ? { ok: true } : { ok: false, error: describeFailure(res.error, 'Failed to change the client status') };
 }
@@ -1082,7 +1083,7 @@
-export async function deleteTenant(id: string): Promise<boolean> {
+export async function deleteTenant(id: string): Promise<{ ok: boolean; error?: string }> {
   const res = await request(`/api/platform/tenants/${id}`, {
     method: 'DELETE',
     body: JSON.stringify({ confirm: true }),
   });
-  return res.ok;
+  return res.ok ? { ok: true } : { ok: false, error: describeFailure(res.error, 'Failed to delete the client') };
 }
diff --git a/Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx b/Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/frontend/admin/src/__tests__/ks1912-client-list-shows-a-refused-status-move-or-delete.test.tsx
@@ -0,0 +1,79 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+import { render, screen, fireEvent, waitFor } from '@testing-library/react';
+
+// KS-1912: the admin client list awaits updateTenantStatus / deleteTenant, ignores the answer and reloads, so when the server refuses a
+// status move (a 409 on a move it does not allow) or a Delete the operator sees no change and no message. The page now shows the server's
+// text. Harness: the REAL page and the REAL services/api.ts; only the network (fetch) and the router hook are replaced, and the row menu
+// (a Radix dropdown) is opened the way a keyboard user does it (Enter on the trigger).
+const h = vi.hoisted(() => ({
+  refuse: '' as string,
+  calls: [] as Array<{ url: string; method: string; body: string }>,
+}));
+
+vi.mock('react-router', () => ({ useNavigate: () => () => undefined }));
+
+const TENANT = { id: 't1', name: 'Acme Pty', slug: 'acme', status: 'active', created_at: '2026-01-01T00:00:00.000Z' };
+
+const reply = (status: number, body: unknown) => ({ ok: status >= 200 && status < 300, status, json: async () => body });
+
+beforeEach(() => {
+  h.refuse = '';
+  h.calls = [];
+  vi.stubGlobal(
+    'fetch',
+    vi.fn(async (url: string, init?: { method?: string; body?: string }) => {
+      const method = (init?.method || 'GET').toUpperCase();
+      h.calls.push({ url, method, body: String(init?.body ?? '') });
+      if (method === 'GET' && url === '/api/platform/tenants') return reply(200, { tenants: [TENANT] });
+      if (method === 'GET' && url.includes('/tenant-key/')) return reply(200, { keyLoaded: false });
+      if (method === 'PATCH' || method === 'DELETE') return h.refuse ? reply(409, { error: h.refuse }) : reply(200, { success: true });
+      return reply(404, {});
+    }),
+  );
+});
+
+afterEach(() => {
+  vi.unstubAllGlobals();
+});
+
+import ClientList from '../pages/platform/ClientList';
+
+const LISTS = () => h.calls.filter((c) => c.method === 'GET' && c.url === '/api/platform/tenants').length;
+
+async function pick(item: string) {
+  render(<ClientList />);
+  await screen.findByText('Acme Pty');
+  const trigger = document.querySelector('[aria-haspopup="menu"]') as HTMLElement;
+  fireEvent.keyDown(trigger, { key: 'Enter' });
+  fireEvent.click(await screen.findByText(item));
+}
+
+describe('KS-1912 client list shows a refused status move or delete', () => {
+  it('control ks1912 C1 an accepted status move is sent, the list reloads and no refusal text shows', async () => {
+    await pick('Suspend');
+    await waitFor(() => expect(LISTS()).toBe(2));
+    const patch = h.calls.find((c) => c.method === 'PATCH');
+    expect(patch?.url).toBe('/api/platform/tenants/t1/status');
+    expect(JSON.parse(patch?.body || '{}')).toEqual({ status: 'suspended' });
+    expect(screen.queryByText(/Cannot change/)).toBeNull();
+  });
+
+  it('control ks1912 C2 a Delete the operator declines is never sent', async () => {
+    vi.stubGlobal('confirm', () => false);
+    await pick('Delete');
+    expect(h.calls.some((c) => c.method === 'DELETE')).toBe(false);
+  });
+
+  it('RED ks1912 R1 a refused status move shows the server message on the page', async () => {
+    h.refuse = 'Cannot change tenant status from active to archived';
+    await pick('Archive');
+    await waitFor(() => expect(screen.queryByText('Cannot change tenant status from active to archived')).not.toBeNull());
+  });
+
+  it('RED ks1912 R2 a refused Delete shows the server message on the page', async () => {
+    h.refuse = 'Tenant is already archived';
+    vi.stubGlobal('confirm', () => true);
+    await pick('Delete');
+    await waitFor(() => expect(screen.queryByText('Tenant is already archived')).not.toBeNull());
+  });
+});
```
