/**
 * =============================================================================
 * Document-write role allow-list — single source of truth (KS-290)
 * =============================================================================
 * The base role allow-list shared by every document-MUTATION verb in
 * `routes/documents.ts`: create, version, sign-cert, share, and
 * transfer-custody. These verbs are all "an issuer acts on a document in
 * their tenant", so they must grant the SAME role set; a connector (`sk_*`)
 * caller still satisfies each route via its per-verb scope (KS-71), checked
 * separately by `isAllowedByRoleOrScope`.
 *
 * Why this const exists rather than a literal per route:
 *   KS-290 — `transfer-custody` was originally written (KS-68) with a
 *   narrower literal (`['ORG_ADMIN','SYSTEM_ADMIN','SUPER_ADMIN']`) that
 *   omitted `ISSUER_ADMIN`, so a document's own issuer/owner got a 403 on
 *   their own document while they could freely create / version / share it.
 *   Every sibling verb already used the wider list, so the lists had
 *   silently drifted. Centralising the base here makes that drift
 *   impossible: change the policy once, every doc-write verb moves together.
 *
 * NOTE — verbs that intentionally differ do NOT use this const:
 *   - `POST /:id/revoke` is gated owner-only (`document.owner.id === user.id`),
 *     a deliberately tighter model for lifecycle-state changes.
 *   - The `OWNER` role (public self-signups, KS-151) is deliberately absent:
 *     it carries only the `documents:write` scope, so it can create/version
 *     its own docs but cannot share or transfer custody. That boundary is
 *     preserved because `OWNER` is in neither this list nor those scopes.
 * =============================================================================
 */

/**
 * Roles permitted to perform any document-mutation verb (create, version,
 * sign-cert, share, transfer-custody). `as const` narrows each entry to a
 * string literal and makes the array `readonly`, matching the
 * `isAllowedByRoleOrScope(req, allowedRoles, requiredScope)` signature.
 */
export const DOCUMENT_WRITE_ROLES = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'] as const;
