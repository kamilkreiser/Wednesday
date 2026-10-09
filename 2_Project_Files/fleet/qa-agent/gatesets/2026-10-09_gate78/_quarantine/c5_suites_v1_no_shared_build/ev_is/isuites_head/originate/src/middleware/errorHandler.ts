/**
 * =============================================================================
 * ORIGINATE GLOBAL ERROR HANDLER
 * =============================================================================
 * KS-727. This handler was written INLINE in `src/index.ts` (`app.use((err, …)`).
 * Its `message` was already safe on a 5xx (`safeMessage` redacts at >= 500 on
 * every environment), but it carried a SECOND channel that was not:
 *
 *     ...(isProduction ? {} : { details: err.message })
 *
 * so on any non-production environment the thrown message still reached the
 * caller, through `details` rather than `message`. KS-658 records the demo VM
 * running every Node service as `NODE_ENV=development`, so that spread was live
 * there. A guard asserting only on `message` would have called this clean —
 * which is why the class guard reads the whole response body as raw text.
 *
 * Being inline, it was also invisible to that guard, which discovers handlers
 * by walking for EXPORTED `errorHandler` symbols. Extracting it here puts it in
 * the corpus: `packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts`
 * imports it and drives it through a real express route across all six
 * NODE_ENV values, asserting on `message` AND `details`.
 *
 * Everything else is carried over unchanged — the 413 branch, the KS-224
 * response shape for `POST /api/verification/verify`, the structured logging,
 * and the fire-and-forget `trackError` persistence.
 * =============================================================================
 */

import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';

/**
 * Terminal error handler for originate.
 *
 * `NODE_ENV` is read at CALL time rather than through the module-load
 * `config.nodeEnv` capture the inline version used: the class guard sets
 * `process.env.NODE_ENV` per assertion, and a load-time capture would leave
 * every one of those assertions inert while still reporting green.
 */
export function errorHandler(err: Error, req: Request, res: Response, _next: NextFunction): void {
  const isProduction = (process.env.NODE_ENV || 'development') === 'production';

  // Handle body-parser payload size errors
  if ((err as Error & { type?: string }).type === 'entity.too.large') {
    res.status(413).json({
      success: false,
      error: { code: 'PAYLOAD_TOO_LARGE', message: 'Payload too large', maxSize: '10mb' },
    });
    return;
  }

  // KS-224: POST /api/verification/verify documents its errors as
  // { verified: false, error: string } (matching its own validation 400s), not
  // the platform { success, error: {...} } envelope. Malformed-body parse errors
  // are caught here by the global json parser before the route runs, so translate
  // them into the endpoint's own error shape to satisfy response_schema_conformance.
  if (
    (err as Error & { type?: string }).type === 'entity.parse.failed' &&
    req.method === 'POST' &&
    req.path === '/api/verification/verify'
  ) {
    res.status(400).json({ verified: false, error: 'Invalid JSON in request body.' });
    return;
  }

  const statusCode = (err as Error & { statusCode?: number }).statusCode || 500;
  const safeMessage = statusCode >= 500 ? 'Internal Server Error' : err.message;

  // Structured Winston logging (replaces console.error)
  logger.error('Request error', {
    message: err.message,
    statusCode,
    path: req.path,
    method: req.method,
    userId: (req as Request & { user?: { userId?: string } }).user?.userId,
    ip: req.ip,
    ...(isProduction ? {} : { stack: err.stack }),
  });

  // Persist 500-level errors to system_errors table (fire-and-forget).
  //
  // Imported lazily: `errorTrackingService` pulls in `../db` (Prisma), and this
  // module is imported directly by the KS-727 class guard. A module-load import
  // would make the guard's corpus depend on a generated Prisma client being
  // present, and the guard treats an unimportable module as a FAILED run — by
  // design, so a handler cannot drop out of the corpus silently. Deferring the
  // import keeps this module import-safe without weakening that rule.
  if (statusCode >= 500) {
    void import('../services/errorTrackingService')
      .then(({ trackError }) =>
        trackError({
          service: 'originate',
          errorType: err.name || 'UnhandledError',
          message: err.message,
          stack: err.stack,
          requestPath: req.path,
          requestMethod: req.method,
          userId: (req as Request & { user?: { userId?: string } }).user?.userId,
          ipAddress: req.ip || req.socket?.remoteAddress,
          severity: 'error',
        })
      )
      .catch(() => {}); // Never let tracking failure propagate
  }

  // KS-727: the `details: err.message` spread that used to sit here is gone.
  // `message` was already redacted at >= 500; `details` was the channel that
  // still carried the thrown text on every non-production environment. The
  // detail is still logged above, so the operator keeps it.
  res.status(statusCode).json({
    success: false,
    error: {
      code: statusCode >= 500 ? 'INTERNAL_ERROR' : 'BAD_REQUEST',
      message: isProduction && statusCode >= 500 ? 'Internal Server Error' : safeMessage,
    },
  });
}
