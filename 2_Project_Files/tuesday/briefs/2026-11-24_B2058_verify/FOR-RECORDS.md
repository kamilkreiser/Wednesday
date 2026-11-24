# FOR RECORDS: lane L1 round 2 of 2 (kit B2053, seat X65), gate B2052's FOUND 1 to 3 closed, head 105b3465 (gate B2058)

For the records lane only, after the landing; nothing here is written into a project file by the gate. Who decided every
choice of this round: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY:
CLARIFICATIONS.md counts 0 on every subject of the round, MEASURED by the drafter over 1114 lines, RELAYED; Stamp S4
states Q1 "a" and Q2 "a" in words as Tuesday's decisions, Q3 to Q9 the defaults).

## The kit's FOR RECORDS (RELAYED from kit B2053, each checked by the gate against the head)
- Gate B2052's FOUND 1 to 3 (lane L1 round 1, pull request 47) are closed by this round: the client reads
  `IsServiceEnabled`'s answer only as ONE text-only `enabled` element alone in the response (a child element, a sibling
  or an attribute such as `xsi:nil` ends `MalformedAnswer`, so the lab's enable writes nothing, exit 8); the lab's run
  folder rule also reads the path with its symbolic links resolved (exit 9 for a link into a work tree, for `read`,
  `write` and `lab-cert`); a panel capture whose decoded bytes hold the password's UTF-8 bytes is not saved (exit 8).
  CHECKED: `Oxpd1Read.cs:96`, `Oxpd1Soap.cs:174`, `LabFiles.cs:78`, `:87`, `:177`, `Oxpd1Command.cs:357`, `:881`; T07,
  S13, S14, S15 green, each red under its mutants; round 1's probe rows A (four), B (password) and C1 now exit 8, 8 and
  9 (MEASURED). **Record it with two corrections** (below): "alone in the response" holds for ELEMENTS only, and the
  link resolution is by the link's text, so one relative-link shape still escapes.
- The README sentences "so the image is never in a commit" and "the password is ... not in the run folder" are replaced
  by what the code does. CHECKED (Lab `Commands/Oxpd1/README.md:19`-`:23`, `:39`-`:42`).
- Named limits: the client's record of a capture holding the password still holds its base64 text; the check looks for
  the UTF-8 bytes only; the run folder rule is checked once before the folder is made; a link that cannot be resolved
  is read as written. CHECKED and MEASURED (gate probe: 3 client logs decode to the password's bytes; the Basic form and
  UTF-16LE saved; a loop, a dangling link and a folder without permission end exit 5).
- Not built (the coordinator's choice, Q6): cells for gate B2052's FOUND 4 (three surviving mutants) and the FOUND 9
  dry-run clause. Unchanged at the head.
- Nothing here has run against a device: **first-run row 2 on the M577 is a separate kit after this lands.**

## Owed items
- **Owed 124 (gate B2052's FOUND 1 to 3, "must land before any first-run row 2 run on the M577"): tick it at the next
  records pass once this pull request has landed** (squash sha and PR number from the merge). The two residuals below are
  narrower shapes of FOUND 1 and 2, graded Minor by gate B2058 and non-blocking; at the coordinator's choice they are
  either named limits in the records (no code) or a new owed item for a later lane. They do not hold owed 124 open.
- Owed 96 stays open for steps 3 and 4 of the first-run list.
- First-run row 2 on the M577 (the read, the enable, the capture, the disable, `undo-owed`; `--addressing 2004`; a fresh
  session folder) is a SEPARATE kit after this lands.

## Named limits the gate adds (MEASURED by the gate's probe on macOS arm64 against its own stub on 127.0.0.1)
- **Five `IsServiceEnabled` answers HP's schema refuses are still read as `false`:** text directly before or after
  `enabled` in the response, CDATA text beside it, an attribute on the response element, `xsi:nil="true"` on the
  response element: each exit 0, ONE `EnableService` sent, its undo entered, printed and owed (gate B2058 FOUND 1;
  `Oxpd1Soap.cs:174` counts elements only).
- **A relative link whose target walks `..` through another link** (`a/esc -> s/../../repo/sub`, `a/s -> d1/d2/d3`) is
  resolved by its text (`<root>/repo/sub`), not as the system resolves it (`<root>/d1/repo/sub`): a run folder behind it
  is accepted and `panel.png` lands inside that work tree, untracked (gate B2058 FOUND 2; `LabFiles.cs:101`, `:107`).
- Answers HP's schema accepts that are refused (the safe side, exit 8, nothing written): `xsi:type="xs:boolean"`,
  `xsi:schemaLocation` and `xml:lang` on `enabled`.
- A short password can match a capture's bytes by chance: the synthetic password `PNG` refused every capture (exit 8).
- On this Mac a path of 40 or 41 links ends exit 5 (the system's own link limit), so the 40-link bound is never passed
  silently here; Linux and Windows UNMEASURED.
- Local CodeQL is not runnable on this Mac (no Rosetta): the pull request's code scanning is the CodeQL read.
