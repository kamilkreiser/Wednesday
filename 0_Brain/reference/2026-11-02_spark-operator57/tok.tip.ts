import express from 'express';
import helmet from 'helmet';
import { z } from 'zod';
import { initDb } from './db.js';
import { tokenise, detokenise, rotateKey } from './vault.js';
import { generateKey, hashKey, encrypt, decrypt } from './crypto.js';
import { query } from './db.js';
import { authenticate as jwtAuthenticate, requireRole, enforceProductionConfig, errorHandler, tenantGucContext, runWithTenantId, rejectNulBytes } from '@secuura/shared';
import { resolveTenantScope } from './tenant-scope.js';

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('tokenisation', {
  requiredEnvVars: ['DATABASE_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

const app = express();
app.use(helmet());
app.use(express.json({ limit: '2mb' }));
app.use(rejectNulBytes()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)

const PORT = parseInt(process.env.PORT || '4021', 10);

const PII_FIELDS = new Set(
  (process.env.PII_FIELDS || 'email,firstName,lastName,displayName,name,phone,phoneNumber,mobile,address,street,city,postcode,zipCode,dateOfBirth,dob,ssn,nationalId').split(','),
);

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'tokenisation', version: '1.0.0' });
});

// KS-458: seed the fail-closed RLS tenant context from x-tenant-id for the
// whole request. This carries the CALLER's tenant only — handlers where
// resolveTenantScope (or a platform-admin body param) yields a different
// EFFECTIVE tenant re-wrap their DB work with runWithTenantId below.
app.use('/api', tenantGucContext());

// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
app.use('/api', jwtAuthenticate());

// -------------------------------------------------------------------------
// POST /api/tokenise
// -------------------------------------------------------------------------

const tokeniseSchema = z.object({
  // KS-166: tenantId is an optional ASSERTION — authority comes from the JWT.
  tenantId: z.string().min(1).optional(),
  key: z.string().min(1),
  fields: z.array(z.object({
    name: z.string(),
    value: z.string(),
  })).min(1).max(500),
});

app.post('/api/tokenise', async (req, res) => {
  try {
    const body = tokeniseSchema.parse(req.body);
    const scope = resolveTenantScope((req as any).user?.tenantId, body.tenantId);
    if (!scope.ok) {
      if (scope.code === 'TENANT_SCOPE_MISMATCH') {
        console.warn('[tokenisation] TENANT_SCOPE_MISMATCH on /api/tokenise', { authTenant: (req as any).user?.tenantId, bodyTenant: body.tenantId });
      }
      res.status(scope.status).json({ success: false, error: { code: scope.code, message: scope.message } });
      return;
    }
    // KS-458: scope the vault writes to the RESOLVED tenant so the RLS GUC
    // matches the rows being written, not whatever x-tenant-id seeded.
    const results = await runWithTenantId(scope.tenantId, () => tokenise(scope.tenantId, body.fields, body.key));
    res.json({ success: true, fields: results });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: message } });
  }
});

// -------------------------------------------------------------------------
// POST /api/detokenise
// -------------------------------------------------------------------------

const detokeniseSchema = z.object({
  // KS-166: tenantId is an optional ASSERTION — authority comes from the JWT.
  tenantId: z.string().min(1).optional(),
  key: z.string().min(1),
  tokens: z.array(z.string()).min(1).max(500),
});

app.post('/api/detokenise', async (req, res) => {
  try {
    const body = detokeniseSchema.parse(req.body);
    const scope = resolveTenantScope((req as any).user?.tenantId, body.tenantId);
    if (!scope.ok) {
      if (scope.code === 'TENANT_SCOPE_MISMATCH') {
        console.warn('[tokenisation] TENANT_SCOPE_MISMATCH on /api/detokenise', { authTenant: (req as any).user?.tenantId, bodyTenant: body.tenantId });
      }
      res.status(scope.status).json({ success: false, error: { code: scope.code, message: scope.message } });
      return;
    }
    // KS-458: scope the vault reads to the RESOLVED tenant so the RLS GUC
    // matches the rows being read, not whatever x-tenant-id seeded.
    const results = await runWithTenantId(scope.tenantId, () => detokenise(scope.tenantId, body.tokens, body.key));
    res.json({ success: true, values: results });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: message } });
  }
});

