/**
 * =============================================================================
 * REFERRAL TYPES
 * =============================================================================
 */

// =============================================================================
// REFERRAL CODE
// =============================================================================

export interface ReferralCode {
  id: string;
  code: string;
  ownerId: string;
  ownerWalletAddress?: string;
  createdAt: Date;
  expiresAt?: Date;
  isActive: boolean;
  maxUses?: number;
  currentUses: number;
  customLabel?: string;
  metadata?: Record<string, any>;
}

export interface ReferralCodeStats {
  code: string;
  totalReferrals: number;
  activeReferrals: number;
  totalRewardsEarned: bigint;
  pendingRewards: bigint;
  conversionRate: number;
  lastUsedAt?: Date;
}

// =============================================================================
// REFERRAL
// =============================================================================

export interface Referral {
  id: string;
  referralCodeId: string;
  referrerId: string;
  referredUserId: string;
  referredWalletAddress?: string;
  status: ReferralStatus;
  createdAt: Date;
  qualifiedAt?: Date;
  rewardDistributedAt?: Date;
  referrerReward: bigint;
  referredReward: bigint;
  fraudCheckPassed: boolean;
  fraudFlags: string[];
  metadata?: Record<string, any>;
}

export enum ReferralStatus {
  PENDING = 'PENDING',           // User signed up but not yet qualified
  QUALIFIED = 'QUALIFIED',       // User completed qualifying action
  REWARDED = 'REWARDED',         // Rewards distributed
  INVALID = 'INVALID',           // Failed fraud checks
  EXPIRED = 'EXPIRED',           // Qualification period expired
}

// =============================================================================
// MILESTONES
// =============================================================================

export interface Milestone {
  id: string;
  name: string;
  description: string;
  tier: MilestoneTier;
  requiredReferrals: number;
  rewardAmount: bigint;
  badge?: string;
  specialPerks?: string[];
  ongoingBonus?: number; // Percentage bonus for future referrals
}

export enum MilestoneTier {
  FIRST_REFERRAL = 'FIRST_REFERRAL',
  BRONZE = 'BRONZE',
  SILVER = 'SILVER',
  GOLD = 'GOLD',
  PLATINUM = 'PLATINUM',
  AMBASSADOR = 'AMBASSADOR',
}

export interface UserMilestoneProgress {
  userId: string;
  currentTier: MilestoneTier | null;
  qualifiedReferrals: number;
  nextMilestone?: Milestone;
  progressToNext: number; // Percentage progress
  milestonesAchieved: AchievedMilestone[];
  totalMilestoneRewards: bigint;
}

export interface AchievedMilestone {
  milestoneId: string;
  tier: MilestoneTier;
  achievedAt: Date;
  rewardAmount: bigint;
  claimedAt?: Date;
}

// =============================================================================
// REWARDS
// =============================================================================

export interface Reward {
  id: string;
  userId: string;
  type: RewardType;
  amount: bigint;
  status: RewardStatus;
  sourceId: string; // referralId or milestoneId
  sourceType: 'REFERRAL' | 'MILESTONE' | 'BONUS';
  createdAt: Date;
  claimedAt?: Date;
  transactionHash?: string;
  metadata?: Record<string, any>;
}

export enum RewardType {
  REFERRAL_BONUS = 'REFERRAL_BONUS',
  REFERRER_REWARD = 'REFERRER_REWARD',
  MILESTONE_REWARD = 'MILESTONE_REWARD',
  AMBASSADOR_BONUS = 'AMBASSADOR_BONUS',
  LEADERBOARD_PRIZE = 'LEADERBOARD_PRIZE',
}

export enum RewardStatus {
  PENDING = 'PENDING',
  CLAIMABLE = 'CLAIMABLE',
  CLAIMED = 'CLAIMED',
  DISTRIBUTED = 'DISTRIBUTED',
  FAILED = 'FAILED',
  CANCELLED = 'CANCELLED',
}

// =============================================================================
// LEADERBOARD
// =============================================================================

export interface LeaderboardEntry {
  rank: number;
  userId: string;
  displayName?: string;
  walletAddress?: string;
  totalReferrals: number;
  qualifiedReferrals: number;
  totalRewardsEarned: bigint;
  currentTier: MilestoneTier | null;
  badge?: string;
}

export interface LeaderboardPeriod {
  type: 'ALL_TIME' | 'MONTHLY' | 'WEEKLY';
  startDate?: Date;
  endDate?: Date;
}

// =============================================================================
// FRAUD DETECTION
// =============================================================================

export interface FraudCheckResult {
  passed: boolean;
  flags: FraudFlag[];
  riskScore: number;
  details: Record<string, any>;
}

export enum FraudFlag {
  IP_COLLISION = 'IP_COLLISION',           // Same IP as referrer
  DEVICE_COLLISION = 'DEVICE_COLLISION',   // Same device fingerprint
  WALLET_COLLISION = 'WALLET_COLLISION',   // Wallet linked to referrer
  RAPID_SIGNUP = 'RAPID_SIGNUP',           // Suspiciously fast signup
  SYBIL_PATTERN = 'SYBIL_PATTERN',         // Multiple accounts pattern
  KNOWN_FRAUD = 'KNOWN_FRAUD',             // Previously flagged
  DISPOSABLE_EMAIL = 'DISPOSABLE_EMAIL',   // Disposable email service
  VPN_DETECTED = 'VPN_DETECTED',           // VPN/proxy detected
  BOT_BEHAVIOR = 'BOT_BEHAVIOR',           // Automated behavior detected
}

export interface FraudCheckContext {
  referrerId: string;
  referredUserId: string;
  referrerIp?: string;
  referredIp?: string;
  referrerDeviceId?: string;
  referredDeviceId?: string;
  referrerWallet?: string;
  referredWallet?: string;
  referrerEmail?: string;
  referredEmail?: string;
  signupDuration?: number; // Seconds from code click to signup
}

// =============================================================================
// API REQUEST/RESPONSE TYPES
// =============================================================================

export interface GenerateCodeRequest {
  customCode?: string;
  maxUses?: number;
  expiresInDays?: number;
  customLabel?: string;
}

export interface ApplyCodeRequest {
  code: string;
  userId: string;
  walletAddress?: string;
  ipAddress?: string;
  deviceId?: string;
  email?: string;
}

export interface ClaimRewardsRequest {
  userId: string;
  rewardIds: string[];
  walletAddress: string;
}

export interface ReferralStatsResponse {
  userId: string;
  referralCode: ReferralCode;
  stats: ReferralCodeStats;
  milestoneProgress: UserMilestoneProgress;
  pendingRewards: Reward[];
  totalRewardsEarned: bigint;
}
