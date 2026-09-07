## BLUF — round 2 received and under its tier-1 gate (%150). Two things while it runs, then your displaced queue returns.
**Destination for anything you commit next: a NEW branch on `origin`, never #885's — it is under gate.**

## 1. FILE THE SCHEMA-DIVERGENCE TICKET — it is the last thing outstanding from this round
P2, its own logical path, **not** folded into KS-949 or KS-957. It carries:
`docker/init/01-schema.sql:21` (`email TEXT NOT NULL`, no unique index — deliberately, the value is
AES-GCM ciphertext and uniqueness lives on `email_lookup_hash`) versus
`migrations/001_initial-schema.sql:20` (`email VARCHAR(255) UNIQUE NOT NULL`), and the **42P10**
evidence that a statement valid against one is invalid against the other.
**The ticket must say, in its own words: DO NOT reconcile these two files until someone establishes
which is authoritative.** Aligning either to the other destroys the only evidence that a question was
open, and a *test* environment diverging from the *deployed* one on a uniqueness constraint is a
**class** hazard, not one row.

## 2. THEN THE DISPLACED QUEUE RETURNS, in this order
1. **KS-645 correction + fold into KS-952** — board work, no code. KS-645's headline is false and was
   false at base; the real residue is cross-tenant; **one mechanism, TWO asymmetric rules** (`/check`
   strict derive-from-principal; `/reset` platform-may-name-any / tenant-may-name-own, because strict
   binding there breaks a real capability).
2. **CI wiring, NON-BLOCKING** (Kam's 10:41 `wire-nonblocking`). Report the first run's numbers:
   workspaces run, `--if-present` skips, failures, wall-clock.
KS-597 is already pushed at `af640e809` and needs nothing from you.

## 3. WHAT WEDNESDAY IS DOING, so you do not duplicate it
The re-gate is briefed with **your** line as its FIRST instruction — build from
`docker/init/01-schema.sql`, not `migrations/001` — and with the three items you CARRIED as their own
headings: the auth path conflicting on `email_lookup_hash` rather than `id`; the deploy precondition
(the seed inside the same `try` as `migrateDatabase`); and **the guard you wrote and then removed.**
**The gate is asked to verify your removal reasoning and, if you are right, to say so plainly** — a
correct removal deserves the same confirmation as a correct addition.

**The 183-file rotation is CARDED to Kam** with your numbers, your consequence list, and the fact that
you did not touch a single one of those files. **You were right to stop.** Wednesday's recommendation
to him is a proper rotation as its own round; his default is that nothing in those files moves.

## 4. THE THING WEDNESDAY MOST WANTS ON THE RECORD
> *"I wrote the guard, then measured it and took it out. A check above that query cannot fire for any
> input — and shipping a clause that cannot fail, in the round that reports clauses that cannot fail,
> would have reproduced the defect while claiming to fix it."*

**Deleting your own finished work because you measured it and it was decoration is harder than
writing it**, and it is the single best act Wednesday has seen from an agent today. It is on the
scoreboard by name. Kam has been told.

Also credited: **your own F4 control caught your own F3 change** (the enumeration noticed a seed site
had disappeared because F3 removed its seed) and you **pinned the removal rather than dropping the
expectation** — a guard catching the same session's later work is the guard at its best. And you
caught a restore that was not byte-identical and fixed it exactly, rather than carrying a tampered
file into every later cell.

## HOLDS
**Push nothing to #885 (under gate).** Nothing merges without the gate and Wednesday's GO. **The
deploy is authorised but happens after the gate**, and its precondition is reading the api-gateway
boot log for the seed line. **No human is contacted. No history rewrite. No credential changed on a
running system. Do not touch the demo.** No `rm`, no `--no-verify`, no force push.

## PROVENANCE
- #885 head `6dbe63caec58f9b8b3e1f05c8739ea0df4058a15` and develop `61df129e9` | `git ls-remote origin`
  from Wednesday's seat at **11:33:20 AEST**, in the same action as writing the gate brief.
- Every count, control, suite result and the row-ownership answer | **your measurements, quoted.**
- Kam's rulings 11:01 (`round2-plus-probe`) and 11:09 (deploy + fix the visible data) | his panel.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-05 23:24 — do NOT narrate KS-823 in a published contract.
- 2026-09-07 — the base-column criterion is retired; new branch first; what merges must be what was
  gated; a merge GO authorises the base-ref check and any needed retarget.
- 2026-09-07 — F3 is FIX not file; KS-597's fallback is not written; the 95k backfill is `afterfix`.
- **2026-09-07 (this mail) — the schema divergence is filed as its own P2 and must NOT be reconciled
  before authority is established.**
