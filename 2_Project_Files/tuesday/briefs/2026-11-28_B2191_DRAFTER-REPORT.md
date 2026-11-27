STARTABLE: YES (four STOP-CLASS questions for the stamp, Q1 to Q4; Q1 is a change outside the commission's literal file list)

# B2191 DRAFTER REPORT: kit X99, OXPd lane AZ-1 round 2 (what-if NOISE re-draft of X98)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2191_SEAT-X99_oxpd2-az1-bicep-whatif-r2.md` (+ `.measured`, 165 claims, `stamp_check.py` exit 0, 0 TODO). Seat tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2191/seat-tools/`. Scratch and evidence: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2191/` (below `<d>`). Drafter clocks: first `date` 01:01:25 AEDT, last before this report 01:15 AEDT.

## BLUF
1. **The judge gained a closed NOISE list of six exact leaves (N1 to N6), copied from X98's saved answer, each matched on ALL seven fields** (type, name, path, change type, before, after). No pattern, no wildcard, no field-name rule. Every other leaf is judged as before (PROTECTED stays PROTECTED). A Modify row whose only non-NoEffect leaves are NOISE prints `PASS NOISE-ONLY`. A mutant's expected-row test now reads only the leaves that are not NOISE. Without that, `mRelayPublic` would always fail on N6 beside it.
2. **The real-data proof (MEASURED):** the revised judge over X98's saved `wi-green.out` printed `WHATIF wi-green green: PASS (declared NoChange 10, NoEffect-only 0, noise-only 3, noise leaves 6, expected rows 0, ignore listed 2)`. The unrevised judge over the same file printed X98's `FAIL 3` (the control). Green compiles to the same `main.json` X98 sent (`ba7a31d7...`). X99's green what-if therefore sends Azure the same template.
3. **`ipVersionType` joins NOISE (N1), and the template does not state it.** Evidence: stating it at the pinned endpoint API `2024-07-01` gives `Warning BCP037` under the pinned Bicep 0.48.1 (also at 2024-10-01 and 2025-01-01; none at 2025-03-01). A warning is a STOP, and an API move is outside D2 and this narrow revision. A client's deployment at that API sends nothing there (the answer's `after.properties` keys are `privateLinkServiceConnections` and `subnet` only), so the template already mirrors it.
4. **One forced change outside the commission's file list (Q1):** `az2189.py` fixes its lane as a constant (`.tools/b2189-x98`) and refuses any other lane (exit 4). With only `whatif2189.py` changed, X99 could not run in `.tools/b2191-x99`. I changed exactly two lines (the constant and the docstring line that names it). The `diff` shows `25c25`, `36c36` and nothing else; selftest 36 of 36. The other nine files are byte-equal (`cmp` rc 0, 9 of 9). `main.bicep` is unchanged.

