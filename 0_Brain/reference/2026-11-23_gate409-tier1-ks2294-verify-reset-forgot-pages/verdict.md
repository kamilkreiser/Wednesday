PR 2285: GO WITH NOTES (at head 7c5b2f7d184de83a6c4e436c94a0335d24fd8174; tier 1)

# Gate 409, tier 1 (Opus), PR 2285 (KS-2294), 2026-11-23 ~01:39-02:00Z (12:39-13:00 AEDT)

Authority: KS-2294 (High, Wednesday's routing). It serves Kam's card `secuura-ks2275-unverified-email-document-reads-1119` = a. Wednesday's HOW: W68_answer_plan (D1-D5, closed list 1-12) and W68_answer_push (fix A). Findings only: nothing fixed, posted, mailed, merged or written to GitHub or Linear.

## Pins
- **First pin, 01:39:32Z (git ls-remote):** develop 8b0a768f28d4642fb3d4153171fe846595d69b5d; refs/pull/2285/head 7c5b2f7d184de83a6c4e436c94a0335d24fd8174.
- **Second pin, 01:59:44Z:** both unchanged. gh: OPEN, MERGEABLE, updatedAt 01:37:01Z, 1 commit, 12 files, +1479 -0.
- **The head:** ONE commit; its parent is bde7a70d054e.
- **Develop moved bde7a70d054e → 8b0a768f28d4 (KS-2315, PR 2274).** It changes 5 paths: originate `systemErrors.ts`, two originate tests and two fragments. **None of them is one of the PR's 12 paths.** No package or lock file changed: 0 with 'package' (control: 2 in the issuer tree).
- **The develop I ran is 8b0a768f28d4, for every suite.**
- **The merged state** is a local commit, e90e375f5b79 (merge-tree rc 0, tree 87f2acb6220c), never pushed.

## How I measured
- **Clone and worktrees:**
  - Clone: `_work/g`, cloned from GitHub (`--reference-if-able` gate 408's clone, `--dissociate`).
  - Worktrees: `d` (develop), `h` (the merged state: suites, static legs, browser stack) and `x` (the merged state: mutants, probes, planted faults).
  - Git write verbs ran only through `_work/gitx.sh`.
- **node_modules:** APFS clones (`cp -c`) of the seat's `s-w68-dev` root, issuer and packages/shared node_modules. That was a read; nothing was written in their tree.
  - The manifests are equal: 8389ed29 → merged has 0 package paths.
  - 0 absolute symlinks; the workspace links are relative.
- **Environment:** Node v26.8.1. TMPDIR is `_work/tmp`.
  - tsx's IPC socket path was too long under `_work/tmp`, so the browser stack used a short symlink, `/private/tmp/g409t → _work/tmp`. The files stayed in `_work`, and the symlink was moved into `_quarantine` at the end.
- **Commands needing a cwd** ran through `_work/run_cwd_g409.py` (subprocess cwd, no shell `cd`).
- **Tools** (all in `_work/`): `mutants_g409.py`, `probes/g409-probe-location.test.tsx`, `probes/g409-probe-real-api.test.ts`, `stack_g409.py`, `lin_read_g409.py` (gate 408's, read-only).
  - Each probe or plant was placed in `x`, run, then moved to `_quarantine` and sha-checked.
- **End state:** d, h and x have 0 porcelain lines. No listeners on my auth or vite ports. The two w68 containers are still Up (never stopped or removed).

## Findings

There is no HIGH and no MEDIUM finding. The token handling, the contract with auth's real routes, the claim path and the routes hold as built, measured in cells, through the real axios instance, and in a real browser against real auth.

### LOW
**G409-2285-1: the cells miss three non-equivalent mutants. Two bear on the brief's own rules.**
- **G8: the strip by router PUSH instead of replace SURVIVES all 59 cells.** With a push, Back would return to `/verify-email?token=…`, because the link entry stays in history.
  - The shipped code uses replace. In the browser, history.length stayed at its pre-strip value, and Back from the next entry landed on `/verify-email` with no query and the "incomplete" view.
  - So the behaviour is right but unpinned. No cell checks history length or Back.
- **G6b: the D5 logout moved BEFORE the request SURVIVES** (it fires on every submit while signed in, including on 422, 404, expired and retry). No cell checks "signed in + a non-200 answer → no logout".
- **G9: the token read from the live router location each render, instead of from state, SURVIVES.** See G409-2285-2 for why.
- **Equivalent at the UI** (each survives; no UI path posts a held token):
  - G2, G2r: the token not dropped on 404 (verify and reset);
  - G2e: not dropped on expired;
  - G2s: not dropped on 200.
  - So "dropped on a final outcome" is true in the code but pinned by no cell.
- **G7: verify reads any 400 as expired.** Equivalent against auth's real route: verify's only 400 that the page can reach is the expired BAD_REQUEST. "Token required" cannot be reached, because the page never posts an empty token.

**G409-2285-2: a code comment says more than holds in the cells' harness.**
- **The comment:** `utils/linkToken.ts` says a router replace means "the router's location and the address bar agree".
- **Measured (probe `g409-probe-location`, with and without StrictMode):** when the page mounts in the SAME commit as the BrowserRouter, as in all four cell files, the address bar is clean but react-router's `useLocation().search` STILL holds `?token=…` (key "default").
  - Cause: the page's layout effect runs before BrowserRouter's own layout effect attaches its history listener (children's effects run before the parent's).
  - That is why G9 survives.
- **In the real app** App.tsx renders no Routes while `isLoading`, so the page mounts after the router is listening (read, not measured in the router's state). The browser proof's address bar and Back behaved correctly.
- **No leak follows:** nothing renders or logs the router's location on these pages. But the comment's claim, and the cells' ability to tell state from location, rest on that mount order.

**G409-2285-3: D5 ends the session of a DIFFERENT account (measured; within the ruling's letter).**
- **What happened:**
  - The browser was signed in as user A (g409.verify1).
  - Invitee B's claim link was opened in it and B's password was set: 200.
  - The page then called logout: **POST /auth/logout 200, so A's own session was ended server-side.**
- **What the ruling says:** "logout after reset/claim when a session exists", so this is per ruling.
- **What does not hold:** the PR's and the code's reason, "auth has just ended every session of that account", is true only when the session is the same account's.
  - Same account: logout answers 401, because auth already revoked it; harmless, and measured.
  - Not a security defect. Wednesday or Kam may want D5 limited to the same account (the page cannot tell today).

### Info
- **Words: ErrorBoundary.** The residuals in the PR body and in facts comment 141113d6 omit the one path the seat's own plan named.
  - `ErrorBoundary.tsx:55` POSTs `window.location.href` to `/api/client-errors` in PROD. A render error before the strip (during "Restoring session…") would carry the token there.
  - Reading originate: its ingest is `POST /client-errors` under the `/api/client-errors` mount, and the boundary posts to the mount root with a `message` field, not `error`. So it likely does not store (read, not run).
  - Low exposure. It is a residual of the D3 class.
- **"D1 to D5 all yes"** (PR line 1): D3 was ruled "NOT this PR". The sentence means "the recommendations were accepted", which is accurate but terse.
- **nginx's own 400 page** (`_gw_err_400`, code BAD_REQUEST, for example a header or cookie that is too large) would read as "expired" on both pages and drop a token that is still valid. It is edge-only; upstream errors pass through (`proxy_intercept_errors` off, confirmed in all three gateway confs).
- **The client's minimum length is 8; auth's strength check needs more** (`MIN_LENGTH_DEFAULT=12`). A 8-11 character password gets auth's real 422 with its details, and the form and the token are kept (measured).
- **A CSRF 403 through the real instance** (validateStatus) reaches the page as "try again" with the token kept. The interceptor's `window.location.reload()` no longer runs (measured: reload not called). That is right: a reload would lose the stripped token.

## The commission's questions

- **Q1 TOKEN HANDLING. Holds**, with G409-2285-1 and -2.
  - **The token is:**
    - read once (state initializer);
    - stripped by router replace in a layout effect before the page's request (V2, R2, P3; M4 and G1 killed);
    - posted only in a JSON body (V3, R4; M6 killed);
    - one post per press (V10, R13; M11 killed);
    - never in the DOM, a console call, a beacon or fetch (V13, R14; M1, M10, M13 and my G5 `console.debug` in the hook all killed);
    - never in storage (the browser check: localStorage and sessionStorage both false).
  - **Outcomes:** dropped on 200, 404 and expired (true in code; G2* equivalent); kept on 422, 503, 429, 403, 5xx and network (M8, M9, G3d, G4, G4r killed).
  - **StrictMode:** one post, the token kept (V12, R16).
  - **Through the REAL issuer axios instance** (probe `g409-probe-real-api`, the adapter honouring validateStatus as axios's own adapters do):
    - X-XSRF-TOKEN is taken from the cookie, `withCredentials` is true, and the url `/auth/verify-email` has no token;
    - 200, 404, 400, 403 (both body shapes), 429, 401 and 503 reach the page unflattened;
    - a network throw returns `{status:0}`;
    - **no console call carries the token, even with the catch logging its error**, because the instance's interceptor already replaces the error with a body-less object.
    - Planted controls: validateStatus dropped makes 7 of 9 red; a catch that logs `body` makes 1 red.
  - **Away and back:** the browser's Back after leaving returns `/verify-email` with no query, which shows "incomplete".
  - **ErrorBoundary window:** see Info.
- **Q2 CONTRACT against auth.ts at 8b0a768f** (verify 1050-1085, reset 927-1045, forgot 895-922; errorHandler).
  - **Status mapping:**
    - verify: 200, 404 (used or user gone), 400 BAD_REQUEST (expired, consumed first);
    - reset: 400 VALIDATION_ERROR (zod), 422 VALIDATION_ERROR (weak or breached, before the token is spent), 404, 400 BAD_REQUEST (expired), 503 ×2;
    - forgot: always 200.
    - Every status maps as ruled.
  - **The two 503 sentences** are rendered verbatim and distinctly. R9 asserts the exact text of each, and M7, G3 and G3d are killed.
  - **422 keeps the form and the token:** R8 and R8b. Measured in the browser too: auth's real 422 showed its details; then the same token with a strong password gave 200.
  - **Expired and reused never read as success:** M2, M2r, M3, M3r killed. In the browser: reuse showed "invalid" and expired showed the D4 text, with the row staying unverified.
  - **CSRF, cookies and a network throw:** see Q1.
- **Q3 INVITE CLAIM and D5.** Measured in the browser against real auth.
  - The claim link `/reset-password?token=` turned an INVITED/unverified/user row into **ACTIVE / email_verified true / OWNER**, and sign-in with the chosen password worked.
  - **D5, same account:** signed in, reset gave 200 and the page POSTed logout (401: already revoked by auth). On reload, /login was shown.
  - **D5, no session:** reset gave 200 and **no logout call**.
  - **D5, another account's session:** see G409-2285-3.
- **Q4 ROUTES.**
  - The three paths are public siblings of /login, outside ProtectedLayout and not redirect-wrapped. P1 and P2 cover signed-out and signed-in. Measured in the browser: verify opened while signed in, and reset too.
  - **nginx:** `location /verify/` (prefix, trailing slash) and `= /verify` do not match `/verify-email`, so it falls to `location /`, which is the issuer (demo 556, production 433, nginx.conf 323).
  - **Basenames:** admin `/admin`, verifier `/verify`, so there is no collision.
  - **Fallback:** the issuer's nginx.conf 137-138 `try_files … /index.html`.
- **Q5 THE ALIAS (fix A).**
  - All 4 cell files import `BrowserRouter as HarnessRouter`. Each has the same 3-line comment saying it exists ONLY because the guard counts the literal tag, and naming the board item.
  - **The guard file has 0 diff lines in the PR.**
  - **The guard reads 27/27** on develop and on the merged state.
  - In non-test issuer source, `main.tsx` is the only router; App.tsx imports only Routes, Route, Navigate and Outlet.
  - **The guard's alias hole, recorded (not fixed):**
    - an aliased BrowserRouter planted in App.tsx: **27/27, passes**;
    - the same with the literal tag: 26/27 (`FAIL real tree`).
- **Q6 CELLS and MUTANTS. 59 cells:** verify 18, reset 22, forgot 11, routes 8.
  - **Red first, on develop 8b0a768f with the 4 files copied in:** the routes file is 8/8 red by assertion ("Unable to find … heading", and for P4 the forgot link); the three page files fail at load (module absent).
  - **Merged state:** 59/59.
  - **Mutants:** control 59/59 before and after, and every file restored and sha-checked.
    - **The seat's 19 (M1-M17, M2r, M3r), re-typed from its tool: 19/19 killed.**
    - **Mine:** G1 (strip after the first request) killed 6; G3 and G3d (503) killed; G4 and G4r (Try again without a token) killed 5 and 7; G5 (console.debug) killed; G6a (logout with no session) killed; G10 and G11 killed.
    - **Survivors:** G8 and G6b (non-equivalent), G9 (G409-2285-2), and G2, G2r, G2e, G2s and G7 (equivalent, reasons above).
- **Q7 WHOLE.**
  - **Issuer vitest WHOLE:** develop **20/20 in 3 files**; merged **79/79 in 7**. 59 names only on the merged state (the 4 files), 0 only on develop, 0 changed.
  - **packages/shared vitest WHOLE** (cwd = the package):
    - **1743 tests: 1742 passed and 1 failed on BOTH arms. The failing-name sets are IDENTICAL:** `wallet-signature … KS-278 accepts a valid wallet signature over the message`.
    - 0 only on either arm, 0 changed.
  - **tsc:** 0 on both arms (planted: rc 2).
  - **eslint src:** 0 errors and 11 warnings on BOTH arms; the PR's files have 0 messages (planted debugger: rc 1).
  - **vite build:** rc 0 on both arms (planted unresolved import: rc 1).
  - **check:bundle:** develop 264.8 KB, merged **267.1 KB**, budget 450 (BUNDLE_BUDGET_GZIP_KB=1: rc 1).
  - **Leg 14:** I ran only the KS-528 router guard (27/27 on both arms), not the other shell suites.
  - **Overlap:**
    - 18 other open PRs; **0 touch any of the 12 paths** (control: 2285's own list matches 12 of 12).
    - PRs 948, 947 and 639 touch only `frontend/issuer/package.json`.
    - merge-tree of 2285 against: 947 rc 0; 639 rc 0; 2284 (KS-2275, 068ce040) rc 0.
    - Against 948 it gives rc 1, but **948 conflicts identically with develop alone** (same CONFLICT set, none in issuer src). It is a stale dependency PR, not this PR.
    - **Planted control:** local commit 2cd2fd5e9c49 on develop adds an import beside App.tsx's PolicyDocs line. Merged with 2285 it gives **rc 1, CONFLICT in App.tsx**.
- **Q8 BROWSER.** Playwright against my local stack:
  - **The stack:**
    - the seat's offered w68-ks2294-pg (as `secuura_app`) and w68-ks2294-redis, used read-write and never stopped;
    - auth from my merged tree under tsx, with NODE_ENV development, SMTP off, links read from my process log, and my own RS256 and PII keys in 0600 files;
    - the issuer vite dev server from my merged tree, through a wrapper that changes only the port and the /api target.
  - **What I drove and saw:**
    - **verify 200:** the row went verified f → t;
    - **reuse:** "invalid";
    - **expired:** the token's expires_at moved 1 h back gave the D4 text, and the row stayed f;
    - **Back:** "incomplete", with no query;
    - **Login's "Forgot your password?" link:** /forgot-password, then the neutral sentence, with the address not in the DOM;
    - **reset, signed in:** 422 with auth's real details, then 200 on the same token, then logout, then sign-in with the new password;
    - **invite claim:** INVITED → ACTIVE, verified, OWNER, then sign-in;
    - **reset, signed out:** 200 and no logout call.
  - **Six throwaway tokens: 0 hits** in 47 console lines and 37 snapshot and console artefacts (control: "Verify your email address" 6). 0 in the DOM after mount, and the address bar was clean after mount.
  - **Seen, as the residual says:** the address bar holds the token during "Restoring session…" before the page mounts.
  - **NOT covered:** the gateway (CSRF double submit, limiters) and nginx. CSRF on the real instance is covered by the probe in Q1.
- **Q9 WORDS. They hold apart from Info items 1-2.**
  - **PR body:**
    - line refs are true at 8b0a768f: auth.ts 201, 349 and 908; nginx-demo 556; nginx-production 433;
    - the Test Evidence figures (20→79, 59, 19/19, 1742/1743, 264.8→267.1, 27/27) are all reproduced;
    - NOT run is honest; there is no closing keyword ("Refs").
  - **Facts comment 141113d6:** read-only, 4,466 B, unedited (updatedAt .929Z before createdAt .958Z); KS-2294 is In Progress, priority 2, 3 comments. It has:
    - the narrowing (item 2, mail delivery, stays open);
    - D3 (fragment links, a sibling ticket) and D4 (KS-2326, the verbatim copy);
    - the four found-outside items, each verified at source: email.ts 250/256 "1 hour" vs password.ts 25 `RESET_TOKEN_EXPIRY_HOURS = 24`; adminConfig.ts 1613-1614 and 1742-1743 `/register?invite=`; api.ts 233-234 vs Login.tsx 120-127; the guard hole (reproduced, Q5).

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- **A recursive grep over `../`:**
  - I issued one `grep -rn … $A ../`. It resolved from the shell's start directory, so it swept the DevMASTER tree read-only.
  - I stopped it by task id after 120 s, and its output was not used.
- **`cut -c` slips:**
  - Once, on my own auth log, to view a boot failure (secrets filtered first).
  - Once, `| cut -c1-12` on a merge-base SHA.
  - Neither was mail, and both were against the commission's `cut -c` rule.
- **Two `git ls-remote` or fetch calls without `GH_CONFIG_DIR`** ("Repository not found"), re-run with it.
- **Hook refusals, which ran nothing:**
  - a `=====` separator;
  - a write verb pointed at gate 408's clone;
  - an unquoted `for … in $mine` (re-issued under `bash`).
- **Playwright artefacts outside my folder:**
  - The Playwright MCP wrote its snapshot and console files into `/Volumes/DevMASTER/WEDNESDAY/.playwright-mcp/`, the project root.
  - I moved my 37 files (timestamped 01-57 to 01-59Z) into `_work/evidence/playwright_mcp/`. The other 223 pre-existing files there were untouched.
  - Its persistent profile kept a session across `browser_close`. That is how G409-2285-3 was found; I said so rather than hide it.
- **Probe faults:**
  - The first real-api probe used an adapter that skipped axios's settle(), so it was blind (the planted validateStatus control passed). It was fixed and re-run with two working controls.
  - Its first stdout write failed (no `process.stdout` in jsdom); it was replaced.
- **Rows I wrote in the seat's offered throwaway database:**
  - users g409.verify1, g409.verify2 and g409.invitee (@example.test);
  - their token rows;
  - one expires_at moved.
  - Its Redis holds their sessions. Both containers are throwaway and labelled w68; I left them running, never stopped.
- **Throwaway secrets:** I read the container's APP_DB_PASSWORD into a 0600 file in `_work/secret`, never printed. The six local-only throwaway link tokens appeared in this session's transcript (no deployed system).
- No mail, no `cd`, no `rm`, no `!CODING` write, no GitHub or Linear write, and no deployed box or database. No process was killed by name: background tasks were stopped by task id.

## Not run
- The api-gateway and nginx in the browser.
- A production build served by the issuer nginx.
- The other leg-14 shell suites (131).
- Preflight legs 3, 4 and 8.
- Node 24.
- A suite run on bde7a70d054e itself (develop 8b0a768f differs only in 5 originate and fragment paths).
