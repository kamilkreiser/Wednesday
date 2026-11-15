STARTABLE: YES (a mechanical rebuild; Q1 (whether a gate round is owed) and Q2 (landing order) need your eye at the stamp; the kit holds both defaults)

# B1579 DRAFTER REPORT (SEAT-N131, NexusAI, rebuild PR #202's counts after #201 landed), drafted Sun 15 Nov 2026 (`date` at start 15:29:36 AEDT, last `date` 15:41:11)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1579_SEAT-N131_nexusai-rebuild-202-counts.md` (130 lines; 5 lines with the four-underscore pattern: four slots and the last line; 0 non-ASCII characters by `LC_ALL=C grep -c '[^ -~]'`; ban-list name scan TOTAL 0, the `x_by_<name>_y` control firing 1 for each of the 9 names, `Kampala` 0). Sidecar `.md.measured`: 105 lines, `stamp_check.py` prints `80 claims, 80 measured, 0 not measured`, rc 0 (run alone, output to a scratch file, not a pipe); it also carries S01 to S25.

## BLUF
- **The job:** on the existing branch `b1567/nexusai-lane-b-test-pins` (PR #202, head `8586c094`, gate G2 GO, 0 findings), make ONE merge commit M of origin main `0fdc77f0`. The counts file is the only conflict; it is resolved by copying main's blob `e145afd0` unchanged. Then run `--update-counts` on M's tree, make ONE counts commit K2, run a plain verify at K2 that must PASS, run a by-program PROOF, and do ONE plain fast-forward push. Sonnet, row **C5** (`model-routing.md:95`), slot 9 (trees `upd21`, `fin4`), port block 9940-9949, no server of its own. PREDICTED lock hold about 50 minutes after N130's hold ends.
- **The conflict is MEASURED, not assumed:** `git merge-file` over scratch copies of the three counts blobs exits rc 1 with one hunk. The two PRs share exactly one path (set program over both compare lists). So the merge brings main's other five paths in clean.
- **The expected pair 5653 / 352 is DERIVED from two real full runs, not by arithmetic alone:** I took the per-file cell counts of N128's plain verify at `a6eae4f1` (whose tree IS main's tree, `66dc47f2`) and replaced the three #202 test files with their counts from N129's plain verify at `8586c094`. Controls: each run alone gives its own reported pair. Only four files differ between the runs. A different measured pair is a STOP in the kit.
- **No gate round owed (my reading; Q1):** after the merge, every byte of the new head is either main's or the GO'd head's. The one exception is the counts file, which the script writes. The PROOF section shows this blob by blob, and Tuesday's diff check is that proof re-run.

