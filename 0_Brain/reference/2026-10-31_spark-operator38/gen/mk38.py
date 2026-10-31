# Operator 37 brief generator. Reuses spark/gen/mk.py (rd, udiff) for the diffs; the prose follows the o36 brief.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='9e1eb55fde5338d0ad95848736cbd013d7b7f651'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
SVC='Blockchain/Dev/services/'
FALL="'unreadable thrown value'"

TASKS={}
PKG='Blockchain/Dev/packages/shared/'
# ---------------- P1: shared createUnhandledRejectionHandler ----------------
P1_PROD=PKG+'src/utils/gracefulShutdown.ts'
P1_TEST=PKG+'src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts'
P1_OLD="""    const detail =
      reason instanceof Error ? `${reason.message}\\n${reason.stack ?? ''}` : String(reason);
"""
P1_NEW="""    let detail: string;
    try {
      detail = reason instanceof Error
        ? `${reason.message}\\n${reason.stack ?? ''}`
        : String(reason);
    } catch {
      detail = 'unreadable thrown value';
    }
"""
P1_T="""import { describe, it, expect } from 'vitest';
import { createUnhandledRejectionHandler } from '../utils/gracefulShutdown';

// KS-1868: the unhandledRejection handler must still log (and still shut down in 'exit' mode)
// when the rejection reason itself cannot be read (a revoked Proxy throws on `instanceof`; an
// Error whose `message` getter throws, throws on `.message`). Today the handler itself throws,
// which in 'survive' mode (the api-gateway) turns one bad rejection into the outage KS-546 prevents.
// The logger and shutdown stand-ins are plain functions, not vi.fn(): a spy could inspect a
// revoked Proxy and fail before the code under test saw it.

type Outcome = { threw: boolean; logs: string[]; shutdowns: string[] };

function run(mode: 'exit' | 'survive', reason: unknown): Outcome {
  const out: Outcome = { threw: false, logs: [], shutdowns: [] };
  const handler = createUnhandledRejectionHandler({
    serviceName: 'svc',
    mode,
    logger: (m: string) => {
      out.logs.push(m);
    },
    shutdown: (s: string) => {
      out.shutdowns.push(s);
    },
  });
  try {
    handler(reason, Promise.resolve());
  } catch {
    out.threw = true;
  }
  return out;
}

describe('KS-1868 unhandledRejection handler reads the reason safely', () => {
  it('control ks1868 C1 an ordinary Error still logs its message and never shuts down in survive mode', () => {
    const out = run('survive', new Error('boom'));
    expect(out.threw).toBe(false);
    expect(out.logs).toHaveLength(1);
    expect(out.logs[0]).toContain('boom');
    expect(out.shutdowns).toEqual([]);
  });

  it('RED ks1868 R1 a revoked Proxy reason is logged as a constant in survive mode, without throwing', () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    const out = run('survive', proxy);
    expect(out.threw).toBe(false);
    expect(out.logs).toHaveLength(1);
    expect(out.logs[0]).toContain('unreadable thrown value');
    expect(out.shutdowns).toEqual([]);
  });

  it('RED ks1868 R2 an Error whose message getter throws is logged as a constant and still shuts down in exit mode', () => {
    const reason = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const out = run('exit', reason);
    expect(out.threw).toBe(false);
    expect(out.logs).toHaveLength(1);
    expect(out.logs[0]).toContain('unreadable thrown value');
    expect(out.shutdowns).toEqual(['unhandledRejection']);
  });
});
"""
TASKS['p1']=dict(
 dir='ks_1868_o38_p1_shared_gracefulshutdown_unhandled_rejection_unreadable_throw',
 prod=P1_PROD, test=P1_TEST, old=P1_OLD, new=P1_NEW, tbody=P1_T,
 svc='shared', where_line=52, catch_start=51,
 fn='the handler returned by `createUnhandledRejectionHandler`', file='gracefulShutdown.ts',
 runner_dir='Blockchain/Dev/packages/shared',
 ref=PKG+'src/__tests__/gracefulShutdown.unhandledRejection.test.ts',
 intro_site="the `detail` read at the top of the listener body returned by `createUnhandledRejectionHandler` in `gracefulShutdown.ts`",
 where_note="The listener body returned by `createUnhandledRejectionHandler` starts at line 51 (`return (reason: unknown) => {`); the `detail` read is lines 52-53.",
 s9note="The seat brief for the security tickets (S9) names `packages/shared` only for `tenant-context.ts` and `tenant-pool-manager.ts` (KS-1860); it does not name `utils/gracefulShutdown.ts`.",
 whatwrong=("In `gracefulShutdown.ts` the listener returned by `createUnhandledRejectionHandler` (the `unhandledRejection` handler body, starts at line 51) computes "
  "`const detail = reason instanceof Error ? `${reason.message}\\n${reason.stack ?? ''}` : String(reason);` (lines 52-53) BEFORE it either logs (mode 'survive', the api-gateway) or logs and calls `shutdown('unhandledRejection')` (mode 'exit'). "
  "If the rejection reason is a revoked Proxy, `reason instanceof Error` itself throws a TypeError (\"Cannot perform 'getPrototypeOf' on a proxy that has been revoked\"); if it is an Error whose `message` getter throws, `reason.message` throws. "
  "Either way the listener throws before it logs or shuts down: in 'survive' mode that is the front-door outage KS-546 was written to prevent (the survive path was the point), in 'exit' mode the process takes an uncaughtException instead of the orderly shutdown. "
  "The fix reads the reason inside its own inner `try` into `let detail: string`, falling back to the constant `unreadable thrown value`. Nothing else changes: an ordinary Error or string reason produces the same log text, the same mode behaviour and the same `survived` counter."),
 consequence="Today a hostile rejection reason makes the listener itself throw, so nothing is logged and, in 'exit' mode, `shutdown` is never called.",
 sibling="Every other function in `gracefulShutdown.ts` and every other `instanceof Error` site in `packages/shared` is NOT in this brief",
 red1="At the tip the listener throws (`run` records that as `threw: true`, so the failure is the `threw` assertion)",
 dbnote="`createUnhandledRejectionHandler` is exported and takes plain `logger` and `shutdown` functions; no process events are emitted (the existing test file says why). The stand-ins record into arrays.")

