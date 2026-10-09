/**
 * =============================================================================
 * GOVERNANCE SERVICE — OpenAPI registrations
 * =============================================================================
 *
 * Decentralised DAO governance: participants, proposals, voting, delegation,
 * tier-weighted vote multipliers. Mounted at /api/governance/*.
 *
 * Endpoints registered (18 paths):
 *   Participants:
 *     - POST /api/governance/participants/register
 *     - GET  /api/governance/participants
 *     - GET  /api/governance/participants/{id}
 *   Proposals:
 *     - POST /api/governance/proposals
 *     - GET  /api/governance/proposals
 *     - GET  /api/governance/proposals/active
 *     - GET  /api/governance/proposals/{id}
 *     - POST /api/governance/proposals/{id}/submit
 *     - POST /api/governance/proposals/{id}/cancel
 *     - POST /api/governance/proposals/{id}/execute
 *     - POST /api/governance/proposals/{id}/vote
 *     - GET  /api/governance/proposals/{id}/votes
 *   Delegation:
 *     - POST   /api/governance/delegate
 *     - DELETE /api/governance/delegate
 *   State + admin:
 *     - GET  /api/governance/state
 *     - GET  /api/governance/config
 *     - GET  /api/governance/stats
 *     - POST /api/governance/process-expired
 * =============================================================================
 */

import { z, sharedRegistry, commonErrorResponses, successEnvelope, FX } from '@secuura/shared';

// -----------------------------------------------------------------------------
// SCHEMAS
// -----------------------------------------------------------------------------

// KS-440: the runtime participant tier vocabulary is the StakeTier union
// (basic/staker/validator/partner) defined in services/governance
// src/types/governance.types.ts (VOTE_MULTIPLIERS / TIER_THRESHOLDS / calculateTier),
// NOT bronze/silver/gold/platinum. GET /participants and /participants/{id} return
// e.g. `tier: "staker"`, which the old enum rejected — publish the real values.
const ParticipantTierEnum = z.enum(['basic', 'staker', 'validator', 'partner']);

// KS-498: reconciled with the runtime ProposalStatus vocabulary
// (types/governance.types.ts) — the service moves passed proposals through
// 'queued' (timelock) and marks threshold misses 'failed'; the previously
// published 'submitted'/'rejected' exist in no code path.
const ProposalStatusEnum = z.enum([
  'draft',
  'active',
  'passed',
  'failed',
  'queued',
  'executed',
  'cancelled',
  'expired',
]);

const ProposalCategoryEnum = z.enum([
  'parameter_change',
  'fee_adjustment',
  'treasury_spend',
  'upgrade',
  'emergency',
  'governance_change',
  'whitelist',
  'general',
]);

// KS-444: was ['yes', 'no', 'abstain'] — no implementation ever accepted those
// values. The governance microservice's CastVoteSchema and the issuer frontend
// (GovernanceDashboard) both use for/against/abstain, so clients generated from
// the old spec enum could never cast a vote. Republished to match the runtime.
// (The gateway governance mock that also used this enum was removed in KS-450.)
const VoteEnum = z.enum(['for', 'against', 'abstain']);

