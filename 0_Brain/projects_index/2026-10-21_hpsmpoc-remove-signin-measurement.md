# HPSM-POC: remove sign-in -- measurement (read-only), main ec0a62a1

Card answered: `hpsmpoc-entra-signout-hint-1021`. Board words (verbatim, 2026-10-21 14:41:01 AEDT): "remove the need to authenticate all together.  Anyone with a link can access the site.  Also, please tell me if there are multiple login levels"
date start: Wed 21 Oct 2026 14:42:07 AEDT · date end: Wed 21 Oct 2026 14:44:21 AEDT
Instrument key: `ec0a62a1:<path>:<line>` = `git show/grep ec0a62a1` in the code repo (2_Project_Files). Nothing hosted, Azure or Entra was contacted.

## BLUF

1. **There are four sign-in levels plus one link-based level**: Admin, Consultant, Partner, Demo (Entra app roles carried in the access token), and Client (an unsigned follow-up link, its own scheme). Demo is already a read-only, synthetic-seed-only level.
2. **Auth is enforced twice and both are fail-closed**: the web server redirects every page but `/` and `/follow-up*` to sign-in and answers 401 to `/api/v1/*` without a session; the API independently requires an Entra JWT on every route (fallback policy) and is itself on the public internet. Removing the web gate alone does nothing useful: the web would still have no token to give the API.
3. **There is NO existing open or demo mode that works on the hosted site.** The API's Development sign-in refuses to start on App Service and in any non-Development environment; the web's mock sign-in is refused on a hosted server. Infra tests forbid `Auth__Development*` in the API settings. Any "no sign-in" is new code (and, for the cleanest shape, one Entra change that is UNMEASURED).
4. **Cheapest shape that honours the words and limits harm**: every visitor is treated as one fixed identity holding the Demo role (read-only, seeded synthetic customers, no audit, no admin, no feedback list). Feedback submit still works for Demo (it reaches the Jira-creating webhook, rate-limited at 5 a minute for the whole shared identity). Writes (Consultant/Partner/Admin) would be open to the world only under options (ii) or a non-Demo fixed identity.
5. **Hosted data**: seeded SYNTHETIC set, plus one hand-entered customer ("Acme Pty Ltd", no "(sample)" mark) and three internal Feedback rows (admin-only to read). The cleanup card `hpsmpoc-hosted-demo-data-cleanup-1021` was RULED **c (leave both)** at 14:42:52 (decisions.json). No HP Restricted material is recorded as being on the site (UNMEASURED against the live database).
6. Not recommended here; facts and costs only.

## 1. LOGIN LEVELS

Roles are defined once: `ec0a62a1:api/src/HpsmPoc.Modules.Assessment/Identity/Caller.cs:10-43`. Policies: `AssessmentModule.cs:150-157`, `FeedbackModule.cs:100-102`, `RulesModule.cs:29`.

| Level | How assigned | What it unlocks |
|---|---|---|
| **Admin** | Entra **app role** "Admin" on the API app registration (`infra/README.md:46`: roles Admin/Consultant/Partner/Demo) assigned to a user in Entra; arrives as the `roles` claim (`Program.cs:56-57`, `RoleClaimType = "roles"`). Roles copied to `app_user.last_roles` on first call/refresh (`Caller.cs:83,100,132`), but the TOKEN is authoritative. | Everything: all reads; all writes (`WritePolicy`); audit read (`AuditPolicy`); metrics + attribution preview (`MetricsSummaryPolicy`); **resetDemoData**, **personal-data export and erasure** (`AdminPolicy`, `AssessmentModule.cs:228-231`); **Feedback list + attachment download** (`FeedbackModule.cs:165-166`); sees ALL customers (`Caller.cs:51`); full ruleset provenance (`ProvenanceView.cs:16`). Web: Admin nav + "Reset demo" (`GlobalNav.cs`-equivalent `GlobalNav.tsx:37`, `AppShell.tsx:113`). |
| **Consultant** | Entra app role "Consultant". | All reads, all writes, audit read, metrics, sees ALL customers, full provenance. NOT: reset demo, personal data, feedback list. |
| **Partner** | Entra app role "Partner". | All reads and writes **but only on customers it owns** (`CustomerScope`, `Caller.cs:210-226`); audit read; NOT metrics (`Caller.cs:28` "the dashboard is Datasec's"); no admin. |
| **Demo** | Entra app role "Demo". | Reads only (`ReadRoles`, `Caller.cs:42`); **seeded synthetic customers only** (`SeedKey is not null`, `Caller.cs:217,238`); metrics + attribution preview; **may submit Feedback** (`FeedbackModule.cs:101`, `RequireRole(Roles.All)`); no writes, no audit, no admin, no feedback list. |
| **Client** | **Not an account.** An unsigned follow-up link (token) opened by `POST /api/v1/client/session` (`AllowAnonymous`, `AssessmentModule.cs:277`), its own `FollowUpLink` scheme; no other policy accepts it, and it is refused (403) on every path but `/api/v1/client` (`Program.cs` `UseFollowUpLinkIsolation`, `AssessmentModule.cs:38-40` comment). Web pages `/follow-up*` are open without sign-in (`proxy.ts:65-69`). | Answer its own follow-up questions and complete them (`ClientFollowUpEndpoints`, `AssessmentModule.cs:278-281`). **This is the one existing "anyone with a link" precedent in the product.** |

