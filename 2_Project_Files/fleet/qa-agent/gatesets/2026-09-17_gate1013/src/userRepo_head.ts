/**
 * =============================================================================
 * USER REPOSITORY — Auth Service
 * =============================================================================
 * Persists users to PostgreSQL. All public methods are async.
 *
 * Database table: `users` (created by docker/init/01-schema.sql)
 * =============================================================================
 */

import { User, UserRole, VerificationLevel, DB_STATUS_TO_DOMAIN } from '../types';
import { query } from '../db';
import { logger } from '../utils/logger';
import {
  encryptField,
  decryptField,
  lookupHash,
  encryptFieldWithDek,
  decryptFieldWithDek,
  isSubjectDekCiphertext,
  isEncryptedPii,
  currentTenantId,
  runWithPlatformScope,
} from '@secuura/shared';
import { subjectDeks } from '../services/subjectDeks';
import { isInfrastructureDbError } from './dbErrors';
import { ServiceUnavailableError } from '../middleware/errorHandler';

// KS-458: the canonical platform default tenant (KS-192) — fail-closed RLS
// forbids NULL tenant_id rows (invisible to every tenant), so user creation
// falls back to this instead of NULL, matching tenant-context.ts.
const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';

// =============================================================================
// ROW MAPPING
// =============================================================================

/**
 * AUDIT B-10: legacy-plaintext acceptance has a HARD CUTOFF.
 *
 * Until 2026-06-01 the platform tolerates plaintext PII rows for the
 * migration tail (returned as-is + warned + encrypted on the next write).
 * After that date, observing a plaintext row in any production-like env
 * fails the read loudly so the operations team is forced to complete
 * the migration. Local-dev and tests stay tolerant indefinitely.
 *
 * To extend the deadline, edit `PII_PLAINTEXT_CUTOFF` in env or this
 * constant — but the right move is to finish the migration, not move
 * the goalposts.
 */
const PII_PLAINTEXT_CUTOFF = process.env.PII_PLAINTEXT_CUTOFF
  ? new Date(process.env.PII_PLAINTEXT_CUTOFF)
  : new Date('2026-06-01T00:00:00Z');

function plaintextStillAcceptable(): boolean {
  const env = process.env.NODE_ENV || 'development';
  const isProdLike = env === 'production' || env === 'staging' || env === 'demo';
  if (!isProdLike) return true;
  return Date.now() < PII_PLAINTEXT_CUTOFF.getTime();
}

/**
 * Decrypt phone_number from its at-rest ciphertext. The AAD is bound to
 * `users.phone_number.<userId>` so a ciphertext copied from another user's
 * row fails verification rather than silently decrypting to the wrong value.
 *
 * For a brief migration window plaintext rows may exist (legacy + freshly
 * inserted before encryption was enforced). They start with anything other
 * than `v<digit>:` so we treat them as plaintext and let them pass through.
 * The next write encrypts them.
 */
/**
 * Generic PII column read with backward-compat for the migration tail.
 * Plaintext rows (anything not matching `v<digit>:`) are returned as-is and
 * a warning is logged so we can track the migration; they're encrypted on
 * the next update to the row.
 */
function decryptPiiCol(
  stored: string | null | undefined,
  column: string,
  userId: string,
  dek: Buffer | null,
): string | undefined {
  if (stored == null || stored === '') return undefined;
  if (!isEncryptedPii(stored)) {
    if (!plaintextStillAcceptable()) {
      // AUDIT B-10: cutoff reached — plaintext PII in a production-like env
      // is now a HARD failure. Operations must complete the encryption
      // backfill. The fail-loud behaviour catches "nobody monitored the
      // warning logs" silently leaving plaintext PII in the DB.
      throw new Error(`[piiCrypto] plaintext ${column} present after PII_PLAINTEXT_CUTOFF (${PII_PLAINTEXT_CUTOFF.toISOString()}) — encryption migration incomplete`);
    }
    logger.warn(`[piiCrypto] plaintext ${column} observed (will encrypt on next update)`, { userId });
    return stored;
  }
  try {
    // KS-291: subject-DEK (`d1:`) rows decrypt under the user's own key; a
    // missing/destroyed DEK means the value is unrecoverable (crypto-shred),
    // which degrades exactly like a failed decrypt. Legacy `v<N>:` rows use
    // the master keyring until the backfill re-wraps them.
    if (isSubjectDekCiphertext(stored)) {
      if (!dek) {
        logger.warn(`[piiCrypto] ${column} is subject-DEK ciphertext but no DEK is available (destroyed or missing)`, { userId });
        return undefined;
      }
      return decryptFieldWithDek(stored, `users.${column}.${userId}`, dek) ?? undefined;
    }
    return decryptField(stored, `users.${column}.${userId}`) ?? undefined;
  } catch (err: any) {
    logger.error(`[piiCrypto] ${column} decrypt failed`, { userId, error: err?.message });
    return undefined;
  }
}

/**
 * Encrypt a PII column value for write under the user's subject DEK (KS-291).
 * Returns null for null/empty so absent values store as NULL. Caller must
 * guard for non-empty strings. Throws SubjectKeyDestroyedError for erased
 * subjects — new PII must never be written for a crypto-shredded user.
 */
async function encryptPiiCol(value: string, column: string, userId: string): Promise<string> {
  const dek = await subjectDeks.getOrCreateDek(userId);
  return encryptFieldWithDek(value, `users.${column}.${userId}`, dek) as string;
}

/**
 * Email is dual-stored: encrypted blob in `email`, HMAC-SHA256 of the
 * lowercased value in `email_lookup_hash`. We decrypt the blob for return
 * to the caller; lookups go via the hash column. Plaintext-tail handling
 * matches the other PII columns.
 */
function decryptEmail(stored: string | null | undefined, userId: string, dek: Buffer | null): string {
  if (stored == null || stored === '') return '';
  if (!isEncryptedPii(stored)) {
    // KS-291: erased users carry a SYNTHETIC plaintext email written by the
    // erasure flow ('deleted_<id>@...' from originate step 10, then
    // 'erased_<id>@...' from the auth cascade). It contains no PII and must
    // pass through — without this guard the B-10 plaintext cutoff below would
    // make every erased row unreadable and 500 admin user listings.
    if (/^(erased|deleted)_.*@anonymized\.local$/.test(stored)) return stored;
    if (!plaintextStillAcceptable()) {
      // AUDIT B-10: see decryptPiiCol above.
      throw new Error(`[piiCrypto] plaintext email present after PII_PLAINTEXT_CUTOFF (${PII_PLAINTEXT_CUTOFF.toISOString()}) — encryption migration incomplete`);
    }
    // Legacy plaintext — return as-is. Migration path: any UPDATE rewrites.
    return stored;
  }
  try {
    // KS-291: dual-format read — see decryptPiiCol.
    if (isSubjectDekCiphertext(stored)) {
      if (!dek) {
        logger.warn('[piiCrypto] email is subject-DEK ciphertext but no DEK is available (destroyed or missing)', { userId });
        return '';
      }
      return decryptFieldWithDek(stored, `users.email.${userId}`, dek) ?? '';
    }
    return decryptField(stored, `users.email.${userId}`) ?? '';
  } catch (err: any) {
    logger.error('[piiCrypto] email decrypt failed', { userId, error: err?.message });
    return '';
  }
}

/**
 * KS-158: decrypt the at-rest MFA TOTP secret (`users.mfa_secret`).
 *
 * Deliberately tolerant of legacy plaintext with NO hard cutoff — unlike the
 * PII columns. A plaintext MFA secret must keep working and lazily re-encrypt
 * on the next write; failing the read (as decryptPiiCol does after the PII
 * cutoff) would lock the user out of MFA entirely. The seed is still sensitive
 * (a stolen row mints valid 6-digit codes), so it IS encrypted on every write.
 */
function decryptMfaSecret(stored: string | null | undefined, userId: string, dek: Buffer | null): string | undefined {
  if (stored == null || stored === '') return undefined;
  if (!isEncryptedPii(stored)) return stored; // legacy plaintext — re-encrypted on next write
  try {
    // KS-291: dual-format read — see decryptPiiCol.
    if (isSubjectDekCiphertext(stored)) {
      if (!dek) {
        logger.warn('[piiCrypto] mfa_secret is subject-DEK ciphertext but no DEK is available (destroyed or missing)', { userId });
        return undefined;
      }
      return decryptFieldWithDek(stored, `users.mfa_secret.${userId}`, dek) ?? undefined;
    }
    return decryptField(stored, `users.mfa_secret.${userId}`) ?? undefined;
  } catch (err: any) {
    logger.error('[piiCrypto] mfa_secret decrypt failed', { userId, error: err?.message });
    return undefined;
  }
}

/**
 * KS-171: decrypt the at-rest platform-admin MFA TOTP secret
 * (`platform_admins.mfa_secret`, in the PLATFORM database). Mirrors
 * decryptMfaSecret for the regular-user table — deliberately tolerant of legacy
 * plaintext with NO hard cutoff, since a failed read would lock a platform admin
 * out of MFA entirely. Plaintext seeds self-heal via
 * reencryptPlatformAdminMfaSecretIfLegacy on the next successful verify. AAD
 * binds the ciphertext to platform_admins.mfa_secret.<id>.
 */
function decryptPlatformAdminMfaSecret(stored: string | null | undefined, adminId: string): string | null {
  if (stored == null || stored === '') return null;
  if (!/^v\d+:/.test(stored)) return stored; // legacy plaintext — re-encrypted on next verify
  try {
    return decryptField(stored, `platform_admins.mfa_secret.${adminId}`) ?? null;
  } catch (err: any) {
    logger.error('[KS-171] platform_admins.mfa_secret decrypt failed', { adminId, error: err?.message });
    return null;
  }
}

/**
 * Map a PostgreSQL row to the User type. Async since KS-291: the row's PII
 * may be `d1:` ciphertext under the user's subject DEK, which is resolved
 * once per row here (cached in-process, so lists cost one key lookup per
 * distinct user per cache-TTL). Rows with no d1: column skip the lookup.
 */
