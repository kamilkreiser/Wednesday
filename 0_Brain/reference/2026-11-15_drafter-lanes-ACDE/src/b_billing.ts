/**
 * =============================================================================
 * BILLING API ROUTES
 * =============================================================================
 * REST API endpoints for certification bundle purchases
 * 
 * PRICING MODEL: One-time purchase certification bundles
 * - Credits never expire
 * - Verifications are FREE
 * - Storage is FREE
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { getStripeService } from '../services/stripeService';
import { 
  CERTIFICATION_BUNDLES, 
  formatPrice, 
  loadStripeConfig,
  getCertificationBundle,
  INCLUDED_FEATURES,
  PAY_AS_YOU_GO_PRICE,
} from '../config/stripe.config';
import { logger } from '../utils/logger';
// KS-1850: the shared platform-role predicate gates POST /admin/credits below.
import { isPlatformRole } from '@secuura/shared';
// KS-1725: zod 4 issues rendered in zod 3.25.76's shape for every response (the client contract unchanged).
import { zod3Issues } from '@secuura/shared/zod3-compat';

const router = Router();

/**
 * KS-431 (extends KS-421 / KS-144): classify a Stripe/provider error into a mapped HTTP
 * response so an invalid caller input or a provider-side outage never leaks as a raw 500.
 * Auth/permission/throttling/unreachable problems are provider-side → 503; any other
 * provider 4xx blames the request — 404 with `notFoundMessage` on the id-input routes, or
 * (KS-445) 400 with `invalidRequestMessage` on the body-input routes where the provider
 * rejected the body, not an id lookup; a genuine provider 5xx / unknown shape is left for
 * the caller to answer 500.
 *
 * @param error - the caught error (a Stripe error carries `type` / `statusCode`).
 * @param res - Express response used to write the 503/404/400 on a classified provider error.
 * @param notFoundMessage - the 404 message for a request-blaming provider 4xx (e.g. "Customer not found").
 * @param invalidRequestMessage - when set, a request-blaming provider 4xx (other than an explicit
 *   "No such …" missing-resource message) answers 400 with this message instead of 404 — for
 *   routes whose caller input is a body the Zod schema can't fully pre-validate (KS-445).
 * @returns true when a 503/404/400 was sent; false when the error is unclassified (caller sends its own 500).
 * @example
 * if (sendClassifiedBillingError(error, res, 'Customer not found')) return;
 */
export function sendClassifiedBillingError(
  error: unknown,
  res: Response,
  notFoundMessage: string,
  invalidRequestMessage?: string,
): boolean {
  const msg = error instanceof Error ? error.message : String(error);
  // KS-144: Stripe-config (invalid/missing key) is a provider-unconfigured outage, not a server fault.
  // KS-445: `Neither apiKey` is stripe-node's constructor throw when the key env var is set but empty.
  if (/Invalid API Key|No API key provided|Neither apiKey|not configured/i.test(msg)) {
    res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Billing provider not configured' } });
    return true;
  }
  // Unknown resource (customer / payment_method / …) → 404. `No such` is Stripe's phrasing.
  if (/No such|resource_missing/i.test(msg)) {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: notFoundMessage } });
    return true;
  }
  // KS-421: the message patterns above miss provider errors phrased any other way (e.g. an
  // invalid id → an invalid_request naming neither pattern). Classify by the structured Stripe fields.
  const providerError = error as { type?: string; statusCode?: number; code?: string };
  const providerStatus = typeof providerError.statusCode === 'number' ? providerError.statusCode : undefined;
  // KS-445: an unreachable provider (network/DNS/timeout) surfaces as stripe-node's
  // StripeConnectionError — no HTTP statusCode at all — so it fell through every branch
  // below to a raw 500. A dependency outage is 503, same as unconfigured. The syscall
  // codes cover a bare Node network error should one bypass the SDK wrapper.
  const NETWORK_ERRNOS = /\b(ECONNREFUSED|ECONNRESET|ENOTFOUND|ETIMEDOUT|EAI_AGAIN|EPIPE)\b/;
  if (
    providerError.type === 'StripeConnectionError' ||
    (typeof providerError.code === 'string' && NETWORK_ERRNOS.test(providerError.code)) ||
    NETWORK_ERRNOS.test(msg)
  ) {
    res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Billing provider unreachable' } });
    return true;
  }
  if (
    providerError.type === 'StripeAuthenticationError' ||
    providerError.type === 'StripePermissionError' ||
    providerStatus === 401 || providerStatus === 403 || providerStatus === 429
  ) {
    res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Billing provider unavailable' } });
    return true;
  }
  if (providerError.type === 'StripeInvalidRequestError' || (providerStatus !== undefined && providerStatus >= 400 && providerStatus < 500)) {
    // KS-445: on body-input routes (create customer / custom checkout) a request-blaming
    // provider 4xx means the body was invalid — there is no id lookup to 404 on.
    if (invalidRequestMessage !== undefined) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: invalidRequestMessage } });
      return true;
    }
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: notFoundMessage } });
    return true;
  }
  return false;
}

