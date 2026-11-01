/**
 * =============================================================================
 * METRICS COLLECTOR SERVICE
 * =============================================================================
 * Collects, stores, and aggregates metrics from all platform services
 * =============================================================================
 */

import { 
  MetricEvent, 
  EventCategory, 
  TimeSeriesDataPoint, 
  MetricSummary,
  AggregationOptions,
  AggregatedMetrics,
  TimeGranularity,
  DashboardOverview,
  DashboardCharts,
  ChartData,
} from '../types';
import { logger } from '../utils/logger';
import { query, isDbAvailable } from '../db';
import { format, subDays, eachDayOfInterval } from 'date-fns';
import { startOfUtcDay, endOfUtcDay } from '../utils/utcDate';

// =============================================================================
// IN-MEMORY STORAGE (Replace with TimescaleDB/InfluxDB in production)
// =============================================================================

interface MetricStore {
  events: MetricEvent[];
  counters: Map<string, number>;
  gauges: Map<string, number>;
  lastUpdated: Date;
}

export class MetricsCollector {
  private store: MetricStore;
  private maxEvents: number = 100000; // Max events in memory

  constructor() {
    this.store = {
      events: [],
      counters: new Map(),
      gauges: new Map(),
      lastUpdated: new Date(),
    };
    
    // Initialize counters
    this.initializeCounters();
    
    logger.info('MetricsCollector initialized');
  }

  private initializeCounters(): void {
    const counterNames = [
      'documents.created',
      'documents.certified',
      'documents.signed',
      'documents.anchored',
      'documents.transferred',
      'documents.revoked',
      'verifications.total',
      'verifications.successful',
      'verifications.failed',
      'users.registered',
      'users.active',
      'users.logins',
      'anchors.submitted',
      'anchors.confirmed',
      'anchors.failed',
      'api.requests',
      'api.errors',
    ];

    counterNames.forEach(name => this.store.counters.set(name, 0));
  }

  // ===========================================================================
  // EVENT TRACKING
  // ===========================================================================

  /**
   * Track a metric event
   */
  track(event: Omit<MetricEvent, 'id' | 'timestamp'>): void {
    const fullEvent: MetricEvent = {
      ...event,
      id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
    };

    // Add to events
    this.store.events.push(fullEvent);
    
    // Update counter
    const counterKey = `${event.category}.${event.action}`;
    const currentValue = this.store.counters.get(counterKey) || 0;
    this.store.counters.set(counterKey, currentValue + (event.value || 1));

    // Trim events if over limit
    if (this.store.events.length > this.maxEvents) {
      this.store.events = this.store.events.slice(-this.maxEvents);
    }

    this.store.lastUpdated = new Date();
    
    logger.debug('Event tracked', { category: event.category, action: event.action });
  }

  /**
   * Increment a counter
   */
  increment(key: string, value: number = 1): void {
    const current = this.store.counters.get(key) || 0;
    this.store.counters.set(key, current + value);
  }

  /**
   * Set a gauge value
   */
  setGauge(key: string, value: number): void {
    this.store.gauges.set(key, value);
  }

  /**
   * Get counter value
   */
  getCounter(key: string): number {
    return this.store.counters.get(key) || 0;
  }

  /**
   * Get gauge value
   */
  getGauge(key: string): number {
    return this.store.gauges.get(key) || 0;
  }

  // ===========================================================================
  // METRIC QUERIES
  // ===========================================================================

  /**
   * Get events by category within time range
   */
  getEvents(
    category: EventCategory,
    startDate: Date,
    endDate: Date,
    action?: string
  ): MetricEvent[] {
    return this.store.events.filter(event => {
      const inTimeRange = event.timestamp >= startDate && event.timestamp <= endDate;
      const matchesCategory = event.category === category;
      const matchesAction = action ? event.action === action : true;
      return inTimeRange && matchesCategory && matchesAction;
    });
  }

  /**
   * Get metric summary for a category
   */
  getSummary(
    category: EventCategory,
    startDate: Date,
    endDate: Date
  ): MetricSummary {
    const events = this.getEvents(category, startDate, endDate);
    
    // Get previous period for trend calculation
    const periodLength = endDate.getTime() - startDate.getTime();
    const previousStart = new Date(startDate.getTime() - periodLength);
    const previousEnd = startDate;
    const previousEvents = this.getEvents(category, previousStart, previousEnd);

    const total = events.reduce((sum, e) => sum + (e.value || 1), 0);
    const previousTotal = previousEvents.reduce((sum, e) => sum + (e.value || 1), 0);
    
    const change = total - previousTotal;
    const changePercent = previousTotal > 0 ? (change / previousTotal) * 100 : 0;

    // Breakdown by action
    const breakdown: Record<string, number> = {};
    events.forEach(event => {
      breakdown[event.action] = (breakdown[event.action] || 0) + (event.value || 1);
    });

    return {
      name: category,
      category,
      total,
      period: { start: startDate, end: endDate },
      breakdown,
      trend: {
        change,
        changePercent: Math.round(changePercent * 100) / 100,
        direction: change > 0 ? 'up' : change < 0 ? 'down' : 'stable',
      },
    };
  }

