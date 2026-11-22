GATE B1924: GO WITH FINDINGS @ d383d21 on main 7b0f4f5

Gate G1 (certificate trust, key material, the token holder), round 1, the one reader. OXPd 2, kit B1915 with ANSWER-1
(seat X29, lane U): owed items 52, 53, 54, 55(1) and the C14 Windows gap. Head
`d383d21cbd4b8a2d709e71e6cd5aa86fc49e6f7e` on `b1915/up-registration-fix-round` (two commits: `759c9060`, parent
`4e8828ee`; `d383d21c`, parent `759c9060`). Read and measured 2026-11-22 22:09 to about 22:30 AEDT, on Opus 5.5, in my
own clones `fleet/state/s311/g1924/clone` (detached at the head) and `clone2` (the merge tree), both by the kit's
`clone.py ... draft` (push URL `invalid://no-push`, no identity). Origin by `gh api -X GET` under the project
GH_CONFIG_DIR: branch = d383d21c (one `b1915` ref); main was 4a0a9717 at 22:10 and **7b0f4f55 at 22:19** (pull request 20,
lane T, landed at 22:14 per the coordinator's note, re-read by GET: one parent 4a0a9717, tree c2b3e0d9, two test files
outside every Registration path); open pull requests 0. `compare main...d383d21c` ahead 2, behind 2, merge base
4e8828ee, exactly the eight owned paths. No write to the project, GitHub or Jira; no push, no pull request; no `cd`;
nothing deleted (my probe file and scanner controls moved to `g1924/_quarantine/`).

**BLUF.** The change does what it says, and every product edit only adds a refusal or a wait: nothing main refused is
now accepted (section NOTHING NEWLY ACCEPTED). Measured on macOS arm64: the head 1587 / 0 failed; the merge with main
7b0f4f55 1589 / 0 failed; the 14 mutants exactly as ANSWER-1 §4.4; my own probes, one or more per rule, hold the
rules (a delete racing two attaches leaves no record in 40 of 40; a block-then-throw issuer and a null-task issuer are
`TokenUnavailable` and the next call asks again; 255- and 257-byte signatures refused while the 256-byte original with
a leading zero is accepted; an ECDSA issuer accepted as the named limit says; an intermediate expired by the library's
clock refused). Hosted push run 45015283855 PASS at 1587; main's 45016304308 PASS at 1581. One Minor finding,
**unchanged from main and outside this diff**: an issuer that answers a renewal with the very token object the holder
holds makes the holder hand out a zero-byte token with no error (G04b). It is next to D3 but not made by it. The rest
are Info. Nothing blocks the landing.

## FOUND

1. **Minor (left from main, not made here): the same token object answered again at a renewal is disposed by the
   holder and then held.** Probe G04b: an issuer that returns one `CloudDeviceToken` instance on every call; the first
   `GetAsync` holds it; at 91 s of a 100 s lifetime (renew at 0.9) the renewal answers the same object; it passes the
   answer check (not yet disposed), then `Finish` runs `entry.Held?.Dispose()` on that very object and sets
   `entry.Held = answer`. MEASURED: the caller gets `token of 27 bytes, all zero True, equal to the issued bytes False`,
   two calls, the shared object disposed. `Finish` is byte for byte main's (the diff touches only `RunFlightAsync`), so
   main does the same (DERIVED). After an `Invalidate` the same shape IS refused by the new check (G04:
   `TokenAnswerRefused`, because `Invalidate` disposed the held object first). Related, DERIVED, not probed: an issuer
   that disposes its answer after returning it also leaves a zero-byte held token (the check reads `IsDisposed` once).
   Fix sketch for the backlog: refuse, or skip the dispose, when `ReferenceEquals(answer, entry.Held)`, or copy the
   answer's bytes into a holder-owned token. Not blocking: the real issuer (an HTTP call, item 53) is not wired and the
   README says the host does not use this library yet. Named in pr-body "Still open" and FOR-RECORDS 1.
