# Drafter notes, Seat C 39th, KS-2052 workflow approve impersonation (2026-11-16 01:0x AEDT)

Output brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatC39_ks2052_approve_impersonation.md

Key measurements (details and provenance in the brief; scratch in _work/):
- develop e659170439406810d368bdebf19dd39c08abeace (re-read 01:06, unchanged). PR 2241 and 2240 still open.
- Fix is route-only (routes/workflows.ts). No file overlap with PR 2241; imports three unchanged helpers from transferAccess.ts. Only open PR on the service file is 2170 (hunk at ~620, escalation sweep), not touched by a route-only fix. Default: base on develop.
- The approve route is also the reject path (decision in body); no separate reject route. No other route takes an actor from the body.
- KS-2052 on the board: Backlog, priority 3 Medium, 0 comments, last updated 2026-11-06. The High raise by S 82nd is not on the board yet.
- Gateway does not proxy /api/workflows/steps; transfer.openapi.ts calls workflows.ts dev-only. Reachability is direct-to-service only.
- Ticket also asks to verify delegatedFrom: put under D2, default OUT (needs a service edit in 2170's file and a behaviour ruling).
- Scratch clone attempt (sparse partial) failed to fetch blobs (credential), so all source was read with gh api contents; _work/clone holds no source and can be ignored.
- Brief size 34.9 KB (limit 35 KB after trimming).

UNMEASURED
