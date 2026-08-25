---
client: Datasec
project: ATTIO
path: /Volumes/DevMASTER/!CODING/Datasec/ATTIO
status: active
updated: 2026-08-25
---

# Datasec / ATTIO

**Last session (2026-08-23):** Wednesday's 9-item brief, all nine complete. The
daily follow-up job's two UX-test defects are fixed, deployed and proven live —
tasks now assign to the deal owner and dedupe on deal+signal — plus three more
defects found along the way (UTC date labels, a swallow I wrote into my own
fail-closed fix, and a coverage threshold that would have silenced the
blindness warning on the first BCC'd mail). ATTIO-7 closed on Kam's overrule,
read first-party from the chatlog rather than from a relay. 270 tests, up from
246.

**Open / next (refreshed 2026-08-25):**
- 🔴 Dated: Pro TRIAL expires ~2026-09-04 — Kam's keep/drop call, with ATTIO-15
  (Quotes object dispose/keep) decided WITH it; Import2 one-off import only
  possible while the trial window is open.
- UI-seat/Kam: token rename "Attio-atent" → "Attio-agent" (+ rotation while on
  that screen), NFR stage drag, report-2 filter to exclude Won/Cancelled/On hold.
- ATTIO-8 (M365 consent) — the standing biggest unlock; gates templates,
  sequences (a staged do-not-enable sequence is ready) and the not-contacted
  signal.
- Next brief carries: ATTIO-23 (housekeeping) + record-keep-synthetic + the
  ATTIO-19 close-out rec.

**Completed (moved off the dashboard 2026-08-25):**
- The combined in-Azure read — DONE 2026-08-24 (s1, scored 1.0): contact
  coverage bound [0,150] via client_id join; ATTIO-19 answered on-ticket (ONE
  quote ever, lead_id NULL, comment 36673). Kam ruled accept same morning.

**Blockers:** ATTIO-8 consent (Kam's one-action unlock). D6 still
synthetic-only; ATTIO-7's closure moved its gate, did not lift it.

**Notes for Wednesday:** Your UX test's "the [SYN] deals have zero addressable
contacts" was a sample of one — measured, 14 of 18 deals ARE linked to real
People; four are not and Ashgrove is one of them. The migration's People path
is built and working; the real risk is input coverage in Vision's own data.
Also: the empty-node_modules/tarball fingerprint is not reliably the Oryx
failure — it looked identical to the 08-21 crashloop on a perfectly healthy
app. Diagnose from /healthz and the deployment record.
