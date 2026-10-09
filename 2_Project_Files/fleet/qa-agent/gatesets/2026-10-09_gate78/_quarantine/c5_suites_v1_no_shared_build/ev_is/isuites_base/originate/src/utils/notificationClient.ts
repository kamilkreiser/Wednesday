/**
 * =============================================================================
 * NOTIFICATION CLIENT — Fire-and-forget lifecycle notifications
 * =============================================================================
 * Sends notification requests to the notification microservice.
 * All calls are non-blocking: failures are logged but never thrown.
 * =============================================================================
 */

import { logger } from './logger';
import {
  sendEmail,
  sendCertificationNotification,
  sendRevocationNotification,
  sendShareNotification,
  isEmailConfigured,
} from '../services/email';

const NOTIFICATION_URL =
  process.env.NOTIFICATION_SERVICE_URL || 'http://notification:3008/api/notifications';

interface NotificationPayload {
  to: string;
  template: string;
  data: Record<string, unknown>;
}

/**
 * Send a notification email via the notification service.
 * Falls back to direct SMTP if the notification service is unreachable.
 * Fire-and-forget: errors are logged but never propagated.
 */
async function sendNotification(payload: NotificationPayload): Promise<void> {
  try {
    const res = await fetch(`${NOTIFICATION_URL}/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(5000),
    });

    if (!res.ok) {
      const body = await res.text().catch(() => 'unknown');
      logger.warn('Notification service returned non-OK, falling back to SMTP', {
        status: res.status,
        body: body.substring(0, 200),
        template: payload.template,
      });
      await sendSmtpFallback(payload);
    } else {
      logger.info('Notification sent via service', { template: payload.template, to: payload.to });
    }
  } catch (err) {
    logger.warn('Notification service unreachable, falling back to SMTP', {
      template: payload.template,
      error: String(err),
    });
    await sendSmtpFallback(payload);
  }
}

/**
 * SMTP fallback: send email directly when the notification microservice is unavailable.
 */
async function sendSmtpFallback(payload: NotificationPayload): Promise<void> {
  if (!isEmailConfigured()) {
    logger.info('SMTP not configured — notification skipped', { template: payload.template, to: payload.to });
    return;
  }

  try {
    const { to, template, data } = payload;

    switch (template) {
      case 'document_certified':
        await sendCertificationNotification(
          to,
          (data.documentTitle as string) || 'Untitled',
          (data.certifierName as string) || 'Unknown',
        );
        break;
      case 'document_revoked':
        await sendRevocationNotification(
          to,
          (data.documentTitle as string) || 'Untitled',
          (data.reason as string) || 'No reason provided',
        );
        break;
      case 'document_shared':
        await sendShareNotification(
          to,
          (data.documentTitle as string) || 'Untitled',
          (data.sharedByName as string) || 'Someone',
          (data.viewUrl as string) || '',
        );
        break;
      default:
        // Generic fallback for other templates
        await sendEmail({
          to,
          subject: `Secuura Notification: ${template}`,
          text: `You have a new notification from Secuura.\n\nDetails: ${JSON.stringify(data, null, 2)}`,
        });
        break;
    }
    logger.info('Notification sent via SMTP fallback', { template, to });
  } catch (err) {
    logger.warn('SMTP fallback also failed (non-blocking)', {
      template: payload.template,
      error: String(err),
    });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// LIFECYCLE NOTIFICATION HELPERS
// ─────────────────────────────────────────────────────────────────────────────

export async function notifyDocumentCertified(params: {
  toEmail: string;
  recipientName?: string;
  documentTitle: string;
  certifierName: string;
  certificationId: string;
  certifiedAt: string;
  viewUrl?: string;
}): Promise<void> {
  await sendNotification({
    to: params.toEmail,
    template: 'document_certified',
    data: {
      recipientName: params.recipientName,
      documentTitle: params.documentTitle,
      certifierName: params.certifierName,
      certificationId: params.certificationId,
      certifiedAt: params.certifiedAt,
      viewUrl: params.viewUrl,
    },
  });
}

export async function notifyDocumentVerified(params: {
  toEmail: string;
  recipientName?: string;
  documentTitle: string;
  verifierName: string;
  verifiedAt: string;
  viewUrl?: string;
}): Promise<void> {
  await sendNotification({
    to: params.toEmail,
    template: 'document_verified',
    data: {
      recipientName: params.recipientName,
      documentTitle: params.documentTitle,
      verifierName: params.verifierName,
      verifiedAt: params.verifiedAt,
      viewUrl: params.viewUrl,
    },
  });
}

export async function notifyDocumentShared(params: {
  toEmail: string;
  recipientName?: string;
  documentTitle: string;
  sharedByName: string;
  shareType: string;
  expiresAt?: string;
  viewUrl?: string;
}): Promise<void> {
  await sendNotification({
    to: params.toEmail,
    template: 'document_shared',
    data: {
      recipientName: params.recipientName,
      documentTitle: params.documentTitle,
      sharedByName: params.sharedByName,
      shareType: params.shareType,
      expiresAt: params.expiresAt,
      viewUrl: params.viewUrl,
    },
  });
}

export async function notifyDocumentRevoked(params: {
  toEmail: string;
  recipientName?: string;
  documentTitle: string;
  revokedBy: string;
  reason?: string;
  revokedAt: string;
}): Promise<void> {
  await sendNotification({
    to: params.toEmail,
    template: 'document_revoked',
    data: {
      recipientName: params.recipientName,
      documentTitle: params.documentTitle,
      revokedBy: params.revokedBy,
      reason: params.reason,
      revokedAt: params.revokedAt,
    },
  });
}

export async function notifyRightsTransferred(params: {
  toEmail: string;
  recipientName?: string;
  documentTitle: string;
  fromName: string;
  transferredAt: string;
  viewUrl?: string;
}): Promise<void> {
  await sendNotification({
    to: params.toEmail,
    template: 'rights_transferred',
    data: {
      recipientName: params.recipientName,
      documentTitle: params.documentTitle,
      fromName: params.fromName,
      transferredAt: params.transferredAt,
      viewUrl: params.viewUrl,
    },
  });
}
