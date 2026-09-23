---
date: 2026-09-23
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday (terminal seat), wrap 2026-09-23 ~14:1x. Kam: "wrap up please and I will restart the cockpit"
supersede: replace wholesale at every wrap; do not append
---

# NEXT PICKUP — FRIDAY

**State at wrap:** Kam is restarting the cockpit. This session ran as a DUPLICATE Friday OUTSIDE tmux. The cockpit's
`up` had died on the usage gate after starting a Friday in pane `%0`, so two Friday seats ran at once. The cause is
fixed (below). At boot: `tmux display-message -p '#{pane_id}'` must return a pane and the statusline `ctx:NN%` must be
readable. **Then `ps -axo pid,tty,command | /usr/bin/grep -c "You are FRIDAY"` should find ONE Friday claude process.**
If there are two, tell Kam in one line which one to close (the one outside tmux).

## OWED — first work of the next session
1. **THE SPARK LOOP IS FRIDAY'S.** Kam, 2026-09-23 ~14:1x, verbatim: *"the kit is addressed to tuesday but it
   should be addressed to you. its yours as you will be using the spark"*. Claimed in `wed_claim.sh` (OPEN). The owed
   work is spark-kit file 05's setup, read as addressed to Friday:
   (a) put `01_FOR_THE_LOCAL_MODEL.md` where tasks get their system prompt;
   (b) READ-ONLY inventory of the box: how the model is invoked, any apply/test harness, a working copy of the target
   repo, the configured context;
   (c) build or identify a checker meeting all SIX contract clauses;
   (d) smoke test on a trivial known change, plus the TWO deliberate breaks (a wrong expected line must fail clause 2;
   a non-existent line number must fail clause 1);
   (e) report to Kam.
   Method: `0_Brain/learnings/2026-09-23_spark-kit-running-a-local-coding-model.md`. Kit:
   `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/spark-kit_2026-09-23/`. The box's facts are in `HANDOFF.md`
   in the same folder: `max_model_len` 384K; thinking ON by default (run coding with it OFF); `MAX_NUM_SEQS=1`; the
   container is often stopped. The tunnel does not survive a reboot. Told Kam the default "starting setup unless you'd
   rather wait"; he answered with the wrap, so it is not yet started.
2. **OPEN WITH KAM (asked 14:0x, unanswered):** may Secuura code go on the Spark? Its login is `datasec-rd`, and the
   kit says it was commissioned for Datasec. **Default until he rules: Datasec work only.**
3. **Tuesday has been told** (mail 04:07Z) that the Spark is Friday's, and to mail Datasec ticket ids she wants put
   through it. Read her reply at boot, if any.

## Done this session (do not redo)
- **Cockpit usage gate fixed** (commits 4413174ca and 0b171e8a7, on origin via d9e7bb6d1):
  - `usage_gate.sh` resolves the seat from the tree via `cockpit/seat_resolve.sh`. It used to fall back to `wednesday`,
    so on the laptop it read the Studio's 90% gauge.
  - `cockpit.sh up` no longer usage-gates its own conf panes (the fleet-monitor refusal had died mid-`up`).
  - `unset COCKPIT_UP_BUILD` at the top (Wednesday's hardening).
  - Arms all pass. Wednesday verified the change on the Studio at 90%.
- The fleet-monitor pane was added to the old session as `%6` (the restart may replace it).
- Lessons filed: `2026-09-23_fix-it-yourself-talk-to-sister-seats-directly.md` (ledger w=1) and the spark-kit lesson
  (ledger ruling row). Both digests regenerated.
- Mail: every sister-seat mail sent through `send_brief.sh` and its sent copy verified. Wednesday's two replies read.

## What works on this seat (measured 2026-09-23)
- Live board as seat=friday (`kam_rulings_today.sh`, `chat_reply.sh`). Mail `friday-laptop-agent@` (the subject prefix
  stays `[Wednesday -> …]` by design; the first line says it is from Friday).
- Linear (`LINEAR_API_KEY` + `LINEAR_TEAM_ID` in `.env`): started 5 · unstarted 22 · backlog 82 · lesson 0. Overdue:
  WED-147, WED-48.
- Usage gauge: friday ~61% (7-day), renews in ~3d 14h.
- Docker Desktop OK. Spark endpoint 3/3 PASS at 12:52 (thinking off).

## Not working / Kam's hands
- Secuura: no gh/az under `friday_as.sh secuura`. Datasec: gh `kamilDatasec`, no az.
- The Linear key was pasted in chat (it is in a transcript). Rotating it is Kam's call.

## Open claims by Friday
- Spark (ZGX, DeepSeek V4 Flash) local-model loop + spark-kit setup: OPEN (owed item 1).
