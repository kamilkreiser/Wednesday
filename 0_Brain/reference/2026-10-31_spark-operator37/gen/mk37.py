# Operator 37 brief generator. Reuses spark/gen/mk.py (rd, udiff) for the diffs; the prose follows the o36 brief.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='cb2320368ae42fa793d81776fdd7fc8404ce312d'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
SVC='Blockchain/Dev/services/'
FALL="'unreadable thrown value'"

TASKS={}
# ---------------- P1: analytics AnalyticsService.loadFromDb ----------------
P1_PROD=SVC+'analytics/src/services/analyticsService.ts'
P1_TEST=SVC+'analytics/src/__tests__/ks1868-analytics-service-load-unreadable-throw.test.ts'
P1_OLD="""    } catch (err) {
      logger.warn('AnalyticsService.loadFromDb failed — using mock data', {
        error: err instanceof Error ? err.message : String(err),
      });"""
P1_NEW="""    } catch (err) {
      let reason: string;
      try {
        reason = err instanceof Error ? err.message : String(err);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('AnalyticsService.loadFromDb failed — using mock data', {
        error: reason,
      });"""
P1_T="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: AnalyticsService.loadFromDb must still log its WARN when the thrown value
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

import { AnalyticsService } from '../services/analyticsService';

const WARNS = () => h.warn.mock.calls.filter((c) => String(c[0]).includes('AnalyticsService.loadFromDb failed'));

describe('KS-1868 AnalyticsService.loadFromDb reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.warn.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message', async () => {
    h.toThrow = new Error('db down');
    await new AnalyticsService().loadFromDb();
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    await new AnalyticsService().loadFromDb().catch(() => undefined);
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
    await new AnalyticsService().loadFromDb().catch(() => undefined);
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""
TASKS['p1']=dict(
 dir='ks_1868_o37_p1_analytics_analyticsservice_loadfromdb_unreadable_throw',
 prod=P1_PROD, test=P1_TEST, old=P1_OLD, new=P1_NEW, tbody=P1_T,
 svc='analytics', where_line=568, catch_start=566,
 fn='AnalyticsService.loadFromDb', file='analyticsService.ts',
 runner_dir='Blockchain/Dev/services/analytics',
 ref=SVC+'vc-issuer/src/__tests__/ks1295-store-db-unavailable-warn.test.ts',
 whatwrong=("In `analyticsService.ts` the catch block of `AnalyticsService.loadFromDb` (starts at line 566) logs "
  "`logger.warn('AnalyticsService.loadFromDb failed — using mock data', { error: err instanceof Error ? err.message : String(err) })` (the `error:` line is 568). "
  "If the thrown value is a revoked Proxy, `err instanceof Error` itself throws a TypeError (\"Cannot perform 'getPrototypeOf' on a proxy that has been revoked\") inside the catch block; if it is an Error whose `message` getter throws, `err.message` throws. "
  "Either way the WARN is not logged and `loadFromDb` rejects instead of falling back to the mock data. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log line uses `reason`. "
  "Nothing else changes: an ordinary Error still logs `{ error: <its message> }`, and the message text of the WARN is unchanged."),
 consequence="Today a hostile thrown value makes the catch block itself throw, so the WARN line is never logged and the function REJECTS instead of falling back to the mock data it already holds.",
 sibling="`metricsCollector.ts:492` (same service, a different file, held by a separate pass) is NOT in this brief",
 red1="At the tip `loadFromDb()` rejects (each cell swallows that rejection, so the failure is the assertion that exactly one WARN was logged)",
 dbnote="`isDbAvailable` and `query` are both exported by `analytics/src/db.ts`; the mock gives both. `new AnalyticsService()` has no I/O (the constructor only generates in-memory mock activity unless IS_PRODUCTION).")

# ---------------- P2: demo-service GET /scenario/context catch ----------------
P2_PROD=SVC+'demo-service/src/routes/scenario.ts'
P2_TEST=SVC+'demo-service/src/__tests__/ks1868-scenario-context-unreadable-throw.test.ts'
P2_OLD="""  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Failed to get scenario context', { error: message });
"""
P2_NEW="""  } catch (err) {
    let message: string;
    try {
      message = err instanceof Error ? err.message : 'Unknown error';
    } catch {
      message = 'unreadable thrown value';
    }
    logger.error('Failed to get scenario context', { error: message });
"""
P2_T="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: the GET /scenario/context handler must still log and answer its generic 500 when the
// thrown value itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose
// `message` getter throws, throws on `.message`).
// The thrown value is raised by a getter on the fake request (plain code, not a vi.fn()): a spy
// could inspect a revoked Proxy and fail before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  error: vi.fn(),
}));

