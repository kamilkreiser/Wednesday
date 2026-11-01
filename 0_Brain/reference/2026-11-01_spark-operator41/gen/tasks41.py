TASKS={}
SVC_ROOT='Blockchain/Dev/services/'

def _res(call):
    return """  const r = await %s.catch(() => 'threw');""" % call

# ---- P1: nft-certificate cardano/provider.ts fetchProtocolParams
NP=SVC_ROOT+'nft-certificate/'
N_REF=NP+'src/__tests__/ks1836-log-silent-on-an-ordinary-own-rows-call.test.ts'
N_OLD="""  } catch (err: any) {
    logger.error('Failed to fetch protocol parameters', { error: err instanceof Error ? err.message : String(err) });
    return null;
  }
"""
N_NEW="""  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('Failed to fetch protocol parameters', { error: reason });
    return null;
  }
"""
N_TEST="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: fetchProtocolParams must still log its ERROR and return null when the thrown value
// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message`
// getter throws, throws on `.message`).
// The Blockfrost stand-in is a plain class, not a vi.fn(): a spy inspects what it rejects with
// and could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  error: vi.fn(),
}));

vi.mock('@blockfrost/blockfrost-js', () => ({
  BlockFrostAPI: class {
    epochsLatestParameters() {
      return Promise.reject(h.toThrow);
    }
    blocksLatest() {
      return Promise.resolve({ slot: 1 });
    }
  },
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: vi.fn(), error: h.error, debug: vi.fn() },
}));

import { initProvider, fetchProtocolParams } from '../cardano/provider';

const ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to fetch protocol parameters'));

describe('KS-1868 fetchProtocolParams reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.error.mockReset();
    initProvider('test-key', 'preprod');
  });

  it('control ks1868 C1 an ordinary Error still logs its message and returns null', async () => {
    h.toThrow = new Error('blockfrost down');
    const r = await fetchProtocolParams().catch(() => 'threw');
    expect(r).toBeNull();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'blockfrost down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and returns null', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    const r = await fetchProtocolParams().catch(() => 'threw');
    expect(r).toBeNull();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and returns null', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const r = await fetchProtocolParams().catch(() => 'threw');
    expect(r).toBeNull();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""

# ---- P2: demo-service routes/state.ts GET /state
DP=SVC_ROOT+'demo-service/'
D_REF=DP+'src/__tests__/ks1868-scenario-context-unreadable-throw.test.ts'
D_OLD="""  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Failed to read demo state', { error: message });
    return res.json(inMemoryState);
  }
"""
D_NEW="""  } catch (err) {
    let message: string;
    try {
      message = err instanceof Error ? err.message : 'Unknown error';
    } catch {
      message = 'unreadable thrown value';
    }
    logger.error('Failed to read demo state', { error: message });
    return res.json(inMemoryState);
  }
"""
D_TEST="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: the GET /state handler must still log and answer with the in-memory state when the
// thrown value itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose
// `message` getter throws, throws on `.message`).
// The Redis stand-in is a plain class, not a vi.fn(): a spy could inspect a revoked Proxy and
// fail before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  error: vi.fn(),
}));

vi.mock('ioredis', () => ({
  default: class {
    on() {
      return this;
    }
    get() {
      return Promise.reject(h.toThrow);
    }
    set() {
      return Promise.resolve('OK');
    }
  },
}));

vi.mock('../utils/logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
}));

import { stateRouter } from '../routes/state';

type Layer = { route?: { path: string; stack: Array<{ handle: (req: unknown, res: unknown) => unknown }> } };
type Outcome = { threw: boolean; status?: number; body?: unknown };

/** Run the real GET /state handler; the Redis stand-in rejects with the value under test. */
async function runHandler(): Promise<Outcome> {
  const layer = (stateRouter as unknown as { stack: Layer[] }).stack.find((l) => l.route?.path === '/state');
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
  try {
    await handle({}, res);
  } catch {
    out.threw = true;
  }
  return out;
}

const ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Failed to read demo state'));
const IN_MEMORY = { currentPersona: null, presenterMode: false, scenarioStep: 0 };

