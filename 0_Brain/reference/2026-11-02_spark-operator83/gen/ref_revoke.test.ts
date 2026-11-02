import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';

process.env.SECURITY_DISABLE_BOOT = '1';

// KS-1868: `revokePriorConnectorKeys` must still log its line and return null (the KS-577 contract) when the thrown value itself cannot be
// read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`).
// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
// itself fail on a revoked Proxy before the code under test saw it. The outcome is captured with
// `.then(onOk, onReject)` so the hostile value is never handed to an assertion message.
// The service logs through console.log (JSON lines), so the log is read from a console.log spy.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  sql: [] as string[],
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  initDb: async () => true,
  query: () => Promise.reject(h.toThrow),
}));

const TENANT = 'c0000000-0000-4000-8000-000000001868';
const CONNECTOR = 'ks1868-connector';
const LOGGED: string[] = [];
const LINES = () =>
  LOGGED.filter((s) => s.includes('KS-577: revoke-on-rotate FAILED')).map((s) => JSON.parse(s) as { error: unknown });

let revokePriorConnectorKeys: (connectorId: string, tenantId: string, keepKeyId: string) => Promise<number | null>;

beforeAll(async () => {
  const mod = await import('../index');
  revokePriorConnectorKeys = mod.revokePriorConnectorKeys;
});

beforeEach(() => {
  h.toThrow = undefined;
  h.sql.length = 0;
  LOGGED.length = 0;

  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
    LOGGED.push(String(args[0]));
  });
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('KS-1868 `revokePriorConnectorKeys` reads the thrown value safely', () => {
  it('control ks1868 C1 an ordinary Error still logs its message and the function still answers null', async () => {
    h.toThrow = new Error('db down');
    const outcome = await revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key').then(
      (value) => ({ rejected: false, value }),
      () => ({ rejected: true, value: undefined }),
    );
    expect(outcome).toEqual({ rejected: false, value: null });
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0].error).toBe('db down');
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the function still answers null', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    const outcome = await revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key').then(
      (value) => ({ rejected: false, value }),
      () => ({ rejected: true, value: undefined }),
    );
    expect(outcome).toEqual({ rejected: false, value: null });
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0].error).toBe('unreadable thrown value');
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and the function still answers null', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const outcome = await revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key').then(
      (value) => ({ rejected: false, value }),
      () => ({ rejected: true, value: undefined }),
    );
    expect(outcome).toEqual({ rejected: false, value: null });
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0].error).toBe('unreadable thrown value');
  });
});
