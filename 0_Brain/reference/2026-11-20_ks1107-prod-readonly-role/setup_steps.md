# KS-1107 production read-only role: setup steps for Kam (drafted 2026-11-20)

Source tags: [R]=repo file under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev (checkout develop 0e6479d7b; the pinned 33ba1d96d5fb is NOT in this checkout, so read-through is of 0e6479d7b); [G]=gate 381 verdict.md; [D]=Seat D 76th P5_prod_path.txt.

## BLUF

- What: one role, `ks1107_readonly`, that can only SELECT a handful of columns on three tables, lives 48 hours, then is dropped. One agent runs the reviewed existing-joiners query once, inside `BEGIN READ ONLY; ... ROLLBACK;`. Only counts go to Wednesday. [G pr_body query: users, organizations, organization_members]
- It exposes: every tenant's rows of those tables (user ids, roles, org ids, email_verified flags, timestamps). No email, password hash or MFA secret: the grant is column-level.
- IMPORTANT, contradicts the brief: migration 039 says "No BYPASSRLS anywhere (the Azure flexible-server admin can't mint it)" [R migrations/039_rls_fail_closed.sql:42]. If production is Azure flexible, `BYPASSRLS` will likely be refused. So Step A uses the repo's own reviewed escape: the policy lets any session read all rows when `app.tenant_scope_bypass = 'platform_admin'` [R 039:65, :73, applied to users and organizations]. The agent sets it inside its read-only transaction. A BYPASSRLS line is offered as optional A3.
- Kam's hands only: A (create), B (connection string into .env, any network step), D (teardown). I draft; I touch nothing.
- Which production? UNMEASURED. No production host appears in any record [D P5]. Two shapes in the repo: (1) Azure Database for PostgreSQL flexible server, version 15, admin `secuuraadmin`, VNet-only (delegated subnet + private DNS zone, no firewall resource) [R deployment/azure/main.bicep:196-219], named `<prefix>-pg`, env "demo" described as "production/demo" [R deploy.sh:50, :1042; RLS_ROLE_CUTOVER.md:58]; (2) a `postgres` container behind pgbouncer [R docker-compose.production.yml:29-34, :103]. Confirm which one you mean before Step A; commands differ only in connecting and in A3.

## Step A: create the role (run as the admin on the PRODUCTION database `secuura`)

A0. On your own Mac, make the password; never paste it into chat, mail or a ticket:

```
openssl rand -hex 24
```

A1. Connect as admin (`secuuraadmin` if flexible server [R RLS_ROLE_CUTOVER.md:9]) to database `secuura` and run, replacing PASSWORD_HERE with A0's output:

```
CREATE ROLE ks1107_readonly LOGIN PASSWORD 'PASSWORD_HERE' NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOBYPASSRLS CONNECTION LIMIT 1 VALID UNTIL 'EXPIRY_HERE';
```

(Replace EXPIRY_HERE with a time 48 hours after you run it, written out, for example `2026-11-22 12:00:00+11`. Postgres takes only a written-out time here, not an expression. Corrected by Wednesday 2026-11-20.)

A2. Read-only by default, and grants on exactly what the query reads [G pr_body; columns from R migrations/001_initial-schema.sql:18, :60, :75, 030_auth_user_columns.sql:19-28, 017_organizations_tenant_id.sql]:

```
ALTER ROLE ks1107_readonly SET default_transaction_read_only = on;
GRANT CONNECT ON DATABASE secuura TO ks1107_readonly;
GRANT USAGE ON SCHEMA public TO ks1107_readonly;
GRANT SELECT (id, tenant_id, organization_id, role, auth_method, status, email_verified, created_at, updated_at) ON users TO ks1107_readonly;
GRANT SELECT (id, tenant_id) ON organizations TO ks1107_readonly;
GRANT SELECT (organization_id, user_id) ON organization_members TO ks1107_readonly;
```

No `ALL TABLES`. Check, expect `f | f | f | 1`:

```
SELECT rolsuper, rolcreaterole, rolbypassrls, rolconnlimit FROM pg_roles WHERE rolname='ks1107_readonly';
```

A3 (optional, only if you want true BYPASSRLS; likely "permission denied" on flexible server per 039:42, works as superuser on a container): 

