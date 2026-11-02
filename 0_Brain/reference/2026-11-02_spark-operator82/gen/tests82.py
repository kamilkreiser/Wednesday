# Operator 82: generate the six new test files (t82_p1..p6.ts.txt) from the merged PR 1931/1932 test harnesses.
import re, os
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator82/gen/'
def ref(n): return open(G+'ref_'+n,encoding='utf-8').read()
HELP_V = """const revokedProxy = (): unknown => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};
const toStringThrows = (): unknown => ({
  toString() {
    throw new Error('ts boom');
  },
});
/** An Error whose `message` getter succeeds and returns the (non-string) value m. */
const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
const reasonOf = (c: unknown[] | undefined): string => {
  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
  return typeof v === 'string' ? v : '<' + typeof v + '>';
};
const SHAPES: Array<[string, () => unknown, string]> = [
  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
  ['an object whose toString throws', toStringThrows, 'unreadable thrown value'],
  ['a null-prototype object', () => Object.create(null), 'unreadable thrown value'],
  ['a Symbol', () => Symbol('ks1868'), 'Symbol(ks1868)'],
];
"""
SHAPES=[('a revoked Proxy',None,'unreadable thrown value'),('an object whose toString throws',None,'unreadable thrown value'),('a null-prototype object',None,'unreadable thrown value'),('a Symbol',None,'Symbol(ks1868)')]
def rcells(label, call_expr, start, vitest=True, extra=''):
    out=''
    for i,(nm,fn,exp) in enumerate(SHAPES):
        out+=f"""  it('RED ks1868 R{start+i} {label}: an Error whose message is {nm} logs {"the constant reason" if exp.startswith("unread") else "the Symbol text"} and the outcome is the ordinary one', async () => {{
    await {call_expr}(withMessage(SHAPES[{i}][1]()), SHAPES[{i}][2]);
  }});

"""
    return out
def swap_comment(txt, newc):
    i=txt.index('// KS-1868:'); j=i
    while txt[j:j+2]=='//':
        j=txt.index('\n',j)+1
    return txt[:i]+newc+txt[j:]
def until(txt, marker): return txt[:txt.index(marker)]

