---
date: 2026-09-16
type: architecture / structural comparison
source: Kam, 2026-09-16 14:00 verbatim — "I don't understand why you work really well, and Tuesday seems to be working very poorly… look at both your structure and Tuesday's structure and see what can be improved so that we have a more autonomous, more independent operational model… make sure that if an ongoing task is provided to Tuesday it lives on and is performed properly."
scope: read-only measurement of /Volumes/DevMASTER/WEDNESDAY vs /Volumes/KK_T9_External_HDD/TUESDAY. No file in either tree was modified except this one.
author: Wednesday (Studio seat, Kamils-Mac-Studio.local), 2026-09-16
deadline that makes this urgent: Kam leaves Monday NIGHT 2026-09-21
---

# Tuesday vs Wednesday — why one seat works and the other does not

## BLUF

**The leading hypothesis is wrong, and that is the finding.** The two trees are not
two diverged copies of the framework: every hook (14/14), every tool (51/51), every
scheduler script (12/12) and every skill (9/9) is **byte-identical** in both, the
launcher differs by **two hunks / twelve lines**, and Tuesday's checkout is a clean
ancestor of Wednesday's HEAD (382 commits behind, same remote). What actually differs
is the layer that **never travels in git**: Tuesday's
`.claude/settings.local.json` is **169 bytes against Wednesday's 1,775** — it wires a
statusline and **nothing else**, so Tuesday runs with **zero of Wednesday's six Claude
Code hooks** (including the PreCompact block that refuses auto-compaction) and **zero
permission guards**; that file is gitignored (`.gitignore:8`), is **not mentioned once
in `PORTABILITY.md`**, and is **not checked once by `doctor.sh`**.

