/**
 * =============================================================================
 * CHARGE EVENT SERVICE (within Originate)
 * =============================================================================
 * Creates and tracks chargeable events alongside certifications.
 * Stores charge events in PostgreSQL via raw queries.
 * Database is the single source of truth.
 *
 * Pricing is loaded from the pricing_config database table on startup,
 * falling back to hardcoded defaults if the table is unavailable.
 * =============================================================================
 */

import { prisma } from '../db';
import { logger } from '../utils/logger';

export type ChargeEventType =
  | 'certification_sign'
  | 'blockchain_anchor'
  | 'verification'
  | 'verification_certificate'
  | 'rights_transfer'
  | 'share'
  | 'premium_timestamp'
  | 'evidence_export'
  | 'api_access';

export type FeeStatus = 'chargeable' | 'free' | 'free_in_context';

export interface ChargeEventRecord {
  id: string;
  eventType: ChargeEventType;
  certificationId: string;
  initiatedBy: string;
  amount: number;
  currency: string;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  feeStatus: FeeStatus;
  typicalPayer?: string;
  metadata?: Record<string, unknown>;
  createdAt: string;
}

// Default pricing fallback (in smallest currency unit — lovelace for ADA, cents for USD)
const DEFAULT_PRICING: Record<string, { ada: number; usd: number; typicalPayer?: string }> = {
  certification_sign:      { ada: 5_000_000, usd: 200, typicalPayer: 'Issuer / Certifier' },
  blockchain_anchor:       { ada: 2_000_000, usd: 80,  typicalPayer: 'Issuer / Certifier' },
  verification:            { ada: 500_000,   usd: 20,  typicalPayer: 'Verifier / Employer' },
  verification_certificate:{ ada: 3_000_000, usd: 120, typicalPayer: 'Verifier (free in recruitment context)' },
  rights_transfer:         { ada: 3_000_000, usd: 120, typicalPayer: 'Rights Holder' },
  share:                   { ada: 0,         usd: 0,   typicalPayer: 'No charge' },
  premium_timestamp:       { ada: 10_000_000,usd: 400, typicalPayer: 'Requesting party' },
  evidence_export:         { ada: 1_000_000, usd: 40,  typicalPayer: 'Requesting party' },
  api_access:              { ada: 100_000,   usd: 4,   typicalPayer: 'API consumer' },
};

// Live pricing cache (loaded from DB on startup, refreshed periodically)
let livePricing: Record<string, { ada: number; usd: number; typicalPayer?: string }> = { ...DEFAULT_PRICING };

/**
 * Load pricing from the pricing_config database table.
 * Called on service startup and can be refreshed at runtime.
 */
