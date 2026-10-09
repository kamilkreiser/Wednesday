/**
 * =============================================================================
 * KS-564 — a connector principal is not a UUID
 * =============================================================================
 * Platform S drives the per-verb endpoints through an `sk_*` connector key. Its
 * JWT principal is the literal string `connector:<platform>:<key-id>` (auth
 * `generateConnectorToken`), NOT a UUID — so writing it into the `UUID` actor
 * columns (`shares.shared_by_id`, `document_lifecycle_events.actor_user_id`)
 * threw Postgres 22P02 and the handlers answered a raw 500. Observed live on
 * the demo VM's originate log (2026-08-05) for every S share / lifecycle write.
 *
 * `POST /api/documents` has always folded a non-UUID owner to NULL and
 * preferred an `onBehalfOf`-resolved same-org user (KS-480 §6); these tests pin
 * the same rule for the per-verb actors.
 * =============================================================================
 */

import { isUuid, toActorUuid } from '../utils/principalId';

const CONNECTOR = 'connector:platform-s:4f125ce6-8cc1-11f1-81f2-96f60c37eec2';
const USER = 'a0000000-0000-4000-8000-000000000010';
const RESOLVED = 'b0000000-0000-4000-8000-000000000020';

describe('KS-564 — isUuid', () => {
  it('accepts a canonical UUID', () => {
    expect(isUuid(USER)).toBe(true);
  });

  it('rejects the connector principal that caused the 22P02', () => {
    expect(isUuid(CONNECTOR)).toBe(false);
  });

  it('rejects non-string and empty values', () => {
    expect(isUuid(undefined)).toBe(false);
    expect(isUuid(null)).toBe(false);
    expect(isUuid('')).toBe(false);
    expect(isUuid(12345)).toBe(false);
  });
});

describe('KS-564 — toActorUuid', () => {
  it('folds a bare connector principal to NULL rather than reaching the ::uuid cast', () => {
    expect(toActorUuid(CONNECTOR, null)).toBeNull();
  });

  it('prefers the onBehalfOf-resolved user, so the row keeps true attribution', () => {
    expect(toActorUuid(CONNECTOR, RESOLVED)).toBe(RESOLVED);
  });

  it('passes an interactive user through unchanged', () => {
    expect(toActorUuid(USER, null)).toBe(USER);
  });

  it('ignores a non-UUID resolved value instead of trusting it blindly', () => {
    // resolveOnBehalfOf returns null when it cannot resolve; guard anyway so a
    // future caller cannot reintroduce the 22P02 through the override path.
    expect(toActorUuid(USER, 'not-a-uuid')).toBe(USER);
    expect(toActorUuid(CONNECTOR, 'not-a-uuid')).toBeNull();
  });
});