# ---------------- P2: shared responseCache middleware, cache read catch ----------------
P2_PROD=PKG+'src/cache/response-cache.ts'
P2_TEST=PKG+'src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts'
P2_OLD="""    } catch (error) {
      logger.error('[ResponseCache] Cache read error', { error: error instanceof Error ? error.message : String(error) });
    }
"""
P2_NEW="""    } catch (error) {
      let reason: string;
      try {
        reason = error instanceof Error ? error.message : String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.error('[ResponseCache] Cache read error', { error: reason });
    }
"""
P2_T="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: the responseCache middleware must still log its cache-read error and fall through to
// the origin handler (`next()`) when the cache store's `get` rejects with a value that cannot be
// read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on
// `.message`). A cache failure must never fail the request.
// The store stand-in is a plain object with plain functions, not vi.fn(): a spy inspects what it
// rejects with and could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  error: vi.fn(),
}));

vi.mock('../logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
}));

import { responseCache, setDefaultCacheStore } from '../cache/response-cache';

type Outcome = { threw: boolean; nextCalls: number };

async function run(): Promise<Outcome> {
  setDefaultCacheStore({
    get: () => Promise.reject(h.toThrow),
    set: () => Promise.resolve(),
    delete: () => Promise.resolve(),
    deleteByTag: () => Promise.resolve(),
  });
  const out: Outcome = { threw: false, nextCalls: 0 };
  const req = { method: 'GET', headers: {}, originalUrl: '/ks1868', url: '/ks1868' };
  const res = {
    statusCode: 200,
    json: () => res,
    setHeader: () => undefined,
    getHeader: () => undefined,
  };
  const next = () => {
    out.nextCalls++;
  };
  try {
    await responseCache({ ttl: 60 })(req as never, res as never, next as never);
  } catch {
    out.threw = true;
  }
  return out;
}

const READ_ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Cache read error'));

