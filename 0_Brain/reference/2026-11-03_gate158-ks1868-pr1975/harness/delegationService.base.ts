/**
 * =============================================================================
 * DELEGATION SERVICE
 * =============================================================================
 * Manages authority delegation for document ownership and transfers
 */

import { v4 as uuidv4 } from 'uuid';
import {
  Delegation,
  DelegationType,
  DelegationStatus,
  DelegationChain,
  DelegationChainLink,
  CreateDelegationRequest,
  DelegationValidationResult,
} from '../types/delegation.types';
import { query, isDbAvailable } from '../db';

// =============================================================================
// CONFIGURATION
// =============================================================================

const DELEGATION_CONFIG = {
  maxDelegationDepth: 5,
  defaultValidityDays: 365,
  maxValidityDays: 730,
  allowedDelegationTypes: ['full', 'approve', 'initiate', 'view', 'sign', 'manage_access'] as DelegationType[],
};

// =============================================================================
// DB HELPERS
// =============================================================================

function rowToDelegation(row: any): Delegation {
  return {
    id: row.id,
    delegatorId: row.delegator_id,
    delegatorDid: row.delegator_did ?? undefined,
    delegateId: row.delegate_id,
    delegateDid: row.delegate_did ?? undefined,
    delegateEmail: row.delegate_email ?? undefined,
    delegateName: row.delegate_name ?? undefined,
    documentId: row.document_id ?? undefined,
    organizationId: row.organization_id ?? undefined,
    delegationType: row.delegation_type ?? [],
    maxAmount: row.max_amount != null ? Number(row.max_amount) : undefined,
    requiresApproval: row.requires_approval ?? false,
    canSubDelegate: row.can_sub_delegate ?? false,
    maxDelegationDepth: row.max_delegation_depth ?? DELEGATION_CONFIG.maxDelegationDepth,
    currentDepth: row.current_depth ?? 0,
    parentDelegationId: row.parent_delegation_id ?? undefined,
    validFrom: new Date(row.valid_from),
    validUntil: row.valid_until ? new Date(row.valid_until) : undefined,
    status: row.status as DelegationStatus,
    createdAt: new Date(row.created_at),
    updatedAt: new Date(row.updated_at),
    revokedAt: row.revoked_at ? new Date(row.revoked_at) : undefined,
    revokedBy: row.revoked_by ?? undefined,
    revokedReason: row.revoked_reason ?? undefined,
    usageCount: row.usage_count ?? 0,
    lastUsedAt: row.last_used_at ? new Date(row.last_used_at) : undefined,
    anchorId: row.anchor_id ?? undefined,
    transactionHash: row.transaction_hash ?? undefined,
  };
}

async function dbGetDelegation(id: string): Promise<Delegation | undefined> {
  if (!isDbAvailable()) return undefined;
  try {
    const result = await query('SELECT * FROM svc_transfer_delegations WHERE id = $1', [id]);
    return result.rows.length > 0 ? rowToDelegation(result.rows[0]) : undefined;
  } catch { return undefined; }
}

async function dbGetDelegationsByDelegator(delegatorId: string): Promise<Delegation[]> {
  if (!isDbAvailable()) return [];
  try {
    const result = await query(
      'SELECT * FROM svc_transfer_delegations WHERE delegator_id = $1 ORDER BY created_at DESC',
      [delegatorId]
    );
    return result.rows.map(rowToDelegation);
  } catch { return []; }
}

async function dbGetDelegationsByDelegate(delegateId: string): Promise<Delegation[]> {
  if (!isDbAvailable()) return [];
  try {
    const result = await query(
      'SELECT * FROM svc_transfer_delegations WHERE delegate_id = $1 ORDER BY created_at DESC',
      [delegateId]
    );
    return result.rows.map(rowToDelegation);
  } catch { return []; }
}

async function dbGetDelegationsByDocument(documentId: string): Promise<Delegation[]> {
  if (!isDbAvailable()) return [];
  try {
    const result = await query(
      'SELECT * FROM svc_transfer_delegations WHERE document_id = $1 ORDER BY created_at DESC',
      [documentId]
    );
    return result.rows.map(rowToDelegation);
  } catch { return []; }
}

