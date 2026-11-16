Seat W 33rd

ADDENDUM 1 (Seat W 33rd): one MEASUREMENT added to your plan, before any product edit. It adds to your BRIEF and STAMP; it supersedes nothing in them.

Why: gate 374 (tier 1, on PR 2249, the names PR) measured with realistic write-side data that the verify answers' "names" carry personal data: `certifiedBy`/`issuer` is usually the certifier's EMAIL LOCAL PART (getUserFromRequest builds `name` from the part of the email before the @), and `certifierOrganizationId` is NOT an organisation id but the certifying USER's id (`certification_metadata.issuerId` = `req.user.userId`). Source: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-16_gate374-tier1-pr2249-ks590-names-open/verdict.md lines 8-29. Kam has a card open on it (secuura-verify-names-personal-data-1116, posted 10:5x, default: PR 2249 HELD).

YOUR ROUTE'S ANSWER carries `issuer: {id, did, verified: true}` (your BRIEF, "Originate verify handler (reading)"). PR-V opens it to ANONYMOUS callers. So, in your plan mail and before building:
1. MEASURE what `issuer.id`, `issuer.did` and every other field of the cert-verify 200 answer hold at the data layer (column, how the write side fills it; with realistic data, not a fixture's placeholder): is any of them a user id, an email or its local part, or another person's identifier?
2. Put the result in a table in the plan QUESTION: field | source column | what it holds | personal (yes/no).
3. If any field is personal, STOP at the plan: Wednesday puts it to Kam on the same card's terms before PR-V opens the route. If none is, say so with the measurement and proceed.

This is the 07:16 ruling ("Public, with personal fields removed") applied to the route you are opening. Kam 09:16's "Anyone, including anonymous" decided WHO may call; it did not decide that personal data goes with the answer.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-16 07:16:08 (live board, verbatim): "Decision secuura-public-audit-personal-fields-1116: a — Public, with personal fields removed".
- Kam 2026-11-16 09:16:45 (live board, verbatim): "Decision secuura-cert-verify-anyone-or-signed-in-1116: b — Anyone, including anonymous".
- As your BRIEF otherwise.
