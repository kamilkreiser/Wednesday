TASKS={}
KP='Blockchain/Dev/services/kyc/'
K_REF=KP+'src/__tests__/db.retry.test.ts'
S9="This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator."

def mknew(old):
    # old is one full source line `    logger.error('MSG', { ... error: err instanceof Error ? err.message : String(err) });\n` at indent 4
    marker='error: err instanceof Error ? err.message : String(err)'
    assert old.count(marker)==1
    s='    '
    head=(s+"let reason: string;\n"+s+"try {\n"+s+"  reason = err instanceof Error ? err.message : String(err);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
    return head+old.replace(marker,'error: reason')

HEAD="""import { describe, it, expect, vi, beforeAll, beforeEach, afterAll } from 'vitest';
import http from 'http';
import { randomUUID } from 'crypto';

process.env.KYC_PROVIDER = 'mock';
process.env.NODE_ENV = 'test';

// KS-1868: `%(helper)s` must still log its line and let %(route)s carry on when the thrown value
// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws,
// throws on `.message`). Harness: the KS-1845 one (real app on a real listener, db and subject-DEK modules replaced).
// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
// itself fail on a revoked Proxy before the code under test saw it.
// Three of the helpers are awaited by handlers with no try/catch (Express 4 never sees their rejection), so
// a rejecting helper leaves the request hanging: the cell gives the request a short deadline and counts the
// unhandled rejection itself instead of letting the runner report it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  failOn: undefined as RegExp | undefined,
  logged: [] as unknown[][],
  unhandled: 0,
}));

vi.mock('../db', () => ({
  initDb: async () => undefined,
  isDbAvailable: () => true,
  query: (sql: string) => {
    if (h.failOn && h.failOn.test(String(sql))) return Promise.reject(h.toThrow);
    return Promise.resolve({ rows: [] });
  },
}));

vi.mock('../subjectDeks', () => ({
  subjectDeks: {
    getOrCreateDek: async () => Buffer.alloc(32, 7),
    getDek: async () => Buffer.alloc(32, 7),
    evict: () => undefined,
  },
}));

vi.mock('../utils/logger', () => {
  const logger = {
    info: () => undefined,
    warn: () => undefined,
    debug: () => undefined,
    error: (...args: unknown[]) => {
      h.logged.push(args);
    },
  };
  return { logger, createLogger: () => logger, validateEnv: () => undefined };
});

vi.mock('@secuura/shared', async (importOriginal) => {
  const actual = await importOriginal<Record<string, unknown>>();
  return {
    ...actual,
    encryptFieldWithDek: (plain: string) => plain,
    isEncryptedPii: () => false,
    isSubjectDekCiphertext: () => false,
    authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  };
});

vi.mock('express', async (importOriginal) => {
  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
  const factory: any = (...args: any[]) => {
    const app = actual(...args);
    app.listen = () => ({ close: (cb?: () => void) => cb?.(), address: () => ({ port: 0 }), on() { return this; } });
    return app;
  };
  Object.assign(factory, actual);
  return { ...actual, default: factory };
});

const TIMEOUT_MS = 2500;
const SITE_ID = randomUUID();
const SAVED_LISTENERS = process.listeners('unhandledRejection');
const onUnhandled = () => {
  h.unhandled += 1;
};

let httpServer: http.Server;
let origin: string;

async function startApp() {
  if (httpServer) return;
  const app = (await import('../index')).default as any;
  httpServer = http.createServer(app);
  await new Promise<void>((resolve) => httpServer.listen(0, '127.0.0.1', () => resolve()));
  origin = 'http://127.0.0.1:' + String((httpServer.address() as any).port);
}

/** undefined when the request got no answer inside the deadline. */
async function callRoute(method: string, path: string, body?: unknown) {
  const res = await fetch(origin + path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
    signal: AbortSignal.timeout(TIMEOUT_MS),
  }).catch(() => undefined);
  if (!res) return undefined;
  const parsed: any = await res.json().catch(() => undefined);
  return { status: res.status, body: parsed };
}

const call = () => %(callsrc)s;
const LINES = () => h.logged.filter((c) => String(c[0]).includes('%(msg)s'));

afterAll(async () => {
  if (httpServer) {
    (httpServer as http.Server & { closeAllConnections?: () => void }).closeAllConnections?.();
    await new Promise<void>((resolve) => httpServer.close(() => resolve()));
  }
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
});

describe('KS-1868 %(helper)s reads the thrown value safely', () => {
  beforeAll(async () => {
    process.removeAllListeners('unhandledRejection');
    process.on('unhandledRejection', onUnhandled);
    await startApp();
  }, 120_000);

  beforeEach(() => {
    h.toThrow = undefined;
    h.failOn = %(failon)s;
    h.logged.length = 0;
    h.unhandled = 0;
  });

  it('control ks1868 C1 an ordinary Error still logs its message and %(okname)s', async () => {
    h.toThrow = new Error('db down');
    const res = await call();
    expect(res?.status).toBe(%(status)d);
%(okcheck)s    expect(LINES()).toHaveLength(1);
    expect(LINES()[0][1]).toEqual(%(meta)s);
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and %(okname)s', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    const res = await call();
    expect(res?.status).toBe(%(status)d);
%(okcheck)s    expect(LINES()).toHaveLength(1);
    expect(LINES()[0][1]).toEqual(%(metaU)s);
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and %(okname)s', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const res = await call();
    expect(res?.status).toBe(%(status)d);
%(okcheck)s    expect(LINES()).toHaveLength(1);
    expect(LINES()[0][1]).toEqual(%(metaU)s);
  });
});
"""

INIT="callRoute('POST', '/api/kyc/initiate', { userId: randomUUID(), requestedLevel: 'BASIC', consentGiven: true })"
def add(key, slug, helper, line, oldline, msg, route, failon, callsrc, status, okname, okcheck, meta_extra, callers, ret, tail_note):
    ms=lambda e: "{ %serror: %s }"%(meta_extra, e)
    old=oldline+"\n"
    new=mknew(oldline+"\n")
    t=HEAD%dict(helper=helper,route=route,callsrc=callsrc,msg=msg,failon=failon,status=status,okname=okname,okcheck=okcheck,
                meta=ms("'db down'"),metaU=ms("'unreadable thrown value'"))
    where_note=("The catch block's `instanceof Error` read is on line %d; the catch logs '%s' at error level and does NOT rethrow: %s. "
      "The message is only logged, never returned to a caller or put in a response. CALLERS (git grep at the tip, kyc/src/index.ts): %s. %s")%(line,msg,ret,callers,tail_note)
    TASKS[key]=dict(svc='kyc',runner='vitest',runcmd='run ',runner_dir='Blockchain/Dev/services/kyc',ref=K_REF,s9note=S9,
      dir='ks_1868_o47_%s_kyc_%s_unreadable_throw'%(key,slug),
      prod=KP+'src/index.ts', test=KP+'src/__tests__/ks1868-kyc-%s-unreadable-throw.test.ts'%slug.replace('_','-'),
      old=old,new=new,tbody=t,where_line=line,fn='`%s`'%helper,file='index.ts',
      shape="`vi.mock(...)` of the collaborators and a dynamic import of the module under test (db.retry.test.ts; its file-scope names do not clash with this test). The harness itself (real app on a real listener, `@secuura/shared` and `express` replaced) follows ks1845-kyc-review-requires-a-platform-reviewer.test.ts, which cannot be the pinned ref because it declares a file-scope `as` that the checker splices into any test that merely uses the TypeScript keyword",
      intro_site="the catch block of `%s` in `services/kyc/src/index.ts`"%helper,
      where_note=where_note,
      whatwrong=("In `index.ts` the catch block of `%s` logs `logger.error('%s', { ... error: err instanceof Error ? err.message : String(err) })` (the read is on line %d) and then %s. "
       "If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
       "Either way the catch throws before the line is logged and before the normal return, so the helper rejects with the hostile value. "
       "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }`.")%(helper,msg,line,ret),
      consequence="Today a hostile rejection from the database layer makes the catch block itself throw, so nothing is logged and the helper rejects.",
      red1="At the tip the request either gets a 500 from the error handler or never answers, so the status assertion fails (and no line is logged)",
      dbnote="`../db`, `../subjectDeks`, `../utils/logger`, `@secuura/shared` (authenticate, three crypto pass-throughs) and `express` (listen) are replaced; no database, no port and no network beyond 127.0.0.1. The helper is not exported, so it is reached through %s."%route,
      sibling="Every other catch block of `index.ts` (including the other four KS-1868 helpers `dbSaveVerification`, `dbGetVerification`, `dbGetVerificationsByUser`, `dbGetVerificationStats`, `dbSaveConsent` that are not this brief's, and the `DB save image failed` catch at :323 which rethrows a constant AppError) is NOT in this brief")

OKP="    expect(res?.body?.success).toBe(true);\n"
add('p1','save_verification','dbSaveVerification',192,
    "    logger.error('DB save verification failed', { error: err instanceof Error ? err.message : String(err) });",
    'DB save verification failed','POST /api/kyc/initiate',r"/INSERT\s+INTO\s+svc_kyc_verifications/i",INIT,201,'the request still completes 201',OKP,'',
    ':712 (POST /api/kyc/initiate, inside a try whose catch calls next(error)), :859 (POST /:id/document, same shape), :896 and :1045 (mock-mode timers, inside `void (async () => {...})().catch(() => {})`), :970 (POST /:id/selfie, try), :1016 (POST /:id/complete, no try), :1114 (POST /:id/review, try). Every caller awaits it and discards the result; none reads a message from it',
    'it returns nothing (void)',
    'The hostile throw reaches a response today only through the route catch -> next(error) -> the shared errorHandler (5xx messages are redacted there per KS-727; not re-read by the operator); the helper\'s OWN message never reaches a response')
add('p2','get_verification','dbGetVerification',202,
    "    logger.error('DB get verification failed', { id, error: err instanceof Error ? err.message : String(err) });",
    'DB get verification failed','GET /api/kyc/:id',r"/FROM\s+svc_kyc_verifications\s+WHERE\s+id/i","callRoute('GET', '/api/kyc/' + SITE_ID)",404,'the route answers 404 Verification not found',"    expect(res?.body?.error?.code).toBe('NOT_FOUND');\n","id: SITE_ID, ",
    ':757 (GET /api/kyc/:id, no try: the handler answers 404 when it gets undefined), :806 (POST /:id/document, try), :876 and :1028 (mock-mode timers, `.catch(() => {})`), :929 (POST /:id/selfie, try), :995 (POST /:id/complete, no try), :1080 (POST /:id/review, try), :1139 (GET /:id/result, no try). Every caller treats undefined as 404 and uses no message',
    'it falls through to `return undefined`',
    'A caller with no try/catch (:757, :995, :1139) leaves a rejecting helper as an unhandled rejection under Express 4 (the request never answers); that is today\'s behaviour for a hostile throw, and the fix makes it behave like an ordinary error already does (404)')
add('p3','get_verifications_by_user','dbGetVerificationsByUser',217,
    "    logger.error('DB get verifications by user failed', { userId, error: err instanceof Error ? err.message : String(err) });",
    'DB get verifications by user failed','GET /api/kyc/user/:userId',r"/FROM\s+svc_kyc_verifications\s+WHERE\s+user_id/i","callRoute('GET', '/api/kyc/user/' + SITE_ID)",200,'the route answers an empty list',"    expect(res?.body?.data?.count).toBe(0);\n","userId: SITE_ID, ",
    ':774 (GET /api/kyc/user/:userId, no try; it answers the list with count) and :350 (inside dbDeleteUserData, the GDPR erasure cascade: DELETE /api/kyc/user/:userId/data at :1177 and the user.erased subscriber at :1274). No caller reads a message. NOTE the :350 caller: when the helper returns [] the erasure continues and still deletes images by user_id and the consents and verification rows; only the legacy-image id collection is skipped. A hostile throw today aborts the erasure instead, so the fix changes that path from "abort" to "continue", which is what an ordinary DB error already does',
    'it returns an empty array',
    'The raise PR must say that the erasure cascade (:350) is a caller whose behaviour for a hostile throw changes from abort to continue')
add('p4','get_verification_stats','dbGetVerificationStats',235,
    "    logger.error('DB get verification stats failed', { error: err instanceof Error ? err.message : String(err) });",
    'DB get verification stats failed','GET /health',r"/COUNT/i","callRoute('GET', '/health')",200,'/health answers zeros',"    expect(res?.body?.stats).toEqual({ totalVerifications: 0, pending: 0, approved: 0 });\n","",
    ':557 (GET /health, no try; it puts stats.total/pending/approved, numbers only, in the response). No message reaches the response. A hostile throw today leaves the health endpoint unanswered (an unhandled rejection), which is the worst place for it',
    'it returns zeros',
    'Only the three counts are in the /health body')
add('p5','save_consent','dbSaveConsent',251,
    "    logger.error('DB save consent failed', { error: err instanceof Error ? err.message : String(err) });",
    'DB save consent failed','POST /api/kyc/initiate',r"/INSERT\s+INTO\s+svc_kyc_consents/i",INIT,201,'the request still completes 201',OKP,'',
    ':725 (POST /api/kyc/initiate, inside a try whose catch calls next(error)); the only caller. It awaits and discards the result; no message is read from it',
    'it returns nothing (void)',
    'The hostile throw reaches a response today only through the route catch -> next(error) -> the shared errorHandler (not re-read)')