# ---------------- P1 auth.ts rehash + logout
t=ref('ks1868-auth-rehash-and-logout-denylist-unreadable-throw.test.ts')
head=swap_comment(until(t,'const getterThrows'),"""// KS-1868 (QA gate 113, G113-F1): the login UPGRADE-ON-VERIFY rehash catch and the logout denylist `.catch` in routes/auth.ts
// log `{ error: reason }` where `reason` is whatever `err?.message` returned. PR 1931 guards the READ; a message that is
// readable but not a string (a revoked Proxy, an object whose toString throws, a null-prototype object, a Symbol) is passed
// to the logger as is, and the real winston throws while formatting it. The cells reject with an Error whose `message`
// getter RETURNS such a value and assert the logged reason is text (the constant when it cannot be turned into text), with
// the login still 200 with tokens and the logout still 200 with the cookie cleared (the outcome an ordinary Error gets).
// A thrown plain string has no message and is logged with no `error`; that is pinned too. Harness: the ks1868 rehash and
// logout test (real router and error handler; the repository, password, session, jwt, lockout, mail and bus mocked; the
// stand-ins reject with a plain function, not a vi.fn()).
""")
body=HELP_V+"""
describe('KS-1868 the login rehash and logout denylist catches log text for a hostile non-string message', () => {
  it('control ks1868 C1 login: an ordinary Error from the rehash write is logged with its message and the login answers 200 with tokens', async () => {
    h.rehashRejects = true;
    h.toThrow = new Error('db down');
    expect(await login()).toEqual(LOGIN_OK);
    expect(REHASH_LINES()).toHaveLength(1);
    expect(reasonOf(REHASH_LINES()[0])).toBe('db down');
  });

  it('control ks1868 C2 logout: an ordinary Error from the denylist write is logged with its message and the logout answers 200 and clears the cookie', async () => {
    h.denylistRejects = true;
    h.toThrow = new Error('redis down');
    expect(await logout()).toEqual(LOGOUT_OK);
    expect(LOGOUT_LINES()).toHaveLength(1);
    expect(reasonOf(LOGOUT_LINES()[0])).toBe('redis down');
  });

  it('control ks1868 C3 login: a thrown plain string has no message and is logged with no error field (not the text undefined)', async () => {
    h.rehashRejects = true;
    h.toThrow = 'plain boom';
    expect(await login()).toEqual(LOGIN_OK);
    expect(REHASH_LINES()).toHaveLength(1);
    expect(reasonOf(REHASH_LINES()[0])).toBe('<undefined>');
  });

  it('control ks1868 C4 logout: a thrown plain string has no message and is logged with no error field (not the text undefined)', async () => {
    h.denylistRejects = true;
    h.toThrow = 'plain boom';
    expect(await logout()).toEqual(LOGOUT_OK);
    expect(LOGOUT_LINES()).toHaveLength(1);
    expect(reasonOf(LOGOUT_LINES()[0])).toBe('<undefined>');
  });

"""
for i,(nm,fn,exp) in enumerate(SHAPES):
    body+=f"""  it('RED ks1868 R{1+i} login: a rehash rejection whose message is {nm} logs {"the constant reason" if exp.startswith("unread") else "the Symbol text"} and the login answers 200 with tokens', async () => {{
    h.rehashRejects = true;
    h.toThrow = withMessage(SHAPES[{i}][1]());
    expect(await login()).toEqual(LOGIN_OK);
    expect(REHASH_LINES()).toHaveLength(1);
    expect(reasonOf(REHASH_LINES()[0])).toBe(SHAPES[{i}][2]);
  }});

"""
for i,(nm,fn,exp) in enumerate(SHAPES):
    body+=f"""  it('RED ks1868 R{5+i} logout: a denylist rejection whose message is {nm} logs {"the constant reason" if exp.startswith("unread") else "the Symbol text"} and the logout answers 200 and clears the cookie', async () => {{
    h.denylistRejects = true;
    h.toThrow = withMessage(SHAPES[{i}][1]());
    expect(await logout()).toEqual(LOGOUT_OK);
    expect(LOGOUT_LINES()).toHaveLength(1);
    expect(reasonOf(LOGOUT_LINES()[0])).toBe(SHAPES[{i}][2]);
  }});

"""
body=body.rstrip('\n')+'\n});\n'
open(G+'t82_p1.ts.txt','w').write(head+body)


def kind(exp): return "the constant reason" if exp.startswith("unread") else "the Symbol text"
def cells(prefix, label, setup, check, start, outcome):
    """R cells: for each shape, `setup` lines then `check` lines (python format strings with {i})."""
    o=''
    for i,(nm,fn,exp) in enumerate(SHAPES):
        o+=f"  it('RED ks1868 R{start+i} {label}: a rejection whose message is {nm} logs {kind(exp)} and {outcome}', async () => {{\n"
        o+=setup.format(i=i)+check.format(i=i)+"  });\n\n"
    return o
def close(b): return b.rstrip('\n')+'\n});\n'

