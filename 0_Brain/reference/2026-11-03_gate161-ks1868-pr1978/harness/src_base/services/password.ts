/**
 * Password Service
 * Secure password hashing + verification + breached-password check.
 *
 * Pen-test F-12 fixes:
 *   1. Argon2id alongside bcrypt — new hashes use Argon2id (m=64MB, t=3,
 *      p=4); existing bcrypt hashes still verify, and on the next
 *      successful login the user's hash is upgraded to Argon2id by the
 *      caller (see UPGRADE-ON-VERIFY note below).
 *   2. Minimum length raised to 12 (was 8). Admin roles can require 14
 *      via `checkPasswordStrength(pw, { minLength: 14 })`.
 *   3. HaveIBeenPwned k-anonymity check — `isPasswordBreached(pw)` sends
 *      the SHA-1 prefix (5 chars) and checks suffix matches locally.
 *      Network failure fails OPEN (returns false) so a HIBP outage doesn't
 *      lock everyone out.
 */

import bcrypt from 'bcryptjs';
import crypto from 'crypto';
import { logger } from '../utils/logger';

// Configuration
const SALT_ROUNDS = 12;
const RESET_TOKEN_BYTES = 32;
const RESET_TOKEN_EXPIRY_HOURS = 24;
const MIN_LENGTH_DEFAULT = 12;
const MIN_LENGTH_ADMIN = 14;

// Argon2id parameters — OWASP ASVS L2 baseline. Memory tuned to fit
// inside a small Container App (64 MiB) without OOM risk.
// KS-254: env-tunable so per-instance login capacity (KS-198) can be traded
// against hash hardness as a CONFIG decision — the in-code defaults are
// unchanged and remain the security baseline. Floors guard against a typo'd
// env value silently weakening hashing below OWASP's argon2id minimum
// (m=19 MiB, t=2, p=1).
function argon2Param(name: string, fallback: number, floor: number): number {
  const parsed = parseInt(process.env[name] ?? '', 10);
  if (!Number.isFinite(parsed) || parsed <= 0) return fallback;
  if (parsed < floor) {
    logger.warn(`${name} below the OWASP argon2id floor — using the floor`, {
      requested: parsed,
      floor,
    });
    return floor;
  }
  return parsed;
}
const ARGON2_OPTS = {
  type: 2 as const, // argon2id
  memoryCost: argon2Param('ARGON2_MEMORY_KIB', 1 << 16, 19 * 1024), // default 64 MiB, floor 19 MiB
  timeCost: argon2Param('ARGON2_TIME_COST', 3, 2),
  parallelism: argon2Param('ARGON2_PARALLELISM', 4, 1),
};

let argon2Mod: typeof import('argon2') | null = null;
async function loadArgon2(): Promise<typeof import('argon2') | null> {
  if (argon2Mod) return argon2Mod;
  try {
    argon2Mod = (await import('argon2')) as typeof import('argon2');
    return argon2Mod;
  } catch (err: any) {
    // Argon2 native binding not present — fall back to bcrypt-only.
    // Logged once per process so the operator can install argon2.
    logger.warn('argon2 native binding unavailable — falling back to bcrypt for new hashes', {
      error: err?.message,
    });
    return null;
  }
}

/**
 * Hash a password. Prefers Argon2id; falls back to bcrypt if the
 * argon2 native binding is unavailable.
 */
export async function hashPassword(password: string): Promise<string> {
  const argon2 = await loadArgon2();
  if (argon2) {
    return argon2.hash(password, ARGON2_OPTS);
  }
  return bcrypt.hash(password, SALT_ROUNDS);
}

/**
 * Verify a password. Recognises both Argon2id (`$argon2id$…`) and bcrypt
 * (`$2a$…` / `$2b$…` / `$2y$…`) hashes. Caller should re-hash with
 * `hashPassword` after a successful bcrypt verify to migrate users
 * forward (see services/auth/src/routes/auth.ts login handler — UPGRADE
 * ON VERIFY).
 */
export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  if (hash.startsWith('$argon2')) {
    const argon2 = await loadArgon2();
    if (!argon2) {
      logger.error('argon2 hash present but argon2 binding unavailable — cannot verify');
      return false;
    }
    try {
      return await argon2.verify(hash, password);
    } catch (err: any) {
      logger.warn('argon2 verify failed', { error: err?.message });
      return false;
    }
  }
  // bcrypt fallback
  return bcrypt.compare(password, hash);
}

/**
 * True iff the verified hash should be re-hashed (migration path).
 * Bcrypt hashes get upgraded to Argon2id on next successful verify.
 */
export function shouldRehashAfterVerify(hash: string): boolean {
  return hash.startsWith('$2');
}

/**
 * HaveIBeenPwned k-anonymity check. Returns true if the password is
 * known-breached. Network failures fail OPEN (return false) so an HIBP
 * outage doesn't block authentication.
 *
 * Disable globally with HIBP_ENABLED=false (default: enabled).
 */
