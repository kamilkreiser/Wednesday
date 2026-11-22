GATE B1926: GO WITH FINDINGS @ b107927 on main 7b0f4f5

Gate G2 (docs), round 1, the one reader. OXPd 2, kit B1922 (seat X34, lane E) as re-cut by ANSWER-1: the adapter
README's named limits, owed items 45 and 46 (README halves). Head `b1079275847295f24be070cd0b4fd7d129a08206` on
`b1922/e-adapter-readme-limits` (ONE commit, ONE parent `4a0a9717277f60647dfc174e60ec04fc7008e615`). Main at the gate
`7b0f4f55d835f669a0539ce65d80e5625bd9c1dc` (pull request 20, two test files). Read and measured 2026-11-22 22:15 to
22:25 AEDT (clocks by `date` and tool lines), on Opus 5.5, in my own clone `fleet/state/s311/g1926/clone` (the kit's
`clone.py ... draft`: push URL `invalid://no-push`, no local identity), detached at the head. Origin by `gh api -X GET`
under the project GH_CONFIG_DIR at 22:19 and 22:21: branch = b1079275, main = 7b0f4f55, open pull requests 0, newest
20; `compare 7b0f4f55...b1079275` ahead 1, behind 1, merge base 4a0a9717, exactly the README +49 -1. No write to the
project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted.

**BLUF.** The head is exactly ANSWER-1's patch (`git diff 4a0a9717 b1079275` sha256 `bc903822...3a8f` = the re-cut's
`1-readme-limits.diff`; README `e17e251b...dee8`, 156 lines, ASCII, longest 119, no `file:line`). I read each of the
15 rows of THE REQUIRED SECTION beside its code lines: every added sentence is TRUE of the code at BASE. None answers a
question that is the product owner's, none names who decided, and the parse step no longer calls C-63's subject open
(it matches C-63 at `CLARIFICATIONS.md:610-624`: "Keep both strict for now", "Revisit after Monday's printer test").
The one remaining "open question" is the late grant (E4), which no clarification touches. Proofs 68 of 68, control
68 of 68, census 13 of 13. The survivor mutant `mIssueNoBump` is green (58 / 0), it is compiled in (the DLL's sha256
changes), and its positive control turns exactly A06 red. The merge with main is clean. The head's hosted run and
main's both read PASS. One Minor: "the specification inputs hold no map" is true of a declared map, but 150 open
objects exist, some read as a raw `JsonElement`. Four Info. Nothing blocks the landing.

## FOUND

1. **Minor: G1's "hold no map" holds only for a declared map.** It is TRUE as the sentence defines it: 206
   `additionalProperties`, all `false`, in 37 inputs; `patternProperties` 0; `propertyNames` 0; the generator reads
   none of them. But the inputs also hold 150 schemas of `type: object` with neither `properties` nor
   `additionalProperties` (my walk over the 37 tracked files: 1616 object schemas, 1442 with `properties`). JSON
   Schema leaves those open by default. 94 are empty request objects (`beepRequest`, `exitRequest`, ...) and 54 are
   named `value`. At least one is generated as `JsonElement`: `CapabilitiesImplInfoItem.Value` at
   `Generated/Application/Models.cs:886`, from `capabilities/properties/implInfo/items/properties/value`. So a reader
   can take "no map" to mean "no object that takes any keys", which is wider than the code. The seat flagged this
   (its E11 NOTE). It is not a false statement, so I did not reword it (the patch is frozen). Named in pr-body
   "Still open" and FOR-RECORDS 1 as one owed README line for a later docs lane. Tuesday may instead re-cut the
   sentence before landing: one line, and a new gate on the one changed row.
2. **Info: an unnamed limit beside E4.** The endpoint receives the refresh array as `ReadOnlyMemory<byte>`
   (`DeviceTokenHolder.cs:331`). The `finally` zeroes it (`:398`) on a timeout, while an endpoint that ignores its
   cancellation (which E4 names) may still be reading it. DERIVED, not run. E4 stays true. FOR-RECORDS 2.
