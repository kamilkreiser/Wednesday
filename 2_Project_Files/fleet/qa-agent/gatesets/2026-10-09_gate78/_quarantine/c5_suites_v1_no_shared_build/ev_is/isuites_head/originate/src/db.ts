/**
 * =============================================================================
 * DATABASE CLIENT — Multi-Tenancy Aware
 * =============================================================================
 * When MULTI_TENANCY_ENABLED=true:
 *   Uses TenantPoolManager to route queries to the correct tenant database.
 *   The `prisma` export provides a Prisma-compatible interface ($queryRaw,
 *   $executeRaw) backed by pg pools — so existing code works unchanged.
 *
 * When MULTI_TENANCY_ENABLED=false (default):
 *   Uses a standard PrismaClient singleton — identical to previous behavior.
 * =============================================================================
 */

import { TenantPoolManager, currentTenantId, isPlatformScope, queryWithTenantGuc } from '@secuura/shared';
import { config } from './config';

// ---------------------------------------------------------------------------
// Feature flag
// ---------------------------------------------------------------------------

const MULTI_TENANCY = process.env.MULTI_TENANCY_ENABLED === 'true';

// ---------------------------------------------------------------------------
// TenantPoolManager (used when multi-tenancy is enabled)
// ---------------------------------------------------------------------------

let tenantManager: TenantPoolManager | null = null;

export function getTenantManager(): TenantPoolManager | null {
  return tenantManager;
}

// ---------------------------------------------------------------------------
// Prisma-compatible wrapper for pg Pool
// ---------------------------------------------------------------------------

/**
 * Creates an object with $queryRaw and $executeRaw that work like Prisma's
 * tagged template literal queries but use a pg Pool underneath.
 *
 * Prisma tagged template: prisma.$queryRaw`SELECT * FROM t WHERE id = ${id}::uuid`
 * This converts to: pool.query('SELECT * FROM t WHERE id = $1::uuid', [id])
 */
export function createPoolProxy(pool: any) {
  function processTemplate(strings: TemplateStringsArray, ...values: any[]): { text: string; params: any[] } {
    let text = '';
    const params: any[] = [];
    for (let i = 0; i < strings.length; i++) {
      text += strings[i];
      if (i < values.length) {
        params.push(values[i]);
        text += `$${params.length}`;
      }
    }
    return { text, params };
  }

  // KS-458 (fail-closed RLS): every statement must carry the active tenant /
  // platform scope GUC INSIDE its own transaction (set_config is_local +
  // pgbouncer transaction pooling). `pool` here is either a real pg Pool
  // (route-level proxies, defaultProxy) or an already-checked-out PoolClient
  // handed out by withTenant() — a PoolClient has `.release`, a Pool doesn't.
  // For a Pool, funnel through queryWithTenantGuc (BEGIN → set_config → query
  // → COMMIT when a scope is active; plain pool.query otherwise). For a
  // withTenant client the GUCs were already applied right after BEGIN, and
  // the statement must stay on that open transaction — query directly.
  const isTxClient = typeof pool.release === 'function';
  const runQuery = (text: string, params: any[]): Promise<any> =>
    isTxClient ? pool.query(text, params) : queryWithTenantGuc(pool, text, params);

  return {
    $queryRaw: async (strings: TemplateStringsArray, ...values: any[]): Promise<any[]> => {
      const { text, params } = processTemplate(strings, ...values);
      const result = await runQuery(text, params);
      return result.rows;
    },

    $executeRaw: async (strings: TemplateStringsArray, ...values: any[]): Promise<number> => {
      const { text, params } = processTemplate(strings, ...values);
      const result = await runQuery(text, params);
      return result.rowCount ?? 0;
    },

    $queryRawUnsafe: async (text: string, ...params: any[]): Promise<any[]> => {
      const result = await runQuery(text, params);
      return result.rows;
    },

    $executeRawUnsafe: async (text: string, ...params: any[]): Promise<number> => {
      const result = await runQuery(text, params);
      return result.rowCount ?? 0;
    },

    $disconnect: async (): Promise<void> => {
      // Pool lifecycle managed by TenantPoolManager — don't close here
    },
  };
}

