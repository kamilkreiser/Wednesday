/**
 * =============================================================================
 * ERROR HANDLER MIDDLEWARE
 * =============================================================================
 * vc-issuer routes through the shared @secuura/shared `errorHandler` (the same
 * AppError-aware handler the 12 services in KS-111 adopted). The previous local
 * handler only recognised a *local* AppError class, so the shared middleware's
 * `UnauthorizedError` (thrown by `authenticate()` in index.ts) fell through to a
 * 500 — turning every missing/invalid-token rejection into a server error
 * instead of a 401 (KS-176).
 *
 * `AppError` is kept here as a thin subclass of the shared AppError so the
 * existing `new AppError(message, statusCode)` throws across the route files
 * keep working unchanged AND get matched by the shared handler. The error `code`
 * is derived from the status so the canonical envelope stays honest (a 404 is
 * NOT_FOUND, not INTERNAL_ERROR).
 * =============================================================================
 */

import { AppError as SharedAppError, errorHandler } from '@secuura/shared';

/** Default error codes by HTTP status, matching the shared error subclasses. */
const CODE_BY_STATUS: Record<number, string> = {
  400: 'BAD_REQUEST',
  401: 'UNAUTHORIZED',
  403: 'FORBIDDEN',
  404: 'NOT_FOUND',
  409: 'CONFLICT',
  422: 'VALIDATION_ERROR',
  429: 'RATE_LIMIT_EXCEEDED',
  503: 'SERVICE_UNAVAILABLE',
};

/**
 * Local AppError kept for back-compat with the route files' `new AppError(msg,
 * status)` throws. Extends the shared AppError so the shared `errorHandler`
 * matches it (`instanceof SharedAppError`) and returns the right status; the
 * `code` is derived from the status when not given explicitly.
 */
export class AppError extends SharedAppError {
  constructor(message: string, statusCode = 500, code?: string, details?: unknown) {
    super(message, statusCode, code ?? CODE_BY_STATUS[statusCode] ?? 'INTERNAL_ERROR', true, details);
  }
}

export { errorHandler };
