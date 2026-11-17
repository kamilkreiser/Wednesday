GATE B1676: GO WITH FINDINGS @ c2ed21d on main 6c1aa32

Tier G2, one round, HPSM-POC lane H-T (B1675): one new vitest row pinning `startingOwner` for 99 letters + lone U+D83D + `b`. Own clone in `fleet/state/s287/g1676/head` (deploy key, repo-local core.sshCommand), node v24.21.0, no server, no port. Nothing pushed, no PR, no merge, no Jira, no alert dismissed, no deploy. Run about 22:10 to 22:15 AEDT 2026-11-17.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| 1 | Minor | I did not re-run main (whole vitest, main-side file count). The main columns (304 / 4339, file 136) are the builder's; my head numbers (304 / 4340, file 137) equal the builder's exactly, and 4340 minus 1 new row = 4339 is consistent. "Lost 0 / added 1 by program" was not re-derived by me. | Accept; hosted CI runs main and head. |
| 2 | Minor | Of the six assertions only the first (`toBe(letters(99) + "\uD83D")`) was proven to fail by my plant. `length`, `charCodeAt`, `endsWith` are implied by it (redundant, not vacuous: each can fail on its own if the first were loosened). `ownerOk(out)` (checkEntry accepts) is independent of startingOwner and was not red-tested by me; it can fail only if checkEntry's owner rule changes, which is its intent. | None. |
| 3 | Info | The row title is about 190 characters. It is truthful (see measured rows) but long. | None; the builder placed the expected value in the title on purpose. |
| 4 | Info | Result is stable across Node/ICU: the cut loop breaks on `cut.length + unit.length > 100` over grapheme segments; a lone surrogate has no grapheme-extend or join rule and is its own segment in every ICU version (measured here: segments 1:61 ... 1:d83d, 1:62, ICU 78.3 / Unicode 17). The `Intl.Segmenter`-absent fallback (code points) gives the same result: a lone surrogate iterates as one 1-unit code point. CI's Node is 24 (`ci.yml` lines 384, 463, 504; `web/.nvmrc` 24), same major as mine. | None. |
| 5 | Info | Commit message mentions "the product owner's 2026-11-17 default"; no ticket key, name, seat or brief id. Fine. | None. |

## Measured rows
| Check | Result |
|---|---|
| Refs | head c2ed21d684482f5566f13ed7d91363d37cd916ba (fetched by name), main 6c1aa32e2e8082ece9f00a7267c60d6e0473b8b5; `rev-list --count main..head` = 1 |
| Diff | numstat `10 0` on exactly `web/src/components/customer/remediation-store.test.ts`; additions only; one `it(` block inside the `startingOwner` describe, immediately before "starts empty when the first character alone..."; `git diff --stat` for remediation-store.ts = empty (byte-identical to main) |
| Text | diff non-ASCII bytes 0 (control with a planted e-acute reads 2); surrogate written as the 6-character escape `\uD83D`; 0 hits for .skip/.todo/.fails/snapshot/added import (control `.skip` reads 1); no new helper (uses existing `longer`, `letters`, `lone`, `ownerOk`); commit message 0 hits for ticket-key pattern, B1675, H180, seat, brief, tuesday, wednesday, kam; one trailer (Co-Authored-By: Claude Sonnet 5.5); author email = committer email (cmp equal) and equals the project checkout's configured email (cmp equal; value not printed) |
| Code read | remediation-store.ts:58-72: trim, return as-is if <= 100, else segment by grapheme and append while `cut.length + unit.length <= 100`, then trimEnd. Input trimmed length 101: 99 `a` (99), lone half (1) = 100, `b` would make 101 so the loop breaks. Result = 99 letters + U+D83D; trimEnd leaves it. Matches the pin. |
| Red-first, file alone at head | true: 137 passed (1 file). Planted `toBe(letters(99))`: 1 failed, 136 passed of 137, the failing test is the new row (AssertionError on the `toBe`). Restored: file byte-equal to the saved copy, `git status --porcelain` 0 |
| Segmentation probe (node 24.21.0, ICU 78.3) | segments of 99 `a` + U+D83D + `b`, last three: `1:61 1:d83d 1:62` |
| npm ci | rc 0 (install-scripts notice is text, no command run) |
| lint / typecheck | rc 0 / rc 0 |
| vitest whole at head | 304 files, 4340 passed, 0 failed (builder head 304 / 4340; builder main 304 / 4339, not re-measured by me) |
| e2e | 0 files under web/e2e mention `remediation-store`; build and e2e not needed, a new row in a unit test file changes nothing the app loads |
| Title vs assertions | title: lone high surrogate that is the 100th unit; 99 letters, lone half, b -> 100 units ending in the lone half, b not added, checkEntry accepts. Assertions: exact value, length 100, last unit 0xD83D, no trailing b, lone check true, ownerOk true. Each clause of the title is asserted. No assertion is vacuous (the first one failed under the plant). |

## Landing texts (builder's evidence folder checked; approved copies in this folder)
- pr-title.txt, squash-subject.txt (68 chars, equal), squash-body.txt: true against my runs (137 / 136 / 4340 / 4339, lint and typecheck rc 0), ASCII, one trailer, no names or keys. Copied unchanged.
- pr-body.md: ends with the required `🤖 Generated with [Claude Code](https://claude.com/claude-code)`; rest true. The infra figures (14 / 325 / validate.sh rc 0) are the builder's, not re-run by me. Copied unchanged.
- landing.txt: copied unchanged; `--match-head-commit c2ed21d684482f5566f13ed7d91363d37cd916ba` equals the head I reviewed. Its quoted landing rule is RELAYED by the builder, not checked by me.

## NOT RUN
- main-side vitest re-measurement (finding 1); infra scans and validate.sh; build; e2e; hosted CI and CodeQL (Tuesday's); a red test of the `ownerOk` line.
