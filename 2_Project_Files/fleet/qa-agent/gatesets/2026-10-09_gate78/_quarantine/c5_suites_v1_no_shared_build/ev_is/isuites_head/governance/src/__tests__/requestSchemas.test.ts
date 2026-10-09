/**
 * =============================================================================
 * GOVERNANCE REQUEST-SCHEMA TESTS (KS-444)
 * =============================================================================
 * Pins the runtime request validators to the published OpenAPI contract for
 * the two write-path drifts adjudicated in KS-444:
 *
 *   1. POST /api/governance/delegate — the published spec emits
 *      `format: date-time` (RFC 3339 §5.6), which permits a numeric UTC
 *      offset as well as `Z`. Bare `.datetime()` rejected spec-legal offset
 *      timestamps (the KS-427 class); DelegateVoteSchema now uses
 *      `{ offset: true }`.
 *
 *   2. POST /api/governance/participants/register — the old ad-hoc truthy
 *      check accepted a spec-violating `walletAddress: {}` (any truthy
 *      value). RegisterParticipantSchema enforces exactly the published
 *      ParticipantRegisterRequest shape.
 * =============================================================================
 */

import { CastVoteSchema, CreateProposalSchema, DelegateVoteSchema, RegisterParticipantSchema } from '../types/governance.types';

describe('DelegateVoteSchema (KS-444 — RFC 3339 expiresAt)', () => {
  const base = { delegateId: 'delegate-1', allProposals: true };

  it('accepts a Z-suffixed UTC datetime', () => {
    const result = DelegateVoteSchema.safeParse({ ...base, expiresAt: '2030-01-01T00:00:00Z' });
    expect(result.success).toBe(true);
  });

  it('accepts a spec-legal numeric-offset datetime (RFC 3339 §5.6)', () => {
    // The exact value class Schemathesis generated from `format: date-time`
    // that the old bare `.datetime()` rejected with "Invalid datetime".
    const result = DelegateVoteSchema.safeParse({ ...base, expiresAt: '2030-01-01T00:00:00+05:30' });
    expect(result.success).toBe(true);
  });

  it('still rejects a non-datetime string', () => {
    const result = DelegateVoteSchema.safeParse({ ...base, expiresAt: 'not-a-date' });
    expect(result.success).toBe(false);
  });

  it('still allows expiresAt to be omitted', () => {
    const result = DelegateVoteSchema.safeParse(base);
    expect(result.success).toBe(true);
  });

  it('still requires allProposals (KS-430 reconciliation preserved)', () => {
    const result = DelegateVoteSchema.safeParse({ delegateId: 'delegate-1' });
    expect(result.success).toBe(false);
  });
});

describe('RegisterParticipantSchema (KS-444 — spec-exact register body)', () => {
  it('accepts the spec-minimal request', () => {
    const result = RegisterParticipantSchema.safeParse({ walletAddress: 'addr1qxyz', stakedAmount: 0 });
    expect(result.success).toBe(true);
  });

  it('accepts the full optional shape', () => {
    const result = RegisterParticipantSchema.safeParse({
      walletAddress: 'addr1qxyz',
      stakedAmount: 1500,
      did: 'did:secuura:abc',
      isDRep: true,
      isConstitutionalCommittee: false,
    });
    expect(result.success).toBe(true);
  });

  it('rejects a non-string walletAddress (the KS-444 finding: `{}` earned a 201)', () => {
    const result = RegisterParticipantSchema.safeParse({ walletAddress: {}, stakedAmount: 0 });
    expect(result.success).toBe(false);
  });

  it('rejects an empty walletAddress (pre-existing behaviour preserved)', () => {
    const result = RegisterParticipantSchema.safeParse({ walletAddress: '', stakedAmount: 0 });
    expect(result.success).toBe(false);
  });

  it('rejects a non-number stakedAmount', () => {
    const result = RegisterParticipantSchema.safeParse({ walletAddress: 'addr1qxyz', stakedAmount: '10' });
    expect(result.success).toBe(false);
  });

  it('rejects a missing body shape (bodyless request → {})', () => {
    const result = RegisterParticipantSchema.safeParse({});
    expect(result.success).toBe(false);
  });

  it('rejects wrong types on the optional role flags', () => {
    const result = RegisterParticipantSchema.safeParse({
      walletAddress: 'addr1qxyz',
      stakedAmount: 0,
      isDRep: 'yes',
    });
    expect(result.success).toBe(false);
  });
});

