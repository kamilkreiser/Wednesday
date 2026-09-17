/**
 * =============================================================================
 * SECURITY MIDDLEWARE — API Gateway
 * =============================================================================
 * Extracted from the gateway monolith. Contains:
 * - sanitizeInput         — XSS prevention via HTML entity encoding
 * - detectSuspiciousRequests — blocks requests matching known attack patterns
 * - bruteForceProtection  — exponential back-off on failed auth (Redis-backed)
 * - requestFingerprint    — hashes client characteristics for tracking
 * =============================================================================
 */

import * as crypto from 'crypto';
import { Request, Response, NextFunction, RequestHandler } from 'express';
import { logger as winstonLogger } from '../utils/logger';
import * as redisService from '../services/redis';

// The Express.Request augmentation (requestId, user) is declared in index.ts
// and is available project-wide via the global namespace merge.

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Shape of the SECURITY_CONFIG object expected by these middleware functions.
 * The gateway owns the actual config — we only declare what we need here.
 */
export interface SecurityConfig {
  bruteForce: {
    freeRetries: number;
    minWait: number;
    maxWait: number;
    lifetime: number;
  };
  suspiciousPatterns: RegExp[];
}

// ---------------------------------------------------------------------------
// Security logging helper (mirrors the gateway's securityLog)
// ---------------------------------------------------------------------------

function securityLog(
  event: string,
  req: Request,
  details?: object,
  severity: 'low' | 'medium' | 'high' | 'critical' = 'medium',
) {
  winstonLogger.warn(event, {
    type: 'security',
    requestId: req.requestId,
    userId: req.user?.userId,
    ip: req.ip,
    severity,
    method: req.method,
    path: req.path,
    userAgent: req.get('user-agent'),
    ...details,
  });
}

// ---------------------------------------------------------------------------
// Input sanitization — prevents XSS
// ---------------------------------------------------------------------------

const sanitize = (value: any): any => {
  if (typeof value === 'string') {
    return value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
  } else if (Array.isArray(value)) {
    // Handle arrays properly — don't convert to objects
    return value.map(item => sanitize(item));
  } else if (typeof value === 'object' && value !== null) {
    const result: Record<string, any> = {};
    for (const [key, val] of Object.entries(value)) {
      result[key] = sanitize(val);
    }
    return result;
  }
  return value;
};

export const sanitizeInput: RequestHandler = (req, _res, next) => {
  if (req.body && typeof req.body === 'object') {
    req.body = sanitize(req.body);
  }
  next();
};

// ---------------------------------------------------------------------------
// Suspicious request detection
// ---------------------------------------------------------------------------

export function createDetectSuspiciousRequests(
  config: SecurityConfig,
): RequestHandler {
  return (req: Request, res: Response, next: NextFunction) => {
    const checkString = (str: string): boolean =>
      config.suspiciousPatterns.some(pattern => pattern.test(str));

    const checkObject = (obj: Record<string, any>): boolean => {
      for (const value of Object.values(obj)) {
        if (typeof value === 'string' && checkString(value)) {
          return true;
        }
        if (typeof value === 'object' && value !== null && checkObject(value)) {
          return true;
        }
      }
      return false;
    };

    // Check URL path
    if (checkString(req.path)) {
      securityLog('SUSPICIOUS_PATH_DETECTED', req, { path: req.path }, 'high');
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request' } });
      return;
    }

    // Check query parameters
    if (req.query && checkObject(req.query as Record<string, any>)) {
      securityLog('SUSPICIOUS_QUERY_DETECTED', req, { query: req.query }, 'high');
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request parameters' } });
      return;
    }

    // Check body
    if (req.body && checkObject(req.body)) {
      securityLog('SUSPICIOUS_BODY_DETECTED', req, { bodyKeys: Object.keys(req.body) }, 'high');
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request body' } });
      return;
    }

    next();
  };
}

// ---------------------------------------------------------------------------
// Brute force protection for authentication endpoints (Redis-backed)
// ---------------------------------------------------------------------------

export function createBruteForceProtection(
  config: SecurityConfig,
): RequestHandler {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.path.includes('/auth/login')) {
      return next();
    }

    const key = req.ip || 'unknown';
    const now = Date.now();

    try {
      const record = await redisService.getBruteForceData(key);

      if (record?.blockedUntil && now < record.blockedUntil) {
        const retryAfter = Math.ceil((record.blockedUntil - now) / 1000);
        res.setHeader('Retry-After', retryAfter.toString());
        securityLog('BRUTE_FORCE_BLOCKED', req, { attemptsToDate: record.attempts }, 'high');
        res.status(429).json({
          error: 'Too many failed attempts',
          message: 'Please try again later',
          retryAfter,
        });
        return;
      }

      // Attach helper to record success/failure
      (req as any).bruteForce = {
        recordFailure: async () => {
          const rec = await redisService.getBruteForceData(key) || { attempts: 0 };
          rec.attempts++;
          if (rec.attempts > config.bruteForce.freeRetries) {
            const waitTime = Math.min(
              config.bruteForce.minWait * Math.pow(2, rec.attempts - config.bruteForce.freeRetries),
              config.bruteForce.maxWait,
            );
            rec.blockedUntil = now + waitTime;
            securityLog('BRUTE_FORCE_LOCKOUT', req, { attempts: rec.attempts, lockoutMs: waitTime }, 'medium');
          }
          await redisService.setBruteForceData(key, rec);
        },
        recordSuccess: async () => {
          await redisService.deleteBruteForceData(key);
        },
      };

      next();
    } catch (error) {
      // On Redis error, allow the request through (fail open for availability)
      winstonLogger.error('[BruteForce] Redis error, allowing request', {
        error: error instanceof Error ? error.message : String(error),
      });
      next();
    }
  };
}

// ---------------------------------------------------------------------------
// Request fingerprinting
// ---------------------------------------------------------------------------

export const requestFingerprint: RequestHandler = (req, _res, next) => {
  const components = [
    req.ip,
    req.headers['user-agent'] || '',
    req.headers['accept-language'] || '',
    req.headers['accept-encoding'] || '',
  ];
  (req as any).fingerprint = crypto
    .createHash('sha256')
    .update(components.join('|'))
    .digest('hex')
    .substring(0, 16);
  next();
};
