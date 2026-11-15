/**
 * =============================================================================
 * STRIPE SERVICE
 * =============================================================================
 * Core Stripe integration for certification bundle purchases
 * 
 * PRICING MODEL: One-time purchase certification bundles
 * - Credits never expire
 * - Verifications are FREE
 * - Storage is FREE
 */

import Stripe from 'stripe';
import { 
  loadStripeConfig, 
  StripeConfig, 
  CERTIFICATION_BUNDLES,
  STRIPE_PRODUCT_IDS, 
  getCertificationBundle,
  PAY_AS_YOU_GO_PRICE,
  loadStripeProductIds,
} from '../config/stripe.config';
import { logger } from '../utils/logger';

// =============================================================================
// TYPES
// =============================================================================

export interface Customer {
  id: string;
  stripeCustomerId: string;
  email: string;
  name?: string;
  metadata?: Record<string, string>;
}

export interface PaymentMethod {
  id: string;
  type: string;
  card?: {
    brand: string;
    last4: string;
    expMonth: number;
    expYear: number;
  };
  isDefault: boolean;
}

export interface Invoice {
  id: string;
  stripeInvoiceId: string;
  customerId: string;
  amountDue: number;
  amountPaid: number;
  currency: string;
  status: string;
  invoiceUrl?: string;
  invoicePdf?: string;
  createdAt: Date;
  paidAt?: Date;
}

export interface Purchase {
  id: string;
  bundleId?: string;
  bundleName?: string;
  certifications: number;
  amount: number;
  currency: string;
  status: string;
  createdAt: Date;
}

// =============================================================================
// SERVICE
// =============================================================================

/**
 * KS-1888: is this Stripe error "the object does not exist"? Stripe answers an unknown id with code `resource_missing`,
 * HTTP 404 and a "No such ..." message; any of the three counts. Everything else is a provider failure.
 */
function isMissingResource(error: unknown): boolean {
  const e = (error ?? {}) as { code?: unknown; statusCode?: unknown; message?: unknown };
  return e.code === 'resource_missing' || e.statusCode === 404 || /No such/i.test(String(e.message ?? ''));
}

export class StripeService {
  private stripe: Stripe;
  private config: StripeConfig;

  constructor() {
    this.config = loadStripeConfig();
    
    this.stripe = new Stripe(this.config.secretKey, {
      apiVersion: '2023-10-16',
      typescript: true,
    });

    // Load product IDs from environment
    loadStripeProductIds();

    logger.info('[Stripe] Initialized', { mode: this.config.mode });
  }

  /**
   * Get publishable key for frontend
   */
  getPublishableKey(): string {
    return this.config.publishableKey;
  }

  /**
   * Get current mode
   */
  getMode(): 'test' | 'live' {
    return this.config.mode;
  }

  // ===========================================================================
  // CUSTOMERS
  // ===========================================================================

  /**
   * Create a Stripe customer
   */
  async createCustomer(params: {
    email: string;
    name?: string;
    userId: string;
    metadata?: Record<string, string>;
  }): Promise<Stripe.Customer> {
    const customer = await this.stripe.customers.create({
      email: params.email,
      name: params.name,
      metadata: {
        userId: params.userId,
        certificationCredits: '0', // Track credits in metadata
        ...params.metadata,
      },
    });

    logger.info('[Stripe] Created customer', { customerId: customer.id });
    return customer;
  }

  /**
   * Get customer by ID
   */
  async getCustomer(customerId: string): Promise<Stripe.Customer | null> {
    try {
      const customer = await this.stripe.customers.retrieve(customerId);
      if (customer.deleted) return null;
      return customer as Stripe.Customer;
    } catch (error) {
      return null;
    }
  }

  /**
   * KS-1888: get a customer for an access check. Unlike getCustomer, only "it does not exist" (or deleted) is null; a
   * provider failure (unconfigured, unreachable, throttled) is thrown, so the route's classifier still answers 503
   * instead of a 404 that blames the caller.
   */
  async findCustomer(customerId: string): Promise<Stripe.Customer | null> {
    try {
      const customer = await this.stripe.customers.retrieve(customerId);
      if (customer.deleted) return null;
      return customer as Stripe.Customer;
    } catch (error) {
      if (isMissingResource(error)) return null;
      throw error;
    }
  }

