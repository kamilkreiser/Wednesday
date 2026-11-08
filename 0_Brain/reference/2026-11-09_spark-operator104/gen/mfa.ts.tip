/**
 * =============================================================================
 * MFA ROUTES — Multi-Factor Authentication
 * =============================================================================
 * Uses the userRepo for persistence. MFA pending setup state is stored in
 * the database with a 10-minute expiry.
 * =============================================================================
 */

import { Router, Response } from 'express';
import { z } from 'zod';
import { AuthenticatedRequest } from '../types';
import { authenticate } from '../middleware/authenticate';
import {
  BadRequestError,
  InvalidCredentialsError,
  ConflictError,
} from '../middleware/errorHandler';
import { logger } from '../utils/logger';
import {
  generateTotpSecret,
  generateOtpAuthUri,
  verifyTotpCode,
  verifyBackupCode,
  generateBackupCodes,
  hashBackupCode,
} from '../services/totp';
// KS-732: this file had NO password verification at all — `bcrypt|compare(|
// verifyPassword` matched 0 times here against 6 in routes/auth.ts.
import { verifyPassword } from '../services/password';
import * as userRepo from '../repositories/userRepo';
import { query } from '../db';
import {
  decryptField,
  encryptFieldWithDek,
  decryptFieldWithDek,
  isSubjectDekCiphertext,
  isEncryptedPii,
} from '@secuura/shared';
import { subjectDeks } from '../services/subjectDeks';

export const mfaRoutes = Router();

// --- Pending MFA setup helpers (DB-backed) ---
// KS-158: the pending TOTP seed is encrypted at rest (AAD bound to the user).
// A stolen mfa_pending_setups row must not yield a usable seed. Reads tolerate
// a legacy-plaintext value (these rows expire in 10 minutes regardless).

const PENDING_AAD = (userId: string) => `mfa_pending.secret.${userId}`;

async function storePendingSetup(userId: string, secret: string, expiresAt: Date): Promise<void> {
  // KS-291: the pending seed is per-subject data — encrypt under the user's
  // own DEK so it is crypto-shredded with the rest of their PII on erasure.
  const dek = await subjectDeks.getOrCreateDek(userId);
  const stored = encryptFieldWithDek(secret, PENDING_AAD(userId), dek) ?? secret;
  await query(
    `INSERT INTO mfa_pending_setups (user_id, secret, expires_at)
     VALUES ($1, $2, $3)
     ON CONFLICT (user_id) DO UPDATE SET secret = $2, expires_at = $3`,
    [userId, stored, expiresAt],
  );
}

async function getPendingSetup(userId: string): Promise<{ secret: string; expiresAt: Date } | null> {
  const result = await query(
    `SELECT secret, expires_at FROM mfa_pending_setups
     WHERE user_id = $1 AND expires_at > NOW() LIMIT 1`,
    [userId],
  );
  if (result.rows.length > 0) {
    const stored = result.rows[0].secret as string;
    // KS-291 dual-format read: d1: rows under the subject DEK, v<N>: rows
    // under the master keyring (migration tail), else legacy plaintext
    // (pre-KS-158). These rows expire within 10 minutes regardless.
    let secret: string;
    if (isSubjectDekCiphertext(stored)) {
      const dek = await subjectDeks.getDek(userId);
      secret = dek ? (decryptFieldWithDek(stored, PENDING_AAD(userId), dek) ?? '') : '';
    } else if (isEncryptedPii(stored)) {
      secret = decryptField(stored, PENDING_AAD(userId)) ?? '';
    } else {
      secret = stored;
    }
    return { secret, expiresAt: new Date(result.rows[0].expires_at) };
  }
  return null;
}

async function deletePendingSetup(userId: string): Promise<void> {
  await query(`DELETE FROM mfa_pending_setups WHERE user_id = $1`, [userId]);
}

// Validation schemas
const setupSchema = z.object({
  totpCode: z.string().length(6).regex(/^\d+$/),
});

// KS-622: the /verify request schema went with the retired endpoint — the
// HANDLER answers 410 without reading a body. It is not the first thing to see
// the body, though: `express.json()` is mounted at app level ahead of this
// router, so a malformed payload is rejected there and errorHandler.ts returns
// 400 INVALID_JSON without this handler ever running. (An earlier version of
// this comment said the route "answers 410 before reading a body"; the
// pre-merge sweep measured a 400 and disproved it — #745 ask 4.) The published
// contract therefore declares 400 alongside 410; see auth.openapi.ts and
// __tests__/ks622-retired-route-contract.test.ts.
// Login's own schema validates `mfaCode` for the surviving path.

