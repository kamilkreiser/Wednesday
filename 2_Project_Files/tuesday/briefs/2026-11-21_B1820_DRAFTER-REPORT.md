STARTABLE: YES - once stamped. The kit is whole (165 lines, 48000 bytes before the stamp, 0 non-ASCII lines, 8 slot lines), `stamp_check.py` exits 0 (117 claims, 117 sidecar lines), and the commit it orders was made twice by the drafter in scratch clones, the second time with the block cut from the kit file itself: tree `6fc18eaa1e7356cf394c3fe2c47bfa1003fafb9c`, `PROOFS: PASS (9 of 9, controls fired 9 of 9)`. NOT run by anyone on a commit: the dotnet build and the 476 tests (RELAYED from the second review's uncommitted scratch merge), the push, the hosted run of the new head.

# B1820 DRAFTER REPORT (OXPd 2, WP4.2 part, the resolution commit; seat X13; delta review B1821)

Written 2026-11-21 by the in-session drafter (Opus, read-only). Work from 08:47 to 09:05 AEDT (clocks by `date`: 08:48:11, 08:49:18, 08:53:02, 08:53:48, 08:56:10, 09:00:28, 09:03:50, 09:04:11).

## BLUF
- **The kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1820_SEAT-X13_oxpd2-wp42-resolve-solution-file.md` (165 lines, 48000 bytes) with sidecar `.measured` (118 lines: a header and 117 claims; 31 of them instructions).
- **The delta review:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1821_GATE_COMMISSION.md` (28 lines, 14554 bytes). It is a DRAFT: it holds the word `HEAD40` 27 times (`grep -o | wc -l`) where the seat's sha40 goes, and one paragraph `MEASURED BY TUESDAY ... TO FILL` for your own reads. Fill both by program before the Agent call.
- **The conflict is exactly the one the review measured.** In my scratch clone, `git merge-tree --write-tree --name-only ec75619e c56f3f3b` exits 1 with ONE conflict, `CONFLICT (content): Merge conflict in Datasec.Suite.slnx`, tree `637918b85232a72ce2ce08ef385c33465688cc74`; control: main merged into itself exits 0. The branch changed 31 paths since the merge base `7bf37526`, main 22; they share ONE path, the solution file.
- **The block** cut by program from `landing.txt` lines 43 to 55 (three leading spaces removed) is 13 lines, 699 bytes, sha256 `df48c25f0a60cfd6fca65912d866b15b70ca0efdb701b00d23cba3fcc841179d`, blob `b659bf846a81faaf2838a5b72f8d744ea3f1cbc2`: the review's figures. It is frozen in the kit at column 1 (kit lines 24 to 36); the seat's program `resolve.py` cuts it from the seat's Step-0 copy and refuses on any other sha256. The seat retypes nothing.
- **The commit is pinned by its tree, not its id:** parents ec75619e then c56f3f3b; tree `6fc18eaa...`; message file sha256 `c29fbb82...` (subject 98 bytes + the one attribution line; `WORDS: clean (1 files)`). The commit id differs per identity and clock (mine: `897083f9` and `b4dd630`, scratch identity, never pushed).
- **Commission wording corrected (Q1):** "main with the branch's 11 paths laid over" cannot be the tree: the 11 are the fix round's commit; the branch has 31 paths since the merge base (the round-1 commit's 20 others hold the library itself). The kit's property lays over all 31 and proves the 11 blob-equal separately (P6).

