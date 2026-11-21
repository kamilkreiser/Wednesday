Changes how the generated parser reads the calls a printer makes INTO the server (the five service-target
specifications: Authentication, JobStatistics, ScanJob, UsbAccessories, UserPolicy). One commit. The change is made in
the generator under `contracts/oxpd2/generator/` and regenerated into `Generated/` (11 files changed, none added or
removed); nothing under `Generated/` is edited by hand, and the landed regeneration test passes.

## What changes, for the service targets only

- **An enum value the specification does not list** is read as that enum's new first member `Unrecognized` (value 0,
  the type's default, marked by the new runtime attribute `Oxpd2UnrecognizedAttribute`), and the rest of the
  callback is used. Matching is exact (ordinal) on the wire name: another letter case, the C# member name, padding,
  an escaped control character, the word `Unrecognized` itself, a number in a string and an empty string each read as
  `Unrecognized`, never as a listed member. An escaped spelling of a listed value reads as that member. A number,
  object, array or boolean in an enum position is still refused `WrongType`.
- **An optional property sent as JSON null** is read as absent and does not count toward `minProperties` or
  `maxProperties`, so a one-of object whose only members are null (or unknown names) is still refused `OutOfRange`.
- **Still refused, as before:** a required property absent or null (`MissingRequired`), a null array item and a
  null body (`WrongType`), the body size limit (checked before anything is read), depth, duplicate keys. A
  duplicate key whose first value is null is now refused `DuplicateKey` (the null is read as absent, then the second
  key is the duplicate); before this change the same body was refused `WrongType` at the null.
- **The raw text of an unlisted value is not kept** anywhere. A new overload
  `Oxpd2Json.TryParse<T>(body, limits, out value, out refusal, out int unrecognized, out IReadOnlyList<string> unrecognizedPaths)`
  reports, on a value only, how many unlisted values were read and the paths (schema names and indexes) of the first
  16 (`MaxReportedPaths`); a refusal reports 0 and an empty, read-only list. The four-argument overload, which the
  adapter's callback handler calls, keeps its signature.

## What does not change

- **The 16 device clients stay strict**: an unlisted value or an optional null in a device answer is refused as
  before, and no client enum or schema gains the new member or flag.
- **Nothing unrecognized is written**: the runtime's own enum converter (it replaces `JsonStringEnumConverter`)
  writes only listed wire names and throws `JsonException` (a fixed message, no value) for `Unrecognized` or any
  number that is not a named member, for every enum. The answer models of the service targets hold no enum.
- **Never a success**: `Unrecognized` is 0 and no listed member is 0, so a check by equality with a success member
  reads it as not succeeded. A new test fails if code outside `Generated/` compares a target enum with `!=` or
  `is not`; today no code outside `Generated/` names a target enum at all.
- The adapter's product code is unchanged; one sentence of its README now describes the behaviour above. In its
  tests, the one refusal row whose only fault was an unlisted value moved into a new delivery case (`P03_`): the
  callback reaches the sink once, reads `Unrecognized`, and is `Answered`.

## Limits, stated plainly

- What a printer does with a refused or a tolerated callback is UNMEASURED; no printer was used.
- Nothing reads the report yet; a later change decides who logs or shows it.
- A new member of a one-of result (an unknown property name) is skipped as before, and the object is then refused.
- No schema of the inputs is a map today; a later input with one would reach the generator's existing paths.
- A sink that serialises the callback model it was handed, with `Unrecognized` in it, gets the converter's
  `JsonException`, and the handler ends that call `SinkFailed`.
- The converter refuses to read or write an enum that has no wire names (the runtime's and the adapter's own enums)
  with `Oxpd2Json.Options`; nothing does so today.
- The exclusion test reads one line at a time: a comparison split across lines, a `switch`, or a value compared
  through a local is not caught by it; it lists every line naming a target enum.

12 new tests (1392 -> 1404 locally and on both hosted legs; skipped 4 on linux, 19 on windows, as before). No package,
lock file, solution line, workflow, build script or project reference changes. Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
