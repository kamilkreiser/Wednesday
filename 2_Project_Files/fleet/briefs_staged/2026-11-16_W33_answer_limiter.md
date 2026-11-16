Seat W 33rd

ANSWER: PR-V limiter shape (Seat W 33rd). RULED: (c). Move the anonymous limiter into the public mount in routes/proxy.ts, AFTER authenticateToken(false), skipping only when req.user is set: the same discriminator as the charge (D8). This SUPERSEDES the limiter-placement half of W33-R2 (index.ts with a Bearer/x-api-key skip); everything else in W33-R2 stands.

WHY: your reading is right and the hook was right. A skip keyed on the header's TEXT can be satisfied by a caller who is not signed in (lowercase bearer, junk Bearer, junk key), so it is a bypass of the anonymous allowance. Keying on req.user, after the same authentication the charge uses, counts exactly the callers the charge treats as anonymous. (c) also edits no shared census file and leaves the audit-mount pins alone. Your withdrawal of the x-api-key half is recorded; the error was in Wednesday's W33-R2 text, which named that skip, not in your build.

WHAT THE READY MUST SHOW (on top of your plan): (1) the counted cells you named (lowercase bearer, junk Bearer, junk key: each counted as anonymous; a signed-in caller and a valid sk_ key NOT counted), each red on a mutant that restores the header-text skip; (2) the ks1503 census and the audit-mount pins GREEN with no edit to either (quote their pass lines); (3) the two stated differences from W33-R2, as facts in the PR body: a junk Bearer now spends the anonymous allowance, and a 429 is answered after the audit middleware, so an over-limit anonymous call now leaves an audit row (say how many rows one over-limit call writes, measured); (4) the hook's final line verbatim on the real push.

Tier for the gate: TIER 1 (anonymous access + a rate limit on a public door). Kam's 09:59 ruling stands: no charge for anonymous calls.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-16 09:16:45 (live board, verbatim): "Decision secuura-cert-verify-anyone-or-signed-in-1116: b — Anyone, including anonymous".
- Kam 2026-11-16 09:59:15 (live board, verbatim): "Decision secuura-cert-verify-anonymous-billing-1116: a — No charge for anonymous calls".
- Kam 2026-11-16 11:12:46 (live board, verbatim): "Decision secuura-verify-names-personal-data-1116: a — Open the names, but not personal data".
