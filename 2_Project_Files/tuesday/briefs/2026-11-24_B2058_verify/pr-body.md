The fix of three limits of the OXPd 1.x Test service change (#47), built against stubs only, before the first run of
the Test service on a device. One commit, `105b3465`, on `main` `89a10a1b` (behind 0, ahead 1). Nine files changed, none
added, all under `src/Datasec.Suite.Adapters.Oxpd1/`, `src/Datasec.Suite.Lab/Commands/Oxpd1/` and the two matching test
folders. No package, no lock file, no project file, no `Datasec.Suite.slnx` line, no workflow, no file under
`contracts/`.

## Why

- The read before an enable took the joined text of `enabled`, so some answers outside HP's schema (a `false` inside a
  child element, split by one, with an element beside it, or with `xsi:nil`) were taken as off and one `EnableService`
  was sent.
- The run folder rule read the path as written only, so a run folder reached through a symbolic link into a git work
  tree was accepted and a panel capture was written inside the tree.
- `panel.png` is the device's decoded bytes: a capture carrying the password's bytes would have been saved with them.

## What changed

- **The client.** The `IsServiceEnabled` catalogue row gains `TextOnly`: its answer is read only when the response holds
  that one element, with no child element and no attribute but a namespace declaration; any other shape ends
  `MalformedAnswer`. The lab's read before an enable then writes nothing and ends exit 8 (its landed "did not answer"
  line). `GetScreenCapture`'s row is unchanged.
- **The lab.** `RunFolderRule` reads the path as written first (the landed message unchanged) and, when that finds no
  `.git`, again with each symbolic link among the existing folders replaced by its final target (at most 40; a link
  that cannot be resolved is kept as written); it guards `oxpd1 read`, `oxpd1 write` and `oxpd1 lab-cert`.
  `ScreenCapture.Save` takes the run's password and saves nothing when the decoded bytes hold its UTF-8 bytes (exit 8).
- **Text.** The adapter README's `enabled` sentence; the lab command README's capture, password and enable bullets, its
  run folder section and its Limits.

## What proves it

- Red first: 12 cases fail by assertion on the landed code (adapter `Total: 55, Failed: 4`; lab `Total: 229, Failed: 8`).
  Green: 2171 / 0 / 2167 / 4 locally; the branch's push run 45366993513: linux 2167 succeeded, windows 2150 succeeded,
  rules 659 files, secret scan clean.
- 10 mutants, each red on exactly its cells, none surviving (the row flag off; a sibling, a child element or an attribute
  taken; a namespace declaration or CDATA refused; the links not resolved or only the last one; a capture holding the
  password saved; one holding all but its last character refused).
- Against a stub on 127.0.0.1: the four shapes above write nothing (exit 8); a run folder through a link into a work
  tree, through a link to a link, through two links, through a relative link or above the tree's root is refused (exit
  9); a link loop, a dangling link or a folder without permission above the run folder ends exit 5 with nothing made; a
  capture holding the password's UTF-8 bytes anywhere in 500,000 bytes is not saved.

## Still open

- Text directly beside `enabled` in the response, or an attribute on the response element itself, is still read (HP's
  schema refuses both); the enable is then sent, its undo entered, printed and owed.
- A relative link whose target walks `..` through another link is resolved by its text, not as the system resolves it:
  a run folder behind such a link can still land inside a work tree (untracked, not committed).
- The capture check looks for the password's UTF-8 bytes only (not its Basic form or UTF-16), and the client's record
  still holds the answer's base64 text. A very short password can match an image by chance and refuse the capture.
- Whether the M577 answers `IsServiceEnabled` in HP's shape, and whether any device's capture holds the password: not
  measured. The run on the device is a separate step after this lands.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the client closes the read by a flag on
one row; refuse the capture rather than scrub it; the path as written first, then the real path; the link cell returns
at once on Windows; the record's base64 a named limit; no cells for the earlier change's other limits; no local CodeQL).
No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
