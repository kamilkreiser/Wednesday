/**
 * =============================================================================
 * PRINCIPAL ID COERCION (KS-564)
 * =============================================================================
 * Connector (`sk_*`) callers authenticate with a JWT whose `userId` is the
 * literal string `connector:<platform>:<key-id>` (auth `generateConnectorToken`)
 * — deliberately NOT a UUID, because a connector is a key, not a user row.
 *
 * Actor columns are `UUID`, so writing a principal id straight into a `::uuid`
 * cast throws Postgres 22P02 ("invalid input syntax for type uuid") and the
 * handler answers a raw 500. `POST /api/documents` has always handled this
 * (documentRepo.saveDocument folds a non-UUID owner to NULL and prefers an
 * `onBehalfOf`-resolved user), but the per-verb endpoints — `/share`,
 * `/lifecycle-events` — never got the same treatment, so every Platform S
 * share / lifecycle write failed on UAT.
 *
 * Attribution when folding to NULL: the connector's identity is recorded on the
 * KS-480 `action_provenance` row for the same operation — but ONLY when the
 * caller supplied `onBehalfOf`, since that is the sole trigger for writing a
 * provenance row. A BARE connector write (no `onBehalfOf`) therefore stores no
 * actor anywhere. That is not a regression — before this fix the write failed
 * outright with a 500 — but it is a real gap, tracked in BACKLOG.md.
 * =============================================================================
 */

const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** True for a canonical UUID string — the only value a `::uuid` cast accepts. */
export function isUuid(value: unknown): value is string {
  return typeof value === 'string' && UUID_PATTERN.test(value);
}

/**
 * Resolve the actor to store in a `UUID` column.
 *
 * @param principalId - the caller's `userId` (a UUID for interactive users, a
 *   `connector:<platform>:<id>` string for `sk_*` connector keys).
 * @param resolvedUserId - an `onBehalfOf`-resolved same-org user id, when the
 *   connector attributed the action to a real person (KS-480 §6). Preferred so
 *   the row carries true per-user attribution rather than NULL.
 * @returns a UUID string, or null when neither is usable.
 * @example
 * // connector with onBehalfOf → the resolved human
 * toActorUuid('connector:platform-s:4f12…', 'a0000000-…-0010') // → 'a0000000-…-0010'
 * // bare connector → NULL, attribution lives on action_provenance
 * toActorUuid('connector:platform-s:4f12…', null)              // → null
 */
export function toActorUuid(
  principalId: unknown,
  resolvedUserId?: string | null,
): string | null {
  if (isUuid(resolvedUserId)) return resolvedUserId;
  if (isUuid(principalId)) return principalId;
  return null;
}
