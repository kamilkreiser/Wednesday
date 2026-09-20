# READY — KS-1223-REFERRALFALLBACK-1 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 05:30 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck-b/REFERRALFALLBACKUNPINNED/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 05:30 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night2/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/referral/src/__tests__/ks1223-wallet-header-fallback.test.ts` (new). `+` lines 42 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 2/2 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `HEADERFALLBACKREMOVED` → red exactly ['RED KS-1223: a principal without walletAddress plus x-wallet']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1223-REFERRALFALLBACK-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1223-ornith35b-night2/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/referral/src/__tests__/ks1223-wallet-header-fallback.test.ts
@@ -0,0 +1,42 @@
+/**
+ * KS-1223 - the referral service's wallet FALLBACK: POST /api/referrals/generate takes the wallet from the
+ * authenticated principal and, when the principal carries none, from the caller's x-wallet-address header
+ * (routes/referrals.ts, the walletAddress line that reads authUser.walletAddress || req.headers x-wallet-address). The #1106-#1111
+ * gate planted the fallback removed and measured 0 red of 26: the suite's five files mention no wallet. The real
+ * route stack is driven over loopback (the KS-444 idiom) with referralService stubbed and RECORDING what
+ * generateCode receives. A characterisation pin of TODAY's fallback - whether a caller-supplied header should
+ * decide the wallet at all is KS-1223's question for the owners, not this file's.
+ */
+import { describe, it, expect, vi } from 'vitest';
+import express from 'express';
+const { generateCode } = vi.hoisted(() => ({
+  generateCode: vi.fn(async (userId: string, walletAddress?: string) => ({ id: 'code-ks1223', code: 'KS1223AA', createdAt: new Date('2026-09-21T00:00:00Z'), expiresAt: undefined, maxUses: undefined, customLabel: undefined, ownerId: userId, ownerWalletAddress: walletAddress })),
+}));
+vi.mock('../services/referralService', () => ({ referralService: { generateCode } }));
+/** Drive the real route stack (express.json -> a stand-in for authenticate() that sets req.user -> referralRoutes) over loopback; returns [status, the walletAddress generateCode received] */
+async function generate(user: Record<string, unknown>, headers: Record<string, string>): Promise<[number, unknown]> {
+  const { referralRoutes } = await import('../routes/referrals');
+  const app = express();
+  app.use(express.json());
+  app.use((req, _res, next) => { (req as any).user = user; next(); });
+  app.use('/api/referrals', referralRoutes);
+  const server = app.listen(0, '127.0.0.1');
+  try {
+    await new Promise<void>((r) => server.once('listening', () => r()));
+    const port = (server.address() as { port: number }).port;
+    const before = generateCode.mock.calls.length;
+    const res = await fetch('http://127.0.0.1:' + String(port) + '/api/referrals/generate', { method: 'POST', headers: { 'Content-Type': 'application/json', ...headers }, body: '{}' });
+    await res.text();
+    return [res.status, generateCode.mock.calls.length === before + 1 ? generateCode.mock.calls[before][1] : 'generateCode not called once'];
+  } finally {
+    server.close();
+  }
+}
+describe('KS-1223: POST /api/referrals/generate falls back to the x-wallet-address header when the principal carries no wallet', () => {
+  it('RED KS-1223: a principal without walletAddress plus x-wallet-address: addr_client answers 201 and generateCode receives addr_client', async () => {
+    expect(await generate({ userId: 'u-ks1223' }, { 'x-wallet-address': 'addr_client' })).toEqual([201, 'addr_client']);
+  });
+  it('CONTROL: a principal WITH walletAddress wins over the header - generateCode receives addr_user', async () => {
+    expect(await generate({ userId: 'u-ks1223', walletAddress: 'addr_user' }, { 'x-wallet-address': 'addr_client' })).toEqual([201, 'addr_user']);
+  });
+});
```
