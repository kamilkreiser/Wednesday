NO GO
Covers pushlock_x6_newbranch_v3.sh sha256 b01fd4ddeef7aa05692f224056fad7ddd56037a8338d50e8be7afafd48ee8529 and the other 19 files listed in driver_built_x6.txt (all 20 matched at the start; the driver, decide and adopt re-matched at the end). A change to any listed file voids this. Gate 227, tier 1, round 1 of 2, 2026-11-06.

## BLUF

**Three blockers. Do not copy this to fleet/prerun/ and do not push with it yet.**

1. **The fast path cannot fire on any real branch today (F1).** `qualify` requires a `legs timed: 16/16` line. That line exists only in X 5th's unpushed KS-2047 commit, not in develop. Of 17 finished real hook outputs from today, 17 are refused on that rule; X 5th's own output, the control, qualifies. So every seat would pay a whole pre-run and then the hook anyway, and ADOPT would refuse all 25 queued seats. It fails safe, but it delivers nothing and would add load.
2. **An instrument error can reach `--no-verify` (F2).** An empty `prerun_decide_x6.py`, as a failed copy on a 98% disk would leave, exits 0 and prints nothing. The driver reads that as QUALIFIES and pushes with no hook and **no record at all**. Measured.
3. **ADOPT can wedge the whole queue, and v3 could not do this (F3).** If the old driver reaches its turn while ADOPT is waiting on the new driver, ADOPT SIGKILLs the lock holder and reports `ADOPTED`, rc 0. The stale lock stays and nothing clears it. Measured with the real V 24th driver.

**The ruling (question 1).** The side-by-side was done and it does match, but only partly in the form Kam asked for. See F7. I do not name it as a blocker of its own; it closes with the first step in question 8. The rule change has **not** landed: F6.

**What held.** Crash, hang, syntax error, pin failure, stale record, other sha, cell count and missing record all reach the hook. Killed-driver states are as the seat reports. ADOPT at 25 tickets kept the order. 5 of 5 reproduced tampers flipped. The real ssh wrapper works for a read. The bounds are a real improvement on v3.

## Findings

Evidence paths are relative to this folder. MEASURED AT RUNTIME was driven in scratch unless it says otherwise. Fix-shapes are prose only; I changed nothing.

### Blockers

**F1. Blocker. The fast path cannot fire outside KS-2047.** `prerun_x5.py:117-118`; `test_driver_x6.py:19` (fixture).
FOUND: `legs timed` occurs 0 times in `preflight.sh` at c5c26b283 and 35bcfa000, and at line 299 in e22ae8c215d4 (control). That commit is on one local branch only. Real hook outputs also have 0 leg rows.
TESTED: `qualify` over every finished real `push.out` from today's seats: 15 refused `legs_timed`, 2 refused `legs_timed,verdict` (real failures), 1 had no verdict. Control pre_normal.out: no reasons.
HOW IT HID: every arm's fixture is X 5th's output from its own timing commit, so "happy" has only ever passed on text no develop-based branch can produce.
ACTION: Wednesday chooses. Land KS-2047 by the normal hook first and pre-run only branches built on it, or have a seat drop the rule from the pinned tool, which needs this gate again. MEASURED AT RUNTIME for the refusal; the options are READ ONLY.
Evidence: evidence/q2_real_hook_output_vs_qualify.txt, evidence/q1_q2_reads.txt. No accident or malice needed.

**F2. Blocker. A decide that exits 0 without deciding gives `--no-verify`.** `pushlock_x6_newbranch_v3.sh:223`, `:51`.
FOUND: the driver tests only `drc -eq 0`. It never reads the word QUALIFIES or decision.json, and the helper check is `[ -f ]`. The sha pin covers prerun_x5.py and nothing pins decide itself.
TESTED: empty decide file and bare `sys.exit(0)`, each with no record: rc 0, path noverify, pushed, hook not run, no decision.json, empty PR line, status says "the pre-run record qualifies". Control, a syntax error, reaches the hook. Found by accident: a fault in my own arm truncated the file.
ACTION: fix-shape: require the positive statement (DECISION path=no-verify for this sha, matched in decision.json) and pin decide's sha in the driver; an arm for each. MEASURED AT RUNTIME.
Evidence: evidence/arms_batch3.out. Accident class.

