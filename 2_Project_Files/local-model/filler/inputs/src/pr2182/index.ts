/**
 * =============================================================================
 * SECUURA TRANSFER SERVICE
 * =============================================================================
 * Handles ownership transfer workflows:
 * - Transfer request creation and management
 * - Multi-signature approval collection
 * - Transfer execution with blockchain anchoring
 * - Notification dispatch
 * - Complete audit trail
 * Port: 4010
 * =============================================================================
 */

// KS-1725: FIRST import, before any module that could parse: installs the zod 3 compatible issue map
// (zod 4 error map; see packages/shared/src/validation/zod3-compat.ts) for this whole process.
import '@secuura/shared/zod3-compat';
import express, { Request, Response, NextFunction, RequestHandler } from 'express';
import { boundedJson } from '@secuura/shared'; // KS-1724: express.json plus the structural caps (array length, node count, depth)
import cors from 'cors';
import helmet from 'helmet';
import { z } from 'zod';
import { v4 as uuidv4 } from 'uuid';
import crypto from 'crypto';
import dotenv from 'dotenv';
import { validateEnv } from './utils/logger';
import { authenticate as jwtAuthenticate, enforceProductionConfig, errorHandler, isoDateTimeSchema, rejectNulBytes } from '@secuura/shared';
import { DOCUMENT_ID_PATTERN } from './utils/ids';

dotenv.config();