// KS-440: reconciled with the runtime participant object (rowToParticipant in
// services/governance/src/services/governanceService.ts). The handler returns
// walletAddress/stakedAmount/votePower/isDRep/isConstitutionalCommittee/
// proposalsCreated/votesCast/lastActiveAt/joinedAt — NOT the old spec's
// voteMultiplier/registeredAt/userId/address, which were required but never
// returned. KS-455: the runtime's lowercase `votescast` wart was normalised to
// `votesCast` (rowToParticipant) together with this spec — no consumer read
// the old casing. `did` is present only for participants that registered one,
// so it is optional.
const ParticipantSchema = sharedRegistry.register(
  'GovernanceParticipant',
  z
    .object({
      id: z.string(),
      walletAddress: z.string(),
      did: z.string().nullable().optional(),
      stakedAmount: z.number(),
      tier: ParticipantTierEnum,
      votePower: z.number(),
      isDRep: z.boolean(),
      isConstitutionalCommittee: z.boolean(),
      proposalsCreated: z.number().int().nonnegative(),
      votesCast: z.number().int().nonnegative(),
      lastActiveAt: z.string(),
      joinedAt: z.string(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    walletAddress: 'addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgse35a3x',
    stakedAmount: 1,
    tier: 'basic',
    votePower: 1,
    isDRep: true,
    isConstitutionalCommittee: true,
    proposalsCreated: 0,
    votesCast: 0,
    lastActiveAt: 'example-lastActiveAt',
    joinedAt: 'example-joinedAt',
  },
  }),
);

// KS-430: reconciled with the runtime validator in routes/governance.ts
// (POST /participants/register), which reads walletAddress + stakedAmount from
// the body and requires both (`if (!walletAddress || typeof stakedAmount !==
// 'number')` → 400). The old spec fields userId/address/tier are silently
// ignored by the handler and their absence let a spec-minimal `{}` earn a 400;
// the real request contract is the wallet address, staked amount, and the
// optional DID / DRep / constitutional-committee flags.
// KS-444: walletAddress carries minLength 1 — the runtime has always rejected
// an empty walletAddress (the old truthy check, now RegisterParticipantSchema
// in the service), so publish the same bound instead of letting a spec-legal
// '' earn a 400.
const ParticipantRegisterRequestSchema = sharedRegistry.register(
  'ParticipantRegisterRequest',
  z.object({
    walletAddress: z.string().min(1),
    // KS-498: bounded to match the runtime (RegisterParticipantSchema) — an
    // unbounded double overflows the votePower multiply to Infinity → null
    // in the response, violating GovernanceParticipant.
    stakedAmount: z.number().nonnegative().max(1e12),
    did: z.string().optional(),
    isDRep: z.boolean().optional(),
    isConstitutionalCommittee: z.boolean().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    walletAddress: 'addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgse35a3x',
    stakedAmount: 1,
  },
  }),
);

// KS-498: reconciled with the runtime Proposal object (types/governance.types.ts,
// serialized by governanceService's row mapper). The old published shape
// (yesVotes/noVotes/abstainVotes/quorumRequired/expiresAt) matched no handler —
// the runtime returns proposalNumber/category/proposerAddress/votingConfig and
// the votesFor/votesAgainst/votesAbstain/totalVotePower/voterCount tallies.
// On-chain refs (txHash/datumHash/ipfsHash) come back as explicit nulls.
const ProposalSchema = sharedRegistry.register(
  'Proposal',
  z
    .object({
      id: z.string(),
      proposalNumber: z.number().int(),
      title: z.string(),
      description: z.string(),
      category: ProposalCategoryEnum,
      proposerId: z.string(),
      proposerAddress: z.string(),
      status: ProposalStatusEnum,
      actions: z.array(z.object({}).passthrough()).optional(),
      votingConfig: z
        .object({
          approvalThresholdBps: z.number().optional(),
          quorumThresholdBps: z.number().optional(),
          votingPeriodHours: z.number().optional(),
          timelockPeriodHours: z.number().optional(),
          requiresConstitutionalApproval: z.boolean().optional(),
        })
        .passthrough(),
      createdAt: z.string(),
      submittedAt: z.string().nullable().optional(),
      votingStartsAt: z.string().nullable().optional(),
      votingEndsAt: z.string().nullable().optional(),
      queuedAt: z.string().nullable().optional(),
      executionEta: z.string().nullable().optional(),
      executedAt: z.string().nullable().optional(),
      cancelledAt: z.string().nullable().optional(),
      votesFor: z.number(),
      votesAgainst: z.number(),
      votesAbstain: z.number(),
      totalVotePower: z.number(),
      voterCount: z.number().int(),
      votes: z.array(z.object({}).passthrough()).optional(),
      txHash: z.string().nullable().optional(),
      datumHash: z.string().nullable().optional(),
      discussionUrl: z.string().nullable().optional(),
      ipfsHash: z.string().nullable().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    proposalNumber: 1,
    title: 'example-title',
    description: 'example-description',
    category: 'parameter_change',
    proposerId: 'example-proposerId',
    proposerAddress: 'example-proposerAddress',
    status: 'draft',
    votingConfig: {
      approvalThresholdBps: 1,
      quorumThresholdBps: 1,
      votingPeriodHours: 1,
      timelockPeriodHours: 1,
      requiresConstitutionalApproval: true,
    },
    createdAt: 'example-createdAt',
    votesFor: 1,
    votesAgainst: 1,
    votesAbstain: 1,
    totalVotePower: 1,
    voterCount: 1,
  },
  }),
);

