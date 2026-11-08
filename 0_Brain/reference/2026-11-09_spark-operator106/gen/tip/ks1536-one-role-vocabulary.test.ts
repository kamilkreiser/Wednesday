/**
 * KS-1536: one role vocabulary, without platform_admin.
 *
 * THE RULING. Kam, 2026-11-06 15:00:27 AEDT, card secuura-ks-1536-platform-admin-role-one-list-1106, option a, verbatim:
 * "One shared list without platform_admin, after a check". The check is on the ticket. Wednesday ruled the split and the
 * fold (ANSWER 2026-11-06T04:56:21Z, option A): this is PR 3a; the auth service's two lists are PR 3b, after a count.
 *
 * THE DEFECT. "Is this caller a platform role?" was answered by separate hard-coded lists that disagreed: platform_admin
 * was a super-role to the gateway and an ordinary user to the key policy, and nothing failed when they drifted.
 *
 * THE ONE LIST is PLATFORM_ROLES behind isPlatformRole in security/keyRevokePolicy.ts, which 15 product files already
 * import. Two named predicates answer the two OTHER questions some lists were answering: platform or organisation-bounded
 * admin, and platform or ORG_ADMIN. A new name, not a second list of platform roles.
 *
 * THE GUARD has the KS-764 call-site guard's shape: a source sweep over services, packages and frontends, with its own
 * planted-tree control, because a guard that cannot see a defect passes on anything. It proves wiring, not behaviour: the
 * gateway's behaviour is services/api-gateway ks1536-gateway-role-checks-are-the-shared-predicates.test.ts.
 */
import { beforeAll, describe, it, expect } from 'vitest';
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, relative, resolve, sep } from 'node:path';
import * as policy from '../security/keyRevokePolicy';

const predicates = policy as unknown as Record<string, ((role: unknown) => boolean) | undefined>;

function findDevRoot(start: string): string {
  let dir = start;
  for (let i = 0; i < 10; i++) {
    if (existsSync(join(dir, 'services')) && existsSync(join(dir, 'packages'))) return dir;
    dir = resolve(dir, '..');
  }
  throw new Error('Blockchain/Dev not found above ' + start);
}
const DEV = findDevRoot(__dirname);

const PLATFORM_YES = ['SYSTEM_ADMIN', 'system_admin', 'SUPER_ADMIN', 'super_admin', 'Super_Admin'];
// Dotless i and long s fold to I and S under toUpperCase(): KS 1591. An array stringifies to its element.
const SPOOFS: unknown[] = ['SUPER_ADMıN', 'ſUPER_ADMIN', 'ORG_ADMıN', 'ISSUER_ADMıN', 'ıssuer_admin', ['SUPER_ADMIN'], ['ORG_ADMIN']];
const ALWAYS_NO: unknown[] = ['platform_admin', 'PLATFORM_ADMIN', 'platform_viewer', 'ADMIN', 'admin', 'OWNER', 'VERIFIER', 'connector', '', undefined, null, ...SPOOFS];

describe('KS-1536: the predicates', () => {
  it.each(PLATFORM_YES)('control ks1536 P1 isPlatformRole admits %s', (role) => {
    expect(predicates.isPlatformRole?.(role)).toBe(true);
  });
  it.each([...ALWAYS_NO, 'ORG_ADMIN', 'ISSUER_ADMIN'].map((r) => [JSON.stringify(r) ?? 'undefined', r]))('control ks1536 P2 isPlatformRole refuses %s', (_l, role) => {
    expect(predicates.isPlatformRole?.(role)).toBe(false);
  });
  it.each([...PLATFORM_YES, 'ORG_ADMIN', 'org_admin', 'ISSUER_ADMIN', 'issuer_admin'])('RED ks1536 P3 isPlatformOrOrgBoundedRole admits %s', (role) => {
    expect(predicates.isPlatformOrOrgBoundedRole?.(role)).toBe(true);
  });
  it.each(ALWAYS_NO.map((r) => [JSON.stringify(r) ?? 'undefined', r]))('RED ks1536 P4 isPlatformOrOrgBoundedRole refuses %s', (_l, role) => {
    expect(predicates.isPlatformOrOrgBoundedRole?.(role)).toBe(false);
  });
  it.each([...PLATFORM_YES, 'ORG_ADMIN', 'org_admin'])('RED ks1536 P5 isPlatformOrOrgAdminRole admits %s', (role) => {
    expect(predicates.isPlatformOrOrgAdminRole?.(role)).toBe(true);
  });
  it.each([...ALWAYS_NO, 'ISSUER_ADMIN', 'issuer_admin'].map((r) => [JSON.stringify(r) ?? 'undefined', r]))('RED ks1536 P6 isPlatformOrOrgAdminRole refuses %s', (_l, role) => {
    expect(predicates.isPlatformOrOrgAdminRole?.(role)).toBe(false);
  });
  it('RED ks1536 P7 the shared barrel exports both new predicates and the guard', () => {
    const barrel = readFileSync(join(DEV, 'packages/shared/src/index.ts'), 'utf8');
    expect(barrel).toContain('isPlatformOrOrgBoundedRole');
    expect(barrel).toContain('isPlatformOrOrgAdminRole');
    expect(barrel).toContain('requirePlatformRole');
  });
});

