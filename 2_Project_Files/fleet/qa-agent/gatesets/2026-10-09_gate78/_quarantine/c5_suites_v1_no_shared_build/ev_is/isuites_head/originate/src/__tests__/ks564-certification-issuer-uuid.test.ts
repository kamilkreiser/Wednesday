/**
 * =============================================================================
 * KS-564 — the certification write path is a FOURTH connector-principal site
 * =============================================================================
 * The original KS-564 fix folded the non-UUID connector principal on
 * `/share` and `/lifecycle-events`. The live end-to-end proof of Option A
 * (connector token accepted on `/api/users/stub`) then reached a site the fix
 * had not covered: `saveCertification` writes `cert.issuer.id` into
 * `documents.issuer_user_id` and `certification_events.actor_user_id`, both
 * `UUID`. A connector-issued certification therefore threw Postgres 22P02
 * (`invalid input syntax for type uuid: "connector:platform-s:<ref>"`), which
 * Stuart's KS-564 error mapping surfaced as a 400 "Certification payload
 * contains values that cannot be stored" — i.e. a server-side column-type
 * fault reported as if the client's payload were at fault.
 *
 * These tests pin the fold and, just as importantly, that the human path is
 * untouched: a real user's UUID must still land in `issuer_user_id`.
 *
 * Attribution is not lost by the fold — `certification_metadata.issuerId`
 * still carries the raw connector principal, and `fromDbRow` reads
 * `row.issuer_user_id || certMeta.issuerId`, so the connector identity
 * survives a round-trip.
 * =============================================================================
 */

import { toActorUuid } from '../utils/principalId';

const CONNECTOR = 'connector:platform-s:ks564-liveproof-001';
const HUMAN = 'a0000000-0000-4000-8000-000000000010';
const RESOLVED = 'b0000000-0000-4000-8000-000000000020';

describe('KS-564 — certification issuer folding', () => {
  it('folds a connector issuer to NULL so the UUID cast cannot throw 22P02', () => {
    expect(toActorUuid(CONNECTOR)).toBeNull();
  });

  it('preserves a human issuer unchanged — the normal certify path must not regress', () => {
    expect(toActorUuid(HUMAN)).toBe(HUMAN);
  });

  it('prefers a resolved user over the connector principal when one is supplied', () => {
    expect(toActorUuid(CONNECTOR, RESOLVED)).toBe(RESOLVED);
  });

  it('folds rather than throwing on the exact principal that failed live', () => {
    // The literal value from the 2026-08-07 local reproduction.
    expect(() => toActorUuid(CONNECTOR)).not.toThrow();
    expect(toActorUuid(CONNECTOR)).toBeNull();
  });
});

describe('KS-564 — certificationRepo applies the fold at both cast sites', () => {
  // The defect was not in the helper (already correct) but in the repo not
  // calling it. Assert against the source so a future edit that reintroduces a
  // raw `cert.issuer.id` cast fails here rather than in production.
  const src = require('fs').readFileSync(
    require('path').join(__dirname, '../repositories/certificationRepo.ts'),
    'utf8',
  );

  it('imports the fold helper', () => {
    expect(src).toContain("import { toActorUuid } from '../utils/principalId'");
  });

  it('never casts the raw issuer principal to uuid', () => {
    expect(src).not.toContain('${cert.issuer.id}::uuid');
  });

  it('casts the folded value at both actor columns', () => {
    const matches = src.match(/\$\{issuerUserId\}::uuid/g) || [];
    expect(matches).toHaveLength(2);
  });

  it('still records the raw principal in certification_metadata for attribution', () => {
    expect(src).toContain('issuerId: cert.issuer.id');
  });
});
