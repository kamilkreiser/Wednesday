# Platform K — open tickets by category (2026-09-02)

## BLUF

- **211 open KS tickets** (non-archived, state not in Done / Canceled / Duplicate / Deployed To Prod), read 2026-09-02T06:40:38Z from the Linear KS board with full pagination.
- **Category 1 — in our hands, ready to action: 124** · **Category 2 — requires input: 48** · **Category 3 — done on our side, awaiting approval: 39**.
- Full four-suite SET evidenced in Linear on **11** tickets overall (7 of the 39 in category 3); PARTIAL 9 · NONE 15 · UNKNOWN 23 · n/a (no PR) 153. Peter's approval is evidenced on 15 of the 39 category-3 tickets.
- Notice: (a) the category-3 queue is large — 39 tickets sit merged-or-PR'd waiting on Peter's review, a deploy sign-off or a close; (b) most PRs raised while GitHub Actions was dead carry **no four-suite run** (only the 7/7 push preflight) — the SET rule only began 2026-08-27 (KS-685); (c) KS-695 is the one ticket where **Stuart is waiting on us**.

## Recommendation

Work category 3 first as a batch: merge the two Peter-approved PRs still unmerged (#764 KS-726, #738 KS-635), take a deploy decision on the merged-not-deployed set (KS-703/705/643/667/728 and the five Tested-Not-Deployed tickets), and ask Peter for the 10 outstanding reviews in one message. Then pick up KS-695 (Stuart is blocked on it) and the sized-and-ready security items (KS-593, KS-591, KS-578, KS-739) from category 1. Category 2 needs 19 rulings from Kam — those are listed in the "Waiting on" column.

## 1. In our hands — ready to action (124)

| Ticket | Title | Pri | State | Assignee | Suites (four) | Peter | Last activity | Note |
|---|---|---|---|---|---|---|---|---|
| KS-486 | Review A — AuthN / AuthZ / tenancy & IDOR | P1 | In Review | Kam/kksecura | PARTIAL (Schemathesis·Akto·Playwright) | n/a | 2026-08-29 | Review A register — ours; split-out rows are separate tickets |
| KS-670 | Demo's on-chain verification has been down for 6 days — Blo… | P1 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-31 | Quota recovered (Kam upgraded); verify anchoring recovered, then close |
| KS-708 | Security: Akto ADD_USER_ID (BOLA, HIGH) on GET /api/platfor… | P1 | Backlog | — | n/a (no PR) | n/a | 2026-08-29 | Kam ruled Option B 2026-08-29; build it |
| KS-169 | [Tracker] 2026-05-29 security review — findings + remediati… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-14 | — |
| KS-229 | [Tracker] 2026-06-10 platform assurance review — gap-analys… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-07-14 | — |
| KS-256 | Add OpenAPI inline examples to all 329 operations — elimina… | P2 | In Review | Kam/kksecura | FULL 2026-08-19 on old head; NOT run on custody rebase | n/a (Peter is author) | 2026-09-01 | Kam lifted the #568 hold 2026-09-02 (merge on a clean suite set); ours to run the four suites on the landing tree and merge |
| KS-304 | Tokenise personal/identifying data — mint a privacy token (… | P2 | Backlog | Kam/kksecura | UNKNOWN | NOT YET | 2026-07-14 | — |
| KS-329 | Phase 2 — JWT RS256 → hybrid (RS256 + ML-DSA-65) | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-12 | — |
| KS-365 | Base-image refresh routine + track postgres CVE-2025-68121… | P2 | Backlog | Kam/kksecura | UNKNOWN | NOT YET | 2026-08-14 | — |
| KS-485 | Security review — plan, methodology & handover (Platform K) | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-28 | — |
| KS-487 | Review B — Input validation, injection, upload, XSS/SSRF &… | P2 | In Progress | Kam/kksecura | FULL 2026-08-13 (CI fan-out on #683); #720 pending | CHANGES REQUESTED 08-31 (#720) | 2026-09-01 | Review B — Peter requested 5 changes on #720; ours to action |
| KS-491 | Review F — Edge, WAF, DDoS & anti-automation | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-18 | Remediated in code; live-edge verification not established |
| KS-565 | Sweeps 2026-08-05: untracked failures across 10 ops — respo… | P2 | Backlog | Kam/kksecura | n/a (no PR of its own) | n/a | 2026-09-01 | Sized L 09-01; not started |
| KS-591 | positive_data_acceptance recurs at scale — 734 failures acr… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | Sized M 09-01; not started |
| KS-593 | not_a_server_error recurs — 17 raw 5xx across 8 ops (KS-431… | P2 | Backlog | Kam/kksecura | n/a (no PR of its own) | n/a | 2026-09-01 | Approach note ready; audit gate (#780) merged 09-01 23:18Z so pushes are unblocked |
| KS-597 | Architecture P1: populate issuer_organization_id at registr… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-09 | — |
| KS-598 | Architecture P1: defuse the MULTI_TENANCY registry upsert —… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-09 | — |
| KS-601 | [Infra] New Platform K dev server "Kintsugi" — restore dev/… | P2 | In Progress | Kam/kksecura | UNKNOWN | n/a | 2026-08-21 | Kintsugi in progress; §4 closed, name ratified |
| KS-602 | BM-1: Certification model — certification = attestation + s… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-11 | — |
| KS-603 | BM-2: Verification is a configurable workflow via smart con… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-11 | — |
| KS-607 | GET /api/anchors/{id} and verify report different statuses… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-31 | Peter's gating question answered 08-12; investigation is ours |
| KS-618 | Client IP is invisible platform-wide on demo: every IP-keye… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-13 | — |
| KS-628 | CI: Performance suite fails on GHCR secondary rate limit wi… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-17 | — |
| KS-637 | Nightly Internal Audit has failed 40 runs straight — DAST,… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-638 | The extranet test board has never shown a green run — 0 pas… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-642 | Security: GET /api/keys enumerates another tenant's API key… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-26 | Likely superseded by KS-742 (deployed to UAT) — verify and close or re-scope |
| KS-644 | Security: /api/events — ANY authenticated user reads every… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-16 | — |
| KS-655 | KS-78 drift check is wrong three ways — reports 7 commits o… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-17 | — |
| KS-663 | The OpenAPI spec is now a consumed contract, but nothing in… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-29 | — |
| KS-668 | Compose seeds published *123 credentials by default, and th… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-24 | — |
| KS-669 | Published spec points integrators at 18 URLs on domains we… | P2 | In Progress | — | UNKNOWN | n/a | 2026-08-21 | #725 merged; E1 rule gap + owner still open (17 URLs moved to KS-678) |
| KS-676 | Two host scripts use bash 4 syntax and cannot run on macOS… | P2 | In Review | Kam/kksecura | NONE (preflight 7/7 only) | REVIEWED, no formal approval | 2026-08-21 | Peter: 'merge yours when you're happy' — merge is our action |
| KS-677 | check-spec-examples is blind to path-parameter and scalar-p… | P2 | In Progress | Kam/kksecura | n/a (no PR — rides #568) | n/a | 2026-09-01 | Fixed and pushed; new reproducible red (9→49) still ours |
| KS-683 | Anchor-status standoff: a consumer repolls anchors K report… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-31 | Stuart's layer 1 confirmed; K-side layers 3/4 remain |
| KS-687 | Akto slot targeting: dump-result-fields.sh resolves the un-… | P2 | In Progress | Kam/kksecura | UNKNOWN | APPROVED 08-27 (#732) | 2026-08-28 | #732 merged (F1); F2 half open and now unblocked |
| KS-692 | Security: /api/status revoke/unrevoke has no tenant ownersh… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-693 | M365 routes answer 503 when ENTRA_* is unconfigured — 9 per… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-695 | S↔K (K-side): erasure by external_ref, documents.title cove… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | Stuart's side is finished and waiting on THIS ticket; design note + sizes posted 09-01 |
| KS-696 | Akto pr-scan is non-deterministic — three runs on near-iden… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-29 | — |
| KS-698 | Security: one request permanently poisons any rate-limit ke… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-27 | — |
| KS-707 | Playwright quality:static is RED again — .prettierignore na… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-28 | — |
| KS-709 | Akto reports a PASS for a test that executed NOTHING — 'cle… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-29 | — |
| KS-716 | The whole super-admin surface is silently unscanned — no sy… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-29 | — |
| KS-720 | POST /api/auth/wallet/link and DELETE /unlink can never suc… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-31 | — |
| KS-722 | Security: social sign-in never verifies the OAuth `state`,… | P2 | Todo | — | n/a (no PR) | n/a | 2026-08-29 | — |
| KS-723 | Declare the remaining ~157 routed-but-undocumented /api ope… | P2 | Todo | — | n/a (no PR) | n/a | 2026-08-29 | — |
| KS-724 | A scan that logs in more than ten times as one user revokes… | P2 | Todo | — | n/a (no PR) | n/a | 2026-08-29 | — |
| KS-725 | test:pr never re-imports the OpenAPI spec, so Akto scans a… | P2 | Todo | — | n/a (no PR) | n/a | 2026-08-31 | — |
| KS-729 | Upgrade ip-address off GHSA-mwp4-54f8-5fhr (high, SSRF) — e… | P2 | Todo | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-730 | Security: 71 inline handlers still return err.message verba… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-31 | — |
| KS-731 | Local slots share one Postgres/Redis credential pair — any… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-732 | Security: POST /api/auth/mfa/disable never verifies the pas… | P2 | Todo | — | n/a (no PR) | n/a | 2026-08-31 | — |
| KS-733 | /api/users/me/mfa/* is unthrottled — the same TOTP surface… | P2 | Todo | — | n/a (no PR) | n/a | 2026-08-31 | — |
| KS-734 | The e2e Playwright suite cannot run from a clean checkout —… | P2 | Todo | — | n/a (no PR) | n/a | 2026-08-31 | — |
| KS-735 | Verify results show the user nothing about what was registe… | P2 | Todo | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-737 | Platform-admin login skips MFA entirely when mfaCode is omi… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-739 | transfer-custody maps a 401/403 from users/lookup to 502 BA… | P2 | Todo | — | n/a (no PR) | n/a | 2026-09-01 | Ruling received: build the 401/403 mapping fix; role/scope half stays with Kam |
| KS-130 | Outlook add-in: add Platform S upload + corporate/domain de… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-06-16 | — |
| KS-131 | Outlook add-in — Workstream A: Platform S functions (v1: up… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-06-10 | — |
| KS-132 | Outlook add-in — Workstream B: corporate/M365 (domain) depl… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-05-25 | — |
| KS-242 | Euro Office (office.eu) connector — joint Platform K + Plat… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-06-10 | — |
| KS-243 | [Marketing] Euro Office (office.eu) connector — go-to-marke… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-06-10 | — |
| KS-247 | [Pre-mainnet] State-thread NFT — Sprint 2 Phase 2 (on-chain… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-06-10 | — |
| KS-248 | [Pre-mainnet] Replace stub ZK proof provider with a real pr… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-06-10 | — |
| KS-287 | [Dev] deploy.sh setup doesn't fully provision a fresh regio… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-305 | State the M365 source-document controller boundary in the c… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-14 | — |
| KS-330 | Phase 3 — Issuer certs + VC PQC signing (ML-DSA, dual-sign) | P3 | Backlog | — | n/a (no PR) | n/a | 2026-06-25 | — |
| KS-332 | Resolve PQC migration dependencies / decisions | P3 | Backlog | — | n/a (no PR) | n/a | 2026-06-25 | — |
| KS-354 | [start-secuura.sh --rebuild] Multi-arch image builds for am… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-07-14 | — |
| KS-408 | boot-platform-stack: assert no container is restart-looping… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-409 | Express 4 → 5 migration (all 15 services) — dependabot #447… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-410 | @types wave: @types/node 26 vs Node 24 runtime — dependabot… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-411 | TypeScript 5 → 6 migration (all packages) — dependabot #428… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-483 | Extend Prettier + knip quality tooling from into the base t… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-27 | — |
| KS-526 | KMS: move platform wallet mnemonic to Key Vault (KS-326 fol… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-07-25 | — |
| KS-528 | Frontends: react-router v6 → v7 migration (3 moderate clien… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-530 | @hono/node-server v1->v2 major bump (GHSA-frvp) - originate… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-541 | Proposal: smart-contract cascading governance hierarchy for… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-31 | — |
| KS-542 | Document encryption phase 2: personal + organisational keys… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-31 | — |
| KS-553 | arm64 GHCR images for the demo VM — compose pull instead of… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-02 | — |
| KS-562 | anchoring threadTokenMint test fails only under root-visibl… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-26 | — |
| KS-567 | CI: GHCR secondary-rate-limit kills deps-changed PR runs —… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-05 | — |
| KS-578 | Cross-tenant API-key revoke misses the DB row when the cach… | P3 | In Review | Kam/kksecura | NONE (#744: not run, CI dead) | APPROVED (#744 merged 09-01) | 2026-09-01 | Approach note ready, no code yet (revoke not durable); ours to build |
| KS-579 | Per-person platform-admin identities — the shared seeded ad… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-26 | — |
| KS-580 | Append-only recovery audit held outside the estate being re… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-26 | — |
| KS-581 | register-connector: volume alerting, rate limit, and correl… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-26 | — |
| KS-583 | DR rehearsal: lose a key → re-key → read-back survives on p… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-07 | — |
| KS-595 | Three undeclared-verb catalogue skips cite CLOSED tickets (… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-19 | Remaining: measure whether the three undeclared-verb defects are live |
| KS-604 | BM-5: System-details document for Peter & Stuart — the tech… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-11 | — |
| KS-605 | Terminology definitions for stakeholders + lawyers — certif… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-11 | — |
| KS-619 | Gateway tenant resolution falls through to the caller's x-t… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-621 | Document reads are scoped by tenant and owner, never by org… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-27 | — |
| KS-625 | /presentations/verify reports a presentation verified witho… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-13 | — |
| KS-626 | Entra Verified-ID callback is unreachable two ways: registe… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-13 | — |
| KS-627 | Implement real wallet signature verification (CIP-8/COSE +… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-26 | — |
| KS-629 | kyc `livenessVideo` is accepted by spec and runtime, then s… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-13 | — |
| KS-630 | Wire the status-page XSS probe into preflight (or decide no… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-650 | services/originate: POST /api/webhooks 500s on its two succ… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | Open question answered (stale fixture); fix the fixture |
| KS-658 | The demo VM runs every service as NODE_ENV=development whil… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-31 | — |
| KS-682 | Playwright keeps no run history — a re-run on the same slot… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-21 | — |
| KS-699 | No table references `users`: 0 of the database's 29 foreign… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-27 | — |
| KS-704 | k6 gate reports a failure rate with no status-code breakdow… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-27 | — |
| KS-736 | Gateway mount-auth check scores authenticateToken(false) as… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-738 | schemathesis run.py bootstrap can os.execv-loop forever on… | P3 | Todo | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-741 | x-emitter-internal is unstripped on the /originate/ route —… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-745 | api-gateway audit export calls /api/audit/logs — a route th… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-746 | Security events carry no tenant at all — KS-743 had to gate… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-747 | Spec drift: GET /api/security/keys declares no parameters w… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-750 | api-gateway + originate keep their own error handlers inste… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-306 | Decide + promote the Art.17 DPIA note into the formal DPIA… | P4 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-14 | — |
| KS-331 | Phase 4 — Decommission classical paths + residual-risk regi… | P4 | Backlog | — | n/a (no PR) | n/a | 2026-06-25 | — |
| KS-339 | Grant Phil + Steve extranet access (evolve toward company s… | P4 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-353 | [start-secuura.sh --rebuild] Clear npm dependency deprecati… | P4 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-403 | boot-platform-stack composite action reads BUILD_TAG/STACK_… | P4 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | — |
| KS-422 | flutter-verify-app: align Android Gradle/AGP toolchain with… | P4 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-14 | — |
| KS-456 | Optional: expose per-process Node heap/RSS metrics (light u… | P4 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-14 | — |
| KS-623 | Test-token env guard is asymmetric: the gateway fails close… | P4 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-13 | — |
| KS-648 | Frontend CSP quality: issuer alone carries 'unsafe-eval', a… | P4 | Backlog | — | n/a (no PR) | n/a | 2026-08-17 | — |
| KS-681 | Launcher drift warning counts HEAD but reports "on main" —… | P4 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-690 | scripts/check-test-wallet-testnet.sh has zero callers — wir… | P4 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-26 | — |
| KS-744 | Gateway 500s on every proxied route for a token lacking ver… | P4 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-748 | svc_api_keys.organization_id is not a tenancy boundary and… | P4 | Backlog | — | n/a (no PR) | n/a | 2026-09-01 | — |
| KS-749 | postcss-selector-parser 6.1.2 carries GHSA-w9m9-85wc-3x92 —… | P4 | Backlog | — | n/a (bump not started) | n/a | 2026-09-01 | The dependency bump itself; #780 (baseline) merged 09-01 |
| KS-740 | POST /api/timestamps/batch cannot serve its own documented… | — | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-09-01 | — |

## 2. Requires input (48)

| Ticket | Title | Pri | State | Assignee | Suites (four) | Peter | Last activity | Waiting on | Note |
|---|---|---|---|---|---|---|---|---|---|
| KS-441 | Akto CI scan throughput: ~21 s local vs ~10 min in the isol… | P1 | Blocked | Peter | PARTIAL (Akto·Schemathesis) | n/a | 2026-08-28 | Peter | Peter's ticket; post-merge review list recorded, not actioned |
| KS-608 | systemTest (Integration mode): GET /api/anchors/{id} and ve… | P1 | Blocked | Peter | n/a (no PR) | n/a | 2026-08-28 | Peter | Peter's ticket, Blocked |
| KS-660 | CI: every `needs: build` suite job dies in 3s with ZERO ste… | P1 | Blocked | — | UNKNOWN | NOT YET | 2026-09-01 | Kam (money) | Blocked on a money decision with a date (GitHub Actions org spend) |
| KS-61 | OpenAPI compliance: documentation gaps across the spec (des… | P2 | Todo | Stuart | n/a (no PR) | n/a | 2026-08-28 | Stuart | Assigned to Stuart (his work) |
| KS-62 | OpenAPI Specification Compliance: Optional Features | P2 | In Review | Stuart | PARTIAL (Akto·Schemathesis 08-12) | n/a | 2026-08-28 | Stuart (sign-off) | Stuart's ticket; #670 merged, example legs need Stuart's sign-off |
| KS-188 | Stateful testing: declare OpenAPI `links` + `operationId` s… | P2 | Todo | Stuart | n/a (no PR) | n/a | 2026-08-28 | Stuart | Assigned to Stuart (his work) |
| KS-232 | Enable Postgres HA + geo-redundant backups + extend retenti… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-12 | Kam (re-scope) | Deferred to commercialisation by Kam 2026-06-23; target resource no longer exists — needs re-scope |
| KS-239 | [Decision] Erasure: multi-step to trigger, but irreversible… | P2 | Backlog | Stuart | n/a (no PR) | n/a | 2026-08-12 | Stuart | Assigned to Stuart (his work) |
| KS-246 | [Pre-mainnet] External Aiken-specialist smart-contract audi… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | Kam (money, mainnet date) | Parked: needs budget + a mainnet date |
| KS-386 | KYC image payloads (svc_kyc_images.data) are plaintext at r… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-12 | Kam + compliance (Stuart) | KYC image retention is a compliance question; options a/b/c await ruling |
| KS-412 | CI: require all systemTest (all tools) PR suites + pre-merg… | P2 | Todo | Peter | n/a (no PR) | n/a | 2026-08-15 | Peter | Assigned to Peter (his work) |
| KS-489 | Review D — Blockchain / anchoring / smart-contract integrity | P2 | In Review | Kam/kksecura | PARTIAL (Schemathesis·Akto) | n/a | 2026-08-31 | Kam (prism scope ruling) | Review D register; the prism delete-vs-implement choice is Kam's |
| KS-525 | Playwright: end-to-end flow coverage across all 310 publish… | P2 | Backlog | Peter | n/a (no PR) | n/a | 2026-07-25 | Peter | Assigned to Peter (his work) |
| KS-568 | systemTest (Schemathesis): S↔K connector identity regressio… | P2 | Backlog | Peter | n/a (no PR) | n/a | 2026-08-07 | Peter | Assigned to Peter (his work) |
| KS-575 | Schemathesis sweep locks itself out of its own account (dem… | P2 | In Progress | Peter | UNKNOWN | NOT YET | 2026-08-25 | Peter | Assigned to Peter (his work) |
| KS-576 | Bulk re-key: one admin-authorised rotate across a named set… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-02 | Kam (rule on Stuart's proposal) | Stuart's grant-driven re-key proposal (2026-09-02) needs a ruling |
| KS-577 | rotate: true mints a new key but never revokes the old one… | P2 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-26 | Stuart (decision) | Contract decision on in-flight writes at revoke is Stuart's |
| KS-588 | systemTest (Schemathesis): /api/status authorization + revo… | P2 | Backlog | Peter | n/a (no PR) | n/a | 2026-08-28 | Peter | Assigned to Peter (his work) |
| KS-590 | systemTest (Schemathesis): verify-by-hash must not resolve… | P2 | Backlog | Peter | n/a (no PR) | n/a | 2026-08-12 | Peter | Assigned to Peter (his work) |
| KS-592 | negative_data_rejection recurs — 176 failures across 10 ops… | P2 | In Review | Kam/kksecura | n/a (no fix PR) | n/a | 2026-09-01 | Kam (KS-662 ruling) | Remaining work is a ruling (split accepted-invalid vs permissive; sequence KS-662 first) |
| KS-624 | prism issues VCs with random bytes as the Ed25519 proof and… | P2 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-08-13 | Kam (ruling) | Awaits Kam's ruling on prism's credential surface (KS-489 scope) |
| KS-634 | No CI gate runs the services' unit suites — a 73-test suite… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-17 | Kam (routing) | Duplicate pair with KS-652; which survives is on Kam's routing queue |
| KS-636 | node:24-alpine carries a CRITICAL (CVE-2026-59873) — our ow… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-15 | Kam (decide / authorise dispatch) | Evidence gathered; dispatching the shared CI watch / deciding is out of agent scope |
| KS-652 | No CI job runs any services/* unit suite — 1219 tests acros… | P2 | Backlog | — | n/a (no PR) | n/a | 2026-08-17 | Kam (routing) | Duplicate pair with KS-634; which survives is on Kam's routing queue |
| KS-665 | KS-256 review follow-ups: 5 example-fixable 400s, the tsx t… | P2 | In Progress | Kam/kksecura | n/a (no PR) | n/a | 2026-08-21 | Peter (agree design) + #568 landing | Item-2 fixture design posted for agreement; held until #568 lands |
| KS-685 | Define the work → test → commit → manual-merge process whil… | P2 | In Review | Stuart | FULL 2026-08-28 (post-merge SET on develop) | APPROVED 08-28 (#749/#751 at-head) | 2026-08-29 | Stuart (own the doc) | Stuart's process write-up; our evidence posted |
| KS-691 | Pre-push preflight cannot run from a git worktree — legs 1… | P2 | In Review | Peter | PARTIAL (Akto x4 slots + unit, 09-01) | n/a (author) | 2026-09-01 | Peter (draft → ready) | Peter's own fix, draft PR #765 |
| KS-717 | Akto test-id catalog and the loaded template library drift… | P2 | In Progress | Peter | UNKNOWN | NOT YET | 2026-08-29 | Peter | Assigned to Peter (his work) |
| KS-101 | Consolidate Platform K billing onto Platform S's Stripe int… | P3 | Backlog | Stuart | n/a (no PR) | n/a | 2026-07-14 | Stuart | Assigned to Stuart (his work) |
| KS-135 | Platform S "S+" refactor — pluggable upload/watermark/sign/… | P3 | Todo | Stuart | n/a (no PR) | n/a | 2026-05-28 | Stuart | Assigned to Stuart (his work) |
| KS-139 | Platform S — upload your test suite so the extranet live ru… | P3 | Backlog | Stuart | n/a (no PR) | n/a | 2026-08-14 | Stuart | Assigned to Stuart (his work) |
| KS-263 | Enable Code Security / GHAS so security scans populate the… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | Kam / GitHub org admin | GHAS/Code Security is an org-level GitHub setting (licensing) |
| KS-378 | Go-live login capacity decision: argon2 budget × per-IP lim… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-07-14 | Kam (decision) | Explicit go-live capacity decision ticket |
| KS-418 | systemTest (all tools): enable nightly platform test suites… | P3 | Todo | Peter | UNKNOWN | NOT YET | 2026-08-14 | Peter | Assigned to Peter (his work) |
| KS-492 | Review G — systemTest (all tools) security regression cover… | P3 | In Progress | Peter | FULL 2026-08-16 (CI fan-out) | n/a | 2026-08-28 | Peter | Peter's standing Review-G tracker |
| KS-502 | systemTest (Schemathesis): skipped security regressions nee… | P3 | Todo | Peter | n/a (no PR) | n/a | 2026-08-24 | Peter | Assigned to Peter (his work) |
| KS-533 | S↔K security register: data-loss / unrecoverability scenari… | P3 | Todo | Peter | n/a (no PR) | n/a | 2026-08-27 | Peter | Assigned to Peter (his work) |
| KS-545 | Rotate demo Cardano wallet mnemonic — GATED: do just before… | P3 | Backlog | Kam/kksecura | n/a (no PR) | n/a | 2026-07-31 | Kam (go-live date) | Gated: rotate just before go-live |
| KS-571 | systemTest (Schemathesis): KS-539 agent document-operation… | P3 | Backlog | Peter | n/a (no PR) | n/a | 2026-08-19 | Peter | Assigned to Peter (his work) |
| KS-572 | systemTest (Schemathesis): pin the KS-546 unhandledRejectio… | P3 | Backlog | Peter | n/a (no PR) | n/a | 2026-08-07 | Peter | Assigned to Peter (his work) |
| KS-573 | systemTest (Schemathesis): assert the shared control-byte b… | P3 | Todo | Peter | UNKNOWN | NOT YET | 2026-08-07 | Peter | Assigned to Peter (his work) |
| KS-582 | [Decision] Approval shape for bulk re-key — two approvers f… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-09-02 | Kam + Stuart | [Decision] approval shape; Stuart's 2026-09-02 proposal reshapes it |
| KS-606 | systemTest (Schemathesis): split scripts/run.py + scripts/r… | P3 | Backlog | Peter | n/a (no PR) | n/a | 2026-08-12 | Peter | Assigned to Peter (his work) |
| KS-651 | [Decision] @secuura/shared is imported by 24 services and d… | P3 | Backlog | — | n/a (no PR) | n/a | 2026-08-17 | Kam (decision) | Explicit [Decision] ticket |
| KS-657 | services/shared (@secuura/service-utils) cannot build — no… | P3 | In Review | — | PARTIAL (Schemathesis·Akto 08-17) | NOT YET | 2026-08-17 | Kam (decision, with KS-651) | Build half merged (#717); the retire/keep decision for services/shared is open |
| KS-679 | Published Anchor.id is anc_… but anchoring only ever mints… | P3 | Todo | Kam/kksecura | n/a (no PR) | n/a | 2026-08-21 | Kam (release hold) | Held deliberately on Kam's word (left in Todo on purpose) |
| KS-686 | not_a_server_error flags the by-design 501 on POST /api/wal… | P3 | Backlog | Peter | n/a (no PR) | n/a | 2026-08-26 | Peter (land guard) | Kam ruled 2026-08-26 (tolerate 501); Peter lands the guard |
| KS-341 | KS-327 follow-up — get X25519MLKEM768 PQ hybrid live on the… | P4 | Backlog | — | n/a (no PR) | n/a | 2026-08-14 | Kam (domain / re-decision) | Deferred per Kam 2026-06-27; no owned domain; premise now dead — needs re-decision |

## 3. Done on our side — awaiting approval (39)

| Ticket | Title | Pri | State | Assignee | Suites (four) | Peter | Last activity | Approval needed from | Note |
|---|---|---|---|---|---|---|---|---|---|
| KS-667 | KS-311 regressed on fresh deploys: migration 033 fails, vau… | P1 | In Review | Kam/kksecura | NONE (preflight 7/7 only) | APPROVED 09-01 | 2026-09-01 | Kam (deploy / accept) | #726 + #772 merged on Peter's at-head approval 09-01 |
| KS-490 | Review E — Deployment, containers & CI/CD supply chain | P2 | Todo | Kam/kksecura | n/a (review) | n/a | 2026-08-17 | Kam (close) | Review E fully dispositioned and re-verified 08-17 |
| KS-566 | KS-539 G-1 split alignment: add onBehalfOf to revoke; drop… | P2 | In Review | Kam/kksecura | UNKNOWN | APPROVED 09-01 (#742) | 2026-09-02 | Stuart (PS-616 reconcile) then close | Code DONE and MERGED (#742, approved by Peter 09-01); Kam ruled 'ask Stuart first' on the ownership gate |
| KS-570 | GET /api/status + /api/leaderboard/* accept revoked-session… | P2 | In Review | Kam/kksecura | PARTIAL (Akto red-run by Peter; deterministic probe) | REVIEWED, blocker cleared 09-01 | 2026-09-01 | Peter (approve/merge) | PR #730; Peter's 08-31 blocker cleared, run posted at 3fe1b6f1a |
| KS-635 | Audit baseline exception expires 2026-08-31 and will block… | P2 | In Review | Kam/kksecura | NONE (CI dead; preflight 7/7) | APPROVED 09-01 | 2026-09-01 | merge under Kam's merge-set; then close | #738; Peter approved 09-01 07:43Z (recorded on KS-729) |
| KS-641 | demo-service has no inbound auth — POST /demo-api/persona/s… | P2 | In Review | Kam/kksecura | NONE (CI dead; preflight 7/7) | REQUESTED | 2026-09-01 | Peter; then Kam (deploy) | PR #737 up; deploy precondition recorded |
| KS-643 | Security: DELETE /api/keys/:id revokes any tenant's key — n… | P2 | In Review | Kam/kksecura | NONE (#744: not run) | APPROVED 09-01 | 2026-09-01 | Kam (deploy / accept) | #744 + #771 merged 09-01 on Peter's at-head approval |
| KS-661 | Rename the `certify` lifecycle verb to `declare` | P2 | In Review | Kam/kksecura | NONE (preflight legs skipped) | n/a (Stuart approved #736) | 2026-08-27 | Stuart (S switches verb) then close | K half deployed to demo 08-26; PS-612 pinged |
| KS-664 | deepmerge-ts GHSA-ggr8-5vv4-36mx (high) — override to 8.0.1… | P2 | In Progress | Kam/kksecura | UNKNOWN | n/a (Peter's fix) | 2026-08-26 | Peter (close) | Fix merged via #725; Peter's ticket to close (baseline row stays) |
| KS-671 | anchoring /health reports 'healthy' with a dead chain path… | P2 | In Review | Kam/kksecura | UNKNOWN | NOT YET | 2026-08-20 | Peter | PR #728 attached; no comments |
| KS-678 | #568 publishes 17 URLs on secuura.io — an unresolving, seem… | P2 | In Progress | Kam/kksecura | n/a (rides #568) | n/a | 2026-08-21 | Peter (accept example.com host) / lands with #568 | Fix pushed on #568's base, folded into the custody branch; host choice offered to Peter |
| KS-688 | run-in-slot.sh locks per worktree, not per slot — two workt… | P2 | Tested Not Deployed | Kam/kksecura | FULL 2026-08-28 (post-merge SET on aa56bec75, KS-685) | APPROVED 08-28 | 2026-08-28 | Kam (deploy sign-off) | #749 merged 08-28 |
| KS-700 | Akto harness prints a FALSE ZERO when its Mongo capture fai… | P2 | Tested Not Deployed | Kam/kksecura | PARTIAL (Akto test:pr PASS + unit) | condition discharged; approval not evidenced | 2026-09-01 | Kam (deploy sign-off) | #752; Peter's merge condition discharged with a real failure |
| KS-702 | Akto `quality` gate is RED on develop — format:check, lint… | P2 | Tested Not Deployed | Kam/kksecura | FULL 2026-08-28 (Sch pr FAIL 6 pre-existing · Akto PASS · PW · k6 5/5) | review answered; approval not evidenced | 2026-08-28 | Kam (deploy sign-off) | #754; Peter's four review points answered |
| KS-703 | Security: a NUL byte in a query param 500s and leaks the ra… | P2 | In Review | Kam/kksecura | UNKNOWN | APPROVED 08-31 | 2026-09-01 | Kam (deploy sign-off) | #757 merged 08-31; 'merged is not deployed' |
| KS-705 | Anchoring is idempotent on the row but not on the submissio… | P2 | In Review | Kam/kksecura | UNKNOWN | APPROVED (inferred, KS-703) | 2026-08-31 | Kam (deploy sign-off) | #756 (KS-703 note: 'both merged on Peter's approval') |
| KS-706 | systemTest/performance quality gate is RED on develop — for… | P2 | Tested Not Deployed | Kam/kksecura | NONE ('not run, stated on the PR') | NOT YET | 2026-08-28 | Kam (deploy sign-off) | #755 |
| KS-712 | 173 routed /api endpoints are absent from the OpenAPI spec… | P2 | In Review | Kam/kksecura | UNKNOWN | REQUESTED | 2026-09-01 | Peter | PR #760; four parked findings filed |
| KS-715 | Akto result capture dies on ENOBUFS — execSync has a timeou… | P2 | In Review | Kam/kksecura | NONE (unit/lint only) | REQUESTED | 2026-08-28 | Peter | PR #759 on Peter |
| KS-727 | Security: errorHandler returns err.message verbatim on any… | P2 | In Review | — | UNKNOWN | APPROVED (#767); #776 REQUESTED | 2026-09-01 | Peter (#776) | #767 merged 09-01 (at-head approval); #776 (class guard) open |
| KS-728 | POST /api/auth/social/link never responds - auth.ts:909 pas… | P2 | In Review | — | UNKNOWN (Peter measured defect live 09-01) | APPROVED 09-01 | 2026-09-01 | Kam (deploy / accept) | #766 merged 09-01 on Peter's at-head approval |
| KS-742 | Security: GET /api/keys enumerates another tenant's keys an… | P2 | Deployed to UAT | Kam/kksecura | NONE (justified: /api/keys unpublished) | APPROVED 09-01 | 2026-09-01 | Kam / Stuart (UAT acceptance) | Deployed to demo and verified; #770 merged on Peter's at-head approval |
| KS-743 | Security: the KS-742 tenancy fix left three live siblings —… | P2 | In Review | Kam/kksecura | FULL* 2026-09-01 (SET ran; exercised 0 of the changed ops) | REQUESTED | 2026-09-01 | Peter | PR #778 (head bbafa5b6b) on Peter |
| KS-751 | Three HIGH advisories published 2026-09-01 block every push… | P2 | Backlog | — | UNKNOWN (preflight 9/9 only) | REQUESTED (#781) | 2026-09-01 | Peter (review #781) | PR #781 (script-mode gate) open on Peter; the actual bump is not started |
| KS-480 | S↔K (K-side): support consistent user/org ownership + crede… | P3 | In Review | Kam/kksecura | UNKNOWN | APPROVED w/ conditions 07-29 (§5/§6) | 2026-08-27 | Stuart (PS-319 close-out) / Kam (close) | K build complete (#610/#611); findings PR #672; Stuart's questions withdrawn |
| KS-508 | GET /api/documents/{id}/sig.json returns undocumented 400 (… | P3 | In Review | Kam/kksecura | FULL 2026-08-17 (CI checks green at merge) | not evidenced | 2026-08-25 | Peter (sweep confirm) / Kam (close) | Merged (#710) + deployed to demo; needs one clean Schemathesis sweep to close |
| KS-514 | POST /api/credentials → 500 INTERNAL_ERROR "Invalid time va… | P3 | In Review | Kam/kksecura | NONE (sweep not re-run) | REQUESTED | 2026-08-27 | Peter | PR #741 up |
| KS-539 | K: define governing rules for document operations by agents | P3 | In Review | Kam/kksecura | n/a (doc) | APPROVED 08-05 | 2026-08-19 | Stuart (sign-off) | Kam + Peter signed off 08-05; Stuart's sign-off deliberately outstanding |
| KS-611 | POST /api/timestamps/batch errors on every sweep (filter_to… | P3 | In Review | Peter | PARTIAL (Schemathesis full sweep 09-01) | n/a (author) | 2026-09-01 | Peter (close) | Peter's ticket; merged 09-01, acceptance holds |
| KS-622 | POST /api/auth/mfa/verify redeems backup codes with no proo… | P3 | In Review | Kam/kksecura | NONE (CI dead; preflight 7/7) | REQUESTED | 2026-08-26 | Peter | PR #745 (option B as ruled) |
| KS-645 | Security: POST /api/rate-limit/reset has no role check — an… | P3 | In Review | Kam/kksecura | NONE (CI dead; preflight 7/7) | REQUESTED | 2026-08-27 | Peter | PR #739 up |
| KS-646 | The `!test-wallet.env` negation makes the hardening structu… | P3 | In Review | Kam/kksecura | NONE (not run) | REQUESTED | 2026-08-26 | Peter | PR #740 up |
| KS-654 | frontend/demo-overlay ships an untracked, unversioned artef… | P3 | In Review | Kam/kksecura | FULL 2026-08-17 (CI: k6·Playwright·Schemathesis·Akto) | not evidenced | 2026-08-17 | Kam (close) | Merged (#713) on all pr jobs green; local-only, no deploy |
| KS-659 | api-gateway spec hot-reload never fires in the container —… | P3 | In Review | — | UNKNOWN | not evidenced | 2026-08-31 | Kam (close) | #718 merged 09-01 (per KS-611 note) |
| KS-680 | validate-env.sh stops at its first main-body error on bash… | P3 | In Review | Kam/kksecura | NONE (preflight 7/7 only) | APPROVED 08-31 | 2026-08-31 | Kam (close) | #743 merged 08-31; no deployable surface |
| KS-689 | POST /api/users/admin/create is mounted without authenticat… | P3 | Tested Not Deployed | Kam/kksecura | FULL 2026-08-28 (post-merge SET on aa56bec75, KS-685) | APPROVED 08-28 (relayed set) | 2026-08-28 | Kam (deploy sign-off) | #748 merged 08-28 |
| KS-711 | systemTest/akto + systemTest/performance quality gates went… | P3 | In Review | Kam/kksecura | UNKNOWN | NOT YET | 2026-08-28 | Peter | PR #758 attached; no comments |
| KS-721 | Anchor schema: accept and anchor platform-s's opaque identi… | P3 | In Review | Kam/kksecura | FULL 2026-08-31 (Sch FAIL 8/311=baseline · Akto PASS · PW PASS · k6 5/5) | REQUESTED | 2026-08-31 | Peter (PR) + Stuart (deploy gate) | PR #763 on Peter; deploy gate is Stuart's (S crypto-shred commitment) |
| KS-726 | Write-ahead the Cardano tx hash: persist the deterministic… | P3 | In Review | Kam/kksecura | UNKNOWN | APPROVED 09-01 | 2026-09-01 | merge under Kam's merge-set | #764 approved by Peter at 035f9b450; not merged |

## Method and corpus

**Board and filter.** Linear team `KS` (Platform K / Secuura Blockchain). GraphQL `issues(filter: {team: {key: {eq: "KS"}}})`, default (non-archived) scope, `first: 100` + `endCursor` pagination: pages of 100, 100, 11 issues; `hasNextPage` on the last page = `False`. Returned 211 non-archived issues; 0 of them in an excluded state, leaving **211 open**. A second read with `includeArchived: true` returned 741 issues: the 530 archived ones are Done 471, Deployed to UAT 17, Canceled 18, Deployed To Prod 9, Duplicate 5, plus 10 archived in non-closed states (Backlog 4, In Review 3, Todo 2, In Progress 1) — archived issues are off the board and treated as closed here; they are not listed.

**Workflow states of team KS (all 12):**

| State | Type | Treatment | Open count |
|---|---|---|---|
| Tested Not Deployed | completed | included | 5 |
| Deployed to UAT | completed | included | 1 |
| Backlog | backlog | included | 105 |
| Todo | unstarted | included | 47 |
| In Progress | started | included | 11 |
| Canceled | canceled | EXCLUDED (closed) | 0 |
| Duplicate | duplicate | EXCLUDED (closed) | 0 |
| Blocked | started | included | 3 |
| In Review | started | included | 39 |
| Deployed To Prod | completed | EXCLUDED (closed) | 0 |
| In Test | started | included | 0 |
| Done | completed | EXCLUDED (closed) | 0 |

`Deployed To Prod` (completed-type) is excluded as closed — it had zero non-archived issues, so the choice changes nothing. Both `Tested Not Deployed` and `Deployed to UAT` are included (category-3 candidates).

**Categories.** 1 = unassigned or assigned to Kam's Secuura account (`kamil.kreiser@secuura.ai`, the identity our agents work under as `kksecura`), state Backlog/Todo/In Progress, and no open question/blocker in the newest comments. 2 = assigned to Peter or Stuart, Blocked, or the newest comments show a pending ruling/decision/money/credential outside our agents' hands. 3 = In Review with a PR attached, or Tested Not Deployed / Deployed to UAT, or work merged and waiting on someone's sign-off/close. Where a ticket fitted two, the category names who must act next and the Note says so. Every row's placement was read from the full comment trail (585 comments across the corpus, `comments(first: 50)` sorted client-side by createdAt).

**Suites column.** FULL = all four platform suites (Schemathesis · Akto · Playwright · k6) evidenced as one SET on the ticket's PR or on the merged tree containing it, with the comment date; a GitHub-Actions `pr` fan-out green at merge time (pre-2026-08-27) counts as FULL and is marked "CI". PARTIAL names the suites evidenced. NONE = the comments state the suites were not run (typically "Not run — CI dead on org billing; push preflight 7/7 only"). UNKNOWN = a PR exists but the Linear comments carry no suite evidence either way (evidence may sit in the PR's Test Evidence block, which was not read). n/a = no PR to test. FULL* on KS-743: the SET ran but exercised none of the changed operations (the ticket's own F-9 note).

**Peter column.** APPROVED = a Peter approval is evidenced in a comment (review id/at-head SHA, or "merged on Peter's at-head approval"); REQUESTED = the PR is open on Peter; NOT YET = PR exists, no review evidence; n/a = no PR, or Peter is the author.

**Not measured.** GitHub was **unread from this seat**: `gh auth status` under the Secuura config reported no logged-in host, so PR review states, head SHAs and PR-body Test Evidence blocks were not consulted; every test/approval fact above comes from Linear comments only. Kam's lifting of the #568 hold (KS-256) is taken from the Wednesday session record of 2026-09-02, not from Linear, where the latest comment still says the hold stands.

## Sources

- Linear, team KS (Secuura workspace), read 2026-09-02T06:40:38Z via `https://api.linear.app/graphql` — issues, states, attachments, comments.
- Read key sourced transiently from `!CODING/Secuura/Blockchain/4_Credentials/.env` (`LINEAR_API_KEY`), never exported or printed.
- Wednesday commit log 2026-09-02 (10:2x entries) for the #568 hold status.
