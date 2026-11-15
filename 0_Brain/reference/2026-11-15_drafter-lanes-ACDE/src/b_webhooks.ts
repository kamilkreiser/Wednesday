/**
 * =============================================================================
 * STRIPE WEBHOOK HANDLER
 * =============================================================================
 * Process Stripe webhook events for certification bundle purchases
 *
 * PRICING MODEL: One-time purchase certification bundles
 * - Credits are added to customer account on successful payment
 * - Credits never expire
 *
 * IDEMPOTENCY (KS-488 C-4): every event is *claimed* in the webhook_events table
 * before any side effect runs. The claim is a conditional INSERT, so it answers
 * three distinct questions that a boolean "have we seen this?" could not:
 *   - claim won        -> first delivery, process it
 *   - claim lost       -> already claimed or processed, 200 without re-processing
 *   - claim impossible -> DB unreachable, 503 so Stripe redelivers
 * The previous check-then-act version returned `false` ("not processed, go
 * ahead") both when the DB said no and when the DB could not answer, so a
 * redelivery during a DB blip re-granted the credits.
 */

import { Router, Request, Response } from 'express';
import Stripe from 'stripe';
import { authenticate, requireRole } from '@secuura/shared';
import { getStripeService } from '../services/stripeService';
import { query, isDbAvailable } from '../db';
import { logger } from '../utils/logger';
import { grantCreditsOnce, checkoutPaymentKey, describeThrown } from '../creditGrants';

const router = Router();

// =============================================================================
// IDEMPOTENCY HELPERS
// =============================================================================

/** Raised when the idempotency claim cannot be made at all (DB unreachable). */
class ClaimUnavailableError extends Error {
  constructor(cause?: string) {
    super(cause ? `Idempotency claim unavailable: ${cause}` : 'Idempotency claim unavailable');
    this.name = 'ClaimUnavailableError';
  }
}

/**
 * Claim an event for processing, before any side effect runs.
 *
 * Returns true when this delivery won the claim and must be processed, false
 * when another delivery already holds it (or it is already processed) and this
 * one is a duplicate. Throws ClaimUnavailableError when the database cannot
 * answer — the caller must then refuse the delivery rather than guess.
 *
 * The conditional upsert is what makes this safe under concurrent redeliveries:
 * two simultaneous deliveries of the same event contend on the `event_id`
 * unique index, and exactly one gets a row back. A row left in 'failed' by a
 * handler that threw is re-claimable, so a paid-for grant is never stranded
 * behind its own tombstone.
 *
 * The payload is stored at claim time, not after processing, so an event whose
 * handler died mid-flight is still replayable by an admin (POST /webhooks/replay).
 */
async function claimEvent(eventId: string, eventType: string, payload: object): Promise<boolean> {
  if (!isDbAvailable()) {
    logger.warn('DB unavailable — refusing webhook, cannot claim event', { eventId });
    throw new ClaimUnavailableError('database unavailable');
  }

  try {
    const result = await query<{ event_id: string }>(
      `INSERT INTO webhook_events (event_id, event_type, payload, status)
       VALUES ($1, $2, $3, 'processing')
       ON CONFLICT (event_id) DO UPDATE
         SET status = 'processing', processed_at = NOW()
         WHERE webhook_events.status = 'failed'
       RETURNING event_id`,
      [eventId, eventType, JSON.stringify(payload)],
    );
    return (result.rowCount ?? result.rows.length) > 0;
  } catch (err: any) {
    logger.error('Idempotency claim failed', { eventId, error: err?.message });
    throw new ClaimUnavailableError(err?.message);
  }
}

/**
 * Finalise a claimed event once its side effects have succeeded.
 *
 * A failure here is logged but not fatal: the credits are already granted and
 * the claim row already blocks redelivery, so the row simply keeps its
 * 'processing' status and its claim-time payload.
 */
