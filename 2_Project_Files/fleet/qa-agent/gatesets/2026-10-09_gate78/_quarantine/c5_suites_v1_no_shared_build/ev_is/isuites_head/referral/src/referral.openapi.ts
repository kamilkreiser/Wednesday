/**
 * =============================================================================
 * REFERRAL SERVICE — OpenAPI registrations
 * =============================================================================
 *
 * Referral codes, milestones, rewards, leaderboard. Four sub-routers
 * mounted under /api/{referrals,milestones,rewards,leaderboard}.
 *
 * Endpoints registered (20 paths, all 20 routes):
 *   Referrals:
 *     - POST   /api/referrals/generate
 *     - GET    /api/referrals/{code}
 *     - POST   /api/referrals/apply
 *     - GET    /api/referrals/user/{userId}
 *     - GET    /api/referrals/user/{userId}/referred
 *     - POST   /api/referrals/qualify
 *     - DELETE /api/referrals/{codeId}
 *   Milestones:
 *     - GET  /api/milestones
 *     - GET  /api/milestones/user/{userId}
 *     - POST /api/milestones/check/{userId}
 *     - GET  /api/milestones/benefits/{tier}
 *   Rewards:
 *     - GET  /api/rewards/user/{userId}
 *     - POST /api/rewards/claim
 *     - GET  /api/rewards/history/{userId}
 *     - GET  /api/rewards/stats/{userId}
 *   Leaderboard:
 *     - GET /api/leaderboard
 *     - GET /api/leaderboard/monthly
 *     - GET /api/leaderboard/position/{userId}
 * =============================================================================
 */

import { z, sharedRegistry, commonErrorResponses, successEnvelope, FX } from '@secuura/shared';

// -----------------------------------------------------------------------------
// SCHEMAS
// -----------------------------------------------------------------------------

const ReferralTierEnum = z.enum(['bronze', 'silver', 'gold', 'platinum']);
const RewardStatusEnum = z.enum(['pending', 'claimable', 'claimed', 'expired']);

const ReferralCodeSchema = sharedRegistry.register(
  'ReferralCode',
  z
    .object({
      id: z.string(),
      code: z.string(),
      ownerUserId: z.string(),
      uses: z.number().int().nonnegative(),
      maxUses: z.number().int().nullable().optional(),
      active: z.boolean(),
      createdAt: z.string(),
      expiresAt: z.string().nullable().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    code: 'example-code',
    ownerUserId: 'example-ownerUserId',
    uses: 0,
    active: true,
    createdAt: 'example-createdAt',
  },
  }),
);

const ReferralGenerateRequestSchema = sharedRegistry.register(
  'ReferralGenerateRequest',
  // KS-444: reconciled with the runtime validator `generateCodeSchema`
  // (routes/referrals.ts). The spec previously declared a required body
  // `userId` (the handler derives the owner from the bearer token — pen-test
  // F-04 — and never reads it) and an `expiresAt` datetime the handler
  // ignores; it also omitted the real fields `expiresInDays`/`customLabel`
  // and the genuine 4-16 length bound on customCode — so a spec-legal
  // one-char code earned a 400. All fields are optional: an empty body
  // generates a random code. Note: custom codes additionally pass a
  // fraud-pattern check (no sequential/repetitive characters), which is
  // business logic beyond the schema and still answers 400.
  z.object({
    // KS-475 (§4): publish the runtime's charset+length as a pattern.
    // validateCustomCode uppercases first, then enforces ^[A-Z0-9]+$ and 4-16
    // — so the published charset is case-insensitive. The remaining rules —
    // reserved words, profanity list, sequential/repetitive scan — are
    // list/arithmetic checks a regex can't express; they stay documented
    // business validation (400 "Invalid custom code: …").
    customCode: z
      .string()
      .regex(/^[A-Za-z0-9]{4,16}$/)
      .optional()
      .openapi({
        description:
          'Vanity code: 4-16 letters/digits (case-insensitive; stored ' +
          'uppercased). Omit to have one generated. Additionally rejected ' +
          '(400) when the code is a reserved word, contains a blocked ' +
          'pattern, or uses sequential/repetitive characters (e.g. "0000", "ABCD").',
      }),
    maxUses: z.number().int().min(1).max(10000).optional(),
    expiresInDays: z.number().int().min(1).max(365).optional(),
    customLabel: z.string().max(100).optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    customCode: 'aaaa',
    maxUses: 1,
    expiresInDays: 1,
    customLabel: 'example-customLabel',
  },
  }),
);

