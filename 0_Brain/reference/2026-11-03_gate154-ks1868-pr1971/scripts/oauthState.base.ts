/**
 * KS-1677 — the Microsoft 365 sign-in's OAuth `state`, bound to one browser, one user, one organisation and
 * one connection, and usable once.
 *
 * Before this, `state` was the connection's own id, and the callback looked the connection up by it alone. So
 * anyone holding a connection id could finish its sign-in with a code from their own Microsoft account, pending
 * or already connected (RFC 6749 §10.12; measured by gate AS1 on #1633).
 *
 * Now each sign-in started at `POST /api/connections/init` gets three random values:
 *   - the `state` sent to Microsoft (only its SHA-256 is kept);
 *   - a browser-binding value, set as an HttpOnly cookie scoped to the callback path (only its SHA-256 is kept);
 *   - a PKCE code verifier, sent to Microsoft as an S256 challenge and stored encrypted.
 *
 * The callback consumes the record with the state AND the binding as the key, in one statement. A caller
 * without the cookie therefore cannot burn a real user's state: the KS-819 lesson, where a state consumed
 * before the request was validated let anyone spend it.
 *
 * Storage follows the connections' own pattern: an in-memory map, plus the `svc_m365_oauth_states` table
 * when the database is up. When it is up, the table is the ONLY authority for a consume. A record that
 * reached only memory during an outage is then refused, not completed. That is fail-closed, and it keeps
 * two processes from each completing the same state.
 */
import crypto from 'crypto';
import { query, isDbAvailable } from './db';
import { encryptToken, decryptToken } from './security/tokenCrypto';
import { logger } from './utils/logger';

export interface PendingOAuthState {
  connectionId: string;
  organizationId: string;
  /** The user id from the token that called init. */
  initiatedBy: string;
  /** SHA-256 hex of the browser-binding cookie's value. */
  bindingHash: string;
  codeVerifier: string;
  expiresAt: Date;
}

export const OAUTH_STATE_TTL_MS = 10 * 60 * 1000;

/** The path the BROWSER sees. The gateway rewrites `/api/m365` to `/api` before m365, but the cookie is the browser's. */
export const OAUTH_BINDING_COOKIE_PATH = '/api/m365/callback';

/** Exported so the real-engine cells run exactly these statements. */
export const OAUTH_STATE_SQL = {
  purgeExpired: 'DELETE FROM svc_m365_oauth_states WHERE expires_at < NOW()',
  insert: `INSERT INTO svc_m365_oauth_states
       (state_hash, binding_hash, connection_id, organization_id, initiated_by, code_verifier, expires_at)
     VALUES ($1, $2, $3, $4, $5, $6, $7)`,
  consume: `DELETE FROM svc_m365_oauth_states
     WHERE state_hash = $1 AND binding_hash = $2
     RETURNING connection_id, organization_id, initiated_by, binding_hash, code_verifier, expires_at`,
} as const;

export const sha256Hex = (value: string): string => crypto.createHash('sha256').update(value, 'utf8').digest('hex');

/** 32 random bytes, base64url: an unguessable value that is also a valid PKCE verifier (43 characters). */
export const randomUrlToken = (): string => crypto.randomBytes(32).toString('base64url');

/** RFC 7636 S256: BASE64URL(SHA256(ASCII(code_verifier))). */
export const pkceChallenge = (verifier: string): string =>
  crypto.createHash('sha256').update(verifier, 'ascii').digest('base64url');

/** One cookie per sign-in, so two sign-ins started in one browser do not overwrite each other's binding. */
export const oauthBindingCookieName = (stateHash: string): string => `m365_oauth_binding_${stateHash.slice(0, 16)}`;

/** Read one cookie from the raw header. There is no cookie parser in this service. */
export function readCookie(header: unknown, name: string): string | undefined {
  if (typeof header !== 'string') return undefined;
  for (const part of header.split(';')) {
    const eq = part.indexOf('=');
    if (eq > 0 && part.slice(0, eq).trim() === name) return part.slice(eq + 1).trim();
  }
  return undefined;
}

export const hashesEqual = (a: string, b: string): boolean =>
  a.length === b.length && crypto.timingSafeEqual(Buffer.from(a, 'utf8'), Buffer.from(b, 'utf8'));

const memOAuthStates = new Map<string, PendingOAuthState>();

export async function saveOAuthState(stateHash: string, rec: PendingOAuthState): Promise<void> {
  const now = Date.now();
  for (const [key, value] of memOAuthStates) {
    if (value.expiresAt.getTime() < now) memOAuthStates.delete(key);
  }
  memOAuthStates.set(stateHash, rec);
  if (!isDbAvailable()) return;
  try {
    await query(OAUTH_STATE_SQL.purgeExpired);
    await query(OAUTH_STATE_SQL.insert, [
      stateHash, rec.bindingHash, rec.connectionId, rec.organizationId, rec.initiatedBy,
      encryptToken(rec.codeVerifier, 'code_verifier', rec.connectionId), rec.expiresAt,
    ]);
  } catch (err: any) {
    logger.warn('DB save OAuth state failed', { error: err?.message });
  }
}

/**
 * Take the record for this state if, and only if, the presented binding matches. A miss leaves the record
 * where it is. Expiry, the connection's status and its organisation are checked by the caller, after this.
 */
export async function consumeOAuthState(stateHash: string, bindingHash: string): Promise<PendingOAuthState | null> {
  if (!isDbAvailable()) {
    const mem = memOAuthStates.get(stateHash);
    if (!mem || !hashesEqual(mem.bindingHash, bindingHash)) return null;
    memOAuthStates.delete(stateHash);
    return mem;
  }
  try {
    const r = await query<{
      connection_id: string; organization_id: string; initiated_by: string;
      binding_hash: string; code_verifier: string | null; expires_at: Date | string;
    }>(OAUTH_STATE_SQL.consume, [stateHash, bindingHash]);
    const row = r.rows[0];
    if (!row) return null;
    memOAuthStates.delete(stateHash);
    const codeVerifier = decryptToken(row.code_verifier, 'code_verifier', row.connection_id);
    if (!codeVerifier) return null;
    return {
      connectionId: row.connection_id,
      organizationId: row.organization_id,
      initiatedBy: row.initiated_by,
      bindingHash: row.binding_hash,
      codeVerifier,
      expiresAt: new Date(row.expires_at),
    };
  } catch (err: any) {
    logger.warn('DB consume OAuth state failed', { error: err?.message });
    return null;
  }
}
