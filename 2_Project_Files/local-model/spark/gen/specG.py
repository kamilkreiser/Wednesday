P='Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts'
TP='Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts'
OLD="  return PLATFORM_ROLES.has(String(role || '').toUpperCase());\n"
NEW='''  // KS-1591: `String(role).toUpperCase()` is not an identity test. U+0131 (dotless i) upper-cases to `I`, U+017F (long s) upper-cases to `S`, and an ARRAY role stringifies to its element, so all three
  // read as SUPER_ADMIN. Only an ASCII fold is applied (a-z to A-Z, every other character untouched), and a role that is not a string is refused outright.
  if (typeof role !== 'string') return false;
  return PLATFORM_ROLES.has(role.replace(/[a-z]/g, (ch) => ch.toUpperCase()));
'''
TEST='''// KS-1591 (packages/shared security/keyRevokePolicy.ts isPlatformRole): the predicate decided "platform administrator" with `String(role || '').toUpperCase()`, which is not an identity test.
// U+0131 (dotless i) upper-cases to `I` and U+017F (long s) upper-cases to `S`, so `super_admin` spelled with either read as SUPER_ADMIN; and a role ARRAY stringifies to its element, so
// `['SUPER_ADMIN']` read as SUPER_ADMIN too. R1 to R5 pin that each of those is refused; C1 to C6 pin that every spelling the platform really uses is still admitted and that an ordinary role,
// an empty role and an absent role are still refused; D1 and D2 go through decideTenantAccess, the caller of the predicate, so the refusal is seen where the decision is made.
// All non-ASCII characters are written as \\u escapes so this file is pure ASCII.
import { describe, it, expect } from 'vitest';
import { isPlatformRole, decideTenantAccess } from '../index';

const DOTLESS_I = '\\u0131';
const LONG_S = '\\u017f';

function asRole(value: unknown): string | undefined {
  return value as string | undefined;
}

describe('KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role', () => {
  it('RED KS-1591 R1 a role spelled with a dotless i is not a platform role', () => {
    expect(isPlatformRole('super_adm' + DOTLESS_I + 'n')).toBe(false);
  });

  it('RED KS-1591 R2 a role spelled with a long s is not a platform role', () => {
    expect(isPlatformRole(LONG_S + 'uper_admin')).toBe(false);
  });

  it('RED KS-1591 R3 a role array holding SUPER_ADMIN is not a platform role', () => {
    expect(isPlatformRole(asRole(['SUPER_ADMIN']))).toBe(false);
  });

  it('RED KS-1591 R4 a role array holding system_admin is not a platform role', () => {
    expect(isPlatformRole(asRole(['system_admin']))).toBe(false);
  });

  it('RED KS-1591 R5 a system admin role spelled with a long s is not a platform role', () => {
    expect(isPlatformRole(LONG_S + 'ystem_admin')).toBe(false);
  });

  it('control KS-1591 C1 SUPER_ADMIN and SYSTEM_ADMIN are platform roles', () => {
    expect(isPlatformRole('SUPER_ADMIN')).toBe(true);
    expect(isPlatformRole('SYSTEM_ADMIN')).toBe(true);
  });

  it('control KS-1591 C2 super_admin and system_admin are platform roles', () => {
    expect(isPlatformRole('super_admin')).toBe(true);
    expect(isPlatformRole('system_admin')).toBe(true);
  });

  it('control KS-1591 C3 a mixed-case spelling is a platform role', () => {
    expect(isPlatformRole('Super_Admin')).toBe(true);
    expect(isPlatformRole('sYsTeM_aDmIn')).toBe(true);
  });

  it('control KS-1591 C4 ordinary roles are not platform roles', () => {
    expect(isPlatformRole('ADMIN')).toBe(false);
    expect(isPlatformRole('ISSUER_ADMIN')).toBe(false);
    expect(isPlatformRole('user')).toBe(false);
  });

  it('control KS-1591 C5 an empty role and an absent role are not platform roles', () => {
    expect(isPlatformRole('')).toBe(false);
    expect(isPlatformRole(undefined)).toBe(false);
    expect(isPlatformRole(asRole(null))).toBe(false);
  });

  it('control KS-1591 C6 a role with surrounding whitespace is still not a platform role', () => {
    expect(isPlatformRole(' SUPER_ADMIN')).toBe(false);
    expect(isPlatformRole('SUPER_ADMIN ')).toBe(false);
  });

  it('RED KS-1591 D1 decideTenantAccess does not give a dotless-i role the platform-admin pass', () => {
    const decision = decideTenantAccess({ role: 'super_adm' + DOTLESS_I + 'n', tenantId: 'tenant-a' }, 'tenant-b');
    expect(decision.allow).toBe(false);
  });

  it('control KS-1591 D2 decideTenantAccess still gives super_admin the platform-admin pass', () => {
    const decision = decideTenantAccess({ role: 'super_admin', tenantId: 'tenant-a' }, 'tenant-b');
    expect(decision).toEqual({ allow: true, reason: 'platform-admin' });
  });
});
'''
S=dict(dir='ks_1591_p1',ticket='KS-1591',
 title='(packages/shared half) isPlatformRole uses String(role).toUpperCase(), which admits a dotless-i, a long-s and an ARRAY role as SUPER_ADMIN; use an ASCII fold and refuse a non-string (RUNG 2, code_patch: one 4-line replacement + one NEW vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 3 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Security-adjacent but it fails toward LESS access (a platform-role claim that was wrongly admitted is now refused). Only the shared predicate `isPlatformRole` changes; `requireKeyAdmin` in services/security is the other half of the ticket and is a different package (the tier refuses two packages), and `isOrgBoundedRole` / `isScopedAdminRole` are left alone on purpose because refusing a non-string role there would REMOVE a restriction. The Spark may fail this one (capability data).",
 products=[(P,[(OLD,NEW)])],
 prodnote=['product, modified in place: ONE hunk, one line replaced by four lines'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 13 cells'],
 runner='vitest` (`npx vitest run src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts` from `Blockchain/Dev/packages/shared',
 tier='code_patch', rung='2 (one hunk given byte-exact; the new test given whole)',
 pins='''# code_patch, ONE hunk in packages/shared + a NEW vitest file; ref = the shared error-handler spec (shape only); line = the changed line.
tier=code_patch
ref=Blockchain/Dev/packages/shared/src/__tests__/error-handler.test.ts
line=141
ctx=65536
''',
 wrong="`isPlatformRole` (`packages/shared/src/security/keyRevokePolicy.ts:140-142`) decides 'is this caller a platform administrator' with `PLATFORM_ROLES.has(String(role || '').toUpperCase())`. `toUpperCase` is not an identity test: U+0131 (dotless i) upper-cases to `I`, U+017F (long s) upper-cases to `S`, and `String(['SUPER_ADMIN'])` is `'SUPER_ADMIN'`, so `super_admin` spelled with either character and a role ARRAY read as SUPER_ADMIN (the pull request 1539 gate measured 200 and 201 on the key routes for all three). The change replaces the one `return` line with four lines: a refusal of any role that is not a string, then the same set lookup over an ASCII-only fold (`role.replace(/[a-z]/g, (ch) => ch.toUpperCase())`). Every ASCII spelling that was admitted before is admitted now (`SUPER_ADMIN`, `super_admin`, `Super_Admin`, `sYsTeM_aDmIn`); an empty, absent or ordinary role is refused as before. Reachability of such a token is NOT established (the ticket says so); the severity is a nit until measured.",
 where="- `packages/shared/src/security/keyRevokePolicy.ts:141` - **must change**: the single line `  return PLATFORM_ROLES.has(String(role || '').toUpperCase());` inside `isPlatformRole` is replaced by the four lines (two comment lines, the `typeof` refusal, the new `return`) under \"The exact change\". The function signature, its doc comment and the closing brace are NOT touched.\n- `isOrgBoundedRole` (:96-98) and `isScopedAdminRole` (:101-103) use the same `String(role || '').toUpperCase()` and are (correct for this brief) NOT touched: refusing a non-string role there would remove a restriction, which is a decision for the owner.\n- `services/security/src/index.ts` `requireKeyAdmin` is the other half of the ticket and is a different package; NOT touched.",
 exactnote="ONE hunk: one line removed, four lines added.\n",
 donot="**Do NOT touch** any other line of `keyRevokePolicy.ts`, `PLATFORM_ROLES`, `index.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII (the two non-ASCII characters are written as `\\u0131` and `\\u017f` escapes inside string literals). Imports `isPlatformRole` and `decideTenantAccess` from `'../index'`, as ks780 does for `decideKeyRevoke`.",
 red=['RED KS-1591 R1','RED KS-1591 R2','RED KS-1591 R3','RED KS-1591 R4','RED KS-1591 R5','RED KS-1591 D1'],
 cells="- RED `R1` (dotless i), `R2` (long s), `R5` (long s on system_admin), `R3`/`R4` (role arrays): at the tip `toUpperCase`/`String` make each of them a platform role, so `isPlatformRole` returns true and the assertion `toBe(false)` fails; after the edit all five are false.\n- RED `D1`: at the tip `decideTenantAccess` gives the dotless-i role the `platform-admin` pass across tenants (`allow: true`); after the edit it is not a platform role and the cross-tenant compare denies it.\n- CONTROL `C1` to `C6`, `D2`: green at the tip AND after (every ASCII casing still admitted; ADMIN, ISSUER_ADMIN, user, empty, undefined, null and whitespace-padded spellings still refused; super_admin still gets the `platform-admin` pass).",
 premises="- `keyRevokePolicy.ts:141` is `  return PLATFORM_ROLES.has(String(role || '').toUpperCase());` and `PLATFORM_ROLES` (:60) is `new Set(['SYSTEM_ADMIN', 'SUPER_ADMIN'])`, read from the cache clone at the tip.\n- `isPlatformRole` and `decideTenantAccess` are exported from `packages/shared/src/index.ts` (:229, :230).\n- `decideTenantAccess({role:'super_admin',tenantId:'tenant-a'}, 'tenant-b')` returns `{ allow: true, reason: 'platform-admin' }` through its first arm (`keyRevokePolicy.ts:172-174`).\n- The package test runner is vitest; the golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether any issuer or seed path can sign a token carrying such a role: NOT established (the ticket says so).\n- How D1's dotless-i caller is decided after the change (a cross-tenant 403 is expected from the compare at :180-183; the cell asserts only `allow === false`).\n- Open PRs touching this file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the packages/shared `isPlatformRole` half of KS-1591.** `requireKeyAdmin` and the sweep for other `toUpperCase()` role comparisons stay open. Link the PR as Refs KS-1591, never a close-word.",
)
