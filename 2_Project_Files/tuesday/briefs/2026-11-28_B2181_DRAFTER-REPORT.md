STARTABLE: YES

# B2181 DRAFTER REPORT (in-session, read-only, Opus) - kit for seat N187: merge main M1 `826bb7a8` into `b2175/rd490-portband` (K `f1df71f5`), regenerate the counts, verify, re-run the rd490 pair, push

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2181_SEAT-N187_nexusai-rd490-merge-main-counts.md` (154 lines; 4 slots plus the last line carry the four-underscore pattern, `/usr/bin/grep -c -E '_''_''_''_'` prints 5). Sidecar `.measured`: 186 claims, 186 filled, `stamp_check.py <kit>` exits 0. Drafting clocks: first `date` 00:01:56 AEDT, last 00:14:25 AEDT, Sat 28 Nov 2026.

## BLUF
- Startable now. Main is still M1 `826bb7a89bfe9517f5aa538a110ab0b1dea3317f` (re-read 00:14:25). The branch is still K `f1df71f5125994d964b695ebc185947fd401642c`. No pull request is open. The live jest lock has no holder and no ticket. No NexusAI pane is live. All 27 NexusAI STATUS files of 24 to 27 Nov end `READY`.
- A real `git merge --no-ff --no-commit` in a scratch clone gives exactly one conflicted path, `scripts/verify-expected-counts.json`. The whole flow was simulated on a hand-set pair 6655 / 421: conflicts PASS, counts PASS, fill PASS, post PASS, and each check's control fired. No jest was run.
- **6655 / 421 is a PREDICTION and the kit treats it as one.** It is main's 6654 / 421 plus the branch's one cell in an existing suite. The seat's update run measures the pair, the frozen `fill2181.py` writes the measured pair into the commit message, and any other pair is a STOP (Q-2). Main's own 6654 / 421 is not just a prediction: the drafter read it in the pull request 269 hosted `Build` log (`VERDICT: PASS` 6654/6654 across 421 suites).
- **The rd490 two-slot check is re-run (step 10) and needs no candidate.** `pair2175.sh` runs both jests inside ONE acquisition of the LIVE lock, as N186 did. What the kit cannot measure is two lock HOLDERS at once (the candidate's counted slots). That gap is written into READY as a named limit for the G1 gate, which reads both this branch and `.tools/b2175/lock/nexusai-lock.sh.candidate` (sha256 `52713e55...`, re-hashed).
- **The counts numstat is `2 2`, not `3 3`** (only `tests` and `_updated` move; `suites` stays 421). `merge2181.py post` checks this, so B2175's ANSWER-1 mistake is not repeated.
- Predicted time: about 70 minutes plus any queue wait. Hard stop about 100. There are three acquisitions: update about 23 minutes, plain about 23, pair about 2 (N186's real runs: 1363 s, 1376 s, 93 s).

## Facts re-measured (instrument; control)
- Refs: `gh api -X GET` under the NexusAI `GH_CONFIG_DIR`.
  - main = M1, with parents BASE `d2aeecf8` and `c02a04c5`.
  - `compare/BASE...M1`: ahead 4, behind 0, six paths.
  - `compare/M1...K`: diverged, ahead 2, behind 4, three paths. This matches s335's "ahead 2 behind 4".
  - `matching-refs/heads/b2175`: one line, at K. Control: `records` length 58. The gh login count of "datasec" is 1.
- Counts pairs (decoded `contents?ref=`): BASE 6634/419, K 6635/419, M1 6654/421, PR 269 head 6654/421.
- Main's pair measured on hosted CI: PR 269 `Build` job 140481663786 log, read by `gh api -X GET --allow-escape-sequences`. It prints `tests=6654 suites=421` as the expectation, `Tests: 6654 passed`, `Test Suites: 421 passed` and `VERDICT: PASS`. M1's own push `Build` (run 45997365963) was still `in_progress` at 00:14:25. It started 12:17:13Z, so it has run about 57 minutes, while the PR build took 39. **Tuesday should read it before landing**; it is not the seat's.
- Unchanged by the merge (`git rev-parse` in scratch):
  - `verify-suite.sh` is `eb9731f5` at BASE, K and M1.
  - `package-lock.json` is `2d7dbece` at all three; sha256 prefix `37e5add354e5`.
  - `package.json`, `jest.config.js` and `deploy-demo.yml` are equal at BASE and M1.
  - The rd490 file and the helper at K are `a92d82b1` and `27c88c3b`.
- Conflict set (scratch clone, `--no-hardlinks --no-checkout` from `.tools/b2175/clone`, which held K and M1; the project checkout held neither): merge rc 1. `--diff-filter=U` and `ls-files -u` name only the counts file.
- Simulation:
  - `merge2181.py counts` on main's file alone: FAIL (control).
  - After a hand-set 6655/421 written by a node line shaped like `verify-suite.sh` 321-335: PASS.
  - `fill2181.py` PASS. Control: refuses an existing out file.
  - `post` PASS with 20 OK lines. Control: a message file carrying 6654 gives FAIL.
  - `conflicts` on the committed tree: FAIL (control).
  - Numstat M1..M2: `3 2` helper, `22 6` rd490, `2 2` counts.
- Prior work (frame: 530 branch refs, 529 distinct heads, `compare/M1...<head>` each, 0 failed reads): only `f1df71f5` touches the rd490 file or the helper. That one hit is the control that the filter fires. 64 heads touch the counts file. Open PRs: none.
- Ports: the helper's rule (sha256 of the path mod 19) was reproduced by program. Controls: `b2152-nodot/mg` 15, `b2143-nodot/chk` 17, `b2175-nodot/pb` 9, `chk` 12, all as recorded.
  - Over the 29 non-`.pre-`, non-`.measured` SEAT files of 27 and 28 Nov, slots 11 and 18 are the ONLY two whose start port has 0 hits. The other slots read 1 to 7; control 22560 reads 5.
  - So the trees are `b2181-nodot/mz` (slot 18, 31520-32159) and `b2181-nodot/pb` (slot 11, 27040-27679).
  - `lsof`: both bands empty. Control: 15 listeners.
- gitleaks 8.30.1: `no leaks found` over the simulated M1..M2 (103 lines) and K..M2. Control: planted random AWS pair, `leaks found: 2`, rc 1.
- Lock: the live `nexusai-lock.sh` sha256 is `cf01bafb...`, 391 lines. The base lists `queue-docker queue-jest released`, with 0 tickets and no owner file (00:05:12, re-listed 00:14:25). The candidate sha256 equals N186's READY line.
- Model:
  - The NexusAI `CLAUDE.md` names no Claude model. `grep -c -i -E 'opus|sonnet|claude model|BRIEF_SEAT_LEVEL'` prints 0; control `'model'` prints 5.
  - The routing row is C2, line 92 (Sonnet). The id is `claude-sonnet-5-5` (`models_latest.json` line 23). The gate is G1, line 108.
  - `CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude` matches all 47 occurrences in the 27 and 28 Nov SEAT kits (ledger 2026-11-26 R333 row).
- Deploy:
  - A later merge of this branch to main starts `Deploy demo`. `on.push` to main ignores only `**.md`, `docs/**` and `tests/**`.
  - Its `build` and `deploy` jobs need `vars.CI_DEPLOY_ENABLED == 'true'` (lines 53 and 91), and `deploy` is bound to the `demo` environment (line 95).
  - On M1's push the run concluded `skipped`, with both jobs skipped. The C-224 hold (CLARIFICATIONS line 2412) stands.
- Landing rule: `CLARIFICATIONS.md` line 2067, "Never squash, never rebase".

## D-decisions
- D-1. Two new frozen programs, written in the drafter's scratch and copied by the seat:
  - `merge2181.py` is B2152's `merge2152.py` re-pinned to K, A, M1 and BASE. Its other changes: the path set is three, the pair is main's plus 1 and 0, the counts diff is `_updated` and `tests` only, and the numstat is `2 2`.
  - `fill2181.py` writes the message from the measured pair, so the pair is never typed. `msg-M.txt` is a template with `@T@` and `@S@`.
  - `v2152.sh`, `pair2175.sh` and `pairsum2175.py` are byte copies of N186's frozen files (the sha256s match B2175's table).
- D-2. One clone `.tools/b2181/clone`, cloned from the project checkout and fetched through the deploy key, as B2152 and B2175 did. Worktree `mz` is made `-b b2175/rd490-portband` at K. Worktree `pb` is made `--detach` at M2 for the pair only.
- D-3. Three acquisitions: update (mid-merge, Linux shape), plain at M2, and the pair at M2. The pair comes last so a pair failure leaves a tested M2 unpushed, not a half-made merge.
- D-4. The commission says "re-read at Step 0", so REFUSE 4(b)-(e) run at Step 0 and again at Step 1. A move of main at Step 0 or Step 1 is a STOP. At the last look, HOLD 20 applies with B2152's rule.
- D-5. REFUSE 4(e) refuses a live lock whose sha256 is not `cf01bafb`, so the verify never runs under a swapped lock.
- D-6. The commit message names only RD-1051, the branch's ticket. RD-1052 (the lock) is not in this branch's files.

## Questions for Tuesday (each with its default)
- Q-1. Builder model: Sonnet, row C2. The NexusAI CLAUDE.md is silent. N186 ran Opus because its Part L was the lock; this kit is a merge plus the project command. Default: Sonnet (`BRIEF_SEAT_LEVEL=sonnet`).
- Q-2. A measured pair other than 6655 / 421 stops before the commit, naming both pairs. The alternative is to accept any PASS pair and record it. Default: STOP.
- Q-3. Three acquisitions, including the rd490 pair re-run at M2 (about 2 minutes). Default: yes.
- Q-4. The update run happens inside the merge (index conflicted until the `git add`), in the Linux shape. This was B2152's Q-5, and it worked there. Default: yes. A red cell naming git or the index is a STOP.
- Q-5. If main moves after M1 but not in the counts file, the seat still pushes M2. If the counts file moved, the seat stops before the push. Default: as written (B2152's Q-6).
- Q-6. Hard stop: launch plus about 100 minutes, plus any queue wait. Default: stamp launch + 100.
- Q-7. The commit message names RD-1051 only. Default: yes.

## UNMEASURED
- The whole suite at the merged tree, in either shape. The pair 6655 / 421 is PREDICTED.
- `PAIRSUM m2` at M2, and its ports in each worker-1 band (PREDICTED from the slots).
- The seat's clone, `npm ci`, worktrees, wrappers and push. Real Linux. The hosted build of the coming pull request. M1's push `Build` (still in progress).
- The candidate lock with two real holders (never run anywhere). This is a named limit for G1.
- STOP-severity checks never run on a real output: `merge2181.py` and `fill2181.py` ran only on the drafter's simulated merge with a hand-set pair. HOLD 69 says a failure traceable to their wording is a `STOPPED: NEEDS TUESDAY` question.
- The chain's inputs, by step. Each is produced by an earlier step or exists at drafting:

| step | inputs |
|---|---|
| 0 trees | K and M1 in the clone (Step 1), frozen files (Step 0) |
| 1 quiet | the live base |
| 2 merge | steps 0 and 1 |
| 3 mainfile | step 2 |
| 4 wrapper | N186's three wrappers (exist) |
| 5 linux-update | steps 3 and 4 |
| 6 pair | step 5 |
| 7 static | step 6 |
| 8 mid-check | step 6 |
| 9 plain | step 6 |
| 10 pair-m2 | step 6 (M2), for the `pb` tree and the pair wrapper of step 4 |
| 11 last-look | Step 1 |
| push | steps 6 to 11 |

## Outside-the-fences disclosure
- GitHub reads were `gh api -X GET` only, under the NexusAI `GH_CONFIG_DIR`. That includes 529 compare reads, the actions runs and jobs reads, and one Actions job-log GET (GitHub's log endpoint). No HTTP to any NexusAI host.
- One anonymous `git ls-remote https://github.com/datasecau/Reporting_Dashboard_Au.git` was run by mistake while probing. It is read-only, its output was discarded, and it returned rc 0.
- Git writes were made only in the drafter's scratch clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2181/clone`: the clone itself (from `.tools/b2175/clone`, a read of that repo), config of the identity `scratch`, checkout, merge, add and commit. There was no fetch, no deploy-key use and no push. One combined command was refused by the no-cd hook before it ran (a `git -C` path held in a variable). Every write verb after that used the typed path.
- Read-only reads in the NexusAI project:
  - N186's and N185's STATUS, wrappers and logs.
  - `CLARIFICATIONS.md` lines 2067 and 2412, and the project `CLAUDE.md`.
  - The live lock and the candidate, hashed only.
  - The lock base listing.
  - `scanlib1114.py`, through `names2142.py`. Its output `raw/names.txt` sits in scratch and was never printed.
  - Clone identity lengths and the `core.sshCommand` length (107); no value was printed.
- Ran: node (slot arithmetic, the scratch counts write; no jest), gitleaks, lsof, tmux list-panes, python.
- No write in the NexusAI project, Jira, GitHub, cards or mail. Scratch in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2181/`:
  - `clone`, `frozen` (the six seat files), `raw`
  - `slot.js`, `cmp1.sh`, `fill_measured.py`
  - `kits.txt`, `branches.tsv`, `shas.txt`, `compare.tsv`
  - `pr269-build.log`, `verify-suite.sh.M1`, `deploy-demo.yml`, `CLAR.M1.md` (empty: the file is not in the repo)
  - `rd490.K.js`
- `raw/planted.out` holds gitleaks' report of the random planted pair. The values are random, not real keys.
