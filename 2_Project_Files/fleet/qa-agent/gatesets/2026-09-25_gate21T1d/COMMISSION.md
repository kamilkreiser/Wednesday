# COMMISSION — DRAFT the tier-1 QA gate kit "gate21T1d" for ONE PR, #1239 KS-1263, ROUND 2 of 2. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-25 (~21:0x AEST, after Seat B 27th's READY at 11:05:25Z). Recorded here as the gate's commission; the QA
agent reads it. Shape copied from the round-1 kit `gatesets/2026-09-25_gate21T1c/` (this PR's round 1), with the tier-2d kit's disposable-Postgres
practice and its develop-pinned control arms, BRIEF_TEMPLATE.md and QA_AGENT_CHARTER.md.

## The PR — TIER 1, ROUND 2 of 2 (the cap: a NO GO ships nothing and tickets the residue)
- **#1239** KS-1263, head `c8e1875c21e994a746e36c8b8efec8de1d9dbc98` (Seat B 27th, READY FOR QA 11:05Z, message id
  `<010001a0d83dd130-b21d129c-bf56-4f91-aa6a-72bd19e97b45-000000@email.amazonses.com>`, captured verbatim in `mail_gate21T1d_ready.md`).
- Round 1 (head `42c20e998`) was NO GO by the tier-1 gate batch1234-t1: report
  `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1234-t1-r1/report.md`. Its #1239 findings:
  ROLLBACK-CELLS-SCHEMA (Major), G-S2-TXCLIENT (Minor), PLATFORM-URL-TRAP (Minor), NOT-PINNED ROUTE-ROLLBACK, POOL-IDENTITY (ticketed as KS-1304, NOT
  this round).
- **Wednesday's round-2 ruling (b):** prove it in MODE T (MULTI_TENANCY_ENABLED=true + PLATFORM_DATABASE_URL to a real secuura_platform). MODE F is a
  NAMED RESIDUAL (no generated Prisma client in a fresh worktree, `Cannot find module '.prisma/client/default'`, ticket KS-1305) and must fail LOUD,
  never pass mislabelled. No package.json edit.
- The seat's claims (a claim with an author): MODE T head 5/5; MODE T at develop e68e2f0e8 (second worktree, same DB) 1 failed / 4 passed, the route
  cell red "Expected: 0, Received: 1"; G-S2 tamper `createShare(…, prisma ?? tx)` 29/29 before, 1 failed / 28 after; MODE F 5 failed / 5 by name;
  originate unit 865/865; the push fast-forwarded the PR ref from 42c20e998 — c8e1875c2 is an amend of B 26th's WIP commit, parent 42c20e998.
  **Measured by the drafter:** head^ == 42c20e998, 42c20e998^ == BASE 6ab9d5021; the round-2 delta is exactly the two test files; the product blobs are
  unchanged (predict_1.out).

## The gate MUST
1. Re-derive every round-1 finding's disposition at c8e1875c2 (CLOSED / STILL OPEN / residual).
2. RUN the cells itself against its OWN database — a free stack slot OR a disposable Postgres on a proven-free loopback port with its own named volume,
   torn down and proven gone; never another gate's containers/volumes (a tier-2 gate batch1241 is running, `qa-g21d-pg-ks980`). Bring up MODE T for
   real (secuura_platform present; the initDb witness / getTenantManager() !== null), run the file at head AND at BASE (develop), reproduce the seat's
   discrimination, plant the G-S2 tamper, and confirm MODE F fails by name, not vacuously. **Drafter's choice: the disposable container** (README §6.1).
3. Check the route cell's red is the intended one (rows, not a connection/auth error), and that develop's drift since the merge-base does not touch the
   /share and /transfer-custody regions the cell reaches (re-measure).
4. Legs 3/4/8 only if a surface is touched (round 1: no surface).
5. Squash body own key only (drop KS-1155, KS-1228); subject <= 92 chars.
6. GO string: `GO: merge #1239 batch`. Routing `QA/Secuura-batch1239` — the drafter PROPOSES `QA/Secuura-batch1239|coagent@agentmail.to|yes` and did NOT
   write inbox_routing.conf.

## Deliver (drafter: no launch, mail, tap, commit, push; writes only in its work dir)
COMMISSION.md, the prompt, the launcher (`bash -n` clean), a repin-and-launch script (re-reads head / develop / mergeable at launch, refuses on mismatch),
a controls script run both ways with the doctored arms pinned to develop, a `--dry-run` of the repin script (rc 0), and README.md with the ONE launch
command.
