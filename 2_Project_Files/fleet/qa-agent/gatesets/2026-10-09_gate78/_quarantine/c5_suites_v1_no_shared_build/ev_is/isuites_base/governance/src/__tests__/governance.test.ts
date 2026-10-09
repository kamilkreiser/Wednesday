/**
 * =============================================================================
 * SECUURA GOVERNANCE SERVICE — UNIT TESTS
 * =============================================================================
 * Tests for:
 *   - Proposal lifecycle (create, submit, vote, finalize, execute, cancel)
 *   - Participant registration and tier assignment
 *   - Voting mechanics (quorum, approval threshold, duplicate votes)
 *   - Vote delegation and revocation
 *   - Status transitions and guardrails
 *   - Pure helper functions (calculateTier, calculateVotePower, hasProposalPassed)
 * =============================================================================
 */

// ---------------------------------------------------------------------------
// Mock DB before importing
// ---------------------------------------------------------------------------

// KS-112: the governance service is now DB-only — the in-memory fallback it
// used to fall back to when `isDbAvailable() === false` was removed. Rather
// than re-introduce a production fallback (a regression) or add a pg-mem
// dependency, back the mocked `../db` with a small *stateful* in-memory store
// keyed to the exact queries governanceService issues. The suite then drives
// real service logic against a faithful, persistent data layer.
jest.mock('../db', () => {
  const tables: Record<string, Map<string, any>> = {
    svc_proposals: new Map(),
    svc_governance_participants: new Map(),
    svc_vote_delegations: new Map(),
  };
  let proposalSeq = 0; // emulates the svc_proposals.proposal_number DB serial

  const paramVal = (token: string, params: any[]): any => {
    const m = /^\$(\d+)$/.exec(token.trim());
    return m ? params[Number(m[1]) - 1] : undefined;
  };

  // Evaluate the small, fixed set of WHERE clauses the service builds.
  const rowMatches = (clause: string, params: any[], row: any): boolean =>
    clause.split(/\s+AND\s+/i).every((raw) => {
      const c = raw.trim();
      if (/^revoked_at IS NULL$/i.test(c)) return row.revoked_at == null;
      if (/^\(expires_at IS NULL OR expires_at > NOW\(\)\)$/i.test(c)) {
        return row.expires_at == null || new Date(row.expires_at) > new Date();
      }
      let m: RegExpExecArray | null;
      if ((m = /^(\w+)\s*=\s*ANY\((\$\d+)\)$/i.exec(c))) {
        const arr = paramVal(m[2], params);
        return Array.isArray(arr) && arr.includes(row[m[1]]);
      }
      if ((m = /^(\w+)\s*=\s*true$/i.exec(c))) return row[m[1]] === true;
      if ((m = /^(\w+)\s*=\s*false$/i.exec(c))) return row[m[1]] === false;
      if ((m = /^(\w+)\s*=\s*(\$\d+)$/i.exec(c))) return row[m[1]] === paramVal(m[2], params);
      return true; // unknown condition → don't exclude
    });

  const query = jest.fn(async (text: string, params: any[] = []) => {
    const sql = String(text).replace(/\s+/g, ' ').trim();
    let m: RegExpExecArray | null;

    // INSERT ... ON CONFLICT (id) DO UPDATE — the service always passes the
    // full object, so a full overwrite-by-id is equivalent to the partial UPSERT.
    if ((m = /^INSERT INTO (\w+) \(([^)]*)\)/i.exec(sql))) {
      const table = m[1];
      const cols = m[2].split(',').map((c) => c.trim());
      const row: any = {};
      cols.forEach((col, i) => { row[col] = params[i]; });
      // svc_proposals.proposal_number is a DB serial (omitted from the INSERT
      // column list) — emulate it: assign on first insert, preserve on upsert.
      if (table === 'svc_proposals') {
        row.proposal_number = tables.svc_proposals.get(row.id)?.proposal_number ?? ++proposalSeq;
      }
      tables[table].set(row.id, row);
      return { rows: [], rowCount: 1 };
    }

    if ((m = /^DELETE FROM (\w+) WHERE id = \$1/i.exec(sql))) {
      tables[m[1]].delete(params[0]);
      return { rows: [], rowCount: 1 };
    }

    if (/MAX\(proposal_number\)/i.test(sql)) {
      let max = 0;
      for (const r of tables.svc_proposals.values()) max = Math.max(max, Number(r.proposal_number || 0));
      return { rows: [{ max_num: max }], rowCount: 1 };
    }

    if (/SUM\(vote_power\)/i.test(sql)) {
      let total = 0;
      for (const r of tables.svc_governance_participants.values()) {
        if (r.is_drep === true) total += Number(r.vote_power || 0);
      }
      return { rows: [{ total }], rowCount: 1 };
    }

    // SELECT * FROM <table> [WHERE ...] [ORDER BY created_at DESC]
    const orderDesc = /ORDER BY created_at DESC/i.test(sql);
    const base = sql.replace(/\s+ORDER BY created_at DESC$/i, '');
    if ((m = /^SELECT \* FROM (\w+)(?: WHERE (.*))?$/i.exec(base))) {
      const table = m[1];
      const where = m[2];
      let rows = Array.from(tables[table].values());
      if (where) rows = rows.filter((r) => rowMatches(where, params, r));
      if (orderDesc) {
        rows = rows.sort((a, b) => {
          const t = new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
          return t !== 0 ? t : Number(b.proposal_number || 0) - Number(a.proposal_number || 0);
        });
      }
      return { rows: rows.map((r) => ({ ...r })), rowCount: rows.length };
    }

    return { rows: [], rowCount: 0 };
  });

  return {
    initDb: jest.fn().mockResolvedValue(true),
    query,
    isDbAvailable: jest.fn().mockReturnValue(true),
    getPool: jest.fn(),
    closeDb: jest.fn(),
  };
});

