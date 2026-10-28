# QA gate 2 (tier 2, batch, round 1 of 2): Secuura #1775 (KS-1467), #1776 (KS-1591), #1780 (KS-1702)

- **Gate model:** Claude Sonnet 5.5 (claude-sonnet-5-5), G2 tier-2 gate, subagent of Wednesday. Spark review model for #1780: deepseek-v4-flash-0731 via the tunnel.
- **Routing receipt:** tier 2 because #1775/#1776 are Spark passes already through the Spark gate half and #1780 is test-only (055 byte-identical). **One item below is security-relevant and tier-1 reading is worth the cost: see #1776 F1.**
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing. Linear was read-only (comments first:100, key never printed). The only writes were to my own clone, my own scratch worktrees, one Docker container I started and removed, and files under this reference folder and the work folder.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate2-1775-1776-1780/repo` (did not exist before; `rev-parse --show-toplevel` asserted equal to that path before the first fetch). Worktrees and scratch under `/private/tmp/claude-501/gatework2/` (spark_gate.sh refuses a work dir under WEDNESDAY). The five worktrees (b1780, h1775, h1776, h1780, w1780) were NOT removed (no-delete rule); they hold only symlinks to node_modules and my scratch edits, each restored byte-identical.
- **node_modules:** read-only symlinks from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/` (root, packages/shared, services/originate, services/security, services/auth). Nothing installed anywhere. Node v26.8.1 (not the repo's LTS 24), every run.
- **Load:** load1 was 7 to 13.5 at each heavy run, never above 14. Spark queue lock was clear.

## Pins (git ls-remote)

| ref | start (19:11) | end (19:26) |
|---|---|---|
| develop | bd6697e079fce41db6b21e094a9eddb3d0e1d08e | bd6697e079fce41db6b21e094a9eddb3d0e1d08e |
| refs/pull/1775/head | 4cd8bb3b4c04a995a94767e44fd256d34d1cc499 (prefix 4cd8bb3b4c04 matches) | same |
| refs/pull/1776/head | 319b0f24f8b9a8da1047b811e2082dfae3b021f9 (prefix 319b0f24f8b9 matches) | same |
| refs/pull/1780/head | ba9a24a775dab486af04b0586a1314f90ef63eee (equals the brief) | same |

Nothing moved. Merge-base of all three with develop is bd6697e079fc (each head is a branch off current develop).

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1775 | KS-1467 | **GO WITH NOTES** | Fix is one line, test goes 19 red / 10 green when the hunk is reverted and 29/29 restored. The two count discrepancies are resolved (neither is a PR error). Notes: docs section number, other-importers suites unrun. |
| #1776 | KS-1591 | **GO WITH NOTES, and do NOT close KS-1591 on merge** | Both new tests go red when their hunk is reverted. But `decideMint` (the POST /api/keys admission) still admits the dotless-i, long-s and array roles at the PR head: measured. Not a defect in the PR's own two sites; a hole in the ticket's own evidence line ("the mint answered 201 for all three"), which neither the PR nor the Spark review names. |
| #1780 | KS-1702 | **GO WITH NOTES** (notes are merge-time only) | 20/20 on a real PG 15 at head, 17/17 base file at base, O3 and O4 mutants red exactly where claimed, SEAM works, seam cannot reach production. Spark said NO GO; I could not make any of its 5 findings stand as a defect. |

Recommended merge order (all three are disjoint in code; only the two docs conflict): **#1775, then #1776, then #1780** (smallest blast radius first; #1776 is the one a human should read before merge; #1780 is test-only and can go any time). Docs: develop's highest Flow-doc section is **83**; all three heads carry `<h2>84.` (collision). At merge give them **84 (first merged), 85, 86**, and rewrite the sub-headings (`84.1`...`84.5` in #1780, and any `84.x` cross-reference inside each block) with the final number. Cheat-sheet `<h2>`s are unnumbered, so nothing to renumber there; each head's block is a pure insertion before `</body>` in both docs (checked: head == base[:i] + block + base[i:], one `</body>`).

---

## Job 1a: the shared-suite count discrepancy (RESOLVED: both numbers are right, they count different things)

FOUND: PR says 1034 -> 1063 (#1775) and 1034 -> 1047 (#1776); the Spark half measured 1039 -> 1068 and 1052.
TESTED: `vitest run --reporter=json` of `packages/shared` on the merge-base tree, #1775 head and #1776 head, with the real Dev-root node_modules (files `suites/shared_b1780.json`, `shared_h1775.json`, `shared_h1776.json` in the work folder).
RESULT:

| tree | files | vitest cells (numTotalTests) | UNIQUE cell names | failed |
|---|---|---|---|---|
| develop bd6697e | 54 | **1039** | **1034** | 2 (see below) |
| #1775 | 55 | **1068** | **1063** | 1 (wallet-signature cbor) |
| #1776 | 55 | **1052** | **1047** | 1 (wallet-signature cbor) |

HOW the gap arises: exactly one title is duplicated, `input types rejects %p`, a parametrised `it.each` whose title never interpolates `%p` into distinct names, so six cells share one name. 1039 raw minus 5 duplicates = 1034 unique names; same for 1068/1063 and 1052/1047. The PR comments say "cells by cell name", so the PR is right by name, and the Spark half is right by raw cell count (and its +29 and +13 deltas equal the PR's). Control: unique names by `file::fullName` give the same 1034/1063, so it is not a cross-file artefact. No new cell vanished or failed in either PR.
Side result: on the BASE tree, in my run, a second cell failed (`threadToken` `parameteriseMintPolicy`, a timeout under load); it passed at #1775 and #1776. The Spark half saw the same cell fail only on HEAD. It is a load-dependent timeout independent of any PR, which closes the Spark half's open question.

## Job 1b: ks949 vs ks1000 (RESOLVED as far as it can be; it concerns #1779, not these three PRs)

FOUND: the discrepancy belongs to PR #1779 (KS-1536, services/auth), not to #1775/#1776/#1780 (the PR comment on KS-1536 says "the same `ks949` tree-walk cell at the 5 s default on both sides"; the Spark half named a `ks1000` REAL cell).
TESTED: (1) both files exist on develop (`ks949-platform-admin-seed-identity.test.ts`, `ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts`); (2) the two files run together at default timeouts on develop: both green, ks949 31 cells in 4972 ms (cells at 2.6 s and 1.8 s, i.e. close to the 5 s default), ks1000 99 cells in 63 s with its REAL cell at 17 s; (3) the full services/auth suite on develop at DEFAULT timeouts under load 8 to 13: 1192 passed, 0 failed, and one suite not loaded (ks1009, "could not locate the Dev root from /Volumes/DevMASTER/WEDNESDAY": my own harness cwd, 8 cells, so 1192 + 8 = 1200, the PR's base count).
HOW to read it: they are two different cells. `ks949` is a documented load-sensitive 5 s timeout (the repo's own docs at #1779's head, flow doc lines 2660, 2771 and 4820, record "ks949 ... 5000 ms timeouts seen ... the same three fail" at base, KS 1155), so the PR's claim is consistent with its default-timeout run. The Spark half ran with `--testTimeout=120000`, which lifts exactly that flake, so the only failure left in its run was a different cell, `ks1000 REAL`, which passes here on an untouched tree. I could NOT reproduce a ks1000 failure and did not find its cause; the Spark half itself flagged its symlinked tree as the likely source. Neither failure reproduced in my clean-tree run. Neither PR text is wrong. This should be carried to #1779's own gate, not this one.

---

## #1775 (KS-1467, shared AppError prototype): GO WITH NOTES

Head 4cd8bb3b4c04 (asserted). Diff vs develop: `packages/shared/src/errors/index.ts` (1/1), the new test (+73), and the two docs (+16, +20).

### Reading the diff against the ticket
The ticket's recommendation is `Object.setPrototypeOf(this, new.target.prototype)` in both places, a cell per subclass, and a deliberate decision on 422 `details`. The PR does the `packages/shared` place only, says so in its comment ("the `services/auth` half is a separate PR"), and the code line is exactly the ticket's. The ticket's own "Not established" list (any other `instanceof <subclass>` outside services/auth; whether the shared handler has a `details` branch) is the right frame for the Majors.

### Mutation check (revert the product hunk on the scratch worktree, restore, re-run)
| step | result |
|---|---|
| product file replaced by develop's `errors/index.ts` | new test **19 failed / 10 passed** of 29 (P1 x9 + P2 x9 + P3 = the 19; C1 x9 + C2 stay green) |
| restored (cmp against the saved file and against the PR blob `refs/pull/1775/head`) | identical; **29 / 29** |
Matches the PR's "19 / 10 / 29" exactly.

### Spark Majors judged
- **F1 (other services' suites not run): UNMEASURED, tightened by me.** `git grep` of the PR head for `instanceof <any of the ten shared subclasses>` outside tests finds exactly two lines: `services/auth/src/middleware/errorHandler.ts:296` (auth's OWN `AppError`, separate file, the ticket's p1 half, not touched here) and a comment in `passwordLoginGate.ts:288`. No service consumes a shared subclass by `instanceof`, so the one-line change has no `instanceof` consumer to break. Positive control: the same grep for `instanceof AppError` returns hits in shared (2), the new test (2) and auth's `dbErrors.test.ts` (1), so the pattern matches. NOT covered: `constructor.name` or `err.name` string checks (my grep was too noisy to be a claim) and any other service's suite, which I did not run.
- **F2 (no auth errorHandler change): SCOPE NOTE.** Confirmed: no auth file in the PR; the PR names it as a separate PR. The ticket stays open until that lands.
- **F3 ("byte-identical" unverifiable): NOT REPRODUCED**, the Spark half verified it by blob; I did not redo it.

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1775-1 | Low (merge-time) | The doc blocks carry section **84**, develop's highest is 83 and #1776 and #1780 also carry 84. | FOUND by reading; TESTED by listing `<h2>` numbers at develop and each head; HOW: `git show` + regex. |
| 1775-2 | Low | The count in the PR text (1034/1063) is by unique name, the raw vitest total is 1039/1068. | See Job 1a. The wording "cells" is ambiguous; the number is not wrong. |
| 1775-3 | Low | The ticket stays open: the services/auth half is another PR and the ticket's 422-`details` decision (a visible response change) is not in this PR. | FOUND in the PR comment and ticket; not tested. |

---

## #1776 (KS-1591, shared + security): GO WITH NOTES (hold KS-1591 open)

Head 319b0f24f8b9 (asserted). Diff: `packages/shared/src/security/keyRevokePolicy.ts` (+4/-1), `services/security/src/index.ts` (+4/-1), two new tests (78 and 89 lines), two docs.

### Mutation check (each product hunk reverted alone, then restored)
| step | result |
|---|---|
| shared `keyRevokePolicy.ts` -> develop's | shared test **6 failed / 7 passed** of 13 (R1, R2, R3, R4, R5, D1) |
| restored (cmp saved file, cmp PR blob) | **13 / 13** |
| security `index.ts` -> develop's | security test **3 failed / 4 passed** of 7 (R1 dotless-i, R2 long-s, R3 array) |
| restored (cmp saved file, cmp PR blob) | **7 / 7** |
| extra mutant A: shared keeps the ASCII fold but stringifies a non-string role | R3 and R4 only go red (2 failed / 11 passed): the non-string half is pinned independently of the fold half |
| extra mutant B: security keeps the fold but stringifies a non-string role | R3 only goes red (1 failed / 6 passed) |
Matches the PR's "6/7 and 3/4 at the pin, 13/13 and 7/7 with the change". Shared suite at head: 1052 cells (1047 by name), only the Node-26 wallet-signature cbor cell red (same as base).

### Reading the diff against the ticket
Ticket "Recommendation": compare against an exact ASCII-folded string and reject a non-string role "in the one shared definition so every caller inherits it"; "Where": `isPlatformRole` and `requireKeyAdmin`; "Worth a sweep for other `toUpperCase()` role comparisons rather than fixing only these two." The two named sites are fixed as written; the fold is correct (for ASCII input it equals `toUpperCase()`, so no admitted ASCII spelling changes; non-ASCII look-alikes and non-strings are refused). The PR can only remove access.

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1776-1 | **Major (completeness, not a defect in the changed lines)** | **`decideMint` is still open.** `services/security/src/provisioningPolicy.ts:97` is `if (KEY_ADMIN_ROLES.has(role.toUpperCase()))` with `role = String(caller?.role ?? '')`. It is the admission test of `POST /api/keys` (`requireKeyAdminOrProvisioner`, index.ts:1143-1164), and it uses the same `KEY_ADMIN_ROLES` set that `requireKeyAdmin` guards. The ticket's own BLUF measurement is "the mint answered 201 for all three"; the PR fixes the GET/DELETE guard (`requireKeyAdmin`) and `isPlatformRole`, and leaves the mint admission as it was. | **FOUND** by reading `git grep` for the role/`toUpperCase` pattern at the PR head; **TESTED** by running the head's real `decideMint` under tsx with six roles: ASCII `ISSUER_ADMIN` -> allow (via admin); dotless-i `ıssuer_admin` -> **allow**; dotless-i `super_admın` -> **allow**; long-s `ſuper_admin` -> **allow**; array `['SUPER_ADMIN']` -> **allow**; `user` -> deny 403. **HOW:** `/private/tmp/.../scratchpad/dm.ts` imported the head file; control row (`user`) shows the function can say no. NOT tested: the full HTTP route (index.ts also calls the now-fixed `isPlatformRole` after admission at :1206/:1249/:1311, so a look-alike `super_admın` that used to mint as a platform admin is now treated as a non-platform tenant admin there: narrower than before, but still admitted past the gate). Judgment: the PR's text says "both halves of the ticket"; by the ticket's Where list that is true, by the ticket's evidence line it is not. **Do not close KS-1591 on merge; file the `decideMint` follow-up.** |
| 1776-2 | Minor | Siblings of the fixed predicate in the SAME file still use `String(role || '').toUpperCase()`: `isOrgBoundedRole` (`keyRevokePolicy.ts:85`) and `isScopedAdminRole` (:102), and `scopes.ts:288`. A dotless-i `ıssuer_admin` is therefore org-bounded and a look-alike `ADMIN` is scoped as ADMIN (these narrow access, so they err the safe way, but the vocabulary is now split inside one file). | FOUND/TESTED by grep at head (positive control: the same grep finds the fixed `:144` line and the auth sites); not executed. |
| 1776-3 | Minor (Spark F2 confirmed, wider than Spark listed) | Other `toUpperCase` role sites remain: `services/auth/src/routes/users.ts:285,:377`, `services/originate/src/middleware/rbac.ts:56,:58`, `services/auth/src/services/password.ts:234`, the four gates in `services/auth/src/routes/issuerCerts.ts` (:69,78,92,109), and `provisioningPolicy.ts:97` (finding 1776-1) which the Spark list missed. | Grep at head, as above. |
| 1776-4 | Low | Security test R3 accepts 401 or 403 for an array role (asserts refusal, not which layer). | Read; the cell goes red under mutant B, so it discriminates. |
| 1776-5 | Low (merge-time) | Docs carry section 84 (see BLUF). | |
| 1776-6 | Info | Reachability of a dotless-i or array role from a real issuer is still not established (the ticket says so). | Not tested. |

### Spark Majors judged
- **F1 (reachability not established): SCOPE NOTE.** Same sentence is in the ticket; the PR does not claim reachability.
- **F2 (no sweep for other toUpperCase role comparisons): CONFIRMED, and understated** (findings 1776-1/2/3). Scope note for the sweep generally, but the `decideMint` site is the ticket's own measured path and deserves a named follow-up, not a general "sweep".

---

## #1780 (KS-1702, migration 055 test hardening): GO WITH NOTES (notes are merge-time)

Head ba9a24a775da (asserted). Diff vs develop: the 055 cell file +136/-14, two docs +19 each. **No migration touched** (`git diff bd6697e..ba9a24a -- Blockchain/Dev/migrations` is empty); 055 sha256 `a4d838106ffe00b6de915a8e82ce5b1a22303db97c567235802da08edf8b4500` identical at develop and head, and identical again after all mutant runs.

### Order followed
1. Spark gate half FIRST, 2. then the Claude check. The Spark half's deterministic step (spark_gate.sh) is **vacuous for this PR**: see finding 1780-H below.

### Spark gate half (`out_p1780/` in the work folder)
- `spark_gate.sh` (28 s) wrote facts.json; targeted run on HEAD and on BASE product code both "files_failed 1, passed 0, failed 0".
- `spark_review.py` (ticket KS-1702; the two Projects Documents html files removed from the full-text section of a copy of the facts, `facts_spark.json`, plus a HARNESS LIMIT line added to `not_run` so the model was not told "0 failed" as a result): 1 attempt, 24,398 prompt tokens, 1,006 completion tokens, 54.9 s, valid JSON, **verdict NO GO**: 2 Major, 2 Minor, 1 Note. Prompt 78 KB.

### Claude check (one container, `gate2-pg-1780`, postgres:15-alpine, 127.0.0.1:55431)
Real PostgreSQL **15.19** (aarch64 musl). Built as the PR doc says: `docker/init` mounted read-only, then the repo's own `scripts/run-migrations.sh` inside the container over a copy of `migrations/` with 055 left out (applied=56 failed=0), then checked: `documents` and `action_provenance` have FORCE RLS, `secuura_app` is non-superuser, no BYPASSRLS. Run with the service's own `jest.integration.config.js`, all cells including RLS (0 skipped).

| # | Check | Result |
|---|---|---|
| C1 | New file at head, real 055 (env unset) | **20 passed / 20** (SETUP, SEAM, FORWARD, B1a, B1b, NOPARENTROW, FORGE1, FORGE2, HUMANOBO, CROSSTENANT, O3, O4, REPORT, NOMINTER, MULTI, UNTOUCHED, NEVER WRITES, IDEMPOTENT, REVERSE, RLS) |
| C2 | Base file at develop | **17 / 17** |
| C3 | M0 control: byte-identical copy of 055 via the seam | 20 / 20 (so SEAM does not fire on a faithful copy) |
| C4 | **O3** (delete line 145, the `ap.tenant_id = p.tenant_id` of the `parent_agrees` half only) | exactly **3 red: SEAM, O3, REPORT**; 17 green |
| C5 | **O4** (both halves scoped on `d.tenant_id`, lines 140 and 145) | exactly **3 red: SEAM, O4, REPORT**; 17 green |
| C6 | SEAM when the seam points at a non-real file | `S` = real 055 plus one trailing comment line: **only SEAM red** (1 failed / 19 passed). A non-existent path: every cell fails with ENOENT. `/dev/null`: fails on the marker `toContain`. |
| C7 | Real 055 sha256 unchanged | `a4d83810...b4500` at start, after all runs, and at the end |
| C8 | Cleanup: tenants, marker rows, `doc-055-*` documents left in the DB after head, M0, O3, O4, O1, S, F and missing-file runs | **0 / 0 / 0** |

Extra mutants (not asked, beyond the PR's claim):
- **O1** (scope removed from the `parent_rows` half alone; the PR's doc says "not tried"): red = SEAM + REPORT only. So REPORT, not a named O cell, is what catches O1.
- **F** (055 made to credit the foreign T3 document): red = SEAM + REPORT, 18 green. This is the direct test of Spark finding 2.

Container removed by exact name: `docker rm -f gate2-pg-1780` printed the name; `docker ps -a` read back: **0 containers matching gate2** (the other seats' containers untouched).

### Can the env seam ever load a non-real migration in production?
`KS1557_055_SQL_UNDER_TEST` appears in exactly three files in the whole PR head (`git grep` and a filesystem grep excluding node_modules): the test file itself (the declaration at line 70, comments at 40 and 304) and the two docs (text). It is read in one place, `ks1557-055-backfill.integration.test.ts:70`. It is NOT read by any `src/` runtime file, nor by `startup-migrations.ts` or `scripts/run-migrations.sh` (neither contains the name). The test file is excluded from the service build (`services/originate/tsconfig.json` excludes `src/**/*.integration.test.ts` and `src/__tests__`) and from the default jest run (`testPathIgnorePatterns` for `.integration.test.ts`). The Dockerfile builds from `tsc`. So production cannot read the seam. Residual risk, test-side only: a CI job that exports it makes SEAM red (by design), not green. **No path from the seam to a production migration.**

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1780-H | Medium for the PROCESS, none for the PR | The Spark gate half cannot measure this PR: `shadow_facts.py` runs `npx jest <file>` and the package's `jest.config.js` has `testPathIgnorePatterns: \.integration\.test\.ts$`, so jest answers "No tests found" and the facts say passed 0 / failed 0 for both sides. A reader of facts.json alone would see 0/0 and could take it for a red-and-green result. Also, the harness's "base product code + head test" arm is meaningless here (the PR changes no product code). | FOUND in `out_p1780/facts.json` and `targeted_head.log`; TESTED by reading jest.config.js and the log tail; HOW: file read. The integration suite needs `jest.integration.config.js` and a real DB, which only this Claude half supplies. |
| 1780-1 | Low (merge-time) | Section number 84 collides with #1775 and #1776 (develop is at 83). | See BLUF. |
| 1780-2 | Info | SEAM is red in EVERY red-proof run by design; the header and the doc say so. Anyone scripting "all green" around a mutant run must expect exactly SEAM + REPORT + one O cell. | Tested (C4, C5). |
| 1780-3 | Info | The suite refuses without `TEST_DATABASE_URL`, and the RLS cell silently `it.skip`s without `TEST_APP_DATABASE_URL`, so a CI run without the app DSN reads "19 passed, 1 skipped". | Read the code at line 491; not run without the app DSN. |

### Spark findings judged
- **Major 1 (cleanup deletes any new marker row in any tenant, not scoped to the run's tenants): SCOPE NOTE, disclosed by the PR.** The PR's own doc says "Not covered: a second process writing marker rows while the suite runs would have its rows removed too." My runs show the cleanup leaving 0 rows after real and mutant runs and not touching pre-existing rows (REVERSE and the snapshot logic). A marker row is only ever written by 055, so the exposure needs a second 055 run against the same DB during the suite. Not a defect.
- **Major 2 (REPORT's tenant scope would pass a mutant that credits the foreign T3 document): NOT REPRODUCED, shown by mutant F.** REPORT also asserts `printedAll.has(fForeign)` is true; a mutant that credits fForeign stops printing it as skipped and REPORT goes red (measured: SEAM + REPORT red, 18 green).
- **Minor (O4 control could be satisfied by a different connector's row): NOT REPRODUCED.** The control's query filters `connector_id = C1`, and the main assertion `rows toEqual([])` over every `create`/`create:connector` row for the child would go red under any extra credited row (O4 mutant does).
- **Minor (SEAM only proves the override is byte-identical): BY DESIGN, not a defect.** A byte-identical copy IS the real migration for the purpose of the test; M0 confirms it is green, S confirms any difference is red.
- **Note (docs make it not "test-only"): NOT A FINDING.** Test-only describes the code; the two-doc rule adds the docs.

### Calibration row (Spark review vs this check, #1780)

| | Spark review (deepseek-v4-flash-0731) | This Claude check |
|---|---|---|
| Verdict | NO GO | GO WITH NOTES |
| Majors | 2 | 0 |
| Minors | 2 | 0 |
| Defects confirmed | 0 | 0 |
| What it was working from | facts.json showing 0/0 (vacuous) plus the diff and the test file text (the two html docs removed from full text) | real PG 15, 20/20, 17/17, 5 mutants (O3, O4, O1, F, S), sha256, seam read sites |
| Cost | 54.9 s, 24.4k prompt tokens | roughly 15 min wall, mostly container and jest time |
| Verdict of the verdict | **False NO GO**: Major 1 is a disclosed scope note; Major 2 is refuted by a mutant; the three small findings are non-defects. It did read the test text well enough to find the real design edges (cleanup scope, report scope), which are worth keeping as questions, but it escalated each to a Major without running one case. | |
Reading: on a DB-backed test file the Spark has no way to run, a Spark NO GO is a prompt to run the mutant, not a defect signal. Same pattern as the Spark half's NO GO on #1775 and #1776 (all three Spark NO GOs have so far come with zero confirmed defects; the #1776 sweep gap that I found, `decideMint`, is something the Spark did NOT find, because its F2 asked for a sweep generically and listed the wrong sites).

---

## Merge-tree (job 3)

All by `git merge-tree --write-tree --name-only` on my own clone, SHA heads, develop = bd6697e079fc.

| merge | rc | result |
|---|---|---|
| develop + #1775 | 0 | clean (tree 5f06cb50186a) |
| develop + #1776 | 0 | clean (tree 1367fddb3ff9) |
| develop + #1780 | 0 | clean (tree e33ca1d8f246) |
| #1775 vs #1776, and #1776 vs #1775 | 1 | conflicts in exactly the two Projects Documents html files, nothing else |
| #1775 vs #1780, and #1780 vs #1775 | 1 | same two docs only |
| #1776 vs #1780, and #1780 vs #1776 | 1 | same two docs only |

**No PR touches another's code files:** non-doc file sets are 2 (#1775), 4 (#1776), 1 (#1780); pairwise intersections are 0, 0, 0; control (a set against itself) returns 4, so the intersection tool is not vacuous. Because each head is a direct child of the same develop commit and each docs block is a pure insertion before `</body>`, every conflict is the same "both appended at the same point" shape; resolving by keeping both blocks, in the merge order above, and renumbering 84/85/86, is mechanical. I did not execute a resolved three-way merge.

## What I did NOT test

- Any other service's suite (#1775/#1776 consumers) and the services/security full suite; the services/auth half of KS-1467; any HTTP route end-to-end for `POST /api/keys` (only `decideMint` the function, finding 1776-1).
- `constructor.name` / `err.name` consumers of the shared subclasses (grep too noisy to claim).
- The four platform suites, a running stack, any deploy, Node 24 (the host has only Node 26.8.1), amd64 Postgres (host is aarch64), PG versions other than 15.19, CI itself.
- The #1780 suite with `TEST_APP_DATABASE_URL` unset (RLS skipped); other single-half mutants beyond O1, O3, O4, F, S; concurrent writers during the suite (the PR's own stated gap).
- Doc accuracy beyond heading structure, insertion shape, and a handful of figures (17/17, 20/20, line 145 of 187 for O3, the mutant list); the doc html checkers named in the gate-c verdict were not run.
- The cause of the `ks1000` failure in the Spark half's #1779 run (could not reproduce; #1779 is outside this batch).
- Linear: read only KS-1467, KS-1591, KS-1536 (comments first:100); KS-1702 was fetched by the Spark review script's own read.

## Evidence locations (work folder `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate2-1775-1776-1780/`)
`out_p1780/` (facts, diff, `spark/review.json`, prompts), `claude1780/` (head/base/mutant jest logs), `mut/` (#1775/#1776 mutation logs), `suites/` (shared and auth suite JSON). Scratch: `/private/tmp/claude-501/gatework2/` (mutant 055 copies in `mut/`, merge-tree outputs `mt_*.txt`).
