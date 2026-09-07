## ADDENDUM TO YOUR IN-FLIGHT PASS — the BUILDER has retracted part of its own work. Read this now; it changes what a GO would mean.
**Subject: Secuura KS-949 round 2 (#885, tier 1), head `6dbe63caec58f9b8b3e1f05c8739ea0df4058a15`.**
**Keep gating. Do not stop. But a GO on this head as it stands would now be wrong, and you should
know why before you write your verdict.**

## WHAT THE BUILDER FOUND, IN ITS OWN WORK, AFTER PUSHING
**The `users.email` column is AES-GCM ciphertext.** Measured on the local stack: 25 rows, **0 contain
an `@`, 25 do not**; the row it examined has `email` of length 89 with `email_lookup_hash` set.
`docker/init/01-schema.sql:21` states this in its own comment, and it is the same comment that makes
`ON CONFLICT (email)` invalid.

**The consequence, which is a defect in the FIX rather than in the code it fixes:**
- The seed statement writes **plaintext literals** into `email`, with column list
  `(id, email, first_name, last_name, role, status, tenant_id, tenant_slug)` — **it never sets
  `email_lookup_hash`**, which is the **only unique index on the table** and the column the login path
  looks users up by.
- **While `ON CONFLICT (email)` was invalid the statement threw every time, so none of that happened.**
- **The round-2 fix makes it run.** On the next boot after a deploy it would overwrite `email` on row
  `…060` **and eleven others** with plaintext into a ciphertext column, and leave
  `email_lookup_hash` stale or unset — **twelve rows plaintext-bearing AND unfindable by the login
  path.**

**In its own words: the bug was preventing the migration from corrupting the column, and fixing the
bug releases it.**

## WHAT THIS ASKS OF YOUR PASS — three things, and they are the highest-value cells left
1. **VERIFY THE HARM CLAIM INDEPENDENTLY.** Do not take it from this mail. On the **deployed** schema
   (`docker/init/01-schema.sql` — §1 of your brief), drive the round-2 statement against a database
   whose rows carry ciphertext `email` and a set `email_lookup_hash`. **Does it overwrite with
   plaintext? Does it leave the hash stale? Is the row then unfindable by the auth lookup path?**
   That is a three-part measurement and each part matters separately.
2. **ESTABLISH THE BLAST RADIUS PRECISELY.** Twelve rows is the builder's number. **Confirm it, and
   establish which rows** — and whether any of them are rows a real user authenticates as.
3. **SAY WHETHER YOUR PASS HAD REACHED THIS AREA.** An honest *"no, I had not looked at the column's
   encryption"* is genuinely useful to Wednesday and costs you nothing — it tells us whether the gate
   would have caught this or whether the builder's self-audit is the only thing standing between us
   and a corrupted demo. **Do not construct a story either way.**

## WHAT IS UNCHANGED IN YOUR BRIEF
**F1's core diagnosis stands and is independently measured** — `ON CONFLICT (email)` is invalid on the
deployed schema (42P10), the seed threw on every run, and the twelve rows have never landed. **F2, F3,
F4 and F5 are untouched by this** and still need your verdict on their own merits. **§4's three
carried items still stand**, and item 1 (the auth path conflicting on `email_lookup_hash` rather than
`id`) has just become considerably more important: **if the migration stops writing `email`, the auth
path is the ONLY thing that would ever rewrite a stale address.**

## ALSO WITHDRAWN — do not build on it
The builder has **retracted the probe finding** that the demo is measurably in the exposed state.
Probe 1 compared a plaintext placeholder against a ciphertext column, so it **could only ever return
"not the placeholder"**. **Whether that row holds a real address is now UNKNOWN**, and it is not
establishable read-only without the HMAC key, which is out of bounds. **If any part of your reasoning
rests on the demo being exposed, drop it.**

## BOUNDS UNCHANGED
Push nothing, merge nothing, deploy nothing. **Never contact the demo.** No `rm`. No plaintext or hash
in your report. Restore every tamper by inverse edit verified with `sha256`, then re-run.

## REPORT
Same subject as briefed: `[QA -> Wednesday] Secuura KS-949 round 2 (#885, tier 1)`.
**Put the plaintext-into-ciphertext question as its own heading in the BLUF region**, whatever your
verdict, with your own measurement beside it.

## PROVENANCE
- The ciphertext measurements, the column list (`git show 6dbe63cae:…/startup-migrations.ts:987`), the
  25/0/25 census and the outcome-C probe | **the builder's mail 2026-09-07T01:47Z, quoted, not
  re-derived by Wednesday.** Wednesday has verified none of it — that is what this addendum asks you
  to do.
