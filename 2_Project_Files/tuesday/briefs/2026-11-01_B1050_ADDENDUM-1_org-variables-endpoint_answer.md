From Tuesday (the Datasec coordinator seat) to SEAT-G259, Datasec / NexusAI. ADDENDUM-1 to BRIEF B1050. Binding. This answers your STOPPED question of 14:41 (STATUS last line).

**Answer: neither (a) nor (b). The brief's "organization variables" read is the REPO-scoped endpoint, which this account can read.** The brief's FACTS line says `actions/organization-variables` (under the repository), not `orgs/datasecau/actions/variables`. Use:

`GH_CONFIG_DIR='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config' gh api -X GET repos/datasecau/Reporting_Dashboard_Au/actions/organization-variables`

It lists exactly the organization variables visible to this repository, which is the set `vars.CI_DEPLOY_ENABLED` in `deploy-demo.yml` can resolve to. Tuesday read it just before writing this addendum: HTTP 200, `total_count` 0 (and `repos/.../actions/variables` `total_count` 0). Re-read it yourself in REFUSE 6, C11 and C13 and quote your own figure with the time.

What changes, and only this:
1. Every read the brief calls "organization variables" / `actions/organization-variables` is the repo-scoped path above. Never call `orgs/datasecau/...` again.
2. The 403 you received on `orgs/datasecau/actions/variables` is recorded in STATUS (Corrections) as a wrong endpoint, not a deploy-switch result. REFUSE 6's "a 403 or other error ... STOP" applies to the three reads as defined here: if the repo-scoped read itself errors, STOP.
3. Everything else stands: clocks from your Step-0 date, round 1 of 2, every check and HOLD.

Resume from your STOP point; record this addendum's sha256 in STATUS before the next read.
