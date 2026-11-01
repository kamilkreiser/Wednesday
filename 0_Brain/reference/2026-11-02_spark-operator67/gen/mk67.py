# Operator 67: KS-1868 originate routes/signatories.ts (P1,P2) and routes/thirdPartyVerifiers.ts (P3,P4): String(error) in log-only catches. Jest. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
SV='Blockchain/Dev/services/originate/'
TD=SV+'src/__tests__/'
REF=TD+'ks1133-v2-verify-hash-read-first.test.ts'
UUID1='11111111-1111-4111-8111-111111111111'
def G(ind,expr='String(error)'):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
def site(ind,msg):
    o=' '*ind+"logger.error('%s', { error: String(error) });\n"%msg
    n=G(ind)+' '*ind+"logger.error('%s', { error: reason });\n"%msg
    return (o,n)
OPEN_PR="No open PR touches this file or its `src/__tests__/` neighbours (the 22 open PRs read 2026-11-02 through the GitHub API; 125 file entries; services/originate appears only as package.json and integration tests in PRs 575/949/1726/1790/1792/1794; positive control services/originate present, 6 entries)."
# ---- test generators ----
def head(routerimport, extra_mocks):
    return f"""process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
const mockExecuteRawUnsafe = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({{
  prisma: {{ $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw, $executeRawUnsafe: mockExecuteRawUnsafe }},
}}));

jest.mock('../middleware/auth', () => ({{
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}}));

jest.mock('../utils/logger', () => ({{
  logger: {{ info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() }},
}}));

import express from 'express';
import type {{ AddressInfo }} from 'net';
{routerimport}
"""
def body(mount, router, routes_ts, comment):
    return f"""{comment}
const UNREADABLE = 'unreadable thrown value';
const ACTOR = '{UUID1}';

const body500 = (message: string) => ({{ success: false, error: {{ code: 'INTERNAL_ERROR', message }} }});

{routes_ts}

const app = express();
app.use(express.json());
app.use((req, _res, next) => {{
  (req as any).user = {{ userId: ACTOR, email: 'ks1868@example.test' }};
  next();
}});
app.use('{mount}', {router});
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {{
  await new Promise<void>((resolve) => {{
    server = app.listen(0, '127.0.0.1', () => resolve());
  }});
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
}});
afterAll(() => server?.close());
beforeEach(() => jest.resetAllMocks());

async function callWithThrow(c: (typeof ROUTES)[number], thrown: unknown): Promise<{{ status: number | 'NO ANSWER'; body: unknown }}> {{
  c.db().mockRejectedValueOnce(thrown);
  try {{
    const res = await fetch(baseUrl + '{mount}' + c.path, {{
      method: c.method,
      headers: {{ 'content-type': 'application/json' }},
      body: c.method === 'GET' ? undefined : JSON.stringify(c.payload ?? {{}}),
      signal: AbortSignal.timeout(1500),
    }});
    return {{ status: res.status, body: await res.json() }};
  }} catch {{
    return {{ status: 'NO ANSWER', body: null }};
  }}
}}

function revokedProxy(): object {{
  const {{ proxy, revoke }} = Proxy.revocable({{}}, {{}});
  revoke();
  return proxy;
}}

function throwingMessageError(): Error {{
  const e = new Error('ks1868 hidden');
  Object.defineProperty(e, 'message', {{
    get() {{
      throw new Error('ks1868 message getter');
    }},
  }});
  return e;
}}

describe.each(ROUTES)('KS-1868 $route catch reads the thrown value safely', (c) => {{
  it(`RED ks1868 R1 ${{c.route}}: a revoked Proxy thrown by the database is logged as a constant reason and answered with the constant 500`, async () => {{
    const reply = await callWithThrow(c, revokedProxy());
    expect(reply).toEqual({{ status: 500, body: body500(c.message) }});
    expect(mockLoggerError.mock.calls).toEqual([[c.context, {{ error: UNREADABLE }}]]);
    expect(c.db()).toHaveBeenCalledTimes(1);
  }});

  it(`RED ks1868 R2 ${{c.route}}: an Error whose message getter throws is logged as a constant reason and answered with the constant 500`, async () => {{
    const reply = await callWithThrow(c, throwingMessageError());
    expect(reply).toEqual({{ status: 500, body: body500(c.message) }});
    expect(mockLoggerError.mock.calls).toEqual([[c.context, {{ error: UNREADABLE }}]]);
    expect(c.db()).toHaveBeenCalledTimes(1);
  }});

  it(`control ks1868 C1 ${{c.route}}: an ordinary Error is logged as before (String of the Error) and the answer is the constant 500`, async () => {{
    const reply = await callWithThrow(c, new Error('ks1868 ordinary'));
    expect(reply).toEqual({{ status: 500, body: body500(c.message) }});
    expect(mockLoggerError.mock.calls).toEqual([[c.context, {{ error: 'Error: ks1868 ordinary' }}]]);
    expect(c.db()).toHaveBeenCalledTimes(1);
  }});

  it(`control ks1868 C2 ${{c.route}}: a thrown string is logged as itself, as before`, async () => {{
    const reply = await callWithThrow(c, 'ks1868 plain string');
    expect(reply).toEqual({{ status: 500, body: body500(c.message) }});
    expect(mockLoggerError.mock.calls).toEqual([[c.context, {{ error: 'ks1868 plain string' }}]]);
    expect(c.db()).toHaveBeenCalledTimes(1);
  }});
}});
"""
def routes_ts(rows):
    s="const ROUTES = [\n"
    for (route,method,path,db,ctx,msg,payload) in rows:
        pl=', payload: undefined' if payload is None else ', payload: '+payload
        s+="  {\n    route: '%s',\n    method: '%s',\n    path: '%s',\n    db: () => %s,\n    context: '%s',\n    message: '%s'%s,\n  },\n"%(route,method,path,db,ctx,msg,pl)
    return s+"];\n"
