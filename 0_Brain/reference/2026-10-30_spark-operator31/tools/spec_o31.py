import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PR = 'Blockchain/Dev/services/auth/src/repositories/issuerCertRepo.ts'
TP = 'Blockchain/Dev/services/auth/src/__tests__/ks1544-class-auth-issuer-certs-list-orders-in-a-total-order.test.ts'
def rep(old, new):
    def f(src):
        assert src.count(old) == 1, (old, src.count(old))
        return src.replace(old, new)
    return f
TEST = r'''/**
 * KS-1544 class (auth): the paged read in repositories/issuerCertRepo.ts (listIssuerCerts, behind GET /issuer-certs) sorts on
 * `uploaded_at`, which is not unique, then pages with `LIMIT ... OFFSET ...`. Rows that tie on the sort key have no defined order
 * between two queries, so a page walk can repeat or skip them (KS-1544 measured the same defect on platform_audit_log).
 * issuer_certs has `id UUID PRIMARY KEY` (migrations/024_issuer_certs.sql), so the ORDER BY now ends in `, id DESC`.
 * Source-text guard: the module needs a database to import.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SRC = readFileSync(resolve(__dirname, '..', 'repositories', 'issuerCertRepo.ts'), 'utf8');

/** Every paged ORDER BY clause (the text from ORDER BY through the OFFSET placeholder), whitespace collapsed. */
function pagedOrders(src: string): string[] {
  const found = src.match(/ORDER BY [^`;]*?OFFSET \$\$\{[^}]*\}/g) ?? [];
  return found.map((s) => s.replace(/\s+/g, ' '));
}

/** True when the clause does not end its sort list in the primary key before LIMIT. */
function tied(clause: string): boolean {
  return !/, id DESC LIMIT/.test(clause);
}

describe('issuer certs paged list orders in a total order (KS-1544 class)', () => {
  it('RED ks1544a T1 the paged list read orders by uploaded_at DESC, id DESC', () => {
    expect(pagedOrders(SRC)).toEqual(['ORDER BY uploaded_at DESC, id DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}']);
  });

  it('RED ks1544a T2 no paged read in issuerCertRepo.ts is left tied', () => {
    expect(pagedOrders(SRC).filter(tied)).toEqual([]);
  });

  it('control ks1544a C1 the scanner flags a tied clause and passes a total one', () => {
    expect(tied('ORDER BY uploaded_at DESC LIMIT $1 OFFSET $2')).toBe(true);
    expect(tied('ORDER BY uploaded_at DESC, id DESC LIMIT $1 OFFSET $2')).toBe(false);
  });

  it('control ks1544a C2 issuerCertRepo.ts has exactly one paged read', () => {
    expect(pagedOrders(SRC)).toHaveLength(1);
  });

  it('control ks1544a C3 the single-row active-cert read keeps its own order', () => {
    expect(SRC).toMatch(/ORDER BY uploaded_at DESC\s+LIMIT 1`/);
  });

  it('control ks1544a C4 the count query is not touched', () => {
    expect(SRC).toContain('SELECT COUNT(*)::text AS count FROM issuer_certs WHERE ${whereClause}');
  });
});
'''
S = dict(dir='ks_1544a_auth_issuer_certs_paged_list_total_order', ticket='KS-1544',
 title="auth: the paged issuer-certs read in repositories/issuerCertRepo.ts ends its ORDER BY in a non-unique column; end it in the primary key (KS-1544 class sibling site) (RUNG 4-5, code_patch2 LOOSE, one product, 1 hunk, one NEW vitest file given whole)",
 intro="DRAFT by Spark operator 31 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / auth service, issuer certificate metadata list) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1544 (platform_audit_log paged without a tie-break; Recommendation: end the ORDER BY in the primary key). THIS SITE IS NOT NAMED IN KS-1544 (it names tenant-provisioning only); it is the same class, listed by operator 29's census on develop 85cd24d81cb9 (`issuerCertRepo.ts`, 'ordering not shown on the OFFSET line') and read by operator 31 at develop a8c554659cb3. Wednesday decides whether to file it under KS-1544 or a new ticket. The product edit is described by behaviour, not given as a diff; the hunk header, the unchanged context lines and a per-hunk skeleton are dictated. This brief changes a sort order only: no credential, token, key-handling or role logic.",
 products=[(PR,[rep("       ORDER BY uploaded_at DESC\n       LIMIT $${params.length + 1} OFFSET", "       ORDER BY uploaded_at DESC, id DESC\n       LIMIT $${params.length + 1} OFFSET")])],
 prodnote=['product, modified in place: ONE one-line replacement (the paged list read in listIssuerCerts)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 6 cells (2 red, 4 control); a source-text guard'],
 runner='vitest` (`npx vitest run src/__tests__/ks1544-class-auth-issuer-certs-list-orders-in-a-total-order.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch2', rung='4-5 (LOOSE: the product line is written by the model, the hunk header and a per-hunk skeleton dictated; one product, 1 hunk; new test given whole)',
 pins='''# code_patch2: 1 product in services/auth (repositories/issuerCertRepo.ts, 1 hunk) + 1 NEW source-text vitest file; ref = ks1009 (same service, shape only); line = the changed line in the product.
tier=code_patch2
ref=Blockchain/Dev/services/auth/src/__tests__/ks1009-wallet-status-reveals-only-existence.test.ts
line=293
ctx=65536
started_ok=KS-1544_is_Backlog/In_Progress_for_tenant-provisioning_only;_issuerCertRepo.ts_is_in_no_OPEN_PR_file_set_(checked_by_GitHub_API_with_a_planted_positive_control)_and_in_no_named_live-seat_file
''',
 wrong="In `services/auth`, the paged read in `listIssuerCerts` (`src/repositories/issuerCertRepo.ts`, the `SELECT * FROM issuer_certs WHERE ${whereClause}` query inside `Promise.all`, lines 290-295) sorts on `uploaded_at DESC`, which is not unique, and then pages with `LIMIT $N OFFSET $M`, so rows that tie on `uploaded_at` have no defined order between two queries and a page walk can repeat or skip them. THE FIX: make the primary key the last sort key, changing ONLY the ORDER BY line: `       ORDER BY uploaded_at DESC` becomes `       ORDER BY uploaded_at DESC, id DESC` (seven leading spaces, direction kept descending to match the existing sort). `issuer_certs` has `id UUID PRIMARY KEY` (migrations/024_issuer_certs.sql:45). The `LIMIT $${params.length + 1} OFFSET $${params.length + 2}` line below it stays byte for byte, and so does everything else in the template string.",
 where="The one line changed (as read at the tip): `src/repositories/issuerCertRepo.ts` `:293`.\n- **NOT TO TOUCH:** the other `ORDER BY uploaded_at DESC` at `:246` (the single-row `findActiveIssuerCertForTenant` read that ends `LIMIT 1`; it is NOT paged and must stay as it is), the `COUNT(*)` query, the `limit`/`offset` clamping, `routes/issuerCerts.ts`, and every other file.",
 donot="**Do NOT touch** any other line of `issuerCertRepo.ts`, the existing tests, or any other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It reads the module as text; it imports no application code.",
 red=['RED ks1544a T1','RED ks1544a T2'],
 cells="- RED `T1` (the paged clause is exactly `ORDER BY uploaded_at DESC, id DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`), `T2` (no paged clause is left tied): both fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (scanner positive and negative controls), `C2` (the file has exactly one paged clause), `C3` (the `LIMIT 1` active-cert read at :246 keeps its order), `C4` (the COUNT query is untouched).",
 premises="- The paged clause is the only `OFFSET` in issuerCertRepo.ts (grep -i at the tip: line 294); the generator asserts the replaced two-line string occurs exactly once; the `ORDER BY uploaded_at DESC` text itself occurs twice (:246 and :293), which is why the replaced string includes the following LIMIT line.\n- `issuer_certs.id` is `UUID PRIMARY KEY DEFAULT gen_random_uuid()` (migrations/024_issuer_certs.sql:45); the only unique constraint besides it is `(tenant_id, fingerprint_sha256)`; `uploaded_at` is `TIMESTAMPTZ NOT NULL DEFAULT NOW()` with no unique index.\n- `listIssuerCerts` has one production caller, `routes/issuerCerts.ts:357` (grep over services/).\n- No open PR touches `issuerCertRepo.ts` or `routes/issuerCerts.ts` (all 130 file rows of the 25 open PRs read through the GitHub API at 2026-10-30 16:1x AEDT; positive control: `providers/social/github.ts` shows as a hit on #1830).",
 unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Query plans / index use: not measured (the table's indexes are tenant/status lookups; a `uploaded_at DESC, id DESC` sort may not use them any differently).\n- Whether any client page-walks this list, and whether `uploaded_at` ties occur in practice (a bulk upload in one transaction would tie on NOW()), is not measured; the defect is reasoned from the SQL, as KS-1544's was.\n- Branches that are not open PRs (a live seat's pushed-but-unraised work) were NOT enumerated; the live-seat list given by the coordinator names no issuerCerts file, but whether a seat holds one uncommitted is unknown.\n- Whether the 'certifications' work of seat U 7th (KS-1844) is this table (issuer certs) or the originate certifications route is not known to the drafter.",
 scope="**The one auth issuerCertRepo.ts paged read named above only.** Not a close of KS-1544 (it names tenant-provisioning); link as 'Refs KS-1544' only if Wednesday files this site under it.",
)
