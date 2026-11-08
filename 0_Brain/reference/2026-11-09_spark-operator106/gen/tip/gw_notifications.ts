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
import { logger } from '../utils/logger';

const router = Router();

/**
 * KS-1410: the only place in this router that turns a caught error into a 500. The six route catch blocks below put
 * the thrown error's own text in the 500 body with NO NODE_ENV guard, so it reached the client in every environment,
 * production included. Same shape as originate's fail500 (KS-1334, KS-730): log the thrown text server-side with
 * the route named, answer the constant body.
 */
function fail500(res: Response, context: string, err: unknown): void {
  // KS-1346: was `String(err)`, which rendered a thrown non-Error object as "[object Object]" and lost
  // its content. Kam ruled 2026-09-27 that such a throw logs its TYPE and FIELD NAMES only. A thrown
  // Error still logs `.message`, and thrown text is still logged verbatim: neither is in this ticket.
  // KS-1771: describing the thrown value (a message getter, a Proxy trap, a revoked Proxy) and writing the log line (a logger that fails) can themselves throw. This line did both with no try of its
  // own, so such a throw escaped fail500 and the constant 500 below was never sent: these handlers are synchronous, so Express handed the throw to the gateway's errorHandler, which answered in
  // place of this route. Describe the value in its own try and log in another (the shape PR 1754 gave platform.ts, KS-1524 a). The line is unchanged for every value that could be described before.
  let described: string;
  try {
    described = err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err;
  } catch {
    described = 'thrown value that could not be described';
  }
  try {
    logger.error(context, { error: described });
  } catch {
    // Nothing more can be said if the logger itself fails; the caller still gets the 500 below.
  }
  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
}

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
    fail500(res, 'Notification list failed (GET /api/notifications)', err);
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
    fail500(res, 'Unread count failed (GET /api/notifications/unread/count)', err);
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
    fail500(res, 'Mark read failed (PATCH /api/notifications/:id/read)', err);
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
    fail500(res, 'Mark all read failed (PATCH /api/notifications/read-all)', err);
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
    fail500(res, 'Notification delete failed (DELETE /api/notifications/:id)', err);
  }
});

// ---------------------------------------------------------------------------
// POST /api/notifications — create a notification in the caller's own list
// KS-1448: this heading said "(internal)". No product code in this repo posts here, and any authenticated caller could.
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

    // KS-1448: a userId other than the caller's is refused, for every principal, platform admins and connector keys
    // included. Before this the row was stored under the body's userId with no check, so any authenticated caller could
    // place a `security` or `system` notification with an actionUrl in another user's inbox. It sits after the validators
    // so a malformed body keeps its 400, and it reads no store, so the answer does not depend on whether the target exists.
    // Own id only is narrower than "unless the caller is an admin" (ticket comment d457b6ed): no caller here needs an admin
    // arm, and adding one is a one-line change. Ruled by Wednesday, the fleet coordinator, 2026-11-06T07:01:24Z; not a Kam ruling.
    if (userId !== getUserId(req)) {
      res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'A notification can only be created for the authenticated caller' },
      });
      return;
    }

    const notification = createNotification(userId, type as Notification['type'], title, message, actionUrl);

    res.status(201).json({ success: true, data: notification });
  } catch (err: any) {
    fail500(res, 'Notification create failed (POST /api/notifications)', err);
  }
});

export default router;
