/**
 * =============================================================================
 * RBAC — role-or-scope authorisation helper (KS-71)
 * =============================================================================
 * Wraps the existing "is the caller's role in this allow-list" gate so that
 * `sk_*` API-key callers (whose role is the literal string `connector`) can
 * still satisfy the gate when their key carries the right scope.
 *
 * The api-gateway already validates scopes on the way in (see
 * `services/api-gateway/src/middleware/scopes.ts`). This helper is the
 * downstream-service counterpart that recognises the same scope on the
 * second hop. Single source of truth for scope strings:
 * `packages/shared/src/security/scopes.ts`.
 *
 * Why this exists rather than a blanket allow-list extension:
 *   - Adding `'CONNECTOR'` to every route's allow-list would duplicate the
 *     scope vocabulary as roles and force every new scope to be issued under
 *     a renamed role.
 *   - Scope-based gating future-proofs the marketplace story (third-party
 *     connectors with restricted scopes like `documents:write` but not
 *     `certifications:write`).
 *   - Defence-in-depth is preserved: human callers still pass through the
 *     role allow-list; only scoped tokens use the scope path.
 * =============================================================================
 */

import type { Request } from 'express';
import { hasScope } from '@secuura/shared/security/scopes';

/**
 * Returns true if the request is authorised by EITHER:
 *   - role is in `allowedRoles` (case-insensitive), OR
 *   - the caller's `scopes` array satisfies `requiredScope` (honours
 *     `<resource>:*` and `*` wildcards via `hasScope`).
 *
 * Returns false otherwise. The route handler is responsible for emitting
 * the 403 response.
 *
 * @param req            the express request (must have `user` attached by
 *                       upstream auth middleware).
 * @param allowedRoles   role strings that always grant access (e.g.
 *                       `['ISSUER_ADMIN','ORG_ADMIN','SYSTEM_ADMIN']`).
 * @param requiredScope  the canonical scope literal from
 *                       `@secuura/shared/security/scopes` (e.g.
 *                       `'documents:write'`).
 */
export function isAllowedByRoleOrScope(
  req: Request,
  allowedRoles: readonly string[],
  requiredScope: string,
): boolean {
  const user = (req as { user?: { role?: string; scopes?: string[] } }).user;
  if (!user) return false;

  // Role path — preserves existing behaviour for JWT-authenticated humans.
  const userRole = String(user.role ?? '').toUpperCase();
  for (const r of allowedRoles) {
    if (r.toUpperCase() === userRole) return true;
  }

  // Scope path — for `sk_*` / OAuth callers.
  const scopes = user.scopes ?? [];
  return hasScope(scopes, requiredScope);
}
