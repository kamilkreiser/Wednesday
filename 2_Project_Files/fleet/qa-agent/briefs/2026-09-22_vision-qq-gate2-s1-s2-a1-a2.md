# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, BATCHED GATE 2 (portal + QuickQuote): A = S-1 feedback report auth (TIER 1), B = S-2 reminder push redaction (TIER 1), C = A-1 sign-in-code budgets (TIER 1), D = A-2 security headers (TIER 2), E = A-3 sign out (TIER 2), F = A-4 PDF FX provenance (TIER 2), G = portal integration main+item4+item1 (TIER 1), H = item 3 ROUND 2 on its rebased head (TIER 1), I = A-5 dockerignore (TIER 2), J = SLOT for O-1 (TIER 1, optional)

**Drafted for Tuesday 2026-09-22 19:30-20:05 AEST by a read-only drafting agent; Tuesday reviews, re-checks the pre-filled PIN table, stamps and launches.**
Commissioned on the Vision_Sales_Portal agent's READY FOR QA mails (via `coagent@`, in `tuesday-agent@agentmail.to`) as
Tuesday's daily note records them (S-1 + A-1 09:19Z, S-2 + A-2 09:29Z; A-3, A-4 added by Tuesday 19:31 / 19:34 AEST), and on
Tuesday's SCOPE UPDATE after gate 1's verdict (G, H, I, slot J). **The drafter did NOT read the mail bodies** (no AgentMail
call in a read-only commission): every builder claim below comes from commit messages, code comments, Tuesday's daily note or
gate 1's report, and is a CLAIM.
**EVERY HEAD WAS PRE-FILLED BY THE DRAFTER (QuickQuote 19:47:29, portal 19:52:51 AEST); THE LAUNCHER RE-READS THEM ALL.** QuickQuote `main` went `47eb533` →
`1f3df8d` at ~19:40 (merges of gate-1 item 1 `bd3e3cf` and item 2 `72f6c0c`) and the builder rebased item 3, A-1..A-5 and O-1
onto it; the drafter pre-filled those rows from `ls-remote` at 19:47:29 AEST (each `cat-file -t` = commit, merge-base
`1f3df8d`, file sets as §1). The portal rows were pre-filled at 19:52:51 once the integration branch (G) and S-2's rebase onto it
existed. **If any head moves before launch, Tuesday edits its row; the launcher parses §PIN, refuses any placeholder, and re-reads
EVERY head by `git ls-remote` immediately before launch, refusing on any mismatch.** The shas in §1 are what the DRAFTER read (the pre-rebase heads) — they locate the code; they
are NOT the gated heads. The gated heads are the §PIN table, which the launcher also appends, verified, to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-22 19:57
Self-check note: Tuesday read the header, the PIN table (every row matches the builder ls-remote heads mailed 09:19Z-09:48Z), section 13 drivable surface and HELD, and section 14 whole. Sections 1-12 were read by headline plus the drafter report (Tuesday wrote their target specs in the commission). Drafter wrong-at-source list read and accepted: S-1 has 10 cells; partner_admin 200 is existing behaviour, not a bypass; S-2 conflict resolved by the rebase; A-4 and O-1 side by side on 1f3df8d.

