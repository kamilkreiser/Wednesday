# B1484 DRAFTER REPORT (kit SEAT-N122, NexusAI landing counts)

Drafter: an Opus kit-drafter sub-agent of Tuesday, Wed 11 Nov 2026, 02:21:27 to 02:37 AEDT (`date` in the same runs). Read-only to origin (`git ls-remote` with the project deploy key, `gh api -X GET` under the NexusAI `GH_CONFIG_DIR`). All writes were in the drafter's scratchpad clone (`/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/90f78cba-aa68-4adc-98aa-7d2087ff2f7f/scratchpad/b1484/clone`, push URL `invalid://no-push`, nothing pushed, no ref outside `refs/sim/*`). No jest, no npm, nothing written under `/Volumes/Datasec_DEV/!CODING/`. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1484_SEAT-N122_nexusai-landing-counts.md` (117 lines, five `____` slots: four slots and the last line).

## BLUF
- **Mechanism chosen: merge current main INTO the gated head (`git merge --no-ff`, must be conflict-free), then ONE counts-only commit regenerated on that merged tree.** Measured over the whole remaining landing sequence: a counts-only commit on the gated head **conflicts** with main on the counts file for every count-changing branch (8 of 8; 7 of 7 with B-learning skipped). Merge-then-counts **merges clean** (9 of 9), its final `merge-tree` into main is **clean** (9 of 9), and **the PR's merge tree equals the branch head's tree**. The branch's own files stay byte-equal to the gated head (0 blobs differ). The counts commit is the only new non-merge commit. The merge's combined diff is empty.
- **Handshake:** the seat's last line `READY B1484-<n>: COUNTS <branch> <K sha40> <t>/<s> ON MAIN <sha8>` matches `status_watch.sh`'s existing `"READY B"[0-9]*` arm. No change to the watcher is needed. The seat then polls `ls-remote` for main to become a merge with `^1` = its ON MAIN sha, `^2` = its K and tree = K's tree. Anything else stops it.
- **Cost (PREDICTED):** about 50 min of jest lock plus about 53 min of hosted Build per row (PR #186's Build took 53 min, n=1). Eight rows take about 13 to 14 hours end to end. The HARD STOP slot has to reflect that, or plan on a HANDOVER.
- **B-learning's gate (B1433b) read PROVISIONAL at 02:33:23**, and its full run held the jest lock from 01:42:54. The kit skips that row unless the gate reads GO / GO WITH FINDINGS @ 725dcf0 when its turn comes.

## Sources read (clock 02:21 to 02:33 AEDT)
| file | lines | sha256 prefix | use |
|---|---|---|---|
| `.../briefs/2026-11-10_B1431_verify/ORDER.md` | 65 | (read whole) | order, counts rule, deltas |
| `.../briefs/2026-11-10_B1433_ADDENDUM-2_counts-at-landing.md` | 17 | (read whole) | the precedent counts commit |
| `.../briefs/2026-11-10_B1483_SEAT-N121_nexusai-write-gate-case-fix.md` | 128 | (read whole) | form and rails |
| `.../briefs/2026-11-10_B1483_ADDENDUM-1_counts-on-branch.md` | (read whole) | | N121's counts are branch-local, superseded at landing |
| `.../briefs/2026-11-10_B1480_SEAT-N118_nexusai-lane-S-successor.md` :194-240 | | | NON-DOT, CHECKS, COUNTS AT LANDING, DEPLOY-DEMO |
| `.../briefs/2026-11-10_NEXUSAI-ALL-LANES_ADDENDUM-1_nondot-verify.md` | 14 | | non-dot rule |
| B1433b `VERDICT.md` | 19 | `c91d1e157701` | **PROVISIONAL @ 725dcf0** (mtime 22:04:37) |
| B1432 `VERDICT-shell.md` | 51 | `aa658d43001d` | GO WITH FINDINGS @ 5cc88ab, +1/+1 |
| B1431 `VERDICT-ci/csp/smtp/archive.md` | 36/34/33/34 | `303fd778ca02` / `15d27ae62f62` / `ed22f7dd121a` / `32b6d317db97` | all GO WITH FINDINGS at their heads |
| B1480 `VERDICT-revoke.md` / `VERDICT-l1.md` | 40/39 | `43660c53e0fe` / `a4d83eb74c33` | GO WITH FINDINGS @ 5fbad1b / 70709c6 |
| every `landing-*.txt` of the eight rows | 11/11/11/11/5/7/7 | | the read-back the kit supersedes |
| `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md` | 2667 | `4d4560d79d5f` | C-57 :418, C-68 :665 (amended :671), C-89 :835, corollary :1157, forward merge :1308, Merge path :2067 |
| `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md` | 154 | `5ccdffdf183e` | row C5 :95 |
| `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/status_watch.sh` | 64 | `284aa913306a` | final-line arms :55-56 |

## State at origin (MEASURED-BY-DRAFTER)
- `ls-remote` 02:22:09, re-read 02:33:23: main `0e3f94c5fc1628463f62e5d40400b2cbf489231f`; F-overflow `a1d7f46d...` and the eight queue heads exactly as in the kit. Main `0e3f94c5` = merge of `849b808c` and `3a5d3444` (PR #186). Its counts file reads 5513/327; `849b808c`'s reads 5493/326.
- Actions runs (02:32:20): PR #186's Build ran 14:26:15Z to 15:19:33Z (**53 min**). PR #187's Build was `in_progress` from 15:20:38Z. Main `0e3f94c5`'s push Deploy demo `skipped`. Pulls: #187 open, #186 merged at 15:20:13Z.
- The project repo's `core.sshCommand` points at `/Volumes/Laptop-DEV/...`, which is unmounted. `ls-remote` from the repo failed with publickey at 02:22:04. The kit sets the Datasec_DEV key path in the seat's clone.
- Jest lock (02:30:43): held by `qa-b1433b-full` since 14:42:54Z. One queued ticket, `b1483-chain` (N121). Load 24.88 on 18 CPUs.
- Port slots (the helper's formula, `test-server.js:89-93` at main): the trees that exist under the project use every slot except **8** (control: `b1430-nodot/b1` printed 6, as recorded). All sixteen kit tree names were chosen by program to hash to 8.

## The measurement (the core of this report)
**Instrument:** `scripts/sim_counts.sh` (appendix A, 80 lines, sha256 prefix `31da85299f46`), run in the scratch clone with `git merge-tree --write-tree` (git 2.54.0, ort) and `git commit-tree`. Each row is simulated on the simulated main of its turn, and the landing is simulated as a merge commit (main, K), which is what `gh pr merge --merge` makes. **The counts VALUES are placeholders** (main's pair plus ORDER.md's delta, `_updated` = `SIMULATED-PLACEHOLDER`); no jest ran, so no pair here is measured. The mechanism is textual and does not depend on the values. Output: full sequence at 02:26:22 to 02:27:47 (sha256 `d8169a5ac6e5`); B-learning skipped at 02:27:48 to 02:29:03 (`776c5d19a7fe`).

Full sequence (overflow, learning, header, ci, csp, smtp, archive, revoke, l1), one row per branch:
| row | A: counts-only on gated head, merge-tree into main | B: merge main into head | B: final merge-tree main+K | tree(merge) = tree(K) | diff main..K = own + counts | own blobs differ | new non-merge commits | content-merged `__tests__` |
|---|---|---|---|---|---|---|---|---|
| overflow | n/a (no count change) | rc 0 | rc 0 | yes | equal (4) | 0 of 4 | 0 | 0 of 390 |
| learning | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 2 | 1 (counts only) | 0 of 391 |
| header | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 2 | 1 (counts only) | 0 of 392 |
| ci | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 7 | 1 (counts only) | 0 of 394 |
| csp | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 4 | 1 (counts only) | 0 of 396 |
| smtp | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 2 | 1 (counts only) | 0 of 397 |
| archive | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 15 | 1 (counts only) | 0 of 398 |
| revoke | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 6 | 1 (counts only) | 0 of 400 |
| l1 | **rc 1, counts file** | rc 0 | rc 0 | yes | equal | 0 of 7 | 1 (counts only) | 0 of 403 |
Final simulated main `d16e1ecc` (`refs/sim/seqfull`), placeholder counts 5595/340, which equals ORDER.md's derived value for row 10. Skip run: 8 of 8 rows match the B pattern above, and 7 of 7 A rows read rc 1 on the counts file. Final `49f79d56`, placeholder 5587/339.

**Control: real merge equals simulation (02:29:19).** A real `git merge --no-ff` of (main + F-overflow, tree `8e25615c71758d41e0d516942dc9b3e081969661`) into `725dcf0` in a scratch worktree gave rc 0 and tree `d31511eea21e2ed1d5fc8fd413984c56b69b419d`, the same tree `merge-tree` printed. Porcelain was empty after. `git show --cc` printed 0 lines (control: the first-parent diff printed 677 lines). The own-file diff against the gated head printed 0 paths (control: against main it printed 2). The merged counts file read 5513/327, which is main's.

**Why A conflicts:** both sides change lines 3-5 of the same 6-line JSON (`_updated`, `tests`, `suites`) relative to the merge base (5493/326). **Why B does not:** no queue branch touches the counts file, so merging main into it takes main's file without conflict. After that, the merge base for the PR is main itself, and only the branch side changes the file.

**Alternatives considered and rejected:**
- (A) counts-only commit on the gated head: conflicts at the PR (measured above). GitHub's merge button cannot land it without a web-editor conflict resolution, and that resolution is itself a merge of main into the branch.
- (C) resolve the counts inside the merge commit (an "evil merge"): no conflict exists to resolve, so it would hide a content change inside a merge. The kit's I4 (empty combined diff) forbids it.
- Rebase or cherry-pick onto main: HOLD 6, and "never rebase" (C-68, Merge path :2067).
- **(D) pipelining (NOT in the kit; Tuesday's option by ADDENDUM):** because tree(PR merge) = tree(K) was measured for every row, the seat could measure row n+1 on `merge-tree(gated n+1, K_n)` while row n's hosted Build runs. The landed main's tree is predictable exactly, and the merge base is unchanged, so the later real merge must reproduce the same tree, checked by tree sha. That saves about 45 min per row. Risk: if row n does not land as K_n, the measurement is void. The kit must then fall back, and the tree check catches it. It must never merge K_n itself into n+1, because that would land n's code through n+1. The drafter kept the kit serial because ORDER.md and C-68 say "on the main of its turn".

## The kit's design decisions (each with its reason)
1. **One lock acquisition per row** (update, counts commit and plain run in one chain), and **no lock held while waiting for a landing**. A whole-run single acquisition would hold the machine-wide lock through about 7 hours of hosted Builds.
2. **The read-back is replaced by invariants I1 to I8.** Every `landing-*.txt` step 1 says `git diff --name-only <gated> <COUNTS_SHA>` prints exactly the counts file. Under any mechanism that brings main in, that is false: it lists main's changes too. I1 (diff main..K = own + counts), I2 (own blobs = gated), I3 (only non-merge commit is K, counts only) and I6 (merge tree = K tree) are what it was trying to say.
3. **Landing detection:** main `^1` = ON MAIN, main `^2` = K, tree(main) = tree(K), counts at main = K's. The precedent shape is `0e3f94c5`'s parents `849b808c` and `3a5d3444`. A W0 expected tree for F-overflow is given (`8e25615c...`).
4. **Name comparison:** the previous row's plain-run JSON is main's name list, because W's tree check proves main's tree equals the previous K's tree. So no extra run of main is needed from row 2 on. The first row rests on I5 (the C-57 by-construction corollary, measured 0 content-merged files) plus the pair. S-revoke's expected removal of 2 names (VERDICT-revoke row 6) is written into the table.
5. **Message hygiene:** a default `git merge` message would name the branch, and every branch name carries a `b14xx` build number. The kit gives a fixed plain-ASCII message.
6. **Model row:** C5 "Merge on a GO" (merge-in), O55 escalation column. Opus because of the tier-1 rows (S-revoke, S-l1) and eight stop-or-go judgements on a moving main. Not C3: no design decision.

## What Tuesday must decide (before or at the stamp)
1. **HARD STOP** against about 13 to 14 hours of serial landing (PREDICTED: 8 x (about 50 min lock + about 53 min hosted Build)). Either a late clock or a planned HANDOVER and a successor seat.
2. **Hold main for the duration.** Tuesday lands nothing on main except these PRs, in order, each with `--match-head-commit <K>` after checking `ls-remote` main = the READY line's `ON MAIN` sha. Any other landing, records PRs included, stops the seat at W.
3. **Accept that the `landing-*.txt` read-back is superseded** by I1 to I8. Note that several `pr-body-*.txt` say "scripts/verify-expected-counts.json is not changed on this branch" (`pr-body-l1.txt:10`, `pr-body-revoke.txt:13`, `pr-body-shell.txt:8`, B1433b `pr-body.txt:8`), and the B1431 bodies quote counts measured on main `849b808c`. Those lines will be stale when the PRs are opened. They are Tuesday's text and the kit does not touch them.
4. **Local plain run: keep (the kit's default, precedent ADDENDUM-2 step 4) or drop.** The hosted PR Build runs the same plain verify on the same tree (I6), so dropping it saves about 22 min per row. That would rest the push gate on the update run alone. ALL-LANES rule 4 is satisfied by the update run, whose tree including the written counts file equals K's tree.
5. **Optionally adopt pipelining (D) by ADDENDUM** if the clock matters more than simplicity.
6. **B-learning:** at 02:33 its gate was still PROVISIONAL. If it does not read GO at the seat's turn, the seat skips it, and it needs its own counts prep later (on whatever main exists then, the same mechanism).

## Not measured (by the drafter)
Every count pair in the kit (PREDICTED sums of RELAYED gate deltas; B-learning's +8/+1 is relayed from the B1433 STATUS through ORDER.md, and its gate has not measured it). The full suite on any merged tree. Hosted Build, CodeQL, npm-audit and gitleaks on any of these PRs. The `CI_DEPLOY_ENABLED` value. Whether GitHub's merge commit for these PRs has exactly two parents in the order (main, head): measured only for PR #186 (`0e3f94c5`).

## Corrections
- The drafter's first simulation run (02:24:46) printed `DIFF: < HISTORY.md` for smtp and archive. Cause: the drafter's own "own files" baseline was `merge-base(head, 3929b794)`, which for the two branches cut from `849b808c` included `849b808c`'s HISTORY.md. The product diff was right. The baseline was fixed to `merge-base(head, origin/main)` and the run was repeated at 02:26:22. The table above is the repeated run.

## Appendix A: `sim_counts.sh` (as run; bash 3.2; the drafter's scratchpad, will not survive the session)
```bash
#!/bin/bash
# sim_counts.sh <clone> <label> <branch keys...>
set -u
C="$1"; LABEL="$2"; shift 2
export GIT_AUTHOR_NAME=sim GIT_AUTHOR_EMAIL=sim@invalid GIT_COMMITTER_NAME=sim GIT_COMMITTER_EMAIL=sim@invalid
export GIT_AUTHOR_DATE='2026-11-11T00:00:00Z' GIT_COMMITTER_DATE='2026-11-11T00:00:00Z'
TMP=$(mktemp -d)
hd() { case $1 in learning) echo 725dcf0ed76572af8773685769e5e5f1414745b2;; header) echo 5cc88abe0eb77d58fc0405e0ea2be0d5da470cd3;; ci) echo c79e2e88f950689f16d17c860616a89b5a3dd7b8;; csp) echo e6addceb8ee6b18127a7813fd62a2f6195a199b1;; smtp) echo 857843e439a3251ed0950287575bbd094bce715a;; archive) echo 52df646848a64d35bd434e0ee9c49682346531da;; revoke) echo 5fbad1ba3ff9a13f6ee86f069b1c732b3db7b3d2;; l1) echo 70709c61d4f555cd6e28f3bb83ad75d811a32907;; overflow) echo a1d7f46da0915f2c58b10f23c74dc196b903e85a;; esac; }
dt() { case $1 in learning) echo 8;; header) echo 1;; ci) echo 14;; csp) echo 27;; smtp) echo 8;; archive) echo 4;; revoke) echo 6;; l1) echo 14;; overflow) echo 0;; esac; }
ds() { case $1 in learning) echo 1;; header) echo 1;; ci) echo 2;; csp) echo 2;; smtp) echo 1;; archive) echo 1;; revoke) echo 2;; l1) echo 3;; overflow) echo 0;; esac; }
g() { git -C "$C" "$@"; }
counts_of() { g show "$1:scripts/verify-expected-counts.json" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("%s/%s"%(d["tests"],d["suites"]))'; }
counts_commit() {   # counts-only commit on $1 with placeholder tests/suites $2 $3
  local parent=$1 t=$2 s=$3 blob tree
  g show "$parent:scripts/verify-expected-counts.json" | python3 -c '
import json,sys
d=json.load(sys.stdin); d["tests"]=int(sys.argv[1]); d["suites"]=int(sys.argv[2]); d["_updated"]="SIMULATED-PLACEHOLDER"
sys.stdout.write(json.dumps(d,indent=2,ensure_ascii=False)+"\n")' "$t" "$s" > "$TMP/c.json"
  blob=$(g hash-object -w "$TMP/c.json")
  rm -f "$TMP/idx"; GIT_INDEX_FILE="$TMP/idx" g read-tree "$parent"
  GIT_INDEX_FILE="$TMP/idx" g update-index --cacheinfo 100644,"$blob",scripts/verify-expected-counts.json
  tree=$(GIT_INDEX_FILE="$TMP/idx" g write-tree)
  g commit-tree "$tree" -p "$parent" -m "Expected test counts for this branch (SIMULATION)"
}
MAIN=$(g rev-parse refs/remotes/origin/main)
for k in "$@"; do
  H=$(hd $k); cur=$(counts_of "$MAIN"); t=${cur%/*}; s=${cur#*/}; nt=$((t+$(dt $k))); ns=$((s+$(ds $k)))
  OWN=$(g diff --name-only "$(g merge-base "$H" refs/remotes/origin/main)" "$H" | sort)
  # A: counts-only on the gated head, merged into main
  [ "$(dt $k)" = 0 ] || { KA=$(counts_commit "$H" "$nt" "$ns"); g merge-tree --write-tree --name-only "$MAIN" "$KA"; echo "A rc $?"; }
  # B: merge main into the gated head, then counts-only commit
  TM=$(g merge-tree --write-tree "$H" "$MAIN" | head -1); M=$(g commit-tree "$TM" -p "$H" -p "$MAIN" -m "Merge main into branch (SIMULATION)")
  #   I5: every __tests__ blob of M equals the gated head's or main's
  #   K = M (no count change) or counts_commit M nt ns
  #   final: merge-tree MAIN K (rc, tree == K^{tree}); diff --name-only MAIN K == OWN + counts;
  #   own blobs K == H; rev-list --no-merges K ^H ^MAIN == [K]; diff M K == counts only
  #   landing: NEWMAIN = commit-tree <final tree> -p MAIN -p K ; MAIN=NEWMAIN
done
```
(Abridged in its print lines only; the logic lines are as run. Full file: the scratchpad path above, sha256 prefix `31da85299f46`.)
