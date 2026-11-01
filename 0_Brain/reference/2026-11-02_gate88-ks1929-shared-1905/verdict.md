# QA GATE 88 (Tier 1, Opus): PR 1905 / KS-1929, batchLoadRelatedData identifier validation

## BLUF
**GO WITH NOTES.** Nothing needs fixing before merge. The one condition is ordering: PR 1903 merges first, because 1905 is stacked on it.
The validator is anchored at both ends, uses no flags, enforces the 63-character cap, accepts only strings and covers both identifiers. It runs before the only prisma call, and there is no early-return path. All 56 bypass probes are refused and nothing reaches the client. These include zero-width characters, a BOM, CR, CRLF, NUL, U+2028, Cyrillic, dotless-i, Kelvin, long-s and math-bold lookalikes, and newline smuggling. For valid names the SQL text is byte-identical to the base and `parentIds` is still bound. The PR's tests go red-first at 12bafc96 (38 red, 7 controls green) and green at the head. All 20 mutants are killed. The SQL guard is green and the entry is no longer ALLOWED-OPEN. Planted unvalidated copies of the call turn it red.

## Heads
- Start 2026-11-01T15:10:52Z (logs/head_start.log): pr1905 `355a3b2a6adaf0f56981a121e8deb8233094eea5` (one commit, parent `12bafc96c91262f7a6ee218f1d5cd8eda84bf858` = pr1903 head), develop `96480cc6a4500da9dbca175cd6e101a82a28ce55`. All match what was expected.
- End 2026-11-01T15:18:18Z (logs/head_end.log): both PR heads unchanged. **develop moved** to `66dc9e15c2db624c6288caf8245f38c9d9a9e081`, one commit (KS-1903, Dockerfile non-root check). It touches none of 1905's paths, and merge-tree onto it is clean (logs/develop_moved.log).
- Reviewed only 12bafc96..355a3b2a: 5 files, +202/-1 (logs/diffstat.log, logs/diff_src.log).

## Findings
- **G88-F1 (note, structural; inherited from the KS-1867 design):** the guard's ALLOWED entry is static. With the validator lines deleted, `check-no-sql-injection.sh` still exits 0 and reports the site as ALLOWED (logs/sqlguard_validator_removed.log). The entry also cites line numbers (`:106-108`, `:117-119`) that go stale on any edit. The real backstop is the unit suite: mutants M11 (guard after query) and M20 (return instead of throw) are both killed. Not a merge blocker. Possible follow-up: have the guard grep for `isSqlIdentifier(` near the allowed site.
- **G88-F2 (note, cosmetic):** the allow entry says "19 mutants". The gate ran its own 20, all killed (logs/mutants_pr_tests.log).
- **G88-F3 (note, cosmetic):** at the base, R2 goes red through `TypeError: Cannot read properties of undefined (reading 'message')` rather than an assertion. It is still red for the right reason (nothing was thrown). The other 37 red cells fail on assertions (logs/base_new_tests.log).
- **G88-F4 (note, scope):** identifier-shape validation does not limit which table or column a caller can name. A caller that passes request-derived but identifier-shaped text (for example `pg_shadow` or `users`) can still read any relation on the search_path. This is outside the ruling's scope, which keeps the export. The PR body should state that callers must map to an allowlist.
- **G88-F5 (environment, pre-existing):** `wallet-signature.test.ts` "accepts a valid wallet signature" fails at both head and base (logs/head_whole.log, logs/base_wallet_signature.log). It is unrelated to this PR. With tests included, tsc reports 26 pre-existing errors in other test files and `ssrf-guard.ts`, and **0** in either PR file (logs/tsc_shared_incl_tests.log, positive control ks781 = 6 lines).

## Q1: Validator and bypass probes
- `/^[A-Za-z_][A-Za-z0-9_]*$/` has no flags. In JS without `m`, `$` matches only at the true end of the string, so a trailing `\n` cannot slip through. The `[A-Za-z]` class is ASCII-only. There is no `g` flag, so there is no `lastIndex` state.
- `isSqlIdentifier` checks, in order: `typeof === 'string'`, then `length <= 63`, then the regex. It is applied to `model || relatedField`, and the guard sits on the first statement of the function, before `$queryRawUnsafe`. The function has no early return. Even with an empty `parentIds`, a bad name is refused with zero client calls (probe).
- Probes (logs/_quarantine/g88probe.test.ts.txt, run in logs/head_new_and_probe.log): 28 bad values × both identifiers = 56 refused with the constant error and 0 client calls. Also passing: an async-rejection check (no synchronous throw), a statelessness check, and 5 valid cases. 109/109 green, which is the PR's 45 plus 64 probes.