// =============================================================================
// KS-1888: WHO MAY ACT ON A STRIPE CUSTOMER
// =============================================================================

/** Metadata keys PUT /customers/:id never writes, for anyone: the balance and the owner record (KS-1888 D3). */
const RESERVED_CUSTOMER_METADATA = ['certificationCredits', 'userId', 'tenantId'];

/**
 * KS-1888 (Wednesday's D1, 2026-10-31): the caller may act on a Stripe customer when they are a platform administrator
 * (the shared isPlatformRole, as KS-1850) or its owner: `metadata.userId` equals the caller's userId, both non-empty
 * strings, exact compare, and where the customer records `metadata.tenantId` it equals the caller's tenantId. A
 * customer with no recorded owner is platform administrators only; tenant roles get nothing beyond their own customer.
 *
 * Limit, not a finding: a customer created before KS-1888 carries whatever userId was last written to it before then, by
 * its creator or by any signed-in caller through the old PUT /customers/:id (KS-1909 asks for the audit), and this trusts it.
 *
 * @param user - the authenticated principal (req.user), possibly absent.
 * @param customer - the Stripe customer, or null/undefined when there is none.
 * @returns true when the caller may act on it; always false when there is no customer.
 */
function mayActOnCustomer(user: unknown, customer: { metadata?: Record<string, string> | null } | null | undefined): boolean {
  if (!customer) return false;
  const caller = (user ?? {}) as { userId?: unknown; role?: unknown; tenantId?: unknown };
  if (isPlatformRole(caller.role as string | undefined)) return true;
  const owner = customer.metadata?.userId;
  if (typeof caller.userId !== 'string' || caller.userId === '' || typeof owner !== 'string' || owner === '') return false;
  if (owner !== caller.userId) return false;
  const recordedTenant = customer.metadata?.tenantId;
  return typeof recordedTenant !== 'string' || recordedTenant === '' || recordedTenant === caller.tenantId;
}

/**
 * KS-1888: may the caller act on the customer an invoice or payment method is attached to? One with no customer is
 * platform administrators only.
 *
 * @param user - the authenticated principal (req.user), possibly absent.
 * @param customer - the object's `customer` field: an id, an expanded customer, or null.
 * @param lookup - how this route reads a customer (getCustomer, or findCustomer where outages must stay 503).
 * @returns true when the caller may act on the object.
 */
async function mayActOnAttachedTo(
  user: unknown,
  customer: string | { id: string } | null | undefined,
  lookup: (customerId: string) => Promise<{ metadata?: Record<string, string> | null } | null>,
): Promise<boolean> {
  const role = (user as { role?: unknown } | undefined)?.role;
  if (isPlatformRole(role as string | undefined)) return true;
  const customerId = typeof customer === 'string' ? customer : customer?.id;
  if (!customerId) return false;
  return mayActOnCustomer(user, await lookup(customerId));
}

/** The 404 each id route answers for an unknown id. KS-1888: a refused caller gets exactly this, so it is no oracle. */
function sendNotFound(res: Response, message: string): void {
  res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message } });
}

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

const CreateCustomerSchema = z.object({
  email: z.string().email(),
  name: z.string().optional(),
  userId: z.string(),
});

const PurchaseBundleSchema = z.object({
  bundleId: z.string(),
  successUrl: z.string().url(),
  cancelUrl: z.string().url(),
  customerEmail: z.string().email().optional(),
});

