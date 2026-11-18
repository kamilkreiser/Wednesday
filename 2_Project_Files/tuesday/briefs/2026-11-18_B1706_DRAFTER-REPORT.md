STARTABLE: YES (kit B1706 / SEAT-M159, MPSCALC-412; stamp_check exits 0, 67 of 67 sidecar lines measured; 8 `____` slots left for Tuesday)

## BLUF
Builder kit drafted for the one-phrase correction of the last sentence of the PANEL-BLOCK lineage note (`src/MpsCalc.Import/PriceBookImporter.cs:150`) plus one new test row. Measured in a scratch copy of main `8ae5db6e` (tarball by `gh api -X GET`, never the project folder): base 197 passed, RED 1 failed of 198 (the new row, `Sub-string not found`), GREEN 198 passed, three mutants each turn exactly the new row red, restored blob equals green blob. Model Sonnet (`BRIEF_SEAT_LEVEL=sonnet` in the launch line), row C2 (`model-routing.md:92`), gate tier G2 (`:109`). docs/IMPORTER.md: no change (see Q1). MPSCALC-413 (`.github/workflows/ci.yml` only) is disjoint: this lane touches no `.github` path and grants nothing there.

## Frozen words
OLD last sentence: `They are outside the approved workbook, so the parity proof counts them per sheet against the recorded section and does not compare them (compatibility basis \"{PanelBlockBasis}\").`
NEW last sentence: `They are outside the approved workbook, so the parity proof counts the section's SKUs per sheet against the store and checks that the store holds exactly the owed (device, SKU) pairs, each once, but does not compare the panel records with the approved workbook and does not re-read the book (compatibility basis \"{PanelBlockBasis}\").`
Replaced phrase runs from `so the parity proof` to `(compatibility basis`; the interpolation and every other byte are untouched. ASCII (python isascii True; replace() of old->new over the whole file equals the edited file; only line 150 differs).
Word-by-word table against ParityProof.cs lines (:91-94, :112-113, :148-149, :175-203) is in the kit FACT 4; sidecar prints the key lines.

## Facts re-measured (instrument)
- Main `8ae5db6ea4ea1fb99a7e306d90e36111b6128d9d` (`gh api -X GET git/ref/heads/main`); open PRs 0; `matching-refs/heads/b1706` 0 (control `b1671` 1). PR #212 is the template's landing.
- Ticket MPSCALC-412 read whole by own GET-only helper (`fleet/state/s289/d1706/jget.py`): Backlog, 0 comments; control `key = MPSCALC-361` reads Done.
- Ruling card read with `decision_queue.sh show` (read verb only): client_project Datasec/MPS, ruled choice a, 2026-11-18 11:22.
- Toolchain `<project>/.tools/dotnet-10.0.404` prints 10.0.404. Heavy slot 1 taken by mkdir, holder moved to scratch, dir removed; 0 locks now. Load1 6.06 then 4.81 (100 s apart, not 120, not independent).
- Base: build 0 warnings 0 errors; Import tests Passed 197/197. RED: Failed 1, Total 198. GREEN: Passed 198/198, numstat src 1/1, test 15/0, diff --check rc 0. Mutants (green source with one change): m1 old phrase back, m2 "and does not re-read the book" dropped, m3 ", each once" dropped: each 1 failed of 198 on the new row only. Predicted head blobs: source `9a9e01dd...`, test `8daf8da9...` (base `b28b2b9a...`, `3ed8d982...`).
- Census (grep of every tracked file of main): the old sentence lives in the importer only; the only reader of the note's text in code is `PanelSectionEndTests.cs:174-177` (a different part of the note); 0 lineage readers in Api, Engine, web, tools, scripts, infra; no tracked store/golden file holds the string.
- Ports: none. No Datasec/MPS pane live (tmux list filtered mps: 0 rows).
- Input/output table: the chain is two steps; RED needs only base files; GREEN needs the RED row (made by the earlier step).

## D-decisions
- D1: the test pins the whole new phrase (Ordinal) and also `DoesNotContain("does not compare them")`; chosen so dropping any clause of the sentence reddens the row (m2, m3 prove it).
- D2: "against the store" for the count clause (the code counts section SKUs against the panel records plus the map-held SKUs, both in the store); "owed" kept as the ticket and ruling word.
- D3: no doc change, no edit of the stale comment at `PanelOptionImportTests.cs:12`.

## Q for Tuesday (default)
- Q1 docs/IMPORTER.md: `:17` says `prove` "counts them and compares the governed options only" and `:88-95` already state the pair check and "does not re-read the book". Not contradictory (the comparison with the approved workbook covers governed options only), so default: no doc change; `:17` is narrower, not wrong; your call whether it is a records-pass item.
- Q2 "owed" has no gloss in the note itself (the sentence before it says each row is an option of every mapped device unless the map pairs them). Default: kept. The product owner's after-landing listing could add a plain gloss if wished; not a code change.
- Q3 held stores keep the old note until re-imported (reported only).
- Q4 stale sibling words: `tests/MpsCalc.Import.Tests/PanelOptionImportTests.cs:12` comment says the proof "counts them only". Not in this lane's paths; default: list for the records pass.
- Q5 the sentence says the proof cannot see a device with no recorded cell only by silence (the code comment at ParityProof.cs:151-152 and docs :91-93 say it); the sentence says "the owed pairs", which is the code's own definition. Default: accept.

## UNMEASURED
- Hosted CI, CodeQL, the whole-solution test (Api, Engine): not run by me; no test outside Import reads the note text (census).
- gitleaks and the identity scans are seat steps; not run by me.
- The B1703 records kit and any MPSCALC-413 kit contents were not read (names only).
- The `.measured` lines for pure kit-label literals are `grep -c` over the kit itself, a presence check, not a tool run.

## Outside-the-fences disclosure
- Scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1706/` (clone from the tarball with a scratch `git init` and commit, jget.py, logs, sidecar builder). A project-folder write happened only via the project's own heavy-lock protocol: `.tools/.heavy-lock-1` created with a holder file, then holder moved out and the directory removed (0 locks after). Package restore by `dotnet build` (allowed).
- One tool call was refused by a hook (`git init` via a shell variable path was read as outside the folder); retried with the literal path inside the scratch. Nothing else refused.
- Read `decision_queue.sh show` for the one ruled card into a scratchpad file; no list, add, rule, amend or withdraw. Jira GET only. `gh api -X GET` only (refs, pulls, tarball).

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1706_SEAT-M159_mps-lane-panel-note-parity-sentence.md` (+ `.measured`)
- Report: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1706_DRAFTER-REPORT.md`
- Scratch (green source, logs): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1706/`
