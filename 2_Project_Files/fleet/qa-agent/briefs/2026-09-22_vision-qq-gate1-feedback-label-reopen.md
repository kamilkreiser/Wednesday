# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, BATCHED GATE 1 (QuickQuote + portal): item 1 feedback CC (TIER 2, two repos), item 2 device label (TIER 2), item 3 reopen an old quote by number (TIER 1), item 4 portal mail HTML escaping (TIER 1)

**Drafted for Tuesday 2026-09-22 18:30-18:55 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on four READY FOR QA mails from the Vision_Sales_Portal agent (sent via `coagent@`), all in `tuesday-agent@agentmail.to`:
- item 1 (QuickQuote `bd3e3cf` + portal `ce01ba9`), 2026-09-22T08:21:17Z, id `<010001a0c8347c1f-ee550842-4d4f-4d8a-ac4b-ba75fffd4fc4-000000@email.amazonses.com>`;
- item 2 (QuickQuote `72f6c0c`), 2026-09-22T08:22:58Z, id `<010001a0c836056a-9c13ff1f-9ad7-4780-ab83-572d94a34e4a-000000@email.amazonses.com>`;
- item 3 (QuickQuote `642b06b`), 2026-09-22T08:33:17Z, id `<010001a0c83f756c-c3207496-e163-44a6-9550-7d28239dd1b9-000000@email.amazonses.com>`;
- item 4 (portal `d11eed6`), 2026-09-22T08:40:37Z, id `<010001a0c8462c34-57ae3724-3346-415b-8218-d1a8d737eebc-000000@email.amazonses.com>` (added to this gate by Tuesday mid-draft).
**All five heads are pinned here; nothing is pinned at launch.** The launcher re-reads each by `git ls-remote` immediately before launch and refuses on any mismatch.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-22 18:53
Self-check note: Tuesday read the section map and sections 9-11 whole plus the drafter's wrong-at-source list (ctx 77%, so the target sections were read via the drafter's summary, not line by line). npm ci --offline --ignore-scripts is CONFIRMED for this gate. Item 3 has two known defects (the lazy-only retention purge; a margin cell asserting nonexistent ids); the builder is fixing them on the same branch, so expect a C re-run.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build any of these changes and you owe no builder anything. **Every line below that reports
what a builder says is a CLAIM, never evidence.**

**ONE batched gate, FOUR targets, TWO repos, ONE session** (Kam's standing rule of 2026-09-18: batch gates, never pay for the
same setup twice). **Give a SEPARATE verdict for each: A GO / NO-GO (with A1 QuickQuote and A2 portal stated separately,
because they merge separately), B GO / NO-GO, C GO / NO-GO, D GO / NO-GO.** Tiers:
- **A (item 1, feedback CC) is TIER 2** (through-code, mail plumbing), in both repos. The gate still checks that no secret,
  margin or buy-price reaches a mail, and that a failing mailbox never fails a submission.
- **B (item 2, label) is TIER 2** (through-code plus a real render).
- **C (item 3, reopen by number) is TIER 1**: an access control, and a NEW stored store of customer data (customer name,
  notes, deal size) kept for a year.
- **D (item 4, mail HTML escaping) is TIER 1**: `server/reminders/dispatcher.js:109` on portal main is a LIVE path — a portal
  user's reminder title/body reaches a CUSTOMER's inbox (`recipient_email`) as live HTML today.

## RULED BY KAM, AND SETTLED (Vision `1_Project_Definition/CLARIFICATIONS.md`, C-01..C-05)
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` — read it whole. In short:
- **C-01** (Kam, 13:38:02 AEST): *"It would be good if all feedback tools CC'd you in on them"* — "you" = the Tuesday seat,
  CC target `tuesday-agent@agentmail.to`, Kam keeps his own copy. Not covered: publishing. **C-02**: start now (timing only).
- **C-04**: `Devices (MFPs)` → `Devices (MFPs/SFPs)`, wording only, no pricing. The builder's two further wording proposals
  (printed "Quote details" line, xlsx "Devices" row) are **Kam's to choose and NOT built** — do not test them as if they were.
- **C-05** (Tuesday's ANSWER 08:24Z, grounded in Kam's tester-thread words in C-03): stored-quote lookup, **creator only
  (session email == stored creator), one identical 404 for "not found" and "not yours"**, server-issued unique numbers,
  re-email makes a NEW number, the old quote is never edited, **no admin override** (QuickQuote has no admin role; the HPAM
  word is a workflow gate, not a security control — Kam 2026-08-11). Accepted defaults: **12-month retention, lazy delete on
  read, ONE config value**; no retrieval for quotes emailed before this ships. Not covered: the offline `file://` tool;
  emailing the creator on a lookup.
- **Both defaults WERE stated to Kam** on the Tuesday board (read in `0_Brain/dashboard/data/chat_tuesday.json`): *"Quote
  numbers from the online tool will end in 'H01' instead of three digits … Default: keep it."* and *"saved quotes are kept
  for 12 months, then removed … That's a single setting."* Weigh that second sentence against Q-C9 below ("then removed"
  is true only for rows that are READ).
- The QuickQuote repo's own rules: `Quoting Tool/hpas-quoting-tool/CLAUDE.md` (single offline HTML file; version discipline;
  **always verify print as a real PDF**; nothing in the sub-project goes near Azure). Read it.

## PRIOR ROUND
- **All four targets are ROUND 1.** None has been gated. There is no earlier Vision/QuickQuote gate launcher or report in
  the fleet; the QA project has no `projects/vision/` directory yet — create it for your report.

