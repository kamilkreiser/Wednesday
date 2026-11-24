The OXPd 1.x Test service on and off and one panel capture, for the first-run list's row 2, built against stubs only. One
commit, `a7f74ff3`, on `main` `c6f5d36a` (behind 0, ahead 1). Fifteen files: two test files added
(`TestServiceTests.cs`, `Oxpd1TestServiceTests.cs`) and thirteen changed, all under `src/Datasec.Suite.Adapters.Oxpd1/`,
`src/Datasec.Suite.Lab/Commands/Oxpd1/`, the two matching test folders and `src/Datasec.Suite.Lab/README.md`. No package,
no lock file, no project file, no `Datasec.Suite.slnx` line, no workflow, no file under `contracts/`.

## Why

- Row 2 of the first-run list (turn on the OXPd Test service and take one panel screenshot) was not built. HP's Test
  service is off at every boot, answers `IsServiceEnabled` while off, and needs admin credentials for `EnableService` and
  `GetScreenCapture` (HP's committed `test.wsdl`).
- The committed contracts README says the read comes first: a disable sent as the undo of an enable turns off a service
  the lane did not turn on, so the undo is owed only when the run turned it on.

## What changed

- **The client.** Two reads, `IsServiceEnabled` (its answer is HP's `enabled` element) and `GetScreenCapture`; two writes,
  `EnableTestService` and `DisableTestService` (HP's empty elements; the disable is the enable's undo). The read-only check
  of the catalogue admits an operation whose name starts with `Get` or is exactly `IsServiceEnabled` (`NonGetRead`); the
  closed list and the action rule are unchanged.
- **The lab.** `oxpd1 write --write EnableTestService` is a dry run unless `--execute`. Executed, it reads
  `IsServiceEnabled` first and writes nothing when the service is already on (exit 0, no undo owed) or when the read is
  refused (6), faults or does not answer a boolean (8); otherwise the undo list's pending row, ONE `EnableService`, the
  row's end, and the printed undo `--write DisableTestService --execute`. A disable makes no read. `undo-owed` owes a
  disable for each enable that may have applied until a disable on the same host has answered after it; a Test service
  line carries the all-zero id. `oxpd1 read --read GetScreenCapture` saves the decoded bytes whole as `panel.png` in the
  run folder when they start with the PNG signature, prints the name, size and SHA-256, never the bytes; exit 8 otherwise.
  `--read` takes the reads by name only (a number is a usage error).
- **Text.** The adapter README, the lab command README and the lab README; the two WS-Addressing sentences state the one
  device reading (the lab's M577 answered 2004/08 and refused 2005/08) and the default is unchanged.
- Four counts of earlier cells move with the new rows (`C03` 5 to 7 and `test.xsd` in its schema set, `K01` 5 to 7, `W01`
  2 to 4); no other line of an earlier cell changes.

## What proves it

- Red first on a permissive first shape: 22 cases fail by assertion (adapter `Total: 47, Failed: 4`; lab `Total: 219,
  Failed: 18`). Green: 2153 / 0 / 2149 / 4 locally; the branch's push run 45339675420: linux 2149 succeeded, windows 2132
  succeeded, rules 659 files, secret scan clean.
- 16 mutants, each red on exactly its cells, none surviving (the one name widened to every `Is` name, the form rule
  dropped, the `enabled` element ignored, the enable's undo removed, the read before the enable skipped or ignored, a
  refused or failed read going on, an agent id taken, `--read` by number, the capture not saved or not checked, an enable
  not owed, any disable clearing, the id rule dropped).
- Against a stub on 127.0.0.1: two `enabled` elements, an `enabled` in another namespace or with no namespace, and
  `TRUE` or `False` write nothing (exit 8); `true`, ` true ` and `1` write nothing (exit 0, already on). A capture with
  text after the base64, two results, or the PNG signature alone saves nothing (exit 8); a capture of 780,000 bytes is
  saved and one of 790,000 bytes ends exit 8 under the 1 MiB answer bound. A second enable in the same session finds the
  service on and writes nothing; one disable clears the owed undo.

## Still open

- An `enabled` element whose text is `false` only after its child elements are joined (`<enabled><x>false</x></enabled>`,
  `fa<x/>lse`), or followed by an extra element, is taken as off and the enable is sent; the undo is still entered,
  printed and owed.
- A run folder under a symbolic link into a git work tree is not refused: the git check reads the path as written. A
  capture taken there lands inside the work tree (untracked, not committed).
- `panel.png` is the device's bytes, decoded and not scrubbed: a capture that carried the password's bytes would hold
  them in the run folder.
- Whether the M577 answers `IsServiceEnabled`, `EnableService`, `GetScreenCapture` and `DisableService` as HP's text says,
  and how large its capture is: not measured. The run on the device is a separate step after this lands.
- Steps 3 and 4 of the first-run list (certificate import and delete, a button's register and unregister) and the echo
  verb are not built.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the one name admitted by name; an enable
on a service already on writes nothing and exits 0; the capture as a read saved in the run folder under the unchanged
answer bound; no read before a disable; the adapter stub's service on by default; the four counts; no default change of
the addressing version; no local CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
