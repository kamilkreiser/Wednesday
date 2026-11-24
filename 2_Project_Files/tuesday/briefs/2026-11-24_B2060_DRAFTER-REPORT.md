STARTABLE: YES

# B2060 DRAFTER REPORT: OXPd 2 lane L4, ROUND 2 OF 2 (the fix round for gate B2059's NO GO), kit for seat X68

Read-only drafter (Opus, claude-opus-5-5) for Tuesday s324, drafted 2026-11-24 21:10:58 to about 21:36 AEDT (clock by `date`). Kit: `2026-11-24_B2060_SEAT-X68_oxpd2-l4-round2.md`; sidecar `.measured` (stamp_check.py: 142 claims, 142 measured, rc 0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s324/d2060/` (below `<d>`); seat tools `<d>/seat-tools/` (11 files).

## BLUF
- ONE change closes FOUND 1 and FOUND 2 in `BARE_BASE64_RUN`: a new `BARE_BASE64_JOIN` = `[ \t]*(?:\r?\n|\\r\\n|\\n)[ \t]*`, the run = line of 16+ base64, any number of JOIN + 16+, then at most one JOIN + 1 to 15; `BARE_BASE64_JOINER` also strips spaces and tabs. FOUND 3: one Limits sentence names every shape measured clean. The docstring's G2 sentence now says exactly what the pattern joins.
- Two NEW cases (`SHORT`: throwaway certificate at 67 columns, `der_run(289)` at 64 LF / 76 CR LF / 64 JSON backslash-n; `BLANK`: YAML 2-space, XML 4-space, tab, a space before each LF), both red first on HEAD1 by `AssertionError: 0 != 1` with all four rows clean. `FLOOR` 115 to 117. 16 mutants, 16 MATCH.
- MEASURED effect: every DER size 256 to 2048 bytes is seen in nine wrapped shapes (round 1: 19% to 25% clean unindented, 100% clean indented; the gate's 407 and 341 reproduced exactly). No false fire on the .NET shared framework or the gate's publish folders. Cost with a fingerprint listed rises from 0.23-0.37 s to 0.44-0.59 s on 32 MB of base64; unchanged with the empty list.
- The seat makes ONE fast-forward commit on HEAD1 `c16306ca`, pushes by sha to the same branch, never rebases. Main unmoved at drafting (89a10a1b, 21:11); B2053 not landed; its 9 paths touch neither `build/` nor `.github/`.

## FACTS RE-MEASURED (instrument; control)
1. Origin (gh api -X GET, project GH_CONFIG_DIR, 21:11 and 21:34): main `89a10a1ba26a16aae7996e059d548bf53531fd44`; `b2057/l4-release-guard-cert-forms` = `c16306caea94d73af099e7c5ef40a1f51627ec65`; `heads/b2060` 0 rows (control heads/b2057 1 row); open pull requests 0 (`pulls?state=open` length 0, 21:33); `b2053/l1-round2-found-1-3` = `105b3465` one commit on main; repo private true, push true.
2. HEAD1 push run: `hosted3.py c16306ca... --unit 115 --floor 115 ...` last line `HOSTED c16306caea94d73af099e7c5ef40a1f51627ec65: PASS` (`<d>/logs/hosted-head1.out`).
3. Frozen run, fresh `<d>/clone3` (`<d>/scratch/frozen_run.py`, `<d>/logs/frozen-clone3.out`): HEAD1 hashes equal kit B2057's "After both"; prior-work literals rc 1 x4, control rc 0; red `Ran 117`, `FAILED (failures=2)`, FAIL 2, ERROR 0, AssertionError 2, ok 115; green `Ran 117` `OK`; `MUTANTS: 16 of 16 MATCH, 16 of 16 undone equal`; `CHECKS-R2: 12 of 12 PASS` (vs HEAD1); round-1 `checks_l4.py` vs BASE `CHECKS: 10 of 10 PASS`; `WORDS: clean (2 files)` (control `CONTROL FIRED: 13 of 13`); `B2[0-9]{3}` 0 / 0 (control: commission 6); `RULES: clean (659 files)`; gitleaks 8.30.1 control rc 1 `leaks found: 1` (quarantined), clone3 rc 0, 8 neutral files rc 0.
4. Probe (`<d>/scratch/probe2.py`, logs `probe-rows.out`, `probe-sweep.out`, `probe-cost.out`, `probe-folders.out`): gate rows A0-A19 and C1-C4 re-run against round 2 / round 1 / pre-pass alternative; round 1 columns reproduce the gate's A and C results (control); new rows N1-N9 and quiet Q1-Q3.
5. Live kits reading the unit number (`grep -c -i -F`): B2053 `--unit 111` 4, `Ran 111` 3; B2056 `--unit 111` 5, `Ran 111` 3; neither reads 115 (control B2057 `--unit 115` 9). Gate B2059 `landing.txt` holds 115 on 12 lines.
6. Toolchain: dotnet `10.0.404`, gitleaks `8.30.1`, Python 3.14.10. Model line `models_latest.json:17` `claude-opus-5-5`; `<project>/CLAUDE.md:7` newest Opus; `brief_seat.sh:31` default opus.
7. Seat id X68 free: brief file names 0 hits (control X67 3); no pane; `.tools/b2060` absent (control b2057 present). Heavy lock folder absent at 21:27.

## WHAT I RAN, WHERE, AT WHAT LOAD
Python only (unit runs, mutants, probes, checks, repo_rules.py) in my scratch clones, no lock (not heavy). load1 1.6 to 4.9 across the session (`uptime` 21:14, 21:16, 21:17, 21:35). **No dotnet job, no heavy lock taken.** Read-only reads of `<project>/.tools/dotnet/shared/Microsoft.{NETCore,AspNetCore}.App/10.0.15` and gate B2059's `g2059/out/{linux,windows}` (the guard reading them in process). Git in the project checkout: none (clones from origin by `clone.py draft`; read verbs in my clones; write verbs only inside `<d>`).

## CHAIN INPUTS (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp S4 | Tuesday's stamp |
| 1 | `<d>/seat-tools` (11 files, hashes in kit); `<repo>` local values; origin HEAD1/BASE; HEAD1 push run | exist (MEASURED) |
| 2 | files at HEAD1 | Step 1 clone |
| 3 | `1-red-r2.diff`, clone at HEAD1 | Step 1 |
| 4 | `2-fix-r2.diff`, `mutants_l4r2.py`, red tree | Step 1, Step 3 |
| 5 | green tree, `heavy.py` | Step 4, Step 1 |
| 6 | staged tree, `checks_l4r2.py`, `checks_l4.py`, `words.py`, `commit-message-r2.txt` | Step 5, Step 1 |
| 7 | the commit, Step 7 (b)'s fetch, `run_step.py`, `hosted3.py` | Step 7 (a), Step 7 (b), Step 1 |

## D-DECISIONS (each a Question in the kit)
D1 fix in the pattern (Q1). D2 two new cases (Q2). D3 FLOOR 117. D4 named limits not built (Q4). D5 publishes-only chain, no rebase, no local CodeQL (Q5, Q7).

## QUESTIONS FOR TUESDAY (defaults already built into the kit)
- Q1 (STOP-CLASS) fix form: default a, JOIN with `[ \t]*` + one `{1,15}` last line, in the regex. Alt b pre-pass strip: same rows, about 2x the cost. Alt c drop the per-line minimum: not built.
- Q2 (STOP-CLASS) cells: default a, two new cases, FLOOR 117. Alt b fold rows into round 1's case, FLOOR stays 115.
- Q3 (STOP-CLASS) landing: default after B2053 (B2057's S4); later kits take `--unit 117 --floor 117`.
- Q4 named limits not built. Q5 publishes-only chain (alt: whole chain, about +10 min lock). Q6 commit subject (239 chars). Q7 no local CodeQL. Q8 Opus, READY +80, push +60, pane X68, gate G1 round 2 of 2.
- Extra for Tuesday (not in the kit's Q list): the commission routes a round-2 NO GO "to Kam"; the kit says "the product owner" (DRAFTER_RULES fence 7: no names in kit text).

## UNMEASURED / NEVER RUN
The two publishes of the round-2 tree (the drafter read the gate's HEAD1 publish folders; the dotnet inputs are identical files); `clone.py seat`; the commit, identity read, `run_step.py` neutral scan; the push and read-back; `hosted3.py` on a round-2 head (PREDICTED `--total 2153 --rules 659 --unit 117 --floor 117`, guards 14/15); any hosted leg; CodeQL; the hosted runner's Python version; alternative c of Q1.

## OBSERVATIONS
- `BARE_BASE64_JOINER` without the blank strip makes the indented case ERROR (`binascii.Error`), so it cannot be a MATCH row in the tool; named in the kit. A 20000-run fuzz of the round-2 rule raised nothing.
- A first frozen clone was set aside (`<d>/_quarantine/clone2-before-fromhex`): `words.py` counted `seat ids 2` because `b"\x30\x82"` in an added line reads as `x30`/`x82`; the helper now uses `bytes.fromhex("3082")` and the patches were re-exported before clone3.
- Round 1's `mutants_l4.py` cannot run on the round-2 tree (`mBareNoJoin` anchor gone); `mutants_l4r2.py` carries its 10 rows re-anchored plus 6 new.
- Card id behind the launch authority: `datasec-oxpd-after-kickoff-lanes-1124` (report only; the kit cites "the product owner's 2026-11-24 ruling").

## OUTSIDE THE FENCES: disclosure
Nothing written outside `<d>` and the three brief files. No write to OXPd (only read: CLAUDE.md, round-1 STATUS, `.tools` listing, `.tools/dotnet/shared` read in process). No Jira, no card store, no `decision_queue.sh`, no hosted host but `gh api -X GET` and `git clone` (draft clones, push URL invalid). No `cd`. Nothing deleted: one clone and the gitleaks control moved to `<d>/_quarantine/`. The heavy lock was never taken, and no other holder's files touched. Nothing to any human; nothing of another client.
