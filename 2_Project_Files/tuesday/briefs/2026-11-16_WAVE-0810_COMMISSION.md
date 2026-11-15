# Wave 08:10, 2026-11-16: three lane-kit drafters from SWEEP-0640 (Tuesday s281)

Tracked so the commission survives rotation. A drafter whose output is absent at the next boot is RE-COMMISSIONED from its section below. Authority: Kam's standing order at every boot (2026-10-24, "check tickets that can be actioned and if there are any, always start the process of working through it") and his 06:2x words "keep going with the tickets". Source of the lanes: `tuesday/briefs/2026-11-16_SWEEP-0640_datasec-actionable-lanes.md` (read its project section and section 5 whole).

**Tuesday's answers to the sweep's section 6, binding:** Q1 HPSMPOC-480/481 stay out. Q2 no RD-930/931 lane today. Q3 MPS M-D later, with 195/316 as re-read-first. Q4 NexusAI: NX-S1 and NX-T first. Q5 MPSCALC-233/123 not launched.

## For every drafter
1. Read `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` whole first (`/Volumes/Laptop-DEV/` paths mean `/Volumes/Datasec_DEV/`).
2. Copy the SHAPE of your template kit and read its drafter report and its seat's STATUS (Deviations and Corrections first). Write ONLY your kit, its `.measured` sidecar (`stamp_check.py --init`; `stamp_check.py <kit>` must exit 0), your report (last line `DRAFTED B<n>: kit <lines> lines, sidecar rc <rc>, questions <n>`), and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s281/d<B-number>/`.
3. **Before writing a lane, grep the pickup (`0_Brain/tasks/NEXT-PICKUP-TUESDAY.md`) and the last two daily notes (`0_Brain/daily_tuesday/2026-11-15.md`, `2026-11-16.md`) for every key of the lane and read each DROPPED / HELD / needs-ruling line** (ledger 2026-11-15: a sweep is a representation; the pickup's later line is the source). A key a hold covers is dropped and named in your report.
4. Every sentence the kit freezes that says what code, a test or a finding DOES has its source line printed beside it in the sidecar (ledger 2026-11-15 w=2). Every literal a seat must match is measured by a real run or a saved log (stamp_check MEASURED LITERALS).
5. Fences: no push, no PR, no Jira WRITE (GET only), no mail, no board, no az, no cd, no deploy. Print no token. Never read `0_Brain/learnings/_ledger.md`. Never publish (no Artifact tool). Never run `decision_queue.sh list`.
6. Clocks in the kit come from `date`, never typed.

## B1603 SEAT-N136: NexusAI lane NX-S1, `backend/server.js` security slice (template: `2026-11-15_B1592_SEAT-N133_nexusai-nx-s1-server-security.md`)
Keys per SWEEP-0640 lane NX-S1 (RD-830, 711, 762, 770, 772, 773, plus the server.js lines of 765, 766, 769, 806). Opus builder (model-routing row C3), G1 gate after. One seat owns `backend/server.js`. The NexusAI jest lock is shared: the kit uses `nexusai-lock.sh` as B1592 did. Code main `d1152289` or later (re-read). The NexusAI counts file: whoever lands second regenerates it (B1592 F1).

## B1604 SEAT-C104: Composer lane PC-C, PCOMP-128 item 2 (template: the latest Composer measurement or DEPLOY.md kit, e.g. `2026-11-15_B1569_SEAT-C101_composer-lane-c-deploy-guide.md`)
Measure migration 0022's Route B on a throwaway database, as SWEEP-0640 section 2 says. Sonnet (row C2), G3. No deploy, no demo VM, no hosted database. Composer's Guided hold (COMP-2 (a)) stands: drop anything it covers.

## B1605 SEAT-H172: HPSM-POC lane H-2, HPSMPOC-482 + 470 point 4 (template: `2026-11-16_B1599_SEAT-H171_hpsmpoc-forwardedproof-race.md`, the test-defect form)
The SQL Server start-up timing test (HostedDemoSlowFirstLoginTests; sightings in the B1585 gate F2 and HPSMPOC-482's two comments) plus 470 point 4 as SWEEP-0640 states. Diagnose test defect vs product first, as B1599 did; no retry, skip or wait added. Sonnet builder, G2 gate on Opus. HPSM standing line: no HP-tool integration; nothing deploys; UAT untouched.