async function dbGetSubDelegations(parentId: string, status?: string): Promise<Delegation[]> {
  if (!isDbAvailable()) return [];
  try {
    let sql = 'SELECT * FROM svc_transfer_delegations WHERE parent_delegation_id = $1';
    const params: unknown[] = [parentId];
    if (status) {
      sql += ' AND status = $2';
      params.push(status);
    }
    const result = await query(sql, params);
    return result.rows.map(rowToDelegation);
  } catch { return []; }
}

async function dbInsertDelegation(d: Delegation): Promise<void> {
  if (!isDbAvailable()) return;
  await query(
    `INSERT INTO svc_transfer_delegations
       (id, delegator_id, delegator_did, delegate_id, delegate_did, delegate_email,
        delegate_name, document_id, organization_id, delegation_type, max_amount,
        requires_approval, can_sub_delegate, max_delegation_depth, current_depth,
        parent_delegation_id, valid_from, valid_until, status,
        revoked_at, revoked_by, revoked_reason, usage_count, last_used_at,
        anchor_id, transaction_hash, created_at, updated_at)
     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28)`,
    [
      d.id, d.delegatorId, d.delegatorDid ?? null, d.delegateId, d.delegateDid ?? null,
      d.delegateEmail ?? null, d.delegateName ?? null, d.documentId ?? null,
      d.organizationId ?? null, JSON.stringify(d.delegationType), d.maxAmount ?? null,
      d.requiresApproval ?? false, d.canSubDelegate, d.maxDelegationDepth, d.currentDepth,
      d.parentDelegationId ?? null, d.validFrom, d.validUntil ?? null, d.status,
      d.revokedAt ?? null, d.revokedBy ?? null, d.revokedReason ?? null,
      d.usageCount, d.lastUsedAt ?? null, d.anchorId ?? null, d.transactionHash ?? null,
      d.createdAt, d.updatedAt,
    ]
  );
}

async function dbUpdateDelegation(d: Delegation): Promise<void> {
  if (!isDbAvailable()) return;
  await query(
    `UPDATE svc_transfer_delegations SET
       status = $2, revoked_at = $3, revoked_by = $4, revoked_reason = $5,
       usage_count = $6, last_used_at = $7, updated_at = $8
     WHERE id = $1`,
    [
      d.id, d.status, d.revokedAt ?? null, d.revokedBy ?? null, d.revokedReason ?? null,
      d.usageCount, d.lastUsedAt ?? null, d.updatedAt,
    ]
  );
}

// =============================================================================
// VERIFY DB
// =============================================================================

export async function verifyDbReady(): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    await query('SELECT 1 FROM svc_transfer_delegations LIMIT 1');
  } catch (err: any) {
    console.warn('[delegationService] DB tables not ready:', err?.message);
  }
}

// =============================================================================
// DELEGATION SERVICE
// =============================================================================

export class DelegationService {
  /**
   * Create a new delegation
   */
  async createDelegation(
    delegatorId: string,
    request: CreateDelegationRequest,
    parentDelegationId?: string
  ): Promise<Delegation> {
    // Validate delegation types
    for (const type of request.delegationType) {
      if (!DELEGATION_CONFIG.allowedDelegationTypes.includes(type)) {
        throw new Error(`Invalid delegation type: ${type}`);
      }
    }

    // Check if delegator has authority to delegate
    if (parentDelegationId) {
      const parentDelegation = await dbGetDelegation(parentDelegationId);
      if (!parentDelegation) {
        throw new Error('Parent delegation not found');
      }
      if (!parentDelegation.canSubDelegate) {
        throw new Error('Parent delegation does not allow sub-delegation');
      }
      if (parentDelegation.currentDepth >= parentDelegation.maxDelegationDepth) {
        throw new Error('Maximum delegation depth reached');
      }
      // Can only delegate permissions you have
      for (const type of request.delegationType) {
        if (!parentDelegation.delegationType.includes(type)) {
          throw new Error(`Cannot delegate ${type} permission that you don't have`);
        }
      }
    }

    // Calculate depth
    let currentDepth = 0;
    if (parentDelegationId) {
      const parent = await dbGetDelegation(parentDelegationId);
      currentDepth = (parent?.currentDepth || 0) + 1;
    }

    // Determine validity period
    const validFrom = request.validFrom ? new Date(request.validFrom) : new Date();
    let validUntil: Date | undefined;
    if (request.validUntil) {
      validUntil = new Date(request.validUntil);
      const maxValidity = new Date();
      maxValidity.setDate(maxValidity.getDate() + DELEGATION_CONFIG.maxValidityDays);
      if (validUntil > maxValidity) {
        validUntil = maxValidity;
      }
    }

    const delegation: Delegation = {
      id: uuidv4(),
      delegatorId,
      delegateId: request.delegateId,
      delegateDid: request.delegateDid,
      delegateEmail: request.delegateEmail,
      delegateName: request.delegateName,
      documentId: request.documentId,
      organizationId: request.organizationId,
      delegationType: request.delegationType,
      maxAmount: request.maxAmount,
      requiresApproval: request.requiresApproval ?? false,
      canSubDelegate: request.canSubDelegate ?? false,
      maxDelegationDepth: request.maxDelegationDepth ?? DELEGATION_CONFIG.maxDelegationDepth,
      currentDepth,
      parentDelegationId,
      validFrom,
      validUntil,
      status: 'active',
      createdAt: new Date(),
      updatedAt: new Date(),
      usageCount: 0,
    };

    // Store delegation in DB
    await dbInsertDelegation(delegation);

    return delegation;
  }