SLOT-J: IN
*(Filled `IN` by Tuesday at 19:46 (O-1 landed as `fix/qq-typed-ps-rates-o1-2026-09-22`; row J's head/base/commits are still filled at launch). If Tuesday flips it to `OUT` — set row J's status to `OUT` — set row J's status to `OUT`, DELETE
§J from this brief AND the `[SLOT-J BEGIN]..[SLOT-J END]` block from the prompt. The launcher refuses the placeholder and any
inconsistency between this line, row J and the two blocks.)*

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build any of these changes and you owe no builder anything. **Every line below that reports
what a builder says is a CLAIM, never evidence.**

**ONE batched gate, NINE targets (+ slot J), TWO repos, ONE session** (Kam's standing rule of 2026-09-18: batch gates, never
pay for the same setup twice). **Give a SEPARATE verdict for each: A, B, C, D, E, F, G, H, I (and J if IN) — each GO /
NO-GO, each naming its pinned sha.**
**⚠ Letter collision:** this gate's TARGET letters are NOT the builder's item names. The builder's QuickQuote backlog items
A-1, A-2, A-3, A-4, A-5 are this gate's TARGETS C, D, E, F, I; gate-1 "item 3" is TARGET H; gate-1 items 1 (portal half) + 4
are inside TARGET G. Always write both (e.g. "C (A-1)").
Tiers:
- **A (S-1, feedback report auth) is TIER 1**: an access control on a route that, on portal main, returns every open feedback
  item (description, `admin_notes`, author username) to anyone on the internet (gate 1's O-2, READ).
- **B (S-2, reminder push redaction) is TIER 1** (privacy): reminder pushes go to a PUBLIC ntfy.sh topic; on main they carry
  customer names and quote numbers.
- **C (A-1, sign-in-code budgets) is TIER 1**: the auth mail surface — a checker that refuses sign-in mail.
- **D (A-2, security headers) is TIER 2**: a CSP that breaks a real flow is an outage.
- **E (A-3, sign out) is TIER 2**: a hosted-only UI control over an existing route.
- **F (A-4, PDF FX provenance) is TIER 2, CUSTOMER-VISIBLE PDF TEXT**.
- **G (portal integration: main + gate-1 item 4 + item 1's portal half) is TIER 1** (item 4 is a live customer-mail injection
  fix): the portal runtime legs gate 1 could NOT run.
- **H (item 3, reopen by number, ROUND 2 of 2 under the cap) is TIER 1**: an access control over a year-long store of customer
  data.
- **I (A-5, `.dockerignore` + `npm ci` in the image) is TIER 2**: build recipe only.
- **J (O-1, the PDF/xlsx print LIST rates instead of typed rates — SLOT) is TIER 1**: customer money.

## RULED BY KAM, AND SETTLED (Vision `1_Project_Definition/CLARIFICATIONS.md`)
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` — read it whole.
- **C-01..C-05 govern G and H** (C-01 feedback CC → Tuesday; C-05 creator-only reopen, one identical 404, no admin override,
  **12-month retention, ONE config value**; Kam was told *"saved quotes are kept for 12 months, then removed … a single
  setting"* — gate 1's C-F1 found that untrue of `642b06b`; H's purge is the answer to it).
- **No C-entry covers A, B, C, D, E, F, I or J.** Their authority is the Vision agent's own security/backlog sweep, commissioned
  by Tuesday. **No product choice in them is Kam's ruling** (A: partner sessions may read the report; B: the push text; C: 6/h
  and 20/h; D: `'unsafe-inline'`; F: "a client can label a made-up rate live"): report each as the BUILDER's choice and say
  whether it needs Kam.
- The QuickQuote repo's own rules: `Quoting Tool/hpas-quoting-tool/CLAUDE.md` (single offline HTML file; version discipline;
  **always verify print as a real PDF**; nothing in the sub-project goes near Azure). Read it.
- Deploys are HELD for Kam. Nothing here merges on your word.

## PRIOR ROUND
- **H is ROUND 2 (the LAST under the two-round cap).** PRIOR ROUND: round 1 gated `642b06b`, verdict **NO-GO** (C-F1, Major:
  retention was lazy-on-read only; `pending` rows never removed). **ITS REPORT IS ON DISK AT:**
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate1/` (`report.md` +
  `evidence/`). Findings carried forward and their disposition (builder claims, per Tuesday's scope update — VERIFY each):
  C-F1 → the scheduled purge `03a0682`; C-F2 (expired-delete before the creator check) → claimed fixed (creator checked first);
  C-F3 (no reopen rate limit) → claimed fixed; C-F4 (`stored:false` not shown) → claimed fixed; C-F6 (`stateJson` can exceed
  32K) → claimed guarded; C-F7 (container-clock stamp), C-F8 (`Infinity`/`0x10`/`1e3` retention), C-F9 (stale HANDOVER),
  C-F10 (claimed red counts), C-F11 (no version bump) → **disposition unknown: say for each whether H changed it.**
- **G is round 2 for gate-1's A2 (`ce01ba9`) and D (`d11eed6`)**: both were **GO on PROBED evidence, runtime legs NOT RUN**
  (blocker: 6 portal tarballs not in the npm cache — minimatch 5.1.6 and 9.0.5, brace-expansion 2.0.2, ip-address 10.2.0,
  lodash 4.17.23, path-to-regexp 0.1.12). Gate 1's report "ACROSS TARGETS" names the legs; G runs them on the merged tree.
- **A, B, C, D, E, F, I (and J) are ROUND 1.**
- **Gate 1's harnesses are REUSABLE BY COPY:** `…/2026-09-22-vision-qq-gate1/evidence/` holds `qa-harness-a1.mjs`,
  `qa-harness-a2.cjs`, `qa-harness-c.mjs`, `qa-harness-c-e2e.mjs`, `qa-harness-d.cjs`, `qa-harness-parse.cjs`,
  `qa-preload-portal.cjs`, `qa-run.py`, `qa-floorcount.py` (+ `work/lockcmp.py`). COPY what you use into this gate's own
  evidence folder, read it before trusting it, and never edit gate 1's copies. **Gate 1's self-findings bind you:** (1) quote
  every path (the project path has a space — gate 1 voided two batches); (2) `file://` pages share localStorage — isolate a
  browser context per case; puppeteer's default PDF is Letter — pass `format: "A4"`; (3) **the real server-side renderer calls
  public FX APIs whenever currency ≠ USD** (`fetchLiveRate`, gate 1's O-4) and gate 1's egress record missed those Chrome
  children (O-5) — see §10.3, this gate must BLOCK and RECORD them.

## PIN — HEADS (FILLED BY TUESDAY AT LAUNCH; parsed and verified by the launcher)
Rules the launcher enforces: every `IN` row has a 40-hex head and base, a commit count, no `@`; head is a commit in its repo;
base is an ancestor AND the merge-base; `git rev-list --count base..head` equals `commits`; `git ls-remote origin
refs/heads/<branch>` equals head NOW; **base is the same repo's MAIN row head or another IN row's head in the same repo**
(stacked rebases are allowed, and must be named). MAIN rows are re-read by `ls-remote` too. An `OUT` row carries `-` in
head/base/commits.


**RE-PINNED BY TUESDAY 19:5x (after the drafter):** G gained ONE commit, `289e2d9` "integration: feedback notify accepts both variable names; an empty list refuses at boot" (server/feedbackNotify.js + feedbackNotify.test.js, +2 cells; gate-1 A1-F2/AX-F1). Gate it AS PART OF G, tier 1 through-code: FEEDBACK_NOTIFY_EMAILS || FEEDBACK_NOTIFY_EMAIL || default; `" , "` and `",,"` refuse at boot (real `node server/index.js` exits non-zero); unset and `""` do not. B was re-stacked onto `289e2d9` (a clean rebase per the builder; diff it against `00c5201` to confirm nothing else changed). The QuickQuote follow-up branch `fix/qq-feedback-followups-2026-09-22` @ a33f87e is NOT in this gate (it goes to the next one).

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | ef5a9c0b942c71b8c3b08feec22ae23dbe622581 | - | - | IN |
| MAIN-Q | quickquote | main | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | - | - | IN |
| A | portal | fix/feedback-report-auth-2026-09-22 | 89af8ba7817f3288765efd680b5e1b9827fc58fd | ef5a9c0b942c71b8c3b08feec22ae23dbe622581 | 3 | IN |
| B | portal | fix/reminder-push-redaction-2026-09-22 | fb23f64ab335a67b7e761e95528bcd4a604ed7ec | 289e2d9545ae08fdcb8fdff47ba0115574e90f3e | 1 | IN |
| G | portal | integration/portal-gate2-2026-09-22 | 289e2d9545ae08fdcb8fdff47ba0115574e90f3e | ef5a9c0b942c71b8c3b08feec22ae23dbe622581 | 7 | IN |
| C | quickquote | feat/qq-otp-send-budget-2026-09-22 | 3c8d3a41733f7f2aa49591a71abfa8fcc1c9cbbe | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 1 | IN |
| D | quickquote | feat/qq-security-headers-2026-09-22 | ae33a94b563e469059c915a80c76e82e6fbf84b8 | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 1 | IN |
| E | quickquote | feat/qq-sign-out-2026-09-22 | 7ccd119ba0c5bdf411cd9c08ccebd5b1ad1ab65d | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 1 | IN |
| F | quickquote | fix/qq-pdf-fx-provenance-2026-09-22 | 0b9551a95a98726e6aebf4c36cb5051245fdc9d9 | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 1 | IN |
| H | quickquote | feat/qq-open-old-quote-2026-09-22 | c8fb771eb980a9c3824977c66dc3844a0af889ad | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 3 | IN |
| I | quickquote | fix/qq-dockerignore-2026-09-22 | b9890c32120e3fb3856774ee56a0a7e6a8cd22b3 | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 1 | IN |
| J | quickquote | fix/qq-typed-ps-rates-o1-2026-09-22 | 0bdbd936e827a0df243332da604a498e2cea6512 | 1f3df8ded0a8357cb6966aba4cc0c4efa78fc593 | 1 | IN |
<!-- PIN-HEADS:END -->

Repos: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`); QuickQuote = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool`
(remote `datasecau/vision_hpas-quickquote`). **Expected shape at launch (Tuesday's scope update):** B's base = G's head (S-2
rebased onto the integration branch); G's base = portal main; QuickQuote targets on `1f3df8d` or later (items 1 + 2 merged), H
and every QuickQuote target rebased onto `1f3df8d` side by side (NOT stacked, as read at 19:47). They conflict with each other at
MERGE time (§12) and the builder rebases each in merge order then — so every QuickQuote GO here is at the pinned, un-stacked sha. **A GO is a statement about the pinned
SHA only.** If a head moves, its verdict expires.

## 1. Targets — READ from the object store at drafting (19:30-20:00 AEST, PRE-REBASE shas)
Drafting shas (read by `ls-remote` 19:30:35 / 19:31:40 / 19:34:45 / 19:40:09, each `cat-file -t` = commit): portal main
`ef5a9c0`; A `89af8ba` (chain `8df198a` → `fb907b9` → `89af8ba`); B `1c726bb`; gate-1 item 4 `d11eed6` (fix `a68b53a`), item 1
portal `ce01ba9`; QuickQuote main `47eb533` then `1f3df8d`; C `8a157bb`; D `f6ca31f`; E `57b373c`; F `6eb367e`; H (item 3)
`03a0682` (child of `642b06b`); I `ebbc953`. **Every file:line below is at the drafting sha; after a rebase, re-locate by content.**
**No drafting target changed a lockfile** (portal `package-lock.json` blob `9d426df`; `stage3/package-lock.json` blob `64e49cb`);
the launcher re-checks this at the pinned heads.

### TARGET A — S-1: `/api/feedback/report` and `/summary` need a session OR the coordinator secret (TIER 1), portal
- **Files over main:** `server/routes/feedback.js`, `test/db/feedback-auth.test.js` (A, 10 tests), `scripts/e2e-feedback-test.js`,
  `DEV-SESSION-SUMMARY.md`, `Reference_doc/feedback-system-overview.md`, `BACKLOG.md` (an unreproduced `routes.test.js`
  before-hook failure, 17/17, "cause UNKNOWN" — watch for it in your `test:db` runs and report it either way).
- **Mechanism (READ at `89af8ba`):** `requireSessionOrCoordinator` (`feedback.js:90-93`): `req.session?.user ||
  checkCoordinatorAuth(req)` → next, else **403 `{"error":"Sign-in or X-Coordinator-Secret required"}`**; on
  `router.get('/report', …)` `:96` and `/summary` `:146`. `checkCoordinatorAuth` (`:352-358`, `fb907b9`): `!secret || typeof
  header !== 'string' || !header` → false; `Buffer.from` both; `a.length === b.length && crypto.timingSafeEqual(a, b)`.
  `/:id/coordinator-action` (`:267-275`) uses it too **and keeps its PRE-EXISTING localhost allowance** (`req.ip` ∈
  `127.0.0.1`/`::1`/`::ffff:127.0.0.1`). `/coordinator-state` GET/PUT (`:360`, `:374`): 403 `Invalid coordinator secret`.
- **`server/index.js:44` sets `app.set('trust proxy', 1)`**: `req.ip` comes from the rightmost `X-Forwarded-For`. The builder's
  own `coordinator-action` cell forges `X-Forwarded-For: 203.0.113.5` to get a NON-local `req.ip` — so the header is honoured.
  **The converse — `X-Forwarded-For: 127.0.0.1` with NO secret — is §3 Q5.**
- **Partner sessions are ALLOWED by design:** the builder's cell asserts `partner_admin` → 200, "as with GET /api/feedback".
  READ: `GET /api/feedback` (`:61`, `requireAuth`) already returns every item with `author_username` to ANY signed-in user. So a
  partner reading `/report` is parity, not a new leak — say so, and say whether partner visibility of `admin_notes` + other
  authors needs Kam.
- **BREAK LIST — consumers that get 403 after A (READ ONLY, do NOT change or run them):**
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Feedback_System/2_Project_Files/packages/coordinator/poller.js:43`
    `const resp = await fetch(project.feedbackUrl, fetchOptions);` — `fetchOptions` carries only `signal` (read 19:33; that
    directory is **not a git repository**, so re-read it). Also `fetchInsecure` (`:40`) and `actionProcessor.js:32`. An archived
    copy `…/Datasec/_archive/Feedback_Coordinator/poller.js:50` has the same shape (note only).
  - Portal `.cursor/rules/check-feedback-workflow.mdc:44` `curl -s http://localhost:4848/api/feedback/report` and `:120`
    `curl -s https://datasec-sales-portal.azurewebsites.net/api/feedback/report | …` — no header. **Never run either** (`:120`
    is the live site).

### TARGET B — S-2: reminder pushes to the public ntfy topic carry no customer detail (TIER 1), portal
- **Pinned `00c5201`, ONE commit rebased onto G `4e0dc02`** (drafting sha `1c726bb` was off main). Files over G:
  `server/reminders/dispatcher.js`, `test/db/reminder-push.test.js` (A, 6 tests), `docker-compose.yml`, `DEV-SESSION-SUMMARY.md`.
  The builder resolved the `dispatcher.js` conflict keeping BOTH item 4's `reminderEmail` (email branch, `escapeHtml(rem.body ||
  rem.title)` at `:30`) and B's `reminderPush` (`:46`, used at `:140`); `module.exports` exports both (`:177`) — READ 19:53.
- **Mechanism (READ at `1c726bb`):** `reminderPush(rem)` = exactly `{ title: "Reminder #<id> due", body: "Open the Vision Sales
  Portal (PRO dashboard → Reminders) to read it." }`, used in the ntfy branch of `dispatchDue()` instead of `sendNtfy(rem.title,
  rem.body || '')`. `docker-compose.yml`: `NTFY_TOPIC: datasec-kam-feedback` → `NTFY_TOPIC: ${NTFY_TOPIC:-}`. `NTFY_SERVER` is
  read at REQUIRE time.
- **Which reminders reach ntfy (READ):** the three rules (`quote_expiry` title `Quote <qnum> expires …`, body `… for
  <customer_name> …`; `poc_commencement` `PoC for <customer> commences …`; `stale_follow_up` `Follow-up gone quiet:
  <customer>`); manual reminders (`routes/reminders.js:39`: `user` → `ntfy` unless `b.channel === 'email'`); and **a `user` +
  `channel 'email'` row with NO `recipient_email`** (falls into the ntfy branch by `dispatchDue`'s condition).
- **Other ntfy publishers (READ, NOT changed by B):** `server/feedbackDigest.js` (counts) and **`server/dbBackup.js:103-121`**
  (`Backup failed: <error>` — READ what the error can carry).

### TARGET C — A-1: per-source and global sign-in-code budgets on `/auth/request` (TIER 1), QuickQuote
- **Files over its base:** `stage3/server.js`, `stage3/test/server.test.mjs` (10 new tests), `BACKLOG.md`.
- **Mechanism (READ at `8a157bb`):** `OTP_IP_BUDGET_PER_HOUR = 6`, `OTP_GLOBAL_BUDGET_PER_HOUR = 20`; `createApp` options
  `otpIpBudgetPerHour = Number(process.env.OTP_IP_BUDGET_PER_HOUR) || 6`, `otpGlobalBudgetPerHour = Number(process.env.
  OTP_GLOBAL_BUDGET_PER_HOUR) || 20`, `otpBudgetWindowMs`, `trustForwardedFor = !!process.env.WEBSITE_SITE_NAME`.
  `clientKey(req, trust)` (exported): with trust, the RIGHTMOST non-empty `X-Forwarded-For` entry, else the socket address;
  `[v6]:port` unbracketed; `a.b.c.d:port` stripped; lower-cased; `::ffff:a.b.c.d` unwrapped; IPv6 keyed by its first four
  hextets + `::/64`. Order in `/auth/request`: email regex (400) → per-address window (429) → cooldown (429) → **per-source
  budget** → **global budget** → `record` both (synchronous, no `await` between check and record) → code → `putOtp` → send.
- **The two new refusal messages (VERBATIM, JSON `error`, 429 + `Retry-After` + `retryAfterSeconds`):**
  `too many sign-in codes requested from your network — try again later` and
  `sign-in is busy right now — try again in a few minutes`.
  The login page (`stage3/login.html:53-76`) renders `error` minus trailing stops, then `. Try again in <N seconds|minutes>.` —
  e.g. *"too many sign-in codes requested from your network — try again later. Try again in 60 minutes."* — and reveals the
  code box on any 429 (for a budget 429 no code was sent).
- **Stated residual:** real App Service `X-Forwarded-For` is **NOT TESTED** (docs-based). A distributed sender can still
  exhaust the global 20/h (stated trade).

### TARGET D — A-2: security headers on every response (TIER 2), QuickQuote
- **Files over its base:** `stage3/server.js` (one `app.use` right after `express()`), `stage3/test/server.test.mjs` (3 tests),
  `BACKLOG.md` (a NEW open item: a false `QUOTE MISMATCH — toggleAdvanced` log on every advanced email — confirm or refute).
- **Headers (READ):** `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'
  'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://api.frankfurter.app https://api.frankfurter.dev
  https://open.er-api.com; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`,
  `Strict-Transport-Security: max-age=31536000`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy:
  no-referrer`, `Cache-Control: no-store` (the builder relies on `send` not overwriting a set Cache-Control on `sendFile`).
- **`'unsafe-inline'` is an ACCEPTED, STATED residual** (a nonce is the builder's named follow-up). Do not NO-GO D on it.

### TARGET E — A-3: a Sign out control in the hosted masthead (TIER 2), QuickQuote
- **Files over its base:** `stage3/strip.js` (inside `HOSTED_EXTRAS`), `stage3/test/strip.test.mjs` (+1), `stage3/test/server.test.mjs`
  (+2, the first `/auth/logout` tests), `BACKLOG.md`.
- **Mechanism (READ at `57b373c`):** `<button id="btnSignOut" class="btn-settings">` as the FIRST child of `.masthead-right`;
  click → `fetch("/auth/logout", { method: "POST" })`; `r.ok || r.status === 401` → `location.href = "/login"`; else (or a throw)
  the text becomes the failure string and the button re-enables. Server side (unchanged): `POST /auth/logout` is `requireAuth` →
  `store.deleteSession(rowKey)` → `Set-Cookie: qqs=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0`. No CSRF token on any
  QuickQuote POST; the cookie is `SameSite=Lax`.
- **The two UI strings (VERBATIM):** `Sign out` and `Sign-out failed — retry` (em dash, U+2014).
- **Residual:** the live Table Storage session delete is **NOT TESTED**.

### TARGET F — A-4: the emailed PDF names the FX source the browser used (TIER 2, CUSTOMER-VISIBLE), QuickQuote
- **Files over its base:** `stage3/lib/pdf.js`, `stage3/strip.js`, `stage3/test/fx-provenance.mjs` (A, 6 tests, real Chrome),
  `stage3/test/strip.test.mjs` (+1), `stage3/package.json` (`test:print` adds `test/fx-provenance.mjs`), `BACKLOG.md`.
- **Mechanism (READ at `6eb367e`):** the collector posts `state.fx = fxState`. In the render page, AFTER `currency` is applied
  (which resets the page's `fxState` to seed): `fx.source === "live"` AND `CONFIG.fxProviders.find(x => x.id === fx.provider)`
  AND page currency ≠ `USD` AND `/^[0-9A-Za-z ,:-]{1,32}$/.test(String(fx.date || ""))` → `fxState = { source: "live", date,
  provider: fxProv.id, srcName: fxProv.srcName }`; else seed stands. `closeBrowser()` exported (no force-exit in tests).
- **Printed line (READ, `index.html:2638` / `:2823`):** live → `` `live reference rate (${fxState.date}) via ${fxState.provider}` ``
  (provider = CONFIG's `id`: `Frankfurter (ECB)`, `Frankfurter legacy`, `Open ER-API`, `index.html:1742-1744`); else `seeded
  table rate (indicative)`; USD → the anchor form. **The builder's 6 cells assert `report.fx` only — none reads PDF text.**
- **Accepted residual (builder):** a client can label a made-up rate "live" — it could already send any `fxRate`.

### TARGET G — portal integration `integration/portal-gate2-2026-09-22` = main + item 4 (`d11eed6`) + item 1 portal (`ce01ba9`) (TIER 1)
- **Pinned `4e0dc02` (19:52:51), 6 commits over `ef5a9c0`:** `7d005de` = merge of item 4 `d11eed6` (fix `a68b53a`); `6c01c87` =
  merge of item 1 portal `ce01ba9` (builder: `BACKLOG.md` conflict only — gate 1 measured the same); `4e0dc02` = a FOLD:
  `feedbackNotify.js` now uses item 4's `server/email/escapeHtml.js` helper instead of its private one (gate 1's D-F2). READ at
  `4e0dc02`: `feedbackNotify.js:22` requires `./email/escapeHtml`; the default list `kreiser.org@me.com,tuesday-agent@agentmail.to`
  is unchanged; lockfile blob `9d426df`. **The fold is NEW CODE that neither gate-1 GO covered: re-run gate 1's A2 probe/escape
  legs against it (the private helper's behaviour must be preserved — diff the two helpers' outputs over the §6 payload classes).**
  Delta over portal main: the union of item 4's files (`server/email/escapeHtml.js`,
  `server/email/escape.test.js`, `server/email/index.js`, `server/reminders/dispatcher.js`, `BACKLOG.md`) and item 1's
  (`server/feedbackNotify.js`, `server/feedbackNotify.test.js`, `server/routes/feedback.js`, `server/email/index.js`,
  `BACKLOG.md`). Gate 1 MEASURED `ce01ba9 × d11eed6`: **CONFLICT in `BACKLOG.md` only; `email/index.js` auto-merges** (D's
  escaped fallback AND A2's `cc`). A2's BACKLOG entry describes the defect D fixes — it should be dropped; A2's private
  `escapeHtml` may be folded into D's helper (gate 1's D-F2).
- **What G exists to run (gate 1's NOT RUN list):** portal `npm ci --offline --ignore-scripts` (the 6 tarballs are now cached —
  builder claim, 09:10Z), `npm test`, `npm run test:db`, **the real `POST /api/feedback` route on local Postgres**, **the real
  `dispatchDue()` on local Postgres**, and gate 1's A2 and D harnesses on the merged tree.

### TARGET H — item 3 ROUND 2: reopen an old quote by number, creator only, on its REBASED head (TIER 1), QuickQuote
- **Round 1 = `642b06b` (NO-GO, C-F1).** `03a0682` (child of `642b06b`, READ): a scheduled purge — `QUOTE_PENDING_MAX_MS = 1 h`,
  `QUOTE_PURGE_INTERVAL_MS = 6 h`, `app.purgeQuotes()` → `store.purgeQuotes(now - QUOTE_RETENTION_MS, now - QUOTE_PENDING_MAX_MS)`,
  "run at boot and every QUOTE_PURGE_INTERVAL_MS by the entry point"; `stage3/lib/store.js` +18; `stage3/test/store.test.mjs` (A,
  36 lines); `stage3/package.json` `test` adds `test/store.test.mjs`. The rebased head (on a main that contains item 1) should
  ALSO carry the builder's C-minor fixes. **Pinned chain (19:47):** `2165343` (item 3, rebased from `642b06b`) → `d88af73` (the
  purge, rebased from `03a0682`) → `c8fb771` (the four minors: `stage3/server.js` +44/−7, `stage3/strip.js` +4/−1,
  `stage3/test/server.test.mjs` +65/−1). **Claims for `c8fb771` (Tuesday, from the builder):** (1) creator checked BEFORE the
  expired delete, so a stranger's lookup leaves the row; (2) the `stored:false` note reads *"It could not be saved for reopening
  later, so keep the email."*; (3) per-field caps with a 30,000-character JSON guard under the 32,767 limit — over the guard the
  quote still MAILS but is marked unstorable; (4) reopen limit **30 per session per 10 min**, then 429 + `Retry-After`. READ at `c8fb771`: `QUOTE_STATE_MAX_CHARS = 30000`
  (`server.js:105`); `REOPEN_MAX = 30, REOPEN_WINDOW_MS = 10 min` (`:106`), keyed `req.session.rowKey || req.session.email`, checked
  BEFORE the number regex and the store read, body `{"error":"too many quote lookups — try again shortly","retryAfterSeconds":N}`;
  the creator check (`:503`) now precedes the expiry delete; the entry point purges at boot and every 6 h, a failed purge logged
  and never fatal (`:668-676`); the `stored:false` note is appended in `strip.js:244`.
- **The builder HAND-RESOLVED the `createApp` signature conflict** on item 3 (and on A-1). Prove the rebase changed nothing but
  that resolution: `git range-diff 47eb533..03a0682 1f3df8d..d88af73` and `git range-diff 47eb533..8a157bb 1f3df8d..3c8d3a4`
  (read-only), plus `git diff` of each rebased commit's own patch vs its pre-rebase patch (`642b06b`→`2165343`, `03a0682`→`d88af73`,
  `8a157bb`→`3c8d3a4`); every differing hunk named, read, and shown to be the conflict resolution (item 1's `feedbackNotify`
  option beside the new options) and nothing else.
- Expected delta over its base: within `BACKLOG.md`, `CLAUDE.md`, `stage3/lib/pdf.js`, `stage3/lib/store.js`,
  `stage3/package.json`, `stage3/server.js`, `stage3/strip.js`, `stage3/test/server.test.mjs`, `stage3/test/store.test.mjs`,
  `stage3/test/strip.test.mjs` (the launcher refuses any file outside that set).

### TARGET I — A-5: `.dockerignore` + `npm ci` in the image (TIER 2, build recipe only), QuickQuote
- **Files over its base (READ at `ebbc953`):** `.dockerignore` (A, 13 lines: `**/node_modules`, `.git`, `stage3/public`,
  `stage3/private`, `Screenshots_for debugging`, `.playwright-mcp`), `stage3/Dockerfile` (`RUN npm install --omit=dev` → `RUN npm
  ci --omit=dev`), `BACKLOG.md` (two duplicate entries closed). Build context = the REPO ROOT (`az acr build … --file
  stage3/Dockerfile .`); the Dockerfile copies `stage3/package.json stage3/package-lock.json*`, installs, then `COPY index.html`,
  `COPY stage3/ /app/stage3/`, `RUN node strip.js`.
- **The defect it closes:** without `.dockerignore`, `COPY stage3/` landed the builder's macOS `node_modules` ON TOP of the image's
  install (and a stale `stage3/public`), so what shipped came from the laptop, not the lockfile.

### TARGET J — O-1 (SLOT, filled IN): the emailed PDF and xlsx keep the rep's typed service rates (TIER 1, customer money), QuickQuote
- **The defect (gate 1 MEASURED on `47eb533` and `642b06b`):** the collector posts fields in DOM order (rates before `currency`);
  `lib/pdf.js` applied them in that order; `currency`'s change handler calls `applyPsvRates()`, overwriting them (typed Advanced
  $2,000 and custom $300/h printed as $2,100 and $280/h; $32,860 vs $32,900). **Two faces (builder):** (a) typed rates overwritten
  by list; (b) a converted currency priced SERVICES at the SEED rate while licences used the live rate (F8's single-rate invariant,
  `index.html`).
- **Drafting head `0bdbd936e827a0df243332da604a498e2cea6512`** on `fix/qq-typed-ps-rates-o1-2026-09-22`, ONE commit, parent the
  NEW main `1f3df8d` (read 19:45:55, `cat-file -t` commit). **Files:** `stage3/lib/pdf.js` +34/−3, `stage3/test/typed-rates.mjs`
  (A, 5 tests, `after(closeBrowser)`), `stage3/package.json` (`test:print` adds `test/typed-rates.mjs`). Stage3 lockfile unchanged.
- **Mechanism (READ at `0bdbd93`):** pass 3 (fields) now applies `currency`, then `fxRate`, then every other field in posted order;
  if the client posted NONE of `price-basic`/`price-advanced`/`price-custom`, `applyPsvRates(currency)` runs again after the posted
  `fxRate` landed (so services are derived at the posted rate, not the seed). The report gains `docText` (`#quoteDoc.innerText`,
  for tests — READ: `server.js` does not log or return `report` wholesale; confirm on the pinned head). `closeBrowser()` exported.
  Pass 1/2 (checks — the PoC gating that `3b67aac` "the emailed PDF and CSV dropped the PoC" introduced the three passes for) are
  unchanged — confirm.
- **CONFIG currencies (READ, `index.html:1734`):** `fxSeeds` USD 1.0000, AUD 1.5500, EUR 0.9300, GBP 0.7900, NZD 1.6700, SGD 1.3500,
  DKK 6.9300. The line-rate formula (`:3433`) is `cur === "USD" ? 1 : (parseFloat(fxRate) || CONFIG.fxSeeds[cur] || 1)`.

### All targets
- **No worktree is pinned. Build your own trees INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store:**
  `git -C <repo> archive <pinned sha> | tar -x -C <a fresh mktemp -d under your project>`. **Never `git worktree add`,
  `checkout`, `switch`, `fetch`, `pull`, `stash`, `reset`, `restore`, `clean`, `gc`, `tag` or commit against either repo, and
  never work inside either checkout.** Both checkouts are the LIVE builder's working trees: pin by sha, read origin by `ls-remote`.
- **Dependencies, without the network:** an archived tree has no `node_modules`. The builder's installed `node_modules` is NOT
  the gated set; do not copy it unless you prove, at copy time, that it matches entry by entry. The sanctioned route: in YOUR
  archived tree, **`npm ci --offline --ignore-scripts`** (in `stage3/` for QuickQuote, at the root for the portal). `--offline`
  forbids the network by construction: a cache miss FAILS rather than fetches — that suite is then **NOT RUN, blocker named**
  (name the missing tarballs). Never `npm install`, never `npm ci` without `--offline`, never `npx` a package that is not already
  in the tree. After it, prove `node_modules/.package-lock.json` matches `git show <sha>:<lockfile>` entry by entry and quote the
  count. Chrome: `PUPPETEER_EXECUTABLE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.
- **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant tree
  for a clean arm; never touch gate 1's trees.
- **`git merge-tree --write-tree` writes objects** — only ever as `GIT_OBJECT_DIRECTORY=<your own mktemp -d>
  GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree --name-only <a> <b>`. The same two
  variables let you `git archive <tree-id>` a merge RESULT. If you cannot do it that way, SKIP it and say so.
- **A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES:** `node --check` on every mutated `.js`/`.mjs` before its arm, exit code
  quoted. A red from a mutant that does not parse or load is a VOID arm, never a red.
- **NOT on main. Nothing merges on your word or a builder's.** Merges are Tuesday's GO on a pinned head.

## 2. Why these tiers, and who is waiting
- **A** closes a live, internet-facing read of every open feedback item. **B** closes a live disclosure of customer names and
  quote numbers on a public topic whose documented name is in the repo (`DEV-SESSION-SUMMARY.md`) — **whether the live topic is
  that value is UNMEASURED (production); do not try to find out.** **C** guards sign-in mail: a false refusal locks people out, a
  bypass sprays strangers and exhausts ACS (exhausted live 2026-08-26, per BACKLOG). **D** a CSP that blocks FX / unlock / email
  breaks the tool. **E** ends a 7-day session on a shared machine. **F** changes customer PDF text. **G** is the condition on
  gate 1's two portal GOs (A2, D). **H** is the last round for item 3 under the cap. **I** decides what code ships in the image.
  **J** is customer money.
- 🔴 **Queue:** deploys HELD for Kam. Merge order: portal G (item 4 + item 1), then S-2 on G, then S-1; QuickQuote items 1 + 2
  merged (`1f3df8d`), then H → C → D → E, and J → F, with I after the puppeteer change is settled — each rebased by the builder (§12).

## 2a. LEGITIMATE SHAPES — CHECKERS in this gate (template §2a)
A (an auth gate), C (a mail budget), B's topic default (an off-switch) and H (creator check, retention purge, reopen rate
limit) each refuse something. Measure every row.

| shape — its ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| A: a signed-in datasec user GETs `/report` | 200 | `req.session?.user` | builder |
| A: a signed-in `partner_admin` GETs `/report` / `/summary` | 200 (parity with `GET /api/feedback`) | `req.session?.user` | builder — **say whether it needs Kam** |
| A: the poller sends the correct `X-Coordinator-Secret` | 200 | `checkCoordinatorAuth` | builder |
| A: that header name in other case | 200 — header names are case-insensitive; NOT a bypass | Node lower-cases names | drafter — measure |
| A: `HEAD /api/feedback/report` with a valid session | 200, no body | Express routes HEAD through GET | drafter — measure |
| A: `/report/`, `/Report` | the SAME gate (non-strict, case-insensitive routing) | Express defaults | drafter — measure |
| A: the Feedback_System poller as it is today (no header) | **403** | neither clause | builder (break list) |
| C: one person, one address, 3 codes in 15 min, then a 4th | 3 × 200 then the per-ADDRESS 429; source budget untouched by the refusal | per-address before budgets | builder |
| C: 6 people behind one NAT, one sign-in each in an hour; a 7th | 6 × 200; the 7th → per-source 429 | 6/h per key | drafter — **grade the 7th** |
| C: off App Service, any `X-Forwarded-For` | ignored; socket address counts | `trustForwardedFor` false | builder |
| C: on App Service, platform-appended `1.2.3.4:5678` rightmost | keyed `1.2.3.4` | port strip | builder |
| C: two IPv6 privacy addresses of one subscriber (same /64) | ONE key | `::/64` | builder |
| C: `OTP_IP_BUDGET_PER_HOUR` unset / `"6"` / `"10"` | 6 / 6 / 10 | `Number(x) || 6` | drafter |
| C: `OTP_IP_BUDGET_PER_HOUR` = `"0"`, `""`, `"abc"` | 6 (falsy → default) — not "off" | `|| 6` | drafter — measure |
| C: `OTP_IP_BUDGET_PER_HOUR` = `"-1"` / `"0.5"` | **READ prediction: `-1` DISABLES the budget** (`0 < -1` false → `windowMs - (now - undefined)` = `NaN`; `NaN > 0` false → allowed, always); `0.5` → 1/h. No boot check. | `windowBudget.waitMs` | drafter — **MEASURE; a negative value meaning unlimited is a finding** (same for the GLOBAL variable) |
| B: `NTFY_TOPIC` unset / `""` | no push, no request at all | `if (!topic)` | builder |
| H: the creator reopens a 364-day-old quote; a stranger reads an expired number | 200; 404 (byte-identical) — and after the fix the stranger's read must NOT delete the row | creator check before expiry | builder (fix claim) — **measure** |
| H: the scheduled purge at boot and every 6 h | expired rows (read or not) and `pending` rows older than 1 h removed; a `pending` row 59 min old KEPT (its send may be in flight) | `purgeQuotes(retention, pending)` | builder — **measure the 59/61-min boundary** |
| H: a rep reopening their own quotes at an ordinary pace (e.g. 10 in 10 min) | 200 each | 30 per session per 10 min | builder — measure |
| H: a busy rep reopening 30 quotes in 10 min, then a 31st | 30 × 200, the 31st → 429 + `Retry-After` | the same limit | builder — **measure; grade whether 30 is a legitimate ceiling, and whether a NEW session resets it (a per-session key can be reset by signing in again)** |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.** A legitimate shape refused is
a **Major**.

## 3. TARGET A — S-1 (TIER 1)
**Drive the portal's `createApp()` in YOUR OWN harness** (exported from the portal's server entry module alongside `main`; the
listener, feedback digest and reminder scheduler start only in `main()` — READ it). Listen `127.0.0.1`, port 0. LOCAL Postgres.
1. **Scope, mechanically:** every changed non-test line is the middleware, its two mounts, the `crypto` require,
   `checkCoordinatorAuth`, the coordinator-action swap, the e2e script's headers and three doc lines.
2. **Builder's cells:** portal `npm run test:db` on YOUR test DB (predicted concurrency 5, feedback-auth 10, harness 4, routes
   17). **Red-proof:** revert `server/routes/feedback.js` to its base's, keep the test → predict which of the 10 redden (the
   coordinator-state cells should stay GREEN — main's `===` refuses the same inputs), then run. Your mutants: the middleware on
   `/report` only; `checkCoordinatorAuth` back to `secret && header && secret === header` (does anything but the SOURCE pin
   catch it? say plainly that no cell measures timing); the length check removed (does the unequal-length cell see a 500 —
   `timingSafeEqual` throws — rather than a 403?).
3. **ADVERSARIAL PASS (A) — every bypass shape; state the FAIL condition before each.** FAIL = any status other than 403, OR any
   refusal body containing an item title/description/`admin_notes`/username/count. Seed a probe item first, then, anonymous, on
   BOTH routes:
   - the header name in any case, with a WRONG secret;
   - `COORDINATOR_SECRET` UNSET and the header `""`, `"undefined"`, `"null"`, `" "`, absent; SET, with the header `""`, one byte
     short, one byte long, secret + `\u0000`, trailing space/tab, the secret twice, and the header sent TWICE (Node joins with
     `, `); a multi-byte UTF-8 secret vs a Latin-1 lookalike;
   - methods `HEAD`, `OPTIONS` (an auto `Allow` answer must carry no data), `POST`, `PUT`;
   - paths `/report/`, `/Report`, `/REPORT`, `/report?x=1`, `/report#x`, `/report;x`, `/%72eport`, `/report%2F`,
     `//api/feedback/report`, `/api/feedback/./report`, `/api/feedback/x/../report`, `/api//feedback/report` — status and where
     each was routed (an encoded variant landing on the SPA fallback is fine; one reaching the handler without the gate is Critical);
   - `X-Forwarded-For: 127.0.0.1`, `X-Real-IP`, `Host: localhost` (no localhost allowance on these routes — confirm);
   - an expired / logged-out session cookie, a forged `connect.sid`.
   Every refusal must be the one 403 JSON (record Content-Type, Content-Length, body).
4. **`/coordinator-*` not regressed:** `coordinator-state` valid 200, wrong/missing/unequal/unset 403 with the same body as
   before; `coordinator-action` valid secret from a non-local `req.ip` passes, wrong 403.
5. **The localhost allowance (PRE-EXISTING on `coordinator-action`) — measure, do not re-tier A on it:** `COORDINATOR_SECRET`
   set, NO header, `X-Forwarded-For: 127.0.0.1` from your loopback client; then `127.0.0.1, 203.0.113.5` and the reverse. READ
   what `trust proxy 1` yields behind App Service (the front end appends the real caller). Can a remote caller make `req.ip`
   loopback in production? It is on main already — a finding against the route, with its evidence class.
6. **The break list (READ ONLY):** re-read `poller.js:43` (and `:40`, `actionProcessor.js`) and the `.cursor` rule `:44`/`:120`;
   state what each does on a 403. Grep the portal and Feedback_System trees for any OTHER consumer of `/report` or `/summary`
   (the digest does not call the route — READ `feedbackDigest.js`).
7. **Timing (PROBED, not a verdict input):** 200 samples each of wrong-equal-length vs wrong-unequal-length on
   `/coordinator-state`; medians. The length check leaks the secret's LENGTH by design — state it.

## 4. TARGET B — S-2 (TIER 1)
**NEVER contact ntfy.sh — or any ntfy host.** Every push is captured by a `fetch` stub installed BEFORE the dispatcher module is
required, with `NTFY_SERVER=http://ntfy.invalid` set before the require (read at require time); the stub THROWS on any URL that
is not `http://ntfy.invalid/…`. Record every process's outbound connections (§10.3).
1. **No push carries customer data, from every source of a push:** all three rules (unique probes in `customer_name` and
   `quote_number` on YOUR test DB), a manual `user` reminder via the REAL `POST /api/reminders` route (probe in title AND body), a
   `user` + `channel:'email'` row with no `recipient_email`, a reminder with `lead_id`/`quote_id`. Grep every captured URL, every
   header (incl. `Title`) and body for every probe VALUE. Also a huge id and a 10 KB title.
2. **Email path and digest unchanged:** a `client` reminder → the SDK recorder (never ACS): subject = title, log subject
   `Reminder #<id>`, the HTML part ESCAPED (item 4's `reminderEmail`, now present on G — parse it); the digest push = counts only.
   Diff `dispatcher.js`'s email branch between G's head and B's head — it must be byte-identical.
3. **The ntfy `notification_log` row:** subject `Reminder #<id>`; no probe value in any column.
4. **docker-compose (READ only; no docker):** `NTFY_TOPIC: ${NTFY_TOPIC:-}`; say what an unset topic does (`sendNtfy` →
   `NTFY_TOPIC not configured`; the reminder is marked `failed`) and whether that is acceptable for local dev.
5. **Sibling publishers (READ):** `dbBackup.js`'s `Backup failed: <error>`; `feedbackDigest.js`'s `formatPushSummary`. Grade each;
   neither is a B blocker unless it carries customer data.
6. **Suites and red-proof, in YOUR tree at B's head:** `npm test`, `npm run test:db` (G's cells + reminder-push 6). Red-proof:
   revert B's `dispatcher.js` hunk only (keep item 4's), keep the test → the redaction cells red, "rules write names" and digest
   green. Yours: `reminderPush` returning `rem.title` in the title only; the compose line restored.
7. **The rebase over G:** report `git diff <G head> <B head> -- server/reminders/dispatcher.js` in full and confirm nothing of
   item 4's escaping was lost in the conflict resolution.

## 5. TARGET C — A-1 (TIER 1)
**The drivable surface is `createApp(...)` in YOUR OWN harness** (the stage3 entry point cannot boot: `lib/store.js` throws
without `TABLES_CONNECTION_STRING`; no Azurite/Azure). Inject an in-memory store written to `lib/store.js`'s contract (gate 1's
`qa-harness-c.mjs` store may be COPIED after reading), a fake mail that records every send, and for the XFF legs pass
`trustForwardedFor: true` explicitly (never set `WEBSITE_SITE_NAME` in a product process; if you prove the env path, do it in a
child whose env you build, and say so). 127.0.0.1, kernel port. Real window values unless a leg says otherwise.
1. **Per source:** 6 codes for 6 DIFFERENT addresses → 6 × 200 and 6 sends; the 7th → 429, verbatim message, `Retry-After` ==
   `retryAfterSeconds` ≤ 3600, **NO send, NO `putOtp`**.
