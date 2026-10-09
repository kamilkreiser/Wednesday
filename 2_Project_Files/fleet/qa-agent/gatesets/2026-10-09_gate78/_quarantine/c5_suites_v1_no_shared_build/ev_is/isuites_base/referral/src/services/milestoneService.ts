/**
 * =============================================================================
 * MILESTONE SERVICE
 * =============================================================================
 * Tracks and awards milestone achievements
 *
 * Storage: DB-only (svc_referral_milestones table)
 */

import { v4 as uuidv4 } from 'uuid';
import {
  Milestone,
  MilestoneTier,
  UserMilestoneProgress,
  AchievedMilestone,
  Reward,
  RewardType,
  RewardStatus,
} from '../types/referral.types';
import { createLogger } from '../utils/logger';
import { query, isDbAvailable } from '../db';

const logger = createLogger('milestone-service');

// =============================================================================
// MILESTONE DEFINITIONS
// =============================================================================

export const MILESTONES: Milestone[] = [
  {
    id: 'milestone-first',
    name: 'First Referral',
    description: 'Welcome to the Secuura community! Earn your first referral reward.',
    tier: MilestoneTier.FIRST_REFERRAL,
    requiredReferrals: 1,
    rewardAmount: BigInt(100_000_000), // 100 SECURA (6 decimals)
    badge: '🌱',
  },
  {
    id: 'milestone-bronze',
    name: 'Bronze Advocate',
    description: 'You\'re making an impact! 5 successful referrals.',
    tier: MilestoneTier.BRONZE,
    requiredReferrals: 5,
    rewardAmount: BigInt(500_000_000), // 500 SECURA
    badge: '🥉',
    specialPerks: ['Early access to new features'],
  },
  {
    id: 'milestone-silver',
    name: 'Silver Champion',
    description: 'Outstanding growth! 25 successful referrals.',
    tier: MilestoneTier.SILVER,
    requiredReferrals: 25,
    rewardAmount: BigInt(2_500_000_000), // 2,500 SECURA
    badge: '🥈',
    specialPerks: ['Priority support', '10% fee discount'],
  },
  {
    id: 'milestone-gold',
    name: 'Gold Partner',
    description: 'Exceptional contribution! 100 successful referrals.',
    tier: MilestoneTier.GOLD,
    requiredReferrals: 100,
    rewardAmount: BigInt(10_000_000_000), // 10,000 SECURA
    badge: '🥇',
    specialPerks: ['Priority support', '20% fee discount', 'Exclusive events access'],
  },
  {
    id: 'milestone-platinum',
    name: 'Platinum Elite',
    description: 'Elite status achieved! 500 successful referrals.',
    tier: MilestoneTier.PLATINUM,
    requiredReferrals: 500,
    rewardAmount: BigInt(50_000_000_000), // 50,000 SECURA
    badge: '💎',
    specialPerks: ['Dedicated account manager', '30% fee discount', 'VIP events'],
  },
  {
    id: 'milestone-ambassador',
    name: 'Secuura Ambassador',
    description: 'You are a true ambassador! 1,000+ successful referrals.',
    tier: MilestoneTier.AMBASSADOR,
    requiredReferrals: 1000,
    rewardAmount: BigInt(100_000_000_000), // 100,000 SECURA
    badge: '👑',
    specialPerks: [
      'Official Ambassador status',
      '50% fee discount',
      'Revenue sharing',
      'Governance voting power',
    ],
    ongoingBonus: 5, // 5% ongoing bonus on all future referrals
  },
];

// =============================================================================
// MILESTONE SERVICE
// =============================================================================

export class MilestoneService {

  // ==========================================================================
  // DATABASE READ HELPERS
  // ==========================================================================

  /**
   * Fetch a single user's milestone progress from the DB.
   * Returns null when the DB is unavailable or no row exists.
   */
  private async dbGetUserProgress(userId: string): Promise<UserMilestoneProgress | null> {
    if (!isDbAvailable()) return null;
    try {
      const result = await query<{
        user_id: string; milestones_completed: string; total_referrals: number;
        total_rewards_earned: string; current_tier: string | null;
      }>('SELECT * FROM svc_referral_milestones WHERE user_id = $1', [userId]);

      if (result.rows.length === 0) return null;

      const r = result.rows[0];
      return this.rowToProgress(r);
    } catch (err: any) {
      logger.error('DB read user progress failed', { userId, error: err?.message });
      return null;
    }
  }

