/**
 * =============================================================================
 * NFT MINTING SERVICE
 * =============================================================================
 * Orchestrates the complete NFT certificate minting process
 */

import { v4 as uuidv4 } from 'uuid';
import {
  StorageTier,
  PrivacyLevel,
  MintNFTRequest,
  MintNFTResponse,
  NFTCertificate,
  NFTStatus,
  CostBreakdown,
} from '../types';
import { metadataBuilderService, CertificationData } from './metadata-builder.service';
import { encryptionService } from './encryption.service';
import { ipfsService } from './ipfs.service';
import { costEstimatorService } from './cost-estimator.service';
import { query, isDbAvailable } from '../db';
import {
  isCardanoNFTReady,
  mintNFTOnChain,
  getPolicyId,
  waitForNFTConfirmation,
} from '../cardano';
import { logger } from '../utils/logger';
import { classifyMintError } from '../utils/mintError';

// =============================================================================
// IN-MEMORY STORAGE (with database persistence fallback)
// =============================================================================

const memNftCertificates = new Map<string, NFTCertificate>();
const certificationCache = new Map<string, CertificationData>();

// Database persistence helper
async function dbSaveNFTCertificate(cert: NFTCertificate): Promise<void> {
  memNftCertificates.set(cert.id, cert);
  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_nft_certificates (
        id, certification_id, user_id, chain, wallet_address, policy_id, asset_name, asset_id,
        transaction_hash, storage_tier, privacy_level, public_fields, status, ipfs_cid,
        encrypted_key, minting_cost, platform_fee, total_cost, error_message, created_at, updated_at, minted_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22)
      ON CONFLICT (id) DO UPDATE SET
        status = EXCLUDED.status,
        transaction_hash = EXCLUDED.transaction_hash,
        policy_id = EXCLUDED.policy_id,
        asset_name = EXCLUDED.asset_name,
        asset_id = EXCLUDED.asset_id,
        ipfs_cid = EXCLUDED.ipfs_cid,
        encrypted_key = EXCLUDED.encrypted_key,
        minting_cost = EXCLUDED.minting_cost,
        platform_fee = EXCLUDED.platform_fee,
        total_cost = EXCLUDED.total_cost,
        error_message = EXCLUDED.error_message,
        updated_at = EXCLUDED.updated_at,
        minted_at = EXCLUDED.minted_at`,
      [
        cert.id,
        cert.certificationId,
        cert.userId,
        cert.chain,
        cert.walletAddress,
        cert.policyId || null,
        cert.assetName || null,
        cert.assetId || null,
        cert.transactionHash || null,
        cert.storageTier,
        cert.privacyLevel,
        JSON.stringify(cert.publicFields || []),
        cert.status,
        cert.ipfsCid || null,
        cert.encryptedKey || null,
        cert.mintingCost || null,
        cert.platformFee || null,
        cert.totalCost || null,
        cert.errorMessage || null,
        cert.createdAt,
        cert.updatedAt,
        cert.mintedAt || null,
      ]
    );
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB save certificate failed', { error: reason });
  }
}

// =============================================================================
// STARTUP LOADING
// =============================================================================

export async function loadFromDb(): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    const result = await query<{
      id: string; certification_id: string; user_id: string; chain: string;
      wallet_address: string; policy_id: string | null; asset_name: string | null;
      asset_id: string | null; transaction_hash: string | null; storage_tier: string;
      privacy_level: string; public_fields: string; status: string;
      ipfs_cid: string | null; encrypted_key: string | null;
      minting_cost: number | null; platform_fee: number | null; total_cost: number | null;
      error_message: string | null; created_at: Date; updated_at: Date; minted_at: Date | null;
    }>('SELECT * FROM svc_nft_certificates');
    for (const row of result.rows) {
      memNftCertificates.set(row.id, {
        id: row.id, certificationId: row.certification_id, userId: row.user_id,
        chain: row.chain as 'cardano' | 'ethereum' | 'polygon', walletAddress: row.wallet_address,
        policyId: row.policy_id || undefined, assetName: row.asset_name || undefined,
        assetId: row.asset_id || undefined, transactionHash: row.transaction_hash || undefined,
        storageTier: row.storage_tier as StorageTier, privacyLevel: row.privacy_level as PrivacyLevel,
        publicFields: JSON.parse(row.public_fields || '[]'), status: row.status as NFTStatus,
        ipfsCid: row.ipfs_cid || undefined, encryptedKey: row.encrypted_key || undefined,
        mintingCost: row.minting_cost != null ? String(row.minting_cost) : undefined,
        platformFee: row.platform_fee != null ? String(row.platform_fee) : undefined,
        totalCost: row.total_cost != null ? String(row.total_cost) : undefined,
        errorMessage: row.error_message || undefined,
        createdAt: new Date(row.created_at), updatedAt: new Date(row.updated_at),
        mintedAt: row.minted_at ? new Date(row.minted_at) : undefined,
      });
    }
    logger.info('Loaded NFT certificates from DB', { count: memNftCertificates.size });
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('Failed to load NFT certificates from DB — starting empty', { error: reason });
  }
}

// =============================================================================
// CERTIFICATION DATA SERVICE
// =============================================================================

const ORIGINATE_SERVICE_URL = process.env.ORIGINATE_SERVICE_URL || 'http://localhost:4004';

async function getCertificationData(certificationId: string): Promise<CertificationData | null> {
  // Check cache first
  if (certificationCache.has(certificationId)) {
    return certificationCache.get(certificationId)!;
  }

  // In production, fetch from originate service — no mock fallback
  if (process.env.NODE_ENV === 'production') {
    try {
      const resp = await fetch(`${ORIGINATE_SERVICE_URL}/api/certifications/${certificationId}`);
      if (!resp.ok) {
        logger.error('Failed to fetch certification from originate service', {
          certificationId,
          status: resp.status,
        });
        return null;
      }
      const body = await resp.json() as { data?: CertificationData };
      const data = body.data || body as unknown as CertificationData;
      if (data) {
        certificationCache.set(certificationId, data);
      }
      return data || null;
    } catch (err: any) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('Error fetching certification data from originate service', {
        certificationId,
        error: reason,
      });
      return null;
    }
  }

  // Try originate service first even in dev, fall back to mock
  try {
    const resp = await fetch(`${ORIGINATE_SERVICE_URL}/api/certifications/${certificationId}`);
    if (resp.ok) {
      const body = await resp.json() as { data?: CertificationData };
      const data = body.data || body as unknown as CertificationData;
      if (data) {
        certificationCache.set(certificationId, data);
        return data;
      }
    }
  } catch {
    // Originate service not available — use mock in development
  }

  // Development/test mock fallback
  logger.warn('Using mock certification data — originate service not reachable. DO NOT USE IN PRODUCTION.');
  const mockData: CertificationData = {
    id: certificationId,
    documentHash: `sha256:${Buffer.from(certificationId).toString('hex').slice(0, 64)}`,
    documentType: 'Certificate',
    documentTitle: 'Professional Certification',
    issuer: {
      name: 'Secuura Demo Issuer',
      did: 'did:prism:demo123',
    },
    recipient: {
      name: 'Demo Recipient',
    },
    issuedDate: new Date().toISOString(),
    verificationUrl: `https://verify.secuura.io/${certificationId}`,
  };

  certificationCache.set(certificationId, mockData);
  return mockData;
}

