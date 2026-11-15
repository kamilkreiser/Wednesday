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

import type { Request } from 'express';
import { SecuuraCredential } from '@secuura/shared/vc';
import { query, isDbAvailable } from '../db';
import { logger } from '../utils/logger';
import { RecordOwner, OWNERLESS, ownerFromRow, ownerOf, ownerlessCredentialReadable, mayReadCredential } from '../ownership';

// ---------------------------------------------------------------------------
// In-memory fallback
// ---------------------------------------------------------------------------
const memoryStore = new Map<string, SecuuraCredential>();
// KS-1116: the creating principal of every credential in memoryStore, so the
// GET /:id bound still holds when getRecordById() falls back to memory — and,
// since KS-1683, the list and by-hash bounds (listReadable, getReadableByHash).
const memoryOwners = new Map<string, RecordOwner>();

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
    let reason: string | undefined;
    try {
      reason = err?.message;
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('Could not ensure vc_credentials_store table', { error: reason });
  }
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Store a credential (dual-write: memory + DB).
 *
 * KS-1116: `owner` is the authenticated principal creating it (the route passes
 * `ownerOf(req)`). Omitted, the row is stored OWNERLESS — which the GET /:id
 * bound refuses, so a caller that forgets it fails closed, never open.
 */
export async function store(credential: SecuuraCredential, owner: RecordOwner = OWNERLESS): Promise<void> {
  memoryStore.set(credential.id, credential);
  // ON CONFLICT below never rewrites the owner columns, so neither does memory.
  if (!memoryOwners.has(credential.id)) memoryOwners.set(credential.id, owner);

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
      `INSERT INTO vc_credentials_store (id, credential, created_by_user_id, created_by_tenant_id)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (id) DO UPDATE SET credential = EXCLUDED.credential`,
      [credential.id, JSON.stringify(credential), owner.userId, owner.tenantId],
    );
  } catch (err: any) {
    logger.warn('DB write failed for credential — kept in memory', {
      credentialId: credential.id,
      error: err?.message,
    });
  }
}

/**
 * KS-1958: the credential store could not be read, so this process will not answer for the credential.
 *
 * Its message is FIXED. The verifier writes `Failed to check credential status: ${error}` into the result the
 * verify routes return, so the database's own error text must never ride on this error, and a hostile thrown
 * value (a revoked Proxy, an Error whose message getter throws) must not be what the verifier stringifies.
 */
export class CredentialStoreReadError extends Error {
  constructor() {
    super('the credential store could not be read');
    this.name = 'CredentialStoreReadError';
  }
}

/**
 * KS-1959: a revoke's database UPDATE did not take effect (it threw, or it matched no row), so the revoke is refused.
 *
 * Its message is FIXED, for the same reason as CredentialStoreReadError: the thrown value is read guarded and only
 * logged, never carried. The revoke route answers it with a 503 and its own fixed public text.
 */
export class CredentialStoreWriteError extends Error {
  constructor() {
    super('the credential store could not be updated');
    this.name = 'CredentialStoreWriteError';
  }
}

export interface GetByIdOptions {
  /**
   * KS-1958: when the database is available and the read THROWS, reject with CredentialStoreReadError instead of
   * answering from memory. Set by the verify path's revocation lookup (services/revocationResolvers.ts) only.
   * memoryStore is filled from the database once, at boot (loadFromDb), and never refreshed: a credential another
   * writer revoked in the database (a second replica, out-of-band SQL) is still unrevoked here, so answering from
   * memory on a failed read verified a revoked credential as valid (gate 152, G152-F1, scenario B).
   * Unchanged with or without it: no database in the process (memory is the only store), and a HEALTHY read that
   * returns no row (a row the database does not hold cannot have been revoked there; no path deletes one).
   */
  failClosedOnReadError?: boolean;
}

/**
 * Retrieve a credential by its EXACT id only (KS-1121; the KS-1020 / #966 rule): a fragment resolves
 * nothing. The LIKE fallback and the includes() scan are deleted.
 * KS-1958: `options.failClosedOnReadError` (see GetByIdOptions); revoke() and every other caller omit it.
 */
