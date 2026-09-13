BLUF. **Your default is ACCEPTED.** When chain m9-s44 is GREEN, roll both live stacks to that step-8 head (FX-PIN + Q1 + FX-ID on 246fb92). Feedback steps 9 and 10 go in the next batch.
- **Authority:** Kam, 18:51 AEST, in the terminal: *"If you don't need to wait until 2100, don't wait. Upgrade as soon as it's ready, and I'll continue doing the testing before tomorrow."* Consequence 2 is met (web 409 check 13/13, 0 SILENT).
- **Same guarded sequence as 87c0026.** Head mail with the one-line pin answer, then ~5 minutes, pc-lane-a, Azure, full post-check on A and B, the PUBLIC browser check and the 26 gate probes, the Caddy fingerprint, and rollback first on any failure.

## Conditions
1. **Pins.** If either pre-check at the step-8 head finds ANY content or capability pin change against live 87c0026, that is a STOP for Tuesday before the deploy. A and B must stay usable.
2. **A LIVE QA GATE IS RUNNING ON THE AZURE DEMO, launched 2026-09-13 11:27:01Z.**
   - It is the live-only delta of the acceptance + security gate, verifying b-tight and the walk-through D-B1 blocked.
   - It works ONLY inside its own tenants: `QA Harness (synthetic) <date time>` and `QA Harness B (synthetic) <date time>`.
   - Its tenants, engagements and audit rows are NOT an anomaly. Your post-check stays on Kam's A and B, and never touches the QA Harness tenants.
   - Its brief expects an upgrade mid-run: it records START/MID/END heads and pauses on repeated 5xx.
   - **Put the exact Azure down/up times and the new head in your REPORT**, so its results can be split by head.
3. **REPORT as before:** the use and avoid lists, plus what Kam will notice. The DO NOT USE stale engagements become read-only, which is W4B-m2's fix working. Label any tunnelled check as tunnelled.

## Unchanged
C11 HOLD. Steps 9 and 10 are prepared. The edge route-table row with its wrong-on-purpose control is accepted. F1 goes to Kam's Monday list.
