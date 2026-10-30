import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PT = 'Blockchain/Dev/services/originate/src/services/errorTrackingService.ts'
PA = 'Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
TP = 'Blockchain/Dev/services/originate/src/__tests__/ks1544-class-originate-paged-lists-order-in-a-total-order.test.ts'
CA = 'ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}'
CB = 'ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}'
RA = 'ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}'
RB = 'ORDER BY display_name ASC, last_name ASC, id ASC LIMIT ${limit} OFFSET ${offset}'
def rep_all(old, new, n):
    def f(src):
        assert src.count(old) == n, (old, src.count(old))
        return src.replace(old, new)
    return f
TEST = r'''/**
 * KS-1544 class (originate): five paged reads in services/errorTrackingService.ts and four in routes/adminConfig.ts end their
 * ORDER BY in a column that is not unique, then page with `LIMIT ${limit} OFFSET ${offset}`. Rows that tie on the sort key have no defined
 * order between two queries, so a page walk can repeat or skip them (KS-1544 measured the same defect on platform_audit_log; KS-1731 on
 * vc-issuer). The ORDER BY of each paged read now ends in the primary key: `, id DESC` after `created_at DESC`, and `, id ASC` after
 * `display_name ASC, last_name ASC` (rights holders). Source-text guard: the two modules need a database and a full app to import.
 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const TRACK = readFileSync(resolve(__dirname, '..', 'services', 'errorTrackingService.ts'), 'utf8');
const ADMIN = readFileSync(resolve(__dirname, '..', 'routes', 'adminConfig.ts'), 'utf8');

/** Every paged ORDER BY clause (the text from ORDER BY through the OFFSET placeholder), whitespace collapsed. */
function pagedOrders(src: string): string[] {
  const found = src.match(/ORDER BY [^`;]*?LIMIT \$\{limit\} OFFSET \$\{offset\}/g) ?? [];
  return found.map((s) => s.replace(/\s+/g, ' '));
}

/** True when the clause ends its sort list in the primary key before LIMIT. */
function tied(clause: string): boolean {
  return !/, id (ASC|DESC) LIMIT/.test(clause);
}

describe('originate paged lists order in a total order (KS-1544 class)', () => {
  it('RED ks1544c T1 every paged read in errorTrackingService.ts ends its ORDER BY in id', () => {
    const clauses = pagedOrders(TRACK);
    expect(clauses).toHaveLength(5);
    expect(clauses.filter(tied)).toEqual([]);
  });

  it('RED ks1544c A1 the two paged audit_logs reads in adminConfig.ts end their ORDER BY in id DESC', () => {
    const clauses = pagedOrders(ADMIN).filter((c) => c.includes('created_at DESC'));
    expect(clauses).toHaveLength(2);
    expect(clauses.filter((c) => !c.includes('ORDER BY created_at DESC, id DESC LIMIT'))).toEqual([]);
  });

  it('RED ks1544c A2 the two paged rights_holders reads in adminConfig.ts end their ORDER BY in id ASC', () => {
    const clauses = pagedOrders(ADMIN).filter((c) => c.includes('display_name'));
    expect(clauses).toHaveLength(2);
    expect(clauses.filter((c) => !c.includes('ORDER BY display_name ASC, last_name ASC, id ASC LIMIT'))).toEqual([]);
  });

  it('control ks1544c C1 the scanner flags a tied clause and passes a total one', () => {
    expect(tied('ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}')).toBe(true);
    expect(tied('ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}')).toBe(false);
    expect(tied('ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}')).toBe(true);
    expect(tied('ORDER BY display_name ASC, last_name ASC, id ASC LIMIT ${limit} OFFSET ${offset}')).toBe(false);
  });

  it('control ks1544c C2 adminConfig.ts has exactly four paged reads, and the unpaged reads keep their ORDER BY', () => {
    expect(pagedOrders(ADMIN)).toHaveLength(4);
    expect(ADMIN).toContain('SELECT * FROM policy_audit_log ORDER BY created_at DESC LIMIT 100');
    expect(ADMIN).toContain('FROM users ORDER BY created_at DESC LIMIT 200');
  });

  it('control ks1544c C3 the count queries of errorTrackingService.ts are not touched', () => {
    expect(TRACK).toContain('SELECT COUNT(*)::int as total FROM system_errors');
    expect(TRACK).toContain('WHERE service = ${opts.service} AND severity = ${opts.severity}');
  });
});
'''
S = dict(dir='ks_1544c_originate_paged_lists_total_order', ticket='KS-1544',
 title="originate: nine paged reads (errorTrackingService.ts x5, adminConfig.ts x4) end their ORDER BY in a non-unique column; end it in the primary key (KS-1544 class sibling sites) (RUNG 5, code_patch2 LOOSE, MULTI-FILE and MIXED SHAPES: two products, two ORDER BY shapes; hunk headers and a per-hunk skeleton dictated; one NEW jest file given whole)",
 intro="DRAFT by Spark operator 28 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1544 (platform_audit_log paged without a tie-break; Recommendation: end the ORDER BY in the primary key). THESE NINE SITES ARE NOT NAMED IN KS-1544 (it names tenant-provisioning only); they are the same class, found by operator 28's census of `ORDER BY ... LIMIT ... OFFSET` in services/*/src on develop 85cd24d81cb9. Wednesday decides whether to file them under KS-1544 or a new ticket. RUNG 5: MULTI-FILE (two products in one service) and MIXED SHAPES (a created_at DESC tie-break `, id DESC` x7, and a `display_name ASC, last_name ASC` tie-break `, id ASC` x2); the product edits are described by behaviour, not given as a diff; the hunk headers, the unchanged context lines and a per-hunk skeleton are dictated.",
 products=[(PT,[rep_all(CA, CB, 5)]),(PA,[rep_all(CA, CB, 2), rep_all(RA, RB, 2)])],
 prodnote=['product 1, modified in place: FIVE one-line replacements (the system_errors reads)','product 2, modified in place: FOUR one-line replacements (two audit_logs reads, two rights_holders reads)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, jest, given in full below; 6 cells (3 red, 3 control); a source-text guard'],
 runner='jest` (`npx jest src/__tests__/ks1544-class-originate-paged-lists-order-in-a-total-order.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch2', rung='5 (LOOSE: product lines written by the model, hunk headers and a per-hunk skeleton dictated; TWO products, two ORDER BY shapes; new test given whole)',
 pins='''# code_patch2: 2 products in services/originate (errorTrackingService.ts hunks + adminConfig.ts hunks) + 1 NEW source-text jest file; ref = ks1695 (same service, shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/originate/src/__tests__/ks1695-certification-reads-need-issuer-holder-or-admin.test.ts
line=91
ctx=65536
started_ok=KS-1544_is_Backlog/In_Progress_for_tenant-provisioning_only;_these_originate_files_are_in_no_held_pass_(grep_2026-10-30);_no_live_seat_owns_errorTrackingService.ts_or_the_adminConfig_list_routes;_the_operator_did_not_check_open_PRs_beyond_ls-remote
''',
 wrong="In `services/originate`, nine paged reads sort on a column that is not unique and then page with `LIMIT ${limit} OFFSET ${offset}`, so rows that tie on the sort key have no defined order between two queries and a page walk can repeat or skip them. In `src/services/errorTrackingService.ts` (`getRecentErrors`) the five `system_errors` reads each end `ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset}`. In `src/routes/adminConfig.ts` two `audit_logs` reads (`GET /audit-logs`) end the same way, and two `rights_holders` reads (`GET /rights-holders`) end `ORDER BY display_name ASC, last_name ASC LIMIT ${limit} OFFSET ${offset}`. THE FIX is the same idea in two shapes, at each of the nine: make the primary key the last sort key, changing ONLY the ORDER BY words. Seven `created_at DESC` clauses become `ORDER BY created_at DESC, id DESC LIMIT ${limit} OFFSET ${offset}`; the two `display_name` clauses become `ORDER BY display_name ASC, last_name ASC, id ASC LIMIT ${limit} OFFSET ${offset}`. Every table has `id UUID PRIMARY KEY`. The rest of each line (the `SELECT` where it shares the line, the `LIMIT`/`OFFSET` placeholders) stays byte for byte.",
 where="The nine lines changed (file order, as read at the tip; the line numbers are the lines of the SQL clause): `errorTrackingService.ts` `:91`, `:100`, `:108`, `:116`, `:123`; `adminConfig.ts` `:1235`, `:1241` (audit_logs, `created_at DESC`) and `:1405`, `:1410` (rights_holders, `display_name ASC, last_name ASC`).\n- **NOT TO TOUCH:** every other `ORDER BY` in both files (in adminConfig.ts: the unpaged reads at :405, :688, :725, :806, :944, :1581, :1671, :1673 keep exactly their text), the `COUNT(*)` queries, the `limit`/`offset` clamping, the WHERE clauses, and every other file.",
 donot="**Do NOT touch** any other line of the two product files, the existing tests, or any other file. In particular the unpaged `ORDER BY created_at DESC` reads stay as they are (they have no `OFFSET`).",
 testnote2="The test section is a NEW jest file given whole. The `+` lines are byte-exact. It reads the two modules as text; it imports no application code.",
 red=['RED ks1544c T1','RED ks1544c A1','RED ks1544c A2'],
 cells="- RED `T1` (every paged clause in errorTrackingService.ts ends in an id column: none does at the tip), `A1` (the two adminConfig created_at clauses end `, id DESC`), `A2` (the two rights_holders clauses end `, id ASC`): all fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (scanner positive and negative controls), `C2` (adminConfig has exactly four paged clauses; two unpaged reads keep their text), `C3` (the count queries are untouched).",
 premises="- The five `errorTrackingService.ts` clauses, the two `adminConfig.ts` audit_logs clauses and the two rights_holders clauses are exactly the ones `grep -c` counts (5, 2, 2) at the tip; the generator asserts each count before it writes the golden.\n- Every table involved has an `id UUID PRIMARY KEY`: `system_errors` (migrations/040_system-errors.sql:26), `audit_logs` (migrations/001_initial-schema.sql:348), `rights_holders` (docker/init/07-rights-holders.sql:10).\n- No held READY pass or queued brief touches these lines (grep of night/READY_*.md and night/briefs/*/golden.diff: KS-1780 p1 edits routes/systemErrors.ts, a different file).",
 unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Query plans: an index on `(created_at DESC)` alone may not serve `ORDER BY created_at DESC, id DESC` (KS-1544 says so for platform_audit_log); not measured here, and the tables are small admin tables.\n- Whether the system_errors and audit_logs reads here are in fact walked page by page by any client is not measured; the defect is reasoned from the SQL, as KS-1544's was.\n- Open PRs touching adminConfig.ts were not enumerated (the file has several held passes elsewhere in the lane).",
 scope="**The nine originate paged reads named above only.** Not a close of KS-1544 (it names tenant-provisioning); link as 'Refs KS-1544' only if Wednesday files these sites under it.",
)
