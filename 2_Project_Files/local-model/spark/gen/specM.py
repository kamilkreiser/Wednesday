D='Blockchain/Dev/services/originate/src/routes/documents.ts'
C='Blockchain/Dev/services/originate/src/routes/certifications.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts'
LIT="userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin'"
D1=("import { verifyMessageSignature, hasNulByte, runWithTenantId, lookupHash, signEmitterHop } from '@secuura/shared';",
    "import { verifyMessageSignature, hasNulByte, runWithTenantId, lookupHash, signEmitterHop, isPlatformRole } from '@secuura/shared';")
D2=("      const userRole = user?.role as string | undefined;\n      const isAdmin = "+LIT+";\n",
    "      const userRole = user?.role as string | undefined;\n      const isAdmin = isPlatformRole(userRole);\n")
D3=("      const userRole = (req as any).user?.role as string | undefined;\n      const isAdmin = "+LIT+";\n",
    "      const userRole = (req as any).user?.role as string | undefined;\n      const isAdmin = isPlatformRole(userRole);\n")
C1=("  if (role === 'system_admin' || role === 'SYSTEM_ADMIN' || role === 'super_admin') return true;\n",
    "  if (isPlatformRole(role)) return true;\n")
C2=("      const isAdmin = "+LIT+";\n\n      const effectiveHolderId",
    "      const isAdmin = isPlatformRole(userRole);\n\n      const effectiveHolderId")