export async function getById(id: string, options: GetByIdOptions = {}): Promise<SecuuraCredential | undefined> {
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
      let reason: string | null | undefined;
      try {
        const m = err?.message;
        reason = m === undefined || m === null ? m : String(m);
      } catch {
        reason = 'unreadable thrown value';
      }
      if (options.failClosedOnReadError) {
        // KS-1958: fail closed. A fresh error with a fixed message, never the thrown value.
        logger.warn('DB read failed — not answering from memory (verify path, KS-1958)', { error: reason });
        throw new CredentialStoreReadError();
      }
      logger.warn('DB read failed — falling back to memory', { error: reason });
    }
  }

  // Fall back to memory
  const exact = memoryStore.get(id);
  if (exact) return exact;
  return undefined;
}

/**
 * KS-1116: the same EXACT lookup as getById, returning the row's creating
 * principal with it, from whichever path found the row. Used by
 * GET /api/credentials/:id, which decides on the record (ownership.ts).
 *
 * getById above is deliberately left as it was: the public verify path's
 * revocation lookup (services/revocationResolvers.ts) calls it with no
 * principal, by contract, and must not be bound.
 */
export interface CredentialRecord {
  credential: SecuuraCredential;
  owner: RecordOwner;
}

export async function getRecordById(id: string): Promise<CredentialRecord | undefined> {
  if (isDbAvailable()) {
    try {
      await ensureTable();
      const result = await query<{
        credential: SecuuraCredential;
        created_by_user_id: string | null;
        created_by_tenant_id: string | null;
      }>(
        'SELECT credential, created_by_user_id, created_by_tenant_id FROM vc_credentials_store WHERE id = $1',
        [id],
      );
      if (result.rows.length > 0) {
        const row = result.rows[0];
        return { credential: row.credential, owner: ownerFromRow(row) };
      }
    } catch (err: any) {
      let reason: string | null | undefined;
      try {
        const m = err?.message;
        reason = m === undefined || m === null ? m : String(m);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('DB read failed — falling back to memory', { error: reason });
    }
  }

  const exact = memoryStore.get(id);
  if (exact) return { credential: exact, owner: memoryOwners.get(id) ?? OWNERLESS };
  return undefined;
}

/**
 * Find a credential whose `credentialSubject.documentHash` matches.
 *
 * UNBOUND: it returns the first match, whoever created it. No route serves it —
 * GET /api/credentials/by-hash/:hash calls getReadableByHash (KS-1683). It is kept
 * because the repository's own cells (credentialRepo.test.ts) exercise it.
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
      let reason: string | null | undefined;
      try {
        const m = err?.message;
        reason = m === undefined || m === null ? m : String(m);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('DB hash lookup failed — falling back to memory', { error: reason });
    }
  }

  for (const value of memoryStore.values()) {
    if (value.credentialSubject.documentHash === hash) return value;
  }
  return undefined;
}

export interface ListOptions {
  issuer?: string;
  documentType?: string;
  limit?: number;
  offset?: number;
}

/**
 * List credentials with optional filters and pagination.
 *
 * UNBOUND: it lists every caller's credentials. No route serves it —
 * GET /api/credentials calls listReadable (KS-1683). It is kept because the
 * repository's own cells (credentialRepo.test.ts) exercise it.
 */
export async function list(options?: ListOptions): Promise<{ credentials: SecuuraCredential[]; total: number }> {
  return selectList(options, null);
}

// ---------------------------------------------------------------------------
// KS-1683: the list and by-hash reads, bound by the KS-1116 rule (owner-less rows: KS-1906)
// ---------------------------------------------------------------------------

/**
 * The credential rule (ownership.ts `mayReadCredential`) as a SQL condition on the owner
 * columns, for the two reads that return MANY rows or pick ONE of several. There,
 * deciding on each record afterwards cannot keep `total`, the page boundaries or
 * "the first match" right, so the database has to apply the rule too.
 *
 * Always parameters $1-$3, in this order:
 *   $1  the caller's userId — never null: a caller without one may read nothing,
 *       and no query is run for it (readerParams)
 *   $2  the caller's tenantId, or null when the token carries none
 *   $3  may the caller read an OWNER-LESS row of its own tenant (KS-1906)
 *
 * Row for row it is mayReadCredential:
 *   - `NULLIF(col, '')` is claim(): '' reads as absent, as ownerFromRow reads it.
 *   - An owned row: the same userId and the same tenant. IS NOT DISTINCT FROM, so
 *     a tenant-less caller matches a tenant-less row — mayRead's
 *     `owner.tenantId === claim(user?.tenantId)` with null === null.
 *   - An owner-less row: KS-1906 can only ever admit a row whose tenant IS the
 *     caller's tenant, so ownerlessCredentialReadable(req, <the caller's tenant>) decides
 *     this branch for every row it could admit, and `= $2` refuses the rest.
 *
 * mayReadCredential still runs on every row this returns, on both paths — a fail-closed
 * backstop. If the SQL and the rule ever disagreed, the row is dropped and never
 * served; `total`, counted by the SQL, would then over-claim. It never under-protects.
 */
const READABLE_BY_CALLER =
  `((NULLIF(created_by_user_id, '') = $1::text` +
  ` AND NULLIF(created_by_tenant_id, '') IS NOT DISTINCT FROM $2::text)` +
  ` OR ($3::boolean AND NULLIF(created_by_user_id, '') IS NULL` +
  ` AND NULLIF(created_by_tenant_id, '') = $2::text))`;

/** READABLE_BY_CALLER's $1-$3 for this caller, or null when it may read nothing at all. */
function readerParams(reader: Request): [string, string | null, boolean] | null {
  // ownerOf reads the caller's claims exactly as mayReadCredential does (claim()).
  const { userId, tenantId } = ownerOf(reader);
  if (userId === null) return null;
  return [userId, tenantId, tenantId !== null && ownerlessCredentialReadable(reader, tenantId)];
}

/**
 * GET /api/credentials: the credentials the caller may read (ownership.ts
 * `mayReadCredential`), filtered and paginated AFTER the owner bound — so `total` and the
 * page are the caller's own, on the DB path and on the in-memory fallback alike.
 */
export async function listReadable(
  reader: Request,
  options?: ListOptions,
): Promise<{ credentials: SecuuraCredential[]; total: number }> {
  return selectList(options, reader);
}

/**
 * GET /api/credentials/by-hash/:hash: the newest credential with this document
 * hash that the caller may read — not the first match. Several callers can hold
 * credentials over the same document, and an unbound `LIMIT 1` would let any of
 * theirs stand in for (or hide) the caller's own.
 */
export async function getReadableByHash(reader: Request, hash: string): Promise<SecuuraCredential | undefined> {
  const params = readerParams(reader);
  if (params === null) return undefined;

  if (isDbAvailable()) {
    try {
      await ensureTable();
      const result = await query<{
        credential: SecuuraCredential;
        created_by_user_id: string | null;
        created_by_tenant_id: string | null;
      }>(
        `SELECT credential, created_by_user_id, created_by_tenant_id FROM vc_credentials_store
         WHERE ${READABLE_BY_CALLER}
           AND credential->'credentialSubject'->>'documentHash' = $4
         ORDER BY created_at DESC, id DESC
         LIMIT 1`,
        [...params, hash],
      );
      if (result.rows.length > 0) {
        const row = result.rows[0];
        if (mayReadCredential(reader, ownerFromRow(row))) return row.credential;
        logger.warn('KS-1683: the by-hash owner filter returned a row mayReadCredential refuses — not served');
        return undefined;
      }
    } catch (err: any) {
      logger.warn('DB hash lookup failed — falling back to memory', { error: err?.message });
    }
  }

  for (const [id, value] of memoryStore.entries()) {
    if (value.credentialSubject.documentHash === hash && mayReadCredential(reader, memoryOwners.get(id) ?? OWNERLESS)) {
      return value;
    }
  }
  return undefined;
}

/** The list, bound by `reader` when one is given (listReadable) and unbound when null (list). */
async function selectList(
  options: ListOptions | undefined,
  reader: Request | null,
): Promise<{ credentials: SecuuraCredential[]; total: number }> {
  const limit = options?.limit ?? 100;
  const offset = options?.offset ?? 0;

  let ownerParams: [string, string | null, boolean] | null = null;
  if (reader) {
    ownerParams = readerParams(reader);
    if (ownerParams === null) return { credentials: [], total: 0 };
  }

  if (isDbAvailable()) {
    try {
      await ensureTable();

      const conditions: string[] = [];
      const params: unknown[] = [];
      let idx = 1;

      // KS-1683: the owner bound is a WHERE condition, so the COUNT below and the
      // page share it — `total` and `hasMore` are counted after the filter.
      if (ownerParams) {
        conditions.push(READABLE_BY_CALLER);
        params.push(...ownerParams);
        idx = 4;
      }

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
      const columns = reader ? 'credential, created_by_user_id, created_by_tenant_id' : 'credential';
      const dataResult = await query<{
        credential: SecuuraCredential;
        created_by_user_id?: string | null;
        created_by_tenant_id?: string | null;
      }>(
        `SELECT ${columns} FROM vc_credentials_store ${where}
         ORDER BY created_at DESC, id DESC LIMIT $${idx++} OFFSET $${idx++}`,
        params,
      );

      let rows = dataResult.rows;
      if (reader) {
        // The fail-closed backstop (see READABLE_BY_CALLER).
        const readable = rows.filter((r) => mayReadCredential(reader, ownerFromRow(r)));
        if (readable.length !== rows.length) {
          logger.warn('KS-1683: the list owner filter returned rows mayReadCredential refuses — not served', {
            dropped: rows.length - readable.length,
          });
        }
        rows = readable;
      }

      return {
        credentials: rows.map((r) => r.credential),
        total,
      };
    } catch (err: any) {
      logger.warn('DB list failed — falling back to memory', { error: err?.message });
    }
  }

  // Memory fallback — bound by the same rule, on the record (KS-1683)
  let credentials = Array.from(memoryStore.entries())
    .filter(([id]) => !reader || mayReadCredential(reader, memoryOwners.get(id) ?? OWNERLESS))
    .map(([, credential]) => credential);

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
    const result = await query<{
      id: string;
      credential: SecuuraCredential;
      created_by_user_id: string | null;
      created_by_tenant_id: string | null;
    }>(
      'SELECT id, credential, created_by_user_id, created_by_tenant_id FROM vc_credentials_store ORDER BY created_at DESC',
    );
    for (const row of result.rows) {
      memoryStore.set(row.id, row.credential);
      memoryOwners.set(row.id, ownerFromRow(row));
    }
    logger.info('credentialRepo loaded credentials from DB', { count: result.rows.length });
  } catch (err) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('credentialRepo.loadFromDb failed — starting with empty store', {
      error: reason,
    });
  }
}

