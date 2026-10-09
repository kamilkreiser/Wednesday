/**
 * Identity Credential Routes
 *
 * Issues W3C Verifiable Credentials that attest to a user's identity
 * assurance level within the Secuura 7-tier model.
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { logger } from '../utils/logger';
import { AppError } from '../middleware/errorHandler';

const router = Router();

const IDENTITY_CREDENTIAL_CONTEXT = 'https://schemas.secuura.io/identity/v1';

const CREDENTIAL_TYPES: Record<string, string> = {
  NONE: 'SecuuraIdentityAssuranceCredential',
  BASIC: 'SecuuraIdentityAssuranceCredential',
  SOCIAL: 'SecuuraSocialIdentityCredential',
  STANDARD: 'SecuuraIdentityAssuranceCredential',
  ENHANCED: 'SecuuraIdentityAssuranceCredential',
  HIGH: 'SecuuraKycVerificationCredential',
  GOVERNMENT: 'SecuuraGovernmentIdentityCredential',
};

const IssueIdentityCredentialSchema = z.object({
  subjectDid: z.string().min(1),
  assuranceLevel: z.enum(['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT']),
  verificationMethods: z.array(z.string()).optional().default([]),
  provider: z.string().optional(),
  region: z.string().optional(),
  expirationDate: z.string().optional(),
  metadata: z.record(z.unknown()).optional(),
});

/**
 * Issue an identity assurance credential
 * POST /api/identity-credentials/issue
 */
router.post('/issue', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const body = IssueIdentityCredentialSchema.parse(req.body);

    const issuerDid = process.env.ISSUER_DID || 'did:prism:secuura-platform-issuer';
    const now = new Date().toISOString();
    const credType = CREDENTIAL_TYPES[body.assuranceLevel] || 'SecuuraIdentityAssuranceCredential';

    const credential = {
      '@context': [
        'https://www.w3.org/2018/credentials/v1',
        IDENTITY_CREDENTIAL_CONTEXT,
      ],
      id: `urn:uuid:${crypto.randomUUID()}`,
      type: ['VerifiableCredential', credType],
      issuer: issuerDid,
      issuanceDate: now,
      ...(body.expirationDate ? { expirationDate: body.expirationDate } : {}),
      credentialSubject: {
        id: body.subjectDid,
        assuranceLevel: body.assuranceLevel,
        verificationMethods: body.verificationMethods,
        verifiedAt: now,
        ...(body.provider ? { provider: body.provider } : {}),
        ...(body.region ? { region: body.region } : {}),
        ...(body.metadata || {}),
      },
      credentialStatus: {
        id: `${process.env.VC_STATUS_URL || 'https://vc.secuura.io'}/status/${crypto.randomUUID()}`,
        type: 'CredentialStatusList2021Entry',
      },
    };

    logger.info('Identity credential issued', {
      subjectDid: body.subjectDid,
      assuranceLevel: body.assuranceLevel,
      credentialType: credType,
    });

    res.status(201).json({
      credential,
      message: `Identity credential issued at ${body.assuranceLevel} assurance level`,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return next(new AppError(`Validation error: ${error.errors.map(e => e.message).join(', ')}`, 400));
    }
    next(error);
  }
});

/**
 * List supported identity credential types
 * GET /api/identity-credentials/types
 */
router.get('/types', (_req: Request, res: Response) => {
  res.json({
    types: Object.entries(CREDENTIAL_TYPES).map(([level, type]) => ({
      assuranceLevel: level,
      credentialType: type,
    })),
    context: IDENTITY_CREDENTIAL_CONTEXT,
  });
});

export { router as identityCredentialRoutes };