2. **Global:** 20 across ≥ 4 sources → the 21st from a FRESH source → 429 global message, one `console.error`, no send. The
   per-source message wins when both apply.
3. **Refused requests spend nothing:** a 400, a per-address 429 and a cooldown 429 each leave both budgets unchanged (count the
   remaining budget). **The converse:** a request that passes the budgets but whose send FAILS or whose `putOtp` THROWS has spent
   budget (READ: `record` runs first) — measure and say whether that is right.
4. **The window slides:** with a small `otpBudgetWindowMs`, budget returns one hit at a time as each ages out; `Retry-After`
   counts to the OLDEST hit's expiry.
5. **ADVERSARIAL PASS (C) — state the FAIL condition before each.** FAIL = more than 6 codes an hour reach the mail recorder for
   what is really one source, or a legitimate distinct source is refused.
   - **XFF forgery (trust on):** rotating LEFT entries per request → one key (the rightmost). Trust off, rotating the whole
     header → the socket key.
   - **Rightmost forgery (the residual):** with trust on and no platform in front, the caller controls the rightmost too — the
     defence rests entirely on App Service APPENDING. **NOT TESTED** (docs-based): carry it as C's top residual.
   - **Header shapes:** empty, `,`, `, ,`, trailing comma, 64 KB, two `X-Forwarded-For` headers (joined), `unknown`, a hostname,
     garbage — which key; can a caller mint unlimited keys? If so, measure that the GLOBAL 20/h still holds.
   - **IPv6 inside one /64:** full, `::` at different positions, leading zeros, upper case, `[v6]:port`, a zone id `fe80::1%en0`,
     embedded-v4 tail `2001:db8:1:2::1.2.3.4` → ONE key; different /64s → different keys. Note a /48 holder's 65,536 keys.
   - **IPv4-mapped:** `::ffff:1.2.3.4` (unwrapped) vs `::ffff:0102:0304` (hex; READ: NOT unwrapped → the `0:0:0:0::/64` bucket
     shared by every hex-mapped address) — measure, grade.
   - **Key-map exhaustion:** 20,000 distinct keys → the sweep; memory/latency bounded; no crash.
   - **Concurrency:** 50 concurrent from one source for 50 addresses → exactly 6 × 200.
