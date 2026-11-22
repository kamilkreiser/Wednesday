GATE B1918: GO WITH FINDINGS @ ea72d92 on main bf6b441

Gate G2 (tests only), round 1, the one reader. OXPd 2, kit B1912 (seat X27): the F13 test-race fix, head
`ea72d92173e540b397589a774a25f15011f1cf58` on `b1912/f13-test-race` (ONE commit, parent = main
`bf6b441e30900127487145c3b65b29d8cc9eb5ea`). Read and measured 2026-11-22 20:16 to 20:28 AEDT (clocks by `date`), on
Opus 5.5, in my own clone `fleet/state/s310/g1918/clone` (made by the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity). Origin by `gh api -X GET` under the project GH_CONFIG_DIR, last read 20:28:24:
branch = ea72d921, main = bf6b441e, open pull requests 0, `compare main...ea72d921` ahead 1, behind 0, exactly the two
test files. No write to the project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted.

**BLUF.** The lane does what it says and only that. Two test files, no `src/`. Index-keyed answers do NOT weaken
F13's property; they make `late` mean what F13's name says (the timed-out call's answer), and both legal orders of
time-out versus first answer stay reachable. The seam is inert when unset and scoped to F13's scenario. RED FIRST
reproduced (whole solution `failed: 1`, that cell, its message; 20 of 20 red), GREEN reproduced (1579 / 0; 200 of
200 on each F13 name), the survivor `mCountFirst` as named, and my own broker mutant (the late answer kept) is caught
by both F13 cells. Hosted PASS re-read. Findings are Minor test gaps for the backlog, none blocking.

## FOUND

1. **Outside-the-frame question: does index keying hide a broker fault?** No. Read at source,
   `src/Datasec.Suite.Sessions/TokenBroker.cs`: the held grant changes only in `AcceptLocked` (`:481-489`), reached
   only with `error is null` (`:430-438`); a time-out sets `RefreshTimedOut` (`:403-406`) and hands the call to
   `DisposeWhenDone` (`:508-527`), which disposes a late answer. Under arrival order F13's `late` could be the LIVE
   call's answer (the hosted red); index keying makes `late` always call 0's, so the assertions after
   `firstRelease` ("late disposed", "held grant still Access(1)", no NewToken event) now test exactly the name's
   promise. Measured: mutant **mKeepLate** (scratch edit: `DisposeWhenDone` accepts the late answer through
   `AcceptLocked` instead of disposing it) -> Sessions assembly `Total: 75, Errors: 0, Failed: 4`: BOTH F13 cells,
   F11 and F05 late; message `after the late answer: the held grant is not the expected one` 2 times. Reverted by
   copy: sha256 `51815f4f...` and git blob `8a6c9703...` = the head's; `git diff ea72d921` rc 0; rebuilt, whole
   solution 1579 / 0.
2. **The seam when unset (`Fakes.cs` at head, `:65-94`).** With `BeforeAnswer` null no await is added, so `_held` is
   read synchronously as before; with `AnswerOfCall` null the old `Answer(cancellationToken)` is called (a
   synchronous throw still faults the async method's task, as before); `Answering` is a counter no other cell reads.
   The one behaviour change for every cell is record-then-count inside the lock, which only makes `Calls == n`
   imply call n-1 is readable. Seam set/read only at `RefreshBoundCellTests.cs:133`, `:136`, `:160`, `:162`; each
   cell's `Kit` owns a new `FakeRefresher` (`Support.cs:223`), so nothing leaks between cells. The whole solution is
   green at 1579 (one added case) with every other cell unchanged.
3. **Minor (test gap, the code is right by reading): one ordering is untested.** In both F13 cells the late answer
   arrives while call 2 is still in flight (`firstRelease` before `secondRelease`). No cell lets the late answer arrive
   AFTER call 2's answer was accepted. Backlog: a third `LateAnswerAfterTimeOut` variant releasing `secondRelease`
   first. Not a NO GO class: the lane's claim is the race fix, not that ordering.
4. **Minor (as the kit named it):** `mCountFirst` is a survivor (`Total: 75, Errors: 0, Failed: 0`), closed by reading
   (record, count and both reads share `lock (_sync)`).
5. **The review of the same wait:** the seat's eight rows and its F10 note agree with my reading (F15, F05 hang/late,
   F08, F09, E07, L01 each have one call in flight). I did not re-print each `file:line` of the seven unchanged cells
   by program beyond the `Answer =` grep (every other cell scripts `Answer` with one fixed or sequential answer).
6. **Seat's claims re-measured, all held:** tool hashes 9 of 9; patch shas at each column; numstat 32/2 and 43/16;
   75 added lines; commit message byte-equal to `commit-message.txt` (subject 233 bytes); hosted numbers. The seat's
   stray no-op `cd` deviation (STATUS DEVIATIONS) changed nothing: accepted.
7. **Instrument note (not a lane finding):** my first gitleaks control (an AWS-shaped key built from parts) did NOT
   fire (rc 0); a second control (a GitHub-token shape) fired (rc 1). Every scan below was run after the firing
   control. Both control folders are in `g1918/_quarantine/`.

## TESTED (MEASURED, all in my clone, every heavy job through the kit's `heavy.py` unchanged, 14 jobs, lock folders
moved to `g1918/_quarantine/locks/`, the project lock absent at the end; load1 4.18 to 9.22, waits only on load or lock)

