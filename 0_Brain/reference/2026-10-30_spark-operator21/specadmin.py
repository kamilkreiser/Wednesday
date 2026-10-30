# Filing-list item (X 3rd F4): api-gateway admin.ts PATCH /api/users/admin/:id 502 echoes err.message (the KS-1791 class). Spark operator 21.
# code_patch2, LOOSE (rung 4): product lines written by the model from the contract, hunk headers dictated; the new test is given whole.
P1='Blockchain/Dev/services/api-gateway/src/routes/admin.ts'
TP='Blockchain/Dev/services/api-gateway/src/__tests__/ks1791class-admin-patch-user-502-never-echoes-the-thrown-text.test.ts'
OLD1=("    } catch (err: any) {\n"
"      res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable', details: { details: err.message } } });\n")
NEW1=("    } catch (err: any) {\n"
"      log('error', '[Users] Admin update could not reach the auth service', { error: err instanceof Error ? err.message : String(err) });\n"
"      res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable' } });\n")
TEST='''/**
 * Filing-list item (seat X 3rd, F4; the KS-1791 class): PATCH /api/users/admin/:id in api-gateway routes/admin.ts forwards to the auth
 * service, and when that forward THROWS its catch answered 502 with `details: { details: err.message }`, so a driver message or an internal
 * host:port reached the client. The sibling in routes/proxy.ts answers the same 502 with no details at all. The fix: the thrown text goes to
 * the server log (deps.log), and the 502 body is the constant { success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable' } }.
 *
 * Harness: the fake req/res dispatch of ks1196 (the real createAdminRoutes router, no server); global fetch is stubbed per cell, so no network.
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import type { Request, Response, Router } from 'express';
import { configureAuth, authenticateToken, parseTestToken } from '../middleware/auth';
import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';

// THE FIXTURE IS LOAD-BEARING: a private host:port and a marker no other code path could produce.
const LEAK = 'connect ECONNREFUSED 10.0.4.17:4003 ks1791class-admin-patch-private-detail';
const BODY_502 = { success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable' } };

function buildTestToken(payload: Record<string, unknown>): string {
  return 'test_token_' + Buffer.from(JSON.stringify(payload)).toString('base64');
}
const ADMIN_HEADERS = { authorization: 'Bearer ' + buildTestToken({ sub: 'admin-1', role: 'SYSTEM_ADMIN', email: 'admin-1@test.io' }) };
const USER_HEADERS = { authorization: 'Bearer ' + buildTestToken({ sub: 'user-1', role: 'user', email: 'user-1@test.io' }) };

type CapturedRes = Response & { _status: number; _json: any };

function dispatch(router: Router, headers: Record<string, string>): Promise<CapturedRes> {
  return new Promise((resolve, reject) => {
    const res: any = {
      _status: 200,
      _json: null,
      status(code: number) {
        res._status = code;
        return res;
      },
      json(payload: unknown) {
        res._json = payload;
        resolve(res);
        return res;
      },
      setHeader() {
        return res;
      },
    };
    const req = {
      method: 'PATCH',
      url: '/api/users/admin/u-ks1791class',
      headers,
      body: { role: 'user' },
      query: {},
      get(name: string) {
        return (this as any).headers[name.toLowerCase()];
      },
    } as unknown as Request;
    router(req, res, (err: unknown) => (err ? reject(err) : resolve(res)));
  });
}

let router: Router;
let logCalls: unknown[][];

beforeEach(() => {
  vi.stubEnv('NODE_ENV', 'test');
  configureAuth({ enableTestTokens: true, defaultTenantId: 'default' });
  logCalls = [];
  router = createAdminRoutes({
    authenticateToken,
    parseTestToken,
    query: async () => ({ rows: [], rowCount: 0 }),
    isDbAvailable: () => false,
    redisService: {},
    services: { auth: { url: 'http://auth.test:4003' } },
    log: (...args: unknown[]) => {
      logCalls.push(args);
    },
  } as unknown as AdminRouteDeps);
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe('admin PATCH /api/users/admin/:id: an unreachable auth service answers 502 without the thrown text', () => {
  it('RED admin-502 P1 the 502 body is exactly the constant envelope, with no details and none of the thrown text', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error(LEAK)));
    const res = await dispatch(router, ADMIN_HEADERS);
    expect(res._status).toBe(502);
    expect(JSON.stringify(res._json)).not.toContain(LEAK);
    expect(res._json).toEqual(BODY_502);
  });

  it('RED admin-502 P2 the thrown text is logged server-side at error level', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error(LEAK)));
    const res = await dispatch(router, ADMIN_HEADERS);
    expect(res._status).toBe(502);
    expect(logCalls.some((c) => c[0] === 'error' && JSON.stringify(c).includes(LEAK))).toBe(true);
  });

  it('RED admin-502 P3 the 502 body is the same for two different thrown texts', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error(LEAK)));
    const first = await dispatch(router, ADMIN_HEADERS);
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('getaddrinfo ENOTFOUND auth.internal')));
    const second = await dispatch(router, ADMIN_HEADERS);
    expect(second._json).toEqual(first._json);
  });

  it('control admin-502 C1 an auth service that answers is relayed with its status and body, and nothing is logged', async () => {
    const upstreamBody = { success: true, data: { id: 'u-ks1791class', role: 'user' } };
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ status: 200, json: async () => upstreamBody }));
    const res = await dispatch(router, ADMIN_HEADERS);
    expect([res._status, res._json]).toEqual([200, upstreamBody]);
    expect(logCalls).toEqual([]);
  });

  it('control admin-502 C2 a caller with no bearer is answered 401 and the auth service is never called', async () => {
    const fetchSpy = vi.fn();
    vi.stubGlobal('fetch', fetchSpy);
    const res = await dispatch(router, {});
    expect([res._status, res._json.error.code, fetchSpy.mock.calls.length]).toEqual([401, 'UNAUTHORIZED', 0]);
  });

  it('control admin-502 C3 a caller who is not an admin is answered 403 and the auth service is never called', async () => {
    const fetchSpy = vi.fn();
    vi.stubGlobal('fetch', fetchSpy);
    const res = await dispatch(router, USER_HEADERS);
    expect([res._status, res._json.error.code, fetchSpy.mock.calls.length]).toEqual([403, 'FORBIDDEN', 0]);
  });
});
'''
S=dict(dir='ks_x3f4_p1_admin_patch_502_no_echo',ticket='KS-1410',
 title="api-gateway admin.ts PATCH /api/users/admin/:id: the 502 catch must stop echoing err.message to the client (filing-list item X 3rd F4, the KS-1791 class) (RUNG 4, code_patch2 LOOSE: the product lines are written from the contract; hunk headers dictated; one NEW vitest file given whole)",
 intro="DRAFT by Spark operator 21 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / api-gateway) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: the NEXT-PICKUP filing list (seat X 3rd, F4: 'admin.ts PATCH 502 echoes err.message, the KS-1791 class'); no Linear ticket exists yet (the brief file is named for KS-1410, the SIBLING ticket of the same class, the 502 of audit-export.ts, because the builder needs a real ticket to read; KS-1410 is NOT what this closes) (board search 2026-10-30 for 'users/admin/:id', 'details: err.message', 'admin.ts PATCH': 0 relevant hits), so the raise seat files one or links the filing. RUNG 4 (looser): the product edit is described by behaviour, not given as a diff; the hunk headers and unchanged context lines are dictated. The sibling `routes/proxy.ts:514` and `:546` already answer this exact 502 with no `details`. Not auth/token code: it is a gateway forward to the auth service. No open PR touches admin.ts or api-gateway source (the only api-gateway file in the 23 open PRs is package.json).",
 products=[(P1,[(OLD1,NEW1)])],
 prodnote=['product, modified in place: ONE hunk in the `catch` of `router.patch(\'/api/users/admin/:id\', ...)`'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 6 cells (3 red, 3 control); drives the real createAdminRoutes router with a fake req/res, no server'],
 runner='vitest` (`npx vitest run src/__tests__/ks1791class-admin-patch-user-502-never-echoes-the-thrown-text.test.ts` from `Blockchain/Dev/services/api-gateway',
 tier='code_patch2', rung='4 (LOOSE: product lines written by the model, hunk headers dictated; new test given whole)',
 pins='''# code_patch2: api-gateway routes/admin.ts (1 hunk) + a NEW vitest file; ref = ks1196 (same createAdminRoutes fake-dispatch harness, shape only); line = the first changed line in the product.
tier=code_patch2
ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts
line=1483
ctx=65536
started_ok=KS-1410_is_the_SIBLING_ticket_of_the_same_class_(audit-export_502),_its_PR_1432_merged;_this_item_is_a_filing-list_entry_(seat_X_3rd_F4)_with_no_ticket_of_its_own;_no_open_PR_touches_api-gateway_source_(only_package_json,_read_2026-10-30);_the_operator_did_not_check_other_live_lanes
''',
 wrong="In `services/api-gateway/src/routes/admin.ts`, `router.patch('/api/users/admin/:id', ...)` forwards the PATCH to the auth service. When that forward throws (a refused connection, a DNS failure, a cut-off body), the `catch (err: any)` answers `502` with the body `{ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable', details: { details: err.message } } }`, so the thrown error's own text (a driver message or an internal host:port) reaches the client. The same 502 in `routes/proxy.ts` (:514, :546) carries no `details`. The fix: in that `catch`, log the thrown text server-side with the router's injected `log` function at level `'error'` (a short fixed message that names the route, and the thrown text in the meta object, taken as `err instanceof Error ? err.message : String(err)`), and answer the constant `{ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable' } }` with NO `details` key. Nothing else in the handler changes: the status 502, the code and the message stay exactly as they are.",
 where="- `services/api-gateway/src/routes/admin.ts:1482-1483` - **must change**: inside `router.patch('/api/users/admin/:id', ...)` (:1463), the `catch (err: any) {` block whose only statement is the `res.status(502).json(...)` line carrying `details: { details: err.message }`. `log` is already in scope (the `deps` destructuring at :552-560 and used at :1457 and :1496). The `try` body (:1465-1481), the 502 status, the code `BAD_GATEWAY` and the message `Auth service unavailable` STAY.\n- `services/api-gateway/src/routes/admin.ts:1018` also interpolates `err.message` (`Network error: ${err.message}`), in the Blockfrost connectivity-test route, which reports a diagnostic to an admin on purpose: it is NOT part of this task and is NOT touched.",
 exactnote="",
 loose="The product edit is described by behaviour in `## What is wrong` and `## Where`; no diff and no `+` line is given for it. Write it yourself: minimal, only what those two sections require.\n\n",
 donot="**Do NOT touch** any other line of `admin.ts` (the Blockfrost route at :1018 least of all, nor the other catch blocks), `routes/proxy.ts`, the existing tests, or any other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It has no top-level await and stubs the global `fetch` per cell.",
 red=['RED admin-502 P1','RED admin-502 P2','RED admin-502 P3'],
 cells="- RED `P1` (the 502 body equals the constant envelope: at the tip it carries `details`), `P2` (the thrown text is in an error-level `log` call: at the tip nothing is logged), `P3` is red at the tip only because the details differ between the two thrown texts: all fail by assertion at the tip, pass after the edit.\n- GREEN at the tip and after: `C1` (an answering auth service is relayed, nothing logged), `C2` (no bearer: 401, fetch never called), `C3` (non-admin role: 403, fetch never called).",
 premises="- `admin.ts:1482` is `    } catch (err: any) {` and :1483 is the `res.status(502).json(...)` line with `details: { details: err.message }`; :1463 opens `router.patch('/api/users/admin/:id'`; read at the tip by script, the golden is generated from the tree at the tip.\n- `proxy.ts:514` and `:546` answer `{ code: 'BAD_GATEWAY', message: 'Auth service unavailable' }` with no details (read at the tip).\n- `ks1240b-every-hand-built-gateway-fetch-is-bounded.test.ts:267` pins the code and message of this 502 (`AUTH_DOWN`) and does not read `details`, so the existing suite does not depend on the field (read at the tip).\n- The harness (fake req/res into `createAdminRoutes`, `configureAuth({ enableTestTokens: true })`, a `test_token_<base64>` bearer) is copied from `ks1196-admin-post-api-admin-document-types.test.ts:11-93`.",
 unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Whether `requireAdmin` accepts the role `user` as 403 (cell C3) with `FORBIDDEN`: read from the source (:612-630), measured only by the control run.\n- No Linear ticket: a raise note must say so. Whether the gateway should also change `admin.ts:1018` is a separate question and is left alone.",
 scope="**The admin.ts PATCH /api/users/admin/:id 502 only.** Not a close of any ticket (none exists); link as 'Refs seat X 3rd F4 (filing list)'.",
)