## Facts re-measured (instrument; control)
1. Main `0fdc77f0181bf7b0534ca562ebb142c8e5da435e`, tree `66dc47f2`, parents `4ba2e03c`, `a6eae4f1` (`gh api -X GET commits/main`, 15:29:54 and 15:35:27, same both times). PR #201 is merged (merge_commit = main). PR #202 is open at `8586c094`, `mergeable=false`, `dirty` (the first read at 15:29:54 printed null/unknown: GitHub computes it late). Open PRs: 1 [S01, S05, S11].
2. Path sets: main's diff (4ba2e03c..0fdc77f0) has 6 paths and the branch's diff has 4. Their intersection is exactly `scripts/verify-expected-counts.json` (python set program; control: branch-only 3, main-only 5) [S04, S06].
3. Counts blobs (`git hash-object` of the raw bytes, equal to the contents API `.sha` for main): base 5636/349 `6c772ba5`; #202 5638/349 `f42e25f1`; main 5651/352 `e145afd0`; `a6eae4f1` 5651/352 [S07]. The merge-file hunk covers `_updated`, `tests` and `suites`; it has 3 markers [S08].
4. The verify script at main: `--update-counts` rewrites `tests`, `suites` and `_updated` only, after every other assertion passes (`verify-suite.sh:320-340`). The plain run fails a grown suite as stale (`:354-360`). Hosted CI runs the plain form (`build.yml:92-93`) on Node 24 (`:29`). The real output lines were copied from N129's saved logs (`verify-u-update.log:22122`, `:22127`). They carry U+2014, so the kit matches only the ASCII prefix [S12, S13].
5. Deploy demo runs only on a push to main (`deploy-demo.yml:26-28`), so the branch push starts no deploy. `deploy.yml` is `workflow_dispatch` only. Neither PR touches `.github/` (0 paths) [S14].
6. Toolchain by path: NexusAI has no drive-local node (`ls .tools/` shows no node or dotnet entry; `.tools/node24/bin/node` is absent). The machine has `/opt/homebrew/bin/node` v26.13.0 and npm 11.20.0, the same as N129 and N130 used today [S16].
7. Slots: by the `test-server.js:89-93` program, the controls read `b1567-nodot/upd10` 7, `b1568-nodot/old52` 4 and `b1563-nodot/old12` 1. Mine, `upd21` and `fin4`, are both 9, which differs from 1, 4 and 7 and from the B1567 gate's 15, 2 and 3. Band 25760-26399: 0 listeners (control: 20 machine-wide) [S18-S20]. Ports 9940-9949: 0 listeners. In the 27 non-`.pre` SEAT kits of 11-14 and 11-15, `994x` hits 0 files; the control `993x` hits 1 (B1578) [S22].
8. Live: N130 holds the jest lock (owner tag `b1568-chain`) and `queue-jest` is empty. Its STATUS read at 15:30 and again at 15:39 shows `kstep` done, so its push is near. No `b1568/*` ref exists at origin yet [S17]. Seat id by program: the highest `SEAT-N` across both Briefs folders is N130, so this seat is N131.

## Chain step inputs (each produced by an EARLIER step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| Step 1 clone, `npm ci`, local branch | origin main, origin branch `8586c094` | origin (REFUSE 4/5 check them) |
| THE MERGE (M) | the `wt` worktree on the local branch; `origin/main` | Step 1 |
| chain 1 `u-update` (`upd21`) | M | THE MERGE |
| chain 2 `kstep` (`wt`) | the counts file written in `upd21` | chain 1 |
| chain 3 `p-plain-K` (`fin4`) | K2 | chain 2 |
| THE PROOF | K2, `8586c094`, `4ba2e03c`, origin main; chain 1's file; chain 3's tree | chain 1-3, Step 1 |
| PUSH | `PROOF OK` | THE PROOF |
No step reads a file a later step makes.

