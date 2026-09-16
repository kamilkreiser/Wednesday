/**
 * =============================================================================
 * API VERSIONING MIDDLEWARE & HELPERS
 * =============================================================================
 * Provides API versioning support for the Secuura gateway.
 *
 * - Mounts all existing /api/* routes under /api/v1/*
 * - Adds backward-compatible redirect from /api/* to /api/v1/*
 * - Sets X-API-Version header on all responses
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';

const router = Router();

// ---------------------------------------------------------------------------
// Version Constants
// ---------------------------------------------------------------------------

/** Current active API version */
export const CURRENT_API_VERSION = 'v1';

/** Paths that should NOT be redirected to a versioned prefix */
// KS-584 P3: /api/v2/ is already versioned — without the exclusion the
// production 307 would rewrite it to the nonsense /api/v1/v2/….
const EXCLUDED_PREFIXES = ['/api/docs', '/api/health', '/api/v1/', '/api/v2/'];

// ---------------------------------------------------------------------------
// Middleware: set version header + redirect unversioned requests
// ---------------------------------------------------------------------------

/**
 * Express middleware that:
 * 1. Sets `X-API-Version` response header on every request.
 * 2. Redirects unversioned `/api/*` requests to `/api/v1/*` using 307
 *    (Temporary Redirect) so the HTTP method and body are preserved.
 */
export function versioningMiddleware() {
  return (req: Request, res: Response, next: NextFunction) => {
    // Always set the version header
    res.setHeader('X-API-Version', CURRENT_API_VERSION);

    // In production, redirect unversioned /api/* requests to /api/v1/*
    // In development, skip redirect — routes are dual-mounted at both paths
    if (
      process.env.NODE_ENV === 'production' &&
      req.path.startsWith('/api/') &&
      !EXCLUDED_PREFIXES.some((prefix) => req.path.startsWith(prefix))
    ) {
      const versionedPath = req.path.replace('/api/', `/api/${CURRENT_API_VERSION}/`);

      // Preserve query string
      const qs = req.originalUrl.includes('?')
        ? req.originalUrl.substring(req.originalUrl.indexOf('?'))
        : '';

      return res.redirect(307, `${versionedPath}${qs}`);
    }

    next();
  };
}

// ---------------------------------------------------------------------------
// Helper: mount routes at both versioned and legacy paths
// ---------------------------------------------------------------------------

/**
 * Registers a router at both `/api/v1/<path>` and `/api/<path>` so that
 * existing clients continue to work while new clients use the versioned URL.
 *
 * @param app   - Express application (or Router)
 * @param path  - Sub-path (e.g. `/documents`)
 * @param routerToMount - Express Router to mount
 */
export function mountVersionedRoutes(
  app: { use: (...args: any[]) => void },
  path: string,
  routerToMount: Router,
): void {
  // Versioned path is the canonical one
  app.use(`/api/${CURRENT_API_VERSION}${path}`, routerToMount);
  // Legacy unversioned path still works
  app.use(`/api${path}`, routerToMount);
}

export default router;
