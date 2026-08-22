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
assessed and skipped with nothing faked. 246 tests pass.

**Open / next:**
- **UI seat (yours):** drag NFR from the end of the board to between Won and
  On hold; re-read the one hand-entered template against the new marker table.
  Neither is possible by API.
- Evidence-label split into two orthogonal columns (mapping-confidence vs
  observed-in-prod) — your recommendation, cheap now all 13 values are measured.
- ATTIO-7 closes only when Kam confirms the security-pack request actually went.

**Blockers:** D6 still absolute — no real customer PII into Attio until the
security pack lands. ATTIO-19 additionally has no source data at all.

**Notes for Wednesday:** Prod is 153 leads over 13 stage values (53 is the `nfr`
SUBSET, not the total — it appears three ways and reads like corroboration).
Attio's status API has NO order field, so any new stage is appended and must be
dragged. The NFR stage is currently last on the board — known, reported by
`apply-pipeline.js`, and outstanding at your seat.
