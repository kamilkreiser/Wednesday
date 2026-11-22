GATE B1927: GO WITH FINDINGS @ 253d217 on main 83683af

Gate G1 (security surface and data destruction: the guarded member removes records), round 1, the one reader. OXPd 2,
kit B1920 (seat X32, lane S): owed items 42(2), 34 N3, N5, N7. Head `253d217b72cbd5c5b43fed63b0bbdd9285aa271b` on
`b1920/secret-store-removal-guard` (ONE commit, parent `7b0f4f55`). Read and measured 2026-11-22 22:33 to about 22:55
AEDT, on Opus 5.5, in my own clones `fleet/state/s311/g1927/clone` (detached at the head) and `clone2` (the red state on
`7b0f4f55`, then the merge tree), both by the kit's `clone.py ... draft` (push URL `invalid://no-push`, no identity).
Origin by `gh api -X GET` under the project GH_CONFIG_DIR: branch = 253d217b (one `b1920` ref); main was 0fc3344a at the
commission and **83683af4 at 22:38** (pull request 22, lane U, per the coordinator's note, re-read by GET: one parent
0fc3344a, tree 98d32f29; nine files since 7b0f4f55, none under the two Secrets folders); open pull requests 0.
`compare main...253d217b` ahead 1, behind 2, merge base 7b0f4f55, exactly the six owned paths. No write to the project,
GitHub or Jira; no push, no pull request; no `cd`; nothing deleted (my probe file, the red test files and the scanner
control moved to `g1927/_quarantine/`).

**BLUF.** The change does what it says. Every product edit only adds a refusal (`StorageFailed`) in front of an
existing operation; nothing main kept is now removed, and the only thing main removed that is now kept is a record
whose payload names an active key while the probe fails (section NOTHING NEWLY REMOVED). The rebased commit is the
reviewed content: the six files equal the frozen patches' after column by sha256, and the stored message equals
`commit-message.txt` (`cmp` rc 0). Measured on macOS arm64: `1-red-first.patch` alone on 7b0f4f55 gives U22, R18, R19
RED by their own assertions (94 / 3 failed); the head 1586 / 0 failed; the merge with main 83683af4 1594 / 0 failed;
the eight mutants and the survivor control exactly as the kit; the public surface equal on base, head and merge, its
plant control firing; my five probes hold every rule. Hosted push run 45017424523 PASS at 1586 (windows skipped 21);
main's 45018313743 PASS at 1589. One Minor finding, a residual window of the guard that the README does not name
(FOUND 1); the rest are Info. Nothing blocks the landing.

## FOUND

1. **Minor (a residual of the guard, owed, not blocking): the probe runs after the judgement, so a failure of the
   protection that ends between `Judge`'s `Open` and `ProbeRoundTrips` still removes a good record.**
   `DeleteUnreadable` calls `Judge` (which opens the record and fails), then `RemoveUnopened` probes; if the protection
   has recovered by then, the probe passes and `_records.Delete` runs on a record that would now open. DERIVED from
   `LocalSecretStore.cs:259-261` and `:495-503`; not measured (it needs a timed fault inside the data protection
   library). The README's D22 (a) limit names the older-key residual but not this window; pr-body "Still open" names
   it. Fix sketch for the backlog: after a passing probe, judge the record again under the lock and remove it only if
   it is still `DoesNotRead`. Not blocking: nothing calls `DeleteUnreadable` in the product (item 42 (1)), and the
   change is strictly safer than main, which removed in every such case.
2. **Info: the named residual (an older active key failing alone) is narrower than stated, DERIVED.** `FullCheck`
   (`:651-691`) refuses a start unless every non-revoked key makes an encryptor, and `CheckRingUnchanged` (run at the top
   of `DeleteUnreadable`) refuses `KeyNotAvailable` unless, elsewhere than Windows, the key source holds every active
   key's protecting key by id. So in-process the shape needs a failure after the start for that one key alone. Probe
   P1 measured the guard on an older active key: with the protection released, `StorageFailed` and the record file
   byte-equal; working, removed and the current key's record reads.