2. **Info: the window and modulus clauses judge the one chain the platform built.** Element 1 is always the leaf's
   direct signer (the chain verified that signature with its key), so the modulus clause reads the right key in a
   chain of two or three (G07: root + intermediate configured, ACCEPTED at T0; the intermediate expired by the
   library's clock, `IssuerNotTrusted`). Two configured issuers of one name and key, one expired by the library's
   clock (a renewed CA certificate): ACCEPTED on macOS in both list orders (G08). Linux and Windows UNMEASURED: a
   platform that built through the expired one would be refused (fail closed, never an acceptance). If the platform
   already refused, rule 8 returned false before the clause, with the same reason; the clause never reads the real
   clock. An issuer whose NotBefore is after the leaf's (not time-nested), inside both windows: ACCEPTED (G08), as
   main.
3. **Info: the window clause and `mModulusNoLength` are held off macOS only.** `mWindowRuleOff`, `mWindowNotAfterOff`,
   `mWindowNotAfterExclusive` and `mModulusNoLength` read GREEN here (the platform refuses those shapes itself). The
   clause's red is C14 on the hosted Windows leg at 759c9060 (re-read at source, job 137174350517: `C14 an issuer
   expired by the library's clock: expected IssuerNotTrusted, nothing was thrown`, `total: 1586`), green on Windows at
   d383d21c. The same standing as `mFixUndone`. Accepted, as ANSWER-1 §3 states.
4. **Info: the exact-length rule (Q1's cost) measured.** G05 found a signature with a leading zero byte after 53
   issues, then attached its 255-byte form (zero stripped, the same value): `IssuerNotTrusted`, v1; its 257-byte form
   (a zero prepended): `IssuerNotTrusted`, v1; the 256-byte original: ACCEPTED, v2 (so the byte comparison handles a
   leading zero). A signer that strips leading zeros (not PKCS#1) would see about one certificate in 256 refused; the
   real issuer's output is UNMEASURED (named in pr-body "Still open").
5. **Info: H36 measured.** An issuer whose `IssueAsync` returns a null task: `TokenUnavailable`, and the next call asks
   again, two calls (G03). The seat's DERIVED reading holds: `Task.Run` gives a cancelled proxy, caught by the existing
   `catch (Exception)`, and `DisposeLate` now sees a non-null task. On main the same shape hangs its callers (the
   seat's reading of BASE, DERIVED; not re-run here).
6. **Each rule's other inputs, read whole and probed.** D1: `lock (_attachSync)` is the attach's own monitor; no other
   lock is taken inside it and the store does not call back, so no new deadlock (DERIVED); G01 (two attaches and a
   delete released together, 40 rounds): records left 0 of 40, outcomes `NotFound/NotFound + delete True` 38,
   `attached/NotFound` 1, `attached/CertificateAlreadyAttached` 1, every delete True. D2: G02 (an issuer that sleeps
   300 ms on the calling thread, then throws): `GetAsync` returned its task after 0 ms; `TokenUnavailable`; the next
   call got the second token. `flight.Cancel` is never disposed, so a late `Task.Run` start cannot see a disposed
   source (DERIVED). D3: `IsDisposed` is `internal` and reads the `volatile` field. D4: an ECDSA issuer: ACCEPTED, v2
   (G06), the named limit. Window: inclusive at both ends, converted as rule 7 converts.
7. **Seat's claims re-measured, all held:** the 13 tool hashes (kit 10 and ANSWER-1 3); both stored commit messages
   equal `commit-message.txt` and `commit-message-2.txt` (`cmp` rc 0); numstat against 4e8828ee 3/0, 4/11, 22/11,
   67/10, 150/1, 68/1, 140/1, 65/1 (= ANSWER-1 §5); 500 files; the mutant lines; the hosted numbers.

## NOTHING NEWLY ACCEPTED (does any path accept what main refused? No; DERIVED from the diff, each with a probe)

- Delete: adds a wait, no outcome change (G01).
- Issuer call: a synchronous throw was `TokenUnavailable` on main and still is (G02, T05). A null task hung on main and
  is now `TokenUnavailable` (G03). An issuer that blocks and then answers inside the bound is still accepted; past the
  bound it is now `TokenTimedOut` (T11): stricter.
- Answer check: one more `||` refusal (T12, G04).
- Rule 8: one more `return false` (the window loop) and one more `&&` (the modulus clause); `Count >= 2` kept; no check
  removed or reordered ahead of the chain's own flags.

## TESTED (MEASURED, macOS arm64; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at a
time; lock folders moved to `g1924/_quarantine/locks/`; waits only on load or on other holders, never broken)

- Head: `CI=true dotnet restore --locked-mode --force` rc 0, 24 `Restored`, porcelain 0 lines; build `0 Warning(s)`
  `0 Error(s)`; whole solution `total: 1587`, `failed: 0`, `succeeded: 1583`, `skipped: 4`, `failed Datasec.` 0.
- Mutants, `mutants_a1.py` unchanged (sha256 a4f21ef6...), rc 0, all 14 `Total: 346, Errors: 0`: RED on its named cell
  only (`Failed: 1`): mNoZeroPkcs8 K06, mReadCertLoose R05, mTimeIgnored C16, mVerifySystemClock C16, mDeleteUnlocked
  X02, mIssuerOnCallerPath T11, mDisposedAnswerHeld T12, mModulusOff C15; GREEN: mCatchNarrow, mFixUndone,
  mModulusNoLength, mWindowRuleOff, mWindowNotAfterOff, mWindowNotAfterExclusive; every `undo cmp 0`; porcelain 0 after.
- Probes: a scratch class `G1924Probes` (9 facts, each reports by `Assert.Fail("PROBE ...")`; source
  `g1924/scratch/G1924Probes.cs`, in no patch), built 0/0 and run by `-class` (Total 9, every one reporting); outcomes
  in FOUND 1, 2, 4, 5 and 6; logs `g1924/logs/g-probes2.log`, `g-probes3.log`. The file was then moved to
  `_quarantine/probe-file/`; `git diff --quiet d383d21c` rc 0, porcelain 0, rebuilt rc 0.
- Merge: `git merge-tree --write-tree 7b0f4f55 d383d21c` rc 0, tree `796bb0bcd0c6e50d6b8d87c1e83d22809b9e81cd`, 500
  files; differs from 7b0f4f55 in exactly the eight owned paths and from d383d21c in exactly the five files main
  gained. That tree checked out in `clone2` (`git diff --quiet 796bb0bc` rc 0 before and after the restore): locked
  restore rc 0; build 0/0; whole solution `total: 1589`, `failed: 0`, `succeeded: 1585`, `skipped: 4`, `failed
  Datasec.` 0. Expected hosted on the merge ref: 1581 + 8 = 1589 both legs, succeeded 1585 / 1570, skipped 4 / 19.
  (Against 4a0a9717: tree 6dd80924..., rc 0, superseded.)
- HOSTED head: `hosted2.py d383d21c... --total 1587 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111
  --floor 111 --hardened-scan` rc 0: run 45015283855, attempt 1, four jobs success, `check runs beside the four: 0`;
  linux 1587 x2, windows 1587 x2; `failed Datasec.` (`grep -i`, anywhere in the line) 0 and 0, control `total: 1587` 2
  and 2; last line `HOSTED d383d21cbd4b8a2d709e71e6cd5aa86fc49e6f7e: PASS`.
- HOSTED main: `hosted2.py 7b0f4f55... --total 1581 ...` rc 0: run 45016304308, four jobs success, Analyze actions,
  csharp, python beside them; `HOSTED 7b0f4f55d835f669a0539ce65d80e5625bd9c1dc: PASS`. Open code-scanning alerts on
  main 0.
- WORDS: `--control` `CONTROL FIRED: 13 of 13`; over the 519 added lines (4e8828ee..d383d21c) and both stored commit
  messages: `WORDS: clean (3 files)`.
- GITLEAKS 8.30.1: control FIRST (a token shape built by program from two halves, never printed): rc 1, `leaks found:
  1`, moved to `_quarantine/gl-control`; then the added lines and both messages as neutral `<n>.txt`: rc 0, `no leaks
  found`.

## CODEQL (read on the pull request; landing step 3)

No CodeQL locally. A reader of the Analyze (csharp) rows checks a `/language:csharp` row AT d383d21c with results_count
0 and open alerts 0, and, if any alert appears, reads it against the shapes this diff adds on purpose: two generic
`catch (Exception)` blocks that return false (`InsideWindow`, `SignatureBelowIssuerModulus`: each can only refuse);
the discarded `ReadEncodedValue()` results and `ReadBitString(out _)`; the null-forgiving `Modulus!` (inside the
try); `Task.Run` inside a flight started fire-and-forget (`_ = RunFlightAsync`, as on main); `lock (_attachSync)`
around a store call; in tests, a `Thread` writing a captured local (X02) and a blocking `Wait` inside an issuer script
(T11). An alert is fixed by a new commit and a new gate, never dismissed.

## NOT TESTED

- Nothing on Linux or Windows locally (the hosted legs are those runs). G08's renewed-issuer pair and the not-nested
  issuer on Linux and Windows: UNMEASURED.
- No publish or release guard locally (the hosted legs ran both: GUARD clean 10 and 11 files). No `run_step.py`
  neutral scan locally (the hosted secret-scan ran it on this head: every hardened row OK). No `repo_rules.py` locally
  (hosted rules job: `RULES: clean (500 files)`).
- The red-first state (`1-red-first.patch` alone) not re-applied here: the seat's and drafter's runs, the hosted
  Windows red at 759c9060 re-read at source, and the mutants on the head (each fix undone turns its cell red) carry it.
- No loops of 100 on the new cells (the seat's and drafter's loops stand; every whole-solution and mutant run here was
  green on every unmutated cell).
- Probe G04b's issuer-disposes-after-return variant (DERIVED only). G04b itself on main (DERIVED: `Finish` unchanged;
  main's token has no `IsDisposed` for the probe to read).

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 239 bytes (under 256; not the commit subjects, which are 303 and 258 bytes). `squash-subject.txt` 248
  bytes, the title plus ` (#PRNUM)`. `squash-body.txt`: what and why in three paragraphs, ending
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. `pr-body.md`: why (owed items 52 to 55(1) and the Windows
  gap), what changed, what proves it, still open (platform-only reds, RSA-only, exact length, the same-object renewal
  left from main, the pool thread), who decides: the coordinator, as coordinator; no line says the product owner
  decided anything; ends with the Claude Code line. `landing.txt` in B1923's form with this pull request's numbers:
  main 7b0f4f55, merge tree 796bb0bc, merge-ref totals 1589 both legs, succeeded 1585 / 1570, skipped 4 / 19, RULES
  500, Ran 111, floor 111; step 6 main's push run PASS at 1589; MAIN MOVES for lanes A1, S, D, E (T already landed),
  with lane S's store members a STOP.
- Scans of these texts: see the lines below this section (SCANS).

## SCANS (of the landing texts, after the last edit)

- `words.py` per file: `pr-title.txt`, `squash-subject.txt`, `squash-body.txt` every class 0 (`WORDS: clean (3 files)`).
  `pr-body.md`: `coordinator` 2 (the required "who decides" line) and 4 non-ASCII bytes (`f0 9f a4 96`, the required
  robot line), every other class 0. Its one B-number hit (the branch name) was removed, then scanned again: 0.
- gitleaks 8.30.1: a fresh firing control (rc 1, moved to `_quarantine/gl-control2`, then `gl-control3`), then the
  seven texts of this folder as neutral `<n>.txt`: rc 0, `no leaks found` (run before and again after the last edits).
- `build/squash_scan.py` (main's, from `clone2`) with `#PRNUM` replaced by `#21` and `squash-body.txt`: control
  `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks (1589 on both legs) and CodeQL read as its
step 3 requires. The Minor finding (FOUND 1, left from main) goes to the backlog; it is not a condition of this
landing.
