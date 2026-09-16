/**
 * =============================================================================
 * CSRF PROTECTION MIDDLEWARE
 * =============================================================================
 * Implements Cross-Site Request Forgery protection using the Double Submit Cookie
 * pattern with additional synchronizer token validation.
 * 
 * Protection includes:
 * - Double Submit Cookie pattern (cookie + header comparison)
 * - Per-request token generation
 * - Token rotation after each request
 * - SameSite cookie attributes
 * - Origin validation
 * 
 * Reference: OWASP CSRF Prevention Cheat Sheet
 * =============================================================================
 */

import { Request, RequestHandler } from 'express';
import crypto from 'crypto';
import { logger } from '../utils/logger';

// =============================================================================
// CONFIGURATION
// =============================================================================

interface CsrfConfig {
  /** Name of the cookie containing the CSRF token */
  cookieName: string;
  /** Name of the header containing the CSRF token from client */
  headerName: string;
  /** Secret used for token generation (should be from environment) */
  secret: string;
  /** Cookie secure flag (should be true in production) */
  secure: boolean;
  /** Cookie SameSite attribute */
  sameSite: 'strict' | 'lax' | 'none';
  /** Token expiration in milliseconds */
  tokenExpiry: number;
  /** Methods that require CSRF validation */
  protectedMethods: string[];
  /** Paths to exclude from CSRF protection */
  excludedPaths: string[];
  /** Allowed origins for origin validation */
  allowedOrigins: string[];
}

// SECURITY: Validate CSRF_SECRET is set before creating config
const CSRF_SECRET = process.env.CSRF_SECRET;
if (!CSRF_SECRET && process.env.NODE_ENV === 'production') {
  console.error('[CSRF] FATAL: CSRF_SECRET is required in production for security!');
  console.error('[CSRF] FATAL: Production startup blocked due to missing CSRF_SECRET.');
  process.exit(1);
}

const DEFAULT_CONFIG: CsrfConfig = {
  cookieName: 'XSRF-TOKEN',
  headerName: 'X-XSRF-TOKEN',
  secret: CSRF_SECRET || crypto.randomBytes(32).toString('hex'),
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict',
  tokenExpiry: 3600000, // 1 hour
  protectedMethods: ['POST', 'PUT', 'PATCH', 'DELETE'],
  // H21 (2026-04-28): excluded auth lifecycle endpoints. Each gets its
  // own per-route CSRF defence by virtue of the cookie attributes:
  //   - login / register / wallet/* — pre-session; no CSRF token to send.
  //     Browser-side defence is the form being a POST with JSON body
  //     (CSRF attacks via image/form tags can't set Content-Type).
  //   - refresh / logout — protected by the refresh-token cookie itself,
  //     which is httpOnly + sameSite: strict. A cross-site forger can't
  //     get that cookie sent at all (sameSite blocks it cross-origin),
  //     so CSRF on refresh/logout is structurally impossible. The
  //     test-reported H21 (admin SPA bouncing on every refresh) fixes
  //     here. /webhooks/ are signed by the upstream provider.
  // 2026-05-05: also excluded the /api/verification/verify* family.
  // These are documented as Public endpoints, the verifier portal calls
  // them anonymously (no auth, no session), and they only return
  // verification metadata about a requested document — there is no user
  // state for a forger to mutate. Without this exclusion the verifier
  // portal cannot complete a verification because its safeFetch wrapper
  // doesn't attach the X-XSRF-TOKEN header.
  excludedPaths: [
    '/health',
    '/api/auth/login',
    '/api/auth/register',
    '/api/auth/refresh',
    '/api/auth/logout',
    '/api/auth/wallet/challenge',
    '/api/auth/wallet/authenticate',
    // Verification endpoint is public-read by design: third-party clients
    // (Outlook add-in, Gmail add-on, custom verifier scripts) call it to
    // look up a content hash. It performs no state-changing operation —
    // POST is used for the request body only. CSRF doesn't apply to
    // read-only RPCs that don't carry session-derived authority. Origin
    // is still checked via CORS_ORIGINS for browser callers; non-browser
    // callers (no Origin header) fall through to the rate limiter.
    // (startsWith match covers /verify, /verify-file, /verify-batch.)
    '/api/verification/verify',
    // KS-1165: the v2 twins are published anonymous (security: []) like v1 — same exclusion, same startsWith rule.
    '/api/v2/verification/verify',
    // Client-side logger sink — sendBeacon fires-and-forgets a JSON batch
    // of warn/error events from the SPA's logger. No session auth, no
    // CSRF interaction; the body is already sanitised client-side. Origin
    // is still policed by CORS for browser callers.
    '/api/logs',
    '/webhooks/',
  ],
  allowedOrigins: process.env.CORS_ORIGINS?.split(',') || (() => {
    const isDev = process.env.NODE_ENV !== 'production';
    const prodOrigins = [
      'https://secuura.io',
      'https://issuer.secuura.io',
      'https://verifier.secuura.io',
    ];
    const devOrigins = [
      'http://localhost:6100',
      'http://localhost:6101',
      'http://localhost:6102',
      'http://localhost:6103',
      'http://localhost:6882',
      'http://localhost:6881',
    ];
    return isDev ? [...devOrigins, ...prodOrigins] : prodOrigins;
  })(),
};

