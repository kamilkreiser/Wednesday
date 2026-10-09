/**
 * KS-431 — webhook :id path-param guard.
 *
 * The webhook write routes (PATCH/DELETE /:id, POST /:id/rotate-secret, /:id/test) cast
 * :id into raw SQL as `${id}::uuid`. Before this guard, a well-formed-but-non-UUID id
 * (e.g. "0") made Postgres throw `22P02 invalid input syntax for type uuid`, which fell
 * through to a raw 500 — reachable for the first time once KS-428 unblocked write paths.
 * `rejectInvalidWebhookId` now returns 400 for a pattern-malformed id and 404 for a
 * well-formed-but-non-UUID id, before any query runs.
 */

import type { Response } from 'express';

// The guard is pure, but importing the router pulls in ../db → ../config, which
// requires DATABASE_URL at load. Mock the transitive infra (same approach as
// ks423-contract-alignments.test.ts) so the unit test stays offline.
jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn() } }));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));
jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import { rejectInvalidWebhookId } from '../routes/webhooks';

/** Minimal Express Response double capturing the status + JSON body the guard emits. */
function mockRes(): Response & { statusCode?: number; body?: unknown } {
  const res: Partial<Response> & { statusCode?: number; body?: unknown } = {};
  // status() records the code and returns `res` so the guard can chain .json().
  res.status = ((code: number) => {
    res.statusCode = code;
    return res as Response;
  }) as Response['status'];
  // json() records the payload the guard sent on rejection.
  res.json = ((payload: unknown) => {
    res.body = payload;
    return res as Response;
  }) as Response['json'];
  return res as Response & { statusCode?: number; body?: unknown };
}

describe('KS-431 rejectInvalidWebhookId', () => {
  it('accepts a canonical UUID (no response sent, returns false)', () => {
    const res = mockRes();
    // A real uuid is usable — the guard must let the handler proceed.
    expect(rejectInvalidWebhookId('a1b2c3d4-5678-4abc-9def-0123456789ab', res)).toBe(false);
    expect(res.statusCode).toBeUndefined();
  });

  it('rejects a well-formed-but-non-UUID id as 404 (the "0" → 22P02 → 500 case)', () => {
    const res = mockRes();
    // "0" satisfies the spec id grammar but is not a UUID → cannot reference a row → 404, never 500.
    expect(rejectInvalidWebhookId('0', res)).toBe(true);
    expect(res.statusCode).toBe(404);
    expect(res.body).toMatchObject({ success: false, error: { code: 'NOT_FOUND' } });
  });

  it('rejects a pattern-malformed id as 400', () => {
    const res = mockRes();
    // A space violates the published id grammar → 400 BAD_REQUEST.
    expect(rejectInvalidWebhookId('not a valid id', res)).toBe(true);
    expect(res.statusCode).toBe(400);
    expect(res.body).toMatchObject({ success: false, error: { code: 'BAD_REQUEST' } });
  });

  it('rejects an empty id as 400', () => {
    const res = mockRes();
    // Empty string fails the leading-char requirement of the grammar → 400.
    expect(rejectInvalidWebhookId('', res)).toBe(true);
    expect(res.statusCode).toBe(400);
  });
});
