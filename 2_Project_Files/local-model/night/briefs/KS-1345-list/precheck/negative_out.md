```diff
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -187,14 +187,16 @@
     // KS-466: organization_id is a uuid column, so the bind param needs an
     // explicit ::uuid cast — without it Postgres raises 42883 (uuid = text has
-    // no operator). The error was silently swallowed by the .catch below, so
+    // no operator). The error was silently swallowed by a .catch on this query, so
     // this list ALWAYS returned [] (a pre-existing bug, independent of RLS).
+    // KS-1345: that .catch is gone. A failed list query now reaches fail500 below
+    // (a constant 500, the error logged), never a 200 with an empty list.
     const rows = await db.$queryRaw`
       SELECT id, url, events, is_active, description, created_at, updated_at
       FROM svc_webhooks
       WHERE organization_id = ${userId}::uuid OR app_id IS NOT NULL
       ORDER BY created_at DESC
-    `.catch((e: any) => { logger.warn('webhooks list query failed', { error: e?.message }); return []; });
-
+    `.catch(() => []);
+
     res.json({ success: true, webhooks: rows });
   } catch (err: any) {
     fail500(res, 'Webhook list failed (GET /api/webhooks)', err);
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
@@ -4,11 +4,11 @@
 // file's fail500 helper and converts the first two sites; parts B and C convert the other five.
 // Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
 //
-// THE GET / TRAP. GET / chains .catch() onto its list query, so a REJECTED $queryRaw is swallowed into
-// a 200 with an empty list and never reaches the catch under test. The GET / cell therefore makes
-// $queryRaw THROW SYNCHRONOUSLY, and every red cell asserts the catch was REACHED (the logger received
-// this route's context with the thrown text), not only that the body is clean. control A0 pins the
-// swallowing branch so the trap cannot come back silently.
+// THE GET / TRAP (until KS-1345). GET / chained .catch() onto its list query, so a REJECTED $queryRaw was
+// swallowed into a 200 with an empty list and never reached the catch under test. The GET / cell therefore
+// makes $queryRaw THROW SYNCHRONOUSLY, and every red cell asserts the catch was REACHED (the logger received
+// this route's context with the thrown text), not only that the body is clean. KS-1345 removed that .catch:
+// cell A0 now pins that a REJECTED list query reaches the same catch, so the swallow cannot come back silently.
 const mockQueryRaw = jest.fn();
 const mockExecuteRaw = jest.fn();
 const mockLoggerError = jest.fn();
@@ -125,14 +125,27 @@
     expect(reply.status).toBe(500);
     expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
   });
-
-  it('control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch', async () => {
-    // PRE-EXISTING behaviour this change must NOT alter, and the reason the GET / cell throws
-    // synchronously: same route, same message, a rejected promise instead, a different answer.
+
+  it('RED KS-1345 A0: a REJECTED list query reaches the catch: a constant 500, logged once, never a 200 []', async () => {
+    // KS-1345: the list query's .catch swallowed a rejection into 200 { success: true, webhooks: [] }, so a
+    // database failure read as "no webhooks". Same route, same message, a rejected promise instead of the
+    // synchronous throw A1/A2 use: the answer must be the same.
     setNodeEnv('production');
     mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
     const res = await fetch(baseUrl + '/api/webhooks');
+    const text = await res.text();
+    expect({ status: res.status, leaked: text.includes(LEAK) }).toEqual({ status: 500, leaked: false });
+    expect(JSON.parse(text)).toEqual(CONSTANT_BODY);
+    expect(mockLoggerError.mock.calls).toEqual([['Webhook list failed (GET /api/webhooks)', { error: LEAK }]]);
+  });
+
+  it('control KS-1345 C: a list query that RESOLVES still answers 200 with its rows and logs nothing', async () => {
+    // Without this, A0 is consistent with GET / answering 500 always.
+    setNodeEnv('production');
+    const row = { id: '6f0e2c1a-1b2c-4d3e-8f40-5a6b7c8d9e0f', url: 'https://partner.example.com/hooks' };
+    mockQueryRaw.mockResolvedValueOnce([row]);
+    const res = await fetch(baseUrl + '/api/webhooks');
     expect(res.status).toBe(200);
-    expect(JSON.parse(await res.text())).toEqual({ success: true, webhooks: [] });
+    expect(JSON.parse(await res.text())).toEqual({ success: true, webhooks: [row] });
     expect(mockLoggerError).not.toHaveBeenCalled();
   });
```