6. **The `2a` rows for C**, measured — above all the negative-value row for BOTH variables.
7. **Login-page strings:** in a real browser against your harness, trigger each new 429 and capture the page's message VERBATIM
   (screenshot + `textContent`), both themes, 1280 and 375 px. Quote both.
8. **Suites, in YOUR tree:** `stage3/` `npm test` (predicted: the base's count + 10); root `node --test` (pricing). **Red-proof:**
   C's `server.js` hunks reverted, tests kept → the 10 new cells red (the `clientKey` cell by import failure — say whether that is
   a real red or an import VOID). Yours: `parts[0]` for the rightmost; the budget checks moved after `putOtp`; the `/64` truncation
   removed.

## 6. TARGET D — A-2 (TIER 2)
1. **Every response class carries all six headers, byte-exact:** `/` signed out and in, `/login`, `/healthz`, `POST /auth/request`
   200 / 400 / 429, a `/auth/verify` failure, a `requireAuth` 401, an advanced-only 403, an unknown-path 404, a **malformed-JSON
   400** and an **oversized-body 413** (body parser — is the middleware before it? READ the order), a forced 500, `HEAD /`,
   `OPTIONS /`, the quote-email route's 200. List any response missing one.
2. **`Cache-Control: no-store` on `sendFile` pages**; no 304 serves a signed-in page to a signed-out request.
3. **A REAL BROWSER, 0 CSP violations** (headless Chrome from YOUR tree, a `securitypolicyviolation` listener AND the console,
   against your harness): OTP sign-in end to end (code from your fake mail); the **FX lookup** — intercept the three FX hosts in
   puppeteer and answer with canned JSON (CSP `connect-src` is still evaluated; nothing may reach the internet), plus one fetch
   to a host NOT in the list (a violation you EXPECT); the **advanced unlock**; the **quote email** (fake mail, real renderer,
   renderer egress blocked per §10.3). Violation count per flow; any font/image/inline handler blocked. The offline `file://`
   page has no headers — say so.
