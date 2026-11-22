The Universal Print registration fix: owed items 52, 53, 54 and 55(1) of the backlog, and the issuer-window gap a
new cell measured on the hosted Windows leg. Two commits on this branch (`759c9060`, then `d383d21c`), merge
base `4e8828ee`. Eight existing files change, all under
`src/Datasec.Suite.UniversalPrint/Registration/` and `tests/Datasec.Suite.UniversalPrint.Tests/Registration/`. No
file is added, and no public member, `RegistrationError` member, package, project, lock, solution or workflow file
changes.

## Why

- Owed item 52: `DeleteRegistration` did not take the attach lock. A delete during an attach's write left the removed
  registration's record (key and certificate) back in the store.
- Owed item 53: the issuer was called on the first caller's thread, and the `IssueTimeout` bound started only on the
  task it returned. An issuer that blocked before returning held its callers past the bound.
- Owed item 54: six mutants of the library left every cell green, and an issuer that answered an already disposed
  token was held.
- Owed item 55(1): on macOS a certificate whose signature value was moved to s + n (n the issuer's modulus, the same
  length, the signed part untouched) was accepted and kept.
- The C14 cell for item 54 then showed that on the hosted Windows leg a configured issuer expired by the library's
  clock was not refused by the platform's chain.

## What changed

- `RegistrationKeys.DeleteRegistration` runs under the same `_attachSync` lock as `AttachCertificate`.
- `CloudDeviceTokenHolder` calls the issuer through `Task.Run`, so the bound starts at once. An issuer that throws, or
  returns a null task, gives a failed or cancelled task, reported as `TokenUnavailable`. The answer check also refuses
  a token that is already disposed (`TokenAnswerRefused`), through a new `internal bool IsDisposed` on
  `CloudDeviceToken`.
- Rule 8 (`ChainsToConfiguredIssuer`) adds two clauses after the chain builds, each refused as `IssuerNotTrusted`:
  - every chain element, the configured issuer included, lies inside its own `NotBefore` to `NotAfter` at the
    library's instant, both ends included, in UTC (`InsideWindow`);
  - the certificate's signature value has the length of the issuer's RSA modulus and lies below it
    (`SignatureBelowIssuerModulus`, the PKCS#1 range). An issuer without an RSA key is not checked by this clause.
- README: rule 8, the removal line, the bound, the answer check and the limits say what the code now does.
- Cells: K06, R05, X02, C14, C15, C16, T11 and T12, with two test-only helpers (`ExportWatchingRsa` and
  `PausingStore`). No existing cell, helper or assertion changes.

## What proves it

- Red first on macOS arm64 against `main` at `4e8828ee`: X02, T11, T12 and C15 fail by their own assertions. C14 failed
  on the hosted Windows leg of `759c9060` and is green on the Windows leg of `d383d21c`.
- Mutants on the head (UniversalPrint assembly, 346 cases): undoing the delete lock, the `Task.Run`, the disposed
  check or the modulus comparison turns X02, T11, T12 or C15 red. Removing the PKCS#8 clear or the record's
  certificate re-check turns K06 or R05 red. Verifying on the system clock, or ignoring the time, turns C16 red.
- Named survivors on macOS: the chain's catch narrowed, the field reads' catch rethrowing, the modulus clause without
  its length test, and the three edits of the window clause. On macOS the platform already refuses those shapes. The
  window clause is held by C14 on the hosted Windows leg.
- C# totals 1587 on both legs at the head (1579 + 8), skipped 4 on linux and 19 on windows, RULES 500 files, 111 unit
  tests with floor 111 (push run 45015283855, four jobs success). Merged with the current `main` the totals are 1589.

## Still open

- s + n and the window clause are measured red only where the platform accepted the shape (macOS for s + n, Windows
  for the issuer window). An issuer without an RSA key is not checked by the modulus clause.
- A signature that is not exactly the modulus's length is refused, as PKCS#1 requires. A real issuer's output is not
  yet measured.
- An issuer that answers a renewal with the very token object the holder already holds is disposed by the holder and
  then held, so callers get a token of zero bytes. This is unchanged from `main` and is left for a later change; the
  real issuer is not wired yet.
- A blocked issuer holds one thread-pool thread until it returns. Items 55(2) to 55(7), 56 and 57 are unchanged.

## Who decides

The coordinator chose, as coordinator, to make the four items and the Windows gap one change, and chose every choice
inside it: the lock, `Task.Run`, the reasons, the modulus rule over a named limit, the window clause and the named
survivors.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
