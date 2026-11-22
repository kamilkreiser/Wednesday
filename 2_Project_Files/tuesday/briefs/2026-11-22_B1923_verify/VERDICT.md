GATE B1923: GO WITH FINDINGS @ bb495b4 on main 4a0a971

Gate G2 (tests only), round 1, the one reader. OXPd 2, kit B1917 (seat X31, lane T): the two held test cells, owed
items 47 and 48. Head `bb495b4a3460cfe1596f5b5a894deca66c1bbb11` on `b1917/t-held-test-cells` (ONE commit, ONE parent
= main `4a0a9717277f60647dfc174e60ec04fc7008e615`). Read and measured 2026-11-22 21:57 to 22:05 AEDT (clocks by `date`
and tool lines), on Opus 5.5, in my own clone `fleet/state/s311/g1923/clone` (the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no local identity), detached at the head. Origin by `gh api -X GET` under the project
GH_CONFIG_DIR at 21:59 and again at 22:05: branch = bb495b4a, main = 4a0a9717, open pull requests 0, newest pull request
19, `compare main...bb495b4a` ahead 1, behind 0, merge base 4a0a9717, exactly the two files (+22 -0, +64 -0). No write
to the project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted.

**BLUF.** The change is exactly what it says: two test files, additions only, no product, generator, project or
workflow line. The W02 theory is the held diff byte for byte; the K8 check walks the whole set of client models (716,
measured, equal to the first reader's probe) and cannot pass by finding none. Both mutants reproduced RED on the head
with one `[FAIL]` each and GREEN at the base's test files, every mutant built with a fresh file time (the seat's `cp -p`
concern, DEVIATIONS 2, does not touch the result). Hosted run PASS at 1581. The findings are Info only: the K8 check
covers one optional property per model at the root only (enough for the rule it guards), and the theory's
`IOException` row is a contrast row the kit's mutants do not reach (the gate's own mutant shows it is not hollow).
Nothing blocks the landing.

## FOUND

