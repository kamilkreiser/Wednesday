/**
 * =============================================================================
 * REFERRAL SERVICE
 * =============================================================================
 * Core referral business logic — DB-only storage (no in-memory Maps)
 */

import { v4 as uuidv4 } from 'uuid';
import {
  ReferralCode,
  ReferralCodeStats,
  Referral,
  ReferralStatus,
  Reward,
  RewardType,
  RewardStatus,
  GenerateCodeRequest,
  ApplyCodeRequest,
  ReferralStatsResponse,
  FraudCheckContext,
} from '../types/referral.types';
import { ReferralCodeGenerator } from './codeGenerator';
import { fraudDetectionService } from './fraudDetection';
import { milestoneService } from './milestoneService';
import { createLogger } from '../utils/logger';
import { query, isDbAvailable } from '../db';

const logger = createLogger('referral-service');

// =============================================================================
// CONFIGURATION
// =============================================================================

const REWARD_CONFIG = {
  // Base rewards (6 decimal places)
  referrerReward: BigInt(50_000_000),   // 50 SECURA per referral
  referredReward: BigInt(25_000_000),   // 25 SECURA signup bonus

  // Qualification requirements
  qualificationPeriodDays: 30, // Days to complete qualifying action
  minCertificationsForQualification: 1, // Min certifications to qualify

  // Limits
  maxActiveCodesPerUser: 5,
  maxReferralsPerCode: 1000,
};

// =============================================================================
// REFERRAL SERVICE
// =============================================================================

export class ReferralService {

  // ==========================================================================
  // DATABASE PERSISTENCE HELPERS (write)
  // ==========================================================================