// ---------------------------------------------------------------------------
// Default pool proxy (used for non-request-scoped operations like startup)
// ---------------------------------------------------------------------------

let defaultProxy: ReturnType<typeof createPoolProxy> | null = null;

// ---------------------------------------------------------------------------
// Prisma fallback (used when multi-tenancy is disabled)
// ---------------------------------------------------------------------------

let prismaClient: any = null;

function getPrismaClient() {
  if (!prismaClient) {
    // Dynamic import to avoid loading Prisma when using pg pools
    // KS-1305: a fresh worktree has @prisma/client installed but NOT generated
    // (npm ci runs with ignore-scripts, so prisma generate never ran); the bare
    // require below then fails as a module error that reads like a product
    // defect. Load it once here and name the cause and the command instead;
    // every other error is rethrown unchanged. On success the require below
    // reads the module cache.
    try {
      require('@prisma/client');
    } catch (err: any) {
      if (err?.code === 'MODULE_NOT_FOUND' && String(err?.message).includes('.prisma/client')) {
        throw new Error(
          '[DB] the generated Prisma client (node_modules/.prisma/client) is missing: npm ci runs with ' +
            'ignore-scripts, so prisma generate never ran. From Blockchain/Dev/services/originate run: ' +
            'cp -R ../../prisma ./prisma && npx prisma generate (KS-1305)',
          { cause: err },
        );
      }
      throw err;
    }
    const { PrismaClient } = require('@prisma/client');
    // Prisma 7 removed the `datasources` constructor option — the connection
    // goes through a driver adapter instead (rust-free client).
    const { PrismaPg } = require('@prisma/adapter-pg');
    prismaClient = new PrismaClient({
      adapter: new PrismaPg({ connectionString: config.databaseUrl }),
      log: config.nodeEnv === 'development'
        ? [{ level: 'error', emit: 'stdout' }, { level: 'warn', emit: 'stdout' }]
        : [{ level: 'error', emit: 'stdout' }],
    });
  }
  return prismaClient;
}

// ---------------------------------------------------------------------------
// KS-458: tenant-GUC Proxy over the real PrismaClient (single-tenant mode)
// ---------------------------------------------------------------------------

/** The raw-SQL entry points that must carry the RLS scope GUC. */
const RAW_SQL_METHODS = new Set(['$queryRaw', '$queryRawUnsafe', '$executeRaw', '$executeRawUnsafe']);

/**
 * KS-458 (fail-closed RLS, migration 039): wrap a real PrismaClient in a JS
 * Proxy so that every `$queryRaw` / `$queryRawUnsafe` / `$executeRaw` /
 * `$executeRawUnsafe` call runs inside ONE interactive transaction together
 * with `set_config(<scope GUC>, ..., is_local=true)` whenever a tenant or
 * platform scope is active (seeded by the tenantGucContext() middleware or by
 * runWithTenantId / runWithPlatformScope). is_local + pgbouncer transaction
 * pooling means the GUC and the statement MUST share a transaction — a bare
 * SET on a pooled connection would leak or vanish.
 *
 * - Tenant scope   → `app.current_tenant_id = <tenantId>` (policy match).
 * - Platform scope → `app.tenant_scope_bypass = 'platform_admin'` (the
 *   deliberate cross-tenant alternative the policy accepts).
 * - No scope       → call through directly (fail-closed: zero tenant rows).
 *
 * The `tx` delegate handed out by $transaction is the REAL transaction
 * client, never this proxy — so the inner call cannot double-wrap. All other
 * properties/methods pass through untouched (bound to the real client so
 * Prisma internals keep their `this`).
 */
function wrapPrismaWithTenantGuc(realPrisma: any): any {
  return new Proxy(realPrisma, {
    get(target, prop, receiver) {
      const value = Reflect.get(target, prop, receiver);
      if (typeof prop === 'string' && RAW_SQL_METHODS.has(prop) && typeof value === 'function') {
        return (...args: any[]) => {
          const tenantId = currentTenantId();
          const platformScope = isPlatformScope();
          // No scope active → straight through (RLS then fails closed).
          if (!tenantId && !platformScope) {
            return value.apply(target, args);
          }
          // One interactive transaction: GUC + statement on one connection.
          return target.$transaction(async (tx: any) => {
            if (platformScope) {
              await tx.$executeRaw`SELECT set_config('app.tenant_scope_bypass', 'platform_admin', true)`;
            } else {
              await tx.$executeRaw`SELECT set_config('app.current_tenant_id', ${tenantId}, true)`;
            }
            return (tx as any)[prop](...args);
          });
        };
      }
      // Pass-through for everything else; bind functions to the real client.
      if (typeof value === 'function') {
        return value.bind(target);
      }
      return value;
    },
  });
}

