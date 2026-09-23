---
date: 2026-09-23
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block — written by the 11:0x seat of 2026-09-23 after delivering FRIDAY (ctx 58%; previous copy: the newest `.pre-0923-*-friday` beside this file)

**🔴 USAGE AT THE 90% CUT (7d:90% at 12:0x).** Nothing new launches — no seat, gate, drafter or successor. Wednesday + Ornith only until the allowance renews (~4 d) or Kam signs into a new account. Re-read `fleet/usage_gate.sh --check` before ANY launch.

**Kam:** on the LIVE board. Last real rows 11:18 ("This was not me…" — about the synthetic test rows) and 11:19 ("share the Friday files"). Both answered. **Friday is DELIVERED**: his drawer holds exactly `Friday_Installer_2026-09-23.zip` (f-62f4e6c4b5) + `spark-kit_2026-09-23.zip` (f-7637d3ff2a); the 3 old files are hidden (audited, reversible). Install steps are in the chat message and the zip's README. **Nothing owed to him.** When Friday first boots on the laptop, her report on the FRIDAY tab is the test of everything below — read it (you cannot read her tab; Kam will relay, or she mails `[Friday -> Wednesday]`).

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
8. **OWED 0 (dated today):** after the 03:30 NAS leg of 09-23 FINISHES (`scheduler/state/nas_sync_last_wednesday.txt` shows 09-23; the leg ran 7h20m+ at 10:50 — an outlier; if still running near 03:30 on 09-24 two legs overlap) run `5_Project_History/2026-09-21_portable_blind_copy_KK_DEV_Local.sh` with `/Volumes/KK_DEV_Local` mounted, then tell Kam total + rc. Do NOT `tail` the unison log (`\r` progress, MB in "4 lines").

### Ornith
Queue empty after KS-1143 round 1 (FAIL at A3 = BRIEF defect, classified; excerpt design VALIDATED — see today's note 10:55). Pool is thin by measurement. Under the 90% cut, feeding Ornith is Wednesday's own brief-writing by hand (no drafter subagents). Next: rebrief KS-1143 as `test_only` (its last local round under Kam's counter).

### RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura) — unchanged from the previous pickup, carry into the next Secuura brief
`secuura-ks998-…-prettier` (a + "and install it also" — note, not machine-readable) · `secuura-ks1163-…` (a; Claude's, at the counter) · `secuura-ks974-…` (a; correct the record on KS-974) · `secuura-ks1084-part-b-…` (a). And read `decision_queue.sh list ruled --undelivered` as a LIST, not a number.

### STANDING RULES (carry)
`safe_push.sh "<message>" <paths…>` — first arg is the MESSAGE; a path list from a variable needs `${=VAR}` (zsh). `cd` REFUSED (even `cd /dev/null`). The live board's hide `--reason` accepts only `[A-Za-z0-9 ._:/()+'-]`, ≤160 chars. Builder subagents CANNOT write report files (harness) — have them return the report as text and save it yourself. A "local" dashboard matrix hits the REAL store unless the new guard stops it (`LIVE_STORE_MATRIX_OK=1` only on purpose). Read any tool output you are about to assert to Kam WHOLE, never through `tail`.