// =============================================================================
// TOKEN GENERATION & VALIDATION
// =============================================================================

interface TokenPayload {
  /** Random token value */
  value: string;
  /** Token creation timestamp */
  timestamp: number;
  /** Request fingerprint */
  fingerprint: string;
}

/**
 * Generate a CSRF token with embedded timestamp and fingerprint
 */
function generateToken(fingerprint: string, secret: string): string {
  const payload: TokenPayload = {
    value: crypto.randomBytes(32).toString('hex'),
    timestamp: Date.now(),
    fingerprint,
  };
  
  const data = JSON.stringify(payload);
  const signature = crypto
    .createHmac('sha256', secret)
    .update(data)
    .digest('hex');
  
  // Combine data and signature in URL-safe base64
  const token = Buffer.from(`${data}.${signature}`).toString('base64url');
  return token;
}

/**
 * Validate a CSRF token
 */
function validateToken(
  token: string,
  fingerprint: string,
  secret: string,
  maxAge: number
): { valid: boolean; reason?: string } {
  try {
    // Decode the token
    const decoded = Buffer.from(token, 'base64url').toString();
    const [data, providedSignature] = decoded.split('.');
    
    if (!data || !providedSignature) {
      return { valid: false, reason: 'Invalid token format' };
    }
    
    // Verify signature
    const expectedSignature = crypto
      .createHmac('sha256', secret)
      .update(data)
      .digest('hex');
    
    if (!crypto.timingSafeEqual(
      Buffer.from(providedSignature),
      Buffer.from(expectedSignature)
    )) {
      return { valid: false, reason: 'Invalid token signature' };
    }
    
    // Parse and validate payload
    const payload: TokenPayload = JSON.parse(data);
    
    // Check timestamp
    const age = Date.now() - payload.timestamp;
    if (age > maxAge) {
      return { valid: false, reason: 'Token expired' };
    }
    
    // Check fingerprint (optional - may differ for legitimate reasons)
    // This is a soft check - log but don't reject
    if (payload.fingerprint !== fingerprint) {
      logger.warn('[CSRF] Token fingerprint mismatch - possible session hijack attempt');
    }
    
    return { valid: true };
  } catch (error) {
    return { valid: false, reason: 'Token validation error' };
  }
}

/**
 * Generate a request fingerprint from client characteristics
 */
function getRequestFingerprint(req: Request): string {
  const components = [
    req.ip,
    req.headers['user-agent'] || '',
    // Don't include accept headers as they can change legitimately
  ];
  
  return crypto
    .createHash('sha256')
    .update(components.join('|'))
    .digest('hex')
    .substring(0, 16);
}

// =============================================================================
// ORIGIN VALIDATION
// =============================================================================

/**
 * Validate the request origin against allowed origins
 */
function validateOrigin(req: Request, allowedOrigins: string[]): boolean {
  const origin = req.headers.origin;
  const referer = req.headers.referer;
  
  // If no origin header, check referer
  const sourceUrl = origin || (referer ? new URL(referer).origin : null);
  
  if (!sourceUrl) {
    // No origin information — in development, allow API clients (Playwright, curl, etc.)
    // that don't send Origin headers. In production, reject to prevent CSRF.
    if (process.env.NODE_ENV !== 'production') {
      return true;
    }
    return false;
  }
  
  // Check against allowed origins
  return allowedOrigins.some(allowed => {
    // Support wildcards for subdomains
    if (allowed.includes('*')) {
      const pattern = allowed.replace(/\*/g, '[^.]+');
      return new RegExp(`^${pattern}$`).test(sourceUrl);
    }
    return sourceUrl === allowed;
  });
}

// =============================================================================
// MIDDLEWARE FACTORY
// =============================================================================

/**
 * Create CSRF protection middleware with custom configuration
 */
