# Builds the B-pass test files from the merged PR 1925 sibling suites (refs saved in the report dir): keeps the harness, replaces header + cells.
import re
import re as _re
THROW_RE=_re.compile(r"function throwingMessageError\(\): Error \{\n  const e = new Error\('ks1868 hidden'\);\n  Object\.defineProperty\(e, 'message', \{\n    get\(\) \{\n      throw new Error\('ks1868 message getter'\);\n    \},\n  \}\);\n  return e;\n\}\n\n?")
def drop_throwing(t):
    t2,n=THROW_RE.subn('',t)
    assert n==1,n
    return t2
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator79/'
G=O+'gen/'
HELPERS='''
// G105-F1 (gate 105, found again by gate 106's reading of the six guards PR 1925 merged): an Error whose `message` getter RETURNS a hostile non-string. The merged guard
// `reason = error instanceof Error ? error.message : String(error)` returned that object unchanged, so `reason` was the object, and the REAL winston logger (KS-1348 redaction and the dev
// format) throws on it inside logger.error, outside the guard's try: the request got no answer. The cells below send logger.error through the real logger (its transports' output
// swallowed, its formats still run), so that the failure is the real one; the ordinary-Error control C2 shows the same harness answers normally. The jest.fn logger of the cells above
// cannot reproduce the failure, because it never formats its arguments.
function messageGetterReturningRevokedProxy(): Error {
  const e = new Error('ks1868 hidden');
  Object.defineProperty(e, 'message', {
    get(): unknown {
      return revokedProxy();
    },
  });
  return e;
}

function messageGetterReturningThrowingToJson(): Error {
  const e = new Error('ks1868 hidden');
  Object.defineProperty(e, 'message', {
    get(): unknown {
      return {
        toJSON(): never {
          throw new Error('ks1868 toJSON threw');
        },
      };
    },
  });
  return e;
}

function useRealLogger(): void {
  const real = jest.requireActual('../utils/logger').logger;
  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
    t.log = (_info: unknown, next: () => void) => next();
  });
  mockLoggerError.mockImplementation((...a: unknown[]) => (real.error as (...x: unknown[]) => unknown)(...a));
}

afterEach(() => {
  mockLoggerError.mockReset();
});
'''
CELLS='''
describe.each(ROUTES)('KS-1868 $route catch reads a hostile message safely', (c) => {
  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its own message and the answer is the constant 500`, async () => {
    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
  });

  it(`control ks1868 C2 ${c.route}: an ordinary Error through the real logger gets the constant 500 and its own message is logged`, async () => {
    useRealLogger();
    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: 'ks1868 ordinary' }]]);
  });

  it(`RED ks1868 R1 ${c.route}: an Error whose message getter returns a revoked Proxy gets the constant 500 through the real logger`, async () => {
    useRealLogger();
    const reply = await callWithThrow(c, messageGetterReturningRevokedProxy());
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: UNREADABLE }]]);
  });

  it(`RED ks1868 R2 ${c.route}: an Error whose message getter returns an object with a throwing toJSON gets the constant 500 through the real logger`, async () => {
    useRealLogger();
    const reply = await callWithThrow(c, messageGetterReturningThrowingToJson());
    expect(reply).toEqual({ status: 500, body: c.constant });
    expect(mockLoggerError.mock.calls).toEqual([[c.context, { error: '[object Object]' }]]);
  });
});
'''
def build(ref, header, out, routes_sub=None):
    s=open(O+ref,encoding='utf-8').read()
    lines=s.split('\n')
    i=0
    while lines[i].startswith('//'): i+=1
    body='\n'.join(lines[i:])
    j=body.index("describe.each(ROUTES)")
    pre=drop_throwing(body[:j].rstrip('\n')+'\n')
    if routes_sub:
        for a,b in routes_sub:
            assert pre.count(a)==1,a
            pre=pre.replace(a,b)
    txt=header.rstrip('\n')+'\n'+pre+HELPERS+CELLS
    open(G+out,'w',encoding='utf-8').write(txt)
    print(out,len(txt.split('\n')))
H1='''// KS-1868 (originate routes/verification.ts, POST /api/verification/verify, POST /api/verification/hash and GET /api/verification/status/:documentId, follow-up of the guards PR 1925 merged): each route
// catch reads the thrown value as `error instanceof Error ? error.message : String(error)` inside its own try and falls back to the constant `unreadable thrown value` when that throws. That
// expression does not coerce `message`: for an Error whose `message` getter RETURNS a hostile non-string (a revoked Proxy; an object whose toJSON throws) `reason` is that object, and the REAL
// winston logger throws on it inside logger.error, outside the try, so the request gets NO answer. The guard now wraps the same expression in String(...) (the form PR 1924 merged in
// routes/certifications.ts), so a value String() cannot read lands in the fallback and an object becomes its string form. A request-side hook makes the handler throw the chosen value from inside its own
// try, on a real loopback listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.'''
H2='''// KS-1868 (originate routes/verification.ts, POST /api/verification/verify-file, follow-up of the guard PR 1925 merged): the route catch reads the thrown value as `error instanceof Error ? error.message : String(error)`
// inside its own try and falls back to the constant `unreadable thrown value` when that throws. That expression does not coerce `message`: for an Error whose `message` getter RETURNS a hostile
// non-string (a revoked Proxy; an object whose toJSON throws) `reason` is that object, and the REAL winston logger throws on it inside logger.error, outside the try, so the request gets NO answer.
// The guard now wraps the same expression in String(...) (the form PR 1924 merged in routes/certifications.ts). A request-side hook makes the handler throw the chosen value from inside its own try, on a real
// loopback listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.'''
build('ref_ks1868-verification-verify-hash-status-route-catches-p1-unreadable-throw.ts',H1,'t79_b1.ts.txt')
build('ref_ks1868-verification-verify-file-route-catch-p2-unreadable-throw.ts',H2,'t79_b2.ts.txt')

