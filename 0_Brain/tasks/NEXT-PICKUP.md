---
date: 2026-09-16
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — but Kam STOPPED her seat 2026-09-14 and on 2026-09-16 commissioned Wednesday to FIX her structure ("do everything possible to make Tuesday work properly", 15:06). He added 14:02 "Feel free to read the Datasec content." So Datasec content is readable for THAT task; Datasec client WORK is still not Wednesday's.
source: replaced WHOLESALE at 15:08 by the 13:2x seat before rotating at the band. Previous copy: .pre-1508-wholesale.
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **Kam's standing words today:** 13:32 the allowance ran out ~12:00; he is on a **DATASEC sign-in**, *"minimal or limited Secuura work on this account… until Sunday when we'll switch over to my account"* · 13:35 *"analyzing what's working properly and address anything and fix anything… continue working with the local LLM on backlog and to-do tickets"* · 14:23 *"go ahead and, if there's anything else that you can do to improve things for both yourself and Tuesday, do that too"* · 15:06 *"do everything possible to make Tuesday work properly. If you need anything for this, put it on a fleet activity tile for me."* · 09:53 *"If something's blocking, move on to the next"* · **he leaves MONDAY NIGHT 2026-09-21.** First person on the panel. **A seat may END ITS TURN only with the model RUNNING or a batch QUEUED.**

## 🔴 FIRST ACTS
1. `kam_rulings_today.sh` — every line, before any card or brief.
2. **Check the KS-692 brief** (`night/briefs/KS-692.md`). An agent is writing it; `autostart_on_brief.sh --tier vitest` is ARMED on it and will build, queue and launch by itself. If it landed and ran, read the verdict and write the READY. If the agent refused instead, card it.
3. **Read the sync** (tmux `syncleg`, log `/private/tmp/sync_t9d.out`). Then run the **KK_DEV_Local** leg — Kam asked for it at 15:05 and it waits for the T9 leg to finish. Case check already done: no clashes, nothing on that drive that is not on DevMASTER.
4. Feed Ornith. If nothing is briefable, commission one (see COMMISSIONING).

## ✅ WHAT LANDED THIS SEAT (13:2x → 15:08)
- **Ornith idle 09:58→13:32 was only half the token cap.** The ollama server died (Kam 13:43: a system update) and G5 refused six cycles into a log nobody reads. **G5 now self-heals** via the new `start_ollama.sh`; **G8** escalates any gate refusing ≥30 min to Kam's panel. Arms 6/6 with the control that the same condition still refuses when the self-heal is off.
- **Storage (Kam 13:40–15:00):** his 141 GB ollama store moved to `/Volumes/DevMASTER/SYSTEM/ollama`, hash-verified on the three largest blobs, **merged with the fleet's so ONE server holds all 13 models**, pointers set on all three surfaces, old store binned on his word. `night_run.sh` PINS its own path so the new global cannot redirect it. **Docker's move lost his images** — told him leading with it; he ruled it an acceptable loss.
- **TUESDAY — the answer overturned the hypothesis.** The trees have NOT diverged (every hook, tool, script and skill byte-identical; launcher differs by 12 lines). **Four layers differed, none in git.** Fixed: tracked `.claude/settings.template.json` + `tools/render_claude_settings.py` rendered at every boot (doctor FAILS HARD under 6 hooks) · boot step 4 reads the seat's own pickup + EXPIRING-GRANTS · per-seat `WEEK-INSTRUCTION-TUESDAY.md` · **all nine launchd jobs are tracked templates installed by `scheduler/install_all_jobs.sh`** (the old installer armed 3 of 9) · **and the fourth cause the report missed: the boot pull only runs on a CLEAN tree and a coordinator's tree is never clean, so it was unreachable at every boot and said nothing.** It now fetches and prints the behind-count.
- **Ornith: 20 pins held today** (KS-1011, KS-1081, KS-1031 among them). 78 pins / 54 tickets held for Sunday.
- **Four Kam rulings delivered** into `fleet/briefs_staged/secuura_raise_ornith_ready_diffs.md`: KS-953 `a` (uniform `callee#n`) · KS-692 `a` (narrow now, bind-creator later) · KS-683 `a` (leave it) · KS-910 `a`.

## 🔭 TUESDAY — ONE THING LEFT AND IT IS KAM'S HANDS
**Launch Tuesday once on the mini.** Measured, not assumed: her tree is CLEAN and her HEAD is `08353b963` while the live remote is `77675569d` — **her cached `origin/main` equals her HEAD, so her own "behind by 0" is a false zero.** Because the tree is clean, the new boot pull runs: it fetches, sees the real gap, pulls, and that one launch then renders her hooks, makes her read her pickup, and arms her nine jobs. Four fixes, one launch. ⚠ **I could not find a tile called "fleet activity"** — asked him to point at it rather than write to the wrong place.

