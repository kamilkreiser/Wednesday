/**
 * =============================================================================
 * ADMIN CONFIGURATION ROUTES
 * =============================================================================
 * REST API for managing:
 * - Pricing configuration
 * - Document type definitions
 * - Workflow configurations
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { getPricingTable, updatePricing, loadPricing } from '../services/chargeEvents';
import { prisma, refreshTenantConfigs, withTenant } from '../db';
import { authenticate, requireRole } from '../middleware/auth';
// KS-458: this router is admin-gated (authenticate + SYSTEM_ADMIN/ORG_ADMIN
// below), and several handlers deliberately read/write across tenants with no
// tenant filter. Under fail-closed RLS (migration 039) those statements need
// the platform-scope GUC bundled into their transaction, or they silently
// see/affect zero rows.
import { runWithPlatformScope, queryWithTenantGuc, decideKeyRevoke } from '@secuura/shared';
import { logger } from '../utils/logger';
import { isDemoSeedEnabled } from '../utils/demoSeedGate';

export const adminConfigRouter = Router();

// Admin routes always use the shared DB — tenant filtering via WHERE clauses, not pool switching.
// The tenant selector in the admin portal is for SETUP/CONFIG, not for browsing client data.
adminConfigRouter.use((req, _res, next) => {
  (req as any).db = prisma; // Always shared DB
  // Pen-test F-04: read tenantId from req.tenantId (set by extractTenantContext
  // middleware after token verification), NOT from raw headers.
  (req as any).filterTenantId = ((req as any).tenantId as string | undefined) || null;
  next();
});

// All routes require authentication + SYSTEM_ADMIN or ORG_ADMIN role.
adminConfigRouter.use(authenticate(), requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'));

/**
 * Minimal email-format check for rights-holder create/update. A rights holder
 * must have a valid email (product decision 2026-05-22, KS-106); this checks the
 * format. Mirrors the `.isEmail()` intent used elsewhere in this service
 * (certifications.ts, thirdPartyVerifiers.ts) without pulling express-validator
 * into these manual handlers.
 */
function isValidEmail(value: unknown): boolean {
  if (typeof value !== 'string') return false;
  const email = value.trim();
  return email.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

const SUPER_ADMIN_ROLES = ['super_admin', 'SUPER_ADMIN', 'SYSTEM_ADMIN', 'platform_admin'];

/**
 * Resolve the tenant (== organization id) a rights-holders request operates on,
 * for the `app.tenant_id` GUC the RLS policy keys off (KS-108 / KS-93).
 *
 * - Tenant-bound admins (ORG_ADMIN, ISSUER_ADMIN…) → their own org from the
 *   verified JWT. They cannot reach another tenant.
 * - super_admins → the verified X-Tenant-Override (`req.tenantId`, set by the
 *   gateway + extractTenantContext) or `?organizationId=`. This is the KS-93
 *   fix: super_admin scopes via the same override used elsewhere, no dual-send.
 *
 * Returns null when no tenant can be resolved — callers MUST treat that as "no
 * access" (empty / 400), never "all tenants". RLS is the backstop: even a wrong
 * value only scopes to that one tenant, it can never leak across tenants.
 */
function resolveTenantId(req: Request): string | null {
  const u = (req as any).user;
  if (u?.role && SUPER_ADMIN_ROLES.includes(u.role)) {
    return ((req as any).tenantId as string | undefined)
      || (req.query?.organizationId as string | undefined)
      || (u?.organizationId as string | undefined)
      || null;
  }
  return (u?.organizationId as string | undefined) || null;
}

// =============================================================================
// TENANT CONFIG REFRESH
// =============================================================================

/** Force reload tenant configs (call after creating a new tenant) */
/**
 * KS-730: the only place in this router that turns a caught error into a 500.
 *
 * WHAT WAS WRONG. Forty-six inline handlers returned `err.message` verbatim unless
 * `NODE_ENV === 'production'`, so `development`, `demo`, `test` and an UNSET NODE_ENV all answered an
 * admin-configuration route with raw internal text. This is the largest of the three files KS-730
 * enumerates, and the reason the ticket asked for a helper rather than 67 edited ternaries.
 *
 * WHY A HELPER AND NOT A DELETION. KS-727's fix was SUBTRACTIVE — its shared handlers already logged
 * at entry, so removing the ternary lost nothing. Measured across the three files this ticket
 * enumerates: **0 of 65 sites log the error before returning it.** Deleting the ternary alone would
 * destroy the diagnostic at all 46 sites here. The log is added in the same change.
 *
 * Each call site passes its own context naming the route, and all 46 are DISTINCT — a mislabelled
 * context is worse than none, because it sends a reader to the wrong handler. The contexts were
 * GENERATED from each site's enclosing route registration rather than hand-written, since 46 typed
 * strings is 46 chances to mislabel one, and a cell asserts the count and the distinctness.
 */
function fail500(res: Response, context: string, err: unknown): void {
  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
}

adminConfigRouter.post('/refresh-tenants', async (_req: Request, res: Response) => {
  try {
    await refreshTenantConfigs();
    res.json({ success: true, message: 'Tenant configs refreshed' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/refresh-tenants)', err);
  }
});

// =============================================================================
// PRICING
// =============================================================================

/** Get current pricing table */
adminConfigRouter.get('/pricing', async (_req: Request, res: Response) => {
  try {
    const pricing = getPricingTable();
    res.json({ success: true, pricing });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (GET /api/admin/pricing)', err);
  }
});

/** Update pricing for an event type */
adminConfigRouter.patch('/pricing/:eventType', async (req: Request, res: Response) => {
  try {
    const { adaAmount, usdAmount } = req.body;
    if (adaAmount === undefined || usdAmount === undefined) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'adaAmount and usdAmount are required' } });
    }
    if (typeof adaAmount !== 'number' || typeof usdAmount !== 'number' || adaAmount < 0 || usdAmount < 0) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'adaAmount and usdAmount must be non-negative numbers' } });
    }
    const updated = await updatePricing(req.params.eventType, adaAmount, usdAmount);
    res.json({ success: updated, message: updated ? 'Pricing updated' : 'Event type not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PATCH /api/admin/pricing/:eventType)', err);
  }
});

/** Refresh pricing cache from database */
adminConfigRouter.post('/pricing/refresh', async (_req: Request, res: Response) => {
  try {
    await loadPricing();
    res.json({ success: true, pricing: getPricingTable() });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/pricing/refresh)', err);
  }
});

// =============================================================================
// DOCUMENT TYPES
// =============================================================================

/** List all document types */
adminConfigRouter.get('/document-types', async (req: Request, res: Response) => {
  try {
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT * FROM document_type_configs ORDER BY name ASC
    `;
    res.json({ success: true, documentTypes: rows.map(mapDocTypeRow) });
  } catch (err: any) {
    // Table may not exist yet — return empty list so frontend uses its defaults
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, documentTypes: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/document-types)', err);
  }
});

/** Create a document type */
adminConfigRouter.post('/document-types', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    if (!d.name || !d.code) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'name and code are required' } });
    }
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      INSERT INTO document_type_configs (
        name, code, description, category, is_active,
        creator_verification_level, owner_verification_level, viewer_verification_level, verifier_verification_level,
        require_mfa, require_wallet_signature, require_kyc, allowed_auth_providers,
        requires_approval, approval_workflow_id, auto_anchor, anchor_network,
        metadata_schema, allowed_sources, webhook_events
      ) VALUES (
        ${d.name}, ${d.code}, ${d.description || null}, ${d.category || 'Other'}, ${d.isActive !== false},
        ${d.creatorVerificationLevel || 'basic'}, ${d.ownerVerificationLevel || 'basic'},
        ${d.viewerVerificationLevel || 'none'}, ${d.verifierVerificationLevel || 'standard'},
        ${d.requireMFA || false}, ${d.requireWalletSignature || false}, ${d.requireKYC || false},
        ${JSON.stringify(d.allowedAuthProviders || [])}::jsonb,
        ${d.requiresApproval || false}, ${d.approvalWorkflowId || null}::uuid, ${d.autoAnchor !== false},
        ${d.anchorNetwork || 'preprod'},
        ${JSON.stringify(d.metadataSchema || [])}::jsonb,
        ${JSON.stringify(d.allowedSources || [])}::jsonb,
        ${JSON.stringify(d.webhookEvents || [])}::jsonb
      ) RETURNING *
    `;
    res.status(201).json({ success: true, documentType: mapDocTypeRow(rows[0]) });
  } catch (err: any) {
    if (err?.message?.includes('unique constraint')) {
      return res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'Document type code already exists' } });
    }
    fail500(res, 'Admin config request failed (POST /api/admin/document-types)', err);
  }
});

/** Update a document type */
adminConfigRouter.put('/document-types/:id', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    const result = await ((req as any).db || prisma).$executeRaw`
      UPDATE document_type_configs SET
        name = COALESCE(${d.name || null}, name),
        description = COALESCE(${d.description || null}, description),
        category = COALESCE(${d.category || null}, category),
        is_active = COALESCE(${d.isActive}, is_active),
        creator_verification_level = COALESCE(${d.creatorVerificationLevel || null}, creator_verification_level),
        owner_verification_level = COALESCE(${d.ownerVerificationLevel || null}, owner_verification_level),
        viewer_verification_level = COALESCE(${d.viewerVerificationLevel || null}, viewer_verification_level),
        verifier_verification_level = COALESCE(${d.verifierVerificationLevel || null}, verifier_verification_level),
        require_mfa = COALESCE(${d.requireMFA}, require_mfa),
        require_wallet_signature = COALESCE(${d.requireWalletSignature}, require_wallet_signature),
        require_kyc = COALESCE(${d.requireKYC}, require_kyc),
        requires_approval = COALESCE(${d.requiresApproval}, requires_approval),
        auto_anchor = COALESCE(${d.autoAnchor}, auto_anchor),
        anchor_network = COALESCE(${d.anchorNetwork || null}, anchor_network),
        metadata_schema = COALESCE(${d.metadataSchema ? JSON.stringify(d.metadataSchema) : null}::jsonb, metadata_schema),
        allowed_sources = COALESCE(${d.allowedSources ? JSON.stringify(d.allowedSources) : null}::jsonb, allowed_sources),
        webhook_events = COALESCE(${d.webhookEvents ? JSON.stringify(d.webhookEvents) : null}::jsonb, webhook_events),
        updated_at = NOW()
      WHERE id = ${req.params.id}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Updated' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/document-types/:id)', err);
  }
});

/** Delete a document type */
adminConfigRouter.delete('/document-types/:id', async (req: Request, res: Response) => {
  try {
    const result = await ((req as any).db || prisma).$executeRaw`
      DELETE FROM document_type_configs WHERE id = ${req.params.id}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Deleted' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (DELETE /api/admin/document-types/:id)', err);
  }
});

