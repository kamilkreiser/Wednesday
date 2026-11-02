/**
 * Wallet Authentication Routes
 * CIP-8 compliant wallet-based authentication for Cardano
 */

import { Router, Response } from 'express';
import { z } from 'zod';
import { v4 as uuidv4 } from 'uuid';
import crypto from 'crypto';
import { AuthenticatedRequest, User } from '../types';
import { generateTokenPair } from '../services/jwt';
import { createSession } from '../services/session';
import {
  AppError,
  BadRequestError,
  UnauthorizedError,
  NotFoundError,
  // KS-796 (KS-781 door 3): this route issues a full token pair, so it answers
  // the same 403 as login when the account has a second factor.
  MfaRequiredError,
} from '../middleware/errorHandler';
import {
  assertAccountMayReceiveCredential,
  mfaCodeRuntimeSchema,
} from '../services/passwordLoginGate';
import { logger } from '../utils/logger';
// KS-720: the middleware was never imported here, so `req.user` could not be
// populated inside this service and BOTH authenticated routes below fell into
// their `if (!req.user)` branch for every caller — including one carrying a
// bearer the gateway had already accepted.
import { authenticate } from '../middleware/authenticate';
import { verifyCIP8Signature, isValidCardanoAddress } from '../utils/cip8';
import { query } from '../db';
import { canonicalWalletAddress, syntheticWalletEmail } from '../utils/walletEmail';
import * as userRepo from '../repositories/userRepo';

export const walletRoutes = Router();

// =============================================================================
// CHALLENGE STORE — DB-first with in-memory fallback
// =============================================================================

interface Challenge {
  id: string;
  walletAddress: string;
  challenge: string;
  nonce: string;
  createdAt: Date;
  expiresAt: Date;
  used: boolean;
}

/** Store a challenge in DB */
async function storeChallenge(challenge: Challenge): Promise<void> {
  await query(
    `INSERT INTO wallet_auth_challenges (id, wallet_address, challenge, nonce, expires_at, used)
     VALUES ($1, $2, $3, $4, $5, $6)
     ON CONFLICT (id) DO NOTHING`,
    [challenge.id, challenge.walletAddress, challenge.challenge, challenge.nonce, challenge.expiresAt, false],
  );
}

/** Retrieve a challenge by ID from DB */
async function getChallenge(id: string): Promise<Challenge | undefined> {
  const result = await query(
    `SELECT id, wallet_address, challenge, nonce, created_at, expires_at, used
     FROM wallet_auth_challenges WHERE id = $1 LIMIT 1`,
    [id],
  );
  if (result.rows.length > 0) {
    const r = result.rows[0];
    return {
      id: r.id,
      walletAddress: r.wallet_address,
      challenge: r.challenge,
      nonce: r.nonce,
      createdAt: new Date(r.created_at),
      expiresAt: new Date(r.expires_at),
      used: r.used,
    };
  }
  return undefined;
}

/** Mark a challenge as used and delete it */
async function consumeChallenge(id: string): Promise<void> {
  await query(`DELETE FROM wallet_auth_challenges WHERE id = $1`, [id]);
}

// Cleanup expired challenges every 5 minutes
setInterval(async () => {
  try {
    await query(`DELETE FROM wallet_auth_challenges WHERE expires_at < NOW()`);
  } catch { /* silent */ }
}, 5 * 60 * 1000);

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

const challengeRequestSchema = z.object({
  walletAddress: z.string()
    .min(1, 'Wallet address is required')
    .refine(
      (addr) => isValidCardanoAddress(addr),
      { message: 'Invalid Cardano address format' }
    ),
});

