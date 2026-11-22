GATE B1960: GO WITH FINDINGS @ 10f446f on main 5b66a7b

Gate G1 (security surface: the card-to-user mapping), round 1 of 2 of lane A2-F2, one Opus reader. OXPd 2, lane A2-F2,
kit B1953 (seat X43; Q1 = a in words at stamp S4, Q2 to Q6 the defaults, each the coordinator's, not the product
owner's): the card store's untyped exit on a text the JSON reader cannot read (gate B1950 FOUND 1). Head
`10f446f39a2ac27565506e3bf342c4900d5dd5dd` on `b1953/a2-f2-malformed-escape`, ONE commit, one parent `49f686a8`. Read
and measured 2026-11-23 06:18 to 06:38 AEDT on Opus 5.5 in my own scratch `fleet/state/s314/g1960/`: `clone` (the
kit's `clone.py ... draft`: push URL `invalid://no-push`, no identity; detached at the head) and worktrees `red`
(`49f686a8` + `1-red.diff`, then + `2-fix.diff`), `phead` (the head) and `pbase` (`49f686a8`) for my probe, `merged`
(main `5b66a7b1` + the head's diff in the index, never committed). Every dotnet job through the kit's `heavy.py`
(sha256 `31adedc8...`) and the wave lock, one at a time (114 jobs, lock waits 0 to 46 behind other holders, load1 3.6
to 6.6); no other holder's lock touched (the B1961 drafter's held it at 06:35, left alone). Origin by `gh api -X GET`
under the project GH_CONFIG_DIR: main `5b66a7b1`; this branch `10f446f3`; `compare 49f686a8...10f446f3` ahead 1, 7
files; `compare main...10f446f3` diverged 1 / 1; pull requests newest 30 (closed, merged), none open; open alerts on
main 0. No write to the project, GitHub or Jira; no push, no pull request, no re-run; no `cd`; nothing deleted (probe
file and scanner control moved to `g1960/_quarantine/`).

**BLUF.** The change does what the kit says and the property holds on every path the library has: one parse
(`CsaStore.cs:242`, the library's only `JsonDocument`), four callers (`:165`, `:171`, `:196`, `:213`), and the walk
(`CsaReading.cs:159`) now reads every name (`:167`) and every string value (`:185`) before `Clone()` and before any read,
inside a try that types an `InvalidOperationException` as `MalformedAnswer` (`CsaStore.cs:254`). The head is BASE plus
the two frozen patches byte for byte. Red first at `49f686a8`: 1806 / 23 failed, all Identity, all `Assert.IsType()
Failure` (22 `InvalidOperationException`, 1 `Value is null`); the head 1806 / 0; 47 of 47 mutants MATCH and undone,
rebuilt, green again; merged with main `5b66a7b1` 1808 / 0, RULES 553; scans clean. My probe (39 shapes, head against
BASE): every unreadable text, raw bytes that are not UTF-8 included, is `TYPED MalformedAnswer` at the head (BASE: 6
untyped, the rest read); every valid text is read at both; the caller's cancellation is `TaskCanceledException` at both.
**The head's only hosted red is Contracts C7** (job 137299375943: exactly one failed test line, of 14 assemblies only
Contracts failed, Identity passed), not this lane's. **One Minor finding: the commit moved two lines the README cites
and did not update the citation (FOUND 1).** Nothing blocks the landing on this lane's merits; it lands AFTER the C7
fix, and the pull request's own windows check is binding (landing.txt).

## FOUND

1. **Minor (documentation; a false pointer in repository text, `<project>/CLAUDE.md:61-62`): `README.md:35` cites
   `CsaStore.cs:288` and `:305` for the two blob-maker catches; at the head they are `:294` and `:311`.** The commit
   inserted six lines at `CsaStore.cs:254` to `:259`; at BASE `:288` and `:305` were the two `catch (Exception)`, at the
   head `:288` and `:305` are each a lone `{` (printed by `awk NR==n` at both). The sentence itself ("anything it
   throws, a cancellation included, is `CodecFailed` too") is still true. Neither the kit (it checked `:45` to `:48`
   and the Limits line), nor the seat ("each printed above and true at the head"), nor `words.py`/`boundary.py` read
   this line. Every other `Csa*.cs:<n>` citation in the repository is true (`git grep` at the head finds five citing
   lines: this one, and `:44` to `:47` with six citations, INFO 7). Fix: one line,
   `:288` -> `:294`, `:305` -> `:311` (a fix round of this lane, or carried to the next Identity lane; the coordinator's
   choice).

## INFO

1. **The boundary, read against the head.** The try of `CsaStore.cs:240` to `:249` holds three calls: the parse, the
   walk and `Clone()`. Every read after it (`CsaStore.cs:166`, `:178` to `:180`, `:197`, `:203`, `:208`, `:215`,
   `:221`; `CsaReading.cs:26` to `:150`) reads a name or a string value of the clone of the walked document, which
   the walk already read from the same bytes; `TryGetProperty`/`EnumerateObject` compare names the walk read; numbers
   are only counted, booleans read with `GetBoolean` on a checked kind, ids with `Guid.TryParse`. The walk returns
   early only on a repeated name, and then the call is `MalformedAnswer` anyway (probe S16, S17). The PATCH answer is
   never parsed (`CsaStore.cs:140`; probe E02 `Enrolled`, 1 PATCH, at both). No other untyped path found.
2. **Other exception families.** `JsonDocument.Parse` raised none but `JsonException` for the shapes probed (empty,
   `null`, a UTF-8 BOM, a raw control character, a wrong escape form per the drafter): typed at both. Its input is
   `ReadOnlyMemory<byte>` (`GraphResponse.cs:27`), so no transcoding `ArgumentException` path exists. No
   `FormatException` source is inside the try (`Guid.TryParse` does not throw).
3. **The caller's cancellation is not swallowed.** Inside the new try nothing awaits or takes the token; MEASURED
   (probe C01 to C05): cancelled before a find, during its request, while a bad or a valid answer is built, or before
   an enrolment: `TaskCanceledException` at head and BASE alike.
4. **No real answer shape becomes a refusal (judged from the repository and the probe, never the network).** The
   design and reports document no answer body with an escape (case-insensitive counts over Design, Analysis, Review,
   Registers, BACKLOG, CLARIFICATIONS, 49 files: `surrogate` 1, an unrelated BACKLOG line 288; `\uXXXX` 0; `emoji` 0;
   `jobTitle` 0); display names are free text (A1 `:200` to `:205`, design `02:78`). MEASURED read at head and BASE: a
   valid surrogate-pair escape in a value and in a name (`\uDBFF\uDFFF` included), raw 4-byte UTF-8, `\u0000`,
   `\uFFFF` `\uFFFE` `\uFEFF` `\uFFFD`, the common escapes, a 1 MB value, a valid pair in a set string. Only a text
   that is not a whole UTF-16 character or not UTF-8 is refused. Whether Graph ever sends one is UNMEASURED.
5. **The catch's trade-off (named, DERIVED).** `catch (InvalidOperationException)` takes any such exception inside
   that try, not only a text read (`ObjectDisposedException` is a subclass; `Clone()` inside the `using` cannot meet a
   disposed document). A later defect in the walk that raises one would end as `MalformedAnswer` with no inner
   exception (the cells assert `Assert.Null(failure.InnerException)`, the same as the `JsonException` catch). A defect
   that hits every answer still turns the existing cells red (every valid-answer cell would refuse); a shape-specific
   one would be masked as a data refusal: fail closed, no user, no write, but the cause is lost. The alternative (catch
   in the walk only, or attach the inner exception) changes the design and the cells; not a finding.
6. **D2's cost reaches further than the kit's wording, as the README states it.** MEASURED (probe, head against
   BASE): an unread field with such a text in an enrolment's search (E03) or user read (E04): BASE `Enrolled` with 1
   PATCH, head `MalformedAnswer` with 0; in the definition's unread `description` (K02): BASE passes, head fails the
   schema check, which every enrolment runs first and does not keep when it fails. A bad escape in `@odata.nextLink`'s
   value (S15): BASE `Ambiguous`, head `MalformedAnswer` (nobody chosen at both). The README's "wherever it sits in the
   answer, a part the store never reads included" (`README.md:47` to `:48`) and its Limits line (`:62` to `:63`)
   cover it; the kit's D2 sentence named the search case only. FOR-RECORDS item 2.
7. **README and comments, at the head, each against the code.** `:44` "one parse, `CsaStore.cs:242`": true. `:45`
   "before anything of it is read (`CsaStore.cs:243`, `CsaReading.cs:159`)": true. `:45` to `:46` "reads every name
   and every string value of the answer once (`CsaReading.cs:167` and `:185`)": true. `:47` "`MalformedAnswer` too
   (`CsaStore.cs:254`)": true. `:47` to `:48` "wherever it sits ... a part the store never reads included": true
   (probe). Limits `:62` to `:63`: true, carries UNMEASURED. `:39` to `:41` (every call typed or the caller's
   cancellation): now true for every shape probed. `:35`: FOUND 1. The class remarks (`CsaReading.cs:12` to `:14`),
   the walk's summary (`:156` to `:157`) and the catch's comment (`CsaStore.cs:256` to `:257`) say the same; they name
   escapes only, though raw bytes that are not UTF-8 also land in that catch (D4 / Q2 as stamped; FOR-RECORDS item 4).
8. **The windows red is C7 only.** Job 137299375943 (attempt 1): one `failed Datasec.` line,
   `Datasec.Suite.Contracts.Tests.GatewayStubTests.C7_one_send_reaches_every_connection_once_and_bad_bodies_send_nothing
   (5s 649ms)`; `total: 1806`, `failed: 1`, `succeeded: 1784`, `skipped: 21`; the 14 assemblies' result lines (each
   printed twice): only `Contracts.Tests.dll` failed, `Identity.Tests.dll` passed (positive control: `C7_` 5 times in
   the log). Linux, rules and secret-scan of the same run: success. Diagnosis B1955 RELAYED; I did not judge C7.
9. **Main at the gate.** Pull request 30 changed four paths (two READMEs, two added test files), not "a Universal
   Print README and one test file" as the commission says; none is shared with this lane. Main's push run 45056289720:
   PASS at `--total 1785 --rules 553`.
10. **CodeQL:** one new type-filtered catch that rethrows a typed failure, and one discarded read; 0 open alerts on
    main. Read on the pull request (landing.txt step 3).

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `fleet/state/s313/d1953/seat-tools/` to `g1960/gate/`; 10 of 10 sha256 equal to kit
  B1953's table. `words.py --control` `CONTROL FIRED: 13 of 13`.
- **THE COMMIT against its kit:** one parent `49f686a8`, `rev-list --count` 1; the stored message byte-equal to
  `commit-message.txt` (287 bytes); author and committer the project's own address (masked); `--name-status` exactly
  seven `M` rows, the owned paths (control: a planted `A` row fails the check); numstat 8/1, 6/0, 7/2, 26/0, 44/0,
  28/0, 28/0; the SHARED FILES `diff --quiet` rc 0, control over `src/Datasec.Suite.Identity` rc 1; public lines added
  or removed 0, control 2; `ls-tree` 551 files at both; the seven blobs printable ASCII, no tab, no CR, final LF
  (control 1); Fact/Theory/InlineData per test file 5/7/18, 6/8/59, 2/6/23, 2/5/16, column 1 0 (equal to the kit).
- **THE PATCHES = THE HEAD:** in worktree `red`, after `1-red.diff` and `2-fix.diff`, `git diff --stat 10f446f3` is
  empty (rc 0).
- **RED FIRST at `49f686a8`** (`red`, `1-red.diff` alone): locked restore rc 0; build `0 Warning(s)` `0 Error(s)`;
  whole solution `total: 1806`, `failed: 23`, `succeeded: 1779`, `skipped: 4`; 23 `failed Datasec.` lines, 23
  Identity, 0 outside; per cell E12 3, F14 11, K07 4, R08 5; `Assert.IsType() Failure` 23, of which
  `typeof(System.InvalidOperationException)` 22 and `Value is null` 1; the Identity executable alone `Total: 135,
  Errors: 0, Failed: 23`, the same counts.
- **GREEN, the head (clone):** `CI=true` locked restore `--force` rc 0; build 0/0; whole solution `total: 1806`,
  `failed: 0`, `succeeded: 1802`, `skipped: 4`.
- **THE MUTANTS:** `mutants_a2f2.py <clone> <keep> run g1960 'B1960 gate'` as ONE call: 47 rows, every row `Total 135`,
  `MATCH`, `undone equal True`; last line `MUTANTS: 47 of 47 MATCH, 47 of 47 undone equal`, rc 0 (the new rows
  `mBadTextUntyped` 23 failed, `mBadTextAsGraphFailed` 23, `mValuesUnread` 11, each red on E12 F14 K07 R08; the three
  grown rows as listed). After it: status clean; both sources back on `446e3868...` and `eb5ee931...`; build 0/0 with
  the library's dll at 06:23:46 after the last restored source at 06:23:13; whole solution again 1806 / 0 / 1802 / 4.
- **MY PROBE** (`G1960Probe.cs`, one fact, 39 shapes, its own byte-level handler, outcomes only, no value printed;
  sha256 `b3f14273...`): `phead` (the head) built 0/0 and run whole `Total: 136, Errors: 0, Failed: 0`; `pbase` (BASE)
  built 0/0, `Total: 113, Errors: 0, Failed: 0`; outcome files `g1960/scratch/probe-head.txt` (`c8c68c83...`) and
  `probe-base.txt` (`8b31cdc2...`); their difference is INFO 1 to 6. A first run of the probe wrapped every failure in
  `AggregateException` (my wrapper's `ContinueWith`; no outcome taken from it); rewritten with `await`, rebuilt, run
  again. The probe file then moved to `g1960/_quarantine/probes/`.
- **THE MERGE:** `git merge-tree --write-tree 5b66a7b1 10f446f3` rc 0, tree `a711478f`, no conflict; `merged` (main +
  the head's diff by `git apply --index`, `write-tree` = `a711478f`, 553 files): locked restore `--force` rc 0; build
  0/0; whole solution `total: 1808`, `failed: 0`, `succeeded: 1804`, `skipped: 4`; `repo_rules.py` `RULES: clean (553
  files)`. The head alone `RULES: clean (551 files)`. Both with `RULES-NOTE: R5 hash half NOT RUN (no supplied-source
  folder here)` (never `--source-documents`). Expected after the merge, as commissioned: 1808 (1785 + 23), RULES 553:
  held.
- **CHECKS:** `boundary.py` `required: _graph.SendAsync( 2, HttpMethod.Patch 1, GetElapsedTime( 1, HttpMethod.Get 1`,
  `BOUNDARY: clean (9 files)`; its control `CONTROL FIRED: 33 of 33`.
- **HOSTED (GET only):** `hosted2.py 10f446f3... --total 1806 --rules 551 ...`: run 45052136167, linux, rules,
  secret-scan success; windows failure (C7, INFO 8): `HOSTED 10f446f3...: FAIL 6`, as the seat printed. `hosted2.py
  5b66a7b1... --total 1785 --rules 553 ...`: run 45056289720, four jobs and three Analyze rows success, linux 1781,
  windows 1764: `HOSTED 5b66a7b1...: PASS`.

## SCANS

- `words.py` over the 147 added lines of `49f686a8..10f446f3` and the head's message (`scratch/words/1.txt`, `2.txt`):
  every count 0, `WORDS: clean (2 files)`.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token-shaped value
  built by program from two halves and 36 random characters in a new scratch folder, never printed): rc 1, `leaks
  found: 1`, folder moved to `g1960/_quarantine/gl-control`; the seven head blobs, the message and the two words files
  as ten files in a new folder: rc 0, `no leaks found`.
- `words.py` over `squash-subject.txt` (201 bytes), `squash-body.txt` and `pr-title.txt` (178 bytes, under 256):
  every count 0, `WORDS: clean (3 files)`.
- `build/squash_scan.py <subject with #31> squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from main
  `5b66a7b1`'s build/): control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks over this verdict folder (seven files, at 06:39 and again at 06:40 after the non-ASCII fix, before this
  line was written): rc 0, `no leaks found`.

## CODEQL

Not run locally (the gate has no CodeQL step). Read on the pull request (`landing.txt` step 3); INFO 10.

## NOT RUN

Any run on Linux or Windows locally (the hosted legs of the head only; the merge with any main on the hosted legs is
not measured, windows succeeded 1787 on `5b66a7b1` PREDICTED); C7 (not this gate's; B1955 and B1961); the seat's
50-run loop (RELAYED, `LOOP: 50 of 50`); `run_step.py`'s neutral scan locally (the hosted secret-scan job ran it on the
head: every hardened row OK); the two publishes and `release_guard.py` locally (linux `GUARD: clean (10 files)` on the
head's push run; windows not reached on the head, PASS on main); `repo_rules.py --source-documents` (never); the merge
with the C7 fix lane's main (not on the origin at 06:36); anything against a tenant; CodeQL; any re-run.

## DEVIATIONS

None from the commission. Two notes: (1) one Bash call of mine tried a `cd` and one an unquoted `======`; both were
refused by the session's hooks before running and re-issued without them. (2) `pbase-restore` moved to the background
after 180 s of lock waits behind another holder; the next job (`pbase-build`) waited on the lock until it was released
(`gate.log`: restore lock taken 06:30:54, build 06:30:59), so the jobs still ran one at a time. (3) Tool slip: the Write tool turned the JSON escape text I typed in INFO 4 and
FOR-RECORDS item 5 (a surrogate pair and four BMP escapes) into the characters themselves; found by a non-ASCII scan
(two lines in each file), replaced by program with the ASCII escape text; every file of this folder now holds 0 lines
outside printable ASCII but the attribution line of `pr-body.md`.

## TREES LEFT

`g1960/clone` detached at `10f446f3`, status clean (mutants undone, rebuilt); worktree `g1960/red` at `49f686a8` with
both patches in its working tree (uncommitted, equal to the head); worktrees `g1960/phead` at `10f446f3` and
`g1960/pbase` at `49f686a8`, clean (the probe file moved out; its build output stays under `bin/`); worktree
`g1960/merged` at `5b66a7b1` with the head's diff staged (tree `a711478f`, never committed); `g1960/logs/**`,
`g1960/scratch/**` (`probe-head.txt`, `probe-base.txt`, `G1960Probe.cs`, `words/`, `gl-blobs/`, `mutants/`, helper
scripts), `g1960/_quarantine/{locks,gl-control,probes}`. No process left running; the wave lock not held by this
reader.
