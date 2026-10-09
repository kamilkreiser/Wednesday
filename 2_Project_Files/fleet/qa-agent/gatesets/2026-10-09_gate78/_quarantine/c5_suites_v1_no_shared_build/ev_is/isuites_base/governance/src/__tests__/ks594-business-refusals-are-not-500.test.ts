/**
 * =============================================================================
 * KS-594 — governance business refusals must not be reported as server errors
 * =============================================================================
 * The register names ONE operation (the active-proposal cap on
 * `POST /api/governance/proposals`). The class sweep found the same shape at
 * 21 sites in `governanceService.ts`: every refusal is a bare `Error`, the
 * routes hand it to `next()`, and the shared `errorHandler` maps anything
 * without a `statusCode` to `500 INTERNAL_ERROR`.
 *
 * So a caller who did nothing wrong is told the server crashed — and, measured
 * on KS-593, 62 of 79 `not_a_server_error` sweep failures were this one defect.
 *
 * These tests drive the REAL Express routes over a REAL socket through the
 * REAL shared error handler, with only the DB mocked, so they assert the status
 * a client actually receives rather than the shape of a thrown object.
 * (Same harness as KS-488 C-4: `app.listen(0)` + `fetch`, no new dependency.)
 *
 * Every rejection case is paired with a case that must SUCCEED, so a change
 * that simply refused everything cannot pass this suite.
 * =============================================================================
 */

import express from 'express';

// ---------------------------------------------------------------------------
// DB mock — pattern-matches the small, fixed set of statements the service
// issues on these paths. Each test sets `dbState` to stage its scenario.
// ---------------------------------------------------------------------------

type DbState = {
  participant: Record<string, unknown> | null;
  activeProposals: number;
  proposals: Record<string, unknown>[];
};

const dbState: DbState = { participant: null, activeProposals: 0, proposals: [] };

jest.mock('../db', () => ({
  isDbAvailable: () => true,
  query: jest.fn(async (sql: string) => {
    const s = String(sql).replace(/\s+/g, ' ').trim();

    if (/FROM svc_governance_participants/i.test(s) && /^SELECT/i.test(s)) {
      return { rows: dbState.participant ? [dbState.participant] : [] };
    }
    if (/FROM svc_proposals/i.test(s) && /status = ANY/i.test(s)) {
      return {
        rows: Array.from({ length: dbState.activeProposals }, (_, i) => ({
          id: `p-active-${i}`,
          proposal_number: i + 1,
          status: 'active',
          category: 'treasury_spend',
          proposer_id: 'someone-else',
          title: `Active proposal ${i}`,
          description: 'An already-active proposal counting towards the cap.',
        })),
      };
    }
    if (/FROM svc_proposals/i.test(s) && /^SELECT/i.test(s)) {
      return { rows: dbState.proposals };
    }
    if (/FROM svc_vote_delegations/i.test(s) && /^SELECT/i.test(s)) {
      return { rows: [] };
    }
    // INSERT / UPDATE / DELETE / everything else — accept, return nothing.
    return { rows: [], rowCount: 0 };
  }),
}));

/* eslint-disable @typescript-eslint/no-var-requires */
const { errorHandler } = require('@secuura/shared');
const { governanceRoutes } = require('../routes/governance');
/* eslint-enable @typescript-eslint/no-var-requires */

const USER_ID = 'user-under-test';

const app = express();
app.use(express.json());
// Stand in for `jwtAuthenticate()`: the routes read `req.user.userId`, which
// authenticate() populates from the verified bearer token. Authentication
// itself is not what this suite is about.
app.use((req, _res, next) => {
  (req as any).user = { userId: USER_ID, tenantId: 'tenant-1' };
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
      const port = typeof addr === 'object' && addr ? addr.port : 0;
      baseUrl = `http://127.0.0.1:${port}`;
      resolve();
    });
  });
});

afterAll(async () => {
  await new Promise<void>((resolve) => server.close(() => resolve()));
});

