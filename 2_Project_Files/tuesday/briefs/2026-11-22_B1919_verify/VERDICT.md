GATE B1919: GO WITH FINDINGS @ 81b5f3e on main 4e8828e

Gate G1 (build and pipeline files), round 1, the one reader. OXPd 2, kit B1916 (seat X30): rule R6's two open-quote
shapes and the hidden flow mapping, and the Linux image base pinned by digest. Head
`81b5f3efc5b3bc841a53e3cf87cfd42969225b50` on `b1916/wp03-r6-shapes-digest-pin` (ONE commit, parent = main
`4e8828ee0259b2605c98ba0f9f319f6527436778`). Read and measured 2026-11-22 21:02 to 21:13 AEDT (clocks by `date` and
tool lines), on Opus 5.5, in my own clones `fleet/state/s310/g1919/clone` (the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity) and `g1919/clone-red` (a local clone of it, push URL `invalid://no-push`). Origin by
`gh api -X GET` under the project GH_CONFIG_DIR at 21:02: branch = 81b5f3ef, main = 4e8828ee, open pull requests 0,
newest pull request 18, `compare main...81b5f3ef` ahead 1, behind 0, exactly the three files. No write to the
project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted.

**BLUF.** The change does what it says and only that: three files, no workflow, no C#. RED FIRST reproduced exactly
(111, `failures=5`, the five rows, five `0 != 1`, 0 ERROR), GREEN reproduced (111, OK), the four mutants killed (2, 3,
1, 4, the same rows as the kit), today's `ci.yml` 0 findings under both rules, and the digest is the hosted runner's
own resolution of the tag: the tag build of main resolved the tag to it and pulled the same base layers the pinned
build pulled, so the pin changes nothing the image step builds today. The named costs H5 to H7 are acceptable. The
findings are Minor: three more false-refusal spellings the kit did not list (one of them a comment line), H8 still
open with a small reach, and nothing that moves the digest later. None blocks the landing.

## FOUND

