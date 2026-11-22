# FOR RECORDS: OXPd 2 sign-in state machine (kit B1914, seat X28, lane A1, WP1.4 card part, C5), gate G1 round 1, reader B1928

Not repository text. For the next OXPd records pass (Jira `OXPD2-14` stays open; nothing here was written into the
project). No person is named. Who decided: the coordinator (Tuesday), as coordinator; nothing here says the product
owner decided anything about this library.

## What lands

- One commit `af26f801` squashed onto main: 30 new files under `src/Datasec.Suite.SignIn/` and
  `tests/Datasec.Suite.SignIn.Tests/` (two of them lock files written by the restore), and `Datasec.Suite.slnx` +2.
  C# totals +57 on both legs (1646 on main `83683af4`); skipped 4 / 19; RULES 530 files; unit tests 111, floor 111.
- WP1.4 card part: the actor per printer, the card paths, the binding rule (D5), the arrival-time stale-tap guard
  (D7), the four display-name forms (F15). The rest of WP1.4 (QR / phone, device-code and enrolment, the panel button,
  the interactive page) stays OUT, as do the identity service (C7, lane A2) and the adapters' and host's wiring.

## The seat's named limits (its STATUS, FOR RECORDS; read and held by this gate)

- A tap the printer re-delivers after a server outage is not caught (D7); needs the outage record or the
  read-sequence restart, after spike S1.
- `TokenObjectId` is taken as the identity service states it.
- A printer that does not confirm a sign-out is not retried; failure reports and failed sign-outs are dropped.
- A stop during the printer step leaves its result unknown. The actor's state is memory only.
- The broker can end a session on its own while the actor holds it.
- `MaxTapAge` (5 s) and `StepTimeout` (30 s) are placeholders, UNMEASURED. A timed-out acquire is not reported.
- A blocking `Audit` handler blocks that printer's events.

## From this gate (for the backlog)

1. **Owed, Minor:** `Audit` is a plain multicast event raised by one delegate call inside one try/catch. A subscriber
   that throws stops every subscriber after it from seeing that refusal (probe P15, MEASURED macOS: a throwing first
   handler, then a counting second handler: `BindingRefused`, the second saw 0 audits). The actor's result is unchanged.
   Fix sketch: raise to each entry of `GetInvocationList()` under its own try/catch. Owed before the host subscribes an
   audit writer beside anything else.
2. **Info, measured cost of Q11:** a `DeviceSignedOutAsync` queued behind a switch's printer step ends the NEW broker
   session while the printer stays signed in with the new user (probe P11: `SignedIn (previous session ended)`, then
   the late sign-out `True`, broker `sid-2` gone, no printer sign-out). The README's Limits do not name it; the kit's
   Q11 names it as the default's cost. Add it to the README's Limits at the adapters' lane, or take the alternative
   (a session id on the notice).
3. **Info, test gap (not a defect at the head):** three of the gate's own mutants survive the 57 cells.
   `rSubjectIgnoreCase` (the D5 (2) subject compare made case-insensitive): no cell has a subject that differs from the
   object id by case only; the head refuses it (probe P06, `SessionRefused` before any printer call), and under the
   mutant the broker would still refuse it after the printer sign-in (DERIVED from its README's exact subject rule).
   `rSupersedeIgnoredAtPrinter` (the `Superseded` check at the printer gate removed): its window is the synchronous
   code between the acquire's answer and the lock, which no fake can reach deterministically. `rBrokerUserFromToken`
   (the broker's session user taken from the grant's subject): EQUIVALENT by reading (the subject was just checked
   ordinally equal to the object id). Suggested cell: B03 with a subject in upper case.
4. **Info, accepted by the S4 wording:** `Guid.TryParse` takes whitespace-padded, parenthesised, 32-digit and
   hex-struct forms of the same identifier (probe P05: each `SignedIn`), and the all-zero identifier binds when the
   lookup and the token both state it (P07). The identity service's job, as the named limit says.
5. **Info:** a display name or name part holding a bidirectional override (U+202E) or a zero-width space (U+200B) is
   kept: `char.IsControl` does not count format characters (probe P08). D6's wording; a later rule may drop category
   Cf for the panel.
6. **Info:** card strings with a leading or trailing space are taken as distinct cards (P03), as the card rule says.
7. **Measured here (DERIVED in the seat's H22 (2)):** a printer that answers a session id with a space, or null, is
   `SessionRefused` with one sign-out, the grant disposed, nothing stored (probe P12).