  /**
   * Fetch pending milestone rewards for a user from the DB.
   */
  private async dbGetPendingRewards(userId: string): Promise<Reward[]> {
    if (!isDbAvailable()) return [];
    try {
      const result = await query<{
        id: string; user_id: string; type: string; amount: string;
        status: string; source_id: string; source_type: string;
        created_at: Date; metadata: any;
      }>(
        `SELECT * FROM svc_referral_milestones_rewards
         WHERE user_id = $1 AND (status = $2 OR status = $3)`,
        [userId, RewardStatus.CLAIMABLE, RewardStatus.PENDING]
      );
      return result.rows.map(row => ({
        id: row.id,
        userId: row.user_id,
        type: row.type as RewardType,
        amount: BigInt(row.amount),
        status: row.status as RewardStatus,
        sourceId: row.source_id,
        sourceType: row.source_type as Reward['sourceType'],
        createdAt: row.created_at,
        claimedAt: (row as any).claimed_at || undefined,
        transactionHash: (row as any).transaction_hash || undefined,
        metadata: typeof row.metadata === 'string' ? JSON.parse(row.metadata) : (row.metadata || {}),
      }));
    } catch (err: any) {
      // Table may not exist yet — fall back gracefully
      logger.error('DB read pending rewards failed', { userId, error: err?.message });
      return [];
    }
  }

  // ==========================================================================
  // DATABASE WRITE HELPERS
  // ==========================================================================

