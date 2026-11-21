GATE B1838: GO WITH FINDINGS @ 70c1fad on main 5e36d8d

Gate G1 Tier 1, round 1 of 2, reader B1838 (the whole lane, items 1 to 8), OXPd 2 WP1.5, the session and token broker,
head `70c1fad55128667e62fa5379719dfc6e0ba3ac1b` (one commit, one parent `5e36d8dca42966395ea3dd014c7f788409eb585f` = main).
Read and measured 2026-11-21 17:03 to 17:45 AEDT (clocks by `date`) on Opus 5.5, in the reader's own clone (cloned from the
origin with the deploy key into `/private/tmp/b1838-gate/clone`, push URL `invalid://no-push`; the working copy where git
write verbs and builds ran is `<session scratchpad>/b1838/clone`, push URL `invalid://no-push`, because the workspace hook
refuses git write verbs outside the session scratchpad). Logs and programs: `/private/tmp/b1838-gate/` (`logs/`, `out/`,
`scratch/`, `mut.sh`). Every heavy job (restore, build, test, each mutant: 16 jobs) went through the kit's `heavy.py`
unchanged (sha256 7 of 7 equal to the kit's list): load read first, the wave's lock by `mkdir` of exactly
`<project>/.tools/wave1-heavy.lock.d` with an `owner.txt`, closed local proxy, released by MOVE into
`/private/tmp/b1838-gate/_quarantine/locks/`. The lock was not held while reading; waits behind the second reader were
not findings. No token, handle, subject or key value is in this folder; every value used is synthetic and made at run
time.

**BLUF.** The lane does what the kit and ANSWER-1 say, and the reader could not make it hand out a token of another
subject, write a record of an ended session, leak a secret into text or a clear store file, or decode a token. Scope,
frozen texts, build (0/0), suite (947/0), hosted run (PASS) and the mutants all hold. **No Blocker, no Major.** Five
Minor findings, none a reason not to merge; the one to read first is F1: **a refresher that blocks its calling thread
before it returns a task is not bounded by `RefreshTimeout`** (measured; it needs a refresher that breaks the
Task-based contract; the lock is not held, other sessions and `SignOut` keep working, nothing is written; a one-line
fix or a README limit). Plain words: the branch can land when the second reader also passes; main has not moved, so the
pull request's checks build the head's own tree.

## Findings

| # | Severity | Blocks? | Finding | Recommendation |
|---|---|---|---|---|
| F1 | Minor (the first to read) | No | **A synchronously blocking refresher hangs its callers past `RefreshTimeout`.** `ObtainAsync` calls `RefreshAsync` synchronously (`TokenBroker.cs:334`), which calls `_refresher.RefreshAsync` (`:389`) before `WaitAsync` (`:390`) exists. Measured (`reader-probes-output.txt`, SYNC-BLOCK): a refresher that blocks its thread, the test clock moved 31 s past the 30 s bound: the caller still waiting 3 s (real) later, 0 timers made; meanwhile another session's `GetTokenAsync` and `SignOut` of the blocked session answered at once (the broker lock is NOT held during the call); on release the caller got `SessionNotFound` and no record of the signed-out session was left. Every asynchronous hang shape is bounded (kit H8 rows; the reader's: an answer 1 tick before the bound accepted, at exactly the bound `RefreshTimedOut`, a re-entrant refresher awaiting its own refresh bounded). Graded Minor because it needs an `ITokenRefresher` that blocks before returning its `Task` (the real one is WP1.4's, on Microsoft's library, UNMEASURED); the second reader owns the bound and may weigh it higher. | Start the call after `await Task.Yield()` or through `Task.Run`, so the bound covers it (the blocked thread still leaks); or a README `## Limits` line. |
| F2 | Minor (text owed; no cell) | No | **D7 across a restart: a wall clock set back while the server runs, then a restart inside the window, lengthens a session's idle life.** Measured: idle 30 min; wall set back 25 min one minute after the last activity; restart at true idle 29 min (wall idle 4 min): restored; at true idle 49 min a read HANDS OUT A TOKEN. The seeded fuzz saw restored idle starts moved later by up to 32 min 35 s (seed 19). Bounded by the session's idle timeout (at most 24 h by D10) and only for steps smaller than the time since the last write. The kit says "across a restart only the wall clock exists" and drops records dated later than the clock (built, cells R05 and the reader's), but this case (the step before the restart, not during the down time) is neither a cell nor a README limit, and the README says "A wall clock set back keeps nothing alive". | README `## Limits` sentence; FOR TUESDAY whether to keep it (a fix needs a time source that survives a restart). |
| F3 | Minor | No | **The record writer can leave an uncleared copy of the token's base64 in a grown buffer.** `SessionRecord.Write` sizes `ArrayBufferWriter` at `1024 + base64 + 2 x (user + subject)` (`SessionRecord.cs:68`) and clears only the final buffer (`:104`). JSON escaping writes up to 6 bytes per character and `Utf8JsonWriter` asks for 3x per string: measured by allocation, a user and subject of 40 `+` or 40 accented characters made the buffer GROW (5,605 B beyond estimate plus record; 60 `+`: 5,685 B); ASCII users of 1 and 64 characters did not (223 and 221 B). A growth copies everything written so far (the subject comes after the access and renewal base64) into a new array and leaves the old one to the collector unzeroed, against D12 "every buffer that held clear token bytes is cleared". Memory only; not reachable from a store file or a text. Whether real subjects hold escaped characters is UNMEASURED (`+` and `'` occur in mail addresses). | Size the estimate with 6 bytes per string character (or write into a buffer the broker owns and clears on growth); a cell that measures the allocation. |
| F4 | Minor (cells) | No | **Two built rules have no cell that can fail.** (a) The `written` instant later than the clock (`TokenBroker.cs:749`): the reader's mutant mWritten (that clause removed) leaves all 53 lane tests green; only the reader's own restore probe goes red. (b) A record-store READ that throws at restore (the builder's named limit): measured by the reader, counted unreadable and DELETED (2 of 2 sessions erased), so a transient read error at start ends every session (fail closed; records). | Add both cells (R05 row with `written` ahead; a throwing `TryLoad` at restore). |
| F5 | Minor (text) | No | (a) D11 says a record is restored when its idle time is "at most" both bounds; the code restores only when LESS (`idle >= ...` drops, `:749`), consistent with the live rule (`:619`); fail closed by one tick, measured ("idle exactly" record dropped). The README says "less than", so code and README agree; the kit's wording differs. (b) `SignOutReason.RestartWindow` is raised by no path (DEVIATIONS 8): a public enum value with no meaning yet. | Records: say "less than" in the kit's successor; drop or document the unused reason when the host wiring lands. |

## 1. Scope (measured in the reader's clone)

`git diff --name-status 5e36d8dc 70c1fad`: 35 rows, 34 `A` (22 under `src/Datasec.Suite.Sessions/`, 12 under
`tests/Datasec.Suite.Sessions.Tests/`), 1 `M` `Datasec.Suite.slnx`; 0 rows outside (control: the same filter counts the 22
src rows). Solution file numstat `2 0`, the two kit lines, each folder in ordinal order (Sessions after Server; Sessions.Tests
after Secrets.Tests), 21 lines. `diff --quiet` over `src/Datasec.Suite.Secrets`, its tests, `Directory.Packages.props`,
`Directory.Build.props`, `global.json`, `.github`, `build`, `README.md`, `NuGet.config`, `.gitignore`, `.editorconfig`,
`packaging`: rc 0. Lock files changed: only the two new ones. T1 and T2 extracted by program from the stamped kit: 8 lines /
258 B / `1fcdc97e...` and 12 / 350 / `e6ca9be1...`, each file byte-equal (control: T1 block vs T2 file False). References:
the library's `deps.json` lists `Datasec.Suite.Secrets` only; its `using` lines are `System.Buffers`, `System.Buffers.Text`,
`System.Security.Cryptography`, `System.Text`, `System.Text.Json`, `Datasec.Suite.Secrets` (no `System.Net`, identity or
logging). No 64-hex, no 43-character base64url, no JWT-shaped literal in 3,886 added lines (controls fire); the 21
long mixed literals are all `contentHash` lines of the two lock files. 0 bytes outside printable ASCII. `words.py`
(control 13 of 13) over the added lines without lock files and the commit message: `WORDS: clean (2 files)`; with the lock
files: 4 hits, all `net10.0/linux-x64` / `win-x64` written by the restore (DEVIATIONS 3, accepted). gitleaks 8.30.1 with
the workflow's four options over the 34 lane files by name and under neutral names: rc 0 each; planted control rc 1.

**No token is decoded, parsed, inspected or minted** (Stamp S4 Q1). Searched: `FromBase64`, `Base64Url.Decode`,
`JsonDocument`, `JsonSerializer`, `Split(`, `IndexOf(`, `Jwt`, `claim`, `unique_name`, `preferred_username`, `upn`,
`Encoding.*.GetString`, `Parse(`: the only decode is `GetBytesFromBase64` at `SessionRecord.cs:209,218,221`, undoing the
record's OWN base64 layer; the bytes are copied, never read. Token bytes are only cloned, zeroed, base64-written into the
record and copied into `AccessToken`. The one `new AccessToken(` is `TokenBroker.cs:615`, inside `HandOutLocked`, whose
first statement is the ordinal subject comparison (`:609`); every hand-out path (`:298`, `:352`, `:263`) goes through it.
No text in the lane says the product owner decided anything about the broker (words scan; manual read of README and
comments).

## 2. The contract and the required section, the reader's own inputs

The reader's probe file (`reader-probes.cs.txt` in this folder; 37 test cases beside the lane's 53; run in the reader's
clone only, never pushed): 90 of 90 green at the head (`logs/probes-2.log`). Every outcome was a token for the right live
session or `TokenBrokerException` with no inner exception; no other exception, no hang (each wait raced a real guard).

- **H1-H4 handles:** 3,730 handles (1,000 random of the right shape; lengths 0, 1, 42, 44, 10000; 10 out-of-alphabet
  characters; one character changed to each of the 63 others in each of 43 places: 2,709, which includes every
  non-canonical last character that decodes to the same 32 bytes; last byte plus one; padded, trailing newline, case
  swapped, null), each through `GetTokenAsync`, `GetNewTokenAsync` and `SignOut`: 11,198 calls, all `SessionNotFound` or
  `false`, ONE distinct message, 0 refresher calls; the right handle with another serial, the serial in lower case, one
  character longer or shorter, and another device's handle: not found; ended by sign-out, new sign-in, `Sweep` expiry and a
  refresh of another subject: not found; the issued handle still worked.
- **H5/H11/Q9 subjects:** 42 near subjects (one character changed in each place, one letter upper-cased in each place,
  leading or trailing space, NUL, all upper case, empty, composed vs decomposed accent): 42 sign-ins refused
  `SubjectMismatch` with nothing kept and no event; the same 42 as refresh answers: each ended the session (event reason
  `SubjectMismatch`), no record left, raw scan clean for both grants.
- **H7-H10 refreshers (20 shapes):** async throw with the token text and the user in the message, a throw FROM the
  interface call itself, a null task, a cancelled task, the refresher's own `TimeoutException`, an
  `OperationCanceledException` from the call -> `RefreshFailed`; null, disposed, expiry now, now minus 1 tick,
  `MinValue`, empty access -> `RefreshAnswerRefused`; access or renewal at cap plus 1 -> `TokenTooLarge`; another subject
  by case, empty subject -> `SubjectMismatch` and the session ended; expiry plus 1 tick, `MaxValue`, access exactly at the
  cap, empty renewal -> accepted. After every refusal the held grant was unchanged and handed out; texts clean.
- **H8 bound:** see F1 and the rows there; the late answer's arrays read zero and a restart reads the OLD token.
- **H12/H13:** 1,000 concurrent `GetNewTokenAsync` -> 1 refresher call, 1,000 equal tokens; 1,000 waiters and a
  `SignOut` during the refresh -> 1,000 `SessionNotFound`, the answer zeroed, no record, raw scan clean.
- **H14 clocks (16 rows):** wall back 1 h / 10 years with the monotonic clock past the idle deadline, monotonic back
  1 day (a faulty provider) with the wall past it, wall forward 1 day / 10 years, monotonic forward alone: expired;
  29 min on both, wall back 1 h alone: alive. Token rows: inside the margin on either clock (each with the other clock
  stepped) -> exactly 1 refresh; outside -> 0; an expired token with a failing refresher on either clock -> never handed
  out. No life lengthened while running (F2 is across a restart).
- **H15 restart:** 50 crafted records through `ISecretStore.Put` (format 2, as text, 1.0, not first; id of another
  record, upper case, null; serial with a space, empty, 129, null; platform 0, 3, as text; OXPd 1.x without or with a
  31-byte hash; OXPd 2 with a hash; hash missing; user empty or null; subject by case, of another user, null; idle 0,
  over 24 h, negative, `Int64.MaxValue`, fractional; access empty, not base64, a number, over the cap; renewal over the
  cap; expiry `Int64.MaxValue`; last activity and `written` 1 s in the future; idle passed, idle exactly, window passed;
  extra, duplicate and missing members; a 200,000-character nested value; trailing data; not JSON; an array; a comment;
  a BOM; invalid UTF-8; one byte) plus a well-formed control and 3 live sessions: `LastRestore` restored 4, expired 5,
  unreadable 45, deleted 50; none of the 50 left or restored; a `sessions/` name of 33 hex and an `other/` name
  untouched; the OXPd 1.x handle still worked. Expired and future-dated records also in the fuzz (below).
- **R03 as amended (fail closed):** one bit flipped at EVERY one of the 776 byte places of a record file, a restart per
  place: 776 of 776 `StoreFailed` from the constructor, no inner exception, every record file byte-equal afterwards; the
  store itself never refused to open; 0 starts. The lane's R03 foreign row also green in the reader's run. **No path
  starts the broker over an unreadable record file.** The only start past an unreadable record is a record store whose
  READ throws while its listing works (a fake): that record is counted unreadable and deleted, never restored (F4 b).
- **H17 store failures:** write at sign-in -> `StoreFailed`, nothing kept, no event; write at an accepted refresh and at
  activity -> the new token returned, written after the store heals (a restart reads it); delete failing at sign-out,
  at a new sign-in, at expiry by `Sweep` -> `StoreFailed`; at expiry by a read -> `SessionExpired`; at a refresh of
  another subject -> `SubjectMismatch`; in every case the session is ended in memory and the record is gone after the
  store heals and `Sweep` runs; a listing that throws -> `StoreFailed` from the constructor.
- **Seeded model-based fuzz:** seeds 1 to 20 (`new Random(seed * 7919)`), 300 operations each (6,000): sign-ins of 4
  users on 5 devices on both platforms (one in ten stating the wrong subject), reads and renewals by key, by handle and
  by a wrong key, refreshers answering well, another subject, expired, null, throwing, hanging and late, sign-outs by key,
  handle and ended handle, `Touch`, `Sweep`, clock steps on either clock in both directions, and restarts (148 in all).
  After every operation: every handed-out token (652 in all) was the right subject's, of a live session, not expired on
  either clock, not idle; the store's `sessions/` names equalled the live sessions exactly (no record of an ended
  session, none written after its delete); restored sessions kept their user and id.

## 3. Nothing leaks

Every `ToString()` and exception message the probes produced (14,941 texts in the handle probe alone) scanned for
the access bytes, renewal state, user/subject, handle text and handle bytes, serial and platform session id, each in raw,
UTF-8, lower and upper hex, base64 and base64url with and without padding, UTF-16 LE and BE, and base64 of the full
groups at all three alignments (15 forms): 0 hits. The raw store files (every byte of every file under the root, a
planted control found first) after sign-in, an accepted refresh, sign-out, expiry, a new sign-in and a restart, for 15
needles including the handle's SHA-256: 0 hits. Disposal proved by reading the arrays: a replaced grant after a refresh,
an ended grant after sign-out, every grant after broker disposal, `TokenGrant.Dispose`, `AccessToken.Dispose`, the
renewal copy handed to the refresher, the refresher's accepted answer, the late answer, and the record bytes the store
returns at restore: all zero. Gap: F3 (a grown writer buffer in memory).

## 4. Time (D7)

Both clocks on every deadline (`IdlePassed` `:618-620`, `RemainingLife` `:623-629`, answer acceptance `:464-465`); the
earlier wins. No timer of the library's own and no thread: the only words found are `WaitAsync` with the broker's
`TimeProvider` (the kit's own mechanism, which makes one provider timer per refresh) and a `ContinueWith` that disposes a
late answer; no `Thread`, `Task.Run`, `Task.Delay`, `Timer`, `DateTime.Now`, `Stopwatch`, `Environment.`. Restore drops a
record whose last activity OR write instant is later than the wall clock (both measured; the second only by the reader's
probe, F4 a). A step while running never lengthened a life (H14); across a restart see F2.

## 5. Build, suite, hosted

Through the lock: `dotnet restore --locked-mode -p:NuGetAudit=false` with `CI=true` rc 0 (closed proxy at 127.0.0.1:9, so
nothing could be fetched; 0 log lines naming http, fetch or download; `git status --porcelain` 0 lines after); build
Release `0 Warning(s)` `0 Error(s)`; the whole suite `total: 947`, `failed: 0`, `succeeded: 943`, `skipped: 4`. The
NuGet audit is off because the closed proxy refuses its request; the hosted legs run it. Hosted run 44873292565 of
70c1fad5, read by GET with the kit's `hosted.py` (unchanged): `HOSTED 70c1fad5...: PASS`; linux and windows `total: 947`
twice each, `failed: 0`, skipped 4 / 19, `0 Warning(s)`, `0 Error(s)`, `GUARD: clean (10 files)` / `(11 files)`; rules
`Ran 53 tests`, `UNIT-TEST FLOOR: ran 53, floor 53`, `RULES: clean (325 files)`; secret-scan both PLANTED-CONTROL lines
and `no leaks found` x3; control run with `--skipped-linux 5` printed `FAIL 2`. Windows log: 20 lines holding `skipped`,
0 name a Sessions test (19 name Secrets). Main 5e36d8dc's own hosted run: PASS, total 894, `GUARD: clean (10 files)` /
`(11 files)`, so the guard counts did not move; `src/Datasec.Suite.Server` names nothing of Sessions (0 files). Code
scanning: 0 analyses for the branch ref; 0 open alerts on main; C# CodeQL cannot extract on this arm64 machine (NOT RUN),
the pull request's scan is the only C# proof.

## 6. Mutants (the reader's own, each with the Edit tool, build and test of the Sessions project as one locked job, undone with the Edit tool and proved by `git diff --quiet -- src` rc 0 or `--stat` showing only the next mutant)

| Mutant | Edit | Red by assertion (lane cells / reader probes) |
|---|---|---|
| mSubj | hand-out comparison -> `Subject is null` | U04 (the only public-path-unreachable cell, as designed) |
| mRace | single-flight always starts a new refresh | F08 x3; the run then aborted (rc 134) in the reader's re-entrant refresher probe, which recursed without single-flight |
| mLate | still-current check -> `_disposed` only | F09; reader: 1,000 waiters + sign-out; blocking refresher |
| mTimeout | bound -> infinite | F05 x2 (one by its 10 s guard), L01; reader: bound probe, 20 fuzz seeds |
| mWall | monotonic halves of idle and remaining life inert | E04, E06, F02 monotonic; reader: clocks, 19 fuzz seeds |
| mRestore | idle and window tests of D11 never true | R01, R02; reader: restart over 50 records |
| mId | session id = first 16 bytes of the access token | P01 ("needle 5 found in clear"), P02, P03, R01-R04, B04, B06, E02; reader: 24 tests |
| mZero | `TokenGrant.Dispose` does not clear | L02, F05 late, F06 x3, F09; reader: raw files and disposal, 1,000 waiters, bound |
| mPsid (own) | key lookup ignores serial match and platform session id | B04 (the reader's fuzz did NOT catch it) |
| mWritten (own) | restore ignores a `written` instant in the future | lane: NONE; reader: restart probe only (F4 a) |
| mAnswerMono (own) | answer acceptance ignores the monotonic clock | F06 "later by the wall clock, earlier by the monotonic" |

After the last undo: `git diff --quiet -- src` rc 0; the product source equals the head, whose whole-suite run is item 5.

## 7. The builder's deviations and named limits

1 R03 amended by ANSWER-1: accepted (measured 776 of 776, above). 2 `NuGetAudit=false`: accepted (kit-directed). 3 four
word hits in the lock files: accepted (restore-written identifiers, same strings on main). 4 mKeepCorrupt proven by R04:
accepted. 5 mTimeout's two reds: accepted (reproduced). 6 the probe test moved to quarantine: accepted (not in the tree).
7 L04 skips compiler-generated members: accepted. 8 `RestartWindow` never raised: Minor text (F5 b). 9 the stray
`rm -f /dev/null`: accepted, no effect (records). 10 local `repo_rules.py` R5 red on main from lane C's 37 files: not this
lane (the reader did not rerun it; records). 11 a worktree left in the seat's clone: accepted (records). Named limits: a
throwing read at restore (F4 b, now measured); two records of one device (NOT tested by the reader); names under
`sessions/` not 32 hex (measured untouched). Builder choices in FOR TUESDAY Q15 (a failed erase at a new sign-in refuses
the new sign-in after ending the earlier; `Sweep` throws after all its work): measured as stated, accepted.

## 8. Texts for the landing

`pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `landing.txt`, `FOR-RECORDS.md` in this folder.
Each text exported through the workflow's own `neutral_export` (cut by program from `ci.yml` lines 120 to 128) as the
commit message of a scratch repository and scanned with `--no-banner --redact --ignore-gitleaks-allow --exit-code 1`:
title, title and body, body, the squash message with a number, the squash body, `landing.txt`, the squash subject: export
rc 0, message stored whole, scan rc 0, `no leaks found`, 7 of 7; control (the squash message plus a planted token built
from parts) rc 1, `leaks found: 2`. `words.py` over the title, squash subject, squash body without its attribution line
and the body without its footer: `WORDS: clean (4 files)`; the squash body whole: `WORDS: clean (1 files)`. All ASCII
except the body's footer line. Nothing in them says the product owner decided anything about the broker.

## NOT RUN / NOT TESTED

The Windows leg of any probe (the hosted Windows leg ran the lane's 53 only). C# CodeQL (cannot extract on arm64). Two
records of one device at restore. Real Microsoft tokens or the real refresher (none exist in this lane). A second process
over one partition. The reader did not rerun `repo_rules.py --source-documents` (main's R5 question is lane C's). A final
whole-solution run after the mutants (the source was proved equal to the head instead). Race interleavings by held
fakes beyond the 1,000-caller rows: the second reader's scope.