async function fromRow(row: any): Promise<User> {
  const needsDek = [row.email, row.first_name, row.last_name, row.display_name, row.phone_number, row.mfa_secret]
    .some((v) => isSubjectDekCiphertext(v));
  const dek = needsDek ? await subjectDeks.getDek(row.id) : null;
  return {
    id: row.id,
    email: decryptEmail(row.email, row.id, dek),
    emailVerified: row.email_verified ?? false,
    passwordHash: row.password_hash ?? undefined,
    firstName: decryptPiiCol(row.first_name, 'first_name', row.id, dek),
    lastName: decryptPiiCol(row.last_name, 'last_name', row.id, dek),
    displayName: decryptPiiCol(row.display_name, 'display_name', row.id, dek),
    phoneNumber: decryptPiiCol(row.phone_number, 'phone_number', row.id, dek),
    phoneVerified: row.phone_verified ?? false,
    mfaEnabled: row.mfa_enabled ?? false,
    mfaSecret: decryptMfaSecret(row.mfa_secret, row.id, dek),
    mfaBackupCodes: row.mfa_backup_codes ?? undefined,
    entraId: row.external_provider === 'entra' ? row.external_id : undefined,
    auth0Id: row.external_provider === 'auth0' ? row.external_id : undefined,
    googleId: row.google_id ?? undefined,
    linkedinId: row.linkedin_id ?? undefined,
    facebookId: row.facebook_id ?? undefined,
    appleId: row.apple_id ?? undefined,
    githubId: row.github_id ?? undefined,
    microsoftPersonalId: row.microsoft_personal_id ?? undefined,
    role: mapDbRole(row.role),
    verificationLevel: mapDbVerificationLevel(row.verification_level),
    organizationId: row.organization_id ?? undefined,
    tenantId: row.tenant_id ?? undefined,
    tenantSlug: row.tenant_slug ?? undefined,
    status: mapDbStatus(row.status),
    lastLoginAt: row.last_login_at ? new Date(row.last_login_at) : undefined,
    walletAddress: row.wallet_address ?? undefined,
    authMethod: row.auth_method ?? 'email',
    createdAt: new Date(row.created_at),
    updatedAt: new Date(row.updated_at),
  };
}

function mapDbRole(role: string): UserRole {
  const mapping: Record<string, UserRole> = {
    user: 'OWNER',
    owner: 'OWNER',
    OWNER: 'OWNER',
    issuer_admin: 'ISSUER_ADMIN',
    ISSUER_ADMIN: 'ISSUER_ADMIN',
    issuer_approver: 'ISSUER_APPROVER',
    ISSUER_APPROVER: 'ISSUER_APPROVER',
    verifier: 'VERIFIER',
    VERIFIER: 'VERIFIER',
    org_admin: 'ORG_ADMIN',
    ORG_ADMIN: 'ORG_ADMIN',
    system_admin: 'SYSTEM_ADMIN',
    SYSTEM_ADMIN: 'SYSTEM_ADMIN',
    super_admin: 'SYSTEM_ADMIN',
  };
  return mapping[role] || 'OWNER';
}

function mapDbVerificationLevel(level: string): VerificationLevel {
  const mapping: Record<string, VerificationLevel> = {
    none: 'NONE',
    NONE: 'NONE',
    basic: 'BASIC',
    BASIC: 'BASIC',
    social: 'SOCIAL',
    SOCIAL: 'SOCIAL',
    standard: 'STANDARD',
    STANDARD: 'STANDARD',
    enhanced: 'ENHANCED',
    ENHANCED: 'ENHANCED',
    high: 'HIGH',
    HIGH: 'HIGH',
    government: 'GOVERNMENT',
    GOVERNMENT: 'GOVERNMENT',
  };
  return mapping[level] || 'BASIC';
}

/**
 * Exported for KS-796 Q1's test. A test that reimplements this mapping asserts
 * its own copy: reverting the `|| 'ACTIVE'` fallback in the product left that
 * suite fully green, which is how this export came to exist.
 */
export function mapDbStatus(status: string): User['status'] {
  // KS-796 Q1. This used to carry its own copy of the mapping and end
  // `|| 'ACTIVE'`. Two things were wrong with that:
  //
  //   1. The copy did not know `inactive` or `deleted`, which the admin endpoint
  //      can write. Both fell through to the fallback.
  //   2. The fallback was ACTIVE — the MOST privileged value. So a status an
  //      admin set specifically to disable an account was converted into the one
  //      status that mints a credential. Failing open, on the exact field whose
  //      job is to close.
  //
  // Now: one shared vocabulary, and an unrecognised value fails CLOSED to
  // DEACTIVATED, which the credential allow-list refuses.
  // KS-796 F-2 (QA PASS 1 on #819) — LOOK UP OWN PROPERTIES ONLY.
  //
  // `DB_STATUS_TO_DOMAIN` is `Object.freeze({...})` on an object LITERAL, so it
  // inherits `Object.prototype`. `Object.freeze` prevents writes; it does not
  // remove the prototype chain. A bare `map[status]` therefore resolved
  // `constructor`, `toString`, `valueOf`, `hasOwnProperty` and `__proto__` to
  // truthy inherited members, `mapped` was returned, and the warn-and-fail-closed
  // branch was never reached — this function returned a FUNCTION as a
  // `User['status']`, silently. The allow-list doors refused it (a function is
  // not 'ACTIVE') but /api/auth/login's deny-list did not, and it minted.
  //
  // Guarded at the LOOKUP rather than by rebuilding the map with a null
  // prototype: this holds however the map is later constructed, and this is the
  // function whose documented contract is to fail closed.
  const own = (k: string): User['status'] | undefined =>
    Object.prototype.hasOwnProperty.call(DB_STATUS_TO_DOMAIN, k) ? DB_STATUS_TO_DOMAIN[k] : undefined;
  const mapped = own(status) ?? own(String(status).toLowerCase());
  if (mapped) return mapped;
  logger.warn(
    `mapDbStatus: unrecognised users.status ${JSON.stringify(status)} — failing closed to DEACTIVATED. ` +
      `Add it to DB_STATUS_TO_DOMAIN (and the CHECK constraint) if it is legitimate.`,
  );
  return 'DEACTIVATED';
}


// =============================================================================
// COLUMN LISTS
// =============================================================================

/** All user columns EXCEPT password_hash — use for general queries */
const USER_COLS = 'id, email, first_name, last_name, display_name, role, status, email_verified, phone_number, phone_verified, mfa_enabled, mfa_secret, mfa_backup_codes, verification_level, organization_id, tenant_id, tenant_slug, wallet_address, auth_method, external_provider, external_id, google_id, linkedin_id, facebook_id, apple_id, github_id, microsoft_personal_id, metadata, created_at, updated_at, last_login_at';

// =============================================================================
// CRUD OPERATIONS
// =============================================================================

/**
 * Find user by ID.
 *
 * KS-963: a DB failure is NOT "user not found", and this function used to
 * answer `null` for both. That collapse is the defect this closes — a real
 * `query()` error and "no such row" became the same answer to every caller.
 *
 * ⚠ TWO THINGS THIS DOES **NOT** DO, both measured, because the ticket that
 * commissioned it claims otherwise and a future reader will grep this comment
 * rather than the ticket:
 *
 * 1. It did not change the DECRYPT path. `fromRow` is `async` and was returned
 *    WITHOUT `await` from inside the try below, so its rejection was never
 *    caught here — a decrypt failure always propagated, before and after
 *    KS-963. KS-963's "getUserById catches and returns null" was false.
 *    KS-999 (2026-09-17) made it `return await fromRow(...)`, previously kept
 *    out of KS-963 as a behaviour change on the normal production path: a
 *    failure inside `fromRow`, the subject-DEK read included, now reaches the
 *    catch. An infrastructure fault becomes ServiceUnavailable (503) instead of
 *    a raw 500; anything else, a decrypt failure included, is rethrown as-is
 *    and is now logged. The five sibling reads below still return `fromRow`
 *    unawaited: KS-1186.
 *
 * 2. It does not un-silence the platform-admin remediation chain. The throw is
 *    caught two frames up by `seedDemoUsersInner`'s per-account handler, which
 *    logs "Failed to seed demo user" and continues to the next account. On
 *    that path the net effect of this change is OBSERVABILITY ONLY: one
 *    attributed error log where there was none. Whether that handler should
 *    abort the seed on an infrastructure error is a separate decision.
 *
 * The remedy is not a new design. The sibling `getUserByEmail` below already
 * does exactly this, and its comment records why: **KS-253**, after a real
 * incident in which 42 of 266 users were told *"Invalid email or password"*
 * with valid credentials during pool starvation. This function was simply the
 * one that was missed.
 *
 * Kam ruled `rethrow` on 2026-09-08 (card `secuura-ks963-getuserbyid-swallows`).
 *
 * Callers that need "absent or unreadable are the same thing" must now say so
 * explicitly at the call site rather than inheriting it from here.
 */
/**
 * KS-1052 / QA F-1: `tenantId` scopes the read the way `query()`'s third
 * argument scopes a write — an explicit tenant overrides the request ALS
 * context, and the GUC is bundled into the same transaction, which is what
 * fail-closed RLS requires (see `db.ts:60-66`). Callers with a request context
 * omit it and keep reading under their own scope, exactly as before.
 *
 * Without it this SELECT is blind on any pre-auth route: `users` is
 * `relrowsecurity=t relforcerowsecurity=t` with `tenant_isolation` since
 * migration 039, and an unset `app.current_tenant_id` yields ZERO rows for a
 * NOBYPASSRLS runtime role. Measured on a local 039 database as a
 * `LOGIN NOBYPASSRLS` role: no GUC -> 0 rows, tenant GUC set -> 1 row, with the
 * row's existence confirmed on a superuser connection.
 */
