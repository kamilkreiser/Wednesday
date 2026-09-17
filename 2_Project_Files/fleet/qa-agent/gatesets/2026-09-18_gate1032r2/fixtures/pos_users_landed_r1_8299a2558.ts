/**
 * =============================================================================
 * USER ROUTES — Profile and Account Management
 * =============================================================================
 * All user lookups and mutations go through the userRepo repository,
 * which persists to PostgreSQL with in-memory fallback.
 * =============================================================================
 */

import { Router, Response } from 'express';
import { z } from 'zod';
import crypto from 'crypto';
import { AuthenticatedRequest, User, UserRole, VerificationLevel, ADMIN_WRITABLE_STATUSES } from '../types';
import { authenticate, authenticateAccessOrConnector } from '../middleware/authenticate';
import { hashPassword, checkPasswordStrength, verifyPassword } from '../services/password';
import { BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from '../middleware/errorHandler'; // KS-1018: needed to rethrow infra errors as 503
import { isInfrastructureDbError } from '../repositories/dbErrors'; // KS-1018: predicate for distinguishing infra DB failures
import { logger } from '../utils/logger';
import * as userRepo from '../repositories/userRepo';
import { revokeAllUserSessions } from '../services/session';
// KS-796 F-4: the SAME predicate the three credential doors consult, so a
// status that cannot receive a credential also cannot keep the sessions it
// already holds.
import { accountStatusForbidsCredential } from '../services/passwordLoginGate';
import { hasNulByte } from '@secuura/shared';

export const userRoutes = Router();

/**
 * KS-703: a U+0000 in a string query parameter reached Postgres unguarded and
 * surfaced the driver's own `invalid byte sequence for encoding "UTF8": 0x00`
 * to the caller as a 500. The platform's control-byte guard (KS-471/472,
 * `findControlBytePath`) walks the request BODY only — nothing on the platform
 * walks the query string — so the two list routes here apply the KS-451
 * primitive themselves and answer the same 400 the body guard gives.
 *
 * Surface: `search` and `role` on `GET /api/users` and `GET /api/users/admin/list`.
 * Both were measured returning 500 on the local stack (2026-08-28); the ticket
 * had recorded only `/admin/list`, and `GET /api/users` is the same handler
 * shape reaching the same `listUsers`/`countUsers` calls.
 *
 * Byte scope: U+0000 ONLY — that is the byte the driver cannot store. Other C0
 * control bytes (U+0001 SOH and friends) are accepted by Postgres and return
 * 200 today, here and everywhere else; widening the guard to the whole query
 * string platform-wide is a NEW rejection on every published GET contract and
 * is tracked separately on KS-703.
 *
 * Returns true when it has already answered — the caller must stop.
 */
/**
 * Flatten whatever `qs` produced for one query param into the list of scalar
 * strings it actually carries.
 *
 * `qs` 6.15.3 under express 4.22.2 does not always hand a handler a string:
 *   `?p=a&p=b` and `?p[]=a` both yield an ARRAY, and `?p[k]=v` yields an
 *   OBJECT. Measured, not assumed — the versions are pinned in the test file.
 *
 * Every element is returned, not just the first or the last: in
 * `?search=a&search=%00x` the NUL is in the SECOND value, so a guard that
 * sampled one position would pass it.
 */
function flattenQueryValue(value: unknown): string[] {
  if (value === undefined || value === null) return [];
  if (typeof value === 'string') return [value];
  if (Array.isArray(value)) return value.flatMap(flattenQueryValue);
  if (typeof value === 'object') return Object.values(value as Record<string, unknown>).flatMap(flattenQueryValue);
  return [String(value)];
}

/**
 * Reject a NUL byte in the list routes' string query params, and normalise
 * what survives to the single string the handlers and the repo expect.
 *
 * TWO defects close on the same line, because both come from the handler
 * receiving a value that is not a string:
 *
 *  1. The NUL bypass. `hasNulByte` is string-only by contract (KS-451) and
 *     that contract is deliberate, documented and pinned by
 *     `packages/shared/src/__tests__/validation.nul.test.ts:53`. So an
 *     array-shaped param walked straight past the guard and reached Postgres
 *     exactly as it did before the guard existed. The normalisation lives
 *     HERE rather than in `hasNulByte`, so a route-level problem does not
 *     change a platform-wide primitive.
 *
 *  2. A type confusion with no attacker in it. `?role=a&role=b` — an ordinary
 *     multi-select filter, no control byte anywhere — 500s on
 *     `role.split(',')` in userRepo. Four sites, because `countUsers` repeats
 *     `listUsers`: :763 / :769 and :807 / :813. Normalising here covers all
 *     four without touching the repo.
 *
 * The ',' collapse is chosen, not arbitrary. It is precisely what the template
 * literal at `userRepo.ts:763` already does to an array implicitly —
 * `` `%${['a','b']}%` `` is `'%a,b%'` — so `search` behaviour is unchanged;
 * and it is the separator `role.split(',')` already expects, so a multi-select
 * role filter starts working instead of crashing.
 *
 * Writing back to `req.query[param]` makes the handlers' existing
 * `as string` casts true rather than merely compiling. Express 4's `req.query`
 * is a plain cached object and a per-key write survives its getter — measured
 * on express 4.22.2 / qs 6.15.3, not assumed.
 */
function rejectNulInListQuery(req: AuthenticatedRequest, res: Response): boolean {
  for (const param of ['search', 'role'] as const) {
    const raw = req.query[param];
    if (raw === undefined) continue;

    const parts = flattenQueryValue(raw);
    if (parts.some((part) => hasNulByte(part))) {
      const message = 'Must not contain a NUL (U+0000) byte';
      res.status(400).json({
        success: false,
        error: { code: 'VALIDATION_ERROR', message, details: [{ path: param, message }] },
      });
      return true;
    }

    req.query[param] = parts.join(',');
  }
  return false;
}

/**
 * Mirror of routes/auth.ts maskEmail — keeps audit logs readable without
 * dragging the auth.ts handler module in. `a***@example.com` is enough
 * granularity to correlate logs without persisting the local-part.
 */
function maskEmail(email: string): string {
  const [local, domain] = email.split('@');
  if (!local || !domain) return '***';
  return `${local[0]}***@${domain}`;
}

// Validation schemas
//
// BACKLOG H8 (was F-HOLDER-02): defence-in-depth on PATCH /api/users/me.
// Zod strips unknown keys by default, so a payload like {role:"SYSTEM_ADMIN"}
// is silently dropped — but `silently` is the wrong behaviour for a sensitive
// endpoint. `.strict()` makes Zod throw on any unknown key, so:
//   - the request 400s with "Unrecognized key 'role'", giving an audit trail
//   - if anyone ever removes a field from the schema and forgets to delete a
//     consuming caller, that mistake is loud, not silent
//   - if CSRF is ever bypassed (XSS-leaked token, misconfig), this still
//     refuses role/verificationLevel attempts before the handler runs.
// The handler also only ever reads the four allowed fields below — that's
// the second layer.
const updateProfileSchema = z.object({
  firstName: z.string().trim().min(1).max(100).optional(),
  lastName: z.string().trim().min(1).max(100).optional(),
  displayName: z.string().trim().min(1).max(200).optional(),
  phoneNumber: z.string().trim().optional(),
}).strict();

const changePasswordSchema = z.object({
  currentPassword: z.string().min(1),
  newPassword: z.string().min(8),
});

const verificationRequestSchema = z.object({
  targetLevel: z.enum(['STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT']),
  documents: z.array(z.string()).optional(),
});

// =============================================================================
// KS-69: scope/role gate for /lookup. Tenant-scoped email → user resolver,
// callable from issuer / connector flows that have only an email and need
// the platform's holderId. Tenant isolation is enforced by comparing the
// caller's tenantId (from the verified JWT) against the resolved user's
// tenantId BEFORE returning anything. (KS-467 reconciliation of the old
// note here: since KS-109 the auth service connects as secuura_app, which
// does NOT bypass RLS, and KS-458 flipped the policy fail-closed — but the
// email lookup goes through the migration-039 SECURITY DEFINER carve-out,
// which is cross-tenant by design, so this app-layer compare is still the
// enforcement, not a redundancy.)
//
// Accepted callers (any of these passes):
//   - Role in the cert-issuance allow-list (the same set originate's
//     ALLOWED_CREATION_ROLES uses).
//   - Scope `users:read` (or `users:*` / `*` wildcard). The gateway also
//     enforces this scope on the proxy route as defence-in-depth.
const ALLOWED_LOOKUP_ROLES = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'];

// =============================================================================
// KS-467: platform-vs-tenant admin split for the user-admin surface.
// The admin role gates below admit tenant-scoped admins (ISSUER_ADMIN /
// ORG_ADMIN) alongside genuine platform admins, so every cross-tenant
// capability must additionally check THIS list — a tenant-scoped admin
// operates only inside its own tenant, mirroring the /lookup + /stub
// template (tenant mismatch → 404, same shape as not-found). The lowercase
// 'admin' / 'super_admin' are the legacy JWT variants the existing gates
// already accept (the seeded platform admin carries 'super_admin').
// =============================================================================
const PLATFORM_ADMIN_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'admin', 'super_admin'];

