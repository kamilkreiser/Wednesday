```
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts
@@ -62,2 +62,2 @@
 
-const { protect } = createCsrfMiddleware();
+const protect = createCsrfMiddleware().protect as (req: Request, res: Response, next: unknown) => void;
@@ -200,3 +200,3 @@
     expect(other.status).toBe(403);
-    expect((await other.json()).error.code).toBe('CSRF_TOKEN_MISSING');
+    expect(((await other.json()) as { error: { code: string } }).error.code).toBe('CSRF_TOKEN_MISSING');
   });
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/csrf.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/csrf.test.ts
@@ -58,2 +58,2 @@
 
-const { protect } = createCsrfMiddleware();
+const protect = createCsrfMiddleware().protect as (req: Request, res: Response, next: unknown) => void;
```
