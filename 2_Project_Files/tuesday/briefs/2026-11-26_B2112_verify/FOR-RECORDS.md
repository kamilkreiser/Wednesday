# FOR RECORDS: lane OX-A round 1 of 2 (kit B2109, seat X77), the OXPd 1.x client readers, head 8ce4a86c (gate B2112: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2109 THE AUTHORITY; owed items 126, 134 and 93 name "the coordinator's choice" in the owed list's
own words, RELAYED; stamp S4 states Q1 and Q2 "a" in words as Tuesday's, Q3 to Q10 the defaults). Nothing here ran
against a device.

## What the lane gives (RELAYED from the kit's FOR RECORDS, CHECKED by the gate at 8ce4a86c where marked)
- Owed items 133, 143 and 146: one helper (`Oxpd1Soap.IsXmlWhiteSpace`, `Oxpd1Soap.cs:41` at the head) takes only
  space, tab, carriage return and line feed; the sync echo (`ReadTextAnswer`, `:264`), the CA store and button records
  readers (`OnlyElements`, `Oxpd1Writer.cs:764`) and the `TextOnly` read (`Oxpd1Soap.cs:184`) use it. CHECKED: twelve
  characters (U+00A0, U+2028, U+3000, U+FEFF, U+0085, U+2003, U+200B, a letter, raw U+00A0 and U+3000 bytes, CDATA of
  a space, empty CDATA) beside the result, and beside the store's entries and the button records, end `MalformedAnswer`
  in every reader (the callback: null); XML's four characters, a comment and a processing instruction are read
  (`g2112/logs/probe-ws.tsv`). The envelope level is outside (gate FOUND 1).