describe('KS-1868 responseCache reads a cache-read failure safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.error.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message and falls through to next()', async () => {
    h.toThrow = new Error('redis down');
    const out = await run();
    expect(out.threw).toBe(false);
    expect(out.nextCalls).toBe(1);
    expect(READ_ERRORS()).toHaveLength(1);
    expect(READ_ERRORS()[0][1]).toEqual({ error: 'redis down' });
  });

  it('RED ks1868 R1 a revoked Proxy rejection logs a constant reason and falls through to next()', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    const out = await run();
    expect(out.threw).toBe(false);
    expect(out.nextCalls).toBe(1);
    expect(READ_ERRORS()).toHaveLength(1);
    expect(READ_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and falls through to next()', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const out = await run();
    expect(out.threw).toBe(false);
    expect(out.nextCalls).toBe(1);
    expect(READ_ERRORS()).toHaveLength(1);
    expect(READ_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""
TASKS['p2']=dict(
 dir='ks_1868_o38_p2_shared_response_cache_read_unreadable_throw',
 prod=P2_PROD, test=P2_TEST, old=P2_OLD, new=P2_NEW, tbody=P2_T,
 svc='shared', where_line=299, catch_start=298,
 fn='the `responseCache` middleware', file='response-cache.ts',
 runner_dir='Blockchain/Dev/packages/shared',
 ref=PKG+'src/__tests__/ks932-timeout-bounds-dns.test.ts',
 intro_site="the cache-read catch block of the `responseCache` middleware in `response-cache.ts`",
 where_note="The catch block starts at line 298 (`} catch (error) {`); it is the one that logs '[ResponseCache] Cache read error'.",
 s9note="The seat brief for the security tickets (S9) names `packages/shared` only for `tenant-context.ts` and `tenant-pool-manager.ts` (KS-1860); it does not name `cache/response-cache.ts`.",
 whatwrong=("In `response-cache.ts` the catch block of the `responseCache` middleware around `defaultStore.get(cacheKey)` (starts at line 298) logs "
  "`logger.error('[ResponseCache] Cache read error', { error: error instanceof Error ? error.message : String(error) })` (line 299). "
  "If the store's `get` rejects with a revoked Proxy, `error instanceof Error` itself throws a TypeError (\"Cannot perform 'getPrototypeOf' on a proxy that has been revoked\") inside the catch block; if it rejects with an Error whose `message` getter throws, `error.message` throws. "
  "Either way the error is not logged and the middleware rejects instead of falling through to `next()`, so a cache failure fails the request it was only meant to speed up. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log line uses `reason`. "
  "Nothing else changes: an ordinary Error still logs `{ error: <its message> }`, the log text is unchanged, and the other catch blocks in the file (RedisCacheStore.set/delete/deleteByTag/addTag and the write-error `.catch`) are untouched."),
 consequence="Today a hostile rejection from the cache store makes the catch block itself throw, so nothing is logged and the middleware rejects instead of calling `next()`.",
 sibling="The other `instanceof Error` sites in `response-cache.ts` (lines 127, 135, 147, 155, 327) are NOT in this brief",
 red1="At the tip the middleware rejects (`run` records that as `threw: true` with `nextCalls` 0, so the failure is the `threw` assertion)",
 dbnote="`setDefaultCacheStore` and `responseCache` are exported; the store stand-in is a plain object whose `get` rejects with the value under test. The logger module (`../logger`, a directory index) is mocked; nothing else is imported by the file that does I/O.")

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
          "started_ok=KS-1868_is_Backlog;_%s_source_is_in_no_open_PR_(44_PRs_406_files_read_2026-10-31_by_op38,_positive_control_services/auth_in_14_entries);_file_not_named_in_the_S9_security_brief;_live_lanes_beyond_PRs_not_checked\n")%(T['file'],T['ref'],T['where_line'],T['svc'].replace('-','_'))
    open(d+'/spark.pins','w').write(pins)
    tp=T['test'].split('/')[-1]; pp=T['prod']
    txt=f"""# KS-1868 {T['svc']}: {T['fn']} must still report when the thrown value cannot be read (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW vitest file given whole)

DRAFT by Spark operator 38 for Wednesday, 2026-10-31. Secuura ({T['svc']}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {T['intro_site']}. {T['consequence']} No open PR touches this file (the 44 open PRs read 2026-10-31 through the GitHub API; 406 file entries; planted positive control: the same scan finds services/auth in 14 of them).

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

`{pp}:{T['where_line']}`. {T['where_note']}

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

- `{pp}:{T['where_line']}` is the `instanceof Error` read at the tip (read whole with `git show` at `{TIP[:12]}`). {T['where_note']}
- Open PRs: 44 read 2026-10-31 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{pp}` (44 PRs, 406 file entries); the positive control services/auth appears in 14 file entries.
- {T['s9note']}

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
