Follow-ups to the CI guards of work package WP0.3. There are seven commits on `5bb1418c`, landed as one squash: five first commits, a fix commit, and a last commit that adds three plain refusals. Only Python files under `build/`, the workflow `.github/workflows/ci.yml` and `README.md` change. No product code, package, solution or lock file changes. Nothing is deployed and nothing is sent: the workflow builds, tests and scans, and has no deploy step.

## What it adds (the first five commits)

- **README:** says that on a pull request the checkout also fetches that pull request's merge commit, and that the second secret scan reads it.
- **Repository rules R6 to R8** (`build/repo_rules.py`), run by the `rules` job:
  - R6 keeps every file under `.github/workflows/` in spellings a line reader can follow.
  - R7 refuses a NUL byte in any tracked file (a binary under any name).
  - R8 refuses the `filter` attribute in any tracked `.gitattributes` (Git LFS would keep only a pointer).
  - The whole workflow file is now held to its reviewed text by a fingerprint, beside the fingerprints of the `secret-scan` and `rules` jobs.
- **Squash message scan** (`build/squash_scan.py`): scans the subject and body of a squash merge BEFORE the merge, through the workflow's own export function and scanner options, after a planted control.
  - Why: a message the scanner flags on `main` would keep `secret-scan` red on every branch, and `main` cannot be rewritten.
- **Second secret scan hardened:**
  - every copy's length is checked against its object;
  - the listing is counted by the lines read;
  - every object a ref of the checkout reaches must be among the listed objects.
- **Release guard** (`build/release_guard.py`):
  - A release mode (`--release`) that refuses an untracked or empty deny-list. It ends 2 today: the development CA's fingerprint is still owed, and neither build leg calls it.
  - G1 finds the library name inside any binary.
  - G2 finds the development CA's name anywhere in a path, and two more PEM labels and UTF-16 text.
  - G3 finds backslash member names and archive formats the guard does not open, by their magic bytes.

## The fix commit

- R6:
  - a comment never starts a block scalar;
  - flow sequences are refused;
  - exported shell functions (`BASH_FUNC_`) are refused.
- R8 splits a `.gitattributes` where git splits it: a line feed; a space, a tab or a carriage return.
- G2 finds the CA name anywhere in a path, and G3's archive magic is made exact and widened.
- A NUL byte or a failed step in a squash scan is exit 2.
- It adds tests for behaviour no case held before.

## The last commit: three refusals in place of three readings

- R6 refuses every byte of a file under `.github/workflows/` that is not printable ASCII (0x20 to 0x7E) or a line feed. That covers a tab, a carriage return, any other control byte, 0x7F and every non-ASCII character.
- R6 refuses a line outside a block scalar that leaves a quoted value open at its end (a quoted value spread over lines).
- R8 refuses a double quote in any `.gitattributes` line that is not a comment line (a quoted pattern).
- Today's workflow and both tracked `.gitattributes` files hold none of these. No fingerprint moves: only the number after `FLOOR=` changes, 108 to 111.

## Known limits (open; a follow-up ticket carries both)

The refusal of a quoted value spread over lines still misses two shapes. In each, the line that opens the quote is read as closed, so the lines after it are read as YAML, and a continuation line ending `: |` hides the rest of a job from R3, R4 and R6.

1. **An expression in a plain key in front of the quote:**
   ```
   env:
     a${{: "b }}
    x: |
     y"
   ```
   with a double or a single quote. The `${{ ... }}` removal runs before the quote reading and takes the opening quote with it.
2. **A quote inside a plain key:** `k "x: "a`, then `  b: |`, then `    "`, with a double or a single quote and their mixes. The quote inside the key is paired with the real opener of the value.

Both are parser-dependent:
- libyaml reads each file as valid and returns the hidden keys.
- Each shape needs a continuation line indented less than its mapping, which the YAML 1.2 specification forbids.
- Whether GitHub's own parser accepts either shape is not measured. For the first shape it probably does not: a `${{` that is not closed inside a key is likely refused as an expression that is not closed, though this is also unmeasured.

Both shapes already existed before these commits; neither is new here. **The backstop:** the whole workflow file is held by its fingerprint (`REVIEWED_WORKFLOW` in `build/tests/test_pipeline_controls.py`). So any edit to `ci.yml` turns the `rules` job red until a person reads the change and sets the new value in the same commit. `ci.yml` is also the only file allowed under `.github/workflows/`.

## Other limits, stated plainly

- **R6 reads lines, not YAML.**
  - Anchors, aliases, tags, several documents in one file, and a scanner command split over several lines are not judged; a reader of the change is the control there.
  - `key: ${{ x }} |` followed by deeper text is not refused. libyaml reads it as invalid YAML.
  - A `- |` block whose text sits two columns past the dash is judged as YAML. That fails closed: write such text one column deeper.
  - Shell text that builds `BASH_FUNC_` or `BASH_ENV` from pieces is not seen.
  - A doubled single quote in a quoted key (`'a''b':`) is not seen.
- **The byte refusal** binds files under `.github/workflows/` only. It does not bind another file under `.github/` (such as `dependabot.yml`), a local action's file (any local `uses:` is refused by R4 anyway), or a workflow file's name. A checkout with CRLF line ends fails closed.
- **The cost of the open-quote refusal:** a plain scalar that holds an unclosed quote where a token may start is refused. Write such text in a block (`run: |`).
- **The cost of the quote refusal in R8:** no quoted pattern can be written. Name a path with a space by a glob.
- **R8 judges tracked `.gitattributes` files only.** `.git/info/attributes`, `core.attributesFile`, `attr.tree` and `--attr-source` are not judged; nothing in the checkout or the workflow sets them. R8 also fires on a line git rejects whole, which is stricter than git.
- **G1** searches the name in ASCII and UTF-16LE only (not UTF-16BE or UTF-32), and only in a file that holds a NUL byte or starts `MZ`. A UTF-16 PEM block is found only when the text starts at an even offset.
- **G3** does not see formats with no magic bytes of their own: brotli, lzma-alone, an old tar without `ustar`. A ZIP with bytes in front is a finding, and its members are not opened.
- **The second secret scan does not see:**
  - text saved as UTF-16 or UTF-32;
  - compressed content;
  - a secret split over two lines;
  - branch and tag names;
  - an object only another kind of ref reaches;
  - a secret across a read cut in a large file that has blank lines, but none within 25 kB of that cut.
- **The squash scan:**
  - a body of blank lines only scans the subject alone;
  - a lone CR in a subject is stored verbatim;
  - a scanner path that cannot run is exit 2, with no test of that branch.

## Tests

- `build/tests`: 111 planted controls, and `FLOOR=111` in the workflow equals that count.
- On this branch: `RULES: clean (412 files)`.
- Merged with `main` at `e1e8043d`, measured locally: `RULES: clean (478 files)`, `Ran 111`.
- The .NET totals do not change: this branch adds no .NET test.
- Local CodeQL over `build/` and `.github/`: 0 results.
