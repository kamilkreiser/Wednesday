---
date: 2026-11-27
type: census
source: read-only structural census, measured 2026-11-27 10:31 to 10:45 AEDT in the tree /Volumes/DevMASTER/WEDNESDAY on host Kamils-Mac-mini (HEAD 895d8b6c8c)
status: live
---

# Current structure census: the three coordinator seats, as measured today

Facts only. Every number is a byte count from `stat`/`wc -c` or a count printed by a command run in this census. Tokens are bytes/4 (an estimate, not a tokenizer reading). Datasec-owned files are reported by path, size and structure only. Files in this tree were changing while measured (a sync loop pulls every 60 s): `NEXT-PICKUP-TUESDAY.md` read 936,327 B and then 937,390 B a few minutes apart.

---

## A. BOOT

### A1. The launchers

| File | Bytes | What it does |
|---|---|---|
| `Launch_Wednesday.command` | 70,422 | THE shared launcher. Resolves the seat from `WED_AGENT`, else the tree's folder name, else hostname, else refuses. Builds one `INITIAL_PROMPT` for all three seats with per-seat substitutions. |
| `Launch_Tuesday.command` | 2,063 | Sets `WED_AGENT=tuesday`, then `exec bash Launch_Wednesday.command`. |
| `Launch_Friday.command` | 3,504 | Refuses outside a tree named FRIDAY; first-run logins (`2_Project_Files/friday/first_run.sh`); loads `4_Credentials/friday.conf`; arms the usage publisher; sets `WED_AGENT=friday`; execs the shared launcher. |
| `Launch_Cockpit.command` | 5,854 | Preflight (claude, tmux, iTerm2), then starts the tmux `fleet` session from `fleet/cockpit/cockpit.conf` (pane 0 = the Wednesday launcher, pane 1 = the monitor). |
| `Launch_New_Machine.command` | 26,006 | Machine bring-up for the Datasec seat (installs, jobs). Not a boot path. |

The root also holds 46 `Launch_Wednesday.command.pre-*` backups (18,777 B to 69,941 B each) and 2 other launcher backups. The launcher grew from 18,778 B (2026-09-03) to 70,422 B (2026-11-22).

### A2. What the launcher runs BEFORE the prompt (in order)

| Step | Launcher lines | Writes |
|---|---|---|
| git fetch / pull of this tree | ~205-250 | the working tree |
| `tools/boot_digest.py --by-tier`, then `tools/boot_digest.py` | 259-265 | `_boot_digest_by_tier.md`, `_boot_digest.md` |
| `tools/rules_card.py --seat <seat>` (only if `_rules_card_<seat>.md` already exists) | 272-282 | `_rules_card_<seat>.md` |
| arm `tools/panel_sync.sh loop`, `fleet/cockpit/live_chat_poll.sh`, `dashboard-cloud/seat/publish_usage.sh` | 285-372 | background loops |
| `tools/render_claude_settings.py` | ~382 | `.claude/settings.local.json` from `.claude/settings.template.json` |
| `doctor.sh --quiet` (103,098 B) | 400-445 | preflight output; hard failures gate a human launch, are carried into the prompt on a rotation |
| `fleet/cockpit/arm_wake_watch.sh`, statusline wiring, local dashboard server | 452-560 | background loops |
| `tools/latest_models.sh` | near the end | `0_Brain/dashboard/data/models_latest.json` |
| `claude --dangerously-skip-permissions --model <alias> "$INITIAL_PROMPT"` | last lines | the seat |

Model at boot: `--model opus` for Wednesday and Tuesday; `--model fable --fallback-model opus` for Friday (launcher comments dated 2026-11-16 and 2026-11-21).

### A3. The boot prompt and the ordered read list

