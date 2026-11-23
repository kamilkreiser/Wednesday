STARTABLE: YES (only with Q1 and Q2 answered "a" in words at the stamp: Q1 keeps `undo-owed` print-only; Q2 reads "re-use the one-attempt password guard" as the read verb's structure and words over at most two password-bearing requests per register run)

# B2011 DRAFTER REPORT: lane W2, the lab wiring of lane W1's writes and the end-of-session undo list, seat Datasec/OXPd2-X59

Drafter B2011 (Opus, in-session, read-only toward the project and GitHub), 2026-11-23 22:47 to 23:41 AEDT. Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2011_SEAT-X59_oxpd2-w2.md` (86653 bytes, 263 lines), sidecar `.measured` beside it (`stamp_check.py`: 199 claims, 199 measured, rc 0). Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s319/d2011/` (below `<d>`). Gate tier G1, round 1 of 2 of lane W2.

## BLUF
- **What main holds to wire.** At main `e39396f9`, `Oxpd1WriteKind` has exactly two members, `RegisterSignInAgent` and `UnregisterSignInAgent` (first-run step 5's pair, from PR 41). The kit wires exactly those two. Nothing in the adapter changes (`checks_w2.py` check 3: the adapter, its tests and `contracts` are unchanged).
- **What is built (frozen in `1-red.diff` + `2-fix.diff`; six Lab paths, 1 A and 5 M):**
  - `oxpd1 write` makes ONE `WriteAsync` per run. It is a dry run unless `--execute` is given; the dry run opens no credentials file and makes no connection.
  - An executed register first makes ONE `GetAuthenticationAgentRecords` read. It refuses with exit 10 when a record already holds the same id (compared as a UUID) or holds an id it cannot read. This is gate B2008 FOUND 2's read-first: the printed undo can never remove an agent that was there before.
  - The run stops at the first 401/403, printing the read verb's own words. Those words now live in one shared constant; no second guard is added.
  - Every executed write is entered in the run folder's `undo-list.tsv` as `Pending` BEFORE it is sent, then rewritten with its end after. The undo command is printed.
  - `oxpd1 undo-owed <session folder>`:
    - reads the list in every run folder of the session and orders the writes by time;
    - keeps a register owed until an ANSWERED unregister of the same host and id comes after it;
    - names an unreadable line by its place only, never its content;
    - exits 11 when anything is owed or unreadable;
    - **sends nothing** (Q1 default: print-only).
- **A landed cell forced where the code lives.** My first prototype put the verb and the list in two new files. The landed cell L03 (`LabCertTests.cs:93`, `Assert.Equal(3, sources.Length)`) then went red: `Expected: 3`, `Actual: 5`. The frozen code is instead appended to the two landed files `Oxpd1Command.cs` and `LabFiles.cs`. L03 stays unchanged and still scans the new code for `X509Store`, `Process` and `Environment.` (D7/Q9; the first files are in `<d>/_quarantine/v0-separate-files/`).
- **Measured in a fresh `<d>/clone3` with the frozen patches:**
  - RED: Lab executable `Total: 168, Errors: 0, Failed: 22`. All 22 are red by an `Assert.` line, and every red cell is in `Oxpd1WriteTests`.
  - GREEN: whole solution `total: 2093`, `failed: 0`, `succeeded: 2089`, `skipped: 4` (BASE 2054 + 39).
  - Mutants: `MUTANTS: 14 of 14 MATCH, 14 of 14 undone equal`.
    - In the prototype run, 13 of 14 matched. The one DIFFER, `mNoReadFirst`, was red on more cells than my first guess (V05, V06 and V10 also count the read's request or the list file). I set its expected row to what it measured, before the frozen run.
  - After the mutants: rebuild 0/0, the Lab dll later than both mutated sources, the whole solution green again (2093/0).
  - Chain:
    - 34 of 34 lock files equal after the locked `--force` restore;
    - `0 Warning(s)`, `0 Error(s)`; whole solution 2093 / 0 / 2089 / 4;
    - `GUARD: clean (14 files)` and `(15 files)`, with no Lab file published;
    - `Ran 111 tests` OK;
    - `RULES: clean (648 files)`; ls-files 648.
  - Checks and scans:
    - `checks_w2.py` 8 of 8.
    - `WORDS: clean (2 files)`.
    - `B2[0-9]{3}` count 0 and 0. `words.py` itself only matches B1xxx (gate B2008 Info 7), so the kit adds this count.
    - gitleaks rc 0 over the clone and over the 11 neutral files; its control returned rc 1.
- BASE is main `e39396f91dbfba3c46cc43d7790adb59581d2853` (tree `4af54a4b`, the commission's). I read its hosted run with `hosted3.py`: `HOSTED ...: PASS` at `--total 2054 --rules 647` (run 45167272161; linux succeeded 2050, windows 2033). PREDICTED head: 2093 and 648 (windows succeeded 2072).

## Facts re-measured (instrument)
- Origin `main` = `e39396f9...` (`gh api -X GET` at 23:03 and 23:19; `clone.py ... draft` three times). Open pull requests 0. `matching-refs/heads/b2011` 0. `.tools/b2011` absent (`b2010` present: the records seat's).
- `CLARIFICATIONS.md` (798 lines, sha `a11df9be`), case-insensitive line counts: undo, dry run, dry-run, sign-in agent, RegisterAuthenticationAgent, execute, end-of-session, undo list, print-only and agent id are each 0. Controls: C-63 1, OQ-6 3, OXPd 145.
- `kam_rulings_today.sh` (19 lines, `<d>/scratch/rulings_today.txt`): each of those words 0; control OXPd 9.
- Nothing in this lane is the product owner's decision.
- `BACKLOG.md` (sha `e99360a8`): no owed item names the undo list or the lab write verb. The only `undo` hits are other subjects.
- The last real WRITE commands on the Lab paths are kit B2006's seat's, in `<project>/1_Project_Definition/Briefs/2026-11-23_B2006_STATUS.md`:
  - line 138: `git commit -F '<lane>/gate/commit-message.txt'`;
  - line 142: `git push origin HEAD:refs/heads/b2006/lh-lab-hygiene`, at 21:57:47.
  - Kit B2005's seat ran the same two in the `git -C '<clone>'` form.
  - The kit's two commands match these token for token, except the branch name.
- Lab executable at BASE: 129 cases. This is DERIVED (168 − 39), not run at BASE.

## D-decisions (all yours as coordinator)
- D1: `undo-owed` is print-only (Q1).
- D2: the guard is the read verb's structure and words, held in one shared constant (Q2).
- D3: the read before a register is the client's list read; ids compared as UUIDs; an unreadable id fails closed.
- D4: a dry run is the same command line without `--execute`.
- D5: `--pin` is required; no first contact, no tree GET.
- D6: the lab refuses `@` in an address and a control character in the name (gate B2008 FOUND 1 and 3, enforced at the lab only).
- D7: the code goes in the two landed files (because of L03).
- D8: new exit codes 10 and 11.
- D9: one commit.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS): does `undo-owed` send the undos?**
  - a (built): it sends nothing.
  - b: `--execute` sends every owed unregister, i.e. a batch of password-bearing requests in one run.
  - c: send only when exactly one undo is owed.
- **Q2 (STOP-CLASS): the password guard.**
  - a (built): the read verb's structure, over at most two password-bearing requests per register run (the read, then the write) and one per unregister, with the same words.
  - b: no read first. This goes against the commission's read-before-register.
  - c: a counter across runs. That would be a second guard, and it belongs to B1996 F16's shared component.
- Q3 to Q12, with defaults as in the kit: the list read; the dry run's folder; pin required; the lab's stricter record rules; the undo list per run folder; exit codes; code placement; level and windows (hard stop 03:30); the inherited pipe and blank-password limits (not this lane's); landing order with the records seat (either order).

## UNMEASURED / NEVER RUN
- Both hosted legs for this lane. The platform-sensitive cells are V04 (a 1 s time-out against a 3 s stub delay) and V11 (reading the list file inside the stub's handler).
- Every device answer.
- The seat's own steps: the `seat`-mode clone, the commit, `run_step.py`'s neutral scan on a commit, the push, the read-back, the hosted run of a lane head, and the rebase.

## Disclosure (no fence crossed; the edges)
- **Hook refusal.** `pretooluse_no_cd.sh` refused one of my Bash calls: a `shasum` read that I had written with a stray leading `cd /dev/null`. I re-issued the `shasum` alone; the hash read was the purpose, not the `cd`.
- **Two tool corrections before the frozen runs (old copies quarantined in `<d>/_quarantine/`):**
  - `mutants_w2.py`: `mNoReadFirst`'s expected cells.
  - `checks_w2.py` check 7: its first cut counted the landed channel's own sends and FAILED. It now counts added `src/` lines only, with the landed count (5) as a control.
- **I overwrote my first full sidecar.** The second measure pass wrote only the 33 manual rows over it. That partial copy is in `<d>/_quarantine/measured-partial`, and the final sidecar was regenerated whole (199 of 199).
- **Stagings and writes outside `<d>`:**
  - I made `git add` / `write-tree` stagings only in my own scratch clones (`<d>/clone2`, `<d>/clone3`; push URL `invalid://no-push`; no ref, no commit).
  - GitHub was read only with `gh api -X GET`, under the project's own `GH_CONFIG_DIR`.
  - The Write tool refused a report draft I tried to keep in scratch. This report is the only report file.
- **Not touched:** Source_Documents, key folders, the NAS library and credentials files. No Jira, no printer, no Azure.
- **Heavy jobs.** Every heavy job went through `heavy.py` and the wave lock. Load reached 19.92 while other drafters built; lock waits were 0 to 6. No other holder's lock was touched.
- **Shell form.** Several reads used short `python3 -I` heredoc programs (read-only).
