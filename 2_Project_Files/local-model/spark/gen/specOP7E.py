P='Blockchain/Dev/services/security/src/index.ts'
TP='Blockchain/Dev/services/security/src/__tests__/ks1601-the-admin-scope-target-query-folds-the-role-under-collate-c.test.ts'
Q='\\"C\\"'   # the two characters backslash-quote around C, as they appear inside the double-quoted SQL string literal in index.ts
C1=("    // `upper(role) = $3` beside it carries the SAME libc-fold class — U+0131 (dotless i) upper-cases\n"
    "    // to `I`, so `upper('admın') = 'ADMIN'` is true. That is PRE-EXISTING, it is not touched here,\n"
    "    // and it is on its own ticket: the pull request 1548 gate's i6.\n",
    "    // KS-1601 (the pull request 1548 gate's i6): the role comparison folds under `COLLATE \"C\"` too. Under the\n"
    "    // default collation a role spelled with U+0131 (dotless i) upper-cased to `ADMIN`, so that row passed this\n"
    "    // guard; under `COLLATE \"C\"` it does not, and every ASCII spelling of ADMIN still matches.\n")
C2=('      "SELECT 1 FROM users WHERE id = $1::uuid AND tenant_id = $2::uuid AND upper(role) = $3 AND lower(status COLLATE '+Q+') = \'active\' LIMIT 1",\n',
    '      "SELECT 1 FROM users WHERE id = $1::uuid AND tenant_id = $2::uuid AND upper(role COLLATE '+Q+') = $3 AND lower(status COLLATE '+Q+') = \'active\' LIMIT 1",\n')
