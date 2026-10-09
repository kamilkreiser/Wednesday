/**
 * =============================================================================
 * ERROR TRACKING SERVICE
 * =============================================================================
 * Persists application errors to the system_errors PostgreSQL table.
 * Used by the error handler middleware and Winston logger transport.
 * =============================================================================
 */

import { prisma } from '../db';
import { logger } from '../utils/logger';

export interface SystemError {
  id: string;
  service: string;
  errorType: string;
  message: string;
  stack?: string;
  requestPath?: string;
  requestMethod?: string;
  userId?: string;
  ipAddress?: string;
  severity: 'warning' | 'error' | 'critical';
  metadata?: Record<string, unknown>;
  resolved: boolean;
  resolvedAt?: string;
  createdAt: string;
}

/**
 * Persist an error to the system_errors table.
 * Runs asynchronously and never throws (fire-and-forget for error handlers).
 */
export async function trackError(opts: {
  service: string;
  errorType: string;
  message: string;
  stack?: string;
  requestPath?: string;
  requestMethod?: string;
  userId?: string;
  ipAddress?: string;
  severity?: 'warning' | 'error' | 'critical';
  metadata?: Record<string, unknown>;
}): Promise<void> {
  try {
    const severity = opts.severity || 'error';
    await prisma.$executeRaw`
      INSERT INTO system_errors (service, error_type, message, stack, request_path, request_method, user_id, ip_address, severity, metadata)
      VALUES (
        ${opts.service},
        ${opts.errorType},
        ${opts.message},
        ${opts.stack || null},
        ${opts.requestPath || null},
        ${opts.requestMethod || null},
        ${opts.userId ? opts.userId : null}::uuid,
        ${opts.ipAddress || null}::inet,
        ${severity},
        ${JSON.stringify(opts.metadata || {})}::jsonb
      )
    `;
  } catch (err: any) {
    // Never throw from error tracking — log to stderr as last resort
    logger.error('Failed to persist error', { error: err instanceof Error ? err.message : String(err) });
  }
}

/**
 * Get recent system errors (for admin dashboard).
 */
export async function getRecentErrors(opts?: {
  service?: string;
  severity?: string;
  resolved?: boolean;
  limit?: number;
  offset?: number;
}): Promise<{ errors: SystemError[]; total: number }> {
  try {
    const limit = opts?.limit || 50;
    const offset = opts?.offset || 0;

    // Build dynamic query based on filters
    let errors: any[];
    let countResult: any[];

    if (opts?.service && opts?.severity) {
      errors = await prisma.$queryRaw`
        SELECT * FROM system_errors
        WHERE service = ${opts.service} AND severity = ${opts.severity}
        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
      `;
      countResult = await prisma.$queryRaw`
        SELECT COUNT(*)::int as total FROM system_errors
        WHERE service = ${opts.service} AND severity = ${opts.severity}
      `;
    } else if (opts?.service) {
      errors = await prisma.$queryRaw`
        SELECT * FROM system_errors WHERE service = ${opts.service}
        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
      `;
      countResult = await prisma.$queryRaw`
        SELECT COUNT(*)::int as total FROM system_errors WHERE service = ${opts.service}
      `;
    } else if (opts?.severity) {
      errors = await prisma.$queryRaw`
        SELECT * FROM system_errors WHERE severity = ${opts.severity}
        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
      `;
      countResult = await prisma.$queryRaw`
        SELECT COUNT(*)::int as total FROM system_errors WHERE severity = ${opts.severity}
      `;
    } else if (opts?.resolved !== undefined) {
      errors = await prisma.$queryRaw`
        SELECT * FROM system_errors WHERE resolved = ${opts.resolved}
        ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
      `;
      countResult = await prisma.$queryRaw`
        SELECT COUNT(*)::int as total FROM system_errors WHERE resolved = ${opts.resolved}
      `;
    } else {
      errors = await prisma.$queryRaw`
        SELECT * FROM system_errors ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}
      `;
      countResult = await prisma.$queryRaw`
        SELECT COUNT(*)::int as total FROM system_errors
      `;
    }

    return {
      errors: errors.map(mapErrorRow),
      total: countResult[0]?.total || 0,
    };
  } catch (err: any) {
    logger.error('Failed to query errors', { error: err instanceof Error ? err.message : String(err) });
    return { errors: [], total: 0 };
  }
}

/**
 * Get error statistics (for dashboard widgets).
 */
export async function getErrorStats(): Promise<{
  totalUnresolved: number;
  bySeverity: Record<string, number>;
  byService: Record<string, number>;
  last24h: number;
  last7d: number;
}> {
  try {
    const unresolved: any[] = await prisma.$queryRaw`
      SELECT COUNT(*)::int as c FROM system_errors WHERE resolved = false
    `;

    const bySeverityRows: any[] = await prisma.$queryRaw`
      SELECT severity, COUNT(*)::int as c FROM system_errors WHERE resolved = false GROUP BY severity
    `;

    const byServiceRows: any[] = await prisma.$queryRaw`
      SELECT service, COUNT(*)::int as c FROM system_errors WHERE resolved = false GROUP BY service
    `;

    const last24h: any[] = await prisma.$queryRaw`
      SELECT COUNT(*)::int as c FROM system_errors WHERE created_at > NOW() - INTERVAL '24 hours'
    `;

    const last7d: any[] = await prisma.$queryRaw`
      SELECT COUNT(*)::int as c FROM system_errors WHERE created_at > NOW() - INTERVAL '7 days'
    `;

    const bySeverity: Record<string, number> = {};
    for (const r of bySeverityRows) bySeverity[r.severity] = r.c;

    const byService: Record<string, number> = {};
    for (const r of byServiceRows) byService[r.service] = r.c;

    return {
      totalUnresolved: unresolved[0]?.c || 0,
      bySeverity,
      byService,
      last24h: last24h[0]?.c || 0,
      last7d: last7d[0]?.c || 0,
    };
  } catch {
    return { totalUnresolved: 0, bySeverity: {}, byService: {}, last24h: 0, last7d: 0 };
  }
}

/**
 * Mark an error as resolved.
 */
export async function resolveError(errorId: string): Promise<boolean> {
  try {
    const result = await prisma.$executeRaw`
      UPDATE system_errors SET resolved = true, resolved_at = NOW() WHERE id = ${errorId}::uuid
    `;
    return result > 0;
  } catch {
    return false;
  }
}

/**
 * Bulk resolve errors by service.
 */
export async function resolveErrorsByService(service: string): Promise<number> {
  try {
    return await prisma.$executeRaw`
      UPDATE system_errors SET resolved = true, resolved_at = NOW()
      WHERE service = ${service} AND resolved = false
    `;
  } catch {
    return 0;
  }
}

function mapErrorRow(r: any): SystemError {
  return {
    id: r.id,
    service: r.service,
    errorType: r.error_type,
    message: r.message,
    stack: r.stack || undefined,
    requestPath: r.request_path || undefined,
    requestMethod: r.request_method || undefined,
    userId: r.user_id || undefined,
    ipAddress: r.ip_address || undefined,
    severity: r.severity,
    metadata: r.metadata || {},
    resolved: r.resolved,
    resolvedAt: r.resolved_at?.toISOString?.() || undefined,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
  };
}
