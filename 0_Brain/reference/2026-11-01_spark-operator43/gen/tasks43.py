TASKS={}
DP='Blockchain/Dev/services/demo-service/'
GP='Blockchain/Dev/services/governance/'
D_REF=DP+'src/__tests__/ks1868-scenario-context-unreadable-throw.test.ts'
G_REF=GP+'src/__tests__/ks1845-process-expired-requires-a-platform-admin.test.ts'
P_OLD="""    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Persona switch error', { error: message });
"""
P_NEW="""    let message: string;
    try {
      message = err instanceof Error ? err.message : 'Unknown error';
    } catch {
      message = 'unreadable thrown value';
    }
    logger.error('Persona switch error', { error: message });
"""
P_TEST="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: the POST /persona/switch handler must still log and answer its generic 500 when the
// thrown value itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose
// `message` getter throws, throws on `.message`).
// The auth stand-in is a plain function, not a vi.fn(): a spy inspects what it rejects with and
// could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  error: vi.fn(),
}));

vi.mock('../utils/logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
}));

vi.mock('../services/authClient', () => ({
  authenticatePersona: () => Promise.reject(h.toThrow),
}));

import { personaRouter } from '../routes/persona';

type Layer = { route?: { path: string; stack: Array<{ handle: (req: unknown, res: unknown) => unknown }> } };
type Outcome = { threw: boolean; status?: number; body?: unknown };

/** Run the real route handler with a valid persona body; the mocked auth call rejects with the value under test. */
async function runHandler(): Promise<Outcome> {
  const layer = (personaRouter as unknown as { stack: Layer[] }).stack.find(
    (l) => l.route?.path === '/persona/switch',
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
    setHeader() {
      return res;
    },
  };
  try {
    await handle({ body: { persona: 'alice' } }, res);
  } catch {
    out.threw = true;
  }
  return out;
}

const ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Persona switch error'));
const GENERIC = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };

describe('KS-1868 persona switch handler reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.error.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message and answers 500', async () => {
    h.toThrow = new Error('auth boom');
    const out = await runHandler();
    expect(out.threw).toBe(false);
    expect(out.status).toBe(500);
    expect(out.body).toEqual(GENERIC);
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'auth boom' });
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
G_OLD="""  } catch (err: any) {
    logger.error('DB get proposal failed', { id, error: err instanceof Error ? err.message : String(err) });
  }
"""
G_NEW="""  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB get proposal failed', { id, error: reason });
  }
"""
G_TEST="""// KS-1868: dbGetProposal (reached through the exported getProposal) must still log its ERROR line and
// resolve `undefined` when the thrown value itself cannot be read (a revoked Proxy throws on
// `instanceof`; an Error whose `message` getter throws, throws on `.message`).
// The db stand-in is a plain function, not a jest.fn(): a spy inspects what it rejects with and
// could itself fail on a revoked Proxy before the code under test saw it.
const mockHolder: { toThrow: unknown; error: jest.Mock } = { toThrow: undefined, error: jest.fn() };

jest.mock('../db', () => ({
  isDbAvailable: () => true,
  query: () => Promise.reject(mockHolder.toThrow),
}));
jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), debug: jest.fn(), error: (...a: unknown[]) => mockHolder.error(...a) },
}));

const { getProposal } = require('../services/governanceService');

const ERRORS = () => mockHolder.error.mock.calls.filter((c) => String(c[0]).includes('DB get proposal failed'));

describe('KS-1868 dbGetProposal reads the thrown value safely', () => {
  beforeEach(() => {
    mockHolder.toThrow = undefined;
    mockHolder.error = jest.fn();
  });

  it('control ks1868 C1 an ordinary Error still logs its message and resolves undefined', async () => {
    mockHolder.toThrow = new Error('db down');
    await expect(getProposal('p-1')).resolves.toBeUndefined();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ id: 'p-1', error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and resolves undefined', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    mockHolder.toThrow = proxy;
    await expect(getProposal('p-1')).resolves.toBeUndefined();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ id: 'p-1', error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and resolves undefined', async () => {
    mockHolder.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await expect(getProposal('p-1')).resolves.toBeUndefined();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ id: 'p-1', error: 'unreadable thrown value' });
  });
});
"""
S9="This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator."
TASKS['p1']=dict(svc='demo-service', runner_dir='Blockchain/Dev/services/demo-service', ref=D_REF, s9note=S9,
 dir='ks_1868_o43_p1_demoservice_persona_switch_unreadable_throw',
 prod=DP+'src/routes/persona.ts', test=DP+'src/__tests__/ks1868-persona-switch-unreadable-throw.test.ts',
 old=P_OLD, new=P_NEW, tbody=P_TEST, where_line=77, fn='the `POST /persona/switch` handler', file='persona.ts',
 shape="the handler is run from the router stack with a fake response; `vi.hoisted` holder, `vi.mock(...)` of the logger and authClient, then the import",
 intro_site="the catch block of the `POST /persona/switch` handler in `routes/persona.ts`",
 where_note="The catch block starts at line 76 (`} catch (err) {`); line 77 reads the message, line 78 logs it with `logger.error('Persona switch error', { error: message })`, and the handler then answers a FIXED generic 500 (`INTERNAL_ERROR` / 'Internal server error'). The message is never in the response body. The 502 branch above ('Persona auth failed') is not this catch and is NOT in this brief.",
 whatwrong=("In `persona.ts` the catch of the switch handler (line 76) computes `const message = err instanceof Error ? err.message : 'Unknown error'` (line 77) and logs it. "
  "If the auth call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the ERROR line is logged and before the generic 500 is sent: the async handler rejects, no log line is written and the caller gets no JSON 500 from this handler. "
  "The fix reads the thrown value inside its own inner `try` into `message`, falling back to the constant `unreadable thrown value`; the log call and the 500 body are unchanged. An ordinary Error still logs `{ error: <its message> }`."),
 consequence="Today a hostile rejection from the auth call makes the catch block itself throw, so nothing is logged and the generic 500 is never sent. The response never carries the message, so the fix cannot change what a client sees on the ordinary path.",
 red1="At the tip the handler rejects (the test records that as `threw`), so no ERROR line is logged, no 500 is sent and the assertions fail",
 dbnote="`../utils/logger` and `../services/authClient` are mocked; no network, no app boot. The handler is taken from `personaRouter.stack` and called with a fake request body (`persona: 'alice'`) and a fake response.",
 sibling="The other branches of the handler (the 400 validation answer, the 502 'Persona auth failed' answer) and every other file of the service are NOT in this brief")
