BLUF. **The acceptance+security gate measured a LIVE DEMO BLOCKER on caf63fd** (INTERIM 09:23:04Z, DKIM pass; its mail is quoted below, not re-derived by Tuesday).
- Through the public URL, sign-in succeeds, but every API call after it is refused by the Caddy Basic gate. The app then shows "Your session ended".
- **Kam is testing the live site tonight**, so this goes AHEAD of the fix lanes for the SEAT. A subagent is fine; no lane pauses.
- **Kam is being asked now whether to apply fix (b).** Prepare and measure it; **do NOT apply it on Azure until Tuesday relays his word.**

## What the gate measured (its words, summarised; 09:11–09:16Z, replicated)
- The gate (Caddy, realm "restricted") needs HTTP Basic in the `Authorization` header on every request.
- The API accepts only `Authorization: Bearer <token>` (`apps/api/src/auth.ts:44`), and the web app sends exactly that (`apps/web/src/api/client.ts:23`; the live bundle `/assets/index-DL3hPt3N.js` carries it).
- One request has one Authorization header, so a request can satisfy the gate or the API, never both:
  - bearer without Basic: 401 from Caddy;
  - Basic without bearer: 401 from the API;
  - real Chromium: sign-in 200, then `/api/dashboard` and `/api/tenants` 401, then a redirect to `/sign-in?next=/`.
- Not load, not mid-upgrade: `/healthz` 200 "0.13.2", web bundle last-modified 08:55:57Z.
- **Why the upgrade post-checks missed it:** earlier live checks ran through the SSH tunnel. The public-URL checks tested only the 401 without credentials and the sign-in page 200. Nothing made an authenticated API call through the gate.

## The ask
1. **Reproduce through the PUBLIC URL, never the tunnel.** A real browser signs in as a synthetic persona and loads S1, and the failure is expected. Use only your own credentials and never print them.
2. **Prepare option (b):**
   - Basic auth stays on everything except `/api/*`;
   - `/api/*` is left to the API's own bearer check;
   - `/idp/*`, and `/idp/token` in particular, stays behind Basic, so tokens still come only from behind the gate.
   - Stage it on **pc-lane-a first**, with the exact rollback written down.
3. **Measure (b) through the gate on pc-lane-a, before Azure:**
   1. a browser sign-in, S1, and opening one engagement all work;
   2. the full list of what `/api/*` answers WITHOUT a bearer through the edge (openapi.json, the 401/404/405 bodies). **Any `/api` route that answers 200 with data and no bearer is a STOP: mail it and do nothing more;**
   3. `/idp/token` still challenges without Basic.
4. **Mail Tuesday a short READY-TO-APPLY** carrying 3.2's list, the rollback, and how long Azure is affected. Then wait for Kam's word, relayed by Tuesday.
5. **Regression check, from now on part of every upgrade post-check:** a scripted browser run THROUGH the public gate that signs in and loads S1. It must fail on today's configuration and pass after the fix.

## Not in scope tonight
- The durable redesign (a cookie gate or source-IP allowlist, or the API accepting a dedicated header) goes to BACKLOG for Monday. Mention it only if (b) proves unworkable.
- The tester's other live findings (missing security headers; Mailpit, MinIO and idp discovery reachable behind the gate) wait for its verdict.

## HOLDS
- Before any `az`: identity check. Never touch `datasec-sales-portal-rg`.
- No engagement or tenant you did not create is touched; Kam is testing.
- The rolling-upgrade rule stands: a head mail before any Azure change, and Tuesday warns Kam.