  /**
   * Get delegation by ID
   */
  async getDelegation(id: string): Promise<Delegation | undefined> {
    return dbGetDelegation(id);
  }

  /**
   * Get all delegations granted by a user
   */
  async getDelegationsGrantedBy(delegatorId: string): Promise<Delegation[]> {
    return dbGetDelegationsByDelegator(delegatorId);
  }

  /**
   * Get all delegations received by a user
   */
  async getDelegationsReceivedBy(delegateId: string): Promise<Delegation[]> {
    return dbGetDelegationsByDelegate(delegateId);
  }

  /**
   * Get all delegations for a document
   */
  async getDelegationsForDocument(documentId: string): Promise<Delegation[]> {
    return dbGetDelegationsByDocument(documentId);
  }

  /**
   * Revoke a delegation
   */
  async revokeDelegation(delegationId: string, revokedBy: string, reason: string): Promise<Delegation> {
    const delegation = await dbGetDelegation(delegationId);
    if (!delegation) {
      throw new Error('Delegation not found');
    }

    // Check authority to revoke
    if (delegation.delegatorId !== revokedBy && delegation.delegateId !== revokedBy) {
      throw new Error('Not authorised to revoke this delegation');
    }

    delegation.status = 'revoked';
    delegation.revokedAt = new Date();
    delegation.revokedBy = revokedBy;
    delegation.revokedReason = reason;
    delegation.updatedAt = new Date();

    await dbUpdateDelegation(delegation);

    // Also revoke any sub-delegations
    await this.revokeSubDelegations(delegationId, revokedBy, 'Parent delegation revoked');

    return delegation;
  }

  /**
   * Revoke all sub-delegations of a delegation
   */
  private async revokeSubDelegations(parentId: string, revokedBy: string, reason: string): Promise<void> {
    const children = await dbGetSubDelegations(parentId, 'active');
    for (const delegation of children) {
      delegation.status = 'revoked';
      delegation.revokedAt = new Date();
      delegation.revokedBy = revokedBy;
      delegation.revokedReason = reason;
      delegation.updatedAt = new Date();
      await dbUpdateDelegation(delegation);

      // Recursively revoke sub-delegations
      await this.revokeSubDelegations(delegation.id, revokedBy, reason);
    }
  }

  /**
   * Validate if a user has delegated authority for an action
   */
  async validateDelegation(
    userId: string,
    documentId: string,
    requiredPermissions: DelegationType[],
    amount?: number
  ): Promise<DelegationValidationResult> {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Get active delegations for this user and document
    const allReceived = await this.getDelegationsReceivedBy(userId);
    const userDelegations = allReceived.filter(d => {
      // Must be active
      if (d.status !== 'active') return false;

      // Must be valid time-wise
      const now = new Date();
      if (d.validFrom > now) return false;
      if (d.validUntil && d.validUntil < now) return false;

      // Must match document or be global
      if (d.documentId && d.documentId !== documentId) return false;

      return true;
    });

    if (userDelegations.length === 0) {
      errors.push('No valid delegation found for this user and document');
      return { isValid: false, errors, warnings };
    }

    // Check if any delegation grants required permissions
    let effectivePermissions: DelegationType[] = [];
    let validDelegation: Delegation | undefined;

    for (const delegation of userDelegations) {
      const hasAllPermissions = requiredPermissions.every(
        perm => delegation.delegationType.includes(perm)
      );

      if (hasAllPermissions) {
        // Check amount limit
        if (amount && delegation.maxAmount && amount > delegation.maxAmount) {
          warnings.push(`Delegation has amount limit of ${delegation.maxAmount}`);
          continue;
        }

        validDelegation = delegation;
        effectivePermissions = delegation.delegationType;
        break;
      }
    }

    if (!validDelegation) {
      errors.push(`Missing required permissions: ${requiredPermissions.join(', ')}`);
      return { isValid: false, errors, warnings };
    }

    // Build delegation chain
    const chain = await this.buildDelegationChain(validDelegation);

    // Validate chain
    if (!chain.isValid) {
      errors.push(chain.invalidReason || 'Invalid delegation chain');
      return { isValid: false, errors, warnings, chain };
    }

    // Check if approval is required
    if (validDelegation.requiresApproval) {
      warnings.push('This action requires approval from the delegator');
    }

    // Record usage
    validDelegation.usageCount++;
    validDelegation.lastUsedAt = new Date();
    validDelegation.updatedAt = new Date();
    await dbUpdateDelegation(validDelegation);

    return {
      isValid: true,
      errors,
      warnings,
      chain,
      effectivePermissions,
    };
  }