// -------------------------------------------------------------------------
// POST /api/generate-key
// -------------------------------------------------------------------------
//
// AUDIT B-5: prior implementation returned the plaintext base64 AES-256-GCM
// key in the response body. Any access log, reverse-proxy log, response
// cache, or browser dev-tools history captured it. Fix:
//   1. Persist the key into the server-side `tenant_keys` table (auto-
//      created), wrapped under the platform KEK loaded from
//      TOKENISATION_KEK env (or the existing PII keyring).
//   2. Return only `{ keyId, keyHash }` — never the plaintext.
//   3. Emit an audit_logs entry per generation.
//
// Recovery / cross-machine retrieval: a separate admin-only, audited
// endpoint can return the wrapped envelope for emergency export.

async function ensureTenantKeysTable(): Promise<void> {
  // KS-110: tenant_keys is now owned by the migration path
  // (migrations/029_tokenisation_tenant_keys.sql). Skip the runtime DDL when the
  // role lacks CREATE on schema public (the least-privilege secuura_app runtime,
  // KS-109) — the attempt would just throw "permission denied" and be swallowed.
  try {
    const probe = await query("SELECT has_schema_privilege(current_user, 'public', 'CREATE') AS ok");
    if (!((probe.rows?.[0] as any)?.ok)) {
      console.log('[tokenisation] skipping runtime tenant_keys DDL — least-privilege role; migration path owns it (KS-110)');
      return;
    }
  } catch {
    // Probe failed — fall through to the original best-effort behaviour.
  }
  await query(`
    CREATE TABLE IF NOT EXISTS tenant_keys (
      id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      tenant_id     UUID NOT NULL,
      tenant_slug   TEXT,
      key_hash      TEXT NOT NULL,
      wrapped_key   BYTEA NOT NULL,
      wrap_iv       TEXT NOT NULL,
      wrap_auth_tag BYTEA NOT NULL,
      version       INT NOT NULL DEFAULT 1,
      status        TEXT NOT NULL DEFAULT 'active',
      created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      rotated_from  UUID,
      UNIQUE (tenant_id, version, status)
        DEFERRABLE INITIALLY DEFERRED
    );
    CREATE INDEX IF NOT EXISTS tenant_keys_tenant_idx ON tenant_keys(tenant_id);
  `);
}

const TOKENISATION_KEK = process.env.TOKENISATION_KEK
  || process.env.PII_ENCRYPTION_KEY
  || '';

if (!TOKENISATION_KEK && (process.env.NODE_ENV === 'production' || process.env.NODE_ENV === 'demo')) {
  console.error('[tokenisation] FATAL: TOKENISATION_KEK (or PII_ENCRYPTION_KEY) required in prod-like envs to wrap tenant keys');
  process.exit(1);
}
// The KEK arrives as a 64-char HEX string (PII_ENCRYPTION_KEY / TOKENISATION_KEK), but the
// crypto.ts encrypt/decrypt helpers decode their key argument as BASE64 (the tenant data-plane
// keys are base64). Re-encode the hex KEK to base64 so its 32 key bytes survive: Buffer.from(
// hex,'hex') = 32 bytes -> .toString('base64') -> crypto.ts base64-decodes back to the same 32
// bytes. Without this, AES-256-GCM got a wrong-length buffer and generate-key/rotate-key 500'd
// with "Invalid key length" (KS-288). originate uses the same key via the shared keyring, which
// already hex-decodes it — hence originate worked and tokenisation didn't.
const KEK_HEX = TOKENISATION_KEK || 'a'.repeat(64); // dev-only fallback — obvious-fake 32-byte hex
const KEK_BYTES = Buffer.from(KEK_HEX, 'hex');
if (KEK_BYTES.length !== 32) {
  // Fail fast (mirrors the unset-KEK guard above): a wrong-length KEK would 500 every key op.
  console.error(
    `[tokenisation] FATAL: KEK must be 32 bytes (64 hex chars); got ${KEK_BYTES.length} bytes after hex-decode`,
  );
  process.exit(1);
}
const EFFECTIVE_KEK = KEK_BYTES.toString('base64');