  private async dbSaveMilestoneProgress(userId: string, progress: UserMilestoneProgress): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_referral_milestones (user_id, milestones_completed, total_referrals, total_rewards_earned, current_tier, updated_at)
         VALUES ($1,$2,$3,$4,$5,NOW())
         ON CONFLICT (user_id) DO UPDATE SET milestones_completed = EXCLUDED.milestones_completed,
           total_referrals = EXCLUDED.total_referrals, total_rewards_earned = EXCLUDED.total_rewards_earned,
           current_tier = EXCLUDED.current_tier, updated_at = NOW()`,
        [userId, JSON.stringify(progress.milestonesAchieved || []), progress.qualifiedReferrals || 0,
         progress.totalMilestoneRewards?.toString() || '0', progress.currentTier || null]
      );
    } catch (err: any) { logger.error('DB save milestone failed', { error: err?.message }); }
  }

  private async dbSavePendingReward(reward: Reward): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_referral_milestones_rewards (id, user_id, type, amount, status, source_id, source_type, created_at, metadata)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
         ON CONFLICT (id) DO NOTHING`,
        [reward.id, reward.userId, reward.type, reward.amount.toString(), reward.status,
         reward.sourceId, reward.sourceType, reward.createdAt, JSON.stringify(reward.metadata || {})]
      );
    } catch (err: any) {
      logger.error('DB save pending reward failed', { rewardId: reward.id, error: err?.message });
    }
  }

  // ==========================================================================
  // ROW-TO-OBJECT HELPER
  // ==========================================================================

  private rowToProgress(r: {
    user_id: string; milestones_completed: string; total_referrals: number;
    total_rewards_earned: string; current_tier: string | null;
  }): UserMilestoneProgress {
    const achieved: AchievedMilestone[] = typeof r.milestones_completed === 'string'
      ? JSON.parse(r.milestones_completed) : (r.milestones_completed || []);
    const progress: UserMilestoneProgress = {
      userId: r.user_id,
      currentTier: (r.current_tier as MilestoneTier) || null,
      qualifiedReferrals: r.total_referrals || 0,
      milestonesAchieved: achieved,
      totalMilestoneRewards: BigInt(r.total_rewards_earned || '0'),
      nextMilestone: undefined,
      progressToNext: 0,
    };
    this.updateProgressToNext(progress);
    return progress;
  }

  // ==========================================================================
  // STARTUP VERIFICATION
  // ==========================================================================

  /**
   * Verify the database is reachable and the milestones table exists.
   * Replaces the old loadFromDb() — no data is cached in memory.
   */
  async verifyDbReady(): Promise<void> {
    if (!isDbAvailable()) {
      logger.warn('DB not available — milestone service running in degraded mode');
      return;
    }
    try {
      const result = await query('SELECT COUNT(*) AS cnt FROM svc_referral_milestones');
      logger.info('Milestone DB verified', { rows: result.rows[0]?.cnt });
    } catch (err: any) {
      logger.warn('Milestone table verification failed — table may need migration', { error: err?.message });
    }
  }

  /**
   * Get all milestone definitions
   */
  getAllMilestones(): Milestone[] {
    return MILESTONES;
  }

  /**
   * Get milestone by tier
   */
  getMilestoneByTier(tier: MilestoneTier): Milestone | undefined {
    return MILESTONES.find(m => m.tier === tier);
  }

  /**
   * Get user's milestone progress
   */
  async getUserProgress(userId: string): Promise<UserMilestoneProgress> {
    // Try to read from DB first
    const dbProgress = await this.dbGetUserProgress(userId);
    if (dbProgress) return dbProgress;

    // No row yet — return a fresh default (not persisted until an action occurs)
    const fresh: UserMilestoneProgress = {
      userId,
      currentTier: null,
      qualifiedReferrals: 0,
      nextMilestone: MILESTONES[0],
      progressToNext: 0,
      milestonesAchieved: [],
      totalMilestoneRewards: BigInt(0),
    };
    return fresh;
  }

  /**
   * Check and award milestones based on referral count
   */
  async checkAndAwardMilestones(
    userId: string,
    qualifiedReferrals: number
  ): Promise<{ newMilestones: Milestone[]; rewards: Reward[] }> {
    const progress = await this.getUserProgress(userId);
    progress.qualifiedReferrals = qualifiedReferrals;

    const newMilestones: Milestone[] = [];
    const newRewards: Reward[] = [];

    // Check each milestone
    for (const milestone of MILESTONES) {
      // Skip already achieved milestones
      const alreadyAchieved = progress.milestonesAchieved.some(
        m => m.tier === milestone.tier
      );
      if (alreadyAchieved) continue;

      // Check if milestone is achieved
      if (qualifiedReferrals >= milestone.requiredReferrals) {
        // Award milestone
        const achieved: AchievedMilestone = {
          milestoneId: milestone.id,
          tier: milestone.tier,
          achievedAt: new Date(),
          rewardAmount: milestone.rewardAmount,
        };
        progress.milestonesAchieved.push(achieved);
        progress.currentTier = milestone.tier;
        progress.totalMilestoneRewards += milestone.rewardAmount;

        newMilestones.push(milestone);

        // Create reward
        const reward: Reward = {
          id: uuidv4(),
          userId,
          type: RewardType.MILESTONE_REWARD,
          amount: milestone.rewardAmount,
          status: RewardStatus.CLAIMABLE,
          sourceId: milestone.id,
          sourceType: 'MILESTONE',
          createdAt: new Date(),
          metadata: {
            milestoneId: milestone.id,
            tier: milestone.tier,
            badge: milestone.badge,
          },
        };
        newRewards.push(reward);

        logger.info('Milestone achieved', {
          userId,
          milestone: milestone.name,
          tier: milestone.tier,
          reward: milestone.rewardAmount.toString(),
        });
      }
    }

    // Update progress to next milestone
    this.updateProgressToNext(progress);

    // Persist pending rewards to DB
    for (const reward of newRewards) {
      await this.dbSavePendingReward(reward);
    }

    // Persist progress to database
    await this.dbSaveMilestoneProgress(userId, progress);

    return { newMilestones, rewards: newRewards };
  }

  /**
   * Calculate progress to next milestone
   */
  private updateProgressToNext(progress: UserMilestoneProgress): void {
    // Find next unachieved milestone
    const achievedTiers = new Set(progress.milestonesAchieved.map(m => m.tier));
    const nextMilestone = MILESTONES.find(m => !achievedTiers.has(m.tier));

    if (nextMilestone) {
      progress.nextMilestone = nextMilestone;

      // Calculate progress percentage
      const prevMilestone = MILESTONES.find(
        m => m.requiredReferrals < nextMilestone.requiredReferrals &&
             !achievedTiers.has(m.tier)
      );
      const baseReferrals = prevMilestone ? prevMilestone.requiredReferrals : 0;
      const range = nextMilestone.requiredReferrals - baseReferrals;
      const current = progress.qualifiedReferrals - baseReferrals;

      progress.progressToNext = Math.min(100, Math.max(0, (current / range) * 100));
    } else {
      progress.nextMilestone = undefined;
      progress.progressToNext = 100;
    }
  }

  /**
   * Get pending rewards for user
   */
  async getPendingRewards(userId: string): Promise<Reward[]> {
    return this.dbGetPendingRewards(userId);
  }

  /**
   * Get ongoing bonus percentage for user (Ambassador status)
   */
  async getOngoingBonusPercentage(userId: string): Promise<number> {
    const progress = await this.getUserProgress(userId);
    const ambassadorMilestone = this.getMilestoneByTier(MilestoneTier.AMBASSADOR);

    if (ambassadorMilestone && progress.currentTier === MilestoneTier.AMBASSADOR) {
      return ambassadorMilestone.ongoingBonus || 0;
    }

    return 0;
  }

  /**
   * Get tier benefits
   */
  getTierBenefits(tier: MilestoneTier): string[] {
    const milestone = this.getMilestoneByTier(tier);
    return milestone?.specialPerks || [];
  }
}

// Export singleton instance
export const milestoneService = new MilestoneService();