const PurchaseCustomSchema = z.object({
  quantity: z.number().int().min(1).max(10000),
  successUrl: z.string().url(),
  cancelUrl: z.string().url(),
  customerEmail: z.string().email().optional(),
});

// =============================================================================
// PUBLIC ROUTES - PRICING INFO
// =============================================================================

/**
 * Build the certification-bundle pricing payload (the shape both GET /bundles
 * and GET /pricing return). Shared so the two stay in lockstep and both satisfy
 * the published BillingPricing schema (`{ bundles, currency, … }`, passthrough).
 *
 * @returns the pricing response body: bundles + currency + included features
 */
function buildPricingPayload(): {
  bundles: unknown[];
  currency: string;
  included: typeof INCLUDED_FEATURES;
  payAsYouGoPrice: typeof PAY_AS_YOU_GO_PRICE;
} {
  const config = loadStripeConfig();
  const bundles = CERTIFICATION_BUNDLES.map(bundle => ({
    id: bundle.id,
    name: bundle.name,
    description: bundle.description,
    certifications: bundle.certifications,
    // KS-440: price is numeric major units (spec: number); priceAmount stays
    // minor units (cents); the formatted string lives on displayPrice.
    price: bundle.price / 100,
    displayPrice: formatPrice(bundle.price, config.currency),
    priceAmount: bundle.price,
    pricePerCert: formatPrice(bundle.pricePerCert, config.currency),
    pricePerCertAmount: bundle.pricePerCert,
    savings: bundle.savings || 0,
    popular: bundle.popular || false,
    features: bundle.features,
  }));
  return {
    bundles,
    currency: config.currency,
    included: INCLUDED_FEATURES,
    payAsYouGoPrice: PAY_AS_YOU_GO_PRICE,
  };
}

/**
 * GET /bundles
 * Get all certification bundles (public)
 */
router.get('/bundles', (_req: Request, res: Response) => {
  res.json(buildPricingPayload());
});

/**
 * GET /bundles/:id
 * Get specific bundle details (public)
 */
router.get('/bundles/:id', (req: Request, res: Response) => {
  const config = loadStripeConfig();
  const bundle = getCertificationBundle(req.params.id);
  
  if (!bundle) {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Bundle not found' } });
    return;
  }

  res.json({
    id: bundle.id,
    name: bundle.name,
    description: bundle.description,
    certifications: bundle.certifications,
    // KS-440: same numeric-price shape as buildPricingPayload().
    price: bundle.price / 100,
    displayPrice: formatPrice(bundle.price, config.currency),
    priceAmount: bundle.price,
    pricePerCert: formatPrice(bundle.pricePerCert, config.currency),
    pricePerCertAmount: bundle.pricePerCert,
    savings: bundle.savings || 0,
    popular: bundle.popular || false,
    features: bundle.features,
    currency: config.currency,
    included: INCLUDED_FEATURES,
  });
});

/**
 * GET /config
 * Get Stripe publishable key (public)
 */
router.get('/config', (_req: Request, res: Response) => {
  const stripeService = getStripeService();
  const config = loadStripeConfig();
  
  res.json({
    publishableKey: stripeService.getPublishableKey(),
    mode: stripeService.getMode(),
    currency: config.currency,
  });
});

// =============================================================================
// CUSTOMER ROUTES (Require Auth)
// =============================================================================

/**
 * POST /customers
 * Create a new customer
 */