async function post(path: string, body: unknown) {
  const res = await fetch(`${baseUrl}${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  let json: any = {};
  try {
    json = JSON.parse(text);
  } catch {
    json = { raw: text };
  }
  return { status: res.status, body: json };
}

function stakedParticipant(stakedAmount: number) {
  return {
    id: USER_ID,
    wallet_address: 'addr_test1_participant',
    staked_amount: stakedAmount,
    tier: 'gold',
    vote_power: stakedAmount,
    is_drep: true,
    is_constitutional_committee: false,
    proposals_created: 0,
    votes_cast: 0,
    joined_at: new Date().toISOString(),
    last_active_at: new Date().toISOString(),
  };
}

const validProposalBody = {
  title: 'Raise the treasury allocation for Q4',
  description:
    'A proposal to raise the treasury allocation so the grants programme can continue through the quarter.',
  category: 'treasury_spend',
};

beforeEach(() => {
  dbState.participant = stakedParticipant(100_000);
  dbState.activeProposals = 0;
  dbState.proposals = [];
});

// ---------------------------------------------------------------------------
// The named defect
// ---------------------------------------------------------------------------

describe('KS-594 — POST /api/governance/proposals, active-proposal cap', () => {
  it('answers 409 CONFLICT when the cap is reached, not 500', async () => {
    dbState.activeProposals = 20; // DEFAULT_GOVERNANCE_CONFIG.maxActiveProposals

    const res = await post('/api/governance/proposals', validProposalBody);

    expect(res.status).toBe(409);
    expect(res.body.success).toBe(false);
    expect(res.body.error.code).not.toBe('INTERNAL_ERROR');
    expect(String(res.body.error.message)).toMatch(/active proposals/i);
  });

  // POSITIVE CONTROL — must succeed. Without it, a change that refused every
  // create would satisfy the assertion above.
  it('still creates a proposal when the cap has NOT been reached', async () => {
    dbState.activeProposals = 3;

    const res = await post('/api/governance/proposals', validProposalBody);

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
  });

  it('answers 400 when the proposer is under the minimum stake, not 500', async () => {
    dbState.participant = stakedParticipant(1); // minProposalStake is 1000

    const res = await post('/api/governance/proposals', validProposalBody);

    expect(res.status).toBe(400);
    expect(res.body.error.code).not.toBe('INTERNAL_ERROR');
    expect(String(res.body.error.message)).toMatch(/minimum stake/i);
  });

  // POSITIVE CONTROL for the stake branch.
  it('still creates a proposal for a proposer at exactly the minimum stake', async () => {
    dbState.participant = stakedParticipant(1000);

    const res = await post('/api/governance/proposals', validProposalBody);

    expect(res.status).toBe(201);
  });

  // The route's own Zod branch is not part of this fix and must keep working.
  it('still answers 400 BAD_REQUEST on a schema-violating body', async () => {
    const res = await post('/api/governance/proposals', {
      title: 'short',
      category: 'treasury_spend',
    });

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('BAD_REQUEST');
  });
});

// ---------------------------------------------------------------------------
// The rest of the class — same shape, other operations
// ---------------------------------------------------------------------------

describe('KS-594 class — other governance refusals carry their own status', () => {
  it('submit on a missing proposal answers 404, not 500', async () => {
    dbState.proposals = [];

    const res = await post('/api/governance/proposals/does-not-exist/submit', {});

    expect(res.status).toBe(404);
    expect(res.body.error.code).not.toBe('INTERNAL_ERROR');
  });

  it('submit by someone other than the proposer answers 403, not 500', async () => {
    dbState.proposals = [
      {
        id: 'p-1',
        proposal_number: 1,
        proposer_id: 'a-different-user',
        status: 'draft',
        category: 'treasury_spend',
        title: 'Someone else proposal',
        description: 'Owned by another participant entirely.',
        created_at: new Date().toISOString(),
      },
    ];

    const res = await post('/api/governance/proposals/p-1/submit', {});

    expect(res.status).toBe(403);
    expect(res.body.error.code).not.toBe('INTERNAL_ERROR');
  });

  it('submit on a non-draft proposal answers 409, not 500', async () => {
    dbState.proposals = [
      {
        id: 'p-2',
        proposal_number: 2,
        proposer_id: USER_ID,
        status: 'active',
        category: 'treasury_spend',
        title: 'Already submitted proposal',
        description: 'This one has already left the draft state.',
        created_at: new Date().toISOString(),
      },
    ];

    const res = await post('/api/governance/proposals/p-2/submit', {});

    expect(res.status).toBe(409);
    expect(res.body.error.code).not.toBe('INTERNAL_ERROR');
  });

  // POSITIVE CONTROL — a legitimate submit must still go through, so the three
  // refusals above cannot be satisfied by refusing everything.
  it('still submits the proposer own draft proposal', async () => {
    dbState.proposals = [
      {
        id: 'p-3',
        proposal_number: 3,
        proposer_id: USER_ID,
        status: 'draft',
        category: 'treasury_spend',
        title: 'My own draft proposal',
        description: 'A draft owned by the caller, in the state that permits submission.',
        created_at: new Date().toISOString(),
      },
    ];

    const res = await post('/api/governance/proposals/p-3/submit', {});

    expect(res.status).toBeLessThan(400);
  });

  it('delegating to yourself answers 400, not 500', async () => {
    const res = await post('/api/governance/delegate', { delegateId: USER_ID, allProposals: true });

    expect(res.status).toBe(400);
    expect(res.body.error.code).not.toBe('INTERNAL_ERROR');
  });
});
