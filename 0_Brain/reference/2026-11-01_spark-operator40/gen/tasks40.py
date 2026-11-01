TASKS={}
PKG='Blockchain/Dev/services/analytics/'
REF=PKG+'src/__tests__/ks1868-analytics-service-load-unreadable-throw.test.ts'

def _test(cls_desc, imp, ctor_call, warnkey, mockextra=''):
    return """import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: %(d)s must still log its WARN when the thrown value
// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose
// `message` getter throws, throws on `.message`).
// The db stand-in is a plain function, not a vi.fn(): a spy inspects what it
// rejects with and could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  warn: vi.fn(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: () => Promise.reject(h.toThrow),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: h.warn, error: vi.fn(), debug: vi.fn() },
}));

%(imp)s

const WARNS = () => h.warn.mock.calls.filter((c) => String(c[0]).includes('%(k)s'));

describe('KS-1868 %(d)s reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.warn.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message', async () => {
    h.toThrow = new Error('db down');
    await %(c)s;
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    await %(c)s.catch(() => undefined);
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await %(c)s.catch(() => undefined);
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
""" % dict(d=cls_desc, imp=imp, c=ctor_call, k=warnkey)

def _new(old_head, msg):
    return old_head

# ---- P1: ExportService.loadFromDb
E_OLD="""    } catch (err) {
      logger.warn('ExportService.loadFromDb failed — starting with empty store', {
        error: err instanceof Error ? err.message : String(err),
      });
    }
"""
E_NEW="""    } catch (err) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('ExportService.loadFromDb failed — starting with empty store', {
        error: reason,
      });
    }
"""
S_OLD="""  } catch (err) {
    logger.warn('loadScheduledJobsFromDb failed — starting with defaults only', {
      error: err instanceof Error ? err.message : String(err),
    });
  }
"""
S_NEW="""  } catch (err) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('loadScheduledJobsFromDb failed — starting with defaults only', {
      error: reason,
    });
  }
"""
COMMON=dict(svc='analytics', runner_dir='Blockchain/Dev/services/analytics', ref=REF,
 s9note="This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator.",
 red1="At the tip the call rejects (the test swallows that with `.catch`), so no WARN is logged and the WARN-count assertion fails",
 dbnote="The `../db` module and `../utils/logger` are mocked; no database, no app boot and no network. The db stand-in is a plain function on purpose.")
TASKS['p1']=dict(COMMON,
 dir='ks_1868_o40_p1_analytics_exportservice_loadfromdb_unreadable_throw',
 prod=PKG+'src/services/exportService.ts',
 test=PKG+'src/__tests__/ks1868-export-service-load-unreadable-throw.test.ts',
 old=E_OLD, new=E_NEW,
 tbody=_test('ExportService.loadFromDb',"import { ExportService } from '../services/exportService';","new ExportService().loadFromDb()",'ExportService.loadFromDb failed'),
 where_line=297, catch_start=295, fn='`ExportService.loadFromDb`', file='exportService.ts',
 intro_site="the catch block of `ExportService.loadFromDb` in `exportService.ts`",
 where_note="The catch block starts at line 295 (`} catch (err) {`); it logs the WARN 'ExportService.loadFromDb failed — starting with empty store' with `{ error: <message> }`. The identical fix is already on develop in `analyticsService.ts` and `metricsCollector.ts` (loadFromDb).",
 whatwrong=("In `exportService.ts` the catch block of `ExportService.loadFromDb` (line 295) logs `logger.warn('ExportService.loadFromDb failed — starting with empty store', { error: err instanceof Error ? err.message : String(err) })` (the read is on line 297). "
  "If the query rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the WARN is emitted: `loadFromDb()` rejects (the caller in `index.ts` runs it inside a startup `Promise.all` with the other loaders) and the operator sees no WARN. "
  "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the WARN uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }` and the log text is unchanged."),
 consequence="Today a hostile rejection from the query makes the catch block itself throw, so no WARN is logged and `loadFromDb()` rejects instead of starting with an empty store.",
 sibling="The other three `instanceof Error` reads in `exportService.ts` (lines 56 and 160, the dbSaveExport catch and the generate catch whose message is stored on the export record) are NOT in this brief")
TASKS['p2']=dict(COMMON,
 dir='ks_1868_o40_p2_analytics_scheduledjobs_loadfromdb_unreadable_throw',
 prod=PKG+'src/services/scheduledJobs.ts',
 test=PKG+'src/__tests__/ks1868-scheduled-jobs-load-unreadable-throw.test.ts',
 old=S_OLD, new=S_NEW,
 tbody=_test('loadScheduledJobsFromDb',"import { loadScheduledJobsFromDb } from '../services/scheduledJobs';","loadScheduledJobsFromDb()",'loadScheduledJobsFromDb failed'),
 where_line=151, catch_start=149, fn='`loadScheduledJobsFromDb`', file='scheduledJobs.ts',
 intro_site="the catch block of the exported function `loadScheduledJobsFromDb` in `scheduledJobs.ts`",
 where_note="The catch block starts at line 149 (`} catch (err) {`); it logs the WARN 'loadScheduledJobsFromDb failed — starting with defaults only' with `{ error: <message> }`.",
 whatwrong=("In `scheduledJobs.ts` the catch block of `loadScheduledJobsFromDb` (line 149) logs `logger.warn('loadScheduledJobsFromDb failed — starting with defaults only', { error: err instanceof Error ? err.message : String(err) })` (the read is on line 151). "
  "If a query rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the WARN is emitted: `loadScheduledJobsFromDb()` rejects (it is one of the startup loaders in `index.ts`) instead of starting with defaults. "
  "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the WARN uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }` and the log text is unchanged."),
 consequence="Today a hostile rejection from the query makes the catch block itself throw, so no WARN is logged and the loader rejects instead of starting with defaults.",
 sibling="The two `instanceof Error` reads in `dbSaveAlertRule` (line 59) and `dbSaveAlert` (line 85) are NOT in this brief")
