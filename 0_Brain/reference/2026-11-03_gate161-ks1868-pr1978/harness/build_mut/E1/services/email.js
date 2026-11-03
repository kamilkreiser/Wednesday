"use strict";
/**
 * =============================================================================
 * EMAIL SERVICE — Azure Communication Services (preferred) + SMTP fallback
 * =============================================================================
 * Sends transactional emails (verification, password reset, notifications).
 *
 * Provider selection (first available wins):
 *   1. Azure Communication Services Email (REST SDK) — if ACS_CONNECTION_STRING
 *      AND ACS_SENDER_ADDRESS are set. Provisioned 2026-04-29 in
 *      secuura-dev-rg.
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
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.sendEmail = sendEmail;
exports.sendVerificationEmail = sendVerificationEmail;
exports.sendPasswordResetEmail = sendPasswordResetEmail;
exports.sendShareNotification = sendShareNotification;
exports.sendCertificationNotification = sendCertificationNotification;
exports.sendRevocationNotification = sendRevocationNotification;
exports.isEmailConfigured = isEmailConfigured;
const nodemailer_1 = __importDefault(require("nodemailer"));
const shared_1 = require("@secuura/shared");
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
// KS-488 C-5: opt-in recipient allow-list. Unset = today's behaviour exactly.
const RECIPIENT_ALLOWLIST = (0, shared_1.parseRecipientAllowlist)(process.env.EMAIL_RECIPIENT_ALLOWLIST);
// ---------------------------------------------------------------------------
// Transport
// ---------------------------------------------------------------------------
let transporter = null;
let smtpMisconfigLogged = false;
function getTransporter() {
    if (!SMTP_ENABLED)
        return null;
    if (transporter)
        return transporter;
    // KS-488 C-5: fail closed and loudly. Enabled-but-unconfigured used to fall
    // back to a real third-party host; refusing is the honest outcome, and the
    // caller already treats a null transport as "not configured".
    const missing = [!SMTP_HOST && 'SMTP_HOST', !SMTP_FROM && 'SMTP_FROM'].filter(Boolean);
    if (missing.length > 0) {
        if (!smtpMisconfigLogged) {
            smtpMisconfigLogged = true;
            console.error(`[Email] SMTP_ENABLED=true but ${missing.join(' and ')} unset — refusing to send. ` +
                `These have no default by design (KS-488 C-5); set them explicitly or unset SMTP_ENABLED.`);
        }
        return null;
    }
    transporter = nodemailer_1.default.createTransport({
        host: SMTP_HOST,
        port: SMTP_PORT,
        secure: SMTP_PORT === 465,
        auth: {
            user: SMTP_USER,
            pass: SMTP_PASS,
        },
        connectionTimeout: 10_000,
        greetingTimeout: 10_000,
        socketTimeout: 15_000,
    });
    console.log(`[Email] SMTP transport created: ${SMTP_HOST}:${SMTP_PORT} from=${SMTP_FROM}`);
    return transporter;
}
// Lazy-loaded ACS client — avoids paying the SDK import cost when not used.
let acsClient = null;
async function getAcsClient() {
    if (!ACS_ENABLED)
        return null;
    if (acsClient)
        return acsClient;
    try {
        const { EmailClient } = await Promise.resolve().then(() => __importStar(require('@azure/communication-email')));
        acsClient = new EmailClient(ACS_CONNECTION_STRING);
        console.log(`[Email] ACS client initialised (sender=${ACS_SENDER_ADDRESS})`);
        return acsClient;
    }
    catch (err) {
        console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${err?.message}`);
        return null;
    }
}
async function sendViaAcs(options) {
    const client = await getAcsClient();
    if (!client)
        return false;
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
    }
    catch (err) {
        let reason;
        try {
            reason = err?.message;
        }
        catch {
            reason = 'unreadable thrown value';
        }
        console.error(`[Email/ACS] Send threw for ${options.to}: ${reason}`);
        return false;
    }
}
/**
 * Send an email. Provider order: ACS (if configured) → SMTP (if configured)
 * → no-op log. Returns true if delivered to a provider successfully.
 */
async function sendEmail(options) {
    // KS-488 C-5: refuse before either provider, so a blocked recipient never
    // reaches a transport and never appears in a provider's logs.
    if (!(0, shared_1.isRecipientAllowed)(options.to, RECIPIENT_ALLOWLIST)) {
        console.warn(`[Email] Recipient not in EMAIL_RECIPIENT_ALLOWLIST — refusing to send: ${options.to}`);
        return false;
    }
    if (ACS_ENABLED) {
        const ok = await sendViaAcs(options);
        if (ok)
            return true;
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
    }
    catch (error) {
        let reason;
        try {
            reason = String(error.message);
        }
        catch {
            reason = 'unreadable thrown value';
        }
        console.error(`[Email/SMTP] Failed to send to ${options.to}: ${reason}`);
        return false;
    }
}
/**
 * Send email verification link.
 */
