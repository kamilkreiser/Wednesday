/**
 * =============================================================================
 * REFERRAL ROUTES
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { referralService } from '../services/referralService';
const router = Router();

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

export const generateCodeSchema = z.object({
  customCode: z.string().trim().min(4).max(16).optional(),
  maxUses: z.number().int().min(1).max(10000).optional(),
  expiresInDays: z.number().int().min(1).max(365).optional(),
  customLabel: z.string().trim().max(100).optional(),
});

export const applyCodeSchema = z.object({
  code: z.string().trim().min(4).max(16),
  userId: z.string().uuid(),
  walletAddress: z.string().optional(),
  ipAddress: z.string().optional(),
  deviceId: z.string().optional(),
  email: z.string().trim().email().optional(),
});

// KS-444: the published spec (ReferralQualifyRequest) declares exactly one
// required plain string. The old manual `if (!userId)` check both rejected
// the spec-legal empty string with a 400 AND let spec-violating non-string
// bodies (e.g. `{ userId: {} }` — truthy) fall through to a 200-with-no-effect.
// Enforce exactly what the spec declares: userId present and a string.
export const qualifyReferralSchema = z.object({
  userId: z.string(),
});

// =============================================================================
// ROUTES
// =============================================================================

/**
 * Generate a new referral code
 * POST /api/referrals/generate
 */
router.post('/generate', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const authUser = (req as any).user;
    const userId = authUser?.userId as string;
    const walletAddress = (authUser?.walletAddress as string) || (req.headers['x-wallet-address'] as string);
    
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }

    const body = generateCodeSchema.parse(req.body);

    const code = await referralService.generateCode(userId, walletAddress, body);

    res.status(201).json({
      success: true,
      data: {
        id: code.id,
        code: code.code,
        shareUrl: `https://secuura.io/r/${code.code}`,
        createdAt: code.createdAt,
        expiresAt: code.expiresAt,
        maxUses: code.maxUses,
        customLabel: code.customLabel,
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: error.errors },
      });
    }
    if (error instanceof Error) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: error.message } });
    }
    next(error);
  }
});

/**
 * Get referral code details
 * GET /api/referrals/:code
 */
router.get('/:code', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { code } = req.params;
    const referralCode = await referralService.getCodeByString(code);

    if (!referralCode) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Referral code not found' } });
    }

    // Don't expose sensitive info for public lookup
    res.json({
      success: true,
      data: {
        code: referralCode.code,
        isActive: referralCode.isActive,
        isExpired: referralCode.expiresAt ? new Date() > referralCode.expiresAt : false,
        customLabel: referralCode.customLabel,
        // Add reward info for display
        referredReward: '25 SECURA',
        referrerReward: '50 SECURA',
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Apply a referral code (new user signup)
 * POST /api/referrals/apply
 */
router.post('/apply', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const body = applyCodeSchema.parse(req.body);

    const referral = await referralService.applyCode({
      code: body.code,
      userId: body.userId,
      walletAddress: body.walletAddress,
      ipAddress: body.ipAddress || req.ip,
      deviceId: body.deviceId,
      email: body.email,
    });

    res.status(201).json({
      success: true,
      data: {
        referralId: referral.id,
        status: referral.status,
        fraudCheckPassed: referral.fraudCheckPassed,
        signupBonus: referral.fraudCheckPassed ? '25 SECURA' : '0 SECURA',
        message: referral.fraudCheckPassed 
          ? 'Referral applied successfully! Complete your first certification to unlock full rewards.'
          : 'Referral could not be verified. Please contact support if you believe this is an error.',
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: error.errors },
      });
    }
    if (error instanceof Error) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: error.message } });
    }
    next(error);
  }
});

/**
 * Get user's referral statistics
 * GET /api/referrals/user/:userId
 */
