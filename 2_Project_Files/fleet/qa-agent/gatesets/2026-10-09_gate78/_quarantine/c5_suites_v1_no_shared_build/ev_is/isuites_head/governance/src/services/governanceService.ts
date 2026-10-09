/**
 * =============================================================================
 * GOVERNANCE SERVICE
 * =============================================================================
 * Core service for DAO governance - proposals, voting, execution
 *
 * Storage: PostgreSQL only (no in-memory Maps).
 * Every read/write goes through the DB via query() from db.ts.
 * =============================================================================
 */

import { v4 as uuidv4 } from 'uuid';
import {
  Proposal,
  ProposalStatus,
  ProposalCategory,
  ProposalAction,
  Vote,
  VoteOption,
  GovernanceParticipant,
  VoteDelegation,
  GovernanceConfig,
  VotingConfig,
  StakeTier,
  DEFAULT_GOVERNANCE_CONFIG,
  calculateTier,
  calculateVotePower,
  hasProposalPassed,
  getVotingConfigForCategory,
} from '../types/governance.types';
import {
  BadRequestError,
  ConflictError,
  ForbiddenError,
  NotFoundError,
} from '@secuura/shared';
import { query, isDbAvailable } from '../db';
import { logger } from '../utils/logger';

// =============================================================================
// PROPOSAL COUNTER (kept in memory, seeded from DB on startup)
// =============================================================================

let proposalCounter = 0;

// Initialize with mock governance config
let governanceConfig: GovernanceConfig = { ...DEFAULT_GOVERNANCE_CONFIG };

// =============================================================================
// ROW → DOMAIN MAPPERS
// =============================================================================

// KS-594: `svc_proposals.voting_config` is `JSONB NOT NULL DEFAULT '{}'`, so a
// row can legitimately hold an EMPTY config — and every consumer of
// `proposal.votingConfig` reads a field off it without a default. Submitting
// such a proposal computed `new Date(now + undefined * …)` → `Invalid time
// value` from `.toISOString()`, i.e. a raw 500 on a request that was fine; the
// same undefined reached the finalize quorum and timelock maths, where it fails
// silently instead of loudly. Filling the gaps at the row boundary fixes all
// five consumers at once rather than guarding each call site.
function normaliseVotingConfig(stored: unknown, category: unknown): VotingConfig {
  const defaults = getVotingConfigForCategory(
    (category as ProposalCategory) || 'general',
    governanceConfig,
  );
  const partial = (stored && typeof stored === 'object' ? stored : {}) as Partial<VotingConfig>;
  return { ...defaults, ...partial };
}

function rowToProposal(r: any): Proposal {
  return {
    id: r.id,
    proposalNumber: r.proposal_number,
    title: r.title,
    description: r.description,
    category: r.category,
    proposerId: r.proposer_id,
    proposerAddress: r.proposer_address,
    status: r.status,
    actions: typeof r.actions === 'string' ? JSON.parse(r.actions) : (r.actions || []),
    votingConfig: normaliseVotingConfig(
      typeof r.voting_config === 'string' ? JSON.parse(r.voting_config) : r.voting_config,
      r.category,
    ),
    createdAt: new Date(r.created_at),
    submittedAt: r.submitted_at ? new Date(r.submitted_at) : undefined,
    votingStartsAt: r.voting_starts_at ? new Date(r.voting_starts_at) : undefined,
    votingEndsAt: r.voting_ends_at ? new Date(r.voting_ends_at) : undefined,
    queuedAt: r.queued_at ? new Date(r.queued_at) : undefined,
    executionEta: r.execution_eta ? new Date(r.execution_eta) : undefined,
    executedAt: r.executed_at ? new Date(r.executed_at) : undefined,
    cancelledAt: r.cancelled_at ? new Date(r.cancelled_at) : undefined,
    votesFor: Number(r.votes_for || 0),
    votesAgainst: Number(r.votes_against || 0),
    votesAbstain: Number(r.votes_abstain || 0),
    totalVotePower: Number(r.total_vote_power || 0),
    voterCount: r.voter_count || 0,
    votes: typeof r.votes === 'string' ? JSON.parse(r.votes) : (r.votes || []),
    txHash: r.tx_hash,
    datumHash: r.datum_hash,
    discussionUrl: r.discussion_url,
    ipfsHash: r.ipfs_hash,
  };
}

