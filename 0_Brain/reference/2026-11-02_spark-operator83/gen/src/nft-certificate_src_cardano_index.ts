/**
 * =============================================================================
 * CARDANO NFT INTEGRATION — ORCHESTRATION
 * =============================================================================
 * Top-level module for real Cardano NFT minting.
 *
 * Behaviour:
 *   - When BLOCKFROST_API_KEY + PLATFORM_WALLET_MNEMONIC are set → real minting
 *   - When either is missing → gracefully disabled (caller falls back to mock)
 * =============================================================================
 */

import { initProvider, fetchProtocolParams, submitTransaction, getTransaction, ProtocolParams } from './provider';
import { initWallet, PlatformWallet } from './wallet';
import { createSignaturePolicy, MintingPolicy } from './mintPolicy';
import { buildMintTransaction } from './mintTransaction';

let cardanoReady = false;
let wallet: PlatformWallet | null = null;
let mintingPolicy: MintingPolicy | null = null;
let cachedParams: ProtocolParams | null = null;
let paramsRefreshedAt = 0;

const PARAMS_CACHE_TTL_MS = 5 * 60 * 1000;

/**
 * Initialise the Cardano NFT integration.
 * Returns true if real minting is available.
 */
export async function initCardanoNFT(network: string): Promise<boolean> {
  const apiKey = process.env.BLOCKFROST_API_KEY;
  const mnemonic = process.env.PLATFORM_WALLET_MNEMONIC;

  if (!apiKey || !mnemonic) {
    console.log('[Cardano-NFT] BLOCKFROST_API_KEY or PLATFORM_WALLET_MNEMONIC not set — mock mode');
    return false;
  }

  try {
    const provider = initProvider(apiKey, network);
    if (!provider) return false;

    wallet = initWallet(mnemonic, network);
    console.log(`[Cardano-NFT] Platform wallet: ${wallet.address}`);

    // Create the default minting policy (signature-based)
    mintingPolicy = createSignaturePolicy(wallet);
    console.log(`[Cardano-NFT] Minting policy ID: ${mintingPolicy.policyId}`);

    cachedParams = await fetchProtocolParams();
    if (!cachedParams) return false;
    paramsRefreshedAt = Date.now();

    cardanoReady = true;
    console.log(`[Cardano-NFT] Integration ready — network: ${network}`);
    return true;
  } catch (err: any) {
    console.error(`[Cardano-NFT] Initialisation failed: ${err?.message}`);
    return false;
  }
}

export function isCardanoNFTReady(): boolean {
  return cardanoReady;
}

export function getWalletAddress(): string | null {
  return wallet?.address ?? null;
}

export function getPolicyId(): string | null {
  return mintingPolicy?.policyId ?? null;
}

async function ensureFreshParams(): Promise<ProtocolParams> {
  if (!cachedParams || Date.now() - paramsRefreshedAt > PARAMS_CACHE_TTL_MS) {
    const fresh = await fetchProtocolParams();
    if (fresh) {
      cachedParams = fresh;
      paramsRefreshedAt = Date.now();
    }
  }
  if (!cachedParams) throw new Error('Protocol parameters unavailable');
  return cachedParams;
}

// ---------------------------------------------------------------------------
// PUBLIC API
// ---------------------------------------------------------------------------

export interface NFTMintResult {
  txHash: string;
  policyId: string;
  assetName: string;
  fee: number;
}

/**
 * Mint an NFT certificate on Cardano.
 *
 * @param recipientAddress  - Bech32 address to receive the minted NFT
 * @param assetName         - Human-readable asset name
 * @param cip25Metadata     - CIP-25 compliant metadata
 */
export async function mintNFTOnChain(
  recipientAddress: string,
  assetName: string,
  cip25Metadata: Record<string, unknown>,
): Promise<NFTMintResult> {
  if (!cardanoReady || !wallet || !mintingPolicy) {
    throw new Error('Cardano NFT integration not ready');
  }

  const params = await ensureFreshParams();

  const result = await buildMintTransaction(
    wallet,
    params,
    mintingPolicy,
    assetName,
    recipientAddress,
    cip25Metadata,
  );

  // KS-444: submission failures (mempool rejections like "All inputs are
  // spent", provider outages) are chain-side, never a client-input fault —
  // tag them with a stable prefix so classifyMintError maps them to a 503
  // instead of blaming the caller with a 400.
  let submittedHash: string;
  try {
    submittedHash = await submitTransaction(result.txCborHex);
  } catch (err: unknown) {
    const detail = err instanceof Error ? err.message : String(err);
    throw new Error(`Transaction submission failed: ${detail}`);
  }

  return {
    txHash: submittedHash || result.txHash,
    policyId: result.policyId,
    assetName: result.assetName,
    fee: result.fee,
  };
}

/**
 * Wait for a transaction to appear on chain.
 */
export async function waitForNFTConfirmation(
  txHash: string,
  maxAttempts = 30,
  delayMs = 10_000,
): Promise<{ confirmed: boolean; blockHash?: string; blockNumber?: number; slot?: number }> {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const tx = await getTransaction(txHash);
      if (tx) {
        return {
          confirmed: true,
          blockHash: tx.block,
          blockNumber: tx.block_height,
          slot: tx.slot,
        };
      }
    } catch {
      // Ignore — keep polling
    }
    await new Promise(r => setTimeout(r, delayMs + require('crypto').randomInt(0, 2000)));
  }
  return { confirmed: false };
}