// KS-796 F-6: exported for the identity assertion — see routes/auth.ts.
export const verifySignatureSchema = z.object({
  challengeId: z.string().uuid('Invalid challenge ID').optional(),
  nonce: z.string().optional(), // Alias for challengeId (for test compatibility)
  walletAddress: z.string().min(1, 'Wallet address is required'),
  signature: z.string().min(1, 'Signature is required'),
  key: z.string().optional(), // CIP-8 public key (hex)
  // KS-796: a wallet signature proves control of the wallet. It says nothing
  // about a second factor, and a wallet account CAN have one — the account is
  // created with `mfaEnabled: false` but the holder may switch it on later
  // through /api/users/me/mfa/*. So the route needs a channel to supply it.
  //
  // Empty counts as absent (KS-781 N-1): a form-backed client posting its whole
  // state sends `mfaCode: ""` for an account with no second factor, and
  // `.optional()` does not apply to a present empty string. That shape returned
  // 400 to every non-MFA user on door 1 before it was fixed.
  // KS-796 Q3: import the ONE definition rather than restating it. This route
  // previously hand-typed the union/optional/transform above — the same three
  // clauses doors 1 and 2 import from passwordLoginGate — which is precisely
  // the drift this door's own commit message said it would not introduce. Four
  // sites, one definition; the agreement test below asserts it.
  mfaCode: mfaCodeRuntimeSchema,
}).refine(
  (data) => data.challengeId || data.nonce,
  { message: 'Either challengeId or nonce is required' }
);

const linkWalletSchema = z.object({
  walletAddress: z.string().min(1),
  signature: z.string().min(1),
  challengeId: z.string().uuid(),
  // CIP-8 COSE_Key public key (hex). Required — verifyCIP8Signature has no
  // fallback path (audit A-02): without the public key, signature math is
  // skipped and the request is rejected.
  key: z.string().min(1, 'CIP-8 public key (hex) is required'),
});

// =============================================================================
// CONSTANTS
// =============================================================================

const CHALLENGE_EXPIRY_MINUTES = 5;
const CHALLENGE_PREFIX = 'SECUURA-AUTH-';

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Generate a cryptographically secure challenge
 */
function generateChallenge(walletAddress: string): Challenge {
  const nonce = crypto.randomBytes(16).toString('hex');
  const timestamp = Date.now();
  const challengeString = `${CHALLENGE_PREFIX}${timestamp}-${nonce}`;
  
  const challenge: Challenge = {
    id: uuidv4(),
    walletAddress,
    challenge: challengeString,
    nonce,
    createdAt: new Date(),
    expiresAt: new Date(Date.now() + CHALLENGE_EXPIRY_MINUTES * 60 * 1000),
    used: false,
  };
  
  return challenge;
}

// CIP-8 signature verification is now in utils/cip8.ts

/**
 * Get or create user by wallet address (DB-backed via userRepo)
 */
async function getOrCreateWalletUser(walletAddress: string): Promise<User> {
  // KS-806: the wallet is identified by its CANONICAL (lowercase) address. CIP-8 verification compares the claimed and the
  // signed address case-insensitively, so one wallet can arrive in several casings; keyed on the raw string each casing was
  // a new account, and the email below (a hash of the address) would otherwise differ per casing too.
  const canonical = canonicalWalletAddress(walletAddress);
  // Look up by wallet address in DB
  // KS-458: wallet auth runs pre-auth (the signed challenge is the
  // credential) — use the SECURITY DEFINER carve-out lookup.
  // auth_find_user_by_wallet compares for exact equality, and a row created before this change stored the address as the
  // client sent it. So the casing the wallet PRESENTED is tried first, then the canonical form: a legacy row stored in
  // that exact casing is found even after the wallet has also logged in with the canonical casing (which, finding no
  // legacy row under it, created a second account; trying the canonical form first would then shadow the legacy row and
  // orphan it). A legacy row stored in a casing the wallet does not present is not found by any lookup here; reaching it
  // needs a case-insensitive lookup function, which is a migration and is not part of this change.
  for (const candidate of [...new Set([walletAddress, canonical])]) {
    const result = await query(
      `SELECT * FROM auth_find_user_by_wallet($1)`,
      [candidate],
    );
    if (result.rows.length > 0) {
      // KS-458: still pre-auth — carve-out lookup.
      const existing = await userRepo.getUserByIdPreAuth(result.rows[0].id);
      if (existing) return existing;
    }
  }

  // Create a new wallet user via userRepo (persists to DB)
  const user: User = {
    id: uuidv4(),
    email: syntheticWalletEmail(walletAddress),
    emailVerified: false,
    phoneVerified: false,
    mfaEnabled: false,
    role: 'OWNER',
    verificationLevel: 'BASIC',
    status: 'ACTIVE',
    createdAt: new Date(),
    updatedAt: new Date(),
    walletAddress: canonical,
    authMethod: 'wallet',
  };
  await userRepo.createUser(user);
  logger.info('Created new wallet user', { userId: user.id, address: walletAddress.slice(0, 20) });
  return user;
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * POST /api/auth/wallet/challenge
 * Request a challenge for wallet authentication
 */
walletRoutes.post('/challenge', async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const data = challengeRequestSchema.parse(req.body);
    
    // Generate challenge and persist
    const challenge = generateChallenge(data.walletAddress);
    await storeChallenge(challenge);
    
    logger.info(`Challenge generated for wallet: ${data.walletAddress.slice(0, 20)}...`);
    
    res.status(200).json({
      challengeId: challenge.id,
      nonce: challenge.id, // Use challengeId as nonce for test compatibility with multi-instance deployments
      challenge: challenge.challenge,
      expiresAt: challenge.expiresAt.toISOString(),
      message: 'Sign this message with your wallet to authenticate',
      format: 'CIP-8',
    });
  } catch (error) {
    next(error);
  }
});

