GATE B1949: NO GO @ 6177b52 on main 394fa99

Gate G2 (documentation plus two pinning cells, no product code), round 1 of 2 of OXPd 2 lane F3 (kit B1945, seat
X41; Q1 to Q5 the coordinator's stamp S4, never the product owner's), the lane's one reader, on Opus 5.5. Commission
`2026-11-23_B1949_GATE_COMMISSION.md` read whole. Read whole as well: kit B1945 (lines 1 to 128 and 129 to 209, two
pages; S4 holds Q1 and Q3 in words), the seat's STATUS (207 lines, ends `READY B1945: 6177b525...`; its two
DEVIATIONS, a no-op `cd` subshell and two heading-vs-quote pointers, change nothing measured here), gate B1939's
VERDICT.md and gate B1943's VERDICT.md whole, B1943's `landing.txt` (the form). Head
`6177b525b127025988ae122a62184bc699a9b5f4` on `b1945/f3-readme-limits`, ONE commit, parent `394fa997` (= main).
Measured 2026-11-23 03:48 to 04:05 AEDT in my own scratch `fleet/state/s313/g1949/`: `clone` (by the kit's `clone.py
... draft`: push URL `invalid://no-push`, no identity; detached at the head) and worktree `both` (lane A2-F's pushed
head `a56ed63b` with this lane's merge tree read in). Every dotnet job and test executable through the kit's
`heavy.py` and the wave lock, one at a time (lock waits 0 to 14, load1 3.4 to 6.9; never broke a lock). Origin by `gh
api -X GET` under the project GH_CONFIG_DIR at 03:56: main `394fa997`; branch `6177b525`; `b1944/a2-f-card-store-follow-ups`
`a56ed63b`; newest pull request 28 (closed); `compare main...6177b525` ahead 1, behind 0, the four files. No write to
the project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted (probe files and the scanner control
moved to `g1949/_quarantine/`).

**BLUF.** Everything mechanical is as the kit and STATUS say: four paths (2 `M`, 2 `A`), no `.cs` under `src/`, the
commit message byte for byte the kit's, both cells GREEN at the head, each of the four mutants red on exactly its
cells, the whole solution 1761 / 0, the hosted run PASS at the head's own numbers, the merge with lane A2-F clean and
1785 / 0, words and gitleaks clean. The Data README's new sentence is TRUE, and my H3 probe now MEASURES the
interceptor form it calls "read from the code". **But the Universal Print README's two new sentences, the lane's whole
deliverable for part (b), are each wrong in a way the lane's own property forbids:** (FOUND 1) the new Limits
sentence is stated for every issuer that answers one object to a call made before a `Remove` and one made after, and
is FALSE in the order my H8 probe measured (the old call answered first: nothing is held, the new call is refused
`TokenAnswerRefused`, no cleared bytes are served); (FOUND 2) D2's sentence is true of the code but says
"`GetAsync(id)` makes a new registration for the same id", which the same README contradicts at `:59` to `:60` ("a
new registration is a new id") and `:24` to `:26`. Both are README text only: no code, no cell change. Round 1 of 2:
this goes back as a one-file fix round (the Universal Print README), with the cells and the Data README kept as they
are.

## FOUND

1. **Major for this lane (README accuracy in the lane's own new sentence; the lane's property (b) fails): the new
   Limits sentence is false when the old call is answered first.** `src/Datasec.Suite.UniversalPrint/Registration/README.md:150`
   to `:153` at the head: "An issuer that answers one token object to two calls for one id across a `Remove(id)`, one
   call made before it and one after, has it held by the id's new registration and disposed by the old call's answer,
   in time or after the bound, so the id then serves cleared bytes". Its subject covers every order of the two
   answers; its predicate holds only when the call made AFTER the `Remove` is answered first (H6, H7; L01). Kit H8
   (old call first) was DERIVED and "not named"; MEASURED here (probe P8 below, macOS arm64, at the head), both forms:
   `in time: shared disposed by the old call's answer True; the new registration's call answered the same object:
   RegistrationException TokenAnswerRefused; next GetAsync served bytes6; calls 3 || late: shared disposed by the old
   call's answer True; ... TokenAnswerRefused; next GetAsync served bytes6; calls 3`. The code: the old call's answer
   is disposed first (`CloudDeviceTokenHolder.cs:328` to `:331` in time; `:236` to `:241` late, against the old
   entry's `Held`, null after `Retire` `:216` to `:218`); the new call's same object then fails `answer.IsDisposed`
   (`:288`), is `TokenAnswerRefused` and `GetAsync` throws it (`:123` to `:124`, `Held` null); the next `GetAsync`
   calls the issuer again. So in H8 the object is NOT "held by the id's new registration" and the id does NOT "then
   serve cleared bytes". The error overstates the harm rather than hiding it (the behaviour is safer than the line
   says, and `:108` to `:110` already say a disposed answer is refused), so nothing unsafe is hidden; but the kit's
   property (b) is "every sentence of ... the Limits line is true of the code ... for one token object answered across
   a `Remove`, in time and after the bound", and this sentence is the lane's. It repeats exactly the defect gate B1943
   FOUND 1 was raised for (a sentence true in one shape, stated for all). **Fix sketch (DERIVED, text only; no code, no
   cell):** add the order, e.g. "... one call made before it and one after, when the call made after it is answered
   first, has it held by ... (the tests assert it, in time and after the bound); answered the other way round, the
   object is disposed before the later call's answer arrives, and that answer is refused `TokenAnswerRefused`." The
   second clause is my probe's, not a cell; whether to pin it (one more half in L01, +0 total) is the coordinator's.

2. **Minor (clarity of D2's sentence, the commission's own question): true of the code, but in this README's words it
   says something false.** `README.md:106` to `:108`: "The registration here is the one the call was made for: after
   `Remove(id)`, a later `GetAsync(id)` makes a new registration for the same id, and a call made before the `Remove`
   compares its answer with the old one only (see Limits)." TRUE of the code read as the holder's per-id entry:
   `DisposeLate` and `Finish` capture the entry the flight ran for (`:230`, `:275`, `:282`, `:300`), `Remove` takes it
   out of the map (`:177`) and the next `GetAsync` adds a new one (`:71` to `:75`). NOT CLEAR: this README defines a
   registration by its id ("`CreateRegistration()` makes the id ... one registration per (printer, flavour)", `:24` to
   `:26`; "a new registration is a new id", `:59` to `:60`), and `GetAsync` creates no id, key or record. Read with
   those lines, "`GetAsync(id)` makes a new registration for the same id" is false. Also "compares its answer with the
   old one only" implies a comparison that could keep the answer; after `Remove` the old entry holds nothing (`:216` to
   `:218`), so such an answer is always disposed (in time by `:328` to `:331` without any compare). D2's judgement
   (keep the per-call reading, not the gate's literal sketch) is RIGHT: L01 proves the id reading false. Only the
   wording needs to change. **Fix sketch (text only):** "The comparison is with the holder's state for the id as it
   was when the call was made: `Remove(id)` ends that state (it then holds nothing) and a later `GetAsync(id)` starts
   a new one, so an answer to a call made before the `Remove` is disposed, even when it is the object the new state
   holds (see Limits)."

## INFO

1. **The Data README's new sentence is true, and wider than it says (no change required).** `src/Datasec.Suite.Data/README.md:59`
   to `:62`. TRUE by `SuiteDbContext.cs:95`, `:110` (the pre-check before `base`), `:206`, `:212` (the watch while
   `saving`). Probes at the head (P1 to P3 below): a `SavedChanges` handler that catches a REMOVAL behaves the same
   (`state in catch Deleted; first save none; ... second save SuiteDataException AuditEntryChanged; rows 2; third save
   SuiteDataException AuditEntryChanged`); the tests assert only the change form (the README's "both" is the hide and
   the next refusal, not change and removal). Wider than "the next save": EVERY later save on that context is refused
   (P3: second, third and a synchronous save each `AuditEntryChanged`), and each refused append stays tracked `Added`
   (`tracker states Added,Added,Modified,Unchanged`). H11 MEASURED: a tracked read through that context returns the
   value never written (`tracked read ActorId user-9; no-tracking read user-1; query count user-9 0`), as "the entry
   stays modified in the context's tracker" implies. A caller's `AcceptAllChanges()` then makes the entry `Unchanged`
   and the next append fails `InvalidOperationException` (the refused `Added` entries accepted): a caller's own
   tracker manipulation, out of frame. An optional clause for the fix round, the coordinator's: "every later save on
   that context refuses it until its tracker is cleared, and a read through that context shows the unwritten value".
2. **H3 is now MEASURED, not only read (no change required).** P1: a `SaveChangesInterceptor` whose `SavedChangesAsync`
   (and, separately, `SavedChanges`) step catches around a change: `async: fired 1; caught 1; first save exception
   none; state Modified; after first rows 2; rows user-9 0; second save SuiteDataException AuditEntryChanged; after
   second rows 2; rows user-9 0 | sync: caught 1; first none; state Modified; second SuiteDataException
   AuditEntryChanged; rows 2; rows user-9 0`. The README's "read from the code and not asserted" stays honest (a probe
   is not a test); it could now say "measured once, not asserted", the coordinator's.
3. **L01 discriminates the reading D2 rejects.** A mutant that compared a late answer with the id's CURRENT entry
   would keep `shared` and turn L01's late half red by the same `Eventually` guard (DERIVED from `:238`); together with
   `mRemovedKeepsAnswer` and `mLateKeepsAll` the cell is not vacuous in either half.
4. **No mutant of the synchronous pre-check (`:95`) is in the kit**: the README says the synchronous path is read from
   the code, and my P1 sync form measured it once. Consistent; not a gap of this lane.

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `fleet/state/s313/d1945/gate/` to `g1949/gate/`; 12 of 12 sha256 equal to kit B1945's
  THE TOOLS (printed by `shasum -a 256`, each compared by eye and by name). `words.py --control` `CONTROL FIRED: 13 of
  13`.
- **THE COMMIT:** `git diff --name-status 394fa997 6177b525`: exactly `M src/Datasec.Suite.Data/README.md`, `M
  src/Datasec.Suite.UniversalPrint/Registration/README.md`, `A tests/Datasec.Suite.Data.Tests/AuditSavedChangesLimitTests.cs`,
  `A tests/Datasec.Suite.UniversalPrint.Tests/Registration/CloudDeviceTokenHolderLimitTests.cs`; no `.cs` under
  `src/`. `f3_checks.py <clone> 394fa997...` on the head's index: four files printable ASCII, 0 tab, 0 CR, final LF;
  `SRC rows: 2 only the two READMEs and no .cs: True` (control passes False); `NAME-STATUS rows: 4` (control passes
  False); `CHECKS: PASS, every control FIRED`. Parent `394fa997`; the stored message equals `commit-message.txt`
  byte for byte (302 bytes, `scratch/msgcmp.py`). The diff read whole: every README line against the code above
  (FOUND 1, FOUND 2, INFO 1); both cells read against `FakeIssuer`, `Expect`, `TestClock`, `TestKit` (`NewContext`,
  `NewContextWith`, `Count`, `Scalar`).
- **THE REQUIRED SECTION:** H1 MEASURED (the cell, its mutants). H2 MEASURED once by P1's sync form (not a cell). H3
  MEASURED (P1, INFO 2). H4 DERIVED, confirmed (no later save: nothing written). H5 confirmed (`AuditTests.cs:261`
  green at the head, red under `mNoStateChanged`). H6, H7 MEASURED (L01 and its mutants). **H8 MEASURED: contradicts
  the Limits sentence (FOUND 1).** H9 unchanged landed sentence. H10 DERIVED, confirmed by reading `:279` to `:285`,
  `:246` (nothing of the old call disposed but its own answer). H11 MEASURED (INFO 1). D2: true, not clear (FOUND 2).
- **GREEN at the head (`clone`):** locked restore rc 0; build `0 Warning(s)` `0 Error(s)`; Data `Total: 65, Errors: 0,
  Failed: 0`; Universal Print `Total: 349, Errors: 0, Failed: 0`; after the mutants and probes (moved out) and a
  rebuild, whole solution `total: 1761`, `failed: 0`, `succeeded: 1757`, `skipped: 4`.
- **THE MUTANTS** (`mutants_f3.py` unchanged, driven by `scratch/mutants_drive.py`: apply, build 0/0, the executable
  whole, undo `equal True`, `diff --stat` and porcelain equal, REBUILD 0/0): `mNoStateChanged` Data `65 / 8` (the new
  cell + `AuditTests` cells at `:115`, `:138`, `:171`, `:202`, `:239`, `:261`, `:277` by name); `mNoPreCheckAsync`
  `65 / 2` (the new cell, `C15_a_removed_entry_is_refused_and_nothing_changes`); `mRemovedKeepsAnswer` Universal
  Print `349 / 2` (L01 `L01 in time the old call's answer disposes the object the id holds: the guard of 10 seconds
  expired`, T08); `mLateKeepsAll` `349 / 3` (L01 `L01 late ...`, T06, T11). Each exactly THE CONTROLS. sha256 before
  and after each apply equal to STATUS's.
- **MY PROBES** (scratch classes `ZG1949DataProbes` P1 to P3 and `ZG1949UpProbes` P8, each reporting by
  `Assert.Fail("PROBE ...")`, in no patch; sources `g1949/scratch/probes/`; built and run whole at the head through the
  lock: Data `Total: 68, Errors: 0, Failed: 3` (the three probes only), Universal Print `Total: 350, Errors: 0, Failed:
  1` (the probe only); then moved to `g1949/_quarantine/probes/`, porcelain 0, rebuilt 0/0). Lines quoted in FOUND 1,
  INFO 1, INFO 2. P8 waits on `shared.IsDisposed` by polling (scratch only).
- **THE MERGE:** lane A2-F's pushed head `a56ed63bb2e39f6c9dbcdbdefd4eaf9dfdf07d07` (ahead of main 1, behind 0; seven
  paths, every one under `src/Datasec.Suite.Identity/` or `tests/Datasec.Suite.Identity.Tests/`, none of this lane's).
  `git merge-tree --write-tree a56ed63b 6177b525` rc 0, tree `b8c476f003648cbbf7e19a348f71d376c190c8e7`; in worktree
  `both` (`read-tree -m -u HEAD b8c476f0`, staged rows exactly this lane's four): locked restore rc 0; build 0/0;
  whole solution `total: 1785`, `failed: 0`, `succeeded: 1781`, `skipped: 4` (commission's both = 1785: HELD). This
  lane first is the head's own tree: 1761. A2-F alone 1783 is the commission's, not measured here. A2-F's head may still
  move: the merge must be re-measured against whatever lands.
- **HOSTED:** `hosted2.py 6177b525... --wait --total 1761 --rules 553 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan` at 03:58: run 45045255551 attempt 1, four jobs success; linux 1761 twice, succeeded
  1757, skipped 4, GUARD 10 files; windows 1761 twice, succeeded 1740, skipped 21, GUARD 11 files; rules RULES 553,
  `UNIT-TEST FLOOR: ran 111, floor 111`; secret-scan every hardened row OK; `HOSTED
  6177b525b127025988ae122a62184bc699a9b5f4: PASS`. `failed Datasec.` lines: linux 0, windows 0; the Data and Universal
  Print test executables `passed` on both legs.

## SCANS

- `words.py` over the 127 added lines of `394fa997..6177b525` and the head's message (`scratch/neutral/1.txt`,
  `2.txt`): every class 0, `WORDS: clean (2 files)`.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token shape
  built by `scratch/leakctl.py` from two halves and 36 random characters, never printed): rc 1, `leaks found: 1`,
  folder moved to `g1949/_quarantine/leak-ctl`; then the two neutral files: rc 0, `no leaks found`.
- The texts of this folder: last section of `FOR-RECORDS.md` names their scan.

## NOT RUN

Anything on Linux or Windows locally (the hosted legs of the head only; the merged tree with A2-F on the hosted legs is
not measured); `repo_rules.py` locally (the hosted `rules` job read 553); `run_step.py` locally (the hosted secret-scan
ran it on the head: PASS); publish and release guard locally (hosted GUARD lines read); the seat's 10-run loop; CodeQL
(no Analyze rows on a push run; read on the pull request); any H8 cell (a probe only).

## DEVIATIONS

None from the commission. My first probe build failed on the test project's own analyser (`xUnit1051`, a call without
`TestContext.Current.CancellationToken`) and was rebuilt with a file-level `#pragma` in the scratch probe files only.
One `grep -r` of mine was refused by the workspace's scope hook and re-run with `--include`. `git fetch` from my draft
clone is refused (no key, by design of `draft` mode); every later origin read was `gh api -X GET`.

## TREES LEFT

`g1949/clone` detached at `6177b525`, porcelain 0 (mutants undone, probes moved out, rebuilt); worktree `g1949/both` at
`a56ed63b` with tree `b8c476f0` staged (uncommitted); `g1949/logs/**`, `g1949/scratch/**`,
`g1949/_quarantine/{locks,leak-ctl,probes}`. No process left running; the wave lock not held by this reader.
