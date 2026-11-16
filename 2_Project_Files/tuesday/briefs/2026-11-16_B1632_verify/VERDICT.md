GATE B1632: GO WITH FINDINGS @ 8af1d43 on main 3e557e5

G2 gate (run on Opus) for the HPSM-POC lane: the start-up warning for FollowUp:TrustedProxies with no ForwardedHeaders:Proof (484) and the 30 s guard (496). Every number below was measured by this gate on 2026-11-16 between 18:34 and 19:11 AEDT. The work was done in its own scratchpad clone (push URL set to invalid) and in /private/tmp/b1632-gate/. Raw per-run rows are in runs.tsv. The probe file is probe-GateProbeTests.cs.txt.

## Findings

| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Major (claim contradicted; not a blocker) | The commit message and STATUS say "no behaviour change". That is false at one edge. The new line resolves `IOptions<FollowUpOptions>.Value` during start-up. At main, nothing reads FollowUpOptions until a follow-up request arrives. So a malformed FollowUp value (probe: `FollowUp:SessionMinutes=abc`) now stops the host from starting with `InvalidOperationException: Failed to convert configuration value 'abc' at 'FollowUp:SessionMinutes'`. With main's Program.cs the host starts, and only follow-up requests would fail. Shipped and valid settings are unaffected; this is arguably a better fail-fast. The kit's D1 prescribed exactly this expression, so the builder followed the kit. Fix: none needed in code. The landing text discloses it: the gate's squash-body.txt and pr-body.txt replace the builder's "no behaviour change" sentence. Tuesday: accept as disclosed, or ask for a ticket. | P16: head FAILED (exception above); the same test with main's Program.cs PASSED (runs.tsv p16-head, p16-mainprog) |
| F2 | Minor | The builder's squash-body.txt has no Co-Authored-By trailer. The pushed commit carries the builder's own "Claude Sonnet 5.5" trailer. That is fine, because the squash body replaces it. Use the gate's squash-body.txt. | builder evidence/squash-body.txt |
| F3 | Minor (disclosed by builder) | red.diff was made at the old base 678a1153, not 3e557e5. This gate re-ran red-first at 3e557e5 itself (below), so the gap is closed. | STATUS:86 |
| F4 | Info | The commit author name is the configured project identity, as the kit requires. It is not a name-scan subject: added lines and the message scan clean. | git log %an |

No Blocker. A Major is a claim my numbers contradict. Here the code is correct and the claim is corrected in the landing text, so the verdict is GO WITH FINDINGS. Tuesday decides whether F1 needs the product owner.

## What was verified (instrument, control)

1. **Refs.**
   - `git ls-remote` (18:3x and again at 19:11): branch = 8af1d43a118eef8e98a6a7fbe8686c9d5003b36b; main = 3e557e56089b3ee4af9e20f08a414a1a4c9ff157.
   - merge-base = main. The branch is 1 commit ahead.
   - Changed paths: 2 of 2 are inside OWNS (Program.cs, ForwardedProofTests.cs).
   - Open PRs: 0. Control: `state=all` lists 327, 326, 325.
   - Sibling branches b15xx-b16xx touching owned paths: b1565 and b1599 only. Both are already squash-landed: the diff from each branch to its squash commit on main is empty. Live overlap is 0.
2. **Merge.** `git merge-tree --write-tree main head` = 27e29322..., equal to the head tree. The merge is clean and is exactly main plus the head blobs (a fast-forward shape), so merge = head for every run.
3. **Diff shape.**
   - Program.cs: 3 lines added, 0 removed. Main's lines 128-131 and the gate at :134-136 are byte-equal at head :128-131 and :137-139.
   - Head with the 3 added lines removed equals main exactly (by program).
   - The new template is byte-equal to the template at :131.
   - The test file removes 1 line: the forcing test's first request, now wrapped in `.WaitAsync(TimeSpan.FromSeconds(30))`.
