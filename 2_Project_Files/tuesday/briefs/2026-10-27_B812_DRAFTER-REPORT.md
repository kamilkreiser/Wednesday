STARTABLE: YES (after the stamp; Q1 to Q4 have defaults)

# B812 drafter report (Sonnet 5.5 drafter, 2026-10-27 about 11:05 to 11:40 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B812_SEAT-R60_composer-records-b682-ticket.md` (163 lines). Seat `Datasec/Security-Composer-R60`, Sonnet (row C8, `model-routing.md:98`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch line's quotes. No ports.

## BLUF
- ONE Jira write: `POST /rest/api/3/issue`, one PCOMP Task, label `plan-comp-389`, text written out in the kit (summary + 9 bold-led blocks), no comment, no transition, no edit. Scope is exactly the ruling's: the second gate's findings 1 to 3 (13 survivors: year 5, month 4, day 4), four closing rows, test-only, later PR with its own gate. Notes N1/N2/Q-1 and the PR #93 residue are explicitly out.
- Records on `records/b812`: new BACKLOG row #389 (the ticket row), one State append on #388 (O1), history entry, `JIRA.md` bullet; `CLARIFICATIONS.md` untouched (C-106 already files the ruling and says the filing is a later records brief). One `merge --no-ff` into root main.
- Main moved since B808 started: now `05424cdb` (B808 fold). The kit is written against that, and highest BACKLOG id 388, highest C-106.

## Facts re-measured (instrument; control)
| Fact | Instrument | Control |
|---|---|---|
| root main `05424cdb39c7...`, merges `05424cdb`, `23f6bad3`, `ce818b93`; `records/b812` absent, `records/b808` present; no `.tools/b812`; root dirt 1192 lines | `git --no-optional-locks rev-parse/log/for-each-ref/status --short`, `ls .tools` | `records/b808` found |
| BACKLOG #386-#388 on main, #389 free; C-106 at `CLARIFICATIONS.md:1900` | `git grep` on main, `grep -n` | #388 and C-106 found |
| Jira total 102, seed 94, held 19, composer 26, zzqxvbw 0; `plan-comp-388/389/390` = 0, `plan-comp-374` = 1 | `jira808.jql` (`project = PCOMP AND (...)`) | zero and positive controls both fired |
| Duplicate searches: quantifier, digit group, survivor, round cap, PR #92, f2245db0 each 1 = PCOMP-95 only; B682 0; 8347f91b 2 (PCOMP-97, -98 as parent sha); no ticket carries the residue | same | `composer` 26 |
| PCOMP-95: Task, Backlog, 1 comment (B808's 40200); description is the original 15 rows, no quantifier text | `jira808.get` | read whole |
| Newest ticket conventions (PCOMP-95 to -102: Task, Backlog, label `plan-comp-<row>`, no seed marker, Medium) | `jira808.jql ORDER BY key DESC` | -- |
| Second gate (B682 STATUS): VERDICT line 518 (1 line); findings at `:454-:458`; 13 = 5+4+4; 0 red of 30/82/164/1522; four closing rows; 132 -> ~148 calls; Notes N1/N2/Q-1 | `grep -n`, `sed -n` | VERDICT count 1 |
| Evidence files `c3d-table.txt`, `raw-route-answers-group-quantifiers.txt`, `fix4-closing-rows.txt` exist | `ls` | -- |
| R60 unused; Composer builder `Security-Composer-J25` (B806) live; ports 9750-9759 free | `grep -l -w R60` over SEAT kits (0), `tmux list-panes -a`, `lsof` | `R58` hits B806 and B808 kits |
| C8 line 98; sonnet id `claude-sonnet-5-5` | `grep -n`, `python3 -I` | -- |
| Kit hygiene: 14 lines with the four-underscore pattern (13 slot lines + last line); `B[0-9]{3}` in the quoted ticket blocks 0 (control: planted `B682` = 1); name terms in the ticket blocks 0 | `grep -c` | planted-line controls fired |

## D-decisions
- D1: ticket row is a NEW row #389 (label = row id, the 374/380-384 convention) plus one State append on #388, not an append alone. Reason: label `plan-comp-<row>` needs its own row.
- D2: the evidence folder path contains `B682`; the Jira text names the three files only (rule: no `B<digits>` in Jira text). Records may use the path.
- D3: the option words are quoted once in the kit with the coordinator's name replaced by "[the coordinator]" (fence 7; the seat copies by program from C-106's Ruled line, as B808 did). Verbatim form with the name is in the commission, not in the kit. The ticket quotes no option words and gives the ruling's date only, no time, no order claim.
- D4: the Jira client is B762's create fence (one Task) narrowed to label `plan-comp-389`; B808's client had a comment-only fence.
- D5: local text scan runs BEFORE the create (no edit exists after).

## Q-questions for Tuesday (each with a default)
- Q1: PCOMP-95's comment (id 40200) says "not ticketed as of this comment". Want a pointer comment on PCOMP-95 to the new key? Default: no (one write verb only, as commissioned); a further brief if wanted.
- Q2: Priority? Default: none sent, Medium stands like PCOMP-95 to -102.
- Q3: Ticket text byte-approval? Default: the stamp accepts the shape; seat freezes and asserts every figure.
- Q4: Row #389 + #388 append, or append only? Default: both (slot ROW-STATE).

## UNMEASURED
Raw test file and `app.ts` at the squash (figures RELAYED from the gate); the three evidence files' contents; PR #92 facts re-read via `gh` (RELAYED from #387/C-106); the card store option label; main/Jira after about 11:20.

## Outside-the-fences disclosure
None. Read-only throughout: Jira GETs via `jira808.py` (scratch scripts in the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/5d4f3df6-7a7d-4042-a868-99d30aaa36b8/scratchpad/r812.py` and `r812b.py`, which import the helper's `get`/`jql`/`adf_text` only), git read verbs, grep/sed, tmux, lsof. No card store access, no `gh`, no ledger or staged-brief reads. One Bash call was refused by the cd hook and one by the zsh `=` hook; both re-issued without the offending text. Two files written: the kit and this report.
