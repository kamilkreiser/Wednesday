KS-1301 The relabel guard's presence-not-truthiness rule is pinned on /version only — sign-cert and sign-wallet have the same rule and no cell
state In Progress

## BLUF

PR **#1237** (KS-1229, merged `e119781ac993`) added four cells pinning that the **/version** route's relabel guard refuses a *present* `null`, empty-string or `false` `documentType`, and waves through only an **absent** one. Under a truthiness tamper of that guard, exactly the three new cells go red — so the pin is real.

**The same presence rule exists on** `sign-cert` **and** `sign-wallet`**, and neither is pinned.**

## Why this is the interesting half

A truthiness bug here is invisible to ordinary testing, because `null`, `''` and `false` all *look* absent to a `if (!documentType)` check while being present in the request. That is precisely the confusion #1237 proved the /version route does **not** have. The two sibling routes make the same distinction and nothing holds them to it — so the guard that was hardest to get right is the one with the least coverage on two of its three call sites.

## The fix shape

Port #1237's four cells to `sign-cert` and `sign-wallet`: a present `null`, a present empty string, a present `false`, and an absent field — with the same truthiness tamper as the red proof, which must redden exactly the new cells.

## NOT claimed

Not a measured defect on either route. Nobody has shown `sign-cert` or `sign-wallet` mishandles a present-falsy `documentType`; the finding is that **nothing would notice if they did**, which is a coverage claim, not a behaviour claim.

## Board search before filing (team Secuura-PK, 1,286 issues incl. archived, 3,631 comments, literal match on titles, descriptions and comments)

* `sign-wallet` -> 20 total / 7 open; `sign-cert` -> 25 total / 7 open; `documentType` -> 52 total / 18 open. The nearest open rows (KS-1229 itself, KS-1213, KS-1202, KS-1133) were read for overlap: **KS-1229** is the parent this residue comes from, and the others concern other properties of those routes, not the presence-vs-truthiness rule.
* Controls that fire: `consumeResetToken` -> 3; nonsense control (`zzz-nonexistent-zzz`) -> 0.

`Refs KS-1229`; does not close it.

## Provenance

Tier-2c QA gate `2026-09-25-batch1218-t2c` (report sha256 `70dc4c987f04…`), raised as a **non-blocking** finding and recorded at the merge. Filed on the coordinator's instruction after the batch landed; it did not hold the merge.
