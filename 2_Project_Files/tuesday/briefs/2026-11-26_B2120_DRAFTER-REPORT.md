STARTABLE: YES

# B2120 DRAFTER REPORT (Sonnet drafter, read-only, for Tuesday s329): Composer records pass for pull request 134 (PCOMP-23 policy PDF half), seat R331

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2120_SEAT-R331_composer-records-pr134.md` (86966 bytes; ten Stamp slots and the last line as four underscores, 11 such lines; `READ-WHOLE-BY-TUESDAY: ____` last). Sidecar: the same name plus `.measured` (188 claims, 188 lines, `stamp_check.py` exit 0; many of the 188 are instruction text or between-span fragments of the checker's backtick pairing and say so). `date` printed 11:28:07 at the start, 11:38:05 and 11:38:21 around the Done-when run, 11:39:05 and 11:39:17 around the repository, record and Jira run, 11:43:57 at the pane read. Seat id: **R331** (R329 and R330 taken; the sibling drafters took R332 for B2119 MPS and R333 for B2118 NexusAI at 11:41; the three ids are distinct; the file names of the 30 other SEAT kits of 11-25 and 11-26 carry R331 in 0 files).

## BLUF
PR 134 is on main as the squash `3222c898f6b6057edd91b7d137a4b7d56cf34791` (merged 2026-11-25T23:31:21Z = 2026-11-26 10:31:21 AEDT; one parent d06508f8; tree 340948986b3a equal to the reviewed head; three files +160 -2). It is on no record. The kit is the B2036 form for it: ONE Jira comment on PCOMP-23 (TEXT-23, 2002 characters, scanner 0 hits in both variants) and at most ONE move to Done, ONE C-entry (C-161 by program), TWO BACKLOG sentences (rows #315 and #456), one JIRA.md bullet, one history entry, one commit, one merge. The move is gated on a seven-row Done-when table that read MET on live reads. The review's six findings F1 to F6 go to ONE destination: one sentence on row #456; nothing is ticketed. Nothing deploys and no text says a deploy is due.

## Facts re-measured with instruments (each is in the sidecar with its source)
- Code main `3222c898`, open PRs 0, newest PRs 134 133 132 closed, `compare 3222c898...main` identical, check runs on the squash `Analyze (csharp)` and `Analyze (javascript-typescript)` success, on the head 75d27893 also `CodeQL` success (3 runs), analyses of main at the squash js 0 and csharp 0, open alerts 0 (`gh api -X GET`, account kamilDatasec, control `pulls/9999` 404). The three blobs, the four release blobs (equal at d06508f8 and 3222c898, unequal at b4681297 as the control), `document-pdf.ts` blob equal at both.
- Commission's figures all agree with source (tree 340948986b3a, both CONTENT_HASH blobs 23cd95f5 and 09d597c6, main analyses 0 and 0, alerts 0). The squash subject equals the gate's `squash-subject.txt` with the number, its body equals the gate's `squash-body.txt` after whitespace collapse, 1 trailer.
- PCOMP-23 (Jira GET, control PCOMP-9999 404): Bug, Backlog, labels `composer-seed-1023` and `plan-comp-315`, comments 40721 and 40958, 0 changelog, transitions 11 21 31 41, no line headed Done-when (control: the PCOMP-12 comment 40957 holds one). PCOMP-120, 121 and 122 Done, PCOMP-123 Backlog; PCOMP-130 Done (B2036's). Project: 130 issues, Done 55, not Done 75, `held` 19, seed marker 94, `updated >= "2026-11-26"` 0.
- Root records repo: main `fa1538060d9518f03e0af372652c11f84850ec85` (the B2036 merge), no remote, the four files clean; highest heading C-160 at `:2996`, so C-161; BACKLOG 486 data rows, rows #315 `:311`, #453 `:449`, #456 `:452`, #496 `:492`, each 5 fields; JIRA.md 65 lines (B2036 bullet at `:65`); history B2036 entry at `:3`. Literals of the landing count 0 in all four files (controls PCOMP-130 12/2/7/10 and C-160 2/1/1/4).
- Pointers by `grep -n` over the raw files at the squash: `change-report.ts:750`, `policy-document.ts:10` and `:836`, test file `:25`, `:26` and five indented cells at `:59 :80 :106 :116 :126` (`^[[:space:]]+it\(` 5, column-1 `^it\(` 0; the bare substring `it(` counts 6 because line 121 holds another word).
- Done-when rows 1 to 7 MET (`proto_donewhen.py`, 11:38:05), each with a control that can fail; 17 text facts OK, `merged_at` converted to 2026-11-26T10:31:21+11:00 (the UTC date is the 25th: both clocks are in TEXT-23).
- Prototype of the helper edits (counted replacements of B2036's `jira_write.py` and `run_controls.sh`): 11 negative guard controls exit 1 before any request, 4 positive pass, `--dry` printed 6 GET, 0 POST, payload sha256 `cfc840a4014f06b1a9287d92db3e025daa2bdec989e2c75efbbf3ec96f926c86`.
- Scanner: the project's `textscan_b1808.py` (B2036's copy, sha256 prefix 47334987c771c170) over a name list built into scratch (8 tokens): 74 planted controls fired, 0 did not; TEXT-23 0 hits both variants; 13 record spans x 12 placeholder variants (156 scans) 0 hits at the final wording. A first run printed 36 hits (capital `Nothing was deployed` in two row sentences; `a later deploy` in SETTLED-134) which I reworded before the stamp.
- Records prototype on scratch copies: C-161 entry 15 lines in C-160's shape, 9162 bytes added, ASCII, 0 pipes, old bytes a strict prefix (`git diff --no-index --numstat` 15/0); BACKLOG rows #315 and #456 each a strict prefix, 5 fields, exactly 2 changed lines, 486 rows (numstat 2/2); control: a planted extra-pipe copy of row #496 reads 6 fields.
- Span sha256 prefixes (final kit): TEXT-23 219c867ae7c69e8a, TOPIC-134 bd5f282637762844, AUTH-134 79e937f9e619dd34, QUESTION-134 89f7f712caf9ce76, SETTLED-134 98e3f0bd01d87894, REVIEW-134 6ad2f8f33429cd4d, TICKET-134 bd4327130e7ba29f, OPEN-134 d7cb4bccbd234315, PERMITS-134 c738d0f14da9c989, FORBIDS-134 1ad6c44a97812610, SUPERSEDES-134 28638f13cd42bc11, LANES-134 5b31a2aed739ad34, ROW-315 405b38a4c4530e1f, ROW-456 26fe1f1013a1e4fe.

## D-decisions (the drafter's, each open to Tuesday)
- D1 The comment says nothing about who decided and nothing about deploys beyond the move sentence: the project's Jira text rule bans the words coordinator, product owner and deploy; the decider is named in AUTH-134 and the "nothing was deployed" statement lives in the C-entry and rows. (FOR-RECORDS item 1 asks for "decided by the coordinator" and "nothing deployed" in the comment; the rule wins.)
- D2 The review's differences from the build (the host-derived PDF hash prefix of the build kit's FACT 9 does not reproduce in the CI image; the claim holds) is carried in REVIEW-134 plainly, as the gate says.
- D3 F1 to F6 appear in the C-entry by count and grade only; their substance is ONE sentence on row #456 (the row that already holds the earlier footer review's Minors and Notes; `B2117` counts 0 on the BACKLOG before). No new row, no ticket (FOR-RECORDS item 4: no ticket by themselves).
- D4 Row #315 (PCOMP-23's own row) gets the state sentence; PCOMP-123 (row #453) and the ticket are named, not touched.
- D5 PCOMP-123 is not commented (its own description and row stand; FOR-RECORDS item 2).
- D6 Dates: every text gives the project's date (2026-11-26) with the UTC clock beside it, because the merge crossed midnight UTC.
- D7 Helper edits are by counted replacement on B2036's `jira_write.py` (label compare becomes two labels; newest comment guard 40958; two comments), fixing nothing else; the seat's pointers are printed by line.

## Questions for Tuesday (each with a default)
- Q1 Does PCOMP-23 move to Done on this landing? Default: YES, slot MOVES `PCOMP-23`, only if the seven-row table reads MET by program, recorded as the coordinator's reading (no Done-when line exists; comment 40721's two clauses are both met; PCOMP-120 to PCOMP-122 are Done; PCOMP-123 is an owner's choice that loses no hash line). Alternative: `NONE` (the comment then ends "Left in Backlog at this stamp.").
- Q2 Where do F1 (Minor) and F2 to F6 (Info) live? Default: ONE sentence on row #456, no new row, no ticket. Alternative: F1 (the Word footer clipped too) as its own row or Task.
- Q3 STATE-ROWS: append a sentence on both rows #315 and #456? Default: `APPEND` (2 changed lines). Alternative: `NONE`, the C-entry alone.
- Q4 Model and gate: Sonnet seat (routing rows C7, C8, G3 at `model-routing.md:97`, `:98`, `:110`; model claude-sonnet-5-5, `models_latest.json:23`), no gate (records only, as B2036). Default: Sonnet.
- Q5 REC-MERGE: `MERGE` as B2036 did (one commit, one `--no-ff` merge, no remote). Default: `MERGE`.

## Inputs of each chain step (each from an EARLIER step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| 0 | the kit, `.tools/b2036/scripts/*` (read-only), the four record files, the gate folder | present at drafting |
| 0 (copies) | `jira_lib`, `jira_write`, `jira_readback`, `jira_counts`, `run_controls.sh`, `build_names`, `textscan_b1808`, `rules_b2036`, `fills_b2036`, `spans_b2036`, `scan_b2036` | `.tools/b2036/scripts` |
| 1 | gh GETs, Jira GETs, pickup line 9, raw files at the squash | present |
| 3 | spans (kit), `names.json` | the kit; Step 0 build |
| 4 | the raw test and source files, VERDICT.md, Jira GETs, `payloads.json` input spans | Step 1 |
| 4 (dry) | `payloads.json`, `movechecks.json`, `jira_before.json` | Step 4 itself, before the dry run |
| 5 | `payloads.json`, `movechecks.json`, the dry run | Step 4 |
| 6 | comment id, move result, C number, date, the four record files | Steps 0 and 5 |

## UNMEASURED (a stamp must know)
- Never run on a real output: `--apply` and `jira_readback.py` (needs an apply log), the seat's own `movechecks_b2120.py`, `prior_work_b2120.py`, the records script and its check, the JIRA.md bullet and history entry scans (the seat builds and scans them), the commit and merge, the identity prints, the pane checks (no Composer pane exists), the in-project `names.json` build. The move (transition 41) was read as available and never posted.
- The review's test, mutant, probe and byte numbers are RELAYED; this pass ran no test, build, image or hosted request. What the demo runs is not known and no text says.
- The BASE slot facts are 11:39 reads: root main fa153806, code main 3222c898, PCOMP-23 two comments; a launch after any move re-measures.
- Check runs on the squash list only the two Analyze legs (the CodeQL check run belongs to the head); main's code-scanning analyses at the squash read results 0 for both languages and alerts 0.
- Word's own layout, a four-digit-page policy PDF and a non-bundled brand body font are unmeasured by the review and say so in the texts.
- `stamp_check.py` passes, but 67 of the 188 sidecar lines are marked instruction or between-span (`/usr/bin/grep -c -E 'INSTRUCTION|NOT A LITERAL|NOT A MATCHED'` prints 67); Tuesday should spot-measure five real ones (e.g. `723ae4e9`, `e1165e8c`, `0e5dd449`, `5eb4abce`, `a8302d64`).

## Checks of the kit never run on a real output
The STOP-severity text checks (JIRA TEXT RULE, records rule, DEPLOY WORD CHECK, marker count, Done-when table, guard controls, BACKLOG and C-entry builds) were each run once on prototype output with their controls firing (scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s329/d2120/proto/`). Not run: the apply and read-back, the seat's own check scripts, the commit and the merge.

## Outside-the-fences disclosure
- Writes: the kit, its sidecar, this report, and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s329/d2120/` (`proto/` with byte copies of B2036's helper scripts and counted-edit prototypes, `raw/`, saved Jira texts, `facts2.out`, `_quarantine/` holding four earlier drafts of the sidecar, MOVED there and not deleted). I claimed R331 early with a one-line stub at the kit path and overwrote it with the kit.
- Read-only uses of the Composer project: `4_Credentials/.gh-config` (gh GET), `4_Credentials/.env` through the project's own `jira_lib.py` imported by `importlib` (nothing printed), `.tools/b2036/scripts/*` and `.tools/b1808/scripts` (copied or read), the four record files, `CLAUDE.md`, the B2036 and B2113 STATUS files. Tuesday's tree: the commission, DRAFTER_RULES, the gate folder, the B2036 kit and its sidecar, model-routing lines, `models_latest.json`, `stamp_check.py`, `brief_seat.sh` line 31, pickup line 9 only. `tmux list-panes -a` and `lsof` (a count) read.
- No Jira write, no GitHub write, no hosted request, no card store, no `decision_queue.sh`, no az, ssh, docker, npm, node, no mail or message, no other seat's tree beyond reading the two sibling kit names, nothing deleted. One call of mine was refused by the zsh word-split hook (a run of equals signs as a separator); it ran nothing.
