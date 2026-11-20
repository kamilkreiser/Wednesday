STARTABLE: YES - once stamped. The kit is whole (156 lines, 45326 bytes before the stamp), `stamp_check.py` exits 0 (123 claims, 123 sidecar lines), and the change it orders was built and measured by the drafter: 0 scan results, build 0 warnings 0 errors, 192 tests green. Not run by anyone: the push, the hosted run of the new head, the hosted code scan.

# B1813 DRAFTER REPORT (OXPd 2, WP1.10, the one-line round the product owner allowed; seat X12; delta review B1814)

Written 2026-11-20 by the in-session drafter (Fable). Work from 21:14:30 to 21:33 AEDT (clocks by `date`). Authority as the commission prints it: card `datasec-oxpd-logging-second-review-nogo-1120`, option a, "One more one-line round, then merge" (RELAYED from the commission; the drafter did not open the card store).

## BLUF
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1813_SEAT-X12_oxpd2-wp110-round3-one-test-word.md`, 45326 bytes, 156 lines, 8 lines with a stamp slot (S1 to S7 and the last line), 0 non-ASCII lines; sidecar `.measured` beside it (124 lines).
- **The delta review:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1814_GATE_COMMISSION.md`, 14566 bytes. It is a DRAFT: it holds the word `HEAD40` 21 times (counted by program) where the seat's new sha goes, and one slot for your own reads. Fill both before the Agent call.
- **Question 1 is settled by measurement: the review's measured copy changed BOTH lines, 76 and 90.** `diff` of its two source copies (`/private/tmp/b1804-gate/codeql/src` and `srcfix`) prints exactly those two lines. My changed file has the same blob as its copy: `48216cd70e5a94eb3926e92d3d4c5890367aa410`. So "the measured change" and "the recommendation" are the same change, and the kit orders it.
- **The kit pins the result, not the method:** after the commit the tree must be `c604d74db4b613ff9892205565260e5e83cf4218`. Any other tree is a STOP. A seat cannot land a third line by accident.
- The reviewer's scratch `/private/tmp/b1804-gate/` STILL EXISTS (clone, `codeql/`, `scratch/heavy.py`, logs). I ran nothing in place. It holds no script of the code-scan steps: I recovered the four command lines from its database logs and wrote them as one program.

