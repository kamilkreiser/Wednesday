STARTABLE: YES

# B1892 DRAFTER REPORT: lane I refuse round (round 3), kit for seat Datasec/OXPd2-X26 (Opus)

Drafter: in-session Opus agent, read-only, for Tuesday s308. Drafted 2026-11-22, 13:55:18 to about 14:20 AEDT (clocks by `date`; the sidecar's `WRITE` line holds the write clock). Commission: `2026-11-22_B1892_LANE-I-REFUSE-ROUND_DRAFTER_COMMISSION.md` (sha256 `de568abb...`), read whole.

## BLUF
- **Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1892_SEAT-X26_oxpd2-wp03-ci-guards-refuse-round.md`, 71740 bytes, 240 lines. Sidecar `.measured` beside it: 150 claims, 150 measured; `stamp_check.py <kit>` exits 0. The seat's read load is 115833 bytes plus the kit, about 187.6 KB in all (the sidecar's `LOAD` line). That fits an Opus seat.
- **Scope:** the three refusals the product owner ruled, and nothing else: D31, D32 and D33 in `build/repo_rules.py`. There are three new cells in `build/tests/test_repo_rules.py`, `FLOOR` goes 108 -> 111, and two README lines change. Four files change, there are no new files and no fingerprint constant moves.
- **Refusal 1 (plain characters only):** every byte of a tracked file under `.github/workflows/` must be 0x20 to 0x7E or 0x0A. Any other byte is an R6 finding on its line, counting lines at line feeds. The check reads the raw bytes in `judge()` through `check_plain`, so it does not depend on the line reader. Of the 8 bytes that a latin-1 `splitlines()` splits at, only 0x0A is allowed (measured over all 256 bytes). **Today's `ci.yml` passes:** 0 bytes outside the set, 0 CR, 0 tab (measured, with a control).
- **Refusal 2 (no quoted value spread over lines):** a line outside a block that leaves a quote open is an R6 finding. This is B1890's proposal. The check is `yaml_scan`, and `yaml_structure` still returns a string because B1890's `p2full.py` calls it. Today's `ci.yml` has 0 such lines.
- **Refusal 3 (no quote in an attribute line):** any `"` in a `.gitattributes` line that is not a comment is an R8 finding. Both tracked `.gitattributes` files have 0 such lines.
- **Red, green and mutants (measured):**
  - Red at `ff1defac`: 3 cells, 19 FAIL lines, 0 ERROR. Every one of the 19 subtests is red.
  - Green: `Ran 111`, OK. `PROVE3: PASS (7 rows)`; its control is `FAIL`.
  - The 13 refusal mutants: 13 killed. Round 2's 38 mutants on the new tree: 37 killed and x38 survives, the same as round 2.
- **Every N1, N2 and N3 probe, through the whole program:** rc 0 at `ff1defac` and rc 1 on the prototype. That includes B1890's `p2full` phantom (rc 1, R6 :221) and B1891's `r8_probe` quoted shapes (rc 1, R8 :1). The two new N2 shapes I found outside the frame are also closed (H37, H38).
- **Merge with main `e1e8043d`** (lane G landed): 82 rows since `5bb1418c`, 0 under `build/`, `.github/` or `README.md`. `merge-tree` rc 0, tree `458df92f`, 478 files, `RULES: clean (478 files)`, `Ran 111`.
- **Other checks:** CodeQL prototype 0+0, control 3+3. gitleaks: control rc 1, neutral rc 0. `words2.py` clean. The hosted run of `ff1defac` PASSes with `--unit 108`, and the control `--unit 111` gives FAIL 2.

## FACTS RE-MEASURED (instrument; log under `fleet/state/s308/d1892/logs/`)
| Fact | Instrument | Result |
|---|---|---|
| The ruling | `decision_queue.sh show datasec-oxpd-ci-guards-round2-nogo-1122` (whole print read) | status ruled, choice `a`, `ruled_ts=2026-11-22T13:53:27.382739+11:00`; option a's label and detail match the commission's quote word for word |
| Origin | `gh api -X GET` 14:05:45 and 14:15:04 (`origin.log`) | branch `b1861/...` = ff1defac (one row); main e1e8043d; pull 15 closed, merged=true, e1e8043d; refs `b1892` 0; pulls with a head starting `b1861` 0; open pulls 0; private true |
| HEAD2 lineage | `rev-parse` (`revs.log`) | ff1defac~1 = 782b3795, ~6 = 5bb1418c |
| Census at HEAD2 and on the merged tree | `census3.py` (`census-ff1defac.log`, `census-merged.log`) | 1 workflow file; `outside-plain 0`; CR 0; tab 0; high 0; open-quote lines 0; 2 `.gitattributes`, quote lines 0; each control above 0 |
| Red then green | `prove3.py` (`prove3.log`, `prove3-control.log`) | PASS (7 rows); control FAIL (6 rows) |
| Mutants | `mutants3.py`, round 2's `mutants.py` | 13 of 13 killed; 37 of 38 killed with x38 surviving (expected) |
| Readers' probes | `probes3.py` (tools), `p2full.py`, `r8_probe.py`, `x85_probe.py`, `ml_probe.py`, `r6probe2.py` | see the kit's FOR TUESDAY. `x85_probe.py` still prints `R6 []` on the prototype, because it calls `check_spellings` directly. That is not a hole; the whole-program run is the real test |
| Frame | `frame3.py` (`frame3-head.log`, `frame3-proto.log`), with Psych and `git check-attr` | H31 to H41 as the kit's table |
| Fingerprints, FLOOR | `test_pipeline_controls` functions by program | scan, rules and whole each True, `floors [111]`; a one-letter control edit gives whole False; indented `def test_` 111, column-1 0 |
| Owned paths | name-status check by program | 4 `M`, 0 bad; a planted control names both bad rows; diff `--quiet` outside the owned paths rc 0, README control rc 1 |
| Workflow step | `run_step.py 'planted controls'` | `Ran 111`, `UNIT-TEST FLOOR: ran 111, floor 111`, porcelain EQUAL |
| Hosted ff1defac | `hosted2.py` GET | PASS at 108; FAIL 2 at 111 (the control) |
| CodeQL 2.27.4 | `codeql_py.py` | prototype 0 results, rc 0; control 28d2852d 6 results, rc 1 |
| Secrets, words | gitleaks 8.30.1; `words2.py` | control rc 1; neutral copies rc 0; `CONTROL FIRED: 13 of 13`; `WORDS: clean (2 files)` over 98 added lines and the message |
| Sources hashed | `shasum -a 256` (`sources.sha256`, 16 rows) | every source row I read, hashed at drafting |

## D-DECISIONS (all are Tuesday's as coordinator inside the product owner's closed list)
- D31: the byte set and the files it binds.
- D32: the open-quote refusal, with `yaml_scan`.
- D33: the attribute-quote refusal.
- D34: the drafter's diffs, cells first.
- D35: no fingerprint moves.
- D36: the moved main, as round 2's Q26.
- D37: the hosted numbers.
- D38: 90/60 minute windows, pane X26, both mutant lists.

## Q-QUESTIONS FOR TUESDAY (each with its default)
1. **Q29 (STOP-class), the byte set.** Default: 0x20 to 0x7E plus LF, over every tracked file under `.github/workflows/`; the finding is R6, per LF line. Alternatives: also allow a tab, or bind every file under `.github/` (H32 is then closed too).
2. **Q30, refusal 2.** Default: the open quote is read by round 2's quote reading, and the cost is named: `run: echo "a` outside a block is refused (measured). Alternative: none inside the ruling.
3. **Q31, refusal 3.** Default: any `"` outside a comment line.
4. **Q33 (STOP-class), the moved main.** Default: as Q26.
5. **Q34, the windows.** Default: 90/60. This round is one program and one test file; round 2's 120/90 is the alternative.
6. **Q36, the review scope.** Default: the three refusals only, per the ruling's "both reviewers check just that".
7. **Q37, a NO GO.** Default: it goes to the product owner.
8. **The ruling's clock, for the stamp.** The commission says 13:53:03; the card prints `ruled_ts` 13:53:27. The kit writes "13:53" only. Default: Tuesday quotes the card's printed value in S1.
9. **The readers' successors.** Default: they re-run N1 through the whole program, not through `x85_probe.py` alone. FOR TUESDAY says why.

## UNMEASURED / NEVER RUN
- GitHub's own YAML parser on any shape (Psych only).
- The `scan every stored object under a neutral name` step on this round's tree (NEVER RUN; its lines are predicted from round 2).
- `gitleaks dir` over the whole draft work tree (I scanned neutral copies of the changed files only).
- B1890's `mutants_r2.py` and its 8 new mutants, and B1891's 16 plus 21 mutants, on the prototype.
- The release guard on lane D's publish folders (unchanged code).
- The hosted run of the merge.
- Windows.
- Timing of the heavy steps (the kit gives estimates).

## CHAIN INPUTS
Every step's inputs exist at HEAD2 or come from an earlier step; the table is in the kit. Step 1 uses `<src>` (14 files), `<repo>` and the origin. Steps 2 and 3 use Step 1's clone and tools. Step 6 uses Step 3's tree. Step 7 uses Step 7(a)'s commit and 7(b)'s fetch.

## STOP-SEVERITY CHECKS RUN ON MY PROTOTYPE
- Each of these was run once with its control firing: the red run, the sha256 match, the fingerprints, FLOOR, rules clean, tree equality (`c7dad617` from both `write-tree` and `rev-parse`), owned paths, ASCII, gitleaks, words, the main owned-rows count, `merge-tree`, CodeQL and the census.
- Marked NEVER RUN in the kit: the hosted comparison for the new head, the neutral-scan step, and the owned-paths check on the seat's commit.

## OUTSIDE THE FENCES (disclosure)
1. **I printed the planted value whole once, in my own tool output.** At 14:06 a gitleaks-control command called `squash_scan.cut()` and printed `value[:2]`, not knowing that `cut()` returns a tuple, so the printed "head" was the function text and the value.
   - It went to no file. I scanned by program afterwards: 83 files of mine (logs, gate, tools, quarantine, kit, sidecar), and 0 of mine hold the value or its tail half. Three files do hold the tail half, as expected: the two `job-secret-scan.log` copies that `hosted2.py` fetched by GET (the runner echoes the workflow), and round 2's unchanged `run_step.py`. The control is that `ci.yml` holds the tail half 2 times.
   - The kit now warns that `cut()` returns a tuple.
   - That command and a second failed attempt left two empty control files. Both are quarantined under `d1892/_quarantine/`.
2. **The prototype commit uses a synthetic identity.** `2a2d91f4` sits in my no-push draft clone with `drafter@invalid` set through `GIT_*` variables for one `commit-tree`, the same form as round 2's `470f2fd3`. It is never pushed, and a tree sha does not depend on identity.
3. **I overwrote my own sidecar once** with a 2-row file (a re-fill run on a partial claims list). I quarantined it and rebuilt the sidecar whole from the full list.
4. **Fences kept:** no write to any project file, Jira or GitHub; `gh` with `-X GET` only; no `--source-documents`; nothing under `Source_Documents/`; no dotnet and no lock; no `cd`; nothing deleted (quarantine only); no message to anyone.

READ-WHOLE: the commission; DRAFTER_RULES.md; both round-2 verdicts and B1890's FOR-RECORDS; the round-2 kit (four pages) and its commission; the two lessons; the probes I ran; `repo_rules.py` at HEAD2 (whole, by ranges) and `test_repo_rules.py`'s case base and the R6/R8 classes.
