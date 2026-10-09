/**
 * =============================================================================
 * PRESENTATION ROUTES
 * =============================================================================
 * W3C Verifiable Presentation creation and verification
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { v4 as uuidv4 } from 'uuid';
import {
  createPresentation,
  SecuuraCredential,
  VerifiablePresentation,
  verifyCredential,
} from '@secuura/shared/vc';
import { logger } from '../utils/logger';
import { AppError } from '../middleware/errorHandler';
import { revocationVerifierConfig } from '../services/revocationResolvers';

const router = Router();

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

// KS-444: the published VcCredential request schema (vc-issuer.openapi.ts)
// declares `expirationDate` as a string and `credentialStatus`/`proof` as
// objects. The create-presentation validator previously ignored those three,
// so a spec-violating credential (e.g. `proof: 123`, `expirationDate: 5`) was
// minted into a stored VP with a 201. Enforce exactly the declared types —
// nothing more (extension fields stay passthrough, matching the spec).
const CreatePresentationCredentialSchema = z.object({
  '@context': z.array(z.string()),
  id: z.string(),
  type: z.array(z.string()),
  issuer: z.union([z.string(), z.object({ id: z.string() }).passthrough()]),
  issuanceDate: z.string(),
  expirationDate: z.string().optional(),
  credentialSubject: z.object({}).passthrough(),
  credentialStatus: z.record(z.unknown()).optional(),
  proof: z.record(z.unknown()).optional(),
}).passthrough();

const CreatePresentationSchema = z.object({
  credentials: z.array(CreatePresentationCredentialSchema),
  holderDID: z.string().optional(),
  challenge: z.string().optional(),
  domain: z.string().optional(),
});

// KS-444: enforce the spec-declared types of the Vp envelope (`id`/`holder`
// strings). The inner credentials deliberately stay permissive: this op is
// PUBLIC (KS-442) and — per the KS-445 decision on /credentials/verify —
// malformed credential/proof CONTENT is a verification FAILURE (200
// verified:false with reasons), never a request error. 400 stays reserved for
// bodies violating the required top-level shape — which, per KS-466 §5, now
// includes a non-object `proof`: the spec (Vp) declares it a record, so an
// array/scalar there is a shape violation, while what's INSIDE an object
// proof remains the verifier's concern.
const VerifyPresentationSchema = z.object({
  presentation: z.object({
    '@context': z.array(z.string()),
    id: z.string().optional(),
    type: z.array(z.string()),
    verifiableCredential: z.array(z.object({}).passthrough()),
    holder: z.string().optional(),
    proof: z.record(z.unknown()).optional(),
  }).passthrough(),
  challenge: z.string().optional(),
  domain: z.string().optional(),
});

// KS-444: the request-presentation op — the spec (VpRequestRequest) declares
// `credentialTypes` as a REQUIRED array of strings and `challenge`/`domain`
// as optional strings. The handler previously only checked
// Array.isArray(credentialTypes), so `credentialTypes: [{}]` or `domain: {}`
// was echoed into a 201. Enforce exactly the declared shape (passthrough for
// the spec's extension fields, e.g. requiredFields/purpose).
const RequestPresentationSchema = z.object({
  credentialTypes: z.array(z.string()),
  challenge: z.string().optional(),
  domain: z.string().optional(),
}).passthrough();

// =============================================================================
// STORAGE — DB-first with in-memory fallback
// =============================================================================

import { query, isDbAvailable } from '../db';

const memPresentationStore = new Map<string, VerifiablePresentation>();

async function storePresentation(id: string, presentation: VerifiablePresentation): Promise<void> {
  memPresentationStore.set(id, presentation);
  if (isDbAvailable()) {
    try {
      await query(
        `INSERT INTO vc_presentations_store (id, presentation, holder_id)
         VALUES ($1, $2, $3)
         ON CONFLICT (id) DO UPDATE SET presentation = EXCLUDED.presentation`,
        [id, JSON.stringify(presentation), (presentation as any).holder || null],
      );
    } catch (err: any) {
      logger.warn('DB storePresentation failed — in-memory only', { error: err?.message });
    }
  }
}

// KS-1020: an id lookup is EXACT or it is 404. This function used to fall back
// from the exact match to `WHERE id LIKE '%<id>%' LIMIT 1` on the DB path and
// to a `key.includes(id)` scan over the in-memory store, so an id that names
// nothing (`0`, `abc`, `1`, `a`, `e`) resolved to an arbitrary stored
// presentation, with no ownership check on that path. Both fallbacks are
// deleted: there is no legitimate caller who knows a fragment of an id and not
// the id. What remains is the exact DB lookup (falling through on a DB error,
// as before) and the exact in-memory get; GET /:id answers 404 on `undefined`.
async function getPresentation(id: string): Promise<VerifiablePresentation | undefined> {
  // DB first
  if (isDbAvailable()) {
    try {
      const result = await query(`SELECT presentation FROM vc_presentations_store WHERE id = $1`, [id]);
      if (result.rows.length > 0) return result.rows[0].presentation as VerifiablePresentation;
    } catch { /* fall through */ }
  }

  // Memory fallback
  const exact = memPresentationStore.get(id);
  if (exact) return exact;
  return undefined;
}