4. **Framing:** a local page on another port iframing the tool → refused.
5. **The false `QUOTE MISMATCH — toggleAdvanced` log** (BACKLOG): reproduce or refute; main's behaviour, note only.
6. **Residuals:** `'unsafe-inline'` (accepted); HSTS without `includeSubDomains` (grade). **Suites:** `stage3/` `npm test`
   (base + 3); red-proof: the middleware removed → the 3 cells red.

## 7. TARGET E — A-3 (TIER 2)
1. **Server side (MEASURED, your harness):** sign in via the REAL OTP routes; `POST /auth/logout` → 200 and a `Set-Cookie`
   clearing `qqs` with `Max-Age=0` (quote it); the OLD cookie replayed → 401 on `/api/…` and the login page on `/` (the session ROW
   is gone — read your store); logout with no session → 401; a second session of the same email is NOT ended (say whether that is
   the intended scope).
2. **The offline `file://` build carries neither the button nor `/auth/logout`:** grep YOUR archived `index.html` for
   `btnSignOut`, `Sign out`, `/auth/logout` → 0, with a positive control in `stage3/public/index.html` after `node stage3/strip.js`.
3. **A real browser, 1280 and 375 px, light and dark:** beside the settings cog, one line, not clipped, keyboard reachable,
   accessible name `Sign out`. Click → `/login`; say what Back shows. Force failure (your harness answers `/auth/logout` 500, then a
   network error) → the text reads `Sign-out failed — retry`, stays; a retry that succeeds leaves. Quote both strings from the DOM.
4. **Absent from print:** a Ctrl+P-equivalent A4 PDF of the hosted page (READ the `@media print` rules) — `pdftotext` has no
   `Sign out`; the emailed PDF likewise.
5. **Adversarial:** a cross-site page (another local port) POSTing to `/auth/logout` — does the Lax cookie ride? Grade.
6. **Suites:** `stage3/` `npm test` (base + 3). Red-proof: `deleteSession` removed in a copy of the route → the replay cell reddens.

## 8. TARGET F — A-4 (TIER 2, CUSTOMER-VISIBLE)
1. **Before/after from REAL PDFs:** the REAL renderer (renderer egress blocked, §10.3) at F's BASE and at F's head, an AUD and a
   EUR quote with a live `fxRate` and a live `fx` claim; `pdftotext` both; quote the provenance line VERBATIM ("before", "after").
   **Money unchanged:** every money figure identical between the two PDFs (diff them).
