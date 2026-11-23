STARTABLE: YES

# B1985 DRAFTER REPORT: OXPd_2 lane H, round 2 of 2 (the solution-line round), kit for seat X51

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1985_SEAT-X51_oxpd2-h-round2.md` (+ `.measured`, `stamp_check.py` rc 0, 136 of 136 claims; 8 `____` slots, last line `READ-WHOLE-BY-TUESDAY: ____`). Tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1985/seat-tools/` (10 files). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1985/`. Drafted 13:01 to 13:24 AEDT 2026-11-23 (`date`). Commission B1985 plus ADDENDUM-1 (the transport slnx line) and ADDENDUM-2 (main is `cad65b86`) folded in.

## BLUF
- Shape: ONE merge commit of main `cad65b865fc09b5e75b49d998ff61db594dd1569` into `b1974/h-host-composition-v0` (at `685d72b6`), then ONE fix commit of 5 paths (all M), then a fast-forward push. No product line changes.
- The merge: `merge-tree` rc 0, no conflict, tree `765182d5`. I made that merge with the kit's own command in `clone3`, and its tree matched.
- The fix (`3-round2.diff`, sha256 `67ba3062...`): two slnx lines (the Server test project, plus the Jobs transport project per ADDENDUM-1); cells H14 and H15 (two `Authorization` lines on each route are 401 in three shapes; a one-line 200 is the control) and `HostRig.RawPostAsync`, a raw TLS client pinned to the served certificate; Server README (the 403 sentence narrowed, the one-header-line rule, the `Kestrel.BadRequests` Debug limit); root `README.md:14-15`.
- MEASURED on the tree the seat will produce (`a17719c2`, the same tree in clone2 and clone3): Server executable 15/0; whole solution `total: 1919`, `failed: 0`, `succeeded: 1915`, `skipped: 4`, with 3 log lines naming the Server test assembly; the transport is built under `bin/Release`; `RULES: clean (598 files)`; `GUARD: clean (14 files)` / `(15 files)`; `CHECKS: 7 of 7 PASS, controls 6 of 6 FIRED`; `MUTANTS: 14 of 14 MATCH, 14 of 14 undone equal`, run twice. Both of round 1's survivors are now red: `mFirstOfTwoHeaders` on H14 and `mNtFirstOfTwoHeaders` on H15.
- PREDICTED hosted: `--total 1919 --rules 598 --skipped-linux 4 --skipped-windows 21 --guard-linux 14 --guard-windows 15` (windows succeeded 1898). The cells have never run on Linux or Windows. Both are a STOP if a leg goes red or skips.

## FACTS RE-MEASURED (instrument, control)
1. Origin by `gh api -X GET` at 13:21:19: main `cad65b86`, branch `685d72b6`, open PRs 0. `cad65b86` has one parent `e193fb63` and tree `97c8b349`.
2. Main `cad65b86` push run 45099054678, read with `hosted3.py --wait --total 1904 --rules 587`: PASS (linux 1900/4, windows 1883/21, guards 10/11). Previous main `e193fb63`: PASS at 1874/580. The control: the first read of e193 printed `FAIL 1` while windows was still in progress, and the read with `--wait` printed PASS.
3. Prototype A (`clone`, merge with e193fb63, one slnx line): 15/0; 1889/0/1885/4; rules 591; guards 14/15; unittest 111 OK; locks 31/31; checks 7/6; words clean (control 13 of 13); gitleaks control rc 1, then rc 0 on the neutral copies and the clone; neutral scan on a prototype COMMIT: 25 of 25, `not among them 0`, `no leaks found`.
4. Prototype B (`clone2`, a stand-in main with the same tree as cad65b86): 1919/0/1915/4; Transport built in Release; rules 598; guards 14/15; locks 32/32; checks 7/6 with 2 slnx lines; 15 `[Fact]` (column 1 0).
5. Prototype C (`clone3`, the real cad65b86): merge tree 765182d5; staged tree a17719c2, equal to B's (`write-tree` in both); checks 7/6; mutants 14/14 (13:16:18 to 13:20:05). The four lane files and the root README are blob-equal across A and C (sha256 of `ls-tree`/`ls-files` listings 98cc55..., equal). Between e193 and cad6, main changed no file under Adapters.Oxpd2, Secrets, Core, Server or Server.Tests, and no Directory/global/NuGet file (count 0; control: Jobs paths 7).
6. Second `apply --check` of the patch: rc 1, `error: patch failed: Datasec.Suite.slnx:8`.

## CHAIN INPUTS (every step's inputs exist at the start or come from an earlier step)
0 kit and stamp | 1 `<src>`, `<repo>` local values, origin (branch at 685d72b6, S2's main), S2's push run | 3 the clone on the branch, S2's sha, `merge-message.txt` (Step 1) | 2 the merged files (Step 3; anchors are checked before Step 4) | 4 `3-round2.diff`, `mutants_h2.py`, the restored merge (Steps 1, 3) | 5 the patched tree (Step 4) | 6 the staged tree, `checks_h2.py`, `words.py`, both messages (Steps 5, 1) | 7 the commit, the origin ref, `run_step.py`, `hosted3.py`. Step 2 runs after Step 3, and the kit says so.

## D-DECISIONS (the coordinator's defaults; none is the product owner's)
- D1: merge, then a fix commit; never rebase. D2: two slnx lines (Server.Tests after Secrets.Tests, line 33; Jobs.Transport after Jobs, line 11). Strict ordinal order would put `Jobs.Transport` before `Jobs/`. I chose the readable order, and nothing reads slnx order. D3: two cells and no product change. D4: README only, no host filter for Kestrel.BadRequests. D5: root README lines 14-15 only.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- Q1 merge, not rebase (default merge). Q2 both slnx lines (default both). Q3 H14/H15 as patched (default). Q4 no host-side log filter (default no; alternative: one `ServerHost.cs` line plus a cell and a mutant). Q5 root README lines 14-15 only; Opus; READY by Step 0 + 120 min, push by Step 0 + 90; pane X51; hard stop 18:30 (default).
- Not a slot question, but for the stamp: lane X1 round 2 (B1984) adds its own slnx line. Whichever lands second merges main again. An adjacent-line conflict there is a STOP (ADDENDUM-1).
- Landing texts: gate B1981's HELD `squash-body.txt` says "13 cells". It must be re-cut to 15 and re-scanned before the squash (the kit says so under FOR TUESDAY).

## UNMEASURED / NEVER RUN
- Every cell on Linux and Windows (PEM load, DPAPI-NG for H08, the raw TLS client of H14/H15). Whether the hosted logs name `Datasec.Suite.Server.Tests` (the kit makes this a positive control at least 1 per leg; locally 3 lines).
- `clone.py seat`; the merge and the commit under the repository identity; the push and its git output line; `ls-remote`, `cat-file -t` and `--is-ancestor` as written; `hosted3.py` on a round-2 head.
- Whether a code-registered logging filter beats a deployment's configuration (Q4 alternative). The framework's default level for the BadRequests category (the README claims nothing about it).
- The whole solution at the merge commit before the patch (1904 is DERIVED from main's push run plus a merge that adds no slnx line).

## OUTSIDE-THE-FENCES DISCLOSURE
- My two prototype commit sets (clone, clone2, clone3) were created with a placeholder identity `draft@invalid.example` (`commit-tree` with GIT_AUTHOR/COMMITTER env, `git -c user.*`, and in clone2 a stand-in "main" commit and merge). This was in scratch clones whose push URL is `invalid://no-push`, nothing was pushed, and the repository's identity was never used. The kit forbids every identity override for the seat.
- In my scratch clones I used write verbs (`switch`, `read-tree -u -m`, `reset --soft`, `merge`, `commit`, `apply`, `add`) and one `git fetch`, which failed (`Permission denied (publickey)`, because a draft clone has no key outside `clone.py`). I then made a third clone (`clone3`) with `clone.py draft` to get cad65b86. Nothing was written to `<repo>`, any `.tools/b*` folder or any project file. GitHub was read only (`gh api -X GET`, `hosted3.py`). There were no Jira calls, no messages, no device connections, and no reads of Source_Documents.
- Heavy jobs all went through `heavy.py` and `wave1-heavy.lock.d`, one at a time, and I never broke another holder's lock. The two mutant runs and two `hosted3.py --wait` reads ran as background shell calls, one process each, and I waited for each to finish. The lock was absent at 13:23.
- Quarantined, not deleted: `_quarantine/gl-control` (the scanner control) and `_quarantine/3-round2-e193-only.diff` (the one-slnx-line patch superseded by ADDENDUM-2). The shipped patch is the former `3-round2-ip.diff`, renamed to `3-round2.diff` with the same bytes (sha256 67ba3062...).
- Card ids and names: none in the kit. The scan was underscore-aware, and its control fired 9 of 9.