3. **Info: E1's edges.** All three of its claims are TRUE:
   - `StoreRefreshValue` (47-72) touches no `Flight` and no `Generation`;
   - a refresh that read before `:58` goes on (314, 323), and a waiter "can" get its failure (280-284);
   - the rotated `Put` (373, 377, under `:352`) and the store's `Put` (`:58`, before its lock `:65-66`) both reach the vault, and the last write stays.

   Two things it does not name:
   - an in-flight refresh that succeeds keeps its access value after the store cleared it (generation unchanged, `:356`, `:387`);
   - a refresh between `:294` and `:314` reads the new value.

   Neither makes the sentence untrue.
4. **Info: E5 holds while that failed refresh is the last completed flight.** If a later flight succeeds, the request
   reuses that flight's access value (`:287-289`). The README's existing paragraph (lines 21 to 24) already says
   this.
5. **Info: the commit subject (262 bytes) is longer than GitHub's 256-character PR title limit.** Kit B1922 makes the
   commit message the squash's subject. That cannot carry over to the title, so `pr-title.txt` (243) and
   `squash-subject.txt` (252, with ` (#PRNUM)`) shorten the parenthesis. The subject then differs from the commit
   message: Tuesday's to accept (landing.txt step 1 says so).
6. **The seat's record (asked by the commission).** Its DEVIATIONS 1 ("Step 1 baseline NOT run") belongs to its
   first stop. Its RE-CUT section ran the baseline at 22:00 to 22:04 (DEVIATIONS 7: restore rc 0, build 0/0, 58 / 0
   failed). **The survivor mutant of Step 4 DID run**: `Total: 58, Errors: 0, Failed: 0`, `[FAIL]` 0, the adapter
   assembly written at 22:04:53 after the 22:04:43 edit, undo proved by `cmp`. The seat did NOT run the positive
   control (its NOT RUN). I ran both (TESTED).

### The 15 rows (TRUE unless named above; lines at BASE, read by me beside each sentence)
- E1 L1: TRUE, edges in FOUND 3.
- E2 L2: TRUE. The lease is a new string (184); `Forget` zeroes only the holder's bytes (102); the request sends it at `SolutionTokenHandler.cs:60-61`.
- E3 L3: TRUE.
  - The rotation's `Put` (377) runs under `entry.Sync` (352), and `Forget`'s `Delete` (107) under it too (97).
  - `GetState` (85), `AcquireAsync` (175) and `RenewAsync` (200) take that lock.
  - `Dispose` takes `_sync` (127) and then each `entry.Sync` (137).
  - `Find` and `Entry` (245, 253) and `ThrowIfDisposed` (164) take `_sync`.
  - The real store is UNMEASURED, as the sentence says.
- E4 L7: TRUE.
  - A timeout throws out of `WaitAsync` (332) to the general catch: cancel (346), then `RefreshFailed` (347). State is untouched (`Ready`, because `:273` refuses a marked device).
  - The grant is never stored. `Flight` is released (301) while the call may still run.
  - "Open question": the register has 0 hits for `refresh`, `timeout` or `late`, and 1 for `grant` (line 688, C-68, not a token).
- E5 L8: TRUE, edges in FOUND 4. On a 401, `RenewAsync` (68); `Flights` moved (235, 280); `Failed` then throws `LastError` (282, 284) before any refresh or retry.
- E6 L11: TRUE. `Generation++` (101) runs before `Delete` (107), and a throw gives `VaultFailed` (111). A refresh in flight fails `:356` and stores nothing. The record stays, and the next `Acquire` refreshes with it (314).
- E7 L10: TRUE. The holder zeroes in its `finally` (398). The credential cache keeps the array it reads (194) and zeroes it at `Issue` (60) or `Forget` (95).
- E8 C9: TRUE. A wrong length returns null (178, 180); `Verify` then returns false (80) and the handler gives `Unauthorized` (`Oxpd2CallbackHandler.cs:109`). `Unavailable` comes only from a throw (104).
- E9 C6: TRUE.
  - Generation moved: the read is dropped unzeroed (187, 189).
  - Another check cached first: also dropped unzeroed (192).
  - Wrong length: dropped unzeroed (178-180).
  - The only `Put` to a callback-hash name is `Issue`'s (55), of `SHA256.HashData` (54, 147); `HashLength` is 32 (20).
