# For the records (MPSCALC-420 and MPSCALC-417), gate round 1

## The tickets now
Both tickets read Backlog, 0 comments, last updated 2026-11-20 10:18 AEDT in the kit's own read at drafting (this gate did not re-read Jira; it is not asked to). A merge does not move a ticket by itself: the records pass moves both and comments on both, after the pull request lands.

One sentence for the MPSCALC-420 comment: the first clause of the X-39 row of docs/ENGINE.md now says the contract carries the purchase recurring projection for a caller with internal-metrics (`purchase.projection`, absent for any other caller) and that the purchase result screen shows it to that caller as a table; no other byte of the file changed; developer documentation only, so no word review is asked (project record C-109, the coordinator's reading); nothing deployed.

One sentence for the MPSCALC-417 comment: infra/README.md gained 16 lines and lost none: step 2 is marked as the record of the first deploy and says it stops at the parameter file with no client ids exported (export both first to what-if an existing site, as step 6 does); the pinned budget start is stated with what to change if a first create is refused, and a first create after October 2026 is said to be not measured; the differences a what-if of the existing site showed on 2026-11-20 are named; nothing deployed.

## What the words rest on, and what is relayed
- The ENGINE.md clause rests on code at main (the contract member, the mapping that nulls it without internal-metrics and on a restricted snapshot read, the result screen that renders the table). Not said: whether the table's words are approved or what the hosted site runs.
- The README's hosted facts are relayed from the deploy record of 2026-11-20 (the what-if's deltas, `netFrameworkVersion` v4.6 against v4.0, the apply that left the budget start at 2026-10-01 and changed none of the 12 site-config fields it hashed, an update with the same past start accepted). They are written as "read on", not as always. The sentence that a first create with a past start is accepted or refused is stated as not measured.
- The date 2026-11-20 is the deploy record's AEDT date; its UTC stamps read 2026-11-19 (about 22:25Z). The README gives no time zone. Not wrong; a records note.

## Ticket candidates (not blocking, not this change)
1. `infra/scripts/validate.sh:4` says the what-if "is infra/README.md step 3". The what-if is step 2 (the create is step 3). A comment in a script; one line to correct. Candidate for a new ticket.
2. `infra/README.md` step 6 still says "expected: Modify of the site's appsettings only" for the what-if of the existing site; the new list says the what-if shows other differences. The kit left line 63 byte-equal on purpose (the ticket asks that it still read true) and the list says to count net of them. A later wording change could reconcile the two; not a defect of this change.
3. The `sku.tier` NoEffect delta of the 2026-11-20 what-if is not in the new list (the ticket does not name it).
4. The second clause of the X-39 row (the Api cannot state a fee) is unchanged and agrees with docs/API.md:611.
5. The ENGINE.md row now reads "... as a table (the web table, T-V5-7), and ..." so "table" appears twice; the parenthetical was kept on purpose (the ticket: keep every other word). A tidy only if someone edits the row again.

## Measured in the gate
The CI python loop at the head: 15 files, each rc 0 (counts in VERDICT.md). The reach probe at the head equals the kit's. Nothing is deployed; landing is the pull request, hosted CI and CodeQL.
