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
- **Status:** active · **Last session:** 2026-08-04 NIGHT (WED-54 Agent Teams
  pilot, wrap 23:34) — **11/11 KS-560 residuals = ONE root cause: KS-561, a
  REAL platform bug** (refresh op mis-declared bearer-authed since #483
  07-11 → silent-refresh 401s everywhere). Harness PR #645 merged (upload
  8/8 demo-green); platform fix #644 DRAFT proven-local, ship AWAITS KAM.
  KS-518/551 Done, #633 merged, KS-559 7/11 patched (PR #646 on CI),
  KS-562 filed. 4 Sonnet teammates, 0 escalations, deploy hold honored.
  (Day sessions: consent+deploy 14:34 wrap; wrap-only 21:21.)
- **Open / next:** merge #646 on CI green · execute #644 merge+demo-ship on
  Kam's ruling, then fresh tier-3 run = KS-560 final receipt · restart akto
  stack when needed · Peter consent window EOD 08-06 (recording after).
- **Kam decisions open (NEW from night run):** #644 KS-561 fix merge + demo
  ship · KS-559 undici acceptance (permanent vs expiring) · #633 main-landing
  (release vs cherry-pick) · KS-539 sign-off (carried) — for decision_queue.
- **Wednesday can help by:** consent-window recording brief; prompt-fidelity
  fold into WED-20 protocol.

### Datasec / NexusAI
- **Status:** active · **Last session:** 2026-08-04 — RD-64 fixed (Settings 403
  was a CSRF token-rotation race, not AI), deployed rev 69, verified end-to-end.
  Side find RD-65 (Low).
- **Open / next:** Kam to confirm RD-64 + close · RD-62 data-freshness surface ·
  RD-61 dead ABTDEMO feed (needs fleet owner, not code) · Release-Ready pile
  awaiting Kam: RD-59/60/63, RD-45, RD-41, RD-23.
- **Blockers:** RD-61 external owner; RD-18 Kam's legal decision.

### Datasec / CypherKey (OneTimePad)
- **Status:** active · **Last session:** 2026-08-02 — ADR-0013 HSM-keyed digests
  shipped (CPKEY-155), digest-pinned ACA deploys (CPKEY-160), CPKEY-95/101 closed.
- **Open / next:** Kam decisions (demo keyed digests, Android fail-open posture,
  Twilio rotation, store publishing) · build queue CPKEY-161/162/163/164.
- **Wednesday can help by:** same pattern — a Kam-decisions sitting.

### Datasec / Vision Sales Portal
- **Status:** active · **Last session:** 2026-08-02 — git housekeeping only;
  main fast-forwarded to 7336e46; prod untouched.
- **Open / next:** 3 dependabot branches to review/merge · confirm Lead_Bot
  LEAD_BOT_API_KEY handoff completed.

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
