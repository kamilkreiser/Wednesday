P='Blockchain/Dev/services/anchoring/src/anchorOverwriteGuard.ts'
T1='Blockchain/Dev/services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts'
TP='Blockchain/Dev/services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts'
E1=("    // The LEFT JOIN carries its OWN `u.tenant_id = $2::uuid`, and that is not\n"
    "    // belt-and-braces duplication of the one on `documents`. `users` has a\n"
    "    // SECOND, permissive policy — `users_auth_lookup`, whose qual is literally\n"
    "    // `true` — and Postgres ORs permissive policies together, so tenant\n"
    "    // isolation on `users` is open for SELECT by construction. Measured on the\n"
    "    // repo schema. A join without its own bound would read a custodian row\n"
    "    // from ANY tenant.\n",
    "    // The LEFT JOIN carries its OWN `u.tenant_id = $2::uuid` bound. `users` has\n"
    "    // a SECOND, permissive policy, `users_auth_lookup`, whose qual is literally\n"
    "    // `true`, but it is granted to the dedicated role `secuura_auth_lookup`,\n"
    "    // not to `public`, so it does not apply to `secuura_app`, the role\n"
    "    // anchoring connects as: there `tenant_isolation` is live. The bound stays\n"
    "    // so the join does not depend on which role the connection holds: a\n"
    "    // connection that held `secuura_auth_lookup` would read a custodian row\n"
    "    // from ANY tenant. (Measured on the repo schema, KS-1663.)\n")
T1E=("    // ⚠ ADDED because a mutant survived. Dropping `AND u.tenant_id = $2::uuid` from the custody\n"
     "    // LEFT JOIN killed no cell, and it is not cosmetic: `users` carries a SECOND, permissive\n"
     "    // policy — `users_auth_lookup`, whose qual is literally `true` — and Postgres ORs permissive\n"
     "    // policies, so tenant isolation on `users` is open for SELECT by construction. Without the\n"
     "    // explicit bound, option (c) would resolve a custodian organisation from ANY tenant the\n"
     "    // moment Kam rules it, and nothing would have objected.\n",
     "    // ⚠ ADDED because a mutant survived. Dropping `AND u.tenant_id = $2::uuid` from the custody\n"
     "    // LEFT JOIN killed no cell, and it is not cosmetic: `users` carries a SECOND, permissive\n"
     "    // policy, `users_auth_lookup` (qual literally `true`), but it is granted to the dedicated role\n"
     "    // `secuura_auth_lookup`, not to `public`, so it does not apply to `secuura_app`. The explicit\n"
     "    // bound keeps the join tenant-scoped whatever role the connection holds: without it, option (c)\n"
     "    // would resolve a custodian organisation from ANY tenant for a connection that held that role,\n"
     "    // and nothing would have objected.\n")
