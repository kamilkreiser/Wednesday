```diff
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks806-wallet-synthetic-email-injective.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks806-wallet-synthetic-email-injective.test.ts
new file mode 100644
index 000000000..08355812e
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks806-wallet-synthetic-email-injective.test.ts
@@ -0,0 +1,131 @@
+/**
+ * KS-806 — the synthetic wallet email must be injective over the address.
+ * `getOrCreateWalletUser` built it from `walletAddress.slice(0, 8)`, which is
+ * the constant `addr_tes` for every preview-testnet address. Two distinct
+ * wallets therefore produced ONE synthetic email. Route-contract proof with
+ * CIP-8 stubbed valid (the repo's precedent, ks796); the db stub returns NO
+ * wallet row so the CREATE branch runs, and createUser CAPTURES what it is
+ * given. This file is the checker's POSITIVE CONTROL (written by the harness
+ * builder, not the model) — kept so a checker that can never PASS is caught.
+ */
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import express from 'express';
+
+const WALLET_A = 'addr_test1qrjjw7rrks806aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
+const WALLET_B = 'addr_test1qrjjw7rrks806bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb';
+const CHALLENGE_ID = '80680680-6806-4806-8806-806806806806';
+
+const state = vi.hoisted(() => ({
+  currentWallet: 'addr_test1qrjjw7rrks806aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' as string,
+  created: [] as Array<{ email: string; walletAddress?: string }>,
+}));
+
+const silentLogger = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
+vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
+vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));
+vi.mock('../utils/cip8', () => ({
+  verifyCIP8Signature: vi.fn(async () => ({ valid: true })),
+  isValidCardanoAddress: vi.fn(() => true),
+}));
+vi.mock('../services/accountLockout', () => ({
+  isLockedOut: vi.fn(async () => false),
+  recordFailure: vi.fn(async () => 1),
+  recordSuccess: vi.fn(async () => undefined),
+}));
+vi.mock('../services/session', () => ({
+  createSession: vi.fn(async () => ({ id: 'sess-806' })),
+  getRedisClient: vi.fn(() => null),
+}));
+vi.mock('../services/jwt', () => ({
+  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_806', refreshToken: 'REFRESH_806', expiresIn: 900 })),
+}));
+vi.mock('../services/totp', () => ({
+  verifyTotpCode: vi.fn(() => false),
+  verifyBackupCode: vi.fn(async () => ({ valid: false, index: -1 })),
+}));
+vi.mock('../repositories/userRepo', () => ({
+  getUserByIdPreAuth: vi.fn(async () => null),
+  createUser: vi.fn(async (u: { email: string; walletAddress?: string }) => { state.created.push(u); return u; }),
+  updateUser: vi.fn(async () => null),
+  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
+  getUserByEmail: vi.fn(async () => null),
+}));
+vi.mock('../db', () => ({
+  query: vi.fn(async (text: string) => {
+    // No existing wallet row: every sign-in takes the CREATE branch.
+    if (text.includes('auth_find_user_by_wallet')) return { rows: [] };
+    if (text.includes('wallet_auth_challenges') && text.trim().toUpperCase().startsWith('SELECT')) {
+      return { rows: [{
+        id: CHALLENGE_ID, wallet_address: state.currentWallet, challenge: 'sign-this',
+        nonce: CHALLENGE_ID, created_at: new Date(),
+        expires_at: new Date(Date.now() + 600000), used: false,
+      }] };
+    }
+    return { rows: [] };
+  }),
+}));
+vi.mock('../middleware/authenticate', () => {
+  const passthrough = () => (_r: unknown, _s: unknown, n: () => void) => n();
+  return {
+    authenticate: passthrough, authenticateAccessOrConnector: passthrough,
+    requireRole: passthrough, requireVerificationLevel: passthrough,
+    requireOwnership: passthrough, requireSameOrganization: passthrough,
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
+afterAll(async () => { await new Promise<void>((r) => server.close(() => r())); });
+beforeEach(() => { state.created = []; });
+
+async function verifyAs(wallet: string): Promise<{ status: number; body: string }> {
+  state.currentWallet = wallet;
+  const res = await fetch(`${base}/api/auth/wallet/verify`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify({ challengeId: CHALLENGE_ID, walletAddress: wallet, signature: 'stub', key: 'stub' }),
+  });
+  return { status: res.status, body: await res.text() };
+}
+
+describe('KS-806: the synthetic wallet email is injective over the address', () => {
+  it('CONTROL — a wallet sign-in with no existing row takes the CREATE branch and mints', async () => {
+    const r = await verifyAs(WALLET_A);
+    expect(r.status, r.body).toBe(200);
+    expect(r.body).toContain('MINTED_806');
+    expect(state.created.length).toBe(1);
+    expect(state.created[0].email.endsWith('@wallet.local')).toBe(true);
+  });
+
+  it('🔴 KS-806 — two addresses sharing their first 8 characters create TWO distinct synthetic emails', async () => {
+    expect(WALLET_A.slice(0, 8)).toBe(WALLET_B.slice(0, 8));
+    expect(WALLET_A).not.toBe(WALLET_B);
+    await verifyAs(WALLET_A);
+    await verifyAs(WALLET_B);
+    expect(state.created.length).toBe(2);
+    expect(state.created[0].email.endsWith('@wallet.local')).toBe(true);
+  });
+
+  it('🔴 KS-806 — the same address always derives the same synthetic email (deterministic)', async () => {
+    await verifyAs(WALLET_A);
+    await verifyAs(WALLET_A);
+    expect(state.created.length).toBe(2);
+    expect(state.created[0].email).toBe(state.created[1].email);
+    expect(state.created[1].email.endsWith('@wallet.local')).toBe(true);
+  });
+});
diff --git a/Blockchain/Dev/services/auth/src/routes/wallet.ts b/Blockchain/Dev/services/auth/src/routes/wallet.ts
index 3134e9525..9eab6e6c9 100644
--- a/Blockchain/Dev/services/auth/src/routes/wallet.ts
+++ b/Blockchain/Dev/services/auth/src/routes/wallet.ts
@@ -197,7 +197,10 @@ async function getOrCreateWalletUser(walletAddress: string): Promise<User> {
   // Create a new wallet user via userRepo (persists to DB)
   const user: User = {
     id: uuidv4(),
-    email: `${walletAddress.slice(0, 8)}...@wallet.local`,
+    // KS-806: the local-part is a hash of the WHOLE address. slice(0, 8) was
+    // the constant `addr_tes` for every preview-testnet address, so two wallets
+    // collided on one synthetic email.
+    email: `${crypto.createHash('sha256').update(walletAddress).digest('hex').slice(0, 24)}@wallet.local`,
     emailVerified: false,
     phoneVerified: false,
     mfaEnabled: false,
```
