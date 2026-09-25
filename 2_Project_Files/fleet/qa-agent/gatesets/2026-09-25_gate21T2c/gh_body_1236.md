#1236 KS-1110 READYAML: both k6 unit tests parse scenarios.yml through readYaml()
head 4296ba6d090c212d0849f488f882d00a2985245e

## BLUF

Two k6 unit tests parsed `config/scenarios.yml` with js-yaml directly, bypassing `readYaml()`. A malformed file would therefore surface as a raw parser error in the tests while the product path reports it through `readYaml`'s own handling - the tests and the product disagreed about what reading that file means. Both now go through `readYaml()`.

Two commits, one per item: **item A** `tests/unit/config/sheddingCeiling.test.ts`, **item B** `tests/unit/package_scripts.test.ts`. One ticket, one test pass, so one PR.

## This PR NARROWS the ticket

Items A and B only. **Item C of the ticket remains open.**

## Test Evidence

**Touched** - `systemTest/performance/tests/unit/config/sheddingCeiling.test.ts` (numstat **14/3**, 129 -> 140 lines) and `systemTest/performance/tests/unit/package_scripts.test.ts` (numstat **13/3**, 71 -> 81). Both numstats equal their checkers'. Both applied strict, as their recorded options require.

**Ran, by me, at this head** - runner read from `package.json`: `npm test` -> `test:unit` -> `vitest run --config vitest.unit.config.ts`.
- `systemTest/performance` **bare 1085/1085 over 63 files, rc 0** at develop in a clean worktree with that package's own deps, **patched 1089/1089 over 63 files, rc 0**. 1089 = 1085 + 2 + 2, each item's own +2.
- Red-first per the checkers: item A fails 1 of 6 at the tip and passes 6 of 6 after; item B fails 1 of 11 and passes 11 of 11.

**A correction to the held READYs, measured rather than inherited**
Both READYs record `baseline: total=1085 failed=1 | after: total=1087 failed=1`. **On a clean worktree at develop the baseline is 1085 passed / 0 failed, rc 0 - the `failed=1` does not reproduce.** It came from the checker's run under multi-seat load, so it is a property of that run and not of this suite. The totals reconcile exactly; only the failure count was wrong. This PR therefore claims no pre-existing failure in that suite.

**NOT run**
- **The pre-push hook ran no `Blockchain/Dev` leg for this push**, because it filters by path and this change touches only `systemTest/performance`: 0 leg headers, an 839-byte hook log against 71 KB for a sibling push. So there is **no `28 passed / 0 failed` to claim here** - the suite did not execute. What did run: the format gate, `systemTest/performance - format:check OK`. Push PROTOCOL-CLEAN.
- No k6 scenario was executed. The sixteen `test:*` scripts in that package drive real load runs against a live stack; none was used, and none is needed for a yaml-reading change.
- No malformed `scenarios.yml` was fed through either test to watch `readYaml` reject it; the change is that the call now goes through `readYaml`, and the cells pin that, not its error text.

**Migrations + config** - none.

Refs KS-1110


🤖 Generated with [Claude Code](https://claude.com/claude-code)

