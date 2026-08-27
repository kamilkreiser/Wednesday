---
client: Datasec
project: NexusAI
path: /Volumes/DevMASTER/!CODING/Datasec/NexusAI
status: active
updated: 2026-08-27
---

# Datasec / NexusAI

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
