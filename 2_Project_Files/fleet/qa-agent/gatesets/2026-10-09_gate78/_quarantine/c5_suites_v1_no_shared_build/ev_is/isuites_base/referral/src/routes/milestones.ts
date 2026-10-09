/**
 * =============================================================================
 * MILESTONE ROUTES
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { milestoneService, MILESTONES } from '../services/milestoneService';
import { referralService } from '../services/referralService';
import { ReferralStatus } from '../types/referral.types';

const router = Router();

// =============================================================================
// ROUTES
// =============================================================================

/**
 * Get all milestone definitions
 * GET /api/milestones
 */
router.get('/', (_req: Request, res: Response) => {
  const milestones = MILESTONES.map(m => ({
    id: m.id,
    name: m.name,
    description: m.description,
    tier: m.tier,
    requiredReferrals: m.requiredReferrals,
    reward: `${Number(m.rewardAmount) / 1_000_000} SECURA`,
    badge: m.badge,
    specialPerks: m.specialPerks,
    ongoingBonus: m.ongoingBonus ? `${m.ongoingBonus}% ongoing bonus` : undefined,
  }));

  res.json({
    success: true,
    data: {
      milestones,
      tiers: [
        { tier: 'FIRST_REFERRAL', referrals: 1, badge: '🌱' },
        { tier: 'BRONZE', referrals: 5, badge: '🥉' },
        { tier: 'SILVER', referrals: 25, badge: '🥈' },
        { tier: 'GOLD', referrals: 100, badge: '🥇' },
        { tier: 'PLATINUM', referrals: 500, badge: '💎' },
        { tier: 'AMBASSADOR', referrals: 1000, badge: '👑' },
      ],
    },
  });
});

/**
 * Get user's milestone progress
 * GET /api/milestones/user/:userId
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

    const progress = await milestoneService.getUserProgress(userId);

    res.json({
      success: true,
      data: {
        currentTier: progress.currentTier,
        qualifiedReferrals: progress.qualifiedReferrals,
        totalMilestoneRewards: `${Number(progress.totalMilestoneRewards) / 1_000_000} SECURA`,
        progressToNext: {
          percentage: `${progress.progressToNext.toFixed(0)}%`,
          nextMilestone: progress.nextMilestone ? {
            name: progress.nextMilestone.name,
            tier: progress.nextMilestone.tier,
            requiredReferrals: progress.nextMilestone.requiredReferrals,
            reward: `${Number(progress.nextMilestone.rewardAmount) / 1_000_000} SECURA`,
            badge: progress.nextMilestone.badge,
            referralsNeeded: progress.nextMilestone.requiredReferrals - progress.qualifiedReferrals,
          } : null,
        },
        achieved: progress.milestonesAchieved.map(m => {
          const milestone = milestoneService.getMilestoneByTier(m.tier);
          return {
            tier: m.tier,
            name: milestone?.name,
            badge: milestone?.badge,
            achievedAt: m.achievedAt,
            reward: `${Number(m.rewardAmount) / 1_000_000} SECURA`,
            claimed: !!m.claimedAt,
          };
        }),
        activeBenefits: progress.currentTier
          ? milestoneService.getTierBenefits(progress.currentTier)
          : [],
        ambassadorBonus: await milestoneService.getOngoingBonusPercentage(userId),
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Check and award milestones for user
 * POST /api/milestones/check/:userId
 */
router.post('/check/:userId', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId } = req.params;

    // Get qualified referral count
    const referrals = await referralService.getReferralsByReferrer(userId);
    const qualifiedCount = referrals.filter(
      r => r.status === ReferralStatus.QUALIFIED || r.status === ReferralStatus.REWARDED
    ).length;

    // Check and award
    const result = await milestoneService.checkAndAwardMilestones(userId, qualifiedCount);

    if (result.newMilestones.length === 0) {
      return res.json({
        success: true,
        data: {
          newMilestones: [],
          message: 'No new milestones achieved',
        },
      });
    }

    res.json({
      success: true,
      data: {
        newMilestones: result.newMilestones.map(m => ({
          id: m.id,
          name: m.name,
          tier: m.tier,
          badge: m.badge,
          reward: `${Number(m.rewardAmount) / 1_000_000} SECURA`,
          specialPerks: m.specialPerks,
        })),
        newRewards: result.rewards.map(r => ({
          id: r.id,
          amount: `${Number(r.amount) / 1_000_000} SECURA`,
          type: r.type,
        })),
        message: `Congratulations! You achieved ${result.newMilestones.length} new milestone(s)!`,
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get tier benefits
 * GET /api/milestones/benefits/:tier
 */
router.get('/benefits/:tier', (req: Request, res: Response) => {
  const { tier } = req.params;
  
  const milestone = milestoneService.getMilestoneByTier(tier as any);
  
  if (!milestone) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Tier not found' } });
  }

  res.json({
    success: true,
    data: {
      tier: milestone.tier,
      name: milestone.name,
      badge: milestone.badge,
      benefits: milestone.specialPerks || [],
      ongoingBonus: milestone.ongoingBonus ? `${milestone.ongoingBonus}% on future referrals` : null,
    },
  });
});

export { router as milestonesRoutes };
