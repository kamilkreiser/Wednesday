# FOR RECORDS: OXPd 2 lane A2, the identity service's card store (kit B1934, seat X36), gate G1 round 1 of 2, reader B1941

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: the cut and every choice inside it, Q1 to Q14 the defaults,
Q4 and Q8 in words at kit B1934's stamp S4. Nothing here says the product owner decided, ruled or approved anything
about this library; the kit's CLARIFICATIONS grep for the lane's subject words counted 0 (RELAYED, kit B1934).

## What lands

- WP1.4 in part, C7 first slice (`02:367`, `03:156`): one commit `75fb5fdf` (parent `c480a0c8`) squashed onto main,
  22 files (21 added under `src/Datasec.Suite.Identity/` and `tests/Datasec.Suite.Identity.Tests/`, two solution
  lines). C# totals +88 on both legs (1750 on `c480a0c8`; 1752 on main `39f57d6a`, measured locally); skipped 4 / 21
  unchanged; RULES +21 (551 on either base); unit tests 111, floor 111.
- The card store against a fake Graph; the Workpath app's names and limits (`HPAuthenticationSuite`, `cardId`, 15
  cards, 50 values, `A1:185-194`); the search's failure and next-page rules that differ from the Workpath app (Q4 as
  stamped); the schema checked, never created (Q8 as stamped). The host does not reference the library.
- `OXPD2-14` stays open (no Jira call by the seat or the gate).

## Deviation-register rows owed (plan `03:108`, OQ-6 `03:378`; for the product owner's approval before phase 3 exits)

The project's deviation register in `1_Project_Definition/` gets these rows from the records seat; the gate writes no
register line. The class is the gate's reading of `03:108`, for the records seat to confirm:

