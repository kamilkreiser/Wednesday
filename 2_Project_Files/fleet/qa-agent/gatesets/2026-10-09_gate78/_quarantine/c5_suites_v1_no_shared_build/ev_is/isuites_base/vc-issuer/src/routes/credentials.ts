/**
 * =============================================================================
 * CREDENTIAL ROUTES
 * =============================================================================
 * W3C Verifiable Credential issuance, retrieval, and verification
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import {
  createVCBuilder,
  SecuuraCredentialType,
  VerificationLevel,
  SecuuraCredential,
  VCIssuer,
  signCredential,
  verifyCredential,
  CredentialIssuanceRequest,
} from '@secuura/shared/vc';
import { logger } from '../utils/logger';
import { AppError } from '../middleware/errorHandler';
import * as credentialRepo from '../repositories/credentialRepo';
import { revocationVerifierConfig } from '../services/revocationResolvers';

const router = Router();

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

export const IssueCredentialSchema = z.object({
  subjectId: z.string().optional(),
  documentId: z.string(),
  documentHash: z.string().min(1),
  documentType: z.nativeEnum(SecuuraCredentialType),
  documentTitle: z.string().min(1),
  documentDescription: z.string().optional(),
  // KS-514: `certificationDate` is deliberately NOT date-validated. It never
  // reaches a Date constructor — the builder passes it through as a string
  // (packages/shared/src/vc/builder.ts:119) — so it cannot produce the 500
  // this guard exists to stop. Tightening it would narrow inputs the published
  // contract permits (bare `type: string`) and put the Schemathesis positive
  // generator at odds with the runtime, which is its own class of failure.
  certificationDate: z.string().optional(),
  // KS-514: an unparseable value here used to reach
  // `builder.setExpirationDate(new Date(...))`, whose `.toISOString()`
  // (builder.ts:97) throws `RangeError: Invalid time value` on an Invalid Date
  // — escaping as a 500 INTERNAL_ERROR. The published contract allows any
  // string, so the runtime must answer 400 for the ones it cannot use. 400 is
  // already a declared response for this operation.
  expirationDate: z
    .string()
    // KS-514 (#741 review, step 1 of 3): empty / whitespace-only means ABSENT, not
    // "bad date". Before this PR such a value passed the schema and was skipped by
    // the truthiness check below (`if (issuanceRequest.expirationDate)`), so it
    // never reached the Date constructor and was never part of the 500. Answering
    // 400 for it would be a contract narrowing this ticket did not ask for, and the
    // cost was measured, not guessed: Schemathesis `positive_data_acceptance` fails
    // on `"expirationDate": ""` precisely because this branch answered 400. Mapping
    // it to undefined preserves the prior behaviour exactly.
    .transform((value) => (value.trim() === '' ? undefined : value))
    // KS-514 (step 2 of 3): the actual fix. An unparseable value used to reach
    // `builder.setExpirationDate(new Date(...))`, whose `.toISOString()`
    // (packages/shared/src/vc/builder.ts:97) throws `RangeError: Invalid time value`
    // on an Invalid Date — escaping as a 500 INTERNAL_ERROR. The published contract
    // allows any string, so the runtime must answer 400 for the ones it cannot use.
    // 400 is already a declared response for this operation.
    .refine((value) => value === undefined || !Number.isNaN(new Date(value).getTime()), {
      message:
        'expirationDate must be a parseable date (e.g. "2027-01-01" or "2027-01-01T00:00:00Z")',
    })
    // KS-201 / KS-514 (step 3 of 3): normalise to canonical UTC at the boundary.
    //
    // WHY THIS EXISTS: `setExpirationDate` normalises (`builder.ts:97`
    // `date.toISOString()`) but `setCredentialSubjectFromRequest` passes the RAW
    // caller string straight through (`builder.ts:120`). Without this transform a
    // credential could be issued whose top-level `expirationDate` reads
    // `2027-03-02T00:00:00.000Z` while its `credentialSubject.expirationDate` still
    // reads `2027-02-30` — divergent values inside one anchored artefact, which is
    // the situation KS-201 exists to prevent. Both sites read `validationResult.data`,
    // so normalising here makes them agree by construction.
    //
    // WHY NOT `isoDateTimeSchema` (packages/shared/src/validation/index.ts:154), the
    // shared schema that does the same normalisation: it is `.datetime({offset:true})`
    // first, so it REJECTS date-only values like `"2027-01-01"`. The published
    // contract for this field is a bare `type: string` and the Schemathesis positive
    // generator emits date-only values, so adopting it would narrow the contract and
    // put the harness at odds with the runtime — the same class of failure the
    // `certificationDate` note above avoids. Decision recorded here rather than left
    // implicit; revisit if the published contract is ever tightened to date-time.
    .transform((value) => (value === undefined ? undefined : new Date(value).toISOString()))
    .optional(),
  issuerReference: z.string().optional(),
  verificationLevel: z.nativeEnum(VerificationLevel).optional(),
  metadata: z.record(z.unknown()).optional(),
});

// KS-466 §5: the published VcCredential schema declares `expirationDate` a
// string and `credentialStatus`/`proof` records — the verify validator ignored
// all three, so a spec-violating `proof: [null, null]` was accepted with 200.
// Enforce exactly the declared SHAPES (KS-444 pattern from presentations.ts);
// what's inside an object proof remains a verification concern per KS-445
// (200 verified:false), never a request error.
const VerifyCredentialSchema = z.object({
  credential: z.object({
    '@context': z.array(z.string()),
    id: z.string(),
    type: z.array(z.string()),
    issuer: z.union([z.string(), z.object({ id: z.string() }).passthrough()]),
    issuanceDate: z.string(),
    expirationDate: z.string().optional(),
    credentialSubject: z.object({}).passthrough(),
    credentialStatus: z.record(z.unknown()).optional(),
    proof: z.record(z.unknown()).optional(),
  }).passthrough(),
});

let statusListIndex = 0;

// =============================================================================
// CONFIGURATION
// =============================================================================

const VC_BASE_URL = process.env.VC_BASE_URL || 'https://secuura.io';
const STATUS_LIST_URL = process.env.STATUS_LIST_URL || `${VC_BASE_URL}/credentials/status`;

// Default issuer (in production, this would come from PRISM DID)
const defaultIssuer: VCIssuer = {
  id: process.env.ISSUER_DID || 'did:prism:secuura_default_issuer',
  name: process.env.ISSUER_NAME || 'Secuura Platform',
  description: 'Secuura Document Authenticity Platform',
};

// =============================================================================
// ROUTES
// =============================================================================

/**
 * Issue a new verifiable credential
 * POST /api/credentials
 */
