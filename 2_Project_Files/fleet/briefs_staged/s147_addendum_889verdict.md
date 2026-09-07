## ADDENDUM to the SUCCESSOR brief — the #889 gate returned one second after it was sent. Read both.

## BLUF
**#889 is GO-with-findings — and its MERGE IS HELD by Wednesday, deliberately.** Not because the gate
failed it (it did not), but because **Finding 1 is Kam's, and it is carded to him with default HOLD.**
**Your work from this verdict is Finding 2, now. Findings 3–5 are filed. Finding 5 is urgent to route.**

## THE MANDATED LEG PAID FOR ITSELF — the reason it was named in the brief
The tester built a real Postgres from the product's **own** provisioning path (`docker/init/*.sql` as
`docker-compose` mounts it, then `run-migrations.sh` verbatim, 48 applied), validated it against the
running dev DB on every property this change touches, and drove **the real `saveDocument`** through the
product's own pool proxy as **`secuura_app`** with RLS forced — **reading every value back out of the
row by a separate superuser connection**, never from the binding. Ten registrations, nine rows, one
correctly refused by RLS.
**Its own words: the two properties the mocked cells could not reach — a schema dependency that turns a
NULL into a 500, and a tenancy predicate no cell pins — are BOTH only visible from a real database.**
That is the whole argument for the leg, measured rather than asserted.

## ⚖️ RULINGS

**1. #889 — DO NOT MERGE. Held pending Kam.** The issuing organisation is taken from the request body
and written with **no check that the caller belongs to it**, while `req.user.organizationId` is in the
same scope — and fifteen lines above, the same handler resolves `onBehalfOf` against the key's own
organisation and **403s a different one**. Within a tenant, a caller can attribute a document to
another organisation. Across tenants it correctly folds to `NULL`.
**Why it is Kam's and not mine:** #889 is the first change that makes that answer visible **on the
public verification surface**, and whether an organisation is a trust boundary inside a tenant is the
open product question **KS-621** is already holding. **On a document-verification product, publishing
an unverified claim about who issued a document is a product decision.** Kam's own boundary from today:
*a merge is Wednesday's; a merge that decides something with a client is his.*
**Do not "fix" it into the PR to unblock yourself** — that decides the question by implementation.

**2. Finding 2 — FIX IT NOW. This is yours and it is in scope.** The new suite is **blind to the
tenancy predicate, the one property it was written to protect** — the ticket's own commit message ranks
it second of three, and the suite would not have caught its removal. **Your regression must drive a
real Postgres**, per KS-968's rule and this gate's proof. **The tester has handed you the exact
control that works:** tamper by deleting `AND tenant_id = ${tenantId}::uuid` from **both**
`organizations` subqueries (leave the `parent_document_id` one alone), and isolate on the two paths
where RLS does **not** already exclude the row — `app.tenant_scope_bypass='platform_admin'`, and a
`BYPASSRLS` role. **On the ordinary `secuura_app` path the predicate is redundant, so a naive tamper
shows nothing and looks like a pass.** That is why its first attempt produced a false null.

**3. Finding 5 — MAJOR, out of scope, and ROUTE IT BEFORE YOU DO ANYTHING ELSE WITH THE BACKFILL.**
This change **arms a previously-inert cascade delete of documents.** **Kam authorised the KS-597
backfill at 10:34 today as its own round AFTER the fix merges** — so this finding lands directly in
front of a round he has already said yes to. It must reach whoever owns **KS-764 / PS-690** first. The
tester's own words: *"the one I would not want quietly filed."* **Do not let it be.**

**4. Findings 3 and 4 — file and track.** 3: column and metadata diverge on re-POST and the column can
never be filled afterwards. 4: *"a registration never fails because of this field"* holds **only on a
schema carrying migration 017** — that qualifier is measured, not rhetorical.

## 🔴 A CORRECTION TO WEDNESDAY'S OWN BRIEF, disclosed because you will see the numbers
**Wednesday's gate brief gave "base develop `9e9a88709`". That was wrong** — it was develop's CURRENT
HEAD, which is not the same thing as the PR's base. The PR API reports `base.sha`
`632f16dfe`, and **neither is the true merge base, which is `db94e9fc8`**; develop has since advanced
`632f16dfe → 023acccf8 → 9710cc1fd → 9e9a88709`. **The tester caught it, used the PR files API rather
than a two-dot diff so the moved base could not contaminate the file list, and it cost nothing.**
**Carry the distinction: "current develop head" and "this PR's base" are two different facts, and a
brief that says one while meaning the other invites a contaminated diff.**

## CREDIT — going on the scoreboard at 1.0
**It caught its own broken instrument and reported it rather than dropping it:** a `TRUNCATE documents`
that failed on an FK meant the tampered run re-POSTed onto the pristine rows and looked identical to
the control. **Two identical runs mean a broken instrument, not a passing product** — it said exactly
that, re-ran with `CASCADE`, and only then reported. It also **refuted its own hypothesis in the
open**, named its fidelity caveat (no generated Prisma client, so it drove the pool proxy and said the
equivalence was read rather than executed), reported the GitHub checks API 403 as *"a limit of my
instrument, not a finding"*, and stated plainly which findings it was **less** confident about.
**It searched the board by symbol, path AND error string before filing, and listed what it reviewed.**

## SELF-CHECK
This addendum does not contradict the SUCCESSOR brief sent one second before it: that brief's queue was
KS-969 item 1 first; **this addendum INSERTS Finding 2 and the Finding 5 routing ahead of it**, which
is a re-ordering, not a reversal. KS-969 item 1 remains your next work after those two.
