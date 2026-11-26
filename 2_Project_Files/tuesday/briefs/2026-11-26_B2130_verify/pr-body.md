Six owed items of the lab tool `oxpd1`, built and tested against a stub device on 127.0.0.1 and the parsers alone,
inside the test process. One commit, `0ae90664`, on `main` `504ca043` (behind 0, ahead 1). Six files, all changed, none
added: `Oxpd1Command.cs`, `Oxpd1EchoVerb.cs` and the README under `src/Datasec.Suite.Lab/Commands/Oxpd1/`, and two test
files and the test stub under `tests/Datasec.Suite.Lab.Tests/Oxpd1/`. No adapter file, no package, no lock file, no
project file, no `Datasec.Suite.slnx` line, no workflow, no file under `contracts/` or `build/`.

## Why

- An executed register read the agent records first, but an answer whose result carried text, CDATA, an attribute or
  `xsi:nil`, or a record holding a second `id` (of another namespace, unqualified, or nested), was taken as holding no
  agent with the run's id, and the register was sent.
- The three address options took U+FFFF in a host (the envelope's writer then threw after the run folder was made), a
  host that is not ASCII (written as typed) and a lone surrogate (written as the percent-encoded U+FFFD).
- The name and title bound of 100 was said in characters while the code and the client count UTF-16 code units.
- An async echo took a callback host whose callback address the client then refused by throwing, after the run folder
  was made; a delay at least as long as the wait or the time-out was taken and ended the run blaming the path or the
  device.

## What changed

- **The read before a register.** Four refusals, each exit 10 with `the read's result holds text, an attribute or a
  second id that the run cannot read whole; nothing was written`: an attribute on the result that is not a namespace
  declaration; a text node of the result that is not XML white space (space, tab, CR, LF); a record whose descendants
  hold an element of local name `id` other than its own one; an attribute or a text node of the same kinds on a record.
  The landed refusals and their words are unchanged.
- **The addresses.** `--agent-service`, `--prompt-page` and `--button-target` take a text only when every character is
  in U+0021 to U+007E, before the landed https, 256 and `@` rules; the two error lines say so.
- **The echo.** One helper builds the callback address for the run and for the parser; the parser refuses a callback
  host whose address with port 65535 and a path of the run's form is over 256 characters (a host name of at most 199),
  and a `--delay-ms` at least `--callback-wait-seconds` (async) or `--timeout-seconds` (sync), defaults counted, each
  exit 2 before any folder.
- **The README** says each rule, counts the bound of 100 in UTF-16 code units, and names in its Limits what the read
  before a register cannot see and that the delay and length rules compare times and assume the longest port.

## What proves it

- Red first: on `main` with the new cells only, the lab's tests read `Total: 352, Failed: 26`, every failure an
  assertion of the new cells. Green: the lab `352 / 0`; the whole solution `total: 2422`, `failed: 0`,
  `succeeded: 2418`, `skipped: 4`; the branch's push run: linux `succeeded: 2418`, windows `succeeded: 2401`, rules
  679 files, `Ran 117 tests`, secret scan clean.
- Eleven mutants, each turning at least its cells red and nothing outside them: each of the four refusals removed (or
  the id count back to the own-namespace children), the ASCII test removed, the length test removed or its bound made
  257, each delay test removed or made to take an equal delay.
- 38 new cases in six cells: twelve answer shapes (nine refused, a namespace declaration taken, and two shapes the
  read cannot see pinned as taken: a comment, and the id as another agent's name); ten addresses (eight refused, an
  `xn--` host and a percent-escaped path taken); the bound at 50 and 51 characters outside the basic plane for a name
  and a title; callback hosts of 232, 200 and 199 characters and a whole run with the longest; eight delays.

## Still open

- Nothing here has run against a device.
- The read before a register cannot see what the client does not hand it: a comment, a `<?...?>` node, anything beside
  the result, and the content of an element whose name the client's logging mask covers (a second `id` inside such an
  element of a record is not seen). The id as the text or an attribute of a record's other elements is not read either.
- The device host and `--callback-host` are not under the ASCII rule: a callback host that is not ASCII is sent as
  typed, and a callback host holding a lone surrogate ends the run with an exception before any folder.
- The delay rule compares times only (the network's own delay is not counted); the length rule assumes port 65535, so
  with a shorter port a host is refused up to six characters early.
- A name or title of 100 UTF-16 code units can show fewer characters (a combining sequence counts each unit).
- The write section's `IsServiceEnabled` sentence of the lab README is unchanged (true, not complete).
- Within ASCII an address reaches the device in .NET's canonical form (host in lower case, the default port left out,
  dot segments removed, characters such as `"` `<` `{` percent-encoded); the dry run prints the envelope.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (one change for all six items; the code
written to a specification; the read's refusals widened from the result to the record and to any depth; printable
ASCII for the three address options; the bound left in UTF-16 code units with a pinning cell; the length check in the
parser with the longest port assumed; the delay rule as a usage error with defaults counted; one stub member; no local
CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent to any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
