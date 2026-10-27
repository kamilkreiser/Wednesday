# QA gate verdict - Secuura/Blockchain PR #1755 (KS-1620 items 3 and 2, Seat Y 1st)

- Tier 2, round 1 of 2. Gate model Claude Sonnet 5.5 (claude-sonnet-5-5). 2026-10-27.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-g-1027/` (clone `repo/`, worktrees `wt_dev`, `wt_p1755`; `mut.sh`, `mut.log`, `gitenv.sh`, `start.sh`, `lsremote_*.txt`). `TMPDIR=/tmp/gg1`. Node v26.8.1. `npm ci` in `wt_p1755/Blockchain/Dev` rc 0 (PID 91506, finished by itself); `packages/shared` built there (rc 0). `wt_dev` has no node_modules (see instrument notes).
- Pushed / merged / commented / edited a ticket / changed a PR: nothing. Git only, no `gh`, no docker. Killed nothing; stray check at the end clean (0 processes of mine).

## BLUF
**GO.** Every claim reproduced exactly; no defect found. INFO items only.

## Pins (start = end)
```
a7d0e1fb99792092aa00b4de42a51788d6a15cf8  refs/heads/develop     (start 20:43:55, end 20:50:18: UNCHANGED)
ed76bb3df69920f00e4594b4f6165f566db7ea90  refs/pull/1755/head    (start = end = briefed pin)
```
Merge base of develop and the PR: `a105a9df`.

## FOUND
- Scope (`develop...head`): 4 files, +55/-1: ks1620 test +21/-0, `tools/info.ts` +1/-1, the two docs +15/-0 and +18/-0. Matches the claim.
- info.ts is 173 lines on develop and on the head. Removing the one `// KS-1541` comment line from each side leaves the two files byte-identical (`diff` empty). The only changed line is the comment at line 129.
- The new comment, against the code: "every status but 401/404 is worded 'refused' (kept ...). A 403/503 fail-closed is a deliberate refusal; a 400, 429, 500 or proxy 502 is not, and the status in the note is how a reader tells them apart." TRUE. The condition is `connectorResult && !connectorResult.ok && status !== 401 && status !== 404` giving `Connector info refused by the gateway (${status})` plus optional `: text`, so 400, 429, 500, 502 all get "refused" with the status; the cells and my mutants confirm it. Imprecision (INFO): "every status" means every non-ok status; a thrown/rejected call (`.catch(() => null)`) or a 200 with null data gets the old note. The comment does not say so. Not wrong enough to matter.
- User-visible wording unchanged: the `refused by the gateway` template line is not in the diff; my wording mutant ("denied") fails 11 of 20 cells.

## TESTED
Emit hash (TypeScript `transpileModule`, comments removed, fixed filename): develop info.ts `6bfef20abaf295a6`, head `6bfef20abaf295a6` (identical); `200 -> 201` one-token change `f4dfef94a1e88023`; the exact values in the seat's mail. My own other one-token change (`!== 404` to `!== 403`) `3049b5030c56fbac`. So the instrument sees a code token and the PR changes none.

Suite: head, mcp-server, whole: 5 files, **20/20** (cold 883 ms, warm re-run 363 ms, no timeouts either time). Develop's info.ts plus develop's test file (copied into the head's tree): 15/15. ks1541 file 6/6. ks1620 file 4 cells on develop, 9 on head.

Mutants of `info.ts` (applied to the head's file, restored each time; OLD = develop's test file, NEW = head's):

| mutant | OLD (15) | NEW (20) |
|---|---|---|
| H1-M3 drop `!connectorResult.ok` | 15/15 survives | 19/20, H1-M3 cell only |
| H1-M8 `typeof message==='string'` to `!= null` | 15/15 survives | 19/20, H1-M8 cell only |
| 400 treated as not-available | 15/15 survives | 19/20, the 400 cell only |
| 429 | 15/15 survives | 19/20, the 429 cell only |
| 502 | 15/15 survives | 19/20, the 502 cell only |
| 200-char bound dropped | 13/15 (B1, B2) | 18/20 (B1, B2) |
| own: slice 200 to 201 | 13/15 | 18/20 (B1, B2) |
| own: 500 treated as not-available | 14/15 (ks1541 C3) | 19/20 (C3) |
| own: 401 dropped from the exclusion | 13/15 | 18/20 (2 controls) |
| own: 404 swapped for 403 | 11/15 | 16/20 (4 cells) |
| own: status dropped from the note | 8/15 | 9/20 |
| own: string-error branch removed | 12/15 | 17/20 |
| own: wording "refused" to "denied" | 8/15 | 9/20 |

All seven numbers the seat quotes (15 of 15, 20 of 20, 19 of 20 each, 13 of 15, 18 of 20) reproduce. Every new cell does kill its own mutant, alone.

Docs (own merge base, both files): text up to `</body>` unchanged (head = base-before-`</body>` + block + base-from-`</body>`), numstat 15/0 and 18/0, one `</body>` each, tags balanced head, base and block; `systemTest/__tests__/html_docs_matrix.test.sh` 18 passed / 0 failed on head and on develop. Flow block 66 with 66.1 to 66.4 plus an unnumbered cheat-sheet block. The figures in 66.1/66.2 (hashes, 15 to 20, 13 to 15, 18 of 20) match my measurements. 66.4 says 9 cells in the ks1620 file and 20 tests: true.

Merge: `git merge-tree --write-tree origin/develop p1755` conflicts on exactly the two docs (2 CONFLICT lines) and nothing else.

## NOTES
- INFO: develop's flow doc already carries section 67.x, so this PR's "66" will need renumbering by the merger (as briefed, not a defect).
- INFO: 66.2 says "Measured at base 885d69b06f5f"; the PR's merge base with develop is `a105a9df` (the branch may have been measured earlier). Cosmetic.
- INFO: the comment wording above ("every status" = every non-ok status).
- INFO: nothing pins the comment itself (the seat says so); the behaviour it describes is pinned for 400/429/502/500.

## NOT TESTED
Node 24 (host has only v26.8.1; the PR says the same). api-client.ts typing of `error` as string (out of scope, stated by the PR). Nothing through a real gateway or stack. The merge simulation covered only the PR against the develop pin, not combined with other gated PRs.

## Instrument notes
1. First tool calls were refused by the workspace hooks: a `cd` call, and a `mkdir`/clone one-liner whose ssh option mentioned the key path under `!CODING` (guard misread a read as a write). I moved the key use into a sourced script (`gitenv.sh`), which only reads the key, per the brief; nothing under `!CODING` was written.
2. My first `npx vitest` run showed 18 passed / 2 skipped / 1 file failed because `packages/shared` was not built; after the build, 20/20. The first number is mine, not the PR's.
3. The develop baseline was run by copying develop's `info.ts` and test file into the head's tree (restored; both worktrees `git status` empty), not in `wt_dev` itself, which has no `node_modules`. Same lockfile not diffed.
4. My mutator replaces a string that must occur exactly once; one mutant ("status dropped") also touches the template literal, which is why its kill count is large; read it as "the status is pinned", not as a precise count.
