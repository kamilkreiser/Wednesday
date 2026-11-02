/**
 * =============================================================================
 * EXPRESS CACHE MIDDLEWARE
 * =============================================================================
 * HTTP response caching middleware for Express applications
 */

import { Request, Response, NextFunction, RequestHandler } from 'express';
import { redisClient, CACHE_TTL, CACHE_PREFIX } from './redis-client';
import crypto from 'crypto';
import { logger } from '../utils/logger';

export interface CacheOptions {
  ttl?: number;
  prefix?: string;
  keyGenerator?: (req: Request) => string;
  condition?: (req: Request) => boolean;
  tags?: string[];
  invalidateOn?: string[];
}

interface CachedResponse {
  statusCode: number;
  headers: Record<string, string>;
  body: unknown;
  cachedAt: string;
  ttl: number;
}

/**
 * Generate cache key from request
 */
function generateCacheKey(req: Request, prefix: string): string {
  const userId = (req as any).user?.userId || 'anonymous';
  const method = req.method;
  const path = req.path;
  const query = JSON.stringify(req.query);
  
  const hash = crypto
    .createHash('md5')
    .update(`${userId}:${method}:${path}:${query}`)
    .digest('hex')
    .substring(0, 16);
  
  return `${prefix}${hash}`;
}

/**
 * Cache middleware factory
 */
export function cacheMiddleware(options: CacheOptions = {}): RequestHandler {
  const {
    ttl = CACHE_TTL.MEDIUM,
    prefix = 'http:',
    keyGenerator = (req) => generateCacheKey(req, prefix),
    condition = () => true,
  } = options;

  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    // Only cache GET requests
    if (req.method !== 'GET') {
      return next();
    }

    // Check condition
    if (!condition(req)) {
      return next();
    }

    // Check if Redis is available
    if (!redisClient.isReady()) {
      return next();
    }

    const cacheKey = keyGenerator(req);

    try {
      // Try to get cached response
      const cached = await redisClient.get<CachedResponse>(cacheKey);

      if (cached) {
        // Set cache headers
        res.setHeader('X-Cache', 'HIT');
        res.setHeader('X-Cache-Key', cacheKey);
        res.setHeader('X-Cached-At', cached.cachedAt);
        
        // Restore original headers
        for (const [key, value] of Object.entries(cached.headers)) {
          if (!['content-length', 'transfer-encoding'].includes(key.toLowerCase())) {
            res.setHeader(key, value);
          }
        }

        res.status(cached.statusCode).json(cached.body);
        return;
      }

      // Cache miss - intercept response
      const originalJson = res.json.bind(res);
      
      res.json = function(body: unknown) {
        // Only cache successful responses
        if (res.statusCode >= 200 && res.statusCode < 300) {
          const responseToCache: CachedResponse = {
            statusCode: res.statusCode,
            headers: {},
            body,
            cachedAt: new Date().toISOString(),
            ttl,
          };

          // Store selected headers
          const headersToCache = ['content-type', 'etag', 'last-modified'];
          for (const header of headersToCache) {
            const value = res.getHeader(header);
            if (value) {
              responseToCache.headers[header] = String(value);
            }
          }

          // Cache asynchronously
          redisClient.set(cacheKey, responseToCache, ttl).catch(err => {
            logger.error('Cache error storing response', { error: String(err) });
          });
        }

        // Set cache headers
        res.setHeader('X-Cache', 'MISS');
        res.setHeader('X-Cache-Key', cacheKey);

        return originalJson(body);
      };

      next();
    } catch (error) {
      logger.error('Cache middleware error', { error: String(error) });
      next();
    }
  };
}

/**
 * Cache invalidation middleware
 */
export function cacheInvalidationMiddleware(patterns: string[]): RequestHandler {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    // Intercept response to invalidate cache on success
    const originalJson = res.json.bind(res);

    res.json = function(body: unknown) {
      // Invalidate cache on successful mutations
      if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          for (const pattern of patterns) {
            redisClient.deletePattern(pattern).catch(err => {
              logger.error('Cache invalidation error', { error: String(err) });
            });
          }
        }
      }

      return originalJson(body);
    };

    next();
  };
}

