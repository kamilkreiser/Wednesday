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
1. `kam_rulings_today.sh` — every line — then `reconcile_rulings.py`, before any card or brief.
2. **Read the model's state before anything else.** `night/queue.md` pending count · the ornith-loop
   launchd job · `uptime` load against the gate of 14. If the queue is empty AND the load is under the
   gate, the first work of the session is a brief.
3. **KS-998 is BUILT AND QUEUED** (`inputs/bash_998.json`). The ornith-loop job takes it when the load
   falls under 14. Read its verdict, source-read the diff, write the READY.
4. **The KK_DEV_Local sync leg is CHAINED** behind the T9 leg by `fleet/chain_ssd_leg.sh` (log
   `/private/tmp/chain_ssd_leg.out`). It is ADDITIVE BY CONSTRUCTION — `-nodeletion` on both roots,
   because `ssd-ssd.prf` ships `confirmbigdel = false` — and it REFUSES to chain if the T9 leg reported
   any deletion. Do not re-run it by hand without reading that log first.
5. Feed Ornith. If nothing is briefable, commission one (see COMMISSIONING).

## ✅ WHAT LANDED THIS SEAT (15:1x → 15:5x)
- **KS-692 HELD, 7/7** — the 15:13 A4 FAIL was the BRIEF, not the model (no 🔴 in the cell titles and no
  `## Red cells` section, so three assertion-reds were classified as controls). Declared, input rebuilt,
  the SAME `out.md` re-checked → PASS. **No second model round spent.** READY written after a source read
  of the applied hunk; Kam's ruling is quoted IN the source comment and its two ticket-state claims
  (KS-586 Done, KS-1116 Backlog) were verified at source.
- **TWO GATES BUILT, both red-proofed on real briefs, both with OVER-FIRE CONTROLS:**
  `build_input.sh` **UNDECLARED-RED GATE** (arms `local-model/tests/undeclared_red_gate_arms.sh` 6/6;
  measured 29 of 30 vitest briefs unaffected) · `build_bash_input.sh` **CONTEXT-AS-ADDITION GATE**
  (arms `local-model/tests/context_as_addition_gate_arms.sh` 5/5) — a `+` line byte-identical to a `-`
  line in the same hunk is CONTEXT, and claiming it as an addition makes B3b/A3c refuse a CORRECT output.
  **w=3 that day: KS-1089, KS-1168 ×2, KS-998 — the last written by this seat's own hand minutes after
  filing the rule against it.**
- **KS-998 was never blocked.** The previous pickup's "every `systemTest/` ticket needs a seat that can
  fetch" was a TIER verdict. Tested: the GitHub compare over Peter's #997 lists 36 files and **neither of
  KS-998's two is among them**. Brief rewritten as a minimal hunk (1 `-`, 8 `+`, 6 context) and queued.
- **KS-1168 briefed by a subagent, ran twice, genuinely failed A3c** — the second run under good load is
  what proved it was the brief and not the machine. See the CONTEXT-AS-ADDITION rule above.
- **KS-1173 NOT briefed, correctly** — a subagent measured that it already exists as `READY_KS-1172-B3`
  ("KS-1172 + KS-1173 PART B") and refused. It also found **2 of 81 READY diffs carry a file header
  buried inside the previous hunk**, so `patch(1)` rejects them as malformed — recorded in
  `fleet/briefs_staged/secuura_raise_ornith_ready_diffs.md` where the Sunday seat lands.
- **Spotlight, not unison, is what pins the machine** — measured ~270% combined CPU against unison's 99%
  of one core. Kam's 09-14 exclusion covered `!CODING`; the drives a SYNC WRITES were never in scope.
  Carded `wed-spotlight-indexes-the-sync-target-drives`, default HOLD.
- **`night/retry_when_load_allows.sh`** — the RETRY-ONCE leg is starved when the checker's own load spike
  trips the gate. It waits, bounded, and reports either way. ⚠ Its first live fire lost a 4-second
  check-then-act race with the runner (cost nothing — ollama serialises same-model calls); fixed by
  `.new` + `mv` to a bounded WAIT.

## 🔭 TUESDAY — ONE LAUNCH BY KAM, AND A SECOND THING ON THAT MACHINE MAY ALSO BE OPEN
**CARDED at 15:5x: `tuesday-one-launch-on-the-mini`** (action-first, default HOLD). Her tree is CLEAN,
HEAD `08353b963` vs live remote `77675569d`, and her cached `origin/main` equals her HEAD — a FALSE
ZERO, so she cannot see the gap; a clean tree means the new boot pull runs and closes it, applying all
four repairs in one launch.
⚠ **TWO CORRECTIONS TO THE PREVIOUS PICKUP, both measured this seat:**
1. **The "fleet activity" tile EXISTS** — `dashboard/cockpit.html:264-268`, heading `Fleet activity`.
   The previous pickup said it could not be found; that was a FALSE ABSENCE from its own search, and it
   left Kam's 15:06 instruction unexecuted for two hours. **But it is not a noticeboard:** it renders
   AGENT MAIL SUBJECTS (`cockpit.html:820`, `[A -> B] rest`), so nothing can be "put on" it except
   agent-to-agent mail. `send_brief.sh` correctly REFUSED `Datasec/Tuesday` — no such inbox in
   `fleet/inbox_routing.conf`. Opening one would reverse Kam's 09-14 "do not message Tuesday" and is
   his call; it is option `channel` on the card.
2. **Kam RULED `grant` on `tuesday-mac-mini-scheduler-full-disk-access` (2026-09-11 15:25) and the card
   carries NO delivery mark.** That is a fact about our paperwork, NOT about his machine. **UNKNOWN from
   this seat, and the instrument that closes it is on the MINI** (`launchctl list`; `~/Library/Logs/
   tuesday_*.err` showing exit 126). If it was never granted, the launch fixes her CODE and her
   scheduled rituals still will not fire. Do not assert either way.

