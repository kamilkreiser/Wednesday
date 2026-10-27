# QA gate verdict - Secuura/Blockchain PRs #1740, #1741, #1742

- Tier 2, round 1 of 2. Gate model: Claude Sonnet 5.5 (claude-sonnet-5-5). Date 2026-10-27.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-c-1027/` (clone `repo/`, worktrees `wt_dev`, `wt_p1740`, `wt_p1741`, `wt_p1742`, raw logs and scripts beside; private `TMPDIR=/tmp/gc1`). Node v26.8.1. `npm ci` run in `Blockchain/Dev` of all four worktrees first (1806 packages, rc 0 each).
- Pushed / merged / commented / edited a ticket: nothing. gh read-only, `gh api user` = `kksecura`.

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1740 KS-1753 (Seat S 4th) | GO WITH NOTES | LOW: new 401 text ends "a user or admin bearer token is refused with 403, not 401", but in the code a user bearer whose session is revoked gets 401 SESSION_INVALIDATED (auth.ts ~:490) and an unverifiable/expired one 401; true only for a valid, live user/admin token. Every numeric claim reproduced; yaml diff is exactly one string, semantically proven. |
| #1741 KS-1738 (Seat R 5th) | GO WITH NOTES | LOW: GitHub reads it **CONFLICTING/DIRTY** against develop (both HTML docs, same `</body>` insertion point as #1737's section 61). The brief named only #1742 as conflicting. Also its docs are numbered 63 while develop's top is 61 and #1739 (62) is still OPEN: a gap of 62 until #1739 lands. Code, red-proof and counts all reproduced. |
| #1742 KS-1754 (Seat S 4th) | GO WITH NOTES | INFO only: doc conflict is the expected numbering one and keep-both loses nothing; control C2's title says "exactly the expected number" but asserts only non-empty (the count is a separate cell). All four mutants reproduced, plus six extras. |

Merge: **#1740 is clean against develop and against every combination.** #1741 and #1742 each conflict with develop in the same two docs only; every order (15 sequences) resolves by keep-both with zero loss (trees below). The seats must renumber/rebase at merge time regardless.

## Pins (start = end)
```
dd893cfa2cdbbfcf73d38d5050ab6bd7d708209c  refs/heads/develop
5f0476f41dc83dc7c449a52fe5c24f5b1c0321b9  refs/pull/1740/head
15515935f9404e89bc3e4a7aaec399d7f8ec2585  refs/pull/1741/head
40570c2f1021135f25b86a8de75919e2c2575b5a  refs/pull/1742/head
```
`lsremote_start.txt` (read before anything) and `lsremote_end.txt`; `diff` empty (rc 0); both equal the briefed pins. PR states at end: #1740 OPEN UNSTABLE MERGEABLE; #1741 OPEN DIRTY CONFLICTING; #1742 OPEN DIRTY CONFLICTING. All three heads are based on older develop (#1740 on c3eb63c9, #1741/#1742 on f3042778), so I used `develop...head` for diffs. The cache `src` clone `git status` is empty; its deploy-key ssh command was copied into my clone's repo-local config for the fetch only.

## #1740 KS-1753

**FOUND**
- Scope vs develop (`develop...head`): exactly 2 files, 6+/4-: `services/api-gateway/src/api-gateway.openapi.ts` (3+/2-, inside the `/api/connector/info` registerPath 401 description; 403 untouched) and `docs/openapi/secuura-api.yaml` (3+/2-, one hunk at ~:15979 inside that 401 description). A two-dot diff against develop shows 10 files only because the head predates #1737/#1738; ignore it.
- Code it relies on, read: `middleware/auth.ts` `refuseConnectorBearer` :267 is reached from `refusesConnectorBearer` only past `if (decoded.type !== 'connector') return false` (:299) and from `authenticateToken` at :480 on `decoded.type === 'connector'`; `services/health.ts:42-46` (the brief said health.ts ~44-46; the file is `services/health.ts`) gives 403 when `!meta || req.user?.role !== 'connector'`. So a connector-JWT Bearer is 401 and a live user/admin bearer is 403: the new sentence is right for those.
- LOW: the sentence "a user or admin bearer token is refused with 403, not 401" is unqualified. A user token with a revoked session is 401 SESSION_INVALIDATED (`auth.ts` ~:490-495) and an invalid/expired one takes the invalid-token 401 path. The first sentence of the same description still covers "no usable credential", so a reader is not badly misled; I did not find a test that pins the wording.

**TESTED / HOW** (all rc 0 unless stated)
- `check:openapi` (generate --check + check:spec-examples): develop rc 0, head rc 0, **414 example blocks, "every published example resolves"** both. Claim holds (BEFORE and AFTER).
- No-op `generate-openapi` at develop: yaml sha256 before = after, **byte-identical**, worktree `git status` empty (312 paths, 1,370,365 bytes). At the head, regeneration also byte-identical to its committed yaml. So the committed yaml equals the generator's output at both ends.
- Yaml diff is one string: I parsed develop's yaml, the merge-base's yaml and the head's yaml with the `yaml` package and walked both trees: the only differing path (head vs develop and head vs merge-base) is `/paths//api/connector/info/get/responses/401/description`. The `.ts` string and yaml string agree (check:openapi).
- Control (check can fail): in my head worktree I edited one phrase in the yaml; `check:openapi` rc **1**, "CHECK FAIL: generated YAML differs from on-disk version"; restored with `git checkout`, `git status` empty, rc 0 again.
- `ks1531-connector-info-is-in-the-published-contract.test.ts`: develop **7/7**, head **7/7**. Full api-gateway vitest: develop **123 files / 1203 tests passed**, head **123 / 1203**, rc 0 both. Claims hold.

