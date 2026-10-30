# KS-1585 n1: security ks1533 test: stale 'UNDECIDED POLICY, KS-1535' docstring on PLAIN_ADMIN_A. Spark operator 19. code_patch2: ONE comment line replaced + 1 NEW vitest source-text file.
P='Blockchain/Dev/services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts'
TP='Blockchain/Dev/services/security/src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts'
OLD="/** `ADMIN`: a KEY_ADMIN_ROLE the arm never engages for. UNDECIDED POLICY, KS-1535. */\n"
NEW="/** `ADMIN`: a KEY_ADMIN_ROLE bounded by its admin organisation scope. RULED, KS-1570 (shape b). */\n"
TEST='''/**
 * KS-1585 n1 - the `PLAIN_ADMIN_A` docstring in ks1533-key-mint-organisation-arm.test.ts must state the ruling.
 *
 * That docstring said `ADMIN` is a key-admin role "the arm never engages for. UNDECIDED POLICY, KS-1535." Kam ruled the policy
 * in KS-1570 (shape b: each ADMIN acts only for the organisations in its admin organisation scope) and the cell that uses
 * `PLAIN_ADMIN_A` was rewritten to RULED, but the docstring on the fixture was left stating the old, wrong position. These are
 * source-text cells: they read the sibling file as text, so no server is started.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const lines = readFileSync(join(__dirname, 'ks1533-key-mint-organisation-arm.test.ts'), 'utf8').split('\\n');
const docstring = lines.find((l) => l.startsWith('/** `ADMIN`:')) ?? 'NO ADMIN DOCSTRING';
const fixtureIndex = lines.findIndex((l) => l.startsWith('const PLAIN_ADMIN_A ='));

describe('KS-1585 n1: the PLAIN_ADMIN_A docstring states the KS-1570 ruling', () => {
  it('RED KS-1585 L1 the docstring no longer calls the ADMIN policy UNDECIDED', () => {
    expect(docstring).not.toMatch(/UNDECIDED/);
  });

  it('RED KS-1585 L2 the docstring names the ruling (RULED, KS-1570)', () => {
    expect(docstring).toMatch(/RULED, KS-1570/);
  });

  it('CONTROL KS-1585 L3 the docstring sits directly above the PLAIN_ADMIN_A fixture', () => {
    expect(fixtureIndex).toBeGreaterThan(0);
    expect(lines[fixtureIndex - 1]).toBe(docstring);
  });

  it('CONTROL KS-1585 L4 the RULED cell the docstring points to still exists in the file', () => {
    expect(lines.some((l) => l.includes("it('RULED (KS-1570, shape b): role `ADMIN` is bounded by its admin organisation scope"))).toBe(true);
  });
});
'''
S=dict(dir='ks_1585_p1_admin_docstring_ruled',ticket='KS-1585',
 title="security ks1533-key-mint-organisation-arm.test.ts:80: the PLAIN_ADMIN_A docstring still says UNDECIDED POLICY, KS-1535 after KS-1570 ruled it (KS-1585 n1): reword to RULED (RUNG 3, code_patch2: one comment line + one NEW source-text vitest file; no behaviour changes)",
 intro="DRAFT by Spark operator 19 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / security service, TEST FILE comment only) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. A COMMENT fix in a test file: no product code, no behaviour change, no test cell of ks1533 changes. Origin: KS-1585 nit n1 (pull request 1535 gate). ONLY n1 is in this brief: n2, n3 and m1-m3 are separate decisions or code. The sibling docstring at :82 (`platform_admin ... UNDECIDED, KS-1535`) is NOT part of n1 and is NOT touched. Link the PR as Refs KS-1585, never a close-word. No open PR touches services/security (checked 2026-10-30 against the GitHub pulls API per-PR file lists).",
 products=[(P,[(OLD,NEW)])],
 prodnote=['a TEST file used as the edited file, modified in place: ONE hunk, the one docstring line at :80 replaced by one line'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 4 cells (2 red, 2 control); source-text reads of the file above, no server'],
 runner='vitest` (`npx vitest run src/__tests__/ks1585-ks1533-admin-docstring-states-the-ruling.test.ts` from `Blockchain/Dev/services/security',
 tier='code_patch2', rung='3 (two files: an existing file with a one-line comment hunk, a new test given whole)',
 pins='''# code_patch2: security ks1533 test file (1 comment hunk, used as the edited file) + a NEW vitest source-text file; ref = another security test that reads a file as text (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/security/src/__tests__/ks1434-api-key-create-spec-declares-rotate.test.ts
line=80
ctx=65536
''',
 wrong="In `services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts` the docstring on the `PLAIN_ADMIN_A` fixture (:80) reads `/** `ADMIN`: a KEY_ADMIN_ROLE the arm never engages for. UNDECIDED POLICY, KS-1535. */`. KS-1570 ruled that policy (Kam, shape b: an ADMIN acts only for the organisations in its admin organisation scope), the file's header (:33-37) says so and the cell at :205-216 is already `RULED (KS-1570, shape b)` and asserts a 403, but this docstring still states the old position that the arm never engages for `ADMIN`. Reword the one line so it states the ruling.",
 where="- `services/security/src/__tests__/ks1533-key-mint-organisation-arm.test.ts:80` - **must change**: the one docstring line `/** `ADMIN`: a KEY_ADMIN_ROLE the arm never engages for. UNDECIDED POLICY, KS-1535. */` becomes `/** `ADMIN`: a KEY_ADMIN_ROLE bounded by its admin organisation scope. RULED, KS-1570 (shape b). */` (byte-exact in the diff below).\n- `:81` (`const PLAIN_ADMIN_A = ...`), `:82-83` (the `platform_admin` docstring and fixture, NOT part of n1), the header at :33-37 and the cell at :205-216 - (correct, STAY).",
 exactnote="ONE comment hunk, one line replaced by one line. The edited file is itself a test file; its cells are unchanged.\n",
 donot="**Do NOT touch** any other line of `ks1533-key-mint-organisation-arm.test.ts` (the `platform_admin` docstring at :82 least of all), any product file, or any other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It reads the sibling file as text with `readFileSync` and has no top-level await. The backticks inside the template-free strings are as written.",
 red=['RED KS-1585 L1','RED KS-1585 L2'],
 cells="- RED `L1` (the docstring does not contain `UNDECIDED`) and `L2` (it matches `RULED, KS-1570`): both fail by assertion at the tip, pass after the edit.\n- GREEN at the tip and after: `L3` (the docstring is directly above the `const PLAIN_ADMIN_A =` line) and `L4` (the RULED cell title the docstring points to still exists).",
 premises="- `ks1533-key-mint-organisation-arm.test.ts:80` is the docstring, :81 the fixture, :205-216 the RULED cell, :33-37 the header paragraph; read at the tip by script, the golden is generated from the tree at the tip, not typed.\n- Another test in the same dir reads sibling source with `readFileSync(join(__dirname, ...))` (ks1570b integration file :154, ks1434 :22-23).",
 unmeasured="- The drafter did NOT run the new file; the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- Whether the checker accepts an existing TEST file as the 'product' of a code_patch2 brief: this is the first brief of that shape from this operator; if the control refuses it, that is a harness finding, not a model one.\n- The docstring at :82 has the same stale label and is deliberately left alone (not in n1).\n- Whether `__dirname` resolves under the security vitest config (other tests in the dir use it).",
 scope="**KS-1585 n1 only.** Link the PR as Refs KS-1585, never a close-word. Comment-only in a test file.",
)