// Validate environment variables at startup
validateEnv();

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('transfer', {
  requiredEnvVars: ['DATABASE_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

// Import routes
import { delegationRoutes } from './routes/delegations';
import { workflowRoutes } from './routes/workflows';

// Import services
import { verifyDbReady as verifyWorkflowDb } from './services/approvalWorkflowService';
import { verifyDbReady as verifyDelegationDb } from './services/delegationService';
// KS-2038: the one place that says who may act on a transfer.
import { decideTransferAccess, isNonUserPrincipal, sameId, signedInCaller, type SignedInCaller, type TransferVerb } from './services/transferAccess';

const app = express();
const PORT = process.env.PORT || 4020;

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

type TransferType = 'simple' | 'sale' | 'inheritance' | 'corporate';
type TransferStatus = 'draft' | 'pending_approval' | 'approved' | 'executing' | 'completed' | 'rejected' | 'cancelled';

interface Transfer {
  id: string;
  documentId: string;
  transferType: TransferType;
  
  // Parties involved
  currentOwnerId: string;
  currentOwnerDid?: string;
  newOwnerId: string;
  newOwnerDid?: string;
  initiatedBy: string;
  
  // Transfer details
  reason?: string;
  legalReference?: string;
  effectiveDate?: Date;
  
  // For sale transfers
  saleAmount?: number;
  saleCurrency?: string;
  paymentVerified?: boolean;
  paymentReference?: string;
  
  // For inheritance transfers
  deceasedId?: string;
  probateReference?: string;
  executorId?: string;
  
  // For corporate transfers
  corporateResolutionRef?: string;
  boardApprovalRef?: string;
  
  // Approval workflow
  requiredApprovals: number;
  approvals: TransferApproval[];
  rejections: TransferRejection[];
  
  // Blockchain anchoring
  anchorId?: string;
  transactionHash?: string;
  blockNumber?: number;
  
  // Status and metadata
  status: TransferStatus;
  statusHistory: StatusChange[];
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date;
  
  // Document snapshot at transfer time
  documentHash: string;
  documentTitle: string;
  documentType: string;
}

interface TransferApproval {
  id: string;
  approverId: string;
  approverRole: string;
  signature?: string;
  walletAddress?: string;
  comment?: string;
  approvedAt: Date;
}

interface TransferRejection {
  id: string;
  rejectorId: string;
  rejectorRole: string;
  reason: string;
  rejectedAt: Date;
}

interface StatusChange {
  fromStatus: TransferStatus | null;
  toStatus: TransferStatus;
  changedBy: string;
  reason?: string;
  changedAt: Date;
}

interface TransferNotification {
  id: string;
  transferId: string;
  type: 'initiated' | 'approval_required' | 'approved' | 'rejected' | 'completed' | 'cancelled';
  recipientId: string;
  recipientEmail?: string;
  message: string;
  sentAt?: Date;
  readAt?: Date;
}

// =============================================================================
// STORAGE — DB-first with in-memory fallback
// =============================================================================

import { initDb, query, isDbAvailable } from './db';
// KS-1725: zod 4 issues rendered in zod 3.25.76's shape for every response (the client contract unchanged).
import { zod3Issues } from '@secuura/shared/zod3-compat';

const memTransfers = new Map<string, Transfer>();
const memTransfersByDocument = new Map<string, string[]>();
const memTransfersByOwner = new Map<string, string[]>();
const memNotifications = new Map<string, TransferNotification>();

async function dbSaveTransfer(t: Transfer): Promise<void> {
  memTransfers.set(t.id, t);
  if (t.documentId) {
    if (!memTransfersByDocument.has(t.documentId)) memTransfersByDocument.set(t.documentId, []);
    const ids = memTransfersByDocument.get(t.documentId)!;
    if (!ids.includes(t.id)) ids.push(t.id);
  }
  if (t.currentOwnerId) {
    if (!memTransfersByOwner.has(t.currentOwnerId)) memTransfersByOwner.set(t.currentOwnerId, []);
    const ids = memTransfersByOwner.get(t.currentOwnerId)!;
    if (!ids.includes(t.id)) ids.push(t.id);
  }
  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_transfers (id, document_id, document_hash, document_title, document_type,
         transfer_type, current_owner_id, current_owner_did, new_owner_id, new_owner_did,
         initiated_by, reason, legal_reference, effective_date, sale_amount, sale_currency,
         payment_verified, payment_reference, required_approvals, anchor_id, transaction_hash,
         block_number, status, status_history, approvals, rejections, created_at, updated_at, completed_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29)
       ON CONFLICT (id) DO UPDATE SET
         status = EXCLUDED.status, status_history = EXCLUDED.status_history,
         approvals = EXCLUDED.approvals, rejections = EXCLUDED.rejections,
         anchor_id = EXCLUDED.anchor_id, transaction_hash = EXCLUDED.transaction_hash,
         block_number = EXCLUDED.block_number, completed_at = EXCLUDED.completed_at,
         updated_at = NOW()`,
      [t.id, t.documentId, t.documentHash, t.documentTitle, t.documentType,
       t.transferType, t.currentOwnerId, t.currentOwnerDid || null, t.newOwnerId, t.newOwnerDid || null,
       t.initiatedBy, t.reason || null, t.legalReference || null, t.effectiveDate || null,
       t.saleAmount || null, t.saleCurrency || null, t.paymentVerified || false, t.paymentReference || null,
       t.requiredApprovals, t.anchorId || null, t.transactionHash || null, t.blockNumber || null,
       t.status, JSON.stringify(t.statusHistory || []), JSON.stringify(t.approvals || []),
       JSON.stringify(t.rejections || []), t.createdAt, t.updatedAt, t.completedAt || null],
    );
  } catch (err: any) {
    log('warn', 'DB save transfer failed', { transferId: t.id, error: err?.message });
  }
}

function rowToTransfer(r: any): Transfer {
  return {
    ...r,
    id: r.id,
    documentId: r.document_id,
    documentHash: r.document_hash,
    documentTitle: r.document_title,
    documentType: r.document_type,
    transferType: r.transfer_type,
    currentOwnerId: r.current_owner_id,
    currentOwnerDid: r.current_owner_did,
    newOwnerId: r.new_owner_id,
    newOwnerDid: r.new_owner_did,
    initiatedBy: r.initiated_by,
    reason: r.reason,
    legalReference: r.legal_reference,
    effectiveDate: r.effective_date ? new Date(r.effective_date) : undefined,
    saleAmount: r.sale_amount ? Number(r.sale_amount) : undefined,
    saleCurrency: r.sale_currency,
    paymentVerified: r.payment_verified,
    paymentReference: r.payment_reference,
    requiredApprovals: r.required_approvals,
    anchorId: r.anchor_id,
    transactionHash: r.transaction_hash,
    blockNumber: r.block_number ? Number(r.block_number) : undefined,
    status: r.status,
    statusHistory: r.status_history || [],
    approvals: r.approvals || [],
    rejections: r.rejections || [],
    createdAt: new Date(r.created_at),
    updatedAt: new Date(r.updated_at),
    completedAt: r.completed_at ? new Date(r.completed_at) : undefined,
  };
}

function rowToNotification(r: any): TransferNotification {
  return {
    id: r.id,
    transferId: r.transfer_id,
    type: r.type,
    recipientId: r.recipient_id,
    recipientEmail: r.recipient_email || undefined,
    message: r.message,
    sentAt: r.sent_at ? new Date(r.sent_at) : undefined,
    readAt: r.read_at ? new Date(r.read_at) : undefined,
  };
}

async function dbGetTransfer(id: string): Promise<Transfer | undefined> {
  if (isDbAvailable()) {
    try {
      const result = await query('SELECT * FROM svc_transfers WHERE id = $1', [id]);
      if (result.rows.length > 0) return rowToTransfer(result.rows[0]);
    } catch { /* fall through */ }
  }
  return memTransfers.get(id);
}

async function dbGetTransfersByOwner(ownerId: string): Promise<Transfer[]> {
  if (isDbAvailable()) {
    try {
      const result = await query(
        'SELECT * FROM svc_transfers WHERE current_owner_id = $1 OR new_owner_id = $1 ORDER BY created_at DESC',
        [ownerId],
      );
      if (result.rows.length > 0) return result.rows.map(rowToTransfer);
    } catch { /* fall through */ }
  }
  const ids = memTransfersByOwner.get(ownerId) || [];
  return ids.map(id => memTransfers.get(id)).filter(Boolean) as Transfer[];
}

async function dbSaveNotification(n: TransferNotification): Promise<void> {
  memNotifications.set(n.id, n);
  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_transfer_notifications (id, transfer_id, type, recipient_id, recipient_email, message, sent_at, read_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
       ON CONFLICT (id) DO UPDATE SET sent_at = EXCLUDED.sent_at, read_at = EXCLUDED.read_at`,
      [n.id, n.transferId, n.type, n.recipientId, n.recipientEmail || null, n.message, n.sentAt || null, n.readAt || null],
    );
  } catch (err: any) {
    log('warn', 'DB save notification failed', { error: err?.message });
  }
}

/**
 * Load all transfers and notifications from the database into the in-memory
 * Maps so that the service survives restarts without data loss.
 */
export async function loadFromDb(): Promise<void> {
  if (!isDbAvailable()) return;

  try {
    const tResult = await query('SELECT * FROM svc_transfers ORDER BY created_at');
    for (const row of tResult.rows) {
      const t = rowToTransfer(row);
      memTransfers.set(t.id, t);
      if (t.documentId) {
        if (!memTransfersByDocument.has(t.documentId)) memTransfersByDocument.set(t.documentId, []);
        const ids = memTransfersByDocument.get(t.documentId)!;
        if (!ids.includes(t.id)) ids.push(t.id);
      }
      if (t.currentOwnerId) {
        if (!memTransfersByOwner.has(t.currentOwnerId)) memTransfersByOwner.set(t.currentOwnerId, []);
        const ids = memTransfersByOwner.get(t.currentOwnerId)!;
        if (!ids.includes(t.id)) ids.push(t.id);
      }
    }

    const nResult = await query('SELECT * FROM svc_transfer_notifications ORDER BY sent_at');
    for (const row of nResult.rows) {
      const n = rowToNotification(row);
      memNotifications.set(n.id, n);
    }

    log('info', 'Loaded data from DB', {
      transfers: tResult.rows.length,
      notifications: nResult.rows.length,
    });
  } catch (err: any) {
    log('warn', 'Failed to load from DB — starting with empty in-memory state', { error: err?.message });
  }
}

// =============================================================================
// LOGGING
// =============================================================================

function log(level: 'info' | 'warn' | 'error', message: string, meta?: object) {
  const timestamp = new Date().toISOString();
  console.log(JSON.stringify({ timestamp, level, service: 'transfer', message, ...meta }));
}

// =============================================================================
// MIDDLEWARE
// =============================================================================

app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:6100', 'http://localhost:6101'],
  credentials: true,
}));
// KS-1724: was `app.use(express.json());`; the same options, plus the structural caps.
app.use(boundedJson({ service: 'transfer' }));
app.use(rejectNulBytes()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)