describe('KS-1868 GET /state reads the thrown value safely', () => {
  beforeEach(() => {
    process.env.REDIS_URL = 'redis://127.0.0.1:1';
    h.toThrow = undefined;
    h.error.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message and answers the in-memory state', async () => {
    h.toThrow = new Error('redis boom');
    const out = await runHandler();
    expect(out.threw).toBe(false);
    expect(out.body).toEqual(IN_MEMORY);
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'redis boom' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and answers the in-memory state', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    const out = await runHandler();
    expect(out.threw).toBe(false);
    expect(out.body).toEqual(IN_MEMORY);
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and answers the in-memory state', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const out = await runHandler();
    expect(out.threw).toBe(false);
    expect(out.body).toEqual(IN_MEMORY);
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""
S9="This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator."
TASKS['p1']=dict(svc='nft-certificate', runner_dir='Blockchain/Dev/services/nft-certificate', ref=N_REF, s9note=S9,
 dir='ks_1868_o41_p1_nftcertificate_provider_fetchprotocolparams_unreadable_throw',
 prod=NP+'src/cardano/provider.ts', test=NP+'src/__tests__/ks1868-provider-fetch-protocol-params-unreadable-throw.test.ts',
 old=N_OLD, new=N_NEW, tbody=N_TEST, where_line=66, catch_start=65, fn='`fetchProtocolParams`', file='provider.ts',
 intro_site="the catch block of `fetchProtocolParams` in `cardano/provider.ts`",
 where_note="The catch block starts at line 65 (`} catch (err: any) {`); it logs the ERROR 'Failed to fetch protocol parameters' with `{ error: <message> }` and returns null. The message is not returned to any caller (the function returns `ProtocolParams | null`).",
 whatwrong=("In `provider.ts` the catch block of `fetchProtocolParams` (line 65) logs `logger.error('Failed to fetch protocol parameters', { error: err instanceof Error ? err.message : String(err) })` (the read is on line 66). "
  "If a Blockfrost call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the ERROR is logged: `fetchProtocolParams()` rejects instead of returning its documented `null` and the operator sees no log line. "
  "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }`, the log text is unchanged and the function still returns null."),
 consequence="Today a hostile rejection from Blockfrost makes the catch block itself throw, so nothing is logged and the function rejects instead of returning null.",
 red1="At the tip the call rejects (the test swallows that with `.catch`), so no ERROR is logged and the log-count assertion fails",
 dbnote="`@blockfrost/blockfrost-js` and `../utils/logger` are mocked; no network, no API key and no app boot. The Blockfrost stand-in is a plain class on purpose.",
 sibling="There is no other `instanceof Error` read in `provider.ts`")
TASKS['p2']=dict(svc='demo-service', runner_dir='Blockchain/Dev/services/demo-service', ref=D_REF, s9note=S9,
 dir='ks_1868_o41_p2_demoservice_state_get_unreadable_throw',
 prod=DP+'src/routes/state.ts', test=DP+'src/__tests__/ks1868-state-get-unreadable-throw.test.ts',
 old=D_OLD, new=D_NEW, tbody=D_TEST, where_line=81, catch_start=80, fn='the `GET /state` handler', file='state.ts',
 intro_site="the catch block of the `GET /state` handler in `routes/state.ts`",
 where_note="The catch block starts at line 80 (`} catch (err) {`); it logs the ERROR 'Failed to read demo state' and answers `res.json(inMemoryState)`. The message is only logged; it never reaches the response body.",
 whatwrong=("In `state.ts` the catch block of the `GET /state` handler (line 80) does `const message = err instanceof Error ? err.message : 'Unknown error'` (line 81), then `logger.error('Failed to read demo state', { error: message })` and `return res.json(inMemoryState)`. "
  "If Redis rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
  "Either way the catch throws before the log and before the fallback answer: the async handler rejects, no ERROR is logged, and the request gets no in-memory fallback. "
  "The fix reads the thrown value inside its own inner `try` into `message`, falling back to the constant `unreadable thrown value`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }` and the handler still answers `res.json(inMemoryState)`."),
 consequence="Today a hostile rejection from Redis makes the catch block itself throw, so no ERROR is logged and the handler rejects instead of answering the in-memory fallback.",
 red1="At the tip the handler promise rejects (the test records that as `threw`), so the `threw` assertion fails",
 dbnote="`ioredis` and `../utils/logger` are mocked; no Redis, no app boot and no network. `REDIS_URL` is set only so that `getRedis()` builds the stand-in client. The Redis stand-in is a plain class on purpose.",
 sibling="The other `instanceof Error` read in `state.ts` (line 110, the POST `/presenter-mode` catch) is NOT in this brief")
