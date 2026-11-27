GATE B2145: GO WITH FINDINGS @ b3248f8 on main 0ca8c65

Gate G1, ROUND 1 OF 2 of lane OX-C kit 2 (part 1: the Universal Print registration, owed 54, 75 and 55 parts (2) to
(7)), one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, kit B2138 (seat X81; stamp S4: Q1 "a" part 1
and Q3 "a" the edits and mutants frozen, the two cells the seat's, each in words; Q2, Q4 to Q9 the defaults; S8 the
canonical heavy runner 31adedc8; every choice the coordinator's, none the product owner's). Head
`b3248f8c6fc2fbcff2dddd9b436c58653b8b3548` on `b2138/lane-c-kit2-uprint`, ONE commit, one parent = main
`0ca8c655ac99f6b9857f645fdd19c03dab23949b` (PR 57's squash; tree 8e3985c1 by gh api and by my clone). Main and the
branch did NOT move during the gate (gh api -X GET 11:43:29 and 11:53:58 AEDT; open pull requests 0 both times; open
code-scanning alerts 0 at 11:50:45). Read and measured 2026-11-27 from 11:42:40 to about 11:56 AEDT (`date`) in my
scratch `fleet/state/s333/g2145/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity; detached at the
head; the frozen mutants ran here) and the worktree `probe` (the head plus two probe files of mine,
`GateProbeB2145Tests.cs` (G1 to G7) and `GateProbeB2145KeyTests.cs` (G8 to G10) in the Universal Print tests, never
committed, never pushed; my probe mutants ran here). Every heavy job through the kit's `heavy.py` (my copy of the eleven
tools: 11 of 11 sha256 equal to THE TOOLS, heavy.py 31adedc8) and the OXPd wave lock, taken per job and released, one at
a time: 22 jobs, lock waits 0 each, 22 released lock folders in `g2145/_quarantine/locks/`, no other holder's lock or
file touched, the lock folder absent at 11:53:58. No process of mine left (`ps`: none under g2145; the one test host on
the machine is the B1839 gate's orphan of 2026-11-21, pid 2177, never touched).

**BLUF.** The head does what its three items ask. **T15 reaches the check under the lock on every run**: the seam runs on
the flight's own thread after the arrival check (`CloudDeviceTokenHolder.cs:293` to `:301` returns before it) and
before `Finish` takes `entry.Sync` (`:303`, then `:309`), with no timing; in shape 1 nothing else can refuse (no entry
is held, so the same-object branch `:316` is skipped; the entry is not removed), so the refusal is `:325`'s. **Shape 2
IS held on its own**: my probe G1 (shape 2 alone) turns red under `mUnderLockOnlyRemoved` with "expected
TokenAnswerRefused, nothing was thrown" (FOUND 2). **The seam changes nothing when null** (one property read, no lock,
no await; `InternalsVisibleTo` names only the Universal Print tests; no product reflection reaches it; 351/0 locally,
2431/0 locally and on both hosted legs). **No README sentence is wider than the code or the owed list's measurement**
on any path I measured: each "measured on macOS arm64" matches owed 55's words (and E4's "for the same registration"
matches the PR 17 reader's probe G10: one request id, 20 of 20); the key-failure exception holds for the key (K07), the
export and the signing call (my G8, G9, FOUND 4); **E5's "reached by no cell on macOS" is MEASURED true for both
catches** (a probe mutant that turns each catch into a throw leaves all 358 cells green; the control, the loader's
catch, reddens C01 and C02; FOUND 3). One wording point (FOUND 5, Info). **No landed cell changed but the two
summaries** (removed lines under `tests/` exactly 2, both summaries; each test file at the head = its frozen result
plus added lines only, removed 0). Pin and green: Universal Print `Total: 351, Errors: 0, Failed: 0` (my run), the
whole solution `total: 2431`, `failed: 0`, `succeeded: 2427`, `skipped: 4` (my run, 61 s); `MUTANTS: 2 of 2 MATCH, 2 of
2 undone equal` (my run of the frozen rows; each red set equal to the seat's); `HOSTED b3248f8c...: PASS` (my read;
control `--total 2432` FAIL 4). **One Minor finding, six Info. None blocks the landing.** Tuesday's points: (a) the seam
can be set only from an assembly named `Datasec.Suite.UniversalPrint.Tests` (FOUND 7, Info); (b) a throwing seam
leaves the flight unfinished until the holder is disposed, MEASURED (FOUND 1, Minor, a named limit for the records,
not a product defect); (c) K07's control is right against `Write`: one `Put` of one name per good registration, in a
store made fresh per bench (Info, no finding).

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (Tuesday's point b: a seam that throws).** MEASURED by probe G2 (green at the head, so each
   assertion below holds): with `AfterArrivalCheck` throwing, the first `GetAsync` has not finished after 2 s, a second
   `GetAsync` for the same id joins the same flight and has not finished after 1 s, the issuer was called once, and
   the answer handed to the seam is NOT disposed; `holder.Dispose()` then ends both calls with
   `ObjectDisposedException`, and the answer is still not disposed after it. Why: `RunFlightAsync` is started
   fire-and-forget (`CloudDeviceTokenHolder.cs:111`, `_ = RunFlightAsync(...)`); an exception from the invoke (`:303`)
   leaves the method before `Finish` (`:304`), so `flight.Done` is never set and `entry.Flight` stays set; `GetAsync`
   waits on `flight.Done` with the caller's token only (`:114`); only `Retire` (`Remove` or `Dispose`, `:217` to
   `:230`) completes it. The faulted task is unobserved. Reach: tests only (the seam is null outside them, no product
   code sets it; T15's two seams do not throw: one disposes, one calls `Invalidate` with a live id on an undisposed
   holder). A future cell whose seam throws (an assertion inside the seam is the likely way) and that awaits
   `GetAsync` without `Expect.Within`'s 10-second guard or without disposing the holder would hang that test
   executable (the family of owed 137 and 138: a test host that never ends). Not a hang today: no landed cell sets a
   throwing seam. Fix (records / a later round, no change needed to land): a sentence in the seam's summary ("a seam
   that throws leaves the flight unfinished until the holder is disposed"), or the invoke inside a `try`/`finally`
   that always reaches `Finish`. Proposed as an owed item (FOR-RECORDS.md PROPOSED 1).
2. **Info (shape 2 held on its own; the seat's H2 was DERIVED).** Probe G1 is T15's shape 2 alone (the shared object
   answered again, `Invalidate(id, first)` in the seam). At the head: green. Under the frozen `mUnderLockOnlyRemoved`
   (applied by `mutants_c2.py run` with my own rows file `scratch/probe_mutants.json`, row `pUnderLockOnlyRemoved`,
   the same OLD and NEW as the frozen row): red, "G1 shape 2 alone: expected TokenAnswerRefused, nothing was thrown";
   red beside it T15 (shape 1's message, as the seat saw) and my G3; nothing else (`Total 358 Failed 3`, undone equal
   True). So shape 2 is held by the check under the lock by itself. Beside it, a shape outside T15 that the same check
   holds: G3, a renewal while a live token is held whose answer is disposed in the seam: at the head the answer is
   not held, the caller is served the held token (the rule for a failed renewal, `:127`), and the next call asks the
   issuer again (3 calls, `BytesOf(3)`); under the mutant the caller is served cleared bytes ("G3 served is the held
   token: the bytes differ"). No landed cell covers G3 on its own; T15 kills the mutant, so no change is needed.
3. **Info (E5 MEASURED; the seat's D-2 confirmed).** The fix commit of PR 17 (`94fe606`, "... any failure of the chain
   build is not trusted") widened the chain-build catch from `CryptographicException` to `Exception`
   (`RegistrationKeys.cs:214` at the head) and added the catch around the first reads of the public key and the two
   validity dates (`RegistrationRecord.cs:164`): `git show 94fe606 -- src/`, the only `catch` lines changed. These are
   E5's two catches; the stamp S1's `249` (`InsideWindow`) and `276` (`SignatureBelowIssuerModulus`) are two other
   catches, each also returning false. "Reached by no cell on macOS", MEASURED on macOS arm64 by probe mutants that
   turn the catch into a throw: `pChainCatchThrows` (`Total 358 Failed 0`, red NONE) and `pFieldReadCatchThrows`
   (`Total 358 Failed 0`, red NONE); control `pLoaderCatchThrows`, the loader's catch (`RegistrationRecord.cs:149`):
   `Failed 2`, red `CertificateRuleTests.C01` and `C02`, so a reached catch does redden. Each undone equal True. "Each
   catch can only refuse": `:214` returns false (`IssuerNotTrusted`), `:164` returns null (`CertificateMalformed`).
   "which cell C01 reaches only on Linux" stays RELAYED (owed 54 and kit B1915; Linux not run here).
4. **Info (the kit's H7 named limit is now MEASURED).** Probes G8 (a key whose PKCS#8 export throws
   `CryptographicException`) and G9 (a key whose signing call throws, `SignHash` and `TrySignHash`): each
   `Assert.Throws<CryptographicException>` exact type, and the store lists no name; G10 (the internal factory returning
   null): `NullReferenceException`, nothing put (the public constructor's factory is `RSA.Create(2048)`,
   `RegistrationKeys.cs:180`, so G10 is the seam's reach only). E1 and the E3 key-failure bullet ("makes the key,
   exports it or signs the request ... nothing is put") hold on all three platform steps (macOS arm64).
5. **Info (README wording, E1).** "One exception to the first rule" sits in the bullet whose rule it means, but the same
   README numbers its attach checks 1 to 8 and says "the first rule that fails names the reason" (`README.md:54`,
   `:57` "1. the id parses"); a reader can take "the first rule" as rule 1. And "One exception" says there is only
   one: other platform calls outside any catch (the chain's set-up and its status and element reads,
   `RegistrationKeys.cs:199` to `:206` and `:220` to `:238`; `RegistrationRecord.Write` inside `Write` before the
   `Put`'s own `try`, `:323`) are not shown to throw on any path and not shown never to throw (UNMEASURED). Not wider
   on any measured path; a records note for the next touch of that bullet ("One exception to that rule").
6. **Info (kit and stamp drift, no effect on the head).** D-1: the Universal Print executable's BASE total is 349, not
   the kit's DERIVED 329 (four `[MemberData(nameof(FixtureNames))]` theories in `IppReaderTests.cs`, which the kit's
   count of `[Fact` plus `[InlineData` left out); the seat used its measurement (351 after), as the kit says. D-2:
   FOUND 3.
7. **Info (Tuesday's point a: who can set the seam).** `InternalsVisibleTo` of `Datasec.Suite.UniversalPrint.csproj`
   names one assembly, `Datasec.Suite.UniversalPrint.Tests` (the only `InternalsVisibleTo` line of that project, `git
   grep` at the head; the repository's `src/` holds 19 such lines, one or two per project, each naming a test
   assembly). `Datasec.Suite.Jobs` and `Datasec.Suite.Lab` reference the assembly but are not named, so
   they cannot see the seam. Reflection in product code: `BindingFlags`, `GetProperty(`, `GetField(`, `GetMethod(`,
   `UnsafeAccessor` over `src/` hit only the OXPd 2 generated runtime's public static enum fields
   (`Oxpd2Json.cs:147`, `Oxpd2QueryBuilder.cs:87`) and JSON `TryGetProperty` calls; none reaches this type. Named
   limit: no assembly of the repository is strong-named (`SignAssembly` on 0 lines), so `InternalsVisibleTo` admits
   any assembly of that simple name, the same reach as the landed internal key-factory constructor of
   `RegistrationKeys` and every other internal seam of the repository; code already running in the process can reach
   private members by reflection anyway.

**Tuesday's point c (Info, no finding).** `CreateRegistration` puts through `Write`, which calls `_store.Put(NameOf(id),
...)` once (`RegistrationKeys.cs:326`; one name, `uprint/<id>`) after the key, the export and the signing request
(`:67` to `:75`). Each `Bench` makes its own `StoreRoot` in a new folder under the system temporary folder
(`StoreRoot.cs:22`, a new GUID), and `ThrowingStore.ListNames` returns the inner store's list (`StoreRoot.cs:200`). So
`Assert.Single(control.Faults.ListNames())` proves one name per good registration in an empty store, and the two
`Assert.Empty` after a failing factory can fail (a put before the failure would list one).

## 1. THE KIT'S OWN GATE LIST

- **`BASE..head` read whole; `--name-status`:** four rows, all `M` (`CloudDeviceTokenHolder.cs` +7, the registration
  README +25 -5, `CloudDeviceTokenHolderTests.cs` +51 -1, `RegistrationKeysTests.cs` +26 -1; 109
  insertions, 7 deletions); `compare/main...b3248f8c` ahead 1, behind 0, 4 files (gh api 11:43:29). The two product
  files are their frozen results: `apply_c2.py ... check` prints `FROZEN` for `CloudDeviceTokenHolder.cs` (1a43d96a)
  and `README.md` (54e1b950). My own application of the ten frozen edits to BASE (each OLD once) gives the frozen
  sha256 of all four files (1a43d96a, 54e1b950, 88929d05, 6e83d33e), and each test file at the head minus its frozen
  result reads removed 0, added 50 and 22. `ls-files` 679 at the head (no file added).
- **The pin run and each mutant's reds.** My head runs: build `0 Warning(s)`, `0 Error(s)`; Universal Print `Total:
  351, Errors: 0, Failed: 0`. The frozen mutants, re-run by me (`mutants_c2.py run`, one call, rc 0, 11:46:16 to
  11:46:30): `mUnderLockOnlyRemoved` `Total 351 Failed 1`, red `CloudDeviceTokenHolderTests.T15` ("T15 an answer
  disposed between the two checks: expected TokenAnswerRefused, nothing was thrown"); `mKeyFailureTyped` `Total 351
  Failed 1`, red `RegistrationKeysTests.K07` ("Exception type was not an exact match / Expected:
  CryptographicException / Actual: RegistrationException"); both MATCH, both undone equal True; each mutant build `0
  Warning(s)`, `0 Error(s)` and rebuilt `Datasec.Suite.UniversalPrint.dll`. Equal to the seat's lines. Then a build and
  the whole solution: K07 and T15 green there, so no mutant binary was left.
- **T15 on every run; shape 2 on its own:** BLUF and FOUND 2. The red under the mutant is deterministic: no delay,
  no timer; the seam's dispose finishes before `Finish` is called on the same thread.
- **Whether the seam can change anything when null:** `AfterArrivalCheck?.Invoke(answer)` reads an auto-property once;
  null skips the call; the property is per instance (no static), so a seam set by one cell cannot reach another
  holder (my ten probe cells and T15 ran in parallel classes, all green). Every landed holder and limit cell (T01 to
  T14, L01) green at the head (351/0), the whole solution 2431/0, both hosted legs `failed: 0`.
- **README sentences against the code and the owed list:** E1 and E3 (55 (7)): FOUND 4 (true for key, export,
  signature) and FOUND 5 (wording). E2 (55 (6) and (3)) and E3 (55 (2) and (5)): owed 55's own measured words, each
  "measured on macOS arm64" (owed 55: "Measured by the readers on macOS arm64 only"); no rule reads a leaf's
  extensions (`Extension`, `KeyUsage`, `BasicConstraint` on 0 lines of the library's code, `git grep`, control
  `ChainPolicy` 1); "no public member returns" the private key is the class summary's own sentence
  (`RegistrationKeys.cs:12` to `:13`). E4 (55 (4)): the PR 17 reader's probe G10 (`2026-11-22_B1904_verify/evidence/
  ReaderProbeTests.cs:299`: one `request.Id`, two good certificates through two instances, 20 runs) printed "both
  accepted in 20; highest version 3" in that folder; its platform is the reader's (owed 55: macOS arm64), RELAYED.
  E5 (54): FOUND 3. E6 (75): the disposed-first forms are refused on arrival (my G7: an answer disposed before it
  arrives never reaches the seam, 0 seam calls, `TokenAnswerRefused`), and T15 reaches the check under the lock.
- **Whether ANY landed cell changed but the two summaries:** no. Removed lines of the diff: README 5 (the frozen
  widenings E3, E4, E6), `CloudDeviceTokenHolderTests.cs` 1 (`Cells T01 to T14`), `RegistrationKeysTests.cs` 1 (`Cells
  K01 to K06`); no helper file is in the diff.
- **The hosted run** (my read, `hosted3.py b3248f8c... --total 2431 --rules 679 --skipped-linux 4 --skipped-windows 21
  --unit 117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15`, no --wait, 11:50:13): run 45917554233,
  linux, windows, rules, secret-scan each completed success, `check runs beside the four: 0`; linux `total: 2431`
  (twice), `succeeded: 2427`, `skipped: 4`, `GUARD: clean (14 files)`; windows `total: 2431` (twice), `succeeded:
  2410`, `skipped: 21`, `GUARD: clean (15 files)`; rules `RULES: clean (679 files)`, `UNIT-TEST FLOOR: ran 117, floor
  117`; secret-scan both planted controls, `no leaks found`; last line `HOSTED b3248f8c...: PASS`, rc 0. Control
  `--total 2432`: `FAIL 4`, rc 1. `failed Datasec.` lines (colour codes stripped): linux 0, windows 0 (control:
  `Datasec.` 315 and 366; `UniversalPrint.Tests.dll ... passed` 2 and 2).

## 2. TUESDAY'S POINTS

(a) FOUND 7. (b) FOUND 1. (c) the paragraph after FOUND.

## 3. ADVERSARIAL BEYOND THE KIT (three or more shapes outside each property; each covered or a named limit)

- **P1** (disposed after the arrival checks: refused, never held, the next call asks again). G1 shape 2 alone: held by
  the check (FOUND 2). G3 a renewal with a live held token: the answer refused and not held, the caller served the
  held token, the next call asks again; MEASURED, red under the mutant (FOUND 2). G4 `Remove(id)` in the seam (a live
  answer): `NotFound`, the answer disposed, the next call asks again (2 calls). G5 `Dispose()` in the seam:
  `ObjectDisposedException`, the answer disposed. G6 an `Invalidate` with an OLD copy in the seam: nothing dropped,
  the answer held (`BytesOf(3)`). G7 an answer disposed before it arrives never reaches the seam. All green at the
  head (MEASURED, macOS arm64). H4 (an entry removed between the checks with a disposed answer): DERIVED as the kit,
  refused by `:325` before the removed branch; the mutant keeps that case. Named limit: an answer disposed by another
  thread between `:325` and `:342` is the same race the lock already closes for the holder's own paths
  (`Invalidate`, `Retire`, `DisposeLate` all take `entry.Sync`); an issuer that keeps and disposes its own answer
  without the lock is the README's existing limit ("An issuer that keeps a token it handed over and later disposes
  ... clears ... the held bytes").
- **P2** (the seam null changes nothing). Who can set it: FOUND 7. Instance, not static: no cross-holder reach. A
  seam that throws, or one that keeps the answer it is handed (it is the very object about to be held), is a test's
  own act: FOUND 1 and a named limit. Null path: one property read; landed cells green locally and on both legs.
- **P3** (a platform failure inside `CreateRegistration()` leaves as that exception, nothing put). G8 export, G9
  signature, G10 a null key from the internal factory: FOUND 4. An exception thrown by the store's `Put` stays
  `RegistrationException` (`StoreFailed`, `:328` to `:332`), outside E1's words (which name the key, the export and
  the request only); not changed by this lane.
- **P4** (each new README sentence no wider than the code or its measurement). E5 MEASURED (FOUND 3); E4's "the same
  registration" supported (section 1); E1's "first rule" and "One exception" (FOUND 5); every "measured on macOS
  arm64" has a macOS source; Linux and Windows UNMEASURED by the sentences' own words.
- **P5** (no landed cell changes; every landed cell green). Removed test lines 2 (the summaries), head = frozen plus
  added lines; 351/0, 2431/0, both legs `failed: 0`; the new cells use only landed helpers (`NewHolder`,
  `Expect.RefusedAsync`, `Expect.Within`, `FakeIssuer.Token`, `Bench(keyFactory:)`), none changed. T15's two holders
  each in their own `using`; K07's three benches each in their own `using`.

## SCANS

- **SCANS-1** (the head): gitleaks 8.30.1, control first (a token built by a program from two halves and random
  characters, never printed, in a new scratch folder: rc 1, then moved to `g2145/_quarantine/gl-control`);
  `gitleaks git <clone> --log-opts=0ca8c655..b3248f8c --redact --ignore-gitleaks-allow --exit-code 1`: `1 commits
  scanned`, `no leaks found`, rc 0; the 109 added lines and the commit message under neutral names `1.txt`, `2.txt`:
  rc 0, `no leaks found`. `words.py --control`: `CONTROL FIRED: 13 of 13`; `words.py` over the added lines and the
  commit message: `WORDS: clean (2 files)` (0 bytes outside printable ASCII); `B2[0-9]{3}` 0 and 0 (control: the kit
  counts 32). The commit message equals the kit's `commit-message.txt` (True).
- **SCANS-2** (this folder's texts) and **SCANS-3**: in `FOR-RECORDS.md`'s last section, after the texts were written.

## NOT RUN

CodeQL (kit FACTS 5: the C# extractor is x86_64; the pull request's own run is the check). The chain's restore with
`--force`, the two publishes and the release guard, `unittest`, `repo_rules.py` and `run_step.py`'s neutral scan
locally (RELAYED from the seat; equal on the hosted legs, my read: GUARD 14 and 15, `Ran 117 tests`, `RULES: clean
(679 files)`, the hosted neutral scan). Linux and Windows for any probe of mine (the hosted legs ran the head's cells
only). C01 on Linux reaching the field-read catch (RELAYED). Nothing was sent to, run on or read from any printer or
device; no Azure, no Jira, no person; no pull request, no push.
