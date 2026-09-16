/**
 * Enforcement Pipeline — Verification Level + Document Type + Workflow
 *
 * Extracted from the API-gateway monolith (index.ts lines 1393-1576).
 * Handles doc-type resolution, verification-level gating, MFA / auth-provider
 * checks, metadata-schema validation, and approval-workflow instantiation.
 */

import * as redisService from './redis';

// -------------------------------------------------------------------------
// Types
// -------------------------------------------------------------------------

export interface UserPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  verificationLevel: string;
  authMethod?: string;
  mfaEnabled?: boolean;
  tenantId?: string;
  tenantSlug?: string;
}

export type EnforcementSuccess = { ok: true; docType: Record<string, unknown> };
export type EnforcementFailure = { ok: false; status: number; error: string; code: string };
export type EnforcementResult = EnforcementSuccess | EnforcementFailure;

export type WorkflowGated = { gated: true; response: Record<string, unknown> };
export type WorkflowNotGated = { gated: false };
export type WorkflowGateResult = WorkflowGated | WorkflowNotGated;

// -------------------------------------------------------------------------
// Constants
// -------------------------------------------------------------------------

export const VERIFICATION_LEVEL_ORDER = [
  'none',
  'basic',
  'social',
  'standard',
  'enhanced',
  'high',
  'government',
];

// -------------------------------------------------------------------------
// Helpers
// -------------------------------------------------------------------------

export function meetsVerificationLevel(userLevel: string, requiredLevel: string): boolean {
  const userIdx = VERIFICATION_LEVEL_ORDER.indexOf((userLevel || 'none').toLowerCase());
  const reqIdx = VERIFICATION_LEVEL_ORDER.indexOf((requiredLevel || 'none').toLowerCase());
  // KS-1176: a user level outside the order ranks as 'none'. A connector key carries
  // 'api_key' (middleware/auth.ts), which indexOf read as -1, and `-1 >= 0` failed even a
  // 'none' requirement, so every connector-key POST /api/documents on a 'none' type
  // (SSD_DOCUMENT) was refused 403. Ranking it as 'none' grants nothing an unauthenticated
  // caller does not already get (enforceDocumentTypeRules' no-user branch) and nothing
  // above 'none'. Known levels are unchanged; so is an unknown REQUIRED level (KS-1190).
  const userRank = userIdx === -1 ? 0 : userIdx;
  return userRank >= reqIdx;
}

/**
 * Fetch DocumentTypeConfig from Redis by code (e.g. 'DEGREE') or by ID.
 * Returns null if not found or doc type is inactive.
 */
export async function resolveDocumentType(typeRef: string): Promise<Record<string, unknown> | null> {
  // KS-501: defence in depth — a non-string reaching .toUpperCase() threw a
  // TypeError that escaped as an unhandled rejection and crashed the whole
  // gateway process. Callers validate first; this guard keeps the helper
  // total even if a new call site forgets.
  if (!typeRef || typeof typeRef !== 'string') return null;
  const ref = typeRef.toUpperCase();
  const allTypes = await redisService.getAllDocumentTypes();
  for (const dt of allTypes) {
    const obj = dt as Record<string, unknown>;
    if (obj.id === typeRef || (obj.code as string || '').toUpperCase() === ref) {
      return obj;
    }
  }
  return null;
}

// -------------------------------------------------------------------------
// Enforcement middleware
// -------------------------------------------------------------------------

/**
 * Enforcement middleware: validates document type rules before document creation.
 * Checks: isActive, verification level, MFA, auth providers, metadata schema.
 * Enriches the request with resolved docType for downstream use.
 */
