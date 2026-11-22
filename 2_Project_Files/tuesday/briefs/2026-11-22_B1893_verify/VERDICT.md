GATE B1893: NO GO @ a9dc8cd on main e1e8043

# B1893 VERDICT: refuse-round delta reader (successor of B1890), OXPd 2 lane I, round 3 (kit B1892, seat X26)

Reader: B1893 (Opus 5.5), 2026-11-22, about 14:35 to 14:45 AEDT. My evidence is in `evidence/` in this folder. A program printed every number below in this session. I worked in my own draft clone in my session scratchpad (push URL `invalid://no-push`). I typed and printed no planted value. The gitleaks control cut the value with `squash_scan.cut(...)[1]` and printed only its length (41) and its two-character head. A program then checked that no file I copied here holds the value past its head (0 files). I ran no `--source-documents`, no dotnet and no lock. I wrote nothing in the OXPd_2 project, pushed nothing, opened no pull request and sent no message.

## The NO GO, in one line
**MAJOR G1 (refusal 2, the quoted value spread over lines): refusal 2 does not refuse an open quote when a `${{` in a plain mapping key comes before it.** `check_spellings` runs `yaml_scan` on `bare`, which is the line after `R6_EXPRESSION` has removed `${{ ... }}`. That regex is non-greedy and does not look at quotes. So in the line `      a${{: "b }}` it removes `${{: "b }}`, which is the key's tail, the `: ` and the opening quote. `bare` is then `      a`: no quote is left open, no `{` is left, and no finding is made. YAML reads that line differently: the key is `a${{` and the value is a double-quoted scalar that is still open. The continuation lines are then read as YAML, and ` x: |` opens the same phantom block as round 2's F1.

Measured through the whole program (`evidence/x3full.py`, `evidence/x3full.log`): the head's own `ci.yml` with one job appended, in a git tree. The appended job's lines are `env:` / `      a${{: "b }}` / ` x: |` / `  y"`, followed by the payload at the job's indent:
```
r2-control-open-quote-low-indent             rc 1 ['RULES: R6 .github/workflows/ci.yml:221']
r2-expr-in-plain-key-hides-open-quote        rc 0 ['RULES: clean (1 files)']
   psych: valid; hidden keys=["runs-on", "env", "permissions", "steps"] permissions="write-all" env={"a${{"=>"b }} x: | y"}
r2-expr-in-plain-key-hides-open-quote-sq     rc 0 ['RULES: clean (1 files)']      (the same with single quotes)
```
The hidden payload is a job-level `"permissions": write-all`, an unpinned `- "uses": actions/checkout@main` and a flow mapping `- { run: "echo x" }`. R3, R4 and R6 all stay quiet.

