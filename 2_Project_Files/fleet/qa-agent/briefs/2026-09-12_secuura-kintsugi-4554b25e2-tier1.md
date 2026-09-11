# QA GATE BRIEF — Secuura/Blockchain: the KINTSUGI DEPLOY of develop `4554b25e2` — TIER 1 (a deploy to dev), ROUND 1

**Charter — read first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

## WHY TIER 1, AND WHAT THIS GATE CAN AND CANNOT REACH
- **Tier 1 because it is a DEPLOY TO DEV** (the 2026-09-05 tiers: anything deploying to dev or demo takes the full gate). **Round 1.**
- **The subject is the RUNNING BOX, not a PR.** Kintsugi (Secuura's dev VM, public at `https://kintsugi.secuura.net`) was moved from develop `0f8fb33c3` to develop **`4554b25e21dfd01113bf40e8f6d34573345a5f37`** by the Secuura agent s187, on 2026-09-11 22:16-22:21Z. Demo was not touched.
- **You have NO credential for kintsugi and NO shell on it.** So this gate is **unauthenticated, from outside**: rendered pages in a real browser, public HTTP contracts, and the through-code link from the deploy to its gate records. **Every authenticated flow is NOT TESTED, and says so.** Creating a QA login on kintsugi would be a credential change on a running system; that is Kam's call, not yours or Wednesday's.
- **The four frontends (admin, issuer, verifier, website) were NOT swapped** — they rebuilt byte-identical. **What changed is BACKEND, behind the same pages.** A regression you find on a page therefore comes from a changed service underneath it.

## TARGET — what was deployed (s187's report, relayed; you cannot read mail)
- **Swapped (25):**
  - behaviour changes: `anchoring`, `api-gateway`, `auth`, `originate`, `security`;
  - the shared package changed in comments only (#785), which rebuilt 16 backends plus `guardian`, `queue` and `demo-service`;
  - `nginx-gateway` (a stale config bake replaced; it serves a bind-mounted file either way).
- **Deployable PRs in the range `0f8fb33c3..4554b25e2`, by service** (s187's per-image table):
  - anchoring: #728 (KS-671, chain reachability read from real calls);
  - api-gateway: #951 (KS-1041 Step 2, the gateway vouch — shipped INERT: `GATEWAY_VOUCH_SECRET` is unset by ruling) and #935 (KS-1057, verify confidence no longer presence-keyed);
  - auth: #872 (KS-732, disabling MFA needs proof of possession), #878 (KS-942, the four public wallet routes stay open), #929 (KS-943, a 0-row UPDATE is not success);
  - originate: #951, #936 (KS-1058), #954 (KS-597 option B, caller-scoped externalRef), #808 (KS-663, documentUuid v4 constraint published);
  - security: #773 (a test file);
  - compose: #951 (the vouch lines), #896 (an `ADMIN_USER_PASSWORD` pass-through).
- **s187's own verification, 39/39 (author evidence — falsify what you can reach):** `/health` 200 JSON · `/originate/health`, `/originate/api/documents`, `/originate/` 404 with no `"path"` field · the new code present inside the containers · the vouch key present-and-empty · wallet separation · the served spec's sha16 `343d694157771e1d`.
- **Wednesday's own public reads, 08:25-08:34 AEST:**
  - `/` 200 `text/html`;
  - `/admin`, `/verify`, `/status`, `/website`, `/showcase`, `/pricing` and `/api/docs` 301 to their trailing-slash forms;
  - `/health`, `/health/deep`, `/health/ready` 200 JSON;
  - `/originate/health` and `/originate/api/documents` 404 JSON;
  - `/system/`, `/webhooks/`, `/analytics/` 404 JSON.
- **Repo READ-ONLY:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. Clone `4554b25e2` by SHA into your own scratch for every code read.

## WHAT THIS GATE MUST ESTABLISH
1. **The box is up and says so honestly.**
   - Read `/health`, `/health/deep` and `/health/ready` whole (key names and statuses; no values that look like secrets).
   - Any service reported not-ready or degraded is a finding. Say whether `degradedReasons` or the anchoring reachability fields are exposed publicly; if not, that half is NOT TESTED with the reason.
2. **The KS-1041 closure still holds, and the vouch control is inert.**
   - The three `/originate/...` probes return 404 with no `"path"` field.
   - **Forgery check (GET only):** on one public, unauthenticated `/api/` read route you choose from the code, send the request with and without forged trust headers (the vouch header name from #951, plus the identity headers `TRUST_HEADER_PATTERN` covers). The responses must not differ in authority.
3. **Rendered surfaces, in a real browser** (the QA project's default driver):
   - pages: `/`, `/admin/`, `/verify/`, `/status/`, `/website/`, `/showcase/`, `/pricing/`, `/api/docs/`;
   - for each: it renders (screenshot), console errors listed, and every page-load `/api/*` call with its status;
   - **a 5xx, a blank render or a broken asset is a finding.** A login FORM rendering is enough — never submit real credentials.
4. **Unauthenticated contracts on the changed services.** Use nonexistent identifiers only; at most 5 requests per endpoint; no account, no upload, no anchoring.
   - **auth login:** a nonexistent address on `example.invalid` with a wrong password returns a 4xx JSON error, never 5xx. **At most 2 attempts in total** — never approach a lockout.
   - **KS-732:** the MFA-disable route with no token returns 401.
   - **KS-942:** the four public wallet routes (read their paths from #878 in your clone) answer without authentication as that PR says.
   - **KS-1057:** the public verification endpoint, with a random nonexistent document id, must never answer verified or on-chain, and must not 5xx.
   - Anything that needs a real document, token or account is NOT TESTED, with the reason.
5. **The served spec equals develop's.** Fetch the spec behind `/api/docs/` and compare it, by hash, with the spec file at `4554b25e2` in your clone.
6. **Every deployed behaviour change has a gate record** (through code).
   - For each PR listed under TARGET, find its QA verdict in `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/`, or say none was found and what you searched.
   - **A deployed change with no gate record is a finding** (a coverage gap, not a verdict on the code).

## NOT COMMISSIONED — said before running
- Any authenticated flow · the wallet / KS-535 check · the database and migrations · container internals · anchoring writes.
- **Demo, in any form.**
- Load or rate-limit testing.
- Fixing anything.

## KNOWN-FRAGILE
- Kintsugi is a box Stuart uses. Probe lightly. **If a route returns 429, stop probing it and report.**
- `/zzz-nope/`-shaped unknown paths return 200 `text/html` (the SPA fallback) — **a 200 on a page is not proof the page exists**; check the rendered content.
- 🔴 **Your tool shell's `grep` may be a SHELL FUNCTION.** Use `/usr/bin/grep`, case-insensitive for prose, with a same-file positive control.
- zsh:
  - no `PIPESTATUS`;
  - unquoted list variables do not word-split;
  - an unmatched glob aborts;
  - `echo ======` aborts.

## BOUNDS
- **Findings only:** no fix, commit, push, merge, deploy, comment or ticket. No contact with Peter or Stuart.
- **NEVER create an account, log in with real credentials, or upload anything to kintsugi.**
- **NEVER touch demo.**
- **NEVER print a credential value**, and never open, read or copy a secrets file (any `.env`, `config/secrets.yml`).
- No ssh. **Never `rm`**: a fresh `mktemp -d`, every expansion guarded `"${X:?unset}"`.
- **No memory maintenance inside this gate session.**
- **Checkout readings** from the Secuura checkout, read verbs only, at start and at end — they must match:
  - `git --no-optional-locks status --porcelain | wc -l`;
  - `shasum -a 256 .git/config`;
  - `git for-each-ref | wc -l`.

## REPORT
- **FOUND / TESTED / HOW** with controls. Every finding that recommends an action carries its evidence class (**MEASURED AT RUNTIME / PROBED / READ ONLY**).
- **NOT TESTED** at the same prominence.
- The origin develop SHA and `/health` at the start and at the end, with timestamps.
- **If a claim in this brief is false, that is Wednesday's error: report it as one.**
- Write to `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1/`, and name the absolute path in the mail.

**Verdict:** GO · GO WITH FINDINGS · NO GO. Severity per the charter.

## VERDICT DESTINATION
**Mail your verdict to `wednesday-agent@agentmail.to`**, subject
`[QA -> Wednesday] TIER 1 GATE KINTSUGI DEPLOY ROUND 1 4554b25e2 -- <GO|GO WITH FINDINGS|NO GO>`,
with a CLOSING section naming anything you want acted on. **Your pane has no scrollback and you cannot receive mail: the verdict mail is the only thing that survives your session.**

PROVENANCE:
- kintsugi deployed to develop 4554b25e21dfd01113bf40e8f6d34573345a5f37 by s187, 25 services swapped, 39 of 39 verification, the per-image PR table, the frontends unchanged | s187's STATUS mails of 2026-09-11 22:17:27Z and 22:24:45Z and its wrap of 22:28:55Z, structured spf dkim and dmarc pass, read whole by Wednesday | read 2026-09-12
- the public status codes and content types listed under TARGET | curl GET from Wednesday's seat against the public kintsugi hostname, 08:25 and 08:34 AEST (remote reads, not files in any tree) | read 2026-09-12
- the gateway's route blocks (health, api, originate, verify, admin, status, website, showcase, pricing) | git show of the nginx-demo.conf file at 4554b25e2 in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, read verbs only | read 2026-09-12
- deploys to dev take the full tier-1 gate | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md line 16 | read 2026-09-12
