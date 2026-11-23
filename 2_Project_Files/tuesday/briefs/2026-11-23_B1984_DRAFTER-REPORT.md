STARTABLE: YES

# B1984 DRAFTER REPORT: OXPd_2 lane X1, fix round (round 2 of 2), kit for seat X50

Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1984_SEAT-X50_oxpd2-x1-round2.md` + `.measured` (151 claims, `stamp_check.py <kit>` rc 0; 8 unfilled stamp slots, last line `READ-WHOLE-BY-TUESDAY: ____`). Tools `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1984/seat-tools/` (11 files). Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1984/`. Drafted 12:46 to 13:25 AEDT (clocks by `date`), with ADDENDUM-1 (13:00) and ADDENDUM-2 (13:14) folded in. The kit now merges main `cad65b86` (PR 35, lane IP). Origin was re-read at 13:24: main is `cad65b86` and the branch is still `1fca08cf`.

## BLUF
- All four FOUNDs are fixed in a prototype and each one is pinned by a cell and a mutant. FOUND 1: a depth bound of 64 is checked during a first `XmlReader` pass, before `XDocument.Load`, and `Mask` has its own bound. FOUND 2: each run of adjacent text and CDATA is joined and then scrubbed, and a `Holds` check over the serialised and joined forms refuses names, namespaces and splits across a child element. FOUND 3: the client sends WS-Addressing 1.0, and the stub reads that namespace from the bindings' `EndpointReference` elements. FOUND 4: the options refuse a time-out unless it is positive, finite and at most 5 minutes. The fault code is now scrubbed before it is cut.
- The prototype was run in a fresh clone (`clone4`) in the order the seat will follow. Merge of main `cad65b86`: `merge-tree` rc 0, tree `d579d9d9`, 617 files. Red: 21 cells, 10 failed (C07 K01 K03 K04 K07 K09 K10 K12 K13 K14), each by an assertion. Green: 21 / 0. Mutants: `MUTANTS: 24 of 24 MATCH, 24 of 24 undone equal`. Whole solution with the two slnx lines: `total: 1925` (main's 1904 + 21), `failed: 0`, `succeeded: 1921`, `skipped: 4`. Also `RULES: clean (617 files)`, `Ran 111 tests`, gitleaks clean, `WORDS: clean (3 files)`. The same steps at the superseded `e193fb63` (`clone3`) also passed: 1895, 610 files, 24 of 24 mutants.
- ADDENDUM-1 is the kit's default (Q1, STOP-CLASS), now with ADDENDUM-2's sha: one merge commit of main `cad65b86`, then one fix commit holding three frozen patches. The slnx lines are in the fix commit. The push is a fast-forward of `b1976/x1-oxpd1-read-client`. There is no rebase, amend or force-push.
- One part of the commission cannot be built as written. The path prefix `/hp/device/webservices/OXPd/` appears in none of the 17 committed files (all 17 print 0; control `Oxpd1Read.cs` 2). So the stub keeps its own hand-written prefix. K01 now checks the prefix by ordinal comparison, and mutant `mPathPrefix` reddens C06 and K01. This is Q2.

## FACTS RE-MEASURED (instrument, control)
- Origin, by `gh api -X GET` at 13:13: the branch is ONE row at `1fca08cf`; main is `e193fb63`; `[true,true]`. Main moved twice while I was drafting: `126c95e8` (PR 33, lane TA, 11 files) and then `e193fb63` (PR 34, lane L1, slnx and Lab). Neither touches the three lane folders: `git diff --quiet da8d64a8 origin/main -- <three folders>` rc 0, control `-- src/Datasec.Suite.Adapters.Oxpd2` rc 1. One PR was open at 12:56 (PR 34, since landed).
- Main's hosted runs, by `hosted2.py`:
  - `e193fb63` (superseded): run 45097688311, 1874, rules 580, PASS.
  - `cad65b86` (MAIN): run 45099054678, `total: 1904` on both legs, linux succeeded 1900 / skipped 4, windows succeeded 1883 / skipped 21, `RULES: clean (587 files)`, `PASS`. This matches ADDENDUM-2's 1904 / 1900 / 1883 / 587.
- `compare/e193fb63...cad65b86` lists 10 files (Jobs.Transport, Jobs README, Jobs tests) and none under the slnx or the lane's folders. `5-slnx.diff` still applies, and the slnx sha256 is the same `c3a0ec1c`.
- WS-Addressing use, by `nsuse.py`, counting declarations against elements and attributes actually used:
  - 2004/08: declared in 4 bindings + 4 port types, used 0 times.
  - 2005/08: 8 elements in the bindings.
  - wsaw 2006/05: 60 attributes in the port types.
  - This matches the gate's counts.
- Schema depth, by `xsddepth.py`: at most 5 levels below a Result. A Result sits at depth 3, so the deepest legal element is at depth 8. That is why the bound is 64.
- Callers and sinks, by `callers.py` (control `XDocument.Load(` 1):
  - `Parse` 1, `Mask` 2 (plus its own recursion 1), `Holds` 2, `Scrub` 3.
  - Record sink 1, result constructions 14, `throw new` 7, `timeout.Token` 2.
- Toolchain: dotnet `10.0.404`, gitleaks `8.30.1`. Lock files: 32 tracked, unchanged after the `--locked-mode` solution restore (0 lines). `.tools/b1984` is absent.

## CHAIN INPUTS
| Step | Inputs | From |
|---|---|---|
| 0 | kit, stamp | Tuesday |
| 1 | `seat-tools/`, the checkout's local values, origin (HEAD1, main), main's run | exists / GitHub |
| 2 merge | clone at HEAD1, `origin/main`, `merge-message.txt` | Step 1 |
| 3 red | merge commit, `3-red.diff`, package cache | Steps 1-2, `.tools/nuget-packages` |
| 4 green + mutants | `4-fix.diff`, `mutants_x2.py`, red build | Steps 1, 3 |
| 5 slnx + solution | `5-slnx.diff`, green tree | Steps 1, 4 |
| 6 checks | staged tree, `words.py`, both messages | Steps 1, 5 |
| 7 commit / push / hosted | fix commit, `run_step.py`, `hosted2.py` | Steps 1, 7a |

## STOP-SEVERITY CHECKS RUN ON THE PROTOTYPE
These were run in `d1984/clone3`. For each: whether it passed, and whether its control fired.
- **Merge-tree:** passed, rc 0 with one line.
- **Red set:** passed, 10 of 21 by assertion.
- **Green:** passed, 21 / 0.
- **Mutants:** passed, 24 of 24. Control: 23 rows reddened their cells; the named survivor `mDtd` read NONE as expected.
- **Owned-paths check:** passed. Control: the planted row counted 1, on both sides.
- **ASCII:** passed. Control: 1.
- **gitleaks:** passed. Control `leaks found: 1`, then moved to `_quarantine/gl-control`.
- **words:** passed. The first run hit once and was fixed; the control printed `CONTROL FIRED: 13 of 13`.
- **Whole solution:** passed, 1925 / 0. The build gives 33 outputs, because `Jobs.Transport` is built as a reference of the Jobs tests and is not in the slnx.
- **repo_rules:** passed, 617.
- The fresh run at `cad65b86` (`clone4`) repeated every one of these: red 10 / 21, green, `mutants-run4.log` 24 of 24, `checks2-c4.txt`, `gl-clone4.log` rc 0.

Never run on a real output of this round, and marked so in the kit:
- the merge commit and the fix commit (I have no git identity, and I did not override one);
- `run_step.py`'s neutral scan;
- the push;
- `hosted2.py` on the new head;
- the 21 cells on Linux or Windows.

## D-DECISIONS (each the coordinator's default, written in the kit)
- **D1:** depth bound 64, in `Parse` and in `Mask`.
- **D2:** join the text, scrub it, then `Holds` gives `MalformedAnswer`. The fault code is scrubbed before it is cut. K12 rows A1–A18: the gate measured A1–A13 and had no A8, so none was invented; A14–A18 are new.
- **D3:** WS-Addressing 1.0, with the stub reading the namespace from the bindings. The path prefix cannot come from the bindings (stated as a Limit).
- **D4:** time-out cap of 5 minutes, enforced by the options.
- **D5:** one merge commit plus one fix commit (ADDENDUM-1).
- **D6:** INFO items not built.

## FINDINGS OF THE PROTOTYPE
- **The stub's ASP.NET route matches the prefix case-insensitively.** Mutant `mPathPrefix` (`OXPD` in capitals) first reddened C06 alone (`mutants-run1.log`). This means that at HEAD1, a case drift in the library's prefix was invisible to every K cell. Fixed in this round by K01's ordinal `StartsWith`.
- **Four mutant expectations differed on the first run and were corrected to what it printed:** `mProxy`, `mWsaAction` and `mWsa2004` also redden K13, and `mPathPrefix` (see above). No code changed after the fresh run, which matched 24 of 24.
- **K12's red at the red step comes from the addressing break first.** FOUND 2 is proved by four single-part mutants (`mJoinOff`, `mLeakCheckOff`, `mTreeLeakCheckOff`, `mCutFirst`), each red on K12 alone.

## Q-QUESTIONS FOR TUESDAY (default first)
- **Q1 (STOP-CLASS), the commit shape:** (a) merge `cad65b86`, then one fix commit with the slnx lines (ADDENDUM-1 and 2); (b) the slnx lines as a third commit; (c) no merge and no slnx this round.
- **Q2, the path prefix:** accept it as a Limit, pinned by K01's ordinal check and `mPathPrefix`. The alternative is a lane-owned text under `contracts/oxpd1/`, but the commission holds that folder unchanged.
- **Q3, the time-out cap:** 5 minutes.
- **Q4, the depth bound:** 64.
- **Q5, the landing hold:** kit B1976 Q3's hold ends, because this head carries the solution lines. The lane can land after a round-2 GO plus green checks and CodeQL.
- **Q6, seat settings:** Opus, READY at Step 0 + 110 min, push by Step 0 + 80 min, pane X50, hard stop 18:30.

## UNMEASURED
- **Lane H round 2 (B1985) also edits `Datasec.Suite.slnx`.** If H lands before the seat's Step 2, main touches the slnx. The kit makes that a STOP, and `5-slnx.diff` would need re-issuing. If H lands after, H's own merge carries the slnx merge (ADDENDUM-2).
- The 21 cells on Linux and Windows. K13 is new there: the deep bodies are 420 kB.
- The live pane list: `tmux list-panes` printed nothing, and its control also read 0.
- Device behaviour with WS-Addressing 1.0 and `mustUnderstand`.
- Whether CodeQL's C# build is not vacuous now that the lane is in the solution.
- The windows skip count for the new head (21 is DERIVED: no lane cell skips).

## OUTSIDE THE FENCES (disclosure)
- I wrote only these two files and their sidecar. All scratch is under `fleet/state/s316/d1984/` (three scratch clones, logs, `seat-tools/`). The initial `--init` sidecar was moved to `d1984/_quarantine/sidecar-init.measured`, not deleted.
- **Git verbs that write, used only in my own draft clones** (push URL `invalid://no-push`, never the project repo): `switch -c`, `read-tree -m -u`, `apply`, `add`, and one `sed -i` on the README in `d1984/clone`. `merge --no-ff --no-commit` failed for lack of an identity; I did not set one.
- Three hook refusals, none worked around: a recursive grep over `fleet/state` (I re-scoped it), a `$VAR`-path git write (re-run with absolute paths), and a `..` copy (re-run with absolute paths).
- All 47 dotnet jobs went through `heavy.py` and the shared lock, one at a time. Lock waits were 0 to 3 per job, and no other holder's lock was touched.
- Reads only: `gh api -X GET`; `hosted2.py` on main.
- Not done: no Jira, no NAS, no `Source_Documents`, no device, nothing to any person.
- I read gate B1980's probe file `G1980Probe-final.cs` (scratch) to copy the A shapes' bodies.
