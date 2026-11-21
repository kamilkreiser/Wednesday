## What this changes

`build/repo_rules.py` rule R5 has two halves. The extension half (no tracked file is a binary by extension) runs
everywhere and is unchanged. The hash half (no tracked file's sha256 equals a file of the supplied source) runs only
where the supplied-source folder exists, which is a local run, never the hosted `rules` job. Since pull request 6 the
repository holds HP's 37 specification inputs under `contracts/oxpd2/hp/`, so a local run of the hash half reported
each of them. This change does two things.

- **The 37 inputs, by path and sha256 together.** The hash half now skips a tracked file only when its exact path and
  its exact sha256 are one well-formed line of the tracked list `contracts/oxpd2/inputs.sha256`
  (`<64 lower-case hex>  hp/<path>`, the path read below `contracts/oxpd2/`). A line of any other shape, a path listed
  twice, or a list that is not tracked exempts nothing. A listed file whose bytes changed, listed bytes at an unlisted
  path, and a listed path outside `hp/` are all still reported. The extension half exempts nothing, so a listed
  `.pem` or `.dll` still fires. The run prints how many files it exempted.
- **Key folders are never opened.** The hash half removes every folder named `certificates`, `certs`, `cert`, `keys`
  or `key` (in any case) from the walk before it descends, so their contents are never listed, and it skips every
  file named `*.key`, `*.pem`, `*.pfx`, `*.p12`, `*.jks` or `*.keystore` by its name before any stat or open. A
  supplied root that is itself such a folder, by its own name or through a link, is not walked. The run prints how
  many folders and files it skipped. The supplied SDK holds a development key folder; before this change a local run
  of the hash half read it.

## The follow-up commit

The second commit closes points raised by the first independent check of this branch:

- The supplied root is resolved through links (`os.path.realpath`) before the key-folder check, so a root given as a
  link under another name is no longer walked.
- New subtests inside the existing cells: a key-folder root given with a trailing separator, with a trailing `/.`, and
  as a link; a recorder of `os.stat` and `os.lstat` that fails if a key file is stat-ed (with its own positive
  control); and a listed path under `contracts/oxpd2/` but outside `hp/`, which must still be reported.
- A test variable was renamed from `secret_text` to `folder_text`. CodeQL's `py/clear-text-storage-sensitive-data`
  read the name as sensitive, though the value is synthetic. The local CodeQL CLI 2.27.4, with both Python suites the
  repository's default setup uses, reads 0 results on this head (3 in each suite on the first commit).
- The module docstring now describes the list by what it is.

## The floor

`FLOOR` in `.github/workflows/ci.yml` moves from 53 to 60 (the first commit adds seven test cells; the follow-up adds
subtests only). After this lands, every hosted `rules` job of this repository prints `Ran 60 tests` and
`UNIT-TEST FLOOR: ran 60, floor 60`.

## Measured

- `build/tests`: `Ran 60 tests`, `OK`, on the head and on its merge with the current main.
- The hash half over the real supplied folder, run locally by this head's own program: 35210 files hashed, 4 key
  folders and 0 key files skipped, 37 tracked files exempted (the list has 37 lines), `RULES: clean`. A planted copy
  of a listed input at another path and a swap of two listed inputs give three `RULES: R5` lines and 35 exempted.
- The hosted run of the head: the four jobs succeed, both build legs total 894 with 0 failed, and the `rules` job
  prints `Ran 60 tests`, `UNIT-TEST FLOOR: ran 60, floor 60` and `RULES: clean (291 files)`.

## Limits, said plainly

- **The exemption is exactly as wide as the list, and the list is open.** One commit that adds a supplied file under
  `contracts/oxpd2/hp/` together with its own line in `inputs.sha256` passes R5. Nothing pins the count (37) or the
  list's own sha256. Any change to `contracts/oxpd2/inputs.sha256` needs a reader.
- **What the prune does not see.** Because the hash half never reads a key folder, a tracked copy of a file from one,
  under any name, is not caught by the hash half: the extension half, the secret scan and a reader of the change are
  the controls there. Folders with other names (for example `ssl`, `private`, `secrets`) and files such as `*.crt` or
  `id_rsa` are walked and hashed. A process running as root is not stopped by file modes. On a filesystem without
  directory-entry types the walk itself may stat a key file. The list is read from the working tree, not the index.
- **Only the root's own last name is checked.** After links are resolved, only the last name of the supplied root is
  compared with the key-folder names: a root below a key folder (for example `.../certificates/sub`), or a link to
  one, is walked, and so is a root named like a key folder that is a link to a folder with another name. The root is
  an operator argument; the default is `Source_Documents`.
- **The hash half runs locally only.** The hosted `rules` job has no supplied-source folder and prints
  `R5 hash half NOT RUN`.
- **The key-folder cell is POSIX-shaped.** It uses file mode 000, symbolic links, and `os.path` functions that call
  `os.stat`; it runs on the Linux `rules` job.

## Records still owed

`README.md` line 71 states R5 without the exemption, and the project's `CLAUDE.md` (lines 50-51) and
`CLARIFICATIONS.md` carry no entry for the 37-file exception. They are a separate records change.

No C# file, project file, lock file, package, HP input, fingerprint list or solution-file line changes, and no
workflow line other than `FLOOR`. Every choice in this change was made inside the build. Nothing is deployed and
nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
