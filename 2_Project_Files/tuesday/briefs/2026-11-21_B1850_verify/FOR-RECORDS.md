# FOR RECORDS: gate B1850 (OXPd 2, lane R5 fix round, head 2229f68 on main 0804860)

What a records pass should file once the head lands. The gate wrote none of it into the project.

## Closed by commit 2229f68 (once landed)

- **F1 of gate B1843** (CodeQL `py/clear-text-storage-sensitive-data`, 3 results, the name `secret_text`): CLOSED.
  Local CodeQL CLI 2.27.4, both suites of the default setup (`python-code-scanning`, `python-security-extended`):
  2229f68b 0 + 0; R1 28d2852d 3 + 3 at `build/tests/test_repo_rules.py:71`, `:366`, `:371` (control fired); main
  0804860b 0 + 0; the merge tree 602ed3b6 0 + 0. `pr_codeql_check.sh` base 0804860b head 2229f68b: KEPT 0, NEW 0,
  rc 0 PASS. The hosted `Analyze (python)` on `refs/pull/N/head` remains the authority at landing.
- **F2 of gate B1843** (mutants g6, g7, g8 survived): CLOSED. The gate's own re-made g6 (root name as given), g7
  (islink/isfile before the key-file skip), g8 (no `hp/` prefix in the line pattern): each RED by assertion on the
  head's tests, each GREEN on R1's tests. Two more of the gate's own on the realpath line (n1 `abspath`, n2
  `realpath` of the basename) and two on the stat recorder (n3 `lexists` before the skip, n4 `os.stat` size before
  the skip): each RED by assertion (n3, n4: `stat of a key file`).
- **F4 of gate B1843** (a root given as a link to a key folder was walked): CLOSED by `os.path.realpath`. The link
  subtest is RED against R1's code (R1 tree plus the head's test file: `FAILED (failures=1)`, the one FAIL
  `[link under another name]`, 0 errors) and GREEN after.
- **F5 of gate B1843** (docstring "kept on the owner's agreement"): CLOSED. `owner|agree|decid|ruling|approv|consent`
  counts 0 in both changed files at the head (R1: `build/repo_rules.py:24`).

## Records points of this gate (none blocks the merge)

- **G1 (Minor, limit).** `realpath` narrows one case R1 covered: a supplied root NAMED like a key folder that is a
  link to a folder with another name is now walked (synthetic: head hashed 1, R1 skipped 1). The docstring's "by its
  name or through a link" reads wider than the code. A one-line widening (check the name given AND the resolved
  name, or every component of the resolved path, which also closes H18) belongs to a later build lane if wanted.
  Operator argument only; the default root is `Source_Documents`.
- **G2 (records, limit H18, now MEASURED).** A root below a key folder (`.../certificates/sub`) and a link to such a
  sub-folder are walked (synthetic run on the head: hashed 1 each). The kit named it DERIVED; the gate measured it.
- **G3 (records).** K1's stat recorder and its positive control depend on `os.path.islink`/`isfile` calling
  `os.stat`/`os.lstat`. On CPython 3.12+ for Windows those are native fast paths (DERIVED, not run), and mode 000 and
  `os.symlink` behave differently there: the cell would fail loudly on Windows, never pass silently. The hosted rules
  job is Linux only (`ubuntu-26.04` image; its Python version is not printed in the log).
- **G4 (records, landing forms).** The default code-scanning setup stores a pull request's analyses on
  `refs/pull/N/head` (pull request 7: three analyses at 9d496955 there, none on `refs/pull/7/merge`), and an alert
  read on `refs/pull/N/merge` prints 0 with nothing analysed. The landing form of gate B1846 read the merge ref. This
  gate's landing reads the analyses on the head ref first (positive control) and then the alerts there. Future
  landing forms should do the same.

## Still owed from gate B1843 (unchanged by this commit)

- **F3** (design, records): the exemption is as wide as the list, and the list is open; one commit can add a supplied
  file under `contracts/oxpd2/hp/` with its own line. Any diff touching `contracts/oxpd2/inputs.sha256` needs a
  reader; optionally pin the count (37) or the list's sha256 (`6760314d...`), or restrict listed paths to `.json`.
- **F6** (a) a renamed copy of a key-folder file escapes the hash half; (b) mode 000 does not stop root; (c) folder
  names outside the five (`ssl`, `private`, `secrets`) and files such as `*.crt`, `id_rsa` are walked and hashed;
  (d) a filesystem without `d_type`; (e) the list is read from the work tree, not the index.
- **F7**: `README.md:71` states R5 without the exemption; `<project>/CLAUDE.md:50-51` and `CLARIFICATIONS.md` carry
  no entry for the 37-file exception.

## The seat's deviations (STATUS of kit B1844), as ruled

1. A `builtin cd` inside a discarded subshell during the tool-hash step: ACCEPTED as a shell-rule slip with no
   effect; the gate re-hashed the ten tools itself (ten of ten equal to the kit's list).
2. Reads in the seat's own clone without `--no-optional-locks`: ACCEPTED, no effect (no other process shares that
   clone).
3. One read-only check beyond the kit (`grep -i download` over the CLI logs): ACCEPTED; it adds evidence and changes
   nothing.

## After the landing

Every later hosted rules job prints `Ran 60 tests` and `UNIT-TEST FLOOR: ran 60, floor 60`; kits and landing forms
that still require 53 on a run built on the new main must say 60.