TASKS['p2']=dict(svc='governance', runner_dir='Blockchain/Dev/services/governance', ref=G_REF, s9note=S9, runner='jest', runcmd='',
 dir='ks_1868_o43_p2_governance_dbgetproposal_unreadable_throw',
 prod=GP+'src/services/governanceService.ts', test=GP+'src/__tests__/ks1868-db-get-proposal-unreadable-throw.test.ts',
 old=G_OLD, new=G_NEW, tbody=G_TEST, where_line=219, fn='`dbGetProposal`', file='governanceService.ts',
 shape="a holder object whose name starts with `mock`, `jest.mock(...)` of the db and logger modules, then a `require` of the module under test",
 intro_site="the catch block of the module function `dbGetProposal` in `services/governanceService.ts`",
 where_note="The catch block starts at line 218 (`} catch (err: any) {`); it logs the ERROR line 'DB get proposal failed' with `{ id, error: <message> }` and does NOT rethrow: the function then returns `undefined` (line 221). The message is only logged. The `dbSave*` helpers above it rethrow and are NOT in this brief.",
 whatwrong=("In `governanceService.ts` the catch block of `dbGetProposal` (line 218) logs `logger.error('DB get proposal failed', { id, error: err instanceof Error ? err.message : String(err) })` (the read is on line 219) and then falls through to `return undefined`. "
  "If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the ERROR line is logged and before the documented `undefined` return: `dbGetProposal` (and `getProposal` and every vote/queue/execute caller of it) rejects with the hostile value instead of treating the proposal as not found. "
  "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ id, error: <its message> }`."),
 consequence="Today a hostile rejection from the database layer makes the catch block itself throw, so nothing is logged and the function rejects instead of returning `undefined`.",
 red1="At the tip `getProposal` rejects, so the `resolves.toBeUndefined()` assertion fails (and no ERROR line is logged)",
 dbnote="`../db` and `../utils/logger` are mocked; no database, no app boot and no network. `dbGetProposal` is not exported, so the test reaches it through the exported `getProposal`.",
 sibling="The other `instanceof Error` reads in `governanceService.ts` (the `dbSave*` helpers that rethrow, the other `dbGet*` helpers, `processExpiredProposals`) are NOT in this brief")
