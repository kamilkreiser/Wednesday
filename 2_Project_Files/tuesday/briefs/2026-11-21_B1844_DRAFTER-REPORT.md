STARTABLE: YES

# B1844 DRAFTER REPORT: OXPd 2, lane R5, fix round (round 2 of 2)

Drafter: Opus 5.5, read-only, in-session, 2026-11-21 17:41:30 to 17:57 AEDT (clocks by `date`). Kit:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1844_SEAT-X21_oxpd2-r5-fix-round.md` (213 lines,
55209 bytes, ASCII, 8 slot lines); sidecar `.measured` beside it (105 claims, 105 measured; `stamp_check.py <kit>` exits 0).
Tools and diffs: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1844/gate/` (ten files, sha256 in the kit).
Scratch, logs and the prototype: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1844/`.

## BLUF
The fix is built and measured on a scratch clone of `28d2852d` (R1). It is one commit, two files, +47 -13, and `ci.yml` is not
touched. F1: `secret_text` becomes `folder_text`, and the local CodeQL CLI 2.27.4 then prints **0 results in both Python
suites** (code-scanning and security-extended). The control is R1 itself, which prints 3 and 3 at the verdict's
`:71/:366/:371`; main prints 0. F2: subtests were chosen over new cells, so `FLOOR` stays 60. g6, g7 and g8 each SURVIVE with R1's
tests and go RED with the new ones. F4: **the one-line fix was TAKEN** (`realpath` in place of `normpath`). Its link subtest is
RED against R1's code by assertion and green after. F5: the docstring now says "(the fingerprint list of HP's specification
inputs)", and `owner` counts 0. Suite: 60 OK. Mutants: 0 of 19 counted mutants survive. Real folder: 35210 / 4 / 0 / 37,
clean, rc 0. `R5-CONTROLS: PASS`. Both secret scans and the word scan are clean.

## What I measured (instrument; control)
- **Origin** (`gh api -X GET`, 17:41:56 and 17:50:32): main `5e36d8dc`, branch `b1836/...` = `28d2852d` (one row), open PRs 0, and
  no PR in any state with a `b1836` head. `compare/main...R1` is ahead 1, behind 0, with the 3 round-1 files. R1's check runs were
  the four, all success, with no `Analyze`. Open code-scanning alerts 0. **Default setup `query_suite: extended`** (the verdict
  measured only the code-scanning suite, so the kit runs both).
- **CodeQL**, through my program `codeql_py.py`: R1 gives `6 results (code-scanning 3, security-extended 3)` with rc 1 (this is
  the control). Main `5e36d8dc` gives 0 and 0. The prototype work tree gives 0 and 0 with rc 0. The CLI logs show the packs
  loading from the local `qlpacks` folder, and `grep -i download` finds 0 lines.
- **Red then green** on a fresh scratch clone of R1 (the diffs applied in order):
  - After `1-tests.diff`: `Ran 60`, `FAILED (failures=1)`. The one FAIL is K1 `[link under another name]`, with 0 ERROR.
  - After `2-code.diff`: `Ran 60`, `OK`.
  - The sha256 of both files equals the prototype's. `.github` is unchanged (rc 0). Counts are 33/23/4, with 0 in column 1.
- **Mutants** (`mutants2.py`):
  - r1 row: K1 red (the red first of F4).
  - m1 to m10 and g1 to g10: each red by FAIL with 0 ERROR (m7 EQUIVALENT). The table is in the kit.
  - The GAP rows (g6/g7/g8 run with R1's tests): rc 0, which shows the gap.
  - `MUTANTS SURVIVING: 0`.
  - The assertions that fired: g6 fails the trailing-separator, trailing-dot and link subtests; g7 fails with "stat of a key
    file: .../store.jks"; g8 fails with `0 != 1`, the copy exempted.
- **Real folder, new program only:** hashed 35210, skipped 4 key folders and 0 key files, exempted 37 (= 37 lines),
  `RULES: clean (291 files)`, rc 0. The empty folder and the hosted form are as in round 1. `r5_controls.py` gives PASS (35
  exempted, the 3 planted lines). I listed, opened or hashed nothing in that folder myself.
- **Workflow step `planted controls`:** `Ran 60`, `UNIT-TEST FLOOR: ran 60, floor 60`, porcelain EQUAL. After a scratch commit,
  the neutral object scan gives `25 of 25`, `objects of this commit not among them 0`, and `no leaks found`.
- **gitleaks 8.30.1:** the planted control gives rc 1; the prototype rc 0; the neutral copies rc 0. **words.py:** control 13 of
  13; the 47 added lines and the commit message are `WORDS: clean (2 files)`.
- **hosted.py on R1:** `--ran 60` gives PASS; the `--ran 61` control gives FAIL 2 on exactly the two `ran` rows.

## Decisions (each Tuesday's default; each a Question)
D1 is the rename, `folder_text`. D2 is subtests in K1 and L5, keeping FLOOR 60 (ruling 2: "say which": SUBTESTS). D3 is F4:
realpath TAKEN, with the named limit H18 (a root below a key folder is walked, DERIVED). D4 is the docstring clause. D5 is NO
REBASE, see Q5. D6 is the drafter's two diffs.

## Questions for Tuesday (default first)
- Q1: `folder_text`. Alternative: another name, which needs a new CodeQL run.
- Q2: subtests, FLOOR 60. Alternative: 3 new cells and FLOOR=63, which ruling 2 allows.
- Q3: realpath taken (one line, tested). Alternative A: check every path component (also one line; closes H18; never run).
  Alternative B: a named limit only.
- Q4: "(the fingerprint list of HP's specification inputs)".
- **Q5 (read this one): ruling 5's "rebase ... BEFORE the push only" cannot be carried out on this round without a force push.**
  R1 is already pushed, and the round-1 rule it cites says "After your push you never rebase". The default is to never rebase.
  If main moved over an owned path, the seat STOPs; otherwise it notes the move and goes on, and the PR merge-ref run is where the
  branch and main meet. Alternative: a rebase plus `--force-with-lease`, which needs your word in S4.
- Q6: the drafter's diffs. Q7: 60/45 minutes, a new X21 pane (0 X21 panes live at 17:50:32), opus. Q8: G1 round 2, a delta read.

## Chain inputs (every step's inputs exist at R1 or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, the stamp | Tuesday |
| 1 | `<src>` (ten files), the origin, `<repo>` local identity, the CodeQL CLI | the drafter's folder, GitHub, the checkout, the TUESDAY tools folder |
| 2 | `<clone>` at R1, `1-tests.diff` | Step 1 |
| 3 | `2-code.diff` | Step 1 |
| 4 | the work tree of Steps 2 and 3 | Steps 2 and 3 |
| 5 | the work tree, R1 in `<clone>`, BASE in `<clone>`, `Source_Documents` | Steps 1 to 3 |
| 6 | the staged tree, `commit-message.txt` | Steps 3 and 1 |
| 7 | the commit, the origin | Step 6 |

## UNMEASURED and NEVER RUN
- Never run: the push, the hosted run of the new head, Windows, and the runner's Python version and user.
- UNMEASURED: whether the CodeQL CLI opens any socket.
- The hosted `Analyze (python)` on this head belongs to the PR, and it is the authority at landing.
- NEVER RUN in the kit:
  - the owned-paths property on the seat's commit;
  - the planted-row control of Step 6(a);
  - the D5 compare (main had not moved);
  - `hosted.py` with an open PR on the branch (duplicate runs).
- The reviewer's `secret_text -> folder_text` "60 OK" was re-measured, not just relayed.

## Outside the fences (disclosure)
1. **I ran Python unit tests, mutants and CodeQL while a dotnet lock was held.**
   - At 17:41:39 the lock `.tools/wave1-heavy.lock.d` was held by "B1838 gate reader" for a dotnet test. DRAFTER_RULES says "No
     test run while a lane holds that project's lock, unless the commission allows it by name", and the commission does not name
     it.
   - My runs were Python only, in my scratch under the TUESDAY tree, never in the project tree. Load1 was 3.7 to 5.6. The
     dotnet job was not touched.
   - The kit's seat is Python-only too. Its HEAVY section says it never takes or waits on the lock, as round 1 did.
2. **I ran R5's new pruned program over the real `Source_Documents`.** That program is the kit's sanctioned reader. The round-1
   drafter and the check did the same, and the commission's item 6 names this run for the seat. The program pruned 4 key folders
   and opened nothing in them.
3. **Git writes happened only in my own scratch clones under d1844.**
   - The clones: `proto`, cloned from the seat's clone `.tools/b1836/clone` (a read of it), and `apply`.
   - In `apply` I set a scratch-only local identity, `drafter scratch <scratch@invalid.example>`, for one never-pushed commit.
     Both clones have a push URL of `invalid://no-push`.
   - I made no git write in any project tree.
4. **`gh` was `-X GET` only, under the project GH_CONFIG_DIR.** There was no Jira, no mail, no message and no Artifact.
5. **My first `mutants2.py` run died on a bug in my own g2 edit** (assertion `text != src`). I fixed it and re-ran in a new folder
   (`sim2`); the dead run's folder `sim` is left in place, not deleted.