# ---------------- P2 internal.ts connector-token
t=ref('ks1868-internal-connector-token-unreadable-throw.test.ts')
head=swap_comment(until(t,"describe('KS-1868"),"""// KS-1868 (QA gate 113, G113-F1 and F2): the POST /internal/connector-token catch in routes/internal.ts logs `{ error: reason }`
// where `reason` is whatever `(err as Error).message` returned, then answers the constant 502 BAD_GATEWAY. PR 1931 guards the
// READ; a message that is readable but not a string (a revoked Proxy, an object whose toString throws, a null-prototype object,
// a Symbol) is passed to the logger as is, and the real winston throws while formatting it. The cells make the security call
// reject with an Error whose `message` getter RETURNS such a value and assert the logged reason is text (the constant when it
// cannot be turned into text), the 502, no token and no unhandled rejection (the outcome an ordinary Error gets). Controls pin
// the two shapes no earlier cell pinned: a thrown `undefined` (reading `.message` throws, so the constant) and a thrown plain
// string (no message: logged with no `error` field, not the text undefined). Harness: the ks1868 connector-token test.
""")
head=head.replace("const SAVED_LISTENERS", "const SAVED_LISTENERS",1)
body=HELP_V+"""
const BAD_GATEWAY = { status: 502, code: 'BAD_GATEWAY', minted: false };

describe('KS-1868 the connector-token catch logs text for a hostile non-string message', () => {
  it('control ks1868 C1: an ordinary Error is logged with its message and the route answers 502 BAD_GATEWAY with no token', async () => {
    h.toThrow = new Error('security down');
    expect(await exchange()).toEqual(BAD_GATEWAY);
    expect(h.unhandled).toBe(0);
    expect(LINES()).toHaveLength(1);
    expect(reasonOf(LINES()[0])).toBe('security down');
  });

  it('control ks1868 C2: a thrown undefined makes the message read throw and the constant reason is logged', async () => {
    h.toThrow = undefined;
    expect(await exchange()).toEqual(BAD_GATEWAY);
    expect(h.unhandled).toBe(0);
    expect(LINES()).toHaveLength(1);
    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
  });

  it('control ks1868 C3: a thrown plain string has no message and is logged with no error field (not the text undefined)', async () => {
    h.toThrow = 'plain boom';
    expect(await exchange()).toEqual(BAD_GATEWAY);
    expect(h.unhandled).toBe(0);
    expect(LINES()).toHaveLength(1);
    expect(reasonOf(LINES()[0])).toBe('<undefined>');
  });

"""
body+=cells('p2','',"    h.toThrow = withMessage(SHAPES[{i}][1]());\n","    expect(await exchange()).toEqual(BAD_GATEWAY);\n    expect(h.unhandled).toBe(0);\n    expect(LINES()).toHaveLength(1);\n    expect(reasonOf(LINES()[0])).toBe(SHAPES[{i}][2]);\n",1,'the route answers 502 with no token')
open(G+'t82_p2.ts.txt','w').write(head+close(body))

# ---------------- P3 issuerCerts.ts
t=ref('ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts')
head=swap_comment(until(t,'const getterThrows'),"""// KS-1868 (QA gate 113, G113-F1 and F2): the GET /api/issuer-certs (list) and POST /api/issuer-certs/:id/revoke catches in
// routes/issuerCerts.ts log `{ error: reason }` where `reason` is `err instanceof Error ? err.message : String(err)`. PR 1931 guards
// the READ; an Error whose message is readable but not a string (a revoked Proxy, an object whose toString throws, a null-prototype
// object, a Symbol) passes it to the logger as is, and the real winston throws while formatting it. The cells reject with an Error
// whose `message` getter RETURNS such a value and assert the logged reason is text (the constant when it cannot be turned into
// text), the constant 500, no unhandled rejection, and no event published (the outcome an ordinary Error gets). Controls pin the
// shapes a non-Error gets today: a thrown plain string is logged as its text and a thrown null-prototype object (String() throws)
// logs the constant. Harness: the ks1868 issuer-cert test (real router; repository, auth middleware and bus mocked).
""")
body=HELP_V+"""
describe('KS-1868 the issuer-cert list and revoke catches log text for a hostile non-string message', () => {
  it('control ks1868 C1 list: an ordinary Error is logged with its message and the route answers the constant 500', async () => {
    h.toThrow = new Error('db down');
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe('db down');
  });

  it('control ks1868 C2 revoke: an ordinary Error is logged with its message, the route answers the constant 500 and no event is published', async () => {
    h.toThrow = new Error('db down');
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe('db down');
  });

  it('control ks1868 C3 list: a thrown null-prototype object cannot be turned into text and the constant reason is logged', async () => {
    h.toThrow = Object.create(null);
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe('unreadable thrown value');
  });

  it('control ks1868 C4 revoke: a thrown plain string is logged as its own text', async () => {
    h.toThrow = 'plain boom';
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe('plain boom');
  });

"""
body+=cells('p3','list',"    h.toThrow = withMessage(SHAPES[{i}][1]());\n","    expect(await list()).toEqual(LIST_500);\n    expect(h.unhandled).toBe(0);\n    expect(LIST_LINES()).toHaveLength(1);\n    expect(reasonOf(LIST_LINES()[0])).toBe(SHAPES[{i}][2]);\n",1,'the route answers the constant 500')
body+=cells('p3','revoke',"    h.toThrow = withMessage(SHAPES[{i}][1]());\n","    expect(await revoke()).toEqual(REVOKE_500);\n    expect(h.unhandled).toBe(0);\n    expect(h.published).toBe(0);\n    expect(REVOKE_LINES()).toHaveLength(1);\n    expect(reasonOf(REVOKE_LINES()[0])).toBe(SHAPES[{i}][2]);\n",5,'the route answers the constant 500 with no event')
open(G+'t82_p3.ts.txt','w').write(head+close(body))

