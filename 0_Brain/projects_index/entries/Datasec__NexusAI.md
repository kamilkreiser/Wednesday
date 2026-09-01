---
client: Datasec
project: NexusAI
path: /Volumes/DevMASTER/!CODING/Datasec/NexusAI
status: active
updated: 2026-09-02
---

# Datasec / NexusAI

**s12 (2026-09-01 17:3x→19:37, 0.85) + s13 LIVE (19:45→):** Kam's round-2 commission (17:25): Settings icon (bi-tree) · 27 NGA-2025-sourced deployment-default factors with references · Sustainability tab root-caused + fixed · SCIM F-1/F-4 tests-first (fb3b11e) · the fleet QA GATE's first live run (Kam 17:55): pass 1 = 18 findings on a 1.0-scored build → fix round (14/17 held) → pass 2 = PASS with findings, six dashboard Major rows + two SCIM Majors remain → **item 5 'fully functional' NOT MET** (PAPER COST $0 on the empty default view) → s13 = refine round 2 on branch `rd-136-nga-defaults-s12` (head cca9fb014). Nothing deployed since --0000091; SCIM OFF. RD-141/143/144/145/146 filed.

**Open / next (refreshed 2026-09-02 00:37 — 🎉 ca98a55 DEPLOYED to demo as --0000092; s14 WRAPPING on my word; s15 = round 6's second half):**
- **Deployed (verified from my seat 00:2x):** rev `--0000092`, image `1.23.0-rd136-s12-ca98a55`, digest sha256:c589bccc…; rollback `--0000091` sha256:055ea791… (re-read live before the swap); range 1d0b9c6..ca98a55 (rounds 2–5), 837/837; (a)/(e) preconditions SUBSTITUTED behind the SSO wall (platform-log line + the presence-discriminating `/css/dark-mode.css`, sha-identical, 404 control) — accepted; doc corrected. RD-136/137/138 **Release Ready**. For Kam: default view shows 'Unavailable' tiles by design (pick All Time); `POST /api/settings/costs` now 400s on invalid values.
- **Round 6 (s14 checkpoint 00:33):** R6-1 RD-157 DONE at `449af60` (the HTML's three typo classes fixed, not the CSS — 3 vs 11 uses, no sheet defined the typo; its flattering jsdom assertion deleted) · R6-4 RD-160 measured, NOTHING changed → **Kam card `nexusai-rd160-brand-chrome-contrast`** (rec #00719f on text-bearing chrome; default HOLD) · **R6-2 RD-158 + R6-3 RD-159 (High) → s15** from `docs/sustainability/S15_ROUND6_HANDOVER.md` at `3f180d6` (sweepPage ENUMERATES — 267/99/7 are over-counts, Bootstrap unpainted in jsdom; the real engine DECIDES — the tester's 87; settings clean) → QA SURFACE UP (pass 7, new port) → whole-page acceptance sweep → completion check → SCORE → any deploy = a fresh GO by digest. `:3015` stays up at ca98a55 as the live control until pass 7's surface stands. s14 SCORE at its wrap (rec 0.85–0.90: two rounds delivered in the engine; three own regressions across rounds 4–5, all gate-caught; exemplary disclosure; QA report ids pass 5 + pass 6).
- **Residual tickets (To Do):** RD-157 In Progress · RD-158 Med · RD-159 High · RD-160/161/162 Low · **RD-155 High PRE-EXISTING** (numeric-only settings.json abandons DATA_DIR — Kam's priority call) · RD-148 + auth-enforced P2-07 re-verify before any SCIM flip (card `nexusai-scim-deploy-live-ab` default A) · `nexusai-energy-kpis-tec` default dark.

**Open / next (refreshed 2026-09-01 23:26 — s14 round 5 briefed; NO deploy from 1f41edc):**
- **s14 (live, holding→round 5):** pass 5 = PASS WITH FINDINGS; my completion check FAILS leg 3 (first-run-setup dark 41/67 lines fail AA) → round 5: R5-1 cost `pattern` does not compile in Chrome (escape the dash; test compiles with the `v` flag) · R5-2 six `.text-*-emphasis` rules need `!important` · R5-3 dark counterparts for first-run-setup's own surfaces (light untouched) · R5-4 real `JsonStorage` in the cache test · R5-5 → RD ticket (a cost cannot be un-set through the product) → QA SURFACE UP (pass 6, new port) → my completion check → SCORE s14 → deploy GO by digest. :3013 retired on this ruling; :3014 until pass 6's surface.
- **Round 4 delivered at `1f41edc` (on origin):** P4-01 blocker dead in a real engine; 8/11 P4 ids fixed; 815/815; RD-152 (three Bootstrap versions) · RD-153 fixed · RD-154 open · **RD-155 High — numeric-only settings.json abandons DATA_DIR → `$HOME/data`; PRE-EXISTING (8eb94ce, 2026-04-18) → not deploy-gating; Kam's morning board: priority call.**
- **Demo:** still rev `--0000091` (s11's build); nothing deployed since. SCIM OFF (card `nexusai-scim-deploy-live-ab` default A; RD-148 + auth-enforced P2-07 re-verify first). Card `nexusai-energy-kpis-tec` default dark.
- **QA gate this project:** passes 1–5 all scored 1.0; the pattern across passes 3–5 — the stand-in agrees with the code and disagrees with the browser — is now the standing acceptance (one real-engine sweep per UI round).

**Open / next (refreshed 2026-09-01 19:4x):**
- [ ] s13: P2-01..08 fixes (tests at the CLASS, RED first) → QA SURFACE UP (pass 3, delta) → Wednesday's completion check → deploy to demo on GO (rollback by DIGEST sha256:055ea791…; Kam: default view shows 'Unavailable' by design — select All Time) → paper KPIs (Q1) as a new round.
- [ ] SCIM: P2-06 (revoke UI) + P2-07 (role check) BEFORE any flip; Kam's A/B open (default A after).
- [ ] Kam cards: `nexusai-energy-kpis-tec` (default dark) · SCIM A/B (prose, default A).

**Completed (moved off the dashboard 2026-09-01, verified at source):** s11 deploy --0000091 · RD-135 both Entra routes · Sustainability MVP · s12's four delivered items.

**Last sessions (2026-08-24, s1+s2+s3 — all 1.0):** Kam's feedback commission
live on demo in <40 min (RD-116, attachments with full untrusted-upload
standards). Data-provenance report answered his tenant question (dashboard data
= synthetic by design; the address he saw = LAW workspace in tenant bf504a5d,
outside our incomplete recorded set — naming it is his). His link double-check
answered with a fresh LAW-credential probe: workspace ACTIVE and ingesting;
printers stale since 1 June. Isolation audit falsified RD-118's own severity
(AI tools returned real ROW DATA; guarded 1 of 11 sites) → RD-118/120/119
shipped to demo (rev 88, SESSION_SECRET on secretRef); 3h post-fix window:
ZERO real-workspace SP tokens vs 374/30d baseline. RD-107 closed on Kam's
sample-data-stays ruling. HEAD 695aa98 == origin/main (verified).

**s4 (2026-08-25, 1.0):** RD-121 fixed at root cause — discovery now reads the
workspace METADATA endpoint (what exists in schema: 682 tables, relevance
filter → exactly the 3 HpamPrinterLogs_* tables, pinned by a test), full-
retention scan as a warn-logged fallback, `slice(0,50)` gone with a canary;
metadata path asserted inside the RD-118 guard with a non-vacuous control.
Deployed rev 0000089 under the reworded Single-mode condition (rollback tag
named + digest-chained before). ACR: Basic SKU, nothing prunes; **RD-124
found** (soft-delete DISABLED while its policy reads 7 days). RD-122 Done on
Wednesday's ruling; RD-123 filed for the residual. origin/main 458cdfb.

**s9 (2026-08-27 06:10–06:44, 1.0):** Session-Start check repointed to the Container App `/api/health` (CLAUDE.md; the launcher never curled the VM — Wednesday's premise, corrected); **RD-128 / RD-125 / RD-129 → Testing, deployed as `nexusai:1.21.0-rd128-rd125-9cdd5ca` → revision `--rd128125`** (rollback 1.20.0-rd121-e151431 digest-verified first; --0000089 deprovisioned = Single mode observed). Retention sweep now logs `feedback before:2 removed:0` on demo (was a false 0 for the feature's life). Third unfiltered export copy fixed in the same PR; `scripts/jira-query.sh` refuses with SEARCH BLIND on a dead token. 🔴 **RD-130 filed: the hourly health sweeper still probes the dead VM (DEFAULT_URLS[0], HEALTH_SWEEP_URLS unset) → ~2,300 false P1s feeding the SLA + morning-digest reports since 05-22.** RD-131 (Fleet Health CSV omits Drum Status). RD-93: transition to Testing is named "In Review" (id 31) — table in JIRA.md. main b376055. Board 62.

**s10 (2026-08-27 12:45–13:08, 1.0):** RD-130 both halves live — `HEALTH_SWEEP_URLS` set on demo (rev --0000090, same image, one URL by ruling, rollback = unset) and the 03:00Z run observed clean (p1 0 vs three P1s the hours before); `DEFAULT_URLS` loses the dead VM (red-first tests + a control against emptying the list), main 63ba114 / HISTORY fdce1ed, 279/279. 🔴 **Ticket corrected: 683 false-P1 audit entries EXIST (30-day retention pruned the rest), not ~2,300 — rec LEAVE, self-expiring; no Kam decision needed.** RD-131 proposal (shape 1; omission in two functions + a false-negative alert). **Filed: RD-132** (docs still name the dead VM as the live demo) · **RD-133** (readRecent line-cap used as a time window; SLA report fails optimistically) · **RD-134** (no scheduler tests; jest/ESM uuid trap, stub proven). Board 65.

**Open / next (refreshed 2026-08-27 13:1x):**
- [ ] RD-132 / RD-133 / RD-134 — next commission when Kam wants one (none launched by default; RD-133 is the one that mis-reports customer downtime).
- [ ] RD-131 — design call on the ticket (proposal posted), when commissioned.
- [ ] RD-128/125/129/130 in Testing — the browser click path still behind RD-76.
- [ ] RD-76/RD-116 browser eyeball on demo (Kam or my browser seat).
- [ ] 18+ tickets in Testing awaiting review / promotion — only if commissioned.
- [ ] PT-002 / PT-011 secret liveness — needs Datasec dev-tenant admin.

**Completed (moved off the dashboard 2026-08-27, verified at source):** RD-130 both halves (s10) · stale VM Session-Start check repointed (s9) · RD-125 · RD-128 · RD-129 (all Testing, deployed).

**s8 (2026-08-26 17:1x, micro, 1.0):** Kam's ruling (sweep + report only) LIVE: `scripts/feedback-sweep.sh` read-only, wired into CLAUDE.md Session Start + launcher FIRST ACTIONS step 6 (both machine-local — outside the repo; HISTORY says so). First live output: 2 items / 0 unreferenced, controls both ways. **RD-129 filed (Medium): a dead Jira token reads as an EMPTY BOARD, not an error** — `jira issue list` exits 0 with "No result", REST returns 200 `[]`; a negative control alone cannot detect a blind search. Boot is guarded by the /myself probe; mid-session token death + JIRA.md recipes are not. RD-125 comment 36707 (does NOT fix RD-125). main fc3bf0d. Board 60. Next session first: REPOINT the stale `curl https://4.198.168.215` Session-Start check (VM wound down 05-22) at the Container Apps health endpoint (ruled).

**s7 (2026-08-26, micro):** Kam's "ticket both feedback items" → agent HELD: both were delivered by
Kam on 2026-05-08 (91dab1bc, deployed) → recorded as **RD-126 (Bug) / RD-127 (Story), both Done**
for the trail; **RD-128 (Bug, Medium, To Do)** new: Export CSV → Job History ignores Copy/Fax
filters (one of two sites updated in May); other nine export functions not audited. HISTORY
823ff43. Board 59. Feedback→Jira has no mechanism either way → card for Kam.

**s6 (2026-08-26, micro, read-only — Kam's feedback-portal question):** store holds 2 human
items (both 2026-05-07, open, no attachments), none since; corroborates Kam's own look.
**RD-125 filed (Medium):** the retention sweep is a permanent no-op for feedback — the route
file exports no getter, both sweep sites bind `() => []`, the RETENTION_SWEEP audit line
records a false `before:0`; 365-day TTL first due ~May 2027. Portal unaffected. HISTORY
0af9b96. Missing feedback #1: Kam — "skip".

**s5 (2026-08-25 09:2x, 1.0):** Kam ruled RD-124 → ACR soft-delete ENABLED on
nexusaidevacrfa39 (7-day recovery proved with an isolated probe; NOT retroactive —
deletes before 2026-08-24T23:25:12Z stay gone; preview feature) and RD-123 → Single
stays (recorded, no infra change). Both Done. Board 57. origin/main e590b35.

**Open / next (as of 2026-08-26 — superseded above):**
- [ ] Repoint the stale Session-Start reachability check (dead VM → Container Apps health) — ruled 08-26.
- [ ] RD-129 dead-token-reads-empty (Medium) — fix when commissioned (mid-session + JIRA.md recipes).
- [ ] RD-128 CSV export ignores Copy/Fax filters (Medium) — one-line fix + audit the other nine export functions, when commissioned.
- [ ] RD-125 retention-sweep no-op (Medium) — fix when commissioned.
- [ ] Feedback→Jira mechanism — Kam's card (nexusai-feedback-loop-mechanism).
- [ ] RD-121 in Testing — promote once a customer-shaped workspace exercises
      the metadata path (demo blocks it by design under SYNTHETIC_DEMO_FEED).
- [ ] RD-76/RD-116 browser eyeball on demo (Kam or my browser seat) — the one
      remaining independent leg on the feedback widget + AI-path fixes.
- [ ] 18+ tickets in Testing awaiting review / promotion — only if
      commissioned.
- [ ] PT-002 / PT-011 secret liveness still unverified — needs Datasec
      dev-tenant admin (same blocker as RD-54/55).

**Completed (moved off the dashboard 2026-08-25, verified by my Jira read):** RD-123 Done ·
RD-124 Done · ACR tag-pruning check done (s4: nothing prunes at Basic SKU).

**Completed (moved off the dashboard 2026-08-24, verified at source):**
RD-107 Done (Kam's ruling, comment 36681) · key-sprawl card ruled RECORD ONLY
by Kam 10:54 (RD-111 annotated — "not a licence for a later session to tidy") ·
restore-path card ruled status-quo (synthetic is the standing state BY RULING).

**Blockers:** none agent-side.

**Notes for Wednesday:** Deploy condition for this app (Single revision mode):
rollback = redeploy by image tag, named BEFORE deploy, tag verified in ACR —
"previous revision retained" is unsatisfiable here (RD-122). The
`storage/` key-sprawl set is recorded, never touched, per Kam's record-only
ruling. Jira gotcha: their JIRA_SITE env var is scheme-less — prefix https://
or CloudFront 301s. tools.js executor logging (AC-3) closes history forward
only — nothing can establish whether the AI tools ever reached the real
workspace before 2026-08-24.