- E10 C5: TRUE, MEASURED below. Only `tests/Datasec.Suite.Adapters.Oxpd2.Tests` references `CallbackCredentials`, so its executable run whole is "every cell" (`git grep -l`).
- E11 G1: TRUE as defined, Minor in FOUND 1.
- E12 G2: TRUE from the converter's source.
  - The factory converts every enum (129). The writer writes only from `_toWire` (187-189). The reader takes only `_byWire` or `_hasUnrecognized` (172-182).
  - Census: 0 wire names and 0 unrecognized in `Oxpd2Refusal.cs` and `DeviceTokenError.cs`; control 20 in `Enums.cs`.
  - NOT RUN as a serialisation (Q6, as stamped).
- E13 G3: TRUE (UNMEASURED; nothing has run on a printer).
- E14 line 63-64: TRUE against C-63 at source. It does not say who chose it, and it does not call the point open. The list's full stop is now a semicolon.
- E15 NAMED OUTS: TRUE. None of item 45 (10)'s `.cs` line, item 46 records (1), (3), (5) or NOT DECIDED 2/3 is in the 49 added lines. C-63's answer to NOT DECIDED 2 is not mentioned (FOR-RECORDS).

## TESTED (MEASURED. Every dotnet job and test executable went through the kit's `heavy.py`, unchanged, one at a time: 13 jobs, lock folders moved to `g1926/_quarantine/locks/`. Waits were only on other holders; no lock was ever broken.)

- **Tools**: `cp -Rc` of `<d1922>/answer1` to `g1926/gate/`; all ten sha256 equal ANSWER-1 section 2.
- **The head's diff and README**:
  - `git diff 4a0a9717 b1079275` sha256 `bc903822...` = the patch. `--name-status`: `M` README only. `--numstat` 49 1.
  - README sha256 `e17e251b...`. Non-printable lines 0, longest line 119, `\.cs:[0-9]` 0, `open question` 1 (E4). `ls-files` 500.
  - The stored message equals `commit-message.txt` (`cat-file` body `cmp` rc 0). Author and committer are one address.
- **Proofs** over the head's tree (the code files are BASE's byte for byte; the diff is the README only):
  - `PROOFS-CONTROL: 68 of 68 FAILED when moved` first, then `PROOFS: 68 of 68 PASS`, then `CENSUS: 13 of 13 as required`. Each rc 0.
- **Build and run**:
  - `CI=true dotnet restore --locked-mode` rc 0, porcelain empty. Build `0 Warning(s)` `0 Error(s)`.
  - The Adapters.Oxpd2 executable run whole: `Total: 58, Errors: 0, Failed: 0`.
- **`mIssueNoBump`** (`3-mutant.txt` exactly, OLD found 1, full write plus `os.utime`):
  - build 0/0; **`Total: 58, Errors: 0, Failed: 0`**, `[FAIL]` 0. Undone: sha256 equal, `git diff --quiet -- src` rc 0.
  - Compiled-in proof: the adapter DLL's sha256 is `d513686f...` at the head and `fd59180e...` under the mutant. It is `d513686f...` again after the undo.
- **Positive control `mIssueNoBump` plus `mNoFill`** (`:192`'s fill made unconditional, the drafter's `proto3.py` text):
  - build 0/0; `Total: 58, Errors: 0, Failed: 1`, `[FAIL]` 1: `RaceCellTests.A06_Issue_during_a_check_that_reads_the_vault_takes_effect` alone.
  - `mNoFill` alone: `Failed: 0`.
  - After every undo: build 0/0, 58 / 0, porcelain empty.