SIG_IMP="import { signatoriesRouter } from '../routes/signatories';"
TPV_IMP="import { thirdPartyVerifiersRouter } from '../routes/thirdPartyVerifiers';"
SIGC="// KS-1868 (originate routes/signatories.ts): the catch blocks of these routes logged `String(error)` themselves and then answered the constant 500. When the thrown value cannot be read\n// (a revoked Proxy; an Error whose `message` getter throws), String() threw INSIDE the catch: the handler's promise rejected and the request got NO answer. Each catch now reads the value\n// inside its own try and logs the constant reason `unreadable thrown value`. The database stand-in rejects with the thrown value on a real loopback listener; a request that gets no answer\n// within the window is reported as the string NO ANSWER, so a hang is a red assertion and not a stuck run."
TPVC=SIGC.replace('signatories.ts','thirdPartyVerifiers.ts')
S={}
S['p1']=dict(dir='ks_1868_o67_p1_originate_signatories_list_check_get_catches_unreadable_throw', prod=SV+'src/routes/signatories.ts',
  edits=[site(6,'Failed to list signatories'),site(6,'Failed to check signatory authorisation'),site(6,'Failed to get signatory')],
  test=TD+'ks1868-signatories-read-routes-p1-unreadable-throw.test.ts',
  tsrc=head(SIG_IMP,'')+body('/api/signatories','signatoriesRouter',routes_ts([
    ('GET /','GET','/?organizationId='+UUID1,'mockQueryRaw','Failed to list signatories','Failed to list signatories',None),
    ('GET /check','GET','/check?organizationId=%s&userId=%s'%(UUID1,UUID1),'mockQueryRaw','Failed to check signatory authorisation','Failed to check authorisation',None),
    ('GET /:id','GET','/'+UUID1,'mockQueryRaw','Failed to get signatory','Failed to get signatory',None)]),SIGC),
  ncells='12 cells: 3 routes x (R1, R2, C1, C2)', nh=3, hunks='3', n_routes=3, lines='181, 236 and 284',
  short='three read-route catch blocks (list, check, get-by-id)',
  fn='the list, check and get-by-id route catches of originate `routes/signatories.ts`',
  routes_txt='GET /api/signatories (list, line 180), GET /api/signatories/check (line 235) and GET /api/signatories/:id (line 283)',
  callers="Read-only routes: each runs one `$queryRaw` and answers rows. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value from the database only, today the catch throws, nothing is logged and the request gets no answer (the handler rejects; the gateway times out); after, the constant reason is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status or log for an ordinary Error or a string changes. Persisted state: none (SELECT only). The /check answer feeds callers deciding whether a user may sign; the 500 body (`authorised` absent) is the same for every thrown value after the change, as it already is for an ordinary Error.")
