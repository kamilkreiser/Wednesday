/**
 * =============================================================================
 * API-GATEWAY GLOBAL ERROR HANDLER
 * =============================================================================
 * KS-727. This handler was written INLINE in `src/index.ts` (`app.use((err, …)`),
 * which had two consequences, one of them live:
 *
 * 1. It returned the thrown message to the caller on every `NODE_ENV` that was
 *    not the exact string `production` — on `message` via
 *    `NODE_ENV === 'production' && statusCode >= 500 ? <generic> : err.message`,
 *    and again on `details` via a `NODE_ENV !== 'production'` spread. KS-658
 *    records the demo VM running every Node service as `NODE_ENV=development`,
 *    so on the demo that was the branch that always executed — on the one
 *    service the internet talks to.
 *
 * 2. Being inline, it was invisible to the KS-727 class guard, which discovers
 *    handlers by walking for EXPORTED `errorHandler` symbols. The guard's PR
 *    claimed the class was closed while the internet-facing instance sat
 *    outside its corpus by construction.
 *
 * Extracting it here fixes both: the redaction is unconditional on 5xx, and the
 * handler is now an exported symbol, so
 * `packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts`
 * imports it and drives it through a real express route across all six
 * NODE_ENV values on every run.
 *
 * Nothing is lost by redacting. `err.message` and `err.stack` are still logged
 * in full below, so the detail reaches the operator — it just stops reaching
 * the caller. Typed client errors (4xx) keep their authored text on every
 * environment: that text is written by us for the caller, not thrown internals.
 *
 * NOTE — the response shape is deliberately UNCHANGED from the inline version
 * (`{ success, error: { code, message } }`, with the gateway's own
 * statusCode→code mapping). Swapping to `@secuura/shared`'s `errorHandler`
 * would have been the tidier fix, but it derives its code from `err.code` and
 * ignores `err.statusCode`, and it drops this handler's request-context
 * logging (path/method/requestId/userId/ip). That is a published-contract and
 * observability change, not a refactor — filed separately rather than folded
 * into a leak fix.
 * =============================================================================
 */

import { Request, Response, NextFunction } from 'express';
import { logger as winstonLogger } from '../utils/logger';

/**
 * Map an HTTP status to the gateway's stable machine-readable error code.
 * This vocabulary is published: `ErrorResponse.code` in
 * `docs/openapi/secuura-api.yaml` documents exactly these values.
 */
function codeForStatus(statusCode: number): string {
  if (statusCode >= 500) return 'INTERNAL_ERROR';
  if (statusCode === 400) return 'BAD_REQUEST';
  if (statusCode === 401) return 'UNAUTHORIZED';
  if (statusCode === 403) return 'FORBIDDEN';
  if (statusCode === 404) return 'NOT_FOUND';
  return 'ERROR';
}

/**
 * Terminal error handler for the api-gateway.
 *
 * `NODE_ENV` is read at CALL time, not captured at module load: the class
 * guard sets `process.env.NODE_ENV` per assertion, and a module-load capture
 * would make every one of those assertions inert while still passing.
 */
export function errorHandler(err: Error, req: Request, res: Response, _next: NextFunction): void {
  const nodeEnv = process.env.NODE_ENV || 'development';
  const statusCode = (err as Error & { statusCode?: number }).statusCode || 500;

  winstonLogger.error('Unhandled error', {
    error: err.message,
    statusCode,
    path: req.path,
    method: req.method,
    requestId: (req as Request & { requestId?: string }).requestId,
    userId: (req as Request & { user?: { userId?: string } }).user?.userId,
    ip: req.ip,
    ...(nodeEnv !== 'production' ? { stack: err.stack } : {}),
  });

  // KS-727: a 5xx is redacted on EVERY environment, not only production.
  // A 4xx keeps its authored text everywhere — see the header.
  const errorMessage = statusCode >= 500 ? 'An unexpected error occurred' : err.message;

  res.status(statusCode).json({
    success: false,
    error: {
      code: codeForStatus(statusCode),
      message: errorMessage,
    },
  });
}

/**
 * Body-parser payload-size filter. Mounted BEFORE {@link errorHandler}: it
 * answers `entity.too.large` itself and passes everything else on.
 *
 * KS-727 (ask 2). This was written inline in `src/index.ts`, and the class
 * guard's corpus-2 rule classified it FILTER — and therefore exempt — because
 * its body contains a `next(err)`. That rule read one token and drew a
 * conclusion about every path. This handler ANSWERS `entity.too.large`
 * itself, so on that path it owns the response body exactly as a terminal
 * handler does, and nothing drove it: a leak added to the 413 branch would
 * have been invisible to both corpora. The classification now turns on
 * whether a body writes a response on ANY path, which makes this site
 * terminal-on-a-path, and the fix for that is the same as for a fully
 * terminal one — export it, so corpus 1 imports it and drives it through a
 * real route across every `NODE_ENV`.
 *
 * Behaviour is UNCHANGED from the inline version: the same 413 body for
 * `entity.too.large`, `next(err)` for everything else. The message is a
 * constant and no field of `err` is copied into the response.
 */
export function payloadTooLargeErrorHandler(
  err: Error,
  _req: Request,
  res: Response,
  next: NextFunction
): void {
  if ((err as Error & { type?: string }).type === 'entity.too.large') {
    res.status(413).json({
      success: false,
      error: { code: 'PAYLOAD_TOO_LARGE', message: 'Payload too large' },
    });
    return;
  }
  next(err);
}
