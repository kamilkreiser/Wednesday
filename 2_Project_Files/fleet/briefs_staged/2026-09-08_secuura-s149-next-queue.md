# NEXT QUEUE — three tickets from today's own findings, in an order that unblocks

## BLUF
**Your queue is not dry — today's work filed eight tickets and three of them are yours to clear now.**
Kam's standing direction (2026-09-02): a ticket that needs no external input is executed, never
listed. **Order matters: KS-990 first, because it UNBLOCKS KS-989.** Checkpoint at your rhythm; if
only the first two fit, say so and stop at a boundary.

RULED BY KAM, NOT YET IN AN ARTEFACT
- **Assignment (Kam, 2026-09-06 09:42, as corrected 10:24):** every NEW or UNASSIGNED Platform K
  ticket is assigned to OUR account. **All eight of today's are unassigned — assign each one to us
  as you pick it up**, and cite the instruction in your first comment. A ticket already on Peter or
  Stuart stays theirs; none of these is.
- **Aggregation (Kam, 2026-09-07 13:23):** one larger ticket per logical path, items as a checklist
  — never three tickets for one line of work.

## 1. KS-990 (P3) — `npm run quality` cannot pass in EITHER package. DO THIS FIRST.
`performance/lint`: `runner/actor_manifest.ts` — `error TS2540: Cannot assign to 'secrets' because
it is a read-only property`. `akto/knip`: two unused exports in `src/core/endpointFalsePositives.ts`.
**Both fail on `develop` today, so neither is yours and neither is new.**
**WHY IT IS FIRST, and it is the whole reason this ordering exists:** KS-989's remedy is to wire a
gate into the push path. **Wiring `quality` while it is permanently red creates a gate that can never
pass — and a gate that can never pass gets bypassed, which is exactly how five instances of KS-989
accumulated unseen.** Fixing this is what makes KS-989's real fix possible.
**Prove it both ways:** `quality` red before, green after, in BOTH packages, with the failing rule
named. **If TS2540 turns out to be load-bearing** — if `secrets` is read-only for a reason and the
assignment is the defect rather than the type — **stop and tell me.** Do not cast it away.

## 2. KS-993 (P2) — nothing type-checks `systemTest/fixtures/`
No tsconfig covers it, so **the TypeScript that runs every suite is type-checked by nobody** — the
gate called this the most useful thing in its report and I agree.
**Expect it to find real defects, and treat that as the point rather than as scope creep.** Add the
narrowest tsconfig that covers the directory, run it, and **REPORT what it finds before fixing
anything beyond trivia.** A wall of new errors is a finding and possibly its own ticket, not a
licence to refactor. **Do not loosen the config to make it pass** — that is the same shape as wiring
a gate that cannot fail.

## 3. KS-992 (P3) — both quarantine guards `rm -rf` what they may have failed to snapshot
`pre_suite.test.sh:51-57` and `quarantine_call_sites.test.sh:40-56`: both `cp`s discard errors with
`2>/dev/null` while `restore()` unconditionally `rm -rf`s `generated/` first. **The gate described
the fix-shape and the regression test it wants — use them.**
**Carry its honest limit into the ticket: the mechanism is proven, a realistic trigger is NOT.** Its
mode-000 trigger is contrived and it said so. **Do not manufacture a realistic trigger to justify the
fix** — the fix stands on the mechanism; say the trigger is unproven.
**Both files, one ticket** (the class, per the aggregation rule) — it is inherited from the model
suite I told you to copy, so it is mine as much as anyone's.

## NOT IN THIS QUEUE, and why
- **KS-989 (P1)** — re-scoped by the gate's correction: **CI is CONFIGURED** (`pr-security-gates.yml:83`
  wires 17 suites including yours) **and cannot EXECUTE** (billing, Kam's). **Put that reconciliation
  ON the ticket** as your first act — before anyone spends a day wiring what already exists — then
  leave it. Its remedy waits on KS-990 and on Kam's billing fix.
- **KS-986** — blocked on the ADMIN_USER_PASSWORD decision. **KS-987, KS-988, KS-991** — real, not
  urgent, and I would rather three done properly than six half-done.
- **KS-968 / #793 / #896 / #899 / #900** — all with Kam. Unchanged.

## HOLDS
Nothing merges without my GO. **Nothing deploys** — the demo is on `400517aaf` and stays there.
No comment addressed to Peter or Stuart. Kam's signature classes unchanged. No `--no-verify`; if the
preflight fires on a stale local `develop` again, **that is KS-991's third instance — record it.**

PROVENANCE:
- the eight tickets, their ids, priorities, states and unassigned status | Linear GraphQL read of KS issues created since 2026-09-07T20:00Z, 8 returned | read 2026-09-08
- KS-990's two failures and that both fail on develop | YOUR measurement reported 22:37Z, with the TS2540 line offset of exactly 7 as its identity evidence | read 2026-09-08
- KS-993's gap and KS-992's fix-shape and honest limit | the QA gate's round-5 report, items 4 and F5-1 | read 2026-09-08
- CI configured vs executing | `pr-security-gates.yml:83` per the gate; 100% startup_failure per KS-961 | read 2026-09-08 — two instruments, two questions
- scope/reversibility: all three are additive or corrective changes to test tooling on a branch, nothing merges under this brief, nothing deploys, and the demo surface is untouched | the HOLDS above | read 2026-09-08

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 09:40