function rowToParticipant(r: any): GovernanceParticipant {
  return {
    id: r.id,
    walletAddress: r.wallet_address,
    did: r.did || undefined,
    stakedAmount: Number(r.staked_amount || 0),
    tier: r.tier || 'basic',
    votePower: Number(r.vote_power || 0),
    isDRep: r.is_drep ?? false,
    isConstitutionalCommittee: r.is_constitutional_committee ?? false,
    proposalsCreated: r.proposals_created || 0,
    votesCast: r.votes_cast || 0,
    lastActiveAt: r.last_active_at ? new Date(r.last_active_at) : new Date(),
    joinedAt: r.joined_at ? new Date(r.joined_at) : new Date(),
  };
}

function rowToDelegation(r: any): VoteDelegation {
  return {
    id: r.id,
    delegatorId: r.delegator_id,
    delegatorAddress: r.delegator_address,
    delegateId: r.delegate_id,
    delegateAddress: r.delegate_address,
    delegatedPower: Number(r.delegated_power || 0),
    allProposals: r.all_proposals ?? true,
    categories: r.categories ? (typeof r.categories === 'string' ? JSON.parse(r.categories) : r.categories) : undefined,
    createdAt: new Date(r.created_at),
    expiresAt: r.expires_at ? new Date(r.expires_at) : undefined,
    revokedAt: r.revoked_at ? new Date(r.revoked_at) : undefined,
  };
}

// =============================================================================
// DB WRITE HELPERS
// =============================================================================

async function dbSaveProposal(p: Proposal): Promise<void> {
  try {
    await query(
      `INSERT INTO svc_proposals (id, title, description, category, proposer_id, proposer_address,
         status, voting_config, actions, votes_for, votes_against, votes_abstain,
         total_vote_power, voter_count, votes, tx_hash, datum_hash, discussion_url, ipfs_hash,
         submitted_at, voting_starts_at, voting_ends_at, queued_at, execution_eta, executed_at,
         cancelled_at, created_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27)
       ON CONFLICT (id) DO UPDATE SET
         status = EXCLUDED.status, votes_for = EXCLUDED.votes_for, votes_against = EXCLUDED.votes_against,
         votes_abstain = EXCLUDED.votes_abstain, total_vote_power = EXCLUDED.total_vote_power,
         voter_count = EXCLUDED.voter_count, votes = EXCLUDED.votes, tx_hash = EXCLUDED.tx_hash,
         executed_at = EXCLUDED.executed_at, cancelled_at = EXCLUDED.cancelled_at`,
      [p.id, p.title, p.description, p.category, p.proposerId, p.proposerAddress,
       p.status, JSON.stringify(p.votingConfig), JSON.stringify(p.actions || []),
       p.votesFor, p.votesAgainst, p.votesAbstain, p.totalVotePower, p.voterCount,
       JSON.stringify(p.votes || []), p.txHash || null, p.datumHash || null,
       p.discussionUrl || null, p.ipfsHash || null, p.submittedAt || null,
       p.votingStartsAt || null, p.votingEndsAt || null, p.queuedAt || null,
       p.executionEta || null, p.executedAt || null, p.cancelledAt || null,
       p.createdAt]
    );
  } catch (err: any) {
    logger.error('DB save proposal failed', { error: err instanceof Error ? err.message : String(err) });
    throw err;
  }
}

async function dbSaveParticipant(p: GovernanceParticipant): Promise<void> {
  try {
    await query(
      `INSERT INTO svc_governance_participants (id, wallet_address, did, staked_amount, tier, vote_power,
         is_drep, is_constitutional_committee, proposals_created, votes_cast, last_active_at, joined_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
       ON CONFLICT (id) DO UPDATE SET
         staked_amount = EXCLUDED.staked_amount, tier = EXCLUDED.tier, vote_power = EXCLUDED.vote_power,
         is_drep = EXCLUDED.is_drep, proposals_created = EXCLUDED.proposals_created,
         votes_cast = EXCLUDED.votes_cast, last_active_at = EXCLUDED.last_active_at`,
      [p.id, p.walletAddress, p.did || null, p.stakedAmount, p.tier, p.votePower,
       p.isDRep, p.isConstitutionalCommittee, p.proposalsCreated, p.votesCast,
       p.lastActiveAt, p.joinedAt]
    );
  } catch (err: any) {
    logger.error('DB save participant failed', { error: err instanceof Error ? err.message : String(err) });
    throw err;
  }
}

