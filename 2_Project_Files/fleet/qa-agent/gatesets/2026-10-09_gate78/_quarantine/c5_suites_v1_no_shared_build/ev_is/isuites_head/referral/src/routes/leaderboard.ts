/**
 * =============================================================================
 * LEADERBOARD ROUTES
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { LeaderboardEntry } from '../types/referral.types';
import { createLogger } from '../utils/logger';
import { query, isDbAvailable } from '../db';

const router = Router();
const logger = createLogger('leaderboard-routes');

// In-memory leaderboard cache (use Redis in production)
interface LeaderboardCache {
  entries: LeaderboardEntry[];
  updatedAt: Date;
}

const leaderboardCache: {
  allTime: LeaderboardCache | null;
  monthly: LeaderboardCache | null;
} = {
  allTime: null,
  monthly: null,
};

const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

// =============================================================================
// ROUTES
// =============================================================================

/**
 * Get all-time referral leaderboard
 * GET /api/leaderboard
 */
router.get('/', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { limit = '50', page = '1' } = req.query;
    const limitNum = Math.min(parseInt(limit as string, 10), 100);
    const pageNum = parseInt(page as string, 10);

    // Check cache
    if (
      leaderboardCache.allTime &&
      Date.now() - leaderboardCache.allTime.updatedAt.getTime() < CACHE_TTL_MS
    ) {
      const startIndex = (pageNum - 1) * limitNum;
      const entries = leaderboardCache.allTime.entries.slice(startIndex, startIndex + limitNum);
      
      return res.json({
        success: true,
        data: {
          period: 'ALL_TIME',
          entries: entries.map(formatLeaderboardEntry),
          pagination: {
            page: pageNum,
            limit: limitNum,
            total: leaderboardCache.allTime.entries.length,
          },
          updatedAt: leaderboardCache.allTime.updatedAt,
        },
      });
    }

    // Rebuild leaderboard (in production, this would query database)
    const entries = await buildLeaderboard('ALL_TIME');
    leaderboardCache.allTime = {
      entries,
      updatedAt: new Date(),
    };

    const startIndex = (pageNum - 1) * limitNum;
    const paginatedEntries = entries.slice(startIndex, startIndex + limitNum);

    res.json({
      success: true,
      data: {
        period: 'ALL_TIME',
        entries: paginatedEntries.map(formatLeaderboardEntry),
        pagination: {
          page: pageNum,
          limit: limitNum,
          total: entries.length,
        },
        updatedAt: leaderboardCache.allTime.updatedAt,
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get monthly referral leaderboard
 * GET /api/leaderboard/monthly
 */
router.get('/monthly', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { limit = '50', page = '1', month } = req.query;
    const limitNum = Math.min(parseInt(limit as string, 10), 100);
    const pageNum = parseInt(page as string, 10);

    // Check cache (for current month only)
    const currentMonth = new Date().toISOString().slice(0, 7);
    const requestedMonth = month as string || currentMonth;

    if (
      requestedMonth === currentMonth &&
      leaderboardCache.monthly &&
      Date.now() - leaderboardCache.monthly.updatedAt.getTime() < CACHE_TTL_MS
    ) {
      const startIndex = (pageNum - 1) * limitNum;
      const entries = leaderboardCache.monthly.entries.slice(startIndex, startIndex + limitNum);
      
      return res.json({
        success: true,
        data: {
          period: 'MONTHLY',
          month: requestedMonth,
          entries: entries.map(formatLeaderboardEntry),
          pagination: {
            page: pageNum,
            limit: limitNum,
            total: leaderboardCache.monthly.entries.length,
          },
          updatedAt: leaderboardCache.monthly.updatedAt,
        },
      });
    }

    // Build monthly leaderboard
    const entries = await buildLeaderboard('MONTHLY', requestedMonth);
    
    if (requestedMonth === currentMonth) {
      leaderboardCache.monthly = {
        entries,
        updatedAt: new Date(),
      };
    }

    const startIndex = (pageNum - 1) * limitNum;
    const paginatedEntries = entries.slice(startIndex, startIndex + limitNum);

    res.json({
      success: true,
      data: {
        period: 'MONTHLY',
        month: requestedMonth,
        entries: paginatedEntries.map(formatLeaderboardEntry),
        pagination: {
          page: pageNum,
          limit: limitNum,
          total: entries.length,
        },
        updatedAt: new Date(),
        // Monthly prizes info
        prizes: {
          first: '5,000 SECURA',
          second: '2,500 SECURA',
          third: '1,000 SECURA',
          topTen: '500 SECURA each',
        },
      },
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Get user's position on leaderboard
 * GET /api/leaderboard/position/:userId
 */
router.get('/position/:userId', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId } = req.params;

    // Build leaderboard if not cached
    if (!leaderboardCache.allTime) {
      const entries = await buildLeaderboard('ALL_TIME');
      leaderboardCache.allTime = {
        entries,
        updatedAt: new Date(),
      };
    }

    const position = leaderboardCache.allTime.entries.findIndex(
      e => e.userId === userId
    );

    if (position === -1) {
      return res.json({
        success: true,
        data: {
          userId,
          ranked: false,
          message: 'You are not yet on the leaderboard. Refer users to get started!',
        },
      });
    }

    const entry = leaderboardCache.allTime.entries[position];
    const total = leaderboardCache.allTime.entries.length;

    res.json({
      success: true,
      data: {
        userId,
        ranked: true,
        position: position + 1,
        totalParticipants: total,
        percentile: ((total - position) / total * 100).toFixed(1),
        stats: formatLeaderboardEntry(entry),
        // Show nearby competitors
        nearby: {
          above: position > 0 
            ? formatLeaderboardEntry(leaderboardCache.allTime.entries[position - 1])
            : null,
          below: position < total - 1
            ? formatLeaderboardEntry(leaderboardCache.allTime.entries[position + 1])
            : null,
        },
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// HELPERS
// =============================================================================

async function buildLeaderboard(
  period: 'ALL_TIME' | 'MONTHLY',
  month?: string
): Promise<LeaderboardEntry[]> {
  if (!isDbAvailable()) {
    logger.warn('Leaderboard: DB not available');
    return [];
  }

  try {
    // Build date filter for monthly leaderboard
    let dateFilter = '';
    const params: unknown[] = [];

    if (period === 'MONTHLY' && month) {
      // month format: YYYY-MM
      dateFilter = 'AND r.created_at >= $1::date AND r.created_at < ($1::date + INTERVAL \'1 month\')';
      params.push(`${month}-01`);
    }

    const sql = `
      SELECT
        r.referrer_id AS user_id,
        COUNT(*) AS total_referrals,
        COUNT(*) FILTER (WHERE r.status IN ('QUALIFIED', 'REWARDED')) AS qualified_referrals,
        COALESCE(SUM(rw.amount), 0) AS total_rewards_earned,
        m.current_tier
      FROM svc_referrals r
      LEFT JOIN svc_referral_rewards rw ON rw.user_id = r.referrer_id AND rw.status IN ('CLAIMED', 'DISTRIBUTED')
      LEFT JOIN svc_referral_milestones m ON m.user_id = r.referrer_id
      WHERE 1=1 ${dateFilter}
      GROUP BY r.referrer_id, m.current_tier
      ORDER BY qualified_referrals DESC, total_referrals DESC
      LIMIT 100
    `;

    const result = await query(sql, params);

    return result.rows.map((row: any, index: number) => ({
      rank: index + 1,
      userId: row.user_id,
      displayName: `User ${row.user_id.substring(0, 8)}`,
      totalReferrals: Number(row.total_referrals),
      qualifiedReferrals: Number(row.qualified_referrals),
      totalRewardsEarned: BigInt(row.total_rewards_earned || 0),
      currentTier: (row.current_tier || 'starter').toUpperCase(),
      badge: getTierBadge((row.current_tier || 'starter').toUpperCase()),
    }));
  } catch (err: any) {
    logger.error('Leaderboard DB query failed', { error: err?.message });
    return [];
  }
}

function formatLeaderboardEntry(entry: LeaderboardEntry): object {
  return {
    rank: entry.rank,
    displayName: entry.displayName || `User ${entry.userId.substring(0, 8)}`,
    totalReferrals: entry.totalReferrals,
    qualifiedReferrals: entry.qualifiedReferrals,
    totalRewardsEarned: `${Number(entry.totalRewardsEarned) / 1_000_000} SECURA`,
    tier: entry.currentTier,
    badge: entry.badge || getTierBadge(entry.currentTier),
  };
}

function getTierBadge(tier: any): string {
  const badges: Record<string, string> = {
    FIRST_REFERRAL: '🌱',
    BRONZE: '🥉',
    SILVER: '🥈',
    GOLD: '🥇',
    PLATINUM: '💎',
    AMBASSADOR: '👑',
  };
  return badges[tier] || '';
}

export { router as leaderboardRoutes };
