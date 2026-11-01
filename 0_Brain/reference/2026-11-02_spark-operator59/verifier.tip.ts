/**
 * =============================================================================
 * BLOCKCHAIN VERIFIER SERVICE
 * =============================================================================
 * Verifies on-chain transaction status using the Blockfrost API.
 * Used by the /record endpoint to confirm that a client-submitted
 * minting transaction actually exists on Cardano.
 * =============================================================================
 */

import { BlockFrostAPI } from '@blockfrost/blockfrost-js';
import { logger } from '../utils/logger';

// =============================================================================
// TYPES
// =============================================================================

export interface TransactionVerification {
  verified: boolean;
  status: 'confirmed' | 'pending' | 'not_found' | 'error';
  block?: string;
  slot?: number;
  fees?: string;
  error?: string;
}

// =============================================================================
// SERVICE
// =============================================================================

export class BlockchainVerifierService {
  private api: BlockFrostAPI | null = null;

  /**
   * Lazy-initialise Blockfrost client.
   * Returns null if no API key is configured — verification will be skipped.
   */
  private getClient(): BlockFrostAPI | null {
    if (this.api) return this.api;

    const apiKey = process.env.BLOCKFROST_API_KEY;
    // Treat the dev/demo placeholder as unconfigured. The bicep sets
    // BLOCKFROST_API_KEY='blockfrost-not-configured' when no real key is given;
    // that value is truthy, so it slipped past this guard and
    // `new BlockFrostAPI({ projectId })` threw on the invalid key. Because
    // getClient() runs OUTSIDE the verify* try/catch, the throw surfaced as a
    // 500 on POST /api/nft/verify/{transaction,asset} (KS-144).
    if (!apiKey || apiKey === 'blockfrost-not-configured') {
      logger.warn('BLOCKFROST_API_KEY not set – on-chain verification disabled');
      return null;
    }

    const network = process.env.CARDANO_NETWORK || 'preprod';
    const projectMap: Record<string, string> = {
      preprod: 'https://cardano-preprod.blockfrost.io/api',
      preview: 'https://cardano-preview.blockfrost.io/api',
      mainnet: 'https://cardano-mainnet.blockfrost.io/api',
    };

    try {
      this.api = new BlockFrostAPI({
        projectId: apiKey,
        customBackend: projectMap[network],
      });
    } catch (err: unknown) {
      // A malformed key or unsupported network must degrade to
      // "verification disabled", never escape as a 500.
      logger.warn('Blockfrost client init failed – on-chain verification disabled', {
        error: err instanceof Error ? err.message : String(err),
      });
      return null;
    }

    return this.api;
  }

  /**
   * Verify that a minting transaction exists on-chain.
   *
   * If Blockfrost is not configured the method returns
   * `{ verified: false, status: 'pending' }` so the record is still saved.
   */
  async verifyTransaction(txHash: string): Promise<TransactionVerification> {
    const client = this.getClient();

    if (!client) {
      // No Blockfrost key — accept the record but flag as unverified
      return { verified: false, status: 'pending' };
    }

    try {
      const tx = await client.txs(txHash);

      return {
        verified: true,
        status: 'confirmed',
        block: tx.block,
        slot: tx.slot,
        fees: tx.fees,
      };
    } catch (err: unknown) {
      // Blockfrost returns 404 for transactions not yet on-chain
      const statusCode = (err as { status_code?: number }).status_code;

      if (statusCode === 404) {
        return { verified: false, status: 'not_found' };
      }

      logger.error('Error verifying transaction', { error: err instanceof Error ? err.message : String(err) });
      return {
        verified: false,
        status: 'error',
        error: (err as Error).message ?? 'Unknown error',
      };
    }
  }

  /**
   * Look up a specific asset on-chain by policy ID + hex asset name.
   */
  async verifyAsset(
    policyId: string,
    assetNameHex: string,
  ): Promise<{ exists: boolean; quantity?: string }> {
    const client = this.getClient();
    if (!client) return { exists: false };

    try {
      const asset = await client.assetsById(`${policyId}${assetNameHex}`);
      return { exists: true, quantity: asset.quantity };
    } catch {
      return { exists: false };
    }
  }
}

// =============================================================================
// SINGLETON EXPORT
// =============================================================================

export const blockchainVerifier = new BlockchainVerifierService();
