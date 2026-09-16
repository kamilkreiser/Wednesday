/**
 * =============================================================================
 * REDIS SERVICE
 * =============================================================================
 * Provides Redis-backed storage for session data, rate limiting, and caching.
 * Falls back to in-memory storage if Redis is unavailable.
 * =============================================================================
 */

import Redis from 'ioredis';
import { logger } from '../utils/logger';

// =============================================================================
// CONFIGURATION
// =============================================================================

const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const REDIS_PREFIX = 'secuura:gateway:';
const CONNECTION_TIMEOUT = 5000;

// TTL defaults (in seconds)
const TTL = {
  bruteForce: 300,        // 5 minutes
  rateLimit: 60,          // 1 minute
  workflow: 3600,         // 1 hour
  document: 3600,         // 1 hour
  privacy: 86400,         // 24 hours
  signature: 86400,       // 24 hours
};

// =============================================================================
// REDIS CLIENT
// =============================================================================

let redisClient: Redis | null = null;
let isConnected = false;
let fallbackMode = false;

// In-memory fallback stores
const fallbackStores = {
  bruteForce: new Map<string, { attempts: number; blockedUntil?: number }>(),
  rateLimit: new Map<string, { count: number; resetAt: number }>(),
  workflows: new Map<string, object>(),
  rejectedDocs: new Map<string, { status: string; rejectionReason: string; rejectedAt: string; rejectedBy: string }>(),
  workflowDocMap: new Map<string, string>(),
  privacy: new Map<string, Record<string, unknown>>(),
  trustedVerifiers: new Map<string, string[]>(),
  signatures: new Map<string, { address: string; signature: string; signedAt: string }>(),
};

/**
 * Initialize Redis connection
 */
export async function initRedis(): Promise<boolean> {
  try {
    logger.info('[Redis] Connecting', { url: REDIS_URL.replace(/\/\/[^:]+:[^@]+@/, '//*****:*****@') });
    
    redisClient = new Redis(REDIS_URL, {
      connectTimeout: CONNECTION_TIMEOUT,
      maxRetriesPerRequest: 3,
      // KS-617: NEVER return null from retryStrategy. ioredis treats null as
      // "stop reconnecting, permanently" — it is not a back-off signal. The
      // previous `if (times > 3)` branch set fallbackMode and gave up, and
      // because it gave up, the 'connect' handler below (which clears
      // fallbackMode) could never fire again. So a Redis blip of more than
      // ~1 second permanently pinned this gateway into in-memory fallback:
      // per-replica rate-limit counters and brute-force state, with the
      // container still reporting healthy, until a human restarted it.
      //
      // Entering fallbackMode on a dropped connection is still right — the
      // gateway must keep serving. What was wrong is that it was a one-way
      // door. Reconnect forever with capped backoff so 'connect' can clear it.
      retryStrategy: (times) => {
        if (times === 4) {
          // Log once on crossing into sustained-outage territory rather than
          // on every attempt, so a long outage does not flood the log.
          logger.warn('[Redis] Connection lost — serving from in-memory fallback, still reconnecting');
          fallbackMode = true;
        }
        return Math.min(times * 200, 5000);
      },
      lazyConnect: true,
    });

    redisClient.on('connect', () => {
      logger.info('[Redis] Connected successfully');
      isConnected = true;
      fallbackMode = false;
    });

    redisClient.on('error', (err) => {
      logger.error('[Redis] Connection error', { error: err.message });
      isConnected = false;
    });

    redisClient.on('close', () => {
      logger.warn('[Redis] Connection closed');
      isConnected = false;
    });

    await redisClient.connect();
    
    // Test connection
    await redisClient.ping();
    isConnected = true;
    logger.info('[Redis] Connection test successful');
    return true;
  } catch (error) {
    // Pen-test M4 fix: production REFUSES to start without Redis. Rate limit
    // + sessions are both Redis-backed; falling back to per-pod in-memory
    // means each replica has its own counter (effectively no rate limit
    // when N replicas are behind a load balancer) and sessions vanish on
    // restart. In dev/test we still warn and fall back so local work keeps
    // flowing.
    if (process.env.NODE_ENV === 'production') {
      logger.error('[Redis] FATAL: connection failed in production — refusing to start', {
        error: (error as Error).message,
      });
      throw new Error('REDIS_REQUIRED_IN_PRODUCTION: ' + (error as Error).message);
    }
    logger.warn('[Redis] Failed to connect, using in-memory fallback (dev/test only)', { error: (error as Error).message });
    fallbackMode = true;
    return false;
  }
}