  /**
   * Build the full delegation chain for a delegation
   */
  async buildDelegationChain(delegation: Delegation): Promise<DelegationChain> {
    const chain: DelegationChainLink[] = [];
    let current: Delegation | undefined = delegation;
    let depth = 0;

    while (current) {
      chain.unshift({
        delegationId: current.id,
        delegatorId: current.delegatorId,
        delegateId: current.delegateId,
        delegationType: current.delegationType,
        depth,
        status: current.status,
        validUntil: current.validUntil,
      });

      if (current.parentDelegationId) {
        current = await dbGetDelegation(current.parentDelegationId);
        depth++;
      } else {
        current = undefined;
      }
    }

    // Validate chain
    let isValid = true;
    let invalidReason: string | undefined;

    for (const link of chain) {
      if (link.status !== 'active') {
        isValid = false;
        invalidReason = `Delegation ${link.delegationId} is ${link.status}`;
        break;
      }
      if (link.validUntil && new Date(link.validUntil) < new Date()) {
        isValid = false;
        invalidReason = `Delegation ${link.delegationId} has expired`;
        break;
      }
    }

    return {
      rootDelegatorId: chain[0]?.delegatorId || delegation.delegatorId,
      chain,
      totalDepth: chain.length,
      isValid,
      invalidReason,
    };
  }

  /**
   * Check and update expired delegations
   */
  async processExpiredDelegations(): Promise<number> {
    if (!isDbAvailable()) return 0;
    try {
      const result = await query(
        `UPDATE svc_transfer_delegations
         SET status = 'expired', updated_at = NOW()
         WHERE status = 'active' AND valid_until IS NOT NULL AND valid_until < NOW()
         RETURNING id`
      );
      return result.rowCount ?? 0;
    } catch (err: any) {
      console.error('[delegationService] processExpiredDelegations error:', err?.message);
      return 0;
    }
  }

  /**
   * Get delegation statistics
   */
  async getStats(): Promise<{
    totalDelegations: number;
    activeDelegations: number;
    expiredDelegations: number;
    revokedDelegations: number;
    averageChainDepth: number;
  }> {
    if (!isDbAvailable()) {
      return { totalDelegations: 0, activeDelegations: 0, expiredDelegations: 0, revokedDelegations: 0, averageChainDepth: 0 };
    }
    try {
      const result = await query(
        `SELECT
           COUNT(*) AS total,
           COUNT(*) FILTER (WHERE status = 'active') AS active,
           COUNT(*) FILTER (WHERE status = 'expired') AS expired,
           COUNT(*) FILTER (WHERE status = 'revoked') AS revoked,
           COALESCE(AVG(current_depth) FILTER (WHERE status = 'active'), 0) AS avg_depth
         FROM svc_transfer_delegations`
      );
      const row = result.rows[0];
      return {
        totalDelegations: Number(row.total),
        activeDelegations: Number(row.active),
        expiredDelegations: Number(row.expired),
        revokedDelegations: Number(row.revoked),
        averageChainDepth: Number(row.avg_depth),
      };
    } catch {
      return { totalDelegations: 0, activeDelegations: 0, expiredDelegations: 0, revokedDelegations: 0, averageChainDepth: 0 };
    }
  }
}

// Export singleton instance
export const delegationService = new DelegationService();
