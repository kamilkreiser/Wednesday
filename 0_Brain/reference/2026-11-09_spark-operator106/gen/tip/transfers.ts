/**
 * =============================================================================
 * TRANSFERS MODULE
 * =============================================================================
 * SDK module for ownership transfers and delegations
 */

import { HttpClient, PaginatedResponse } from '../client';

// =============================================================================
// TYPES
// =============================================================================

export type TransferStatus = 'pending' | 'approved' | 'rejected' | 'completed' | 'cancelled';
export type DelegationType = 'full' | 'approve' | 'initiate' | 'view' | 'sign' | 'manage_access';
export type DelegationStatus = 'active' | 'revoked' | 'expired';

export interface Transfer {
  id: string;
  documentId: string;
  fromUserId: string;
  toUserId: string;
  status: TransferStatus;
  reason?: string;
  workflowType: string;
  approvals: Array<{
    userId: string;
    action: string;
    timestamp: string;
    comment?: string;
  }>;
  createdAt: string;
  completedAt?: string;
}

export interface Delegation {
  id: string;
  grantorId: string;
  delegateId: string;
  type: DelegationType;
  status: DelegationStatus;
  scope: string[];
  constraints?: {
    documentTypes?: string[];
    maxAmount?: number;
    maxDelegations?: number;
  };
  expiresAt: string;
  createdAt: string;
  revokedAt?: string;
}

export interface InitiateTransferInput {
  documentId: string;
  toUserId: string;
  reason?: string;
  requiresApproval?: boolean;
  workflowType?: 'single' | 'sequential' | 'parallel' | 'threshold';
}

export interface CreateDelegationInput {
  delegateId: string;
  type: DelegationType;
  scope: string[];
  constraints?: {
    documentTypes?: string[];
    maxAmount?: number;
    maxDelegations?: number;
  };
  expiresAt: string;
}

// =============================================================================
// MODULE
// =============================================================================

export class TransfersModule {
  constructor(private http: HttpClient) {}

  // ---------------------------------------------------------------------------
  // TRANSFERS
  // ---------------------------------------------------------------------------

  /**
   * Initiate a new transfer
   */
  async initiate(input: InitiateTransferInput): Promise<Transfer> {
    return this.http.post('/api/transfers/initiate', input);
  }

  /**
   * List transfers
   */
  async list(params?: {
    status?: TransferStatus;
    documentId?: string;
    limit?: number;
    offset?: number;
  }): Promise<PaginatedResponse<Transfer>> {
    return this.http.get('/api/transfers', { params: params as Record<string, unknown> });
  }

  /**
   * Get transfer by ID
   */
  async get(id: string): Promise<Transfer> {
    return this.http.get(`/api/transfers/${id}`);
  }

  /**
   * Approve or reject a transfer
   */
  async approve(
    transferId: string,
    action: 'approve' | 'reject' | 'accept',
    options?: {
      comment?: string;
      signature?: string;
    }
  ): Promise<Transfer> {
    return this.http.post(`/api/transfers/${transferId}/approve`, {
      action,
      ...options,
    });
  }

  /**
   * Cancel a transfer
   */
  async cancel(transferId: string, reason: string): Promise<Transfer> {
    return this.http.post(`/api/transfers/${transferId}/cancel`, { reason });
  }

  // ---------------------------------------------------------------------------
  // DELEGATIONS
  // ---------------------------------------------------------------------------

  /**
   * Create a new delegation
   */
  async createDelegation(input: CreateDelegationInput): Promise<Delegation> {
    return this.http.post('/api/delegations', input);
  }

  /**
   * List delegations
   */
  async listDelegations(params?: {
    received?: boolean;
    type?: DelegationType;
    status?: DelegationStatus;
  }): Promise<{ delegations: Delegation[] }> {
    return this.http.get('/api/delegations', { params: params as Record<string, unknown> });
  }

  /**
   * Get delegation by ID
   */
  async getDelegation(id: string): Promise<Delegation> {
    return this.http.get(`/api/delegations/${id}`);
  }

  /**
   * Revoke a delegation
   */
  async revokeDelegation(id: string, reason?: string): Promise<Delegation> {
    return this.http.post(`/api/delegations/${id}/revoke`, { reason });
  }

  /**
   * Validate delegation chain
   */
  async validateDelegation(input: {
    delegatorId: string;
    delegateId: string;
    action: string;
  }): Promise<{
    valid: boolean;
    chain: Delegation[];
    reason?: string;
  }> {
    return this.http.post('/api/delegations/validate', input);
  }
}
