/**
 * KS-176 regression: vc-issuer must return 401 (not 500) on missing/invalid
 * token, and the local AppError subclass must still map to its own status.
 *
 * The bug: vc-issuer wires the shared `authenticate()` (which throws the shared
 * `UnauthorizedError`) but used a *local* error handler that only matched a
 * local AppError class — so the shared 401 fell through to the 500 default.
 * The fix routes errors through the shared, AppError-aware `errorHandler` and
 * makes the local `AppError` a subclass of the shared one. This test drives the
 * real chain (shared authenticate -> service errorHandler) without DB/HTTP.
 */

import { describe, it, expect, vi } from 'vitest';
import type { Request, Response } from 'express';
import { authenticate, UnauthorizedError } from '@secuura/shared';
import { errorHandler, AppError } from '../middleware/errorHandler';

/** Minimal Response double capturing status() + json(). */
function mockRes(): Response & { _status: number; _body: unknown } {
  const res = {
    _status: 0,
    _body: undefined as unknown,
    status(code: number) {
      this._status = code;
      return this;
    },
    json(body: unknown) {
      this._body = body;
      return this;
    },
  };
  return res as unknown as Response & { _status: number; _body: unknown };
}

/** Run the error through the shared handler and return what it wrote. */
function handle(err: Error): { status: number; body: any } {
  const res = mockRes();
  errorHandler(err, {} as Request, res, vi.fn());
  return { status: res._status, body: res._body as any };
}

describe('KS-176 — vc-issuer auth error mapping', () => {
  it('returns 401 when no bearer token is provided', async () => {
    const req = { headers: {} } as Request;
    const captured: Error[] = [];
    await authenticate()(req as any, mockRes() as any, ((err?: unknown) => {
      if (err) captured.push(err as Error);
    }) as any);

    expect(captured).toHaveLength(1);
    const { status, body } = handle(captured[0]);
    expect(status).toBe(401);
    expect(body.error.code).toBe('UNAUTHORIZED');
  });

  it('maps the shared UnauthorizedError (e.g. "Invalid token") to 401, not 500', () => {
    // authenticate() emits `next(new UnauthorizedError('Invalid token'))` on a
    // bad/expired JWT. The pre-fix local handler only matched its own AppError
    // class, so this shared error fell through to the 500 default — the bug.
    const { status, body } = handle(new UnauthorizedError('Invalid token'));
    expect(status).toBe(401);
    expect(body.error.code).toBe('UNAUTHORIZED');
    expect(body.error.message).toBe('Invalid token');
  });

  it('maps the local AppError to its own status (e.g. 404 NOT_FOUND), not 500', () => {
    const { status, body } = handle(new AppError('Credential not found', 404));
    expect(status).toBe(404);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('NOT_FOUND');
    expect(body.error.message).toBe('Credential not found');
  });

  it('falls back to 500 only for genuinely unexpected errors', () => {
    const { status, body } = handle(new Error('kaboom'));
    expect(status).toBe(500);
    expect(body.error.code).toBe('INTERNAL_ERROR');
  });
});
