# KS board triage, part B2 (97 open HIGH tickets), 2026-11-02

Method: Linear GraphQL (description + newest 3 comments), own scratch clone repo_b2 of origin/develop, deploy test = merge-base --is-ancestor against b1fb543640e7 (kintsugi). GitHub PR API was unavailable (no gh login), so PR state is inferred from develop squash subjects/bodies; "UNVERIFIED" marks the gaps. Bucket = one per ticket.

key | board state | bucket | evidence | next action | size
--- | --- | --- | --- | --- | ---
KS-771 | In Progress | DONE-NOT-CLOSED | #798 merged e7cfe4b5 (deployed y); Peter 2026-10-22 approved block #842-#848, no item fails; newest comment 2026-10-22 | Close ticket (review stream accepted) | -
KS-775 | In Progress | DONE-NOT-CLOSED | #798,#801,#1036 merged (all deployed y); 09-17 qs rows fixed in range on express 4; express 5 migration ruled 09-03 unchanged (KS-763); newest comment 2026-09-17 | Close; express 5 migration tracked separately | -
KS-801 | In Progress | DONE-NOT-CLOSED | #817 merged 0f6854cc, #1459 merged 672352369b (squash, deployed y, ancestor of b1fb543640e7); 10-12 stays open pending deploy verify; newest comment 2026-10-12 | Deploy-verify on kintsugi then close | -
KS-806 | In Review | DONE-NOT-CLOSED | #1476 merged efc84906 (deployed y); 10-12 "stays OPEN: nothing is deployed" (now an ancestor of b1fb543640e7); follow-ups KS-1486/KS-1498 filed; newest comment 2026-10-12 | Verify on kintsugi, close | -
KS-869 | In Progress | NEEDS-KAM | #854 merged 50913d2c3, #880 merged 7d7f6bd5 (deployed y); 09-08 was waiting on Kam: merging #880 picks Option 1 for Platform S (Stuart-facing contractual choice) and removes key overlap KS-843 grace ruling relied on; newest comment 2026-09-08 | Confirm Kam accepts the Option 1 consequence in hindsight; then close or re-scope with KS-889 (re-mint path) | -
KS-932 | In Progress | DONE-NOT-CLOSED | #1004 merged 40fe4db6 (deployed y); live sweep of hung-DNS in a container owed (batched in a Sunday QA pass); newest comment 2026-09-16 | Run the live DNS sweep on a local slot, then close | S
KS-937 | In Progress | AGENT-BUILDABLE | #876,#874 merged (deployed y); 40ed3573 (10-10, deployed y) landed F-A plus relative dest and uid-0 group; #1444 head is a merge-develop commit, not on develop (UNVERIFIED: no GitHub API); 09-13 residue F-B/F-F open then; newest comment 2026-09-13 | Re-measure checklist F-A..F-F at develop, finish what is left or close | S
KS-962 | In Progress | DONE-NOT-CLOSED | #973 merged 81800225 (deployed y); closes only when a deploy seat verifies secuuraadmin rolbypassrls on a deployed box (ruling 09-13); newest comment 2026-09-13 | Deploy seat runs the rolbypassrls check on kintsugi, then close | S
KS-966 | In Progress | DONE-NOT-CLOSED | #888 merged 3af1d37b (deployed y); items 3 and 4 stood down against KS-969 (09-07); Peter 09-11 consequence note recorded in docs; newest comment 2026-09-11 | Close (items done or moved) | -
KS-968 | In Review | NEEDS-KAM | #1485 merged 8f674b3c, #1800 merged 92a02a35, #905 (all deployed y); DEPLOY NOTE 10-12: first boot in both-rows state without ADMIN_USER_PASSWORD SUSPENDS the account holding admin@secuura.com; which outcome each environment gets is Kam's choice; newest comment 2026-10-12 | Kam picks per-environment outcome; deploy seat checks read-only state first | -
KS-974 | In Progress | DONE-NOT-CLOSED | #1198 merged a314a9bc (deployed y); Kam ruled 09-22 option a: leave both routes as designed, record corrected; newest comment 2026-09-25 | Close | -
KS-998 | In Review | DONE-NOT-CLOSED | #1530/#1729 (1b550684), #1532, #1540, #1553, #1545 (= 0662f721 item 3) merged, all deployed y; #1407 merged 7bcc2ed5; #1422/#1442 not on develop (UNVERIFIED: docs/merge-only heads); 10-13 last seat comment; newest comment 2026-10-13 | Verify item 4 on develop, then close | S
KS-1012 | Backlog | NEEDS-KAM | No PR; ruleset require-pr-gates (7 dead required checks, 0 approvals, admin bypass ALWAYS) on develop and main; 0 comments | Kam decides the branch-protection policy; then a GitHub-admin change (not a seat job) | -
KS-1038 | Backlog | AGENT-BUILDABLE | No PR; auth-exhaustive races its own lockout (4 redis lockout keys per run); measured; 0 comments | Serialize the spec / isolate lockout keys; description briefable | M
KS-1051 | Backlog | AGENT-BUILDABLE | No PR; develop RED on services/originate jest (2 of 4 cells in ks444 test) and no gate runs it; KS-826 carried in 09-14; newest comment 2026-09-14 | Fix the two cells, wire suite into a blocking gate; briefable | M
KS-1055 | Backlog | AGENT-BUILDABLE | No PR; per-tenant DBs never receive file migrations, FORCE RLS with zero policies (measured); only active under multi-tenancy; related KS-1235 | Run file migrations on tenant DB provisioning; briefable but design-sensitive | L
KS-1080 | Backlog | AGENT-BUILDABLE | No PR; akto-autoheal runs root with docker.sock RW (local test stack); 09-10 note: Peter high-risk class (systemTest gate logic); newest comment 2026-09-10 | Drop root / socket-proxy; Peter reviews; briefable | S
KS-1100 | Backlog | AGENT-BUILDABLE | No PR; kintsugi deploy 4554b25e2 carried 4 changes with no QA gate record (#872,#896,#728,#808); 09-12 qa-login created on kintsugi; newest comment 2026-09-12 | Run the four retro QA gates; briefable | M
KS-1107 | Backlog | AGENT-BUILDABLE | No PR; POST /api/auth/register accepts client-supplied organizationId with no check; impact not traced | Trace impact then bind to caller; briefable | M
KS-1148 | Backlog | AGENT-BUILDABLE | No PR; CI jobs run without install/build (audit:contract, ks949 seed idempotence); recurrence 10-09 x3; note KS-638 says GH Actions retired (UNVERIFIED which jobs still run); newest comment 2026-10-09 | Confirm where these jobs run now, add install/build steps | S
KS-1149 | Backlog | AGENT-BUILDABLE | No PR; launcher outside repo edited 09-14 (keepalive); 10-26 measured 364 s idle cutoff and rc 141, keepalive test results; newest comment 2026-10-26 | Confirm launcher keepalive holds on a >6 min push; document or close | S
KS-1184 | Backlog | AGENT-BUILDABLE | No PR; workflow-approve persists before forward so a refused forward strands the instance (KS-1087 gate F2); 09-16 record from gate on #1010; newest comment 2026-09-16 | Persist after forward / add re-forward path; design note in ticket | M
KS-1214 | Backlog | AGENT-BUILDABLE | No PR; mcp-server POST /hash (and /verify, /verify-batch per 10-31) read caller-supplied filePath with no auth; 11-01 gate 82 still sees 500 echo; newest comment 2026-11-01 | Remove/gate filePath; measure deployed exposure read-only first; briefable | M
KS-1235 | Backlog | AGENT-BUILDABLE | No PR; auth tenant-pool statements carry no tenant GUC under fail-closed RLS (multi-tenancy flag); 0 comments | Set tenant GUC in tenantManager path; related KS-1055 | M
KS-1280 | Backlog | AGENT-BUILDABLE | No PR; /api/certifications/:id/verify forwards a revoked session Bearer (gateway session check never runs); measured in-process | Mount authenticateToken on route; briefable | S
KS-1372 | Todo | AGENT-BUILDABLE | No PR; gateway failed-login lockout inert: recordFailure never called | Wire recordFailure into login failure path | M
KS-1376 | Backlog | AGENT-BUILDABLE | No PR; certifications ends RLS FORCE with no tenant_isolation policy on fresh DB (gate39 N-G39-1 Major) | Add policy migration; briefable | M
KS-1379 | Backlog | AGENT-BUILDABLE | No PR; PR #1339 locks re-resolved from bare manifests (~1000 non-target moves); 09-29 gate42 checklist item added; newest comment 2026-09-29 | Re-resolve locks minimally per package; briefable | L
KS-1383 | Backlog | AGENT-BUILDABLE | No PR; revoked credential resubmitted with another live id verifies true; 10-12 priority raised to High on Wednesday's ruling; bypass where NODE_ENV not production; newest comment 2026-10-12 | Bind verify to the proof; related KS-1375 (started) | M
KS-1390 | Todo | AGENT-BUILDABLE | No PR; e2e-v2 (24 specs, 222 tests) wired into no gate; Peter 09-29 six extra findings; newest comment 2026-09-29 | Wire into gate inventory/pre-push; scope after Peter comment | L
KS-1429 | Backlog | BLOCKED | #1403 merged fa690e5a (harness, deployed y); test waits on KS-692 bind-creator half (KS-692 started); newest comment 2026-10-06 | Wait for KS-692; then add the test | -
KS-1430 | Backlog | BLOCKED | #1403 merged fa690e5a (deployed y); waits on KS-577 revoke-on-rotate (KS-577 started); newest comment 2026-10-06 | Wait for KS-577; then add the test | -
KS-1483 | Backlog | STALE/DUPLICATE | No PR; folded into KS-998 item 2 (#1540 merged 405e33a1); 10-19 comment: hook now refuses the push, ticket BLUF stale; newest comment 2026-10-19 | Close as superseded by KS-998 | -
KS-1486 | Backlog | AGENT-BUILDABLE | No PR; two simultaneous first wallet logins issue a token for an id not in DB (4 of 5 rounds); filed from #1476 gate | Make wallet create idempotent (upsert/returning); briefable | M
KS-1498 | Backlog | AGENT-BUILDABLE | No PR; suspended mixed-case wallet account evaded by lower-case login; needs case-insensitive lookup plus migration | Normalise lookup plus migration (do not deploy w/o review) | M
KS-1516 | Backlog | NEEDS-KAM | No PR; opentimestamps/blockchain timestamps report verified true; /verify accepts forged proof; ACTION says policy decision first (KS-753 gate m2) | Kam/policy: what an unverified timestamp may claim; then build | -
KS-1535 | Backlog | AGENT-BUILDABLE | No PR; Kam ruled 10-12: leave ADMIN unbounded for now, change before deployment; newest comment 2026-10-12 | Bound ADMIN by organisation before deploy; briefable | M
KS-1574 | Backlog | AGENT-BUILDABLE | No PR; GET /api/keys has no organisation arm (facts only for builder, 10-13); build on normaliseOrgId equality; newest comment 2026-10-13 | Add org bound to list; briefable | S
KS-1640 | Backlog | AGENT-BUILDABLE | No PR; chain-first verify blobs hard-code anchored:true, drop status/acknowledged (v1+v2) | Pass through anchoring status; briefable | M
KS-1646 | Backlog | AGENT-BUILDABLE | No PR; fresh clone has core.hooksPath unset so pre-push preflight silently does not run | Auto-set hooksPath (postinstall/doctor); briefable | S
KS-1688 | Backlog | BLOCKED | No PR; /api/documents/:id/version lacks per-document access check; Stuart 10-19/20 answered S only versions own docs; Kam 10-20: fix must come SECOND after KS-1557 (started); newest comment 2026-10-20 | Land KS-1557 first, then build this | M
KS-1690 | Backlog | AGENT-BUILDABLE | No PR; OAuth refresh_token grant ignores origin session; 10-20 gate BS1 confirmed scoping with two conditions (in comment); newest comment 2026-10-20 | Check session in refresh grant; briefable | M
KS-1696 | Backlog | AGENT-BUILDABLE | No PR; GET /api/gdpr/deletion-log without userId reads all tenants; Stuart 10-20: S never reads it; newest comment 2026-10-20 | Require userId / tenant bound; briefable | S
KS-1699 | Backlog | AGENT-BUILDABLE | No PR; certifications /:id/verify,/share,/recertify lack per-record access check; Stuart 10-20: S never calls them; newest comment 2026-10-20 | Add per-record check; briefable | M
KS-1739 | Backlog | AGENT-BUILDABLE | No PR; Node 26 breaks sync cbor.encode on host test runs (images pin node 24) | Pin host node/ switch to async encode in tests | S
KS-1740 | Backlog | AGENT-BUILDABLE | No PR; no supported way to put a user in a second tenant on local stack; blocks KS-1741 | Add supported provisioning route/script; briefable | M
KS-1741 | Backlog | BLOCKED | No PR; assignee Peter; paused 10-27 parked until KS-1740 lands (KS-1740 backlog); newest comment 2026-10-27 | Wait for KS-1740 | -
KS-1819 | Backlog | AGENT-BUILDABLE | No PR; thread-mint spends platform wallet outside withWalletLock, no role check (fee drain) | Add role check + withWalletLock; briefable | M
KS-1820 | Backlog | AGENT-BUILDABLE | No PR; nft-certificate shares the platform wallet mnemonic, /api/nft/mint has no role check | Role check now; separate wallet is a config decision | M
KS-1821 | Backlog | AGENT-BUILDABLE | No PR; in-lock confirmed write omits transactionHash (inferred from code, not reproduced) | Reproduce then fix; briefable | S
KS-1831 | Backlog | AGENT-BUILDABLE | No PR; documents/:id/sign: any tenant user, revoked to signed, no signature check; 10-30 wider (documents:read connector key reaches it); interacts with KS-1814; newest comment 2026-10-30 | Add authz and terminal-state guard; briefable | M
KS-1833 | Backlog | AGENT-BUILDABLE | No PR; lifecycle-events route: any tenant user records event and triggers anchor emission | Add authz; same family as KS-1831 | M
KS-1855 | Backlog | AGENT-BUILDABLE | No PR; gateway answers four admin/verify routes from fabricated stand-ins before proxy | Remove/guard stand-ins by env | S
KS-188 | Todo | AGENT-BUILDABLE | No PR; assignee Stuart; 0 of 613 OpenAPI links covered; Peter measurement notes 09-18 to 10-07; newest comment 2026-10-07 | Declare links + operationId; spec work, large | L
KS-1890 | Backlog | AGENT-BUILDABLE | No PR; tenant-provisioning checks no role on any route (reachable directly, not via gateway) | Add role middleware; briefable | M
KS-1931 | Backlog | AGENT-BUILDABLE | No PR; kyc dbGetVerificationsByUser returns [] on error so GDPR erasure continues; 11-01 gate 85 (PR 1900) adds two more points; newest comment 2026-11-01 | Throw instead of [] plus the two added points; briefable | M
KS-1933 | Todo | AGENT-BUILDABLE | No PR; QA gate 95 (11-02): one Stripe purchase credited more than once (3 ways + 2 catches). Wednesday staged briefs today (seatF22_billing_credit_once, answer_F22_design): likely already in flight | Confirm seat F 22nd owns it; do not double-brief | M
KS-1935 | Todo | AGENT-BUILDABLE | No PR; addCertificationCredits optimistic lock not a compare-and-set (Stripe update unconditional); same billing seat as KS-1933 | Fold into the KS-1933 build | S
KS-1936 | Todo | AGENT-BUILDABLE | No PR; PATCH admin/identity/users/:id/level reachable by ORG_ADMIN/ISSUER_ADMIN; tenant bound unmeasured | Measure bound then restrict role; briefable | S
KS-239 | Backlog | NEEDS-CLIENT | No PR; decision for Stuart (erasure completeness incl. backups); 08-12: crypto-shred mechanism does not exist, gated on KS-291; newest comment 2026-08-12 | Stuart sign-off; nothing for a seat | -
KS-304 | Backlog | NEEDS-CLIENT | #297 merged 0dacbdb1 (docs only); Kam ruled 09-02: tell Stuart S goes first; newest comment 2026-09-02 | Wait for Platform S tokenisation; chase Stuart | -
KS-329 | Backlog | BLOCKED | No PR; blocked by KS-756 (backlog) per 09-02 split; ruling (a) already made; newest comment 2026-09-02 | Build KS-756 first | -
KS-485 | Todo | STALE/DUPLICATE | Hub/tracker (100 comments), 10-29 comments are deploy reports for develop e3d8456ec81d on both boxes; related KS-1814 etc.; newest comment 2026-10-29 | Not a work item: keep as register, drop priority or close with Kam | -
KS-491 | Todo | NEEDS-KAM | No PR; edge/WAF register; F-9 resolved 08-17; remaining WAF, Postgres/Redis, CAPTCHA rows and Peter's LOW Server:nginx finding (KS-1397); newest comment 2026-09-30 | Kam: WAF/CAPTCHA product and spend decisions | -
KS-525 | Backlog | AGENT-BUILDABLE | No PR; assignee Peter; 10-26 re-grounding: nothing started, Phase 0 helpers absent; 23 flows over 310 ops; newest comment 2026-07-25 | Break into phases; briefable after Phase 0 | L
KS-565 | Backlog | AGENT-BUILDABLE | #1403,#757,#756 merged (deployed y); Peter 10-09/10-21 more recurrences incl. POST /api/documents 500 on title >500; newest comment 2026-10-21 | Fix remaining genuine 500s/schema drift in batches | L
KS-576 | Todo | BLOCKED | No PR; must not ship before KS-577 (started); Stuart 09-02 proposes grant-driven re-key (PS-740); newest comment 2026-09-02 | Wait for KS-577; align with PS-740 | -
KS-590 | Backlog | NEEDS-KAM | No PR; Peter 10-06: four disclosure questions need Kamil's answer (verify-by-hash cross-tenant field disclosure); newest comment 2026-10-06 | Kam answers disclosure questions | -
KS-598 | Todo | AGENT-BUILDABLE | No PR; MULTI_TENANCY registry upsert collapses registrations per (hash,tenant); confirmed live 09-02; newest comment 2026-09-02 | Migration + ON CONFLICT change; briefable | M
KS-602 | Backlog | NEEDS-KAM | No PR; BM-1 certification model (business-model definition); 0 comments | Product ruling needed before any build | -
KS-603 | Backlog | NEEDS-KAM | No PR; BM-2 verification as configurable workflow via smart contracts; 0 comments | Product ruling needed | -
KS-607 | Backlog | STALE/DUPLICATE | No PR; blocks KS-608 (completed); 08-12 Kam answered Peter: same lifecycle fact, different resolution scope; newest comment 2026-08-12 | Close if KS-608 shipped the invariant (UNVERIFIED not checked here) | -
KS-61 | Todo | AGENT-BUILDABLE | No PR; assignee Stuart; "reminder ticket, per-API as touched"; Peter 06-03 compliance improved, 09-14 sweep gaps; newest comment 2026-09-14 | Park or batch spec description gaps | L
KS-624 | Backlog | NEEDS-KAM | No PR; prism issues VCs with random-byte proof (fraud-grade, A-11 pattern); 08-13 third instance remediated; awaits Kam's ruling covering instances; newest comment 2026-08-13 | Kam rules on prism (remove vs fix) | -
KS-636 | Backlog | AGENT-BUILDABLE | No PR; node:24-alpine CRITICAL CVE-2026-59873 (08-01); 08-15 evidence of Kintsugi rebuild only; newest comment 2026-08-15 | Re-scan current base image; bump/rebuild if still present | S
KS-638 | Backlog | STALE/DUPLICATE | No PR; extranet test board 0 passed in 22; 09-07 GitHub Actions retired (100% startup_failure) so premise moved; newest comment 2026-09-07 | Rescope or close; superseded by Actions retirement | -
KS-655 | Backlog | NEEDS-KAM | No PR; KS-78 drift check wrong 3 ways; 09-02 BOUNCE: change is Kam's call, fleet-wide fix on WED board; newest comment 2026-09-02 | Kam go-ahead for the fleet-wide fix | -
KS-668 | Backlog | AGENT-BUILDABLE | No PR; compose forwarding of ADMIN_USER_PASSWORD landed with #896 (per Peter 09-10); *123 defaults / 11 rotation vars still unconfirmed; newest comment 2026-09-10 | Re-measure on develop, finish remaining half | M
KS-678 | Backlog | AGENT-BUILDABLE | No PR; 08-21 comment says fixed and pushed but 09-05 reconciled: never started, no PR or remote branch; 17 secuura.io URLs in published spec; newest comment 2026-09-05 | Redo fix (generator + sources); domain ownership may need Kam | M
KS-683 | Todo | DONE-NOT-CLOSED | No K-side PR; Platform-S PR #581 (PS-644) merged; 08-21 Kam confirmed at demo: repoll loop gone; newest comment 2026-08-21 | Close (K labelling already honest per KS-587) | -
KS-696 | Todo | AGENT-BUILDABLE | No PR; Akto pr-scan non-deterministic; 08-27 six-run table; Peter 09-28 suggests a mechanism; newest comment 2026-09-28 | Chase mechanism from Peter note; briefable | M
KS-709 | Backlog | AGENT-BUILDABLE | 4f7766a3 (KS-1286 Akto bump, deployed y) partial; Peter 10-15 ruled Option A, 10-27 four scans execute nothing and report headline still PASSED; newest comment 2026-10-27 | Make report headline fail on zero-execution; fix the four scans | M
KS-716 | Todo | AGENT-BUILDABLE | No PR; super-admin surface unscanned (no system_admin block); Peter 09-30 fallback works when issuer token dead; newest comment 2026-09-30 | Provision system_admin block / fallback; briefable | S
KS-725 | Todo | AGENT-BUILDABLE | No PR; test:pr never re-imports OpenAPI; 08-31 measured re-import exposes fields; Peter 09-28 reverified; newest comment 2026-09-28 | Add re-import step to test:pr | S
KS-735 | Todo | NEEDS-CLIENT | No PR; 09-02 BOUNCE: contract question (flat vs nested) is Peter's call; PS-723 Stuart ruled direction; newest comment 2026-09-02 | Peter answers contract question | -
KS-756 | Backlog | AGENT-BUILDABLE | No PR; createSession mints opaque refresh token, nothing reads it; KS-329 ruling (a) prerequisite; blocks KS-329 | Wire refresh read path; auth security change | L
KS-768 | Backlog | DONE-NOT-CLOSED | Delivered in PR #796 (9ca2636e on develop, deployed y) per 09-03 comment; ticket still Backlog; newest comment 2026-09-03 | Close | -
KS-770 | Todo | STALE/DUPLICATE | Review-stream tracker for Peter (19 tickets); latest comments 09-28; newest comment 2026-09-28 | Tracker: close when streams done, priority drop | -
KS-772 | Todo | STALE/DUPLICATE | Review-stream tracker for Stuart (20 tickets); 10-29 comments are deploy reports; newest comment 2026-10-29 | Tracker: close when stream done | -
KS-787 | Backlog | AGENT-BUILDABLE | No PR; K cannot tell S revokes without lifecycle event; depends on what S emits | Add K-side classification; may need Stuart (S emits) | M
KS-889 | Backlog | NEEDS-KAM | No PR; 09-06 measured: backfill impossible, only 5 of 32 active keys recoverable; re-mint is the only path; KS-843 cutover evidence; newest comment 2026-09-06 | Kam: re-mint vs accept; Stuart-facing | -
KS-939 | Backlog | AGENT-BUILDABLE | No PR; launcher boot prompt asserted by no cell; launcher lives outside repo (Blockchain/Launch_Claude.command); newest comment 2026-09-06 | Add boot-prompt assertion cell; briefable | M
KS-951 | Backlog | AGENT-BUILDABLE | No PR; default-password CI gate catches one shape, 4 of 5 canaries pass | Extend gate and canaries; briefable | M
KS-967 | Backlog | AGENT-BUILDABLE | No PR; both credential guards blind to .env.example values | Fix scan roots/exclusions; briefable | M
KS-987 | Backlog | AGENT-BUILDABLE | No PR; rsync breaks bind mount by inode so stale OpenAPI spec ships; KS-1021 duplicate merged in; related KS-1823; newest comment 2026-09-14 | Runbook restart step plus gate check | M
KS-995 | Backlog | AGENT-BUILDABLE | No PR; Linear issueArchive cascades to sub-issues incl. non-terminal | Add pre-archive guard to board scripts | S
KS-996 | Backlog | AGENT-BUILDABLE | No PR; 95 archived tickets in non-terminal states; measure whether a cascade did it | Read-only measurement; restoration needs Kam | S

## Counts per bucket

- DONE-NOT-CLOSED: 11
- PR-OPEN: 0
- AGENT-BUILDABLE: 60
- NEEDS-KAM: 11
- NEEDS-CLIENT: 3
- BLOCKED: 6
- STALE/DUPLICATE: 6
- Total: 97

## Agent-buildable seat-hours (S=0.5, M=2, L=5): 117.0

Note: KS-1933/KS-1935 (2.5 h) appear already in flight with seat F 22nd; KS-525 and KS-188 are really multi-session (L is a floor).

## NEEDS-KAM

- KS-869: Confirm Kam accepts the Option 1 consequence in hindsight; then close or re-scope with KS-889 (re-mint path) (#854 merged 50913d2c3, #880 merged 7d7f6bd5 (deployed y); 09-08 was waiting on Kam: merging #880 picks Option )
- KS-968: Kam picks per-environment outcome; deploy seat checks read-only state first (#1485 merged 8f674b3c, #1800 merged 92a02a35, #905 (all deployed y); DEPLOY NOTE 10-12: first boot in both-row)
- KS-1012: Kam decides the branch-protection policy; then a GitHub-admin change (not a seat job) (No PR; ruleset require-pr-gates (7 dead required checks, 0 approvals, admin bypass ALWAYS) on develop and main)
- KS-1516: Kam/policy: what an unverified timestamp may claim; then build (No PR; opentimestamps/blockchain timestamps report verified true; /verify accepts forged proof; ACTION says po)
- KS-491: Kam: WAF/CAPTCHA product and spend decisions (No PR; edge/WAF register; F-9 resolved 08-17; remaining WAF, Postgres/Redis, CAPTCHA rows and Peter's LOW Serv)
- KS-590: Kam answers disclosure questions (No PR; Peter 10-06: four disclosure questions need Kamil's answer (verify-by-hash cross-tenant field disclosur)
- KS-602: Product ruling needed before any build (No PR; BM-1 certification model (business-model definition); 0 comments)
- KS-603: Product ruling needed (No PR; BM-2 verification as configurable workflow via smart contracts; 0 comments)
- KS-624: Kam rules on prism (remove vs fix) (No PR; prism issues VCs with random-byte proof (fraud-grade, A-11 pattern); 08-13 third instance remediated; a)
- KS-655: Kam go-ahead for the fleet-wide fix (No PR; KS-78 drift check wrong 3 ways; 09-02 BOUNCE: change is Kam's call, fleet-wide fix on WED board)
- KS-889: Kam: re-mint vs accept; Stuart-facing (No PR; 09-06 measured: backfill impossible, only 5 of 32 active keys recoverable; re-mint is the only path; KS)
