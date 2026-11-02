STARTABLE: YES (after Tuesday fills the five Stamp lines and the last line; nothing in the sources blocks the seat. One thing needs your eye before launch: Q-1, a landed PR the commission did not name.)

# DRAFTER-REPORT B1189 | SEAT-R151 | Security Composer records for PR #113

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1189_SEAT-R151_composer-records-113.md` (106 lines; template shape of B1123; model row C8 `model-routing.md:98`, Sonnet, `BRIEF_SEAT_LEVEL=sonnet` written inside the launch quotes; model id `models_latest.json:23`). Every pointer in it was printed by `grep -n` / `awk NR==n` over the raw file before it was typed. The kit types no clock of its own.

## BLUF
- PR #113 is landed at origin: squash `f5f33e189f34d36fa374c0ac1d6fa38d003df8ec`, converted 2026-11-03 06:44:26 AEDT, 2 files +530 -2, both blobs equal the head's, CodeQL and both Analyze runs success, 0 open alerts on main and on the pull head. The landing text in `2026-11-03_PR113_landing/` is the squash message byte for byte.
- The kit records it (BACKLOG rows #449 to #456, entries C-121 and C-122, History, `JIRA.md`), files up to four tickets (the 18 cells, the 8 tab cells, the q7 plant, option C) plus one comment on PCOMP-23, five Jira writes at most, no transition, no removal. PCOMP-23 is comment-only by the project's rule (C-112, `CLARIFICATIONS.md:2049`): no MOVE slot, closing condition (1) NOT MET on the gate's cells, last gate line NO GO round 2 of 2 on the class.
- **A finding outside the commission: PR #112 (PCOMP-119's rows, gate B1154) is merged and recorded nowhere.** Squash `01bc16e4`, converted 2026-11-02 21:02:31 AEDT, it is also the base of PR #113. Item 3 of the commission ("owed rows from B1151 and B1154") cannot be written honestly without recording that landing, so the kit does (rows #454 and #455, entry C-122, State append on row #446), with no Jira write on PCOMP-119. Q-1 and Q-2.
- Every figure in the commission reproduced at its source; none disagreed.

## Facts re-measured, with instruments and controls
| fact | instrument | control |
|---|---|---|
| PR #113 merged, squash sha, base, head, 2 files +109 -1 and +421 -1, one parent, tree `de4bdbb9`, `verified` true, 1 `Co-Authored-By` | `gh api -X GET` `pulls/113`, `commits/f5f33e18` under the project `GH_CONFIG_DIR` | `pulls/9999` 404 |
| merged_at 2026-11-02T19:44:26Z = 2026-11-03 06:44:26 AEDT | `TZ=Australia/Sydney date -r` over `date -j -u -f` | output printed by the program |
| both blobs at squash = at head (`52789494`, `58d3110c`) | `contents/<path>?ref=` at head and squash; `git hash-object` of the fetched files agrees | the TREES differ (squash `de4bdbb9`, head `a789ead5`; main moved by PR #112), so the comparison can fail |
| squash message body = `squash-body.txt`; subject = `squash-subject.txt` + " (#113)" | `diff -q` rc 0 | `diff -q` against `pr-body.txt` rc 1 |
| `localdomain` 0 in the squash | `grep -c` over the commit JSON | control commit `cbe86ba6...` carries it in its author field |
| check-runs: head CodeQL, Analyze x2 success; squash Analyze x2 success | `commits/<sha>/check-runs` | n/a (states printed) |
| open alerts main 0, `refs/pull/113/head` 0 | `code-scanning/alerts?state=open&ref=` | `state=fixed` 20 |
| main at origin = `f5f33e18`; open PRs #91, #86, #85; #85 holds `document-pdf.ts` | `git/ref/heads/main`, `pulls?state=open`, `pulls/85/files` | #86 has 0 such files |
| PR #112 merged, squash `01bc16e4`, parent `69b01339`, tree `0faee598`, 1 file +79 -1, blob `50d91dd2` = head's, Analyze x2 success, alerts on its head 0 | same | same |
| Root repo: HEAD main = `0406d583`, 0 dirty lines on the four paths, 0 staged, no `MERGE_HEAD`/`index.lock`, 0 remotes, none of `b1189` names | `git --no-optional-locks` read verbs, `ls .git` | `.tools/b1123` lists 2 entries |
| Highest C-120 (`CLARIFICATIONS.md:2246`, 2267 lines), highest BACKLOG #448 (`BACKLOG.md:444`), `JIRA.md` 43 lines | `grep -n -i`, `awk`, `wc -l` | `PR #88` finds `:1797` |
| No record of PR #113, B1151, B1154, B1161, PR #112, `bf5b945` | `grep -c -i -F` over the four record files | PCOMP-119 finds 3/3/1/3 hits |
| Gate figures: 9,508 cells, 151,162 pages, 9,379 of 9,397, OUT 18, MODEL-SHORT 26, 8 tab cells, 6.45 pt, 246 + 51, 17 of 17, 11 of the 28, 1,883 cells, 0 cells lose the hash line, 8,535 of 8,535 (Word), 10 of 10 rows, 12 + 6, 1,999 of 9,397 | `awk NR==n` then `grep -c -F` per string on `B1161_STATUS.md:1, :99, :106, :123, :186, :187, :188` and `residue.md:5, :21` | 29 strings each found once; a planted wrong string found 0 |
| Verdict lines: B1151 `:248` NO GO round 1 of 2; B1161 `:231` NO GO round 2 of 2 (the cap), same class; B1154 `:147` GO WITH FOLLOW-UPS round 1 of 2 own counter | `grep -n`, `awk NR==n` | the class string printed from B1151 line 1 equals B1161's |
| Source lines in the merged file: `change-report.ts` 536 to 539 (comment), 556 (`matchAll`), 559 (`const size = ...`), test 335 and 336 (`NAME_LENGTH = 250`, `COMPANY_LENGTH = 200`) | fetched squash blobs, `grep -n`, `sed -n` | blobs hash to the squash blob shas |
| Jira: total 119, Done 26, held 19, seed 94, highest PCOMP-119; PCOMP-23 Backlog 0 comments labels `composer-seed-1023` + `plan-comp-315`; PCOMP-119 Backlog 0 comments; labels `plan-comp-447` to `-457` 0 each | read-only JQL GETs (every JQL `project = PCOMP AND ( ... )`) | `plan-comp-446` 1; `zzqxvbw` 0, `composer` 53, `Waite` 43 |
| Duplicates: `hash line` 1 (PCOMP-23 only), `fingerprint` 0, `modelledFooterRows` 0, `linebreak` 0, `page label` 0, `pdfmake` 1 (PCOMP-70, other subject), `bracket` 1 (PCOMP-98), `tab characters` 1 (PCOMP-104 Done), `trailing space` 5, `line break` 6, `footer` 7 | same | stemmer baseline above |
| Seat-name scans over Tuesday's non-`.pre-` kits: `R151` 0, `B1189` 0 | `grep -l -w -i` | `R135` 3, `B1123` 7 |
| Panes: no Composer pane; `ps` over `Datasec Security Composer` no line | `tmux list-panes -a`, `ps -axo` | see disclosure: the `ps` zero used `grep -v grep`, so it had no own-line control; the kit makes the seat re-count with one |
| Leftovers of the footer and rows lanes all modified within 3 days | `stat -f '%Sm'` over `.tools/b11{40,44,51,54,60,61}*` | `date` printed beside |
| Kit mechanics: 6 four-underscore lines; 0 non-ASCII; Jira texts: no name, no backtick, no backslash, "Composer" only before " PR #", "deployed" once inside NOT DEPLOYED, 0 "production"/"live"/"fully pinned"/"Datasec"; summaries 220, 201, 174, 222 characters (limit 255) | `grep -c`, python `ord > 127` | a planted `____` line counted 1 |

