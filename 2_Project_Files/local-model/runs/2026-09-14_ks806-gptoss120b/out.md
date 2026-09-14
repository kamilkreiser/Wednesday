```diff
--- a/Blockchain/Dev/services/auth/src/routes/wallet.ts
+++ b/Blockchain/Dev/services/auth/src/routes/wallet.ts
@@ -165,7 +165,7 @@
   // Create a new wallet user via userRepo (persists to DB)
   const user: User = {
     id: uuidv4(),
-    email: `${walletAddress.slice(0, 8)}...@wallet.local`,
+    // KS-806: use hash of full wallet address for synthetic email to avoid collisions
+    email: `${crypto.createHash('sha256').update(walletAddress).digest('hex').slice(0, 24)}...@wallet.local`,
     emailVerified: false,
     phoneVerified: false,
     mfaEnabled: false,
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks806-wallet-synthetic-email-injective.test.ts
@@ -0,0 +1,145 @@
+/**
+ * KS-806 — synthetic email injective test
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+
+const WALLET1 = 'addr_test1qrjjw7rrks796exampleaddress0000000000000000000000';
+const WALLET2 = 'addr_test1qrjjw7rrks796differentaddress1111111111111111111111';
+const CHALLENGE_ID = '11111111-2222-4333-8444-555555555555';
+
+const state = vi.hoisted(() => ({
+  status: 'ACTIVE' as string,
+  mfaEnabled: false,
+  mfaSecret: 'JBSWY3DPEHPK3PXP' as string | null,
+  lockedOut: false,
+}));
+
+const silentLogger = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+
+vi.mock('../utils/cip8', () => ({
+  verifyCIP8Signature: vi.fn(async () => ({ valid: true })),
+  isValidCardanoAddress: vi.fn(() => true),
+}));
+
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false),
+  recordFailure: vi.fn(),
+  recordSuccess: vi.fn(),
+}));
+
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 'sess-806' })),
+  getRedisClient: vi.fn(() => null),
+}));
+
+vi.mock('../services/jwt', () => ({
+  generateTokenPair: vi.fn(() => ({
+    accessToken: 'MINTED_WALLET_ACCESS_TOKEN',
+    refreshToken: 'MINTED_WALLET_REFRESH',
+    expiresIn: 900,
+  })),
+}));
+
+vi.mock('../services/totp', () => ({
+  verifyTotpCode: vi.fn((_s: string, code: string) => code === '123456'),
+  verifyBackupCode: vi.fn(async () => ({ valid: false, index: -1 })),
+}));
+
+const createdUsers: any[] = [];
+vi.mock('../repositories/userRepo', () => ({
+  getUserByIdPreAuth: vi.fn(async () => null),
+  createUser: vi.fn(async (u: any) => { createdUsers.push(u); return u; }),
+  updateUser: vi.fn(async () => null),
+  reencryptMfaSecretIfLegacy: vi.fn(),
+  getUserByEmail: vi.fn(),
+}));
+
+let challengeCall = 0;
+vi.mock('../db', () => ({
+  query: vi.fn(async (text: string) => {
+    if (text.includes('auth_find_user_by_wallet')) return { rows: [] };
+    if (text.includes('wallet_auth_challenges') && text.trim().toUpperCase().startsWith('SELECT')) {
+      const wallet = challengeCall === 0 ? WALLET1 : WALLET2;
+      challengeCall++;
+      return { rows: [{ 
+        id: CHALLENGE_ID,
+        wallet_address: wallet,
+        challenge: 'sign-this',
+        nonce: CHALLENGE_ID,
+        created_at: new Date(),
+        expires_at: new Date(Date.now() + 600000),
+        used: false,
+      }] };
+    }
+    return { rows: [] };
+  }),
+}));
+
+vi.mock('../middleware/authenticate', () => {
+  const passthrough = () => (_r: unknown, _s: unknown, n: () => void) => n();
+  return {
+    authenticate: passthrough,
+    authenticateAccessOrConnector: passthrough,
+    requireRole: passthrough,
+    requireVerificationLevel: passthrough,
+    requireOwnership: passthrough,
+    requireSameOrganization: passthrough,
+  };
+});
+vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));
+
+let server: Server;
+let base: string;
+
+beforeAll(async () => {
+  const { walletRoutes } = await import('../routes/wallet');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  const app = express();
+  app.use(express.json());
+  app.use('/api/auth/wallet', walletRoutes);
+  app.use(errorHandler);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+});
+
+afterAll(async () => {
+  await new Promise<void>((r) => server.close(() => r()));
+});
+
+beforeEach(() => {
+  createdUsers.length = 0;
+  challengeCall = 0;
+});
+
+async function verify(walletAddress: string): Promise<{ status: number; body: string }> {
+  const res = await fetch(`${base}/api/auth/wallet/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({
+      challengeId: CHALLENGE_ID,
+      walletAddress,
+      signature: 'stub-signature',
+      key: 'stub-key',
+    }),
+  });
+  return { status: res.status, body: await res.text() };
+}
+
+describe('KS-806 — synthetic email injective', () => {
+  it('🔴 KS-806 — two wallets with same prefix get different synthetic emails', async () => {
+    const res1 = await verify(WALLET1);
+    expect(res1.status).toBe(200);
+    const res2 = await verify(WALLET2);
+    expect(res2.status).toBe(200);
+    expect(createdUsers.length).toBe(2);
+    const email1 = createdUsers[0].email;
+    const email2 = createdUsers[1].email;
+    expect(email1).not.toBe(email2);
+  });
+});
```
