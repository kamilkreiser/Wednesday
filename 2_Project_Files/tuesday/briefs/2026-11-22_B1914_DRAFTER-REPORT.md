STARTABLE: YES

# B1914 DRAFTER REPORT: lane A1 (WP1.4 sign-in state machine, C5), seat Datasec/OXPd2-X28

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1914_SEAT-X28_oxpd2-a1.md` (99097 bytes, 343 lines at the sidecar write; sha256 in the sidecar's `KIT` line). Sidecar: `...a1.md.measured` (`stamp_check.py <kit>` exit 0: 168 claims, 168 measured). Drafted 20:15 to 21:01 AEDT 2026-11-22 by a read-only drafter (Opus). Scratch and every program behind a number: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1914/` (`clone/`, `logs/`, `scripts/`, `scratch/`, `gate/`).

## BLUF
- The kit is startable now. It is a product kit in B1840's form, with B1912's toolchain and lock rules. It covers the per-printer actor, the card paths, the binding rule, a stale-tap guard on arrival time and the four F15 forms. Everything runs against fakes of the identity service and the printer, over the REAL token broker. QR/phone and device-code enrolment are OUT.
- **I built the whole lane as a prototype and ran it** (macOS arm64; 65 heavy jobs, all through `heavy.py` and the wave lock):
  - 55 new test cases.
  - Red first against throwing stubs: `total: 1633`, `failed: 54`. All 54 red rows are SignIn cells. L02 is green against the stubs, as its row says.
  - Green: `total: 1633`, `failed: 0`, `skipped: 4` at `bf6b441e`. With pull request 18's two files placed (blob shas equal to `main`'s): `total: 1634`, `failed: 0` at the new BASE `4e8828ee`.
  - 250 runs of the new assembly: 0 failed.
  - 22 mutants: 21 red on their cells, 1 equivalent survivor (mSupersedeLate), named in the kit.
  - The chain passed: the locked restore with `--force` and `CI=true` (26 of 26 lock files unchanged), both publishes, `GUARD: clean (10 files)` and `GUARD: clean (11 files)`, `Ran 111 tests` OK, `RULES: clean (528 files)` without `--source-documents`.
  - Scans: `WORDS: clean (2 files)`; `gitleaks` reported `no leaks found` (its control fired); the boundary scan was clean, with 23 of 23 controls fired.
