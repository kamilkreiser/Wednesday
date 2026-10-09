/**
 * =============================================================================
 * ERROR HANDLER MIDDLEWARE
 * =============================================================================
 * KS-103: previously this handler derived the status purely from
 * `res.statusCode` (which is still 200 when an error is thrown before any
 * response is sent), so every error — including the `UnauthorizedError`
 * thrown by the shared `authenticate()` middleware — collapsed to HTTP 500.
 *
 * It now normalises the error to the shared `AppError` so typed errors keep
 * their HTTP status (e.g. 401 for a missing/invalid token, 422 for Zod
 * validation) and emits the canonical `{ success, error: { code, message } }`
 * shape, while preserving referral's request-context logging.
 * =============================================================================
 */

import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';
import { AppError, BadRequestError, ValidationError, formatErrorResponse } from '@secuura/shared';
import { createLogger } from '../utils/logger';

const logger = createLogger('referral-error-handler');

/**
 * KS-445: body-parser failures reach this handler BEFORE any route runs. The
 * gateway streams /api/referral* bodies through unparsed (it skips its own
 * express.json() for proxied paths), so referral's express.json() is the
 * first thing to JSON.parse fuzzer garbage. Those failures arrive as plain
 * SyntaxErrors / http-errors carrying `.type` + `.status` — NOT AppErrors —
 * so they fell through to the 500 fallback and a client's malformed body was
 * answered as a raw INTERNAL_ERROR on POST /api/referrals/apply|generate.
 * A bad body is the client's error: answer 400 (matches the shared
 * errorHandler in @secuura/shared and auth's entity.parse.failed mapping).
 */
const isBodyParserError = (err: Error): boolean => {
  const bp = err as Error & { type?: string; status?: number };
  return (
    bp.type === 'entity.parse.failed' ||
    (err instanceof SyntaxError && 'body' in (err as object)) ||
    // Any other body-parser http-error (entity.too.large 413,
    // charset.unsupported 415, request.aborted 400, …) — all client-side
    // request problems; the spec's declared 400 covers "malformed payload,
    // missing required fields, or wrong content-type".
    (typeof bp.type === 'string' && typeof bp.status === 'number' && bp.status >= 400 && bp.status < 500)
  );
};

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
) => {
  // Normalise to an AppError so the HTTP status reflects the error type.
  const appError: AppError =
    err instanceof AppError
      ? err
      : err instanceof ZodError
        ? new ValidationError('Validation failed', err.errors)
        : isBodyParserError(err)
          ? new BadRequestError('Malformed request body')
          : // KS-727: generic on EVERY environment. The gate here was inverted
            // relative to the one fixed in packages/shared/src/errors/index.ts
            // (`=== 'development' ? leak : generic` rather than
            // `=== 'production' ? generic : leak`), which is why the sweep that
            // fixed fourteen services by grep did not match it — and why the
            // one environment it leaked on is the one that matters: KS-658
            // records the demo VM running every Node service as
            // `NODE_ENV=development`, so on the demo this was the branch that
            // always executed.
            //
            // Nothing is lost: the logger call below already records
            // `err.message` and, for 5xx, `err.stack` — so the detail still
            // reaches the operator, it just stops reaching the caller. Typed
            // errors return above carrying their own authored text.
            new AppError('An unexpected error occurred');

  logger[appError.statusCode >= 500 ? 'error' : 'warn'](`${appError.code}: ${err.message}`, {
    statusCode: appError.statusCode,
    method: req.method,
    path: req.path,
    ip: req.ip,
    userId: (req as any).user?.userId,
    ...(appError.statusCode >= 500 && { stack: err.stack }),
  });

  res.status(appError.statusCode).json(formatErrorResponse(appError));
};
