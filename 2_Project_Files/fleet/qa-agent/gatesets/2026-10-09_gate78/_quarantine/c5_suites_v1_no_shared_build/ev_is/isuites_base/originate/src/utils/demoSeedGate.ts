/**
 * =============================================================================
 * DEMO-SEED GATE (KS-487 B-3)
 * =============================================================================
 * Whether `POST /api/admin/seed-demo-users` may run in this process.
 *
 * Lives in its own module so it can be unit-tested without importing
 * `routes/adminConfig.ts`, which pulls in `config.ts` and throws at module load
 * unless DATABASE_URL/JWT_SECRET are set. The route-level suite for that file is
 * a DB-gated integration test (`rightsHolders.tenant-scope.integration.test.ts`,
 * run via `npm run test:integration`), and a security gate should not be
 * reachable only by the heavier suite.
 *
 * ---------------------------------------------------------------------------
 * WHY BOTH FLAGS, AND WHY NO `isDevLike` BYPASS
 * ---------------------------------------------------------------------------
 * `auth` established this pattern in pen-test F-05
 * (`services/auth/src/repositories/userRepo.ts:966-985`): seeding requires
 * `ALLOW_DEFAULT_SEED_PASSWORDS=true`, and non-dev environments additionally
 * require `ENABLE_DEMO_SEED=true`. F-05's finding was that gating on
 * `NODE_ENV !== 'production'` was unsafe because the demo ran as
 * `NODE_ENV=demo` and therefore got the seed.
 *
 * This gate is deliberately stricter: **both** flags, always, with no
 * environment-shaped exemption. The difference is the threat model —
 * auth's seeder runs once at boot under operator control, whereas this is an
 * HTTP endpoint any authenticated ORG_ADMIN can call repeatedly. "The process
 * looks like dev" is not a property an attacker-triggerable route should trust.
 *
 * That is not hypothetical here. The demo VM runs the same `docker-compose.yml`
 * as local, in which originate is configured `NODE_ENV=development` — so an
 * `isDevLike` bypass would leave this route open on the live demo. F-05's lesson
 * in a new costume.
 *
 * Neither flag is set for originate in any deploy config (`services.bicep` sets
 * both, but only on the `auth` container), so the endpoint refuses everywhere by
 * default — including locally, where a developer opts in via `.env`.
 */

/** Env keys read by {@link isDemoSeedEnabled}. Exported for tests and docs. */
export const DEMO_SEED_FLAGS = ['ALLOW_DEFAULT_SEED_PASSWORDS', 'ENABLE_DEMO_SEED'] as const;

/**
 * True only when BOTH demo-seed flags are exactly `'true'`.
 *
 * Compared against the literal string rather than coerced: `'false'`, `'0'` and
 * `'no'` are all truthy strings, and a gate that opens on `ALLOW_..=false` would
 * be worse than no gate because it would read as configured-and-closed.
 *
 * @param env Environment to read. Defaults to `process.env`; injectable so tests
 *   need not mutate global state.
 * @returns `true` if demo-user seeding is permitted in this process.
 * @example
 *   if (!isDemoSeedEnabled()) return res.status(403).json({ ... });
 */
export function isDemoSeedEnabled(env: NodeJS.ProcessEnv = process.env): boolean {
  return DEMO_SEED_FLAGS.every((flag) => env[flag] === 'true');
}
