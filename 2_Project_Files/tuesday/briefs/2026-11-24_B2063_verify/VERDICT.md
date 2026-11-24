GATE B2063: GO WITH FINDINGS @ 0ca131e on main f5882ed

Gate G1 (a CI and security control: the release guard decides what may ship; the change touches `.github/workflows/ci.yml`
and `build/`), ROUND 2 OF 2 of lane L4, one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane L4, kit
B2060 (seat X68; stamp S4: Q1 "a" the fix in the pattern, Q2 "a" two new cases and FLOOR 117, Q3 after B2053 (landed),
each in words, every one the coordinator's, none the product owner's), on round 1's kit B2057 and gate B2059 (NO GO).
Head `0ca131eb477f2fff5e6f9b3f79e3ef32846bb296` on `b2057/l4-release-guard-cert-forms` = HEAD1 `c16306ca` + ONE commit
(parent c16306ca; c16306ca's parent 89a10a1b; no rebase). Main `f5882ed74275200ffd37ac998ee650ada0820241` (PR 48) did NOT
move during the gate (gh api -X GET about 21:52 and 22:05; open pull requests 0; the branch still 0ca131eb at 22:05).
Read and measured 2026-11-24 about 21:50 to 22:12 AEDT in my scratch `fleet/state/s324/g2063/`: `clone` (clone.py draft:
push URL `invalid://no-push`, no identity; detached at the head), worktrees `red` (c16306ca + `1-red-r2.diff`) and
`merge` (f5882ed7 with the merge-tree's tree read in; no commit made). Six heavy jobs through the kit's `heavy.py`
(sha256 31adedc8...) and the wave lock, one at a time, lock waits 0 each; the six released lock folders are mine, in
`g2063/_quarantine/locks/`; no other holder's lock or file touched; the lock absent at 22:05.

**BLUF.** Round 2 closes both blockers of round 1 and the docstring is now true. The head is HEAD1 plus the two frozen
patches byte for byte; the eleven tools equal THE TOOLS' sha256 (mine and the seat's copy, 11 of 11 each); red first
exactly the two new cases by `AssertionError` on HEAD1; head `Ran 117 tests`, `OK`; `MUTANTS: 16 of 16 MATCH, 16 of 16
undone equal` (my run of the frozen tool); `CHECKS-R2: 12 of 12 PASS`, `CHECKS: 10 of 10 PASS`. **Gate B2059's probe
re-run against the head: every SEEN row still SEEN, A2 to A5, A19, C2, C3 now SEEN, every named limit still clean as
the docstring says; its size sweep (every DER size 256 to 2048 bytes) reads 0 clean in all nine shapes (round 1: 341 to
1793 clean per shape), and in seven more shapes of my own and 388 larger sizes up to 16 KB, 0 clean.** No false fire:
the .NET shared framework folders and four publish folders (B2059's, the seat's, mine of the squash tree) read the same
lines under round 1 and round 2, list empty and with a fingerprint listed. The SQUASH with main f5882ed7 builds clean:
`total: 2171`, `failed: 0`, `Ran 117 tests` OK, `RULES: clean (659 files)`, `GUARD: clean (14 files)` / `(15 files)` (the
commission's PREDICTED numbers, now MEASURED). One Minor gap remains in the Limits text (FOUND 1: a JSON-escaped tab
beside an escaped line end is neither seen nor named). It does not block.

## FOUND

1. **Minor, does NOT block (a JSON-escaped tab beside an escaped line end is not seen and not named).** The JOIN
   (`release_guard.py:81` `[ \t]*(?:\r?\n|\\r\\n|\\n)[ \t]*`) takes the JSON escapes `\n` and `\r\n` as line ends and
   real spaces and tabs around them, but not the JSON escape `\t`. A tab-indented XML or YAML text stored in a JSON
   string (`"...\n\t\tMIIC...\n\t\t..."`) therefore splits into one run per line, each under 128. MEASURED (the probe,
   `logs/probe-extra.out`, `logs/probe-rows.out` E5): `64 JSON \n\t` 1793 of 1793 sizes clean, `76 JSON \r\n\t\t` 1793 of
   1793 clean; E5 (the throwaway certificate) clean at round 2, round 1 and BASE (not a regression). The G2 sentence says
   "with any spaces or tabs before or after each line end", which literally means the characters (it names the escapes
   "the characters backslash n" separately), and the Limits sentence does not name this shape: a records reader could take
   the escaped form as covered. Plausibility: second-order (a tab-indented certificate document embedded in JSON),
   dormant while the list is empty. Grade Minor, like gate B2059 FOUND 3. Fix, later and only if the coordinator wants
   it: one Limits clause, or `\\t` beside `[ \t]` in the JOIN with a row and a mutant. Carried in pr-body.md "Still open"
   and FOR-RECORDS.md.

2. **Info (other unnamed clean shapes, each rare or already covered by a named limit).** MEASURED clean at round 2,
   round 1 and BASE: a no-break space (UTF-8 `C2 A0`) as indentation (E6; not a space or tab: unnamed, rare); CR CR LF
   (E7) and a backslash-newline shell continuation (E23), both under "any other line end"; a first line under 16
   characters, an XML tag glued to a 10-character first piece (E8), under "a line shorter than 16 base64 characters
   before its last line"; width 15 (E12) and an empty line inside the run (E24), as named.

3. **Info (cost: acceptable, linear).** MEASURED in process (`logs/probe-cost.out`, load1 about 1 to 2.5): list empty,
   BASE = round 1 = round 2 (32 MB base64 text 0.02 s, 24 MB binary 0.11 s). One fingerprint listed, BASE / round 1 /
   round 2: 32 MB one line 0.04 / 0.32 / 0.43 s; 76-col CR LF 0.04 / 0.43 / 0.51 s; 4-space indented 0.05 / 0.23 / 0.59 s;
   24 MB binary 0.14 / 0.30 / 0.30 s; adversarial `30 82 ff ff` frames as base64 0.00 / 0.99 / 0.99 s (unchanged, gate
   B2059 FOUND 6); three adversarial blank shapes aimed at the new `[ \t]*` (16 letters + 100 000 blanks, x80; 16/15
   letter lines x470 000; blanks-LF-blanks x400 000) 0.19 / 0.30 / 0.18 s at round 2 against 0.05 / 0.22 / 0.09 s at
   round 1: no super-linear growth. Each repetition of the run is split by a JOIN that must hold a CR, LF or backslash
   (outside the line class), so the split is unique.

4. **Info (the tests).** The two new cases are the only test change (check 8: 0 test lines removed; check 11: the 41
   HEAD1 methods byte-equal); each asserts all four rows SEEN by name and quiet with another fingerprint; the short-tail
   case pins its tails `[1, 2, 6]` so a row cannot drift to a full last line. `der_run` builds bytes from SHA-256 of
   counters (no certificate of anyone). Not a mutant row (the kit says so): `BARE_BASE64_JOINER` without the blank
   removal turns BLANK into an ERROR, not a FAIL; the removal is held by that ERROR. I did not re-run that variant.

5. **Info (coupling and order).** The `rules` job's lines move 111 to 117 at this landing (115 was never on main). Lane
   L3 (b2056, its round 2 being drafted) adds no file under `build/` or `.github/` (MEASURED on its round-1 head
   4b9814f1: 13 paths; three-way merge-tree with this squash tree rc 0, tree 84b988fe); whichever of the two lands second
   takes the first's numbers (landing.txt MAIN MOVES).

6. **Info (process, the seat's own DEVIATIONS 3).** The seat named a no-op `cd` inside a subshell in its Step 1 (no file
   or directory changed; the tool hashes re-done by program: I re-measured them, 11 of 11 equal in its `.tools/b2060/gate`).
   Not a code matter. I made the same slip once (see OUTSIDE THE FENCES below).

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- `<HEAD1>..<head>` read whole (`logs/tree_check.out`): three `M` rows, numstat 1/1, 15/9, 46/0; against BASE three `M`,
  1/1, 44/7, 134/0; file sha256 at HEAD1 and the head = THE CODE's columns (ci.yml `567a3a74...`, guard `f2888169...` 311
  lines, test file `c383b8cf...` 585 lines); the commit message equals `commit-message-r2.txt` (297 bytes, subject 239).