- BASE: two files sha256 = THE CODE's BASE column; `ls-files` 500; `apply --check 1-red-first.patch` rc 0.
- `restore --locked-mode --force -p:NuGetAudit=false` CI=true rc 0, porcelain only the two patched files.
- RED (`1-red-first.patch` on BASE, shas `f622a1dd...` / `754828ca...`): build 0 W / 0 E; whole solution `total:
  1579`, `failed: 1`, `succeeded: 1574`, `skipped: 4`; the ONE `failed` line is
  `F13_the_late_answer_is_never_kept_when_the_timed_out_call_answers_after_the_second_call`; its message
  `F13 first answers last after the late answer: the held grant is not the expected one` count 1 (control `total:` 1);
  `guard won` 0 (not a hang). `loop-red runs 20 pass 0 fail 20 other 0 seconds 5`.
- GREEN (`2-index-keyed.patch` on top: `RefreshBoundCellTests.cs` `4d2c8884...`, `Fakes.cs` unchanged;
  `git diff --quiet ea72d921` rc 0, i.e. the working tree IS the head; control vs BASE rc 1): build 0 / 0; whole
  solution `total: 1579`, `failed: 0`, `succeeded: 1575`, `skipped: 4`. `loop-green-new runs 200 pass 200 fail 0 other
  0 seconds 40`; `loop-green-old runs 200 pass 200 fail 0 other 0 seconds 40`.
- `mCountFirst` (count moved before `lock (_sync)`; diff `67a68 >` / `75d75 <`): build 0/0, Sessions `Total: 75,
  Errors: 0, Failed: 0`; undone by copy, `cmp` rc 0.
- `mKeepLate`: as FOUND 1; undone and proved; rebuild; whole solution 1579 / 0 / 1575 / 4.
- `git diff --name-status BASE ea72d921`: exactly `M` the two paths; `merge-tree --write-tree bf6b441e ea72d921` rc 0,
  tree `7bf6924b...` = the head's tree, 500 entries.
- `repo_rules.py <clone>` (no option, `test ! -e g1918/1_Project_Definition` rc 0): `RULES-NOTE: R5 hash half NOT RUN`,
  `RULES: clean (500 files)`; `unittest discover build/tests`: `Ran 111 tests`, OK.
- `hosted2.py ea72d921... --total 1579 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111
  --hardened-scan` (run 45006189382, attempt 1, four jobs success, no other check run): every row OK, last line
  `HOSTED ea72d92173e540b397589a774a25f15011f1cf58: PASS`.
- `words.py --control` `CONTROL FIRED: 13 of 13`; over the 75 added lines and the commit message: `WORDS: clean (2
  files)`. gitleaks (after the firing control) over the added lines, the message and both head files as neutral
  `<n>.txt`: rc 0, `no leaks found`.
- Pull request 17's head `94fe6067` carries 8 distinct check names (linux, windows, secret-scan, rules twice each;
  Analyze actions/csharp/python; CodeQL), all success. Open code-scanning alerts on main: 0.

## NOT TESTED

- No local Linux or Windows run; no CodeQL locally (read on the pull request, landing step 3). No `dotnet publish` or
  `release_guard.py` locally (the hosted legs print `GUARD: clean (10 files)` / `(11 files)`; the seat ran both).
- The race's hosted frequency; whether main's next push run is linux green (landing step 6 reads it).
- `run_step.py` neutral scan of the commit (the hosted secret-scan job ran it on this head: OK rows above).
- The late-answer-after-acceptance ordering (FOUND 3).

## HOW

Clone `python3 -I g1918/gate/clone.py g1918/clone draft` (tools copied from `fleet/state/s310/d1912/gate/` by `cp -Rc`,
9 of 9 sha256 equal). Patches by `git apply` in the scratch clone; mutants by a program (`g1918/scratch/mk_mutant.py`)
and a heredoc, each undone by copying the saved file from `g1918/scratch/pre-mutant/` and proved by sha256 / `cmp` /
git blob. Logs: `g1918/logs/` (`g-red-test.log`, `loop-red/`, `g-green-test.log`, `loop-green-new/`,
`loop-green-old/`, `g-mcf-sessions.log`, `g-mkl-sessions.log`, `g-undo-test.log`, `hosted-head.out`, `hosted-head/`,
`words-landing.log`, `landing-gitleaks.log`, `squash-scan.log`). Scratch clone left at the head's content (two files
modified relative to its local BASE checkout, equal to `ea72d921`), build outputs in `bin/` and `obj/`.

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 223 bytes. `pr-body.md` (ends with the Claude Code line). `squash-subject.txt` 242 bytes, ends
  ` (#PRNUM)`. `squash-body.txt` ends with the `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` line.
  `landing.txt` in B1904's form: 8 check names; merge-ref totals 1579 both legs, succeeded 1575 / 1560, skipped 4 / 19,
  RULES 500, Ran 111, floor 111; step 6 requires main's push run to read linux PASS.
- `words.py` over the four message texts: squash subject, squash body and PR title clean (every class 0); PR body 6
  hits, all expected: `coordinator` 2 (the required "who decides" line) and 4 non-ASCII bytes (the required robot
  line, line 49). gitleaks over all five texts as neutral names: rc 0, `no leaks found`. `build/squash_scan.py` with
  the subject's `#PRNUM` replaced by `#18` and `squash-body.txt`: control `rc 1, found 2`, message `rc 0, found 0`,
  `SQUASH-SCAN: clean`.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks and CodeQL read as step 3 requires.