2. **The bounds hold:** provider not in `CONFIG.fxProviders` (its `srcName` value, other case, trailing space, object, array) →
   seed; the printed name is CONFIG's `id` whatever `srcName` the client sent; `source` ≠ `"live"` (`"LIVE"`, `true`, object) →
   seed; USD + live claim → anchor; an old client with NO `fx` → `seeded table rate (indicative)`.
3. **ADVERSARIAL PASS (F) — injection into the PDF HTML; state the FAIL condition before each.** FAIL = any client byte other than a
   regex-passing `date` in the printed document, or any markup rendering. Beyond the builder's payloads: `date` = `2026-09-22<b>`,
   `&lt;b&gt;`, `&#60;`, a 32-char letters/spaces string (it PASSES — e.g. `live reference rate (PAY INTO ACCT 123) via Frankfurter
   (ECB)`: measure, grade against free-text `custName`/`quoteNotes`), `\n`/`\r`/` `, `["2026-09-22"]` (`String()` → passes),
   an object; extra `fx` keys (`srcName: "<img src=x onerror=…>"`, `html`, `__proto__`, `constructor`). **Any other `fxState` field
   into the PDF HTML:** READ every `fxState` use in `index.html` (`:2638`, `:2823`, `:2999`, …) and state which fields are
   interpolated. Render one hostile case; look at the page image.
4. **The test file exits on its own with a correct exit code:** `node --test stage3/test/fx-provenance.mjs` alone → exit 0 and the
   process ends (time it). **Red-proof:** break ONE assertion in a parse-checked copy → non-zero exit AND the process still exits.
   Then drop `after(closeBrowser)` in a copy → does it hang (deadline it)?
5. **Suites:** `stage3/` `npm test` (base + 1), `npm run test:print` (print-fit + fx-provenance 6), `npm run test:xlsx`.
   Red-proof: the `pdf.js` block removed → live cells red, seed/anchor green. **Print as a real PDF:** page 1 and page 2 each one
   A4 with the longest provenance line (`Open ER-API`, `22 Sep 2026`).
6. **Cross-target (READ):** H stores an allowlisted state with no `fx` and no `fxRate`; a reopened, re-emailed quote takes the
   page's `fxState` at re-email time — say whether its provenance line stays honest. J (O-1) reorders `currency` → `fxRate` →
   rest in the same `pdf.js` pass; F's block must still run AFTER the currency reset once rebased onto J — flag it (§J Q7).

## 9. TARGET G — portal integration (TIER 1): gate 1's NOT RUN portal legs, on the merged tree
1. **Install:** `npm ci --offline --ignore-scripts` at the root of YOUR archived G tree → exit code; if `ENOTCACHED`, name every
   missing tarball (gate 1's six), and the runtime legs are **NOT RUN, blocker named**. Then `node_modules` vs the lockfile, entry
   by entry (predicted 247/247).
2. **Composition (READ):** G's delta over portal main is exactly item 4's + item 1's changes plus the BACKLOG resolution (and any
   `escapeHtml` fold): `git diff d11eed6 <G> ` and `git diff ce01ba9 <G>` — every hunk that differs from a straight union is named
   and read. `email/index.js` carries BOTH the escaped fallback and `cc`.
3. **Suites:** `npm test` (predicted: main's 62 + 8 + 5 = 75 — gate 1 measured 56/64/61 only UNDER STUBS, with
   `server/quotes/pdf.test.js` failing on `pdfkit`; say whether it loads now); `npm run test:db` on YOUR test DB (predicted 5 + 4
   + 17 — watch A's BACKLOG note about a one-off `routes.test.js` before-hook failure); `escape.test.js` + `feedbackNotify.test.js`
   by name.
4. **The real `POST /api/feedback` on local Postgres** (gate 1 §3 Q2-Q4, A2 half): the SDK recorder under the portal's ACS provider
   (dummy `ACS_EMAIL_CONNECTION_STRING`/`ACS_EMAIL_SENDER`), a real signed-in session through the real login route: 201, the row
   stored, ONE `beginSend` To `kreiser.org@me.com` CC `tuesday-agent@agentmail.to`, the `notification_log` row (status `sent`,
   subject `Vision feedback #N (type)` with no title, recipient masked, and note gate 1's observation that the CC is not in the
   audit row); probe values (gate 1's list) in no mail field; the provider (i) rejects, (ii) throws in the constructor, (iii) never
   resolves, (iv) is unconfigured → each POST 201 within its deadline, row stored, process alive.
5. **The real `dispatchDue()` on local Postgres** (gate 1 §6 Q1-Q3, Q7): a client reminder with every payload class of gate 1's
   §6 Q1 in title/body → the SDK recorder captures the mail; **PARSE the HTML part** (headless Chrome `document` — gate 1's
   `qa-harness-parse.cjs` method): no element but the signature's `<p>`s, no `on*` attribute, no `href`/`src`; the text part
   unchanged byte for byte; no double-escaping of a caller's own html (quote email, approvals, settings test send).
6. **Gate 1's D and A2 harnesses, COPIED, on G's tree** — with the real `pg` this time (not gate 1's stub preload). Quote pass counts.
7. **Red-proof on G:** revert `a68b53a`'s three non-test files to main's, keep `escape.test.js` → predicted the reminder and
   fallback cells red; revert item 1's `email/index.js` + `routes/feedback.js` → 2 of 8 red (gate 1's measurement under stubs).
8. **Gate 1's C-D1 (approvals mail interpolates `p.detail` with unvalidated `inputs.currency`, raw):** re-read on G; still present?
   (Minor, internal.)

## 10. TARGET H — item 3, ROUND 2 (TIER 1)
**Harness:** COPY gate 1's `qa-harness-c.mjs` / `qa-harness-c-e2e.mjs` (read them first), update for H's `createApp` signature
(it now also carries item 1's `feedbackNotify` and the purge). In-memory store to `lib/store.js`'s contract — **extend it to
`purgeQuotes`**, written from `lib/store.js` at H, not from `store.test.mjs`.
1. **Gate 1's C legs, re-run on H:** Q1-Q4 access (creator 200; stranger 404 BYTE-IDENTICAL to not-found / malformed / old-scheme /
   expired / pending; 401s with 0 store reads; advanced withheld), Q5 store (the forbidden list derived from the page's ADVANCED
   regions, probes under every id, READ THE ROW), Q6/Q10 numbers (3 / 50 real renders, 120 fake → 99 + 21 × 503, no row behind,
   two replicas; old `…-NNN` numbers → the standard 404), the IDOR table, and the Q11 E2E in a real browser. Quote each against gate
   1's measured values.
2. **The purge (`03a0682`) — C-F1's answer:** with a frozen clock and your store: a sent quote never reopened, at 364 / 366 days,
   after `app.purgeQuotes()` → kept / GONE; a `pending` row at 59 min / 61 min → kept / GONE; a `pending` row whose creator reads it
   first; `QUOTE_RETENTION_DAYS=30` applies to rows already stored. READ the entry point: the purge runs at boot and every 6 h —
   confirm a boot purge cannot crash the boot (a store that throws in `purgeQuotes`), and that two replicas purging concurrently is
   harmless. **PROBE the real `store.purgeQuotes`** with `@azure/data-tables` replaced by a stub that records the `listEntities`
   filter and the deletes: quote the OData filter; assert it selects exactly (expired OR pending-older-than-1h) and escapes its
   values. The real service's filter semantics are **NOT TESTED**.
   **Retention honesty:** is *"kept for 12 months, then removed"* now true of the code, within the 6 h purge interval? Say it
   plainly — Tuesday relays, Kam decides.
3. **The builder's C-minor fixes (claims — verify each, state the FAIL condition first, and give EACH its own red-proof: a
   parse-checked mutant that undoes that one fix alone, and the cell (builder's or yours) that reddens — a fix with no cell that
   reddens is a finding):**
   - **C-F2:** the creator check now precedes the expired-delete: a STRANGER reading an expired number gets the identical 404 and
     the row is NOT deleted by that read (the purge removes it later); the creator's read of an expired row → 404 (and deleted, or
     not — READ). Re-run gate 1's timing leg (300 samples per class) and say whether any class separates.
   - **C-F3 (reopen rate limit — claimed 30 per session per 10 min, then 429 + `Retry-After`):** READ its numbers and key; drive 2,000 guesses → where it refuses, the
     status/body (does the 429 differ from the 404 in a way that leaks existence? it must not); the legitimate pace of §2a is not
     refused; the limit's own window slides.
   - **C-F4 (`stored:false` shown):** mail sent, update to `sent` fails → the rep's note must carry *"It could not be saved for
     reopening later, so keep the email."* — quote the string VERBATIM from the rendered page (both themes, 375 px).
   - **C-F6 (per-field caps + a 30,000-character JSON guard under the 32,767 limit; over the guard the quote MAILS but is
     unstorable):** measure `stateJson` length at the caps' maxima and at 29,999 / 30,000 / 30,001; multi-byte text (the real
     Table Storage limit is in UTF-16 units — does the guard count characters or bytes? say which is right); over the guard: the
     mail goes, no row (or no stored state) is left, the rep is told (quote the note); no partial row.
**ADVERSARIAL PASS (H) — state the FAIL condition before each.** FAIL = any response or side effect that differs between "exists
   but not yours" and "does not exist", a stranger's action that changes another person's row, or a limit a caller can reset for free.
   - **The limiter as an oracle:** the 429 is decided BEFORE the lookup (READ) — confirm by measurement that the 30th/31st request
     behaves identically for real, foreign, malformed and nonexistent numbers.
   - **Resetting the limiter:** a new session (sign in again — which costs an OTP under C's budgets on C's head, but NOT on H's head,
     where C is absent: say what the reset costs on H alone), two sessions in parallel, a forged/expired cookie (401 before the
     limiter?), the 10,000-key sweep.
   - **The purge as a weapon:** can any request make the purge delete a row early (a crafted `createdAtMs` via the POST? READ the
     write path), or make a boot purge hang the boot (a store whose `purgeQuotes` never resolves — the entry point does not await it:
     confirm the listener still starts)?
   - **The 30,000 guard:** a POST just over it with multi-byte characters; a POST that is under 30,000 characters but over 64 KiB in
     UTF-8 — say which the real store limit counts.
4. **A1 × item 3 (gate 1 measured a real `server.js` conflict):** H is rebased onto a main that contains item 1, so H's tree IS the
   merge result. Re-run gate 1's A1 harness (CC, probes, failing mailbox) on H — the conflict was in the `createApp` signature both
   touch.
5. **Suites, in YOUR tree:** `stage3/` `npm test` (server + strip + store), `npm run test:print`, `npm run test:xlsx`, root
   `node --test`. **Red-proofs:** gate 1's (creator check removed, allowlist pass-through, reserved number not passed to the
   render — count the reds honestly this time); the purge's `pending` branch removed → does a cell redden?; the creator/expiry order
   swapped back → does a cell redden now (gate 1: GREEN)?; the rate limiter removed → does a cell redden?
6. **Carried C findings:** for C-F7 (container-clock stamp), C-F8 (`Infinity`/`0x10`/`1e3`), C-F9, C-F10, C-F11 — changed by H or not.

