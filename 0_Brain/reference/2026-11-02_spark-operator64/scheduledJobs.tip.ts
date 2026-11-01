/**
 * =============================================================================
 * SCHEDULED JOBS SERVICE
 * =============================================================================
 * Handles scheduled tasks like:
 * - Daily metric aggregation
 * - Weekly/monthly report generation
 * - Data cleanup and archiving
 * - Alert evaluation
 * =============================================================================
 */

import { CronJob } from 'cron';
import { MetricsCollector } from './metricsCollector';
import { ReportGenerator } from './reportGenerator';
import { ReportType, AlertRule, Alert, AlertSeverity } from '../types';
import { logger } from '../utils/logger';
import { subMonths, subDays } from 'date-fns';
import { startOfUtcMonth, endOfUtcMonth } from '../utils/utcDate';
import { query, isDbAvailable } from '../db';

// In-memory alert storage (with database persistence)
const memAlertRules: AlertRule[] = [];
const memActiveAlerts: Alert[] = [];

// =============================================================================
// DATABASE PERSISTENCE HELPERS
// =============================================================================

async function dbSaveAlertRule(rule: AlertRule): Promise<void> {
  // Add to memory if not already present
  if (!memAlertRules.find(r => r.id === rule.id)) {
    memAlertRules.push(rule);
  }
  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_alert_rules (id, name, metric, condition, threshold, severity, enabled, cooldown_minutes)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8) ON CONFLICT (id) DO UPDATE SET
       name = EXCLUDED.name,
       metric = EXCLUDED.metric,
       condition = EXCLUDED.condition,
       threshold = EXCLUDED.threshold,
       severity = EXCLUDED.severity,
       enabled = EXCLUDED.enabled,
       cooldown_minutes = EXCLUDED.cooldown_minutes`,
      [
        rule.id,
        rule.name,
        rule.metric,
        rule.condition,
        rule.threshold,
        rule.severity,
        rule.enabled,
        rule.cooldownMinutes,
      ]
    );
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.info('DB save alert rule failed', { error: reason });
  }
}

async function dbSaveAlert(alert: Alert): Promise<void> {
  memActiveAlerts.push(alert);
  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_active_alerts (id, rule_id, severity, message, value, threshold, triggered_at, acknowledged_at, resolved_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) ON CONFLICT (id) DO UPDATE SET
       acknowledged_at = EXCLUDED.acknowledged_at,
       resolved_at = EXCLUDED.resolved_at`,
      [
        alert.id,
        alert.ruleId,
        alert.severity,
        alert.message,
        alert.value,
        alert.threshold,
        alert.triggeredAt,
        alert.acknowledgedAt || null,
        alert.resolvedAt || null,
      ]
    );
  } catch (err: any) {
    logger.info('DB save alert failed', { error: err instanceof Error ? err.message : String(err) });
  }
}

// =============================================================================
// DATABASE PERSISTENCE LOADING
// =============================================================================

export async function loadScheduledJobsFromDb(): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    const rulesResult = await query<{
      id: string;
      name: string;
      metric: string;
      condition: string;
      threshold: number;
      severity: string;
      enabled: boolean;
      cooldown_minutes: number;
    }>('SELECT * FROM svc_alert_rules');

    for (const row of rulesResult.rows) {
      if (!memAlertRules.find(r => r.id === row.id)) {
        memAlertRules.push({
          id: row.id,
          name: row.name,
          metric: row.metric,
          condition: row.condition as AlertRule['condition'],
          threshold: row.threshold,
          severity: row.severity as AlertSeverity,
          enabled: row.enabled,
          cooldownMinutes: row.cooldown_minutes,
        });
      }
    }
    logger.info('ScheduledJobs loaded alert rules from DB', { count: rulesResult.rows.length });

    const alertsResult = await query<{
      id: string;
      rule_id: string;
      severity: string;
      message: string;
      value: number;
      threshold: number;
      triggered_at: string;
      acknowledged_at: string | null;
      resolved_at: string | null;
    }>('SELECT * FROM svc_active_alerts ORDER BY triggered_at DESC LIMIT 500');

    for (const row of alertsResult.rows) {
      memActiveAlerts.push({
        id: row.id,
        ruleId: row.rule_id,
        severity: row.severity as AlertSeverity,
        message: row.message,
        value: row.value,
        threshold: row.threshold,
        triggeredAt: new Date(row.triggered_at),
        acknowledgedAt: row.acknowledged_at ? new Date(row.acknowledged_at) : undefined,
        resolvedAt: row.resolved_at ? new Date(row.resolved_at) : undefined,
      });
    }
    logger.info('ScheduledJobs loaded active alerts from DB', { count: alertsResult.rows.length });
  } catch (err) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('loadScheduledJobsFromDb failed — starting with defaults only', {
      error: reason,
    });
  }
}

export class ScheduledJobs {
  private metricsCollector: MetricsCollector;
  private reportGenerator: ReportGenerator;
  private jobs: CronJob[] = [];

