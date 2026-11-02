# Generates the two test files for operator 84 (auth issuerCertSweep.ts, vitest).
HEAD = r"""import { describe, it, expect, beforeAll, afterAll, beforeEach, afterEach, vi } from 'vitest';

// KS-1868 (operator 83 screen, issuer cert sweep): the catches in services/auth/src/services/issuerCertSweep.ts log
// `{ error: err instanceof Error ? err.message : String(err) }` with the read INSIDE the logger call's arguments, unguarded.
// A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch itself throw; an Error
// whose message is readable but not a string (a null-prototype object, a Symbol) is handed to the logger as is. The cells make the
// repository, the event bus or the platform scope reject with such a value and assert the line is logged as text (the constant
// when the value cannot be turned into text) and that the sweep goes on exactly as it does for an ordinary Error. Harness: the
// real sweep module with the logger, event bus, repository and shared scope replaced by plain stand-ins (no database, no network).
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  expiredFail: false,
  soonFailDays: 0,
  expiredRows: [] as unknown[],
  soonRows: {} as Record<number, unknown[]>,
  soonCalls: [] as number[],
  published: [] as string[],
  expiredPublishFails: false,
  soonPublishFails: false,
  scopeFails: false,
  logged: [] as unknown[][],
  unhandled: 0,
}));

const capture = vi.hoisted(() => ({
  debug: () => undefined,
  info: () => undefined,
  warn: (...args: unknown[]) => {
    h.logged.push(['warn', ...args]);
  },
  error: (...args: unknown[]) => {
    h.logged.push(['error', ...args]);
  },
  log: () => undefined,
}));
vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
vi.mock('@secuura/shared', () => ({
  runWithPlatformScope: (fn: () => Promise<unknown>) => (h.scopeFails ? Promise.reject(h.toThrow) : fn()),
}));
vi.mock('../events', () => ({
  EventTypes: { ISSUER_CERT_EXPIRED: 'EXPIRED', ISSUER_CERT_EXPIRING_SOON: 'SOON' },
  publishEvent: (type: string) => {
    h.published.push(type);
    if ((type === 'EXPIRED' && h.expiredPublishFails) || (type === 'SOON' && h.soonPublishFails)) {
      return Promise.reject(h.toThrow);
    }
    return Promise.resolve(undefined);
  },
}));
vi.mock('../repositories/issuerCertRepo', () => ({
  markExpiredCerts: () => (h.expiredFail ? Promise.reject(h.toThrow) : Promise.resolve(h.expiredRows)),
  findExpiringSoon: (days: number) => {
    h.soonCalls.push(days);
    if (h.soonFailDays === days) return Promise.reject(h.toThrow);
    return Promise.resolve(h.soonRows[days] ?? []);
  },
}));

const SAVED_LISTENERS = process.listeners('unhandledRejection');
const onUnhandled = () => {
  h.unhandled += 1;
};
const SAVED_INTERVAL_ENV = process.env.ISSUER_CERT_SWEEP_INTERVAL_MS;

let mod: typeof import('../services/issuerCertSweep');
beforeAll(async () => {
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  mod = await import('../services/issuerCertSweep');
});
afterAll(() => {
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
  if (SAVED_INTERVAL_ENV === undefined) delete process.env.ISSUER_CERT_SWEEP_INTERVAL_MS;
  else process.env.ISSUER_CERT_SWEEP_INTERVAL_MS = SAVED_INTERVAL_ENV;
});
beforeEach(() => {
  delete process.env.ISSUER_CERT_SWEEP_INTERVAL_MS;
  h.toThrow = undefined;
  h.expiredFail = false;
  h.soonFailDays = 0;
  h.expiredRows = [];
  h.soonRows = {};
  h.soonCalls.length = 0;
  h.published.length = 0;
  h.expiredPublishFails = false;
  h.soonPublishFails = false;
  h.scopeFails = false;
  h.logged.length = 0;
  h.unhandled = 0;
});
afterEach(() => {
  mod.stopIssuerCertSweep();
});

const row = (id: string) => ({
  id,
  tenantId: 'ten-1868',
  fingerprintSha256: 'fp-' + id,
  name: 'name-' + id,
  validUntil: new Date('2026-12-01T00:00:00.000Z'),
});
const flush = () => new Promise<void>((resolve) => setTimeout(resolve, 30));
async function run(): Promise<{ ok: boolean; value: unknown }> {
  try {
    return { ok: true, value: await mod.runIssuerCertSweep() };
  } catch {
    return { ok: false, value: undefined };
  }
}
const LINES = (level: string, msg: string) => h.logged.filter((c) => c[0] === level && c[1] === msg);
/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
const reasonOf = (c: unknown[] | undefined): string => {
  const v = (c?.[2] as { error?: unknown } | undefined)?.error;
  return typeof v === 'string' ? v : '<' + typeof v + '>';
};

const revokedProxy = (): unknown => {
  const rp = Proxy.revocable({}, {});
  rp.revoke();
  return rp.proxy;
};
/** An Error whose `message` getter succeeds and returns the value m. */
const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
const getterThrows = (): unknown =>
  Object.create(Error.prototype, {
    message: {
      get() {
        throw new Error('getter boom');
      },
    },
  });
const SHAPES: Array<[string, () => unknown, string]> = [
  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
  ['an Error whose message getter throws', getterThrows, 'unreadable thrown value'],
  ['an Error whose message is a null-prototype object', () => withMessage(Object.create(null)), 'unreadable thrown value'],
  ['an Error whose message is a Symbol', () => withMessage(Symbol('ks1868')), 'Symbol(ks1868)'],
];
"""

