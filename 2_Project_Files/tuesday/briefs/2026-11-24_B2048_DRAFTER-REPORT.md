STARTABLE: YES (only with Q1 and Q2 answered "a" in words at the stamp: Q1 admits exactly `IsServiceEnabled`, by name, as the one read whose name does not start with `Get`; Q2 makes an enable on a service already on write nothing, owe nothing and exit 0)

# B2048 DRAFTER REPORT: lane L1, first-run row 2 (the OXPd 1.x Test service on and off and one panel capture), seat Datasec/OXPd2-X63

Drafter B2048 (Opus, in-session, read-only toward the project and GitHub), 2026-11-24 15:26 to 16:45 AEDT. Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2048_SEAT-X63_oxpd2-l1-test-service.md` (93861 bytes, 288 lines), sidecar `.measured` beside it (`stamp_check.py`: 243 claims, 243 measured, rc 0). Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s323/d2048/` (below `<d>`). Gate tier G1, round 1 of 2 of lane L1. Seat id X63: an underscore-aware word scan over the 209 non-`.pre-`, non-`.measured` SEAT kits of 2026-11-17 to 2026-11-24 found X63 in 0 kits (control X62: 3 kits); `tmux list-panes` showed no `Datasec/OXPd2` pane.

## BLUF
- **Built (frozen in `1-red.diff` + `2-fix.diff`; 15 paths, 2 A and 13 M):** the four L1 folders of sweep section 3, plus `src/Datasec.Suite.Lab/README.md`, which no lane's list names.
  - **The widening.** The read-only check of `Oxpd1Read.cs` keeps its three rules and widens ONE. A name now has the form of a read when it starts with `Get` OR is exactly `IsServiceEnabled` (`NonGetRead`).
  - **Why that name:** HP's text says the Test service answers it while the service is off, and the contracts README names it as the read before `EnableService`.
  - **No other non-`Get` name passes.** T01 runs the rule over all 51 non-`Get` operation names of the 7 committed bindings (78 operations), plus near names. T02 plants each of the 51 in BOTH the allowed list and a row; only `IsServiceEnabled` passes.
  - **Red-proofs:** `mIsPrefixWidened` (admit every name starting `Is`) turns T01 red and nothing else; `mReadFormDropped` turns T02 red and nothing else. `checks_l1.py` check 10 reads the staged set: it has one non-`Get` member, the constant, and the constant is `IsServiceEnabled`.
  - **The client** reads `IsServiceEnabled` and `GetScreenCapture`. HP's answer element for `IsServiceEnabled` is `enabled`, so each row gains a `ResultElement` field; T06 proves the generic `IsServiceEnabledResult` shape is refused. The client writes `EnableTestService` and `DisableTestService`: empty bodies, validated against the committed `test.xsd`. The disable is the enable's undo.
  - **The lab write.** `oxpd1 write --write EnableTestService` is a dry run unless `--execute`. Executed, it makes ONE `IsServiceEnabled` read first:
    - service already on: nothing written, no undo owed, exit 0;
    - read refused: exit 6;
    - any other end, or a non-boolean answer: exit 8;
    - otherwise the landed path: list entry, ONE write, list end, the undo printed.
    A disable makes no read.
  - **`undo-owed`** owes a disable for each enable. Test service lines carry the all-zero id; a line whose id has the wrong kind is unreadable.
  - **The capture.** `oxpd1 read --read GetScreenCapture` saves `panel.png` whole in the run folder, and only when the base64 decodes to bytes that start with the PNG signature. It prints the name, the size and the SHA-256, never the bytes. The size is bounded by the client's 1 MiB answer bound, which is unchanged. The image is never committed: the run folder is refused inside a git work tree.
  - **The two WS-Addressing README sentences** now state the M577 reading: 2005 got an empty 400, 2004 was answered. The default is unchanged (Tuesday's answer to the sweep's Q2).
- **Measured in a fresh `<d>/clone3` with the frozen patches:**
  - RED: adapter `Total: 47, Errors: 0, Failed: 4`; Lab `Total: 219, Errors: 0, Failed: 18`. All 22 are red by an `Assert.` line and all are in the two new classes.
  - GREEN: whole solution `total: 2151`, `failed: 0`, `succeeded: 2147`, `skipped: 4` (BASE 2112 + 39).
  - Mutants: `MUTANTS: 16 of 16 MATCH, 16 of 16 undone equal`. After the mutants: rebuild, both dlls later than the mutated sources, the solution green again.
  - Chain: locks 34 of 34 equal after the locked `--force` restore; 2151 / 0 / 2147 / 4; `GUARD: clean (14 files)` and `GUARD: clean (15 files)`; `Ran 111 tests` OK; `RULES: clean (659 files)`; `CHECKS: 10 of 10 PASS`; `WORDS: clean (2 files)`; `B2[0-9]{3}` 0 and 0.
  - gitleaks: control rc 1; the clone and 20 neutral files rc 0.
- **BASE** = main `e2a20aefda7d4356af2b264576a7e3faaf0bce2c`, read by `gh api -X GET` at 15:53:10 and again at 16:24:57. Open pull requests 0; `heads/b2048` 0 rows (control `heads/b2011` 1 row).
  - BASE's push run read by `hosted3.py`: `HOSTED ...: PASS` at `--total 2112 --rules 657` (run 45284683760; linux 2108, windows 2091).
  - PREDICTED for the head: `--total 2151 --rules 659`, windows succeeded 2130.