## 11. TARGET I — A-5 (TIER 2, build recipe only)
**No `docker` in this gate (§13 HELD). The image build itself is NOT RUN — say so.** Prove the image CONTENTS before/after without it:
1. **The build context, emulated (PROBED):** from YOUR archived trees at I's base and I's head, compute the file set Docker would
   send as the context, applying `.dockerignore` with Docker's own matching rules (Go `filepath.Match` per path component, `**`,
   leading/trailing-whitespace trimming, `!` exceptions; READ the rules — name the implementation you used; if a dockerignore
   matcher is already in a tree's `node_modules`, prefer it; never install one). Then simulate the Dockerfile's `COPY`s: list what
   lands in `/app/stage3/` in each case. **Seed each tree with a fake `stage3/node_modules/SENTINEL` and a stale
   `stage3/public/index.html`** (the laptop conditions the defect describes) and show: at the base, both ride into the image and
   overwrite; at I, neither does.
2. **`npm ci --omit=dev` vs the lockfile (PROBED):** in a copy of `stage3/` at I, run `npm ci --omit=dev --offline --ignore-scripts`
   (the image runs WITHOUT `--ignore-scripts` — say what install scripts the prod set has, READ) and prove the installed set equals
   the lockfile's non-dev entries, entry by entry. Say what `npm ci` does if the lockfile is missing (the `package-lock.json*` glob
   would then copy nothing — READ: `npm ci` refuses; confirm by running it in a copy without the lockfile, offline).
3. **Nothing needed is excluded:** `strip.js` needs `../index.html` (copied explicitly) — confirm `strip.js`, `lib/`,
   `login.html`, `server.js` are in the context; `.git` exclusion breaks nothing at build or run time (grep for runtime reads of
   `.git`); `Screenshots_for debugging` (a space) is matched as intended.
4. **Suites:** none change; `stage3/` `npm test` on I (== base) as a control. **Residual:** `az acr build`'s handling of
   `.dockerignore` and the real image are **NOT TESTED**.

<!-- SLOT-J:BEGIN -->
## J. TARGET J — O-1: typed service rates reach the PDF and xlsx (TIER 1, customer money) — present because SLOT-J: IN
*Builder claim (Tuesday, 19:46): pass 3 applies currency, then fxRate, then the rest; no posted prices → `applyPsvRates` re-derives
at the POSTED rate; `report.docText`; `closeBrowser`; 5 cells in `test/typed-rates.mjs`.* **The builder's cells read `docText` and
the workbook rows; YOU read real PDFs.**
1. **Before/after from REAL documents** (the real renderer, egress blocked per §13.3), at J's BASE and J's head, each case in
   COLLECTOR ORDER (DOM order: price inputs before `currency`), `pdftotext` the PDF AND read the xlsx cells: (i) USD with typed
   Advanced $2,000 and custom $300/h; (ii) AUD typed A$3,000 / A$450 h with a posted live `fxRate`; (iii) untouched rates exactly as
   the collector posts them (the browser's own values); (iv) NO price fields posted; (v) the posted `fxRate` printed (the FX line and
   every converted figure use it, not the seed). Quote the before/after money lines VERBATIM, and the totals, and show the totals
   equal the rep's on-screen total (drive the page in a browser for the screen figure, same inputs).
2. **F8's single-rate invariant across EVERY line of the document:** for each converted-currency case, recompute every money line
   (licences, services, PoC, Workpath, totals) from USD list at ONE rate and show no line was priced at a different rate. Name any
   line that disagrees.
3. **ADVERSARIAL PASS (J) — state the FAIL condition before each.** FAIL = a printed price that is neither the rep's typed value nor
   the list value at the posted rate, a document carrying two rates, or a crash/500.
   - every other CONFIG currency: EUR, GBP, NZD, SGD, DKK (typed and untouched);
   - a posted `fxRate` of `0`, `-1`, `NaN`, `""`, `"abc"`, `1e308`, `0.0000001`, and one with a thousands comma — what prints, and
     does the invariant hold (the formula falls back to the seed on a falsy parse — does that give TWO rates when prices were typed?);
   - HOSTILE ORDER: prices posted AFTER `currency` and `fxRate` in the JSON; `currency` posted twice (JSON last-wins); `fxRate`
     without `currency`; a currency CONFIG does not have (`XXX`, `usd`);
   - **PoC gating not regressed (`3b67aac`):** a PoC quote (advanced session, PoC ticked, `pocDevices`, `poc-own`) renders the PoC
     lines in PDF + xlsx exactly as at the base; the `cleared` report stays empty; a SIMPLE session's PoC ids are still refused.
4. **Red-proof:** J's pass-3 reordering reverted (keep the tests; parse-checked) → which of the 5 cells redden; the re-derive block
   removed → does the no-price-fields cell redden?; your own: the order fix applied to `currency` but not `fxRate`.
5. **The test file exits on its own** (as §8 Q4 for F): `node --test stage3/test/typed-rates.mjs` → exit 0, process ends; one
   assertion broken in a copy → non-zero and still exits.
6. **Suites:** `stage3/` `npm test` (unchanged by J), `npm run test:print` (print-fit + typed-rates 5), `npm run test:xlsx`, root
   `node --test`. **Print as a real A4 PDF**, page 1 and page 2, with the longest service lines.
7. **J × F (A-4):** both sit side by side on `1f3df8d` and CONFLICT textually (same `page.evaluate`, same `closeBrowser`); the
   builder merges O-1 first and rebases A-4 onto it at merge time. Quote `merge-tree` J × F (own object dir); do NOT resolve. Name
   the cells to re-run on the rebased F: J's 5 + F's 6 together, and one render exercising both (typed AUD rates + a live `fx`
   claim) — the typed rates, the posted rate and the `live reference rate (…) via …` line correct in ONE document.
<!-- SLOT-J:END -->

## 12. Across targets — merges and the queue
**Every prediction below is a READ from `git diff -U0` hunk ranges: portal rows at the drafting shas, QuickQuote rows at the
PINNED rebased heads over `1f3df8d` (read 19:47-19:50). Quote `git merge-tree --write-tree --name-only` from YOUR OWN object
directory for each pair, or say you skipped it.** The builder rebases each in merge order at merge time; your job is to say which
pairs conflict and which cells must be re-run on each rebased head — never to resolve a conflict.

**Merge order and the KNOWN future conflicts (builder + Tuesday, 19:47):** QuickQuote **item 3 (H) → A-1 (C) → A-2 (D) → A-3 (E)**,
all on the `createApp` region / `server.test.mjs` tail; **O-1 (J) → A-4 (F)** on the `lib/pdf.js` evaluate; **A-4 (F) / A-5 (I) /
`fix/qq-puppeteer-25-2026-09-22` (`3d0167e`, NOT a target: puppeteer-core 25.0.2 + a node:22 image; `stage3/package.json`,
`package-lock.json`, `Dockerfile`)** on `package.json` / `Dockerfile`. Portal: G (item 4 + item 1) → B (S-2, already on G) → A (S-1).

| pair (pinned QuickQuote heads / drafting portal shas) | files both sides change | READ prediction |
|---|---|---|
| H `c8fb771` × C `3c8d3a4` | `stage3/server.js`, `stage3/test/server.test.mjs` | **CONFLICT**: both edit the `createApp` signature `:74`; both append after `server.test.mjs:836` |
| H × D `ae33a94` | `server.js`, `server.test.mjs`, `BACKLOG.md` | server.js likely clean (D inserts after `:89`; H after `:70` and at `:74`); test tail after `:836` **CONFLICT**; BACKLOG both after `:80` **CONFLICT** |
| H × E `7ccd119` | `stage3/strip.js`, `server.test.mjs` | **CONFLICT**: both insert after `strip.js:246`; test tail |
| H × F `0b9551a` | `stage3/lib/pdf.js`, `stage3/package.json`, `stage3/strip.js` | **CONFLICT likely**: pdf.js H `:111`/`:137` vs F after `:109`/`:136`; package.json H `:10` vs F `:11` (adjacent); strip.js H `:241` vs F `:237` (close — measure) |
| H × J `0bdbd93` | `stage3/lib/pdf.js`, `stage3/package.json` | **CONFLICT likely**: pdf.js `:136`/`:137` adjacent; package.json `:10`/`:11` adjacent |
| C × D, C × E, D × E | `stage3/test/server.test.mjs` (C × D also `server.js`) | **CONFLICT** — each appends after `:836`; C × D in server.js likely clean (C `:74`, D after `:89`) |
| E × F | `stage3/test/strip.test.mjs` | **CONFLICT** — both append after `:161` (`strip.js` E after `:246`, F `:237`: clean) |
| J × F | `stage3/lib/pdf.js`, `stage3/package.json` | **CONFLICT** — both change `:136` (report fields) and `:149` (`closeBrowser` export), both edit `test:print` `:11` |
| I `b9890c3` × `3d0167e` (puppeteer, not a target) | `stage3/Dockerfile` | measure (I edits the install line `:19`; `3d0167e` changes the base image and may touch the same region) |
| I × any target | `BACKLOG.md` (`:208`, `:604`) | clean |
| item 4 `d11eed6` → B `1c726bb` | `server/reminders/dispatcher.js` | CONFLICT at drafting (both insert after `:20`; both rewrite `module.exports` `:151`) — **resolved by B's rebase onto G; verify §4 Q7** |
| **A `89af8ba` × G `4e0dc02` — REQUIRED (Tuesday: A stays off main, NOT stacked)** | `server/routes/feedback.js`, `BACKLOG.md` | feedback.js likely clean (item 1 after `:12`, `:184`; A at `:9`, `:79-81`, `:131`, `:255-257`, `:332-336`); **BACKLOG CONFLICT likely** (all append after `:136`). Measure it from your own object directory; if feedback.js merges clean, archive that result and run A's `feedback-auth` cells + G's feedback-route leg on it (PROBED) |
| A × B `00c5201` | `DEV-SESSION-SUMMARY.md`, `BACKLOG.md` via G | as A × G, plus DEV-SESSION-SUMMARY clean (A `:66-67`, `:396`; B `:105`) |