## Facts re-measured (instrument, control)
- Origin (`gh api -X GET`, 01:06:43 and 01:13:30): main `0ee3b0913c539eb34ae16ca921a65307ff7fa343`, tree `fc101f81...`, parent `7d652c5f`; open PRs 0; `b2191` refs 0; `b2189` refs 0; `contents/deploy` 404 (control `contents/build` 5 entries).
- BASE hosted (`hosted3.py` over BASE's own run, 01:06:53): `HOSTED 0ee3b091...: PASS` at `--total 2445 --rules 739 ... --guard-linux 14 --guard-windows 15`. Control `--total 2446`: `FAIL 4`.
- BASE tree in `<d>/sim` from the tarball: `HEAD^{tree}` = `fc101f81...` (equal to origin), 739 files. With the two files staged: `checks2189.py` 7 of 7 PASS, 7 controls FIRED; `RULES: clean (741 files)`; `Ran 117 tests` OK; `WORDS: clean (2 files)` (words control 13 of 13); B-number count 0 and 0 (control: parameters file 1); gitleaks control rc 1, then the sim tree, the three neutral files, the two revised tools and the kit plus sidecar each rc 0.
- Builds (Bicep 0.48.1, sha256 `62cd5958...`, codesign verify rc 0, `--verbose=2` names Microsoft Corporation (UBF8T346G9); plain `-dv` gives 0 Authority lines, which is X98's DEVIATION 1, now written into the kit): green and the five mutants each `OK (0 warnings)`.
- `whatif2189.py --selftest`: 72 of 72 (52 old + 20 new). Eight one-line tool mutants each lower the count (`<d>/tool-mutants.txt`): noise off 63; name ignored 71; before ignored 71; change type ignored 71; other leaves ignored beside noise 69; type ignored 71; after ignored 71; path ignored 71. The first two drafts left four of these mutants alive (name, change type, type, after, path). I added a targeted check for each and re-ran until all eight fired. The earlier runs are kept in `<d>/_superseded/`.
- `az2189.py --selftest` 36 of 36; `list` over the new lane gives 14 entries (8 what-if, 6 read, 0 write), with `b2191-x99` 8 times and `b2189-x98` 0 times. `whatif2189.py list`: `LIST: 13 declared, 7 ignore, 6 noise, 5 mutants`.
- Machine (01:13:33): OXPd2 panes X93, X94, X96, X97 (no X98, no X99); no az process (pgrep rc 1; control tmux 750 lines); `<lane>` absent.

## D-decisions (all in the kit)
D8 NOISE list (seven-field exact match, six tuples, each beside its `wi-green-deltas.txt` line). D9 `ipVersionType` as N1. D10 the `az2189.py` lane lines. D1 to D7 are carried unchanged from kit B2189 (D2 also now says a NOISE line is never a DELTA to converge on). New REFUSE items: `<x98>/logs/wi-green.out` sha256 must still be `f899db44...`; there must be no X98 pane; there must be no `b2189/` or `b2191/` branch. The rebase rule is tightened: any move of `main` is `STOPPED: NEEDS TUESDAY` before the push, because four build lanes are live and their totals are unknown.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS): accept the two-line `az2189.py` lane change.** Default **a**, accept it. The alternatives are reusing X98's lane (forbidden by the commission) or a re-draft that makes the lane an argument.
- **Q2 (STOP-CLASS): the NOISE list matches on seven fields.** Default **a**. Alternative **b** is the commission's four-field tuple. Cost of b: a second, unknown private endpoint connection on the namespace would also read N6. The selftest has that look-alike, and the before-ignored mutant shows it is caught only by pinning `before`. Cost of a: an etag that Azure rewrites fails N2, so the run STOPs (R11; conservative).
- **Q3 (STOP-CLASS): `ipVersionType` is NOISE N1.** Default **a**. Alternative b: move the endpoint's API to 2025-03-01 or later in a later lane and state it.
- **Q4 (STOP-CLASS): convergence.** Default **a**, as X98's S4.
- **Q5: README sentence.** The README says "no resource reads `Create`, `Delete`, `Modify`, ...". The judge accepts NOEFFECT-ONLY (already in kit B2189) and now NOISE-ONLY `Modify`, so the sentence is stricter than the check. Default: leave it unchanged (the commission keeps the README byte-equal); the G1 gate may raise it. Alternative: a one-sentence README change in a re-draft.
- Q6 to Q11: carried from kit B2189's Q3 to Q9 with the same defaults (lane parameters; JSON not committed; one G1 gate on Opus, 120/100 minutes, pane X99; launch now; potentialChanges FAIL; what exists only).

## UNMEASURED
Azure's answer to X99's own what-if, including whether all six leaves come back identical (the etag especially). The five mutants' real answers (X98 never reached them). Whether what-if accepts `requiresClientAuthorization` as changeable (`mHcAuth`). The CI predicates are no longer unmeasured. I re-read `.github/workflows/ci.yml` at `0ee3b091` in `<d>/sim`: lines 4 to 7 run `push` on `main` and `'b[0-9]*/**'`, line 211 is `FLOOR=117`, line 218 runs `python3 -I build/repo_rules.py .`, and `deploy` appears 0 times. That matches kit B2189's read. Kit B2189's five old tool mutants were not re-run on the revised file.

## Chain inputs
See the kit's CHAIN INPUTS table. Every Step-1 input exists at drafting: `<src>`, `<src98>`, `<cli-src>`, and X98's `wi-green.out` and `.rc` (each MEASURED by `ls -d`, `shasum` or `cat`).

## Outside-the-fences disclosure
- **No az command was run.** No write in the OXPd project, Azure, GitHub, Jira, cards or mail. GitHub access was `gh api -X GET` only, under the OXPd `GH_CONFIG_DIR`: commits, pulls, refs, contents, the tarball, and `hosted3.py`'s run and log reads.
- Read-only reads outside the commission's named files:
  - `<project>/.tools/b2189-x98/logs/*` (by program and by the judge, which only reads).
  - Seat X90's saved `prov-network.out`, for the endpoint API versions the subscription offers.
  - Seat X92's STATUS (for the sidecar).
- I ran each seat tool's own `--selftest`. The two selftests create temp folders under `/var/folders`; that is the tools' own behaviour, the same as at B2189.
- I copied the Bicep CLI into `<d>/bicep` and ran it on `<d>` files only. It is the same binary B2189 ran.
- The scratch repository `<d>/sim` (no remote) holds one commit made with a synthetic `drafter@invalid.example` identity through env vars, as the B2189 drafter did. It is not a project repository.
- No deletes. Superseded mutant folders and an earlier sidecar were moved to `<d>/_superseded/`. The gitleaks control token was moved to `<d>/_quarantine/`.
- **One write outside the commission's file list:** the `az2189.py` two-line change (Q1).