const ReferralApplyRequestSchema = sharedRegistry.register(
  'ReferralApplyRequest',
  // KS-444: reconciled with the runtime validator `applyCodeSchema`
  // (routes/referrals.ts). The genuine contract bounds `code` to 4-16 chars
  // (all issued codes are in that range) and `userId` to a uuid (the users
  // table key), and accepts optional fraud-signal fields — the spec's former
  // plain strings meant spec-legal values earned validation 400s. Published
  // here as documentation of reality.
  z.object({
    code: z.string().min(4).max(16),
    userId: z.string().uuid().openapi({
      description: 'The user who is applying the referral code (the referee).',
    }),
    walletAddress: z.string().optional(),
    ipAddress: z.string().optional(),
    deviceId: z.string().optional(),
    email: z.string().email().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    code: 'example-code',
    userId: FX.issuer.id,
  },
  }),
);

const ReferralQualifyRequestSchema = sharedRegistry.register(
  'ReferralQualifyRequest',
  z.object({
    userId: z.string().openapi({
      description:
        'Marks the referee as having met the qualification threshold (e.g. ' +
        'first paid certification). Triggers the referrer\'s milestone check + reward.',
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    userId: FX.issuer.id,
  },
  }),
);

// KS-440: publish the real milestone definition (milestones.ts GET /). Each
// entry is { id, name, description, tier(uppercase string), requiredReferrals,
// reward(string), badge, specialPerks?, ongoingBonus? }. The old schema used the
// lowercase ReferralTierEnum and a `requiredQualifiedReferrals` field the runtime
// never emits; republish the fields actually returned.
const MilestoneSchema = sharedRegistry.register(
  'Milestone',
  z
    .object({
      id: z.string().optional(),
      name: z.string().optional(),
      description: z.string().optional(),
      tier: z.string(),
      requiredReferrals: z.number().int().nonnegative(),
      reward: z.string().optional(),
      badge: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    tier: 'example-tier',
    requiredReferrals: 0,
  },
  }),
);

// KS-440: POST /api/milestones/check/{userId} returns the enveloped
// re-evaluation result `{ success, data: { newMilestones, message, newRewards? } }`
// (milestones.ts POST /check/:userId) — NOT the UserMilestone progress shape the
// spec previously published (which required userId/currentTier/qualifiedReferrals,
// none of which this endpoint emits).
const MilestoneCheckResponseSchema = sharedRegistry.register(
  'MilestoneCheckResponse',
  successEnvelope(
    z
      .object({
        newMilestones: z.array(z.record(z.string(), z.unknown())),
        newRewards: z.array(z.record(z.string(), z.unknown())).optional(),
        message: z.string().optional(),
      })
      .passthrough(),
  ).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      newMilestones: [
        {},
        {},
      ],
    },
  },
  }),
);

const UserMilestoneSchema = sharedRegistry.register(
  'UserMilestone',
  z
    .object({
      userId: z.string(),
      currentTier: ReferralTierEnum,
      qualifiedReferrals: z.number().int().nonnegative(),
      nextTier: ReferralTierEnum.nullable().optional(),
      remainingForNext: z.number().int().nullable().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    userId: FX.issuer.id,
    currentTier: 'bronze',
    qualifiedReferrals: 0,
  },
  }),
);

const TierBenefitsSchema = sharedRegistry.register(
  'TierBenefits',
  z
    .object({
      tier: ReferralTierEnum,
      benefits: z.array(z.string()),
      multiplier: z.number().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    tier: 'bronze',
    benefits: [
      'example-benefits[]',
      'example-benefits[]',
    ],
  },
  }),
);