- **Do NOT hand-resolve any conflict.** For each CLEAN pair, archive the merge RESULT into your project and run that repo's `npm
  test` on it (PROBED).
- **A GO is a GO at the pinned sha only.** Name, for each target, the cells to re-run on its rebased head after the target ahead of
  it merges (at least: C, D, E each re-run on H-merged main — the `createApp` signature and the `server.test.mjs` tail; F re-run on
  J-merged main — §J Q7; I re-run against the puppeteer image change). **CI:** `gh` is not authenticated for `datasecau`; every
  target's CI half is **NOT RUN**, measured at merge.

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (`session-tools/nexusai-lock.sh`).
1. **The Vision builder seat is LIVE** (claude `1613`, pane `%41`) and owns portal `:4848` and stage3 `:8080`. **Gate 1's QA seat**
   (claude `87320`, pane `%43`) may still be alive. **Never use 4848 or 8080**, nor `47787` (Tuesday's dashboard), nor any port
   another seat holds. Take every port from the kernel (listen on 0) and bind `127.0.0.1` wherever YOUR harness listens. Never start
   the portal's entry point (it binds `0.0.0.0` in `main()`).
2. **Postgres = the running local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all.**
   Create `vsp_qa_g2_<epoch>` for app runs and `vsp_qa_g2_test_<epoch>` as `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs — never
   point it at `salesportal`, `salesportal_test`, or any `vsp_qa_g1_*` database). The connection uses the repo's LOCAL defaults in
   `server/db.js` / `scripts/ensure-test-db.js`; never anything from `Vision_Sales_Portal/4_Credentials/`. Use the `pg` client from
   YOUR `node_modules` (no `psql` here). If `:5433` does not answer, the portal runtime legs are **NOT RUN, blocker named** — do not
   start a container. Leave your databases in place and list their names (no DROP).
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH, HOME = a fresh mktemp dir, TZ, NODE_ENV = `test`
   or `development` — never `production` — PORT, a fresh random SESSION_SECRET / unlock word / `COORDINATOR_SECRET` you generate,
   DATABASE_URL / TEST_DATABASE_URL = yours, PUPPETEER_EXECUTABLE_PATH, `NTFY_SERVER=http://ntfy.invalid`, dummy provider values).
   **NEVER set in a product process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX` (with both set, QuickQuote SENDS FOR REAL), any real
   `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`,
   `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product process's env KEY NAMES (never values) and assert none is forbidden.
   **Egress — including Chrome children:** the real QuickQuote renderer's page calls three public FX APIs whenever currency ≠ USD
   (gate 1 O-4). **Block it** — e.g. a preload in YOUR harness that wraps the renderer's puppeteer launch to add
   `--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1` (or request interception on every page the renderer opens) — and
   **prove the block with a positive control** (one renderer page's FX fetch is attempted and fails, recorded). Record outbound
   connections of EVERY process you start, Chrome children included (`lsof -nP -iTCP` over the whole process tree, not just node).
   Anything but `127.0.0.1` is a finding against your harness or the product.
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND an entry point of
   either app (the portal's server entry file, the stage3 server file, or your own harness file) ANYWHERE in the remaining argv,
   from the kernel; **"ours" = the ancestor chain CONTAINS your claude pid**. Chrome children of your renderer count as yours and
   must be reaped. **Negative controls, same run, must classify FOREIGN:** the Vision builder's claude `1613` (pane `%41`), Tuesday's
   claude `45678` (pane `%0`), and gate 1's claude `87320` (pane `%43`) if still running. Re-read them at start; if one has exited,
   say so and use the others. Never by `EADDRINUSE`, a whole-command-line grep, or raw `comm`. Method:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorcount.py`
   (with `qa-floorlib.sh`), or gate 1's Vision copy — COPY either into your own evidence folder; edit neither original. **A zero is
   reportable only beside a control that fired in the same window** (spawn one server your way, the count must RISE, reap it).
5. **THE DEADLINE RULE:** every real-server, browser and database step has a written DEADLINE (boot 60 s, request 30 s, render 60 s,
   DB connect 15 s, exit 20 s) and a client timeout on every request (this machine has no `timeout` binary — gate 1 voided a reading
   on it; build deadlines into your own runner); a step past its deadline is ABORTED and reported (a hung product request IS a
   finding). **Every server, browser and child you start is killed in a `finally`** (SIGTERM, then SIGKILL after a grace), confirmed
   by your counter. **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes;
   a step with no heartbeat for 5 minutes is aborted and reported.** C's key-exhaustion leg, D's browser flows, F's exit-code leg and H's 50-render leg are the
   shapes that hang.

**Reap every server and every Chrome you start.** An orphan of yours is someone else's foreign process.

### Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (App Service `hpas-quickquote`, resource group `hpas-quickquote-rg`, its ACR `hpasqqacr`, its Table
  Storage) **or the live portal** (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` —
  PRODUCTION: the live site, its Postgres `datasec-sales-db.postgres.database.azure.com` and key vault). No request to either host,
  no DB connection to either, not even a GET or a health probe. **Never ntfy.sh** or any ntfy host (stub the fetch). **Never the
  three FX hosts** (intercept in your browser; block in the renderer). Never run the `.cursor` rule's curl lines. Never the
  Feedback_System coordinator.
- The portal: `createApp()` in YOUR harness, on LOCAL Postgres, `env -i`. QuickQuote: `createApp` in YOUR harness, and the offline
  `index.html` from `file://`.

### HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npx` of anything not
  already in your tree.** The launcher points `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Real sends are OFF.** Every provider is a recorder you wrote; nothing reaches ACS, Agent Mail, ntfy or an FX host from a product
  process, a renderer or a browser you drive.
- **Findings-only:** do not commit, do not move any branch, do not file a ticket, do not write inside either repo, inside
  `Vision_Sales_Portal/`, inside `Feedback_System/`, or inside gate 1's report folder. The gate fixes nothing.
- **NEVER `rm`** — quarantine, per the template §5; every preload, stub, harness and fixture lives under YOUR project.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate2/report.md`

**Questions:** your sender `QA/Datasec-Vision` has NO inbox routing line in the fleet — you cannot receive an answer reliably. If
you must ask, mail `tuesday-agent@agentmail.to`, subject `[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one
Question / Meanwhile / Needed-by), **and proceed on the safest reading without waiting**; record the question and the reading you
took in the report.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 2: S-1 + S-2 + portal integration (tier 1) + item 3 round 2 (tier 1) + A-1 (tier 1) + A-2..A-5 (tier 2), heads as pinned at launch`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the QA
project has none. Use it ONLY in your own verdict/question `curl`; it must never enter a product process's environment (§13.3).
Never put the key, or any secret, in a mail or the report.

Verdict format:
- **A (S-1), B (S-2), C (A-1), D (A-2), E (A-3), F (A-4), G (portal integration), H (item 3 round 2), I (A-5)** — and **J (O-1)**
  if IN — each **GO / NO-GO**, stated SEPARATELY PER TARGET, each naming its pinned sha and branch. For G, state separately what it
  means for gate 1's A2 and D conditions. For H, state whether C-F1 is closed.
- The verbatim strings Kam's publish ask needs: C's two refusal messages as the login page renders them; E's `Sign out` and
  `Sign-out failed — retry`; F's BEFORE and AFTER provenance lines from real PDFs; B's push title and body; H's `stored:false` note;
  J's before/after money lines (if IN).
- Then one paragraph on the queue quoting §12's merge-tree results (or that you skipped them): which GO survives which merge order,
  which cells must be re-run on each rebased head, and that every target's CI half is NOT RUN (gh unauthenticated).
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section — at least: real App Service `X-Forwarded-For` (C's
  defence rests on it), the live Table Storage session delete (E) and purge filter (H), real ACS/Agent Mail/ntfy delivery, the live
  ntfy topic's value (B), the Feedback_System poller after merge, the real Docker image and `az acr build` (I), Node 20 (this machine
  runs node v26; both apps ship on Node 20), CI, the stage3 entry point's boot). Every action recommendation carries its evidence
  class: MEASURED AT RUNTIME / PROBED / READ ONLY. §3 Q3, §3 Q5, §4 Q1, §5 Q5, §6 Q3, §8 Q3, §9 Q4-Q5, §10 Q2-Q3 and §11 Q1 must
  each carry one.
- Report each pinned head, and both mains, as three timestamped readings (start / mid / end), each with its branch name.

PROVENANCE:
- drafting heads (NOT the gated heads — §PIN is filled at launch): portal main ef5a9c0b942c…, fix/feedback-report-auth-2026-09-22 89af8ba7817f…, fix/reminder-push-redaction-2026-09-22 1c726bbda7e4…, fix/mail-html-escape-2026-09-22 d11eed6af2bb…, fix/feedback-mail-cc-tuesday-2026-09-22 ce01ba95fa9e…; QQ main 47eb533034108c… then 1f3df8ded0a8… (merges of bd3e3cf and 72f6c0c), feat/qq-otp-send-budget-2026-09-22 8a157bbe2924…, feat/qq-security-headers-2026-09-22 f6ca31ff467b…, feat/qq-sign-out-2026-09-22 57b373c2a638…, fix/qq-pdf-fx-provenance-2026-09-22 6eb367e76e1e…, feat/qq-open-old-quote-2026-09-22 03a0682470c8…, fix/qq-dockerignore-2026-09-22 ebbc9535a81e…; integration/portal-gate2-2026-09-22 ABSENT | `git -C <repo> ls-remote origin` | read 2026-09-22 19:30:35, 19:31:40, 19:34:45, 19:40:09 AEST
- chains: 8df198a (parent ef5a9c0) → fb907b9 → 89af8ba; 1c726bb, 8a157bb, f6ca31f, 57b373c, 6eb367e, ebbc953 each one commit on 47eb533/ef5a9c0; 03a0682 parent 642b06b; 1f3df8d = merge(d757984, 72f6c0c), d757984 = merge(47eb533, bd3e3cf) | `git log --format='%H %P %s'`, `merge-base` | read 19:30-19:41
- file sets / numstat; lockfile blobs 9d426df (portal) and 64e49cb (stage3) unchanged by every drafting target | `git diff --numstat`, `git rev-parse <sha>:<lockfile>` | read 19:30-19:41
- mechanisms, strings, line numbers; trust proxy `server/index.js:44`; createApp/main split; ntfy publishers; login.html rendering; Dockerfile | `git diff`, `git show <sha>:<file>`, `git grep` | read 19:31-19:45
- break list: Feedback_System poller.js:43 (not a git repo), `_archive/…/poller.js:50`, `.cursor/rules/check-feedback-workflow.mdc:44/:120` | `sed -n`, `git show 89af8ba:<file>` | read 19:33
- gate 1's verdicts, NOT RUN list, C findings, O-1..O-5, harness file names, self-findings | `…/2026-09-22-vision-qq-gate1/report.md` (547 lines) + `ls evidence/` | read 19:42-19:46
- test counts: portal test/db at ef5a9c0 5/4/17, + feedback-auth 10 (A), + reminder-push 6 (B); stage3 server.test 40 + strip 12 = 52 at 47eb533; new cells C 10, D 3, E 3, F 1 + fx-provenance 6 | `grep -c '^test('` on `git show` | read 19:33-19:36
- builder claims / READY times / merge order / item 6 offline npm ci | Tuesday daily note `0_Brain/daily_tuesday/2026-09-22.md` 19:11-19:29 lines; Tuesday's SCOPE UPDATE message | read 19:33, 19:41 (mail bodies NOT read)
- seats: %41 → claude 1613 (Vision), %0 → claude 45678 (Tuesday; gate 1's brief named 63076, which exited), %43 → claude 87320 (gate 1 QA), %44 → 8360, %36 → 57419 (NexusAI) | `tmux list-panes -a`, `ps -axo pid,ppid,comm` | read 19:32
