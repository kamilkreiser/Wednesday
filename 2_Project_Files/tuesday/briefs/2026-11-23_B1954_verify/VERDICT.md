GATE B1954: GO WITH FINDINGS @ 5cdcb80 on main 49f686a

Gate G2 (README text plus one pinning half in an existing cell, no product code), round 2 of 2 of OXPd 2 lane F3 (kit
B1952, seat X42; Q1 to Q4 the coordinator's stamp S4, Q1 and Q3 in words, never the product owner's), the lane's one
reader, on Opus 5.5. Commission `2026-11-23_B1954_GATE_COMMISSION.md` read whole. Read whole as well: kit B1952 (lines
1 to 149 and 150 to 211, two pages), Tuesday's `2026-11-23_B1952_ANSWER-1_stale-rules-status.md`, the seat's STATUS
(264 lines, ends `READY B1952: 5cdcb806...`), gate B1949's VERDICT.md and FOR-RECORDS.md and its landing texts, gate
B1950's `landing.txt` (the form). Head `5cdcb8066a3ba32de4dcf3df9b231102b1bcdfe6` on `b1945/f3-readme-limits`, ONE
commit on round 1's head `6177b525` (parent read by `git log --format=%P`), which is one commit on `394fa997`.
Measured 2026-11-23 05:15 to 05:30 AEDT in my scratch `fleet/state/s313/g1954/`: `clone` (kit B1945's `clone.py ...
draft`: push URL `invalid://no-push`, no identity; detached at the head) and worktree `both` (main `49f686a8` with the
merge tree read in). Every dotnet job and test executable through the kit's `heavy.py` and the wave lock, one at a
time (lock waits 0 on every job, load1 1.4 to 6.7; never broke a lock). Origin by `gh api -X GET` under the project
GH_CONFIG_DIR at 05:25: main `49f686a8` (one parent `394fa997`, tree `89af052b`); branch `5cdcb806`; newest pull
request 29 (closed, merged); none open. No write to the project, GitHub or Jira; no push, no pull request; no `cd`;
nothing deleted (probe file and scanner control moved to `g1954/_quarantine/`).

**BLUF.** Both round-1 findings are CLOSED. The new Limits sentence is true in both orders, in time and after the
bound, on every path its scope words admit: L01's four forms are green at the head and each of the five mutants
reds exactly its cells with the kit's messages; my own probes measure two shapes L01 does not (P1: the old call is
a renewal of a held token, held first; P2: disposed first THROUGH the under-lock check `:318`, the path the sentence
names its order by), both as the sentence says. The late-answer sentence no longer says `GetAsync` makes a
registration nor that the old call "compares with the old one". Mechanics hold: two `M` rows on round 1, the lane's
four rows on `394fa997`, no `.cs` under `src/`, Data README and Data cell byte for byte, the message byte for byte the
kit's, the head's solution 1761 / 0, the head's push run green on every count, and **the merge with main `49f686a8`
is clean and runs `total: 1785`, `failed: 0`, `succeeded: 1781`, `skipped: 4`, `RULES: clean (553 files)`**. One
Minor finding, no change required to land: the sentence names the disposed-first order by the check under the
registration's lock, and no test in the suite pins that check (FOUND 1).

## FOUND