  /**
   * Get aggregated metrics over time
   */
  aggregate(
    category: EventCategory,
    options: AggregationOptions
  ): AggregatedMetrics {
    const events = this.getEvents(category, options.startDate, options.endDate);
    
    // Group by time granularity
    const dataPoints = this.groupByGranularity(events, options.granularity);
    
    const values = dataPoints.map(d => d.value);
    const total = values.reduce((sum, v) => sum + v, 0);
    
    return {
      granularity: options.granularity,
      data: dataPoints,
      total,
      average: values.length > 0 ? total / values.length : 0,
      min: values.length > 0 ? Math.min(...values) : 0,
      max: values.length > 0 ? Math.max(...values) : 0,
    };
  }

  private groupByGranularity(
    events: MetricEvent[],
    granularity: TimeGranularity
  ): TimeSeriesDataPoint[] {
    const grouped = new Map<string, number>();
    
    events.forEach(event => {
      const key = this.getTimeKey(event.timestamp, granularity);
      grouped.set(key, (grouped.get(key) || 0) + (event.value || 1));
    });

    return Array.from(grouped.entries())
      .map(([key, value]) => ({
        timestamp: new Date(key),
        value,
      }))
      .sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
  }

  private getTimeKey(date: Date, granularity: TimeGranularity): string {
    switch (granularity) {
      case 'hour':
        return format(date, 'yyyy-MM-dd HH:00');
      case 'day':
        return format(date, 'yyyy-MM-dd');
      case 'week':
        return format(date, "yyyy-'W'ww");
      case 'month':
        return format(date, 'yyyy-MM');
      case 'year':
        return format(date, 'yyyy');
      default:
        return format(date, 'yyyy-MM-dd');
    }
  }

  // ===========================================================================
  // DASHBOARD DATA
  // ===========================================================================

  /**
   * Get dashboard overview data
   */
  getDashboardOverview(): DashboardOverview {
    const today = new Date();
    const startOfToday = startOfUtcDay(today);
    const endOfToday = endOfUtcDay(today);

    // Document metrics
    const documentEvents = this.getEvents(EventCategory.DOCUMENT, startOfToday, endOfToday);
    const certifiedToday = documentEvents.filter(e => e.action === 'certified').length;

    // Verification metrics
    const verificationEvents = this.getEvents(EventCategory.VERIFICATION, startOfToday, endOfToday);
    const successfulVerifications = verificationEvents.filter(e => e.action === 'successful').length;
    const failedVerifications = verificationEvents.filter(e => e.action === 'failed').length;

    // User metrics
    const userEvents = this.getEvents(EventCategory.USER, startOfToday, endOfToday);
    const newUsersToday = userEvents.filter(e => e.action === 'registered').length;

    // Anchor metrics
    const anchorEvents = this.getEvents(EventCategory.ANCHOR, startOfToday, endOfToday);
    const anchorsConfirmed = anchorEvents.filter(e => e.action === 'confirmed').length;
    const anchorsFailed = anchorEvents.filter(e => e.action === 'failed').length;
    const anchorTotal = anchorsConfirmed + anchorsFailed;

    return {
      totalDocuments: this.getCounter('documents.created'),
      documentsCertifiedToday: certifiedToday,
      totalVerifications: this.getCounter('verifications.total'),
      verificationsToday: successfulVerifications + failedVerifications,
      activeUsers: this.getGauge('users.active') || 0,
      newUsersToday,
      anchorSuccessRate: anchorTotal > 0 ? (anchorsConfirmed / anchorTotal) * 100 : 100,
      anchorsToday: anchorTotal,
      systemHealth: {
        status: 'healthy',
        uptime: process.uptime(),
        responseTime: this.getGauge('api.responseTime') || 50,
      },
    };
  }

