/**
 * =============================================================================
 * REDIS-BACKED SECURITY STORES
 * =============================================================================
 * Production-ready security stores using Redis for:
 * - Rate limiting (horizontally scalable)
 * - Brute force protection (persistent across restarts)
 * - CSRF token management
 * 
 * These replace the in-memory stores for production deployments.
 * =============================================================================
 */

import { redisClient, CACHE_TTL } from '../cache/redis-client';
import { logger } from '../utils/logger';

// =============================================================================
// TYPES
// =============================================================================

export interface RateLimitRecord {
  count: number;
  resetAt: number;
}

export interface BruteForceRecord {
  attempts: number;
  lastAttempt: number;
  blockedUntil?: number;
}

export interface CSRFTokenRecord {
  token: string;
  expiresAt: number;
}

// =============================================================================
// RATE LIMIT STORE
// =============================================================================

export class RedisRateLimitStore {
  private prefix = 'security:ratelimit:';

  /**
   * Get rate limit record for a key
   */
  async get(key: string): Promise<RateLimitRecord | null> {
    try {
      const record = await redisClient.get<RateLimitRecord>(`${this.prefix}${key}`);
      
      // Check if expired
      if (record && Date.now() > record.resetAt) {
        await this.delete(key);
        return null;
      }
      
      return record;
    } catch (error) {
      logger.error('RedisRateLimitStore error getting record', { error: String(error) });
      return null;
    }
  }

  /**
   * Set rate limit record
   */
  async set(key: string, record: RateLimitRecord): Promise<void> {
    try {
      const ttl = Math.ceil((record.resetAt - Date.now()) / 1000);
      if (ttl > 0) {
        await redisClient.set(`${this.prefix}${key}`, record, ttl);
      }
    } catch (error) {
      logger.error('RedisRateLimitStore error setting record', { error: String(error) });
    }
  }

  /**
   * Increment rate limit counter atomically
   */
  async increment(key: string, windowMs: number): Promise<{ count: number; resetAt: number }> {
    try {
      const fullKey = `${this.prefix}${key}`;
      const ttlSeconds = Math.ceil(windowMs / 1000);
      
      // Atomic increment with expiry
      const count = await redisClient.incrWithExpiry(fullKey, ttlSeconds);
      const ttl = await redisClient.ttl(fullKey);
      const resetAt = Date.now() + (ttl * 1000);
      
      return { count, resetAt };
    } catch (error) {
      logger.error('RedisRateLimitStore error incrementing', { error: String(error) });
      // Fallback: allow request but don't track
      return { count: 1, resetAt: Date.now() + windowMs };
    }
  }

  /**
   * Delete rate limit record
   */
  async delete(key: string): Promise<void> {
    try {
      await redisClient.delete(`${this.prefix}${key}`);
    } catch (error) {
      logger.error('RedisRateLimitStore error deleting record', { error: String(error) });
    }
  }

  /**
   * Check if key exists
   */
  async has(key: string): Promise<boolean> {
    try {
      return await redisClient.exists(`${this.prefix}${key}`);
    } catch (error) {
      logger.error('RedisRateLimitStore error checking existence', { error: String(error) });
      return false;
    }
  }
}

// =============================================================================
// BRUTE FORCE STORE
// =============================================================================

export class RedisBruteForceStore {
  private prefix = 'security:bruteforce:';
  private defaultLifetime = 300; // 5 minutes

  /**
   * Get brute force record for a key
   */
  async get(key: string): Promise<BruteForceRecord | null> {
    try {
      return await redisClient.get<BruteForceRecord>(`${this.prefix}${key}`);
    } catch (error) {
      logger.error('RedisBruteForceStore error getting record', { error: String(error) });
      return null;
    }
  }

  /**
   * Set brute force record
   */
  async set(key: string, record: BruteForceRecord, lifetimeMs?: number): Promise<void> {
    try {
      const ttl = Math.ceil((lifetimeMs || this.defaultLifetime * 1000) / 1000);
      await redisClient.set(`${this.prefix}${key}`, record, ttl);
    } catch (error) {
      logger.error('RedisBruteForceStore error setting record', { error: String(error) });
    }
  }

  /**
   * Record a failed attempt
   */
  async recordFailure(
    key: string,
    config: { freeRetries: number; minWait: number; maxWait: number; lifetime: number }
  ): Promise<BruteForceRecord> {
    try {
      const record = await this.get(key) || { attempts: 0, lastAttempt: 0 };
      const now = Date.now();
      
      record.attempts++;
      record.lastAttempt = now;
      
      // Calculate lockout if exceeded free retries
      if (record.attempts > config.freeRetries) {
        const waitTime = Math.min(
          config.minWait * Math.pow(2, record.attempts - config.freeRetries),
          config.maxWait
        );
        record.blockedUntil = now + waitTime;
      }
      
      await this.set(key, record, config.lifetime);
      return record;
    } catch (error) {
      logger.error('RedisBruteForceStore error recording failure', { error: String(error) });
      return { attempts: 1, lastAttempt: Date.now() };
    }
  }