- The two patches against THE TOOLS: sha256 `b4b14ecf...` and `0fb39969...`, equal; temporary index `read-tree c16306ca`,
  `apply --cached` both, `write-tree` `54fb6f6e` = `0ca131eb^{tree}` (EQUAL); red tree `ca9e3ebf`.
- Red first (`g2063/red`, `logs/red-unit.log`): `Ran 117 tests`, `FAILED (failures=2)`, 0 errors, exactly
  `test_g2_indented_or_blank_padded_wrapped_base64_fires` and `test_g2_wrapped_base64_whose_last_line_is_short_fires`,
  each `AssertionError: 0 != 1 : ['GUARD: clean (4 files)']` (all four rows clean on HEAD1); 115 `ok`. Head
  (`logs/head-unit.log`): `Ran 117 tests`, `OK`.
- Mutants (`logs/mutants.out`): 16 rows, each `Ran 117`, `ERROR 0`, red exactly its listed cases, `MATCH`, `undone equal
  True`; porcelain 0 lines after.
- Any wrapped or indented listed certificate still clean outside the named limits: only FOUND 1 (escaped tab), and the
  Info shapes of FOUND 2. False fires: none (FOLDERS below). Cost: FOUND 3.
- Every docstring sentence against the code: G2 "a bare, line-wrapped or indented base64 file; lines joined by CR LF, LF
  or the characters backslash n or backslash r backslash n, with any spaces or tabs before or after each line end" =
  `:81`; "every line but the last at least 16 base64 characters long, the last at least 1" = `:82`-`:83`; "a run of at
  least 128" = `:85`, `:165`; "four alignments" = `:167`-`:171`; "while the list holds a fingerprint" = `:161`-`:162`.
  Limits: each named shape MEASURED clean as stated (A6, A7, A8, A9, A10, A11, A16, A18, E12, E24). The round-1 sentence
  Tuesday withdrew ("a bare or line-wrapped base64 file") is gone (`grep -c -i -F` 0 at the head, 1 at HEAD1); its
  replacement is true for every size and shape measured.