1. **Minor (test coverage of the clause the sentence is named by; not a false sentence; no change required to
   land).** `README.md:153` to `:157` at the head name the order by "when the later call's answer is checked under
   the registration's lock just before it would be held" (`CloudDeviceTokenHolder.cs:318` to `:324`) and end "(the
   tests assert both orders, in time and after the bound)". L01's disposed-first forms dispose the object BEFORE the
   later answer arrives (`CloudDeviceTokenHolderLimitTests.cs:95` to `:97`), so the refusal comes from the ARRIVAL
   check `:288` and `:318` is never reached. MEASURED: a scratch mutant of mine that removes ONLY the `:318` block
   (`gLockCheckOnly`, sha256 `85fc5ea6...` -> `bd87ad2d...`, restored `equal True`, rebuilt) leaves every test of the
   suite green (`Total: 352, Errors: 0, Failed: 3`, the three failures being my three probes only), while my probe P2
   (below) turns to `later answer HELD (no exception); next GetAsync calls 2` in both forms. So the `:318` check, which
   the landed bullet `:111` to `:112` names and this sentence names its order by, is guarded by no cell today (the
   kit's `mHoldDisposedAnswer` removes BOTH checks together, so it cannot tell; T12 goes through `:288` too). This is a
   gap that pull request 28 left, not one this lane adds, and the sentence is TRUE on that path (P2 at the head:
   `TokenAnswerRefused; next GetAsync calls 3 bytes3 True`, in time and late). "The tests assert both orders" is true
   of the two orders; it is not true of the under-lock branch of the second. For the backlog, the coordinator's: a
   cell that reaches `:318` (P2 needed the private entry lock held by reflection; the test folder has no seam for it).

## INFO

1. **"as it was when the call was made" (`README.md:106`) has a snapshot reading that is false; the reading the
   bullet fixes is true.** P3 (no `Remove`): call 1 times out, call 2 on the SAME state holds object B, call 1's late
   answer is B: `disposed False; served bytes2 True; calls 2` (kept: compared with what the state holds when the answer
   arrives, `:238`). Read as a snapshot of what the state held when the call was made (nothing), the sentence would say
   disposed. The bullet's own "holds at that moment" (`:105`) and "`Remove(id)` ends that state ... a later
   `GetAsync(id)` starts a new one" (`:107`) make "state" the per-id entry, which is the true reading. No change
   required; a later wording could say "the state that was current when the call was made".
2. **Two locks, one name.** "checked under the registration's lock" (`:154`) is the NEW state's lock (`:302`); the old
   call's dispose runs under the OLD state's lock (`:302` of its own `Finish`, or `:236` in `DisposeLate`). The README
   never says they differ, and that difference is why the H14 interleaving exists. The sentence names its order by the
   check, so it holds either way (kit R1, Q1 S4).
3. **The late disposed-first refusal (`L01 ... :98`, late) is seen red by no mutant on its own**: L01 is one `[Fact]`,
   `mHoldDisposedAnswer` stops it at the in-time form first (MEASURED: `L01 old call first in time the later call's
   answer: expected TokenAnswerRefused, nothing was thrown`). P2's late form under `gLockCheckOnly` shows the late
   shape does depend on the product's check. Not a truth gap.
4. **"one valid token object" (`:151`)** is not defined; the arrival check `:287` to `:290` includes "not disposed",
   and in the disposed-first order the object is disposed when the later answer arrives. Read, as the kit's R1 says,
   as the size and lifetime rules; with that reading every clause is true.
5. **The head's push run** 45050685757: workflow `completed success`; `rules` check run still `in_progress` with
   conclusion `success` and `completed_at 2026-11-22T17:39:48Z` at my 05:25 read (Tuesday ANSWER-1 accepted it). The
   pull request's run is the binding one; if its `rules` row sticks the same way, `pr_checks_wait.sh` may not see 8
   completed rows: read the job's log (landing step 3) and stop for the coordinator rather than re-run.

## THE CLAUSES AGAINST THE CODE AT THE HEAD (README `:106` to `:110`, `:151` to `:158`; holder `CloudDeviceTokenHolder.cs`, sha256 `85fc5ea6...`, unchanged since `394fa997`)

| Clause | Code | Verdict |
|---|---|---|
| R2 "The comparison is with the holder's state for the id as it was when the call was made" | `DisposeLate(entry, ...)` and `Finish(entry, ...)` take the entry the flight ran for (`:230`, `:265`, `:275`, `:282`, `:297`, `:300`) | TRUE (per-entry reading; INFO 1) |
| "`Remove(id)` ends that state (it then holds nothing)" | `:177` out of the map; `Retire` `:216` to `:218` (Removed, Held disposed, null) | TRUE (P1: `A disposed by Remove True`) |
| "a later `GetAsync(id)` starts a new one" | `:71` to `:75`; a caller on the removed entry loops `:84` to `:87` | TRUE |
| "an answer that arrives after the `Remove` to a call made before it is disposed, even when it is the object the new state holds" | in time `:297` -> `:328` to `:331`; refused and disposed `:287` to `:292`, `:318` to `:323`; late `:275` -> `:236` to `:241` against Held null | TRUE (L01 4 forms; P1; P2) |
| R1 scope "one valid ... one call made before it and one after, both answered after it and the later one within its bound" | excludes H13 (answer before `Remove`: held `:334` to `:337`, disposed by `Retire` `:217`) and H12 (later past its bound: `:275`, never held) | scope honest (DERIVED, as the kit's H12, H13) |
| "has it disposed by the old call's answer, in time or after the bound" | in time `:330` (entry Removed); late `:240` (old Held null) | TRUE (L01; P1 both forms; P2 both forms) |
| "If the object is not yet disposed when the later call's answer is checked under the registration's lock just before it would be held, the holder's new state for the id holds it" | `:318` passes, `:334` to `:337` on the new entry (not Removed) | TRUE (L01 round-1 halves; P1) |
| "so the id then serves cleared bytes" | `CopyOf` `:258` to `:259` copies `Held.Buffer` with no disposed check; `CloudDeviceToken.cs:62` zeroes it | TRUE (L01; P1 `id serves all-zero True`) |
| "if it is, that answer is refused `TokenAnswerRefused`, nothing is held, and the next `GetAsync(id)` calls the issuer again" | `:288` -> `:293`, or `:318` -> `:322`; `GetAsync` throws `:123` to `:124`; next call `:94` to `:105` | TRUE on both paths (L01 via `:288`; P2 via `:318`; FOUND 1) |
| "(the tests assert both orders, in time and after the bound)" | L01 `:17` to `:20` | TRUE of the orders; the `:318` branch unasserted (FOUND 1) |
| kept: "The holder does not check for any of these, and it hands out such cleared bytes until a renewal succeeds or the token's whole lifetime has passed." | `:89`, `:121` to `:122` | TRUE (unchanged words, reflowed) |
| H14 (dispose between `:318` and `:335`) | different locks; held then cleared = the first clause | covered by the wording (named by the check); NOT scheduled (no seam inside the lock) |
| L01 rename `...AndServedClearedOnlyWhenTheLaterAnswerIsHeldFirst` and the summary "in both orders of the two answers" | the four forms | TRUE |

**FOUND 1 of B1949 (Limits, one order stated for all): CLOSED** (both orders stated, each true). **FOUND 2 of B1949
(D2's words): CLOSED** (`git grep -c -F 'makes a new registration' 5cdcb806 -- src` finds nothing; "compares its answer
with the old one" is gone; the README's "a new registration is a new id" `:59` to `:60` no longer contradicted).

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `d1945/gate/` to `g1954/gate1/` and `d1952/gate/` to `g1954/gate2/`; `scratch/toolcheck.py`:
  `TOOLS 16 of 16`, `files gate1 12 gate2 4`. `words.py --control` `CONTROL FIRED: 13 of 13`.
- **THE COMMIT:** `git diff --name-status 6177b525 5cdcb806`: two `M` rows (the UP README `13 9`, the L01 file `45 2`);
  against `394fa997`: `M` Data README `4 1`, `M` UP README `13 4`, `A` Data cell `53 0`, `A` L01 file `104 0`.
  `scratch/headcheck.py`: the five files at the head equal THE CODE's after/kept sha256 (UP README 159 lines, L01 104,
  Data README, Data cell, holder `85fc5ea6...`), each printable ASCII; stored message equals `commit-message-r2.txt`
  byte for byte (278 bytes, subject 220 characters); 553 files at the head and in the merge tree. `f3r2_checks.py
  <clone> 6177b525...`: `CHECKS-R2: PASS, every control FIRED`; `f3_checks.py <clone> 394fa997...`: `CHECKS: PASS,
  every control FIRED`. The diff read whole (above).
- **GREEN at the head:** locked restore rc 0; build `0 Warning(s)` `0 Error(s)`; Universal Print executable whole
  `Total: 349, Errors: 0, Failed: 0`; after the mutants and probes (probe moved out, porcelain 0, rebuilt 0/0) the whole
  solution `total: 1761`, `failed: 0`, `succeeded: 1757`, `skipped: 4`; `repo_rules.py` (no `--source-documents`)
  `RULES-NOTE: R5 hash half NOT RUN ...`, `RULES: clean (553 files)`.
- **THE MUTANTS** (`scratch/drive_mutants.py`: the kit's programs unchanged; apply, build 0/0, the UP executable whole
  with no selector, undo `equal True`, `diff --stat` equal, REBUILD 0/0 after every undo):
  `mRemovedClearsOnly` `349 / 1`: L01 `L01 old call first in time the old call's answer disposes the object first: the
  guard of 10 seconds expired`. `mLateClearsOnly` `349 / 1`: L01 `L01 old call first late ... disposes the object
  first: the guard of 10 seconds expired`. `mHoldDisposedAnswer` `349 / 2`: L01 `L01 old call first in time the later
  call's answer: expected TokenAnswerRefused, nothing was thrown`, T12 `T12 a disposed answer: expected
  TokenAnswerRefused, nothing was thrown`. `mRemovedKeepsAnswer` `349 / 2`: L01 `L01 in time the old call's answer
  disposes the object the id holds: ...`, T08. `mLateKeepsAll` `349 / 3`: L01 `L01 late ...`, T06, T11. Each exactly
  THE CONTROLS; each apply's sha256 pair equal to the seat's STATUS.
- **MY PROBES** (scratch class `ZG1954UpProbes`, `scratch/probes/`, reporting by `Assert.Fail("PROBE ...")`, in no
  patch; built and run whole at the head through the lock: `Total: 352, Errors: 0, Failed: 3`, the probes only; then
  moved to `g1954/_quarantine/probes/`, porcelain 0, rebuilt):
  - P1 (held first, the old call a RENEWAL of a held token A): `in time: renewal caller NotFound; A disposed by Remove
    True; shared held by new state before old answer True; after old answer shared disposed True; id serves all-zero
    True; calls 3 || late: renewal caller served A's copy; A disposed by Remove True; shared held ... True; after old
    answer shared disposed True; id serves all-zero True; calls 3`.
  - P2 (disposed first THROUGH `:318`: the new entry's lock held by a thread of the probe, the later answer released,
    500 ms, then the old answer, then the lock let go): `in time: later call still waiting at the lock True; later
    answer TokenAnswerRefused; next GetAsync calls 3 bytes3 True || late: ... TokenAnswerRefused; next GetAsync calls 3
    bytes3 True`. Control that P2 reaches `:318`: under `gLockCheckOnly` both forms read `later answer HELD (no
    exception); next GetAsync calls 2 bytes3 False` (FOUND 1).
  - P3 (INFO 1): `disposed False; served bytes2 True; calls 2`.
  - H14 NOT scheduled: the window is inside the new entry's lock, between two lines of one method; no seam.
- **THE MERGE with main `49f686a8`:** `git merge-tree --write-tree 49f686a8 5cdcb806` rc 0, tree
  `fa7993532a6e826be54f56c70f9ee314dd43c1ee` (no conflict; `diff --name-status 49f686a8 fa799353` = exactly the lane's
  four rows; `394fa997..49f686a8` = seven Identity paths). In worktree `both` (`read-tree -m -u HEAD fa799353`, staged
  rows exactly the four): locked restore rc 0; build `0 Warning(s)` `0 Error(s)`; whole solution **`total: 1785`,
  `failed: 0`, `succeeded: 1781`, `skipped: 4`**; `repo_rules.py` `RULES: clean (553 files)`. The commission's
  1785 / 0 / 1781 / 4 / 553: HELD. Also `merge-tree --write-tree 10f446f3 5cdcb806` (lane A2-F2's pushed head) rc 0,
  tree `a711478f`, not built (MAIN MOVES).
- **HOSTED (GET only; nothing re-run):** head run 45050685757 `push completed success attempt 1`; check runs linux,
  windows, secret-scan `completed success`, rules `in_progress success` (INFO 5). Job logs read by
  `scratch/runlogs.py` (escape sequences allowed, colour stripped): linux `total: 1761` x2, `failed: 0`, `succeeded:
  1757`, `skipped: 4`, 0/0, `GUARD: clean (10 files)`; windows `total: 1761` x2, `failed: 0`, `succeeded: 1740`,
  `skipped: 21`, 0/0, `GUARD: clean (11 files)`; rules `Ran 111 tests`, `UNIT-TEST FLOOR: ran 111, floor 111`,
  `RULES: clean (553 files)`; secret-scan both PLANTED-CONTROL lines, `no leaks found` x3, `objects of this commit not
  among them 0`, NEUTRAL-EXPORT `wrong 0` x2, NEUTRAL-SCAN-REACH `not among the stored objects 0`. `failed Datasec.`
  lines: linux 0, windows 0 (control: the UP test assembly's `passed` line, 2 per leg). Main's push run 45048341660
  (`49f686a8`): linux 1783 x2 / 1779 / 4, windows 1783 x2 / 1762 / 21, RULES 551, Ran 111, floor 111, GUARD 10 and 11;
  CodeQL on main at `49f686a8`: csharp, python, actions results 0; open alerts on main 0. No code-scanning analysis
  exists for the branch (push runs have no Analyze rows): read on the pull request.

## SCANS

- `words.py` over the 58 added lines of `6177b525..5cdcb806` (`added.py`: `ADDED: 58`) and the head's message: every
  class 0, `WORDS: clean (2 files)`.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (`scratch/leakctl.py`,
  two halves and 36 random characters, never printed): rc 1, `leaks found: 1`, folder moved to `g1954/_quarantine/leak-ctl`;
  then `scratch/neutral/1.txt` (the added lines) and `2.txt` (the message): rc 0, `no leaks found`.
- The texts of this folder: FOR-RECORDS.md, last section.

## NOT RUN

Anything on Linux or Windows locally; the merged tree on the hosted legs (the pull request's run builds it); CodeQL
(read on the pull request); `run_step.py` locally (the hosted secret-scan ran it on the head); publish and release
guard locally (the hosted GUARD lines read); the seat's 10-run loop; H14 as a schedule; the merge with lane A2-F2's head
built (merge-tree only).

## DEVIATIONS

None from the commission. P2 holds a private lock by reflection and waits 500 ms of real time: scratch only, never a
pattern for the test folder. `gLockCheckOnly` is my own scratch mutant (`scratch/p2_control.py`), applied, restored
byte for byte (`restored equal True`) and rebuilt; never committed.

## TREES LEFT

`g1954/clone` detached at `5cdcb806`, porcelain 0 (mutants undone, probe moved out, rebuilt); worktree `g1954/both` at
`49f686a8` with tree `fa799353` staged (uncommitted); `g1954/logs/**`, `g1954/scratch/**`,
`g1954/_quarantine/{locks,leak-ctl,probes}`. No process left running; the wave lock not held by this reader.