- **Merge**: `git merge-tree --write-tree 7b0f4f55 b1079275` rc 0, tree `9302f7bfc8a1e61f6235536a365a6c5770f49699`, 500 files.
  - Against main it differs in the README only (blob `be3528c0` = the head's). Against the head it differs in PR 20's two test files only.
  - PR 20 touches no file the proof table names.
  - Expected merge-ref totals: main's 1581 + 0.
- **Hosted, head**: `hosted2.py b1079275... --total 1579 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111 --hardened-scan` rc 0.
  - Run 45015821397, four jobs success, nothing beside them.
  - linux 1579 x2 / 1575 / 4 / 0 failed, GUARD clean (10 files). windows 1579 x2 / 1560 / 19, GUARD clean (11 files).
  - rules: Ran 111, floor 111, RULES clean (500 files). secret-scan: every hardened row OK.
  - `HOSTED b1079275847295f24be070cd0b4fd7d129a08206: PASS`. `failed Datasec.` lines 0 per leg (control: `total: 1579` 2 in each).
- **Hosted, main**: `hosted2.py 7b0f4f55... --wait --total 1581 ...` rc 0, run 45016304308.
  - linux 1581 x2 / 1577 / 4; windows 1581 x2 / 1562 / 19; RULES 500; three Analyze rows success.
  - `HOSTED 7b0f4f55d835f669a0539ce65d80e5625bd9c1dc: PASS`. Open code-scanning alerts on main: 0.
  - Main's ruleset `strict_required_status_checks_policy`: false (a branch behind main is not blocked).
- **WORDS**: `--control` gives `CONTROL FIRED: 13 of 13`. Over the 49 added lines and the commit message: `WORDS: clean (2 files)`.
- **GITLEAKS 8.30.1**:
  - Control first: a token shape built by program from two halves and random characters, never printed. rc 1, `leaks found: 1`, moved to `_quarantine/gl-control`.
  - Then the added lines, the message and the README as neutral `<n>.txt`: rc 0, `no leaks found`.

## NOT TESTED

- No whole-solution run, publish or release guard locally. The hosted legs (fresh checkouts) carry those, and the change is one Markdown file that nothing reads (`git grep -i readme` finds no reader of it).
- No CodeQL locally. It is read on the pull request (landing step 3).
- Whether a hosted leg keeps `mIssueNoBump` green: UNMEASURED, and not a landing condition.
- E12 as a serialisation of `Oxpd2RefusalKind` or `DeviceTokenError`: NOT RUN (read from the converter's source).
- The `run_step.py` neutral scan locally (the hosted secret-scan job ran it on this head: OK rows above).

## HOW

- Driver `g1926/scratch/mutants_run.py`, output in `g1926/logs/mutants_run.out`. It applies and undoes every mutant by a full write plus `os.utime`, and sends every job through `heavy.py`.
- Compiled-in proof: `g1926/scratch/compiled_in.py`, output `logs/compiled_in.out`.
- Per-job logs: `g1926/logs/g-*.log`. Proofs: `logs/proofs*.log`, `census.log`.
- Hosted: `logs/hosted.out` and `logs/hosted/`; `logs/hosted-main.out` and `logs/hosted-main/`.
- Diff, added lines and message in `g1926/scratch/` (`head.diff`, `added.txt`, `msg.txt`, `neutral/`, `neutral-landing/`, `squash-scan.out`).
- The clone is left detached at the head, porcelain empty, `bin/` and `obj/` kept. No process is left running, and this gate does not hold the wave lock.

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 243 bytes (under 256; shortened from the 262-byte commit subject, FOUND 5).
- `pr-body.md` covers:
  - owed items 45 and 46: what changed and why, and what proves it;
  - Still open: the late grant, item 45 (10)'s `.cs` line, and FOUND 1's open objects;
  - who decides: the coordinator.

  No line says the product owner decided anything. It ends with the Claude Code line.
- `squash-subject.txt` 252 bytes: the title plus ` (#PRNUM)`.
- `squash-body.txt`: what and why in three paragraphs, ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- `landing.txt` follows B1923's form, with MAIN MOVES (already moved: 7b0f4f55) and MAIN MOVES AGAIN:
  - 8 check names;
  - merge-ref totals 1581 on both legs (main 7b0f4f55 + 0), succeeded 1577 / 1562, skipped 4 / 19, RULES 500, Ran 111, floor 111;
  - step 6: main's push run PASS by `hosted2.py` at 1581, new main tree `9302f7bf`.
- `words.py` over the title, the squash subject and the squash body: clean (3 files, every class 0). The PR body gives 6 hits, all expected: `coordinator` 2 (the required "who decides" line) and 4 non-ASCII bytes (the required robot line). `landing.txt`, FOR-RECORDS.md and this file are records for Tuesday, never repository text.
- gitleaks over the six texts of this folder other than VERDICT.md, as neutral names: rc 0, `no leaks found`. A fresh control (rc 1, moved to `_quarantine/gl-control2`) ran first. All seven texts, this file's final draft included, were scanned again after a third fresh control (rc 1, moved to `_quarantine/gl-control3`): rc 0, `logs/gl-verdict.log`.
- `build/squash_scan.py` with `#PRNUM` replaced by `#21` and `squash-body.txt`: control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks and CodeQL read as step 3 requires.
FOUND 1 can go to the records, or Tuesday can re-cut that sentence first. Either way it is the coordinator's choice.
