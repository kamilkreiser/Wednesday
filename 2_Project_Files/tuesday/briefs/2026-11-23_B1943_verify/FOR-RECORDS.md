# FOR RECORDS: OXPd 2 sign-in and device-token follow-ups (lane F1: kits B1935 and B1940), gate G1 round 2 of 2, reader B1943

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: both rounds' cut and every choice inside them (kit B1935 Q1 = a,
Q2 = a; kit B1940 Q1 = a, Q2 = a, Q3 = a, each in words at its stamp S4, and every other default). Round 1's README
sentence on the same-object renewal rested on the coordinator's premature ratification at kit B1935's Q1; gate B1938
measured it false and kit B1940 retracted and rewrote it. Nothing here says the product owner decided, ruled or
approved anything about this lane (kit B1940's CLARIFICATIONS greps for the subject words counted 0, RELAYED).

## State at this gate

- Verdict GO WITH FINDINGS at `93ea278e` on main `0c3900b7` (round 2 of 2). Lands as ONE squash of `c15e13f5` and
  `93ea278e` (landing.txt in this folder): C# totals +7 on both legs (1669 on `c480a0c8`; 1759 on main `0c3900b7`,
  measured locally), skipped 4 / 21 unchanged, RULES unchanged (530 on `c480a0c8`, 551 on `0c3900b7`), unit tests 111,
  floor 111.
- Gate B1938's findings, measured at the head:
  1. FOUND 1 (the late same-object answer disposed by the clean-up): CLOSED. T14 red at `c15e13f5`, green at the head,
     red under `mLateDisposesHeld` only; probe L1 (B1938 G1's own form, 500 runs): head `disposed False | third served
     bytes 1 = 500`, `c15e13f5` `disposed True | third served len 27 all zero = 500`.
  2. FOUND 2 (the race with `Invalidate`): CLOSED. `CloudDeviceTokenHolder.cs:318` to `:324`; probe R1 (G4's shape,
     3000 runs): head all-zero 0, `c15e13f5` 7, with the re-check removed 6; the late-clean-up race R2 (3000): head 0,
     removed re-check 4, `c15e13f5` 2970. `mNoDisposedRecheck` is the named surviving mutant (348 / 0).
  3. FOUND 3 (one object for two registrations): NAMED (`README.md:146` to `:149`), not refused (kit B1940 Q2 = a).
  4. FOUND 4 ("cannot tell"): CLOSED ("does not check", `README.md:146`).
- Parts (a) to (c) (round 1's SignIn work): byte for byte `c15e13f5` (round 2 touches no SignIn path); `mAuditOneTry`
  and `mEmptyTaken` still red on exactly their cells.

## From this gate (for the backlog)

1. **Minor, NOT NAMED, unchanged by this lane (the same at `c15e13f5`): one token object answered to two calls for ONE
   registration id across a `Remove`.** `Remove(id)` retires the entry (`CloudDeviceTokenHolder.cs:211` to `:224`); a
   later `GetAsync(id)` makes a new entry (`:71` to `:75`). An old call's answer that is the object the NEW entry
   holds is disposed: late, by `DisposeLate`, which compares with the OLD entry's `Held` (null after `Retire`,
   `:236` to `:241`); in time, by `Finish`'s removed path (`:328` to `:331`). The id then serves cleared bytes.
   MEASURED (probes H15a, H15b, head and `c15e13f5` alike): `X disposed by the old entry's late answer True; the new
   registration then served len 27 all zero`; `X disposed by the old entry's answer True; ... served len 27 all zero`.
   Read literally ("registration" = the id), `README.md:104` to `:106` ("unless it is the very token object the
   registration holds at that moment: that object is kept as it is") is false in H15a; the Remove bullet
   (`README.md:115` to `:116`, "an answer that arrives later is disposed") is true; the Limits line names two
   registrations, not one id across a `Remove`. Needs a buggy issuer that answers one object to two calls (H3's
   family). Fix sketch (DERIVED, not built): name it in the Limits line ("one token object answered to two
   registrations, or to two calls for one id across a `Remove`"), no code change; or a refusal across entries (kit
   B1940 D3: not small or safe). The seat disclosed this shape as H15 (STATUS, DERIVED); the gate measured it.
2. **Info: T14's comment and its wait.** `CloudDeviceTokenHolderTests.cs:474` to `:477` say the clean-up "has run
   when this task ends", then wait for `issuer.Issued.Count == 2`. `FakeIssuer.RunAsync` adds the token to `Issued`
   before its task completes (`FakeIssuer.cs:155` to `:164`), so the wait does not prove the clean-up ran; the red at
   `c15e13f5` rests on the continuation running inline (`ExecuteSynchronously`, `CloudDeviceTokenHolder.cs:250`) on
   the thread that completes the issuer's task. MEASURED red 1 of 1 here, 20000 of 20000 by the drafter (RELAYED). At
   the head the cell cannot read red for timing (DERIVED: a clean-up that runs later also keeps the held object). A
   future cell author: wait on the object's state, not on `Issued`.
3. **Info: a late answer that is a copy a caller holds is disposed, clearing that caller's copy** (probe L2, head and
   `c15e13f5`: `the caller's copy disposed by the late clean-up True; the holder then served bytes 1`). As the README
   says (a late answer that is not the held object is disposed); the caller's `AsSpan` then throws
   `ObjectDisposedException` (`CloudDeviceToken.cs:48`), never cleared bytes. No change needed; the issuer misbehaved.
4. **Info (DERIVED, unchanged by this lane): an answer that completes at the very instant of the bound** fails the
   `when (!call.IsCompleted)` filter (`:272`), so it is reported `TokenUnavailable` and disposed by `DisposeLate`
   (unless it is the held object, then kept). Not a held-token path; a wording question for "An issuer that throws is
   `TokenUnavailable`" (`README.md:113`).
5. **Info (DERIVED): the late clean-up now waits for the registration's lock on the thread that completes the
   issuer's task** (`ExecuteSynchronously`), for at most one of the holder's own short sections; no path nests
   `_sync` and an entry's lock (GetAsync `:68` / `:82`, Invalidate `:144` / `:155`, Remove `:174` / `:214`, Dispose
   `:191` / `:214`), and nothing completes a task while holding an entry's lock (`Finish` `:342`, `Retire` `:223` after
   the lock; `Flight.Done` runs continuations asynchronously, `:350`). Under an entry's lock the holder calls the
   handed-in `TimeProvider` (`:89`, `:121`, `:337`), as before this lane. MEASURED: probe D1, 600 runs of late
   answers, renewals, callers and `Invalidate` at once: every task ended within its bound; all-zero 0 at the head
   (3 with the re-check removed, 29 at `c15e13f5`).
6. **Carried, not in this lane (RELAYED from kit B1940):** gate B1929 I-1; gate B1928 FOUND 3 and 5; the D7
   re-delivery limit's cost; the real issuer's hand-over of its answers (UNMEASURED); kit B1940 NOT DECIDED item 1
   (whether the holder should own a copy of every answer's bytes: it would close H3, H4, H5, H12 and item 1 above).
7. **UNMEASURED:** every probe on Linux and Windows; the hosted legs on the merge with main `0c3900b7` (windows
   succeeded 1738 PREDICTED); CodeQL on the pull request (none open yet).
