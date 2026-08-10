# Projects index — state of all coding projects

Wednesday's situational awareness across the whole system. One section per project.
Until the other projects' wrap-up hooks write here themselves (see README.md), this
file is refreshed by Wednesday reading each project's `5_Project_History/history.md`
(newest at top) and vault notes — read-only.

Last full sweep: **never** (first sweep = WED-7). Partial freshness via the
end-of-session feed: see `entries/` cards. **Refreshed 2026-08-10 07:1x** —
05:30 shift change: 3 panes tapped, 3 accounted for (Vision "idle since last
close", NexusAI "already wrapped, ritual NOT re-run", overnight handover
05:33). History files re-checked on DevMASTER: Blockchain newest 08-07
(session 11), Vision 08-08, CypherKey 08-04, Lead_Bot 08-06, NexusAI wrap
86416fe — all unchanged since their last recorded sessions; no card edits
needed. Nothing has run since Saturday night's wraps.

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
- **2026-08-06 session 10 (evening, NEWEST — read from their history.md +
  shift-change wrap, 2026-08-07 06:0x):** KS-480 consent **recorded accurately,
  NOT by silence** (Peter had answered explicitly 08-05 11:36). Sizing Peter's
  bulk re-key turned up **two verified live defects on the client platform**:
  1. **`rotate: true` mints a new key and NEVER revokes the old one** — today's
     "rotation" is *issue an additional credential*, not *replace one*, so
     re-keying a lost key does not contain it. Known at code level
     (`platform.ts:501` concedes it); what is absent is evidence the semantics
     were decided deliberately for the DR case §4/§5 rests on.
  2. **An admin cannot list an org's keys on demo at all** — `GET /api/keys`
     serves a boot-warm memory cache filled by unscoped queries under
     fail-closed RLS. Live proof: table holds **25 rows** while the boot log
     reads `apiKeys: 0`. Masked because validation is unaffected and the cache
     lazily re-warms only keys **in active use** — precisely not a lost one.
  - **Net: neither half of "lose a key, re-key" has a working admin path on
    demo today.** Honest size for a bulk re-key that actually recovers:
    **~1–1.5 weeks, dominated by two decisions, not code.**
  - 7-way ticket split PROPOSED, nothing created. **KS-532 is Done+archived so
    it rejects comments** — Peter's DR rehearsal has no home, and as he wrote it
    (3 steps) it would PASS today while leaving the compromised credential live;
    it needs a 4th step confirming the old key is dead.
  - **KS-570 (High, assigned to Kam) sitting in Backlog** — revoked-session JWTs
    accepted on `/api/status` + `/api/leaderboard/*`. Looks mis-triaged.
  - State: branch `docs/ks480-rotation-and-key-listing-findings` (`1597ab72d`)
    pushed, **no PR**, deploy hold respected. Nothing built, nothing deployed.
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

- **Status:** active · **session 12 (2026-08-10 morning) scored 1.0** — Kam's
  thirteen rulings unlocked the architecture; P1 tickets created
  (KS-596/597/598), **KS-587 + KS-586 SHIPPED to develop+demo** (#659
  `521c78d41`, #660 `f217bc1ee`; verified independently: develop==origin,
  clean), 08-04 test-red proven stale (fresh e2e 210/0; real defect = the
  Schemathesis leg renders no-results as FAIL → KS-492/Peter), KS-585
  deferred in-window (to 09-05). P4 resized 2–3wk → 3–4wk by Kam's ruling
  (d) — accepted, informational. Rule-7 notify done. Wrapped clean; pane
  closed.
