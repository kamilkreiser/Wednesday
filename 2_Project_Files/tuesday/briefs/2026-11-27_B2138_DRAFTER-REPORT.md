STARTABLE: YES

# B2138 DRAFTER REPORT: OXPd 2, lane OX-C kit 2 PART 1 (owed 54, 75, 55; 137 and 121 part 2; 138 a tooling commission), seat X81

Drafted 2026-11-27 by an in-session read-only drafter (Opus) for Tuesday s332. First `date`: `Fri 27 Nov 2026 09:05:02 AEDT`; the sidecar's first line carries the write clock. Kit: `tuesday/briefs/2026-11-27_B2138_SEAT-X81_oxpd2-lane-c-kit2.md` (233 lines), sidecar `.measured` (`stamp_check.py` exit 0: "154 claims, 154 measured, 0 not measured"). Scratch: `fleet/state/s332/d2138/` (the seat's tools are in its `seat-tools/`).

**STARTABLE means: the kit is complete and stamp-checked; its LAUNCH waits on two things outside it** (both in its REFUSE AT ONCE and Stamp S2/S3): kit 1 (`b2134/lane-c-kit1-hygiene`, 641935b5) landed on `main` by squash (gate B2137 was reviewing it at drafting; `main` was still 38a031e5, 0 open pull requests), and the records seat of that landing ended READY. Not launchable this minute.