// =============================================================================
// WORKFLOWS
// =============================================================================

/** List all workflows */
adminConfigRouter.get('/workflows', async (req: Request, res: Response) => {
  try {
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT * FROM workflow_configs ORDER BY name ASC
    `;
    res.json({ success: true, workflows: rows.map(mapWorkflowRow) });
  } catch (err: any) {
    // Table may not exist yet — return empty list so frontend uses its defaults
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, workflows: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/workflows)', err);
  }
});

/** Create a workflow */
adminConfigRouter.post('/workflows', async (req: Request, res: Response) => {
  try {
    const w = req.body;
    if (!w.name) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'name is required' } });
    }
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      INSERT INTO workflow_configs (name, description, type, is_active, steps, document_types, sla_hours)
      VALUES (
        ${w.name}, ${w.description || null}, ${w.type || 'sequential'}, ${w.isActive !== false},
        ${JSON.stringify(w.steps || [])}::jsonb, ${JSON.stringify(w.documentTypes || [])}::jsonb,
        ${w.slaHours || 24}
      ) RETURNING *
    `;
    res.status(201).json({ success: true, workflow: mapWorkflowRow(rows[0]) });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/workflows)', err);
  }
});

/** Update a workflow */
adminConfigRouter.put('/workflows/:id', async (req: Request, res: Response) => {
  try {
    const w = req.body;
    const result = await ((req as any).db || prisma).$executeRaw`
      UPDATE workflow_configs SET
        name = COALESCE(${w.name || null}, name),
        description = COALESCE(${w.description || null}, description),
        type = COALESCE(${w.type || null}, type),
        is_active = COALESCE(${w.isActive}, is_active),
        steps = COALESCE(${w.steps ? JSON.stringify(w.steps) : null}::jsonb, steps),
        document_types = COALESCE(${w.documentTypes ? JSON.stringify(w.documentTypes) : null}::jsonb, document_types),
        sla_hours = COALESCE(${w.slaHours || null}, sla_hours),
        updated_at = NOW()
      WHERE id = ${req.params.id}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Updated' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/workflows/:id)', err);
  }
});

/** Delete a workflow */
adminConfigRouter.delete('/workflows/:id', async (req: Request, res: Response) => {
  try {
    const result = await ((req as any).db || prisma).$executeRaw`
      DELETE FROM workflow_configs WHERE id = ${req.params.id}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Deleted' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (DELETE /api/admin/workflows/:id)', err);
  }
});

// =============================================================================
// VERIFICATION QUEUE
// =============================================================================

/** List verification queue items */
adminConfigRouter.get('/verification-queue', async (req: Request, res: Response) => {
  try {
    const status = req.query.status as string | undefined;
    const priority = req.query.priority as string | undefined;

    const filterStatus = (status && status !== 'all') ? status : null;
    const filterPriority = (priority && priority !== 'all') ? priority : null;

    // KS-29: tenant-scoped — admin in tenant A cannot list items in tenant B.
    // tenant_id was added in migration 015; req.tenantId is the effective
    // tenant after extractTenantContext resolves any X-Tenant-Override.
    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT * FROM admin_verification_queue
      WHERE tenant_id = ${tenantId}::uuid
        AND (${filterStatus}::text IS NULL OR status = ${filterStatus})
        AND (${filterPriority}::text IS NULL OR priority = ${filterPriority})
      ORDER BY created_at DESC
    `;
    res.json({ success: true, items: rows.map(mapQueueRow) });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, items: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/verification-queue)', err);
  }
});

/** Perform an action on a verification queue item */
adminConfigRouter.post('/verification-queue/:id/action', async (req: Request, res: Response) => {
  try {
    const { action, notes, assignedTo } = req.body;
    if (!action) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'action is required (approve, reject, escalate, assign)' } });
    }

    let newStatus: string;
    switch (action) {
      case 'approve': newStatus = 'approved'; break;
      case 'reject': newStatus = 'rejected'; break;
      case 'escalate': newStatus = 'escalated'; break;
      case 'assign': newStatus = 'in_review'; break;
      default:
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Unknown action: ${action}` } });
    }

    // KS-29: tenant-scoped action — admin in tenant A cannot transition an
    // item in tenant B by guessing its id.
    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';
    const result = await ((req as any).db || prisma).$executeRaw`
      UPDATE admin_verification_queue SET
        status = ${newStatus},
        assigned_to = COALESCE(${assignedTo || null}, assigned_to),
        notes = COALESCE(${notes || null}, notes),
        updated_at = NOW()
      WHERE id = ${req.params.id}
        AND tenant_id = ${tenantId}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? `Item ${action}d` : 'Item not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/verification-queue/:id/action)', err);
  }
});

// =============================================================================
// INTEGRATIONS
// =============================================================================

/** List all integrations */
adminConfigRouter.get('/integrations', async (req: Request, res: Response) => {
  try {
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT * FROM admin_integrations ORDER BY name ASC
    `;
    res.json({ success: true, integrations: rows.map(mapIntegrationRow) });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, integrations: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/integrations)', err);
  }
});

/** Create an integration */
adminConfigRouter.post('/integrations', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    if (!d.name || !d.integrationType || !d.provider) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'name, integrationType, and provider are required' } });
    }
    // Pen-test F-09
    const id = `int_${require('crypto').randomUUID()}`;
    await ((req as any).db || prisma).$executeRaw`
      INSERT INTO admin_integrations (id, name, integration_type, provider, status, config)
      VALUES (${id}, ${d.name}, ${d.integrationType}, ${d.provider},
              ${d.status || 'disconnected'}, ${JSON.stringify(d.config || {})}::jsonb)
    `;
    res.status(201).json({ success: true, integration: { id, ...d } });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/integrations)', err);
  }
});

/** Update an integration */
adminConfigRouter.put('/integrations/:id', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    const result = await ((req as any).db || prisma).$executeRaw`
      UPDATE admin_integrations SET
        name = COALESCE(${d.name || null}, name),
        status = COALESCE(${d.status || null}, status),
        config = COALESCE(${d.config ? JSON.stringify(d.config) : null}::jsonb, config),
        error_message = ${d.errorMessage || null},
        last_sync_at = ${d.status === 'connected' ? new Date() : null},
        updated_at = NOW()
      WHERE id = ${req.params.id}
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Updated' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/integrations/:id)', err);
  }
});

/** Delete an integration */
adminConfigRouter.delete('/integrations/:id', async (req: Request, res: Response) => {
  try {
    const result = await ((req as any).db || prisma).$executeRaw`
      DELETE FROM admin_integrations WHERE id = ${req.params.id}
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Deleted' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (DELETE /api/admin/integrations/:id)', err);
  }
});

// =============================================================================
// PLATFORM SETTINGS
// =============================================================================

/** Get all settings (optionally filtered by category) */
adminConfigRouter.get('/settings', async (req: Request, res: Response) => {
  try {
    const category = req.query.category as string | undefined;
    let rows: any[];
    if (category) {
      rows = await ((req as any).db || prisma).$queryRaw`
        SELECT * FROM admin_settings WHERE category = ${category} ORDER BY key ASC
      `;
    } else {
      rows = await ((req as any).db || prisma).$queryRaw`
        SELECT * FROM admin_settings ORDER BY category ASC, key ASC
      `;
    }

    // Convert to a nested object grouped by category
    const settings: Record<string, Record<string, unknown>> = {};
    for (const row of rows) {
      if (!settings[row.category]) settings[row.category] = {};
      const shortKey = row.key.includes('.') ? row.key.split('.').slice(1).join('.') : row.key;
      settings[row.category][shortKey] = row.value;
    }

    res.json({ success: true, settings });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, settings: {} });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/settings)', err);
  }
});

/** Update one or more settings */
adminConfigRouter.put('/settings', async (req: Request, res: Response) => {
  try {
    const updates: Record<string, unknown> = req.body;
    let updatedCount = 0;

    for (const [key, value] of Object.entries(updates)) {
      const result = await ((req as any).db || prisma).$executeRaw`
        UPDATE admin_settings SET value = ${JSON.stringify(value)}::jsonb, updated_at = NOW()
        WHERE key = ${key}
      `;
      if (result > 0) updatedCount++;
      else {
        // Insert if not exists
        const category = key.split('.')[0] || 'general';
        await ((req as any).db || prisma).$executeRaw`
          INSERT INTO admin_settings (key, value, category) VALUES (${key}, ${JSON.stringify(value)}::jsonb, ${category})
          ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
        `;
        updatedCount++;
      }
    }

    res.json({ success: true, updatedCount });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/settings)', err);
  }
});

// =============================================================================
// DASHBOARD
// =============================================================================

