/**
 * qa1004-drafter-consumer.test.ts — DRAFTER probe (jest, originate). deliverWebhook with the REAL @secuura/shared (the clone's
 * dist built at head — NOT the sharedModuleMock) and `dns/promises` lookup hung. Records what the operator surfaces receive for a
 * DNS timeout: the returned error (persisted to svc_webhook_deliveries.error by dispatchEvent) and the logger.warn line.
 * webhooks.ts:462 hard-codes timeoutMs 10000, so the cell takes ~10 s.
 */
jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn() } }));
jest.mock('../middleware/auth', () => ({ authenticate: () => (_q: unknown, _s: unknown, n: () => void) => n() }));
jest.mock('../utils/logger', () => ({ logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() } }));
const lookupMock = jest.fn();
jest.mock('dns/promises', () => ({ lookup: (...a: unknown[]) => lookupMock(...a) }));
import * as fs from 'fs';
import { deliverWebhook } from '../routes/webhooks';
import { logger } from '../utils/logger';
import * as shared from '@secuura/shared';

it('C-1 a hung lookup through the real guard, as originate delivers', async () => {
  lookupMock.mockImplementation(() => new Promise(() => {}));
  const t0 = Date.now();
  const r = await deliverWebhook('https://hung-resolver.example.com/hook', 'sec', { type: 'test.ping', id: 'evt_qa' });
  const rec = { elapsed: Date.now() - t0, result: r, warn: (logger.warn as jest.Mock).mock.calls, lookupCalls: lookupMock.mock.calls.length,
    sharedIsReal: typeof (shared as any).safeOutboundRequest === 'function' && !(jest.isMockFunction((shared as any).safeOutboundRequest)) };
  fs.writeFileSync(process.env.QA1004_OUT as string, JSON.stringify(rec, null, 1));
  expect(rec.lookupCalls).toBe(1);
}, 20000);