// KS-450: the gateway mock that used to answer this op (title/description
// min 1 + free-form metadata) is removed — the governance service now serves
// it live. Publish the service's real CreateProposalSchema
// (types/governance.types.ts): title 10–200, description 50–10000, category a
// required enum, plus the optional actions / discussionUrl / votingConfig the
// handler forwards. `metadata` is gone — the runtime never read it.
const ProposalCreateRequestSchema = sharedRegistry.register(
  'ProposalCreateRequest',
  z.object({
    title: z.string().min(10).max(200),
    description: z.string().min(50).max(10000),
    category: z.enum([
      'parameter_change',
      'fee_adjustment',
      'treasury_spend',
      'upgrade',
      'emergency',
      'governance_change',
      'whitelist',
      'general',
    ]),
    actions: z
      .array(
        z.object({
          actionType: z.enum(['contract_call', 'parameter_update', 'treasury_transfer', 'upgrade']),
          targetContract: z.string().optional(),
          targetFunction: z.string().optional(),
          parameters: z.record(z.string(), z.unknown()),
          recipient: z.string().optional(),
          amount: z.number().optional(),
        }),
      )
      .optional(),
    discussionUrl: z.string().url().optional(),
    votingConfig: z
      .object({
        approvalThresholdBps: z.number().min(1).max(10000).optional(),
        quorumThresholdBps: z.number().min(1).max(10000).optional(),
        votingPeriodHours: z.number().min(1).max(720).optional(),
        timelockPeriodHours: z.number().min(0).max(168).optional(),
      })
      .optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    title: 'example-title',
    description: 'example-descriptionxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    category: 'parameter_change',
  },
  }),
);

// KS-450: POST /proposals now answers from the real service — the enveloped
// `{ success, data: <Proposal>, message }` (201, status starts at 'draft'),
// not the mock's flat proposal object.
const ProposalCreateResponseSchema = sharedRegistry.register(
  'ProposalCreateResponse',
  z.object({
    success: z.literal(true),
    data: ProposalSchema,
    message: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      id: '00000000-0000-4000-8000-0000000000ff',
      proposalNumber: 1,
      title: 'example-title',
      description: 'example-description',
      category: 'parameter_change',
      proposerId: '00000000-0000-4000-8000-0000000000ff',
      proposerAddress: '00000000-0000-4000-8000-0000000000ff',
      status: 'draft',
      votingConfig: {
        approvalThresholdBps: 1,
        quorumThresholdBps: 1,
        votingPeriodHours: 1,
        timelockPeriodHours: 1,
        requiresConstitutionalApproval: true,
      },
      createdAt: FX.timestamps.createdAt,
      votesFor: 1,
      votesAgainst: 1,
      votesAbstain: 1,
      totalVotePower: 1,
      voterCount: 1,
    },
    message: 'example-message',
  },
  }),
);

