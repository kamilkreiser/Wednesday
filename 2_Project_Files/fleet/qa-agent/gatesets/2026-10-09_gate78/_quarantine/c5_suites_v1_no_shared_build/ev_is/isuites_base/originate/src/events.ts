/**
 * =============================================================================
 * EVENT BUS INITIALISATION — Originate Service
 * =============================================================================
 * Initialises the shared EventBus on startup and re-exports helpers.
 * If REDIS_URL is not set, event publishing is silently skipped.
 * =============================================================================
 */

import Redis from 'ioredis';
import { logger } from './utils/logger';

// ---------------------------------------------------------------------------
// Types (mirrored from @secuura/shared/events to avoid cross-package build dep)
// ---------------------------------------------------------------------------

export interface SecuuraEvent {
  type: string;
  payload: Record<string, unknown>;
  timestamp: string;
  source: string;
  correlationId?: string;
}

export const EventTypes = {
  DOCUMENT_CREATED: 'document.created',
  DOCUMENT_ANCHORED: 'document.anchored',
  DOCUMENT_VERIFIED: 'document.verified',
  DOCUMENT_REVOKED: 'document.revoked',
  CERTIFICATION_ISSUED: 'certification.issued',
  USER_REGISTERED: 'user.registered',
  USER_LOGIN: 'user.login',
  // KS-291: GDPR erasure fan-out. Consumed by the auth / kyc / m365 /
  // wallet-connector user.erased subscribers (shared EventBus consumer
  // groups) — same stream key format, so local publish + shared subscribe
  // interoperate.
  USER_ERASED: 'user.erased',
  EMAIL_SEND_REQUESTED: 'email.send_requested',
  AUDIT_LOG: 'audit.log',
  RETENTION_ENFORCE: 'retention.enforce',
  ANCHOR_REQUESTED: 'anchor.requested',
  NFT_MINT_REQUESTED: 'nft.mint_requested',
} as const;

export type EventType = (typeof EventTypes)[keyof typeof EventTypes];

// ---------------------------------------------------------------------------
// Lightweight publisher (self-contained — no cross-package import needed)
// ---------------------------------------------------------------------------

const STREAM_PREFIX = 'secuura:events:';
let redis: Redis | null = null;
const SERVICE_NAME = 'originate';

/**
 * Initialise event publishing. Safe to call multiple times.
 * Returns true if Redis connection was established.
 */
export function initEventBus(redisUrl?: string): boolean {
  const url = redisUrl || process.env.REDIS_URL;
  if (!url) {
    logger.warn('REDIS_URL not set — event publishing disabled');
    return false;
  }

  if (redis) return true;

  try {
    redis = new Redis(url, {
      maxRetriesPerRequest: 3,
      // KS-617: NEVER return null from retryStrategy. ioredis treats null as
      // "stop reconnecting, permanently" — it is not a back-off signal. The
      // previous `if (times > 5) return null` meant any Redis blip lasting
      // more than a few hundred milliseconds killed this client for the life
      // of the process: no further reconnect attempts, so the 'ready'/'connect'
      // event never fired again and the availability flag stayed false until a
      // human restarted the container — while the container kept reporting
      // healthy. Reconnect forever with capped exponential backoff instead.
      // Per-command latency is bounded separately by maxRetriesPerRequest, so
      // this does not make callers hang while Redis is down: individual
      // commands still fail fast and the connection heals itself.
      retryStrategy(times) {
        return Math.min(times * 200, 5000);
      },
      lazyConnect: true,
    });

    redis.on('error', (err) => {
      logger.debug('EventBus Redis error (non-fatal)', { error: err.message });
    });

    logger.info('EventBus initialised for originate service');
    return true;
  } catch (err: any) {
    logger.warn('Failed to initialise EventBus', { error: err?.message });
    return false;
  }
}

/**
 * Fire-and-forget event publish.
 * Silently no-ops if the EventBus is not initialised.
 */
export async function publishEvent(
  type: EventType,
  payload: Record<string, unknown>,
  correlationId?: string,
): Promise<void> {
  if (!redis) return;

  const event: SecuuraEvent = {
    type,
    payload,
    timestamp: new Date().toISOString(),
    source: SERVICE_NAME,
    ...(correlationId ? { correlationId } : {}),
  };

  try {
    if (redis.status !== 'ready' && redis.status !== 'connecting') {
      await redis.connect();
    }
    await redis.xadd(
      `${STREAM_PREFIX}${type}`,
      '*',
      'event',
      JSON.stringify(event),
    );
  } catch {
    // Fire-and-forget — never let event publishing break the service
  }
}

/**
 * Disconnect the event bus (call during graceful shutdown).
 */
export async function shutdownEventBus(): Promise<void> {
  if (redis) {
    try {
      redis.disconnect();
    } catch {
      // ignore
    }
    redis = null;
  }
}
