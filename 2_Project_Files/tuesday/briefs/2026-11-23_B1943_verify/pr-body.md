Follow-ups of the sign-in state machine (WP1.4) and the device-token holder (WP4.1). Two commits on this branch, landed
as one squash: `c15e13f5` (round 1, parent `c480a0c8`) and `93ea278e` (round 2, a fast-forward on `c15e13f5`). Seven
existing files change, all under `src/Datasec.Suite.SignIn/`, `tests/Datasec.Suite.SignIn.Tests/`,
`src/Datasec.Suite.UniversalPrint/Registration/` and its test folder. No file is added, and no public member,
`TapOutcome` or `RegistrationError` member, package, project, lock, solution or workflow file changes.

## Why

- One `Audit` handler that threw hid a binding refusal from every handler after it: the multicast delegate was called
  inside one `try`.
- A card user whose object id was the empty identifier (all zeros) was signed in.
- The sign-in README did not say when a tap can take effect, nor what a printer sign-out queued behind a switch does.
- An issuer that answered a renewal with the very token object the holder held made the holder dispose that object
  and hand out a zero-byte token with no error.

## What changed

Round 1 (`c15e13f5`):

- `SignInActor.RaiseAudit`: one `SignInAuditEventArgs`, then each entry of `GetInvocationList()` in its own `try`, in
  subscription order. `SignInActor`: `|| userId == Guid.Empty` beside the `Guid.TryParse` of the card user's object
  id, so such a lookup answer is `LookupFailed` and changes nothing. SignIn README: two sentences and two Limits lines.
- `CloudDeviceTokenHolder.Finish`: under the entry's lock, an answer that `ReferenceEquals` the held token is not held
  and not disposed; `Failed` with `TokenAnswerRefused`, so the failed-renewal rule serves the held token while its
  lifetime lasts. Cells `B08`, `B09` (three forms), `B10`, `T13`.

The read of round 1 measured three paths its README sentence on the same-object renewal ("that object is kept as it is")
did not hold for: an answer arriving after the bound, a race with `Invalidate`, and one object for two registrations.
That sentence had been stamped on the coordinator's own premature reading of round 1's kit; it is retracted and
rewritten in round 2 from what the code does.

Round 2 (`93ea278e`):

- The late-answer clean-up (`DisposeLate`) takes the registration's lock and does not dispose an answer that is, at
  that moment, the very token object held; that object stays held and is owned like any held token. Cell `T14`.
- `Finish` checks `answer.IsDisposed` again under the registration's lock before anything is held, so an `Invalidate`
  (or a late clean-up) between the first check and the hold can no longer get a disposed token held.
- Registration README: the late-answer and answer sentences rewritten from the code, and the Limits line now names one
  token object answered for two registrations and says the holder "does not check" a copy's origin.

## What proves it

- Red first (macOS arm64): round 1's cells alone at `c480a0c8`: SignIn 62, 5 failed; Universal Print 347, 1 failed
  (T13). Round 2's cell alone at `c15e13f5`: Universal Print 348, 1 failed (T14, `the late answer's clean-up disposed
  the held token`). Each by its own assertion; green with the fix.
- Six mutants, each red on exactly its cells (B08; B09's three forms and B10; T13, three mutants; T14). The seventh, the removed
  re-check in `Finish`, survives every cell (a race window has no deterministic cell); scratch race probes are its control: 3000 runs each,
  all-zero tokens served 0 and 0 at the head, 6 and 4 with the re-check removed, 7 and 2970 on `c15e13f5` (counts of
  a race on one machine, not rates).
- C# totals 1669 on both legs at the head (1662 + 7), skipped 4 on linux and 21 on windows, RULES 530 files, 111 unit
  tests with floor 111 (push run 45036798637, four jobs success). Merged with main `0c3900b7` locally: 1759 / 0 (1755
  succeeded, 4 skipped), RULES 551.

## Still open

- Named in the Registration README Limits: an issuer that keeps a token it handed over and later disposes or changes
  it; a copy the holder handed out answered back; one token object answered for two registrations (then the holder's
  own `Remove`, `Invalidate`, renewal or late clean-up for one clears the bytes the other holds).
- Not yet named: one object answered to two calls for ONE id across a `Remove` (the old call's answer, late or in
  time, is disposed and clears the object the id holds again; measured, the same before this change).
- How the real device-token issuer hands over its answers is not known (it is not in the library). Whether a printer
  sends a late sign-out is not known.

## Who decides

The coordinator chose, as coordinator, both rounds' cut and every choice inside them: the empty identifier refused
at the lookup, one `try` per handler, a same-object renewal refused with the held token kept, the late clean-up that
skips the held object under the lock, the disposed re-check with a named surviving mutant, and the two-registration
shape named rather than refused. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
