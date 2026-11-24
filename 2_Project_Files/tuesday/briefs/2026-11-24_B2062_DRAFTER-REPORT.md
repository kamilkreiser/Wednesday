STARTABLE: YES

# B2062 DRAFTER REPORT: OXPd 2 lane L3, round 2 of 2 (fix round after gate B2061 NO GO), build kit for seat X69

Drafted 2026-11-24 21:41:11 to 22:01 AEDT (first and last `date`) by a read-only Opus drafter for Tuesday s324. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2062_SEAT-X69_oxpd2-l3-round2.md` (77 KB, ASCII only, 8 stamp slots, last line `READ-WHOLE-BY-TUESDAY: ____`); sidecar `...l3-round2.md.measured` (`stamp_check.py` rc 0: 165 claims, 165 measured). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s324/d2062/` (below `<d>`). Seat tools: `<d>/seat-tools/` (11 files).

## BLUF
- **One fast-forward commit on HEAD1 `4b9814f1` (branch `b2056/l3-onedrive-browse`), three `M` paths, no add/delete/rename:** `BrowseTests.cs` (O02 row `D4648F06C91D9D3D!54927` replaced by `SYNTHETIC0002!12345`; new `[Fact]` O12 inserted above O10), `MyDriveBrowser.cs` (`Followable`'s last line becomes `string target = next.GetLeftPart(UriPartial.Query);` plus the compare/return on `target`; doc comment updated), module `README.md` (the false "never opens another user's drive" half-sentence replaced by a remote-item line, a `drives/{id}` Limits line and a fragment line).
- **Red first on HEAD1 by assertion (MEASURED, frozen patches in `<d>/clone2`):** OneDrive executable `Total: 50, Errors: 0, Failed: 1`, the one red O12: `Assert.Equal() Failure`, Expected `(PagingLoop, 1)`, Actual `(TooManyPages, 100)`. That is the gate's probe P2 shape exactly. The new O02 row is green on HEAD1, as it should be: it is test data, not a new behaviour. It is red under `mFolderSelectDropped` (MEASURED: that mutant's log names the new row `[FAIL]` once).
- **Green:** `Total: 50, Errors: 0, Failed: 0`; whole solution `total: 2203`, `failed: 0`, `succeeded: 2199`, `skipped: 4`. **Mutants:** `MUTANTS: 16 of 16 MATCH, 16 of 16 undone equal`. These are round 1's 15 rows, with `mLoopUnchecked` re-anchored (now red on O09 and O12), plus a new `mFragmentKept` (red on O12 only).
- **Chain:** `locks equal 36 of 36`, guard `14` and `15` files clean, `Ran 111 tests`, `RULES: clean (671 files)`. Checks: `CHECKS-R2: 10 of 10 PASS` against HEAD1 and round 1's `CHECKS: 10 of 10 PASS` against BASE. Words, gitleaks and the B-number count are all clean, each with its control fired.
- **FLOOR does not move.** The hosted push run builds the branch tree, whose workflow still reads `FLOOR=111`, so the kit predicts `--total 2203 --rules 671 --unit 111 --floor 111` (see Q5: this is my reading of the commission's unit/floor line).

## FACTS RE-MEASURED (instrument, control)
| # | Fact | Instrument | Control |
|---|---|---|---|
| 1 | origin `main` = `f5882ed74275200ffd37ac998ee650ada0820241`; `b2056/l3-onedrive-browse` = `4b9814f1b18fb269ac88862e99355e267a57eba2`, its parent `89a10a1b`; `heads/b2062` 0 rows; PRs 48..43 closed, 0 open; private/push true | `gh api -X GET` (21:41:22, re-read 21:58:45 into `<d>/evidence/origin.txt`); `git log --format='%H %P'` | `heads/b20` listing 11 rows (others present) |
| 2 | **Lane L4 moved during drafting:** `b2057/l4-release-guard-cert-forms` went from `c16306ca` (21:41) to `0ca131eb477f2fff5e6f9b3f79e3ef32846bb296` (21:58:45). X68 pushed its round 2, and its pane was gone at 21:58. `main` was unchanged. | same | — |
| 3 | HEAD1's three files equal round 1's "After both" sha256 (`83e5bf19…`, `e6bb9f73…`, `59c532a5…`) | `shasum` in `frozen.py` (`<d>/logs/frozen-red.out`) | the round-1 kit's THE CODE table |
| 4 | HEAD1 hosted push run `HOSTED 4b9814f1…: PASS` at `--total 2202 --rules 671 --unit 111 --floor 111 …` | `hosted3.py` (`<d>/logs/hosted-head1.out`) | its own `NOT-A-LINE-OF-ANY-LOG count 0` control |
| 5 | Red/green/mutants/chain as in BLUF | `heavy.py` (lock waits 0 on every job; load1 2.0–6.8), logs in `<d>/logs/` | `Total:` lines; per-mutant undo equal True |
| 6 | lane literal census at HEAD1 (12 files): hex16 1, consumer-shape 1 (both the O02 row), GUID 0, URLs 6 (all `example.test`), `!`-tokens 4 (O02 row, `b!synthetic-drive_0001`, the regex class twice) | `<d>/scratch/idscan.py` → `<d>/logs/idscan-head1.out` | it found the O02 row (the class fires); at the fixed tree `checks_l3r2.py` check 4 reads `hits none` with control hex16 1 / consumer 1 at HEAD1 |
| 7 | Microsoft `driveitem-search.md` holds `"id": "0123456789abc!123"` at lines 115 and 190; `driveitem-list-children.md` `deprecat` 0 lines, `children` 41; neither holds `SYNTHETIC` | plain unauthenticated HTTPS GET of `raw.githubusercontent.com/microsoftgraph/microsoft-graph-docs-contrib/main/api-reference/v1.0/api/{driveitem-search,driveitem-list-children}.md` (HTTP 200, 8735 and 7596 bytes) into `<d>/evidence/ms/` | `children` 41 |
| 8 | Round 1's `mutants_l3.py` can't run on round-2 code: `MUTANT mLoopUnchecked refused: OLD text occurs 0 times`, rc 1, nothing written | `<d>/evidence/priorwork.txt` | `git status --porcelain` unchanged |
| 9 | `main` f5882ed7 changed 9 paths since BASE, none in the lane; `main`'s `FLOOR=111` | `git diff --name-only 89a10a1b f5882ed7`; `git show f5882ed7:.github/workflows/ci.yml` | — |
| 10 | seat id X69 free: 0 brief file names, and only this commission among briefs of 11-23/24; `.tools/b2062` absent | `ls | grep -c -E` word scan; `grep -l` | X68: 3 file names; `^b2060$` 1 |
| 11 | model `claude-opus-5-5` (`models_latest.json:17`); OXPd `CLAUDE.md:7` newest Opus; `brief_seat.sh:31` `${BRIEF_SEAT_LEVEL:-opus}` | `awk NR==n` | — |

## D-DECISIONS (mine as drafter; each is a Question to Tuesday in the kit)
- **D1:** FOUND 1 fixed with the gate's own example literal `SYNTHETIC0002!12345` (it keeps the `!` row).
- **D2:** FOUND 2 handled as README wording only.
- **D3:** FOUND 3 fixed in code with `GetLeftPart(UriPartial.Query)`, used for both the compare and the address sent.
- **D4:** the new cell is its own `[Fact]` O12, not a row added to O09.
- **D5:** one fast-forward commit, no rebase, and round 1's whole chain (the diff holds a `.cs` file).
- **Left alone on purpose:** `OneDriveBrowseException.cs:17` (true after the fix) and the Graph layer's identical `FollowableLink` compare (not this lane's; it goes in FOR RECORDS).

