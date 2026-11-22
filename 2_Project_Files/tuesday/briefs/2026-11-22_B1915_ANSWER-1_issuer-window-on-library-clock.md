# B1915 ANSWER-1 (from Tuesday) -- to seat X29's STOPPED line about cell C14 on the hosted Windows leg

**Answer: option (a), a product rule in this lane.** C14 is kept exactly as it is: not dropped, not loosened, not made platform-aware, not a limit. Make ONE new fast-forward commit on top of `759c90609e9a8a71aa4bbef32a8d13f2d1682d77` on the pushed branch `b1915/up-registration-fix-round`. It applies the frozen patch `3-fix.patch` below byte for byte. Then push with no force, read the hosted run, and end `READY B1915: <sha40>`. **Never rebase, amend, reset or force.** A fix round on a pushed branch never rebases.

Marks are as in your kit. MEASURED = the drafter printed it, on macOS arm64, in its own scratch clones `<a1>/clone` and `<a1>/clone2` of your pushed head. RELAYED = read in your STATUS or the hosted logs. DERIVED = source reading. UNMEASURED = nobody has measured it. Here `<a1>` = `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1915a1` (READ and COPY only). The drafter ran nothing on Linux or Windows. The drafter wrote nothing in `<lane>`, `<clone>`, `<repo>` or GitHub (`<lane>/clone` was read back at 21:41: HEAD `759c9060`, `status --porcelain` 0 lines).

## 1. Why Windows accepted the issuer (read from the code and the log; the platform mechanism is UNMEASURED)
- **The code at `759c9060`** (`RegistrationKeys.cs:191-228`, rule 8) builds an `X509Chain` with these settings:
  - `TrustMode = CustomRootTrust`;
  - `CustomTrustStore.AddRange(_issuers)`, exactly the configured issuers;
  - `RevocationMode = NoCheck` and `DisableCertificateDownloads = true`;
  - `VerificationTime = now.UtcDateTime` and `VerificationTimeIgnored = false`, where `now` is the library's `TimeProvider`.
  The library accepts only when all of these hold: `Build` returns true, no exception is thrown, every `ChainStatus` is `NoError`, `ChainElements.Count >= 2`, and the modulus rule holds on `ChainElements[1]`. Nothing in the library checks an element's window itself. Rule 7 checks the LEAF only (`:130-134`).
- **C14's shape** (`CertificateRuleTests.cs:376-413`): the configured issuer is self-signed. So it is the custom root, and (DERIVED) chain element 1. Its window is real-1 day to real+3000 days. The library's clock is real+4000 days: the issuer is EXPIRED by the library's clock and VALID by the real clock. The leaf runs from real-1 day to library+365 days. It is inside its window by both clocks, and it is not time-nested inside its issuer.
- **The log** (`<lane>/logs/hosted/job-windows.log:245-249`, run 45011414586, image `windows-2025-vs2026` at `:17`): `C14 an issuer expired by the library's clock: expected IssuerNotTrusted, nothing was thrown`, at `CertificateRuleTests.cs:406`. "Nothing was thrown" means every condition above held on Windows (DERIVED from `:208-227`). On that leg, `Build` was true, every status flag was clear (no `NotTimeValid`, no `NotTimeNested`), and the issuer's modulus check passed.
- **What the log cannot tell apart (UNMEASURED; only a Windows run can say):**
  - (i) the Windows chain did not test the custom root's window at `VerificationTime`; or
  - (ii) the Windows chain did not judge at `VerificationTime` at all, and used the real clock, by which this issuer is valid.
  Both fit the one red. **Cell C16 below tells them apart on the next hosted Windows run:** under (ii) it is red there.
- **Linux, for contrast** (DERIVED): C14 is green on the hosted Linux leg (your HOSTED RUN). Its control half (the same leaf, not time-nested) is accepted there. So Linux refused the issuer for its window at the library's instant, not for nesting.
- **macOS** (MEASURED): `mVerifySystemClock` and `mTimeIgnored` turn C14 red. So macOS judges at `VerificationTime`.

## 2. The rule
**Rule 8 gains one clause.** After the chain builds with every status flag clear, every element of the built chain must lie inside its own `NotBefore` to `NotAfter` at the library's instant `now`. This covers the leaf, the configured issuer (element 1) and any further element. Both ends are included, in UTC. Otherwise the reason is `IssuerNotTrusted`. There is no new `RegistrationError` member (L01 still pins thirteen) and no public member changes (`InsideWindow` is `private static`).
- **The leaf too:** yes, the loop covers it. That part cannot fire, because rule 7 already refused a leaf outside its window at the same `now`, with `CertificateNotTimeValid`. Rule 7 runs first, so its reason wins.