  constructor(metricsCollector: MetricsCollector, reportGenerator: ReportGenerator) {
    this.metricsCollector = metricsCollector;
    this.reportGenerator = reportGenerator;
    this.initializeDefaultAlertRules();
    logger.info('ScheduledJobs initialized');
  }

  /**
   * Start all scheduled jobs
   */
  start(): void {
    // Daily metrics aggregation - every day at midnight
    this.addJob('0 0 * * *', () => this.dailyAggregation(), 'Daily Aggregation');

    // Weekly report - every Monday at 6 AM
    this.addJob('0 6 * * 1', () => this.generateWeeklyReport(), 'Weekly Report');

    // Monthly report - 1st of every month at 6 AM
    this.addJob('0 6 1 * *', () => this.generateMonthlyReport(), 'Monthly Report');

    // Data cleanup - every day at 3 AM
    this.addJob('0 3 * * *', () => this.dataCleanup(), 'Data Cleanup');

    // Alert evaluation - every 5 minutes
    this.addJob('*/5 * * * *', () => this.evaluateAlerts(), 'Alert Evaluation');

    // Active user gauge update - every minute
    this.addJob('* * * * *', () => this.updateActiveUsers(), 'Active Users Update');

    logger.info(`Started ${this.jobs.length} scheduled jobs`);
  }

  /**
   * Stop all scheduled jobs
   */
  stop(): void {
    this.jobs.forEach(job => job.stop());
    this.jobs = [];
    logger.info('All scheduled jobs stopped');
  }

  private addJob(cronTime: string, onTick: () => void, name: string): void {
    try {
      const job = new CronJob(cronTime, () => {
        logger.info(`Running job: ${name}`);
        try {
          onTick();
          logger.info(`Job completed: ${name}`);
        } catch (error) {
          logger.error(`Job failed: ${name}`, { error });
        }
      });
      job.start();
      this.jobs.push(job);
    } catch (error) {
      logger.error(`Failed to create job: ${name}`, { error });
    }
  }

  // ===========================================================================
  // JOB IMPLEMENTATIONS
  // ===========================================================================

  /**
   * Daily metrics aggregation
   */
  private dailyAggregation(): void {
    const today = new Date();
    const yesterday = subDays(today, 1);

    logger.info('Running daily aggregation', { date: yesterday.toISOString() });

    // Update daily counters
    // In production, this would write to a time-series database
    const stats = this.metricsCollector.getStoreStats();
    logger.info('Daily stats', stats);
  }

  /**
   * Generate weekly report
   */
  private generateWeeklyReport(): void {
    const endDate = new Date();
    const startDate = subDays(endDate, 7);

    this.reportGenerator.generateReport({
      type: ReportType.USAGE,
      startDate,
      endDate,
    }).then(report => {
      logger.info('Weekly report generated', { reportId: report.id });
      // In production, send via email or store in S3
    }).catch(error => {
      logger.error('Failed to generate weekly report', { error });
    });
  }

  /**
   * Generate monthly report
   */
  private generateMonthlyReport(): void {
    const lastMonth = subMonths(new Date(), 1);
    const startDate = startOfUtcMonth(lastMonth);
    const endDate = endOfUtcMonth(lastMonth);

    this.reportGenerator.generateReport({
      type: ReportType.MONTHLY,
      startDate,
      endDate,
    }).then(report => {
      logger.info('Monthly report generated', { reportId: report.id });
      // In production, send via email or store in S3
    }).catch(error => {
      logger.error('Failed to generate monthly report', { error });
    });

    // Also generate compliance report
    this.reportGenerator.generateReport({
      type: ReportType.COMPLIANCE,
      startDate,
      endDate,
    }).then(report => {
      logger.info('Compliance report generated', { reportId: report.id });
    }).catch(error => {
      logger.error('Failed to generate compliance report', { error });
    });
  }

  /**
   * Data cleanup - prune old events
   */
  private dataCleanup(): void {
    const retentionDays = parseInt(process.env.METRICS_RETENTION_DAYS || '90', 10);
    const cutoffDate = subDays(new Date(), retentionDays);

    const pruned = this.metricsCollector.pruneEvents(cutoffDate);
    logger.info('Data cleanup completed', { prunedEvents: pruned, retentionDays });
  }

  /**
   * Update active users gauge
   */
  private updateActiveUsers(): void {
    // In production, this would query Redis/DB for active sessions
    // For now, use a mock value
    const activeUsers = Math.floor(Math.random() * 50) + 10;
    this.metricsCollector.setGauge('users.active', activeUsers);
  }

  // ===========================================================================
  // ALERT SYSTEM
  // ===========================================================================