// =============================================================================
// DATABASE PERSISTENCE LOADING
// =============================================================================

export async function loadPresentationsFromDb(): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    const result = await query<{ id: string; presentation: VerifiablePresentation }>(
      'SELECT id, presentation FROM vc_presentations_store ORDER BY created_at DESC',
    );
    for (const row of result.rows) {
      memPresentationStore.set(row.id, row.presentation);
    }
    logger.info('Presentations loaded from DB', { count: result.rows.length });
  } catch (err) {
    logger.warn('loadPresentationsFromDb failed — starting with empty store', {
      error: err instanceof Error ? err.message : String(err),
    });
  }
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * Create a verifiable presentation
 * POST /api/presentations
 */
router.post('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const validationResult = CreatePresentationSchema.safeParse(req.body);
    if (!validationResult.success) {
      throw new AppError(`Validation error: ${validationResult.error.message}`, 400);
    }

    const { credentials, holderDID, challenge, domain } = validationResult.data;

    // Create presentation
    const presentation = createPresentation(
      credentials as unknown as SecuuraCredential[],
      holderDID
    );

    // Add ID
    const presentationId = `${process.env.VC_BASE_URL || 'https://secuura.io'}/presentations/${uuidv4()}`;
    const fullPresentation: VerifiablePresentation = {
      ...presentation,
      id: presentationId,
    };

    // Sign the presentation. Audit A-11: previously this code HMAC-signed
    // under a hardcoded `secuura-dev-signing-key` fallback while stamping
    // the proof as `Ed25519Signature2020` — the same fraud pattern as the
    // credential issuance path. Same gates apply: VC_ISSUANCE_DISABLED kill
    // switch; refuse in production unless real key provided; honest type
    // label when running with a dev placeholder.
    if (holderDID) {
      if (process.env.VC_ISSUANCE_DISABLED === 'true') {
        throw new AppError(
          'VC presentation signing is currently disabled (VC_ISSUANCE_DISABLED=true). ' +
            'Provision a real Ed25519 signing key in VC_SIGNING_KEY and unset VC_ISSUANCE_DISABLED to resume.',
          503,
        );
      }
      const vcSigningKey = process.env.VC_SIGNING_KEY;
      const isExplicitDevMode = process.env.EXPLICIT_DEV_MODE === 'true';
      if (!vcSigningKey && !isExplicitDevMode) {
        throw new AppError(
          'VC_SIGNING_KEY is required to sign a presentation. ' +
            'Refusing to emit an HMAC-signed presentation falsely labelled Ed25519. ' +
            'Provision an Ed25519 key, or set EXPLICIT_DEV_MODE=true plus a per-call dev key to issue HmacSha256DevPlaceholder2026 presentations.',
          503,
        );
      }

      const crypto = await import('crypto');
      const created = new Date().toISOString();
      const payload = JSON.stringify({
        presentationId,
        holderDID,
        created,
        challenge,
        domain,
      });

      let proofValue: string;
      let proofType: string;
      if (vcSigningKey && vcSigningKey.length >= 64 && !vcSigningKey.startsWith('placeholder')) {
        // Real Ed25519 PKCS8 hex key — produce a real Ed25519 signature.
        try {
          const keyBuf = Buffer.from(vcSigningKey, 'hex');
          const keyObj = crypto.createPrivateKey({ key: keyBuf, format: 'der', type: 'pkcs8' });
          const sig = crypto.sign(null, Buffer.from(payload), keyObj);
          proofValue = `z${sig.toString('base64url')}`;
          proofType = 'Ed25519Signature2020';
        } catch (e) {
          throw new AppError(
            `VC_SIGNING_KEY did not parse as Ed25519 PKCS8 hex: ${(e as Error).message}. Refusing to fall back to HMAC.`,
            500,
          );
        }
      } else {
        // EXPLICIT_DEV_MODE path — clearly-labelled non-cryptographic placeholder.
        const hmac = crypto.createHmac('sha256', vcSigningKey ?? '');
        hmac.update(payload);
        proofValue = `zDEV_${hmac.digest('base64url')}`;
        proofType = 'HmacSha256DevPlaceholder2026';
      }

      (fullPresentation as any).proof = {
        type: proofType,
        created,
        verificationMethod: `${holderDID}#key-1`,
        proofPurpose: 'authentication',
        challenge,
        domain,
        proofValue,
      };
    }

    // Store presentation (DB + memory)
    await storePresentation(presentationId, fullPresentation);

    logger.info('Presentation created', {
      presentationId,
      credentialCount: credentials.length,
      holderDID,
    });

    res.status(201).json({
      success: true,
      presentation: fullPresentation,
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Verify a verifiable presentation
 * POST /api/presentations/verify
 */
router.post('/verify', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const validationResult = VerifyPresentationSchema.safeParse(req.body);
    if (!validationResult.success) {
      throw new AppError(`Validation error: ${validationResult.error.message}`, 400);
    }

    const { presentation, challenge, domain } = validationResult.data;

    // Verify each credential in the presentation
    const credentialResults = await Promise.all(
      presentation.verifiableCredential.map(async (credential) => {
        // KS-1352: the same defect reached this route, which passed NO config at all. Only the
        // revocation resolvers are added - the constructor's other defaults are left exactly as
        // they were, so nothing but revocation changes here.
        return verifyCredential(credential as unknown as SecuuraCredential, {
          ...revocationVerifierConfig(),
        });
      })
    );

    // KS-444: an EMPTY verifiableCredential array must never verify true —
    // `[].every()` is vacuously true, so a fuzz-degenerate presentation
    // ({verifiableCredential: [], proof: [null, null]}) previously came back
    // `verified: true` from a public endpoint. A presentation that presents
    // no credentials has verified nothing.
    const hasCredentials = presentation.verifiableCredential.length > 0;
    const allCredentialsValid = hasCredentials && credentialResults.every(r => r.verified);

    // Verify presentation proof (if present)
    let presentationProofValid = true;
    const rawProof = (presentation as any).proof;
    // KS-444: same normalisation as the shared verifier (KS-445) — a proof
    // that is present but not an object (array/primitive/null) is a
    // verification FAILURE, not something to silently treat as valid.
    const proofIsMalformed =
      rawProof !== undefined &&
      (rawProof === null || typeof rawProof !== 'object' || Array.isArray(rawProof));
    const proof = proofIsMalformed ? undefined : rawProof;

    if (proofIsMalformed) {
      presentationProofValid = false;
    } else if (proof) {
      // Check challenge and domain if provided
      if (challenge && proof.challenge !== challenge) {
        presentationProofValid = false;
      }
      if (domain && proof.domain !== domain) {
        presentationProofValid = false;
      }
      // In production, verify the cryptographic signature
    }

    const verified = allCredentialsValid && presentationProofValid;

    logger.info('Presentation verified', {
      presentationId: (presentation as any).id,
      verified,
      credentialCount: presentation.verifiableCredential.length,
    });

    res.json({
      verified,
      presentationId: (presentation as any).id,
      holder: (presentation as any).holder,
      credentialResults: credentialResults.map((r: { credentialId: string; verified: boolean; issuer: unknown; credential: { status: string }; errors?: string[] }, i: number) => ({
        credentialIndex: i,
        credentialId: r.credentialId,
        verified: r.verified,
        issuer: r.issuer,
        status: r.credential.status,
        errors: r.errors,
      })),
      checks: {
        allCredentialsValid,
        presentationProofValid,
        challengeValid: !challenge || proof?.challenge === challenge,
        domainValid: !domain || proof?.domain === domain,
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get presentation by ID
 * GET /api/presentations/:id
 */
router.get('/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;

    const presentation = await getPresentation(id);

    if (!presentation) {
      throw new AppError('Presentation not found', 404);
    }

    res.json({ presentation });
  } catch (error) {
    next(error);
  }
});

/**
 * Request a credential presentation
 * POST /api/presentations/request
 */
router.post('/request', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-444: validate the spec-declared shape (credentialTypes: string[],
    // challenge/domain: optional strings) instead of a bare Array.isArray check.
    const validationResult = RequestPresentationSchema.safeParse(req.body);
    if (!validationResult.success) {
      throw new AppError(`Validation error: ${validationResult.error.message}`, 400);
    }

    const { credentialTypes, challenge, domain } = validationResult.data;
    // Spec extension fields (passthrough) the handler also honours — the spec
    // does not declare their types, so they are read loosely, unvalidated.
    const { requiredFields, purpose } = req.body;

    const requestId = uuidv4();
    const presentationRequest = {
      id: requestId,
      type: 'PresentationRequest',
      credentialTypes,
      requiredFields: requiredFields || [],
      purpose: purpose || 'Credential verification',
      challenge: challenge || uuidv4(),
      domain: domain || process.env.VC_BASE_URL || 'https://secuura.io',
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 15 * 60 * 1000).toISOString(), // 15 minutes
    };

    logger.info('Presentation request created', {
      requestId,
      credentialTypes,
    });

    res.status(201).json({
      success: true,
      request: presentationRequest,
    });
  } catch (error) {
    next(error);
  }
});

export { router as presentationRoutes };