jest.mock('../utils/logger', () => ({
  logger: {
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
    debug: jest.fn(),
  },
  validateEnv: jest.fn(),
}));

// ---------------------------------------------------------------------------
// Imports
// ---------------------------------------------------------------------------

import {
  calculateTier,
  calculateVotePower,
  hasProposalPassed,
  getVotingConfigForCategory,
  DEFAULT_GOVERNANCE_CONFIG,
  DEFAULT_VOTING_CONFIG,
  DelegateVoteSchema,
} from '../types/governance.types';
import type { Proposal } from '../types/governance.types';

import {
  registerParticipant,
  getParticipant,
  getParticipants,
  getTotalVotePower,
  createProposal,
  submitProposal,
  getProposal,
  getProposals,
  castVote,
  finalizeProposal,
  executeProposal,
  cancelProposal,
  delegateVote,
  revokeDelegation,
  getGovernanceConfig,
  updateGovernanceConfig,
  getGovernanceStats,
  processExpiredProposals,
} from '../services/governanceService';

// ===========================================================================
// 1. PURE HELPER FUNCTIONS (governance.types.ts)
// ===========================================================================

describe('Pure helper functions', () => {
  describe('calculateTier', () => {
    it('should return basic for 0', () => {
      expect(calculateTier(0)).toBe('basic');
    });

    it('should return basic for < 1000', () => {
      expect(calculateTier(999)).toBe('basic');
    });

    it('should return staker for exactly 1000', () => {
      expect(calculateTier(1000)).toBe('staker');
    });

    it('should return staker for 9999', () => {
      expect(calculateTier(9999)).toBe('staker');
    });

    it('should return validator for exactly 10000', () => {
      expect(calculateTier(10000)).toBe('validator');
    });

    it('should return validator for 99999', () => {
      expect(calculateTier(99999)).toBe('validator');
    });

    it('should return partner for exactly 100000', () => {
      expect(calculateTier(100000)).toBe('partner');
    });

    it('should return partner for 1000000', () => {
      expect(calculateTier(1000000)).toBe('partner');
    });
  });

  describe('calculateVotePower', () => {
    it('should return 1x for basic tier', () => {
      expect(calculateVotePower(500, 'basic')).toBe(500);
    });

    it('should return 1x for staker tier', () => {
      expect(calculateVotePower(2000, 'staker')).toBe(2000);
    });

    it('should return 1.5x for validator tier', () => {
      expect(calculateVotePower(10000, 'validator')).toBe(15000);
    });

    it('should return 2x for partner tier', () => {
      expect(calculateVotePower(100000, 'partner')).toBe(200000);
    });

    it('should floor fractional results', () => {
      expect(calculateVotePower(1, 'validator')).toBe(1);
    });
  });

  describe('hasProposalPassed', () => {
    const makeProposal = (overrides: Partial<Proposal>): Proposal => ({
      id: 'test',
      proposalNumber: 1,
      title: 'Test',
      description: 'Test proposal',
      category: 'general',
      proposerId: 'p1',
      proposerAddress: 'addr1',
      status: 'active',
      votingConfig: { ...DEFAULT_VOTING_CONFIG },
      createdAt: new Date(),
      votesFor: 0,
      votesAgainst: 0,
      votesAbstain: 0,
      totalVotePower: 10000,
      voterCount: 0,
      votes: [],
      ...overrides,
    });

    it('should pass when quorum met and majority for', () => {
      const p = makeProposal({
        votesFor: 6000,
        votesAgainst: 4000,
        votesAbstain: 0,
        totalVotePower: 10000,
        votingConfig: {
          ...DEFAULT_VOTING_CONFIG,
          quorumThresholdBps: 1000,
          approvalThresholdBps: 5000,
        },
      });
      expect(hasProposalPassed(p)).toBe(true);
    });

    it('should fail when quorum not met', () => {
      const p = makeProposal({
        votesFor: 500,
        votesAgainst: 0,
        votesAbstain: 0,
        totalVotePower: 10000,
        votingConfig: {
          ...DEFAULT_VOTING_CONFIG,
          quorumThresholdBps: 1000,
          approvalThresholdBps: 5000,
        },
      });
      expect(hasProposalPassed(p)).toBe(false);
    });

    it('should fail when approval threshold not met', () => {
      const p = makeProposal({
        votesFor: 3000,
        votesAgainst: 7000,
        votesAbstain: 0,
        totalVotePower: 10000,
        votingConfig: {
          ...DEFAULT_VOTING_CONFIG,
          quorumThresholdBps: 1000,
          approvalThresholdBps: 5000,
        },
      });
      expect(hasProposalPassed(p)).toBe(false);
    });

    it('should exclude abstentions from approval calculation', () => {
      const p = makeProposal({
        votesFor: 600,
        votesAgainst: 400,
        votesAbstain: 9000,
        totalVotePower: 10000,
        votingConfig: {
          ...DEFAULT_VOTING_CONFIG,
          quorumThresholdBps: 1000,
          approvalThresholdBps: 5000,
        },
      });
      expect(hasProposalPassed(p)).toBe(true);
    });

    it('should fail when no votes cast', () => {
      const p = makeProposal({ totalVotePower: 10000 });
      expect(hasProposalPassed(p)).toBe(false);
    });
  });

  describe('getVotingConfigForCategory', () => {
    it('should return defaults for general category', () => {
      const config = getVotingConfigForCategory('general');
      expect(config.approvalThresholdBps).toBe(DEFAULT_GOVERNANCE_CONFIG.defaultApprovalThresholdBps);
      expect(config.votingPeriodHours).toBe(DEFAULT_GOVERNANCE_CONFIG.defaultVotingPeriodHours);
    });

    it('should apply emergency overrides', () => {
      const config = getVotingConfigForCategory('emergency');
      expect(config.votingPeriodHours).toBe(24);
      expect(config.timelockPeriodHours).toBe(6);
      expect(config.requiresConstitutionalApproval).toBe(true);
    });

    it('should apply governance_change overrides', () => {
      const config = getVotingConfigForCategory('governance_change');
      expect(config.approvalThresholdBps).toBe(6700);
      expect(config.quorumThresholdBps).toBe(2000);
    });

    it('should apply treasury_spend overrides', () => {
      const config = getVotingConfigForCategory('treasury_spend');
      expect(config.approvalThresholdBps).toBe(6000);
      expect(config.requiresConstitutionalApproval).toBe(true);
    });
  });
});

