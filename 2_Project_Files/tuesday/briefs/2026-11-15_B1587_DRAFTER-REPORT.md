STARTABLE: YES (a mechanical rebuild in B1579's exact form; Q1 (whether a gate round is owed) needs your eye at the stamp, because the gate's own verdict says one thing and B1579's rule another; the kit holds a default)

# B1587 DRAFTER REPORT (SEAT-N132, NexusAI, rebuild the banner branch's counts after #201 and #202 landed), drafted Sun 15 Nov 2026 (`date` at start 18:01:21 AEDT, last `date` 18:08:56)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1587_SEAT-N132_nexusai-rebuild-b1568-counts.md` (132 lines; 5 lines with the four-underscore pattern: four slots and the last line; 0 non-ASCII lines by `LC_ALL=C grep -c '[^ -~]'`; ban-list name scan TOTAL 0 over the nine names of the gate's list, the `x_by_<name>_y` control firing 1 for each, `kamera kamikaze` 0; the decision-card-id shape scan hit only the path `locks-laptop-1017`, control `nexusai-field-grant-holder-1115` fires). Sidecar `.md.measured`: 107 lines, `stamp_check.py` prints `82 claims, 82 measured, 0 not measured`, rc 0 (run alone, output to a scratch file, not a pipe); it also carries S01 to S25.

## BLUF
- **The job:** on the existing branch `b1568/nexusai-f2-banner-above-overlay` (head `a63389b1`, base `4ba2e03c`, four commits, gate G2 GO WITH FINDINGS), make ONE merge commit M of origin main `6335717d`. The counts file is the only conflict; it is resolved by copying main's blob `0127a623` unchanged. Then `--update-counts` on M's tree, ONE counts commit K3, a plain verify at K3 that must PASS, a by-program PROOF, ONE plain fast-forward push. Sonnet, row **C5** (`model-routing.md:95`), slot 18 (trees `upd23`, `fin6`), port block 9980-9989 (my proposal), no server of its own. PREDICTED lock hold about 60 minutes (B1579 measured 56 for the same two verifies).
- **The conflict is MEASURED, not assumed:** `git merge-file -p` over scratch copies of the three counts blobs exits rc 1 with one hunk and 3 markers (control: theirs = base gives rc 0). The two path sets share exactly one path, the counts file (branch 9 paths, main 9 paths). So the merge brings main's other eight paths in clean.
- **The expected pair 5666 / 353 is DERIVED from two real full runs:** main's tree run (B1579's plain verify at `17b7511d`, 5653/352, whose tree equals `6335717d`'s tree `ded306c3`, measured by the commits API) with the two branch test files (`rd490` 66 to 72, new `rd858` 7) taken from B1568's plain verify at `a63389b1` (5649/350). Derived both ways, the per-file maps are equal. Controls: each run alone reproduces its own pair. A different measured pair is a STOP.
- **The id-superset control (C-57) WILL report one missing id, by design:** the RD-486 (d) title main renamed in #202. The branch predates the rename. My program over the two runs predicts exactly that (missing 1, new 0), and B1579's `pairtable.py` already carries the matching `IDSUPERSET-ONLY-RD590-RENAME` line. The kit tells the seat to expect it and to STOP on any other missing id.
- **No PR exists for this branch yet** (0 open PRs). The seat pushes; Tuesday opens the PR and lands by merge commit pinned to K3, using B1568_verify's three landing files with the sha (and `<N>`) replaced.

## Facts re-measured (instrument; control)
1. Main `6335717d3625760409612ebe757f5589f65dbafb`, tree `ded306c3`, parents `0fdc77f0` and `17b7511d` (`gh api -X GET commits/main`, 18:01). `17b7511d`'s tree is also `ded306c3` (commits API on both). Open PRs 0 [S01, S04].
2. Path sets: main's diff (`4ba2e03c...6335717d`, ahead 8, behind 0) has 9 paths; the branch's (`4ba2e03c...a63389b1`, ahead 4) has 9. Intersection exactly `scripts/verify-expected-counts.json` (python set program; control: branch-only 8, main-only 8) [S04, S06]. The eight non-counts branch paths have the same blob at main as at base (S25 table), so main never touched them.
3. Counts blobs (python sha1 of the raw API bytes equals the contents API `.sha` for each, True five times): base 5636/349 `6c772ba5`; branch head 5649/350 `a962b9b0`; main 5653/352 `0127a623` (also at `17b7511d`) [S07]. Merge-file hunk covers `_updated`, `tests`, `suites`; 3 markers [S08].
4. Verify script at main: `--update-counts` rewrites `tests`, `suites`, `_updated` only, after every other assertion passes (`verify-suite.sh:317-340`, `_updated` at `:333`, UPDATED line `:337`); the plain run fails a grown suite as stale (`:354-360`); PASS line `:366`. Hosted CI runs the plain form (`build.yml:92-93`) on Node 24 (`:29`). Line pointers printed by `grep -n` over the raw file at `6335717d` [S12, S13].
5. Deploy demo runs only on a push to main (`deploy-demo.yml:26-28`; `paths-ignore` `'**.md'`, `'docs/**'`, `'tests/**'`), so the branch push starts nothing. **This branch changes four `static/` paths, which are not path-ignored, so Tuesday's later landing WILL start Deploy demo**; both jobs must read skipped (the gate's finding 4). Neither side touches `.github/` or `package*.json` (0 and 0 by program) [S14].
6. Toolchain by path: NexusAI has no drive-local node (`ls .tools | grep -i -c -E 'node|dotnet'` 0; control `grep -c b1579` 1; `.tools/node24/bin/node` absent). Machine node `/opt/homebrew/bin/node` v26.13.0, npm 11.20.0 at 18:03 [S16].
7. Slots: `upd23` and `fin6` are both 18 (program controls: `upd10` 7, `old52` 4, `old12` 1, `upd21` 9 equal what those seats recorded). Band 31520-32159: 0 listeners (control: 16 machine-wide) [S18-S20].
8. Live: no `Datasec/NexusAI-*` pane (tmux names listed in S17); the jest lock has no owner file and `queue-jest` is empty. Seat id by program: the highest `SEAT-N` in the briefs folder is N131, so this seat is N132.
9. Sources in the pickup and today's note: this lane is named as "NEXT" at pickup lines 77, 99 and 110; no DROPPED or HELD mark names b1568 or this lane (the only DROPPED line is the Composer lane; /usr/bin/grep with the control `DROPPED` count 14 in the pickup).