## 📋 COMMISSIONING — the shape that works, and it is the week's answer
**Brief-writing is no longer human-shaped.** A subagent given the rules VERBATIM wrote KS-1081 (7/7 first sample) where a coordinator-written brief took four rounds. **The KS-692 prompt is the template — keep its rules list intact, each line is a paid-for round.** Three of five commissions came back as measured REFUSALS (KS-953, KS-683, KS-692-first-pass) and every one was right and produced a card. **A refusal is a complete answer; say so in the prompt.**
**BRIEF RULES** — no CONTEXT lines inside the `## The exact change` fence · every `-` line byte-for-byte and UNIQUE at the tip · no backslash continuations · no `\$`/`\u` in a `+` line · one hunk per function when a line repeats · cells are LITERAL code with pass/fail counters, declarations first · every 🔴 red at the tip BY ASSERTION · one 🟢 control · 🔴 **test body under ~110 lines** (above it the model emits a placeholder comment and the one-line file asserts nothing and exits 0) · 🔴 **carry the completeness arm** (cells-run == `EXPECTED_CELLS`, proven to fire).

## 🔴 THE SYNC AS I LEAVE IT — read this before touching it
- Running in tmux `syncleg`, log `/private/tmp/sync_t9d.out`. **Third attempt.** #1 died instantly (`nohup`, no PTY). #2 ran 28 min walking `qa-worktrees` before Kam ruled them excluded. #3 is this one, with `ignore = Name qa-worktrees*` in force — **verified: 0 worktree paths scanned, against a control showing the scan IS producing paths.**
- **State at 15:1x: unison is `S+` at 0.0% CPU and the log has not grown in three separate 15–20 s checks.** The pane's last line is `!CODING/Datasec/Vision_Sales_Portal/v230-before-pagebottom-light.png`. **Nothing has propagated — 0 `Deleting`, 0 real conflicts (`<-?->`, not the English word).** So nothing is half-done and it is safe to kill and restart.
- ⚠ **Do NOT conclude the drives are dead.** I checked with `timeout 10 ls` and got "NOT responding" for BOTH — **macOS has no `timeout`**, so the COMMAND failed, not the drives. Re-checked without it: both respond, T9 800 GiB free, DevMASTER 1.0 TiB free. That trap is already in this file's list and I walked into it anyway.
- **Owed after it:** the **KK_DEV_Local** leg (Kam 15:05). Case check already done — no clashes, nothing on that drive absent from DevMASTER. Run it the same way: from a tmux session, never `nohup`.

## ⏳ BLOCKED / OPEN
- **Every `systemTest/` ticket** (incl. ruled KS-910): Peter's #997 merged 36 files all under `systemTest/` and `0b25f823f` is not in the local object store. Needs a seat that can fetch.
- **KS-1163** needs one change across a script and TWO suites; `bash_patch` expresses product + ONE test. Not started.
- **The POOL is the week's real risk**, not the machinery. Most of what remains needs a decision, a design, or the stale checkout.

## ⚠ TRAPS
- **`git -C $VAR <write verb>` is REFUSED by the hook** — use the LITERAL path. Sixth consecutive seat.
- **`rm` outside the scratchpad is REFUSED**, including via a variable. Quarantine by `mv` — and that applies to code you WRITE.
- **Never edit `night/*.sh` or a `checker.sh` while a runner is live** — check the lock, write `<file>.new` and `mv`. The Edit tool rewrites in place and is the wrong tool for a live script.
- **`devnas-sync.sh` needs a PTY** (`script -q /dev/null`): launched with `nohup` it dies in under a second and does nothing. Run it from a tmux session.
- **Its log is CARRIAGE-RETURN separated** — 148 KB in six "lines". `tr '\r' '\n'` FIRST, and grep unison's own marker `<-?->` for conflicts, never the English word (the word matches the FILENAMES of old conflict copies).
- **`ignore = Name foo` is an EXACT match** — the QA worktrees are `qa-worktrees-<seat>-<sha>`, so it needed `qa-worktrees*`. My check for it was wrong the same way.
- **`chat_reply.sh` now REFUSES a repeated sentence** (rc 3). `CHAT_ALLOW_REPEAT=1` overrides. **Use `CHAT_DRY=1` to test anything** — arming it sent three junk messages to Kam's panel.
- **`pgrep -fl` on a `bash -c` body prints the whole script.** `ls -1` hides dotfiles. Both produced false readings today.
- **The prior-ruling gate caught me FOUR times today** — Blockfrost, the ownership model, and twice more. **Never `--override-prior-rulings` on the first run.** Read the refusal, open what it names, and put the measurement in the BLUF.
