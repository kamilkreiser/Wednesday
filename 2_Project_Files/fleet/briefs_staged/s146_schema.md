# ADDENDUM — while you are on that box: capture which SCHEMA it carries. It decides whether ANY of this reaches Kam's row.

## BLUF
**One addition to the deploy verification you are already doing. It is READ-ONLY and it is not a new
probe** — it is the deploy establishing the state of its own target, which your brief already required
(*"verify the artefact, not the exit code"*). **Do not widen it into anything else.**

**Capture, from the database the deploy targets:** does `users` have **`email_lookup_hash`**,
**`tenant_id`**, **`tenant_slug`**? Do the functions **`auth_find_user_by_email_hash`**,
**`_by_id`**, **`_by_email_legacy`** exist? Is there a unique index on `email_lookup_hash`?
**Never select the address.** Column and function names only.

## WHY IT MATTERS AND WHY IT IS URGENT-ISH RATHER THAN URGENT
The round-2 gate measured the **Azure** substrate — round 1's biggest NOT-TESTED — by standing up
`deployment/azure/migrate/init.sql` exactly as `deployment/azure/migrate/run.sh:26` applies it. On
that schema: **no `email_lookup_hash`, no `tenant_id`, no `tenant_slug`, and 0 of 3
`auth_find_user_by_email_*` functions.** Driving the upgrade shape there:

> `error "Failed to seed demo user" {"error":"function auth_find_user_by_email_hash(unknown) does not exist"}`
> → row afterwards: **status=active, REAL-HASH. THE REMEDIATION DOES NOT RUN AT ALL.**

**So: if the box carries the Azure-init schema, merging and deploying #888 remediates NOTHING there.**

**Your own KS-960 note** — *"the running DB has no FK, so the deployed schema is docker/init again"* —
**is evidence for the other answer, and the gate was careful to call it evidence and not a
measurement.** You are the only one on that box today. **One `information_schema` read settles it.**

**Three live possibilities for Kam's row and nobody has excluded any of them:** S3-shaped
(remediated), S5-shaped (the 23505 in F3-RESIDUE, NOT remediated), or Azure-schema (nothing runs).

## BOUNDS — narrow, and they are the point
- **READ ONLY.** `information_schema` / `pg_proc` / `pg_index` shape queries. **No row data. No
  address. No credential. No write, no restart, no migration you were not already running.**
- **This is NOT a widening of Kam's probe authorisation** — his `domain-probe-then-decide` ruling is
  spent and delivered as your deploy's before/after proof. **This is your own deploy verifying its
  target's shape.** If you disagree that it falls inside the deploy, **say so and do not run it** —
  I will card it for Kam instead. **That refusal would be correct and I would back it.**
- **Nothing about Azure credits, subscriptions or billing** — Kam killed that subject at 13:06. The
  word "Azure" here means a SQL file in the repo, nothing more.

## WHAT TO DO WITH THE ANSWER
Put it in the deploy receipt as its own line. **If it is the Azure schema, say plainly that a later
#888 deploy would remediate nothing on this box** — that is a bigger finding than the deploy itself
and it goes to Kam through me immediately, not at your wrap.

PROVENANCE:
- The Azure substrate measurement, the 0-of-3 functions and the "does not run at all" result | the QA gate's round-2 verdict, 2026-09-07T03:56:49Z, §AZURE, quoted; NOT re-derived by Wednesday | read 2026-09-07
- Your KS-960 "no FK, so docker/init" note, carried as EVIDENCE not measurement | the gate's own characterisation of it in the same section | read 2026-09-07
- Kam's probe ruling being spent and delivered | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-demo-row-060-remediation - Wednesday's own tree, not yours | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 14:02
Adds one read to the deploy verification and supersedes nothing. It explicitly declines to widen
Kam's spent probe authorisation and offers the refusal path if the seat disagrees with the scoping.
