```diff
--- a/services/auth/src/routes/users.ts
+++ b/services/auth/src/routes/users.ts
@@ -13,7 +13,7 @@ import crypto from 'crypto';
 import { AuthenticatedRequest, User, UserRole, VerificationLevel, ADMIN_WRITABLE_STATUSES } from '../types';
 import { authenticate, authenticateAccessOrConnector } from '../middleware/authenticate';
 import { hashPassword, checkPasswordStrength, verifyPassword } from '../services/password';
-import { BadRequestError, NotFoundError, ValidationError } from '../middleware/errorHandler';
+import { AppError, BadRequestError, NotFoundError, ValidationError } from '../middleware/errorHandler';
 import { logger } from '../utils/logger';
 import * as userRepo from '../repositories/userRepo';
 import { revokeAllUserSessions } from '../services/session';
@@ -931,6 +931,10 @@ userRoutes.patch('/me', authenticate(), async (req: AuthenticatedRequest, res: R
 
     const updated = await userRepo.updateUser(user.id, updates);
     logger.info('User profile updated', { userId: user.id });
+    // KS-1050: a 0-row UPDATE answers null since KS-943 — never report success over it.
+    if (!updated) {
+      throw new AppError('Profile update did not persist — the update matched no row', 500, 'PROFILE_UPDATE_NOT_PERSISTED');
+    }
 
     res.json({
       success: true,
--- /dev/null
+++ b/services/auth/src/__tests__/ks1050-users-ts-933-answers-success-true.test.ts
@@ -0,0 +1,132 @@
+/**
+ * KS-1050 — PATCH /api/users/me answers `success: true` even when updateUser
+ * returns null because its UPDATE matched zero rows. The fix is to refuse that
+ * with a 500 error code PROFILE_UPDATE_NOT_PERSISTED instead of lying about
+ * persistence.
+ */
+
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+const SEED_USER_ID = 'aaaaaaaa-2222-4222-8222-aaaaaaaaaaaa';
+
+const state = vi.hoisted(() => ({
+  caller: { userId: SEED_USER_ID, role: 'USER', tenantId: 'tenant-default' },
+  users: new Map<string, Record<string, unknown>>(),
+}));
+
+const repoMock = vi.hoisted(() => ({
+  getUserById: vi.fn(async (id: string) => state.users.get(id) ?? null),
+  updateUser: vi.fn(async () => null),
+  listUsers: vi.fn(async () => []),
+  countUsers: vi.fn(async () => 0),
+  emailExists: vi.fn(async () => false),
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
+vi.mock('../db', () => ({ isDbAvailable: () => false, query: vi.fn(async () => ({ rows: [] })) }));
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
+    email: 'ada@tenant-default.example',
+    firstName: 'Ada',
+    lastName: 'Lovelace',
+    role: 'USER',
+    status: 'ACTIVE',
+    verificationLevel: 'BASIC',
+    tenantId: 'tenant-default',
+  });
+  state.caller = { userId: SEED_USER_ID, role: 'USER', tenantId: 'tenant-default' };
+});
+
+async function patchMe(body: unknown): Promise<globalThis.Response> {
+  return fetch(`${baseUrl}/me`, {
+    method: 'PATCH',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify(body),
+  });
+}
+
+describe('KS-1050 — a null updateUser must not answer success 200', () => {
+  it('🔴 KS-1050 — updateUser returns null: the response is NOT success 200', async () => {
+    repoMock.updateUser.mockResolvedValue(null);
+    const res = await patchMe({ firstName: 'Ada' });
+    expect(res.status).toBe(500);
+    const body = await res.json();
+    expect(body.success).toBe(false);
+    expect(body.error.code).toBe('PROFILE_UPDATE_NOT_PERSISTED');
+  });
+
+  it('🔴 KS-1050 — a null return never answers success: true', async () => {
+    repoMock.updateUser.mockResolvedValue(null);
+    const res = await patchMe({ firstName: 'Ada' });
+    const body = await res.json();
+    expect(body.success).not.toBe(true);
+  });
+
+  it('KS-1050 control — updateUser returns the row: 200 success with the row values', async () => {
+    const updatedRow = {
+      ...state.users.get(SEED_USER_ID),
+      firstName: 'Ada',
+      updatedAt: new Date(),
+    };
+    repoMock.updateUser.mockResolvedValue(updatedRow as any);
+    const res = await patchMe({ firstName: 'Ada' });
+    expect(res.status).toBe(200);
+    const body = await res.json();
+    expect(body.success).toBe(true);
+    expect(body.data.firstName).toBe('Ada');
+  });
+});
```
