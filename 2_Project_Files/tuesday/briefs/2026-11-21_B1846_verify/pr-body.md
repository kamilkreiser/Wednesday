## What this closes

One commit that follows up three points of the OXPd 2 contracts lane's first independent check. Every code change is in
the generator (`contracts/oxpd2/generator`). `src/Datasec.Suite.Adapters.Oxpd2/Generated` is regenerated from it, five
files change, and none is edited by hand. The existing regeneration test checks on both build legs that the committed
folder matches a fresh generation. The new tests are in `tests/Datasec.Suite.Contracts.Tests`.

- **Read-only lists.** Four public `IReadOnlyList` members handed out the arrays behind them:
  `Oxpd2Schema.Properties`, `Oxpd2Schema.EnumValues`, `Oxpd2InboundOperation.RequestContentTypes` and
  `Oxpd2InboundCatalogue.Operations`. Any code in the process could cast one of them and write to it, and that write
  changed the result of every later parse. Each member now returns one `ReadOnlyCollection` made once, and the parser
  reads the private arrays. `RequestContentTypes` wraps a copy of the array it is given. New cells: a reflection walk
  that fails if any public list-shaped member of the runtime, the catalogue or any reachable schema can be written to
  (it visits 4362 schemas), with a control that names a member backed by an array; and a cast-and-write cell that
  tries an identity write first, then the write that would clear a required property, and then checks that a later
  parse refuses the same body at the same path.
- **A bounded body limit.** A client built with a body limit near `int.MaxValue` threw `OverflowException` on a small
  answer. `Oxpd2ParseLimits` now refuses any `maxBodyBytes` above the new `Oxpd2ParseLimits.HighestMaxBodyBytes`,
  which is `System.Array.MaxLength - 1` (2147483590 on .NET 10.0.15). The bounded read keeps the limit plus one byte,
  so the read code itself is unchanged. New cells: the constructor's edges, and the first JSON-answer method of each of
  the 16 clients, built at the highest accepted limit, reading a small answer with and without a declared length.
- **The Unicode length rule.** String lengths were already counted in Unicode scalar values, but no test pinned that
  down. Row N9 gains strings of astral characters, written as raw UTF-8, at `maxLength` (accepted) and one past it
  (refused), at `minLength` and one under it where `minLength` is 2 or more, and a mixed row. Each row first checks
  that its body is within the size limit. If the code counted UTF-16 units instead of scalar values, N9 would now fail.

## Behaviour change

**`new Oxpd2ParseLimits(maxBodyBytes, maxDepth)` now throws `ArgumentOutOfRangeException` (parameter `maxBodyBytes`)
for any value above `Oxpd2ParseLimits.HighestMaxBodyBytes` (`System.Array.MaxLength - 1`).** Values such as
`int.MaxValue - 1` used to be accepted and are now refused when the limits are made. Every value from 1 up to the bound
is accepted as before. The defaults (1 MiB, depth 32) and every parse result are unchanged.

## What this does not change or prove

- The parser's results are otherwise unchanged. The same inputs give the same value or refusal before and after this
  change, and no refusal holds a byte of the body.
- Not covered by design: reflection into private fields, and the lists inside one parsed value (each parse builds its
  own, and no later parse reads them). A client at the highest limit given a body near 2 GiB is not tested.
- Nothing here talks to a printer, a simulator or a tenant. Every payload is synthetic.
- No HP input, fingerprint list, project file, lock file, package, workflow, build file or solution-file line changes.
  Every choice in this change was made inside the build. Nothing is deployed and nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
