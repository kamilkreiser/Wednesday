/**
 * KS-480 §6 — on-behalf-of provenance: validation semantics.
 *
 * extractOnBehalfOf: connector-only (JWT callers 400), KS-202-trimmed shape.
 * The anchoring-side structural exclusion regression (provenance never in the
 * anchored payload) lives in services/anchoring
 * ks480-provenance-exclusion.test.ts — originate's auto-anchor body
 * (documents.ts buildAnchorBody) is a fixed-field literal with no caller
 * spread, and anchoring's schema strips unknown keys on the second hop.
 */

import type { Request } from 'express';

// provenance.ts imports ../db, whose config demands DATABASE_URL at module
// load — provision a dummy before the import (no connection is made; these
// tests never touch the DB).
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

// eslint-disable-next-line @typescript-eslint/no-var-requires
const { extractOnBehalfOf, onBehalfOfSchema, OnBehalfOfError } = require('../services/provenance');

function reqWith(body: unknown, role?: string): Request {
  return { body, user: role ? { role, userId: 'connector:test', organizationId: 'org-1' } : undefined } as unknown as Request;
}

const OBO = { email: 'jane@org.example', displayName: 'Jane Doe', externalRef: 'guid-1' };

describe('KS-480 — extractOnBehalfOf', () => {
  it('returns null when absent', () => {
    expect(extractOnBehalfOf(reqWith({}, 'connector'))).toBeNull();
    expect(extractOnBehalfOf(reqWith({ title: 'x' }, 'ISSUER_ADMIN'))).toBeNull();
  });

  it('accepts a valid triplet from a connector', () => {
    expect(extractOnBehalfOf(reqWith({ onBehalfOf: OBO }, 'connector'))).toEqual(OBO);
  });

  it('400s a JWT (non-connector) caller sending it', () => {
    expect.assertions(2);
    try {
      extractOnBehalfOf(reqWith({ onBehalfOf: OBO }, 'ISSUER_ADMIN'));
    } catch (e) {
      expect(e).toBeInstanceOf(OnBehalfOfError);
      expect((e as InstanceType<typeof OnBehalfOfError>).status).toBe(400);
    }
  });

  it('400s malformed shapes (bad email / blank displayName / oversize externalRef / non-object)', () => {
    const bads = [
      { email: 'nope' },
      { email: 'a@b.co', displayName: '   ' },
      { email: 'a@b.co', externalRef: 'x'.repeat(200) },
      'just-a-string',
    ];
    expect.assertions(bads.length * 2);
    for (const bad of bads) {
      try {
        extractOnBehalfOf(reqWith({ onBehalfOf: bad }, 'connector'));
      } catch (e) {
        expect(e).toBeInstanceOf(OnBehalfOfError);
        expect((e as InstanceType<typeof OnBehalfOfError>).status).toBe(400);
      }
    }
  });

  it('trims before validating (KS-202)', () => {
    const parsed = onBehalfOfSchema.parse({ email: '  jane@org.example  ', displayName: ' Jane ' });
    expect(parsed.email).toBe('jane@org.example');
    expect(parsed.displayName).toBe('Jane');
  });
});