router.post('/customers', async (req: Request, res: Response) => {
  try {
    const data = CreateCustomerSchema.parse(req.body);
    // KS-1888 D2: the owner comes from the token. A body userId that is not the caller's is refused unless a platform
    // administrator is creating the customer for that user. Answered before Stripe is called.
    const user = (req as any).user as { userId?: unknown; tenantId?: unknown; role?: unknown } | undefined;
    const callerId = typeof user?.userId === 'string' && user.userId !== '' ? user.userId : undefined;
    const ownCustomer = callerId !== undefined && data.userId === callerId;
    if (!ownCustomer && !isPlatformRole(user?.role as string | undefined)) {
      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'userId does not match the caller' } });
      return;
    }
    const stripeService = getStripeService();

    // Check if customer already exists. KS-1888 D2: only one the caller may act on is returned; anyone else gets a new
    // customer of their own, so posting an email never hands over someone else's customer.
    const existing = (await stripeService.listCustomersByEmail(data.email)).find((c) => mayActOnCustomer(user, c));
    if (existing) {
      res.json({ customer: existing, existing: true });
      return;
    }

    // The tenant is recorded only for the caller's own customer; it is never guessed for another user's.
    const tenantId = ownCustomer && typeof user?.tenantId === 'string' && user.tenantId !== '' ? user.tenantId : undefined;
    const customer = await stripeService.createCustomer({
      email: data.email,
      name: data.name,
      userId: ownCustomer ? (callerId as string) : data.userId,
      ...(tenantId ? { metadata: { tenantId } } : {}),
    });
    res.status(201).json({ customer, existing: false });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request', details: zod3Issues(error.issues) } });
      return;
    }
    logger.error('[Billing] Create customer error', { error: error instanceof Error ? error.message : String(error) });
    // KS-445: this route never classified provider errors, so an unconfigured/unreachable
    // Stripe answered a raw 500. Caller input here is the body, so a provider 4xx → 400.
    if (sendClassifiedBillingError(error, res, 'Customer not found', 'Invalid customer details')) return;
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create customer' } });
  }
});

/**
 * GET /customers/by-email
 * Find a customer by email address
 *
 * KS-1888 D4: declared above GET /customers/:id. Below it, Express handed /customers/by-email to the :id handler
 * (id "by-email"), so this route never ran.
 */
router.get('/customers/by-email', async (req: Request, res: Response) => {
  try {
    const email = req.query.email as string;
    if (!email) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'email query parameter is required' } });
      return;
    }

    const stripeService = getStripeService();
    // KS-1888: of the customers with this email, one the caller may act on; someone else's reads like none.
    const customer = (await stripeService.listCustomersByEmail(email)).find((c) => mayActOnCustomer((req as any).user, c));

    if (!customer) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Customer not found' } });
      return;
    }

    res.json({ customer });
  } catch (error) {
    logger.error('[Billing] Find customer by email error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to find customer' } });
  }
});

/**
 * GET /customers/:id
 * Get customer details
 */
router.get('/customers/:id', async (req: Request, res: Response) => {
  try {
    const stripeService = getStripeService();
    const customer = await stripeService.getCustomer(req.params.id);

    // KS-1888: a customer the caller may not act on reads exactly like an unknown one.
    if (!mayActOnCustomer((req as any).user, customer)) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Customer not found' } });
      return;
    }

    res.json({ customer });
  } catch (error) {
    logger.error('[Billing] Get customer error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get customer' } });
  }
});

/**
 * GET /customers/:id/credits
 * Get customer's certification credit balance
 */
router.get('/customers/:id/credits', async (req: Request, res: Response) => {
  try {
    const stripeService = getStripeService();
    // KS-1888: owner or platform administrator. An unknown id is 404 now too (it read as a zero balance), so a
    // customer the caller may not act on and an unknown one answer the same.
    if (!mayActOnCustomer((req as any).user, await stripeService.getCustomer(req.params.id))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
    const balance = await stripeService.getCertificationBalance(req.params.id);
    
    res.json({
      customerId: req.params.id,
      credits: balance,
      unlimited: {
        verifications: true,
        storage: true,
      },
    });
  } catch (error) {
    logger.error('[Billing] Get credits error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get credit balance' } });
  }
});

/**
 * PUT /customers/:id
 * Update customer details
 */
router.put('/customers/:id', async (req: Request, res: Response) => {
  try {
    const UpdateCustomerSchema = z.object({
      email: z.string().email().optional(),
      name: z.string().optional(),
      // KS-1888 D3: the balance and the owner record are not writable here, by anyone. Checked with the body, before
      // the owner check, so a foreign customer and an unknown one answer the same 400.
      metadata: z
        .record(z.string(), z.string())
        .refine((m) => !RESERVED_CUSTOMER_METADATA.some((key) => Object.prototype.hasOwnProperty.call(m, key)), {
          message: `metadata may not set ${RESERVED_CUSTOMER_METADATA.join(', ')}`,
        })
        .optional(),
    });
    const data = UpdateCustomerSchema.parse(req.body);
    const stripeService = getStripeService();
    // KS-1888: owner or platform administrator; findCustomer keeps a provider outage a 503.
    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(req.params.id))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
    const customer = await stripeService.updateCustomer(req.params.id, data);
    res.json({ customer });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request', details: zod3Issues(error.issues) } });
      return;
    }
    logger.error('[Billing] Update customer error', { error: error instanceof Error ? error.message : String(error) });
    if (sendClassifiedBillingError(error, res, 'Customer not found')) return;
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update customer' } });
  }
});

