-- Gate 71 only: fault injection in the throwaway gate71-pg platform DB. Not part of the repo's schema.
CREATE TABLE IF NOT EXISTS gate_fault (kind text PRIMARY KEY);
CREATE OR REPLACE FUNCTION gate_fault_tenants() RETURNS trigger AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM gate_fault WHERE kind = 'update_tenants') THEN RAISE EXCEPTION 'gate71 injected: update on tenants fails'; END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS gate_fault_tenants ON tenants;
CREATE TRIGGER gate_fault_tenants BEFORE UPDATE ON tenants FOR EACH ROW EXECUTE FUNCTION gate_fault_tenants();
CREATE OR REPLACE FUNCTION gate_fault_audit() RETURNS trigger AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM gate_fault WHERE kind = 'audit:' || NEW.action) THEN RAISE EXCEPTION 'gate71 injected: audit % fails', NEW.action; END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS gate_fault_audit ON platform_audit_log;
CREATE TRIGGER gate_fault_audit BEFORE INSERT ON platform_audit_log FOR EACH ROW EXECUTE FUNCTION gate_fault_audit();
-- Added after G71-M2 survived: a fault raised at COMMIT time (deferred constraint trigger), so a transaction that
-- already wrote its audit row is rolled back by the server. Distinguishes "audit on the tx client" from "audit on the pool".
CREATE OR REPLACE FUNCTION gate_fault_commit() RETURNS trigger AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM gate_fault WHERE kind = 'commit_tenants') THEN RAISE EXCEPTION 'gate71 injected: commit fails'; END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS gate_fault_commit ON tenants;
CREATE CONSTRAINT TRIGGER gate_fault_commit AFTER UPDATE ON tenants DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION gate_fault_commit();