1. **What R6 now refuses that a writer would legitimately write (judged: acceptable).** Re-measured by
   `check_spellings` on single lines, green `[1]`, old rule `[]`: H5 `  b${{ x }}: c`; H6 `      - "a ${{ x }}: b"`;
   H7 `        run: echo "hello"`, `    if: github.event_name == 'push'`. **Beyond the kit's list (same instrument,
   same result):** `      - echo "hi"` and `          args: --flag 'x'` (H7's family); `    name: &n "rules"` and
   `    name: !!str 'rules'` (an anchor or a tag before a quoted value: the value-start test knows only the first
   non-blank, `- ` and `: `). Why acceptable: every one fails closed (the rules job goes red with the line number;
   nothing passes silently); each has a mechanical rewrite (`${{ }}` or a block scalar); today's `ci.yml` uses none
   (no `if:` line; every multi-word quoted command is in a `run: |` block); and the whole-file fingerprint already
   sends every `ci.yml` edit to a person. The real cost is friction: the first `if: a == 'b'` someone adds, GitHub's
   own documented spelling, will be refused with only a line number.
2. **Minor, new (my probe, a shape the kit did not list): a comment line is refused.** Refusal (iii) reads the raw
   line, comment included. Single line `    # ci-${{ github.ref }}: one group per ref`: green `[1]`, old `[]`. End to
   end: planted above line 15 of a copy of today's `ci.yml` in `clone-red` (rule file = the head's, `cmp` rc 0), the
   new rule printed `RULES: R6 .github/workflows/ci.yml:15` rc 1, the old rule `RULES: clean (500 files)` rc 0;
   restored by copy. A comment is never YAML, so this is a pure false refusal. A comment with a colon before the
   marker (`# one group per ref: ci-${{ github.ref }}: ...`) stays quiet (measured). Low cost; backlog: read (iii)
   on the line without its comment (`yaml_scan`'s own comment cut), with a quiet row.
3. **What it still lets through: H8 (`    name: ${{ x }} |`, `[]` both), and its reach is small.** The reader opens a
   phantom block YAML does not. Measured with libyaml 0.2.1 (`/usr/bin/ruby -ryaml`) on five whole-document
   prototypes: libyaml accepts the line only when the next line is not indented more than the key (`name` and a
   `permissions: write-all` key, or `- name:` and a `uses: evil/x@main` key at the same indent), and there the
   reader's block ends at once (rule `[]` with nothing skipped: the next key is read); with a more indented next line
   libyaml refuses the document (`Psych::SyntaxError`, three prototypes). And R3 and R4 read every line regardless of
   blocks (`repo_rules.py:381-387`): a phantom block hides lines from R6's spellings only. Not proved for GitHub's
   parser. Stays a named limit (pr-body, squash body).
4. **No other let-through found** in the shapes I tried: a quote after an expression in a value
   (`name: ${{ x }} "y"`) is quiet and harmless (YAML reads a plain scalar; the reader reads a closed quote, and an
   unclosed one fires `left_open`); a quote after `[`, `{` or `,` is flagged and the flow refusals fire anyway; an
   expression key after a dash (`- ${{ x }}: y`) fires; `- - "a"` and `name:  "a"` are quiet.
5. **Today's `.github/workflows/ci.yml`:** `check_spellings` over its 218 lines: `[]` green and `[]` old. Its one
   `${{` (line 15, `group: ci-${{ github.ref }}`) sits after the colon. No finding changes.
6. **The digest (compared with hosted logs by GET, escape codes removed, by program).** Three linux job logs: main
   `4e8828ee`'s tag build (job 137164654716, run 45008282606), the b1912 head's tag build (job 137158213066) and the
   head's pinned build (job 137169546416, run 45009852222). Each names exactly one aspnet digest,
   `12b1135f5f8b3c0a214f2a680ff2033dff4f684f445d6c697d9524ceeb303586`, equal to the Dockerfile's (`True` x3). In the
   tag builds it follows `load metadata for mcr.microsoft.com/dotnet/aspnet:10.0` as `[1/3] FROM ...@sha256:` and
   `resolve ...@sha256:`: the builder's own resolution. **Does pinning change what is built?** No, today: the seven
   sha256 values of the base pull (the digest and its six layer and config blobs) are identical in main's tag build
   and the head's pinned build; only the four exported values of the new image differ, as any rebuild's do. The
   head's `load metadata` line carries the digest (0 lines without it). Whether the digest is the multi-platform
   index or the amd64 manifest: UNMEASURED (the pinned build on the amd64 runner succeeded either way).
7. **Minor (records): nothing moves the digest.** `.github/` holds only `workflows/ci.yml` (no Dependabot or other
   updater), so a patch image of `10.0` reaches the build only by a change of this line (D4's named cost). Backlog:
   who moves it and when.
8. **Seat's claims re-measured, all held:** tool hashes 9 of 9; THE CODE's patched sha256 for all three files (head
   tree) and the BASE column (clone-red at BASE); numstat 25/6, 7/1, 2/1; 34 added lines; the stored commit message
   equals `commit-message.txt` (1714 bytes); the hosted numbers. The seat's one `cd` slip (its DEVIATIONS) changed
   nothing: accepted. Its STATUS first line still reads PENDING with a READY last line: a records note.

## TESTED (MEASURED; every suite run through the kit's `heavy.py` unchanged, one at a time, 7 jobs, lock folders
moved to `g1919/_quarantine/locks/`; waits only on load or on other holders, never broken)

- `git diff --name-only 4e8828ee 81b5f3ef`: exactly `build/repo_rules.py`, `build/tests/test_repo_rules.py`,
  `packaging/linux/Dockerfile`; `ls-files` 500; `merge-tree --write-tree 4e8828ee 81b5f3ef` rc 0, tree
  `ac3bf369805ef760a583afb1dbc785c64ace6b1b` = the head's own tree.
- RED: `1-red-first.patch` alone on BASE in `clone-red` (apply rc 0, `test_repo_rules.py` sha256 `586bb74a...` =
  THE CODE, `repo_rules.py` `da1aa060...` = BASE): `g-red: rc 1 (91s, lock waits 17)`; `Ran 111 tests`,
  `FAILED (failures=5)`; `^ERROR:` 0; `^FAIL:` 5, exactly the flow-mapping method and the four labelled shape rows;
  `AssertionError: 0 != 1` 5.
- GREEN (the head, `-v`): `g-green: rc 0 (76s, lock waits 14)`; `Ran 111 tests`, `OK`, 111 lines ` ... ok`, 0
  FAIL/ERROR. `python3 -I build/repo_rules.py <clone>`: `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder
  here)`, `RULES: clean (500 files)`, rc 0 (the clone's parent holds no `1_Project_Definition`).
- MUTANTS (Edit tool on the head's `repo_rules.py`, each undone by copy from `scratch/pre-mutant/`, `cmp` rc 0):
  mNoMisplaced `failures=2` (the two `after a quote inside the key` rows); mNoKeyExpression (diff `309,310d308`)
  `failures=3` (flow mapping, the two `behind an expression in the key` rows); mRaw `failures=1` (quiet
  `name: ${{ 'a' }}`); mAnyMarker `failures=4` (quiet `fromJSON('[1]')`, flow mapping, quiet `${{ 'a' }}`, quiet
  `"x: ${{ github.ref }}"`). Each `Ran 111 tests`, 0 ERROR. No survivor. After the last: `git diff --quiet 81b5f3ef`
  rc 0. Then `g-green-2: rc 0 (11s, lock waits 1)`: `Ran 111 tests`, `OK`.
- PROBES: the single-line table of FOUND 1 to 4 (`scratch/probe.py`, 20 lines, green and old rule files side by
  side); the comment plant end to end (FOUND 2); five H8 documents through libyaml (`scratch/h8.py`).
- HOSTED: `hosted2.py 81b5f3ef... --total 1579 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor
  111 --hardened-scan` rc 0: run 45009852222, attempt 1, four jobs success, `check runs beside the four: 0`; linux
  1579 x2 / 1575 / 4 / 0 failed, GUARD clean (10 files); windows 1579 x2 / 1560 / 19 / 0, GUARD clean (11 files);
  rules Ran 111, floor 111, RULES clean (500 files); secret-scan every hardened row OK; last line
  `HOSTED 81b5f3efc5b3bc841a53e3cf87cfd42969225b50: PASS`. Its `job-linux.log` names the pinned digest 6 times.
- WORDS: `--control` `CONTROL FIRED: 13 of 13`; over the 34 added lines and the stored commit message:
  `WORDS: clean (2 files)`.
- GITLEAKS 8.30.1: control FIRST (a token shape built from two halves by program, never printed): rc 1,
  `leaks found: 1`, folder moved to `_quarantine/gl-control`; then the added lines, the message and the three head
  files as neutral `<n>.txt`: rc 0, `no leaks found`.
- Main `4e8828ee`'s check names: the four jobs and Analyze (actions, csharp, python); open code-scanning alerts on
  main 0. Pull request 18's head `ea72d921` carries 8 distinct check names (four jobs twice each, three Analyze,
  CodeQL), all success.

## NOT TESTED

- No local Linux or Windows run, no docker, no dotnet, no registry call: the C# legs and the image step are judged by
  the hosted run only (the lane changes no C#).
- No CodeQL locally: the Python analysis is read on the pull request (landing step 3 requires a `/language:python`
  row at the head's sha with results_count 0).
- GitHub's own YAML parser on the five red shapes and on H8 (libyaml only). Whether the digest is an index or one
  platform's manifest. The `run_step.py` neutral scan of the commit (the hosted secret-scan job ran it on this head:
  OK rows above).

## HOW

Tools copied by `cp -Rc` from `fleet/state/s310/d1916/gate/` to `g1919/gate/` (9 of 9 sha256 equal to the kit). Logs:
`g1919/logs/` (`g-red.log`, `g-green.log`, `g-m*.log`, `g-green-2.log`, `hosted-head.out`, `hosted-head/`,
`job-<id>.raw` x3, `gl-*.log`, `words-landing.log`, `squash-scan.log`). Scripts: `g1919/scratch/` (`probe.py`,
`h8.py`, `ciyml.py`, `digest.py`, `layers.py`, `mres.py`), with the head's and BASE's rule files side by side in
`scratch/green-rules/` and `scratch/base-rules/`. `clone` left at the head (porcelain 0 lines, detached at 81b5f3ef);
`clone-red` left at BASE plus patches 1 and 2 (= the head's two `build/` files; its `ci.yml` restored by copy).

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 186 bytes (= the commit subject). `pr-body.md` (OXPD2-25 / C-67's follow-up and owed item 7; the
  named costs H5 to H7 plus those of FOUND 1 and 2, the open H8, stated plainly; who decides: the coordinator; ends
  with the Claude Code line). `squash-subject.txt` 195 bytes, the commit subject plus ` (#PRNUM)`.
  `squash-body.txt`: the seat's commit body plus one paragraph naming the costs and H8; ends with the
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` line. `landing.txt` in B1918's form: 8 check names;
  merge-ref totals 1579 both legs, succeeded 1575 / 1560, skipped 4 / 19, RULES 500, Ran 111, floor 111, the pinned
  digest on the linux leg; step 6: main's push run PASS and its linux log naming the pinned digest.
- `words.py` over the four message texts: title, squash subject and squash body clean (every class 0); PR body 8
  hits, all expected: ticket key 1 and clarification id 1 (the required OXPD2-25 / C-67 line), `coordinator` 2 (the
  required "who decides" line), 4 non-ASCII bytes (the required robot line). gitleaks (after a fresh firing control,
  rc 1) over all six texts of this folder but VERDICT.md as neutral names: rc 0, `no leaks found`.
  `build/squash_scan.py` with the subject's `#PRNUM` replaced by `#19` and `squash-body.txt`: control `rc 1, found 2`,
  message `rc 0, found 0`, `SQUASH-SCAN: clean`.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks and CodeQL read as step 3 requires.
