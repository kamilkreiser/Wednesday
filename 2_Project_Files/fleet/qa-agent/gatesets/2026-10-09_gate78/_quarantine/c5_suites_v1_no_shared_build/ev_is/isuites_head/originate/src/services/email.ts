/**
 * =============================================================================
 * EMAIL SERVICE — Azure Communication Services (preferred) + SMTP fallback
 * =============================================================================
 * Sends transactional emails for document lifecycle events (certification,
 * revocation, sharing notifications).
 *
 * Provider selection (first available wins):
 *   1. Azure Communication Services Email (REST SDK) — if ACS_CONNECTION_STRING
 *      AND ACS_SENDER_ADDRESS are set. This is the recommended path on dev/demo
 *      Azure deployments. Provisioned 2026-04-29 in secuura-dev-rg.
 *   2. SMTP via nodemailer — ONLY if SMTP_ENABLED=true AND SMTP_HOST is set.
 *      Used by the legacy AgentMail / SendGrid integrations.
 *   3. No-op log — if neither is configured.
 *
 * Azure Communication Services config:
 *   ACS_CONNECTION_STRING  — `endpoint=https://...;accesskey=...` from
 *                            `az communication list-key`
 *   ACS_SENDER_ADDRESS     — e.g. `donotreply@<azuremanaged>.azurecomm.net`
 *
 * SMTP config (legacy fallback) — KS-488 C-5: every value below is explicit.
 * There are deliberately NO defaults pointing at a real mail provider, and the
 * transport cannot switch itself on:
 *   SMTP_HOST     — SMTP server. REQUIRED when enabled. No default.
 *   SMTP_PORT     — SMTP port (default: 465)
 *   SMTP_USER     — SMTP username. No default.
 *   SMTP_PASS     — SMTP password / API key. Does NOT enable the transport.
 *   SMTP_FROM     — From address. REQUIRED when enabled (falls back to
 *                   EMAIL_FROM, then ACS_SENDER_ADDRESS). No literal default.
 *   SMTP_ENABLED  — the ONLY switch. Must be exactly 'true'. Default: off.
 * =============================================================================
 */

import nodemailer from 'nodemailer';
// KS-1378 round 2 (N-1339-1): nodemailer 10 ships its own declarations, which export the
// default as a VALUE and Transporter as a TYPE, so tsc prefers them over @types/nodemailer and
// the namespace form `nodemailer.Transporter` has nothing behind it (TS2503, rc 2 -> the image cannot build).
// A type-only import of the named type. Every VALUE use of `nodemailer` below is unchanged.
import type { Transporter } from 'nodemailer';
import {
  sanitizeHeaderText,
  escapeHtmlText,
  parseRecipientAllowlist,
  isRecipientAllowed,
} from '@secuura/shared';

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const ACS_CONNECTION_STRING = process.env.ACS_CONNECTION_STRING || '';
const ACS_SENDER_ADDRESS = process.env.ACS_SENDER_ADDRESS || '';
const ACS_ENABLED = !!ACS_CONNECTION_STRING && !!ACS_SENDER_ADDRESS;

// KS-488 C-5: SMTP is opt-in ONLY, and defaults to nothing real.
//
// Before this, two defaults combined into a transport that could switch itself
// on and point at someone else's infrastructure without anyone deciding to:
//   - SMTP_ENABLED was true whenever SMTP_PASS was set, so a password alone
//     silently enabled sending;
//   - SMTP_HOST/USER/FROM defaulted to a real third-party provider, so an
//     accidentally-enabled transport delivered through it rather than failing.
// SMTP_ENABLED is now the only switch, and an enabled-but-unconfigured
// transport refuses to send (see getTransporter) instead of guessing.
const SMTP_HOST = process.env.SMTP_HOST || '';
const SMTP_PORT = parseInt(process.env.SMTP_PORT || '465', 10);
const SMTP_USER = process.env.SMTP_USER || '';
const SMTP_PASS = process.env.SMTP_PASS || '';
const SMTP_FROM = process.env.SMTP_FROM || process.env.EMAIL_FROM || ACS_SENDER_ADDRESS || '';
const SMTP_ENABLED = process.env.SMTP_ENABLED === 'true';

