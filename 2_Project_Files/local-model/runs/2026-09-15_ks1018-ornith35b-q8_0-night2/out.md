```diff
--- a/Blockchain/Dev/services/auth/src/routes/users.ts
+++ b/Blockchain/Dev/services/auth/src/routes/users.ts
@@ -13,7 +13,7 @@ import crypto from 'crypto';
 import { AuthenticatedRequest, User, UserRole, VerificationLevel, ADMIN_WRITABLE_STATUSES } from '../types';
 import { authenticate, authenticateAccessOrConnector } from '../middleware/authenticate';
 import { hashPassword, checkPasswordStrength, verifyPassword } from '../services/password';
-import { BadRequestError, NotFoundError, ValidationError } from '../middleware/errorHandler';
+import { BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from '../middleware/errorHandler'; // KS-1018: rethrow infra errors as 503
 import { logger } from '../utils/logger';
 import * as userRepo from '../repositories/userRepo';
+import { isInfrastructureDbError } from '../repositories/dbErrors'; // KS-1018: predicate for infra-error detection
 import { revokeAllUserSessions } from '../services/session';
@@ -1180,7 +1180,10 @@ async function getVerificationRequest(id: string): Promise<VerificationRequest |
           reviewedBy: r.reviewed_by || undefined,
           rejectionReason: r.rejection_reason || undefined,
         };
       }
-    } catch { /* fall through */ }
+    } catch (err: any) { // KS-1018: name the error and rethrow infrastructure failures as 503
+      logger.error('DB getVerificationRequest failed', { error: err?.message, code: err?.code });
+      if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
+    }
   }
   return memVerificationRequests.get(id) || null;
 }
@@ -1201,7 +1204,10 @@ async function findPendingVerificationRequest(userId: string): Promise<Verifica
         };
       }
       return null;
     }
-    } catch { /* fall through */ }
+    } catch (err: any) { // KS-1018: name the error and rethrow infrastructure failures as 503
+      logger.error('DB findPendingVerificationRequest failed', { error: err?.message, code: err?.code });
+      if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
+    }
   }
   return Array.from(memVerificationRequests.values()).find(
     r => r.userId === userId && r.status === 'PENDING'
@@ -1223,7 +1229,10 @@ async function listUserVerificationRequests(userId: string): Promise<Verificati
         reviewedAt: r.reviewed_at?.toISOString?.() || r.reviewed_at || undefined,
         reviewedBy: r.reviewed_by || undefined,
         rejectionReason: r.rejection_reason || undefined,
       }));
     }
-    } catch { /* fall through */ }
+    } catch (err: any) { // KS-1018: name the error and rethrow infrastructure failures as 503
+      logger.error('DB listUserVerificationRequests failed', { error: err?.message, code: err?.code });
+      if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
+    }
   }
   return Array.from(memVerificationRequests.values())
     .filter(r => r.userId === userId)

--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts
@@ -0,0 +1,165 @@
+/**
+ * KS-1018 — three verification-store reads swallow EVERY DB error with a bare
+ * `catch { }` and answer from an in-memory map. A DB outage therefore reads as
+ * "no such request". This file asserts that after the fix each of those catches
+ * names the error, logs it, and RETHROWS an infrastructure failure as 503.
+ *
+ * The mocking shape mirrors ks1013-admin-patch-malformed-id.test.ts: hoisted
+ * repoMock for userRepo, authenticate injecting state.caller, db mocked with
+ * isDbAvailable=true and a programmatic query fn, errorHandler on the app. We do
+ * NOT mock ../repositories/dbErrors so the real predicate is under test.
+ */
+
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const SEED_USER_ID = 'aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa';
+
+const state = vi.hoisted(() => ({
+  caller: { userId: SEED_USER_ID, role: 'USER' },
+  users: new Map<string, Record<string, unknown>>(),
+}));
+
+const repoMock = vi.hoisted(() => ({
+  getUserById: vi.fn(async (id: string) => state.users.get(id) ?? null),
+  updateUser: vi.fn(async () => null),
+  createUser: vi.fn(async (user: Record<string, unknown>) => user),
+}));
+vi.mock('../repositories/userRepo', () => repoMock);
+
+vi.mock('../middleware/authenticate', () => {
+  const injectCaller =
+    () => (req: express.Request & { user?: unknown }, _res: express.Response, next: express.NextFunction) => {
+      (req as { user: unknown }).user = { ...state.caller };
+      next();
+    };
+  return { authenticate: injectCaller, authenticateAccessOrConnector: injectCaller };
+});
+
+// db is mocked but NOT stubbed to succeed by default — each cell programs its own rejection / success via dbQuery.
+const dbState = vi.hoisted(() => ({
+  query: vi.fn(async (_sql: string, _params?: any[]) => ({ rows: [] })),
+}));
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: dbState.query,
+}));
+
+vi.mock('../services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
+vi.mock('../services/password', () => ({
+  hashPassword: vi.fn(async () => 'hashed'),
+  checkPasswordStrength: vi.fn(() => ({ ok: true })),
+  verifyPassword: vi.fn(async () => true),
+}));
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+import { userRoutes } from '../routes/users';
+import { errorHandler } from '../middleware/errorHandler';
+
+let server: Server;
+let baseUrl: string;
+
+beforeAll(async () => {
+  const app = express();
+  app.use(express.json());
+  app.use('/', userRoutes);
+  app.use(errorHandler);
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => {
+      const { port } = server.address() as AddressInfo;
+      baseUrl = `http://127.0.0.1:${port}`;
+      resolve();
+    });
+  });
+});
+
+afterAll(async () => {
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+});
+
+beforeEach(() => {
+  vi.clearAllMocks();
+  state.users.clear();
+  state.users.set(SEED_USER_ID, {
+    id: SEED_USER_ID,
+    email: 'a@tenant-a.example',
+    role: 'USER',
+    status: 'ACTIVE',
+    verificationLevel: 'BASIC',
+    tenantId: 'tenant-default',
+  });
+  state.caller = { userId: SEED_USER_ID, role: 'USER' };
+  // Default to a successful empty result so the control cell can run without reprogramming — but each test overrides via mockRejectedValue when needed.
+  (dbState.query as any).mockResolvedValue({ rows: [] });
+});
+
+const infraError = Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' });
+
+describe('KS-1018 — three verification-store reads swallow EVERY DB error with a bare catch {} and answer from an in-memory map', () => {
+  it('🔴 KS-1018 — GET /me/verification: a refused DB connection answers 503, not 200 from memory', async () => {
+    (dbState.query as any).mockRejectedValue(infraError);
+    const res = await fetch(`${baseUrl}/me/verification`);
+    expect(res.status).toBe(503);
+    const body = await res.json();
+    expect(body.error.code).toBe('SERVICE_UNAVAILABLE');
+  });
+
+  it('🔴 KS-1018 — POST /verification/:id/review as SYSTEM_ADMIN: a refused DB connection answers 503, not 404', async () => {
+    state.caller = { userId: SEED_USER_ID, role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' };
+    repoMock.getUserById.mockImplementation(async (id: string) => state.users.get(id) ?? null);
+    (dbState.query as any).mockRejectedValue(infraError);
+    const res = await fetch(`${baseUrl}/verification/some-id/review`, {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json' },
+      body: JSON.stringify({ action: 'approve' }),
+    });
+    expect(res.status).toBe(503);
+    const body = await res.json();
+    expect(body.error.code).toBe('SERVICE_UNAVAILABLE');
+  });
+
+  it('KS-1018 control — a non-infrastructure DB error still falls through to the in-memory map', async () => {
+    (dbState.query as any).mockRejectedValue(Object.assign(new Error('relation does not exist'), { code: '42P01' }));
+    const res = await fetch(`${baseUrl}/me/verification`);
+    expect(res.status).toBe(200);
+    const body = await res.json();
+    expect(body.data.requests).toEqual([]);
+  });
+});

```