export async function isPasswordBreached(password: string): Promise<boolean> {
  if (process.env.HIBP_ENABLED === 'false') return false;
  try {
    const sha1 = crypto.createHash('sha1').update(password).digest('hex').toUpperCase();
    const prefix = sha1.slice(0, 5);
    const suffix = sha1.slice(5);
    const url = `https://api.pwnedpasswords.com/range/${prefix}`;
    const res = await fetch(url, {
      headers: { 'Add-Padding': 'true' },
      signal: AbortSignal.timeout(2_000),
    });
    if (!res.ok) {
      logger.warn('HIBP lookup non-200 — failing open', { status: res.status });
      return false;
    }
    const body = await res.text();
    for (const line of body.split('\n')) {
      const [hashSuffix] = line.trim().split(':');
      if (hashSuffix === suffix) return true;
    }
    return false;
  } catch (err: any) {
    logger.warn('HIBP lookup failed — failing open', { error: err?.message });
    return false;
  }
}

/**
 * Check password strength
 */
export interface PasswordStrength {
  score: number;  // 0-4
  feedback: string[];
  isStrong: boolean;
}

export function checkPasswordStrength(
  password: string,
  options: { minLength?: number } = {},
): PasswordStrength {
  // Pen-test F-12 fix: floor raised from 8 → 12 (default), 14 for admins.
  const minLength = options.minLength ?? MIN_LENGTH_DEFAULT;
  const feedback: string[] = [];
  let score = 0;

  // Length check
  if (password.length >= minLength) score++;
  if (password.length >= minLength + 2) score++;
  if (password.length < minLength) feedback.push(`Password must be at least ${minLength} characters`);
  
  // Character variety — require at least 3 of 4 categories
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasDigit = /[0-9]/.test(password);
  const hasSpecial = /[^a-zA-Z0-9]/.test(password);
  
  if (hasLower) score += 0.5;
  else feedback.push('Add lowercase letters');
  
  if (hasUpper) score += 0.5;
  else feedback.push('Add uppercase letters');
  
  if (hasDigit) score += 0.5;
  else feedback.push('Add numbers');
  
  if (hasSpecial) score += 0.5;
  else feedback.push('Add special characters');
  
  const categoriesMet = [hasLower, hasUpper, hasDigit, hasSpecial].filter(Boolean).length;
  if (categoriesMet < 3) {
    feedback.push('Use at least 3 of: lowercase, uppercase, numbers, special characters');
  }
  
  // Common patterns to avoid
  const commonPatterns = [
    /^123456/,
    /password/i,
    /qwerty/i,
    /letmein/i,
    /welcome/i,
    /admin/i,
    /^(.)\1+$/,  // Repeated characters
    /^(012|123|234|345|456|567|678|789)/,  // Sequential digits
    /^(abc|bcd|cde|def)/i,  // Sequential letters
  ];
  
  for (const pattern of commonPatterns) {
    if (pattern.test(password)) {
      score = Math.max(0, score - 1);
      feedback.push('Avoid common patterns and dictionary words');
      break;
    }
  }
  
  // Require minimum length AND at least 3 character categories to be "strong"
  const isStrong = password.length >= minLength && categoriesMet >= 3 && score >= 3;

  return {
    score: Math.min(4, Math.floor(score)),
    feedback,
    isStrong,
  };
}

/**
 * Helper: minimum length for a given role. SYSTEM_ADMIN / PLATFORM_ADMIN
 * get 14, everyone else gets 12. Use in registration / password-reset
 * validators.
 */
export function minLengthForRole(role: string | undefined): number {
  if (!role) return MIN_LENGTH_DEFAULT;
  const upper = role.toUpperCase();
  if (upper === 'SYSTEM_ADMIN' || upper === 'PLATFORM_ADMIN') return MIN_LENGTH_ADMIN;
  return MIN_LENGTH_DEFAULT;
}

/**
 * Generate password reset token
 */
export function generateResetToken(): {
  token: string;
  hash: string;
  expiresAt: Date;
} {
  const token = crypto.randomBytes(RESET_TOKEN_BYTES).toString('hex');
  const hash = crypto.createHash('sha256').update(token).digest('hex');
  const expiresAt = new Date(Date.now() + RESET_TOKEN_EXPIRY_HOURS * 3600000);
  
  return { token, hash, expiresAt };
}

/**
 * Verify reset token
 */
export function verifyResetToken(token: string, storedHash: string): boolean {
  const hash = crypto.createHash('sha256').update(token).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(storedHash));
}

/**
 * Generate email verification token
 */
export function generateEmailVerificationToken(): string {
  return crypto.randomBytes(32).toString('hex');
}

/**
 * Generate random password
 */
export function generateRandomPassword(length: number = 16): string {
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
  const array = new Uint8Array(length);
  crypto.getRandomValues(array);
  return Array.from(array, byte => chars[byte % chars.length]).join('');
}