const requestLogger: RequestHandler = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    log('info', 'Request completed', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: `${Date.now() - start}ms`,
    });
  });
  next();
};
app.use(requestLogger);

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

const initiateTransferSchema = z.object({
  // KS-474: `doc-<ts>-<hex>` external ids, not UUIDs — see utils/ids.ts
  documentId: z.string().regex(DOCUMENT_ID_PATTERN),
  transferType: z.enum(['simple', 'sale', 'inheritance', 'corporate']),
  currentOwnerId: z.string().guid(),
  newOwnerId: z.string().guid(),
  newOwnerDid: z.string().optional(),
  reason: z.string().optional(),
  legalReference: z.string().optional(),
  effectiveDate: isoDateTimeSchema.optional(), // KS-427: accept RFC 3339 offsets, normalise to UTC
  
  // Sale-specific
  saleAmount: z.number().positive().optional(),
  saleCurrency: z.string().length(3).optional(),
  paymentReference: z.string().optional(),
  
  // Inheritance-specific
  deceasedId: z.string().guid().optional(),
  probateReference: z.string().optional(),
  executorId: z.string().guid().optional(),
  
  // Corporate-specific
  corporateResolutionRef: z.string().optional(),
  boardApprovalRef: z.string().optional(),
  
  // Document info
  documentHash: z.string().regex(/^[a-f0-9]{64}$/i),
  documentTitle: z.string().min(1),
  documentType: z.string().min(1),
});

const approveTransferSchema = z.object({
  approverId: z.string().guid(),
  approverRole: z.string(),
  // KS-518: `reason` is in the published TransferApproveRequest but was
  // undeclared here — zod's non-strict objects silently DROP unknown keys,
  // so a schema-violating `reason: {}` was accepted and ignored. Declaring
  // it types it (non-string → 400) without changing valid-input behaviour.
  reason: z.string().optional(),
  signature: z.string().optional(),
  walletAddress: z.string().optional(),
  comment: z.string().optional(),
});

const rejectTransferSchema = z.object({
  rejectorId: z.string().guid(),
  rejectorRole: z.string(),
  reason: z.string().min(1),
  // KS-1435: declare signature on the reject schema — before, rejectTransferSchema
  // omitted it entirely, so a wrong-typed signature passed validation with 200 and
  // the reject still ran; the published contract did not match the runtime.
  signature: z.string().optional(),
});