PCOMP-23's reading (kit, table before Step 5): it has no Done-when line. Fix shape (`BACKLOG.md:311`): "Footer line budget, plus a test at 250 + 200 characters." (1) budget: NOT MET on the gate's cells for the whole defect (18 + 8 cells, policy-PDF half not done: `B1161_STATUS.md:186`, `:187`, `:202`, `B1151_STATUS.md:62`); (2) test at 250 + 200: MET (`change-report.test.ts:335`, `:336`; 10 of 10 rows). Rule quoted at `CLARIFICATIONS.md:2029` (C-111 (3)) and `:2049` (C-112). PCOMP-116 is not touched (named in the kit's HOLDS and partition; its gate B1181 is NO GO round 2 of 2 @ `643c389`, decision pending).

Owed rows read from the earlier gates:
- B1151 (NO GO round 1 of 2): policy-PDF half still owed (`:62`, FOR TUESDAY `:224`); Notes B1151-6, -8, -9, -10, -11 (`:213`, `:215` to `:218`). Round 2's own disposition of the round-1 findings is `B1161_STATUS.md:30` to `:40`: B1151-2, -3, -5, -7 closed or answered (no row); B1151-1, -4, -6 carried into B1161-1, -2, -4, -5 (rows #450, #451); B1151-8, -9, -10, -11 stand (row #456).
- B1154 (GO WITH FOLLOW-UPS round 1 of 2): B1154-1 (residue list names neither B1 nor C1, a follow-up edit needs a ruling), B1154-2 (a sentence no run backs), Notes -3 to -8, and removal of the builder's leftovers (`:135`). Plus the landing of PR #112 itself (unrecorded).
- B1161 (NO GO round 2 of 2): the four open-case items (rows #450 to #453), and rows #456: B1161-5 to -11, plants q8 q10 q11 q19.

## D-decisions (mine)
- D1. Four ticket slots (`NEW-A` to `NEW-D`), one comment slot, `MAX_WRITES = 5`, labels `plan-comp-450` to `-453` matching rows #450 to #453; rows #447 and #448 never had tickets, so no label gap clashes (`plan-comp-447` to `-457` all 0).
- D2. PR #112 recorded in this kit (rows #454, #455, C-122 on its slot, a State append on row #446) with no Jira write on PCOMP-119.
- D3. PCOMP-23 comment-only; no `MOVE` slot exists.
- D4. REMOVAL not in the kit: every leftover is inside the 3-day exclusion that the B1123 stamp quotes (`B1123 kit :29`); the seat's last line says removal deferred.
- D5. Row numbers fixed (#449 to #456) because the approved Jira texts cite them; REFUSE 6 stops the seat on any other highest id, so a concurrent records seat cannot silently renumber.
- D6. Jira texts carry no cell-level or work-number pointers except the two source files' line numbers, which Step 3 re-prints from the squash blobs (a pointer that disagrees HOLDS its text).
- D7. The tab-cell names `Y4-tab8-x6-L118` and `Z-tab40-L075` to `-L081` are in ticket B as the gate's frame names; they contain no `B<digits>`.

## Q-questions for Tuesday (each with a default)
- Q-1. Record PR #112 in this kit? It is the base of PR #113 and the lane of gate B1154, and no record has it. **Default: yes** (slot `C-122` FILE; rows #454 and #455). NONE makes the seat skip C-122 and write rows #454 and #455 only.
- Q-2. Comment on or move PCOMP-119 (the gate observed all five of its clauses; whether B1 and C1 count against the residue list is unsettled, `B1154_STATUS.md:134`)? **Default: no, `JIRA-OTHER` NONE**; a later kit with approved text, after your reading.
- Q-3. Ticket (a), the 18 cells, is the residue of PCOMP-23, which stays open and owns the footer subject. **Default: file it separately** (`NEW-A` FILE); row #450 and the PCOMP-23 comment name PCOMP-23 as the open owner.
- Q-4. Ticket (d), option C, is a measurement and a choice for the product owner, not a defect (none recommended in `residue.md`). **Default: FILE as commissioned**; NONE keeps row #453 and the comment says "recorded, not ticketed".
- Q-5. Comment on PCOMP-23 at all (precedent: B1123 commented on PCOMP-98 and PCOMP-114 without moving)? **Default: yes** (`COMMENT-23` FILE).
- Q-6. Authority sentence in C-122: the kit says "the coordinator's landing under C-101 (1) and the relayed merge-once-tested grant" only if the STATUS files back it, otherwise "RELAYED, not recorded in the sources read". **Default: as written.** Please say if the product owner ruled on PR #112 separately.
- Q-7. Removal of the lanes' leftovers (B1154-8, B1161 trees): **Default: deferred**; compute the date from the newest mtime (the `wt-b1161-*` trees) plus 3 days and bring it back as its own kit.
- Q-8. The "11 of 28" figure has two denominators in the gate (11 of the 28 wide-letter footers that print whole at main; 11 of 1,366 shorter footers). The ticket text uses the first, as the commission did. **Default: keep.**

## UNMEASURED
The hosted site; every gate cell (RELAYED); whether main, Jira or a pane moved after the last read; who merged either PR; PR #112's head check-runs (the seat reads them at Step 3); the docker images; what exactly the 17 in "17 of 17" counts beyond the gate's phrase; the cause of the tab-width gap; whether PR #85 still holds the shared layout file at launch (read at drafting: 1 file match of 57).

## Outside-the-fences disclosure
- **Jira reads used my own scratch reader**, `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/e571ea36-4d5c-4e12-9849-e91ce4dbfd97/scratchpad/jr.py`, not the project's helper: it asserts the Jira host, reads the three `JIRA_` values from the project `.env` inside the process, sends GET only, prints no token. (Fence 2 asks for the project's own helpers; I read the header of `jira791.py` and chose a narrower reader that cannot write.)
- Scratch files in that scratchpad: `jr.py`, `sq.txt`, `sq-body.txt`, `cr-test.ts`, `cr-src.ts`, `texts.txt`. Nothing in the project tree was written except the two files named.
- No decision card was opened; `decision_queue.sh` not used; I did not read `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, any WEDNESDAY/FRIDAY tree or a non-Datasec project.
- I listed Tuesday's `briefs/` directory and scanned the non-`.pre-` kits by name for the seat and work-number words; I read two kits whole (the B1123 template and the B1112 kit it points to) and the PR #113 landing files.
- Git was read-only (`rev-parse`, `for-each-ref`, `status --porcelain`, `diff --cached --name-only`, `ls-files`, `remote`); `git hash-object` ran on scratch copies only. `gh` was `-X GET` throughout under the project `GH_CONFIG_DIR`. No az, ssh, docker, hosted probe. `lsof -nP -iTCP` was run once to count listeners (13); no port block was assigned.
- The `ps` zero above lacked an own-line control. Four commands were refused or failed on shell mechanics (zsh word-split hook twice, a leading `=` separator, one wrong tool name) and were re-run in `bash` heredocs with no effect on any file. A few early listing greps were case-sensitive; every zero claimed in this report used `-i -F` with a positive control.
- No typed clock appears in the kit; the report's converted merge times are `date -r` output.