async function dbSaveDelegation(d: VoteDelegation): Promise<void> {
  try {
    await query(
      `INSERT INTO svc_vote_delegations (id, delegator_id, delegator_address, delegate_id, delegate_address,
         delegated_power, all_proposals, categories, created_at, expires_at, revoked_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
       ON CONFLICT (id) DO UPDATE SET
         delegated_power = EXCLUDED.delegated_power, revoked_at = EXCLUDED.revoked_at`,
      [d.id, d.delegatorId, d.delegatorAddress, d.delegateId, d.delegateAddress,
       d.delegatedPower, d.allProposals, d.categories ? JSON.stringify(d.categories) : null,
       d.createdAt, d.expiresAt || null, d.revokedAt || null]
    );
  } catch (err: any) {
    logger.error('DB save delegation failed', { error: err instanceof Error ? err.message : String(err) });
    throw err;
  }
}

// =============================================================================
// DB READ HELPERS
// =============================================================================

async function dbGetProposal(id: string): Promise<Proposal | undefined> {
  try {
    const result = await query('SELECT * FROM svc_proposals WHERE id = $1', [id]);
    if (result.rows.length > 0) return rowToProposal(result.rows[0]);
  } catch (err: any) {
    logger.error('DB get proposal failed', { id, error: err instanceof Error ? err.message : String(err) });
  }
  return undefined;
}

async function dbGetAllProposals(filters?: {
  status?: ProposalStatus | ProposalStatus[];
  category?: ProposalCategory;
  proposerId?: string;
}): Promise<Proposal[]> {
  try {
    const conditions: string[] = [];
    const params: unknown[] = [];
    let idx = 1;

    if (filters?.status) {
      const statuses = Array.isArray(filters.status) ? filters.status : [filters.status];
      conditions.push(`status = ANY($${idx})`);
      params.push(statuses);
      idx++;
    }
    if (filters?.category) {
      conditions.push(`category = $${idx}`);
      params.push(filters.category);
      idx++;
    }
    if (filters?.proposerId) {
      conditions.push(`proposer_id = $${idx}`);
      params.push(filters.proposerId);
      idx++;
    }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';
    const result = await query(`SELECT * FROM svc_proposals ${where} ORDER BY created_at DESC`, params);
    return result.rows.map(rowToProposal);
  } catch (err: any) {
    logger.error('DB get all proposals failed', { error: err instanceof Error ? err.message : String(err) });
    return [];
  }
}

async function dbGetParticipant(id: string): Promise<GovernanceParticipant | undefined> {
  try {
    const result = await query('SELECT * FROM svc_governance_participants WHERE id = $1', [id]);
    if (result.rows.length > 0) return rowToParticipant(result.rows[0]);
  } catch (err: any) {
    logger.error('DB get participant failed', { id, error: err instanceof Error ? err.message : String(err) });
  }
  return undefined;
}

async function dbGetParticipantByAddress(walletAddress: string): Promise<GovernanceParticipant | undefined> {
  try {
    const result = await query('SELECT * FROM svc_governance_participants WHERE wallet_address = $1', [walletAddress]);
    if (result.rows.length > 0) return rowToParticipant(result.rows[0]);
  } catch (err: any) {
    logger.error('DB get participant by address failed', { walletAddress, error: err instanceof Error ? err.message : String(err) });
  }
  return undefined;
}

async function dbGetAllParticipants(filters?: {
  isDRep?: boolean;
  isConstitutionalCommittee?: boolean;
  minTier?: StakeTier;
}): Promise<GovernanceParticipant[]> {
  try {
    const conditions: string[] = [];
    const params: unknown[] = [];
    let idx = 1;

    if (filters?.isDRep !== undefined) {
      conditions.push(`is_drep = $${idx}`);
      params.push(filters.isDRep);
      idx++;
    }
    if (filters?.isConstitutionalCommittee !== undefined) {
      conditions.push(`is_constitutional_committee = $${idx}`);
      params.push(filters.isConstitutionalCommittee);
      idx++;
    }
    if (filters?.minTier) {
      const tierOrder: StakeTier[] = ['basic', 'staker', 'validator', 'partner'];
      const minIndex = tierOrder.indexOf(filters.minTier);
      const validTiers = tierOrder.slice(minIndex);
      conditions.push(`tier = ANY($${idx})`);
      params.push(validTiers);
      idx++;
    }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';
    const result = await query(`SELECT * FROM svc_governance_participants ${where}`, params);
    return result.rows.map(rowToParticipant);
  } catch (err: any) {
    logger.error('DB get all participants failed', { error: err instanceof Error ? err.message : String(err) });
    return [];
  }
}

