---
date: 2026-09-16
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's — but Kam STOPPED the Tuesday seat 2026-09-14 07:20 ("until further notice"), and on 2026-09-16 14:00 he commissioned Wednesday to ANALYSE Tuesday's structure and fix it. He added 14:02: "Feel free to read the Datasec content. There is no secrets from you." So Datasec content is readable for THAT task; Datasec client WORK is still not Wednesday's to do.
source: replaced WHOLESALE at 14:10 by the 13:2x seat at its 50% checkpoint. Previous copy beside this file: .pre-1410-wholesale.
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **Kam's standing words today, all receipted:** 06:39 "keep going through the day with the local agent" · 09:53 "If something's blocking, move on to the next. This is especially important for next week" · **13:32 THE ALLOWANCE RAN OUT ~12:00 — he signed in on a DATASEC account; "minimal or limited Secuura work on this account… until Sunday when we'll switch over to my account and we can do more robust action"** · 13:35 "analyzing what's working properly and address anything and fix anything before we go on… continue working with the local LLM on backlog and to-do tickets" · 13:40 storage onto DevMASTER · 14:00 the Tuesday commission (below) · 18:23 (09-15) **he leaves MONDAY NIGHT 2026-09-21** — the unattended loop must be BUILT and PILOTED by Monday morning. Speak in the FIRST person on the panel. A seat may END ITS TURN only with the model RUNNING or a batch QUEUED.

## 🔴 STATE at 14:10
- **Floor:** `%0` Wednesday only — the fleet session died with the allowance ~12:00 and was not rebuilt. Usage gate OPEN (7d **0%**, renews in ~1d 18h on this Datasec sign-in). Origin contains HEAD.
- **Two subagents live** (launched 14:0x, results not yet in): (1) the **Tuesday-vs-Wednesday structural comparison** → writes `1_Project_Definition/Architecture/2026-09-16_tuesday-vs-wednesday-structure.md`; (2) the **KS-1081 brief** → writes `2_Project_Files/local-model/night/briefs/KS-1081.md` (Kam ruled option a: env.example is canonical). Neither builds an input or queues anything — that is the seat's job.
- **ORNITH: idle with an empty queue at 14:10.** Server UP (drive-local, `start_ollama.sh`). The moment KS-1081's brief lands: `build_bash_input.sh` → queue line → `night_run.sh`.
- **A background hash check is still running** on the three largest ollama blobs (61 + 48 + 17 GB, both ends — ~252 GB of reads). Read `/private/tmp/claude-501/.../bmkbf51v2.output` or just re-run `move_ollama_store.sh --verify`. **Until it is clean, do NOT reclaim `~/.ollama`** — and reclaiming it needs Kam's word anyway.

## ✅ WHAT THIS SEAT DID (13:2x → 14:10)
- **Ornith was idle 09:58 → 13:32 and only half of that was the token cap.** The ollama server died before 12:24 (Kam 13:43: a system update — diagnosis closed) and G5 refused six cycles into a log nobody reads. Fixed in the path: `start_ollama.sh` (new) · **G5 self-heals** by calling it · **G8** escalates any gate refusing ≥30 min to Kam's panel, rate-limited, markers moved to `log/_quarantine_g8/`. Arms `tests/g5_selfheal_g8_alert_arms.sh` **6/6** including the control that the same condition refuses under `NIGHT_G5_SELFHEAL=0`.
- **KS-1011 PASS 7/7, held, READY written** (78 READY files now). Kam's option b.
- **Three harness defects fixed:** `build_bash_input.sh` `show(tf)` → `try_show()` (the NEW-test mode had become unreachable; proven by a discriminating PAIR); RETRY-ONCE gained `B3b`/`B3c` (the bash tier had NO retry) and its `&&/||` precedence was grouped so the disable flag disables; `OLLAMA_MODELS` PINNED in night_run.sh.
- **Storage** (see the daily note for the numbers): ollama's 141 GB moved + pointers set on all three surfaces; Docker's move lost his images and he ruled it an acceptable loss.

## 🎯 THE NEXT SEAT'S FIRST ACTS, in order
1. `kam_rulings_today.sh` — read EVERY line before any card or brief.
2. **Feed Ornith.** If `night/briefs/KS-1081.md` exists: build the input, queue it, launch. If not, the next candidates from `night/candidates.md` that are NOT under `systemTest/` — KS-1168 (Kam ruled a, EXACT-only search), KS-1031, KS-953, KS-692. **Do not brief a `systemTest/` ticket** (see BLOCKED).
3. **Read the Tuesday comparison** the moment it lands and take it to Kam with a recommendation, not a summary. This is the highest-value thing on the desk: it is the same problem as his unattended week, and he leaves Monday night.
4. Ask Kam for the one word on reclaiming `~/.ollama` once the hash check is clean.

