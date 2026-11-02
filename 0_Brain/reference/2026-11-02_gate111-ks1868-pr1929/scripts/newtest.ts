// KS-1868: `verifyDbReady` must still
// log its ERROR line and resolve when the thrown value itself cannot be read (a revoked Proxy
// throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`).
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

const { verifyDbReady } = require('../services/governanceService');

const ERRORS = () => mockHolder.error.mock.calls.filter((c) => String(c[0]) === 'Failed to seed proposal counter from DB');

describe('KS-1868 `verifyDbReady` reads the thrown value safely', () => {
  beforeEach(() => {
    mockHolder.toThrow = undefined;
    mockHolder.error = jest.fn();
  });

  it('control ks1868 C1 an ordinary Error still logs its message and resolves undefined', async () => {
    mockHolder.toThrow = new Error('db down');
    await expect(verifyDbReady()).resolves.toBeUndefined();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and resolves undefined', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    mockHolder.toThrow = proxy;
    await expect(verifyDbReady()).resolves.toBeUndefined();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and resolves undefined', async () => {
    mockHolder.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await expect(verifyDbReady()).resolves.toBeUndefined();
    expect(ERRORS()).toHaveLength(1);
    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