describe('KS-1536: requirePlatformRole', () => {
  // No req.user is the shared requireRole's own 401 path; a role is admitted or refused exactly as isPlatformRole says.
  let mw: Record<string, unknown>;
  beforeAll(async () => { mw = (await import('../middleware/index')) as unknown as Record<string, unknown>; }, 60_000);
  async function run(user: unknown): Promise<string> {
    const factory = mw.requirePlatformRole as undefined | (() => (req: unknown, res: unknown, next: (e?: unknown) => void) => void);
    if (!factory) return 'absent';
    let out = 'not called';
    factory()({ user }, {}, (e?: unknown) => { out = e ? (e as { constructor: { name: string } }).constructor.name : 'next'; });
    return out;
  }
  it.each(PLATFORM_YES)('RED ks1536 M1 admits %s', async (role) => { expect(await run({ role })).toBe('next'); });
  it.each(['platform_admin', 'ORG_ADMIN', 'ADMIN', 'OWNER'])('RED ks1536 M2 refuses %s with ForbiddenError', async (role) => {
    expect(await run({ role })).toBe('ForbiddenError');
  });
  it('RED ks1536 M3 no user is UnauthorizedError', async () => { expect(await run(undefined)).toBe('UnauthorizedError'); });
});

// ---- the guard

