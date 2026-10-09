/**
 * =============================================================================
 * DATA RETENTION SCHEDULER
 * =============================================================================
 * Runs data retention enforcement on a configurable interval (default: daily).
 * Auto-deletes or anonymizes expired data based on registered retention policies.
 * =============================================================================
 */

import { enforceRetention } from './gdprService';
import { logger } from '../utils/logger';

const INTERVAL_MS = parseInt(process.env.RETENTION_INTERVAL_MS || '', 10) || 24 * 60 * 60 * 1000; // default 24h
let timer: ReturnType<typeof setInterval> | null = null;

export function startRetentionScheduler(): void {
  if (timer) {
    logger.warn('Scheduler already running');
    return;
  }

  const STARTUP_DELAY_MS = parseInt(process.env.RETENTION_STARTUP_DELAY_MS || '', 10) || 60_000; // default 60s
  logger.info('Scheduler started', { intervalHours: Math.round(INTERVAL_MS / 3600000), startupDelayMs: STARTUP_DELAY_MS });

  // Defer first enforcement to allow service readiness, then repeat on interval
  setTimeout(() => {
    runEnforcement();
    timer = setInterval(runEnforcement, INTERVAL_MS);
  }, STARTUP_DELAY_MS);
}

export function stopRetentionScheduler(): void {
  if (timer) {
    clearInterval(timer);
    timer = null;
    logger.info('Scheduler stopped');
  }
}

async function runEnforcement(): Promise<void> {
  try {
    logger.info('Starting scheduled enforcement');
    const logs = await enforceRetention();
    const total = logs.reduce((sum, l) => sum + l.recordsAffected, 0);
    if (total > 0) {
      logger.info('Enforcement complete', { policiesApplied: logs.length, recordsAffected: total });
    } else {
      logger.info('Enforcement complete — no records required processing');
    }
  } catch (err: any) {
    logger.error('Scheduled enforcement failed', { error: err instanceof Error ? err.message : String(err) });
  }
}