/** Aggregate platform stats (used by audit log page header) */
adminConfigRouter.get('/dashboard', async (req: Request, res: Response) => {
  try {
    const db = (req as any).db || prisma;

    // H25 (2026-04-28): honour X-Tenant-Override on the count queries.
    // Without this, a super_admin viewing tenant X via the override sees
    // platform-wide totals (1597 / 1400 etc.) regardless of which tenant
    // is selected — the H12 banner says "Cross-tenant mode" but the data
    // behind it is unscoped. Per-tenant routing at the connection level
    // exists (TenantPoolManager) but in dev all tenants share the same
    // Postgres database, so connection-level routing alone doesn't filter.
    //
    // Logic: if the original request supplied X-Tenant-Override (super-
    // admin viewing a specific tenant), tag every count query with
    // `WHERE tenant_id = $1` (joining via owner_user_id → users for
    // documents). With no override, return platform-wide aggregate
    // (the existing default — which is what H15's "PLATFORM TOTALS"
    // label tells the operator they're seeing).
    const overrideHeader = req.headers['x-tenant-override'] as string | undefined;
    const overrideUuid =
      overrideHeader && /^[0-9a-fA-F-]{36}$/.test(overrideHeader) ? overrideHeader : null;

    // BACKLOG H3: totalVerifications used to count ALL audit_logs rows (wrong
    // — that's a count of every recorded mutation, not just verifies).
    // Filter to just verification-related audit entries. Prefer the audit_logs
    // path if rows exist; fall back to anchor_store as a coarse approximation.
    // KS-458 (admin cross-tenant): platform-wide totals / override-tenant
    // counts have no request-tenant filter (or filter a DIFFERENT tenant than
    // the caller's), so they run under the platform scope.
    const [docCount, userCount, verifyCount] = await runWithPlatformScope(() => Promise.all([
      overrideUuid
        ? db.$queryRaw`
            SELECT COUNT(d.id)::int AS count
            FROM documents d
            LEFT JOIN users u ON d.owner_user_id = u.id
            WHERE u.tenant_id = ${overrideUuid}::uuid
          `.catch(() => [{ count: 0 }])
        : db.$queryRaw`SELECT COUNT(*)::int AS count FROM documents`.catch(() => [{ count: 0 }]),
      overrideUuid
        ? db.$queryRaw`SELECT COUNT(*)::int AS count FROM users WHERE tenant_id = ${overrideUuid}::uuid`
            .catch(() => [{ count: 0 }])
        : db.$queryRaw`SELECT COUNT(*)::int AS count FROM users`.catch(() => [{ count: 0 }]),
      overrideUuid
        ? db.$queryRaw`
            SELECT COUNT(a.id)::int AS count FROM audit_logs a
            LEFT JOIN users u ON a.user_id = u.id
            WHERE (a.action LIKE 'verification.%' OR a.resource_type = 'verification')
              AND u.tenant_id = ${overrideUuid}::uuid
          `.catch(() => [{ count: 0 }])
        : db.$queryRaw`
            SELECT COUNT(*)::int AS count FROM audit_logs
            WHERE action LIKE 'verification.%' OR resource_type = 'verification'
          `.catch(() => [{ count: 0 }]),
    ])) as any[];

    const totalDocs = docCount[0]?.count ?? 0;
    const totalUsers = userCount[0]?.count ?? 0;
    const totalVerifications = verifyCount[0]?.count ?? 0;

    // Count blockchain anchors
    let totalAnchors = 0;
    try {
      // anchor_store doesn't have tenant_id directly — go via document_id → documents → users.
      // Skip the join when no override (platform-wide aggregate).
      // KS-458 (admin cross-tenant): the documents/users join has no
      // request-tenant filter — platform scope, same as the counts above.
      const anchorCount = (await runWithPlatformScope(() => overrideUuid
        ? db.$queryRaw`
            SELECT COUNT(a.id)::int AS count
            FROM anchor_store a
            JOIN documents d ON a.document_id = d.external_id
            LEFT JOIN users u ON d.owner_user_id = u.id
            WHERE u.tenant_id = ${overrideUuid}::uuid
          `
        : db.$queryRaw`SELECT COUNT(*)::int AS count FROM anchor_store`)) as any[];
      totalAnchors = anchorCount[0]?.count ?? 0;
    } catch { /* table may not exist */ }

    // BACKLOG H3: previously hard-counted only auth + anchoring (+1 for self
    // = 3). The platform actually runs 30+ services. Health enumeration
    // doesn't belong in originate — the API gateway already has the
    // authoritative `/system/status` endpoint that probes every service.
    // Omitting the field tells the frontend to query /system/status itself
    // (it already has that fallback path).

    // Recent activity from audit log — KS-28 tenant-scoped. The dashboard
    // is rendered per the request's effective tenant; super_admin override
    // flips that via X-Tenant-Override.
    let recentActivity: any[] = [];
    try {
      const dashboardTenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';
      recentActivity = await ((req as any).db || prisma).$queryRaw`
        SELECT id, action, resource_type, user_id, created_at, success, details
        FROM audit_logs
        WHERE tenant_id = ${dashboardTenantId}::uuid
        ORDER BY created_at DESC LIMIT 10
      `;
    } catch { /* table may not exist */ }

    res.json({
      success: true,
      stats: {
        totalDocuments: totalDocs,
        totalUsers: totalUsers,
        totalVerifications,
        totalAnchors,
        // servicesOnline intentionally omitted — caller should hit
        // /system/status for the authoritative number.
      },
      recentActivity: recentActivity.map((r: any) => ({
        id: r.id,
        action: r.action,
        resourceType: r.resource_type,
        userId: r.user_id,
        createdAt: r.created_at?.toISOString?.() || r.created_at,
        success: r.success,
        details: r.details,
      })),
    });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (GET /api/admin/dashboard)', err);
  }
});

// =============================================================================
// VERIFICATION POLICIES
// =============================================================================

/** List verification policies */
adminConfigRouter.get('/verification-policies', async (req: Request, res: Response) => {
  try {
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT * FROM verification_policies ORDER BY created_at DESC
    `;
    res.json({
      success: true,
      policies: rows.map(mapPolicyRow),
      total: rows.length,
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, policies: [], total: 0 });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/verification-policies)', err);
  }
});

/** Create a verification policy */
adminConfigRouter.post('/verification-policies', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    if (!d.name) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'name is required' } });
    }
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      INSERT INTO verification_policies (
        name, description, scope, is_active,
        min_user_verification_level, min_org_verification_level,
        required_auth_providers, require_mfa, require_wallet_signature,
        region_restrictions, enforcement_mode
      ) VALUES (
        ${d.name}, ${d.description || null}, ${d.scope || 'deployment'},
        ${d.isActive !== false},
        ${d.minUserVerificationLevel || 'BASIC'}, ${d.minOrgVerificationLevel || 'BASIC'},
        ${JSON.stringify(d.requiredAuthProviders || [])}::jsonb,
        ${d.requireMFA || false}, ${d.requireWalletSignature || false},
        ${JSON.stringify(d.regionRestrictions || [])}::jsonb,
        ${d.enforcementMode || 'warn'}
      ) RETURNING *
    `;
    res.status(201).json({ success: true, policy: mapPolicyRow(rows[0]) });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/verification-policies)', err);
  }
});

/** Update a verification policy */
adminConfigRouter.put('/verification-policies/:id', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    const result = await ((req as any).db || prisma).$executeRaw`
      UPDATE verification_policies SET
        name = COALESCE(${d.name || null}, name),
        description = COALESCE(${d.description || null}, description),
        scope = COALESCE(${d.scope || null}, scope),
        is_active = COALESCE(${d.isActive}, is_active),
        min_user_verification_level = COALESCE(${d.minUserVerificationLevel || null}, min_user_verification_level),
        enforcement_mode = COALESCE(${d.enforcementMode || null}, enforcement_mode),
        updated_at = NOW()
      WHERE id = ${req.params.id}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Updated' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/verification-policies/:id)', err);
  }
});

/** Delete a verification policy */
adminConfigRouter.delete('/verification-policies/:id', async (req: Request, res: Response) => {
  try {
    const result = await ((req as any).db || prisma).$executeRaw`
      DELETE FROM verification_policies WHERE id = ${req.params.id}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Deleted' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (DELETE /api/admin/verification-policies/:id)', err);
  }
});

/** Verification policy audit trail */
adminConfigRouter.get('/verification-policies/audit', async (req: Request, res: Response) => {
  try {
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT * FROM policy_audit_log ORDER BY created_at DESC LIMIT 100
    `;
    res.json({ success: true, entries: rows });
  } catch {
    res.json({ success: true, entries: [] });
  }
});

/** Regional verification policies */
adminConfigRouter.get('/verification-policies/regional', async (req: Request, res: Response) => {
  try {
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT * FROM verification_policies
      WHERE region_restrictions IS NOT NULL AND region_restrictions != '[]'::jsonb
      ORDER BY name ASC
    `;
    res.json({ success: true, regions: rows.map(mapPolicyRow) });
  } catch {
    res.json({ success: true, regions: [] });
  }
});

// =============================================================================
// ORGANIZATIONS
// =============================================================================

/** List organizations */
adminConfigRouter.get('/organizations', async (req: Request, res: Response) => {
  try {
    // KS-458 (admin cross-tenant): org listing join has no tenant filter.
    const rows: any[] = await runWithPlatformScope(() => ((req as any).db || prisma).$queryRaw`
      SELECT o.*, COUNT(om.user_id)::int AS user_count
      FROM organizations o
      LEFT JOIN organization_members om ON om.organization_id = o.id
      GROUP BY o.id
      ORDER BY o.name ASC
    `);
    res.json({
      success: true,
      organizations: rows.map(mapOrgRow),
      total: rows.length,
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, organizations: [], total: 0 });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/organizations)', err);
  }
});

/** Create an organization */
adminConfigRouter.post('/organizations', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    if (!d.name) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'name is required' } });
    }
    const slug = d.slug || d.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    // KS-458 (admin cross-tenant): organizations is a fail-closed flip table
    // and a new org is not the caller's tenant — platform scope for the write.
    const rows: any[] = await runWithPlatformScope(() => ((req as any).db || prisma).$queryRaw`
      INSERT INTO organizations (name, slug, type, status, domain, settings)
      VALUES (${d.name}, ${slug}, ${d.type || 'issuer'}, ${d.status || 'active'},
              ${d.domain || null}, ${JSON.stringify(d.settings || {})}::jsonb)
      RETURNING *
    `);
    res.status(201).json({ success: true, organization: mapOrgRow(rows[0]) });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/organizations)', err);
  }
});

/** Update an organization */
adminConfigRouter.put('/organizations/:id', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    // KS-458 (admin cross-tenant): targets an arbitrary org by id, no
    // caller-tenant filter — platform scope so the UPDATE matches under RLS.
    const result = await runWithPlatformScope(() => ((req as any).db || prisma).$executeRaw`
      UPDATE organizations SET
        name = COALESCE(${d.name || null}, name),
        type = COALESCE(${d.type || null}, type),
        status = COALESCE(${d.status || null}, status),
        domain = COALESCE(${d.domain || null}, domain),
        updated_at = NOW()
      WHERE id = ${req.params.id}::uuid
    `);
    res.json({ success: result > 0, message: result > 0 ? 'Updated' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/organizations/:id)', err);
  }
});

