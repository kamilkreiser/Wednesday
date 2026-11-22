The sign-in state machine (component C5), work package WP1.4 in part: the card paths only. One commit on this
branch (`af26f801`, parent `7b0f4f55`). It adds a new library `src/Datasec.Suite.SignIn/` and its test project
`tests/Datasec.Suite.SignIn.Tests/` (30 files, two of them lock files written by the restore) and two lines of
`Datasec.Suite.slnx`. No package, workflow, existing project or existing lock file changes. The library references
`Datasec.Suite.Sessions` only.

## Why

- The plan's row for WP1.4 names a per-device actor, the known-card paths, the binding rule and the display name in
  the four forms. The design asks for one instance per printer that serialises its events through a channel.
- The design's binding rule: the token obtained for a known card must carry the object id of the card's user, or
  the sign-in is refused and audited.
- The printer's read event carries no time of reading, so a stale-tap guard can rest only on the time the event
  arrived at the server.

## What changed

- `SignInActor`, one per (device serial, platform). `TapAsync(cardId, arrivedAt)` and `DeviceSignedOutAsync()`
  queue an event on one unbounded channel read by one loop. Each tap ends in one of fourteen `TapOutcome` values.
- The card paths. The same card while its user is signed in signs out with no lookup. A card of the signed-in user
  (object ids equal as `Guid`) signs out. Another user's card signs the first out and then the second in. An unknown
  card signs the signed-in user out and is reported. There is no wait between a sign-out and the next sign-in.
- The binding rule. The `IdentityGrant`'s `TokenObjectId` and the card user's `ObjectId` must both parse as `Guid`
  and be equal (`BindingRefused` otherwise). The grant's `Subject` must equal the card user's `ObjectId` ordinally
  before the printer is told anything (`SessionRefused` otherwise). On a refusal the `Audit` event is raised once
  (outcome, serial, platform only), the printer is told and the grant is disposed.
- The stale-tap guard. An age from arrival to the tap's turn of at least `MaxTapAge` (5 s, a placeholder), or a
  stamp from the future, is `StaleTap` and calls nothing.
- Every identity and printer call runs off the loop under `WaitAsync(StepTimeout, TimeProvider, token)` (30 s, a
  placeholder). A late grant is disposed. A printer sign-in that fails or times out is followed by one sign-out.
- A newer tap drops an attempt that has not reached the printer's sign-in. A queue bound (16) applies. The
  printer's own sign-out ends the broker session. A broker refusal signs the printer out. A stop ends every waiting
  tap as `Stopped`.
- The display name in the four forms (first and last name by default, sign-in name, display name, mail), with
  their fallbacks and length limits. Every public type that holds a value prints a fixed mask.
- README with the behaviour and a Limits section.

## What proves it

- 57 new cases (27 facts, 7 theories, 30 rows) against fakes of the identity service and the printer and the real
  `TokenBroker` over an in-memory store, on a test clock. Every cell was red first against stubs.
- 50 consecutive runs of the SignIn assembly: 57 of 57 each time.
- 24 mutants of the product code, each red on its own cell, except one shown equivalent by reading (the attempt
  left cancellable during the printer step).
- C# totals 1638 on both legs at the head (skipped 4 on linux and 19 on windows), RULES 530 files, 111 unit tests
  with floor 111. Merged with the current `main` the totals are 1646.
- No reference to a network, identity, logging, card or Graph library and no writable static field (cell L02). A
  scan of the library's source finds no network, file, console, delay, timer or wall-clock call.

## Still open

- Nothing has run against a printer, a simulator or a tenant. `MaxTapAge` and `StepTimeout` are placeholders.
- A tap the printer re-delivers after a server outage arrives with a fresh stamp and is not caught. That needs the
  outage record or the read-sequence restart, in a later change.
- `DeviceSignedOutAsync` carries no session id, so a late sign-out notice of an earlier session ends the current
  broker session while the printer stays signed in. Whether a printer sends one late is not measured.
- The `Audit` event is a plain multicast event: a subscriber that throws stops the subscribers after it from
  seeing that refusal. The actor itself is unaffected.
- The actor's state is memory only. A printer that does not confirm a sign-out is not retried. A stop during the
  printer's sign-in leaves its result unknown. QR, phone and device-code sign-in, enrolment, the panel button and
  Concurrency retries are not here, and the host does not use the library yet.

## Who decides

The coordinator chose, as coordinator, the cut of this change (the card part only, against fakes) and every
choice inside it: the card string as input, the paths, the identifier comparison and the subject check, the
arrival-time guard with re-delivery as a named limit, the bounds, the queue, the default display-name form and
the names of the types.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