## 📋 COMMISSIONING — the shape that works, and it is the week's answer
**Brief-writing is no longer human-shaped.** A subagent given the rules VERBATIM wrote KS-1081 (7/7 first sample) where a coordinator-written brief took four rounds. **The KS-692 prompt is the template — keep its rules list intact, each line is a paid-for round.** Three of five commissions came back as measured REFUSALS (KS-953, KS-683, KS-692-first-pass) and every one was right and produced a card. **A refusal is a complete answer; say so in the prompt.**
**BRIEF RULES** — 🔴 **a vitest brief DECLARES its reds**: either 🔴 in every red cell's `it(` title, or a `## Red cells` section with one `- ` line per title. A4 recognises no third way, and with both empty it reads every genuine assertion-red as a CONTROL red and refuses a CORRECT output (KS-692, 15:13 today — cost one round). `build_input.sh` now REFUSES that shape (`ALLOW_UNDECLARED_REDS=1` overrides; arms `local-model/tests/undeclared_red_gate_arms.sh` 6/6 incl. an over-fire control) · no CONTEXT lines inside the `## The exact change` fence · every `-` line byte-for-byte and UNIQUE at the tip · no backslash continuations · no `\$`/`\u` in a `+` line · one hunk per function when a line repeats · 🔴 **NEVER disambiguate two identical blocks by removing and RE-ADDING unchanged lines as an anchor** — a `+` line is a claim that the line is not at the tip, the model rightly emits the honest minimal hunk, and A3c then refuses a correct output (KS-1168 ×2 today, 15/46 then 18/46 absent; KS-1089 this morning is the same collision, w=2). Use unprefixed CONTEXT lines, or split on genuinely unique nearby text, or take one site per round · cells are LITERAL code with pass/fail counters, declarations first · every 🔴 red at the tip BY ASSERTION · one 🟢 control · 🔴 **test body under ~110 lines** (above it the model emits a placeholder comment and the one-line file asserts nothing and exits 0) · 🔴 **carry the completeness arm** (cells-run == `EXPECTED_CELLS`, proven to fire).

## 🔴 THE SYNC AS I LEAVE IT — read this before touching it
- Running in tmux `syncleg`, log `/private/tmp/sync_t9d.out`. **Third attempt.** #1 died instantly (`nohup`, no PTY). #2 ran 28 min walking `qa-worktrees` before Kam ruled them excluded. #3 is this one, with `ignore = Name qa-worktrees*` in force — **verified: 0 worktree paths scanned, against a control showing the scan IS producing paths.**
- ⚠ **CORRECTED 15:2x — THE SYNC IS ALIVE AND WORKING. Do NOT kill it.** The previous line read `S+` at
  0.0% CPU from a SNAPSHOT and concluded it was stalled. A DELTA settles it and a snapshot cannot: two
  `ps -o time=` reads 10 s apart showed 11.9 s of CPU burned, i.e. ~99% of one core, and it has since
  passed 43 minutes of CPU. **The log is quiet because unison buffers during reconciliation, not because
  it is stuck.** Still 0 `Deleting` and 0 real conflicts (`<-?->`, never the English word — that matches
  old conflict-copy FILENAMES).
- **The real load source is NOT unison.** `ps -Ao pcpu,pid,comm -r` at 15:37: Spotlight at ~270% combined
  (mds_stores 132, spotlightknowledged 53, mds 47, knowledgeconstructiond 22, mdworker_shared 19) against
  unison's 99% of one core. That is what holds the 1-min load over the model's gate of 14. Carded:
  `wed-spotlight-indexes-the-sync-target-drives`.
- ⚠ **Do NOT conclude the drives are dead.** I checked with `timeout 10 ls` and got "NOT responding" for BOTH — **macOS has no `timeout`**, so the COMMAND failed, not the drives. Re-checked without it: both respond, T9 800 GiB free, DevMASTER 1.0 TiB free. That trap is already in this file's list and I walked into it anyway.
- **The KK_DEV_Local leg (Kam 15:05) is CHAINED, not owed** — `fleet/chain_ssd_leg.sh` waits on the T9
  pid, reads that leg's log for deletions/conflicts, and **REFUSES to chain if the T9 leg deleted
  anything** (that is Kam's call, not a seat's). It runs `unison ssd-ssd` with `-nodeletion` on BOTH
  roots — **because `~/.unison/ssd-ssd.prf` ships `confirmbigdel = false`**, unlike `devnas.prf` which has
  it true — and with `-ignore 'Name qa-worktrees*'`, Kam's own 15:00 ruling applied to the second leg.
  The profile itself is NOT edited; both guards are command-line only. Log: `/private/tmp/chain_ssd_leg.out`.

## ⏳ BLOCKED / OPEN
- ⚠ **CORRECTED 15:3x — "every `systemTest/` ticket is blocked" was a TIER VERDICT and it is WRONG.**
  The stale object store is real, but it only blocks a ticket whose FILES actually moved. Measured via
  the GitHub compare API (`48e65c435...0b25f823f`, repo `Secuura/Distributed_Secuura`): 36 files, and
  **neither of KS-998's two is among them** — so its `-` lines are byte-identical at the real tip and it
  was never blocked. **Run that compare per ticket before inheriting this.** (Also corrected: the G6
  override note says the 36 are "all-under-systemTest/"; one is not — `Projects Documents/…html`. Its
  operative claim, nothing under `Blockchain/Dev`, still holds.)
- **KS-910 and the other `systemTest/` tickets: UNMEASURED, not blocked.** Run the same compare.
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
