# FOR RECORDS: OXPd 2 CI guards follow-up (rule R6) and the Linux image digest pin (kit B1916, WP0.3 follow-up), gate G1 round 1, reader B1919

Not repository text. For the next OXPd records pass (backlog, runbook, ticket OXPD2-25, owed items); nothing here was
written into the project. No person is named.

## What lands

- ONE commit `81b5f3ef` on main `4e8828ee`, three files: `build/repo_rules.py` (25 added, 6 removed),
  `build/tests/test_repo_rules.py` (7 added, 1 removed), `packaging/linux/Dockerfile` (2 added, 1 removed). No C#,
  workflow, package, lock or project file. Unit tests 111, floor 111 (unchanged); RULES 500 files (unchanged); C#
  totals 1579 on both legs (unchanged).
- Rule R6 gains two refusals outside a block scalar: `${{` before the line's first colon and blank (an expression in a
  key; raw line), and a quoted scalar opening where no value starts (after the expression removal). They close the two
  open-quote limits that pull request 16's squash message carried and the ticket's hidden flow-mapping cell.
- `packaging/linux/Dockerfile` names `mcr.microsoft.com/dotnet/aspnet:10.0@sha256:12b1135f5f8b3c0a214f2a680ff2033dff4f684f445d6c697d9524ceeb303586`.
  The gate read three hosted linux logs by GET: the tag builds of main `4e8828ee` (job 137164654716) and of the
  b1912 head (job 137158213066) resolved the tag to this digest, and the head's pinned build (job 137169546416)
  pulled the same seven base sha256 values as main's tag build. Owed item 7 closes when this lands.

## From this gate

1. **Named costs re-measured (green `[1]`, old rule `[]`, by `check_spellings` on single lines):** H5 `b${{ x }}: c`;
   H6 `- "a ${{ x }}: b"`; H7 `run: echo "hello"`, `if: github.event_name == 'push'`.
2. **Costs the kit did not list (same instrument):** `- echo "hi"` and `args: --flag 'x'` (H7's family);
   `name: &n "rules"` and `name: !!str 'rules'` (an anchor or a tag before a quoted value); and a comment line holding
   an expression before its first colon and blank, `# ci-${{ github.ref }}: one group per ref` (refusal (iii) reads the
   raw line, comment included). The comment case was also run end to end: planted above line 15 of a copy of today's
   `ci.yml`, the new rule printed `RULES: R6 .github/workflows/ci.yml:15` (rc 1), the old rule `RULES: clean (500
   files)`. A comment is never YAML, so this one is a pure false refusal; low cost (rewording the comment clears it).
3. **H8 (a block indicator after an expression, `name: ${{ x }} |`) stays open, and its reach is small (measured with
   libyaml 0.2.1 through `/usr/bin/ruby`):** libyaml accepts the line only where the next line is not indented more
   than the key, and there the reader's phantom block ends at once (rule `[]`, nothing skipped); a more indented next
   line is a YAML error. R3 and R4 read every line regardless of blocks (`repo_rules.py:382-387`), so a phantom block
   hides lines from R6's spellings only. Backlog: refuse `|` or `>` read after the expression removal when the raw line
   has an expression before it, or name it as a limit for good.
4. **Today's `ci.yml`:** 0 findings under both rules; it holds one `${{` (line 15, after the colon), no `if:` line,
   and every multi-word quoted command sits in a `run: |` block, so the costs fall on spellings it does not use.
5. **The pin's upkeep:** nothing in the repository moves the digest (no `.github/dependabot.yml`; `.github/` holds
   only `workflows/ci.yml`). A patch image of the `10.0` tag reaches the build only by a change of this line. Backlog:
   a records line naming who moves it and when, or a later lane that reads the newest digest from a hosted log.
6. **The root README's line 29** still names the tag only (true; Q5 of the kit, unchanged).
7. **Instrument note:** the seat's STATUS first line still reads `PROGRESS B1916: PENDING` while its last line is
   `READY B1916: 81b5f3ef...` (a records note, not a defect of the change).