const ROLE_LITERAL = /['"`]platform_?admin['"`]/i; // 'platform-admin', with a hyphen, is a decision reason in keyRevokePolicy.ts, not a role
const SPELLING = /['"`](?:super_?admin|system_?admin|platform_?admin)['"`]/i;
const LIST = /\[[^[\]]*?\]|\([^()]*?\)/gs;
// Not a role check. The RLS sentinel is a GUC value, every such line names its GUC. password.ts asks how long a password
// must be, and that spelling keeps the longer minimum: leaving it costs nothing, removing it would weaken a row that exists.
const NOT_A_ROLE_LINE = /tenant_scope_bypass/;
const NAMED_EXCEPTIONS = new Set(['services/auth/src/services/password.ts']);

function sourceFiles(root: string): string[] {
  const out: string[] = [];
  const walk = (dir: string): void => {
    for (const name of readdirSync(dir)) {
      if (name === 'node_modules' || name === 'dist' || name === '__tests__' || name === '__mocks__') continue;
      const p = join(dir, name);
      if (statSync(p).isDirectory()) walk(p);
      else if (/\.tsx?$/.test(name) && !/\.(test|spec|d)\.tsx?$/.test(name)) out.push(p);
    }
  };
  for (const top of ['services', 'packages', 'frontend']) {
    const t = join(root, top);
    if (!existsSync(t)) continue;
    for (const pkg of readdirSync(t)) {
      const src = join(t, pkg, 'src');
      if (existsSync(src)) walk(src);
    }
  }
  return out;
}

function sweep(root: string): { roleLines: string[]; listCounts: Record<string, number> } {
  const roleLines: string[] = [];
  const listCounts: Record<string, number> = {};
  for (const p of sourceFiles(root)) {
    const rel = relative(root, p).split(sep).join('/');
    const text = readFileSync(p, 'utf8');
    if (!NAMED_EXCEPTIONS.has(rel)) {
      text.split('\n').forEach((line, i) => {
        if (ROLE_LITERAL.test(line) && !NOT_A_ROLE_LINE.test(line)) roleLines.push(`${rel}:${i + 1}: ${line.trim().slice(0, 120)}`);
      });
    }
    const lists = (text.match(LIST) ?? []).filter((m) => m.length <= 1200 && SPELLING.test(m) && !NOT_A_ROLE_LINE.test(m)).length;
    if (lists > 0) listCounts[rel] = lists;
  }
  return { roleLines, listCounts };
}

describe('KS-1536: the guard', () => {
  const baseline = JSON.parse(readFileSync(join(__dirname, 'ks1536-inline-role-lists.baseline.json'), 'utf8')) as Record<string, number>;
  const here = sweep(DEV);

  it('RED ks1536 G1 platform_admin is a role nowhere in non-test source, outside the named exceptions', () => {
    expect(here.roleLines).toEqual([]);
  });

  it('RED ks1536 G2 no file holds more inline platform-role lists than the frozen baseline', () => {
    // The roughly 55 lists that omit platform_admin are baselined, not reconciled: each one is its own authorisation change.
    // A count below the baseline passes: lower the number in the same PR that removes a list.
    const over = Object.entries(here.listCounts).filter(([f, n]) => n > (baseline[f] ?? 0)).map(([f, n]) => `${f}: ${n} > ${baseline[f] ?? 0}`);
    expect(over).toEqual([]);
  });

  it('control ks1536 G3 the sweep can SEE a defect: a planted tree reds both rules, and ignores what it should', () => {
    const root = mkdtempSync(join(tmpdir(), 'ks1536-'));
    const src = join(root, 'services/planted/src');
    mkdirSync(join(src, '__tests__'), { recursive: true });
    writeFileSync(join(src, 'a.ts'), "const R = ['super_admin', 'platform_admin'];\n");
    writeFileSync(join(src, 'b.ts'), "const R = new Set(['SUPER_ADMIN', 'SYSTEM_ADMIN']);\n");
    writeFileSync(join(src, 'guc.ts'), "set_config('app.tenant_scope_bypass', 'platform_admin', true);\n");
    writeFileSync(join(src, '__tests__/t.test.ts'), "const R = ['platform_admin'];\n");
    writeFileSync(join(src, 'c.test.ts'), "const R = ['platform_admin'];\n");
    const planted = sweep(root);
    expect(planted.roleLines).toEqual(["services/planted/src/a.ts:1: const R = ['super_admin', 'platform_admin'];"]);
    expect(planted.listCounts).toEqual({ 'services/planted/src/a.ts': 1, 'services/planted/src/b.ts': 1 });
  });

  it('control ks1536 G4 the sweep reads the real tree: the one list and a known caller are found', () => {
    expect(here.listCounts['packages/shared/src/security/keyRevokePolicy.ts']).toBeGreaterThan(0);
    expect(sourceFiles(DEV).length).toBeGreaterThan(300);
  });

  it('RED ks1536 G5 tokenisation guards both key routes with requirePlatformRole and keeps no list of its own', () => {
    const t = readFileSync(join(DEV, 'services/tokenisation/src/index.ts'), 'utf8');
    expect(t.match(/requirePlatformRole\(\)/g)?.length).toBe(2);
    expect(t).not.toContain('PLATFORM_ADMIN_ROLES');
  });

  it('RED ks1536 G6 originate adminConfig resolves tenants by the shared predicate and keeps no list of its own', () => {
    const t = readFileSync(join(DEV, 'services/originate/src/routes/adminConfig.ts'), 'utf8');
    expect(t).not.toContain('SUPER_ADMIN_ROLES');
    expect(t).toMatch(/if \(isPlatformRole\(u\?\.role\)\) \{/);
  });

  it('RED ks1536 G7 the two portal role mappings no longer spell it', () => {
    expect(readFileSync(join(DEV, 'frontend/shared/src/auth/index.ts'), 'utf8')).not.toMatch(ROLE_LITERAL);
    expect(readFileSync(join(DEV, 'frontend/admin/src/store/authStore.ts'), 'utf8')).not.toMatch(ROLE_LITERAL);
  });
});