## QUESTIONS FOR TUESDAY (each with its default; Q1–Q3 STOP-CLASS, S4 in words)
1. **Q1, the O02 literal.** Default a: `SYNTHETIC0002!12345`. Alternative: Microsoft's example `0123456789abc!123` (a re-export of about 10 minutes).
2. **Q2, FOUND 2.** Default a: a README Limits line, no binding. Alternative: bind the `drives/{id}` forms to a drive id. **This is costlier than the gate implied.** The listing sees no drive id today because the Select has no `parentReference` (0 lines, measured). Binding therefore means changing the Select, which moves the G1/G2 query and four cells' assertions (a re-draft). The other way, binding to the first `drives/{id}` link seen, does not stop that first link naming another drive.
3. **Q3, FOUND 3.** Default a: compare and send without the fragment (O12 plus `mFragmentKept`). Alternatives: a README limit only, or refuse any link that has a fragment.
4. **Q4.** O12 as its own Fact (default), or as a second row of O09 (rewrites a round-1 cell).
5. **Q5, hosted unit numbers.** Default: `--unit 111 --floor 111` on the push run in both cases. The push run builds the branch tree, which has `FLOOR=111`. I read the commission's line ("are the new main's own values") as applying to the pull request's merge-ref, which is Tuesday's to prove. Taking it literally would make `hosted3.py` FAIL a green run if L4 lands first. **This now matters: L4's round 2 was pushed during drafting.**
6. **Q6, commit subject.** Default: the kit's (271 characters, words-clean, no "round"/"gate").
7. **Q7, local CodeQL.** Not run.
8. **Q8, chain.** Default: round 1's whole chain. Alternative: B2060's short chain.
9. **Q9, seat settings.** Opus, READY at Step 0 + 90, push by Step 0 + 70, pane `Datasec/OXPd2-X69`, G1 round 2 of 2; landing order free against L4.
10. **Q10.** Leave `OneDriveBrowseException.cs` untouched (default), or add a fourth owned path.

