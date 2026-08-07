---
client: Datasec
project: Vision_Sales_Portal
path: /Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal
status: active
updated: 2026-08-07
---

# Datasec / Vision Sales Portal

**Last session (2026-08-07):** Took over the **HPAS QuickQuote** sub-project from
Will Parker. Imported his full history to `datasecau/vision_hpas-quickquote`
(30 commits, byte-verified against the handover), then extracted a pure pricing
engine and **wired it in — v2.08 `49b3dfc`, the whole money fix-list F1–F10 is
closed in the live tool**, plus F7/F8. Measured, not asserted: professional
services in AUD went from A$5,045.25 to A$3,255.00. 35 tests green, print
verified as a real PDF in both themes.

**Open / next:**
- F15 (SKUs under individual apps) then F16 (Auth Manager mandatory) — these are
  what confused Joshua and caused a wrong-SKU quote on the live ABT deal
- F17, F11, F13, F12; then simplifications F18–F23
- CI — the 35 tests only run when a human types `node --test`. Cheapest win left.

**Blockers:** `stage1/pricing-engine` is 4 commits ahead of `main` and
**unmerged by design** — needs Wednesday's word under protocol v1.3. WIL-54
(per-app price chips showing USD) needs a product decision, not a patch.

**Notes for Wednesday:** The tool lives at `Quoting Tool/hpas-quoting-tool/` —
its **own** repo, NOT inside `2_Project_Files`. Vision's live site, DB and key
vault (`datasec-sales-portal-rg`) were untouched all session and nothing in this
sub-project should approach them. **No contact with Will** (Kam's ruling).
Known and deferred: page 1 overflows to 3 pages on mix-and-match + custom note +
comments — reproduced on v2.06, so pre-existing, not a regression.
