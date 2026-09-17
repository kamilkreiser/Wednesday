/**
 * =============================================================================
 * KS-843 — THE `subjects:erase` GATE ON THE GDPR ERASURE ROUTES
 * =============================================================================
 * Kam ruled 2026-09-03: *"Dedicated scope `subjects:erase` — mint it for S's
 * key at registration; refuse others 403."*
 *
 * The refusal ships behind a switch because it cannot be turned on safely in
 * one step: every connector key issued before the scope existed lacks it, and
 * Platform K has no way to add a scope to an existing key (the security
 * service exposes create / list / revoke / validate — no PATCH, and no
 * `UPDATE svc_api_keys` anywhere in it). So `requireScopeOrRole` admits a
 * role-only caller and LOGS while `SUBJECTS_ERASE_SCOPE_ENFORCED` is unset,
 * and refuses once it is `'true'`.
 *
 * This file drives the middleware directly rather than through a server: the
 * behaviour under test is a decision about a principal, and a fake req/res
 * makes the branch that fires observable without a socket.
 *
 * NOTE ON LOCATION: the ruling named `services/originate/src/__tests__/`, but
 * the gate is gateway-side (`services/api-gateway/src/middleware/scopes.ts`,
 * mounted in `routes/proxy.ts`), so the test lives beside the code it tests.
 * Deviation stated rather than silently taken.
 * =============================================================================
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import type { Request, Response, NextFunction } from 'express';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { requireScopeOrRole } from '../middleware/scopes';
import { logger } from '../utils/logger';

const SCOPE = 'subjects:erase';
const ROLES = ['connector'] as const;
const FLAG = 'SUBJECTS_ERASE_SCOPE_ENFORCED';

type Captured = { status?: number; body?: unknown };

function drive(user: unknown): { captured: Captured; nexted: boolean } {
  const captured: Captured = {};
  let nexted = false;
  const req = {
    user,
    method: 'POST',
    originalUrl: '/api/gdpr/erasures',
  } as unknown as Request;
  const res = {
    status(code: number) { captured.status = code; return this; },
    json(payload: unknown) { captured.body = payload; return this; },
  } as unknown as Response;
  const next = (() => { nexted = true; }) as NextFunction;
  requireScopeOrRole(SCOPE, ROLES, FLAG)(req, res, next);
  return { captured, nexted };
}

const CONNECTOR_NO_SCOPE = {
  role: 'connector', authMethod: 'api_key', scopes: ['documents:read'],
  connectorId: 'conn-123', organizationId: 'org-abc', tenantId: 'tenant-1',
};
const CONNECTOR_WITH_SCOPE = { ...CONNECTOR_NO_SCOPE, scopes: ['documents:read', SCOPE] };

describe('KS-843 — subjects:erase gate', () => {
  let warn: ReturnType<typeof vi.spyOn>;
  const priorFlag = process.env[FLAG];

  beforeEach(() => {
    delete process.env[FLAG];
    warn = vi.spyOn(logger, 'warn').mockImplementation((() => logger) as never);
  });
  afterEach(() => {
    warn.mockRestore();
    if (priorFlag === undefined) delete process.env[FLAG];
    else process.env[FLAG] = priorFlag;
  });

  it('CONTROL — an unauthenticated caller is refused 401, so the cells below are about SCOPE, not about auth', () => {
    const { captured, nexted } = drive(undefined);
    expect(nexted).toBe(false);
    expect(captured.status).toBe(401);
  });

  it('🔴 GRACE (switch unset) — a role-only caller is ADMITTED and logged exactly once', () => {
    // The cell that makes this shippable: with the flag unset, Platform S's
    // existing key keeps working. If this ever reds, the cutover has broken a
    // live partner integration.
    const { nexted, captured } = drive(CONNECTOR_NO_SCOPE);
    expect(nexted).toBe(true);
    expect(captured.status).toBeUndefined();
    expect(warn).toHaveBeenCalledTimes(1);
    const [msg, meta] = warn.mock.calls[0] as [string, Record<string, unknown>];
    expect(msg).toContain('KS-843');
    // The log is the operator's instrument for deciding when to flip the
    // switch, so the fields it must carry are asserted by name.
    expect(meta).toMatchObject({
      requiredScope: SCOPE,
      role: 'connector',
      connectorId: 'conn-123',
      organizationId: 'org-abc',
      method: 'POST',
      route: '/api/gdpr/erasures',
      enforceFlag: FLAG,
    });
  });

  it('🔴 ENFORCING (switch = "true") — the same role-only caller is REFUSED 403 with a stable code', () => {
    process.env[FLAG] = 'true';
    const { nexted, captured } = drive(CONNECTOR_NO_SCOPE);
    expect(nexted).toBe(false);
    expect(captured.status).toBe(403);
    expect(captured.body).toMatchObject({
      success: false,
      error: { code: 'INSUFFICIENT_SCOPE', required: SCOPE },
    });
    // No grace line: the request was refused, not admitted.
    expect(warn).not.toHaveBeenCalled();
  });

  it('🔴 a caller HOLDING the scope passes in BOTH modes, and is never logged as a grace admission', () => {
    for (const mode of [undefined, 'true']) {
      warn.mockClear();
      if (mode === undefined) delete process.env[FLAG]; else process.env[FLAG] = mode;
      const { nexted, captured } = drive(CONNECTOR_WITH_SCOPE);
      expect(nexted, `flag=${String(mode)}`).toBe(true);
      expect(captured.status).toBeUndefined();
      expect(warn).not.toHaveBeenCalled();
    }
  });

  it('🔴 wildcards are honoured — `*` and `subjects:*` both grant, enforcing or not', () => {
    // requireScope's `includes()` would fail both of these. This gate uses
    // hasScope, so the shared vocabulary's wildcard rules actually apply.
    process.env[FLAG] = 'true';
    for (const scopes of [['*'], ['subjects:*']]) {
      const { nexted } = drive({ ...CONNECTOR_NO_SCOPE, scopes });
      expect(nexted, JSON.stringify(scopes)).toBe(true);
    }
  });

  it('🔴 the KS-835 authMethod hole is NOT inherited — an `email` principal with neither scope nor role is refused', () => {
    // requireScope() returns next() for any principal whose authMethod is
    // 'jwt' or 'email', and KS-835 records that OAuth-minted tokens carry the
    // 'email' label too. A new auth door must not inherit that branch.
    for (const authMethod of ['email', 'jwt']) {
      for (const flag of [undefined, 'true']) {
        if (flag === undefined) delete process.env[FLAG]; else process.env[FLAG] = flag;
        const { nexted, captured } = drive({ role: 'user', authMethod, scopes: [] });
        expect(nexted, `${authMethod}/${String(flag)}`).toBe(false);
        expect(captured.status).toBe(403);
      }
    }
  });

  it('🔴 a typo in the flag leaves the GRACE on — it must never silently start refusing', () => {
    // `!== 'true'` rather than `=== 'false'`: an operator who sets the flag to
    // "TRUE", "1" or "yes" gets the safe branch, not a broken partner.
    for (const v of ['TRUE', '1', 'yes', '', 'false']) {
      warn.mockClear();
      process.env[FLAG] = v;
      const { nexted } = drive(CONNECTOR_NO_SCOPE);
      expect(nexted, `flag=${v}`).toBe(true);
    }
  });

  it('🔴 MOUNT ORDER — the erasure gate is registered BEFORE the catch-all /api/gdpr mount', () => {
    // A gate registered after the catch-all is unreachable while looking
    // exactly like a gate.
    //
    // The first version of this cell used a bare `indexOf` and RED — because
    // the comment above the routes contains the words `router.use('/api/gdpr',
    // …)` while explaining the ordering. The reader found the PROSE before the
    // statement. Match a statement at the start of a line, never a substring.
    const src = readFileSync(join(__dirname, '..', 'routes', 'proxy.ts'), 'utf8');
    const all = [...src.matchAll(/^[ \t]*router\.use\('\/api\/gdpr'/gm)].map((m) => m.index as number);
    expect(all.length, 'CONTROL — both the gate mount and the catch-all must exist').toBe(2);
    const [gate, catchAll] = all;
    expect(gate).toBeLessThan(catchAll);
    // The gate mount is the one that invokes the door; the catch-all is the
    // proxy. Round 3 moved the chain into `erasureDoor`, declared above the
    // mount, so the assertion is now: the door is BUILT before the gate mount,
    // the gate mount INVOKES it, and the catch-all comes after both.
    const doorDecl = src.search(/^[ \t]*const erasureDoor = Router\(\);/m);
    expect(doorDecl, 'CONTROL — the door must be declared').toBeGreaterThan(-1);
    expect(doorDecl).toBeLessThan(gate);
    expect(src.slice(doorDecl, gate)).toContain('requireScopeOrRole(ERASURE_SCOPE');
    expect(src.slice(gate, catchAll)).toContain('erasureDoor(req, res,');
  });

  it('🔴 F-7 + F-9 — express does the matching, on the COLLAPSED path, so no spelling walks around it', () => {
    // The source half; the behavioural halves are the driven cells in
    // ks843-erasure-path-bypass.test.ts (six separator shapes, six case
    // shapes). Two fixes are pinned here because the second was caused by the
    // first: F-7's fix hand-rolled a matcher, and F-9 was that matcher being
    // case-sensitive where express is not.
    const src = readFileSync(join(__dirname, '..', 'routes', 'proxy.ts'), 'utf8');
    // The door is an express Router mounted at '/erasures' — express decides,
    // so case and trailing slash cannot drift from the rest of the file.
    expect(src).toMatch(/^[ \t]*const erasureDoor = Router\(\);/m);
    expect(src).toMatch(/^[ \t]*erasureDoor\.use\($/m);
    expect(src).toMatch(/^[ \t]*'\/erasures',$/m);
    // The one normalisation express will not do, and the reason it is needed.
    // KS-1187: it goes through collapseRepeatedSlashes, which leaves an
    // absolute-form target's scheme://authority alone, and the door is judged
    // on the canonical path. The whole-string collapse this line used to pin
    // was the KS-1187 bypass (`http://h/erasures` became `http:/h/erasures`, so
    // the door never matched); the control at the end forbids it in code.
    expect(src).toMatch(/erasureDoorVerdict\(collapseRepeatedSlashes\(original\), erasureDoorCaseSensitive\)/);
    // ...and req.url must be put back, or the gateway forwards a normalised
    // copy of what it was sent and the grace log disagrees with the upstream.
    expect(src).toMatch(/^[ \t]*req\.url = original;$/m);
    // CONTROL — the exact-route form that F-7 walked around must NOT come back.
    expect(src).not.toMatch(/^[ \t]*router\.post\('\/api\/gdpr\/erasures'/m);
    // CONTROL — nor the hand-rolled matcher that F-9 walked around. Stripped of
    // comment lines first: this file's own prose names the shapes it forbids,
    // and a check that greps for code must exclude the comments describing it.
    const code = src.split('\n').filter((l) => !/^\s*(\*|\/\*|\/\/)/.test(l)).join('\n');
    expect(code).not.toContain('ERASURE_SUBPATH');
    expect(code, 'a bare /erasures regex tested by hand is what F-9 was').not.toMatch(/\/\^\\\/erasures\(/);
    expect(code, 'KS-1187: a whole-string // collapse breaks absolute-form targets').not.toMatch(/replace\(\/\\\/\{2,\}\/g, '\/'\)/);
  });

  // RESTORED in round 3 (KS-843 F-10). The round-2 rewrite of this file went
  // 10 cells to 9 and reported it as `-1`; it was -3/+2, and this was one of
  // the three removed with no successor. `S_CONNECTOR_SCOPES` was then read
  // by no test in the repository, which is exactly the state #841's F-2 was
  // raised about. Restored verbatim from the parent commit 87450b54c.
  it('🔴 F-2 — the connector mint set equals the agreed contract set EXACTLY', () => {
    // The #841 gate found the mint set entirely uncovered: S_CONNECTOR_SCOPES
    // lives in one file, createPlatformRoutes is referenced by no test, and
    // "register-connector" appears in zero test files — so "the scope is
    // minted from now on" rested on READ evidence alone.
    //
    // EQUALITY, not toContain: an extra scope quietly appearing in the set a
    // partner's key is minted with is as much a defect as a missing one, and
    // toContain cannot see it.
    //
    // WHAT THIS CELL IS, HONESTLY: a source-structural read of the literal,
    // not a driven registration. It cannot see the route handler regress
    // around it — if `scopes` stopped being passed to the security service
    // altogether, this stays green. Driving the real handler needs a stubbed
    // security service plus the auth chain, which is its own piece of work;
    // the gap is named here rather than papered over.
    const src = readFileSync(join(__dirname, '..', 'routes', 'platform.ts'), 'utf8');
    const block = /const S_CONNECTOR_SCOPES = \[([\s\S]*?)\];/.exec(src);
    expect(block, 'CONTROL — the mint set must be findable, or this cell proves nothing').not.toBeNull();
    const minted = [...(block as RegExpExecArray)[1].matchAll(/'([^']+)'/g)].map((m) => m[1]);
    expect(minted).toEqual([
      'documents:write', 'documents:read', 'documents:share', 'documents:revoke',
      'documents:transfer-custody', 'certifications:write', 'anchors:read', 'anchors:write',
      'subjects:erase',
    ]);
  });
});
