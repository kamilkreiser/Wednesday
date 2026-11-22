GATE B1950: GO WITH FINDINGS @ a56ed63 on main 394fa99

Gate G1 (security surface: the card-to-user mapping), round 2 of 2 of lane A2, one Opus reader. OXPd 2, lane A2-F, kit
B1944 (seat X40; Q1 to Q6 the defaults, Q1 and Q2 in words, each the coordinator's stamp S4, not the product owner's):
the card store's two owed Minors of gate B1941. Head `a56ed63bb2e39f6c9dbcdbdefd4eaf9dfdf07d07` on
`b1944/a2-f-card-store-follow-ups`, ONE commit, one parent `394fa997`. Read and measured 2026-11-23 03:49 to 04:10 AEDT
on Opus 5.5 in my own scratch `fleet/state/s313/g1950/`: `clone` (the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity; detached at the head) and three worktrees of it: `red` (main + `1-red.diff`, then +
`2-fix.diff`), `base` (main, for a probe), `merged` (a LOCAL merge commit `1805c319` of the head and lane F3's head
`6177b525`, never pushed). Every dotnet job through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock
`.tools/wave1-heavy.lock.d`, one at a time (lock waits 0 to 4, load1 2.1 to 6.9); no other holder's lock touched. Origin by
`gh api -X GET` under the project GH_CONFIG_DIR at 04:03: main `394fa997`; this branch `a56ed63b`; `b1945/f3-readme-limits`
`6177b525`; `compare main...a56ed63b` ahead 1, behind 0, merge base `394fa997`, 7 files; pull requests newest 28 (closed,
merged), none open. No write to the project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted (my
probe file and the scanner control moved to `g1950/_quarantine/`).

**BLUF.** Both owed Minors are closed as the kit says and the property holds on every path the commit names: every
exception either maker call throws, a cancellation of any kind included, ends `CodecFailed` with no request after it
and nothing written; every answer the store reads goes through the one parse and the whole-answer check before any
value is read, so a name held twice anywhere is `MalformedAnswer` and no user, count, schema pass or write follows. The
head is the two frozen patches byte for byte. Red first at main: 1783 / 24 failed, all Identity, all `Assert.IsType()
Failure` (6 naming the escaped cancellation, 18 `Value is null`); the head 1783 / 0; 44 of 44 mutants MATCH and undone,
rebuilt, green again; merged with lane F3's head 1785 / 0, RULES 553; the head's hosted run PASS; scans clean. **One
Minor finding, no wrong user and no write: the new whole-answer walk turns a name written with an invalid escape (a
lone UTF-16 surrogate such as `\uD800`) ANYWHERE in an answer into an untyped `InvalidOperationException` (FOUND 1).**
At main the same answer was read normally when that name sat in a part the store never reads; for a name inside the
set or a value the store reads it was already untyped at main. Nothing blocks the landing; FOUND 1 goes to the records
pass with its fix sketch, or back as a one-line fix round; that choice is the coordinator's.

## FOUND