def cell(kind, n, title, body):
    return "  it('%s ks1868 %s%d %s', async () => {\n%s  });\n" % (kind, 'C' if kind=='control' else 'R', n, title, body)

def lines(*ls): return ''.join('    '+l+'\n' for l in ls)

# ---- site bodies
MSG66='Issuer cert sweep: markExpiredCerts failed'
MSG95='Issuer cert sweep: findExpiringSoon(7d) failed'
MSG83='publishEvent ISSUER_CERT_EXPIRED failed'
MSG113='publishEvent ISSUER_CERT_EXPIRING_SOON failed'
def b66(thrown, want):
    return lines("h.expiredFail = true;","h.toThrow = %s;"%thrown,"h.soonRows = { 30: [row('c30')] };",
     "expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });",
     "expect(h.soonCalls).toEqual([30, 7, 1]);","expect(h.published).toEqual(['SOON']);",
     "expect(LINES('error', '%s')).toHaveLength(1);"%MSG66,
     "expect(reasonOf(LINES('error', '%s')[0])).toBe(%s);"%(MSG66,want))
def b95(thrown, want):
    return lines("h.soonFailDays = 7;","h.toThrow = %s;"%thrown,"h.soonRows = { 30: [row('c30')], 1: [row('c1')] };",
     "expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 1: 1 } } });",
     "expect(h.soonCalls).toEqual([30, 7, 1]);","expect(h.published).toEqual(['SOON', 'SOON']);",
     "expect(LINES('error', '%s')).toHaveLength(1);"%MSG95,
     "expect(reasonOf(LINES('error', '%s')[0])).toBe(%s);"%(MSG95,want))
def b83(thrown, want):
    return lines("h.expiredRows = [row('cert-exp')];","h.expiredPublishFails = true;","h.toThrow = %s;"%thrown,
     "expect(await run()).toEqual({ ok: true, value: { expired: 1, expiringSoon: { 30: 0, 7: 0, 1: 0 } } });",
     "await flush();","expect(h.unhandled).toBe(0);",
     "expect(LINES('warn', '%s')).toHaveLength(1);"%MSG83,
     "expect(reasonOf(LINES('warn', '%s')[0])).toBe(%s);"%(MSG83,want),
     "expect((LINES('warn', '%s')[0]?.[2] as { certId?: string } | undefined)?.certId).toBe('cert-exp');"%MSG83)
