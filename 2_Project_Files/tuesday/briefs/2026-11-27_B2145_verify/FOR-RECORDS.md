# FOR RECORDS: gate B2145 (G1, round 1 of 2 of lane OX-C kit 2), head b3248f8c on main 0ca8c655

For the records pass after the squash lands (none of this is true on main before it). Written by the gate reader; no
project file was written by the gate.

## The kit's FOR RECORDS (RELAYED from kit B2138, checked by this gate)

- Owed item 75 closed: an internal test seam on the holder (called with an answer between the check made on its
  arrival and the check under the registration's lock; null outside the tests) and cell T15, which reaches the check
  under the lock in two shapes (an answer disposed there; the held object answered again and invalidated there); a
  mutant that keeps that check only for a removed entry turns T15 red. The README's Limits sentence now says the landed
  disposed-first forms reach the arrival check. **Gate check:** MEASURED; the mutant re-run (T15 red only); shape 2
  red on its own under the same mutant (probe G1); a third shape held by the same check (probe G3, a renewal with a
  live held token) red under it too (VERDICT.md FOUND 2).
- Owed item 55 parts (2) to (6) closed as named limits in the registration README, each "measured on macOS arm64"; part
  (7) closed by the README's exception to its first rule and a Limits bullet, pinned by cell K07 (a key the platform
  cannot make leaves as the platform's exception; nothing is put); a mutant that types the failure turns K07 red.
  **Gate check:** each sentence against owed 55's measured words (part (4)'s "for the same registration" against the PR
  17 reader's probe G10: one request id, 20 of 20); part (7) also MEASURED for the export and the signing call (probes
  G8, G9; VERDICT.md FOUND 4); one wording note (FOUND 5).
- Owed item 54 closed as a named limit: the two catches no cell reaches on macOS (around the chain's build, and around
  the first reads of the public key and the validity dates; the latter reached by C01 on Linux only), each of which can
  only refuse. **Gate check:** "reached by no cell on macOS" MEASURED for both (a probe mutant turning each catch into
  a throw: 0 reds of 358; control, the loader's catch: C01 and C02 red); the two catches are the fix commit 94fe606's
  (`RegistrationKeys.cs:214`, `RegistrationRecord.cs:164` at the head), not the stamp's 249 and 276 (VERDICT.md
  FOUND 3). C01 on Linux stays RELAYED.
- Owed items 137 and 121 stay open for part 2 of this lane's kit 2; owed item 138 stays open for a tooling change of the
  runner outside the repository.
- Nothing here ran against a device.

## Which owed items close when the squash lands

75; 55 parts (2) to (7) (part (1) was closed by pull request 22 for RSA issuers, its non-RSA limit already named on
main; whether 55 is then ticked whole is the records pass's call, the kit's NOT DECIDED 2); 54 (the rest after pull request
22: `mCatchNarrow` and `mFixUndone` stay named survivors on macOS, now named in the README).

## What stays owed

- 137 (the Server tests' hang; part 2 of this lane's kit 2): not met in this gate's whole run (`Datasec.Suite.Server.Tests`
  passed in 20 s).
- 121 (the other device-facing handlers' chain policy; part 2).
- 138 (the runner leaves an orphan test host at its bound; a tooling commission outside the repository): the B1839
  gate's orphan (`/private/tmp/b1839-gate/clone/.../Datasec.Suite.Sessions.Tests`, pid 2177, parent 1) is still alive at
  11:45 on 2026-11-27, six days after it started; never touched by this gate.
- 76's README note on the lock of the old call's clean-up (not this lane's), unchanged.

## PROPOSED owed items (this gate's findings; file only if the coordinator agrees)

1. **Universal Print registration tests: a seam that throws leaves the issuer call unfinished** (VERDICT.md FOUND 1,
   Minor). MEASURED (macOS arm64, gate probe G2): with `AfterArrivalCheck` throwing, `GetAsync` does not finish (2 s), a
   second call for the id joins the same unfinished call (1 s), the answer handed to the seam is never disposed, and
   only `Dispose()` (or `Remove`) of the holder ends the callers (`ObjectDisposedException`). Cause: the flight is
   started fire-and-forget and the throw leaves it before `Finish`, so its completion source is never set
   (`CloudDeviceTokenHolder.cs:111`, `:303`, `:304`, `:114`). Reach: tests only; no landed cell sets a throwing seam.
   Risk: a later cell whose seam throws (an assertion inside it) and that awaits `GetAsync` outside the 10-second
   `Expect.Within` guard, or without disposing the holder, would hang its test executable. Fix (a later round): a
   sentence in the seam's summary, or the invoke inside `try`/`finally` so that `Finish` is always reached.

## Notes for the records (no item)

- E1's "One exception to the first rule": the README also numbers its attach checks 1 to 8 ("the first rule that
  fails"), so "the first rule" can be read as rule 1; and "One exception" claims uniqueness that no reader proved (the
  chain's set-up and status reads, and the record builder inside `Write`, run outside any catch; UNMEASURED whether any
  can throw). For the next touch of that bullet: "One exception to that rule" (VERDICT.md FOUND 5).
- The kit derived the Universal Print BASE total as 329 from `[Fact` plus `[InlineData` counts; the measured 349 includes
  four `[MemberData]` theories in `IppReaderTests.cs` (seat D-1). A later kit's derivation counts `MemberData` rows.
- The seam is visible to any assembly named `Datasec.Suite.UniversalPrint.Tests`: no assembly of the repository is
  strong-named (FOUND 7); the same reach as every internal seam of the repository.
- The kit's H7 (export and signing failures, a named limit without a cell) is now MEASURED by probes G8 and G9
  (not committed); no cell is owed for it.

## SCANS of this folder

- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#58`, `squash-body.txt` and
  `pr-title.txt`: `WORDS: clean (3 files)`; `pr-body.md`: `product owner` 1 and `coordinator` 2 (the "Who decides"
  section) and the attribution line's emoji bytes, every other class 0 (the PR body is not committed); `B[12][0-9]{3}`,
  `X[78][0-9]`, `SEAT-` and card ids 0 in all four; `build/squash_scan.py` (the head's, equal to main's: `git diff
  --quiet 0ca8c655 HEAD -- build .github` rc 0) with `#58`: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN:
  clean`.
- **SCANS-3:** gitleaks 8.30.1 over this folder's seven files and the `#58` subject under neutral names `1.txt` to
  `8.txt`, the control re-planted first (rc 1, moved to `g2145/_quarantine/gl-control-2`): rc 0, `no leaks found`
  (11:58). FOR-RECORDS.md was scanned before this section was filled; this section adds no value of any kind.
