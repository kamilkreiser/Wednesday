/**
 * =============================================================================
 * STATUS LIST ROUTES
 * =============================================================================
 * Credential status (revocation) management via StatusList2021
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import {
  createStatusListManager,
  StatusListManager,
} from '@secuura/shared/vc';
import { requireRole } from '@secuura/shared';
import { logger } from '../utils/logger';
import { AppError } from '../middleware/errorHandler';

const router = Router();

// =============================================================================
// AUTHORIZATION (KS-586)
// =============================================================================

// KS-586: these routes previously had NO authorization — any authenticated
// user, in any tenant, with any role, could create status lists and revoke or
// un-revoke credentials (jwtAuthenticate at the /api mount verifies the
// signature and nothing else). Revocation state is an integrity operation on a
// document-authenticity platform, so every WRITE now requires an admin-class
// role. Enforced once at the route table — a gate on the router, ahead of the
// route definitions — rather than per-endpoint, so a future POST added to this
// file is covered by default instead of shipping open.
//
// KS-692 (Kam 2026-09-16, card secuura-ks692-status-revoke-interim-posture, option a:
// Narrow now, bind-creator later). Tenant scoping still cannot be enforced here: a status
// list lives in a process-local Map with no owning tenant, so there is no tenant to compare
// a caller against, and an ISSUER_ADMIN in ANY tenant could revoke or un-revoke ANY
// tenant's credential (reproduced live). Until a list carries an owner, writes are for the
// platform roles only. When lists gain an owner, ISSUER_ADMIN comes back together with a
// per-list ownership check. Tracked on KS-692; KS-586 is Done and no longer tracks this.
// 'SUPER_ADMIN'/'super_admin' are the legacy JWT variants the existing admin
// gates already accept — the seeded platform admin carries 'super_admin'
// (see services/auth/src/routes/users.ts:90 and issuerCerts.ts ADMIN_ROLES).
export const STATUS_WRITE_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin'] as const;

router.use((req: Request, res: Response, next: NextFunction) => {
  // Reads stay authenticated-only (status lists are verification data);
  // every non-read verb requires an admin-class role.
  if (req.method === 'GET' || req.method === 'HEAD' || req.method === 'OPTIONS') {
    return next();
  }
  return requireRole(...STATUS_WRITE_ROLES)(
    req as Parameters<ReturnType<typeof requireRole>>[0],
    res,
    next,
  );
});

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

// KS-444: the published StatusListCreateRequest schema declares
// `id: string (minLength 1)`, `purpose: 'revocation' | 'suspension'` and
// `capacity: positive integer`. The handler previously only checked `!id`, so
// an `id` sent as an OBJECT (`{}` — truthy) was accepted and echoed into a
// 201. Enforce exactly the declared types; extension fields the handler also
// honours (issuerDID/issuerName) are undeclared in the spec and stay
// passthrough/unvalidated.
const CreateStatusListSchema = z.object({
  id: z.string().min(1),
  purpose: z.enum(['revocation', 'suspension']).optional(),
  capacity: z.number().int().positive().optional(),
}).passthrough();

// =============================================================================
// STATUS LIST MANAGERS (one per purpose)
// =============================================================================

const statusListManagers = new Map<string, StatusListManager>();

// Initialize default revocation list
const defaultStatusListId = process.env.STATUS_LIST_ID || 'default';
const issuerDID = process.env.ISSUER_DID || 'did:prism:secuura_default_issuer';

statusListManagers.set(defaultStatusListId, createStatusListManager({
  id: `${process.env.VC_BASE_URL || 'https://secuura.io'}/credentials/status/${defaultStatusListId}`,
  issuerDID,
  issuerName: process.env.ISSUER_NAME || 'Secuura Platform',
  purpose: 'revocation',
}));

/**
 * KS-1352: is this credential revoked in ANY status list this process holds?
 *
 * The verify path needs the status list's own revocation bit, and `statusListManagers` is
 * module-local. This is the narrowest accessor that answers the question: it exposes no manager
 * and permits no mutation.
 *
 * Keyed by CREDENTIAL ID, not by index. A credential's `credentialStatus.statusListIndex` comes
 * from the issue route's own counter, which is a different sequence from `allocateIndex()`, so an
 * index from one is not a valid key into the other. `getEntry()` distinguishes "not in this list"
 * from "in this list and not revoked", which is what lets the verifier abstain rather than guess.
 *
 * `found: false` means no list holds this credential - for example it was never allocated, or it
 * was allocated in another replica. The caller decides what that means; this function does not.
 */
