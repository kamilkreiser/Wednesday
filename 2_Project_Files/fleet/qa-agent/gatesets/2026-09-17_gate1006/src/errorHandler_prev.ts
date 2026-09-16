/**
 * =============================================================================
 * ERROR HANDLER — DEMO SERVICE (KS-844)
 * =============================================================================
 * demo-service mounted no error middleware, so any error reaching express (a
 * raw 0x00 body the JSON parser refuses, a thrown route) was answered by
 * express's default handler: an HTML page carrying the stack trace and absolute
 * file paths.
 *
 * This answers JSON in the platform's error envelope instead. A 5xx never
 * carries the thrown message; a 4xx carries the parser's or route's own
 * message. It is an EXPORTED module rather than an inline `app.use((err, …))`
 * in app.ts on purpose: the KS-727 class guard (packages/shared
 * ks727-errorhandler-class-guard.test.ts) forbids a terminal inline handler in
 * a service entrypoint, and an exported one lands in its corpus 1, where it is
 * driven across every NODE_ENV with a leak canary.
 * =============================================================================
 */

import type { NextFunction, Request, Response } from 'express';

/**
 * Terminal JSON error middleware. Mounted last in `createApp()`, after the 404
 * handler. Express recognises error middleware by its four declared
 * parameters, so the unused `_next` must stay.
 */
export function errorHandler(
  err: Error & { status?: number; statusCode?: number },
  _req: Request,
  res: Response,
  _next: NextFunction,
): void {
  const status = err.status ?? err.statusCode ?? 500;
  const code = status === 400 ? 'BAD_REQUEST' : status === 413 ? 'PAYLOAD_TOO_LARGE' : status >= 500 ? 'INTERNAL_ERROR' : 'REQUEST_ERROR';
  res.status(status).json({
    success: false,
    error: { code, message: status >= 500 ? 'Internal server error' : err.message },
  });
}
