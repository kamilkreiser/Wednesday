# B641 DRAFTER REPORT (builder brief for Security Composer PR #89 round 3, SEAT-J12, test files only)

Drafted 2026-10-25 07:26 to about 07:45 AEDT (clock `date`) by the read-only kit drafter (Sonnet 5.5). Nothing was built, run, fetched, cloned or launched. Two files written under `tuesday/briefs/`; no other file written. Read-only `gh` only (`gh auth status` printed `Logged in to github.com account kamilDatasec`); git READ verbs only in the Composer repo; no `decision_queue.sh`, no Artifact/Docs/mail/chat tool.

## BLUF
- **Startable: YES**, once Tuesday stamps it (8 slots plus the last line) and load allows. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B641_SEAT-J12_composer-89-round3-deploy-scanner-rows.md`.
- **Kit: 152 lines; 9 lines carry the four-underscore pattern** (eight slot lines at 128-135 and the last line `READ-WHOLE-BY-TUESDAY: ____` at 152): `/usr/bin/grep -c -E '_''_''_''_'` prints 9 (the stamped copy must print 0). 0 non-ASCII bytes and 0 tabs (python byte count; control `cafe` with an accent counts 2), 0 `@CAPS@` tokens. No person's name, no card slug.
- Seat J12, pane `Datasec/Security-Composer-J12`, ports **9910-9919**, Sonnet `claude-sonnet-5-5`, row C2 build. One commit on `577e31d7`, plain fast-forward to `b616/composer-c-db-0026-0027`; two paths only: `packages/db/test/b616-deploy-commands.db.test.ts` and `packages/db/test/b616-0026-down.db.test.ts`.
- Tuesday's ruling is in the brief verbatim (line 11).

## FACTS, RE-MEASURED, WITH THE INSTRUMENT
| Fact | Value | Instrument and time |
|---|---|---|
| PR #89 head and branch | `577e31d7da4308b022eee1c4798c34e3dd13a846` (branch = `refs/pull/89/head`) | `git --no-optional-locks ls-remote origin ...`, 07:26:20 |
| main | `e019ac3abf628cbb6a50eb871b8f65b86a58ff6e`, unmoved | same |
| `refs/pull/89/merge` | `83fcd6a9dc9aa9a8179456f3222efa7dbb902e97` | same |
| PR #88 head | `0ba2a6b0b165f541789d5fe4704a3477ffd84319` | same |
| PR #90 branch | `b631/composer-test-wait-and-comment` = `7b2b238672a7180f1710d085827bbc8fb14b3775` | same; `gh api pulls?state=open` |
| `refs/heads/b641*`, `b626*`, `b640*` | none (ls-remote of `refs/heads/b6*` listed no such name) | same |
| PR #89 state | open, not draft, mergeable true, clean | `gh api -X GET pulls/89`, 07:26 |
| Open PRs | #90 (2 files), #89, #88 (3 files), #86 (2 files), #85 draft (57 files) | `gh api pulls?state=open`, `pulls/<n>/files` |
| Shared paths with Yours | 0 (the two test files appear only in #89; #90 holds one web and one engine test; #88 holds `app.ts`, its test file and `openapi.test.ts`; #86 holds two package files; #85 holds content, engine, renderers files, none under `packages/db`) | read of the file lists, 07:2x (not a `grep -x -F` run: UNMEASURED as a program; the seat re-runs it with controls) |
| Ports 9910-9919 | free | `lsof -nP -iTCP:9910-9919 -sTCP:LISTEN` rc 1, 07:26; whole-word scan `/usr/bin/grep -l -w -E '991[0-9]'` over non-`.pre-` briefs 2026-10-24_* and 2026-10-25_*: 0 files; control `printf 'port 9915 x'` reads 1 |
| Other blocks named by briefs | G104 (B640) 9900-9909 (adjacent, not overlapping), J11 9810-9819, G99 9830-9839, J10 9770-9779 | `/usr/bin/grep -o` of B631 and B640, B627 briefs |
| Live panes | `tuesday`, `Datasec/HPSM-POC-G103`, `Datasec/NexusAI-G100`, `Datasec/MPS-M20`, `Datasec/MPS-M19`, `Datasec/Security-Composer-J10`, `fleet-monitor` | `tmux list-panes -a -F '#{@cockpit_name}'`, 07:26 (no J12, no G104, no G98 pane) |
| Load | 9.52 9.52 9.63, then 10.43 9.77 9.71 | `uptime`, 07:26 and 07:27: above the 7 gate, expect a wait |
| `.tools` | b615, b616, b618, b620, b623, b624, b627, b631, b633 and `wt-b624-*`, `wt-b627-*`, `wt-b631-*`, `wt-b633-*`; no b640 yet, no b641 | `ls .tools`; glob `*b641*` "no matches" |
| New test file | 119 lines, blob `a9ab73640aabae292f8d1827ac318ca574ee4bf0`; head tree `41abb32c4766cb5434a7e54281f3e98c6c754153` | `git rev-parse <head>:<path>` |
| Round-2 delta | 6 files, +153 -13 | `git diff --stat d3dfb5c5 577e31d7` |
| Scanner defect lines | `:29` `line.startsWith("```")`, `:30` the `inBlock` toggle, `:85` `span.includes("!")`, `:91` the psql guard, `:88` and `:97` the two row titles | `git show 577e31d7:<path> \| cat -n` |
| REFUSE 7 strings | each prints 1 (7 strings in 3 files; control `zzz-no-such-string-7f3a` prints 0) | `git show <head>:<path> \| /usr/bin/grep -c -F`, 07:4x |
| DEPLOY.md fences | 16 fence lines, 12 indented (2-3 spaces), 4 at column 0, no `~~~`; **between lines 432 and 540 exactly ONE fenced block, column 0, lines 450-453; the 0027 section (492-539) holds none** | `awk` over `git show <head>:DEPLOY.md`; headings by `/usr/bin/grep -n -i` |
| `shape()` in 0026-down | privileges query at `:84-87` with `AND grantee = 'pc_app'` (`:85`); `b616-0027-down.db.test.ts:65-72` carries the `grantee` form plus the `table_privileges` query | `git show \| sed -n` |
| `input_hash` column | `0001_core_schema.sql:180` `input_hash char(64)`, in the table starting at `:170` (`policy_version_id`) | `git grep -n -i input_hash <head> -- packages/db/migrations` and `sed -n 170,182p` |
| Model | `levels.sonnet.model_id` = `claude-sonnet-5-5` (checked_at 2026-10-25 07:19 +1100); opus `claude-opus-5-5` | read of `models_latest.json` |
| Routing | C2 build `model-routing.md:92`; C1 `:91` ("Gate NO GO: one fix round on the same seat model"); L6 `:85` does not fit (local row; the Claude column is "apply the ready golden", none exists); next gate G2 `:109` (tier 2) | `/usr/bin/grep -n -i -E` over the file (154 lines) |
| Wrapper source | `.tools/b624/scripts/` holds `vt.sh` (db-group vitest with the tree and a named DEPLOY.md mounted at `/repo/DEPLOY.md`), `fmt.sh`, `heavy.sh` (gate, heartbeat, `$K/logs/heartbeat.txt`), `names_cmp.py`, `pty_paste.py` | `wc -l` and `sed -n 1,8p` of five files (read, not run) |
| Gate B633 | 273 lines; findings 213-231; C6 tables 134-171; ROUND-CAP 240-248 | read whole |

## D-DECISIONS (mine; Tuesday strikes any at the stamp)
- **D1 Ports 9910-9919.** Free; no brief names the block; the G104 gate holds 9900-9909 (adjacent). Keep.
- **D2 Model and row.** C2 build, `BRIEF_SEAT_LEVEL=sonnet` = `claude-sonnet-5-5`, id read from `models_latest.json`. Row L6 rejected (reason above). Operator deploy text is not touched this round, so no Opus argument; the scanner is a test-validity surface. Keep.
- **D3 Wrapper source.** The finished builder J9's kit `.tools/b624/scripts/` (ten named files, read-only, `cmp` at copy, rename only), because it already carries the restored `ps` gate, heartbeat, move-release and 40-minute give-up and has `vt.sh` and `fmt.sh` that mount a named DEPLOY.md. The gate G99's scripts and evidence stay unread (precedent: B624 and B627). The builder writes its own mutant driver; `mut*.py` of the earlier lanes stay unread.
- **D4 Scanner design left to the seat inside rails.** The brief fixes the behaviour (track open and close of every fence, any indentation, trim the info string, first word decides, drop an unterminated block) and the claims that must become true, not the code. Both existing titles stay byte-for-byte (names lost 0).
- **D5 The psql guard moves INSIDE a function a control row also calls** (so S11 is killable wherever the guard sits). This is a design requirement of B-2; the DEPLOY row keeps its title and its call.
- **D6 Two proofs of the planted bang, not one:** durable in-memory rows over the real DEPLOY.md text (one block planted per section, indented and column 0), plus one-off planted DEPLOY.md copies mounted at `/repo/DEPLOY.md` (the gate's own method, with the sha256 printed inside the container). Reason: the 0027 section holds no block at the head, so only a planted one can prove that section; and a durable row stays after this round.
- **D7 S10 (whole file scanned) handled by an optional bound control** ("a bang after `## A later migration` and before the first heading is not flagged"); if the seat adds none it argues S10 equivalent. S12 stays equivalent-or-stronger (argued). S15 is now the shipped behaviour, so its inverse S15r must be killed; the brief adds own mutants S16-S22 for each new branch of the fixed scanner. Any reachable survivor is fixed before the push (this is the last commit the ruling allows).
- **D8 B633-8** (ids in the file's header comment): REMOVE, since the file is touched anyway; the gate graded it a Note and the brief made it an item the READY line reports.
- **D9 B633-5 fix** copied from `b616-0027-down.db.test.ts:65-72` (grantee in the select and order, plus `table_privileges`), with a first measurement that head equals base on the unmutated recipe. The n1/n6 column `input_hash` was read in `0001_core_schema.sql:180`; the seat re-measures.
- **D10 One CodeQL alert = STOP** (no second commit without Tuesday's word, since the ruling allows one commit).
- **D11 Time.** Target READY 2 h, hard stop 3.5 h, no later than 12:30 AEDT; load is 9-10 so waits dominate. Tuesday names the time.
- **D12 READY line** carries the round-3 note, per-finding results, the S01-S22 killed/survivor counts, and "test files only".
- **D13 pty proof** is one macOS bash and one zsh paste of the planted indented command (the shell stops at `event not found` before docker runs, so no stand-in docker is needed); the Linux shell is NOT TESTED (the gate measured Linux bash 5.2.15 already).

## Q-QUESTIONS FOR TUESDAY
- **Q1 B633-4 and B633-3 (unchanged DEPLOY.md sentences) stay open.** The gate noted that B633-4 read without Tuesday's earlier "Minor" ruling would be a G-7 Major (the 0026 sentence is false for a database holding 0026 and 0027, and the new 0027 sentence says the name is not fixed). The ruling bars any DEPLOY.md byte this round, so they go to the tier 2 gate unchanged; the brief lists them in FOR TUESDAY. Confirm that the product owner is told, or ticket them.
- **Q2 Gate model for the next gate.** Row G2 (`:109`) says tier 2 is Sonnet first; the scanner is a test-validity surface where the round-2 gate (Opus) found two Majors the builder missed. Sonnet or Opus for the tier 2 gate is yours.
- **Q3 Launch timing.** Load is 9.5-10.4; J10 (B627) is live; G104 (B640) may launch beside it. `launch_when_cool` will hold the launch. Confirm J12 goes after G104 or alongside.
- **Q4 Intersection program.** My 0-shared reading was by eye from the file lists, not by `grep -x -F`; the seat re-runs it with controls (REFUSE 4).

## UNMEASURED (nobody ran it)
Every build, test, mutant, pty, container, probe; that P1-P5 behave in the current scanner as the gate's V9-V11 did; that the fixed scanner is green on the real head file; that the wider `shape()` leaves the 0026 down-test green on the unmutated recipe; that the image build is a cache hit; that `vt.sh`, `fmt.sh`, `names_run.sh` run unchanged after the rename; whether the tier 2 gate finds a further reachable scanner variant (nested lists deeper than one level, block quotes, a fence opened inside an indented code block).

## OUTSIDE THE FENCES (disclosed)
Two Bash calls were refused by shell hooks (one with a `cd`, one with an unquoted `======`); nothing ran. One `grep -P` call failed on macOS grep and was redone in python. I read five `.tools/b624/scripts` files' first 8 lines (read-only, Composer project) and the opening of briefs B631, B640, B626, B627, B633-drafter-adjacent text for ports and kit names; I did not open `Source_Documents`, any SOW, `inbound/`, `decision_queue`, or the stray file `!CODING/Datasec/Datasec`. No other project's material was read.