  private async dbSaveReferralCode(c: ReferralCode): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_referral_codes (id, code, owner_id, owner_wallet_address, is_active, max_uses, current_uses, custom_label, metadata, created_at, expires_at)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
         ON CONFLICT (id) DO UPDATE SET is_active = EXCLUDED.is_active, current_uses = EXCLUDED.current_uses`,
        [c.id, c.code, c.ownerId, c.ownerWalletAddress || null, c.isActive, c.maxUses || null,
         c.currentUses, c.customLabel || null, JSON.stringify(c.metadata || {}), c.createdAt, c.expiresAt || null]
      );
    } catch (err: any) { logger.error('DB save code failed', { error: err?.message }); }
  }

  private async dbSaveReferral(r: Referral): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_referrals (id, referral_code_id, referrer_id, referred_user_id, referred_wallet_address,
           status, referrer_reward, referred_reward, fraud_check_passed, fraud_flags, metadata, created_at, qualified_at, reward_distributed_at)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
         ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status, fraud_check_passed = EXCLUDED.fraud_check_passed,
           fraud_flags = EXCLUDED.fraud_flags, qualified_at = EXCLUDED.qualified_at, reward_distributed_at = EXCLUDED.reward_distributed_at`,
        [r.id, r.referralCodeId, r.referrerId, r.referredUserId, r.referredWalletAddress || null,
         r.status, r.referrerReward?.toString() || '0', r.referredReward?.toString() || '0',
         r.fraudCheckPassed, JSON.stringify(r.fraudFlags || []), JSON.stringify(r.metadata || {}),
         r.createdAt, r.qualifiedAt || null, r.rewardDistributedAt || null]
      );
    } catch (err: any) { logger.error('DB save referral failed', { error: err?.message }); }
  }

  private async dbSaveReward(reward: Reward): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_referral_rewards (id, user_id, type, amount, status, source_id, source_type, transaction_hash, metadata, created_at, claimed_at)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
         ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status, transaction_hash = EXCLUDED.transaction_hash, claimed_at = EXCLUDED.claimed_at`,
        [reward.id, reward.userId, reward.type, reward.amount?.toString() || '0', reward.status,
         reward.sourceId, reward.sourceType, reward.transactionHash || null,
         JSON.stringify(reward.metadata || {}), reward.createdAt, reward.claimedAt || null]
      );
    } catch (err: any) { logger.error('DB save reward failed', { error: err?.message }); }
  }

  // ==========================================================================
  // DATABASE READ HELPERS
  // ==========================================================================

  /** Row-to-ReferralCode conversion */
  private rowToReferralCode(r: any): ReferralCode {
    return {
      id: r.id,
      code: r.code,
      ownerId: r.owner_id,
      ownerWalletAddress: r.owner_wallet_address || undefined,
      isActive: r.is_active,
      maxUses: r.max_uses || undefined,
      currentUses: r.current_uses,
      customLabel: r.custom_label || undefined,
      metadata: typeof r.metadata === 'string' ? JSON.parse(r.metadata) : r.metadata,
      createdAt: new Date(r.created_at),
      expiresAt: r.expires_at ? new Date(r.expires_at) : undefined,
    };
  }

  /** Row-to-Referral conversion */
  private rowToReferral(r: any): Referral {
    return {
      id: r.id,
      referralCodeId: r.referral_code_id,
      referrerId: r.referrer_id,
      referredUserId: r.referred_user_id,
      referredWalletAddress: r.referred_wallet_address || undefined,
      status: r.status as ReferralStatus,
      referrerReward: BigInt(r.referrer_reward || '0'),
      referredReward: BigInt(r.referred_reward || '0'),
      fraudCheckPassed: r.fraud_check_passed,
      fraudFlags: typeof r.fraud_flags === 'string' ? JSON.parse(r.fraud_flags) : r.fraud_flags,
      metadata: typeof r.metadata === 'string' ? JSON.parse(r.metadata) : r.metadata,
      createdAt: new Date(r.created_at),
      qualifiedAt: r.qualified_at ? new Date(r.qualified_at) : undefined,
      rewardDistributedAt: r.reward_distributed_at ? new Date(r.reward_distributed_at) : undefined,
    };
  }

  /** Row-to-Reward conversion */
  private rowToReward(r: any): Reward {
    return {
      id: r.id,
      userId: r.user_id,
      type: r.type as RewardType,
      amount: BigInt(r.amount || '0'),
      status: r.status as RewardStatus,
      sourceId: r.source_id,
      sourceType: r.source_type as 'REFERRAL' | 'MILESTONE' | 'BONUS',
      transactionHash: r.transaction_hash || undefined,
      metadata: typeof r.metadata === 'string' ? JSON.parse(r.metadata) : r.metadata,
      createdAt: new Date(r.created_at),
      claimedAt: r.claimed_at ? new Date(r.claimed_at) : undefined,
    };
  }

  /** Get a single referral code by id */
  private async dbGetReferralCode(id: string): Promise<ReferralCode | null> {
    if (!isDbAvailable()) return null;
    try {
      const result = await query('SELECT * FROM svc_referral_codes WHERE id = $1 LIMIT 1', [id]);
      if (result.rows.length === 0) return null;
      return this.rowToReferralCode(result.rows[0]);
    } catch (err: any) {
      logger.error('DB read referral code failed', { error: err?.message, id });
      return null;
    }
  }

  /** Get all referral codes owned by a user */
  private async dbGetCodesByOwner(ownerId: string): Promise<ReferralCode[]> {
    if (!isDbAvailable()) return [];
    try {
      const result = await query('SELECT * FROM svc_referral_codes WHERE owner_id = $1', [ownerId]);
      return result.rows.map((r: any) => this.rowToReferralCode(r));
    } catch (err: any) {
      logger.error('DB read codes by owner failed', { error: err?.message, ownerId });
      return [];
    }
  }

  /** Get all referrals for a specific referral code */
  private async dbGetReferralsByCode(codeId: string): Promise<Referral[]> {
    if (!isDbAvailable()) return [];
    try {
      const result = await query('SELECT * FROM svc_referrals WHERE referral_code_id = $1', [codeId]);
      return result.rows.map((r: any) => this.rowToReferral(r));
    } catch (err: any) {
      logger.error('DB read referrals by code failed', { error: err?.message, codeId });
      return [];
    }
  }

  /** Get all referrals where referrer_id matches */
  private async dbGetReferralsByReferrer(referrerId: string): Promise<Referral[]> {
    if (!isDbAvailable()) return [];
    try {
      const result = await query('SELECT * FROM svc_referrals WHERE referrer_id = $1', [referrerId]);
      return result.rows.map((r: any) => this.rowToReferral(r));
    } catch (err: any) {
      logger.error('DB read referrals by referrer failed', { error: err?.message, referrerId });
      return [];
    }
  }

  /** Get all rewards for a user */
  private async dbGetRewardsByUser(userId: string): Promise<Reward[]> {
    if (!isDbAvailable()) return [];
    try {
      const result = await query('SELECT * FROM svc_referral_rewards WHERE user_id = $1', [userId]);
      return result.rows.map((r: any) => this.rowToReward(r));
    } catch (err: any) {
      logger.error('DB read rewards by user failed', { error: err?.message, userId });
      return [];
    }
  }

  /** Find a referral code by its code string */
  private async dbGetCodeByString(code: string): Promise<ReferralCode | null> {
    if (!isDbAvailable()) return null;
    try {
      const result = await query('SELECT * FROM svc_referral_codes WHERE code = $1 LIMIT 1', [code]);
      if (result.rows.length === 0) return null;
      return this.rowToReferralCode(result.rows[0]);
    } catch (err: any) {
      logger.error('DB read code by string failed', { error: err?.message, code });
      return null;
    }
  }

  /** Find a referral by referred_user_id */
  private async dbGetReferralByReferredUser(referredUserId: string): Promise<Referral | null> {
    if (!isDbAvailable()) return null;
    try {
      const result = await query('SELECT * FROM svc_referrals WHERE referred_user_id = $1 LIMIT 1', [referredUserId]);
      if (result.rows.length === 0) return null;
      return this.rowToReferral(result.rows[0]);
    } catch (err: any) {
      logger.error('DB read referral by referred user failed', { error: err?.message, referredUserId });
      return null;
    }
  }

  /** Find a pending referral by referred_user_id */
  private async dbGetPendingReferralByUser(referredUserId: string): Promise<Referral | null> {
    if (!isDbAvailable()) return null;
    try {
      const result = await query(
        'SELECT * FROM svc_referrals WHERE referred_user_id = $1 AND status = $2 LIMIT 1',
        [referredUserId, ReferralStatus.PENDING]
      );
      if (result.rows.length === 0) return null;
      return this.rowToReferral(result.rows[0]);
    } catch (err: any) {
      logger.error('DB read pending referral failed', { error: err?.message, referredUserId });
      return null;
    }
  }

  /** Get a single reward by id and user_id */
  private async dbGetReward(rewardId: string, userId: string): Promise<Reward | null> {
    if (!isDbAvailable()) return null;
    try {
      const result = await query(
        'SELECT * FROM svc_referral_rewards WHERE id = $1 AND user_id = $2 LIMIT 1',
        [rewardId, userId]
      );
      if (result.rows.length === 0) return null;
      return this.rowToReward(result.rows[0]);
    } catch (err: any) {
      logger.error('DB read reward failed', { error: err?.message, rewardId });
      return null;
    }
  }

  // ==========================================================================
  // STARTUP — VERIFY DB READY
  // ==========================================================================

  async verifyDbReady(): Promise<void> {
    if (!isDbAvailable()) {
      logger.warn('Database not available — referral service will not function');
      return;
    }
    try {
      const codesResult = await query('SELECT COUNT(*) as count FROM svc_referral_codes');
      const referralsResult = await query('SELECT COUNT(*) as count FROM svc_referrals');
      const rewardsResult = await query('SELECT COUNT(*) as count FROM svc_referral_rewards');

      logger.info('Referral DB tables verified', {
        codes: codesResult.rows[0]?.count ?? 0,
        referrals: referralsResult.rows[0]?.count ?? 0,
        rewards: rewardsResult.rows[0]?.count ?? 0,
      });
    } catch (err: any) {
      logger.error('Failed to verify referral DB tables — service may not function', { error: err?.message });
    }
  }

  // ==========================================================================
  // REFERRAL CODE MANAGEMENT
  // ==========================================================================

  /**
   * Generate a new referral code for a user
   */
  async generateCode(
    userId: string,
    walletAddress?: string,
    options?: GenerateCodeRequest
  ): Promise<ReferralCode> {
    // Check if user has too many active codes
    const userCodes = await this.dbGetCodesByOwner(userId);
    const activeCodes = userCodes.filter(c => c.isActive);

    if (activeCodes.length >= REWARD_CONFIG.maxActiveCodesPerUser) {
      throw new Error(`Maximum ${REWARD_CONFIG.maxActiveCodesPerUser} active codes allowed`);
    }

    // Generate or validate custom code
    let code: string;
    if (options?.customCode) {
      const validation = ReferralCodeGenerator.validateCustomCode(options.customCode);
      if (!validation.valid) {
        throw new Error(`Invalid custom code: ${validation.errors.join(', ')}`);
      }
      code = ReferralCodeGenerator.normaliseCode(options.customCode);

      // Check if code already exists
      const existing = await this.dbGetCodeByString(code);
      if (existing) {
        throw new Error('This code is already in use');
      }
    } else {
      code = ReferralCodeGenerator.generate();
    }

    // Calculate expiration
    let expiresAt: Date | undefined;
    if (options?.expiresInDays) {
      expiresAt = new Date();
      expiresAt.setDate(expiresAt.getDate() + options.expiresInDays);
    }

    // Create referral code
    const referralCode: ReferralCode = {
      id: uuidv4(),
      code,
      ownerId: userId,
      ownerWalletAddress: walletAddress,
      createdAt: new Date(),
      expiresAt,
      isActive: true,
      maxUses: options?.maxUses || REWARD_CONFIG.maxReferralsPerCode,
      currentUses: 0,
      customLabel: options?.customLabel,
    };

    // Store
    await this.dbSaveReferralCode(referralCode);

    logger.info('Referral code generated', {
      userId,
      code,
      codeId: referralCode.id,
    });

    return referralCode;
  }

  /**
   * Get referral code by code string
   */
  async getCodeByString(code: string): Promise<ReferralCode | undefined> {
    const normalised = ReferralCodeGenerator.normaliseCode(code);
    const result = await this.dbGetCodeByString(normalised);
    return result || undefined;
  }

  /**
   * Get referral code by ID
   */
  async getCodeById(id: string): Promise<ReferralCode | undefined> {
    const result = await this.dbGetReferralCode(id);
    return result || undefined;
  }

  /**
   * Get all codes owned by a user
   */
  async getUserCodes(userId: string): Promise<ReferralCode[]> {
    return this.dbGetCodesByOwner(userId);
  }

  /**
   * Deactivate a referral code
   */
  async deactivateCode(codeId: string, userId: string): Promise<boolean> {
    const code = await this.dbGetReferralCode(codeId);
    if (!code) return false;
    if (code.ownerId !== userId) {
      throw new Error('Not authorised to deactivate this code');
    }
    code.isActive = false;
    await this.dbSaveReferralCode(code);
    return true;
  }

  // ==========================================================================
  // REFERRAL APPLICATION
  // ==========================================================================

  /**
   * Apply a referral code (when new user signs up)
   */
  async applyCode(request: ApplyCodeRequest): Promise<Referral> {
    const { code, userId, walletAddress, ipAddress, deviceId, email } = request;

    // Find and validate code
    const referralCode = await this.getCodeByString(code);
    if (!referralCode) {
      throw new Error('Invalid referral code');
    }

    if (!referralCode.isActive) {
      throw new Error('This referral code is no longer active');
    }

    if (referralCode.expiresAt && new Date() > referralCode.expiresAt) {
      throw new Error('This referral code has expired');
    }

    if (referralCode.maxUses && referralCode.currentUses >= referralCode.maxUses) {
      throw new Error('This referral code has reached its maximum uses');
    }

    // Cannot refer yourself
    if (referralCode.ownerId === userId) {
      throw new Error('You cannot use your own referral code');
    }

    // Check if user was already referred
    const existingReferral = await this.dbGetReferralByReferredUser(userId);
    if (existingReferral) {
      throw new Error('You have already been referred');
    }

    // Fraud check
    const fraudContext: FraudCheckContext = {
      referrerId: referralCode.ownerId,
      referredUserId: userId,
      referrerWallet: referralCode.ownerWalletAddress,
      referredWallet: walletAddress,
      referredIp: ipAddress,
      referredDeviceId: deviceId,
      referredEmail: email,
    };

    const fraudCheck = await fraudDetectionService.checkFraud(fraudContext);

    // Create referral
    const referral: Referral = {
      id: uuidv4(),
      referralCodeId: referralCode.id,
      referrerId: referralCode.ownerId,
      referredUserId: userId,
      referredWalletAddress: walletAddress,
      status: fraudCheck.passed ? ReferralStatus.PENDING : ReferralStatus.INVALID,
      createdAt: new Date(),
      referrerReward: REWARD_CONFIG.referrerReward,
      referredReward: REWARD_CONFIG.referredReward,
      fraudCheckPassed: fraudCheck.passed,
      fraudFlags: fraudCheck.flags,
      metadata: {
        fraudRiskScore: fraudCheck.riskScore,
        fraudDetails: fraudCheck.details,
      },
    };

    // Store
    await this.dbSaveReferral(referral);

    // Update code usage
    referralCode.currentUses++;
    await this.dbSaveReferralCode(referralCode);

    // Record for fraud tracking
    if (fraudCheck.passed) {
      fraudDetectionService.recordReferral(fraudContext);
    }

    // If passed fraud check, create signup bonus for referred user
    if (fraudCheck.passed) {
      await this.createReward(userId, {
        type: RewardType.REFERRAL_BONUS,
        amount: REWARD_CONFIG.referredReward,
        sourceId: referral.id,
        sourceType: 'REFERRAL',
        metadata: { reason: 'Signup bonus' },
      });
    }

    logger.info('Referral applied', {
      referralId: referral.id,
      code: referralCode.code,
      referrerId: referralCode.ownerId,
      referredUserId: userId,
      fraudPassed: fraudCheck.passed,
    });

    return referral;
  }

  /**
   * Qualify a referral (when user completes qualifying action)
   */
  async qualifyReferral(referredUserId: string): Promise<Referral | null> {
    // Find pending referral for user
    const referral = await this.dbGetPendingReferralByUser(referredUserId);

    if (!referral) {
      return null;
    }

    // Update status
    referral.status = ReferralStatus.QUALIFIED;
    referral.qualifiedAt = new Date();
    await this.dbSaveReferral(referral);

    // Create reward for referrer
    const ambassadorBonus = await milestoneService.getOngoingBonusPercentage(referral.referrerId);
    let referrerRewardAmount = referral.referrerReward;

    if (ambassadorBonus > 0) {
      const bonus = (referral.referrerReward * BigInt(ambassadorBonus)) / BigInt(100);
      referrerRewardAmount += bonus;
    }

    await this.createReward(referral.referrerId, {
      type: RewardType.REFERRER_REWARD,
      amount: referrerRewardAmount,
      sourceId: referral.id,
      sourceType: 'REFERRAL',
      metadata: {
        referredUserId,
        ambassadorBonus: ambassadorBonus > 0 ? ambassadorBonus : undefined,
      },
    });

    // Check milestones
    const referrerReferrals = await this.getReferralsByReferrer(referral.referrerId);
    const qualifiedCount = referrerReferrals.filter(
      r => r.status === ReferralStatus.QUALIFIED || r.status === ReferralStatus.REWARDED
    ).length;

    await milestoneService.checkAndAwardMilestones(referral.referrerId, qualifiedCount);

    logger.info('Referral qualified', {
      referralId: referral.id,
      referrerId: referral.referrerId,
      referredUserId,
      qualifiedCount,
    });

    return referral;
  }

  // ==========================================================================
  // STATISTICS
  // ==========================================================================

  /**
   * Get statistics for a referral code
   */
  async getCodeStats(codeId: string): Promise<ReferralCodeStats | null> {
    const code = await this.dbGetReferralCode(codeId);
    if (!code) return null;

    const referrals = await this.dbGetReferralsByCode(codeId);

    const qualified = referrals.filter(
      r => r.status === ReferralStatus.QUALIFIED || r.status === ReferralStatus.REWARDED
    );

    const totalRewards = qualified.reduce(
      (sum, r) => sum + r.referrerReward,
      BigInt(0)
    );

    const pendingReferrals = referrals.filter(r => r.status === ReferralStatus.PENDING);
    const pendingRewards = pendingReferrals.reduce(
      (sum, r) => sum + r.referrerReward,
      BigInt(0)
    );

    const lastReferral = referrals.sort(
      (a, b) => b.createdAt.getTime() - a.createdAt.getTime()
    )[0];

    return {
      code: code.code,
      totalReferrals: referrals.length,
      activeReferrals: qualified.length,
      totalRewardsEarned: totalRewards,
      pendingRewards,
      conversionRate: referrals.length > 0
        ? (qualified.length / referrals.length) * 100
        : 0,
      lastUsedAt: lastReferral?.createdAt,
    };
  }

  /**
   * Get full referral stats for a user
   */
  async getUserStats(userId: string): Promise<ReferralStatsResponse | null> {
    const codes = await this.getUserCodes(userId);
    const primaryCode = codes.find(c => c.isActive) || codes[0];

    if (!primaryCode) {
      return null;
    }

    const stats = await this.getCodeStats(primaryCode.id);
    if (!stats) return null;

    const progress = await milestoneService.getUserProgress(userId);
    const pendingRewards = await this.getUserPendingRewards(userId);

    const userRewards = await this.dbGetRewardsByUser(userId);
    const totalRewardsEarned = userRewards
      .filter(r => r.status === RewardStatus.CLAIMED || r.status === RewardStatus.DISTRIBUTED)
      .reduce((sum, r) => sum + r.amount, BigInt(0));

    return {
      userId,
      referralCode: primaryCode,
      stats,
      milestoneProgress: progress,
      pendingRewards,
      totalRewardsEarned,
    };
  }

  /**
   * Get referrals for a referrer
   */
  async getReferralsByReferrer(referrerId: string): Promise<Referral[]> {
    return this.dbGetReferralsByReferrer(referrerId);
  }

  /**
   * Get referred users by a referrer
   */
  async getReferredUsers(referrerId: string): Promise<{ userId: string; status: ReferralStatus; joinedAt: Date }[]> {
    const referrals = await this.getReferralsByReferrer(referrerId);
    return referrals.map(r => ({
      userId: r.referredUserId,
      status: r.status,
      joinedAt: r.createdAt,
    }));
  }

  // ==========================================================================
  // REWARDS
  // ==========================================================================

  /**
   * Create a reward for a user
   */
  private async createReward(userId: string, params: {
    type: RewardType;
    amount: bigint;
    sourceId: string;
    sourceType: 'REFERRAL' | 'MILESTONE' | 'BONUS';
    metadata?: Record<string, any>;
  }): Promise<Reward> {
    const reward: Reward = {
      id: uuidv4(),
      userId,
      type: params.type,
      amount: params.amount,
      status: RewardStatus.CLAIMABLE,
      sourceId: params.sourceId,
      sourceType: params.sourceType,
      createdAt: new Date(),
      metadata: params.metadata,
    };

    await this.dbSaveReward(reward);

    logger.info('Reward created', {
      userId,
      rewardId: reward.id,
      type: params.type,
      amount: params.amount.toString(),
    });

    return reward;
  }

  /**
   * Get all rewards for a user
   */
  async getUserRewards(userId: string): Promise<Reward[]> {
    return this.dbGetRewardsByUser(userId);
  }

  /**
   * Get pending (claimable) rewards for a user
   */
  async getUserPendingRewards(userId: string): Promise<Reward[]> {
    const milestoneRewards = await milestoneService.getPendingRewards(userId);
    const allRewards = await this.dbGetRewardsByUser(userId);
    const referralRewards = allRewards.filter(
      r => r.status === RewardStatus.CLAIMABLE || r.status === RewardStatus.PENDING
    );
    return [...milestoneRewards, ...referralRewards];
  }

  /**
   * Claim rewards
   */
  async claimRewards(
    userId: string,
    rewardIds: string[],
    walletAddress: string
  ): Promise<{ claimed: Reward[]; failed: string[] }> {
    const claimed: Reward[] = [];
    const failed: string[] = [];

    for (const rewardId of rewardIds) {
      const reward = await this.dbGetReward(rewardId, userId);

      if (!reward) {
        failed.push(rewardId);
        continue;
      }

      if (reward.status !== RewardStatus.CLAIMABLE) {
        failed.push(rewardId);
        continue;
      }

      // Mark as claimed (in production, initiate blockchain transfer)
      reward.status = RewardStatus.CLAIMED;
      reward.claimedAt = new Date();
      reward.metadata = {
        ...reward.metadata,
        claimedToWallet: walletAddress,
      };

      await this.dbSaveReward(reward);
      claimed.push(reward);

      logger.info('Reward claimed', {
        userId,
        rewardId,
        amount: reward.amount.toString(),
        walletAddress,
      });
    }

    return { claimed, failed };
  }
}

// Export singleton instance
export const referralService = new ReferralService();
