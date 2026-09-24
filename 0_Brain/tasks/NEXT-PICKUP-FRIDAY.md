---
date: 2026-09-24
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, end-of-day wrap 2026-09-24 ~16:5x (ctx ~60%)
supersede: replace wholesale at every wrap; do not append (the previous version is NEXT-PICKUP-FRIDAY.md.pre-0924-1650-wrap)
---

# NEXT PICKUP — FRIDAY

**The tree lives at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`.** Quote every path (spaces).

## 🔴 FIRST, EVERY BOOT AND EVERY CHECKPOINT
- `python3 2_Project_Files/tools/reconcile_rulings.py` (then `--apply` for Friday cards). **Twice on 2026-09-24 Kam's taps went unrecorded** and a panel message told him Friday was "waiting" on cards he had answered (ledger w=2). `chat_reply.sh` now warns on stderr when taps are pending: **read that warning, never skip it.**

## STATE AT THE WRAP (nothing running)
- **No build seat open.** Cards open on the Friday tab: **1**, `hpsmpoc-playbook-module2-readiness` (unanswered at 16:5x; default = kept separate). Everything Kam ruled today is recorded and delivered.
- **HPSM-POC** (`/Users/kamilkreiser/1FILES TO SYNC/HPSM-POC`, claimed): main **420d796** (push CI green) = B06 + B07-C + B07-B + readiness-against-the-real-API. CLARIFICATIONS up to **C-16**. Card `hpsmpoc-playbook-module2-readiness` (posted 16:2x) is OPEN; on `a`, brief a web seat to make module 2 the readiness flow (the snapshot stays reachable elsewhere).
  - Queued (BACKLOG "Follow-ups from B06/B07"): API partner "self" subject (duplicate records from parallel starts; Seat A's area); EF fail-level log on the handled sign-in race; customer-snapshot scoring off until an SME-approved ruleset exists (no approval path in the app).
  - Waiting on Kam's hands: **9 Azure providers** (command on the panel).
  - Owed by Friday (older): the Spark checker loosened for tests/UI/docs (Kam `spark-byte-exact: b`), when the Spark is back on.
- **Datasec Security Composer** (claimed): HPSM-light main **c018e07**, **deployed to the demo 16:4x** (live CSS index-CAI9pV2L; rollback = `/opt/hpsm/composer.prev`). Runbook: `2_Project_Files/friday/composer_demo_deploy.md`. CLARIFICATIONS up to **C-04**.
  - **NEXT BUILD (ruled by Kam, C-04):** fold the S5 discovery screen's two content notices into ONE tappable line at ≤600 px (same wording). Small: one web seat, brief from B04's K2 + STATUS; no deploy without Kam's word (card it with before/after at 390 px).
  - Guide v1.2 is FINAL for Paul (Kam: the 13 practice points stand). Kam sends it; nothing to Paul from Friday.
  - BACKLOG 5/11: remove the HP SOW file name + internal text from the demo BEFORE anyone outside Datasec sees it (C-03). 12: product observations. Waiting on Kam: the HP E8 SOW file into `1_Project_Definition/Source_Documents/` (CI's one red step).
- **The Spark:** powered down by Kam 13:58 (container stopped; laptop tunnel closed). On re-plug: the box's `run-a2.sh` + the tunnel (PORTABILITY 22). Datasec work only until Kam rules on Secuura.

## Mechanisms (paths, not pane ids)
- STATUS wake: `2_Project_Files/friday/watch_status.sh <seen-file> "<glob>"` (background; exits on a NEW READY/BLOCKED/STOP; keyed on the READY count).
- Seats: `cockpit.sh launch Datasec/<Project>-<A|B|C>` (the launcher takes the newest `_SEAT-<X>_` brief in the project's `1_Project_Definition/Briefs/`); close with `fleet/cockpit/pane_close.sh %N`. PRs and merges from Friday as kamilDatasec (`2_Project_Files/friday/friday_as.sh datasec gh …`), head-pinned squash, then watch main's push CI.

## Left in place (never delete; Kam's call)
- Stopped container `b07c-mssql` (HPSM-POC's SQL Server probe). HPSM-POC worktrees `.tools/wt-B06-A`, `.tools/wt-B07-*`. Composer compose project `pc-b03` UP on 127.0.0.1:18380 (the mobile pass's seat stack).
- On the demo VM: `authorized_keys.pre-friday-*` backups (they hold only removed PUBLIC keys).

## Owed housekeeping (older)
- Tuesday never replied to the 09-23 Spark/HPSM mails. Kam's Linear key and Jira token were pasted in chat on 09-23: rotation suggested once each, his call.

## Open claims by Friday
Spark loop · Datasec/HPSM · Datasec/HPSM-POC · Datasec/Datasec Security Composer (all OPEN: ongoing projects).
