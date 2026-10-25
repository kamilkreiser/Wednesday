# B577 DRAFTER REPORT (2026-10-24, Sonnet drafter, read-only; reads 11:25-11:50 AEDT per `date`)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B577_SEAT-M13_mps-105-fix-round-2.md` (98 lines; sha256 `a9d582a6c13a04d9cc2158a288d7777438f736d7ff11d1c530e64f4d1d1a316c`) and its `.pre-stamp` copy (`cp`, `cmp` rc 0, same sha256). Unstamped copy reads **8** lines with `/usr/bin/grep -c -E '_''_''_''_'` (slot lines 83-89, all ending in the slot, and the last line 98); control: a scratch file `a____b` reads 1; lines with the pattern not at line end: 0. Non-ASCII bytes 0 (`LC_ALL=C grep -c '[^ -~]'`). Nothing launched, committed, pushed or posted; only the three named files were written.

## Shape
Three commits on `4db8661d`, one Sonnet seat `Datasec/MPS-M13`, ports 9280-9289: (1) the product owner's words (B569 folded in: `sections.ts:385` constant to `'All device classes'`, one added literal-typed `it` in `dealPair.test.tsx`, red first); (2) B566-1 Major: one new Theory in `DealUsageCombinedPair.cs` pinning the colour-pages threshold (totals 1, 0.5, 0.01 pages), green at base by design, red under `> 1m`, `>= 1m`, `> 0.5m`, `> 0.01m`; (3) B566-6 Minor: `DealUsageColourRowTests.cs:290` floor `>= 20` back to `>= 100` (the gate measured 125; STOP if the seat reads under 100), killed by a generator mutant G1. B566-5 (dead helpers) LEFT: the round-cap statement asks no fix. B566-2 enforced as a seat-local NuGet home proven from `packageFolders`. B566-3/-4/-7 nothing.

## Reads (all read-only)
B566 STATUS (282 lines, whole: findings `:227-233`, round-cap `:247-253`, C4 mutant tables, FOR TUESDAY); B569 brief, `.pre-stamp` listed and DRAFTER-REPORT whole; B573 brief (whole, template shape) and its report; `Proposal.cs:505-560` (predicate `> 0m;` count 1), `DealUsageColourRowTests.cs:225-320` (floor line 290 count 1), `DealUsageCombinedPair.cs:1-260` (helpers, Facts, property), `sections.ts:374-392`, `dealPair.test.tsx` whole, `web/package.json`; B561 pre-stamp brief by grep (build/test/lint commands). `decision_queue.sh show mpscalc-pr105-device-class-cell-words-1024` (the one show): `ruled`, `choice='b'`, ruled_ts 08:53:16. Not touched: `decision_queue.sh list`, `fleet_ack.sh`, the scoreboard, `briefs_staged/`, Jira, any `.tools/b5*` contents, any write verb on the MPS repo.

## Partition program (`gh api -X GET pulls/<n>/files --paginate`, `comm -12` against the four Yours paths)
```
lane      n paths  shared with Yours
PR #102      21      0   (holds DealUsageNoCountedDevice.cs, a different file)
PR #104       7      0
PR #105      17      4   (self, by design)
PR #106       9      0   (head is now 4ef1adcb73ac, B573's push)
```
Control: a planted `web/src/proposal/template/sections.ts` in #104's list reads 1. **Shared with every other open PR: 0.** Live panes (`tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` 11:25): `tuesday`, `Datasec/MPS-G76`, `Datasec/MPS-M12`, `Datasec/HPSM-POC-H11`, `Datasec/HPSM-POC-H10`, `fleet-monitor`; G73 is gone (its verdict is the last line of its STATUS, `VERDICT:`); no `Datasec/MPS-M13`. Not-yours seats named in the brief from both sides: G76, M12, the #106 delta gate (B576).

## Pins, ports, slots, load
ls-remote 11:25:37: branch and `refs/pull/105/head` = `4db8661dad27fd2e8d79e0731d998dd1c0f03362`, merge `28899d9e...`, main `a5b4bbb5d377f29dd63bf0c64d54b44c122a6055`. `pulls/105`: `open false clean`, 6 commits, 17 files. Ports: `lsof -nP -iTCP:9280-9289` empty, rc 1 (no bind control by the drafter; the brief gives the seat one). Word-boundary scan `\b928[0-9]\b` over `briefs/2026-10-2[34]_*`: no file, rc 1; positive control `\b923[0-9]\b` lists the three B573 files. Heavy slots: only `heavy-slot-1` exists, holder `B574 11:23:36 mut-api` (read, untouched). Load averages 4.27 6.49 7.66 at 11:25. `.tools/b577` absent. `git status` of the project root not run by me (I wrote nothing there).

## Deviations and points for Tuesday
1. **Node 24 is not in the project's `.tools/`** (no node directory; `ls` of `.tools` read in full). The box has `/opt/homebrew/bin/node` v26.8.1; `web/package.json` engines `>=20.19.0`; CI runs 24.21.0; the B566 gate ran 26.8.1 and matched CI's counts. The brief tells the seat to record the version and say "node 24 NOT RUN" unless it finds one without opening another seat's tree.
2. **The words change is user-facing** (the deal-wide "Device class" cell prints `All device classes` in the one-pager and the full proposal usage table). The brief says so twice and suggests Tuesday may tier the delta gate 1. The longer cell's fit in a printed page is NOT TESTED by anyone.
3. Commit 2 is green at the base head by design (the code is right; there is no red-at-base for a test-strength fix); its proof is the mutants, said in the brief. Honest bound stated: a threshold in (0, 0.01) still survives.
4. Commit 2 depends on the API accepting fractional colour pages (the gate says it does, RELAYED); the brief orders a STOP if not. Commit 3 depends on the dropped counter reading at least 100 on both hosts (gate: 125); STOP if not.
5. The B569 brief is superseded and was never launched (`refs/heads/b569*` is a REFUSE condition so a stray launch cannot double up). Suggested hard stop 3.5 h, target READY 2.5 h after launch (three commits, a web `npm ci`, two mutant matrices, a whole CI line).
6. Not measured: no C#/TypeScript compiled, no test run; per-mutant red counts are not predicted numerically (the seat writes its own predictions first).
