# Freshdesk hosting for QuickQuote — feasibility research

**Date:** 2026-08-28 · **Author:** Wednesday research agent · **Scope:** public docs only, read-only. Nothing logged into.
**Kam's question:** "Can I host the quick quote tool behind or on the Freshdesk infrastructure?" Plus the 2026-08-28 constraint: **OTP sign-in is removed; users sign in with the Freshdesk login they already have.**

## BLUF

Yes, in shape **(B) — behind Freshdesk**: Freshdesk becomes the front door and identity provider, the Node/Express app and its secrets stay on Azure. Shape **(A) — fully on Freshdesk** is *technically* possible only for agent-seat users, as a Freshworks "custom app" in the `full_page_app` placement with serverless (SMI) functions, but the platform's limits (20 s function timeout, 100 KB payloads, 40 KB key-value records, 50 calls/min, 100 MB object store, no documented headless-browser/PDF runtime, no documented mail-with-attachment primitive) make it a rebuild that fights the platform to reproduce PDF/CSV email, HPAM gating and Table-Storage persistence. It is **not** possible for portal contacts: end-user apps exist only as two ticket-page sidebars, with no full-page portal placement. Shape (C) (plain link) is the fallback if the account is on Free/Growth.

## Recommendation

**Shape B.** Keep QuickQuote on Azure App Service; delete the OTP flow; make Freshdesk the identity source.

- **If the users are Freshdesk AGENTS:** build a small custom app (private, free, no review, installs from Admin > Apps > Custom apps, up to 25 per account) using `full_page_app` so QuickQuote appears as an icon in the left nav and fills the viewport. The app's `server.js` (SMI) holds a secure iparam (shared secret / RSA key), mints a short-lived signed JWT for the logged-in agent (`loggedInUser.contact.email`, `role_ids`, `group_ids`) and hands it to the Azure app, which verifies it and opens a session. The HPAM margin gate keys off `role_ids`/`group_ids` **server-side on Azure**, so buy-price data never reaches the browser — same guarantee as today. Plan-tier precondition: custom apps are on every paid Freshdesk plan (UNVERIFIED for Free); no marketplace listing needed.
- **If the users are PORTAL CONTACTS (partners):** the app framework cannot help (no full-page portal placement). Instead use Freshdesk's Contact SSO: Freshdesk redirects to the Azure app's auth endpoint (JWT, RS256) — that endpoint becomes the only login, and QuickQuote is reached either from a portal nav link/custom-CSP-allowed iframe (Pro/Enterprise) or directly. Verified identity = the JWT your own endpoint minted, i.e. Freshdesk still trusts Azure, not vice versa; role gating uses contact company/tag fields fetched via the Freshdesk API with an API key held on Azure. **Precondition: Pro or Enterprise** (custom SSO policies for portals, portal layout/pages and CSP editing are all Pro+).
- "Freshdesk Support Desk" vs "Freshworks Customer Service Suite/Omni": same developer platform and same Pro/Enterprise gates; Omni's Growth plan is also excluded from portal customisation. No material difference for this decision.

## Detail