/**
 * Helper to find challenge by ID or nonce (DB-only)
 */
async function findChallenge(challengeId?: string, nonce?: string): Promise<Challenge | undefined> {
  if (challengeId) {
    return getChallenge(challengeId);
  }

  if (nonce) {
    // Try nonce as a challengeId (UUID format) for test compatibility
    const direct = await getChallenge(nonce);
    if (direct) return direct;

    // Search by actual nonce field in DB
    const result = await query(
      `SELECT id, wallet_address, challenge, nonce, created_at, expires_at, used
       FROM wallet_auth_challenges WHERE nonce = $1 AND expires_at > NOW() LIMIT 1`,
      [nonce],
    );
    if (result.rows.length > 0) {
      const r = result.rows[0];
      return {
        id: r.id, walletAddress: r.wallet_address, challenge: r.challenge,
        nonce: r.nonce, createdAt: new Date(r.created_at),
        expiresAt: new Date(r.expires_at), used: r.used,
      };
    }
  }

  return undefined;
}

/**
 * POST /api/auth/wallet/verify
 * POST /api/auth/wallet/authenticate (alias)
 * Verify signed challenge and issue tokens
 */
async function handleWalletVerify(req: AuthenticatedRequest, res: Response, next: (err?: unknown) => void) {
  try {
    const data = verifySignatureSchema.parse(req.body);
    
    // Get challenge by ID or nonce (DB-first)
    const challenge = await findChallenge(data.challengeId, data.nonce);
    if (!challenge) {
      throw new NotFoundError('Challenge not found or expired');
    }
    
    // Verify challenge hasn't expired
    if (challenge.expiresAt < new Date()) {
      await consumeChallenge(challenge.id);
      throw new BadRequestError('Challenge has expired');
    }
    
    // Verify challenge hasn't been used
    if (challenge.used) {
      throw new BadRequestError('Challenge has already been used');
    }
    
    // Verify wallet address matches
    if (challenge.walletAddress !== data.walletAddress) {
      throw new BadRequestError('Wallet address does not match challenge');
    }
    
    // Verify signature using CIP-8
    const verificationResult = await verifyCIP8Signature(
      data.walletAddress,
      challenge.challenge,
      data.signature,
      data.key
    );
    
    if (!verificationResult.valid) {
      logger.warn('Invalid signature for wallet', {
        address: data.walletAddress.slice(0, 20),
        error: verificationResult.error,
      });
      throw new UnauthorizedError(verificationResult.error || 'Invalid signature');
    }
    
    // Get or create user (DB-backed)
    const user = await getOrCreateWalletUser(data.walletAddress);

    // -----------------------------------------------------------------------
    // KS-796 (KS-781 door 3) — THE SIGNATURE PROVED THE WALLET, NOT THE ACCOUNT.
    //
    // Everything above verifies that the caller controls the wallet address.
    // Nothing above asks whether the ACCOUNT that address resolves to may be
    // issued a credential at all. Before this call, `routes/wallet.ts`
    // referenced neither `isLockedOut`, nor `user.status`, nor `mfaEnabled`
    // anywhere ahead of the mint — measured, with `routes/auth.ts` as the
    // control at 13 and 4 hits for the same patterns.
    //
    // The sharpest consequence needs no account-linking and no second factor:
    // `getOrCreateWalletUser` returns an EXISTING user whatever its status, so
    // an admin could SUSPEND a wallet account and it would keep minting full
    // token pairs. Suspension was not a thing this door could observe.
    //
    // Shared with door 1 by construction rather than by convention — a third
    // inline copy of these rules is precisely what produced KS-737 and KS-781.
    // -----------------------------------------------------------------------
    const accountGate = await assertAccountMayReceiveCredential(user, {
      mfaCode: data.mfaCode,
      sourceIp: req.ip || 'unknown',
      route: 'POST /api/auth/wallet/verify',
    });
    if (!accountGate.ok) {
      if (accountGate.reason === 'mfa_required') throw new MfaRequiredError();
      // Uniform refusal (pen-test F-11): a suspended, deactivated or
      // locked-out account is not distinguishable here from a bad signature.
      throw new UnauthorizedError('Invalid signature');
    }

    // Create session — wallet auth is a SPA flow (user signs a challenge in
    // their Cardano wallet extension via the browser), so clientType: 'browser'.
    const session = await createSession(
      user,
      req.ip || 'unknown',
      req.headers['user-agent'] || 'unknown',
      undefined,
      'browser',
    );
    
    // Generate tokens with session ID
    const tokens = generateTokenPair(user, session.id);
    
    logger.info('Wallet authentication successful', { address: data.walletAddress.slice(0, 20) });
    
    // Consume challenge (delete from DB + memory)
    await consumeChallenge(challenge.id);
    
    res.status(200).json({
      ...tokens,
      token: tokens.accessToken, // Alias for test compatibility
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        verificationLevel: user.verificationLevel,
        walletAddress: user.walletAddress,
      },
      sessionId: session.id,
    });
  } catch (error) {
    next(error);
  }
}