async function finaliseEvent(
  eventId: string,
  customerId: string | null,
  creditsAdded: number,
  amount: number,
  currency: string | null,
): Promise<void> {
  try {
    await query(
      `UPDATE webhook_events
          SET status = 'processed',
              customer_id = $2,
              credits_added = $3,
              amount = $4,
              currency = $5,
              processed_at = NOW()
        WHERE event_id = $1`,
      [eventId, customerId, creditsAdded, amount, currency],
    );
    logger.debug('Webhook event finalised', { eventId, creditsAdded });
  } catch (err) {
    // KS-1933: this runs AFTER the credit, so it must never throw: a throw here used to release the claim and
    // let the redelivery credit the purchase again. Type and field names only (KS-1346 rule a).
    logger.error('Failed to finalise webhook event', { eventId, ...describeThrown(err) });
  }
}

/**
 * Release a claim after the handler threw, so the redelivery can retry.
 *
 * Without this the claim row is a tombstone: every subsequent delivery of a
 * genuinely-unprocessed event is answered "duplicate" and the customer never
 * receives the credits they paid for.
 */
async function releaseClaim(eventId: string, reason: string): Promise<void> {
  try {
    await query(
      `UPDATE webhook_events SET status = 'failed' WHERE event_id = $1 AND status = 'processing'`,
      [eventId],
    );
    logger.warn('Webhook claim released for retry', { eventId, reason });
  } catch (err) {
    // The claim stays 'processing' and the event needs an admin replay. Say so
    // loudly rather than letting it look like an ordinary handler failure.
    // KS-1933: never throw from here, whatever was thrown (an unreadable value
    // used to escape, leave the request unanswered and strand the row silently).
    logger.error('Failed to release webhook claim — event needs manual replay', {
      eventId,
      ...describeThrown(err),
    });
  }
}

// =============================================================================
// WEBHOOK HANDLER
// =============================================================================

/**
 * POST /webhooks/stripe
 * Handle Stripe webhook events
 *
 * IMPORTANT: This route must receive raw body, not parsed JSON
 */