let prismaGucProxy: any = null;

/** The GUC-aware Prisma client the module `prisma` export delegates to (KS-458). */
function getGucPrisma() {
  if (!prismaGucProxy) {
    prismaGucProxy = wrapPrismaWithTenantGuc(getPrismaClient());
  }
  return prismaGucProxy;
}

// ---------------------------------------------------------------------------
// Exported `prisma` — compatible interface for both modes
// ---------------------------------------------------------------------------

/**
 * The default database client. When multi-tenancy is off, this is a real
 * PrismaClient. When on, it's a pg-pool proxy for the default tenant.
 *
 * For tenant-scoped queries, use `getRequestPrisma(req)` instead.
 */
export const prisma: {
  $queryRaw: (strings: TemplateStringsArray, ...values: any[]) => Promise<any[]>;
  $executeRaw: (strings: TemplateStringsArray, ...values: any[]) => Promise<number>;
  $queryRawUnsafe: (text: string, ...params: any[]) => Promise<any[]>;
  $executeRawUnsafe: (text: string, ...params: any[]) => Promise<number>;
  $disconnect: () => Promise<void>;
} = {
  // KS-458: the single-tenant path goes through the GUC Proxy (getGucPrisma)
  // so a scoped request's raw SQL carries the RLS tenant/platform GUC; the
  // multi-tenant defaultProxy is GUC-aware via queryWithTenantGuc.
  $queryRaw: async (strings: TemplateStringsArray, ...values: any[]) => {
    if (MULTI_TENANCY && defaultProxy) {
      return defaultProxy.$queryRaw(strings, ...values);
    }
    return getGucPrisma().$queryRaw(strings, ...values);
  },
  $executeRaw: async (strings: TemplateStringsArray, ...values: any[]) => {
    if (MULTI_TENANCY && defaultProxy) {
      return defaultProxy.$executeRaw(strings, ...values);
    }
    return getGucPrisma().$executeRaw(strings, ...values);
  },
  $queryRawUnsafe: async (text: string, ...params: any[]) => {
    if (MULTI_TENANCY && defaultProxy) {
      return defaultProxy.$queryRawUnsafe(text, ...params);
    }
    return getGucPrisma().$queryRawUnsafe(text, ...params);
  },
  $executeRawUnsafe: async (text: string, ...params: any[]) => {
    if (MULTI_TENANCY && defaultProxy) {
      return defaultProxy.$executeRawUnsafe(text, ...params);
    }
    return getGucPrisma().$executeRawUnsafe(text, ...params);
  },
  $disconnect: async () => {
    if (prismaClient) {
      await prismaClient.$disconnect();
    }
    if (tenantManager) {
      await tenantManager.shutdown();
    }
  },
};

/**
 * Force the TenantPoolManager to reload configs from the platform DB.
 * Call after creating a new tenant so it's immediately available.
 */
export async function refreshTenantConfigs(): Promise<void> {
  if (tenantManager) {
    await tenantManager.refreshConfigs();
  }
}

/**
 * Get a Prisma-compatible client scoped to the current request's tenant.
 * Falls back to the default client if no tenant context is available.
 */
export function getRequestPrisma(req: { tenantPool?: any }): typeof prisma {
  if (!MULTI_TENANCY || !req.tenantPool) {
    return prisma;
  }
  return createPoolProxy(req.tenantPool) as typeof prisma;
}

// ---------------------------------------------------------------------------
// Tenant-scoped transaction (KS-108) — required for rights_holders RLS
// ---------------------------------------------------------------------------