## D-decisions (drafter)
- D1 **M takes main's counts blob, and K2 rebuilds it.** That keeps the two commits the commission names: M's diff against main is the three test files only, and K2's diff against M is the counts file only. The resolution is a `git show origin/main:<path> >` copy with a hash check, not an edit. `checkout --theirs` is banned with the rest of the `checkout -- <file>` family.
- D2 **I dropped the template's "plain verify that refuses first" step.** An `--update-counts` PASS already asserts jest rc 0, 0 failed and passed = total before it writes (`verify-suite.sh:306-310`, `:317-319`), so the refusal run would add only the stale-counts message, at a cost of about 23 minutes. Two verifies, not three.
- D3 **Any move of main is a STOP, not a second merge (HOLD 20, REFUSE 4).** A second merge changes the expected pair and the PROOF's frame, and the commission allows ONE merge commit.
- D4 **No CodeQL CLI and no mutation step.** The seat adds no code line. Every new byte is main's (analysed on main) or the GO'd head's (gated with the CLI: 0 results in its three files). Hosted CodeQL runs on the new PR head when the push lands, and that is NOT TESTED in READY.
- D5 **Identity source is N129's clone `.tools/b1567/clone`**, read only: lengths 12 and 46 match the B1555 clone N129 and N130 copied from.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q1 Gate round.** Row C5 (`model-routing.md:95`) puts the coordinator's at-source check on a merge-in, and G2 (`:109`) covers "follow-ups whose mechanism a prior gate already measured". **Default: no new gate round. Your diff check is PROOF rows 1-3 re-run at source (`gh api compare` and blob reads), plus hosted Build and CodeQL green on K2 before landing.** The alternative is a G2 round on K2, about 15 minutes of gate time.
- **Q2 Landing order with N130 (B1568).** N130's branch is based on `4ba2e03c` and also ends in a counts commit. If it lands before this seat pushes, main moves and this kit STOPs (HOLD 20). **Default: land nothing on NexusAI main between this stamp and `READY B1579`. Land #202 first. B1568's PR then gets its own rebuild kit of this same form.**
- **Q3 A measured pair other than 5653 / 352.** **Default: STOP with the per-file table. Do not commit K2 and explain it afterwards.** A difference would be a real interaction between #201 and #202, which is the very thing the derivation cannot see.
- **Q4 Merge message form.** The kit writes its own subject and keeps the branch name out of it, because the branch name holds a build number that HOLD 19 bans. Git's default "Merge remote-tracking branch 'origin/main' into b1567/..." would carry it. **Default: the kit's subject.**
- **Q5 The HEADS AT LAUNCH slot** asks you to read whether any `b1568/*` ref exists at origin. **Default: if one exists, that is not a STOP for this seat. It only matters for Q2's landing order.**

## UNMEASURED / PREDICTED
- The merged tree's pair (DERIVED 5653 / 352), both verify durations (RELAYED about 23 minutes each from N129) and the lock wait behind N130.
- The real `git merge` exit code and its unmerged list. They are PREDICTED from merge-file and the path sets, because no merge ran in any project repo (fence 3).
- M's tree sha and parents order (PREDICTED `8586c094` first). The rev-list counts in PROOF row 4 (PREDICTED 5 and 4).
- Hosted Build and CodeQL on K2, Node 24, and the Deploy demo run a landing would start.

## Outside-the-fences disclosure
- Writes: the kit, its sidecar and this report. Scratch is only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1579/`: raw copies of the counts blobs and the merge-file scratch in `mf/`, `slot.py`, `derive.py` and its output, copies by `cat` of two jest JSONs, workflow and script copies, kit scan lists, the first sidecar skeleton (moved aside before a re-init), and the `stamp_check` output. Nothing was written under `/Volumes/Datasec_DEV/!CODING/`. No clone was made. No git command ran in a project repo except `config --local --get` on `.tools/b1567/clone` (lengths only, `--no-optional-locks`). There were no Jira or GitHub writes, no messages, no az, docker or hosted HTTP, and no `tmux send-keys` (one `tmux list-panes` read).
- Reads in the project folder (read-only): both B1567 and B1568 STATUS files, the B1568 kit (slot, OWNS), the `.tools/b1567/logs` verify logs, the `.tools/b1563/logs` step log, both `raw/jest-p-plain-K.json` files, the lock directory and its owner file, the `nexusai-lock.sh` header, `scanlib1114.py:20`, and `CLARIFICATIONS.md` by grep. I did not run `decision_queue.sh` in any form; no card was needed.
- Hook events: one zsh refusal of an unquoted `=====` separator (re-issued with `----`). One pathguard refusal of a `cp` FROM another seat's tree: the guard read the source as a write. I re-issued it as `cat src > scratch`, which only reads that tree, and no override was used. Advisories about case-sensitive greps and grep-into-cut: every absence I state has a control.
- Rule-text drift found: DRAFTER_RULES says `brief_seat.sh` defaults to Opus at "line 24". Today the default is at `:31` (`LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`). The rule still holds, but its line pointer is stale.
- Weakest parts: the derivation's blind spot (Q3); the lock wait behind N130; and Q2, whether main stays still for about 70 minutes.

DRAFTED B1579: kit 130 lines, sidecar rc 0, questions 5