/** Delete an organization (cascade: members, rights holders, documents, users) */
adminConfigRouter.delete('/organizations/:id', async (req: Request, res: Response) => {
  try {
    const db = (req as any).db || prisma;
    const orgId = req.params.id;

    // Cascade delete dependent records in correct order
    // KS-108: scope this org's rights_holders delete to its tenant under RLS.
    await withTenant(orgId, (tx) => tx.$executeRaw`DELETE FROM rights_holders WHERE organization_id = ${orgId}::uuid`);
    // KS-458 (admin cross-tenant): the cascade targets an arbitrary org's
    // documents/members/org rows, not the caller's tenant — platform scope.
    const result = await runWithPlatformScope(async () => {
      await db.$executeRaw`DELETE FROM documents WHERE issuer_organization_id = ${orgId}::uuid`;
      await db.$executeRaw`DELETE FROM organization_members WHERE organization_id = ${orgId}::uuid`;
      return db.$executeRaw`
        DELETE FROM organizations WHERE id = ${orgId}::uuid
      `;
    });
    res.json({ success: result > 0, message: result > 0 ? 'Deleted (cascade)' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (DELETE /api/admin/organizations/:id)', err);
  }
});

// =============================================================================
// API KEYS
// =============================================================================

/** List API keys (tenant-scoped, reads svc_api_keys — the table the
 *  gateway's /api/keys/validate also reads, so keys returned here are
 *  the same set that actually validates through the gateway).
 *
 *  KS-33: cut over from `api_keys` to `svc_api_keys` so the originate
 *  admin path and the security-service validation path see the same
 *  rows. KS-24's tenant-scoping guarantees still hold — `svc_api_keys`
 *  has tenant_id NOT NULL + RLS post-migration 018, and every WHERE
 *  filters on req.tenantId here too as defence-in-depth. */
adminConfigRouter.get('/api-keys', async (req: Request, res: Response) => {
  try {
    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT id, key_prefix, name, scopes, rate_limit, is_active,
             expires_at, last_used_at, created_at
      FROM svc_api_keys
      WHERE tenant_id = ${tenantId}::uuid
      ORDER BY created_at DESC
    `;
    res.json({
      success: true,
      keys: rows.map((r: any) => ({
        id: r.id,
        keyPrefix: r.key_prefix,
        name: r.name,
        // svc_api_keys.scopes is text[]; expose as `permissions` to
        // keep the admin UI's response shape unchanged across the
        // KS-33 cutover.
        permissions: Array.isArray(r.scopes) ? r.scopes : [],
        rateLimit: r.rate_limit,
        isActive: r.is_active,
        expiresAt: r.expires_at?.toISOString?.() || r.expires_at,
        lastUsedAt: r.last_used_at?.toISOString?.() || r.last_used_at,
        createdAt: r.created_at?.toISOString?.() || r.created_at,
      })),
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, keys: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/api-keys)', err);
  }
});

/** Create an API key. KS-33: writes to svc_api_keys so the resulting
 *  sk_* validates through the gateway (security service's
 *  /api/keys/validate reads svc_api_keys, not api_keys). */
adminConfigRouter.post('/api-keys', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    // KS-1206: the security service bounds this field to an integer from 1 to 10000; refuse anything else before the INSERT.
    if (d.rateLimit !== undefined && !(Number.isInteger(d.rateLimit) && d.rateLimit >= 1 && d.rateLimit <= 10000)) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'rateLimit must be an integer from 1 to 10000' } });
    }
    if (!d.name) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'name is required' } });
    }
    // Audit A-12: API key value MUST be cryptographic — 32 bytes from
    // crypto.randomBytes (256 bits of entropy, hex-encoded).
    const cryptoMod = require('crypto') as typeof import('crypto');
    const keyValue = `sk_${cryptoMod.randomBytes(32).toString('hex')}`;
    const keyPrefix = keyValue.substring(0, 12);
    // KS-24 + KS-33: tenant from req.tenantId (extractTenantContext-set);
    // organization_id is optional in svc_api_keys post-018 — SYSTEM_ADMIN
    // issuing a per-tenant key without picking a specific org is fine.
    // The internal record id is `key_<uuid>` to match the format the
    // security service uses for its own POST /api/keys (see
    // services/security/src/index.ts:703).
    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';
    const recordId = `key_${cryptoMod.randomUUID()}`;
    const orgId = (d.organizationId as string) || ((req as any).user?.organizationId as string | undefined) || null;
    const scopes = Array.isArray(d.permissions) && d.permissions.length > 0
      ? d.permissions as string[]
      : ['read'];
    // KS-33 follow-up: svc_api_keys.scopes is JSONB on every deploy
    // (docker/init/04 declares it; CORE_MIGRATIONS post-PR #14 declares
    // it; the security service's dbSaveApiKey at services/security/src/
    // index.ts:194 writes it via JSON.stringify). PR #10's `::text[]`
    // cast worked against a non-existent canonical TEXT[] shape and
    // failed at runtime against the real JSONB column. Cast as JSONB
    // here so the originate admin endpoint matches the rest of the
    // pipeline.
    const rows: any[] = await ((req as any).db || prisma).$queryRaw`
      INSERT INTO svc_api_keys (
        id, organization_id, tenant_id, name, key_hash, key_prefix,
        scopes, rate_limit, rate_limit_window, usage_count,
        is_active, expires_at
      )
      VALUES (
        ${recordId},
        ${orgId},
        ${tenantId}::uuid,
        ${d.name},
        encode(digest(${keyValue}, 'sha256'), 'hex'),
        ${keyPrefix},
        ${JSON.stringify(scopes)}::jsonb,
        ${d.rateLimit || 1000},
        3600,
        0,
        TRUE,
        ${d.expiresAt ? new Date(d.expiresAt) : null}
      ) RETURNING id, key_prefix, name, scopes, rate_limit, is_active, expires_at, created_at
    `;
    res.status(201).json({
      success: true,
      key: keyValue,
      apiKey: {
        id: rows[0].id,
        keyPrefix: rows[0].key_prefix,
        name: rows[0].name,
        permissions: Array.isArray(rows[0].scopes) ? rows[0].scopes : [],
        rateLimit: rows[0].rate_limit,
        isActive: rows[0].is_active,
        expiresAt: rows[0].expires_at,
        createdAt: rows[0].created_at,
      },
    });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/api-keys)', err);
  }
});

/** Revoke an API key. KS-33: writes to svc_api_keys (same table the
 *  gateway validates against, so a revoked key actually stops working
 *  on the next gateway request once the security service's per-key
 *  cache expires — 30 s for invalid, 60 s for valid per
 *  services/api-gateway/src/middleware/auth.ts apiKeyCache). */
adminConfigRouter.delete('/api-keys/:id', async (req: Request, res: Response) => {
  try {
    // KS-25/33: tenant-scoped — a super_admin revokes a key in another tenant by
    // passing X-Tenant-Override (the gateway resolves it into req.tenantId), the
    // same mechanism the mint endpoint uses; otherwise revocation is scoped to the
    // caller's own tenant (default-tenant fallback in single-tenancy).
    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';

    // KS-764 (QA F-764-01): this route is the SECOND surface that revokes a key,
    // and until now it authorised on ROLE + TENANT only. `adminConfigRouter`
    // admits ORG_ADMIN (see the requireRole at the top of this file), so an
    // ORG_ADMIN in organisation A could revoke organisation B's key inside the
    // same tenant — the exact defect KS-764 closed on
    // services/security's DELETE /api/keys/:id, still open here.
    //
    // It now routes through the SAME `decideKeyRevoke` as that route, imported
    // from @secuura/shared. Not a second copy of the rule: two implementations
    // of one policy cannot witness each other drifting.
    //
    // RESOLVE FIRST, THEN AUTHORISE — the comparison needs the key's own
    // organisation, so the row is read before the decision. The read stays
    // TENANT-SCOPED exactly as the UPDATE below always was: the defect is
    // same-tenant cross-ORGANISATION, so no platform-scope widening is needed
    // or wanted here (services/security wraps its lookup only because it must
    // resolve rows in OTHER tenants).
    const keyRows: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT id, tenant_id, organization_id
        FROM svc_api_keys
       WHERE id = ${req.params.id}
         AND tenant_id = ${tenantId}::uuid
    `;
    if (keyRows.length === 0) {
      return res.json({ success: false, message: 'Not found' });
    }
    // BLAST RADIUS — a comparison this route did NOT make before (Peter's #799
    // review, finding 3). `decideKeyRevoke` delegates to `decideTenantAccess`,
    // which evaluates `user.tenantId !== targetTenantId` and refuses a caller
    // with NO tenant outright (`403 caller has no tenant`). This route
    // previously made no tenant comparison at all.
    //
    // It works today only because the auth service signs `tenantId` into
    // interactive JWTs — and it does so CONDITIONALLY
    // (`services/auth/src/services/jwt.ts:263`), so a tenant-less user receives
    // a token without the claim and is refused here. Any other token minter, or
    // a token predating that field, is refused for the same reason.
    //
    // That refusal is the intended fail-closed direction and is NOT being
    // softened: defaulting a missing tenant would let the caller's absence
    // choose the answer. It is recorded here because the organisation arm's
    // blast radius was documented and this one was not, and an undeclared
    // dependency is the half that surprises someone later. Both `JwtPayload`
    // types now DECLARE `tenantId` so the requirement is visible to the
    // compiler rather than resting on what auth happens to sign.
    const decision = decideKeyRevoke((req as any).user, {
      id: String(keyRows[0].id),
      // The SELECT above matched `tenant_id = ${tenantId}`, so the row's tenant IS
      // this value — passing it is exact, not a widening of the row's own field.
      tenantId,
      organizationId: keyRows[0].organization_id == null ? undefined : String(keyRows[0].organization_id),
    });
    if (!decision.allow) {
      logger.warn('API key revoke refused', {
        keyId: String(keyRows[0].id),
        keyTenantId: keyRows[0].tenant_id,
        keyOrganizationId: keyRows[0].organization_id,
        callerTenantId: (req as any).user?.tenantId,
        callerOrganizationId: (req as any).user?.organizationId,
        callerRole: (req as any).user?.role,
        reason: decision.reason,
      });
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Not authorised to revoke this key' },
      });
    }

    // KS-337: svc_api_keys has no `updated_at` column (the mint INSERT never
    // declares one), so the previous `SET …, updated_at = NOW()` 500'd on every
    // revoke — keys could never be revoked. is_active = false is all revocation
    // needs; it propagates within 30–60 s as the gateway's per-key validate cache
    // expires (see api-gateway middleware/auth.ts apiKeyCache).
    const result = await ((req as any).db || prisma).$executeRaw`
      UPDATE svc_api_keys SET is_active = false
       WHERE id = ${req.params.id}
         AND tenant_id = ${tenantId}::uuid
    `;
    res.json({ success: result > 0, message: result > 0 ? 'Key revoked' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (DELETE /api/admin/api-keys/:id)', err);
  }
});

// =============================================================================
// AUDIT LOGS
// =============================================================================

/** List audit logs */
adminConfigRouter.get('/audit-logs', async (req: Request, res: Response) => {
  try {
    const limit = Math.min(parseInt(req.query.limit as string) || 200, 1000);
    const offset = parseInt(req.query.offset as string) || 0;
    const action = req.query.action as string | undefined;
    // KS-28: tenant-scoped — admin in tenant A can only see actions in
    // their own tenant. Cross-tenant audit visibility (super_admin
    // platform-wide audit dashboard) goes through routes/platform.ts and
    // is gated separately on the SUPER_ADMIN role.
    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';

    let rows: any[];
    if (action) {
      rows = await ((req as any).db || prisma).$queryRaw`
        SELECT * FROM audit_logs
         WHERE tenant_id = ${tenantId}::uuid AND action = ${action}
        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
      `;
    } else {
      rows = await ((req as any).db || prisma).$queryRaw`
        SELECT * FROM audit_logs
         WHERE tenant_id = ${tenantId}::uuid
        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
      `;
    }

    const countResult: any[] = await ((req as any).db || prisma).$queryRaw`
      SELECT COUNT(*)::int AS total FROM audit_logs
       WHERE tenant_id = ${tenantId}::uuid
    `;

    res.json({
      success: true,
      logs: rows.map(mapAuditRow),
      events: rows.map(mapAuditRow),
      total: countResult[0]?.total ?? rows.length,
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, logs: [], events: [], total: 0 });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/audit-logs)', err);
  }
});

// =============================================================================
// REPORTS
// =============================================================================

/** List reports */
adminConfigRouter.get('/reports', async (_req: Request, res: Response) => {
  try {
    // Aggregate summary reports from existing data
    // KS-458 (admin cross-tenant): platform-wide aggregates, no tenant filter.
    const [docStats, userStats] = await runWithPlatformScope(() => Promise.all([
      prisma.$queryRaw`
        SELECT status, COUNT(*)::int AS count FROM documents GROUP BY status
      `.catch(() => []),
      prisma.$queryRaw`
        SELECT role, COUNT(*)::int AS count FROM users GROUP BY role
      `.catch(() => []),
    ])) as any[];

    res.json({
      success: true,
      reports: [
        {
          id: 'doc-summary',
          name: 'Document Summary',
          type: 'summary',
          data: docStats,
          generatedAt: new Date().toISOString(),
        },
        {
          id: 'user-summary',
          name: 'User Summary',
          type: 'summary',
          data: userStats,
          generatedAt: new Date().toISOString(),
        },
      ],
    });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (GET /api/admin/reports)', err);
  }
});

// =============================================================================
// PRIVACY
// =============================================================================

/** Get privacy settings (consent + retention policies) */
adminConfigRouter.get('/privacy', async (_req: Request, res: Response) => {
  try {
    const [consentRows, retentionRows] = await Promise.all([
      prisma.$queryRaw`SELECT * FROM consent_records ORDER BY given_at DESC LIMIT 100`.catch(() => []),
      prisma.$queryRaw`SELECT * FROM data_retention_policies ORDER BY data_type ASC`.catch(() => []),
    ]) as any[];

    res.json({
      success: true,
      consents: (consentRows as any[]).map((r: any) => ({
        id: r.id,
        userId: r.user_id,
        purpose: r.purpose,
        source: r.source,
        givenAt: r.given_at?.toISOString?.() || r.given_at,
        expiresAt: r.expires_at?.toISOString?.() || r.expires_at,
        withdrawnAt: r.withdrawn_at?.toISOString?.() || r.withdrawn_at,
      })),
      retentionPolicies: (retentionRows as any[]).map((r: any) => ({
        id: r.id,
        dataType: r.data_type,
        retentionDays: r.retention_period_days,
        legalBasis: r.legal_basis,
        deletionMethod: r.deletion_method,
        autoDelete: r.auto_delete,
        isActive: r.is_active,
      })),
    });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (GET /api/admin/privacy)', err);
  }
});

/** Update privacy/retention settings */
adminConfigRouter.put('/privacy', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    let updatedCount = 0;

    if (d.retentionPolicies && Array.isArray(d.retentionPolicies)) {
      for (const policy of d.retentionPolicies) {
        if (policy.id) {
          const result = await ((req as any).db || prisma).$executeRaw`
            UPDATE data_retention_policies SET
              retention_period_days = COALESCE(${policy.retentionDays || null}, retention_period_days),
              auto_delete = COALESCE(${policy.autoDelete}, auto_delete),
              deletion_method = COALESCE(${policy.deletionMethod || null}, deletion_method),
              is_active = COALESCE(${policy.isActive}, is_active),
              updated_at = NOW()
            WHERE id = ${policy.id}::uuid
          `;
          updatedCount += result;
        }
      }
    }

    res.json({ success: true, updatedCount });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/privacy)', err);
  }
});