// KS-450: the gateway governance mock is removed — POST /api/governance/proposals
// and POST /api/governance/proposals/{id}/vote are now served live by this
// service, and the published spec (governance.openapi.ts ProposalCreateRequest /
// VoteRequest) was republished to these runtime validators. Pin them so the
// spec and the runtime cannot silently drift apart again.
describe('CreateProposalSchema (KS-450 — spec pinned to the live service)', () => {
  const valid = {
    title: 'Raise the verification quorum',
    description:
      'Increase the default quorum threshold for verification-category proposals from 10% to 15% to harden demo governance.',
    category: 'governance_change',
  };

  it('accepts the spec-minimal request (title ≥10, description ≥50, category)', () => {
    expect(CreateProposalSchema.safeParse(valid).success).toBe(true);
  });

  it('accepts the full optional shape (actions, discussionUrl, votingConfig)', () => {
    const result = CreateProposalSchema.safeParse({
      ...valid,
      actions: [{ actionType: 'parameter_update', parameters: { quorum: 1500 } }],
      discussionUrl: 'https://forum.example.com/t/quorum',
      votingConfig: { approvalThresholdBps: 5000, votingPeriodHours: 168 },
    });
    expect(result.success).toBe(true);
  });

  it('rejects a title under 10 chars (the published minLength)', () => {
    expect(CreateProposalSchema.safeParse({ ...valid, title: 'Too short' }).success).toBe(false);
  });

  it('rejects a description under 50 chars (the published minLength)', () => {
    expect(CreateProposalSchema.safeParse({ ...valid, description: 'Brief.' }).success).toBe(false);
  });

  it('rejects a missing category (required enum in spec and runtime)', () => {
    const { category: _category, ...noCategory } = valid;
    expect(CreateProposalSchema.safeParse(noCategory).success).toBe(false);
  });

  it('rejects an out-of-vocabulary category', () => {
    expect(CreateProposalSchema.safeParse({ ...valid, category: 'random' }).success).toBe(false);
  });

  it('rejects a non-url discussionUrl', () => {
    expect(CreateProposalSchema.safeParse({ ...valid, discussionUrl: 'not-a-url' }).success).toBe(false);
  });

  it('rejects an out-of-range votingConfig votingPeriodHours (max 720)', () => {
    expect(
      CreateProposalSchema.safeParse({ ...valid, votingConfig: { votingPeriodHours: 1000 } }).success,
    ).toBe(false);
  });
});

describe('CastVoteSchema body subset (KS-450 — the vote route parses omit proposalId)', () => {
  // The route parses CastVoteSchema.omit({ proposalId: true }) — the id comes
  // from the path param. Pin exactly that body-facing subset.
  const BodySchema = CastVoteSchema.omit({ proposalId: true });

  it('accepts each published vote option', () => {
    for (const vote of ['for', 'against', 'abstain']) {
      expect(BodySchema.safeParse({ vote }).success).toBe(true);
    }
  });

  it('accepts an optional reason within the 1000-char cap', () => {
    expect(BodySchema.safeParse({ vote: 'for', reason: 'r'.repeat(1000) }).success).toBe(true);
  });

  it('rejects the retired yes/no vocabulary (the KS-444 finding)', () => {
    expect(BodySchema.safeParse({ vote: 'yes' }).success).toBe(false);
  });

  it('rejects a missing vote (bodyless request)', () => {
    expect(BodySchema.safeParse({}).success).toBe(false);
  });

  it('rejects a reason over the published 1000-char cap', () => {
    expect(BodySchema.safeParse({ vote: 'for', reason: 'r'.repeat(1001) }).success).toBe(false);
  });
});
