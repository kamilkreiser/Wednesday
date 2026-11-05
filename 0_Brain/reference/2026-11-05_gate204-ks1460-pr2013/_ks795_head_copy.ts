/**
 * =============================================================================
 * KS-795 (KS-781 door 2) — the social callback must not link an existing
 * account on an email match alone
 * =============================================================================
 * `GET /api/auth/social/:provider/callback` resolved a user by provider id and,
 * failing that, by `profile.email` — and on a hit attached the social identity
 * to that account and minted a token pair. A profile carrying the victim's
 * address was therefore enough to take the victim's account.
 *
 * WHY "REQUIRE profile.emailVerified" IS NOT THE FIX
 * --------------------------------------------------
 * Half the adapters do not derive that flag from anything:
 *
 *   google.ts:59              Boolean(profile.verified_email)   the provider's flag
 *   apple.ts:50               Boolean(payload.email_verified)   the provider's flag
 *   linkedin.ts:56            Boolean(profile.email_verified)   the provider's flag
 *   github.ts:65 / :69        primary.verified on ONE branch, literal `true` on
 *                             the other — one boolean reaches the route and it
 *                             cannot tell which branch produced it
 *   facebook.ts:54            Boolean(profile.email)   PRESENCE, not verification
 *   microsoft-personal.ts:58  true                     literal
 *
 * So the rule under test is SOUND DERIVATION *and* a true flag, and the refusal
 * is TERMINAL — leaving the user unresolved would fall into the CREATE branch
 * and insert a second row on an address that already has one.
 *
 * WHAT THIS FILE DELIBERATELY DOES NOT MOCK
 * -----------------------------------------
 * `mayAutoLinkByEmail` and `PROVIDER_EMAIL_VERIFICATION_IS_SOUND` are THE THING
 * UNDER TEST. Only `SocialProviderFactory` is replaced (a real provider needs a
 * real OAuth app; see the probe recorded on KS-795), so the decision function
 * that runs here is the shipped one.
 *
 * RUNTIME STATUS, stated so nobody reads this suite as more than it is: the
 * front-door probe could not reach this branch — zero providers are configured
 * on this stack — but the enablement check was measured to be the ONLY barrier
 * (two `.env.local` variables moved the same unauthenticated request into the
 * live GitHub token exchange, with an unconfigured provider as the control).
 * These cases drive the REAL handler; they do not drive a real provider.
 * =============================================================================
 */

import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import express from 'express';
import { randomUUID } from 'node:crypto';

const VICTIM_EMAIL = 'victim@secuura.local';

const state = vi.hoisted(() => ({
  /** what the stubbed provider hands back */
  profileEmail: 'victim@secuura.local',
  profileEmailVerified: true,
  /** does an account already carry this social identity? */
  alreadyLinked: false,
  /** does an account with the profile's email exist? */
  emailAccountExists: true,
  /** KS-806: which email that existing account carries (default: the victim's) */
  existingEmail: '' as string,
  /** KS-795 part (a): the resolved account's own condition */
  accountStatus: 'ACTIVE' as string,
  accountMfaEnabled: false,
  /** KS-795 F-4: override the provider identity, to model TWO distinct ones */
  providerId: '' as string,
}));