- **Which property this breaks.** The kit's property is "no line outside a block scalar leaves a quoted value open". The README's new R6 sentence is "a line outside a block scalar that leaves a quoted value open at its end (a quoted value spread over lines) is a finding". The R6 docstring and the `check_spellings` docstring say the same. The line `      a${{: "b }}` is outside any block and leaves a quoted value open, and it is not a finding. The commission grades "a hole of the SAME three classes still open through the whole program" as a NO GO.
- **It was there at HEAD2 too.** At `ff1defac` the same shape gives rc 0 (`evidence/x3full-head2.log`). So this is not a regression. It is a gap in the new refusal's reach.
- **What I measured, and what I did not.**
  - Ruby Psych (libyaml) reads the file as valid and returns the hidden keys. Psych is NOT GitHub's parser.
  - The spec-indent control gives rc 1 (`evidence/x3spec.log`: the payload's quoted keys fire), but the open-quote line itself is still not flagged there. Only the shape whose continuation is indented less than its key hides the job, exactly as in round 2's F1. A strict reading of the YAML spec rejects that indentation (DERIVED, as in round 2).
  - The shape needs `${{` with no closing `}}` inside a mapping key. GitHub's template reader very likely refuses such a key as an expression that is not closed. That is DERIVED from my memory of the runner's template-reader source; I could not open the source here and did not measure it. If it holds, GitHub rejects the workflow before any job runs.
  - GitHub's acceptance of the whole shape is UNMEASURED. It cannot be measured without pushing a workflow.
- **What lessens it, without clearing it.** The same mitigations as round 2 apply. `ci.yml` is held by its whole-file fingerprint, so any such edit turns `test_the_whole_workflow_is_the_reviewed_text` red until a person moves `REVIEWED_WORKFLOW`. `test_pipeline_controls.py` allows only one workflow file. On top of those, this shape needs two parser leniencies: libyaml's low indentation, and a `${{` key that GitHub probably refuses. On mitigations alone I would put this below round 2's F1. But the commission names this class as a NO GO, and the shipped README sentence is false for this shape. So I grade it Major and NO GO.
- **The fix default I propose.** I measured it in a scratch export only; `evidence/x3full-fixsketch.log` holds the probe run. It is one condition in `check_spellings`: `if left_open or yaml_scan(line)[1]:`. In words: judge the open quote on the raw line too, with its expressions kept. In my scratch export of the head the change gave these results:
  - the suite `Ran 111 tests`, `OK`;
  - `RULES: clean (412 files)` on the head's tree, so no line of today's `ci.yml` is affected and no fingerprint moves;
  - both G1 shapes `rc 1` (`R6 .github/workflows/ci.yml:222`);
  - every other row of `x3full` unchanged in rc.

  A fix round would add a cell for each of the two G1 shapes (double quote and single quote), and a mutant that drops the raw-line test. **The alternatives:**
  - Remove expressions only outside quoted scalars. That is a new reading, which the ruling's way (a refusal) avoids.
  - Refuse any `${{` before a line's first `: `, i.e. an expression in a mapping key. That is a plain refusal. Its cost: a key holding an expression is never allowed, which today's `ci.yml` never needs (UNMEASURED by census).

## What I re-ran at a9dc8cd (the kit's FOR TUESDAY lines for B1890's successor and for "Both")
- **Scope.**
  - `diff --name-status ff1defac a9dc8cd` gives 4 `M` rows: `ci.yml`, `README.md`, `build/repo_rules.py` and `build/tests/test_repo_rules.py`. There are 0 `A`, `D` or `R` rows. The numstat is 1/1, 2/2, 31/5 and 64/0.
  - `diff --quiet` over `src tests packaging contracts build/denylist build/tests/test_pipeline_controls.py build/release_guard.py build/squash_scan.py` and both of their tests gives rc 0. The control over `README.md` gives rc 1.
  - The tree is `c7dad617` (= the drafter's prototype). The four sha256 equal `FIXED.sha256`, 4 of 4.
  - By GET at 14:42: the branch is ONE row at a9dc8cd9; the compare shows ahead 1, behind 0, 4 files; the commit has ONE parent ff1defac; open pull requests 0; pull requests with a head starting `b1861` 0. `main` is e1e8043d.
  - The commit message equals the kit's `commit-message.txt`.
  - **HOLDS.**
- **The rest of `repo_rules.py` against ff1defac.** I read the whole diff. Its hunks are the docstrings, `R6_NOT_PLAIN`, `yaml_structure` (now `return yaml_scan(line)[0]`, which is the same loop and the same string answer), `yaml_scan`, `check_plain`, the open-quote finding, R8's quote finding, and the `check_plain` call in `judge`. No other line changed. In `test_repo_rules.py`, 64 lines are added and 0 removed: one new class with three methods, and no existing method edited. **Nothing else changed in behaviour: HOLDS.**
- **The fingerprints** (`evidence/fingerprints.log`): `scan True rules True whole True floors [111] planted 111`. The control, a one-letter edit, gives `whole False`. `test_pipeline_controls.py` is unchanged (rc 0), and its three constants equal ff1defac's. Indented `def test_` lines total 111, column-1 0, and `FLOOR=111` is at `ci.yml:211`. **HOLDS.**
- **Suite and rules.** The suite gives `Ran 111 tests`, `OK`. I printed that `1_Project_Definition` is absent in the clone (rc 0). `repo_rules.py` WITHOUT `--source-documents` then gives `RULES-NOTE: R5 hash half NOT RUN`, `RULES: clean (412 files)`, rc 0. **HOLDS.**
- **`p2full.py`** (my round-2 probe, unchanged): `phantom-low-indent rc 1 ['RULES: R6 .github/workflows/ci.yml:221']` (rc 0 in round 2). Both controls give rc 1. `today's ci.yml: lines outside a block that leave a quote open: 0`. This equals the kit's MEASURED line. **Round-2 F1 / N2 is CLOSED for its own shape.**
- **`r6probe2.py`** (unchanged): of 15 rows, 11 are unchanged against my round-2 log and 4 changed, each toward a finding:
  - `dq-` and `sq-continuation-ends-colon-bar-low-indent` go from rc 0 to rc 1 `R6 :16`;
  - `dq-continuation-ends-colon-bar-spec-indent` gains `R6 :16`;
  - `tab-before-hash-comment` gains `R6 :12` (the tab byte).

  `expression-then-bar-then-deeper-payload` stays quiet (H39, B1890 F2; Psych INVALID; a record). This equals the kit's MEASURED account.
- **My 22 round-1 mutants and 8 round-2 mutants at the new head** (`evidence/mutants_r3.py`: round 2's list unchanged, HEAD set to a9dc8cd; `evidence/mutants-r3.log`): **27 killed of 34**, the same split as round 2.
  - m12 SURVIVED (the named equivalent of D19).
  - m1, m5, m9 and m16 were NOT APPLIED (their text moved in round 2). Their remakes m1b, m5b, m9b and m16b are all killed.
  - n1 and n2 SURVIVED (the tab shapes). Through the whole program both are equivalent now. With n1 applied, `jobs:\t# x: |` still gives `R6 :12`, rc 1. With n2 applied, `name:\t"a` plus a continuation still gives `R6 :221`, rc 1. Refusal 1 refuses the tab before any line is read. That makes them records, not findings.
  - The pristine export gives `Ran 111`, 0 FAIL, 0 ERROR.
- **The seat's refusal mutants** (`mutants3.py`, run from my copy of the tools): `MUTANTS3: 13 killed, 0 survived (none), 0 not applied of 13`, and the pristine copy gives `Ran 111`.
- **Refusal 1 and refusal 3 through the whole program** (`x3full.log`): every shape fires.
  - Refusal 1: NEL alone (0x85), VT, FF, 0x1C, 0x1D, 0x1E, NUL (also R7), `Å` in UTF-8, U+2029, and a high byte on a last line with no line feed.
  - Refusal 3: a quoted pattern after a BOM, after a CR, after a tab, with an escaped quote, a quote in an attribute value, a quote on a last line with no line feed, and a file named `.GitAttributes`. The comment lines that hold quotes stay quiet. `git check-attr` (2.54.0) sets `filter: lfs` in each quoted-pattern shape that R8 now refuses.

  **Refusals 1 and 3: no hole found.**
- **Local CodeQL 2.27.4:**
  - head a9dc8cd: `0 results (code-scanning 0, security-extended 0)`, rc 0, 7 of 7 Python files and 1 of 1 Actions file;
  - control 28d2852d: `6 results (code-scanning 3, security-extended 3)`, rc 1.

  **HOLDS.**
- **Words and gitleaks.**
  - The added lines, by program from `diff -U0`: 98. `words2.py --control` gives `CONTROL FIRED: 13 of 13`. Over the added lines and the stored message: `WORDS: clean (2 files)`, with 2 byte escapes removed by the allowance.
  - gitleaks 8.30.1: the planted control gives rc 1. The 4 changed files, the added lines and the message under neutral names give rc 0, `no leaks found`.

  **HOLDS.**
- **Hosted run 44980825061 of a9dc8cd by GET** (`hosted2.py ... --total 1335 --rules 412 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111 --hardened-scan`): `HOSTED a9dc8cd93969dfd5f623c10345257b6e6a723104: PASS`.
  - Every job is attempt 1.
  - linux: total 1335, 4 skipped. windows: total 1335, 19 skipped. Both legs `GUARD: clean`.
  - rules: `Ran 111`, `UNIT-TEST FLOOR: ran 111, floor 111`, `RULES: clean (412 files)`.
  - secret-scan: `found under a neutral name 25 of 25`, both `NEUTRAL-EXPORT` lines `wrong 0`, `NEUTRAL-SCAN: stored objects 1072`, `REACH ... 0`.
  - Control: `--unit 108 --floor 108` gives `FAIL 2` on exactly the two `rules` rows.

  **HOLDS.**
- **README and the docstrings against the code.** They match the code for refusal 1 and refusal 3. For refusal 2 they are false for G1's shape (above).

## Rule on 6: THE MERGE with main e1e8043d (`evidence/merges3.py`, `evidence/merges3.log`)
| Merge | merge-tree | Tree | `repo_rules.py` (no `--source-documents`) | `build/tests` | Files | FLOOR / indented `def test_` | ci.yml |
|---|---|---|---|---|---|---|---|
| main e1e8043d + a9dc8cd | rc 0, and both orders give the same tree | `458df92f03ab0e0f8240e65f8b65d6c64458e5f2` (= the kit's MEASURED tree) | `RULES: clean (478 files)`, rc 0 | `Ran 111`, OK | **478** | 111 / 111 | equal to the head's; one workflow file |

The merge base is 5bb1418c. Since that base, `main` changed 0 rows under `build/`, `.github/` or exactly `README.md`, and 0 `.gitattributes` files. The control on the head's side counts 9. **The merge HOLDS.** On a NO GO these numbers are records; a fix round moves `Ran` and `FLOOR` to 113 if it adds two cells.

## Findings
| # | Severity | Inside the three refusals? | Finding | Where |
|---|---|---|---|---|
| G1 | **MAJOR** | **yes: refusal 2** | An open quote after a `${{` in a plain mapping key (`a${{: "b }}`) is not refused, because the expression removal runs before the quote reading and swallows the opening quote. A multi-line quoted value then hides a whole job (rc 0, libyaml valid). GitHub's acceptance is UNMEASURED and DERIVED as likely refused (an unclosed `${{` in a key), and the low indentation is spec-invalid. The README and docstring sentences for refusal 2 are false for this shape. It was there at HEAD2 too | `build/repo_rules.py:292`-`:295` (`bare` then `yaml_scan(bare)`) |
| G2 | records | no (R6's older flow rule) | The same expression removal hides a `{` on that line: `a${{: {b: "}}"}` makes no finding on its own line (libyaml: a flow mapping under `env`). The file is red here only because of the payload's quoted keys. My fix default for G1 does not cover it; the "refuse `${{` in a key" alternative would | `repo_rules.py:296` (`"{" in bare`) |
| G3 | Minor (test gap) | yes: refusal 2 | The open-quote cell has no shape with an expression in front of the quote. Its "after a tab" shape is also refused by refusal 1 on the same line, so that subTest cannot tell the two refusals apart | `test_repo_rules.py`, `RefusalsOfWhatALineReaderCannotRead` |
| G4 | records | no | n1 and n2 (the tab shapes of round 2) still survive in the unit suite, but they are equivalent through the whole program (refusal 1) | `evidence/mutants-r3.log` |
| G5 | records (reader conduct, mine) | no | Two of my commands were refused by the workspace hooks before they ran, so they changed nothing. One held a stray `cd /dev/null` that I had typed by mistake. The other held `git switch` and `git init` on a path written as a shell variable, which the hook cannot resolve (the targets were my scratchpad). I re-ran them with literal paths and without the `cd` | this session |

## What I did NOT test
- GitHub's own parser on G1's shape (it can only be measured by a pushed workflow). My reading of the runner's template reader is from memory; I did not read its source here.
- A census of today's `ci.yml` for keys holding `${{` (the cost of the second alternative).
- Anything on Windows, and Ubuntu `mawk`.
- B1891's N1, N2 and N3 probes, `r8_probe.py`, and its mutants (B1894's assignment). The release guard on lane D's real publish folders.
- `prove3.py`, `frame3.py`, `census3.py` and round 2's 38 `mutants.py` (the seat ran them; I ran my own lists and `mutants3.py`).
- CodeQL on a pull request, and a merge-ref hosted run (no pull request exists).

On a NO GO I write no landing texts. FOR-RECORDS.md holds the merge numbers and the records items.