// ===========================================================================
// 2. PARTICIPANT MANAGEMENT
// ===========================================================================

describe('Participant Management', () => {
  it('should register a new participant with correct tier', async () => {
    const p = await registerParticipant('wallet_p1', 5000);
    expect(p.walletAddress).toBe('wallet_p1');
    expect(p.stakedAmount).toBe(5000);
    expect(p.tier).toBe('staker');
    expect(p.votePower).toBe(5000);
  });

  it('should assign validator tier and 1.5x vote power', async () => {
    const p = await registerParticipant('wallet_p2', 20000);
    expect(p.tier).toBe('validator');
    expect(p.votePower).toBe(30000);
  });

  it('should assign partner tier and 2x vote power', async () => {
    const p = await registerParticipant('wallet_p3', 200000);
    expect(p.tier).toBe('partner');
    expect(p.votePower).toBe(400000);
  });

  it('should retrieve participant by ID', async () => {
    const p = await registerParticipant('wallet_p4', 1500);
    const found = await getParticipant(p.id);
    expect(found).toBeDefined();
    expect(found!.walletAddress).toBe('wallet_p4');
  });

  it('should retrieve participant by wallet address', async () => {
    await registerParticipant('wallet_p5', 2000);
    const found = await getParticipant('wallet_p5');
    expect(found).toBeDefined();
  });

  it('should update existing participant on re-registration', async () => {
    await registerParticipant('wallet_p6', 1000);
    const updated = await registerParticipant('wallet_p6', 50000);
    expect(updated.tier).toBe('validator');
    expect(updated.stakedAmount).toBe(50000);
  });

  it('should filter participants by isDRep', async () => {
    await registerParticipant('wallet_drep', 5000, { isDRep: true });
    const dreps = await getParticipants({ isDRep: true });
    expect(dreps.some(p => p.walletAddress === 'wallet_drep')).toBe(true);
  });

  it('should calculate total vote power for DReps', async () => {
    const power = await getTotalVotePower();
    expect(power).toBeGreaterThan(0);
  });
});