// Register both endpoints
walletRoutes.post('/verify', handleWalletVerify);
walletRoutes.post('/authenticate', handleWalletVerify);

/**
 * GET /api/auth/wallet/status
 * Check whether a wallet address is registered.
 *
 * KS-1009: this route is PUBLIC by design (KS-720, KS-942): a wallet address is public and sign-in must know whether to offer
 * "sign in" or "register". It therefore answers ONLY whether the wallet is registered. It used to add the account's internal user
 * id, role and creation time for a registered wallet, so anyone holding a public address could resolve it to an internal id and
 * a role without a token. Nothing in the repository read those fields. Do not add any account attribute to this response.
 */
walletRoutes.get('/status/:walletAddress', async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    const { walletAddress } = req.params;

    // KS-458: pre-auth wallet lookup — SECURITY DEFINER carve-out. Only the id is read: it is the least the branch needs.
    const result = await query(
      `SELECT id FROM auth_find_user_by_wallet($1)`,
      [walletAddress],
    );

    if (result.rows.length === 0 || !result.rows[0].id) {
      res.json({ exists: false, message: 'Wallet not registered' });
      return;
    }

    res.json({ exists: true });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/auth/wallet/link
 * Link a wallet to an existing account (requires authentication)
 */
// KS-720: `authenticate()` is applied HERE and on /unlink only. /challenge,
// /verify, /authenticate and /status/:walletAddress are public by design and
// must stay that way — the risk of this fix is over-applying it, so the router
// is deliberately NOT blanketed.
//
// KS-942: that last sentence used to read "A cell pins that the four stay open"
// and it was FALSE for /authenticate — gating that route alone left the whole
// services/auth suite green (43 files, 595 tests, 0 failed). The cell now exists
// and is named here so the claim and its guard cannot drift apart again:
//
//   __tests__/ks942-public-wallet-routes-stay-open.test.ts
//
// It asserts each of the four answers WITHOUT a bearer AND emits a marker only a
// working route produces — `not 401` alone passes for a route that is merely
// broken. Note it deliberately does NOT live in ks796-wallet-verify-account-gate:
// that file mocks THIS module's `authenticate` to a passthrough, so no assertion
// added there can see a gate at all.
walletRoutes.post('/link', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    if (!req.user) {
      throw new BadRequestError('Authentication required to link wallet');
    }

    const data = linkWalletSchema.parse(req.body);

    // Get challenge (DB-first)
    const challenge = await getChallenge(data.challengeId);
    if (!challenge) {
      throw new NotFoundError('Challenge not found or expired');
    }

    // Verify signature using CIP-8 — public key (data.key) is now required.
    const verificationResult = await verifyCIP8Signature(
      data.walletAddress,
      challenge.challenge,
      data.signature,
      data.key
    );

    if (!verificationResult.valid) {
      throw new UnauthorizedError(verificationResult.error || 'Invalid signature');
    }

    // Link wallet to user via userRepo (persists to DB)
    //
    // KS-943: the return is CHECKED, not discarded. updateUser now answers null
    // when its UPDATE matched 0 rows — the case fail-closed RLS produces from an
    // unresolved tenant GUC. Answering "Wallet linked successfully" over a write
    // that never landed is the same lie KS-720 removed from the unlink path, one
    // step further in.
    const linked = await userRepo.updateUser(req.user.userId, { walletAddress: data.walletAddress });
    if (!linked) {
      throw new AppError(
        'Wallet link did not persist — the update matched no row',
        500,
        'WALLET_LINK_NOT_PERSISTED',
      );
    }

    // Consume challenge
    await consumeChallenge(data.challengeId);

    logger.info('Wallet linked to user', { userId: req.user.userId });

    res.json({
      success: true,
      message: 'Wallet linked successfully',
      walletAddress: data.walletAddress,
    });
  } catch (error) {
    next(error);
  }
});

