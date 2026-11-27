Three owed items of the Universal Print registration library, built and tested inside the test process only: every
cell runs against the fake issuer, the test clock and the tests' own store under the system temporary folder. One
commit, `b3248f8c`, on `main` `0ca8c655` (behind 0, ahead 1). Four files, all changed, none added:
`CloudDeviceTokenHolder.cs` and the registration README under `src/Datasec.Suite.UniversalPrint/Registration/`, and two
test files (`CloudDeviceTokenHolderTests.cs`, `RegistrationKeysTests.cs`). No package, no lock file, no project file,
no `Datasec.Suite.slnx` line, no workflow, no file under `contracts/` or `build/`.

## Why

- The holder checks an answer for disposal twice: when it arrives and again under the registration's lock just before
  it would be held. No test reached the second check: the limit cells' disposed-first forms dispose the object before
  the answer arrives, so the first check refuses it, and a change that removed the second check left every test green.
- The README said every failure after construction is a `RegistrationException`; a failure of the platform while
  `CreateRegistration()` makes the key, exports it or signs the request leaves as the platform's own exception.
- Five platform behaviours measured on macOS arm64, and two catches of the certificate checks that no cell reaches on
  macOS, were not named in the README.

## What changed

- **The seam.** `internal Action<CloudDeviceToken>? AfterArrivalCheck { get; set; }` on the holder, invoked with the
  answer after the arrival check and before the lock is taken (`CloudDeviceTokenHolder.cs:52`, `:303`). Null outside
  the tests. The check under the lock (`:325`) is unchanged.
- **Cell T15.** Two shapes: an answer disposed in the seam, and the held object answered again and invalidated in the
  seam. Each is `TokenAnswerRefused`, nothing is held, and the next call asks the issuer again.
- **Cell K07.** A key factory that throws `CryptographicException` and one that throws `InvalidOperationException`:
  each leaves as that type and the store lists no name; the control first, a good registration puts one name.
- **The README.** The exception to its first rule; Limits bullets for a configured issuer disposed after construction,
  the one-element chain rule's reach, a leaf's extensions, a record put back to its first form, two instances each
  accepting an attach, a platform failure inside `CreateRegistration()`, and the two catches no cell reaches on macOS;
  the last Limits bullet says which check the limit cells' disposed-first forms reach and that T15 reaches the other.
- **Test summaries.** `Cells T01 to T15` and `Cells K01 to K07`; no other landed test line changes.

## What proves it

- The Universal Print tests `351 / 0` (two more than `main`'s 349); the whole solution `total: 2431`, `failed: 0`,
  `succeeded: 2427`, `skipped: 4`; the branch's push run: linux `succeeded: 2427`, windows `succeeded: 2410`, rules 679
  files, `Ran 117 tests`, secret scan clean.
- Two mutants, each turning exactly its cell red and nothing else: the check under the lock kept only for a removed
  entry (T15: "expected TokenAnswerRefused, nothing was thrown"), and the key failure turned into a typed refusal (K07:
  `RegistrationException` where `CryptographicException` is expected).
- Probes run beside the change, not committed: T15's second shape alone is red under the first mutant; the export and
  the signing call failing leave as `CryptographicException` with nothing put; a change that makes either named catch
  throw leaves every cell green on macOS, while the same change to the certificate loader's catch turns two cells red.

## Still open

- Nothing here has run against a device.
- The README's limits are measured on macOS arm64 only; Linux and Windows are unmeasured by those sentences' own words.
  The catch around the first reads of the public key and the validity dates is reached by one cell on the hosted Linux
  leg only; which exception other than a cryptographic one the chain's build can throw is unmeasured.
- A seam that throws leaves its issuer call unfinished: the callers for that id wait until the holder is disposed, and
  the answer it was handed is not cleared. Tests only (the seam is null outside them); no cell sets a throwing seam.
- The seam is visible to the one test assembly named in the project file; no assembly of the repository is
  strong-named, as for every other internal member.
- Owed: the Server tests' time bound per cell; the other device-facing handlers' chain policy; the heavy-job runner's
  bound (outside the repository).
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (this part of the lane first; the seam,
summary and README edits frozen and the two cells written to their table; a seam in the product rather than reflection
on the private lock; the key failure as a README exception pinned by a cell, with no code change; the two catches and
the five platform behaviours as named limits; no local CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent to any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