**State table** (L = the library's clock, the only clock the library reads; R = the real clock).

| Leaf by L | Issuer by L | Outcome on every platform (by the code) | Measured |
|---|---|---|---|
| before or after its window | any | `CertificateNotTimeValid` (rule 7 runs first; unchanged) | P5 (both after): `CertificateNotTimeValid`, macOS |
| inside | before its window | `IssuerNotTrusted` (the new clause) | P4: `IssuerNotTrusted`, macOS |
| inside | after its window | `IssuerNotTrusted` (the new clause) | C14: green on macOS (100 of 100 with the patch); RED on hosted Windows at `759c9060` |
| inside | NotAfter == L exactly | the clause accepts (inclusive); the platform's own answer at the boundary is not ruled on (README limit) | P1: ACCEPTED, macOS; P1b (L one second after): `IssuerNotTrusted`, macOS |
| inside | NotBefore == L exactly | as above | P2: ACCEPTED, macOS |
| inside | inside | the rest of rule 8 decides (flags, two elements, the modulus) | every accepting cell |

**R is never read by the library.** R matters only if a platform's chain ignores `VerificationTime`.

| Case | Outcome by the code | Status by platform |
|---|---|---|
| Inside by L, expired by R | ACCEPTED | **C16** (new): MEASURED on macOS (100 of 100); Linux PREDICTED from §1; Windows UNMEASURED (C16's hosted run is the instrument) |
| Expired by L, valid by R | refused | C14 |

**The patch:** `<a1>/3-fix.patch`, sha256 `3008794df1f21c16b7dafccc5297104b0f6a29dbc5e8155a5da2c67a9e7488cc`, 9804 bytes, 150 lines, printable ASCII and LF (control: a planted tab reads 1). It changes three of your eight owned files, and no other path. `git apply --check` on a fresh clone of your pushed `759c9060` gave rc 0, and `apply` gave rc 0 (MEASURED in `<a1>/clone3`). The three files are `cmp`-equal to `<a1>/clone`'s. A second `--check` on the applied tree is refused, rc 1.

| File | numstat against `759c9060` (MEASURED) | sha256 after (lines) |
|---|---|---|
| `src/Datasec.Suite.UniversalPrint/Registration/RegistrationKeys.cs` | 27 2 | `0d6c7c33f64a29fe9df68df60cea5e54f5a91d3628b953cc8dcacd391e959a76` (339) |
| `src/Datasec.Suite.UniversalPrint/Registration/README.md` | 10 8 | `b45f8c5375ad76a01a7fe855e1bece653ef3b6a80275f628cd210b0367719a90` (139) |
| `tests/Datasec.Suite.UniversalPrint.Tests/Registration/CertificateRuleTests.cs` | 44 1 | `cd08ec63c0362982455092d9dfc91767aa39d9c8bfdf52407cb33f91e1420e38` (532) |

- **The product change:**
  - `ChainsToConfiguredIssuer` gains, after the status loop and before the return: `foreach (var element in chain.ChainElements)`, refusing (`return false`) unless `InsideWindow(element.Certificate, now)` (`:230` and `:232` after the patch).
  - A new `private static bool InsideWindow(X509Certificate2, DateTimeOffset)` (`:242`). It is inclusive at both ends and converts to UTC as `RegistrationRecord` does (`:161-162`). Any exception reads false.
  - The method's summary names the new clause.
- **The README:**
  - rule 8 (it starts at `:70`; the new clause is at `:72-74`);
  - two Limits lines (`:126-129`): the wall-clock-set-back line now names the issuer and rules 7 and 8; the boundary line now says rules 7 and 8.
- **The test file:** the class summary reads `Cells C01 to C16`, plus the new cell C16 (`:479`), described in §5.
- **Ordering against the existing checks:**
  1. Rule 7 (the leaf on L) runs first and wins when the leaf is outside its window, whatever the issuer. P5 shows this.
  2. Inside rule 8 the order is: `Build` and the catch, then the status flags, then the new window clause, then `Count >= 2`, then the modulus rule. All of them give the one reason `IssuerNotTrusted`, so the order inside rule 8 changes no reason.
  3. No existing cell pins another reason for these shapes. C07 pins `CertificateNotTimeValid` for a leaf one second outside its window under an issuer inside its own; rule 7 still decides that. C07's boundary helper allows `IssuerNotTrusted`. C01's allowed reasons already include `IssuerNotTrusted`.
- **Totals with the patch (MEASURED, macOS arm64, `<a1>/clone`, every job through the kit's `heavy.py`):**
  - UniversalPrint assembly: `Total: 346, Errors: 0, Failed: 0` (345 at `759c9060`; +1 = C16).
  - Whole solution `dotnet test -c Release --no-build`: `total: 1587`, `failed: 0`, `succeeded: 1583`, `skipped: 4`, `failed Datasec.` lines 0 (control: your `red-test.log` reads 4). The same four numbers came again on `<a1>/clone3`: the final patch applied to a fresh copy of `759c9060`, with a fresh locked restore, build and test (21:47).
  - Build: `0 Warning(s)`, `0 Error(s)`.
  - Loops of 100: `loop-green-C14 runs 100 pass 100 fail 0 other 0` and `loop-green-C16 runs 100 pass 100 fail 0 other 0`.
  - `repo_rules.py` (no `--source-documents`): `RULES: clean (500 files)`, rc 0. `unittest`: `Ran 111 tests`, `OK`.
- **The count is 1587, not 1586, because C16 is added.**

## 3. How it is proved, honestly
- **On macOS arm64 C14 is green with or without the rule**, because the platform already refuses the expired issuer. MEASURED: green 100 of 100 at `759c9060` (your loop) and with the patch (the drafter's).
- **So a mutant that removes the rule stays green on macOS.** MEASURED with `mutants_a1.py`:
  - `mWindowRuleOff` (the clause made a no-op) GREEN;
  - `mWindowNotAfterOff` GREEN;
  - `mWindowNotAfterExclusive` GREEN.
  The first two are PREDICTED red on hosted Windows (C14). That is the same standing as `mFixUndone`, which is killed on hosted Linux only.
- **No local red-first is possible.** The new clause can fire only on a chain the platform has already accepted, and macOS does not accept one with an issuer outside its window. A cell that drove `InsideWindow` directly would be a compile error at `759c9060`, not a red. Even then it would not see the call removed.
- **The red-first instrument is the hosted Windows leg.** C14 RED at `759c9060` (run 45011414586, RELAYED and read at source) is the red. C14 GREEN on the Windows leg of your new head is the proof. If it is still red there, the rule did not close the gap: `STOPPED: NEEDS TUESDAY`, never a loosened cell.

## 4. Your steps (Steps 0 to 7 of your kit still bind; these replace its Steps 3, 4 and 7(b) for this commit)
1. **Setup.**
   - `mkdir '<lane>/gate-a1'`.
   - Copy these three files from `<a1>` into it with `cp -c`, then print their sha256. Any difference is a STOP:
     - `3-fix.patch` `3008794df1f21c16b7dafccc5297104b0f6a29dbc5e8155a5da2c67a9e7488cc`
     - `commit-message-2.txt` `2d9023d4423683d5ca568965ee545d8498e5e5faa1f393998abb6ea361a15740`
     - `gate/mutants_a1.py` `a4f21ef682a651ced3bcdfc8ddd5d46e194cbdd1215d6bc04f1bc6b3c74f4254`
     `mutants_a1.py` is your `mutants.py` plus three window mutants at the end of its list. Read its header; never edit it.
   - Check the state of `<clone>`: `rev-parse HEAD` = `759c90609e9a8a71aa4bbef32a8d13f2d1682d77`, and `status --porcelain` 0 lines.
   - Origin (`gh api -X GET`):
     - `matching-refs/heads/b1915` must be ONE row, at `759c9060`;
     - `refs/heads/main` should be `4a0a9717277f60647dfc174e60ec04fc7008e615`.
   - If main is later than `4a0a9717`, run `compare/4e8828ee0259b2605c98ba0f9f319f6527436778...<main>`. If any file there is under either `Registration/` folder, STOP.
   - Write `<lane>/predictions-2.txt` (sha256 printed) BEFORE any edit, with the numbers of steps 2 to 6 below.
2. **Apply.**
   - `git -C '<clone>' apply --check '<lane>/gate-a1/3-fix.patch'` rc 0, then `apply`.
   - The three sha256 must equal the table in §2. The other five owned files keep your green column.
   - `git -C '<clone>' diff --name-only` lists exactly the three paths.
3. **HEAVY, each through `<lane>/gate/heavy.py`:**
   - build: `0 Warning(s)`, `0 Error(s)`;
   - whole solution: `total: 1587`, `failed: 0`, `succeeded: 1583`, `skipped: 4`;
   - `loop.sh` 100 runs, 600 s, for C14 and for C16, each `runs 100 pass 100 fail 0 other 0`. C16's full name is `Datasec.Suite.UniversalPrint.Tests.Registration.CertificateRuleTests.C16_AChainInsideItsWindowsByTheLibrarysClockAndExpiredByTheRealClockIsAccepted`.
4. **Mutants:** `python3 -I '<lane>/gate-a1/mutants_a1.py' '<lane>' '<clone>' 'B1915 seat X29'`. It prints 14 lines; MEASURED here, each `Total: 346, Errors: 0`:
   - RED on the named cell only (`Failed: 1`): `mNoZeroPkcs8` K06; `mReadCertLoose` R05; `mTimeIgnored` C16; `mVerifySystemClock` C16; `mDeleteUnlocked` X02; `mIssuerOnCallerPath` T11; `mDisposedAnswerHeld` T12; `mModulusOff` C15.
   - GREEN: `mCatchNarrow`, `mFixUndone`, `mModulusNoLength`, `mWindowRuleOff`, `mWindowNotAfterOff`, `mWindowNotAfterExclusive`.
   - Every line ends `undo cmp 0`.
   **This is a change from your kit: `mTimeIgnored` and `mVerifySystemClock` are now killed by C16, no longer by C14** (MEASURED: with the rule alone and no C16, both read GREEN, `<a1>/logs/mutants-rule-only-2.out`). Then build again.
5. **Step 5 (THE CHAIN), whole, as your kit says.**
   - Expect `total: 1587` from the whole solution.
   - The guard lines are unchanged: 10 and 11 files. The drafter did not run the publishes or the guard: NOT RUN here.
   - Expect `Ran 111 tests` and `RULES: clean (500 files)` (both MEASURED here).
6. **Step 6 (CHECKS), staged by name: the three paths.**
   - (a) `diff --cached --name-status 759c9060` is 3 rows, all `M`. `diff --cached --name-status 4e8828ee` is still your eight rows. The SHARED FILES `diff --quiet` gives rc 0, with your control. `--numstat 759c9060` must match §2.
   - (b) ASCII, no tab, LF and a final newline: 0 per file.
   - (c) **Scanner control FIRST**, before the commit. Then `gitleaks dir '<clone>'`. Then the three staged blobs and `commit-message-2.txt` under neutral names in a NEW folder: rc 0 (the drafter's neutral copies of the patch, the message and the three files read `no leaks found`; its control rc 1).
   - (d) The added lines against `759c9060` (81 lines, MEASURED), plus `commit-message-2.txt`, through `words.py`: `WORDS: clean (2 files)` (MEASURED).
7. **Commit:** `git -C '<clone>' commit -F '<lane>/gate-a1/commit-message-2.txt'`.
   - The subject is 258 bytes; the file is 316 bytes and 3 lines.
   - `log --format='%h %ae | %ce' 759c9060..HEAD` gives ONE row, with both addresses equal to the clone's own `user.email`. Never override the identity.
   - The parent must be `759c9060`.
   - Then `run_step.py` (the neutral scan of every stored object), as in your Step 6(c).
8. **Before the push (replaces kit 7(b)):**
   - `git -C '<clone>' fetch origin main`.
   - `rev-parse origin/main`: `4a0a9717` expected (a later main: step 1's compare again).
   - `merge-base origin/main HEAD` must print `4e8828ee0259b2605c98ba0f9f319f6527436778`. **`merge-base --is-ancestor origin/main HEAD` is now rc 1 by design. Main moved, and that is no STOP.** MEASURED by `gh api -X GET compare/4e8828ee...4a0a9717` at 21:26: ahead 1, behind 0, files `build/repo_rules.py`, `build/tests/test_repo_rules.py`, `packaging/linux/Dockerfile`. None is under `Registration/`, so the move is harmless.
   - `ls-remote origin refs/heads/b1915/up-registration-fix-round` must print `759c9060...`. Anything else: no push, STOP.
   - **Do not rebase.**
9. **Push:** `git -C '<clone>' push origin HEAD:refs/heads/b1915/up-registration-fix-round`, with no `--force`, no `+`, no lease. It is a fast-forward from `759c9060`. Any `[rejected]`, `[remote rejected]` or `remote: error` line: no second attempt, STOP.
   - **Read back:**
     - `matching-refs/heads/b1915`: one row, your new sha;
     - `compare/759c9060...<sha>`: ahead 1, behind 0, the 3 files;
     - `compare/4e8828ee...<sha>`: ahead 2, the eight owned paths;
     - `compare/main...<sha>`: DERIVED behind 1, ahead 2;
     - pull requests from this branch: 0.
10. **Hosted:** `python3 -I '<lane>/gate/hosted2.py' <sha40> '<lane>/logs/hosted-2' --wait --total 1587 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111 --hardened-scan`.
    - Use your OWN Step 5 total if it differs from 1587, and say why.
    - **The rules floor did not change on main:** `4a0a9717`'s push `rules` job (137175783996) printed `Ran 111 tests`, `UNIT-TEST FLOOR: ran 111, floor 111`, `RULES: clean (500 files)` (MEASURED from its log). In any case, your branch's run reads your branch's tree.
    - Print every `failed Datasec.` line of both legs. Count it anywhere in the line: the timestamp comes first.
    - PREDICTED Windows: `total: 1587`, `succeeded: 1568`, `skipped: 19`, `failed: 0`. **C16 on Windows is UNMEASURED.** A red C16 there means the Windows chain judges on the real clock (§1 reading (ii)). A red C14 there means the clause did not close the gap. Either one is `STOPPED: NEEDS TUESDAY`, with the lines quoted, never a loosened cell. Your kit's 7(f) "a red job is yours ONCE" is spent by this commit.
    - Last line on success: `READY B1915: <sha40>`.

## 5. What else it changes
- **Cells:**
  - one new cell, **C16**: a chain inside its windows by the library's clock and expired by the real clock is ACCEPTED, version 2. The library's clock is real-2000 days; the issuer runs from real-3000 to real-1000 days and the leaf from L-1 to L+365 days, nested inside its issuer.
  - No existing cell, helper or assertion changes. C14 is byte for byte unchanged.
  - Count: `[Fact]` in `CertificateRuleTests.cs` goes from 19 to 20 by the indented pattern (column 1: 0). The totals are UniversalPrint 345 to 346 and whole solution 1586 to 1587, on every leg.
  - **Why C16 is needed:** with the clause, the library judges every element on its own clock. Without C16, the two clock mutants of the kit's item 54 survive on macOS (MEASURED). C16 kills both there (MEASURED), and it also measures §1's question on Windows.
- **Public members:** none added, removed or changed. No `RegistrationError` member added.
- **Lines:** product 27 added and 2 removed in `RegistrationKeys.cs`; README 10 and 8; test 44 and 1. Against BASE `4e8828ee` the branch then reads: `RegistrationKeys.cs` 67 10, `README.md` 22 11, `CertificateRuleTests.cs` 150 1, and the other five as at `759c9060`.
- **For the gate's probe list (G1, Tuesday's):**
  - an issuer whose NotAfter equals the library clock exactly: ACCEPTED on macOS (P1, MEASURED);
  - one second after: `IssuerNotTrusted` (P1b);
  - NotBefore equal: ACCEPTED (P2);
  - an issuer before its window: `IssuerNotTrusted` (P4);
  - leaf and issuer both after their windows: `CertificateNotTimeValid` (P5);
  - an issuer valid by the library clock and expired by the real clock: ACCEPTED on macOS (C16). On Windows this is UNMEASURED until C16's hosted run. If Windows refuses it, the cause is the platform's chain, not this clause: the clause never reads the real clock.
  The probes were run on macOS only, in a scratch test class `<a1>/probes/ProbeA1.cs` that is in no patch (log `<a1>/logs/c2-probe-run2.log`). Also for the gate: your H36 (a null task from the issuer), unchanged by this answer.

**What to write in STATUS:** the sections of your kit for this commit, under `## FIX 2 (ANSWER-1)`. In DEVIATIONS, record "kit 7(b)'s is-ancestor check replaced by ANSWER-1 §4.8" and "mTimeIgnored/mVerifySystemClock now killed by C16 (ANSWER-1 §4.4)". Your earlier STATUS lines stay as written. FOR RECORDS adds (RELAYED):
- "Item 54 F2 / the hosted Windows gap: rule 8 now requires every chain element inside its window on the library's clock (cell C14, red on hosted Windows at 759c9060); cell C16 a chain judged on the library's clock alone".