router.get('/user/:userId', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId } = req.params;
    
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const authUserId = (req as any).user?.userId as string;
    if (authUserId && authUserId !== userId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised to view this data' } });
    }

    const stats = await referralService.getUserStats(userId);

    if (!stats) {
      // Generate a code if user doesn't have one
      return res.json({
        success: true,
        data: {
          hasCode: false,
          message: 'Generate your referral code to start earning rewards',
        },
      });
    }

    res.json({
      success: true,
      data: {
        hasCode: true,
        referralCode: {
          code: stats.referralCode.code,
          shareUrl: `https://secuura.io/r/${stats.referralCode.code}`,
          isActive: stats.referralCode.isActive,
          expiresAt: stats.referralCode.expiresAt,
        },
        stats: {
          totalReferrals: stats.stats.totalReferrals,
          qualifiedReferrals: stats.stats.activeReferrals,
          conversionRate: `${stats.stats.conversionRate.toFixed(1)}%`,
          totalRewardsEarned: `${Number(stats.totalRewardsEarned) / 1_000_000} SECURA`,
          pendingRewards: `${stats.pendingRewards.reduce((sum, r) => sum + Number(r.amount), 0) / 1_000_000} SECURA`,
        },
        milestoneProgress: {
          currentTier: stats.milestoneProgress.currentTier,
          qualifiedReferrals: stats.milestoneProgress.qualifiedReferrals,
          nextMilestone: stats.milestoneProgress.nextMilestone ? {
            name: stats.milestoneProgress.nextMilestone.name,
            requiredReferrals: stats.milestoneProgress.nextMilestone.requiredReferrals,
            reward: `${Number(stats.milestoneProgress.nextMilestone.rewardAmount) / 1_000_000} SECURA`,
            badge: stats.milestoneProgress.nextMilestone.badge,
          } : null,
          progressToNext: `${stats.milestoneProgress.progressToNext.toFixed(0)}%`,
          milestonesAchieved: stats.milestoneProgress.milestonesAchieved.map(m => ({
            tier: m.tier,
            achievedAt: m.achievedAt,
            reward: `${Number(m.rewardAmount) / 1_000_000} SECURA`,
          })),
        },
        pendingRewardsCount: stats.pendingRewards.length,
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get users referred by a referrer
 * GET /api/referrals/user/:userId/referred
 */
router.get('/user/:userId/referred', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId } = req.params;
    
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const authUserId = (req as any).user?.userId as string;
    if (authUserId && authUserId !== userId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised to view this data' } });
    }

    const referredUsers = await referralService.getReferredUsers(userId);

    res.json({
      success: true,
      data: {
        total: referredUsers.length,
        referredUsers: referredUsers.map(u => ({
          // In production, fetch display names from user service
          displayName: `User ${u.userId.substring(0, 8)}...`,
          status: u.status,
          joinedAt: u.joinedAt,
        })),
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Qualify a referral (internal endpoint - called when user completes action)
 * POST /api/referrals/qualify
 */
router.post('/qualify', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-444: validate against the spec's declared shape (see schema above).
    const { userId } = qualifyReferralSchema.parse(req.body);

    const referral = await referralService.qualifyReferral(userId);

    if (!referral) {
      return res.json({
        success: true,
        data: {
          qualified: false,
          message: 'No pending referral found for this user',
        },
      });
    }

    res.json({
      success: true,
      data: {
        qualified: true,
        referralId: referral.id,
        referrerId: referral.referrerId,
        qualifiedAt: referral.qualifiedAt,
      },
    });
  } catch (error) {
    // KS-444: spec declares 400 for a bad request body — answer the ZodError
    // here with the canonical envelope (same shape as /generate and /apply)
    // rather than letting the shared errorHandler pick the status.
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Validation error', details: error.errors },
      });
    }
    next(error);
  }
});

/**
 * Deactivate a referral code
 * DELETE /api/referrals/:codeId
 */
router.delete('/:codeId', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { codeId } = req.params;
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const userId = (req as any).user?.userId as string;
    
    if (!userId) {
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }

    const deactivated = await referralService.deactivateCode(codeId, userId);

    if (!deactivated) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Referral code not found' } });
    }

    res.json({
      success: true,
      message: 'Referral code deactivated',
    });
  } catch (error) {
    if (error instanceof Error) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: error.message } });
    }
    next(error);
  }
});

export { router as referralRoutes };
