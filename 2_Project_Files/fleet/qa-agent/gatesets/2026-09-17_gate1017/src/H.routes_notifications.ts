/**
 * =============================================================================
 * NOTIFICATION ROUTES
 * =============================================================================
 * Notification management router for user-facing notification CRUD.
 *
 * Usage in index.ts:
 *   import notificationRouter, { createNotification } from './routes/notifications';
 *   app.use('/api/notifications', notificationRouter);
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import crypto from 'crypto';
import { authenticateToken } from '../middleware/auth';

const router = Router();

// KS-375: every notifications operation is documented as bearer-authed
// (api-gateway.openapi.ts). Enforce it router-wide — without this, POST /
// accepted unauthenticated writes for arbitrary userIds, and the per-route
// req.user guards below always 401'd real tokens because nothing decoded them.
router.use(authenticateToken(true));

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface Notification {
  id: string;
  userId: string;
  type: 'purchase' | 'certification' | 'verification' | 'transfer' | 'security' | 'system';
  title: string;
  message: string;
  read: boolean;
  actionUrl?: string;
  createdAt: string;
}

// ---------------------------------------------------------------------------
// In-memory store (backed by notification service in production)
// ---------------------------------------------------------------------------

const notifications = new Map<string, Notification[]>();

// ---------------------------------------------------------------------------
// Helper — create a notification programmatically
// ---------------------------------------------------------------------------

export function createNotification(
  userId: string,
  type: Notification['type'],
  title: string,
  message: string,
  actionUrl?: string,
): Notification {
  const notification: Notification = {
    id: crypto.randomUUID(),
    userId,
    type,
    title,
    message,
    read: false,
    actionUrl,
    createdAt: new Date().toISOString(),
  };

  const userNotifications = notifications.get(userId) || [];
  userNotifications.unshift(notification);
  notifications.set(userId, userNotifications);

  return notification;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function getUserId(req: Request): string | null {
  return (req as any).user?.userId || null;
}

// ---------------------------------------------------------------------------
// GET /api/notifications — list user's notifications
// ---------------------------------------------------------------------------

router.get('/', (req: Request, res: Response) => {
  try {
    const userId = getUserId(req);
    if (!userId) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      return;
    }

    const userNotifications = notifications.get(userId) || [];

    // Optional query filters
    const { type, read, limit = '50', offset = '0' } = req.query;

    let filtered = [...userNotifications];

    if (type && typeof type === 'string') {
      filtered = filtered.filter((n) => n.type === type);
    }

    if (read !== undefined) {
      const isRead = read === 'true';
      filtered = filtered.filter((n) => n.read === isRead);
    }

    const limitNum = Math.min(parseInt(String(limit), 10) || 50, 200);
    const offsetNum = parseInt(String(offset), 10) || 0;

    const paginated = filtered.slice(offsetNum, offsetNum + limitNum);

    res.json({
      success: true,
      data: paginated,
      pagination: {
        total: filtered.length,
        limit: limitNum,
        offset: offsetNum,
      },
    });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
  }
});

// ---------------------------------------------------------------------------
// GET /api/notifications/unread/count — count of unread notifications
// ---------------------------------------------------------------------------

router.get('/unread/count', (req: Request, res: Response) => {
  try {
    const userId = getUserId(req);
    if (!userId) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      return;
    }

    const userNotifications = notifications.get(userId) || [];
    const unreadCount = userNotifications.filter((n) => !n.read).length;

    res.json({ success: true, data: { unreadCount } });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
  }
});

// ---------------------------------------------------------------------------
// PATCH /api/notifications/:id/read — mark a single notification as read
// ---------------------------------------------------------------------------

router.patch('/:id/read', (req: Request, res: Response) => {
  try {
    const userId = getUserId(req);
    if (!userId) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      return;
    }

    const { id } = req.params;
    const userNotifications = notifications.get(userId) || [];
    const notification = userNotifications.find((n) => n.id === id);

    if (!notification) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Notification not found' } });
      return;
    }

    notification.read = true;

    res.json({ success: true, data: notification });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
  }
});

// ---------------------------------------------------------------------------
// PATCH /api/notifications/read-all — mark all notifications as read
// ---------------------------------------------------------------------------

router.patch('/read-all', (req: Request, res: Response) => {
  try {
    const userId = getUserId(req);
    if (!userId) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      return;
    }

    const userNotifications = notifications.get(userId) || [];
    let updatedCount = 0;

    for (const n of userNotifications) {
      if (!n.read) {
        n.read = true;
        updatedCount++;
      }
    }

    res.json({ success: true, data: { updatedCount } });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
  }
});

// ---------------------------------------------------------------------------
// DELETE /api/notifications/:id — delete a notification
// ---------------------------------------------------------------------------

router.delete('/:id', (req: Request, res: Response) => {
  try {
    const userId = getUserId(req);
    if (!userId) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      return;
    }

    const { id } = req.params;
    const userNotifications = notifications.get(userId) || [];
    const index = userNotifications.findIndex((n) => n.id === id);

    if (index === -1) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Notification not found' } });
      return;
    }

    userNotifications.splice(index, 1);
    notifications.set(userId, userNotifications);

    res.json({ success: true, message: 'Notification deleted' });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
  }
});

// ---------------------------------------------------------------------------
// POST /api/notifications (internal) — create a notification
// ---------------------------------------------------------------------------

router.post('/', (req: Request, res: Response) => {
  try {
    const { userId, type, title, message, actionUrl } = req.body;

    // KS-498: enforce the published string types, not just truthiness — a
    // truthy non-string (e.g. `message: {}`) previously passed this guard,
    // was stored verbatim, and every subsequent read violated the published
    // NotificationItem response schema.
    // `data` is published as an object — reject arrays/scalars so a
    // schema-violating payload doesn't silently pass (KS-498 follow-up).
    const dataField = req.body?.data;
    if (
      typeof userId !== 'string' || !userId ||
      typeof type !== 'string' || !type ||
      typeof title !== 'string' || !title ||
      typeof message !== 'string' || !message ||
      (actionUrl !== undefined && typeof actionUrl !== 'string') ||
      (dataField !== undefined && (typeof dataField !== 'object' || dataField === null || Array.isArray(dataField)))
    ) {
      res.status(400).json({
        success: false,
        error: {
          code: 'BAD_REQUEST',
          message: 'Missing or non-string required fields: userId, type, title, message',
        },
      });
      return;
    }

    const validTypes: Notification['type'][] = [
      'purchase', 'certification', 'verification', 'transfer', 'security', 'system',
    ];

    if (!(validTypes as string[]).includes(type)) {
      res.status(400).json({
        success: false,
        error: {
          code: 'BAD_REQUEST',
          message: `Invalid notification type. Must be one of: ${validTypes.join(', ')}`,
        },
      });
      return;
    }

    const notification = createNotification(userId, type as Notification['type'], title, message, actionUrl);

    res.status(201).json({ success: true, data: notification });
  } catch (err: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message || 'Internal server error' } });
  }
});

export default router;
