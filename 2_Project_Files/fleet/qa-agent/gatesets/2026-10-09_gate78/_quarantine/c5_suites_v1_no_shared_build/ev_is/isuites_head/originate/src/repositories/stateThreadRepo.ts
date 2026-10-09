/**
 * =============================================================================
 * STATE-THREAD REGISTRY REPOSITORY
 * =============================================================================
 * F6 + AUDIT S-3/S-17 Sprint 2 Phase 1.
 *
 * Implements StateThreadRegistry against the local Postgres pool. Backs the
 * `state_thread_registry` table from migration 010. Reads from this table
 * are the off-chain trust root: the indexer trusts ONLY UTxOs carrying a
 * registered policy ID. See packages/shared/src/cardano/threadToken.ts.
 * =============================================================================
 */

import { prisma } from '../db';
import { logger } from '../utils/logger';
import {
  StateThreadRegistry,
  StateThreadRegistryEntry,
  CardanoNetwork,
} from '@secuura/shared';

interface DbRow {
  document_id: string;
  policy_id: string;
  asset_name: string;
  script_address: string;
  seed_tx_out_ref: string;
  mint_tx_hash: string | null;
  network: string;
  originator_pkh: string;
  created_at: Date | string;
  status: string;
  burned_at: Date | string | null;
  burn_tx_hash: string | null;
}

function rowToEntry(r: DbRow): StateThreadRegistryEntry {
  return {
    documentId: r.document_id,
    policyId: r.policy_id,
    assetName: r.asset_name,
    scriptAddress: r.script_address,
    seedTxOutRef: r.seed_tx_out_ref,
    mintTxHash: r.mint_tx_hash,
    network: r.network as CardanoNetwork,
    originatorPkh: r.originator_pkh,
    createdAt: r.created_at instanceof Date ? r.created_at : new Date(r.created_at),
    status: r.status === 'burned' ? 'burned' : 'active',
    burnedAt: r.burned_at
      ? r.burned_at instanceof Date
        ? r.burned_at
        : new Date(r.burned_at)
      : null,
    burnTxHash: r.burn_tx_hash,
  };
}

class PgStateThreadRegistry implements StateThreadRegistry {
  async insert(
    row: Omit<StateThreadRegistryEntry, 'createdAt' | 'burnedAt' | 'burnTxHash' | 'status'>,
  ): Promise<StateThreadRegistryEntry> {
    const result = (await prisma.$queryRawUnsafe(
      `INSERT INTO state_thread_registry
         (document_id, policy_id, asset_name, script_address,
          seed_tx_out_ref, mint_tx_hash, network, originator_pkh)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
       ON CONFLICT (document_id) DO UPDATE
         SET policy_id      = state_thread_registry.policy_id,
             asset_name     = state_thread_registry.asset_name,
             script_address = state_thread_registry.script_address
       RETURNING *`,
      row.documentId,
      row.policyId,
      row.assetName,
      row.scriptAddress,
      row.seedTxOutRef,
      row.mintTxHash,
      row.network,
      row.originatorPkh,
    )) as DbRow[];
    if (!result.length) {
      throw new Error(`Failed to insert state_thread_registry row for ${row.documentId}`);
    }
    return rowToEntry(result[0]);
  }

  async getByDocumentId(documentId: string): Promise<StateThreadRegistryEntry | null> {
    const result = (await prisma.$queryRawUnsafe(
      'SELECT * FROM state_thread_registry WHERE document_id = $1 LIMIT 1',
      documentId,
    )) as DbRow[];
    return result[0] ? rowToEntry(result[0]) : null;
  }

  async getByPolicyId(
    policyId: string,
    network: CardanoNetwork,
  ): Promise<StateThreadRegistryEntry | null> {
    const result = (await prisma.$queryRawUnsafe(
      'SELECT * FROM state_thread_registry WHERE policy_id = $1 AND network = $2 LIMIT 1',
      policyId,
      network,
    )) as DbRow[];
    return result[0] ? rowToEntry(result[0]) : null;
  }

  async markBurned(documentId: string, burnTxHash: string): Promise<void> {
    await prisma.$executeRawUnsafe(
      `UPDATE state_thread_registry
         SET status = 'burned',
             burn_tx_hash = $2
       WHERE document_id = $1
         AND status = 'active'`,
      documentId,
      burnTxHash,
    );
    logger.info('state_thread_registry: marked burned', { documentId, burnTxHash });
  }
}

export const stateThreadRepo: StateThreadRegistry = new PgStateThreadRegistry();
