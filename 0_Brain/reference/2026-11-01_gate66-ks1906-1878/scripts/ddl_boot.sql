CREATE TABLE IF NOT EXISTS vc_credentials_store (
    id TEXT PRIMARY KEY,
    credential JSONB NOT NULL,
    created_by_user_id TEXT,
    created_by_tenant_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
