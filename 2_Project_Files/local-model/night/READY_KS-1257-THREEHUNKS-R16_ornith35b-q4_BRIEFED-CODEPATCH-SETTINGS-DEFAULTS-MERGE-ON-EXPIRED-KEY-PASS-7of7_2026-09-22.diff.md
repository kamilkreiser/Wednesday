# READY — KS-1257-THREEHUNKS-R16 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1257-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 07:07 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1257-ornith35b-night2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1257-ornith35b-night2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1257-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_rebrief1257-drafter-precheck/1257THREEHUNKS-R16-FINAL/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:07 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1257-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `a1931d2f3f99b88748d9db49b9eb36e0572b5e5d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/admin.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	7	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
85	1	Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (12 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 12 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 7.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/admin.ts byte-exact incl. leading whitespace (apply mode strict): OK 12 line(s) byte-exact incl. leading whitespace (of 12; 12 line(s) added by the apply)` [a3i_indent.out: `OK 12 line(s) byte-exact incl. leading whitespace (of 12; 12 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts fails at the untouched tip (3 failed / 22 run; controls green; assertion reds)` [red_first.json: failed=3 of total=22; red cell(s): ['KS-1257 (#1038 gate N38-2): a write after the key expired is laid over the defaults, and GET reads them back RED KS-1257 R4b: a partial write after the key expired persists the four default categories beside what it wrote', 'KS-1257 (#1038 gate N38-2): a write after the key expired is laid over the defaults, and GET reads them back RED KS-1257 R5: a re-save with an EMPTY body after the key expired persists the defaults, not an empty document', 'KS-1257 (#1038 gate N38-2): a write after the key expired is laid over the defaults, and GET reads them back RED KS-1257 R5: after a partial write past the expiry, GET settings answers every default category and the written one']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts passes with the product hunk (22 passed / 22 run)` [green_after.json: failed=0 of total=22, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=697 failed=0 | after: total=702 failed=0` · `NEW reds: []` [baseline_suite.json total=697 failed=0; after_suite.json total=702 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +97/-8 test=src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (+12/-7 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` (+85/-1); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `a1931d2f3f99b88748d9db49b9eb36e0572b5e5d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1257-ornith35b-night2/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1257-R16-THREEHUNKS.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1257-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -1104,3 +1104,12 @@
+  // KS-1257 (#1038 / KS-1233 batch gate N38-2): the platform-settings defaults live in ONE place, frozen so no
+  // handler can mutate them; GET and PUT /api/admin/settings below lay the stored document over them, so a
+  // partial admin write after the key expired never drops a category again.
+  const PLATFORM_SETTINGS_DEFAULTS: Record<string, unknown> = Object.freeze({
+    general: Object.freeze({ platformName: 'Secuura', defaultLanguage: 'en', maintenanceMode: false }),
+    security: Object.freeze({ mfaRequired: false, sessionTimeout: 3600, passwordPolicy: 'strong' }),
+    notifications: Object.freeze({ emailEnabled: true, slackEnabled: false, webhookUrl: '' }),
+    blockchain: Object.freeze({ network: 'preprod', confirmationBlocks: 6, autoAnchor: false }),
+  });
   // =========================================================================
   // Platform Settings (Redis-backed)
   // =========================================================================
@@ -1108,11 +1117,7 @@
   router.get('/api/admin/settings', requireAdmin, async (req: Request, res: Response) => {
     const { category } = req.query;
-    const allSettings = (await redisService.getNotificationSettings('platform-settings') || {
-      general: { platformName: 'Secuura', defaultLanguage: 'en', maintenanceMode: false },
-      security: { mfaRequired: false, sessionTimeout: 3600, passwordPolicy: 'strong' },
-      notifications: { emailEnabled: true, slackEnabled: false, webhookUrl: '' },
-      blockchain: { network: 'preprod', confirmationBlocks: 6, autoAnchor: false },
-    }) as Record<string, unknown>;
+    const stored = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, unknown>;
+    const allSettings: Record<string, unknown> = { ...PLATFORM_SETTINGS_DEFAULTS, ...stored };
     if (category && typeof category === 'string' && allSettings[category]) {
       res.json({ settings: { [category]: allSettings[category] } });
     } else {
@@ -1137,7 +1142,7 @@
       }
     }
     const existing = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, unknown>;
-    const merged = { ...existing, ...body };
+    const merged = { ...PLATFORM_SETTINGS_DEFAULTS, ...existing, ...body };
     await redisService.setNotificationSettings('platform-settings', merged);
     res.json({ success: true, settings: merged, updatedAt: new Date().toISOString() });
   });
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
@@ -119,4 +119,5 @@
     const b = await dispatch(h.router, withTypes([]));
     expect([a._status, b._status, h.writes.length]).toEqual([200, 200, 2]);
-    expect(h.writes[0]).toEqual({ key: 'platform-settings', value: withTypes(['SSD_DOCUMENT']) });
+    // KS-1257: the stored document now carries the defaults beside the written category, so pin the integrations only.
+    expect([h.writes[0]?.key, (h.writes[0]?.value as any)?.integrations]).toEqual(['platform-settings', withTypes(['SSD_DOCUMENT']).integrations]);
   });
@@ -181,3 +182,86 @@
     expect([res._status, h.writes.length, lastOf4]).toEqual([200, 1, [['SSD_DOCUMENT'], ['PASSPORT'], ['SSD_DOCUMENT'], null]]);
   });
 });
+
+describe('KS-1257 (#1038 gate N38-2): a write after the key expired is laid over the defaults, and GET reads them back', () => {
+  const DEFAULT_CATEGORIES = ['general', 'security', 'notifications', 'blockchain'];
+
+  /** A stateful redis double: the key starts EXPIRED (null) and then holds whatever the last PUT stored. */
+  function buildStateful() {
+    let stored: unknown = null;
+    const writes: unknown[] = [];
+    const passThrough: RequestHandler = (_req, _res, next) => next();
+    const router = createAdminRoutes({
+      authenticateToken: () => passThrough,
+      parseTestToken: () => ADMIN,
+      query: async () => ({ rows: [], rowCount: 0 }),
+      isDbAvailable: () => false,
+      redisService: {
+        getNotificationSettings: async () => stored,
+        setNotificationSettings: async (_key: string, value: unknown) => {
+          stored = value;
+          writes.push(value);
+        },
+      },
+      services: {},
+      log: () => undefined,
+    } as unknown as AdminRouteDeps);
+    return { router, writes, current: () => stored };
+  }
+
+  function dispatchGet(router: Router): Promise<CapturedRes> {
+    return new Promise((resolve, reject) => {
+      const res = makeRes(() => resolve(res));
+      const req = {
+        method: 'GET',
+        url: '/api/admin/settings',
+        headers: { authorization: 'Bearer ks1257-admin' },
+        query: {},
+        get(name: string) {
+          return (this as any).headers[name?.toLowerCase()];
+        },
+      } as unknown as Request;
+      router(req, res as any, (err: unknown) => (err ? reject(err) : resolve(res)));
+    });
+  }
+
+  /** Which of the four default categories a document carries, in the default order. */
+  const categoriesOf = (doc: unknown) => DEFAULT_CATEGORIES.filter((c) => (doc as any)?.[c] !== undefined);
+
+  it('RED KS-1257 R4b: a partial write after the key expired persists the four default categories beside what it wrote', async () => {
+    const h = buildStateful();
+    const res = await dispatch(h.router, withTypes(['SSD_DOCUMENT']));
+    expect([res._status, h.writes.length, categoriesOf(h.current()), (h.current() as any)?.integrations])
+      .toEqual([200, 1, DEFAULT_CATEGORIES, withTypes(['SSD_DOCUMENT']).integrations]);
+  });
+
+  it('RED KS-1257 R5: a re-save with an EMPTY body after the key expired persists the defaults, not an empty document', async () => {
+    const h = buildStateful();
+    const res = await dispatch(h.router, {});
+    expect([res._status, h.writes.length, categoriesOf(h.current())]).toEqual([200, 1, DEFAULT_CATEGORIES]);
+  });
+
+  it('RED KS-1257 R5: after a partial write past the expiry, GET settings answers every default category and the written one', async () => {
+    const h = buildStateful();
+    await dispatch(h.router, withTypes(['SSD_DOCUMENT']));
+    const got = await dispatchGet(h.router);
+    const settings = (got._json as any)?.settings;
+    expect([got._status, categoriesOf(settings), settings?.general?.platformName, settings?.integrations])
+      .toEqual([200, DEFAULT_CATEGORIES, 'Secuura', withTypes(['SSD_DOCUMENT']).integrations]);
+  });
+
+  it('control: a partial write over a stored document keeps the categories it did not write', async () => {
+    const h = buildStateful();
+    await dispatch(h.router, { general: { platformName: 'Acme' } });
+    const res = await dispatch(h.router, withTypes([]));
+    expect([res._status, h.writes.length, (h.current() as any)?.general?.platformName, (h.current() as any)?.integrations])
+      .toEqual([200, 2, 'Acme', withTypes([]).integrations]);
+  });
+
+  it('control: GET settings with the key expired answers the defaults', async () => {
+    const h = buildStateful();
+    const got = await dispatchGet(h.router);
+    const settings = (got._json as any)?.settings;
+    expect([got._status, h.writes.length, categoriesOf(settings), settings?.general?.platformName]).toEqual([200, 0, DEFAULT_CATEGORIES, 'Secuura']);
+  });
+});
```