```
ALTER ROLE ks1107_readonly BYPASSRLS;
```

Why: users and organizations have FORCE RLS with a tenant GUC policy; without the GUC or BYPASSRLS the role sees 0 rows [R 039:107-111, :120-127]. organization_members: no RLS policy found in the migrations (grep of policies, zero hits; positive control: users/organizations hits) so it reads plainly, UNMEASURED on the live database.

Check on production before the run that 039 is applied (otherwise the older permissive 017 policy applies and the GUC is not needed): UNMEASURED.

## Step B: the way in for ONE agent

B1. You give: host, port 5432, database `secuura`, user `ks1107_readonly`, `sslmode=require` [R deploy.sh:684 uses this URL shape for the admin]. Put ONE line in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` (the .env is mode 600 [measured ls]; workspace rule 3 says gitignored). Variable name, proposed:

```
SECUURA_PROD_RO_DATABASE_URL=postgresql://ks1107_readonly:PASSWORD_HERE@HOST:5432/secuura?sslmode=require
```

Type it in an editor, not through a command that lands in shell history. Currently no such variable exists (count 0, positive control: file exists).

B2. Network: UNMEASURED beyond the repo. Likely shapes:
- Flexible server, VNet-integrated (what main.bicep defines): not reachable from the Mac. Options: (i) a temporary jump VM inside the VNet plus an SSH tunnel, host in the URL becomes `localhost`; (ii) Kam runs the one query himself via `az containerapp exec` into a service that has psql [R RUNBOOK.md:245, PENDING-DEPLOY.md:183] and pastes only counts. Option (ii) needs no agent access at all and no .env line.
- Flexible server with public access and firewall rules (not what the bicep shows): add a rule for the Mac's public IP only; removal in D.
- Container postgres (compose): `ports` are reset to none [R docker-compose.production.yml:30], so SSH tunnel to the host box: `ssh -L 5433:... ` then host `localhost:5433`.

## Step C: tell Wednesday, then the run

C1. You post one panel line: `KS-1107 prod read role READY, expires <time>, var SECUURA_PROD_RO_DATABASE_URL, network: <direct|tunnel|none>`.

C2. One Opus seat then does exactly this once, counts only to Wednesday, no row values in mail or tickets:

```
BEGIN READ ONLY;
SET LOCAL app.tenant_scope_bypass = 'platform_admin';
-- the reviewed query from PR 2259 body, wrapped as counts (total rows, cross_tenant true, is_member false, email_verified false)
ROLLBACK;
```

(The `SET LOCAL` line is dropped if A3 succeeded.) [G: query is a candidate design; it cannot see stub-claim exposures.]

## Step D: teardown (yours), with checks

D1. Drop the role (drop its grants first):

```
REVOKE ALL ON users, organizations, organization_members FROM ks1107_readonly;
REVOKE ALL ON SCHEMA public FROM ks1107_readonly;
REVOKE ALL ON DATABASE secuura FROM ks1107_readonly;
DROP ROLE ks1107_readonly;
```

Check, expect 0 rows:

```
SELECT rolname FROM pg_roles WHERE rolname='ks1107_readonly';
```

D2. Remove any firewall rule, tunnel or jump VM; check by listing rules or `ssh` refusal.

D3. Delete the `SECUURA_PROD_RO_DATABASE_URL` line from `.env`; check with `grep -c SECUURA_PROD_RO /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` (expect 0, after a positive control on another variable).

If you do nothing, VALID UNTIL stops the login at 48h, but the role object and grants remain: D1 is still needed.

## What could go wrong

- 0 rows returned: 039 applied and the GUC line missing, or A3 failed. Not an error in the role.
- `permission denied` on A3: expected on flexible server [R 039:42]; use the GUC route.
- The GUC route is available to ANY session that can read, so the grant list is the real limit; keep it column-level.
- Host unreachable: B2 is unmeasured; the choice is yours.
- The password reaches .env: keep it out of chat, mail, tickets, shell history.

## What each step does NOT do

A: no write, no DDL right for the role, no access to emails or hashes. B: no change to any service or app config. C: no row values leave the seat. D: does not undo queries (there are none that write).