1. **The card search: a failed status is a typed failure (`GraphFailed`), never "no user".** Workpath: `A1:208` ("a
   failed HTTP status on that search is treated as "no user"", sending an existing user down the enrolment path).
   Reading: class (3), a security fix of a listed weakness: **W10** (`02:691`, "Silent failures that look like success
   or "new user" (failed search = unknown card; swallowed write errors)", target "Lookup failure is an error state,
   never "unknown card"; write failures fail the sign-in"; source `A1:564`, report A1 section 8.2 item 11). Built:
   `CsaStore.cs:228-237`; cell F06 (400, 403, 404, 500), mutant `mMissingEverywhere`.
2. **The card search: an answer with a next page is `Ambiguous`, nobody chosen; in an enrolment it is
   `HeldByAnotherUser`, nothing written.** Workpath: `A1:208` ("Only the first page of the card search is read").
   Reading: no W row covers it (the W table `02:682-708` read for "page"): a design choice neither ruled nor forced,
   which `03:108` also sends to OQ-6. Built: `CsaStore.cs:66-69`, `:113`, `:207`; cells F04, E06; mutant
   `mFirstPageOnly`.
3. **Two choices beside them that are this design's, not Workpath's measured behaviour, for the same register's
   judgement (the gate's suggestion; the records seat decides whether they are rows):** (a) an enrolment is refused
   when ANY other user holds the card's prefix, also for another mail (E06 second row); Workpath's enrolment rule for
   that case is UNMEASURED (`A1:200-208` describe the search, not the enrolment's check); (b) the schema is checked and
   never created, where the Workpath app creates the set and the definitions on demand (`A1:185`); a tenant no
   Workpath printer has used fails `SchemaMissing` until creation lands (owed item 1 below).

## Owed items this lane leaves (RELAYED from kit B1934 FOR RECORDS, for the records seat to number)

1. Schema creation (the set and the card definition: a body from a source, then a cell per field).
2. The second slice of the store: writing other values (`UPAR`, per-user values), removing a card, the refresh-token
   chunks (`A1:190`, a security question first: stored as plain text there).
3. The blob maker that holds the card key (master list item 1; design `02:613`).
4. The adapter from `CardLookupResult` to lane A1's `ICardIdentityService` (after lane F1 lands).
5. The Entra flows, the QR gateway and the national clouds (each a package: a supervised fetch, C-61).
6. An integration run against a test tenant (every UNMEASURED of kit H18).
7. Graph's limit on one value's length.

## From this gate (for the backlog)

1. **Owed, Minor (VERDICT FOUND 1): a blob maker that throws `OperationCanceledException` (or `TaskCanceledException`)
   of its own leaves the store untyped.** `CsaStore.cs:282` and `:299` catch `when (failure is not
   OperationCanceledException)`, so the maker's own cancellation passes through although the caller did not cancel.
   MEASURED (gate probe P07, macOS arm64, on the head): prefix maker throws it, caller's token not cancelled: find ends
   `OperationCanceledException`, requests 0; blob maker throws `TaskCanceledException` in an enrolment: ends
   `TaskCanceledException`, patches 0. Nothing is requested, chosen or written, but the call ends in neither a typed
   result nor the caller's cancellation (kit D10 and the README's "Every call returns its typed result, or throws ...").
   Fix sketch: hand the call's token to `PrefixOf` and `BlobOf` and filter `when (failure is not
   OperationCanceledException || !cancellationToken.IsCancellationRequested)`, with an F08 row per maker (+2 cases).
2. **Owed, Minor (VERDICT FOUND 2): a name twice outside the set is read last-wins, not refused.** `CsaReading.Set`
   refuses a name twice INSIDE the set (`CsaReading.cs:67-73`, F07 "a name twice"), but `RequiredString`,
   `OptionalString` (`:132-145`) and the set and page reads (`CsaReading.cs:47`, `:57`; `CsaStore.cs:196`, `:207`) use
   `TryGetProperty`, which takes the LAST of duplicate names. MEASURED (probe P05): `mail` twice, the holder's mail
   last, `Found`; first, `AssociationInvalid`; `id` twice, another id first, `Found` with the last id; the set twice
   and the page's `value` twice, the last read. The README says "Answers are read strictly: a shape the store does not
   name is `MalformedAnswer`". Only an answer Graph itself sends reaches this (UNMEASURED whether Graph ever repeats a
   name), so no path is open to a caller; it is a strictness gap against the README. Fix sketch: one duplicate-name
   check of the user object, `customSecurityAttributes` and the page (a small helper in `CsaReading`), F07 and R03 rows
   (+4 cases), or a README Limits line naming last-wins.
3. **Info, for the integration run (owed item 6): a null value inside the set fails the read, and with it the search
   of every card that user holds.** MEASURED (P05): `"refreshToken": null` in a user's set: read `MalformedAnswer`;
   enrol `MalformedAnswer`; beside a true holder in a search answer: the whole search `MalformedAnswer`. A null set or
   null attributes read empty (R02). Whether Graph ever answers a null attribute inside a set (for example after the
   Workpath app's "PATCH with an empty refreshToken collection", `A1:206`) is UNMEASURED. Measure it in the integration
   run; if Graph does, a null attribute needs its rule (count 0, or a named limit).
4. **Info: a failed or cancelled write may still have been applied.** MEASURED (P08): the tenant applies the PATCH and
   answers 500: `GraphFailed`, the card is held; cancelled after the tenant applied it: `TaskCanceledException`, the
   card is held, the next enrolment `AlreadyEnrolled`; answered 503 then retried by the Graph layer: `Enrolled`, two
   PATCHes, no duplicate entry. No half-written state exists (one PATCH of the whole collection, idempotent), but the
   README's "a `CsaStoreException` ... after which nothing of that call is used or written" can be read as "the write
   did not happen". A README clause ("a failed or cancelled write may have been applied; enrolling again reads
   `AlreadyEnrolled`") would close it.
5. **Info: the schema check does not read the definition's `status`, `usePreDefinedValuesOnly`, `attributeSet` or
   `name`.** MEASURED (P11): a definition with `status` `Deprecated`, with `usePreDefinedValuesOnly` true, or naming
   another set and attribute, passes. With predefined values only, an enrolment would be refused by Graph at the
   write (UNMEASURED), typed `GraphFailed`. For owed item 1 (schema creation) to settle together.
6. **Info: concurrent enrolments lose a card silently.** MEASURED (P09): two enrolments of two cards for one user at
   once: both `Enrolled`, two PATCHes, one card left. The README names the loss; neither caller is told.
7. **Info: the mail tag is two characters.** By `A1:189` the last two of the 64 characters derive from the mail
   (12 bits); the store's user binding is exactly that comparison (Workpath's format, kept by `02:748`). The store
   chooses no user on a prefix alone (P01: case, padding, a trailing space, the bare prefix all `AssociationInvalid`).
8. **Info: an empty mail reaches the maker as an empty text, not null** (P03c). What the real maker does with "" against
   null is the maker's (owed item 3), UNMEASURED.

## Not measured (carried)

- Every Graph address, header, answer shape and status (the fake's); the search's lag; Graph's attribute-name case
  rule; a value's length limit; whether Graph counts annotations against the 50; the PATCH replacing the whole
  collection; the schema permission for a later creation (each UNMEASURED, kit H18).
- The hosted legs on the merge with main `39f57d6a` (windows succeeded 1731 PREDICTED); lane F1's round 2 (not pushed
  at the gate's read).
- CodeQL on the pull request (no pull request exists yet).
