# FOR RECORDS: lane LH (kit B2006, seat X58), the lab tool's hygiene before the first printer run, head 25cb4cb2 (gate B2009)

For the records lane only; nothing here is written into a project file by the gate. Who decided every choice of this
lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY; CLARIFICATIONS.md counts 0
on every subject of the lane, RELAYED from the drafter; S4's answers are the defaults, each the coordinator's).

## Owed items this commit builds (numbers MEASURED in BACKLOG.md by the drafter at 20:58, RELAYED; the records lane ticks
## each only with the pull request that lands it)
- **88 ECHO**: built for all four parsers (`probe`, `print`, `oxpd1 read`, `oxpd1 lab-cert`) through `ParserWords`.
- **89 EXITS**: blank `--run` / `--credentials-file` exit 2; a run folder that cannot be made exit 5 ("exists or cannot be
  made"); a credentials file that cannot be read exit 7.
- **80 PLAIN**: the coordinator's interim first-run rule ("no run passes --plain-discovery-tree without --pin") is code
  (`ProbeCommand.cs:128`).
- **82 DUP**: `Masking.Body` catches `ArgumentException` (a repeated JSON name is not shown).
- **90 LABTEXT**: `CommandRegistry.cs:19` and `DeviceChannel.cs:37` corrected; P13 and R11 are contains-checks,
  red-proofed (3 mutants red, a fourth command red on none).
- **81 SHOWN**: only an untyped body is read by its first byte.

## From the kit's FOR RECORDS (RELAYED, copied)
- ECHO is built for all four parsers (`probe` and `lab-cert` beyond the commission's two). A word typed after a known
  option is taken as its value (`--run <pin>` names the folder and is printed): a named limit in the Print and Oxpd1
  READMEs. A word given as the host is taken as the host when it reads as a DNS name or an IPv4 address.
- EXITS: exit 5 now means "run folder exists or cannot be made" and exit 7 of `oxpd1 read` "no password read from the
  file" (missing, unreadable, no such name, empty). A write failing after the folder is made (the summary, a call's
  record, `lab-cert`'s files, the client's log) is not caught: a named limit.
- PLAIN: with a pin, the plain call can still go out before any handshake checked the pin (as before).
- DUP and SHOWN: a typed body is read by its type alone, and only an untyped body by its first byte. A type naming json
  or xml anywhere in its text is read as that kind.
- Y05's mode-000 and dangling-link rows return at once on Windows (no Unix mode; a link needs a privilege there); the
  held-open row is the read failure on every leg.
- Left for the next lane (the coordinator's order): the lab wiring of lane W1's write calls and the end-of-session undo
  list (design review B1996 F19).

## Changed by the gate's measurements (MEASURED, gate probe, macOS arm64, .NET 10.0.404, stubs on 127.0.0.1)
- **H5 is no longer only DERIVED:** a 64-hex word (lower or upper case) is `UriHostNameType.Unknown` and is refused as
  a host by all four parsers with a fixed text. A host-shaped password is taken as the host (the stated limit holds).
- **ECHO measured wide:** 192 argument shapes (`=` forms, unicode lookalikes of `--`, empty and space words, repeats,
  every insert position) over the four parsers: the word in no output.
- **PLAIN measured over every order:** 120 argument orders and 9 malformed-pin shapes without a valid pin: 0 requests,
  0 TLS connections.
- **EXITS:** exit 5 holds for a read-only parent, a 300-character name and a path below `/dev/null` (reasons
  `UnauthorizedAccessException`, `PathTooLongException`, `DirectoryNotFoundException`); exit 7 holds for a symbolic-link
  loop, a file in a mode-000 folder and `/dev/null`.
- **H21 measured:** a type of "" or spaces is sniffed; an untyped JSON body led by a BOM or a space is not shown.

## Main moved during the gate (for the landing record)
- Lane W1 landed as PR 41 (main `b4b4ef60`, 22:20:48 AEDT) while this gate ran; this lane's merge with it is clean
  (tree `4af54a4b`), builds, and tests 2054 / 0 / 2050 / 4 with RULES 647 (= W1's main 2020 / 645 plus 34 and plus 2).
  The landing form is written for that main.

## Gate findings to carry (VERDICT.md FOUND; one Minor, six Info; none blocking)
- FOUND 1 (Minor): a credentials file that is a named pipe with no writer blocks `oxpd1 read` (no cancellation reaches
  the synchronous read) instead of ending in exit 7; nothing sent, nothing printed. Round 2: read only a regular file,
  or a README limit.
- FOUND 2 (Info): the usage error's argument number counts from the command's own arguments, not the whole line.
- FOUND 3 (Info): a lone U+200B is not blank to .NET and is taken as a name.
- FOUND 4 (Info): H5 and the value limits measured (above).
- FOUND 5 (Info): the exit-9 line prints the folder holding `.git`, not the typed `--run` value (the seat's H24 (i) is
  broader than the code).
- FOUND 6 (Info): masking edges measured; the new catch can hide, never reveal.
- FOUND 7 (Info): on Windows the `UnauthorizedAccessException` catch of the credentials reader has no cell (Q6's
  designed early return).
