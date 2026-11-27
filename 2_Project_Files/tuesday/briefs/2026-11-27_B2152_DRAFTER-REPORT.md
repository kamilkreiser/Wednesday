STARTABLE: YES

# B2152 DRAFTER REPORT (in-session, read-only, Sonnet) - kit for seat N185: merge main (M1) into `b2143/lane3-kit1` (K), regenerate the counts

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2152_SEAT-N185_nexusai-lane3-counts-merge.md` (144 lines, 4 slots plus the last line carry `____`; `/usr/bin/grep -c -E '_''_''_''_'` prints 5), sidecar `.measured` (141 claims, 141 filled; `stamp_check.py <kit>` exits 0). Drafting clocks: first `date` 15:08:31 AEDT, last 15:17:42 AEDT, Fri 27 Nov 2026.

## BLUF
- Startable now: no jest lock is held (`queue-jest` empty, no lock folder), the only live pane is `tuesday`, main is M1 `de39619cac31e475fe46350e29bdb3047b86e046`, the branch is K `895da3f4630e170e038a1b5b2c78008ae7633b93`, no pull request is open.
- The merge's conflict set was proved in a scratch clone by a real `git merge --no-ff --no-commit`: exactly one conflicted path, `scripts/verify-expected-counts.json`. The six-path / blob / counts-shape checks of the gate's step 0b all pass on a simulated merge commit (hand-set pair 6634 / 419: NOT the project command; no jest was run).
- The pair 6634 / 419 stays PREDICTED (M1 6606 / 417 plus the branch's 28 and 2).
- Predicted time about 70 minutes, hard stop about 90 (two whole-suite runs, the lane's last two read 1438 s and 1453 s).

## Facts re-measured (instrument; control)
- main sha, branch sha, parents of M1, `compare BASE...M1` ahead 10 behind 0 with nine paths = the nine paths of pull request 267: `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (control: `matching-refs/heads/records` length 58; login count of "datasec" 1).
- Counts blob pairs: BASE 6530 / 411, K 6558 / 413, M1 6606 / 417 (decoded `contents?ref=<sha>`).
- Conflict set: scratch clone (`--no-hardlinks` of the project checkout, origin set to GitHub, explicit-refspec fetch through the deploy key, rc 0); merge rc 1; `diff --diff-filter=U` and `ls-files -u` name only the counts file. The program's own control refuses a two-path list.
- `scripts/verify-suite.sh` is blob `eb9731f5...` at BASE, K and M1; the parse block is lines 237 to 256 and the `--update-counts` write lines 320 to 335 (`awk NR==`), which confirms the gate's reason for writing main's file first.
- Simulated flow (scratch only, repeated twice): `merge2152.py conflicts` PASS, `counts` PASS, `post` PASS (23 OK lines); controls: `counts` before the pair is set FAIL (3 lines), `post` on a wrong earlier simulated commit FAIL (message and counts shape). The post program checks: parents (K then M1), message equals the frozen one-line text, ASCII, name scan with planted control (real four names), id scan with planted control, `M1 M2` diff = the six paths, five non-counts blobs equal K's and the pinned shas, `K..M2` path set equals `BASE..M1` (nine), main's non-counts blobs at M2, counts diff `_updated`/`suites`/`tests` only, numstat `3 3`, identity ae = ce = configured, clean tree, no merge left.
- Port band: `b2152-nodot/mg` slot 15, 29600 to 30239 (control: `b2143-nodot/chk` slot 17 reproduced); 0 kit hits (control 22560 reads 6 of 30 kits); `lsof` band empty (control 15 listeners). Chosen after `chk`, `merge`, `mrg`, `vfy` hit other kits' band edges.
- Real-run literals: copied by `grep -c -F` from the lane's own logs `.tools/b2143/logs/verify-linux-update.log` and `verify-plain.log` (the em dash is named, not typed); 413 `PASS` lines each, `EADDRINUSE` 0 in each.
- gitleaks 8.30.1: `no leaks found` over the simulated M1..M2 diff (538 lines); the planted-key control read `leaks found: 1`, rc 1 (the kit says match the words, not the number, because kit B2143 said 2).
- Git-reading tests: 18 test files mention git; the working-tree lister `rd719-chartjs-vendored.test.js` keeps only `.html` and `.js`, so a merge in progress should not change it (UNMEASURED under jest).