## BLUF
- **Split by the commission's own default (Q1, STOP-CLASS):** this kit builds owed 54, 75 and 55 (Universal Print registration only: four files, all `M`, no path shared with kit 1). Owed 137 (the `HostRig.cs` per-cell bound, serial on kit 1's file, its hang seen once and not reproduced: kit 1's STATUS H13 "a one-off") and 121 (README lines in three modules of three lanes) are part 2. Owed 138 (`heavy.py`, outside the repository) is left for a separate tooling commission (Q2 default); the kit keeps its interim rule (end your own orphan by pid).
- **75:** an `internal Action<CloudDeviceToken>? AfterArrivalCheck` test seam on `CloudDeviceTokenHolder` (the project's own seam form, `JobSpool.BeforeFolderDelete`), invoked between the arrival check and `Finish`'s lock. Cell T15 (2 shapes: an answer disposed there; the held object answered again and invalidated there) reaches the check under the lock on every run, never by a race. Frozen mutant `mUnderLockOnlyRemoved` (the check fires only for a removed entry) reddens T15 only (PREDICTED; the review measured that removing that block leaves every landed cell green).
- **55 (7):** the README's "Every failure after construction is a `RegistrationException`" is wider than the code (no catch around the key factory, export or signing in `CreateRegistration()`); E1 adds the exception, a Limits bullet names it, cell K07 pins it (a factory throwing `CryptographicException` and one throwing `InvalidOperationException` each leave as that type, nothing is put; control first). Frozen mutant `mKeyFailureTyped` reddens K07.
- **55 (2) to (6):** five named limits, each "measured on macOS arm64" (owed list: Linux and Windows UNMEASURED); two existing bullets widened in place (leaf extensions; an older stored form).
- **54:** `mCatchNarrow` and `mFixUndone` cannot be reached by a platform-independent shape (kit B1915's seat tried the one known shape; `mFixUndone` dies only on hosted Linux via C01): a named limit (E5), no cell.
- Ten frozen edits (`edits_c2.json`, groups `seam` and `text`), two frozen mutants, two seat-written cells; PREDICTED UP executable `Total: <BASE + 2>` (BASE DERIVED 329), whole solution `total: 2431` (kit 1's head MEASURED 2429), `RULES: clean (679 files)`.

## FACTS RE-MEASURED (instrument, then what it printed)
- Origin (`gh api -X GET`, OXPd GH_CONFIG_DIR, 09:05:54 AEDT): main `38a031e5...`, tree `22c5f214`; open pulls 0; `matching-refs/heads/b2134` 1 row `641935b5...` (tree `7ec27cb9`, parent 38a031e5); `matching-refs/heads/b2138` 0.
- Kit 1's head tree: tarball by `gh api -X GET`, 679 files, scratch `git write-tree` = `7ec27cb935fee08e2162532b146c1b89b96d817e` (equal). The four owned files hash the same at 38a031e5 and at 641935b5 (kit 1 touches no Universal Print path).
- Kit 1's head hosted: `hosted3.py 641935b5 --total 2429 --rules 679 --skipped-linux 4 --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15` -> `HOSTED ...: PASS`; control `--total 2430` -> `FAIL 4` rc 1.
- BACKLOG.md `ba8ab83e...` (1192 lines): lines STARTING WITH `54. - [ ] `, `75. - [ ] `, `55. - [ ] `, `137. - [ ] `, `138. - [ ] `, `121. - [ ] ` 1 each (control `54. - [x] ` 0). A substring count of `54. - [ ] ` reads 2 (item 154): the kit says `startswith` for that reason. CLAUDE.md `0f1fccc0...` (line 7 newest Opus; 55-56, 82 landing; 83 toolchain).
- Frozen edits: each OLD once (10 of 10); `apply_c2.py` on a copy of kit 1's head tree: `APPLIED seam: 4 edits, 3 of 3 files equal`, `APPLIED text: 6 edits, 1 of 1 files equal`; second `seam` apply `APPLY REFUSED` rc 1; `check` prints BASE on the head tree, FROZEN on the copy.
- `checks_c2.py`: kit 1 head's index `CHECKS: 2 of 9 PASS` (every control FIRED); simulated staged edit (frozen edits + prototype cells) `CHECKS: 9 of 9 PASS`.
- `mutants_c2.py --list` rc 0 (`LIST: 2 mutants, 1 suites, 2 cells`), bad row rc 1; apply/undo of both on the green files: `equal True` twice.
- `words.py --control` 13 of 13; over the commit message and the 36 added lines of the frozen edits: `WORDS: clean (2 files)`; over the 105 simulated added lines (with prototype cells): clean; `B2[0-9]{3}` 0 and 0.
- gitleaks 8.30.1: control rc 1 (quarantined); the eleven tools and the simulated added lines rc 0, `no leaks found`.
- Toolchain `<project>/.tools/dotnet/dotnet --version` 10.0.404. Indented counts over the UP tests at kit 1's head: `[Fact` 155, `[Theory` 40, `[InlineData` 174, `MemberData` 0, column-1 0.
- Seat id X81: 0 of 384 non-`.pre-` SEAT kit files of 2026-11-2x (control X80: 1). No port. Load `7.98 11.31 7.13` at 09:17 (gate B2137's jobs); lock folder absent at 09:17; panes `tuesday` and two unnamed.

## D-DECISIONS (all the coordinator's defaults; each is a Q)
D1 part 1 of two (54, 75, 55); D2 138 not in this code kit; D3 edits and mutants frozen, cells the seat's; D4 75 by an internal seam, not reflection plus timing; D5 55 (7) by a README exception pinned by K07, no code change; D6 54 a named limit; D7 55 (2)-(6) named limits, two bullets widened; D8 new cells, two frozen class summaries (`checks_c2.py` check 4 allows exactly those two removed lines).

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS, S4 in words): one kit or two.** Default a: part 1 = 54, 75, 55; 137 and 121 a later part-2 commission. Alternative b: all six in one kit (re-draft).
- **Q2: owed 138.** Default: a separate tooling commission for the runner in Tuesday's tree (new process group per job, ended at the bound); this kit keeps the pid rule. Alternative: a changed runner inside this lane's `gate/`.
- **Q3 (STOP-CLASS, S4 in words): who writes what.** Default a: seam, summaries and README frozen; mutants frozen; cells the seat's. Alternative b: the seat writes all to a specification.
- Q4: seam in the product (default) vs reflection on `Entry.Sync` through a copy's `Origin` and a timed dispose (no product line; a race that can pass without reaching the check).
- Q5: README exception + K07 (default) vs a typed refusal for a failed key generation (product change).
- Q6: 54 named limit (default) vs a Linux-only assertion.
- Q7: named limits with two bullets widened (default) vs new bullets only.
- Q8: the two summaries frozen (default) vs left stale.
- Q9: ONE G1 gate (default; the seam is a product line on a token surface) vs G2; Opus, `BRIEF_SEAT_LEVEL=opus`, `CLAUDE_CONFIG_DIR` inside the quotes; pane `Datasec/OXPd2-X81`; READY Step 0 + 120, push Step 0 + 100.

## UNMEASURED (each named in the kit where it is used)
- No dotnet job ran: every pin, green, total and mutant expectation is PREDICTED, each with the assertion it must break or pass. I did not take the OXPd wave lock at all (a G1 gate was using it; load was near 8).
- The UP executable's BASE total (329 DERIVED from attribute counts); the seat measures it at Step 1.
- BASE's own push run after kit 1's squash (Stamp S2 gives its numbers; the drafter measured kit 1's head run only).
- That the seam compiles warning-free under `TreatWarningsAsErrors` (DERIVED: `answer` is non-null by flow analysis after the arrival check), and that `mKeyFailureTyped`'s lambda compiles warning-free (DERIVED). A build failure of a frozen line is `STOPPED: NEEDS TUESDAY` by the kit.
- The prototype cells in `d2138/gen/proto_*.cs.txt` were never compiled; they are NOT given to the seat and NOT frozen.
- C01 reaching the field-read catch on Linux is RELAYED (kit B1915 D5), not re-measured at this tree.

## CHAIN INPUTS (every step's inputs exist at BASE or come from an earlier step; the kit's table)
0 stamp (S2 BASE after squash, S3 records READY, S4, S8); 1 `<src>` (exists), `<repo>` values, origin, BASE run, records STATUS, BACKLOG; 2 BASE files + `edits_c2.json` (Step 1); 3 group seam + the cells on the Step-1 clone; 4 pinned tree (3) + group text + frozen mutants (1); 5 green tree (4); 6 staged tree (5) + checks/words/message/edits (1); 7 commit (7a), origin/main fetch, run_step/hosted3 (1).

## OUTSIDE THE FENCES (disclosure)
- Writes: only the kit, its `.measured`, this report, and scratch under `fleet/state/s332/d2138/` (three scratch git repositories made by `git init` there: `k1repo` (kit 1's head tree, index only), `sim` (the simulated staged edit), none with a remote or a commit; superseded check folders and the first sidecar draft moved to `d2138/_quarantine/`). The first `--init` sidecar was moved (not deleted) to `d2138/_quarantine/measured.v1` after I corrected kit line 1, then re-initialised and filled. Nothing written to the OXPd project folder, Jira, GitHub or any card store; no push; no pull request; the OXPd wave lock never taken.
- Reads of the project folder by path only (no recursive read): `CLAUDE.md`, `BACKLOG.md` (by line ranges and in-process counts), `CLARIFICATIONS.md` (sha256 only), kit 1's `2026-11-27_B2134_STATUS.md` (tail and grep), `ls -d` of `.tools/b2134`, `.tools/b2137` (absent), `.tools/b2138` (absent) and the lock folder (absent), and `.tools/dotnet/dotnet --version`.
- One background grep over `tuesday/briefs/*_verify` ran past its 120 s cap and was stopped by me (TaskStop) before printing; read-only.
- Hook refusals: one `cd` (re-issued without it) and one unquoted `=====` separator (re-issued); nothing ran either time.
- GitHub: `gh api -X GET` only under the OXPd GH_CONFIG_DIR (commits, pulls, matching-refs, one tarball, check runs and job logs via `hosted3.py`). No Jira call. No HTTP to any other host. No person, HP or device contacted.
- Read Tuesday-tree evidence: kit B2134 (kit, commission, report, ANSWER-1), kit B1915 and B1937's lines on 54, the sweep's lane OX-C block, DRAFTER_RULES. Did NOT read the ledger, the scoreboard, `fleet/briefs_staged/`, any card store, or any WEDNESDAY/FRIDAY tree.
