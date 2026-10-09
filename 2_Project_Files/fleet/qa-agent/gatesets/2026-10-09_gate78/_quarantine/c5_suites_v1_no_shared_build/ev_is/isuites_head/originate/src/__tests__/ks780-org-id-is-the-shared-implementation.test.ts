/**
 * =============================================================================
 * KS-780 — originate's `normaliseOrgId` IS the shared implementation, not a copy
 * =============================================================================
 * `services/orgId.ts` used to carry originate's own normaliser while the shared
 * revoke policy carried a byte-identical private one. After KS-780 it is a
 * re-export of `@secuura/shared`'s, and this file is the cell that keeps it so:
 * a future "small local tweak" that turned the re-export back into a private
 * function would leave every originate resolver test green while the policy
 * drifted — the exact defect the ticket names — and would red HERE, by name.
 *
 * REAL, not mocked: `@secuura/shared` is imported as is. The three callers
 * (provenance.ts, gdprService.ts, routes/documents.ts) are deliberately NOT
 * loaded — their import lines are byte-identical before and after the move,
 * and their own suites (ks597-*, ks695-*, qa-f4-*) exercise the comparison.
 * =============================================================================
 */

import { readFileSync } from 'fs';
import { join } from 'path';
import * as shared from '@secuura/shared';
import { normaliseOrgId } from '../services/orgId';

// Hex LETTERS on purpose: an all-digit uuid upper-cases to itself and a case
// cell against it proves nothing — measured, the tamper below left it green.
const ORG = 'a1b2c3d4-e5f6-4a7b-8c9d-ef0123456789';

describe('KS-780 — one implementation, seen from originate', () => {
  it('I1 the re-export IS the shared function — identity, not a behaviourally equal copy', () => {
    expect(typeof shared.normaliseOrgId).toBe('function');
    expect(normaliseOrgId).toBe(shared.normaliseOrgId);
  });

  it('I2 the module carries no implementation of its own — its source is a re-export', () => {
    const src = readFileSync(join(__dirname, '..', 'services', 'orgId.ts'), 'utf8');
    expect(src).toMatch(/export \{ normaliseOrgId \} from '@secuura\/shared';/);
    const definitions = src
      .split('\n')
      .filter((l) => /^\s*(export\s+)?(function|const)\s+normaliseOrgId\b/.test(l));
    // Non-empty here means a private definition has come back.
    expect(definitions).toEqual([]);
  });

  it('I3 the properties the resolvers rely on still hold through the re-export', () => {
    expect(normaliseOrgId(`  ${ORG.toUpperCase()} `)).toBe(ORG);
    expect(normaliseOrgId('   ')).toBeNull();
    expect(normaliseOrgId(undefined)).toBeNull();
  });
});
