/**
 * KS-1448 (api-gateway routes/notifications.ts, POST /): the handler stored a notification under the BODY's userId
 * with no check against the caller, so any authenticated caller could place a `security` or `system` notification
 * with an actionUrl in another user's inbox (in-app phishing; the finding is row 1 of KS-486, Review A).
 *
 * THE RULING, verbatim, Wednesday (the fleet coordinator, not Kam), ANSWER 2026-11-06T07:01:24Z:
 *   "KS-1448 shape B: own id only, 403 for every other userId, every principal."
 *   "403 not 404; after the validators, before createNotification; omitted userId stays 400; connector keys refused
 *   except their own id."
 * This is narrower than Peter's suggestion on the ticket (comment d457b6ed, "unless the caller is an admin"): no
 * caller in this repo needs an admin arm, and adding one is a one-line change.
 *
 * Harness: the fake req/res dispatch of notifications.test.ts (the real router, no server, no network), with the
 * router-wide authenticateToken replaced by a pass-through, so req.user is exactly what the cell sets. That is how a
 * connector principal and a token with no userId are reached without a security service. The real middleware is
 * driven by the refusal cell in notifications.test.ts.
 *
 * Every read of the response uses optional access, so on code without the check a cell fails by assertion on the 201
 * it received, never by a TypeError on a field that is not there.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import type { Request, Response, Router } from 'express';

const mockLoggerError = vi.hoisted(() => vi.fn());
vi.mock('../utils/logger', () => ({
  logger: { error: mockLoggerError, warn: vi.fn(), info: vi.fn(), debug: vi.fn() },
}));
vi.mock('../middleware/auth', () => ({
  authenticateToken: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

import notificationsRouter from '../routes/notifications';

const REFUSAL = {
  success: false,
  error: { code: 'FORBIDDEN', message: 'A notification can only be created for the authenticated caller' },
};

type Captured = Response & { _status: number; _json: any };

function makeRes(onFinish: () => void): Captured {
  const res: any = {
    _status: 200,
    _json: null,
    status(code: number) {
      res._status = code;
      return res;
    },
    json(body: unknown) {
      res._json = body;
      onFinish();
      return res;
    },
    setHeader() {
      return res;
    },
  };
  return res;
}

function dispatch(router: Router, opts: { method: string; url: string; user?: unknown; body?: unknown }): Promise<Captured> {
  return new Promise((resolve, reject) => {
    const res = makeRes(() => resolve(res));
    const req = {
      method: opts.method,
      url: opts.url,
      headers: {},
      body: opts.body,
      query: {},
      user: opts.user,
      get(name: string) {
        return (this as any).headers[name?.toLowerCase()];
      },
    } as unknown as Request;
    router(req, res as any, (err: unknown) => (err ? reject(err) : resolve(res)));
  });
}

const post = (user: unknown, body: unknown) => dispatch(notificationsRouter, { method: 'POST', url: '/', user, body });

/** The rows a user can read. The store is process-local and keyed by userId, so each cell uses ids of its own. */
async function rowsOf(userId: string): Promise<any[]> {
  const res = await dispatch(notificationsRouter, { method: 'GET', url: '/', user: { userId } });
  return res._json?.data ?? [];
}

const BODY = { type: 'system', title: 'T', message: 'M' };

// Every principal the middleware can attach, and the role spellings a token can carry. A platform admin is here on
// purpose: the ruling says every principal, and isPlatformRole is deliberately not consulted.
const PRINCIPALS: ReadonlyArray<readonly [string, Record<string, unknown>]> = [
  ['a plain user', { userId: 'ks1448-user', role: 'user' }],
  ['an owner', { userId: 'ks1448-owner', role: 'OWNER' }],
  ['a verifier', { userId: 'ks1448-verifier', role: 'VERIFIER' }],
  ['an issuer admin', { userId: 'ks1448-issuer', role: 'ISSUER_ADMIN' }],
  ['an org admin', { userId: 'ks1448-org', role: 'ORG_ADMIN' }],
  ['a system admin', { userId: 'ks1448-system', role: 'SYSTEM_ADMIN' }],
  ['a super admin in the casing a JWT carries', { userId: 'ks1448-super-lower', role: 'super_admin' }],
  ['a super admin in upper case', { userId: 'ks1448-super-upper', role: 'SUPER_ADMIN' }],
  ['a platform_admin role', { userId: 'ks1448-platform', role: 'platform_admin' }],
  // The shape authenticateToken attaches for a valid sk_ key (middleware/auth.ts).
  ['a connector key', { userId: 'connector:ks1448-conn', role: 'connector', connectorId: 'ks1448-conn', authMethod: 'api_key' }],
];

beforeEach(() => mockLoggerError.mockClear());

