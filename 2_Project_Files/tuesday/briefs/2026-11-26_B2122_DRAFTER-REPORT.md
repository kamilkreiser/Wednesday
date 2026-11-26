STARTABLE: YES

# B2122 DRAFTER REPORT: OXPd 2, lane OX-B kit 1 (the lab tool `oxpd1`: LabFiles.cs, its tests and the Lab README), seat X78

Drafter: read-only Opus agent in Tuesday's session (s330). First `date`: `Thu 26 Nov 2026 12:07:47 AEDT`; sidecar written `Thu 26 Nov 2026 12:26:38 AEDT` (its first line). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s330/d2122/` (below `<d>`).

## Files written
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2122_SEAT-X78_oxpd2-lane-b-lab-oxpd1.md` (93063 bytes; 9 slot lines `____`, S1 to S8 and the last line; printable ASCII, `grep -c -E '[^ -~]'` 0).
- Sidecar: `.../2026-11-26_B2122_SEAT-X78_oxpd2-lane-b-lab-oxpd1.md.measured` (227 claims, 227 measured; `stamp_check.py <kit>` rc 0, `<d>/logs/stamp-check.out`).
- This report.
- Seat tools (in my scratch, for `<src>`): `<d>/seat-tools/` = `clone.py`, `hosted3.py`, `run_step.py`, `words.py` (kit B2109's, sha256 equal), `heavy.py` (canonical `31adedc8...`), and this kit's `checks_b1.py` (`d60a4886...`), `mutants_b1.py` (`255b22d0...`), `commit-message.txt` (`f7ad9bae...`, 373 bytes, subject 315 characters).

## BLUF
1. Kit 1 of 2 for lane OX-B, the commission's default split: owed **108** (undo-owed names an unopenable run folder and an unlistable session folder as unreadable, exit 11), **111** (six shapes pinned, test only), **145** (button arm named, default throws), **142** (certificate bound on bytes read through a stream, links followed), **127** (`RealPath` walks part by part by each link's own text), **150** (Lab README callback sentence; the whole Known-not-changed bullet removed, since 127 closes its first half).
2. Five files changed, none added: `LabFiles.cs`, the Oxpd1 `README.md`, `Oxpd1WriteTests.cs` (U06, U07, U08), `Oxpd1CaStoreTests.cs` (U09), `Oxpd1TestServiceTests.cs` (S16). 17 new cases, 6 PREDICTED red on BASE, six mutants, all in `LabFiles.cs`.
3. PREDICTED totals: Lab executable 297 -> 314; whole solution 2367 -> 2384 (succeeded 2380, skipped 4; Windows 2363 / 21); rules 679 unchanged.
4. **The precondition the commission set is met already:** R330 ended `READY B2115: 42f4d663... | C-89 | ticked owed 93 94 126 133 134 143 146, in part 85, new owed 148 to 151 | jira comment 41510` (its STATUS last line at 12:24:59), its pane is gone, and the live `BACKLOG.md` holds item 150 and the seven ticks. `main` is still `c73cda4c`.
5. Same model as B2109: the seat writes the code to a per-symbol specification (the drafter cannot build: the wave lock is inside the project). Every red/green/mutant number is PREDICTED; a miss stops the seat with a question to Tuesday.

## Facts re-measured (instrument, control)
- Origin (`gh api -X GET`, project `GH_CONFIG_DIR`, account `kamilDatasec`; 12:08:10 and 12:24:56): `main` `c73cda4cdf7bf5cd1c6c43cfc20a4c5c400c3809`, one parent `8757daa6`, tree `dd15534f`; open PRs 0; `matching-refs/heads/b2122` 0 (control `b2109` 1); private true, push true; `compare/8757daa6...c73cda4c` lists 10 files, all in the adapter folders (PR 54 touched no lab file).
- BASE tree: tarball by GET into `<d>/src_c73c`; `git write-tree` in a scratch index printed `dd15534f...` (equal to main's tree); 679 files.
- BASE push run 45716051253: `hosted3.py ... --total 2367 --rules 679 ...` -> `HOSTED c73cda4c...: PASS`; control `--total 2368` -> `FAIL 4` rc 1 (`<d>/logs/hosted-base.out`, `hosted-ctl.out`).
- Lab test counts at BASE (indented patterns over every `.cs` of `tests/Datasec.Suite.Lab.Tests`): Fact 62, Theory 58, InlineData 235, column-1 0, MemberData/ClassData/TheoryData 0 -> DERIVED executable total 297 (the hosted log gives no per-assembly total).
- The five owned files at BASE: sha256 and line counts in the kit table; each printable ASCII, no tab, no CR, final LF (control: planted U+00A0 counted 1).
- New cell prefixes absent at BASE (`U06_`/`U07_`/`U08_` in Oxpd1WriteTests 0, control `U05_` 1; `U09_` in Oxpd1CaStoreTests 0, control `U08_` 1; `S16_` in Oxpd1TestServiceTests 0, control `S15_` 1). The three classes are not partial (`grep -c -i partial` 0 each; planted control 1).
- Every BASE pointer in the kit printed by `grep -n`/`awk NR==` over `<d>/src_c73c` (one corrected during drafting: the CaStore `LabFiles()` helper is `:26` to `:43`).
- Prior work by GET of `LabFiles.cs` at each merge and its parent: RealPath from PR 48 (`f5882ed7`), CaCertificateFile from 52 (`1ccf6d0c`), Family from 53 (`8757daa6`), the undo folder loop already at `e2a20aef^`.
- Live `BACKLOG.md` after R330 (12:25:07): sha256 `5a206f90...`, 1131 lines; in-process `startswith` counts: `150. - [ ] Lab tool oxpd1 (after pull request 54): two sentences of the Lab README` 1; `93/94/126/133/134/143/146. - [x] ` 1 each; `108/111/127/142/145. - [ ] ` 1 each; control `93. - [ ] ` 0. Item 150's first lines equal BL-150 of B2115.
- Seat id X78 free: word-boundary scan of every file in `tuesday/briefs/` -> only this commission names `X78` (control `X77` 14 files); no pane `Datasec/OXPd2-X78`.
- Machine (12:17:06): load `2.97 2.73 2.69`; 872 GiB free; wave lock absent; `<project>/.tools/b2122` absent; dotnet `10.0.404`, gitleaks `8.30.1` by path; `<repo>` local `core.sshCommand` set, deploy key present.
- Tools: `checks_b1.py` on BASE `CHECKS: 1 of 8 PASS` (controls fire in each line); on a simulated staged edit (no compile) `CHECKS: 8 of 8 PASS`; `mutants_b1.py --list` good rc 0 (`LIST: 1 mutants, 2 new cells`), bad (adapter path) `LIST REFUSED: rows mBad` rc 1; `apply`/`undo` on a scratch `LabFiles.cs` restored sha256 `049f05f4...`, second apply refused; the red-label regex maps three synthetic Lab `[FAIL]` lines to `Oxpd1CaStoreTests.U09`, `Oxpd1TestServiceTests.S16`, `Oxpd1WriteTests.U06`; `words.py --control` 13 of 13; `words.py` over the commit message `WORDS: clean (1 files)`; B2xxx count in the message 0.

## Chain inputs (every step's input exists at BASE or comes from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp slots (S4 Q1/Q2 answers, S8 runner sha) | Tuesday's stamp |
| 1 | `<src>` 8 files; `<repo>` local values; origin BASE; BASE push run; R330 STATUS + live BACKLOG | my scratch (exists); `<repo>`; GitHub; R330 (READY now) |
| 2 | files at BASE | the clone from Step 1 |
| 3 | THE NEW CELLS; restored, built clone | kit; Step 1 |
| 4 | red tree; C1 to C5; `mutants_b1.py`; `mutants.json` written after green | Step 3; kit; Step 1; Step 4 |
| 5 | green tree, mutants undone and rebuilt | Step 4 |
| 6 | staged tree; `checks_b1.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