async function dbGetActiveDelegations(filters?: {
  delegateId?: string;
  delegatorId?: string;
}): Promise<VoteDelegation[]> {
  try {
    const conditions: string[] = ['revoked_at IS NULL', '(expires_at IS NULL OR expires_at > NOW())'];
    const params: unknown[] = [];
    let idx = 1;

    if (filters?.delegateId) {
      conditions.push(`delegate_id = $${idx}`);
      params.push(filters.delegateId);
      idx++;
    }
    if (filters?.delegatorId) {
      conditions.push(`delegator_id = $${idx}`);
      params.push(filters.delegatorId);
      idx++;
    }

    const where = `WHERE ${conditions.join(' AND ')}`;
    const result = await query(`SELECT * FROM svc_vote_delegations ${where}`, params);
    return result.rows.map(rowToDelegation);
  } catch (err: any) {
    logger.error('DB get active delegations failed', { error: err instanceof Error ? err.message : String(err) });
    return [];
  }
}

// =============================================================================
// STARTUP — verify DB is ready and seed the proposal counter
// =============================================================================

/**
 * Verify the database is reachable and seed the proposal counter.
 * Replaces the old loadFromDb() that populated in-memory Maps.
 */
export async function verifyDbReady(): Promise<void> {
  if (!isDbAvailable()) {
    logger.warn('Database not available — governance service cannot operate without DB');
    return;
  }

  try {
    const result = await query('SELECT COALESCE(MAX(proposal_number), 0) AS max_num FROM svc_proposals');
    proposalCounter = Number(result.rows[0]?.max_num || 0);
    logger.info('DB ready — proposal counter seeded', { proposalCounter });
  } catch (err: any) {
    logger.error('Failed to seed proposal counter from DB', { error: err instanceof Error ? err.message : String(err) });
  }
}

// Keep loadFromDb as an alias so existing callers don't break at import time
export const loadFromDb = verifyDbReady;

// =============================================================================
// PARTICIPANT MANAGEMENT
// =============================================================================

/**
 * Register or update a governance participant
 */
export async function registerParticipant(
  walletAddress: string,
  stakedAmount: number,
  options?: {
    did?: string;
    isDRep?: boolean;
    isConstitutionalCommittee?: boolean;
  }
): Promise<GovernanceParticipant> {
  const existing = await dbGetParticipantByAddress(walletAddress);

  const tier = calculateTier(stakedAmount);
  const votePower = calculateVotePower(stakedAmount, tier);

  const participant: GovernanceParticipant = {
    id: existing?.id || uuidv4(),
    walletAddress,
    did: options?.did,
    stakedAmount,
    tier,
    votePower,
    isDRep: options?.isDRep ?? (stakedAmount >= 1000),
    isConstitutionalCommittee: options?.isConstitutionalCommittee ?? false,
    proposalsCreated: existing?.proposalsCreated ?? 0,
    votesCast: existing?.votesCast ?? 0,
    lastActiveAt: new Date(),
    joinedAt: existing?.joinedAt ?? new Date(),
  };

  await dbSaveParticipant(participant);
  logger.info('Participant registered', {
    participantId: participant.id,
    tier,
    votePower
  });
  return participant;
}

/**
 * Get participant by ID or wallet address
 */
export async function getParticipant(idOrAddress: string): Promise<GovernanceParticipant | undefined> {
  const byId = await dbGetParticipant(idOrAddress);
  if (byId) return byId;
  return dbGetParticipantByAddress(idOrAddress);
}

/**
 * Get all participants with optional filters
 */
export async function getParticipants(filters?: {
  isDRep?: boolean;
  isConstitutionalCommittee?: boolean;
  minTier?: StakeTier;
}): Promise<GovernanceParticipant[]> {
  return dbGetAllParticipants(filters);
}

