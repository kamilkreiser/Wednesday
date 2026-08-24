---
client: Datasec
project: NexusAI
path: /Volumes/DevMASTER/!CODING/Datasec/NexusAI
status: active
updated: 2026-08-25
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

**s5 (2026-08-25 09:2x, 1.0):** Kam ruled RD-124 → ACR soft-delete ENABLED on
nexusaidevacrfa39 (7-day recovery proved with an isolated probe; NOT retroactive —
deletes before 2026-08-24T23:25:12Z stay gone; preview feature) and RD-123 → Single
stays (recorded, no infra change). Both Done. Board 57. origin/main e590b35.

**Open / next:**
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