/**
 * Revoke a credential by updating its status.
 *
 * KS-1959: when the database is available, a revoke counts only if its UPDATE takes effect. An UPDATE that throws
 * (whatever it throws) or that matches no row rejects with CredentialStoreWriteError, which the route answers with a
 * 503. Before, the catch only logged ("kept in memory") and the route answered 200 while the row stayed unrevoked, so
 * the next healthy read, and loadFromDb after a restart, verified the credential as valid. A success answer now means
 * the database row is revoked.
 *
 * Memory is still written first, unchanged (Wednesday's ruling (a) on KS-1959): where the database holds an
 * unrevoked row, the healthy read wins (KS-1958) and the credential verifies as it really is; where memory is the
 * credential's only record (no row, e.g. its INSERT failed at issuance), the revoked copy keeps it failing verify
 * in this process, as before. Writing memory only after the database would make that zero-row case verify valid.
 * No database in this process (memory is the only store): unchanged.
 *
 * `rowCount`: pg sets it from the CommandComplete tag ("UPDATE n") for every UPDATE, so a real result always
 * carries a number. A non-number is read as success, not as zero (existing test fakes answer `{ rows: [] }`).
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
    let rowCount: unknown;
    try {
      await ensureTable();
      const result = await query(
        `UPDATE vc_credentials_store SET credential = $1 WHERE id = $2`,
        [JSON.stringify(revokedCredential), credential.id],
      );
      rowCount = result?.rowCount;
    } catch (err: any) {
      let error: string | null | undefined;
      try {
        const m = err?.message;
        error = m === undefined || m === null ? m : String(m);
      } catch {
        error = 'unreadable thrown value';
      }
      // KS-1959: fail closed. A fresh error with a fixed message, never the thrown value.
      logger.warn('DB revoke update failed — the revoke is refused (KS-1959)', { credentialId: credential.id, error });
      throw new CredentialStoreWriteError();
    }
    if (typeof rowCount === 'number' && rowCount < 1) {
      logger.warn('DB revoke update matched no row — the revoke is refused (KS-1959)', { credentialId: credential.id });
      throw new CredentialStoreWriteError();
    }
  }

  return revokedCredential;
}