/**
 * Get total vote power across all DRep participants
 */
export async function getTotalVotePower(): Promise<number> {
  try {
    const result = await query(
      'SELECT COALESCE(SUM(vote_power), 0) AS total FROM svc_governance_participants WHERE is_drep = true'
    );
    return Number(result.rows[0]?.total || 0);
  } catch (err: any) {
    logger.error('DB get total vote power failed', { error: err instanceof Error ? err.message : String(err) });
    return 0;
  }
}

// =============================================================================
// PROPOSAL MANAGEMENT
// =============================================================================

/**
 * Create a new proposal (draft status)
 */
export async function createProposal(
  proposerId: string,
  title: string,
  description: string,
  category: ProposalCategory,
  options?: {
    actions?: Omit<ProposalAction, 'id' | 'executed'>[];
    discussionUrl?: string;
    customVotingConfig?: Partial<VotingConfig>;
  }
): Promise<Proposal> {
  let proposer = await dbGetParticipant(proposerId);

  if (!proposer) {
    // Auto-register the user as a governance participant with basic tier
    proposer = await registerParticipant(proposerId, governanceConfig.minProposalStake, {
      isDRep: false,
      isConstitutionalCommittee: false,
    });
    // Update the participant's id to match the proposerId for lookup
    if (proposer.id !== proposerId) {
      // Delete the auto-generated record and re-save with the correct id
      try {
        await query('DELETE FROM svc_governance_participants WHERE id = $1', [proposer.id]);
      } catch { /* best effort */ }
      proposer.id = proposerId;
      await dbSaveParticipant(proposer);
    }
  }

  if (proposer.stakedAmount < governanceConfig.minProposalStake) {
    throw new BadRequestError(`Minimum stake of ${governanceConfig.minProposalStake} required to create proposals`);
  }

  // Check max active proposals
  const activeProposals = await dbGetAllProposals({ status: ['active', 'queued'] });
  if (activeProposals.length >= governanceConfig.maxActiveProposals) {
    throw new ConflictError(`Maximum of ${governanceConfig.maxActiveProposals} active proposals reached`);
  }

  // Get voting config with category-specific overrides
  const baseConfig = getVotingConfigForCategory(category, governanceConfig);
  const votingConfig: VotingConfig = {
    ...baseConfig,
    ...options?.customVotingConfig,
  };

  proposalCounter++;

  const proposal: Proposal = {
    id: uuidv4(),
    proposalNumber: proposalCounter,
    title,
    description,
    category,
    proposerId,
    proposerAddress: proposer.walletAddress,
    status: 'draft',
    actions: options?.actions?.map(a => ({
      ...a,
      id: uuidv4(),
      executed: false,
    })),
    votingConfig,
    createdAt: new Date(),
    votesFor: 0,
    votesAgainst: 0,
    votesAbstain: 0,
    totalVotePower: 0,
    voterCount: 0,
    votes: [],
    discussionUrl: options?.discussionUrl,
  };

  await dbSaveProposal(proposal);

  // Update proposer stats
  proposer.proposalsCreated++;
  proposer.lastActiveAt = new Date();
  await dbSaveParticipant(proposer);

  logger.info('Proposal created', {
    proposalId: proposal.id,
    proposalNumber: proposal.proposalNumber,
    title
  });
  return proposal;
}

/**
 * Submit a draft proposal to start voting
 */
export async function submitProposal(proposalId: string, proposerId: string): Promise<Proposal> {
  const proposal = await dbGetProposal(proposalId);

  if (!proposal) {
    throw new NotFoundError('Proposal');
  }

  if (proposal.proposerId !== proposerId) {
    throw new ForbiddenError('Only the proposer can submit the proposal');
  }

  if (proposal.status !== 'draft') {
    throw new ConflictError('Only draft proposals can be submitted');
  }

  const now = new Date();
  const votingEnds = new Date(now.getTime() + proposal.votingConfig.votingPeriodHours * 60 * 60 * 1000);

  // Snapshot total vote power at submission time
  const totalVotePower = await getTotalVotePower();

  proposal.status = 'active';
  proposal.submittedAt = now;
  proposal.votingStartsAt = now;
  proposal.votingEndsAt = votingEnds;
  proposal.totalVotePower = totalVotePower;
  proposal.votingConfig.snapshotTimestamp = now;

  await dbSaveProposal(proposal);

  logger.info('Proposal submitted', {
    proposalId: proposal.id,
    proposalNumber: proposal.proposalNumber,
    votingEndsAt: votingEnds.toISOString()
  });
  return proposal;
}