/**
 * Check if Redis is available
 */
export function isRedisAvailable(): boolean {
  return isConnected && !fallbackMode && redisClient !== null;
}

/**
 * Get Redis client (for direct access if needed)
 */
export function getRedisClient(): Redis | null {
  return redisClient;
}

// =============================================================================
// BRUTE FORCE PROTECTION
// =============================================================================

interface BruteForceData {
  attempts: number;
  blockedUntil?: number;
}

export async function getBruteForceData(key: string): Promise<BruteForceData | null> {
  const fullKey = `${REDIS_PREFIX}bf:${key}`;
  
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  
  return fallbackStores.bruteForce.get(key) || null;
}

export async function setBruteForceData(key: string, data: BruteForceData): Promise<void> {
  const fullKey = `${REDIS_PREFIX}bf:${key}`;
  
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.bruteForce, JSON.stringify(data));
  } else {
    fallbackStores.bruteForce.set(key, data);
  }
}

export async function deleteBruteForceData(key: string): Promise<void> {
  const fullKey = `${REDIS_PREFIX}bf:${key}`;
  
  if (isRedisAvailable()) {
    await redisClient!.del(fullKey);
  } else {
    fallbackStores.bruteForce.delete(key);
  }
}

// =============================================================================
// RATE LIMITING
// =============================================================================

interface RateLimitData {
  count: number;
  resetAt: number;
}

export async function getRateLimitData(key: string): Promise<RateLimitData | null> {
  const fullKey = `${REDIS_PREFIX}rl:${key}`;
  
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  
  return fallbackStores.rateLimit.get(key) || null;
}

export async function setRateLimitData(key: string, data: RateLimitData): Promise<void> {
  const fullKey = `${REDIS_PREFIX}rl:${key}`;
  
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.rateLimit, JSON.stringify(data));
  } else {
    fallbackStores.rateLimit.set(key, data);
  }
}

// =============================================================================
// WORKFLOW STORAGE (for testing)
// =============================================================================

export async function getWorkflow(id: string): Promise<object | null> {
  const fullKey = `${REDIS_PREFIX}wf:${id}`;
  
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  
  return fallbackStores.workflows.get(id) || null;
}

export async function setWorkflow(id: string, data: object): Promise<void> {
  const fullKey = `${REDIS_PREFIX}wf:${id}`;
  
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.workflow, JSON.stringify(data));
  } else {
    fallbackStores.workflows.set(id, data);
  }
}

export async function deleteWorkflow(id: string): Promise<boolean> {
  const fullKey = `${REDIS_PREFIX}wf:${id}`;

  if (isRedisAvailable()) {
    const deleted = await redisClient!.del(fullKey);
    return deleted > 0;
  }

  return fallbackStores.workflows.delete(id);
}

export async function getAllWorkflows(): Promise<object[]> {
  if (isRedisAvailable()) {
    const keys = await redisClient!.keys(`${REDIS_PREFIX}wf:*`);
    const workflowKeys = keys.filter(k => !k.includes('wf-doc:'));
    if (workflowKeys.length === 0) return [];
    const pipeline = redisClient!.pipeline();
    workflowKeys.forEach(k => pipeline.get(k));
    const results = await pipeline.exec();
    return (results || [])
      .filter(([err, val]) => !err && val)
      .map(([, val]) => JSON.parse(val as string));
  }

  return Array.from(fallbackStores.workflows.values());
}

// =============================================================================
// INTEGRATION STORAGE
// =============================================================================

const integrationStore = new Map<string, object>();

export async function getIntegration(id: string): Promise<object | null> {
  const fullKey = `${REDIS_PREFIX}integ:${id}`;

  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }

  return integrationStore.get(id) || null;
}

export async function setIntegration(id: string, data: object): Promise<void> {
  const fullKey = `${REDIS_PREFIX}integ:${id}`;

  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.document, JSON.stringify(data));
  } else {
    integrationStore.set(id, data);
  }
}

