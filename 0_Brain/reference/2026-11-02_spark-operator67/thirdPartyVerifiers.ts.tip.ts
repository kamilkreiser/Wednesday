/**
 * =============================================================================
 * THIRD-PARTY VERIFIER ROUTES
 * =============================================================================
 * API for registering, managing, and executing platform-authorised third-party
 * verifications. Third-party verifiers are organisations/individuals approved
 * by Secuura to perform elevated verification.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { body, param, validationResult } from 'express-validator';
import { v4 as uuidv4 } from 'uuid';
import crypto from 'crypto';
import { prisma } from '../db';
import { logger } from '../utils/logger';
import { authenticate } from '../middleware/auth';

export const thirdPartyVerifiersRouter = Router();
// All routes here require an authenticated Bearer JWT. Audit A-09 + A-01:
// previously trusted client-supplied x-user-* headers via getUserFromRequest;
// the gateway now strips those (commit c796138f0) and this enforces real
// authentication as defense in depth.
thirdPartyVerifiersRouter.use(authenticate());


// ─────────────────────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────────────────────

function getUserFromRequest(req: Request): { id: string; email?: string } | null {
  // Pen-test F-04: read from authenticated req.user (set by authenticate()
  // middleware), NOT from raw headers. Direct header reads are spoofable
  // by anyone reaching the service directly.
  const user = (req as any).user;
  const userId = user?.userId;
  if (!userId) return null;
  return { id: userId, email: user?.email };
}

function hashApiKey(key: string): string {
  return crypto.createHash('sha256').update(key).digest('hex');
}

function generateApiKey(): string {
  return `tpv_${crypto.randomBytes(32).toString('hex')}`;
}

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/third-party-verifiers/register — Register a new third-party verifier
// ─────────────────────────────────────────────────────────────────────────────

thirdPartyVerifiersRouter.post(
  '/register',
  [
    body('organizationName').isString().notEmpty().withMessage('Organisation name is required'),
    body('contactEmail').isEmail().withMessage('Valid contact email is required'),
    body('verificationTypes').optional().isArray(),
    body('tier').optional().isIn(['standard', 'premium', 'enterprise']),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const { organizationName, contactEmail, verificationTypes, tier } = req.body;
      const id = uuidv4();
      const now = new Date();

      await ((req as any).db || prisma).$executeRaw`
        INSERT INTO third_party_verifiers (
          id, organization_name, contact_email, verification_types, tier, status, created_at, updated_at
        ) VALUES (
          ${id}::uuid,
          ${organizationName},
          ${contactEmail},
          ${JSON.stringify(verificationTypes || [])}::jsonb,
          ${tier || 'standard'},
          'pending',
          ${now},
          ${now}
        )
      `;

      logger.info('Third-party verifier registered', { id, organizationName, contactEmail });

      res.status(201).json({
        success: true,
        verifier: {
          id,
          organizationName,
          contactEmail,
          verificationTypes: verificationTypes || [],
          tier: tier || 'standard',
          status: 'pending',
          createdAt: now.toISOString(),
        },
        message: 'Registration submitted. Awaiting platform approval.',
      });
    } catch (error: any) {
      if (error.code === '23505') {
        return res.status(409).json({
          success: false,
          error: { code: 'CONFLICT', message: 'A verifier with this email is already registered' },
        });
      }
      logger.error('Failed to register verifier', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to register verifier' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// GET /api/third-party-verifiers — List all verifiers (admin)
// ─────────────────────────────────────────────────────────────────────────────

thirdPartyVerifiersRouter.get('/', async (req: Request, res: Response) => {
  try {
    const status = (req.query.status as string) || 'all';

    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT
        id,
        organization_name AS "organizationName",
        contact_email AS "contactEmail",
        verification_types AS "verificationTypes",
        tier,
        status,
        approved_by AS "approvedBy",
        approved_at AS "approvedAt",
        suspended_at AS "suspendedAt",
        suspended_reason AS "suspendedReason",
        created_at AS "createdAt"
      FROM third_party_verifiers
      WHERE ${status} = 'all' OR status = ${status}
      ORDER BY created_at DESC
    `;

    res.json({ success: true, verifiers: rows, total: rows.length });
  } catch (error) {
    logger.error('Failed to list verifiers', { error: String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list verifiers' } });
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/third-party-verifiers/:id/approve — Approve a pending verifier
// ─────────────────────────────────────────────────────────────────────────────

thirdPartyVerifiersRouter.post(
  '/:id/approve',
  [param('id').isString().notEmpty().withMessage('Verifier ID is required')],
  async (req: Request, res: Response) => {
    try {
      const admin = getUserFromRequest(req);
      if (!admin) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const apiKey = generateApiKey();
      const apiKeyHash = hashApiKey(apiKey);
      const now = new Date();

      const result = await ((req as any).db || prisma).$executeRaw`
        UPDATE third_party_verifiers
        SET status = 'active',
            api_key_hash = ${apiKeyHash},
            approved_by = ${admin.id}::uuid,
            approved_at = ${now},
            updated_at = ${now}
        WHERE id = ${req.params.id}::uuid
          AND status = 'pending'
      `;

      if (result === 0) {
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'Verifier not found or not in pending state' },
        });
      }

      logger.info('Third-party verifier approved', { id: req.params.id, approvedBy: admin.id });

      res.json({
        success: true,
        message: 'Verifier approved',
        apiKey,
        note: 'Store this API key securely. It will not be shown again.',
      });
    } catch (error) {
      logger.error('Failed to approve verifier', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to approve verifier' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/third-party-verifiers/:id/suspend — Suspend an active verifier
// ─────────────────────────────────────────────────────────────────────────────

thirdPartyVerifiersRouter.post(
  '/:id/suspend',
  [
    param('id').isString().notEmpty().withMessage('Verifier ID is required'),
    body('reason').optional().isString(),
  ],
  async (req: Request, res: Response) => {
    try {
      const admin = getUserFromRequest(req);
      if (!admin) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { reason } = req.body;
      const now = new Date();

      const result = await ((req as any).db || prisma).$executeRaw`
        UPDATE third_party_verifiers
        SET status = 'suspended',
            suspended_at = ${now},
            suspended_reason = ${reason || null},
            updated_at = ${now}
        WHERE id = ${req.params.id}::uuid
          AND status = 'active'
      `;

      if (result === 0) {
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'Verifier not found or not active' },
        });
      }

      logger.info('Third-party verifier suspended', { id: req.params.id, reason });

      res.json({ success: true, message: 'Verifier suspended' });
    } catch (error) {
      logger.error('Failed to suspend verifier', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to suspend verifier' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/third-party-verifiers/:id/reinstate — Reinstate a suspended verifier
// ─────────────────────────────────────────────────────────────────────────────

thirdPartyVerifiersRouter.post(
  '/:id/reinstate',
  [param('id').isString().notEmpty().withMessage('Verifier ID is required')],
  async (req: Request, res: Response) => {
    try {
      const admin = getUserFromRequest(req);
      if (!admin) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const result = await ((req as any).db || prisma).$executeRaw`
        UPDATE third_party_verifiers
        SET status = 'active',
            suspended_at = NULL,
            suspended_reason = NULL,
            updated_at = NOW()
        WHERE id = ${req.params.id}::uuid
          AND status = 'suspended'
      `;

      if (result === 0) {
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'Verifier not found or not suspended' },
        });
      }

      res.json({ success: true, message: 'Verifier reinstated' });
    } catch (error) {
      logger.error('Failed to reinstate verifier', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to reinstate verifier' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/third-party-verifiers/verify — Perform a third-party verification
// ─────────────────────────────────────────────────────────────────────────────

thirdPartyVerifiersRouter.post(
  '/verify',
  [
    body('certificationId').isString().notEmpty().withMessage('Certification ID is required'),
    body('apiKey').isString().notEmpty().withMessage('API key is required'),
    body('notes').optional().isString(),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const { certificationId, apiKey, notes } = req.body;
      const keyHash = hashApiKey(apiKey);

      // Authenticate the verifier by API key
      const verifiers: any[] = await ((req as any).db || prisma).$queryRaw`
        SELECT id, organization_name AS "organizationName", tier, verification_types AS "verificationTypes"
        FROM third_party_verifiers
        WHERE api_key_hash = ${keyHash}
          AND status = 'active'
      `;

      if (verifiers.length === 0) {
        return res.status(401).json({
          success: false,
          error: { code: 'UNAUTHORIZED', message: 'Invalid or inactive API key' },
        });
      }

      const verifier = verifiers[0];
      const recordId = uuidv4();
      const now = new Date();

      // Record the third-party verification
      await ((req as any).db || prisma).$executeRaw`
        INSERT INTO third_party_verification_records (
          id, verifier_id, certification_id, verification_result, confidence_score, notes, audit_trail, created_at
        ) VALUES (
          ${recordId}::uuid,
          ${verifier.id}::uuid,
          ${certificationId},
          'verified',
          ${95.00},
          ${notes || null},
          ${JSON.stringify({
            verifierOrg: verifier.organizationName,
            verifierTier: verifier.tier,
            timestamp: now.toISOString(),
            method: 'api_key_authentication',
          })}::jsonb,
          ${now}
        )
      `;

      logger.info('Third-party verification recorded', {
        recordId,
        verifierId: verifier.id,
        certificationId,
      });

      res.json({
        success: true,
        verification: {
          id: recordId,
          certificationId,
          verifier: verifier.organizationName,
          tier: verifier.tier,
          result: 'verified',
          confidenceScore: 95.0,
          timestamp: now.toISOString(),
        },
      });
    } catch (error) {
      logger.error('Failed to perform third-party verification', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to perform verification' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// GET /api/third-party-verifiers/:id/records — Get verification records for a verifier
// ─────────────────────────────────────────────────────────────────────────────

thirdPartyVerifiersRouter.get(
  '/:id/records',
  [param('id').isString().notEmpty().withMessage('Verifier ID is required')],
  async (req: Request, res: Response) => {
    try {
      const rows: any[] = await ((req as any).db || prisma).$queryRaw`
        SELECT
          id,
          certification_id AS "certificationId",
          verification_result AS "result",
          confidence_score AS "confidenceScore",
          notes,
          audit_trail AS "auditTrail",
          created_at AS "createdAt"
        FROM third_party_verification_records
        WHERE verifier_id = ${req.params.id}::uuid
        ORDER BY created_at DESC
        LIMIT 100
      `;

      res.json({ success: true, records: rows, total: rows.length });
    } catch (error) {
      logger.error('Failed to get verification records', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get records' } });
    }
  },
);