HP='Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts'
H1=("    base[key] = typeof value === 'function' ? jest.fn() : value;\n",
"    // KS-1701: isPlatformRole is a pure predicate over a role string. An inert jest.fn() answers undefined for every caller, which would turn every platform admin into an ordinary user in a suite\n    // that exercises an admin path through this mock, so it stays the real function (the only function export kept real).\n    base[key] = typeof value === 'function' && key !== 'isPlatformRole' ? jest.fn() : value;\n")
TEST='''// KS-1701 (originate routes/documents.ts and routes/certifications.ts): four places answered "is this caller a platform administrator?" with a hand-written literal that names
// system_admin, SYSTEM_ADMIN and super_admin and omits SUPER_ADMIN, so a platform administrator whose token carries that casing was treated as an ordinary user. The repo's own predicate
// isPlatformRole (packages/shared) upper-cases the claim and covers every spelling; the certification by-id read already uses it. These cells read the two route files as text (no app
// boot, no database) and pin that no hand-written role literal is left in either file, that documents.ts imports the predicate, and the number of call sites in each file.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const DOCUMENTS = readFileSync(join(__dirname, '..', 'routes', 'documents.ts'), 'utf8');
const CERTIFICATIONS = readFileSync(join(__dirname, '..', 'routes', 'certifications.ts'), 'utf8');

/** The number of non-overlapping occurrences of `needle` in `text`. */
function count(text: string, needle: string): number {
  return text.split(needle).length - 1;
}

describe('KS-1701: platform-admin checks in originate use isPlatformRole', () => {
  it('RED KS-1701 R1 documents.ts keeps no hand-written system_admin comparison', () => {
    expect(count(DOCUMENTS, "=== 'system_admin'")).toBe(0);
  });

  it('RED KS-1701 R2 certifications.ts keeps no hand-written system_admin comparison', () => {
    expect(count(CERTIFICATIONS, "=== 'system_admin'")).toBe(0);
  });

  it('RED KS-1701 R3 documents.ts imports isPlatformRole from the shared package', () => {
    expect(DOCUMENTS).toMatch(/import \\{[^}]*\\bisPlatformRole\\b[^}]*\\} from '@secuura\\/shared';/);
  });

  it('RED KS-1701 R4 documents.ts calls isPlatformRole at the list scoping and at the by-id read', () => {
    expect(count(DOCUMENTS, 'isAdmin = isPlatformRole(userRole);')).toBe(2);
  });

  it('RED KS-1701 R5 certifications.ts calls isPlatformRole at the list scoping and at callerMayCertifyDocument', () => {
    expect(count(CERTIFICATIONS, 'isAdmin = isPlatformRole(userRole);')).toBe(1);
    expect(count(CERTIFICATIONS, 'if (isPlatformRole(role)) return true;')).toBe(1);
  });

  it('control KS-1701 C1 certifications.ts still imports isPlatformRole exactly once', () => {
    expect(count(CERTIFICATIONS, "import { isPlatformRole } from '@secuura/shared';")).toBe(1);
  });

  it('control KS-1701 C2 the certification by-id read helper still calls isPlatformRole on the authenticated role', () => {
    expect(CERTIFICATIONS).toContain('if (isPlatformRole(authUser?.role as string | undefined)) return true;');
  });

  it('control KS-1701 C3 callerMayCertifyDocument still checks the owner', () => {
    expect(CERTIFICATIONS).toContain('  if (document.owner?.id && document.owner.id === userId) return true;');
  });

  it('control KS-1701 C4 documents.ts still imports sanitizeString and the other shared names it had', () => {
    expect(DOCUMENTS).toContain("import { sanitizeString } from '@secuura/shared/security';");
    expect(DOCUMENTS).toContain('verifyMessageSignature, hasNulByte, runWithTenantId, lookupHash, signEmitterHop');
  });
});
'''
S=dict(dir='ks_1701_p1',ticket='KS-1701',
 title='originate: four hand-written platform-admin role literals in routes/documents.ts and routes/certifications.ts omit SUPER_ADMIN; call the repo predicate isPlatformRole (RUNG 3, code_patch2: 2 products, 5 hunks, + one NEW source-text jest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 4 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. The ticket is facts-only ('no remedy proposed'); the fix shape here (call `isPlatformRole`, which the ticket names as the repo's own predicate and which originate already uses at certifications.ts and adminConfig.ts) is the drafter's, and it WIDENS access for the SUPER_ADMIN casing (a platform administrator is now treated as one). The fifth site in the ticket (adminConfig.ts SUPER_ADMIN_ROLES, which includes platform_admin) is a different kind and is NOT touched. The Spark may fail this one (capability data).",
 products=[(D,[D1,D2,D3]),(C,[C1,C2])],
 prodnote=['product 1, modified in place: THREE hunks - the shared import gains `isPlatformRole`, then two one-line replacements of the hand-written literal','product 2, modified in place: TWO hunks - two one-line replacements of the hand-written literal; the import is already there'],
 tests=[dict(path=TP,content=TEST),dict(path=HP,new=False,edits=[H1])],
 testnote=['NEW file, jest, given in full below; 9 cells (source-text pins)','SUPPORT test helper, modified in place: ONE hunk - the shared-module mock keeps isPlatformRole real'],
 runner='jest` (`npx jest src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch2', rung='3 (five hunks in two products given byte-exact; the new test given whole)',
 pins='''# code_patch2: 2 products in services/originate (documents.ts 3 hunks; certifications.ts 2 hunks) + 1 NEW source-text jest file; ref = ks1695 (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/originate/src/__tests__/ks1695-certification-reads-need-issuer-holder-or-admin.test.ts
line=48
ctx=65536
''',
 wrong="Four places in `services/originate` decide 'is this caller a platform administrator?' with the same hand-written literal `role === 'system_admin' || role === 'SYSTEM_ADMIN' || role === 'super_admin'`: the documents LIST scoping (`routes/documents.ts:300`), the `GET /api/documents/:id` cross-tenant fallback (`:1101`), the certifications LIST scoping (`routes/certifications.ts:964`) and `callerMayCertifyDocument` (`:123`). All four omit `SUPER_ADMIN` (the upper-case spelling), so a platform administrator whose token carries it is treated as an ordinary user; the identical omission copied into a new access check caused a measured regression during KS-1695, fixed by calling `isPlatformRole`. The change replaces each literal with `isPlatformRole(<the same role variable>)` and adds `isPlatformRole` to documents.ts's existing `@secuura/shared` import (certifications.ts already imports it). The predicate upper-cases the claim and covers `SYSTEM_ADMIN` and `SUPER_ADMIN`, so every spelling the literal accepted is accepted now, plus `SUPER_ADMIN` and mixed-case spellings.",
 where="- `routes/documents.ts:48` - **must change**: add `, isPlatformRole` at the end of the named imports of the one `@secuura/shared` import line.\n- `routes/documents.ts:300` and `:1101` - **must change**: the line `const isAdmin = userRole === 'system_admin' || ...;` becomes `const isAdmin = isPlatformRole(userRole);` (the `userRole` line above each is context and unchanged).\n- `routes/certifications.ts:123` - **must change**: `if (role === 'system_admin' || ...) return true;` becomes `if (isPlatformRole(role)) return true;`.\n- `routes/certifications.ts:964` - **must change**: the `isAdmin` line becomes `const isAdmin = isPlatformRole(userRole);`.\n- Every other line of both files, the `adminConfig.ts` set that includes `platform_admin`, and `packages/shared` are NOT touched.",
 exactnote="FIVE hunks in two files: documents.ts three (import, :300, :1101), certifications.ts two (:123, :964). Each replaced line is quoted whole.\n",
 donot="**Do NOT touch** any other line of the two files, `adminConfig.ts`, the shared package, or any other file.",
 testnote2="The FIRST test file (`ks1701-...test.ts`) is a NEW file, given whole: its `+` lines are the entire file, byte for byte; pure ASCII, jest globals, no top-level await, it reads the two route files with `readFileSync` from `__dirname/../routes` and boots no app. The SECOND (`helpers/sharedModuleMock.ts`) is an EXISTING file edited in place by the ONE hunk shown, nothing else.",
 red=['RED KS-1701 R1','RED KS-1701 R2','RED KS-1701 R3','RED KS-1701 R4','RED KS-1701 R5'],
 cells="- RED `R1` to `R5`: at the tip the files still hold the hand-written literal (counts 2 and 2), documents.ts does not import the predicate, and the call-site strings are absent; after the edit the counts are 0, the import matches and the call-site counts are 2, 1 and 1.\n- CONTROL `C1` to `C4`: green at the tip AND after (certifications.ts imports `isPlatformRole` once and the by-id helper calls it; the owner check still follows the admin line; documents.ts keeps its other shared imports).",
 premises="- documents.ts :48 is the `@secuura/shared` import quoted above; :300 and :1101 are the two lines `      const isAdmin = userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin';`, each preceded by a `userRole` declaration (read from the cache clone at the tip; line numbers have moved from the ticket's 299/1076).\n- certifications.ts :57 imports `isPlatformRole`, :123 and :964 are the literals, :169 is the by-id helper's call.\n- The originate test runner is jest; tests that mock `@secuura/shared` go through `helpers/sharedModuleMock`, which turns every function export (isPlatformRole included) into an inert `jest.fn()`: a suite that mocks the shared module AND relies on an admin path in documents.ts could change result. NOT measured here beyond the harness suite check.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether an existing suite drives an admin path in documents.ts through the shared-module mock (the harness's whole-suite check measures this; a red there is the finding).\n- The behaviour change itself (SUPER_ADMIN and mixed-case spellings are now platform admins at these four sites) is not observed on the wire: the cells are source-text pins.\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes the four-site part of KS-1701** (the fifth site in adminConfig.ts, the `platform_admin` question and KS-1536's vocabulary decision stay open). Link the PR as Refs KS-1701, never a close-word.",
)
