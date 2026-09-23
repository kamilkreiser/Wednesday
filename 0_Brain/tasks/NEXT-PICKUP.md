---
date: 2026-09-23
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block — written by the 17:0x seat of 2026-09-23 (refreshed at its 50% checkpoint; previous copy: the newest `.pre-0923-*-17seat` beside this file)

**🔴 USAGE 93% (`usage_gate.sh --check` rc 3).** Only the round-20 lane runs past the cut (EXPIRING-GRANTS event row: one raise seat + its gates + its successor). No other seat, gate or drafter. Wednesday + Ornith by hand otherwise.

**Kam:** last real row 14:25:35; nothing owed to him. Told on the panel 17:2x: KS-1143 held, Seat B rotated.

### 🔴🔴 LIVE LANE — round 20 (Secuura), comes before everything below (refreshed 19:1x local)
- **TIER 2 MERGED + VERIFIED** (08:09-08:10Z): #1202 #1203 #1205 #1206 squashed at their gated heads; develop **`72f480ca3584…`**, tree `d13a26e19c8d…` == the gate's END_TREE (Wednesday via GitHub commit API). Tickets In Progress. Nothing deployed.
- **TIER 1 = SEVEN PRs, all raised + READY:** #1204 KS-851 · #1207 KS-1245 · #1208 KS-1287 (3 files) · #1209 KS-1033 · #1210 KS-1239 · #1211 KS-1084 (P0) · **#1212 KS-1143 (the Ornith self-testing READY, PR 11)** — all on base `2bc5ccf63` (ruling (a) for #1212 — my addendum's new-develop base was unreachable without a fetch; ledger row). Heads verified by Wednesday 18:32:12.
- **TIER 1: SIX MERGED + VERIFIED** (develop `dd8f99cc75b9…`, tree == the gate's END_TREE). **#1210 KS-1239 FIX ROUND (2 of 2) SENT ~20:0x** (`fleet/briefs_staged/2026-09-23_seatB22_fix1210_round2.md`): update KS-781 LEG D's line pins; its READY (round 2) is owed. **Then:** re-gate #1210 alone (tier 1; copy `fleet/qa-agent/gatesets/2026-09-23_gate20T1_seatB/`), GO, merge; **then the kintsugi deploy commission** (never demo; the lane grant ends once merged + deployed to kintsugi). If round 2 NO GOs: the cap — ticket the residue, no round 3 without Kam.
- **Seat B 22nd (%55) HOLDING** at ctx ~42%, wake acked (`wake_ack.sh %55`). Its wake path = Wednesday's mail + a pointer tap (`cockpit.sh say … --mail`).
- **Gate questions the drafter left for the verdict to settle:** #1204 is tier 1 by ruling, not by files; PR 11's tier-1 case depends on whether anything CONSUMES LEG F's output.
- Latent engine defect for the handover of round 21: `raise19.py:694-698` / the `raiseC20.py` lineage compare a cumulative count with a per-stage pair (fixed in `raise20.py` only, ruling (a)).

### 🟢 Ornith — KS-1143 HELD (the self-testing harness is BUILT)
- `night/READY_KS-1143-GUARDMENTION-SELFTEST-1_…PASS-7of7_2026-09-23.diff.md` — its ONE rebrief (R19) passed 7/7: strict apply, red 1/232 alone, green 232/232, `+`/`-` identical to the brief's golden.
- **code_patch SELF-TESTING mode** (brief line `## Self-testing — test hunks: N` + `## Red cells`): `tasks/code_patch/selftest_split.py`, `checker.sh`, `night/build_input.sh`, `night/hold_ready.py` (also fixed: excerpted inputs). Arms `local-model/tests/selftest_mode_arms.sh [CLONE]`; IMPROVEMENTS row 17:2x. **This widens the pool: any ticket whose "product" is a self-testing suite file is now briefable** — the next brief-writing pass should look for them.
- Queue empty again after KS-1143. Standing rule: Ornith constantly working — next act is a brief, by hand (no drafters at 93%).

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
8. **OWED 0 (dated today):** after the 03:30 NAS leg of 09-23 FINISHES (`scheduler/state/nas_sync_last_wednesday.txt` shows 09-23; the leg ran 7h20m+ at 10:50 — an outlier; if still running near 03:30 on 09-24 two legs overlap) run `5_Project_History/2026-09-21_portable_blind_copy_KK_DEV_Local.sh` with `/Volumes/KK_DEV_Local` mounted, then tell Kam total + rc. Do NOT `tail` the unison log (`\r` progress, MB in "4 lines").

### Ornith
See the KS-1143 block at the top (HELD 17:23). The OWED item 7 line about rebriefing KS-1143 as test_only is SUPERSEDED — it went through the new self-testing mode instead.

### RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura) — unchanged from the previous pickup, carry into the next Secuura brief
`secuura-ks998-…-prettier` (a + "and install it also" — note, not machine-readable) · `secuura-ks1163-…` (a; Claude's, at the counter) · `secuura-ks974-…` (a; correct the record on KS-974) · `secuura-ks1084-part-b-…` (a). And read `decision_queue.sh list ruled --undelivered` as a LIST, not a number.

### STANDING RULES (carry)
`safe_push.sh "<message>" <paths…>` — first arg is the MESSAGE; a path list from a variable needs `${=VAR}` (zsh). `cd` REFUSED (even `cd /dev/null`). The live board's hide `--reason` accepts only `[A-Za-z0-9 ._:/()+'-]`, ≤160 chars. Builder subagents CANNOT write report files (harness) — have them return the report as text and save it yourself. A "local" dashboard matrix hits the REAL store unless the new guard stops it (`LIVE_STORE_MATRIX_OK=1` only on purpose). Read any tool output you are about to assert to Kam WHOLE, never through `tail`.