const disableSchema = z.object({
  // KS-732 (#872 review, note 1): OPTIONAL. It was required, so a wallet or
  // social account — the accounts the else-branch below exists for — had to post
  // a dummy string that is never verified. That is the same "collect a credential
  // and discard it" wart this ticket removes, surviving in the schema.
  //
  // ⚠ THIS RELAXES A STATUS CODE, and that is worth saying out loud rather than
  // filing under "additive": a PASSWORD account that omits the field used to get
  // 400 from Zod and now gets 401 from the branch below. Both are refusals, and
  // 401 is the better one here — a 400-vs-401 split would tell an unauthenticated
  // caller which accounts carry a password. No request that succeeds today
  // starts failing.
  password: z.string().min(1).optional(),
  totpCode: z.string().length(6).regex(/^\d+$/).optional(),
  // KS-732 — ADDITIVE, and it has to be a separate field. `totpCode` is
  // `.length(6).regex(/^\d+$/)` while generateBackupCodes() emits 8-char
  // base32, so a backup code can never reach the handler through it; code that
  // read one from `totpCode` would be DEAD. Widening `totpCode` instead would
  // change an existing field's accepted values; adding a field cannot make any
  // request that is valid today start failing.
  // The pattern is the 8-char alternative of the platform's own
  // MFA_CODE_PATTERN (passwordLoginGate.ts:87), not a second opinion about what
  // a backup code looks like.
  backupCode: z.string().regex(/^[A-Za-z0-9]{8}$/).optional(),
});