describe('KS-1448: POST /api/notifications refuses a userId other than the caller', () => {
  it.each(PRINCIPALS)('RED KS-1448 R1: %s posting for another user gets 403 and no row is stored', async (label, user) => {
    const target = `ks1448-target-${label.replace(/\W+/g, '-')}`;
    const res = await post(user, { ...BODY, userId: target });
    expect(res._status).toBe(403);
    expect(res._json).toEqual(REFUSAL);
    expect(await rowsOf(target)).toEqual([]);
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('RED KS-1448 R2: the phishing shape, type security with an actionUrl, stores nothing for the target', async () => {
    const target = 'ks1448-target-phish';
    const res = await post({ userId: 'ks1448-phisher', role: 'user' }, { userId: target, type: 'security', title: 'Security alert', message: 'Please re-verify your account.', actionUrl: 'https://example.com/attacker' });
    expect(res._status).toBe(403);
    expect(await rowsOf(target)).toEqual([]);
  });

  it('RED KS-1448 R3: an id differing only in case or by a trailing space is another id', async () => {
    const user = { userId: 'ks1448-exact', role: 'user' };
    for (const near of ['KS1448-EXACT', 'ks1448-exact ', ' ks1448-exact']) {
      const res = await post(user, { ...BODY, userId: near });
      expect([near, res._status]).toEqual([near, 403]);
      expect(await rowsOf(near)).toEqual([]);
    }
  });

  it('RED KS-1448 R4: a token with no userId, or no user at all, stores nothing for anyone', async () => {
    for (const user of [{ role: 'user' }, undefined]) {
      const target = `ks1448-target-nouser-${user === undefined ? 'undefined' : 'role-only'}`;
      const res = await post(user, { ...BODY, userId: target });
      expect(res._status).toBe(403);
      expect(res._json).toEqual(REFUSAL);
      expect(await rowsOf(target)).toEqual([]);
    }
  });

  it('RED KS-1448 R5: the answer does not depend on whether the target has rows, which is why 403 and not 404', async () => {
    const known = 'ks1448-known';
    const seeded = await post({ userId: known, role: 'user' }, { ...BODY, userId: known });
    expect(seeded._status).toBe(201);
    const caller = { userId: 'ks1448-prober', role: 'user' };
    const onKnown = await post(caller, { ...BODY, userId: known });
    const onUnknown = await post(caller, { ...BODY, userId: 'ks1448-nobody' });
    expect([onKnown._status, onUnknown._status]).toEqual([403, 403]);
    expect(JSON.stringify(onKnown._json)).toBe(JSON.stringify(onUnknown._json));
    expect(JSON.stringify(onKnown._json)).not.toContain(known);
    expect((await rowsOf(known)).length).toBe(1);
  });
});

describe('KS-1448 controls: green before and after the check', () => {
  it.each([
    ['a plain user', { userId: 'ks1448-own-user', role: 'user' }],
    ['a system admin', { userId: 'ks1448-own-system', role: 'SYSTEM_ADMIN' }],
    // "connector keys refused except their own id": a key's own id is its connector:<id> principal.
    ['a connector key on its own id', { userId: 'connector:ks1448-own', role: 'connector' }],
  ] as const)('control KS-1448 C1: %s creates for its own id, and reads the row back', async (_label, user) => {
    const res = await post(user, { ...BODY, userId: user.userId });
    expect(res._status).toBe(201);
    expect(res._json?.data?.userId).toBe(user.userId);
    expect((await rowsOf(user.userId)).map((n) => n.id)).toEqual([res._json?.data?.id]);
  });

  it('control KS-1448 C2: own id with type security and an actionUrl still creates; only another inbox is refused', async () => {
    const user = { userId: 'ks1448-own-security', role: 'user' };
    const res = await post(user, { userId: user.userId, type: 'security', title: 'T', message: 'M', actionUrl: 'https://example.com/mine' });
    expect(res._status).toBe(201);
    expect(res._json?.data?.actionUrl).toBe('https://example.com/mine');
  });

  it.each([
    ['missing fields', { userId: 'ks1448-other' }],
    ['a type outside the enum', { userId: 'ks1448-other', type: 'nope', title: 'T', message: 'M' }],
    ['a non-string actionUrl', { userId: 'ks1448-other', type: 'system', title: 'T', message: 'M', actionUrl: 7 }],
    ['a data field that is an array', { userId: 'ks1448-other', type: 'system', title: 'T', message: 'M', data: [] }],
    ['a non-string userId', { userId: 7, type: 'system', title: 'T', message: 'M' }],
    ['an array userId holding the caller', { userId: ['ks1448-order'], type: 'system', title: 'T', message: 'M' }],
  ] as const)('control KS-1448 C3: the validators run first, %s keeps its 400 for a caller who would be refused', async (_label, body) => {
    const res = await post({ userId: 'ks1448-order', role: 'user' }, body);
    expect(res._status).toBe(400);
    expect(res._json?.error?.code).toBe('BAD_REQUEST');
  });

  it('control KS-1448 C4: an omitted userId stays 400 and is not defaulted to the caller', async () => {
    const user = { userId: 'ks1448-omitted', role: 'user' };
    const res = await post(user, BODY);
    expect(res._status).toBe(400);
    expect(res._json?.error?.code).toBe('BAD_REQUEST');
    expect(await rowsOf(user.userId)).toEqual([]);
  });
});

describe('KS-1448: the published spec says what the route does', () => {
  const SPEC = readFileSync(join(__dirname, '..', 'api-gateway.openapi.ts'), 'utf8');
  const at = SPEC.indexOf("method: 'post',\n  path: '/api/notifications',");
  const block = at === -1 ? '' : SPEC.slice(at, SPEC.indexOf('sharedRegistry.registerPath', at));

  it('RED KS-1448 S1: neither false line about internal callers is left in the route block', () => {
    expect(block.length).toBeGreaterThan(0);
    expect(block).not.toContain('service-to-service');
    expect(block).not.toContain('typically called by');
    expect(block).not.toContain('Used by backend services');
  });

  it('RED KS-1448 S2: the description states the refusal', () => {
    expect(block).toContain("any other value answers 403");
  });

  it('control KS-1448 S3: 403 stays declared on the route', () => {
    expect(block).toContain('403: commonErrorResponses[403]');
  });
});