export async function deleteIntegration(id: string): Promise<boolean> {
  const fullKey = `${REDIS_PREFIX}integ:${id}`;

  if (isRedisAvailable()) {
    const deleted = await redisClient!.del(fullKey);
    return deleted > 0;
  }

  return integrationStore.delete(id);
}

export async function getAllIntegrations(): Promise<object[]> {
  if (isRedisAvailable()) {
    const keys = await redisClient!.keys(`${REDIS_PREFIX}integ:*`);
    if (keys.length === 0) return [];
    const pipeline = redisClient!.pipeline();
    keys.forEach(k => pipeline.get(k));
    const results = await pipeline.exec();
    return (results || [])
      .filter(([err, val]) => !err && val)
      .map(([, val]) => JSON.parse(val as string));
  }

  return Array.from(integrationStore.values());
}

// =============================================================================
// REJECTED DOCUMENTS
// =============================================================================

interface RejectedDocData {
  status: string;
  rejectionReason: string;
  rejectedAt: string;
  rejectedBy: string;
}

export async function getRejectedDocument(id: string): Promise<RejectedDocData | null> {
  const fullKey = `${REDIS_PREFIX}rejected:${id}`;

  if (isRedisAvailable()) {
    try {
      const data = await redisClient!.get(fullKey);
      if (data) return JSON.parse(data);
    } catch {
      // Fall through to in-memory
    }
  }

  return fallbackStores.rejectedDocs.get(id) || null;
}

export async function setRejectedDocument(id: string, data: RejectedDocData): Promise<void> {
  const fullKey = `${REDIS_PREFIX}rejected:${id}`;

  // Always update in-memory fallback
  fallbackStores.rejectedDocs.set(id, data);

  if (isRedisAvailable()) {
    try {
      await redisClient!.setex(fullKey, TTL.privacy, JSON.stringify(data));
    } catch {
      // In-memory fallback already set above
    }
  }
}

// =============================================================================
// WORKFLOW-DOCUMENT MAPPING
// =============================================================================

export async function getWorkflowDocumentMapping(workflowId: string): Promise<string | null> {
  const fullKey = `${REDIS_PREFIX}wf-doc:${workflowId}`;

  if (isRedisAvailable()) {
    try {
      return await redisClient!.get(fullKey);
    } catch {
      // Fall through to in-memory
    }
  }

  return fallbackStores.workflowDocMap.get(workflowId) || null;
}

export async function setWorkflowDocumentMapping(workflowId: string, documentId: string): Promise<void> {
  const fullKey = `${REDIS_PREFIX}wf-doc:${workflowId}`;

  // Always update in-memory fallback
  fallbackStores.workflowDocMap.set(workflowId, documentId);

  if (isRedisAvailable()) {
    try {
      await redisClient!.setex(fullKey, TTL.privacy, documentId);
    } catch {
      // In-memory fallback already set above
    }
  }
}

// =============================================================================
// PRIVACY SETTINGS
// =============================================================================

export async function getPrivacySettings(userId: string): Promise<Record<string, unknown> | null> {
  const fullKey = `${REDIS_PREFIX}privacy:${userId}`;
  
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  
  return fallbackStores.privacy.get(userId) || null;
}

export async function setPrivacySettings(userId: string, settings: Record<string, unknown>): Promise<void> {
  const fullKey = `${REDIS_PREFIX}privacy:${userId}`;
  
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.privacy, JSON.stringify(settings));
  } else {
    fallbackStores.privacy.set(userId, settings);
  }
}

// =============================================================================
// TRUSTED VERIFIERS
// =============================================================================

export async function getTrustedVerifiers(userId: string): Promise<string[]> {
  const fullKey = `${REDIS_PREFIX}trusted:${userId}`;
  
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : [];
  }
  
  return fallbackStores.trustedVerifiers.get(userId) || [];
}

export async function setTrustedVerifiers(userId: string, verifiers: string[]): Promise<void> {
  const fullKey = `${REDIS_PREFIX}trusted:${userId}`;
  
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.privacy, JSON.stringify(verifiers));
  } else {
    fallbackStores.trustedVerifiers.set(userId, verifiers);
  }
}

