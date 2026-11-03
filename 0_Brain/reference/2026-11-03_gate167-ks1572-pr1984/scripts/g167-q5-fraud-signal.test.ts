/**
 * Gate 167 Q5 cells (copied into the tree under test for the run, then quarantined). The REAL route, the REAL
 * referralService.applyCode and the REAL fraudDetectionService; only the referral service's private DB methods are
 * stubbed (code lookup returns one active code, saves are no-ops) and getLinkedWalletAddress returns null.
 * Measures: what context checkFraud receives, and whether the in-memory ip/device counters are fed.
 */
import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import express from 'express';
import http from 'http';
import type { AddressInfo } from 'net';

vi.mock('../db', async (importOriginal) => ({
  ...(await importOriginal<typeof import('../db')>()),
  getLinkedWalletAddress: vi.fn(async () => null),
}));

import { referralService } from '../services/referralService';
import { fraudDetectionService } from '../services/fraudDetection';
import { referralRoutes } from '../routes/referrals';
import { errorHandler } from '../middleware/errorHandler';

const REFERRER = 'a1672aaa-1672-4672-8672-00000000000a';
const ids = Array.from({ length: 6 }, (_, i) => `b1672bbb-1672-4672-8672-00000000000${i}`);
let current = ids[0];
let server: http.Server; let base: string;
const svc = referralService as any;
const contexts: any[] = [];

beforeAll(async () => {
  vi.spyOn(svc, 'dbGetCodeByString').mockImplementation(async () => ({ id: 'code-1', code: 'G167AAAA', ownerId: REFERRER, ownerWalletAddress: undefined,
    isActive: true, maxUses: undefined, currentUses: 0, createdAt: new Date(), expiresAt: undefined }));
  vi.spyOn(svc, 'dbGetReferralByReferredUser').mockResolvedValue(null);
  vi.spyOn(svc, 'dbSaveReferral').mockResolvedValue(undefined);
  vi.spyOn(svc, 'dbSaveReferralCode').mockResolvedValue(undefined);
  vi.spyOn(svc, 'dbSaveReward').mockResolvedValue(undefined);
  const real = fraudDetectionService.checkFraud.bind(fraudDetectionService);
  vi.spyOn(fraudDetectionService, 'checkFraud').mockImplementation(async (c) => { contexts.push({ ...c }); return real(c); });
  const app = express(); app.use(express.json());
  app.use((req, _res, next) => { (req as any).user = { userId: current, role: 'USER', tenantId: 't' }; next(); });
  app.use('/api/referrals', referralRoutes); app.use(errorHandler);
  server = http.createServer(app); await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
afterAll(async () => { await new Promise<void>((r) => server.close(() => r())); });

describe('G167 Q5 fraud signal', () => {
  it('six callers, same body ip and device: what checkFraud sees, pass/fail, and the in-memory counters', async () => {
    const out: any[] = [];
    for (const id of ids) {
      current = id;
      const r = await fetch(`${base}/api/referrals/apply`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: 'G167AAAA', userId: id, ipAddress: '203.0.113.7', deviceId: 'dev-same' }) });
      const b = await r.json();
      out.push({ status: r.status, passed: b?.data?.fraudCheckPassed });
    }
    const stats = fraudDetectionService.getStats();
    const ctx = contexts.map((c) => ({ referredIp: c.referredIp, referredDeviceId: c.referredDeviceId, referrerIp: c.referrerIp, referrerDeviceId: c.referrerDeviceId }));
    console.log('G167Q5 ' + JSON.stringify({ out, stats, ctx0: ctx[0], ctx5: ctx[5], n: contexts.length }));
    expect(contexts.length).toBe(6); // control: the real checkFraud ran once per apply
  });
});
