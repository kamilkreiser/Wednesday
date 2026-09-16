/**
 * =============================================================================
 * RESET SERVICE — DEMO SERVICE
 * =============================================================================
 * Handles database restoration from pg_dump snapshots and Redis cache flushing.
 * Used by the reset endpoint to restore demo data to its pristine seed state.
 * =============================================================================
 */

import { promisify } from 'util';
import { execFile as execFileCb } from 'child_process';
import fs from 'fs';

import Redis from 'ioredis';

import { logger } from '../utils/logger';

const execFile = promisify(execFileCb);

// =============================================================================
// DATABASE RESET
// =============================================================================

export interface ResetDatabaseResult {
  success: boolean;
  durationMs: number;
}

/**
 * Restore PostgreSQL database from a pg_dump snapshot file.
 * Uses pg_restore with --clean --if-exists to drop and recreate objects.
 */
export async function resetDatabase(snapshotPath: string): Promise<ResetDatabaseResult> {
  // Validate snapshot file exists
  try {
    fs.accessSync(snapshotPath, fs.constants.R_OK);
  } catch {
    throw new Error(`Snapshot file not found or not readable: ${snapshotPath}`);
  }

  const databaseUrl = process.env.DATABASE_URL;
  if (!databaseUrl) {
    throw new Error('DATABASE_URL environment variable is not set');
  }

  const startTime = Date.now();
  logger.info('Starting database reset', { snapshotPath });

  try {
    const { stderr } = await execFile('pg_restore', [
      '--clean',
      '--if-exists',
      '--no-owner',
      '--no-acl',
      '--dbname',
      databaseUrl,
      snapshotPath,
    ]);

    // pg_restore writes warnings to stderr even on success
    if (stderr) {
      logger.warn('pg_restore warnings (non-fatal)', { stderr: stderr.trim() });
    }

    const durationMs = Date.now() - startTime;
    logger.info('Database reset complete', { durationMs });

    return { success: true, durationMs };
  } catch (err: unknown) {
    const durationMs = Date.now() - startTime;
    const message = err instanceof Error ? err.message : 'Unknown pg_restore error';
    logger.error('Database reset failed', { error: message, durationMs });
    throw new Error(`pg_restore failed: ${message}`);
  }
}

// =============================================================================
// REDIS RESET
// =============================================================================

export interface ResetRedisResult {
  success: boolean;
  keysCleared: number;
}

/**
 * Flush all Redis keys. Creates a dedicated connection to avoid interfering
 * with the state route's connection lifecycle.
 */
export async function resetRedis(): Promise<ResetRedisResult> {
  const redisUrl = process.env.REDIS_URL;
  if (!redisUrl) {
    logger.info('No REDIS_URL configured, skipping Redis flush');
    return { success: true, keysCleared: 0 };
  }

  const client = new Redis(redisUrl, {
    maxRetriesPerRequest: 1,
    retryStrategy: () => null,
  });

  try {
    logger.info('Starting Redis flush');

    const dbSize = await client.dbsize();
    await client.flushall();

    logger.info('Redis flush complete', { keysCleared: dbSize });

    return { success: true, keysCleared: dbSize };
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Unknown Redis error';
    logger.error('Redis flush failed', { error: message });
    throw new Error(`Redis flush failed: ${message}`);
  } finally {
    await client.quit();
  }
}
