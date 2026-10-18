# Gate 25 kit — DRAFTER REPORT (2026-10-18, from 11:36:41 AEDT; read-only drafter, Opus 5.5)

**BLUF:** Kit drafted for **gate 25** (routing name `QA/NexusAI-gate25`, tags `qa-g25-*`). It is a TIER-1 re-gate AS MERGED: RD-761 on `c7ca0ed` (M761), RD-794 stacked on M761 (M794S), and RD-794 on `c7ca0ed` (M794M). That makes three verdict lines plus one ORDER line. `bash -n` is clean. `--check` passes every content guard (it ran with the two READY overrides) and stops only on your stamps. **The three merged trees rebuild exactly** in my scratch mirror: each is the mechanical merge plus the seat's counts blob, so no line of code was hand-written in any merge.

## Files
- Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate25-rd761-rd794-merged.md`
- Launcher: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate25.sh` (mode +x)
- This report.
- Scratch only (my session scratchpad, not the project): two clones (`g25clone-bare-unused.git`, `g25m.git`), the two READY bodies (`g25_ready761.txt`, `g25_ready794.txt`), and query scripts.

## Gate number
**25.** The last NexusAI routing line is `QA/NexusAI-gate24` (`inbox_routing.conf:227`), and no gate-25 file exists. I did not edit `inbox_routing.conf`.

## Stamps Tuesday owes (the launcher refuses until all are done)
1. **Copy both READY mails WHOLE into `briefs/`** as `2026-10-18_nexusai-rd761-merged-READY-mail.txt` and `2026-10-18_nexusai-rd794-merged-READY-mail.txt`. The bodies are byte-equal to my scratch copies. The RD-794 one equals your `rd794ready.txt`. Without these files the launcher refuses at guard 31, which names the missing path.
2. **T1-T9** `RULED:` slots: write "default" or the ruling. 9 slots.
3. **The SELF-CHECK line and the Self-check note**, last and by hand. Including the T-slots, that is 11 `@STAMP@` placeholders.
4. **The route line** `QA/NexusAI-gate25|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`.

## Launch command
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/NexusAI-gate25' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate25.sh'"
```
Pre-flight: `bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate25.sh' --check`

`--check` result at ~12:05, run with the overrides: guards `9 MODEL 40 6 7 8 18T 18 90 91 22 93 94 70 70N 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86` all pass. Details:
- ls-remote took 1 attempt. Main is `c7ca0ed`, and the heads are `7f1881e` and `cd171f9`.
- The seat's merge objects are present. Their trees, parents, counts, lockfile and patch-ids are as pinned.
- The negative-control seats are `78171` (Datasec/NexusAI-O) and `32287` (tuesday).
- The Laptop-DEV jest lock was held by `s101o-rd476-verify`, reported as a NOTE (FIFO).
- It then refused only on 31R (overrides), 32 (11 placeholders) and 40 (route).

## Open decisions for Tuesday (the T-slots that matter)
- **T1, the C-57 runner.** "Via the installed tool" cannot mean running it in place. It writes into `$ROOT/session-tools/`, and it runs `worktree add` in ROOT's repo and `rm -rf`/`worktree remove --force` on its own worktree path. It also needs the merged sha as a commit in ROOT's repo, and the gate's rebuilt merges live only in the gate's store.
  - Default (a) is a byte-identical COPY run with `C57_ROOT` set to the gate's own shim. The runner's own `rm -rf` is disclosed as the one H-33 exception, made a no-op by proving the path absent first.
  - It also waives H-28's 40-minute cap for its three holds. The seat measured about 66 minutes per invocation, so the brief plans 75.
  - Option (b) is the gate's own id-superset runner, with the installed tool's verdict lines RELAYED.
- **T2, RD-794's own nine missing ids.** C-215's three conditions are worded for main-side retitles only. RD-794's 9 are the mirror case: 8 renames by `c36005b`/`014c0cd`, plus W5 parked under C-130.
  - Default (a): they are accounted under C-133 plus gate 19's F3 table, and named as such, never as C-215.
  - Option (b): any B-side leftover is a STOP for you.
  - Your ANSWER-4 points to the ANSWER-3 conditions for RD-794, but read literally those conditions do not fit these 9.
