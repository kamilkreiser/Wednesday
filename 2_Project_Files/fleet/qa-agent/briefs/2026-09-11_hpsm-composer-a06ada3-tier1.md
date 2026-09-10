# QA GATE — TIER 1, round 1 — Datasec / HPSM — Policy Composer WP0 + WP1 + WP2 @ a06ada3

**Why TIER 1:** this build carries row-level security and tenant isolation, a secret-scanning control, and an egress (no-cloud) proof. All are security surfaces (learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap). **Round 1 of 2 under the cap.**

**What the verdict is used for:** Tuesday scores the build session on it, and the next Composer work packages (the rules engine and the API that wires RLS into the stack) are built on top of this head. **A GO is a statement about the SHA `a06ada39c4554655607f658b81fe5d367a1bfe90`, never about the repo.**

## Charter (read first, in full)
`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` (this machine's copy; the template's DevMASTER path is not mounted here).

## 1. Target
- **Client / Project:** Datasec / HPSM, the Policy Composer (Phase 1). **R0: only Datasec content is in this brief. Name no other client.**
- **Code under test:** the local git repository `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`, branch `main`, head `a06ada39c4554655607f658b81fe5d367a1bfe90` (4 commits: `09622b6` WP0, `5fd5870` WP1, `14705c3` lockfile, `a06ada3` WP2). Its remote is the private GitHub repo `datasecau/HPSM-light`, at the same SHA (the builder's PUSHED mail 22:25:58Z plus Tuesday s6's `ls-remote` at 08:25; not re-derived here). **You have no GitHub identity and you do not need one.**
- **How to reach it:** clone into your OWN `mktemp -d`: `git clone --no-hardlinks '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer' "$T/repo"`, then check out `a06ada39c4554655607f658b81fe5d367a1bfe90` **in your clone**. **Never write into `6_Policy_Composer` or its `.git`**: no fetch, no worktree add, no checkout, no `npm install` there. A builder seat may be live in that project.
- **Environment:** local Docker on this Mac only. **Non-prod by construction:** no cloud resource exists for this product. **Production? No.**
- **Shared Docker daemon:** another Datasec seat may be building images or running containers on this same daemon. **Never stop, remove or restart a container you did not start.** Run the Composer's stack under its own project name and port: `PC_COMPOSE_PROJECT=policy-composer-qa PC_EDGE_PORT=18180` (both are read by `scripts/common.sh:3-4` and `compose.yaml:86`). Bring down only your own project when you finish, with `scripts/down.sh` under the same env vars.

