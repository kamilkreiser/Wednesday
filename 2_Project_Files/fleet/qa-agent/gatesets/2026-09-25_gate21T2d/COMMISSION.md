# COMMISSION — DRAFT the round-21 FOURTH tier-2 batch QA gate kit "gate21T2d" over #1241 and #1242. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-25 (~19:1x AEST). Recorded here as the gate's commission; the QA agent reads it. Shape copied from the
most recent tier-2 kit `gatesets/2026-09-25_gate21T2c/` (tier-2 content: through-code review + red proof RED at base / GREEN at head in the tester's
own clone; no browser) with the two-row mechanics of `gatesets/2026-09-25_gate21T1c/` (JSON pins, routing-file override, controls run both ways with
`--invert`), BRIEF_TEMPLATE.md and QA_AGENT_CHARTER.md.

## The batch — TIER 2 on both, FROZEN at two, round 1 of 2, one seat (Seat B 26th)
- **#1241** KS-1226 item 2, head `e2d0518df40228f0a183bc4223c7a6840821253e` (READY FOR QA 2 at 07:42Z). Claims: red proof in two steps (cells alone
  at the tip → 2 failed / 6 passed; R1/R2 fail by assertion "expected null to deeply equal { passed: 243, failed: 1 }"); package 1085/1085 base →
  1090/1090 head (+5 cells); capture groups asserted at build time (3 groups, passed at group 2). Item 1 (the 15 s budget at :127, F4) is a DECISION
  and OUT of scope — KS-1226 does not close on this PR. NOT covered per the author: no live child vitest emitting a real skipped segment; `todo` and
  other segments still return null. **This PR's product fix originated in a local-model (Spark) round that failed twice and was rebuilt by a Claude
  seat — review the diff independently.**
- **#1242** KS-980, head `a35569aa020e63b2660b60e48b4f0286c46b27fc` (READY FOR QA 3 at 08:03Z). Claims: shape (1), no new role / grant / migration;
  the integration test's DB user was a superuser with rolbypassrls=TRUE so the RLS predicate cells were inert; the fix routes the P1 cell through
  writerOn() on the APP role (secuura_app, bypassrls false). Red proof three arms: A,B = the ticket's tamper (predicate removed from both
  organizations subqueries) → P1/P2 cells fail; C = fix reverted → D1 and D2 fail while the original four stay green. Head 6/6 on the file; full
  originate integration 14/14 (2 suites). DB-gate refuses loudly (non-zero, named) when the app DSN is absent. NOT covered per the author: legs 3/4/8;
  TEST_APP_DATABASE_URL exercised only in its COMPOSED form; NO CI wiring.
- **Postgres for #1242:** a FREE stack slot (slots 2–4 hold kept volumes from today's gates; never touch another gate's containers/volumes; tear down
  what you start) OR a disposable container on a proven-free loopback port — the prompt states which, with teardown and a proof-of-gone step. A
  tier-1 gate (QA/Secuura-batch1234, pane %16) is running and may hold a slot. **Drafter's choice: a disposable container (no slot is free — slots
  2, 3 and 4 all hold kept volumes at 09:21Z); see the prompt's THE DISPOSABLE POSTGRES.**
- Develop at commissioning: `c41e268eb9355fe06eed7590455aa2fbbd90c59b` (moved today by many merges). Base-invariant checks required:
  diff(develop, merged) == own paths at head blobs, or a DECLARED overlap measured exactly. **Measured: no overlap for either PR.**

## Gate rules the prompt carries (from the precedent, in substance)
1. Per-PR GO / NO GO / GO WITH FINDINGS, findings-only; worktrees from refs/pull/<n>/head, never write the shared checkout.
2. The fleet STOP count in force after #1218: `pre_push_hook_base.test.sh` 28 passed / 0 failed, `pre_push_hook_base_fixture_guard.test.sh`
   6 passed / 0 failed, shell suites 60 of 60 — NO STANDALONE run of those suites.
3. Anchoring wording "N passed / 1 failed; threadTokenMint pre-existing (KS-562)" where anchoring runs (neither PR touches anchoring).
4. KS-1155 load false-red: re-run once; an assertion failure is real.
5. Reap only the gate's own processes (by cwd + ppid, never by name, never pid 1).
6. HOLDS: no merge, push, ticket/PR write, deploy.
7. GO string: `GO: merge #1241, #1242 batch`.
8. A MERGE ADDENDUM per PR (subject <= 92 chars, own keys only, equality targets, SHIPS-WITH line).
9. Routing `QA/Secuura-batch1241`; the PROPOSED line `QA/Secuura-batch1241|coagent@agentmail.to|yes` — NOT written by the drafter.

## Deliver (drafter: no launch, mail, tap, commit, push; writes only in its work dir)
COMMISSION.md, the prompt, the launcher (`bash -n` clean), predict / fill / repin-and-launch scripts, a controls script run both ways (every control
able to fail), a `--dry-run` of the repin script (rc 0), and README.md with the ONE launch command.