// =============================================================================
// NFT MINTING SERVICE
// =============================================================================

export class NFTMintingService {
  /**
   * Mint an NFT certificate
   */
  async mintNFT(request: MintNFTRequest): Promise<MintNFTResponse> {
    const nftId = uuidv4();

    try {
      // Create initial record
      const nftRecord: NFTCertificate = {
        id: nftId,
        certificationId: request.certificationId,
        userId: 'user-id', // Would come from auth context
        chain: request.chain,
        walletAddress: request.walletAddress,
        storageTier: request.storageTier,
        privacyLevel: request.privacyLevel,
        publicFields: request.customPublicFields || [],
        status: NFTStatus.PENDING,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      await dbSaveNFTCertificate(nftRecord);

      // Get certification data
      const certification = await getCertificationData(request.certificationId);
      if (!certification) {
        throw new Error('Certification not found');
      }

      // Update status
      await this.updateStatus(nftId, NFTStatus.PROCESSING);

      // Handle IPFS upload for Premium tier
      let ipfsCid: string | undefined;
      let encryptedKey: string | undefined;

      if (request.storageTier === StorageTier.PREMIUM && request.documentData) {
        await this.updateStatus(nftId, NFTStatus.UPLOADING_IPFS);

        const walletSignature = request.walletSignature;
        if (!walletSignature) {
          if (process.env.NODE_ENV === 'production' || process.env.NODE_ENV === 'staging') {
            throw new Error('Wallet signature is required for PREMIUM storage tier encryption');
          }
          logger.warn('No wallet signature provided — using dev fallback. DO NOT USE IN PRODUCTION.');
        }
        const encryptResult = encryptionService.encryptWithWalletKey(
          request.documentData,
          walletSignature || (process.env.NODE_ENV === 'production'
            ? (() => { throw new Error('Wallet signature required in production'); })()
            : `dev-sig-${request.walletAddress}`)
        );

        // Upload to IPFS
        const uploadResult = await ipfsService.uploadEncrypted(
          encryptResult.encryptedData,
          {
            filename: `cert-${certification.id}`,
            originalMimeType: request.documentMimeType || 'application/pdf',
            encryptionMethod: 'AES-256-GCM',
          }
        );

        if (!uploadResult.success) {
          throw new Error(`IPFS upload failed: ${uploadResult.error}`);
        }

        ipfsCid = uploadResult.cid;
        encryptedKey = JSON.stringify({
          iv: encryptResult.iv,
          authTag: encryptResult.authTag,
          keySalt: encryptResult.keySalt,
        });

        // Update record
        nftRecord.ipfsCid = ipfsCid;
        nftRecord.encryptedKey = encryptedKey;
        await dbSaveNFTCertificate(nftRecord);
      }

      // Build metadata
      const metadata = metadataBuilderService.buildMetadata(certification, {
        storageTier: request.storageTier,
        privacyLevel: request.privacyLevel,
        customPublicFields: request.customPublicFields,
        ipfsCid,
        encryptedKey,
      });

      // Generate asset name
      const assetName = metadataBuilderService.generateAssetName(certification.id);

      // Estimate costs
      const metadataSize = metadataBuilderService.estimateMetadataSize(metadata);
      const costs = costEstimatorService.estimateCost({
        storageTier: request.storageTier,
        chain: request.chain,
        metadataSize,
        documentSize: request.documentData?.length,
      });

      // Update status to minting
      await this.updateStatus(nftId, NFTStatus.MINTING);

      // Perform minting based on chain
      let transactionHash: string;
      let policyId: string;

      if (request.chain === 'cardano') {
        const mintResult = await this.mintOnCardano(
          request.walletAddress,
          metadata,
          assetName
        );
        transactionHash = mintResult.txHash;
        policyId = mintResult.policyId;
      } else {
        const mintResult = await this.mintOnEVM(
          request.chain,
          request.walletAddress,
          metadata
        );
        transactionHash = mintResult.txHash;
        policyId = mintResult.contractAddress;
      }

      // Update record with success
      nftRecord.transactionHash = transactionHash;
      nftRecord.policyId = policyId;
      nftRecord.assetName = assetName;
      nftRecord.assetId = `${policyId}.${assetName}`;
      nftRecord.mintingCost = costs.subtotal;
      nftRecord.platformFee = costs.platformFee;
      nftRecord.totalCost = costs.total;
      nftRecord.status = NFTStatus.MINTED;
      nftRecord.mintedAt = new Date();
      nftRecord.updatedAt = new Date();
      await dbSaveNFTCertificate(nftRecord);

      return {
        success: true,
        transactionHash,
        policyId,
        assetName,
        assetId: nftRecord.assetId,
        nftCertificateId: nftId,
        metadata,
        ipfsCid,
        costs,
      };
    } catch (error) {
      // KS-444: the Cardano SDK throws plain strings (bech32 parse errors),
      // so (error as Error).message could be undefined and the failure body
      // lost its message entirely. Normalise + classify the failure so the
      // route can answer with an honest status (404/503/400).
      const { message, errorCode } = classifyMintError(error);

      // Update record with failure
      const nftRecord = memNftCertificates.get(nftId);
      if (nftRecord) {
        nftRecord.status = NFTStatus.FAILED;
        nftRecord.errorMessage = message;
        nftRecord.updatedAt = new Date();
        await dbSaveNFTCertificate(nftRecord);
      }

      return {
        success: false,
        error: message,
        errorCode,
      };
    }
  }

  /**
   * Record a client-side minting result.
   * The actual minting was done in the browser via MeshSDK + CIP-30 wallet.
   * This method stores the record so the platform can track NFT certificates.
   */
  async recordClientMint(params: {
    certificationId: string;
    txHash: string;
    policyId: string;
    assetName: string;
    assetId: string;
    walletAddress: string;
    metadata?: Record<string, unknown>;
    storageTier?: StorageTier;
    privacyLevel?: PrivacyLevel;
    onChainVerified: boolean;
    onChainStatus: string;
  }): Promise<NFTCertificate> {
    const nftId = uuidv4();

    const record: NFTCertificate = {
      id: nftId,
      certificationId: params.certificationId,
      userId: 'user-id', // Would come from auth context in production
      chain: 'cardano',
      walletAddress: params.walletAddress,
      policyId: params.policyId,
      assetName: params.assetName,
      assetId: params.assetId,
      transactionHash: params.txHash,
      storageTier: params.storageTier ?? StorageTier.STANDARD,
      privacyLevel: params.privacyLevel ?? PrivacyLevel.PARTIAL,
      publicFields: [],
      status: params.onChainVerified ? NFTStatus.MINTED : NFTStatus.PENDING,
      createdAt: new Date(),
      mintedAt: params.onChainVerified ? new Date() : undefined,
      updatedAt: new Date(),
    };

    await dbSaveNFTCertificate(record);
    logger.info('Recorded client mint', {
      nftId,
      txHash: params.txHash,
      tier: record.storageTier,
      onChainStatus: params.onChainStatus,
    });

    return record;
  }

  /**
   * Get NFT certificate by ID
   */
  async getNFTCertificate(nftId: string): Promise<NFTCertificate | null> {
    // Check memory first
    const memCert = memNftCertificates.get(nftId);
    if (memCert) return memCert;
    
    // Try database if available
    if (isDbAvailable()) {
      try {
        const result = await query<{
          id: string;
          certification_id: string;
          user_id: string;
          chain: string;
          wallet_address: string;
          policy_id: string | null;
          asset_name: string | null;
          asset_id: string | null;
          transaction_hash: string | null;
          storage_tier: string;
          privacy_level: string;
          public_fields: string;
          status: string;
          ipfs_cid: string | null;
          encrypted_key: string | null;
          minting_cost: number | null;
          platform_fee: number | null;
          total_cost: number | null;
          error_message: string | null;
          created_at: Date;
          updated_at: Date;
          minted_at: Date | null;
        }>('SELECT * FROM svc_nft_certificates WHERE id = $1', [nftId]);
        
        if (result.rows.length > 0) {
          const row = result.rows[0];
          const cert: NFTCertificate = {
            id: row.id,
            certificationId: row.certification_id,
            userId: row.user_id,
            chain: row.chain as 'cardano' | 'ethereum' | 'polygon',
            walletAddress: row.wallet_address,
            policyId: row.policy_id || undefined,
            assetName: row.asset_name || undefined,
            assetId: row.asset_id || undefined,
            transactionHash: row.transaction_hash || undefined,
            storageTier: row.storage_tier as StorageTier,
            privacyLevel: row.privacy_level as PrivacyLevel,
            publicFields: JSON.parse(row.public_fields || '[]'),
            status: row.status as NFTStatus,
            ipfsCid: row.ipfs_cid || undefined,
            encryptedKey: row.encrypted_key || undefined,
            mintingCost: row.minting_cost != null ? String(row.minting_cost) : undefined,
            platformFee: row.platform_fee != null ? String(row.platform_fee) : undefined,
            totalCost: row.total_cost != null ? String(row.total_cost) : undefined,
            errorMessage: row.error_message || undefined,
            createdAt: row.created_at,
            updatedAt: row.updated_at,
            mintedAt: row.minted_at || undefined,
          };
          // Cache in memory
          memNftCertificates.set(cert.id, cert);
          return cert;
        }
      } catch (err: any) {
        let reason: string;
        try {
          reason = err instanceof Error ? err.message : String(err);
        } catch {
          reason = 'unreadable thrown value';
        }
        logger.error('DB get certificate failed', { error: reason });
      }
    }
    
    return null;
  }

  /**
   * Get all NFT certificates for a user
   */
  async getUserNFTCertificates(userId: string): Promise<NFTCertificate[]> {
    const certificates: NFTCertificate[] = [];
    
    // Check memory first
    for (const cert of memNftCertificates.values()) {
      if (cert.userId === userId) {
        certificates.push(cert);
      }
    }
    
    // Try database if available
    if (isDbAvailable()) {
      try {
        const result = await query<{
          id: string;
          certification_id: string;
          user_id: string;
          chain: string;
          wallet_address: string;
          policy_id: string | null;
          asset_name: string | null;
          asset_id: string | null;
          transaction_hash: string | null;
          storage_tier: string;
          privacy_level: string;
          public_fields: string;
          status: string;
          ipfs_cid: string | null;
          encrypted_key: string | null;
          minting_cost: number | null;
          platform_fee: number | null;
          total_cost: number | null;
          error_message: string | null;
          created_at: Date;
          updated_at: Date;
          minted_at: Date | null;
        }>('SELECT * FROM svc_nft_certificates WHERE user_id = $1 ORDER BY created_at DESC', [userId]);
        
        for (const row of result.rows) {
          // Skip if already in memory
          if (memNftCertificates.has(row.id)) continue;
          
          const cert: NFTCertificate = {
            id: row.id,
            certificationId: row.certification_id,
            userId: row.user_id,
            chain: row.chain as 'cardano' | 'ethereum' | 'polygon',
            walletAddress: row.wallet_address,
            policyId: row.policy_id || undefined,
            assetName: row.asset_name || undefined,
            assetId: row.asset_id || undefined,
            transactionHash: row.transaction_hash || undefined,
            storageTier: row.storage_tier as StorageTier,
            privacyLevel: row.privacy_level as PrivacyLevel,
            publicFields: JSON.parse(row.public_fields || '[]'),
            status: row.status as NFTStatus,
            ipfsCid: row.ipfs_cid || undefined,
            encryptedKey: row.encrypted_key || undefined,
            mintingCost: row.minting_cost != null ? String(row.minting_cost) : undefined,
            platformFee: row.platform_fee != null ? String(row.platform_fee) : undefined,
            totalCost: row.total_cost != null ? String(row.total_cost) : undefined,
            errorMessage: row.error_message || undefined,
            createdAt: row.created_at,
            updatedAt: row.updated_at,
            mintedAt: row.minted_at || undefined,
          };
          certificates.push(cert);
          memNftCertificates.set(cert.id, cert);
        }
      } catch (err: any) {
        let reason: string;
        try {
          reason = err instanceof Error ? err.message : String(err);
        } catch {
          reason = 'unreadable thrown value';
        }
        logger.error('DB get user certificates failed', { error: reason });
      }
    }
    
    return certificates.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  }

  /**
   * Get NFT certificates by wallet address
   */
  async getWalletNFTCertificates(walletAddress: string): Promise<NFTCertificate[]> {
    const certificates: NFTCertificate[] = [];
    
    // Check memory first
    for (const cert of memNftCertificates.values()) {
      if (cert.walletAddress === walletAddress) {
        certificates.push(cert);
      }
    }
    
    // Try database if available
    if (isDbAvailable()) {
      try {
        const result = await query<{
          id: string;
          certification_id: string;
          user_id: string;
          chain: string;
          wallet_address: string;
          policy_id: string | null;
          asset_name: string | null;
          asset_id: string | null;
          transaction_hash: string | null;
          storage_tier: string;
          privacy_level: string;
          public_fields: string;
          status: string;
          ipfs_cid: string | null;
          encrypted_key: string | null;
          minting_cost: number | null;
          platform_fee: number | null;
          total_cost: number | null;
          error_message: string | null;
          created_at: Date;
          updated_at: Date;
          minted_at: Date | null;
        }>('SELECT * FROM svc_nft_certificates WHERE wallet_address = $1 ORDER BY created_at DESC', [walletAddress]);
        
        for (const row of result.rows) {
          // Skip if already in memory
          if (memNftCertificates.has(row.id)) continue;
          
          const cert: NFTCertificate = {
            id: row.id,
            certificationId: row.certification_id,
            userId: row.user_id,
            chain: row.chain as 'cardano' | 'ethereum' | 'polygon',
            walletAddress: row.wallet_address,
            policyId: row.policy_id || undefined,
            assetName: row.asset_name || undefined,
            assetId: row.asset_id || undefined,
            transactionHash: row.transaction_hash || undefined,
            storageTier: row.storage_tier as StorageTier,
            privacyLevel: row.privacy_level as PrivacyLevel,
            publicFields: JSON.parse(row.public_fields || '[]'),
            status: row.status as NFTStatus,
            ipfsCid: row.ipfs_cid || undefined,
            encryptedKey: row.encrypted_key || undefined,
            mintingCost: row.minting_cost != null ? String(row.minting_cost) : undefined,
            platformFee: row.platform_fee != null ? String(row.platform_fee) : undefined,
            totalCost: row.total_cost != null ? String(row.total_cost) : undefined,
            errorMessage: row.error_message || undefined,
            createdAt: row.created_at,
            updatedAt: row.updated_at,
            mintedAt: row.minted_at || undefined,
          };
          certificates.push(cert);
          memNftCertificates.set(cert.id, cert);
        }
      } catch (err: any) {
        let reason: string;
        try {
          reason = err instanceof Error ? err.message : String(err);
        } catch {
          reason = 'unreadable thrown value';
        }
        logger.error('DB get wallet certificates failed', { error: reason });
      }
    }
    
    return certificates.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  }

  /**
   * Estimate minting cost
   */
  estimateCost(
    storageTier: StorageTier,
    chain: 'cardano' | 'ethereum' | 'polygon',
    metadataSize?: number,
    documentSize?: number
  ): CostBreakdown {
    return costEstimatorService.estimateCost({
      storageTier,
      chain,
      metadataSize,
      documentSize,
    });
  }

  /**
   * Get quick cost estimate for UI
   */
  getQuickEstimate(
    tier: StorageTier,
    chain: 'cardano' | 'ethereum' | 'polygon'
  ): string {
    return costEstimatorService.getQuickEstimate(tier, chain);
  }

  // ===========================================================================
  // PRIVATE METHODS
  // ===========================================================================

  private async updateStatus(nftId: string, status: NFTStatus): Promise<void> {
    const record = memNftCertificates.get(nftId);
    if (record) {
      record.status = status;
      record.updatedAt = new Date();
      await dbSaveNFTCertificate(record);
    }
  }

  /**
   * Mint NFT on Cardano.
   * Uses real blockchain transactions when BLOCKFROST_API_KEY and
   * PLATFORM_WALLET_MNEMONIC are configured, otherwise falls back to mock.
   */
  private async mintOnCardano(
    walletAddress: string,
    metadata: ReturnType<typeof metadataBuilderService.buildMetadata>,
    assetName: string
  ): Promise<{ txHash: string; policyId: string }> {

    // ── Real Cardano minting ──────────────────────────────────────────────
    if (isCardanoNFTReady()) {
      try {
        // Build CIP-25 metadata from the platform metadata
        const cip25Metadata: Record<string, unknown> = {
          name: (metadata as any).name || assetName,
          description: (metadata as any).description || 'Secuura NFT Certificate',
          image: (metadata as any).image || ((metadata as any).ipfsCid
            ? `ipfs://${(metadata as any).ipfsCid}`
            : undefined),
          mediaType: 'application/json',
          secuura: {
            version: '1.0',
            certificationId: (metadata as any).certificationId,
            documentHash: (metadata as any).documentHash,
            documentType: (metadata as any).documentType,
            issuer: (metadata as any).issuer,
            issuedDate: (metadata as any).issuedDate,
            verificationUrl: (metadata as any).verificationUrl,
            storageTier: (metadata as any).storageTier,
            privacyLevel: (metadata as any).privacyLevel,
          },
        };

        logger.info('Minting NFT on-chain', {
          recipient: walletAddress,
          asset: assetName,
          policy: getPolicyId(),
        });

        const result = await mintNFTOnChain(walletAddress, assetName, cip25Metadata);

        logger.info('NFT minted successfully', {
          txHash: result.txHash,
          policyId: result.policyId,
          fee: `${result.fee} lovelace`,
        });

        // Fire-and-forget confirmation polling
        waitForNFTConfirmation(result.txHash).then((c) => {
          if (c.confirmed) {
            logger.info('Tx confirmed', { blockNumber: c.blockNumber, slot: c.slot });
          } else {
            logger.warn('Tx not yet confirmed', { txHash: result.txHash });
          }
        }).catch(() => { /* ignore */ });

        return {
          txHash: result.txHash,
          policyId: result.policyId,
        };
      } catch (err: any) {
        logger.error('Real minting failed', { error: err instanceof Error ? err.message : String(err) });
        throw err; // Propagate — let caller handle the failure
      }
    }

    // ── Mock mode ─────────────────────────────────────────────────────────
    const mockPolicyId = Buffer.from(uuidv4().replace(/-/g, '').slice(0, 56)).toString('hex').slice(0, 56);
    const mockTxHash = Buffer.from(uuidv4() + uuidv4()).toString('hex').slice(0, 64);

    await new Promise(resolve => setTimeout(resolve, 2000));

    logger.info('Minting Cardano NFT (MOCK)', {
      wallet: walletAddress,
      policyId: mockPolicyId,
      assetName,
      txHash: mockTxHash,
    });

    return {
      txHash: mockTxHash,
      policyId: mockPolicyId,
    };
  }

  /**
   * Mint NFT on EVM chain
   * In production, this would use ethers.js or similar
   */
  private async mintOnEVM(
    chain: string,
    walletAddress: string,
    _metadata: ReturnType<typeof metadataBuilderService.buildMetadata>
  ): Promise<{ txHash: string; contractAddress: string }> {
    // Mock implementation
    // In production:
    // 1. Connect to NFT contract
    // 2. Build mint transaction
    // 3. Sign with WalletConnect
    // 4. Wait for confirmation
    
    const mockContractAddress = `0x${Buffer.from(uuidv4()).toString('hex').slice(0, 40)}`;
    const mockTxHash = `0x${Buffer.from(uuidv4() + uuidv4()).toString('hex').slice(0, 64)}`;

    // Simulate transaction time
    await new Promise(resolve => setTimeout(resolve, 3000));

    logger.info('Minting EVM NFT (MOCK)', {
      chain,
      wallet: walletAddress,
      contract: mockContractAddress,
      txHash: mockTxHash,
    });

    return {
      txHash: mockTxHash,
      contractAddress: mockContractAddress,
    };
  }
}

// =============================================================================
// SINGLETON EXPORT
// =============================================================================

export const nftMintingService = new NFTMintingService();
