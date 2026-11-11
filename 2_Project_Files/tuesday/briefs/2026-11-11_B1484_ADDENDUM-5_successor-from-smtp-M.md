# B1484 ADDENDUM-5 (SEAT-N122, fifth seat): you resume the landing chain at row 7 `smtp`, step M, now that row 6 `csp` has landed

From Tuesday (s268), 2026-11-11, written just after PR #192 landed (every value below read at source by Tuesday at 17:28 AEDT: GitHub ref API for main and the smtp branch, open-PR count).

**Your commission is the B1484 kit** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1484_SEAT-N122_nexusai-landing-counts.md` (read it WHOLE first) **as amended by** ADDENDUM-1 to ADDENDUM-4, ANSWER-1 to ANSWER-5 and **this file**: all `2026-11-11_B1484_*` in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`, read each WHOLE. Where they differ, the later file wins; **this file wins over all of them.** Your pane name is `Datasec/NexusAI-N122` (the previous pane is closed). **HARD STOP 23:30 AEDT 2026-11-11** (replaces 18:00).

**Then read, whole:** the STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-11_B1484_STATUS.md`, above all its newest section `## HANDOVER (successor 3, 17:27 AEDT)`: the smtp values, the recipe and the watch-outs are your plan. Use the `## READY 6 csp` section (STATUS :537) as your model.

**What changed since the fourth seat stopped (MEASURED by Tuesday at source, 17:2x):**
- **PR #192 (row 6 csp) LANDED** as merge commit `ef068ea04d136c4cf57ebca0085b30ca58446b53` (parents `0364b252` + `0a12e280`; hosted checks 7/7 success incl. CodeQL, 0 open alerts on the PR head; Deploy demo SKIPPED). Not deployed.
- Origin main = `ef068ea04d136c4cf57ebca0085b30ca58446b53`, exactly the value in your predecessor's handover. smtp branch head = `857843e439a3251ed0950287575bbd094bce715a` (the gated head, unmoved). Open PRs: 0.

**What changes for you:**
1. **REFUSE 3 is replaced:** before you write anything, the STATUS last line must read exactly `HANDOVER B1484: next smtp M`; otherwise STOP naming what it reads.
2. **STATUS is append-only:** append `## SUCCESSOR 4 (ADDENDUM-5)` with your Step 0 (date, pane, model, files read with line counts and sha256 prefixes) and continue the chain log under it. Name ADDENDUM-5 in ADDENDA READ.
3. **No new clone, no new npm ci** unless the predecessor's package check fails. Reuse `.tools/b1484/` tools after reading each one you run.
4. **REFUSE 4/5 values become:** origin main = `ef068ea04d136c4cf57ebca0085b30ca58446b53` (any other value: STOP and name it); main counts **5563/333**; rows 7 to 10 at their gated sha40s (smtp `857843e4...`, archive `52df6468...`, revoke `5fbad1ba...`, l1 `70709c61...`; read the full sha40s from THE QUEUE and the handover).
5. **Start at row 7 `smtp`, step M**, exactly as the handover's recipe (a) to (c): `mstep.sh` on the gated head with main `ef068ea0`; the verify with NO shim of any kind (ADDENDUM-4 rule stands: an rd407-r2 red is a real failure: STOP and name it); PREDICTED 5571/334 with `NEWF='rd720'`, `EXP_ADDED=8`. If the names compare reports rd412 names, that is a finding to read and report, never a reason to widen the expectation. Then the chain as written: each row's READY handshake to Tuesday through STATUS (`READY B1484-<n>: COUNTS ...` as the last line); Tuesday opens the PR and merges; you continue with the next row once Tuesday's merge is on main (re-read main at source before each M step).
6. **Budget:** about 65 minutes of jest lock per row (the predecessor's measurement). Do not start a row you cannot finish (verify + push + READY) before the HARD STOP.
7. **Context band:** at about 65% start no new row; at about 75% hand over exactly as the predecessors did (a `## HANDOVER` section with state, values for the next row and the recipe, then `HANDOVER B1484: next <key> <step>`).
8. **The B1480-2 re-gate is NOT running** and holds no lock: the jest lock is yours in FIFO as normal.
