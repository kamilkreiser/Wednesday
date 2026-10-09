/**
 * =============================================================================
 * AUTHORISED SIGNATORY ROUTES
 * =============================================================================
 * CRUD API for managing Authorised Signatories — individuals nominated by an
 * organisation to certify documents on its behalf.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { body, param, query, validationResult } from 'express-validator';
import { v4 as uuidv4 } from 'uuid';
import { prisma } from '../db';
import { logger } from '../utils/logger';
import { authenticate } from '../middleware/auth';

export const signatoriesRouter = Router();
// All routes here require an authenticated Bearer JWT. Audit A-09 + A-01:
// previously trusted client-supplied x-user-* headers via getUserFromRequest;
// the gateway now strips those (commit c796138f0) and this enforces real
// authentication as defense in depth.
signatoriesRouter.use(authenticate());


// ─────────────────────────────────────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────────────────────────────────────

function getUserFromRequest(req: Request): { id: string; email?: string; name?: string } | null {
  // Pen-test F-04: read from authenticated req.user (set by authenticate()
  // middleware), NOT from raw headers. Direct header reads are spoofable
  // by anyone reaching the service directly.
  const user = (req as any).user;
  const userId = user?.userId;
  if (!userId) return null;
  const email = user?.email as string | undefined;
  return {
    id: userId,
    email,
    name: email?.split('@')[0],
  };
}

/**
 * KS-23 (KS-4 phase 5b): every signatory call is tenant-scoped.
 * Mirrors getReqTenantId in routes/documents.ts and routes/certifications.ts.
 */
const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';
function getReqTenantId(req: Request): string {
  const tid = (req as any).tenantId as string | undefined;
  return tid || DEFAULT_TENANT_ID;
}

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/signatories — Nominate a new authorised signatory
// ─────────────────────────────────────────────────────────────────────────────