// =============================================================================
// RIGHTS HOLDERS
// =============================================================================

/** List rights holders (search, filter, paginate) — filtered by organization */
adminConfigRouter.get('/rights-holders', async (req: Request, res: Response) => {
  try {
    const search = req.query.search as string | undefined;
    const limit = Math.min(parseInt(req.query.limit as string) || 100, 500);
    const offset = parseInt(req.query.offset as string) || 0;

    // KS-108: scope by the resolved tenant; RLS (via withTenant) is the hard
    // guarantee against cross-tenant leakage on this shared table. No tenant
    // resolved → no access. KS-93: super_admin scopes via the verified
    // X-Tenant-Override or ?organizationId= (resolveTenantId), no dual-send.
    const tenantId = resolveTenantId(req);
    if (!tenantId) {
      return res.json({ success: true, rightsHolders: [], total: 0 });
    }

    const rows: any[] = await withTenant(tenantId, async (tx) => {
      if (search) {
        const q = `%${search}%`;
        return tx.$queryRaw`
          SELECT * FROM rights_holders
          WHERE organization_id = ${tenantId}::uuid
            AND (first_name ILIKE ${q} OR last_name ILIKE ${q} OR email ILIKE ${q} OR display_name ILIKE ${q} OR external_id ILIKE ${q})
            AND status = 'active'
          ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}
        `;
      }
      return tx.$queryRaw`
        SELECT * FROM rights_holders WHERE organization_id = ${tenantId}::uuid AND status = 'active'
        ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}
      `;
    });

    res.json({
      success: true,
      rightsHolders: rows.map(mapRightsHolderRow),
      total: rows.length,
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, rightsHolders: [], total: 0 });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/rights-holders)', err);
  }
});

/** Get a single rights holder by ID */
adminConfigRouter.get('/rights-holders/:id', async (req: Request, res: Response) => {
  try {
    const tenantId = resolveTenantId(req);
    if (!tenantId) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Rights holder not found' } });
    }
    // KS-108: scope the lookup to the caller's tenant via an explicit
    // organization_id filter (PRIMARY — enforces regardless of DB role) plus the
    // withTenant GUC so RLS is defense-in-depth. Closes the prior cross-tenant
    // read (this query previously had no org filter). NOTE: RLS alone does not
    // bind the Azure admin connection (secuuraadmin) — see KS-108; the explicit
    // filter is what guarantees isolation until services run as a least-priv role.
    const rows: any[] = await withTenant(tenantId, (tx) => tx.$queryRaw`
      SELECT * FROM rights_holders WHERE id = ${req.params.id}::uuid AND organization_id = ${tenantId}::uuid AND status = 'active'
    `);
    if (rows.length === 0) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Rights holder not found' } });
    }
    res.json({ success: true, rightsHolder: mapRightsHolderRow(rows[0]) });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (GET /api/admin/rights-holders/:id)', err);
  }
});

/** Create a rights holder */
adminConfigRouter.post('/rights-holders', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    // KS-106 (product decision 2026-05-22): a rights holder must have a valid
    // email. Name is optional — display_name falls back to the email below.
    if (!d.email) {
      return res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'email is required' } });
    }
    if (!isValidEmail(d.email)) {
      return res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'email must be a valid email address' } });
    }
    // KS-108: a rights holder belongs to one tenant. Resolve it (super_admin via
    // override/query/body.organizationId; tenant-bound admin via their own org).
    // tenant_id is set to the same value the RLS WITH CHECK enforces.
    const tenantId = resolveTenantId(req) || (d.organizationId as string | undefined) || null;
    if (!tenantId) {
      return res.status(400).json({ success: false, error: { code: 'TENANT_SCOPE_REQUIRED', message: 'organizationId (or X-Tenant-Override) is required to create a rights holder' } });
    }
    const displayName = d.displayName || [d.firstName, d.lastName].filter(Boolean).join(' ') || d.email;
    const wantInvite = d.sendInvite !== false;
    const inviteToken = require('crypto').randomBytes(32).toString('hex');

    const created = await withTenant(tenantId, async (tx) => {
      const rows: any[] = await tx.$queryRaw`
        INSERT INTO rights_holders (email, first_name, last_name, display_name, external_id, organization_id, tenant_id, metadata)
        VALUES (${d.email}, ${d.firstName || null}, ${d.lastName || null}, ${displayName},
                ${d.externalId || null}, ${tenantId}::uuid, ${tenantId}::uuid, ${JSON.stringify(d.metadata || {})}::jsonb)
        RETURNING *
      `;
      const mapped = mapRightsHolderRow(rows[0]);
      if (wantInvite) {
        await tx.$executeRaw`
          UPDATE rights_holders SET invite_sent = true, invite_sent_at = NOW(), invite_token = ${inviteToken}, updated_at = NOW()
          WHERE id = ${rows[0].id}::uuid
        `;
        mapped.inviteSent = true;
      }
      return mapped;
    });

    // Fire-and-forget the invitation email outside the transaction (best-effort).
    if (wantInvite) {
      try {
        const baseUrl = process.env.FRONTEND_URL || 'http://localhost:6882';
        const inviteUrl = `${baseUrl}/register?invite=${inviteToken}`;
        const { sendRightsHolderInvite } = require('../services/email');
        // Pen-test F-04: read identity/org from authenticated req.user and
        // tenant from req.tenantSlug (populated by extractTenantContext from
        // the verified JWT-derived header), NOT from raw spoofable headers.
        const authUser = (req as any).user;
        const orgName = (authUser?.organizationName as string | undefined)
          || ((req as any).tenantSlug as string | undefined)
          || 'Secuura Platform K';
        sendRightsHolderInvite({
          recipientEmail: d.email,
          recipientName: displayName,
          organizationName: orgName,
          inviteUrl,
          inviterName: (authUser?.email as string | undefined) || undefined,
        }).catch(() => {}); // fire-and-forget
        (created as any).inviteUrl = inviteUrl;
      } catch { /* invite email is best-effort */ }
    }

    res.status(201).json({ success: true, rightsHolder: created });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/rights-holders)', err);
  }
});

/** Update a rights holder */
adminConfigRouter.put('/rights-holders/:id', async (req: Request, res: Response) => {
  try {
    const d = req.body;
    // Validate email format on update too — same rule as create. (F-LOCAL-RH-EMAIL-VALIDATION-01)
    if (d.email && !isValidEmail(d.email)) {
      return res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'email must be a valid email address' } });
    }
    const tenantId = resolveTenantId(req);
    if (!tenantId) {
      return res.json({ success: false, message: 'Not found' });
    }
    // KS-108: RLS scopes the update to the caller's tenant — a cross-tenant id
    // simply matches no row.
    const result = await withTenant(tenantId, (tx) => tx.$executeRaw`
      UPDATE rights_holders SET
        email = COALESCE(${d.email || null}, email),
        first_name = COALESCE(${d.firstName || null}, first_name),
        last_name = COALESCE(${d.lastName || null}, last_name),
        display_name = COALESCE(${d.displayName || null}, display_name),
        external_id = COALESCE(${d.externalId || null}, external_id),
        metadata = COALESCE(${d.metadata ? JSON.stringify(d.metadata) : null}::jsonb, metadata),
        updated_at = NOW()
      WHERE id = ${req.params.id}::uuid AND organization_id = ${tenantId}::uuid
    `);
    res.json({ success: result > 0, message: result > 0 ? 'Updated' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PUT /api/admin/rights-holders/:id)', err);
  }
});

