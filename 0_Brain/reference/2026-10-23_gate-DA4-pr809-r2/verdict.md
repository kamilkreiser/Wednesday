VERDICT #809: GO WITH NOTE at head 7892929e7eb2... (tier 2, round 2 of 2; landing tree 650b240b2ab8 on develop 25f42d80b0fc; 0 blockers, 2 notes)

## BLUF
- The round-1 blocker is closed. The seven new entries now use `checks.not_a_server_error.expected-statuses = ["2xx", "3xx", "4xx", "503"]`, byte-identical to develop's 14 existing 503 entries. I ran every assertion the lockstep tests make against the head: all pass (21/21, orphaned [], unguarded [], `enabled=false` [], each tolerance exactly {503}).
- The author's predicted landing tree `650b240b2ab8` is correct on LIVE develop `25f42d80b0fc`; it differs from develop in exactly the two PR files (+13 lines in `check_predicates.py`, +35 in `schemathesis.toml`, 0 deletions).
- Nothing that is not run is a blocker for an interim test-config change (see Q5). Two notes, neither blocks.

## FOUND
Heads at start and end (`git ls-remote`, identical both times, 12:51 and 12:53 AEDT): develop `25f42d80b0fc7f99528ae7fc54ac66f50f85d5df`, #809 `7892929e7eb2c45a46ac38f2d7cdcc571b276167`.
- **NOTE 1 (cosmetic, toml comment):** the new KS-693 comment block has a hard wrap that leaves a one-fragment line (`# to M365_UNAVAILABLE_RESPONSE before any` / `# route logic ...`), and the block ends with two blank lines where the file's convention is one. Cosmetic only.
- **NOTE 2 (unmeasured claim):** the comment states "Live-verified 2026-09-04: all seven return 503 with the declared envelope." That is the author's claim from an earlier round, carried in a comment; I did not and could not re-measure it (no stack). The code supports it: all seven routes sit behind `requireM365` (`m365-integration/src/index.ts` lines 710, 830, 881, 1013, 1192, 1271, 1565) and `requireM365` is at line 261 with `if (!isConfigured())` at 262, so the comment's "about line 261" is right.
- No other finding.

## TESTED / HOW
Method: scratch clone, fetched develop and `refs/pull/809/head` into private refs, extracted the toml, `check_predicates.py` and `tests/support/by_design_tolerances.py` from develop, the head, the derived landing tree, and round-1 head `736442fa9158`; imported the project's own helper module by path under Python 3.14.5 with `-I` (no pytest). The frozensets were read with `ast`. Script: `scratchpad/da4/chk.py`.

**Q1, blocker closed.** I read all lockstep assertions in `test_integration_5xx_guard.py` (`TestLockstepWithSchemathesisToml`: unguarded, orphaned, exactly-{503}, dead-key, KS-544 four present) and the cross-set class in `test_by_design_501_guard.py` (501 ops tolerate exactly {501}, every tolerating op owned by exactly one guard, no shared ops, no dead key, wallets/verify present). Results:

| assertion | develop | head 7892929e7eb2 | landing tree |
|---|---|---|---|
| frozenset / toml tolerates 503 | 14 / 14 | 21 / 21 | 21 / 21 |
| unguarded (toml minus frozenset) | [] | [] | [] |
| orphaned (frozenset minus toml) | [] | [] | [] |
| tolerance wider than {503} | none | none | none |
| `enabled=false` ops | [] | [] | [] |
| 501 set orphaned / unowned / shared | [] / [] / [] | [] / [] / [] | [] / [] / [] |
| KS-544 four present; wallets/verify in 501 set | yes | yes | yes |

Develop control matches the author's 14/14/[]/[]; the head matches 21/21/[]/[].
Positive control from a different family (the same instrument on round-1 head `736442fa9158`): toml tolerates 503 on 14 of 21, orphaned = exactly the seven new ops (`m365/connections/init`, `connections/{id}/refresh`, `documents/sync`, `outlook/exchange-token`, `m365/sites`, `onedrive/files/{id}/sync`, `teams/webhook-config`). So the zeros above are produced by an instrument that does fire.

**Q2, shape.** All seven new lines match develop's 14 lines exactly (21 column-0 occurrences of the canonical line; the only other `not_a_server_error` form is the single `["2xx","3xx","4xx","501"]` for wallets/verify). Dead-key text appears 2 times, both in develop's own header comments (lines ~338 and ~732), untouched by the diff; live `enabled = false` lines: 0. Exactly one `POST /api/teams/webhook-config` block, carrying `positive_data_acceptance` AND the 503 tolerance. 49 entries, no duplicates; frozenset == toml 503 set (21 == 21). `connections/complete` appears 0 times in either file.

**Q3, scope since round 1.** `git diff 736442fa9158 7892929e7eb2` is 2 files, +13/-11: seven `enabled = false` -> `expected-statuses` line swaps, plus the two comment rewrites (`index.ts:229` -> per-route `requireM365`, about line 261). Nothing else moved. Develop's schemathesis tree is unchanged since round-1 develop `95a2dff1d784` (empty diff over `systemTest/schemathesis`), so the four merges since (#1253 #923 #927 #920) touched nothing there.

**Q4, spec.** On develop, `Blockchain/Dev/docs/openapi/secuura-api.yaml`: all seven operations present with a declared 503 (parsed per-operation); `/api/m365/connections/complete` has 0 occurrences (control: `connections/init` present, 2 occurrences).

**Q5, not covered.** (a) pytest suite: not run (conftest refuses Python < 3.14.8, nothing bypassed). The assertions that matter for this change were reproduced by calling the same helpers, so I judge this an accepted NOT RUN. (b) Real Schemathesis run and live 503 claim: no stack; the 503 behaviour is code-supported (`requireM365`), and the toml shape is the one develop already runs on 14 operations, so this is an accepted NOT RUN for an interim test-config change (note 2 records it). (c) No hook check ran on the push: systemTest-only, no `package.json` under `systemTest/schemathesis`; the CI/pre-push gate will run the unit suite, and I show it would pass its lockstep assertions. Accepted, not a blocker.

## NOT RUN
pytest (any), a real Schemathesis run, live 503 envelope, hook legs, Docker/stack, `test_not_a_server_error_suppression.py` (drives the real CLI against a stub; needs the venv), PR body and GitHub/Linear state. The pre-existing stale historical quote in `docs/reviewer-comments/ks-693-m365-503-floor.md` line 105 (old `enabled = false` approach) is outside the PR's two files and left alone.

Housekeeping: `git -C /Volumes/DevMASTER/WEDNESDAY status --short` shows no untracked or modified paths outside `0_Brain/`, `5_Project_History/`, `2_Project_Files/local-model/`, `2_Project_Files/fleet/briefs_staged/`. Secuura project folder not touched; I used the project deploy key via `GIT_SSH_COMMAND` for read-only `ls-remote`/`fetch` into the scratch clone only.

## Wall-clock
Started 12:51 AEDT, finished about 12:55 (shell clock).

sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: 0a8635055bdc1751532c7930f572f7958b0e6e94003805e3a685efe12fca3c3e