## #1741 KS-1738

**FOUND**
- Scope (`develop...head`): 5 files, 149+/1-: `support/generated_guard.sh` 32+/0-, `generated_guard_restore.test.sh` 78+/0-, `bootstrap_login_diagnosis.test.sh` 6+/1- (the trap line plus 5 comment lines), flow doc +12, cheat sheet +21. No product code.
- Guard change: `local rc=$?` stays the first statement; an optional `$1` is applied after it; empty or non-digit is refused with a named stderr line and falls back to `$?`; digits win. With no argument behaviour is unchanged.
- Chained trap in bootstrap suite: `trap 'rc=$?; stop_stub; generated_guard_restore "$rc"' EXIT` (captures first, stub stops before the guard, as the comment explains).
- Docs: numstat 0 deletions; asserted by script that head text equals merge-base text up to `</body>` and the suffix from `</body>` is unchanged (both docs): pure append. Section number **63**, develop's last is 61 and 62 (#1739) is not merged: LOW, a gap, not a content problem. Doc entries still say "measured at base c3eb63c9d23b" (INFO, same pattern as the previous batch).
- LOW: head is CONFLICTING against current develop (see Merge orders); the briefed "conflicting by design" list named only #1742.

**TESTED / HOW** (bash 3.2 harness, `TMPDIR=/tmp/gc1`; the suite makes its own `mktemp -d /tmp/ks1735.XXXXXX` which it removes on exit)
- `generated_guard_restore.test.sh`: develop (original suite + original guard) **15/0**; head **20/0**; **RED = new suite + ORIGINAL guard: 18 passed / 2 failed, rc 1**; control original suite + NEW guard **15/0**. Claims hold exactly.
- Which two cells go red on the original guard: **B'** ("a chained cleanup that HANDS THE STATUS IN keeps 3") and the **non-numeric argument** cell. The brief wrote "B arm red"; precisely, plain **B** (chained, no status, expects 1) is **green on both** guards by design (the fix is opt-in; the cell documents the residual flattening), and the red arm is **B'**. A and C green on both. Not a finding, a naming note.
- Independent A/B/C driver (mine, `abc.sh`, a fake `cp` that fails only into `*/generated/`, suite exits 3): original guard A=3, B=1, B'=1 (arg ignored), C=3; new guard A=3, B=1, **B'=3**, C=3, C'=3. Extras on the new guard: suite exit 7 + chained status -> **7**; suite exit 0 + failed restore -> 1 (the guard's "never report green" rule survives); `-1` and `""` refused, fall back to `$?` -> 1. The ticket's A/B/C table (3 / 1 / 3) reproduced.
- Mutant (copy of the new guard, non-numeric refusal branch disabled): suite 19/1, only the non-numeric cell red, rc 1.
- `bootstrap_login_diagnosis.test.sh`, short `TMPDIR=/tmp/gc1`: develop **18/0**, head **18/0**, rc 0 both. A deliberately long TMPDIR (~70 chars under /tmp/gc1) still read 18/0 for me, so I did **not** reproduce the "long TMPDIR reads 7/11" remark (my string may simply not have been long enough to break the socket bind; not a PR problem).