## What I measured, and how (scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s303/d1820/`)
1. Origin by `gh api -X GET` under the project `GH_CONFIG_DIR` (08:48:11 and 09:00:28): main `c56f3f3b`, `b1788/wp42-ipp-encoder` `ec75619e`; `b1786` has moved to `9fe53569` since the B1813 stamp (another lane; not this kit's); pull requests 2, both closed and merged, neither on this branch; `rules/branches/b1788/wp42-ipp-encoder` lists 0 rules (control: main lists 4), so a merge commit on the branch is accepted; squash merge allowed.
2. Two scratch clones by `clone.py` mode draft (push URL `invalid://no-push`): `clone` and `clone2`. In each: `git merge --no-ff --no-commit c56f3f3b` printed the three lines (rc 1); porcelain 22 lines (20 `A`, 1 `M`, 1 `UU Datasec.Suite.slnx`); `resolve.py`; `git add`; `git commit -F merge-message.txt`; `proofs.py` PASS 9 of 9 with 9 controls fired. `clone2` cut the block from THE KIT FILE (`<Solution>` at kit line 24, `</Solution>` at 36). `git merge --abort` measured on a separate local branch: porcelain 22 lines before, 0 after, HEAD the reviewed head. **The merge needs an identity even with `--no-commit`** (git refused with `Committer identity unknown`, rc 128, before I set a scratch identity): the seat-mode clone carries the checkout's.
3. `resolve.py` controls: a block with one changed byte REFUSED on the sha256; `landing.txt` itself (indented block) REFUSED as holding no block.
4. Light jobs of the workflow on the merged tree: `Ran 53 tests` `OK`; `RULES: clean (76 files)` (hash half NOT RUN, as it prints); `gitleaks git` rc 0; the workflow step `scan every stored object under a neutral name` via `run_step.py`: rc 0, `25 of 25`, `NEUTRAL-SCAN: stored objects 288 (195 blob, 15 commit, 78 tree), copies written 576, objects of this commit not among them 0`. So the neutral scan handles a two-parent commit.
5. `hosted.py` (kit B1813's reader plus `--rules N`, needed because the rules line reads 76 files on the merged tree): on ec75619e `--total 285 --rules 56` PASS; control `--total 476 --rules 76` FAIL 5; on main `--total 192 --rules 46` every count OK and FAIL 2 only for the code-scanning rows main carries (a branch push carries only the four jobs: ec75619e shows 0 beside them). Both parents show `GUARD: clean (10 files)` and `(11 files)`; the merged prediction keeps them (the server references Core only, measured).
6. `history_entry.py` on a byte copy of the history file: the three True lines; a second run refused.
7. CI predicate read at source: `ci.yml` test step greps `total: +[1-9]` (lines 46 and 76) and the reader counts `total: 476` on 2 lines per leg; the push trigger `b[0-9]*/**` (line 7) covers the branch.

## D-decisions (mine, inside the commission)
- D1 a program, not a hand, writes the file: `resolve.py` refuses unless HEAD, MERGE_HEAD, the unmerged set (exactly the solution file, stages 1 2 3) and the block sha256 all hold; it stages and commits nothing.
- D2 the property is checked entry by entry from `ls-tree` of the two parents (P3), independent of git's merge, AND as `diff <trial tree> HEAD` = the solution file (P4): the commission's two forms.
- D3 the trial command is fixed with full shas in the order head, main: the conflict markers carry the names, so the trial tree id depends on that order.
- D4 no local dotnet job by the drafter (see fences): the build and 476 are the seat's Step 5, under the lock exactly as B1813 words it.
- D5 the hosted reader requires `--rules 76`, both GUARD lines and no check run beside the four.

## Questions for Tuesday (each with its default; the kit assumes every default)
- Q1 tree property over 31 paths, not 11 (default: 31, with P6 proving the 11; cost of the alternative: an unbuildable tree, no alternative offered).
- Q2 no local baseline build of the parents (default: none, hosted runs of both parents read by GET; cost: a red on the merged tree cannot be split into before/after without more runs).
- Q3 one history entry (default yes; note `words.py` counts 2 B-number hits in the template, both the STATUS path, as B1813's template had; history.md is a records file outside the repository).
- Q4 the commit message file (default as frozen).
- Q5 no local code scan (default none; RELAYED: C# cannot be extracted here for this lane).
- Q6 a red hosted job: STOP, no second commit.
- Q7 windows 60/45, pane `Datasec/OXPd2-X13`.
- Q8 (B1821) a NO GO on the resolution commit: the commission names no route. Default in the draft: it says what failed in one plain line and stops; whether it goes to the product owner on a card (the lane is past round 2 of 2) or back to Tuesday for a new resolution kit is Tuesday's to write in before the Agent call. Cost of leaving it: the reviewer picks a route itself.

## Chain inputs (rule 4: each input made by an earlier step or present at BASE)
| Step | Inputs | Made by |
|---|---|---|
| 0 | the stamped kit | Tuesday's stamp |
| 1 | origin by GET; `gate/` (d1820); the checkout's local config; the deploy key | BASE |
| 2 | `<clone>` | Step 1(c) |
| 3 | `<clone>` on the branch; `<lane>/gate/merge-message.txt`; the Step-0 kit copy | Steps 1(b), 1(c), 0 |
| 4 | the commit; the message file | Step 3 |
| 5 | the committed tree; `<lane>/{logs,dotnet-home,_quarantine/locks}`; the project's SDK and package cache | Steps 1(b), 3; BASE |
| 6 | the commit; origin by GET | Steps 3 to 5 |
| 7 | the pushed sha40; the template | Step 6; Step 1(b) |

## UNMEASURED / NEVER RUN on a real output (marked so in the kit)
The REFUSE checks; `clone.py` mode seat and P8 against a seat identity; restore/build/test of the merged commit (476 RELAYED); `status --porcelain` after a build; the push and its read-back counts by GET (`ahead_by` 2 and 3, files 22 and 31: measured locally only); `hosted.py --wait` and its verdict on the new head; the history program on the live file; the hosted code scan of the later pull request.

## What I did NOT read
The second verdict's items 1 and 2 (lines 22 to 150) and `FOR-RECORDS.md`; `pr-body.md` and `squash-body.txt` beyond their numbered lines (the delta review re-reads them all); the builders' STATUS files of this lane; kit B1802; the round-1 verdict; the decision store (the product owner's Opus words are RELAYED from the commission).

## Outside the fences (disclosure)
- Network: two `git clone` of the origin over ssh with the project's deploy key, set in the `clone.py` process only (the B1813 drafter's method); GETs only by `gh api -X GET` under the project `GH_CONFIG_DIR`.
- Git writes only in my two scratch clones under d1820 (switch, merge, merge-tree, add, commit, abort, a clone-local scratch identity `drafter scratch`); nothing pushed (push URL invalid).
- **No write in any project tree:** I did NOT take the wave's lock and ran NO dotnet job (taking the lock is a `mkdir` under `<project>/.tools/`, outside the files the commission lets me write); `dotnet --version` ran with its home in my scratch. The history file was read into my scratch by python (a `cp` was refused by the path guard for parsing the source as the target; nothing was written there).
- No Jira, no message, no Artifact, no `cd`, nothing deleted. Load 1.16 to 2.49 throughout; panes `Datasec/OXPd2-X10` and `-X11` live beside me; the lock folder absent at 08:49 and never touched by me.