// KS 2055 half 2: Kam's ruling 2026-11-11: reason is optional, a string, trimmed, at most 1000 characters; absent, null or empty records 'Cancelled by user'.
const cancelTransferSchema = z.object({
  reason: z.string().trim().max(1000).nullish(),
});

// =============================================================================
// ROUTES
// =============================================================================

// Health check
app.get('/health', (_req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'transfer',
    version: '0.1.0',
    timestamp: new Date().toISOString(),
    stats: {
      totalTransfers: memTransfers.size,
      pendingApprovals: Array.from(memTransfers.values()).filter(t => t.status === 'pending_approval').length,
      completed: Array.from(memTransfers.values()).filter(t => t.status === 'completed').length,
    },
  });
});

// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
app.use('/api', jwtAuthenticate());

// Mount delegation and workflow routes
app.use('/api/delegations', delegationRoutes);
app.use('/api/workflows', workflowRoutes);

// API info
app.get('/api', (_req: Request, res: Response) => {
  res.json({
    service: 'Secuura Transfer Service',
    version: '0.2.0',
    endpoints: {
      transfers: {
        'POST /api/transfers': 'Initiate ownership transfer',
        'GET /api/transfers': 'List transfers (with filters)',
        'GET /api/transfers/:id': 'Get transfer details',
        'POST /api/transfers/:id/approve': 'Approve transfer (multi-sig)',
        'POST /api/transfers/:id/reject': 'Reject transfer',
        'POST /api/transfers/:id/execute': 'Execute approved transfer',
        'POST /api/transfers/:id/cancel': 'Cancel pending transfer',
        'GET /api/transfers/:id/history': 'Get transfer status history',
        'GET /api/transfers/document/:documentId': 'Get transfers for document',
      },
      delegations: {
        'POST /api/delegations': 'Create delegation',
        'GET /api/delegations': 'List delegations (granted/received)',
        'GET /api/delegations/:id': 'Get delegation details with chain',
        'GET /api/delegations/document/:documentId': 'Get delegations for document',
        'POST /api/delegations/:id/revoke': 'Revoke delegation',
        'POST /api/delegations/validate': 'Validate delegation authority',
        'GET /api/delegations/stats/overview': 'Get delegation statistics',
      },
      workflows: {
        'GET /api/workflows': 'List available workflows',
        'GET /api/workflows/:id': 'Get workflow details',
        'POST /api/workflows': 'Create custom workflow',
        'GET /api/workflows/transfer/:transferId/status': 'Get workflow status',
        'POST /api/workflows/steps/:stepId/approve': 'Approve workflow step',
        'GET /api/workflows/pending/me': 'Get pending approvals',
        'POST /api/workflows/escalate': 'Process escalations',
      },
      notifications: {
        'GET /api/notifications': 'Get user notifications',
        'PATCH /api/notifications/:id/read': 'Mark notification as read',
      },
    },
    transferTypes: {
      simple: 'Direct owner-to-owner transfer',
      sale: 'Transfer with payment verification',
      inheritance: 'Transfer with legal/probate documentation',
      corporate: 'Transfer requiring corporate governance approval',
    },
    delegationTypes: {
      full: 'Full authority over document',
      approve: 'Can approve transfers',
      initiate: 'Can initiate transfers',
      view: 'Can view document details',
      sign: 'Can sign on behalf of owner',
      manage_access: 'Can manage access grants',
    },
    workflowTypes: {
      single: 'Single approver',
      sequential: 'Approvers in order',
      parallel: 'All approvers at once',
      threshold: 'N of M approvers',
      hierarchical: 'Based on org hierarchy',
    },
  });
});

// KS-2081: refused before the body is read or any transfer is looked up, so this answer depends on the caller alone and says nothing about any id.
const refuseNonUserPrincipal = (req: Request, res: Response): boolean => {
  if (!isNonUserPrincipal((req as any).user)) return false;
  res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'An API key cannot open or act on a transfer.' } });
  return true;
};

/**
 * POST /api/transfers
 * Initiate a new ownership transfer
 */
