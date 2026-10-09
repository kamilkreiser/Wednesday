import type { Request } from 'express';
import { isAllowedByRoleOrScope } from '../middleware/rbac';
import { DOCUMENT_WRITE_ROLES } from '../middleware/documentWriteRoles';

/**
 * KS-71 — scope-aware RBAC helper.
 *
 * The helper sits in front of every write route in originate. It must:
 *   - keep accepting JWT humans whose role is in the allow-list,
 *   - newly accept `sk_*` connector callers whose `scopes` array carries
 *     the required scope (or a `<resource>:*` / `*` wildcard),
 *   - reject anything else.
 */

const ALLOWED = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'];

function reqWith(user: { role?: string; scopes?: string[] } | null): Request {
  return { user } as unknown as Request;
}

describe('isAllowedByRoleOrScope (KS-71)', () => {
  it('accepts a role in the allow-list (uppercase match)', () => {
    const req = reqWith({ role: 'ISSUER_ADMIN' });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(true);
  });

  it('accepts a role in the allow-list (case-insensitive)', () => {
    const req = reqWith({ role: 'issuer_admin' });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(true);
  });

  it('accepts a connector role when the exact scope is granted', () => {
    const req = reqWith({ role: 'connector', scopes: ['documents:write'] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(true);
  });

  it('accepts a connector role when a resource wildcard is granted', () => {
    const req = reqWith({ role: 'connector', scopes: ['documents:*'] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(true);
  });

  it('accepts a connector role when the global wildcard is granted', () => {
    const req = reqWith({ role: 'connector', scopes: ['*'] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(true);
  });

  it('rejects a connector role with no scopes', () => {
    const req = reqWith({ role: 'connector', scopes: [] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(false);
  });

  it('rejects a connector role with a different-resource scope', () => {
    const req = reqWith({ role: 'connector', scopes: ['certifications:write'] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(false);
  });

  it('rejects a connector role with a read-only scope when write is required', () => {
    const req = reqWith({ role: 'connector', scopes: ['documents:read'] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(false);
  });

  it('rejects an out-of-allow-list role with no scopes (e.g. plain VERIFIER)', () => {
    const req = reqWith({ role: 'VERIFIER' });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(false);
  });

  it('accepts both paths combined (in-allow-list role + redundant scope)', () => {
    const req = reqWith({ role: 'ISSUER_ADMIN', scopes: ['documents:write'] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(true);
  });

  it('rejects when req.user is missing', () => {
    const req = reqWith(null);
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(false);
  });

  it('rejects when role and scopes are both undefined', () => {
    const req = reqWith({});
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(false);
  });

  // KS-151: OWNER (the role assigned to every self-registered user) carries
  // a `documents:write` scope by default (`getDefaultScopesForRole` in
  // `@secuura/shared/security/scopes`) so they pass the originate gate via
  // the scope path. Without this, /api/auth/register users hit 403 on the
  // first POST /api/documents.
  it('accepts OWNER carrying the default documents:write scope (KS-151)', () => {
    const req = reqWith({ role: 'OWNER', scopes: ['documents:write'] });
    expect(isAllowedByRoleOrScope(req, ALLOWED, 'documents:write')).toBe(true);
  });

  // Negative pair: the documents:write scope must NOT silently leak access
  // to sibling document verbs (share / transfer-custody) — those routes have
  // their own scope gates (KS-71). Confirms the OWNER grant is narrowly
  // bounded to the genesis/version write surface.
  it('KS-151: rejects OWNER + documents:write when documents:share is required', () => {
    const req = reqWith({ role: 'OWNER', scopes: ['documents:write'] });
    expect(
      isAllowedByRoleOrScope(req, ['ISSUER_ADMIN', 'ORG_ADMIN'], 'documents:share'),
    ).toBe(false);
  });

  it('KS-151: rejects OWNER + documents:write when documents:transfer-custody is required', () => {
    const req = reqWith({ role: 'OWNER', scopes: ['documents:write'] });
    expect(
      isAllowedByRoleOrScope(req, ['ISSUER_ADMIN', 'ORG_ADMIN'], 'documents:transfer-custody'),
    ).toBe(false);
  });
});

/**
 * KS-290 — transfer-custody must accept the document's own issuer/owner.
 *
 * The bug: `transfer-custody` (KS-68) shipped with a narrower role literal
 * (`ORG_ADMIN`/`SYSTEM_ADMIN`/`SUPER_ADMIN`) that omitted `ISSUER_ADMIN`, so
 * an `ISSUER_ADMIN` owner got 403 on their own document while every sibling
 * doc-write verb (create/version/share/sign-cert) let them through. The fix
 * unifies all doc-write verbs onto the shared `DOCUMENT_WRITE_ROLES` base so
 * the lists cannot drift apart again.
 *
 * These tests assert the gate against the REAL exported const (not a
 * hand-built copy), so a future edit that drops `ISSUER_ADMIN` from the base
 * — or re-narrows transfer-custody specifically — fails here.
 */
describe('DOCUMENT_WRITE_ROLES base — transfer-custody (KS-290)', () => {
  it('the shared base includes ISSUER_ADMIN (regression guard for the KS-290 drift)', () => {
    expect(DOCUMENT_WRITE_ROLES).toContain('ISSUER_ADMIN');
  });

  it('ISSUER_ADMIN passes the transfer-custody gate (KS-290 fix)', () => {
    const req = reqWith({ role: 'ISSUER_ADMIN' });
    expect(isAllowedByRoleOrScope(req, DOCUMENT_WRITE_ROLES, 'documents:transfer-custody')).toBe(true);
  });

  it('ORG_ADMIN still passes the transfer-custody gate (admin override preserved)', () => {
    const req = reqWith({ role: 'ORG_ADMIN' });
    expect(isAllowedByRoleOrScope(req, DOCUMENT_WRITE_ROLES, 'documents:transfer-custody')).toBe(true);
  });

  it('a connector with documents:transfer-custody scope passes (PS-124 sk_* path)', () => {
    const req = reqWith({ role: 'connector', scopes: ['documents:transfer-custody'] });
    expect(isAllowedByRoleOrScope(req, DOCUMENT_WRITE_ROLES, 'documents:transfer-custody')).toBe(true);
  });

  it('a connector with only documents:write does NOT pass transfer-custody (scope is verb-specific)', () => {
    const req = reqWith({ role: 'connector', scopes: ['documents:write'] });
    expect(isAllowedByRoleOrScope(req, DOCUMENT_WRITE_ROLES, 'documents:transfer-custody')).toBe(false);
  });

  it('public-signup OWNER + documents:write stays 403 on transfer-custody (KS-151 boundary preserved)', () => {
    const req = reqWith({ role: 'OWNER', scopes: ['documents:write'] });
    expect(isAllowedByRoleOrScope(req, DOCUMENT_WRITE_ROLES, 'documents:transfer-custody')).toBe(false);
  });
});

/**
 * KS-71 — full-route-shape integration coverage (one test, per Kam's
 * 2026-05-14 ask). The unit tests above exercise the helper in
 * isolation; this test wires the helper into a tiny Express POST
 * handler that mirrors `services/originate/src/routes/documents.ts:192`
 * exactly, then hits it with both an in-allow-list role token and a
 * connector token carrying `documents:write`. Both must 201; a
 * connector token without scope must 403.
 *
 * Goal: catch any future code change in the route that strips the
 * `req.user.scopes` field (or shape-shifts it to a different name)
 * before it ships. The unit-helper tests can't see that — they call
 * the helper directly with a hand-built `req.user`.
 */
import express from 'express';
import http from 'http';

describe('isAllowedByRoleOrScope — POST /api/documents shape (integration)', () => {
  function buildApp(): express.Express {
    const app = express();
    app.use(express.json());
    // Inject req.user from x-test-user header BEFORE the route. Keeps
    // the test self-contained without needing a real JWT verifier —
    // the helper only reads req.user.role + req.user.scopes, so the
    // injection is functionally equivalent to the gateway's JWT
    // middleware result.
    app.use((req, _res, next) => {
      const raw = req.headers['x-test-user'];
      if (typeof raw === 'string') (req as any).user = JSON.parse(raw);
      next();
    });
    app.post('/api/documents', (req, res) => {
      const allowed = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'];
      if (!isAllowedByRoleOrScope(req, allowed, 'documents:write')) {
        return res.status(403).json({ success: false, error: { code: 'FORBIDDEN' } });
      }
      return res.status(201).json({
        success: true,
        gatePath: (req as any).user?.role === 'connector' ? 'scope' : 'role',
      });
    });
    return app;
  }

  function callRoute(
    app: express.Express,
    user: Record<string, unknown> | null,
  ): Promise<{ status: number; body: any }> {
    return new Promise((resolve, reject) => {
      const server = app.listen(0, '127.0.0.1', () => {
        const addr = server.address();
        if (!addr || typeof addr === 'string') {
          server.close();
          return reject(new Error('Failed to get test server address'));
        }
        const req = http.request(
          {
            hostname: '127.0.0.1',
            port: addr.port,
            path: '/api/documents',
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...(user ? { 'x-test-user': JSON.stringify(user) } : {}),
            },
          },
          (res) => {
            let data = '';
            res.on('data', (c) => (data += c));
            res.on('end', () => {
              server.close();
              try {
                resolve({ status: res.statusCode || 500, body: data ? JSON.parse(data) : {} });
              } catch {
                resolve({ status: res.statusCode || 500, body: { raw: data } });
              }
            });
          },
        );
        req.on('error', (err) => {
          server.close();
          reject(err);
        });
        req.write(JSON.stringify({}));
        req.end();
      });
    });
  }

  it('200 for ISSUER_ADMIN; 200 for connector+documents:write; 403 for connector with no scope', async () => {
    const app = buildApp();

    const issuer = await callRoute(app, { role: 'ISSUER_ADMIN' });
    expect(issuer.status).toBe(201);
    expect(issuer.body.gatePath).toBe('role');

    const connectorWithScope = await callRoute(app, { role: 'connector', scopes: ['documents:write'] });
    expect(connectorWithScope.status).toBe(201);
    expect(connectorWithScope.body.gatePath).toBe('scope');

    const connectorNoScope = await callRoute(app, { role: 'connector', scopes: [] });
    expect(connectorNoScope.status).toBe(403);
    expect(connectorNoScope.body.error.code).toBe('FORBIDDEN');
  });
});