  private initializeDefaultAlertRules(): void {
    const defaultRules: AlertRule[] = [
      {
        id: 'high-error-rate',
        name: 'High API Error Rate',
        metric: 'api.errors',
        condition: 'gt',
        threshold: 100,
        severity: AlertSeverity.ERROR,
        enabled: true,
        cooldownMinutes: 15,
      },
      {
        id: 'anchor-failures',
        name: 'Blockchain Anchor Failures',
        metric: 'anchors.failed',
        condition: 'gt',
        threshold: 5,
        severity: AlertSeverity.WARNING,
        enabled: true,
        cooldownMinutes: 30,
      },
      {
        id: 'low-success-rate',
        name: 'Low Verification Success Rate',
        metric: 'verifications.failed',
        condition: 'gt',
        threshold: 50,
        severity: AlertSeverity.WARNING,
        enabled: true,
        cooldownMinutes: 60,
      },
      {
        id: 'suspicious-activity',
        name: 'Suspicious Activity Detected',
        metric: 'security.suspicious',
        condition: 'gt',
        threshold: 0,
        severity: AlertSeverity.CRITICAL,
        enabled: true,
        cooldownMinutes: 5,
      },
    ];
    
    // Save default rules to memory and DB
    defaultRules.forEach(rule => {
      dbSaveAlertRule(rule).catch(() => {});
    });
  }

  /**
   * Evaluate all alert rules
   */
  private evaluateAlerts(): void {
    const now = new Date();

    memAlertRules.filter(rule => rule.enabled).forEach(rule => {
      const value = this.metricsCollector.getCounter(rule.metric);
      const shouldAlert = this.checkCondition(value, rule.condition, rule.threshold);

      if (shouldAlert) {
        // Check cooldown
        const existingAlert = memActiveAlerts.find(
          (a: any) => a.ruleId === rule.id && !a.resolvedAt
        );

        if (existingAlert) {
          const cooldownEnd = new Date(
            existingAlert.triggeredAt.getTime() + rule.cooldownMinutes * 60 * 1000
          );
          if (now < cooldownEnd) {
            return; // Still in cooldown
          }
        }

        // Create new alert
        const alert: Alert = {
          id: `alert_${Date.now()}_${rule.id}`,
          ruleId: rule.id,
          severity: rule.severity,
          message: `${rule.name}: ${value} exceeds threshold of ${rule.threshold}`,
          value,
          threshold: rule.threshold,
          triggeredAt: now,
        };

        memActiveAlerts.push(alert);
        this.notifyAlert(alert, rule);
      } else {
        // Resolve any existing alerts for this rule
        memActiveAlerts
          .filter((a: any) => a.ruleId === rule.id && !a.resolvedAt)
          .forEach((a: any) => {
            a.resolvedAt = now;
            logger.info('Alert resolved', { alertId: a.id, rule: rule.name });
          });
      }
    });
  }

  private checkCondition(value: number, condition: string, threshold: number): boolean {
    switch (condition) {
      case 'gt': return value > threshold;
      case 'lt': return value < threshold;
      case 'eq': return value === threshold;
      case 'gte': return value >= threshold;
      case 'lte': return value <= threshold;
      default: return false;
    }
  }

  private notifyAlert(alert: Alert, rule: AlertRule): void {
    logger.warn('ALERT TRIGGERED', {
      alertId: alert.id,
      rule: rule.name,
      severity: alert.severity,
      message: alert.message,
      value: alert.value,
      threshold: alert.threshold,
    });

    // In production, send to:
    // - PagerDuty/OpsGenie
    // - Slack/Teams
    // - Email
    // - SMS for critical alerts
  }

  // ===========================================================================
  // PUBLIC METHODS
  // ===========================================================================

  /**
   * Get all alert rules
   */
  getAlertRules(): AlertRule[] {
    return [...memAlertRules];
  }

  /**
   * Get active alerts
   */
  getActiveAlerts(): Alert[] {
    return memActiveAlerts.filter(a => !a.resolvedAt);
  }

  /**
   * Get all alerts (including resolved)
   */
  getAllAlerts(limit: number = 100): Alert[] {
    return memActiveAlerts.slice(-limit);
  }

  /**
   * Acknowledge an alert
   */
  acknowledgeAlert(alertId: string): boolean {
    const alert = memActiveAlerts.find(a => a.id === alertId);
    if (alert && !alert.acknowledgedAt) {
      alert.acknowledgedAt = new Date();
      dbSaveAlert(alert).catch(() => {});
      logger.info('Alert acknowledged', { alertId });
      return true;
    }
    return false;
  }

  /**
   * Add a custom alert rule
   */
  addAlertRule(rule: AlertRule): void {
    dbSaveAlertRule(rule).catch(() => {});
    logger.info('Alert rule added', { ruleId: rule.id, name: rule.name });
  }

  /**
   * Remove an alert rule
   */
  removeAlertRule(ruleId: string): boolean {
    const index = memAlertRules.findIndex(r => r.id === ruleId);
    if (index !== -1) {
      memAlertRules.splice(index, 1);
      logger.info('Alert rule removed', { ruleId });
      return true;
    }
    return false;
  }

  /**
   * Manually trigger a report generation
   */
  async triggerReport(type: ReportType): Promise<string> {
    const endDate = new Date();
    let startDate: Date;

    switch (type) {
      case ReportType.MONTHLY:
        startDate = startOfUtcMonth(subMonths(endDate, 1));
        break;
      default:
        startDate = subDays(endDate, 7);
    }

    const report = await this.reportGenerator.generateReport({
      type,
      startDate,
      endDate,
    });

    return report.id;
  }
}