/**
 * Get proposal by ID
 */
export async function getProposal(proposalId: string): Promise<Proposal | undefined> {
  return dbGetProposal(proposalId);
}

/**
 * Get proposals with filters
 */
export async function getProposals(filters?: {
  status?: ProposalStatus | ProposalStatus[];
  category?: ProposalCategory;
  proposerId?: string;
}): Promise<Proposal[]> {
  const proposals = await dbGetAllProposals(filters);
  return proposals.sort((a, b) => b.proposalNumber - a.proposalNumber);
}

// =============================================================================
// VOTING
// =============================================================================

/**
 * Cast a vote on a proposal
 */
export async function castVote(
  proposalId: string,
  voterId: string,
  voteOption: VoteOption,
  reason?: string
): Promise<Vote> {
  const proposal = await dbGetProposal(proposalId);
  if (!proposal) {
    throw new NotFoundError('Proposal');
  }

  if (proposal.status !== 'active') {
    throw new ConflictError('Proposal is not open for voting');
  }

  // Check voting period
  if (proposal.votingEndsAt && new Date() > proposal.votingEndsAt) {
    throw new ConflictError('Voting period has ended');
  }

  const voter = await dbGetParticipant(voterId);
  if (!voter) {
    throw new ForbiddenError('Voter not registered as governance participant');
  }

  if (!voter.isDRep) {
    throw new ForbiddenError('Voter is not a DRep');
  }

  // Check for existing vote
  const existingVote = proposal.votes.find(v => v.voterId === voterId);
  if (existingVote) {
    throw new ConflictError('Already voted on this proposal');
  }

  // Check for delegation (use delegated power if applicable)
  const delegatedPower = await getDelegatedPowerFor(voterId, proposal.category);
  const totalVotePower = voter.votePower + delegatedPower;

  const vote: Vote = {
    id: uuidv4(),
    proposalId,
    voterId,
    voterAddress: voter.walletAddress,
    vote: voteOption,
    votePower: totalVotePower,
    tier: voter.tier,
    reason,
    votedAt: new Date(),
  };

  // Update proposal tallies
  proposal.votes.push(vote);
  proposal.voterCount++;

  switch (voteOption) {
    case 'for':
      proposal.votesFor += totalVotePower;
      break;
    case 'against':
      proposal.votesAgainst += totalVotePower;
      break;
    case 'abstain':
      proposal.votesAbstain += totalVotePower;
      break;
  }

  // Update voter stats
  voter.votesCast++;
  voter.lastActiveAt = new Date();

  await dbSaveProposal(proposal);
  await dbSaveParticipant(voter);

  logger.info('Vote cast', {
    proposalId: proposal.id,
    proposalNumber: proposal.proposalNumber,
    voteOption,
    votePower: totalVotePower
  });

  // Check if proposal should be finalized early
  await checkProposalFinalization(proposal);

  return vote;
}

/**
 * Check if proposal can be finalized early
 */
async function checkProposalFinalization(proposal: Proposal): Promise<void> {
  const totalVotes = proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain;
  const remaining = proposal.totalVotePower - totalVotes;

  // If remaining votes can't change outcome, finalize early
  if (proposal.votesFor > (proposal.totalVotePower - proposal.votesFor) &&
      proposal.votesFor > proposal.votesAgainst + remaining) {
    // Proposal has guaranteed passed
    await finalizeProposal(proposal.id);
  } else if (proposal.votesAgainst > proposal.totalVotePower - proposal.votesAgainst) {
    // Proposal has guaranteed failed
    await finalizeProposal(proposal.id);
  }
}

/**
 * Finalize a proposal after voting ends
 */
