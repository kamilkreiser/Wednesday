/**
 * =============================================================================
 * GOVERNANCE TYPES
 * =============================================================================
 * Type definitions for DAO governance with token-weighted voting
 */

import { z } from 'zod';

// =============================================================================
// ENUMS
// =============================================================================

/**
 * Proposal status lifecycle
 */
export type ProposalStatus = 
  | 'draft'        // Not yet submitted
  | 'active'       // Open for voting
  | 'passed'       // Met approval threshold
  | 'failed'       // Did not meet threshold
  | 'queued'       // Passed, waiting for timelock
  | 'executed'     // Successfully executed
  | 'cancelled'    // Cancelled by proposer or governance
  | 'expired';     // Voting period ended without quorum

/**
 * Proposal category/type
 */
export type ProposalCategory = 
  | 'parameter_change'    // Change platform parameters
  | 'fee_adjustment'      // Modify fee structure
  | 'treasury_spend'      // Spend from treasury
  | 'upgrade'             // Platform upgrade
  | 'emergency'           // Emergency action
  | 'governance_change'   // Change governance rules
  | 'whitelist'           // Add/remove whitelisted verifiers
  | 'general';            // General governance proposal

/**
 * Vote option
 */
export type VoteOption = 'for' | 'against' | 'abstain';

/**
 * Stake tier for vote multipliers
 */
export type StakeTier = 'basic' | 'staker' | 'validator' | 'partner';

// =============================================================================
// VOTE POWER CONFIGURATION
// =============================================================================

/**
 * Vote multipliers by tier (basis points, 10000 = 1x)
 */
export const VOTE_MULTIPLIERS: Record<StakeTier, number> = {
  basic: 10000,     // 1x
  staker: 10000,    // 1x
  validator: 15000, // 1.5x
  partner: 20000,   // 2x
};

/**
 * Tier thresholds in SECURA tokens
 */
export const TIER_THRESHOLDS: Record<StakeTier, number> = {
  basic: 0,
  staker: 1000,
  validator: 10000,
  partner: 100000,
};

// =============================================================================
// CORE TYPES
// =============================================================================

/**
 * Governance participant (DRep or committee member)
 */
export interface GovernanceParticipant {
  id: string;
  walletAddress: string;
  did?: string;
  
  // Staking info
  stakedAmount: number;
  tier: StakeTier;
  votePower: number;         // Calculated: stakedAmount * multiplier
  
  // Role
  isDRep: boolean;
  isConstitutionalCommittee: boolean;
  
  // Activity
  proposalsCreated: number;
  votesCast: number;
  lastActiveAt: Date;
  
  joinedAt: Date;
}

/**
 * Vote record
 */
export interface Vote {
  id: string;
  proposalId: string;
  voterId: string;
  voterAddress: string;
  
  vote: VoteOption;
  votePower: number;          // Power at time of vote
  tier: StakeTier;            // Tier at time of vote
  
  reason?: string;            // Optional voting reason
  signature?: string;         // On-chain signature
  
  votedAt: Date;
  txHash?: string;            // On-chain tx if anchored
}

/**
 * Proposal
 */
export interface Proposal {
  id: string;
  proposalNumber: number;     // Sequential number for display
  
  // Content
  title: string;
  description: string;
  category: ProposalCategory;
  
  // Proposer
  proposerId: string;
  proposerAddress: string;
  
  // Status
  status: ProposalStatus;
  
  // Execution details (for executable proposals)
  actions?: ProposalAction[];
  
  // Voting configuration
  votingConfig: VotingConfig;
  
  // Timestamps
  createdAt: Date;
  submittedAt?: Date;         // When moved from draft to active
  votingStartsAt?: Date;
  votingEndsAt?: Date;
  queuedAt?: Date;            // When moved to timelock queue
  executionEta?: Date;        // When can be executed
  executedAt?: Date;
  cancelledAt?: Date;
  
  // Vote tallies
  votesFor: number;           // Total vote power for
  votesAgainst: number;       // Total vote power against
  votesAbstain: number;       // Total vote power abstain
  totalVotePower: number;     // Total eligible vote power at snapshot
  voterCount: number;         // Number of unique voters
  
  // Individual votes
  votes: Vote[];
  
  // On-chain reference
  txHash?: string;
  datumHash?: string;
  
  // Metadata
  discussionUrl?: string;
  ipfsHash?: string;          // Full proposal content on IPFS
}

/**
 * Proposal action (for executable proposals)
 */
export interface ProposalAction {
  id: string;
  actionType: 'contract_call' | 'parameter_update' | 'treasury_transfer' | 'upgrade';
  
  // Target
  targetContract?: string;
  targetFunction?: string;
  
  // Parameters
  parameters: Record<string, unknown>;
  
  // For treasury spend
  recipient?: string;
  amount?: number;
  
  // Execution
  executed: boolean;
  executedAt?: Date;
  executionTxHash?: string;
}

