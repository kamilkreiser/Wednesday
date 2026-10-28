P='Blockchain/Dev/services/security/src/db.ts'
TP='Blockchain/Dev/services/security/src/__tests__/ks1587-transaction-listens-for-a-client-error-while-checked-out.test.ts'
E1=("  const client = await getClient();\n  try {\n    await client.query('BEGIN');\n",
    "  const client = await getClient();\n"
    "  // KS-1587 N1: a pg client that nobody listens to raises its 'error' event as an uncaught exception when the backend dies under it\n"
    "  // (\"Connection terminated unexpectedly\"), which exits the process. Listen for it while the client is checked out; the failing\n"
    "  // query's own rejection still reaches the catch below.\n"
    "  const onClientError = (err: Error) => {\n"
    "    dbLog('error', 'DB client error while checked out', { error: err.message });\n"
    "  };\n"
    "  client.on('error', onClientError);\n"
    "  try {\n    await client.query('BEGIN');\n")
E2=("    throw err;\n  } finally {\n    client.release();\n  }\n",
    "    throw err;\n  } finally {\n    client.removeListener('error', onClientError);\n    client.release();\n  }\n")
TEST='''// KS-1587 N1 (security db.ts transaction()): the pg client checked out for a transaction had no 'error' listener. When the database kills the backend under it
// (a failover, a terminated session), pg emits 'error' on the client; an EventEmitter with no listener turns that into an uncaught exception, and the process exits
// (gracefulShutdown). transaction() now listens while the client is checked out, logs the event, and removes the listener before releasing the client.
// pg is mocked: the client is a plain EventEmitter with query and release spies. R1 and R2 are red until the listener exists; C1 to C3 pin what must not move.
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { EventEmitter } from 'events';

const h = vi.hoisted(() => ({ client: null as any }));

vi.mock('pg', () => ({
  // A plain function (not an arrow) so `new Pool(...)` is constructible.
  Pool: vi.fn(function PoolMock() {
    return {
      query: vi.fn(),
      on: vi.fn(),
      end: vi.fn().mockResolvedValue(undefined),
      connect: vi.fn(async () => h.client),
    };
  }),
}));

function makeClient() {
  const c: any = new EventEmitter();
  c.query = vi.fn(async () => ({ rows: [] }));
  c.release = vi.fn();
  return c;
}

/** Fresh copy of the module per test: db.ts holds module-level state. */
async function importDb() {
  vi.resetModules();
  return import('../db');
}

describe('KS-1587 N1: transaction() listens for a client error while the client is checked out', () => {
  let consoleSpy: ReturnType<typeof vi.spyOn>;

  beforeEach(() => {
    process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test';
    consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    h.client = makeClient();
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    delete process.env.DATABASE_URL;
  });

  it('RED KS-1587 R1 an error event emitted on the client inside the transaction does not throw', async () => {
    const db = await importDb();
    const out = await db.transaction(async (client) => {
      expect(() => client.emit('error', new Error('Connection terminated unexpectedly'))).not.toThrow();
      return 'done';
    });
    expect(out).toBe('done');
  });

  it('RED KS-1587 R2 exactly one error listener is attached while the transaction runs', async () => {
    const db = await importDb();
    let seen = -1;
    await db.transaction(async (client) => {
      seen = client.listenerCount('error');
      return null;
    });
    expect(seen).toBe(1);
  });

  it('control KS-1587 C1 the listener is gone and the client is released once after a committed transaction', async () => {
    const db = await importDb();
    await db.transaction(async () => 'x');
    expect(h.client.listenerCount('error')).toBe(0);
    expect(h.client.release).toHaveBeenCalledTimes(1);
    expect(h.client.query.mock.calls.map((c: unknown[]) => c[0])).toEqual(['BEGIN', 'COMMIT']);
  });

  it('control KS-1587 C2 a throwing callback is rolled back, rethrown, and the listener is removed', async () => {
    const db = await importDb();
    await expect(db.transaction(async () => { throw new Error('boom'); })).rejects.toThrow('boom');
    expect(h.client.query.mock.calls.map((c: unknown[]) => c[0])).toEqual(['BEGIN', 'ROLLBACK']);
    expect(h.client.listenerCount('error')).toBe(0);
    expect(h.client.release).toHaveBeenCalledTimes(1);
  });

  it('control KS-1587 C3 the callback receives the checked-out client itself', async () => {
    const db = await importDb();
    let got: unknown = null;
    await db.transaction(async (client) => { got = client; return null; });
    expect(got).toBe(h.client);
  });
});
'''
S=dict(dir='ks_1587_p1',ticket='KS-1587',
 title='security db.ts transaction(): the checked-out pg client has no error listener, so a backend killed under it raises an uncaught exception (item N1, RUNG 2, code_patch: two hunks in one product + one NEW vitest file; the DRAFTER chose log-and-continue)',
 intro="DRAFT by Spark operator 7 for Wednesday, 2026-10-29 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Item N1 only of KS-1587, and only the security service's transaction() (the ticket's second comment names this file, db.ts:59-72). NOT in this brief: items m-a and m-b (referral integration cells), `queryWithTenantGuc` in packages/shared and security's own queryWithTenantGuc path, which carry the same pattern. DECISION FLAG: the ticket asks for 'a client.on(error, ...)' without saying what the handler does; this brief logs through dbLog and lets the failing query's own rejection reach the existing catch.",
 products=[(P,[E1,E2])],
 prodnote=['product, modified in place: TWO hunks (listener attached after getClient; listener removed in the finally)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (2 red, 3 control; pg mocked, the client is an EventEmitter)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1587-transaction-listens-for-a-client-error-while-checked-out.test.ts` from `Blockchain/Dev/services/security',
 tier='code_patch', rung='2 (two hunks, 9 added lines and 1 added line byte-exact; the new test given whole)',
 pins='''# code_patch, 2 hunks in security db.ts transaction() + a NEW vitest file; ref = db.retry.test.ts (the pg-mocked db.ts shape); line = the first changed line.
tier=code_patch
ref=Blockchain/Dev/services/security/src/__tests__/db.retry.test.ts
line=60
ctx=65536
''',
 wrong="`transaction()` in `services/security/src/db.ts:59-72` checks a client out of the pool (`getClient()`), runs BEGIN, the callback and COMMIT, and releases the client in a `finally`. Nothing listens for the client's `'error'` event. When the database kills the backend under a checked-out client (a failover, a terminated session) `pg` emits `'error'` on the client; an EventEmitter with no listener turns that into an uncaught exception, and in production an uncaught exception exits the process (gracefulShutdown). The request itself fails with the query's own rejection and the next request works, so the process exit is the avoidable part. The change: after `getClient()`, attach a named handler `onClientError` that logs through `dbLog('error', 'DB client error while checked out', { error: err.message })`, and in the `finally` call `client.removeListener('error', onClientError)` before `client.release()`. Nothing else in the function changes.",
 where="- `src/db.ts:60-62` - **must change**: after `const client = await getClient();` (line 60, context) seven lines are inserted before `try {`: three comment lines, `const onClientError = (err: Error) => {`, the `dbLog(...)` line, `};`, and `client.on('error', onClientError);`. `try {` and `await client.query('BEGIN');` are context.\n- `src/db.ts:69-70` - **must change**: in the `finally`, directly before `client.release();` the line `client.removeListener('error', onClientError);` is inserted (`throw err;` and `} finally {` are context).\n- Every other function in the file is NOT touched.",
 exactnote="Two hunks in one file, in file order.\n",
 donot="**Do NOT touch** `getClient`, `query`, the BEGIN/COMMIT/ROLLBACK statements, `dbLog`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It uses `vi.hoisted` for the mutable client the `vi.mock('pg')` factory returns.",
 red=['RED KS-1587 R1','RED KS-1587 R2'],
 cells="- RED `R1`: at the tip emitting `'error'` on a client with no listener throws (EventEmitter semantics), so `not.toThrow()` fails by ASSERTION; after the edit the handler absorbs it.\n- RED `R2`: at the tip the listener count inside the transaction is 0, not 1.\n- CONTROL `C1` to `C3`: green at the tip AND after (BEGIN/COMMIT order and a single release; ROLLBACK and rethrow on a throwing callback; the callback gets the checked-out client).",
 premises="- `db.ts:59-72` is `transaction()` as quoted; `dbLog` is a module-level function in the same file (`:17`), so no import changes (read at the tip).\n- `db.retry.test.ts` already mocks `pg` the same way (a constructible `Pool` mock) and imports `../db` after `vi.resetModules()`.\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- A REAL `pg` backend kill is not exercised (the mock models only the EventEmitter behaviour): the ticket's own measurement (`Connection terminated unexpectedly` reported as an uncaught exception) is not re-run.\n- Whether security's ROLLBACK in the catch can itself fail on a dead connection and replace the original error: unmeasured, not changed.\n- Open PRs touching this file: none by the git file lists of PRs 1782 and 1785-1799 read on 2026-10-29.",
 scope="**KS-1587 item N1, security transaction() only.** DECISION FLAG above. Link the PR as Refs KS-1587, never a close-word (m-a, m-b and the shared-code half stay open).",
)
