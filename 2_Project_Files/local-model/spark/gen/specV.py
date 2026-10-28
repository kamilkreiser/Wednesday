D='Blockchain/Dev/services/governance/src/'
PS=D+'services/governanceService.ts'
PR=D+'routes/governance.ts'
TP=D+'__tests__/ks1732-a-failed-proposals-read-is-a-500-not-an-empty-list.test.ts'
S1=("    logger.error('DB get all proposals failed', { error: err instanceof Error ? err.message : String(err) });\n    return [];\n",
    "    logger.error('DB get all proposals failed', { error: err instanceof Error ? err.message : String(err) });\n    throw err;\n")
R1=("router.get('/proposals', async (req: Request, res: Response) => {\n",
    "router.get('/proposals', async (req: Request, res: Response, next: NextFunction) => {\n")
R2=("  const proposals = await governanceService.getProposals({\n    status: statusFilter,\n    category,\n    proposerId,\n  });\n",
    "  const proposals = await governanceService.getProposals({\n    status: statusFilter,\n    category,\n    proposerId,\n  }).catch(next);\n  if (!proposals) return;\n")
R3=("router.get('/proposals/active', async (_req: Request, res: Response) => {\n  const proposals = await governanceService.getProposals({ status: 'active' });\n",
    "router.get('/proposals/active', async (_req: Request, res: Response, next: NextFunction) => {\n  const proposals = await governanceService.getProposals({ status: 'active' }).catch(next);\n  if (!proposals) return;\n")
