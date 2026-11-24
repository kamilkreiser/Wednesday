# FOR RECORDS: lane L1 (kit B2048, seat X63), the OXPd 1.x Test service on and off and one panel capture (first-run row 2, built against the stubs), head a7f74ff3 (gate B2052)

For the records lane only, after the landing; nothing here is written into a project file by the gate. Who decided every
choice of this lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY:
CLARIFICATIONS.md counts 0 on every subject of the lane, MEASURED by the drafter and re-run by the seat over 1114 lines,
RELAYED; Stamp S4 states Q1 "a" and Q2 "a" in words as Tuesday's decisions, Q3 to Q11 the defaults).

## The kit's FOR RECORDS (RELAYED from kit B2048, each checked by the gate against the head)
- The OXPd 1.x client reads two operations of HP's committed Test binding: `IsServiceEnabled` (admitted by name as the one
  read whose name does not start with `Get`; no other name without `Get` passes, over every operation of the seven
  committed bindings) and `GetScreenCapture`; and writes two: `EnableTestService` and `DisableTestService` (the disable is
  the enable's undo). CHECKED: `Oxpd1Read.cs:110` (`NonGetRead`), `:113`-`:114` (`IsReadName`: `StartsWith("Get",
  Ordinal) || Equals(NonGetRead, Ordinal)`), `:133`-`:134`; `Oxpd1Writer.cs:182`; T01 and T02 green, each red under its
  mutant.
- The lab's `oxpd1 write --write EnableTestService --execute` reads `IsServiceEnabled` first and writes nothing when the
  service is already on (exit 0, no undo owed); `DisableTestService` makes no read; `undo-owed` owes a disable for each
  enable that may have taken effect until a disable on the same host has answered. CHECKED: `Oxpd1Command.cs:777`-`:784`,
  `:867`-`:904`; `LabFiles.cs:234`, `:238`, `:255`; S02 to S06, S11, S12; the gate's probe D1 to D3 (below).
- `oxpd1 read --read GetScreenCapture` saves the panel image whole as `panel.png` in the run folder (base64 that decodes to
  bytes starting with the PNG signature only; size bounded by the client's 1 MiB answer bound; never printed; the run
  folder is refused inside a git work tree). CHECKED with one correction: the git work-tree refusal reads the path as
  written (`LabFiles.cs:76`, `:85`); a run folder under a symbolic link into a work tree is NOT refused (gate FOUND 2,
  MEASURED). Record it with that limit.
- The two README sentences on the WS-Addressing version now state the M577 reading (2005 answered an empty 400, 2004
  answered); the default is unchanged. CHECKED against the first-run seat's STATUS BLUF item 3 (line 26 of
  `Briefs/2026-11-24_B2044_STATUS.md`: R03 2005 `HttpStatus 400, empty answer`; r03b 2004 answered 200; firmware
  `2510156_069175`), read by the gate; `Oxpd1ClientOptions.Addressing` unchanged (not in the diff).
- Named limits: the read before an enable and the enable are not atomic; what a device does with a disable of a service
  already off is UNMEASURED; a real panel capture's size is UNMEASURED; a password inside the base64 text breaks the
  capture (exit 8); the PNG check is the signature only. CHECKED (probe B: password text in the base64 text: exit 8,
  nothing saved; trailing bytes after a PNG: saved whole).
- **Owed 96 stays open for steps 3 and 4.** Nothing here has run against a device: **first-run row 2 on the M577 is a
  separate kit** (after landing: `--addressing 2004`, a fresh session folder, the read, the enable, the capture, the
  disable, `undo-owed`).

## Named limits the gate adds (MEASURED by the gate's probe on macOS arm64 against its own stub on 127.0.0.1)
- **The read before an enable takes the JOINED text of `enabled`** (`Oxpd1Command.cs:888`, `XElement.Value`): an
  `enabled` holding a child element whose text is `false`, a `false` split by an element, `false` followed by an extra
  sibling element, or `false` with `xsi:nil="true"` is taken as off and ONE `EnableService` is sent (its undo entered,
  printed and owed). Answers outside HP's schema; gate FOUND 1.
- **`panel.png` is decoded device bytes and is not scrubbed:** a synthetic PNG carrying the password's bytes was saved
  whole with them (the output, the summary and the client's log held no password). The landed sentence "The password is
  ... not in the run folder" (`Commands/Oxpd1/README.md:37`-`:38`) no longer covers every file of the run folder; gate
  FOUND 3.
- The capture's real bound is about three quarters of `MaxAnswerBytes` (base64): 780,000 bytes saved, 790,000 bytes
  `TooLarge` (exit 8, nothing saved), MEASURED.
- Base64 with line breaks inside, and a result whose text is split by a child element, decode and are saved (lenient,
  bytes equal); text after the base64 (`...==junk!!`), two results, an empty result and the 8-byte signature alone save
  nothing (exit 8).
- Two enables in one session: the second finds the service on and writes nothing; after a reboot (stub off) a third
  enable writes again; `undo-owed` names ONE disable (the latest enable on that host), and one answered disable clears it.
- `IsServiceEnabled` is "Added for OXPd Release 1.7" in HP's committed `test.xsd` (the comment at line 920, above `IsServiceEnabled`, `EnableService`, `DisableService`): whether the M577's
  firmware answers it is UNMEASURED (the device kit's first read says).
- Local CodeQL is not runnable on this Mac (no Rosetta): the pull request's code scanning is the CodeQL read.
