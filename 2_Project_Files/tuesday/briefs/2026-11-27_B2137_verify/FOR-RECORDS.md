# FOR RECORDS: gate B2137 (G1, round 1 of 2 of lane OX-C kit 1), head 641935b5 on main 38a031e5

For the records pass after the squash lands (none of this is true on main before it). Written by the gate reader; no
project file was written by the gate.

## The kit's FOR RECORDS (RELAYED from kit B2134, checked by this gate)

- Owed item 131 closed by its first option: the Graph walk keeps and compares each address without its fragment
  (`GetLeftPart(UriPartial.Query)`, one helper for both sites), so a next link that differs from an address already
  requested only by its fragment ends the walk as `PagingLoop`; the address requested is unchanged; a `%23` in a path or
  query is not a fragment. **Gate check:** MEASURED (red first 3 rows, 7 mutants, a 34-pair key table and 6 walk
  shapes: the only change of judgment is the fragment-only class; HTTP/1.1 sends no fragment, MEASURED on macOS arm64).
- Owed item 122 closed by its first option, the coordinator's choice: the line
  `CertificateRevocationCheckMode = X509RevocationMode.NoCheck` is dropped (it set the property's own default and is not
  read beside the chain policy); DA18 is unchanged and two mutants show it pins both the mode and the policy's
  `RevocationMode`. CodeQL at the base read no alert on that line. **Gate check:** the default `NoCheck` MEASURED on
  macOS arm64; DA18 green on the hosted linux and windows legs of the head.
- Owed item 119 closed: the Server README says that a hash the host holds in memory (issued through its
  `CallbackCredentials`, or read from the vault once) is checked without the vault until the process ends, and that only
  a serial within the rule whose hash it does not hold is `503` when the vault throws; a new cell pins every shape, with
  a test switch that makes the tests' store throw. **Gate check:** true on every single-process path measured; see
  PROPOSED 1 for another process.
- Owed item 120 closed: the transport's cancellation sentence and the doc comment of `ConnectFailed` say "measured on
  macOS arm64; other platforms UNMEASURED" (the platform of the review of pull request 35 and of its session's own test
  log). **Gate check:** supported (VERDICT.md section 2 c; arm64 is DERIVED for the probe run itself, whose own log
  prints no architecture).
- Owed item 77 closed: the Identity README cites `CsaStore.cs:294` in `PrefixOf` and `:311` in `BlobOf`; its other six
  citations were checked true at the head. **Gate check:** check 9 re-run, 8 of 8 (control BASE 6 of 8).
- Owed item 84 stays open: its part (2), a host-side filter for the framework's Debug line on a malformed header, is the
  logging work's; nothing of it was built.
- A candidate for the records (H9): a credential re-issued for a serial by another process is refused by a running host
  that holds the older hash, until it restarts (the host keeps a hash until the process ends). **Gate:** MEASURED, and
  its other half too (PROPOSED 1).
- Nothing here ran against a device.

## Which owed items close when the squash lands

119, 120, 77, 131, 122 (each by the line above).

## What stays owed

- 84 part (2) (the logging work); 121 (the other device-facing handlers: `HttpIppTransport.cs:43` keeps the same mode
  line with no chain policy, read there); 54, 75, 55, 138 (the later OX-C kit).
- 137 (the Server tests' hang on macOS arm64): seen AGAIN once by the build seat of this lane (its first whole-solution
  run at the head, 1800 s, the same fingerprint: main thread in a managed `Monitor.Wait`, `Kestrel Timer`, `Console
  logger queue processing thread` and `.NET File Watcher` threads, no inet socket; evidence in
  `<project>/.tools/b2134/logs/green-whole.log` and `orphan-server-tests-sample.txt`), with the BASE control green and
  three later head runs green (the seat), and two more head runs green and the Server executable alone green six times
  in this gate. Not this lane's (VERDICT.md FOUND 2). Add this sighting to 137's Symptom line (now seen twice).
- 138 (the runner leaves an orphan test host at its time bound): this gate saw a second orphan on the machine, not of
  this lane, `/private/tmp/b1839-gate/clone/tests/Datasec.Suite.Sessions.Tests/...` (pid 2177, parent 1, started
  2026-11-21 17:15, 14 threads, no inet socket), still alive at 09:15 on 2026-11-27; never touched by this gate. Its
  owner is the gate of B1839; whether it is a hang or only an orphan is UNMEASURED.

## PROPOSED owed items (this gate's findings; file only if the coordinator agrees)

1. **Server: a hash held until the process ends means a credential re-issued, or a device forgotten, by ANOTHER process
   over the same vault is not seen by a running host** (VERDICT.md FOUND 1, Minor). MEASURED (macOS arm64, gate probe
   S1, S2): the host holds `SYNTH0101`'s hash from an issue; a second `CallbackCredentials` over the host's vault
   re-issues it; with the store answering, the older credential gets `200` and the new one `401`. The host holds
   `SYNTH0102`'s hash; a second instance's `Forget` deletes the vault record (names 1 to 0); the old credential still
   gets `200`. The Server README's "the issued one passes" and "until the process ends" read as true only for one
   process; its Limits do not name the multi-process case. Reach: a deployment where a credential is issued or revoked by
   another process (no route of this host issues or forgets one today: `.Issue(` and `.Forget(` on 0 lines of `src/`
   outside the adapter README). Fix (a later round): a README Limits clause, and the design question of how a running
   host learns of a re-issue or a revocation (a time bound on the held hash, a re-read on a mismatch, or one issuing
   process). Pre-existing behaviour of `CallbackCredentials` (unchanged by this lane).
2. **Tools: `mutants_c1.py run` leaves each suite's test bin built from its LAST mutant** (VERDICT.md FOUND 7, Info).
   The tool undoes the source, not the build; a `dotnet test --no-build` after it runs the mutant assemblies. MEASURED
   by this gate's own slip: a whole run after the mutants read `failed: 2`, exactly the last mutant of each suite
   (`mLoopKeyOriginal`'s row 6 and `mPolicyOnline`'s DA18); after a build, `total: 2429`, `failed: 0`. The kit's Step 4
   asks for that build and the seat did it (`post-mutants-build`); the tool's header could say so. Records note, no code.

## Notes for the records (no item)

- `mLoopKeyAdd` row 2 turned red by the `PagingLoop` assertion, not the sends assertion the kit's text named;
  `mLoopKeyCompare` row 2 (UNMEASURED in the kit) turned red: `AbsoluteUri` keeps an empty `#` (MEASURED directly by this
  gate's key table: `items?page=2#`).
- The kit's H4 named limit is now MEASURED on macOS arm64: an explicit `:443`, `%41`, the host's and scheme's letter
  case, dot segments, a backslash, the hex case of an escape and a lone `%` are written the same by `AbsoluteUri` and
  `GetLeftPart`; an empty `?` is kept (`items?` and `items` are two keys); parameter order and a trailing slash are two
  keys.