export async function loadPricing(): Promise<void> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT event_type, ada_amount, usd_amount, typical_payer FROM pricing_config WHERE is_active = true
    `;
    if (rows.length > 0) {
      const dbPricing: Record<string, { ada: number; usd: number; typicalPayer?: string }> = {};
      for (const r of rows) {
        dbPricing[r.event_type] = {
          ada: Number(r.ada_amount),
          usd: Number(r.usd_amount),
          typicalPayer: r.typical_payer || undefined,
        };
      }
      livePricing = { ...DEFAULT_PRICING, ...dbPricing };
      logger.info('Pricing loaded from database', { eventTypes: rows.length });
    }
  } catch (err: any) {
    logger.warn('Failed to load pricing from DB, using defaults', { error: err?.message });
  }
}

/**
 * Get the current pricing table (for API exposure).
 */
export function getPricingTable(): Record<string, { ada: number; usd: number; typicalPayer?: string }> {
  return { ...livePricing };
}

/**
 * Update a single event type's pricing in the database.
 */
export async function updatePricing(
  eventType: string,
  adaAmount: number,
  usdAmount: number,
): Promise<boolean> {
  try {
    const result = await prisma.$executeRaw`
      UPDATE pricing_config SET ada_amount = ${adaAmount}::bigint, usd_amount = ${usdAmount}::bigint, updated_at = NOW()
      WHERE event_type = ${eventType}
    `;
    if (result > 0) {
      await loadPricing(); // Refresh cache
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

// =============================================================================
// DB READINESS CHECK
// =============================================================================

export async function verifyDbReady(): Promise<void> {
  try {
    await prisma.$queryRaw`SELECT 1`;
    logger.info('chargeEvents: database connection verified');
  } catch (err: any) {
    logger.error('chargeEvents: database connection FAILED — charge events will not be available', {
      error: err instanceof Error ? err.message : String(err),
    });
    throw new Error('Database is required for charge event operations');
  }
}

/**
 * Create a charge event and persist it to the database.
 * Returns the charge event with its ID so it can be linked to lineage data.
 *
 * KS-25b: every write is tenant-scoped. The caller passes the effective
 * tenant id (req.tenantId after extractTenantContext, with the same default
 * fallback as documents/certifications routes). The DB has NOT NULL +
 * RLS on tenant_id since migration 013, so a missing or wrong tenantId
 * fails loud.
 */
export async function createChargeEvent(
  eventType: ChargeEventType,
  certificationId: string,
  initiatedBy: string,
  tenantId: string,
  opts?: {
    currency?: 'ADA' | 'USD';
    feeStatus?: FeeStatus;
    metadata?: Record<string, unknown>;
  },
): Promise<ChargeEventRecord> {
  const currency = opts?.currency || 'ADA';
  const pricing = livePricing[eventType] || DEFAULT_PRICING[eventType] || { ada: 0, usd: 0 };
  const amount = currency === 'ADA' ? pricing.ada : pricing.usd;
  const feeStatus = opts?.feeStatus || (amount > 0 ? 'chargeable' : 'free');
  const typicalPayer = pricing.typicalPayer;

  // Pen-test F-09: charge-event IDs are billing-relevant. Use a CSPRNG.
  const id = `ce_${require('crypto').randomUUID()}`;
  const now = new Date().toISOString();

  const record: ChargeEventRecord = {
    id,
    eventType,
    certificationId,
    initiatedBy,
    amount,
    currency,
    status: 'completed',
    feeStatus,
    typicalPayer,
    metadata: opts?.metadata,
    createdAt: now,
  };

  // Persist to DB
  try {
    await prisma.$executeRaw`
      INSERT INTO charge_events (id, event_type, certification_id, initiated_by, tenant_id, amount, currency, status, fee_status, typical_payer, metadata, created_at)
      VALUES (
        ${id}, ${eventType}, ${certificationId}, ${initiatedBy}, ${tenantId}::uuid,
        ${amount}::bigint, ${currency}, ${'completed'}, ${feeStatus},
        ${typicalPayer || null}, ${JSON.stringify(record.metadata || {})}::jsonb, ${new Date()}
      )
    `;
  } catch (err: any) {
    logger.error('Failed to persist charge event to DB', { error: err?.message });
    throw err;
  }

  logger.info('Charge event created', { eventType, certificationId, initiatedBy, amount: formatAmount(amount, currency), feeStatus });
  return record;
}

/**
 * Get all charge events for a certification (tenant-scoped).
 */
export async function getChargeEventsByCertification(
  certificationId: string,
  tenantId: string,
): Promise<ChargeEventRecord[]> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM charge_events
       WHERE certification_id = ${certificationId}
         AND tenant_id = ${tenantId}::uuid
       ORDER BY created_at ASC
    `;
    return rows.map((r) => ({
      id: r.id,
      eventType: r.event_type,
      certificationId: r.certification_id,
      initiatedBy: r.initiated_by,
      amount: Number(r.amount),
      currency: r.currency,
      status: r.status,
      feeStatus: r.fee_status || 'chargeable',
      typicalPayer: r.typical_payer,
      metadata: r.metadata,
      createdAt: r.created_at?.toISOString?.() || r.created_at,
    }));
  } catch (err: any) {
    logger.warn('Failed to fetch charge events from DB', { error: err?.message });
    throw err;
  }
}