## Facts re-measured (instrument)
- **HP's committed `test.wsdl`, by line:**
  - `IsServiceEnabled`: guest or admin (`:504`);
  - `EnableService`: admin (`:525`);
  - `DisableService`: guest or admin (`:547`);
  - `GetScreenCapture`: admin, and an `IllegalOperation` fault while the service is disabled (`:367`, `:381`);
  - the `enabled` element: `test.xsd:928` to `:934`.
  This settles the sweep's UNMEASURED "admin or guest" line for HP's text only, not for the device.
- **`CLARIFICATIONS.md` (1114 lines):**
  - 0 lines each: `test service`, `screen capture`, `panel capture`, `IsServiceEnabled`, `EnableService`, `DisableService`, `GetScreenCapture`, `addressing`;
  - `screenshot`: 4 lines, all on other subjects;
  - controls: `C-72` 5, `OXPd` 183.
  Nothing in this lane is the product owner's decision.
- **Local CodeQL cannot run on this machine.**
  - `codeql database create --language=csharp --build-mode=none` ended rc 2 with `Semmle.Autobuild.CSharp: Bad CPU type in executable`.
  - `file` reports that program as `Mach-O 64-bit executable x86_64`, and `arch -x86_64 /usr/bin/true` ends rc 1: this machine has no Rosetta.
  - The commission asked for local CodeQL "per the form", but the form kits never ran it, and gates B2008, B2009 and B2026 list it as NOT RUN.
  - The kit names it NOT RUNNABLE and leaves CodeQL to the pull request's own run (Q8). **This blocks local CodeQL for every C# seat and gate on this machine, not only this lane.**
- **The BASE totals per executable** (40 adapter, 187 Lab) are DERIVED, not run.

## D-decisions (all yours as coordinator)
- **D1:** one name admitted, by name (Q1).
- **D2:** an enable on a service already on writes nothing and exits 0 (Q2).
- **D3:** capture handling as above (Q3).
- **D4:** the capture goes through `oxpd1 read`. The lab's `--read` now takes the enum's names exactly, which refuses `1` as the landed `Get` test did.
- **D5:** no read before a disable.
- **D6:** a Test service write takes no agent option; the all-zero id rule.
- **D7:** the adapter stub starts with the Test service ON, because the landed K01 and K12 loop over every read. The lab stub starts OFF.
- **D8:** four landed literals moved, and no other landed line:
  - C03: 5 to 7;
  - `Schemas()` gains `test.xsd`;
  - K01: 5 to 7;
  - W01: 2 to 4.
- **D9:** README addressing lines only.
- **D10:** one commit, pushed by sha; no local CodeQL.

## Q-questions for Tuesday (each with a default; the kit's Questions section has each alternative and its cost)
- **Q1 (STOP-CLASS), the widening:** default "a", one name by name.
- **Q2 (STOP-CLASS), an enable on a service already on:** default "a", nothing written, exit 0.
- **Q3:** `panel.png`, under the unchanged 1 MiB answer bound.
- **Q4:** the capture through `oxpd1 read`.
- **Q5:** no read before a disable.
- **Q6:** the adapter stub's Test service ON by default.
- **Q7:** the four literals.
- **Q8:** no local CodeQL.
- **Q9:** Opus, READY at +120, push by +90, pane X63, gate G1 round 1 of 2.
- **Q10:** README lines only.
- **Q11:** either landing order with L2. There is no common path, and L2's kit B2049 is already stamped.

## STOP-severity checks run once on the drafter's own output (each with its control)
The tool hashes; the PRIOR-WORK greps; RED by assertion; the mutants; `checks_l1.py` 10 of 10; the lock files; RULES; gitleaks; WORDS and the B2xxx count; the guard counts; `apply --check` of `2-fix.diff` alone (rc 1).
NEVER RUN, and marked so in the kit:
- `clone.py seat`;
- the commit and its identity read;
- the neutral scan of a commit;
- the push by sha;
- `hosted3.py` on a head of this lane;
- the rebase;
- the hosted legs;
- CodeQL.

## Chain inputs
Every step's inputs exist at BASE or come from an earlier step (the kit's CHAIN INPUTS table).

## UNMEASURED
- The M577's answers to the four Test operations, its capture size against the 1 MiB bound, and its handling of a disable when the service is already off.
- The Windows and Linux legs (PREDICTED only).

## Outside-the-fences disclosure
- **Writes:** the kit, its sidecar, this report, and my scratch `<d>/`. The scratch holds three draft clones with push URL `invalid://no-push`, the logs, the tools, `proto/` and `_quarantine/`.
- **Write verbs in my own scratch clones only:** `git apply`, `git add`, and `read-tree` into a private index file. Never in a project checkout or another seat's clone. A hook refused one `git apply` that named the scratch clone through a shell variable; it was re-run with literal paths.
- **Things that went wrong and were redone:**
  - A first `2-fix.diff` cut lost its final context line (`corrupt patch`). It was re-cut.
  - A first frozen run stopped at its red build: the analyzer rule xUnit2029 refused `Assert.Empty` over a filter. I stopped that background run with TaskStop and changed T01 to `Assert.DoesNotContain`. The frozen run was then redone whole in a fresh clone.
  - `checks_l1.py`'s first cut printed 9 of 10: check 7 counted the client's own class comment, which names `SendWriteAsync`. The check was re-scoped to Lab lines, and the checks and the neutral gitleaks scan were run again.
  - Every discarded artefact is in `<d>/_quarantine/`.
- **Shared resources:** every dotnet job ran through `heavy.py` and the shared wave lock. There was one CodeQL attempt (rc 2), and load1 reached 28.1.
- **GitHub:** `gh api -X GET` and `hosted3.py` (GET only) under the project's `GH_CONFIG_DIR`, plus three `git clone`s in draft mode.
- **Not touched:** no Jira, no Azure, no printer, no message to anyone.