/** Prisma-compatible client handed to a `withTenant` callback. */
export type TenantTx = {
  $queryRaw: (strings: TemplateStringsArray, ...values: any[]) => Promise<any[]>;
  $executeRaw: (strings: TemplateStringsArray, ...values: any[]) => Promise<number>;
  $queryRawUnsafe: (text: string, ...params: any[]) => Promise<any[]>;
  $executeRawUnsafe: (text: string, ...params: any[]) => Promise<number>;
};

/**
 * Run `fn` inside a single DB transaction with the Postgres session GUC
 * `app.tenant_id` set to `tenantId` (transaction-scoped via
 * `set_config(..., is_local=true)`). This is the mechanism the `rights_holders`
 * RLS policy keys off (KS-108): the GUC and the queries MUST share one
 * connection + one transaction, which a bare `pool.query()` can't guarantee
 * under pgbouncer transaction pooling.
 *
 * The callback receives a Prisma-compatible client bound to that transaction —
 * use it (not the module `prisma`) for every query that must be tenant-scoped.
 *
 * `tenantId` MUST be a trusted value (derived from the verified JWT /
 * X-Tenant-Override), never raw client input. It is sent as a bind parameter,
 * so it is not an injection vector, but an attacker-chosen value would scope to
 * the wrong tenant.
 */
export async function withTenant<T>(
  tenantId: string,
  fn: (tx: TenantTx) => Promise<T>,
): Promise<T> {
  if (MULTI_TENANCY && tenantManager) {
    // pg Pool path (dev/demo): check out one connection for the whole txn.
    const client = await tenantManager.getDefaultPool().connect();
    try {
      await client.query('BEGIN');
      await client.query("SELECT set_config('app.tenant_id', $1, true)", [tenantId]);
      // KS-458: ALSO set app.current_tenant_id in the SAME transaction so
      // statements in this callback that touch the fail-closed flip tables
      // (documents, users, audit_logs, …) are scoped too. app.tenant_id stays
      // — it serves the separate rights_holders policy (KS-108).
      await client.query("SELECT set_config('app.current_tenant_id', $1, true)", [tenantId]);
      const result = await fn(createPoolProxy(client) as TenantTx);
      await client.query('COMMIT');
      return result;
    } catch (err) {
      try { await client.query('ROLLBACK'); } catch { /* connection may be broken */ }
      throw err;
    } finally {
      client.release();
    }
  }
  // Single-tenant fallback (local default): Prisma interactive transaction.
  // The tx client is itself Prisma-compatible, so `fn` works unchanged.
  return getPrismaClient().$transaction(async (tx: any): Promise<T> => {
    await tx.$executeRawUnsafe("SELECT set_config('app.tenant_id', $1, true)", tenantId);
    // KS-458: same-transaction scope for the fail-closed flip tables — see
    // the pool branch above. app.tenant_id stays for rights_holders (KS-108).
    await tx.$executeRawUnsafe("SELECT set_config('app.current_tenant_id', $1, true)", tenantId);
    return fn(tx as TenantTx);
  });
}

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

/**
 * Initialize the database layer. Call once at service startup.
 */
export async function initDb(): Promise<void> {
  if (MULTI_TENANCY) {
    const platformUrl = process.env.PLATFORM_DATABASE_URL;
    if (!platformUrl) {
      console.warn('[DB] MULTI_TENANCY_ENABLED=true but PLATFORM_DATABASE_URL not set — falling back to single-tenant mode');
      return;
    }

    tenantManager = new TenantPoolManager({
      platformDatabaseUrl: platformUrl,
      defaultDatabaseUrl: config.databaseUrl,
    });
    await tenantManager.init();

    defaultProxy = createPoolProxy(tenantManager.getDefaultPool());
    console.log('[DB] Multi-tenancy enabled — using TenantPoolManager');
  } else {
    // Verify Prisma connection
    try {
      await getPrismaClient().$queryRaw`SELECT 1`;
      console.log('[DB] Prisma connection verified (single-tenant mode)');
    } catch (err: any) {
      console.error('[DB] Prisma connection failed:', err.message);
    }
  }
}

/**
 * Graceful shutdown.
 */
export async function disconnectDb(): Promise<void> {
  await prisma.$disconnect();
  console.log('[DB] Database connections closed');
}