export interface UsageSummaryRow {
  eventType: string;
  count: number;
  adaTotal: number; // ADA (lovelace ÷ 1e6)
  usdTotal: number; // USD (cents ÷ 100)
}

export interface UsageSummary {
  tenantId: string;
  from: string | null;
  to: string | null;
  byEventType: UsageSummaryRow[];
  totals: { count: number; adaTotal: number; usdTotal: number };
}

/**
 * Aggregate this tenant's recorded metering (charge_events) by event type over an
 * optional [from, to] window — the data behind the partner-facing usage/read API
 * (KS-320, Option 2). adaTotal rolls up the actual chain-native ADA charged
 * (lovelace ÷ 1e6). usdTotal is the list-price USD value of the usage (KS-335,
 * Option A): chargeable events × the event type's configured USD price — the
 * platform records charges in ADA, so the USD figure is derived from the price
 * catalog, not summed from USD-recorded rows. Tenant-scoped via an
 * explicit WHERE tenant_id (RLS is fail-open in single-tenancy — migrations
 * 009/013 — so the explicit filter is the real boundary).
 *
 * Args:
 *   tenantId: the caller's tenant (from the authenticated context, never the body).
 *   from / to: optional inclusive ISO-8601 bounds on created_at; null = unbounded.
 *
 * Returns: per-event-type counts + ADA/USD totals, plus grand totals.
 */
export async function getUsageSummary(
  tenantId: string,
  from?: string | null,
  to?: string | null,
): Promise<UsageSummary> {
  const fromTs = from || null;
  const toTs = to || null;
  const rows: any[] = await prisma.$queryRaw`
    SELECT event_type,
           COUNT(*)::int AS count,
           COALESCE(SUM(CASE WHEN currency = 'ADA' THEN amount ELSE 0 END), 0)::bigint AS ada_total,
           SUM(CASE WHEN amount > 0 THEN 1 ELSE 0 END)::int AS chargeable_count
      FROM charge_events
     WHERE tenant_id = ${tenantId}::uuid
       AND status = 'completed'
       AND (${fromTs}::timestamptz IS NULL OR created_at >= ${fromTs}::timestamptz)
       AND (${toTs}::timestamptz IS NULL OR created_at <= ${toTs}::timestamptz)
     GROUP BY event_type
     ORDER BY event_type
  `;
  const byEventType: UsageSummaryRow[] = rows.map((r) => {
    // KS-335 / Option A: usdTotal is the list-price USD value of the metered usage —
    // chargeable events × the event type's configured USD price — NOT a sum of
    // USD-recorded amounts. Every charge_event is recorded chain-native in ADA, so a
    // `currency = 'USD'` sum is always 0; the USD prices live in pricing_config /
    // DEFAULT_PRICING (loaded into livePricing) and are applied here. We use the same
    // `amount > 0` chargeable basis as ada_total, so free events (amount 0) are
    // excluded from both totals. adaTotal stays the actual chain-native ADA charged.
    const price = livePricing[r.event_type] || DEFAULT_PRICING[r.event_type] || { ada: 0, usd: 0 };
    const usdCents = Number(r.chargeable_count) * price.usd;
    return {
      eventType: r.event_type,
      count: Number(r.count),
      adaTotal: Number(r.ada_total) / 1_000_000,
      usdTotal: usdCents / 100,
    };
  });
  const totals = byEventType.reduce(
    (acc, r) => ({ count: acc.count + r.count, adaTotal: acc.adaTotal + r.adaTotal, usdTotal: acc.usdTotal + r.usdTotal }),
    { count: 0, adaTotal: 0, usdTotal: 0 },
  );
  return { tenantId, from: fromTs, to: toTs, byEventType, totals };
}

/**
 * Format a currency amount for logging.
 */
function formatAmount(amount: number, currency: string): string {
  if (currency === 'ADA') return `₳${(amount / 1_000_000).toFixed(2)}`;
  return `$${(amount / 100).toFixed(2)}`;
}
