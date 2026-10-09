/**
 * =============================================================================
 * FRAUD DETECTION SERVICE
 * =============================================================================
 * Anti-fraud measures for referral system
 */

import { 
  FraudCheckResult, 
  FraudFlag, 
  FraudCheckContext 
} from '../types/referral.types';
import { createLogger } from '../utils/logger';
import { query, isDbAvailable } from '../db';

const logger = createLogger('fraud-detection');

// =============================================================================
// CONFIGURATION
// =============================================================================

const FRAUD_CONFIG = {
  // Risk score thresholds
  thresholds: {
    pass: 30,      // Below this = pass
    review: 70,    // Above this = manual review
    block: 100,    // Above this = auto block
  },
  
  // Individual flag weights
  flagWeights: {
    [FraudFlag.IP_COLLISION]: 40,
    [FraudFlag.DEVICE_COLLISION]: 50,
    [FraudFlag.WALLET_COLLISION]: 80,
    [FraudFlag.RAPID_SIGNUP]: 20,
    [FraudFlag.SYBIL_PATTERN]: 60,
    [FraudFlag.KNOWN_FRAUD]: 100,
    [FraudFlag.DISPOSABLE_EMAIL]: 15,
    [FraudFlag.VPN_DETECTED]: 10,
    [FraudFlag.BOT_BEHAVIOR]: 70,
  },
  
  // Time-based checks
  minSignupDuration: 30, // Minimum seconds for legitimate signup
  
  // Pattern detection
  maxReferralsPerIp: 3,
  maxReferralsPerDevice: 2,
};

// Disposable email domains (simplified list - use a service in production)
const DISPOSABLE_EMAIL_DOMAINS = new Set([
  'tempmail.com', 'throwaway.email', '10minutemail.com',
  'guerrillamail.com', 'mailinator.com', 'dispostable.com',
  'tempail.com', 'fakeinbox.com', 'sharklasers.com',
  'trashmail.com', 'mailnesia.com', 'temp-mail.org',
]);

// =============================================================================
// FRAUD DETECTION SERVICE
// =============================================================================

export class FraudDetectionService {
  // In-memory caches (ephemeral - use Redis in production)
  private memIpReferralCounts: Map<string, { count: number; referrerIds: Set<string> }> = new Map();
  private memDeviceReferralCounts: Map<string, { count: number; referrerIds: Set<string> }> = new Map();
  private memKnownFraudUsers: Set<string> = new Set();
  private memWalletToUserMap: Map<string, string> = new Map();

  // ==========================================================================
  // DATABASE FRAUD LOGGING
  // ==========================================================================

