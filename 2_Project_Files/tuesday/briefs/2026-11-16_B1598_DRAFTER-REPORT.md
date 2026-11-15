STARTABLE: YES (a mechanical rebuild in B1587's exact form; the conflict, the pair and the slot are measured or derived from real runs; the one open call, who gates the delta, is Tuesday's and the kit holds the verdict's own default)

# B1598 DRAFTER REPORT (SEAT-N135, NexusAI, rebuild the first-run and sign-in branch's counts after #204 landed), drafted Mon 16 Nov 2026 (`date` at start 01:54:58 AEDT, last `date` 02:00:25 for the final measurements)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1598_SEAT-N135_nexusai-rebuild-b1595-counts.md` (132 lines; 5 lines with the four-underscore pattern: four slots and the last line; 0 non-ASCII lines by `LC_ALL=C grep -c '[^ -~]'`; underscore-aware ban-name scan over the kit 0 for each of kamil, kreiser, kam, peter with the `x_by_<name>_y` control firing 1 each). Sidecar `.md.measured`: 108 lines, `stamp_check.py` prints `82 claims, 82 measured, 0 not measured`, rc 0 (output to `fleet/state/s280/d1598/sc.out`); it also carries S01 to S26.

## BLUF
- **The job:** on the existing branch `b1595/nexusai-f1-first-run-login-fixes` (head `b2732d92`, base `117bf81e`, four commits, gate G1 GO WITH FINDINGS, finding F1 = this rebuild), make ONE merge commit M of origin main `2a033405` (PR #204's merge commit, landed 01:15 AEDT). The counts file is the only conflict; it is resolved by copying main's blob `f963bd18` unchanged. Then `--update-counts` on M's tree, ONE counts commit K2, a plain verify at K2 that must PASS, a by-program PROOF, ONE plain fast-forward push. Sonnet, row **C5** (`model-routing.md:95`), slot 2 (trees `upd4`, `fin24`), port block 9880-9889 (my proposal), no server of its own. PREDICTED lock hold about 62 minutes (B1587 measured 59.5 for the same two verifies, this tree adds 41 cells and 8 suites).
- **The conflict is MEASURED, not assumed:** `git merge-file -p` over scratch copies of the three counts blobs exits rc 1 with one hunk and 3 markers (control: all three = base gives rc 0, 0 markers). The two path sets share exactly one path, the counts file (branch 12 paths, main 9, union 20). The gate's own `merge-tree` against `2a033405` says the same (RELAYED).
- **The expected pair 5707 / 361 is DERIVED from two real full runs and equals the gate's relayed number:** main's tree run (B1592's plain verify at `78a1c4fb`, whose tree `886135be` equals main's, 5686/356) with the eight branch test files (five new, three edited) replaced by the branch run at `b2732d92` (5687/358). Derived both ways the per-file maps are equal. The kit marks 5707/361 as RELAYED from the gate and DERIVED, never the seat's; the seat's own `--update-counts` run decides it.
- **The id-superset control differs from B1587's:** zero missing ids expected (no title was renamed on either side: predicted merged ids 5707, union 5707, missing 0; control drop one id gives 1). The kit tells the seat to change `pairtable.py`'s final lines to `IDSUPERSET-NONE-MISSING yes` and to STOP on any missing id.
- **No pull request exists for this branch** (0 open PRs). The seat pushes; Tuesday commissions the small G1 delta gate on M and K2, opens the PR and lands by merge commit pinned to K2 using `2026-11-16_B1595_verify/{landing.txt,merge-subject.txt,merge-body.txt}` with the sha replaced; Deploy demo must read skipped.

## Facts re-measured (instrument; control)
1. Main `2a033405a4ef8c9709e11c7c711e9e8d65e1a453`, tree `886135be`, parents `117bf81e` and `78a1c4fb`, committed 2026-11-15T14:15:29Z = 01:15 AEDT (`gh api -X GET commits/main`, 01:55). `78a1c4fb`'s tree is also `886135be` (commits API on both). Open PRs 0 [S01, S04].
2. Path sets: main's diff (`117bf81e...2a033405`, ahead 8, behind 0) has 9 paths; the branch's (`117bf81e...b2732d92`, ahead 4) has 12. Intersection exactly `scripts/verify-expected-counts.json` (python set program; control: branch-only 11, main-only 8, union 20) [S04, S06]. For the eleven non-counts branch paths the blob at main equals the blob at base (S25 table), so main never touched them; the five new test files are absent at base and main (404).
3. Counts blobs (python sha1 of the raw API bytes equals the contents API `.sha`, True four times): base 5666/353 `76a72af8`; branch head 5687/358 `027c7859`; main 5686/356 `f963bd18` (also at `78a1c4fb`) [S07]. Merge-file hunk covers `_updated`, `tests`, `suites`; 3 markers [S08].
4. Verify script at main: `--update-counts` sets `tests`, `suites`, `_updated` only (`verify-suite.sh:317-340`, `_updated` at `:333`, UPDATED line `:337`); the plain run fails a grown suite as stale (`:354-360`); PASS line `:366`. Hosted CI runs the plain form (`build.yml:92-93`) on Node 24 (`:29`). Line pointers printed by `grep -n` and `awk NR==` over the raw files at `2a033405` [S12, S13].
5. Deploy demo runs only on a push to main (`deploy-demo.yml:26-28`; `paths-ignore` `'**.md'`, `'docs/**'`, `'tests/**'`), so the branch push starts nothing. The branch changes 3 `static/` and 8 `__tests__/` paths (not ignored), so Tuesday's later landing WILL start Deploy demo; both jobs must read skipped (`landing.txt` lines 10-12). Neither side touches `.github/` or `package*.json` (0 and 0 by program) [S14].
6. Toolchain by path: NexusAI has no drive-local node (`ls .tools | grep -i -c -E 'node|dotnet'` 0; control `grep -c b1587` 1; `.tools/node24/bin/node` absent). Machine node `/opt/homebrew/bin/node` v26.13.0, npm 11.20.0 at 02:00 [S16].
7. Slots: tonight's used slots by program: B1592's eight trees all 11, B1595's six all 14, B1587 18, B1579 9, B1567 7, B1568 4, B1563 1 (`slot-controls.out`). Mine `b1598-nodot/upd4` and `fin24` are both 2 (`slot-cand.out`); band 21280-21919 has 0 listeners (control 14 machine-wide at 01:57, 15 at 02:00) [S18-S20].
8. Ports: 9880-9889 has 0 listeners and 0 hits in the 44 non-`.pre` SEAT kits of 11-15 and 11-16 by word-boundary scan (control `994[0-9]` 3 hits). Rejected: 9990 (B1596), 9980 (B1587, B1593, B1596), 9970 (B1582), 9890 (B1571, B1577), 9960 (B1581, B1594) [S22].
9. Live: no `NexusAI` cockpit name in `tmux list-panes -a` (0; the named panes are `tuesday` and `fleet-monitor`); the jest lock has no owner file and `queue-jest` is empty. Seat id by program: the highest `SEAT-N` in the briefs folder is N134, so this seat is N135 (as commissioned) [S17].
10. B1587's tools are the source (READY `3baa9584`, STATUS Corrections read): all fifteen files present; the kit lists the per-file counts of lines naming the old build (proof.py 22 leads) so the seat knows what to change [S26].

## Chain step inputs (each produced by an EARLIER step or present at BASE)
| step | inputs | produced by |
| --- | --- | --- |
| Step 1 clone, `npm ci`, local branch | origin main, origin branch `b2732d92` | origin (REFUSE 4/5 check them) |
| THE MERGE (M) | the `wt` worktree on the local branch; `origin/main` | Step 1 |
| chain 1 `u-update` (`upd4`) | M | THE MERGE |
| chain 2 `kstep` (`wt`) | the counts file written in `upd4` | chain 1 |
| chain 3 `p-plain-K` (`fin24`) | K2 | chain 2 |
| THE PROOF | K2, `b2732d92`, `117bf81e`, origin main; chain 1's file; chain 3's tree and run | chain 1-3, Step 1 |
| `pairtable.py` inputs | main's run (`.tools/b1592/raw/jest-p-plain-K.json`) and the branch's run (`.tools/b1595/raw/jest-p-plain-K.json`), both `cp`'d into `raw/`; step 3's run | already on disk at BASE (both files exist, `ls -la`: 2826704 and 2826130 bytes); step 3 |
| PUSH | `PROOF OK` | THE PROOF |
No step reads a file a later step makes.

## D-decisions (drafter)
- D1 **M takes main's counts blob, and K2 rebuilds it** (B1579's D1, B1587's D1). M's diff against main is the eleven branch paths only; K2's diff against M is the counts file only.
- D2 **Two verifies, not three.** An `--update-counts` PASS already asserts every other condition before it writes.
- D3 **Any move of main is a STOP, not a second merge** (HOLD 20, REFUSE 4).
- D4 **No CodeQL CLI, no mutation step.** Every byte the seat adds is main's or the gated head's; the gate already ran CodeQL 2.27.4 on the head (64 to 63 results). Hosted CodeQL on the PR head is NOT TESTED in READY and is Tuesday's to read.
- D5 **Identity source is `.tools/b1587/clone`** (most recent clone of the same form; lengths 12 and 46, values never printed).
- D6 **Tool source is `.tools/b1587/`** (finished, READY, carries `--plan`, PROOF, C-57 control, C-89, the refresher). The kit lists the changes and the leftover-name check.
- D7 **`chain.list` minutes 40, not 35**: B1587's verifies took 29 min 42 s and 29 min 44 s against its 35-minute allowance, and this tree has 41 more cells and 8 more suites.
- D8 **The id-superset control is kept but its expected result is "none missing"** (B1587's one expected rename does not apply; no title moved). The seat replaces the rename line in `pairtable.py`.
- D9 **Merge and counts subjects** as written in the kit, with no branch name (it carries a build number) and only the nine allowed ticket keys (six from the branch's commit messages, three from #204's). The gate's `merge-subject.txt` is for the later PR landing, not for M.
- D10 **The Level paragraph names the delta gate** (G1, `model-routing.md:108`, Opus first) as owed after the seat, per the verdict's F1 and `landing.txt` lines 3-6; the seat is told it is not the seat's to commission.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q1 Gate round.** F1 and `landing.txt` ask for the rebuilt delta to be re-gated; you told me it is a small G1 delta gate on M and K2 only (round 2 of 2 on this branch's G1 row). **Default: commission it after READY, against the PROOF rows' claim that K2 is main's blobs plus the gated head's blobs plus the script-written counts file**; the seat's full plain verify at K2 is not a substitute for the gate's own reads (the page-script probe, CodeQL on the merge), but it covers any jest interaction.
- **Q2 Port block.** None was assigned. **Default: 9880-9889**, checked (0 listeners, 0 kit hits). The seat starts no server, so it is a label.
- **Q3 Landing order.** Main must not move between your stamp and `READY B1598` (HOLD 20 makes a move a STOP). **Default: land nothing on NexusAI main until READY.** The sibling lane `rd-721-icons-vendor-s91p` rewrites `login.html:10` (gate F3) and would conflict; it is not touched here and must not land first without its seat making the href absolute.
- **Q4 Message form** (D9). **Default: the kit's own subjects.**

## UNMEASURED / PREDICTED
- The merged tree's pair (DERIVED 5707 / 361, RELAYED from the gate's merge run; not measured by anything the drafter ran), both verify durations (RELAYED about 30 minutes each from B1587; predicted hold 62), and that the jsdom cells of `rd456`, `rd475` and `rd481` and the new `rd888`/`rd926`/`rd988` files pass together on the merged tree (the gate ran the full merged verify but the kit's seat is the first to commit it).
- The real `git merge` exit code and its unmerged list (PREDICTED from merge-file and the path sets; the gate's `merge-tree` rc 1 is a RELAYED agreement; no merge ran in any project repo: fence 3). M's parent order (PREDICTED `b2732d92` first) and the rev-list counts (PREDICTED 10 and 6 from the compare API's ahead_by 8 and 4).
- The C-57 id-superset result on the real merged run (PREDICTED missing 0).
- Hosted Build and CodeQL on K2, Node 24, and the Deploy demo run a landing would start (the variable `CI_DEPLOY_ENABLED` was not read: no HTTP to hosted hosts).
- The gate's F2 (probe residue in the operator's home, `~/data/.machine-id`) is closed by the gate itself; the kit does not ask the seat to re-check it.

## Outside-the-fences disclosure
- Writes: the kit, its sidecar and this report, plus scratch files only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s280/d1598/`: contents-API copies of the counts file at four refs (`c/`), the two compare JSONs, `main.json`, raw copies of four workflow/script/test-helper files at `2a033405` (`src/`), `mf/` (merge-file scratch), `derive.py`/`derive.out`, `slot-controls.out`, `slot-cand.out`, `blobs11.out`, `blobs8.out`, `fill.py`, the `stamp_check` outputs. Nothing was written under `/Volumes/Datasec_DEV/!CODING/`. No clone was made. No git command ran in a project repo except `config --local --get` on `.tools/b1587/clone` (lengths only, `--no-optional-locks`); `git merge-file` and `git hash-object` ran on scratch copies.
- GitHub: `gh api -X GET` only (contents, compare, commits, pulls, matching-refs, user), under NexusAI's own `GH_CONFIG_DIR`. No writes, no HTTP to any hosted, demo or production host, no az, docker or ssh, no mail, no Jira. I did not run `decision_queue.sh` in any form; no card was needed. Two `tmux list-panes` reads and `lsof` reads.
- Read in the project folder (read-only): B1587's tools, STATUS, logs and `raw/` names; `.tools/b1592/raw/jest-p-plain-K.json` and `.tools/b1595/raw/jest-p-plain-K.json` (per-file counts only, by `derive.py`); STATUS last lines of B1587, B1592 and B1595; the jest lock directory; `nexusai-lock.sh` line 2; `scanlib1114.py` line 20; `CLARIFICATIONS.md` by grep and `awk NR==`. Read in the Tuesday tree: DRAFTER_RULES, the template kit, its report and sidecar, the B1579 kit (first 40 lines), B1595_verify's VERDICT and landing.txt and the merge-subject/merge-body text, `model-routing.md` lines 95, 108 and 109, `models_latest.json`, `brief_seat.sh` grep, `stamp_check.py` header, the kit briefs folder listing and port-block lines.
- Hook events: one refusal of a multi-word `$K` list used unquoted in a `for` (re-run inside `bash <<EOF`), one refusal of an unquoted `====` separator (re-issued with `----`); advisories about case-sensitive greps and grep into `cut`: every count in the sidecar carries a control or a stated source.
- Rule-text drift: DRAFTER_RULES says `brief_seat.sh` defaults to Opus at "line 24"; today it is `:31` (`LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`), as B1587's report already noted. The rule holds. DRAFTER_RULES writes `/Volumes/Laptop-DEV/` paths: read as `/Volumes/Datasec_DEV/` per the commission.
- Weakest parts: the derivation's blind spot (a cell depending on both changes at once); the kit's 'line pointer' `landing.txt` lines 3-6 and 10-12, which I printed by `awk` once each at drafting; and Q1 (the gate's scope is Tuesday's).

DRAFTED B1598: kit 132 lines, sidecar rc 0, questions 4
