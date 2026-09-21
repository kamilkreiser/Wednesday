# KS-1257 R16-DEFAULTSMERGE - Wednesday's task for Ornith: platform-settings reads and writes are laid over ONE defaults document, so a partial admin write after the key expired never drops a category (code_patch, vitest, TWO product hunks in admin.ts + the ks1230 test MODIFIED IN PLACE) at develop 64ab10513 (written 05:56 on 2026-09-22 by Wednesday's feed5 drafter from services/api-gateway/src/routes/admin.ts:1104-1159 read at the tip and ks1230-settings-write-validates-allowed-document-types.test.ts read whole, 183 lines)
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the feed5 drafter at 05:56 on 2026-09-22 AEST, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- Ticket KS-1257 (P4, Backlog, unassigned, no PR attachment; the #1038 / KS-1233 batch gate's N38-2, Minor, SHIPS-WITH): "On develop, a re-save after the key has expired persisted {} for 24 h. Since #1038, it persists {} forever, and GET settings returns {}, without the defaults for every category the write didn't include. ... Merge the write over the defaults (or over the current value) instead of replacing the whole document, and pin R4b and R5 with cells." THE DRAFTER'S READING (Wednesday may veto): the write is laid over the defaults AND the current value (`{ ...DEFAULTS, ...existing, ...body }`) - the current value already wins over the defaults today when the key is present, so this is the ticket's two options in one spread, not a choice between them; and the GET lays the stored document over the same defaults, so a partial document persisted BEFORE this fix (the ticket's "forever" on kintsugi) also reads its missing categories back. The four defaults are the GET's own literal at the tip (`:1111-1114`), hoisted into ONE const so the two sites cannot drift - each category wrapped in `Object.freeze` (the defaults are shared by every request, so no handler may mutate them; the spread copies them anyway), which also keeps every added line distinct from the six removed ones (the builder's context-as-addition gate refused the first draft at 05:57, whose four category lines were byte-identical to the GET's).
- The sites at 64ab10513: `admin.ts:1110-1115` (the GET's `stored || {literal}`, six lines) and `:1140` (`    const merged = { ...existing, ...body };`). Two hunks in ONE product file; the first inserts the const with TRAILING context (`:1108-1109`, the GET's opening lines, no blank line in either hunk); strict `git apply --check` rc 0 measured on the product hunks alone and on the two-file diff.
- The test file EXISTS at the tip and is MODIFIED IN PLACE (`test_file=` pin): its control at `:121` pins the stored value as exactly the body (`expect(h.writes[0]).toEqual({ key: 'platform-settings', value: withTypes(['SSD_DOCUMENT']) })`) - true at the tip, FALSE after the fix (the stored document now carries the four defaults beside `integrations`), so that ONE line is rewritten to pin the key and the integrations only (green on both trees); the five new cells are appended as a second `describe` after the file's last line (`:183`). No other line of the file changes. The file's existing stub answers `getNotificationSettings` null for every read (the expired-key shape) and its `dispatch` is PUT-only, so the new describe carries its own stateful double (`buildStateful`) and a `dispatchGet`, reusing the file's `makeRes`, `dispatch`, `ADMIN`, `withTypes`, `createAdminRoutes` and its imported types.
- Typecheck (the 16th round's per-file method, the modified test file + admin.ts AFTER both hunks; `runs/2026-09-22_feed5-drafter-precheck/typecheck/typecheck_feed5.log`, 05:55:50 AEST): 0 errors in the file, 0 total (rc 0); a planted TS2322 CAUGHT.
- Every `+` line of both fences is ASCII-only, backslash-free and carries NO double-quote character (measured: 13 product lines, 85 test lines, 0 / 0 / 0; odd-quote lines []). The word `password` appears in one `+` line only inside the hoisted literal `passwordPolicy: 'strong'`, byte-identical to the tip's `:1112`.
- Collision check: no PR of the 16th round touches `routes/admin.ts` or the ks1230 file (Seat C 16th's api-gateway files are ks864c/ks1123/ks1073/ks1185/ks1199/ks1204 test files, system-status.ts and verification.ts); no held READY names KS-1257 or touches admin.ts (`ls night/READY_* | grep -c -i -E '1257|admin'` = 0). The readers of the container (`verification.ts:1214/1260`, `health.ts:47`, the held KS-1231 A/B READYs) read `integrations` only and are untouched by four extra top-level keys.

## What is wrong (one paragraph)
`PUT /api/admin/settings` (`routes/admin.ts:1123-1143`) reads the stored platform-settings document and lays the body over it (`:1139-1140`); when the key is ABSENT (it expired under the pre-#1038 TTL, or was never written) `existing` is `{}`, so a partial write - one category, or the empty body a re-save sends - persists ONLY what it carried, and since #1038 made the key permanent that partial document persists forever. `GET /api/admin/settings` (`:1108-1121`) falls back to its four-category literal only when NOTHING is stored (`:1110`), so once a partial document exists it answers that document without the defaults for the categories the write never included (the gate's rows R4b and R5). The fix hoists the literal into `PLATFORM_SETTINGS_DEFAULTS`, lays every write over `{ ...defaults, ...existing, ...body }` and every read over `{ ...defaults, ...stored }`. NOT in this task: the KS-1230 validation (`:1124-1138`, untouched), the allow-list readers, the Redis TTL (KS-1233, done), `/api/verification/policy` (`:1147-1159`, reads its own defaults per key).

## The exact change - TWO EDITS in the product file (two hunks; copy both headers)
E1 - `services/api-gateway/src/routes/admin.ts`: the const is INSERTED before the GET (`:1108`), and the GET's six-line `stored || {literal}` (`:1110-1115`, the six `-` lines) is REPLACED by two lines. Hunk header `@@ -1108,9 +1108,15 @@`. Two-space indent on the const (function scope, the same as `router.get`), four inside its literal, four on the two replacement lines.
E2 - the PUT's merge (`:1140`, the one `-` line) is REPLACED by the three-way spread. Hunk header `@@ -1139,3 +1145,3 @@` (new-side start 1145 = 1139 + the 6 lines E1 adds).
```
@@ -1108,9 +1108,15 @@
+  // KS-1257 (#1038 / KS-1233 batch gate N38-2): the defaults live in one place, frozen so no handler can
+  // mutate them, and every read and every write is laid over them - a partial admin write after the key
+  // expired never drops a category again.
+  const PLATFORM_SETTINGS_DEFAULTS: Record<string, unknown> = Object.freeze({
+    general: Object.freeze({ platformName: 'Secuura', defaultLanguage: 'en', maintenanceMode: false }),
+    security: Object.freeze({ mfaRequired: false, sessionTimeout: 3600, passwordPolicy: 'strong' }),
+    notifications: Object.freeze({ emailEnabled: true, slackEnabled: false, webhookUrl: '' }),
+    blockchain: Object.freeze({ network: 'preprod', confirmationBlocks: 6, autoAnchor: false }),
+  });
+
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
@@ -1139,3 +1145,3 @@
     const existing = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, unknown>;
-    const merged = { ...existing, ...body };
+    const merged = { ...PLATFORM_SETTINGS_DEFAULTS, ...existing, ...body };
     await redisService.setNotificationSettings('platform-settings', merged);
```
Copy every `+` line byte for byte (the blank `+` line after the const's closing `});` is a `+` with nothing after it); the `-` lines are the tip's :1110-1115 and :1140 exactly; every context line keeps its leading space.

## The test - the EXISTING ks1230 file MODIFIED IN PLACE (two hunks), not a new file
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts`
MODIFY: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` then the two hunks below with their headers exactly as printed (`@@ -119,4 +119,5 @@` rewrites the one control line `:121`; `@@ -181,3 +182,86 @@` appends the new describe after the file's last line `:183` - it has leading context only because there is no line after it). Do NOT touch any other line of the file. 85 `+` lines, 1 `-` line.
```
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
Cells (every NEW cell RED or CONTROL, nothing optional; the rewritten `:121` control keeps its title and is green on both trees):
- RED `it('RED KS-1257 R4b: a partial write after the key expired persists the four default categories beside what it wrote')` - at the tip the stored document is `{ integrations }` only: `categoriesOf` reads `[]` where the four names are expected (the red, by assertion); after E1+E2 `['general', 'security', 'notifications', 'blockchain']`.
- RED `it('RED KS-1257 R5: a re-save with an EMPTY body after the key expired persists the defaults, not an empty document')` - at the tip an empty body after expiry stores `{}` (categories `[]`); after the fix, the four defaults.
- RED `it('RED KS-1257 R5: after a partial write past the expiry, GET settings answers every default category and the written one')` - at the tip GET answers the stored `{ integrations }` (categories `[]`, no `general`); after the fix every default category plus `integrations`, `general.platformName` `'Secuura'`.
- CONTROL `it('control: a partial write over a stored document keeps the categories it did not write')` - the current value wins over the defaults and the body wins over the current value on both trees: `general.platformName` stays `'Acme'`, `integrations` is the second write's.
- CONTROL `it('control: GET settings with the key expired answers the defaults')` - with nothing stored GET answers the four defaults on both trees (the tip's `||` literal; after the fix the same document through the spread), 0 writes.
- (rewritten) `it('control: an array of strings and an empty array are stored with 200')` - its last expectation now pins `[key, integrations]`; green on both trees.

## Red cells
- RED KS-1257 R4b: a partial write after the key expired persists the four default categories beside what it wrote
- RED KS-1257 R5: a re-save with an EMPTY body after the key expired persists the defaults, not an empty document
- RED KS-1257 R5: after a partial write past the expiry, GET settings answers every default category and the written one

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:1110` - **must change**: `    const allSettings = (await redisService.getNotificationSettings('platform-settings') || {`
* `:1111` - **must change**: `      general: { platformName: 'Secuura', defaultLanguage: 'en', maintenanceMode: false },`
* `:1112` - **must change**: `      security: { mfaRequired: false, sessionTimeout: 3600, passwordPolicy: 'strong' },`
* `:1113` - **must change**: `      notifications: { emailEnabled: true, slackEnabled: false, webhookUrl: '' },`
* `:1114` - **must change**: `      blockchain: { network: 'preprod', confirmationBlocks: 6, autoAnchor: false },`
* `:1115` - **must change**: `    }) as Record<string, unknown>;`
* `:1140` - **must change**: `    const merged = { ...existing, ...body };`
* `:1108` - (correct) `  router.get('/api/admin/settings', requireAdmin, async (req: Request, res: Response) => {` - stays (the const goes ABOVE it)
* `:1109` - (correct) `    const { category } = req.query;` - stays
* `:1116` - (correct) `    if (category && typeof category === 'string' && allSettings[category]) {` - stays (trailing context of E1)
* `:1139` - (correct) `    const existing = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, unknown>;` - stays (leading context of E2)
* `:1141` - (correct) `    await redisService.setNotificationSettings('platform-settings', merged);` - stays (trailing context of E2)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts` with the E1 and E2 hunks (headers `@@ -1108,9 +1108,15 @@` and `@@ -1139,3 +1145,3 @@`), then `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` with the two test hunks (headers `@@ -119,4 +119,5 @@` and `@@ -181,3 +182,86 @@`); no double quote, no `\$` / `\u` / backslash of any kind in a `+` line; every context line keeps its leading space.