3. **Info: the partition folder under a running store is not watched (README: "at the start only"), measured.** Probe
   P4: partition folder moved aside and replaced by a link to it under a running store: `Put` returned 1 and wrote
   where the link points, `ListNames` listed 2; the record folder is a real folder behind the link, so
   `RefuseLinkedFolder` does not fire. At the next start the same link is refused `StorageFailed` (measured). A link
   swapped in between the look and the file operation is likewise not seen (README limit, not probed: needs a race).
   A `ListAll` during a swap: each record's `TryRead` repeats the folder check, so a swap seen mid-listing throws
   `StorageFailed` rather than listing records unreadable (DERIVED; not raced).
4. **Info: D2's one extra refusal and the removals that stay, measured.** Probe P2: good/b's bytes at good/a's path
   (the stated name does not hash to the id, payload under the current key), protection released: `StorageFailed`,
   file kept; working: removed, good/b reads. Probe P3, protection released: a foreign partition's record at this
   partition's path is removed (true, gone), and a file that is no record (no key id) is removed (true, gone): as main,
   as D1 states.
5. **Info: the folder check against other shapes, measured.** Probe P5: the record folder swapped for a DANGLING link:
   `ListNames` and `Put` `StorageFailed`, nothing made at the target, the folder put back reads. A direct
   `FileSecretRecordStore` over a link path, with and without a trailing separator: `ListIds` `StorageFailed` both
   (the separator does not blind the check on macOS; Linux UNMEASURED).
6. **Seat's claims re-measured, all held:** the eleven tool hashes; the six head files' sha256 equal THE CODE's after
   column and the six at 7b0f4f55 and at 0fc3344a equal its BASE column; numstat 14/0, 44/2, 16/5, 31/0, 35/0, 67/0;
   500 files; the mutant lines; the hosted numbers; the surface lines.

## NOTHING NEWLY REMOVED (does any path now remove what main kept, or keep what main removed? DERIVED from the diff, each
with a probe)

