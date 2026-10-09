/**
 * =============================================================================
 * GOVERNANCE API ROUTES
 * =============================================================================
 * REST API endpoints for DAO governance operations
 */

import { Router, Request, Response, NextFunction } from 'express';
import * as governanceService from '../services/governanceService';
import {
  CreateProposalSchema,
  CastVoteSchema,
  DelegateVoteSchema,
  RegisterParticipantSchema,
  ProposalStatus,
  ProposalCategory,
} from '../types/governance.types';

const router = Router();

// =============================================================================
// PARTICIPANT ROUTES
// =============================================================================

/**
 * POST /api/governance/participants/register
 * Register or update a governance participant
 */
router.post('/participants/register', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-444: validate against the published request schema instead of the old
    // truthy check, which accepted a spec-violating `walletAddress: {}` (any
    // truthy value) and silently ignored type errors on did/isDRep/
    // isConstitutionalCommittee.
    const { walletAddress, stakedAmount, did, isDRep, isConstitutionalCommittee } =
      RegisterParticipantSchema.parse(req.body);

    const participant = await governanceService.registerParticipant(
      walletAddress,
      stakedAmount,
      { did, isDRep, isConstitutionalCommittee }
    );

    res.status(201).json({
      success: true,
      data: participant,
    });
  } catch (error: any) {
    if (error.name === 'ZodError') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * GET /api/governance/participants
 * Get all governance participants
 */
router.get('/participants', async (req: Request, res: Response) => {
  const { isDRep, isConstitutionalCommittee, minTier } = req.query;

  const participants = await governanceService.getParticipants({
    isDRep: isDRep === 'true' ? true : isDRep === 'false' ? false : undefined,
    isConstitutionalCommittee: isConstitutionalCommittee === 'true',
    minTier: minTier as any,
  });

  res.json({
    success: true,
    data: participants,
    count: participants.length,
  });
});

/**
 * GET /api/governance/participants/:id
 * Get participant by ID or wallet address
 */
router.get('/participants/:id', async (req: Request, res: Response) => {
  const participant = await governanceService.getParticipant(req.params.id);
  
  if (!participant) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Participant not found' } });
  }
  
  res.json({
    success: true,
    data: participant,
  });
});

// =============================================================================
// PROPOSAL ROUTES
// =============================================================================

/**
 * POST /api/governance/proposals
 * Create a new proposal
 */
router.post('/proposals', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const userId = (req as any).user?.userId as string;
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    
    const validatedData = CreateProposalSchema.parse(req.body);
    
    const proposal = await governanceService.createProposal(
      userId,
      validatedData.title,
      validatedData.description,
      validatedData.category,
      {
        actions: validatedData.actions,
        discussionUrl: validatedData.discussionUrl,
        customVotingConfig: validatedData.votingConfig,
      }
    );
    
    res.status(201).json({
      success: true,
      data: proposal,
      message: `Proposal #${proposal.proposalNumber} created as draft`,
    });
  } catch (error: any) {
    if (error.name === 'ZodError') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * GET /api/governance/proposals
 * Get proposals with optional filters
 */
router.get('/proposals', async (req: Request, res: Response) => {
  const { status, category, proposerId } = req.query;
  
  let statusFilter: ProposalStatus | ProposalStatus[] | undefined;
  if (status) {
    statusFilter = (status as string).split(',') as ProposalStatus[];
    if (statusFilter.length === 1) statusFilter = statusFilter[0];
  }
  
  const proposals = await governanceService.getProposals({
    status: statusFilter,
    category: category as ProposalCategory,
    proposerId: proposerId as string,
  });
  
  res.json({
    success: true,
    data: proposals,
    count: proposals.length,
  });
});

/**
 * GET /api/governance/proposals/active
 * Get active proposals only
 */
router.get('/proposals/active', async (_req: Request, res: Response) => {
  const proposals = await governanceService.getProposals({ status: 'active' });
  
  res.json({
    success: true,
    data: proposals,
    count: proposals.length,
  });
});

/**
 * GET /api/governance/proposals/:id
 * Get proposal by ID
 */
router.get('/proposals/:id', async (req: Request, res: Response) => {
  const proposal = await governanceService.getProposal(req.params.id);
  
  if (!proposal) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Proposal not found' } });
  }
  
  res.json({
    success: true,
    data: proposal,
  });
});