  /**
   * Get dashboard charts data
   */
  getDashboardCharts(days: number = 7): DashboardCharts {
    const endDate = new Date();
    const startDate = subDays(endDate, days);
    const interval = eachDayOfInterval({ start: startDate, end: endDate });

    // Documents by day
    const documentsByDay = this.getChartDataForCategory(
      EventCategory.DOCUMENT,
      interval,
      'Documents'
    );

    // Verifications by day
    const verificationsByDay = this.getChartDataForCategory(
      EventCategory.VERIFICATION,
      interval,
      'Verifications'
    );

    // User growth
    const userGrowth = this.getChartDataForCategory(
      EventCategory.USER,
      interval,
      'New Users',
      'registered'
    );

    // Anchors by network (pie chart data)
    const anchorsByNetwork: ChartData = {
      labels: ['Mainnet', 'Preprod', 'Preview'],
      datasets: [{
        label: 'Anchors',
        data: [
          this.getCounter('anchors.mainnet') || 0,
          this.getCounter('anchors.preprod') || 0,
          this.getCounter('anchors.preview') || 0,
        ],
        backgroundColor: ['#38a169', '#3182ce', '#805ad5'],
      }],
    };

    // Documents by type
    const documentsByType: ChartData = {
      labels: ['Certificate', 'Diploma', 'License', 'Permit', 'Deed', 'Other'],
      datasets: [{
        label: 'Documents',
        data: [
          this.getCounter('documents.type.certificate') || 0,
          this.getCounter('documents.type.diploma') || 0,
          this.getCounter('documents.type.license') || 0,
          this.getCounter('documents.type.permit') || 0,
          this.getCounter('documents.type.deed') || 0,
          this.getCounter('documents.type.other') || 0,
        ],
        backgroundColor: ['#38a169', '#3182ce', '#805ad5', '#d69e2e', '#e53e3e', '#718096'],
      }],
    };

    // Top organizations (mock data)
    const topOrganizations: ChartData = {
      labels: ['Org A', 'Org B', 'Org C', 'Org D', 'Org E'],
      datasets: [{
        label: 'Documents',
        data: [150, 120, 90, 75, 60],
        backgroundColor: '#3182ce',
      }],
    };

    return {
      documentsByDay,
      verificationsByDay,
      userGrowth,
      anchorsByNetwork,
      documentsByType,
      topOrganizations,
    };
  }

  private getChartDataForCategory(
    category: EventCategory,
    interval: Date[],
    label: string,
    action?: string
  ): ChartData {
    const data = interval.map(date => {
      const dayStart = startOfUtcDay(date);
      const dayEnd = endOfUtcDay(date);
      const events = this.getEvents(category, dayStart, dayEnd, action);
      return events.reduce((sum, e) => sum + (e.value || 1), 0);
    });

    return {
      labels: interval.map(d => format(d, 'MMM d')),
      datasets: [{
        label,
        data,
        borderColor: '#3182ce',
        backgroundColor: 'rgba(49, 130, 206, 0.1)',
      }],
    };
  }

  // ===========================================================================
  // UTILITY METHODS
  // ===========================================================================

  /**
   * Get all counters
   */
  getAllCounters(): Record<string, number> {
    return Object.fromEntries(this.store.counters);
  }

  /**
   * Get all gauges
   */
  getAllGauges(): Record<string, number> {
    return Object.fromEntries(this.store.gauges);
  }

  /**
   * Clear old events
   */
  pruneEvents(olderThan: Date): number {
    const originalLength = this.store.events.length;
    this.store.events = this.store.events.filter(e => e.timestamp >= olderThan);
    return originalLength - this.store.events.length;
  }

  /**
   * Get store stats
   */
  getStoreStats(): { eventCount: number; counterCount: number; gaugeCount: number; lastUpdated: Date } {
    return {
      eventCount: this.store.events.length,
      counterCount: this.store.counters.size,
      gaugeCount: this.store.gauges.size,
      lastUpdated: this.store.lastUpdated,
    };
  }

  // ===========================================================================
  // DATABASE PERSISTENCE LOADING
  // ===========================================================================

  async loadFromDb(): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      const result = await query<{
        id: string;
        type: string;
        action: string;
        metadata: Record<string, unknown> | null;
        timestamp: string;
      }>(
        `SELECT id, type, action, metadata, timestamp
         FROM svc_analytics_events
         ORDER BY timestamp DESC
         LIMIT $1`,
        [this.maxEvents],
      );
      for (const row of result.rows) {
        this.store.events.push({
          id: row.id,
          category: row.type as EventCategory,
          action: row.action,
          value: (row.metadata as any)?.value ?? 1,
          timestamp: new Date(row.timestamp),
          userId: (row.metadata as any)?.userId,
          organizationId: (row.metadata as any)?.organizationId,
          documentId: (row.metadata as any)?.documentId,
          metadata: row.metadata ?? undefined,
        });
      }
      logger.info('MetricsCollector loaded events from DB', { count: result.rows.length });
    } catch (err) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('MetricsCollector.loadFromDb failed — starting with empty store', {
        error: reason,
      });
    }
  }
}

// Singleton instance
export const metricsCollector = new MetricsCollector();
