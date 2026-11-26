Eight owed items of the OXPd 1.x client, built and tested against bodies held in the tests and stubs on 127.0.0.1 only.
One commit, `8ce4a86c`, on `main` `8757daa6` (behind 0, ahead 1). Ten files, all changed, none added: five under
`src/Datasec.Suite.Adapters.Oxpd1/` and five under `tests/Datasec.Suite.Adapters.Oxpd1.Tests/`. No lab file, no package,
no lock file, no project file, no `Datasec.Suite.slnx` line, no workflow, no file under `contracts/` or `build/`.

## Why

- Four strict readers (the sync echo, the CA store, the button records, and through `TextOnly` the `IsServiceEnabled`
  read) tested the text beside an element with .NET's string white-space test, which also takes a no-break space and
  other Unicode spaces that HP's schema reads as text. An answer HP's schema refuses was then read.
- The `IsServiceEnabled` read took text, CDATA or an attribute beside `enabled` (five shapes HP's schema refuses), and
  the lab then sent `EnableService`.
- The callback body was read more loosely than the sync echo's answer, while the README said both were read the same
  way.
- The sign-in agent record and the button target took an address whose user-information part is empty
  (`https://@host/...`), which HP's `LimitedUri` pattern refuses.
- The `Timeout` doc comment said more than the README, and a register's undo was not named as restoring nothing.

## What changed

- **One helper.** `Oxpd1Soap.IsXmlWhiteSpace` (internal) is true only when every character is a space, a tab, a carriage
  return or a line feed. It replaces .NET's test in `ReadTextAnswer` and in the writer's `OnlyElements`, and the
  `TextOnly` rule uses it: a no-break space or any other character beside an element there is text, and the answer
  ends `MalformedAnswer` (the callback: null).
- **`IsServiceEnabled`.** `TextOnly` also refuses an attribute of the response element that is not a namespace
  declaration, and any text of the response that is CDATA or not XML white space. The README's limit that named the
  five shapes is removed.
- **The callback body.** `CallbackMessage` reads the body with the sync echo's own reader (`ReadTextAnswer`): one
  `AsyncEchoStringComplete` with no attribute but a namespace declaration, holding one text-only `message` that is not
  empty (HP's `test:Message`, `minLength` 1) and nothing beside it but XML white space; anything else is null.
- **An `@` in an address.** The sign-in agent's two addresses and the button target refuse an address whose absolute
  form holds `@` anywhere: the rule the echo's callback and the lab's address options already carry. This is stricter
  than HP's `LimitedUri`, which allows an `@` after the first `/`; the README says a target page whose address holds an
  `@` cannot be registered (`%40` is taken).
- **Documentation only.** The `Timeout` summary now says what the README's Typed ends say. The two `Undo` doc comments
  and one README Limits bullet say a register's undo removes the record of its id even when that record was there
  before (HP: a register replaces it), so it restores nothing; the read before a register is the caller's.

## What proves it

- Red first: on `main` with the new cells only, the adapter's tests read `Total: 133, Failed: 23`, every failure an
  assertion of the new cells. Green: the adapter `133 / 0`; the whole solution `total: 2367`, `failed: 0`,
  `succeeded: 2363`, `skipped: 4`; the branch's push run: linux `succeeded: 2363`, windows `succeeded: 2346`, rules
  679 files, `Ran 117 tests`, secret scan clean. The lab's cells over the callback and `IsServiceEnabled` are green on
  both legs.
- Nine mutants, each turning at least its cells red and nothing outside them: the helper as .NET's test; the tab
  dropped; .NET's test back in the echo reader; .NET's test back in `OnlyElements`; the response-text test removed;
  the response-attribute test removed; the callback read loosely; the `@` test dropped from the agent's address; the
  `@` test dropped from the button target.
- 29 new cases: a no-break space before or after the sync echo's result; the callback body's eleven shapes; seven
  `IsServiceEnabled` shapes, each also validated against HP's committed schema; a no-break space beside the CA store's
  entries or result and beside the button records or result; an `@` in each address; each with its XML-white-space or
  no-`@` control taken.

## Still open

- Nothing here has run against a device.
- Not built: a cap on attributes per element (the work after an answer's body stays bounded by the size and depth
  bounds, not by `Timeout`); the lab's own reads before a register are the lab's.
- Known, not changed here: text of any kind in the SOAP `Body` beside the response element, or in the `Envelope`
  beside the `Body`, is not looked at by any of these readers (the response itself is still read whole); text inside
  a button record beside its `id` is not read (a record's other parts are the device's); a value of `enabled` that is
  not an XML Schema boolean (`maybe`, `TRUE`, a no-break space beside it) is answered by the client as written (the
  lab's switch refuses it before any write); a CDATA section holding only white space beside an element, an
  `xsi:schemaLocation` or an `xml:lang` on a response element are refused although HP's schema takes them (the safe
  side).
- The lab README's sentences on the callback and on the five `IsServiceEnabled` answers become stale with this change;
  they are the lab's to update.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (all eight items in one change; one
helper of four characters for every reader; `IsServiceEnabled` fixed rather than named; the callback through the sync
echo's reader, an empty message null; any `@` refused in both records; the `Timeout` and undo changes as documentation
only; new cells only; no local CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent to any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
