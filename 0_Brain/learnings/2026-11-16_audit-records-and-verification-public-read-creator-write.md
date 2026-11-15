---
date: 2026-11-16
type: grant
source: Kam, live board 2026-11-16 07:03:38 view=wednesday (note on card secuura-ks1703-ac4-same-company-reads-1115)
status: live
tier: W
---

# Secuura: audit records and verification are PUBLIC to read; only the creator (and uses the smart contract expressly allows) may WRITE them. A standing rule for every related task and ticket

**The operative case, so the headline matches it:** Wednesday is about to brief, stamp, gate or GO any Secuura work that decides WHO may read or write an audit record or a verification result (KS-1703 and its siblings, the analytics/audit routes, any access-control cell on them). **Read access is not restricted for these two record kinds: anyone in the world may read them. Write access is the creator, plus any use the smart contract expressly allows.** Brief and gate against that, not against the older "company-wide" or "creator and admins only" options.

**His words, verbatim (07:03:38):**
> *"Decision secuura-ks1703-ac4-same-company-reads-1115 note: new rule for all related tasks and tickets.  Audit records and verification can be read by anyone in the world.  writing can only be done by the creator and other uses expressly allowed in the smart contract"*

He answered the card OUTSIDE its two options (a company-wide, b creator and admins only). The card tool cannot record a note as a choice, so the card was WITHDRAWN with his words as the reason (07:0x) and this file is the record (the 2026-09-20 KS-1175 precedent).

**Wednesday's reading, said back on the panel at 07:0x (bf-b7e41615d299) with what is checked before anything is built:**
1. "Anyone in the world" = unauthenticated read is allowed for audit records and verification results.
2. Write = the record's creator, plus uses the smart contract expressly allows; nobody else (admins are not named, so admin WRITE is not granted by this rule).
3. **Data EXPORTS are not named** and stay as they are (cross-company refused by PR 2242; inside-company unchanged) until he says otherwise.
4. **Two things measured BEFORE any change ships (Wednesday's duty, told to him):** (a) PR 2242 (merged 2026-11-16, KS-1703) refuses cross-company audit reads: the parts that contradict this rule are identified at source by a seat; (b) what an audit record HOLDS (emails, user ids, IP addresses, personal data): a public read of a record carrying personal data is a privacy exposure, and it goes back to Kam with the measurement before any route is opened (the 2026-08-21 challenge-me rule; personal data is the one place this rule could hurt).

**How to apply:**
1. Every Secuura brief touching audit or verification access carries this rule verbatim in RULED BY KAM, with the reading above.
2. A cell that pins "cross-company audit read refused" is now pinning the OPPOSITE of his rule: such cells are named in the next build/measure seat's brief, not silently kept or silently deleted.
3. Do not widen it: exports, documents (KS-1695: ownerless documents = platform admins only) and certifications keep their own rulings.
4. No expiry stated: "new rule for all related tasks and tickets" reads as standing until he changes it.

**Family:** [[2026-09-20_ks1175-hold-lifted-make-the-fix]] (a card answered outside its options; recorded by hand) · [[2026-08-21_challenge-me-when-you-think-im-wrong]] (the privacy measurement goes back to him) · [[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (read the scope: audit + verification, not exports) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).

## RULED 2026-11-16 07:16:08 — Kam, live board (view=wednesday), verbatim: "Decision secuura-public-audit-personal-fields-1116: a — Public, with personal fields removed"
- The public read of an audit record does NOT carry the personal fields: `userId`, `ipAddress`, `userAgent` and the free-text fields (`details`, `previousState`, `newState`; `errorMessage` by Wednesday's reading of "free text"), and, by Wednesday's reading, a `resourceId` / `target_id` that names a person. The platform admin log counts as an audit record (Wednesday's reading, stated in the S 85th ANSWER; Kam may narrow it).
- Still OPEN with Kam (defaults = nothing changes): `secuura-verify-public-withheld-names-1116` (do verification's four withheld name fields open?) and `secuura-cert-verify-anyone-or-signed-in-1116` (does certification verify, which records a billing charge, open to anonymous callers?).

## RULED 2026-11-16 09:16:45 and 09:17:09 — Kam, live board (view=wednesday), verbatim: "Decision secuura-cert-verify-anyone-or-signed-in-1116: b — Anyone, including anonymous" · "Decision secuura-verify-public-withheld-names-1116: b — Open the names too"
- **Certification verify** (`POST /api/certifications/:id/verify`) opens to ANY caller, anonymous included. This SUPERSEDES card secuura-ks1699-verify-audience-1113 = c (signed-in only) for this route. PR 2225 (built on the signed-in reading) does not merge as written. **Still open, money (his class):** who an anonymous verify bills — card `secuura-cert-verify-anonymous-billing-1116` (rec a: no charge; default: the build seat opens the route with no anonymous charge and the PR does not merge until he taps).
- **Verification names** open to everyone: title, issuer, certifiedBy and the certifier's organisation id. This REVERSES card secuura-ks590-verify-disclosure-four-questions-1102 = a and row A16; PR 2138 (KS-590, builds the withholding) is OUT of every merge queue (B 188th told by ADDENDUM 1, 09:18); the older scope-scrub (`scopeTenantFields`) is build work under this ruling.
- The 07:16 audit-record ruling is untouched: personal fields stay out of PUBLIC AUDIT records. Names on a VERIFICATION are now public by his word; do not conflate the two.
- **RULED 2026-11-16 09:59:15 (live board, verbatim): "Decision secuura-cert-verify-anonymous-billing-1116: a — No charge for anonymous calls".** An anonymous certification verify records NO billing event; signed-in calls are billed as today. PR-V carries no money hold (W 32nd's ADDENDUM 1, 10:00).