const initiateTransferHandler = async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-2081: not requireCaller, because a token with no user id keeps this door's body fallback below; who may open for whom is KS-2049's.
    if (refuseNonUserPrincipal(req, res)) return;
    const data = initiateTransferSchema.parse(req.body);
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const initiatedBy = ((req as any).user?.userId as string) || data.currentOwnerId;
    
    const transferId = uuidv4();
    
    // Determine required approvals based on transfer type
    let requiredApprovals = 1;
    if (data.transferType === 'sale') requiredApprovals = 2; // Both parties
    if (data.transferType === 'inheritance') requiredApprovals = 2; // Executor + beneficiary
    if (data.transferType === 'corporate') requiredApprovals = 3; // Board members
    
    const transfer: Transfer = {
      id: transferId,
      documentId: data.documentId,
      transferType: data.transferType,
      currentOwnerId: data.currentOwnerId,
      newOwnerId: data.newOwnerId,
      newOwnerDid: data.newOwnerDid,
      initiatedBy,
      reason: data.reason,
      legalReference: data.legalReference,
      effectiveDate: data.effectiveDate ? new Date(data.effectiveDate) : undefined,
      saleAmount: data.saleAmount,
      saleCurrency: data.saleCurrency,
      paymentReference: data.paymentReference,
      paymentVerified: false,
      deceasedId: data.deceasedId,
      probateReference: data.probateReference,
      executorId: data.executorId,
      corporateResolutionRef: data.corporateResolutionRef,
      boardApprovalRef: data.boardApprovalRef,
      requiredApprovals,
      approvals: [],
      rejections: [],
      status: 'pending_approval',
      statusHistory: [{
        fromStatus: null,
        toStatus: 'pending_approval',
        changedBy: initiatedBy,
        reason: 'Transfer initiated',
        changedAt: new Date(),
      }],
      documentHash: data.documentHash,
      documentTitle: data.documentTitle,
      documentType: data.documentType,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    // Persist transfer (DB + mem)
    await dbSaveTransfer(transfer);
    
    // Create notifications
    createNotification(transferId, 'initiated', data.currentOwnerId, 
      `Transfer initiated for "${data.documentTitle}"`);
    createNotification(transferId, 'approval_required', data.newOwnerId,
      `You have been proposed as the new owner of "${data.documentTitle}". Please review and approve.`);
    
    log('info', 'Transfer initiated', { 
      transferId, 
      documentId: data.documentId, 
      type: data.transferType,
    });
    
    res.status(201).json({
      success: true,
      data: formatTransferResponse(transfer),
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(error.issues) } });
    }
    next(error);
  }
};
app.post('/api/transfers', initiateTransferHandler);
app.post('/api/transfers/initiate', initiateTransferHandler);

/**
 * GET /api/transfers
 * List transfers with optional filters
 */
app.get('/api/transfers', async (req: Request, res: Response) => {
  const { ownerId, status, type, limit = '50', offset = '0' } = req.query;
  
  let filtered: Transfer[] = [];
  
  if (ownerId) {
    filtered = await dbGetTransfersByOwner(ownerId as string);
  } else if (isDbAvailable()) {
    try {
      const result = await query('SELECT * FROM svc_transfers ORDER BY created_at DESC');
      filtered = result.rows.map(rowToTransfer);
    } catch {
      filtered = Array.from(memTransfers.values());
    }
  } else {
    filtered = Array.from(memTransfers.values());
  }
  
  if (status) {
    filtered = filtered.filter(t => t.status === status);
  }
  if (type) {
    filtered = filtered.filter(t => t.transferType === type);
  }
  
  filtered.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
  
  const total = filtered.length;
  const results = filtered
    .slice(parseInt(offset as string), parseInt(offset as string) + parseInt(limit as string))
    .map(formatTransferResponse);
  
  res.json({
    success: true,
    data: {
      transfers: results,
      total,
      limit: parseInt(limit as string),
      offset: parseInt(offset as string),
    },
  });
});

/**
 * GET /api/transfers/:id
 * Get transfer details
 */
app.get('/api/transfers/:id', async (req: Request, res: Response) => {
  const transfer = await dbGetTransfer(req.params.id);
  
  if (!transfer) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Transfer not found' } });
  }
  
  res.json({
    success: true,
    data: formatTransferResponse(transfer),
  });
});

// KS-2038: the caller checks the four doors share. Each answers on `res` and returns null when it refused, so a door cannot carry on past a refusal.
const requireCaller = (req: Request, res: Response): SignedInCaller | null => {
  if (refuseNonUserPrincipal(req, res)) return null;
  const caller = signedInCaller((req as any).user);
  if (!caller) {
    res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
  }
  return caller;
};

const refuseUnlessEntitled = (caller: SignedInCaller, verb: TransferVerb, transfer: Transfer, res: Response): boolean => {
  const access = decideTransferAccess(caller.userId, verb, transfer);
  if (access.allow) return false;
  if (access.status === 404) {
    // KS-2038: a stranger reads exactly what an unknown id reads, as on KS-1851 and KS-692, so a refusal does not confirm the transfer exists.
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Transfer not found' } });
    return true;
  }
  res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: `Not permitted to ${verb} this transfer` } });
  return true;
};

/**
 * POST /api/transfers/:id/approve
 * Approve a transfer (multi-sig)
 */
