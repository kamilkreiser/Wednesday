The follow-up of OXPD2-25 (C-67: "Merge now, the two shapes ticketed as known limits", pull request 16) and owed item 7
(the Linux image base named by tag only). One commit `81b5f3ef` on `main` `4e8828ee`, three files:
`build/repo_rules.py`, `build/tests/test_repo_rules.py`, `packaging/linux/Dockerfile`.

## Why

Rule R6 refuses a line outside a block scalar that leaves a quoted value open at its end. Two spellings left a value
open in YAML while R6's own quote reading saw the line as closed, so the lines below were read as YAML and a
continuation ending in a colon and a bar opened a phantom block that hid the rest of a job from R6:

- a quote opened behind an expression in a plain key (`name${{: "a }}`): the expression removal took the quote away;
- a quote opened after a quote inside a plain key (`my "key: "a`): the quote reading paired the two quotes.

The ticket's third cell, a flow mapping hidden inside an expression in a key (`env${{: {x: {permissions: write-all}}`),
had the same cause.

## What changed

- `build/repo_rules.py`, rule R6, two refusals for a line outside a block scalar: (a) `${{` before the line's first
  colon and blank (an expression in a key), read on the raw line; (b) a quoted scalar that opens anywhere but at the
  line's first non-blank, after a sequence dash and a blank, or after a colon and a blank (a quote inside a plain
  key), read after the expression removal as a third value of `yaml_scan`. (a) closes the first shape and the hidden
  flow mapping; (b) closes the second. The module docstring and `check_spellings`'s docstring say so.
- `build/tests/test_repo_rules.py`: seven rows in two existing planted controls (each shape in double and single
  quotes with two quoted keys hidden below it, the hidden flow mapping, and two quiet lines). No new test case: 111
  tests, `FLOOR=111`, `ci.yml` unchanged. The five new red rows fail against the old rule by their own assertion; four
  mutants of the new rule are each caught.
- `packaging/linux/Dockerfile`: `FROM mcr.microsoft.com/dotnet/aspnet:10.0@sha256:12b1135f5f8b3c0a214f2a680ff2033dff4f684f445d6c697d9524ceeb303586`,
  the digest the hosted linux job's builder resolved for the `10.0` tag (read from hosted logs, no registry call; the
  tag build of `main` `4e8828ee` resolved the same digest and pulled the same base layers). One comment line says
  where it comes from.

## The costs, stated plainly

Outside a block scalar, R6 now also refuses YAML that is valid and that a person may write:

- a plain value with a quoted word after its first word: `run: echo "hello"`, `if: github.event_name == 'push'`,
  `args: --flag 'x'`, `- echo "hi"`;
- a key closed after an expression: `b${{ x }}: c`;
- a quoted value holding an expression and then a colon and a blank: `- "a ${{ x }}: b"`;
- a quoted value behind an anchor or a tag: `name: &n "rules"`, `name: !!str 'rules'`;
- a comment line holding an expression before its first colon and blank: `# ci-${{ github.ref }}: one group per ref`.

Such a value is written inside `${{ }}` or as a block scalar (as every command of today's `ci.yml` already is; it has
no `if:` line), and such a comment is reworded. Every edit of `ci.yml` is already read by a person through the
whole-file fingerprint. Today's workflow gives 0 findings under the old and the new rule.

The pin's cost: a later patch image of the `10.0` tag no longer reaches the build until this line moves its digest.
Nothing in the repository moves it automatically.

## Still open

- A block indicator after an expression (`name: ${{ x }} |`) is still not refused: the line reader opens a block that
  YAML does not. The lines it then skips are judged for the shell words only. libyaml accepts such a line only when the
  next line is not indented more than the key, and there the reader's block ends at once; a more indented next line is
  a YAML error. Measured, not proved for every parser.
- Anchors, aliases, tags beyond the case above, several documents, and a scanner command split over lines stay outside
  what the line reader judges (the module docstring's limits). Whether GitHub's own parser accepts the five red shapes
  is not measured.

## Who decides

The lane, its cut and every choice inside it (the two refusals and not the raw-line quote reading, the named costs
accepted, the digest pin) are the coordinator's, made as coordinator.

111 tests, floor 111; RULES 500 files; C# totals 1579 on both legs (skipped 4 on linux, 19 on windows), unchanged
(branch run 45009852222). Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