TEST='''// KS-1663 (anchoring, readOwningDocument): the comment above the custody LEFT JOIN, and the same inference in the ks1385 integration test's C-e cell, said `users` is "open for SELECT by construction"
// because the permissive policy `users_auth_lookup` has a qual of `true`. That omitted the policy's roles: it is granted to the dedicated role `secuura_auth_lookup`, not to `public`, so it does not apply to
// `secuura_app`, the role anchoring connects as. The tenant bound on the join is right and stays; only the stated reason was false.
// These cells read the two files as text. R1 and R2 are the product-comment cells (red until the comment is corrected); T1 and T2 pin the corrected test comment; C1 to C3 pin what must not move.
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const GUARD_SRC = readFileSync(resolve(__dirname, '..', 'anchorOverwriteGuard.ts'), 'utf8');
const C_E_SRC = readFileSync(resolve(__dirname, 'ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts'), 'utf8');

describe('KS-1663: the custody-join comments say what the policy does', () => {
  it('RED KS-1663 R1 the guard comment no longer says users is open for SELECT by construction', () => {
    expect(GUARD_SRC).not.toContain('open for SELECT by construction');
  });

  it('RED KS-1663 R2 the guard comment names the role the permissive policy is granted to', () => {
    expect(GUARD_SRC).toContain('granted to the dedicated role `secuura_auth_lookup`');
  });

  it('control KS-1663 T1 the C-e cell comment no longer says users is open for SELECT by construction', () => {
    expect(C_E_SRC).not.toContain('open for SELECT by construction');
  });

  it('control KS-1663 T2 the C-e cell comment names the role the permissive policy is granted to', () => {
    expect(C_E_SRC).toContain('granted to the dedicated role');
  });

  it('control KS-1663 C1 the custody join still carries its own tenant bound', () => {
    expect(GUARD_SRC).toContain('AND u.tenant_id = $2::uuid');
  });

  it('control KS-1663 C2 the LEFT-not-INNER comment is still there', () => {
    expect(GUARD_SRC).toContain('LEFT, not INNER');
  });

  it('control KS-1663 C3 both files were read (the instrument is not reading an empty string)', () => {
    expect(GUARD_SRC.length).toBeGreaterThan(1000);
    expect(C_E_SRC.length).toBeGreaterThan(1000);
  });
});
'''
S=dict(dir='ks_1663_p1',ticket='KS-1663',
 title='anchoring: a correct tenant bound on the custody join rests on a false reason (users is NOT open for SELECT: users_auth_lookup is role-restricted) - correct the two comments (RUNG 3, code_patch2: one comment hunk + one comment hunk in an existing integration test + one NEW source-text vitest file)',
 intro="DRAFT by Spark operator 7 for Wednesday, 2026-10-29 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. A COMMENT-ONLY fix: no behaviour changes, the bound stays. The ticket's open question (does anything else in anchoring lean on the belief) is NOT in this brief.",
 products=[(P,[E1])],
 prodnote=['product, modified in place: ONE hunk, a seven-line comment replaced by an eight-line comment (no code)'],
 tests=[dict(path=TP,content=TEST),dict(path=T1,new=False,edits=[T1E])],
 testnote=['NEW file, vitest, given in full below; 7 cells (2 red, 5 control; source-text reads of the two files)','EXISTING integration file, modified in place: ONE hunk, a six-line comment inside the C-e cell replaced by a seven-line comment (no assertion changes; the file is not run by the default vitest config)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts` from `Blockchain/Dev/services/anchoring',
 tier='code_patch2', rung='3 (three files: a comment hunk, a comment hunk in an existing integration test, a new test given whole)',
 pins='''# code_patch2: anchoring anchorOverwriteGuard.ts (1 comment hunk) + the ks1385 integration test (1 comment hunk, SUPPORT) + a NEW vitest source-text file; ref = a source-text anchoring test (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/anchoring/src/__tests__/ks1175-getid-view-wired.test.ts
line=255
ctx=65536
''',
 wrong="The comment inside `readOwningDocument` (`services/anchoring/src/anchorOverwriteGuard.ts:255-261`) justifies the custody LEFT JOIN's own `u.tenant_id = $2::uuid` bound by saying `users` is \"open for SELECT by construction\" because the permissive policy `users_auth_lookup` has a qual of `true`. That omits the policy's roles: measured on the repo's migrated schema (pg 15), `users_auth_lookup` is `cmd = SELECT`, qual `true`, `roles = {secuura_auth_lookup}`, a dedicated role and NOT `public`; as `secuura_app` (what anchoring connects as) a read of `users` under tenant A's GUC sees tenant B's row 0 times. So the policy does not apply to anchoring, `tenant_isolation` is live, and the stated reason is false. The bound itself is right and stays. The same inference is repeated in the comment inside the C-e cell of `__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts` (`:533-538`). Both comments are reworded to the measured fact; no code and no assertion changes.",
 where="- `src/anchorOverwriteGuard.ts:255-261` - **must change**: the seven comment lines beginning `    // The LEFT JOIN carries its OWN` and ending `    // from ANY tenant.` are replaced by the eight comment lines under \"The exact change\". The comment line `    //` and `    // LEFT, not INNER:` that follow, and every code line, are NOT touched.\n- `src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts:533-538` - **must change**: the six comment lines inside `it('C-e a custodian user in ANOTHER tenant ...` beginning `    // ⚠ ADDED because a mutant survived.` are replaced by the seven lines under \"The test\". The line after them (`const doc = await makeDocument(`) is NOT touched.",
 exactnote="ONE hunk in the product file (comments only).\n",
 donot="**Do NOT touch** any code line, any other comment, or any assertion in either existing file.",
 testnote2="The first test section is a NEW file given whole; the second modifies an EXISTING file (one comment block). In both, the `+` lines are byte-exact. The new file uses `vitest` imports, reads the two files with `readFileSync` relative to `__dirname`, and has no top-level await.",
 red=['RED KS-1663 R1','RED KS-1663 R2'],
 cells="- RED `R1`: at the tip the guard comment still contains `open for SELECT by construction`.\n- RED `R2`: at the tip the new sentence is absent.\n- CONTROL `T1` and `T2`: they read the existing integration test file, which the patch's other test section has already edited when only the test sections are applied, so they are green with the tests alone and green after the product edit; they pin the new test comment.\n- CONTROL `C1` to `C3`: green at the tip AND after.",
 premises="- Lines `:255-261` of the product file and `:533-538` of the existing integration test are as quoted (read at the tip; the removed lines carry U+2014 em dashes and a U+26A0 sign, the added lines are ASCII except the U+26A0 sign kept on the first test-comment line).\n- The policy facts (`roles = {secuura_auth_lookup}`, `secuura_app` sees 0 foreign rows) are the ticket author's measurement on 2026-10-19; the drafter did not re-run them.\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The policy measurement above is the ticket's, not re-run.\n- Open PRs touching these files: none by the git file lists of PRs 1782 and 1785-1799 read on 2026-10-29, and none in the Seat U KS-1494 worktree.",
 scope="**The two comments of KS-1663 only.** The ticket's open question (does anything else in anchoring lean on `users` being readable cross-tenant) stays open on the ticket. Link the PR as Refs KS-1663, never a close-word.",
)