## ⏳ BLOCKED — stated, not worked around
- **Every `systemTest/` ticket** (KS-998, KS-910, KS-1148, KS-1162 and most of Kam's 09:53 rulings): Peter's #997 merged 36 files, ALL under `systemTest/`, and `0b25f823f` is not in the local object store. `tip_override.txt` is verified only for `Blockchain/Dev`. Briefing one means briefing against a stale copy of exactly the files that moved. Fetching is a Secuura seat's job, and that spends the account Kam wants kept light.
- **KS-1163** needs ONE change across `Start_Up/start-secuura.sh` and TWO suites (`start_secuura_expected_services` + `start_secuura_slot_names`). `bash_patch` expresses product + ONE test file. Part A passes B2/B3/B3b/B4-red/B5-green and stops at B6 (the sibling goes 0→8); Part B's model hunk landed on the `prefix_of` definition at :45. The harness extension is Wednesday's and is NOT started.

## 📋 BRIEF RULES — every one of these cost a model round. Break them and you pay again.
- **Nothing a cell READS lives in prose** — every declaration is the FIRST line of the fenced block.
- **NEVER show a CONTEXT line inside the `## The exact change` fence.** Name context lines in prose above it. Every line in the fence carries `+` or `-` and is a change. (KS-1011 r1.)
- **No backslash continuations in a `+` block** — the model drops them. One long line instead. (KS-1011 r2.)
- **Test cells are LITERAL SHELL, written out in full.** Describe them and the model invents a helper whose assertion is a mutation, and every cell reports FAIL while the product hunk is correct. (KS-1011 r3.)
- Every 🔴 cell fails at the tip BY ASSERTION, never by a throw or an unbound variable. Include one 🟢 CONTROL green at the tip AND after.
- A text pattern ends at ONE unambiguous character, never a quote+space pair. No `\$`/`\u` in a `+` line. One replacement hunk per function when a line repeats.
- Every `-` line must exist byte-for-byte at the tip — copy from `git show`, never retype.

## ⚠ TRAPS
- **`git -C $VAR <write verb>` is REFUSED by the hook** — write the LITERAL path. This has now failed at six consecutive seats; only the hook has ever held.
- **`rm` outside the session scratchpad is REFUSED**, including through a variable. Quarantine by `mv` — and that applies to code you WRITE too: G7 moves its markers, so G8 does as well.
- **NEVER edit `night/*.sh` or a `tasks/*/checker.sh` while a runner is live.** Check the lock (`night/log/.night_run.lock/pid`, `kill -0`), and if live write `<file>.new` and `mv` it over — bash reads a script incrementally and the old inode keeps running. The Edit tool rewrites in place, so it is the WRONG tool for a live script.
- **`sleep N; cmd` is blocked in the tool.** Wait with a background `until` loop (`run_in_background: true`).
- An rc read through a pipe is the LAST command's (`> out; rc=$?`). zsh: `for x in $LIST` and `kill $PIDS` do not word-split.
- **`pgrep -fl` on a `bash -c` body prints the WHOLE script** — thousands of lines into your context. Use `pgrep -f <pat> | while read p; do ps -o pid,ppid,lstart -p $p; done`.
- **`ls -1` does not show dotfiles.** A quarantine dir of `.marker.<ts>` files reads as empty — that is a false absence from your own instrument.
- The statusline was readable at boot (ctx:33% at 13:31) and `tmux capture-pane` has not found it since. If you cannot read it, say "unread", never guess a number.
- `note_entry.sh --stdin` with a quoted heredoc; any clock in a row, brief or panel line is `$(date +%H:%M)` substituted by the shell, never typed.

## 🔭 THE BIG ONE — Kam's 14:00 commission, verbatim in the daily note
Tuesday works poorly (not responding, not following instructions, not coordinating agents) and Kam wants her brought up to "almost like you", autonomously if that is what it takes — plus whatever else is needed so that **an ongoing task given once LIVES ON and is performed properly** while he is away. The comparison agent's report is the input; the deliverable is a recommendation split into INSTRUCTION / SKILL / CODE with what must land before **Monday 2026-09-21**.
