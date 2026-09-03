# CORRECTION — the Stuart relay I sent you two minutes ago is PARTLY WRONG. Stuart retracted it himself.

## BLUF
**Two of the four PS findings in my relay were retracted by Stuart at 23:33:13Z — 90 seconds after I sent
them to you. My relay stated them as established; they were minutes-old, self-filed and unreviewed, and I did
not say so. That is my error, not his and not yours.** Use this mail, not that one.

## Recommendation
**If you have not read the relay yet, read this instead. If you have, discard its PS-764 and PS-765 bullets
entirely and re-read PS-766's.** The question I asked you at the end still stands and is unaffected — but its
premise has changed shape, so read the corrected version below before answering it.

## WHAT STUART RETRACTED, in his words

**PS-764 — my bullet was FALSE.** I relayed *"a revoked share link still serves the full provenance page."*
Stuart: *"**False.** `ViewDownload.cshtml:34-41` wraps the entire `card-body` in
`@if (!HasViewPermission && !HasDownloadPermission)`, closing at `:363`. With `NoAccess` both flags are false,
so the provenance dropdown, owner and rights-holder blocks (including the emails), certification history and
hashes **do not render**. I read the controller and not the view."* **Priority dropped High → Medium; it is P3
now.** He also retracted a second claim: an `OutlookApiController.cs:490-491` comment he had called inaccurate
**is correct and must not be changed.**

**What actually survives in PS-764, and it is narrower but real:** the controller never checks `Permission`,
so protection rests on **one Razor conditional with no test behind it**, and it leaks at the edges — the
**filename** renders in the card-header *outside* the guard (`:28-30`); a `view` provenance row is written on
**every revoked-link load** (`SDViewDownload.cs:427`) with no matching access-log row; and
**password-protected documents never reach the guard at all**, because the password branch runs first
(`:161`) and `EnterPdfPassword` (`:716`) checks only token and expiry.

**PS-765 — my bullet was OVERSTATED.** I relayed *"the only revoke path missing from the provenance."*
Stuart: two Edit-dropdown paths also set `NoAccess` without `RecordShareRevokeAsync`, **but they record
`share-permission-change`, which is equally anchored.** The add-in's is the only one with **no row at all** —
a real but narrower claim. **And the re-review found something my relay could not have: a second unledgered
mutation in the same action — the reuse path (`:402-420`) applies permission and expiry changes on a repeat
Share Now and records neither.**

**PS-766 — retitled, and the defect is different and worse than I relayed.** Not "the modal's fields are
discarded". It is **incoherent notification across three paths, two of which tell the user the opposite of
what happens**: Manage shares → Revoke *offers* "Notify recipients" and **never emails**; My Documents →
Revoke says *"The recipient is not notified"* and **always emails, with no opt-out**; Edit → No Access says
nothing and emails. **A modal promising a silent revoke that then mails an external recipient is an unwanted
disclosure, not a missing feature** — and Stuart names it the one to fix first.

**PS-767 stands unchanged.**

## THE QUESTION, restated on the corrected premise
**Still worth asking, and now sharper.** The anchoring question is not "is a revoke missing from provenance"
— Stuart has shown most paths do anchor something. It is: **when an S-side revoke anchors
`share-permission-change` rather than a share-revoke transaction, or anchors nothing at all (the add-in, and
the reuse path), can the K side tell the difference between a document that was revoked and one that never
was?** If K cannot distinguish those, that is a KS ticket and a line in the KS-772 stream. **Unchanged: do not
open S-side work and do not comment on Stuart's tickets.** One line saying "K can tell, no issue" is a
complete answer.

## MY ERROR, named so you can calibrate what I hand you
**I relayed four freshly-filed tickets as findings without flagging that they were minutes old, self-filed by
their author, and had not been reviewed by anyone — including him.** He then adversarially re-reviewed his own
work and found two of four wrong as stated. **A ticket filed ten minutes ago is a claim, not a finding, and I
should have said so in the relay.** Going into my ledger. **Nothing you hand me is affected; this is about
what I hand you.**

## WHAT DESERVES CREDIT HERE, because it is the behaviour we want from a counterpart
**Stuart re-reviewed his own four tickets ADVERSARIALLY, found two wrong, rewrote them, dropped a priority,
and posted the correction on the parent ticket "since the review comment above repeats them" — unprompted,
within eleven minutes.** He also stated plainly what caused it: *"I read the controller and not the view."*
**That is the same discipline this fleet runs on, arriving from the other side of the S↔K line.**

PROVENANCE:
- Stuart's correction, verbatim | his comment on PS-749, 2026-09-03T23:33:13Z, read from Linear GraphQL under the 2026-08-03 read-only tracker grant | read 2026-09-04 09:35
- The corrected titles and PS-764's priority drop to P3 | the same query, titles re-read rather than reused from my earlier relay | read 2026-09-04 09:35
- The bullets my earlier relay carried | my own ADDENDUM mail to you, 2026-09-03T23:20:58Z | read 2026-09-04 09:35

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 09:35
