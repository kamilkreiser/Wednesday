CREATE TABLE IF NOT EXISTS svc_proposals (
    id TEXT PRIMARY KEY,
    proposal_number SERIAL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'general',
    proposer_id TEXT NOT NULL,
    proposer_address TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    voting_config JSONB NOT NULL DEFAULT '{}',
    actions JSONB DEFAULT '[]',
    votes_for NUMERIC DEFAULT 0,
    votes_against NUMERIC DEFAULT 0,
    votes_abstain NUMERIC DEFAULT 0,
    total_vote_power NUMERIC DEFAULT 0,
    voter_count INTEGER DEFAULT 0,
    votes JSONB DEFAULT '[]',
    tx_hash TEXT,
    datum_hash TEXT,
    discussion_url TEXT,
    ipfs_hash TEXT,
    submitted_at TIMESTAMPTZ,
    voting_starts_at TIMESTAMPTZ,
    voting_ends_at TIMESTAMPTZ,
    queued_at TIMESTAMPTZ,
    execution_eta TIMESTAMPTZ,
    executed_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_svc_proposals_status ON svc_proposals(status);
CREATE INDEX IF NOT EXISTS idx_svc_proposals_proposer ON svc_proposals(proposer_id);
CREATE INDEX IF NOT EXISTS idx_svc_proposals_category ON svc_proposals(category);

CREATE TABLE IF NOT EXISTS svc_governance_participants (
    id TEXT PRIMARY KEY,
    wallet_address TEXT NOT NULL UNIQUE,
    did TEXT,
    staked_amount NUMERIC DEFAULT 0,
    tier TEXT NOT NULL DEFAULT 'basic',
    vote_power NUMERIC DEFAULT 0,
    is_drep BOOLEAN DEFAULT FALSE,
    is_constitutional_committee BOOLEAN DEFAULT FALSE,
    proposals_created INTEGER DEFAULT 0,
    votes_cast INTEGER DEFAULT 0,
    last_active_at TIMESTAMPTZ DEFAULT NOW(),
    joined_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_svc_gov_participants_tier ON svc_governance_participants(tier);

CREATE TABLE IF NOT EXISTS svc_vote_delegations (
    id TEXT PRIMARY KEY,
    delegator_id TEXT NOT NULL,
    delegator_address TEXT NOT NULL,
    delegate_id TEXT NOT NULL,
    delegate_address TEXT NOT NULL,
    delegated_power NUMERIC NOT NULL DEFAULT 0,
    all_proposals BOOLEAN DEFAULT TRUE,
    categories JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);