S['p2']=dict(dir='ks_1868_o67_p2_originate_signatories_patch_revoke_reinstate_catches_unreadable_throw', prod=SV+'src/routes/signatories.ts',
  edits=[site(6,'Failed to update signatory'),site(6,'Failed to revoke signatory'),site(6,'Failed to reinstate signatory')],
  test=TD+'ks1868-signatories-write-routes-p2-unreadable-throw.test.ts',
  tsrc=head(SIG_IMP,'')+body('/api/signatories','signatoriesRouter',routes_ts([
    ('PATCH /:id','PATCH','/'+UUID1,'mockExecuteRawUnsafe','Failed to update signatory','Failed to update signatory',"{ displayName: 'Ks Name' }"),
    ('POST /:id/revoke','POST','/%s/revoke'%UUID1,'mockExecuteRaw','Failed to revoke signatory','Failed to revoke signatory',"{ reason: 'ks1868' }"),
    ('POST /:id/reinstate','POST','/%s/reinstate'%UUID1,'mockExecuteRaw','Failed to reinstate signatory','Failed to reinstate signatory',None)]),SIGC),
  ncells='12 cells: 3 routes x (R1, R2, C1, C2)', nh=3, hunks='3', n_routes=3, lines='357, 415 and 464',
  short='three write-route catch blocks (update, revoke, reinstate)',
  fn='the update (PATCH), revoke and reinstate route catches of originate `routes/signatories.ts`',
  routes_txt='PATCH /api/signatories/:id (line 356), POST /api/signatories/:id/revoke (line 414) and POST /api/signatories/:id/reinstate (line 463)',
  callers="Admin write routes. The catch runs only AFTER the database call rejected, and it only logs and answers: it never retries, rolls back or writes, and it sits after the write, so whether a signatory is updated, revoked or reinstated is decided by the database call alone and is identical before and after. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value from the database only, today the catch throws, nothing is logged and the request gets no answer (the handler rejects; the gateway times out); after, the constant reason is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status or log for an ordinary Error or a string changes. Persisted state: unchanged in every case (the failed statement did not write; the catch writes nothing).")
S['p3']=dict(dir='ks_1868_o67_p3_originate_third_party_verifiers_list_suspend_reinstate_catches_unreadable_throw', prod=SV+'src/routes/thirdPartyVerifiers.ts',
  edits=[site(4,'Failed to list verifiers'),site(6,'Failed to suspend verifier'),site(6,'Failed to reinstate verifier')],
  test=TD+'ks1868-third-party-verifiers-admin-routes-p3-unreadable-throw.test.ts',
  tsrc=head(TPV_IMP,'')+body('/api/third-party-verifiers','thirdPartyVerifiersRouter',routes_ts([
    ('GET /','GET','/','mockQueryRaw','Failed to list verifiers','Failed to list verifiers',None),
    ('POST /:id/suspend','POST','/%s/suspend'%UUID1,'mockExecuteRaw','Failed to suspend verifier','Failed to suspend verifier',"{ reason: 'ks1868' }"),
    ('POST /:id/reinstate','POST','/%s/reinstate'%UUID1,'mockExecuteRaw','Failed to reinstate verifier','Failed to reinstate verifier',None)]),TPVC),
  ncells='12 cells: 3 routes x (R1, R2, C1, C2)', nh=3, hunks='3', n_routes=3, lines='143, 240 and 279',
  short='three admin-route catch blocks (list, suspend, reinstate)',
  fn='the list, suspend and reinstate route catches of originate `routes/thirdPartyVerifiers.ts`',
  routes_txt='GET /api/third-party-verifiers (list, line 142; its catch is at 4-space indent), POST /:id/suspend (line 239) and POST /:id/reinstate (line 278)',
  callers="Admin routes on third-party verifiers (trust records). The catch runs only AFTER the database call rejected, and it only logs and answers: it never retries, rolls back or writes, so whether a verifier is suspended or reinstated is decided by the database call alone and is identical before and after. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value from the database only, today the catch throws, nothing is logged and the request gets no answer (the handler rejects; the gateway times out); after, the constant reason is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status or log for an ordinary Error or a string changes. Persisted state: unchanged in every case. **NOT touched: the /:id/approve catch (line 192), which issues the verifier's API key; key issuance is out of scope, and the /register catch (line 102), where an `error.code` check precedes the String(error).**")
S['p4']=dict(dir='ks_1868_o67_p4_originate_third_party_verifiers_verify_records_catches_unreadable_throw', prod=SV+'src/routes/thirdPartyVerifiers.ts',
  edits=[site(6,'Failed to perform third-party verification'),site(6,'Failed to get verification records')],
  test=TD+'ks1868-third-party-verifiers-verify-routes-p4-unreadable-throw.test.ts',
  tsrc=head(TPV_IMP,'')+body('/api/third-party-verifiers','thirdPartyVerifiersRouter',routes_ts([
    ('POST /verify','POST','/verify','mockQueryRaw','Failed to perform third-party verification','Failed to perform verification',"{ certificationId: 'ks1868-cert', apiKey: 'tpv_ks1868' }"),
    ('GET /:id/records','GET','/%s/records'%UUID1,'mockQueryRaw','Failed to get verification records','Failed to get records',None)]),TPVC),
  ncells='8 cells: 2 routes x (R1, R2, C1, C2)', nh=2, hunks='2', n_routes=2, lines='365 and 397',
  short='two route catch blocks (verify, records)',
  fn='the verify and records route catches of originate `routes/thirdPartyVerifiers.ts`',
  routes_txt='POST /api/third-party-verifiers/verify (line 364) and GET /api/third-party-verifiers/:id/records (line 396)',
  callers="POST /verify authenticates the verifier by API key with one `$queryRaw` (the SELECT is the call the stand-in rejects, so the INSERT of a verification record is never reached in these cells); GET /:id/records is a SELECT. The catch runs only after a database call rejected and only logs and answers; it never writes, so whether a verification record exists is decided by the database call alone and is identical before and after. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value from the database only, today the catch throws, nothing is logged and the request gets no answer (the handler rejects; the gateway times out); after, the constant reason is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status or log for an ordinary Error or a string changes. Persisted state: unchanged in every case. **NOT touched: the /:id/approve catch (line 192), which issues an API key.**")