// KS-144: real response is the canonical envelope `{ success, data: [...], count }`
// (not a top-level `proposals` array). successEnvelope is .passthrough() so the
// extra `count` key is tolerated.
const ProposalListResponseSchema = sharedRegistry.register(
  'ProposalListResponse',
  successEnvelope(z.array(ProposalSchema)).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: [
      {
        id: '00000000-0000-4000-8000-0000000000ff',
        proposalNumber: 1,
        title: 'example-title',
        description: 'example-description',
        category: 'parameter_change',
        proposerId: '00000000-0000-4000-8000-0000000000ff',
        proposerAddress: '00000000-0000-4000-8000-0000000000ff',
        status: 'draft',
        votingConfig: {
          approvalThresholdBps: 1,
          quorumThresholdBps: 1,
          votingPeriodHours: 1,
          timelockPeriodHours: 1,
          requiresConstitutionalApproval: true,
        },
        createdAt: FX.timestamps.createdAt,
        votesFor: 1,
        votesAgainst: 1,
        votesAbstain: 1,
        totalVotePower: 1,
        voterCount: 1,
      },
      {
        id: '00000000-0000-4000-8000-0000000000ff',
        proposalNumber: 1,
        title: 'example-title',
        description: 'example-description',
        category: 'parameter_change',
        proposerId: '00000000-0000-4000-8000-0000000000ff',
        proposerAddress: '00000000-0000-4000-8000-0000000000ff',
        status: 'draft',
        votingConfig: {
          approvalThresholdBps: 1,
          quorumThresholdBps: 1,
          votingPeriodHours: 1,
          timelockPeriodHours: 1,
          requiresConstitutionalApproval: true,
        },
        createdAt: FX.timestamps.createdAt,
        votesFor: 1,
        votesAgainst: 1,
        votesAbstain: 1,
        totalVotePower: 1,
        voterCount: 1,
      },
    ],
  },
  }),
);

const VoteRequestSchema = sharedRegistry.register(
  'VoteRequest',
  z.object({
    vote: VoteEnum,
    // KS-444: the governance microservice's CastVoteSchema caps reason at 1000
    // chars — publish the cap so a spec-legal longer reason isn't generated and
    // rejected. (Enforced solely by the service since KS-450 removed the mock.)
    reason: z.string().max(1000).optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    vote: 'for',
  },
  }),
);

// KS-498: reconciled with the runtime Vote record (types/governance.types.ts) —
// voterId/voterAddress/votePower/tier/votedAt, not the never-returned
// participantId/weight/castAt guess (the drift the KS-450 comment above
// deferred to the response-sweep family).
const VoteSchema = sharedRegistry.register(
  'Vote',
  z
    .object({
      id: z.string(),
      proposalId: z.string(),
      voterId: z.string(),
      voterAddress: z.string(),
      vote: VoteEnum,
      votePower: z.number(),
      tier: ParticipantTierEnum,
      reason: z.string().nullable().optional(),
      signature: z.string().nullable().optional(),
      votedAt: z.string(),
      txHash: z.string().nullable().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    proposalId: 'example-proposalId',
    voterId: 'example-voterId',
    voterAddress: 'example-voterAddress',
    vote: 'for',
    votePower: 1,
    tier: 'basic',
    votedAt: 'example-votedAt',
  },
  }),
);

// KS-450: the gateway mock that used to shadow POST /proposals/{id}/vote is
// removed — the real governance service answers it now, with the enveloped
// `{ success, data: <vote record>, message }`. The record is the service's
// Vote shape (types/governance.types.ts): voterId/votePower/votedAt — NOT the
// mock's flat { voted, ..., voteWeight, createdAt } nor the older published
// participantId/weight/castAt guess (that drift on the votes-list schemas is
// tracked separately under the KS-440/KS-455 response-sweep family).
const VoteCastResponseSchema = sharedRegistry.register(
  'GovernanceVoteResponse',
  z.object({
    success: z.literal(true),
    data: z
      .object({
        id: z.string(),
        proposalId: z.string(),
        voterId: z.string(),
        voterAddress: z.string().optional(),
        vote: VoteEnum,
        votePower: z.number().nonnegative(),
        tier: z.string().optional(),
        reason: z.string().optional(),
        votedAt: z.string(),
      })
      .passthrough(),
    message: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      id: 'example-id',
      proposalId: 'example-proposalId',
      voterId: 'example-voterId',
      vote: 'for',
      votePower: 0,
      votedAt: 'example-votedAt',
    },
    message: 'example-message',
  },
  }),
);

