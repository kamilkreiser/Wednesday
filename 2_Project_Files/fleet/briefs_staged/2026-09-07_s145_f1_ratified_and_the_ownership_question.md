## BLUF — F1 RATIFIED, and your expanded diagnosis is inside scope: keep going. **But your own finding raises the question the DEPLOY depends on, and it is not yet answered: which seed path actually owns row …060 on the demo, and will this fix rewrite it?**
No new authorisation needed — you found a bigger version of the defect you were sent to fix, and
"fix the seeder" still covers it. **Do not stop.** Finish F2–F5 and push one head.

## 🔴 THE QUESTION — answer it before READY, because Kam's deploy hangs on it
**Your two measurements together imply something neither of them says alone.** You wrote:
> *"if the twelve-row seed has NEVER succeeded on that box, the six ids present must come from another
> seed path — and there are other paths (`docker/init`, `deployment/azure/migrate`)… I am not claiming
> which."*

**That restraint was right. But follow the implication one step, because it decides whether the deploy
works:** if row `…060` on the demo was written by `docker/init/01-schema.sql` or by
`deployment/azure/migrate/run-platform.sh` rather than by `startup-migrations.ts`, then **fixing
`startup-migrations.ts` may not rewrite it** — and Kam has authorised a deploy on the understanding
that it removes his address.

**So: establish WHICH path owns that row on the demo, and state plainly whether the round-2 fix
rewrites it.** Three honest outcomes and Wednesday wants whichever is true:
- **(a) The fixed seeder rewrites it** — the deploy does what Kam thinks it does. Say how you know.
- **(b) Another path owns it** — name the path; **that path needs the same remediate-then-skip**, and
  it is in scope under Kam's *"fix the issues with the visible data."*
- **(c) You cannot establish it without a second probe** — say so and STOP. Wednesday takes the probe
  question back to Kam; he ruled one probe and a second is his.
**Do not touch the demo to answer this.** Source reading and your existing probe data first.

**This is the coordinator's question, not a criticism of your report** — you were asked to fix a
seeder and you did, better than the brief asked. Wednesday's job is the sentence nobody's task
contains, and the sentence here is: *a fix that does not reach the row is a deploy that does not
remediate.*

## F1 — RATIFIED, and the diagnosis expansion is the better finding
**`ON CONFLICT (email)` is INVALID on the deployed schema (42P10), so the statement threw on EVERY
run, fresh database included.** That is a strictly larger and better-supported claim than round 1's,
and **it indicts the gate's own control**: *"fresh DB → INSERT 0 12"* was measured on
`migrations/001_initial-schema.sql` (where `email` is `VARCHAR(255) UNIQUE`) and is **false** on
`docker/init/01-schema.sql` (`email TEXT NOT NULL`, no unique index — deliberately, because the email
is AES-GCM ciphertext and the uniqueness lives on `email_lookup_hash`).

**That is this ticket's own shape, one level up: a control built on the wrong environment reports
green while every deployment fails.** Measured in **rolled-back transactions** against the running
stack — the right way to ask a live system a question.

**The suite is the best regression work Wednesday has seen this week.** The statement **extracted from
the product source with its sha256 printed** rather than restated (a copy drifts, passes, and proves
nothing about what ships); **CONTROL-1** asserting the OLD form still fails 42P10, which proves the
harness reproduces the defect instead of passing everything; **CONTROL-2** checking the row count
against a WRONG expectation so "12" cannot be a constant quietly agreeing with itself; and a red-proof
that reds **9 of 12 with exactly the right 3 staying green.** Legs 10 and 12 checked rather than
assumed, including that the reached-suite count moved 14 → 15.

## CARRIED TO THE RE-GATE — your line, and it is the most important sentence in the next brief
> *"Ask the tester to build the DEPLOYED schema, not the migrations one. Round 1 measured a fresh-DB
> success that cannot happen in any environment we run."*
**It is already written into Wednesday's re-gate notes verbatim and will be in the brief's §1.**
Without it the re-gate reproduces the same false green, which is precisely how this defect survived
round 0.

## NEW TICKET — file it, do not fix it this round
**Two divergent schema sources for the same table.** `docker/init/01-schema.sql:21` and
`migrations/001_initial-schema.sql:20` disagree about `users.email` (TEXT no-unique vs VARCHAR(255)
UNIQUE). **Do NOT reconcile them** — establish which is authoritative first, and the ticket says so:
the deployed one is what runs, the migrations one is what tests build, and **aligning either to the
other without settling which is correct converts "not built yet" into "not in the contract".** Name
both files, both lines, the 42P10 evidence, and that a *test* environment diverging from the
*deployed* environment on a uniqueness constraint is a **class** hazard, not one row. **P2, its own
ticket, its own logical path** — it is not KS-949's and not KS-957's.

## THE REST OF THE ROUND — unchanged
F2 (three files still publishing a password beside the identity) · **F3 (FIX, with the consequence
list: which environments authenticate with that credential today, MEASURED — and no plaintext, no
hash, in any artefact)** · F4 (guard enumerates seed sites from the tree — and note your own finding
makes this sharper: the other seed paths are not hypothetical, one of them is probably what seeded the
demo) · F5 (revert `ALLOW_DEFAULT_SEED_PASSWORDS` to default-DENY) · then **push ONE head** and READY.

## HOLDS
Nothing merges without the re-gate and Wednesday's GO. **The deploy is authorised but happens AFTER
the gate.** No history rewrite. **No credential changed on a running system.** **Do not touch the
demo.** No `rm`, no `--no-verify`, no force push. No plaintext or hash in any artefact.

## PROVENANCE
- The 42P10 / `INSERT 0 1` pair, both schema declarations, the suite results and the red-proof |
  **your measurements, quoted, not re-derived by Wednesday.**
- `seed_ids_present_of_12 = 6` | your probe of 01:06:50Z, quoted.
- Kam's deploy grant and *"fix the issues with the visible data"* | his panel 2026-09-07 11:09:06.
- F1 committed locally at `8ea9cf9d4`, unpushed | your report; Wednesday has not read your tree.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-05 23:24 — do NOT narrate KS-823 in a published contract.
- 2026-09-07 — the base-column criterion is retired; new branch first; what merges must be what was
  gated; a merge GO authorises the base-ref check and any needed retarget.
- 2026-09-07 — F3 is FIX, not file (supersedes the 11:02 mail).
- **2026-09-07 (this mail) — the expanded F1 diagnosis is RATIFIED as in-scope. The schema divergence
  is a SEPARATE ticket and must NOT be reconciled before authority is established. Answer the
  row-ownership question before READY.**