/**
 * Voting configuration for a proposal
 */
export interface VotingConfig {
  // Thresholds (basis points, 10000 = 100%)
  approvalThresholdBps: number;      // Required % of votes for approval
  quorumThresholdBps: number;        // Required % participation
  
  // Durations
  votingPeriodHours: number;
  timelockPeriodHours: number;       // Delay after passing before execution
  
  // Special rules
  requiresConstitutionalApproval: boolean;
  constitutionalThreshold?: number;  // Required committee votes
  
  // Snapshot
  snapshotBlock?: number;            // Block for vote power snapshot
  snapshotTimestamp?: Date;
}

/**
 * Governance configuration (global settings)
 */
export interface GovernanceConfig {
  // Default voting parameters
  defaultApprovalThresholdBps: number;
  defaultQuorumThresholdBps: number;
  defaultVotingPeriodHours: number;
  defaultTimelockPeriodHours: number;
  
  // Proposal requirements
  minProposalStake: number;          // Min stake to create proposal
  proposalDeposit: number;           // Deposit required (refunded if passes)
  maxActiveProposals: number;
  
  // Emergency settings
  emergencyMultisigThreshold: number;
  emergencyTimelockHours: number;
  
  // Constitutional committee
  constitutionalCommitteeSize: number;
  constitutionalVetoThreshold: number;
  
  // Category-specific overrides
  categoryOverrides: Partial<Record<ProposalCategory, Partial<VotingConfig>>>;
}

/**
 * Delegation record
 */
export interface VoteDelegation {
  id: string;
  delegatorId: string;
  delegatorAddress: string;
  
  delegateId: string;
  delegateAddress: string;
  
  delegatedPower: number;
  
  // Scope
  allProposals: boolean;
  categories?: ProposalCategory[];    // If not all
  
  createdAt: Date;
  expiresAt?: Date;
  revokedAt?: Date;
}

// =============================================================================
// DEFAULT CONFIGURATIONS
// =============================================================================

export const DEFAULT_GOVERNANCE_CONFIG: GovernanceConfig = {
  defaultApprovalThresholdBps: 5000,  // 50% approval
  defaultQuorumThresholdBps: 1000,    // 10% participation
  defaultVotingPeriodHours: 168,      // 7 days
  defaultTimelockPeriodHours: 48,     // 2 days
  
  minProposalStake: 1000,             // Must be at least Staker tier
  proposalDeposit: 100,               // 100 SECURA deposit
  maxActiveProposals: 20,
  
  emergencyMultisigThreshold: 3,
  emergencyTimelockHours: 6,
  
  constitutionalCommitteeSize: 5,
  constitutionalVetoThreshold: 3,
  
  categoryOverrides: {
    emergency: {
      votingPeriodHours: 24,
      timelockPeriodHours: 6,
      requiresConstitutionalApproval: true,
      constitutionalThreshold: 3,
    },
    governance_change: {
      approvalThresholdBps: 6700,     // 67% for governance changes
      quorumThresholdBps: 2000,       // 20% quorum
      timelockPeriodHours: 72,
    },
    treasury_spend: {
      approvalThresholdBps: 6000,     // 60% for treasury
      requiresConstitutionalApproval: true,
      constitutionalThreshold: 2,
    },
    upgrade: {
      approvalThresholdBps: 6700,
      quorumThresholdBps: 1500,
      timelockPeriodHours: 72,
      requiresConstitutionalApproval: true,
    },
  },
};

export const DEFAULT_VOTING_CONFIG: VotingConfig = {
  approvalThresholdBps: 5000,
  quorumThresholdBps: 1000,
  votingPeriodHours: 168,
  timelockPeriodHours: 48,
  requiresConstitutionalApproval: false,
};

// =============================================================================
// ZOD SCHEMAS
// =============================================================================

export const CreateProposalSchema = z.object({
  title: z.string().min(10).max(200),
  description: z.string().min(50).max(10000),
  category: z.enum([
    'parameter_change', 'fee_adjustment', 'treasury_spend', 
    'upgrade', 'emergency', 'governance_change', 'whitelist', 'general'
  ]),
  actions: z.array(z.object({
    actionType: z.enum(['contract_call', 'parameter_update', 'treasury_transfer', 'upgrade']),
    targetContract: z.string().optional(),
    targetFunction: z.string().optional(),
    parameters: z.record(z.unknown()),
    recipient: z.string().optional(),
    amount: z.number().optional(),
  })).optional(),
  discussionUrl: z.string().url().optional(),
  votingConfig: z.object({
    approvalThresholdBps: z.number().min(1).max(10000).optional(),
    quorumThresholdBps: z.number().min(1).max(10000).optional(),
    votingPeriodHours: z.number().min(1).max(720).optional(),
    timelockPeriodHours: z.number().min(0).max(168).optional(),
  }).optional(),
});