TEST='''/**
 * KS-1732 - a FAILED database read of the proposals table must not answer as an empty list.
 * Before: dbGetAllProposals caught every error and returned [], so GET /proposals and GET /proposals/active answered 200 with an empty list,
 * and the active-proposal cap in createProposal (which reads through the same helper) failed open. After: the read rejects, the two list routes hand
 * the error to next(), and the shared errorHandler answers 500. The harness is the one ks1722 and ks594 use: the REAL routes over a REAL socket through
 * the REAL shared error handler, only the database mocked. Cell ids are letters plus digits.
 */
import express from 'express';

const mockState = { failReads: false };

jest.mock('../db', () => ({
  isDbAvailable: () => true,
  query: jest.fn(async (sql: string) => {
    const flat = sql.replace(/\\s+/g, ' ').trim();
    if (/FROM svc_proposals/.test(flat)) {
      if (mockState.failReads) throw new Error('connection terminated (ks1732 test)');
      return {
        rows: [
          {
            id: 'p-active-1',
            proposal_number: 1,
            proposer_id: 'alice',
            status: 'active',
            category: 'general',
            title: 'KS-1732 proposal',
            description: 'd',
            voting_config: {},
            created_at: new Date('2026-10-28T00:00:00Z'),
          },
        ],
      };
    }
    return { rows: [] };
  }),
}));
const { errorHandler } = require('@secuura/shared');
const { governanceRoutes } = require('../routes/governance');
const governanceService = require('../services/governanceService');

const app = express();
app.use(express.json());
app.use((req, _res, next) => {
  (req as any).user = { userId: 'alice', tenantId: 'tenant-1' };
  next();
});
app.use('/api/governance', governanceRoutes);
app.use(errorHandler);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => {
      const addr = server.address();
      baseUrl = `http://127.0.0.1:${typeof addr === 'object' && addr ? addr.port : 0}`;
      resolve();
    });
  });
});

afterAll(async () => {
  if (server) await new Promise<void>((resolve) => server.close(() => resolve()));
});

beforeEach(() => {
  mockState.failReads = false;
});

async function get(path: string): Promise<{ status: number; body: any }> {
  const r = await fetch(`${baseUrl}/api/governance${path}`);
  return { status: r.status, body: await r.json().catch(() => null) };
}

describe('KS-1732: a failed proposals read is a 500, not an empty list', () => {
  it('RED KS-1732 R1 GET /proposals with a failing database answers 500, success false, no data', async () => {
    mockState.failReads = true;
    const r = await get('/proposals');
    expect([r.status, r.body?.success, r.body?.data]).toEqual([500, false, undefined]);
  });

  it('RED KS-1732 R2 GET /proposals/active with a failing database answers 500, success false, no data', async () => {
    mockState.failReads = true;
    const r = await get('/proposals/active');
    expect([r.status, r.body?.success, r.body?.data]).toEqual([500, false, undefined]);
  });

  it('RED KS-1732 R3 the service read itself rejects with the database error instead of resolving to an empty list', async () => {
    mockState.failReads = true;
    await expect(governanceService.getProposals()).rejects.toThrow('connection terminated (ks1732 test)');
  });

  it('control KS-1732 C1 a healthy GET /proposals still answers 200 with the one proposal', async () => {
    const r = await get('/proposals');
    expect([r.status, r.body?.success, r.body?.count, (r.body?.data ?? []).map((p: { id: string }) => p.id)]).toEqual([200, true, 1, ['p-active-1']]);
  });

  it('control KS-1732 C2 a healthy GET /proposals/active still answers 200 with the one proposal', async () => {
    const r = await get('/proposals/active');
    expect([r.status, r.body?.success, r.body?.count]).toEqual([200, true, 1]);
  });

  it('control KS-1732 C3 processExpiredProposals still resolves 0 (its own catch) when the read fails', async () => {
    mockState.failReads = true;
    await expect(governanceService.processExpiredProposals()).resolves.toBe(0);
  });
});
'''
S=dict(dir='ks_1732_p1',ticket='KS-1732',
 title='governance: a failed database read answers as empty - dbGetAllProposals swallows into [] so GET /proposals returns 200 [] and the active-proposal cap fails open; let the read reject and have the two list routes pass it to next() (RUNG 3, code_patch2: 4 hunks in 2 products + one NEW jest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 5 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. The ticket states the defect and names the fix shape of KS-1345 (let the read reject to the route, constant 500) but marks two choices as ruling-sensitive; this brief takes the narrow side of both and says so in Scope.",
 products=[(PS,[S1]),(PR,[R1,R2,R3])],
 prodnote=['product 1 (governanceService.ts), modified in place: ONE hunk, one line replaced','product 2 (routes/governance.ts), modified in place: THREE hunks (one handler signature, one call given a .catch, the active handler signature and call)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, jest, given in full below; 6 cells (3 red, 3 control; real routes over a socket, database mocked)'],
 runner='jest` (`npx jest src/__tests__/ks1732-a-failed-proposals-read-is-a-500-not-an-empty-list.test.ts` from `Blockchain/Dev/services/governance',
 tier='code_patch2', rung='3 (four hunks in two products given byte-exact; the new test given whole)',
 pins='''# code_patch2: governance governanceService.ts (1 hunk) + routes/governance.ts (3 hunks) + a NEW jest file; ref = ks1722 (same harness, shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/governance/src/__tests__/ks1722-proposals-list-refuses-an-unusable-filter.test.ts
line=256
ctx=65536
''',
 wrong="`dbGetAllProposals` in `services/governance/src/services/governanceService.ts` catches every database error, logs it and returns `[]` (`:254-256`). Its callers read that as 'no proposals': `getProposals` (so `GET /api/governance/proposals` and `GET /api/governance/proposals/active` answer `200` with `data: []`, `count: 0`), and `createProposal`'s active-proposal cap (`:495-497`), which therefore fails OPEN when the read fails. The change: the catch still logs, then rethrows (`throw err;`). The two list handlers in `routes/governance.ts` are plain `async` functions with no error path, and Express 4 does not route a rejected async handler to the error middleware, so each is given `next` and adds `.catch(next)` to its `getProposals` call and returns early when the result is falsy (a rejected read resolves to `undefined` after `next(error)` ran) (the POST handlers in the same file reach `next(error)` through try/catch; this form avoids re-indenting the call). The shared `errorHandler` then answers 500. `processExpiredProposals` (`:1013`) already has its own catch returning 0 and is unchanged in behaviour.",
 where="- `src/services/governanceService.ts:256` - **must change**: inside `dbGetAllProposals`'s catch block, directly after the `logger.error('DB get all proposals failed', ...)` line, the statement `return [];` becomes `throw err;`.\n- `src/routes/governance.ts:141` - **must change**: the handler signature `router.get('/proposals', async (req: Request, res: Response) => {` gains a third parameter `next: NextFunction` (`NextFunction` is already imported at :8).\n- `src/routes/governance.ts:159` - **must change**: `const proposals = await governanceService.getProposals({ status: statusFilter, category, proposerId });` (five lines) gains `.catch(next)` on the closing `});` line, followed by `if (!proposals) return;`.\n- `src/routes/governance.ts:176` and `:177` - **must change**: the `/proposals/active` handler gains `next: NextFunction` and its `getProposals` call gets the same `.catch` and early return.\n- Every other line of both files, including `getProposal`, `getGovernanceStats` and the other helpers' catches (`dbGetProposal`, `dbGetParticipant` and the rest, which the ticket lists but does not decide), is NOT touched.",
 exactnote="Four hunks in two files: one in `governanceService.ts`, then three in `routes/governance.ts`, in file order.\n",
 donot="**Do NOT touch** any other `catch` in `governanceService.ts`, any other route, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, jest globals, no top-level await. It mocks `../db`, mounts the real router behind the real `errorHandler`, and calls it over a socket with `fetch`, as the existing ks1722 test does.",
 red=['RED KS-1732 R1','RED KS-1732 R2','RED KS-1732 R3'],
 cells="- RED `R1`/`R2`: at the tip a failing read answers `200` with `data: []`; after the edit it answers `500` with `success: false` and no `data`.\n- RED `R3`: at the tip `getProposals()` resolves to `[]`; after the edit it rejects with the database error.\n- CONTROL `C1` to `C3`: green at the tip AND after (healthy list and active list unchanged; `processExpiredProposals` still resolves 0 on a failing read).",
 premises="- `governanceService.ts:254-256` is the catch quoted above and `routes/governance.ts:141,159,176-177` are the lines quoted (read at the tip).\n- The Express version is 4.x (`^4.18.2`): a rejected async handler is not routed to the error middleware, hence the `.catch` that calls `next`.\n- The shared `errorHandler` maps an error without a `statusCode` to 500 (KS-594 header).\n- The service's test runner is jest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The ticket's second ruling-sensitive choice (whether the cap should refuse rather than allow when it cannot count) is taken here as 'refuse by erroring': a failed read now makes `createProposal` reject. That path has no cell in this brief.\n- Whether a 500 is the right answer vs a 503 for a database outage: the ticket names KS-1345's constant 500; not measured here.\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Narrow slice of KS-1732: `dbGetAllProposals` and the two list routes only.** The other value-returning catches in the file (`dbGetProposal`, `dbGetParticipant`, `dbGetParticipantByAddress`, `dbGetAllParticipants`, `dbGetActiveDelegations`, `getTotalVotePower`) are NOT changed and stay open: the ticket asks whether not-found must stay distinguishable from a failed read. Link the PR as Refs KS-1732, never a close-word.",
)