function isPlatformAdmin(role: string): boolean {
  return PLATFORM_ADMIN_ROLES.includes(role);
}

// KS-486: canonical role validation for the admin create/update routes.
// A case-sensitive denylist plus a case-normalising DB layer (userRepo
// lowercases on insert; mapDbRole reads 'super_admin' back as SYSTEM_ADMIN)
// let a tenant-scoped admin mint a platform SYSTEM_ADMIN via a case variant
// like "Super_Admin". Allow-list instead: fold any case/alias to the single
// canonical UserRole (or null → reject), and use that one value for BOTH the
// platform-only guard and persistence so the check and the stored role can
// never disagree. Mirrors mapDbRole's alias table (userRepo.ts).
const ROLE_ALIASES: Record<string, UserRole> = {
  user: 'OWNER',
  owner: 'OWNER',
  issuer_admin: 'ISSUER_ADMIN',
  issuer_approver: 'ISSUER_APPROVER',
  verifier: 'VERIFIER',
  org_admin: 'ORG_ADMIN',
  system_admin: 'SYSTEM_ADMIN',
  super_admin: 'SYSTEM_ADMIN',
};
function normalizeAssignableRole(input: unknown): UserRole | null {
  if (typeof input !== 'string') return null;
  return ROLE_ALIASES[input.trim().toLowerCase()] ?? null;
}
// Canonical roles only a platform admin may assign.
const PLATFORM_ONLY_CANONICAL_ROLES: readonly UserRole[] = ['SYSTEM_ADMIN'];

function hasUsersReadScope(scopes: readonly string[] | undefined): boolean {
  if (!scopes || scopes.length === 0) return false;
  if (scopes.includes('*')) return true;
  if (scopes.includes('users:*')) return true;
  return scopes.includes('users:read');
}

const lookupQuerySchema = z.object({
  // Same upper bound RFC 5321 allows for the local + domain combined,
  // catches obvious garbage before we hit the repo.
  email: z.string().trim().email().min(3).max(320),
});

// KS-74: POST /api/users/stub — same RBAC as /lookup. Either an allow-list
// role or `users:read` / `users:create` / `users:*` / `*` scope. The
// `users:create` alias is accepted because creating an INVITED stub is
// closer in intent to "create" than "read", but the response shape is
// identical to /lookup so the scope distinction is documentation-only.
const stubBodySchema = z.object({
  email: z.string().trim().email().min(3).max(320),
});

function hasUsersStubScope(scopes: readonly string[] | undefined): boolean {
  if (!scopes || scopes.length === 0) return false;
  if (scopes.includes('*')) return true;
  if (scopes.includes('users:*')) return true;
  if (scopes.includes('users:read') || scopes.includes('users:create')) return true;
  // KS-564 (Option A): a connector issuing certifications by recipient email
  // MUST mint the KS-74 INVITED stub to have a holder id to point at, so the
  // certification scope authorises this specific lookup-or-create. Narrower
  // than granting Platform S `users:*`, which would open the rest of the
  // users surface it has no need for.
  return scopes.includes('certifications:write');
}

