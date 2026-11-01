/**
 * =============================================================================
 * NFT CERTIFICATE API ROUTES
 * =============================================================================
 * REST API endpoints for NFT certificate minting and management
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { nftMintingService } from '../services/minting.service';
import { readerIdentity, selectReadableCertificates } from '../services/nftReadGate';
import { StorageTier, PrivacyLevel, STORAGE_TIER_CONFIGS, PRIVACY_CONFIGS } from '../types';
import { blockchainVerifier } from '../services/blockchain-verifier.service';
import { ipfsService } from '../services/ipfs.service';
import { costEstimatorService } from '../services/cost-estimator.service';
import { metadataBuilderService } from '../services/metadata-builder.service';
import { logger } from '../utils/logger';
// KS-1850: the shared platform-role predicate gates PUT /admin/platform-fee below.
import { isPlatformRole } from '@secuura/shared';
import { mintFailureHttpStatus, mintFailureEnvelopeCode } from '../utils/mintError';

const router = Router();

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

const MintNFTSchema = z.object({
  certificationId: z.string().uuid(),
  walletAddress: z.string().min(10),
  chain: z.enum(['cardano', 'ethereum', 'polygon']),
  storageTier: z.nativeEnum(StorageTier),
  privacyLevel: z.nativeEnum(PrivacyLevel),
  customPublicFields: z.array(z.string()).optional(),
  customMetadata: z.record(z.unknown()).optional(),
});

const EstimateCostSchema = z.object({
  storageTier: z.nativeEnum(StorageTier),
  chain: z.enum(['cardano', 'ethereum', 'polygon']),
  metadataSize: z.number().int().positive().optional(),
  documentSize: z.number().int().positive().optional(),
});

const RecordMintSchema = z.object({
  certificationId: z.string().min(1),
  txHash: z.string().regex(/^[0-9a-fA-F]{64}$/, 'Must be a 64-character hex string'),
  policyId: z.string().min(1),
  assetName: z.string().min(1),
  assetId: z.string().min(1),
  walletAddress: z.string().min(10),
  metadata: z.record(z.unknown()).optional(),
  storageTier: z.nativeEnum(StorageTier).optional(),
  privacyLevel: z.nativeEnum(PrivacyLevel).optional(),
});

// =============================================================================
// ROUTES
// =============================================================================

/**
 * POST /api/nft/mint
 * Mint an NFT certificate
 */
router.post('/mint', async (req: Request, res: Response): Promise<void> => {
  try {
    const validationResult = MintNFTSchema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors },
      });
      return;
    }

    const request = validationResult.data;

    // In production, get document data from certification service if Premium tier
    const mintRequest = {
      ...request,
      documentData: undefined, // Would be fetched from certification
      documentMimeType: undefined,
    };

    const result = await nftMintingService.mintNFT(mintRequest);

    if (result.success) {
      res.status(201).json({
        success: true,
        data: {
          nftCertificateId: result.nftCertificateId,
          transactionHash: result.transactionHash,
          policyId: result.policyId,
          assetName: result.assetName,
          assetId: result.assetId,
          ipfsCid: result.ipfsCid,
          costs: result.costs,
        },
      });
    } else {
      // KS-444 (KS-445 precedent): answer each mint-failure class with its
      // honest status — a missing certification is a 404 and an unavailable
      // chain/IPFS dependency is a 503; only genuine client faults (e.g. a
      // wallet address that passes min-length but is not valid bech32) stay 400.
      const status = mintFailureHttpStatus(result.errorCode);
      res.status(status).json({
        success: false,
        error: {
          code: mintFailureEnvelopeCode(status),
          message: result.error,
          errorCode: result.errorCode,
        },
      });
    }
  } catch (error) {
    logger.error('Error minting NFT', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to mint NFT certificate' },
    });
  }
});

/**
 * POST /api/nft/record
 * Record a client-side minting result.
 * The frontend mints via CIP-30 wallet (e.g. Lace) and then calls this
 * endpoint so the backend can verify the transaction on-chain and persist
 * the NFT certificate record.
 */
router.post('/record', async (req: Request, res: Response): Promise<void> => {
  try {
    const validationResult = RecordMintSchema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors },
      });
      return;
    }

    const data = validationResult.data;

    // Verify the transaction exists on-chain via Blockfrost
    const verification = await blockchainVerifier.verifyTransaction(data.txHash);

    // Store the record even if on-chain verification is pending
    const record = await nftMintingService.recordClientMint({
      certificationId: data.certificationId,
      txHash: data.txHash,
      policyId: data.policyId,
      assetName: data.assetName,
      assetId: data.assetId,
      walletAddress: data.walletAddress,
      metadata: data.metadata,
      storageTier: data.storageTier,
      privacyLevel: data.privacyLevel,
      onChainVerified: verification.verified,
      onChainStatus: verification.status,
    });

    res.status(201).json({
      success: true,
      data: {
        nftCertificateId: record.id,
        txHash: record.transactionHash,
        policyId: record.policyId,
        assetName: record.assetName,
        assetId: record.assetId,
        onChainVerified: verification.verified,
        onChainStatus: verification.status,
      },
    });
  } catch (error) {
    logger.error('Error recording NFT mint', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to record NFT mint' },
    });
  }
});