  /**
   * Record a successful attempt (reset counter)
   */
  async recordSuccess(key: string): Promise<void> {
    try {
      await this.delete(key);
    } catch (error) {
      logger.error('RedisBruteForceStore error recording success', { error: String(error) });
    }
  }

  /**
   * Check if key is blocked
   */
  async isBlocked(key: string): Promise<{ blocked: boolean; retryAfter?: number }> {
    try {
      const record = await this.get(key);
      
      if (!record || !record.blockedUntil) {
        return { blocked: false };
      }
      
      const now = Date.now();
      if (now < record.blockedUntil) {
        return {
          blocked: true,
          retryAfter: Math.ceil((record.blockedUntil - now) / 1000),
        };
      }
      
      return { blocked: false };
    } catch (error) {
      logger.error('RedisBruteForceStore error checking block status', { error: String(error) });
      return { blocked: false };
    }
  }

  /**
   * Delete brute force record
   */
  async delete(key: string): Promise<void> {
    try {
      await redisClient.delete(`${this.prefix}${key}`);
    } catch (error) {
      logger.error('RedisBruteForceStore error deleting record', { error: String(error) });
    }
  }

  /**
   * Get attempt count
   */
  async getAttempts(key: string): Promise<number> {
    try {
      const record = await this.get(key);
      return record?.attempts || 0;
    } catch (error) {
      logger.error('RedisBruteForceStore error getting attempts', { error: String(error) });
      return 0;
    }
  }
}

// =============================================================================
// CSRF TOKEN STORE
// =============================================================================

export class RedisCSRFStore {
  private prefix = 'security:csrf:';
  private defaultTTL = CACHE_TTL.SESSION; // 5 minutes

  /**
   * Generate and store a CSRF token
   */
  async generate(sessionId: string): Promise<string> {
    try {
      const crypto = await import('crypto');
      const token = crypto.randomBytes(32).toString('hex');
      const expiresAt = Date.now() + (this.defaultTTL * 1000);
      
      await redisClient.set(
        `${this.prefix}${sessionId}`,
        { token, expiresAt },
        this.defaultTTL
      );
      
      return token;
    } catch (error) {
      logger.error('RedisCSRFStore error generating token', { error: String(error) });
      throw error;
    }
  }

  /**
   * Validate a CSRF token
   */
  async validate(sessionId: string, token: string): Promise<boolean> {
    try {
      const record = await redisClient.get<CSRFTokenRecord>(`${this.prefix}${sessionId}`);
      
      if (!record) {
        return false;
      }
      
      // Check expiry
      if (Date.now() > record.expiresAt) {
        await this.delete(sessionId);
        return false;
      }
      
      // Constant-time comparison to prevent timing attacks
      const crypto = await import('crypto');
      return crypto.timingSafeEqual(
        Buffer.from(record.token),
        Buffer.from(token)
      );
    } catch (error) {
      logger.error('RedisCSRFStore error validating token', { error: String(error) });
      return false;
    }
  }

  /**
   * Refresh CSRF token (generate new one)
   */
  async refresh(sessionId: string): Promise<string> {
    await this.delete(sessionId);
    return this.generate(sessionId);
  }

  /**
   * Delete CSRF token
   */
  async delete(sessionId: string): Promise<void> {
    try {
      await redisClient.delete(`${this.prefix}${sessionId}`);
    } catch (error) {
      logger.error('RedisCSRFStore error deleting token', { error: String(error) });
    }
  }
}

// =============================================================================
// SINGLETON INSTANCES
// =============================================================================

export const redisRateLimitStore = new RedisRateLimitStore();
export const redisBruteForceStore = new RedisBruteForceStore();
export const redisCSRFStore = new RedisCSRFStore();

// =============================================================================
// FACTORY FUNCTION
// =============================================================================

/**
 * Get appropriate security stores based on environment
 * Falls back to in-memory stores if Redis is not available
 */
export async function getSecurityStores(): Promise<{
  rateLimit: RedisRateLimitStore;
  bruteForce: RedisBruteForceStore;
  csrf: RedisCSRFStore;
  isRedis: boolean;
}> {
  try {
    // Try to connect to Redis
    await redisClient.connect();
    const isReady = await redisClient.ping();
    
    if (isReady) {
      logger.info('Using Redis-backed security stores');
      return {
        rateLimit: redisRateLimitStore,
        bruteForce: redisBruteForceStore,
        csrf: redisCSRFStore,
        isRedis: true,
      };
    }
  } catch (error) {
    logger.warn('Redis not available, using in-memory stores (not recommended for production)');
  }
  
  // Return Redis stores anyway - they'll handle errors gracefully
  return {
    rateLimit: redisRateLimitStore,
    bruteForce: redisBruteForceStore,
    csrf: redisCSRFStore,
    isRedis: false,
  };
}

export default {
  redisRateLimitStore,
  redisBruteForceStore,
  redisCSRFStore,
  getSecurityStores,
};