A user holding several roles is shown as the highest (`entra.ts:43-45`). No seed users exist in the API; the only seeded identity is a synthetic **seed owner** for the demo data (`HostedDemo.cs:40-45`, label "Demo presenter (synthetic seed owner)", real Entra object id supplied by infra param). Mock/laptop sign-in picker offers the same four roles (`page.tsx:24`). The Development header sign-in (laptop only) accepts the same four (`DevelopmentAuthentication.cs:67`).

Role assignment mechanics (which humans hold which role in the hosted tenant) is **UNMEASURED** (needs Entra read; fenced).

## 2. HOW AUTH IS ENFORCED TODAY

**Web (Next.js server, which is also the BFF)**
- `resolveAuth` (`web/src/server/auth/config.ts:48`) yields `mock | entra | off`. With no Entra settings on a **hosted** server (`WEBSITE_SITE_NAME`/`WEBSITE_HOSTNAME`/`IDENTITY_ENDPOINT`, line 52) it returns `off` (fail closed, "the mock sign-in is refused"); `off` = sign-in and every API call answer 503. Hosted demo sets `AUTH_ENTRA_TENANT_ID`/`CLIENT_ID` etc. (`infra/modules/appservice.bicep:199-200`) so it runs `entra`.
- Page gate: `needsSignIn` (`web/src/proxy.ts:65-70`): in `mock` no gate; `/`, `/follow-up`, `/follow-up/*` open; everything else needs `readSession`. Unsigned page request is 307 to `/?next=<validated path>` (`proxy.ts` B377-3 block). Static assets, `/api/*` and the health probe are outside the matcher.
- API calls: `bff.ts` (~lines 395-420): `off` is 503 `api-off` (line 403); with Entra, no usable session is **401 `signin-required`** (line 414) and the session's access token is forwarded as `Authorization: Bearer` (line ~130 of that segment). CSRF/size/content-type guard on every mutation (`guard.ts`).
- Auth routes: `/api/auth/signin`, `callback/microsoft-entra-id`, `session`, `signout` (`web/src/app/api/auth/**`); `routes.ts` answers 404 in `mock`, 503 in `off`.
- `[auth]` log lines are `console.warn` reasons only (`entra.ts:210,215,230,260,322-333`; `config`/`routes.ts`); a startup `[auth]` line was not found at ec0a62a1 by name (grep of `[auth]` returns only those warn sites; positive control: the grep did hit them). The sign-in redirect `/?next=` is `proxy.ts` (above) and `returnPath.ts`.

**API (ASP.NET Core)**
- `AddJwtBearer` Entra (`Program.cs:47-59`), audience = API app id, roles from `roles`; **fallback policy RequireAuthenticatedUser** (`Program.cs:64-65`). Anonymous routes in the whole API: `/health`, `/health/ready` (`Program.cs:140-141`), `GET /api/v1/rulesets/schema-version` (`RulesModule.cs:36`), `POST /api/v1/client/session` (`AssessmentModule.cs:277`). Every other route carries a role policy.
- `CallerFilter` (`Gate.cs:25-47`) resolves the principal to an `app_user` row (creates on first call, `Caller.cs:93-112`); a missing/unauthenticated principal yields null (route is already refused before that).
- Both apps have `publicNetworkAccess: 'Enabled'` (`appservice.bicep:71,165`); no `ipSecurityRestrictions` appears in the bicep (grep zero; positive control: the same grep hit the `publicNetworkAccess` lines). So **the API is directly reachable from the internet**, protected only by the JWT.

