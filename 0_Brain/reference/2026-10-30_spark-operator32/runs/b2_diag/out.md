```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1457-audit-finish-reads-use-the-entry-path.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1457-audit-finish-reads-use-the-entry-path.test.ts
@@ -33,3 +33,4 @@
 type QueryMock = Mock<(sql: string, params: unknown[]) => Promise<{ rows: unknown[] }>>;
-type LogMock = Mock<(level: string, msg: string, ctx?: Record<string, unknown>) => void>;
+type LogMock = Mock<(level: string, msg: string, ctx?: Record<string, unknown>) => void>;
+type AuditLog = Parameters<typeof createAuditMiddleware>[0]['log'];
 const makeQuery = (): QueryMock => vi.fn(async (_sql: string, _params: unknown[]) => ({ rows: [] as unknown[] }));
@@ -47,3 +48,3 @@
   app.use(express.json());
-  app.use(createAuditMiddleware({ query: opts.query, isDbAvailable: () => true, log: opts.log }));
+  app.use(createAuditMiddleware({ query: opts.query, isDbAvailable: () => true, log: opts.log as unknown as AuditLog }));
   const handler: express.RequestHandler = (_req, res) => { res.status(opts.status).json(opts.reply); };
@@ -126,3 +127,3 @@
     app.use(express.json());
-    app.use(createAuditMiddleware({ query, isDbAvailable: () => true, log: makeLog() }));
+    app.use(createAuditMiddleware({ query, isDbAvailable: () => true, log: makeLog() as unknown as AuditLog }));
     app.use('/api/auth/login', rateLimit({
```
