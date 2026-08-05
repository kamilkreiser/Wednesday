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