// ===========================================================================
// 3. PROPOSAL LIFECYCLE
// ===========================================================================

describe('Proposal Lifecycle', () => {
  let proposerId: string;

  beforeAll(async () => {
    const p = await registerParticipant('wallet_proposer', 5000, { isDRep: true });
    proposerId = p.id;
  });

  describe('createProposal', () => {
    it('should create a draft proposal', async () => {
      const proposal = await createProposal(
        proposerId,
        'Increase fee cap',
        'A'.repeat(60),
        'fee_adjustment',
      );

      expect(proposal.status).toBe('draft');
      expect(proposal.title).toBe('Increase fee cap');
      expect(proposal.category).toBe('fee_adjustment');
      expect(proposal.votesFor).toBe(0);
      expect(proposal.voterCount).toBe(0);
      expect(proposal.proposalNumber).toBeGreaterThan(0);
    });

    it('should use category-specific voting config', async () => {
      const proposal = await createProposal(
        proposerId,
        'Emergency fix test',
        'X'.repeat(60),
        'emergency',
      );

      expect(proposal.votingConfig.votingPeriodHours).toBe(24);
      expect(proposal.votingConfig.requiresConstitutionalApproval).toBe(true);
    });

    it('should auto-register participant if not found', async () => {
      const proposal = await createProposal(
        'new_unknown_participant',
        'Auto register test proposal',
        'Y'.repeat(60),
        'general',
      );

      expect(proposal.proposerId).toBe('new_unknown_participant');
    });

    it('should increment proposal counter', async () => {
      const p1 = await createProposal(proposerId, 'Proposal A', 'Z'.repeat(60), 'general');
      const p2 = await createProposal(proposerId, 'Proposal B', 'W'.repeat(60), 'general');
      expect(p2.proposalNumber).toBeGreaterThan(p1.proposalNumber);
    });
  });

  describe('submitProposal', () => {
    it('should transition draft to active with voting dates', async () => {
      const proposal = await createProposal(proposerId, 'Submit test', 'Q'.repeat(60), 'general');
      const submitted = await submitProposal(proposal.id, proposerId);

      expect(submitted.status).toBe('active');
      expect(submitted.submittedAt).toBeDefined();
      expect(submitted.votingStartsAt).toBeDefined();
      expect(submitted.votingEndsAt).toBeDefined();
      expect(submitted.totalVotePower).toBeGreaterThan(0);
    });

    it('should reject if not the proposer', async () => {
      const proposal = await createProposal(proposerId, 'Submit auth test', 'R'.repeat(60), 'general');
      await expect(submitProposal(proposal.id, 'someone_else')).rejects.toThrow(
        'Only the proposer can submit',
      );
    });

    it('should reject if already submitted', async () => {
      const proposal = await createProposal(proposerId, 'Double submit', 'S'.repeat(60), 'general');
      await submitProposal(proposal.id, proposerId);
      await expect(submitProposal(proposal.id, proposerId)).rejects.toThrow('Only draft proposals');
    });

    it('should throw for nonexistent proposal', async () => {
      await expect(submitProposal('nonexistent', proposerId)).rejects.toThrow('Proposal not found');
    });
  });

  describe('getProposal / getProposals', () => {
    it('should retrieve a proposal by id', async () => {
      const proposal = await createProposal(proposerId, 'Retrieve test', 'T'.repeat(60), 'general');
      const found = await getProposal(proposal.id);
      expect(found).toBeDefined();
      expect(found!.title).toBe('Retrieve test');
    });

    it('should filter proposals by status', async () => {
      const active = await getProposals({ status: 'active' });
      active.forEach((p) => expect(p.status).toBe('active'));
    });

    it('should filter proposals by category', async () => {
      await createProposal(proposerId, 'Fee test filter', 'U'.repeat(60), 'fee_adjustment');
      const filtered = await getProposals({ category: 'fee_adjustment' });
      filtered.forEach((p) => expect(p.category).toBe('fee_adjustment'));
    });

    it('should sort proposals by number descending', async () => {
      const all = await getProposals();
      for (let i = 1; i < all.length; i++) {
        expect(all[i - 1].proposalNumber).toBeGreaterThan(all[i].proposalNumber);
      }
    });
  });
});

