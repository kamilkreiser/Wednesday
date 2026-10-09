/**
 * KS-1305 - a fresh worktree has `@prisma/client` installed but the GENERATED
 * client (`node_modules/.prisma/client`) absent: `npm ci` runs with
 * ignore-scripts, so `prisma generate` never ran. The bare
 * `require('@prisma/client')` in `getPrismaClient()` (src/db.ts) then throws
 * `Cannot find module '.prisma/client/default'` - a module error that reads
 * like a product defect. The fix rethrows that one error as a sentence naming
 * the cause and the working command; every other load error is unchanged.
 *
 * Harness: the KS-458 suite's (`@prisma/client` replaced by a jest.mock
 * factory, single-tenant branch of `withTenant`). No database, no generate.
 */

process.env.DATABASE_URL = 'postgresql://user:pass@localhost:5432/db';
delete process.env.MULTI_TENANCY_ENABLED;

/** The error the next `require('@prisma/client')` throws; null = load the fake client. */
let mockLoadError: (Error & { code?: string }) | null = null;
let mockCallbackRan = false;

jest.mock('@prisma/client', () => {
  if (mockLoadError) throw mockLoadError;
  return {
    PrismaClient: class {
      async $executeRawUnsafe() {
        return 1;
      }
      async $transaction(fn: (tx: any) => Promise<any>) {
        return fn(this);
      }
      async $disconnect() {}
    },
  };
});

import { withTenant } from '../db';

/**
 * The error jest's resolver raises when the generated client is absent.
 *
 * @param {string} message - The module error's message.
 * @returns {Error & { code?: string }} An error carrying code MODULE_NOT_FOUND.
 */
function moduleNotFound(message: string): Error & { code?: string } {
  const err: Error & { code?: string } = new Error(message);
  err.code = 'MODULE_NOT_FOUND';
  return err;
}

describe('KS-1305: a missing generated Prisma client is diagnosed, not reported as a module error', () => {
  beforeEach(() => {
    mockCallbackRan = false;
  });

  it('RED KS-1305 D1: the missing .prisma/client names the cause and the generate command', async () => {
    mockLoadError = moduleNotFound(
      "Cannot find module '.prisma/client/default' from 'node_modules/@prisma/client/default.js'",
    );

    const run = withTenant('t-1305', async () => {
      mockCallbackRan = true;
      return 'never';
    });

    await expect(run).rejects.toThrow('the generated Prisma client (node_modules/.prisma/client) is missing');
    await expect(run).rejects.toThrow('cp -R ../../prisma ./prisma && npx prisma generate');
    expect(mockCallbackRan).toBe(false);
  });

  it('CONTROL KS-1305 C1: any other load error is rethrown unchanged (the same object)', async () => {
    const other = moduleNotFound("Cannot find module '@prisma/client' from 'src/db.ts'");
    mockLoadError = other;

    let caught: unknown = null;
    try {
      await withTenant('t-1305', async () => 'never');
    } catch (err) {
      caught = err;
    }

    expect(caught).toBe(other);
  });

  // KS-1305: C3 pins the FIRST term of the guard's conjunction. Added by Seat R 1st, not by the
  // Spark payload: the shipped cells left `err?.code === 'MODULE_NOT_FOUND'` uncovered, because D1
  // supplies a matching code AND a matching message while C1 supplies a matching code and a
  // NON-matching message ('@prisma/client', an at-sign, not a dot). So no cell presented an error
  // whose MESSAGE matches while its CODE does not, and deleting the code test reddened nothing.
  it('CONTROL KS-1305 C3: a .prisma/client message with a different code is rethrown unchanged', async () => {
    // KS-1305: same message shape as D1 so only the CODE differs -- that is the term under test.
    const other: Error & { code?: string } = new Error(
      "Cannot find module '.prisma/client/default' from 'node_modules/@prisma/client/default.js'",
    );
    other.code = 'ERR_MODULE_RESOLUTION_FAILED';
    mockLoadError = other;

    let caught: unknown = null;
    try {
      await withTenant('t-1305', async () => 'never');
    } catch (err) {
      caught = err;
    }

    // KS-1305: the SAME object, so the guard did not rewrite it into the KS-1305 sentence.
    expect(caught).toBe(other);
  });

  it('CONTROL KS-1305 C2: with the client generated, withTenant runs its callback as before', async () => {
    mockLoadError = null;

    const result = await withTenant('t-1305', async () => {
      mockCallbackRan = true;
      return 'ran';
    });

    expect(result).toBe('ran');
    expect(mockCallbackRan).toBe(true);
  });
});