router.post('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Validate request body
    const validationResult = IssueCredentialSchema.safeParse(req.body);
    if (!validationResult.success) {
      throw new AppError(`Validation error: ${validationResult.error.message}`, 400);
    }

    const issuanceRequest: CredentialIssuanceRequest = validationResult.data;

    // Get issuer from request or use default
    const issuer: VCIssuer = req.body.issuer || defaultIssuer;

    // Allocate status list index for revocation support
    const currentStatusIndex = statusListIndex++;

    // Build the credential
    const builder = createVCBuilder({
      baseUrl: VC_BASE_URL,
      statusListUrl: STATUS_LIST_URL,
    });

    builder
      .setType(issuanceRequest.documentType)
      .setIssuer(issuer)
      .setCredentialSubjectFromRequest(issuanceRequest)
      .setCredentialStatus(currentStatusIndex)
      .setInitialProvenance(issuer.id);

    if (issuanceRequest.expirationDate) {
      builder.setExpirationDate(new Date(issuanceRequest.expirationDate));
    }

    const unsignedCredential = builder.build();

    // Sign the credential. Audit A-11: the previous code used a hardcoded
    // `secuura-dev-signing-key` fallback under HMAC while stamping the proof
    // as `Ed25519Signature2020` — fraud-grade for a credential issuer. The
    // gate below removes that fallback entirely. signCredential() in the
    // shared lib also enforces an honest proof-type label.
    if (process.env.VC_ISSUANCE_DISABLED === 'true') {
      throw new AppError(
        'VC issuance is currently disabled. Provision a real Ed25519 signing key in VC_SIGNING_KEY and unset VC_ISSUANCE_DISABLED to resume.',
        503,
      );
    }
    const vcSigningKey = process.env.VC_SIGNING_KEY;
    if (!vcSigningKey) {
      // Refuse unless the operator has explicitly opted into dev mode. We do
      // NOT fall back to a hardcoded key under any circumstances.
      throw new AppError(
        'VC_SIGNING_KEY environment variable is required for credential issuance. ' +
          'Refusing to issue an HMAC-signed credential that would falsely claim Ed25519. ' +
          'Provision a 32-byte Ed25519 PKCS8 hex key, OR set EXPLICIT_DEV_MODE=true plus a per-call dev key to issue clearly-labelled HmacSha256DevPlaceholder2026 credentials.',
        503,
      );
    }
    const signedCredential = await signCredential(
      unsignedCredential,
      issuer.id,
      vcSigningKey,
    );

    // Store the credential
    await credentialRepo.store(signedCredential);

    logger.info('Credential issued', {
      credentialId: signedCredential.id,
      documentId: issuanceRequest.documentId,
      documentType: issuanceRequest.documentType,
      issuerDID: issuer.id,
    });

    res.status(201).json({
      success: true,
      credential: signedCredential,
      metadata: {
        statusListIndex: currentStatusIndex,
        issuedAt: signedCredential.issuanceDate,
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * List credentials
 * GET /api/credentials
 */
router.get('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { limit = '100', offset = '0', issuer, documentType } = req.query;

    const parsedLimit = parseInt(limit as string, 10);
    const parsedOffset = parseInt(offset as string, 10);

    const { credentials, total } = await credentialRepo.list({
      issuer: issuer as string | undefined,
      documentType: documentType as string | undefined,
      limit: parsedLimit,
      offset: parsedOffset,
    });

    res.json({
      credentials,
      pagination: {
        total,
        limit: parsedLimit,
        offset: parsedOffset,
        hasMore: parsedOffset + parsedLimit < total,
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get credential by ID
 * GET /api/credentials/:id
 */
router.get('/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;

    const credential = await credentialRepo.getById(id);

    if (!credential) {
      throw new AppError('Credential not found', 404);
    }

    res.json({ credential });
  } catch (error) {
    next(error);
  }
});

/**
 * Revoke a credential
 * POST /api/credentials/:id/revoke
 */
router.post('/:id/revoke', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const { reason } = req.body;

    const revokedCredential = await credentialRepo.revoke(id, reason);

    if (!revokedCredential) {
      throw new AppError('Credential not found', 404);
    }

    logger.info('Credential revoked', {
      credentialId: revokedCredential.id,
      reason,
    });

    res.json({
      success: true,
      message: 'Credential revoked successfully',
      credentialId: revokedCredential.id,
      revokedAt: new Date().toISOString(),
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Verify a credential
 * POST /api/credentials/verify
 *
 * KS-445 (public since KS-442 — tokenless): a spec-legal but fuzz-shaped
 * credential (e.g. `proof: [null]`) used to crash the shared verifier with a
 * null deref → raw 500. The null/shape guards live in
 * packages/shared/src/vc/verifier.ts and still matter: presentations/verify
 * feeds permissive inner credentials to the same verifier.
 *
 * KS-466 §5 refined the KS-445 boundary: the published VcCredential schema
 * declares `proof` a record, so a NON-OBJECT proof (array/scalar) is a
 * request-shape violation → Zod 400, same as any other spec-shape breach.
 * Structural problems INSIDE an object proof ("Proof missing type", missing
 * proofValue, …) remain a verification FAILURE — 200 `verified: false` with
 * the reason in `result.errors` — exactly the KS-445 semantic.
 */
router.post('/verify', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const validationResult = VerifyCredentialSchema.safeParse(req.body);
    if (!validationResult.success) {
      throw new AppError(`Validation error: ${validationResult.error.message}`, 400);
    }

    const { credential } = validationResult.data;

    // Verify the credential
    const verificationResult = await verifyCredential(credential as unknown as SecuuraCredential, {
      checkStatus: true,
      checkExpiration: true,
      checkBlockchain: false, // Will enable when blockchain integration is ready
      // KS-1352: without these two, `checkStatus: true` above was inert - checkStatus() had no
      // resolver to consult, so it returned valid over an empty error list and a credential
      // revoked by EITHER route verified true with `checks.status: true`.
      ...revocationVerifierConfig(),
    });

    logger.info('Credential verified', {
      credentialId: credential.id,
      verified: verificationResult.verified,
    });

    res.json({
      verified: verificationResult.verified,
      result: verificationResult,
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get credential by document hash
 * GET /api/credentials/by-hash/:hash
 */
router.get('/by-hash/:hash', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { hash } = req.params;

    const credential = await credentialRepo.getByHash(hash);

    if (!credential) {
      throw new AppError('Credential not found for document hash', 404);
    }

    res.json({ credential });
  } catch (error) {
    next(error);
  }
});

export { router as credentialRoutes };