export function createCsrfMiddleware(customConfig: Partial<CsrfConfig> = {}): {
  protect: RequestHandler;
  generateToken: RequestHandler;
} {
  const config: CsrfConfig = { ...DEFAULT_CONFIG, ...customConfig };
  
  // Warn if using default secret in production
  if (process.env.NODE_ENV === 'production' && !process.env.CSRF_SECRET) {
    logger.error('[CSRF] Using generated secret in production — set CSRF_SECRET environment variable');
  }
  
  /**
   * Middleware to generate and set CSRF token cookie
   */
  const generateTokenMiddleware: RequestHandler = (req, res, next) => {
    const fingerprint = getRequestFingerprint(req);
    const token = generateToken(fingerprint, config.secret);
    
    // Set the CSRF token cookie
    res.cookie(config.cookieName, token, {
      httpOnly: false, // Client needs to read this
      secure: config.secure,
      sameSite: config.sameSite,
      maxAge: config.tokenExpiry,
      path: '/',
    });
    
    // Also expose token in response header for SPAs
    res.setHeader('X-CSRF-Token', token);
    
    next();
  };
  
  /**
   * Middleware to validate CSRF token on protected requests
   */
  const protectMiddleware: RequestHandler = (req, res, next) => {
    // Skip for excluded paths
    if (config.excludedPaths.some(path => req.path.startsWith(path))) {
      return next();
    }

    // Skip for unprotected methods
    if (!config.protectedMethods.includes(req.method)) {
      return next();
    }

    // KS-428: CSRF applies only to requests carrying ambient authority —
    // credentials the browser attaches automatically (cookies). The previous
    // guard was inverted: it skipped CSRF when Authorization was absent and
    // enforced it on Bearer requests, protecting exactly the requests that
    // cannot be forged and waving through the shape it was written to stop.
    //
    //   - Header-credentialled requests (Authorization: Bearer, x-api-key)
    //     skip CSRF: those credentials live in the client (localStorage /
    //     memory / config), are never auto-attached cross-site — no CSRF
    //     attack surface.
    //   - Requests with no cookies skip CSRF: no ambient authority means
    //     nothing for a cross-site attacker to ride, and the auth middleware
    //     401s them next. This preserves the KS-3 DRIFT-AUTH-403-VS-401 fix
    //     (the spec documents 401 for missing Authorization; CSRF must not
    //     pre-empt it with a 403).
    //   - Requests WITH cookies and no header credential get the full
    //     origin + double-submit validation. No CSRF-protected route reads
    //     auth from a cookie today (verified KS-428: the only cookie reads
    //     in services/ are auth refresh/logout, both in excludedPaths and
    //     defended by httpOnly + sameSite:strict) — this branch is
    //     defence-in-depth for any future cookie-session route.
    if (req.headers.authorization?.startsWith('Bearer ') || req.headers['x-api-key']) {
      return next();
    }
    if (!req.headers.cookie) {
      return next();
    }

    // Validate origin for all protected requests
    if (!validateOrigin(req, config.allowedOrigins)) {
      logger.warn('[CSRF] Origin validation failed', {
        origin: req.headers.origin,
        referer: req.headers.referer,
        path: req.path,
        ip: req.ip,
      });
      res.status(403).json({
        success: false,
        error: {
          code: 'CSRF_ORIGIN_INVALID',
          message: 'Invalid request origin',
        },
      });
      return;
    }
    
    // Get token from cookie
    const cookieToken = req.cookies?.[config.cookieName];
    
    // Get token from header
    const headerToken = req.headers[config.headerName.toLowerCase()] as string;
    
    // Both tokens must be present
    if (!cookieToken || !headerToken) {
      logger.warn('[CSRF] Missing CSRF token', {
        hasCookie: !!cookieToken,
        hasHeader: !!headerToken,
        path: req.path,
        ip: req.ip,
      });
      res.status(403).json({
        success: false,
        error: {
          code: 'CSRF_TOKEN_MISSING',
          message: 'Missing CSRF token',
        },
      });
      return;
    }
    
    // Tokens must match (timing-safe comparison)
    try {
      if (!crypto.timingSafeEqual(
        Buffer.from(cookieToken),
        Buffer.from(headerToken)
      )) {
        logger.warn('[CSRF] Token mismatch', {
          path: req.path,
          ip: req.ip,
        });
        res.status(403).json({
          success: false,
          error: {
            code: 'CSRF_TOKEN_MISMATCH',
            message: 'CSRF token mismatch',
          },
        });
        return;
      }
    } catch {
      res.status(403).json({
        success: false,
        error: {
          code: 'CSRF_TOKEN_INVALID',
          message: 'Invalid CSRF token format',
        },
      });
      return;
    }
    
    // Validate the token structure and expiry
    const fingerprint = getRequestFingerprint(req);
    const validation = validateToken(cookieToken, fingerprint, config.secret, config.tokenExpiry);
    
    if (!validation.valid) {
      logger.warn('[CSRF] Token validation failed', {
        reason: validation.reason,
        path: req.path,
        ip: req.ip,
      });
      res.status(403).json({
        success: false,
        error: {
          code: 'CSRF_TOKEN_INVALID',
          message: validation.reason || 'Invalid CSRF token',
        },
      });
      return;
    }
    
    // Token is valid - proceed
    next();
  };
  
  return {
    protect: protectMiddleware,
    generateToken: generateTokenMiddleware,
  };
}

// =============================================================================
// EXPORTS
// =============================================================================

export const csrfMiddleware = createCsrfMiddleware();

/**
 * Helper to get a new CSRF token (for API endpoints)
 */
export function getCsrfToken(req: Request): string {
  const fingerprint = getRequestFingerprint(req);
  return generateToken(fingerprint, DEFAULT_CONFIG.secret);
}

export default csrfMiddleware;
