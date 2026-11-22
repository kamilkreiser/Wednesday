# FOR RECORDS: OXPd 2 sign-in and device-token follow-ups (kit B1935, lane F1), gate G1 round 1 of 2, reader B1938

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator (Q1 = a, Q2 = a, each the coordinator's stamp S4, and every
other default of the kit); nothing here says the product owner decided anything about this lane.

## State at this gate

- Verdict NO GO at `c15e13f5` (round 1 of 2): goes back as a fix round. Nothing lands from this verdict.
- Proved and needing nothing in round 2: (a) the audit fan-out (B08; order, snapshot and one arguments object measured
  in scratch); (b) the empty identifier refused at the lookup in every form `Guid.TryParse` reads (B09, B10; P, X and
  padded forms in scratch); (c) the two SignIn README Limits lines, true by the code.
- (d) closes the T13 shape and the concurrent-callers shape (main disposed the held object there), but not the three
  paths below.

## From this gate (for the backlog or the round-2 kit)

1. **Minor: a same-object answer that arrives after the issue bound is disposed by the late-answer path**
   (`DisposeLate`, `CloudDeviceTokenHolder.cs:227` to `:242`, reached from `:263` to `:268`), which clears the held
   token; the next renewal that fails inside the lifetime serves the cleared bytes. MEASURED (probe G1, head and main
   alike): `held disposed by the late answer True; third (issuer throws) served len 27 all zero True`. The new README
   sentence "that object is kept as it is (not disposed)" (`README.md:108` to `:109`) is false in that shape. Fix
   sketch: skip the late dispose under `entry.Sync` when the late answer is the held object, with a cell of G1's shape.
2. **Minor: a race between a same-object answer and a concurrent `Invalidate` with a current copy.** The disposed check
   (`:278` to `:286`) runs outside the entry's lock; an `Invalidate` before `Finish` takes it nulls `Held`, the
   same-object compare fails, and the disposed object is held as accepted. MEASURED (probe G4, 3000 runs, one run each):
   head 14 served all-zero, main 2973. Fix sketch: re-check `answer.IsDisposed` in `Finish` under `entry.Sync`.
3. **Minor, unchanged from main and not named: one issuer object answered to two registrations** is held by both; the
   holder's own `Remove`, `Invalidate` or renewal of one clears it for the other. MEASURED: G2 and G3, `served len 27
   all zero True` on head and main. Fix sketch: name it in the Limits line `README.md:140` to `:142`, or refuse an
   answer held by another entry, or the kit's Q1 alternative c.
4. **Info: the Limits line's "the holder cannot tell either"** for a copy answered back: a copy carries `Origin` and
   `Generation`, so the holder could tell; "does not check" is exact. G6 re-measured the drafter's Q2 shape.
5. **Carried from the kit, not in this lane:** gate B1929 I-1 (a grant whose access token is already disposed reaches
   the printer before the broker refuses it); gate B1928 FOUND 3 and 5; the D7 re-delivery limit's cost.
6. **For the kit form (agreeing with the seat's note):** the gate rebuilt after every mutant's undo, as the commission
   asked; with that order every run that had to be green was green.
7. **UNMEASURED:** every probe on Linux and Windows; how the real device-token issuer hands over its answers (it is
   not in the library); whether a printer sends a late sign-out.
