/**
 * KS-914 A-4/A-5 — `deliverWebhook` must keep "we refused to send" separate
 * from "their endpoint was down".
 *
 * Two comments in the first round claimed the two "stay distinguishable at the
 * call site". They were not: the failure arm was a bare `{ok:false; error}`
 * with nothing to branch on, so both cases took the same branch, logged the
 * same line and persisted the same `status 0 / success false`. The string
 * `blocked by SSRF guard` went from two files to zero, and the loss lands on
 * two operator-facing surfaces — the persisted `svc_webhook_deliveries.error`
 * and the `delivery.error` of the `/test` response.
 *
 * The gate also observed that `deliverWebhook` has NO unit test at either SHA,
 * which is why the A-1 timeout defect would have been caught by nothing. These
 * cells are the start of that coverage, scoped to the distinction this round
 * restores. Each cell is pinned to ITS branch — the returned error string AND
 * the log line — because a cell that only asserts "some failure" passes on
 * either branch and measures nothing.
 */

jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn() } }));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));
jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

const mockSafeOutboundRequest = jest.fn();
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    encryptField: (v: unknown) => v,
    decryptField: (v: unknown) => v,
    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
    assertSafeOutboundUrl: jest.fn(),
    safeOutboundRequest: (...args: unknown[]) => mockSafeOutboundRequest(...args),
  }),
);

import { deliverWebhook } from '../routes/webhooks';
import { logger } from '../utils/logger';

const warn = logger.warn as unknown as jest.Mock;

describe('KS-914 deliverWebhook — blocked vs failed', () => {
  beforeEach(() => {
    mockSafeOutboundRequest.mockReset();
    warn.mockReset();
  });

  it('a guard refusal is prefixed `blocked by SSRF guard:` and logged as blocked', async () => {
    mockSafeOutboundRequest.mockResolvedValue({
      ok: false,
      reason: 'blocked',
      error: 'host "evil.example" resolves to 10.0.0.1, which is forbidden: RFC1918 private (10.0.0.0/8)',
    });

    const r = await deliverWebhook('https://evil.example/hook', 'sec', { type: 'x', id: 'y' });

    expect(r.status).toBe(0);
    expect(r.success).toBe(false);
    // The prefix is the operator-facing half. It is restored verbatim, because
    // it is what anyone grepping delivery history is already looking for.
    expect(r.error).toMatch(/^blocked by SSRF guard: /);
    expect(r.error).toContain('RFC1918');
    expect(warn).toHaveBeenCalledWith(
      'webhook delivery blocked by SSRF guard',
      expect.objectContaining({ url: 'https://evil.example/hook' }),
    );
  });

  it('a transport failure is NOT prefixed, and is logged as a failure', async () => {
    mockSafeOutboundRequest.mockResolvedValue({
      ok: false,
      reason: 'request_failed',
      error: 'request exceeded its 10000ms deadline (connect, transfer and drain)',
    });

    const r = await deliverWebhook('https://subscriber.example/hook', 'sec', { type: 'x', id: 'y' });

    expect(r.status).toBe(0);
    expect(r.success).toBe(false);
    // THE DISCRIMINATOR. Without the reason tag this string is identical to the
    // blocked case's, which is exactly the defect this round closes.
    expect(r.error).not.toMatch(/blocked by SSRF guard/);
    expect(r.error).toBe('request exceeded its 10000ms deadline (connect, transfer and drain)');
    expect(warn).toHaveBeenCalledWith(
      'webhook delivery failed',
      expect.objectContaining({ url: 'https://subscriber.example/hook' }),
    );
  });

  it('a delivered webhook reports the destination status and logs no warning', async () => {
    mockSafeOutboundRequest.mockResolvedValue({ ok: true, response: { ok: true, status: 202 } });

    const r = await deliverWebhook('https://subscriber.example/hook', 'sec', { type: 'x', id: 'y' });

    expect(r.status).toBe(202);
    expect(r.success).toBe(true);
    expect(r.error).toBeUndefined();
    expect(warn).not.toHaveBeenCalled();
  });

  it('passes a TOTAL deadline to the guard, not a socket-idle timer', async () => {
    mockSafeOutboundRequest.mockResolvedValue({ ok: true, response: { ok: true, status: 200 } });

    await deliverWebhook('https://subscriber.example/hook', 'sec', { type: 'x', id: 'y' });

    expect(mockSafeOutboundRequest).toHaveBeenCalledWith(
      'https://subscriber.example/hook',
      expect.objectContaining({ timeoutMs: 10000, method: 'POST' }),
    );
  });
});
