Lab tool hygiene before its first run against a printer. One commit, `25cb4cb2`, on `2e2feae8` (ahead 1; `main` has since
gained the OXPd 1.x sign-in agent writes, `b4b4ef60`, which touch no Lab path: the merge builds and its 2054 cases pass).
Two files are added (`src/Datasec.Suite.Lab/Commands/ParserWords.cs`, `tests/Datasec.Suite.Lab.Tests/HygieneTests.cs`) and
fourteen change, all under `src/Datasec.Suite.Lab/` or `tests/Datasec.Suite.Lab.Tests/` (the four commands, `RunRecorder`,
`Masking`, `LabFiles`, the command table and device channel doc comments, the three Lab READMEs, and the two registry
cells). No package, no `.csproj`, no lock file, no `Datasec.Suite.slnx` line, no workflow, no `Directory.*` file, no path of
the OXPd 1.x client.

## Why

- A pin or the admin password typed in the wrong place (`--password=<value>`, a stray word) was echoed by the usage error,
  and agents drive this tool, so its output lands in transcripts.
- A blank `--run` or `--credentials-file`, an unreadable or dangling-link credentials file, or a run folder that cannot be
  made ended in an unhandled exception where each README lists an exit code.
- A `probe` run without `--pin` could still send the plain-HTTP discovery tree GET.
- A JSON answer holding one name twice crashed the masking; a typed body was read by its first byte.
- Two doc comments no longer said what the code does, and two registry cells listed the commands exactly, so every new
  command had to edit them.

## What changed

- `ParserWords`: a word the parser does not know is named by its position only (`argument <n> is not an option of this
  command (the word is not shown)`); an option of the command given last is still named (`no value after --pin`), from a
  closed list in each command's code. All four parsers (`probe`, `print`, `oxpd1 read`, `oxpd1 lab-cert`) use it.
- Exit 2 for a blank `--run` (each command) and a blank `--credentials-file`; exit 5 for a run folder that exists or cannot
  be made (the reason names the exception's type only); exit 7 for a credentials file that cannot be read.
- `probe`: `--plain-discovery-tree` needs `--pin` (exit 2 without it).
- `Masking`: `ArgumentException` caught (the body is not shown, only its type and length); a body is read by its first
  byte only when it has no type.
- `CommandRegistry.cs` and `DeviceChannel.cs` doc comments corrected; P13 and R11 check names by contains (distinct, every
  usage listed, print right after probe).

## What proves it

- Red first on `main` + the test files: Lab 129 / 28 failed, exactly the 28 planted cases, each by an `Assert.` line.
  Green: 2041 / 0 / 2037 / 4. 16 mutants, 15 each red on exactly its cells and a fourth command red on none.
- The branch's push run 45160807294: linux 2037 succeeded, windows 2020 succeeded, rules 645 files, secret scan clean.

## Still open

- A word typed as the value of a known option is taken as that value: a pin or password given as `--run`'s value names the
  run folder and is printed; a password with a host name's shape typed as the host is printed as the host (stated limits).
- A write that fails after the run folder is made (the summary, a call's record, `lab-cert`'s files) is not caught.
- With `--pin`, the plain discovery tree GET can go out before any handshake checked the pin.
- A credentials file that is a named pipe with no writer blocks `oxpd1 read` until a writer appears (nothing is sent);
  a usage error's argument number counts from the command's own arguments, not the whole line.
- No device has been reached.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (one helper for all four parsers, exit 5
and exit 7 widened rather than new codes, the plain-needs-pin rule, the untyped-only sniffing, the contains-checks). No
choice in this change is the product owner's.

Nothing is deployed; nothing was sent.