TEST='''// KS-1601 (security, PUT /api/keys/admin-scopes/:userId): the target query folded the stored STATUS under COLLATE "C" (KS-1598) but the stored ROLE still under the database's default libc collation,
// so a role spelled with U+0131 (dotless i) upper-cased to ADMIN and passed the guard. The role comparison now folds under COLLATE "C" as well. The real-Postgres cells for the U+0131 spelling live in
// the integration file (ks1570b-admin-scope-route.integration.test.ts), which needs a database; these cells read src/index.ts as text so the one-line change is pinned in the default run.
// R1 to R3 are red until the change exists; C1 to C3 pin what must not move.
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const INDEX_SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');

describe('KS-1601: the admin-scope target query folds the role under COLLATE "C"', () => {
  it('RED KS-1601 R1 the target query no longer compares a default-collation upper(role)', () => {
    expect(INDEX_SRC).not.toContain('AND upper(role) = $3');
  });

  it('RED KS-1601 R2 the target query compares upper(role COLLATE ...) = $3', () => {
    expect(INDEX_SRC).toContain('AND upper(role COLLATE ');
  });

  it('RED KS-1601 R3 the comment no longer says the role fold is untouched', () => {
    expect(INDEX_SRC).not.toContain('PRE-EXISTING, it is not touched here');
  });

  it('control KS-1601 C1 the status fold still sits under COLLATE "C" in the same query', () => {
    expect(INDEX_SRC).toContain('AND lower(status COLLATE ');
  });

  it('control KS-1601 C2 the query still binds the literal ADMIN as the third parameter', () => {
    expect(INDEX_SRC).toContain("[userId, tenantId, 'ADMIN']");
  });

  it('control KS-1601 C3 the file was read (the instrument is not reading an empty string)', () => {
    expect(INDEX_SRC.length).toBeGreaterThan(10000);
  });
});
'''
S=dict(dir='ks_1601_p1',ticket='KS-1601',
 title='security PUT /api/keys/admin-scopes/:userId: the target query folds the stored role under the default libc collation (U+0131 dotless i upper-cases to ADMIN) while the status beside it folds under COLLATE "C" - apply COLLATE "C" to the role fold (RUNG 2, code_patch: one hunk with two edit points in one product + one NEW source-text vitest file; the DRAFTER took the ticket\'s minimal change)',
 intro="DRAFT by Spark operator 7 for Wednesday, 2026-10-29 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. DECISION FLAG: the ticket asks for a decision ('apply the fold to both columns, or write down why they differ') and names the minimal change if the fold is applied; this brief takes that minimal change. The ticket's real-Postgres cells (a U+0131 role must answer 404) belong in ks1570b-admin-scope-route.integration.test.ts and are NOT in this brief: they need a database. This is a SECURITY-adjacent SQL predicate (who may be granted an admin organisation scope): the PR needs a tier-1 gate.",
 products=[(P,[C1,C2])],
 prodnote=['product, modified in place: ONE hunk with TWO edit points (a three-line comment replaced by three lines; one SQL string line, `upper(role)` becomes `upper(role COLLATE "C")`)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 6 cells (3 red, 3 control; a source-text read of src/index.ts)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1601-the-admin-scope-target-query-folds-the-role-under-collate-c.test.ts` from `Blockchain/Dev/services/security',
 tier='code_patch', rung='2 (one hunk with two edit points, byte-exact; the new test given whole)',
 pins='''# code_patch, 1 hunk (2 edit points) in security src/index.ts (a comment + one SQL line) + a NEW source-text vitest file; ref = ks742 route-contract spec (shape only); line = the first changed line.
tier=code_patch
ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts
line=1651
ctx=65536
''',
 wrong="In `services/security/src/index.ts` the target query of `PUT /api/keys/admin-scopes/:userId` (`:1659-1662`) compares the stored role with `upper(role) = $3` under the database's DEFAULT libc collation, while the status comparison beside it was moved to `lower(status COLLATE \"C\") = 'active'` by KS-1598. Under a libc collation `upper()` of a role spelled with U+0131 (LATIN SMALL LETTER DOTLESS I) is `ADMIN`, so such a row passes the guard (measured by the gate on PostgreSQL 15.14 under en_AU.UTF-8 and en_US.UTF-8; `users.role` has no CHECK constraint). Under `COLLATE \"C\"` it does not, and every ASCII spelling of ADMIN still matches. The change: the role comparison becomes `upper(role COLLATE \"C\") = $3`, and the three-line comment at `:1651-1653` that says the role fold is untouched is replaced by a three-line comment that says it is applied (KS-1601).",
 where="- `src/index.ts:1651-1653` - **must change**: the three comment lines beginning `    // \\`upper(role) = $3\\` beside it carries the SAME libc-fold class` and ending `    // and it is on its own ticket: the pull request 1548 gate's i6.` are replaced by the three lines under \"The exact change\". The blank-comment line `    //` after them and the comment that follows are NOT touched.\n- `src/index.ts:1660` - **must change**: in the SQL string literal, `upper(role) = $3` becomes `upper(role COLLATE \\\"C\\\") = $3` (inside the double-quoted TypeScript string the quotes around C are written with a backslash, exactly like the `lower(status COLLATE \\\"C\\\")` that follows it on the same line). Nothing else on the line changes.",
 exactnote="ONE hunk in one file (the two edit points are 7 lines apart, so git merges them into a single hunk).\n",
 donot="**Do NOT touch** the status comparison, the parameter list `[userId, tenantId, 'ADMIN']`, any other SQL, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await.",
 red=['RED KS-1601 R1','RED KS-1601 R2','RED KS-1601 R3'],
 cells="- RED `R1` to `R3`: at the tip `AND upper(role) = $3` is present, `AND upper(role COLLATE ` is absent and the old comment is present; after the edit all three flip.\n- CONTROL `C1` to `C3`: green at the tip AND after (the status fold is untouched; the third parameter is still the literal ADMIN; the file was read).",
 premises="- `index.ts:1651-1653` is the three-line comment and `:1660` the SQL line quoted above (read at the tip; the removed comment lines carry a U+2014 em dash and a U+0131 character, the added lines are ASCII).\n- The SQL line already writes `lower(status COLLATE \\\"C\\\")` with backslash-escaped quotes, so the edit follows the same escaping.\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The U+0131 behaviour on a real database is the gate's measurement (PR 1548, filed on the ticket), not re-run here; no real-Postgres cell is added by this brief.\n- Whether any production row holds a role spelling that only matched through the default-collation fold (and so would now answer 404): unmeasured.\n- Open PRs touching this file: none by the git file lists of PRs 1782 and 1785-1799 read on 2026-10-29.",
 scope="**KS-1601 only, minimal change.** DECISION FLAG above. Link the PR as Refs KS-1601 until the owner has confirmed the fold and the real-Postgres cell exists.",
)