async function sendVerificationEmail(email, verifyUrl) {
    return sendEmail({
        to: email,
        subject: 'Verify your Secuura account',
        text: `Welcome to Secuura!\n\nPlease verify your email by clicking this link:\n${(0, shared_1.escapeHtmlText)(verifyUrl)}\n\nThis link expires in 24 hours.\n\n— Secuura Team`,
        html: `
      <h2>Welcome to Secuura!</h2>
      <p>Please verify your email address by clicking the link below:</p>
      <p><a href="${(0, shared_1.escapeHtmlText)(verifyUrl)}" style="background:#06b6d4;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;">Verify Email</a></p>
      <p>Or copy this link: <br/><a href="${(0, shared_1.escapeHtmlText)(verifyUrl)}">${(0, shared_1.escapeHtmlText)(verifyUrl)}</a></p>
      <p>This link expires in 24 hours.</p>
      <p>— Secuura Team</p>
    `,
    });
}
/**
 * Send password reset link.
 */
async function sendPasswordResetEmail(email, resetUrl) {
    return sendEmail({
        to: email,
        subject: 'Reset your Secuura password',
        text: `You requested a password reset.\n\nClick this link to reset your password:\n${(0, shared_1.escapeHtmlText)(resetUrl)}\n\nThis link expires in 1 hour. If you did not request this, ignore this email.\n\n— Secuura Team`,
        html: `
      <h2>Password Reset</h2>
      <p>You requested a password reset for your Secuura account.</p>
      <p><a href="${(0, shared_1.escapeHtmlText)(resetUrl)}" style="background:#06b6d4;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;">Reset Password</a></p>
      <p>Or copy this link: <br/><a href="${(0, shared_1.escapeHtmlText)(resetUrl)}">${(0, shared_1.escapeHtmlText)(resetUrl)}</a></p>
      <p>This link expires in 1 hour. If you did not request this, ignore this email.</p>
      <p>— Secuura Team</p>
    `,
    });
}
/**
 * Send document share notification.
 */
async function sendShareNotification(recipientEmail, documentTitle, sharedByName, shareUrl) {
    // KS-488 C-5: sanitise for the header, escape at each HTML site.
    const title = (0, shared_1.sanitizeHeaderText)(documentTitle);
    const sharedBy = (0, shared_1.sanitizeHeaderText)(sharedByName);
    return sendEmail({
        to: recipientEmail,
        subject: `${sharedBy} shared a document with you on Secuura`,
        text: `${sharedBy} has shared "${title}" with you on Secuura.\n\nView the document: ${shareUrl}\n\n— Secuura Team`,
        html: `
      <h2>Document Shared With You</h2>
      <p><strong>${(0, shared_1.escapeHtmlText)(sharedBy)}</strong> has shared the following document with you:</p>
      <p style="font-size:18px;font-weight:bold;">${(0, shared_1.escapeHtmlText)(title)}</p>
      <p><a href="${(0, shared_1.escapeHtmlText)(shareUrl)}" style="background:#06b6d4;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;">View Document</a></p>
      <p>— Secuura Team</p>
    `,
    });
}
/**
 * Send document certification notification to holder.
 */
async function sendCertificationNotification(holderEmail, documentTitle, issuerName) {
    const title = (0, shared_1.sanitizeHeaderText)(documentTitle);
    const issuer = (0, shared_1.sanitizeHeaderText)(issuerName);
    return sendEmail({
        to: holderEmail,
        subject: `Your document "${title}" has been certified on Secuura`,
        text: `Your document "${title}" has been certified by ${issuer} on Secuura.\n\nLog in to view your certified credential.\n\n— Secuura Team`,
        html: `
      <h2>Document Certified</h2>
      <p>Your document <strong>"${(0, shared_1.escapeHtmlText)(title)}"</strong> has been certified by <strong>${(0, shared_1.escapeHtmlText)(issuer)}</strong>.</p>
      <p>Log in to Secuura to view your certified credential.</p>
      <p>— Secuura Team</p>
    `,
    });
}
/**
 * Send revocation notification.
 */
async function sendRevocationNotification(holderEmail, documentTitle, reason) {
    const title = (0, shared_1.sanitizeHeaderText)(documentTitle);
    const revocationReason = (0, shared_1.sanitizeHeaderText)(reason);
    return sendEmail({
        to: holderEmail,
        subject: `Document "${title}" has been revoked on Secuura`,
        text: `The document "${title}" has been revoked.\n\nReason: ${revocationReason}\n\nPlease contact the issuer for more information.\n\n— Secuura Team`,
        html: `
      <h2>Document Revoked</h2>
      <p>The document <strong>"${(0, shared_1.escapeHtmlText)(title)}"</strong> has been revoked.</p>
      <p><strong>Reason:</strong> ${(0, shared_1.escapeHtmlText)(revocationReason)}</p>
      <p>Please contact the issuer for more information.</p>
      <p>— Secuura Team</p>
    `,
    });
}
function isEmailConfigured() {
    // KS-488 C-5: ACS is the preferred provider, so a deployment on ACS with SMTP
    // deliberately off is still configured for email. Reporting only SMTP_ENABLED
    // made an ACS-only deployment look unconfigured and skip its notifications.
    return ACS_ENABLED || (SMTP_ENABLED && !!SMTP_HOST && !!SMTP_FROM);
}