signatoriesRouter.post(
  '/',
  [
    body('organizationId').isString().notEmpty().withMessage('Organization ID is required'),
    body('userId').isString().notEmpty().withMessage('User ID is required'),
    body('displayName').isString().notEmpty().withMessage('Display name is required'),
    body('title').optional().isString(),
    body('documentTypes').optional().isArray(),
    body('canDelegate').optional().isBoolean(),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const actor = getUserFromRequest(req);
      if (!actor) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { organizationId, userId, displayName, title, documentTypes, canDelegate } = req.body;

      const id = uuidv4();
      const now = new Date();
      const tenantId = getReqTenantId(req);

      const docTypesArray = `{${(documentTypes || []).map((t: string) => `"${t}"`).join(',')}}`;
      await ((req as any).db || prisma).$executeRaw`
        INSERT INTO signatories (
          id, tenant_id, organization_id, user_id, display_name, title, document_types,
          can_delegate, status, nominated_by, nominated_at, created_at, updated_at
        ) VALUES (
          ${id}::uuid,
          ${tenantId}::uuid,
          ${organizationId}::uuid,
          ${userId}::uuid,
          ${displayName},
          ${title || null},
          ${docTypesArray}::text[],
          ${canDelegate || false},
          'active',
          ${actor.id}::uuid,
          ${now},
          ${now},
          ${now}
        )
      `;

      logger.info('Authorised signatory nominated', { id, organizationId, userId, nominatedBy: actor.id });

      res.status(201).json({
        success: true,
        signatory: {
          id,
          organizationId,
          userId,
          displayName,
          title,
          documentTypes: documentTypes || [],
          canDelegate: canDelegate || false,
          status: 'active',
          nominatedBy: actor.id,
          nominatedAt: now.toISOString(),
        },
      });
    } catch (error: any) {
      if (error.code === '23505') {
        return res.status(409).json({
          success: false,
          error: { code: 'CONFLICT', message: 'This user is already an authorised signatory for this organisation' },
        });
      }
      logger.error('Failed to nominate signatory', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to nominate signatory' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// GET /api/signatories — List signatories for an organisation
// ─────────────────────────────────────────────────────────────────────────────

signatoriesRouter.get(
  '/',
  [query('organizationId').isString().notEmpty().withMessage('Organization ID is required').isUUID().withMessage('Organization ID must be a UUID')],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const { organizationId, status } = req.query;
      const statusFilter = (status as string) || 'active';
      const tenantId = getReqTenantId(req);

      const rows: any[] = await ((req as any).db || prisma).$queryRaw`
        SELECT
          s.id,
          s.organization_id AS "organizationId",
          s.user_id AS "userId",
          s.display_name AS "displayName",
          s.title,
          s.document_types AS "documentTypes",
          s.can_delegate AS "canDelegate",
          s.status,
          s.nominated_by AS "nominatedBy",
          s.nominated_at AS "nominatedAt",
          s.revoked_at AS "revokedAt",
          s.revocation_reason AS "revokedReason",
          u.email AS "userEmail"
        FROM signatories s
        LEFT JOIN users u ON u.id = s.user_id
        WHERE s.tenant_id = ${tenantId}::uuid
          AND s.organization_id = ${organizationId as string}::uuid
          AND (${statusFilter} = 'all' OR s.status = ${statusFilter})
        ORDER BY s.display_name ASC
      `;

      res.json({ success: true, signatories: rows, total: rows.length });
    } catch (error) {
      logger.error('Failed to list signatories', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list signatories' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// GET /api/signatories/check — Check if a user is an authorised signatory
// (Must be registered BEFORE /:id to prevent Express matching "check" as :id)
// ─────────────────────────────────────────────────────────────────────────────

signatoriesRouter.get(
  '/check',
  [
    query('organizationId').isString().notEmpty().withMessage('Organization ID is required').isUUID().withMessage('Organization ID must be a UUID'),
    query('userId').isString().notEmpty().withMessage('User ID is required').isUUID().withMessage('User ID must be a UUID'),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const { organizationId, userId, documentType } = req.query;
      const tenantId = getReqTenantId(req);

      const rows: any[] = await ((req as any).db || prisma).$queryRaw`
        SELECT id, document_types AS "documentTypes", can_delegate AS "canDelegate"
        FROM signatories
        WHERE tenant_id = ${tenantId}::uuid
          AND organization_id = ${organizationId as string}::uuid
          AND user_id = ${userId as string}::uuid
          AND status = 'active'
      `;

      if (rows.length === 0) {
        return res.json({ success: true, authorised: false });
      }

      const signatory = rows[0];
      const types = signatory.documentTypes as string[];

      // If documentTypes is empty → authorised for all types
      const authorised =
        types.length === 0 || !documentType || types.includes(documentType as string);

      res.json({
        success: true,
        authorised,
        signatoryId: signatory.id,
        canDelegate: signatory.canDelegate,
        permittedTypes: types,
      });
    } catch (error) {
      logger.error('Failed to check signatory authorisation', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to check authorisation' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// GET /api/signatories/:id — Get signatory details
// ─────────────────────────────────────────────────────────────────────────────

signatoriesRouter.get(
  '/:id',
  [param('id').isString().notEmpty().withMessage('Signatory ID is required')],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const tenantId = getReqTenantId(req);
      const rows: any[] = await ((req as any).db || prisma).$queryRaw`
        SELECT
          s.id,
          s.organization_id AS "organizationId",
          s.user_id AS "userId",
          s.display_name AS "displayName",
          s.title,
          s.document_types AS "documentTypes",
          s.can_delegate AS "canDelegate",
          s.status,
          s.nominated_by AS "nominatedBy",
          s.nominated_at AS "nominatedAt",
          s.revoked_at AS "revokedAt",
          s.revocation_reason AS "revokedReason",
          u.email AS "userEmail"
        FROM signatories s
        LEFT JOIN users u ON u.id = s.user_id
        WHERE s.id = ${req.params.id}::uuid
          AND s.tenant_id = ${tenantId}::uuid
      `;

      if (rows.length === 0) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Signatory not found' } });
      }

      res.json({ success: true, signatory: rows[0] });
    } catch (error) {
      logger.error('Failed to get signatory', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get signatory' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// PATCH /api/signatories/:id — Update signatory details
// ─────────────────────────────────────────────────────────────────────────────

signatoriesRouter.patch(
  '/:id',
  [
    param('id').isString().notEmpty().withMessage('Signatory ID is required'),
    body('displayName').optional().isString().notEmpty(),
    body('title').optional().isString(),
    body('documentTypes').optional().isArray(),
    body('canDelegate').optional().isBoolean(),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const actor = getUserFromRequest(req);
      if (!actor) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { displayName, title, documentTypes, canDelegate } = req.body;

      // Pen-test M6 fix: was previously string-concatenated into a raw SQL
      // statement — `displayName` / `title` / `req.params.id` were inlined
      // unescaped into the SQL, classic injection. Rewrite as parameterised
      // query: build $N placeholders for the fields the caller actually
      // sent, push the values into the params array in matching order, then
      // execute via $executeRaw[Unsafe] with positional params.
      const setClauses: string[] = ['updated_at = NOW()'];
      const params: any[] = [];
      if (displayName !== undefined) {
        params.push(displayName);
        setClauses.push(`display_name = $${params.length}`);
      }
      if (title !== undefined) {
        params.push(title);
        setClauses.push(`title = $${params.length}`);
      }
      if (documentTypes !== undefined) {
        params.push(JSON.stringify(documentTypes));
        setClauses.push(`document_types = $${params.length}::jsonb`);
      }
      if (canDelegate !== undefined) {
        params.push(canDelegate);
        setClauses.push(`can_delegate = $${params.length}`);
      }
      params.push(req.params.id);
      const idIdx = params.length;
      params.push(getReqTenantId(req));
      const tenantIdx = params.length;

      await ((req as any).db || prisma).$executeRawUnsafe(
        `UPDATE signatories SET ${setClauses.join(', ')}
         WHERE id = $${idIdx}::uuid
           AND tenant_id = $${tenantIdx}::uuid`,
        ...params,
      );

      logger.info('Signatory updated', { id: req.params.id, updatedBy: actor.id });

      res.json({ success: true, message: 'Signatory updated' });
    } catch (error) {
      logger.error('Failed to update signatory', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update signatory' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/signatories/:id/revoke — Revoke signatory authorisation
// ─────────────────────────────────────────────────────────────────────────────

signatoriesRouter.post(
  '/:id/revoke',
  [
    param('id').isString().notEmpty().withMessage('Signatory ID is required'),
    body('reason').optional().isString(),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const actor = getUserFromRequest(req);
      if (!actor) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { reason } = req.body;
      const now = new Date();
      const tenantId = getReqTenantId(req);

      const result = await ((req as any).db || prisma).$executeRaw`
        UPDATE signatories
        SET status = 'revoked',
            revoked_at = ${now},
            revocation_reason = ${reason || null},
            updated_at = ${now}
        WHERE id = ${req.params.id}::uuid
          AND tenant_id = ${tenantId}::uuid
          AND status = 'active'
      `;

      if (result === 0) {
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'Signatory not found or already revoked' },
        });
      }

      logger.info('Signatory revoked', { id: req.params.id, revokedBy: actor.id, reason });

      res.json({
        success: true,
        message: 'Signatory authorisation revoked',
        revokedAt: now.toISOString(),
      });
    } catch (error) {
      logger.error('Failed to revoke signatory', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to revoke signatory' } });
    }
  },
);

// ─────────────────────────────────────────────────────────────────────────────
// POST /api/signatories/:id/reinstate — Reinstate a revoked signatory
// ─────────────────────────────────────────────────────────────────────────────

signatoriesRouter.post(
  '/:id/reinstate',
  [param('id').isString().notEmpty().withMessage('Signatory ID is required')],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const actor = getUserFromRequest(req);
      if (!actor) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const tenantId = getReqTenantId(req);
      const result = await ((req as any).db || prisma).$executeRaw`
        UPDATE signatories
        SET status = 'active',
            revoked_at = NULL,
            revocation_reason = NULL,
            reinstated_at = NOW(),
            updated_at = NOW()
        WHERE id = ${req.params.id}::uuid
          AND tenant_id = ${tenantId}::uuid
          AND status = 'revoked'
      `;

      if (result === 0) {
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'Signatory not found or not in revoked state' },
        });
      }

      logger.info('Signatory reinstated', { id: req.params.id, reinstatedBy: actor.id });

      res.json({ success: true, message: 'Signatory reinstated' });
    } catch (error) {
      logger.error('Failed to reinstate signatory', { error: String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to reinstate signatory' } });
    }
  },
);

// NOTE: /check route is registered above /:id to prevent Express route shadowing.
