/**
 * =============================================================================
 * KS-566 — G-1 split alignment (Kam's ruling 2026-08-05, KS-539)
 * =============================================================================
 *   onBehalfOf pattern = share / revoke / transfer-custody
 *   connector pattern  = anchor / lifecycle
 *
 * The ticket asks for three call-site moves. It does NOT say what the
 * measurement on 2026-08-22 says: `handleOnBehalfOf` is the ONLY writer of an
 * `action_provenance` row and fires ONLY when the caller supplied the field
 * (all 4,641 rows on demo carry the full triplet; zero connector-only rows
 * exist). So dropping the field from lifecycle-events and flat anchors, as
 * written, would leave those two operations writing NO provenance row at all —
 * trading a named actor for no actor, on the two routes carrying most of S's
 * traffic.
 *
 * These tests pin the fallback that makes the split safe: the row is built
 * from ONE pure function, and a connector write with no `onBehalfOf` still
 * produces exactly one row — attributed to the connector, with every PII
 * column NULL.
 */

// provenance.ts imports ../db, whose config demands DATABASE_URL at module
// load, and buildProvenanceRow encrypts with the platform keyring — provision
// both before the import (no connection is made; these tests never touch the
// DB). Same pattern as ks480-provenance.test.ts.
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
process.env.PII_ENCRYPTION_KEY = process.env.PII_ENCRYPTION_KEY || 'a'.repeat(64);

import { registerKey, setActiveVersion, registerLookupHmacKey, __resetKeyringForTesting } from '@secuura/shared';

// eslint-disable-next-line @typescript-eslint/no-var-requires
const { buildProvenanceRow } = require('../services/provenance');

// The keyring is initialised at service startup, not lazily from env — mirror
// that here (same pattern as lifecyclePayloadCodec.test.ts).
beforeAll(() => {
  __resetKeyringForTesting();
  registerKey(1, 'a'.repeat(64));
  setActiveVersion(1);
  registerLookupHmacKey('b'.repeat(64));
});

afterAll(() => __resetKeyringForTesting());

const TENANT = 'a0000000-0000-4000-8000-000000000001';
const ORG = 'b0000000-0000-4000-8000-000000000002';
const CONNECTOR = 'connector:platform-s:4f12ab';
const DOC = 'doc-0000000000000-5eeded0c';
const OBO = { email: 'jane@org.example', displayName: 'Jane Doe', externalRef: 'person-guid-1' };

describe('KS-566 — connector-only provenance (the G-1 fallback)', () => {
  it('builds a full attributed row when onBehalfOf is present (unchanged behaviour)', () => {
    const row = buildProvenanceRow({
      documentId: DOC, action: 'share', tenantId: TENANT, organizationId: ORG,
      connectorId: CONNECTOR, obo: OBO, resolvedUserId: null,
    });
    expect(row.tenantId).toBe(TENANT);
    expect(row.action).toBe('share');
    expect(row.connectorId).toBe(CONNECTOR);
    // PII columns carry ciphertext, never plaintext.
    expect(row.emailEnc).toBeTruthy();
    expect(row.emailEnc).not.toContain('jane@org.example');
    expect(row.displayNameEnc).toBeTruthy();
    expect(row.displayNameEnc).not.toContain('Jane Doe');
    expect(row.emailHash).toBeTruthy();
    expect(row.externalRef).toBe('person-guid-1');
  });

  it('builds a CONNECTOR-ONLY row when onBehalfOf is absent — one row, no principal', () => {
    const row = buildProvenanceRow({
      documentId: DOC, action: 'lifecycle:rename', tenantId: TENANT, organizationId: ORG,
      connectorId: CONNECTOR, obo: null,
    });
    expect(row.tenantId).toBe(TENANT);
    expect(row.documentId).toBe(DOC);
    expect(row.action).toBe('lifecycle:rename');
    // The connector IS the actor on this path — that is the whole point.
    expect(row.connectorId).toBe(CONNECTOR);
    // Every identity column is NULL: there is no principal, and we must not
    // invent one. `external_ref` too — it is S's PersonGuid, not the key's.
    expect(row.emailEnc).toBeNull();
    expect(row.displayNameEnc).toBeNull();
    expect(row.emailHash).toBeNull();
    expect(row.externalRef).toBeNull();
    expect(row.resolvedUserId).toBeNull();
  });

  it('builds a connector-only row for the flat-anchor action too', () => {
    const row = buildProvenanceRow({
      documentId: DOC, action: 'anchor', tenantId: TENANT,
      connectorId: CONNECTOR, obo: null,
    });
    expect(row.action).toBe('anchor');
    expect(row.connectorId).toBe(CONNECTOR);
    expect(row.emailHash).toBeNull();
  });

  it('never emits plaintext PII into any column, on either path', () => {
    const attributed = JSON.stringify(buildProvenanceRow({
      documentId: DOC, action: 'revoke', tenantId: TENANT, connectorId: CONNECTOR, obo: OBO,
    }));
    expect(attributed).not.toContain('jane@org.example');
    expect(attributed).not.toContain('Jane Doe');
    // externalRef is the deliberate exception — it is the pseudonym that
    // SURVIVES erasure (migration 041 / Peter §6-2), so it is stored plain.
    expect(attributed).toContain('person-guid-1');
  });

  it('a connector-only row carries no erasure handle, because there is nothing to erase', () => {
    const row = buildProvenanceRow({
      documentId: DOC, action: 'lifecycle:delete', tenantId: TENANT, connectorId: CONNECTOR, obo: null,
    });
    // email_hash is the GDPR lookup key. A row with no subject must not carry
    // one — a non-null hash here would make erasure claim a subject it cannot
    // name.
    expect(row.emailHash).toBeNull();
  });
});
