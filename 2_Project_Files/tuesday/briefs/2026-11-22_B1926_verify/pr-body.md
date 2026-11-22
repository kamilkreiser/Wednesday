The OXPd 2 adapter README names its limits as the code stands, owed items 45 and 46 of the backlog (their README
halves). One commit `b1079275` on `main` `4a0a9717`, one file: `src/Datasec.Suite.Adapters.Oxpd2/README.md` (+49 -1).
No `.cs` file, no test, no generator, package, project, lock, solution or workflow file changes. No build or test reads
this file.

## Why

The adapter landed with only one of its known limits in the README (the timing of the enrolled-serial lookup). The
readers of the adapter lane and of the tolerant-reading lane listed the others. This change states each one, so a
reader of the README is not handed a behaviour the code does not have.

## What changed

- Three new headings under `## Limits`, after its last bullet; no existing bullet is moved or changed.
  - `### Limits of the token holder` (seven bullets): `StoreRefreshValue` neither waits for nor stops a refresh in
    flight, and both its write and a rotated refresh value reach the vault (the last write stays); an access value
    already handed to a request is still sent once after `Forget`; the vault calls of a rotation and of `Forget` run
    under the serial's lock, and `Dispose` can hold every other serial's lookup behind one (UNMEASURED with a real
    store); a refresh answered after `RefreshTimeout` is not waited for and its grant is never stored, and two calls
    can be in flight (whether a late grant should be kept is an open question); a 401 after a failed refresh of its
    serial ends with that failure; a `Forget` whose vault delete throws reports `VaultFailed` and leaves the old
    refresh value; a vault binding must return a fresh copy from every `TryGet`.
  - `### Limits of the callback credentials` (three bullets): a stored hash of the wrong length reads as no
    credential (`Unauthorized`), not `Unavailable`; a read that is not cached, and a wrong-length read, are dropped
    without being zeroed; the `Issue` race cell is held by two mechanisms, so removing the generation bump alone turns
    no cell red.
  - `### Limits of the generated reading` (three bullets): the 206 `additionalProperties` of the 37 specification
    inputs are all `false` and the generator does not read the keyword (an input with a map: UNMEASURED); the runtime
    options write an enum only by its wire name and read only a listed wire name or the unrecognized member; what a
    printer does with a refused or a tolerated callback is UNMEASURED.
- The parse step's line in Part 2: the full stop inside the list of semicolons becomes a semicolon, and the line says
  that device answers are read strictly as a choice for now, to be looked at again once a printer's traffic is seen.

The README carries no `file:line`: the line that proves each sentence lives in the lane's proof table, not in the file.

## What proves it

- Each sentence was read beside the code it describes, and a program checks 68 `file:line` tokens against the
  source (68 of 68 present; moved one line down, 68 of 68 fail) and 13 counts no single line can show (13 of 13).
- The one claim about the tests was run: with `Bump(serial);` removed from `Issue` the adapter's test executable
  stays green (58 cases, 0 failed); with that change and the cache fill made unconditional together, exactly the
  `Issue` race cell turns red (58 cases, 1 failed); the cache-fill change alone stays green.
- C# totals 1579 on both legs, unchanged (skipped 4 on linux and 19 on windows); RULES 500 files; 111 unit tests,
  floor 111 (branch run 45015821397, four jobs success).

## Still open

- Whether a refresh answered after its timeout should be kept is named as an open question, not answered.
- The one-line doc comment on `IDeviceSecretVault.TryGet` (item 45's other half) is a `.cs` change and stays owed to a
  later code lane.
- "The specification inputs hold no map" is true of a declared map (`additionalProperties` with a schema,
  `patternProperties`, `propertyNames`: none). The inputs also hold 150 objects that declare neither `properties` nor
  `additionalProperties`, and some of them are generated as a raw `JsonElement`; the README does not name them yet.

## Who decides

The lane, its scope (item 45's limits (1) to (11), README halves only, and item 46's README lines that are limits),
the grouping under three headings and the proof table are the coordinator's choices, made as coordinator.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
