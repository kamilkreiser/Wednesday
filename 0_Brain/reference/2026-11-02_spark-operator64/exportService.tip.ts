/**
 * =============================================================================
 * EXPORT SERVICE
 * =============================================================================
 * Handles data export and report generation
 */

import { v4 as uuidv4 } from 'uuid';
import {
  ExportRequest,
  ExportResult,
  ExportFormat,
  AnalyticsQuery,
} from '../types/analytics.types';
import { analyticsService } from './analyticsService';
import { query, isDbAvailable } from '../db';
import { logger } from '../utils/logger';

// =============================================================================
// EXPORT SERVICE
// =============================================================================

export class ExportService {
  private memExports: Map<string, ExportResult> = new Map();

  // ===========================================================================
  // DATABASE PERSISTENCE HELPERS
  // ===========================================================================

  private async dbSaveExport(exportResult: ExportResult): Promise<void> {
    this.memExports.set(exportResult.id, exportResult);

    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_analytics_exports (id, status, type, format, download_url, expires_at, created_at, completed_at, error)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) ON CONFLICT (id) DO UPDATE SET
         status = EXCLUDED.status,
         download_url = EXCLUDED.download_url,
         expires_at = EXCLUDED.expires_at,
         completed_at = EXCLUDED.completed_at,
         error = EXCLUDED.error`,
        [
          exportResult.id,
          exportResult.status,
          exportResult.type,
          exportResult.format,
          exportResult.downloadUrl || null,
          exportResult.expiresAt || null,
          exportResult.createdAt,
          exportResult.completedAt || null,
          exportResult.error || null,
        ]
      );
    } catch (err: any) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.info('DB save export failed', { error: reason });
    }
  }

  // ===========================================================================
  // CREATE EXPORT
  // ===========================================================================

  async createExport(request: ExportRequest): Promise<ExportResult> {
    const exportId = uuidv4();
    
    const exportResult: ExportResult = {
      id: exportId,
      status: 'pending',
      type: request.type,
      format: request.format,
      createdAt: new Date().toISOString(),
    };
    
    await this.dbSaveExport(exportResult);
    
    // Process export asynchronously
    this.processExport(exportId, request);
    
    return exportResult;
  }

  // ===========================================================================
  // GET EXPORT STATUS
  // ===========================================================================

  async getExport(exportId: string): Promise<ExportResult | null> {
    return this.memExports.get(exportId) || null;
  }

  // ===========================================================================
  // LIST EXPORTS
  // ===========================================================================

  async listExports(limit: number = 20): Promise<ExportResult[]> {
    const exports = Array.from(this.memExports.values());
    return exports.slice(0, limit).sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  // ===========================================================================
  // PROCESS EXPORT
  // ===========================================================================

  private async processExport(exportId: string, request: ExportRequest): Promise<void> {
    const exportResult = this.memExports.get(exportId);
    if (!exportResult) return;

    try {
      // Update status to processing
      exportResult.status = 'processing';
      await this.dbSaveExport(exportResult);

      // Get data based on type
      const query: AnalyticsQuery = {
        period: request.period,
        startDate: request.startDate,
        endDate: request.endDate,
      };

      let data: unknown;
      
      switch (request.type) {
        case 'certifications':
          data = await analyticsService.getCertificationMetrics(query);
          break;
        case 'verifications':
          data = await analyticsService.getVerificationMetrics(query);
          break;
        case 'users':
          data = await analyticsService.getUserMetrics(query);
          break;
        case 'governance':
          data = await analyticsService.getGovernanceMetrics(query);
          break;
        case 'revenue':
          data = await analyticsService.getRevenueMetrics(query);
          break;
        default:
          throw new Error(`Unknown export type: ${request.type}`);
      }

      // Convert to format
      const exportData = await this.convertToFormat(data, request.format);

      // In a real implementation, this would upload to S3/cloud storage
      // For now, we'll create a data URL
      const downloadUrl = this.createDownloadUrl(exportData, request.format);

      // Update export result
      exportResult.status = 'completed';
      exportResult.downloadUrl = downloadUrl;
      exportResult.completedAt = new Date().toISOString();
      exportResult.expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(); // 24 hours
      
      await this.dbSaveExport(exportResult);
    } catch (error) {
      exportResult.status = 'failed';
      exportResult.error = error instanceof Error ? error.message : 'Unknown error';
      await this.dbSaveExport(exportResult);
    }
  }

  // ===========================================================================
  // FORMAT CONVERSION
  // ===========================================================================

  private async convertToFormat(data: unknown, format: ExportFormat): Promise<string> {
    switch (format) {
      case 'json':
        return JSON.stringify(data, null, 2);
      
      case 'csv':
        return this.convertToCSV(data);
      
      case 'xlsx':
        // For XLSX, we'd use a library like exceljs
        // For now, return JSON
        return JSON.stringify(data, null, 2);

      case 'pdf':
        // KS-444: 'pdf' is in the published format enum (spec-is-contract). A
        // real renderer (e.g. pdfkit) is future work, so — like the xlsx
        // placeholder above — return the JSON payload so the export completes.
        return JSON.stringify(data, null, 2);

      default:
        return JSON.stringify(data, null, 2);
    }
  }

  private convertToCSV(data: unknown): string {
    if (!data || typeof data !== 'object') {
      return '';
    }

    const obj = data as Record<string, unknown>;
    const rows: string[] = [];

    // Flatten the object for CSV
    const flatData = this.flattenObject(obj);
    
    // Header row
    rows.push(Object.keys(flatData).join(','));
    
    // Data row
    rows.push(Object.values(flatData).map(v => {
      if (typeof v === 'string') {
        return `"${v.replace(/"/g, '""')}"`;
      }
      return String(v);
    }).join(','));

    return rows.join('\n');
  }

  private flattenObject(obj: Record<string, unknown>, prefix: string = ''): Record<string, unknown> {
    const result: Record<string, unknown> = {};
    
    for (const [key, value] of Object.entries(obj)) {
      const newKey = prefix ? `${prefix}_${key}` : key;
      
      if (value && typeof value === 'object' && !Array.isArray(value)) {
        Object.assign(result, this.flattenObject(value as Record<string, unknown>, newKey));
      } else if (Array.isArray(value)) {
        result[newKey] = JSON.stringify(value);
      } else {
        result[newKey] = value;
      }
    }
    
    return result;
  }

  private createDownloadUrl(data: string, format: ExportFormat): string {
    // In production, this would be a cloud storage URL
    // For development, we encode as base64
    const base64 = Buffer.from(data).toString('base64');
    const mimeType = this.getMimeType(format);
    return `data:${mimeType};base64,${base64}`;
  }

  private getMimeType(format: ExportFormat): string {
    switch (format) {
      case 'json':
        return 'application/json';
      case 'csv':
        return 'text/csv';
      case 'xlsx':
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      case 'pdf':
        // KS-444: honest content type — the payload behind it is the JSON
        // placeholder (see convertToFormat), so don't claim application/pdf.
        return 'application/octet-stream';
      default:
        return 'application/octet-stream';
    }
  }

  // ===========================================================================
  // DATABASE PERSISTENCE LOADING
  // ===========================================================================

  async loadFromDb(): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      const result = await query<{
        id: string;
        status: string;
        type: string;
        format: string;
        download_url: string | null;
        expires_at: string | null;
        created_at: string;
        completed_at: string | null;
        error: string | null;
      }>('SELECT * FROM svc_analytics_exports ORDER BY created_at DESC LIMIT 500');

      for (const row of result.rows) {
        const exportResult: ExportResult = {
          id: row.id,
          status: row.status as ExportResult['status'],
          type: row.type,
          format: row.format as ExportFormat,
          downloadUrl: row.download_url ?? undefined,
          expiresAt: row.expires_at ?? undefined,
          createdAt: row.created_at,
          completedAt: row.completed_at ?? undefined,
          error: row.error ?? undefined,
        };
        this.memExports.set(exportResult.id, exportResult);
      }
      logger.info('ExportService loaded exports from DB', { count: result.rows.length });
    } catch (err) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('ExportService.loadFromDb failed — starting with empty store', {
        error: reason,
      });
    }
  }

  // ===========================================================================
  // REPORT GENERATION
  // ===========================================================================

  async generateReport(
    type: 'summary' | 'detailed',
    period: string
  ): Promise<{
    title: string;
    generatedAt: string;
    sections: Array<{ title: string; content: unknown }>;
  }> {
    const query: AnalyticsQuery = { period: period as 'month' };

    const [overview, certifications, verifications, governance, revenue] = await Promise.all([
      analyticsService.getPlatformOverview(query),
      analyticsService.getCertificationMetrics(query),
      analyticsService.getVerificationMetrics(query),
      analyticsService.getGovernanceMetrics(query),
      analyticsService.getRevenueMetrics(query),
    ]);

    const sections = [
      {
        title: 'Executive Summary',
        content: {
          totalUsers: overview.users.total,
          activeUsers: overview.users.active,
          totalCertifications: certifications.totalActive,
          totalVerifications: verifications.totalVerifications,
          mrrGrowth: revenue.mrr.growth,
          successRate: verifications.successRate,
        },
      },
      {
        title: 'Certification Metrics',
        content: type === 'detailed' ? certifications : {
          totalActive: certifications.totalActive,
          issued: certifications.totalIssued,
          topIssuers: certifications.topIssuers.slice(0, 3),
        },
      },
      {
        title: 'Verification Metrics',
        content: type === 'detailed' ? verifications : {
          total: verifications.totalVerifications,
          successRate: verifications.successRate,
          performance: verifications.performance,
        },
      },
      {
        title: 'Governance Metrics',
        content: type === 'detailed' ? governance : {
          proposals: governance.proposals,
          participation: governance.voting.averageParticipation,
        },
      },
      {
        title: 'Revenue Metrics',
        content: type === 'detailed' ? revenue : {
          mrr: revenue.mrr.current,
          arr: revenue.arr,
          growth: revenue.mrr.growth,
          churnRate: revenue.churn.rate,
        },
      },
    ];

    return {
      title: `${type === 'detailed' ? 'Detailed' : 'Summary'} Analytics Report`,
      generatedAt: new Date().toISOString(),
      sections,
    };
  }
}

// Singleton instance
export const exportService = new ExportService();

export default exportService;