- The two new cases and nothing else of a round-1 or landed case: CHECKS-R2 checks 6, 8, 11 (cases 117, new 2; 0 lines
  removed; 41 methods byte-equal); the helpers `wrap` and `der_run` are new names.
- `ci.yml` against main f5882ed7 (on the squash tree): exactly `-          FLOOR=111` / `+          FLOOR=117`; no other
  line; no job fingerprint moved (`test_pipeline_controls.py` green in the head and merge runs).

## FRAME (stamp checklist item 11: each every/never/only sentence the change adds, three shapes outside the tested one)

| Sentence | Shapes outside the tested ones | Result |
|---|---|---|
| "every line but the last at least 16 ..., the last at least 1" | a last line of padding only (66, 70 LF, 74 CR LF: 16 to 18 sizes each); width exactly 16 (E11; sweep 0 clean); a last line of 1 character with indent (E1) | covered |
| "with any spaces or tabs before or after each line end" | tab before CR LF (E22, E4); blank on both sides + CR LF (E2); trailing blank + indent (extra sweep 0 clean); 6-space at 100 columns | covered; **escaped tab FOUND 1**; NBSP Info |
| "lines joined by ... backslash n or backslash r backslash n" | with 2 spaces after (E3, sweep 0 clean); with a tab before, width 67 (E4); `\r\n` at 64 (sweep 0 clean) | covered; `\n\t` FOUND 1 |
| "a bare, line-wrapped or indented base64 file" (the form list) | YAML plain scalar with the first line after the key (E10); XML first line inline after the tag (E9); a 16+ letter line glued before the run (E21); unpadded run with a YAML key line glued after (E13, E14) | covered |
| (P2 in containers) | UTF-16LE file (E16); ZIP member, tab + CR LF (E17); chain files both orders (E18 to E20) | covered |
| Limits "is not seen ..." | each named shape measured clean (above) | true as stated |
| "does nothing while the list is empty" | A18; cost rows list empty = BASE | covered |