- `DeleteUnreadable`: one new `throw` before `_records.Delete`, only when the payload's key id is an active key AND the
  probe fails. It can only keep what main removed (U22, P1, P2); it never removes what main kept. Records under a
  foreign, unknown or revoked key and non-records are removed exactly as on main (U04, U13, U22's second half, P3).
- `ProbeRoundTrips`: protects and unprotects 32 random bytes under a purpose of four parts (a record's is five), writes
  nothing to disk (automatic key generation is off), zeroes both arrays, returns false on any exception.
- Start: one new `throw StorageFailed` before `OwnerOnly.CreateFolder(partitionFolder)`: a refusal before anything is
  made (R18, P4).
- `FileSecretRecordStore`: one new check at the top of each of the four members, before any file operation: a refusal
  only (R19, P5). No member's success path changes.
- No new field (U21 green), no new `SecretStoreError` member, no public or protected line (diff count 0, control 1).

## TESTED (MEASURED, macOS arm64; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at a
time; lock folders moved to `g1927/_quarantine/locks/`; waits only on load or on other holders, never broken)

- Tools: `cp -Rc` of the drafter's `gate/`, eleven sha256 equal to THE TOOLS; `words.py --control` `CONTROL FIRED: 13
  of 13`.
- RED FIRST: `clone2` at 7b0f4f55, `git apply 1-red-first.patch` rc 0 (three test files = the after column, product =
  BASE); locked restore rc 0; build 0/0; Secrets executable whole `Total: 94, Errors: 0, Failed: 3`, the three `[FAIL]`
  lines R19, R18, U22; messages `Assert.Throws() Failure: No exception was thrown` twice and `U22: a record under a key
  of the ring was removed while the protection failed`.
- SURFACE: the surface program built 0/0 outside both clones; on the base product (the red tree) `SURFACE: 160 lines,
  sha256 cd5625c8b890b6e31ee518054e28fc2470b4ae2a671a98639c1cbcd6e815218c`; on the head the same, `cmp` rc 0; on the
  merge tree the same, `cmp` rc 0; `ISecretStore` 4 member lines (`Put`, `TryGet`, `Delete`, `ListNames`). Control:
  `public const int SurfacePlant = 1;` planted after `MaxValueLength`: `161 lines, sha256 88feb4f6...de7b`, the one extra
  line `field System.Int32 SurfacePlant = 1 static`; undone by copy, `cmp` rc 0, rebuilt, surface `cmp` base rc 0. By
  diff: public/protected lines in `diff -U0 7b0f4f55 253d217b -- 'src/Datasec.Suite.Secrets/*.cs'` 0; control (one
  added `private` made `public` on the stream) 1.
- Head: `CI=true dotnet restore --locked-mode --force` rc 0, 24 lock files `cmp` rc 0, porcelain 0 lines; build 0/0;
  Secrets executable `Total: 94, Errors: 0, Failed: 0, Skipped: 4`; whole solution `total: 1586`, `failed: 0`,
  `succeeded: 1582`, `skipped: 4`, `failed Datasec.` 0.
- Mutants, `mutants.py` unchanged, rc 0, every `undo cmp 0`: mGuardOff, mGuardKeyInverted, mProbeAlways RED U22;
  mLiteralSketch `Failed: 3` RED U04 U13 U22; mPartitionLinkOff RED R18; mFolderCheckOff RED R19;
  mRevocationAloneTaken RED R17; mGuardFirstRecordOnly RED G03; each other `Total: 94, Errors: 0, Failed: 1`.
  Survivor control (7b0f4f55's three test files in place, `diff --numstat -- tests` 0 rows, 1178/394/143 lines): the
  five named mutants each `Total: 89, Errors: 0, Failed: 0`, `RED none: GREEN`; patched files back, `cmp` rc 0 each,
  porcelain 0.
- Probes: a scratch class `G1927Probes` (5 facts, each reports by `Assert.Fail("PROBE ...")`; source
  `g1927/scratch/G1927Probes.cs`, in no patch), built 0/0 and run by `-class` (Total 5, every one reporting); outcomes
  in FOUND 2 to 5; log `g1927/logs/probes.log`. The file was then moved to `_quarantine/probe-file/`; `git diff --quiet
  253d217b` rc 0, porcelain 0.
- Merge: `git merge-tree --write-tree 83683af4 253d217b` rc 0, tree `773a57983534d5308ced7a1b5af71654d1e0883b`, 500
  files; differs from 83683af4 in exactly the six owned paths and from 253d217b in exactly the nine files main gained.
  That tree in place in `clone2` (`git diff --quiet 773a5798` rc 0 before and after the restore): locked restore rc 0;
  build 0/0; whole solution `total: 1594`, `failed: 0`, `succeeded: 1590`, `skipped: 4`, `failed Datasec.` 0. Expected
  hosted on the merge ref: 1589 + 5 = 1594 both legs, succeeded 1590 / 1573, skipped 4 / 21.
- HOSTED head: `hosted2.py 253d217b... --total 1586 --rules 500 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan` rc 0: run 45017424523, attempt 1, four jobs success; linux 1586 x2, succeeded 1582,
  skipped 4; windows 1586 x2, succeeded 1565, skipped 21; `failed Datasec.` 0 and 0 (control `total: 1586` 2); last
  line `HOSTED 253d217b72cbd5c5b43fed63b0bbdd9285aa271b: PASS`. The five new cells green on linux; U22, R17, G03 green
  on windows (their first runs there).
- HOSTED main: `hosted2.py 83683af4... --total 1589 --skipped-windows 19 ...` rc 0: run 45018313743, four jobs success,
  Analyze actions, csharp, python success beside them; `HOSTED 83683af4be3fb39612153c103f922fc2febf7acc: PASS`.
- WORDS: over the 207 added lines (7b0f4f55..253d217b) and the stored commit message: `WORDS: clean (2 files)`.
- GITLEAKS 8.30.1: control FIRST (a token shape built by program from a prefix and random characters, never printed):
  rc 1, moved to `_quarantine/gl-control`; then the added lines and the message as neutral `<n>.txt`: rc 0, `no leaks
  found`.

## CODEQL (read on the pull request; landing step 3)

No CodeQL locally. A reader of the Analyze (csharp) rows checks a `/language:csharp` row AT 253d217b with results_count
0 and open alerts 0, and, if any alert appears, reads it against the shapes this diff adds on purpose: the generic
`catch (Exception)` in `ProbeRoundTrips` that returns false (it can only refuse a removal); the null-forgiving
`stored!` on the `DoesNotRead` arm (`Judge` sets it non-null on that path); in tests, `Directory.CreateSymbolicLink`
and the `IDisposable` cast that releases the protection services. An alert is fixed by a new commit and a new gate,
never dismissed.

## NOT TESTED

- Nothing on Linux or Windows locally (the hosted legs are those runs). R18 and R19 never run on Windows (designed
  skips, Stamp S4 Q6). DPAPI-NG: UNMEASURED.
- FOUND 1's window and the older-active-key residual: not produced (each needs a fault inside the data protection
  library). A link swapped between a look and a file operation, and a swap racing `ListAll`: not raced.
- No publish or release guard locally, no `run_step.py` neutral scan locally, no `repo_rules.py` locally: the hosted
  legs ran each on this head (GUARD clean 10 and 11 files, every hardened secret-scan row OK, `RULES: clean (500
  files)`).
- No loops of 100 on the new cells (every whole-solution and mutant run here was green on every unmutated cell).

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 230 bytes (under 256; not the commit subject, 286 bytes). `squash-subject.txt` 239 bytes, the title
  plus ` (#PRNUM)`. `squash-body.txt`: what and why in three paragraphs, ending `Co-Authored-By: Claude Opus 5.5
  <noreply@anthropic.com>`. `pr-body.md`: why (owed items 42(2), 34 N3, N5, N7), what changed, what proves it, still
  open (the older active key, FOUND 1's window, the by-path checks and the partition at the start only, DPAPI-NG), who
  decides: the coordinator, as coordinator; no line says the product owner decided anything; ends with the Claude Code
  line. `landing.txt` in B1924's form with this pull request's numbers: main 83683af4 (per the coordinator's note,
  re-read by GET), merge tree 773a5798, merge-ref totals 1594 both legs, succeeded 1590 / 1573, skipped 4 / 21, RULES
  500, Ran 111, floor 111; step 6 main's push run PASS at 1594; MAIN MOVES for lanes A1 and D (T, E and U already
  landed), with any change under the two Secrets folders a STOP. `FOR-RECORDS.md` for the records pass.
- Scans of these texts: see SCANS.

## SCANS (of the landing texts, after the last edit)

- `words.py` per file: `pr-title.txt`, `squash-subject.txt`, `squash-body.txt` every class 0 (`WORDS: clean (1 files)`
  each). `pr-body.md`: `coordinator` 2 (the required "who decides" line) and 4 non-ASCII bytes (the required robot
  line), every other class 0. The commit's own added lines and stored message: `WORDS: clean (2 files)`.
- gitleaks 8.30.1: a fresh firing control (rc 1, moved to `_quarantine/gl-control2`), then the seven texts of this
  folder as neutral `<n>.txt`: rc 0, `no leaks found` (run after the last edit of every text but this SCANS section).
- `build/squash_scan.py` (main 83683af4's, from `clone2`) with `#PRNUM` replaced by `#23` and `squash-body.txt`:
  control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.

Can it land? Yes, by `landing.txt`, once the pull request's merge-ref checks (1594 on both legs, windows skipped 21)
and CodeQL read as its step 3 requires. The Minor finding (FOUND 1) goes to the backlog; it is not a condition of this
landing.
