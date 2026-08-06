# Projects index — state of all coding projects

Wednesday's situational awareness across the whole system. One section per project.
Until the other projects' wrap-up hooks write here themselves (see README.md), this
file is refreshed by Wednesday reading each project's `5_Project_History/history.md`
(newest at top) and vault notes — read-only.

Last full sweep: **never** (first sweep = WED-7). Partial freshness via the
end-of-session feed: see `entries/` cards (currently Secuura__Blockchain 08-04,
Datasec__NexusAI 08-04, Datasec__CypherKey 08-02, Datasec__Vision_Sales_Portal
08-02 — summarised below). Wrap emails routed through 2026-08-04 boot.

---

## Template per project

### <Client> / <Project>
- **Path:** …
- **Status:** active | paused | done
- **Last session:** YYYY-MM-DD — one-line summary
- **Open / next:** carried-over items
- **Wednesday can help by:** …

---

## Fresh (from entry cards)

### Secuura / Blockchain (Platform K) — most active
- **2026-08-06 session 9 (SHIPPED):** KS-563 (Urgent) **live on demo** — #651
  merged to develop `be2d60ef2`, plus fix `4f1152ed7`. Demo verify matrix green:
  upload-only w/ real confirmed anchor → verified true · isCertified FALSE ·
  isAnchored TRUE · certification absent; genuinely certified → full
  certification object. Verifier-portal rendering fix shipped with it (Kam ruled
  it stays in). Demo anchoring confirmed still REAL (47h up, wallet present).
  **KS-564: all three legs built, NOT merged** (branch `9c24b5c1e`) — Option A
  unit-proven only; ships as one piece after live proof, then a ship ruling.
  **Peter KS-480 consent: NOT recorded — record only AFTER EOD 2026-08-06.**
- **Their finding, now a fleet rule:** the demo deploy caught a FALSE NEGATIVE
  in their own fix that local proof could never find (local anchoring is
  mock-mode by design since KS-535). See
  [[../learnings/2026-08-06_local-proof-is-not-target-evidence]].

- **Status:** active · scored 1.0 twice today (ship + protocol adherence).
- **Open / next:** KS-564 live proof then a ship ruling (all three legs as one
  piece) · **Peter KS-480 consent — after EOD 08-06 only** · Stuart's KS-539
  verdict · 2 flaky tier-3 tests.
- **Prior (08-05 session 8):** KS-539 signed off (G-1 split, #648, develop
  c9be578c3) · KS-559 closed (#646 merged 955aa0f11; root cause = GitHub
  secondary rate limit, not the suites I had blamed; durable fix KS-567) ·
  undici PERMANENT · #633 next train.
- **Wednesday can help by:** getting ship rulings Kam-traceable (their v1.2
  hold today proved why that matters); prompt-fidelity fold into WED-20.

### Datasec / NexusAI
- **Status:** active · **Last session:** 2026-08-06 (LIVE now, pane %3) —
  RD-61 synthetic demo feed per Kam's 08-05 ruling.
- **Board (live-corrected by their agent 2026-08-06 — my card was days stale):**
  RD-64 **already Done** (not awaiting confirm) · the Release-Ready pile is
  **gone**: RD-59/60/63/45/23 closed at the 08-04 sweep, RD-41 Put on Hold with
  an explicit do-NOT-deploy note · actual Release Ready today = **RD-58 + RD-56**
  (both Low, both new since my card).
- **RD-61 root cause (their verification):** upstream, not code — the ABTDEMO lab
  fleet was only ever 3 devices and they dropped off one at a time (May 6 → May 28
  → Jun 1); last event was a Service job, not a user print. Nothing to reconnect.
- **2026-08-06 (SHIPPED):** RD-61 synthetic feed **deployed to demo** and
  verified; RD-67 + RD-68 done; scoped-Contributor redeploy test PASSED (proved
  the downgrade first: `az group list` 7 → 3 RGs). ACR now pulls via managed
  identity with the admin account DISABLED — a push-capable stored credential
  removed. Identity: `nexusai-claude-deploy`, no subscription-scope rights.
  Open: RD-15 demo video no longer matches the new synthetic fleet (their
  ticket); WED-80 feedback recon requested.
- **In flight:** synthetic feed as a provider mirroring the AzureLogAnalytics
  surface; **code defaults to the REAL feed**, demo Container App sets the flag
  (their deviation, confirmed — a synthetic default would ship fake telemetry to
  Marketplace customers). Demo deploy is approval-class, awaiting a Kam ship
  ruling after local proof.
- **Blockers:** RD-18 Kam's legal decision.

### Datasec / CypherKey (OneTimePad)
- **Status:** active · **Last session:** 2026-08-02 — ADR-0013 HSM-keyed digests
  shipped (CPKEY-155), digest-pinned ACA deploys (CPKEY-160), CPKEY-95/101 closed.
