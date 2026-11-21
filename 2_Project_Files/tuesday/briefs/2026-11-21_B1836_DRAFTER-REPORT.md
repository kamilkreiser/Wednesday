STARTABLE: YES - on one condition: Stamp S4 must answer Q1 in words. Adding seven planted controls means `FLOOR` in `ci.yml` has to go from 53 to 60 in the same commit; without that the `rules` job goes red (MEASURED). The commission told this lane to STOP before touching `ci.yml`, so the kit refuses to start until S4 answers Q1.

# B1836 drafter report: lane R5 (seat X21), the R5 exemption for HP's listed inputs and the key-folder prune

Drafted 2026-11-21, 17:00:09 to 17:17:16 AEDT (clocks by `date`), by an Opus drafter. Kit: `2026-11-21_B1836_SEAT-X21_oxpd2-r5-hp-inputs-exemption.md` (61962 bytes, 236 lines, 0 non-ASCII bytes) with its sidecar `.measured` (129 claims, 129 measured; `stamp_check.py <kit>` exit 0). Scratch and tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1836/` (`gate/` is what the seat copies; `logs/` holds every run cited below).

## BLUF
- Today R5's hash half, run locally against the supplied folder, reports the 37 tracked HP inputs: 37 lines, set-equal to `inputs.sha256`, rc 1. I measured this with `main`'s own judge; only its walk was replaced by the pruned walk, so no key folder was hashed.
- The change does two things:
  - **The exemption.** A tracked file is exempt only when the pair (its path, its sha256) is one well-formed line of the tracked list.
  - **The prune.** The walk drops every key folder before descending into it, and skips key files by name before any stat or open.
- On the real folder the prototype reads:
  - 4 key folders pruned and 35210 files hashed.
  - 37 files exempted, `RULES: clean (291 files)`, rc 0.
- Real-folder controls, run on a scratch clone of BASE:
  - A copy of a listed input planted at `docs/control.json` is reported.
  - Two listed inputs with their bytes swapped are both reported.
  - The exempted count drops to 35 (`R5-CONTROLS: PASS`).
- **Unlike the earlier build kits, I ran the whole change myself.** The seat applies my three sha-checked diffs in order (tests first) and re-proves each stage. Python only: no dotnet, no lock.

## What I measured, and how
1. **The origin and the base hosted run.** `gh api -X GET` under the project `GH_CONFIG_DIR`, at 17:00:09 and again at 17:09:12 and 17:17:16:
   - main `5e36d8dc` throughout; pull requests 1 to 6 all merged, 0 open.
   - `b1831/wp15-token-broker` pushed at `70c1fad5`; no `b1836` ref; 0 open code-scanning alerts.
   - The base hosted run, read with my `hosted.py` copy: linux and windows `total: 894` (skipped 4 and 19), `RULES: clean (291 files)`, `Ran 53 tests`, PASS.
   - Control: with `--ran 60` it prints `FAIL 2` on exactly the two `ran 60` rows.
2. **My scratch clone of `5e36d8dc`.** Cloned from the b1831 seat's clone by `file://` (a read), with its push URL set to invalid. Its read-only baseline: 291 tracked files, `Ran 53 tests` OK, and R5 in the hosted form `RULES: clean (291 files)`.
3. **The prototype.** Three diffs (tests, code, floor), applied to a fresh scratch clone of `5e36d8dc` in that order, running the full `build/tests` suite after each:

   | After | Result |
   |---|---|
   | tests diff | `Ran 60`, `FAILED (failures=7)`, 0 errors (6 R5 cells, plus the floor cell `[53] != [60]`) |
   | code diff | `FAILED (failures=1)`, the floor cell only |
   | floor diff | `Ran 60` OK; the rules-job fingerprint test still passes (the fingerprint reads `FLOOR=N`) |

   - All three resulting files are byte-equal to the prototype clone.
   - `run_step.py 'planted controls'` (the workflow's own step) printed `Ran 60 tests`, `UNIT-TEST FLOOR: ran 60, floor 60`, OK, and porcelain EQUAL.
4. **Mutants** (`mutants.py`, run in `mut/` folders only, never touching a supplied folder):
   - `main`'s code gives 6 red.
   - m1 to m6, m9 and m10 each turn their own cell red.
   - m7 (case-insensitive regex) is EQUIVALENT, and I say so in the kit.
   - My first `..`-segment check was also equivalent. I removed it from the code; string equality with `git ls-files` names already covers it.
   - Result: `MUTANTS SURVIVING: 0`.
   - One test fix: the first K1 failed against `main` with a PermissionError (an ERROR, not a red). I wrapped it, so it now fails by assertion.
5. **Real supplied folder** (17:04:50 to 17:04:54):
   - The prototype's output is in the BLUF; `before.py` gives the 37-line baseline.
   - A names-only census (`census.py`) pruned folders before descent and opened no file. It found 3 `certificates` folders plus a `CypherKey-cypherkey/cert` folder, and 0 key-extension files outside them.
   - Review B1830 counted 35215 files with only the two `tools/certificates` folders pruned. So 5 files sit in the other two folders (DERIVED).
6. **Text checks.**
   - `words.py --control` gives 13 of 13, and the scan is clean over the added lines and the commit message (2 files). The first docstring held "review" once; I reworded it.
   - gitleaks 8.30.1: planted control rc 1; the clone rc 0; the four neutral copies rc 0.
   - ASCII check: 0 offending lines per changed file; the U+200B control fires.

## Decisions (D) and Questions for Tuesday (Q), each with its default
- **Q1, STOP-CLASS (`FLOOR`).** Default A: `FLOOR=53` becomes `FLOOR=60` in the same commit. That is what `test_pipeline_controls.py`'s own docstring requires, and the fingerprint does not move. Alternative B: leave `ci.yml` alone and fold the cells into subtests. B is a STOP in this kit because the diff for it is not written.
- **Q2 (D1, D2): the exemption key and the line form.**
  - The key is the pair (path, sha256).
  - A line must match `^([0-9a-f]{64})  (hp/[!-~]+)$` exactly.
  - A malformed line exempts nothing and is not itself reported.
- **Q3 (D4):** the extension half exempts nothing.
- **Q4 (D3):** the list must be tracked; a path listed twice exempts nothing.
- **Q5 (D5): what the prune covers.**
  - Folder names, any case: `certificates`, `certs`, `cert`, `keys`, `key`.
  - Key files: `.key`, `.pem`, `.pfx`, `.p12`, `.jks`, `.keystore`.
  - A supplied root that is itself a key folder is not walked.
  - Alternatives: `tools/certificates` only, or DRAFTER_RULES' minimum.
  - Named limit: a renamed tracked copy of a pruned file escapes the hash half.
- **Q6 (D6):** two new note lines, printed only when the hash half runs. The hosted output does not change (MEASURED).
- **Q7 (D7, D8):** the seat applies the drafter's diffs, and `judge` keeps its old call form.
- **Q8:** `README.md:71` (the R5 line) and `<project>/CLAUDE.md:50-51` (the no-copy rule) are not this lane's to change. Both go to FOR TUESDAY.
- **Q9:** READY by Step 0 + 90 minutes, push by Step 0 + 60, pane `Datasec/OXPd2-X21`.
- **Q10:** gate tier G1.

## Literal-check proof (MEASURED LITERALS rule 4)
Every step's inputs either exist at BASE or come from an earlier step:
- The diffs and tools come from `<src>`.
- The clone comes from Step 1; `predictions.txt` is written before any change.
- Steps 2 and 3 apply the diffs in order. Step 3's sha256 check reads Step 3's own output.
- Step 4 uses the clone's working tree. `r5_controls.py` clones BASE itself.
- Step 5 reads the staged tree. `run_step.py` on the neutral-scan step runs after the commit, as written.

## Not run (UNMEASURED)
- No push, no hosted run of this change, nothing on Windows (the `windows` leg runs no Python tests).
- The hosted runner's Python version, and the user it runs as (H13).
- The seat's `git log` identity check and the read-back.
- `run_step.py` on the neutral-scan step for this change (it needs a commit).

## What I did not read
- Kit B1829's whole body. I read its section headings, Q1, Stamp S4 and the R5 lines found by grep.
- Kit B1831: everything except the REQUIRED SECTION's table rows (lines 117 to 141 in part).
- B1830's FOR-RECORDS, landing and texts files.
- `SETUP_RUNBOOK.md`.
- The B1829 STATUS beyond its section list and DEVIATIONS.
- The design documents.
- The other lanes' kits (they were being written alongside this one).

## Reading load (the seat's)
The kit (61962 bytes) plus about 99.8 kB: `CLAUDE.md` 10052, `CLARIFICATIONS.md` 33300, the six tool headers 5815, four repository files 34926, the three diffs 15699. Total about 161.7 kB.

## Outside the fences
- **My first names-only census listed the entries of the `CypherKey-cypherkey/cert` folder.** It was not yet in my prune set. Nothing was opened, hashed or printed except a total, which was 0 key-extension files. I then added the name to the default prune set.
- Two of my bash calls first used `$S` inside `git -C`, and the hook refused them. I re-ran them with literal paths in my own scratch.
- No git write outside my scratch clones, which have invalid push URLs. No Jira call, no project-tree write, no message.

## Owed records (for the records kit)
- The product owner's 2026-11-21 ruling to keep the 37 files, and his 09:40 words, have no entry in `CLARIFICATIONS.md` (0 hits; control `## C-45` 1).
- `CLAUDE.md:50-51` still states the no-copy rule unamended.
- `README.md:71` will understate R5 once this lane lands.