## THE HEAD AND THE SQUASH, MEASURED BY THE GATE (logs `g2063/logs/`)

- `merge_check.out`: `git merge-tree --write-tree f5882ed7 0ca131eb` rc 0, tree `1b633300`; the worktree's index tree
  equals it; = main outside the three paths (`diff --quiet` rc 0); the three blobs = the head's; 659 files.
- Heavy jobs on the squash tree (`heavy.py`, `CI=true`): `m-restore` (`--locked-mode`) rc 1: NU1900 "Warning As Error:
  Error occurred while getting package vulnerability data" for every project, because the runner's closed proxy refuses
  the audit feed (an environment fact, not the code; every gate and seat runs with the audit off); `m-restore2` with
  `-p:NuGetAudit=false` rc 0; `m-build` rc 0, `0 Warning(s)`, `0 Error(s)`; `m-test` rc 0: `total: 2171`, `failed: 0`,
  `succeeded: 2167`, `skipped: 4`; `m-publish-linux` and `m-publish-windows` rc 0 (14 and 15 files); then, not heavy,
  the squash tree's guard `GUARD: clean (14 files)` and `(15 files)` rc 0, unit run `Ran 117 tests` `OK`, `repo_rules.py`
  `RULES: clean (659 files)` rc 0; porcelain after: the three staged `M` rows, no lock file.
- Hosted (`hosted.out`, `hosted3.py 0ca131eb... --total 2153 --rules 659 --skipped-linux 4 --skipped-windows 21 --unit
  117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15`): run 45377804612, attempt 1, four jobs success;
  linux `succeeded: 2149`, windows `succeeded: 2132`; GUARD 14 / 15; rules `Ran 117 tests in`, `UNIT-TEST FLOOR: ran 117,
  floor 117`, `RULES: clean (659 files)`; secret-scan every proof line; check runs beside the four 0. `HOSTED
  0ca131eb...: PASS`.
- Main (`hosted-main.out`, `--total 2171 --rules 659 --unit 111 --floor 111`): run 45374389206, `HOSTED f5882ed7...:
  PASS`, Analyze (actions, csharp, python) success. Code scanning at f5882ed7: csharp, python, actions results_count 0;
  open alerts repository-wide 0 (GET about 22:00).

## THE PROBE (scratch only, never committed: `g2063/scratch/probe.py`; outputs `logs/probe-*.out`)