- **T3, the network.** Default: `gh` READ, including the Actions variables listing, which the commission's item 6 needs. `npm audit` is NOT RUN; the brief argues the merged lockfile and package.json are byte-identical to main's instead. Option (b) allows one `npm audit` call.
- **T7, the order.** The gate measures both orders and rules on the evidence. The turn order stays yours.
- **T8.** Local server boots for the interaction probes, with a new **H-36 socket ledger**: a require-first preload that sees axios, fetch, https and the SDK.

## Key findings while drafting (all in the brief's WRONG list)
1. **Gate 24's clone mode (`git clone --no-local`) carries NEITHER head (MEASURED).** `7f1881e` is only under `refs/remotes/origin/…` and `cd171f9` only under `refs/remotes/t9-drive-2026-10-15/…`. A `--mirror` clone carries both. The seat's merges are in no clone at all. T6 therefore defaults to one `--mirror` store with `g25/*` refs.
2. **Tree rebuild (MEASURED in scratch).** Each merge-tree conflicts in the counts file only.
   - Substituting the seat's counts blob gives `fb8197a`, `e2bb3ac` and `64bebaa`, matching the pins exactly.
   - The counts blob carries an `_updated` timestamp, so no regeneration can reproduce it byte for byte. The tree proof is therefore built as "differs in the counts path only" plus the gate's own verify passing.
3. **The seat's claims verified (MEASURED).** Its patch-id claims hold for all four file/order pairs. Its gated-file tables hold (7/10 and 13/15). Lockfile `19477a9` with proxy-addr 2.0.8 is in all three trees. `#19`/`#20` (server.js :16606/:16815 on main) count 0 in both RD-794 trees, and `ollamaAdapter.js` is absent from both. `deploy-demo.yml` blob `953b2a2` is identical everywhere, and both of its jobs are gated on `vars.CI_DEPLOY_ENABLED == 'true'`.
4. **Real interaction surface (MEASURED).** RD-761 and main both touched `buildFullHealthDetails`: main moved `healthDetailsForCaller` into the new `services/healthProjection.js`. The two auto-merge, so row r2 probes the health surfaces.
   - Main added no caller of the Log Analytics client. The 121-line caller multiset is identical at all seven revisions. A text census can't rule out helper-wrapped or library-internal calls, though; that is r2's call graph plus the ledger.
5. **The order (MEASURED in scratch).**
   - Stacked lands two gated trees as fast-forwards: M761, then M794S.
   - Main-order lands M794M first, after which 36a0dc0 is no longer a fast-forward. RD-761 then needs a NEW merge. Its predicted tree `db852b2` equals M794S except for the counts file, so the final tree is the same either way. Main-order costs one unmeasured merge commit, a C-57 run, a new PR head on #58, and an extra intermediate main.
6. **No docker, no az.** Nothing in either head touches the image, and the Laptop-DEV lock base has no `queue-docker/`. So the kit drops all image legs and forbids `az` entirely. Gate 24 disclosed a stray `az version` call.

## Corrections to the commission
- **The load figure.** Your commission says "1-minute load below 8". The brief and the launcher quote your ANSWER-1 ("load1 below 8") as the authority and mark gate 24's 40 as superseded. This is consistent, not a correction.
- **"C-57 via the installed tool"** is not literally possible in place (T1 above). The kit runs a byte-identical copy under `C57_ROOT`.
- **"C-215's three conditions"** cover only the 4 main-side retitles. RD-794's 9 need T2.
- **Ruling (o)'s EXTENSION source** (gate 20's `answer-starvation.txt`) is on the unmounted T9. The launcher instead checks the words as carried in gate 24's brief and this brief.
- **Gate 19/20 reports** are on the T9 and unreadable. They are named NOT READ (L-B7). Their kits on this drive are referenced instead.
- **RD-761's range from 8853e36 is 17 commits including one merge** (`65bce88`, main into the branch). Gate 20's range `72ca5d3..7f1881e` is 7 linear commits. The PIN table uses 17 from the merge base.

## Holds I did not break
- In the NexusAI repo I used read verbs only, plus `patch-id` over diff output.
- No fetch, worktree, merge or `merge-tree --write-tree` ran there. Those ran only in my scratch clones.
- No az, docker, gh, npm, jest or lock ticket.
- No HTTP to any app host. The only network calls were AgentMail GETs and `git ls-remote`.
- No secret was printed. Nothing was written in the TUESDAY root, and nothing was deleted.
