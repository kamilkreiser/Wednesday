# KS-1585 m2 (gate on PR 1535, KS-1570 PR A): scripts/rls/verify-fail-closed.sh EXPECTED_TABLES lacks admin_organisation_scopes, so every verification run prints a DRIFT line. Spark operator 16. code_patch2: ONE one-token hunk in a shell script + 1 NEW vitest source-text file. gen: op16 patched mk2 (trailing-blank fix).
P='Blockchain/Dev/scripts/rls/verify-fail-closed.sh'
TP='Blockchain/Dev/services/security/src/__tests__/ks1585-rls-verifier-expects-admin-organisation-scopes.test.ts'
E1=('document_lifecycle_events action_provenance"\n',
    'document_lifecycle_events action_provenance admin_organisation_scopes"\n')
TEST='''// KS-1585 m2 (the Opus gate on PR 1535, KS-1570 PR A): migration 049 gave admin_organisation_scopes a FORCE row level security tenant_isolation policy, and the script
// scripts/rls/verify-fail-closed.sh derives its live set from the policies but keeps EXPECTED_TABLES as the spec for the other direction of the drift check. The table was missing
// from that spec, so every verification run printed a DRIFT line for it. These cells read the script and the migration as text. R1 is red until the table is in the spec;
// C1 to C4 pin what makes the expectation warranted and that the list was parsed (not an empty instrument).
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

// Blockchain/Dev, reached the way ks1434-api-key-create-spec-declares-rotate.test.ts does (__tests__ -> src -> security -> services -> Dev).
const devRoot = join(__dirname, '../../../..');
const SCRIPT = readFileSync(join(devRoot, 'scripts/rls/verify-fail-closed.sh'), 'utf8');
const MIGRATION = readFileSync(join(devRoot, 'migrations/049_admin_organisation_scopes.sql'), 'utf8');

const line = SCRIPT.match(/^EXPECTED_TABLES="([^"]*)"$/m);
const EXPECTED: string[] = line ? line[1].split(/\\s+/).filter(Boolean) : [];

describe('KS-1585 m2: the fail-closed verifier expects admin_organisation_scopes', () => {
  it('RED KS-1585 R1 EXPECTED_TABLES names admin_organisation_scopes', () => {
    expect(EXPECTED).toContain('admin_organisation_scopes');
  });

  it('control KS-1585 C1 migration 049 gives that table a FORCE row level security tenant_isolation policy (so the expectation is warranted)', () => {
    expect(MIGRATION).toContain('ALTER TABLE admin_organisation_scopes FORCE ROW LEVEL SECURITY;');
    expect(MIGRATION).toContain('CREATE POLICY tenant_isolation ON admin_organisation_scopes');
  });

  it('control KS-1585 C2 the list was parsed and still holds the older entries (the instrument is not reading an empty line)', () => {
    expect(EXPECTED.length).toBeGreaterThan(20);
    expect(EXPECTED).toContain('users');
    expect(EXPECTED).toContain('action_provenance');
  });

  it('control KS-1585 C3 no table is listed twice', () => {
    expect(new Set(EXPECTED).size).toBe(EXPECTED.length);
  });

  it('control KS-1585 C4 the script still derives its live set from tenant_isolation policies (the other direction of the drift check)', () => {
    expect(SCRIPT).toContain("WHERE policyname='tenant_isolation'");
  });
});
'''
S=dict(dir='ks_1585_p1_rls_expected_tables',ticket='KS-1585',
 title='security RLS verifier: EXPECTED_TABLES in scripts/rls/verify-fail-closed.sh lacks admin_organisation_scopes, so every run prints a DRIFT line (KS-1585 m2): add the one table name + a NEW source-text vitest file (RUNG 3, code_patch2: one one-token hunk in one shell script + one NEW test file; no logic changes)',
 intro="DRAFT by Spark operator 16 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / security) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. A ONE-TOKEN data fix in a verification script: the table list is the script's spec; nothing else changes. Origin: KS-1585 m2 (Opus gate on PR 1535, KS-1570 PR A: 'EXPECTED_TABLES without admin_organisation_scopes. The script's own selector picks the table up (measured), so every verification run prints a DRIFT line. Fix: add the table.'). ONLY m2 is in this brief; m1 (503 classifier), m3 (PR B write-time checks), n1 (a docstring whose wording depends on the policy status of KS-1535, which this operator could not confirm as ruled), n2 and n3 are not. Link the PR as Refs KS-1585, never a close-word.",
 products=[(P,[E1])],
 prodnote=['product (a shell script), modified in place: ONE hunk, one table name appended to one quoted list'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (1 red, 4 control; text reads of the script and migration 049)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1585-rls-verifier-expects-admin-organisation-scopes.test.ts` from `Blockchain/Dev/services/security',
 tier='code_patch2', rung='3 (two files: a one-token product hunk, a new test given whole)',
 pins='''# code_patch2: scripts/rls/verify-fail-closed.sh (one-token hunk) + a NEW vitest source-text file; ref = another security test that reads a repo file as text (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/security/src/__tests__/ks1434-api-key-create-spec-declares-rotate.test.ts
line=53
ctx=65536
''',
 wrong="`scripts/rls/verify-fail-closed.sh` verifies, as the app role, that every table carrying a fail-closed `tenant_isolation` policy shows 0 rows with no tenant context. It DERIVES its live set from `pg_policies` and keeps `EXPECTED_TABLES` (line 53) as the spec, so drift is caught in both directions: a table in the spec that lost its policy fails; a table that is fail-closed live but not in the spec prints `DRIFT <table> is fail-closed live but missing from EXPECTED_TABLES`. Migration 049 (`049_admin_organisation_scopes.sql`) created `admin_organisation_scopes` with FORCE row level security and a fail-closed `tenant_isolation` policy, but the table was never added to `EXPECTED_TABLES`, so every run prints that DRIFT line (the gate measured that the script's own selector picks the table up). Append `admin_organisation_scopes` to the end of the quoted list on line 53, and add a new vitest file that reads the script and the migration as text.",
 where="- `Blockchain/Dev/scripts/rls/verify-fail-closed.sh:53` - **must change**: the one line `EXPECTED_TABLES=\"...document_lifecycle_events action_provenance\"` gains ` admin_organisation_scopes` before the closing quote (the diff below gives it byte-exact). Line 54 is blank, line 55 starts the comment `# Live fail-closed set`.\n- `Blockchain/Dev/migrations/049_admin_organisation_scopes.sql` - (correct, STAYS) creates the table, `FORCE ROW LEVEL SECURITY` and the `tenant_isolation` policy the new cells read.",
 exactnote="ONE product hunk. The hunk ends with ONE blank context line (a single line containing just the diff marker, a space): that is intended, keep it.\n",
 donot="**Do NOT touch** any other line of the script, any other script, the migration, or any other file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. The new file is pure ASCII, uses `vitest` imports, reads the two files with `readFileSync` relative to `__dirname`, and has no top-level await.",
 red=['RED KS-1585 R1'],
 cells="- RED `R1`: at the tip `EXPECTED_TABLES` has no `admin_organisation_scopes`, so `toContain` fails by assertion.\n- GREEN at the tip and after: `C1` (migration 049 text), `C2` (list parsed, more than 20 entries, `users` and `action_provenance` present), `C3` (no duplicate), `C4` (the live-set query text is unchanged).\n- After the edit all five are green.",
 premises="- `scripts/rls/verify-fail-closed.sh:53` is the `EXPECTED_TABLES=\"...\"` line and `:54` is blank (read at the tip by script; the golden is generated from the tree at the tip, not typed).\n- `migrations/049_admin_organisation_scopes.sql` has `ALTER TABLE admin_organisation_scopes FORCE ROW LEVEL SECURITY;` and `CREATE POLICY tenant_isolation ON admin_organisation_scopes` (read at the tip).\n- The security service's vitest config includes `src/__tests__/*.test.ts` and excludes only `*.integration.test.ts`; the tip's `ks1434` test reads a repo file the same way.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The script itself was NOT run (it needs a live database as the app role); the claim that the DRIFT line prints today is the gate's measurement, restated.\n- Whether another table with a fail-closed policy is also missing from the list was not measured (that needs the live policy set).\n- The migration-number collision (two files numbered 049 at the tip and in PR 1383) is not part of this brief.",
 scope="**KS-1585 m2 only.** Link the PR as Refs KS-1585, never a close-word. No logic change.",
)
