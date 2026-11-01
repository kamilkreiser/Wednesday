/**
 * =============================================================================
 * ANALYTICS SERVICE
 * =============================================================================
 * Data aggregation and metrics calculation service
 */

import { v4 as uuidv4 } from 'uuid';
import {
  TimePeriod,
  PlatformOverview,
  CertificationMetrics,
  VerificationMetrics,
  GovernanceMetrics,
  RevenueMetrics,
  UserMetrics,
  RealTimeMetrics,
  ActivityEvent,
  AnalyticsQuery,
} from '../types/analytics.types';
import { query, isDbAvailable } from '../db';
import { logger } from '../utils/logger';

// =============================================================================
// MOCK DATA GENERATORS
// =============================================================================

function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomFloat(min: number, max: number, decimals: number = 2): number {
  return parseFloat((Math.random() * (max - min) + min).toFixed(decimals));
}

function generateTimeSeries(days: number, baseValue: number, variance: number): Array<{ date: string; value: number }> {
  const series: Array<{ date: string; value: number }> = [];
  const now = new Date();
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    
    series.push({
      date: date.toISOString().split('T')[0],
      value: Math.max(0, baseValue + randomInt(-variance, variance)),
    });
  }
  
  return series;
}

function getDaysForPeriod(period: TimePeriod): number {
  switch (period) {
    case 'hour': return 1;
    case 'day': return 1;
    case 'week': return 7;
    case 'month': return 30;
    case 'quarter': return 90;
    case 'year': return 365;
    case 'all': return 365;
    default: return 30;
  }
}

// =============================================================================
// ANALYTICS SERVICE
// =============================================================================

const IS_PRODUCTION = process.env.NODE_ENV === 'production';

export class AnalyticsService {
  private memActivityFeed: ActivityEvent[] = [];
  private maxActivityEvents = 1000;

