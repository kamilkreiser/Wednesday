STARTABLE: YES (once Tuesday stamps the ten slots and the last line; no Composer pane runs, root `main` and code `main` are as the kit says, PCOMP-128 is untouched since 2026-11-11, nothing needs a port)

# Drafter report, B1576 (SEAT-R235, Composer records for PR #129)
Drafter: a read-only Agent-tool drafter, 2026-11-15 14:37:39 to about 14:48 AEDT by the machine `date` (it printed 14:37:39, 14:37:56, 14:38:10, 14:38:20, 14:38:46, 14:39:37, 14:42:49, 14:46:03, 14:46:53). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1576_SEAT-R235_composer-records-129.md` (101 lines) and sidecar `.md.measured` (97 lines). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1576/` (`jget.py`, a copy of the s275 GET-only Jira helper; `textscan_copy.py`, a copy of B1552's scanner; `scan.py`; `measure.py`; `texts/` with the six texts; raw API reads `pr129.json`, `sq.json`, `sq_msg.txt`, `sq_body.txt`, `pr_body.txt`, `analyses.json`, `DEPLOY_base.md`, `DEPLOY_main.md`).

## BLUF
1. **Composer PR #129 is in none of the four root record files, and its ticket PCOMP-128 is untouched since 2026-11-11 (0 comments, 0 changelog entries, Backlog).** So, unlike the template B1552 (no ticket, zero Jira writes), this kit has ONE Jira write behind slot COMMENT-128: a facts-only comment on PCOMP-128 (TEXT-128, exact bytes in the kit), NOT moved, because items (2) and (5) stay open and its Done-when is "proposed, not ruled" (the project's Done rule C-111 (3) / C-112, as C-131 applied to PCOMP-12).
2. **The review's one Minor is RECORDED, not ticketed** (the commission asked "ticket or record, say which"): it is about the wording of the same three bullets, PCOMP-128 stays open as their ticket, and the review says "for a later wording pass". It goes into row #485 item (1) and one sentence of TEXT-128.
3. Records: C-149 (expected; next free by program), rows #484 (landing) and #485 (open items, row only), one optional `Update 2026-11-15 (C-149): ...` sentence on row #479 (slot STATE-479), one `JIRA.md` bullet, one history entry, one commit, one `--no-ff` merge into root `main` (no remote). **The 12/6 diff prediction of the B1569 kit appears nowhere in the records; every text states 9 lines added, 3 removed, in 3 places** (measured: `pulls/129` additions 9 deletions 3; `diff` of the raw DEPLOY.md at both shas 9 `>` and 3 `<`).
4. Measured: PR #129 merged true at 2026-11-15T02:16:27Z (13:16:27 AEDT), squash `27adb70991ff3d7ec13f0732de6ecdcb1aab8043`, ONE parent `68975c10`, tree `db97ada9...` equal to head `56fe57d4`'s tree, one path `DEPLOY.md` +9 -3, `compare` ahead 1 behind 0; code `main` = `27adb709`; open PRs #85 only. CodeQL and both Analyze success on the head before the merge; both Analyze success on the squash; `results_count` 0 on all four analysis rows; open code-scanning alerts on main 0. DEPLOY.md 758 to 764 lines; UNMEASURED on lines 360 and 693 only at main (5 lines at base).
5. `stamp_check.py` exits 0 (97 claims, 97 measured).

## Facts re-measured, with instrument and control
| Fact | Instrument (clock from `date`) | Control |
|---|---|---|
| PR #129 title, branch, merged true, `merged_at` 02:16:27Z, squash `27adb709...`, head `56fe57d4...`, base `68975c10...`, 1 commit, 1 file, +9 -3 | `gh api -X GET .../pulls/129` and `/files` under the project `GH_CONFIG_DIR` (14:37:56) | `pulls/9999` HTTP 404 (14:37:56, 14:46:03) |
| Squash: one parent `68975c10`, tree `db97ada98437959b830dfa47f3970cffefdc6011` = head tree, verified true, files `DEPLOY.md` 9/3; `compare` ahead 1 behind 0 | `commits/27adb709`, `git/commits/56fe57d4`, `compare` (14:38:10) | -- |
| Squash subject = PR title = `squash-subject.txt`; body after subject = `squash-body.txt`; title = `pr-title.txt` (each `diff` rc 0); PR body = `pr-body.txt` after `rstrip` (raw diff: the API adds two trailing blank lines) | `diff`, python compare (14:38:20, 14:46:03) | one-character mutant of the PR body compares unequal |
| Code `main` `27adb709`; open PRs [#85 draft]; newest PRs 129..120 | `branches/main`, `pulls?state=open`, `pulls?state=all&per_page=10` | list holds #85 and #128 |
| Checks: head `CodeQL` 02:14:28Z, `Analyze (csharp)` 02:14:35Z, `Analyze (javascript-typescript)` 02:15:36Z success; squash both Analyze success 02:17:59Z, 02:20:41Z, no CodeQL check-run | `commits/<sha>/check-runs` (14:38:20) | head lists 3, squash 2 |
| Analyses `results_count` 0 (2 per commit; `refs/pull/129/head`, `refs/heads/main`); open alerts on main 0 | full analyses list filtered by `commit_sha` in jq | `code-scanning/alerts?state=fixed&per_page=20` 20 rows |
| DEPLOY.md 758 -> 764 lines; UNMEASURED lines 360, 693 at main; 5 lines at base; `postgres 16.15` 3 -> 6; Route B first lines `:354 :401 :628 :677` | raw `contents?ref=` at both shas, `wc -l`, `grep -n`, `diff` | base count 5 vs main 2 (the grep can fire) |
| Gate VERDICT 31 lines, sha256 prefix `de5763ef8c051d47`; line 1 `GO WITH FINDINGS`; line 3 G2 docs round 1 of 2; line 12 Minor 1; finding text read whole | `shasum`, `wc -l`, `awk NR` | -- |
| B1569 STATUS 89 lines, prefix `6403f3d19dd3bd07`, last line `READY B1569: 56fe57d4...`; B1569 kit prefix `bb7e2b89e184b141` (equal to the project copy); authority phrase at line 123 (count 1), PART-WORDS BUILD line 127 | `shasum`, `grep -n -i -F` | `zzqxvbw` 0 |
| Root: HEAD main `c1c7a7b2`, no remote, 0 staged, record files clean, no lock/MERGE_HEAD, 126 refs, user.email and B1552 commit/merge identity `kamil.kreiser@datasec.com.au`; `records/b1576`, `.tools/b1576`, `wt-b1576-rec` absent | `git --no-optional-locks` read verbs, `ls` (14:37:39 to 14:42:49) | `records/b1552` resolves `d8d272da...`; `2_Project_Files` remote `origin` |
| Anchors: C-148 `:2789` highest, C-149 0; JIRA.md 57 lines, `- B1552` `:57`; BACKLOG 479 lines, 473 data rows, #483 `:479`, #479 `:475`, #484/#485 0; history 2,211 lines, B1552 at `:3` | `wc -l`, `grep -n/-c -E`, `awk -F'|'` | C-148 1, `^- B1552 ` 1, `| 483 ` 1 |
| Not already recorded: `PR #129`, `27adb709`, `56fe57d4`, `B1569`, `B1576`, `C-149`, `#484`, `#485` 0 0 0 0 | `grep -c -i -F` per file | `PR #128` 9 3 1 5; `C-148` 2 3 1 3 |
| Jira: PCOMP-128 Backlog, Task, `plan-comp-479`, updated 2026-11-11T18:03:30, 0 comments, 0 changelog, transitions 11/21/31/41 (41 Done); counts 128 / Done 47 / held 19 / seed 94 / needs-kam 2 / Backlog 81; `created`/`updated >= "2026-11-14"` 0 / 0; `plan-comp-483`, `-484` 0 | `jget.py` (every JQL `project = PCOMP AND ( ... )`, GET only, token in-process) (14:38:46) | `PCOMP-9999` 404; `plan-comp-479` 1; `composer` 66; `zzqxvbw` 0 |
| Helper fault the seat would hit: `.tools/b1486/scripts/jira_write.py:31` `newest=max(...)` raises on 0 comments | `awk NR==31` | PCOMP-128 comments 0 |
| Texts: TEXT-128 1,184 chars, SETTLED 1,245, ROW-484 1,577 (4 pipes), ROW-485 1,399 (4 pipes), STATE-479 347, TOPIC 282; all ASCII; records rule 0 hits on all six; Jira rule 0 hits on TEXT-128; sha256 prefixes `a6c6490115531ed3`, `3c40ff4a29438ae7`, `dedcb592055b6382`, `224d50b8a3f3ba50`, `0601692da9bf4c94`, `11a3ab66034bad1c` | `scan.py` (regexes copied from B1552's scanner + the B1509 Jira rule) | the 19 B1552 controls fire, both clean phrases clean; 12 Jira-rule plants fire (B1569, C-149, R235, gate, `_by_coordinator_`, status, bracket, backtick, 5 minutes, deployed, live, a path); a clean Jira phrase reads 0 |
| Kit spans equal the scratch texts byte for byte (1 span each); each HOLD replacement phrase occurs exactly once in its text | python over the kit | -- |
| Seat id: `R235`, `R234`, `R233` 0 files over the non-`.pre-` SEAT kits of 11-13/14/15 | `bash -c` loop, `grep -q -w -F` | `R232` 2, `R231` 7, `R228` 4 |
| Live seats' kits (B1568, B1571, B1572, B1573) name `Security Composer` 0 and `PCOMP` 0 | `grep -c` | this kit: `Security Composer` 9 |
| Model rows `model-routing.md:97` C7, `:110` G3; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:31` LEVEL default opus | `grep -n`, `awk NR` | -- |

## Differences from the B1552 template (each deliberate)
- **A Jira section with one write** (B1489's one-key form): closed list PCOMP-128, one comment, MOVE empty, dry run first, read-back by program, controls `PCOMP-12` / `PCOMP-127`. Template had "ZERO WRITES, AS A PROPERTY".
- **STATE-479 replaces STATE-481**: the earlier row the landing answers is PCOMP-128's row #479 (items (3) and (4) say "The words are stale").
- **Slot COMMENT-128** added (default HOLD); with HOLD, three phrases switch by program to "not commented" (each asserted once). Stamp: 10 slots + last line = 11 four-underscore lines.
- **REFUSE 5 STOPs if the numbers differ** (C-149, #484, #485 are written literally into the texts), instead of letting the seat renumber.
- **Helpers copied from `.tools/b1486/scripts/`** (the template copied B1549's GET-only ones), with the `max()` fault named.
- Texts carry no backticks (plain file names), so each is one backtick span in the kit, taken by program.

## Chain inputs (rule 4)
| Step | Inputs | Produced by / exists at |
|---|---|---|
| 0 | the kit; `.tools/b1486/scripts/` and `.tools/b1552/scripts/textscan_b1552.py` | BASE (exist now) |
| 0 | `refs-before.txt`, `status-all-before.txt`, `.tools/b1576/`, evidence `runs/` | made by Step 0 itself |
| PRIOR WORK | PCOMP-128 GETs, PR list, record files, C-131, C-148, rows #479 and #483 | BASE (read-only) |
| 1 | gate folder, B1569 STATUS and kit, GitHub reads, raw DEPLOY.md | BASE |
| 2 | decision table | Step 1 + slots |
| 3 | scanner copy + the texts | Step 0 copy; texts from the kit spans |
| 4 | `payloads.json` (TEXT-128), adapted helper copies | Steps 0 and 3 |
| 5 | the dry run's pass | Step 4 |
| 6 | comment id (or HOLD) for C-149 (3) and the bullet; texts | Steps 3 to 5; worktree made by Step 6's `worktree add` |
| 7 | STATUS | all earlier steps |

## D-decisions (mine)
- D-1: the Minor is RECORDED (row #485 (1) and TEXT-128), not ticketed (BLUF 2).
- D-2: PCOMP-128 commented, NOT moved (items (2), (5) open; Done-when not ruled).
- D-3: the builder's "pg_restore 16.15" note goes into row #485 (2) as NOT RULED; the builder's census note (22 vs 12 files) and the clock jump are left out (no effect on the record).
- D-4: the authority line claims no ruling of the product owner on the words: the lane ran under "keep going with the tickets" and the 2026-11-06 grant, and the coordinator accepted the words at the build stamp (PART-WORDS BUILD).
- D-5: 36 of 97 sidecar lines are artefacts or kit-internal literals (12 backtick-pair artefacts of prose, 2 chain inputs made by Step 0, 22 slot values / status-line forms / step words), each marked with a real count in the kit.

## Questions for Tuesday (each with a default)
- **Q-1 (slot COMMENT-128):** post TEXT-128 on PCOMP-128? Default HOLD; I recommend POST (the ticket's items (3) and (4) are done on main and it has no comment at all; C7 asks you to approve the body byte for byte by this slot).
- **Q-2 (Minor):** record (row #485 + one sentence in TEXT-128) rather than a new Task? Default RECORD, as written. If you want a ticket, it is a new kit line and a create; this kit has none.
- **Q-3 (slot ROW-FORM):** APPEND rows #484 and #485? Default NONE; I recommend APPEND.
- **Q-4 (slot STATE-479):** append the `Update 2026-11-15 (C-149)` sentence on row #479? Default NONE; I recommend APPEND (needs ROW-FORM APPEND).
- **Q-5 (slot REC-MERGE):** MERGE into root `main`? Default HOLD; I recommend MERGE, as B1552.
- **Q-6:** the "pg_restore 16.15" wording note is recorded as NOT RULED in row #485 (2). Default keep; strike item (2) before stamping if you judge it noise (the gate judged the words equal).

## UNMEASURED
- Any hosted state or deploy; "NOT DEPLOYED" is a repository fact only.
- The builder's test counts and the restore measurement of 2026-11-11: RELAYED, not re-run.
- Who merged PR #129 (the committer reads GitHub's own address; the record names no one).
- Whether the B1486 helper copies run cleanly after adaptation: not run (I did not execute another seat's helper; I named the one fault I can see by reading, line 31).
- The kits of the ten unnamed panes.

## Outside-the-fences disclosure
- Writes: only my kit, its `.measured` sidecar (via `stamp_check.py --init`, then filled by my `measure.py`), this report, and scratch files under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1576/`.
- Reads: the commission, DRAFTER_RULES.md, the B1552 kit, report, sidecar and project STATUS, the B1569 kit, its project STATUS, gate folder, the B1489 and B1509 kits (Jira sections), the Composer root record files (C-131, C-133, C-144, C-148 whole; rows #479, #481 tail, #482, #483; JIRA.md 1-8 and 52-57; history 1-13), `.tools/b1486/scripts/` (headers and `jira_write.py`), `.tools/b1552/scripts/textscan_b1552.py` (read, copied into my scratch by `cat >`), `model-routing.md`, `models_latest.json`, `brief_seat.sh`, `stamp_check.py`, the live seats' kits (two `grep -c` each), tmux pane names, `gh api -X GET` (about 20 calls), Jira GET (about 20 calls, every JQL `project = PCOMP AND ( ... )`).
- Hooks refused three commands and nothing ran from them: a `git symbolic-ref` (re-run as `rev-parse --abbrev-ref`), a `cp` whose source sat in the Composer tree (re-done as `cat > <scratch>`), and an unquoted `====` separator (re-run with `----`). No write reached any project.
- No `decision_queue.sh`, no briefs_staged, scoreboard, ledger, WEDNESDAY/FRIDAY tree, non-Datasec project, az, ssh, docker, npm, hosted host, mail, Jira write, GitHub write, or message to a human.

DRAFTED B1576: kit 101 lines, sidecar rc 0, questions 6