def build(k):
    X=S[k]; PROD=X['prod']; nr=X['n_routes']
    old=mk.rd(PROD); new=old
    for o,n in X['edits']:
        assert new.count(o)==1,(k,o[:70],new.count(o))
        new=new.replace(o,n)
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    hl=[l for l in pd.splitlines() if l.startswith('@@ ')]
    assert len(hl)==X['nh'],(k,len(hl),hl)
    tbody=X['tsrc']
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    golden=pd+td
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator67/gen/t67_%s.ts.txt'%k,'w').write(tbody)
    first=0; cur=None
    for l in pd.splitlines():
        if l.startswith('@@ '):
            cur=int(l.split()[1].split(',')[0][1:]); continue
        if cur is None: continue
        if l.startswith('-') and not l.startswith('---'): first=cur; break
        if l.startswith(' '): cur+=1
    assert first
    fname=PROD.split('/')[-1]
    pins=("# code_patch2: originate %s (%s hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/originate_%s_and_src/__tests__/_are_in_no_open_PR_(22_PRs_125_files_read_2026-11-02_by_op67,_originate_only_as_package.json_and_3_integration_tests_in_575/949/1726/1790/1792/1794,_positive_control_services/originate_in_6_entries);_live_lanes_beyond_PRs_not_checked\n")%(fname,X['hunks'],REF,first,fname)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    nred=2*nr
    txt=f"""# KS-1868 originate: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunk(s) given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 67 for Wednesday, 2026-11-02. Secuura (originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `String(error)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file (adds the inline `let reason` guard, originate certifications.ts shape; lines {X['lines']}). {OPEN_PR} Other KS-1868 files are separate briefs.

File: `{PROD}`  (product, modified in place: EXACTLY {X['hunks']} hunk(s))
Test file: `{X['test']}`  (NEW file, jest, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `jest` (`npx jest src/__tests__/{tp}` from `Blockchain/Dev/services/originate`)
Tier: `code_patch2`
Rung: **3 ({X['hunks']} product hunk(s), skeletons dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the {X['hunks']} hunk(s) under "The exact change", in that order, byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

In `routes/{fname}` the catch blocks of {X['routes_txt']} each log `logger.error('<context>', {{ error: String(error) }})` and then answer a constant 500. If the database call rejects with a revoked Proxy, or with an Error whose `message` getter throws, `String(error)` itself throws inside the catch; the catch throws, nothing is logged and the request gets no answer. The fix keeps each log line's text and replaces only the value: it first reads the same expression `String(error)` into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `{{ error: reason }}`. The constant 500 answers are untouched. This is the inline guard already merged in originate `routes/certifications.ts` (`let reason: string; try {{ ... }} catch {{ reason = 'unreadable thrown value'; }}`); this file has no helper and none is added.

## Where

`{PROD}`: lines {X['lines']}. {X['callers']}

## The exact change

EXACTLY {X['hunks']} hunk(s) in the product file. The file header lines and every `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any other catch block of the file, any message text, or any other line.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (a jest file that replaces the db, auth and logger modules and drives the router on a loopback listener). `../db` (a `prisma` whose `$queryRaw`, `$executeRaw` and `$executeRawUnsafe` are jest stand-ins; the route's own call is made to reject with the thrown value), `../middleware/auth` (pass-through) and `../utils/logger` are replaced; a small middleware sets `req.user`; the router is mounted on a real loopback listener. The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

Each of the {nred} red cells is named `RED ks1868 R1 <route>` or `RED ks1868 R2 <route>`: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route ({nred} cells).

## Cells and controls

- RED at the tip, GREEN after: the {nred} cells above. At the tip the handler rejects instead of answering, so the request reports `NO ANSWER` after 1.5 seconds and the assertion fails; after the edit the constant reason is logged and the constant 500 answered.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `Error` is logged as `Error: <message>`, as before, and the answer is the constant 500) and 'control ks1868 C2' (a thrown string is logged as itself), once per route ({nred} cells).

## Premises (each one measured, with where)

- `{PROD}` lines {X['lines']} are the `String(error)` reads at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 22 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` (125 file entries; services/originate only as package.json in PRs 575/949/1726 and integration tests in 1790/1792/1794); the positive control services/originate appears in 6 file entries.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). A real Express listener is used; a real Postgres is not.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
