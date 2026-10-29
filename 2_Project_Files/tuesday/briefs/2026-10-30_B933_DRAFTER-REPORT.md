STARTABLE: YES (after your stamp; filler lane, Python only, one path, no port, no other lane names the path). One collision you must rule on at stamp: item 2 turns two existing GREEN harmless-row entries red (Q-1).

# B933 drafter report (Opus, 2026-10-30 about 10:20 to 10:50 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B933_SEAT-H64_hpsmpoc-403-404-infra-test-extensions.md` (149 lines; 8 four-underscore lines = 7 slots + the last line; at-sign slot pattern 0; non-ASCII lines 0, by `LC_ALL=C grep -c -E '[^ -~]'`). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, Jira GETs through a scratch reader that loads `.tools/b649/jira.py` by path, a tarball extract and `bicep build` in my scratchpad, python probes of single functions on scratch copies. No worktree, no ref, no push, no Jira write, no message, no `cd`. Nothing written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H64` (Sonnet `claude-sonnet-5-5`, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes) creates `b933/hpsmpoc-403-404-infra-test-extensions` off main `e21d8044` with TWO commits on `infra/tests/test_security_baseline.py`: commit 1 builds HPSMPOC-403 items 2-6 (environment pinned in the suffix's scoped uniqueString; storage/sql/openai name bindings via a new additive `NAME_CALL_BINDINGS`; `if` in the suffix evaluated per environment; fullwidth digit three added to the integer row's refused list; an IndexError row for the vault-name read) and records item 1 DECLINED; commit 2 rewrites HPSMPOC-404's three comments with a tokenize+AST proof of no code byte. Red-first, mutants, whole infra under 3.14/3.9, stop at READY FOR QA; Tuesday opens and lands the PR.

## Facts re-measured (instrument; control)
- Main `e21d80442980fb61ad9fb11aaf393c0b20c0ad2d` (`commits/main`; control `commits?sha=main&per_page=3` lists e21d8044, 94274a75, 9659148c). Open PRs 0. `matching-refs/heads/b93` = only `b93/gate-b94-notes` (no b933). Ruleset `deletion non_fast_forward code_scanning required_status_checks`. Check-runs on e21d8044: 19 (18 success, 1 skipped).
- Test file blob `79e6b3bd...` = `git hash-object` of the raw bytes (control `printf abc` -> `f2ba8f84...`); 2614 lines; sha256 `cbe999b9...`; 123 `def test_`; 8 non-ASCII lines. It equals PR #243's final head file (the B920 drafter's predicted blob).
- **Item 1 decline verified at source:** `infra/bicepconfig.json:16` `"prefer-interpolation": { "level": "error" }`; a scratch `main.bicep` with line 68 as `keyVault: concat('kv-', prefix, '-', suffix)` -> `bicep build` rc 1, `(68,13) : Error prefer-interpolation`, no output file; unedited copy in the same folder rc 0. `validate.sh:14-15` builds and lints main.bicep. B919-9 is TRUE.
- Compiled bindings: `storage.name` = `[variables('names').storage]`, `sql.serverName` = `[variables('names').sqlServer]`, `openai.name` = `[variables('names').openAi]`.
- Probes (functions loaded from scratch copies, never the suite): the `if` plant reads `''` from `suffix_problem` today, its condition `equals('a','b')` evaluates False; fullwidth-range and NFKC widening mutants both still refuse U+0663 but PARSE U+FF13 (so the new entry kills both B922-2 survivors); `arm_parse` raises IndexError for `format('kv-{0}', variables('prefix')`, `format(`, `format('a',`; with IndexError dropped from line 1131 the vault-name read RAISES (m39 visible); the two no-environment suffixes at lines 1839-1840 read `''` today.
- Ports: `lsof -nP -iTCP:9700-9999 -sTCP:LISTEN` 0 lines. Panes `%0 tuesday`, `%1 fleet-monitor`. Word scan for `H64` in today's non-pre SEAT kits 0 (control `H58` 3). Load 3.27 at 10:27.
- Model rows: L6:85, C2:92, G2:109, G3:110, G-cap:111; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus.