4. **Build.** Release build of the solution: 0 warnings, 0 errors, at main, head, the red copy, the probe copy, the mutants and the plant. TreatWarningsAsErrors is on.
5. **Red without the fix** (own copy: head tree with main's Program.cs):
   - Rows 1 and 4 are red by assertion 3 of 3 (`Assert.Single() Failure: The collection was empty`). The other 26 tests in the class pass. Row 4's existing-line assertion passed, which proves the capture sees `app.Logger` start-up warnings.
   - Rows 2, 3 and 5 (absence rows) are each killed by their own mutation of the product condition. Each mutant was built 0/0 and the six-test row filter run once:
     - M1, drop `&& !forwarded.HasProof`: row 2 red.
     - M2, `Any()` in place of the non-blank test: row 5 red. This proves a single-space entry binds as a blank string, which the builder had left unproven.
     - M3, the warning fires whenever the list is non-null: rows 3 and 5 red.
   - No new row is vacuous.
6. **Boundary probes** (22 cases in a probe class, at head and with main's Program.cs). Each asserts the exact counts of the new line, the existing ForwardedHeaders line and the platform-switch line. Modes: hosted (Production, real bearer), local (Development + Development sign-in) and testing.
   - Head: 22/22 pass.
     - Named + Proof absent: 1 line, in all three modes.
     - Named + Proof set: 0.
     - Named + Proof blank (""): 1. This matches HasProof (IsNullOrEmpty).
     - Absent: 0. Section value "": 0, and the host starts (no null list). Entry "": 0. Entry tab+space: 0.
     - Blank + named: 1. Two named: 1, once. Unparseable entry "web-server": 1 (non-blank names a proxy, per Q-5).
     - Both lists + proof: 0/0. ForwardedHeaders only, no proof: existing 1, new 0. Both lists, no proof: 1 and 1.
     - Platform switch + follow-up: switch line 1, new 1. Switch alone: switch line 1, new 0.
   - Main's Program.cs: exactly the 10 expect-a-line cases go red, with new-line count 0 where 1 was expected. The 12 absence cases stay green, and the existing lines' counts are identical. The existing two warnings are unchanged in behaviour as well as in text.
   - A whitespace Proof (" ") refuses start by design: IsProofForm, pre-existing. It is not a warning case.
7. **The 30 s guard (496)** (own scratch plant: the hold moved above `await nextMiddleware`):
   - With the guard: the forcing test fails in 33 s and 33 s (2 of 2) with `System.TimeoutException`, at ForwardedProofTests.cs:233 (the guarded first request).
   - Without the guard, same plant: `dotnet test` was still running at 90 s. It was stopped by pid (the pid and its 10 children, all confirmed gone).
   - The guard turns a hang into a red. It cannot produce a pass, and its `finally` still releases the hold. The watch read keeps its own 30 s guard, and nothing else in the test changed. It does not mask a real hang. The builder's method (STATUS:47, FOR TUESDAY) was sound and reproduces.
8. **Repeated runs at main and head, compared by program** (trx-parsed, load1 per run in runs.tsv):

   | Job | Main | Head | Notes |
   |---|---|---|---|
   | ForwardedProofTests class | 23/23 x3 | 28/28 x5 | +5 = the five rows |
   | Hosting. group (default host) | 221/221 x2 | 226/226 x2 | = 221 + 5 |
   | SQL Server part (ci.yml filter; pinned MSSQL and Azurite images by digest; ports 10190/10191; judge extracted from ci.yml:278-310 by program) | 1486/1486, judge rc 0, 325 databases | 1491/1491, judge rc 0, 330 databases | floor 100 |
   | Whole api predicate (Azurite on 10191; per-assembly console lines) | not run | Rules 164, Assessment 311, Reporting 865, Feedback 478, Api 2361 = 4179 passed, 0 failed, 0 skipped | 0 skipped in every assembly means the Azurite tests ran |

9. **infra hidden-characters scan.** `test_hidden_characters.py` (python 3.14.10) ran 14 OK at main and at head. Control: a planted U+202E in a tracked file in a scratch tree gives FAILED (failures=1).
10. **Scans over the 69 added lines and the commit message** (python -I -B; each control fired):
    - Ban-list and identity names, underscore-aware: 0. Control `_by_Kam_`: 1.
    - Work ids (B-numbers, seat, day names, HPSMPOC-n): 0.
    - Non-ASCII: 0. Cf characters: 0.
    - Skip/Retry/Sleep/Delay/Collection: 0. The only wait is the D3 `WaitAsync(30 s)`.
    - Secrets, tenant ids and hosts: 0.
    - Sensitive-name row: 1 hit, the pre-existing synthetic `Token('R', 0)` helper on the guarded line. It is passed to a request, not written to a file or log, so it is not a CodeQL storage or log sink.
    - The new LogWarning logs only two constants (a literal section name and `ForwardedClientAddress.ProofKey`, the same constant :131 already logs on main).
    - JS and Python CodeQL floor rows: not applicable, C# only. 0 hits.
11. **Claims in builder STATUS:**
    - True (my numbers):
      - the build is 0/0;
      - rows 1 and 4 are red by assertion;
      - the existing line reads 1 at base;
      - class 23 to 28;
      - Hosting 221 to 226;
      - SQL 1486 to 1491 with 325 to 330 databases and judge clean;
      - whole api 4179;
      - hidden-characters 14 OK;
      - Program.cs +3/-0 with a byte-identical template;
      - the D3 guard gives a TimeoutException in about 30 s, and the run hangs without it;
      - MAIN MOVED with no owned path touched (the 678a1153..3e557e56 diff is 4 web/README paths);
      - 2 paths changed.
    - False: "no behaviour change" (F1).
    - Not shown by me: the x10 repeat counts (I ran x5 and x2), and infra unittest 325 / validate.sh (not in this commission's list).
    - Builder disclosure 2 (rows 2, 3 and 5 not mutation-proven) is now closed by this gate (item 5).

## NOT RUN

- CodeQL csharp: NOT RUN (cannot extract on arm64). Hosted CodeQL is the only C# proof.
- `infra/scripts/validate.sh` and the full infra unittest discover: not run (only the hidden-characters scan was commissioned). The diff touches no infra file.
- Whole api predicate at main: not run (head only). The ci.yml Azurite named-10 judge was not run over all trx files, because the per-assembly trx shared one file name and only the last survived. "0 skipped" per assembly stands in.
- The SQL Server `api-other-and-feedback` shard: not run. It does not read Hosting or the changed files, and hosted CI is its proof.
- Load: the load gate (load1 < 7) was met at 18:34 (5.79) and at times after, but most runs started with load1 7.1-10.4. All heavy jobs ran strictly one at a time. Every run's load1 is in runs.tsv, and no red was seen on any non-planted run.

## Hygiene

- Containers b1632-mssql and b1632-azurite were created and removed per job: 0 left.
- Ports 10190-10199: 0 listeners at 19:11. Control: the unfiltered listener list shows 13.
- No process of this gate is left: 0.
- Nothing pushed, no PR, no Jira, no mail, no az, no hosted HTTP (GitHub GET reads only).
- Nothing written in the HPSM project folder. Its only porcelain entry, an untracked "HP Docs/", was there before this gate.
