GATE B1896: GO WITH FINDINGS @ 48134ee on main 9c9a721

Gate B1896, tier G2, one Sonnet reader (claude-sonnet-5-5), 2026-11-22. Head 48134ee03d1002febea0a74f797313970fbc9549 (one parent, 9c9a72199dca98026b5acab7020c409ae47db39f); branch `b1895/mps-infra-430-433` and main both re-read by `gh api -X GET` at the gate (main unmoved, 0 open pull requests, 0 open code-scanning alerts).

## Grade
GO WITH FINDINGS. No weakened or skipped test, no template or behaviour byte changed, no red, no scope breach, and no acceptance line claimed met that is not (the one line that is met only in part, MPSCALC-431's first-failure line, is stated plainly by the seat and by Stamp S5). Findings are records and text only (F1 to F3 below).

## Rule (1): the diff is the frozen text
- `apply_edits.py` cut from the kit by line range (lines 37 to 240, not retyped) and run on a copy of the base tarball: blobs after `6486350d718c6c720b2989602cccd6d9df9f9d6a` (test_infra.py) and `22322327ddc2dcb13f57b28b71a2c27187a4d80c` (validate.sh), the prototype's. `cmp` of both outputs against the head tarball's files: IDENTICAL, byte for byte. `git hash-object` of the head files prints the same two blobs.
- `diff -rq` of the whole base tree against the whole head tree names exactly two files. numstat `106 9` and `1 1`. validate.sh diff is one removed and one added line (`step 3` to `step 2`), mode stays 100755, size 1655 both. GitHub's commit view: files exactly those two (106/9 and 1/1), one parent, author and committer the same Datasec address, message as the kit's body, ending `Co-Authored-By: Claude Sonnet 5.5`.
- scans.py: 107 added lines, 0 non-ASCII, 0 Cf, 0 GUID, 0 hosts, 0 tabs, name scan 12 quiet and 12 controls fired. No template, README or script-behaviour byte.

## Rule (2): re-runs in the gate's own scratch copy (BICEP = the project's 0.48.1 binary)
- `test_infra.py`: Ran 49, OK. `test_validate_script.py`: Ran 6, OK.
- `red.py`, base tarball vs head tarball, a fresh scratch folder: 31 labels, every line MATCH, `labels 31 | DIFF 0`, no `Ran 0 tests`.
- `check433.py`: base exit 1 (`header names: ['3']`), head exit 0 (`['2']`). `grep -rci -F 'README.md step 3' infra/scripts`: 0 at head, 1 at base (control). `bash -n validate.sh` rc 0.
- CI python loop (`ciloop.sh`), 15 files, `files=15 nonzero=0`; Ran counts 10, 23, 15, 12, 33, 49, 6, 8, 16, 44, 39, 19, 56, 51, 13: equal to the kit's CENSUS table in every row.
- Not run by the gate (NOT RUN): dotnet, npm, web, hosted CI and CodeQL (they decide on the pull request). No `az`, no deploy.

## Rule (3): each acceptance check, line by line
MPSCALC-430 (tickets read whole by Jira GET at the gate: Backlog, 0 comments, 0 links, stamps unchanged; the quoted checks equal the kit's).
- "A test fails when any of the three tables or the list of plants is emptied, shown by emptying each in turn": MET. `h430-pinned` FAILED (failures=5), `h430-computed` (7), `h430-site` (12), `h430-plants` (1), `h430-siteplants` (1); at base `b430-plants` reads OK (the ticket's own claim) and `b430-pinned` fails 4 sub-tests only.
- "it passes on the real file": MET. `head0` OK, Ran 49.
- "the count of tests is printed before (43) and after": MET. `base0` Ran 43 OK; `head0` Ran 49 OK (the 6 added: 5 in `TheTablesAndPlantListsAreNotEmpty`, 1 in `TheSitePropertyGuardsFireOnPlantedSource`).
- "no other byte of infra changes": MET. Whole-tree diff names two files.

MPSCALC-431.
- "each mutant test asserts exactly one new problem": MET for the three mutant tests the ticket's recommendation names (compiled mutants `one_setting_problem`, the id swap, the planted source), each takes `before` from the unmutated template and asserts `len(new_problems(...)) == 1` with a message naming the key. `h431-two` (a checker that reports two problems per change) fires 34 sub-tests. The older guard classes keep their own convention, which the ticket allows.
- "a removed setting gives a message that names the key and not a bare KeyError": MET. `h431-removed` out.txt holds `setting WEBSITES_CONTAINER_START_TIME_LIMIT is not in the unmutated template, so there is nothing to remove` and 0 KeyError lines; the base run `b431-removed` holds 1 KeyError (control), errors=1.
- "the first failure printed names the key of the defect": MET ONLY BY THE SUB-TEST LABEL, plainly. `h431-defect` out.txt line 53, the first failure printed: `FAIL: test_each_planted_source_change_is_one_problem (...TheSettingValueGuardsFireOnPlantedSource...) (plant='WEBSITES_ENABLE_APP_SERVICE_STORAGE')`; the key is in the label. The assertion message of that sub-test is still the bare `unique anchor` (the planted text is gone from the defective source). The cascade falls from 34 failures at base (`b431-defect`) to 2 at head, so the "another key" half of the ticket's complaint is cured; the "names the key by message" half is not. Not a defect of the kit (Q3, S5): this is Finding F1, to be read by the records pass in those words.
- "the file passes on the real template; the count of tests is printed before and after; no other byte of infra changes": MET (as 430).

MPSCALC-432.
- "Each of the seven properties is checked by the test against a stated value": MET. Seven rows added to `SITE_EXPECT` (alwaysOn True, http20Enabled True, remoteDebuggingEnabled False, use32BitWorkerProcess False, appCommandLine "dotnet MpsCalc.Api.dll", clientAffinityEnabled False, publicNetworkAccess "Enabled"); the template lines `showcase.bicep` `:42 :46 :47 :48 :52 :38 :39` are the kit's and the seat's printed ones, and the planted runs find the template writes each.
- "each row turns red under a planted change of the template source": MET. `h432-1` to `h432-7` each FAILED (failures=1), Ran 1 test; at base `b432-1` to `b432-7` each stay OK (43), which is the ticket's gap shown; `h432-control` OK.
- "stays green on the real template": MET (`head0`, `h432-control`). "the count of tests is printed before and after": MET (43, 49). "no template byte changes and no other byte of infra changes": MET.

MPSCALC-433.
- "The comment at infra/scripts/validate.sh:4 names the what-if step as infra/README.md numbers it": MET. validate.sh line 4 reads `# and is infra/README.md step 2.`; README line 59 is `2. **What-if, pass 1 (S).**`; `check433.py` exit 0 at head.
- "the text README.md step 3 reads 0 lines of infra/scripts": MET (0 at head, control 1 at base).
- "no other byte of the file changes (a diff of one line)": MET (`1 1`, mode 755, size equal).
- "the python test files of the CI workflow pass (15 files)": MET (`nonzero=0`).
- "no template, test or code behaviour changes": MET for template and code; the test file is changed by the other three tickets, which the commit states; the script's behaviour is unchanged.

## Rule (4): the seat's residue incident
Confirmed nothing tracked moved: the compare of branch against main lists two files only; the three files (`Datasec` in `!CODING/Datasec/`, `MPS` and `Commercial` in the MPS project root) exist today as untracked zero-byte files with the mtimes the seat named (16 Nov 08:20 and 2 Nov 07:59), so the `mv -n` move-back restored them. The seat wrote outside its lane for a few minutes (its own words); no content could be lost (0 bytes). Records line only (F3).

## Rule (5): landing texts
Written in this folder in the form of the B1881 folder: `pr-title.txt` (101 characters, equals the commit subject), `pr-body.md`, `squash-subject.txt` ending `(#PRNUM)`, `squash-body.txt` ending `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (the commission's form; the branch commit itself carries `Claude Sonnet 5.5`, that is the seat's, and the squash commit is the merger's), `landing.txt` (`pr_checks_wait.sh ... --min-checks 9`; the nine check names of PR 225's head f81e36f: package, CodeQL, dotnet, python, web, Analyze (python), Analyze (actions), Analyze (csharp), Analyze (javascript-typescript), all success; CodeQL analyses at the head first with 0 alerts; head-pinned squash; no deploy), `FOR-RECORDS.md` (the Q3 gap, the 9449 gitleaks history findings with five sampled at source by location only).

## Findings
- F1 (records/text, Minor): MPSCALC-431's "first failure printed names the key" is met by the sub-test label only; the `unique anchor` message is unchanged. Tuesday's own Q3 choice. The records pass reads it so.
- F2 (records, relayed): 9449 `generic-api-key` findings in main's history by `gitleaks git` (9426 in `purchase_bom_scenarios.json`); none in this commit. Five sampled by location: all line 1 (minified fixture), 28-character generated-looking identifiers after a `line` or `section` key, DERIVED as fixture data. Not proven for the rest; a records ticket for an allowlist or baseline.
- F3 (records): three untracked zero-byte stray files in the MPS project root and one level above; the seat's loop touched them and restored them.
- Gate note (own): my first extraction of the tarballs went into a scratchpad folder named `head` that already held another task's files, so a few MPS files were added there; the gate's real work is in `g1896/`. Nothing was deleted; no project, Jira or GitHub write; no credential printed.
