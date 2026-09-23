## 2026-09-23 13:12 → 14:1x AEST — FRIDAY seat (laptop, terminal copy outside tmux) — cockpit gate fixed; spark-kit adopted; the Spark ruled Friday's

**Kam's cockpit launch refused on the laptop, and that is how two Fridays came to run at once. Friday fixed the cause, adopted Wednesday's spark-kit, and Kam ruled the Spark is Friday's.**

- **Duplicate seat found by the process table:** `Launch_Cockpit.command` → `cockpit.sh up` started Friday in `%0`, then the usage gate refused the fleet-monitor pane and `up` died, so the window closed and the seat ran headless. Kam then opened a second Friday (this one) outside tmux. This seat wrote nothing until Kam chose which one to work with.
- **Fix** (4413174ca + 0b171e8a7): `usage_gate.sh` resolves the seat from the tree through `seat_resolve.sh` (the `wednesday` fallback read the Studio's 90% gauge instead of Friday's 61%); `up` no longer gates its own conf panes; `COCKPIT_UP_BUILD` is unset at the top (Wednesday's hardening). TESTED: gate 8/8, rebase arms 5/5, scratch-socket arms (old up@95% rc 1 = the defect; new up builds both; add@95% refused incl. an exported bypass, which was a real hole on 4413174ca; add@50% ok). Wednesday verified on the Studio at 90%.
- **Correction (ledger w=1):** Friday first handed the fix to "the cockpit Friday" with a sentence for Kam to relay. Kam: *"You will need to fix it, but if you need something done by Wednesday, send Wednesday an email and communicate with her directly."* Filed as a lesson.
- **Spark-kit** (Wednesday's, from "1FILES TO SYNC"): filed under `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/spark-kit_2026-09-23/` and adopted as a lesson, with this box's measured differences (384K context, thinking ON by default, one request at a time). Wednesday folded them into her kit's 04. **Kam ruled the Spark is Friday's** ("its yours as you will be using the spark"): claimed, Tuesday and Wednesday mailed directly. OPEN: Secuura code on the `datasec-rd` box; default Datasec only.
- Pickup replaced wholesale: the Spark setup (kit 05) is owed item 1.

## 2026-09-23 12:37 → 13:1x AEST — FRIDAY seat (laptop), first boot → first wrap (Kam relaunches it in the cockpit)

**Friday booted for the first time, tested every tool built for it, and closed the gaps Kam named.** Boot: by-tier digest 518 KB (199 lessons) read whole; own ledger empty; ctx UNMEASURED (not in tmux — estimate ~20%).

- **First-boot test result** (posted verbatim to Kam's FRIDAY tab): doctor 10 warnings; live board, inbox, claims and chat mirror all work as seat=friday; `send_brief.sh` still labels Friday's mail `[Wednesday -> …]` (documented half-fix).
- **Spark (ZGX, DeepSeek V4 Flash), Kam's ask:** ssh alias OK; the container had been stopped 18 h (RAM freed for the Ornith comparison) — relaunched with its own `run-a2.sh`, healthy in ~4 min, now on a READ-scope HF token (Kam revoked the write token). From the laptop through a keepalive tunnel: instruct → executed code 5/5, multi-turn revision 3/3, structured tool call — all PASS. Handoff moved out of the root to `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/` with the test script. doctor check (friday only, both branches exercised) + PORTABILITY 22.
- **Docker** on the laptop: hello-world rc 0.
- **Gauge fix** (claimed → fixed → released; Wednesday mailed): `publish_usage.sh` refused seat `friday` (server and poster already knew it) — fixed, `Launch_Friday.command` arms it each launch; live publish 201, read-back 200 (friday 60%). Commit 5b161a71c.
- **Linear** configured with Kam's key (`.env` only; verified absent from all git history): WED started 5 · unstarted 22 · backlog 82; lesson 0 (validated); overdue WED-147, WED-48.
- No corrections, no ledger rows, no lessons filed. Pickup: `0_Brain/tasks/NEXT-PICKUP-FRIDAY.md` (replaced wholesale); FIRST-BOOT-FRIDAY.md retired.

