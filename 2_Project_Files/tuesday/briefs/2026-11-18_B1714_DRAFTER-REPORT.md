STARTABLE: YES, but only after #222 is merged into main (the kit's REFUSE 4a refuses otherwise); Tuesday stamps after that.

# B1714 drafter report (SEAT-N152, NexusAI NX-M counts on main)
Drafted Wed 18 Nov 2026, `date` readings 14:14:14, 14:15:29, 14:17:06 and 14:20:29 AEDT. Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1714_SEAT-N152_nexusai-nx-m-counts-on-main.md` (106 lines), sidecar `.measured` 103 of 103 claims, `stamp_check.py <kit>` rc 0 (run alone). Stamp slots: `/usr/bin/grep -c -E '_''_''_''_'` = 5 (four slots plus the last line).

## BLUF
- One lock acquisition, four chain steps: `update` (the verify's own `--update-counts` in `b1714-nodot/upd20` on the merge commit M), `kstep` (counts file alone as K), `p-plain-K` (a second plain verify in `b1714-nodot/chk10`), `mainmove-last`. The merge M, the clone and the trees are made before the lock (no jest). Setup about 40 minutes, lock hold about 50 (PREDICTED; Tuesday sets the HARD STOP slot).
- Refuses if #222 is not `closed` and merged or its merge sha is not an ancestor of origin/main (control: main is not an ancestor of the branch, rc 1), if any open PR touches the counts file or the lane's two test files, or if the remote branch is not at `50e6db9a`.
- No rebase, no force-push, no PR. Conflict property: exactly `scripts/verify-expected-counts.json` (RELAYED from the gate's measurement on 078e7b3d; the drafter may not run merge-tree). Resolution takes main's blob by `git show ... >` file with a blob-hash equality check; M subject is the given `Merge main into the re-drive and clear-key tests branch`; K subject `RD-717 and RD-749: regenerate the expected counts after the merge`.
- If main moves again before the push: no second merge, no push, `STOPPED` (HOLD 13). Default for Q-1 below.

## Facts re-measured with instruments (all via GET-only `gh api` under the NexusAI `GH_CONFIG_DIR`, or local `ls`, `lsof`, `tmux`)
| fact | printed |
|---|---|
| main | `832bf2d9efff51d58d44feb48c811798fec1da55` (branches/main and matching-refs/heads/main agree) |
| branch head at origin | `50e6db9ae29b024079bf1943a4341a2a76336854` (matching-refs/heads/b1691) |
| compare main...branch | ahead_by=3 behind_by=7 status=diverged, merge_base 2de5e84c |
| #221 / #220 / #219 | merged=true; merge shas 078e7b3d558382689900fbf73a25f3cc5bf2f5a7 / 832bf2d9... / 5b3ca950f551399945cff493f1e19558870ae97a |
| #222 | state=open merged=false head 700ed93a9da2a91613c0fcee00d32ffc65298bd6; files rd798 (+33 -25) and rd799 (+1 -1) only; open PR count 1 |
| counts file | 2de5e84c 5870/377; branch 50e6db9a 5876/377; 078e7b3d and 832bf2d9 5881/378 |
| paths main moved over 2de5e84c (compare to 832bf2d9) | npm-audit workflow, HISTORY.md, audit-prod test, rd385 test, backend/server.js, healthSweeperScheduler.js, scripts/audit-prod.js, the counts file; rd681/rd684 matches 0 |
| lane blobs at 50e6db9a | rd681 `362052d5`, rd684 `04f6164d` (contents API sha) |
| counts-file diff shape | simulated with the script's node logic on main's file: 4 lines changed (`_updated`, `tests`); control self-diff 0. A first simulation by python json.dumps changed 6 lines (it escapes the dash in `_why`), which is an artefact, not the script's behaviour |
| verify script literals | main `scripts/verify-suite.sh` 367 lines: `VERDICT: PASS` count 1 (line 366, long dash after it), `GREW` 1 (line 357), control absent string 0; update mode refuses while MIN_TESTS/MIN_SUITES set (line 234) |
| workflows | `build.yml` on pull_request to main and push to main; `deploy-demo.yml` on push to main (paths-ignore md, docs, tests) plus dispatch; `deploy.yml` dispatch only |
| slot 8 | free: slots named in non-pre-stamp SEAT-N kits of 17 and 18 Nov are 0-7, 9, 13, 15, 16, 17; `lsof -nP -iTCP:25120-25759 -sTCP:LISTEN` 0 lines (control: whole-machine listen call 12 lines); trees `b1714-nodot/upd20` and `chk10` both slot 8 by program (controls: `b1691-nodot/old9` 7, `b1680-nodot/old34` 2); panes only `tuesday` and `fleet-monitor` |
| paths free | `.tools/b1714`, `b1714-nodot`, B1714 STATUS all absent |
| toolchain | node v26.13.0, npm 11.20.0, no `.tools/node*` (count 0), CI Node 24 (`build.yml:29`) |

## Inputs of each chain step (each from an earlier step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| update | upd20 at M, clone `node_modules` | THE WORK steps 1-4 (before the lock) |
| kstep | regenerated counts file | step `update` |
| p-plain-K | chk10 detached at K | step `kstep` |
| mainmove-last | BASE sha | THE WORK step 1 |

## D-decisions (mine, overrule freely)
- D-1: no third verify at M before regenerating (the task asks regenerate then one plain; the gate already measured the regenerating run on 078e7b3d). The measured pair must equal main's pair at BASE plus (6, 0), else STOP; that replaces trusting 5887.
- D-2: model row C5 (merge-in), Sonnet; G2 gate already given by B1700 on the three lane paths.
- D-3: the browser assertion is excluded from the chain (CI runs it separately; the merge changes no browser-visible file, UNMEASURED).
- D-4: slot 8 chosen over 10-12, 14, 18 (all free; lowest).

## Q-questions for Tuesday
- Q-1: if main moves between the verify and the push, should the seat repeat once itself? Default: no; STOP and ask (verified pair belongs to the verified base).
- Q-2: the merge is not re-gated (diff to main stays the gated three paths, proved by program). Default: Tuesday checks `git diff --name-only origin/main <head>` at the PR.

## UNMEASURED
Whether the merge of 832bf2d9 or later (with #222) conflicts only in the counts file (the drafter may not run merge-tree or fetch; the gate measured it on 078e7b3d, and the seat aborts on any other shape). Whether #222 adds cells (the seat's pair rule decides). Time of each verify on this load. Node 24 and Linux. The browser assertion. The `core.sshCommand` of the lane clone works for a push (it did for the lane's own push; the drafter's ls-remote through the project's stale checkout printed a permission error, which is why the kit builds a fresh clone).

## Outside-the-fences disclosure
Read only: the two named kits and report forms, the gate VERDICT, commission and landing text, the B1691 chain tools (first 60 lines of five scripts), `model-routing.md` rows, `models_latest.json:23`, `brief_seat.sh:31`, `CLARIFICATIONS.md:2067`. One local `git ls-remote` through the project's own checkout (read verb) failed on a stale key path and printed no ref; no repository state changed. No decision-queue, Jira, mail or fleet/briefs_staged read. Scratch files only in the session scratchpad (a copy of main's counts file and verify script, a sidecar-filling script); a second stamp_check `--init` created the sidecar. The retired address, hosts and key values were not printed; no product file was opened.