## D-decisions (mine, in the kit)
- D-1: Item 1 declined, and the seat re-runs the lint check itself and writes the reason in STATUS and the commit-1 body.
- D-2: Item 2 is pinned on the SAME uniqueString call that takes resourceGroup().id, checked AFTER the existing scope check with a NEW message, so all nine entries of the existing RED suffix row keep their exact message. It forces the one named exception: the two GREEN entries at lines 1839-1840 are replaced by the same wrappers WITH the environment, and the old values asserted RED in a new row (Q-1).
- D-3: Item 3 additive: new `NAME_CALL_BINDINGS` after `PREFIX_CALL_BINDINGS`; only the loop line 1180 changes; `MODULE_CALL_BINDINGS` and the row at 1687 that pins it stay byte-equal. Other calls' name params (appservice, rbac) and what `names.storage/sqlServer/openAi` place are residuals.
- D-4: Item 4 confined to `if` nodes in the suffix walk: condition evaluated per environment by the file's own `arm_value`; decided -> the picked branch must be scoped; undecidable -> both. The reader functions (`arm_parse`, `arm_value`, `evaluated`) are NOT changed. The test plant carries the environment so only item 4 can catch it.
- D-5: Item 5 is one loop entry, no `assertIsNone` line (B922-1: it cannot fail alone). Escape written as six ASCII characters; two programmatic checks because the Write tool decodes backslash-u (I hit-proofed this kit with a placeholder and a python write).
- D-6: Item 6 is a row; line 1131 is not changed.
- D-7: Two commits, 404 AFTER 403, so the comments describe the code as it stands (including the new calls and the evaluated `if`); the `suffix_problem` docstring is updated in commit 1 because commit 1 changes that function. Commit 2's proof: token streams equal minus comments except exactly one docstring STRING token, plus an AST equality with that docstring neutralised.

## Q-questions for Tuesday (each with a default)
- Q-1: Accept the named exception of Property H (d): two GREEN entries of `test_harmless_edits_of_the_suffix...` (lines 1839-1840) replaced by environment-holding variants, old values asserted RED in a new row? Default **YES** (item 2 cannot be built otherwise; the B916 stamp ruled the same shape YES for its Q-1). If NO, item 2 must be DECLINED instead, and the kit's E2 rows drop out.
- Q-2: May the seat copy `run_infra.sh`, `repeat20.sh`, `modrun.py` read-only from `.tools/b916/` (only `K=` and worktree name changed, diff printed)? Default **YES** (the B920 stamp allowed the same).
- Q-3: Class and round for the tier-2 gate. PR #243 used both rounds of class B (B919 NO GO, B922 GO WITH FINDINGS). Default: **a new PR on the same class starts at round 1 of 2, NO GO 0 of 2** (B916's kit counted rounds per PR); if you count per class across PRs, the next NO GO is the cap and needs the product owner.
- Q-4: Two commits in one PR (403 then 404) rather than two PRs? Default **YES** (one path, one gate; the sweep's "G3 for -404" means no separate gate; land with explicit `--subject`/`--body-file` carrying both keys, B922 noted a two-commit squash title is UNMEASURED).
- Suggested times: target READY 150 min, HARD STOP 210 min after Step 0.

## Sweep pointers found WRONG or loose
- "above `evaluated` line 716": the stale block that describes `evaluated` is lines 592-597, above `ARM_TOKEN` (598). The ticket's wording "the block above evaluated" matches B919-4's "head lines 590-597".
- "the integer row at line 1814": 1814 is the def line; the refused-list loop to edit is line 1829.
- The sweep seed omits that item 2 flips two existing GREEN entries (lines 1839-1840).
- Not in the sweep: two MORE stale comments that 404 does not name (`RULES` trailing comment line 1210 and the row-section comment line 1598 each still say "rbac, keyvault and appservice"). The kit holds them byte-equal and reports them FOR TUESDAY; a follow-up ticket, or widen 404 at stamp if you want them in commit 2.

## UNMEASURED
Any row's pass/fail in the real file; the whole-infra count after the change (base 301 RELAYED from B922); real-file mutants; whether the E4 walk leaves every existing suffix message equal (the seat's corpus check); the CI runner's Python; the two-commit squash title.

## Outside-the-fences disclosure
None breached. I read only `.tools/b649/jira.py` and `.tools/b884/read.py` headers (named helpers). Scratch: tarball extract, compiled JSON, lint copies, probe scripts and mutant copies under my session scratchpad `drafters/b933/` only.