// =============================================================================
// GET /api/auth/mfa/status
// =============================================================================
mfaRoutes.get('/status', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const userId = req.user?.userId;
    if (!userId) throw new InvalidCredentialsError();

    const user = await userRepo.getUserById(userId);

    res.json({
      success: true,
      data: {
        mfaEnabled: user?.mfaEnabled || false,
        mfaType: user?.mfaSecret ? 'totp' : null,
        backupCodesRemaining: user?.mfaBackupCodes?.length || 0,
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// POST /api/auth/mfa/setup/start
// =============================================================================
mfaRoutes.post('/setup/start', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const userId = req.user?.userId;
    if (!userId) throw new InvalidCredentialsError();

    const user = await userRepo.getUserById(userId);
    if (!user) throw new InvalidCredentialsError();
    if (user.mfaEnabled) throw new ConflictError('MFA is already enabled');

    const secret = generateTotpSecret();
    const otpAuthUri = generateOtpAuthUri(secret, user.email);
    const expiresAt = new Date(Date.now() + 10 * 60 * 1000);

    await storePendingSetup(userId, secret, expiresAt);

    logger.info('MFA setup started', { userId });

    res.json({
      success: true,
      data: {
        secret,
        otpAuthUri,
        expiresAt: new Date(Date.now() + 10 * 60 * 1000),
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// POST /api/auth/mfa/setup/verify
// =============================================================================
mfaRoutes.post('/setup/verify', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const userId = req.user?.userId;
    if (!userId) throw new InvalidCredentialsError();

    const data = setupSchema.parse(req.body);

    const pending = await getPendingSetup(userId);
    if (!pending) throw new BadRequestError('No pending MFA setup. Please start setup first.');
    if (new Date() > pending.expiresAt) {
      await deletePendingSetup(userId);
      throw new BadRequestError('MFA setup has expired. Please start again.');
    }

    if (!verifyTotpCode(pending.secret, data.totpCode)) {
      throw new InvalidCredentialsError();
    }

    const backupCodes = generateBackupCodes(10);
    const hashedBackupCodes = await Promise.all(backupCodes.map(hashBackupCode));

    // Persist MFA state to DB via the repository — wrapped in error handling
    // to ensure atomicity: if cleanup fails, revert the user update.
    // KS-1052: checked — the backup codes are returned to the user below.
    await userRepo.updateUserOrThrow(userId, {
      mfaEnabled: true,
      mfaSecret: pending.secret,
      mfaBackupCodes: hashedBackupCodes,
      verificationLevel: 'STANDARD',
    }, 'MFA setup');

    try {
      await deletePendingSetup(userId);
    } catch (cleanupErr) {
      // Revert the user update to maintain consistency
      logger.error('Failed to delete pending MFA setup — reverting user update', { userId, error: cleanupErr });
      // KS-1052: this is the ONE site that deliberately does NOT use
      // updateUserOrThrow. It is a compensating revert inside a catch, and
      // throwing here would replace the BadRequestError below with a 503,
      // hiding the failure the user actually needs to see.
      //
      // But it must not be silent either: if the revert does not land, the
      // account is left MFA-ENABLED with a pending setup that was never
      // cleaned up — strictly worse than the state we were compensating for.
      // So the return is checked and the inconsistency is named in the log.
      const reverted = await userRepo.updateUser(userId, {
        mfaEnabled: false,
        // KS-938: null, NOT undefined. updateUser skips any field whose value is
        // `undefined`, so `undefined` here emitted a PARTIAL update that never named
        // mfa_secret or mfa_backup_codes — the revert left a live TOTP seed and unspent
        // backup codes in the row. null passes the guard and writes SQL NULL.
        mfaSecret: null,
        // KS-938: as above. The encryption branch guards on `typeof val === 'string'`,
        // so a null can never enter it.
        mfaBackupCodes: null,
        verificationLevel: 'BASIC',
      } as any);
      if (!reverted) {
        logger.error(
          'MFA revert could not be confirmed — account may be left MFA-enabled with an uncleaned pending setup',
          { userId },
        );
      }
      throw new BadRequestError('MFA setup failed — please try again.');
    }

    logger.info('MFA setup completed', { userId });

    res.json({
      success: true,
      data: {
        mfaEnabled: true,
        backupCodes,
        message: 'MFA enabled successfully. Please save your backup codes securely.',
      },
    });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// POST /api/auth/mfa/verify — RETIRED (KS-622), always 410 Gone
// =============================================================================
// This endpoint redeemed a backup code with NO proof of factor one. It took
// `userId` straight from the request body, it was the only one of the six
// routes on mfaRoutes without authenticate() (deliberately, per KS-468 — it was
// the pre-auth login MFA-challenge step), and the login account-lockout could
// never engage on it because it never saw an email. It was also the ONLY path
// that could redeem a backup code: login's `mfaCode` was `^[0-9]{6}$` while a
// backup code is 8 characters, so login's own verifyBackupCode call could never
// receive one.
//
// Kam's ruling 2026-08-26 (option B): widen login to accept backup codes and
// retire this route. Login is the correct home — it verifies the password
// BEFORE it looks at `mfaCode`, so redemption now requires factor one by
// construction.
//
// Retired as 410 Gone rather than deleted so the retirement is discoverable:
// the path still resolves (preflight leg 4 stays honest) and the published
// contract says what happened instead of handing callers a bare 404.
//
// It performs NO lookup and NO redemption — asserted in the tests, because
// "returns 410" and "does not touch the user" are different claims.
mfaRoutes.post('/verify', (_req: AuthenticatedRequest, res: Response) => {
  res.status(410).json({
    success: false,
    error: {
      code: 'GONE',
      message:
        'POST /api/auth/mfa/verify is retired. Send the TOTP or backup code as ' +
        '`mfaCode` on POST /api/auth/login, which verifies the password first.',
    },
  });
});

// =============================================================================
// POST /api/auth/mfa/disable
// =============================================================================
mfaRoutes.post('/disable', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const userId = req.user?.userId;
    if (!userId) throw new InvalidCredentialsError();

    const data = disableSchema.parse(req.body);
    // KS-732 (#872 review): NOT getUserById. That selects USER_COLS, which
    // omits password_hash, so `user.passwordHash` was undefined for every
    // account and the password branch below never executed — the route silently
    // required a code from password accounts too, and the description asserted
    // a check that did not run. The unit suite could not see it because its
    // `../db` stub returned the whole row whatever the column list; the stub now
    // projects onto the selected columns, so this call is load-bearing.
    const user = await userRepo.getUserByIdWithPasswordHash(userId);
    if (!user) throw new InvalidCredentialsError();
    if (!user.mfaEnabled) throw new BadRequestError('MFA is not enabled');

    // KS-732 — DISABLING MFA MUST COST A PROOF OF POSSESSION.
    //
    // What stood here read `password` off the schema and never used it, and
    // gated the TOTP check on `data.totpCode` being PRESENT — so omitting the
    // code skipped verification entirely and any holder of a bearer removed the
    // second factor with `{"password":"anything"}`. Collecting a credential and
    // discarding it is worse than not asking: it reads to a client author as a
    // check.
    //
    // The ticket's first suggested remedy — "just verify the password" — is
    // NOT safe as written. getOrCreateWalletUser() builds its User with no
    // passwordHash at all (measured: 0 occurrences in routes/wallet.ts against
    // 10 in routes/auth.ts), and `password_hash` is NULLABLE since migration
    // 001. Requiring a password would make this route UNSATISFIABLE for a wallet
    // account: MFA could be enabled and never removed.
    //
    // So: require the strongest proof the account can actually produce, and
    // never nothing. The same "which proof can this account give" shape
    // services/passwordLoginGate.ts already uses.
    const totpOk =
      !!user.mfaSecret && !!data.totpCode && verifyTotpCode(user.mfaSecret, data.totpCode);

    if (user.passwordHash) {
      // A password account proves possession with the password it already
      // sends. A supplied TOTP code is still verified below rather than
      // ignored — a WRONG code must fail, not be skipped.
      // `password` is optional on the schema now, so absence is a refusal here
      // rather than a 400 — never a skipped check.
      if (!data.password || !(await verifyPassword(data.password, user.passwordHash))) {
        throw new InvalidCredentialsError();
      }
      if (data.totpCode && !totpOk) {
        throw new InvalidCredentialsError();
      }
    } else {
      // No password to verify (wallet / social). A valid TOTP code OR a valid
      // backup code is the only remaining proof, and one of them is REQUIRED —
      // so this branch can never be satisfied by a bearer alone, which is the
      // whole defect.
      const backupOk =
        !!data.backupCode &&
        Array.isArray(user.mfaBackupCodes) &&
        user.mfaBackupCodes.length > 0 &&
        (await verifyBackupCode(data.backupCode, user.mfaBackupCodes)).valid;
      if (!totpOk && !backupOk) {
        throw new InvalidCredentialsError();
      }
    }

    // KS-1052: a false "MFA disabled" locks the user out of their own account.
    await userRepo.updateUserOrThrow(userId, {
      mfaEnabled: false,
      // KS-938: null, NOT undefined — see the revert site above. A user who disables MFA
      // because the authenticator was compromised kept a re-armable seed in the row while
      // this call answered 200 "MFA disabled successfully".
      mfaSecret: null,
      // KS-938: null, NOT undefined.
      mfaBackupCodes: null,
      verificationLevel: 'BASIC',
    } as any, 'MFA disable');

    logger.info('MFA disabled', { userId });
    res.json({ success: true, message: 'MFA disabled successfully' });
  } catch (error) {
    next(error);
  }
});

// =============================================================================
// POST /api/auth/mfa/backup-codes/regenerate
// =============================================================================
mfaRoutes.post('/backup-codes/regenerate', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const userId = req.user?.userId;
    if (!userId) throw new InvalidCredentialsError();

    const { totpCode } = req.body;
    const user = await userRepo.getUserById(userId);
    if (!user || !user.mfaEnabled || !user.mfaSecret) {
      throw new BadRequestError('MFA is not enabled');
    }

    if (!totpCode || !verifyTotpCode(user.mfaSecret, totpCode)) {
      throw new InvalidCredentialsError();
    }

    const backupCodes = generateBackupCodes(10);
    const hashedBackupCodes = await Promise.all(backupCodes.map(hashBackupCode));

    // KS-1052: the response below says "Previous codes are now invalid" and
    // hands over new ones. On a write that did not land NEITHER is true — the
    // new codes do not work and the old ones still do.
    await userRepo.updateUserOrThrow(userId, { mfaBackupCodes: hashedBackupCodes }, 'Backup-code regeneration');

    logger.info('Backup codes regenerated', { userId });

    res.json({
      success: true,
      data: {
        backupCodes,
        message: 'New backup codes generated. Previous codes are now invalid.',
      },
    });
  } catch (error) {
    next(error);
  }
});