app.post('/api/transfers/:id/approve', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-2038: the actor is the signed-in identity. Before, approverId and approverRole were taken from the body and no caller was checked.
    const caller = requireCaller(req, res);
    if (!caller) return;
    const data = approveTransferSchema.parse(req.body);
    const transfer = memTransfers.get(req.params.id);
    
    if (!transfer) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Transfer not found' } });
    }
    
    // KS-2038: before any status answer, so a stranger learns nothing about the transfer.
    if (refuseUnlessEntitled(caller, 'approve', transfer, res)) return;
    
    // KS-2038: approverId stays required and must be the caller. It stays required so a body that names nobody, such as the SDK's { action: 'reject' }, keeps its 400 and is never read as an approval.
    if (!sameId(data.approverId, caller.userId)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'approverId must be the signed-in user' } });
    }
    
    if (transfer.status !== 'pending_approval') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Cannot approve transfer in ${transfer.status} status` } });
    }
    
    // Check if already approved by this user
    // KS-2038: compares the caller, not a body field, so one caller can no longer meet a multi-approval count by varying the id.
    if (transfer.approvals.some(a => sameId(a.approverId, caller.userId))) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Already approved by this user' } });
    }
    
    const approval: TransferApproval = {
      id: uuidv4(),
      // KS-2038: recorded from the token. The body's approverRole is still required by the published schema, and its value is not read.
      approverId: caller.userId,
      approverRole: caller.role,
      signature: data.signature,
      walletAddress: data.walletAddress,
      comment: data.comment,
      approvedAt: new Date(),
    };
    
    transfer.approvals.push(approval);
    transfer.updatedAt = new Date();
    
    // Check if all required approvals collected
    if (transfer.approvals.length >= transfer.requiredApprovals) {
      transfer.status = 'approved';
      transfer.statusHistory.push({
        fromStatus: 'pending_approval',
        toStatus: 'approved',
        changedBy: caller.userId, // KS-2038: was the body's approverId
        reason: 'All required approvals collected',
        changedAt: new Date(),
      });
      
      createNotification(transfer.id, 'approved', transfer.currentOwnerId,
        `Transfer of "${transfer.documentTitle}" has been fully approved and is ready for execution.`);
    }
    
    await dbSaveTransfer(transfer);
    
    log('info', 'Transfer approved', { 
      transferId: transfer.id, 
      approverId: caller.userId, // KS-2038: was the body's approverId
      totalApprovals: transfer.approvals.length,
      required: transfer.requiredApprovals,
    });
    
    res.json({
      success: true,
      data: {
        approval,
        transfer: formatTransferResponse(transfer),
        fullyApproved: transfer.status === 'approved',
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(error.issues) } });
    }
    next(error);
  }
});

/**
 * POST /api/transfers/:id/reject
 * Reject a transfer
 */
app.post('/api/transfers/:id/reject', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-2038: the actor is the signed-in identity. Before, rejectorId and rejectorRole were taken from the body and no caller was checked.
    const caller = requireCaller(req, res);
    if (!caller) return;
    const data = rejectTransferSchema.parse(req.body);
    const transfer = memTransfers.get(req.params.id);
    
    if (!transfer) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Transfer not found' } });
    }
    
    // KS-2038: before any status answer, so a stranger learns nothing about the transfer.
    if (refuseUnlessEntitled(caller, 'reject', transfer, res)) return;
    
    // KS-2038: rejectorId stays required and must be the caller, the same rule as approve.
    if (!sameId(data.rejectorId, caller.userId)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'rejectorId must be the signed-in user' } });
    }
    
    if (transfer.status !== 'pending_approval') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Cannot reject transfer in ${transfer.status} status` } });
    }
    
    const rejection: TransferRejection = {
      id: uuidv4(),
      // KS-2038: recorded from the token. The body's rejectorRole is still required by the published schema, and its value is not read.
      rejectorId: caller.userId,
      rejectorRole: caller.role,
      reason: data.reason,
      rejectedAt: new Date(),
    };
    
    transfer.rejections.push(rejection);
    transfer.status = 'rejected';
    transfer.updatedAt = new Date();
    transfer.statusHistory.push({
      fromStatus: 'pending_approval',
      toStatus: 'rejected',
      changedBy: caller.userId, // KS-2038: was the body's rejectorId
      reason: data.reason,
      changedAt: new Date(),
    });
    
    createNotification(transfer.id, 'rejected', transfer.initiatedBy,
      `Transfer of "${transfer.documentTitle}" has been rejected. Reason: ${data.reason}`);
    
    await dbSaveTransfer(transfer);
    log('info', 'Transfer rejected', { transferId: transfer.id, rejectorId: caller.userId }); // KS-2038: was the body's rejectorId
    
    res.json({
      success: true,
      data: formatTransferResponse(transfer),
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(error.issues) } });
    }
    next(error);
  }
});

/**
 * POST /api/transfers/:id/execute
 * Execute an approved transfer
 */
