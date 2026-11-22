# FOR RECORDS: OXPd 2 Universal Print registration fix (kit B1915 + ANSWER-1, lane U), gate G1 round 1, reader B1924

Not repository text. For the next OXPd records pass (backlog owed items 52 to 55, Jira `OXPD2-18`); nothing here was
written into the project. No person is named. Who decided: the coordinator (Tuesday), as coordinator; nothing here
says the product owner decided anything about this round.

## What lands

- Two commits `759c9060` and `d383d21c` squashed onto main as one: eight existing files under the two `Registration/`
  folders (product +96 -32, tests +423 -4 against `4e8828ee`). C# totals +8 on both legs (1589 on main `7b0f4f55`);
  skipped 4 / 19; RULES 500 files; unit tests 111, floor 111.
- Owed item 52 closes: `DeleteRegistration` takes the attach lock; X02.
- Owed item 53 closes: the issuer through `Task.Run`; T11. A blocked issuer holds one pool thread (README limit).
- Owed item 54 closes: K06 (`mNoZeroPkcs8`), R05 (`mReadCertLoose`), C16 (`mTimeIgnored`, `mVerifySystemClock`; C14
  no longer kills them on macOS), the cheap check T12. `mCatchNarrow` and `mFixUndone` stay named survivors on macOS.
- Owed item 55(1) closes by the modulus rule (C15, red on macOS at main). RSA issuers only; s + n on Linux and Windows
  green at the head (the platforms refuse it or the rule does; which one is UNMEASURED there).
- Item 54 F2 / the hosted Windows gap (RELAYED, ANSWER-1): rule 8 now requires every chain element inside its window on
  the library's clock (C14, red on hosted Windows at 759c9060, green at d383d21c); C16 a chain judged on the library's
  clock alone (green on Windows: the platform does not judge on the real clock, ANSWER-1 reading (ii) ruled out).
- Items 55(2) to (7), 56 and 57 unchanged.

## From this gate (for the backlog)

1. **Owed, Minor, unchanged from main:** an issuer that answers a renewal with the SAME token object the holder already
   holds: `Finish` disposes `entry.Held` (that object) and then holds it, so every caller gets a token of zero bytes
   with no error (probe G04b, MEASURED macOS: 27 bytes, all zero). After an `Invalidate` the same shape is refused by
   the new disposed check (G04). Fix sketch: in `Finish`, refuse or skip the dispose when `ReferenceEquals(answer,
   entry.Held)`, or have the holder copy the answer's bytes into a token it owns (which also closes an issuer that
   disposes its answer after returning it, DERIVED). Owed before the real issuer lands.
2. **Info:** the window clause and the modulus clause judge the one chain the platform built. Two configured issuers of
   one name and key, one expired by the library's clock: ACCEPTED on macOS in both orders (G08); Linux and Windows
   UNMEASURED; a platform that picked the expired one would refuse (fail closed).
3. **Info:** the window clause's only red is hosted Windows (C14 at 759c9060); the three window mutants survive on
   macOS (the same standing as `mFixUndone`, killed on Linux only).
4. **Measured here (was DERIVED in the seat's H36):** an issuer that returns a null task is `TokenUnavailable` and the
   next call asks again (G03).
5. **Info:** the modulus clause refuses a signature not exactly the modulus's length (255- and 257-byte encodings of a
   real signature value both `IssuerNotTrusted`, the 256-byte original with its leading zero ACCEPTED; G05). A signer
   that strips a leading zero would see about one certificate in 256 refused; a real issuer's output is UNMEASURED.