- Owed item 126 (first option): `IsServiceEnabled` is `Answered` only when the response holds no attribute but a
  namespace declaration and no text but XML white space beside `enabled`; the adapter README's "Known, not changed
  here: five `IsServiceEnabled` answers" bullet is removed (CHECKED: count 0 at the head, 1 at BASE). The five shapes
  of 126 now end `MalformedAnswer` (T08 rows 1 to 5, red on BASE by assertion in the gate's own run), so the lab's
  Test-service switch sends no `EnableService` on them (DERIVED: `ReadBeforeEnableAsync`'s default arm, exit
  `ReadFailed`; not run through the lab).
- Owed item 134, the client half: `CallbackMessage` reads the callback body by `ReadTextAnswer` (`Oxpd1Echo.cs:224`); an
  empty message is null (HP's `test:Message`, `minLength` 1). CHECKED: over 761 bodies the callback, `ReadTextAnswer`
  and the sync echo's reader on the same-shaped body agree on every one (DIFFER 0; 49 answered).
- Owed item 93 (D6 kept): the sign-in agent's two addresses and the button target refuse an address whose absolute form
  holds `@` anywhere (`Oxpd1Writer.cs:188`, `:291`). CHECKED: nine `@` forms refused in all three positions; `%40`
  and look-alike characters are taken (gate FOUND 6, Info).
- Owed item 85: the `Timeout` doc comment narrowed (`Oxpd1ClientOptions.cs:86` to `:89`); the follow-up (a cap on
  attributes per element, or the time-out inside the masking copy) STAYS OWED.
- Owed item 94, the client half: the two `Undo` doc comments (`Oxpd1Writer.cs:357` to `:363`, `:539` to `:542`) and the
  README Limits bullet "A register's undo restores nothing that was there before." (README `:183`).

## Which owed items this squash closes, and which stay owed (the records seat reads and decides)
- **Close on this squash:** 133, 143, 146, 126, 93; 134 (its client half; the item's lab README sentence is lane
  OX-B's, below: the records seat decides whether 134 closes now or when OX-B lands that sentence).
- **85: stays owed** for its named follow-up (the attribute cap); its doc-comment half is done.
- **94: the gate's reading differs from the kit's framing.** The kit and the commission say 94's lab half stays owed as
  item 106. The owed list's own words for 94 are "this item stays open until both land" (a README limit AND, in the lab
  wiring, a read of the device's sign-in agent records before any register, refusing a held id). That lab read is ALREADY
  at BASE (`Oxpd1Command.cs` `ReadBeforeRegisterAsync`, called at `:925`, defined at `:1009` at 8757daa6/8ce4a86c; the
  lab's own summary: "An executed register first reads the device's sign-in agent records and refuses when an agent with
  the same id is already there"), and owed item 106 is the looseness OF that read (filed after it landed). So with this
  squash both halves of 94 exist: the records seat may close 94 naming this squash, with 106 left open for the read's
  strictness (lane OX-B). If the records seat keeps 94 open, its reason is 106, not a missing read.
- **Gate findings of earlier rounds closed by this squash** (if it lands; the records seat checks each): gate B2103
  FOUND 2 (the button records reader took a no-break space beside the records or the result) and gate B2096 FOUND 4
  (the same class in the CA store reader), both through `OnlyElements` (V06 and B06, red on BASE in the gate's run).

## For lane OX-B after this lands (the two lab README sentences; READ at 8757daa6 by `git show ... | awk`)
- `src/Datasec.Suite.Lab/Commands/Oxpd1/README.md:220` (in `:219` to `:221`): "... for ONE callback: a POST to that path
  whose body is HP's `AsyncEchoStringComplete` holding the message." Stale in degree: the callback body is now read by
  the sync echo's rules (no attribute on the element, nothing beside the message but XML white space, a non-empty
  text-only message); the lab answers 400 to every body `CallbackMessage` reads as null (`Oxpd1EchoVerb.cs:518`).
- `src/Datasec.Suite.Lab/Commands/Oxpd1/README.md:308` to `:311`: the bullet "Known, not changed here (MEASURED against a
  stub after the real-path rule landed): ... and five `IsServiceEnabled` answers HP's schema refuses (text beside
  `enabled`, an attribute or `xsi:nil` on its response element) are read as the `enabled` text (the adapter README's
  Limits)." The second half becomes FALSE when this lands (and its pointer to the adapter README's Limits dangles); the
  first half (the relative-link run folder) is not this lane's and stays.

## Owed items, proposed for the records pass (none is ticked by the gate)
- **NEW owed item proposed (gate FOUND 1, Minor): text at the SOAP envelope level is not looked at by any OXPd 1.x
  reader.** Text of any kind (a letter, a no-break space, U+3000, CDATA) in the `Body` beside the response element, or
  in the `Envelope` beside the `Body`, is read past by `ReadAnswer` (`Oxpd1Soap.cs:147`, `:153`), `ReadTextAnswer`
  (`:244`, `:245`), `ReadEmptyAnswer` (`:208`, `:209`), `ReadStore` (`Oxpd1Writer.cs:634`, `:635`) and `ReadButtons`
  (`:712`, `:713`), which take `Elements()` only; MEASURED (`g2112/logs/probe-ws.tsv`): every such shape `Answered`
  (the callback: the message). The response itself is still read whole, so no answer changes; but the README's new
  sentence (README `:146` to `:149`, "Where a reader allows white space beside an element ... a no-break space or any
  other character there is text, and the answer ends `MalformedAnswer`") and the kit's P1 are wider than the code.
  SOAP 1.2 allows only white-space character children there (SOAP 1.2 Part 1, the Envelope and Body information items;
  DERIVED, no envelope schema is committed under `contracts/`, so not measured by schema). Fix when the readers are next
  touched: one envelope-level test with `IsXmlWhiteSpace` over the `Envelope`'s and the `Body`'s text nodes, in one
  shared place, with a row per reader; or narrow the README sentence to the response and result levels.
- **NEW owed item proposed (gate FOUND 2, Minor): the CDATA arm of the new `TextOnly` text test is not pinned by any
  cell.** A mutant dropping `t is XCData ||` from `responseText` (`Oxpd1Soap.cs:184`) survives every cell (the gate's
  `xTextOnlyNoCData`: `Total 133 Failed 0`), because T08's CDATA row holds non-white text that the other arm also
  refuses. The code is right (a CDATA section of only white space beside `enabled` ends `MalformedAnswer`, MEASURED).
  Fix: one T08 row "CDATA holding only white space beside enabled" in a later round.
- **Info, for the device kits:** a value of `enabled` outside XML Schema's boolean (`maybe`, `TRUE`, a no-break space or
  U+3000 beside it) is `Answered` by the client as written and schema-refused; the lab's switch refuses it at
  `XmlConvert.ToBoolean` (exit `ReadFailed`, nothing written); `oxpd1 read` prints it (gate FOUND 3).

## Added by the gate (MEASURED; see VERDICT.md)
- FOUND 1 Minor: envelope-level text unchecked in every OXPd 1.x reader; the README's four-characters sentence is wider.
- FOUND 2 Minor: the CDATA arm of `responseText` survives a mutant (no cell pins a white-space-only CDATA).
- FOUND 3 Info: `IsServiceEnabled`'s value is not checked against `xs:boolean` by the client (the lab refuses it).
- FOUND 4 Info: text inside a button record beside its `id` is read past (gate B2103 FOUND 3's class; by design).
- FOUND 5 Info: the readers refuse schema-valid shapes (a white-space-only CDATA beside an element, `xsi:schemaLocation`
  or `xml:lang` on a response): the safe side.
- FOUND 6 Info: D6 refuses `@` where HP's pattern takes it (a query, a fragment, a path); `%40` and look-alikes are taken;
  no record is built today outside the lab, whose own rule already refuses every `@`.
- FOUND 7 Info: kit and record notes (the kit's first form of `mCallbackLoose` is an equivalent mutant, MEASURED; H10 now
  MEASURED: `Oxpd1Soap.Parse` keeps white-space-only text nodes; the `ReadStore` and `ReadButtons` doc comments still say
  "white-space text"; `ContractTests.Validate` loads without `PreserveWhitespace`).
