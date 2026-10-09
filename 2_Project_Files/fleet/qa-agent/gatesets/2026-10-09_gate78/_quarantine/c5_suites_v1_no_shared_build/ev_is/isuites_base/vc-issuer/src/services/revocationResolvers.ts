/**
 * =============================================================================
 * KS-1352 - REVOCATION RESOLVERS FOR THE VERIFY PATH
 * =============================================================================
 * A revoked credential must fail verification, by EITHER revoke route. Kam ruled option (a):
 * "Fix verify properly: a revoked credential fails".
 *
 * The two revoke routes write to two DIFFERENT authorities, and before this module the verify
 * path consulted neither:
 *   - `POST /api/credentials/:id/revoke` -> `credentialRepo.revoke()`, which writes `revoked`,
 *     `revokedAt` and `revocationReason` into the STORED record's `credentialStatus`;
 *   - `POST /api/status/:id/revoke`      -> the status list manager's own revocation bit.
 * `POST /api/credentials/verify` wired no resolver at all, so `checkStatus()` returned
 * `{ valid: errors.length === 0 }` over an empty error list - i.e. VALID - and nothing anywhere
 * read `credentialStatus.revoked`.
 *
 * This lives in one place because TWO routes had the same defect: the credentials verify route
 * and `POST /api/presentations/verify`, which called the same shared verifier with no config.
 *
 * BOTH RESOLVERS ARE KEYED BY CREDENTIAL ID. The issue route allocates
 * `credentialStatus.statusListIndex` from its own module counter, which is a different sequence
 * from the status list manager's `allocateIndex()` - so an index from one is not a valid key into
 * the other, and resolving revocation by index can test an unrelated bit.
 * =============================================================================
 */

import type { VCVerifierConfig } from '@secuura/shared/vc';
import * as credentialRepo from '../repositories/credentialRepo';
import { statusListRevocation } from '../routes/status';

/**
 * The revocation half of a verifier config, for spreading into a `verifyCredential` call.
 *
 * Built per call rather than held as a constant: `credentialRepo`'s backing store and the status
 * list managers are both process state that changes as credentials are issued and revoked, and a
 * resolver captured once at module load would read a snapshot of it.
 */
export function revocationVerifierConfig(): Pick<
  VCVerifierConfig,
  'storedRecordResolver' | 'statusListRevocationResolver'
> {
  return {
    /**
     * ARM 1 - the stored issuer record.
     *
     * `found: false` when the repository has no record for this id, and the verifier then
     * ABSTAINS rather than failing closed. That is deliberate and it is the boundary of Kam's
     * ruling: he ruled that a REVOKED credential fails, not that an unknown one does. Failing
     * closed here would refuse every credential on a process with no database, because
     * `credentialRepo.loadFromDb()` returns silently when the database is unavailable and the
     * memory store then starts empty. The gap this leaves - a revoked credential whose record was
     * lost still verifies - is recorded on the ticket rather than closed here.
     */
    storedRecordResolver: async (credentialId: string) => {
      const record = await credentialRepo.getById(credentialId);
      if (!record) {
        return { found: false, revoked: false };
      }
      const status = record.credentialStatus;
      return {
        found: true,
        revoked: status?.revoked === true,
        revocationReason: status?.revocationReason,
      };
    },

    /**
     * ARM 2 - the status list's own bit, across every list this process holds.
     *
     * Separate from arm 1 so the rule stays an OR of two independently checkable conditions: a
     * credential revoked through only one route must still fail.
     */
    statusListRevocationResolver: async (credentialId: string) => statusListRevocation(credentialId),
  };
}