- **`main` moved while I drafted.** It went from `bf6b441e` to `4e8828ee` (pull request 18, X27's F13 fix, two Sessions test files only). Its hosted run reads `HOSTED 4e8828ee...: PASS` (hosted2.py). The kit is written against `4e8828ee`.
- Two Questions are STOP-class and need S4 in words:
  - **Q5:** the binding rule.
  - **Q7:** the stale-tap guard, which settles owed item 32's fact (2).

## Facts re-measured (instrument; control)
| Fact | Value | Instrument |
|---|---|---|
| origin `main` | `4e8828ee0259b2605c98ba0f9f319f6527436778` at 20:50:26 (was `bf6b441e` at 20:15:57) | `gh api -X GET .../git/ref/heads/main` under the project GH_CONFIG_DIR |
| pull request 18 | merged 09:35:19Z; compare `bf6b441e...4e8828ee`: ahead 1, behind 0, 2 files (Sessions tests) | `gh api -X GET compare`; blob shas equal to `git hash-object` of the GET'd raw files |
| BASE hosted | `HOSTED 4e8828ee...: PASS` at `--total 1579 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111 --hardened-scan` | `hosted2.py` |
| tree | 500 blobs; 0 paths under `src/Datasec.Suite.SignIn` or `tests/Datasec.Suite.SignIn` | GET tree, jq |
| open PRs / `b1914` refs | 0 / 0 | `gh api -X GET` |
| slnx placement | `PLACED: 2 lines (src at 14, tests at 29)`, both folders `ordinal: True` | `place.py --dry` on BASE's file (and `--write` on the prototype) |
| new lock files | src 17 lines `1a1957a6...`, tests 172 lines `7df6497a...`; 24 existing unchanged | `shasum -a 256` before and after, `cmp` rc 0 |
| toolchain | dotnet `10.0.404`, gitleaks `8.30.1`, cache 121 entries | `--version`, `ls \| wc -l` |
| local totals | red 1633/54 failed; green 1633/0; on 4e8828ee files 1634/0 | `dotnet test` logs, escape codes stripped |
| loop | 50 + 200 runs, 250 pass | the drafter's `scripts/loop-all.sh` via heavy.py |
| test methods | 25 `[Fact]`, 7 `[Theory]`, 30 `[InlineData`, 0 at column 1 | `grep -c -E '^[[:space:]]+...'` per file |
| words / leaks | `WORDS: clean (2 files)`; `no leaks found` (control rc 1) | `words.py`; `gitleaks dir` |
| Server reference | only `Datasec.Suite.Core` | the csproj, read |

## D-decisions (all Tuesday's as coordinator; each is a Q in the kit)
- **D1** A new library that references Sessions only and takes the card STRING. There is no reference to Cards: `CardRead`'s constructor is private and its factories are internal.
- **D2** One Channel and one loop per printer, with a `TapResult` per tap.
- **D3** The card rule: 1 to 32 printable ASCII, not blank, no upper case.
- **D4** The six card paths:
  - The same card signs out with no lookup.
  - A card of the same user (equal as a `Guid`) signs out.
  - Another user's card signs the first out, then signs the second in.
  - An unknown card signs the current user out and reports `UnknownCard`.
  - HPAM's 2-second wait is NOT copied.
- **D5** The binding rule (Q5, STOP-class), two checks:
  - The token's object id must equal the card user's object id, compared as a `Guid`.
  - The grant's subject must equal that object id, checked before the printer is told.
  - On a failure: `BindingRefused`, one audit event carrying no identity, and the grant is disposed.
- **D6** The F15 forms, default `FirstAndLast`, falling back to the display name and then the UPN. Field limits are 255, 128 and 254 (B2:119-120). The user name and the fully qualified name are both the UPN.
- **D7** The stale-tap guard (Q7, STOP-class):
  - It rests on arrival time. `MaxTapAge` is 5 s, a placeholder until spike S1.
  - A stamp from the future is refused.
  - A tap the printer re-delivers after an outage is a NAMED LIMIT.
  - Two alternatives are listed in the kit.
- **D8** A newer tap supersedes an attempt that has not reached the printer yet. This is HPAM's stale-session guard.
- **D9** Every call is bounded at 30 s. A late grant is disposed. One sign-out request follows a failed or timed-out printer step.
- **D10** The queue holds 16 taps; one more is `QueueFull`.
- **D11** `DeviceSignedOutAsync` handles the printer's own sign-out.
- **D12** When the broker refuses, the printer is signed out and the outcome is `SessionRefused`.
- **D13** The session user is the object id; the idle timeout is 30 min.
- **D14** A stop keeps the broker session.
- **D15 / D16** Typed results and masks only; no logging, network, timer or package.
- **D17** The type names.

## Q-questions for Tuesday (defaults assumed in the kit)
- **Q5 (STOP-class): the binding rule.**
  - Default: D5.
  - Alternative A: compare the object ids as text.
  - Alternative B: carry both object ids in the audit event.
- **Q7 (STOP-class): the stale-tap guard.**
  - Default: arrival time, 5 s, and re-delivery after an outage is a named limit.
  - Alternative A: a not-before grace window after a host restart.
  - Alternative B: no age guard in the actor.
- **Q16: should the seat get the prototype?**
  - Default: no. The seat writes its own code (about 2000 lines), and the gate can compare two implementations.
  - Alternative: hand the prototype over as the starting point. This is faster overnight, but the gate then reads only one implementation.
  - If speed matters more tonight, flip this one.
- **Q4: an unknown card while someone is signed in.**
  - Default: the current user is signed out.
  - Alternative: nothing changes.
- **Q6: the default display-name form.**
  - Default: `FirstAndLast`.
  - Alternative: `DisplayName`. The Workpath sources differ (A1:513).
- Q1 to Q3 and Q8 to Q17 are as the kit lists them. Each has a default, an alternative and a cost.

## Chain inputs (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, the stamp | Tuesday |
| 1 | `<src>` (7 files, sha256 in the kit), the origin, BASE's push run | the drafter's scratch, GitHub |
| 2 | the frozen T1 and T2, `place.py`, BASE's slnx | the Step 1 extraction and copy |
| 3 | the two projects and slnx lines, the stubs, BASE's Sessions test lock (for the lock rule) | Step 2; the clone at BASE |
| 4 | the red tree | Step 3 |
| 5 | the green tree with the mutants undone; paths staged | Step 4 |
| 6 | the staged tree, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit, `origin/main` | 7(a); the fetch in 7(b) |

## UNMEASURED
- Anything on Linux, Windows or a hosted runner for this lane. The hosted totals of 1634 and `RULES: clean (528 files)` are PREDICTED.
- Whether the seat's restore writes lock files byte-equal to mine. This is PREDICTED, and a difference is not a stop if the lock rule passes.
- All printer and identity behaviour: `MaxTapAge` and `StepTimeout` are placeholders.
- B06 and B07 (an `AcquireAsync` that answers null; an `Audit` handler that throws) are in the kit but NOT in the prototype, and are marked NEVER RUN.
- The local neutral-object scan (`run_step.py`) was not run on any commit of this lane. Its wordings were measured in `main`'s hosted log.
- The commission said not to touch the SDK key folder, Source_Documents or the NAS. I opened none of them.

## Outside-the-fences disclosure
- **Files I wrote:**
  - The kit, its sidecar and this report.
  - Everything under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1914/`.
  - One temporary file, `/tmp/claude-501/sc.txt` (stamp_check output). It was outside my scratch, so I moved it to `d1914/_quarantine/`.
- **Writes inside the OXPd_2 project:** only through `heavy.py`. That is the shared lock folder `.tools/wave1-heavy.lock.d`, taken and released 65 times by MOVE into `d1914/_quarantine/locks/` (66 entries there). The package cache stayed at 121 entries. I created no `.tools/b1914`.
- **My scratch clone:** a `git clone --no-hardlinks` of B1912's drafter clone (`s310/d1912/clone`, read only), detached at `bf6b441e`, with push URL `invalid://no-push`. The write verbs (checkout, add) ran in my own clone only. I placed pull request 18's two files there from `gh api -X GET` contents.
- **Other reads:** template kits B1912, B1840 and B1913, and `place.py` from `s304/d1841/gate` (copied, then changed by 2 hunks into my gate). The project's CLAUDE.md, CLARIFICATIONS (C-42, C-61, C-68), BACKLOG item 32, and the design and analysis lines cited.
- **No** Jira call, no push, no PR, no Artifact or mail, no message to anyone, no az, docker or ssh, no deletion. I never broke another holder's lock (I waited on B1915's).
