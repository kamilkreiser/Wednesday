/**
 * =============================================================================
 * CREDENTIAL REPOSITORY
 * =============================================================================
 * Dual-write storage for Verifiable Credentials.
 * Persists to PostgreSQL when available, with an in-memory Map as fallback.
 *
 * Uses a dedicated `vc_credentials_store` table to avoid foreign-key issues
 * with the `verifiable_credentials` table whose `issuer_did` column references
 * `did_documents`.
 *
 * The table is owned by the migration path — `migrations/001_initial-schema.sql`
 * and `docker/init/03-service-tables.sql`. KS-1281 (#1231) removed the runtime
 * `CREATE TABLE`: `ensureTable()` below performs an existence check and issues
 * no DDL, because the runtime role has no CREATE on schema `public`.
 * =============================================================================
 */

import { SecuuraCredential } from '@secuura/shared/vc';
import { query, isDbAvailable } from '../db';
import { logger } from '../utils/logger';

// ---------------------------------------------------------------------------
// In-memory fallback
// ---------------------------------------------------------------------------
const memoryStore = new Map<string, SecuuraCredential>();

// ---------------------------------------------------------------------------
// Table existence check (KS-1281: no runtime DDL; migration 001 owns the table)
// ---------------------------------------------------------------------------
let tableEnsured = false;

