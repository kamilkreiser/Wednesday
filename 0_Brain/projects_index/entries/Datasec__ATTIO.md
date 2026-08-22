---
client: Datasec
project: ATTIO
path: /Volumes/DevMASTER/!CODING/Datasec/ATTIO
status: active
updated: 2026-08-22
---

# Datasec / ATTIO

**Last session (2026-08-22):** Six of Kam's rulings recorded (each verified
first-party at the chatlog, not from the relay). ATTIO-21 done — bridge now reads
Vision prod on a least-privilege role, delivery proven byte-exact by sha256.
attr-cap and nfr-onhold rulings implemented, tested and applied live. ATTIO-19
assessed and skipped with nothing faked. 246 tests pass. **Evening: Wednesday
completed Kam's hands-on UX test** (salesperson + manager passes, full
13-template audit — all clean, [[FILL]] markers only); report at
`WEDNESDAY/1_Project_Definition/Research/2026-08-22_attio-ux-test-report.md`.
Security-pack request OVERRULED by Kam 19:51 (public posture sufficient) —
ATTIO-7 closes on that ruling next session; D6's gate is now Kam's informed
acceptance + mechanics.

**Open / next (next ATTIO brief leads):**
- **Bridge fixes from the UX test (ungated, our code):** assign daily-job
  follow-up tasks to the deal owner (unassigned → Home shows "Tasks 0") +
  idempotency on task writes (Ashgrove follow-up duplicated by manual run +
  first scheduled fire).
- Rename/filter the "Total deals in pipeline" report (counts Won/Cancelled/
  On-hold: 18 vs 12 active — headline overstates) · rename the misspelled
  "Attio-atent" workspace member.
- Record the security-pack ruling + close ATTIO-7 · datasec@attio.email
  BCC-ingestion assessment (no M365 consent needed) · evidence-label
  two-column split · ATTIO-19 source-data owner question.
- **Migration plan requirement (CORRECTED 2026-08-23 — the UX-test "zero
  addressable contacts" was a sample of one; 14 of 18 deals ARE linked, the
  People path is built and running):** MEASURE contact coverage across the
  153 real leads before migrating and report it as a first-class number —
  leads with no parseable contact arrive as unemailable deals. One Azure-side
  read answers this AND ATTIO-19's quote-usage question together.
- **UI seat (mine):** NFR drag = Kam's 10 seconds (not automatable) ·
  Companies-by-Country awaits Kam's fresh word (HOLD; report has live data).
- At ATTIO-8 (M365 consent — now the biggest single unlock: email, templates,
  sequences, not-contacted signal): decide template signature strategy (typed
  signatures risk double-signing).

**Blockers:** D6 real-data gate now = Kam's informed acceptance + migration
mechanics (security-pack questionnaire dropped by his ruling). ATTIO-19
additionally has no source data at all.

**Notes for Wednesday:** Prod is 153 leads over 13 stage values (53 is the `nfr`
SUBSET, not the total — it appears three ways and reads like corroboration).
Attio's status API has NO order field, so any new stage is appended and must be
dragged. Trial lapses ~09-04 ("13 days left" banner live).