## Exactly which change the prototype measured, and its three results
The change: in `tests/Datasec.Suite.Logging.Tests/KeyValueShapeTests.cs`, line 76 `...Empty.Add("Password", s).Add("Kept", Kept);` and line 90 `Tuple.Create("Password", s);`, the word `Password` to `Passphrase` in each. `git diff --numstat`: `2 2`, one file. Scratch clone `/private/tmp/b1813-draft/clone` (fetched from the origin with the project's deploy key; push URL `invalid://no-push`), at `6bcd02ed05544e398262dee0f13282abd658255e`.
1. **Scan** (the review's method: CodeQL 2.27.4, `csharp-security-extended.qls`, the extractor's managed program, references from built outputs): changed tree `rules 63 results 0`. **Control FIRED:** the untouched head, same session, `rules 63 results 1`, `cs/cleartext-storage-of-sensitive-information`, 7.5, `KeyValueShapeTests.cs:126`. Both runs: 33 source files, 333 resolved references, 0 unresolved, "Failed to resolve 2 types": the review's own numbers.
2. **Build:** `0 Warning(s)`, `0 Error(s)` (changed tree and untouched head).
3. **Tests:** `total: 192`, `failed: 0`, `succeeded: 192`, `skipped: 0` (both). Detailed run: `KV kvU-at-10 clean`, `KV kvU-pl-10 clean`, `KV kvU-at-17 clean`, `KV kvU-pl-17 clean`, each once.
Also on the prototype commit (made in a copy inside the session scratchpad, tree `c604d74d...`, scratch identity, never pushed): `gitleaks git` no leaks found; the workflow's neutral-scan step rc 0 (`25 of 25`, `objects of this commit not among them 0`; 229 stored objects, 11 commits, with the six branches the origin held at 21:17); unit tests `Ran 53 tests` `OK`; `RULES: clean (46 files)` (hash half not run).
All heavy jobs: 22, through one runner (load1 read first, under 7 required; `mkdir` of exactly `<project>/.tools/wave1-heavy.lock.d`; a time bound; the lock moved into my scratch; the three build settings of the verdict's finding 8; a closed local proxy). The lock was never waited for; highest load1 at a start 6.05; no build process of mine alive afterwards; the lock folder does not exist now. That folder was my only write under the project.

## Does the cell still test what it tested: YES, measured
- `src/Datasec.Suite.Logging/DenyListData.cs:18`: `new("password", ["password", "passwd", "pwd", "passphrase", "otp"]),`.
- Three mutants of the round-2 record, in the review's own wording (its `mutants2.py`), on the changed tree, each undone and proved (`git diff --quiet -- src` rc 0):

| Mutant | With `Passphrase` (mine) | With `Password` (the review's log) | Rows of makers 10 and 17 red |
|---|---|---|---|
| mK1, structure half of the sibling rule removed | 13 failed | 13 failed | `kvU-at-10` |
| mK2, sequence half removed | 4 failed | 4 failed | `kvU-pl-17`, `kvU-at-17` |
| mK3, text rule removed | 26 failed | 26 failed | `kvU-pl-10` |

  The set of failing K01 rows is identical in all three. After the last undo: 192 green.

## The sibling search on the head (its hits)
Program `siblings.py` (control 7 of 7). It lists every text constant in the 16 C# files of the two folders that holds a word the scanner's rule reads as a credential (the rule's own word list, read at source), with its syntactic place. At the head: 61 constants; 18 are arguments of a method call. After the change: 59 and 16.
The 18 at the head:
- **The two of the change:** `KeyValueShapeTests.cs:76` (`Add`), `:90` (`Create`).
- 13 calls that return nothing: `DenyListTests.cs:68` (`AssertRemoved`), `:71`, `:339` (`Assert.Contains`); `KeyValueShapeTests.cs:223`, `:254` and `LogScannerTests.cs:74` (the logger's `Information`); `KeyValueShapeTests.cs:225`, `:256` (`Assert.Equal`); `:290`, `:293`, `:311`, `:312`, `:313` (`Assert.Contains`).
- 2 that return a truth value to an assertion: `DenyListTests.cs:356`, `KeyValueShapeTests.cs:366` (`string.Contains`).
- **1 near miss: `KeyValueShapeTests.cs:95`, `JsonDocument.Parse("{\"Password\":\"" + s + ...)`.** Its result DOES reach the logger. Its argument is a constant joined to a variable, which the rule does not read as a constant argument, and the scan reads 0 with it unchanged. See Q2.
**No other line of the same shape by the rule's own definition.** Read by me at source, each of the 18. Not a data-flow proof: the scan is.

## Questions, each with its default
- **Q1 (which lines):** default both, 76 and 90. Settled above: the measured copy changed both.
- **Q2 (line 95):** default not the same shape, not changed, named in the kit under OUTSIDE THE FRAME and to the reviewer in B1814 item 2. Alternative: you take it to the product owner before the launch as a wider change. My reading: by the commission's loose wording ("a constant holding a credential word whose result reaches a logger call") line 95 fits; by the rule's source and by the measured scan it does not. That gap is yours to rule, not the seat's.
- **Q3 (the seat runs the local scan):** default yes, control at the head first. It makes the seat run the CodeQL program in your tree (`2_Project_Files/tools/codeql/`) and read `fleet/state/s302/d1813/gate/`: named exceptions to the project's read-inside-only rule. Alternative: only the delta review scans.
- **Q4 (history entry):** default one entry, by a program I tested on a copy. Alternative: none this round ("nothing else is added"), records write it after the merge. The ruling's words are about the repository; the project's rules file asks each seat for an entry. Yours.
- **Q5 (commit message):** default the file `gate/commit-message.txt` (750 bytes; subject `Use the key word Passphrase in two key-and-value test makers (WP1.10)`). Word counts 0 in every class of the verdict's item 7 (control 13 of 13). It went through the repository's own neutral-scan step as a real commit message: no leaks.
- **Q6 (a red hosted job):** default STOP, no second commit.
- **Q7 (window, pane):** READY at Step 0 + 60 minutes, push by + 40, pane `Datasec/OXPd2-X12`. Measured machine time for everything a seat runs: under 2 minutes, plus a hosted run of about 2 minutes.

## STOP-severity checks of the kit that I did NOT run on a real output
Each is marked so in the kit (a failure traceable to the kit's wording is `STOPPED: NEEDS TUESDAY`):
1. The kit's REFUSE checks.
2. `clone.py` in mode `seat` (I ran mode `draft`: same clone lines, no identity copy), and the `git switch` after it.
3. The identity comparison of the commit (`%ae | %ce` against the clone's configured address).
4. The restore against the project's own package cache (I restored from a copy; `diff -rq` between the two: 0 lines).
5. The push and its read-back by GET.
6. `hosted.py --wait` while jobs still run, and its verdict on the new head. On the OLD head it prints `PASS` with every count of the verdict's item 6; with a wrong total it prints `FAIL 4`.
7. The history program on the live file (run on a copy; a second run refused).
Every other STOP check ran once on the prototype with its control fired: blob id, tree id, test totals, the four `KV` lines, sibling search at both trees, local scan, word counts, message hash, scope proofs, both secret scans of the commit.

## Outside the frame (kit section OUTSIDE THE FRAME, 8 rows; each STOP AND ASK, no behaviour specified)
The local scan differing from the one measured; the hosted version or rule set differing (hosted `main` by GET at 21:26:01: csharp 63 rules, CodeQL 2.27.4, 0 open alerts, the same as local); another line of the same shape; line 95 and the constructor-built makers; another test file or lane; the Python analysis; a check run beside the four; any local result at the changed tree.

## Reading load of the seat (summed by program)
119598 bytes before the stamp: the kit 45326; `<project>/CLAUDE.md` 10052; `CODEQL-FIRST-PR.md` 7796; the ten files of `gate/` 38065; `KeyValueShapeTests.cs` 18359. The seat does not read the verdict, an earlier kit or an earlier STATUS.

## Inputs of each step
Step 1: the origin branch, the checkout's local configuration, the folder `gate/`. Step 2: the clone; `gate/heavy.py`, `siblings.py`, `codeql_local.py`, `extractor-arm/`; the CodeQL program. Step 3: the clone. Step 4: the built tree of Step 3. Step 5: `gate/commit-message.txt`, `words.py`, `run_step.py`. Step 6: the commit; `hosted.py`. Step 7: the pushed sha; the template and `history_entry.py`. Each exists now or is made by an earlier step.

## What I read, and what not
Read whole: the commission; the verdict folder's eight files; the round-2 kit as stamped (323 lines) and its drafter report; the round-2 STATUS (470 lines, two pages); `DRAFTER_RULES.md`; the project's `CLAUDE.md`; the B1804 commission; the reviewer's `heavy.py`, `setup.py`, `texts.py`, `hosted.py`; the scanner rule's source (`SensitiveActions.qll`, the storage query, the logger sink).
NOT read: the round-2 kit's sidecar beyond its first 25 lines (cut at 600 characters), and its `.pre-stamp`; the four earlier commissions B1804 names; the first verdict and the first kit; the gate standard; the reviewer's `scope.py` and `mutants2.py` beyond the lines a search printed; `KeyValueShapeTests.cs` beyond lines 1 to 20, 58 to 135 and the lines a search printed; the other 15 C# files (each by the lines the search printed); the card store; Jira; anything under `Source_Documents/`.

## My disclosed slips
1. **One git write verb in a clone outside your tree got past the hook:** `git checkout --detach` in `/private/tmp/b1813-draft/clone`. The hook then refused `switch`, `commit` and `fetch` there. I made the prototype commit in a copy inside the session scratchpad, as the hook's own message says. The clone itself was made by a program (the round-2 form), which the hook does not see: the commission ordered that clone.
2. `DRAFTER_RULES.md` forbids a drafter to fetch, test or write more than two files; this commission ordered a clone, a build, tests, scans and four files. I followed the commission. In the project I wrote nothing but the lock folder (made and moved 22 times).
3. The kit's restore differs from the round-2 kit's: audit off and a closed proxy, as the review ran it, because that is what I measured. The round-2 seat's audited restore is not in this kit.
4. Two of my shell lines read `$?` after a pipeline (a hook warned). The proof in both is the printed line, not the code.
5. Two absences rest on a search with no positive control in the same command: "no pane named `OXPd2`" and "no build process of mine alive". Your S3 read covers the first.
6. I first wrote that `HEAD40` stands 12 times in B1814; a program counted 21 and corrected the sentence.
7. `words.py` matches B-numbers without regard to case, so it flags a branch name. The commit message holds none; the history entry names the branch and is not run through it.
8. The sidecar: 39 of 123 lines say "instruction, nothing to run". On kit lines 79, 88 and 131 the checker pairs backticks across two code spans and picks up prose between them; those lines carry no literal of their own.
9. Scratch left: `/private/tmp/b1813-draft/` (781 MB, mostly a copy of the package cache; the clone holds the two changed lines uncommitted), the commit copy in the session scratchpad, and `fleet/state/s302/d1813/` (31 MB: the tools, the extractor's 43 files, copies of five reviewer programs and three SARIF files). Nothing deleted. My first sidecar was moved to scratch, not removed.
10. Nothing pushed, opened, merged or sent. No Jira, no GitHub write. Hosted calls: `gh api -X GET`, one `git ls-remote`, one clone.