# ---------------- P4 oauth.ts
t=ref('ks1868-oauth-authorize-token-unreadable-throw.test.ts')
head=swap_comment(until(t,'const getterThrows'),"""// KS-1868 (QA gate 113, G113-F1 and F2): the POST /api/oauth/authorize and POST /api/oauth/token outer catches in routes/oauth.ts
// log `{ error: reason }` where `reason` is whatever `error.message` returned, then answer the constant 500 `server_error`. PR 1931
// guards the READ; a message that is readable but not a string (a revoked Proxy, an object whose toString throws, a null-prototype
// object, a Symbol) is passed to the logger as is, and the real winston throws while formatting it. The cells make the client app
// lookup reject with an Error whose `message` getter RETURNS such a value and assert the logged reason is text (the constant when
// it cannot be turned into text), the constant 500, no code or session minted and no unhandled rejection (the outcome an ordinary
// Error gets). Controls pin the shapes no earlier cell pinned: a thrown `undefined` (reading `.message` throws, so the constant) and
// a thrown plain string (no message: logged with no `error` field, not the text undefined). Harness: the ks1868 oauth test.
""")
body=HELP_V+"""
describe('KS-1868 the oauth authorize and token catches log text for a hostile non-string message', () => {
  it('control ks1868 C1 authorize: an ordinary Error is logged with its message and the route answers 500 server_error', async () => {
    h.toThrow = new Error('app lookup down');
    expect(await authorizeDeny()).toEqual(SERVER_ERROR);
    expect(h.unhandled).toBe(0);
    expect(AUTHORIZE_LINES()).toHaveLength(1);
    expect(reasonOf(AUTHORIZE_LINES()[0])).toBe('app lookup down');
  });

  it('control ks1868 C2 token: an ordinary Error is logged with its message and the route answers 500 server_error', async () => {
    h.toThrow = new Error('app lookup down');
    expect(await tokenExchange()).toEqual(SERVER_ERROR);
    expect(h.unhandled).toBe(0);
    expect(TOKEN_LINES()).toHaveLength(1);
    expect(reasonOf(TOKEN_LINES()[0])).toBe('app lookup down');
  });

  it('control ks1868 C3 authorize: a thrown undefined makes the message read throw and the constant reason is logged', async () => {
    h.toThrow = undefined;
    expect(await authorizeDeny()).toEqual(SERVER_ERROR);
    expect(h.unhandled).toBe(0);
    expect(AUTHORIZE_LINES()).toHaveLength(1);
    expect(reasonOf(AUTHORIZE_LINES()[0])).toBe('unreadable thrown value');
  });

  it('control ks1868 C4 token: a thrown undefined makes the message read throw and the constant reason is logged', async () => {
    h.toThrow = undefined;
    expect(await tokenExchange()).toEqual(SERVER_ERROR);
    expect(h.unhandled).toBe(0);
    expect(TOKEN_LINES()).toHaveLength(1);
    expect(reasonOf(TOKEN_LINES()[0])).toBe('unreadable thrown value');
  });

  it('control ks1868 C5 token: a thrown plain string has no message and is logged with no error field (not the text undefined)', async () => {
    h.toThrow = 'plain boom';
    expect(await tokenExchange()).toEqual(SERVER_ERROR);
    expect(h.unhandled).toBe(0);
    expect(TOKEN_LINES()).toHaveLength(1);
    expect(reasonOf(TOKEN_LINES()[0])).toBe('<undefined>');
  });

"""
body+=cells('p4','authorize',"    h.toThrow = withMessage(SHAPES[{i}][1]());\n","    expect(await authorizeDeny()).toEqual(SERVER_ERROR);\n    expect(h.unhandled).toBe(0);\n    expect(AUTHORIZE_LINES()).toHaveLength(1);\n    expect(reasonOf(AUTHORIZE_LINES()[0])).toBe(SHAPES[{i}][2]);\n",1,'the route answers 500 server_error')
body+=cells('p4','token',"    h.toThrow = withMessage(SHAPES[{i}][1]());\n","    expect(await tokenExchange()).toEqual(SERVER_ERROR);\n    expect(h.unhandled).toBe(0);\n    expect(TOKEN_LINES()).toHaveLength(1);\n    expect(reasonOf(TOKEN_LINES()[0])).toBe(SHAPES[{i}][2]);\n",5,'the route answers 500 server_error')
open(G+'t82_p4.ts.txt','w').write(head+close(body))
print('ok')

