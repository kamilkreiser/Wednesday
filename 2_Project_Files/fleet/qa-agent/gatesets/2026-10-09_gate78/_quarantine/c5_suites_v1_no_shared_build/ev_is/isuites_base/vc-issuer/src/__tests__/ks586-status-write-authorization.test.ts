/**
 * KS-586 regression: /api/status WRITES require an admin-class role.
 *
 * Before this gate, the status routes had no authorization of any kind — any
 * authenticated user (proven live with role OWNER) could create status lists
 * and revoke/un-revoke credentials. The gate is pinned AT THE ROUTE TABLE
 * (a router-level guard registered ahead of every route), so these tests
 * enumerate the router's actual route stack rather than a hand-kept list:
 * a future POST added to status.ts is covered by the same assertions
 * automatically.
 *
 * Tenant scoping is deliberately NOT asserted here — the ownership model is
 * the KS-539/KS-547/KS-586 joint decision and is tracked on KS-586.
 */

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import express, { NextFunction, Request, Response } from 'express';
import type { Server } from 'http';
import { statusRoutes, STATUS_WRITE_ROLES } from '../routes/status';
import { errorHandler } from '../middleware/errorHandler';

/** Build an app that authenticates every request as the role named in the x-test-role header. */
function buildApp(): express.Express {
  const app = express();
  app.use(express.json());
  app.use((req: Request, _res: Response, next: NextFunction) => {
    // The x-test-role header stands in for jwtAuthenticate: absent = anonymous.
    const role = req.header('x-test-role');
    if (role) {
      (req as Request & { user: unknown }).user = { userId: 'u-1', role, organizationId: 'org-1' };
    }
    next();
  });
  app.use('/api/status', statusRoutes);
  app.use(errorHandler);
  return app;
}

/** Every route registered on the router, read from the live route table. */
function routeTable(): Array<{ path: string; methods: string[] }> {
  const stack = (
    statusRoutes as unknown as {
      stack: Array<{ route?: { path: string; methods: Record<string, boolean> } }>;
    }
  ).stack;
  return stack
    .filter((layer) => layer.route)
    .map((layer) => ({
      path: layer.route!.path,
      methods: Object.keys(layer.route!.methods).filter((m) => layer.route!.methods[m]),
    }));
}

/** Substitute concrete params so a probe reaches the gate, not a 404. */
function concrete(path: string): string {
  return `/api/status${path.replace(':id', 'default').replace(':index', '0')}`;
}

let server: Server;
let baseUrl: string;

beforeAll(async () => {
  const app = buildApp();
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  if (address === null || typeof address === 'string') throw new Error('no ephemeral port');
  baseUrl = `http://127.0.0.1:${address.port}`;
});

afterAll(async () => {
  await new Promise<void>((resolve) => server.close(() => resolve()));
});

const writes = routeTable().filter((r) => r.methods.some((m) => m !== 'get' && m !== 'head'));
const reads = routeTable().filter((r) => r.methods.every((m) => m === 'get' || m === 'head'));

describe('KS-586 — status write authorization (route-table pin)', () => {
  it('the route table actually contains write routes (the pin is not vacuous)', () => {
    expect(writes.length).toBeGreaterThanOrEqual(4); // allocate, revoke, unrevoke, create
  });

  it.each(writes.map((r) => [r.methods.join(','), r.path] as const))(
    'non-privileged role gets 403 on %s %s (never reaches business logic)',
    async (_methods, path) => {
      const res = await fetch(`${baseUrl}${concrete(path)}`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-test-role': 'OWNER' },
        body: '{}',
      });
      expect(res.status).toBe(403);
    },
  );

  it.each(STATUS_WRITE_ROLES.map((r) => [r] as const))(
    '%s passes the gate (request reaches the handler, so status is never 401/403)',
    async (role) => {
      // Bogus body/params mean the handler may 400/404 — the assertion is
      // only that AUTHORIZATION passed, i.e. we got past the gate.
      const res = await fetch(`${baseUrl}/api/status/default/revoke`, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-test-role': role },
        body: '{}',
      });
      expect([401, 403]).not.toContain(res.status);
    },
  );

  it.each(reads.map((r) => [r.path] as const))(
    'reads stay authenticated-only: OWNER is not 403 on GET %s',
    async (path) => {
      const res = await fetch(`${baseUrl}${concrete(path)}`, {
        headers: { 'x-test-role': 'OWNER' },
      });
      expect(res.status).not.toBe(403);
    },
  );

  it('an anonymous request is refused (401) on a write, not role-403', async () => {
    const res = await fetch(`${baseUrl}/api/status/default/revoke`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: '{}',
    });
    expect(res.status).toBe(401);
  });
});