const RewardSchema = sharedRegistry.register(
  'Reward',
  z
    .object({
      id: z.string(),
      userId: z.string(),
      type: z.string(),
      amount: z.number(),
      currency: z.string().optional(),
      status: RewardStatusEnum,
      reason: z.string().nullable().optional(),
      createdAt: z.string(),
      claimedAt: z.string().nullable().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    userId: FX.issuer.id,
    type: 'example-type',
    amount: 1,
    status: 'pending',
    createdAt: 'example-createdAt',
  },
  }),
);

const RewardClaimRequestSchema = sharedRegistry.register(
  'RewardClaimRequest',
  // KS-430: reconciled with the runtime validator `claimRewardsSchema`
  // (routes/rewards.ts). The published schema declared a single `rewardId`,
  // but the handler requires `userId` (the claiming user), a non-empty
  // `rewardIds` array (the rewards to claim), and `walletAddress` (the payout
  // target) — a `{ rewardId }` body earned a 400 (invalid_type/Required).
  // KS-444 re-adjudication: the uuid formats and the non-empty walletAddress
  // ARE the genuine contract (userId/reward ids are uuid table keys; the
  // runtime rejects anything else), so they are now published as
  // documentation of reality — spec-legal plain strings were still earning
  // validation 400s.
  z.object({
    userId: z.string().uuid().openapi({
      description: 'The user claiming the rewards (must own them).',
    }),
    rewardIds: z
      .array(z.string().uuid())
      .min(1)
      .max(50)
      .openapi({ description: 'IDs of the rewards to claim (1-50).' }),
    walletAddress: z.string().min(1).openapi({
      description: 'Destination wallet the claimed tokens are sent to.',
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    userId: FX.issuer.id,
    rewardIds: [
      '550e8400-e29b-41d4-a716-446655440000',
      '550e8400-e29b-41d4-a716-446655440000',
    ],
    walletAddress: 'addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgse35a3x',
  },
  }),
);

// KS-440: publish the real formatted entry (leaderboard.ts
// `formatLeaderboardEntry`). It emits rank/displayName/totalReferrals/
// qualifiedReferrals/totalRewardsEarned(string)/tier(uppercase string like
// BRONZE/AMBASSADOR)/badge — it does NOT emit `userId` or `score`, and `tier`
// is not the lowercase ReferralTierEnum. Republish the fields actually returned.
const LeaderboardEntrySchema = sharedRegistry.register(
  'LeaderboardEntry',
  z
    .object({
      rank: z.number().int().positive(),
      displayName: z.string(),
      totalReferrals: z.number().int().nonnegative(),
      qualifiedReferrals: z.number().int().nonnegative(),
      totalRewardsEarned: z.string().optional(),
      tier: z.string().optional(),
      badge: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    rank: 1,
    displayName: FX.issuer.displayName,
    totalReferrals: 0,
    qualifiedReferrals: 0,
  },
  }),
);

// KS-440: the runtime is enveloped — `{ success, data: { period, entries,
// pagination, updatedAt } }` (leaderboard.ts), and the monthly variant adds
// `month` + `prizes` (allowed via passthrough). The old schema published a bare
// `{ entries, total }`, so `entries` was flagged required-but-absent (it lives
// under `data`). Republish the envelope.
const LeaderboardResponseSchema = sharedRegistry.register(
  'LeaderboardResponse',
  successEnvelope(
    z
      .object({
        period: z.string(),
        entries: z.array(LeaderboardEntrySchema),
        pagination: z
          .object({
            page: z.number().int().optional(),
            limit: z.number().int().optional(),
            total: z.number().int().optional(),
          })
          .passthrough()
          .optional(),
        updatedAt: z.string().optional(),
      })
      .passthrough(),
  ).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      period: 'example-period',
      entries: [
        {
          rank: 1,
          displayName: FX.issuer.displayName,
          totalReferrals: 0,
          qualifiedReferrals: 0,
        },
        {
          rank: 1,
          displayName: FX.issuer.displayName,
          totalReferrals: 0,
          qualifiedReferrals: 0,
        },
      ],
    },
  },
  }),
);

