# Spark OPERATOR round 3 (o116). Commissioned 2026-11-09 ~17:4x by the 17:3x Wednesday seat (successor of the 15:3x seat).
Why: spark_status.py at 17:35 printed "IDLE since last round 49 min ago — queue EMPTY" (rule 2026-10-28: never keep the Spark idle). Kam 2026-11-09 15:58 (live board): "spark is also back online. please use it as much as possible".

Read the round-1 commission WHOLE and follow it exactly, with the changes below: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds/commission.md
Then read the round-2 commission (its changes still apply unless overridden here): /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-2/commission.md

Changes from rounds 1 and 2:
1. ROWIDs use o116.
2. Also EXCLUDE: KS-2144, KS-2147, KS-2148 (round 2 PASSes, HELD, awaiting a raise seat); KS-1807 and KS-2151 (owed to a docs build seat); KS-2152, KS-2153 (filed today, not briefed); KS-785 (PR 2127, Seat R 91st); KS-1473 and PR 2128 (Seat G 31st); KS-624, KS-625 (PRs 2130 and 2131, gated, awaiting merge).
3. Live seats now: B 119th (merge seat, no build files) · S 45th (board seat, no build files) · G 31st (as round 2, plus PR 2128's file set) · R 91st (as round 1, plus PR 2127's file set) · T 22nd (as round 2, plus the KS-1976 and KS-1415 E10/E11 files). Lane Y is free. The open-PR census (GitHub PR API, each PR's files) is the authority for files; this list is Wednesday's reading of the briefs.
4. HOLD every PASS yourself with /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py exactly as round 2 did (a clean --dry-run first, then the real run; report each READY path and rc). Do not raise, push, post or mail.
5. Prefer the tiers that need no prepare_clone, as round 2; say which tier and why per ticket.
6. Read the round-2 output files in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-2/ (prscan.py, fetch_open.py) and reuse them rather than rewriting; their outputs (prs_*.json, open_all.json) are 70+ minutes stale: re-run, never reuse the data.
7. Stop after 4 rounds or 75 minutes, whichever first.
Output: your final message, line 1 'Spark rounds o116: <n> briefed, <p> PASS (<h> held), <f> FAIL, <q> still queued', then per ticket as round 1. If your Write is accepted, also save it to /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-3/report.md.
