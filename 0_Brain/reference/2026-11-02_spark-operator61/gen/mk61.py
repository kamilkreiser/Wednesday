# Operator 61: KS-1868 analytics routes/analytics.ts nine Zod-preceded catches, 3 passes x 3 sites (code_patch2).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
SV='Blockchain/Dev/services/analytics/'
PROD=SV+'src/routes/analytics.ts'
TD=SV+'src/__tests__/'
REF=TD+'ks1868-export-service-db-save-unreadable-throw.test.ts'
E="error instanceof Error ? error.message : String(error)"
IFL="    if (error instanceof z.ZodError) {\n"
DET="details: error.errors"
CATCHL="  } catch (error) {\n"
NEWHEAD=("  } catch (thrown) {\n"
"    let error: unknown = thrown;\n"
"    try {\n"
"      if (!(thrown instanceof z.ZodError)) {\n"
"        String(thrown instanceof Error ? thrown.message : thrown);\n"
"      }\n"
"    } catch {\n"
"      error = new Error('unreadable thrown value');\n"
"    }\n")
# route, service object, method, log text, 500 text, 400 text, req literal
S={
 'overview':('GET /overview','analyticsService','getPlatformOverview','Error fetching overview','Failed to fetch overview metrics','Invalid query parameters','{ query: {} }'),
 'certifications':('GET /certifications','analyticsService','getCertificationMetrics','Error fetching certification metrics','Failed to fetch certification metrics','Invalid query parameters','{ query: {} }'),
 'verifications':('GET /verifications','analyticsService','getVerificationMetrics','Error fetching verification metrics','Failed to fetch verification metrics','Invalid query parameters','{ query: {} }'),
 'governance':('GET /governance','analyticsService','getGovernanceMetrics','Error fetching governance metrics','Failed to fetch governance metrics','Invalid query parameters','{ query: {} }'),
 'revenue':('GET /revenue','analyticsService','getRevenueMetrics','Error fetching revenue metrics','Failed to fetch revenue metrics','Invalid query parameters','{ query: {} }'),
 'users':('GET /users','analyticsService','getUserMetrics','Error fetching user metrics','Failed to fetch user metrics','Invalid query parameters','{ query: {} }'),
 'activity':('GET /activity','analyticsService','getActivityFeed','Error fetching activity','Failed to fetch activity feed','Invalid query parameters','{ query: {} }'),
 'exports':('POST /exports','exportService','createExport','Error creating export','Failed to create export','Invalid export request','{ body: {} }'),
 'reports':('POST /reports','exportService','generateReport','Error generating report','Failed to generate report','Invalid report request','{ body: {} }'),
}
P={'p1':['overview','certifications','verifications'],'p2':['governance','revenue','users'],'p3':['activity','exports','reports']}
LABEL={'p1':'overview, certifications and verifications','p2':'governance, revenue and users','p3':'activity, POST exports and POST reports'}
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 21 open PRs read 2026-11-02 through the GitHub API; 119 file entries; services/analytics appears only as package.json / package-lock.json in PRs 575, 649, 948 and 1360; planted positive control: the same scan finds services/originate in 6 entries)."


import subprocess, re, tempfile
SCR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/67d2d8aa-3620-4c8c-99c3-e332209d1f85/scratchpad/'
def pdiff(path,old,new):
    # patience diff (aligns the unchanged 400 block); same header/trim as mk.udiff
    os.makedirs(SCR,exist_ok=True)
    open(SCR+'o61_old.ts','w',encoding='utf-8').write(old); open(SCR+'o61_new.ts','w',encoding='utf-8').write(new)
    r=subprocess.run(['git','diff','--no-index','--patience','-U3','--no-color',SCR+'o61_old.ts',SCR+'o61_new.ts'],capture_output=True)
    lines=r.stdout.decode('utf-8').splitlines(keepends=True)
    i=[k for k,l in enumerate(lines) if l.startswith('@@')][0]
    body=[re.sub(r'^(@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@).*$',r'\1',l.rstrip('\n'))+'\n' if l.startswith('@@') else l for l in lines[i:] if not l.startswith('\\')]
    return f'diff --git a/{path} b/{path}\n--- a/{path}\n+++ b/{path}\n'+''.join(mk.trim(body))

def mkedit(old, key):
    route,so,meth,logm,ans,bad,req=S[key]
    logold="    logger.error('%s', { error: %s });\n"%(logm,E)
    assert old.count(logold)==1,(key,old.count(logold))
    li=old.index(logold)
    ci=old.rindex(CATCHL,0,li)
    assert old[ci+len(CATCHL):].startswith(IFL),key
    return old[:ci]+NEWHEAD+old[ci+len(CATCHL):]