app.post('/api/transfers/:id/execute', async (req: Request, res: Response) => {
  // KS-2038: the caller is required and checked. Before, any signed-in user could execute any approved transfer, and a token with no user id was recorded as 'system'.
  const caller = requireCaller(req, res);
  if (!caller) return;
  const transfer = memTransfers.get(req.params.id);
  
  if (!transfer) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Transfer not found' } });
  }
  
  // KS-2038: before any status answer, so a stranger learns nothing about the transfer.
  if (refuseUnlessEntitled(caller, 'execute', transfer, res)) return;
  
  if (transfer.status !== 'approved') {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Cannot execute transfer in ${transfer.status} status` } });
  }
  
  // For sale transfers, verify payment if not already done
  if (transfer.transferType === 'sale' && !transfer.paymentVerified) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Payment must be verified before execution' } });
  }
  
  // Update status to executing
  transfer.status = 'executing';
  transfer.updatedAt = new Date();
  transfer.statusHistory.push({
    fromStatus: 'approved',
    toStatus: 'executing',
    changedBy: caller.userId, // KS-2038: requireCaller above means no fallback to 'system' is left
    reason: 'Execution started',
    changedAt: new Date(),
  });
  
  // In development mode, mock blockchain anchoring
  setTimeout(() => {
    transfer.anchorId = `anchor_${Date.now()}`;
    transfer.transactionHash = `mock_tx_${crypto.randomBytes(32).toString('hex')}`;
    transfer.blockNumber = null as any; // F-03: real blockHeight populates after confirmation
    transfer.status = 'completed';
    transfer.completedAt = new Date();
    transfer.updatedAt = new Date();
    transfer.statusHistory.push({
      fromStatus: 'executing',
      toStatus: 'completed',
      changedBy: 'system',
      reason: 'Blockchain anchoring completed',
      changedAt: new Date(),
    });
    
    createNotification(transfer.id, 'completed', transfer.currentOwnerId,
      `Transfer of "${transfer.documentTitle}" has been completed. The new owner is now in control.`);
    createNotification(transfer.id, 'completed', transfer.newOwnerId,
      `You are now the owner of "${transfer.documentTitle}". Transaction: ${transfer.transactionHash}`);
    
    dbSaveTransfer(transfer).catch(() => {});
    log('info', 'Transfer completed', { transferId: transfer.id, txHash: transfer.transactionHash });
  }, 2000);
  
  res.json({
    success: true,
    data: {
      transfer: formatTransferResponse(transfer),
      message: 'Transfer execution started. Blockchain anchoring in progress.',
    },
  });
});

/**
 * POST /api/transfers/:id/cancel
 * Cancel a pending transfer
 */
app.post('/api/transfers/:id/cancel', async (req: Request, res: Response) => {
  // KS-2038: the caller is required and checked. Before, any signed-in user could cancel any pending transfer, and a token with no user id was recorded as 'unknown'.
  const caller = requireCaller(req, res);
  if (!caller) return;
  const transfer = memTransfers.get(req.params.id);
  const parsed = cancelTransferSchema.safeParse(req.body ?? {});
  if (!parsed.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(parsed.error.issues) } });
  }
  const { reason } = parsed.data;
  if (!transfer) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Transfer not found' } });
  }
  
  // KS-2038: before any status answer, so a stranger learns nothing about the transfer.
  if (refuseUnlessEntitled(caller, 'cancel', transfer, res)) return;
  
  if (!['draft', 'pending_approval'].includes(transfer.status)) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Cannot cancel transfer in ${transfer.status} status` } });
  }
  
  const previousStatus = transfer.status; // KS-2055: captured before the assignment below, so the history entry records the real from-status
  transfer.status = 'cancelled';
  transfer.updatedAt = new Date();
  transfer.statusHistory.push({
    fromStatus: previousStatus,
    toStatus: 'cancelled',
    changedBy: caller.userId, // KS-2038: requireCaller above means no fallback to 'unknown' is left
    reason: reason || 'Cancelled by user',
    changedAt: new Date(),
  });
  
  createNotification(transfer.id, 'cancelled', transfer.newOwnerId,
    `Transfer of "${transfer.documentTitle}" has been cancelled.`);
  
  await dbSaveTransfer(transfer);
  log('info', 'Transfer cancelled', { transferId: transfer.id });
  
  res.json({
    success: true,
    data: formatTransferResponse(transfer),
  });
});

/**
 * GET /api/transfers/:id/history
 * Get transfer status history
 */
app.get('/api/transfers/:id/history', async (req: Request, res: Response) => {
  const transfer = await dbGetTransfer(req.params.id);
  
  if (!transfer) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Transfer not found' } });
  }
  
  res.json({
    success: true,
    data: {
      transferId: transfer.id,
      history: transfer.statusHistory,
      approvals: transfer.approvals,
      rejections: transfer.rejections,
    },
  });
});

/**
 * GET /api/transfers/document/:documentId
 * Get all transfers for a document
 */
app.get('/api/transfers/document/:documentId', (req: Request, res: Response) => {
  const transferIds = memTransfersByDocument.get(req.params.documentId) || [];
  const documentTransfers = transferIds
    .map(id => memTransfers.get(id))
    .filter(Boolean)
    .map(t => formatTransferResponse(t!));
  
  res.json({
    success: true,
    data: {
      documentId: req.params.documentId,
      transfers: documentTransfers,
      count: documentTransfers.length,
    },
  });
});