1. **Info: the K8 check's reach is one optional property per model, root only.** `strict.Properties.FirstOrDefault(p
   => !p.Required)`: the first optional root property of each client model, set to null in `Payloads.Minimal`'s body.
   This is "every client model with an optional root property", as the kit and Stamp S4 say, and not "every optional
   property". It is enough for what it guards: the optional-null rule (`Oxpd2Json.cs:431`) tests the schema's
   `Tolerant` flag, which is per schema, and nested client schemas are held non-tolerant by K8's existing walk over
   every reachable schema. Named in pr-body "Still open" and FOR-RECORDS 1. No change needed.
2. **Info: the theory's `IOException` row is a contrast row.** No mutant of the kit can turn it red (kit THE
   CONTROLS says so). My own mutant `mIO` (`|| ex is IOException` added to the `JobNotFound` arm of
   `ScanReceiver.cs:232`) turns it red (Jobs `Total: 122, Errors: 0, Failed: 5`: this row, three `C01` rows and
   `L01`), so the row is not hollow, but landed cells already held that arm. It cannot pass by an early refusal:
   `ThrowingBody` never returns 0 (it throws on every read after its prefix), so the parser never sees a truncated
   body.
3. **Each cell tests what its name says (read whole, both files, `BASE..head`).** W02 theory: `Assert.Equal(expected,
   ex.Reason)` (the reason), `Assert.Null(ex.InnerException)` (no inner exception), `AssertGoneAsync` (the job gone from
   memory: `ListFiles` throws `JobNotFound`; its folder gone within the 10 s guard), `Assert.Equal(0,
   t.Spool.ReservedBytes)` (reserved 0). `Guard.Fails` is `Task.WhenAny` against the 10 s bound then
   `Assert.ThrowsAsync<JobServiceException>` (exact type; no catch-all). K8 row: `value is null && nullRefusal is not
   null && Kind == WrongType && Path == "$." + optional.Name` (all four, one assertion); the only `continue` skips a
   model with no optional root property; `Assert.True(optionalNulls > 0, ...)` after the loop. The walk is
   `SiteRead.Models().Where(m => !SiteRead.IsTarget(m))`, the same enumeration K8's landed walk uses.
4. **The walk is the whole set, MEASURED.** The Contracts executable run whole with `-diagnostics` on the head printed
   `[D::Datasec.Suite.Contracts.Tests] K8: client models refusing an optional root null 716` (Total 148, Failed 0):
   equal to the 716 of the tolerant-reading first reader's probe (RELAYED, that reader's F1). This was the seat's one
   UNMEASURED item.
5. **The seat's DEVIATIONS 2 (`cp -p` undo), my own reading.** The concern is real in principle (a restored file
   older than its built output can be skipped by an incremental build), but it could not change any result the seat
   reports: every later mutant was re-applied by a fresh write, the seat's final rebuild read Jobs 122 / Contracts
   148 with `Failed: 0` (either mutant still compiled in would turn its new cell red), and the hosted run comes from a
   fresh checkout. I re-did every apply and undo by a full write plus `os.utime` (never `cp -p`) and reproduced the
   seat's numbers exactly. DEVIATIONS 1 (BASE 4a0a9717, totals +1 per S2), 3 (`CI=true` on publish), 4 (stack line
   628 in Release) and 5 (a `shasum -c` re-run) accepted.
6. **Seat's claims re-measured, all held:** tool hashes 9 of 9 (my `cp -Rc` copy); `1-w02-body.diff` sha256
   `ca79627a...` = the head's own `git diff BASE head -- ReceiverTests.cs` byte for byte (`cmp` rc 0) = the third
   round's `.tools/b1872/gate/2-w02-body.diff`; `2-k8-optional-null.diff` = the head's Contracts diff (`cmp` rc 0); the
   head's two files `cc7bfb32...` and `aac57dc4...` and the three product files `1a695d77...`, `a3c9f6e6...`,
   `d8850334...` (= the kit); numstat 64/0 and 22/0; 86 added lines; the stored commit message equals
   `commit-message.txt` (302 bytes, `cmp` rc 0); one parent; the hosted numbers.

## TESTED (MEASURED; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at a time,
20 jobs, lock folders moved to `g1923/_quarantine/locks/`; waits only on load or on other holders, never broken)

- `git diff --name-only 4a0a9717 bb495b4a`: exactly `tests/Datasec.Suite.Contracts.Tests/TolerantReadingTests.cs`,
  `tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs`. `ls-files` 500. `merge-tree --write-tree 4a0a9717 bb495b4a` rc 0,
  tree `c2b3e0d95e7604132a24268088de1d92e69a6ca0` = the head's own tree (GET).
- GREEN on the head: `CI=true dotnet restore --locked-mode` rc 0, porcelain 0 lines; build `0 Warning(s)` `0 Error(s)`;
  Jobs `Total: 122, Errors: 0, Failed: 0`; Contracts `Total: 148, Errors: 0, Failed: 0`.
- `mReasonDisposed` (the exact text of `3-mutants.txt`, OLD found 1) on the head: build 0/0; Jobs `Total: 122, Errors:
  0, Failed: 1`, `[FAIL]` 1:
  `...ReceiverTests.W02_a_body_whose_read_throws_ends_the_receive_typed_and_the_job_is_wiped(thrown: "ObjectDisposedException") [FAIL]`,
  `Expected: JobNotFound`, `Actual:   ScanRefused`, at `ReceiverTests.cs(567,0)`. With BASE's `ReceiverTests.cs`
  (written from `git show`, sha256 `7528a5c5...`) under the same mutant: build 0/0; Jobs `Total: 120, Errors: 0,
  Failed: 0`. Undone by full write: both files equal to the head's, `git diff --quiet -- src contracts tests` rc 0.
- `mNullStrictToo` on `Oxpd2Json.cs` AND `Oxpd2RuntimeText.cs` (OLD found 1 each) on the head: build 0/0; Contracts
  `Total: 148, Errors: 0, Failed: 1`, `[FAIL]` 1:
  `Datasec.Suite.Contracts.Tests.TolerantReadingTests.K8_the_device_clients_stay_strict [FAIL]`, message
  `K8: Datasec.Suite.Adapters.Oxpd2.Generated.Application.ActiveApplication did not refuse an optional null:`. With
  BASE's `TolerantReadingTests.cs` (`3c97174e...`) under the same mutant: build 0/0; Contracts `Total: 148, Errors: 0,
  Failed: 0` (green under a mutant that the head's binary reds proves the base's file was compiled). Undone by full
  write: all three equal, `git diff --quiet` rc 0.
- After all undos: build 0/0, Jobs 122 / 0 failed, Contracts 148 / 0 failed; the five files' sha256 = the head's;
  porcelain 0 lines. The diagnostics run (FOUND 4). `mIO` (FOUND 2), undone, rebuilt, Jobs 122 / 0 failed.
- HOSTED: `hosted2.py bb495b4a... --total 1581 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor
  111 --hardened-scan` rc 0: run 45014390651, attempt 1, four jobs success, `check runs beside the four: 0`; linux
  1581 x2 / 1577 / 4 / 0 failed, `0 Warning(s)` `0 Error(s)`, GUARD clean (10 files); windows 1581 x2 / 1562 / 19 / 0,
  GUARD clean (11 files); rules Ran 111, floor 111, RULES clean (500 files); secret-scan every hardened row OK; last
  line `HOSTED bb495b4a3460cfe1596f5b5a894deca66c1bbb11: PASS`. `failed Datasec.` lines (`grep -i -F`): linux 0, windows
  0 (controls: `total: 1581` 2 in each).
- WORDS: `--control` `CONTROL FIRED: 13 of 13`; over the 86 added lines and the stored commit message:
  `WORDS: clean (2 files)`; non-ASCII lines in the added text 0.
- GITLEAKS 8.30.1: control FIRST (a token shape built from two halves and random characters by program, never
  printed): rc 1, `leaks found: 1`, moved to `_quarantine/scan-control`; then the added lines and the message as
  neutral `<n>.txt`: rc 0, `no leaks found`.
- Check names by GET: pull request 18's head `ea72d921` and 19's head `81b5f3ef` each carry 8 distinct names (linux,
  windows, secret-scan, rules twice each; Analyze (actions), (csharp), (python); CodeQL), all success; main 4a0a9717
  carries the four jobs and the three Analyze rows, all success; open code-scanning alerts on main 0.

## NOT TESTED

- No whole-solution run, publish or release guard locally: the hosted legs (fresh checkouts) carry those, and the
  change is two test files. No local Linux or Windows run.
- No CodeQL locally: the C# analysis is read on the pull request (landing step 3 requires a `/language:csharp` row at
  the head's sha with results_count 0).
- The `run_step.py` neutral scan of the commit locally (the hosted secret-scan job ran it on this head: OK rows above).
- A mutant against `ThrowingBody` or the K8 row's body builder themselves (read, not mutated).

## HOW

Tools copied by `cp -Rc` from `fleet/state/s310/d1917/gate/` to `g1923/gate/` (9 of 9 sha256 equal to the kit).
Driver `g1923/scratch/mutants_run.py` (applies each mutant by a full write and `os.utime`, never `cp -p`; restores the
same way; every job through `heavy.py`); its output `g1923/logs/mutants_run.console2` and `mutants_run.out`; per-job
logs `g1923/logs/g-*.log`; hosted `g1923/logs/hosted.out` and `g1923/logs/hosted/`; diffs, added lines and message in
`g1923/scratch/` (`head-w02.diff`, `head-k8.diff`, `added.txt`, `msg.txt`, `neutral/`, `neutral-landing/`,
`squash-scan.out`). `clone` left detached at the head, porcelain 0 lines, `bin/`/`obj/` kept. No process left running;
the wave lock is not held by this gate.

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 244 bytes (= the commit subject, `cmp` rc 0; under 256). `pr-body.md` (owed items 47 and 48: what
  changed and why, what proves it, the K8 check's one-property root-only reach and owed item 46 left open; who decides:
  the coordinator; no line says the product owner decided anything about these tests; ends with the Claude Code line).
  `squash-subject.txt` 253 bytes, the subject plus ` (#PRNUM)`. `squash-body.txt`: the seat's commit body (its one
  attribution line) as the end, with three paragraphs of what and why before it; ends with
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. `landing.txt` in B1919's form: 8 check names; merge-ref
  totals 1581 both legs, succeeded 1577 / 1562, skipped 4 / 19, RULES 500, Ran 111, floor 111; step 6: main's push run
  PASS by `hosted2.py` at 1581.
- `words.py` over title, squash subject and squash body: clean (every class 0). PR body 6 hits, all expected:
  `coordinator` 2 (the required "who decides" line) and 4 non-ASCII bytes (the required robot line). `landing.txt` and
  this folder's other files are records for Tuesday, never repository text.
- gitleaks (after a fresh firing control, rc 1, moved to `_quarantine/gl-control2`) over the six texts of this folder
  but VERDICT.md as neutral names: rc 0, `no leaks found`; after the last edits, again over all seven texts including
  a draft of this file (control `gl-control3` rc 1 first): rc 0. `build/squash_scan.py` with `#PRNUM` replaced by `#20` and
  `squash-body.txt`: control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks and CodeQL read as step 3 requires.
