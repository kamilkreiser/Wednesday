---
date: 2026-09-23
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop — claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, first wrap 2026-09-23 ~13:1x (Kam: "wrap up for now and I will relaunch in the cockpit")
supersede: replace wholesale at every wrap; do not append
---

# NEXT PICKUP — FRIDAY

**State at wrap:** no project claimed by Friday, no agent briefed, no card open. Kam gave this seat no week
instruction (`WEEK-INSTRUCTION-FRIDAY.md` status none). He is relaunching Friday **inside the cockpit (tmux)** —
so at boot, **read the statusline `ctx:NN%` from the pane** (the first boot could not: it ran outside tmux, and
its "~20%" was an estimate).

## OWED — first work of the next session
1. **Confirm the cockpit relaunch fixed the instrument:** `tmux display-message -p '#{pane_id}'` returns a pane,
   and the statusline is readable. If Friday is still outside tmux, say so to Kam in one line.
2. **Nothing else is owed to Kam.** Wait for his first instruction on the FRIDAY tab; do not drive either client
   unprompted.
3. **THE SPARK LOOP IS FRIDAY'S (Kam 2026-09-23 ~14:1x: "its yours as you will be using the spark"; claimed in wed_claim.sh).** Owed: spark-kit file 05's setup, read as addressed to Friday: place 01 as the system prompt → inventory the box (how the model is invoked, any apply/test harness, a working copy of the target repo, the configured context) → build/identify a checker meeting all six contract clauses → smoke test incl. the TWO deliberate breaks → report to Kam. Method: `learnings/2026-09-23_spark-kit-running-a-local-coding-model.md`; kit: `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/spark-kit_2026-09-23/`. **Datasec work only on the Spark until Kam rules on Secuura code** (the box is `datasec-rd`; asked 14:0x, unanswered).

## What works on this seat (measured 2026-09-23)
- Live board as seat=friday: `kam_rulings_today.sh`, `chat_reply.sh` (HTTP 201 to the Friday partition).
- Mail: `friday-laptop-agent@agentmail.to` sends and receives. ⚠ `send_brief.sh` still prefixes subjects
  `[Wednesday -> …]` (line ~621, a documented half-fix — the prefix is the fleet's routing key). **Every brief
  Friday sends says in its first lines that it is from Friday and that replies go to friday-laptop-agent@.**
- Linear: `LINEAR_API_KEY` + `LINEAR_TEAM_ID` in `4_Credentials/.env` (Kam's key, account Wednesday, team WED).
  At wrap: started 5 · unstarted 22 · backlog 82 · lesson-label 0 (validated). Overdue: WED-147, WED-48.
- Usage gauge: `publish_usage.sh` accepts `friday` (commit 5b161a71c); `Launch_Friday.command` arms it each
  launch; live row friday 60% at 12:55.
- Docker Desktop 29.7.2: hello-world rc 0.
- **Spark (ZGX) DeepSeek V4 Flash:** container relaunched 12:47 (it had been stopped 18 h to free RAM), health OK;
  tunnel `ssh -f -N … -L 8888:127.0.0.1:8888 ZGX-Nano-G1n` running (pid 29671 at wrap — it does NOT survive a
  laptop reboot; re-open with HANDOFF.md §1). Instruct / multi-turn / tool-call tests 3/3 PASS. Handoff, test
  script and output: `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/`. It is a MODEL ENDPOINT, one request
  at a time, thinking OFF for coding; the agent loop lives on our side. `doctor.sh` checks it for friday only;
  PORTABILITY item 22.

## Not working / Kam's hands
- Secuura: no gh, no az under `friday_as.sh secuura`. Datasec: gh `kamilDatasec` OK, no az. Log in when Kam
  wants Friday driving a client.
- The Linear key was pasted in chat (it is in the session transcript). Kam told; rotation is his call.
- Doctor leftovers, all known: Matilda Premium not downloaded (browser speaks anyway) · DevMASTER not mounted ·
  stale `--model` warning (launcher deliberately unpinned by Kam 09:33) · stale 09-13 grants warning · exec-bit
  warning cosmetic (0 of 1070 git-executable files lack +x) · Tuesday's ledger 3c rows (hers).

## Open claims by Friday
None (the gauge claim was released after the fix).