def testbody(k):
    sites=[S[x] for x in P[k]]
    meths={'analyticsService':[],'exportService':[]}
    for s in sites: meths[s[1]].append(s[2])
    svc=''
    for so in ('analyticsService','exportService'):
        if meths[so]:
            svc+="vi.mock('../services/%s', () => ({\n  %s: {\n"%(so,so)+''.join("    %s: () => Promise.reject(ks.toThrow),\n"%m for m in meths[so])+"  },\n}));\n"
    cases=''.join("  { route: '%s', req: %s, logMsg: '%s', answer: '%s', bad: '%s' },\n"%(s[0],s[6],s[3],s[4],s[5]) for s in sites)
    return f"""/**
 * KS-1868: the three analytics route catches below ({LABEL[k]}) each test `error instanceof z.ZodError` first and then read the caught value
 * with `error instanceof Error ? error.message : String(error)` for a `logger.error` line. Both reads can themselves throw (a revoked Proxy throws
 * on `instanceof`; an Error whose `message` getter throws throws on `.message`), and inside an async Express 4 handler the rejection is not caught:
 * the request gets no response and Node sees an unhandled rejection. Each catch now probes both reads inside its own try: an unreadable value is
 * replaced by an ordinary Error and so is logged as the constant `unreadable thrown value` and the route answers the same constant 500 as for any ordinary Error. An ordinary ZodError
 * still answers 400 with `details` equal to its `errors`, and an ordinary Error still logs its own message and answers the constant 500.
 *
 * `express`, the request schemas, the service and the logger are replaced and the route handlers are captured and called directly with a fake
 * request and response: no port is bound, no database is touched. The stand-ins that reject with the thrown value are plain functions, not vi.fn():
 * a spy inspects what it rejects with and could itself fail on a revoked Proxy before the code under test saw it.
 */
import {{ describe, it, expect, vi, beforeAll, beforeEach }} from 'vitest';
import {{ z }} from 'zod';

const ks = vi.hoisted(() => ({{
  routes: {{}} as Record<string, (req: unknown, res: unknown) => Promise<void>>,
  toThrow: undefined as unknown,
  error: vi.fn(),
}}));

vi.mock('express', () => {{
  const router = {{
    get: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {{
      ks.routes['GET ' + p] = f;
    }},
    post: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {{
      ks.routes['POST ' + p] = f;
    }},
  }};
  return {{ Router: () => router, default: {{ Router: () => router }} }};
}});
vi.mock('../types/analytics.types', () => {{
  const passThrough = {{ parse: (v: unknown) => v }};
  return {{
    AnalyticsQuerySchema: passThrough,
    ActivityQuerySchema: passThrough,
    ExportRequestSchema: passThrough,
    ReportRequestSchema: passThrough,
  }};
}});
{svc}vi.mock('../utils/logger', () => ({{
  logger: {{ info: vi.fn(), warn: vi.fn(), debug: vi.fn(), error: ks.error }},
}}));

type Res61 = {{
  statusCode: number;
  body: unknown;
  status(c: number): Res61;
  json(b: unknown): Res61;
}};

function mkRes(): Res61 {{
  const r: Res61 = {{
    statusCode: 200,
    body: undefined,
    status(c) {{
      r.statusCode = c;
      return r;
    }},
    json(b) {{
      r.body = b;
      return r;
    }},
  }};
  return r;
}}

type Case61 = {{ route: string; req: unknown; logMsg: string; answer: string; bad: string }};

const CASES61: Case61[] = [
{cases}];

const ERRS61 = (msg: string) => ks.error.mock.calls.filter((c) => c[0] === msg);

/** Run one route handler with the service call rejecting with `value`. A handler that rejects (the defect) leaves the response untouched at 200. */
async function invoke(c: Case61, value: unknown): Promise<Res61> {{
  ks.toThrow = value;
  const res = mkRes();
  await ks.routes[c.route](c.req, res).catch(() => undefined);
  return res;
}}

beforeAll(async () => {{
  await import('../routes/analytics');
}});

beforeEach(() => {{
  ks.toThrow = undefined;
  ks.error.mockReset();
}});

describe.each(CASES61)('KS-1868 analytics $route catch reads the thrown value safely', (c) => {{
  const body500 = (m: string) => ({{ success: false, error: {{ code: 'INTERNAL_ERROR', message: m }} }});

  it(`RED ks1868 R1 ${{c.route}}: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500`, async () => {{
    const {{ proxy, revoke }} = Proxy.revocable({{}}, {{}});
    revoke();
    const res = await invoke(c, proxy);
    expect(res.statusCode).toBe(500);
    expect(res.body).toEqual(body500(c.answer));
    expect(ERRS61(c.logMsg)).toHaveLength(1);
    expect(ERRS61(c.logMsg)[0][1]).toEqual({{ error: 'unreadable thrown value' }});
  }});

  it(`RED ks1868 R2 ${{c.route}}: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500`, async () => {{
    const getterThrows = Object.create(Error.prototype, {{
      message: {{
        get() {{
          throw new Error('getter boom');
        }},
      }},
    }});
    const res = await invoke(c, getterThrows);
    expect(res.statusCode).toBe(500);
    expect(res.body).toEqual(body500(c.answer));
    expect(ERRS61(c.logMsg)).toHaveLength(1);
    expect(ERRS61(c.logMsg)[0][1]).toEqual({{ error: 'unreadable thrown value' }});
  }});

  it(`control ks1868 C1 ${{c.route}}: an ordinary ZodError answers 400 with details equal to its errors and logs nothing`, async () => {{
    const zerr = new z.ZodError([{{ code: 'custom', path: ['limit'], message: 'ks1868 control issue' }}]);
    const res = await invoke(c, zerr);
    expect(res.statusCode).toBe(400);
    expect(res.body).toEqual({{
      success: false,
      error: {{ code: 'BAD_REQUEST', message: c.bad, details: zerr.errors }},
    }});
    expect(ks.error).not.toHaveBeenCalled();
  }});

  it(`control ks1868 C2 ${{c.route}}: an ordinary Error logs its message and the answer is the constant 500 without it`, async () => {{
    const res = await invoke(c, new Error('ordinary boom 10.0.0.7'));
    expect(res.statusCode).toBe(500);
    expect(res.body).toEqual(body500(c.answer));
    expect(JSON.stringify(res.body)).not.toContain('ordinary boom');
    expect(ERRS61(c.logMsg)).toHaveLength(1);
    expect(ERRS61(c.logMsg)[0][1]).toEqual({{ error: 'ordinary boom 10.0.0.7' }});
  }});
}});
"""

