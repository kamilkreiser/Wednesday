STARTABLE: YES (conditional on PR #134 having landed and the `#134 merge commit` slot being stamped; the kit refuses to start otherwise)

# B869 drafter report (kit: 2026-10-28_B869_SEAT-G192_nexusai-135-rd898-exact-label-gate-tier2.md)

## BLUF
Tier-2 gate kit for NexusAI PR #135 (RD-898, one test file, 46/13), seat Datasec/NexusAI-G192, ports 9870-9879, Sonnet (row G2, model-routing.md:109; id claude-sonnet-5-5 from models_latest.json:23). Shape copied from B865 (plumbing, lock tool, fence, landing) with the B853 mutant table as the baseline. Differences from B865: the base is main-after-#134 (a stamp slot `#134 merge commit`, refused if not a 40-hex sha), main moving by exactly #134's two paths is EXPECTED, and #134-not-landed is a STOP with one question. Slot count: 8 lines carry four underscores (7 slots plus the last line); non-ASCII 0; at-sign token count 0 (all three measured by program on the written file; the first two controls are the kit's own REFUSE 1 wording, not re-run here).

## Facts re-measured (instrument, time 04:28-04:40 AEDT)
- `ls-remote` + `gh api -X GET` under the NexusAI GH_CONFIG_DIR: main f4ea31c9 (unchanged), #135 head = branch = 4d466a9a, `refs/pull/135/merge` 356293e4 (parents f4ea31c9, 4d466a9a; tree 7bb21fb6; this is the OLD merge ref, the kit says so and tells the gate to re-read it). #134 head 44f6f5eb, merge ref 5cc31e8c; b869* absent. Open PRs: #134, #135. PR #135: open, not draft, commits 1, changed_files 1, +46 -13, mergeable_state `blocked` (build running). Control for ls-remote: b855/b856 branches print.
- `pulls/135/files`: one path, blob 5710f03c; `pulls/134/files`: the rd891 test and counts file; blob of rd892 test at main e266ef36, of testing.js 7fa16e85 (both read via contents API).
- Check-runs on the head: CodeQL, three Analyze, scan, audit-production-deps success; build in_progress. Analyses for the PR ref: three rows at 4d466a9a, results_count 0, error empty; open alerts 0 (list length; the alerts/9999 404 control was NOT re-run by me, only restated from the sibling kit).
- Product line: static/js/testing.js:41 at main read in full (the mutant anchor). Head test file read from the API (267 lines): EXTRA_SLOTS line 56, D1 161, D2 185, F1 212 with the exact assertion at 224; the old loose assertion read from the main blob at line 191. Non-ASCII in the head file 0 (the grep -P control failed on macOS grep; I counted with a different pattern: the one hit set was only in my kit text, since fixed).
- Round count: verdict lines read over Briefs/*_STATUS.md: B853 = GO WITH FOLLOW-UPS round 1 of 2 (PR #132); NO GO census = B592, B647, B667 (other classes); B865 PENDING; no verdict names #135. Hit list for the frame: B854, B855, B856, B865.
- Ports: lsof 9870-9879 rc 1 (no bound-and-freed control run). Word-boundary scan (python3 -I, 103 non-.pre- SEAT kits of 10-27 and 10-28): 987x hits exactly B856 (closed builder's own) and B862 (names it as a partner block); control 986x hits B855, B862, B865. Panes: M52, G186-G190 and tuesday and fleet-monitor; none named G192; session-tools/b869 and worktrees/b869-* absent.
- Launch form: copied from the B853 stamp (launch_when_cool.sh at 2_Project_Files/tuesday/tools/, existence verified by find) with WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet inside the quotes, as B865 stamped.
- Load1 6.02 / 7.03 / 8.12 at 04:28.

## D-decisions
- D-1 Tier 2 (G2) stands: no product byte changes; hand-up rule carried.
- D-2 Mutant naming GL1-GL15 (GL4b added for the builder's trim-after-upper shape). New shapes beyond the builder: zero-width space (GL9), tab (GL10), `|| 'unknown'` (GL11, the older no-new-word pin), toLowerCase (GL12), toLocaleUpperCase('tr') (GL13, may be NOT-A-MUTANT under ICU), text dropped (GL14), widening probe (GL15, a Note). Grading: a filler or case shape left green is a Major; this is a stronger line than B865's GM6/GM10 Notes because the PR's whole claim is those pins.
- D-3 Tamper controls: GT1 puts the old loose assertion back (from the main blob) and runs GL1, GL3, GL9; GT2 removes the accented rows and runs GL5 (shows which row carries which mutant; a table, not a finding); GT3 a wrong expected padded label (must go red).
- D-4 The B853 matrix, GL7 (guard deleted, 14) and GL8 (angle brackets, 9), are kept as regression columns.
- D-5 Sequencing logic in REFUSE 2, 6, C2 and the Landing: compare f4ea31c9...M134 must be exactly #134's two paths (expected); a later move on rd892 test, static/js/**, the page, helpers, verify-suite.sh, build.yml, package*.json, counts file, or the test-text walkers (local-date-single-definition, rd429-nul-byte) is a STOP; other paths continue. Pair on the merge result must be 5223/310.
- D-6 The base tree runs the HEAD's test file over main's product (the pins do not exist in the old file), plus one pristine run of the old file first.
- D-7 The PR body's sentence "Verify at the head: 5220 tests" is true on the old main only; graded as a Note about text (C10), not a defect.

## Q-questions for Tuesday
- Q-1 Fill the `#134 merge commit` slot from `pulls/134` merge_commit_sha at launch. Default: do not launch until #134 has landed.
- Q-2 Hard stop: drafter suggests target 150 / hard stop 240 minutes after the gate's Step-0 date (jest lock queue: G188 and M52 may hold tickets). Default accept.
- Q-3 Is GL13 (Turkish locale) worth a ticket if ICU makes it a non-mutant? Default: report NOT-A-MUTANT and move on.
- Q-4 The B853 matrix said GL1-GL9 shapes; the PR body's "14 and 9" claim is graded as a Major if different (G-2). Default as written.

## UNMEASURED
Lock tool and fence sha256 not re-hashed by me (relayed from the B865 stamp; the kit's REFUSE 4 re-hashes). alerts/9999 and lsof bound-and-freed controls not run. The CI build's step predicate (build.yml / verify-suite.sh line numbers) is relayed from the B865 kit, not re-read; the kit tells the gate to print the lines it reads. I did not read B853 STATUS beyond its last line and verdict lines. Deploy-demo workflow facts relayed. node v26 vs 24 unmeasured by anyone. B862's branch not on origin at last read of the PR lists only (not re-read by ls-remote for b862*).

## Outside-the-fences disclosure
Nothing written other than the two files; one scratch file written under the session scratchpad (head.js, testing.js copies from the API); no cd, no fetch/clone, no HTTP to hosted hosts; gh used with -X GET default reads only under the NexusAI GH_CONFIG_DIR; no decision queue, no ledger/scoreboard/briefs_staged read; I read the sibling B865 kit, the B853 kit (grep lines), the B856 STATUS whole, DRAFTER_RULES whole. One tool-hook note: a first command was refused for an unquoted `==` separator and re-run with `---`. The Write tool converted my escape sequences into real non-ASCII characters (as the builder's STATUS also warned); I fixed them by program and the kit now reads 0 non-ASCII bytes.