async function emitAudit(action: string, tenantId: string, details: Record<string, unknown>): Promise<void> {
  try {
    // KS-28: include the writing tenant on every audit row. tenantId is
    // already on the call signature — the previous version put it into
    // organization_id (a misuse; tenant_id and organization_id are
    // different scopes) without setting tenant_id at all, so cross-tenant
    // reads of these rows leaked. Keeping organization_id populated for
    // backward compat with any reader that filters on it.
    await query(
      `INSERT INTO audit_logs (
         id, tenant_id, organization_id, action, resource_type, resource_id,
         details, success, created_at
       ) VALUES (gen_random_uuid(), $1::uuid, $1, $2, 'tenant_key', $1::uuid, $3, true, NOW())`,
      [tenantId, action, JSON.stringify(details)],
    );
  } catch (err: unknown) {
    // Best-effort; audit-log unavailability shouldn't block the operation,
    // but it MUST be logged so we know the audit chain has gaps.
    console.warn('[tokenisation] audit emit failed', { action, tenantId, error: (err as Error).message });
  }
}

// KS-175: generate-key + rotate-key are control-plane key operations that take
// an arbitrary tenantId in the body, so they must NOT be reachable by a
// tenant-scoped user (key substitution / sabotage / DoS). Gate them to
// platform-level roles only — distinct from the KS-166 data-plane tenant-match,
// because these are legitimately cross-tenant (tenant-provisioning generates a
// NEW tenant's key). tenant-provisioning forwards the calling platform-admin's
// bearer token, so the audited actor is the real admin, not a service identity.
const PLATFORM_ADMIN_ROLES = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'super_admin', 'platform_admin'];

app.post('/api/generate-key', requireRole(...PLATFORM_ADMIN_ROLES), async (req, res) => {
  try {
    const { tenantId, tenantSlug } = req.body;
    if (!tenantId) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'tenantId is required' } });
      return;
    }
    await ensureTenantKeysTable();
    const { key, keyHash } = generateKey();
    // Wrap the plaintext key under the KEK before persisting. The DB
    // never sees the raw bytes.
    const { ciphertext: wrappedKey, iv, authTag } = encrypt(key, EFFECTIVE_KEK);

    // KS-458: platform-admin route provisioning ANOTHER tenant's key — the
    // request ALS carries the CALLER's tenant, so re-scope the writes (incl.
    // the audit_logs row) to the TARGET tenant or fail-closed RLS drops them.
    const { keyId, createdAt } = await runWithTenantId(tenantId, async () => {
      const inserted = await query<{ id: string; created_at: string }>(
        `INSERT INTO tenant_keys (
           tenant_id, tenant_slug, key_hash,
           wrapped_key, wrap_iv, wrap_auth_tag, version, status
         ) VALUES ($1, $2, $3, $4, $5, $6, 1, 'active')
         RETURNING id, created_at`,
        [tenantId, tenantSlug || null, keyHash, wrappedKey, iv, authTag],
      );

      await emitAudit('tenant_key.generated', tenantId, {
        keyId: inserted.rows[0]?.id, keyHash, version: 1,
        actor: (req as any).user?.userId ?? (req as any).user?.sub,
        actorRole: (req as any).user?.role,
      });

      return { keyId: inserted.rows[0]?.id, createdAt: inserted.rows[0]?.created_at };
    });

    res.json({
      success: true,
      keyId,
      keyHash,
      tenantId,
      tenantSlug: tenantSlug || '',
      algorithm: 'aes-256-gcm',
      version: 1,
      createdAt,
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : message } });
  }
});

// -------------------------------------------------------------------------
// POST /api/rotate-key
// -------------------------------------------------------------------------
//
// AUDIT B-5: the prior implementation accepted both old + new plaintext
// keys in the request body — same exposure problem as generate-key. The
// new flow performs rotation entirely server-side: the caller passes only
// `{ tenantId }` and the service:
//   1. Reads the wrapped active key from `tenant_keys`.
//   2. Generates a new key, wraps it under the KEK.
//   3. Re-encrypts every `vault_entries` row from old → new key inside a
//      transaction.
//   4. Marks the old key row `rotated`, inserts the new row as `active`.
//   5. Emits an audit_logs entry.
const rotateSchema = z.object({
  tenantId: z.string().min(1),
});