// KS-488 C-5: opt-in recipient allow-list. Unset = today's behaviour exactly;
// an allow-list nobody configured must not quietly start dropping mail.
const RECIPIENT_ALLOWLIST = parseRecipientAllowlist(process.env.EMAIL_RECIPIENT_ALLOWLIST);

// ---------------------------------------------------------------------------
// Transport
// ---------------------------------------------------------------------------

let transporter: Transporter | null = null;
let smtpMisconfigLogged = false;

function getTransporter(): Transporter | null {
  if (!SMTP_ENABLED) return null;
  if (transporter) return transporter;

  // KS-488 C-5: fail closed and loudly. Enabled-but-unconfigured used to fall
  // back to a real third-party host; refusing is the honest outcome, and the
  // caller already treats a null transport as "not configured".
  const missing = [!SMTP_HOST && 'SMTP_HOST', !SMTP_FROM && 'SMTP_FROM'].filter(Boolean);
  if (missing.length > 0) {
    if (!smtpMisconfigLogged) {
      smtpMisconfigLogged = true;
      console.error(
        `[Email] SMTP_ENABLED=true but ${missing.join(' and ')} unset — refusing to send. ` +
          `These have no default by design (KS-488 C-5); set them explicitly or unset SMTP_ENABLED.`,
      );
    }
    return null;
  }

  transporter = nodemailer.createTransport({
    host: SMTP_HOST,
    port: SMTP_PORT,
    secure: SMTP_PORT === 465,
    auth: {
      user: SMTP_USER,
      pass: SMTP_PASS,
    },
  });

  console.log(`[Email] SMTP transport created: ${SMTP_HOST}:${SMTP_PORT} from=${SMTP_FROM}`);
  return transporter;
}

// ---------------------------------------------------------------------------
// Send functions
// ---------------------------------------------------------------------------

export interface EmailOptions {
  to: string;
  subject: string;
  text: string;
  html?: string;
}

// Lazy-loaded ACS client — avoids paying the SDK import cost when not used.
let acsClient: any | null = null;