// KS-498: the handler (GET /proposals/:id/votes) returns the enveloped
// `{ success, data: { summary, votes } }`, not a flat votes array.
// participationPercent is NaN→null when totalVotePower is 0 (0/0), so it is
// published nullable.
const VoteListResponseSchema = sharedRegistry.register(
  'VoteListResponse',
  z.object({
    success: z.literal(true),
    data: z.object({
      summary: z
        .object({
          totalVotes: z.number().int().nonnegative(),
          votesFor: z.number().nonnegative(),
          votesAgainst: z.number().nonnegative(),
          votesAbstain: z.number().nonnegative(),
          totalVotePower: z.number().nonnegative(),
          participationPercent: z.number().nullable(),
          approvalPercent: z.number(),
        })
        .passthrough(),
      votes: z.array(VoteSchema),
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      summary: {
        totalVotes: 0,
        votesFor: 0,
        votesAgainst: 0,
        votesAbstain: 0,
        totalVotePower: 0,
        participationPercent: null,
        approvalPercent: 1,
      },
      votes: [
        {
          id: 'example-id',
          proposalId: 'example-proposalId',
          voterId: 'example-voterId',
          voterAddress: 'example-voterAddress',
          vote: 'for',
          votePower: 1,
          tier: 'basic',
          votedAt: 'example-votedAt',
        },
        {
          id: 'example-id',
          proposalId: 'example-proposalId',
          voterId: 'example-voterId',
          voterAddress: 'example-voterAddress',
          vote: 'for',
          votePower: 1,
          tier: 'basic',
          votedAt: 'example-votedAt',
        },
      ],
    },
  },
  }),
);

// KS-430: reconciled with the runtime DelegateVoteSchema. The handler destructures
// { delegateId, allProposals, categories, expiresAt } and passes allProposals to
// delegateVote(), so allProposals is a genuinely-required part of the delegation
// payload — it was omitted here, letting a spec-minimal `{ delegateId }` earn a 400
// (Required allProposals). categories + expiresAt are the optional scope/expiry the
// handler forwards. (delegateAddress, which the handler ignores, was loosened to
// optional runtime-side rather than published here.)
const DelegateRequestSchema = sharedRegistry.register(
  'DelegateRequest',
  z.object({
    delegateId: z.string(),
    allProposals: z.boolean(),
    categories: z
      .array(
        z.enum([
          'parameter_change',
          'fee_adjustment',
          'treasury_spend',
          'upgrade',
          'emergency',
          'governance_change',
          'whitelist',
          'general',
        ]),
      )
      .optional(),
    expiresAt: z.string().datetime().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    delegateId: FX.issuer.id,
    allProposals: true,
  },
  }),
);

// KS-450: GET /state was answered by the gateway mock (flat shape with a
// `config` key, totalStaked a string) until the mock's removal — the real
// governance service wraps the state in the `{ success, data }` envelope,
// returns numeric totalStaked, and names the config key `parameters`
// (routes/governance.ts GET /state).
const GovernanceStateSchema = sharedRegistry.register(
  'GovernanceState',
  z
    .object({
      success: z.literal(true),
      data: z
        .object({
          currentEpoch: z.number(),
          totalStaked: z.number(),
          activeProposals: z.number(),
          totalProposals: z.number(),
          totalParticipants: z.number(),
          parameters: z.object({}).passthrough(),
        })
        .passthrough(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      currentEpoch: 1,
      totalStaked: 1,
      activeProposals: 1,
      totalProposals: 1,
      totalParticipants: 1,
      parameters: {},
    },
  },
  }),
);

