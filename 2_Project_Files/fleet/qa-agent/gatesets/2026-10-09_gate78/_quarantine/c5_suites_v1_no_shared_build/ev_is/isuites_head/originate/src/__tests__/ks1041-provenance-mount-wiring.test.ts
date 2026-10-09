/**
 * =============================================================================
 * KS-1041 Step 2, round 2 (PR #951 F2/C1) — the provenance middleware is
 * MOUNTED in the real originate app, ahead of the metering shim
 * =============================================================================
 * `ks1041-gateway-provenance.test.ts` proves the middleware against a COPY of
 * the metering predicate on a harness app. Nothing proved index.ts mounts it:
 * round 1 of the #951 gate deleted the mount and the full originate suite
 * stayed at its baseline (536 cells, the same two unrelated reds).
 *
 * index.ts calls `app.listen` when it is loaded. Rather than change originate's
 * boot path, this file spies on express's `application.listen` BEFORE loading
 * index.ts. express copies `application` onto each app at the moment
 * `express()` creates it, so the REAL app loads with its real mount order, the
 * real routes/metering.ts shim and the real authenticate(), and binds nothing.
 * The test serves that app on its own 127.0.0.1 listener.
 *
 * Only the metering data read is replaced: getUsageSummary returns a marker no
 * other code path produces. So the vouched cell asserts that the HANDLER ran —
 * never merely "not 401", which stays green on a route whose gate is gone.
 * =============================================================================
 */

import express from 'express';
import http from 'http';
import type { AddressInfo } from 'net';

// Synthetic, generated for this file only — never any environment's value.
const SECRET = 'ks1041-round2-synthetic-vouch'.padEnd(64, '1');
const TENANT = '11111111-1111-4111-8111-111111111111';
const FORGED = { 'x-user-role': 'connector', 'x-tenant-id': TENANT, 'x-user-id': 'attacker' };

const mockUsageMarker = {
  tenantId: 'ks1041-marker-only-getUsageSummary-returns',
  from: null,
  to: null,
  byEventType: [],
  totals: { count: 1041, adaTotal: 0, usdTotal: 0 },
};
const mockGetUsageSummary = jest.fn(async (..._args: unknown[]) => mockUsageMarker);

jest.mock('../services/chargeEvents', () => ({
  ...jest.requireActual('../services/chargeEvents'),
  getUsageSummary: (...args: unknown[]) => mockGetUsageSummary(...args),
}));

// index.ts registers these on the process at load. Removed again in afterAll so
// its uncaughtException handler (which exits the process) never outlives this file.
const PROCESS_EVENTS = ['unhandledRejection', 'uncaughtException', 'SIGTERM', 'SIGINT'] as const;
const addedListeners: Array<[string, (...args: any[]) => void]> = [];

let listenSpy: jest.SpyInstance;
let server: http.Server;
let base = '';

beforeAll(async () => {
  // config.ts refuses to load without it. Nothing connects: the only code that
  // would is index.ts's listen callback, which the spy never runs.
  process.env.DATABASE_URL = 'postgresql://ks1041:never-connected@127.0.0.1:1/ks1041';
  process.env.GATEWAY_VOUCH_SECRET = SECRET;

  const before = new Map(PROCESS_EVENTS.map((e) => [e, process.listeners(e as any).slice()]));
  // Stands in for the http.Server index.ts would get back; it only sets two timeouts on it.
  const notBound = { keepAliveTimeout: 0, headersTimeout: 0, close: (cb?: () => void) => cb?.() };
  listenSpy = jest.spyOn(express.application, 'listen').mockImplementation((() => notBound) as any);

  const mod = await import('../index');

  for (const e of PROCESS_EVENTS) {
    for (const l of process.listeners(e as any)) {
      if (!before.get(e)!.includes(l)) addedListeners.push([e, l as (...args: any[]) => void]);
    }
  }

  server = http.createServer(mod.default);
  // 127.0.0.1, never all interfaces — KS-860.
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}, 60000);

afterAll(async () => {
  // Guarded: when beforeAll could not load the app, THAT failure has to be the
  // one jest reports — not a TypeError from closing a server that never started.
  if (server) await new Promise<void>((resolve) => server.close(() => resolve()));
  for (const [e, l] of addedListeners) process.removeListener(e as any, l);
  const { stopOverloadMonitor } = await import('@secuura/shared');
  stopOverloadMonitor();
  listenSpy?.mockRestore();
  delete process.env.GATEWAY_VOUCH_SECRET;
});

describe('KS-1041 round 2 — the real originate app refuses unvouched trust headers', () => {
  it('CONTROL — the real index.ts ran to its listen call, and that call bound nothing', () => {
    expect(listenSpy).toHaveBeenCalledTimes(1);
  });

  it('C1 — forged connector headers WITHOUT a vouch get the real authenticate() 401 and never reach the handler', async () => {
    mockGetUsageSummary.mockClear();
    const res = await fetch(`${base}/api/metering/usage`, { headers: FORGED });
    expect(res.status).toBe(401);
    await expect(res.json()).resolves.toMatchObject({
      error: { code: 'UNAUTHORIZED', message: 'Authentication required' },
    });
    expect(mockGetUsageSummary).not.toHaveBeenCalled();
  });

  it('the same request WITH the gateway vouch reaches the real handler through the metering shim', async () => {
    mockGetUsageSummary.mockClear();
    const res = await fetch(`${base}/api/metering/usage`, { headers: { ...FORGED, 'x-gateway-vouch': SECRET } });
    expect(res.status).toBe(200);
    await expect(res.json()).resolves.toEqual({ success: true, data: mockUsageMarker });
    expect(mockGetUsageSummary).toHaveBeenCalledWith(TENANT, undefined, undefined);
  });
});