/**
 * GET /api/notifications
 * Get notifications for a user
 */
app.get('/api/notifications', (req: Request, res: Response) => {
  // Pen-test F-04: read from authenticated req.user (set by authenticate()
  // middleware), NOT from raw headers. Direct header reads are spoofable.
  const userId = ((req as any).user?.userId as string) || (req.query.userId as string);
  
  if (!userId) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'User ID required' } });
  }
  
  const userNotifications = Array.from(memNotifications.values())
    .filter(n => n.recipientId === userId)
    .sort((a, b) => (b.sentAt?.getTime() || 0) - (a.sentAt?.getTime() || 0));
  
  res.json({
    success: true,
    data: {
      notifications: userNotifications,
      unreadCount: userNotifications.filter(n => !n.readAt).length,
    },
  });
});

/**
 * PATCH /api/notifications/:id/read
 * Mark notification as read
 */
app.patch('/api/notifications/:id/read', (req: Request, res: Response) => {
  const notification = memNotifications.get(req.params.id);
  
  if (!notification) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Notification not found' } });
  }
  
  notification.readAt = new Date();
  
  res.json({
    success: true,
    data: notification,
  });
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function formatTransferResponse(transfer: Transfer) {
  return {
    id: transfer.id,
    documentId: transfer.documentId,
    transferType: transfer.transferType,
    currentOwnerId: transfer.currentOwnerId,
    newOwnerId: transfer.newOwnerId,
    newOwnerDid: transfer.newOwnerDid,
    reason: transfer.reason,
    legalReference: transfer.legalReference,
    effectiveDate: transfer.effectiveDate,
    saleAmount: transfer.saleAmount,
    saleCurrency: transfer.saleCurrency,
    paymentVerified: transfer.paymentVerified,
    requiredApprovals: transfer.requiredApprovals,
    currentApprovals: transfer.approvals.length,
    status: transfer.status,
    anchorId: transfer.anchorId,
    transactionHash: transfer.transactionHash,
    blockNumber: transfer.blockNumber,
    documentTitle: transfer.documentTitle,
    documentType: transfer.documentType,
    createdAt: transfer.createdAt,
    updatedAt: transfer.updatedAt,
    completedAt: transfer.completedAt,
  };
}

function createNotification(
  transferId: string,
  type: TransferNotification['type'],
  recipientId: string,
  message: string
) {
  const notification: TransferNotification = {
    id: uuidv4(),
    transferId,
    type,
    recipientId,
    message,
    sentAt: new Date(),
  };
  
  dbSaveNotification(notification).catch(() => {});
  
  // In production, this would send actual notifications (email, push, etc.)
  log('info', 'Notification created', { notificationId: notification.id, type, recipientId });
}

// =============================================================================
// ERROR HANDLING
// =============================================================================

app.use((_req: Request, res: Response) => {
  res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not Found' } });
});

// KS-111: route errors through the shared AppError-aware handler (maps
// AppError.statusCode + Zod -> 4xx; emits the canonical {success,error} shape).
app.use(errorHandler);

// =============================================================================
// START SERVER
// =============================================================================

/**
 * One-shot DB boot work: warm the in-memory transfer / notification caches
 * and verify + seed the approval-workflow and delegation tables.
 * Passed to initDb as its onReady hook so it runs on the boot success path
 * AND again when the DB only comes up after a lost start race (KS-377
 * background retry) — recovery re-runs it instead of silently skipping it
 * (KS-382).
 */
async function runDbBootTasks(): Promise<void> {
  await loadFromDb();
  await verifyWorkflowDb();
  await verifyDelegationDb();
}

// Initialize DB, load persisted data, then start server
initDb(runDbBootTasks).then((connected) => {
  log('info', 'Database init', { connected });
});

const server = app.listen(PORT, () => {
  log('info', 'Transfer Service started', { port: PORT });
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║               SECUURA TRANSFER SERVICE                        ║
╠═══════════════════════════════════════════════════════════════╣
║  Port:      ${String(PORT).padEnd(47)}║
║  API Info:  http://localhost:${PORT}/api                         ║
║  Health:    http://localhost:${PORT}/health                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Transfer Types:                                              ║
║    • Simple: Direct owner-to-owner                           ║
║    • Sale: With payment verification                         ║
║    • Inheritance: With probate/legal docs                    ║
║    • Corporate: With governance approval                     ║
╠═══════════════════════════════════════════════════════════════╣
║  Delegation Types:                                            ║
║    • Full: Complete authority                                 ║
║    • Approve: Transfer approval only                         ║
║    • Initiate: Can start transfers                           ║
║    • View / Sign / Manage Access                             ║
╠═══════════════════════════════════════════════════════════════╣
║  Workflows:                                                   ║
║    • Simple, Sequential, Parallel, Threshold, Hierarchical   ║
╚═══════════════════════════════════════════════════════════════╝
`);
});
// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;

export default app;