// KS-440: reconciled with the runtime GovernanceConfig (DEFAULT_GOVERNANCE_CONFIG
// in services/governance/src/types/governance.types.ts, returned by
// getGovernanceConfig). The runtime returns the voting-parameter config —
// approval/quorum/timelock defaults, proposal requirements, emergency +
// constitutional settings, and per-category overrides — NOT the old spec's
// voteMultipliers/tierThresholds (those live in the StakeTier constants, not in
// the config response). The route wraps this in the `{ success, data }`
// envelope (see successEnvelope at the config path below).
const GovernanceConfigSchema = sharedRegistry.register(
  'GovernanceConfig',
  z
    .object({
      defaultApprovalThresholdBps: z.number(),
      defaultQuorumThresholdBps: z.number(),
      defaultVotingPeriodHours: z.number(),
      defaultTimelockPeriodHours: z.number(),
      minProposalStake: z.number(),
      proposalDeposit: z.number(),
      maxActiveProposals: z.number(),
      emergencyMultisigThreshold: z.number(),
      emergencyTimelockHours: z.number(),
      constitutionalCommitteeSize: z.number(),
      constitutionalVetoThreshold: z.number(),
      categoryOverrides: z.record(z.string(), z.record(z.string(), z.unknown())),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    defaultApprovalThresholdBps: 1,
    defaultQuorumThresholdBps: 1,
    defaultVotingPeriodHours: 1,
    defaultTimelockPeriodHours: 1,
    minProposalStake: 1,
    proposalDeposit: 1,
    maxActiveProposals: 1,
    emergencyMultisigThreshold: 1,
    emergencyTimelockHours: 1,
    constitutionalCommitteeSize: 1,
    constitutionalVetoThreshold: 1,
    categoryOverrides: {},
  },
  }),
);

// KS-440: reconciled with the runtime getGovernanceStats
// (services/governance/src/services/governanceService.ts). The runtime returns
// flat aggregate counts — total/active/passed/failed proposals, participants,
// DReps, vote power, and average participation — NOT the old spec's
// proposalsByStatus/participantsByTier/totalVotesCast (which the handler never
// produces). The route wraps this in the `{ success, data }` envelope (see
// successEnvelope at the stats path below).
const GovernanceStatsSchema = sharedRegistry.register(
  'GovernanceStats',
  z
    .object({
      totalProposals: z.number().int().nonnegative(),
      activeProposals: z.number().int().nonnegative(),
      passedProposals: z.number().int().nonnegative(),
      failedProposals: z.number().int().nonnegative(),
      totalParticipants: z.number().int().nonnegative(),
      totalDReps: z.number().int().nonnegative(),
      totalVotePower: z.number(),
      avgParticipation: z.number(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    totalProposals: 0,
    activeProposals: 0,
    passedProposals: 0,
    failedProposals: 0,
    totalParticipants: 0,
    totalDReps: 0,
    totalVotePower: 1,
    avgParticipation: 1,
  },
  }),
);

const GovernanceSuccessSchema = sharedRegistry.register(
  'GovernanceSuccess',
  z
    .object({
      success: z.boolean(),
      message: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
  },
  }),
);