## 1. Targets — verified at drafting from the object store (18:35-18:43 AEST)
**origin, by `git ls-remote origin …`, read 18:35:31 and again 18:43:08 AEST (same values both times):**
QuickQuote (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool`, remote
`datasecau/vision_hpas-quickquote`): main `47eb533034108c5c92d6b36af44554528ffc71ec`;
`fix/qq-feedback-cc-tuesday-2026-09-22` `bd3e3cf730cfda7d29c74c389e46c8c9d62b2005`;
`fix/qq-mfp-sfp-label-2026-09-22` `72f6c0cc93d52da98ca2205496522b9d82875b26`;
`feat/qq-open-old-quote-2026-09-22` `642b06b4857155cdfdadab2228aad751fb45ce44`.
Portal (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files`, remote
`datasecau/vision_datasec-sales-portal`): main `ef5a9c0b942c71b8c3b08feec22ae23dbe622581`;
`fix/feedback-mail-cc-tuesday-2026-09-22` `ce01ba95fa9e074f0e5ed8d4e429600cf0eadb24`;
`fix/mail-html-escape-2026-09-22` `d11eed6af2bbb8b96e1985d26da8eccf5205612b`.
**Queue neighbours, NOT targets of this gate:** QuickQuote `fix/qq-qs-advisory-2026-09-22` `320a169` (lockfile only: qs
6.16.0 / express 4.22.3 / body-parser 1.20.8 — announced READY in item 3's mail, NOT commissioned here) and
`backlog/qq-qnum-collision-2026-09-22` `44405c6` (BACKLOG.md only).

**Every QuickQuote target is ONE single-parent commit off `47eb533`. A2 is one commit off `ef5a9c0`. D is two commits off
`ef5a9c0`: `a68b53a600c301a045ec83d00a90ca02c70308b8` (the fix) then `d11eed6` (BACKLOG.md only).** Both mains are unmoved
since the targets were cut. `stage3/package-lock.json` is byte-identical at `47eb533`, A1, B and C (blob `64e49cb`); the
portal `package-lock.json` is byte-identical at `ef5a9c0`, A2 and D (blob `9d426df`). **No target changes a dependency.**

### TARGET A — item 1: feedback CCs Tuesday (TIER 2), TWO repos
- **A1 QuickQuote `bd3e3cf`, five files, +149/−7:** `stage3/server.js` (a `DEFAULT_FEEDBACK_NOTIFY =
  "kreiser.org@me.com,tuesday-agent@agentmail.to"`; `parseRecipients`; first address = To, the rest = CC on ONE send;
  `createApp` THROWS on a list with no address), `stage3/lib/mail.js` (`cc` on both the ACS and the Agent Mail provider),
  `stage3/package.json` (test script adds `test/mail.test.mjs`), `stage3/test/mail.test.mjs` (A), `stage3/test/server.test.mjs`.
  Env name: **`FEEDBACK_NOTIFY_EMAIL`** (singular). The feedback send stays off the response path
  (`mail.send(...).catch(...)`, not awaited).
- **A2 portal `ce01ba9`, five files, +218/−3:** `server/feedbackNotify.js` (A: its own `escapeHtml`, `notifyRecipients`,
  `buildFeedbackMail`, `notifyFeedback` which never throws), `server/feedbackNotify.test.js` (A), `server/routes/feedback.js`
  (+4: `notifyFeedback(result.rows[0], req.session.user)` after the INSERT, not awaited), `server/email/index.js` (`cc` on the
  ACS provider and through `sendEmail`), `BACKLOG.md` (the unescaped-HTML entry that D now fixes). Env name:
  **`FEEDBACK_NOTIFY_EMAILS`** (PLURAL) — the builder calls it "same shape and default" as QuickQuote's; the NAMES differ.
- Claimed: QQ stage3 `npm test` 57/57 (was 52), pricing 66/66, red-proof 5 fail with `server.js` + `lib/mail.js` reverted;
  portal `npm test` 70/70 (8 new), `test:db` 5+4+17 on local Postgres, red-proof 2 of 8 fail; the real route run on LOCAL
  Postgres under `env -i` with `scripts/e2e-feedback-test.js` → 3 items, 3 `notification_log` rows, subject
  `Vision feedback #N (type)`, status `skipped` (no provider locally).

### TARGET B — item 2: `Devices (MFPs/SFPs)` (TIER 2)
- **QuickQuote `72f6c0c`, two files:** `index.html` — exactly TWO changed lines (numstat 2/2): `:1251`
  `<label for="devices">Devices (MFPs)</label>` → `Devices (MFPs/SFPs)`, and `:1655` `toolVersion: "2.30"` → `"2.31"`;
  `quote-engine.test.mjs` +12 (one test). Claimed: pricing 67/67, stage3 52/52, print-fit 18/18, xlsx-parity 5/5; headless
  Chrome render of `file://index.html` light + dark at 1280 and 375 px; the label is not laid out in print media.

### TARGET C — item 3: reopen an old quote by its number, creator only (TIER 1)
- **QuickQuote `642b06b`, seven files, +562/−14:** `stage3/server.js` (+145), `stage3/lib/store.js` (a `quotes` table:
  `reserveQuote` = `createEntity`, 409 → false; `updateQuote` Merge; `getQuote` 404 → null; `deleteQuote` swallows errors),
  `stage3/lib/pdf.js` (prints the number it is given), `stage3/strip.js` (+91: the "Open a previous quote" box, hosted page
  only), `stage3/test/server.test.mjs` (+273, "+12 cases", 64/64 claimed), `CLAUDE.md` (Stage 3 note), `BACKLOG.md` (+12).
- **Mechanism (READ, `git diff 47eb533 642b06b -- stage3/server.js`):** `POST /api/quote/email` reserves
  `DSQ-YYYYMMDD-HHMMSS-H01..H99` (stem from the SERVER's local clock; `SERVER_QNUM_RE = /^DSQ-\d{8}-\d{6}-H\d{2}$/`) BEFORE
  rendering, with `creator = req.session.email`, `status "pending"`, `advanced`, and
  `stateJson = storableQuoteState(state, advanced)` — an ALLOWLIST: `QUOTE_FIELD_IDS` = devices, term, currency, custName,
  quoteNotes, qty-custom, price-basic, price-advanced, price-custom, pocDevices, wpReady; `QUOTE_CHECK_IDS` = registerDeal,
  mode-bundle, mode-mix, five app-*, four svc-*, svcSimpleYes/No, poc, poc-own, wpReadyChk; `QUOTE_ADVANCED_IDS` (poc,
  poc-own, pocDevices, wpReadyChk, wpReady) kept only for an advanced session. 99 clashes in one second → **503**. The render
  must print the reserved number or the route 500s. After the mail, `status "sent"`; a failure there → 200 `stored:false`.
  `GET /api/quote/:qnum` (requireAuth): trim + toUpperCase; regex → store read → `status !== "sent"` → retention (on
  `createdAtMs`; **expired rows are deleted here, before the creator check**) → `row.creator !== req.session.email` — every
  refusal the same `404 {"error":"quote not found"}`; the state is re-filtered on the way OUT for a simple session
  (`advancedWithheld`). Retention: `QUOTE_RETENTION_DAYS` (default 365), non-positive/NaN → `createApp` throws.
- **Where the ids live (READ, `index.html` at `642b06b`):** the ADVANCED sentinel regions are SVC `:1265-1310` (holds
  `wpReady :1280`, `pocDevices :1298`), UI `:1538-1591` (holds the margin inputs `cpDay :1551`, `cpMonth :1556`,
  `cpYear :1560`, `cpTerm :1564`, `cpPct :1570`), PM `:1600-1610`, JS `:3274-3399`, SEAM `:3574-3585`. `psvHourly :1213` is the
  saved-PS-rate panel. **`price-basic :1427`, `price-advanced :1434`, `price-custom :1447`, `qty-custom :1448` are STORED and
  sit OUTSIDE every ADVANCED region** — rep-entered service prices labelled "Unit price" / "rate/hr", placeholder POA. The
  drafter reads them as SELL-side; Q-C5 asks you to establish it, not assume it.
- **Numbers:** the offline tool's `quoteNumber()` (`index.html:2384`) is `DSQ-YYYYMMDD-HHMMSS-NNN`, NNN = a page-local
  counter `% 1000`, local time; every hosted number so far ended `-001`. Server numbers end `H` + two digits.
- **Storage is Azure Table Storage** (`@azure/data-tables`, `TABLES_CONNECTION_STRING` required at require-time of
  `lib/store.js`). **There is no Azurite on this machine** (`command -v azurite` empty, read 18:40) and no Postgres here: the
  builder ran every cell against an in-memory store "with the same createEntity/409 contract".
- The builder's own slip, on record in its READY: a `git checkout` during red-proofing wiped its uncommitted server changes;
  it re-applied the patch from a script before committing. Weigh it as a reason to verify that the committed `642b06b` is what
  the cells describe, not as a defect.

### TARGET D — item 4: portal mail HTML escaping (TIER 1)
- **Portal `d11eed6`, five files over `ef5a9c0`:** `server/email/escapeHtml.js` (A, "THE helper", the five-character map,
  `null`/`undefined` → ''), `server/email/index.js` (the text-only fallback becomes `<pre>${escapeHtml(text)}</pre>`;
  `escapeHtml` re-exported), `server/reminders/dispatcher.js` (a pure `reminderEmail(rem)`: `html:
  <p>${escapeHtml(rem.body || rem.title)}</p>…`, `text` unchanged, `subject: rem.title`), `server/email/escape.test.js` (A, 5
  tests), `BACKLOG.md` (d11eed6: 8 portal production-dependency advisories, offered as a later item — not a target).
- **On main `ef5a9c0` (READ):** `dispatcher.js:109` `html: \`<p>${rem.body || rem.title}</p>…\`` and `email/index.js:43`
  `` html || `<pre>${text || ''}</pre>` ``.
- **`sendEmail` callers at `d11eed6` (READ, `git grep -n "sendEmail("` + every `require('../email')`):** `reminders/dispatcher.js:120`,
  `routes/quotes.js:220` (approvals mail, interpolates `quote.scenario`, `p.type`, `p.detail` into HTML UNESCAPED — the builder
  says scenario is a DB CHECK enum and detail is engine-built), `routes/quotes.js:434` (`doc.html` from `quotes/document.js`,
  which has its own private `esc()`), `routes/settings.js:108` (static test send). **A2 adds a fifth caller that the text grep
  MISSES:** `feedbackNotify.js` calls it as `sender(...)` after `require('./email').sendEmail`.
- Claimed: `npm test` 67/67, `test:db` 5+4+17 incl. a concurrency test driving the real `dispatchDue()`; red-proof removing
  only the two `escapeHtml(...)` calls fails 2 of 5.

### All targets
- **No worktree is pinned. Build your own trees INSIDE YOUR OWN PROJECT (Testing Agent MAIN), from the object store:**
  `git -C <repo> archive <sha> | tar -x -C <a fresh mktemp -d under your project>`. **Never `git worktree add`, `checkout`,
  `switch`, `fetch`, `pull`, `stash`, `reset`, `restore`, `clean`, `gc` or commit against either repo, and never work inside
  either checkout.** Both checkouts are the live builder's working trees (the QuickQuote one moved from
  `feat/qq-open-old-quote-2026-09-22` to `fix/qq-qs-advisory-2026-09-22` DURING drafting): pin by sha, read origin by `ls-remote`.
- **Dependencies, without the network:** an archived tree has no `node_modules`. **The builder's installed trees MOVED during
  drafting:** at 18:41 both matched the gated lockfiles exactly (stage3 282/282, portal 247/247); by 18:50 the QuickQuote
  checkout was on `fix/qq-qs-advisory-2026-09-22` (qs 6.16.0 / express 4.22.3 / body-parser 1.20.8 installed) and the portal's
  `node_modules` carried the npm-audit set (11 entries differ: body-parser, brace-expansion, express, ip-address, lodash,
  minimatch, path-to-regexp, qs, …). **So the builder's `node_modules` is NOT the gated dependency set; do not use it unless you
  prove, at copy time, that it matches entry by entry.** The sanctioned route: in YOUR archived tree,
  **`npm ci --offline --ignore-scripts`** (in `stage3/` for QuickQuote, at the root for the portal). `--offline` forbids the
  network by construction: if a tarball is not in this machine's npm cache it FAILS rather than fetches — then that suite is
  **NOT RUN, blocker named**. Never `npm install`, never `npm ci` without `--offline`, never `npx` a package that is not already
  in the tree. After it, prove `node_modules/.package-lock.json` matches `git show <sha>:<lockfile>` entry by entry and quote
  the count. If you do copy a matching builder tree instead, COPY, never symlink (a test must not write into the builder's tree).
- **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** A fresh `mktemp -d` per arm; never reuse a mutant
  tree for a clean arm.
- **`git merge-tree --write-tree` writes objects** — always `GIT_OBJECT_DIRECTORY=<your mktemp -d>
  GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects`. The same two variables let you `git archive <tree-id>` a merge RESULT.
- **A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES:** `node --check` on every mutated `.js`/`.mjs` before its arm, exit code
  quoted. For `index.html` mutants, prove the page still loads (the pricing pack's engine extraction runs, and a render
  completes). A red from a mutant that does not parse or load is a VOID arm, never a red.
- **NOT on main. Nothing merges on your word or a builder's.** Merges are Tuesday's GO on a gated head.

## 2. Why these tiers, and who is waiting
- **A** routes every feedback item — free text a customer-facing rep typed, plus the rep's email address and the quote on
  screen (devices, term, currency, grand total) — to a THIRD-PARTY mailbox (`agentmail.to`) as well as Kam. That is what
  Kam asked for; the gate proves nothing ELSE rides along, and that the new send cannot break a submission.
- **B** is customer-visible wording and a version bump; the print is the tool's most fragile property.
- **C** is an access control over a new, year-long store of customer names, notes and deal sizes, reachable by anyone who
  can sign in (sign-in is OPEN: an OTP to whatever address is typed — Kam 2026-08-11). A wrong creator check is a
  cross-customer data leak; a stored margin input is a leak of what the HPAM gate exists to protect.
- **D** closes a live injection of user-typed markup into customer mail.
- 🔴 **The queue.** Four READY items; deploys are HELD for Kam (C-01/C-02 "not covered: publishing"). The builder has
  already said A1 and C, and A2 and D, collide (§7). Tuesday merges on a GO.

## 2a. LEGITIMATE SHAPES — three CHECKERS in this gate (template §2a)
Each refuses something: a BOOT (A1's recipient parse, C's retention parse) or a READ (C's creator check). A false boot refusal
is an outage of the hosted tool; a false 404 locks a rep out of their own quote. Measure every row.

| shape — its ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| A1: `FEEDBACK_NOTIFY_EMAIL` UNSET (the live app today, per the builder) | boots; To Kam, CC Tuesday | `|| DEFAULT_FEEDBACK_NOTIFY`, parse → 2 addresses | drafter |
| A1: set to ONE address (an operator overriding it) | boots; that To, **no CC** — Tuesday silently dropped | "replaces the whole list" (code comment) | drafter — **say whether that is acceptable, and whether anything warns** |
| A1: `"a@x, b@y ,"` (spaces, trailing comma) | boots; To a, CC [b] | trim + filter(Boolean) | drafter |
| A1: `""` (set but empty) | boots on the DEFAULT (empty string is falsy) — not a refusal | `||` | drafter — **measure** |
| A1: `" , "` | boot REFUSED `needs at least one address` | `!FEEDBACK_TO` | builder |
| A2: `FEEDBACK_NOTIFY_EMAILS` = `" , "` | **no boot check**: each POST still 201, the mail silently not sent (`{ok:false}` + console.warn) | `notifyRecipients` → `to` undefined | drafter — **measure; state the asymmetry with A1** |
| C: `QUOTE_RETENTION_DAYS` unset / `"365"` / `"30"` / `"0.5"` | boots | `Number(x) * day > 0` | drafter |
| C: `""` | boots on 365 (falsy → default) | `||` | drafter — measure |
| C: `"0"`, `"-1"`, `"abc"` | boot REFUSED | `!(ms > 0)` | builder (cell 9: "a bad value fails at boot") |
| C: the creator reopening with the SAME address typed in different CASE at sign-in | 200 (both sides lower-cased at `/auth/verify`) | `email.toLowerCase()` at verify; `creator = req.session.email` | drafter — **measure** |
| C: the creator in a NEW session (logged out, signed in again, next day) | 200 | the check is on email, not session id | drafter |
| C: the creator on a second device while the first session is live | 200 | as above | drafter |
| C: the number typed lower-case, with surrounding spaces, or pasted with a trailing newline | 200 | `.trim().toUpperCase()` | builder (lower case) / drafter (whitespace — **measure**, incl. `%0A` in the path) |
| C: the creator reopening a quote made in ADVANCED mode from a SIMPLE session | 200, PoC/Workpath withheld, `advancedWithheld: true` | out-filter | builder (cell 4) |
| C: a quote whose mail went but whose `status → sent` update failed (`stored:false`) | 404 to its own creator | `status !== "sent"` | builder (cell 10) — **say whether the rep is told it cannot be reopened** |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.** A legitimate shape refused is a
**Major** (for C: the creator cannot reach their own quote; for a boot row: the hosted tool does not start).

## 3. TARGET A — item 1: feedback CCs Tuesday (TIER 2, A1 QuickQuote + A2 portal)
**Answer each with a measurement (evidence class on each):**
1. **Scope, mechanically:** every changed non-test line in A1 is the recipient parse, the `cc` plumbing in `lib/mail.js`, and
   the two lines of the feedback send; in A2 the new module, the `cc` in `email/index.js`, and the four route lines. Nothing
   on the OTP, quote-email or auth paths changes (the quote mail's `bcc`/sales copy is untouched — confirm).
2. **The CC is real, proven against a FAKE provider only.** For A1, drive the real `lib/mail.js` ACS path with the
   `@azure/communication-email` module replaced by a recorder (a preload under YOUR project, registered before `lib/mail.js`
   loads; dummy `ACS_CONNECTION_STRING`/`MAIL_SENDER` values that are not real), and assert the captured
   `message.recipients` = `to [kreiser.org@me.com]`, `cc [tuesday-agent@agentmail.to]`, ONE `beginSend` per item, identical
   text for both. Drive the Agent Mail path too, with `globalThis.fetch` replaced by a recorder that NEVER reaches the network
   and refuses any host at all; assert `body.cc`. For A2, the same SDK recorder under the portal's ACS provider (dummy
   `ACS_EMAIL_CONNECTION_STRING`/`ACS_EMAIL_SENDER`), through the REAL route on LOCAL Postgres (§8), and read the
   `notification_log` row: status `sent`, subject `Vision feedback #N (type)` with **no title**, recipient masked.
3. **No secret, margin or buy-price reaches a mail — attack it.** Post feedback whose `context` (A1) / body (A2) carries
   planted probe values under every name that must never travel: `cpDay`, `cpMonth`, `cpYear`, `cpTerm`, `cpPct`, `psvHourly`,
   `advWord`, `margin`, `buyPrice`, `cost`, `sessionSecret`, `unlockSecret`, a fake cookie, and (A2) `admin_notes`,
   `created_by`, `status`, `priority`. Grep the captured subject, text, html, cc and headers for every probe VALUE. Also
   READ: A1 `safeContext` sends `ctxGrandTotal` — in an advanced, custom-priced (`cpPct`) quote the total reveals the applied
   discount against public list price. Pre-existing since item 10 (`ddf1134`); A only adds a recipient. Say so, grade it,
   do not re-tier A on it. For A2, READ whether any portal page puts a token or secret in its URL (the mail carries
   `page_url`), and whether `req.session.user` as passed carries anything beyond the five fields the mail prints.
4. **A failing mailbox never fails a submission.** For each app: the fake provider (i) rejects, (ii) throws synchronously
   in the constructor, (iii) NEVER resolves (a hung send), (iv) is not configured at all. Each POST must return 201 within its
   deadline, the row must be stored, and the process must not crash (Node turns an unhandled rejection into exit — READ the
   `app.get/post` wrapper in A1's server, and prove A2's un-awaited `notifyFeedback` cannot reject). For A1 also read
   `/healthz`'s `mail` block after two failures (`failing: true`).
5. **The `2a` rows for A1/A2**, measured. State plainly that the two apps use DIFFERENT variable names
   (`FEEDBACK_NOTIFY_EMAIL` vs `FEEDBACK_NOTIFY_EMAILS`) and differ in empty-list behaviour; grade it (an operator setting one
   name on the wrong app gets the default silently).
6. **Suites, in YOUR tree, by path and command:** QuickQuote root `node --test` (pricing, predicted 66); `stage3/` `npm test`
   (predicted 57); portal `npm test` (predicted 70) and `npm run test:db` against YOUR test database (§8; predicted 5+4+17).
   **Red-proof:** revert A1's `stage3/server.js` + `stage3/lib/mail.js` to `47eb533`'s, keep the tests → predicted 5 red;
   revert A2's `server/email/index.js` + `server/routes/feedback.js` to `ef5a9c0`'s → predicted 2 of 8 red. Read why each red
   is red. Add your own mutant per app: the CC dropped but the To kept (does a cell catch "Tuesday silently removed"?), and the
   send made AWAITED with a rejecting provider (does a cell catch a 500 on submission?).

## 4. TARGET B — item 2: the device label (TIER 2)
1. **The diff is exactly the two lines** (MEASURED from the object store, launcher guard 55 re-checks): the label and the
   version; `for="devices"` unchanged; nothing else in `index.html`.
2. **Real render** of YOUR archived `index.html` in headless Chrome (`/Applications/Google Chrome.app`, via
   `PUPPETEER_EXECUTABLE_PATH`), `file://`, light and dark, 1280 and 375 px: the label reads `DEVICES (MFPS/SFPS)` on screen
   (CSS uppercase), on ONE line, no clipping, the input still labelled (accessible name `Devices (MFPs/SFPs)`). Look at the
   screenshots. Then the **hosted** page: run `node stage3/strip.js` in your tree and render `stage3/public/index.html` the same
   way (the builder did NOT drive the hosted build in a browser).
3. **Print, as a real PDF** (the repo's rule): `stage3/` `npm run test:print` (predicted 18/18) and `npm run test:xlsx`
   (predicted 5/5), plus one Ctrl+P-equivalent PDF of the tallest quote, both themes: page 1 and page 2 each one A4. Confirm
   `2.31` in the badge and in every document footer.
4. `node --test` at the repo root (predicted 67). Mutant: the label reverted, version kept → the new test must redden.
5. READ: no other string names the device type (`git grep -n -i -E "MFPs?|multifunction|single.function" 72f6c0c`); list what
   remains, so Kam's two unbuilt proposals are decided on the full set. Do not build or test them.

## 5. TARGET C — item 3: reopen an old quote by number, creator only (TIER 1)
**The drivable surface is `createApp(...)` in YOUR OWN harness** (the stage3 entry point cannot boot here: `lib/store.js`
throws without `TABLES_CONNECTION_STRING`, and there is no Azurite or Azure you may use). Inject: an in-memory store you
write yourself to the SAME contract as `lib/store.js` (createEntity refuses an existing RowKey; getEntity of a missing key →
null) — do not import the one in `server.test.mjs` unread; the REAL `lib/pdf.js` renderer (Chrome) for at least the E2E and
the numbering legs; a fake mail that records. Bind 127.0.0.1, a port the kernel gives you. Sign in through the REAL
`/auth/request` + `/auth/verify` routes (read the OTP from your fake mail's record), never by writing a session row by hand
— except where a leg says so.
**Answer each with a measurement:**
1. **Creator → 200** with the stored form state (devices, customer, notes, apps, service tier), a lower-case number accepted.
2. **Another signed-in user → 404, body BYTE-IDENTICAL** to: a nonexistent well-formed number, a malformed number, an
   old-scheme `…-001` number, an expired number, a `pending` number. Compare status line, headers that vary (Content-Length,
   ETag, Content-Type) AND body. A difference in any header is a finding.
3. **No session → 401**; a forged cookie (`qqs=<sid>.<bad sig>`), a cookie for a logged-out session, and an expired session →
   401. Say what the 401 body is and whether it differs from 404 (it may: 401 before 404 is fine, and reveals nothing about a
   number — confirm by reading that the store is not queried before auth).
4. **No advanced field for a non-advanced session:** an advanced quote with PoC/Workpath reopened from a simple session →
   those ids absent, `advancedWithheld: true`; the same creator after `/api/advanced/unlock` → present. A SIMPLE session that
   POSTs advanced ids never stores them (read the row).
5. **Margin / buy-price NEVER stored — READ THE ROW, and derive the forbidden list from the page, not from the builder.**
   Enumerate every input/select/textarea id inside the five ADVANCED regions of `index.html` at `642b06b` (§1) plus
   `psvHourly`, `advWord`, `fbMsg`, `fxRate`; post a state carrying a unique probe value under EVERY id on the page (advanced
   and simple sessions); then assert on the stored `stateJson` AND on every other column of the row that no forbidden id and
   no forbidden probe VALUE appears. Note: the builder's cell names `margin` and `buyPrice` — **no element with those ids
   exists on the page** (READ), so those two assertions are vacuous; say whether any real buy-price field exists at all.
   **Establish whether `price-basic`, `price-advanced`, `price-custom` (stored) are sell prices or cost inputs** — read
   `HANDOVER/02-business-rules.md` and where the engine uses them. If any is a cost/margin input, that is a **Major**.
6. **Unique server-issued numbers under concurrency.** Frozen clock: 3, then 50, then 120 concurrent `POST /api/quote/email`
   in one second (fake renderer allowed for the 120 leg; name it). Expect distinct numbers, each opening for its own creator
   only; for 120, exactly 99 successes and 21 × 503 with an honest message — and NO row left behind for a 503. Two
   `createApp` instances sharing one store (two replicas): still distinct. `TZ=UTC` vs `TZ=Australia/Sydney`: the stem
   follows the process clock; say what that means for a number read by a rep in Sydney (the printed time is the container's).
7. **The Table Storage adapter itself (PROBED, not MEASURED):** drive the real `lib/store.js` `reserveQuote` / `getQuote` /
   `updateQuote` / `deleteQuote` with `@azure/data-tables` replaced by a stub that throws the SDK's own `RestError` shapes
   (409 on create, 404 on get/update) — read those shapes from the installed package. Carry the real service's 409 as
   **NOT TESTED** (no Azurite, no Azure): the first real proof is after deploy.
8. **Retention config:** default 365 (opens at 364 days, 404 at 366, row gone); `QUOTE_RETENTION_DAYS=30` (29 / 31); changing
   the value applies to rows already stored; the `2a` boot rows.
9. **Retention honesty (READ + MEASURED):** deletion happens ONLY when an expired row is READ. A quote nobody reopens is kept
   **indefinitely**, and `pending` rows (mail failed, render crashed) are never swept (the builder's own backlog entry). Kam was
   told *"kept for 12 months, then removed"*. Report whether that sentence is true of the code, as a finding with its evidence
   class; name the owner (Tuesday relays; Kam decides). Also: a row missing `createdAtMs` never expires (`NaN` comparison) —
   READ whether any code path can write one.
10. **Old and new numbers co-exist (customer-visible):** an old `…-NNN` number typed in → the standard 404 (not an error, not a
    different message); the page's `quoteNumber()` is untouched; the printed PDF and the xlsx carry the `H` number on one
    line in monospace (render it, `pdftotext` it, look at a page image, both themes); a customer holding an old number sees
    nothing change. Say whether any other consumer parses the number format (grep both repos and `HANDOVER/`).
11. **The E2E, in a real browser against your harness:** sign in, fill, email, reload, open by number (lower case), every
    field restored, totals equal; re-email → a NEW number, the old row unchanged (read it); a second user typing the first
    number → the "No quote … that you created was found" note, their form untouched. The page sets values with `.value` and
    messages with `.textContent` (READ `strip.js`); confirm a stored `custName`/`quoteNotes` carrying `<img src=x onerror=…>`
    renders inert after reopening, on screen AND in the re-emailed PDF.

**ADVERSARIAL PASS (C) — state the FAIL condition before each:**
- **Enumeration by number:** the number space is guessable (a timestamp + `H01` for almost every quote). There is no rate
  limit on `GET /api/quote/:qnum` (READ: confirm no limiter anywhere in `stage3/`). Drive 2,000 well-formed guesses from one
  session with a deadline; report the rate achieved and whether anything throttles, logs or alarms. A leak needs an oracle —
  the next bullet is the oracle hunt.
- **Timing between 404s:** 300 samples each of not-found, not-yours, malformed, pending, EXPIRED (the expired path awaits a
  delete first), interleaved, same connection reuse; report median and p95 per class. A separable class is a finding (grade
  it; the expired oracle reveals that a number EXISTED). State that your store is in-memory, so the real Table Storage gap
  (a 404 exception vs a found entity) is **NOT MEASURED** here.
- **Session fixation / session handling:** a pre-set `qqs` cookie before sign-in must not become authenticated; after verify
  the cookie is REPLACED; logout kills the session server-side (the old cookie → 401); the cookie flags (`HttpOnly; Secure;
  SameSite=Lax`). Unlocking advanced in one session does not unlock another session of the same email.
- **IDOR via any other parameter:** the GET honours nothing but the path (`?creator=`, `?email=`, `X-Forwarded-For`, a body on
  GET, `%2F`, double encoding, `..`, a 1 MB path, Unicode look-alikes of `H`, `DSQ-…-H1`, `…-H100`, `…-h01 ` with a tab); the
  POST cannot choose, reuse or overwrite a number (`state.qnum`, `fields.quoteNumber`, a body `qnum`, a replayed request →
  a new number, never an overwrite of someone else's row); nothing lets the POST write `creator`. A number reserved by user A
  then 503/500 on render — can user B's retry land on A's pending row?
12. **Suites, in YOUR tree:** `stage3/` `npm test` (predicted 64), `node stage3/strip.js` + `node --test stage3/test/strip.test.mjs`
    (predicted 12), `npm run test:print` (18), `npm run test:xlsx` (5), root `node --test` (66). **Red-proofs** (each mutant
    parse-checked, each predicted before running): the creator check removed (builder: 2 red — cells 2, 7); the allowlist
    replaced by pass-through (3 red — 4, 5, 6); the reserved number not passed to the render (5 red). Yours: the expiry check
    moved AFTER the creator check (any red? it changes the timing oracle); the 404 body for not-yours changed by one character
    (does the byte-identical cell catch it?); `QUOTE_ADVANCED_IDS` emptied; `toUpperCase()` removed.
13. **Version discipline (READ):** C adds a visible control to the hosted page and bumps neither `CONFIG.toolVersion` nor the
    stage3 package version (`0.3.2`). The repo's `CLAUDE.md` says a behaviour change without a bump is a bug; stage3-only
    commits in the history (`258e131`, `8116ef1`) did not bump either. Say which rule applies and grade it.

## 6. TARGET D — item 4: portal mail HTML escaping (TIER 1)
1. **No raw markup survives in the HTML part.** Through `reminderEmail(rem)` AND through `sendEmail`'s text-only fallback (real
   ACS provider, SDK recorder), for each payload class: `<script>`, `<img src=x onerror=…>`, `<svg onload=…>`, an event-handler
   attribute inside an allowed-looking tag, `<a href="javascript:…">`, `<a href="data:text/html;base64,…">`, `<style>`,
   `<!--`, `</pre>` / `</p>` breakout, CDATA, entity tricks (`&lt;script&gt;` typed literally, `&#x3C;`, `&#60`, `&amp;lt;`),
   quotes in attribute context, a NUL and C0 bytes, CRLF. **Assert by PARSING the HTML part** (an HTML parser available in the
   portal's `node_modules`, or a headless Chrome `document`), not by substring: the parsed body must contain no element
   other than the signature's own `<p>`s / the `<pre>`, and no attribute beginning `on`, no `href`/`src`. Render one in Chrome.
2. **The plain-text part is unchanged**, byte for byte, for every payload (`text: rem.body || rem.title`).
3. **No double-escaping of a caller's own html:** the quote-email path (`routes/quotes.js:434`, `doc.html`), the approvals
   path (`:220`) and the settings test send pass their html through untouched; a `&amp;` in a caller's html stays `&amp;`.
4. **Enumerate EVERY caller of `sendEmail`**, by `require` of the email module and by any alias, not by the call text (the
   text grep misses A2's `sender(...)`): for each, which fields are user-typed, whether they reach HTML, and whether they are
   escaped. The approvals mail (`quotes.js:220`) interpolates `quote.scenario`, `p.type`, `p.detail` raw — **establish from the
   schema and the pricing engine whether any of those can carry user-typed text** (a customer name, a free-text line). If one
   can, that is a sibling of the class D fixes and D did not reach it: a finding, grade by who receives that mail
   (`APPROVALS_INBOX`, internal).
5. **Who can put text in a reminder, and who receives it** (READ `routes/reminders.js`, `emailPolicy.recipientAllowed`): any
   role that can create a client reminder, with which recipients. That is the blast radius of main's live defect; say it.
6. **Subject and headers:** `subject: rem.title` goes into the ACS subject unescaped (correctly — it is not HTML). Probe CRLF
   and very long titles against the SDK recorder; say what the SDK does with them (READ its validation).
7. **Suites and red-proof, in YOUR tree:** `npm test` (predicted 67), `npm run test:db` on YOUR test DB (5+4+17), including the
   real `dispatchDue()` against local Postgres with the SDK recorder capturing a reminder mail end to end. **Red-proof: revert
   `a68b53a`'s three non-test files to `ef5a9c0`'s, keep `escape.test.js`** → predicted the reminder and fallback cells red
   (the builder reverted only the two calls: 2 of 5); read why. Your own: escape only `<` and `>` (does anything catch a quote
   or `&`?); escape applied twice (does the "not double-escaped" cell catch it?).
8. **Duplicate helpers (READ):** after A2 and D both land there are two `escapeHtml`s (A2's private one in `feedbackNotify.js`
   and D's "THE helper"), plus the private `esc()` in `quotes/document.js` and `tco/report.js`. The builder offers to fold A2's
   into D's "in whichever rebase merges second". Grade it (Polish); it is a merge-order note, not a blocker.

## 7. Across targets — merges and the queue (NOT measured by the drafter: measure them)
**The drafter could not run `git merge-tree --write-tree` (read-only commission). Every row below is UNMEASURED — quote
`git merge-tree --write-tree --name-only` from YOUR OWN object directory for each.** Hunk facts the drafter READ (`git diff -U0`):

| pair | files both sides change | READ prediction |
|---|---|---|
| A1 `bd3e3cf` × C `642b06b` | `stage3/server.js`, `stage3/test/server.test.mjs` | **CONFLICT in `server.js`**: both INSERT after `:54` (A1 +16, C +58) and edit the adjacent `createApp` signature lines `:56`/`:58`/`:59`. The builder's READY says "different regions" — the insertion point is the same. `server.test.mjs`: A1 at `:571-580`, C at `:19`, `:38`, `:85`, `:795` — likely clean. |
| A1 × B `72f6c0c` | none | clean |
| B × C | none (`index.html` + root test vs `stage3/` + docs) | clean |
| C × `44405c6` (backlog) | `BACKLOG.md` — both insert after `:80` | conflict (docs); the builder says 44405c6 "closes when this merges" |
| C × `320a169` (qs lockfile, not a target) | none | clean; say whether C's cells are unchanged on 320a169's dependency set (NOT COMMISSIONED to run — carry it) |
| A2 `ce01ba9` × D `d11eed6` | `server/email/index.js`, `BACKLOG.md` | **likely CONFLICT in `email/index.js`** (A2 edits `:37` and inserts after `:44`; D edits `:43` and inserts after `:2`); `BACKLOG.md` both append after `:136` → conflict. A2's backlog entry describes exactly the defect D fixes; whichever merges second must drop it. |

- **On every merge RESULT you can build** (archive it into your project; PROBED): for A1×C, if merge-tree conflicts, say so
  and do NOT hand-resolve (a resolution is the builder's); if it is clean, run `stage3/` `npm test` on the result. Same for
  A2×D with portal `npm test`.
- **A GO is a GO at the gated sha only.** Name the cells to re-run on each real merged tree (the builder will rebase whichever
  merges second). **CI:** `gh` is not authenticated for `datasecau` in this project, so no gate may claim a CI result; state that
  every target's CI half is **NOT RUN** and is measured at merge.

## 8. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock (replaces NexusAI's four clauses), plus THE DEADLINE RULE
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's** (`session-tools/nexusai-lock.sh` is
NexusAI's floor; a Vision gate holding it blocks NexusAI seats). Neither Vision's `CLAUDE.md` nor its `CLARIFICATIONS.md`
names a port or floor rule (READ 18:3x) — so this section is the rule, derived from what the code and the machine show:
1. **The Vision builder seat is LIVE** (claude pid `1613`, tmux pane `%41`) and owns the defaults: portal `:4848`
   (`server/index.js`, binds `0.0.0.0`), stage3 `:8080`, the E2E scripts' `BASE_URL http://localhost:4848`. **Never use 4848
   or 8080**, nor `47787` (Tuesday's dashboard), nor any port a NexusAI seat holds. Take every port from the kernel (listen on
   0, or check it free with `lsof -nP -iTCP:<p> -sTCP:LISTEN` immediately before) and bind `127.0.0.1` wherever YOUR harness
   calls `listen`. The portal entry point binds all interfaces by its own code — record it, do not change it.
2. **Postgres = the running local container on `127.0.0.1:5433`, and ONLY databases you create.** It is a docker container
   listening on all interfaces, shared with the builder. **No docker command at all** (no start, stop, exec, run, pull). Create
   `vsp_qa_g1_<epoch>` for app runs and `vsp_qa_g1_test_<epoch>` as `TEST_DATABASE_URL` for `test:db` (it TRUNCATEs — never
   point it at `salesportal` or `salesportal_test`, the builder's). The connection uses the repo's LOCAL compose defaults in
   `server/db.js` / `scripts/ensure-test-db.js`; never anything from `Vision_Sales_Portal/4_Credentials/` (`.env`,
   `accounts.md`). There is no `psql` here: use the `pg` client from the copied `node_modules`. If `:5433` does not answer, the
   portal runtime legs are **NOT RUN, blocker named** — do not start a container. Leave your databases in place and list their
   names in the report (no DROP; quarantine, not removal).
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH, HOME = a fresh mktemp dir, TZ, NODE_ENV =
   `test` or `development` — never `production` — PORT, a fresh random SESSION_SECRET and unlock word you generate, DATABASE_URL
   / TEST_DATABASE_URL = yours, PUPPETEER_EXECUTABLE_PATH, and the dummy provider values of §3). **NEVER set in a product
   process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX` (with both set, QuickQuote's `lib/mail.js` SENDS FOR REAL through Agent
   Mail), any real `ACS_*` / `MAIL_SENDER`, `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, `APPROVALS_INBOX` pointing at a real
   box, `NTFY_TOPIC`, `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Before trusting any run, print the product process's env KEY
   NAMES (never values) and assert none of the forbidden ones is present. **Egress:** record the outbound connections of every
   server you run (`lsof -nP -a -p <pid> -iTCP`) — anything but `127.0.0.1` is a finding against your harness or the product
   (READ first which schedulers start at portal boot: reminders, feedback digest, monday sync — and prove none dials out).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND an entry point of
   either app (the portal's server entry file, the stage3 server file, or your own harness file) ANYWHERE in the remaining argv,
   argv from the kernel; **"ours" = the ancestor chain CONTAINS your claude pid**. Chrome children of your renderer count as
   yours by the same rule and must be reaped. **Negative controls, same run, must classify FOREIGN:** the Vision builder's claude
   `1613` (pane `%41`) and Tuesday's claude `63076` (pane `%0`); NexusAI-G `57419` / NexusAI-H `29254` may be added. Re-read
   them at start; if one has exited, say so and use the others. Never by `EADDRINUSE`, a whole-command-line grep, or raw `comm`.
   Gate 5's NexusAI instrument shows the method:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorcount.py`
   (with `qa-floorlib.sh`) — build your own copy under your project with the Vision entry points; do not edit gate 5's.
   **A zero is reportable only beside a control that fired in the same window** (spawn one server your way, the count must
   RISE, reap it).
5. **THE DEADLINE RULE:** every real-server, browser and database step has a written DEADLINE (e.g. boot 60 s, request 30 s,
   render 60 s, DB connect 15 s, exit 20 s) and a client timeout on every request; a step past its deadline is ABORTED and
   reported (a hung product request IS a finding). **Every server, browser and child you start is killed in a `finally`**
   (SIGTERM, then SIGKILL after a grace), confirmed by your counter. **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at
   least every 2 minutes; a step with no heartbeat for 5 minutes is aborted and reported.** §3 Q4 (a hung send), §5 Q6 (120
   concurrent renders) and the enumeration leg are exactly the shapes that hang.

**Reap every server and every Chrome you start.** An orphan of yours is the builder's foreign process.

## 9. Drivable surface — LOCAL ONLY. **NEVER the live QuickQuote or the live portal.**
- **NEVER the live** QuickQuote (App Service `hpas-quickquote`, resource group `hpas-quickquote-rg`, its ACR `hpasqqacr`, its
  Table Storage) **or the live portal** (`https://datasec-sales-portal.azurewebsites.net`, resource group
  `datasec-sales-portal-rg` — PRODUCTION: the live site, its Postgres `datasec-sales-db.postgres.database.azure.com` and key
  vault). No request to either host, no DB connection to either, not even a GET or a health probe.
- The portal: its own entry point in YOUR tree, on LOCAL Postgres, `env -i` (§8). QuickQuote: `createApp` in YOUR harness
  (§5), and the offline `index.html` from `file://`.

## 10. HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker`, no `npm install`, no `npm ci` without `--offline --ignore-scripts`, no `npx` of anything not
  already in your tree.** The launcher points
  `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories so no identity is inherited.
- **Real sends are OFF.** Every provider is a recorder you wrote; nothing reaches ACS, Agent Mail or ntfy from a product process.
- **Findings-only:** do not commit, do not move any branch, do not file a ticket, do not write inside either repo or anywhere in
  `Vision_Sales_Portal/` (`1_Project_Definition/`, `4_Credentials/`, `5_Project_History/` included). The gate fixes nothing.
- **NEVER `rm`** — quarantine, per the template §5; every preload, stub, harness and fixture lives under YOUR project.

## 11. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-22-vision-qq-gate1/report.md`

**Questions:** your sender `QA/Datasec-Vision` has NO inbox routing line in the fleet — you cannot receive an answer
reliably. If you must ask, mail `tuesday-agent@agentmail.to`, subject `[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>`
(Context / one Question / Meanwhile / Needed-by), **and proceed on the safest reading without waiting**; record the question
and the reading you took in the report.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 1: item 1 @ bd3e3cf + ce01ba9 (tier 2) + item 2 @ 72f6c0c (tier 2) + item 3 @ 642b06b (tier 1) + item 4 @ d11eed6 (tier 1)`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the
QA project has none. Use it ONLY in your own verdict/question `curl`; it must never enter a product process's environment
(§8.3). Never put the key, or any secret, in a mail or the report.

Verdict format:
- **A: GO / NO-GO** (A1 QuickQuote `bd3e3cf`, A2 portal `ce01ba9`, each stated), **B: GO / NO-GO**, **C: GO / NO-GO**,
  **D: GO / NO-GO**, stated SEPARATELY PER TARGET, each naming its sha.
- Then one paragraph on the queue quoting §7's merge-tree results, A1 × C and A2 × D first: which GO survives which merge
  order, which cells must be re-run on the merged tree, and that every target's CI half is NOT RUN (gh unauthenticated).
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section — at least: real Table Storage 409, the timing
  gap on real Table Storage, real ACS/Agent Mail delivery, Node 20 (this machine runs node v26.8.1; both apps ship on Node 20),
  CI, the stage3 entry point's boot, the offline tool's `file://` print on a partner laptop). Every action recommendation carries
  its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY. §3 Q3, §5 Q5, §5 Q7, §5 Q9, the timing leg and §6 Q4 must each
  carry one.
- Report each target's head, and both mains, as three timestamped readings (start / mid / end), each with its branch name.

PROVENANCE:
- origin heads: QQ main 47eb533034108c5c92d6b36af44554528ffc71ec, fix/qq-feedback-cc-tuesday-2026-09-22 bd3e3cf730cf…, fix/qq-mfp-sfp-label-2026-09-22 72f6c0cc93d5…, feat/qq-open-old-quote-2026-09-22 642b06b48571…, fix/qq-qs-advisory-2026-09-22 320a16986030…, backlog/qq-qnum-collision-2026-09-22 44405c6a6933…; portal main ef5a9c0b942c…, fix/feedback-mail-cc-tuesday-2026-09-22 ce01ba95fa9e…, fix/mail-html-escape-2026-09-22 d11eed6af2bb… | `git -C <repo> ls-remote origin refs/heads/<b>` | read 2026-09-22 18:35:31, 18:41:26 (D), 18:43:08 AEST
- chains: bd3e3cf, 72f6c0c, 642b06b, 320a169, 44405c6 each one commit, parent 47eb533; ce01ba9 parent ef5a9c0; a68b53a parent ef5a9c0, d11eed6 parent a68b53a | `git log --format='%H %P' <base>..<head>`, `merge-base` | read 18:36-18:41
- file sets / numstat per target; a68b53a = 4 non-BACKLOG files, d11eed6 = BACKLOG.md only | `git diff --stat`, `--name-only`, `--numstat` | read 18:36-18:43
- lockfile blobs identical (stage3 64e49cb at 47eb533/A1/B/C; portal 9d426df at ef5a9c0/A2/D); installed node_modules matched (282/282, 247/247) at 18:41 and did NOT at 18:50 (QQ checkout on fix/qq-qs-advisory @ 320a169, 3 entries differ; portal 11 entries differ) | `git rev-parse <sha>:<lockfile>`; python compare of `node_modules/.package-lock.json`; `git rev-parse --abbrev-ref HEAD` | read 18:41-18:50
- A1/A2/C/D mechanisms, hunk ranges, ADVANCED sentinel lines, stored ids, sendEmail callers | `git diff`, `git diff -U0`, `git show <sha>:<file>`, `git grep` | read 18:36-18:42
- READY mail bodies (items 1-4) and Tuesday's item-3 ANSWER (08:24:09Z) | AgentMail GET list tuesday-agent@ (limit 100) + `inbox_digest.sh full` | read 18:33-18:42
- C-01..C-05 | `Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md` | read 18:34
- Vision + QuickQuote project rules (no port/floor rule named) | `Vision_Sales_Portal/CLAUDE.md`, `Quoting Tool/hpas-quoting-tool/CLAUDE.md` | read 18:34
- H-suffix and 12-month defaults stated to Kam | `0_Brain/dashboard/data/chat_tuesday.json` | read 18:40
- portal defaults: PORT 4848 (`server/index.js:22`, listen 0.0.0.0 `:178`), DB localhost:5433 (`server/db.js:4`), test DB default salesportal_test (`scripts/ensure-test-db.js:10`); stage3 PORT 8080, TABLES_CONNECTION_STRING required (`lib/store.js:10-11`), Agent Mail fallback when ACS absent (`lib/mail.js`) | `git show ce01ba9:…`, `git show 642b06b:…` | read 18:37-18:39
- :5433 LISTEN by com.docker (pid 14632), no Vision node server running | `lsof -nP -iTCP:5433 -sTCP:LISTEN`; `ps` | read 18:38
- seats: %41 → claude 1613 (Vision), %0 → claude 63076 (Tuesday), %36 → 57419, %38 → 29254 | `tmux list-panes -a`; `ps` | read 18:38
- tools: Google Chrome.app present; pdftotext present; no psql, pg_isready or azurite; node v26.8.1; stage3 Dockerfile `FROM node:20-bookworm-slim`, portal Dockerfile `FROM node:20-alpine` | `ls`, `which`, `command -v`, `git show` | read 18:39-18:40
- no earlier Vision/QuickQuote gate launcher or QA project dir | `ls launchers | grep -i -E 'vision|quickquote|qq'`; `ls Testing Agent MAIN/projects` | read 18:30