export const CastVoteSchema = z.object({
  proposalId: z.string().uuid(),
  vote: z.enum(['for', 'against', 'abstain']),
  reason: z.string().max(1000).optional(),
});

export const DelegateVoteSchema = z.object({
  delegateId: z.string(),
  // KS-430: the delegate route handler destructures only
  // { delegateId, allProposals, categories, expiresAt } — delegateAddress is
  // never read, so requiring it made a spec-compliant `{ delegateId, allProposals }`
  // request earn a 400 on a field the op ignores. Loosened to optional so the
  // published contract and the validator agree; the handler behaviour is unchanged.
  delegateAddress: z.string().optional(),
  allProposals: z.boolean(),
  categories: z.array(z.enum([
    'parameter_change', 'fee_adjustment', 'treasury_spend',
    'upgrade', 'emergency', 'governance_change', 'whitelist', 'general'
  ])).optional(),
  // KS-444: the published spec emits `format: date-time` (RFC 3339 §5.6), which
  // permits a numeric UTC offset as well as `Z` — but bare `.datetime()` accepts
  // only `Z`, so a spec-legal `2030-01-01T00:00:00+05:30` earned a 400 (the
  // KS-427 class). `{ offset: true }` accepts the legal grammar; the handler
  // normalises to UTC via `new Date(expiresAt)` (KS-201: accept the instant at
  // the boundary, store UTC).
  expiresAt: z.string().datetime({ offset: true }).optional(),
});

// KS-444: request schema for POST /participants/register, mirroring the
// published ParticipantRegisterRequest spec schema exactly. The old ad-hoc
// truthy check (`if (!walletAddress || typeof stakedAmount !== 'number')`)
// accepted any truthy walletAddress — a spec-violating `walletAddress: {}`
// registered a participant with an object stored as its address. Enforce only
// what the spec declares: walletAddress non-empty string (min 1 matches the
// pre-existing rejection of ''), stakedAmount number, optional did string and
// role booleans.
// KS-498: stakedAmount is bounded — an unbounded double (±6.8e307 from the
// fuzzer, or JSON 1e999 → Infinity) overflows the votePower multiply to
// ±Infinity, which JSON-serialises to null and violates the published
// GovernanceParticipant response schema. Negative stake is meaningless and
// produced a negative/overflowed votePower. Ceiling mirrors the spec
// (governance.openapi.ts ParticipantRegisterRequest).
export const RegisterParticipantSchema = z.object({
  walletAddress: z.string().min(1),
  stakedAmount: z.number().nonnegative().finite().max(1e12),
  did: z.string().optional(),
  isDRep: z.boolean().optional(),
  isConstitutionalCommittee: z.boolean().optional(),
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Calculate tier from staked amount
 */
export function calculateTier(stakedAmount: number): StakeTier {
  if (stakedAmount >= TIER_THRESHOLDS.partner) return 'partner';
  if (stakedAmount >= TIER_THRESHOLDS.validator) return 'validator';
  if (stakedAmount >= TIER_THRESHOLDS.staker) return 'staker';
  return 'basic';
}

/**
 * Calculate vote power from stake and tier
 */
export function calculateVotePower(stakedAmount: number, tier: StakeTier): number {
  const multiplier = VOTE_MULTIPLIERS[tier];
  return Math.floor((stakedAmount * multiplier) / 10000);
}

/**
 * Check if proposal has passed
 */
export function hasProposalPassed(proposal: Proposal): boolean {
  const totalVotes = proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain;
  
  // Check quorum
  const participationBps = Math.floor((totalVotes / proposal.totalVotePower) * 10000);
  if (participationBps < proposal.votingConfig.quorumThresholdBps) {
    return false;
  }
  
  // Check approval (exclude abstentions from approval calculation)
  const votesConsidered = proposal.votesFor + proposal.votesAgainst;
  if (votesConsidered === 0) return false;
  
  const approvalBps = Math.floor((proposal.votesFor / votesConsidered) * 10000);
  return approvalBps >= proposal.votingConfig.approvalThresholdBps;
}

/**
 * Get voting config for category with overrides
 */
export function getVotingConfigForCategory(
  category: ProposalCategory,
  config: GovernanceConfig = DEFAULT_GOVERNANCE_CONFIG
): VotingConfig {
  const override = config.categoryOverrides[category] || {};
  
  return {
    approvalThresholdBps: override.approvalThresholdBps ?? config.defaultApprovalThresholdBps,
    quorumThresholdBps: override.quorumThresholdBps ?? config.defaultQuorumThresholdBps,
    votingPeriodHours: override.votingPeriodHours ?? config.defaultVotingPeriodHours,
    timelockPeriodHours: override.timelockPeriodHours ?? config.defaultTimelockPeriodHours,
    requiresConstitutionalApproval: override.requiresConstitutionalApproval ?? false,
    constitutionalThreshold: override.constitutionalThreshold,
  };
}
