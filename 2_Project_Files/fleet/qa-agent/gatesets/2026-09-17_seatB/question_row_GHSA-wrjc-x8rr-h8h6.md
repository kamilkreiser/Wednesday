SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: audit row GHSA-wrjc-x8rr-h8h6 react-router (Seat B)
TS: 2026-09-17T07:26:55.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CONTEXT
Row 11 of 15: GHSA-wrjc-x8rr-h8h6, react-router (KS-528). expires 2026-09-30, which lapses Wed 30 Sep 10:00 AEST.
- [G] medium: an open redirect via a backslash in <Link> / useNavigate (a CVE-2025-68470 bypass). Range >=6.0.0 <7.18.0; fixed ONLY in 7.18.0.
- [V] the v6 line has no fix: react-router 6.30.x ends at 6.30.6, still inside the range.
- Carried at 6.30.4 in frontend/admin, issuer and verifier, plus root. It ships in the three portal client bundles.
- Lead, not proof: 0 of the 48 `navigate(` calls in the three portals build a target from searchParams / redirect / returnTo / next / location.state. Instrument: a one-line git grep, narrow by construction; control: 48 navigate( calls found.
- A v7 migration is client source code in 3 portals (KS-528), outside my write scope.
- Row 13 (react-router-dom GHSA-jjmj) is separately fixable at 6.30.6 and is PR-5. It does not clear this row.

QUESTION
Which does Kam choose for row 11?
(a) Commission the KS-528 react-router v7 migration as source work (a seat with source scope). It will not land by Wed 30 Sep without a dated decision covering the gap.
(b) Record a dated decision for this row pending KS-528, with the reach lead above as its reason. That is Kam's call, not mine.
(c) Something else Kam names.
My recommendation: (a) and (b) together. Commission the migration, and date the row to its planned landing, so the fix has an owner and the date has a reason.

MEANWHILE
Continuing with PR-1 (hono) and PR-2 (colord).

NEEDED-BY
Fri 25 Sep to you. The row lapses Wed 30 Sep 10:00 AEST.

Seat B