## #1742 KS-1754

**FOUND**
- Scope (`develop...head`): 3 files, 171+/0-: one new test `services/m365-integration/src/__tests__/ks1754-the-connection-status-enum-agrees-in-all-three-declarations.test.ts` (138 lines), flow doc +16, cheat sheet +17. No `src/` product file touched. The three declarations are where briefed: `index.ts:94` union, `m365-integration.openapi.ts:89` and `:114` `z.enum`.
- Test design (read in full): comment stripper is string-aware; `storedUnion` and `declaredEnums` extractors; 5 cells (C1 non-empty sources; C2 non-empty extraction; C3 comment-blindness with a positive twin inside the same cell; count == 2 enums; all values equal and equal to the four KS-1700 values). Env overrides `KS1754_INDEX_TS` / `KS1754_OPENAPI_TS` point the extractors at copies.
- Docs: numstat 0 deletions; base text up to `</body>` equal and suffix unchanged (both docs): append-only. Doc section is **61**; develop already has a 61 (#1737). Expected conflict, reported as such.
- INFO: C2's title says it checks "exactly the expected number of spec enums", but the body asserts only that every extracted enum is non-empty; the count is asserted by the next cell, so nothing is unprotected, only the title overstates.
- INFO: scrape-based by design: a status enum built from a shared constant or aliased type would not be found by the `z.enum([...])` literal regex (the alias case fails loudly, see M8), so the pin tells you to add it deliberately; it does not prove the service only assigns those four values.

**TESTED / HOW**
- `m365-integration` vitest: develop **26 files / 261 tests**, head **27 files / 266 tests**, 0 failed, rc 0 both. `check:test-types` rc 0 both; m365 line at head `0 errors: 0 in the baseline, 0 new; 0 stale baseline entries` (develop identical, 36 vs 37 files examined). Claims hold.
- Mutants on COPIES of `index.ts` and `m365-integration.openapi.ts` under `mut/` (live files untouched), the new test file run with the env overrides (`runmut.sh`):
| arm | result | cell that went red |
|---|---|---|
| control (unmodified copies) | 5/5, rc 0 | none |
| M1 drop 'error' from the union (:94) | 1 failed / 4 passed | "all three carry the SAME four values" (stored union must be the four) |
| M2 add 'expired' at :114 | 1 / 4 | same cell, "spec z.enum copy 2" |
| M3 add 'expired' at :89 | 1 / 4 | same cell, "spec z.enum copy 1" |
| M4 third agreeing copy | 1 / 4 | the COUNT cell alone ("expected 3 to be 2") |
| M5 reorder values in one enum | 5/5 green | none (order-insensitive, as intended) |
| M6 commented correct enum + live drifted one | 1 / 4 | agreement cell (the comment does not rescue the drift) |
| M7 live enum correct, drift only in a trailing comment | 5/5 green | none (comment-blind, correct) |
| M8 union refactored to an alias | 3 failed / 2 passed | C2 and both red cells fail loudly (extractor finds 0) |
| M9 one z.enum replaced by `z.string()` | 1 / 4 | COUNT cell ("expected 1 to be 2") |
| M10 drop 'error' from one z.enum | 1 / 4 | agreement cell |
  Claims reproduced: M1..M4 each 1 failed / 4 passed, green control 5/5, M4 fires the COUNT cell alone. The commented-enum control and its positive twin are both in cell C3 (negative half: commented enums yield `[]`; positive twin: the same text uncommented yields `[['pending','connected']]`; plus a `//` inside a string literal survives); C3 passes on the unmodified tree, and M6/M7 show the comment-blindness holds on the real files in both directions.

## Merge orders (my clone only; `git merge-tree --write-tree` chained with `commit-tree`; `merge_out.txt`, script `merges.py`)
Develop at dd893cfa. #1740 is clean in every position. #1741 and #1742 each conflict with develop, in the **same two files only** (the script refuses to resolve anything else, and none arose): `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` and `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html`, because each adds its block at the same `</body>` as #1737's block now in develop. Resolution used: keep develop's text and insert each PR's added block (head minus its merge-base, asserted to be a pure pre-`</body>` insertion) before `</body>`, in merge order. Nothing is dropped.

| order | result | tree |
|---|---|---|
| develop + #1740 | clean | cc19966e8767d2d3af41125b7c9fd5c20fa6746c |
| develop + #1741 | docs conflict (expected class; unflagged in brief) -> keep-both | d7ec2a2b1a695f61e1a5c14c517e26a2c131e2c7 |
| develop + #1742 | docs conflict (expected) -> keep-both | 2e3a17d9d831ee6e4823b189984e45dd9a93e5e6 |
| 1740,1741 = 1741,1740 | #1741 doc conflict only, one tree | c292ad4948d6cea5aa3a7b831c09fe925cc62b5b |
| 1740,1742 = 1742,1740 | #1742 doc conflict only, one tree | c9d1d28fcf8bd46815f8e1e5d7cff5064c1a609f |
| 1741,1742 | both doc conflicts | 88a21e7af5742cc912c3eacd72635887abd717fa |
| 1742,1741 | both doc conflicts | 102f8cb6d93e6886c7650fd3fd79ddf35f5391a5 |
| all three, 1741 before 1742 (any position of 1740: 3 orders) | doc conflicts only | 83f44927ba4af35c1cd30e18274441deb200eb77 |
| all three, 1742 before 1741 (3 orders) | doc conflicts only | e396e9415b175b354b637c4eb18d512190b1e073 |

Conservation: each all-three tree vs develop = +326 / -5, exactly the sum of the three PRs (6+/4- , 149+/1- , 171+/0-); docs +28 / +38 with zero deletions. Numbering after keep-both: 1741 first gives `..., 61 (#1737), 63 (#1741), 61 (#1742)`; 1742 first gives `..., 61, 61, 63`. So **#1742's section 61 must be renumbered at merge (fleet rule, expected)**, and #1741's 63 leaves 62 empty unless #1739 (open, also a doc-block adder) lands first; whichever of #1739/#1741/#1742 merges last will need the same mechanical resolution. Cheat-sheet sections are unnumbered.

## NOT TESTED
- Any HTTP probe of `GET /api/connector/info` with a user/admin/connector bearer (the 401/403 split is established by reading `auth.ts` and `health.ts` and by the existing ks1531 suite, not by a live request).
- Whether #1741's chained trap preserves a **failing** bootstrap suite's status in the real suite (only the guard and its driver were exercised; the bootstrap suite was run green only).
- The four "platform suites" the seat marks UNMEASURED; the aggregate `run-shell-suites.sh`; lint; Linear states; browsers.
- Suites on the merged trees (trees computed only, not built/run).
- #1742's two doc entries' figures beyond the 26/261 -> 27/266 and 0/0/0 numbers I re-measured.

## My instrument errors
1. First `m365` vitest run at #1742 read 16 files failed (rc 1) and `check:test-types` rc 2: `packages/shared/dist` had not been built there (`Blockchain/Dev/.npmrc` sets `ignore-scripts=true`, so `npm ci` does not build it; develop had it only because my earlier `generate-openapi` run built it). I built it in the head worktree (`npm run build --workspace=packages/shared`) and re-ran: 27/266, rc 0. The first result was my environment, not the PR; both sides were then symmetric. (This is the same class of error as the previous gate's missing install.)
2. The fleet hooks refused `cd`, a `git -C $VAR fetch`, `rm` inside a script, and an unquoted `======`; I re-issued everything as script files with literal absolute paths and used `npm --prefix` and `mktemp -d` instead of `cd`/`rm`. No effect on results.
3. One zsh no-match (`--include=*.ts` unquoted) and one mutants-log read from the wrong cwd; re-run correctly.
4. My long-TMPDIR control for `bootstrap_login_diagnosis` did not reproduce the seat's 7/11 (see #1741); I do not know whether my path was long enough. Treated as NOT reproduced, not as a refutation.

## Files outside the workspace
None kept. Writes: the workspace, `/tmp/gc1` (private TMPDIR, scratch copies, temp git index files), the suite's own self-cleaning `/tmp/ks1735.*`, and this verdict folder `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-c-batch/`. `find /Volumes/DevMASTER/WEDNESDAY -maxdepth 1 -newer lsremote_start.txt` lists only `.git` (the repo's own); no stray file in the WEDNESDAY root. All four worktrees `git status` empty at the end.
