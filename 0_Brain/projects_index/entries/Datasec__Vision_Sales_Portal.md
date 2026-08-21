---
client: Datasec
project: Vision_Sales_Portal
path: /Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal
status: active
updated: 2026-08-21
---

# Datasec / Vision_Sales_Portal

**Last session (2026-08-21):** Nothing changed in this repo. The session ran
from Vision's launcher but all work landed in the coupled sibling ATTIO — see
`Datasec__ATTIO.md`. Vision was read extensively as the migration's source of
truth: the six-stage CHECK, the 16-value data-driven stage map, the ~90
stage_data fields and the 13 email templates. Repo clean, main, 0/0, prod
untouched.

**Open / next:**
- QuickQuote v2.20 deploy, on Kam's signed word — nothing else is Vision-side.
- Otherwise the next session is ATTIO work; see that card.

**Blockers:** QuickQuote main is AHEAD of live. `hpas-quickquote.azurewebsites.net`
runs v0.3.2-tool2.19 while main carries the corrected v2.20 PoC rule — a
customer-facing pricing fix that has never shipped. Unchanged since 2026-08-14.
Production deploy is a v1.3 signature class, so it needs Kam's own mail.

**Notes for Wednesday:** Two facts worth carrying into ATTIO planning. Prod's
`leads.current_stage` has NO CHECK constraint (it silently failed to re-add), so
the live vocabulary is open-ended — 16 candidates known, 13 observed, 3 unresolvable
until someone queries prod from inside Azure. And prod Postgres firewalls dev
machines, which gates the real migration as much as the security pack does.
