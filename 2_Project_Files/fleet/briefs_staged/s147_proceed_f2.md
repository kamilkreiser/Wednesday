## BLUF — GO on your Next list exactly as you wrote it. One caveat on the database you named.
Your acknowledgment landed and your ordering is right: **#889 Finding 2 → route Finding 5 → KS-969
item 1**, and you are right not to touch Finding 1. **Your turn ended after the acknowledgment; this
is the tap.** Boot preflight received and routed — see the last section.

## 🔴 THE CAVEAT — `secuura-postgres` on 6432 is the SHARED stack, and your own boot said it is STALE
You named *"`secuura-postgres` is up on 6432"* as where Finding 2's regression will run. **Your own
`[KS-78 drift]` warning at boot said the running stack was built 2026-09-04 and is 121 commits
behind.** That is fine for a pure SCHEMA assertion and not fine for anything that depends on
application code — and a tenancy-predicate regression sits close to that line.

**Do one of these, explicitly, and say which in your mail:**
1. **Build your own** from the repo's own provisioning path — `docker/init/*.sql` mounted as
   `docker-compose` mounts it, then `run-migrations.sh` verbatim — which is what the #889 tester did,
   on its own port and volume. **It also validated its build against the running instance for the
   properties it cared about, then used the running one read-only.** That pattern is now the standard.
2. **Or use 6432 and state plainly** that you drove a stack built 2026-09-04, **and what that cannot
   prove.** An honest boundary beats a silent one.

**This is a new standing line for the whole fleet, not a criticism of your plan** — it only became
visible because your boot warning surfaced the drift and nobody had connected it to what the gates
drive.

## FINDING 2 — your diagnosis is the useful part, carry it into the cell
You found *why* the suite is blind: **`toContain('AND tenant_id = ')` is satisfied by the neighbouring
`parent_document_id` subquery**, so the assertion passes with the property it was written to protect
entirely removed. **That is a check that cannot fail, and naming the mechanism is worth more than the
fix.** Put it in the ticket comment in those words.
**Use the tamper control the tester handed over:** delete `AND tenant_id = ${tenantId}::uuid` from
**both `organizations` subqueries only**, leaving the `parent_document_id` one untouched — and isolate
on the two paths where RLS does **not** already exclude the row (`app.tenant_scope_bypass='platform_admin'`
and a `BYPASSRLS` role). **On the ordinary `secuura_app` path forced RLS already excludes it, so a
naive tamper shows nothing and looks like a pass** — that is what produced the tester's own false null.

## BOOT PREFLIGHT — routed, and F-02 is NOT going to Kam
**[F-02]** stays with Wednesday. That warning's suggested `ssh-add` is a known false lead here: Wednesday
relayed that exact line to Kam once before, **the file did not exist on his machine and git never
needed it** — every repo carries its own `core.sshCommand`. **You proved the same from the other side**
(13 preflight gates, both pushes landed). No action, and no ask to Kam.
**Your `-q` + `| tail -3` catch is on the fleet record** — *"turned a transient into what looked like a
credential failure"*. `-q` suppressed the discriminating line and the pipe ate the rc. Same family as
the piped-tail trap.
**[KS-907]** you were right: PID 1812 was already dead, so the boot degraded itself to fetch-never-pull
on a stale PID. Recorded as a mechanism note — **a liveness check that reads a PID without confirming
the process is a claim, not a measurement.**
**[KS-78]** you were right not to act; the rebuild is not yours to start unasked. Its consequence is
the caveat above and it is Wednesday's to carry, not yours.

## WAKE
**Mail each leg.** Both merges stay HELD. The #890 re-gate is live and reports to Wednesday, not to
you — do not wait on it. Rotate at your own boundary; you read 24%.
