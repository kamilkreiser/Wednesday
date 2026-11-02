/**
 * Session Routes
 * Session management endpoints
 */

import { Router, Response } from 'express';
import { AuthenticatedRequest } from '../types';
import { authenticate } from '../middleware/authenticate';
import { getUserSessions, revokeSession } from '../services/session';
import { NotFoundError, ForbiddenError } from '../middleware/errorHandler';
import { logger } from '../utils/logger';

export const sessionRoutes = Router();

/**
 * GET /api/sessions
 * List all active sessions for current user
 */
sessionRoutes.get('/', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const sessions = await getUserSessions(req.user!.userId);
    
    res.json({
      success: true,
      data: sessions.map(session => ({
        id: session.id,
        ipAddress: session.ipAddress,
        userAgent: session.userAgent,
        deviceId: session.deviceId,
        lastActivityAt: session.lastActivityAt,
        createdAt: session.createdAt,
        expiresAt: session.expiresAt,
        isCurrent: session.id === req.sessionId,
      })),
    });
  } catch (error) {
    next(error);
  }
});

/**
 * DELETE /api/sessions/:id
 * Revoke a specific session
 */
sessionRoutes.delete('/:id', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const { id } = req.params;
    
    // Prevent revoking current session through this endpoint
    if (id === req.sessionId) {
      throw new ForbiddenError('Cannot revoke current session. Use /api/auth/logout instead.');
    }
    
    // Get all user sessions to verify ownership
    const sessions = await getUserSessions(req.user!.userId);
    const session = sessions.find(s => s.id === id);
    
    if (!session) {
      throw new NotFoundError('Session');
    }
    
    await revokeSession(id);
    
    logger.info('Session revoked', { sessionId: id, userId: req.user!.userId });
    
    res.json({
      success: true,
      message: 'Session revoked successfully',
    });
  } catch (error) {
    next(error);
  }
});

/**
 * DELETE /api/sessions
 * Revoke all sessions except current
 */
sessionRoutes.delete('/', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const sessions = await getUserSessions(req.user!.userId);
    
    // Revoke all except current
    let revokedCount = 0;
    for (const session of sessions) {
      if (session.id !== req.sessionId) {
        await revokeSession(session.id);
        revokedCount++;
      }
    }
    
    logger.info('All other sessions revoked', {
      userId: req.user!.userId,
      revokedCount,
    });
    
    res.json({
      success: true,
      message: `${revokedCount} session(s) revoked`,
      data: {
        revokedCount,
      },
    });
  } catch (error) {
    next(error);
  }
});