**Existing switches for an open/demo mode**
- API `Auth:Development:Enabled` (`DevelopmentAuthentication.cs:36-46`): off by default; throws at startup if on with a hosting-platform marker (line 31, 44) or outside Development (line 52); loopback callers only; infra test forbids `Auth__Development*` (`infra/tests/test_security_baseline.py:294`). **Cannot be used on the hosted site by config.**
- Web mock sign-in: only when no Entra setting and not hosted (`config.ts:52-54`). **Refused on hosted by design** (gate B63 F-3).
- Web `HPSM_API_DEV_AUTH_HEADER/VALUE` forwards a static dev header to a **loopback API only** (`bff.ts` resolveMode; `config.ts` also returns `off` if combined with Entra).
- Searches for `open mode`, `AUTH_DISABLED`, `DEMO_OPEN` at ec0a62a1: zero (positive control: `AllowAnonymous` hit 4 sites). `git log -S AllowAnonymous` shows only the commits that introduced the client follow-up and health/rules routes (a8c165a, 4ee5a31, 62eb89d). **No prior implementation or revert of an open mode.**

**Prior rulings (records repo `datasecau/HPSM-POC-analysis` listing read via gh api; CLARIFICATIONS read from the local project copy, 157 lines, ends at C-48-era text)**
- Local `CLARIFICATIONS.md` line 62 / 67 (verbatim): "Decision hpsmpoc-dev-signin: a — Keep it (four locks)" and "the Development-only sign-in stays (four locks); missing ids keep returning 404; the Partner role sees only its own customers."
- Line 24: the Entra tenant and subscription host Dev/UAT/Demo (tenant/sub ids not assumed).
- Line 87: "Seats still never copy HP Restricted material (the exec deck, the financial model)."
- The local CLARIFICATIONS copy does not reach the later hosted C-numbers (the bicep cites C-59 for the forwarded-address ruling, `infra/env/demo.bicepparam`), so rulings C-49 onward on hosted sign-in are **UNMEASURED here** (not in the local file; would need the records repo's current CLARIFICATIONS blob).
- Cards (decisions.json): `hpsmpoc-entra-signout-hint-1021` open, default c; `hpsmpoc-hosted-demo-data-cleanup-1021` ruled c at 14:42:52 (overriding the default recommendation a).

## 3. WHAT AN UNAUTHENTICATED VISITOR WOULD REACH

Assume sign-in removed and the visitor is treated as a fixed identity. What it reaches depends on that identity's role (section 1); the worst case is Admin/Consultant.

**(a) Data on the hosted site.** The API seeds a SYNTHETIC set at startup (`HostedDemo__Seed__Enabled=true` for demo, `appservice.bicep:136`; label "hosted demo seed (SYNTHETIC)", `HostedDemo.cs:162`). Card `hpsmpoc-hosted-demo-data-cleanup-1021` (decisions.json, B377 08:00): first row of the customer list is a **hand-entered "Acme Pty Ltd" with no "(sample)" mark** (its own PDF calls it synthetic), and Admin > Feedback holds **three internal rows** (a deploy-test note with a commit id, an earlier remark from the owner, a raw customer-id address). **Ruled c, leave both, 14:42:52.** Nothing from HP or a customer is recorded as being on the site; the only HP-derived material in the project is under the Restricted hold (`CLAUDE.md:87`: seats never copy HP Restricted material, i.e. the exec deck and financial model) and those files are not read by anything the app loads (UNMEASURED against the live database and report store). Real HP people are not users of the site as far as the files say (UNMEASURED). The Demo role sees only seeded rows (`SeedKey != null`), so the hand-entered customer is **hidden from Demo but visible to Admin/Consultant**. The feedback rows are visible only to Admin.

**(b) Write routes** (all `WritePolicy` = Admin/Consultant/Partner unless noted; `AssessmentModule.cs:196-281`): create/update/delete customer, put customer profile, create assessment, put/clear response, add evidence reference, submit (scoring), finding disposition, create/update/discard action plan and items, generate narrative (Azure OpenAI call, rate-limited), review narrative, generate report (PDF + blob write), follow-up create/revoke/review (issues client links), `ensureSelfCustomer`, `POST /showcase/reset`. Admin-only writes: `POST /admin/demo/reset`, `DELETE /admin/users/{id}/personal-data`. Imports (`/customers/{id}/imports` multipart upload, 5 routes) answer **404 `import.off` on hosted**: `Assessment:ImportsEnabled` is false in `appsettings.json:17` and infra never sets it (grep zero; positive control: `appsettings.Development.json:15` is true). Demo can write nothing except feedback submit. Web has no write route of its own beyond the BFF proxy and `/api/auth/*`.

**(c) Routes acting outward with the project's credentials.**
- **Feedback submit** `POST /api/v1/feedback` (+ multipart attachments up to ~20 MiB): hosted route is `automation` (`appservice.bicep:124`), i.e. it posts to a webhook URL held in Key Vault (`Feedback__Automation__WebhookUrl/Token`, lines 125-126) that creates the Jira ticket (route per the card text and `FeedbackDispatcher`); anonymous spam would create tickets. Limit: `SubmitPerMinute` = 5 (`FeedbackModule.cs:48`), keyed per caller (`Key(http)`, line 191) held in process memory (comment line 175), so **a single shared identity = 5 submissions a minute for the world, in total**, per API instance (2 instances = 10). A shared identity also means one abuser can starve everyone else's feedback (denial of the feature, not of the site).
- **Generate narrative** calls Azure OpenAI with the API's managed identity (`appservice.bicep:110-116`, deployment capacity 10 k TPM in `demo.bicepparam`): cost and abuse surface, rate-limited (`NarrativeRateLimit`, `AssessmentModule.cs:134,258`). Write role only.
- **Generate report** writes PDFs to blob storage (managed identity). Write role only.
- Client follow-up link issuing: write role only.
- Mail (Graph) is NOT wired on hosted demo: route `automation`, not `rest` (`appservice.bicep:122-124` comment: `rest` would add Jira/Mail settings). Mail sink exists in code (`JiraRestMailSink`) but is off hosted.

**(d) Secrets, tokens, identities, audit.**
- Secrets/tokens: none are returned by any route; the BFF keeps the session token server-side and `/api/auth/session` returns name + roles only (`entra.ts:269-273`, `routes.ts`). The webhook URL/token are Key Vault references and logged nowhere (`FeedbackModule.cs` `RemoveAllLoggers`). `/health/ready` returns no detail to anonymous callers (`AssessmentModule.cs` readiness doc).
- User identities: `app_user` holds the token's display name and preferred_username (the only personal data kept, `Caller.cs:62`); exposed to **Admin only** via personal-data export, the Feedback list (`SubmittedBy` user id and roles, `FeedbackEndpoints.cs:27`) and `/me`. Under a shared Demo identity nobody's name would be new data (the one row is the shared account).
- Audit log: `GET /assessments/{id}/audit` is Admin/Consultant/Partner only (`AuditPolicy`); a Demo identity cannot read it. Audit actor ids are uuids, never names.
- **Direct API exposure**: if auth is relaxed **in the API** (not just the web), the API host (`app-hpsmpoc-api-demo-*`, public) is reachable without going through the web gate, the CSRF guard, the BFF's size caps, or the web's rate behaviour.

## 4. OPTIONS (facts and costs; no recommendation)

Common constraints: the API validates a real Entra JWT, so the web BFF must obtain a token for some principal; the Development sign-in cannot run hosted (section 2); infra tests `test_security_baseline.py:294` and `rule_web_settings` pin settings and would need updates; the sign-out finding of the card becomes moot (no sign-out) but `/api/auth/*` stays for the Client-free path.

**(i) Config/code flag: every visitor is signed in as ONE fixed identity (recommended role if chosen: Demo, the only read-only level).**
- Shape A (token-based, API unchanged): new web env flag (e.g. a hosted "open demo" mode) makes `needsSignIn` false and has `bff.ts` obtain a **client-credentials/managed-identity token** for a service principal that holds the **Demo** app role on the API registration; `/api/auth/session` returns a fixed "Demo (shared)" view. Files: `web/src/server/auth/config.ts` (new mode, ~40 lines), `entra.ts` (token fetch, ~60), `proxy.ts` (gate, ~5), `bff.ts` (bearer source, ~15), `routes.ts` and `AppShell.tsx` / `entra-session.ts` (no sign-in/out UI, ~30), tests, `appservice.bicep` + `test_security_baseline.py` (new setting). **Code, plus one Entra change**: assign the Demo app role to the web managed identity or a new app on `hpsm-poc-api-demo` (UNMEASURED whether the registration's role has `allowedMemberTypes` including Application; if not, the manifest edit is needed; identity must be the project's own, see CLAUDE.md fences).
- Shape B (API-side handler): new scheme in `Program.cs`/`Auth/` that authenticates every request as a fixed Demo principal when a hosted flag is on. Files: API `Auth/*.cs`, `Program.cs`, startup guard, security tests, bicep. Exposes the **API host directly** (public), no web in front; the largest blast radius per line of code.
- Reversal: remove the setting and redeploy (config-only to turn OFF once the code is in; the code itself stays dormant). Needs the push-to-demo grant and a deploy before the 23:59 freeze tonight, a backup and live check (B402 shape).
- Exposes (section 3): Demo-visible seeded synthetic customers; reads, metrics; **feedback submit to Jira with a shared 5/min limit**; nothing writes elsewhere; no audit/admin/feedback list; the hand-entered customer and internal Feedback rows are not visible to Demo.

**(ii) Everything anonymous (`AllowAnonymous` + fallback policy removed, no identity).**
- Not a config change: `CallerFilter` needs a Caller (it returns null for an unauthenticated principal) and every handler reads `CallerAccess.Get(http)`, so some synthetic caller is still required; i.e. it collapses into (i) Shape B with a role of your choice. If the role is Consultant/Admin: all of section 3(b)-(c) is open to the world, including **Reset demo, personal-data erase, narrative generation (Azure OpenAI spend), report/blob writes and feedback-to-Jira**, on a public API host. Files: as Shape B plus every policy. Reversal: code revert + redeploy.

**(iii) Anonymous read-only, writes still signed in.**
- Same plumbing as (i) Shape A/B for reads (Demo is already exactly "read-only" at the policy level), while the Entra sign-in stays available on the web for Consultant/Partner/Admin: the web decides per request (session present = that user's token; absent = the shared Demo token). Extra over (i): keep `/api/auth/*`, keep the sign-in screen, UI shows "Sign in for edit". Files: (i) plus `AppShell.tsx` and screen gates (about 3-5 more web files). Reversal as (i). Exposure equals (i) for visitors; signed-in users retain today's powers. Today's sign-out finding (account picker) still applies to the people who do sign in.

**Not an option from the measurements**: flipping an existing flag (none exists, section 2); reusing mock mode on hosted (refused by design); the Development header sign-in (blocked by startup guards on the platform).

## FOUND / TESTED / HOW / NOT TESTED

**FOUND**
- Five levels (Admin, Consultant, Partner, Demo via Entra app roles; Client via link) with the policy matrix in section 1.
- Two independent enforcement layers (web redirect/401 and API JWT), fail-closed, no open mode, and explicit guards forbidding the Development sign-in hosted.
- API host is publicly reachable; Imports are off hosted; feedback goes to a webhook (Jira), mail is not wired hosted; Demo cannot read audit, admin, or the feedback list.
- The data-cleanup card is ruled c (14:42:52); the signout card is still open with default c.

**TESTED**
- Nothing was executed against any host. Code claims were read from the pinned commit; absence claims carry a positive control (AllowAnonymous grep found 4 sites; `ImportsEnabled` grep found the Development value; `publicNetworkAccess` grep found its lines; `[auth]` grep found the warn sites).

**HOW**
- `git --no-optional-locks -C <2_Project_Files> show/grep/log/ls-tree ec0a62a1 -- <path>` through a read-only wrapper script; one `gh api` GET of the records repo tree listing; local reads of CLARIFICATIONS, the pickup (first ~400 lines), the 2026-10-21 daily note and the card store (decisions.json) for the two cards; no Source_Documents or HP Restricted file was opened.

**NOT TESTED / UNMEASURED**
- The hosted site's live state: build id, actual rows in the hosted database, whether HP-derived content exists there, Key Vault webhook target (Jira project / any other recipient), instance count.
- Who holds which Entra role in the hosted tenant; whether the API app registration permits assigning the Demo role to an application (managed identity) rather than a user.
- Whether the hosted web returns the exact 401/307 shapes (read in code only).
- C-numbers after the local CLARIFICATIONS copy's last entry (including any later ruling on hosted sign-in); the records repo's current blob was not read.
- Cost of the Azure OpenAI deployment past the 10 k TPM capacity and the Jira-ticket rate the webhook can absorb.
- Behaviour of the 5/min feedback limiter across two API instances and under the shared-identity abuse pattern.
