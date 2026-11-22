# FOR RECORDS: OXPd 2 card store follow-ups (lane A2-F, kit B1944, seat X40), gate G1 round 2 of 2 of lane A2, reader B1950

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this round's cut and every choice inside it (kit B1944 Q1 = a
and Q2 = a, each in words at its stamp S4; Q3 to Q6 the defaults). Nothing here says the product owner decided, ruled
or approved anything about this lane (kit B1944's CLARIFICATIONS greps for the subject words counted 0, RELAYED; the
strict printer-answer ruling C-63 is about the printer and is not cited for this library).

## State at this gate

- Verdict GO WITH FINDINGS at `a56ed63b` on main `394fa997` (round 2 of 2 of lane A2). Lands as ONE squash
  (landing.txt in this folder): C# totals +24 on both legs (1783 on `394fa997`, measured locally and on the head's push
  run), skipped 4 / 21 unchanged, RULES unchanged (551), unit tests 111, floor 111. With lane F3's head: 1785, RULES 553
  (measured locally).
- Gate B1941's findings, measured at the head:
  1. FOUND 1 (a blob maker's own cancellation left the store untyped): CLOSED. F12 (6 rows) red at `394fa997`, green at
     the head, red under `mPrefixCancelPasses` and `mBlobCancelPasses`; probe P07 (20 maker shapes, head against main):
     `CodecFailed` each at the head, the 12 cancellation shapes untyped at main.
  2. FOUND 2 (a name twice outside the set read last-wins): CLOSED by refusal. F13, R07, K06, E11 (18 rows) red at
     `394fa997`, green at the head; four new mutants each MATCH; probe P05 (mail, escaped mail, id, value, set, nextLink
     twice): `MalformedAnswer` at the head, the last copy read at main.
- Q4 (deviation register): not a register row in the kit's reading (Workpath's handling of a repeated name and of a
  maker's cancellation is UNMEASURED; neither change alters what is stored); for the records seat to judge.

## From this gate (for the backlog)

1. **Owed, Minor (VERDICT FOUND 1): a name with an invalid escape (a lone UTF-16 surrogate) anywhere in an answer ends
   the call in an untyped `InvalidOperationException`.** The whole-answer walk reads every name (`CsaReading.cs:163`);
   `GetJsonAsync` catches only `JsonException` (`CsaStore.cs:250`). MEASURED (probe P05x, macOS arm64): such a name in
   an unread property of a search user, in another attribute set, at the page's top level, in the user read, in the
   schema definition answer, in an enrolment's search: untyped at the head (0 PATCH); main read those answers normally
   (the enrolment wrote its PATCH). Already untyped at main and unchanged: such a name inside `HPAuthenticationSuite`,
   and such an escape in a value the store reads (`displayName`, by `GetString`); an unread value is harmless at both.
   Nothing is chosen or written. Whether Graph ever sends such an escape is UNMEASURED. Fix sketch: catch
   `InvalidOperationException` beside `JsonException` at `CsaStore.cs:250` (+1 F13 row: closes every name case); the
   value case needs the reads in the same typed catch (+1 R row).
2. **Info: D4's named cost is stated in the README only by "any object, at any depth"** (`README.md:41` to `:43`); the
   README does not say in words that a repeated name in a part the store never reads also fails the call, nor that
   Graph's sending one is UNMEASURED (the seat's observation, confirmed). The frozen patch is the kit's text, as S4 asked.
3. **Info (DERIVED, MEASURED as the kit's H8): a caller that cancelled while the maker throws gets `CodecFailed`, not its
   cancellation** (probe: the caller's source cancelled inside the maker, which throws with the caller's token: find 1
   request, enrolment 4, then `CodecFailed`). Typed; not named in the README.
4. **Info: D4 judged from the repository's own sources.** No answer shape with a repeated name is documented in report A1
   (`A1:200`, `:204` are addresses only), A4, A6, A9 or the design `02` / `03`; the one documented collection form holds
   `cardId@odata.type` beside `cardId`, two names. A refusal is typed (`MalformedAnswer`), never "unknown card" (W10).
5. **Info: cosmetic** `FindTests.cs:240` `Exception thrown =kind` (no space; builds without a warning).
6. **Carried, not in this lane (RELAYED from kit B1944):** gate B1941 FOR-RECORDS items 3 to 8 (a null value inside the
   set, a failed or cancelled write that was applied, the schema definition's unread fields, concurrent enrolments, the
   two-character mail tag, an empty mail), lane A2's owed items 1 to 7, Q4's two departures for OQ-6 (the records
   lane's); and kit B1944's NOT DECIDED item 1 (whether Graph ever repeats a name; the integration run).
7. **UNMEASURED:** every probe on Linux and Windows; the hosted legs on the merge with lane F3 (windows succeeded 1764
   PREDICTED); CodeQL on the pull request (none open yet); every Graph answer shape (the fake's).
