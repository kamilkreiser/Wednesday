TASKS={}
PKG='Blockchain/Dev/packages/shared/'
P1_PROD=PKG+'src/security/audit-logger.ts'
P1_TEST=PKG+'src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts'
P1_OLD="""      } catch (error) {
        logger.error('Failed to process audit event', { error: error instanceof Error ? error.message : String(error) });
        // Re-add to buffer for retry
"""
P1_NEW="""      } catch (error) {
        let reason: string;
        try {
          reason = error instanceof Error ? error.message : String(error);
        } catch {
          reason = 'unreadable thrown value';
        }
        logger.error('Failed to process audit event', { error: reason });
        // Re-add to buffer for retry
"""
P1_T="""import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// KS-1868: AuditLogger.flush must still log its failure and put the event back in the buffer for
// retry when `onEvent` rejects with a value that cannot be read (a revoked Proxy throws on
// `instanceof`; an Error whose `message` getter throws, throws on `.message`). Today the catch
// block itself throws, so flush() rejects and the failed event is dropped instead of retried.
// `onEvent` is a plain function, not vi.fn(): a spy inspects what it rejects with and could itself
// fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  error: vi.fn(),
}));

vi.mock('../logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
}));

import { AuditLogger, AuditEventCategory } from '../security/audit-logger';

type Outcome = { threw: boolean; delivered: number };

async function run(toThrow: unknown): Promise<Outcome> {
  let fail = true;
  let delivered = 0;
  const audit = new AuditLogger({
    serviceName: 'svc',
    version: '1',
    environment: 'test',
    hashIntegrity: false,
    maxBatchSize: 1000,
    flushIntervalMs: 3600000,
    onEvent: () => {
      if (fail) return Promise.reject(toThrow);
      delivered++;
      return Promise.resolve();
    },
  });
  const out: Outcome = { threw: false, delivered: 0 };
  try {
    await audit.log(AuditEventCategory.SECURITY, 'KS1868_PROBE');
    try {
      await audit.flush();
    } catch {
      out.threw = true;
    }
    fail = false;
    await audit.flush();
    out.delivered = delivered;
  } finally {
    audit.stopFlushTimer();
  }
  return out;
}

const FLUSH_ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to process audit event'));

describe('KS-1868 AuditLogger.flush reads an onEvent failure safely', () => {
  beforeEach(() => {
    h.error.mockReset();
  });
  afterEach(() => {
    vi.clearAllTimers();
  });

  it('control ks1868 C1 an ordinary Error is logged with its message and the event is retried', async () => {
    const out = await run(new Error('sink down'));
    expect(out.threw).toBe(false);
    expect(FLUSH_ERRORS()).toHaveLength(1);
    expect(FLUSH_ERRORS()[0][1]).toEqual({ error: 'sink down' });
    expect(out.delivered).toBe(1);
  });

  it('RED ks1868 R1 a revoked Proxy rejection is logged as a constant and the event is retried', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    const out = await run(proxy);
    expect(out.threw).toBe(false);
    expect(FLUSH_ERRORS()).toHaveLength(1);
    expect(FLUSH_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
    expect(out.delivered).toBe(1);
  });

  it('RED ks1868 R2 an Error whose message getter throws is logged as a constant and the event is retried', async () => {
    const hostile = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const out = await run(hostile);
    expect(out.threw).toBe(false);
    expect(FLUSH_ERRORS()).toHaveLength(1);
    expect(FLUSH_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
    expect(out.delivered).toBe(1);
  });
});
"""
TASKS['p1']=dict(
 dir='ks_1868_o39_p1_shared_audit_logger_flush_unreadable_throw',
 prod=P1_PROD, test=P1_TEST, old=P1_OLD, new=P1_NEW, tbody=P1_T,
 svc='shared', where_line=322, catch_start=321,
 fn='`AuditLogger.flush`', file='audit-logger.ts',
 runner_dir='Blockchain/Dev/packages/shared',
 ref=PKG+'src/__tests__/ks932-timeout-bounds-dns.test.ts',
 intro_site="the catch block of `AuditLogger.flush` in `audit-logger.ts`",
 where_note="The catch block starts at line 321 (`} catch (error) {`) inside the `for (const event of events)` loop of `flush()`; it logs 'Failed to process audit event' and then re-adds the event to the buffer.",
 s9note="The seat brief for the security tickets (S9) names `packages/shared` only for `tenant-context.ts` and `tenant-pool-manager.ts` (KS-1860); it does not name `security/audit-logger.ts`.",
 whatwrong=("In `audit-logger.ts` the catch block of `AuditLogger.flush` (starts at line 321) logs "
  "`logger.error('Failed to process audit event', { error: error instanceof Error ? error.message : String(error) })` (line 322) and only then re-adds the event with `this.eventBuffer.unshift(event)` (line 324). "
  "If `onEvent` rejects with a revoked Proxy, `error instanceof Error` itself throws a TypeError (\"Cannot perform 'getPrototypeOf' on a proxy that has been revoked\") inside the catch block; if it rejects with an Error whose `message` getter throws, `error.message` throws. "
  "Either way the catch throws before the `unshift`: `flush()` rejects, the failed event (already removed from the buffer at the top of `flush`) is lost instead of retried, and the periodic timer call `this.flush()` becomes an unhandled rejection. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log line uses `reason`. "
  "Nothing else changes: an ordinary Error still logs `{ error: <its message> }`, the log text is unchanged, and the `unshift` retry is untouched."),
 consequence="Today a hostile rejection from `onEvent` makes the catch block itself throw, so nothing is logged, the event is not put back, and flush() rejects.",
 sibling="Every other function in `audit-logger.ts` and every other `instanceof Error` site in `packages/shared` is NOT in this brief",
 red1="At the tip `flush()` rejects (`run` records that as `threw: true`, and the event is never delivered, so the failure is the `threw` assertion)",
 dbnote="`AuditLogger` is exported and takes a plain `onEvent` function; `hashIntegrity` is off and the flush interval is an hour so the timer never fires, and `stopFlushTimer()` clears it. The logger module (`../logger`, a directory index) is mocked.")
