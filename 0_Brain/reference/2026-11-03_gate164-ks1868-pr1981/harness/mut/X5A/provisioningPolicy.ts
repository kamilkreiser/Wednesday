/**
 * =============================================================================
 * PROVISIONING MINT POLICY (KS-480 §4 amendment, 2026-07-30)
 * =============================================================================
 * Who may cause `POST /api/keys` to mint, and within what limits.
 *
 * The gateway's `register-connector` route authorises the *organisational*
 * question (may this caller provision an Organisation, in which tenant, may it
 * rotate) and then asks this service to mint that org's key, forwarding the
 * caller's own credential. So this service must accept a provisioning-scoped
 * connector for the mint — but only within limits it enforces ITSELF, because a
 * key can also be presented here directly, bypassing that route.
 *
 * The three limits, and why each exists:
 *   1. never mint a provisioning scope (`organizations:register`) — no
 *      self-replication, so one leaked provisioning key cannot breed more;
 *   2. never mint a wildcard (`*` / `<resource>:*`) — no escalation to a key
 *      broader than the caller could ever hold;
 *   3. only mint into the caller's OWN tenant.
 *
 * KS-742 correction: limits 1-3 sit BELOW the KEY_ADMIN_ROLES early return, so
 * they bind provisioners and never bound admins. A tenant-scoped ISSUER_ADMIN
 * therefore took `via: 'admin'` and met no tenancy check at all. The admin half
 * of limit 3 is now enforced in the route (index.ts, `decideTenantAccess`)
 * AFTER the tenant is resolved, because this function runs before the body is
 * parsed and cannot see which tenant the key will land in. This header used to
 * state limit 3 as universal; it was true of one branch only.
 *
 * Deliberately NOT a copy of the contract's §8 scope list: that list is the
 * gateway route's business (it refuses any caller-supplied override outright),
 * and duplicating it here would give it two homes that could drift. What lives
 * here is the escalation policy, stable regardless of what §8 contains.
 *
 * Read/revoke of keys stay admin-only — provisioning is create-only.
 *
 * Extracted from index.ts so it is unit-testable without booting the service
 * (index.ts calls app.listen on import) — same reason as anchoring's
 * anchorSchema.ts / threadMintRequest.ts.
 * =============================================================================
 */

/** Roles permitted full API-key management (create/list/revoke). */
export const KEY_ADMIN_ROLES: ReadonlySet<string> = new Set([
  'SYSTEM_ADMIN',
  'SUPER_ADMIN',
  'ORG_ADMIN',
  'ISSUER_ADMIN',
  'ADMIN',
]);

/** The provisioning-only scope from the shared vocabulary (KS-480 §4). */
export const PROVISIONING_SCOPE = 'organizations:register';

/**
 * True when a scope would escalate a provisioning key's own authority — a
 * wildcard, or the provisioning scope itself.
 *
 * @param scope - the requested scope literal.
 * @returns true when a provisioning caller must not be allowed to mint it.
 * @example isEscalatingScope('documents:*') // → true
 */
export function isEscalatingScope(scope: string): boolean {
  return scope === '*' || scope.endsWith(':*') || scope === PROVISIONING_SCOPE;
}

/** The caller identity as attached by the shared JWT middleware. */
export interface MintCaller {
  role?: string;
  scopes?: readonly string[];
  tenantId?: string;
}

/** The mint request fields the policy inspects. */
export interface MintRequest {
  scopes?: unknown;
  tenantId?: unknown;
}

export type MintDecision =
  | { allow: true; via: 'admin' | 'provisioner' }
  | { allow: false; status: 403; message: string; offendingScopes?: string[] };

/**
 * Decide whether a caller may mint an API key with the requested shape.
 *
 * @param caller - the verified principal (role / scopes / tenant).
 * @param body - the mint request (only `scopes` and `tenantId` are inspected).
 * @returns an allow decision naming the authorising path, or a deny with the
 *          message the route should return.
 * @example
 *   decideMint({role: 'SYSTEM_ADMIN'}, {})                       // allow via admin
 *   decideMint({role: 'connector', scopes: ['organizations:register']}, {scopes: ['*']})
 *   // → deny (escalating scope)
 */
export function decideMint(caller: MintCaller | undefined, body: MintRequest): MintDecision {
  const role = String(caller?.role ?? '');
  if (KEY_ADMIN_ROLES.has(role.toUpperCase())) {
    return { allow: true, via: 'admin' };
  }

  const isProvisioner = role === 'connector' && (caller?.scopes ?? []).includes(PROVISIONING_SCOPE);
  if (!isProvisioner) {
    return { allow: false, status: 403, message: 'API key management requires an admin role' };
  }

  // Limit 1 + 2 — no self-replication, no wildcard escalation.
  const requested = Array.isArray(body.scopes) ? (body.scopes as unknown[]) : [];
  const offending = requested.filter((s): s is string => typeof s === 'string' && isEscalatingScope(s));
  if (offending.length > 0) {
    return {
      allow: false,
      status: 403,
      message: `A provisioning key may not mint these scopes: ${offending.join(', ')}`,
      offendingScopes: offending,
    };
  }

  // Limit 3 — own tenant only. An absent body tenant is fine: the mint then
  // resolves the tenant from the key/org, which cannot cross tenants.
  const bodyTenant = typeof body.tenantId === 'string' ? body.tenantId : '';
  if (bodyTenant && caller?.tenantId && bodyTenant !== caller.tenantId) {
    return { allow: false, status: 403, message: 'A provisioning key may only mint keys in its own tenant' };
  }

  return { allow: true, via: 'provisioner' };
}