**Second finding, equally mechanical:** the boot prompt's Tuesday paragraph
(`Launch_Wednesday.command:400-406`) orders her to read two files that were moved into
`0_Brain/tasks/_superseded_2026-09-09/` on 2026-09-09, and it names
`NEXT-PICKUP-TUESDAY.md` **only as something to write at wrap, never to read at boot**.
No boot step in the launcher names a pickup file for *either* seat — Wednesday reads
hers purely by habit (measurable in her daily notes; absent from Tuesday's). An ongoing
task therefore survives a rotation on Wednesday's seat because of a *custom*, and dies
on Tuesday's because nothing carries it.

**Third:** of the **nine** `launchd` jobs that keep Wednesday alive on this Mac,
**six have no on-drive plist at all** and none exist as `com.tuesday.*`. Tuesday's tree
has **never written `fleet/state/chat_sync.log`** — the 60-second job that puts her
replies on Kam's one page has never run there. A naive "copy Wednesday's files to
Tuesday" fixes none of these three things.

---

## Recommendation

Ordered by value per unit of risk. **MUST = land before Monday 2026-09-21.**

| # | Change | Class | Effort | Monday? |
|---|---|---|---|---|
| **R1** | **Make the hook/permission config travel.** Add a *tracked* `.claude/settings.template.json`; have `Launch_Wednesday.command` render `.claude/settings.local.json` from it at each boot (substituting `$PROJECT_DIR` and the seat name), and add a `doctor.sh` leg that **fails** if the live file is missing any of the six hooks. This one change restores to Tuesday: the PreCompact block, the post-compact re-ground, and the four PreToolUse guards. | **CODE** | ~1 h | **MUST** |
| **R2** | **Fix the Tuesday scope paragraph** (`Launch_Wednesday.command:400-406`). It orders a read of `FIRST-BOOT-TUESDAY.md` and `NEXT-PICKUP-DATASEC-LAPTOP.md`, both superseded 2026-09-09. Replace with `NEXT-PICKUP-TUESDAY.md`. | **INSTRUCTION** | 10 min | **MUST** |
| **R3** | **Add the pickup read as a numbered boot step for BOTH seats** (between steps 4 and 5): read the seat's own pickup + `EXPIRING-GRANTS.md` WHOLE, and treat its owed actions as the first work. Today this is habit on one seat and nothing on the other. | **INSTRUCTION** | 15 min | **MUST** |
| **R4** | **Arm the launchd set on Tuesday's Mac** — `WED_AGENT=tuesday bash 2_Project_Files/scheduler/install_scheduler.command` (shiftchange/wake/close/nassync; dailysweep correctly skipped), plus `com.tuesday.chatsync` per PORTABILITY 22, plus `install_night.command`/`install_receipt.command` if Ornith is wanted there. **And add chatsync to the installer** so it stops being hand-work. Without chatsync Tuesday is invisible on Kam's page. | **CODE** (+ 30 min at the mini) | ~50 min | **MUST** |
| **R5** | **Seat-scope `WEEK-INSTRUCTION.md`.** There is one file and boot step 4 reads `${BRAIN_DIR}/tasks/WEEK-INSTRUCTION.md` for *both* seats — Kam's Secuura-week words would become Tuesday's Datasec standing order. Give it a `-TUESDAY` twin, or a per-seat `## Scope` section the boot reads by seat. | **INSTRUCTION** | 20 min | **MUST** (if Tuesday is to run the week) |
| **R6** | **Pull Tuesday's tree forward** (382 commits) and re-run `doctor.sh` there — *after* R1–R3/R5 are committed, so she gets them in the same pull. Brings the 09-15 stuck-tap read-back, the rotate-refusal tap, `WEEK-INSTRUCTION.md`, the unattended-week design, `derive_candidates.py`, `daily_receipt.sh` and the four newest lessons. | **CODE** | 10 min | **MUST** |
| **R7** | **Structured OWED ACTIONS in the pickup.** `learnings/2026-09-14_kams-instruction-stands-until-he-withdraws-it.md` documents Kam's instruction being inverted into a do-nothing default and copied faithfully across two rotations. The lesson exists; nothing enforces it. Give the pickup a `## OWED (Kam)` table — verbatim words · safe form · state (OWED / DONE / WITHDRAWN-BY-KAM-`<ts>`) — and a doctor warning when a row has been OWED > 24 h. | **INSTRUCTION + CODE** | ~1.5 h | should |
| **R8** | **doctor.sh refuses silence.** Legs for: the six hooks present; `chat_sync.log` mtime < 5 min; the seat's pickup exists and is < 24 h old. Today doctor checks `launchctl` 14 times and the hook config **zero** times. | **CODE** | ~1 h | should |
| **R9** | **Finish the unattended-week pieces its own design marks as owed** (`Architecture/2026-09-16_unattended-week-loop.md`): (b) re-derive candidates every 6 h from the loop job; (e) the receipt counts **distinct READY pins** and names holds / "queue dry since HH:MM" / "coordinator dead since HH:MM". (d)'s G7/G8 are already in Wednesday's `night_run.sh`. | **CODE** | ~3 h | (b)+(e) MUST |
| **R10** | **Per-seat daily notes.** Boot step 5 (`:469`) sends both seats to one `0_Brain/daily/`; there is exactly one such directory. 2026-09-13's note is 280 lines with **49 "Secuura" mentions and 4 "Datasec"** — a Tuesday boot's mandated episodic read is overwhelmingly another client's work. Split to `0_Brain/daily/<seat>/`. | **INSTRUCTION** (+ a file move) | 45 min | nice-to-have |

**If only three things land: R1, R2+R3, R4.** They are the three layers that do not
travel — config, instruction, and machine — and each is independently sufficient to
keep Tuesday broken.

---

## Detail

### 1. Divergence — measured

#### 1a. The launchers

| file | WEDNESDAY tree | TUESDAY tree | verdict |
|---|---|---|---|
| `Launch_Tuesday.command` | 2,063 B | 2,063 B | **byte-identical** (`diff` clean). 20 lines: it sets `WED_AGENT=tuesday` and `exec`s the shared launcher. There is deliberately only ONE launcher. |
| `Launch_Wednesday.command` (the shared one) | md5 `0de03454…`, 42,638 B | md5 `7cdd4f74…`, 41,717 B | Tuesday's copy **is** Wednesday's `.pre-0916-rotateread` backup, byte for byte. |

The whole boot-prompt divergence is **two hunks, twelve added lines**:

1. `:463-468` — boot step 4 now also reads `0_Brain/tasks/WEEK-INSTRUCTION.md` and acts
   on it when `status: live` and `valid_until` has not passed.
2. `:578-585` — after `wednesday_rotate.sh --self`, sleep ~8 s and **read the last line
   of `rotate_wednesday.log`**; `REFUSED` means the seat is still here. (Added because
   on 2026-09-16 a 01:11 refusal went unread and a seat sat **4 h 19 min** idle.)

That is the entire launcher gap. **The boot prompt is not why Tuesday behaves badly.**

#### 1b. Git

Same remote (`git@github.com:kamilkreiser/Wednesday.git`). Tuesday HEAD `08353b963`
(2026-09-15 09:05) is an **ancestor** of Wednesday HEAD `fe8e8e205` (2026-09-16 14:00);
`rev-list --count` = **382 commits behind**; Tuesday's working tree is **clean**
(0 porcelain lines).

#### 1c. Live scripts, content-diffed (excluding `.pre-*` backups)

| directory | files | missing in TUE | content differs |
|---|---|---|---|
| `2_Project_Files/fleet/hooks/` | 14 / 14 | **0** | **0** |
| `2_Project_Files/tools/` | 51 / 51 | **0** | **0** |
| `2_Project_Files/scheduler/` | 12 / 12 | **0** | **0** |
| `0_Brain/skills/` | 9 / 9 | **0** | **0** |
| `2_Project_Files/fleet/usage_gate.sh` | 3,677 B | — | **identical** |
| `2_Project_Files/fleet/cockpit/` | 43 / 40 (the 3 extra are `.pre-*` backups) | **0** | **3**: `wake_ack.sh` (3 lines), `wake_watch.sh` (5), `wednesday_rotate.sh` (54) |
| `2_Project_Files/local-model/night/` | — | **5 scripts**: `derive_candidates.py`, `daily_receipt.sh`, `new_brief.sh`, `install_receipt.command`, `candidates.md` | `build_input.sh`, `night_run.sh`, `queue.md`, `done.md` |
| `2_Project_Files/attention/`, `coordination/` | — | 0 | 0 |

#### 1d. Brain

| | WEDNESDAY | TUESDAY |
|---|---|---|
| lesson files (`0_Brain/learnings/2*.md`, no `.pre-*`) | **172** | **168** |
| the 4 WED-only | `2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry.md` · `2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix.md` · `2026-09-15_ornith-q4-only-volume-week-qa-sunday-merge-once.md` · `2026-09-16_if-something-blocks-move-on-to-the-next.md` | — |
| Tuesday's own ledger `_ledger_laptop_datasec.md` | 51,219 B | **51,219 B — identical** |
| `0_Brain/tasks/` | +`WEEK-INSTRUCTION.md` | everything else present, incl. `NEXT-PICKUP-TUESDAY.md` (29,947 B) |
| `1_Project_Definition/Architecture/` | +`2026-09-16_unattended-week-loop.md` | 17 of 18 |

**Nothing structural is missing from Tuesday's brain.** She carries the same 168
lessons, the same nine skills, her own 51 KB ledger, and her own 30 KB pickup.

#### 1e. The divergence that matters — untracked files

`.gitignore:8` ignores `.claude/settings.local.json`. `git ls-files .claude/` in **both**
trees returns four files, and the live config is not among them.

| | WEDNESDAY (1,775 B) | TUESDAY (169 B) |
|---|---|---|
| statusline | yes | yes |
| `PreCompact` → `precompact_block.sh` | **yes** | **NO** |
| `SessionStart[compact]` → `session_start_compact.sh` | **yes** | **NO** |
| `PreToolUse` → `pretooluse_no_cd.sh` | **yes** | **NO** |
| `PreToolUse` → `pretooluse_seat_scoped_chat.sh` | **yes** | **NO** |
| `PreToolUse` → `pretooluse_grep_case.sh` | **yes** | **NO** |
| `PreToolUse` → `pretooluse_no_rm.sh` | **yes** | **NO** |
| `permissions.ask` (6 patterns: `!CODING/**`, vault, force-push) | **yes** | **NO** |

A **decoy** makes this hard to see: `.claude/settings.local.json.pre-0914-grepcase`
(1,455 B) **is tracked**, so it rides into Tuesday's tree — but it is *Wednesday's*
backup: it names `/Volumes/DevMASTER/WEDNESDAY/…` and `'[Wednesday]'`. A file listing
of Tuesday's `.claude/` looks like she has the hooks. She does not.

And nothing would tell anyone:
- `PORTABILITY.md`: **0** matches for `settings.local` or `hooks` in the Claude-config
  sense (positive control from the same file: "Tuesday" appears **21** times).
- `doctor.sh`: **0** matches for `settings.local` / `pretooluse` / `precompact`
  (positive control from the same file: `launchctl` appears **14** times).

---

### 2. Per-symptom mechanism check

#### Symptom 1 — "not responding to questions"

**On the panel she did respond.** Seat-scoped measurement on the `view` field over
2026-09-09 → 2026-09-14 02:10 (the window both seats were live), "next reply after each
of Kam's messages":

| | Kam msgs | ≤5 min | ≤15 min | ≤60 min | never | median |
|---|---|---|---|---|---|---|
| **TUESDAY** (`view="tuesday"`) | 60 | 47 | 52 | **60** | **0** | **2.4 min** |
| **WEDNESDAY** (`view="wednesday"`) | 133 | 121 | 130 | 133 | 0 | 1.1 min |

Kam has sent **zero** messages to the Tuesday tab since her last reply
(2026-09-14T02:06), so the silence since then is his stop, not her.

**Where she genuinely did not respond is the terminal.** The tail of
`TUESDAY/2_Project_Files/fleet/cockpit/logs/wake_watch_runner.log`:

```
2026-09-14 02:33:31 WAKE: pane 'wednesday' (%0) shows BUSY indicators but content FROZEN ~6 min …
2026-09-14 02:33:31 tapped wednesday pane %0
2026-09-14 02:49:40 … FROZEN ~6 min …   2026-09-14 02:57:46 … FROZEN ~6 min …
2026-09-14 03:05:52 … FROZEN ~6 min …
```

Taps landing on a pane that produced nothing, four times in 33 minutes, while her chat
stream ended at 02:06. `FROZEN` appears **191** times in her log against **150** in
Wednesday's.

**The mechanism Wednesday has and Tuesday does not:** the **tap read-back / stuck-tap
recovery** in `wake_ack.sh` + `arm_wake_watch.sh`, which lands text at the pane, reads
it back, and re-submits if it is still sitting at the prompt. Wednesday's log carries
**45** read-back lines — **32 on 2026-09-15 and 13 on 2026-09-16**, i.e. it shipped the
day *after* Kam stopped Tuesday. Tuesday's log: **0**. This is a CODE gap she could not
have had, and it is in the 382 commits she is behind.

**Compounding it:** `com.tuesday.chatsync` has never run. `fleet/state/chat_sync.log`
is 912,765 B in Wednesday's tree (mtime 2026-09-16 14:09) and **does not exist** in
Tuesday's, whose entire `fleet/state/` holds one file. `fleet/state/` is gitignored
(`.gitignore:43`), so this is genuine local evidence. Without that 60-second job, a
reply Tuesday writes reaches Kam's one page only when a Wednesday seat happens to pull.

#### Symptom 2 — "not following instructions"

Three mechanisms, all present for Wednesday, all absent for Tuesday.

1. **The four PreToolUse guards.** They are not advice; they are refusals. This very
   session was refused twice (`pretooluse_no_cd.sh` on a `cd`, `pretooluse_seat_scoped_chat.sh`
   on a chat read that did not mention `view`) and advised three times by
   `pretooluse_grep_case.sh`. Wednesday's 2026-09-13 handover block lists them under
   "TRAPS MET THIS SEAT". Tuesday's config wires **none** of them, so every rule they
   carry is memory-only for her.
2. **The PreCompact block.** `fleet/hooks/precompact_block.sh` exits 2 to *refuse*
   auto-compaction — "compaction is a failure mode, not a feature" (working-rhythm §4);
   `session_start_compact.sh` re-grounds a session that came back from one anyway.
   Tuesday has neither. Her long sessions compact into summaries-of-summaries with no
   re-ground, which is the mechanical form of a seat that starts well and drifts.
3. **Instruction inversion across a rotation.**
   `0_Brain/learnings/2026-09-14_kams-instruction-stands-until-he-withdraws-it.md`
   (present in **both** trees) records the measured case: Kam's 2026-09-13 20:45
   *"Send me the email with the content"* became *"unanswered question; default: no
   harness email unless he asks"* in s13's pickup, and s14 copied it faithfully — the
   agreement was lost across two rotations without anyone deciding to drop it. The
   lesson exists. **No mechanism enforces it.** (→ R7)

**Plus a context tax nobody chose.** The launcher promises Tuesday "your own … daily
notes" (`:396`) but boot step 5 (`:469`) sends both seats to the same
`${BRAIN_DIR}/daily/`, and there is exactly one such directory. `2026-09-13.md` is 280
lines: **49** "Secuura" mentions, **4** "Datasec". Tuesday's mandated episodic read is
another client's day. (→ R10)

#### Symptom 3 — "not coordinating agents"

Measured from each watcher's own `armed: … agents=N` census line, 2026-09-10 → 09-14:

| | samples | agents = 0 | agents ≥ 3 |
|---|---|---|---|
| **WEDNESDAY** | 682 | 59 (**8.7 %**) | 295 (**43.3 %**) |
| **TUESDAY** | 482 | 133 (**27.6 %**) | 37 (**7.7 %**) |

Tuesday ran an **empty floor three times as often** and a full floor **five times less
often**. But nothing structural forbids her from coordinating: `launchers.conf` carries
seven Datasec/Secuura entries, `cockpit.sh` and `seat_resolve.sh` are identical in both
trees, and her own history entry of 2026-09-14 06:52 names S45/S46 gate lanes she ran.
The gap is **drive**, not capability — and the drive is exactly what the four WED-only
lessons carry, headed by
`2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry.md`.

#### Symptom 4 — the ongoing task dying — see §3

---

### 3. The ongoing-task problem

#### 3a. What keeps work alive in Wednesday's tree **today**

*Nine* `launchd` jobs, verified live on this Mac with `launchctl list`:

| label | fires | runs |
|---|---|---|
| `com.wednesday.shiftchange` | 05:30 | `scheduler/shift_change.sh` |
| `com.wednesday.wake` | 06:00 | `scheduler/wake_wednesday.sh` |
| `com.wednesday.ornith-receipt` | 06:45 | `local-model/night/daily_receipt.sh --post` → the panel |
| `com.wednesday.dailysweep` | 15:00 | `scheduler/daily_sweep.sh` |
| `com.wednesday.close` | 23:00 | `scheduler/close_wednesday.sh` |
| `com.wednesday.ornith-night` | 23:30 | `local-model/night/night_run.sh` |
| `com.wednesday.nassync` | 03:30 | `scheduler/nas_sync.sh` |
| `com.wednesday.ornith-loop` | **every 900 s** | `night/night_run.sh` (consumes `night/queue.md`, gates G1–G8) |
| `com.wednesday.chatsync` | **every 60 s** | `tools/chat_sync.sh` |

Plus, on-drive: `night/derive_candidates.py` → `night/candidates.md` (the queue's
*source*, re-derived); `night/new_brief.sh`; `fleet/cockpit/wake_watch.sh` +
`arm_wake_watch.sh` + `wake_ack.sh` (tap, read back, re-submit);
`wednesday_rotate.sh --self|--dead` + `rotate_liveness.sh` + `dead_banner_check.sh`;
`0_Brain/tasks/WEEK-INSTRUCTION.md` + its boot-step-4 read + its `doctor.sh` expiry
warning; and the design itself,
`1_Project_Definition/Architecture/2026-09-16_unattended-week-loop.md`.

That design's own table already names what is **owed**: (b) re-derive candidates at
every boot *and every 6 h from the loop job*; (d) a liveness line when the queue has
been empty > 2 h; (e) the receipt must count **distinct READY pins**, not verdict lines,
and must say when the queue is dry or the coordinator is dead. Its build order also
lists a Monday-morning decision-card batch to Kam and the T5 multi-file split tier.
`WEEK-INSTRUCTION.md` is currently **`status: none`, `valid_until: 2026-09-16`** — the
mechanism is armed and empty, waiting for Kam's Monday-night line.

#### 3b. The break, and it is in the instructions, not the code

```
$ grep -n 'NEXT-PICKUP\|FIRST-BOOT' Launch_Wednesday.command
402:${BRAIN_DIR}/tasks/FIRST-BOOT-TUESDAY.md — it is who you are, …
404:${BRAIN_DIR}/tasks/NEXT-PICKUP-DATASEC-LAPTOP.md for the actual state of your projects.
405:Replace the first-boot brief with your own NEXT-PICKUP-TUESDAY.md at your first wrap; …
```

Three hits, **all inside the Tuesday paragraph**, and:

| file named at boot | exists in WED | exists in TUE |
|---|---|---|
| `FIRST-BOOT-TUESDAY.md` | **NO** | **NO** |
| `NEXT-PICKUP-DATASEC-LAPTOP.md` | **NO** | **NO** |
| `NEXT-PICKUP-TUESDAY.md` | yes | yes |
| `NEXT-PICKUP.md` | yes | yes |

Both missing files sit in `0_Brain/tasks/_superseded_2026-09-09/`. **Tuesday's very
first boot instruction is a read of two files deleted a week ago**, and her actual
pickup is named only as something to *write*.

**Wednesday is no better on paper.** No boot step names `NEXT-PICKUP.md` either; her
own ledger `_ledger.md` mentions it **zero** times. She reads it because she always
has. The evidence is in her own notes — `0_Brain/daily/2026-09-16.md:30`
*"…NEXT-PICKUP whole; yesterday's note WHOLE…"*, and `:47` *"NEXT-PICKUP +
EXPIRING-GRANTS + TASKS whole"*. Against that, Tuesday's notes for **2026-09-12 and
2026-09-13 contain zero** hits for `FIRST-BOOT` / `NEXT-PICKUP-TUESDAY` /
`NEXT-PICKUP-DATASEC` (positive control from the same files: "Tuesday" appears 38 and
33 times).

**So the continuity of an ongoing task rests on a habit one seat has and the other does
not, and on no instruction at all.** That is R3, and it is the single cheapest fix in
this document.

#### 3c. What is missing for a seat to run a week unattended

| gap | class | already designed? |
|---|---|---|
| the pickup is **read** at boot, by instruction, on both seats | **INSTRUCTION** | no — R3 |
| Kam's standing instructions carried as a **state-machine** (OWED / DONE / WITHDRAWN), not prose | **INSTRUCTION + CODE** | no — R7; the lesson exists, the mechanism does not |
| `WEEK-INSTRUCTION.md` **seat-scoped** so Tuesday's week is not Wednesday's | **INSTRUCTION** | no — R5 |
| hooks present, so a week-long seat cannot silently auto-compact | **CODE** | no — R1 |
| candidates **re-derived every 6 h** from the loop job (a ticket taken during the day must drop out) | **CODE** | yes — design piece (b), owed |
| receipt counts **distinct READY pins**, names holds, says "queue dry since" / "coordinator dead since" | **CODE** | yes — design piece (e), owed |
| empty-queue liveness line to the panel | **CODE** | yes — piece (d); G7/G8 **already in** Wednesday's `night_run.sh`, absent from Tuesday's |
| a ruled pool so the week does not run dry (KS-998, KS-1011, KS-1081, KS-1168 as one card batch with defaults) | **INSTRUCTION** (a card to Kam) | yes — build order item 4, owed |
| doctor refuses silence (hooks / chatsync heartbeat / pickup freshness) | **CODE** | no — R8 |
| Tuesday's tree pulled forward so she has any of the above | **CODE** | no — R6 |

The **pilot** the design names (Saturday, on renewed allowance: one seat boots on the
instruction file alone, briefs K=4, the receipt reports it) is still the right test, and
it should be run on **both** seats, not just Wednesday's.

---

### 4. Machine-local — what would NOT travel with a file copy

1. **Six launchd plists with no on-drive copy at all**:
   `com.wednesday.{shiftchange,wake,close,nassync,dailysweep,chatsync}.plist`, living
   only in `~/Library/LaunchAgents/` on `Kamils-Mac-Studio.local`. A `find` for these
   names across both trees returns nothing. All six hardcode
   `/Volumes/DevMASTER/WEDNESDAY/...`.
2. **Three that do have on-drive templates** — `com.wednesday.ornith-{night,loop,receipt}.plist`
   in `local-model/night/` — still need arming per machine.
   Good news: `scheduler/install_scheduler.command`, `night/install_night.command` and
   `night/install_receipt.command` are all **already agent-aware** (they refuse an
   unknown `WED_AGENT`, label jobs `com.$AGENT.*`, carry `WED_AGENT` in
   `EnvironmentVariables` because launchd does not inherit it, and correctly skip
   `dailysweep` for Tuesday since it sweeps Secuura). **`chatsync` is the one job no
   installer arms** — hand-installed, documented only as PORTABILITY item 22.
3. **`.claude/settings.local.json`** — gitignored; the hooks and permission guards. §1e.
4. **`.git/hooks/pre-commit`** — untracked by design (PORTABILITY 191-199). Present at
   3,109 B in **both** trees; **this one is already done** for Tuesday.
5. **`4_Credentials/.claude/`** — Tuesday's own Claude auth namespace
   (`Launch_Wednesday.command:71-76`): a **separate Anthropic account** with its own
   allowance. Wednesday deliberately stays on the global config. Both seats exec
   `claude --model opus`, so the *alias* matches; what the account can actually serve
   is unmeasured (§5).
6. **TCC grants** — scheduler automation (PORTABILITY 15) and calendar (18), GUI-only,
   per machine *and per terminal host*.
7. **tmux, iTerm2, jq, the Ollama model store** (PORTABILITY 13/14/17). Note
   `com.kam.ollama-models` is loaded on this Mac, and `local-model/set_ollama_pointers.sh`
   + `start_ollama.sh` exist **only in Wednesday's tree**.
8. **Hostname** — this seat is `Kamils-Mac-Studio.local`, Tuesday's is
   `Kamils-Mac-mini.localdomain`. The launcher's hostname fallback (`:49`) still names
   only `Kamils-MBP*`; the mini would hit the REFUSE branch if `WED_AGENT` were unset.
   The folder-name discriminator (`:44-46`) is what saves it — which is correct, and
   worth leaving alone.
9. **The dashboard server** — Tuesday deliberately does not serve one
   (`Launch_Wednesday.command:341-343`, Kam's "one website" ruling). Her panel presence
   therefore depends **entirely** on `com.tuesday.chatsync` plus the Studio being up.
   That is why item 1's chatsync gap reads to Kam as "Tuesday is not answering".

---

## What I could not establish

- **Whether Tuesday's Mac mini has any `com.tuesday.*` launchd jobs.** I measured this
  Mac only; the mini was not reachable from this session. The absence of
  `chat_sync.log` in her tree is strong indirect evidence for chatsync specifically,
  and says nothing about the other five.
- **Whether `/Volumes/KK_T9_External_HDD/TUESDAY` is the live checkout the mini boots
  from, or a synced copy.** Two gitignored artefacts argue it is live — her
  `4_Credentials/.claude/` (15 entries, `history.jsonl` 389 KB, mtimes to 2026-09-15
  09:06) and `fleet/cockpit/logs/wake_watch_runner.log` (848 KB, to 2026-09-14 10:40) —
  but I did not confirm the mini mounts this drive.
- **Tuesday's Claude account tier and weekly allowance.** Her auth lives in her own
  namespace and I did not open credential material. If that account cannot serve Opus,
  `--model opus` degrades silently and that alone would explain a large behaviour gap.
  **One check at the mini would settle it and it is cheap.**
- **Whether "not responding" means the panel or the terminal.** The panel numbers say
  she answered (2.4 min median, 0 unanswered); the frozen-pane evidence says the
  terminal. Kam's own words would settle which he meant.
- **Why Kam stopped her on 2026-09-14.** Her 06:52 history entry records the
  instruction-inversion correction; nothing on disk records a decision to stop the seat.
- **Whether the night pipeline is Datasec-usable at all.** `derive_candidates.py`
  derives from the Secuura KS board against a pinned tip. A Tuesday equivalent needs its
  own board and tip. Unmeasured.
- **The 54-line `wednesday_rotate.sh` diff's behaviour under Tuesday's seat resolver.**
  I read the diff (the refusal tap + the one-push-before-refusing on containment) and it
  is seat-generic by construction, but I did not exercise it.