## 2. Spec / DoD being tested against
- **Definitions of done:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md`, section **6.1** rows WP0, WP1 and WP2, plus section **2.2** (the cardinality checks WP2 automates) and section **1.9** (item attributes).
- **Seed contract:** `.../Architecture/2026-09-10_policy-composer/2026-09-10_seed-data-CONTRACT.md`.
- **Source tree (read-only):** your clone.
- **The claims to challenge.** These come from the builder's session 33 wrap. They are inputs to falsify, not evidence:
  1. `scripts/ci.sh` is GREEN 12/12 at this head. The citation step needs the E8 SOW text from outside the repo: `PC_E8_SOW_TEXT=/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md` (the default at `scripts/ci.sh:64`, relative to the ORIGINAL repo, so set it explicitly in your clone). The builder says the text is pinned by SHA-256 `8722f8ab…`; read the pin from the repo, not from here.
  2. **Egress:** only `edge` sits on a non-internal network and only `edge` publishes a port, bound to 127.0.0.1. From api, worker, db, idp, web, objects and mail, public DNS fails and TCP to 1.1.1.1:443 and 8.8.8.8:53 fails, while db:5432 is reachable. The probe carries a control on an ordinary network, so it cannot pass blind.
  3. **Secret scan:** gitleaks, digest-pinned, run with `--network none`. The pre-commit hook (`core.hooksPath=.githooks`) refuses a commit carrying a planted key. Tree and history are clean.
  4. **RLS (WP2):** own-tenant reads only on 5 tables. Cross-tenant update and delete by id affect 0 rows. Cross-tenant insert is refused (42501). A session with no tenant sees 0 rows. A catalog guard asserts that every tenant table has RLS enabled, forced, and a policy. Mutations: `USING (true)` fails all four behavioural isolation tests, and removing 0002's `REVOKE INSERT` fails T03 and T17.
  5. **Invariants:** released-version immutability (T10–T12; released → superseded is the only permitted change), one editable version (T06), the app role lacks INSERT on policy (T17), the atomic creation function is not executable by PUBLIC, and A-28: a manifest-hash change in `in_technical_review`, `awaiting_customer` or `approved` returns the version to draft, while a same-hash rewrite keeps the state.
  6. **WP1 content:** 123 controls exactly once; 22 category counts match Appendix A; 26 questions; silent columns empty and flagged `CONTENT_PROVISIONAL` (the builder counts 1,653 flags); **zero invented severities or mappings** (all 55 severities carry a `source_ref` equal to the Preview's printed value; no ISO/NIST/SOC 2/HIPAA mappings); the content hash is reproducible (two builds equal the committed `CONTENT_HASH`).
  7. **A draft-DDL defect the builder found and fixed:** `device_capability_release`'s publish CHECK passed with NULL publishers. A test proves the draft expression passes and the fix refuses.

## 3. Scope
- **Charter sentence:** re-derive the WP0–WP2 definition-of-done claims from a clean clone at `a06ada3`, attacking the security surfaces (RLS, tenant isolation, egress, secret scanning) hardest, and look for what the builder's own tests CANNOT see.
- **In scope, and where each runs:** everything in §2 runs in YOUR clone, on the shared daemon, under your own compose project. `scripts/ci.sh`, `scripts/test-db.sh`, `scripts/egress-test.sh`, `scripts/secret-scan.sh`, `scripts/health-check.sh`, all by path.
- **The adversarial questions Tuesday wants answered, beyond re-running:**
  - **The catalog guard's PREDICATE.** How does the test define "tenant table"? Enumerate every table in the migrated schema that carries a tenant or engagement key, **directly or by FK chain**, and compare with the 5 tables the behavioural tests cover. A table outside the guard's predicate is a finding even when every test is green (learnings/2026-09-07_a-census-complete-over-a-frame-that-is-not).
  - **Mutations the builder did not run.** For example: drop `FORCE ROW LEVEL SECURITY` on one table; make the tenant GUC fall back to a default rather than NULL; grant the app role BYPASSRLS. Does something go RED? A mutation that stays green is the finding. Restore byte-identical after each one, and prove it.
  - **Does the egress probe cover every container the compose file defines?** Count the services in `compose.yaml` against the list the probe iterates.
  - **Superuser in the running stack.** The builder states RLS is NOT in force in the running stack (superuser connection, migrations not run). **Do NOT file that as a new defect.** DO measure it and state it with its evidence class, because WP4 is built on the answer.
- **Out of scope / do NOT touch:** screens (there are none yet); the .NET bridge beyond its 3 skeleton tests; any GitHub, Jira or cloud call; the HPSM analysis repository at the project root; anything under `3_Access_Keys` or `4_Credentials`; the T9 vault. **Never** push, and never write into the original repo.

## 4. Credentials (POINTER ONLY)
- None needed. The stack's local development secrets are generated or declared in the repo for local use. **Never reproduce a secret value, its prefix or its length in the report.** The OIDC mock issues no tokens (discovery and JWKS only), so no role matrix exists to exercise yet. Report that as a coverage gap, not a failure.

## 5. State-mutation & cleanup
- **Sanctioned pattern:** a throwaway database and compose project that you start and own. Tenants and rows you create live only there.
- **NEVER `rm`**, per the template's standing rule: one `mktemp -d` per attempt, abandon the old one; quarantine by move if anything must be cleared, and guard every expansion.

## 6. Output boundary (fixed)
Findings, reports and recommendations ONLY. No code, no tests, no commits, no tickets. **Evidence class on every action recommendation:** MEASURED AT RUNTIME / PROBED / READ ONLY.

## 7. Known-fragile / known-changed
- **Known and NOT new:** RLS not wired into the running stack (WP4). The idp mock issues no tokens (WP4/WP5). The bridge is a CLI skeleton (WP7). MinIO and Mailpit are checked only at their health endpoints. CI has only run on this Mac mini, because the citation test needs the gitignored SOW text.
- **Builder's own disclosed gap:** the RLS catalog guard is structural only. Mutant 2 (`USING true`) passed it, and the behavioural tests caught it. Treat this as a lead, not a closed item.
- **Recent Kam rulings that changed content defaults (do not flag the change itself):** Q-20 "always remediate High" and its reach, ruled 2026-09-11 08:18 (every remediable High item ON; high-impact ones also need the release approval; Strict applies the same High rule). WP3 executes it and WP0–WP2 do not, so **a remediation-default mismatch in WP1 content is in scope only if the content itself contradicts section 1.9.**
- **Build the schema the product deploys** (template §7): name which migrations the test database is built from, and whether the running stack would build the same schema. The builder says the stack never runs them. If two sources disagree, that is a finding; do NOT reconcile them.

## 8. Logistics
- **Time-box:** one session. If the full CI cannot run, report each leg you could not run as **NOT RUN with the blocker named**.
- **Report on disk:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-a06ada3-tier1/report.md`, with evidence beside it. **Every finding carries FOUND / TESTED / HOW** (learnings/2026-09-07_analysis-records-what-tested-and-how).
- **Head readings:** report the clone's HEAD at start, mid and end with the branch name beside each SHA. Also report the ORIGINAL repo's `main`, read with `git --no-optional-locks -C <path> rev-parse main` only.
- **You have no inbox.** You can mail but you cannot receive. Where this brief does not answer something, take the safest reading, state it in the report, and carry on. **Approval-class items (anything cloud, billable, external or irreversible) are never yours. Stop and name them.**
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer WP0-WP2 @ a06ada3 (tier 1)`. Lead with GO / GO WITH FINDINGS / NO GO, then the report path, then the findings BLUF. **Datasec's coordinator is TUESDAY; never mail `wednesday-agent@`.**

PROVENANCE:
- claims 1-7, the NOT-TESTED list and the builder's disclosed gaps | datasec-hpsm session 33 wrap mail to tuesday-agent@, 2026-09-10T12:13:04Z, spf/dkim/dmarc pass | read 2026-09-11
- head a06ada3 and the 4-commit history on local main | git --no-optional-locks -C 6_Policy_Composer log/rev-parse, run by Tuesday | read 2026-09-11
- remote HPSM-light main == a06ada3 | datasec-hpsm PUSHED mail 2026-09-10T22:25:58Z and Tuesday s6 ls-remote 08:25:05 (pickup) | read 2026-09-11
- WP0-WP2 definitions of done and section numbers | ARCHITECTURE.md section 6.1 rows, read by Tuesday | read 2026-09-11
- PC_COMPOSE_PROJECT / PC_EDGE_PORT overridable | 6_Policy_Composer/scripts/common.sh:3-4 and compose.yaml:86 | read 2026-09-11
- SOW text default path | 6_Policy_Composer/scripts/ci.sh:64 | read 2026-09-11
- Q-20 reach ruling and the Strict reading | decision_queue.sh show hpsm-composer-remediate-high-reach; ARCHITECTURE.md section 1.9 lines 382-392 | read 2026-09-11
- no containers running at commission time | docker ps (empty) by Tuesday | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 08:37