export async function enforceDocumentTypeRules(
  body: Record<string, unknown>,
  user: UserPayload | undefined,
): Promise<EnforcementResult> {
  const typeRefRaw = body.documentType || body.type || '';
  // KS-501: `as string` was a compile-time cast, not a runtime coercion — a
  // truthy non-string documentType (123, [...], {...}) passed the falsy
  // guard and crashed the gateway at typeRef.toUpperCase() (unhandled
  // rejection → whole-process restart → a measured 66-operation 502
  // cascade). A non-string type reference is a caller error: reject 400.
  if (typeRefRaw && typeof typeRefRaw !== 'string') {
    return {
      ok: false,
      status: 400,
      error: 'documentType must be a string (a document-type code or id)',
      code: 'VALIDATION_ERROR',
    };
  }
  const typeRef = (typeRefRaw || '') as string;
  if (!typeRef) {
    return { ok: true, docType: {} };
  }

  const docType = await resolveDocumentType(typeRef);
  if (!docType) {
    // KS-388: documentType validates dynamically against the registered catalogue
    // (an admin-managed set — a static enum would fight the admin CRUD). When the
    // catalogue has registered types, an unknown documentType is a caller error;
    // when the catalogue is EMPTY (never seeded, or Redis TTL expiry), validation
    // is not configured and the historical pass-through stands — otherwise every
    // creation (including Platform-S's SSD_DOCUMENT) would 400 on a fresh boot.
    const registered = await redisService.getAllDocumentTypes();
    if (registered.length > 0) {
      return {
        ok: false,
        status: 400,
        error: `Unknown document type "${typeRef}" — not in the registered document-type catalogue (see GET /api/document-types)`,
        code: 'UNKNOWN_DOCUMENT_TYPE',
      };
    }
    return { ok: true, docType: {} };
  }

  if (docType.isActive === false) {
    return { ok: false, status: 403, error: `Document type "${docType.name}" is currently disabled`, code: 'DOC_TYPE_DISABLED' };
  }

  if (!user) {
    if (docType.creatorVerificationLevel && (docType.creatorVerificationLevel as string).toLowerCase() !== 'none') {
      return { ok: false, status: 401, error: 'Authentication required for this document type', code: 'AUTH_REQUIRED' };
    }
    return { ok: true, docType };
  }

  const requiredLevel = (docType.creatorVerificationLevel as string) || 'none';
  const userLevel = user.verificationLevel || 'none';
  if (!meetsVerificationLevel(userLevel, requiredLevel)) {
    return {
      ok: false, status: 403,
      error: `This document type requires ${requiredLevel.toUpperCase()} verification. Your current level is ${userLevel.toUpperCase()}.`,
      code: 'INSUFFICIENT_VERIFICATION_LEVEL',
    };
  }

  if (docType.requireMFA === true) {
    if (!user.mfaEnabled) {
      return { ok: false, status: 403, error: 'This document type requires Multi-Factor Authentication to be enabled on your account', code: 'MFA_REQUIRED' };
    }
  }

  const allowedProviders = docType.allowedAuthProviders as string[] | undefined;
  if (allowedProviders && allowedProviders.length > 0) {
    const userAuthMethod = (user.authMethod || 'email').toLowerCase();
    const allowed = allowedProviders.map(p => p.toLowerCase());
    if (!allowed.includes(userAuthMethod) && !allowed.includes('email') && !allowed.includes('any')) {
      return {
        ok: false, status: 403,
        error: `This document type requires authentication via: ${allowedProviders.join(', ')}. You are using: ${userAuthMethod}.`,
        code: 'AUTH_PROVIDER_NOT_ALLOWED',
      };
    }
  }

  const schema = docType.metadataSchema as Array<{ name: string; required: boolean }> | undefined;
  if (schema && schema.length > 0) {
    const metadata = (body.metadata || body.data || {}) as Record<string, unknown>;
    const missing: string[] = [];
    for (const field of schema) {
      if (field.required && (metadata[field.name] === undefined || metadata[field.name] === null || metadata[field.name] === '')) {
        missing.push(field.name);
      }
    }
    if (missing.length > 0) {
      return {
        ok: false, status: 400,
        error: `Missing required metadata fields: ${missing.join(', ')}`,
        code: 'MISSING_METADATA',
      };
    }
  }

  return { ok: true, docType };
}

// -------------------------------------------------------------------------
// Workflow gate
// -------------------------------------------------------------------------

/**
 * Workflow gate: if the resolved docType requires approval, create a workflow
 * instance and hold the document in pending_approval status.
 */
export async function createWorkflowInstanceIfRequired(
  docType: Record<string, unknown>,
  documentId: string,
  body: Record<string, unknown>,
  user: UserPayload | undefined,
): Promise<WorkflowGateResult> {
  const needsApproval = docType.requiresApproval === true;
  const workflowId = docType.approvalWorkflowId as string | null;

  if (!needsApproval || !workflowId) {
    return { gated: false };
  }

  const workflow = await redisService.getWorkflow(workflowId) as Record<string, unknown> | null;
  const steps = (workflow?.steps || []) as Array<Record<string, unknown>>;

  const instanceId = `wfi-${require('crypto').randomUUID()}`;
  const stepInstances = steps.map((step, idx) => ({
    id: `step-${instanceId}-${idx}`,
    stepIndex: idx,
    name: step.name || `Step ${idx + 1}`,
    type: step.type || 'approval',
    approverType: step.approverType || 'role',
    approverValue: step.approverValue || step.approvers || 'admin',
    requireComment: step.requireComment || false,
    status: idx === 0 ? 'pending' : 'waiting',
  }));

  const instance: Record<string, unknown> = {
    id: instanceId,
    workflowId,
    workflowName: (workflow?.name as string) || 'Approval Workflow',
    documentId,
    status: 'pending_approval',
    currentStepIndex: 0,
    steps: stepInstances,
    createdBy: user?.userId || 'unknown',
    createdAt: new Date().toISOString(),
  };

  await redisService.setWorkflowInstance(instanceId, instance);

  await redisService.setPendingDocument(documentId, {
    ...body,
    id: documentId,
    status: 'pending_approval',
    workflowInstanceId: instanceId,
    createdBy: user?.userId,
    createdAt: new Date().toISOString(),
  });

  return {
    gated: true,
    response: {
      id: documentId,
      type: (body.documentType || body.type || 'DOCUMENT') as string,
      status: 'pending_approval',
      title: body.title,
      contentHash: body.contentHash,
      requiresApproval: true,
      workflowInstance: {
        id: instanceId,
        workflowId,
        workflowName: instance.workflowName,
        status: 'pending_approval',
        currentStep: stepInstances[0] || null,
        totalSteps: stepInstances.length,
      },
      createdAt: instance.createdAt,
    },
  };
}