def b113(thrown, want):
    return lines("h.soonRows = { 30: [row('c30')] };","h.soonPublishFails = true;","h.toThrow = %s;"%thrown,
     "expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });",
     "await flush();","expect(h.unhandled).toBe(0);",
     "expect(LINES('warn', '%s')).toHaveLength(1);"%MSG113,
     "expect(reasonOf(LINES('warn', '%s')[0])).toBe(%s);"%(MSG113,want),
     "expect((LINES('warn', '%s')[0]?.[2] as { daysRemaining?: number } | undefined)?.daysRemaining).toBe(30);"%MSG113)
def btimer(thrown, want):
    return lines("h.scopeFails = true;","h.toThrow = %s;"%thrown,
     "mod.startIssuerCertSweep(0);",
     "for (let i = 0; i < 40 && LINES('error', 'Initial issuer cert sweep failed').length < 1; i++) await flush();",
     "mod.stopIssuerCertSweep();","await flush();","expect(h.unhandled).toBe(0);",
     "expect(LINES('error', 'Initial issuer cert sweep failed')).toHaveLength(1);",
     "expect(reasonOf(LINES('error', 'Initial issuer cert sweep failed')[0])).toBe(%s);"%want,
     "expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(0);")

SHAPES=[('a revoked Proxy',),('an Error whose message getter throws',),('an Error whose message is a null-prototype object',),('an Error whose message is a Symbol',)]
def shapecells(start, site, fn, idxs):
    out=''; n=start
    for i in idxs:
        out+=cell('RED',n,'%s: a rejection that is %s is logged as text and the sweep goes on as it does for an ordinary Error'%(site,SHAPES[i][0]),
                  fn('SHAPES[%d][1]()'%i,'SHAPES[%d][2]'%i)); n+=1
    return out,n

def p1():
    t=HEAD+"\ndescribe('KS-1868 the issuer cert sweep body catches log text for a hostile thrown value', () => {\n"
    t+=cell('control',1,'markExpiredCerts: an ordinary Error is logged with its message and the sweep still runs the expiring-soon pass',b66("new Error('db down')","'db down'"))
    t+=cell('control',2,'markExpiredCerts: a thrown plain string is logged as its own text and the sweep still runs the expiring-soon pass',b66("'plain boom'","'plain boom'"))
    t+=cell('control',3,'findExpiringSoon(7): an ordinary Error is logged with its message and the other windows still run',b95("new Error('db down')","'db down'"))
    t+=cell('control',4,'the ISSUER_CERT_EXPIRED publish: an ordinary Error is logged as a warning with its message and nothing is unhandled',b83("new Error('bus down')","'bus down'"))
    n=1
    for site,fn,idx in (('markExpiredCerts',b66,[0,1,2,3]),('findExpiringSoon(7)',b95,[0,1,2,3]),('ISSUER_CERT_EXPIRED publish',b83,[0,3])):
        c,n=shapecells(n,site,fn,idx); t+=c
    return t+"});\n", n-1
def p2():
    t=HEAD+"\ndescribe('KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value', () => {\n"
    t+=cell('control',1,'the ISSUER_CERT_EXPIRING_SOON publish: an ordinary Error is logged as a warning with its message and nothing is unhandled',b113("new Error('bus down')","'bus down'"))
    t+=cell('control',2,'the ISSUER_CERT_EXPIRING_SOON publish: a thrown plain string is logged as a warning with its own text',b113("'plain boom'","'plain boom'"))
    t+=cell('control',3,'the startup sweep: an ordinary Error is logged with its message ',btimer("new Error('scope down')","'scope down'"))
    t+=cell('control',4,'the startup sweep: a thrown plain string is logged as its own text ',btimer("'plain boom'","'plain boom'"))
    n=1
    for site,fn,idx in (('ISSUER_CERT_EXPIRING_SOON publish',b113,[0,1,2,3]),('startup sweep',btimer,[0,1,2,3])):
        c,n=shapecells(n,site,fn,idx); t+=c
    return t+"});\n", n-1
if __name__=='__main__':
    import sys
    D='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator84/gen/'
    for name,f in (('t84_p1.ts.txt',p1),('t84_p2.ts.txt',p2)):
        t,nr=f(); open(D+name,'w').write(t); print(name,len(t.splitlines()),'lines',nr,'red cells')
