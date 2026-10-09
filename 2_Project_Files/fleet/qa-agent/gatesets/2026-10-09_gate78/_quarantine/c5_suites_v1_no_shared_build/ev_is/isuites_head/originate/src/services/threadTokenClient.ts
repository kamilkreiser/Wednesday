/**
 * =============================================================================
 * THREAD-TOKEN MINT CLIENT (originate → anchoring RPC)
 * =============================================================================
 * F6 + AUDIT S-3/S-17 Sprint 2 Phase 2 part B.
 *
 * Calls anchoring's POST /api/anchors/thread-mint at document-creation time
 * and persists the returned (policy_id, asset_name, script_address)
 * tuple into state_thread_registry via stateThreadRepo.
 *
 * Design choice: anchoring owns the chain interaction (lucid + wallet);
 * originate owns the registry. The boundary between them is a small RPC.
 *
 * Failure semantics: if the mint fails, document creation MUST NOT silently
 * fall back to the legacy metadata-label-only path — that would leave a
 * "trustable" UTxO without a registry entry, defeating the whole point of
 * the state-thread NFT scheme. Caller should treat any error here as a
 * fatal document-creation failure.
 * =============================================================================
 */

import { logger } from '../utils/logger';
import { stateThreadRepo } from '../repositories/stateThreadRepo';
import { CardanoNetwork, StateThreadRegistryEntry } from '@secuura/shared';

interface MintArgs {
  documentId: string;
  documentHashHex: string;
  originatorPkhHex: string;
  documentType: string;
  metadataHashHex: string;
  deploymentIdHex?: string;
  createdAtMs?: number;
  /** Forwarded as Authorization: Bearer to anchoring (which requires authenticate()). */
  bearerToken: string;
}

interface MintResponse {
  success: boolean;
  data?: {
    policyId: string;
    scriptAddress: string;
    mintTxHash: string;
    seedTxOutRef: string;
    network: CardanoNetwork;
  };
  error?: string;
  details?: string;
}

const ANCHORING_URL = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';

export async function mintAndRegisterThreadToken(args: MintArgs): Promise<StateThreadRegistryEntry> {
  // 1. Skip if a registry entry already exists — idempotent on documentId.
  const existing = await stateThreadRepo.getByDocumentId(args.documentId);
  if (existing) {
    logger.info('thread-token mint: existing registry entry, skipping mint', {
      documentId: args.documentId,
      policyId: existing.policyId,
    });
    return existing;
  }

  // 2. Call anchoring's mint endpoint.
  const url = `${ANCHORING_URL}/api/anchors/thread-mint`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: args.bearerToken,
    },
    body: JSON.stringify({
      documentId: args.documentId,
      documentHashHex: args.documentHashHex,
      originatorPkhHex: args.originatorPkhHex,
      documentType: args.documentType,
      metadataHashHex: args.metadataHashHex,
      deploymentIdHex: args.deploymentIdHex || '',
      createdAtMs: args.createdAtMs,
    }),
  });

  const body = (await resp.json().catch(() => ({}))) as MintResponse;
  if (!resp.ok || !body.success || !body.data) {
    const msg = body.error || body.details || `anchoring returned HTTP ${resp.status}`;
    logger.error('thread-token mint failed', { documentId: args.documentId, error: msg });
    throw new Error(`thread-token mint failed: ${msg}`);
  }

  // 3. Persist into state_thread_registry.
  const entry = await stateThreadRepo.insert({
    documentId: args.documentId,
    policyId: body.data.policyId,
    assetName: '', // canonical empty bytestring; matches THREAD_ASSET_NAME_HEX
    scriptAddress: body.data.scriptAddress,
    seedTxOutRef: body.data.seedTxOutRef,
    mintTxHash: body.data.mintTxHash,
    network: body.data.network,
    originatorPkh: args.originatorPkhHex,
  });

  logger.info('thread-token minted + registered', {
    documentId: args.documentId,
    policyId: entry.policyId,
    mintTxHash: entry.mintTxHash,
  });
  return entry;
}