The prompt template (launcher lines 653-875) is 16,976 B before substitution; with the per-seat scope block (lines 592-651) the region is 21,529 B. The Claude Code harness additionally auto-loads `/Volumes/DevMASTER/CLAUDE.md` (12,611 B) and `WEDNESDAY/CLAUDE.md` (11,072 B) as project instructions (observed in this census session's own context).

| # | Prompt step | File | Wednesday B | Tuesday B | Friday B | Read mode stated in the prompt |
|---|---|---|---|---|---|---|
| 1 | rules | `CLAUDE.md` | 11,072 | same | same | whole |
| 1 | routing | `0_Brain/CLAUDE.md` | 4,487 | same | same | whole |
| 2 | identity | `0_Brain/identity/persona.md` | 1,925 | same | same | whole |
| 2 | identity | `0_Brain/identity/voice-protocol.md` | 3,658 | same | same | whole |
| 2 | people | `0_Brain/people/kam.md` | 4,228 | same | same | whole |
| 3 | rules card | `0_Brain/learnings/_rules_card_<seat>.md` | 113,173 | 112,423 | 114,510 | whole; REPLACES the by-tier digest |
| 3 | (fallback, no card) | `0_Brain/learnings/_boot_digest_by_tier.md` | 739,006 | same | same | whole only when no card exists |
| 3 | (second fallback) | `0_Brain/learnings/_boot_digest.md` | 745,136 | same | same | only if the by-tier file is missing |
| 3 | own ledger | `_ledger.md` / `_ledger_laptop_datasec.md` / `_ledger_friday.md` | 27,186 | 91,940 | 92,562 | whole |
| 3 | other ledgers | the other seats' ledgers | 184,502 | 119,748 | 119,126 | "row headlines only" (partial; not counted below) |
| 3 | scoreboard | `0_Brain/projects_index/scoreboard.md` (2,089,382 B, 1,810 table rows, mean 1,154 B/row) | ~17,000 | filtered | filtered | newest ~15 rows; Datasec seats through an inclusion filter |
| 4 | pickup | `NEXT-PICKUP.md` / `NEXT-PICKUP-TUESDAY.md` / `NEXT-PICKUP-FRIDAY.md` | 287,068 | 937,390 | 371,618 | whole |
| 4 | grants | `0_Brain/tasks/EXPIRING-GRANTS.md` | 87,458 | same | same | whole |
| 4 | tasks | `0_Brain/tasks/TASKS.md` | 1,553 | same | same | whole |
| 4 | index | `0_Brain/projects_index/INDEX.md` | 230,651 | same | same | step 4 says read it; step 3 says its dated history "only back to the newest two blocks" |
| 4 | entries | `0_Brain/projects_index/entries/*` (7 files, one a sync-conflict copy) | 91,839 | same | same | "every file ... if it exists" |
| 4 | week | `WEEK-INSTRUCTION.md` / `-TUESDAY.md` / `-FRIDAY.md` | 5,051 | 4,475 | 1,356 | whole |
| 5 | daily notes | yesterday + today in `daily/` / `daily_tuesday/` / `daily_friday/` | 45,076 + 2,572 | 102,782 + 35,498 | 175,193 + 27,443 | whole (root CLAUDE.md says the last two notes) |
| 6-8 | live sources | project `history.md` heads, Linear API, AgentMail inboxes | n/a | n/a | n/a | network / other trees |
| later | before first launch | `models_latest.json` 4,721; `fleet/specs/model-routing.md` 27,514 | 32,235 | same | same | whole, once |
| Tuesday only | "on your very first boot" | `FIRST-BOOT-TUESDAY.md` 6,877; `NEXT-PICKUP-DATASEC-LAPTOP.md` 12,306 | - | 19,183 | - | text is still in every Tuesday prompt |

### A4. Totals of the mandated whole-reads (steps 1 to 5, excluding the prompt, partial reads and on-demand files)

| Seat | With INDEX.md + entries whole | bytes/4 | Without INDEX.md + entries | bytes/4 | Largest single item |
|---|---|---|---|---|---|
| Wednesday | 916,997 B | ~229,000 | 594,507 B | ~149,000 | pickup 287,068 (31%) |
| Tuesday | 1,721,379 B | ~430,000 | 1,398,889 B | ~350,000 | pickup 937,390 (54%) |
| Friday | 1,219,553 B | ~305,000 | 897,063 B | ~224,000 | pickup 371,618 (30%) |

A seat with no rules card would read the 739,006 B by-tier digest instead of its ~113 KB card (+~626 KB). Tuesday's and Friday's figures are the copies in THIS tree; their live trees are elsewhere (see NOT MEASURED).

### A5. Generated boot files

| File | Generator | When | Committed to git |
|---|---|---|---|
| `_boot_digest.md` (745,136) | `tools/boot_digest.py` (17,781 B) | every launch; wrap step 3b | yes (1,722 commits touch the by-tier file) |
| `_boot_digest_by_tier.md` (739,006) | `tools/boot_digest.py --by-tier` | every launch; wrap step 3b | yes |
| `_rules_card_{wednesday,tuesday,friday}.md` | `tools/rules_card.py --seat` (22,270 B) from `_rules_index.tsv` + the `_ledger*.md` files | every launch of that seat; wrap step 3b-i | yes |
| `_family_index.md` (14,026, mtime 10 Sep) | `tools/family_index.py` | not in the launcher | yes |
| `_tier_census.md` (14,682, mtime 5 Sep) | a tool under `2_Project_Files/tools/` (header says GENERATED) | not in the launcher | yes |
| `0_Brain/dashboard/data/models_latest.json` | `tools/latest_models.sh` | every launch | yes |
| `.claude/settings.local.json` | `tools/render_claude_settings.py` from the template | every launch | no (15 dated backups beside it) |

### A6. Where the three seats' boots differ (all from one variable, `WED_AGENT`)

| Aspect | Wednesday | Tuesday | Friday |
|---|---|---|---|
| Scope paragraph | Secuura + general | every Datasec project | both clients, with three claim/identity rules |
| Rules card | `_rules_card_wednesday.md` | `_rules_card_tuesday.md` | `_rules_card_friday.md` |
| Own ledger | `_ledger.md` | `_ledger_laptop_datasec.md` | `_ledger_friday.md` |
| Pickup / week file | `NEXT-PICKUP.md` / `WEEK-INSTRUCTION.md` | `-TUESDAY` variants | `-FRIDAY` variants |
| Daily notes dir | `0_Brain/daily/` | `0_Brain/daily_tuesday/` | `0_Brain/daily_friday/` |
| Own inbox | wednesday-agent@ | tuesday-agent@ | friday-laptop-agent@ |
| Claude config | global `~/.claude` | `4_Credentials/.claude` | `4_Credentials/.claude` |
| Stale-card tool | `tools/stale_card_escalate.sh --send` | `tuesday/tools/escalate_48h.sh --dry-run` | as Wednesday (default branch) |
| Model flag | `--model opus` | `--model opus` | `--model fable --fallback-model opus` |
| First-boot text | none | FIRST-BOOT-TUESDAY block | none (0 hits for FIRST-BOOT-FRIDAY in the launcher; the file exists, 5,309 B) |
| Scoreboard read | raw head | inclusion filter on `Datasec/` | inclusion filter |

Everything else in the prompt is identical text, written in Wednesday's voice: steps 2, 7, 8, 10 and the standing-behaviour block say "Become Wednesday", "[... -> Wednesday]", "dedicated Wednesday workspace" for all three seats.

### A7. Boot instructions that disagree with each other (same fact, different files)

| Fact | Says A | Says B |
|---|---|---|
| How lessons load | root `CLAUDE.md` session-start step 2: "Read ALL of `0_Brain/learnings/`"; `0_Brain/CLAUDE.md`: "**All** of `learnings/`" | launcher step 3: read the rules card, "Do NOT read the individual lesson files at boot" |
| Which machine a seat is on | launcher scope text: Wednesday "on the Studio", Tuesday "Mac mini" | this WEDNESDAY tree runs on `Kamils-Mac-mini`; pickup header says "Mac mini seat"; `_rules_index/README.md` records the same staleness |
| INDEX.md | step 3: history only back to the newest two blocks | step 4: read INDEX.md |
| Voice | root `CLAUDE.md` rule 3: "Moira, en_IE" | `PORTABILITY.md` item 2: "Matilda (Premium)" with a fallback chain to Moira |
| Master drive | root `CLAUDE.md` rule 0: "The T9 SSD is the master copy" | root `CLAUDE.md` header and `PORTABILITY.md`: DevMASTER is the master (2026-08-25) |

---

## B. BRAIN

### B1. Inventory of `0_Brain/` by folder (files on disk, `.venv`/`.git`/`node_modules` skipped)

| Folder | Files | Bytes | of which `.pre-*` / `conflict_on` backups (files / bytes) | Largest files |
|---|---|---|---|---|
| `learnings/` | 429 | 35,243,129 | 79 / 27,195,452 | `_ledger_archive.md` 2,898,334; its backups 2.4 to 2.8 MB each |
| `tasks/` | 408 | 113,968,054 | 386 / 108,536,225 | pickup backups ~2.0 MB each |
| `projects_index/` | 133 | 28,372,089 | 26 / 24,059,607 | `scoreboard.md` 2,089,382 |
| `dashboard/` | 158 | 35,651,945 | 77 / 12,087,198 | `data/chat_log.json` 6,946,320; `data/decisions.json` 5,204,491 |
| `daily/` | 125 | 19,036,548 | 8 / 2,987,413 | `.spoken.log` 1,025,085 |
| `daily_tuesday/` | 70 | 6,704,289 | 0 | largest note 396,140 |
| `daily_friday/` | 37 | 2,414,415 | 0 | largest note 192,322 |
| `inbox/` | 13 | 121,312 | 0 | |
| `skills/` | 10 | 47,009 | 1 / 5,871 | `delegation-protocol.md` 9,769 |
| `attention/` | 1 | 40,716 | 0 | `queue.json` |
| `handover/` | 5 | 33,305 | 0 | |
| `parkinglot/` | 2 | 23,917 | 0 | |
| `fleet/` | 3 | 13,324 | 0 | claims files |
| `people/` | 2 | 5,925 | 0 | |
| `identity/` | 2 | 5,583 | 0 | |
| root files | 2 | 16,779 | 0 | `CLAUDE.md` 4,487 |
| **Subtotal without `reference/`** | **1,400** | **241,698,339** | **577 / 174,871,766 (72%)** | live content ≈ 66.8 MB |
| `reference/` | 5,948,807 | 279,423,868,233 | 56 / 9,897,170 | three `dev.tgz` of ~304 MB each; 1,437 top-level entries |

Git: 65,143 tracked files in the repo, 20,601 under `0_Brain/` (19,303 of them under `reference/`); pack size 700.17 MiB; 29,192 commits; 4,367 tracked paths match `.pre-` or `conflict_on`.

### B2. Growth visible from dated names

| Series | 2026-07 | 2026-08 | 2026-09 | 2026-10 | 2026-11 (to the 27th) |
|---|---|---|---|---|---|
| Lesson files created (292 total, 1,229,441 B) | 4 | 78 | 129 | 46 | 35 |
| `daily/` notes: count / mean B / max B | 1 / 3,090 / 3,090 | 29 / 48,664 / 150,638 | 30 / 206,956 / 657,131 | 28 / 126,879 / 370,815 | 27 / 142,585 / 317,753 |
| `daily_tuesday/`: count / mean / max | - | - | 15 / 70,361 / 249,389 | 27 / 90,704 / 217,531 | 27 / 118,549 / 396,140 |
| `daily_friday/`: count / mean / max | - | - | 8 / 48,799 / 102,105 | 15 / 59,881 / 146,789 | 12 / 92,730 / 192,322 |
| Staged brief `.md` files in `fleet/briefs_staged/` (by mtime) | - | - | 1,755 | 1,196 | 2,365 |

### B3. The learnings pipeline

| Stage | File(s) | Size / count | Written by |
|---|---|---|---|
| Source of truth | `learnings/20*.md`, one lesson per file, YAML frontmatter (`date`, `type`, `source`, `status`, `tier`) | 292 files, 1,229,441 B; largest live 29,509 B | the seat, by hand, same session |
| Sidecar index | `learnings/_rules_index.tsv` (spec `_rules_index/README.md`, 6,246 B) | 134,264 B; 379 rows x 7 columns (`file, status, seats, family, triggers, enforced_by, rule`); 342 live, 25 superseded, 12 dead; 293 rows scoped `all`; 30 families; 5 rows with a non-empty `enforced_by`; rule text 91,251 B | the seat, by hand, in the same action as the lesson |
| Rules card | `_rules_card_<seat>.md` | ~113 KB, ~418 lines; "Most reinforced", then one section per family | `rules_card.py --seat`; weights recomputed each run from ledger rows citing the lesson, "never stored" |
| Moment lookup | none (stdout) | - | `rules_card.py --at <trigger>` over a fixed 22-word trigger vocabulary |
| Family files | `learnings/families/*.md` | 25 files, 328 KB; header: "synthesised from the member lessons" 2026-11-18 | hand/agent synthesis; no generator found in the launcher |
| Digests | `_boot_digest.md`, `_boot_digest_by_tier.md` | 745,136 / 739,006 B | `boot_digest.py`; per lesson: headline, frontmatter, operative paragraph, section index, rules sections verbatim |
| Checks | - | - | `boot_digest.py --check`, `rules_card.py --check`, both called from `doctor.sh` |
| Audits | `learnings/_audits/` | 14 files, 6 KB to 45 KB | weekly consolidation ritual (`0_Brain/skills/weekly-consolidation.md`) |

Measured overlap between generated files: the two digests share 93.9% of bytes in identical lines; the Wednesday and Friday cards share 67.4%; Wednesday and Tuesday cards 27.9% (the lines differ by the per-seat weight shown).

### B4. Ledgers and the archive rule

| File | Bytes | Table rows | Notes |
|---|---|---|---|
| `_ledger.md` (Wednesday) | 27,186 | 22 | longest row 5,858 B |
| `_ledger_laptop_datasec.md` (Tuesday; historical filename) | 91,940 | 73 | |
| `_ledger_friday.md` | 92,562 | 87 | |
| `_ledger_archive.md` | 2,898,334 | 1,937 | 64 dated `## Archived` blocks, 2026-08-29 to 2026-11-26 |
| `_ledger_laptop_datasec_archive.md` | 861,627 | 604 | 11 blocks |
| `_ledger_friday_archive.md` | 132,567 | 131 | 1 block |
| `_ledger_fleet_insights.md` | 90,296 | not counted | mtime 5 Sep |

Archive rule (root `CLAUDE.md` wrap step 3c): move every row older than ~3 days to the archive, verbatim, with a conservation assert; "Nothing is edited and nothing is deleted". Each archive run leaves a `.pre-*` copy of both files: 77 ledger/archive backups sit in `learnings/` (part of the 27.2 MB of backups there). `.gitignore` excludes `_ledger.md.pre-*` and `_ledger_archive.md.pre-*` only.

### B5. Pickup files

| File | Bytes | Lines | `##` blocks | Block shape | Backups beside it |
|---|---|---|---|---|---|
| `tasks/NEXT-PICKUP.md` | 287,068 | 912 | 109 | 106 dated STATE / CHECKPOINT / ROTATING / WRAP blocks stacked newest-first since the 2026-11-13 wholesale replacement (14 days), plus STANDING, OWED, FOLDED | 193 `.pre-*` |
| `tasks/NEXT-PICKUP-TUESDAY.md` | 937,390 | 1,654 | 58 | 57 blocks of one repeating kind, longest line 7,605 B | 127 `.pre-*` |
| `tasks/NEXT-PICKUP-FRIDAY.md` | 371,618 | 830 | 41 | 18 live-marked blocks, 21 marked superseded, longest line 18,509 B | 35 `.pre-*` |
| `tasks/NEXT-PICKUP-archive.md` | 1,590,574 | 5,820 | 551 | | |
| `tasks/NEXT-PICKUP-TUESDAY-archive.md` | 1,906,371 | 7,774 | 853 | | |
| `tasks/NEXT-PICKUP-FRIDAY.archive-2026-11-19.md` | 58,157 | | | | |

`NEXT-PICKUP.md`'s own frontmatter reads: "Replace wholesale; never stack: add ONE block at the top per checkpoint, and fold older blocks away at each rotation." The mean block is ~2.6 KB. `tasks/` holds 386 backup files totalling 108.5 MB against 5.4 MB of live files.

Other boot-read task files: `EXPIRING-GRANTS.md` 87,458 B (83 table rows; was 4,122 B on 2026-09-18, 20,142 on 10-02, 50,937 on 11-15); `TASKS.md` 1,553 B.

### B6. `projects_index/`

| Item | Size | Structure |
|---|---|---|
| `INDEX.md` | 230,651 B, 993 lines | 151 lines contain "refreshed"; project sections begin at line 689; per-project sections for 5 projects; "Known projects (pending first sweep)" list |
| `entries/` | 7 files, 91,839 B | one card per project, mtimes 4 Aug to 19 Sep; one is a sync-conflict copy (25,322 B) |
| `scoreboard.md` | 2,089,382 B | 1,810 table rows, one per scored delegation; 19 `.pre-*` backups of 1.5 to 1.6 MB |
| `decision_queue.md` | 83,328 B | |
| `clarifications_register.md` | 21,576 B | |
| dated sweep / lane / pack reports | ~95 files, 5 KB to 38 KB each | `2026-10-16` onward: morning-sweep, rotation-sweep, ticket-sweep, lane-plan files |

### B7. Places where the same fact is held in more than one file

| Fact | Copies |
|---|---|
| A lesson's rule | the lesson file; its `_rules_index.tsv` row (hand-written one-liner); three rules cards; two digests; its family file; ledger rows citing it |
| A correction event | a ledger row (2 to 6 KB of prose); the daily-note retro; often a lesson file; later the ledger archive |
| Seat state at a checkpoint | the pickup block; the daily note; `.pre-*` copy of the pickup; the pickup archive |
| Project status | `INDEX.md` section; `entries/<project>.md`; the project's own `5_Project_History/history.md`; scoreboard rows; sweep reports; Linear/Jira boards |
| A decision card | `0_Brain/dashboard/data/decisions.json`; the Azure Table `cards` (dual-write); `projects_index/decision_queue.md`; often quoted in a brief's "RULED BY KAM" section and in the pickup |
| A chat message from the owner | `chat_log.json`; `chat_<seat>.json`; `chat_kam.json`; the Azure Table `messages`; quoted verbatim in lessons, briefs and the prompt log (`1_Project_Definition/Discovery/00_prompt-log.md`, 274,524 B) |
| Session-start and session-end rituals | root `CLAUDE.md`; `0_Brain/CLAUDE.md`; the launcher prompt; workspace `/Volumes/DevMASTER/CLAUDE.md` (fleet-comms half) |
| Standing lines for briefs | `fleet/STANDING_LINES.md` (118,880 B, 60 `##` sections); `fleet/specs/brief-standing-lines.md` (143,551 B, 44 `##` sections); `fleet/specs/secuura-brief-traps.md` (8,619 B). The first two share 0 identical lines. |
| Model IDs and routing | `models_latest.json`; `fleet/specs/model-routing.md`; launcher comments; lessons |
| The whole brain | one git repo (`kamilkreiser/Wednesday`) cloned as the WEDNESDAY, TUESDAY and FRIDAY trees; a stale TUESDAY clone also sits at `/Volumes/DevMASTER/TUESDAY` (HEAD dated 2026-09-16) |
| Machine dependencies | `PORTABILITY.md` (54,031 B, items 1 to 31); `doctor.sh` checks; `Launch_New_Machine.command`; `dashboard-cloud/PORTABILITY.md` |

### B8. Generated or machine-refreshed files that are committed

`_boot_digest.md`, `_boot_digest_by_tier.md`, three `_rules_card_*.md`, `_family_index.md`, `_tier_census.md`, and 87 tracked files under `0_Brain/dashboard/` including `brain_state.json`, `agentmail.json`, `linear_*.json`, `*_calendar.json`, `news.json`, `tickets.json`, `usage_*.json`, `models_latest.json`, `decisions.json`, `chat_*.json`. The session's opening `git status` showed 15 of these dashboard files and 4 learnings generated files modified. `brain_state.json` appears in 4,735 commits; `NEXT-PICKUP.md` in 2,736.

---

## C. HOW A WORKER AGENT GETS CONTEXT TODAY

### C1. Three launch paths (one per seat)

| Seat | Path | How the brief reaches the worker | What the worker reads first |
|---|---|---|---|
| Wednesday | `fleet/brief_and_launch.sh` (5,783 B): usage gate, then `fleet/send_brief.sh` (42,818 B), then read-back of the project inbox, then `fleet/cockpit/cockpit.sh launch <Client/Project>` (35,567 B) | by EMAIL (AgentMail) to the project or lane inbox from `fleet/inbox_routing.conf` (~215 routes); subject `[Wednesday -> <Client>/<Project>] ...` | the project's own `Launch_Claude.command` boot ritual, then the mail |
| Tuesday | `2_Project_Files/tuesday/brief_seat.sh` (4,495 B) run inside a cockpit pane | a brief FILE at an absolute path in the coordinator's tree, named in the prompt | per its header: the brief (its step 0 copies it in); project identity dirs from the project |
| Friday | `2_Project_Files/friday/brief_seat.sh` (1,512 B) | a brief file path relative to the project dir | `./CLAUDE.md` and `1_Project_Definition/CLARIFICATIONS.md`, then the brief |

`cockpit.sh launch` looks the launcher path up in `fleet/cockpit/launchers.conf` (4,758 B, 41 rows mapping projects and lettered lanes to 10 distinct launcher paths) and runs it in a new tmux pane; `SEAT_MODEL_ENV=<id>` is passed through as the project launcher's model variable. On this machine 2 of the 10 launcher paths exist (both Secuura); the 8 Datasec paths point at mounts not present here.

### C2. What `send_brief.sh` enforces (refusals, read from the script)

| Gate | Refuses when |
|---|---|
| Seat identity | `WED_AGENT` unset/unknown, or disagrees with the tree's folder name |
| Routing | destination not in `inbox_routing.conf` |
| Subject tokens | a stop/hold/checkpoint token outside the leading position |
| Body size / placeholders | body empty or trivially short; an unfilled `@UPPER@` token |
| `PROVENANCE:` block (`--kind brief`) | missing, a line without `<fact> | <source> | read YYYY-MM-DD`, a relative path with no tree named, a scope claim or a queued ticket with no provenance line |
| `SELF-CHECK:` line | missing, or dated other than today |
| `RULED BY KAM, NOT YET IN AN ARTEFACT` | ruled-but-undelivered cards exist for the project and the section is absent |
| Lane tag | body prints another lane's outbound tag |
| GO mails | a stray untracked file exists (`gate_stray_check.sh`) |

`STANDING_LINES.md` states of itself: "What this is NOT, stated plainly: a mechanism. Nothing forces a brief to carry these." No script among `fleet/*.sh`, `tools/*.sh`, the tuesday tools or the launcher references either standing-lines file by name (0 files matched).

### C3. Templates and specs

| File | Bytes | Content (structure) |
|---|---|---|
| `fleet/specs/BRIEF_SKELETON.md` | 6,183 | BLUF; 1 ITEM 0; 2 queue; 3 HOLDS; 4 "if an instruction looks wrong, say so" + the wake; 5 RULED BY KAM literal; 6 RULED BY WEDNESDAY literal; PROVENANCE and SELF-CHECK literals |
| `fleet/STANDING_LINES.md` | 118,880 | 60 `##` sections: READY-FOR-QA definition, instruments, HOLDS, one repo-specific section, then ~50 single-incident rules appended by date (2026-09-22 to 2026-11-12) |
| `fleet/specs/brief-standing-lines.md` | 143,551 | 44 `##` sections, consolidated 2026-08-30, last modified 21 Sep |
| `fleet/specs/model-routing.md` | 27,514 | v1.0 in force 2026-10-18: model IDs read from `models_latest.json`; four checks before the table; local-model predicate; decision table 4a local, 4b Claude, 4c QA gates tiered by what the change touches; launch receipt; switching a seat |
| `fleet/qa-agent/QA_AGENT_CHARTER.md` | 24,230 | client-neutral testing charter, 10 sections |
| `fleet/qa-agent/BRIEF_TEMPLATE.md` | 17,119 | QA invocation brief: target, spec, scope, credentials pointer, cleanup, output boundary, evidence class, logistics |
| `fleet/qa-agent/gate_common.md` | 6,923 | common section of every gate commission: role, workdir, read-only checkout, pin subject, method, verdict file, report, rounds |
| `tuesday/DRAFTER_RULES.md` | 17,216 | 6 headings; 8 dated backups (6,391 B on 11-04 to 16,628 B on 11-21) |

### C4. Staged briefs, by size

| Set | Files | Total | Median | p90 | Max |
|---|---|---|---|---|---|
| `fleet/briefs_staged/` all entries | 8,011 (5,316 `.md`, 1,067 `.out`, 1,024 `.txt`, 200 `.subject`) | 83,966,444 B | | | |
| its `.md` files | 5,316 | 62,416,071 B | 2,546 | 39,978 | 425,508 |
| its `.md` files over 10 KB (the commissioning briefs) | 1,137 | 51,271,292 B | 38,006 | | |
| November files named `*seat*` | 652 | | 36,817 (mean 41,175) | | 425,508 |
| files named `*seatS*` / `*seatD*` | 148 / 143 | | 25,707 / 13,099 | | 155,871 / 95,031 |
| `tuesday/briefs/` `.md` (sizes only) | 4,146 | 111,598,700 B | 12,317; over-10 KB median 39,192 | 69,166 | 202,668 |
| `friday/briefs_drafts/` `.md` (sizes only) | 570 | 8,737,363 B | 9,092; over-10 KB median 23,561 | 38,041 | 98,201 |

A seat's round is one large brief (35 KB to 46 KB in the three read) followed by several small mails (700 B to 3.5 KB: answer-plan, go, answer-wrap).

### C5. Three recent Wednesday seat briefs, structure only (2026-11-26; a read-only measurement seat, a build seat, a merge seat)

| Section (generalised) | Measure seat, 46,143 B / 160 lines | Build seat, 38,095 B / 117 lines | Merge seat, 39,425 B / 120 lines |
|---|---|---|---|
| Title line (seat, lane, mode, tickets) | 1,449 | 1,181 | 584 (+1,079 preamble) |
| STAMP (coordinator fills; "wins over every line below") | 1,489 | 2,771 | 1,650 |
| AUTHORITY (owner's words verbatim) | 1,024 | 1,392 | 1,103 |
| HOLDS / carried rules | 1,587 | 841 | 2,167 |
| RULED BY KAM, NOT YET IN AN ARTEFACT | 686 | 564 | 1,056 |
| First actions / stop items / sequence | 1,491 | 3,090 | 921 |
| The work itself (task sections, what the drafter already read, kit) | ~23,900 | ~17,500 | ~21,900 |
| NOT YOURS / MAIL / BLOCKED / WRAP / ROUTING AND MODEL | 3,244 | 2,021 | 871 |
| PROVENANCE | 11,038 (28 lines) | 7,836 (22 lines) | 6,690 (20 lines) |
| SELF-CHECK | 203 | 215 | 263 |
| `/Volumes/...` paths pointed at | 37 | 30 | 29 |

Restated versus pointed at, measured on these files: verbatim-line overlap between consecutive briefs of the SAME lane was 1.0% and 0.8% of bytes; between different lanes 0.0% to 0.1%. Zero lines are copied verbatim from `STANDING_LINES.md` and none of the three names that file. `CLAUDE.md` is mentioned 0, 4 and 1 times; `history.md` 3, 3 and 2 times. Holds, mail rules, wrap rules and routing are therefore re-written in fresh words in every brief rather than pasted or pointed at; provenance is 17% to 24% of each brief. Each brief carries a STAMP section because a drafter sub-agent writes the body and the coordinator stamps it.

### C6. What the worker's own project launcher makes it read (one Secuura project, structure and sizes only)

| Item | Bytes | Notes |
|---|---|---|
| `Launch_Claude.command` | 39,821 | prompt with 7 scope rules and 9 first actions; default model from an env variable the cockpit sets |
| Required read a | `/Volumes/DevMASTER/CLAUDE.md` 12,611 | workspace rules |
| Required read b | `Notes (MASTER)/CLAUDE.md` 6,480 | vault routing |
| Required read c | project `CLAUDE.md` 27,858 | 27 headings: overview, repo and deploy, architecture (12 lines), local dev, environments, key rules, sync workflow, git flow, merge flow, session checklists |
| Client-level `CLAUDE.md` | 2,709 | |
| Context | `Notes (MASTER)/context/voice-and-writing.md` 1,534 every session; 5 other context files (1 B to 1,249 B) only when customer-facing | |
| Vault daily notes | today's and the newest prior note in `Notes (MASTER)/daily/` | |
| `5_Project_History/history.md` | 7,768,935 B, 1,395 `##` entries | "TOP entry" only; the top entry is 1,973 B |
| `2_Project_Files/BACKLOG.md` | not sized | open deferred items |
| Live checks | Linear, the team portal skill (`skills/Current/extranet.md` 11,616), AgentMail inbox | the brief arrives here |
| `1_Project_Definition/` | `PROJECT.md` 878 B; `architecture/` 4 files (1,354 to 22,100 B, all dated 2026-08-07); 2 roadmap HTML files (~100 KB each); 1 summary folder | NOT in the launcher's read list |

The fixed file reads total about 51 KB (~13K tokens) before the brief (35 KB to 46 KB) and the live checks. The project folder's root holds 137 entries, including ~35 dot-directories that are per-seat worktrees. Other projects for comparison: Tokenomics launcher 12,658 / `CLAUDE.md` 3,011; `QA_AGENT` launcher 2,979 / `CLAUDE.md` 8,230.

No file named or structured as a per-project "brief for coordinators" versus "brief for workers" was found: project knowledge for the coordinator is `INDEX.md` + `entries/` + pickup blocks; for the worker it is the project `CLAUDE.md` plus whatever the brief restates.

---

## D. SKILLS TODAY

### D1. `0_Brain/skills/` (the coordinator's rituals; 10 files, 47,009 B)

| File | Bytes | Modified | Purpose (its H1) |
|---|---|---|---|
| `delegation-protocol.md` | 9,769 | 2026-09-01 | the ritual for every delegated task |
| `delegation-monitoring.md` | 8,264 | 2026-08-05 | attending a live delegation |
| `working-rhythm.md` | 6,891 | 2026-08-10 | how the coordinator operates within her design |
| `weekly-consolidation.md` | 6,421 | 2026-10-05 | weekly consolidation ritual (+1 backup, 5,871) |
| `teammate-round-loop.md` | 2,185 | 2026-08-06 | teammate round loop |
| `browser-verify-before-deliver.md` | 2,171 | 2026-08-06 | browser-verify before deliver |
| `churn-aware-sync.md` | 2,052 | 2026-08-06 | two-pass churn-aware sync |
| `weekly-industry-scan.md` | 1,930 | 2026-08-03 | weekly industry scan |
| `lesson-ingestion.md` | 1,455 | 2026-08-03 | async teaching channel |

### D2. `/Volumes/DevMASTER/Notes (MASTER)/skills/` (read-only vault; the workers' skills)

`README.md` (5,385 B): "Skills are reusable instruction sets. They live here as markdown files and are referenced from project `CLAUDE.md` files"; `Current/` is "loaded by default in every project".

| `Current/` file | Bytes | Modified | One-line purpose |
|---|---|---|---|
| `always-verify-and-check.md` | 10,728 | 2026-04-25 | verify assumptions, confirm before claiming done |
| `end-of-session.md` | 10,750 | 2026-09-04 | commit, push, log, wrap mail |
| `extranet.md` | 11,616 | 2026-09-10 | session-start check of a client team task portal (+ a conflict copy, 11,339) |
| `platform-setup.md` | 4,935 | 2026-04-19 | step-by-step for common platforms |
| `no-skip-on-failure.md` | 3,052 | 2026-06-12 | fix root cause and re-verify, never skip |
| `no-time-deferrals.md` | 3,020 | 2026-06-12 | time is not a reason to descope |
| `azure.md` | 1,402 | 2026-04-19 | Azure conventions |
| `credentials.md` | 1,436 | 2026-04-19 | credential storage |
| `never-update-prod.md` | 1,249 | 2026-04-19 | gate changes that touch demo/staging/prod |
| `git-hygiene.md` | 1,183 | 2026-04-19 | commit and branch discipline |
| `security.md` | 1,093 | 2026-04-19 | secrets, input validation, least privilege, dependency hygiene |
| `pii.md` | 1,083 | 2026-04-19 | PII handling |
| `testing.md` | 1,017 | 2026-04-19 | tests on new functionality |
| `prompt-master.md` | 359 | 2026-04-19 | pointer to the meta-skill |
| `README.md` | 1,788 | 2026-04-25 | index |

`Meta/`: 8 files, 1,772 to 2,782 B (decision-toolkit, fact-checker, find-skills, front-end-slides, humanizer, mcp-builder, process-interviewer, prompt-master). `Library/`: 3 files, 867 to 1,102 B (agent-browser, audio-transcriber, open-router) + README. Ten of the fifteen `Current/` files have not changed since April 2026.

### D3. `.claude` skill and agent directories (list only)

| Location | Found |
|---|---|
| `/Volumes/DevMASTER/WEDNESDAY/.claude/` | `settings.local.json` (3,546), `settings.template.json` (4,162) and their backups; NO `skills/`, `agents/` or `commands/` directory |
| `2_Project_Files/**/.claude/{skills,agents}` (depth 4) | none |
| `~/.claude/skills/` | one folder `synced/` holding 4 UUID-named entries |
| `~/.claude/plugins/` | `marketplaces/claude-plugins-official`, `synced/` (the same 4 UUID names), `store/`, a 3,089,462 B directory cache |
| `~/.claude/agents/`, `~/.claude/commands/` | do not exist |

Hooks in `.claude/settings.template.json`: 1 PreCompact, 1 SessionStart (compact), 13 PreToolUse (no-cd, recursive scope, cockpit verb, seat-scoped chat, grep case, grep cut, no-rm, no-autostash, zsh wordsplit, pipe rc, note-alone, inbox scope, clock guard). `fleet/hooks/` holds 23 non-backup files.

### D4. Update checks that exist

| Thing checked | Mechanism | When |
|---|---|---|
| Newest model ID per level | `tools/latest_models.sh` -> `models_latest.json` from the Models API, else the public docs page; failure keeps the old JSON and prints its age | every launch |
| Digests match the lesson files | `boot_digest.py --check` via `doctor.sh` | every launch |
| Every lesson has an index row | `rules_card.py --check` via `doctor.sh` | every launch |
| Weekly consolidation not lapsed | `doctor.sh` reads the newest `_audits/` file's age | every launch |
| CodeQL CLI present and runnable | `doctor.sh` runs the drive-local binary (`tools/codeql/`, PORTABILITY item 29) | every launch |
| A skill or an external standard is current | NONE FOUND. No script in `tools/` or `fleet/` fetches, hashes or version-checks any file in `0_Brain/skills/` or the vault `skills/`; skill files carry no version or source-URL field in the heads read. |

### D5. Security and QA gate templates and the standards they cite

Word-bounded, case-insensitive counts across `QA_AGENT_CHARTER.md`, `BRIEF_TEMPLATE.md`, `gate_common.md` and `STANDING_LINES.md` (positive control: "SFDIPOT" counts 3 in the charter):

| Term | Charter | Brief template | gate_common | STANDING_LINES |
|---|---|---|---|---|
| OWASP, ASVS, CWE, NIST, ISO 27001, CodeQL, semgrep, gitleaks, ISTQB | 0 | 0 | 0 | 0 |
| SFDIPOT | 3 | 0 | 0 | 0 |
| session-based | 1 | 0 | 0 | 0 |

The vault's `skills/Current/security.md` (1,093 B) cites "npm audit" once and none of the standards above. Files in the tree that DO mention CodeQL/semgrep/gitleaks/OWASP: `tools/safe_push.sh`, `doctor.sh`, `fleet/specs/brief-standing-lines.md`. Gate tiering lives in `model-routing.md` section 4c. Per-gate artefacts: `fleet/qa-agent/briefs/` 882 entries, `gatesets/` 205, `launchers/` 360 (generated by `gen_launcher_from_template.py`, 4,987 B). `fleet/` also holds 12 `launch_secreview_*.sh` scripts and ~30 other one-off `launch_*.sh` scripts (Datasec-scoped; not read).

---

## E. EXISTING DATABASE OR STRUCTURED STORES

### E1. Local JSON stores in `0_Brain/dashboard/data/` (89 files, 54 of them backups or conflict copies)

| File | Bytes | Kind |
|---|---|---|
| `chat_log.json` | 6,946,320 | owner chat, all seats (gitignored; readers must filter on `view`, enforced by a PreToolUse hook) |
| `decisions.json` | 5,204,491 | decision cards: a JSON list of 1,706 objects with 11 fields (`id, title, bluf, client_project, options, recommended, default_action, status, ts, ruled_choice, ruled_ts`); 1,639 ruled, 65 withdrawn, 2 open |
| `chat_wednesday.json` / `chat_tuesday.json` / `chat_friday.json` | 2,546,609 / 1,491,799 / 797,610 | per-seat chat streams |
| `chat_legacy.json`, `chat_kam.json` | 1,569,832 / 126,913 | |
| `ack_state.json` | 111,868 | |
| 25 small files | 2 B to 13,004 B | `news`, `tickets`, `agentmail`, `brain_state`, `linear_wed`, `linear_personal`, `models_latest`, `parkinglot`, calendars, `views`, `layout`, `usage_<seat>`, `*_error`, `muted`, `pinned`, `archived` |

Other structured, non-markdown state: `0_Brain/attention/queue.json` (40,716); `_rules_index.tsv` (134,264); `fleet/inbox_routing.conf`, `fleet/cockpit/launchers.conf`, `cockpit.conf`; `fleet/card_id_gate.allow`; `fleet/state/` and `fleet/cockpit/state/` runtime dirs. Merging of the JSON stores across machines is done by purpose-built union tools (`tools/union_chat_log.py`, `union_decisions.py`, `union_scoreboard.py`, `decisions_union.py`, `records_union.py`, `reconcile_rulings.py`); there is no `.gitattributes` file in the repo root. `panel_sync.sh` header: "An automatic autostash corrupted decisions.json and chat_log.json today, twice".

### E2. The cloud dashboard (`2_Project_Files/dashboard-cloud/`)

| Aspect | Fact (from its `README.md`, 21,464 B, `requirements.txt` and `app/main.py`, 57,123 B) |
|---|---|
| Stack | FastAPI on an Azure App Service B1 Linux plan; `azure-data-tables==12.6.0`, `azure-identity`, `msal`, `PyJWT` |
| Storage | Azure TABLE storage (one storage account, managed identity, shared key disabled): tables `messages`, `cards`, `usage`, `files`; a blob container `files` in the same account |
| Keys | `PartitionKey` = client (`Secuura`, `Datasec`, `WED`, `Friday`, `ALL`, plus `USAGE`, `AUDIT`); `RowKey` = `<UTC ts>_<id>` or `card_<id>` |
| Content | rows hold ciphertext plus clear routing fields; per-record AES-256-GCM data key wrapped to the owner's key ring and the addressed seat's certificate key |
| Access | owner through Entra sign-in; each seat through its own Entra app + certificate; the partition comes from token roles |
| Relation to local | "dual-write": `tools/chat_reply.sh` and `tools/decision_queue.sh` write locally, then post the same record through `tools/_live_board.sh` |

### E3. SQL engines on this machine (Kamils-Mac-mini)

| Check | Result |
|---|---|
| `which psql postgres` | `/opt/homebrew/bin/psql`, `/opt/homebrew/bin/postgres` (symlinks into `Cellar/postgresql@15/15.19_1`); both report 15.19 |
| `brew list` filtered | `postgresql@15`, `sqlite` |
| `brew services list` | `postgresql@15` status `none` |
| running server | none (`pgrep -f postgres` rc 1) |
| `which sqlite3` | `/usr/bin/sqlite3` |
| database files in the tree (depth 4, outside `reference/`) | one: `2_Project_Files/tools/omlx/base/usage.sqlite3` |
| use by the seats' own memory | none found |

`PORTABILITY.md` item 25 on that Postgres install: "No service: no `brew services` job, no launchd plist; every suite/gate starts its own cluster on a private data dir + 127.0.0.1 port and stops it by pid." and "nothing uses it; never start a service on it." It was installed for one client's pre-push test suites, not for the framework.

### E4. What the rules files say about state, drives and machine-local dependencies (quotes)

| Source | Quote |
|---|---|
| root `CLAUDE.md`, rule 0 | "Portability first (Kam, 2026-07-31). The T9 SSD is the master copy — everything for this project lives on the drive so Kam can pull it and plug it into his laptop. Duplication is fine; tools may be installed drive-local (`2_Project_Files/tools/`). Machine-local dependencies (voice downloads, keychain items, Claude Code itself) go on the `PORTABILITY.md` checklist. Never store project state off-drive." |
| root `CLAUDE.md`, header | "one drive for Wednesday AND the dev code — DevMASTER is the master; the T9 becomes a unison sync copy/backup via `!SYNC FILES/Sync All Drives.command`" |
| root `CLAUDE.md`, wrap step 3a | "did this session install or start relying on any NEW machine-local tool/dependency? If yes → add a check to `2_Project_Files/doctor.sh` + a PORTABILITY.md item in the same wrap." |
| `PORTABILITY.md`, top | "DevMASTER is the master copy ... Plug it into any Mac and everything should be here. These are the ONLY machine-local dependencies; run through this list on a new machine." and "Keep this file updated whenever a new machine-local dependency appears." |
| `PORTABILITY.md`, item 6 | "Claude Code auto-memory | Lives in `~/.claude` per machine — NOT portable. Wednesday's real memory is `0_Brain/` (on-drive) by design; treat auto-memory as a cache" |
| lesson `2026-07-31_fully-portable-drive.md` | "Never store project state outside the drive (no ~/Library, no /usr/local, no machine-local caches that matter). If a tool needs installing, install it under the project folder" |
| rules index row for that lesson | "When I add a tool, state or config: keep it on the drive (2_Project_Files/tools/), keep scripts self-locating, list anything machine-local in PORTABILITY.md and doctor.sh." |
| `Launch_Tuesday.command` | "the two trees are clones of one repo" / "WHAT IS SHARED: this repo, the persona, the voice protocol, people/kam.md, and the W and M tier lessons." |
| launcher prompt, scope rule 3 | "Secrets: 4_Credentials/.env and 3_Access_Keys/ only; never committed, never copied into 0_Brain/ or 1_Project_Definition/." |
| lesson families (rules card) | a family `never-delete-quarantine` and wrap step 3c "Nothing is edited and nothing is deleted — this is a move" |

How state travels today: git (origin `git@github.com:kamilkreiser/Wednesday.git`; `panel_sync.sh loop` pulls and pushes every 60 s and skips a dirty tree), unison between drives (leaves `(conflict_on_<date>)` copies), a nightly NAS sync job, and the Azure Table for chat and cards. `PORTABILITY.md` lists 31 machine-local or drive-local items, including 12+ launchd jobs under `scheduler/jobs/`.

---

## F. PAIN SIGNALS ALREADY WRITTEN DOWN

| # | What the seats recorded | Where |
|---|---|---|
| 1 | The full lesson load cost 34% of the context window (lessons 336 KB + ledger); the digest was built in response. | `tools/boot_digest.py` header (2026-09-02); launcher step 3 |
| 2 | The mandated whole-reads were measured at ~886 KB ≈ 220K tokens, "more than a context window"; first carded 2026-09-09 at 229K and found still unruled on 09-18. | `learnings/2026-09-18_the-boot-spec-outgrew-the-context-window.md`; cards `wed-boot-read-exceeds-the-context-window`, `tuesday-boot-digest-outgrew-the-window` |
| 3 | A seat trimmed its own boot on an unmeasured window size; the arithmetic was wrong and the lesson was corrected the same day. | `learnings/2026-09-08_the-boot-spec-outgrew-its-window.md` |
| 4 | The pickup file's rule is "replace wholesale", yet 62 blocks had been appended; 91% of 220 KB was self-declared dead weight. Today's file again holds 106 stacked blocks. | same 09-18 lesson; `NEXT-PICKUP.md` frontmatter; `tasks/2026-10-23_pickup-owed-census.md` (a census commissioned because the Datasec pickup was read "in chunks, never whole") |
| 5 | The ledger reached 322 KB, larger than the digest beside it; rows run 1.4 to 3 KB of prose, so the 3-day archive rule "addresses age; the cost is driven by row size and row rate". | root `CLAUDE.md` step 3c; cards `wed-ledger-boot-cost`, `wed-ledger-archive`, `wed-ledger-archive-has-no-trigger`; `tools/family_index.py` header ("could trace ZERO behaviour changes to reading a ROW") |
| 6 | The boot prompt named one ledger when there were two; a seat read ~86K tokens of the other client's corrections and never opened its own. | launcher comment lines 561-582; card `wed-boot-names-one-ledger-there-are-two` |
| 7 | "The lesson digest is too large to read at boot": the rules index and card were built 2026-11-18 as a trial. | `learnings/_rules_index/README.md`; launcher lines 268-282 |
| 8 | Generated files drift or bite: the by-tier digest was stale for six days because the wrap named only the bare command; a fix written into a generated file lasted until the next boot; a sync-conflict copy of a lesson was served in both digests. | root `CLAUDE.md` step 3b; `learnings/2026-09-09_a-fix-in-a-generated-file-lives-until-the-next-boot.md`; `boot_digest.py` glob comment |
| 9 | Seats booted at 51 to 57% context by reading scoreboard, INDEX history and ledger whole; "a seat that boots past 50% has ~20 minutes of useful life"; one seat died at 100%. | launcher step 3 and CONTEXT INSTRUMENT paragraph; `learnings/2026-09-02_the-statusline-is-the-context-instrument.md`, `2026-08-03_context-discipline-close-before-full.md`, family `context-and-rotation.md` |
| 10 | Rituals that nothing triggers lapse: the weekly consolidation lapsed four Sundays twice; standing lines are "not a mechanism"; briefs are costly ("the brief is the cost"); brief pointers went stale. | `_audits/2026-11-16_consolidation.md`; `fleet/STANDING_LINES.md` preface; `learnings/2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md`, `2026-08-04_validate-brief-pointers.md`, `2026-08-25_travel-drive-stale-pointers.md` |

Related standing decision: `learnings/2026-08-03_context-loading-split.md` ("full for me, narrow for sub-agents"; sub-agents "also get loaded FULLY — for now ... this will be varied when required"). Earlier design note on tiers: `1_Project_Definition/Architecture/2026-09-05_learning-tiers-context-split-plan.md`. Today's commission is captured in `learnings/2026-11-27_fleet-structure-project-fable-postgres-brain-tiered-briefs-skills.md` (3,481 B).

---

## NOT MEASURED

| Item | Why |
|---|---|
| `4_Credentials/`, `3_Access_Keys/` | excluded by instruction |
| Tuesday's and Friday's LIVE trees | not on this machine's mounts. `/Volumes/DevMASTER/TUESDAY` is a clone whose HEAD is dated 2026-09-16 (no rules card in it); `/Volumes/DEV-Working/FRIDAY` exists but is not a git repository from this host; `tuesday/brief_seat.sh` names `/Volumes/Laptop-DEV/TUESDAY`, which is not mounted. All Tuesday/Friday sizes are this tree's synced copies. |
| Actual tokens and the statusline context % after a boot | bytes/4 is an estimate; no seat boot was run or observed |
| What a seat really reads versus what the prompt mandates | not observable from files (e.g. how much of a 937 KB pickup is read) |
| The 8 Datasec project launchers and their `CLAUDE.md` / `1_Project_Definition/` | paths in `launchers.conf` are absent on this machine (`/Volumes/DevMASTER/!CODING/Datasec/` does not exist; `/Volumes/Laptop-DEV` not mounted) |
| Content of Datasec-owned files (`tuesday/briefs/`, `daily_tuesday/`, Tuesday's pickup and ledger, `DRAFTER_RULES.md` body, `launch_secreview_*.sh`) | client isolation: sizes and structure only |
| The local chat stores' content and schema | a PreToolUse hook refuses unscoped reads of the chat store; only file sizes were taken |
| `0_Brain/reference/` in detail | 5.9 million files, 279 GB; only the total, the top-level entry count (1,437) and the tracked count (19,303) were taken |
| The 4 UUID-named synced skills/plugins under `~/.claude` | listed only; machine-local to this Mac |
| AgentMail inboxes, Linear, the Azure Table contents, launchd job state | network or credentialed sources; nothing was sent, posted or queried |
| Whether any worker launcher loads the vault `skills/Current/` files mechanically | the Secuura launcher's prompt names one skill file by path; the README says skills are "referenced from project CLAUDE.md files"; no loader script was found, and the other launchers could not be read |
| `2_Project_Files/BACKLOG.md` size in the Secuura project; the Secuura sibling projects' definition folders | not sized |
| Exact tracked/untracked split of each backup class | only repo-wide counts were taken |