// -----------------------------------------------------------------------------
// ROUTES — participants
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/participants/register',
  tags: ['Governance', 'Participants'],
  summary: 'Register as a governance participant',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: required — the runtime 400s a bodyless request (walletAddress +
    // stakedAmount are mandatory), so don't publish the body as optional.
    body: { content: { 'application/json': { schema: ParticipantRegisterRequestSchema } }, required: true },
  },
  responses: {
    201: {
      description: 'Registered',
      // KS-498: the handler returns the canonical `{ success, data }` envelope,
      // not a flat participant object.
      content: { 'application/json': { schema: successEnvelope(ParticipantSchema) } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/participants',
  tags: ['Governance', 'Participants'],
  summary: 'List participants',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Participants',
      content: {
        'application/json': {
          // KS-118: match the handler's {success, data, count} envelope.
          schema: z.object({
            success: z.literal(true),
            data: z.array(ParticipantSchema),
            count: z.number().int().nonnegative(),
          }),
        },
      },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/participants/{id}',
  tags: ['Governance', 'Participants'],
  summary: 'Get a participant by id',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Participant',
      // KS-440: the handler wraps the participant in the `{ success, data }`
      // envelope (routes/governance.ts GET /participants/:id) — the old spec
      // applied ParticipantSchema to the bare response, so envelope keys were
      // read as the participant object (missing id/tier/... → 200 violation).
      content: { 'application/json': { schema: successEnvelope(ParticipantSchema) } },
    },
    401: commonErrorResponses[401],
    404: commonErrorResponses[404],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — proposals
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/proposals',
  tags: ['Governance', 'Proposals'],
  summary: 'Create a draft proposal',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: required — the runtime 400s a bodyless request (title +
    // description are mandatory), so don't publish the body as optional.
    body: { content: { 'application/json': { schema: ProposalCreateRequestSchema } }, required: true },
  },
  responses: {
    201: {
      description: 'Draft proposal created',
      // KS-450: the real service (no longer the gateway mock) answers with the
      // `{ success, data, message }` envelope.
      content: { 'application/json': { schema: ProposalCreateResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    // KS-594: the runtime now refuses this with a typed ConflictError instead
    // of a bare Error the shared handler flattened into 500 INTERNAL_ERROR.
    409: { ...commonErrorResponses[409], description: 'The per-tenant active-proposal cap is already reached' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/proposals',
  tags: ['Governance', 'Proposals'],
  summary: 'List proposals',
  // KS-448: the service JWT-authenticates every /api route (pen-test H2), so the
  // KS-144-era public marker had drifted from runtime. Reference reads stay
  // auth-required per the KS-424 pt-2 decision.
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Proposals',
      content: { 'application/json': { schema: ProposalListResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/proposals/active',
  tags: ['Governance', 'Proposals'],
  summary: 'List currently-active proposals (status=active, not expired)',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Active proposals',
      content: { 'application/json': { schema: ProposalListResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/proposals/{id}',
  tags: ['Governance', 'Proposals'],
  summary: 'Get a proposal by id',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Proposal',
      // KS-498: enveloped `{ success, data }` like every governance read.
      content: { 'application/json': { schema: successEnvelope(ProposalSchema) } },
    },
    401: commonErrorResponses[401],
    404: commonErrorResponses[404],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/proposals/{id}/submit',
  tags: ['Governance', 'Proposals'],
  summary: 'Move a draft proposal to active voting',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    200: {
      description: 'Submitted',
      // KS-498: handler returns `{ success, data, message }`.
      content: { 'application/json': { schema: ProposalCreateResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Not in draft status' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    // KS-594: the runtime now refuses this with a typed ConflictError instead
    // of a bare Error the shared handler flattened into 500 INTERNAL_ERROR.
    409: { ...commonErrorResponses[409], description: 'The proposal is not in the draft state' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/proposals/{id}/cancel',
  tags: ['Governance', 'Proposals'],
  summary: 'Cancel a proposal (proposer or admin)',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    200: {
      description: 'Cancelled',
      // KS-498: handler returns `{ success, data, message }`.
      content: { 'application/json': { schema: ProposalCreateResponseSchema } },
    },
    401: commonErrorResponses[401],
    400: commonErrorResponses[400],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    // KS-594: the runtime now refuses this with a typed ConflictError instead
    // of a bare Error the shared handler flattened into 500 INTERNAL_ERROR.
    409: { ...commonErrorResponses[409], description: 'The proposal is in a state that cannot be cancelled' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/proposals/{id}/execute',
  tags: ['Governance', 'Proposals'],
  summary: 'Execute a passed proposal',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    200: {
      description: 'Executed',
      // KS-498: handler returns `{ success, data, message }`.
      content: { 'application/json': { schema: ProposalCreateResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Not passed or not yet votable' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    // KS-594: the runtime now refuses this with a typed ConflictError instead
    // of a bare Error the shared handler flattened into 500 INTERNAL_ERROR.
    409: { ...commonErrorResponses[409], description: 'The proposal is not queued, or its timelock has not passed' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/proposals/{id}/vote',
  tags: ['Governance', 'Proposals'],
  summary: 'Cast a vote on an active proposal',
  description: 'Vote weight is multiplied by the participant\'s tier multiplier.',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
    // KS-444: required — the runtime 400s a bodyless request (vote is
    // mandatory), so don't publish the body as optional.
    body: { content: { 'application/json': { schema: VoteRequestSchema } }, required: true },
  },
  responses: {
    200: {
      description: 'Vote recorded',
      // KS-450: the gateway mock is removed — the real service answers with the
      // `{ success, data: <vote record>, message }` envelope.
      content: { 'application/json': { schema: VoteCastResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    409: { ...commonErrorResponses[409], description: 'Already voted on this proposal' },
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/proposals/{id}/votes',
  tags: ['Governance', 'Proposals'],
  summary: 'List all votes cast on a proposal',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Votes',
      content: { 'application/json': { schema: VoteListResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — delegation
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/delegate',
  tags: ['Governance', 'Delegation'],
  summary: 'Delegate voting power to another participant',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: required — the runtime 400s a bodyless request (delegateId +
    // allProposals are mandatory), so don't publish the body as optional.
    body: { content: { 'application/json': { schema: DelegateRequestSchema } }, required: true },
  },
  responses: {
    200: {
      description: 'Delegation set',
      content: { 'application/json': { schema: GovernanceSuccessSchema } },
    },
    401: commonErrorResponses[401],
    400: commonErrorResponses[400],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'delete',
  path: '/api/governance/delegate',
  tags: ['Governance', 'Delegation'],
  summary: 'Revoke an existing delegation',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Delegation revoked',
      content: { 'application/json': { schema: GovernanceSuccessSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — state + config + admin
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/state',
  security: [{ bearerAuth: [] }],
  tags: ['Governance'],
  summary: 'Live governance state (counts of proposals/participants/votes)',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'State',
      content: { 'application/json': { schema: GovernanceStateSchema } },
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/config',
  security: [{ bearerAuth: [] }],
  tags: ['Governance'],
  summary: 'Governance config (vote multipliers, tier thresholds, defaults)',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Config',
      // KS-440: the handler wraps config in the `{ success, data }` envelope
      // (routes/governance.ts GET /config) — publish the envelope, not the bare
      // config object.
      content: { 'application/json': { schema: successEnvelope(GovernanceConfigSchema) } },
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/governance/stats',
  security: [{ bearerAuth: [] }],
  tags: ['Governance'],
  summary: 'Aggregate governance stats',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Stats',
      // KS-440: the handler wraps stats in the `{ success, data }` envelope
      // (routes/governance.ts GET /stats) — publish the envelope, not the bare
      // stats object.
      content: { 'application/json': { schema: successEnvelope(GovernanceStatsSchema) } },
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/governance/process-expired',
  tags: ['Governance', 'Admin'],
  summary: 'Sweep expired proposals (admin/cron)',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Sweep complete',
      content: { 'application/json': { schema: GovernanceSuccessSchema } },
    },
    401: commonErrorResponses[401],
    403: { ...commonErrorResponses[403], description: 'Admin role required' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});