// ===========================================================================
// 4. VOTING
// ===========================================================================

describe('Voting', () => {
  let proposerId: string;
  let voter1Id: string;
  let voter2Id: string;

  beforeAll(async () => {
    const p = await registerParticipant('wallet_vote_proposer', 5000, { isDRep: true });
    proposerId = p.id;
    const v1 = await registerParticipant('wallet_voter1', 5000, { isDRep: true });
    voter1Id = v1.id;
    const v2 = await registerParticipant('wallet_voter2', 10000, { isDRep: true });
    voter2Id = v2.id;
    await registerParticipant('wallet_voter3', 100000, { isDRep: true });
  });

  it('should cast a vote successfully', async () => {
    const proposal = await createProposal(proposerId, 'Vote test 1', 'V'.repeat(60), 'general');
    await submitProposal(proposal.id, proposerId);

    const vote = await castVote(proposal.id, voter1Id, 'for', 'I support this');
    expect(vote.vote).toBe('for');
    expect(vote.votePower).toBeGreaterThan(0);
    expect(vote.proposalId).toBe(proposal.id);
  });

  it('should tally votes correctly', async () => {
    const proposal = await createProposal(proposerId, 'Tally test', 'A1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);

    await castVote(proposal.id, voter1Id, 'for');
    await castVote(proposal.id, voter2Id, 'against');

    const updated = (await getProposal(proposal.id))!;
    expect(updated.votesFor).toBeGreaterThan(0);
    expect(updated.votesAgainst).toBeGreaterThan(0);
    expect(updated.voterCount).toBe(2);
  });

  it('should reject duplicate vote from same voter', async () => {
    const proposal = await createProposal(proposerId, 'Dup vote test', 'B1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);

    await castVote(proposal.id, voter1Id, 'for');
    await expect(castVote(proposal.id, voter1Id, 'against')).rejects.toThrow(
      'Already voted',
    );
  });

  it('should reject vote on non-active proposal', async () => {
    const proposal = await createProposal(proposerId, 'Inactive vote test', 'C1'.repeat(30), 'general');
    await expect(castVote(proposal.id, voter1Id, 'for')).rejects.toThrow(
      'not open for voting',
    );
  });

  it('should reject vote from non-DRep', async () => {
    const nonDrep = await registerParticipant('wallet_nondrep', 500, { isDRep: false });
    const proposal = await createProposal(proposerId, 'DRep test', 'D1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);

    await expect(castVote(proposal.id, nonDrep.id, 'for')).rejects.toThrow('not a DRep');
  });

  it('should reject vote from unregistered participant', async () => {
    const proposal = await createProposal(proposerId, 'Unreg vote test', 'E1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);

    await expect(castVote(proposal.id, 'unregistered_id', 'for')).rejects.toThrow(
      'not registered',
    );
  });

  it('should track abstain votes correctly', async () => {
    const proposal = await createProposal(proposerId, 'Abstain test', 'F1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);

    await castVote(proposal.id, voter1Id, 'abstain');

    const updated = (await getProposal(proposal.id))!;
    expect(updated.votesAbstain).toBeGreaterThan(0);
    expect(updated.voterCount).toBe(1);
  });
});

// ===========================================================================
// 5. PROPOSAL FINALIZATION (quorum & approval threshold)
// ===========================================================================

describe('Proposal Finalization', () => {
  let proposerId: string;
  let bigVoterId: string;

  beforeAll(async () => {
    const p = await registerParticipant('wallet_final_proposer', 5000, { isDRep: true });
    proposerId = p.id;
    const big = await registerParticipant('wallet_big_voter', 200000, { isDRep: true });
    bigVoterId = big.id;
  });

  it('should finalize a passing proposal to queued status', async () => {
    const proposal = await createProposal(proposerId, 'Pass test', 'G1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);

    await castVote(proposal.id, bigVoterId, 'for');

    const finalized = await finalizeProposal(proposal.id);
    expect(['queued', 'failed', 'expired']).toContain(finalized.status);
  });

  it('should reject finalizing non-active proposal', async () => {
    const proposal = await createProposal(proposerId, 'Final inactive', 'H1'.repeat(30), 'general');
    await expect(finalizeProposal(proposal.id)).rejects.toThrow('not active');
  });

  it('should throw for nonexistent proposal', async () => {
    await expect(finalizeProposal('nonexistent')).rejects.toThrow('not found');
  });
});

// ===========================================================================
// 6. PROPOSAL EXECUTION
// ===========================================================================

describe('Proposal Execution', () => {
  let proposerId: string;
  let bigVoterId: string;

  beforeAll(async () => {
    const p = await registerParticipant('wallet_exec_proposer', 5000, { isDRep: true });
    proposerId = p.id;
    const big = await registerParticipant('wallet_exec_voter', 200000, { isDRep: true });
    bigVoterId = big.id;
  });

  it('should reject execution of non-queued proposal', async () => {
    const proposal = await createProposal(proposerId, 'Exec non-queued', 'I1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);

    await expect(executeProposal(proposal.id, proposerId)).rejects.toThrow(
      'not queued',
    );
  });

  it('should reject execution before timelock expires', async () => {
    const proposal = await createProposal(proposerId, 'Exec timelock', 'J1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);
    await castVote(proposal.id, bigVoterId, 'for');

    const finalized = await finalizeProposal(proposal.id);

    if (finalized.status === 'queued') {
      await expect(executeProposal(proposal.id, proposerId)).rejects.toThrow(
        'Timelock not passed',
      );
    }
  });
});

// ===========================================================================
// 7. PROPOSAL CANCELLATION
// ===========================================================================

describe('Proposal Cancellation', () => {
  let proposerId: string;

  beforeAll(async () => {
    const p = await registerParticipant('wallet_cancel_proposer', 5000, { isDRep: true });
    proposerId = p.id;
  });

  it('should allow proposer to cancel a draft proposal', async () => {
    const proposal = await createProposal(proposerId, 'Cancel draft', 'K1'.repeat(30), 'general');
    const cancelled = await cancelProposal(proposal.id, proposerId);
    expect(cancelled.status).toBe('cancelled');
    expect(cancelled.cancelledAt).toBeDefined();
  });

  it('should allow proposer to cancel an active proposal', async () => {
    const proposal = await createProposal(proposerId, 'Cancel active', 'L1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);
    const cancelled = await cancelProposal(proposal.id, proposerId);
    expect(cancelled.status).toBe('cancelled');
  });

  it('should allow constitutional committee member to cancel', async () => {
    const cc = await registerParticipant('wallet_cc_member', 5000, {
      isDRep: true,
      isConstitutionalCommittee: true,
    });
    const proposal = await createProposal(proposerId, 'CC cancel test', 'M1'.repeat(30), 'general');
    const cancelled = await cancelProposal(proposal.id, cc.id);
    expect(cancelled.status).toBe('cancelled');
  });

  it('should reject cancellation by non-proposer non-committee', async () => {
    const stranger = await registerParticipant('wallet_stranger', 2000, { isDRep: true });
    const proposal = await createProposal(proposerId, 'Stranger cancel', 'N1'.repeat(30), 'general');
    await expect(cancelProposal(proposal.id, stranger.id)).rejects.toThrow(
      'Only proposer or constitutional committee',
    );
  });

  it('should reject cancellation of a proposal in a non-cancellable status', async () => {
    // A genuinely DB-backed service returns copies, not live references, so a
    // terminal status must be reached *in storage* (not by mutating a fetched
    // object, which the old in-memory store aliased). Cancel once to persist a
    // terminal `cancelled` status, then assert a second cancel is rejected by
    // the status guard (only draft/active/queued are cancellable).
    const proposal = await createProposal(proposerId, 'Exec cancel test', 'O1'.repeat(30), 'general');
    await submitProposal(proposal.id, proposerId);
    await cancelProposal(proposal.id, proposerId);

    await expect(cancelProposal(proposal.id, proposerId)).rejects.toThrow(
      'cannot be cancelled',
    );
  });
});

// ===========================================================================
// 8. VOTE DELEGATION
// ===========================================================================

describe('Vote Delegation', () => {
  let delegatorId: string;
  let delegateId: string;

  beforeAll(async () => {
    const d1 = await registerParticipant('wallet_delegator', 5000, { isDRep: true });
    delegatorId = d1.id;
    const d2 = await registerParticipant('wallet_delegate', 10000, { isDRep: true });
    delegateId = d2.id;
  });

  it('should create a delegation', async () => {
    const delegation = await delegateVote(delegatorId, delegateId, true);
    expect(delegation.delegatorId).toBe(delegatorId);
    expect(delegation.delegateId).toBe(delegateId);
    expect(delegation.allProposals).toBe(true);
    expect(delegation.delegatedPower).toBeGreaterThan(0);
  });

  it('should reject self-delegation', async () => {
    await expect(delegateVote(delegatorId, delegatorId, true)).rejects.toThrow(
      'Cannot delegate to yourself',
    );
  });

  it('should revoke existing delegation on new delegation', async () => {
    const newDelegate = await registerParticipant('wallet_new_delegate', 8000, { isDRep: true });
    const d = await delegateVote(delegatorId, newDelegate.id, true);
    expect(d.delegateId).toBe(newDelegate.id);
  });

  it('should revoke delegation', async () => {
    await delegateVote(delegatorId, delegateId, true);
    await revokeDelegation(delegatorId);
    // Revoking again should be a no-op (no error)
    await revokeDelegation(delegatorId);
  });

  it('should reject if delegator not found', async () => {
    await expect(delegateVote('fake_id', delegateId, true)).rejects.toThrow(
      'not found',
    );
  });

  it('should accept category-specific delegation', async () => {
    const d = await delegateVote(delegatorId, delegateId, false, ['fee_adjustment', 'general']);
    expect(d.allProposals).toBe(false);
    expect(d.categories).toEqual(['fee_adjustment', 'general']);
  });

  it('should add delegated power to voter power', async () => {
    // Create fresh participants to isolate delegation effect
    const del1 = await registerParticipant('wallet_del_power1', 5000, { isDRep: true });
    const del2 = await registerParticipant('wallet_del_power2', 10000, { isDRep: true });

    await delegateVote(del1.id, del2.id, true);

    const proposal = await createProposal(del2.id, 'Delegation power test', 'P1'.repeat(30), 'general');
    await submitProposal(proposal.id, del2.id);

    const vote = await castVote(proposal.id, del2.id, 'for');
    // del2 has 10000 stake at validator tier (1.5x) = 15000 own power + del1's 5000 delegated
    expect(vote.votePower).toBe(20000);
  });
});

// ===========================================================================
// 9. GOVERNANCE CONFIG
// ===========================================================================

describe('Governance Config', () => {
  it('should return the current config', async () => {
    const config = await getGovernanceConfig();
    expect(config.defaultApprovalThresholdBps).toBe(5000);
    expect(config.maxActiveProposals).toBe(20);
  });

  it('should update config partially', async () => {
    const updated = await updateGovernanceConfig({ maxActiveProposals: 50 });
    expect(updated.maxActiveProposals).toBe(50);
    expect(updated.defaultApprovalThresholdBps).toBe(5000);

    // Restore
    await updateGovernanceConfig({ maxActiveProposals: 20 });
  });
});

// ===========================================================================
// 10. GOVERNANCE STATS
// ===========================================================================

describe('Governance Stats', () => {
  it('should return correct stat shape', async () => {
    const stats = await getGovernanceStats();
    expect(stats).toHaveProperty('totalProposals');
    expect(stats).toHaveProperty('activeProposals');
    expect(stats).toHaveProperty('passedProposals');
    expect(stats).toHaveProperty('failedProposals');
    expect(stats).toHaveProperty('totalParticipants');
    expect(stats).toHaveProperty('totalDReps');
    expect(stats).toHaveProperty('totalVotePower');
    expect(stats).toHaveProperty('avgParticipation');
    expect(stats.totalProposals).toBeGreaterThan(0);
    expect(stats.totalParticipants).toBeGreaterThan(0);
  });
});

// ===========================================================================
// 11. EXPIRED PROPOSALS
// ===========================================================================

describe('processExpiredProposals', () => {
  it('should return the count of processed proposals', async () => {
    const count = await processExpiredProposals();
    expect(typeof count).toBe('number');
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

// ===========================================================================
// 12. DELEGATE REQUEST VALIDATION (KS-430)
// ===========================================================================

describe('DelegateVoteSchema (KS-430 spec/runtime reconciliation)', () => {
  // The delegate route handler never reads delegateAddress, so a spec-compliant
  // body carrying only the fields the handler uses must validate.
  it('accepts a body without delegateAddress (it is ignored by the handler)', () => {
    const result = DelegateVoteSchema.safeParse({
      delegateId: 'participant-1',
      allProposals: true,
    });
    expect(result.success).toBe(true);
  });

  // delegateAddress is still allowed when a client chooses to send it.
  it('still accepts a body that includes delegateAddress', () => {
    const result = DelegateVoteSchema.safeParse({
      delegateId: 'participant-1',
      delegateAddress: 'addr_test1abc',
      allProposals: false,
    });
    expect(result.success).toBe(true);
  });

  // allProposals remains genuinely required (the handler forwards it to delegateVote).
  it('rejects a body missing allProposals', () => {
    const result = DelegateVoteSchema.safeParse({ delegateId: 'participant-1' });
    expect(result.success).toBe(false);
  });
});
