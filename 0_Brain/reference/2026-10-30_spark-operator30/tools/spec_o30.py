import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PR = 'Blockchain/Dev/services/staking/src/routes/rewards.ts'
TP = 'Blockchain/Dev/services/staking/src/__tests__/ks1544-class-staking-rewards-paged-lists-order-in-a-total-order.test.ts'
def rep(old, new):
    def f(src):
        assert src.count(old) == 1, (old, src.count(old))
        return src.replace(old, new)
    return f
TEST = r'''/**
 * KS-1544 class (staking): the two paged reads in routes/rewards.ts (GET /history/:address over svc_reward_claims and GET /distributions over
 * svc_revenue_distributions) end their ORDER BY in a column that is not unique (`claimed_at`, `distributed_at`), then page with
 * `LIMIT $n OFFSET $m`. Rows that tie on the sort key have no defined order between two queries, so a page walk can repeat or skip them
 * (KS-1544 measured the same defect on platform_audit_log). Both tables have `id TEXT PRIMARY KEY` (migrations/002_verification-tiers.sql),
 * so the ORDER BY of each paged read now ends in `, id`. Source-text guard: the module needs a database to import.
 */
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SRC = readFileSync(resolve(__dirname, '..', 'routes', 'rewards.ts'), 'utf8');

/** Every paged ORDER BY clause (the text from ORDER BY through the OFFSET placeholder), whitespace collapsed. */
function pagedOrders(src: string): string[] {
  const found = src.match(/ORDER BY [^'`;]*?LIMIT \$\d+ OFFSET \$\d+/g) ?? [];
  return found.map((s) => s.replace(/\s+/g, ' '));
}

/** True when the clause does not end its sort list in the primary key before LIMIT. */
function tied(clause: string): boolean {
  return !/, id LIMIT/.test(clause);
}

describe('staking rewards paged lists order in a total order (KS-1544 class)', () => {
  it('RED ks1544s T1 the paged claims read orders by claimed_at, id', () => {
    const clauses = pagedOrders(SRC).filter((c) => c.includes('claimed_at'));
    expect(clauses).toEqual(['ORDER BY claimed_at, id LIMIT $2 OFFSET $3']);
  });

  it('RED ks1544s T2 the paged distributions read orders by distributed_at, id', () => {
    const clauses = pagedOrders(SRC).filter((c) => c.includes('distributed_at'));
    expect(clauses).toEqual(['ORDER BY distributed_at, id LIMIT $1 OFFSET $2']);
  });

  it('RED ks1544s T3 no paged read in rewards.ts is left tied', () => {
    expect(pagedOrders(SRC).filter(tied)).toEqual([]);
  });

  it('control ks1544s C1 the scanner flags a tied clause and passes a total one', () => {
    expect(tied('ORDER BY claimed_at LIMIT $2 OFFSET $3')).toBe(true);
    expect(tied('ORDER BY claimed_at, id LIMIT $2 OFFSET $3')).toBe(false);
    expect(tied('ORDER BY distributed_at LIMIT $1 OFFSET $2')).toBe(true);
    expect(tied('ORDER BY distributed_at, id LIMIT $1 OFFSET $2')).toBe(false);
  });

  it('control ks1544s C2 rewards.ts has exactly two paged reads', () => {
    expect(pagedOrders(SRC)).toHaveLength(2);
  });

  it('control ks1544s C3 the count and summary queries are not touched', () => {
    expect(SRC).toContain('SELECT COUNT(*) AS cnt FROM svc_reward_claims WHERE address = $1');
    expect(SRC).toContain("'SELECT COUNT(*) AS cnt FROM svc_revenue_distributions'");
    expect(SRC).toContain('SELECT COALESCE(SUM(staker_amount),0) AS total_distributed FROM svc_revenue_distributions');
  });
});
'''
S = dict(dir='ks_1544s_staking_rewards_paged_lists_total_order', ticket='KS-1544',
 title="staking: two paged reads in routes/rewards.ts (claims history, distributions) end their ORDER BY in a non-unique column; end it in the primary key (KS-1544 class sibling sites) (RUNG 5, code_patch2 LOOSE, one product, 2 hunks, one NEW vitest file given whole)",
 intro="DRAFT by Spark operator 30 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / staking) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1544 (platform_audit_log paged without a tie-break; Recommendation: end the ORDER BY in the primary key). THESE TWO SITES ARE NOT NAMED IN KS-1544 (it names tenant-provisioning only); they are the same class, found by operator 29's census on develop 85cd24d81cb9 and re-read by operator 30 at that tip. Wednesday decides whether to file them under KS-1544 or a new ticket. The third staking site (routes/stake.ts, `ORDER BY stake_date`) is DELIBERATELY NOT in this brief: another seat is editing stake.ts. The product edits are described by behaviour, not given as a diff; the hunk headers, the unchanged context lines and a per-hunk skeleton are dictated.",
 products=[(PR,[rep("ORDER BY claimed_at LIMIT $2 OFFSET $3", "ORDER BY claimed_at, id LIMIT $2 OFFSET $3"), rep("ORDER BY distributed_at LIMIT $1 OFFSET $2", "ORDER BY distributed_at, id LIMIT $1 OFFSET $2")])],
 prodnote=['product, modified in place: TWO one-line replacements (the claims read, the distributions read)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 6 cells (3 red, 3 control); a source-text guard'],
 runner='vitest` (`npx vitest run src/__tests__/ks1544-class-staking-rewards-paged-lists-order-in-a-total-order.test.ts` from `Blockchain/Dev/services/staking',
 tier='code_patch2', rung='5 (LOOSE: product lines written by the model, hunk headers and a per-hunk skeleton dictated; one product, 2 hunks; new test given whole)',
 pins='''# code_patch2: 1 product in services/staking (routes/rewards.ts, 2 hunks) + 1 NEW source-text vitest file; ref = ks591 (same service, shape only); line = the first changed line in the product.
tier=code_patch2
ref=Blockchain/Dev/services/staking/src/__tests__/ks591-stake-complete-unstake-body-required.test.ts
line=315
ctx=65536
started_ok=KS-1544_is_Backlog/In_Progress_for_tenant-provisioning_only;_stake.ts_is_deliberately_excluded_(Seat_E_22nd_edits_it);_rewards.ts_is_not_in_the_exclusion_list_the_coordinator_gave;_the_operator_did_not_check_open_PRs_beyond_ls-remote
''',
 wrong="In `services/staking`, two paged reads in `src/routes/rewards.ts` sort on a column that is not unique and then page with `LIMIT ... OFFSET ...`, so rows that tie on the sort key have no defined order between two queries and a page walk can repeat or skip them. `GET /history/:address` (`:315`) reads `SELECT * FROM svc_reward_claims WHERE address = $1 ORDER BY claimed_at LIMIT $2 OFFSET $3`; `GET /distributions` (`:362`) reads `SELECT * FROM svc_revenue_distributions ORDER BY distributed_at LIMIT $1 OFFSET $2`. THE FIX: make the primary key the last sort key, changing ONLY the ORDER BY words: `ORDER BY claimed_at, id LIMIT $2 OFFSET $3` and `ORDER BY distributed_at, id LIMIT $1 OFFSET $2`. Both tables have `id TEXT PRIMARY KEY` (migrations/002_verification-tiers.sql:693 and :703); the sort direction stays ascending, as it is. The rest of each line (the `SELECT`, the `WHERE`, the placeholders and the quotes) stays byte for byte.",
 where="The two lines changed (as read at the tip): `src/routes/rewards.ts` `:315` and `:362`.\n- **NOT TO TOUCH:** the `COUNT(*)` queries, the `SUM` summary queries, the `limit`/`offset` parsing, and every other file. In particular `src/routes/stake.ts` is not part of this change.",
 donot="**Do NOT touch** any other line of `rewards.ts`, the existing tests, or any other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It reads the module as text; it imports no application code.",
 red=['RED ks1544s T1','RED ks1544s T2','RED ks1544s T3'],
 cells="- RED `T1` (the claims clause is exactly `ORDER BY claimed_at, id LIMIT $2 OFFSET $3`), `T2` (the distributions clause is exactly `ORDER BY distributed_at, id LIMIT $1 OFFSET $2`), `T3` (no paged clause is left tied): all fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (scanner positive and negative controls), `C2` (rewards.ts has exactly two paged clauses), `C3` (the count and sum queries are untouched).",
 premises="- The two clauses are the only `OFFSET` in rewards.ts (grep -i at the tip: lines 315 and 362); the generator asserts each replaced string occurs exactly once.\n- `svc_reward_claims` and `svc_revenue_distributions` each have `id TEXT PRIMARY KEY` (migrations/002_verification-tiers.sql:693, :703; docker/init/04-sprint2-service-tables.sql:582, :593); neither has a unique index on the sort column (only `address` and `quarter` indexes).\n- No edit of rewards.ts is staged by this brief's author in any other brief (stake.ts excluded on purpose).",
 unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Query plans: not measured; the tables are small and indexed on address / quarter only.\n- Whether any client page-walks these lists, and whether `claimed_at` / `distributed_at` ties occur in practice, is not measured; the defect is reasoned from the SQL, as KS-1544's was.\n- Open PRs touching rewards.ts were not enumerated (ls-remote only); the coordinator named only stake.ts as live.",
 scope="**The two staking rewards.ts paged reads named above only.** Not a close of KS-1544 (it names tenant-provisioning); link as 'Refs KS-1544' only if Wednesday files these sites under it.",
)
