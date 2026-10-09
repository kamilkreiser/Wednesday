/**
 * KS-487 B-3 — the demo-seed gate on POST /api/admin/seed-demo-users.
 *
 * That route seeded 14 accounts across every tenant with the bcrypt of
 * `admin123` (published in the source), under `runWithPlatformScope`, with
 * `ON CONFLICT (email) DO UPDATE SET password_hash = ..., role = ...` and no
 * environment gate at all. Any authenticated ORG_ADMIN of any tenant could
 * therefore reset the password and role of an account in another tenant to a
 * value printed in this repository, then sign in as it.
 *
 * These tests pin the gate half. `isDemoSeedEnabled` takes an injected env so
 * the whole truth table is exercised without mutating global state and without
 * importing `routes/adminConfig.ts` (which loads `config.ts` and throws unless
 * DATABASE_URL/JWT_SECRET are set — the reason its route suite is a DB-gated
 * integration test).
 *
 * The default-deny cases are the point: every one of them is an environment in
 * which the endpoint used to run.
 */

import { isDemoSeedEnabled, DEMO_SEED_FLAGS } from '../utils/demoSeedGate';

const ON = { ALLOW_DEFAULT_SEED_PASSWORDS: 'true', ENABLE_DEMO_SEED: 'true' };

describe('KS-487 B-3 — demo-seed gate', () => {
  it('opens only when BOTH flags are exactly "true"', () => {
    expect(isDemoSeedEnabled({ ...ON })).toBe(true);
  });

  it('is closed when the environment is empty (the default everywhere)', () => {
    // Neither flag is set for originate in docker-compose.yml or services.bicep,
    // so this is the real state on local, the demo VM and any future deploy.
    expect(isDemoSeedEnabled({})).toBe(false);
  });

  it.each([
    ['only ALLOW_DEFAULT_SEED_PASSWORDS', { ALLOW_DEFAULT_SEED_PASSWORDS: 'true' }],
    ['only ENABLE_DEMO_SEED', { ENABLE_DEMO_SEED: 'true' }],
  ])('is closed with %s — one flag is not enough', (_label, env) => {
    expect(isDemoSeedEnabled(env)).toBe(false);
  });

  // A gate that opens on the string 'false' is worse than no gate: it reads as
  // configured-and-closed while being open. Every value below is truthy in JS.
  it.each(['false', 'FALSE', '0', 'no', 'off', 'null', 'undefined', ' true', 'true ', 'True', 'TRUE'])(
    'is closed when a flag is the truthy-but-not-"true" string %p',
    (value) => {
      expect(isDemoSeedEnabled({ ...ON, ENABLE_DEMO_SEED: value })).toBe(false);
      expect(isDemoSeedEnabled({ ...ON, ALLOW_DEFAULT_SEED_PASSWORDS: value })).toBe(false);
    },
  );

  // F-05's actual finding: the demo ran as NODE_ENV=demo and got the seed
  // anyway. This gate must not consult NODE_ENV at all — and the demo VM runs
  // the same compose file as local, where originate is NODE_ENV=development, so
  // an isDevLike bypass would leave the route open on the live demo.
  it.each(['development', 'dev', 'test', 'demo', 'staging', 'production', undefined])(
    'ignores NODE_ENV=%s entirely — no environment-shaped bypass',
    (nodeEnv) => {
      expect(isDemoSeedEnabled({ NODE_ENV: nodeEnv })).toBe(false);
      expect(isDemoSeedEnabled({ ...ON, NODE_ENV: nodeEnv })).toBe(true);
    },
  );

  it('requires exactly the two documented flags', () => {
    expect([...DEMO_SEED_FLAGS].sort()).toEqual(
      ['ALLOW_DEFAULT_SEED_PASSWORDS', 'ENABLE_DEMO_SEED'].sort(),
    );
    // An unrelated flag must not open it — guards against a future rename
    // leaving the check reading a key nothing sets.
    expect(isDemoSeedEnabled({ ENABLE_DEMO_SEEDING: 'true', ALLOW_SEED: 'true' })).toBe(false);
  });

  it('does not read the ambient process.env when an env is injected', () => {
    const saved = { ...process.env };
    try {
      process.env.ALLOW_DEFAULT_SEED_PASSWORDS = 'true';
      process.env.ENABLE_DEMO_SEED = 'true';
      // Injected env wins: the ambient one is fully open, this must still close.
      expect(isDemoSeedEnabled({})).toBe(false);
    } finally {
      process.env = saved;
    }
  });
});