export async function addTrustedVerifier(userId: string, verifierDid: string): Promise<void> {
  const existing = await getTrustedVerifiers(userId);
  if (!existing.includes(verifierDid)) {
    existing.push(verifierDid);
    await setTrustedVerifiers(userId, existing);
  }
}

// =============================================================================
// DOCUMENT SIGNATURES
// =============================================================================

interface SignatureData {
  address?: string;
  walletAddress?: string;
  signature: string;
  nonce?: string;
  signedAt: string;
}

export async function getDocumentSignature(documentId: string): Promise<SignatureData | null> {
  const fullKey = `${REDIS_PREFIX}sig:${documentId}`;

  if (isRedisAvailable()) {
    try {
      const data = await redisClient!.get(fullKey);
      if (data) return JSON.parse(data);
    } catch {
      // Fall through to in-memory
    }
  }

  return fallbackStores.signatures.get(documentId) || null;
}

export async function setDocumentSignature(documentId: string, data: SignatureData): Promise<void> {
  const fullKey = `${REDIS_PREFIX}sig:${documentId}`;

  // Always update in-memory fallback
  fallbackStores.signatures.set(documentId, {
    address: data.address || data.walletAddress || '',
    signature: data.signature,
    signedAt: data.signedAt,
  });

  if (isRedisAvailable()) {
    try {
      await redisClient!.setex(fullKey, TTL.signature, JSON.stringify(data));
    } catch {
      // In-memory fallback already set above
    }
  }
}

// =============================================================================
// DOCUMENT TYPES STORAGE
// =============================================================================

const documentTypesStore = new Map<string, object>();

export async function getDocumentType(id: string): Promise<object | null> {
  const fullKey = `${REDIS_PREFIX}doctype:${id}`;

  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }

  return documentTypesStore.get(id) || null;
}

export async function setDocumentType(id: string, data: object): Promise<void> {
  const fullKey = `${REDIS_PREFIX}doctype:${id}`;

  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.document, JSON.stringify(data));
  } else {
    documentTypesStore.set(id, data);
  }
}

export async function deleteDocumentType(id: string): Promise<boolean> {
  const fullKey = `${REDIS_PREFIX}doctype:${id}`;

  if (isRedisAvailable()) {
    const deleted = await redisClient!.del(fullKey);
    return deleted > 0;
  }

  return documentTypesStore.delete(id);
}

export async function getAllDocumentTypes(): Promise<object[]> {
  if (isRedisAvailable()) {
    const keys = await redisClient!.keys(`${REDIS_PREFIX}doctype:*`);
    if (keys.length === 0) return [];
    const pipeline = redisClient!.pipeline();
    keys.forEach(k => pipeline.get(k));
    const results = await pipeline.exec();
    return (results || [])
      .filter(([err, val]) => !err && val)
      .map(([, val]) => JSON.parse(val as string));
  }

  return Array.from(documentTypesStore.values());
}

// =============================================================================
// WORKFLOW INSTANCES (enforcement pipeline)
// =============================================================================

const workflowInstancesStore = new Map<string, object>();

export async function getWorkflowInstance(id: string): Promise<object | null> {
  const fullKey = `${REDIS_PREFIX}wfi:${id}`;
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  return workflowInstancesStore.get(id) || null;
}

export async function setWorkflowInstance(id: string, data: object): Promise<void> {
  const fullKey = `${REDIS_PREFIX}wfi:${id}`;
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.workflow * 24, JSON.stringify(data));
  } else {
    workflowInstancesStore.set(id, data);
  }
}

export async function getAllWorkflowInstances(): Promise<object[]> {
  if (isRedisAvailable()) {
    const keys = await redisClient!.keys(`${REDIS_PREFIX}wfi:*`);
    if (keys.length === 0) return [];
    const pipeline = redisClient!.pipeline();
    keys.forEach(k => pipeline.get(k));
    const results = await pipeline.exec();
    return (results || [])
      .filter(([err, val]) => !err && val)
      .map(([, val]) => JSON.parse(val as string));
  }
  return Array.from(workflowInstancesStore.values());
}

// =============================================================================
// PENDING DOCUMENTS (held during workflow approval)
// =============================================================================

const pendingDocumentsStore = new Map<string, object>();