router.post(
  '/stripe',
  async (req: Request, res: Response) => {
    const signature = req.headers['stripe-signature'] as string;

    if (!signature) {
      logger.error('Missing stripe-signature header');
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Missing signature' } });
      return;
    }

    let event: Stripe.Event;

    try {
      const stripeService = getStripeService();
      event = stripeService.constructWebhookEvent(req.body, signature);
    } catch (error) {
      let reason: string;
      try {
        reason = String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('Webhook signature verification failed', { error: reason });
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid signature' } });
      return;
    }

    logger.info('Webhook event received', { eventType: event.type, eventId: event.id });

    // --- Idempotency claim (KS-488 C-4) ---
    // Claimed before any side effect. An unreachable DB is refused, not
    // assumed-clean: Stripe retries a 5xx with backoff for days, and a delayed
    // grant is recoverable where a double grant is not.
    let claimed: boolean;
    try {
      claimed = await claimEvent(event.id, event.type, event);
    } catch (error) {
      let reason: string;
      try {
        reason = error instanceof Error ? error.message : String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('[Webhook] Refusing delivery — idempotency unavailable', {
        eventId: event.id,
        eventType: event.type,
        error: reason,
      });
      res.status(503).json({
        success: false,
        error: {
          code: 'SERVICE_UNAVAILABLE',
          message: 'Idempotency store unavailable — retry this delivery',
        },
      });
      return;
    }

    if (!claimed) {
      logger.info('Duplicate webhook event — skipping', { eventId: event.id, eventType: event.type });
      res.json({ received: true, duplicate: true });
      return;
    }

    try {
      const result = await handleWebhookEvent(event);

      await finaliseEvent(
        event.id,
        result.customerId,
        result.creditsAdded,
        result.amount,
        result.currency,
      );

      res.json({ received: true });
    } catch (error) {
      let message: string;
      try {
        message = error instanceof Error ? error.message : String(error);
      } catch {
        message = 'unreadable thrown value';
      }
      logger.error(`[Webhook] Error handling ${event.type}:`, { error: message });
      // Hand the claim back so the redelivery is processed rather than
      // acknowledged as a duplicate.
      await releaseClaim(event.id, message);
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Webhook handler failed' } });
    }
  }
);

// =============================================================================
// REPLAY ENDPOINT
// =============================================================================

/**
 * POST /webhooks/replay
 * Re-process a previously stored webhook event.
 *
 * Body: { eventId: string, reason: string }
 *
 * KS-157: Protected by admin authentication. Each replay is audit-logged
 * with actor identity + reason so a misuse is forensically reconstructible.
 * Not currently gateway-exposed (gateway only routes `/webhooks/stripe` to
 * billing) — this is defence-in-depth against an in-VNet attacker.
 */
router.post(
  '/replay',
  authenticate(),
  requireRole('SYSTEM_ADMIN', 'SUPER_ADMIN'),
  async (req: Request, res: Response) => {
    // The replay endpoint receives JSON (not raw), so parse if needed
    let body: any;
    try {
      body = typeof req.body === 'string' || Buffer.isBuffer(req.body)
        ? JSON.parse(req.body.toString())
        : req.body;
    } catch {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid JSON body' } });
      return;
    }

    const { eventId, reason } = body || {};

    if (!eventId) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Missing eventId in request body' } });
      return;
    }

    // KS-157: require a free-text reason so replays leave a forensic trail.
    if (!reason || typeof reason !== 'string' || reason.trim().length < 3) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Missing or too-short `reason` (min 3 chars) — required for audit trail' } });
      return;
    }

    if (!isDbAvailable()) {
      res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Database unavailable — cannot replay events' } });
      return;
    }

    try {
      const result = await query<{ payload: object; event_type: string; status: string }>(
        'SELECT payload, event_type, status FROM webhook_events WHERE event_id = $1',
        [eventId],
      );

      if (result.rows.length === 0) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Event not found', eventId } });
        return;
      }

      const row = result.rows[0];
      const event = row.payload as Stripe.Event;

      // KS-157: structured audit trail for the replay action.
      const actor = (req as any).user || {};
      logger.info('Replaying webhook event', {
        eventId,
        eventType: row.event_type,
        actorUserId: actor.userId,
        actorEmail: actor.email,
        actorRole: actor.role,
        reason: reason.trim(),
      });

      const handlerResult = await handleWebhookEvent(event);

      // Update the existing record with fresh processed_at timestamp
      await query(
        `UPDATE webhook_events
         SET status = 'replayed', credits_added = $2, processed_at = NOW()
         WHERE event_id = $1`,
        [eventId, handlerResult.creditsAdded],
      );

      res.json({
        replayed: true,
        eventId,
        eventType: row.event_type,
        creditsAdded: handlerResult.creditsAdded,
      });
    } catch (error) {
      let reason: string;
      try {
        reason = error instanceof Error ? error.message : String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('Replay failed', { eventId, error: reason });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Replay failed' } });
    }
  }
);

// =============================================================================
// EVENT HANDLERS
// =============================================================================

interface WebhookHandlerResult {
  customerId: string | null;
  creditsAdded: number;
  amount: number;
  currency: string | null;
}

