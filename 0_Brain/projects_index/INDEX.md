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
- **Status:** active · **Last session:** 2026-08-05 session 8 (21:00–22:3x,
  WED-65 rulings executed, scored 1.0) — **KS-539 SIGNED OFF** (G-1 split, PR
  #648 merged, develop c9be578c3; contradictions flagged not merged; KS-566
  alignment ticket; Stuart+Peter verdicts unblocked) · **KS-559 CLOSED** (#646
  merged 955aa0f11 on FULL green — real root cause = GitHub secondary rate
  limit on the ~29-image push burst after cache invalidation; my
  Schemathesis/Akto-reds hypothesis corrected: outcome=skipped boot
  casualties, no test ever ran; durable fix = KS-567 retry/backoff) · undici
  PERMANENT in baseline · #633 next-train note · vault conflict copy deleted
  under authorization w/ diff receipt. Local stack DOWN, demo untouched.
  (Wrap mail 22:15 + history validated 08-06 06:0x.)
- **Open / next (today's openers, Kam-ruled):** staged local bring-up +
  rebuild to c9be578c3 FIRST → **KS-563 (Urgent**, false "Certified by
  issuer" on merely-anchored docs) → **KS-564 (High**, users/stub recipient
  resolution 500s on demo-pk). Both carry a demo-deploy leg when fixed —
  ship ruling needed then. **Peter KS-480 consent: record only AFTER EOD
  TODAY 08-06.** Watch: KS-539 Stuart/Peter verdicts · 2 flaky tier-3 tests.
- **Wednesday can help by:** launching their session (Kam's go), ship ruling
  when KS-563/564 land; prompt-fidelity fold into WED-20 protocol.

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
- **Not running on this Mac:** no launch agent installed, no lead-bot job
  loaded, nothing listening on 4902.
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