// =============================================================================
// PURCHASE ROUTES
// =============================================================================

/**
 * POST /checkout/bundle
 * Purchase a certification bundle
 */
router.post('/checkout/bundle', async (req: Request, res: Response) => {
  try {
    const data = PurchaseBundleSchema.parse(req.body);
    const stripeService = getStripeService();
    const bundle = getCertificationBundle(data.bundleId);

    if (!bundle) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Bundle not found' } });
      return;
    }

    // Get customer ID from auth if available
    const customerId = (req as any).user?.stripeCustomerId;

    const session = await stripeService.createBundleCheckoutSession({
      customerId,
      customerEmail: data.customerEmail,
      bundleId: bundle.id,
      successUrl: data.successUrl,
      cancelUrl: data.cancelUrl,
    });

    res.json({ 
      sessionId: session.id, 
      url: session.url,
      bundle: {
        id: bundle.id,
        name: bundle.name,
        certifications: bundle.certifications,
        price: bundle.price,
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request', details: zod3Issues(error.issues) } });
      return;
    }
    logger.error('[Billing] Create checkout session error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create checkout session' } });
  }
});

/**
 * POST /checkout/custom
 * Purchase a custom number of certifications
 */
router.post('/checkout/custom', async (req: Request, res: Response) => {
  try {
    const data = PurchaseCustomSchema.parse(req.body);
    const stripeService = getStripeService();

    // Calculate price based on quantity (use best bundle rate)
    const pricePerCert = stripeService.calculatePricePerCert(data.quantity);
    const totalPrice = data.quantity * pricePerCert;

    // Get customer ID from auth if available
    const customerId = (req as any).user?.stripeCustomerId;

    const session = await stripeService.createCustomCheckoutSession({
      customerId,
      customerEmail: data.customerEmail,
      quantity: data.quantity,
      totalPrice,
      successUrl: data.successUrl,
      cancelUrl: data.cancelUrl,
    });

    res.json({ 
      sessionId: session.id, 
      url: session.url,
      purchase: {
        certifications: data.quantity,
        pricePerCert,
        totalPrice,
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request', details: zod3Issues(error.issues) } });
      return;
    }
    logger.error('[Billing] Create custom checkout session error', { error: error instanceof Error ? error.message : String(error) });
    // KS-445: same gap as POST /customers — no classifier meant a raw 500. A "No such
    // customer" (stale req.user.stripeCustomerId) stays 404; any other provider 4xx
    // blames the body → 400.
    if (sendClassifiedBillingError(error, res, 'Customer not found', 'Invalid checkout request')) return;
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create checkout session' } });
  }
});

// =============================================================================
// PAYMENT HISTORY ROUTES
// =============================================================================

/**
 * GET /customers/:customerId/purchases
 * List customer's purchase history
 */
router.get('/customers/:customerId/purchases', async (req: Request, res: Response) => {
  try {
    const limit = parseInt(req.query.limit as string) || 10;
    const stripeService = getStripeService();
    // KS-116: an unknown customer makes Stripe's paymentIntents.list throw
    // ("No such customer") -> 500. Guard with getCustomer (returns null on
    // not-found) and return 404, matching GET /customers/:id. KS-1888: a customer the caller may not act on reads
    // the same.
    const customer = await stripeService.getCustomer(req.params.customerId);
    if (!mayActOnCustomer((req as any).user, customer)) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Customer not found' } });
      return;
    }
    const purchases = await stripeService.listPurchases(req.params.customerId, limit);
    res.json({ purchases });
  } catch (error) {
    logger.error('[Billing] List purchases error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list purchases' } });
  }
});

/**
 * GET /customers/:customerId/invoices
 * List customer invoices
 */