vi.mock('../utils/logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
}));

import { scenarioRouter } from '../routes/scenario';

type Layer = { route?: { path: string; stack: Array<{ handle: (req: unknown, res: unknown) => unknown }> } };
type Outcome = { threw: boolean; status?: number; body?: unknown };

/** Run the real route handler with a request whose `query` getter throws the value under test. */
async function runHandler(): Promise<Outcome> {
  const layer = (scenarioRouter as unknown as { stack: Layer[] }).stack.find(
    (l) => l.route?.path === '/scenario/context',
  );
  const handle = layer!.route!.stack[0].handle;
  const out: Outcome = { threw: false };
  const res = {
    status(code: number) {
      out.status = code;
      return res;
    },
    json(body: unknown) {
      out.body = body;
      return res;
    },
  };
  const req = {
    get query(): never {
      throw h.toThrow;
    },
  };
  try {
    await handle(req, res);
  } catch {
    out.threw = true;
  }
  return out;
}

const ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to get scenario context'));
const GENERIC = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };

describe('KS-1868 scenario context handler reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.error.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message and answers 500', async () => {
    h.toThrow = new Error('query boom');
    const out = await runHandler();
    expect(out.threw).toBe(false);
    expect(out.status).toBe(500);
    expect(out.body).toEqual(GENERIC);
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'query boom' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and answers 500', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    const out = await runHandler();
    expect(out.threw).toBe(false);
    expect(out.status).toBe(500);
    expect(out.body).toEqual(GENERIC);
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and answers 500', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const out = await runHandler();
    expect(out.threw).toBe(false);
    expect(out.status).toBe(500);
    expect(out.body).toEqual(GENERIC);
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""
TASKS['p2']=dict(
 dir='ks_1868_o37_p2_demo_service_scenario_context_unreadable_throw',
 prod=P2_PROD, test=P2_TEST, old=P2_OLD, new=P2_NEW, tbody=P2_T,
 svc='demo-service', where_line=113, catch_start=112,
 fn='the `GET /scenario/context` handler', file='scenario.ts',
 runner_dir='Blockchain/Dev/services/demo-service',
 ref=SVC+'demo-service/src/__tests__/persona.test.ts',
 whatwrong=("In `scenario.ts` the catch block of the `GET /scenario/context` handler (starts at line 112) computes `const message = err instanceof Error ? err.message : 'Unknown error';` (line 113), logs it with `logger.error('Failed to get scenario context', { error: message })` and answers a generic 500 `{ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } }` (the thrown text is NOT sent to the client). "
  "If the thrown value is a revoked Proxy, `err instanceof Error` itself throws a TypeError (\"Cannot perform 'getPrototypeOf' on a proxy that has been revoked\") inside the catch block; if it is an Error whose `message` getter throws, `err.message` throws. "
  "Either way the error is not logged and the generic 500 is not sent; the handler throws out of its catch. The fix reads the thrown value inside its own inner `try` into `message`, falling back to the constant `unreadable thrown value` (the existing `'Unknown error'` branch for non-Errors is kept). "
  "Nothing else changes: an ordinary Error still logs `{ error: <its message> }` and the client still gets the same generic 500."),
 consequence="Today a hostile thrown value makes the catch block itself throw, so the log line is never written and the generic 500 is never sent.",
 sibling="Other `instanceof Error` sites in `demo-service` (`index.ts`, `persona.ts`, `reset.ts`, `state.ts`, `resetService.ts`) are NOT in this brief",
 red1="At the tip the handler throws out of its catch (`runHandler` records that as `threw: true`, so the failure is the assertion that a 500 was answered)",
 dbnote="The real route handler is taken from `scenarioRouter.stack` (the layer for `/scenario/context`) and called with a fake `req` whose `query` getter throws the value under test and a fake `res` recording `status`/`json`. The logger module is mocked as in `persona.test.ts`.")

def build(k):
    T=TASKS[k]
    old=mk.rd(T['prod']); assert old.count(T['old'])==1
    new=old.replace(T['old'],T['new'])
    pd=mk.udiff(T['prod'],old,new)
    pd_body=pd.split('\n',1)[1]          # drop the `diff --git` line like the o35 briefs
    td=mk.udiff(T['test'],'',T['tbody'],True)
    nlines=len(T['tbody'].splitlines())
    golden=pd+td
    d=BR+T['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    pins=("# code_patch2: %s (1 hunk) + a NEW vitest file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_Backlog;_%s_source_is_in_no_open_PR_(43_PRs_read_2026-10-31_by_op36,_positive_control_services/auth_in_20_lines);_not_in_the_S9_security_brief;_live_lanes_beyond_PRs_not_checked\n")%(T['file'],T['ref'],T['where_line'],T['svc'].replace('-','_'))
    open(d+'/spark.pins','w').write(pins)
    tp=T['test'].split('/')[-1]; pp=T['prod']
    txt=f"""# KS-1868 {T['svc']}: {T['fn']} must still report when the thrown value cannot be read (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW vitest file given whole)

DRAFT by Spark operator 37 for Wednesday, 2026-10-31. Secuura ({T['svc']}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: the catch block of {T['fn']} in `{T['file']}`. {T['consequence']} No open PR touches `{T['svc']}` source of this file (the 43 open PRs read 2026-10-31 through the GitHub API; planted positive control: the same scan finds services/auth in 20 lines of its output).

File: `{pp}`  (product, modified in place: ONE hunk)
Test file: `{T['test']}`  (NEW file, vitest, given in full below; 3 cells (2 red, 1 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `{T['runner_dir']}`)
Tier: `code_patch2`
Rung: **3 (one product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{pp}` - modified in place: EXACTLY the one hunk under "The exact change", byte for byte.
2. `{T['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{T['whatwrong']}

## Where

`{pp}:{T['where_line']}`. The catch block starts at line {T['catch_start']}.

## The exact change

ONE hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The WARN/message text may contain an em dash; copy it unchanged.

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. {T['sibling']}.

## The test

File: `{T['test']}`

The test section is a NEW vitest file given whole. The `+` lines are byte-exact. The shape is copied from `{T['ref']}` (a `vi.hoisted` holder, `vi.mock(...)` of the collaborators, then the import). There is no database, no app boot and no network here.

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws). {T['red1']}; after the edit the result carries the constant `unreadable thrown value`.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `Error` logs/returns its own message), the control showing the normal path is unchanged.
- The stand-in rejecting with the thrown value is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.
- {T['dbnote']}

## Premises (each one measured, with where)

- `{pp}:{T['where_line']}` is the `instanceof Error` read inside the catch block at the tip (read whole with `git show` at `{TIP[:12]}`); the catch block starts at line {T['catch_start']}.
- Open PRs: 43 read 2026-10-31 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{pp}`; the positive control services/auth appears in 20 lines of the scan output.
- The seat brief for the security tickets (S9) names neither this file nor this service.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other 252 sites were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path was not run.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