H3='''// KS-1868 (originate routes/verificationV2.ts, POST /api/v2/verification/verify and POST /api/v2/verification/verify-file, follow-up of the guards PR 1925 merged): both route catches read the thrown value as
// `error instanceof Error ? error.message : String(error)` inside their own try and fall back to the constant `unreadable thrown value` when that throws. That expression does not coerce `message`: for an
// Error whose `message` getter RETURNS a hostile non-string (a revoked Proxy; an object whose toJSON throws) `reason` is that object, and the REAL winston logger throws on it inside logger.error, outside the
// try, so the request gets NO answer. Both guards now wrap the same expression in String(...) (the form PR 1924 merged in routes/certifications.ts). The database stand-in rejects with the thrown value on a
// real loopback listener; a request that gets no answer within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run.'''
build('ref_ks1868-verification-v2-route-catches-p1-unreadable-throw.ts',H3,'t79_b3.ts.txt')

# b4: retention scheduler
s=open(O+'ref_ks1868-retention-scheduler-run-enforcement-p3-unreadable-throw.ts',encoding='utf-8').read()
lines=s.split('\n'); i=0
while lines[i].startswith('//'): i+=1
body='\n'.join(lines[i:])
j=body.index("describe('KS-1868 retention scheduler")
pre=drop_throwing(body[:j].rstrip('\n')+'\n')
H4='''// KS-1868 (originate services/retentionScheduler.ts, runEnforcement, follow-up of the guard PR 1923 merged): the scheduled data-retention run catches a failure of `enforceRetention()` and reads it as
// `err instanceof Error ? err.message : String(err)` inside its own try, with the constant `unreadable thrown value` when that throws. That expression does not coerce `message`: for an Error whose `message` getter
// RETURNS a hostile non-string (a revoked Proxy; an object whose toJSON throws) `reason` is that object, and the REAL winston logger throws on it inside logger.error, outside the try, so the run's promise
// rejects with nothing logged (the timer callbacks do not await or catch it: an unhandled rejection). The guard now wraps the same expression in String(...) (the form PR 1924 merged in routes/certifications.ts), so a
// value String() cannot read lands in the fallback and an object becomes its string form. Nothing about WHEN or WHETHER enforcement runs changes. runEnforcement is module-private, so the cells start the scheduler
// with a 10 ms startup delay under fake timers (setImmediate stays real so a pending rejection surfaces inside the cell that caused it) and let the first scheduled run fire. The cells that name the real logger send
// logger.error through it (its transports' output swallowed, its formats still run); the jest.fn logger of the other cells cannot reproduce the failure, because it never formats its arguments.'''
CELLS4='''
function messageGetterReturningRevokedProxy(): Error {
  const e = new Error('ks1868 hidden');
  Object.defineProperty(e, 'message', {
    get(): unknown {
      return revokedProxy();
    },
  });
  return e;
}

function messageGetterReturningThrowingToJson(): Error {
  const e = new Error('ks1868 hidden');
  Object.defineProperty(e, 'message', {
    get(): unknown {
      return {
        toJSON(): never {
          throw new Error('ks1868 toJSON threw');
        },
      };
    },
  });
  return e;
}

function useRealLogger(): void {
  const real = jest.requireActual('../utils/logger').logger;
  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
    t.log = (_info: unknown, next: () => void) => next();
  });
  mockLoggerError.mockImplementation((...a: unknown[]) => (real.error as (...x: unknown[]) => unknown)(...a));
}

// The logged value must already be a string when the logger is called (a typeof check, so that a hostile object is never printed by the assertion itself).
const loggedTypes = (): string[] => mockLoggerError.mock.calls.map((c) => typeof (c[1] as { error?: unknown }).error);

describe('KS-1868 retention scheduler reads a hostile message safely', () => {
  afterEach(() => {
    mockLoggerError.mockReset();
  });

  it('control ks1868 C1 runEnforcement: an ordinary Error logs its own message', async () => {
    await runWithThrow(new Error('ks1868 ordinary'));
    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: 'ks1868 ordinary' }]]);
  });

  it('control ks1868 C2 runEnforcement: an ordinary Error through the real logger logs its own message', async () => {
    useRealLogger();
    await runWithThrow(new Error('ks1868 ordinary'));
    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
    expect(loggedTypes()).toEqual(['string']);
    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: 'ks1868 ordinary' }]]);
  });

  it('RED ks1868 R1 runEnforcement: an Error whose message getter returns a revoked Proxy is logged as the constant reason through the real logger', async () => {
    useRealLogger();
    await runWithThrow(messageGetterReturningRevokedProxy());
    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
    expect(loggedTypes()).toEqual(['string']);
    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: 'unreadable thrown value' }]]);
  });

  it('RED ks1868 R2 runEnforcement: an Error whose message getter returns an object with a throwing toJSON is logged as its string form through the real logger', async () => {
    useRealLogger();
    await runWithThrow(messageGetterReturningThrowingToJson());
    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
    expect(loggedTypes()).toEqual(['string']);
    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: '[object Object]' }]]);
  });
});
'''
txt=H4.rstrip('\n')+'\n'+pre+CELLS4
open(G+'t79_b4.ts.txt','w',encoding='utf-8').write(txt); print('b4',len(txt.split('\n')))
