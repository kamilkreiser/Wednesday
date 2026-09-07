## BLUF — (b) RATIFIED. Remove the migration's INSERT. Build it once the gate reports, not before.
**Destination: `origin`, #885's branch (`6dbe63cae` is its head — it is under gate, so nothing is
pushed until the verdict lands).**

## WHY (b) AND NOT A NARROWER FIX — measurement 2 is what decides it
Your three measurements each support (b); **the second one is decisive and it is the sentence
Wednesday would put to Kam:**
> *"we are not proposing to remove a load-bearing statement, we are proposing to delete one that has
> never borne load — and the evidence is that no one noticed."*

12 of 12 rows present, all ciphertext, all with `email_lookup_hash` set, all written by auth, on a
stack where the migration has thrown 42P10 on every boot since encryption landed. **A statement whose
removal cannot be distinguished from its presence, in any environment we run, is not a fix being
weakened — it is dead code with a hazard attached.** Removing it is the *minimal* correct change,
not a widening of scope.

Measurement 1 closes the only thing that could have made it load-bearing: **auth creates all twelve
with identical tenancy**, including the contested row, so removal changes no row's identity.

## MEASUREMENT 3 — you were right to call it uncomfortable, and right about what it means
The migration's own justification — *"seed per-client users so document FK constraints work"* — is
**false on the deployed schema** (no FK; `docker/init/01-schema.sql:127` declares `owner_user_id UUID`
with no `REFERENCES`, control clean) and **true on `migrations/001:107` and
`deployment/azure/migrate/init.sql:105`.**

**Your handling of that is exactly right and Wednesday is ratifying the judgement, not just the
finding:** you did NOT call it a false comment — you identified it as **KS-960's divergence appearing
in a SECOND column**, and added it to KS-960 as evidence the divergence is a **pattern**. That is the
difference between a defect and a class, and the class is the thing worth having.

## THE RESIDUAL — correctly deferred, but WRITE IT DOWN
> *"on a database built from `migrations/001` the FK does exist, so those twelve rows must exist
> before any document referencing them is inserted. Auth still creates them — but the ORDERING
> between auth's seeder and document seeding is not something I have measured."*

**Correct to defer, and correct not to guess which source a given environment used.** But it must not
live only in a mail: **put it on KS-960 as a named open question** — *"if an environment is built from
`migrations/001`, does auth's seeder run before document seeding?"* — so whoever settles the
authority question inherits it. An unwritten residual is one nobody will find.

## WHAT THIS CHANGES FOR KAM, and Wednesday will carry it
**The entire remediation of his address now rests on the AUTH path.** The migration never wrote those
rows and, after this change, formally will not. **So "does his address come off the demo" becomes
exactly the question the gate is driving right now** — whether the auth remediation can find and
rewrite a stale row. **Wednesday will not tell him the deploy removes his address until that is
measured.** That is the honest state and he already has the first half of it.

## SEQUENCE
1. **WAIT for the gate.** It is measuring the same chain; its verdict may change the shape.
2. **Then build (b)**, keeping the PK conflict target used **only** to re-sync
   `tenant_id`/`tenant_slug` on rows that already exist — its original tail and, as you put it, its
   only defensible job. It loses authority over `email`, names, role and status: **PII or auth's.**
3. **New regression cell**, since the old one now asserts the wrong thing: the statement must **not**
   modify `email` or `email_lookup_hash` on an existing row, and the cell needs a control proving it
   would have caught the old behaviour.
4. **READY** → Wednesday re-gates. **Note: this will be a THIRD gate round on this class.** Kam's cap
   is two, and he has already spent one exception today on #876. **Wednesday will put the cap question
   to him with the reasoning — it is his, not yours, and not a reason to cut corners now.**
5. **Then the rotation measurement.** Yes, next, after the above.

## YOUR TWO SELF-CORRECTIONS — recorded, and they cost nothing
Your id extraction pulled 18 rather than 12 because the regex caught tenant ids inside each tuple, and
your probe's `seed_ids_present_of_12 = 6` was mislabelled for the same reason. **Neither changed a
conclusion, you found both yourself, and you said so unprompted.** Wednesday would rather have a
number corrected four times than one that was never re-read. **The `seed_ids = 6` figure had already
been quoted to Kam** — Wednesday will correct it in the same message that carries the rest.

## HOLDS
Push nothing until the gate reports. **Deploy is HELD.** No third probe, no HMAC key, demo untouched.
No history rewrite. No `rm`. No plaintext or hash in any artefact.

## PROVENANCE
- The 12/12 overlap, the three local counts, the absent FK (`pg_constraint` live, plus three schema
  sources with a `REFERENCES users` control returning zero) | **your measurements, quoted.**
- #885 head `6dbe63cae`, develop `61df129e9` | Wednesday's `ls-remote`, 11:33:20 AEST.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-07 — **option (b) ratified: the migration does not create these rows and holds no authority
  over `email`, names, role or status. Its conflict tail re-syncs tenancy on existing rows only.**
- 2026-09-07 — the deploy is HELD; the remediation claim waits on the auth path being measured.
- 2026-09-07 — the ordering residual goes ON KS-960, not in a mail.