async function ensureTable(): Promise<void> {
  if (tableEnsured) return;
  try {
    // KS-1281: migration 001 owns vc_credentials_store and the runtime role has no CREATE on schema public,
    // so this is an existence check only - no DDL at runtime.
    await query('SELECT 1 FROM vc_credentials_store LIMIT 0');
    tableEnsured = true;
  } catch (err: any) {
    logger.warn('Could not ensure vc_credentials_store table', { error: err?.message });
  }
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Store a credential (dual-write: memory + DB).
 */
export async function store(credential: SecuuraCredential): Promise<void> {
  memoryStore.set(credential.id, credential);

  if (!isDbAvailable()) {
    // KS-1295: this return used to be SILENT. The caller is told the credential was
    // stored, nothing reaches PostgreSQL, and on restart the credential is simply
    // gone — with no line to grep, no counter and no artefact, so the event cannot
    // be investigated after the fact. #1231 made the sibling table-absent path loud;
    // this matches it. The id is named because it is the only handle that ties this
    // line to the credential a later 404 or failed revoke will be asking about.
    logger.warn('Credential stored in memory only — the database is unavailable', {
      credentialId: credential.id,
      reason: 'isDbAvailable() returned false',
    });
    return;
  }

  try {
    await ensureTable();
    await query(
      `INSERT INTO vc_credentials_store (id, credential)
       VALUES ($1, $2)
       ON CONFLICT (id) DO UPDATE SET credential = EXCLUDED.credential`,
      [credential.id, JSON.stringify(credential)],
    );
  } catch (err: any) {
    logger.warn('DB write failed for credential — kept in memory', {
      credentialId: credential.id,
      error: err?.message,
    });
  }
}

/**
 * Retrieve a credential by its EXACT id only (KS-1121; the KS-1020 / #966 rule): a fragment resolves
 * nothing. The LIKE fallback and the includes() scan are deleted.
 */
export async function getById(id: string): Promise<SecuuraCredential | undefined> {
  // Try DB first
  if (isDbAvailable()) {
    try {
      await ensureTable();
      // Exact match
      const result = await query<{ credential: SecuuraCredential }>(
        'SELECT credential FROM vc_credentials_store WHERE id = $1',
        [id],
      );
      if (result.rows.length > 0) return result.rows[0].credential;
    } catch (err: any) {
      logger.warn('DB read failed — falling back to memory', { error: err?.message });
    }
  }

  // Fall back to memory
  const exact = memoryStore.get(id);
  if (exact) return exact;
  return undefined;
}

/**
 * Find a credential whose `credentialSubject.documentHash` matches.
 */
export async function getByHash(hash: string): Promise<SecuuraCredential | undefined> {
  if (isDbAvailable()) {
    try {
      await ensureTable();
      const result = await query<{ credential: SecuuraCredential }>(
        `SELECT credential FROM vc_credentials_store
         WHERE credential->'credentialSubject'->>'documentHash' = $1
         LIMIT 1`,
        [hash],
      );
      if (result.rows.length > 0) return result.rows[0].credential;
    } catch (err: any) {
      logger.warn('DB hash lookup failed — falling back to memory', { error: err?.message });
    }
  }

  for (const value of memoryStore.values()) {
    if (value.credentialSubject.documentHash === hash) return value;
  }
  return undefined;
}

/**
 * List credentials with optional filters and pagination.
 */
export async function list(options?: {
  issuer?: string;
  documentType?: string;
  limit?: number;
  offset?: number;
}): Promise<{ credentials: SecuuraCredential[]; total: number }> {
  const limit = options?.limit ?? 100;
  const offset = options?.offset ?? 0;

  if (isDbAvailable()) {
    try {
      await ensureTable();

      const conditions: string[] = [];
      const params: unknown[] = [];
      let idx = 1;

      if (options?.issuer) {
        conditions.push(`credential->'issuer'->>'id' = $${idx++}`);
        params.push(options.issuer);
      }
      if (options?.documentType) {
        conditions.push(`credential->'type' @> $${idx++}::jsonb`);
        params.push(JSON.stringify([options.documentType]));
      }

      const where = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

      const countResult = await query<{ count: string }>(
        `SELECT COUNT(*) AS count FROM vc_credentials_store ${where}`,
        params,
      );
      const total = parseInt(countResult.rows[0].count, 10);

      params.push(limit);
      params.push(offset);
      const dataResult = await query<{ credential: SecuuraCredential }>(
        `SELECT credential FROM vc_credentials_store ${where}
         ORDER BY created_at DESC LIMIT $${idx++} OFFSET $${idx++}`,
        params,
      );

      return {
        credentials: dataResult.rows.map((r) => r.credential),
        total,
      };
    } catch (err: any) {
      logger.warn('DB list failed — falling back to memory', { error: err?.message });
    }
  }

  // Memory fallback
  let credentials = Array.from(memoryStore.values());

  if (options?.issuer) {
    credentials = credentials.filter((c) => {
      const issuerId = typeof c.issuer === 'string' ? c.issuer : c.issuer.id;
      return issuerId === options.issuer;
    });
  }
  if (options?.documentType) {
    credentials = credentials.filter((c) => c.type.includes(options.documentType as string));
  }

  const total = credentials.length;
  const paged = credentials.slice(offset, offset + limit);
  return { credentials: paged, total };
}

/**
 * Load all credentials from DB into the in-memory store on startup.
 */
export async function loadFromDb(): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    await ensureTable();
    const result = await query<{ id: string; credential: SecuuraCredential }>(
      'SELECT id, credential FROM vc_credentials_store ORDER BY created_at DESC',
    );
    for (const row of result.rows) {
      memoryStore.set(row.id, row.credential);
    }
    logger.info('credentialRepo loaded credentials from DB', { count: result.rows.length });
  } catch (err) {
    logger.warn('credentialRepo.loadFromDb failed — starting with empty store', {
      error: err instanceof Error ? err.message : String(err),
    });
  }
}

/**
 * Revoke a credential by updating its status.
 */
export async function revoke(
  id: string,
  reason?: string,
): Promise<SecuuraCredential | undefined> {
  const credential = await getById(id);
  if (!credential) return undefined;

  const revokedCredential = {
    ...credential,
    credentialStatus: {
      ...credential.credentialStatus,
      revoked: true,
      revokedAt: new Date().toISOString(),
      revocationReason: reason,
    },
  } as SecuuraCredential;

  // Update memory
  memoryStore.set(credential.id, revokedCredential);

  // Update DB
  if (isDbAvailable()) {
    try {
      await ensureTable();
      await query(
        `UPDATE vc_credentials_store SET credential = $1 WHERE id = $2`,
        [JSON.stringify(revokedCredential), credential.id],
      );
    } catch (err: any) {
      logger.warn('DB revoke update failed — kept in memory', { error: err?.message });
    }
  }

  return revokedCredential;
}