- **Open / next:** Kam decisions (demo keyed digests, Android fail-open posture,
  Twilio rotation, store publishing) · build queue CPKEY-161/162/163/164.
- **Wednesday can help by:** same pattern — a Kam-decisions sitting.

### Datasec / Vision Sales Portal — GO-LIVE PREP INCOMING (WED-77)
- **Status:** active · **Last session:** 2026-08-04 — 3 dependabot branches
  merged (`3dd24fa`), supply-chain checked, 144 tests green locally, then
  Kam-approved zip deploy: **main == origin == prod at `ef5a9c0`**.
- **Kam signal 2026-08-06:** multiple Vision meetings this week and next →
  changes + live preparation coming shortly. Heads-up brief already on the bus
  (state-of-play, go-live blockers, anything needing Kam's hands).
- **Go-live risk list:** 5 remaining npm audit highs · dev DB won't boot (PG15
  volume vs postgres:16) · no auto-deploy wiring (manual zip via az, verified
  twice) · their GH_CONFIG_DIR unauthenticated and global `gh` floats, so CI
  reads may need Kam.
- **Lead_Bot link (corrected today):** direction is **Vision → Lead_Bot**.
  Vision generated the 64-hex key on 07-03; Lead_Bot held the old *leaked*
  40-char key. Lead_Bot is swapping it today; pointing the bot at the prod
  portal is **Kam-held at localhost** pending discovery of any running instance.

### Datasec / Lead_Bot — dormant since 2026-07-03, session live today (%4)
- **Status:** active today (WED-75) · no git repo, no history.md until today,
  which is exactly why its state was invisible to the fleet.
- **Findings:** handoff genuinely never done (key hashes differ; BOT_USER_ID
  matches) · the residual key is the gitleaks-found leaked value → this is leak
  remediation, not a sync · nothing running that we can see (no .env in
  2_Project_Files so compose would fail; no launchd agent; data last written
  2026-02-19) · **no az/gh auth at all** in that session (correctly reported,
  not requested) so the Azure-VM/systemd possibility is unverifiable.
- **Resources it depends on** (read from `2_Project_Files/README.md` +
  `config.js`, 2026-08-06): **Telegram Bot API** (the entry point — QR codes
  point at `t.me/<bot>?start=client`) · **Sales Portal API** `POST /api/bot/leads`
  · **PostgreSQL** (silent fallback when the API fails) · **SMTP** (notifications,
  currently non-functional — creds empty) · a host: Azure VM/systemd,
  Docker, or a macOS launch agent. Listens on port 4902.
- **Telegram bot state, live-checked 2026-08-06 ~10:4x:** `getMe` returns
  **ALIVE — @Datasec_Lead_Bot, id 8477664019**; `getWebhookInfo` shows polling
  mode, **0 pending updates, no errors**. So the bot account was NOT deleted,
  and nothing is queuing unanswered. Kam believed it had been deleted — the
  deleted resource is therefore something else (likely the Azure VM host);
  confirm which before concluding anything about a running instance.
- **NO INSTANCE IS RUNNING ANYWHERE — resolved 2026-08-06 without az.** The
  decisive test: Telegram allows exactly ONE `getUpdates` consumer per bot, so
  a second caller gets 409 Conflict. My call returned **no conflict** → nothing
  is polling → no live bot (it polls continuously; no webhook is set). Backed
  by: 0 pending updates · no host record anywhere in the fleet (the README's
  `azureuser@<vm-ip>` is a placeholder) · nothing local (no launch agent, no
  job, nothing on 4902; submissions.json last written 2026-02-19).
- **Never successfully submitted to prod, ever:** the vault's 2026-07-03 note
  records that before Vision wired it up that day, prod had NO
  `LEAD_BOT_API_KEY` at all — "Lead Bot can't submit to prod, pre-existing 401".
- **Net:** Lead_Bot is a fully-built, now correctly-keyed bot that has never
  been deployed. This is a deployment decision, not a live risk.
- **Open:** point-at-prod (Kam-held) + locate any running instance (needs the
  Datasec tenant confirmed — rule 4, still TBD for this project).

---

## Known projects (pending first sweep — WED-7)

### Secuura / Tokenomics
### Datasec / NexusAI Printer Dashboard
### Datasec / Vision Sales Portal
### Datasec / HP Auth Suite (security review)
### Datasec / Lead_Bot, Task_Dispatcher, myPKI, Feedback_System, Marketing_Collateral, Websites
### Side / Visualiser (coagent.live/VI)
### Side / Clara (local AI)
### Side / Testing Agent MAIN, Security Testing Agent, MultiAgent Coordination, Paperclip, Claude to Claude