  private async dbSaveActivityEvent(event: ActivityEvent): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(
        `INSERT INTO svc_analytics_events (id, type, action, actor_id, actor_name, actor_type, target_id, target_type, target_name, metadata, timestamp)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11) ON CONFLICT DO NOTHING`,
        [event.id, event.type, event.action,
         event.actor?.id || null, event.actor?.name || null, event.actor?.type || null,
         event.target?.id || null, event.target?.type || null, event.target?.name || null,
         JSON.stringify(event.metadata || {}), event.timestamp]
      );
    } catch { /* ignore */ }
  }

  constructor() {
    if (!IS_PRODUCTION) {
      this.generateMockActivity();
    }
  }

  // ===========================================================================
  // PLATFORM OVERVIEW
  // ===========================================================================

  async getPlatformOverview(analyticsQuery: AnalyticsQuery): Promise<PlatformOverview> {
    const period = analyticsQuery.period || 'month';

    if (IS_PRODUCTION) {
      logger.warn('getPlatformOverview: real DB aggregation not yet implemented — returning zeros');
      return {
        timestamp: new Date().toISOString(),
        period,
        users: { total: 0, active: 0, new: 0, growth: 0 },
        organizations: { total: 0, active: 0, new: 0 },
        certifications: { total: 0, issued: 0, revoked: 0, expired: 0, pending: 0 },
        verifications: { total: 0, successful: 0, failed: 0, averageTime: 0 },
        blockchain: { transactionsAnchored: 0, totalAnchorCost: 0, averageConfirmationTime: 0 },
        privacy: { zkProofsGenerated: 0, zkProofsVerified: 0, selectiveDisclosures: 0 },
      };
    }

    return {
      timestamp: new Date().toISOString(),
      period,
      
      users: {
        total: randomInt(5000, 10000),
        active: randomInt(2000, 5000),
        new: randomInt(100, 500),
        growth: randomFloat(5, 15),
      },
      
      organizations: {
        total: randomInt(200, 500),
        active: randomInt(150, 400),
        new: randomInt(10, 50),
      },
      
      certifications: {
        total: randomInt(50000, 100000),
        issued: randomInt(1000, 5000),
        revoked: randomInt(10, 100),
        expired: randomInt(50, 200),
        pending: randomInt(100, 500),
      },
      
      verifications: {
        total: randomInt(100000, 500000),
        successful: randomInt(95000, 490000),
        failed: randomInt(1000, 10000),
        averageTime: randomInt(50, 200),
      },
      
      blockchain: {
        transactionsAnchored: randomInt(10000, 50000),
        totalAnchorCost: randomFloat(100, 500),
        averageConfirmationTime: randomInt(20, 60),
      },
      
      privacy: {
        zkProofsGenerated: randomInt(5000, 20000),
        zkProofsVerified: randomInt(4000, 18000),
        selectiveDisclosures: randomInt(3000, 15000),
      },
    };
  }

  // ===========================================================================
  // CERTIFICATION METRICS
  // ===========================================================================

  async getCertificationMetrics(query: AnalyticsQuery): Promise<CertificationMetrics> {
    const period = query.period || 'month';
    const days = getDaysForPeriod(period);
    
    const timeSeries = generateTimeSeries(days, 150, 50);
    
    return {
      timestamp: new Date().toISOString(),
      period,
      
      totalIssued: randomInt(40000, 80000),
      totalRevoked: randomInt(500, 2000),
      totalExpired: randomInt(1000, 5000),
      totalActive: randomInt(35000, 70000),
      
      byType: {
        educational_degree: {
          issued: randomInt(15000, 30000),
          revoked: randomInt(100, 500),
          active: randomInt(14000, 28000),
        },
        employment_certificate: {
          issued: randomInt(10000, 25000),
          revoked: randomInt(200, 800),
          active: randomInt(9000, 23000),
        },
        professional_certification: {
          issued: randomInt(8000, 15000),
          revoked: randomInt(50, 200),
          active: randomInt(7500, 14000),
        },
        identity_document: {
          issued: randomInt(5000, 10000),
          revoked: randomInt(100, 400),
          active: randomInt(4500, 9000),
        },
      },
      
      topIssuers: [
        { issuerId: 'issuer-1', issuerName: 'University of Technology', count: randomInt(5000, 10000), percentage: randomFloat(10, 20) },
        { issuerId: 'issuer-2', issuerName: 'Global Corp HR', count: randomInt(3000, 7000), percentage: randomFloat(8, 15) },
        { issuerId: 'issuer-3', issuerName: 'Professional Institute', count: randomInt(2000, 5000), percentage: randomFloat(5, 12) },
        { issuerId: 'issuer-4', issuerName: 'State Education Board', count: randomInt(1500, 4000), percentage: randomFloat(4, 10) },
        { issuerId: 'issuer-5', issuerName: 'Tech Academy', count: randomInt(1000, 3000), percentage: randomFloat(3, 8) },
      ],
      
      timeSeries: timeSeries.map(t => ({
        date: t.date,
        issued: t.value,
        revoked: randomInt(1, 10),
        verified: t.value * randomInt(2, 5),
      })),
      
      averages: {
        timeToVerify: randomInt(100, 300),
        verificationsPerCert: randomFloat(2, 8),
        lifespan: randomInt(365, 1825),
      },
    };
  }

  // ===========================================================================
  // VERIFICATION METRICS
  // ===========================================================================

  async getVerificationMetrics(query: AnalyticsQuery): Promise<VerificationMetrics> {
    const period = query.period || 'month';
    const days = getDaysForPeriod(period);
    
    const total = randomInt(100000, 500000);
    const successful = Math.floor(total * randomFloat(0.95, 0.99));
    
    const timeSeries = generateTimeSeries(days, Math.floor(total / days), Math.floor(total / days / 4));
    
    return {
      timestamp: new Date().toISOString(),
      period,
      
      totalVerifications: total,
      successfulVerifications: successful,
      failedVerifications: total - successful,
      successRate: parseFloat(((successful / total) * 100).toFixed(2)),
      
      bySource: {
        api: Math.floor(total * 0.6),
        qrCode: Math.floor(total * 0.25),
        directLink: Math.floor(total * 0.1),
        widget: Math.floor(total * 0.05),
      },
      
      byVerifierType: {
        employer: Math.floor(total * 0.4),
        educational_institution: Math.floor(total * 0.25),
        government: Math.floor(total * 0.15),
        healthcare: Math.floor(total * 0.1),
        other: Math.floor(total * 0.1),
      },
      
      topVerifiers: [
        { verifierId: 'ver-1', verifierName: 'Major Employer Inc', count: randomInt(5000, 15000) },
        { verifierId: 'ver-2', verifierName: 'Recruitment Agency', count: randomInt(3000, 10000) },
        { verifierId: 'ver-3', verifierName: 'Background Check Co', count: randomInt(2000, 8000) },
        { verifierId: 'ver-4', verifierName: 'University Admissions', count: randomInt(1500, 6000) },
        { verifierId: 'ver-5', verifierName: 'Healthcare Provider', count: randomInt(1000, 4000) },
      ],
      
      timeSeries: timeSeries.map(t => ({
        date: t.date,
        total: t.value,
        successful: Math.floor(t.value * 0.97),
        failed: Math.floor(t.value * 0.03),
      })),
      
      performance: {
        averageResponseTime: randomInt(80, 150),
        p50ResponseTime: randomInt(50, 100),
        p95ResponseTime: randomInt(150, 300),
        p99ResponseTime: randomInt(300, 500),
      },
    };
  }

  // ===========================================================================
  // GOVERNANCE METRICS
  // ===========================================================================

  async getGovernanceMetrics(query: AnalyticsQuery): Promise<GovernanceMetrics> {
    const period = query.period || 'month';
    const days = getDaysForPeriod(period);
    
    const timeSeries = generateTimeSeries(days, 5, 3);
    
    return {
      timestamp: new Date().toISOString(),
      period,
      
      proposals: {
        total: randomInt(50, 150),
        active: randomInt(5, 15),
        passed: randomInt(30, 80),
        rejected: randomInt(10, 30),
        executed: randomInt(25, 70),
        cancelled: randomInt(2, 10),
      },
      
      voting: {
        totalVotes: randomInt(5000, 20000),
        uniqueVoters: randomInt(500, 2000),
        averageParticipation: randomFloat(40, 70),
        averageTurnout: randomFloat(30, 60),
      },
      
      byCategory: {
        platform_fees: { total: randomInt(10, 30), passed: randomInt(5, 20), rejected: randomInt(2, 10) },
        feature_addition: { total: randomInt(15, 40), passed: randomInt(10, 30), rejected: randomInt(3, 10) },
        parameter_change: { total: randomInt(8, 25), passed: randomInt(5, 18), rejected: randomInt(2, 7) },
        treasury: { total: randomInt(5, 15), passed: randomInt(3, 10), rejected: randomInt(1, 5) },
        general: { total: randomInt(10, 30), passed: randomInt(6, 20), rejected: randomInt(2, 10) },
      },
      
      topVoters: [
        { oderId: 'voter-1', voterName: 'Active Participant', voteCount: randomInt(50, 100), votingPower: randomInt(10000, 50000) },
        { oderId: 'voter-2', voterName: 'Major Stakeholder', voteCount: randomInt(40, 80), votingPower: randomInt(8000, 40000) },
        { oderId: 'voter-3', voterName: 'Community Member', voteCount: randomInt(30, 60), votingPower: randomInt(5000, 25000) },
        { oderId: 'voter-4', voterName: 'Early Adopter', voteCount: randomInt(25, 50), votingPower: randomInt(3000, 15000) },
        { oderId: 'voter-5', voterName: 'Regular Voter', voteCount: randomInt(20, 40), votingPower: randomInt(2000, 10000) },
      ],
      
      timeSeries: timeSeries.map(t => ({
        date: t.date,
        proposalsCreated: Math.max(0, t.value),
        votesCast: t.value * randomInt(50, 150),
        proposalsExecuted: Math.floor(t.value * 0.6),
      })),
    };
  }

  // ===========================================================================
  // REVENUE METRICS
  // ===========================================================================

  async getRevenueMetrics(query: AnalyticsQuery): Promise<RevenueMetrics> {
    const period = query.period || 'month';
    const days = getDaysForPeriod(period);
    
    const mrr = randomInt(50000, 150000);
    const previousMrr = mrr * randomFloat(0.85, 0.98);
    
    const timeSeries = generateTimeSeries(days, Math.floor(mrr / 30), Math.floor(mrr / 100));
    
    return {
      timestamp: new Date().toISOString(),
      period,
      currency: 'USD',
      
      revenue: {
        total: mrr * (days / 30),
        subscriptions: mrr * (days / 30) * 0.85,
        transactions: mrr * (days / 30) * 0.12,
        other: mrr * (days / 30) * 0.03,
      },
      
      mrr: {
        current: mrr,
        previous: previousMrr,
        growth: parseFloat((((mrr - previousMrr) / previousMrr) * 100).toFixed(2)),
      },
      
      arr: mrr * 12,
      
      byTier: {
        starter: { subscribers: randomInt(200, 500), revenue: randomInt(5000, 15000), churn: randomFloat(2, 5) },
        professional: { subscribers: randomInt(100, 300), revenue: randomInt(10000, 30000), churn: randomFloat(1, 3) },
        business: { subscribers: randomInt(20, 80), revenue: randomInt(10000, 40000), churn: randomFloat(0.5, 2) },
        enterprise: { subscribers: randomInt(5, 20), revenue: randomInt(5000, 20000), churn: randomFloat(0, 1) },
      },
      
      churn: {
        rate: randomFloat(2, 5),
        count: randomInt(10, 50),
        revenue: randomInt(1000, 5000),
      },
      
      timeSeries: timeSeries.map(t => ({
        date: t.date,
        revenue: t.value,
        newSubscriptions: randomInt(1, 10),
        cancellations: randomInt(0, 3),
      })),
      
      cohorts: [
        { cohort: '2025-10', initialUsers: 100, retainedUsers: 85, retentionRate: 85 },
        { cohort: '2025-11', initialUsers: 120, retainedUsers: 100, retentionRate: 83.3 },
        { cohort: '2025-12', initialUsers: 150, retainedUsers: 130, retentionRate: 86.7 },
        { cohort: '2026-01', initialUsers: 180, retainedUsers: 165, retentionRate: 91.7 },
      ],
    };
  }

  // ===========================================================================
  // USER METRICS
  // ===========================================================================

  async getUserMetrics(query: AnalyticsQuery): Promise<UserMetrics> {
    const period = query.period || 'month';
    const days = getDaysForPeriod(period);
    
    const total = randomInt(5000, 15000);
    const timeSeries = generateTimeSeries(days, Math.floor(total / days / 10), 5);
    
    return {
      timestamp: new Date().toISOString(),
      period,
      
      counts: {
        total,
        active: Math.floor(total * randomFloat(0.4, 0.6)),
        inactive: Math.floor(total * randomFloat(0.3, 0.5)),
        new: randomInt(100, 500),
      },
      
      byRole: {
        issuer: Math.floor(total * 0.15),
        holder: Math.floor(total * 0.7),
        verifier: Math.floor(total * 0.1),
        admin: Math.floor(total * 0.05),
      },
      
      activity: {
        dailyActiveUsers: randomInt(500, 2000),
        weeklyActiveUsers: randomInt(2000, 5000),
        monthlyActiveUsers: randomInt(4000, 10000),
        averageSessionDuration: randomInt(180, 600),
        averageActionsPerSession: randomFloat(5, 15),
      },
      
      engagement: {
        certificationsIssued: randomInt(1000, 5000),
        verificationsPerformed: randomInt(5000, 20000),
        proposalsCreated: randomInt(10, 50),
        votesCast: randomInt(500, 2000),
      },
      
      timeSeries: timeSeries.map(t => ({
        date: t.date,
        signups: t.value,
        activeUsers: t.value * randomInt(10, 30),
        churned: Math.floor(t.value * 0.1),
      })),
      
      byRegion: {
        'North America': Math.floor(total * 0.35),
        'Europe': Math.floor(total * 0.3),
        'Asia Pacific': Math.floor(total * 0.2),
        'Latin America': Math.floor(total * 0.1),
        'Other': Math.floor(total * 0.05),
      },
    };
  }

  // ===========================================================================
  // REAL-TIME METRICS
  // ===========================================================================

  async getRealTimeMetrics(): Promise<RealTimeMetrics> {
    return {
      timestamp: new Date().toISOString(),
      
      activeUsers: randomInt(100, 500),
      activeSessions: randomInt(150, 600),
      
      lastHour: {
        certifications: randomInt(10, 50),
        verifications: randomInt(100, 500),
        transactions: randomInt(5, 30),
        apiCalls: randomInt(5000, 20000),
      },
      
      systemHealth: {
        apiLatency: randomInt(50, 150),
        errorRate: randomFloat(0, 1),
        uptime: randomFloat(99.5, 99.99),
      },
      
      recentEvents: this.memActivityFeed.slice(0, 20).map(event => ({
        id: event.id,
        type: event.type,
        timestamp: event.timestamp,
        description: event.action,
        metadata: event.metadata,
      })),
    };
  }

  // ===========================================================================
  // ACTIVITY FEED
  // ===========================================================================

  async getActivityFeed(limit: number = 50, offset: number = 0): Promise<ActivityEvent[]> {
    return this.memActivityFeed.slice(offset, offset + limit);
  }

  addActivityEvent(event: Omit<ActivityEvent, 'id' | 'timestamp'>): void {
    const newEvent: ActivityEvent = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      ...event,
    };
    
    // Save to DB (fire and forget)
    this.dbSaveActivityEvent(newEvent).catch(() => {});
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
        actor_id: string | null;
        actor_name: string | null;
        actor_type: string | null;
        target_id: string | null;
        target_type: string | null;
        target_name: string | null;
        metadata: Record<string, unknown> | null;
        timestamp: string;
      }>(
        `SELECT * FROM svc_analytics_events
         ORDER BY timestamp DESC
         LIMIT $1`,
        [this.maxActivityEvents],
      );

      if (result.rows.length > 0) {
        this.memActivityFeed = result.rows.map(row => ({
          id: row.id,
          type: row.type as ActivityEvent['type'],
          action: row.action,
          timestamp: row.timestamp,
          actor: row.actor_id ? {
            id: row.actor_id,
            name: row.actor_name || '',
            type: (row.actor_type || 'user') as 'user' | 'organization' | 'system',
          } : undefined,
          target: row.target_id ? {
            id: row.target_id,
            type: row.target_type || '',
            name: row.target_name ?? undefined,
          } : undefined,
          metadata: row.metadata ?? undefined,
        }));
        logger.info('AnalyticsService loaded activity feed from DB', { count: result.rows.length });
      }
    } catch (err) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('AnalyticsService.loadFromDb failed — using mock data', {
        error: reason,
      });
    }
  }

  private generateMockActivity(): void {
    const eventTypes = [
      { type: 'certification' as const, actions: ['issued', 'verified', 'revoked'] },
      { type: 'verification' as const, actions: ['completed', 'failed'] },
      { type: 'user' as const, actions: ['registered', 'logged_in', 'updated_profile'] },
      { type: 'governance' as const, actions: ['proposal_created', 'vote_cast', 'proposal_executed'] },
      { type: 'transfer' as const, actions: ['initiated', 'approved', 'completed'] },
    ];

    for (let i = 0; i < 100; i++) {
      const eventType = eventTypes[randomInt(0, eventTypes.length - 1)];
      const action = eventType.actions[randomInt(0, eventType.actions.length - 1)];
      
      const timestamp = new Date();
      timestamp.setMinutes(timestamp.getMinutes() - randomInt(1, 1440)); // Last 24 hours
      
      const mockEvent: ActivityEvent = {
        id: uuidv4(),
        type: eventType.type,
        action,
        timestamp: timestamp.toISOString(),
        actor: {
          id: `user-${randomInt(1, 100)}`,
          name: `User ${randomInt(1, 100)}`,
          type: 'user',
        },
        target: {
          id: `target-${randomInt(1, 1000)}`,
          type: eventType.type,
        },
      };
      this.memActivityFeed.push(mockEvent);
    }

    // Sort by timestamp descending
    this.memActivityFeed.sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  }
}

// Singleton instance
export const analyticsService = new AnalyticsService();

export default analyticsService;
