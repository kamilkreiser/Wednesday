P='Blockchain/Dev/services/auth/src/routes/auth.ts'
TP='Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts'
OLD='''setTimeout(() => {
  userRepo.seedDemoUsers(hashPassword).catch((err) =>
    logger.error('Failed to seed demo users', { error: err }),
  );
}, 2000);
'''
NEW='''// KS-1776: seedDemoUsers is started from a timer, outside any request. A synchronous throw from it (a repository mock that lacks the export, a repository that is not ready) never reached the
// .catch below, so it escaped the timer as an uncaught exception that the test runner pinned on whichever test was running. Both the throw and the rejection now go to the same log line.
const logSeedFailure = (err: unknown): void => {
  logger.error('Failed to seed demo users', { error: err });
};
setTimeout(() => {
  try {
    userRepo.seedDemoUsers(hashPassword).catch(logSeedFailure);
  } catch (err) {
    logSeedFailure(err);
  }
}, 2000);
'''
TEST='''// KS-1776 (services/auth routes/auth.ts): importing the routes module arms a module-scope `setTimeout(..., 2000)` that calls `userRepo.seedDemoUsers(hashPassword).catch(...)`. When the
// repository mock of a test has no `seedDemoUsers` export, vitest's mock THROWS on that property read, synchronously, inside the timer callback: the `.catch` is never reached and the
// error escapes as an uncaught exception that vitest pins on whichever test is running (seen once, in ks781-login-authorize-agree, in a loaded run). Here the timer is driven with FAKE
// timers so the escape is an assertion: D1 reads whether firing the timer throws, D2 reads whether the failure is logged instead. C1 and C2 pin what must not change.
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';

const silent = { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() };
vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));

const USER_REPO_BASE = {
  getUserById: vi.fn(async () => null),
  getUserByIdPreAuth: vi.fn(async () => null),
  getUserByEmail: vi.fn(async () => null),
  updateUser: vi.fn(async () => undefined),
  getPlatformAdmin: vi.fn(async () => null),
  updatePlatformAdminPassword: vi.fn(async () => undefined),
  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
  reencryptPlatformAdminMfaSecretIfLegacy: vi.fn(async () => undefined),
};

vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [], rowCount: 0 })) }));
vi.mock('../repositories/userRepo', () => ({ ...USER_REPO_BASE }));
vi.mock('../services/session', () => ({
  createSession: vi.fn(async () => ({ id: 'sess-new' })),
  getSession: vi.fn(async () => null),
  rotateSessionRefreshToken: vi.fn(async () => undefined),
  revokeSession: vi.fn(async () => undefined),
  getRedisClient: vi.fn(() => null),
  validateSession: vi.fn(async () => true),
  updateSessionActivity: vi.fn(async () => undefined),
}));
vi.mock('../services/refreshDenylist', () => ({
  isRefreshJtiDenylisted: vi.fn(async () => false),
  denylistRefreshJti: vi.fn(async () => undefined),
}));
vi.mock('../services/accountLockout', () => ({
  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => 1),
  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
}));
vi.mock('../services/password', () => ({
  verifyPassword: vi.fn(async () => false), hashPassword: vi.fn(async () => '$argon2id$stub'),
  checkPasswordStrength: vi.fn(() => ({ ok: true })), generateResetToken: vi.fn(() => 'tok'), shouldRehashAfterVerify: vi.fn(() => false),
}));
vi.mock('../services/email', () => ({ sendVerificationEmail: vi.fn(async () => undefined), sendPasswordResetEmail: vi.fn(async () => undefined) }));
vi.mock('../events', () => ({ publishEvent: vi.fn(async () => undefined), EventTypes: {} }));

function advance(ms: number): string {
  try {
    vi.advanceTimersByTime(ms);
    return 'ok';
  } catch (err) {
    return 'THREW ' + (err instanceof Error ? err.message : String(err));
  }
}

beforeAll(() => {
  vi.useFakeTimers();
});
afterAll(() => {
  vi.useRealTimers();
});

describe('KS-1776: the demo-user seed timer cannot escape as an uncaught throw', () => {
  it('RED KS-1776 D1 firing the seed timer does not throw when the repository has no seedDemoUsers', async () => {
    vi.resetModules();
    silent.error.mockClear();
    await import('../routes/auth');
    expect(advance(2500)).toBe('ok');
  });

  it('RED KS-1776 D2 the missing seedDemoUsers is logged as Failed to seed demo users instead', async () => {
    vi.resetModules();
    silent.error.mockClear();
    await import('../routes/auth');
    advance(2500);
    expect(silent.error.mock.calls.map((call) => call[0])).toEqual(['Failed to seed demo users']);
  });

  it('control KS-1776 C1 with seedDemoUsers present it is called once, with the password hasher, after 2000 ms and not before', async () => {
    vi.resetModules();
    const seed = vi.fn(async () => undefined);
    vi.doMock('../repositories/userRepo', () => ({ ...USER_REPO_BASE, seedDemoUsers: seed }));
    await import('../routes/auth');
    advance(1999);
    expect(seed).not.toHaveBeenCalled();
    advance(1);
    expect(seed).toHaveBeenCalledTimes(1);
    expect(typeof (seed.mock.calls[0] as unknown[])[0]).toBe('function');
  });

  it('control KS-1776 C2 a seedDemoUsers that rejects is logged as Failed to seed demo users', async () => {
    vi.resetModules();
    silent.error.mockClear();
    vi.doMock('../repositories/userRepo', () => ({ ...USER_REPO_BASE, seedDemoUsers: vi.fn(async () => { throw new Error('ks1776 rejection'); }) }));
    await import('../routes/auth');
    advance(2500);
    await Promise.resolve();
    await Promise.resolve();
    expect(silent.error.mock.calls.map((call) => call[0])).toEqual(['Failed to seed demo users']);
  });
});
'''
S=dict(dir='ks_1776_p1',ticket='KS-1776',
 title='services/auth routes/auth.ts:62: the module-scope 2 s seedDemoUsers timer escapes as an uncaught exception when the repository has no seedDemoUsers; start it inside a try and share one log line (RUNG 2-3, code_patch: one product hunk replacing 5 lines with 12 + one NEW fake-timer vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 2 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. The ticket is FACTS ONLY (no fix proposed, 'what, if anything, to do: not decided'). This brief chooses the smallest fix that touches no behaviour of the seed itself - a try around the call and one shared log line - and says so; the alternatives (an environment/test guard on the timer, `unref()`, moving the seed to startup) are NOT taken. The raise seat must confirm the shape with the ticket's owner. The Spark may fail this one (capability data: a fake-timer test with a full route-module mock set).",
 products=[(P,[(OLD,NEW)])],
 prodnote=['product, modified in place: ONE hunk, five lines replaced by twelve'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 4 cells'],
 runner='vitest` (`npx vitest run src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch', rung='2-3 (one hunk byte-exact; the new test is a fake-timer test with a 9-module mock set copied in shape from ks1151)',
 pins='''# code_patch, ONE hunk in routes/auth.ts + a NEW fake-timer vitest (test_file NOT pinned: it would mean MODIFY); ref = the ks1151 route-module spec (the mock set, shape only); line = the changed line at the tip.
tier=code_patch
ref=Blockchain/Dev/services/auth/src/__tests__/ks1151-auth-refresh-refuses-oauth-token.test.ts
line=62
ctx=65536
''',
 wrong="`routes/auth.ts:59-66` arms, at module import, `setTimeout(() => { userRepo.seedDemoUsers(hashPassword).catch((err) => logger.error('Failed to seed demo users', { error: err })); }, 2000);`. In a test file whose `../repositories/userRepo` mock has no `seedDemoUsers` export, vitest's mock throws SYNCHRONOUSLY on that property read, so the `.catch` is never reached and the error escapes the timer as an uncaught exception that vitest attributes to whichever test is running (seen once, in `ks781-login-authorize-agree.test.ts`, in a loaded run; 49 test files mock `../repositories/userRepo`, 11 of them import `routes/auth`). The change starts the seed inside a `try` whose `catch` and the existing `.catch` share ONE log function, so a synchronous throw and an async rejection both log `Failed to seed demo users` with the same fields. Nothing about when the timer fires, what it calls, or what a healthy repository does changes.",
 where="- `services/auth/src/routes/auth.ts:62-66` - **must change**: the five lines from `setTimeout(() => {` to `}, 2000);` (the call and its `.catch`) are replaced by the twelve lines under \"The exact change\": a two-line comment, the `logSeedFailure` function (3 lines), and the timer with the `try` / `catch`. The comment banner above (`:59-61`) and everything after `}, 2000);` stay.\n- Every other line is (correct) and is NOT touched.",
 exactnote="ONE hunk. The comment lines are part of the byte-exact `+` lines.\n",
 donot="**Do NOT touch** `seedDemoUsers` in `userRepo.ts`, any test mock, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Vitest imports are explicit. The timer is driven with `vi.useFakeTimers()`; `advance()` reports a throw as the string `THREW ...` so a red is an assertion. Pure ASCII.",
 red=['RED KS-1776 D1','RED KS-1776 D2'],
 cells="- RED `D1`: at the tip firing the timer throws `[vitest] No \"seedDemoUsers\" export is defined on the \"../repositories/userRepo\" mock` and the cell reads `THREW ...`; after, `ok`.\n- RED `D2`: at the tip nothing is logged (the throw skipped the logger); after, `Failed to seed demo users` is logged once.\n- CONTROL `C1` (a present `seedDemoUsers` is called once, with a function argument, at 2000 ms and not at 1999) and `C2` (a rejecting `seedDemoUsers` is logged): green at the tip AND after.",
 premises="- `routes/auth.ts:62` is `setTimeout(() => {` and the call is `:63`; read with `git show 8894c7486f82:Blockchain/Dev/services/auth/src/routes/auth.ts`.\n- `ks1151-auth-refresh-refuses-oauth-token.test.ts` imports the routes module under the same nine-module mock set (db, userRepo, session, refreshDenylist, accountLockout, password, email, events, logger); this test copies that set and drops the supertest-style socket parts.\n- The package test runner is vitest; the golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The ticket records the failure once, in a loaded run, and not whether the exit status is non-zero for an uncaught error alone.\n- Whether importing `routes/auth` under fake timers arms other timers whose firing at 2500 ms upsets the mocks: the control run measures it (if a control cell fails with the golden, this brief is not queued).\n- Open PRs touching either file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes KS-1776** only if the owner accepts this fix shape; otherwise Refs. Link as Refs KS-1776.",
)
