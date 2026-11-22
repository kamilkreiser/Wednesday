Two held test cells, owed items 47 and 48 of the backlog. One commit `bb495b4a` on `main` `4a0a9717`, two test
files only: `tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs` (+64 -0) and
`tests/Datasec.Suite.Contracts.Tests/TolerantReadingTests.cs` (+22 -0). No product code, no generator, no package,
project, lock, solution or workflow file changes.

## Why

Both items are test gaps over product code that is already right: each names a mutant of the product that no landed
test turns red.

- Owed item 47: the scan receiver maps a body whose read throws `ObjectDisposedException` to `JobNotFound` and any
  other body failure to `ScanRefused` (`src/Datasec.Suite.Jobs/ScanReceiver.cs`, the last throw of `ReceiveAsync`).
  Dropping the `ObjectDisposedException` arm (`mReasonDisposed`) left every landed cell green. The W02 body theory
  that pins it was written for the job service's third test-only round and held out of that round.
- Owed item 48: client models (the device answers) must stay strict: an optional root property sent as JSON null is
  refused as `WrongType`; only the service-target models read an optional null as absent. Dropping the
  `schema.Tolerant` condition from that rule (`mNullStrictToo`) left every landed cell green.

## What changed

- `ReceiverTests.cs`: the theory `W02_a_body_whose_read_throws_ends_the_receive_typed_and_the_job_is_wiped`, two
  rows. A multipart body gives its first part's header and 2000 bytes of a synthetic document, then every later read
  throws. `ObjectDisposedException` ends the receive `JobNotFound`, `IOException` ends it `ScanRefused`; in both the
  exception has no inner exception, the job is gone from memory and its folder is gone, and the spool's reserved bytes
  are 0. A private `ThrowingBody` stream serves the bytes and then throws. The text is the held diff byte for byte.
- `TolerantReadingTests.cs`: one more check inside `K8_the_device_clients_stay_strict` (no new test case). For every
  client model whose root schema has an optional property, the minimal valid body with the first such property set to
  null must parse to no value and a `WrongType` refusal at `$.<name>`. The walk counts the models it checked and
  asserts the count is above 0, so it cannot pass by finding none; it never pins the exact count, so a new client
  model does not turn it red.

## What proves it

- Red first, by mutant on the head: `mReasonDisposed` turns exactly the theory's `ObjectDisposedException` row red
  (`Expected: JobNotFound`, `Actual: ScanRefused`; Jobs 122 cases, 1 failed); `mNullStrictToo`, applied to the
  generated runtime and to its generator text alike, turns exactly K8 red (`did not refuse an optional null`;
  Contracts 148 cases, 1 failed).
- The same mutants with the base's two test files leave both assemblies green (Jobs 120, Contracts 148): the new
  cells, and nothing else, kill them.
- C# totals 1581 on both legs (1579 + the theory's two rows), skipped 4 on linux and 19 on windows, unchanged; RULES
  500 files; 111 unit tests, floor 111 (branch run 45014390651, four jobs success).

## Still open

- The K8 check sets one optional property per model (the first in schema order) and the root only; nested client
  schemas are held strict by K8's existing walk over every reachable schema's `Tolerant` flag.
- Whether device answers should be read tolerantly at all stays open (owed item 46). This check pins today's
  strict reading and would turn red, by design, if that question is ever answered yes.

## Who decides

The lane, both items in one test-only change, the K8 check's shape (every client model, a count above 0) and the W02
theory kept byte for byte are the coordinator's choices, made as coordinator.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
