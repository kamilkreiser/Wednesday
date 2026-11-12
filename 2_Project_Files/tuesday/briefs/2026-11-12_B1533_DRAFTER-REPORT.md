STARTABLE: YES (after the stamp; both heavy slots were held at 10:5x, so expect a wait; launch window is Tuesday's)

# B1533 DRAFTER REPORT (read-only drafter, 2026-11-12 10:51-10:5x AEDT; `date` printed 10:51:09, 10:53:16, 10:55:47)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1533_SEAT-M129_mps-392-393-words-and-tiles.md` (95 lines by `wc -l`; 12 slot lines of four underscores by `grep -c`, control: the unstamped B1530 pre-stamp copy prints 12 too; 0 non-ASCII lines; 0 hits for the owner's or coordinators' names). Seat `Datasec/MPS-M129`, branch `b1533/mps-392-393-words-and-tiles`, two commits, plain push, no PR, not deployed, Sonnet (C2, `model-routing.md:92`, `models_latest.json:23`, G2 at `:109`; all three re-printed), `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, ports 9890-9899.

## BLUF
- The approved strings are in the kit as FACT 2 and are byte-identical to the document: W1, W2, W3 each occur once in the kit and once in the document (python `count`, control: W1 with one character changed counts 0).
- Main is `793d0a9c` (the #185 squash), not the document's `baf0aabe`. Every file:line of the document's builder section still holds at the new base (re-printed with `grep -n`/`awk NR`); the kit prints them again in FACT 3.
- **The document's "the script's test / a test" understates the test footprint.** Item 1's rows are in `scripts/tests/test_scripts.py` (not `test_deploy_pre1.py`), item 2's in `test_deploy_pre1.py`, and the item-3 dry-run last line is asserted by `assertEqual` in THREE seed test files (four sites). All five files go in the partition (D-5, Q-1).
- Item 6 is built as find-then-fix with a reproduce-or-not branch; item 5 as measure-then-set; item 4 as the document's selector with a tile-fit check.

## Facts re-measured (instrument; control)
- main sha: `gh api -X GET .../git/ref/heads/main` = 793d0a9c52c961852b4a1f04bb826ffff752ce74; open PRs 0 at 10:51, later #186 (b1528) open; `^b15` branches 10; b1527/b1530/b1531/b1532/b1533 0 rows (control: b1528 1 row).
- Lanes: `compare main...<branch>` for all 10 `^b15` branches; only b1512 (#181) and b1514 (#182) name my files, both merged (control: those lists printed my files). B1530's kit (M128, live) and B1527 (M126, live) grant none of my nine paths.
- Jira: own GET-only reader at `fleet/state/s271/d1533/jira_get.py` (not copied from any `.tools`), MPSCALC-392 and -393 Backlog, 0 comments, updated 11-11 22:26; control MPSCALC-361 Done.
- Ports: lsof 9890-9899 = 0 (control: unfiltered 12); digit-bounded scan of 47 non-`.pre-` SEAT kits for `989x` = 0 files (control: `985x` = 1 file, the B1530 kit). The B1533 kit itself did not exist at scan time.
- Test footprint: whole-tarball grep of main with positive controls (see FACT 4). "did not pass" occurs only at `deploy-from-ci.sh:175-176`. "everything a real run checks" occurs only in `seed.py`. No hidden-character test exists in this repo's `infra/tests` (listing: `test_infra.py`, `test_validate_script.py`; `grep -c hidden` over the tree list = 0).
- Tools: no `codeql`, no `shellcheck`; gitleaks, Chrome, python 3.9.6 present. Heavy locks both held at 10:5x (M126, M128).

## D-decisions
- D-1/D-2: W1 goes in a block at `:260` only; the other three exit-3 paths already end on their own NOT PROVEN line (`:241`, `:249`, `:254`) and are not touched. Rows (a)-(e) include controls that W1 does NOT appear on a proven start, a probe, a failed byte check or missing HSTS.
- D-3: `:684-685` (client-credentials dry run) not given a folder sentence (the words cover the dry run's last line only).
- D-4: `:176` only (the proposal, not the alternative). Rows pin the last stderr line and that `:175`'s text is unchanged.
- D-5: test partition widened to the five files that carry the old sentences.
- D-6/D-7/D-8: item 4 selector from the document; STOP (not a fix) if tile content overflows at 601 or the rule scrolls the page; item 5 forces a classic scrollbar by an injected style in the spec only, proves it by `innerWidth - clientWidth`, STOPs if it reads 0 (config is B1530's); existing overlay-edge rows and constants keep their values, classic edges are new constants; a 1 px sweep 500-1500 per role and kind in one page per pair; new item-4 widths go in a separate list because `MID_WIDTHS` expects `[3,3]` for six tiles.
- D-9: item 6 gets (a) a reproduce-on-Home measurement with a planted control, (b) element location with a hide-and-watch confirmation, (c) a bounded route census if Home does not reproduce, (d) a fix only inside the home-tile rules, never `overflow-x: hidden` on html/body/.main, (e) rows that are red-before if reproduced and guard rows if not.
- D-11: if item 6 lands outside the partition the branch is still pushed with items 1-5 and the last line is the STOP.

## Q-questions for Tuesday (defaults are in Stamp S4)
- Q-1: The five test files (two in `scripts/tests/`, three in `tools/demo/test/`) are in the partition. Default yes.
- Q-2: Give the `--client-credentials` dry-run line (`seed.py:684-685`) a folder sentence? The approved words do not cover it; that path makes no request. Default NO (left as is).
- Q-3: If item 6's cause sits outside the partition, push items 1-5 and end with the STOP. Default yes.
- Q-4: If item 6 does not reproduce on any reachable screen, ship guard rows and a READY with `ITEM 6 NOT REPRODUCED`. Default yes.
- Q-5: Sweep rows live in `home-tiles-fill.spec.ts` (partition names it) rather than a sibling spec. Default yes.
- Q-6: READY at Step 0 + 180 minutes (not 150: two commits, six sweeps, heavy-slot waits). Default 180; Tuesday writes S9.

## Observations for Tuesday (not for the seat to fix)
- W2 says "the kept copy named above" and "the line above says why"; on `reread_overlay`'s early returns at `deploy-from-ci.sh:159-160` no copy may exist (host lookup failing, or the copy not creatable). The words are frozen; the kit asks the seat to read those paths and report whether W2 still reads true.
- The ticket's "574 against 575" is `scrollWidth` below `clientWidth`, which is no overflow; item 6 may not reproduce on Home at all.
- Two B1530 and B1533 paths do not overlap; B1530 deletes a `LEFT_OUT` entry in `web/playwright.config.ts`, which this kit forbids editing.

## UNMEASURED
Tile fit at 177 px tracks, whether Chrome here can force a 17 px classic scrollbar, the classic edges, item 6's cause and persona set beyond `ROLES`, Linux/CI behaviour of the sweep timings, whether `bash`'s `stop` is reached through `scm_host` failing with a message.

## Outside-the-fences disclosure
Reads only: Jira GET (own helper, token never printed), `gh api -X GET` (contents, tree, compare, matching-refs, pulls, commits, one tarball of main saved and extracted into the scratch folder), `lsof`, `tmux list-panes`, `uptime`, `df`, `which`. Writes: this kit, this report, and files under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1533/` (raw file copies, a tarball and its extraction, `jira_get.py`, `jira_392_393.txt`, `tree.txt`). No ref write, no `cd`, no HTTP to any hosted site. One shell call was refused by a hook (an unquoted line of equals signs) and re-run quoted.
