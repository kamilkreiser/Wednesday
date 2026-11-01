/**
 * =============================================================================
 * ANALYTICS API ROUTES
 * =============================================================================
 * REST API endpoints for analytics data
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { analyticsService } from '../services/analyticsService';
import { exportService } from '../services/exportService';
import {
  AnalyticsQuerySchema,
  ActivityQuerySchema,
  ExportRequestSchema,
  ReportRequestSchema,
} from '../types/analytics.types';
import { logger } from '../utils/logger';

const router = Router();

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================
// ExportRequestSchema / ReportRequestSchema live in types/analytics.types.ts
// (moved in KS-444) so they are unit-testable alongside the other request
// schemas — each mirrors its published schema in analytics.openapi.ts.

// =============================================================================
// PLATFORM OVERVIEW
// =============================================================================

/**
 * GET /api/analytics/overview
 * Get platform overview metrics
 */
router.get('/overview', async (req: Request, res: Response): Promise<void> => {
  try {
    const query = AnalyticsQuerySchema.parse(req.query);
    const overview = await analyticsService.getPlatformOverview(query);
    
    res.json({
      success: true,
      data: overview,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: error.errors },
      });
      return;
    }
    
    logger.error('Error fetching overview', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch overview metrics' },
    });
  }
});

// =============================================================================
// CERTIFICATION METRICS
// =============================================================================

/**
 * GET /api/analytics/certifications
 * Get certification metrics
 */
router.get('/certifications', async (req: Request, res: Response) => {
  try {
    const query = AnalyticsQuerySchema.parse(req.query);
    const metrics = await analyticsService.getCertificationMetrics(query);
    
    res.json({
      success: true,
      data: metrics,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: error.errors },
      });
    }
    
    logger.error('Error fetching certification metrics', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch certification metrics' },
    });
  }
});

// =============================================================================
// VERIFICATION METRICS
// =============================================================================

/**
 * GET /api/analytics/verifications
 * Get verification metrics
 */
router.get('/verifications', async (req: Request, res: Response) => {
  try {
    const query = AnalyticsQuerySchema.parse(req.query);
    const metrics = await analyticsService.getVerificationMetrics(query);
    
    res.json({
      success: true,
      data: metrics,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: error.errors },
      });
    }
    
    logger.error('Error fetching verification metrics', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch verification metrics' },
    });
  }
});

// =============================================================================
// GOVERNANCE METRICS
// =============================================================================

/**
 * GET /api/analytics/governance
 * Get governance metrics
 */
router.get('/governance', async (req: Request, res: Response) => {
  try {
    const query = AnalyticsQuerySchema.parse(req.query);
    const metrics = await analyticsService.getGovernanceMetrics(query);
    
    res.json({
      success: true,
      data: metrics,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: error.errors },
      });
    }
    
    logger.error('Error fetching governance metrics', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch governance metrics' },
    });
  }
});

// =============================================================================
// REVENUE METRICS
// =============================================================================

/**
 * GET /api/analytics/revenue
 * Get revenue metrics
 */
router.get('/revenue', async (req: Request, res: Response) => {
  try {
    const query = AnalyticsQuerySchema.parse(req.query);
    const metrics = await analyticsService.getRevenueMetrics(query);
    
    res.json({
      success: true,
      data: metrics,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: error.errors },
      });
    }
    
    logger.error('Error fetching revenue metrics', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch revenue metrics' },
    });
  }
});

// =============================================================================
// USER METRICS
// =============================================================================

/**
 * GET /api/analytics/users
 * Get user metrics
 */
router.get('/users', async (req: Request, res: Response) => {
  try {
    const query = AnalyticsQuerySchema.parse(req.query);
    const metrics = await analyticsService.getUserMetrics(query);
    
    res.json({
      success: true,
      data: metrics,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: error.errors },
      });
    }
    
    logger.error('Error fetching user metrics', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch user metrics' },
    });
  }
});

// =============================================================================
// REAL-TIME METRICS
// =============================================================================

/**
 * GET /api/analytics/realtime
 * Get real-time platform metrics
 */
router.get('/realtime', async (_req: Request, res: Response) => {
  try {
    const metrics = await analyticsService.getRealTimeMetrics();
    
    res.json({
      success: true,
      data: metrics,
    });
  } catch (error) {
    logger.error('Error fetching real-time metrics', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch real-time metrics' },
    });
  }
});

// =============================================================================
// ACTIVITY FEED
// =============================================================================

/**
 * GET /api/analytics/activity
 * Get activity feed
 */
router.get('/activity', async (req: Request, res: Response) => {
  try {
    // KS-267: validate + coerce limit/offset (reject wrong-type / out-of-range
    // with 400) instead of the old `parseInt(...) || 50` that swallowed junk.
    const { limit, offset } = ActivityQuerySchema.parse(req.query);

    const activity = await analyticsService.getActivityFeed(limit, offset);

    res.json({
      success: true,
      data: {
        events: activity,
        pagination: {
          limit,
          offset,
          hasMore: activity.length === limit,
        },
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: error.errors },
      });
      return;
    }

    logger.error('Error fetching activity', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch activity feed' },
    });
  }
});

// =============================================================================
// EXPORTS
// =============================================================================

/**
 * POST /api/analytics/exports
 * Create a new data export
 */
router.post('/exports', async (req: Request, res: Response) => {
  try {
    const request = ExportRequestSchema.parse(req.body);
    const exportResult = await exportService.createExport(request);
    
    res.status(202).json({
      success: true,
      data: exportResult,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid export request', details: error.errors },
      });
    }
    
    logger.error('Error creating export', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to create export' },
    });
  }
});

/**
 * GET /api/analytics/exports/:id
 * Get export status
 */
router.get('/exports/:id', async (req: Request, res: Response) => {
  try {
    const exportResult = await exportService.getExport(req.params.id);
    
    if (!exportResult) {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'Export not found' },
      });
    }
    
    res.json({
      success: true,
      data: exportResult,
    });
  } catch (error) {
    logger.error('Error fetching export', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch export' },
    });
  }
});

/**
 * GET /api/analytics/exports
 * List recent exports
 */
router.get('/exports', async (req: Request, res: Response) => {
  try {
    const limit = parseInt(req.query.limit as string) || 20;
    const exports = await exportService.listExports(limit);
    
    res.json({
      success: true,
      data: exports,
    });
  } catch (error) {
    logger.error('Error listing exports', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to list exports' },
    });
  }
});

// =============================================================================
// REPORTS
// =============================================================================

/**
 * POST /api/analytics/reports
 * Generate an analytics report
 */
router.post('/reports', async (req: Request, res: Response) => {
  try {
    const { type, period } = ReportRequestSchema.parse(req.body);
    const report = await exportService.generateReport(type, period);
    
    res.json({
      success: true,
      data: report,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Invalid report request', details: error.errors },
      });
    }
    
    logger.error('Error generating report', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to generate report' },
    });
  }
});

export default router;
