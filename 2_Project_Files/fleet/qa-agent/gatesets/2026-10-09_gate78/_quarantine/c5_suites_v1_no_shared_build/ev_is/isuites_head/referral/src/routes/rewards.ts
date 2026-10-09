/**
 * =============================================================================
 * REWARD ROUTES
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { referralService } from '../services/referralService';
import { milestoneService } from '../services/milestoneService';
import { RewardStatus, RewardType } from '../types/referral.types';
const router = Router();

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

const claimRewardsSchema = z.object({
  userId: z.string().uuid(),
  rewardIds: z.array(z.string().uuid()).min(1).max(50),
  walletAddress: z.string().min(1),
});

// =============================================================================
// ROUTES
// =============================================================================

/**
 * Get user's rewards
 * GET /api/rewards/user/:userId
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

    const allRewards = await referralService.getUserRewards(userId);
    const milestoneRewards = await milestoneService.getPendingRewards(userId);
    
    // Combine and categorise
    const combined = [...allRewards, ...milestoneRewards];
    
    const pending = combined.filter(
      r => r.status === RewardStatus.PENDING || r.status === RewardStatus.CLAIMABLE
    );
    const claimed = combined.filter(
      r => r.status === RewardStatus.CLAIMED || r.status === RewardStatus.DISTRIBUTED
    );

    const totalPending = pending.reduce((sum, r) => sum + r.amount, BigInt(0));
    const totalClaimed = claimed.reduce((sum, r) => sum + r.amount, BigInt(0));

    res.json({
      success: true,
      data: {
        summary: {
          pendingCount: pending.length,
          pendingTotal: `${Number(totalPending) / 1_000_000} SECURA`,
          claimedCount: claimed.length,
          claimedTotal: `${Number(totalClaimed) / 1_000_000} SECURA`,
          lifetimeTotal: `${(Number(totalPending) + Number(totalClaimed)) / 1_000_000} SECURA`,
        },
        pending: pending.map(r => ({
          id: r.id,
          type: r.type,
          typeLabel: getRewardTypeLabel(r.type),
          amount: `${Number(r.amount) / 1_000_000} SECURA`,
          sourceType: r.sourceType,
          createdAt: r.createdAt,
          canClaim: r.status === RewardStatus.CLAIMABLE,
        })),
        claimed: claimed.slice(0, 20).map(r => ({
          id: r.id,
          type: r.type,
          typeLabel: getRewardTypeLabel(r.type),
          amount: `${Number(r.amount) / 1_000_000} SECURA`,
          claimedAt: r.claimedAt,
          transactionHash: r.transactionHash,
        })),
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Claim pending rewards
 * POST /api/rewards/claim
 */
router.post('/claim', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const body = claimRewardsSchema.parse(req.body);
    
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const authUserId = (req as any).user?.userId as string;
    if (authUserId && authUserId !== body.userId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised' } });
    }

    const result = await referralService.claimRewards(
      body.userId,
      body.rewardIds,
      body.walletAddress
    );

    const totalClaimed = result.claimed.reduce(
      (sum, r) => sum + r.amount, 
      BigInt(0)
    );

    res.json({
      success: true,
      data: {
        claimed: result.claimed.map(r => ({
          id: r.id,
          amount: `${Number(r.amount) / 1_000_000} SECURA`,
          type: r.type,
        })),
        failed: result.failed,
        totalClaimed: `${Number(totalClaimed) / 1_000_000} SECURA`,
        message: result.claimed.length > 0
          ? `Successfully claimed ${result.claimed.length} reward(s). Tokens will be sent to ${body.walletAddress}`
          : 'No rewards were claimed',
        // In production, return transaction details
        transactionPending: result.claimed.length > 0,
      },
    });
  } catch (error) {
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
 * Get reward history
 * GET /api/rewards/history/:userId
 */
router.get('/history/:userId', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId } = req.params;
    const { page = '1', limit = '20', type } = req.query;

    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const authUserId = (req as any).user?.userId as string;
    if (authUserId && authUserId !== userId) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorised to view this data' } });
    }

    let rewards = await referralService.getUserRewards(userId);
    
    // Filter by type if specified
    if (type && typeof type === 'string') {
      rewards = rewards.filter(r => r.type === type);
    }

    // Sort by date (newest first)
    rewards.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());

    // Pagination
    const pageNum = parseInt(page as string, 10);
    const limitNum = parseInt(limit as string, 10);
    const startIndex = (pageNum - 1) * limitNum;
    const endIndex = startIndex + limitNum;
    const paginatedRewards = rewards.slice(startIndex, endIndex);

    res.json({
      success: true,
      data: {
        rewards: paginatedRewards.map(r => ({
          id: r.id,
          type: r.type,
          typeLabel: getRewardTypeLabel(r.type),
          amount: `${Number(r.amount) / 1_000_000} SECURA`,
          status: r.status,
          sourceType: r.sourceType,
          createdAt: r.createdAt,
          claimedAt: r.claimedAt,
          transactionHash: r.transactionHash,
          metadata: r.metadata,
        })),
        pagination: {
          page: pageNum,
          limit: limitNum,
          total: rewards.length,
          totalPages: Math.ceil(rewards.length / limitNum),
          hasMore: endIndex < rewards.length,
        },
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get reward statistics
 * GET /api/rewards/stats/:userId
 */
router.get('/stats/:userId', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId } = req.params;

    const rewards = await referralService.getUserRewards(userId);
    
    // Group by type
    const byType = new Map<RewardType, bigint>();
    for (const reward of rewards) {
      if (reward.status === RewardStatus.CLAIMED || reward.status === RewardStatus.DISTRIBUTED) {
        const current = byType.get(reward.type) || BigInt(0);
        byType.set(reward.type, current + reward.amount);
      }
    }

    // Group by month
    const byMonth = new Map<string, bigint>();
    for (const reward of rewards) {
      if (reward.status === RewardStatus.CLAIMED || reward.status === RewardStatus.DISTRIBUTED) {
        const month = new Date(reward.createdAt).toISOString().slice(0, 7); // YYYY-MM
        const current = byMonth.get(month) || BigInt(0);
        byMonth.set(month, current + reward.amount);
      }
    }

    res.json({
      success: true,
      data: {
        byType: Object.fromEntries(
          Array.from(byType.entries()).map(([type, amount]) => [
            type,
            `${Number(amount) / 1_000_000} SECURA`,
          ])
        ),
        byMonth: Object.fromEntries(
          Array.from(byMonth.entries())
            .sort((a, b) => b[0].localeCompare(a[0]))
            .slice(0, 12)
            .map(([month, amount]) => [
              month,
              `${Number(amount) / 1_000_000} SECURA`,
            ])
        ),
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// HELPERS
// =============================================================================

function getRewardTypeLabel(type: RewardType): string {
  switch (type) {
    case RewardType.REFERRAL_BONUS:
      return 'Signup Bonus';
    case RewardType.REFERRER_REWARD:
      return 'Referral Reward';
    case RewardType.MILESTONE_REWARD:
      return 'Milestone Achievement';
    case RewardType.AMBASSADOR_BONUS:
      return 'Ambassador Bonus';
    case RewardType.LEADERBOARD_PRIZE:
      return 'Leaderboard Prize';
    default:
      return 'Reward';
  }
}

export { router as rewardsRoutes };
