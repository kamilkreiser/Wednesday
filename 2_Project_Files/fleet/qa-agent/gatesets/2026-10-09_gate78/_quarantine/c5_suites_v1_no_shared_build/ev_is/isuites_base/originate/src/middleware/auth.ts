/**
 * =============================================================================
 * AUTHENTICATION & AUTHORIZATION MIDDLEWARE
 * =============================================================================
 * JWT validation and role-based access control for the Originate service.
 * =============================================================================
 */

import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { isSessionActive } from '@secuura/shared';
import { verifyJwtRs256 } from '@secuura/shared/crypto/jwks';
import { logger } from '../utils/logger';

export interface JwtPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  /**
   * KS-764 (Peter's #799 review, finding 3): DECLARED because a policy reads it.
   *
   * `decideTenantAccess` — which `decideKeyRevoke` delegates to — compares
   * `user.tenantId` against the target and returns `403 caller has no tenant`
   * when it is absent (`keyRevokePolicy.ts:175`). Until this line, no payload
   * type declared the field: the revoke routes worked only because the auth
   * service HAPPENS to sign it in, and `services/auth/src/services/jwt.ts:263`
   * signs it CONDITIONALLY — `...(meta.tenantId ? { tenantId } : {})` — so a
   * tenant-less user genuinely receives a token without the claim.
   *
   * The dependency was real, load-bearing and invisible to the compiler, which
   * is what made it undeclared rather than merely optional. Declaring it does
   * not change behaviour; it makes the contract checkable, so a future token
   * minter can see what the authorisation path requires.
   */
  tenantId?: string;
  verificationLevel: string;
  // KS-257: session id minted by auth at login; present on interactive JWTs.
  sessionId?: string;
  // KS-151: role-derived scopes minted by auth (`getDefaultScopesForRole`).
  // `isAllowedByRoleOrScope` in `./rbac.ts` reads this to grant scoped
  // callers (e.g. OWNER → `documents:write`) without role-allow-list growth.
  scopes?: string[];
  iat?: number;
  exp?: number;
}

export interface AuthenticatedRequest extends Request {
  user?: JwtPayload;
}


// KS-347: verify RS256 tokens with a public key resolved by the token's `kid`
// from auth's JWKS endpoint, falling back to the static JWT_PUBLIC_KEY. An auth
// signing-key rotation (KS-326/346) is therefore picked up WITHOUT redeploying
// originate, while staying a strict superset of the previous static-key path
// (JWKS unconfigured/unreachable → static key, exactly as before). Alg pinning
// (no RS256->HS256 confusion / alg:none, KS-179/326) is preserved inside the
// shared verifier; originate still holds only PUBLIC key material. Async for the
// JWKS fetch — the only caller is the async authenticate() middleware below.
async function verifyRs256(token: string): Promise<JwtPayload> {
  return (await verifyJwtRs256(token)) as unknown as JwtPayload;
}

function getUser(req: Request): JwtPayload | undefined {
  return (req as any)._secuuraUser;
}

function setUser(req: Request, user: JwtPayload): void {
  // Pen-test F-04 alignment: stash under both `_secuuraUser` (legacy
  // originate-local helpers) and `req.user` (the shared canonical field
  // the F-04 sweep migrated handlers to read). Either path picks up the
  // verified JWT payload.
  (req as any)._secuuraUser = user;
  (req as any).user = user;
}

/**
 * Verify JWT token and attach user to request.
 * If `required` is false, unauthenticated requests pass through with no user.
 */
export function authenticate(options: { required?: boolean } = { required: true }) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const authHeader = req.headers.authorization;

      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        if (options.required) {
          return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
        }
        return next();
      }

      const token = authHeader.split(' ')[1];
      // KS-184/347: RS256-only verification; key resolved by kid via JWKS with a
      // static-key fallback (see verifyRs256). Async for the JWKS fetch.
      const decoded = await verifyRs256(token);

      // KS-257: defense-in-depth session-revocation check. originate verifies
      // JWTs independently of the gateway, so it must also honour revocation —
      // otherwise a revoked-session token reaching originate kept working until
      // expiry (~1h). Only interactive sessions carry a sessionId. Fail OPEN if
      // the session store is unreachable (log, don't 401 all traffic on a blip).
      if (decoded.sessionId) {
        const active = await isSessionActive(decoded.sessionId);
        if (active === false) {
          return res.status(401).json({ success: false, error: { code: 'SESSION_INVALIDATED', message: 'Session has been invalidated' } });
        }
        if (active === null) {
          logger.warn('Session-revocation check skipped — session store unreachable', { sessionId: decoded.sessionId });
        }
      }

      setUser(req, decoded);
      next();
    } catch (error) {
      // KS-584 P3: classify by error NAME as well as instanceof. verifyRs256
      // delegates to @secuura/shared's jsonwebtoken, which in the container
      // layout (/shared/node_modules) is a DIFFERENT module instance than this
      // file's import — instanceof fails across instances, so a malformed
      // bearer fell through to next(error) and surfaced as a raw 500 (the
      // KS-431/449/497 class) instead of the 401 this branch always intended.
      const name = (error as { name?: string } | null)?.name;
      if (
        error instanceof jwt.JsonWebTokenError
        || error instanceof jwt.TokenExpiredError
        || name === 'JsonWebTokenError'
        || name === 'TokenExpiredError'
        || name === 'NotBeforeError'
      ) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid or expired token' } });
      }
      next(error);
    }
  };
}

/**
 * Require the authenticated user to have one of the specified roles.
 * Must be used AFTER `authenticate()`.
 */
export function requireRole(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = getUser(req);
    if (!user) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    // Normalise role aliases: super_admin and SUPER_ADMIN are treated as SYSTEM_ADMIN
    const effectiveRole = ['super_admin', 'SUPER_ADMIN'].includes(user.role) ? 'SYSTEM_ADMIN' : user.role;
    if (!allowedRoles.includes(effectiveRole)) {
      logger.warn('Access denied — insufficient role', {
        userId: user.userId,
        role: user.role,
        requiredRoles: allowedRoles,
        path: req.path,
      });
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Insufficient permissions' } });
    }
    next();
  };
}

/**
 * True if the user's (alias-normalised) role is one of `allowedRoles`.
 * `super_admin`/`SUPER_ADMIN` normalise to `SYSTEM_ADMIN`, matching `requireRole`.
 * For inline owner-or-admin checks (e.g. a record loaded by a non-userId key).
 */
export function hasAnyRole(user: JwtPayload | undefined, allowedRoles: string[]): boolean {
  if (!user) return false;
  const effectiveRole = ['super_admin', 'SUPER_ADMIN'].includes(user.role) ? 'SYSTEM_ADMIN' : user.role;
  return allowedRoles.includes(effectiveRole);
}

/**
 * Require the caller to be the subject of the request (their `userId` matches the
 * `:userId` path param) OR to hold one of `allowedRoles`. Use AFTER
 * `authenticate()` on per-user data routes: a plain `authenticate()` lets any
 * logged-in user read another user's data by changing the path param
 * (KS-228 IDOR / BOLA). `paramName` is configurable for routes keyed differently.
 */
export function requireSelfOrRole(allowedRoles: string[], paramName = 'userId') {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = getUser(req);
    if (!user) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    const subjectId = req.params[paramName];
    if (user.userId === subjectId || hasAnyRole(user, allowedRoles)) {
      return next();
    }
    logger.warn('Access denied — not owner and insufficient role (KS-228)', {
      userId: user.userId,
      role: user.role,
      subjectId,
      path: req.path,
    });
    return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'You may only access your own data' } });
  };
}
