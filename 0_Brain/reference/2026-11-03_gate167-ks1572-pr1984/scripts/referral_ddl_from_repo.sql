-- =============================================================================
-- REFERRAL SERVICE
-- =============================================================================

CREATE TABLE IF NOT EXISTS svc_referral_codes (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    owner_id TEXT NOT NULL,
    owner_wallet_address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    max_uses INTEGER,
    current_uses INTEGER DEFAULT 0,
    custom_label TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_svc_ref_codes_owner ON svc_referral_codes(owner_id);
CREATE INDEX IF NOT EXISTS idx_svc_ref_codes_code ON svc_referral_codes(code);

CREATE TABLE IF NOT EXISTS svc_referrals (
    id TEXT PRIMARY KEY,
    referral_code_id TEXT NOT NULL REFERENCES svc_referral_codes(id),
    referrer_id TEXT NOT NULL,
    referred_user_id TEXT NOT NULL,
    referred_wallet_address TEXT,
    status TEXT NOT NULL DEFAULT 'PENDING',
    referrer_reward BIGINT DEFAULT 0,
    referred_reward BIGINT DEFAULT 0,
    fraud_check_passed BOOLEAN DEFAULT FALSE,
    fraud_flags JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    qualified_at TIMESTAMPTZ,
    reward_distributed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_svc_referrals_referrer ON svc_referrals(referrer_id);
CREATE INDEX IF NOT EXISTS idx_svc_referrals_code ON svc_referrals(referral_code_id);
CREATE INDEX IF NOT EXISTS idx_svc_referrals_status ON svc_referrals(status);

CREATE TABLE IF NOT EXISTS svc_referral_rewards (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    type TEXT NOT NULL,
    amount BIGINT NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'PENDING',
    source_id TEXT NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'REFERRAL',
    transaction_hash TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    claimed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_svc_ref_rewards_user ON svc_referral_rewards(user_id);
CREATE INDEX IF NOT EXISTS idx_svc_ref_rewards_status ON svc_referral_rewards(status);

CREATE TABLE IF NOT EXISTS svc_referral_milestones (
    user_id TEXT PRIMARY KEY,
    milestones_completed JSONB DEFAULT '[]',
    total_referrals INTEGER DEFAULT 0,
    total_rewards_earned BIGINT DEFAULT 0,
    current_tier TEXT DEFAULT 'starter',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS svc_referral_fraud_log (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    ip_address TEXT,
    device_fingerprint TEXT,
    referrer_id TEXT,
    flag_type TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_svc_fraud_log_ip ON svc_referral_fraud_log(ip_address);

-- =============================================================================
