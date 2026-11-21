STARTABLE: YES

# B1861 DRAFTER REPORT: OXPd 2, wave 3, lane I (WP0.3 follow-ups OXPD2-20 to OXPD2-24, the CI guards)

Drafter: Opus 5.5, read-only, in-session, 2026-11-21 19:55:38 to about 20:45 AEDT (clocks by `date`). Kit:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1861_SEAT-X26_oxpd2-wp03-ci-guard-follow-ups.md`
(74,220 bytes, ASCII, 8 slot lines). Its sidecar `.measured` sits beside it: 120 claims, 120 measured, and
`stamp_check.py <kit>` exits 0. Tools, diffs and messages: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s305/d1861/gate/`
(21 files, sha256 in the kit). Prototype, logs and scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s305/d1861/`.

## BLUF
All five tickets are built and measured as five commits on a scratch clone. The clone was built on `762e774e`. Pull request 10
(lane A) landed at 20:08, so it was rebased onto the new main `977cbeb2` (BASE). The seven diffs came out byte-identical on both
bases, and every measurement was repeated on BASE.

The lane adds 772 lines and removes 52 across nine files under `build/`, `ci.yml` and `README.md`. `FLOOR` moves from 60 to 84,
in steps. Results on BASE:
- `PROVE: PASS (49 rows)`: 34 mutants killed and 0 survived; 7 gap rows; the 16 new rule cells are each red by FAIL on the old
  code, with 0 ERROR.
- `SCAN-FAULTS: PASS`.
- CodeQL shows 0 results in both suites on the final tree, and on each of C2, C3 and C4. My first prototype got 3 results; they
  were fixed in the diffs.
- Both secret scans, the word scan and the squash scan of the five messages are clean.
- The new release guard is clean on a real local publish folder of each leg: 10 and 11 files.

**The kit commissions less than the tickets** (Q13, STOP-class). Two parts of OXPD2-24 are left out: the packaging-job rule and
the `.pdb`/`web.config` policy. Read literally, the first would make today's clean `linux` and `windows` jobs red. Also left out:
OXPD2-21's flagged-message decision and its runbook line, and OXPD2-22's two "consider" items.

## The five tickets' scope sentences (read by GET, `jira_get.py`, 19:56:17; each Backlog, parent OXPD2-3, 0 comments)
- **OXPD2-20:** "reword line 72 to say every object that a branch or a tag of the origin reaches, and on a pull request that pull request's own merge commit; reword line 73 to say the checkout fetches branches and tags, and on a pull request its merge commit. Nothing else in the file changes." Commissioned whole, as C1.
- **OXPD2-21:** "a script under build/, Python 3 with the standard library only, that takes a subject file and a body file, makes a scratch repository outside the checkout with one commit carrying exactly that message, exports it through the same function the workflow uses (cut from the workflow file by program, not copied by hand) and scans it with the workflow's four scanner options; it ends 0 only on no finding. With a planted control: the same message plus the workflow's own planted value must end non-zero." Commissioned as C3. Two parts are left out: the runbook line goes to FOR RECORDS, and the flagged-message decision goes to NOT DECIDED.
- **OXPD2-22:** "list each object's size as well and require each first copy of a file, a commit or a tag to be 55 bytes longer than its object; count the listing by lines read, not by line ends; consider one planted repository for each place, each one required, which removes the sum; consider one batch process for the export before the repository grows." Commissioned as C4. It adds a 43008-byte check of the second copy and a reach check; the reach check is what makes the ticket's acceptance true. The two "consider" items default to NOT built (D8, D9).
- **OXPD2-23:** "under .github/workflows/ refuse any quoted mapping key, any backslash escape inside double quotes and any flow mapping, and refuse BASH_ENV; make a tracked file that holds a NUL byte a finding unless its path is on a short reviewed list inside the rule; refuse an LFS filter in a tracked .gitattributes; fingerprint the whole workflow file with the floor number read as a letter; and say in the README how a build adds a job (set the fingerprint in the same commit, after review)." Commissioned whole as C2: R6, R7, R8, the whole-file fingerprint and a one-workflow case.
- **OXPD2-24:** "a release mode in which 0 fingerprints is exit 2 and a deny-list away from the tracked file is refused; a rule that any job that packages, publishes or uploads an artefact calls the guard in that mode on the same folder first; the name rule as a substring, and ZIP member names split on a backslash as well; the library's name searched in every file that holds a NUL byte, not only in files that start as a Windows program; an archive the guard cannot open is a finding; a key store or certificate container it cannot read into is a finding in a release artefact; the two other PEM labels accepted, and UTF-16 text decoded before the PEM search. ... Decide in the same build whether .pdb files and the Windows web.config belong in a package." Commissioned as C5, without the packaging-job rule (NOT DECIDED 1) and the `.pdb`/`web.config` decision (NOT DECIDED 2).

## What I measured (instrument; control)
- **Origin** (`gh api -X GET` under the project `GH_CONFIG_DIR`):
  - Main was `762e774e` at 19:55; then `977cbeb2` at 20:29 (PR 10). Its compare shows 40 files, 0 of them under `build/`, `.github/` or `README.md`.
  - No ref starts `b1861`. Open pull requests: 0. Open alerts: 0.
  - Default setup reads `configured`, `extended`, `actions,csharp,python`.
- **Hosted runs, read with the R5-aware reader** (`hosted.py`, and `hosted2.py` = the same plus `--hardened-scan`):
  - Main `762e774e`: total 973, skipped 4 and 19, GUARD 10 and 11, `Ran 60`, floor 60, `RULES: clean (329 files)`. Result: PASS.
  - BASE: total 1170, skipped 4 and 19, GUARD 10 and 11, `Ran 60`, `RULES: clean (368 files)`, NEUTRAL-SCAN 814 objects. Result: PASS.
  - Control: `--total 973` on BASE gives FAIL 4 on exactly the total rows. `--hardened-scan` on `762e774e` gives FAIL 4 on exactly the four new rows.
- **Scope collisions:**
  - All 14 refs of the origin: 0 tracked files with a NUL byte and 0 `filter` attributes, and the new R6/R7/R8 `judge()` gives 0 findings on each tree. Control: a planted NUL file and a planted `filter=lfs` fire R7 and R8.
  - 5 in-flight branches: 0 changed paths under lane I's paths.
- **Prototype suite:** after the five commits it gives 60, 71, 76, 76 and 84 tests, each `OK`. The `planted controls` step through `run_step.py` gives `Ran 84`, `UNIT-TEST FLOOR: ran 84, floor 84`. `repo_rules.py` gives clean on 370 files.
- **prove.py:**
  - Every tree is built outside any repository. My first run applied nothing in silence: `git apply` was inside the TUESDAY work tree. Now the program uses `GIT_CEILING_DIRECTORIES` and a reverse check.
  - Stages: C2 tests on the old code give exactly 8 FAIL and 0 ERROR; C5 tests on the old code give exactly 8 FAIL and 0 ERROR.
  - Gap rows: 6 edits outside the two jobs, plus a second workflow file. Each is green at BASE and red after C2.
  - Mutants: 14 for the rules, 6 for the squash scan, 14 for the guard; all 34 killed.
  - Two earlier survivors were closed by strengthening cells: a late NUL byte, and `--cleanup=verbatim` (a body with trailing spaces). A third, "control one copy enough", was closed by a first-copies-only stand-in.
- **scan_faults.py:** BASE's step stays green with a `cat-file -p` that prints nothing, with an omitted object of another branch, with the first line cut and with the block cut. The new step is red on all four. With no final line end, BASE loses an object and the new step copies them all. The clone's porcelain is EQUAL before and after.
- **CodeQL 2.27.4** (`codeql_py.py`, both suites):
  - Control `28d2852d`: 6 results (3 and 3). Main: 0.
  - First prototype: 3 results. One was `py/clear-text-storage-sensitive-data` on a test variable `trusted`; the other was `py/overly-permissive-file` on `chmod 0o755`. Both are fixed in the diffs (`extended`, `0o700`).
  - Final tree (rebased): 0. WORKTREE: 0.
  - C2, C3 and C4 were measured on the `762e774e`-based commits; their `build/` and `.github/` are identical after the rebase.
- **gitleaks 8.30.1:** the planted control gives rc 1; `dir` and `git` over the prototype give rc 0. The neutral step gives 25 of 25, `wrong 0` twice, REACH `not among the stored objects 0`, and `no leaks found`.
- **squash_scan.py with the real scanner:**
  - Each of `msg-1` to `msg-5` gives control `rc 1, found 2` and `SQUASH-SCAN: clean`.
  - A body holding the planted value gives `SQUASH-SCAN: FINDING in the message`, rc 1.
- **Release guard (read only) on lane D's seat's local publish** (`.tools/b1831/out/linux`, `out/windows`):
  - Main's guard and the new guard both give `GUARD: clean (10 files)` and `GUARD: clean (11 files)`; these equal the hosted counts.
  - The new guard with `--release` exits 2 (0 fingerprints).
- **Words:**
  - `words.py` gives `WORDS: 20 hits` on the added lines: 10 seat ids that are Python byte escapes such as `\x28`, and 10 hits from the existing `REVIEWED_*` name family.
  - `words2.py` (D14 allowance) gives `WORDS: clean (6 files)`. Its control fires 13 of 13, and "after the review" and "X26" still count after the allowance.

## Questions for Tuesday (default first; STOP-class marked; the kit's D1 to D14)
- Q1 five commits on one branch, one squash landing. Q2 R6 refuses every backslash outside a block, plus explicit keys and indentation numbers.
- **Q3 STOP-class: R7's list is empty.** Any later lane that tracks a NUL-byte file (a binary fixture, UTF-16 text, SQLite) goes red and must ask. Say in words whether you carry R7 into every live kit.
- Q4 R8 refuses any `filter` attribute. Q5 the whole-file fingerprint is added, the two job fingerprints are kept, and `ci.yml` is the only workflow.
- Q6 three length checks (55, 43008, folder listing). Q7 the reach check is built. Q8 one planted repository per place: not built, because it would change the `PLANTED-CONTROL` line every reader requires. Q9 the batch export: not built.
- Q10 the squash scan runs the control, then the message, in one run; the control needs at least 2 findings. Q11 unopened formats are G3 in every mode, and key stores are G3 in release mode only.
- Q12 the drafter's seven diffs; `words2.py`; READY at Step 0 + 90 and push at Step 0 + 70; a new pane X26 at opus; a G1 gate.
- **Q13 STOP-class: commission less than the tickets** (the table in the kit). Answer in words.

## NOT DECIDED (in the kit)
1. OXPD2-24's packaging-job rule. Built literally it is STOP-class: `ci.yml:48`, `:78` and `:52` publish or build an image, and release mode exits 2 while the CA fingerprint is owed.
2. OXPD2-24's `.pdb`/`web.config` decision, which is a packaging policy for the product owner.
3. OXPD2-21's flagged-message-on-main decision.
4. Whether the tickets move on landing, which is the records pass.

## What each guard change means for seats building after it (FOR TUESDAY; table in the kit)
- **Floor:** `Ran` and `FLOOR` become 84, so readers need `--unit 84 --floor 84`. A seat that branched before the landing reads 60 on its branch run and 84 on its PR merge-ref run.
- **File count:** the rules count is main's plus 2.
- **secret-scan:** the existing proof lines are unchanged (MEASURED locally; DERIVED for hosted), so old readers pass. `hosted2.py --hardened-scan` adds four optional rows.
- **New rules:** no later lane may track a NUL-byte file (R7) or a `filter` attribute (R8). R6 binds only an editor of `ci.yml`.
- **Workflow edits:** any later `ci.yml` edit sets `REVIEWED_WORKFLOW`.
- **Release guard:** default-mode output is unchanged on today's publish. A later publish that gains `.gz`/tar/7z files, the CA name inside a name, or the library name in any binary goes red on `linux`/`windows`.
- **Squash scan:** Tuesday's standing pre-merge step can now run `build/squash_scan.py`.

## Chain inputs (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, the stamp | Tuesday |
| 1 | `<src>` (21 files), the origin, `<repo>` local identity, the CodeQL CLI, gitleaks | drafter folder, GitHub, checkout, TUESDAY tools, Homebrew |
| 2 to 6 | `<clone>` on origin/main, the diffs and messages in `<lane>/gate` | Step 1 |
| 4 | `<clone>/build/squash_scan.py` | Step 4's own apply |
| 5 | BASE's step by `git show`, the new step in the work tree, every origin branch in the clone | Steps 1 and 5 |
| 6 | `prove.py` builds from BASE by `git archive` plus the diffs | Step 1 |
| 7 | the staged tree, the message files | Steps 2 to 6 |
| 8 | the five commits, the origin | Steps 2 to 7 |

## NEVER RUN / UNMEASURED
- **NEVER RUN:**
  - a push, and any hosted run of a lane-I head;
  - Windows, and Ubuntu's `mawk` on the new `awk` (only macOS awk 20200816; POSIX features only, DERIVED);
  - the runner's Python 3.12 on the new cells;
  - the owned-paths property and the Step 7(a) planted-row control on the seat's commits;
  - the rebase rule (main moved during drafting, so I rebased my scratch, not a seat's);
  - `hosted2.py --hardened-scan` PASS on a real head (only its FAIL control on `762e774e`).
- **UNMEASURED:**
  - whether a .NET single-file bundle's member names are in clear (no bundle built);
  - whether the CodeQL CLI opens a socket;
  - how old readers react to the new secret-scan lines on a hosted log (DERIVED from their needles).

## What I did not read
- Lanes A, B, E, F, G, H, SL kits and code.
- The B1836 kit beyond its file name.
- The B1841 kit beyond grep of its section heads and rebase lines.
- `02`, `03`, `05`, `CLARIFICATIONS.md` beyond a grep for C-42 and C-45.
- `SETUP_RUNBOOK.md` beyond a grep for "squash".
- `BACKLOG.md` beyond a grep for the ticket keys.
- The three CI-skeleton verdicts beyond the rows named in the tickets.
- Any decision card.
- Nothing of HPSM-POC. Nothing under `Source_Documents/`. No key folder listed, hashed or opened.

## Reading load (summed by program)
252,661 bytes, about 63,000 tokens. That covers this commission (5,890), the plan (31,441), the push commission (10,255),
DRAFTER_RULES (17,216), the B1844 kit (58,528) and its report (8,481), the five Jira bodies (15,445), main's `ci.yml`, README and
`build/` files read whole or in ranges (about 59,000), the earlier tools' sources (about 22,000), the verdict rows (about 9,700),
and an estimated 9,000 bytes of B1841 grep output. Program outputs I produced are not counted.

## Outside the fences (disclosure)
1. **Unit tests, mutants, CodeQL and the second-scan step ran on this machine** (Python, git, gitleaks, CodeQL; load1 up to 6.1).
   - They ran in my scratch under the TUESDAY tree, never in a project tree, and no dotnet ran.
   - I did not check the wave's heavy lock before running. DRAFTER_RULES forbids tests beside a held lock unless the commission allows it, and my commission does not name it.
   - I checked it after my runs, at 20:40:55: `.tools/wave1-heavy.lock.d` was absent. Whether it was held during my runs (19:55 to 20:38) is UNMEASURED.
2. **I read a seat's folder in the project tree** (`.tools/b1831/out/linux` and `out/windows`, lane D's local publish output) with my prototype release guard and main's. These were read-only file reads that wrote nothing there, to measure that the new guard is quiet on a real publish shape.
3. **Git writes happened only in my scratch clones under d1861.**
   - `main` was cloned with `clone.py draft`: push URL `invalid://no-push`, no identity copied. It was fetched once with the project deploy key, through `GIT_SSH_COMMAND` in one process.
   - `proto` was cloned from `main`, with push URL `invalid://no-push` and a scratch-only identity `drafter scratch <scratch@invalid.example>`. Its history was rewritten three times with `reset --hard` and `am`. Its keep-v1 to keep-v4 branches are left in place.
   - I made no git write in any project tree.
4. **Programs deleted their own temporary folders** under my scratch: `TemporaryDirectory` in my R6/R7/R8 census over 14 refs, and in `squash_scan.py`'s own scratch.
5. **My first `prove.py` run applied the diffs nowhere** (inside the TUESDAY repository, `git apply` skipped them in silence) and reported DIFFERENT. `git status` of TUESDAY then read 0 changed or untracked paths: nothing was written there. The program was fixed.
6. Jira GET only (5 issues), `gh api -X GET` only. No mail, no message, no Artifact, no Docs.