## CHAIN INPUTS (each step's inputs exist at HEAD1 or come from an earlier step)
| Step | Inputs | Produced by / present at |
|---|---|---|
| 0 | kit, stamp slots | Tuesday's stamp |
| 1 | `<src>` 11 files; `<repo>` local values; origin HEAD1/BASE; HEAD1 push run | `<d>/seat-tools` (exists); `<repo>`; GitHub (MEASURED) |
| 2 | files at HEAD1 | Step 1 clone |
| 3 | `1-red-r2.diff`; clone at HEAD1; package cache | Step 1; Step 1; `<project>/.tools/nuget-packages` |
| 4 | `2-fix-r2.diff`, `mutants_l3r2.py`; red tree built | Step 1; Step 3 |
| 5 | green tree, mutants undone and rebuilt; `heavy.py` | Step 4; Step 1 |
| 6 | staged tree; `checks_l3r2.py`, `checks_l3.py`, `words.py`, message | Step 5; Step 1 |
| 7 | commit; origin branch and `main`; `run_step.py`, `hosted3.py` | Step 7a; 7b fetch; Step 1 |

## STOP-severity checks run once on my own output (PASS, control fired)
- Tool sha256.
- PRIOR-WORK greps: rc 1 ×3, control found.
- Red by assertion: 1 of 1.
- 16 mutants MATCH.
- `checks_l3r2` 10/10 and `checks_l3` 10/10.
- Locked restore `--force`: 36/36 lock files equal.
- `RULES: clean (671 files)`.
- gitleaks: control rc 1, then rc 0 over the clone and the 8 neutral files.
- `WORDS: clean (2 files)`: control fired 13 of 13; B-number count 0, control 5.
- HEAD1 hosted PASS.

**Never run:** `clone.py seat`, the commit and identity read, `run_step.py` neutral scan, the push and read-back, `hosted3.py` on a round-2 head, the hosted legs, CodeQL. Each is marked NEVER RUN in the kit.

**Disclosure on check 7:** my first `checks_l3r2.py` run printed `FAIL 7`. The check had compared `-U0` lines in order, but git aligns the inserted block one line higher. I rewrote it to compare the lines as a set plus the exact whole file, then re-ran: PASS. The kit's sha256 is the rewritten file's.

## UNMEASURED
- How Graph really answers: next-link form, whether it ever sends a fragment, behaviour on a `drives/{id}` the user cannot open.
- The wire (no socket was opened).
- Linux and Windows behaviour of the new cell (PREDICTED green).
- The merge build with `f5882ed7`: total 2221 is DERIVED (2220 + 1), not built.
- `GetLeftPart(UriPartial.Query)` equality with the first address is shown only through O04/O09/O11/O12 staying green, not by a separate probe.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Heavy jobs** (restore, build, test, publish, test executable) ran through the project's `heavy.py` and its wave lock, as the commission allows. The lock was absent at every take: 0 waits, so X68's lock was never touched. They ran only in my scratch clones `<d>/clone` and `<d>/clone2`. In those clones I used git write verbs (switch, apply, add) because they are my own scratch. In the project repo I used none.
- **Microsoft:** two plain unauthenticated GETs of raw.githubusercontent.com, named in FACTS 7. Nothing else outside GitHub's `gh api -X GET`.
- **Files I wrote:** only the kit, its sidecar and this report under `tuesday/briefs/`, plus files under `<d>`. I moved the `--init` TODO sidecar and a temporary `.measured.new` into `<d>/_quarantine/`; nothing was deleted.
- **Project files read (read-only):** `B2056_STATUS.md`, `CLAUDE.md`.
- **Hooks:** two commands were refused by hooks (a `====` separator; a `git -C $C` write verb the hook could not resolve). Both were re-run with the corrected form; nothing ran outside the fences.
- **Nothing sent:** no mail, Jira, card store, push, PR or project write; no message to any human; nothing of another client.