export async function getUserById(id: string, tenantId?: string): Promise<User | null> {
  try {
    const result = await query(`SELECT ${USER_COLS} FROM users WHERE id = $1 LIMIT 1`, [id], tenantId);
    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-999: await so the catch classifies infra failures inside fromRow
    return null;
  } catch (err: any) {
    logger.error('DB getUserById failed', { error: err?.message, code: err?.code });
    if (isInfrastructureDbError(err)) {
      throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
    throw err;
  }
}

/**
 * By-id lookup that ALSO carries `password_hash`.
 *
 * KS-732 (#872 review): USER_COLS deliberately omits password_hash, so
 * `getUserById` returns a User whose `passwordHash` is always undefined. Any
 * caller branching on `if (user.passwordHash)` therefore takes the FALSE arm for
 * every account, password accounts included — silently, because the shape is
 * correct and only the value is missing. That is what made the MFA-disable
 * password check dead code while reading as the check that closed the defect.
 *
 * Use this ONLY where the hash is actually verified. It is a separate function
 * rather than a column added to USER_COLS on purpose: USER_COLS feeds every
 * general query in this file, and widening it would put the hash in listings,
 * social lookups and admin reads that have no business holding it.
 *
 * Error behaviour matches getUserById (KS-963): infrastructure failures are
 * rethrown, never flattened into `null` — a caller deciding an auth question
 * must not read "the database is down" as "no such user".
 */
export async function getUserByIdWithPasswordHash(id: string): Promise<User | null> {
  try {
    const result = await query(
      `SELECT ${USER_COLS}, password_hash FROM users WHERE id = $1 LIMIT 1`,
      [id],
    );
    if (result.rows.length > 0) return fromRow(result.rows[0]);
    return null;
  } catch (err: any) {
    logger.error('DB getUserByIdWithPasswordHash failed', { error: err?.message, code: err?.code });
    if (isInfrastructureDbError(err)) {
      throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
    throw err;
  }
}

/**
 * Find user by ID for the pre-auth token flows (refresh / password-reset /
 * email-verification), where the caller holds a proven token but no tenant
 * context exists yet. KS-458: fail-closed RLS makes the plain lookup return
 * nothing pre-auth, so this goes through the SECURITY DEFINER carve-out
 * (migration 039). Post-auth callers should keep using getUserById.
 *
 * KS-963 (widened 2026-09-09): this carried the IDENTICAL swallow `getUserById`
 * was fixed for. The earlier version of this comment said the recommendation to
 * include it had been made and not taken — **it has now been taken.** Kam ruled
 * `include` on 2026-09-09 07:08: *"Widen #907 to getUserByIdPreAuth now — two
 * lines, same pattern, same round."* #907 had already merged, so it landed
 * separately; the decision is his, the vehicle is the only thing that changed.
 *
 * Why it mattered here more than the shared shape suggests — there are FIVE
 * callers. Four read `null` as "no such user", two of those DESTROY a credential
 * on it, and the fifth reads `null` as "no tenant context" instead:
 *
 *   routes/auth.ts:816   password reset  → consumed the reset token, then 404
 *   routes/auth.ts:859   email verify    → consumed the email token, then 404
 *   routes/wallet.ts:193 wallet sign-in  → fell through into `createUser`
 *   routes/auth.ts:686   token refresh   → InvalidCredentialsError (logged out)
 *   userRepo.ts:859      updateUser      → 200 "Password has been reset
 *                                          successfully" over an UPDATE issued
 *                                          with `tenant undefined`; and on the
 *                                          LOGIN success path (auth.ts:587, the
 *                                          unguarded `lastLoginAt` write) a
 *                                          silent miss — now a 503 with NO
 *                                          UPDATE issued. That louder failure is
 *                                          the ruled behaviour (KS-963 r2).
 *
 * The fifth is an INTRA-module call with no `userRepo.` qualifier, so a symbol
 * grep structurally cannot see it — which is why an earlier version of this
 * comment said four. `ks468-authenticate-tenant-guc.test.ts:139` had named five
 * all along; the #913 tier-1 gate found it with a TypeScript LanguageService
 * reference walk. It is written down here because this list is the artefact the
 * next reader greps.
 *
 * Both consumes sit INSIDE the `if (!user)` branch, so a throw never reaches
 * them: a database blip stops burning a single-use token the user cannot get
 * back. Measured at head at the wire, across all five callers: 503 with ZERO
 * writes — wallet issues no INSERT and no challenge DELETE, `updateUser` no
 * UPDATE, and neither single-use token is consumed.
 *
 * ⚠ What the PRE-CHANGE wallet path did to an EXISTING row is NOT established.
 * The gate's harness never executed the INSERT (no `PII_ENCRYPTION_KEY`), so no
 * account of the outcome — the one this comment used to give, or any other —
 * is recorded here. What IS established is that control flow reached
 * `createUser`.
 *
 * That is the same reasoning as the sibling: a DB error is not "no such user".
 */
export async function getUserByIdPreAuth(id: string): Promise<User | null> {
  try {
    const result = await query(`SELECT ${USER_COLS} FROM auth_find_user_by_id($1)`, [id]);
    if (result.rows.length > 0) return fromRow(result.rows[0]);
    return null;
  } catch (err: any) {
    logger.error('DB getUserByIdPreAuth failed', { error: err?.message, code: err?.code });
    if (isInfrastructureDbError(err)) {
      throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
    throw err;
  }
}

/**
 * KS-467: by-id lookup for PLATFORM-admin callers on the user-admin surface.
 * getUserById runs under the request's tenant GUC (fail-closed RLS since
 * KS-458), which confines it to the caller's own tenant — correct for
 * tenant-scoped admins, wrong for a platform admin managing any tenant's
 * users. The route gates on isPlatformAdmin before calling this.
 */
export async function getUserByIdPlatformScope(id: string): Promise<User | null> {
  return runWithPlatformScope(() => getUserById(id));
}

/** KS-467: updateUser for platform-admin callers — see getUserByIdPlatformScope. */
export async function updateUserPlatformScope(id: string, updates: Partial<User>): Promise<User | null> {
  return runWithPlatformScope(() => updateUser(id, updates));
}

/**
 * KS-467: resolve an organization's tenant for the admin-PATCH ownership
 * check. Platform-scoped read on purpose: the value is only compared against
 * the caller's tenant to authorise the assignment, never returned to the
 * client, and the caller must get the SAME rejection whether the org is
 * foreign-tenant or nonexistent (no cross-tenant existence disclosure).
 *
 * Returns `{ tenantId }` when the org exists (tenantId may be null for
 * legacy rows — treated as not-owned by any tenant admin), or null when it
 * doesn't. A malformed (non-UUID) id is reported as "not found" rather than
 * surfacing the Postgres 22P02 cast error as a 500.
 */
export async function getOrganizationTenant(orgId: string): Promise<{ tenantId: string | null } | null> {
  return runWithPlatformScope(async () => {
    try {
      const result = await query<{ tenant_id: string | null }>(
        'SELECT tenant_id FROM organizations WHERE id = $1 LIMIT 1',
        [orgId],
      );
      return result.rows.length > 0 ? { tenantId: result.rows[0].tenant_id } : null;
    } catch (err: any) {
      logger.warn('DB getOrganizationTenant failed — treating as not found', { error: err?.message });
      return null;
    }
  });
}

/**
 * Find user by email. Audit 1.3 phase 4a: now does an HMAC lookup against
 * the email_lookup_hash column rather than LIKE/LOWER on the encrypted
 * blob — the encrypted column is non-deterministic so direct equality
 * doesn't work. During the migration window where some rows still hold
 * plaintext emails (no lookup hash), we fall back to the legacy
 * `LOWER(email) = $1` query.
 */
export async function getUserByEmail(email: string): Promise<User | null> {
  const normalised = email.toLowerCase().trim();
  try {
    const hash = lookupHash(normalised);
    // KS-458: pre-auth lookup (login/registration — no tenant known yet), so
    // it cannot satisfy the fail-closed tenant_isolation policy. Goes through
    // the SECURITY DEFINER carve-out created in migration 039 instead.
    const result = await query(
      'SELECT * FROM auth_find_user_by_email_hash($1)',
      [hash],
    );
    if (result.rows.length > 0) return fromRow(result.rows[0]);

    // Legacy fallback: rows that pre-date the hash column still have
    // plaintext email and no hash. They're identifiable by NOT starting
    // with 'v<digit>:'. The next UPDATE will fill in the hash.
    const legacy = await query(
      'SELECT * FROM auth_find_user_by_email_legacy($1)',
      [normalised],
    );
    if (legacy.rows.length > 0) return fromRow(legacy.rows[0]);
    return null;
  } catch (err: any) {
    // KS-253: a DB failure is NOT "user not found". Swallowing it here made
    // the login route answer 401 "Invalid email or password" to users with
    // valid credentials during pool starvation (42/266 in the KS-217 storm).
    logger.error('DB getUserByEmail failed', { error: err?.message, code: err?.code });
    if (isInfrastructureDbError(err)) {
      throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
    throw err;
  }
}

const SOCIAL_ID_COLUMN_MAP: Record<string, string> = {
  google: 'google_id',
  linkedin: 'linkedin_id',
  facebook: 'facebook_id',
  apple: 'apple_id',
  github: 'github_id',
  microsoft_personal: 'microsoft_personal_id',
};

/** Find user by social provider ID */
export async function getUserBySocialId(provider: string, providerId: string): Promise<User | null> {
  const column = SOCIAL_ID_COLUMN_MAP[provider];
  if (!column) return null;

  try {
    // KS-458: pre-auth lookup (OAuth callback — no tenant known yet) → the
    // SECURITY DEFINER carve-out; the function whitelists the same provider
    // columns as SOCIAL_ID_COLUMN_MAP.
    const result = await query(`SELECT ${USER_COLS} FROM auth_find_user_by_social($1, $2)`, [provider, providerId]);
    if (result.rows.length > 0) return fromRow(result.rows[0]);
    return null;
  } catch (err: any) {
    // KS-253: same contract as getUserByEmail — DB failure is not "not found"
    logger.error('DB getUserBySocialId failed', { error: err?.message, code: err?.code });
    if (isInfrastructureDbError(err)) {
      throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
    throw err;
  }
}

/** Check if email exists. Same dual-path as getUserByEmail. */
export async function emailExists(email: string): Promise<boolean> {
  const normalised = email.toLowerCase().trim();
  try {
    const hash = lookupHash(normalised);
    // KS-458: pre-auth existence check — SECURITY DEFINER carve-out (039).
    const byHash = await query<{ exists: boolean }>(
      'SELECT EXISTS(SELECT 1 FROM auth_find_user_by_email_hash($1)) AS exists',
      [hash],
    );
    if (byHash.rows[0]?.exists) return true;
    // Legacy plaintext fallback
    const legacy = await query<{ exists: boolean }>(
      'SELECT EXISTS(SELECT 1 FROM auth_find_user_by_email_legacy($1)) AS exists',
      [normalised],
    );
    return legacy.rows[0]?.exists ?? false;
  } catch (err: any) {
    // KS-253: returning false on a DB outage told registration the email was
    // free — same masquerade class as the login 401. Fail loud instead.
    logger.error('DB emailExists failed', { error: err?.message, code: err?.code });
    if (isInfrastructureDbError(err)) {
      throw new ServiceUnavailableError('Authentication service temporarily unavailable, please retry');
    }
    throw err;
  }
}

/** Create a new user */
export async function createUser(user: User): Promise<User> {
  // Audit 1.3 phase 4a: email is encrypted at rest, with a separate
  // HMAC column for indexed equality lookups. The encryption is
  // non-deterministic (random IV) so the old UNIQUE(email) constraint
  // wouldn't block duplicates any more — we ON CONFLICT against the
  // hash column, which IS deterministic.
  const normEmail = user.email.toLowerCase().trim();
  const encryptedEmail = await encryptPiiCol(normEmail, 'email', user.id);
  const emailHash = lookupHash(normEmail);

  // KS-458: WITH CHECK requires the GUC to match the inserted tenant_id, and
  // NULL tenant rows are unreachable under fail-closed RLS — default the
  // tenant (covers social/wallet signups that arrive tenant-less) and pass
  // it explicitly so pre-auth creation paths satisfy the policy.
  if (!user.tenantId) user.tenantId = DEFAULT_TENANT_ID;

  await query(
    `INSERT INTO users (
      id, email, email_lookup_hash, password_hash, first_name, last_name, display_name,
      role, status, email_verified, mfa_enabled, mfa_secret, mfa_backup_codes,
      verification_level, wallet_address, auth_method, organization_id,
      tenant_id, tenant_slug,
      metadata, created_at, updated_at
    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22)
    ON CONFLICT (email_lookup_hash) WHERE email_lookup_hash IS NOT NULL DO UPDATE SET
      password_hash = COALESCE(EXCLUDED.password_hash, users.password_hash),
      display_name = COALESCE(EXCLUDED.display_name, users.display_name),
      email_verified = EXCLUDED.email_verified OR users.email_verified,
      tenant_id = COALESCE(EXCLUDED.tenant_id, users.tenant_id),
      tenant_slug = COALESCE(EXCLUDED.tenant_slug, users.tenant_slug),
      updated_at = NOW()`,
    [
      user.id,
      encryptedEmail,
      emailHash,
      user.passwordHash || null,
      // Audit 1.3 phase 3: name columns are encrypted at rest with AAD bound
      // to the user id. Encrypt at INSERT time so a brand-new user is never
      // stored as plaintext, even briefly.
      user.firstName ? await encryptPiiCol(user.firstName, 'first_name', user.id) : null,
      user.lastName ? await encryptPiiCol(user.lastName, 'last_name', user.id) : null,
      user.displayName ? await encryptPiiCol(user.displayName, 'display_name', user.id) : null,
      user.role.toLowerCase(),
      user.status.toLowerCase(),
      user.emailVerified,
      user.mfaEnabled,
      // KS-158: encrypt the TOTP seed at INSERT too (matches the name columns)
      // so a user created with MFA pre-set is never stored plaintext.
      user.mfaSecret ? await encryptPiiCol(user.mfaSecret, 'mfa_secret', user.id) : null,
      user.mfaBackupCodes || null,
      user.verificationLevel.toLowerCase(),
      user.walletAddress || null,
      user.authMethod || 'email',
      user.organizationId || null,
      user.tenantId || null,
      user.tenantSlug || null,
      JSON.stringify({}),
      user.createdAt,
      user.updatedAt,
    ],
    user.tenantId,
  );
  logger.debug('User persisted to DB', { userId: user.id });

  return user;
}

/**
 * KS-74: Create an INVITED stub user for an email that isn't on Platform K yet.
 *
 * Behaviour:
 *   - If a user with this email already exists in the caller's tenant, return
 *     it as-is (idempotent). `alreadyExisted` is true; the caller treats this
 *     as a successful resolve, not a stub creation.
 *   - If a user with this email exists in a DIFFERENT tenant, throw
 *     EMAIL_RESERVED_ELSEWHERE. The global `email` uniqueness constraint
 *     (KS-74 known limitation) means we cannot insert a second row. The
 *     caller surfaces this as a 404 to avoid cross-tenant disclosure (same
 *     privacy stance as `/api/users/lookup`).
 *   - Otherwise, insert a stub row with `status='invited'`, no password
 *     hash, `email_verified=false`, tenant_id pinned to the caller's tenant.
 *
 * The stub is claimed on `POST /api/auth/register` for the same email —
 * see routes/auth.ts.
 */
export async function createInvitedStub(
  email: string,
  callerTenantId: string | undefined,
): Promise<{ user: User; alreadyExisted: boolean }> {
  const existing = await getUserByEmail(email);
  if (existing) {
    if (callerTenantId && existing.tenantId && existing.tenantId !== callerTenantId) {
      const err = new Error(
        `Email ${email} already reserved in a different tenant`,
      ) as Error & { code: string };
      err.code = 'EMAIL_RESERVED_ELSEWHERE';
      throw err;
    }
    return { user: existing, alreadyExisted: true };
  }

  const { v4: uuidv4 } = await import('uuid');
  const stub: User = {
    id: uuidv4(),
    email: email.toLowerCase().trim(),
    emailVerified: false,
    passwordHash: undefined,
    firstName: undefined,
    lastName: undefined,
    displayName: undefined,
    phoneVerified: false,
    mfaEnabled: false,
    role: 'USER' as UserRole,
    verificationLevel: 'BASIC' as VerificationLevel,
    status: 'INVITED',
    tenantId: callerTenantId,
    createdAt: new Date(),
    updatedAt: new Date(),
  };
  await createUser(stub);
  logger.info('KS-74: invited stub created', {
    userId: stub.id,
    tenantId: callerTenantId,
  });
  return { user: stub, alreadyExisted: false };
}

/** Update user fields */
export async function updateUser(id: string, updates: Partial<User>): Promise<User | null> {
  const setClauses: string[] = [];
  const values: unknown[] = [];
  let idx = 1;

  const fieldMap: Record<string, string> = {
    passwordHash: 'password_hash',
    email: 'email',
    firstName: 'first_name',
    lastName: 'last_name',
    displayName: 'display_name',
    emailVerified: 'email_verified',
    // phoneNumber was previously missing here — silently dropped on every
    // update. Restored AND wired through the at-rest encryption helper below.
    phoneNumber: 'phone_number',
    phoneVerified: 'phone_verified',
    mfaEnabled: 'mfa_enabled',
    mfaSecret: 'mfa_secret',
    mfaBackupCodes: 'mfa_backup_codes',
    role: 'role',
    status: 'status',
    verificationLevel: 'verification_level',
    walletAddress: 'wallet_address',
    authMethod: 'auth_method',
    organizationId: 'organization_id',
    tenantId: 'tenant_id',
    tenantSlug: 'tenant_slug',
    lastLoginAt: 'last_login_at',
  };

  for (const [tsField, dbCol] of Object.entries(fieldMap)) {
    if (tsField in updates && updates[tsField as keyof User] !== undefined) {
      let val = updates[tsField as keyof User];
      // Lowercase enum values for DB
      if (['role', 'status', 'verificationLevel', 'authMethod'].includes(tsField) && typeof val === 'string') {
        val = (val as string).toLowerCase();
      }
      // PII at rest (audit 1.3): encrypt name + phone + email columns with
      // AAD bound to the user id so a ciphertext can't be ported between
      // rows.
      const encryptedCols: Record<string, string> = {
        firstName: 'first_name',
        lastName: 'last_name',
        displayName: 'display_name',
        phoneNumber: 'phone_number',
        email: 'email',
        // KS-158: the TOTP seed is encrypted at rest with AAD users.mfa_secret.<id>.
        // Reads go through decryptMfaSecret (tolerant of the legacy-plaintext tail).
        mfaSecret: 'mfa_secret',
      };
      if (encryptedCols[tsField] && typeof val === 'string' && val !== '') {
        // Email also needs the lookup hash updated atomically — handle
        // alongside the encryption write below.
        if (tsField === 'email') {
          const norm = val.toLowerCase().trim();
          const ct = await encryptPiiCol(norm, 'email', id);
          const hash = lookupHash(norm);
          setClauses.push(`email = $${idx}`);
          setClauses.push(`email_lookup_hash = $${idx + 1}`);
          values.push(ct);
          values.push(hash);
          idx += 2;
          continue;
        }
        val = await encryptPiiCol(val, encryptedCols[tsField], id);
      }
      setClauses.push(`${dbCol} = $${idx}`);
      values.push(val);
      idx++;
    }
  }

  // KS-458: pre-auth flows (login rehash, MFA backup consumption, token
  // resets) update the row before any tenant context exists — resolve the
  // row's own tenant via the carve-out lookup so the UPDATE satisfies the
  // fail-closed policy. Post-auth callers keep their request context, and
  // `undefined` means exactly that: read and write under the ambient scope.
  //
  // QA F-1: this is resolved ONCE and used for BOTH the write and the
  // read-back. It used to scope only the write, so on a pre-auth route the
  // UPDATE landed and the trailing SELECT was blind — `updateUser` answered
  // `null` for a change that HAD been applied. Every caller that treats `null`
  // as failure then reported the opposite of what the database did; with
  // `updateUserOrThrow` in front of them that became a 503 after a successful
  // credential write, with the single-use token already burnt.
  const tenantForRls = currentTenantId()
    ? undefined
    : (await getUserByIdPreAuth(id))?.tenantId ?? undefined;

  if (setClauses.length > 0) {
    setClauses.push(`updated_at = NOW()`);
    values.push(id);
    const result = await query(
      `UPDATE users SET ${setClauses.join(', ')} WHERE id = $${idx}`,
      values,
      tenantForRls,
    );

    // KS-943: a 0-row UPDATE is reported as success unless someone looks.
    //
    // The statement was issued and its result DISCARDED, then `getUserById(id)`
    // was returned — so a write that matched nothing came back carrying the
    // row's OLD values, which reads exactly like a successful update. KS-720
    // moved this class from "no statement issued" to "statement issued, effect
    // unverified"; this closes the remainder.
    //
    // 0 rows is not hypothetical here. Under fail-closed RLS
    // (migrations/039_rls_fail_closed.sql) an unresolved tenant GUC produces
    // PRECISELY a 0-row UPDATE — the silent no-op is the case that design
    // deliberately creates.
    //
    // Returns null rather than throwing, deliberately. `updateUser` has 24
    // non-test callers and most discard the return; throwing would convert every
    // silent no-op in the auth service into a 500 at once, which is a much wider
    // change than this defect. `null` is already inside the declared
    // `Promise<User | null>`, so no caller's type contract moves and no new
    // exception path appears — callers that check the return now learn the
    // truth, and callers that ignore it behave exactly as before.
    if (result.rowCount === 0) {
      logger.warn('User UPDATE matched 0 rows — the write did NOT take effect', {
        userId: id,
        columns: setClauses.filter((c) => !c.startsWith('updated_at')).map((c) => c.split(' ')[0]),
        tenantForRls: tenantForRls ?? null,
      });
      return null;
    }
    logger.debug('User updated in DB', { userId: id, rowCount: result.rowCount });
  }

  // Return the updated user from DB, under the SAME scope the UPDATE used.
  return getUserById(id, tenantForRls);
}

/**
 * updateUser, with the return CHECKED instead of discarded.
 *
 * KS-1052: `updateUser` answers `User | null`, and 21 of its 24 non-test
 * callers discard that answer. Four of them then burn a single-use credential
 * or tell the user their password changed. This is the one place that turns a
 * silent no-op into a refusal, so the call sites need one word changed rather
 * than an `if` each — a guard nobody can forget to copy.
 *
 * ⚠ WHAT `null` DOES AND DOES NOT TELL US — do not widen this message.
 * `updateUser` returns null for TWO reasons and the caller cannot tell them
 * apart: the UPDATE matched no row, OR the trailing read-back found nothing.
 *
 * QA F-1 closed the second cause on the path that mattered: `updateUser` now
 * reads back under the SAME tenant scope its UPDATE used, so a pre-auth route
 * no longer answers `null` for a write that landed. It is NOT closed in
 * general — a row whose tenant cannot be resolved at all, or an ambient scope
 * that does not match the row, still reads blind — so the weaker wording
 * stands on purpose.
 *
 * So this says "could not be confirmed" and nothing about whether the change
 * was applied. The earlier message here added "— the change was not applied",
 * which is the stronger cause this very comment forbids; QA reproduced it
 * being false (F-1/F-2) and it is gone. Asserting that cause is also the
 * defect QA raised as F-929-2 against the sibling fix in wallet.ts.
 *
 * 503, not 500, deliberately: the condition is retryable and the caller is
 * being asked to retry. That matters most where the caller still holds an
 * unburnt single-use token — a 500 invites them to give up on a credential
 * that is still valid.
 */
export async function updateUserOrThrow(
  id: string,
  updates: Partial<User>,
  operation: string,
): Promise<User> {
  const updated = await updateUser(id, updates);
  if (!updated) {
    logger.error('User update could not be confirmed — refusing to report success', {
      userId: id,
      operation,
      columns: Object.keys(updates),
    });
    throw new ServiceUnavailableError(
      `${operation} could not be confirmed. Please retry — if you already succeeded, you may not need to.`,
    );
  }
  return updated;
}

/**
 * List users (admin) — supports search, pagination, role filter, and (KS-467)
 * an optional tenant restriction.
 *
 * `tenantId` is the cross-org IDOR guard: the routes pass the caller's own
 * tenant for tenant-scoped admins (ISSUER_ADMIN / ORG_ADMIN) and omit it only
 * for genuine platform admins, so the deliberate platform scope below never
 * hands a tenant admin another tenant's users.
 */
export async function listUsers(
  params: { limit?: number; offset?: number; search?: string; role?: string; tenantId?: string } | number = 100,
  offsetArg = 0,
): Promise<User[]> {
  // KS-458: admin-only caller (role-gated routes) listing across tenants —
  // deliberate platform scope; without it the list silently shrinks to the
  // caller's own tenant under fail-closed RLS. KS-467: tenant-scoped admins
  // are confined by the explicit tenant_id predicate instead.
  return runWithPlatformScope(() => listUsersInner(params, offsetArg));
}

async function listUsersInner(
  params: { limit?: number; offset?: number; search?: string; role?: string; tenantId?: string } | number = 100,
  offsetArg = 0,
): Promise<User[]> {
  const limit = typeof params === 'number' ? params : (params.limit ?? 100);
  const offset = typeof params === 'number' ? offsetArg : (params.offset ?? 0);
  const search = typeof params === 'object' ? (params.search ?? '') : '';
  const role = typeof params === 'object' ? (params.role ?? '') : '';
  const tenantId = typeof params === 'object' ? (params.tenantId ?? '') : '';

  const conditions: string[] = [];
  const values: any[] = [];
  let idx = 1;

  // KS-467: confine tenant-scoped admin callers to their own tenant.
  if (tenantId) {
    conditions.push(`tenant_id = $${idx}`);
    values.push(tenantId);
    idx++;
  }
  if (search) {
    const pattern = `%${search}%`;
    conditions.push(`(email ILIKE $${idx} OR first_name ILIKE $${idx} OR last_name ILIKE $${idx} OR display_name ILIKE $${idx})`);
    values.push(pattern);
    idx++;
  }
  if (role) {
    const roles = role.split(',').map(r => r.trim());
    const placeholders = roles.map((_, i) => `$${idx + i}`).join(', ');
    conditions.push(`role IN (${placeholders})`);
    values.push(...roles);
    idx += roles.length;
  }

  const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';
  values.push(limit, offset);
  const result = await query(
    `SELECT ${USER_COLS} FROM users ${whereClause} ORDER BY created_at DESC LIMIT $${idx} OFFSET $${idx + 1}`,
    values,
  );
  // KS-291: fromRow is async (per-row subject-DEK resolve, cached in-process)
  return Promise.all(result.rows.map((r) => fromRow(r)));
}

/**
 * Count users — supports optional search, role filter, and (KS-467) tenant
 * restriction (same contract as listUsers: set for tenant-scoped admins).
 */
export async function countUsers(search = '', role = '', tenantId = ''): Promise<number> {
  // KS-458: admin-only cross-tenant count — platform scope (see listUsers).
  return runWithPlatformScope(() => countUsersInner(search, role, tenantId));
}

async function countUsersInner(search = '', role = '', tenantId = ''): Promise<number> {
  const conditions: string[] = [];
  const values: any[] = [];
  let idx = 1;

  // KS-467: confine tenant-scoped admin callers to their own tenant.
  if (tenantId) {
    conditions.push(`tenant_id = $${idx}`);
    values.push(tenantId);
    idx++;
  }
  if (search) {
    const pattern = `%${search}%`;
    conditions.push(`(email ILIKE $${idx} OR first_name ILIKE $${idx} OR last_name ILIKE $${idx} OR display_name ILIKE $${idx})`);
    values.push(pattern);
    idx++;
  }
  if (role) {
    const roles = role.split(',').map(r => r.trim());
    const placeholders = roles.map((_, i) => `$${idx + i}`).join(', ');
    conditions.push(`role IN (${placeholders})`);
    values.push(...roles);
  }

  const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';
  const result = await query<{ count: string }>(`SELECT COUNT(*) AS count FROM users ${whereClause}`, values);
  return parseInt(result.rows[0]?.count || '0', 10);
}

/**
 * List distinct organisations derived from user records.
 *
 * KS-467: `tenantId` confines the list to one tenant's organisations — the
 * routes pass the caller's own tenant for tenant-scoped admins and omit it
 * only for platform admins (same contract as listUsers).
 */
export async function listOrganizations(
  tenantId = '',
): Promise<
  Array<{ id: string; name: string; type: string; status: string; userCount: number; documentCount: number; createdAt: string }>
> {
  // KS-458: admin-only cross-tenant org list — platform scope (see listUsers).
  return runWithPlatformScope(() => listOrganizationsInner(tenantId));
}

async function listOrganizationsInner(
  tenantId = '',
): Promise<
  Array<{ id: string; name: string; type: string; status: string; userCount: number; documentCount: number; createdAt: string }>
> {
  // KS-467: optional tenant restriction for tenant-scoped admin callers.
  const whereClause = tenantId ? 'WHERE o.tenant_id = $1' : '';
  const values = tenantId ? [tenantId] : [];
  // Combine organizations from the organizations table with user-derived counts
  const result = await query<{
    id: string;
    name: string;
    type: string;
    status: string;
    user_count: string;
    document_count: string;
    created_at: string;
  }>(
    `SELECT
       o.id,
       o.name,
       COALESCE(o.type, 'Organization') AS type,
       COALESCE(o.status, 'active') AS status,
       COALESCE(uc.user_count, 0)::text AS user_count,
       0::text AS document_count,
       o.created_at::text AS created_at
     FROM organizations o
     LEFT JOIN (
       SELECT organization_id, COUNT(*) AS user_count
       FROM users
       WHERE organization_id IS NOT NULL
       GROUP BY organization_id
     ) uc ON uc.organization_id = o.id
     ${whereClause}
     ORDER BY COALESCE(uc.user_count, 0) DESC, o.created_at DESC`,
    values,
  );

  return result.rows.map((r) => ({
    id: r.id,
    name: r.name || 'Unknown Org',
    type: r.type || 'Organization',
    status: r.status || 'active',
    userCount: parseInt(r.user_count, 10) || 0,
    documentCount: parseInt(r.document_count, 10) || 0,
    createdAt: r.created_at,
  }));
}

// =============================================================================
// TOKEN STORES
// =============================================================================

interface TokenRecord {
  userId: string;
  expiresAt: Date;
}

/** Store a password reset token */
export async function storeResetToken(tokenHash: string, userId: string, expiresAt: Date): Promise<void> {
  await query(
    `INSERT INTO password_reset_tokens (user_id, token_hash, expires_at) VALUES ($1, $2, $3)`,
    [userId, tokenHash, expiresAt],
  );
}

/** Retrieve and validate a reset token */
export async function getResetToken(tokenHash: string): Promise<TokenRecord | null> {
  const result = await query(
    `SELECT user_id, expires_at FROM password_reset_tokens
     WHERE token_hash = $1 AND used_at IS NULL LIMIT 1`,
    [tokenHash],
  );
  if (result.rows.length > 0) {
    return { userId: result.rows[0].user_id, expiresAt: new Date(result.rows[0].expires_at) };
  }
  return null;
}

/** Consume (mark as used) a reset token */
export async function consumeResetToken(tokenHash: string): Promise<void> {
  await query(
    `UPDATE password_reset_tokens SET used_at = NOW() WHERE token_hash = $1`,
    [tokenHash],
  );
}

/** Store an email verification token */
export async function storeEmailToken(tokenHash: string, userId: string, expiresAt: Date): Promise<void> {
  await query(
    `INSERT INTO email_verification_tokens (user_id, token_hash, expires_at) VALUES ($1, $2, $3)`,
    [userId, tokenHash, expiresAt],
  );
}

/** Retrieve and validate an email verification token */
export async function getEmailToken(tokenHash: string): Promise<TokenRecord | null> {
  const result = await query(
    `SELECT user_id, expires_at FROM email_verification_tokens
     WHERE token_hash = $1 AND used_at IS NULL LIMIT 1`,
    [tokenHash],
  );
  if (result.rows.length > 0) {
    return { userId: result.rows[0].user_id, expiresAt: new Date(result.rows[0].expires_at) };
  }
  return null;
}

/** Consume an email verification token */
export async function consumeEmailToken(tokenHash: string): Promise<void> {
  await query(
    `UPDATE email_verification_tokens SET used_at = NOW() WHERE token_hash = $1`,
    [tokenHash],
  );
}

// =============================================================================
// SEED DEMO USERS — loaded on startup if not already in DB
// =============================================================================

export async function seedDemoUsers(hashFn: (pw: string) => Promise<string>): Promise<void> {
  // KS-458: boot-time seeding writes accounts across several demo tenants —
  // a deliberately cross-tenant path, so it runs under the platform scope.
  return runWithPlatformScope(() => seedDemoUsersInner(hashFn));
}

async function seedDemoUsersInner(hashFn: (pw: string) => Promise<string>): Promise<void> {
  // Pen-test F-05 fix: gating the seeder on `NODE_ENV !== production` was
  // unsafe because the demo Azure environment runs as `NODE_ENV=demo` and
  // therefore got the seed (with its `*123` defaults). The new gate is
  // explicit: ALLOW_DEFAULT_SEED_PASSWORDS=true must be set to seed at
  // all, and any non-dev environment additionally needs ENABLE_DEMO_SEED=true.
  const isDevLike = ['development', 'dev', 'test'].includes(process.env.NODE_ENV || '');
  if (process.env.ALLOW_DEFAULT_SEED_PASSWORDS !== 'true') {
    logger.info('Demo user seeding skipped — set ALLOW_DEFAULT_SEED_PASSWORDS=true to enable');
    return;
  }
  if (!isDevLike && process.env.ENABLE_DEMO_SEED !== 'true') {
    logger.info('Demo user seeding skipped in non-dev env (set ENABLE_DEMO_SEED=true alongside ALLOW_DEFAULT_SEED_PASSWORDS=true)');
    return;
  }
  if (!isDevLike) {
    logger.warn('Demo user seeding enabled in non-dev environment via ALLOW_DEFAULT_SEED_PASSWORDS=true + ENABLE_DEMO_SEED=true', {
      nodeEnv: process.env.NODE_ENV,
    });
  }

  // Pen-test F-05 helper — every demo account password resolves from an
  // env var first, with the legacy hardcoded default as a fallback. The
  // hardcoded fallbacks remain only because the seeder itself is now
  // gated on ALLOW_DEFAULT_SEED_PASSWORDS=true (above) — i.e. a deploy
  // that doesn't explicitly opt in never sees these strings.
  // For per-tenant rotation, set DEMO_<TENANT>_PASSWORD env vars in
  // Azure Key Vault and surface them to the auth container.
  const seedPw = (envVar: string, legacyDefault: string): string => {
    return process.env[envVar] || legacyDefault;
  };

  // A password with NO published fallback. `seedPw` above is deliberately
  // permissive — the lint at scripts/check-no-default-passwords.sh even
  // exempts it — because those accounts are ordinary fictional demo personas
  // and the whole seeder is gated on ALLOW_DEFAULT_SEED_PASSWORDS.
  //
  // That gate is configuration, not absence, and it is not enough for the
  // platform SYSTEM_ADMIN: that account carries cross-tenant reach, so a
  // deploy that flips one env var would stand up a known-password account
  // that can read every tenant. KS-949; Kam ruled (2026-09-07) that this
  // identity must not remain reachable by a published default.
  //
  // Returns null when the env var is unset, and the seed loop SKIPS the
  // account rather than inventing a value. Fail-closed: no account is
  // strictly safer than an account whose password is in the repository.
  const requiredSeedPw = (envVar: string): string | null => process.env[envVar] || null;

  // Not a hash of anything. bcrypt and argon2 hashes both begin `$`; this cannot
  // be produced by either, so a verify against it fails rather than matching some
  // unlucky input. Paired with `status = 'suspended'` so the account is refused
  // before any verify runs at all.
  const UNUSABLE_PASSWORD_HASH = '!disabled:no-seed-password-supplied';

  const demoAccounts = [
    {
      id: 'a0000000-0000-4000-8000-000000000010',
      email: process.env.DEMO_USER_EMAIL || 'demo@secuura.io',
      password: seedPw('DEMO_USER_PASSWORD', 'demo123'),
      firstName: 'Demo',
      lastName: 'User',
      // KS-547: was OWNER. /certifications/issue now gates on
      // DOCUMENT_WRITE_ROLES and the public demo flow certifies as this
      // account, so it needs a role inside that list. The seeder updates
      // existing rows on boot, so this re-roles demo@ on next deploy.
      role: 'ISSUER_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      // KS-192: aligned to the canonical DEFAULT_TENANT_ID (a0000…1) used by
      // the seeded documents + the code path (shared/db/tenant-context.ts,
      // api-gateway/middleware/auth.ts, originate). Was 00000…1, which left
      // default-tenant users on a different tenant than their own documents —
      // invisible under fail-closed RLS (KS-174).
      tenantId: 'a0000000-0000-4000-8000-000000000001',
      tenantSlug: 'default',
    },
    {
      id: 'a0000000-0000-4000-8000-000000000020',
      email: process.env.ADMIN_USER_EMAIL || 'admin@secuura.com',
      // KS-964: this used to take a published fallback password. The account is
      // the platform SYSTEM_ADMIN and the comment above already states why that
      // class must not be reachable by a published default — it applied to the
      // …060 identity and equally to this one. Unset env var => not seeded.
      password: requiredSeedPw('ADMIN_USER_PASSWORD'),
      // KS-966 F2: the variable that governs THIS row, so the fail-closed
      // hint below can name it instead of naming another account's.
      passwordVar: 'ADMIN_USER_PASSWORD',
      firstName: 'Admin',
      lastName: 'User',
      role: 'SYSTEM_ADMIN' as UserRole,
      verificationLevel: 'HIGH' as VerificationLevel,
      // KS-192: aligned to the canonical DEFAULT_TENANT_ID (a0000…1) used by
      // the seeded documents + the code path (shared/db/tenant-context.ts,
      // api-gateway/middleware/auth.ts, originate). Was 00000…1, which left
      // default-tenant users on a different tenant than their own documents —
      // invisible under fail-closed RLS (KS-174).
      tenantId: 'a0000000-0000-4000-8000-000000000001',
      tenantSlug: 'default',
    },
    {
      id: 'a0000000-0000-4000-8000-000000000030',
      email: 'issuer@secuura.com',
      password: seedPw("DEMO_ISSUER_PASSWORD", "issuer123"),
      firstName: 'Issuer',
      lastName: 'User',
      role: 'ISSUER_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      // KS-192: aligned to the canonical DEFAULT_TENANT_ID (a0000…1) used by
      // the seeded documents + the code path (shared/db/tenant-context.ts,
      // api-gateway/middleware/auth.ts, originate). Was 00000…1, which left
      // default-tenant users on a different tenant than their own documents —
      // invisible under fail-closed RLS (KS-174).
      tenantId: 'a0000000-0000-4000-8000-000000000001',
      tenantSlug: 'default',
    },
    {
      id: 'a0000000-0000-4000-8000-000000000040',
      email: 'verifier@secuura.com',
      password: seedPw("DEMO_VERIFIER_PASSWORD", "verifier123"),
      firstName: 'Verifier',
      lastName: 'User',
      role: 'VERIFIER' as UserRole,
      verificationLevel: 'STANDARD' as VerificationLevel,
      // KS-192: aligned to the canonical DEFAULT_TENANT_ID (a0000…1) used by
      // the seeded documents + the code path (shared/db/tenant-context.ts,
      // api-gateway/middleware/auth.ts, originate). Was 00000…1, which left
      // default-tenant users on a different tenant than their own documents —
      // invisible under fail-closed RLS (KS-174).
      tenantId: 'a0000000-0000-4000-8000-000000000001',
      tenantSlug: 'default',
    },
    {
      id: 'a0000000-0000-4000-8000-000000000050',
      email: 'holder@secuura.com',
      password: seedPw("DEMO_HOLDER_PASSWORD", "holder123"),
      firstName: 'Rights',
      lastName: 'Holder',
      role: 'OWNER' as UserRole,
      verificationLevel: 'BASIC' as VerificationLevel,
      // KS-192: aligned to the canonical DEFAULT_TENANT_ID (a0000…1) used by
      // the seeded documents + the code path (shared/db/tenant-context.ts,
      // api-gateway/middleware/auth.ts, originate). Was 00000…1, which left
      // default-tenant users on a different tenant than their own documents —
      // invisible under fail-closed RLS (KS-174).
      tenantId: 'a0000000-0000-4000-8000-000000000001',
      tenantSlug: 'default',
    },
    // Secuura Co. platform user
    {
      id: 'a0000000-0000-4000-8000-000000000060',
      // Was a real person's address and name (Kam Kreiser). KS-913 did the
      // same substitution for the ORG_ADMIN row in originate's seed list;
      // this is the remaining live site, plus the api-gateway migration that
      // seeds the matching row in the main DB. `.invalid` rather than
      // `example.com` to match the eleven sibling rows in that migration —
      // both are reserved.
      //
      // KS-949 F1 correction: this used to end "and the two files MUST agree
      // because the seeder and the migration key on the email". Neither keys on
      // email, and one of them never could.
      //
      // This seeder keys on `email_lookup_hash` — the deterministic column, for
      // the reason createUser states: the encryption is non-deterministic, so a
      // UNIQUE on the ciphertext could not block duplicates.
      //
      // The api-gateway migration still says `ON CONFLICT (email)`, which is
      // INVALID on the deployed schema — measured 42P10, because
      // `docker/init/01-schema.sql` declares email TEXT with no unique index. So
      // that statement throws on every boot and has never seeded anything. A fix
      // was written and REVERTED out of this PR (Kam, 2026-09-07 `split`): moving
      // it to the primary key made the statement run, and running it wrote
      // PLAINTEXT into this encrypted column without setting
      // `email_lookup_hash`. The bug was preventing the corruption; fixing it
      // released it. The migration is being repaired in its own round, where the
      // ratified shape is that it stops inserting these rows entirely — this
      // seeder already creates all twelve, correctly.
      //
      // The two files should still agree on the VALUE, so that whichever path
      // writes the row writes the same address. That is a consistency wish, not
      // a mechanism either statement depends on — and stating it as a mechanism
      // is what let the migration keep an email-keyed clause that cannot run.
      email: 'platform.admin@secuura-test.invalid',
      // No published fallback — see requiredSeedPw. Unset env var => this
      // account is not seeded at all.
      password: requiredSeedPw('DEMO_SECUURA_PASSWORD'),
      // KS-966 F2: see ADMIN_USER_PASSWORD above.
      passwordVar: 'DEMO_SECUURA_PASSWORD',
      firstName: 'Platform',
      lastName: 'Admin',
      role: 'SYSTEM_ADMIN' as UserRole,
      verificationLevel: 'HIGH' as VerificationLevel,
      tenantId: 'a0000000-0000-4000-8000-000000000099',
      tenantSlug: 'secuura-co',
    },
    // ==========================================================================
    // PER-CLIENT TENANT USERS
    // ==========================================================================
    // Oxford University
    {
      id: 'c1000000-0000-4000-8000-000000000001',
      email: 'james.wilson@oxford-test.invalid',
      password: seedPw("DEMO_OXFORD_PASSWORD", "oxford123"),
      firstName: 'James',
      lastName: 'Wilson',
      role: 'ORG_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      tenantId: 'b1000000-0000-4000-8000-000000000001',
      tenantSlug: 'oxford-university',
    },
    {
      id: 'c1000000-0000-4000-8000-000000000002',
      email: 'registrar@oxford-test.invalid',
      password: seedPw("DEMO_OXFORD_PASSWORD", "oxford123"),
      firstName: 'Helen',
      lastName: 'Clarke',
      role: 'ISSUER_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      tenantId: 'b1000000-0000-4000-8000-000000000001',
      tenantSlug: 'oxford-university',
    },
    {
      id: 'c1000000-0000-4000-8000-000000000003',
      email: 'alice@student.oxford-test.invalid',
      password: seedPw("DEMO_OXFORD_PASSWORD", "oxford123"),
      firstName: 'Alice',
      lastName: 'Smith',
      role: 'OWNER' as UserRole,
      verificationLevel: 'STANDARD' as VerificationLevel,
      tenantId: 'b1000000-0000-4000-8000-000000000001',
      tenantSlug: 'oxford-university',
    },
    // BUPA Health UK
    {
      id: 'c2000000-0000-4000-8000-000000000001',
      email: 'sarah.mitchell@bupa-test.invalid',
      password: seedPw("DEMO_BUPA_PASSWORD", "bupa123"),
      firstName: 'Sarah',
      lastName: 'Mitchell',
      role: 'ORG_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      tenantId: 'b2000000-0000-4000-8000-000000000001',
      tenantSlug: 'bupa-health-uk',
    },
    {
      id: 'c2000000-0000-4000-8000-000000000002',
      email: 'david.thompson@bupa-test.invalid',
      password: seedPw("DEMO_BUPA_PASSWORD", "bupa123"),
      firstName: 'David',
      lastName: 'Thompson',
      role: 'ISSUER_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      tenantId: 'b2000000-0000-4000-8000-000000000001',
      tenantSlug: 'bupa-health-uk',
    },
    {
      id: 'c2000000-0000-4000-8000-000000000003',
      email: 'emma.wilson@bupa-test.invalid',
      password: seedPw("DEMO_BUPA_PASSWORD", "bupa123"),
      firstName: 'Emma',
      lastName: 'Wilson',
      role: 'VERIFIER' as UserRole,
      verificationLevel: 'STANDARD' as VerificationLevel,
      tenantId: 'b2000000-0000-4000-8000-000000000001',
      tenantSlug: 'bupa-health-uk',
    },
    {
      id: 'c2000000-0000-4000-8000-000000000004',
      email: 'patient.records@bupa-test.invalid',
      password: seedPw("DEMO_BUPA_PASSWORD", "bupa123"),
      firstName: 'Patient',
      lastName: 'Records',
      role: 'OWNER' as UserRole,
      verificationLevel: 'BASIC' as VerificationLevel,
      tenantId: 'b2000000-0000-4000-8000-000000000001',
      tenantSlug: 'bupa-health-uk',
    },
    // Apex Consulting
    {
      id: 'c3000000-0000-4000-8000-000000000001',
      email: 'james@apex-test.invalid',
      password: seedPw("DEMO_APEX_PASSWORD", "apex123"),
      firstName: 'James',
      lastName: 'Wright',
      role: 'ORG_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      tenantId: 'b3000000-0000-4000-8000-000000000001',
      tenantSlug: 'apex-consulting',
    },
    {
      id: 'c3000000-0000-4000-8000-000000000002',
      email: 'sarah@apex-test.invalid',
      password: seedPw("DEMO_APEX_PASSWORD", "apex123"),
      firstName: 'Sarah',
      lastName: 'Palmer',
      role: 'ISSUER_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      tenantId: 'b3000000-0000-4000-8000-000000000001',
      tenantSlug: 'apex-consulting',
    },
    // Greenfield University
    {
      id: 'c4000000-0000-4000-8000-000000000001',
      email: 'issuer.e2e@greenfield-test.invalid',
      password: seedPw("DEMO_GREENFIELD_PASSWORD", "greenfield123"),
      firstName: 'Sarah',
      lastName: 'Chen',
      role: 'ISSUER_ADMIN' as UserRole,
      verificationLevel: 'ENHANCED' as VerificationLevel,
      tenantId: 'b4000000-0000-4000-8000-000000000001',
      tenantSlug: 'greenfield-university',
    },
    // Delta Corp
    {
      id: 'c5000000-0000-4000-8000-000000000001',
      email: 'delta.user@delta-corp-test.invalid',
      password: seedPw("DEMO_DELTA_PASSWORD", "delta123"),
      firstName: 'Delta',
      lastName: 'User',
      role: 'OWNER' as UserRole,
      verificationLevel: 'STANDARD' as VerificationLevel,
      tenantId: 'b5000000-0000-4000-8000-000000000001',
      tenantSlug: 'delta-corp',
    },
  ];

  for (const account of demoAccounts) {
    try {
      // requiredSeedPw returned null: the account has no published default and
      // no env var was supplied. Do NOT create it — but an environment that was
      // seeded BEFORE this change already carries the old row, and skipping
      // outright leaves it exactly as it was.
      //
      // THE FIRST VERSION OF THIS SKIP WAS A BUG, and the shape is worth naming.
      // It sat ABOVE the H5 id-collision branch below — the one block that
      // rewrites a stale row's email in place. So on an already-seeded database
      // the real identity was never touched and its old password hash stayed
      // live, while a FRESH environment looked perfectly clean. The safe-looking
      // default was the only configuration that preserved the thing the change
      // exists to remove: a fail-closed guard placed above a remediation does not
      // fail closed on the problem, it fails closed OVER it.
      //
      // So: remediate, THEN skip. Rewrite the stale row to the fictional identity
      // and SUSPEND it. No password is invented — the hash is replaced with a
      // sentinel that cannot be produced by any hash function, so the previously
      // published default stops working, and `status` is set so the account is
      // refused before a password is ever checked.
      if (account.password === null) {
        // KS-966 F2: the hint must name the variable that governs THIS row.
        // It was hard-coded to DEMO_SECUURA_PASSWORD — right for the ...060
        // identity it was written for, and WRONG for admin@secuura.com, which
        // this change newly routes through this branch. An operator following
        // it would set a variable that seeds a different account and still find
        // their admin missing. Where an entry declares no name we say nothing
        // specific rather than naming the wrong one: a generic sentence is
        // honest, a wrong variable name is misinformation.
        const passwordVar = (account as { passwordVar?: string }).passwordVar;
        const hint = passwordVar
          ? `set ${passwordVar} to seed this account instead`
          : "set this account's seed-password environment variable to seed it instead";

        // KS-966 F3: find the stale row by EMAIL as well as by id.
        //
        // The remediation was keyed on getUserById(account.id) alone, so a row
        // carrying this address under any OTHER id — created by a test run, an
        // older seeder, or by hand — was never found. It survived ACTIVE with
        // its old password hash, which means the published credential kept
        // working on exactly the account this change exists to close.
        const byId = await getUserById(account.id);
        const byEmail = await getUserByEmail(account.email);
        const emailRowIsDistinct = byEmail !== null && byEmail.id !== account.id;

        if (byId) {
          const normEmail = account.email.toLowerCase().trim();
          await query(
            `UPDATE users SET
               email = $2,
               email_lookup_hash = $3,
               password_hash = $4,
               first_name = $5,
               last_name = $6,
               display_name = $7,
               status = 'suspended',
               updated_at = NOW()
             WHERE id = $1`,
            [
              account.id,
              await encryptPiiCol(normEmail, 'email', account.id),
              lookupHash(normEmail),
              UNUSABLE_PASSWORD_HASH,
              account.firstName ? await encryptPiiCol(account.firstName, 'first_name', account.id) : null,
              account.lastName ? await encryptPiiCol(account.lastName, 'last_name', account.id) : null,
              await encryptPiiCol(`${account.firstName} ${account.lastName}`, 'display_name', account.id),
            ],
          );
        }

        if (emailRowIsDistinct) {
          // Credential only — deliberately NOT the identity rewrite above.
          // This row was FOUND BY this address, so it already holds it; writing
          // it again is a no-op that would give two rows the same
          // email_lookup_hash and trip its unique index. Suspending it and
          // replacing the hash is what actually closes the hole: the account
          // stops being reachable, which is the point.
          await query(
            `UPDATE users SET
               password_hash = $2,
               status = 'suspended',
               updated_at = NOW()
             WHERE id = $1`,
            [byEmail.id, UNUSABLE_PASSWORD_HASH],
          );
        }

        if (byId || emailRowIsDistinct) {
          logger.warn('Demo user NOT seeded (no password supplied) — the pre-existing row was re-identified and SUSPENDED', {
            email: account.email,
            remediatedById: Boolean(byId),
            remediatedByEmail: emailRowIsDistinct,
            hint,
          });
        } else {
          logger.info('Demo user seeding skipped — no password supplied, and no pre-existing row to remediate', {
            email: account.email,
            hint,
          });
        }
        continue;
      }
      const passwordHash = await hashFn(account.password);
      const exists = await emailExists(account.email);
      if (exists) {
        // Ensure demo account always has the correct password, role, and status
        // (accounts may have been created by test runs with different credentials)
        const existing = await getUserByEmail(account.email);
        if (existing) {
          await updateUser(existing.id, {
            passwordHash,
            role: account.role,
            verificationLevel: account.verificationLevel,
            status: 'ACTIVE',
            emailVerified: true,
            tenantId: (account as any).tenantId,
            tenantSlug: (account as any).tenantSlug,
          });
          logger.info('Demo user updated to match seed config', { email: account.email, role: account.role });
        }
        continue;
      }

      // BACKLOG H5: handle id-collision-with-different-email case. The
      // pre-F-16 seed used real-looking domains (ox.ac.uk, bupa.com) which
      // were later switched to .invalid TLDs. The old rows are still in
      // the DB with the same UUIDs but old emails — createUser would
      // fail on users_pkey. Rewrite the email in place so the seeded
      // account becomes the documented one.
      const idCollision = await getUserById(account.id);
      if (idCollision) {
        const normEmail = account.email.toLowerCase().trim();
        const encryptedEmail = await encryptPiiCol(normEmail, 'email', account.id);
        const newEmailHash = lookupHash(normEmail);
        await query(
          `UPDATE users SET
             email = $2,
             email_lookup_hash = $3,
             password_hash = $4,
             first_name = $5,
             last_name = $6,
             display_name = $7,
             role = $8,
             verification_level = $9,
             status = 'ACTIVE',
             email_verified = true,
             tenant_id = $10,
             tenant_slug = $11,
             updated_at = NOW()
           WHERE id = $1`,
          [
            account.id,
            encryptedEmail,
            newEmailHash,
            passwordHash,
            account.firstName ? await encryptPiiCol(account.firstName, 'first_name', account.id) : null,
            account.lastName ? await encryptPiiCol(account.lastName, 'last_name', account.id) : null,
            await encryptPiiCol(`${account.firstName} ${account.lastName}`, 'display_name', account.id),
            account.role.toLowerCase(),
            account.verificationLevel.toLowerCase(),
            (account as any).tenantId,
            (account as any).tenantSlug,
          ],
        );
        logger.info('Demo user re-emailed to match seed config (id collision resolved)', { email: account.email });
        continue;
      }

      const user: User = {
        id: account.id,
        email: account.email,
        emailVerified: true,
        passwordHash,
        firstName: account.firstName,
        lastName: account.lastName,
        displayName: `${account.firstName} ${account.lastName}`,
        phoneVerified: false,
        mfaEnabled: false,
        role: account.role,
        verificationLevel: account.verificationLevel,
        status: 'ACTIVE',
        tenantId: (account as any).tenantId,
        tenantSlug: (account as any).tenantSlug,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      await createUser(user);
      logger.info('Demo user seeded', { email: account.email, verificationLevel: account.verificationLevel });
    } catch (err: any) {
      logger.error('Failed to seed demo user', { email: account.email, error: err?.message });
    }
  }
}

// =============================================================================
// PLATFORM ADMIN LOOKUP (multi-tenancy)
// =============================================================================

interface PlatformAdmin {
  id: string;
  email: string;
  passwordHash: string;
  name: string;
  role: string;
  mfaEnabled: boolean;
  mfaSecret: string | null;
  status: string;
}

// Read at call time (not module load) so the value reflects the live env even
// when it's configured after this module is first imported — and so it's
// observable in tests. The platform_admins table lives in this separate DB.
function platformDbUrl(): string {
  return process.env.PLATFORM_DATABASE_URL || '';
}

/**
 * KS-158: lazily migrate a legacy-plaintext `users.mfa_secret` to encrypted
 * at rest. Called after a successful MFA verification (the user has just proven
 * control), so existing MFA users self-heal on next use without a blocking
 * backfill. No-op if the secret is already encrypted or absent.
 */
export async function reencryptMfaSecretIfLegacy(userId: string): Promise<void> {
  try {
    // KS-458: runs mid-login (pre-auth) — read via the carve-out lookup and
    // write with the row's own tenant so both sides satisfy fail-closed RLS.
    const r = await query<{ mfa_secret: string | null; tenant_id: string | null }>(
      `SELECT mfa_secret, tenant_id FROM auth_find_user_by_id($1)`,
      [userId],
    );
    const stored = r.rows[0]?.mfa_secret;
    // isEncryptedPii (not /^v\d+:/) so a d1: subject-DEK row is never
    // mistaken for plaintext and double-encrypted (KS-291).
    if (typeof stored === 'string' && stored !== '' && !isEncryptedPii(stored)) {
      const enc = await encryptPiiCol(stored, 'mfa_secret', userId);
      await query(`UPDATE users SET mfa_secret = $1, updated_at = NOW() WHERE id = $2`, [enc, userId], r.rows[0]?.tenant_id ?? undefined);
      logger.info('[KS-158] re-encrypted legacy plaintext mfa_secret', { userId });
    }
  } catch (err: any) {
    // Never fail the verify on a migration hiccup — just log.
    logger.error('[KS-158] mfa_secret re-encrypt failed', { userId, error: err?.message });
  }
}

export async function getPlatformAdmin(email: string): Promise<PlatformAdmin | null> {
  const dbUrl = platformDbUrl();
  if (!dbUrl) return null;
  try {
    const { Pool } = await import('pg');
    const pool = new Pool({ connectionString: dbUrl, max: 2 });
    const result = await pool.query(
      `SELECT id, email, password_hash, name, role, mfa_enabled, mfa_secret, status
       FROM platform_admins WHERE email = $1 AND status = 'active'`,
      [email.toLowerCase()],
    );
    await pool.end();
    if (result.rows.length === 0) return null;
    const row = result.rows[0];
    return {
      id: row.id,
      email: row.email,
      passwordHash: row.password_hash,
      name: row.name,
      role: row.role,
      mfaEnabled: row.mfa_enabled,
      // KS-171: decrypt the at-rest TOTP seed (tolerant of legacy plaintext).
      mfaSecret: decryptPlatformAdminMfaSecret(row.mfa_secret, row.id),
      status: row.status,
    };
  } catch (err) {
    logger.warn('Platform admin lookup failed (platform DB may not be configured)', { error: (err as Error).message });
    return null;
  }
}

/**
 * KS-171: lazily migrate a legacy-plaintext `platform_admins.mfa_secret` to
 * encrypted at rest. Called after a successful platform-admin MFA verification
 * (the admin has just proven control of the seed), so existing admins self-heal
 * on next login without a blocking backfill. Encrypts with AAD
 * platform_admins.mfa_secret.<id>. No-op if already encrypted or absent; never
 * throws — a migration hiccup must not fail the login.
 */
export async function reencryptPlatformAdminMfaSecretIfLegacy(adminId: string): Promise<void> {
  const dbUrl = platformDbUrl();
  if (!dbUrl) return;
  try {
    const { Pool } = await import('pg');
    const pool = new Pool({ connectionString: dbUrl, max: 2 });
    try {
      const r = await pool.query<{ mfa_secret: string | null }>(
        `SELECT mfa_secret FROM platform_admins WHERE id = $1`,
        [adminId],
      );
      const stored = r.rows[0]?.mfa_secret;
      if (typeof stored === 'string' && stored !== '' && !/^v\d+:/.test(stored)) {
        const enc = encryptField(stored, `platform_admins.mfa_secret.${adminId}`) as string;
        await pool.query(
          `UPDATE platform_admins SET mfa_secret = $1, updated_at = NOW() WHERE id = $2`,
          [enc, adminId],
        );
        logger.info('[KS-171] re-encrypted legacy plaintext platform_admins.mfa_secret', { adminId });
      }
    } finally {
      await pool.end();
    }
  } catch (err: any) {
    // Never fail the login on a migration hiccup — just log.
    logger.error('[KS-171] platform_admins.mfa_secret re-encrypt failed', { adminId, error: err?.message });
  }
}

/**
 * T1-B (F-12 phase 2): update a platform_admin's password_hash. Used by the
 * login UPGRADE-ON-VERIFY path so bcrypt admins migrate to argon2id on
 * next successful login.
 */
export async function updatePlatformAdminPassword(adminId: string, newHash: string): Promise<void> {
  const dbUrl = platformDbUrl();
  if (!dbUrl) throw new Error("PLATFORM_DATABASE_URL not configured");
  const { Pool } = await import('pg');
  const pool = new Pool({ connectionString: dbUrl, max: 2 });
  try {
    await pool.query(
      `UPDATE platform_admins SET password_hash = $1, updated_at = NOW() WHERE id = $2`,
      [newHash, adminId],
    );
  } finally {
    await pool.end();
  }
}
