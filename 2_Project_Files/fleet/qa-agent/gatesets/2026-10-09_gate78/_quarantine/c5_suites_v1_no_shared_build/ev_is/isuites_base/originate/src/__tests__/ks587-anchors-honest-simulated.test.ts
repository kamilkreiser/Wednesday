/**
 * KS-587 — originate's anchor read/write honesty predicate.
 *
 * Mirrors services/anchoring honestAnchor rules: a placeholder transaction id
 * (`tx_sim_`/`mock_tx_`/`tx_…`) or a raw simulated flag marks the anchor
 * simulated — GET /api/anchors/:documentId then nulls the id, sets
 * simulated:true + simulatedTxRef, and never claims verified; saveAnchorToDb
 * persists the flag (it previously dropped it, which is how tx_sim_ rows
 * landed as simulated=false "confirmed on-chain proof").
 */

// routes/anchors.ts imports ../db, whose config demands DATABASE_URL at module
// load — provision a dummy before the import (no connection is made).
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

// eslint-disable-next-line @typescript-eslint/no-var-requires
const { isSimulatedAnchor, FABRICATED_TX_PREFIX } = require('../routes/anchors');

const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';

describe('KS-587 — isSimulatedAnchor', () => {
  it('real hash, flag false/absent → not simulated', () => {
    expect(isSimulatedAnchor(REAL_TX, false)).toBe(false);
    expect(isSimulatedAnchor(REAL_TX, undefined)).toBe(false);
  });

  it.each(['mock_tx_abc', 'tx_sim_abc', 'tx_row-id-fallback'])(
    'placeholder %s → simulated even when the flag lies (incident shape)',
    (placeholder) => {
      expect(isSimulatedAnchor(placeholder, false)).toBe(true);
    },
  );

  it('stored flag true → simulated regardless of hash shape', () => {
    expect(isSimulatedAnchor(REAL_TX, true)).toBe(true);
  });

  it('null/empty id with flag unset → not simulated (no claim either way)', () => {
    expect(isSimulatedAnchor(null, undefined)).toBe(false);
    expect(isSimulatedAnchor('', false)).toBe(false);
  });

  it('prefixes only match at position 0', () => {
    expect(FABRICATED_TX_PREFIX.test('xxmock_tx_1')).toBe(false);
  });
});
