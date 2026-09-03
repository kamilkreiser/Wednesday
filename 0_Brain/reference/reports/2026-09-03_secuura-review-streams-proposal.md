# Secuura / Blockchain — review streams for Peter and Stuart (proposal, 2026-09-03 12:0x)

## BLUF
Four review streams cover **all 97 active Platform K tickets** (40 + 19 + 18 + 20; zero unmapped, zero duplicates): **three for Peter, one for Stuart**. Each stream is one Linear parent issue with the tickets as sub-issues and **one test pass** built from commands that already exist in the repo's DEV-PROCESS (measured wall-clocks, not invented). Built as an **overlay**: the 18 existing projects stay as the fine-grained catalogue; 3 new parent issues are created (one parent is reused) and 85 tickets are re-parented. Nothing deleted, no ticket changes project.

## Recommendation
Approve as proposed. **Default: if you have not objected by 12:45, the agent builds the overlay** (3 parents + 85 re-parentings). Amend by naming a stream or a ticket to move.

## The four streams

| Stream | Reviewer | Tickets | Parent | Folds in | The one test pass |
|---|---|---|---|---|---|
| **1. Platform Security** | Peter | 40 | reuse **KS-485** (already the root of KS-486/487/489/490/491/492 and their children; 11 already parented keep their parents, KS-485 adopts 28) | Auth/Tenancy/Access (15) · Security Review K (13) · Akto OWASP (8) · Security/Privacy/Compliance (1) · the K-side half of Anchoring (3) | Akto `test:pre-merge` (~7–8 min; full OWASP 30–50 min) → the five Code Security Gates (seconds each) → `npm test` in auth, api-gateway, security, anchoring + `packages/shared`. **Stated gap:** until KS-716 lands the super-admin surface is unscanned — a clean Akto today is clean over a smaller surface than it looks. |
| **2. API Contract & the four platform suites** | Peter | 19 | NEW parent | Schemathesis (11) · OpenAPI Spec (6) · Playwright (1) · k6 (1) | regenerate the spec → **restart** the gateway (bind-mounted yaml; a rebuild does not publish it) → Schemathesis pre-merge (**13.4 min measured**, ~2,016 cases / 318 ops) reporting the failing SET of operation ids vs the develop baseline → spec-auth-conformance → Playwright static+unit+e2e → k6 smoke reading the printed Status line (exit is 0 either way). Two traps go in the stream description: a second back-to-back Schemathesis run 401s at setup (the fuzz tiers change demo@'s password — `docker restart secuura-auth` re-seeds); a partial stack gives a confident FALSE RED (502s scored as findings). |
| **3. Build, supply chain & release gates** | Peter | 18 | NEW parent | Dependency Currency (7) · Infra/Dev Env (6) · CI/CD Gates (4) · Docs/Process (1) | from a **clean checkout on macOS**: preflight → lockfile clean-room → `npm run test:migrations` (~40 s) → validate-env. Every ticket in the stream is a way that sequence currently fails or lies on someone else's machine (bash-4 syntax, validate-env stopping at the first error, preflight from a worktree, the audit baseline expiring). One reviewer, one clean checkout, one run. |
| **4. S↔K integration contract** | **Stuart** | 20 | NEW parent inside the existing "Integrate S with K" project | Integrate S with K (17) · the S-facing half of Anchoring (3: KS-721 identityCommitment, KS-683 anchor-status standoff, KS-735 what verify shows) | run **from Platform S against K, by Stuart** (the acceptance is an S-side behaviour): register-connector → originate with identityCommitment → anchor → verify → anchor status → erasure by external_ref → rotate + bulk re-key → revoke-on-rotate; plus K's systemTest Integration mode (KS-608). The only stream whose pass the author cannot run alone — which is why it is Stuart's. |

**Why the cut is where it is:** by what one test pass proves, not by topic. Anchoring is the example: KS-671/705/679 are proved by K's own suites (Peter 1); KS-721/683/735 only by an S-side call (Stuart). Keeping the project whole would give Stuart three tickets he cannot test.

## What stays outside
- The **82 backlog** tickets (nothing to test yet; they join a stream at Todo).
- Four projects with zero active tickets: Commercialisation · SSO (Entra/Google/Apple/GitHub — PS-side) · Post-Quantum Migration · Connectors.
- The **12 Tested Not Deployed** — past review; they belong to today's demo/UAT deploy, not a stream.
- Peter's own PR #792 and the 10 dependabot PRs.

## Mechanics and the one risk
Overlay, not replacement: 3 new parent issues + 85 re-parentings; the 2026-09-02 catalogue (18 projects, 35 archived with reasons) survives untouched. Risk: Linear's free-plan create cap has refused creates before at no readable threshold — the three parents are the only creates; re-parentings are updates and are not capped. If a create is refused, the agent stops and reports.

*Source: Secuura agent s115, plan-confirmation 2b, 2026-09-03 01:56Z, every id read from Linear in the same action (state + assignee). Nothing on the board has moved. Prepared by Wednesday.*