/**
 * POST /api/governance/proposals/:id/submit
 * Submit a draft proposal to start voting
 */
router.post('/proposals/:id/submit', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const userId = (req as any).user?.userId as string;
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    
    const proposal = await governanceService.submitProposal(req.params.id, userId);
    
    res.json({
      success: true,
      data: proposal,
      message: `Proposal #${proposal.proposalNumber} submitted - voting is now open`,
    });
  } catch (error: any) {
    // KS-594: this used to answer 400 BAD_REQUEST for ANY error carrying a
    // message, which flattened three different truths into one status — a
    // missing proposal (404), a caller who is not the proposer (403), a state
    // conflict (409) — and, worse, reported a genuine internal failure as the
    // CLIENT's bad request. The service now throws typed AppErrors, so hand
    // everything to the shared error handler and let each carry its own status.
    next(error);
  }
});

/**
 * POST /api/governance/proposals/:id/cancel
 * Cancel a proposal
 */
router.post('/proposals/:id/cancel', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const userId = (req as any).user?.userId as string;
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    
    const proposal = await governanceService.cancelProposal(req.params.id, userId);
    
    res.json({
      success: true,
      data: proposal,
      message: `Proposal #${proposal.proposalNumber} cancelled`,
    });
  } catch (error: any) {
    // KS-594: this used to answer 400 BAD_REQUEST for ANY error carrying a
    // message, which flattened three different truths into one status — a
    // missing proposal (404), a caller who is not the proposer (403), a state
    // conflict (409) — and, worse, reported a genuine internal failure as the
    // CLIENT's bad request. The service now throws typed AppErrors, so hand
    // everything to the shared error handler and let each carry its own status.
    next(error);
  }
});

/**
 * POST /api/governance/proposals/:id/execute
 * Execute a queued proposal
 */
router.post('/proposals/:id/execute', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const userId = (req as any).user?.userId as string;
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    
    const proposal = await governanceService.executeProposal(req.params.id, userId);
    
    res.json({
      success: true,
      data: proposal,
      message: `Proposal #${proposal.proposalNumber} executed`,
    });
  } catch (error: any) {
    // KS-594: this used to answer 400 BAD_REQUEST for ANY error carrying a
    // message, which flattened three different truths into one status — a
    // missing proposal (404), a caller who is not the proposer (403), a state
    // conflict (409) — and, worse, reported a genuine internal failure as the
    // CLIENT's bad request. The service now throws typed AppErrors, so hand
    // everything to the shared error handler and let each carry its own status.
    next(error);
  }
});

// =============================================================================
// VOTING ROUTES
// =============================================================================

/**
 * POST /api/governance/proposals/:id/vote
 * Cast a vote on a proposal
 */
router.post('/proposals/:id/vote', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const userId = (req as any).user?.userId as string;
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    
    const { vote, reason } = CastVoteSchema.omit({ proposalId: true }).parse(req.body);
    
    const voteRecord = await governanceService.castVote(req.params.id, userId, vote, reason);
    
    res.json({
      success: true,
      data: voteRecord,
      message: `Vote recorded: ${vote}`,
    });
  } catch (error: any) {
    if (error.name === 'ZodError') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    // KS-594: this used to answer 400 BAD_REQUEST for ANY error carrying a
    // message, which flattened three different truths into one status — a
    // missing proposal (404), a caller who is not the proposer (403), a state
    // conflict (409) — and, worse, reported a genuine internal failure as the
    // CLIENT's bad request. The service now throws typed AppErrors, so hand
    // everything to the shared error handler and let each carry its own status.
    next(error);
  }
});

/**
 * GET /api/governance/proposals/:id/votes
 * Get all votes for a proposal
 */