### A — Fully on Freshdesk (agent-only)
- **Placements:** `full_page_app` (left nav, full viewport, one active app), ticket/contact sidebars, backgrounds. Apps run in sandboxed iframes; SPA frameworks are fine (Freshworks' own blog shows React full-page apps). A 3k-line HTML/JS bundle is fine; print CSS works in the iframe (print-fit CI would need re-validation).
- **Serverless:** Node 18.18 (default manifest), functions triggered by product events, external events (webhook URL, 250/min, 100 KB), scheduled events, and SMI (`client.request.invoke`, 20 s timeout → 40 s if request timeout raised via Dev-Assist ticket, 100 KB payload, 50/min). Jobs: up to 2 min, 15 concurrent.
- **Secrets:** secure iparams are hidden from the front end; usable only via request-template header substitution `<%= encode(iparam.x) %>` and inside `server.js` (iparams injected into the payload). So the HPAM gate and Azure/ACS keys **can** stay server-side in shape A. Outbound HTTP must go through request templates (FQDN host, 15 s, 6 MB response, 50/min) — calling Azure/ACS is allowed.
- **Storage:** KV store 40 KB per key+value, 60-char keys, 50/min; entity store 20 fields/10 000 records/100 KB/250/min; object store 10 MB per file, 100 MB per app per account. Table-Storage-scale quote/feedback history does not fit; you would still keep Azure storage.
- **PDF/email:** no platform mail-with-attachment primitive; you would call ACS via a request template. No documentation of headless Chrome in the serverless runtime → server-side PDF rendering UNVERIFIED/likely infeasible; client-side PDF would have to be generated in the browser and pushed through 100 KB SMI payloads or the object store.
- **Cost:** custom apps free; developer account free (UNVERIFIED for account-creation prerequisites). Limits are extendable only by Dev-Assist tickets.
- **Verdict:** possible but a ground-up rebuild against tight quotas; not sensible for this tool.

### B — Behind Freshdesk (recommended)
- **Agents:** `loggedInUser` (via `client.data.get`) exposes `id`, `contact.email`, `role_ids`, `group_ids`, `occasional`. This is client-side data, so the *verified* artefact must be minted in `server.js` with a secure-iparam key (Freshworks' own "secure your middleware with JWT" pattern — page 403'd to the fetcher, listed UNVERIFIED but referenced in search). SMI docs do not state that the platform injects the caller's identity server-side — treat the email/roles as app-asserted and sign them; do not rely on them beyond what an agent seat already implies.
- **Contacts:** Contact SSO (SAML/OIDC/JWT, JWT = RS256, claims `sub`,`email`,`iat`,`nonce`, names) configured in the Neo Admin Center; custom SSO policies per portal are Pro/Enterprise. Portal pages accept custom HTML/Liquid/JS on Pro+ (JS with `nonce="{{portal.nonce}}"`, CSP `frame-src`/`script-src` editable), but there is no "new page" facility — only the 17 built-in pages/layout, so an embed would be an iframe inside an existing page or simply a nav link.

### C — Link only
Zero-build fallback: nav link in Freshdesk (agent nav or portal header) to the Azure URL; still needs Freshdesk SSO on the Azure side for the OTP removal.

### Constraint scorecard (this tool)
1. Secrets/HPAM gate: A keeps them server-side via secure iparams; B keeps them on Azure. Both OK.
2. Email PDF: A must call ACS via request templates, PDF rendering unresolved; B unchanged.
3. Auth: OTP → Freshdesk identity in both; agent case verified via app-minted JWT, contact case via Contact SSO JWT/SAML.
4. Persistence: A's stores are far smaller than Table Storage; keep Azure either way.
5. PDF: server-side only viable on Azure.
6. Cost: platform free; Pro/Enterprise plan is the real cost for the contact path.
7. Distribution: custom (private) app, admin-installed, no marketplace review; marketplace not needed.

## Sources (all read 2026-08-28)
- Rate limits & constraints (v2.3, Freshdesk): https://developers.freshworks.com/docs/app-sdk/v2.3/freshdesk/rate-limits-and-constraints/
- End-user apps (portal placements, SMI-only rule): https://developers.freshworks.com/docs/app-sdk/v2.3/freshdesk/end-user-apps/
- Placeholders incl. full_page_app: https://developers.freshworks.com/docs/app-sdk/v2.3/freshdesk/front-end-apps/placeholders/
- Request method / templates (v3.0): https://developers.freshworks.com/docs/app-sdk/v3.0/support_ticket/advanced-interfaces/request-method/
- SMI (v3.0): https://freshworks.dev/docs/app-sdk/v3.0/contact/serverless-apps/server-method-invocation/
- Jobs: https://developers.freshworks.com/docs/app-sdk/v3.0/contact/serverless-apps/jobs/
- App manifest (Node 18.18): https://developers.freshworks.com/docs/app-sdk/v3.0/common/front-end-apps/app-manifest/
- Custom apps (no review, 30 min): https://developers.freshworks.com/docs/app-sdk/v3.0/deal/app-submission-process/custom-apps/
- Entity storage: https://developers.freshworks.com/docs/app-sdk/v3.0/service_change/data-store/entity-storage/
- loggedInUser data method: https://developers.freshworks.com/docs/app-sdk/v3.0/support_email/front-end-apps/data-method/
- Community: request timeout 15→30 s via Dev-Assist: https://community.freshworks.dev/t/request-timeout-in-production-limited-to-15-seconds-how-to-extend-for-custom-apps/19518 ; serverless limits Q&A: https://community.freshworks.dev/t/a-few-questions-on-various-limits-with-freshservice-serverless-apps/13960
- Freshdesk pricing (Growth $19 / Pro $55 / Enterprise $89, portal customisation Pro+): https://www.freshworks.com/freshdesk/pricing/
- Advanced portal customisation (Pro/Enterprise, 17 pages): https://support.freshdesk.com/support/solutions/articles/50000010256-customize-portal-layout-and-pages-advanced-portal-customization-
- Portal CSP / nonce (Pro/Enterprise): https://support.freshdesk.com/support/solutions/articles/50000005660-configuring-csp-for-freshdesk-portal
- Custom SSO policies for portals (Pro/Enterprise): https://support.freshdesk.com/support/solutions/articles/50000010538-create-custom-sso-policies-for-portals
- SSO in Freshdesk (agents; all plans): https://support.freshdesk.com/support/solutions/articles/50000001658-single-sign-on-in-freshdesk
- Custom JWT SSO (agents + contacts, RS256): https://support.freshworks.com/support/solutions/articles/50000000670-how-to-configure-sso-with-custom-jwt-implementation-
- Third-party explainer (agent vs contact SSO): https://www.getmacha.com/blog/freshdesk-sso-explained ; https://www.eesel.ai/blog/freshdesk-portal-customization
- Search-only (not fetched, UNVERIFIED wording): "custom apps free to build/run" via https://developers.freshworks.com/docs/getting-started/paid-apps-program/ ; secure-iparams guidance via https://developers.freshworks.com/docs/app-sdk/v3.0/common/whats-new/
- Unreachable: Medium full-page-app and JWT-middleware posts (HTTP 403); several `developers.freshworks.com/docs/app-sdk/v3.0/freshdesk/...` and `/common/...` URLs (404 — docs moved to module paths); Freshdesk discussion topic 32317 (login redirect).

## Open questions for Kam
1. Which login do "the people who would access this tool" hold — Freshdesk **agent seats** or **portal contact** logins? This decides B-agent (custom app, any paid plan) vs B-contact (needs Pro/Enterprise).
2. What plan is Datasec's Freshdesk on (Free/Growth/Pro/Enterprise, Support Desk or Omni)?
3. Which Freshdesk role/group (agents) or company/tag (contacts) should unlock HPAM mode?