## Chain step inputs (each produced by an EARLIER step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| Step 1 clone, `npm ci`, local branch | origin main, origin branch `a63389b1` | origin (REFUSE 4/5 check them) |
| THE MERGE (M) | the `wt` worktree on the local branch; `origin/main` | Step 1 |
| chain 1 `u-update` (`upd23`) | M | THE MERGE |
| chain 2 `kstep` (`wt`) | the counts file written in `upd23` | chain 1 |
| chain 3 `p-plain-K` (`fin6`) | K3 | chain 2 |
| THE PROOF | K3, `a63389b1`, `4ba2e03c`, origin main; chain 1's file; chain 3's tree and run | chain 1-3, Step 1 |
| `pairtable.py` inputs | main's run and the branch's run, both `cp`'d into `raw/`; step 3's run | already on disk at BASE (`.tools/b1579/raw/jest-p-plain-K.json`, `.tools/b1568/raw/jest-p-plain-K.json`); step 3 |
| PUSH | `PROOF OK` | THE PROOF |
No step reads a file a later step makes.

## D-decisions (drafter)
- D1 **M takes main's counts blob, and K3 rebuilds it** (B1579's D1). M's diff against main is the eight branch paths only; K3's diff against M is the counts file only.
- D2 **Two verifies, not three** (B1579's D2). An `--update-counts` PASS already asserts every other condition before it writes.
- D3 **Any move of main is a STOP, not a second merge** (HOLD 20, REFUSE 4).
- D4 **No CodeQL CLI, no mutation step.** Every byte the seat adds is main's or the gated head's. Hosted CodeQL on the PR head is NOT TESTED in READY and is Tuesday's to read.
- D5 **Identity source is `.tools/b1579/clone`** (most recent clone of the same form; lengths 12 and 46, values never printed).
- D6 **Tool source is `.tools/b1579/`**, not `.tools/b1567/` (B1579's tools already carry the `--plan` mode, the PROOF, the C-57 control, C-89 and the refresher). The kit lists the changes (shas, file list, `pairtable.py` inputs, expected id) and the leftover-name check.
- D7 **`chain.list` minutes 35, not 30**: B1579's two verifies took 27 min 32 s and 28 min 26 s against its 30-minute allowance, and this tree has 14 more cells.
- D8 **The id-superset control is kept (B1579 added it beyond its kit) and its one expected missing id is written into the kit**, so the seat does not stop on a result already predicted by program.
- D9 **Merge subject** `Merge main into the banner and Testing page branch (the access audit and the test pins landed first)` and counts subject `Expected test counts after main's access audit and test pins and the banner slice`, with no branch name (it carries a build number, HOLD 19). Ticket keys allowed: the three of this branch and the four of main.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q1 Gate round.** The gate's finding 1 says "the rebuilt head needs a delta gate" and `landing.txt` line 3 says "re-gate that delta"; B1579's rule (Tuesday's stamp on that kit, and `model-routing.md:109` G2 "follow-ups whose mechanism a prior gate already measured") was that your PROOF rows re-run at source plus hosted Build and CodeQL on the new head suffice. **Default: no new gate round, B1579's rule**, because every byte of K3 is main's blob (gated by #201's and #202's gates) or `a63389b1`'s blob (gated by B1568's gate) except the script-written counts file, and a full plain verify at K3 covers any interaction in jest, including the `rd490` browser cells. The alternative is a G2 round on K3's delta (about 15 minutes of gate time). The kit says the tension in its Level paragraph, so the seat is not misled either way.
- **Q2 Port block.** The commission assigned none. **Default: 9980-9989**, which I checked (0 listeners, 0 hits in 35 kits; 9950-9959 hits the B1580 Composer kit, 9960 and 9970 blocks hit one kit each). The seat starts no server, so this is a label.
- **Q3 Landing order.** Main must not move between your stamp and `READY B1587` (HOLD 20 makes a move a STOP). **Default: land nothing on NexusAI main until READY**; the B1588 records seat touches the records files and Jira only, not main. After READY: re-run PROOF rows 1 to 3 at source, wait for hosted Build and CodeQL on K3, open the PR, land by merge commit pinned to K3 with `landing.txt`'s files (replace `<N>` and the sha); Deploy demo must read skipped.
- **Q4 Merge message form** (D9). **Default: the kit's own subjects.**
- **Q5 The Minors.** The gate's Minors 2 to 4 (dangling words on the Testing page; two other 9999 fixed elements; Deploy demo unshown) are NOT in this kit and go to the NexusAI records pass (B1588 is told to leave the B1568 Minors out until it lands). **Default: as written.**

## UNMEASURED / PREDICTED
- The merged tree's pair (DERIVED 5666 / 353), both verify durations (RELAYED about 28 minutes each from B1579; predicted lock hold 60), and that `rd490`'s browser cells pass on the merged tree (the gate ran them at main plus the head paths at `0fdc77f0`, not at `6335717d`).
- The real `git merge` exit code and its unmerged list (PREDICTED from merge-file and the path sets; no merge ran in any project repo: fence 3). M's parent order (PREDICTED `a63389b1` first) and the rev-list counts (PREDICTED 10 and 6 from the compare API's ahead_by 8 and 4).
- The C-57 id-superset result on the real merged run (PREDICTED missing 1, from two runs).
- Hosted Build and CodeQL on K3, Node 24, and the Deploy demo run a landing would start (the variable `CI_DEPLOY_ENABLED` was not read: no HTTP to hosted hosts).

## Outside-the-fences disclosure
- Writes: the kit, its sidecar and this report, plus scratch files only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s279/d1587/`: contents-API copies of the counts file at five refs, three compare JSONs, raw copies of five workflow/script/test-helper files at `6335717d`, `mf/` (merge-file scratch), `slot.py`, `derive.out`, `idsuper.out`, `fill.py`, `namescan_kit.py`, the first sidecar skeleton and the `stamp_check` outputs. Nothing was written under `/Volumes/Datasec_DEV/!CODING/`. No clone was made. No git command ran in a project repo except `config --local --get` on `.tools/b1579/clone` (lengths only, `--no-optional-locks`).
- GitHub: `gh api -X GET` only (contents, compare, commits, pulls, matching-refs, user), under NexusAI's own `GH_CONFIG_DIR`. No writes, no HTTP to any hosted, demo or production host, no az, docker or ssh, no mail, no Jira. I did not run `decision_queue.sh` in any form; no card was needed. One `tmux list-panes` read.
- Reads in the project folder (read-only): B1579's kit, report, sidecar, STATUS, tools, `raw/` and `logs/`; B1568's `raw/` run JSON and STATUS lines; the jest lock directory; `nexusai-lock.sh` line 2; `scanlib1114.py` lines 1-25; `CLARIFICATIONS.md` by grep (C-57, C-89, `:2067`). Read in the Tuesday tree: the commission, DRAFTER_RULES, B1568_verify's four files, the pickup and today's note by grep, `model-routing.md` lines 95 and 109, `models_latest.json`, `stamp_check.py`, `status_watch.sh`.
- Hook events: one refusal of a `cd` (my first scratch command began with `cd`; re-issued with absolute paths), one refusal of an unquoted `=====` separator (re-issued quoted). Advisories about case-sensitive greps, grep into `cut` and `$?` after a pipe: every count in the sidecar carries a control or a stated source.
- Rule-text drift found: DRAFTER_RULES says `brief_seat.sh` defaults to Opus at "line 24"; today it is `:31` (`LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`). The rule holds; its line pointer is stale. DRAFTER_RULES also writes `/Volumes/Laptop-DEV/` paths: read as `/Volumes/Datasec_DEV/` per the commission.
- Weakest parts: the derivation's blind spot (Q3 of the kit: a cell whose count depends on both changes); whether `rd490`'s browser cells hold on the merged tree (UNMEASURED); and Q1.

DRAFTED B1587: kit 132 lines, sidecar rc 0, questions 5