const silentLogger = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
vi.mock('../utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silentLogger, createLogger: () => silentLogger }));

// ONLY the factory is stubbed. `mayAutoLinkByEmail` and the soundness table are
// imported from the real module, because they are the subject.
vi.mock('../providers/social', async (importOriginal) => {
  const real = await importOriginal<Record<string, unknown>>();
  const NAMES = ['google', 'linkedin', 'facebook', 'apple', 'github', 'microsoft_personal'];
  class StubFactory {
    get(name: string) {
      if (!NAMES.includes(name)) return undefined;
      return {
        name,
        getAuthUrl: () => 'https://provider.test/auth',
        exchangeCode: async () => ({
          providerId: state.providerId || `${name}-provider-id-1`,
          provider: name,
          email: state.profileEmail,
          emailVerified: state.profileEmailVerified,
          displayName: 'Victim',
          firstName: 'Vic',
          lastName: 'Tim',
          rawProfile: {},
        }),
      };
    }
    getEnabled() { return NAMES; }
    has(n: string) { return NAMES.includes(n); }
    isValidProvider(n: string) { return NAMES.includes(n); }
  }
  return { ...real, SocialProviderFactory: StubFactory };
});

const createdUsers: unknown[] = [];
const linkWrites: Array<{ id: string; updates: Record<string, unknown> }> = [];

vi.mock('../repositories/userRepo', () => ({
  getUserBySocialId: vi.fn(async () =>
    state.alreadyLinked
      ? { id: 'user-linked', email: VICTIM_EMAIL, status: state.accountStatus, mfaEnabled: state.accountMfaEnabled, mfaSecret: 'JBSWY3DPEHPK3PXP', verificationLevel: 'SOCIAL' }
      : null,
  ),
  getUserByEmail: vi.fn(async (email: string) =>
    state.emailAccountExists && email === (state.existingEmail || VICTIM_EMAIL)
      ? { id: 'user-victim', email: state.existingEmail || VICTIM_EMAIL, status: state.accountStatus, mfaEnabled: state.accountMfaEnabled, mfaSecret: 'JBSWY3DPEHPK3PXP', verificationLevel: 'BASIC' }
      : null,
  ),
  updateUser: vi.fn(async (id: string, updates: Record<string, unknown>) => {
    linkWrites.push({ id, updates });
    return null;
  }),
  // KS-1460 (rows 4 and 6): the SOCIAL raise now goes through updateUserOrThrow. It is recorded in the
  // same list and lands (a row comes back), so every assertion in this file reads exactly as before.
  updateUserOrThrow: vi.fn(async (id: string, updates: Record<string, unknown>) => {
    linkWrites.push({ id, updates });
    return { id, ...updates };
  }),
  createUser: vi.fn(async (u: unknown) => { createdUsers.push(u); return u; }),
  getPlatformAdmin: vi.fn(async () => null),
  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
}));

/**
 * KS-722 Shape 1 — an IN-MEMORY Redis double, not a null.
 *
 * `getRedisClient` used to return null, which was fine while nothing in this
 * route read Redis. The social callback now verifies the OAuth `state`, and it
 * FAILS CLOSED when Redis is unavailable — so a null client turned all 19 cases
 * below into 403 OAUTH_STATE_INVALID before any of their own subjects ran.
 *
 * The double is deliberately real rather than a mock of `consumeOAuthState`:
 * these cases then drive the ACTUAL store, so the burn-on-use and
 * provider-binding behaviour is exercised on every callback here, not just in
 * the state file's own tests.
 */
const redisStore = new Map<string, string>();
vi.mock('../services/session', () => ({
  createSession: vi.fn(async () => ({ id: 'sess-795' })),
  getRedisClient: vi.fn(() => ({
    setex: async (k: string, _ttl: number, v: string) => { redisStore.set(k, v); return 'OK'; },
    // KS-1967: the account lockout reads and writes through this client too. Its old fail-open
    // swallowed the TypeError this double's missing get/incr/expire/set/del raised, so these cases
    // never noticed; the lockout now refuses (503) when its store throws. This is the lockout surface
    // of a store that is UP and holds no lock and no count, which is what the cases effectively had
    // before. No assertion changed.
    get: async () => null,
    incr: async () => 1,
    expire: async () => 1,
    set: async () => 'OK',
    del: async () => 1,
    getdel: async (k: string) => { const v = redisStore.get(k) ?? null; redisStore.delete(k); return v; },
  })),
  validateSession: vi.fn(async () => true),
  updateSessionActivity: vi.fn(async () => undefined),
}));

// A recognisable credential: the assertion is "a token pair was MINTED", not
// "the status was 200" — a route could answer 500 having already minted one.
vi.mock('../services/jwt', () => ({
  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_SOCIAL_ACCESS_TOKEN', refreshToken: 'MINTED_SOCIAL_REFRESH', expiresIn: 900 })),
  verifyAccessToken: vi.fn(() => ({})),
}));
// Every middleware FACTORY the transitively-imported routers register — not
// only the one this route uses. `routes/users.ts` registers
// authenticateAccessOrConnector() at import time, so a partial mock makes the
// whole module graph fail to load (and the failure surfaces as an unrelated
// afterAll error, which is how it presented).
const passthrough = () => (_r: unknown, _s: unknown, n: () => void) => n();
vi.mock('../middleware/authenticate', () => ({
  authenticate: passthrough,
  authenticateAccessOrConnector: passthrough,
  requireRole: passthrough,
  requireVerificationLevel: passthrough,
  requireOwnership: passthrough,
  requireSameOrganization: passthrough,
}));
vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));
vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));