router.get('/customers/:customerId/invoices', async (req: Request, res: Response) => {
  try {
    const limit = parseInt(req.query.limit as string) || 10;
    const stripeService = getStripeService();
    // KS-116: same as /purchases — an unknown customer makes invoices.list
    // throw -> 500. Guard with getCustomer and return 404. KS-1888: a customer the caller may not act on reads the same.
    const customer = await stripeService.getCustomer(req.params.customerId);
    if (!mayActOnCustomer((req as any).user, customer)) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Customer not found' } });
      return;
    }
    const invoices = await stripeService.listInvoices(req.params.customerId, limit);
    res.json({ invoices });
  } catch (error) {
    logger.error('[Billing] List invoices error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list invoices' } });
  }
});

// =============================================================================
// PAYMENT METHOD ROUTES
// =============================================================================

/**
 * POST /customers/:customerId/setup-intent
 * Create setup intent for adding payment method
 */
router.post('/customers/:customerId/setup-intent', async (req: Request, res: Response) => {
  try {
    const stripeService = getStripeService();
    // KS-1888: owner or platform administrator; findCustomer keeps a provider outage a 503.
    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(req.params.customerId))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
    const setupIntent = await stripeService.createSetupIntent(req.params.customerId);
    res.json({ clientSecret: setupIntent.client_secret });
  } catch (error) {
    logger.error('[Billing] Create setup intent error', { error: error instanceof Error ? error.message : String(error) });
    if (sendClassifiedBillingError(error, res, 'Customer not found')) return;
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create setup intent' } });
  }
});

/**
 * GET /customers/:customerId/payment-methods
 * List customer payment methods
 */
router.get('/customers/:customerId/payment-methods', async (req: Request, res: Response) => {
  try {
    const stripeService = getStripeService();
    // KS-1888: owner or platform administrator; findCustomer keeps a provider outage a 503.
    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(req.params.customerId))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
    const paymentMethods = await stripeService.listPaymentMethods(req.params.customerId);
    res.json({ paymentMethods });
  } catch (error) {
    logger.error('[Billing] List payment methods error', { error: error instanceof Error ? error.message : String(error) });
    // KS-431: shared classifier (extracted from the KS-421 inline block below).
    if (sendClassifiedBillingError(error, res, 'Customer not found')) return;
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list payment methods' } });
  }
});

/**
 * POST /customers/:customerId/default-payment-method
 * Set default payment method
 */
router.post('/customers/:customerId/default-payment-method', async (req: Request, res: Response) => {
  try {
    const { paymentMethodId } = req.body;
    // KS-445: a truthiness check alone lets a fuzzer-shaped non-string (number/object)
    // through to the Stripe call — reject anything but a non-empty string up front.
    if (!paymentMethodId || typeof paymentMethodId !== 'string') {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'paymentMethodId is required' } });
      return;
    }

    const stripeService = getStripeService();
    // KS-1888: owner or platform administrator; findCustomer keeps a provider outage a 503.
    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(req.params.customerId))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
    await stripeService.setDefaultPaymentMethod(req.params.customerId, paymentMethodId);
    res.json({ success: true });
  } catch (error) {
    logger.error('[Billing] Set default payment method error', { error: error instanceof Error ? error.message : String(error) });
    if (sendClassifiedBillingError(error, res, 'Customer not found')) return;
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to set default payment method' } });
  }
});

/**
 * DELETE /payment-methods/:id
 * Remove payment method
 */
router.delete('/payment-methods/:id', async (req: Request, res: Response) => {
  try {
    const stripeService = getStripeService();
    // KS-1888: a payment method belongs to the owner of its customer; one the caller may not act on reads like an
    // unknown one. Both lookups throw on a provider outage, so that stays a 503.
    const paymentMethod = await stripeService.getPaymentMethod(req.params.id);
    if (!paymentMethod || !(await mayActOnAttachedTo((req as any).user, paymentMethod.customer, (id) => stripeService.findCustomer(id)))) {
      sendNotFound(res, 'Payment method not found');
      return;
    }
    await stripeService.detachPaymentMethod(req.params.id);
    res.json({ success: true });
  } catch (error) {
    logger.error('[Billing] Detach payment method error', { error: error instanceof Error ? error.message : String(error) });
    if (sendClassifiedBillingError(error, res, 'Payment method not found')) return;
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to remove payment method' } });
  }
});

// =============================================================================
// INVOICE DETAIL ROUTE
// =============================================================================

/**
 * GET /invoices/:id
 * Get a single invoice by ID
 */