# ---------------- P5 anchoring index.ts
t=ref('ks1868-anchoring-read-route-catches-unreadable-throw.test.ts')
head=swap_comment(until(t,'const revokedProxy'),"""// KS-1868 (QA gate 114, G114-F1): three read-side catches of the anchoring service log `error: <reason>` where `reason` is whatever
// `err?.message` returned. PR 1932 guards the READ; a message that is readable but not a string (a revoked Proxy, an object whose
// toString throws, a null-prototype object, a Symbol) is passed to `log()` as is, and its `JSON.stringify` throws on a revoked
// Proxy inside the catch (the tx route then never answers). Cells: GET /api/anchors/tx/:txHash (`dbGetAnchorByTx` logs and returns
// undefined, 404), GET /api/anchors/verify/:hash (the local lookup logs and falls to the chain step; with no Cardano credentials
// 404) and POST /api/anchors/verify (the content-hash lookup logs, verified false). The cells reject with an Error whose `message`
// getter RETURNS such a value and assert the logged reason is text (the constant when it cannot be turned into text) and the
// answer an ordinary Error gets. Controls pin a thrown plain string (no message: logged with no `error` key, not the text
// undefined). Harness: the ks1868 anchoring read-route test (real index.ts app, real RS256 bearer, `../db` mocked, plain-function
// rejections). Every statement the cells reject is a SELECT: nothing is submitted, signed or written.
""")
helpers=HELP_V.split('/** The logged')[0]+"""/** The logged `error` key of a JSON log line as a string; the type name when it is not one. */
const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? o.error : '<' + typeof o?.error + '>');
const SHAPES: Array<[string, () => unknown, string]> = [
  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
  ['an object whose toString throws', toStringThrows, 'unreadable thrown value'],
  ['a null-prototype object', () => Object.create(null), 'unreadable thrown value'],
  ['a Symbol', () => Symbol('ks1868'), 'Symbol(ks1868)'],
];
"""
mid=t[t.index('const TX_MSG'):t.index('describe(')]
body=helpers+mid+"""
async function tx(thrown: unknown, reason: string): Promise<void> {
  h.toThrow = thrown;
  expectAnswer(await byTx(), 404, TX_ANSWER);
  expect(h.unhandled).toBe(0);
  expect(lines(TX_MSG)).toHaveLength(1);
  expect(reasonOf(lines(TX_MSG)[0])).toBe(reason);
  expect(h.writes).toBe(0);
}
async function hash(thrown: unknown, reason: string): Promise<void> {
  h.toThrow = thrown;
  expectAnswer(await byHash(), 404, HASH_ANSWER);
  expect(h.unhandled).toBe(0);
  expect(lines(HASH_MSG)).toHaveLength(1);
  expect(reasonOf(lines(HASH_MSG)[0])).toBe(reason);
  expect(h.writes).toBe(0);
}
async function verifyHash(thrown: unknown, reason: string): Promise<void> {
  h.toThrow = thrown;
  expectAnswer(await verify(), 200, VERIFY_ANSWER);
  expect(h.unhandled).toBe(0);
  expect(lines(VERIFY_MSG)).toHaveLength(1);
  expect(reasonOf(lines(VERIFY_MSG)[0])).toBe(reason);
  expect(h.writes).toBe(0);
}

describe('KS-1868 the anchoring read-route catches log text for a hostile non-string message', () => {
  it('control ks1868 C1 tx lookup: an ordinary Error is logged with its own message and the route answers 404', async () => {
    await tx(new Error(LOOKUP_DOWN), LOOKUP_DOWN);
  });

  it('control ks1868 C2 verify-by-hash: an ordinary Error is logged with its own message and the chain step answers 404', async () => {
    await hash(new Error(LOOKUP_DOWN), LOOKUP_DOWN);
  });

  it('control ks1868 C3 content-hash verify: an ordinary Error is logged with its own message and the route answers verified false', async () => {
    await verifyHash(new Error(LOOKUP_DOWN), LOOKUP_DOWN);
  });

  it('control ks1868 C4 tx lookup: a thrown plain string has no message and is logged with no error key (not the text undefined)', async () => {
    await tx('plain boom', '<undefined>');
  });

  it('control ks1868 C5 verify-by-hash: a thrown plain string has no message and is logged with no error key (not the text undefined)', async () => {
    await hash('plain boom', '<undefined>');
  });

"""
for start,label,fn in ((1,'tx lookup','tx'),(5,'verify-by-hash','hash'),(9,'content-hash verify','verifyHash')):
    body+=cells('p5',label,"","    await %s(withMessage(SHAPES[{i}][1]()), SHAPES[{i}][2]);\n"%fn,start,'the answer is the ordinary one')
