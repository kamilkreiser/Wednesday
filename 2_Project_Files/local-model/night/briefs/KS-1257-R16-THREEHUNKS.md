# KS-1257 R16-THREEHUNKS - Wednesday's task for Ornith (REBRIEF, round 2 of 2): platform-settings reads and writes are laid over ONE defaults document, so a partial admin write after the key expired never drops a category (code_patch, vitest, THREE product hunks in admin.ts - numbered, ascending, each a single context / minus / plus / context block - + the ks1230 test MODIFIED IN PLACE, unchanged from round 1) at develop a1931d2f3 (RE-PINNED at 06:41: develop moved from 64ab10513 to a1931d2f3 at 06:35 by eight merged test-only PRs #1147-#1161; routes/admin.ts and the ks1230 file are byte-identical between the two tips, so every line number below holds; written 06:30 on 2026-09-22 by Wednesday's rebrief1257 drafter from services/api-gateway/src/routes/admin.ts:1098-1160 read at the tip and ks1230-settings-write-validates-allowed-document-types.test.ts read whole, 183 lines)
Tip: `a1931d2f3f99b88748d9db49b9eb36e0572b5e5d`
Runner: `vitest`

## Premises (measured by the rebrief1257 drafter at 06:30 on 2026-09-22 AEST, in `--shared` scratchpad clones detached at 64ab10513 and, after the re-pin, at a1931d2f3; Wednesday re-derives before queueing)
- Ticket KS-1257 (P4, Backlog, unassigned, no PR attachment; the #1038 / KS-1233 batch gate's N38-2, Minor, SHIPS-WITH): "On develop, a re-save after the key has expired persisted {} for 24 h. Since #1038, it persists {} forever, and GET settings returns {}, without the defaults for every category the write didn't include. ... Merge the write over the defaults (or over the current value) instead of replacing the whole document, and pin R4b and R5 with cells." THE DRAFTER'S READING (unchanged from round 1; Wednesday may veto): the write is laid over the defaults AND the current value (`{ ...DEFAULTS, ...existing, ...body }`), and the GET lays the stored document over the same defaults, so a partial document persisted BEFORE this fix also reads its missing categories back. The four defaults are the GET's own literal at the tip (`:1111-1114`), hoisted into ONE const so the two sites cannot drift, each category wrapped in `Object.freeze`.
- ROUND 1 (`runs/2026-09-22_ks1257-ornith35b-night`, FAIL A5/A6/A7): the model's 125-line diff carried EXACTLY the golden's lines (the sorted line multisets are identical, the four `@@` headers identical and in the same order) - but inside the first product hunk it moved the ten leading `+` lines (the const) from ABOVE the hunk's first context line to BELOW its six `-` lines, i.e. it re-shaped `+ / context / - / + / context` into `context / - / + / context`. The const therefore landed INSIDE the GET handler (after `const { category } = req.query;`), the PUT could not see it (`tsc TS2304 at admin.ts:1146`), and every PUT cell went red. The lesson this brief applies: EVERY hunk is written in the one shape the model emits - leading context, then `-` lines, then `+` lines, then trailing context, ONE group of each - and the const gets its OWN pure-insertion hunk, not adjacent to any other hunk.
- A two-part split (Kam's KS-1231 shape) was MEASURED and does not exist here: the PUT-merge hunk applied ALONE at the tip type-fails (`src/routes/admin.ts(1140,25): error TS2304: Cannot find name 'PLATFORM_SETTINGS_DEFAULTS'`, `runs/2026-09-22_rebrief1257-drafter-precheck/split_measure.log`), because both sites need the ONE const and only one part may declare it; the const + GET hunks alone type-check (rc 0), the three together type-check (rc 0). The only split that stands alone on both sides duplicates the defaults literal in two scopes - the drift the ticket's "ONE document" exists to remove - so this is ONE brief with THREE numbered hunks.
- The sites at a1931d2f3 (== 64ab10513 for these two files): `admin.ts:1110-1115` (the GET's `stored || {literal}`, six lines) and `:1140` (`    const merged = { ...existing, ...body };`). The const is INSERTED above the Platform Settings banner (`:1104-1106`, three non-blank comment lines = hunk 1's trailing context; the line above, `:1103`, is blank and is NOT in the hunk). Strict `git apply --check` rc 0 measured on the three product hunks alone and on the two-file diff; no hunk is adjacent to another (hunk 1 ends at `:1106`, hunk 2 starts at `:1108`; hunk 2 ends at `:1118`, hunk 3 starts at `:1137`).
- The test file EXISTS at the tip and is MODIFIED IN PLACE (`test_file=` pin) - its two hunks are BYTE-IDENTICAL to round 1's, which the model reproduced byte for byte (measured: round 1's test section contains the fence exactly). Its control at `:121` is rewritten to pin the key and the integrations only (green on both trees); the five new cells are appended as a second `describe` after the file's last line (`:183`). No other line of the file changes.
- Typecheck (the 16th round's per-file method, the modified test file + admin.ts AFTER all three hunks; `runs/2026-09-22_rebrief1257-drafter-precheck/typecheck/typecheck_rebrief1257.log`): `r1 ks1230-settings-write-validates-allowed-document-types.test.ts: modified test file at its real path + admin.ts AFTER the three hunks -> 0 error(s) in the file(s) (0 total, rc 0)`, 06:30:52 AEST at 64ab10513 and the same line again at 06:43:05 AEST at the re-pinned a1931d2f3; a planted TS2322 control CAUGHT both times. Golden through the real code_patch checker: PASS 7/7 strict at 64ab10513 (06:31) and PASS 7/7 strict at a1931d2f3 (06:42).
- Every `+` line of both fences is ASCII-only, backslash-free and carries NO double-quote character (measured: 12 product lines, 85 test lines, 0 / 0 / 0). No blank line is asked of the model as CONTEXT or as a product `+` line (the round-1 blank `+` after the const's `});` is gone - the const now sits directly above the banner). The test fence keeps its nine blank `+` lines because the model reproduced them in round 1.
- Collision check: no PR of the 16th round touches `routes/admin.ts` or the ks1230 file; no held READY names KS-1257 or touches admin.ts. The readers of the container (`verification.ts`, `health.ts`, the held KS-1231 A/B READYs) read `integrations` only and are untouched by four extra top-level keys.

## What is wrong (one paragraph)
`PUT /api/admin/settings` (`routes/admin.ts:1123-1143`) reads the stored platform-settings document and lays the body over it (`:1139-1140`); when the key is ABSENT (it expired under the pre-#1038 TTL, or was never written) `existing` is `{}`, so a partial write - one category, or the empty body a re-save sends - persists ONLY what it carried, and since #1038 made the key permanent that partial document persists forever. `GET /api/admin/settings` (`:1108-1121`) falls back to its four-category literal only when NOTHING is stored (`:1110`), so once a partial document exists it answers that document without the defaults for the categories the write never included (the gate's rows R4b and R5). The fix hoists the literal into `PLATFORM_SETTINGS_DEFAULTS` (declared ONCE, at the factory function's scope, above the Platform Settings banner, so BOTH handlers see it), lays every write over `{ ...defaults, ...existing, ...body }` and every read over `{ ...defaults, ...stored }`. NOT in this task: the KS-1230 validation (`:1124-1138`, untouched), the allow-list readers, the Redis TTL (KS-1233, done), `/api/verification/policy` (`:1147-1159`, reads its own defaults per key).

## The exact change - THREE EDITS in the product file (three hunks, NUMBERED, in ASCENDING line order; copy all three headers)
THE ORDER IS THE TASK. Hunk 1 at `:1104` comes BEFORE hunk 2 at `:1108`, which comes BEFORE hunk 3 at `:1137`; emit them in this order, each under its own `@@` header, never merged into one hunk. Inside EVERY hunk the lines run in exactly ONE sequence: context lines, then `-` lines, then `+` lines, then context lines - never a `+` line before a `-` line, never context between a `-` and a `+`.
E1 (hunk 1, header `@@ -1104,3 +1104,12 @@`) - a PURE INSERTION: it has NO `-` line and NO leading context. Its nine `+` lines come FIRST and its three context lines (the tip's `:1104-1106`, the Platform Settings banner) come LAST, so the const is inserted ABOVE the banner, at the factory function's scope (two-space indent, the same as `router.get`), OUTSIDE every handler. Do not put any line above the nine `+` lines (the tip's `:1103` is blank). The const must NOT land inside `router.get` - if it sits after `const { category } = req.query;` the PUT cannot see it and the task fails.
E2 (hunk 2, header `@@ -1108,11 +1117,7 @@`) - the GET's six-line `stored || {literal}` (`:1110-1115`, the six `-` lines) is REPLACED by two lines; leading context `:1108-1109`, trailing context `:1116-1118`. New-side start 1117 = 1108 + the 9 lines E1 adds.
E3 (hunk 3, header `@@ -1137,7 +1142,7 @@`) - the PUT's merge (`:1140`, the one `-` line) is REPLACED by the three-way spread; leading context `:1137-1139`, trailing context `:1141-1143`. New-side start 1142 = 1137 + 9 - 4.
```
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
```
Copy every `+` line byte for byte; the `-` lines are the tip's :1110-1115 and :1140 exactly; every context line keeps its leading space. Two-space indent on the const and its comment lines (function scope), four inside its literal, four on the two replacement lines of E2 and on the one of E3. No blank line anywhere in these three hunks.

## The test - the EXISTING ks1230 file MODIFIED IN PLACE (two hunks), not a new file
File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts`
MODIFY: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` then the two hunks below with their headers exactly as printed (`@@ -119,4 +119,5 @@` rewrites the one control line `:121`; `@@ -181,3 +182,86 @@` appends the new describe after the file's last line `:183` - it has leading context only because there is no line after it). Do NOT touch any other line of the file. 85 `+` lines, 1 `-` line. These two hunks are byte-identical to round 1's, which you reproduced exactly - do the same again.
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
- RED `it('RED KS-1257 R4b: a partial write after the key expired persists the four default categories beside what it wrote')` - at the tip the stored document is `{ integrations }` only: `categoriesOf` reads `[]` where the four names are expected (the red, by assertion); after E1+E2+E3 `['general', 'security', 'notifications', 'blockchain']`.
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
* `:1104` - (correct) `  // =========================================================================` - stays (first trailing context line of E1; the const goes ABOVE it)
* `:1105` - (correct) `  // Platform Settings (Redis-backed)` - stays (trailing context of E1)
* `:1106` - (correct) `  // =========================================================================` - stays (last trailing context line of E1)
* `:1108` - (correct) `  router.get('/api/admin/settings', requireAdmin, async (req: Request, res: Response) => {` - stays (leading context of E2; the const is NOT inside this handler)
* `:1109` - (correct) `    const { category } = req.query;` - stays (leading context of E2)
* `:1116` - (correct) `    if (category && typeof category === 'string' && allSettings[category]) {` - stays (trailing context of E2)
* `:1117` - (correct) `      res.json({ settings: { [category]: allSettings[category] } });` - stays (trailing context of E2)
* `:1118` - (correct) `    } else {` - stays (trailing context of E2)
* `:1137` - (correct) `      }` - stays (leading context of E3)
* `:1138` - (correct) `    }` - stays (leading context of E3)
* `:1139` - (correct) `    const existing = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, unknown>;` - stays (leading context of E3)
* `:1141` - (correct) `    await redisService.setNotificationSettings('platform-settings', merged);` - stays (trailing context of E3)
* `:1142` - (correct) `    res.json({ success: true, settings: merged, updatedAt: new Date().toISOString() });` - stays (trailing context of E3)
* `:1143` - (correct) `  });` - stays (trailing context of E3)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts` with the E1, E2 and E3 hunks IN THAT ORDER (headers `@@ -1104,3 +1104,12 @@`, `@@ -1108,11 +1117,7 @@`, `@@ -1137,7 +1142,7 @@`), then `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts` with the two test hunks (headers `@@ -119,4 +119,5 @@` and `@@ -181,3 +182,86 @@`); no double quote, no backslash of any kind in a `+` line; every context line keeps its leading space; inside every hunk the order is context, `-`, `+`, context.