router.get('/invoices/:id', async (req: Request, res: Response) => {
  try {
    const stripeService = getStripeService();
    const invoice = await stripeService.getInvoice(req.params.id);

    // KS-1888: an invoice belongs to the owner of its customer; one the caller may not act on reads like an unknown one.
    if (!invoice || !(await mayActOnAttachedTo((req as any).user, invoice.customer, (id) => stripeService.getCustomer(id)))) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Invoice not found' } });
      return;
    }

    res.json({ invoice });
  } catch (error) {
    logger.error('[Billing] Get invoice error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get invoice' } });
  }
});

// =============================================================================
// CREDIT MANAGEMENT ROUTES (Admin)
// =============================================================================

/**
 * POST /admin/credits
 * Add certification credits to a customer (admin only)
 */
router.post('/admin/credits', async (req: Request, res: Response) => {
  try {
    // Admin only — verify role from gateway auth.
    // Pen-test F-04: read role ONLY from authenticated req.user (set by
    // authenticate() middleware) — fallback to raw headers was spoofable.
    // KS-1850: platform administrators only (the shared isPlatformRole: SYSTEM_ADMIN / SUPER_ADMIN, ASCII case
    // fold only). Before, the list was ['SYSTEM_ADMIN', 'ORG_ADMIN', 'OWNER']: OWNER is every self-registered
    // user, and ORG_ADMIN is a tenant role while customerId crosses customers. The 403 body is unchanged, and it
    // is answered before the body is parsed or Stripe is called.
    if (!isPlatformRole((req as any).user?.role)) {
      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } });
      return;
    }

    const AdminCreditsSchema = z.object({
      customerId: z.string().min(1),
      credits: z.number().int().positive(),
    });
    const data = AdminCreditsSchema.parse(req.body);
    const stripeService = getStripeService();
    const newBalance = await stripeService.addCertificationCredits(data.customerId, data.credits);

    res.json({
      customerId: data.customerId,
      creditsAdded: data.credits,
      newBalance,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request', details: zod3Issues(error.issues) } });
      return;
    }
    logger.error('[Billing] Add credits error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to add credits' } });
  }
});

/**
 * POST /credits/use
 * Use certification credits from a customer's balance
 */
router.post('/credits/use', async (req: Request, res: Response) => {
  try {
    const UseCreditsSchema = z.object({
      customerId: z.string().min(1),
      credits: z.number().int().positive(),
    });
    const data = UseCreditsSchema.parse(req.body);
    const stripeService = getStripeService();
    // KS-1888: only the customer's owner or a platform administrator spends its credits; findCustomer keeps a provider
    // outage a 503.
    if (!mayActOnCustomer((req as any).user, await stripeService.findCustomer(data.customerId))) {
      sendNotFound(res, 'Customer not found');
      return;
    }
    const result = await stripeService.useCertificationCredits(data.customerId, data.credits);

    if (!result.success) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Insufficient credits', currentBalance: result.newBalance, requested: data.credits },
      });
      return;
    }

    res.json({
      success: true,
      customerId: data.customerId,
      creditsUsed: data.credits,
      newBalance: result.newBalance,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request', details: zod3Issues(error.issues) } });
      return;
    }
    // KS-445: a fuzzed customerId reaching the provider throws (No such customer /
    // unconfigured / unreachable) — classify like every other billing op instead
    // of leaking a raw 500. customerId is an id lookup, so provider 4xx → 404.
    if (sendClassifiedBillingError(error, res, 'Customer not found')) return;
    logger.error('[Billing] Use credits error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to use credits' } });
  }
});

// =============================================================================
// LEGACY ROUTES (deprecated - kept for backwards compatibility)
// =============================================================================

/**
 * GET /pricing - public pricing summary.
 *
 * KS-452: this previously `res.redirect(301, '/billing/bundles')`. Through the
 * gateway that relative Location resolved to `/billing/bundles` (a non-`/api`
 * path), which nginx served as the issuer-portal SPA `index.html` — so a
 * spec-`application/json` endpoint answered 200 `text/html` (SPA fallthrough).
 * The published contract (BillingPricing) is JSON, so return the pricing
 * payload directly rather than bouncing the caller onto a browser route.
 */
router.get('/pricing', (_req: Request, res: Response) => {
  res.json(buildPricingPayload());
});

export default router;
