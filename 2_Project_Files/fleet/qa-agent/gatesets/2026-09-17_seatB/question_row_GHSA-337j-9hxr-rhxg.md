SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: audit row GHSA-337j-9hxr-rhxg react-router (Seat B)
TS: 2026-09-17T07:26:59.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CONTEXT
Row 12 of 15: GHSA-337j-9hxr-rhxg, react-router (KS-528). expires 2026-09-30, which lapses Wed 30 Sep 10:00 AEST.
- [G] medium: arbitrary constructor injection via deserializeErrors() in React Router SSR hydration. Range >=6.4.0 <7.18.0; fixed ONLY in 7.18.0 (major, the same migration as row 11).
- Carried at 6.30.4 in frontend/admin, issuer and verifier, plus root (client bundles).
- Lead toward unreachable-by-construction: the portals use `BrowserRouter` (9 hits) and none of the data-router or SSR APIs that feed hydration data to deserializeErrors. createBrowserRouter, RouterProvider, hydrationData, __staticRouterHydrationData, StaticRouter, createStaticHandler and renderToString each read 0 across frontend/{admin,issuer,verifier}/src. Instrument: git grep -F per name; control: BrowserRouter 9. I have not read react-router's own source to confirm deserializeErrors is only on that path.

QUESTION
Same decision as row 11, asked per row as the brief requires. Which does Kam choose for row 12?
(a) Commission the KS-528 v7 migration.
(b) Record a dated decision pending it, with the reach lead above as its reason.
(c) Something else Kam names.
My recommendation: the same as row 11. This row's reach lead is stronger (no SSR at all).

MEANWHILE
Continuing with PR-1 (hono) and PR-2 (colord).

NEEDED-BY
Fri 25 Sep to you. The row lapses Wed 30 Sep 10:00 AEST.

Seat B