## Q2: Valid input unchanged
The probe's "G88 valid" block (5 name pairs, including 63-character names and the reserved words `select`/`from`) asserts the exact call `[template, ids]` and that the ids array is the same object passed in. It passes at the **base** optimization.ts (logs/base_probe_valid.log: 5 passed) and at the head. The SQL text is byte-identical and `parentIds` is bound as `$1`. A hostile id never appears in the SQL text.

## Q3: Guard
- `run-code-guards.sh` on the head tree: rc=0, "13 code guards passed" (logs/guards_head.log). `check-no-sql-injection.sh`: rc=0, **ALLOWED-OPEN (0)**. optimization.ts:120 is now **ALLOWED**, with a reasoned entry citing `isSqlIdentifier` (optimization.ts:106-108) and the guard at :117-119. Both line citations were verified (logs/sqlguard_head.log).
- Planted an unvalidated copy in `packages/shared/src/db/index.ts`: the SQL guard and run-code-guards both returned rc=1, with the hit named (logs/sqlguard_plant_otherfile.log, logs/guards_plant_otherfile.log). Planted the identical line a second time inside optimization.ts: rc=1, hit at :184 (logs/sqlguard_plant_samefile.log). The tree was restored and porcelain is 0.

## Q4: Red-first, suites, types, lint, dependents, mutants
- At base 12bafc96 (optimization.ts only swapped): 38 failed and 7 passed. The 7 are the V1, V2, V3×4 and B1 controls (logs/base_new_tests.log). At the head: 45/45 pass.
- Whole packages/shared suite (cwd = package): 1152 passed and 1 failed, the pre-existing wallet-signature failure (G88-F5) (logs/head_whole.log).
- tsc, plain project: rc=0 (logs/tsc_shared_plain.log). Tests included: 0 errors in the PR files (G88-F5).
- eslint on both changed files: rc=0, 0 errors and 0 warnings. Both files were really linted, not ignored (logs/eslint_pr_files.log, logs/eslint_json_summary.log).
- Dependents, `tsc --noEmit` against the head-built shared: services/originate rc=0, services/anchoring rc=0 (logs/tsc_originate.log, logs/tsc_anchoring.log).
- Mutants against the PR's own test file: 20 run, 20 killed (logs/mutants_pr_tests.log, logs/mut_pr_*.log):

  | Mutant | Effect |
  |---|---|
  | M01 | drop `^` |
  | M02 | drop `$` |
  | M03 | add `m` flag |
  | M04 | drop length check |
  | M05 | cap 64 |
  | M06 | `<` instead of `<=` |
  | M07 | drop typeof check |
  | M08 | drop model check |
  | M09 | drop field check |
  | M10 | `\|\|` changed to `&&` |
  | M11 | guard after query |
  | M12 | message leaks the value |
  | M13 | digit allowed first |
  | M14 | `.` in character class |
  | M15 | space in character class |
  | M16 | `g` flag |
  | M17 | `.*` tail |
  | M18 | `\p{L}` with `u` flag |
  | M19 | cap 62 |
  | M20 | return instead of throw |

## Q5: Caller safety of the thrown constant
`git grep -w batchLoadRelatedData` at the head finds only the definition, the new test, the allow entry and the fragments. At develop it finds only the definition. There are 0 in-repo callers (logs/callers.log). The export lists of optimization.ts at base and head are identical apart from line offsets. `index.ts:18 export * from './db/optimization'` is unchanged. The error is a plain `Error('Invalid SQL identifier')` delivered as an async rejection, and it never carries the value (R2, M12). The only behaviour change for an external caller is a rejection on input that was already injectable, plus refusal of schema-qualified `public.x`, which the PR documents.

## Q6: Merge
- merge-tree of pr1905 (which contains 1903) onto develop 96480cc6: clean, tree `82f5331b…`. pr1903 alone onto develop: clean, tree `5fa16ca3…`. Onto the moved develop 66dc9e15: clean, tree `91e09ba8…` (logs/merge_tree.log, logs/develop_moved.log).
- `develop...pr1905` lists 13 files: 1903's 9 (the SQL guard script, its 5 shell tests, the .allow file and 2 fragments) plus 1905's 4 new paths. Confirmed: **1905 cannot merge before 1903**. Until 1903 merges, its diff against develop carries 1903's files.

## Notes for the PR body
- Merge after PR 1903. Retarget to develop once 1903 lands, so the diff shrinks to 5 files.
- Gate 88: 56 bypass probes refused (zero-width, BOM, CR/CRLF/NUL/U+2028, Unicode lookalikes, newline smuggling), 20/20 independent mutants killed, SQL text byte-identical to the base for valid names, guard red on planted copies, originate and anchoring tsc green.
- Callers still need a table/column allowlist. Shape validation stops SQL injection but not reads of arbitrary relations (G88-F4).
- The guard entry is static and does not check that the validator is present. The unit suite is the backstop (G88-F1).
- The wallet-signature failure is pre-existing and unrelated (G88-F5).
