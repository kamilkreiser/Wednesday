STARTABLE: YES

# B664 drafter report | SEAT-H23 | HPSM-POC | HPSMPOC-351 (drafted 2026-10-25, 12:4x AEDT, Sonnet 5.5, read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B664_SEAT-H23_hpsmpoc-351-ci-workflow-reader-test.md` (127 lines, shape of B652).

## BLUF
- One new branch `b664/hpsmpoc-ci-reader-test` off main `754bf1e7`; two paths: `infra/tests/test_ci_workflow.py` (new reader class for the SQL Server shard job) and `.github/workflows/ci.yml` lines 164 and 675 (comment-only, in place, 679 lines kept). Sonnet C2 (model-routing line 92), gate G2 tier 2 (line 109), round 0 of 2 on this class; launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- Nothing blocks launch: main is still `754bf1e7`; open PRs are #215 (`web/src/audit-dev.test.ts`) and #216 (`web/src/server/mock/attribution-preview.test.ts`), both share 0 paths with the lane; no `b664/*` ref; no pane or kit names H23; ports 9600-9609 free (the seat needs none).
- The "14 plants" are 13 semantic plants plus 1 equivalent edit (plant 14, a trailing word on a comment outside the allowed block). The kit makes the reader red on 01-13 and green on 14 (see D-3).
- CI pass predicate written into the kit: the reader runs inside the required `infra (Bicep validate)` job via `validate.sh:21` -> `test_security_baseline.py main()` (line 1556), which runs every `infra/tests/test_*.py` and passes only with tests green, `ResourceWarnings: 0` and `Files still open: 0`. `ci.yml` does not name `test_ci_workflow.py`.
- The audit comment at lines 391-393 (ticket item 3, finding FT8) is deliberately NOT in the lane; it waits for the audit-dev lane (PR #215) to land.

## Facts re-measured (instrument, control)
- main `754bf1e7f6eed2f140468dd283551eca1299d46e` by `gh api commits/main` and `git ls-remote origin refs/heads/main` (project clone). Control: `refs/heads/b629/*` prints 1 line (`ceac7406...`); `refs/heads/b664/*` prints nothing. `cat-file -t 754bf1e7` in the project clone now prints `commit` (the B652 kit said it was missing).
- Open PRs by `pulls?state=open`: 215 (head `afcedf03...`, `b652/hpsmpoc-audit-dev-older-rows`, 1 file `web/src/audit-dev.test.ts`), 216 (head `2e1c4ddd...`, `b651/hpsmpoc-nonascii-digit-exempt`, 1 file `web/src/server/mock/attribution-preview.test.ts`). Intersection with my two paths by `grep -c -x -F -f`: 0 and 0; controls: planted path 1, clean list 0. Branch compares agree. Code-scanning open alerts 0 (`length`; no positive control run).
- Blobs by contents API at `754bf1e7`: `ci.yml` `87d7590e...` (679 lines), `test_ci_workflow.py` `7569ef1b...` (170 lines, 9 `def test_`, counted by grep; Python 3.14.7 on this machine).
- Comment lines: `sed -n 164p` and `sed -n 675p` each match `^ *#` (1 each); a pattern count of 2 lines in the file holds a person or coordinator-seat name, at 164 and 675 (names not written in the kit or here). Control: 391-393 is a different block (record-entry citation, not a name).
- Shard job at `754bf1e7`: matrix `:175`, filters `:252` and `:255`, Feedback line `:256-257`, proof step `:274`, floors `:314`, aggregator `:353-365`. The exact strings the seat pins are listed as fact checks in the kit REFUSE section, each with a count and a no-such control.
- Plants: B638 STATUS lines 65-84 (14 rows, plant 14 equivalent); `c1-infra-readers-base-and-control.txt` last lines: reader rc 0 on all 14.
- Ticket: Jira GET with the project helper (`.tools/b467/jira.py`, imported in-process, token not printed), JQL `project = HPSMPOC AND ( key = HPSMPOC-351 )`: 1 issue, Backlog, Task, created 2026-10-25 09:59:58 (+1100), 0 comments, labels `b638-gate`, `b649-2026-10-25`, `test`.
- FT8: the ticket cites `B628_STATUS.md:163`; read there, it is numbered item 8 (the audit comment at 391-393). A grep for the string FT8 in B628 STATUS finds nothing (the id is the records seat's label, found in B649 and B653 STATUS and the ticket). So FT8 is the lines 391-393 item, not this lane's.
- Ports: `lsof -nP -iTCP:9600-9609 -sTCP:LISTEN` 0 lines; positive control (bind 9601 for 4 s) 2 lines. Word-boundary scan of non-`.pre-` SEAT kits of 10-24 and 10-25: hits only B608 (yesterday, finished). Live kits B650, B659, B660, B661, B662, B663: 0 hits. Panes: tuesday, MPS-G114, NexusAI-G113, HPSM-POC-G112, HPSM-POC-G111, Security-Composer-G110, NexusAI-M9, fleet-monitor. `SEAT-H23`/`HPSM-POC-H23` word scan of all kits: 0 (control: H22 hits B651/B652 kits).
- Load: `uptime` 4.55, 6.88, 8.03 at 12:47; not independent reads.
- Checks on main commit: 19 check-runs, 18 success, 1 skipped.
- Landing: CLARIFICATIONS.md line 138 records one head-pinned squash (precedent, not a written rule; the project CLAUDE.md prints nothing for squash/match-head); ruleset facts RELAYED from B638 Check 8d and the B652 kit. Quoted in the kit as such.
- Kit hygiene by program: 8 lines match the four-underscore pattern (7 slots + last line); 0 non-ASCII; 0 hits for the owner's name tokens and for the two record-entry ids.

## D-decisions (mine, for Tuesday to accept or change)
- D-1: Reader style is stdlib text/regex in the existing file's style (the file's own docstring says no YAML library on the runner), as a NEW class; existing 9 tests byte-equal.
- D-2: Two commits suggested (comment commit and test commit apart) so the gate reads the comment-only diff alone.
- D-3: The sweep said "red on each of the 14 plants it should catch"; the gate's table has 13 semantic plants + 1 equivalent. Kit: red on 01-13 (including the soft ones 01 timeout, 03 floor, 10 job `api` name, by pinning the file's own values so a legitimate change becomes a one-line data edit beside the `ci.yml` edit), green on 14. The pinned-values trade goes in FOR TUESDAY for the product owner.
- D-4: Complement proof by a small filter-grammar evaluator over sample names, plus a set comparison of namespaces; its limits to be stated in a comment.
- D-5: Part B proof program = 2 hunks at 164/675, every changed line a whole-line comment, comment-stripped remainders byte-equal, ruby YAML structure equal, 679 lines; five planted controls including a trailing `# v7.0.1` comment (a comment but not a whole-line one).
- D-6: Pane name H23; no ports; heavy lock only for the deploy-package run and repeats (the reader is milliseconds).
- D-7: Target READY 2 h, hard stop 3.5 h after launch (suggestion for the stamp).

