-- gate 134 throwaway schema: governance tables verbatim from docker/init/04-sprint2-service-tables.sql (extracted by pg_up.sh),
-- users with migration 039's fail-closed tenant_isolation policy, ENABLE + FORCE RLS; app role without SUPERUSER / BYPASSRLS.
CREATE TABLE users (id uuid PRIMARY KEY, tenant_id uuid NOT NULL, email text, wallet_address text);
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE users FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON users
  USING ((current_setting('app.current_tenant_id', true) IS NOT NULL AND current_setting('app.current_tenant_id', true) <> ''
          AND tenant_id::text = current_setting('app.current_tenant_id', true))
         OR current_setting('app.tenant_scope_bypass', true) = 'platform_admin')
  WITH CHECK ((current_setting('app.current_tenant_id', true) IS NOT NULL AND current_setting('app.current_tenant_id', true) <> ''
          AND tenant_id::text = current_setting('app.current_tenant_id', true))
         OR current_setting('app.tenant_scope_bypass', true) = 'platform_admin');
CREATE ROLE gate_app LOGIN PASSWORD 'gate134local' NOSUPERUSER NOBYPASSRLS;
GRANT SELECT ON users TO gate_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON svc_proposals, svc_governance_participants, svc_vote_delegations TO gate_app;
GRANT USAGE, SELECT ON SEQUENCE svc_proposals_proposal_number_seq TO gate_app;