## D-decisions (each Tuesday's default as coordinator; each a Question)
D1 kit 1 of 2; D2 the seat writes the code; D3 108 at the reviewer's proposal only (listing failure; session listing caught; `none` narrowed so `no undo list was read` never prints beside an unreadable folder); D4 142 by a stream bounded at 64 KiB + 1, links followed, refusal text unchanged; D5 127 part by part by `LinkTarget` text, no `ResolveLinkTarget`, no `GetFullPath` of a joined link text; D6 150 takes both sentences and the whole bullet, the write section's `IsServiceEnabled` sentence (README :103-:107) left alone; D7 145 throws `ArgumentOutOfRangeException`; D8 111 pins BASE behaviour with a safe-side re-pin rule; D9 permission and link rows return early on Windows (precedent Y05 and S14).

## Questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS, S4 in words): one kit or two.** Default a: kit 1 of 2 as above; kit 2 (110, 109, 107, 106 in `Oxpd1Command.cs`; 135, 136 in `Oxpd1EchoVerb.cs`) after this lands. Alt b: everything in one kit.
- **Q2 (STOP-CLASS, S4 in words): who writes the code.** Default a: the seat, to the kit's spec, with predicted reds and mutants. Alt b: a re-draft by a drafter allowed the wave lock, freezing diffs.
- Q3 (108 scope). Default: the reviewer's proposal only. Alt: also unreadable when the listing holds `undo-list.tsv` that is not a readable file (flips U07 rows 1 and 6, closes H9).
- Q4 (142). Default: bounded stream, links followed. Alt: refuse any non-regular path (U09 row 4 flips).
- Q5 (127). Default: part-by-part walk by each link's own text. Alt: realpath via P/Invoke, or a Limits line only.
- Q6 (145). Default: `ArgumentOutOfRangeException`. Alt: `UnreachableException`.
- Q7 (111). Default: safe-side re-pin rule (re-pin a U07 row to BASE's words when BASE still ends 11 and never says `nothing is owed`; STOP otherwise). Alt: any U07 difference is a STOP.
- Q8 (150 scope). Default: the callback sentence and the whole bullet; README :103-:107 unchanged. Alt: widen that sentence too.
- Q9 (Windows). Default: early returns in the permission and link rows (Y05/S14 precedent).
- Q10 (gate, level, timing, pane). Default: G1 (`model-routing.md:108`), no local CodeQL, Opus (`<project>/CLAUDE.md:7`, `BRIEF_SEAT_LEVEL=opus`), READY at Step 0 + 180, push by Step 0 + 150, pane `Datasec/OXPd2-X78`, launched only after R330's READY with its pane gone (true now), gate round 1 of 2 of lane OX-B kit 1.

## UNMEASURED / PREDICTED (the riskiest predictions, for the stamp)
- Every dotnet number: red 6 of 314, green 314 / 2384, all six mutants MATCH. None run.
- .NET file-system behaviour the cells rest on, DERIVED from source and docs, not run here: `File.Exists` false inside a mode-000 folder; `Directory.Exists` true for a mode-000 folder whose parent is readable; `Directory.GetDirectories` throwing `UnauthorizedAccessException` on a mode-000 session (RELAYED from owed 108's probe); `GetDirectories` listing a link to a folder (U07 row 4); `File.ReadAllLines` dropping a UTF-8 BOM (U07 row 2); `Directory.CreateSymbolicLink` storing a relative text as given (S16); `FileInfo.Length` of a link being the link's own size (RELAYED from owed 142's probe). U07 rows have the D8 safety valve; the others stop the seat.
- That the hosted linux runner is not root: DERIVED from the landed Y05 "no read permission" row being green on linux.
- A named pipe as the certificate file: no cell (no .NET call makes a pipe and a cell starts no program); README Limits clause only.

## Outside-the-fences disclosure
- No write to the OXPd project, Jira, GitHub or the card store; no `cd`; nothing deleted (two superseded scratch folders and the first sidecar moved into `<d>/_quarantine/`); no recursive read over the project folder (files read by path only: `CLAUDE.md`, `BACKLOG.md`, the B2109 and B2115 STATUS files' tails or sections, `.tools/` listed at depth 1 only, `.tools/b2109` listed at depth 1; `.tools/b2115` not opened); `Source_Documents/` not touched. `gh` only as `gh api -X GET` under the project `GH_CONFIG_DIR`. No Jira call. Nothing to any person, HP or device.
- Git write verbs ran ONLY in my own scratch repo `<d>/selftest/clone` (a copy of BASE's tarball, no remote): `init`, `add`, one `commit` with `-c user.name/user.email` set to a placeholder (scratch only, never a project repo), `add` of the simulated edit, and one `git stash` to clear that simulated edit before the BASE-side check rerun. Plus a bare scratch `GIT_DIR` (`<d>/treegit`) for the tree hash. None of this touches the project.
- The kit carries the GitHub login name `kamilDatasec` in FACTS 1 (as kit B2109 did); it is not text the seat copies into a commit.
- Card ids: none read, none cited.
