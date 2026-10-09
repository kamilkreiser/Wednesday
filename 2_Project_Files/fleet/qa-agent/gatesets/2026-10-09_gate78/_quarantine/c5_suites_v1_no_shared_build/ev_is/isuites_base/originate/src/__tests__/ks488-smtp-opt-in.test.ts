/**
 * KS-488 C-5 — SMTP must be opt-in, and must never default to a real provider.
 *
 * The mirror of the auth service's suite of the same name. Both services carry
 * their own copy of this email module, and the original ticket named only one
 * of them — so a regression test in only one service would repeat exactly the
 * shape of the defect it is pinning.
 *
 * The module reads its configuration once at import time, so each case sets the
 * environment and re-requires it through `jest.isolateModules`. That is
 * deliberate: it binds the assertions to the real module's real initialisation
 * rather than to a re-implementation of it.
 */

type EmailModule = typeof import('../services/email');

const SMTP_VARS = [
  'SMTP_HOST',
  'SMTP_PORT',
  'SMTP_USER',
  'SMTP_PASS',
  'SMTP_FROM',
  'SMTP_ENABLED',
  'EMAIL_FROM',
  'ACS_CONNECTION_STRING',
  'ACS_SENDER_ADDRESS',
] as const;

const saved: Record<string, string | undefined> = {};

function loadEmailModule(env: Record<string, string>): EmailModule {
  for (const key of SMTP_VARS) delete process.env[key];
  Object.assign(process.env, env);
  let mod!: EmailModule;
  jest.isolateModules(() => {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    mod = require('../services/email') as EmailModule;
  });
  return mod;
}

beforeEach(() => {
  for (const key of SMTP_VARS) saved[key] = process.env[key];
});

afterEach(() => {
  for (const key of SMTP_VARS) {
    if (saved[key] === undefined) delete process.env[key];
    else process.env[key] = saved[key] as string;
  }
});

describe('KS-488 C-5: SMTP is opt-in only', () => {
  it('a password ALONE does not enable the transport', () => {
    // The exact regression: SMTP_PASS set, SMTP_ENABLED absent.
    const email = loadEmailModule({ SMTP_PASS: 'a-real-looking-api-key' });
    expect(email.isEmailConfigured()).toBe(false);
  });

  it('a password plus a host still does not enable it without the switch', () => {
    const email = loadEmailModule({
      SMTP_PASS: 'a-real-looking-api-key',
      SMTP_HOST: 'smtp.example.test',
      SMTP_FROM: 'noreply@example.test',
    });
    expect(email.isEmailConfigured()).toBe(false);
  });

  it('SMTP_ENABLED must be exactly "true" — no truthy-string coercion', () => {
    for (const value of ['TRUE', 'True', '1', 'yes', 'on']) {
      const email = loadEmailModule({
        SMTP_ENABLED: value,
        SMTP_HOST: 'smtp.example.test',
        SMTP_FROM: 'noreply@example.test',
      });
      expect(email.isEmailConfigured()).toBe(false);
    }
  });
});

describe('KS-488 C-5: no default points at a real mail provider', () => {
  it('enabled with no host fails closed rather than defaulting to one', () => {
    const email = loadEmailModule({
      SMTP_ENABLED: 'true',
      SMTP_FROM: 'noreply@example.test',
    });
    expect(email.isEmailConfigured()).toBe(false);
  });

  it('enabled with no from-address fails closed', () => {
    const email = loadEmailModule({
      SMTP_ENABLED: 'true',
      SMTP_HOST: 'smtp.example.test',
    });
    expect(email.isEmailConfigured()).toBe(false);
  });

  it('sending while enabled-but-unconfigured refuses, and says why once', async () => {
    const errors: string[] = [];
    const spy = jest.spyOn(console, 'error').mockImplementation((...args: unknown[]) => {
      errors.push(args.join(' '));
    });
    try {
      const email = loadEmailModule({ SMTP_ENABLED: 'true' });
      const first = await email.sendEmail({
        to: 'someone@example.test',
        subject: 'should not send',
        text: 'should not send',
      });
      const second = await email.sendEmail({
        to: 'someone@example.test',
        subject: 'should not send either',
        text: 'should not send either',
      });

      expect(first).toBe(false);
      expect(second).toBe(false);

      const refusals = errors.filter((line) => line.includes('refusing to send'));
      // Loud, but once — an unconfigured deployment must not flood its own logs.
      expect(refusals).toHaveLength(1);
      expect(refusals[0]).toContain('SMTP_HOST');
      expect(refusals[0]).toContain('SMTP_FROM');
    } finally {
      spy.mockRestore();
    }
  });
});

describe('KS-488 C-5: the positive case still works', () => {
  it('an explicitly configured SMTP deployment reports configured', () => {
    const email = loadEmailModule({
      SMTP_ENABLED: 'true',
      SMTP_HOST: 'smtp.example.test',
      SMTP_USER: 'someone',
      SMTP_PASS: 'a-real-looking-api-key',
      SMTP_FROM: 'noreply@example.test',
    });
    expect(email.isEmailConfigured()).toBe(true);
  });

  it('an ACS-only deployment reports configured even with SMTP off', () => {
    // Pins the second half of the fix: isEmailConfigured() used to return
    // SMTP_ENABLED alone, so an ACS deployment looked unconfigured and its
    // callers skipped notifications they could in fact have sent.
    const email = loadEmailModule({
      ACS_CONNECTION_STRING: 'endpoint=https://example.test/;accesskey=not-a-real-key',
      ACS_SENDER_ADDRESS: 'donotreply@example.test',
    });
    expect(email.isEmailConfigured()).toBe(true);
  });
});