/**
 * DELETE /api/auth/wallet/unlink
 * Unlink a wallet from current account (requires authentication)
 */
walletRoutes.delete('/unlink', authenticate(), async (req: AuthenticatedRequest, res: Response, next) => {
  try {
    if (!req.user) {
      throw new BadRequestError('Authentication required');
    }

    // Get user to check they have a wallet linked
    const user = await userRepo.getUserById(req.user.userId);
    if (!user?.walletAddress) {
      throw new BadRequestError('No wallet linked to this account');
    }

    // KS-720: `null`, NOT `undefined`. userRepo.updateUser's write loop guards
    // each field with `tsField in updates && updates[tsField] !== undefined`, so
    // an `undefined` value is SKIPPED — it produced zero setClauses and issued NO
    // UPDATE AT ALL, while this line's comment said "persists to DB" and the
    // handler returned success. Measured, with the link shape and a known-good
    // field as controls. `null` passes that guard and writes wallet_address=NULL.
    //
    // The guard itself is NOT changed: updateUser is shared by many routes and
    // BACKLOG.md already tracks a separate deferred defect in it. Fixing the
    // caller keeps this change to one endpoint.
    //
    // KS-943: the return is CHECKED, not discarded. The KS-720 note above fixed
    // WHICH value is written; this fixes whether the write is verified to have
    // happened at all. updateUser answers null on a 0-row UPDATE, and answering
    // "Wallet unlinked successfully" over that is the residual of the same class.
    const unlinked = await userRepo.updateUser(req.user.userId, { walletAddress: null } as any);
    if (!unlinked) {
      throw new AppError(
        'Wallet unlink did not persist — the update matched no row',
        500,
        'WALLET_UNLINK_NOT_PERSISTED',
      );
    }

    logger.info('Wallet unlinked from user', { userId: req.user.userId });

    res.json({
      success: true,
      message: 'Wallet unlinked successfully',
    });
  } catch (error) {
    next(error);
  }
});