app.post('/api/rotate-key', requireRole(...PLATFORM_ADMIN_ROLES), async (req, res) => {
  try {
    const body = rotateSchema.parse(req.body);
    await ensureTenantKeysTable();

    // KS-458: PLATFORM_ADMIN route rotating ANOTHER tenant's key — the request
    // ALS carries the admin's own tenant, so the whole flow (tenant_keys swap,
    // the vault_entries re-encrypt sweep in rotateKey, the audit row) re-scopes
    // to the target tenant or fail-closed RLS returns/updates zero rows.
    await runWithTenantId(body.tenantId, async () => {
      // Look up the current active key
      const active = await query<{
        id: string; version: number;
        wrapped_key: Buffer; wrap_iv: string; wrap_auth_tag: Buffer;
      }>(
        `SELECT id, version, wrapped_key, wrap_iv, wrap_auth_tag
           FROM tenant_keys WHERE tenant_id = $1 AND status = 'active'
           LIMIT 1`,
        [body.tenantId],
      );
      if (active.rows.length === 0) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'No active key for tenant — call /api/generate-key first.' } });
        return;
      }
      const oldRow = active.rows[0];
      const oldKey = decrypt(oldRow.wrapped_key, oldRow.wrap_iv, oldRow.wrap_auth_tag, EFFECTIVE_KEK);

      // Mint the new key + wrap it
      const { key: newKey, keyHash: newHash } = generateKey();
      const wrappedNew = encrypt(newKey, EFFECTIVE_KEK);

      // Re-encrypt every row in vault_entries from old → new
      const result = await rotateKey(body.tenantId, oldKey, newKey);

      // Atomically: insert new active row + mark old as rotated.
      // (Two statements — DB-level atomicity via a transaction would be the
      // next step; for now the UNIQUE index on (tenant_id, version, status) is
      // DEFERRABLE so the swap doesn't immediately collide.)
      await query(`UPDATE tenant_keys SET status = 'rotated' WHERE id = $1`, [oldRow.id]);
      const inserted = await query<{ id: string; created_at: string }>(
        `INSERT INTO tenant_keys (
           tenant_id, tenant_slug, key_hash,
           wrapped_key, wrap_iv, wrap_auth_tag, version, status, rotated_from
         ) VALUES ($1, NULL, $2, $3, $4, $5, $6, 'active', $7)
         RETURNING id, created_at`,
        [body.tenantId, newHash, wrappedNew.ciphertext, wrappedNew.iv, wrappedNew.authTag, oldRow.version + 1, oldRow.id],
      );

      await emitAudit('tenant_key.rotated', body.tenantId, {
        oldKeyId: oldRow.id,
        newKeyId: inserted.rows[0]?.id,
        newVersion: oldRow.version + 1,
        vaultRowsRotated: result.rotated,
        vaultRowsFailed: result.failed,
        actor: (req as any).user?.userId ?? (req as any).user?.sub,
        actorRole: (req as any).user?.role,
      });

      res.json({
        success: true,
        newKeyId: inserted.rows[0]?.id,
        newKeyHash: newHash,
        newVersion: oldRow.version + 1,
        vaultRowsRotated: result.rotated,
        vaultRowsFailed: result.failed,
      });
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : message } });
  }
});

// -------------------------------------------------------------------------
// POST /api/detect-pii
// -------------------------------------------------------------------------

app.post('/api/detect-pii', async (req, res) => {
  try {
    const { fields } = req.body as { fields: Record<string, unknown> };
    if (!fields || typeof fields !== 'object') {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'fields object is required' } });
      return;
    }
    const piiFields: string[] = [];
    for (const key of Object.keys(fields)) {
      if (PII_FIELDS.has(key)) {
        piiFields.push(key);
      }
    }
    res.json({ success: true, piiFields, totalFields: Object.keys(fields).length });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: message } });
  }
});

// -------------------------------------------------------------------------
// POST /api/hash-key  (validate a key by returning its hash)
// -------------------------------------------------------------------------

app.post('/api/hash-key', async (req, res) => {
  try {
    const { key } = req.body;
    if (!key) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'key is required' } }); return; }
    res.json({ success: true, keyHash: hashKey(key) });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: message } });
  }
});

// -------------------------------------------------------------------------
// START
// -------------------------------------------------------------------------

await initDb();

// KS-111: final AppError-aware handler — thrown AppErrors (and unknowns) get the
// canonical {success,error} JSON + correct status instead of Express's HTML 500.
app.use(errorHandler);

const server = app.listen(PORT, () => {

  console.log(`[tokenisation] Listening on port ${PORT}`);
});
// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;
