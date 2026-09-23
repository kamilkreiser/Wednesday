## 2026-09-23 12:37 → 13:1x AEST — FRIDAY seat (laptop), first boot → first wrap (Kam relaunches it in the cockpit)

**Friday booted for the first time, tested every tool built for it, and closed the gaps Kam named.** Boot: by-tier digest 518 KB (199 lessons) read whole; own ledger empty; ctx UNMEASURED (not in tmux — estimate ~20%).

- **First-boot test result** (posted verbatim to Kam's FRIDAY tab): doctor 10 warnings; live board, inbox, claims and chat mirror all work as seat=friday; `send_brief.sh` still labels Friday's mail `[Wednesday -> …]` (documented half-fix).
- **Spark (ZGX, DeepSeek V4 Flash), Kam's ask:** ssh alias OK; the container had been stopped 18 h (RAM freed for the Ornith comparison) — relaunched with its own `run-a2.sh`, healthy in ~4 min, now on a READ-scope HF token (Kam revoked the write token). From the laptop through a keepalive tunnel: instruct → executed code 5/5, multi-turn revision 3/3, structured tool call — all PASS. Handoff moved out of the root to `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/` with the test script. doctor check (friday only, both branches exercised) + PORTABILITY 22.
- **Docker** on the laptop: hello-world rc 0.
- **Gauge fix** (claimed → fixed → released; Wednesday mailed): `publish_usage.sh` refused seat `friday` (server and poster already knew it) — fixed, `Launch_Friday.command` arms it each launch; live publish 201, read-back 200 (friday 60%). Commit 5b161a71c.
- **Linear** configured with Kam's key (`.env` only; verified absent from all git history): WED started 5 · unstarted 22 · backlog 82; lesson 0 (validated); overdue WED-147, WED-48.
- No corrections, no ledger rows, no lessons filed. Pickup: `0_Brain/tasks/NEXT-PICKUP-FRIDAY.md` (replaced wholesale); FIRST-BOOT-FRIDAY.md retired.