- **Open / next:**
  0. **Kam (new, on the 11:45 flag):** KS-587 residue (83 honest-but-confirmed
     incident docs: re-anchor vs mark failed) · **Secuura Linear cap now a
     REAL hard block** (~259 active, USAGE_LIMIT_EXCEEDED; upgrade = money,
     or cull) · joint authorization-model ruling (KS-539/547/586, one
     decision). Stuart cover note + S-pack v1.0 still await his send.
  2. **Stuart:** KS-577 cutover shape (blocks KS-576) · S-side confirm on
     KS-564 before it leaves In Review.
  3. **KS-587** — 84 demo anchors flagged `simulated=false, confirmed` while
     carrying `mock_tx_` hashes. **KS-586/KS-570** — one test decides High vs
     Urgent (does any verify path consult `/api/status`?). **KS-585** before
     the js-yaml baseline acceptance expires **2026-09-05**.
  4. Housekeeping: delete demo org `ks564-demo-verify-20260807` once Stuart
     confirms · open branch no PR `docs/ks480-rotation-and-key-listing-findings`.
  - **⚠ Two systemic finds worth fleet broadcast:** the **baked-migrations
    deploy trap** (runner reports `failed=0` while never seeing the file) and
    **branch protection on `develop` is advisory for their identity** (ruleset
    warned, then accepted a direct push).
  - **KS-564 SHIPPED 08-07** (Kam's authored 03:19Z approval). Finding B
    retracted — key listing works; ruling 2a moot.
- **Prior (08-05 session 8):** KS-539 signed off (G-1 split, #648, develop
  c9be578c3) · KS-559 closed (#646 merged 955aa0f11; root cause = GitHub
  secondary rate limit, not the suites I had blamed; durable fix KS-567) ·
  undici PERMANENT · #633 next train.
- **Wednesday can help by:** getting ship rulings Kam-traceable (their v1.2
  hold today proved why that matters); prompt-fidelity fold into WED-20.

### Datasec / NexusAI
- **Status:** active · **Last session:** 2026-08-08/09 — **boot-only, ZERO
  execution.** Briefed RD-77→RD-73 (02:11Z), plan confirmed and ANSWERED
  (02:15Z), then sat idle ~17h at 9% context and never picked the answer up;
  wrapped honestly at the 05:30 tap ("execution handed to next session").
  Their own named cause: no 3-min inbox re-check loop after asking. The
  confirmed plan is intact — brief + QUESTION + ANSWER thread is the full
  spec; next session re-verifies the v1.3 DKIM grant and executes. Receipt:
  HISTORY.md pushed @ `86416fe`, repo clean, both tracked Azure secrets
  untouched/unexamined (triage never began).
- **Prior (2026-08-07):** RD-67+68 DEPLOYED, rev --0000076 Healthy,
  --0000075 retained as rollback; DKIM authorship verification originated
  here, now fleet standard. CLOSED clean; at the 08-08 shift change it
  correctly declined to re-run the ritual (re-verified: repo clean @
  `c5c385f` in sync, vault in sync, demo healthy on --0000076).
- **First item next session (their call, and I agree): RD-77 (High)** — the
  gitleaks gate only scans push deltas, so nothing committed before 2026-04-25
  has ever been examined, and it stays green while **two Azure client secrets
  sit in TRACKED files on main**. Triage existing findings before widening the
  scan, or it goes permanently red.
- **RD-55** — confirm whether the Entra ID app secret is live, rotate if so,
  then the history scrub. Irreversible-class → **Kam's signed mail**.
- **RD-73** — deploy.yml still deploys to the decommissioned 4.x VM on every
  push. Reversible dev/CI config → inside Wednesday's v1.3 scope.
- **Needs Kam:** RD-61 demo sign-off (expect the fictional 10-printer DEMO-
  fleet — deliberate; RD-69 tracks the RD-15 video knock-on) · RD-76 (Entra SSO
  blocks all visual demo verification) · RD-74 · purge-or-keep on the dangling
  141 MB ACR manifest.
- **Caveat their agent flagged:** the project CLAUDE.md carrying the v1.3
  section sits OUTSIDE the git repo (not version-controlled); the vault
  decision file is the deliberate redundancy.
- **⚠ RD-71 — their highest-value board item:** the Dockerfile COPYs a directory
  whose contents are gitignored with nothing tracked keeping it, so **a clean
  clone simply fails to build**. CI hides it behind a `|| mkdir -p` fallback and
  Kam's working tree has the folder — so it builds for Kam and for CI and for
  **nobody else**. A contractor, or a release build from a tag, hits a wall.
- **Fleet-wide gotcha from their permission test:** Azure's `runningState` read
  "Activating" and never flipped to "Running" despite health OK on 20 consecutive
  polls and 0 restarts — **automation gating on that field would hang.**
- **Honest gap they named:** the three operations predicted to FAIL under scoped
  Contributor (`az group create/delete`, `az provider register`) were NOT
  empirically tested — that half is confirmed by the permission model, not by
  experiment. A Marketplace pre-publish dry-run will need a temporary grant.
- **Prior (08-06 day):** RD-61 synthetic demo feed per Kam's 08-05 ruling.
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
- **2026-08-08/09 (NEWEST): MERGED + CI WIRED, runs UNOBSERVED.** Stage 1+2
  merged to `main` (`3afee8d`, `--no-ff`, proven from clean clones before and
  after) and CI added (`c628b6e`); QuickQuote `main == origin @ 8422617`.
  **DoD 3–4 deliberately UNCLAIMED — nobody on this machine can see the
  workflow runs** (no datasecau GitHub access; routes in BACKLOG.md).
  `ci-proof/forced-red @ 2704141` stays on the remote until someone watches
  its run go red. Close-out = one `gh auth login` by Kam in a Vision launcher
  shell, then: main green? forced-red red? delete branch, tick BACKLOG.
  **Run NOT yet scored** — score after the CI runs are observed. Their two
  QUESTION mails (plan confirmation, CI observation) went unanswered — the
  gap was Wednesday's; acknowledge in the next brief.
- **QUOTING TOOL (sub-project, own repo `datasecau/vision_hpas-quickquote`):
  Stage 1+2 COMPLETE at v2.12 `f67bef0` (08-08 overnight, scored 1.0).** Whole
  fix list F1–F23 shipped (F18 Stage-3 gated by design); 45 tests + 72-scenario
  UI regression green; ground truth 374→5 days→$10,500 intact; AUD exactly
  1.55× USD across all 36 pairs. **F15/F16 — the wrong-SKU ABT quote defects —
  are closed with ~10 days to the 18 Aug deadline.**
  - **Open:** merge `stage1/pricing-engine` (8 commits ahead of main —
    Wednesday's to authorise under v1.3) · CI (cheapest item, v1.3 scope) ·
    **WIL-54 product call** (per-app chips show USD rate-card figures in every
    currency) · pre-existing page-1 print overflow · then hosted Stage 3 (OTP,
    Postgres, emailed PDF, server-side HPAM gate, F18).
  - **For Kam, in the agent's own words: the HPAM gate does not protect the
    margin data** — one offline HTML file ships margin logic, buy prices and
    the check itself in page source. "Start simple" is what shipped; partners
    not seeing buy prices only becomes true at Stage 3.
  - `main` remains Will's untouched v2.06 (`7428f39`), byte-verified provenance.
- **Status:** active · **Portal last session:** 2026-08-04 — 3 dependabot
  branches merged (`3dd24fa`), supply-chain checked, 144 tests green locally,
  then Kam-approved zip deploy: **main == origin == prod at `ef5a9c0`**.
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

### Datasec / Lead_Bot — WED-75 CLOSED 2026-08-06, session wrapped at shift change
- **Honest state, their words, and it must not be misread: "credential fixed,
  wiring open" — NOT "handoff complete".** The LEAD_BOT_API_KEY handoff is done
  and the leaked key is gone from disk, but **`SALES_PORTAL_URL` is still
  localhost on Kam's HOLD**, so Lead_Bot → Vision is not live end-to-end.
- **Artefacts that did not exist before and now do:** `history.md`, `BACKLOG.md`,
  a root `.gitignore`, and their index card.
- **⚠ There is still NO git repository in this project** — not a clean tree,
  none exists at the root or in `2_Project_Files`. `history.md` is a single copy
  on one SSD. Needs Kam's `gh auth login` as `datasecau`.
- **WED-78 ordering they recommend (and I agree):** (b) Kam names this project's
  Datasec tenant so someone can look for a running instance, THEN (a) the prod
  wiring decision. (b) genuinely gates (a) — deciding to point the bot at prod
  without knowing what is already running is deciding blind.
- **Status:** WED-75 closed · no Linear team, no LINEAR_* keys in its .env.
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
