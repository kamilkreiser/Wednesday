---
date: 2026-09-23
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block — written by the 17:0x seat of 2026-09-23 at its ROTATION (~23:5x, ctx ~79%); previous copy: the newest `.pre-0923-*-rotate` beside this file

**FLOOR CLEAR:** `%0 wednesday` + `%9 fleet-monitor` only. No Claude seat or gate live. **Usage 7d:97%** — the round-20 lane grant is EXPIRED (moved in EXPIRING-GRANTS), so the 90% cut governs every launch: **nothing new launches** until the allowance renews (~3 d 14 h) or Kam signs into a new account.
**Kam:** last real row 14:25:35; told on the panel at every milestone (last 23:4x: kintsugi deployed + verified). Nothing owed to him. It is past 23:00 — **no voice until 06:00.**
**Tuesday:** still silent since ~12:19 (no reply to the 14:20 check-in). Relaunch on the mini is Kam's hands; tell him in one line when she replies.

### ✅ ROUND 20 — DONE END TO END (do not re-derive)
11 PRs merged (#1202-#1212, incl. the local model's #1212 KS-1143), all verified at source; kintsugi runs develop `6ab9d5021e96` (rounds 19+20) verified V1-V13 with controls, KS-535 held, demo untouched; rule-7 comments posted 13:53Z and verified ON LINEAR (KS-601 / KS-485 Peter / KS-772 Stuart) after Wednesday corrected two overclaims. Seat B 21st/22nd/23rd scored 0.95/0.97/0.93. **All eleven tickets stay In Progress — the CLOSING PASS is Wednesday's** (a morning item: which of them can close now that they are deployed and verified).

### CARRY TO THE NEXT SECUURA BRIEF (when a launch is possible again)
1. LEGD-BYTEXT — KS-781 LEG D should pin by TEXT not NUMBER (six moves so far) → a ticket.
2. `.dockerignore` `tests` does not match `__tests__` → test sources ship into runtime images; ~23 needless rebuilds per shared change → a ticket (Seat B 23rd's measurement is in its handover).
3. The latent cumulative-count defect in `raise19.py:694-698` / the `raiseC20.py` lineage (fixed in `raise20.py` only).
4. KS-1143 / #1212's INDIRECT-INVOCATION false negative stays open on KS-1143; KS-1084 (P0) stays open: cross-tenant effect NOT measured + Part B out.
5. The four RULED-BY-KAM undelivered cards (below) still ride.

### 🟢 Ornith — KS-1143 HELD (the self-testing harness is BUILT)
- `night/READY_KS-1143-GUARDMENTION-SELFTEST-1_…PASS-7of7_2026-09-23.diff.md` — its ONE rebrief (R19) passed 7/7: strict apply, red 1/232 alone, green 232/232, `+`/`-` identical to the brief's golden.
- **code_patch SELF-TESTING mode** (brief line `## Self-testing — test hunks: N` + `## Red cells`): `tasks/code_patch/selftest_split.py`, `checker.sh`, `night/build_input.sh`, `night/hold_ready.py` (also fixed: excerpted inputs). Arms `local-model/tests/selftest_mode_arms.sh [CLONE]`; IMPROVEMENTS row 17:2x. **This widens the pool: any ticket whose "product" is a self-testing suite file is now briefable** — the next brief-writing pass should look for them.
- Queue empty again after KS-1143. Standing rule: Ornith constantly working — next act is a brief, by hand (no drafters at 93%).
- **UPDATE 2026-09-24 00:1x (the 00:00 seat): Ornith is BLOCKED ON AN INPUT, not on an empty pool.** `build_input.sh` REFUSES every ticket (G6, rc 2, measured): origin develop `6ab9d5021e96` is not in the Secuura checkout's object store (local develop `2bc5ccf63`; rounds 19+20 were merged via the GitHub API; 32 commits under Blockchain/Dev, so no `tip_override` is possible). **FIRST ACT of the next Secuura seat (whenever a launch is allowed): `git fetch origin develop` in its checkout** — and every future Secuura brief carries "fetch develop before you wrap" as a standing line. **STAGED, READY TO QUEUE the moment the tip is local:** `local-model/night/briefs/KS-1131.md` (item 1 F-A only, SELF-TESTING, 2 hunks; golden applies at fuzz 0 at `2bc5ccf63`; red/green SIMULATED in node with the file's own helper lines; the exact build command is the 09-24 00:09 line at the foot of `night/queue.md`). KS-1131 items 2-4 (F-B `:206`, F-C `:256`, P2 wallet slice) are the next three briefs — region-disjoint, same file.

### 🔴 OPEN — TUESDAY SILENT since ~12:19 (last commit `030b28c28` 12:19; no reply to the 14:20 check-in as of 17:2x). Kam knows (14:18) and a relaunch on the mini is HIS hands. When her reply lands, tell Kam in one line.

### What FRIDAY is (do not re-derive)
Third coordinator seat, Kam's laptop, BOTH clients. Launcher `Launch_Friday.command` (refuses outside a FRIDAY tree) → `2_Project_Files/friday/first_run.sh` once → shared `Launch_Wednesday.command` with `WED_AGENT=friday`. Inbox `friday-laptop-agent@agentmail.to`. Live-board partition `Friday` (Entra `friday-seat` be8404ab-…). Per-client identity via `friday/friday_as.sh`. Claims every project with `wed_claim.sh` before driving it. Reports: `fleet/REPORT_2026-09-23_friday-seat-tools.md`, `dashboard-cloud/REPORT_2026-09-23_friday-seat.md`. Brain: `tasks/FIRST-BOOT-FRIDAY.md`.
**⚠ The Friday certificate ALSO sits on the Studio (`4_Credentials/dashboard-cloud/friday-seat.pem`) — this machine can act as Friday while it does. Never use it from this seat except to verify.**

### OWED (mine; none blocks Kam; all are Wednesday-only tooling, doable under the 90% cut)
1. `dashboard-cloud/seat/publish_usage.sh:30` → accept `friday`. It is RUNNING (pid 9380 at 11:5x): stop the loop, edit, run once, re-arm (never edit a running bash script).
2. doctor.sh warns "Launch_Wednesday.command has no recognisable --model line" — stale since Tuesday's e402c5bc7 (10:35, Kam 09:33 on HER tab: launchers follow the configured default). The PREVIOUS pickup's claim that the launcher pins `--model claude-opus-5-5 --fallback-model opus` is FALSE — it was unpinned. Fix the check to accept "no pin"; read Kam's 09:33 words on the Tuesday tab first.
3. `get_kam_messages.py --json` does not filter synthetic rows (text output does).
4. No `fleet/USAGE_STOP.friday` — Friday inherits Wednesday's cut. Ask Kam only if it bites.
5. Friday cannot read the 3 pre-existing ALL rows until `migrate_rewrap.py` (changes live rows — it was not run).
6. Literal "wednesday" pane names in cockpit.sh:90,460 · pane_close.sh:72 · pane_prompt_check.sh:29 · monitor.sh:213 · tap_wednesday.sh:78 (Tuesday has the same gap).
7. Carried from before: `hold_ready.py` cannot carry a card ruling; `night_run.sh:403` discards G7 alert stderr (stop job → edit → --once → re-arm); code_patch builder should refuse `product_file` under `__tests__/` (KS-1143 is ONE round, rebrief as test_only is its last local round); `checker.sh:660` `2>/dev/null` on a3c_plus.
8. ✅ **DONE 2026-09-24 00:40 (rc 0, 534,663 files / 44 GB; Kam told on the panel) — do not re-run.** Was: **OWED 0 (dated today):** after the 03:30 NAS leg of 09-23 FINISHES (`scheduler/state/nas_sync_last_wednesday.txt` shows 09-23; the leg ran 7h20m+ at 10:50 — an outlier; if still running near 03:30 on 09-24 two legs overlap) run `5_Project_History/2026-09-21_portable_blind_copy_KK_DEV_Local.sh` with `/Volumes/KK_DEV_Local` mounted, then tell Kam total + rc. Do NOT `tail` the unison log (`\r` progress, MB in "4 lines").

### Ornith
See the KS-1143 block at the top (HELD 17:23). The OWED item 7 line about rebriefing KS-1143 as test_only is SUPERSEDED — it went through the new self-testing mode instead.

### RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura) — unchanged from the previous pickup, carry into the next Secuura brief
`secuura-ks998-…-prettier` (a + "and install it also" — note, not machine-readable) · `secuura-ks1163-…` (a; Claude's, at the counter) · `secuura-ks974-…` (a; correct the record on KS-974) · `secuura-ks1084-part-b-…` (a). And read `decision_queue.sh list ruled --undelivered` as a LIST, not a number.

### STANDING RULES (carry)
`safe_push.sh "<message>" <paths…>` — first arg is the MESSAGE; a path list from a variable needs `${=VAR}` (zsh). `cd` REFUSED (even `cd /dev/null`). The live board's hide `--reason` accepts only `[A-Za-z0-9 ._:/()+'-]`, ≤160 chars. Builder subagents CANNOT write report files (harness) — have them return the report as text and save it yourself. A "local" dashboard matrix hits the REAL store unless the new guard stops it (`LIVE_STORE_MATRIX_OK=1` only on purpose). Read any tool output you are about to assert to Kam WHOLE, never through `tail`.