**F3. Blocker for ADOPT. A race kills the lock holder.** `adopt_x6.py:72-83` (checks read once), `:133-142` (TERM, 15 s, KILL).
FOUND: nothing re-reads the holder or status before the rename or the signals. bash defers TERM during a push, so a holder in its hook always reaches the KILL.
TESTED: real V 24th driver behind one live ticket; that ticket leaves after ADOPT's checks, while the new driver prechecks (slowed to about 8 s; real precheck median is 11 s). Result: adopt rc 0 `ADOPTED`, old driver dead, holder names the dead pid, lock still present after the hook finished, new driver stuck silent at MY TURN. The push landed anyway. Everything behind waits for a human.
HOW IT HID: `AD_holds_lock` only tests a driver already holding the lock at check time.
ACTION: do not run ADOPT in the first round (question 7). Fix-shape: re-read turn and holder immediately before the rename and before each signal, and never KILL a pid named in the holder. MEASURED AT RUNTIME.
Evidence: evidence/arms_batch4_adopt_race.out. Accident class: it needs only the seat ahead finishing. The window grows as pushes get faster.

### Major

**F4. A stray `PRERUN_DISABLE` turns off any rule in production.** `prerun_x5.py:85`, `launch_driver_x6.py:37-38`.
TESTED: with `PRERUN_DISABLE=tip`, a record about another sha went `--no-verify`, hook not run, and the PR line says the checks ran "on 218fe055b70e, the commit pushed" when 1d12cd8538c8 was pushed. With `rc,verdict`, a FAILED record qualifies. Controls without the variable fall back and refuse. The launcher scrubs X6_ names only, and X 5th's test tool uses this knob.
ACTION: fix-shape: decide falls back if the variable is set at all, and the launcher scrubs it. MEASURED AT RUNTIME. Evidence: evidence/arms_batch1.out. An export in a seat's shell is enough; no malice.

**F5. The format gate is not a superset of the hook's.** `prerun_x5.py:69-70`. DRIVER BUILT line 30 says COVERED.
TESTED with the REAL `check-package-format.sh` at origin develop, two stub packages:
- touched package with no usable prettier and a red format:check: hook mode rc 1 REFUSED, `--all` rc 0 with a named SKIP. The hook would refuse and the pre-run passes.
- red UNTOUCHED package: hook mode rc 0, `--all` rc 1, which makes decide REFUSE with exit 5. Its comment "The hook would refuse it too" is false here.
The gate's output is discarded (`capture_output`), so the record and PR line show `rc 0 (--all)` and the SKIP is lost. The hook also passes `FORMAT_GATE_TREE`; the pre-run does not, which the seat's list leaves out.
ACTION: fix-shape: run hook mode against the branch's changed set and keep the output. MEASURED AT RUNTIME. Evidence: evidence/arms_batch2.out. Accident class.

