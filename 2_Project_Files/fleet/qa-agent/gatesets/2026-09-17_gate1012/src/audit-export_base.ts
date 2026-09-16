/**
 * =============================================================================
 * AUDIT LOG EXPORT ROUTES
 * =============================================================================
 * Admin endpoints for exporting audit logs in CSV or JSON format.
 *
 * Usage in index.ts:
 *   import auditExportRouter from './routes/audit-export';
 *   app.use('/api/admin/audit', auditExportRouter);
 * =============================================================================
 */

import { Router, Request, Response } from 'express';

const router = Router();

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface AuditEntry {
  id: string;
  timestamp: string;
  type: string;
  action: string;
  userId: string;
  email?: string;
  ipAddress?: string;
  userAgent?: string;
  resource?: string;
  resourceId?: string;
  details?: string;
  outcome: 'success' | 'failure';
}

type AuditType = 'all' | 'auth' | 'document' | 'admin' | 'billing';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const SECURITY_SERVICE_URL = process.env.SECURITY_SERVICE_URL || 'http://localhost:4005';

function escapeCSVField(value: string | undefined | null): string {
  if (value == null) return '';
  const str = String(value);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

function formatDate(dateStr: string): string {
  // Validate and normalize date input
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) {
    throw new Error(`Invalid date: ${dateStr}`);
  }
  return date.toISOString().split('T')[0];
}

function auditEntriesToCSV(entries: AuditEntry[]): string {
  const headers = [
    'id', 'timestamp', 'type', 'action', 'userId', 'email',
    'ipAddress', 'userAgent', 'resource', 'resourceId', 'details', 'outcome',
  ];

  const headerRow = headers.join(',');

  const dataRows = entries.map((entry) =>
    headers.map((h) => escapeCSVField((entry as any)[h])).join(','),
  );

  return [headerRow, ...dataRows].join('\n');
}

// ---------------------------------------------------------------------------
// GET /api/admin/audit/export
// ---------------------------------------------------------------------------

router.get('/export', async (req: Request, res: Response) => {
  try {
    // Auth check — admin only
    const user = (req as any).user;
    if (!user) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      return;
    }

    const adminRoles = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN', 'ORG_ADMIN'];
    if (!adminRoles.includes(user.role)) {
      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } });
      return;
    }

    // Parse query parameters
    const format = (req.query.format as string) || 'json';
    const fromDate = req.query.from as string;
    const toDate = req.query.to as string;
    const type: AuditType = (req.query.type as AuditType) || 'all';

    if (!['csv', 'json'].includes(format)) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Format must be "csv" or "json"' } });
      return;
    }

    if (!fromDate || !toDate) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Both "from" and "to" date parameters are required' } });
      return;
    }

    let formattedFrom: string;
    let formattedTo: string;

    try {
      formattedFrom = formatDate(fromDate);
      formattedTo = formatDate(toDate);
    } catch {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid date format. Use YYYY-MM-DD.' } });
      return;
    }

    // Fetch audit logs from security service
    const queryParams = new URLSearchParams({
      from: formattedFrom,
      to: formattedTo,
      type,
    });

    const authHeader = req.headers.authorization;
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (authHeader) headers['Authorization'] = authHeader;

    let entries: AuditEntry[] = [];

    try {
      const response = await fetch(
        `${SECURITY_SERVICE_URL}/api/audit/logs?${queryParams.toString()}`,
        { method: 'GET', headers },
      );

      if (response.ok) {
        const data = await response.json();
        entries = (data as any)?.data || (data as any)?.logs || [];
      } else {
        const errorData = await response.json().catch(() => ({}));
        res.status(response.status).json({
          success: false,
          error: {
            code: 'BAD_GATEWAY',
            message: (errorData as any)?.error || `Security service returned ${response.status}`,
          },
        });
        return;
      }
    } catch (err: any) {
      res.status(502).json({
        success: false,
        error: {
          code: 'BAD_GATEWAY',
          message: `Failed to reach security service: ${err.message}`,
        },
      });
      return;
    }

    // Generate filename
    const filename = `audit-logs_${formattedFrom}_${formattedTo}_${type}`;

    if (format === 'csv') {
      const csv = auditEntriesToCSV(entries);

      res.setHeader('Content-Type', 'text/csv; charset=utf-8');
      res.setHeader('Content-Disposition', `attachment; filename="${filename}.csv"`);
      res.send(csv);
      return;
    }

    // JSON format
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Content-Disposition', `attachment; filename="${filename}.json"`);
    res.json({
      success: true,
      meta: {
        from: formattedFrom,
        to: formattedTo,
        type,
        totalEntries: entries.length,
        exportedAt: new Date().toISOString(),
      },
      data: entries,
    });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
  }
});

export default router;