async function handleWebhookEvent(event: Stripe.Event): Promise<WebhookHandlerResult> {
  const stripeService = getStripeService();
  const result: WebhookHandlerResult = {
    customerId: null,
    creditsAdded: 0,
    amount: 0,
    currency: null,
  };

  switch (event.type) {
    // =========================================================================
    // CHECKOUT EVENTS - Primary handler for bundle purchases
    // =========================================================================
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      const credits = await handleCheckoutComplete(session, stripeService, event);
      result.customerId = (session.customer as string) || null;
      result.creditsAdded = credits;
      result.amount = session.amount_total || 0;
      result.currency = session.currency || null;
      break;
    }

    // =========================================================================
    // PAYMENT EVENTS - Backup handler for direct payments
    // =========================================================================
    case 'payment_intent.succeeded': {
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      const credits = await handlePaymentSucceeded(paymentIntent, stripeService, event);
      result.customerId = (paymentIntent.customer as string) || null;
      result.creditsAdded = credits;
      result.amount = paymentIntent.amount || 0;
      result.currency = paymentIntent.currency || null;
      break;
    }

    case 'payment_intent.payment_failed': {
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      await handlePaymentFailed(paymentIntent);
      result.customerId = (paymentIntent.customer as string) || null;
      result.amount = paymentIntent.amount || 0;
      result.currency = paymentIntent.currency || null;
      break;
    }

    // =========================================================================
    // INVOICE EVENTS
    // =========================================================================
    case 'invoice.paid': {
      const invoice = event.data.object as Stripe.Invoice;
      await handleInvoicePaid(invoice);
      result.customerId = (invoice.customer as string) || null;
      result.amount = invoice.amount_paid || 0;
      result.currency = invoice.currency || null;
      break;
    }

    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      await handleInvoicePaymentFailed(invoice);
      result.customerId = (invoice.customer as string) || null;
      result.amount = invoice.amount_due || 0;
      result.currency = invoice.currency || null;
      break;
    }

    // =========================================================================
    // CUSTOMER EVENTS
    // =========================================================================
    case 'customer.created': {
      const customer = event.data.object as Stripe.Customer;
      logger.info('Customer created', { customerId: customer.id, email: customer.email });
      result.customerId = customer.id;
      break;
    }

    case 'customer.updated': {
      const customer = event.data.object as Stripe.Customer;
      logger.info('Customer updated', { customerId: customer.id });
      result.customerId = customer.id;
      break;
    }

    // =========================================================================
    // CHARGE EVENTS - Alternative trigger for credit addition
    // =========================================================================
    case 'charge.succeeded': {
      const charge = event.data.object as Stripe.Charge;
      logger.info('Charge succeeded', { chargeId: charge.id });
      result.customerId = (charge.customer as string) || null;
      result.amount = charge.amount || 0;
      result.currency = charge.currency || null;
      break;
    }

    default:
      logger.debug('Unhandled webhook event', { eventType: event.type });
  }

  return result;
}

// =============================================================================
// HANDLER IMPLEMENTATIONS
// =============================================================================

/**
 * Handle checkout session completion - ADD CERTIFICATION CREDITS
 * Returns the number of credits added.
 */
async function handleCheckoutComplete(
  session: Stripe.Checkout.Session,
  stripeService: ReturnType<typeof getStripeService>,
  event: Pick<Stripe.Event, 'id' | 'type'>,
): Promise<number> {
  logger.info('Checkout completed', { sessionId: session.id });

  const customerId = session.customer as string;
  const certifications = parseInt(session.metadata?.certifications || '0', 10);
  const bundleId = session.metadata?.bundleId;

  if (!customerId) {
    logger.error('No customer ID in checkout session');
    return 0;
  }

  let creditsAdded = 0;
  if (certifications > 0) {
    // KS-1933: credit the PAYMENT once — this purchase's payment_intent.succeeded, a redelivery after a throw,
    // or an admin replay finds the payment already credited and adds nothing.
    const newBalance = await grantCreditsOnce(
      { paymentKey: checkoutPaymentKey(session), customerId, credits: certifications, eventId: event.id, eventType: event.type },
      (c, n) => stripeService.addCertificationCredits(c, n),
    );
    if (newBalance === null) {
      return 0;
    }
    creditsAdded = certifications;

    logger.info('Certification credits added', { credits: certifications, customerId });
    logger.info('Bundle purchase details', { bundleId: bundleId || 'custom', newBalance });

    // Email notification — uses console logging in dev; integrate SendGrid/SES in production
    logger.info('Purchase confirmation email queued', { customerId, credits: certifications });
    if (process.env.SENDGRID_API_KEY) {
      logger.debug('SendGrid integration pending');
    }
  } else {
    logger.warn('Checkout has no certifications in metadata', { sessionId: session.id });
  }

  // Log additional details
  logger.info('Payment status', { status: session.payment_status });
  logger.info('Payment amount', { amount: session.amount_total ? session.amount_total / 100 : 0, currency: session.currency });

  return creditsAdded;
}

/**
 * Handle successful payment - BACKUP credit addition
 * This is a backup in case checkout.session.completed doesn't fire.
 * Returns the number of credits added.
 */
