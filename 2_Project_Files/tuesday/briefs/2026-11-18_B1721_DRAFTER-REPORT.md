STARTABLE: YES - after Tuesday stamps the 8 slots; stamp_check.py exits 0 (73 claims, 73 measured); words frozen from printed code lines; one lane, one path, comment lines only.

# B1721 DRAFTER REPORT (kit: 2026-11-18_B1721_SEAT-M161_mps-lane-m-e-stale-class-comment-414.md)
Drafted 2026-11-18 about 23:08 to 23:15 AEDT (clock reads by `date`: 23:08:52, 23:09:07, 23:10:45, 23:13:54, 23:14:46).

## BLUF
MPSCALC-414 at main 51ed36eb958c33ed83703eba7e81c5b7bea261fe (MPS #215 landed). Line 12 of `tests/MpsCalc.Import.Tests/PanelOptionImportTests.cs` is replaced by three comment lines whose every word is read against `ParityProof.cs` lines I printed. One path differs; head blob predicted `0c48e9803fb8f99b15e32a2ed2539b8aeec1ef5e`; base blob `bf60a393a54ba4ff9422808c14e62a0c761d461c`. docs/IMPORTER.md:17 is untouched, per Tuesday's ruling. Gate G3, Sonnet. Records (Jira comment/move, C-entry) are named in the kit as NOT this lane's.

## Facts re-measured (instrument -> result)
- main sha: `gh api -X GET .../git/ref/heads/main` -> 51ed36eb...; open PRs `pulls --jq length` -> 0; `matching-refs/heads/b1721` -> 0 (control `heads/b1706` -> 1).
- MPSCALC-414 whole, own GET-only Jira helper in scratch: Backlog, label records-pass-1118, updated 12:36, 0 comments; scope sentence quoted in the kit ("no identifier, attribute, assertion or test row changes"). Control: MPSCALC-361 reads Done.
- C-109 (`awk NR==2716` of CLARIFICATIONS.md; settles line :2720) read: developer-only sentences are corrected from the code without the product owner's word review. C-181 (:3474-3485) read: #214/#215 landed, 414 filed, stale comment named as work owed.
- Old line 12 (printed by awk over the tarball): `...They are outside the approved workbook: the parity proof counts them only.`; phrase count over docs, src, tests, .github -> 1 (control: `They are outside the approved workbook` same line 1). File has 0 CRLF and ONE non-ASCII character (U+2026, line 57): the kit forbids any whole-file rewrite.
- ParityProof.cs lines printed and cited: :89-94 (governed), :112-113 (not from the book), :148-149, :175-203 (counts), :190-201 (owed, SequenceEqual, refusal). PriceBookImporter.cs:150 already carries the #215 sentence (blob 9a9e01dd).
- Frozen replacement: python applied it to a copy: non-comment remainder equal base (True); old phrase 1 -> 0; added lines ASCII, max 127 chars; `git hash-object` -> 0c48e980...; scratch git repo base/head: `diff --name-only` -> the one path, grep -c -v -x -> 0 (planted docs path -> 1), `diff --check` rc 0, numstat `3 1`.
- New-sentence grep: `the parity proof counts the` at head -> 3 files (this comment, PanelSectionEndTests.cs, PriceBookImporter.cs), one hit each.
- Census: no program reads the comment; `PanelOptionImportTests` is named in 1 file of src/tests/docs/.github together (itself); `counts them and compares` -> docs/IMPORTER.md:17 only.
- Toolchain: `<project>/.tools/dotnet-10.0.404/dotnet --version` -> 10.0.404; global.json pins 10.0.404, rollForward disable. CI `.github/workflows/ci.yml:42-43`, `TreatWarningsAsErrors` named at :41.
- Panes: `tmux list-panes -a` filtered for mps -> 0. Heavy locks -> none (`ls` no match). `df -g` -> 1070 GiB free. Load1 6.22 at 23:10.
- Model: `models_latest.json:23` claude-sonnet-5-5; routing row L1 `model-routing.md:80`; gate G3 `model-routing.md:110`.

## D-decisions (mine)
- D1: one line becomes three lines (the file wraps at about 127). D2: added the word "panel" ("the panel section's SKUs") so the comment stands alone. D3: no RED test step, since this lane adds no test; the proof is the comment-only program (strip `///` lines, remainders equal, control planted) plus old-phrase count 1 -> 0 plus build/test counts equal to the seat's own base counts. D4: the 198 test count is RELAYED (ticket, C-181) and the kit tells the seat to measure its own. D5: kit says the records seat is Tuesday's to commission after landing (assertion about Tuesday's plan; edit if wrong).

## Q-questions for Tuesday
- Q1 (docs:17): left alone as ruled; default stands.
- Q2 (3 lines vs the ticket's "comment line"): default three lines.
- Q3 ("panel" added): default kept.
- Q4 (model row): L1's S55 column reads "esc (build seat)", not "1st"; I cited it honestly with C2:92 as the "1st" comparison. Default Sonnet per your instruction.
- Q5 (S0-S6 stamps, launch): unchanged from the B1706 shape; S6 READY target is Step 0 + 30 minutes (B1706 used 45).

## UNMEASURED
No dotnet build or test was run by me (the seat measures base and head counts; 198 is relayed). gitleaks exists at /opt/homebrew/bin/gitleaks but was not run. Hosted CI and CodeQL not run. The ban-list name scan is by reference to GATE-VERIFIER-STANDARD step 7 (path cited, list not copied). The B1706 `Failed:     0` literal is measured only as present in the B1706 kit, not re-run.

## Outside-the-fences disclosure
Read-only: Jira GETs (MPSCALC-414 and -361) with the project's .env in-process, never printed; `gh api -X GET` under the project GH_CONFIG_DIR; tarball of main unpacked in my scratch; one `dotnet --version` call (the toolchain binary, version only); `ls -d` on `.local` and `Source_Documents` for existence only (both absent); `command -v gitleaks`; tmux list-panes. I created a scratch git repo with a local scratch identity under `fleet/state/s291/d1721/gs` (not a Datasec repo). I did not read any card, `fleet/briefs_staged/`, the scoreboard or the ledger. I read B1706's STATUS and the project's CLARIFICATIONS.md by line ranges only. Two Bash calls were refused by hooks (a `cd`, then an `rm -rf`) and re-issued without them. Writes: the kit, its `.measured` sidecar, this report, and scratch under `fleet/state/s291/d1721/`.
