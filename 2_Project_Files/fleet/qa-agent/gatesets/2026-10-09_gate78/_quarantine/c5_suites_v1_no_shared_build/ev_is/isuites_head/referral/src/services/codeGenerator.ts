/**
 * =============================================================================
 * REFERRAL CODE GENERATOR
 * =============================================================================
 * Generates unique, memorable referral codes
 */

import { customAlphabet } from 'nanoid';
import { createLogger } from '../utils/logger';

const logger = createLogger('code-generator');

// Alphabet without ambiguous characters (no 0, O, l, 1, I)
const SAFE_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';

// Generate 8-character codes by default
const generateCode = customAlphabet(SAFE_ALPHABET, 8);

// Reserved words that cannot be used as codes
const RESERVED_WORDS = new Set([
  'SECUURA', 'ADMIN', 'TEST', 'DEMO', 'HELP',
  'SUPPORT', 'OFFICIAL', 'TEAM', 'FREE', 'PROMO',
  'BONUS', 'VIP', 'PREMIUM', 'GOLD', 'SILVER',
  'PLATINUM', 'AMBASSADOR', 'PARTNER', 'STAFF',
]);

// Profanity filter (simplified - in production use a proper library)
const BLOCKED_PATTERNS = [
  /fuck/i, /shit/i, /ass(?!et)/i, /damn/i, /hell/i,
  /bitch/i, /cunt/i, /dick/i, /cock/i, /pussy/i,
];

export class ReferralCodeGenerator {
  /**
   * Generate a unique referral code
   */
  static generate(): string {
    let code: string;
    let attempts = 0;
    const maxAttempts = 10;

    do {
      code = generateCode();
      attempts++;
    } while (
      attempts < maxAttempts && 
      (this.isReserved(code) || this.containsBlockedPattern(code))
    );

    if (attempts >= maxAttempts) {
      logger.warn('Code generation required multiple attempts', { attempts });
    }

    return code;
  }

  /**
   * Validate a custom referral code
   */
  static validateCustomCode(code: string): { valid: boolean; errors: string[] } {
    const errors: string[] = [];
    const normalizedCode = code.toUpperCase().trim();

    // Length check
    if (normalizedCode.length < 4) {
      errors.push('Code must be at least 4 characters');
    }
    if (normalizedCode.length > 16) {
      errors.push('Code must be 16 characters or less');
    }

    // Character check
    const validChars = /^[A-Z0-9]+$/;
    if (!validChars.test(normalizedCode)) {
      errors.push('Code can only contain letters and numbers');
    }

    // Reserved word check
    if (this.isReserved(normalizedCode)) {
      errors.push('This code is reserved and cannot be used');
    }

    // Profanity check
    if (this.containsBlockedPattern(normalizedCode)) {
      errors.push('Code contains inappropriate content');
    }

    // Sequential/repetitive pattern check
    if (this.hasSequentialPattern(normalizedCode)) {
      errors.push('Code contains sequential or repetitive patterns');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Normalise a code for storage and lookup
   */
  static normaliseCode(code: string): string {
    return code.toUpperCase().trim().replace(/[^A-Z0-9]/g, '');
  }

  /**
   * Check if code is reserved
   */
  private static isReserved(code: string): boolean {
    return RESERVED_WORDS.has(code.toUpperCase());
  }

  /**
   * Check for blocked patterns (profanity, etc.)
   */
  private static containsBlockedPattern(code: string): boolean {
    return BLOCKED_PATTERNS.some(pattern => pattern.test(code));
  }

  /**
   * Check for sequential/repetitive patterns like AAAA, 1234, ABCD
   */
  private static hasSequentialPattern(code: string): boolean {
    // Check for repetitive characters (3+ in a row)
    if (/(.)\1{2,}/.test(code)) {
      return true;
    }

    // Check for sequential patterns (ascending or descending)
    for (let i = 0; i < code.length - 2; i++) {
      const c1 = code.charCodeAt(i);
      const c2 = code.charCodeAt(i + 1);
      const c3 = code.charCodeAt(i + 2);

      // Ascending
      if (c2 === c1 + 1 && c3 === c2 + 1) {
        return true;
      }
      // Descending
      if (c2 === c1 - 1 && c3 === c2 - 1) {
        return true;
      }
    }

    return false;
  }

  /**
   * Generate a vanity code (starts with user-specified prefix)
   */
  static generateVanityCode(prefix: string, maxLength: number = 12): string | null {
    const normalizedPrefix = this.normaliseCode(prefix);
    
    // Validate prefix
    const validation = this.validateCustomCode(normalizedPrefix);
    if (!validation.valid) {
      return null;
    }

    const remainingLength = Math.max(4, maxLength - normalizedPrefix.length);
    const suffix = customAlphabet(SAFE_ALPHABET, remainingLength)();
    
    return normalizedPrefix + suffix;
  }
}
