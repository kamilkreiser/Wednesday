GATE B1890: NO GO @ ff1defa on main ca94ed9

# B1890 VERDICT: whole-lane reader (successor of B1879), OXPd 2 lane I, fix round (kit B1882, seat X26), G1 round 2 of 2

Reader: B1890 (Opus 5.5), 2026-11-22, about 10:27 to 10:50 AEDT. My evidence is in `evidence/` in this folder. Every number below was printed by a program in this session. I worked in my own draft clone (push URL `invalid://no-push`) in my session scratchpad. I typed and printed no planted value. The one control that needed it cut the value from the workflow's two halves by `squash_scan.cut`, and printed only its length (41) and its two-character head. I ran no `--source-documents`, no dotnet and no lock. I wrote nothing in the OXPd_2 project, pushed nothing, opened no pull request and sent no message.

## The NO GO, in one line
**MAJOR F1 (new; it was there at HEAD1 too, and neither round-1 reader found it): a multi-line quoted scalar still opens a phantom R6 block.** The fix reads each line on its own. A continuation line of a quoted scalar that does not close on its first line is therefore read as YAML, and if it ends in `: |`, R6 opens a block there. When that continuation line is indented less than its key, every later line at that indent or deeper is skipped as block text. That can be a whole job holding a quoted `"permissions": write-all`, an unpinned `- "uses": actions/checkout@main` and a flow mapping `- { run: ... }`, and R3, R4 and R6 all stay quiet. Measured through the whole program on the repository's own `ci.yml` with one job appended (`evidence/p2full.py`, `evidence/p2full.log`):
```
phantom-low-indent     rc 0 ['RULES: clean (1 files)']
   psych: valid; hidden.name="a x: | y" hidden.permissions="write-all" steps=[{"uses"=>"actions/checkout@main"}, {"run"=>"echo x"}]
control-spec-indent    rc 1 ['RULES: R6 .github/workflows/ci.yml:224', 'RULES: R6 ...:226', 'RULES: R6 ...:227']
control-no-bar         rc 1 (the same three R6 lines)
```
The appended job is `name: "a` / ` x: |` / `  y"`, then the payload at the job's indent.
- **Which property it breaks.** The head's own R6 docstring says "A block scalar is the lines after a line whose YAML, with its comment and its quoted scalars taken out, ends in a key and | or >". It also says "A comment never starts a block". Kit D15 says that in "a multi-line quoted scalar: its rest is never read as YAML". The line ` x: |` is inside a quoted scalar, so with its quoted scalars taken out it is empty, and yet R6 opens a block on it. This is the F1 class exactly: a phantom block on a line that YAML does not read as a block start. The commission grades "an R6/R8/G2/G3 hole of the same class" as a NO GO.
- **How it was measured, and what was not.**
  - Ruby's Psych (libyaml 0.2.1, `/usr/bin/ruby`) reads the file as valid and returns the hidden keys exactly. That is the reference C parser, but it is NOT GitHub's parser.
  - The YAML 1.2 productions (s-flow-line-prefix(n)) want the continuation lines indented past the parent mapping. So a strict parser rejects the low-indent shape (DERIVED). At the spec's own indent R6 fires: that is the control row.
  - Whether GitHub accepts the low-indent shape is UNMEASURED. It cannot be measured without pushing a workflow.
  - At HEAD1 the same shapes are just as quiet (`evidence/r6probe2.log`, rows `dq-/sq-continuation-ends-colon-bar-low-indent`). So this is not a regression of the fix: it is a hole that the fix's own new wording now claims to close.
