## BLUF — retraction ACCEPTED, the deploy is HELD, and your proposed shape is RIGHT IN DIRECTION but has a hole I want you to close before you build it.
**Nothing is deployed. Nothing merged. Kam has been told, leading with it, and the gate has the
addendum.** You did the right thing at every step of this and it is on the scoreboard.

## 1. THE HOLE — `email` is `NOT NULL`, so the INSERT must still supply something
Your proposal: *"the migration should stop writing `email` at all… keep the primary-key conflict
target, but update only the non-PII columns, and let auth own the address."*

**Direction ratified.** Encrypted PII belongs to the service that owns the encryption; the migration's
stated purpose is *"seed per-client users so document FK constraints work"*, which needs rows to
EXIST, not addresses to be correct; and its **original** conflict tail updated only
`tenant_id`/`tenant_slug`, so this is a return to the original intent rather than a new design.

**But `docker/init/01-schema.sql:21` declares `email TEXT NOT NULL`.** So "stop writing `email`"
can apply cleanly to the **ON CONFLICT UPDATE tail** — and **not** to the INSERT itself, which must
put *something* in that column to create a row at all.

**So answer this before you build:** on a **FRESH** database, what does that column get?
- If the migration still inserts **plaintext**, the defect is **narrowed to fresh installs, not
  closed** — the column's invariant (every value is ciphertext, `email_lookup_hash` set) is still
  violated, just less often. **A narrower version of the same corruption is not a fix.**
- If the migration should not create these rows at all on a fresh database — because auth's
  `seedDemoUsers` creates them correctly — **then say so**, and the change is larger than a conflict
  tail: it is about which service owns those twelve rows.
- If there is a third answer, it is yours to find; **do not pick the one that makes the diff smallest.**

**State which, with the measurement that decides it.** This is the question your proposal implies and
does not answer, and it is exactly the kind that gets settled by whichever option is least work.

## 2. HOLD THE REDESIGN UNTIL THE GATE REPORTS — it is measuring your exact chain right now
**The gate reached the plaintext-into-ciphertext consequence BY ITSELF, before Wednesday's addendum
arrived.** Observed on its pane in the same action, with the addendum still queued and unread:
> *"Confirmed four defects with controls green. Now driving the decisive chain — whether the auth
> remediation can still see the row after the gateway writes plaintext."*

**So the gate is independently driving whether the auth path can still find the row after the gateway
writes plaintext — which is precisely the question your redesign turns on.** Wait for it. Building
against your own model when a measurement of that model is minutes away is how a fix gets written
twice.

## 3. WHAT WEDNESDAY IS RULING NOW, so you are not blocked on all of it
- **The deploy is HELD** until the shape is settled and re-gated. Kam's authorisation stands; the
  thing it authorised has changed, and he has been told that plainly.
- **The retraction is accepted in full and scoped exactly as you scoped it:** withdrawn is the claim
  that the demo is measurably exposed; **F1's core diagnosis (42P10, the statement never ran) stands
  because it was measured independently of any probe**, and F2–F5, KS-960, KS-961 and PR #887 are
  untouched.
- **No third probe.** The honest post-deploy check needs the HMAC key and you were right to refuse it.
  **"Not verifiable read-only from here" is the answer Wednesday wants recorded** — inventing a check
  that cannot fail, in this of all rounds, would be the defect wearing our own uniform.
- **The rotation measurement is NEXT after this**, not now.

## 4. WHAT WEDNESDAY OWES YOU — the credit, plainly
**You took your own finished, pushed, committed work apart twice today.** First the status guard, which
you built and then deleted after measuring that it could not fire. Now this — you read your own commit
message hours later, noticed you had quoted the ciphertext comment as the reason `ON CONFLICT (email)`
was invalid **and had not carried it forward to the probe you had already run**, and said so.

**Your sentence is the one going in the record:** *"the bug was preventing the migration from
corrupting the column, and fixing it releases it."* **A fix that is worse than the defect, found by
the person who wrote it, before it shipped.** Nothing in our gate design would have been as fast.

And the probe discipline held under pressure: **outcome C, stopped where the pre-registration said to
stop**, pre-registration hashed at 01:45:27Z **before** the run, the address never selected, and the
key refused. **Every one of those was a place you could have reached further and did not.**

## HOLDS
Push nothing to #885. **The deploy is HELD.** No third probe. No HMAC key. Do not touch the demo. No
history rewrite. No `rm`. No plaintext or hash in any artefact.

## PROVENANCE
- The ciphertext census, the column list, outcome C and the pre-registration hash | **your
  measurements, quoted.**
- The gate reaching it independently | **Wednesday's own `capture-pane` on `%150` at 11:48 AEST**, in
  the same action that sent the tap, with the tap showing as queued and unread.
- `email TEXT NOT NULL` | `docker/init/01-schema.sql:21`, as you cited it.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-07 — **the deploy is HELD pending the settled shape and a re-gate.**
- 2026-09-07 — **the migration must not write PII into a column the auth service owns; direction
  ratified, exact shape pending your answer on the fresh-database case and the gate's verdict.**
- 2026-09-07 — no third probe; "not verifiable read-only" is the recorded answer.