1. **Minor (contract; fails closed, no wrong user, no write): the whole-answer walk widens an untyped exit.**
   `CsaReading.cs:163` reads `property.Name` for every property of every object (`CsaStore.cs:243`), and the .NET reader
   throws `InvalidOperationException` when it reads a name whose escape is a lone surrogate. `GetJsonAsync` catches only
   `JsonException` (`CsaStore.cs:250`), so the call ends in neither a typed result nor the caller's cancellation.
   MEASURED (probe P05x, macOS arm64, the head against main): a lone-surrogate name in an unread property of a search
   user, in another attribute set, or at the page's top level: head `OTHER System.InvalidOperationException, requests
   1`, main `RESULT Found userA`; the same in the user read: head untyped, main `RESULT attributes`; in the definition
   answer of the schema check: head untyped, main passes; in an enrolment's search answer: head untyped with 0 PATCH,
   main `Enrolled` with 1 PATCH. Already untyped at main and unchanged (carried, not this lane): such a name inside
   `HPAuthenticationSuite` (the set's own `EnumerateObject`) and such an escape in a VALUE the store reads
   (`displayName`: `GetString`); a value the store never reads stays harmless at both. Against the README's "Every
   call returns its typed result, or throws ... or the caller's cancellation" (`README.md:39` to `:41`) and the kit's
   required property ("whatever answer the Graph layer hands the store ..."). Reaching it needs Graph to send such an
   escape (UNMEASURED; RFC 8259 grammar admits it). Not killed by any cell. Fix sketch (DERIVED, not built): catch
   `InvalidOperationException` beside `JsonException` at `CsaStore.cs:250` (closes every name case, as the walk reads
   every name before anything else), plus one F13 row; the value case needs the reads of `CsaReading` (or the four
   callers' reads) inside the same typed catch, plus one R row.

## INFO

1. **D1 as built, measured wider than its cells (P07, head against main).** Prefix maker and blob maker, each throwing
   `OperationCanceledException`, `TaskCanceledException`, an `OperationCanceledException` carrying an already-cancelled
   token of its own, an `AggregateException` of one, or `InvalidOperationException`, in a find and in an enrolment (20
   shapes): head `TYPED CodecFailed` each, requests 0 (prefix) / 1 (find, blob) / 4 (enrol, blob), patches 0; main
   untyped for the 12 cancellation shapes. H8 (the caller's own source cancelled inside the maker, which then throws
   with the caller's token): head `CodecFailed` (find 1 request, enrol 4), main untyped: the kit's named limit holds as
   DERIVED. L04 (the caller cancelled before each of the four calls): `TaskCanceledException` as the Graph layer raises
   it, 1 request, head and main alike. Both maker calls are the only two (`CsaStore.cs:286`, `:303`); no
   `when (failure is not OperationCanceledException)` is left in the library (0 hits, 9 files).
2. **D2 as built: one parse, one check, every read after it.** One JSON parse in the library (`CsaStore.cs:242`), called
   by the set read (`:165`), the definition read (`:171`), the search (`:196`) and the user read (`:213`); the check at
   `:243` runs on `document.RootElement` before `Clone()` and before any `TryGetProperty`; the PATCH's answer is never
   parsed (`:140`; MEASURED H21: a PATCH answer holding a name twice, or not JSON at all, `Enrolled` with 1 PATCH). No
   second parse, no `JsonElement` read before the check, no value read through another API (the reads use
   `TryGetProperty`/`EnumerateObject`/`EnumerateArray` on the clone of the same checked document).
3. **The comparison is right (P05, head against main).** Names are compared after their escapes are read: `mail` then a
   fully escaped `mail`, and a name written once with a valid surrogate-pair escape and once raw,
   are each refused (main: `Found`). Case-only differences are NOT repeats and must not be: the store reads with the
   ordinal, case-sensitive `TryGetProperty`, so `Mail` beside `mail` and `CardID` beside `cardId` leave nothing
   ambiguous in what it reads (`Found userA` at both; `mRepeatedNameCaseless` reddens R01). Also refused at the head:
   the empty name twice, a name twice in an object inside an array in an unread place, `@odata.nextLink` twice (main
   read it `Ambiguous`). Depth: 60 levels in an unread place `Found`; 70 `MalformedAnswer` (the parser's default limit,
   a `JsonException`); the walk's recursion is bounded by the parser.
4. **D3 lost no case.** The removed set check enumerated exactly the names the walk now checks at that object, and every
   caller of `CsaReading.Set` reads an element that came through `GetJsonAsync` (`CsaStore.cs:205` by `User`, `:221`);
   the tests call `CsaReading` nowhere. F07 "a name twice" is green at the head and red under `mRepeatedNameTaken`,
   `mRepeatedNameShallow` and `mRepeatedNameArraysSkipped`; probe "cardId twice inside the set" `MalformedAnswer` at
   both.
5. **D4's cost, judged from the repository's own sources (no network).** Report A1 documents the search and read
   addresses (`A1:200`, `:204`) and no answer body; the design (`02`, `03`) and reports A1, A4, A6, A9 hold no answer
   shape with a repeated name (case-insensitive counts for `duplicate (name|propert|key)`, `name twice`, `repeated
   name`, `same name`, `odata.type`, `last-wins`: 0 on an answer shape; 2 unrelated lines). The one documented
   collection form (the store's own write and the fake: `cardId@odata.type` beside `cardId`) holds two distinct names.
   A refusal is `MalformedAnswer`, a typed failure, never `NotFound`, so it cannot turn a holder into an "unknown card"
   that is sent to enrolment (W10's target); its cost is a failed sign-in or enrolment for the holders of that one
   card's prefix, fail closed. Whether Graph ever repeats a name: UNMEASURED (owed item 6, the integration run).
6. **README sentences, at the head, each against the code.** `:34` to `:35` ("not handed the caller's token ... a
   cancellation included, is `CodecFailed` too (`CsaStore.cs:288` and `:305`)"): true; `ICardBlobCodec` takes a card and
   a mail only; `:288` and `:305` are the two `catch (Exception)`. `:41` to `:45`: "a name twice ... any object, at any
   depth" true (INFO 3); "names compared ordinally after their escapes are read" true; "every answer the store reads
   ... one parse, `CsaStore.cs:242`" true (INFO 2); "before anything of it is read (`CsaStore.cs:243`,
   `CsaReading.cs:155`)" true. The class comments (`CsaStore.cs:17` to `:18`, `CsaReading.cs:9` to `:13`) say the same;
   "`TryGetProperty` answers the LAST of names held twice" is the .NET reader's behaviour as MEASURED by gate B1941 P05
   and again here at main (`mail` twice, `id` twice: the last one read). The unchanged general sentence of `:39` to
   `:41` is the one FOUND 1 contradicts. The seat's own observation stands: the README states D4's cost only through
   "any object, at any depth" and does not say that Graph's sending one is UNMEASURED; S4 asked for the cost "as the
   kit writes it", and the frozen patch is the kit's text, so this is a wording note, not a finding.
7. **Cosmetic (the seat named it):** `FindTests.cs:240` `Exception thrown =kind == ...` (no space after `=`); builds
   `0 Warning(s)`.
8. **CodeQL:** two unfiltered `catch (Exception)` around a handed-in object (`CsaStore.cs:288`, `:305`); the rest of
   `src/` already holds 32 unfiltered `catch (Exception)` lines (grep at the head, these two and one filtered line
   excepted) with 0 open alerts on main (GET, 04:04), so no new alert class is DERIVED; read
   on the pull request (landing.txt step 3).

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `fleet/state/s313/d1944/seat-tools/` to `g1950/gate/`; 10 of 10 sha256 equal to kit
  B1944's table (printed in one `shasum` call). `words.py --control` `CONTROL FIRED: 13 of 13`.
- **THE COMMIT against its kit:** parent `394fa997` only, `rev-list --count` 1; the stored message byte-equal to
  `commit-message.txt` (299 bytes); `--name-status` exactly seven `M` rows, the owned paths (control: a planted `A` row
  fails the check); numstat 39/6, 9/3, 8/3, 29/0, 74/0, 25/0, 25/0; the SHARED FILES `diff --quiet` rc 0 (also over
  `Fakes.cs` and `LimitTests.cs`), control over `src/Datasec.Suite.Identity` rc 1; public lines added or removed 0,
  control 2; `ls-tree` 551 files at both; the seven blobs printable ASCII, no tab, no CR, final LF (control 1);
  Fact/Theory/InlineData per test file 5/6/15, 6/7/48, 2/5/18, 2/4/12, column 1 0 (equal to the kit). D1, D2, D3 read
  whole (FOUND, INFO 1 to 4).
- **THE PATCHES = THE HEAD:** in worktree `red` (main + `1-red.diff`): `git diff --stat a56ed63b` lists only the three
  product files; after `2-fix.diff` it is empty.
- **RED FIRST at main `394fa997`:** locked restore rc 0; build `0 Warning(s)` `0 Error(s)`; whole solution `total: 1783`,
  `failed: 24`, `succeeded: 1755`, `skipped: 4`; 24 `failed Datasec.` lines, 24 Identity; per cell E11 2, F12 6, F13 9,
  K06 3, R07 4; `Assert.IsType() Failure` 24 (18 `Value is null`, 3 `OperationCanceledException`, 3
  `TaskCanceledException`); `NotImplementedException` 0, `TimeoutException` 0.
- **GREEN, the head (clone):** `CI=true` locked restore `--force` rc 0; build 0/0; whole solution `total: 1783`, `failed:
  0`, `succeeded: 1779`, `skipped: 4`, `Passed!`.
- **THE MUTANTS:** `mutants_a2f.py <clone> <keep> run g1950 'B1950 gate'` as ONE call: 44 rows, every row `Total 112`,
  `MATCH`, `undone equal True`; last line `MUTANTS: 44 of 44 MATCH, 44 of 44 undone equal` (the seat's 44 rows,
  row for row). After it: status clean; build 0/0 with the library's dll at 03:56:10 after the last restored source at
  03:55:07; whole solution again 1783 / 0 / 1779 / 4.
- **MY PROBE** (`G1950Probes.cs`, one fact, 56 shapes, outcomes only, no value printed): in `red` (= the head) built 0/0
  and run whole `Total: 113, Errors: 0, Failed: 0`; in `base` (main) built 0/0 and run whole `Total: 89, Errors: 0,
  Failed: 0`; outcome files `g1950/scratch/probe-head.txt` and `probe-base.txt`; their diff is FOUND 1 and INFO 1 and 3.
  The probe file then moved to `g1950/_quarantine/probes/`.
- **THE MERGE:** main is `394fa997`, the branch's own base, so landing first is the head's tree `89af052b`. Lane F3's
  head `6177b525` (4 paths: two READMEs under Data and UniversalPrint/Registration, one new test file in each of their
  test folders): `git merge-tree --write-tree a56ed63b 6177b525` rc 0, tree `b8c476f0`, no conflict; in worktree
  `merged`: locked restore rc 0; build 0/0; whole solution `total: 1785`, `failed: 0`, `succeeded: 1781`, `skipped: 4`;
  `repo_rules.py` `RULES: clean (553 files)`. The head alone: `RULES: clean (551 files)`. Both with `RULES-NOTE: R5 hash
  half NOT RUN (no supplied-source folder here)` (never `--source-documents`).
- **CHECKS:** `boundary.py` `required: _graph.SendAsync( 2, HttpMethod.Patch 1, GetElapsedTime( 1, HttpMethod.Get 1`,
  `BOUNDARY: clean (9 files)`; its control `CONTROL FIRED: 33 of 33`.
- **HOSTED:** `hosted2.py a56ed63b... --total 1783 --rules 551 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor
  111 --hardened-scan` rc 0: run 45045417543, attempt 1, four jobs success; linux 1783 twice, succeeded 1779, skipped 4,
  GUARD 10 files; windows 1783 twice, succeeded 1762, skipped 21, GUARD 11 files; RULES 551, `Ran 111`, floor 111; every
  hardened secret-scan row OK; `HOSTED a56ed63bb2e39f6c9dbcdbdefd4eaf9dfdf07d07: PASS`. Main `394fa997` with `--total
  1759 --rules 551`: run 45040156344, four jobs and three Analyze rows success, `HOSTED 394fa997...: PASS`.

## SCANS

- `words.py` over the 209 added lines of `394fa997..a56ed63b` and the head's message (`scratch/words/1.txt`, `2.txt`):
  every count 0, `WORDS: clean (2 files)`. Over `squash-subject.txt`, `squash-body.txt`, `pr-title.txt` of this
  folder: see the last lines of this section.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token-shaped value
  built by program from two halves and 36 random characters in a new scratch folder, never printed): rc 1, `leaks found:
  1`, folder moved to `g1950/_quarantine/gl-control`; the seven head blobs, the message and the two words files as ten
  files in a new folder: rc 0, `no leaks found`.
- `words.py` over `squash-subject.txt` (222 bytes), `squash-body.txt` and `pr-title.txt` (167 bytes, under 256):
  every count 0, `WORDS: clean (3 files)`.
- `build/squash_scan.py <subject with #29> squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from main
  `394fa997`'s build/): control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks over this verdict folder (seven files, at 04:08, before these last lines were written): rc 0, `no leaks
  found`.

## CODEQL

Not run locally (the gate has no CodeQL step). Read on the pull request (`landing.txt` step 3); INFO 8.

## NOT RUN

Any run on Linux or Windows locally (the hosted legs of the head only; the merge with lane F3 on the hosted legs is
not measured, windows succeeded 1764 PREDICTED); the seat's 50-run loop (RELAYED, `LOOP: 50 of 50`; my runs: whole
solution 4 times, the Identity executable twice for the probe, 88 mutant jobs); `run_step.py`'s neutral scan locally
(the hosted secret-scan job ran it on the head: PASS); the two publishes and `release_guard.py` locally (the hosted
legs' `GUARD:` lines: PASS); `repo_rules.py --source-documents` (never); anything against a tenant; CodeQL.

## DEVIATIONS

None from the commission. Two notes: (1) my first `boundary.py --control` call omitted the clone argument and printed
`BOUNDARY: 4 problems` over 0 files (a usage slip, not a result); the correct form printed `CONTROL FIRED: 33 of 33`.
(2) My first `git worktree add` for the merge named a wrong sha and the next heavy job failed before its command ran
(no folder); `heavy.py` released the lock in its `finally` (the lock folder absent, checked), and the job was re-run
under a new label against the real local merge commit `1805c319`.

## TREES LEFT

`g1950/clone` detached at `a56ed63b`, status clean (mutants undone, rebuilt), plus the LOCAL commit `1805c319` (the
merge with `6177b525`; push URL `invalid://no-push`, never pushed); worktree `g1950/red` at `394fa997` with both
patches in its working tree (uncommitted, equal to the head); worktree `g1950/base` at `394fa997`, clean; worktree
`g1950/merged` at `1805c319`, clean; `g1950/logs/**`, `g1950/scratch/**` (`probe-head.txt`, `probe-base.txt`,
`words/`, `gl-blobs/`, `mutants/`, helper scripts), `g1950/_quarantine/{locks,gl-control,probes}`. No process left
running; the wave lock not held by this reader (absent at 04:08).