open(G+'t82_p5.ts.txt','w').write(head+close(body))

# ---------------- P6 originate anchors.ts (jest)
t=ref('ks1868-anchors-route-catches-unreadable-throw.test.ts')
head=swap_comment(until(t,'const revokedProxy'),"""// KS-1868 (QA gate 114, G114-F1 and F2): the originate anchor routes log `error: <reason>` in three catches (getAnchorByDocumentId
// warn, the GET /:documentId route catch and verifyAnchorsDbReady) where `reason` is `err instanceof Error ? err.message :
// String(err)`. PR 1932 guards the READ; an Error whose message is readable but not a string (a revoked Proxy, an object whose
// toString throws, a null-prototype object, a Symbol) passes it to the logger as is, and the real winston throws while formatting
// it. The cells reject with an Error whose `message` getter RETURNS such a value and assert the logged reason is text (the
// constant when it cannot be turned into text), the route answers the constant 500 and verifyAnchorsDbReady throws the constant
// error. G114-F2: the GET uses an abort signal (a hang is a null answer, not a jest timeout), unhandled rejections are counted, and
// the rejection of verifyAnchorsDbReady is read through a plain `.then(ok, err)` (no jest matcher touches a hostile value).
// Controls pin a thrown plain string (a non-Error is logged as its own text). Harness: the ks1868 anchors test. Nothing is written.
""")
helpers=HELP_V.split('/** The logged')[0]+"""/** The logged `error` field of a logger call as a string; the type name when it is not one. */
const reasonOf = (c: unknown[] | undefined): string => {
  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
  return typeof v === 'string' ? v : '<' + typeof v + '>';
};
const SHAPES: Array<[string, () => unknown, string]> = [
  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
  ['an object whose toString throws', toStringThrows, 'unreadable thrown value'],
  ['a null-prototype object', () => Object.create(null), 'unreadable thrown value'],
  ['a Symbol', () => Symbol('ks1868'), 'Symbol(ks1868)'],
];

let unhandled = 0;
const onUnhandled = () => {
  unhandled += 1;
};
beforeAll(() => {
  process.on('unhandledRejection', onUnhandled);
});
afterAll(() => {
  process.removeListener('unhandledRejection', onUnhandled);
});
beforeEach(() => {
  unhandled = 0;
});

async function getAnchor(): Promise<{ status: number; code: string | undefined } | null> {
  try {
    const res = await fetch(`${baseUrl}/api/anchors/${DOC}`, { signal: AbortSignal.timeout(1500) });
    const body = (await res.json()) as { error?: { code?: string } };
    return { status: res.status, code: body.error?.code };
  } catch {
    return null;
  }
}
const readyOutcome = (): Promise<string> =>
  verifyAnchorsDbReady().then(
    () => 'resolved',
    (e: unknown) => (e instanceof Error ? e.message : '<non-error>'),
  );
async function route(thrown: unknown, reason: string): Promise<void> {
  mockState.toThrow = thrown;
  expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
  expect(unhandled).toBe(0);
  expect(mockState.warned).toHaveLength(1);
  expect(mockState.warned[0][0]).toBe('Failed to fetch anchor from DB');
  expect(reasonOf(mockState.warned[0])).toBe(reason);
  expect(mockState.errored).toHaveLength(1);
  expect(mockState.errored[0][0]).toBe('Failed to get anchor');
  expect(reasonOf(mockState.errored[0])).toBe(reason);
  expect(mockState.writes).toBe(0);
}
async function ready(thrown: unknown, reason: string): Promise<void> {
  mockState.toThrow = thrown;
  expect(await readyOutcome()).toBe(DB_READY_MESSAGE);
  expect(mockState.errored).toHaveLength(1);
  expect(reasonOf(mockState.errored[0])).toBe(reason);
}

describe('KS-1868 the originate anchor catches log text for a hostile non-string message', () => {
  it('control ks1868 C1 GET /:documentId: an ordinary Error is logged with its own message on both lines and the route answers 500', async () => {
    await route(new Error('Connection terminated unexpectedly'), 'Connection terminated unexpectedly');
  });

  it('control ks1868 C2 verifyAnchorsDbReady: an ordinary Error is logged with its own message and the constant error is thrown', async () => {
    await ready(new Error('db down'), 'db down');
  });

  it('control ks1868 C3 GET /:documentId: a thrown plain string is logged as its own text on both lines and the route answers 500', async () => {
    await route('plain boom', 'plain boom');
  });

  it('control ks1868 C4 verifyAnchorsDbReady: a thrown plain string is logged as its own text and the constant error is thrown', async () => {
    await ready('plain boom', 'plain boom');
  });

"""
body=helpers+"\n"+""
body=body.rstrip('\n')+"\n\n"
# the describe starts after helpers; the body already opened describe in helpers string -> assemble
body2=helpers
for start,label,fn,outc in ((1,'GET /:documentId','route','both lines carry it and the route answers 500'),(5,'verifyAnchorsDbReady','ready','the constant error is thrown')):
    body2+=cells('p6',label,"","    await %s(withMessage(SHAPES[{i}][1]()), SHAPES[{i}][2]);\n"%fn,start,outc)
mid=t[t.index('const DB_READY_MESSAGE') if False else 0:0]
open(G+'t82_p6.ts.txt','w').write(head+close(body2))
print('ok2')