/**
 * POST /api/nft/estimate
 * Estimate minting cost
 */
router.post('/estimate', async (req: Request, res: Response): Promise<void> => {
  try {
    const validationResult = EstimateCostSchema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors },
      });
      return;
    }

    const { storageTier, chain, metadataSize, documentSize } = validationResult.data;

    const estimate = nftMintingService.estimateCost(
      storageTier,
      chain,
      metadataSize,
      documentSize
    );

    res.json({
      success: true,
      data: {
        estimate,
        tier: STORAGE_TIER_CONFIGS[storageTier],
      },
    });
  } catch (error) {
    logger.error('Error estimating cost', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to estimate cost' },
    });
  }
});

/**
 * GET /api/nft/certificates
 * List user's NFT certificates
 */
router.get('/certificates', async (req: Request, res: Response): Promise<void> => {
  try {
    // KS-1836 (services/nftReadGate.ts): the owner is the verified caller, never
    // the query string, and the selectors can only narrow the caller's own rows.
    // An empty selector counts as absent; a non-string one matches nothing.
    const ownerId = readerIdentity((req as any).user);
    if (ownerId === null) {
      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'A verified caller identity is required' } });
      return;
    }
    const walletAddress = req.query.walletAddress === '' ? undefined : req.query.walletAddress;
    const userIdSelector = req.query.userId === '' ? undefined : req.query.userId;

    const fetched = typeof walletAddress === 'string'
      ? await nftMintingService.getWalletNFTCertificates(walletAddress)
      : await nftMintingService.getUserNFTCertificates(ownerId);
    const certificates = selectReadableCertificates(fetched, ownerId, { walletAddress, userId: userIdSelector });

    const withheld = fetched.length - certificates.length;
    if (withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {
      logger.warn('NFT certificate list narrowed to the caller', {
        ownerId, walletAddress, userIdSelector, returned: certificates.length, withheld,
      });
    }

    res.json({
      success: true,
      data: {
        certificates,
        count: certificates.length,
      },
    });
  } catch (error) {
    logger.error('Error fetching certificates', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch NFT certificates' },
    });
  }
});

/**
 * GET /api/nft/certificates/:id
 * Get NFT certificate details
 */
router.get('/certificates/:id', async (req: Request, res: Response): Promise<void> => {
  try {
    const { id } = req.params;

    const certificate = await nftMintingService.getNFTCertificate(id);

    if (!certificate) {
      res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'NFT certificate not found' },
      });
      return;
    }

    res.json({
      success: true,
      data: certificate,
    });
  } catch (error) {
    logger.error('Error fetching certificate', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch NFT certificate' },
    });
  }
});

/**
 * GET /api/nft/tiers
 * Get available storage tiers and their features
 */
router.get('/tiers', async (_req: Request, res: Response): Promise<void> => {
  try {
    const tiers = Object.values(STORAGE_TIER_CONFIGS).map(tier => ({
      ...tier,
      quickEstimates: {
        cardano: nftMintingService.getQuickEstimate(tier.tier, 'cardano'),
        ethereum: nftMintingService.getQuickEstimate(tier.tier, 'ethereum'),
        polygon: nftMintingService.getQuickEstimate(tier.tier, 'polygon'),
      },
    }));

    res.json({
      success: true,
      data: tiers,
    });
  } catch (error) {
    logger.error('Error fetching tiers', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch storage tiers' },
    });
  }
});

/**
 * GET /api/nft/privacy-options
 * Get available privacy options
 */
router.get('/privacy-options', async (_req: Request, res: Response): Promise<void> => {
  try {
    const options = Object.values(PRIVACY_CONFIGS);

    res.json({
      success: true,
      data: options,
    });
  } catch (error) {
    logger.error('Error fetching privacy options', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch privacy options' },
    });
  }
});

/**
 * GET /api/nft/supported-chains
 * Get supported blockchain chains
 */
