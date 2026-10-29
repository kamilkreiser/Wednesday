# KS-1802 (Spark operator 8, 2026-10-29): adminConfig.ts:2112 inner catch reads err?.message unguarded. code_patch, build: GEN_TIP=e4cd2e13... python3 -I spark/gen/mk2.py <this>
P='Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts'
E1=("    return err?.message?.includes('does not exist') === true || err?.code === '42P01';\n  } catch {\n    return false;\n  }\n}\n",
    "    return err?.message?.includes('does not exist') === true || err?.code === '42P01';\n  } catch {\n    return false;\n  }\n}\n\n"
    "/** KS-1802: the thrown value's message for a log line; the fixed fallback when the value cannot be read (a revoked Proxy, a `message` getter that throws). */\n"
    "function readableErrorMessage(err: any): string | undefined {\n  try {\n    return err?.message;\n  } catch {\n    return 'thrown value that could not be described';\n  }\n}\n")
E2=("        logger.error('Demo user seed failed', { email: u.email, error: err?.message });\n",
    "        logger.error('Demo user seed failed', { email: u.email, error: readableErrorMessage(err) });\n")
TEST='''// KS-1802 (originate routes/adminConfig.ts, POST /seed-demo-users): the per-user catch counted the failure (failed++) and THEN logged `err?.message`. That read touches the thrown value, so a
// revoked Proxy, or an object whose `message` getter throws, made the read throw from inside the catch: the loop stopped at the first such user, the rest of the seed was never attempted, and the
// route answered the constant 500 instead of its normal report. The fix reads the message through a guarded helper. The database is mocked (the same mocks as the KS-1780 cells); both seed flags
// are set, the route is driven over a real loopback listener, and every insert is made to reject with the hostile value.
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
process.env.ALLOW_DEFAULT_SEED_PASSWORDS = 'true';
process.env.ENABLE_DEMO_SEED = 'true';

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
const mockLogError = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
  refreshTenantConfigs: jest.fn(),
  withTenant: (_t: unknown, fn: (tx: unknown) => unknown) => fn({ $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw }),
  getTenantManager: () => null,
}));

jest.mock('../middleware/auth', () => {
  const actual = jest.requireActual('../middleware/auth');
  return {
    ...actual,
    authenticate: () => (req: any, _res: unknown, next: () => void) => {
      const principal = { id: 'u-ks1802', role: 'SYSTEM_ADMIN', tenantId: 't-ks1802' };
      req._secuuraUser = principal; req.user = principal; req.tenantId = principal.tenantId;
      next();
    },
    requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  };
});

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
    runWithPlatformScope: (fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLogError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { adminConfigRouter } from '../routes/adminConfig';

const USERS = 14;
const app = express();
app.use('/api/admin', express.json(), adminConfigRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  (server as unknown as { closeAllConnections?: () => void })?.closeAllConnections?.();
  server?.close();
});
beforeEach(() => {
  mockQueryRaw.mockReset();
  mockExecuteRaw.mockReset();
  mockLogError.mockReset();
  mockQueryRaw.mockResolvedValue([]);
});

async function seed(): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
  try {
    const res = await fetch(baseUrl + '/api/admin/seed-demo-users', { method: 'POST', signal: AbortSignal.timeout(3000) });
    return { status: res.status, body: await res.json() };
  } catch {
    return { status: 'NO ANSWER', body: null };
  }
}

function revokedProxy(): object {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
}

function throwingMessageGetter(): object {
  return {
    get message(): string {
      throw new Error('ks1802 getter');
    },
  };
}

describe('KS-1802: seed-demo-users keeps going when a user insert throws a hostile value', () => {
  it('RED KS-1802 R1: every insert rejecting with a revoked Proxy is reported as 14 failed, not as the constant 500', async () => {
    mockExecuteRaw.mockRejectedValue(revokedProxy());
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
  });

  it('RED KS-1802 R2: every insert rejecting with a throwing message getter is reported as 14 failed, not as the constant 500', async () => {
    mockExecuteRaw.mockRejectedValue(throwingMessageGetter());
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
  });

  it('RED KS-1802 R3: one hostile failure on the first user does not stop the other 13 from being seeded', async () => {
    mockExecuteRaw.mockRejectedValueOnce(revokedProxy()).mockResolvedValue(1);
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 13, created: 13, alreadyPresent: 0, failed: 1 } });
  });

  it('control KS-1802 C1: an ordinary Error on every insert is reported as 14 failed and its message is logged', async () => {
    mockExecuteRaw.mockRejectedValue(new Error('ks1802 ordinary'));
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
    expect(mockLogError).toHaveBeenCalledWith('Demo user seed failed', { email: 'james.wilson@ox.ac.uk', error: 'ks1802 ordinary' });
  });

  it('control KS-1802 C2: every insert creating a row is reported as 14 created', async () => {
    mockExecuteRaw.mockResolvedValue(1);
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: USERS, created: USERS, alreadyPresent: 0, failed: 0 } });
  });

  it('control KS-1802 C3: every insert hitting a conflict is reported as 14 already present', async () => {
    mockExecuteRaw.mockResolvedValue(0);
    expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: USERS, failed: 0 } });
  });
});
'''
S=dict(dir='ks_1802_p1',ticket='KS-1802',
 title='originate POST /api/admin/seed-demo-users: the per-user catch reads err?.message unguarded, so a hostile thrown value stops the seed and turns the report into the constant 500 (RUNG 2, code_patch: two hunks in one product + one NEW jest file)',
 intro="DRAFT by Spark operator 8 for Wednesday, 2026-10-29 AEDT. Secuura (Platform K / originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: filed by Seat R 8th as 1802-3 from the gate 13 review of PR 1802 (develop `e4cd2e1325ba`); severity Low; related KS-1780 and KS-1772. The route is demo-only (both seed flags required, refuses everywhere by default).",
 products=[(P,[E1,E2])],
 prodnote=['product, modified in place: TWO hunks (a new 9-line insertion (blank line, doc comment, 7-line helper) after isMissingTableError :147, and the one log line at :2112)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, jest, given in full below; 6 cells (3 red, 3 control; database, auth, shared and logger modules mocked as in the KS-1780 cells)'],
 runner='jest` (`npx jest src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch', rung='2 (two hunks, nine inserted lines and one changed line byte-exact; the new test given whole)',
 pins='''# code_patch, 2 hunks in originate adminConfig.ts + a NEW jest file; ref = the KS-1780 sibling (same mocks and listener shape); line = the first changed line (the helper insertion).
tier=code_patch
ref=Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts
line=148
ctx=65536
''',
 wrong="In `POST /seed-demo-users` the loop over the 14 demo users wraps each insert in `try { ... } catch (err: any) { failed++; logger.error('Demo user seed failed', { email: u.email, error: err?.message }); }` (`adminConfig.ts:2107-2113`). `failed++` (:2111) runs first, but the next statement reads `err?.message` from the thrown value itself. If that value is a revoked Proxy, or an object whose `message` getter throws, the read throws from inside the catch, leaves the `for` loop, and is caught by the route's outer `catch` (:2143), which answers `fail500` (the constant 500): the users after the first hostile one are never attempted, and the operator gets no `created / alreadyPresent / failed` report. `fail500` (:110) and the KS-1780 helpers (:133, :141) already survive such values; this is the one catch in the file that still reads the value unguarded. The change: add a helper `readableErrorMessage(err)` that returns `err?.message` inside a `try` and a fixed fallback string in the `catch`, and log `readableErrorMessage(err)` instead of `err?.message`. Every value that could be read before logs the same text as before.",
 where="- `src/routes/adminConfig.ts:141-147` - (correct, STAYS) `function isMissingTableError(err: any): boolean {` ... closing `}` at :147. **Must change:** insert directly after that closing `}` (a blank line, then a doc comment line and a 7-line function `readableErrorMessage`), before the blank line and `adminConfigRouter.post('/refresh-tenants'` that follow it.\n- `src/routes/adminConfig.ts:2112` - **must change:** `        logger.error('Demo user seed failed', { email: u.email, error: err?.message });` becomes the same line with `error: readableErrorMessage(err)`.\n- `fail500`, `errorMessageIncludes`, `isMissingTableError`, the outer catch at :2143 and the Alice rights-holder block's bare `catch { /* skip */ }` at :2132 are NOT touched.",
 exactnote="Two hunks in one file, in file order.\n",
 donot="**Do NOT touch** any other line of `adminConfig.ts`, and no other file but the new test.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, jest globals (no import of `describe`/`it`/`expect`), no top-level await. It mocks `../db`, `../middleware/auth`, `@secuura/shared` (through the existing `./helpers/sharedModuleMock`) and `../utils/logger` exactly as the KS-1780 cells do, sets both seed flags before the import, and drives the route over a real loopback listener.",
 red=['RED KS-1802 R1','RED KS-1802 R2','RED KS-1802 R3'],
 cells="- RED `R1`/`R2`/`R3`: at the tip the route answers the constant 500 for a hostile value (the log read throws out of the loop), so the `toEqual({ status: 200, ... })` assertion fails; after the edit the loop finishes and the report is the 200 body (R1/R2: 14 failed; R3: 13 created, 1 failed).\n- CONTROL `C1`-`C3`: green at the tip AND after (an ordinary Error is counted failed and its message logged; all-created; all-conflict).",
 premises="- `adminConfig.ts:2107-2113` is the loop catch quoted above (`failed++` :2111, the log :2112), read at `e4cd2e1325ba`; the loop is inside the outer `try` that ends at :2143.\n- The gate at :2043 is `isDemoSeedEnabled()` (`utils/demoSeedGate.ts`), which reads `process.env` at call time and needs both flags equal to `'true'`.\n- `users` is a literal list of 14 entries (:2066-2083 area), the first is `james.wilson@ox.ac.uk`; the insert is `db.$executeRaw` under `runWithPlatformScope`; the response keys are `success, seededUsers, created, alreadyPresent, failed` (:2136-2142).\n- The Alice block (:2118-2132) calls `db.$queryRaw` for Oxford's org; the test makes it resolve `[]`, so `oxfordOrgId` is undefined and the block does nothing.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Not read: whether an existing test already drives POST /seed-demo-users end to end through this router with a different mock shape that this new file could collide with (ks730c and ks928 mention the route; they were not read in full).\n- The ranges `:2066-2083` (the users list) and `:2118-2132` (the Alice block) were read by eye, not quoted.\n- Open PRs touching adminConfig.ts: not listed here (see the report); the raising seat checks.",
 scope="**Closes KS-1802** (the one catch the ticket names). Link the PR as Refs KS-1802 until the QA gate has passed. Not KS-1801: that is test-only (`ks_1801_p1`, `ks_1801_p2`) and edits a different test file.",
)