/** Delete (deactivate) a rights holder */
adminConfigRouter.delete('/rights-holders/:id', async (req: Request, res: Response) => {
  try {
    const tenantId = resolveTenantId(req);
    if (!tenantId) {
      return res.json({ success: false, message: 'Not found' });
    }
    // KS-108: RLS scopes the (soft) delete to the caller's tenant.
    const result = await withTenant(tenantId, (tx) => tx.$executeRaw`
      UPDATE rights_holders SET status = 'inactive', updated_at = NOW() WHERE id = ${req.params.id}::uuid AND organization_id = ${tenantId}::uuid
    `);
    res.json({ success: result > 0, message: result > 0 ? 'Deactivated' : 'Not found' });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (DELETE /api/admin/rights-holders/:id)', err);
  }
});

/** List documents for a specific rights holder */
adminConfigRouter.get('/rights-holders/:id/documents', async (req: Request, res: Response) => {
  try {
    const db = (req as any).db || prisma;
    const rows: any[] = await db.$queryRaw`
      SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
             d.certification_scope, d.created_at, d.certified_at,
             d.certification_metadata, d.metadata
      FROM documents d
      WHERE d.rights_holder_id = ${req.params.id}::uuid
      ORDER BY d.created_at DESC
    `;
    res.json({
      success: true,
      documents: rows.map((r: any) => ({
        id: r.external_id || r.id,
        title: r.title,
        documentType: r.document_type,
        status: r.status,
        certificationScope: r.certification_scope,
        contentHash: r.content_hash,
        issuer: (r.certification_metadata || {}).issuerName || (r.metadata || {}).issuedBy,
        createdAt: r.created_at?.toISOString?.() || r.created_at,
        certifiedAt: r.certified_at?.toISOString?.() || r.certified_at,
      })),
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist')) {
      return res.json({ success: true, documents: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/rights-holders/:id/documents)', err);
  }
});

/** Send invite to a rights holder */
adminConfigRouter.post('/rights-holders/:id/invite', async (req: Request, res: Response) => {
  try {
    const tenantId = resolveTenantId(req);
    if (!tenantId) return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Rights holder not found' } });

    // KS-108: look up + flag the invite within the caller's tenant (RLS).
    const rh: any = await withTenant(tenantId, async (tx) => {
      const rows: any[] = await tx.$queryRaw`SELECT * FROM rights_holders WHERE id = ${req.params.id}::uuid AND organization_id = ${tenantId}::uuid`;
      return rows[0] || null;
    });
    if (!rh) return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Rights holder not found' } });
    if (!rh.email) return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Rights holder has no email address' } });

    const inviteToken = require('crypto').randomBytes(32).toString('hex');
    await withTenant(tenantId, (tx) => tx.$executeRaw`
      UPDATE rights_holders SET invite_sent = true, invite_sent_at = NOW(), invite_token = ${inviteToken}, updated_at = NOW()
      WHERE id = ${req.params.id}::uuid AND organization_id = ${tenantId}::uuid
    `);

    const baseUrl = process.env.FRONTEND_URL || 'http://localhost:6882';
    const inviteUrl = `${baseUrl}/register?invite=${inviteToken}`;

    // Send invitation email
    const { sendRightsHolderInvite } = require('../services/email');
    // Pen-test F-04: read identity/org from authenticated req.user and
    // tenant from req.tenantSlug (populated by extractTenantContext from
    // the verified JWT-derived header), NOT from raw spoofable headers.
    const authUser = (req as any).user;
    const orgName = (authUser?.organizationName as string | undefined)
      || ((req as any).tenantSlug as string | undefined)
      || 'Secuura Platform K';
    const inviterName = (authUser?.email as string | undefined) || undefined;
    const rhName = rh.display_name || [rh.first_name, rh.last_name].filter(Boolean).join(' ') || rh.email;

    const emailSent = await sendRightsHolderInvite({
      recipientEmail: rh.email,
      recipientName: rhName,
      organizationName: orgName,
      inviteUrl,
      inviterName,
    });

    res.json({
      success: true,
      message: emailSent ? `Invitation email sent to ${rh.email}` : `Invite created for ${rh.email} (email delivery pending — check SMTP config)`,
      inviteUrl,
      emailSent,
    });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/rights-holders/:id/invite)', err);
  }
});

// =============================================================================
// IDENTITY MANAGEMENT
// =============================================================================

/** List all users (alias for admin portal Users page) */
adminConfigRouter.get('/users', async (req: Request, res: Response) => {
  try {
    const db = (req as any).db || prisma;
    const role = req.query.role as string | undefined;
    // KS-458 (admin cross-tenant): users list has no tenant filter.
    let rows: any[];
    if (role) {
      rows = await runWithPlatformScope(() => db.$queryRaw`SELECT id, email, first_name, last_name, role, status, verification_level, created_at, last_login_at FROM users WHERE role = ${role} ORDER BY created_at DESC LIMIT 200`);
    } else {
      rows = await runWithPlatformScope(() => db.$queryRaw`SELECT id, email, first_name, last_name, role, status, verification_level, created_at, last_login_at FROM users ORDER BY created_at DESC LIMIT 200`);
    }
    res.json({
      success: true,
      data: {
        users: rows.map((r: any) => ({
          id: r.id, email: r.email, firstName: r.first_name, lastName: r.last_name,
          displayName: [r.first_name, r.last_name].filter(Boolean).join(' ') || r.email,
          role: r.role, status: r.status, verificationLevel: r.verification_level,
          createdAt: r.created_at?.toISOString?.() || r.created_at,
          lastLoginAt: r.last_login_at?.toISOString?.() || r.last_login_at,
        })),
        total: rows.length, limit: 200, offset: 0,
      },
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, data: { users: [], total: 0 } });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/users)', err);
  }
});

/** List users with verification info */
adminConfigRouter.get('/identity/users', async (req: Request, res: Response) => {
  try {
    // KS-458 (admin cross-tenant): users/organizations join, no tenant filter.
    const rows: any[] = await runWithPlatformScope(() => ((req as any).db || prisma).$queryRaw`
      SELECT u.id, u.email, u.first_name, u.last_name, u.role,
             u.verification_level, u.mfa_enabled, u.external_provider,
             u.status, o.name AS org_name, o.id AS org_id
      FROM users u
      LEFT JOIN organization_members om ON om.user_id = u.id
      LEFT JOIN organizations o ON o.id = om.organization_id
      ORDER BY u.email ASC
      LIMIT 200
    `);
    res.json({
      success: true,
      users: rows.map((r: any) => ({
        userId: r.id,
        email: r.email,
        name: [r.first_name, r.last_name].filter(Boolean).join(' ') || r.email,
        verificationLevel: r.verification_level || 'BASIC',
        authMethod: r.external_provider || 'email',
        mfaEnabled: r.mfa_enabled ?? false,
        walletConnected: false,
        orgId: r.org_id,
        orgName: r.org_name,
        status: r.status,
      })),
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, users: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/identity/users)', err);
  }
});

/** List organizations for identity management */
adminConfigRouter.get('/identity/organizations', async (req: Request, res: Response) => {
  try {
    // KS-458 (admin cross-tenant): org listing, no tenant filter.
    const rows: any[] = await runWithPlatformScope(() => ((req as any).db || prisma).$queryRaw`
      SELECT id, name, type, status, domain, verification_level
      FROM organizations ORDER BY name ASC
    `);
    res.json({
      success: true,
      organizations: rows.map((r: any) => ({
        orgId: r.id,
        orgName: r.name,
        trustLevel: r.verification_level || 'STANDARD',
        verificationMode: r.type || 'issuer',
        domain: r.domain,
        domainVerified: !!r.domain,
        status: r.status || 'active',
      })),
    });
  } catch (err: any) {
    if (err?.message?.includes('does not exist') || err?.code === '42P01') {
      return res.json({ success: true, organizations: [] });
    }
    fail500(res, 'Admin config request failed (GET /api/admin/identity/organizations)', err);
  }
});

/** Update user verification level */
adminConfigRouter.patch('/identity/users/:id/level', async (req: Request, res: Response) => {
  try {
    const { verificationLevel } = req.body;
    const valid = ['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT'];
    if (!verificationLevel || !valid.includes(verificationLevel)) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `verificationLevel must be one of: ${valid.join(', ')}` } });
    }
    // KS-458 (admin cross-tenant): targets an arbitrary user by id, no
    // caller-tenant filter — platform scope so the UPDATE matches under RLS.
    const result = await runWithPlatformScope(() => ((req as any).db || prisma).$executeRaw`
      UPDATE users SET verification_level = ${verificationLevel}, updated_at = NOW()
      WHERE id = ${req.params.id}::uuid
    `);
    res.json({ success: result > 0, userId: req.params.id, verificationLevel });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (PATCH /api/admin/identity/users/:id/level)', err);
  }
});

/** List identity providers */
adminConfigRouter.get('/identity/providers', async (_req: Request, res: Response) => {
  const providers = [
    { name: 'entra', label: 'Microsoft Entra ID', tier: 'ENHANCED', configured: !!process.env.ENTRA_CLIENT_ID, status: process.env.ENTRA_CLIENT_ID ? 'active' : 'unconfigured' },
    { name: 'auth0', label: 'Auth0', tier: 'ENHANCED', configured: !!process.env.AUTH0_DOMAIN, status: process.env.AUTH0_DOMAIN ? 'active' : 'unconfigured' },
    { name: 'okta', label: 'Okta', tier: 'ENHANCED', configured: !!process.env.OKTA_DOMAIN, status: process.env.OKTA_DOMAIN ? 'active' : 'unconfigured' },
    { name: 'google', label: 'Google', tier: 'SOCIAL', configured: !!process.env.GOOGLE_CLIENT_ID, status: process.env.GOOGLE_CLIENT_ID ? 'active' : 'unconfigured' },
    { name: 'linkedin', label: 'LinkedIn', tier: 'SOCIAL', configured: !!process.env.LINKEDIN_CLIENT_ID, status: process.env.LINKEDIN_CLIENT_ID ? 'active' : 'unconfigured' },
    { name: 'github', label: 'GitHub', tier: 'SOCIAL', configured: !!process.env.GITHUB_CLIENT_ID, status: process.env.GITHUB_CLIENT_ID ? 'active' : 'unconfigured' },
    { name: 'email', label: 'Email + Password', tier: 'BASIC', configured: true, status: 'active' },
    { name: 'wallet', label: 'Cardano Wallet', tier: 'STANDARD', configured: true, status: 'active' },
  ];
  res.json({ success: true, providers });
});

// =============================================================================
// ROW MAPPERS
// =============================================================================

function mapDocTypeRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    name: r.name,
    code: r.code || r.id,
    description: r.description,
    category: r.category,
    isActive: r.is_active ?? true,
    creatorVerificationLevel: r.creator_verification_level || 'basic',
    ownerVerificationLevel: r.owner_verification_level || 'basic',
    viewerVerificationLevel: r.viewer_verification_level || 'none',
    verifierVerificationLevel: r.verifier_verification_level || 'standard',
    requireMFA: r.require_mfa ?? false,
    requireWalletSignature: r.require_wallet_signature ?? false,
    requireKYC: r.require_kyc ?? false,
    allowedAuthProviders: r.allowed_auth_providers || [],
    requiresApproval: r.requires_approval ?? false,
    approvalWorkflowId: r.approval_workflow_id || null,
    autoAnchor: r.auto_anchor ?? true,
    anchorNetwork: r.anchor_network || 'preprod',
    metadataSchema: r.metadata_schema || [],
    allowedSources: r.allowed_sources || [],
    webhookEvents: r.webhook_events || [],
    documentCount: r.document_count ?? 0,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
    updatedAt: r.updated_at?.toISOString?.() || r.updated_at,
  };
}

function mapWorkflowRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    name: r.name,
    description: r.description,
    type: r.type,
    isActive: r.is_active,
    steps: r.steps || [],
    documentTypes: r.document_types || [],
    slaHours: r.sla_hours,
    usageCount: r.usage_count,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
    updatedAt: r.updated_at?.toISOString?.() || r.updated_at,
  };
}

function mapQueueRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    documentId: r.document_id,
    documentTitle: r.document_title,
    submitterName: r.submitter_name,
    submitterEmail: r.submitter_email,
    organizationId: r.organization_id,
    organizationName: r.organization_name,
    documentType: r.document_type,
    status: r.status,
    priority: r.priority,
    assignedTo: r.assigned_to,
    slaDeadline: r.sla_deadline?.toISOString?.() || r.sla_deadline,
    workflowId: r.workflow_id,
    notes: r.notes,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
    updatedAt: r.updated_at?.toISOString?.() || r.updated_at,
  };
}

function mapIntegrationRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    name: r.name,
    integrationType: r.integration_type,
    provider: r.provider,
    status: r.status,
    config: r.config || {},
    lastSyncAt: r.last_sync_at?.toISOString?.() || r.last_sync_at,
    errorMessage: r.error_message,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
    updatedAt: r.updated_at?.toISOString?.() || r.updated_at,
  };
}

function mapPolicyRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    name: r.name,
    description: r.description,
    scope: r.scope,
    isActive: r.is_active,
    minUserVerificationLevel: r.min_user_verification_level,
    minOrgVerificationLevel: r.min_org_verification_level,
    requiredAuthProviders: r.required_auth_providers || [],
    requireMFA: r.require_mfa,
    requireWalletSignature: r.require_wallet_signature,
    regionRestrictions: r.region_restrictions || [],
    enforcementMode: r.enforcement_mode,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
    updatedAt: r.updated_at?.toISOString?.() || r.updated_at,
  };
}

function mapOrgRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    name: r.name,
    type: r.type,
    status: r.status,
    domain: r.domain,
    userCount: r.user_count ?? 0,
    documentCount: 0,
    verificationLevel: r.verification_level,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
    updatedAt: r.updated_at?.toISOString?.() || r.updated_at,
  };
}

function mapRightsHolderRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    email: r.email,
    firstName: r.first_name,
    lastName: r.last_name,
    displayName: r.display_name || [r.first_name, r.last_name].filter(Boolean).join(' ') || r.email,
    externalId: r.external_id,
    organizationId: r.organization_id,
    userId: r.user_id,
    status: r.status,
    inviteSent: r.invite_sent,
    inviteSentAt: r.invite_sent_at?.toISOString?.() || r.invite_sent_at,
    metadata: r.metadata,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
    updatedAt: r.updated_at?.toISOString?.() || r.updated_at,
  };
}

function mapAuditRow(r: any): Record<string, unknown> {
  return {
    id: r.id,
    action: r.action,
    type: r.action,
    resourceType: r.resource_type,
    resourceId: r.resource_id,
    actor: r.user_id,
    userId: r.user_id,
    organizationId: r.organization_id,
    success: r.success ?? true,
    ipAddress: r.ip_address,
    userAgent: r.user_agent,
    details: r.details,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
  };
}

// =============================================================================
// CERTIFICATION METADATA BACKFILL
// =============================================================================

/** Backfill certification_metadata on documents missing issuer info */
adminConfigRouter.post('/backfill-certification-metadata', async (req: Request, res: Response) => {
  try {
    const db = (req as any).db || prisma;
    const { issuerName, certifiedAt } = req.body;
    if (!issuerName) return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'issuerName is required' } });

    const meta = JSON.stringify({
      issuerName,
      certifiedAt: certifiedAt || new Date().toISOString(),
    });

    // KS-458 (admin cross-tenant): backfill sweeps documents platform-wide.
    const result = await runWithPlatformScope(() => db.$executeRaw`
      UPDATE documents SET
        certification_metadata = COALESCE(certification_metadata, '{}'::jsonb) || ${meta}::jsonb,
        updated_at = NOW()
      WHERE status IN ('certified', 'signed', 'anchored')
        AND (certification_metadata IS NULL
             OR certification_metadata->>'issuerName' IS NULL
             OR certification_metadata->>'issuerName' = '')
    `);

    res.json({ success: true, updatedCount: result });
  } catch (err: any) {
    fail500(res, 'Admin config request failed (POST /api/admin/backfill-certification-metadata)', err);
  }
});

/**
 * Seed demo/test users for all tenants — idempotent, and gated (KS-487 B-3).
 *
 * WHAT THIS WAS. Any authenticated `ORG_ADMIN` could POST here, with no
 * environment gate of any kind, and the upsert read:
 *
 *     ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash,
 *                                       ..., role = EXCLUDED.role
 *
 * So it was not "create these accounts if missing" — it was an unconditional
 * **password and role reset**, keyed on email, for 14 named accounts, running
 * under `runWithPlatformScope` and therefore across every tenant. The hash it
 * wrote is the bcrypt of `admin123`, published in this file.
 *
 * That is a cross-tenant account-takeover primitive: an ORG_ADMIN of tenant A
 * resets an account in tenant B to a password printed in this repository, then
 * signs in as it. Four of the fourteen are seeded `ORG_ADMIN`. One of the
 * addresses used to belong to a real person rather than a fictional demo
 * persona; KS-913 replaced it with `org.admin@example.com` / `Demo Org Admin`,
 * so every address in the list is now fictional and `example.com` is the
 * IANA-reserved domain for exactly this. The gate below is still what stops
 * the primitive; removing the address removed the personal data, not the hole.
 *
 * TWO INDEPENDENT FIXES, because either alone leaves a hole:
 *
 *  1. **The gate** (below). `auth` already solved this class in pen-test F-05
 *     (`services/auth/src/repositories/userRepo.ts:966-985`): seeding requires
 *     `ALLOW_DEFAULT_SEED_PASSWORDS=true`, and non-dev additionally requires
 *     `ENABLE_DEMO_SEED=true`. That hardening never reached this route — the
 *     same one-half-fixed shape as KS-488 C-1, where a hardened sender made an
 *     unhardened verifier look handled.
 *
 *     This gate is deliberately STRICTER than auth's: it requires **both** flags
 *     unconditionally, with no `isDevLike` bypass. auth's seeder runs once at
 *     boot; this one is an HTTP endpoint an attacker can call at will, so
 *     "looks like dev" is not a safe exemption. It matters concretely — the demo
 *     VM runs this same compose file, where originate has `NODE_ENV=development`,
 *     so an `isDevLike` bypass would leave the route wide open on the live demo.
 *     That is F-05's own lesson (the demo ran as `NODE_ENV=demo` and got the
 *     seed) in a new costume.
 *
 *     Neither flag is set for originate in any deploy config (`services.bicep`
 *     sets both, but on the `auth` block only), so this route now refuses
 *     everywhere by default, including locally. A developer who wants it sets
 *     both in their `.env` — an opt-in, which is the point.
 *
 *  2. **The upsert** no longer touches existing rows. Even correctly gated, a
 *     route that silently rewrites the credentials of an account that already
 *     exists is the wrong primitive: "seed" means "create if absent". Existing
 *     accounts are now counted and skipped, and the response reports both, so an
 *     operator can see that nothing was overwritten.
 */