The head guard, round 1's guard and BASE's, each from `git show` into `scratch/{head,r1,base}` (sha256 `f2888169...`,
`e2473ad7...`, `cb29b0c4...`), in process on temporary folders; the landed throwaway certificate (`cert_der()` of the
head's test module, fingerprint asserted equal to `TEST_CERT_SHA256`) and synthetic DER runs framed `30 82` made in the
probe; nothing of either printed; a temporary deny-list per row.
- Rows (`probe-rows.out`): gate B2059's A0 to A19, B1 to B10, C1 to C4, each re-run (every expectation met), my E1 to
  E24 and Q1 to Q4 (the quiet rows quiet).
- Sweep (`probe-sweep.out`): B2059's shapes and the drafter's nine (64 LF, 76 CR LF, 67, 72, 60 LF, 64 LF 2-space, 76 CR
  LF 4-space, 64 LF tab, 64 JSON `\n`): round 2 CLEAN 0 in each; round 1 407, 341, 401, 363, 440, 1793, 1793, 1793, 407
  (B2059's 407 and 341 reproduced exactly; the drafter's 401, 363, 440 reproduced).
- Wide (`probe-wide.out`): 76 LF, 64 CR LF, 76 LF trailing blank, 64 JSON `\r\n`, 64 JSON `\n` + 2 spaces, 16 LF, 100 LF
  6-space: round 2 0 clean each (round 1 341, 407, 1793, 407, 1793, 1644, 1793); sizes 2049 to 16383 step 37 (388), 64
  LF and 64 CR LF 4-space: 0 clean.
- Extra (`probe-extra.out`): 66 LF, 70 LF, 74 CR LF (the widths where a last line is padding only), 64 LF 2-space with
  a trailing blank: 0 clean; the two escaped-tab shapes 1793 clean (FOUND 1).
- Folders (`probe-folders.out`): `Microsoft.NETCore.App/10.0.15` (188), `Microsoft.AspNetCore.App/10.0.15` (144), my
  squash-tree publishes (14, 15), gate B2059's (14, 15), the seat's `.tools/b2060/out` (14, 15; read only): `GUARD: clean`
  under round 1 and round 2, list empty and with the test fingerprint listed; lines only in round 2: 0 in all 12 rows.

## SCANS

- gitleaks 8.30.1: control FIRST, a token built by `scratch/scans_prep.py control` from two halves and 36 random
  characters (never printed), scanned alone: rc 1, `leaks found: 1`; moved to `g2063/_quarantine/gl-control`. The three
  head blobs, both commit messages, the added lines against HEAD1 (62) and against BASE (179), and both patches under
  neutral names (`scratch/neutral`, 9 files): rc 0 `no leaks found`. `gitleaks git` over `89a10a1b..0ca131eb`: 2 commits,
  rc 0 `no leaks found`.
- `words.py --control` `CONTROL FIRED: 13 of 13`; over the added lines (HEAD1 and BASE) and both commit messages:
  `WORDS: clean (4 files)`. `B2[0-9]{3}`: 0 in each of the four (control: this gate's commission 7).
- This folder's texts: `squash_scan.py` (the squash tree's, = main's) with #49 and #50: `SQUASH-SCAN: clean` each
  (control rc 1 found 2); `words.py` over squash subject (#49), squash body and PR title: `WORDS: clean (3 files)`;
  gitleaks over the seven files of this folder: see the last line of this section, written after the scan.
- gitleaks (about 22:06): the control re-scanned first (`_quarantine/gl-control`) rc 1 `leaks found: 1`; this folder's
  seven files as `scratch/neutral-texts/1.txt` to `7.txt` rc 0 `no leaks found` (only this line was added after it).

## NOT RUN

- CodeQL locally (no tool on this Mac for it; the pull request's own run is the authority, `landing.txt` step 3).
- `run_step.py`'s neutral scan of every stored object (the hosted secret-scan job ran it on the head: every proof line,
  read by `hosted3.py`; the seat's local run RELAYED).
- Anything on Windows or Linux by the gate (the hosted legs are the seat's push run, read by me). The pull request's
  merge-ref run (no pull request exists).
- Lane L3's round-2 head (it does not exist): the L3-first numbers in `landing.txt` MAIN MOVES (B) are DERIVED.
- The `BARE_BASE64_JOINER` blank-removal variant (FOUND 4), and a fuzz of the round-2 rule (the drafter's 20 000-run fuzz
  RELAYED, not re-run).

## OUTSIDE THE FENCES (said plainly)

- One Bash call (the squash tree's linux guard read, about 22:01) began with `bash -c "cd /tmp >/dev/null 2>&1; true" ;`,
  a no-op `cd` in a child shell: no file and no working directory of the session changed, and the guard read after it is
  unaffected. It breaks the commission's "no cd" form; named, not hidden.
- Nothing else: writes only under `g2063/` and this folder; GitHub by `gh api -X GET` only; no push, pull request,
  re-run, Jira, Azure, printer, device or human contact; nothing deleted (the control token moved to `_quarantine`).

## LANDING

**GO WITH FINDINGS: land this head by the form in `landing.txt`** (one head-pinned SQUASH of both commits onto main,
`--match-head-commit 0ca131eb...`; on f5882ed7 the squash tree is `1b633300`; the PR run must read total 2171, Ran 117,
floor 117, RULES 659, guards 14 and 15, and the python and actions code-scanning rows 0). FOUND 1 does not block: it is
carried as "still open" in `pr-body.md` and `FOR-RECORDS.md`.
