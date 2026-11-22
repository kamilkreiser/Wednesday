Follow-ups of the sign-in state machine (WP1.4) and the device-token holder (WP4.1). One commit on this branch,
`c15e13f5`, parent `c480a0c8` (main). Seven existing files change, all under `src/Datasec.Suite.SignIn/`,
`tests/Datasec.Suite.SignIn.Tests/`, `src/Datasec.Suite.UniversalPrint/Registration/` and its test folder. No file is
added, and no public member, `TapOutcome` or `RegistrationError` member, package, project, lock, solution or workflow
file changes. The landing is one squash.

## Why

- One `Audit` handler that threw hid a binding refusal from every handler after it: the multicast delegate was called
  inside one `try`.
- A card user whose object id was the empty identifier (all zeros) was signed in.
- The sign-in README did not say when a tap can take effect, nor what a printer sign-out queued behind a switch does.
- An issuer that answered a renewal with the very token object the holder held made the holder dispose that object
  and hand out a zero-byte token with no error.

## What changed

- `SignInActor.RaiseAudit`: one `SignInAuditEventArgs`, then each entry of `GetInvocationList()` in its own `try`, in
  subscription order. The event's doc comment says so.
- `SignInActor`: `|| userId == Guid.Empty` beside the existing `Guid.TryParse` of the card user's object id, so such a
  lookup answer is `LookupFailed` and changes nothing.
- SignIn README: the two sentences above, and two Limits lines (`MaxTapAge` plus four `StepTimeout` bounds, about 125
  seconds at the defaults; a late printer sign-out ends the new broker session, UNMEASURED whether a printer sends it).
- `CloudDeviceTokenHolder.Finish`: under the entry's lock, an answer that `ReferenceEquals` the held token is not held
  and not disposed; the outcome is `Failed` with `TokenAnswerRefused`, so the existing failed-renewal rule serves the
  held token while its lifetime lasts. Registration README: the answer rule and one Limits line.
- Cells: `B08`, `B09` (three forms), `B10` and `T13`; `Kit` gains one optional parameter. No existing cell, helper or
  assertion changes.

## What proves it

- Red first on macOS arm64 with the cells alone at `c480a0c8`: SignIn 62, 5 failed (B08, three B09 rows, B10); Universal Print
  347, 1 failed (T13); each by its own assertion. Green with the fix: 62 and 347, 0 failed.
- Five mutants, each red on exactly its cells: one `try` for the whole list (B08); the empty identifier taken (three
  B09 rows, B10); the same-object check never met, the object refused but disposed, the object taken as a renewal (T13 each).
- Outside the cells, measured in scratch on the head: the empty identifier in the `P`, `X` and padded forms is
  `LookupFailed` with no acquire; handlers keep subscription order and the raise is a snapshot; fifty callers racing a
  same-object renewal get one call and the held bytes.
- C# totals 1668 on both legs at the head (1662 + 6), skipped 4 on linux and 21 on windows, RULES 530 files, 111 unit
  tests with floor 111 (push run 45029555551, four jobs success). With the other open lane as well: 1670, measured
  locally.

## Still open

- A held token object answered after the issue bound is disposed by the late-answer path, and the next failed renewal
  within the lifetime hands out its cleared bytes (measured); the README's new answer sentence is false in that shape.
- An `Invalidate` with a current copy that lands between the disposed check and the hold can still make the holder
  hold a disposed answer (measured as a race: 14 of 3000 runs on the head, 2973 of 3000 on `main`).
- One issuer object answered to two registrations is held by both; when the holder lets it go for one, the other
  serves cleared bytes (measured; the same on `main`; not named in the README).
- The README's "the holder cannot tell either" for a copy answered back: the holder does not check, though a copy
  carries its origin.

## Who decides

The coordinator chose, as coordinator, to make these four follow-ups one change and every choice inside it: the
empty identifier refused at the lookup rather than at the binding rule, a same-object renewal refused with the held
token kept, one `try` per handler, and the README limits named rather than asserted.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