let server: Server;
let base: string;

beforeAll(async () => {
  const { authRoutes } = await import('../routes/auth');
  const { errorHandler } = await import('../middleware/errorHandler');
  const app = express();
  app.use(express.json());
  app.use('/api/auth', authRoutes);
  app.use(errorHandler);
  // Same finding as #818 F-05(b): bind loopback, matching the base URL below.
  server = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => server.once('listening', () => r()));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

afterAll(async () => {
  await new Promise<void>((r) => server.close(() => r()));
});

beforeEach(() => {
  state.profileEmail = VICTIM_EMAIL;
  state.profileEmailVerified = true;
  state.alreadyLinked = false;
  state.emailAccountExists = true;
  state.existingEmail = '';
  createdUsers.length = 0;
  linkWrites.length = 0;
  state.accountStatus = 'ACTIVE';
  state.accountMfaEnabled = false;
  state.providerId = '';
});

/**
 * Drive the callback as a legitimate caller: initiate first so a real `state`
 * exists, then present it (KS-722 Shape 1). Going through `storeOAuthState`
 * rather than seeding the map by hand means these cases would break if the key
 * shape or the provider binding ever drifted — which is the point of a double
 * instead of a mocked-out gate.
 */
async function callback(provider: string): Promise<{ status: number; body: string }> {
  const { storeOAuthState } = await import('../services/oauthState');
  const oauthState = `test-state-${randomUUID()}`;
  await storeOAuthState(oauthState, provider);
  const res = await fetch(
    `${base}/api/auth/social/${provider}/callback?code=stub-code&state=${encodeURIComponent(oauthState)}`,
    { redirect: 'manual' },
  );
  return { status: res.status, body: await res.text() };
}

/**
 * The writes that ATTACH AN IDENTITY, separated from the ones that do not.
 *
 * The happy path issues TWO updateUser calls: the link, and the `BASIC ->
 * SOCIAL` verification-level upgrade three statements later. An assertion on
 * the total call count is therefore stricter than the product and fails on the
 * correct behaviour — it did, on the first run of this file. The subject is
 * whether a social identity was attached, so that is what is counted.
 */
function socialIdWrites() {
  return linkWrites.filter(({ updates }) => Object.keys(updates).some((k) => k.endsWith('Id')));
}

/** No identity was attached and no credential left the building. */
function expectNothingIssued(body: string) {
  expect(socialIdWrites(), 'the social identity must not have been attached').toEqual([]);
  expect(createdUsers, 'a duplicate account must not have been created').toEqual([]);
  expect(body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
  expect(body).not.toContain('MINTED_SOCIAL_REFRESH');
}

describe('KS-795: auto-linking by email requires a SOUNDLY derived, true emailVerified', () => {
  // -------------------------------------------------------------------------
  // CONTROL 1 IS LOAD-BEARING. It is the only case asserting a link and a mint
  // DO happen. Without it, a harness that can never reach the link branch — a
  // broken factory stub, an unmounted route, a rejected query — would satisfy
  // every "was not linked" assertion in this file while testing nothing.
  // -------------------------------------------------------------------------
  it('CONTROL — google with a verified email links the existing account and mints', async () => {
    const res = await callback('google');
    expect(res.status).toBe(200);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(socialIdWrites()).toHaveLength(1);
    expect(socialIdWrites()[0]).toMatchObject({ id: 'user-victim', updates: { googleId: 'google-provider-id-1' } });
  });

  it('CONTROL — apple, a second sound provider, behaves the same', async () => {
    const res = await callback('apple');
    expect(res.status).toBe(200);
    expect(socialIdWrites()[0]?.updates).toMatchObject({ appleId: 'apple-provider-id-1' });
  });

  it('CONTROL — linkedin, the third sound provider, behaves the same', async () => {
    const res = await callback('linkedin');
    expect(res.status).toBe(200);
    expect(socialIdWrites()[0]?.updates).toMatchObject({ linkedinId: 'linkedin-provider-id-1' });
  });

  for (const provider of ['facebook', 'microsoft_personal', 'github']) {
    it(`refuses ${provider} — its emailVerified is not derived from the provider's own signal`, async () => {
      const res = await callback(provider);
      expect(res.status).toBe(403);
      expect(res.body).toContain('SOCIAL_SIGN_IN_REFUSED');
      expectNothingIssued(res.body);
    });
  }

  it('refuses a SOUND provider when the flag is false — soundness alone is not enough', async () => {
    state.profileEmailVerified = false;
    const res = await callback('google');
    expect(res.status).toBe(403);
    expect(res.body).toContain('SOCIAL_SIGN_IN_REFUSED');
    expectNothingIssued(res.body);
  });

  // -------------------------------------------------------------------------
  // The two cases that bound the change. The refusal is on LINKING an existing
  // account, not on the provider — get either wrong and this fix breaks sign-in
  // for everyone rather than closing a takeover.
  // -------------------------------------------------------------------------
  it('BOUND — an unsound provider with NO existing account still signs up normally', async () => {
    state.emailAccountExists = false;
    const res = await callback('facebook');
    expect(res.status).toBe(200);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(createdUsers).toHaveLength(1);
  });

  it('BOUND — an unsound provider ALREADY linked still signs in; the gate is on linking', async () => {
    state.alreadyLinked = true;
    const res = await callback('facebook');
    expect(res.status).toBe(200);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(socialIdWrites(), 'an already-linked identity must not be re-attached').toEqual([]);
  });
});

describe('KS-795: the soundness declaration cannot go quietly stale', () => {
  it('every social provider has an explicit soundness entry — a new one cannot default in', async () => {
    const { ALL_SOCIAL_PROVIDERS, PROVIDER_EMAIL_VERIFICATION_IS_SOUND } = await import('../providers/social');

    // CONTROLS: a walk that saw nothing would report no gaps for the wrong reason.
    expect(ALL_SOCIAL_PROVIDERS.length).toBeGreaterThan(0);
    expect(new Set(ALL_SOCIAL_PROVIDERS).size).toBe(ALL_SOCIAL_PROVIDERS.length);

    const declared = Object.keys(PROVIDER_EMAIL_VERIFICATION_IS_SOUND);
    expect([...declared].sort(), 'a provider is missing from, or invented in, the soundness table')
      .toEqual([...ALL_SOCIAL_PROVIDERS].sort());
    for (const p of ALL_SOCIAL_PROVIDERS) {
      expect(typeof PROVIDER_EMAIL_VERIFICATION_IS_SOUND[p], `${p} must be classified true or false`).toBe('boolean');
    }
  });

  it("a change to any provider's emailVerified derivation invalidates its classification", async () => {
    // WHY THIS SHAPE, and not the obvious one: a guard asserting "a SOUND
    // provider's file contains no literal `emailVerified = true`" MISCLASSIFIES
    // FACEBOOK, whose defect is `Boolean(profile.email)` — not a literal. That
    // guard would have passed the clearest unsound case. Soundness is a human
    // judgement per provider and no test can make it; what a test CAN do is
    // refuse to let the judgement outlive the code it was made about.
    const dir = path.resolve(__dirname, '../providers/social');
    // sha256(the file's emailVerified lines, whitespace-normalised).slice(0,8),
    // measured at `48641bda3`. github carries FOUR such lines because its
    // derivation spans two branches — which is exactly why it is classified
    // unsound, and exactly what this fingerprint is watching.
    const FINGERPRINTS: Record<string, string> = {
      'google.ts': '68209c5d',
      'apple.ts': 'aba7fd61',
      'linkedin.ts': '6a4e48aa',
      'github.ts': '7a81798f',
      'facebook.ts': 'efb8faaf',
      'microsoft-personal.ts': '62f11848',
    };

    const actual: Record<string, string> = {};
    for (const file of Object.keys(FINGERPRINTS)) {
      const src = fs.readFileSync(path.join(dir, file), 'utf8');
      const lines = src
        .split('\n')
        .filter((l) => l.includes('emailVerified'))
        .map((l) => l.trim().replace(/\s+/g, ' '));

      // CONTROL: a file whose derivation we could not find would fingerprint the
      // empty string and match nothing — or worse, match another empty one.
      expect(lines.length, `${file}: no emailVerified assignment found — has the adapter moved?`).toBeGreaterThan(0);

      actual[file] = crypto.createHash('sha256').update(lines.join('\n')).digest('hex').slice(0, 8);
    }

    expect(
      actual,
      'A provider\'s emailVerified derivation changed. Re-read it and re-decide its entry in ' +
        'PROVIDER_EMAIL_VERIFICATION_IS_SOUND, then update the fingerprint here in the same commit.',
    ).toEqual(FINGERPRINTS);
  });
});


// ===========================================================================
// KS-795 part (a) — THE ACCOUNT GATE ON THE CALLBACK
//
// Part (b), above, stops an UNSOUND email claim attaching a social identity to
// someone else's account. It never asks the other question: may THIS account
// receive a credential at all? The callback reaches `createSession` +
// `generateTokenPair` by three routes — an existing social id, an email link,
// and a freshly created row — and all three fell straight through. So an
// account an admin had SUSPENDED, already carrying a social identity, minted a
// full token pair on every callback: no linking step, no second factor.
//
// The gate is placed at the MINT, not on the link branch the commission named,
// because a gate on one of three branches is one an attacker walks around by
// already being linked. `alreadyLinked` below is that case.
// ===========================================================================

describe('KS-795 part (a): the callback gates the ACCOUNT, not just the linking', () => {
  it('CONTROL — an ACTIVE account still mints (or every refusal below proves nothing)', async () => {
    state.alreadyLinked = true;
    const res = await callback('google');
    expect(res.status).toBe(200);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
  });

  // ⚠ WAS "SUSPENDED and DEACTIVATED only". That omission is now CLOSED.
  //
  // On the pre-#819 parent `accountStatusForbidsCredential` was a DENY-list
  // naming exactly those two, so PENDING and INVITED passed the gate and minted
  // — measured, not assumed: asserting them here failed with "expected 200 not
  // to be 200", which is why they were deferred rather than dropped. PR #819
  // (KS-796 Q1) inverted the predicate: `STATUSES_MAY_RECEIVE_CREDENTIAL` is
  // `Object.freeze(['ACTIVE'])` (`src/types/index.ts:169`) against a five-value
  // vocabulary, so every status but ACTIVE is refused by default. This branch is
  // rebased onto that, so the two cases arrive below — the interaction between
  // the two PRs is now asserted rather than described in a comment.
  it.each(['SUSPENDED', 'DEACTIVATED'])(
    'a %s account ALREADY LINKED is refused — the case needing no link and no second factor',
    async (status) => {
      state.alreadyLinked = true;
      state.accountStatus = status;
      const res = await callback('google');
      expect(res.status).not.toBe(200);
      expect(res.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
      expect(res.body).not.toContain('MINTED_SOCIAL_REFRESH');
    },
  );

  /**
   * KS-796 Q1 x KS-795 — the two statuses the old deny-list let through, on BOTH
   * arrival routes, because door 2 resolves an account two different ways and a
   * gate on one is a gate an attacker walks around by taking the other.
   *
   * The assertion is deliberately NOT `.not.toBe(200)` alone. That is satisfied
   * by a 500, so a handler that crashed on an unrecognised status would read as
   * a refusal. It asserts the refusal the product actually specifies -- 403 from
   * `ForbiddenError('Account may not sign in')` -- AND that no credential was
   * minted AND that no social identity was attached on the way past.
   */
  it.each(['PENDING', 'INVITED'])(
    'a %s account is refused on BOTH arrival routes — the statuses the deny-list let mint',
    async (status) => {
      // Route 1 — ALREADY LINKED: no link write and no second factor needed.
      state.alreadyLinked = true;
      state.emailAccountExists = true;
      state.accountStatus = status;
      const linked = await callback('google');
      expect(linked.status).toBe(403);
      expect(linked.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
      expect(linked.body).not.toContain('MINTED_SOCIAL_REFRESH');
      expect(socialIdWrites()).toHaveLength(0);

      // Route 2 — reached by the EMAIL-LINK branch, which is where the account
      // is resolved by address rather than by an identity it already carries.
      linkWrites.length = 0;
      state.alreadyLinked = false;
      state.emailAccountExists = true;
      state.accountStatus = status;
      const emailLinked = await callback('google');
      expect(emailLinked.status).toBe(403);
      expect(emailLinked.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
      expect(emailLinked.body).not.toContain('MINTED_SOCIAL_REFRESH');
    },
  );

  it('a SUSPENDED account reached by the EMAIL-LINK branch is refused too', async () => {
    state.alreadyLinked = false;
    state.emailAccountExists = true;
    state.accountStatus = 'SUSPENDED';
    const res = await callback('google');
    expect(res.status).not.toBe(200);
    expect(res.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
  });

  it('an MFA account gets 403 MFA_REQUIRED and no credential — the callback cannot carry a factor', async () => {
    state.alreadyLinked = true;
    state.accountMfaEnabled = true;
    const res = await callback('google');
    expect(res.status).toBe(403);
    expect(res.body).toContain('MFA_REQUIRED');
    expect(res.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
  });

  it('BOUND — a NEW signup is unaffected: it is created ACTIVE and still mints', async () => {
    state.alreadyLinked = false;
    state.emailAccountExists = false;
    const res = await callback('google');
    expect(res.status).toBe(200);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
  });
});

// =============================================================================
// KS-795 F-4 — AN EMPTY PROVIDER EMAIL IS NEVER A KEY
//
// apple returns `email` only on the first authorization and github yields '' when
// there is neither a public nor a verified address, so this is reachable rather
// than hypothetical. Unfixed, two DIFFERENT provider ids carrying empty emails
// both fall through to CREATE; the statement's
// `ON CONFLICT (email_lookup_hash) DO UPDATE` collapses them onto ONE row while
// `createUser` returns its input object either way, so the second caller is
// minted a session and a token pair for a user id that was never inserted --
// and `user_sessions` has no foreign key to `users`, so it is written, not
// refused.
//
// The CONTROL is load-bearing: if a profile WITH an email stopped creating and
// minting, every refusal below would pass for the wrong reason.
// =============================================================================
describe('KS-795 F-4: an empty provider email is never a link key or a create key', () => {
  it('CONTROL — a profile WITH an email still creates a new account and mints', async () => {
    state.alreadyLinked = false;
    state.emailAccountExists = false;
    const res = await callback('apple');
    expect(res.status).toBe(200);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(createdUsers).toHaveLength(1);
  });

  it('refuses terminally when the provider supplies no email and nothing matched by identity', async () => {
    state.alreadyLinked = false;
    state.emailAccountExists = false;
    state.profileEmail = '';
    const res = await callback('apple');
    expect(res.status).toBe(403);
    expect(res.body).toContain('SOCIAL_EMAIL_UNAVAILABLE');
    expect(res.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(createdUsers).toHaveLength(0);
  });

  /**
   * S130-F1 — PARAMETERISED OVER WHAT THE REPOSITORY ACTUALLY KEYS ON.
   *
   * This case used to pass only `''`. The guard it exercises is `!profile.email`,
   * which is falsy for `''` — and TRUE for every whitespace-only address. The
   * repository does not agree: `getUserByEmail`, `getUserByEmailLookup` and
   * `createUser` all normalise with `.toLowerCase().trim()`, so `' '`, `'\t\t'`
   * and `'  \n '` every one key on the SAME `email_lookup_hash` as a literal
   * empty address.
   *
   * So two distinct provider identities carrying different whitespace collapsed
   * onto one row through `ON CONFLICT (email_lookup_hash) DO UPDATE` and minted
   * two token pairs — the exact collision F-4 exists to foreclose, reached by
   * walking around the guard rather than through it.
   *
   * Measured against the UNFIXED product before the fix was written: `''`
   * refused, and the other three each created a row and minted twice.
   *
   * Latent today — it needs a provider that emits a whitespace address and none
   * is configured — which is why it is Major-latent rather than live. Latent is
   * when it is cheap.
   */
  it.each([
    ['a literal empty string', ''],
    ['a single space', ' '],
    ['tabs', '\t\t'],
    ['mixed whitespace and a newline', '  \n '],
  ])('two DIFFERENT identities with %s for an email cannot merge — zero rows, zero credentials', async (_label, email) => {
    state.alreadyLinked = false;
    state.emailAccountExists = false;
    state.profileEmail = email;

    state.providerId = 'apple-identity-A';
    const first = await callback('apple');
    state.providerId = 'apple-identity-B';
    const second = await callback('apple');

    expect(first.status, 'the first identity must be refused').toBe(403);
    expect(second.status, 'and so must the second').toBe(403);
    expect(first.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(second.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    // The merge is not merely avoided -- no row exists for either identity to
    // collapse onto. Unfixed, this is 2 for every value the repository trims
    // to empty.
    expect(createdUsers).toHaveLength(0);
  });

  it('BOUND — an account resolved BY ITS SOCIAL ID is unaffected by an empty email', async () => {
    state.alreadyLinked = true;
    state.profileEmail = '';
    const res = await callback('apple');
    expect(res.status).toBe(200);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
  });
});

// =============================================================================
// KS-795 F-5 — A REFUSED CALLBACK MUTATES NOTHING
//
// Two writes used to precede the gate: the identity link, and the BASIC ->
// SOCIAL verification-level upgrade. So a callback the platform had just
// REFUSED still changed the account it refused.
//
// The link write is the one that matters, and its danger is latent rather than
// current: `updateUser` drops social-id fields today, so nothing is persisted.
// The moment that is repaired, a pre-gate link write attaches an ATTACKER's
// provider identity to a SUSPENDED victim -- the refusal holds for that one
// request and hands over a permanent key.
//
// The CONTROL is load-bearing in the strict sense: on the already-linked path a
// successful callback writes NOTHING either (the stub returns verificationLevel
// SOCIAL and there is no link to make), so a "zero writes" assertion there would
// pass on the broken product too. It therefore uses the EMAIL-LINK branch, the
// one path where success is expected to write.
// =============================================================================
describe('KS-795 F-5: the gate precedes both writes', () => {
  it('CONTROL — an ACTIVE account through the EMAIL-LINK branch DOES write', async () => {
    state.alreadyLinked = false;
    state.emailAccountExists = true;
    state.accountStatus = 'ACTIVE';
    const res = await callback('google');
    expect(res.status).toBe(200);
    expect(socialIdWrites()).toHaveLength(1);
    expect(linkWrites.length).toBeGreaterThan(0);
  });

  it.each(['SUSPENDED', 'DEACTIVATED', 'PENDING', 'INVITED'])(
    'a %s account refused on the EMAIL-LINK branch mutates NOTHING',
    async (status) => {
      state.alreadyLinked = false;
      state.emailAccountExists = true;
      state.accountStatus = status;
      const res = await callback('google');
      expect(res.status).toBe(403);
      expect(socialIdWrites()).toHaveLength(0);
      expect(linkWrites).toHaveLength(0);
    },
  );

  it('an MFA account refused at the gate mutates nothing either', async () => {
    state.alreadyLinked = false;
    state.emailAccountExists = true;
    state.accountMfaEnabled = true;
    const res = await callback('google');
    expect(res.status).toBe(403);
    expect(res.body).toContain('MFA_REQUIRED');
    expect(linkWrites).toHaveLength(0);
  });
});

// =============================================================================
// KS-795 F-6 — DOOR 2 STOPS TELLING AN UNAUTHENTICATED CALLER THE ACCOUNT STATE
//
// `passwordLoginGate.ts` states the platform's own rule: locked out, suspended,
// deactivated, SSO-only, unknown email and wrong password all return the SAME
// refusal, because differentiating them leaks account existence and state.
// Door 1 obeys it. Door 2 returned ACCOUNT_LINK_REQUIRED ("An account already
// exists for this email address") for one refusal and FORBIDDEN "Account may
// not sign in" for another, so a caller could separate a healthy account from a
// disabled one.
//
// MFA_REQUIRED is deliberately still distinct: door 1 differentiates it too, so
// that is a documented difference rather than drift.
// =============================================================================
describe('KS-795 F-6: the two state-revealing refusals collapse to one shape', () => {
  it('the unsound-provider refusal and the disabled-account refusal are INDISTINGUISHABLE', async () => {
    // An UNSOUND provider against a perfectly healthy account.
    state.alreadyLinked = false;
    state.emailAccountExists = true;
    state.accountStatus = 'ACTIVE';
    const unsoundProvider = await callback('facebook');

    // A SOUND provider against a disabled account.
    state.alreadyLinked = false;
    state.emailAccountExists = true;
    state.accountStatus = 'SUSPENDED';
    const disabledAccount = await callback('google');

    expect(unsoundProvider.status).toBe(disabledAccount.status);
    expect(unsoundProvider.body).toBe(disabledAccount.body);
    expect(unsoundProvider.body).toContain('SOCIAL_SIGN_IN_REFUSED');
    // The two specific leaks that used to be there.
    expect(unsoundProvider.body).not.toContain('ACCOUNT_LINK_REQUIRED');
    expect(unsoundProvider.body).not.toContain('already exists');
  });

  it('MFA_REQUIRED stays distinct — door 1 differentiates it too', async () => {
    state.alreadyLinked = true;
    state.accountMfaEnabled = true;
    const res = await callback('google');
    expect(res.body).toContain('MFA_REQUIRED');
    expect(res.body).not.toContain('SOCIAL_SIGN_IN_REFUSED');
  });

  it('the refusal names no route, because the remedy it used to name does nothing', async () => {
    state.alreadyLinked = false;
    state.emailAccountExists = true;
    state.accountStatus = 'ACTIVE';
    const res = await callback('facebook');
    expect(res.body).not.toContain('/api/auth/social/link');
    expect(res.body).not.toContain('account settings');
  });
});

// ---- KS-806 (#1476 delta gate, Minor-C): social sign-up is a create path that took any provider email -------------------
// wallet.local is the synthetic domain of wallet accounts. No provider can have verified an address in it, so a profile
// carrying one is refused (the uniform SOCIAL_SIGN_IN_REFUSED) before it can link to an existing account or create a row.
describe('KS-806 - the social callback refuses a profile in the reserved wallet.local domain', () => {
  it.each(['w-0123456789abcdef0123456789abcdef01234567@wallet.local', 'W-ABC@WALLET.LOCAL'])(
    'RED KS-806 - a verified provider email %s creates nothing and mints nothing',
    async (email) => {
      state.profileEmail = email;
      state.profileEmailVerified = true;
      state.emailAccountExists = false;
      const res = await callback('google');
      expect(res.body).toContain('SOCIAL_SIGN_IN_REFUSED');
      expect(res.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
      expect(createdUsers, 'no account may be created from a wallet.local address').toEqual([]);
      expect(socialIdWrites()).toEqual([]);
    },
  );

  // Delta gate Minor-1: the guard must run BEFORE the email-match link step, not only before the create. A wallet account
  // already carries the synthetic address; a provider profile claiming it (verified, from a sound provider) would
  // otherwise reach the link branch and attach a social identity to the wallet account. Moving the guard into the create
  // block must turn this cell red (it links and mints), which is what pins its position.
  it('RED KS-806 - a profile in wallet.local that MATCHES AN EXISTING ACCOUNT is refused before the link step: nothing is linked and nothing is minted', async () => {
    const walletEmail = 'w-0123456789abcdef0123456789abcdef01234567@wallet.local';
    state.profileEmail = walletEmail;
    state.profileEmailVerified = true;
    state.emailAccountExists = true;
    state.existingEmail = walletEmail;
    const res = await callback('google');
    expect(res.body).toContain('SOCIAL_SIGN_IN_REFUSED');
    expect(res.body).not.toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(socialIdWrites(), 'the social identity must not be attached to the wallet account').toEqual([]);
    expect(createdUsers).toEqual([]);
  });

  it('CONTROL KS-806 - the same shape with an ORDINARY address links as before (the harness can express a link)', async () => {
    state.profileEmail = 'linkable-806@example.com';
    state.profileEmailVerified = true;
    state.emailAccountExists = true;
    state.existingEmail = 'linkable-806@example.com';
    const res = await callback('google');
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(socialIdWrites().length, 'a verified, sound-provider email match links the identity').toBeGreaterThan(0);
  });

  it('CONTROL KS-806 - an ordinary new address still signs up (a row is created and a token pair is minted)', async () => {
    state.profileEmail = 'newcomer-806@example.com';
    state.profileEmailVerified = true;
    state.emailAccountExists = false;
    const res = await callback('google');
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
    expect(createdUsers).toHaveLength(1);
  });

  it('CONTROL KS-806 - a look-alike domain still signs up', async () => {
    state.profileEmail = 'newcomer-806@notwallet.local';
    state.profileEmailVerified = true;
    state.emailAccountExists = false;
    const res = await callback('google');
    expect(createdUsers).toHaveLength(1);
    expect(res.body).toContain('MINTED_SOCIAL_ACCESS_TOKEN');
  });
});
