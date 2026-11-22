The first part of the identity service (WP1.4 in part, component C7): the card store, a new library
`src/Datasec.Suite.Identity/` and its test project `tests/Datasec.Suite.Identity.Tests/`. One commit, `75fb5fdf`, on
`c480a0c8`. 22 files: 21 added under the two new folders, and `Datasec.Suite.slnx` (2 lines added, 0 removed). No
package, project reference beyond `Datasec.Suite.Graph`, workflow, build, lock file of another project or shared file
changes.

## Why

The card-to-user records live in the tenant's custom security attributes, and a card enrolled at a Workpath printer must
work at an OXPd printer and the reverse (design `02` line 16). The sign-in state machine (pull request 23) consumes a
card lookup next; this library is that lookup and the enrolment, against a fake Graph. Only the card store is
buildable now without a package: the Entra sign-in flows need MSAL and the QR gateway client needs SignalR.

## What changed

- `CsaStore.FindUserByCardAsync`: one search by the card's 62-character prefix with `$count=true` and
  `ConsistencyLevel: eventual` (the Workpath app's search, report A1 line 200, with `givenName` and `surname` added to
  its `$select`); per answered user the whole 64-character blob is made for that user's own mail and compared
  ordinally. `Found` only when exactly one user holds it; `NotFound`, `AssociationInvalid` or `Ambiguous` otherwise.
  Two rules differ from the Workpath app on purpose: a failed search is a typed `GraphFailed`, never "no user"; an
  answer with a next page is `Ambiguous`, never "the first page is all".
- `ReadAttributesAsync`: one read of the user's set; one value per single value and per collection entry, annotations
  none; a shape it does not name is `MalformedAnswer`.
- `EnrolCardAsync`: the schema check, a search that no other user holds the prefix, a read of the user, then ONE
  `PATCH users/<id>` of the whole card collection (every held entry in its order, the new blob at the end, the two
  `@odata.type` annotations, no other attribute). Refused at the 16th card entry and the 51st value.
- `EnsureSchemaAsync`: the set and the card definition are checked (`String`, collection, searchable), never created;
  a pass is kept for `SchemaCacheLifetime` (default 1 hour, 1 second to 24 hours) on the store's `TimeProvider`.
- The blob is made by an `ICardBlobCodec` the caller hands in (it needs the card key, which this library never holds);
  its prefix and blob are checked (lengths, base64url, the blob after its prefix) before any of it reaches a request.
- Texts (`ToString`, exception messages) are fixed masks or counts. No logging, no timer, no request of the library's
  own, no POST, PUT or DELETE. The host does not reference the library (published folders 10 and 11 files, unchanged).

## What proves it

- 88 new test cases (19 facts, 17 theories, 69 rows) over the REAL `GraphClient` and an in-memory handler (no socket),
  a no-key blob maker and a test clock. Red first: with the tests and stub store alone, 87 fail by
  `NotImplementedException` and the reference cell is green by design (on `c480a0c8`, and again on main `39f57d6a`:
  1752 / 87 failed).
- 39 product mutants, each red on exactly its listed cells, each undone and rebuilt.
- Whole solution 1750 / 0 at the head (1662 + 88), skipped 4 on linux and 21 on windows, RULES 551 files (530 + 21),
  111 unit tests, floor 111 (push run 45032204534, four jobs success). Merged with main `39f57d6a` locally: 1752 / 0
  (1748 succeeded, 4 skipped), RULES 551.
- The two new lock files hold exactly the Graph layer's packages; no existing lock file changes; the locked restore
  changes nothing.

## Still open

- Nothing has run against a tenant: every address, header, answer shape and status is the fake's assumption, UNMEASURED
  against Graph. The search is eventually consistent; two enrolments for one user at once can lose a card (both report
  `Enrolled`); a user whose mail changed keeps the old entry and both count; attribute names are compared ordinally; a
  value's length limit in Graph is UNMEASURED (README `## Limits`).
- A blob maker that throws `OperationCanceledException` of its own leaves the store untyped (no request is made, no user
  chosen, nothing written). A name twice outside the set (a user's `id` or `mail`, the set itself, the page's `value`)
  is read last-wins, not refused. A failed or cancelled write may still have been applied by the tenant; the next
  enrolment reads `AlreadyEnrolled`.
- Owed: schema creation; writing other values, removing a card, the refresh-token chunks; the blob maker that holds the
  card key; the adapter to the sign-in state machine; the Entra flows, the QR gateway and the national clouds; an
  integration run against a test tenant.
- The two search rules that differ from the Workpath app are deviation-register rows for approval before phase 3 exits.

## Who decides

The coordinator chose, as coordinator, the cut and every choice inside it (the names and limits, the handed-in blob
maker, the two search rules, the count rule, one write of the whole collection, check-only schema, the cache lifetime).
No choice inside this cut is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
