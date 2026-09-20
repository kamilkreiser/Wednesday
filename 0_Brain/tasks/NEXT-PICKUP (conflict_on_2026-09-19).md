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
3. ⚠ **KS-998 is NOT queued any more — it was REALLOCATED to Claude under Kam's counter** (2 rounds).
   Do not re-queue it at the local model. Same for KS-1168 and KS-1163. They are batch work for a
   Secuura seat or the Sunday pass; their specs are complete and their `done.md` rows say so.
4. **The KK_DEV_Local sync leg is CHAINED** behind the T9 leg by `fleet/chain_ssd_leg.sh` (log
   `/private/tmp/chain_ssd_leg.out`). It is ADDITIVE BY CONSTRUCTION — `-nodeletion` on both roots,
   because `ssd-ssd.prf` ships `confirmbigdel = false` — and it REFUSES to chain if the T9 leg reported
   any deletion. Do not re-run it by hand without reading that log first.
5. Feed Ornith. If nothing is briefable, commission one (see COMMISSIONING).

## ✅ WHAT LANDED THIS SEAT (15:1x → 18:0x)
- 🔴 **KAM'S NEW STANDING RULE, and it is a COUNTER — learn it before you brief anything.**
  Email 07:45Z: the local model is PERMANENT, Wednesday routes, and *"If local fails, the task is
  allocated to a Claude agent. Not urgently but when it makes sense."* Then 07:57Z, when asked:
  *"Rebriefing once is ok and might generate positive results. Doing it more would be a waste with
  diminishing results."* → **original brief + ONE rebrief, then Claude. No third round, whatever the
  diagnosis says.** Filed `learnings/2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do.md`.
  🔑 He replaced Wednesday's judgement call (brief-defect vs model-limit) with a counter —
  **where a countable rule and a judgement rule agree, prefer the countable one.**
- **REALLOCATED to Claude under that counter (recorded on their `done.md` rows, spec carries over —
  batch them, do not open a seat per ticket):** **KS-1168** (Kam-ruled; round 3 the model emitted a
  literal `\n` inside a CONTEXT line and corrupted the patch) · **KS-1163** (4 rounds, all pre-rule;
  needs one change across a script AND two suites, which `bash_patch` cannot express) · **KS-998**
  (Kam-ruled; 2 rounds = the counter's limit).
- **KS-692 HELD 7/7** — the 15:13 FAIL was the brief, not the model. Re-checked the SAME output, no
  second round spent. READY written after a source read; Kam's ruling is quoted IN the source comment.
- **THREE GATES BUILT, all red-proofed with OVER-FIRE CONTROLS:** `build_input.sh` UNDECLARED-RED GATE
  (arms 6/6) · CONTEXT-AS-ADDITION on **both** builders (`tests/context_as_addition_gate_arms.sh` 5/5
  bash, `..._vitest_arms.sh` 6/6) — **it was bash-only at first, and that hole cost KS-1168 two rounds;
  one arm now asserts the gate exists on BOTH.**
- 🔴 **AN ARM'S RED FIXTURE MUST BE SOMETHING NOBODY IS TRYING TO FIX.** ARM 1 pointed at the live
  KS-1168 brief; the repair landed, the brief stopped being defective, and the arm went red — which looks
  exactly like the gate breaking. Fixture FROZEN at `tests/fixtures/briefs/KS-1168.md` (reached via
  `NIGHT_BRIEFS_DIR`); ARM 0 now proves the fixture IS defective before ARM 1 claims anything, and ARM 3
  is a DISCRIMINATING PAIR (frozen vs live repaired, opposite verdicts).
- **Kam's dashboard change is BUILT and he RATIFIED THE SCOPE** (07:41Z "the scope looks good"): the right
  panel is split, `#needscroll` pinned `flex:none` max-height 46%, so what needs him cannot scroll away.
  ⚠ **NOT visually verified — the Chrome extension is not connected.** Anything beyond that shape (a third
  column, removing ruled rows) is NOT covered by his ratification.
- **Spotlight, not unison, pins the machine** (~270% CPU vs unison's one core). His 09-14 exclusion covered
  `!CODING`; the drives a SYNC WRITES were never in scope. Carded, default HOLD.

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
- **The POOL is the week's real risk**, not the machinery. Three of four commissions this afternoon came
  back as CORRECT refusals (KS-1173 already a passing READY · KS-1125 already fixed at the tip with no
  copyable `pg`-mock shape · plus KS-953/KS-683 earlier). Every refusal was right and each saved a round.
- 🟢 **BUT THE POOL IS WIDER THAN THE QUEUE HEADER CLAIMS.** That header says coverage-only tickets
  "cannot pass RED-FIRST" — **true when written, false now.** `build_input.sh` grew a `## Tamper` block on
  2026-09-15 (test-only mode: A3 test file only, A4 red UNDER THE TAMPER, A5 green at the tip) and **19
  held READYs already use it.** The header is corrected in place. Coverage-only tickets — which the
  backlog is dominated by — ARE briefable on the vitest tier. Exemplars: `night/briefs/KS-1120.md`,
  `KS-1123.md`, `KS-1118.md`. **This is the widening Kam asked for on 09-15 18:19, and it was already
  built; nobody had pointed the candidate list at it.**
- ⚠ **Trap on `api-gateway/src/startup-migrations.ts`, measured 2026-09-16 so nobody re-derives it:**
  `migrateDatabase` is NOT exported, and `runStartupMigrations` uses a bare CJS `require('pg')` which
  `vi.mock('pg', …)` does NOT intercept (that works elsewhere only because `src/db.ts` uses a static ESM
  import). No suite currently mocks that path. Pick a target reachable from an exported symbol.

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