export async function finalizeProposal(proposalId: string): Promise<Proposal> {
  const proposal = await dbGetProposal(proposalId);
  if (!proposal) {
    throw new NotFoundError('Proposal');
  }

  if (proposal.status !== 'active') {
    throw new ConflictError('Proposal is not active');
  }

  const passed = hasProposalPassed(proposal);

  if (passed) {
    proposal.status = 'queued';
    proposal.queuedAt = new Date();
    proposal.executionEta = new Date(
      proposal.queuedAt.getTime() + proposal.votingConfig.timelockPeriodHours * 60 * 60 * 1000
    );
    logger.info('Proposal passed', {
      proposalId: proposal.id,
      proposalNumber: proposal.proposalNumber,
      executionEta: proposal.executionEta.toISOString()
    });
  } else {
    // Check if failed due to quorum or approval
    const totalVotes = proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain;
    const participationBps = Math.floor((totalVotes / proposal.totalVotePower) * 10000);

    if (participationBps < proposal.votingConfig.quorumThresholdBps) {
      proposal.status = 'expired';
      logger.info('Proposal expired', {
        proposalId: proposal.id,
        proposalNumber: proposal.proposalNumber,
        reason: 'quorum not met'
      });
    } else {
      proposal.status = 'failed';
      logger.info('Proposal failed', {
        proposalId: proposal.id,
        proposalNumber: proposal.proposalNumber,
        reason: 'approval threshold not met'
      });
    }
  }

  await dbSaveProposal(proposal);
  return proposal;
}

/**
 * Execute a queued proposal
 */
export async function executeProposal(proposalId: string, _executorId: string): Promise<Proposal> {
  const proposal = await dbGetProposal(proposalId);
  if (!proposal) {
    throw new NotFoundError('Proposal');
  }

  if (proposal.status !== 'queued') {
    throw new ConflictError('Proposal is not queued for execution');
  }

  // Check timelock
  if (proposal.executionEta && new Date() < proposal.executionEta) {
    throw new ConflictError(`Timelock not passed. Execution available at ${proposal.executionEta.toISOString()}`);
  }

  // Check constitutional approval if required
  if (proposal.votingConfig.requiresConstitutionalApproval) {
    // In production, this would check on-chain multi-sig
    logger.info('Constitutional approval required', {
      proposalId: proposal.id,
      proposalNumber: proposal.proposalNumber
    });
  }

  // Execute actions
  if (proposal.actions) {
    for (const action of proposal.actions) {
      logger.info('Executing action', {
        proposalId: proposal.id,
        actionType: action.actionType
      });
      action.executed = true;
      action.executedAt = new Date();
      // In production, this would call the actual contract/function
    }
  }

  proposal.status = 'executed';
  proposal.executedAt = new Date();

  await dbSaveProposal(proposal);
  logger.info('Proposal executed', {
    proposalId: proposal.id,
    proposalNumber: proposal.proposalNumber
  });
  return proposal;
}

/**
 * Cancel a proposal
 */
export async function cancelProposal(proposalId: string, cancellerId: string): Promise<Proposal> {
  const proposal = await dbGetProposal(proposalId);
  if (!proposal) {
    throw new NotFoundError('Proposal');
  }

  if (!['draft', 'active', 'queued'].includes(proposal.status)) {
    throw new ConflictError('Proposal cannot be cancelled');
  }

  const canceller = await dbGetParticipant(cancellerId);

  // Check permissions
  const isProposer = proposal.proposerId === cancellerId;
  const isConstitutionalMember = canceller?.isConstitutionalCommittee;

  if (!isProposer && !isConstitutionalMember) {
    throw new ForbiddenError('Only proposer or constitutional committee can cancel');
  }

  proposal.status = 'cancelled';
  proposal.cancelledAt = new Date();

  await dbSaveProposal(proposal);
  logger.info('Proposal cancelled', {
    proposalId: proposal.id,
    proposalNumber: proposal.proposalNumber,
    cancelledBy: isProposer ? 'proposer' : 'committee'
  });
  return proposal;
}

// =============================================================================
// DELEGATION
// =============================================================================

/**
 * Delegate vote power to another participant
 */
