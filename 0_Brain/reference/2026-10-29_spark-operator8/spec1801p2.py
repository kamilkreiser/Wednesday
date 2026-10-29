# KS-1801 p2 (Spark operator 8): the two errorMessageIncludes sites, appended as a new describe block.
import importlib.util, os
_s = importlib.util.spec_from_file_location('s1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec1801p1.py')); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
ANCHOR="  };\n}\n\ndescribe('KS-1780: adminConfig catches answer a hostile thrown value', () => {\n"
BLOCK='''
// KS-1801: the two catches that call errorMessageIncludes (it reads the message only, never `code`) are driven too. Each row names the thrown value that the catch DOES recognise
// (`hit`) and the answer that gives; a hostile value must fall through to the constant 500 like every other catch above.
const DOC_ID = '00000000-0000-4000-8000-000000000001';
const MESSAGE_ROUTES = [
  {
    label: 'POST /document-types', method: 'POST', path: '/document-types', body: JSON.stringify({ name: 'KS-1801 type', code: 'ks1801' }),
    hit: new Error('duplicate key value violates unique constraint "x"'),
    hitAnswer: { status: 409, body: { success: false, error: { code: 'CONFLICT', message: 'Document type code already exists' } } },
  },
  {
    label: 'GET /rights-holders/:id/documents', method: 'GET', path: '/rights-holders/' + DOC_ID + '/documents', body: undefined,
    hit: new Error('relation "documents" does not exist'),
    hitAnswer: { status: 200, body: { success: true, documents: [] } },
  },
] as const;

async function callMessageRoute(route: (typeof MESSAGE_ROUTES)[number], thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
  mockQueryRaw.mockRejectedValueOnce(thrown);
  try {
    const res = await fetch(baseUrl + '/api/admin' + route.path, {
      method: route.method,
      headers: { 'content-type': 'application/json' },
      body: route.body,
      signal: AbortSignal.timeout(1500),
    });
    return { status: res.status, body: await res.json() };
  } catch {
    return { status: 'NO ANSWER', body: null };
  }
}

describe('KS-1801: the errorMessageIncludes catches answer a hostile thrown value', () => {
  it.each(MESSAGE_ROUTES)('RED KS-1801 B1 $label: a revoked Proxy thrown by the query is answered with the constant 500', async (route) => {
    expect(await callMessageRoute(route, revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
  });

  it.each(MESSAGE_ROUTES)('RED KS-1801 B2 $label: an object whose message getter throws is answered with the constant 500', async (route) => {
    expect(await callMessageRoute(route, throwingMessageGetter())).toEqual({ status: 500, body: CONSTANT_BODY });
  });

  it.each(MESSAGE_ROUTES)('control KS-1801 D1 $label: the Error the catch recognises is still answered as before', async (route) => {
    expect(await callMessageRoute(route, route.hit)).toEqual(route.hitAnswer);
  });

  it.each(MESSAGE_ROUTES)('control KS-1801 D2 $label: an ordinary Error is still answered with the constant 500', async (route) => {
    expect(await callMessageRoute(route, new Error('ks1801 ordinary'))).toEqual({ status: 500, body: CONSTANT_BODY });
  });

  it.each(MESSAGE_ROUTES)('control KS-1801 D3 $label: a thrown object with only code 42P01 is NOT recognised here (this catch reads the message only) and gets the constant 500', async (route) => {
    expect(await callMessageRoute(route, { code: '42P01' })).toEqual({ status: 500, body: CONSTANT_BODY });
  });
});
'''
T=dict(_m.T)
T.update(dict(dir='ks_1801_p2',
 title='the KS-1780 hostile-throw cells never drive the two adminConfig catches that call errorMessageIncludes (POST /document-types, GET /rights-holders/:id/documents): add a driven describe block (p2 of 2; RUNG 3, TEST-ONLY: one in-place appended hunk with a planted tamper; the product does not change)',
 intro=_m.T['intro'].replace('p1 here = 9 of those 11 (every GET whose catch calls `isMissingTableError`); the other 2 (the sites that call `errorMessageIncludes`) are the twin brief `ks_1801_p2`.', 'p2 here = the other 2 of those 11 (the sites whose catch calls `errorMessageIncludes`); the other 9 (every GET whose catch calls `isMissingTableError`) are the twin brief `ks_1801_p1`.'),
 ref='Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts',
 tamper_line=134, tamper_from="  try {", tamper_to="  JSON.stringify(err?.message); try {",
 statement_ok="line 134 is the `try {` that opens the body of `errorMessageIncludes` (:133-139); the tamper puts one complete statement in front of it on the same line, which reads `err?.message` OUTSIDE the try; `JSON.stringify(...)` is a call, so no unused-expression error, and the file still compiles; `try {` and its `catch {` stay balanced",
 edit=(ANCHOR, "  };\n}\n"+BLOCK+"\ndescribe('KS-1780: adminConfig catches answer a hostile thrown value', () => {\n"),
 red=['RED KS-1801 B1 POST /document-types:','RED KS-1801 B1 GET /rights-holders/:id/documents:','RED KS-1801 B2 POST /document-types:','RED KS-1801 B2 GET /rights-holders/:id/documents:'],
 nh_txt='1 hunk, a new describe block inserted between throwingMessageGetter (ends :96) and the existing describe (:98)', nh_word='ONE hunk', nh_head='ONE EDIT in the TEST file (one hunk, a block inserted above the existing describe)',
 what_wrong="`ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` drives four routes; `adminConfig.ts` has 15 catch sites that read the thrown value, and 11 of them are covered only by the source-text cell S1. `ks_1801_p1` drives nine of the 11 through the `ROUTES` table. The last two do not fit that table, because they are not 'table missing' catches: they call `errorMessageIncludes(err, ...)` (:133, message only, no `code`), POST `/document-types` (:248, needle `unique constraint`, answers 409) and GET `/rights-holders/:id/documents` (:1589, needle `does not exist`, answers 200 with `documents: []`). The POST also needs a method and a JSON body, which the file's `callWithThrow` (GET only) cannot send. This task INSERTS one new `describe` block (above the existing one, so the hunk has trailing context), with its own two-row table and its own small caller, and touches no existing line. Each row gets two reds (a revoked Proxy and a throwing `message` getter must be answered with the constant 500) and three controls (the Error the catch recognises is still answered as before; an ordinary Error gets the constant 500; a `{code: '42P01'}` object is NOT recognised by these two catches, so it also gets the constant 500). The product is right at the tip.",
 where="- `routes/adminConfig.ts:133-139` - (correct, STAYS) `function errorMessageIncludes(err: any, needle: string): boolean {` / `  try {` (:134, the line the tamper corrupts in the checker's clone) / `    return err?.message?.includes(needle) === true;` / `  } catch {` / `    return false;`.\n- The two sites at e4cd2e1325ba: POST `/document-types` handler :220-252 (the `$queryRaw` INSERT is the first database call, after the `!d.name || !d.code` 400 guard at :221; `if (errorMessageIncludes(err, 'unique constraint'))` at :248 answers 409 `{ success: false, error: { code: 'CONFLICT', message: 'Document type code already exists' } }` at :249); GET `/rights-holders/:id/documents` handler :1563-1593 (`db.$queryRaw` is the only database call; `if (errorMessageIncludes(err, 'does not exist'))` at :1589 answers `{ success: true, documents: [] }` at :1590).\n- Test file: one hunk inserted directly after `throwingMessageGetter()` (its closing lines :95-96 are `  };` / `}`) and before `describe('KS-1780: ...` (:98); it reuses the file's `mockQueryRaw`, `baseUrl`, `CONSTANT_BODY`, `revokedProxy()` and `throwingMessageGetter()` and adds no import.",
 cells="- RED under the tamper: `RED KS-1801 B1 <label>` and `RED KS-1801 B2 <label>` for both rows fail at the `toEqual({ status: 500, ... })` (the tampered helper reads `err?.message` outside its try, the handler rejects, NO ANSWER). Four assertion reds.\n- GREEN at the untouched tip: all ten new cells, and every existing cell. D1 pins the recognised-error answers (409 / 200 empty), D2 the constant 500, D3 that `{code: '42P01'}` is not a match for these two catches.\n- CONTROL under the tamper: D1, D2, D3 and every existing cell stay green (a readable Error or `{code}` object is unaffected); no existing cell calls `errorMessageIncludes`.",
 unmeasured="- The drafter did NOT run jest by hand: the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- Not read: that `express.json()` parses the POST body before the `/document-types` handler (the test mounts `express.json()` at app level, line 58, and the handler reads `req.body` at :219); the control measures it (D1 needs the 409).\n- Not read: whether a lower middleware in `adminConfigRouter` rejects a POST before the handler (the two `use` calls :36-45 are mocked or pass through; the control measures it).\n- `MESSAGE_ROUTES` uses `as const`; `route.hit` and `route.hitAnswer` types are read through it, and whether ts-jest diagnostics are on for this suite is not read.\n- Open PRs touching this test file: not listed here (see the report); the raising seat checks.",
 scope="**Narrowing: drives the last 2 of the 11 S1-only catch sites of KS-1801** (the first 9 are `ks_1801_p1`). The PR links Refs KS-1801, never a close-word, unless p1 has landed. No product file changes.",
))