**F6. The standing rule still forbids this.** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md:96`, quoted: "**No `--no-verify`, no force pushes, no `--admin`.** A gate that stops you is a question it is asking — answer it, do not route around it." Lines 418 and 438 also say never. 0 lines there name the pre-run (control: 54 lines name push).
Project rules: `Secuura/CLAUDE.md`, `Blockchain/CLAUDE.md` and `2_Project_Files/CLAUDE.md` have 0 hits for no-verify and 0 for hook (controls 1, 8, 12 for push). `.claude/skills/secuura-test-discipline/SKILL.md` has 0. `CONTRIBUTING.md:432-435` and the hook header allow it if the PR says so, naming legs. `DEV-PROCESS.md:175` says "never `--no-verify`" about a rate-limit case. The vault's skills have 0.
ACTION: Wednesday amends line 96 with a named exception before any real use; seats boot on it. READ ONLY.

**F7. The side-by-side matches, on narrower ground than the ruling reads.** My own uncapped re-diff of every run: residual 0 to 2 lines. Two at once: one `setpgid` line. Three at once: one KS-1401 postmaster warning. X 5th's printout capped at 14 lines per leg, so I re-read in full; nothing was hidden. The first pair was properly discarded by X 5th (SIGINT, 79 cells).
The limits:
- **Same commit is inferred, not proven.** No sha appears in the outputs or the design mail and the worktrees are gone. 3522 identical lines and 117 suites point to one commit, X 5th's timing commit.
- That commit is not on develop.
- **The tool was never in it.** The runs used `run_pre_x5.sh`. `prerun_x5.py run`, the path seats will use, has never run on the real repo, so its format gate never has either.
- "Normal" is that same script, not a push through the hook.
ACTION: one real tool run compared with one real hook run on one named sha. READ ONLY plus my re-diff. Evidence: evidence/q1_full_diff.txt.

**F8. Every real push will log NOT VERIFIED.** `pushlock_x6_newbranch_v3.sh:268-271`.
FOUND: `ls-remote > lsremote.txt 2>&1`. The `-v` wrapper now passes non-debug ssh lines to stderr, so awk reads four words.
TESTED: those exact lines over a real read: `LSSHA=[Authenticated / <sha> / Transferred: / Bytes]`, result NOT VERIFIED, origin holding that very sha. Control with stderr kept out gives the sha.
HOW IT HID: arms use a local path as origin (`test_driver_x6.py:52`), so ssh and the wrapper never ran in any driver arm.
ACTION: fix-shape: separate stderr, as lines 107 and 116 do. MEASURED AT RUNTIME, real ssh, read only. Evidence: evidence/q8_lsremote_line268.txt. A read-back that always alarms teaches seats to ignore it.

**F9. A tree changed during the pre-run and restored before its end qualifies.** `prerun_x5.py:62, 75`.
TESTED: tracked file edited mid-run, restored before the end: the check saw "EDITED MID-RUN", the commit holds "change", the record says clean and decide says QUALIFIES. Only the two ends are read. The hook shares this in principle, but the pre-run is about 20 minutes outside the lock with the seat free to keep working.
ACTION: fix-shape: at least a dated warning in the seats' lines; a periodic read if wanted. MEASURED AT RUNTIME. Evidence: evidence/arms_batch3.out. Accident class.

**F10. Nothing ties the pre-run to the hook's current contents.**
TESTED: a branch whose `.githooks/pre-push` carries a new refusal pushes `--no-verify`, hook not run, no sign. The real gap is any check added to the hook after this gate: the pre-run's list is fixed in prerun_x5.py.
ACTION: fix-shape: pin the hook's sha in the tool; a different hook falls back. MEASURED AT RUNTIME. Evidence: evidence/arms_batch1.out.

**F11. The PR line is false outside the clean path.** `prerun_decide_x6.py:106-111`, driver `:273`. Question 9.
TESTED:
- REAL hook, docs-only push: says "the hook ran the preflight"; it exited at line 372 with no preflight.
- `--no-verify` retries exhausted, rc 128, origin empty: "Pushed with --no-verify".
- Hook refused, rc 1, origin empty: "Pushed through the pre-push hook".
- Pin failure with a good hook push: the line reads "REFUSED: ...".
- Syntax error: the line is a traceback. Crash stub: empty.
- Reused OUT with a stale decision.json, hook ran: "Pushed with --no-verify".
The clean `--no-verify` line is accurate on legs and suites but silent on format-gate SKIPs (F5).
ACTION: fix-shape: write the line from the push result and the hook's own output, and write a plain "no line, read status" otherwise. MEASURED AT RUNTIME. Evidence: evidence/arms_batch2.out, evidence/arms_batch3.out. A reader cannot tell which case it has.

**F12. Kam's "at most 3-4 at once" is not enforced.** `prerun_x5.py:59`. `--slotdir` is optional, the seat's usage line omits it, and decide never checks. A killed pre-run also leaves its slot dir for good. READ ONLY.

**F13. The arms can pass for the wrong reason (question 6).** Fixture from a non-develop commit (F1), no ssh (F8), stub hook, no real format gate (F5). The arg tampers flip by usage error: `decide-arg-sha` flipped `no_hook` through `DECIDE ERROR rc=2`, not through any sha rule. No tamper or arm covers decide exiting 0 without deciding (F2). The tamper list covers the driver only.

### Minor

**F14. Forgery is cheaper than DRIVER BUILT says.** Editing three JSON fields (sha, sha_end, finished_utc) with the output untouched qualifies. The seat says record AND output together; X 5th's handover had it right. Malice or a hand-fix. A FAILED output with only rc edited still refuses. MEASURED.

**F15. REFUSE fires on non-failures.** `prerun_decide_x6.py:45-46`. A pre-run killed by signal (rc -15 or -9, "nothing failed") refuses at the turn and costs the place, after hours of waiting. No guard is lost. MEASURED.

**F16. The stated worst case under the lock is low.** The seat's 1,120 s omits the hook gate (180), the precheck (up to about 966) and decide (120). READ ONLY arithmetic: `--no-verify` about 2,506 s, hook path about 4,686 s (78 min). Still finite where v3 was not. `bound_x6.py` kills one group; a suite in its own group (`run-shell-suites` setpgid) may outlive the kill, unmeasured.

**F17. No heartbeat after MY TURN.** `pushlock_x6_newbranch_v3.sh:165` says a quiet file means stuck, which is untrue during a 20-minute hook. The F3 run's status stopped at "MY TURN after 0 polls". MEASURED.

**F18. One seat name for all.** `pushlock_x6_newbranch_v3.sh:41`. Shared from fleet/prerun/, every new ticket and holder says "Seat X 6th". MEASURED.

**F19. ADOPT's 15 s wait is thin.** `adopt_x6.py:113`. Real precheck over 98 status files: median 11 s, p90 12, max 21, 4 over 15. It refuses safely, but says the new driver "was stopped" while it is still live (TERM deferred), the retry then refuses on that pid, and driver.pid blocks the same outdir. MEASURED. Evidence: evidence/q7_real_precheck_times.txt, evidence/arms_batch3.out.

**F20. Small claims and leftovers.** The launcher "scrubs every one" misses `X6_ADOPT_WAIT`. Its TMPDIR `/private/tmp/x6t` is never created and the handover calls it safe to clear, so a cleared one meets the first fallback's preflight, unmeasured. It is also the seat's scratch folder. READ ONLY.

## Answers by question

**1. The ruling.** Done with limits, F7. The rule to change is STANDING_LINES.md:96, not changed, F6.

**2. Hook coverage.** My own list from the file:
- Refusals: non-fast-forward 62-81 (ALLOW_FORCE 77-79); format gate missing 311-319; sha not HEAD 351-359; format failed 329-334 via 363 and 365, including deps-absent REFUSED and NOTHING CHECKED in the script; preflight 393-400.
- Skips: empty, delete, notcommit, tagnobase, onremote 339-349; no Blockchain/Dev change 372.
The seat's line numbers and refusals match; the hook's bytes are identical at c5c26b283 and 35bcfa000. Its "COVERED" on the format gate is wrong, F5. "DROPPED" (docs-only) is sound but F5's second shape and F11's docs-only line follow from it. "NOT covered" is sound because of new-branches-only.
Between pre-run and push:
- Gitignored files: measured, a changed one still qualifies (arms_batch2.out). Same blind spot as the hook, but now up to 2 h old. The shared dist is the live case (STANDING_LINES:404).
- Develop moving: the develop gate handles overlap under the lock. Leg use of `origin/develop` (`check-no-demo-mutation.sh`, named at preflight.sh:794) reads a shared ref that is stale either way: the checkout read 1b1b65c74 while origin held 35bcfa000. Not measured.
- A merge that changes the cell count falls back every branch until the file is edited.

**3. Can it lie?** Other sha, dirty, other branch, other worktree, failed, truncated, edited count, stale: all refused. Lies I got: empty decide (accident, F2), `PRERUN_DISABLE` (accident, F4), mid-run edit (accident, F9), new hook check (accident, F10), three-field JSON edit (malice, F14). A symlinked or re-used out dir gained nothing: binding and the output hash hold. I read that rather than ran it.

**4. Fails safe?** Crash, hang, missing cells, unreadable record: yes. Exit 0 without deciding: **no**, F2. Failed record for another sha falling back is right: the hook then runs, so nothing is hidden.

**5. Bounds and lock.** F16, F17. The driver alone adds no new wedge: KILL under the lock matches v3 (re-measured, arms_batch2.out). ADOPT does add one, F3. W 29th's blind spot: better while queued, unchanged after MY TURN, worse under ADOPT.

**6. Tampers.** Five reproduced on my scratch: push-no-verify-dropped, decide-arg-sha, refuse-exit, pathsel-default, hook-push-no-verify, all flipped, coverage line reproduced (evidence/q6_tampers_reproduced.txt). Three of mine on decide (drop the checked-out-branch read, drop sha_end from about_this, drop the dirty read), all flipped against shipped (evidence/arms_batch2.out). Wrong-reason passes: F13.

**7. ADOPT.** Worst real outcome: F3, every seat behind wedged until a human clears the lock. At 25 tickets, position 13: 3.1 s in a shim world, order kept, old driver stopped, others untouched (arms_batch3.out). No network and one adopt at a time. **It should not run in the first round.** Today it would also refuse every queued seat under F1, and those seats cannot gain the timing line without a new sha. MEASURED AT RUNTIME for F3 and scale; "refuses every seat" is inferred from F1. The live queue read 26 tickets, all LIVE, at about 07:55Z, and 25 files at 08:06Z.

**8. The untested list.**
- Must run first: `prerun_x5.py run` for real on a named branch (F7), and `rehearse_push_x6_nb.sh` gatetest, which reaches the real gates with no push. It has never been run.
- Real ssh: done for a read by this gate: rc 0 in 4 s, 79 log lines per connection, about 6.7 KB, no leftovers (evidence/q8_real_ssh_read.txt). That found F8.
- Real hook under `bound_x6.py`: run one fallback before seats rely on it, since F1 sends everyone there.
- The first real push can answer: push over `-v` ssh, real "closed by remote host" text.
- Nobody can cheaply answer: the bound under a real stall. Accept it.
**Smallest safe first real use**, after F2, F4, F5, F6, F8, F11 are fixed and round 2 passes: the KS-2047 branch, the only one that can qualify. Merge develop in, do one real pre-run, compare it with a hook run on that sha, gatetest, one ticket, no ADOPT, origin read back by hand. READ ONLY as a recommendation.

**9. PR line.** F11. Truthful on the clean path only.

## NOT tested

- Real hook through a real push, the real 16 legs, `prerun_x5.py run` on the real repo. Forbidden or out of scope here.
- Any real push. Real overlap gate and `rehearse_push_x6_nb.sh` (read only).
- A real network stall. Concurrent ADOPTs. Many drivers at once. ADOPT with a real ssh precheck.
- The seat's full 83-tamper, 33-arm and 77-cell runs: sampled, 5 tampers as above.
- `test_driver_x6.py` read to line 250 plus its arm list and tail, not whole. QA charter read to line 80. `develop_gate.sh` and `overlap_gate.sh` not read; the seat's diffs not re-derived.
- Three-at-once load on today's develop.

## Conduct

- Scratch: everything ran under tmp/ and scratch/ here (42 MB, gitignored). Origin was a local bare repo. Controls: the guard refused the real queue path, the audit regex fired on a planted line, and worlds and origin URLs resolved inside tmp/. Audit over shim logs, per batch: 0 calls naming a real path (84, 237, 365, 49 calls).
- End state: no process names my scratch. Nothing in the seat's tools folder changed since the commission landed. No gate ticket in the real queue (0 of 25, control 25 of 25 name a seat). `refs/heads/feature/ks-test` absent at origin.
- Heads: origin develop 35bcfa000 at 07:49Z, 08:04Z and 08:06Z; shared checkout 1b1b65c74 on develop at the first and last read. The commission's c5c26b283 was already behind.
- **Reads outside the folder I should name.** Real `git ls-remote` of develop about six times, three of them through the seat's wrapper with the deploy key. These are read verbs on origin, a judgement call for question 8. I read `push_queue.sh list` once and the real lock's holder.
- **Mistakes of mine.**
  - One recursive glob over today's seat folders hit my 120 s limit and finished in the background.
  - First T3 arm moved a scratch `.git` away, so git walked up into the WEDNESDAY repo and ran read commands there, including `status` without `GIT_OPTIONAL_LOCKS=0`, which may have refreshed its index. Redesigned, not re-run; arms_batch1.out holds that superseded result.
  - Three arm faults corrected: a mid-run timing error, a truncating file write (which exposed F2), and a precheck slowed past ADOPT's wait.
  - One `symbolic-ref` was refused by the no-cd hook; replaced with a read verb.
- Load stayed 6 to 7. One suite at a time. Fixed nothing, posted nothing.
