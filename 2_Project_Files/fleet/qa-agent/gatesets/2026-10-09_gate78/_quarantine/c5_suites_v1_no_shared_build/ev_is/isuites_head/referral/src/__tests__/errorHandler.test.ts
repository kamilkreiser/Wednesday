/**
 * KS-103 — referral's error handler previously read `res.statusCode` (still
 * 200 when the error is thrown before a response), so the UnauthorizedError
 * from the shared authenticate() middleware came back as 500. It must now
 * surface as 401. Untyped errors still fall back to 500.
 *
 * KS-445 — body-parser failures (malformed JSON on POST /api/referrals/apply
 * and /generate) are plain SyntaxErrors carrying `.type`/`.status`, not
 * AppErrors, so they normalised to the 500 fallback — a client's garbage body
 * answered as a raw INTERNAL_ERROR. They must now surface as 400 BAD_REQUEST.
 */

import { describe, it, expect, vi } from 'vitest';
import express from 'express';
import type { Request, Response, NextFunction } from 'express';
import { UnauthorizedError } from '@secuura/shared';
import { errorHandler } from '../middleware/errorHandler';

// The route module pulls in referralService (DB-backed). Stub it so importing
// the routes for the HTTP-level tests never touches a real datastore.
vi.mock('../services/referralService', () => ({ referralService: {} }));

interface Captured {
  statusCode: number;
  body: { success: boolean; error: { code: string; message: string } };
}

/** Invoke referral's handler with a stub request/response, capturing output. */
function run(err: Error): Captured {
  const captured = { statusCode: 0, body: undefined } as unknown as Captured;
  const req = { method: 'GET', path: '/api/leaderboard', ip: '127.0.0.1' } as unknown as Request;
  const res = {
    status(code: number) {
      captured.statusCode = code;
      return this;
    },
    json(payload: unknown) {
      captured.body = payload as Captured['body'];
      return this;
    },
  } as unknown as Response;
  errorHandler(err, req, res, (() => undefined) as unknown as NextFunction);
  return captured;
}

describe('referral errorHandler — AppError status mapping (KS-103)', () => {
  it('returns 401 for a missing-token UnauthorizedError (was 500)', () => {
    const r = run(new UnauthorizedError('No token provided'));
    expect(r.statusCode).toBe(401);
    expect(r.body.success).toBe(false);
    expect(r.body.error.code).toBe('UNAUTHORIZED');
  });

  it('falls back to 500 for an untyped Error', () => {
    const r = run(new Error('boom'));
    expect(r.statusCode).toBe(500);
    expect(r.body.error.code).toBe('INTERNAL_ERROR');
  });
});

describe('referral errorHandler — body-parser errors are 400, not 500 (KS-445)', () => {
  it('maps entity.parse.failed (malformed JSON body) to 400 BAD_REQUEST', () => {
    // express.json() raises a SyntaxError decorated with type/status/body —
    // reproduce the exact shape body-parser hands the error middleware.
    const err = Object.assign(new SyntaxError('Unexpected token \'"\' in JSON at position 1'), {
      type: 'entity.parse.failed',
      status: 400,
      statusCode: 400,
      body: '{"',
      expose: true,
    });
    const r = run(err);
    expect(r.statusCode).toBe(400);
    expect(r.body.success).toBe(false);
    expect(r.body.error.code).toBe('BAD_REQUEST');
  });

  it('maps other body-parser 4xx http-errors (entity.too.large) to 400', () => {
    const err = Object.assign(new Error('request entity too large'), {
      type: 'entity.too.large',
      status: 413,
      statusCode: 413,
      expose: true,
    });
    const r = run(err);
    expect(r.statusCode).toBe(400);
    expect(r.body.error.code).toBe('BAD_REQUEST');
  });

  it('still 500s a plain SyntaxError with no body-parser markers', () => {
    // A SyntaxError thrown by our own code (no `.body`, no `.type`) is a real
    // server fault — it must NOT be laundered into a client error.
    const r = run(new SyntaxError('broken template'));
    expect(r.statusCode).toBe(500);
    expect(r.body.error.code).toBe('INTERNAL_ERROR');
  });
});

describe('KS-445 — POST /api/referrals/apply|generate answer 400 on malformed JSON (was raw 500)', () => {
  /**
   * Drive the real route stack (express.json → referralRoutes → errorHandler)
   * exactly as index.ts wires it, minus auth — the parse failure fires before
   * any route or auth middleware runs, which is the production path the
   * KS-440 sweep hit through the gateway (proxied bodies arrive unparsed).
   */
  async function postGarbage(path: string): Promise<{ status: number; body: Captured['body'] }> {
    const { referralRoutes } = await import('../routes/referrals');
    const app = express();
    app.use(express.json());
    app.use('/api/referrals', referralRoutes);
    app.use(errorHandler);

    const server = app.listen(0, '127.0.0.1');
    try {
      // KS-845: listen(0, host) defers the bind, so address() is null until 'listening' fires.
      await new Promise<void>((r) => server.once('listening', () => r()));
      const port = (server.address() as { port: number }).port;
      const res = await fetch(`http://127.0.0.1:${port}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{"code": "REF2026",', // truncated JSON — the fuzzer's raw-garbage class
      });
      return { status: res.status, body: (await res.json()) as Captured['body'] };
    } finally {
      server.close();
    }
  }

  it('POST /api/referrals/apply → 400 BAD_REQUEST envelope', async () => {
    const r = await postGarbage('/api/referrals/apply');
    expect(r.status).toBe(400);
    expect(r.body.success).toBe(false);
    expect(r.body.error.code).toBe('BAD_REQUEST');
  });

  it('POST /api/referrals/generate → 400 BAD_REQUEST envelope', async () => {
    const r = await postGarbage('/api/referrals/generate');
    expect(r.status).toBe(400);
    expect(r.body.success).toBe(false);
    expect(r.body.error.code).toBe('BAD_REQUEST');
  });
});