// =============================================================================
// GET /api/users/lookup?email=… — bridge email to userId for cert issuance
// =============================================================================
// KS-69: SSD's cert-issuance flow knows the recipient's email but not their
// Platform K userId. This endpoint resolves the email within the caller's
// tenant. Returns 404 (not 200-empty) so positive existence isn't trivially
// readable from response shape — the `users:read` scope or one of the
// allow-list roles is the actual gate.
userRoutes.get('/lookup', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const parsed = lookupQuerySchema.safeParse({ email: req.query.email });
    if (!parsed.success) {
      // Per the KS-69 acceptance criteria the malformed-query response is
      // a 400 (BadRequest), not 422 (Validation). BadRequestError emits
      // the right status; the Zod issues are inlined into the message
      // so callers can still see what's wrong.
      throw new BadRequestError(
        'email query parameter is required and must be a valid email address: ' +
          parsed.error.issues.map((i) => i.message).join('; '),
      );
    }
    const { email } = parsed.data;

    const callerRole = String((req.user as { role?: string } | undefined)?.role ?? '').toUpperCase();
    const callerScopes = (req.user as { scopes?: string[] } | undefined)?.scopes;
    const allowedByRole = ALLOWED_LOOKUP_ROLES.includes(callerRole);
    const allowedByScope = hasUsersReadScope(callerScopes);
    if (!allowedByRole && !allowedByScope) {
      logger.warn('users/lookup blocked — insufficient role and scope', {
        callerUserId: req.user?.userId,
        callerRole,
        callerTenantId: req.user?.tenantId,
      });
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'users:read scope or an allowed role is required for this endpoint' },
      });
    }

    const callerTenantId = req.user?.tenantId;
    const callerEmail = req.user?.email ? maskEmail(req.user.email) : undefined;

    const user = await userRepo.getUserByEmail(email);

    // 404 when the user doesn't exist OR is in a different tenant. The
    // negative response shape is identical in both branches so the caller
    // cannot distinguish "no such email" from "exists in another tenant" —
    // the latter would be a cross-tenant disclosure even if subtle.
    if (!user || (callerTenantId && user.tenantId && user.tenantId !== callerTenantId)) {
      logger.info('users/lookup: miss', {
        callerUserId: req.user?.userId,
        callerTenantId,
        queriedEmail: maskEmail(email),
        crossTenant: !!(user && callerTenantId && user.tenantId !== callerTenantId),
      });
      return res.status(404).json({
        success: false,
        error: { code: 'USER_NOT_FOUND', message: 'No user with that email in this tenant' },
      });
    }

    logger.info('users/lookup: hit', {
      callerUserId: req.user?.userId,
      callerEmail,
      callerTenantId,
      resolvedUserId: user.id,
      resolvedTenantId: user.tenantId,
      authPath: allowedByRole ? 'role' : 'scope',
    });

    return res.json({
      success: true,
      data: {
        userId: user.id,
        organizationId: user.organizationId,
        tenantId: user.tenantId,
        displayName: user.displayName,
        verificationLevel: user.verificationLevel,
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// POST /api/users/stub — KS-74: idempotent lookup-or-create for INVITED stubs
// =============================================================================
// SSD's cert-issuance flow can supply only a recipient email. If the email
// is already a Platform K user in the caller's tenant, return it (idempotent
// resolve). If not, mint an INVITED stub row tagged to the caller's tenant
// so the cert has a real holder id to point at. The stub is claimed when
// the email signs up via /api/auth/register.
//
// Cross-tenant case: if the email exists in a *different* tenant, return 404
// — identical shape to /lookup's cross-tenant miss — to avoid disclosing
// the existence of users in other tenants. Known KS-74 limitation of the
// global email uniqueness constraint (per-tenant emails is a separate
// future migration).
// KS-564 (Option A): this ONE route also accepts a connector token — see
// authenticateAccessOrConnector. Every other route keeps plain authenticate().
userRoutes.post('/stub', authenticateAccessOrConnector(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const parsed = stubBodySchema.safeParse(req.body);
    if (!parsed.success) {
      throw new BadRequestError(
        'email is required and must be a valid email address: ' +
          parsed.error.issues.map((i) => i.message).join('; '),
      );
    }
    const { email } = parsed.data;

    const callerRole = String((req.user as { role?: string } | undefined)?.role ?? '').toUpperCase();
    const callerScopes = (req.user as { scopes?: string[] } | undefined)?.scopes;
    const allowedByRole = ALLOWED_LOOKUP_ROLES.includes(callerRole);
    const allowedByScope = hasUsersStubScope(callerScopes);
    if (!allowedByRole && !allowedByScope) {
      logger.warn('users/stub blocked — insufficient role and scope', {
        callerUserId: req.user?.userId,
        callerRole,
        callerTenantId: req.user?.tenantId,
      });
      return res.status(403).json({
        success: false,
        error: {
          code: 'FORBIDDEN',
          message: 'users:read / users:create scope or an allowed role is required for this endpoint',
        },
      });
    }

    const callerTenantId = req.user?.tenantId;

    try {
      const result = await userRepo.createInvitedStub(email, callerTenantId);
      logger.info('users/stub: resolved', {
        callerUserId: req.user?.userId,
        callerTenantId,
        queriedEmail: maskEmail(email),
        userId: result.user.id,
        alreadyExisted: result.alreadyExisted,
        status: result.user.status,
      });
      return res.status(result.alreadyExisted ? 200 : 201).json({
        success: true,
        data: {
          userId: result.user.id,
          status: result.user.status,
          email: result.user.email,
          alreadyExisted: result.alreadyExisted,
          tenantId: result.user.tenantId,
        },
      });
    } catch (err: any) {
      if (err?.code === 'EMAIL_RESERVED_ELSEWHERE') {
        logger.info('users/stub: cross-tenant block (returning 404)', {
          callerUserId: req.user?.userId,
          callerTenantId,
          queriedEmail: maskEmail(email),
        });
        return res.status(404).json({
          success: false,
          error: { code: 'USER_NOT_FOUND', message: 'No user with that email in this tenant' },
        });
      }
      throw err;
    }
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// GET /api/users — List users for ORG_ADMIN+ (issuer portal Users page)
// =============================================================================
userRoutes.get('/', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const role = req.user!.role as string;
    const ADMIN_ROLES = ['SYSTEM_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'admin', 'super_admin', 'SUPER_ADMIN'];
    if (!ADMIN_ROLES.includes(role)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Forbidden — admin role required' } });
    }

    // KS-467: tenant-scoped admins list only their own tenant; platform
    // admins keep the deliberate cross-tenant view. A tenant admin with no
    // tenant claim has no scope to list under — refuse rather than disclose.
    const callerTenantId = req.user?.tenantId as string | undefined;
    if (!isPlatformAdmin(role) && !callerTenantId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Tenant context required' } });
    }
    const tenantScope = isPlatformAdmin(role) ? undefined : callerTenantId;

    if (rejectNulInListQuery(req, res)) return;

    const limit = Math.min(parseInt(req.query.limit as string) || 50, 200);
    const offset = parseInt(req.query.offset as string) || 0;
    const search = (req.query.search as string) || '';
    const roleFilter = (req.query.role as string) || '';

    const users = await userRepo.listUsers({ limit, offset, search, role: roleFilter, tenantId: tenantScope });
    const total = await userRepo.countUsers(search, roleFilter, tenantScope ?? '');

    res.json({
      success: true,
      data: {
        users: users.map(u => ({
          id: u.id,
          email: u.email,
          firstName: u.firstName,
          lastName: u.lastName,
          displayName: u.displayName,
          role: u.role,
          status: u.status,
          verificationLevel: u.verificationLevel,
          organizationId: u.organizationId,
          lastLoginAt: u.lastLoginAt,
          createdAt: u.createdAt,
        })),
        total,
        limit,
        offset,
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// GET /api/users/admin/list — Admin: list all users (paginated)
// =============================================================================
userRoutes.get('/admin/list', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const role = req.user!.role as string;
    const ADMIN_ROLES = ['SYSTEM_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'admin', 'super_admin', 'SUPER_ADMIN'];
    if (!ADMIN_ROLES.includes(role)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin role required' } });
    }

    // KS-467: tenant-scoped admins (ISSUER_ADMIN / ORG_ADMIN) list only
    // their own tenant; platform admins keep the cross-tenant view. No
    // tenant claim on a tenant-scoped admin → refuse rather than disclose.
    const callerTenantId = req.user?.tenantId as string | undefined;
    if (!isPlatformAdmin(role) && !callerTenantId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Tenant context required' } });
    }
    const tenantScope = isPlatformAdmin(role) ? undefined : callerTenantId;

    if (rejectNulInListQuery(req, res)) return;

    const limit = Math.min(parseInt(req.query.limit as string) || 50, 200);
    const offset = parseInt(req.query.offset as string) || 0;
    const search = (req.query.search as string) || '';
    const roleFilter = (req.query.role as string) || '';

    const users = await userRepo.listUsers({ limit, offset, search, role: roleFilter, tenantId: tenantScope });
    const total = await userRepo.countUsers(search, roleFilter, tenantScope ?? '');

    res.json({
      success: true,
      data: {
        users: users.map(u => ({
          id: u.id,
          email: u.email,
          firstName: u.firstName,
          lastName: u.lastName,
          displayName: u.displayName,
          role: u.role,
          status: u.status,
          verificationLevel: u.verificationLevel,
          organizationId: u.organizationId,
          lastLoginAt: u.lastLoginAt,
          createdAt: u.createdAt,
        })),
        total,
        limit,
        offset,
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// GET /api/users/admin/organizations — Admin: list organizations from user data
// =============================================================================
userRoutes.get('/admin/organizations', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const role = req.user!.role as string;
    const ADMIN_ROLES = ['SYSTEM_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'admin', 'super_admin', 'SUPER_ADMIN'];
    if (!ADMIN_ROLES.includes(role)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin role required' } });
    }

    // KS-467: tenant-scoped admins see only their own tenant's organisations;
    // platform admins keep the cross-tenant view (same split as /admin/list).
    const callerTenantId = req.user?.tenantId as string | undefined;
    if (!isPlatformAdmin(role) && !callerTenantId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Tenant context required' } });
    }

    const orgs = await userRepo.listOrganizations(isPlatformAdmin(role) ? '' : (callerTenantId ?? ''));

    res.json({
      success: true,
      data: {
        organizations: orgs,
        total: orgs.length,
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// POST /api/users/admin/create — Admin: create a new user
// =============================================================================
userRoutes.post('/admin/create', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const role = req.user!.role as string;
    const ADMIN_ROLES = ['SYSTEM_ADMIN', 'ORG_ADMIN', 'super_admin', 'SUPER_ADMIN'];
    if (!ADMIN_ROLES.includes(role)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin role required' } });
    }

    const { email, password, firstName, lastName, role: newRole, verificationLevel } = req.body;

    if (!email || !password) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Email and password are required' } });
    }

    // KS-467: a tenant-scoped admin must not mint platform-admin accounts,
    // and any user it creates belongs to its OWN tenant — createUser would
    // otherwise default the row to the platform default tenant, which is a
    // cross-tenant write. Platform admins keep the existing behaviour.
    const callerIsPlatform = isPlatformAdmin(role);
    const callerTenantId = req.user?.tenantId as string | undefined;
    if (!callerIsPlatform && !callerTenantId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Tenant context required' } });
    }
    // KS-486: validate + canonicalise the requested role (allow-list, case/alias
    // -insensitive) so a variant like "Super_Admin" can't bypass the platform-only
    // guard and normalise to SYSTEM_ADMIN at rest. Default to OWNER when none given
    // (unchanged from the prior 'USER' default, which mapped to OWNER at read).
    let canonicalRole: UserRole = 'OWNER';
    if (newRole !== undefined && newRole !== null && newRole !== '') {
      const normalisedRole = normalizeAssignableRole(newRole);
      if (!normalisedRole) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid role' } });
      }
      canonicalRole = normalisedRole;
    }
    if (!callerIsPlatform && PLATFORM_ONLY_CANONICAL_ROLES.includes(canonicalRole)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Only a platform admin can assign a platform-admin role' } });
    }

    // KS-486 sweep follow-up: a non-string verificationLevel (e.g. `{}`)
    // crashed the create at userRepo's `.toLowerCase()` → raw 500. Validate
    // the type here → 400; empty string keeps the BASIC default below.
    if (verificationLevel !== undefined && verificationLevel !== null && typeof verificationLevel !== 'string') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'verificationLevel must be a string' } });
    }

    // Check if user already exists
    const exists = await userRepo.emailExists(email);
    if (exists) {
      return res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'User with this email already exists' } });
    }

    // Hash password
    const passwordHash = await hashPassword(password);

    // Create user
    const user: User = {
      id: crypto.randomUUID(),
      email,
      emailVerified: true, // Admin-created users are pre-verified
      passwordHash,
      firstName: firstName || '',
      lastName: lastName || '',
      displayName: `${firstName || ''} ${lastName || ''}`.trim() || email,
      phoneVerified: false,
      mfaEnabled: false,
      role: canonicalRole,
      verificationLevel: (verificationLevel || 'BASIC') as VerificationLevel,
      status: 'ACTIVE',
      // KS-467: tenant-scoped admins create users in their own tenant only;
      // platform admins leave it unset (createUser defaults the platform
      // default tenant, the pre-existing behaviour).
      tenantId: callerIsPlatform ? undefined : callerTenantId,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    await userRepo.createUser(user);

    logger.info('Admin created user', { email, role: user.role, createdBy: req.user!.userId });

    res.status(201).json({
      success: true,
      data: {
        id: user.id,
        email: user.email,
        displayName: user.displayName,
        role: user.role,
        verificationLevel: user.verificationLevel,
        status: user.status,
      },
    });
  } catch (err) {
    next(err);
  }
});

// =============================================================================
// PATCH /api/users/admin/:id — Admin: update a user (role, status, etc.)
// =============================================================================
userRoutes.patch('/admin/:id', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const role = req.user!.role as string;
    if (role !== 'SYSTEM_ADMIN' && role !== 'ORG_ADMIN' && role !== 'admin' && role !== 'super_admin' && role !== 'SUPER_ADMIN') {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin role required' } });
    }

    const { id } = req.params;
    const updates = req.body || {};

    // Only allow updating safe fields
    const allowedFields = ['status', 'role', 'verificationLevel', 'displayName', 'firstName', 'lastName', 'organizationId'];
    const safeUpdates: Record<string, any> = {};
    for (const key of allowedFields) {
      if (updates[key] !== undefined) {
        safeUpdates[key] = updates[key];
      }
    }

    if (Object.keys(safeUpdates).length === 0) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'No valid fields to update' } });
    }

    // KS-486: validate + canonicalise the requested role (allow-list, case/alias
    // -insensitive) and replace it with the single canonical value, used for both
    // the platform-only guard below and the persisted write, so a case variant
    // can't slip past the guard and normalise to SYSTEM_ADMIN at rest.
    if (safeUpdates.role !== undefined) {
      const normalisedRole = normalizeAssignableRole(safeUpdates.role);
      if (!normalisedRole) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid role' } });
      }
      safeUpdates.role = normalisedRole;
    }

    // Validate status values. KS-486 sweep follow-up: `!== undefined` (not
    // truthy) — an EMPTY-string status previously slipped past this check and
    // was written raw to the row, corrupting the status vocabulary.
    // KS-796 Q1: derived from the ONE vocabulary, not a fourth hand-written copy.
    // The previous literal omitted `deactivated` and `invited` — so the gate
    // named a status this endpoint refused to write, while `inactive` and
    // `deleted` were writable and unknown to the mapper.
    //
    // KS-796 F-3: the writable set is the ADMIN-WRITABLE subset, NOT the whole
    // column vocabulary. `= DB_USER_STATUSES` newly admitted `invited`, which
    // `POST /api/auth/register` treats as "claimable" — an admin "disabling" an
    // account made it publicly takeable instead. The reason each member is on
    // the list, and why `invited` is not, is at the constant.
    const VALID_STATUSES = ADMIN_WRITABLE_STATUSES;
    if (safeUpdates.status !== undefined && !VALID_STATUSES.includes(safeUpdates.status)) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Invalid status. Must be one of: ${VALID_STATUSES.join(', ')}` } });
    }

    const adminId = req.user!.userId;
    const callerIsPlatform = isPlatformAdmin(role);
    const callerTenantId = req.user?.tenantId as string | undefined;

    // KS-467: separation of duties — no caller changes their OWN role
    // through this endpoint; a peer or higher admin grants it.
    if (safeUpdates.role && id === adminId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Cannot change your own role' } });
    }
    // KS-467: role ceiling — platform-admin roles are grantable only by a
    // platform admin (a tenant admin could otherwise self-provision a
    // platform account inside its tenant and escalate from there).
    if (safeUpdates.role && !callerIsPlatform && PLATFORM_ONLY_CANONICAL_ROLES.includes(safeUpdates.role as UserRole)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Only a platform admin can assign a platform-admin role' } });
    }

    // KS-1013: validate the id FORMAT before the lookup. A non-UUID reaches
    // Postgres, raises 22P02 (or 22021 for a NUL byte / invalid UTF-8) and
    // propagates as a raw 500 — the KS-536 4xx rule, and the same family as
    // KS-478 / KS-451 / KS-431 / KS-693.
    //
    // This is a 400, NOT the 404 the neighbouring oauth.ts:1035 guard answers.
    // That route reasons "every real app id is a UUID we mint, so anything
    // else is simply not a known app"; here the honest answer is that the
    // REQUEST was malformed. A 404 would repeat the wrong answer this ticket
    // was filed for — telling a caller "user not found" about an id that could
    // never name a user in any tenant. It discloses nothing either way: a
    // malformed id is invalid for every tenant, so the 404-for-both rule that
    // hides foreign-tenant targets below is untouched.
    //
    // ⚠ KS-963 is NOT the cause of the 500 this replaces. That ruling removed
    // the swallow which had been hiding this gap behind a wrong 404; the route
    // never validated the format. Do not revert it to "fix" this route.
    if (!z.string().uuid().safeParse(id).success) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid user id' } });
    }

    // KS-467 (PS-198 analog): ownership re-check before the by-id write,
    // mirroring the /lookup + /stub template (users.ts:~160). Read the
    // target under platform scope so the row is visible regardless of the
    // request's tenant GUC (finding 4: this path must NOT depend on RLS
    // binding — the app-layer compare is the enforcement), then require a
    // tenant-scoped admin's target to sit in the caller's own tenant. A
    // foreign-tenant (or absent) target returns 404, identical to
    // not-found, so org/user existence isn't disclosed across the boundary.
    const target = await userRepo.getUserByIdPlatformScope(id);
    if (!target || (!callerIsPlatform && (!callerTenantId || target.tenantId !== callerTenantId))) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } });
    }

    // KS-467: a supplied organizationId must exist and — for tenant-scoped
    // admins — belong to the caller's own tenant. The rejection is identical
    // for "doesn't exist" and "foreign tenant" so org existence isn't
    // disclosed across the boundary. Explicit null clears the assignment.
    if (safeUpdates.organizationId !== null && safeUpdates.organizationId !== undefined) {
      const org = await userRepo.getOrganizationTenant(String(safeUpdates.organizationId));
      const orgOwned = org !== null && (callerIsPlatform || (!!callerTenantId && org.tenantId === callerTenantId));
      if (!orgOwned) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid organizationId' } });
      }
    }

    logger.info('Admin user update', { targetUserId: id, updatedBy: adminId, changes: safeUpdates });

    // Write under platform scope: the ownership gate above is the security
    // boundary (same as the /lookup template), and the plain tenant-GUC
    // write path is unreliable on this proxied admin route.
    const updatedUser = await userRepo.updateUserPlatformScope(id, safeUpdates);

    if (!updatedUser) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } });
    }

    // KS-360: a "suspend/deactivate now" admin action must cut access immediately,
    // not after the in-flight access token's ≤1h TTL. updateUser doesn't touch
    // sessions, and the gateway's KS-257 check only 401s once the session is
    // revoked — so revoke all of the target's sessions here. Keyed off the
    // post-update canonical status, which is exactly what login/refresh and the
    // gateway enforce. (GDPR erasure already revokes via userErasedSubscriber.)
    //
    // KS-796 F-4: this was the THIRD copy of the deny-list — `SUSPENDED ||
    // DEACTIVATED`, with a comment reasoning that "PENDING/INVITED aren't
    // access-revocations and shouldn't have live sessions". That reasoning was
    // sound while those two were not admin-writable. Once they were, an admin
    // setting a live account to `pending` revoked nothing, and (before F-1) the
    // account kept minting at /api/auth/login. Three of the four things an
    // operator expects from "change this user's status" did not happen.
    //
    // Derived from the same allow-list the credential doors use, so "this status
    // cannot hold a credential" and "cut the sessions it already has" can no
    // longer disagree — which is the whole KS-796 thesis applied to the one site
    // that still restated it.
    if (accountStatusForbidsCredential(updatedUser)) {
      const sessionsRevoked = await revokeAllUserSessions(id);
      logger.info('Admin status change revoked active sessions', { targetUserId: id, status: updatedUser.status, sessionsRevoked, revokedBy: adminId });
    }

    res.json({
      success: true,
      data: {
        id: updatedUser.id,
        email: updatedUser.email,
        role: updatedUser.role,
        status: updatedUser.status,
        verificationLevel: updatedUser.verificationLevel,
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// GET /api/users/me — Current user profile
// Also mounted at GET /api/auth/me as an alias (F-06 audit 2026-05-15) — the
// "current authenticated user" concept is reasonable on either surface, and
// pre-existing clients (issuer/admin/verifier portals + e2e-v2 tier1
// auth.api.spec.ts) hit /api/auth/me. Keep the handler here so /me semantics
// stay co-located with the rest of the user routes; the auth router imports
// `meHandler` and re-mounts.
// =============================================================================
export const meHandler = async (req: AuthenticatedRequest, res: Response, next: import('express').NextFunction) => {
  try {
    const user = await userRepo.getUserById(req.user!.userId);
    if (!user) throw new NotFoundError('User');

    // Resolve organization/tenant name from JWT claims or platform DB
    let organizationName: string | undefined;
    let tenantId = user.tenantId;
    let tenantSlug = user.tenantSlug;

    // Try to get org name from JWT (set by gateway from login)
    const jwtTenantSlug = req.user?.tenantSlug as string | undefined;
    if (jwtTenantSlug) {
      tenantSlug = tenantSlug || jwtTenantSlug;
    }

    // Look up tenant name from platform DB
    // For platform admins without a tenantId, fall back to DEFAULT_TENANT_ID
    const effectiveTenantId = tenantId || process.env.DEFAULT_TENANT_ID;
    if ((effectiveTenantId || tenantSlug) && process.env.PLATFORM_DATABASE_URL) {
      try {
        const pg = require('pg');
        const pPool = new pg.Pool({ connectionString: process.env.PLATFORM_DATABASE_URL, max: 1 });
        const lookup = effectiveTenantId
          ? await pPool.query('SELECT id, name, slug FROM tenants WHERE id = $1 LIMIT 1', [effectiveTenantId])
          : await pPool.query('SELECT id, name, slug FROM tenants WHERE slug = $1 LIMIT 1', [tenantSlug]);
        if (lookup.rows.length > 0) {
          organizationName = lookup.rows[0].name;
          tenantSlug = tenantSlug || lookup.rows[0].slug;
          tenantId = tenantId || lookup.rows[0].id;
        }
        await pPool.end();
      } catch { /* platform DB unavailable */ }
    }

    res.json({
      success: true,
      data: {
        id: user.id,
        email: user.email,
        emailVerified: user.emailVerified,
        firstName: user.firstName,
        lastName: user.lastName,
        displayName: user.displayName,
        phoneNumber: user.phoneNumber,
        phoneVerified: user.phoneVerified,
        mfaEnabled: user.mfaEnabled,
        role: user.role,
        verificationLevel: user.verificationLevel,
        organizationId: user.organizationId,
        organizationName,
        tenantId,
        tenantSlug,
        status: user.status,
        lastLoginAt: user.lastLoginAt,
        createdAt: user.createdAt,
      },
    });
  } catch (error) {
    next(error);
  }
};

userRoutes.get('/me', authenticate(), meHandler);

// =============================================================================
// PATCH /api/users/me — Update profile
// =============================================================================
userRoutes.patch('/me', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const data = updateProfileSchema.parse(req.body);
    const user = await userRepo.getUserById(req.user!.userId);
    if (!user) throw new NotFoundError('User');

    const updates: Partial<User> = {};
    if (data.firstName !== undefined) updates.firstName = data.firstName;
    if (data.lastName !== undefined) updates.lastName = data.lastName;
    if (data.displayName !== undefined) updates.displayName = data.displayName;
    if (data.phoneNumber !== undefined) {
      updates.phoneNumber = data.phoneNumber;
      updates.phoneVerified = false;
    }

    // KS-1050: "success: true" over a write that did not land tells the user their
    // profile changed when it did not. The helper refuses with a retryable 503.
    const updated = await userRepo.updateUserOrThrow(user.id, updates, 'Profile update');
    logger.info('User profile updated', { userId: user.id });

    res.json({
      success: true,
      data: {
        id: updated?.id,
        email: updated?.email,
        firstName: updated?.firstName,
        lastName: updated?.lastName,
        displayName: updated?.displayName,
        phoneNumber: updated?.phoneNumber,
        phoneVerified: updated?.phoneVerified,
        updatedAt: updated?.updatedAt,
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// POST /api/users/me/change-password
// =============================================================================
userRoutes.post('/me/change-password', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const data = changePasswordSchema.parse(req.body);
    const user = await userRepo.getUserById(req.user!.userId);
    if (!user || !user.passwordHash) throw new NotFoundError('User');

    const isValid = await verifyPassword(data.currentPassword, user.passwordHash);
    if (!isValid) throw new BadRequestError('Current password is incorrect');

    const strength = checkPasswordStrength(data.newPassword);
    if (!strength.isStrong) {
      throw new ValidationError('New password is too weak', { feedback: strength.feedback });
    }

    const newHash = await hashPassword(data.newPassword);
    // KS-1052: "Password changed successfully" over a write that did not land
    // is the worst kind of wrong — the user believes the old password is dead.
    await userRepo.updateUserOrThrow(user.id, { passwordHash: newHash }, 'Password change');

    logger.info('Password changed', { userId: user.id });
    res.json({ success: true, message: 'Password changed successfully' });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// TOTP helpers (RFC 6238) — inline implementation for MFA in users routes
// =============================================================================
const BASE32_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';

function generateBase32Secret(length = 20): string {
  const bytes = crypto.randomBytes(length);
  return Array.from(bytes).map(b => BASE32_CHARS[b % 32]).join('');
}

function base32Decode(encoded: string): Buffer {
  const cleaned = encoded.replace(/=+$/, '').toUpperCase();
  let bits = '';
  for (const c of cleaned) {
    const idx = BASE32_CHARS.indexOf(c);
    if (idx === -1) continue;
    bits += idx.toString(2).padStart(5, '0');
  }
  const bytes: number[] = [];
  for (let i = 0; i + 8 <= bits.length; i += 8) {
    bytes.push(parseInt(bits.substring(i, i + 8), 2));
  }
  return Buffer.from(bytes);
}

function generateTOTP(secret: string, timeStep = 30, digits = 6, offset = 0): string {
  const key = base32Decode(secret);
  const counter = Math.floor(Date.now() / 1000 / timeStep) + offset;
  const buf = Buffer.alloc(8);
  buf.writeUInt32BE(Math.floor(counter / 0x100000000), 0);
  buf.writeUInt32BE(counter >>> 0, 4);
  const hmac = crypto.createHmac('sha1', key).update(buf).digest();
  const off = hmac[hmac.length - 1] & 0x0f;
  const code = ((hmac[off] & 0x7f) << 24 | hmac[off + 1] << 16 | hmac[off + 2] << 8 | hmac[off + 3]) % (10 ** digits);
  return code.toString().padStart(digits, '0');
}

function verifyTOTP(secret: string, code: string, window = 1): boolean {
  for (let i = -window; i <= window; i++) {
    if (generateTOTP(secret, 30, 6, i) === code) return true;
  }
  return false;
}

// =============================================================================
// MFA ENDPOINTS (inline — these also exist in mfa.ts for the dedicated flow)
// =============================================================================

/** POST /api/users/me/mfa/enable */
userRoutes.post('/me/mfa/enable', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const user = await userRepo.getUserById(req.user!.userId);
    if (!user) throw new NotFoundError('User');
    if (user.mfaEnabled) throw new BadRequestError('MFA is already enabled');

    const secret = generateBase32Secret(20);
    // KS-1052: the QR code below is generated from this secret. If the secret
    // did not persist, every code the user's app produces will be rejected.
    await userRepo.updateUserOrThrow(user.id, { mfaSecret: secret } as any, 'MFA setup');

    const qrCodeUrl = `otpauth://totp/Secuura:${encodeURIComponent(user.email)}?secret=${secret}&issuer=Secuura&algorithm=SHA1&digits=6&period=30`;

    logger.info('MFA setup initiated', { userId: user.id });
    res.json({
      success: true,
      data: { secret, qrCode: qrCodeUrl, message: 'Scan the QR code with your authenticator app, then verify with a code' },
    });
  } catch (error) {
    next(error);
  }
});

/** POST /api/users/me/mfa/verify */
userRoutes.post('/me/mfa/verify', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const { code } = req.body;
    if (!code || typeof code !== 'string' || code.length !== 6) {
      throw new BadRequestError('Invalid verification code — must be 6 digits');
    }

    const user = await userRepo.getUserById(req.user!.userId);
    if (!user) throw new NotFoundError('User');
    if (!user.mfaSecret) throw new BadRequestError('MFA setup not initiated — call /mfa/enable first');
    if (!verifyTOTP(user.mfaSecret, code)) throw new BadRequestError('Invalid verification code — please try again');

    const backupCodes = Array.from({ length: 10 }, () =>
      crypto.randomBytes(4).toString('hex').toUpperCase()
    );

    // KS-1052: the backup codes are handed to the user in the response below.
    // Handing out codes that were never stored is worse than failing.
    await userRepo.updateUserOrThrow(user.id, {
      mfaEnabled: true,
      verificationLevel: 'STANDARD',
      mfaBackupCodes: backupCodes,
    }, 'MFA enable');

    logger.info('MFA enabled', { userId: user.id });
    res.json({
      success: true,
      data: { message: 'MFA enabled successfully', backupCodes, verificationLevel: 'STANDARD' },
    });
  } catch (error) {
    next(error);
  }
});

/** POST /api/users/me/mfa/disable */
userRoutes.post('/me/mfa/disable', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const { code } = req.body;
    const user = await userRepo.getUserById(req.user!.userId);
    if (!user) throw new NotFoundError('User');
    if (!user.mfaEnabled) throw new BadRequestError('MFA is not enabled');

    if (!code || typeof code !== 'string' || code.length !== 6) {
      throw new BadRequestError('Valid 6-digit verification code required');
    }

    if (user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {
      throw new BadRequestError('Invalid verification code');
    }

    // KS-1052: a false "MFA disabled" is a lockout — the user stops carrying
    // their authenticator for a factor that is still enforced.
    await userRepo.updateUserOrThrow(user.id, {
      mfaEnabled: false,
      mfaSecret: undefined,
      verificationLevel: 'BASIC',
    } as any, 'MFA disable');

    logger.info('MFA disabled', { userId: user.id });
    res.json({ success: true, message: 'MFA disabled successfully' });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// VERIFICATION REQUEST WORKFLOW
// =============================================================================

// =============================================================================
// VERIFICATION REQUEST WORKFLOW — DB-backed with in-memory fallback
// =============================================================================

import { query as dbQuery, isDbAvailable } from '../db';

interface VerificationRequest {
  id: string;
  userId: string;
  currentLevel: string;
  targetLevel: string;
  documents: string[];
  status: 'PENDING' | 'IN_REVIEW' | 'APPROVED' | 'REJECTED';
  submittedAt: string;
  reviewedAt?: string;
  reviewedBy?: string;
  rejectionReason?: string;
}

const memVerificationRequests = new Map<string, VerificationRequest>();

// KS-1194 (Kam, fail-closed): a save that did not persist is never acknowledged.
// It used to set the in-memory copy first, swallow a failed INSERT with a warning
// and return, so POST /me/verification answered 200 PENDING for a row that did not
// exist and the review answered "approved" over a row still PENDING. The row is now
// written first and the memory copy set only after it lands; a failure throws
// (infrastructure → 503, anything else rethrown). With no database at all the
// memory-only path is unchanged (whether it should exist is KS-1018's item 3).
async function saveVerificationRequest(req: VerificationRequest): Promise<void> {
  if (!isDbAvailable()) {
    memVerificationRequests.set(req.id, req);
    return;
  }
  try {
    await dbQuery(
      `INSERT INTO verification_upgrade_requests
         (id, user_id, current_level, target_level, documents, status, submitted_at, reviewed_at, reviewed_by, rejection_reason)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
       ON CONFLICT (id) DO UPDATE SET
         status = EXCLUDED.status, reviewed_at = EXCLUDED.reviewed_at,
         reviewed_by = EXCLUDED.reviewed_by, rejection_reason = EXCLUDED.rejection_reason`,
      [req.id, req.userId, req.currentLevel, req.targetLevel, req.documents,
       req.status, req.submittedAt, req.reviewedAt || null, req.reviewedBy || null, req.rejectionReason || null],
    );
  } catch (err: any) {
    logger.error('DB saveVerificationRequest failed', { error: err?.message, code: err?.code });
    if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    throw err;
  }
  memVerificationRequests.set(req.id, req);
}

async function getVerificationRequest(id: string): Promise<VerificationRequest | null> {
  if (isDbAvailable()) {
    try {
      const result = await dbQuery(
        `SELECT * FROM verification_upgrade_requests WHERE id = $1 LIMIT 1`, [id],
      );
      if (result.rows.length > 0) {
        const r = result.rows[0];
        return {
          id: r.id, userId: r.user_id, currentLevel: r.current_level,
          targetLevel: r.target_level, documents: r.documents || [],
          status: r.status, submittedAt: r.submitted_at?.toISOString?.() || r.submitted_at,
          reviewedAt: r.reviewed_at?.toISOString?.() || r.reviewed_at || undefined,
          reviewedBy: r.reviewed_by || undefined,
          rejectionReason: r.rejection_reason || undefined,
        };
      }
    } catch (err: any) { // KS-1018: name the error and rethrow infrastructure failures so they surface instead of reading stale memory
      logger.error('DB getVerificationRequest failed', { error: err?.message, code: err?.code });
      if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
  }
  return memVerificationRequests.get(id) || null;
}

async function findPendingVerificationRequest(userId: string): Promise<VerificationRequest | null> {
  if (isDbAvailable()) {
    try {
      const result = await dbQuery(
        `SELECT * FROM verification_upgrade_requests WHERE user_id = $1 AND status = 'PENDING' LIMIT 1`,
        [userId],
      );
      if (result.rows.length > 0) {
        const r = result.rows[0];
        return {
          id: r.id, userId: r.user_id, currentLevel: r.current_level,
          targetLevel: r.target_level, documents: r.documents || [],
          status: r.status, submittedAt: r.submitted_at?.toISOString?.() || r.submitted_at,
        };
      }
      return null;
    } catch (err: any) { // KS-1018: name the error and rethrow infrastructure failures so they surface instead of reading stale memory
      logger.error('DB findPendingVerificationRequest failed', { error: err?.message, code: err?.code });
      if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
  }
  return Array.from(memVerificationRequests.values()).find(
    r => r.userId === userId && r.status === 'PENDING'
  ) || null;
}

async function listUserVerificationRequests(userId: string): Promise<VerificationRequest[]> {
  if (isDbAvailable()) {
    try {
      const result = await dbQuery(
        `SELECT * FROM verification_upgrade_requests WHERE user_id = $1 ORDER BY submitted_at DESC`,
        [userId],
      );
      return result.rows.map((r: any) => ({
        id: r.id, userId: r.user_id, currentLevel: r.current_level,
        targetLevel: r.target_level, documents: r.documents || [],
        status: r.status, submittedAt: r.submitted_at?.toISOString?.() || r.submitted_at,
        reviewedAt: r.reviewed_at?.toISOString?.() || r.reviewed_at || undefined,
        reviewedBy: r.reviewed_by || undefined,
        rejectionReason: r.rejection_reason || undefined,
      }));
    } catch (err: any) { // KS-1018: name the error and rethrow infrastructure failures so they surface instead of reading stale memory
      logger.error('DB listUserVerificationRequests failed', { error: err?.message, code: err?.code });
      if (isInfrastructureDbError(err)) throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
  }
  return Array.from(memVerificationRequests.values())
    .filter(r => r.userId === userId)
    .sort((a, b) => new Date(b.submittedAt).getTime() - new Date(a.submittedAt).getTime());
}

/** POST /api/users/me/verification — Request verification level upgrade */
userRoutes.post('/me/verification', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const data = verificationRequestSchema.parse(req.body);
    const user = await userRepo.getUserById(req.user!.userId);
    if (!user) throw new NotFoundError('User');

    const LEVEL_ORDER = ['BASIC', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT'];
    const currentIndex = LEVEL_ORDER.indexOf(user.verificationLevel);
    const targetIndex = LEVEL_ORDER.indexOf(data.targetLevel);

    if (targetIndex <= currentIndex) {
      throw new BadRequestError(
        `Cannot request ${data.targetLevel} — current level is already ${user.verificationLevel}`
      );
    }

    const existingRequest = await findPendingVerificationRequest(user.id);
    if (existingRequest) throw new BadRequestError('A verification request is already pending');

    if (data.targetLevel === 'STANDARD' && user.mfaEnabled) {
      await userRepo.updateUser(user.id, { verificationLevel: 'STANDARD' });
      logger.info('Verification auto-approved (MFA enabled)', { userId: user.id, newLevel: 'STANDARD' });
      return res.json({
        success: true,
        message: 'Verification level upgraded to STANDARD (MFA already enabled)',
        data: { currentLevel: 'STANDARD', targetLevel: data.targetLevel, status: 'APPROVED' },
      });
    }

    const requestId = `vr-${require('crypto').randomUUID()}`;
    const request: VerificationRequest = {
      id: requestId,
      userId: user.id,
      currentLevel: user.verificationLevel,
      targetLevel: data.targetLevel,
      documents: data.documents || [],
      status: 'PENDING',
      submittedAt: new Date().toISOString(),
    };
    await saveVerificationRequest(request);

    logger.info('Verification upgrade requested', { requestId, userId: user.id, targetLevel: data.targetLevel });
    res.json({
      success: true,
      message: 'Verification request submitted for review',
      data: { requestId, currentLevel: user.verificationLevel, targetLevel: data.targetLevel, status: 'PENDING' },
    });
  } catch (error) {
    next(error);
  }
});

/** GET /api/users/me/verification */
userRoutes.get('/me/verification', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const user = await userRepo.getUserById(req.user!.userId);
    if (!user) throw new NotFoundError('User');

    const requests = await listUserVerificationRequests(user.id);
    res.json({ success: true, data: { currentLevel: user.verificationLevel, requests } });
  } catch (error) {
    next(error);
  }
});

/** POST /api/users/verification/:requestId/review — Admin review */
userRoutes.post('/verification/:requestId/review', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const { requestId } = req.params;
    const { action, reason } = req.body;

    if (!['SYSTEM_ADMIN', 'ORG_ADMIN', 'super_admin', 'SUPER_ADMIN'].includes(req.user!.role as string)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin role required' } });
    }

    const request = await getVerificationRequest(requestId);
    if (!request) throw new NotFoundError('Verification request');

    // KS-467: verification_upgrade_requests carries no RLS policy (the
    // lookup above is a bare by-id read), so re-check the SUBJECT user's
    // tenant before acting. Resolve the subject under platform scope (the
    // /lookup template — don't depend on RLS binding) and require a
    // tenant-scoped admin's subject to be in the caller's own tenant. A
    // foreign-tenant subject yields the same 404 as a missing request,
    // disclosing nothing across the boundary; platform admins review any.
    const callerIsPlatform = isPlatformAdmin(req.user!.role as string);
    if (!callerIsPlatform) {
      const subject = await userRepo.getUserByIdPlatformScope(request.userId);
      const callerTenantId = req.user?.tenantId as string | undefined;
      if (!subject || !callerTenantId || subject.tenantId !== callerTenantId) {
        throw new NotFoundError('Verification request');
      }
    }

    if (request.status !== 'PENDING') throw new BadRequestError(`Request already ${request.status}`);

    if (action === 'approve') {
      // KS-1194 (Kam: "approve raises the level only after the row persists"):
      // the APPROVED row is saved FIRST (a failed save throws before the level
      // moves), then the level is raised. A copy is saved, never the looked-up
      // object, which may be the in-memory map's own entry. The two writes cannot
      // share one transaction: updateUser issues its own query (possibly on a
      // tenant pool) and takes no client. So if raising the level fails or matches
      // no row (updateUser answers null, KS-943), the row is restored to PENDING and
      // the review answers 503; if that restore also fails, the row may read
      // APPROVED at an unchanged level, which is logged as an error with the request id.
      const approved: VerificationRequest = {
        ...request, status: 'APPROVED', reviewedAt: new Date().toISOString(), reviewedBy: req.user!.userId,
      };
      await saveVerificationRequest(approved);
      let raised: unknown = null;
      try {
        // KS-467: platform-scope write — the subject may sit in another tenant
        // (platform-admin review), and the app-layer tenant gate above is the
        // enforcement for tenant-scoped admins.
        raised = await userRepo.updateUserPlatformScope(request.userId, { verificationLevel: request.targetLevel as any });
      } catch (err: any) {
        logger.error('Verification approve: raising the verification level failed', { requestId, userId: request.userId, error: err?.message });
      }
      if (!raised) {
        try {
          await saveVerificationRequest({ ...request, status: 'PENDING', reviewedAt: undefined, reviewedBy: undefined });
        } catch (restoreErr: any) {
          logger.error(
            'Verification approve: the level was not raised and the request row could not be restored to PENDING; the row may read APPROVED at an unchanged level',
            { requestId, userId: request.userId, error: restoreErr?.message },
          );
        }
        throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
      }
      logger.info('Verification request approved', { requestId, userId: request.userId, newLevel: request.targetLevel });
      res.json({ success: true, message: 'Verification approved', data: approved });
    } else if (action === 'reject') {
      const rejected: VerificationRequest = {
        ...request, status: 'REJECTED', reviewedAt: new Date().toISOString(), reviewedBy: req.user!.userId,
        rejectionReason: reason || 'Requirements not met',
      };
      await saveVerificationRequest(rejected);
      logger.info('Verification request rejected', { requestId, userId: request.userId, reason });
      res.json({ success: true, message: 'Verification rejected', data: rejected });
    } else {
      throw new BadRequestError('Action must be "approve" or "reject"');
    }
  } catch (error) {
    next(error);
  }
});