- **What lessens it, without clearing it.** It is the same mitigation as round 1's F1: `ci.yml` is held by the whole-file fingerprint, so any such edit turns `test_the_whole_workflow_is_the_reviewed_text` red until a person moves `REVIEWED_WORKFLOW`.
- **The fix default I propose (measured in a scratch copy only, `evidence/` has no diff of it).** In `check_spellings`, a line outside a block whose `yaml_structure` leaves a quote open is an R6 finding: a multi-line quoted scalar is refused, the same way a flow collection is refused on its first line. Inside `yaml_structure` that is the one fact `quote is not None` at the end of the loop. In my scratch copy of the head the change gave these results:
  - the suite `Ran 108`, `OK`;
  - `RULES: clean (412 files)` on the head's tree, because today's `ci.yml` has 0 lines outside a block that leave a quote open (`p2full.log` last line), so no fingerprint moves;
  - the phantom shape `rc 1`.

  **The alternative** is to carry the open quote across lines, so that continuation lines count as text until the quote closes. Its cost: more state, and a stray quote mark could make R6 read real YAML as text, which would be a new hole. The fix-round kit would add a cell for ` x: |` under an open `"` and under an open `'`, each with a quoted key below it that must fire, plus a mutant that drops the open-quote test.

## What I re-ran at ff1defac (the kit's FOR TUESDAY lines for B1879 and for "Both")
- **Scope.**
  - `diff --name-status 782b3795 ff1defac` gives eight `M` rows, exactly the owned paths, with 0 `A`, `D` or `R`.
  - The numstat equals FACT 5: 1/1, 5/5, 29/14, 63/16, 18/9, 75/0, 98/0, 89/0.
  - `diff --quiet` over `build/tests/test_pipeline_controls.py build/denylist src tests packaging contracts` gives rc 0. The control over `README.md` gives rc 1.
  - The tree is `79a6ca2d` (= the drafter's prototype). The eight sha256 equal `FIXED.sha256`, 8 of 8.
  - By GET: the branch is ONE row at ff1defac, the compare shows ahead 1, behind 0, 8 files, the commit has ONE parent 782b3795, and pull requests with a head starting `b1861` number 0.
  - The fingerprints: `job_sha256(secret-scan)`, `job_sha256(rules)` and `workflow_sha256` each equal their constant, and `floors` gives `[108]`. As a control, an edit of one byte run moves the workflow fingerprint. Indented `def test_` lines total 108, column-1 0, and `planted_controls` gives 108. **HOLDS.**
- **Suite and rules.** The suite gives `Ran 108 tests`, `OK`. `repo_rules.py` WITHOUT `--source-documents` gives `RULES-NOTE: R5 hash half NOT RUN`, `RULES: clean (412 files)`, rc 0. `git ls-files` gives 412. **HOLDS.**
- **Round-1 F1 probe** (`p1full.py`, unchanged but for the clone): the control is `R6 :16` and the R3 control is `R3 :16`. **The comment line `# the jobs: |` now gives `rc 1 R6 :17`, and the trailing `jobs: # list: >` gives `rc 1 R6 :16`.** Round-1 F1 is CLOSED.
- **My 22 mutants at the new head** (`evidence/mutants_r2.py`: round 1's program with its HEAD constant set to ff1defac):
  - **17 killed**: m2, m3, m4, m6, m7, m8, m10, m11, m13, m14, m15, m17, m18, m19, m20, m21, m22.
  - **m12 SURVIVED**: the named equivalent of D19.
  - **4 NOT APPLIED**, because their text moved: m1, m5, m9, m16. Re-made against the fixed lines as m1b, m5b, m9b, m16b, **all 4 killed**.

  This equals the kit's MEASURED "17 killed of 22". The pristine export gives `Ran 108`, 0 FAIL, 0 ERROR.
- **Eight new mutants of mine on the fixed code:**
  - 6 killed: n3 (CR not a separator in R8), n4 (a ZIP not at the start unseen), n5 (NUL in the body unseen), n6 (CA name in the last member only), n7 (failed step not caught), n8 (block start on the raw line).
  - **2 SURVIVED.** **n1**: a `#` after a TAB not taken as a comment. That re-opens round-1 F1 for `jobs:\t# x: |`, which my probe shows fires at the head. **n2**: a quote after a tab not a token start. These are F3 below.
- **`prove.py`** (round 1's tools, against `5bb1418c`): `PROVE: PASS (49 rows)`, 34 killed. As the kit says, it never reads C1.
- **`scan_faults.py`**: 6 of 6 `as wanted`, porcelain EQUAL, `SCAN-FAULTS: PASS`.
- **Local CodeQL 2.27.4** (`codeql_py.py`):
  - head ff1defac: `0 results (code-scanning 0, security-extended 0)`, rc 0, 7 of 7 Python files and 1 of 1 Actions files;
  - control `28d2852d`: `6 results (code-scanning 3, security-extended 3)`, rc 1.

  **HOLDS.**
- **Hosted run 44961377381** of ff1defac by GET (`hosted2.py ... --total 1335 --rules 412 --skipped-linux 4 --skipped-windows 19 --unit 108 --floor 108 --hardened-scan`): `HOSTED ff1defac24c24a0331af201db6a7d0cc6de40d3d: PASS`. Every job is attempt 1. The secret scan's lines: `NEUTRAL-EXPORT ... wrong 0` (both), `NEUTRAL-SCAN: stored objects 1061`, `REACH ... 0`. Control: `--unit 84 --floor 84` gives `FAIL 2` on exactly the two `rules` rows. **HOLDS.**
- **Words and gitleaks.**
  - The added lines, by program from `diff -U0`: 378. `words2.py --control` gives `CONTROL FIRED: 13 of 13`. Over the added lines and the stored message: `WORDS: clean (2 files)`, with 73 byte escapes removed by the allowance.
  - The stored message equals `commit-message.txt` byte for byte (386).
  - gitleaks 8.30.1: the planted control gives rc 1. The clone's work tree gives rc 0. The 10 files under neutral names (the added lines, the message, and all 8 changed files including `ci.yml`) give rc 0.

  **HOLDS.**
- **README and the two docstrings against the code.** I read them in full. G1, G2, G3, R6, R8, `Limits, said plainly:` and the squash exit-2 list each say what the code does, except the R6 wording quoted in F1 above. No text says the product owner decided anything.

## Rule on 3: Tuesday's two STOP-class answers as built
- **Q14** (a comment line ends a block only by its indentation; a comment never opens one): **HOLDS as built, and the reading opens no hole that I could find.**
  - A comment line at the key's column inside a block, and a less-indented comment line followed by a quoted key, each fire (`r6probe2.log`). YAML ends a block scalar at a less-indented line whether it is a comment or not, so the lines after it are YAML: stricter, never hidden.
  - Every comment-opened phantom I tried now fires: a tab before `#`, an anchor or a tag before a comment, a comment holding a quote, a quoted value holding `#` and `: |`, and a doubled single quote. Psych reads each as valid YAML with the hidden key.
  - **F1 above is not a comment and not the Q14 reading:** it comes from the per-line reading of a multi-line quoted scalar.
- **Q26** (C1 pushed alone; the moved main measured): **HOLDS.**
  - By GET: ONE parent 782b3795 and no merge commit. `main` is ca94ed96: 50 rows since 5bb1418c, 0 under `build/`, `.github/` or `README.md` (the seat's list, my read of the merge below).
  - `merge-tree --write-tree ca94ed96 ff1defac`: rc 0, tree `9a1e42a23551ca4d8f87946dd9536451b17cae2a` (= Tuesday's S3 tree).

## Rule on 6: THE MERGE (`evidence/merges2.py`, `evidence/merges2.log`)
| Merge | merge-tree | Tree | `repo_rules.py` (no `--source-documents`) | `build/tests` | Files | FLOOR / indented `def test_` | ci.yml |
|---|---|---|---|---|---|---|---|
| main ca94ed96 + ff1defac | rc 0 | `9a1e42a23551ca4d8f87946dd9536451b17cae2a` | `RULES: clean (446 files)`, rc 0 | `Ran 108`, OK | **446** | 108 / 108 | equal to the head's; one workflow |
| main ca94ed96 + ff1defac + lane G edaa1b70 | rc 0 (both orders give the same tree) | `f82bc8949772cd1e6db7840456c07dbbb3729f3f` | `RULES: clean (478 files)`, rc 0 | `Ran 108`, OK | **478** | 108 / 108 | equal to the head's; one workflow |

Lane G `b1841/wp17-scan-and-print-jobs` is at edaa1b70 (by GET). It is now built on main (merge base ca94ed96, ahead 5, behind 0), it changes 33 files, and none of them is under `build/`, `.github/` or `README.md`, or is a `.gitattributes`. Its changed files hold 0 NUL bytes. Its own branch has 476 files and `FLOOR=60`. **Both merges HOLD.** (On NO GO these numbers are records: a fix round moves `Ran`, `FLOOR` and possibly the rules count again.)

## Rule on 7: the seat's one deviation (the neutral-copy glob)
**ACCEPTED, no effect on the result.** The first neutral folder missed the dot-named copy of `ci.yml` because the shell glob skipped it. The seat saw it by counting (8, not 9), scanned a second folder of all nine before the commit, and named it. I re-made the check myself with all 8 changed files of ff1defac, the added lines and the message under neutral names: gitleaks rc 0, and the planted control rc 1. The hosted `secret-scan` read every stored object under neutral names: PASS.

## Findings
| # | Severity | Finding | Where |
|---|---|---|---|
| F1 | **MAJOR** | A multi-line quoted scalar whose continuation line ends `: |`, indented below its key, opens a phantom R6 block. A whole job with `"permissions": write-all`, an unpinned quoted `"uses"` and a flow mapping passes R3, R4 and R6. libyaml reads it as valid. GitHub's acceptance is UNMEASURED, and a strict reading of the YAML spec rejects the indentation. The head's R6 text ("its quoted scalars taken out") claims the case | `build/repo_rules.py` `check_spellings` (block start on `structure`, `:277`); `yaml_structure` reads lines one by one |
| F2 | Minor | A new phantom from expression removal. `name: ${{ github.sha }} |` becomes `name:  |` and opens a block: the head is quiet where HEAD1 fired (`r6probe2.log` `expression-then-bar-then-deeper-payload`). Psych reads that shape as INVALID YAML, and a valid YAML plain scalar cannot carry deeper structure after it, so I could build no valid shape that hides a key. The fix of F1 could remove expressions after the structure is read, or test the block start on `yaml_structure(line)` with the expressions kept | `repo_rules.py` `:273`-`:277` |
| F3 | Minor (test gaps) | Two of my mutants on the new code survive. n1: a `#` after a tab not a comment, which re-opens round-1 F1 for `jobs:\t# x: |` and has no cell. n2: a quote after a tab not a token start | `test_repo_rules.py` |
| F4 | records | `name: "x"#: |` (no space before `#`) opens a block in both HEAD1 and the head. Psych: INVALID YAML. Not a hole | `r6probe2.log` |
| F5 | records (reader conduct, mine) | One of my commands held a no-op subshell `(cd /tmp ...; true)` before a Python call. It changed no state and no folder. I name it because my brief says never type `cd` | this session |

## What I did NOT test
- GitHub's own YAML parser on F1's shape (it can only be measured by a pushed workflow). YamlDotNet locally (no dotnet).
- Anything on Windows, and Ubuntu `mawk`.
- The release guard on lane D's real publish folders, and B1880's F1 to F4 and m1 to m8 probes and its 16 mutants (that is B1891's assignment). I relied on the hosted legs' `GUARD: clean (10 files)` and `(11 files)`.
- The drafter's 38 `mutants.py`, `prove2.py`, `r8_vs_git.py` and `outframe.py` (the seat ran them; I re-ran my own lists).
- CodeQL on a pull request (none exists).
- Lane G's dotnet totals (not this lane's). The merge's hosted run (none exists).

On a NO GO I write no landing texts. FOR-RECORDS.md holds the merge numbers and the records items for the fix round.