async function getAcsClient(): Promise<any | null> {
  if (!ACS_ENABLED) return null;
  if (acsClient) return acsClient;
  try {
    const { EmailClient } = await import('@azure/communication-email');
    acsClient = new EmailClient(ACS_CONNECTION_STRING);
    console.log(`[Email] ACS client initialised (sender=${ACS_SENDER_ADDRESS})`);
    return acsClient;
  } catch (err: any) {
    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${err?.message}`);
    return null;
  }
}

async function sendViaAcs(options: EmailOptions): Promise<boolean> {
  const client = await getAcsClient();
  if (!client) return false;
  try {
    const message = {
      senderAddress: ACS_SENDER_ADDRESS,
      content: {
        subject: options.subject,
        plainText: options.text,
        ...(options.html ? { html: options.html } : {}),
      },
      recipients: { to: [{ address: options.to }] },
    };
    const poller = await client.beginSend(message);
    const result = await poller.pollUntilDone();
    if (result.status === 'Succeeded') {
      console.log(`[Email/ACS] Sent to ${options.to}: ${options.subject} (messageId: ${result.id})`);
      return true;
    }
    console.error(`[Email/ACS] Send failed for ${options.to}: status=${result.status}`, result.error);
    return false;
  } catch (err: any) {
    console.error(`[Email/ACS] Send threw for ${options.to}: ${err?.message}`);
    return false;
  }
}

/**
 * Send an email. Provider order: ACS (if configured) → SMTP (if configured)
 * → no-op log. Returns true if delivered to a provider successfully.
 */
export async function sendEmail(options: EmailOptions): Promise<boolean> {
  // KS-488 C-5: refuse before either provider, so a blocked recipient never
  // reaches a transport and never appears in a provider's logs.
  if (!isRecipientAllowed(options.to, RECIPIENT_ALLOWLIST)) {
    console.warn(`[Email] Recipient not in EMAIL_RECIPIENT_ALLOWLIST — refusing to send: ${options.to}`);
    return false;
  }

  if (ACS_ENABLED) {
    const ok = await sendViaAcs(options);
    if (ok) return true;
    console.warn(`[Email] ACS send failed — falling through to SMTP if configured.`);
  }

  const transport = getTransporter();
  if (!transport) {
    console.log(`[Email] No provider configured — would send to ${options.to}: ${options.subject}`);
    return false;
  }

  try {
    const info = await transport.sendMail({
      from: `Secuura <${SMTP_FROM}>`,
      to: options.to,
      subject: options.subject,
      text: options.text,
      html: options.html,
    });
    console.log(`[Email/SMTP] Sent to ${options.to}: ${options.subject} (messageId: ${info.messageId})`);
    return true;
  } catch (error: any) {
    console.error(`[Email/SMTP] Failed to send to ${options.to}: ${error.message}`);
    return false;
  }
}

/**
 * Send document share notification.
 */
export async function sendShareNotification(
  recipientEmail: string,
  documentTitle: string,
  sharedByName: string,
  shareUrl: string
): Promise<boolean> {
  // KS-488 C-5: caller-supplied text is sanitised for the header and escaped
  // for the body. `shareUrl` is platform-constructed, so it is escaped as an
  // attribute value but not otherwise altered.
  const title = sanitizeHeaderText(documentTitle);
  const sharedBy = sanitizeHeaderText(sharedByName);

  return sendEmail({
    to: recipientEmail,
    subject: `${sharedBy} shared a document with you on Secuura`,
    text: `${sharedBy} has shared "${title}" with you on Secuura.\n\nView the document: ${shareUrl}\n\n— Secuura Team`,
    html: `
      <h2>Document Shared With You</h2>
      <p><strong>${escapeHtmlText(sharedBy)}</strong> has shared the following document with you:</p>
      <p style="font-size:18px;font-weight:bold;">${escapeHtmlText(title)}</p>
      <p><a href="${escapeHtmlText(shareUrl)}" style="background:#06b6d4;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;">View Document</a></p>
      <p>— Secuura Team</p>
    `,
  });
}

/**
 * Send document certification notification to holder.
 */
export async function sendCertificationNotification(
  holderEmail: string,
  documentTitle: string,
  issuerName: string
): Promise<boolean> {
  const title = sanitizeHeaderText(documentTitle);
  const issuer = sanitizeHeaderText(issuerName);

  return sendEmail({
    to: holderEmail,
    subject: `Your document "${title}" has been certified on Secuura`,
    text: `Your document "${title}" has been certified by ${issuer} on Secuura.\n\nLog in to view your certified credential.\n\n— Secuura Team`,
    html: `
      <h2>Document Certified</h2>
      <p>Your document <strong>"${escapeHtmlText(title)}"</strong> has been certified by <strong>${escapeHtmlText(issuer)}</strong>.</p>
      <p>Log in to Secuura to view your certified credential.</p>
      <p>— Secuura Team</p>
    `,
  });
}

/**
 * Send revocation notification.
 */
export async function sendRevocationNotification(
  holderEmail: string,
  documentTitle: string,
  reason: string
): Promise<boolean> {
  const title = sanitizeHeaderText(documentTitle);
  const revocationReason = sanitizeHeaderText(reason);

  return sendEmail({
    to: holderEmail,
    subject: `Document "${title}" has been revoked on Secuura`,
    text: `The document "${title}" has been revoked.\n\nReason: ${revocationReason}\n\nPlease contact the issuer for more information.\n\n— Secuura Team`,
    html: `
      <h2>Document Revoked</h2>
      <p>The document <strong>"${escapeHtmlText(title)}"</strong> has been revoked.</p>
      <p><strong>Reason:</strong> ${escapeHtmlText(revocationReason)}</p>
      <p>Please contact the issuer for more information.</p>
      <p>— Secuura Team</p>
    `,
  });
}

/**
 * Send rights holder invitation email.
 */
export async function sendRightsHolderInvite(opts: {
  recipientEmail: string;
  recipientName: string;
  organizationName: string;
  inviteUrl: string;
  inviterName?: string;
}): Promise<boolean> {
  const { recipientEmail, inviteUrl } = opts;
  // KS-488 C-5: every caller-supplied value here reaches both a header and an
  // HTML body. Sanitise once, escape at each HTML site.
  const recipientName = sanitizeHeaderText(opts.recipientName);
  const organizationName = sanitizeHeaderText(opts.organizationName);
  const inviterName = opts.inviterName ? sanitizeHeaderText(opts.inviterName) : undefined;
  const firstName = recipientName.split(' ')[0] || recipientName;

  return sendEmail({
    to: recipientEmail,
    subject: `You've been invited to Secuura Platform K by ${organizationName}`,
    text: [
      `Dear ${firstName},`,
      '',
      `${organizationName} has added you as a rights holder on Secuura Platform K.`,
      '',
      'Secuura Platform K is a blockchain-verified document certification platform. As a rights holder, you can:',
      '- View documents and certifications issued to you',
      '- Verify the authenticity of your certified documents',
      '- Share verified credentials with third parties',
      '',
      `To get started, create your account using the link below:`,
      '',
      inviteUrl,
      '',
      'This link is unique to you. Do not share it with anyone.',
      '',
      `If you have any questions, please contact ${organizationName} directly.`,
      '',
      'Best regards,',
      `The ${organizationName} Team`,
      `Powered by Secuura Platform K`,
    ].join('\n'),
    html: `
      <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1a1a2e;">
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 32px; border-radius: 12px 12px 0 0;">
          <h1 style="color: #06b6d4; margin: 0; font-size: 24px;">Secuura Platform K</h1>
          <p style="color: #94a3b8; margin: 8px 0 0 0; font-size: 14px;">Blockchain-Verified Document Certification</p>
        </div>

        <div style="background: #ffffff; padding: 32px; border: 1px solid #e2e8f0; border-top: none;">
          <h2 style="margin: 0 0 16px 0; color: #1e293b;">You've been invited</h2>

          <p>Dear ${escapeHtmlText(firstName)},</p>

          <p><strong>${escapeHtmlText(organizationName)}</strong> has added you as a <strong>rights holder</strong> on Secuura Platform K${inviterName ? ` (invited by ${escapeHtmlText(inviterName)})` : ''}.</p>

          <p>As a rights holder, you can:</p>
          <ul style="color: #475569; line-height: 1.8;">
            <li>View documents and certifications issued to you</li>
            <li>Verify the authenticity of your certified documents</li>
            <li>Share verified credentials with third parties</li>
            <li>Download blockchain-anchored proof of certification</li>
          </ul>

          <div style="text-align: center; margin: 32px 0;">
            <a href="${escapeHtmlText(inviteUrl)}" style="background: #06b6d4; color: white; padding: 14px 32px; border-radius: 8px; text-decoration: none; display: inline-block; font-weight: 600; font-size: 16px;">
              Create Your Account
            </a>
          </div>

          <p style="color: #64748b; font-size: 13px;">This link is unique to you. Do not share it with anyone.</p>

          <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;" />

          <p style="color: #64748b; font-size: 13px;">
            If you have any questions, please contact <strong>${escapeHtmlText(organizationName)}</strong> directly.
            If you did not expect this invitation, you can safely ignore this email.
          </p>
        </div>

        <div style="background: #f8fafc; padding: 16px 32px; border-radius: 0 0 12px 12px; border: 1px solid #e2e8f0; border-top: none; text-align: center;">
          <p style="margin: 0; color: #94a3b8; font-size: 12px;">
            Powered by Secuura Platform K &mdash; Blockchain-verified document certification
          </p>
        </div>
      </div>
    `,
  });
}

export function isEmailConfigured(): boolean {
  // KS-488 C-5: ACS is the preferred provider, so a deployment on ACS with SMTP
  // deliberately off is still configured for email. Reporting only SMTP_ENABLED
  // made an ACS-only deployment look unconfigured and skip its notifications.
  return ACS_ENABLED || (SMTP_ENABLED && !!SMTP_HOST && !!SMTP_FROM);
}