export async function delegateVote(
  delegatorId: string,
  delegateId: string,
  allProposals: boolean,
  categories?: ProposalCategory[],
  expiresAt?: Date
): Promise<VoteDelegation> {
  const delegator = await dbGetParticipant(delegatorId);
  const delegate = await dbGetParticipant(delegateId);

  if (!delegator || !delegate) {
    throw new NotFoundError('Delegator or delegate');
  }

  if (delegatorId === delegateId) {
    throw new BadRequestError('Cannot delegate to yourself');
  }

  // Revoke existing active delegation
  const existingDelegations = await dbGetActiveDelegations({ delegatorId });
  for (const existing of existingDelegations) {
    existing.revokedAt = new Date();
    await dbSaveDelegation(existing);
  }

  const delegation: VoteDelegation = {
    id: uuidv4(),
    delegatorId,
    delegatorAddress: delegator.walletAddress,
    delegateId,
    delegateAddress: delegate.walletAddress,
    delegatedPower: delegator.votePower,
    allProposals,
    categories: allProposals ? undefined : categories,
    createdAt: new Date(),
    expiresAt,
  };

  await dbSaveDelegation(delegation);
  logger.info('Vote delegated', {
    delegationId: delegation.id,
    delegatorAddress: delegator.walletAddress,
    delegateAddress: delegate.walletAddress
  });
  return delegation;
}

/**
 * Revoke a delegation
 */
export async function revokeDelegation(delegatorId: string): Promise<void> {
  const activeDelegations = await dbGetActiveDelegations({ delegatorId });

  for (const delegation of activeDelegations) {
    delegation.revokedAt = new Date();
    await dbSaveDelegation(delegation);
  }

  if (activeDelegations.length > 0) {
    logger.info('Delegation revoked', { delegatorId });
  }
}

/**
 * Get delegated power for a voter on a category
 */
async function getDelegatedPowerFor(delegateId: string, category: ProposalCategory): Promise<number> {
  const delegations = await dbGetActiveDelegations({ delegateId });

  return delegations
    .filter(d => d.allProposals || d.categories?.includes(category))
    .reduce((sum, d) => sum + d.delegatedPower, 0);
}

// =============================================================================
// GOVERNANCE CONFIG
// =============================================================================

/**
 * Get current governance configuration
 */
export function getGovernanceConfig(): GovernanceConfig {
  return { ...governanceConfig };
}

/**
 * Update governance configuration (requires governance approval in production)
 */
export function updateGovernanceConfig(updates: Partial<GovernanceConfig>): GovernanceConfig {
  governanceConfig = { ...governanceConfig, ...updates };
  logger.info('Configuration updated', { updates });
  return governanceConfig;
}

// =============================================================================
// STATISTICS
// =============================================================================

/**
 * Get governance statistics
 */
export async function getGovernanceStats(): Promise<{
  totalProposals: number;
  activeProposals: number;
  passedProposals: number;
  failedProposals: number;
  totalParticipants: number;
  totalDReps: number;
  totalVotePower: number;
  avgParticipation: number;
}> {
  const allProposals = await dbGetAllProposals();
  const allParticipants = await dbGetAllParticipants();
  const totalVotePower = await getTotalVotePower();

  const finishedProposals = allProposals.filter(p =>
    ['executed', 'failed', 'expired'].includes(p.status)
  );

  const avgParticipation = finishedProposals.length > 0
    ? finishedProposals.reduce((sum, p) => {
        const totalVotes = p.votesFor + p.votesAgainst + p.votesAbstain;
        return sum + (p.totalVotePower > 0 ? totalVotes / p.totalVotePower : 0);
      }, 0) / finishedProposals.length * 100
    : 0;

  return {
    totalProposals: allProposals.length,
    activeProposals: allProposals.filter(p => p.status === 'active').length,
    passedProposals: allProposals.filter(p => ['queued', 'executed'].includes(p.status)).length,
    failedProposals: allProposals.filter(p => ['failed', 'expired'].includes(p.status)).length,
    totalParticipants: allParticipants.length,
    totalDReps: allParticipants.filter(p => p.isDRep).length,
    totalVotePower,
    avgParticipation: Math.round(avgParticipation * 100) / 100,
  };
}

// =============================================================================
// SCHEDULED TASKS
// =============================================================================

/**
 * Process expired proposals (call periodically)
 */
export async function processExpiredProposals(): Promise<number> {
  try {
    const activeProposals = await dbGetAllProposals({ status: 'active' });
    const now = new Date();
    let processed = 0;

    for (const proposal of activeProposals) {
      if (proposal.votingEndsAt && now > proposal.votingEndsAt) {
        await finalizeProposal(proposal.id);
        processed++;
      }
    }

    return processed;
  } catch (err: any) {
    logger.error('processExpiredProposals failed', { error: err instanceof Error ? err.message : String(err) });
    return 0;
  }
}