export async function getPendingDocument(id: string): Promise<object | null> {
  const fullKey = `${REDIS_PREFIX}pendoc:${id}`;
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  return pendingDocumentsStore.get(id) || null;
}

export async function setPendingDocument(id: string, data: object): Promise<void> {
  const fullKey = `${REDIS_PREFIX}pendoc:${id}`;
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.workflow * 24, JSON.stringify(data));
  } else {
    pendingDocumentsStore.set(id, data);
  }
}

export async function deletePendingDocument(id: string): Promise<boolean> {
  const fullKey = `${REDIS_PREFIX}pendoc:${id}`;
  if (isRedisAvailable()) {
    const deleted = await redisClient!.del(fullKey);
    return deleted > 0;
  }
  return pendingDocumentsStore.delete(id);
}

// =============================================================================
// VERIFICATION POLICIES STORAGE
// =============================================================================

const verificationPoliciesStore = new Map<string, object>();

export async function getVerificationPolicy(id: string): Promise<object | null> {
  const fullKey = `${REDIS_PREFIX}vpol:${id}`;
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  return verificationPoliciesStore.get(id) || null;
}

export async function setVerificationPolicy(id: string, data: object): Promise<void> {
  const fullKey = `${REDIS_PREFIX}vpol:${id}`;
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.document, JSON.stringify(data));
  } else {
    verificationPoliciesStore.set(id, data);
  }
}

export async function deleteVerificationPolicy(id: string): Promise<boolean> {
  const fullKey = `${REDIS_PREFIX}vpol:${id}`;
  if (isRedisAvailable()) {
    const deleted = await redisClient!.del(fullKey);
    return deleted > 0;
  }
  return verificationPoliciesStore.delete(id);
}

export async function getAllVerificationPolicies(): Promise<object[]> {
  if (isRedisAvailable()) {
    const keys = await redisClient!.keys(`${REDIS_PREFIX}vpol:*`);
    if (keys.length === 0) return [];
    const pipeline = redisClient!.pipeline();
    keys.forEach(k => pipeline.get(k));
    const results = await pipeline.exec();
    return (results || [])
      .filter(([err, val]) => !err && val)
      .map(([, val]) => JSON.parse(val as string));
  }
  return Array.from(verificationPoliciesStore.values());
}

// =============================================================================
// NOTIFICATION SETTINGS STORAGE
// =============================================================================

const notificationSettingsStore = new Map<string, object>();

export async function getNotificationSettings(key: string): Promise<object | null> {
  const fullKey = `${REDIS_PREFIX}notif:${key}`;
  if (isRedisAvailable()) {
    const data = await redisClient!.get(fullKey);
    return data ? JSON.parse(data) : null;
  }
  return notificationSettingsStore.get(key) || null;
}

export async function setNotificationSettings(key: string, data: object): Promise<void> {
  const fullKey = `${REDIS_PREFIX}notif:${key}`;
  if (isRedisAvailable()) {
    await redisClient!.setex(fullKey, TTL.privacy, JSON.stringify(data));
  } else {
    notificationSettingsStore.set(key, data);
  }
}

// =============================================================================
// CLEANUP (for in-memory fallback)
// =============================================================================

export function cleanupFallbackStores(): void {
  const now = Date.now();
  
  // Clean brute force store
  for (const [key, value] of fallbackStores.bruteForce.entries()) {
    if (value.blockedUntil && now > value.blockedUntil) {
      fallbackStores.bruteForce.delete(key);
    }
  }
  
  // Clean rate limit store
  for (const [key, value] of fallbackStores.rateLimit.entries()) {
    if (now > value.resetAt) {
      fallbackStores.rateLimit.delete(key);
    }
  }
}

// Start periodic cleanup for fallback stores
setInterval(cleanupFallbackStores, 60000);

// =============================================================================
// HEALTH CHECK
// =============================================================================

export async function getRedisHealth(): Promise<{ status: string; mode: string; latency?: number }> {
  if (!isRedisAvailable()) {
    return { status: 'fallback', mode: 'in-memory' };
  }
  
  try {
    const start = Date.now();
    await redisClient!.ping();
    const latency = Date.now() - start;
    
    return { status: 'healthy', mode: 'redis', latency };
  } catch (error) {
    return { status: 'error', mode: 'redis' };
  }
}