def build(k):
    sites=P[k]; n=len(sites)
    test=TD+'ks1868-analytics-routes-zod-catches-%s-unreadable-throw.test.ts'%k
    old=mk.rd(PROD); new=old
    for s in sites: new=mkedit(new,s)
    pd=pdiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    hl=[l for l in pd.splitlines() if l.startswith('@@ ')]
    assert len(hl)==3,(k,hl)
    tbody=testbody(k)
    td=mk.udiff(test,'',tbody,True); nlines=len(tbody.splitlines())
    open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator61/gen/t61_%s.ts.txt'%k,'w',encoding='utf-8').write(tbody)
    golden=pd+td
    d=BR+'ks_1868_o61_%s_analytics_routes_zod_precheck_catches_%s_unreadable_throw'%(k,'_'.join(sites))
    os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    first=0; cur=None
    for l in pd.splitlines():
        if l.startswith('@@ '):
            cur=int(l.split()[1].split(',')[0][1:]); continue
        if cur is None: continue
        if l.startswith('-') and not l.startswith('---'): first=cur; break
        if l.startswith(' '): cur+=1
    assert first
    pins=("# code_patch2: analytics routes/analytics.ts (3 hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/analytics_src/routes/analytics.ts_and_src/__tests__/_are_in_no_open_PR_(21_PRs_119_files_read_2026-11-02_by_op61,_analytics_only_as_package.json/package-lock.json_in_575/649/948/1360,_positive_control_services/originate_in_6_entries);_live_lanes_beyond_PRs_not_checked\n")%(REF,first)
    open(d+'/spark.pins','w').write(pins)
    tp=test.split('/')[-1]
    rt=[S[x][0] for x in sites]
    lines=', '.join(str(int(l.split()[1].split(',')[0][1:])) for l in hl)
    txt=f"""# KS-1868 analytics: the Zod-preceded catches of {LABEL[k]} must still answer when the thrown value cannot be read (RUNG 3, code_patch2: 3 product hunks given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 61 for Wednesday, 2026-11-02. Secuura (analytics) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {n} catch blocks in ONE file, inline, with no shared helper: {', '.join(rt)}. {OPEN_PR} This is pass O61-{k.upper()} of three on this file (the other six Zod-preceded catches are in the other two passes; the three catches without a Zod branch are held separately by another operator and are NOT touched here).

File: `{PROD}`  (product, modified in place: EXACTLY 3 hunks, one per catch block)
Test file: `{test}`  (NEW file, vitest, given in full below; 12 cells: 3 routes x (R1, R2, C1, C2))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/analytics`)
Tier: `code_patch2`
Rung: **3 (3 product hunks, skeletons dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the 3 hunks under "The exact change", in that order, byte for byte.
2. `{test}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

In `routes/analytics.ts` each of these catch blocks starts with `if (error instanceof z.ZodError) {{ ...400 with details: error.errors... }}` and then has ONE line that reads the caught value: `logger.error('<text>', {{ error: error instanceof Error ? error.message : String(error) }});`, followed by the CONSTANT 500 body `{{ success: false, error: {{ code: 'INTERNAL_ERROR', message: '<fixed text>' }} }}`; the message is only logged. If the awaited service call rejects with a revoked Proxy, `error instanceof z.ZodError` itself throws a TypeError (`instanceof` reads the prototype) before anything else; if it rejects with an Error whose `message` getter throws, `error.message` throws. Either way the catch throws before anything is logged and before the 500 is sent; the async handler rejects, Express 4 does not catch that, and the request gets no response (the gateway proxy times out). The fix renames the catch parameter to `thrown`, adds `let error: unknown = thrown;` as the first line, and then probes the two reads inside one `try`: `if (!(thrown instanceof z.ZodError)) {{ String(thrown instanceof Error ? thrown.message : thrown); }}`. If the probe throws, `error` is replaced by `new Error('unreadable thrown value')`, an ordinary Error. Every line after that (the `if (error instanceof z.ZodError)` branch with `details: error.errors`, the `logger.error` line and the 500) is left BYTE-FOR-BYTE as it is, so the code that runs for an ordinary ZodError, an ordinary Error or a string is the code that runs today; only an unreadable value changes (from "the catch throws, no response" to logging the constant `unreadable thrown value` and the constant 500 an ordinary Error gets). The log message text and the 500 body are untouched. The same constant text (`'unreadable thrown value'`) is the one already merged in this service (exportService.ts, analyticsService.ts, metricsCollector.ts, scheduledJobs.ts); no helper is added. 

## Where

`{PROD}`: the catch blocks of {', '.join(rt)} (hunks begin at old lines {lines}). CALLERS (git grep at the tip): the router is mounted at `/api/analytics` in analytics `src/index.ts` (:78) and reached over HTTP through the api-gateway proxy; no in-process caller. **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable thrown value from the service call or the request parsing: today the catch itself throws, the request gets NO response and Node sees an unhandled rejection; after, the constant reason is logged and the route answers its existing constant 500, exactly what an ordinary Error already gets (cells R1/R2 against control C2). (2) Ordinary ZodError: unchanged 400 and body (control C1). (3) Persisted state: the POST routes create an export or a report only inside the awaited service call; nothing in the catch writes, so nothing persisted changes.

## The exact change

EXACTLY 3 hunks in the product file, in this order. The file header lines and every `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only; a context line that is blank in the file may hold four spaces: keep exactly what is shown). The log message text (the string literal before `, `) is unchanged. **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it.

## The test

File: `{test}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (a vitest file that replaces the module's collaborators with plain functions and a spy logger). `express` (a `Router` whose `get` and `post` capture the handlers), the request schemas in `../types/analytics.types` (pass-through `parse`), the service in `../services/...` (each method rejects with the value the cell sets) and `../utils/logger` (`error` is a spy recording the call) are replaced; the captured handler is called with a fake request and response, no port is bound, no database is touched. The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells

- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route (6 cells). At the tip the handler rejects instead of answering, so the response stays at the default 200 and the status assertion fails; after the edit the constant `unreadable thrown value` is logged and the 500 is sent.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `z.ZodError` answers 400 with `details` equal to `zerr.errors`, the exact body, and nothing is logged) and 'control ks1868 C2' (an ordinary `Error` logs its own message under the existing `logger.error` text and the answer is the constant 500 without it), once per route (6 cells).
- The stand-ins rejecting with the thrown value are plain functions, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` at the tip (read whole with `git show` at `{TIP[:12]}`): every catch named above starts `if (error instanceof z.ZodError)` and has the one `instanceof Error` log line.
- Open PRs: 21 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (119 file entries; services/analytics only as package.json / package-lock.json in PRs 575, 649, 948 and 1360); the positive control services/originate appears in 6 file entries.
- No existing analytics test imports `routes/analytics.ts` or pins its 400 `details` (git grep at the tip: the two ks1364 tests read the schemas and the OpenAPI document only; they cite the route in comments). So control C1 is the first pin of the `details: error.errors` body.
- The pinned ref `ks1868-export-service-db-save-unreadable-throw.test.ts` (merged KS-1868 analytics test) runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. A ZodError subclass whose own `errors` getter throws is not handled (the 400 branch still reads `zodError.errors` as today). Whether a real path throws an unreadable value here is not known (KS-1868 says the same). The service boot path, a real Postgres and a real Express 4 were not run.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
