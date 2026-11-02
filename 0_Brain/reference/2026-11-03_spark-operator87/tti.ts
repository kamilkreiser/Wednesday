/**
 * =============================================================================
 * THREAD-TOKEN INDEX (anchoring read path)
 * =============================================================================
 * F6 + AUDIT S-3/S-17 Sprint 2 Phase 1.
 *
 * When the off-chain reads UTxOs back from the chain (during /api/anchors/
 * verify or document-state lookups), it MUST trust only UTxOs carrying a
 * registered state-thread NFT. Without this, an attacker can lock a UTxO
 * at the document_contract script address with any datum and the indexer
 * would believe it (canonical Cardano "datum hijacking").
 *
 * This module is the read-path filter. It reads the state_thread_registry
 * table to get the set of trusted (policy_id, document_id) pairs, then
 * keeps only UTxOs whose value contains exactly one token under one of
 * those policy IDs.
 *
 * **Phase 1 scope (this commit):**
 *   - Read-side helper functions only. No writes — minting + locking is in
 *     services/originate (the issuer side, not the verifier side).
 *   - Optional registry: if the table is empty (pre-NFT-era), the helper
 *     returns the input UTxOs unchanged so the existing metadata-label path
 *     keeps working. The "NFT-required" mode flips on once the migration
 *     to thread tokens is complete and `STRICT_THREAD_TOKEN_INDEX=true` is
 *     set in env.
 *
 * **Phase 2 (deferred):**
 *   - Build the actual mint+lock tx in services/originate (requires CSL or
 *     CML Plutus tx construction — see threadToken.ts header note).
 *   - Add the burn-detection watcher that flips registry rows to 'burned'.
 * =============================================================================
 */

import { query } from '../db';
import { logger } from '../utils/logger';
import {
  StateThreadRegistryEntry,
  CardanoNetwork,
  utxoCarriesThreadToken,
  selectThreadTokenUtxos,
  UtxoLike,
} from '@secuura/shared';

const STRICT_MODE = process.env.STRICT_THREAD_TOKEN_INDEX === 'true';

interface DbRow {
  document_id: string;
  policy_id: string;
  network: string;
  status: string;
}

/**
 * Load the active (document_id, policy_id) pairs for a network. Hot path —
 * caller should cache this if it's calling repeatedly. Returns empty list
 * if the registry table doesn't exist yet (pre-migration-010 environments).
 */
export async function loadActiveRegistry(
  network: CardanoNetwork,
): Promise<Pick<StateThreadRegistryEntry, 'documentId' | 'policyId'>[]> {
  try {
    const result = await query(
      `SELECT document_id, policy_id, network, status
         FROM state_thread_registry
        WHERE network = $1 AND status = 'active'`,
      [network],
    );
    return (result.rows as unknown as DbRow[]).map((r) => ({
      documentId: r.document_id,
      policyId: r.policy_id,
    }));
  } catch (err: any) {
    // The migration may not have run in older environments. Silently degrade
    // to the metadata-label path — STRICT_THREAD_TOKEN_INDEX flips this to a
    // hard error when the migration is mandatory.
    if (STRICT_MODE) {
      logger.error('state_thread_registry unavailable in STRICT mode', {
        error: err?.message,
      });
      throw err;
    }
    logger.debug('state_thread_registry not available — falling back to metadata-only', {
      error: err?.message,
    });
    return [];
  }
}

/**
 * Filter a list of UTxOs to those carrying a registered thread token. In
 * non-strict mode (default), an empty registry is treated as "no NFT scheme
 * deployed yet" and the input list is returned unchanged. In strict mode,
 * a UTxO that does not carry a registered policy ID is dropped from the
 * returned list — callers should treat dropped UTxOs as if they did not
 * exist.
 *
 * Returns triples instead of bare UTxOs so the caller can attribute each
 * surviving UTxO to a known document.
 */
export async function filterUtxosByRegistry<U extends UtxoLike>(
  utxos: U[],
  network: CardanoNetwork,
): Promise<Array<{ utxo: U; documentId: string | null; policyId: string | null }>> {
  const registry = await loadActiveRegistry(network);

  if (registry.length === 0) {
    if (STRICT_MODE) {
      // Strict mode + empty registry = explicit drop of every UTxO. Callers
      // should treat this as "no anchors of trustable provenance" rather
      // than "registry is bootstrapping" — Phase 2 must populate the
      // registry before flipping STRICT on.
      logger.warn('STRICT_THREAD_TOKEN_INDEX=true but registry is empty — dropping all UTxOs');
      return [];
    }
    // Pre-NFT-era anchors: pass through unchanged with null attribution.
    return utxos.map((utxo) => ({ utxo, documentId: null, policyId: null }));
  }

  const matched = selectThreadTokenUtxos(utxos, registry);
  return matched;
}

/**
 * Single-UTxO trust check — returns true iff the UTxO carries a registered
 * thread token (or, in non-strict mode, the registry is empty).
 */
export async function utxoIsTrusted(utxo: UtxoLike, network: CardanoNetwork): Promise<boolean> {
  const registry = await loadActiveRegistry(network);
  if (registry.length === 0) return !STRICT_MODE;
  return registry.some((r) => utxoCarriesThreadToken(utxo, r.policyId));
}