## Q-questions for Tuesday
- Q-1: Do you want plants 01 (shard timeout), 03 (floor) and 10 (job `api` name) caught, or only the filter/proof/aggregator ones (02, 04, 05, 06-09, 11-13)? Default: catch all 13 (kit as written).
- Q-2: Should the seat be told to wait for PR #215 to land before the pair run? Default: no; the two lanes touch different paths and the comment edits move no line number (proved by the hunk program).
- Q-3: Landing wording: squash with `--match-head-commit` is the convention by one recorded precedent and the B638 gate's note. Default: you read the precedent before the merge and land it as in #213/#214.

## UNMEASURED
No python test, ruby, worktree, plant or mutant was run; no new test written. The runner's Python version; whether `test_security_baseline.py` runs without the Bicep binary; whether CodeQL analyses Python here; whether each soft plant can be caught without over-pinning; `git blame` of 164 and 675; the contents of the 14 plant files (only their one-line descriptions); whether `actionlint` is installed on the seat's machine (it printed not found for `which`, with no ruby-free control).

## Outside the fences
None intended. Read only: DRAFTER_RULES, B652 kit, the sweep rows, B638/B628/B649/B653 STATUS (grep and sed excerpts), the B638 evidence plant files, model-routing.md and models_latest.json (grep/sed), CLARIFICATIONS.md and CLAUDE.md of the project (grep), the project `.tools/b467/jira.py` header (read to use it; imported in-process, one GET, no token printed), `ci.yml`, the reader, `validate.sh`, `test_security_baseline.py`, `test_hidden_characters.py`, `test_resource_hygiene.py` via `gh api -X GET contents` into the session scratchpad. Not opened: decision_queue, briefs_staged, scoreboard, `_ledger.md`, any WEDNESDAY/FRIDAY tree, other projects. Two slips to disclose: my first `gh` call batch hit the no-cd hook (refused, nothing ran), and one `grep` of the kit printed two lines of quoted records text containing an em dash and an arrow, which I replaced with a paraphrase in the kit. The shell wrote scratch files (ci.yml, reader, jget.py, plant lists) under the session scratchpad only.