async function handlePaymentSucceeded(
  paymentIntent: Stripe.PaymentIntent,
  stripeService: ReturnType<typeof getStripeService>,
  event: Pick<Stripe.Event, 'id' | 'type'>,
): Promise<number> {
  logger.info('Payment succeeded', { paymentIntentId: paymentIntent.id });

  const customerId = paymentIntent.customer as string;
  const certifications = parseInt(paymentIntent.metadata?.certifications || '0', 10);
  const bundleId = paymentIntent.metadata?.bundleId;
  let creditsAdded = 0;

  // Only process if we have certifications metadata
  // (checkout.session.completed should handle most cases)
  if (customerId && certifications > 0) {
    // Check if credits were already added by checkout event
    // We store a flag in metadata to prevent double-crediting
    if (!paymentIntent.metadata?.creditsAdded) {
      // KS-1933: the same payment key as this purchase's checkout.session.completed (its payment_intent), so
      // whichever event arrives second adds nothing. (Nothing writes metadata.creditsAdded; the check stays as is.)
      const newBalance = await grantCreditsOnce(
        { paymentKey: `pi:${paymentIntent.id}`, customerId, credits: certifications, eventId: event.id, eventType: event.type },
        (c, n) => stripeService.addCertificationCredits(c, n),
      );
      if (newBalance === null) {
        return 0;
      }
      creditsAdded = certifications;

      logger.info('Credits added via payment_intent backup', { credits: certifications });
      logger.info('Bundle purchase details', { bundleId: bundleId || 'custom', newBalance });
    } else {
      logger.debug('Credits already added', { paymentIntentId: paymentIntent.id });
    }
  }

  logger.info('Payment amount', { amount: paymentIntent.amount / 100, currency: paymentIntent.currency });

  return creditsAdded;
}

/**
 * Handle failed payment
 */
async function handlePaymentFailed(paymentIntent: Stripe.PaymentIntent): Promise<void> {
  logger.warn('Payment failed', { paymentIntentId: paymentIntent.id });

  const customerId = paymentIntent.customer as string;
  const error = paymentIntent.last_payment_error;

  logger.warn('Failed payment customer', { customerId });
  logger.warn('Payment error details', { errorMessage: error?.message || 'Unknown' });
  logger.warn('Payment error code', { errorCode: error?.code || 'Unknown' });

  // Email notification — payment failure alert
  logger.info('Payment failure email queued', { customerId });
  if (process.env.SENDGRID_API_KEY) {
    logger.debug('SendGrid failure notification pending');
  }
}

/**
 * Handle invoice paid
 */
async function handleInvoicePaid(invoice: Stripe.Invoice): Promise<void> {
  logger.info('Invoice paid', { invoiceId: invoice.id });

  const customerId = invoice.customer as string;
  const amount = invoice.amount_paid;
  const invoiceUrl = invoice.hosted_invoice_url;

  logger.info('Invoice payment received', { customerId, amount: amount / 100, currency: invoice.currency });
  logger.debug('Invoice URL', { invoiceUrl });

  // Email notification — invoice receipt
  logger.info('Invoice receipt email queued', { customerId });
  if (process.env.SENDGRID_API_KEY) {
    logger.debug('SendGrid receipt email pending');
  }
}

/**
 * Handle invoice payment failed
 */
async function handleInvoicePaymentFailed(invoice: Stripe.Invoice): Promise<void> {
  logger.warn('Invoice payment failed', { invoiceId: invoice.id });

  const customerId = invoice.customer as string;
  const attemptCount = invoice.attempt_count;
  const nextAttempt = invoice.next_payment_attempt;

  logger.warn('Invoice payment retry failed', { customerId, attemptCount });
  logger.info('Next payment attempt', { nextAttempt: nextAttempt ? new Date(nextAttempt * 1000).toISOString() : 'N/A' });

  // Email notification — invoice payment retry failure
  logger.info('Invoice retry failure email queued', { customerId, attemptCount });
  if (process.env.SENDGRID_API_KEY) {
    logger.debug('SendGrid retry failure email pending');
  }
}

export default router;