const ReferralSuccessSchema = sharedRegistry.register(
  'ReferralSuccess',
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
// ROUTES — referrals
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/referrals/generate',
  tags: ['Referrals'],
  summary: 'Generate a referral code for a user',
  security: [{ bearerAuth: [] }],
  request: {
    body: { content: { 'application/json': { schema: ReferralGenerateRequestSchema } } },
  },
  responses: {
    201: {
      description: 'Code generated',
      // KS-498: the handler (routes/referrals.ts) returns a `{ success, data }`
      // envelope with a share-ready projection — id/code/shareUrl/createdAt/
      // maxUses always, expiresAt/customLabel only when set — not the full
      // ReferralCode record the read endpoints serve.
      content: {
        'application/json': {
          schema: z.object({
            success: z.literal(true),
            data: z
              .object({
                id: z.string(),
                code: z.string(),
                shareUrl: z.string(),
                createdAt: z.string(),
                expiresAt: z.string().nullable().optional(),
                maxUses: z.number().int(),
                customLabel: z.string().nullable().optional(),
              })
              .passthrough(),
          }),
        },
      },
    },
    400: { ...commonErrorResponses[400], description: 'Validation error or code already taken' },
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
  path: '/api/referrals/{code}',
  security: [{ bearerAuth: [] }],
  tags: ['Referrals'],
  summary: 'Look up a referral code',
  request: { params: z.object({ code: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Code',
      // KS-1015: the handler (routes/referrals.ts, GET /:code) returns a success/data envelope
      // with a public projection: code, isActive, isExpired, referredReward and referrerReward
      // always, customLabel only when set. It leaves out id and ownerUserId on purpose (a public
      // lookup), so the spec follows the runtime. ReferralCodeSchema stays for the owner list.
      content: {
        'application/json': {
          schema: z.object({
            success: z.literal(true),
            data: z
              .object({
                code: z.string(),
                isActive: z.boolean(),
                isExpired: z.boolean(),
                customLabel: z.string().optional(),
                referredReward: z.string(),
                referrerReward: z.string(),
              })
              .passthrough(),
          }),
        },
      },
    },
    404: { ...commonErrorResponses[404], description: 'Code not found / inactive' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/referrals/apply',
  tags: ['Referrals'],
  summary: 'Apply a referral code to the calling user',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: the handler requires code+userId — a bodyless request is a 400.
    body: { content: { 'application/json': { schema: ReferralApplyRequestSchema } }, required: true },
  },
  responses: {
    200: {
      description: 'Applied',
      content: { 'application/json': { schema: ReferralSuccessSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Code invalid / expired / max-uses' },
    401: commonErrorResponses[401],
    409: { ...commonErrorResponses[409], description: 'User already applied a referral' },
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
  path: '/api/referrals/user/{userId}',
  tags: ['Referrals'],
  summary: 'List referral codes owned by a user',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Codes',
      content: {
        'application/json': {
          schema: z.object({ codes: z.array(ReferralCodeSchema) }),
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
  path: '/api/referrals/user/{userId}/referred',
  tags: ['Referrals'],
  summary: 'List users this user has referred',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Referred users',
      content: {
        'application/json': {
          schema: z.object({
            referees: z.array(
              z
                .object({
                  userId: z.string(),
                  appliedAt: z.string(),
                  qualified: z.boolean(),
                })
                .passthrough(),
            ),
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
  method: 'post',
  path: '/api/referrals/qualify',
  tags: ['Referrals'],
  summary: 'Mark a referee as qualified (svc-to-svc on first paid action)',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: the handler requires userId — a bodyless request is a 400.
    body: { content: { 'application/json': { schema: ReferralQualifyRequestSchema } }, required: true },
  },
  responses: {
    200: {
      description: 'Qualification recorded; milestone + reward triggered',
      content: { 'application/json': { schema: ReferralSuccessSchema } },
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
  path: '/api/referrals/{codeId}',
  tags: ['Referrals'],
  summary: 'Deactivate a referral code',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ codeId: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Code deactivated',
      content: { 'application/json': { schema: ReferralSuccessSchema } },
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
// ROUTES — milestones
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/milestones',
  security: [{ bearerAuth: [] }],
  tags: ['Milestones'],
  summary: 'List milestone tiers + thresholds',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Milestones',
      content: {
        'application/json': {
          // KS-440: runtime is enveloped { success, data: { milestones, tiers } }
          // (milestones.ts GET /). The old bare { milestones } flagged
          // `milestones` required-but-absent (it lives under `data`).
          schema: successEnvelope(
            z
              .object({
                milestones: z.array(MilestoneSchema),
                tiers: z.array(z.record(z.string(), z.unknown())).optional(),
              })
              .passthrough(),
          ),
        },
      },
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
  path: '/api/milestones/user/{userId}',
  tags: ['Milestones'],
  summary: 'Get a user\'s milestone progress',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Progress',
      content: { 'application/json': { schema: UserMilestoneSchema } },
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
  method: 'post',
  path: '/api/milestones/check/{userId}',
  tags: ['Milestones'],
  summary: 'Re-evaluate a user\'s milestone status (svc-to-svc / cron)',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Re-evaluation result',
      content: { 'application/json': { schema: MilestoneCheckResponseSchema } },
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
  path: '/api/milestones/benefits/{tier}',
  security: [{ bearerAuth: [] }],
  tags: ['Milestones'],
  summary: 'Get the benefits associated with a tier',
  request: {
    params: z.object({
      tier: ReferralTierEnum,
    }),
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Tier benefits',
      content: { 'application/json': { schema: TierBenefitsSchema } },
    },
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — rewards
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/rewards/user/{userId}',
  tags: ['Rewards'],
  summary: 'List a user\'s rewards (any status)',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Rewards',
      content: {
        'application/json': {
          schema: z.object({ rewards: z.array(RewardSchema) }),
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
  method: 'post',
  path: '/api/rewards/claim',
  tags: ['Rewards'],
  summary: 'Claim a claimable reward',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: the handler requires userId+rewardIds+walletAddress — a
    // bodyless request is a 400.
    body: { content: { 'application/json': { schema: RewardClaimRequestSchema } }, required: true },
  },
  responses: {
    200: {
      description: 'Claimed',
      content: { 'application/json': { schema: RewardSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Reward not claimable (pending / already claimed / expired)' },
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
  path: '/api/rewards/history/{userId}',
  tags: ['Rewards'],
  summary: 'Reward history for a user (claimed or expired)',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'History',
      content: {
        'application/json': {
          schema: z.object({ rewards: z.array(RewardSchema) }),
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
  path: '/api/rewards/stats/{userId}',
  tags: ['Rewards'],
  summary: 'Aggregate reward stats for a user',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Stats',
      content: { 'application/json': { schema: successEnvelope(z.object({ byType: z.record(z.string(), z.unknown()), byMonth: z.record(z.string(), z.unknown()) }).passthrough()) } },
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
// ROUTES — leaderboard
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/leaderboard',
  security: [{ bearerAuth: [] }],
  tags: ['Leaderboard'],
  summary: 'All-time leaderboard',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Leaderboard',
      content: { 'application/json': { schema: LeaderboardResponseSchema } },
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
  path: '/api/leaderboard/monthly',
  security: [{ bearerAuth: [] }],
  tags: ['Leaderboard'],
  summary: 'Current calendar-month leaderboard',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Monthly leaderboard',
      content: { 'application/json': { schema: LeaderboardResponseSchema } },
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
  path: '/api/leaderboard/position/{userId}',
  tags: ['Leaderboard'],
  summary: 'Get a user\'s leaderboard position + rank',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ userId: z.string().openapi({ example: FX.holder.id }) }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'User position',
      content: { 'application/json': { schema: successEnvelope(z.object({ userId: z.string(), ranked: z.boolean().optional(), message: z.string().optional() }).passthrough()) } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'User has no leaderboard entry' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});