  /**
   * Update customer
   */
  async updateCustomer(
    customerId: string,
    params: {
      email?: string;
      name?: string;
      metadata?: Record<string, string>;
    }
  ): Promise<Stripe.Customer> {
    return this.stripe.customers.update(customerId, params);
  }

  /**
   * Find customer by email
   */
  async findCustomerByEmail(email: string): Promise<Stripe.Customer | null> {
    const customers = await this.stripe.customers.list({
      email,
      limit: 1,
    });
    return customers.data[0] || null;
  }

  /**
   * KS-1888: every customer with this email (Stripe allows duplicates), so a route can pick the caller's own instead
   * of Stripe's first match.
   */
  async listCustomersByEmail(email: string): Promise<Stripe.Customer[]> {
    const customers = await this.stripe.customers.list({
      email,
      limit: 100,
    });
    return customers.data;
  }

  /**
   * Get customer's certification credit balance
   */
  async getCertificationBalance(customerId: string): Promise<number> {
    const customer = await this.getCustomer(customerId);
    if (!customer) return 0;
    
    const credits = parseInt(customer.metadata?.certificationCredits || '0', 10);
    return isNaN(credits) ? 0 : credits;
  }

  /**
   * Add certification credits to customer (optimistic locking with retry)
   */
  async addCertificationCredits(customerId: string, credits: number): Promise<number> {
    const maxRetries = 3;
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      const customer = await this.stripe.customers.retrieve(customerId);
      if (customer.deleted) throw new Error('Customer deleted');
      const currentBalance = parseInt(customer.metadata?.certificationCredits || '0', 10);
      const newBalance = currentBalance + credits;

      await this.stripe.customers.update(customerId, {
        metadata: { certificationCredits: String(newBalance) },
      });

      // Verify the balance was not changed by a concurrent update
      const verify = await this.stripe.customers.retrieve(customerId);
      if (!verify.deleted && parseInt(verify.metadata?.certificationCredits || '0', 10) === newBalance) {
        logger.info('[Stripe] Added credits', { credits, customerId, newBalance });
        return newBalance;
      }
      logger.warn('[Stripe] Credit update conflict, retrying', { attempt, customerId });
    }
    throw new Error('Failed to update credits after retries');
  }

  /**
   * Use certification credits (optimistic locking with retry)
   */
  async useCertificationCredits(customerId: string, credits: number): Promise<{ success: boolean; newBalance: number }> {
    const maxRetries = 3;
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      const customer = await this.stripe.customers.retrieve(customerId);
      if (customer.deleted) throw new Error('Customer deleted');
      const currentBalance = parseInt(customer.metadata?.certificationCredits || '0', 10);

      if (currentBalance < credits) {
        return { success: false, newBalance: currentBalance };
      }

      const newBalance = currentBalance - credits;

      await this.stripe.customers.update(customerId, {
        metadata: { certificationCredits: String(newBalance) },
      });

      // Verify the balance was not changed by a concurrent update
      const verify = await this.stripe.customers.retrieve(customerId);
      if (!verify.deleted && parseInt(verify.metadata?.certificationCredits || '0', 10) === newBalance) {
        logger.info('[Stripe] Used credits', { credits, customerId, newBalance });
        return { success: true, newBalance };
      }
      logger.warn('[Stripe] Credit update conflict, retrying', { attempt, customerId });
    }
    throw new Error('Failed to update credits after retries');
  }

  // ===========================================================================
  // BUNDLE CHECKOUT
  // ===========================================================================

  /**
   * Create checkout session for bundle purchase
   */
  async createBundleCheckoutSession(params: {
    customerId?: string;
    customerEmail?: string;
    bundleId: string;
    successUrl: string;
    cancelUrl: string;
    metadata?: Record<string, string>;
  }): Promise<Stripe.Checkout.Session> {
    const bundle = getCertificationBundle(params.bundleId);
    if (!bundle) {
      throw new Error(`Invalid bundle: ${params.bundleId}`);
    }

    const stripeIds = STRIPE_PRODUCT_IDS[params.bundleId];
    if (!stripeIds) {
      // If product IDs aren't in env, create a price on the fly
      logger.info('[Stripe] Creating ad-hoc price for bundle', { bundleId: params.bundleId });
    }

    const sessionParams: Stripe.Checkout.SessionCreateParams = {
      mode: 'payment', // One-time payment, not subscription
      line_items: stripeIds?.priceId 
        ? [{ price: stripeIds.priceId, quantity: 1 }]
        : [{
            price_data: {
              currency: this.config.currency,
              product_data: {
                name: `Secuura ${bundle.name}`,
                description: `${bundle.certifications} document certifications`,
                metadata: {
                  bundleId: bundle.id,
                  certifications: bundle.certifications.toString(),
                },
              },
              unit_amount: bundle.price,
            },
            quantity: 1,
          }],
      success_url: params.successUrl,
      cancel_url: params.cancelUrl,
      metadata: {
        bundleId: bundle.id,
        certifications: bundle.certifications.toString(),
        ...params.metadata,
      },
      payment_intent_data: {
        metadata: {
          bundleId: bundle.id,
          certifications: bundle.certifications.toString(),
        },
      },
    };

    if (params.customerId) {
      sessionParams.customer = params.customerId;
    } else if (params.customerEmail) {
      sessionParams.customer_email = params.customerEmail;
    }

    return this.stripe.checkout.sessions.create(sessionParams);
  }

  /**
   * Create checkout session for custom quantity purchase
   */
  async createCustomCheckoutSession(params: {
    customerId?: string;
    customerEmail?: string;
    quantity: number;
    totalPrice: number;
    successUrl: string;
    cancelUrl: string;
    metadata?: Record<string, string>;
  }): Promise<Stripe.Checkout.Session> {
    const sessionParams: Stripe.Checkout.SessionCreateParams = {
      mode: 'payment',
      line_items: [{
        price_data: {
          currency: this.config.currency,
          product_data: {
            name: `Secuura Certification Credits`,
            description: `${params.quantity} document certifications`,
            metadata: {
              type: 'custom',
              certifications: params.quantity.toString(),
            },
          },
          unit_amount: params.totalPrice,
        },
        quantity: 1,
      }],
      success_url: params.successUrl,
      cancel_url: params.cancelUrl,
      metadata: {
        type: 'custom',
        certifications: params.quantity.toString(),
        ...params.metadata,
      },
      payment_intent_data: {
        metadata: {
          type: 'custom',
          certifications: params.quantity.toString(),
        },
      },
    };

    if (params.customerId) {
      sessionParams.customer = params.customerId;
    } else if (params.customerEmail) {
      sessionParams.customer_email = params.customerEmail;
    }

    return this.stripe.checkout.sessions.create(sessionParams);
  }

  /**
   * Calculate best price per certification for a quantity
   */
  calculatePricePerCert(quantity: number): number {
    // Find the best bundle rate for the quantity
    const sortedBundles = [...CERTIFICATION_BUNDLES]
      .filter(b => b.id !== 'single') // Exclude single purchase
      .sort((a, b) => a.pricePerCert - b.pricePerCert); // Sort by best price

    // Find the bundle that applies based on quantity
    for (const bundle of sortedBundles) {
      if (quantity >= bundle.certifications) {
        return bundle.pricePerCert;
      }
    }

    // For smaller quantities, find proportional pricing
    if (quantity >= 5) {
      // Give small discount for 5+ certs
      return Math.round(PAY_AS_YOU_GO_PRICE * 0.9); // 10% off
    }

    // Default to pay-as-you-go
    return PAY_AS_YOU_GO_PRICE;
  }

  // ===========================================================================
  // PURCHASE HISTORY
  // ===========================================================================

  /**
   * List customer purchases
   */
  async listPurchases(customerId: string, limit: number = 10): Promise<Purchase[]> {
    const paymentIntents = await this.stripe.paymentIntents.list({
      customer: customerId,
      limit,
    });

    return paymentIntents.data
      .filter(pi => pi.status === 'succeeded')
      .map(pi => {
        const bundleId = pi.metadata?.bundleId;
        const bundle = bundleId ? getCertificationBundle(bundleId) : null;
        
        return {
          id: pi.id,
          bundleId: bundleId || undefined,
          bundleName: bundle?.name,
          certifications: parseInt(pi.metadata?.certifications || '0', 10),
          amount: pi.amount,
          currency: pi.currency,
          status: pi.status,
          createdAt: new Date(pi.created * 1000),
        };
      });
  }

  // ===========================================================================
  // PAYMENT METHODS
  // ===========================================================================

  /**
   * Create setup intent for adding payment method
   */
  async createSetupIntent(customerId: string): Promise<Stripe.SetupIntent> {
    return this.stripe.setupIntents.create({
      customer: customerId,
      payment_method_types: ['card'],
    });
  }

  /**
   * List customer payment methods
   */
  async listPaymentMethods(customerId: string): Promise<Stripe.PaymentMethod[]> {
    const methods = await this.stripe.paymentMethods.list({
      customer: customerId,
      type: 'card',
    });
    return methods.data;
  }

  /**
   * Set default payment method
   */
  async setDefaultPaymentMethod(
    customerId: string,
    paymentMethodId: string
  ): Promise<Stripe.Customer> {
    return this.stripe.customers.update(customerId, {
      invoice_settings: {
        default_payment_method: paymentMethodId,
      },
    });
  }

  /**
   * KS-1888: get a payment method for an access check; null only when Stripe says it does not exist, a provider failure
   * is thrown (as findCustomer).
   */
  async getPaymentMethod(paymentMethodId: string): Promise<Stripe.PaymentMethod | null> {
    try {
      return await this.stripe.paymentMethods.retrieve(paymentMethodId);
    } catch (error) {
      if (isMissingResource(error)) return null;
      throw error;
    }
  }

  /**
   * Detach payment method
   */
  async detachPaymentMethod(paymentMethodId: string): Promise<Stripe.PaymentMethod> {
    return this.stripe.paymentMethods.detach(paymentMethodId);
  }

  // ===========================================================================
  // INVOICES
  // ===========================================================================

  /**
   * List customer invoices
   */
  async listInvoices(customerId: string, limit: number = 10): Promise<Stripe.Invoice[]> {
    const invoices = await this.stripe.invoices.list({
      customer: customerId,
      limit,
    });
    return invoices.data;
  }

  /**
   * Get invoice
   */
  async getInvoice(invoiceId: string): Promise<Stripe.Invoice | null> {
    try {
      return await this.stripe.invoices.retrieve(invoiceId);
    } catch (error) {
      return null;
    }
  }

  // ===========================================================================
  // WEBHOOKS
  // ===========================================================================

  /**
   * Construct webhook event from payload
   */
  constructWebhookEvent(
    payload: string | Buffer,
    signature: string
  ): Stripe.Event {
    if (!this.config.webhookSecret) {
      throw new Error('Webhook secret not configured');
    }

    return this.stripe.webhooks.constructEvent(
      payload,
      signature,
      this.config.webhookSecret
    );
  }

  /**
   * Handle successful payment - add credits to customer
   */
  async handleSuccessfulPayment(paymentIntent: Stripe.PaymentIntent): Promise<void> {
    const customerId = paymentIntent.customer as string;
    const certifications = parseInt(paymentIntent.metadata?.certifications || '0', 10);

    if (customerId && certifications > 0) {
      await this.addCertificationCredits(customerId, certifications);
      logger.info('[Stripe] Payment processed — credits added', { paymentId: paymentIntent.id, certifications, customerId });
    }
  }

  /**
   * Handle checkout session completed - add credits
   */
  async handleCheckoutCompleted(session: Stripe.Checkout.Session): Promise<void> {
    const customerId = session.customer as string;
    const certifications = parseInt(session.metadata?.certifications || '0', 10);

    if (customerId && certifications > 0) {
      await this.addCertificationCredits(customerId, certifications);
      logger.info('[Stripe] Checkout completed — credits added', { sessionId: session.id, certifications, customerId });
    }
  }
}

// Singleton instance
let stripeServiceInstance: StripeService | null = null;

export function getStripeService(): StripeService {
  if (!stripeServiceInstance) {
    stripeServiceInstance = new StripeService();
  }
  return stripeServiceInstance;
}

export default StripeService;
