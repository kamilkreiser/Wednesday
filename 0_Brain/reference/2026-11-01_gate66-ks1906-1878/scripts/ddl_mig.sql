CREATE TABLE IF NOT EXISTS vc_credentials_store (
    id TEXT PRIMARY KEY,
    credential JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE vc_credentials_store   ADD COLUMN IF NOT EXISTS created_by_user_id   TEXT;
ALTER TABLE vc_credentials_store   ADD COLUMN IF NOT EXISTS created_by_tenant_id TEXT;
