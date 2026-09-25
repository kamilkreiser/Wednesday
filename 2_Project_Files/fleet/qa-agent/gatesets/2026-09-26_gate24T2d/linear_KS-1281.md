KS-1281 vc-issuer boot warns 'Could not ensure vc_credentials_store table … permission denied for schema public' (runtime DDL vs least privilege; benign, migration 001 owns the table)
state In Progress

## BLUF

Every vc-issuer boot logs one WARN: `Could not ensure vc_credentials_store table {"error":"permission denied for schema public"}`. It is pre-existing. Seat A 14th's scoped kintsugi deploy (develop `f9c28a8b8`, 2026-09-19) surfaced it: the warn was present before and after the vc-issuer swap. It is benign today, because migration 001 creates the table. The pattern is runtime DDL against a least-privilege role.

## Recommendation

Low priority, no rush. Remove the runtime `CREATE TABLE` from `credentialRepo.ensureTable()`, since the migration path already owns the table, or reduce it to an existence check. No action is needed on any running environment.

## Detail

* **Where:** `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts:28-42`.
  * `ensureTable()` runs `CREATE TABLE IF NOT EXISTS vc_credentials_store (…)` and logs the WARN when it fails.
  * It is called from 6 sites (:57, :79, :116, :149, :213, :254).
  * It has been in place since `e50dbde98` (2026-02-18).
* **Why it is benign:** the table is created on the migration path: `migrations/001_initial-schema.sql:745` (since `ca7c2bf03`, 2026-03-22) and `docker/init/03-service-tables.sql:135`. The runtime role lacks CREATE on schema `public`, so only the DDL fails.
* **Read from source, not measured on the box:** on a failure `tableEnsured` stays `false`, so each later call re-runs the CREATE and logs again. On kintsugi there have been 0 credential operations since the new container started, so the once-per-boot count is all that was observed.
* **Measured on kintsugi (read-only log counts):**
  * before the swap: 1 WARN in 1832 lines (container start 2026-09-18T22:21:34Z);
  * after the swap: 1 WARN in 43 lines (start 2026-09-19T06:09:06Z).
* **History:** KS-92 and KS-110 (both Done and archived) hardened runtime DDL for the `secuura_app` cutover. KS-110's investigation comment lists vc-issuer as doing "only a `SELECT 1` health check, no DDL", but this `ensureTable` predates it. That is how the site was missed.
* **Board search before filing** (`searchIssues`, archived and comments included, literal match on title and description):
  * Terms: the literal warn text, `vc_credentials_store`, `permission denied for schema public`, and `ensureTable vc-issuer credentialRepo`. 244 issues returned.
  * The nearest non-match is **KS-1121** (credentialRepo substring lookup: same file, different defect).
  * The literal `permission denied for schema public` hits (KS-92, KS-110, KS-215, KS-419, KS-60, KS-72, KS-80) are other services or closed history. None tracks this site.
* Filed by seat A 14th on Wednesday's ruling (2026-09-19 06:16:57Z). Related to KS-1272, the analogous pre-existing api-gateway boot WARN.