/**
 * Document cache helper
 */
export const documentCache = {
  async get(documentId: string): Promise<unknown | null> {
    return redisClient.get(`${CACHE_PREFIX.DOCUMENT}${documentId}`);
  },

  async set(documentId: string, data: unknown): Promise<void> {
    await redisClient.set(`${CACHE_PREFIX.DOCUMENT}${documentId}`, data, CACHE_TTL.DOCUMENT);
  },

  async invalidate(documentId: string): Promise<void> {
    await redisClient.delete(`${CACHE_PREFIX.DOCUMENT}${documentId}`);
  },

  async invalidateAll(): Promise<number> {
    return redisClient.deletePattern(`${CACHE_PREFIX.DOCUMENT}*`);
  },
};

/**
 * User cache helper
 */
export const userCache = {
  async get(userId: string): Promise<unknown | null> {
    return redisClient.get(`${CACHE_PREFIX.USER}${userId}`);
  },

  async set(userId: string, data: unknown): Promise<void> {
    await redisClient.set(`${CACHE_PREFIX.USER}${userId}`, data, CACHE_TTL.USER_PROFILE);
  },

  async invalidate(userId: string): Promise<void> {
    await redisClient.delete(`${CACHE_PREFIX.USER}${userId}`);
  },
};

/**
 * Certification cache helper
 */
export const certificationCache = {
  async get(certId: string): Promise<unknown | null> {
    return redisClient.get(`${CACHE_PREFIX.CERTIFICATION}${certId}`);
  },

  async set(certId: string, data: unknown): Promise<void> {
    await redisClient.set(`${CACHE_PREFIX.CERTIFICATION}${certId}`, data, CACHE_TTL.DOCUMENT);
  },

  async invalidate(certId: string): Promise<void> {
    await redisClient.delete(`${CACHE_PREFIX.CERTIFICATION}${certId}`);
  },

  async invalidateByUser(userId: string): Promise<number> {
    return redisClient.deletePattern(`${CACHE_PREFIX.CERTIFICATION}user:${userId}:*`);
  },
};

/**
 * Governance cache helper
 */
export const governanceCache = {
  async getState(): Promise<unknown | null> {
    return redisClient.get(`${CACHE_PREFIX.GOVERNANCE}state`);
  },

  async setState(data: unknown): Promise<void> {
    await redisClient.set(`${CACHE_PREFIX.GOVERNANCE}state`, data, CACHE_TTL.SHORT);
  },

  async getProposal(proposalId: string): Promise<unknown | null> {
    return redisClient.get(`${CACHE_PREFIX.PROPOSAL}${proposalId}`);
  },

  async setProposal(proposalId: string, data: unknown): Promise<void> {
    await redisClient.set(`${CACHE_PREFIX.PROPOSAL}${proposalId}`, data, CACHE_TTL.SHORT);
  },

  async invalidateProposal(proposalId: string): Promise<void> {
    await redisClient.delete(`${CACHE_PREFIX.PROPOSAL}${proposalId}`);
    await redisClient.delete(`${CACHE_PREFIX.GOVERNANCE}state`);
  },
};

/**
 * Rate limiting helper
 */
export const rateLimitCache = {
  async checkLimit(
    key: string,
    limit: number,
    windowSeconds: number
  ): Promise<{ allowed: boolean; remaining: number; resetIn: number }> {
    const cacheKey = `${CACHE_PREFIX.RATE_LIMIT}${key}`;
    
    const count = await redisClient.incrWithExpiry(cacheKey, windowSeconds);
    const ttl = await redisClient.ttl(cacheKey);
    
    return {
      allowed: count <= limit,
      remaining: Math.max(0, limit - count),
      resetIn: ttl > 0 ? ttl : windowSeconds,
    };
  },
};

export default {
  cacheMiddleware,
  cacheInvalidationMiddleware,
  documentCache,
  userCache,
  certificationCache,
  governanceCache,
  rateLimitCache,
};
