---
date: 2026-10-09
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-09 ~09:4x by the morning seat (booted ~09:12, ctx ~62%). Previous copy in that session's scratchpad (NEXT-PICKUP.pre-1009.md); its owed items are carried below. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 KAM'S STANDING WORDS TODAY (read first; all receipted on the panel)
- **MODEL: every agent Wednesday starts (pane seats AND Agent-tool sub-agents) runs on Opus 5.5 "for now"**, until the model-review phase makes it deliberate (Kam ~09:4x, superseding his ~09:3x "Spark, Ornith and Sonnet until Monday"). Sonnet trial WED-153 PAUSED. Spark/Ornith first where the predicate fits. Project launchers pin Opus 5: switch each seat with `/model claude-opus-5-5` typed by `tmux send-keys` at an IDLE prompt (NOT `cockpit.sh say`: it prefixes `[Wednesday tap]` and the command arrives as a message — ledger 10-09) and verify the statusline reads Opus 5.5. Agent-tool drafters: omit `model` (they inherit this seat's Opus 5.5). Grant: `learnings/2026-10-09_spark-ornith-sonnet-only-until-monday.md` (top block). Kam signs Wednesday into its own account Monday 12 Oct.
- **Boot model check** (Kam): built — `tools/latest_models.sh` → `0_Brain/dashboard/data/models_latest.json`; spec `fleet/specs/model-routing.md` v0 (share with Tuesday/Friday by coordination mail after Kam has seen it; no client content). 13 stale project pins reported to Kam; their fix is each project's agent or Kam.
- **Stuart's list** (Kam: "please look at a message from Stuart"): report `0_Brain/reference/2026-10-09_stuart-list/REPORT.md`. Reply text handed to Kam on the panel (he sends). Cards: `secuura-ks1195-s-key-ceiling-1009` (rec a 3,000/h new keys; default 18:00 brief a, nothing merged), `secuura-ks1384-anchor-per-event-1009` (rec c measure first; default 18:00 read-only trace). The housekeeping promise to Stuart = KS-1387, KS-1172, KS-1175 CLOSED TODAY (board seat); KS-1173 after its residues; KS-577 stays open.

## FLOOR UPDATE (10:1x, 66% checkpoint) — supersedes the 09:4x floor where they differ
- **%4 Seat J 1st** (`Secuura/Blockchain-J`, NEW lane: routing line + launchers.conf entry added 10:1x, backups `.pre-1009-laneJ`), board seat: closes **KS-1172 and KS-1175 only**; **KS-1387 HELD** (Peter's revert PR #1360 open; card `secuura-ks1380-peter-reverting-1358` = b). Brief `fleet/briefs_staged/2026-10-09_seatJ1_board_housekeeping_SEND.md`. Owed: its plan ANSWER carrying the literal `WRITE (Seat J 1st)` + the two body sha256s (read the bodies first; client-visible text); the idle-prompt `/model claude-opus-5-5`. **Tell Kam KS-1387 stays open (his Stuart reply said it closes today).**
- **F 6th now on Opus 5.5** (typed 09:5x, dialog confirmed). Plan ANSWER sent 22:50Z: proceed to raise base; objects transfer moved to R 21st. Next from it: `STATUS: raise base`.
- **R 21st** still booting on Opus 5 at 10:0x: switch by hand at its plan mail (send-keys, then Enter twice: the command, then "Yes, switch" on the confirm dialog).
- **K 1st (KS-1402) brief READY to read:** `fleet/briefs_staged/2026-10-09_seatK_build_ks1402_DRAFT.md` (323 lines). Mechanism = a DB lookup by originate's own DB login (Wednesday accepts it as a technical reading of Kam's "own service credential"; send Kam a one-line FYI with veto when launching). Its Qs: lane K, lock `.push-lock-g1`, flow 44, Q-OBJ-K waits on R 21st's transfer. Needs routing + launchers.conf lines for `-K` like J.
- **send_brief's undelivered-ruling gate does not map `-J` (and will not map `-K`)**: the J brief went out with no ruled-cards section and no refusal (the 10-08 registry-gap class, again). OWED: unknown `Blockchain-*` tag REFUSES.

## FLOOR (09:4x)
%0 wednesday · %1 monitor · **%2 Seat F 6th** (`Secuura/Blockchain-F`, KS-808 raise, brief `fleet/briefs_staged/2026-10-09_seatF6_raise_ks808_SEND.md`) · **%3 Seat R 21st** (`Secuura/Blockchain-R`, #1427 merge-in + squash, brief `…_seatR21_merge1427_SEND.md`). Both booting on Opus 5; background waiters (`scratchpad/model_when_idle.sh`, log `scratchpad/model_switch.log`) type `/model claude-opus-5-5` when each turn ends — CHECK the log + statuslines; a rotation kills the waiters (re-type by hand at an idle prompt).
- **Owed to F 6th:** plan ANSWER (read WHOLE through NEEDED-BY) — **SUPERSEDE its amendment item 2 by name: the objects transfer is R 21st's, F 6th checks presence and transfers nothing.** Q-READ808: Wednesday reads the built run-migrations diff before its push. Ctx reads by pane (`seat_ctx.py` if no statusline).
- **Owed to R 21st:** plan ANSWER; then its `STATUS: re-prediction` → ANSWER carrying the literal `START STEP 2 (Seat R 21st)`; ctx reads; after M is pushed + qm green: GO 2 built from the brief's M1 table and run against its extracted builder regexes (13/13, `qm Q2 STRICT` + `qm green` PRESENT, `4998 bytes` no comma) + the separate ADDENDUM (`ACTIONS VERDICT (Wednesday):` + `0 new failures`); verify the squash at source; WRAP → score → `pane_close.sh %3`.
- Both seats were mailed `ADDENDUM … model is Opus 5.5` (09:3x).

## DRAFTERS RUNNING (background; a rotation kills them — re-commission from today's note)
- gate77 kit → `fleet/qa-agent/gatesets/2026-10-09_gate77/KIT_REPORT.md` (#1429-#1434). On return: read whole, rule Qs, re-pin right before launch, launch the gate on Opus 5.5, AFTER #1427 lands (develop moves).
- Board housekeeping + KS-1402 build briefs → `fleet/briefs_staged/2026-10-09_seat*_board_housekeeping_DRAFT.md`, `…_build_ks1402_DRAFT.md`. Check the KS-1402 mechanism vs Kam's words ("own service credential") before sending.
- KS-695 ask 3 / KS-723 / KS-1385 slice 1 briefs → `fleet/briefs_staged/2026-10-09_seat*_DRAFT.md`.
Each: read WHOLE, rule its Qs, SEND AMENDMENT (develop, floor, model), `brief_and_launch.sh`, then the idle `/model` switch.

## LOCAL MODELS
- **Spark:** KS-1438 round 2 queued (`spark/queue.md`); if it FAILS, KS-1438 goes to a Claude seat (counter spent). Check `spark/done.md`.
- **Ornith 1.5:** queue empty with a measured why-line (19 tickets read, 0 fit). KS-937 HELD (`night/READY_KS-937-…2026-10-09.diff.md`) → raise with the next raise seat; it widens a push guard, so its gate proves the guard still refuses its targets.

## OWED (Wednesday tooling)
- `wed_claim.sh:54` / `safe_push.sh:108` internal `--autostash` (w=5 today; zero loss) → `safe_pull.sh`. After ANY `wed_claim.sh`, `git stash list` + `git status` before committing.
- `cockpit.sh model <pane> <id>` (idle-prompt send-keys + statusline verify), from today's waiter prototype.
- Release the `wed_claim` claim for the models check once Kam has seen the spec (`wed_claim.sh release`).
- Carried from 10-08: `Launch_Wednesday.command` step-5 seat-note resolver line; c4 selftest scratch reuse; `commitg1.sh:68` untracked blind spot; commit tools miss duplicate `Refs`; send_brief REFUSE unknown `Blockchain-*` tag; delivery sweep of the 64 undelivered secuura- cards; #1430/#1431 "unnamed legs" body polish (gate77); #1428 docs follow-up (N-1428-1/2/6).

## STANDING NOTES
- Pathspec-only commits; pull with `tools/safe_pull.sh`. decisions.json and chat stores are STATE.
- A seat cannot read its own context: gates are mail handshakes; Wednesday reads the pane.
- Before any GO, copy the seat's GO shape from its brief and run its builder regexes against it.
- Grants live: October deploy (to Sat 31 Oct), week instruction (to Sun 11 Oct), TESTED merge grant (open-ended), Opus-5.5-for-all-agents (until the model review). The over-90% grants of 10-08 are EXPIRED.
