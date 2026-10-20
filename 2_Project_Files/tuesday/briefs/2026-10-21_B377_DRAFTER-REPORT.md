# B377 drafter report (Tuesday s131 drafter, 2026-10-21 ~07:2x-07:4x AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B377_SEAT-Q1_hpsmpoc-hosted-reviewer-walkthrough.md`. Two stamp slots to fill: `DEPLOYED_BUILD_ID` and `STAMP_AUTHORITY` (both on one line; the refusal count reads 1 line, 2 matches; after stamping it must read 0). Launch line is B367's with `opus`, pane `Datasec/HPSM-POC-Q1`.

## Questions for Tuesday / Kam (each with my recommended answer)
1. **How will HP actually sign in, and which role?** The only records route to the hosted web is C-70's demo Entra user (role Admin, MFA with a registered authenticator, secrets only in `4_Credentials/.env`). I found NO record that chose a reviewer access route for the hosted web on 2026-10-03: C-41 and C-45 of that date are the D-9/D-10 database steps and the Security Manager VM. Recommend: Kam decides the HP account, role and MFA onboarding BEFORE the handover; the seat walks as demo Admin and reports sign-in friction as V1; do not let the seat try other accounts. If a 2026-10-03 route exists in a file I did not find, point the seat at it in the stamp.
2. **May the seat open `/customers/<id>/narrative`?** B316 and B366 held "no narrative opened" (it may trigger an AI call). An HP reviewer will certainly open it. Recommend: skip in B377 (brief rule 4), and have Tuesday ask a separate card whether a read-only GET of a stored, approved narrative is safe; the walk then lists it as a coverage gap, not a silent omission.
3. **Admin is not view-only (C-70). Accept the demo Admin as the walking identity?** Recommend yes, with the client-side fence that aborts every non-GET to `/api/` except `/api/auth/*` and a control that must fire first. It is stricter than B366's visit and it is the only credential that exists.
4. **Hold deploys and PR merges to deploy during the walk?** Standing grant C-71/C-105 lets another seat deploy. Recommend: Tuesday holds hosted deploys for the 120-minute window and says so in the stamp; the seat records the build id at start, mid and end regardless.
5. **Scope: this site only, or also the Security Manager VM and the FTA review Static Web App (`calm-smoke-080e4e200.3.azurestaticapps.net`, C-66)?** Recommend this site only; if Kam will hand HP those two as well, draft separate briefs (different access, different tenants of risk).
6. **Is `main` `fa8416d` (tests-only #166) acceptable as the source for code-area hints while hosted runs `6818896`?** Recommend yes: the compare shows only two test files, so web source is identical. The brief tells the seat to use a tarball at either sha and say which.
7. **Time-box 120 minutes and a 300-page-load cap: right size?** Recommend keep; 50 routes x 2 loads is 100, plus viewports, plus journeys.
8. **Should wording findings propose replacement text?** Recommend no (brief says quote and locate only): new customer-facing words need Kam's approval on records.
9. **Does Tuesday want screenshots to hold the demo user's name?** Recommend no; the brief makes the seat mask or crop any address and leak-scan the evidence.

## What I could not verify (UNMEASURED)
- Nothing on the hosted site: I made no HTTP request (per fence). So the hosted build id today, whether the site is up, whether `/design-system` and `/follow-up` are public, the real sign-in screens and the time they take, and every page's behaviour are unmeasured. Hosted `3cBXgbJ5OOq2IZ-rmpNUZ` = `6818896` is RELAYED from B366 STATUS (`:1`, `:342`), not re-read.
- Whether the demo user's password, TOTP secret and registered authenticator still work (the three env NAMES are present, MEASURED by a name-only pattern match; I printed no value; this means I did read `.env` for names, which is outside "never open `.env`" in a seat brief but within my read-only drafter fence; no value left my process).
- Whether Playwright and axe-core are installed in the project's `web/node_modules` (the project root checkout has a `web/node_modules`; `.tools/ms-playwright` holds `chromium-1243`, MEASURED by `ls`; `signin256.cjs` ran under node v26.8.1 at B366, RELAYED). The root checkout is STALE (its `web/src/app` has 3 files plus an api folder), so I took routes from `gh api …/git/trees/6818896b…` (1,534 paths, 50 `page.tsx`, 5 `route.ts`, MEASURED) instead.
- Whether a UAT copy (C-52) was ever stood up and which URL HP would be given: the records show the plan and Kam's "yes", not a built UAT site. I wrote the brief for the demo host only.
- Whether the "Reset demo" wording (POC-12, "the offline demo") was fixed; whether branding is still undecided (RELAYED from `design-system.md:5`, 2026-09-23, old).
- The demo script (`1_Project_Definition/Demo/2026-09-23_demo-story-and-7min-script-v0.md`) was NOT read; the brief uses the M2 review guide's journey map instead (read, 60 lines; it describes the old mock prototype, so the brief says to treat it as a map, not truth). `design-system.md` read for its first 30 lines only (104 lines total).
- HP's reviewer role (Admin, Consultant or Demo) and how HP gets MFA.
- B370 (records for the deploy) last line: `RECORDS COMMITTED: ae7cdced… 1 C-entries, 0 tickets, 3 comments, 2 Done` (RELAYED, tail only); I did not read it whole, so a records ruling about what HP sees could exist that I missed (the brief tells the seat to search for one under PRIOR WORK).
- I did not re-read `CLARIFICATIONS.md` whole: I pulled it by `gh api` GET (2,009 lines on main at ~07:25, scratchpad copy) and searched by pattern; C-70 and C-45 were read in full, the rest by hits.

## Measured by me (read verbs only)
- Main `fa8416de…` (`ls-remote`); `compare 6818896...fa8416d` ahead 1, two test files only; recent commits list shows #166 merged 2026-10-20T20:00:59Z.
- Hosted deploy facts relayed from B366 STATUS: URLs, health endpoints, imports OFF, 6 sample customers, 3 feedback items, PDF sha256 and size, the sign-in script and its three env names.
- B377 is free (no `B377` file in either `Briefs/` folder).
- Load at 07:24: 2.50 / 5.37 / 6.71.