## D-decisions
- D-1. Two new frozen files (in the drafter's scratch, copied by the seat): `merge2152.py` (the checks above) and `msg-M.txt` (the commission's message, one line); `v2152.sh` is B2143's `v2143.sh` with one header word changed (diff printed one line); `names2142.py` is used from its s332 path (the B2143 addendum's path). The existing `static2143.py` cannot judge a merge commit (it asserts a path set per tag), so it is not used.
- D-2. One jest tree `b2152-nodot/mg`, a worktree created `-b b2143/lane3-kit1` at K, doing the merge, both verifies, the commit and the push; a fresh clone and `npm ci` under `.tools/b2152` (the lane's `.tools/b2143` is read only).
- D-3. The commit is a plain `git commit -F` with no path list (git refuses a partial commit in a merge); the kit says so as HOLD 70.
- D-4. Landing text's wording "inside ONE jest-lock acquisition" read as the update run; the plain verify at M2 needs the commit, so it is a second acquisition.
- D-5. No `merge --abort` by the seat (an abort is a STOP); a merge left in progress is named in the handover.

## Questions for Tuesday (each with its default)
- Q-1. The seat commits the merge (the landing text calls it "Tuesday's commit"; the commission says the seat). Default: yes.
- Q-2. Sonnet builder, row C2 (line 92; model id `claude-sonnet-5-5`, models_latest line 23). Default: Sonnet.
- Q-3. Hard stop: about 90 minutes from launch (predicted 70: clone and `npm ci` 10, merge and checks 10, update run 25, plain verify 25, push), plus any jest-queue wait. Default: stamp launch + 90.
- Q-4. Two jest acquisitions (update run, then the plain verify at M2) rather than one. Default: two.
- Q-5. The update run happens inside the merge (index still conflicted until the `git add`), in the Linux shape the lane's K used (`TMPDIR=/tmp`, persistent dot-free `RUNNER_TEMP`). Default: yes, as the landing text orders; a red cell naming git or the index is a STOP.
- Q-6. If main moves after M1 but not in the counts file, the seat still pushes M2 (Tuesday re-reads main before opening the pull request); if the counts file moved, it stops before the push. Default: as written.

## UNMEASURED
- Whole suite at the merged tree (pair 6634 / 419 PREDICTED; passing under the Linux shape and the own shape); the seat's clone, `npm ci` and worktree; the lock wrappers as the seat writes them; the push; real Linux; the hosted build.
- Every seat-typed command's behaviour (flagged `UNMEASURED` in the sidecar); `git merge-base K M1` as typed (the compare read implies BASE).
- STOP-severity checks never run on a real output: `merge2152.py` ran only on a simulated merge with a hand-set pair, so a failure the seat can trace to its wording is a `STOPPED: NEEDS TUESDAY` question, not the seat's to amend (the kit's HOLD 69 says so).
- Inputs of the chain, by step (each is produced by an earlier step or exists at BASE): step 0 K and M1 (Step 1 clone), frozen files (Step 0); step 2 clone and step 0; step 3 step 2; step 4 the b2143 wrappers (exist); step 5 steps 3 and 4; step 6 step 5; step 7 step 6; step 8 step 6; step 9 Step 1. The kit prints the table.

## Outside-the-fences disclosure
- Read-only gh reads under the NexusAI `GH_CONFIG_DIR` only (`-X GET`); no HTTP to a host.
- Git writes only in the drafter's own scratch clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d2152/clone` (clone, remote set-url, `core.sshCommand` from the project's deploy key path (value not printed), fetch of two refs from GitHub, checkout, merge, add, commit with identity `scratch`). Nothing was pushed.
- Read-only reads of NexusAI project files: the lane's `.tools/b2143` wrapper and log files, `CLARIFICATIONS.md` line 2067, the lock base listing, the STATUS last lines, session-tools `nexusai-lock.sh` header and `scanlib1114.py` (via `names2142.py`, output file in scratch, names not printed).
- Ran: node (slot arithmetic, a scratch counts write; no jest), gitleaks, lsof, tmux list-panes.
- A mis-typed redirect created `/tmp/null` (189 bytes of git merge text) at 15:09; moved at 15:17 to `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d2152/_quarantine/stray-tmp-null.txt` (189 bytes, present; the move printed only an owner-copy warning). Disclosed for the record.
- No write in the NexusAI project folder, Jira, GitHub, cards or mail. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d2152/` (clone, frozen, helper scripts, `names.txt` holding the four ban-list names: never printed, to be quarantined or left for Tuesday's choice).