router.get('/proposals/:id/votes', async (req: Request, res: Response) => {
  const proposal = await governanceService.getProposal(req.params.id);
  
  if (!proposal) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Proposal not found' } });
  }
  
  const summary = {
    totalVotes: proposal.voterCount,
    votesFor: proposal.votesFor,
    votesAgainst: proposal.votesAgainst,
    votesAbstain: proposal.votesAbstain,
    totalVotePower: proposal.totalVotePower,
    participationPercent: Math.round(
      ((proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain) / proposal.totalVotePower) * 10000
    ) / 100,
    approvalPercent: proposal.votesFor + proposal.votesAgainst > 0
      ? Math.round((proposal.votesFor / (proposal.votesFor + proposal.votesAgainst)) * 10000) / 100
      : 0,
  };
  
  res.json({
    success: true,
    data: {
      summary,
      votes: proposal.votes,
    },
  });
});

// =============================================================================
// DELEGATION ROUTES
// =============================================================================

/**
 * POST /api/governance/delegate
 * Delegate vote power to another participant
 */
router.post('/delegate', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const userId = (req as any).user?.userId as string;
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }
    
    const { delegateId, allProposals, categories, expiresAt } =
      DelegateVoteSchema.parse(req.body);
    
    const delegation = await governanceService.delegateVote(
      userId,
      delegateId,
      allProposals,
      categories,
      expiresAt ? new Date(expiresAt) : undefined
    );
    
    res.json({
      success: true,
      data: delegation,
      message: 'Vote power delegated',
    });
  } catch (error: any) {
    if (error.name === 'ZodError') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    // KS-594: this used to answer 400 BAD_REQUEST for ANY error carrying a
    // message, which flattened three different truths into one status — a
    // missing proposal (404), a caller who is not the proposer (403), a state
    // conflict (409) — and, worse, reported a genuine internal failure as the
    // CLIENT's bad request. The service now throws typed AppErrors, so hand
    // everything to the shared error handler and let each carry its own status.
    next(error);
  }
});

/**
 * DELETE /api/governance/delegate
 * Revoke delegation
 */
router.delete('/delegate', async (req: Request, res: Response) => {
  // Pen-test F-04: read from authenticated req.user (set by authenticate()
  // middleware), NOT from raw headers. Direct header reads are spoofable.
  const userId = (req as any).user?.userId as string;
  if (!userId) {
    return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
  }
  
  await governanceService.revokeDelegation(userId);
  
  res.json({
    success: true,
    message: 'Delegation revoked',
  });
});

// =============================================================================
// CONFIG & STATS ROUTES
// =============================================================================

/**
 * GET /api/governance/state
 * Get current governance state (for E2E testing compatibility)
 */
router.get('/state', async (_req: Request, res: Response) => {
  const stats = await governanceService.getGovernanceStats();
  const config = governanceService.getGovernanceConfig();
  
  res.json({
    success: true,
    data: {
      currentEpoch: 1,
      totalStaked: stats.totalVotePower || 0,
      activeProposals: stats.activeProposals || 0,
      totalProposals: stats.totalProposals || 0,
      totalParticipants: stats.totalParticipants || 0,
      parameters: config,
    },
  });
});

/**
 * GET /api/governance/config
 * Get governance configuration
 */
router.get('/config', (_req: Request, res: Response) => {
  const config = governanceService.getGovernanceConfig();
  
  res.json({
    success: true,
    data: config,
  });
});

/**
 * GET /api/governance/stats
 * Get governance statistics
 */
router.get('/stats', async (_req: Request, res: Response) => {
  const stats = await governanceService.getGovernanceStats();
  
  res.json({
    success: true,
    data: stats,
  });
});

/**
 * POST /api/governance/process-expired
 * Process expired proposals (admin/cron endpoint)
 */
router.post('/process-expired', async (_req: Request, res: Response) => {
  const processed = await governanceService.processExpiredProposals();
  
  res.json({
    success: true,
    data: { processed },
    message: `Processed ${processed} expired proposals`,
  });
});

export { router as governanceRoutes };