export function statusListRevocation(credentialId: string): { found: boolean; revoked: boolean } {
  for (const manager of statusListManagers.values()) {
    if (manager.getEntry(credentialId)) {
      return { found: true, revoked: manager.isRevoked(credentialId) };
    }
  }
  return { found: false, revoked: false };
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * Get status list credential
 * GET /api/status/:id
 */
router.get('/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;

    const manager = statusListManagers.get(id);
    if (!manager) {
      throw new AppError('Status list not found', 404);
    }

    const statusListCredential = manager.buildStatusListCredential();

    res.json({
      credential: statusListCredential,
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Check if an index is revoked
 * GET /api/status/:id/check/:index
 */
router.get('/:id/check/:index', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id, index } = req.params;

    const manager = statusListManagers.get(id);
    if (!manager) {
      throw new AppError('Status list not found', 404);
    }

    const indexNum = parseInt(index, 10);
    // KS-440: reject a non-numeric OR negative index. A bitstring position is a
    // non-negative integer; without the `< 0` guard the handler echoed a negative
    // index straight back, violating the response schema (index minimum 0).
    if (isNaN(indexNum) || indexNum < 0) {
      throw new AppError('Invalid index', 400);
    }

    const isRevoked = manager.isIndexRevoked(indexNum);

    res.json({
      statusListId: id,
      index: indexNum,
      isRevoked,
      checkedAt: new Date().toISOString(),
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get all revoked indexes
 * GET /api/status/:id/revoked
 */
router.get('/:id/revoked', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;

    const manager = statusListManagers.get(id);
    if (!manager) {
      throw new AppError('Status list not found', 404);
    }

    const revokedIndexes = manager.getRevokedIndexes();

    res.json({
      statusListId: id,
      revokedIndexes,
      totalRevoked: revokedIndexes.length,
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Allocate a new index for a credential
 * POST /api/status/:id/allocate
 */
router.post('/:id/allocate', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const { credentialId } = req.body;

    // KS-440: require a non-empty STRING. The old truthy `!credentialId` check let
    // a fuzzed non-string (e.g. `{}`) through, which the handler then echoed back
    // into the response — violating the response schema (credentialId: string).
    if (typeof credentialId !== 'string' || credentialId.length === 0) {
      throw new AppError('credentialId is required and must be a string', 400);
    }

    const manager = statusListManagers.get(id);
    if (!manager) {
      throw new AppError('Status list not found', 404);
    }

    const index = manager.allocateIndex(credentialId);

    logger.info('Status list index allocated', {
      statusListId: id,
      credentialId,
      index,
    });

    res.json({
      statusListId: id,
      credentialId,
      index,
      allocatedAt: new Date().toISOString(),
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Revoke a credential by ID
 * POST /api/status/:id/revoke
 */
router.post('/:id/revoke', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const { credentialId, reason } = req.body;

    // KS-440: require a non-empty STRING. The old truthy `!credentialId` check let
    // a fuzzed non-string (e.g. `{}`) through, which the handler then echoed back
    // into the response — violating the response schema (credentialId: string).
    if (typeof credentialId !== 'string' || credentialId.length === 0) {
      throw new AppError('credentialId is required and must be a string', 400);
    }
    // KS-1269: index is optional and not read here, but a present index must be an integer (-1 stays admitted, the KS-662 ruling).
    if (req.body.index !== undefined && !Number.isInteger(req.body.index)) {
      throw new AppError('index must be an integer', 400);
    }
    // KS-440: `reason` is an optional string; a fuzzed object was echoed into the
    // response `reason` (schema: string). Reject a non-string reason.
    if (reason !== undefined && typeof reason !== 'string') {
      throw new AppError('reason must be a string', 400);
    }

    const manager = statusListManagers.get(id);
    if (!manager) {
      throw new AppError('Status list not found', 404);
    }

    // KS-444/KS-445: revoking a credential that was never allocated in this list
    // makes the manager throw a plain Error → a raw 500. An unknown credential is
    // a not-found, not a server fault.
    if (manager.getIndex(credentialId) === undefined) {
      throw new AppError('Credential not found in status list', 404);
    }

    manager.revoke(credentialId, reason);

    logger.info('Credential revoked in status list', {
      statusListId: id,
      credentialId,
      reason,
    });

    res.json({
      statusListId: id,
      credentialId,
      revoked: true,
      reason,
      revokedAt: new Date().toISOString(),
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Unrevoke a credential by ID
 * POST /api/status/:id/unrevoke
 */
router.post('/:id/unrevoke', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const { credentialId } = req.body;

    // KS-440: require a non-empty STRING. The old truthy `!credentialId` check let
    // a fuzzed non-string (e.g. `{}`) through, which the handler then echoed back
    // into the response — violating the response schema (credentialId: string).
    if (typeof credentialId !== 'string' || credentialId.length === 0) {
      throw new AppError('credentialId is required and must be a string', 400);
    }

    const manager = statusListManagers.get(id);
    if (!manager) {
      throw new AppError('Status list not found', 404);
    }

    // KS-444/KS-445: same not-found class as revoke — an unallocated credential
    // must not surface as a raw 500.
    if (manager.getIndex(credentialId) === undefined) {
      throw new AppError('Credential not found in status list', 404);
    }

    // KS-1269: index is optional and not read here, but a present index must be an integer.
    // KS-1371: and not below the declared minimum 0 (KS-662 tolerates index -1 on revoke only).
    if (req.body.index !== undefined && (!Number.isInteger(req.body.index) || req.body.index < 0)) {
      throw new AppError('index must be a non-negative integer', 400);
    }
    manager.unrevoke(credentialId);

    logger.info('Credential unrevoked in status list', {
      statusListId: id,
      credentialId,
    });

    res.json({
      statusListId: id,
      credentialId,
      revoked: false,
      unrevokedAt: new Date().toISOString(),
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Create a new status list
 * POST /api/status
 */
router.post('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-444: enforce the spec-declared request shape (see schema above).
    const validationResult = CreateStatusListSchema.safeParse(req.body);
    if (!validationResult.success) {
      throw new AppError(`Validation error: ${validationResult.error.message}`, 400);
    }

    const { id, purpose = 'revocation' } = validationResult.data;
    // Spec extension fields (passthrough) the handler also honours — undeclared
    // in the spec, so read loosely, unvalidated.
    const { issuerDID: customIssuerDID, issuerName } = req.body;

    if (statusListManagers.has(id)) {
      throw new AppError('Status list with this ID already exists', 409);
    }

    const manager = createStatusListManager({
      id: `${process.env.VC_BASE_URL || 'https://secuura.io'}/credentials/status/${id}`,
      issuerDID: customIssuerDID || issuerDID,
      issuerName: issuerName || 'Secuura Platform',
      purpose: purpose as 'revocation' | 'suspension',
    });

    statusListManagers.set(id, manager);

    logger.info('Status list created', {
      statusListId: id,
      purpose,
    });

    res.status(201).json({
      statusListId: id,
      purpose,
      createdAt: new Date().toISOString(),
    });
  } catch (error) {
    next(error);
  }
});

/**
 * List all status lists
 * GET /api/status
 */
router.get('/', async (_req: Request, res: Response, next: NextFunction) => {
  try {
    const statusLists = Array.from(statusListManagers.keys()).map(id => ({
      id,
      url: `${process.env.VC_BASE_URL || 'https://secuura.io'}/credentials/status/${id}`,
    }));

    res.json({
      statusLists,
      total: statusLists.length,
    });
  } catch (error) {
    next(error);
  }
});

export { router as statusRoutes };