router.get('/supported-chains', async (_req: Request, res: Response): Promise<void> => {
  try {
    const chains = [
      {
        id: 'cardano',
        name: 'Cardano',
        symbol: 'ADA',
        enabled: true,
        testnet: 'preview',
        wallets: ['eternl', 'nami', 'flint', 'lace', 'yoroi', 'gerowallet', 'nufi', 'typhon'],
      },
      {
        id: 'ethereum',
        name: 'Ethereum',
        symbol: 'ETH',
        enabled: false, // Coming soon
        testnet: 'sepolia',
        wallets: ['metamask', 'walletconnect', 'rainbow', 'coinbase'],
      },
      {
        id: 'polygon',
        name: 'Polygon',
        symbol: 'MATIC',
        enabled: false, // Coming soon
        testnet: 'mumbai',
        wallets: ['metamask', 'walletconnect', 'rainbow', 'coinbase'],
      },
    ];

    res.json({
      success: true,
      data: chains,
    });
  } catch (error) {
    logger.error('Error fetching supported chains', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch supported chains' },
    });
  }
});

// =============================================================================
// BLOCKCHAIN VERIFICATION ROUTES
// =============================================================================

/**
 * POST /api/nft/verify/transaction
 * Verify a minting transaction on-chain
 */
router.post('/verify/transaction', async (req: Request, res: Response): Promise<void> => {
  try {
    const schema = z.object({
      txHash: z.string().regex(/^[0-9a-fA-F]{64}$/, 'Must be a 64-character hex string'),
    });

    const validationResult = schema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors },
      });
      return;
    }

    const verification = await blockchainVerifier.verifyTransaction(validationResult.data.txHash);

    res.json({
      success: true,
      data: verification,
    });
  } catch (error) {
    logger.error('Error verifying transaction', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to verify transaction' },
    });
  }
});

/**
 * POST /api/nft/verify/asset
 * Verify an NFT asset exists on-chain
 */
router.post('/verify/asset', async (req: Request, res: Response): Promise<void> => {
  try {
    const schema = z.object({
      policyId: z.string().min(1),
      assetNameHex: z.string().min(1),
    });

    const validationResult = schema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors },
      });
      return;
    }

    const { policyId, assetNameHex } = validationResult.data;
    const result = await blockchainVerifier.verifyAsset(policyId, assetNameHex);

    res.json({
      success: true,
      data: result,
    });
  } catch (error) {
    logger.error('Error verifying asset', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to verify asset' },
    });
  }
});

// =============================================================================
// IPFS ROUTES
// =============================================================================

/**
 * POST /api/nft/ipfs/upload
 * Upload encrypted data to IPFS
 */
router.post('/ipfs/upload', async (req: Request, res: Response): Promise<void> => {
  try {
    const schema = z.object({
      data: z.string().min(1, 'Base64-encoded data required'),
      filename: z.string().min(1),
      originalMimeType: z.string().min(1),
      encryptionMethod: z.string().default('AES-256-GCM'),
    });

    const validationResult = schema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors },
      });
      return;
    }

    const { data, filename, originalMimeType, encryptionMethod } = validationResult.data;
    const encryptedData = Buffer.from(data, 'base64');

    const result = await ipfsService.uploadEncrypted(encryptedData, {
      filename,
      originalMimeType,
      encryptionMethod,
    });

    if (result.success) {
      res.status(201).json({
        success: true,
        data: {
          cid: result.cid,
          size: result.size,
          pinned: result.pinned,
          gatewayUrl: result.cid ? ipfsService.getGatewayUrl(result.cid) : undefined,
        },
      });
    } else {
      res.status(500).json({
        success: false,
        error: { code: 'INTERNAL_ERROR', message: result.error || 'IPFS upload failed' },
      });
    }
  } catch (error) {
    logger.error('Error uploading to IPFS', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to upload to IPFS' },
    });
  }
});

/**
 * POST /api/nft/ipfs/pin
 * Pin a CID to ensure it stays available
 */
router.post('/ipfs/pin', async (req: Request, res: Response): Promise<void> => {
  try {
    const schema = z.object({ cid: z.string().min(1) });
    const validationResult = schema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors } });
      return;
    }

    const pinned = await ipfsService.pin(validationResult.data.cid);

    res.json({
      success: true,
      data: { cid: validationResult.data.cid, pinned },
    });
  } catch (error) {
    logger.error('Error pinning CID', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to pin CID' } });
  }
});

/**
 * POST /api/nft/ipfs/unpin
 * Unpin a CID to allow garbage collection
 */
router.post('/ipfs/unpin', async (req: Request, res: Response): Promise<void> => {
  try {
    const schema = z.object({ cid: z.string().min(1) });
    const validationResult = schema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors } });
      return;
    }

    const unpinned = await ipfsService.unpin(validationResult.data.cid);

    res.json({
      success: true,
      data: { cid: validationResult.data.cid, unpinned },
    });
  } catch (error) {
    logger.error('Error unpinning CID', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to unpin CID' } });
  }
});

/**
 * GET /api/nft/ipfs/:cid
 * Fetch content from IPFS by CID
 */
