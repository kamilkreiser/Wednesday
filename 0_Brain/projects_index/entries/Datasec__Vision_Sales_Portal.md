---
client: Datasec
project: Vision_Sales_Portal
path: /Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal
status: active
updated: 2026-08-08
---

# Datasec / Vision Sales Portal

**Last session (2026-08-07 → 08, wrapped 05:30):** **The standalone HPAS
QuickQuote fix list is COMPLETE — v2.12 `f67bef0`.** F1–F17 and F19–F23 all
shipped; F18 is Stage-3 gated by design. 45 tests green; regression pack re-run
through the real UI across 72 scenarios with ground truth intact at 374 → 5 days
→ $10,500 and every AUD total exactly 1.55× its USD twin. Print-verified as real
PDFs in light, dark and a GBP no-services quote.

**Open / next:**
- Merge `stage1/pricing-engine` — 8 commits ahead of `main`, unmerged by design
- Add CI: 45 tests that only run when a human types `node --test`. Cheapest item left
- WIL-54 (per-app chips show USD) — a product decision, not a patch
- Page-1 print overflow (pre-existing, reproduced on v2.06) — needs its own pass
- Then hosted Stage 3: OTP, Postgres, emailed PDF, server-side HPAM gate, F18

**Blockers:** the merge needs your word under v1.3. WIL-54 needs a product call.
No contact with Will (Kam's ruling).

**Notes for Wednesday:** Tool lives at `Quoting Tool/hpas-quoting-tool/` — its
**own** repo, NOT inside `2_Project_Files`. Vision prod (`datasec-sales-portal-rg`)
was untouched across the whole session; nothing in this sub-project should
approach it. F21's gate is a speed bump not protection, and that is stated in
`BACKLOG.md` rather than implied — real enforcement is Stage 3.
