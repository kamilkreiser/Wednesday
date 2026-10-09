/**
 * =============================================================================
 * DB AVAILABILITY RETRY — UNIT TESTS (KS-377 / KS-382 — governance)
 * =============================================================================
 * Verifies the boot-order resilience contract of src/db.ts: a failed initial
 * probe must schedule background re-probes with capped backoff and flip
 * isDbAvailable() to true once the database answers — never latch degraded
 * mode for the process lifetime. Also verifies the KS-382 extension: the
 * one-shot boot work registered via initDb's onReady hook (the governance
 * proposal-counter seed) runs on boot success AND is re-run on recovery, so
 * recovery is complete rather than just the flag flip.
 * =============================================================================
 */

// Controllable stand-in for pg.Pool.query — each test scripts its behaviour.
// (The `mock` prefix is required so jest's hoisted module factory below is
// allowed to reference it.)
const mockQuery = jest.fn();

jest.mock('pg', () => ({
  // A plain function (not an arrow) so `new Pool(...)` is constructible —
  // jest forwards the `new` to the implementation.
  Pool: jest.fn(function PoolMock() {
    return {
      query: mockQuery,
      on: jest.fn(),
      end: jest.fn().mockResolvedValue(undefined),
      connect: jest.fn(),
    };
  }),
}));

/** Fresh copy of the module per test — db.ts holds module-level state. */
async function importDb(): Promise<typeof import('../db')> {
  jest.resetModules();
  return import('../db');
}

const DB_UP = { rows: [{ ok: 1 }] };

describe('db availability retry (KS-377)', () => {
  // Silence db.ts's structured console.log lines; restored per test below.
  // (Deliberately NOT jest.restoreAllMocks() — that would also strip the pg
  // module mock's implementation between tests.)
  let consoleSpy: jest.SpyInstance;

  beforeEach(() => {
    // Modern (non-legacy) fake timers so async timer advancement works.
    jest.useFakeTimers({ legacyFakeTimers: false });
    mockQuery.mockReset();
    process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test';
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.useRealTimers();
    consoleSpy.mockRestore();
    delete process.env.DATABASE_URL;
  });

  it('reports available immediately when the probe succeeds at boot', async () => {
    mockQuery.mockResolvedValue(DB_UP);
    const db = await importDb();

    await expect(db.initDb()).resolves.toBe(true);
    expect(db.isDbAvailable()).toBe(true);
  });

  it('recovers when the DB comes up after a lost boot race (the KS-377 latch)', async () => {
    // Boot race: the first probe fails, the DB is up by the first retry.
    mockQuery.mockRejectedValueOnce(new Error('Connection terminated due to connection timeout'));
    mockQuery.mockResolvedValue(DB_UP);
    const db = await importDb();

    await expect(db.initDb()).resolves.toBe(false);
    expect(db.isDbAvailable()).toBe(false);

    // First background re-probe fires after the initial 1s delay.
    await jest.advanceTimersByTimeAsync(1_000);
    expect(db.isDbAvailable()).toBe(true);
  });

  it('backs off between failed retries and still recovers eventually', async () => {
    // initDb + first two retries fail, third retry succeeds.
    mockQuery
      .mockRejectedValueOnce(new Error('down'))
      .mockRejectedValueOnce(new Error('down'))
      .mockRejectedValueOnce(new Error('down'))
      .mockResolvedValue(DB_UP);
    const db = await importDb();

    await db.initDb();

    // Retry 1 at +1s — fails, backoff doubles to 2s.
    await jest.advanceTimersByTimeAsync(1_000);
    expect(db.isDbAvailable()).toBe(false);

    // Advancing less than the backed-off delay must NOT probe again.
    await jest.advanceTimersByTimeAsync(1_000);
    expect(db.isDbAvailable()).toBe(false);

    // Complete retry 2's 2s window — fails, backoff doubles to 4s.
    await jest.advanceTimersByTimeAsync(1_000);
    expect(db.isDbAvailable()).toBe(false);

    // Retry 3 at +4s succeeds — the flag flips without any restart.
    await jest.advanceTimersByTimeAsync(4_000);
    expect(db.isDbAvailable()).toBe(true);
    // initDb + 3 retries = 4 probes in total.
    expect(mockQuery).toHaveBeenCalledTimes(4);
  });

  it('does not retry when DATABASE_URL is unset (config error, not a race)', async () => {
    delete process.env.DATABASE_URL;
    const db = await importDb();

    await expect(db.initDb()).resolves.toBe(false);

    // No probe ever runs — there is nothing to retry toward.
    await jest.advanceTimersByTimeAsync(120_000);
    expect(mockQuery).not.toHaveBeenCalled();
    expect(db.isDbAvailable()).toBe(false);
  });

  it('closeDb cancels a pending retry', async () => {
    mockQuery.mockRejectedValue(new Error('down'));
    const db = await importDb();

    await db.initDb();
    expect(mockQuery).toHaveBeenCalledTimes(1);

    await db.closeDb();

    // The scheduled probe must not fire after shutdown.
    await jest.advanceTimersByTimeAsync(60_000);
    expect(mockQuery).toHaveBeenCalledTimes(1);
  });

  it('runs registered boot work when the boot probe succeeds (KS-382)', async () => {
    mockQuery.mockResolvedValue(DB_UP);
    const db = await importDb();
    // Stand-in for governanceService.verifyDbReady (proposal-counter seed).
    const bootWork = jest.fn().mockResolvedValue(undefined);

    await expect(db.initDb(bootWork)).resolves.toBe(true);
    expect(bootWork).toHaveBeenCalledTimes(1);
  });

  it('re-runs registered boot work when the DB recovers after a lost boot race (KS-382)', async () => {
    // Boot race: the probe fails at boot, so the proposal-counter seed is
    // skipped at that point …
    mockQuery.mockRejectedValueOnce(new Error('down'));
    mockQuery.mockResolvedValue(DB_UP);
    const db = await importDb();
    const bootWork = jest.fn().mockResolvedValue(undefined);

    await expect(db.initDb(bootWork)).resolves.toBe(false);
    expect(bootWork).not.toHaveBeenCalled();

    // … and the recovery probe at +1s must run it, not just flip the flag.
    await jest.advanceTimersByTimeAsync(1_000);
    expect(db.isDbAvailable()).toBe(true);
    expect(bootWork).toHaveBeenCalledTimes(1);
  });
});