router.get('/ipfs/:cid', async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const data = await ipfsService.fetch(req.params.cid);

    res.json({
      success: true,
      data: {
        cid: req.params.cid,
        content: data.toString('base64'),
        size: data.length,
        gatewayUrl: ipfsService.getGatewayUrl(req.params.cid),
      },
    });
  } catch (error) {
    // KS-118: an unknown cid is a 404 and an unreachable gateway is a 503.
    // Forward the typed error to the shared errorHandler instead of
    // flattening every IPFS failure into a 500.
    next(error);
  }
});

/**
 * GET /api/nft/ipfs/:cid/encrypted
 * Fetch encrypted content from IPFS and parse the encrypted package
 */
router.get('/ipfs/:cid/encrypted', async (req: Request, res: Response, next: NextFunction): Promise<void> => {
  try {
    const result = await ipfsService.fetchEncrypted(req.params.cid);

    res.json({
      success: true,
      data: {
        cid: req.params.cid,
        encryptedData: result.encryptedData.toString('base64'),
        metadata: result.metadata,
        size: result.encryptedData.length,
      },
    });
  } catch (error) {
    // KS-118: same as GET /ipfs/:cid — a missing cid is a 404, an
    // unreachable gateway is a 503. Let the shared errorHandler map it.
    next(error);
  }
});

/**
 * GET /api/nft/ipfs/provider/info
 * Get current IPFS provider information
 */
router.get('/ipfs/provider/info', async (_req: Request, res: Response): Promise<void> => {
  res.json({
    success: true,
    data: {
      provider: ipfsService.getProviderName(),
    },
  });
});

// =============================================================================
// METADATA & COST ADMIN ROUTES
// =============================================================================

/**
 * POST /api/nft/metadata/estimate-size
 * Estimate metadata size in bytes for a given configuration
 */
router.post('/metadata/estimate-size', async (req: Request, res: Response): Promise<void> => {
  try {
    const schema = z.object({
      certificationId: z.string().default('00000000-0000-0000-0000-000000000000'),
      documentHash: z.string().default('placeholder-hash'),
      documentType: z.string().default('certificate'),
      issuerName: z.string().default('Test Issuer'),
      issuedDate: z.string().default(new Date().toISOString()),
      storageTier: z.nativeEnum(StorageTier),
      privacyLevel: z.nativeEnum(PrivacyLevel),
      customPublicFields: z.array(z.string()).optional(),
    });

    const validationResult = schema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors } });
      return;
    }

    const { storageTier, privacyLevel, customPublicFields, ...certData } = validationResult.data;

    const metadata = metadataBuilderService.buildMetadata(
      {
        id: certData.certificationId,
        documentHash: certData.documentHash,
        documentType: certData.documentType,
        issuer: { name: certData.issuerName },
        issuedDate: certData.issuedDate,
      },
      { storageTier, privacyLevel, customPublicFields }
    );

    const sizeBytes = metadataBuilderService.estimateMetadataSize(metadata);

    res.json({
      success: true,
      data: {
        sizeBytes,
        sizeKB: (sizeBytes / 1024).toFixed(2),
        metadata,
      },
    });
  } catch (error) {
    logger.error('Error estimating metadata size', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to estimate metadata size' } });
  }
});

/**
 * PUT /api/nft/admin/platform-fee
 * Update platform fee configuration (admin only)
 */
router.put('/admin/platform-fee', async (req: Request, res: Response): Promise<void> => {
  try {
    // Admin only — verify role from gateway auth.
    // Pen-test F-04: read role ONLY from authenticated req.user (set by
    // authenticate() middleware) — fallback to raw headers was spoofable.
    // KS-1850: platform administrators only (the shared isPlatformRole: SYSTEM_ADMIN / SUPER_ADMIN, ASCII case
    // fold only). Before, the list was ['SYSTEM_ADMIN', 'ORG_ADMIN', 'OWNER']: OWNER is every self-registered
    // user, and the fee is platform-wide, not a tenant setting. The 403 body is unchanged, and it is answered
    // before the body is validated or the fee is changed.
    if (!isPlatformRole((req as any).user?.role)) {
      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } });
      return;
    }

    const schema = z.object({
      percentage: z.number().min(0).max(100),
      fixed: z.number().min(0),
    });

    const validationResult = schema.safeParse(req.body);
    if (!validationResult.success) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation error', details: validationResult.error.errors } });
      return;
    }

    const { percentage, fixed } = validationResult.data;
    costEstimatorService.updatePlatformFee(percentage, fixed);

    res.json({
      success: true,
      data: {
        platformFeePercentage: percentage,
        platformFeeFixed: fixed,
        message: 'Platform fee updated',
      },
    });
  } catch (error) {
    logger.error('Error updating platform fee', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update platform fee' } });
  }
});

export default router;