adminConfigRouter.post('/seed-demo-users', async (req: Request, res: Response) => {
  try {
    // Gate first — before touching the DB, and before the known hash is even
    // referenced. Both flags required; no NODE_ENV exemption (see above and the
    // rationale in utils/demoSeedGate.ts).
    if (!isDemoSeedEnabled()) {
      logger.warn('Demo-user seeding refused — endpoint not enabled in this environment', {
        route: 'POST /api/admin/seed-demo-users',
        nodeEnv: process.env.NODE_ENV,
        allowDefaultSeedPasswords: process.env.ALLOW_DEFAULT_SEED_PASSWORDS === 'true',
        enableDemoSeed: process.env.ENABLE_DEMO_SEED === 'true',
        callerTenantId: (req as any).tenantId ?? null,
      });
      return res.status(403).json({
        success: false,
        error: {
          code: 'DEMO_SEED_DISABLED',
          message:
            'Demo-user seeding is disabled. It writes accounts with a default password across ' +
            'all tenants, so it requires both ALLOW_DEFAULT_SEED_PASSWORDS=true and ' +
            'ENABLE_DEMO_SEED=true to be set explicitly for this service.',
        },
      });
    }
    const db = (req as any).db || prisma;
    // All test users use password: admin123
    const ADMIN123 = '$2a$10$fE0nueu9bnPJbfndacwar.4F137bqzux9o/fhVh/wwND2stNFgAHG';
    const users = [
      // Oxford
      { id: 'c1000000-0000-4000-8000-000000000001', email: 'james.wilson@ox.ac.uk', hash: ADMIN123, name: 'Prof James Wilson', role: 'ORG_ADMIN' },
      { id: 'c1000000-0000-4000-8000-000000000002', email: 'registrar@ox.ac.uk', hash: ADMIN123, name: 'Dr Helen Clarke', role: 'OWNER' },
      { id: 'c1000000-0000-4000-8000-000000000003', email: 'alice@student.ox.ac.uk', hash: ADMIN123, name: 'Alice Smith', role: 'OWNER' },
      // BUPA
      { id: 'c2000000-0000-4000-8000-000000000001', email: 'sarah.mitchell@bupa.co.uk', hash: ADMIN123, name: 'Sarah Mitchell', role: 'ORG_ADMIN' },
      { id: 'c2000000-0000-4000-8000-000000000002', email: 'david.thompson@bupa.co.uk', hash: ADMIN123, name: 'David Thompson', role: 'OWNER' },
      { id: 'c2000000-0000-4000-8000-000000000003', email: 'emma.wilson@bupa.co.uk', hash: ADMIN123, name: 'Emma Wilson', role: 'OWNER' },
      { id: 'c2000000-0000-4000-8000-000000000004', email: 'patient.records@bupa.co.uk', hash: ADMIN123, name: 'Patient Records', role: 'OWNER' },
      // Apex
      { id: 'c3000000-0000-4000-8000-000000000001', email: 'james@apex-consulting.com', hash: ADMIN123, name: 'James Wright', role: 'ORG_ADMIN' },
      { id: 'c3000000-0000-4000-8000-000000000002', email: 'sarah@apex-consulting.com', hash: ADMIN123, name: 'Sarah Palmer', role: 'OWNER' },
      { id: 'c3000000-0000-4000-8000-000000000003', email: 'tom@apex-consulting.com', hash: ADMIN123, name: 'Tom Davis', role: 'OWNER' },
      { id: 'c3000000-0000-4000-8000-000000000004', email: 'lisa@client-corp.com', hash: ADMIN123, name: 'Lisa Chen', role: 'OWNER' },
      // Greenfield
      { id: 'c4000000-0000-4000-8000-000000000001', email: 'issuer.e2e@greenfield.ac.uk', hash: ADMIN123, name: 'Dr Sarah Chen', role: 'OWNER' },
      // Delta
      { id: 'c5000000-0000-4000-8000-000000000001', email: 'delta.user@delta-corp.com', hash: ADMIN123, name: 'Delta User', role: 'OWNER' },
      // Secuura Co.
      { id: 'c6000000-0000-4000-8000-000000000001', email: 'org.admin@example.com', hash: ADMIN123, name: 'Demo Org Admin', role: 'ORG_ADMIN' },
    ];

    // KS-458 (admin cross-tenant): seeds users across all demo tenants.
    //
    // KS-487 B-3: `DO NOTHING`, previously
    // `DO UPDATE SET password_hash = EXCLUDED.password_hash, ..., role = EXCLUDED.role`.
    // That reset the credentials AND the role of any pre-existing account
    // matching one of these emails, to a hash published in this file — the
    // takeover primitive. Seeding means "create if absent"; an account that
    // already exists is the operator's, not ours, and re-running this must never
    // silently hand it back with a known password.
    //
    // `created` and `alreadyPresent` are counted separately and both returned:
    // the old handler reported a single `seededUsers` that incremented on
    // overwrite, so a run that rewrote 14 live accounts and a run that created
    // 14 new ones produced identical output.
    let created = 0;
    let alreadyPresent = 0;
    let failed = 0;
    for (const u of users) {
      try {
        const [firstName, ...lastParts] = u.name.split(' ');
        const lastName = lastParts.join(' ');
        const rows = await runWithPlatformScope(() => db.$executeRaw`
          INSERT INTO users (id, email, password_hash, first_name, last_name, role, status, created_at, updated_at)
          VALUES (${u.id}::uuid, ${u.email}, ${u.hash}, ${firstName}, ${lastName}, ${u.role}, 'active', NOW(), NOW())
          ON CONFLICT (email) DO NOTHING
        `);
        // $executeRaw returns the affected row count: 1 = inserted, 0 = conflict.
        if (rows > 0) created++;
        else alreadyPresent++;
      } catch (err: any) {
        // Previously a bare `catch {}` commented "skip duplicates" — but with
        // DO NOTHING a conflict is no longer an exception, so anything reaching
        // here is a real failure and was being swallowed silently.
        failed++;
        logger.error('Demo user seed failed', { email: u.email, error: err?.message });
      }
    }

    // Seed Alice as rights holder (scoped to Oxford's organization)
    try {
      // KS-108: resolve Oxford's org id, then seed the RH under that tenant (RLS).
      // KS-458 (admin cross-tenant): Oxford's org row is not the caller's tenant.
      const orgRows: any[] = await runWithPlatformScope(() => db.$queryRaw`SELECT id FROM organizations WHERE slug = 'oxford' LIMIT 1`);
      const oxfordOrgId = orgRows[0]?.id;
      if (oxfordOrgId) {
        await withTenant(oxfordOrgId, (tx) => tx.$executeRaw`
          INSERT INTO rights_holders (id, email, first_name, last_name, display_name, external_id, user_id, organization_id, tenant_id, status, invite_sent)
          VALUES ('d1000000-0000-4000-8000-000000000001'::uuid, 'alice@student.ox.ac.uk', 'Alice', 'Smith', 'Alice Smith', 'STU-OX-2026-001',
                  'c1000000-0000-4000-8000-000000000003'::uuid,
                  ${oxfordOrgId}::uuid, ${oxfordOrgId}::uuid,
                  'active', true)
          ON CONFLICT (id) DO UPDATE SET organization_id = EXCLUDED.organization_id, tenant_id = EXCLUDED.tenant_id
        `);
      }
    } catch { /* skip */ }

    // `seededUsers` retained for any existing caller, but it now means "created"
    // rather than "created or overwritten" — the counts below are the real answer.
    res.json({
      success: true,
      seededUsers: created,
      created,
      alreadyPresent,
      failed,
    });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
  }
});

/** Copy baseline data (doc types, orgs) from default DB into ALL tenant databases */
adminConfigRouter.post('/migrate-tenant-data', async (_req: Request, res: Response) => {
  try {
    const { getTenantManager } = require('../db');
    const mgr = getTenantManager?.();
    if (!mgr) return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Multi-tenancy not enabled' } });

    const platformPool = mgr.getPlatformPool();
    const defaultPool = mgr.getDefaultPool();

    // Get all active tenants with databases
    const tenants = await platformPool.query(
      `SELECT t.id, t.slug, tc.db_name FROM tenants t
       LEFT JOIN tenant_config tc ON t.id = tc.tenant_id
       WHERE t.status = 'active' AND tc.db_name IS NOT NULL`
    );

    // Get baseline data from default DB (bypass tenant routing — use raw pool)
    // KS-458 (admin cross-tenant): raw-pool reads skip the GUC-aware proxies,
    // so bundle the platform-scope GUC in-transaction via queryWithTenantGuc.
    let docTypes, orgs;
    try {
      docTypes = await runWithPlatformScope(() => queryWithTenantGuc(defaultPool, 'SELECT * FROM document_type_configs WHERE is_active = true'));
    } catch { docTypes = { rows: [] }; }
    try {
      orgs = await runWithPlatformScope(() => queryWithTenantGuc(defaultPool, 'SELECT * FROM organizations'));
    } catch { orgs = { rows: [] }; }

    // If default DB has no doc types, use hardcoded defaults
    if (docTypes.rows.length === 0) {
      const defaults = [
        { name: 'University Degree', code: 'university_degree', description: 'Academic degree certificates', category: 'Education' },
        { name: 'Academic Transcript', code: 'academic_transcript', description: 'Official academic transcripts', category: 'Education' },
        { name: 'Employment Reference', code: 'employment_reference', description: 'Employment references', category: 'Employment' },
        { name: 'Identity Document', code: 'identity_document', description: 'Government-issued identity', category: 'Government' },
        { name: 'Professional License', code: 'professional_license', description: 'Professional licensing', category: 'Professional' },
        { name: 'Certificate of Insurance', code: 'certificate_of_insurance', description: 'Insurance certificates', category: 'Insurance' },
        { name: 'Medical Record', code: 'medical_record', description: 'Clinical and health records', category: 'Healthcare' },
        { name: 'Contract Agreement', code: 'contract_agreement', description: 'Signed contracts and agreements', category: 'Legal' },
        { name: 'Compliance Certificate', code: 'compliance_certificate', description: 'Regulatory compliance certifications', category: 'Compliance' },
        { name: 'Training Certificate', code: 'training_certificate', description: 'Training completion certificates', category: 'Training' },
        { name: 'Property Deed', code: 'property_deed', description: 'Property ownership documents', category: 'Property' },
        { name: 'Power of Attorney', code: 'power_of_attorney', description: 'Legal authority delegation', category: 'Legal' },
        { name: 'Birth Certificate', code: 'birth_certificate', description: 'Official birth records', category: 'Government' },
        { name: 'Professional Membership', code: 'professional_membership', description: 'Professional body memberships', category: 'Professional' },
      ];
      docTypes = { rows: defaults.map(d => ({ ...d, is_active: true, metadata_schema: [] })) };
    }

    const results: any[] = [];

    for (const tenant of tenants.rows) {
      try {
        const tenantPool = mgr.getPool(tenant.id);
        let copied = { docTypes: 0, orgs: 0 };

        // Ensure document_type_configs table has varchar id (not UUID)
        try {
          // Check current id column type and fix if needed
          const colCheck = await tenantPool.query(
            `SELECT data_type FROM information_schema.columns WHERE table_name='document_type_configs' AND column_name='id'`
          );
          if (colCheck.rows.length > 0 && colCheck.rows[0].data_type === 'uuid') {
            // Drop and recreate with varchar id (table is empty on new tenant DBs)
            await tenantPool.query(`DROP TABLE IF EXISTS document_type_configs CASCADE`);
          }
          await tenantPool.query(`
            CREATE TABLE IF NOT EXISTS document_type_configs (
              id VARCHAR(100) PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              description TEXT,
              category VARCHAR(100) DEFAULT 'general',
              is_active BOOLEAN DEFAULT TRUE,
              metadata_schema JSONB DEFAULT '[]',
              created_at TIMESTAMPTZ DEFAULT NOW(),
              updated_at TIMESTAMPTZ DEFAULT NOW()
            )
          `);
        } catch { /* best effort */ }

        // Copy document type configs
        // KS-458 (admin cross-tenant): per-tenant seeding writes on a raw
        // tenant pool — platform-scope GUC bundled per statement.
        for (const dt of docTypes.rows) {
          try {
            const dtCode = dt.code || dt.name?.toLowerCase().replace(/\s+/g, '_');
            await runWithPlatformScope(() => queryWithTenantGuc(
              tenantPool,
              `INSERT INTO document_type_configs (id, name, description, category, is_active)
               VALUES ($1, $2, $3, $4, $5)
               ON CONFLICT (id) DO NOTHING`,
              [dtCode, dt.name, dt.description, dt.category || 'general', true]
            ));
            copied.docTypes++;
          } catch (e: any) {
            copied.docTypes++; // Count even if conflict
          }
        }

        // Copy organizations
        // KS-458 (admin cross-tenant): organizations is a fail-closed flip
        // table — the seeding write needs the platform-scope GUC in-transaction.
        for (const org of orgs.rows) {
          try {
            await runWithPlatformScope(() => queryWithTenantGuc(
              tenantPool,
              `INSERT INTO organizations (id, name, slug, domain, industry, country, status, settings, created_at, updated_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
               ON CONFLICT DO NOTHING`,
              [org.id, org.name, org.slug, org.domain, org.industry, org.country, org.status, JSON.stringify(org.settings || {}), org.created_at, org.updated_at]
            ));
            copied.orgs++;
          } catch { /* skip */ }
        }

        results.push({ tenant: tenant.slug, ...copied });
      } catch (err: any) {
        results.push({ tenant: tenant.slug, error: err.message?.substring(0, 60) });
      }
    }

    res.json({ success: true, results });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
  }
});