  private async dbLogFraud(ip: string, device: string, referrerId: string, flagType: string, details: object): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_referral_fraud_log (ip_address, device_fingerprint, referrer_id, flag_type, details) VALUES ($1,$2,$3,$4,$5)`,
        [ip || null, device || null, referrerId || null, flagType, JSON.stringify(details)]
      );
    } catch { /* ignore */ }
  }

  // ==========================================================================
  // STARTUP LOADING
  // ==========================================================================

  async loadFromDb(): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      const rows = await query<{
        ip_address: string | null; device_fingerprint: string | null;
        referrer_id: string; flag_type: string;
      }>('SELECT ip_address, device_fingerprint, referrer_id, flag_type FROM svc_referral_fraud_log');
      for (const r of rows.rows) {
        if (r.ip_address) {
          const ipData = this.memIpReferralCounts.get(r.ip_address) || { count: 0, referrerIds: new Set<string>() };
          ipData.count++;
          if (r.referrer_id) ipData.referrerIds.add(r.referrer_id);
          this.memIpReferralCounts.set(r.ip_address, ipData);
        }
        if (r.device_fingerprint) {
          const devData = this.memDeviceReferralCounts.get(r.device_fingerprint) || { count: 0, referrerIds: new Set<string>() };
          devData.count++;
          if (r.referrer_id) devData.referrerIds.add(r.referrer_id);
          this.memDeviceReferralCounts.set(r.device_fingerprint, devData);
        }
        if (r.flag_type === 'KNOWN_FRAUD' && r.referrer_id) {
          this.memKnownFraudUsers.add(r.referrer_id);
        }
      }
      logger.info('Loaded fraud data from DB', { ips: this.memIpReferralCounts.size, devices: this.memDeviceReferralCounts.size, flaggedUsers: this.memKnownFraudUsers.size });
    } catch (err: any) {
      logger.warn('Failed to load fraud data from DB — starting empty', { error: err?.message });
    }
  }

  /**
   * Perform comprehensive fraud check
   */
  async checkFraud(context: FraudCheckContext): Promise<FraudCheckResult> {
    const flags: FraudFlag[] = [];
    const details: Record<string, any> = {};

    logger.info('Starting fraud check', {
      referrerId: context.referrerId,
      referredUserId: context.referredUserId,
    });

    // 1. Known fraud check
    if (this.memKnownFraudUsers.has(context.referredUserId)) {
      flags.push(FraudFlag.KNOWN_FRAUD);
      details.knownFraud = 'User previously flagged for fraud';
    }

    // 2. IP collision check
    if (context.referrerIp && context.referredIp) {
      if (context.referrerIp === context.referredIp) {
        flags.push(FraudFlag.IP_COLLISION);
        details.ipCollision = 'Same IP address as referrer';
      } else {
        // Check IP patterns
        const ipData = this.memIpReferralCounts.get(context.referredIp);
        if (ipData && ipData.count >= FRAUD_CONFIG.maxReferralsPerIp) {
          flags.push(FraudFlag.SYBIL_PATTERN);
          details.ipPattern = `IP has ${ipData.count} previous referrals`;
        }
      }
    }

    // 3. Device collision check
    if (context.referrerDeviceId && context.referredDeviceId) {
      if (context.referrerDeviceId === context.referredDeviceId) {
        flags.push(FraudFlag.DEVICE_COLLISION);
        details.deviceCollision = 'Same device fingerprint as referrer';
      } else {
        const deviceData = this.memDeviceReferralCounts.get(context.referredDeviceId);
        if (deviceData && deviceData.count >= FRAUD_CONFIG.maxReferralsPerDevice) {
          flags.push(FraudFlag.SYBIL_PATTERN);
          details.devicePattern = `Device has ${deviceData.count} previous referrals`;
        }
      }
    }

    // 4. Wallet collision check
    if (context.referrerWallet && context.referredWallet) {
      if (context.referrerWallet === context.referredWallet) {
        flags.push(FraudFlag.WALLET_COLLISION);
        details.walletCollision = 'Same wallet as referrer';
      } else {
        // Check if wallet is linked to referrer
        const linkedUser = this.memWalletToUserMap.get(context.referredWallet);
        if (linkedUser === context.referrerId) {
          flags.push(FraudFlag.WALLET_COLLISION);
          details.walletLinked = 'Wallet previously linked to referrer';
        }
      }
    }

    // 5. Rapid signup check
    if (context.signupDuration !== undefined) {
      if (context.signupDuration < FRAUD_CONFIG.minSignupDuration) {
        flags.push(FraudFlag.RAPID_SIGNUP);
        details.rapidSignup = `Signup completed in ${context.signupDuration}s (min: ${FRAUD_CONFIG.minSignupDuration}s)`;
      }
    }

    // 6. Disposable email check
    if (context.referredEmail) {
      const domain = context.referredEmail.split('@')[1]?.toLowerCase();
      if (domain && DISPOSABLE_EMAIL_DOMAINS.has(domain)) {
        flags.push(FraudFlag.DISPOSABLE_EMAIL);
        details.disposableEmail = `Disposable email domain: ${domain}`;
      }
    }

    // Calculate risk score
    const riskScore = this.calculateRiskScore(flags);

    // Determine pass/fail
    const passed = riskScore < FRAUD_CONFIG.thresholds.pass;

    const result: FraudCheckResult = {
      passed,
      flags,
      riskScore,
      details,
    };

    // Log fraud detection to database if flags found
    if (flags.length > 0) {
      await this.dbLogFraud(
        context.referredIp || '',
        context.referredDeviceId || '',
        context.referrerId,
        flags[0], // Log primary flag
        details
      );
    }

    logger.info('Fraud check completed', {
      referrerId: context.referrerId,
      referredUserId: context.referredUserId,
      passed,
      riskScore,
      flagCount: flags.length,
    });

    return result;
  }

  /**
   * Calculate risk score from flags
   */
  private calculateRiskScore(flags: FraudFlag[]): number {
    let score = 0;
    for (const flag of flags) {
      score += FRAUD_CONFIG.flagWeights[flag] || 0;
    }
    return Math.min(score, 100);
  }

  /**
   * Record a successful referral for pattern tracking
   */
  recordReferral(context: FraudCheckContext): void {
    // Track IP
    if (context.referredIp) {
      const ipData = this.memIpReferralCounts.get(context.referredIp) || { count: 0, referrerIds: new Set() };
      ipData.count++;
      ipData.referrerIds.add(context.referrerId);
      this.memIpReferralCounts.set(context.referredIp, ipData);
    }

    // Track device
    if (context.referredDeviceId) {
      const deviceData = this.memDeviceReferralCounts.get(context.referredDeviceId) || { count: 0, referrerIds: new Set() };
      deviceData.count++;
      deviceData.referrerIds.add(context.referrerId);
      this.memDeviceReferralCounts.set(context.referredDeviceId, deviceData);
    }

    // Track wallet
    if (context.referredWallet) {
      this.memWalletToUserMap.set(context.referredWallet, context.referredUserId);
    }
  }

  /**
   * Flag a user as fraudulent
   */
  flagAsFraud(userId: string, reason: string): void {
    this.memKnownFraudUsers.add(userId);
    logger.warn('User flagged as fraud', { userId, reason });
  }

  /**
   * Clear fraud flag (after manual review)
   */
  clearFraudFlag(userId: string): void {
    this.memKnownFraudUsers.delete(userId);
    logger.info('Fraud flag cleared', { userId });
  }

  /**
   * Get fraud statistics
   */
  getStats(): {
    totalFlaggedUsers: number;
    trackedIps: number;
    trackedDevices: number;
  } {
    return {
      totalFlaggedUsers: this.memKnownFraudUsers.size,
      trackedIps: this.memIpReferralCounts.size,
      trackedDevices: this.memDeviceReferralCounts.size,
    };
  }
}

// Export singleton instance
export const fraudDetectionService = new FraudDetectionService();
